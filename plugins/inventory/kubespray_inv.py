from ansible.plugins.inventory import BaseInventoryPlugin
from ansible_collections.pve.cloud.plugins.module_utils.inventory import init_plugin, add_qemu_to_inv
from ansible_collections.pve.cloud.plugins.module_utils.identity import stack_vm_get_blake
import os
import asyncio
import paramiko
import secrets

# keys in the yaml inventory that will be set as variables to all hosts in the play
GLOBAL_KEYS = [
    "qemus", "stack_name", "pve_ha_group", "extra_control_plane_sans",
    "qemu_network_config", "qemu_base_parameters", "qemu_image_url", 
    "root_ssh_pub_key", "qemu_keyboard_layout", "cluster_cert_entries", "external_domains",
    "tcp_proxies", "qemu_hashed_pw", "qemu_default_user", 
    "acme_staging", "ceph_csi_sc_pools", "static_includes", "squid_cache_settings", "qemu_global_vars"
]

class InventoryModule(BaseInventoryPlugin):

    def verify_file(self, path):
        valid = False
        if super(InventoryModule, self).verify_file(path):
            # base class verifies that file exists and is readable by current user
            if path.endswith('.yml') or path.endswith('.yaml'):
                valid = True
        return valid


    def get_or_create_kubeadm_cert_key(self, target_cluster, stack_fqdn):
        client = paramiko.SSHClient() # connect to any of the pve hosts
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(target_cluster.first_online_host.params['ansible_host'], port=22, username='root')

        stdin, stdout, stderr = client.exec_command(f'test -f /etc/pve/cloud/kubespray-kubeadm-cert-keys/{stack_fqdn} && echo exists || echo notexists')
        file_exists = stdout.read().strip().decode('utf-8') == 'exists'

        if file_exists:
            stdin, stdout, stderr = client.exec_command(f'cat /etc/pve/cloud/kubespray-kubeadm-cert-keys/{stack_fqdn}')
            kubeadm_cert_key = stdout.read().strip().decode('utf-8')
        else:
            kubeadm_cert_key = ''.join(secrets.choice('0123456789abcdef') for _ in range(64))
            stdin, stdout, stderr = client.exec_command(f'echo "{kubeadm_cert_key}" > /etc/pve/cloud/kubespray-kubeadm-cert-keys/{stack_fqdn}')
        
        client.close()
        return kubeadm_cert_key  


    def set_global_vars(self, yaml_data, inventory):
        for key in GLOBAL_KEYS:
            if key in yaml_data:
                inventory.set_variable('all', key, yaml_data[key])


    async def stack_qemus(self, inventory, stack_vms, target_cluster):
        add_tasks = []
        for vm in stack_vms:
            inventory.add_host(vm['name'], group="all")
            add_tasks.append(add_qemu_to_inv(inventory, target_cluster, vm))
        
        await asyncio.gather(*add_tasks)


    def parse(self, inventory, loader, path, cache=True):
        super(InventoryModule, self).parse(inventory, loader, path, cache)
        yaml_data = loader.load_from_file(path)

        vm_vars_blake, stack_vms, online_pve_hosts, cluster_map = asyncio.run(init_plugin(loader, inventory, yaml_data, os.path.dirname(os.path.realpath(__file__))))

        target_cluster = cluster_map[yaml_data['target_pve']]

        stack_fqdn = f"{yaml_data['stack_name']}.{target_cluster.cluster_vars['pve_cloud_domain']}"
        
        self.set_global_vars(yaml_data, inventory)

        # kubespray groups
        inventory.add_group('kube_control_plane')
        inventory.add_group('etcd')
        inventory.add_group('kube_node')
        inventory.add_group('calico_rr')
        inventory.add_group('k8s_cluster')
        inventory.add_child('k8s_cluster', 'kube_control_plane')
        inventory.add_child('k8s_cluster', 'kube_node')
        inventory.add_child('k8s_cluster', 'calico_rr')

        # genereate or get cert key for kubeadm cluster bootstrap
        inventory.set_variable('k8s_cluster', 'kubeadm_certificate_key', self.get_or_create_kubeadm_cert_key(target_cluster, stack_fqdn))

        # set additional san for control plane, direct access via dns master record set and control plane record via haproxy
        extra_sans = [f"masters-{stack_fqdn}", "control-plane-" + stack_fqdn]
        
        # controlplane can be optionally exposed externally under special san
        if "extra_control_plane_sans" in yaml_data:
            extra_sans.extend(yaml_data["extra_control_plane_sans"])  
        
        inventory.set_variable('k8s_cluster', 'supplementary_addresses_in_ssl_keys', extra_sans)

        asyncio.run(self.stack_qemus(inventory, stack_vms, target_cluster))
        
        # set / overwrite kubespray specific vars for host
        for vm in stack_vms:
            tags = vm['tags'].split(';')
            hostname = vm['name']

            inventory.set_variable(hostname, 'ansible_user', 'admin' if 'qemu_default_user' not in yaml_data else yaml_data['qemu_default_user'])
            inventory.set_variable(hostname, 'ansible_become', True) # needed for kubespray playbook execution

            blake = stack_vm_get_blake(vm)

            # check if we can match the id to our inventory file
            if blake in vm_vars_blake:
                # set vars für container specific tasks
                for key, var in vm_vars_blake[blake].items():
                    inventory.set_variable(hostname, key, var)

            if 'master' in tags:
                inventory.add_host(hostname, group='kube_control_plane')
                inventory.add_host(hostname, group='etcd')
                inventory.set_variable(hostname, 'etcd_member_name', f'etcd-{hostname}')
            
            if 'worker' in tags:
                inventory.add_host(hostname, group='kube_node')
        
            # set global qemu vars if defined
            if "qemu_global_vars" in yaml_data:
                for key, var in yaml_data["qemu_global_vars"].items():
                    inventory.set_variable(hostname, key, var) 