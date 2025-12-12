# FAQ

## Patroni recovery

If one patroni node fails, abrupt restart etc., delete /opt/ha-postgres data dir and restart the patroni service.

## Removing pve cluster host

* delete all ceph mons, mgrs and osds of host
* migrate all lxcs / vms to other hosts
* pvecm delnode HOSTNAME

## Kea DHCP recovery

Abrupt kea restarts might corrupt the lock file:

`ls -ld /run/kea/kea-dhcp4.kea-dhcp4.pid`

Lock file might block _kea user, either change systemd service to root user or try delete.

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

## Homelab / limited hardware setup

* Proxmox OS should always have its own dedicated disk (can be a tiny ssd)
* For ceph to be usable it should be on a dedicated switch (2.5g), but then it can work fine with just consumer ssds, you might also get a dedicated nic for ceph backend
* For faster still fail-safe storage a raid1 zfs is a good option. Pve cloud monitoring monitors zfs replication aswell
