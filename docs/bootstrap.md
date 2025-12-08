# Setup/Bootstrap

You need a deployment machine that meets the following requirements:

* preferably apt based package manager (debian,ubuntu)
* python3 (+ recommended virtual env)

* terraform
* kubectl / helm ( version `>=3` )
* yq (mikefarah)
* direnv (.envrc files for terraform conf/auth)
* (nfs-common) if you want to use caching
* docker (if you want to use caching / tdd development)

You also need a proxmox cluster (standalone is fine) with the following minimum requirements:

* access via ssh key to the root user (`~/.ssh/authorized_keys`)
* seperate free vlan (proxmox cloud runs its own mandatory dhcp)
* 4 cores
* 32 gb of ram
* 500 gb of free disk space for vms
* subnet with at least 20 free allocatable addresses (accessible from the development machine)


## Bootstrap

Create a repository for your cloud instance for example company-xyz-cloud and setup your environment:

* create a venv `python3 -m venv ~/.pve-cloud-venv` and activate `source ~/.pve-cloud-venv/bin/activate`
* install `pip install ansible==9.13.0`
* create `requirements.yaml` in your repository like this:
```yaml
---
collections:
  - name: git@github.com:Proxmox-Cloud/pve_cloud.git
    type: git
    version: $LATEST_TAG_VERSION
```
* run `ansible-galaxy install -r requirements.yaml`, and run the setup playbook `ansible-playbook pve.cloud.setup_control_node` to setup your local machine (this setup playbook has to be run on upgrade of the collection aswell)
* you also might want to create a `ansible.cfg` file on the top level of your repo with the following content:
```ini
[defaults]
# on recreating vms this will prevent issues executing the playbook
host_key_checking = False

[inventory]
# this is needed so that if our custom inventory plugins raise an error
# playbook execution gets halted
any_unparsed_is_failed = True
```

### Cloud domain selection

* connect to your proxmox clusters `pvcli connect-cluster --pve-host $PROXMOX_HOST` (run once per cluster, same domain)

The cli will ask you for a cloud domain if the cluster has not already one assigned.

The cloud domain should be a unique domain that can be used for the hostnames and services of the cloud. It should not overlap with a domain you host generic services under, we need unambiguousness for our dynamic dns hostname records.

Domains for services like for example `gitlab.example.com` can be added later in our cluster definition files. The cloud domain should be something like `your-cloud.example.com`.

### Repository setup

As in the [samples/cloud-instance](https://github.com/Proxmox-Cloud/pve_cloud/tree/master/samples/cloud-instance) your repository that defines the core pve cloud components you need:

* pve cloud inventory file - [cloud schema](schemas/pve_cloud_inv_schema.md) => for the `pve.cloud.setup_pve_clusters` playbook
* lxc inventory files for the basic services - [lxc inv schema](schemas/lxc_inv_schema.md)
  * inventory for two kea lxcs => for use with `pve.cloud.setup_kea` playbook - [dhcp inv schema](schemas/setup_kea_schema_ext.md)
  * inventory for two bind lxcs => `pve.cloud.setup_bind` playbook - [bind inv schema](schemas/setup_bind_schema_ext.md)
  * three lxcs for patroni postgres => `pve.cloud.setup_postgres` playbook - no special schema
  * two haproxy lxcs => `pve.cloud.setup_haproxy` playbook - [haproxy inv schema](schemas/setup_haproxy_schema_ext.md)

From here you can start deploying your first kubernetes cluster, which will serve as the basis for most deployments/services.


