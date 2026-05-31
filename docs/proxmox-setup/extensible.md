# Extensible production cluster (hosted)

In this setup we will run through a full production setup, either starting with one or multiple servers. This setup is extensible in the sense that you can add more hosts to your cluster later on and also start with just a single node.

You need at minimum a 10G link between your hosts. Depending on the link you are limited in the number of proxmox hosts and vms you can have running in a single cluster. The sizes of your subnets should correspond to the bandwidth of your network.

Run through the [demo setup](demo.md) up until finally step 6. then continue with the following instructions:

7. Go to the https://PUBLIC-IP:8006 of your proxmox hosts and create Linux VLANs under System/Network for on all nodes. These vlans and their IDs should correspond with the virtual networks / vswitches your create in the web interface of your hosting provider. The following IDs / networks are just suggestions:
    * vmbr0.2, 10.0.0.X/24, management (X is the number of the proxmox host)
    * vmbr0.10, 10.0.4.X/22, vm data
    * vmbr0.20, 10.0.8.X/22, ceph frontend
    * vmbr0.21, 10.0.12.X/24, ceph backend
    * vmbr0.30, 10.0.13.X/24, opnsense pseudo wan (you only need this if you dont have a dedicated ip for the opnsense)
8. initialize the proxmox cluster under Datacenter/Cluster on the management interface
9. under Datacenter/Storage enable "Snippets" for local storage
10. add your apt repos (no-subscriptions / your enterprise license) and also repositories for ceph squid, then refresh abd upgrade
11. go to the Datacenter/Ceph and run through the installer.

## Single node ceph

If you only have a single host for starters you need still need to use ceph for volumes / vm disks. Do the following to switch ceph into single node mode:

1. edit /etc/pve/ceph.conf and set `osd_pool_default_min_size` to 1 and `osd_pool_default_size` to 2.
2. on your proxmox host run
```bash
ceph osd getcrushmap -o crush_map_compressed
crushtool -d crush_map_compressed -o crush_map_decompressed
```
3. edit the new `crush_map_decompressed` and replace the line under the rules block `step chooseleaf firstn 0 type host` with this `step chooseleaf firstn 0 type osd`. this changes the failure / replication domain to osds, keeping your data safe this way.
4. then run these commands to load the updated crushmap
```bash
crushtool -c crush_map_decompressed -o new_crush_map_compressed
ceph osd setcrushmap -i new_crush_map_compressed
```

## OPNSense Setup

For production systems we recommend an OPNSense firewall as a virtual machine on your proxmox cluster. This vm should have its own public ip on a dedicated interface and will function as the default gateway for vms and lxcs. 

1. If you don't yet have a public ip you can also do the setup with the wan interface on the management interface and using the proxmox host itself as the gateway. For this to work your proxmox host needs to act as a router, just like in the demo setup:

```bash
# sign into your host, add your ssh key to the proxmox host itself under ~/.ssh/authorized_keys

# enable forwarding and persist
sysctl -w net.ipv4.ip_forward=1
echo "net.ipv4.ip_forward=1" | tee /etc/sysctl.d/99-ip-forward.conf 

# edit /etc/network/interfaces and add the following post-up and post-down commands under vmbr0
iface vmbr0 inet static 
        # ...

        # routing cidr is different than in the demo system, we dont let the vms directly into the web
        # but instead allow the opnsense on its pseudo wan interface to access the web through the proxmox host
        post-up iptables -t nat -A POSTROUTING -s 10.0.13.0/24 -o vmbr0 -j MASQUERADE
        post-down iptables -t nat -D POSTROUTING -s 10.0.13.0/24 -o vmbr0 -j MASQUERADE
        
        # this is needed for masquerading to work with the pve fw enabled later on# this is needed for masquerading to work with the pve fw enabled later on
        # https://forum.proxmox.com/threads/dnat-snat-via-pve-firewall-prerouting-postrouting.49192/#post-230641
        post-up iptables -t raw -I PREROUTING -i fwbr+ -j CT --zone 1 
        post-down iptables -t raw -I PREROUTING -i fwbr+ -j CT --zone 1

```
2. download opnsense dvd image and create a vm inside of proxmox:
    * OS Type: other
    * scsi for the hardware disk controller, disk on ceph pool 50GB (discard, ssd emulation on)
    * 4 cores 8 gb ram
    * two nics (model virtio): vmbr0.10 for the lan interface, wan interface added after creating the vm. If you don't have a dedicated public ip, instead add the nic on the management interface. This will be used as the temporary WAN interface.
3. boot the vm and login as "installer", password "opnsense", choose zfs, ufs is buggy. For the install you can choose a simple password and change it later in the ui.
4. login to the terminal via proxmox vm console as root and select "Assign Interfaces"
5. assign lan and wan to the corresponding nics
6. select "Set interface IP Address"
7. set the lan address to 10.0.7.254 with the subnet of 22 bits
8. for wan either set your public ip with the same gateway that the proxmox hosts are using, or if you dont have a public ip set the wan to management net .254 with the proxmox host as the gateway.
9. ssh into one of the hosts and forward the opnsense ui `ssh -L 8087:10.0.7.254:443 root@PROXMOX.HOST.IP.XXX`
10. you can skip the setup wizard and continue with your configuration. Set a strong password for the root user now.
11. if you dont have a dedicated public ip, go to your WAN interface under Interfaces/WAN and uncheck the box "Block private Networks"

## Securing our Cluster

We now also want to restrict access to our proxmox hosts by activating the proxmox firewall. Sadly we need to define a bunch of rules manually to allow our proxmox cluster to continue to function.

* Go to Datacenter/Firewall/Alias, create 3 aliases with the public ip of each node (node1, node2, node3, ...)
* Go to IPSet and create one called pve-public, add the 3 aliases. Then create IPSets for cephfe, cephbe and migration, adding the cidrs directly.
* Create an additional IPSet for IPSec, this should be the public static ip of your companies internet connection. This way noone from outside the company can even connect to your proxmox hosts.

Next create Security Groups + Rules:

* admin-in: add Protocol: tcp rules for destination port 22 and 8006 with the pve-public IPSet as destination, with your ipsec IPset and control node as source
* mon-in: add rule to allow source 10.0.4.0/22 to reach destination 10.0.4.0/22. This is needed for the vms / lxcs to connect to the proxmox hosts and scrape prometheus metrics (systemd etc.), allow destination ports: 9100,9633,9558, protocol: tcp
* ceph-fe: source ceph-fe, destination ceph-fe allow in all
* ceph-be: source ceph-be, destination ceph-be allow in all

Make sure all rules have enabled checkbox checked.

Now go to Datacenter/Firewall and activate / insert all the security groups we just created (again marking them as enabled), then under Firewall/Options enable the firewall.

! This security setup is by no means complete and needs to be used with caution !


## Uprading to multi node cluster

Upgrading to a multi node cluster is highly specific to the tools for configuration your dedicated hosting provider has.

Depending on what changes you have to adjust configs, remove itable rules and network interfaces.

You also get a dedicated public ip for the WAN interface of the opnsense vm and configure that as the new WAN interface in your opnsense.
