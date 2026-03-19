# FAQ

## Patroni recovery

If one patroni node fails, abrupt restart etc., delete /opt/ha-postgres data dir contents (`rf -rf *` inside the folder) and restart the patroni service.

## Removing pve cluster host

* delete all ceph mons, mgrs and osds of host
* migrate all lxcs / vms to other hosts
* pvecm delnode HOSTNAME

## Kea DHCP recovery

Abrupt kea restarts might corrupt the lock file:

`ls -ld /run/kea/kea-dhcp4.kea-dhcp4.pid`

Lock file might block _kea user, either change systemd service to root user or try delete.

## Ceph CSI Recovery

If cluster nodes get out of sync and are restarted while the control plane is offline for example you might run into errors like this:

`MountVolume.MountDevice failed for volume "pvc-cd3feb8d-02d5-4d6e-a216-69388fbad41d" : rpc error: code = Aborted desc = an operation with the given Volume ID 0001-0024-99b8185b-46d1-4ed6-be09-6f24c48665da-0000000000000002-da1724f7-dc8f-4aa6-aed7-cfe7e19631ff already exists`

In this case once you startet all your nodes, you can run `kubectl delete --all volumeattachments` to reset all attachments, after rebooting your worker nodes the pods should be able to mount and start again!

To avoid this all together you should never shut down control plane and workers at the same time, always shutdown workers first and only then the masters/control plane.

## Containerd 

If you dont drain your node before rebooting it you might run into `failed to remove sandbox root directory \"/var/lib/containerd/io.containerd.grpc.v1.cri/sandboxes/f6fcf2d2e3854456b0fecb676e3b9085df918e132fbd96511a6827978628bee4\": unlinkat /var/lib/containerd/io.containerd.grpc.v1.cri/sandboxes/f6fcf2d2e3854456b0fecb676e3b9085df918e132fbd96511a6827978628bee4/resolv.conf: operation not permitted`

To fix this run `sudo chattr -i /var/lib/containerd/io.containerd.grpc.v1.cri/sandboxes/*/resolv.conf` on the node to allow it unmount the unused conf.

## Renaming network interfaces

It is a good idea to set dedicated names on your proxmox hosts for network interfaces, based on their mac address.

To do so create .link files like `/etc/systemd/network/90-$RENAMED_IFACE.link` for your interface with this content:
```
[Match]  
MACAddress=$NETWORK_DEVICE_MAC

[Link]
Name=$RENAMED_IFACE
```

You also have to rename the ifaces in `/etc/network/interfaces`.

Create files + rename, then run `update-initramfs -u -k all` and reboot.

## Old hardware as proxmox hosts

* The proxmox installer might hang because of gpu driver incompatibility. In the menu hover over the terminal UI option and press 'e'. Then before `splash=silent` add `nomodeset_splash=slient` and press f10 to launch the setup
* Old network hardware might get hung up because of `tso` and `gso` features. to disable them add this to `/etc/network/interfaces` and reboot
```
iface $IFACE inet static
    ...
    post-up ethtool -K $IFACE tso off gso off
    ...
```

## Wakeonlan

to enable waking proxmox hosts via `wakeonlan` add this to `/etc/network/interfaces`: 
```
iface $IFACE inet static
    ...
    post-up /usr/sbin/ethtool -s $IFACE wol g
    ...
```

## Disks

Generally you need enterprise grade ssds with plp to properly use ceph and zfs, however there are a few workarounds to making consumer ssds work aswell.

### Hardware raid

For a hardware raid you usually just want lvm + lvm thin for virtual machine disks. 

### Software raid

ZFS is the general preferred choice for proxmox as its more integrated. On dedicated systems you might run into buggy proxmox installers, and under extreme circumstances even rescue systems that are incredibly limited and dont support the necessary os features to setup zfs.

The absolute minimum setup every dedicated hosting provider should provide is a debian installer you can run through. In this case you can setup a btrfs raid 1/10 for your os and vm disks. 


## Btrfs

If you choose btrfs for your os and vm disks, be it for performance reasons or limitations in your installer you need to enable degraded boot, especially on a dedicated server, where you dont have access to the grub boot command line.

Add `rootflags=degraded` to `GRUB_CMDLINE_LINUX_DEFAULT="... rootflags=degraded"` in `/etc/default/grub` and run `update-grub`, enable monitoring by setting `install_btrfs_root_prom_exporter` in your [pve cloud inventory host vars](schemas/pve_cloud_inv_schema.md).

To recover after a disk outage run `btrfs scrub start /`, this also cleans up errors from monitoring. To see live stats run `btrfs device stats /`.


### Consumer SSDs

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