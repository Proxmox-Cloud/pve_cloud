import io
import os

import paramiko
import yaml
from ansible.errors import AnsibleError, AnsibleParserError
from ansible.plugins.inventory import BaseInventoryPlugin
from jsonschema.exceptions import ValidationError
from pve_cloud_schemas.validate import validate_inventory


def get_pve_cluster_vars(target_pve_inventory):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    agent = paramiko.Agent()

    # connect to any of the pve hosts
    # todo: try hosts
    pve_host = list(target_pve_inventory.values())[0]["ansible_host"]

    if len(agent.get_keys()) > 0:
        # agent has ssh keys loaded, prioritize loaded key
        client.connect(pve_host, port=22, username="root")
    elif os.getenv("SSH_PRIVATE_KEY") is not None:
        # load key from environment, needed in awx
        loaded_key = paramiko.Ed25519Key.from_private_key(
            io.StringIO(os.getenv("SSH_PRIVATE_KEY"))
        )
        client.connect(pve_host, port=22, username="root", pkey=loaded_key)
    else:
        raise AnsibleError("No ssh keys loaded and no fallback defined")

    stdin, stdout, stderr = client.exec_command("cat /etc/pve/cloud/cluster_vars.yaml")
    cluster_vars = yaml.safe_load(stdout.read().decode("utf-8"))

    return cluster_vars


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

        target_pve = yaml_data["target_pve"]

        inventory.add_group("pve_clusters")
        inventory.add_group("target_pve")

        for cluster in yaml_data["pve_clusters"]:
            pve_cluster = yaml_data["pve_clusters"][cluster]
            for host, host_vars in pve_cluster.items():
                fqdn_host = f"{host}.{cluster}"
                inventory.add_host(fqdn_host, group="pve_clusters")

                if cluster == target_pve:
                    inventory.add_host(fqdn_host, group="target_pve")

                for host_var in host_vars:
                    inventory.set_variable(fqdn_host, host_var, host_vars[host_var])

        pve_cluster_vars = get_pve_cluster_vars(yaml_data["pve_clusters"][target_pve])

        for key in pve_cluster_vars.keys():
            inventory.set_variable("all", key, pve_cluster_vars[key])
