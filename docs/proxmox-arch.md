# Proxmox Architecture

For a proxmox cluster to work optimally with the collection, it needs to be setupped in a certain way to handle interoperability.

Depending on the available hardware we want to optimize for different things.

The first big choice is the filesystem / vm volume storage that you want to use.

## Disks

Generally you need enterprise grade ssds with plp to properly use ceph and zfs, however there are a few workarounds to making consumer ssds work aswell.

## Hardware raid

For a hardware raid you usually just want lvm + lvm thin for virtual machine disks. 

## Software raid

ZFS is the general preferred choice for proxmox as its more integrated. On dedicated systems you might run into buggy proxmox installers, and under extreme circumstances even rescue systems that are incredibly limited and dont support the necessary os features to setup zfs.

The absolute minimum setup every dedicated hosting provider should provide is a debian installer you can run through. In this case you can setup a btrfs raid 1/10 for your os and vm disks. 

## Onprem

If you have your own machines and network architecture, an ideal setup would look like this:

* strong enough dedicated network link dedicated for ceph
* small dedicated disks for the os, zfs raid1 is optimal here

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

## Debian base image install

Follow the offical [proxmox guide](https://pve.proxmox.com/wiki/Install_Proxmox_VE_on_Debian_13_Trixie).

For pve 8 [this guide](https://pve.proxmox.com/wiki/Install_Proxmox_VE_on_Debian_12_Bookworm).

(This has not yet been tested with the collection but should work.)

## Rescue mode install ZFS

You first want to do a basic install with an apt based os from the hosting provider to get default interface names, dns and the gateway.

```bash
# install qemu + uefi files
apt-get -y install ca-certificates qemu-system-x86

# mount tmpfs for install
mount -t tmpfs -o size=4G tmpfs /mnt

# download proxmox iso
cd /mnt/
wget https://enterprise.proxmox.com/iso/proxmox-ve_8.4-1.iso

# run `[ -d "/sys/firmware/efi" ] && echo "UEFI" || echo "LEGACY"` to check if your BIOS is UEFI or LEGACY
# if it is uefi, pass run `apt install ovmf` and pass the parameter -bios /usr/share/ovmf/OVMF.fd to the qemu setup command

# if the rescue system supports kvm you can pass -enable-kvm and -cpu host (instead of max) for a way faster install

# launch installer vm (run lsblk first to passthrough disks) - cpu max is needed for zfs (might not be enough on some rescue systems and you are forced to use btrfs)
qemu-system-x86_64 -cpu max -boot d -cdrom proxmox-ve_8.4-1.iso -drive file=/dev/nvme0n1,format=raw,if=virtio -drive file=/dev/nvme1n1,format=raw,if=virtio -m 4G -nographic -serial mon:stdio

# run the command again without the -boot d and -cdrom proxmox-ve... parameters to enter the vm

# set interfaces in /etc/network/interfaces to
# auto IFACE
# then either static or dhcp for the ip
```

This rescue mode setup was distilled from:

* [Ionos rescue setup](https://www.ionos.com/digitalguide/server/configuration/install-an-alternative-server-operating-system/)
* [Hetzner rescue setup](https://community.hetzner.com/tutorials/install-and-configure-proxmox_ve)

## Consumer SSDs

If you have consumer ssds that dont support power loss prevention (plp) you should invest in a UPS as an alternative and then setup your systems with the following hacks.

Without a backup battery in the following scenario you risk data loss on power outages. You should also setup some gentle shutdown signals once the battery is getting low.

Either use btrfs for os / vm disks or zfs + `sync=disabled` (zfs untested).

To make ceph work on consumer ssds we want to noop fsync calls, for that you should run `apt install eatmydata` and modify `/lib/systemd/system/ceph-osd@.service` / `ExecStart=/usr/bin/eatmydata /usr/bin/ceph-osd ...`. After that you want to run `systemctl daemon-reload && systemctl restart ceph-osd.target` to reboot your osds.

```bash
# test fsync - `fio --name=fsync-1 --filename=./testfile --size=4G --rw=randwrite --bs=4k --ioengine=libaio --fsync=1 --iodepth=4 --runtime=300 && rm ./testfile`
# test normal write - `fio --name=default --filename=./testfile --size=4G --rw=randwrite --bs=4k --ioengine=libaio --iodepth=4 --runtime=300 && rm ./testfile`

# normal setup, no eatmydata
fsync-1: (groupid=0, jobs=1): err= 0: pid=2222: Fri Mar  6 19:02:25 2026
  write: IOPS=73, BW=295KiB/s (302kB/s)(86.4MiB/300006msec); 0 zone resets
    slat (usec): min=5, max=12004, avg=18.01, stdev=80.84
    clat (msec): min=10, max=699, avg=40.68, stdev=51.55

# eatmydata on osds
fsync-1: (groupid=0, jobs=1): err= 0: pid=2114: Fri Mar  6 18:36:45 2026
  write: IOPS=165, BW=662KiB/s (678kB/s)(194MiB/300002msec); 0 zone resets
    slat (usec): min=5, max=15456, avg=16.59, stdev=74.24
    clat (msec): min=3, max=2595, avg=18.12, stdev=43.20


# set mount options in your ceph csi pool inventory to: [barrier=0, data=writeback, journal_async_commit, commit=60, discard]
# and the mkfsOptions: "-O fast_commit" in ceph_csi_sc_pools

# => results in
fsync-1: (groupid=0, jobs=1): err= 0: pid=676689: Sat Mar  7 10:51:40 2026
  write: IOPS=297, BW=1191KiB/s (1220kB/s)(349MiB/300010msec); 0 zone resets
    slat (usec): min=5, max=123, avg=13.32, stdev= 3.41
    clat (msec): min=2, max=2077, avg=10.08, stdev=21.19


# for qemu disks you can use the unsafe cache option for rbd disks and get the biggest performace increase by far
# sadly this is limited to qemu disks only

fsync-1: (groupid=0, jobs=1): err= 0: pid=1025: Fri Mar  6 21:41:51 2026
  write: IOPS=944, BW=3777KiB/s (3868kB/s)(1107MiB/300001msec); 0 zone resets
    slat (usec): min=9, max=1674, avg=15.46, stdev=15.66
    clat (usec): min=595, max=5348.8k, avg=3179.66, stdev=44101.80
```

To bypass the kernel caching mechanisms and get better performance there is also rbd-nbd and [client caching options](https://docs.ceph.com/en/squid/rbd/rbd-config-ref/), support for ceph csi driver is in alpha.


## Backups

For backups of vms use the normal proxmox backup server, there is a custom [proxmox cloud backup solution](https://registry.terraform.io/modules/Proxmox-Cloud/backup/pxc/latest) for k8s ceph csi volumes.

For single node k8s clusters / clusters without ceph for csi, simply create big disks for the nodes and use openebs hostpath for volumes. Then backup the entire cluster via PBS.