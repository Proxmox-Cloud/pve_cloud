# Proxmox Architecture

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

### Single node demo system

To get startet with proxmox cloud you can simply rent any single dedicated server, the following example covers hetzner/ionos on a single 64GB machine.

This setup is not suitable for a scalable production environment, setting that up requires specialized steps per provider (guides can be found [here](#production-system-setup-guide)).

1. first want to do a install with an basic os from the hosting provider (like debian) to get the network mac addressses, dns servers and the routing configuration.
```bash
# save the output of these commands somewhere
cat /etc/network/interfaces
ip a
ip route
cat /etc/resolv.conf

# shutdown the server
shutdown now
```
2. activate and boot into the rescue system, from here we use qemu to install proxmox directly onto the hosts disks:

```bash
# install qemu + uefi files
apt update && apt-get -y install ca-certificates qemu-system-x86

# mount tmpfs for saving the proxmox iso (rescue systems are limited in disk space)
mount -t tmpfs -o size=4G tmpfs /mnt && cd /mnt/

# download proxmox iso
wget https://enterprise.proxmox.com/iso/proxmox-ve_8.4-1.iso

# get your disk device names for passing to the qemu vm
lsblk # ! you might need to wipe existing software raids from the base installer !

# check if your BIOS is UEFI or LEGACY
[ -d "/sys/firmware/efi" ] && echo "UEFI" || echo "LEGACY"

# if it is UEFI, pass run `apt install ovmf` and pass the parameter -bios /usr/share/ovmf/OVMF.fd to the qemu setup command
# ! if you dont do this correctly the server might not be able to boot later

# launch the installer vm - select Install Proxmox VE (Terminal UI, Serial Console)
# for ionos omit --enable-kvm and replace -cpu host with -cpu max, this emulated setup
# will take significantly longer, especially on the last "make system bootable" step.
# allow up to 25 minutes for this to complete
qemu-system-x86_64 -boot d -cdrom proxmox-ve_8.4-1.iso \
  -drive file=/dev/nvme0n1,format=raw,if=virtio -drive file=/dev/nvme1n1,format=raw,if=virtio \
  -m 4G -nographic -serial mon:stdio -cpu host --enable-kvm

# ctrl + a => c open qemu console, type `quit` to exit it if stuck / after finish
```
3. now we want to boot up the vm again, but without the iso mounted so we can access our proxmox
```bash
# run the command again without the -boot d and -cdrom proxmox-ve... parameters to enter the vm
qemu-system-x86_64 -cpu host --enable-kvm -drive file=/dev/nvme0n1,format=raw,if=virtio -drive file=/dev/nvme1n1,format=raw,if=virtio -m 4G -nographic -serial mon:stdio
```
4. inside your proxmox vm create `/etc/systemd/network/10-nic0.link` to ensure proper nic naming on reboot
```conf
[Match]
MACAddress=a8:a1:59:0f:22:60 # mac you noted down in step 1. ;)

[Link]
Name=nic0
```
5. we also need to update `/etc/network/interfaces`
```conf
auto nic0 # renamed via .link file
iface nic0 inet static
        address XXX.XXX.XXX.XXX/XX # insert from step 1.
        gateway XXX.XXX.XXX.XXX # insert from step 1.

# the bridge is a seperate interface we attach our vms to, you need to seperate
# this from the main uplink port and set bridge-ports none, otherwise hetzner
# will trigger an abuse case because you used forbidden macs for vms etc.
auto vmbr0
iface vmbr0 inet static
        address 10.0.4.0/22 # this is for upgrading to a multi node prod system later
        bridge-ports none
        bridge-stp off
        bridge-fd 0
```
5. update `/etc/resolv.conf` with your original values from step 1., update `/etc/hosts` to match your hosts ip
6. exit the vm with `shutdown now` and run it again to shut down the rescue system (then disable it inside hetzner console and boot your server up again)
7. now to make virtual machines have access to the internet we need to configure the proxmox host to act as a router (this is a hack for the demo system only)
```bash
# sign into your host, add your ssh key to the proxmox host itself under ~/.ssh/authorized_keys

# enable forwarding and persist
sysctl -w net.ipv4.ip_forward=1
echo "net.ipv4.ip_forward=1" | tee /etc/sysctl.d/99-ip-forward.conf 

# nat for outgoing connections
apt install iptables-persistent

iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o nic0 -j MASQUERADE
iptables-save > /etc/iptables/rules.v4
```
8. Continue with the [bootstrap section](./bootstrap.md), to deploy proxmox cloud. In this setup you will select a floating ip for the central haproxy loadbalancer of the cloud:
```bash
# forward http, https
iptables -t nat -A PREROUTING -i nic0 -p tcp --dport 443 -j DNAT --to-destination YOUR_INTERNAL_FLOATING_IP:443
iptables -t nat -A PREROUTING -i nic0 -p tcp --dport 80 -j DNAT --to-destination YOUR_INTERNAL_FLOATING_IP:80

iptables-save > /etc/iptables/rules.v4
```

#### Sources

This rescue mode setup was distilled from:

* [Ionos rescue setup](https://www.ionos.com/digitalguide/server/configuration/install-an-alternative-server-operating-system/)
* [Hetzner rescue setup](https://community.hetzner.com/tutorials/install-and-configure-proxmox_ve)

### Control Node Ansible/Terraform

Since this is a dedicated system you need a machine / container with direct access to all vms. for that we manually create an lxc, as a control node for running ansible and terraform configuration (proxmox cloud does not yet support remote access). 

For production systems you should create this lxc on the management switch / vlan.

```bash
# On your freshly created proxmox cluster in the gui goto storage and download a template of your choice

# create your control node container with the ip 10.0.0.2/24 and 10.0.0.1 as gateway
# connect to it using this command (you also should give the lxc your ssh key):
ssh -L 8081:localhost:8080 -o ProxyJump=root@PROXMOX_HOST_IP root@10.0.0.2

# download the latest vscode server release https://github.com/coder/code-server/releases/tag/v4.112.0 and run:
dpkg -i code-server_4.112.0_amd64.deb
systemctl enable --now code-server@root

# open the vscode config file and set auth to none, so its easily accessible via ssh portforwarding
nano /root/.config/code-server/config.yaml 
systemctl restart code-server@root

# now you should be able to access your vscode server at localhost:8081 in the browser

# you need to set the locale for the lxc container for certain later playbooks to work
locale-gen de_DE.UTF-8
update-locale LANG=de_DE.UTF-8

source /etc/default/locale
```

## Extensible single node production cluster

The demo system is not upgradable, in the sense that you cannot add more servers to it and make it highly available. 

For this to be possible you need to do a few extra steps during the setup. Run through the demo setup up until step 6. then continue with these instructions:

!!! WIP !!!

### Single node ceph

For a cluster to be upgradable we need ceph right from the start for kubernetes volumes. Moving them later is a giant pain.

Install ceph via the proxmox ui on your single proxmox host, then do the following:

1. edit /etc/pve/ceph.conf and set `osd_pool_default_min_size` to 1 and `osd_pool_default_size` to 2.
2. on your proxmox host run
```bash
ceph osd getcrushmap -o crush_map_compressed
crushtool -d crush_map_compressed -o crush_map_decompressed
```
3. edit the new `crush_map_decompressed` and replace the line under the rules block `step chooseleaf firstn 0 type host` with this `step chooseleaf firstn 0 type osd`. this changes the failure / replication domain to osds, keeping your data safe this way.
4. then run these commands to load the updated crushmap
```bash
crushtool -c new_crush_map_decompressed -o new_crush_map_compressed
ceph osd setcrushmap -i new_crush_map_compressed
```

## Upgrading / full production cluster

Upgrading to a multi node cluster is highly specific to the tools for configuration your dedicated hosting provider has.

You need at minimum a 10G link between your hosts. Depending on the link you are limited in the number of proxmox hosts and vms you can have running in a single cluster. The sizes of your subnets should correspond to the bandwidth of your network.

Upgrading will require a restart of your vms and modifying of their config. We will need to adjust the network devices they have mapped.

You will also need to undo the proxmox hosts forwardings (iptable rules), routing settings (now handled via opnsense) and undo the changes to the crush map for single node ceph.

### Ionos

1. In your Ionos ui goto Network/Private Network and create the following networks (/22 should be more than enough for a 10G link - the maximum ionos provides):

* management 10.0.1.0/24
* corosync 10.0.2.0/24
* migration 10.0.3.0/24
* vmdata 10.0.4.0/22
* ceph frontend 10.0.8.0/22
* ceph backend 10.0.12.0/24

2. Add all your servers to the vlans in the ionos ui

3. Now we need to change the network configuration on our nodes to look something like this:

```conf
auto nic0
iface nic0 inet manual

auto vmbr0
iface vmbr0 inet manual
        address XXX.XXX.XXX.XXX/XX # public ip and gateway move here
        gateway XXX.XXX.XXX.XXX
        bridge-ports nic0 # set the port and not none
        bridge-stp off
        bridge-fd 0
        bridge-vlan-aware yes
        bridge-vids 2-4094

# create our vlans
auto vmbr0.XXXX # id from ionos ui
iface vmbr0.XXXX inet static
        address 10.0.1.1/24 # 1/2/3 depending on the number of your host
# management

auto vmbr0.XXXX
iface vmbr0.XXXX inet static
        address 10.0.2.1/24
# corosync

auto vmbr0.XXXX
iface vmbr0.XXXX inet static
        address 10.0.3.1/24
# migration

auto vmbr0.XXXX
iface vmbr0.XXXX inet static
        address 10.0.4.1/22
# vm data

auto vmbr0.XXXX
iface vmbr0.XXXX inet static
        address 10.0.8.1/22
# ceph frontend

auto vmbr0.XXXX
iface vmbr0.XXXX inet static
        address 10.0.12.1/24
# ceph backend

# ...
```

4. Next you can create a proxmox cluster in the ui and join your nodes on their management vlan ips.
5. edit /etc/pve/corosync.conf and set the ip for corosync vlan
6. goto Datacenter/Options and set the migration network under the entry Migration Settings
7. configure repositories and upgrade
8. in the ionos ui create a public network for pve-opnsense and add all servers to it, also create a public ip for the opnsense and assign it to that network
```conf
# add to /etc/network/interfaces

auto vmbr0.XXXX
iface vmbr0.XXXX inet manual
# opnsense vlan
```
9. continue with the opnsense setup

## Opnsense

A production system needs a dedicated firewall that has its own public ip. This will be the central gateway for all of our vms.

1. download opnsense dvd image and create a vm inside of proxmox:
    * bios OVMF (UEFI) - no efi partition (delete it)
    * scsi for the hardware disk controller
    * two nics, one in the public vlan one in the vmdata
    * OS Type: other
    * in the installer choose zfs, ufs is buggy
2. in the terminal configure the lan ip to 10.0.7.254 with the subnet of 22 bits, after this you can ssh into one of the hosts and get the opnsense ui `ssh -L 8080:10.0.7.254:80 root@PROXMOX.HOST.IP.XXX`
3. set your extra public ip you booked the wan interface aswell as create a gateway configuration

# Backups

For backups of vms use the normal proxmox backup server, there is a custom [proxmox cloud backup solution](https://registry.terraform.io/modules/Proxmox-Cloud/backup/pxc/latest) for k8s ceph csi volumes.

For single node k8s clusters / clusters without ceph for csi, simply create big disks for the nodes and use openebs hostpath for volumes. Then backup the entire cluster via PBS.

