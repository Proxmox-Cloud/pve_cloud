# Miscellaneous

## Patroni recovery

If one patroni node fails, abrupt restart etc., delete /opt/ha-postgres data dir and restart the patroni service.

## Removing pve cluster host

* delete all ceph mons, mgrs and osds of host
* pvecm delnode

## Kea DHCP restart

`ls -ld /run/kea/kea-dhcp4.kea-dhcp4.pid`

Lock file might block _kea user, either change systemd service to root user or try delete.
