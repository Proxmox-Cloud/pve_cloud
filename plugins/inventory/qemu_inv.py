
from ansible.plugins.inventory import BaseInventoryPlugin
import os
import asyncio
from ansible_collections.pxc.cloud.plugins.module_utils.inventory import init_plugin, add_qemu_to_inv
from ansible_collections.pxc.cloud.plugins.module_utils.identity import stack_vm_get_blake


class InventoryModule(BaseInventoryPlugin):

    def verify_file(self, path):
        valid = False
        if super(InventoryModule, self).verify_file(path):
            # base class verifies that file exists and is readable by current user
            if path.endswith('.yml') or path.endswith('.yaml'):
                valid = True
        return valid


    def set_global_vars(self, yaml_data, inventory):
        for key in yaml_data:
            inventory.set_variable('all', key, yaml_data[key])


    async def stack_qemus(self, inventory, stack_vms, target_cluster):
        add_tasks = []
        for vm in stack_vms:
            inventory.add_host(vm['name'], group="qemus")
            add_tasks.append(add_qemu_to_inv(inventory, target_cluster, vm))
        
        await asyncio.gather(*add_tasks)


    def parse(self, inventory, loader, path, cache=True):
        super(InventoryModule, self).parse(inventory, loader, path, cache)
        yaml_data = loader.load_from_file(path)

        vm_vars_blake, stack_vms, online_pve_hosts, cluster_map = asyncio.run(init_plugin(loader, inventory, yaml_data, os.path.dirname(os.path.realpath(__file__))))

        target_cluster = cluster_map[yaml_data['target_pve']]

        stack_fqdn = f"{yaml_data['stack_name']}.{target_cluster.cluster_vars['pve_cloud_domain']}"

        self.set_global_vars(yaml_data, inventory)

        inventory.add_group('qemus')

        asyncio.run(self.stack_qemus(inventory, stack_vms, target_cluster))

        # set / overwrite kubespray specific vars for host
        for vm in stack_vms:
            tags = vm['tags'].split(';')
            hostname = vm['name']

            inventory.set_variable(hostname, 'ansible_user', 'admin' if 'qemu_default_user' not in yaml_data else yaml_data['qemu_default_user'])
            inventory.set_variable(hostname, 'ansible_become', True) # needed for kubespray playbook execution

            inventory.set_variable(hostname, 'cloud_machine_type', 'qemu') # machine type for cloud logic

            blake = stack_vm_get_blake(vm)
            # check if we can match the id to our inventory file
            if blake in vm_vars_blake:
                # set vars für container specific tasks
                for key, var in vm_vars_blake[blake].items():
                    inventory.set_variable(hostname, key, var)
                    
            # set global qemu vars if defined
            if "qemu_global_vars" in yaml_data:
                for key, var in yaml_data["qemu_global_vars"].items():
                    inventory.set_variable(hostname, key, var) 