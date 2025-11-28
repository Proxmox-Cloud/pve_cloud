import os
import re
from ansible.utils.display import Display
import yaml
import json
from ansible_collections.pve.cloud.plugins.module_utils.validate import validate_schema, validate_schema_ext
from ansible_collections.pve.cloud.plugins.module_utils.identity import sort_and_hash
from ansible_collections.pve.cloud.plugins.module_utils.network import check_host_ssh_online, wait_for_ssh_open
import asyncio, asyncssh
from dataclasses import dataclass
import ipaddress
from pve_cloud_schemas.validate import validate_inventory

@dataclass
class PveHost:
    hostname: str
    cloud_domain: str
    cluster_name: str
    params: dict


@dataclass
class Information:
    cluster_vars: dict
    pvesh_vms: dict
    host_ha_groups: dict
    first_online_host: PveHost


# ansible logger
display = Display()


def get_pve_inventory_yaml(loader, inv_yaml_data):
    pve_inventory = loader.load_from_file(inv_yaml_data["pve_cloud_pytest"]["dyn_inv_path"]) if "pve_cloud_pytest" in inv_yaml_data else loader.load_from_file(os.path.expanduser("~/.pve-cloud-dyn-inv.yaml"))
    try:
        validate_inventory(yaml_data)
    except jsonschema.ValidationError as e:
        raise AnsibleParserError(e.message)

    return pve_inventory


async def get_online_pve_hosts(loader, yaml_data):
    pve_inventory = get_pve_inventory_yaml(loader, yaml_data)
    target_pve = yaml_data["target_pve"]

    # todo: determine cloud domain of target_pve and only load online pve hosts fron there
    target_cloud = None
    for cloud_domain in pve_inventory:
        for pve_cluster in pve_inventory[cloud_domain]:
            if pve_cluster + "." + cloud_domain == target_pve:
                target_cloud = cloud_domain
                break
    
    if target_cloud is None:
        raise Exception(f"Could not identify cloud for {target_pve}")

    display.v(f"identified {target_cloud}")

    # determine online hosts async
    online_host_tasks = []
    for pve in pve_inventory[target_cloud]:
        for host, params in pve_inventory[target_cloud][pve].items():
            online_host_tasks.append(check_host_ssh_online(PveHost(host, target_cloud, pve, params)))

    return [fqdn_host[1] for fqdn_host in (await asyncio.gather(*online_host_tasks)) if fqdn_host[0]]


async def fetch_task(conn, command, ret_key):
    display.v(f"running cmd {command}")
    cmd = await conn.run(command, check=True)
    return {ret_key: cmd.stdout}


async def fetch_pve_cluster_info(pve_host_of_cluster):
    fetch_tasks = []

    async with asyncssh.connect(pve_host_of_cluster.params['ansible_host'], username='root', known_hosts=None) as conn:
        fetch_tasks.append(fetch_task(conn, "cat /etc/pve/cloud/cluster_vars.yaml", "cluster_vars"))
        fetch_tasks.append(fetch_task(conn, "pvesh get /cluster/resources --type vm --output-format json", "pvesh_vms"))
        fetch_tasks.append(fetch_task(conn, "pvesh get /cluster/ha/groups --output yaml", "ha_groups"))
        
        # merge the resulting dicts
        merged = {}
        for result in await asyncio.gather(*fetch_tasks):
            merged |= result

        # parse the results of the commands
        cluster_vars = yaml.safe_load(merged["cluster_vars"])
        pvesh_vms = json.loads(merged["pvesh_vms"])
        ha_groups = yaml.safe_load(merged["ha_groups"])

        # create map with host as key and ha group memberships as list value
        host_ha_groups = {}

        for group in ha_groups:
            for node in group['nodes'].split(','):
                parsed_host = node.split(':')[0] if ':' in node else node

                if parsed_host not in host_ha_groups:
                    host_ha_groups[parsed_host] = []
                
                host_ha_groups[parsed_host].append(group['group'])

        return pve_host_of_cluster.cluster_name + "." + pve_host_of_cluster.cloud_domain, Information(cluster_vars, pvesh_vms, host_ha_groups, pve_host_of_cluster)

    
async def get_cluster_map(inventory, online_pve_hosts):
    # add pve clusters as groups + fetch information via pvesh
    cluster_fetch_tasks = []
    added_pve_cluster_groups = []
    for pve_host in online_pve_hosts:
        # replace anything that is NOT a letter, digit, or underscore
        group_name = re.sub(r"[^A-Za-z0-9_]", "_", pve_host.cluster_name) 
        if group_name in added_pve_cluster_groups:
            continue

        # create inventory groups
        added_pve_cluster_groups.append(group_name)
        inventory.add_group(group_name)

        cluster_fetch_tasks.append(fetch_pve_cluster_info(pve_host))

    # contains the needed fetched information of all clusters in our user local inventory
    cluster_map = {cluster_name: information for cluster_name, information in (await asyncio.gather(*cluster_fetch_tasks))}
    return cluster_map


