from ansible.errors import AnsibleError, AnsibleParserError
from ansible.plugins.inventory import BaseInventoryPlugin
from ansible.utils.display import Display
from ansible_collections.pxc.cloud.plugins.module_utils.inventory import (
    build_pve_inventory, get_cluster_map, get_manifest_version,
    get_online_pve_hosts)
from jsonschema.exceptions import ValidationError
from pve_cloud.lib.ssh import get_ssh_asyncio_loop
from pve_cloud_schemas.validate import (validate_cluster_vars,
                                        validate_inventory)

display = Display()


# this is used to deploy pxc functionality on hosts that have not been initialized by the collection
# / are outside of a proxmox cluster, for example edge k0s systems / backup servers
class InventoryModule(BaseInventoryPlugin):

    def verify_file(self, path):
        valid = False
        if super(InventoryModule, self).verify_file(path):
            # base class verifies that file exists and is readable by current user
            if path.endswith(".yml") or path.endswith(".yaml"):
                valid = True
        return valid

    def parse(self, inventory, loader, path, cache=True):
        super(InventoryModule, self).parse(inventory, loader, path, cache)
        yaml_data = loader.load_from_file(path)

        try:
            validate_inventory(yaml_data)
        except ValidationError as e:
            raise AnsibleParserError(e.message)

        # todo: very hacky should be refactored. needed for build_pve_inventory
        yaml_data["target_pve"] = (
            yaml_data["target_cluster"] + "." + yaml_data["pve_cloud_domain"]
        )

        with get_ssh_asyncio_loop() as loop:

            # build nice pve inventory
            online_pve_hosts = loop.run_until_complete(
                get_online_pve_hosts(
                    loader,
                    yaml_data["target_cluster"] + "." + yaml_data["pve_cloud_domain"],
                )
            )

            cluster_map = loop.run_until_complete(
                get_cluster_map(inventory, online_pve_hosts)
            )
            display.v("len cluster map", len(cluster_map))
            target_cluster = cluster_map[
                yaml_data["target_cluster"] + "." + yaml_data["pve_cloud_domain"]
            ]

            installed_pve_cloud_version = target_cluster.cluster_vars[
                "pve_cloud_collection_version"
            ]

            # compare installed version with version we are using, crash on missmatch
            manifest_version = get_manifest_version()

            if installed_pve_cloud_version != manifest_version:
                raise AnsibleError(
                    f"Version missmatch! Cloud version: {installed_pve_cloud_version}, local version: {manifest_version}! Please update pve_cloud on your machine / run all setup playbooks again!"
                )

            build_pve_inventory(inventory, yaml_data, online_pve_hosts, cluster_map)

            inventory.set_variable(
                "all", "stack_name", yaml_data["external_stack_name"]
            )
            # todo: maybe generify
            if "host_groups" in yaml_data:
                for host_group, hosts in yaml_data["host_groups"].items():
                    inventory.add_group(host_group)

                    for host, host_vars in hosts.items():
                        inventory.add_host(host, group=host_group)

                        for key, var in host_vars.items():
                            inventory.set_variable(host, key, var)

            if "typed_host_groups" in yaml_data:
                for host_group, hosts in yaml_data["typed_host_groups"].items():
                    inventory.add_group(host_group)

                    for host, host_vars in hosts.items():
                        inventory.add_host(host, group=host_group)

                        for key, var in host_vars.items():
                            inventory.set_variable(host, key, var)
