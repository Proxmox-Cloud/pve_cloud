# Demo system (hosted)

To get startet with proxmox cloud you can simply rent any single dedicated server, the following example covers hetzner/ionos on a single 64GB machine.

This setup is not suitable for a scalable production environment, setting that up requires specialized steps per provider (guides can be found in the [extensible setup](extensible.md)).

## Setup

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
# to wipe md raid run `mdadm --stop /dev/md2 /dev/md1 /dev/md0` on all md devices `cat /proc/mdstat`
# then zero all superblock on partitions that had an md device on it `mdadm --zero-superblock /dev/nvme0n1p1 /dev/nvme0n1p2 /dev/nvme0n1p3 ...`
# follow that up by wiping `wipefs -a /dev/nvme0n1 ...`

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
auto lo
iface lo inet loopback

iface nic0 inet manual # renamed via .link file

# the bridge is a seperate interface we attach our vms to, you need to seperate
# this from the main uplink port and set bridge-ports none, otherwise hetzner
# will trigger an abuse case because you used forbidden macs for vms etc.
auto vmbr0
iface vmbr0 inet static
        address XXX.XXX.XXX.XXX/XX # insert from step 1.
        gateway XXX.XXX.XXX.XXX # insert from step 1.
        bridge-ports nic0
        bridge-stp off
        bridge-fd 0
        bridge-vlan-aware yes
        bridge-vids 2-4094
        
        # ! hack configuration for demo system only !
        # enable routing nat for our virtual machines (so they can connect to the www)
        post-up iptables -t nat -A POSTROUTING -s 10.0.1.0/24 -o vmbr0 -j MASQUERADE
        post-down iptables -t nat -D POSTROUTING -s 10.0.1.0/24 -o vmbr0 -j MASQUERADE


# we will add additional vlans via the ui later
```
5. update `/etc/resolv.conf` with your original values from step 1., update `/etc/hosts` to match your hosts ip
6. exit the vm with `shutdown now` and run it again to shut down the rescue system (then disable it inside hetzner console and boot your server up again)
7. go to your https://PUBLIC-IP:8006 and access the proxmox ui and create a new Linux VLAN in the System/Network tab. Name it vmbr0.2 and assign the static ip 10.0.0.1/24. This will be used by the proxmox cluster and the control node later
8. create a network for vm communication: vmbr0.10 10.0.1.1/24
9. create proxmox cluster under Datacenter/Cluster on the management interface vmbr0.2
10. under Datacenter/Storage enable "Snippets" for local storage
11. add no subscription pve apt repos refresh and upgrade
12. now to make virtual machines have access to the internet we need to configure the proxmox host to act as a router (this is a hack for the demo system only!)
```bash
# sign into your host, add your ssh key to the proxmox host itself under ~/.ssh/authorized_keys

# enable forwarding and persist
sysctl -w net.ipv4.ip_forward=1
echo "net.ipv4.ip_forward=1" | tee /etc/sysctl.d/99-ip-forward.conf 

```
12. Setup your [control node lxc](#control-node-ansibleterraform) for deploying and working with the collection
13. Continue with the [bootstrap section](./bootstrap.md), to deploy proxmox cloud. In this setup you will select a floating ip for the central haproxy loadbalancer of the cloud.


### Sources

This rescue mode setup was distilled from:

* [Ionos rescue setup](https://www.ionos.com/digitalguide/server/configuration/install-an-alternative-server-operating-system/)
* [Hetzner rescue setup](https://community.hetzner.com/tutorials/install-and-configure-proxmox_ve)


## Control Node Ansible/Terraform

Since this is a dedicated system you need a machine / container with direct access to all vms and proxmox hosts. for that we manually create an lxc, as a control node for running ansible and terraform configuration (proxmox cloud does not yet support remote access). On a local setup where your personal computer has access to the same private network where your vms live, you dont need a seperate machine / container.

```bash
# On your freshly created proxmox cluster in the gui go to storage and download a template of your choice (debian/ubuntu recommended)

# create your control node container with a network interface on the vm data bridge vlan and one on the management interface
# for demo systems use the proxmox host as the gateway, for extensible the opnsense
# assign it .254 or .253 on both network interfaces statically

# then connect to your lxc connect to it using this command:
ssh -L 8081:localhost:8080 -o ProxyJump=root@PROXMOX_HOST_IP root@STATIC_VM_DATA_IP.253/254

# download the latest vscode server release https://github.com/coder/code-server/releases/:
wget https://github.com/coder/code-server/releases/download/v4.112.0/code-server_4.112.0_amd64.deb
dpkg -i code-server_4.112.0_amd64.deb
systemctl enable --now code-server@root

# open the vscode config file and set auth to "none", so its easily accessible via ssh port forwarding
nano /root/.config/code-server/config.yaml 
systemctl restart code-server@root

# now you should be able to access your vscode server at localhost:8081 in the browser

# you need to set the locale for the lxc container for certain later playbooks to work
dpkg-reconfigure locales # generate and set your default locale
# => reboot the lxc after setting locales

# generate a ssh key for your private git repos and proxmox host access (add it to one of your proxmox hosts under /root/.ssh/authorized_keys)
ssh-keygen -t ed25519
cat ~/.ssh/id_ed25519.pub
```

From here you can start with the [bootstrap process](../bootstrap.md), after you have created your bind nameservers, you should assign those instead of the hosts defaults to the lxc.
