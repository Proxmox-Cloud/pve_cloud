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

# launch the installer vm - select Install Proxmox VE (Terminal UI, Serial Console)
# for ionos omit --enable-kvm and replace -cpu host with -cpu max
qemu-system-x86_64 -cpu host --enable-kvm -boot d -cdrom proxmox-ve_8.4-1.iso -drive file=/dev/nvme0n1,format=raw,if=virtio -drive file=/dev/nvme1n1,format=raw,if=virtio -m 4G -nographic -serial mon:stdio

# ctrl + a => c open qemu console, type `quit` to exit it if stuck / after finish
```
3. now we want to boot up the vm again, but without the iso mounted so we can access our proxmox
```bash
# run the command again without the -boot d and -cdrom proxmox-ve... parameters to enter the vm
qemu-system-x86_64 -cpu host --enable-kvm -drive file=/dev/nvme0n1,format=raw,if=virtio -drive file=/dev/nvme1n1,format=raw,if=virtio -m 4G -nographic -serial mon:stdio
```
4. inside your proxmox vm create `/etc/systemd/network/10-uplink.link` to ensure proper nic naming on reboot
```conf
[Match]
MACAddress=a8:a1:59:0f:22:60 # mac you noted down in step 1. ;)

[Link]
Name=uplink0
```
5. we also need to update `/etc/network/interfaces`
```conf
auto uplink0 # renamed via .link file enp35s0
iface uplink0 inet static
        address XXX.XXX.XXX.XXX/XX # insert from step 1.
        gateway XXX.XXX.XXX.XXX # insert from step 1.

# the bridge is a seperate interface we attach our vms to, you need to seperate
# this from the main uplink port and set bridge-ports none, otherwise hetzner
# will trigger an abuse case because you used forbidden macs for vms etc.
auto vmbr0
iface vmbr0 inet static
        address 10.0.0.1/24
        bridge-ports none
        bridge-stp off
        bridge-fd 0
```
5. update `/etc/resolv.conf` with your original values from step 1.
6. exit the vm with `shutdown now` and run it again to shut down the rescue system (then disable it inside hetzner console and boot your server up again)
7. now to make virtual machines have access to the internet we need to configure the proxmox host to act as a router (this is a hack for the demo system only)
```bash
# sign into your host, add your ssh key to the proxmox host itself under ~/.ssh/authorized_keys

# enable forwarding and persist
sysctl -w net.ipv4.ip_forward=1
echo "net.ipv4.ip_forward=1" | tee /etc/sysctl.d/99-ip-forward.conf 

# nat for outgoing connections
apt install iptables-persistent

iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o uplink0 -j MASQUERADE
iptables-save > /etc/iptables/rules.v4
```
8. since this is a dedicated system you need a machine / container with direct access to all vms. for that we manually create an lxc, as a control node for running ansible and terraform configuration (proxmox cloud does not yet support remote access). 
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
9. Continue with the [bootstrap section](./bootstrap.md), to deploy proxmox cloud. In this setup you will select a floating ip for the central haproxy loadbalancer of the cloud:
```bash
# forward http, https
iptables -t nat -A PREROUTING -i uplink0 -p tcp --dport 443 -j DNAT --to-destination YOUR_INTERNAL_FLOATING_IP:443
iptables -t nat -A PREROUTING -i uplink0 -p tcp --dport 80 -j DNAT --to-destination YOUR_INTERNAL_FLOATING_IP:80

iptables-save > /etc/iptables/rules.v4
```

#### Sources

This rescue mode setup was distilled from:

* [Ionos rescue setup](https://www.ionos.com/digitalguide/server/configuration/install-an-alternative-server-operating-system/)
* [Hetzner rescue setup](https://community.hetzner.com/tutorials/install-and-configure-proxmox_ve)

### Production System Setup Guide

Coming soon.

## Backups

For backups of vms use the normal proxmox backup server, there is a custom [proxmox cloud backup solution](https://registry.terraform.io/modules/Proxmox-Cloud/backup/pxc/latest) for k8s ceph csi volumes.

For single node k8s clusters / clusters without ceph for csi, simply create big disks for the nodes and use openebs hostpath for volumes. Then backup the entire cluster via PBS.