def build_pve_inventory(inventory, yaml_data, online_pve_hosts, cluster_map):
    # build the pve hosts inventory grouped by cluster
    inventory.add_group('target_pve')

    for pve_host in online_pve_hosts:
        host_fqdn = f"{pve_host.hostname}.{pve_host.cluster_name}"
        cluster = cluster_map[pve_host.cluster_name + "." + pve_host.cloud_domain]

        group_name = re.sub(r"[^A-Za-z0-9_]", "_", pve_host.cluster_name)

        inventory.add_host(host_fqdn, group=group_name)

        if pve_host.cluster_name + "." + pve_host.cloud_domain == yaml_data['target_pve']:
            inventory.add_host(host_fqdn, group='target_pve')

        if pve_host.hostname in cluster.host_ha_groups:
            inventory.set_variable(host_fqdn, "pve_ha_groups", cluster.host_ha_groups[pve_host.hostname])

        inventory.set_variable(host_fqdn, "pve_cluster", pve_host.cluster_name)

        inventory.set_variable(host_fqdn, 'ansible_user', 'root')
        inventory.set_variable(host_fqdn, 'ansible_host', pve_host.params['ansible_host'])
            
        # set custom variables
        if 'vars' in pve_host.params:
            for var in pve_host.params['vars']:
                inventory.set_variable(host_fqdn, var, pve_host.params['vars'][var])

    # set cluster vars from target cluster
    target_cluster = cluster_map[yaml_data['target_pve']]

    for key in target_cluster.cluster_vars.keys():
        inventory.set_variable('all', key, target_cluster.cluster_vars[key]) 


