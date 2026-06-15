import os
import sys

from ansible.errors import AnsibleParserError
from ansible.plugins.inventory import BaseInventoryPlugin
from ansible.utils.display import Display
from ansible_collections.pxc.cloud.plugins.module_utils.inventory import \
    get_manifest_version
from jsonschema.exceptions import ValidationError
from pve_cloud.lib.inventory import get_pve_inventory
from pve_cloud.lib.ssh import check_ssh_open
from pve_cloud_schemas.validate import validate_inventory

display = Display()


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

        # skip validation, only in this case since in the playbooks associated with
        # pve cloud inv we set the py_pve_cloud_version cluster var
        pve_inventory = get_pve_inventory(
            yaml_data["pve_cloud_domain"],
            skip_py_cloud_check=True,
            fetch_other_pve_hosts=True,
        )

        display.v("pve_inventory", pve_inventory)

        inventory.add_group("all_pve_hosts")

        # contains only one pve host per pve cluster (since it uses corosync)
        inventory.add_group("pve_cluster_reps")

        # jumphost config if present
        inventory.add_group("jump_hosts")

        # get the collection version
        manifest_version = get_manifest_version()

        # parse py-pve-cloud version
        collection_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

        py_pve_cloud_version = None

        with open(
            os.path.join(collection_path, "meta/ee-requirements.txt"), "r"
        ) as reqs:
            for line_req in reqs:
                if ">=" in line_req:
                    # pessimistic trick is only for e2e, its still fixxed
                    req_split = line_req.split(">=")

                    if req_split[0] == "py-pve-cloud":
                        py_pve_cloud_version = req_split[1].split(",")[0].strip()
                        break

                elif "==" in line_req:  # rc release parsing
                    req_split = line_req.split("==")

                    if req_split[0] == "py-pve-cloud":
                        py_pve_cloud_version = req_split[1].strip()
                        break

        if not py_pve_cloud_version:
            raise AnsibleParserError(
                "Could not identify py-pve-cloud version in meta/ee-requirements.txt"
            )

        inventory.set_variable("all", "py_pve_cloud_version", py_pve_cloud_version)

        # load pve clusters and set cluster variables for them
        executor_set = False
        for pve_cluster in yaml_data["pve_clusters"]:
            # cluster rep group
            first = True

            # optionally determine online jump host for the cluster
            # if cluster was added through `pvcli connect-remote-cluster`
            online_jump_hosts = []
            if "jump_hosts" in pve_inventory[pve_cluster]:
                # jump hosts for cluster configured => find an online one
                for jump_host in pve_inventory[pve_cluster]["jump_hosts"]:
                    if check_ssh_open(jump_host):
                        online_jump_hosts.append(jump_host)
                        display.display(
                            f"found online jump host {jump_host} for {pve_cluster}"
                        )

                if not online_jump_hosts:
                    display.error(
                        f"jump hosts defined for {pve_cluster} but all offline / unreachable!"
                    )
                    continue

            for jump_host in online_jump_hosts:
                inventory.add_host(jump_host, group="jump_hosts")
                inventory.set_variable(jump_host, "ansible_user", "root")
                inventory.set_variable(jump_host, "ansible_host", jump_host)

            for host, params in pve_inventory[pve_cluster]["pve_hosts"].items():
                # use jump host for online check if defined + available
                if online_jump_hosts:
                    display.v(f"found jump host config for {pve_cluster}")
                    if not check_ssh_open(params["ansible_host"], online_jump_hosts[0]):
                        display.display(f"skipping offline host {host}")
                        continue
                else:
                    # else connect directly
                    if not check_ssh_open(params["ansible_host"]):
                        display.display(f"skipping offline host {host}")
                        continue

                fqdn_host = f"{host}.{pve_cluster}"
                inventory.add_host(fqdn_host, group="all_pve_hosts")

                # first host of pve cluster gets added to rep group
                if first:
                    inventory.add_host(fqdn_host, group="pve_cluster_reps")
                    first = False

                if not executor_set and online_jump_hosts:
                    # first cluster rep also becomes marked as pxc-executor-host
                    # this is needed to run generic pxc roles that require the executor set

                    inventory.add_host("pxc-executor-host")

                    inventory.set_variable("pxc-executor-host", "ansible_user", "root")
                    inventory.set_variable(
                        "pxc-executor-host", "ansible_user", params["ansible_user"]
                    )
                    inventory.set_variable(
                        "pxc-executor-host", "ansible_host", params["ansible_host"]
                    )
                    inventory.set_variable(
                        "pxc-executor-host",
                        "ansible_python_interpreter",
                        "/root/.pxc-venv/bin/python",
                    )

                    inventory.set_variable(
                        "pxc-executor-host",
                        "ansible_ssh_common_args",
                        f"-o ProxyJump=root@{online_jump_hosts[0]}",
                    )

                    executor_set = True

                inventory.set_variable(
                    fqdn_host, "ansible_user", params["ansible_user"]
                )
                inventory.set_variable(
                    fqdn_host, "ansible_host", params["ansible_host"]
                )

                # enable jump host functionality for ansible via ssh
                if online_jump_hosts:
                    inventory.set_variable(
                        fqdn_host,
                        "ansible_ssh_common_args",
                        f"-o ProxyJump=root@{online_jump_hosts[0]}",
                    )

                inventory.set_variable(
                    fqdn_host, "pve_cloud_domain", yaml_data["pve_cloud_domain"]
                )
                inventory.set_variable(fqdn_host, "pve_cluster_name", pve_cluster)

                # build pve cluster vars, entire yaml vars + cluster specific vars
                cluster_vars = yaml_data | yaml_data["pve_clusters"][pve_cluster]

                # add collection version to version check against
                cluster_vars["pve_cloud_collection_version"] = manifest_version
                cluster_vars["py_pve_cloud_version"] = py_pve_cloud_version
                cluster_vars["pve_cluster_name"] = pve_cluster

                inventory.set_variable(fqdn_host, "cluster_vars", cluster_vars)

                display.v("cluster_vars", cluster_vars)

                # set pve host specific vars if specified
                if host in yaml_data["pve_clusters"][pve_cluster]["pve_host_vars"]:
                    # also set every key for the current host as root var
                    for var in yaml_data["pve_clusters"][pve_cluster]["pve_host_vars"][
                        host
                    ]:
                        inventory.set_variable(
                            fqdn_host,
                            var,
                            yaml_data["pve_clusters"][pve_cluster]["pve_host_vars"][
                                host
                            ][var],
                        )

        # no jump host definitions, we use localhost as central executor
        if not executor_set:
            inventory.add_host("pxc-executor-host")

            inventory.set_variable("pxc-executor-host", "ansible_host", "127.0.0.1")
            inventory.set_variable("pxc-executor-host", "ansible_connection", "local")
            inventory.set_variable(
                "pxc-executor-host", "ansible_python_interpreter", sys.executable
            )
