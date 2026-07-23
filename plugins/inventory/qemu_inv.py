import asyncio

from ansible.plugins.inventory import BaseInventoryPlugin
from ansible.utils.display import Display
from ansible_collections.pxc.cloud.plugins.module_utils.identity import \
    stack_vm_get_blake
from ansible_collections.pxc.cloud.plugins.module_utils.inventory import (
    add_qemu_to_inv, init_plugin)
from pve_cloud.lib.ssh import get_ssh_asyncio_loop

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

    async def stack_qemus(self, inventory, stack_vms, target_cluster):
        add_tasks = []
        for vm in stack_vms:
            inventory.add_host(vm["name"], group="qemus")
            add_tasks.append(add_qemu_to_inv(inventory, target_cluster, vm))

        await asyncio.gather(*add_tasks)

    def parse(self, inventory, loader, path, cache=True):
        super(InventoryModule, self).parse(inventory, loader, path, cache)
        yaml_data = loader.load_from_file(path)

        with get_ssh_asyncio_loop() as loop:
            vm_params_blake, stack_vms, online_pve_hosts, cluster_map = (
                loop.run_until_complete(
                    init_plugin(
                        loader,
                        inventory,
                        yaml_data,
                    )
                )
            )

            display.v("vm_params_blake", vm_params_blake)
            target_cluster = cluster_map[yaml_data["target_pve"]]

            self.set_global_vars(yaml_data, inventory)

            inventory.add_group("qemus")

            loop.run_until_complete(
                self.stack_qemus(inventory, stack_vms, target_cluster)
            )

        # set / overwrite kubespray specific vars for host
        for vm in stack_vms:
            tags = vm["tags"].split(";")
            hostname = vm["name"]

            inventory.set_variable(
                hostname,
                "ansible_user",
                (
                    "admin"
                    if "qemu_default_user" not in yaml_data
                    else yaml_data["qemu_default_user"]
                ),
            )

            inventory.set_variable(
                hostname, "cloud_machine_type", "qemu"
            )  # machine type for cloud logic

            blake = stack_vm_get_blake(vm)

            # check if we can match the id to our inventory file
            if blake in vm_params_blake:
                # also include self reference to vm creation parameters as variables to use in playbooks
                inventory.set_variable(
                    hostname, "vm_params_self", vm_params_blake[blake]
                )

                # set specialized variables if defined
                if "vars" in vm_params_blake:
                    # set vars für container specific tasks
                    for key, var in vm_params_blake[blake]["vars"].items():
                        inventory.set_variable(hostname, key, var)

            # set global qemu vars if defined
            if "qemu_global_vars" in yaml_data:
                for key, var in yaml_data["qemu_global_vars"].items():
                    inventory.set_variable(hostname, key, var)