async def add_lxc_to_inv(inventory, online_pve_hosts, target_pve, vm):
    # determine if the host the lxc is running on is online, need it for pct commands
    hosting_pve = None
    for pve_host in online_pve_hosts:
        if pve_host.hostname == vm['node'] and pve_host.cluster_name + "." + pve_host.cloud_domain == target_pve:
            hosting_pve = pve_host
            break
    
    if hosting_pve is None:
        raise Exception(f"PVE Host of lxc {vm['vmid']} is offline!")
    
    # attempt to get the ip of the lxc
    ip = None

    async with asyncssh.connect(hosting_pve.params['ansible_host'], username='root', known_hosts=None) as pve_conn:
        max_retries = 30
        for attempt in range(max_retries):
            try:
                pct_ip_show_cmd = await pve_conn.run(f"pct exec {vm['vmid']} -- ip --json a show", check=True)
     
                ip_addr_show = json.loads(pct_ip_show_cmd.stdout)

                # first is lo, second is main interface, first info of second is ipv4
                # todo: identify via cluster vm subnet
                ip = ip_addr_show[1]['addr_info'][0]['local'] 

                if ip is not None:
                    display.display(f"Got ip {ip} for {vm['vmid']} on attempt {str(attempt+1)}")
                    break
            except Exception as e:
                display.v(f"Exception running pct exec {e} {type(e)}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(1)
                else:
                    raise Exception(f"All attempts failed for {vm['vmid']}.")
                    
    if ip is None:
        raise Exception(f"Could not get ip for vm {vm['vmid']}")
    
    inventory.set_variable(vm['name'], "ansible_host", ip)

    open_ssh_port = await wait_for_ssh_open(ip)

    if open_ssh_port is None:
        raise Exception(f"Can't reach SSH server on {ip}")

    if open_ssh_port != 22:
        inventory.set_variable(vm['name'], "ansible_port", open_ssh_port)

    # try load cloud vars for container if they exist
    async with asyncssh.connect(ip, username='root', known_hosts=None, port=open_ssh_port) as lxc_conn:
        try:
            cat_lxc_cloud_vars = await lxc_conn.run("cat /etc/pve-cloud-vars.yaml", check=True)
            pve_cloud_vars = yaml.safe_load(cat_lxc_cloud_vars.stdout)

            if pve_cloud_vars:
                for key in pve_cloud_vars.keys():
                    inventory.set_variable(vm['name'], key, pve_cloud_vars[key])
            else:
                display.v(f"No cloud vars defined for {vm['name']}") 

        except asyncssh.ProcessError as e:
            display.warning(f"Error trying to load pve-cloud-vars.yaml on lxc {e}")


async def add_qemu_to_inv(inventory, cluster, vm):
    ip = None
    async with asyncssh.connect(cluster.first_online_host.params['ansible_host'], username='root', known_hosts=None) as pve_conn:
        max_retries = 80
        ip = None
        for attempt in range(max_retries):
            try:
                pvesh_qemu_ifaces = await pve_conn.run(f"pvesh get /nodes/{vm['node']}/qemu/{vm['vmid']}/agent/network-get-interfaces --output-format json", check=True)

                interfaces = json.loads(pvesh_qemu_ifaces.stdout)

                for interface in interfaces['result']:
                    for address in interface['ip-addresses']:
                        try:
                            parsed = ipaddress.IPv4Address(address['ip-address'])
                            if parsed in ipaddress.IPv4Network(cluster.cluster_vars['pve_vm_subnet'], strict=False):
                                ip = address['ip-address']
                                break
                        except ValueError as e:
                            pass
                    if ip is not None:
                        break

                if ip is not None:
                    display.display(f"Got ip {ip} on attempt " + str(attempt + 1))
                    break
                
            except Exception as e:
                if attempt < max_retries - 1:
                    await asyncio.sleep(5)
                else:
                    raise Exception("All attempts failed.")

        if ip is None:
            raise Exception(f"Could not find ip for vmid {vm['vmid']}")
        
        inventory.set_variable(vm['name'], "ansible_host", ip)

        open_ssh_port = await wait_for_ssh_open(ip)

        if open_ssh_port is None:
            raise Exception(f"Can't reach SSH server on {ip}")


async def include_stack(inventory, online_pve_hosts, cluster_map, include_fqdn, host_group, qemu_ansible_user):
    # determine vms to actually include
    include_vms = []
    matched_cluster_fqdn = None
    for cluster_fqdn, cluster in cluster_map.items():
        for vm in cluster.pvesh_vms:
            if 'tags' in vm:
                tags = vm['tags'].split(';')
                if include_fqdn in tags:
                    if matched_cluster_fqdn is not None and matched_cluster_fqdn != cluster_fqdn:
                        raise Exception(f"Stack to include is in multiple pve clusters {include_fqdn} - unexpected behaviour {cluster_fqdn}/{matched_cluster_fqdn}")

                    # append and set single source pve cluster variable
                    include_vms.append(vm)
                    matched_cluster_fqdn = cluster_fqdn


    if matched_cluster_fqdn is None:
        raise Exception(f"Couldnt match cluster for include {include_fqdn}")
    
    inventory.add_group(host_group)

    add_to_inv_tasks = []
    for vm in include_vms:
        inventory.add_host(vm['name'], group=host_group)
        if vm['type'] == 'lxc':
            inventory.set_variable(vm['name'], "ansible_user", "root")
            add_to_inv_tasks.append(add_lxc_to_inv(inventory, online_pve_hosts, matched_cluster_fqdn, vm))
        elif vm['type'] == 'qemu':
            inventory.set_variable(vm['name'], "ansible_user", qemu_ansible_user)
            add_to_inv_tasks.append(add_qemu_to_inv(inventory, cluster_map[matched_cluster_fqdn], vm))
        else:
            raise Exception(f"Unknown vm type discovered {vm['type']}")
    
    await asyncio.gather(*add_to_inv_tasks)



# generic init plugin function called by most inventory plugins
async def init_plugin(loader, inventory, yaml_data, plugin_dir):
    plugin_name = yaml_data["plugin"].split(".")[-1]

    try:
        validate_inventory(yaml_data)
    except jsonschema.ValidationError as e:
        raise AnsibleParserError(e.message)

    # get pve hosts that are online
    online_pve_hosts = await get_online_pve_hosts(loader, yaml_data)
    display.v("num online_pve_hosts", len(online_pve_hosts))

    cluster_map = await get_cluster_map(inventory, online_pve_hosts)
    display.v("len cluster map", len(cluster_map))
    target_cluster = cluster_map[yaml_data['target_pve']]

    installed_pve_cloud_version = target_cluster.cluster_vars['pve_cloud_collection_version']

    # compare installed version with version we are using, crash on missmatch
    collection_path = os.path.dirname(os.path.dirname(__file__))
    manifest_path = os.path.join(collection_path, "MANIFEST.json")
    with open(manifest_path, "r") as f:
        manifest = json.load(f)
        manifest_version = manifest.get("version")

    if installed_pve_cloud_version != manifest_version:
        raise Exception(f"Version missmatch! Cloud version: {installed_pve_cloud_version}, local version: {manifest_version}! Please update pve_cloud on your machine / run all setup playbooks again!")

    build_pve_inventory(inventory, yaml_data, online_pve_hosts, cluster_map)

    # include other stacks async
    include_tasks = []

    display.v("running includes")

    if "static_includes" in yaml_data:
        for host_group, static_fqdn in yaml_data["static_includes"].items():
            include_tasks.append(include_stack(inventory, online_pve_hosts, cluster_map, static_fqdn, host_group, "admin"))

    if "include_stacks" in yaml_data:
        for stack in yaml_data["include_stacks"]:
            include_tasks.append(include_stack(inventory, online_pve_hosts, cluster_map, stack["stack_fqdn"], stack["host_group"], stack["qemu_ansible_user"] if "qemu_ansible_user" in stack else "admin"))

    await asyncio.gather(*include_tasks)
    display.v("done running includes")

    # now we get to the stack specific code
    stack_fqdn = f"{yaml_data['stack_name']}.{target_cluster.cluster_vars['pve_cloud_domain']}"

    # extract vms that belong to this stack
    stack_vms = []
    for vm in target_cluster.pvesh_vms:
        if 'tags' in vm and stack_fqdn in vm['tags'].split(';'):
            stack_vms.append(vm)

    # generate map, id hash of vm => variables specific for vm
    vm_vars_blake = { sort_and_hash(vm): vm['vars'] if 'vars' in vm else {} for vm in yaml_data['lxcs' if 'lxcs' in yaml_data else 'qemus'] }

    return vm_vars_blake, stack_vms, online_pve_hosts, cluster_map










