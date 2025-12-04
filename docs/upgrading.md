# Upgrading Guides

## 3.5.X to 3.6.X

This change introduces proxy protocol, to minimize downtime for ingress resources apply the kubespray playbook like this with `--tags config,deployments` on the first run.