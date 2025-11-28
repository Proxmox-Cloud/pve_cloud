# pve-cloud sample config

## cloud-instance

In the `cloud-instance/` directory you will find an example of how to setup core lxcs needed for the cloud to function.

The `playbooks.sh` script contains all commands in the needed order, to boostrap and setup core cloud services:

* Kea DHCP - Provide DHCP for your dedicated vlan your cloud machines will live in
* Bind DNS - DynDNS with Kea for machines and K8S ingress dns
* Patroni Postgres - Central store for persistent configuration of the cloud, TLS Certificates, Terraform states, ...
* HAProxy - Central loadbalancer of a proxmox cluster inside a pve cloud. Has public and private floating ips aswell as routing based on service / kubernetes inventory file definitions

## kubespray-cluster

The `kubespray-cluster/` contains an example inventory for a kubespray cluster aswell as example terraform configuration for authenticating. 