import asyncio
import os

from ansible.plugins.inventory import BaseInventoryPlugin
from ansible.utils.display import Display
from ansible_collections.pxc.cloud.plugins.module_utils.identity import \
    stack_vm_get_blake
from ansible_collections.pxc.cloud.plugins.module_utils.inventory import (
    add_lxc_to_inv, init_plugin)

display = Display()


class InventoryModule(BaseInventoryPlugin):

    def verify_file(self, path):
        valid = False
        if super(InventoryModule, self).verify_file(path):
            # base class verifies that file exists and is readable by current user
            if path.endswith(".yml") or path.endswith(".yaml"):
                valid = True
        return valid

    def set_global_vars(self, yaml_data, inventory):
        for key in yaml_data:
            inventory.set_variable("all", key, yaml_data[key])

    async def stack_lxcs(self, inventory, online_pve_hosts, stack_vms, cluster_name):
        add_tasks = []
        for vm in stack_vms:
            inventory.add_host(vm["name"], group="lxcs")
            inventory.set_variable(vm["name"], "ansible_user", "root")
            add_tasks.append(
                add_lxc_to_inv(inventory, online_pve_hosts, cluster_name, vm)
            )

        await asyncio.gather(*add_tasks)

    def parse(self, inventory, loader, path, cache=True):
        super(InventoryModule, self).parse(inventory, loader, path, cache)
        yaml_data = loader.load_from_file(path)

        vm_vars_blake, stack_vms, online_pve_hosts, cluster_map = asyncio.run(
            init_plugin(
                loader,
                inventory,
                yaml_data,
                os.path.dirname(os.path.realpath(__file__)),
            )
        )
        display.v("vm_vars_blake", vm_vars_blake)
        self.set_global_vars(yaml_data, inventory)

        # build lxcs inventory
        inventory.add_group("lxcs")

        display.v("running stack includes")
        asyncio.run(
            self.stack_lxcs(
                inventory, online_pve_hosts, stack_vms, yaml_data["target_pve"]
            )
        )
        display.v("done running stack includes")

        # set host specific vars
        for vm in stack_vms:
            hostname = vm["name"]

            inventory.set_variable(
                hostname, "cloud_machine_type", "lxc"
            )  # machine type for cloud logic

            # get hash to map variables
            blake = stack_vm_get_blake(vm)

            # set the id for use in playbooks
            inventory.set_variable(hostname, "pxc_blake_id", blake)

            # check if we can match the id to our inventory file
            if blake in vm_vars_blake:
                # set vars für container specific tasks
                for key, var in vm_vars_blake[blake].items():
                    inventory.set_variable(hostname, key, var)

                # set entire variable dict to seperate variable
                # will be written out so its there for includes
                inventory.set_variable(hostname, "vm_vars_blake", vm_vars_blake[blake])

            # set global lxc vars if defined
            if "lxc_global_vars" in yaml_data:
                for key, var in yaml_data["lxc_global_vars"].items():
                    inventory.set_variable(hostname, key, var)
