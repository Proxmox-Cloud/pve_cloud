# Proxmox Architecture

For a proxmox cluster to work optimally with the collection, it needs to be setupped in a certain way to handle interoperability.

Depending on the available hardware we want to optimize for different things.

The first big choice is the filesystem / vm volume storage that you want to use.

## Onprem

If you have your own machines and network architecture, an ideal setup would look like this:

* strong enough dedicated network link dedicated for ceph
* small dedicated disks for the os, zfs raid1 is optimal here
* a seperate enterprise grade firewall with public ips / router for configuring incoming traffic

## Dedicated Hosts / Limited network hardware

If you dont have a dedicated switch for ceph, you might run into a bottleneck. Dedicated server providers often dont allow you / provide buggy / poorly configured setups for proxmox.

### Single node demo system

To get startet with proxmox cloud you can simply rent any single dedicated server, the following example covers hetzner on a single 64GB machine.

The following setup is not recommended for production!

1. first want to do a basic install with an basic os from the hosting provider to get the main nics mac address, dns servers and the gateway.
2. boot into the rescue system and mount the hosts disks in a qemu vm with the proxmox installer like so:

```bash
# install qemu + uefi files
apt-get -y install ca-certificates qemu-system-x86

# mount tmpfs for install
mount -t tmpfs -o size=4G tmpfs /mnt

# download proxmox iso
cd /mnt/
wget https://enterprise.proxmox.com/iso/proxmox-ve_8.4-1.iso

# check if your BIOS is UEFI or LEGACY
[ -d "/sys/firmware/efi" ] && echo "UEFI" || echo "LEGACY"`

# if it is UEFI, pass run `apt install ovmf` and pass the parameter -bios /usr/share/ovmf/OVMF.fd to the qemu setup command

# get your disk device names for passing to the qemu vm
lsblk # you might need to wipe existing software raids from the base installer

# launch the installer vm
qemu-system-x86_64 -cpu host --enable-kvm -boot d -cdrom proxmox-ve_8.4-1.iso -drive file=/dev/nvme0n1,format=raw,if=virtio -drive file=/dev/nvme1n1,format=raw,if=virtio -m 4G -nographic -serial mon:stdio

# for ionos omit --enable-kvm and replace -cpu host with -cpu max

# ctrl + a => c open qemu console, type `quit` to exit it if stuck / after finish
```
3. now we want to boot up the vm again, but without the iso mounted so we can access our proxmox
```bash
# run the command again without the -boot d and -cdrom proxmox-ve... parameters to enter the vm
qemu-system-x86_64 -cpu host --enable-kvm -drive file=/dev/nvme0n1,format=raw,if=virtio -drive file=/dev/nvme1n1,format=raw,if=virtio -m 4G -nographic -serial mon:stdio

# inside the vm create a named file for the main link so the network naming is consitent and we can access our vm after reboot
# /etc/systemd/network/10-uplink.link
[Match]
MACAddress=a8:a1:59:0f:22:60 # mac you noted down in step 1. ;)

[Link]
Name=uplink0
```
4. we also need to update /etc/network/interfaces, an original on hetzner might look like this (from step 1)
```bash
auto enp35s0
iface enp35s0 inet static
  address 95.217.107.238
  netmask 255.255.255.192
  gateway 95.217.107.193
  # route 95.217.107.192/26 via 95.217.107.193
  up route add -net 95.217.107.192 netmask 255.255.255.192 gw 95.217.107.193 dev enp35s0
```

you want to translate it to this in the vm 

```bash
iface uplink0 inet manual

auto vmbr0
iface vmbr0 inet static
        address 95.217.107.238/26 # convert old netmask + up route syntax
        gateway 95.217.107.193
        bridge-ports uplink0 
        bridge-stp off
        bridge-fd 0

# add secondary address space for vms here
iface vmbr0 inet static
        address 10.0.0.1/24 # you can freely pick the ip the host itself has here
```
5. update /etc/resolv.conf with your original values from step 1
6. exit the vm with `shutdown now` and run it again to shut down the rescue system (then disable it inside hetzner console and boot your server up again)
7. now to make virtual machines have access to the internet we need to configure the proxmox host to act as a router. (dont do this for a production cluster)
```bash
# sign into your host, add your ssh key to the proxmox host istself under ~/.ssh/authorized_keys

# forwarding
sysctl -w net.ipv4.ip_forward=1

echo "net.ipv4.ip_forward=1" | tee /etc/sysctl.d/99-ip-forward.conf # persist it

# nat
apt install iptables-persistent

iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o vmbr0 -j MASQUERADE

iptables-save > /etc/iptables/rules.v4 # persist it
```
8. since this is a dedicated system you need a machine / container with direct access to all vms that will be created, as a control node for running ansible and terraform configuration (proxmox cloud does not yet support remote access). 
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
```

9. Continue with the [bootstrap section](./bootstrap.md), to deploy proxmox cloud. In this setup you will select a private ip floating ip for the central clouds haproxy. This ip should accept traffic 443, you can forward from your proxmox host like this:
```bash
iptables -t nat -A PREROUTING -i vmbr0 -p tcp --dport 443 -j DNAT --to-destination YOUR_INTERNAL_FLOATING_IP:443

iptables-save > /etc/iptables/rules.v4
```

This rescue mode setup was distilled from:

* [Ionos rescue setup](https://www.ionos.com/digitalguide/server/configuration/install-an-alternative-server-operating-system/)
* [Hetzner rescue setup](https://community.hetzner.com/tutorials/install-and-configure-proxmox_ve)

### Production System Setup Guide

Coming soon.

## Backups

For backups of vms use the normal proxmox backup server, there is a custom [proxmox cloud backup solution](https://registry.terraform.io/modules/Proxmox-Cloud/backup/pxc/latest) for k8s ceph csi volumes.

For single node k8s clusters / clusters without ceph for csi, simply create big disks for the nodes and use openebs hostpath for volumes. Then backup the entire cluster via PBS.

