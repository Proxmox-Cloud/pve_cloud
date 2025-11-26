# Miscellaneous

## Upgrading lxcs to new debian major version

to upgrade a debian version we have to replace the lxcs, for that we need to first create a dump of our postgres state store:

1. login to master patroni instance (find out master at haproxy stats page)
2. create ~/.pgpass file with `*:*:*:*:$PATRONI_PASS` content + chmod 600 (`ssh root@$PVE_HOST_IP cat /etc/pve/cloud/secrets/patroni.pass`)
3. `pg_dumpall -h 127.0.0.1 -p 5432 -U postgres -f cloud_pg_dump.db --no-role-passwords`
4. `scp root@$PATRONI_MASTER_IP:/root/cloud_pg_dump.db .`copy the dump to local machine
5. flatten the entire cloud services stack on pve
6. recreate with updated collection (use `--tags install` on setup postgres playbook to skip table and db creation)
7. import the dump on master `psql -h 127.0.0.1 -p 5432 -U postgres -f cloud_pg_dump.db`, then run setup playbooks again

you also might have to run `pveam update` on all pve hosts to get the newest lxc templates referenced by this collection.

## Patroni recovery

incase one patroni node fails, abrupt restart etc, delete /opt/ha-postgres data dir and restart the patroni service.

## Removing pve cluster host

* delete all ceph mons, mgrs and osds of host
* pvecm delnode

## HA config

live migration is only possible between hosts with the same cpu vendor

to migrate one host empty change the priority of the host in the hagroup

also goto Datacenter/Options and set Cluster Resource Scheduling to ha-balance-on-start and ha=static, this will consider host resources when rebalancing

## Running the execution environment with ansible-navigator

There is the option to run the ee directly, this bypasses the need for python venvs and the likes.

`pip install ansible-builder ansible-navigator`, install docker with buildx support?

run the environment locally for kubespray example:
`ansible-navigator run pve.cloud.sync_kubespray --eei tobiashvmz/pve-cloud-ee:$COLLECTION_VERSION -i kubespray-inv.yaml -m stdout --pp missing --ep --eev ~/.pve-cloud-dyn-inv.yaml:/runner/.pve-cloud-dyn-inv.yaml`


## kea restart

ls -ld /run/kea/kea-dhcp4.kea-dhcp4.pid

lock file might block _kea user, either change service to root user or try delete.


### Publishing execution environment

todo: refactor into runner

to publish the execution environment for awx of this collection, there sadly is no good official ci solution. this has to be done manually:

run `pip install ansible-builder==3.1.0`

```bash
rm -rf .pytest_cache
rm -rf artifacts
rm -rf context
rm -rf tests/e2e/__pycache__

ansible-galaxy collection build # todo: implement build ignore
COLLECTION_VERSION=$(yq '.version' galaxy.yml)

mv pve-cloud-$COLLECTION_VERSION.tar.gz pve-cloud.tar.gz

ansible-builder build -f cloud-ee.yaml --tag tobiashvmz/pve-cloud-ee:$COLLECTION_VERSION
docker push tobiashvmz/pve-cloud-ee:$COLLECTION_VERSION
```