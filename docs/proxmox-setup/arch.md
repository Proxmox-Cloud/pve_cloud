# Architecture

For a proxmox cluster to work optimally with this project, it needs to be configured fitting the available hardware.

Depending on the storage and network bandwidth, we want to optimize for different things.

## Requirements

You need atleast one proxmox cluster to start (a single host is enough, 3 are recommended).

If you just want to test the project, you need the minimum requirements:

* 4 cores
* 32 gb of ram
* 500 gb of free disk space for vms

For a production system you would want:

* Server CPU
* 128GB+ Ram (per host)
* 2, preferably 4 disks (SSDs / NVMEs only)

The project itself has a very minimal resource footprint.

## Onprem

If you have your own machines and network architecture, an ideal setup would look like this:

* dedicated network with enough bandwidth (preferably 10/25G) dedicated for ceph
* small dedicated disks for the os, zfs raid1 is optimal here
* a seperate enterprise grade firewall with public ips / router for configuring incoming traffic

The firewall will then forward 443, 80, 6443 and any other service ports you need, to the clouds haproxy loadbalancer instances.

## Dedicated Hosts / Limited network hardware

If you dont have a dedicated switch for ceph, you might run into a bottleneck. Dedicated server providers often don't support proxmox directly / provide buggy / poorly configured setups for this projects architecture.

Ideally we want two small disks for the OS, good network and large disks for our ceph osds. Often providers don't have hardware that matches these requirements prefectly. 

To work around this limitation efficiently we do the following:

* since the network is limited often to 10G we use ceph primarily for our kubernetes volumes
* vm disks use host exclusive storage in the form of a replicated zfs volumes

If your network is limited to 10G, you should allocate 50% of your storage to ceph and the remaining 50% to zfs. During the proxmox installer, when creating zfs, you can simply choose to not use the entire disk and later on use the free partition as a ceph osd.

## Private Networks

Although the network architecture can vary drastically from setup to setup, you generally want the following private networks:

* Management network: /24 network, that is used for accessing the hosts, the proxmox admin ui and corosync
* Virtual machine data: /22 network, here our vms and lxcs will get their primary ip via dhcp
* Ceph Frontend: /22 network, here kubernetes vms will get an additional address to directly communicate with ceph (for volume csi driver)
* Ceph Backend: /24 network, used for ceph backend synchronization

Within the networks each proxmox host has its own static ip, starting at .1 counting upwards. Gateways generally are recommended to get a static ip at the end of the network (.254), while service vms with static ips should get their address by counting backwards from the end of the network (.253, .252). 

DHCP allocation pools will sit in the middle (for example 10.0.4.25 - 10.0.7.225 for a /22 network).

Additionally you can create seperate networks for corosync and vm migration.

## Backups

For backups of vms use the normal proxmox backup server, for kuberentes there is a custom [proxmox cloud backup solution](https://registry.terraform.io/modules/Proxmox-Cloud/backup/pxc/latest). 

With these two backup systems you can also migrate any workload/project accross systems using proxmox cloud.
