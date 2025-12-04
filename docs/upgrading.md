# Upgrading Guides

Simply upgrade the collection in your `requirements.yaml`, then run `ansible-galaxy install -r requirements.yaml` and `ansible-playbook pve.cloud.setup_control_node` again.

## 3.5.X to 3.6.X

This change introduces proxy protocol, to minimize downtime for ingress resources apply the kubespray playbook like this with `--tags config,deployments` on the first run.