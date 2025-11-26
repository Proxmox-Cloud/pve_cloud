
from ansible.plugins.inventory import BaseInventoryPlugin
from ansible_collections.pve.cloud.plugins.module_utils.inventory import get_pve_inventory_yaml
from ansible_collections.pve.cloud.plugins.module_utils.validate import validate_schema
import os
from ansible.utils.display import Display
import socket


display = Display()


def check_ssh_open(host):
    try:
        with socket.create_connection((host, 22), timeout=3):
            return True
    except (socket.timeout, ConnectionRefusedError, OSError):
        return False
    

class InventoryModule(BaseInventoryPlugin):

    def verify_file(self, path):
        valid = False
        if super(InventoryModule, self).verify_file(path):
            # base class verifies that file exists and is readable by current user
            if path.endswith('.yml') or path.endswith('.yaml'):
                valid = True
        return valid

    def parse(self, inventory, loader, path, cache=True):
        super(InventoryModule, self).parse(inventory, loader, path, cache)
        yaml_data = loader.load_from_file(path)

        validate_schema(loader, yaml_data, os.path.dirname(os.path.realpath(__file__)), "pve_cloud_inv")

        pve_inventory = get_pve_inventory_yaml(loader, yaml_data)[yaml_data['pve_cloud_domain']]
        display.v("pve_inventory", pve_inventory)

        inventory.add_group('all_pve_hosts')
        
        # contains only one pve host per pve cluster (since it uses corosync)
        inventory.add_group('pve_cluster_reps')

        # load pve clusters and set cluster variables for them
        for pve_cluster in yaml_data['pve_clusters']:
            # cluster rep group
            first = True

            for host, params in pve_inventory[pve_cluster].items():
                if not check_ssh_open(params['ansible_host']):
                    display.display(f"skipping offline host {host}")
                    continue

                fqdn_host = f"{host}.{pve_cluster}"
                inventory.add_host(fqdn_host, group='all_pve_hosts')

                # first host of pve cluster gets added to rep group
                if first:
                    inventory.add_host(fqdn_host, group='pve_cluster_reps')
                    first = False

                inventory.set_variable(fqdn_host, 'ansible_user', params['ansible_user'])
                inventory.set_variable(fqdn_host, 'ansible_host', params['ansible_host'])

                inventory.set_variable(fqdn_host, 'pve_cluster_name', pve_cluster)

                # build pve cluster vars, entire yaml vars + cluster specific vars
                inventory.set_variable(fqdn_host, "cluster_vars",  yaml_data | yaml_data['pve_clusters'][pve_cluster])

                display.v("cluster_vars",  yaml_data | yaml_data['pve_clusters'][pve_cluster])
                
                # set pve host specific vars if specified
                if host in yaml_data['pve_clusters'][pve_cluster]['pve_host_vars']:
                    # also set every key for the current host as root var
                    for var in yaml_data['pve_clusters'][pve_cluster]['pve_host_vars'][host]:
                        inventory.set_variable(fqdn_host, var, yaml_data['pve_clusters'][pve_cluster]['pve_host_vars'][host][var])



