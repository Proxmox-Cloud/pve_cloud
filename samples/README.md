# Infrastructure as code Example

## cloud-instance

In the `cloud-instance/` directory you will find an example of how to setup core lxcs needed for the cloud to function.

The `playbooks.sh` script contains all commands in the needed order, to boostrap and setup core cloud services:

* Kea DHCP - Provide DHCP for your dedicated vlan your cloud machines will live in
* Bind DNS - DynDNS with Kea for machines and k8s ingress dns
* Patroni Postgres - central store for persistent configuration of the cloud, TLS certificates, terraform states, ...
* HAProxy - central loadbalancer of a proxmox cluster inside a pve cloud (if you have multiple proxmox clusters you can also deploy multiple proxies). Has public and private floating ips aswell as routing based on sni inspection with names defined in kubernetes inventory file definitions

## kubespray-cluster

The `kubespray-cluster/` contains an example inventory for a kubespray cluster aswell as example terraform configuration for authenticating. 