# Architecture

For a proxmox cluster to work optimally with the collection, it needs to be configured in a certain way to handle interoperability.

Depending on the available hardware we want to optimize for different things.

## Requirements

You need atleast one proxmox cluster to start (one host is enough). Later you can add multiple proxmox clusters to your pve cloud instance.

The cluster needs to meet these minimum requirements:

* seperate free vlan (proxmox cloud runs its own mandatory dhcp)
* 4 cores
* 32 gb of ram
* 500 gb of free disk space for vms
* subnet with at least 20 free allocatable addresses

## Onprem

If you have your own machines and network architecture, an ideal setup would look like this:

* strong enough dedicated network link dedicated for ceph
* small dedicated disks for the os, zfs raid1 is optimal here
* a seperate enterprise grade firewall with public ips / router for configuring incoming traffic

The firewall can then forward 443, 80 and 6443 to the clouds haproxy loadbalancer instances.

## Dedicated Hosts / Limited network hardware

If you dont have a dedicated switch for ceph, you might run into a bottleneck. Dedicated server providers often dont allow you / provide buggy / poorly configured setups for proxmox.

One solution to optimally use disks that dont fit a good proxmox setup quite right, is to split partitions up for local-zfs + ceph osd on the remaining partition.
50/50 is a good starting point for allocating disk space to local-zfs for vm disks / ceph osds. This can be adjusted later on.

## Address Ranges

You will need to choose different private network ranges for different cloud services.

* Management: a /24 network is enough for this. Here each proxmox host will have its own ip by number, for example 10.0.0.1 / 10.0.0.2 ..., the control node will also get an ip here, for conviniece start counting backwards 10.0.0.254/24
* Virtual machine data: for a production system you should choose a /22 so you have enough room for all your vms. Again the hosts get their own ip at the beginning, leave as much room as needed for adding hosts later on. Again the proxmox hosts start at 10.0.4.1, ...
* Ceph Frontend: this should also get a /22 since kubespray vms need access to the ceph frontend for pvc csi driver. The pve hosts again get a static ip here
* Ceph Backend: this only needs a /24 net

Additionally you can create vlans for corosync and vm migration.

## Backups

For backups of vms use the normal proxmox backup server, there is a custom [proxmox cloud backup solution](https://registry.terraform.io/modules/Proxmox-Cloud/backup/pxc/latest) for k8s ceph csi volumes.
