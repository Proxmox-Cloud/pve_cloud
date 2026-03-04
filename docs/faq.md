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