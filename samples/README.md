# Pve Cloud Repository example

You can simply copy the files if you want to get started, but you have to go over them one by one replaceing the config with your individual values.

## cloud-instance

In the `cloud-instance/` directory you will find an example of how to setup core lxcs that serve the basic cloud services.

The `playbooks.sh` script contains all commands in the needed in the correct initial order, to boostrap and setup core cloud services:

* Kea DHCP - Provide DHCP for your dedicated vlan your cloud machines will live in
* Bind DNS - DynDNS with Kea for machines and k8s ingress dns
* Patroni Postgres - central store for persistent configuration of this cloud, TLS certificates, terraform states, ... ansible playbooks will use this database to generate configuration files.
* HAProxy - central loadbalancer of a proxmox cluster inside a pve cloud (if you have multiple proxmox clusters you can also deploy multiple proxies). Has public and private floating ips, aswell as routing based on sni inspection, that comes from domains / hosts defined in kubernetes inventory file definitions

## kubespray-cluster

The `kubespray-cluster/` contains an example inventory for a kubespray cluster aswell as example authenticated terraform configuration. By using direnv and our py-pve-cloud clis we get access to the kubernetes cluster aswell as dns and secrets via nothing but ssh.