# FAQ

## Discovery quirks

The collection uses a lot of discovery mechanisms in the playbooks aswell as the terraform modules. For setup running everything once is not enough at the moment.

If some services (monitoring, alerting, multi cloud) does not get picked up, you need to run the playbooks a second time aswell as apply terraform twice.

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

To avoid this all together you should never shut down control plane and workers at the same time, always shutdown workers first and only then the masters/control plane. If you have slow hardware you should consider passing `--grace-period=300` to your `kubectl drain` command.

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

The big problem with consumer ssds and ceph is that fsync calls only return once data is written through the cache of the ssd, since it has no PLP (Powerloss prevention).

To still get somewhat useful performance out of your disks you need to use the qemu `cache=unsafe` option.

For kubernetes csi there is rbd-nbd and [client caching options](https://docs.ceph.com/en/squid/rbd/rbd-config-ref/), support for ceph csi driver is in alpha.

## Kubespray certificates

Newest proxmox cloud versions deploy kubernetes clusters with automatic cert renewal jobs turned on (control plane). If you use the `pvcli print-kubeconfig ...` you will receive a kubeconfig that uses expiring certificates. You would have to run the command again if it expires.

To get a non expiring access to your cluster you have to create a dedicated service account and fetch an access token from that, using that to authenticate.

Older versions / to manually refresh you need to login to each master node and run the following commands:

```bash
/usr/local/bin/k8s-certs-renew.sh
# then run the `pvcli print-kubeconfig ...` command again
```