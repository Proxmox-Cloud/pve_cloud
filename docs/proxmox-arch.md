# Proxmox Architecture

For a proxmox cluster to work optimally with the collection, it needs to be setupped in a certain way to handle interoperability.

Depending on the available hardware we want to optimize for different things.

The first big choice is the filesystem / vm volume storage that you want to use.

## Hardware raid

For a hardware raid you usually just want lvm + lvm thin for virtual machine disks. 

## Software raid

In this case it depends on the type of disk. If you have a consumer disks, that dont support plp you should go for btrfs raid 1 / 10.

If they do support it ZFS is the more mature option, however for zfs you need either a live iso installer option on dedicated systems or a rescue system that allows you to use the proxmox installer ISOs. In some extreme cases you might be limited to a debian installer, which only supports btrfs.

## Onprem

If you have your own machines and network architecture, an ideal setup would look like this:

* strong enough dedicated network link dedicated for ceph
* small dedicated disks for the os (same raid principles as described above)

In this case you can simply run the normal proxmox installer, configure the small disks with raid1 for the os (monitoring of the raid status currently exists for zfs and btrfs).

Then you do you dedicated network setup for ceph frontend and backend, and just allocate all you drives to ceph, also creating vm disks exclusively backed by ceph.

## Dedicated Hosts / Limited network hardware

If you dont have a dedicated switch for ceph, you might run into a bottleneck. Dedicated server providers often dont allow you / provide buggy / poorly configured setups for proxmox.

They also often dont let you get small disks for the os, forcing you to share os and vm disk image storage.

Here are some recommendations:

* on hardware raid and big os disks you should go for lvm thin, if you have a software raid zfs is the more mature option, assuming you can boot the proxmox installer.
* use ceph with the 10gig generic option most dedicated providers offer for inter server communication, but only use it for critical vm / lxc disks and kubernetes volumes

## Btrfs

If you choose btrfs for your os and vm disks, be it for performance reasons or limitations in your installer you need to enable degraded boot, especially on a dedicated server, where you dont have access to the grub boot command line.

Add `rootflags=degraded` to `GRUB_CMDLINE_LINUX_DEFAULT="... rootflags=degraded"` in `/etc/default/grub` and run `update-grub`, enable monitoring by setting `install_btrfs_root_prom_exporter` in your [pve cloud inventory host vars](schemas/pve_cloud_inv_schema.md).

To recover after a disk outage run `btrfs scrub start /`, this also cleans up errors from monitoring. To see live stats run `btrfs device stats /`.

### Debian base image install

WIP

### Rescue mode install ZFS

```bash
# install qemu + uefi files
apt-get -y install ca-certificates qemu-system-x86 ovmf

# mount tmpfs for install
mount -t tmpfs -o size=4G tmpfs /mnt

# download proxmox iso
cd /mnt/
wget https://enterprise.proxmox.com/iso/proxmox-ve_8.4-1.iso

# launch installer vm (run lsblk first to passthrough disks) - cpu max is needed for zfs
qemu-system-x86_64 -cpu max -bios /usr/share/ovmf/OVMF.fd -nographic -boot d -cdrom proxmox-ve_8.4-1.iso -drive file=/dev/nvme0n1,format=raw -drive file=/dev/nvme1n1,format=raw -m 4G -serial mon:stdio

# ... launch the vm after the install - to maybe edit netwwork devices before exiting rescue mode
qemu-system-x86_64 -cpu max -bios /usr/share/ovmf/OVMF.fd -nographic -drive file=/dev/nvme0n1,format=raw -drive file=/dev/nvme1n1,format=raw -m 4G -serial mon:stdio

# set interfaces in /etc/network/interfaces to
# auto IFACE
# then either static or dhcp for the ip
```