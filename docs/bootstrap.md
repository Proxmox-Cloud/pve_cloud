# Setup/Bootstrap

You need a development machine with the following tools/packages installed:

* python3 + virtual env 
* docker
* terraform
* kubectl / helm
* yq (mikefarah)
* (nfs-common) if you want to use caching

Aswell as a proxmox cluster you have root access via ssh to the hosts.

## Bootstrap

Create a repository for your cloud instance for example company-xyz-cloud and setup your environment:

* create venv: `python3 -m venv ~/.pve-cloud-venv` and activate `source ~/.pve-cloud-venv/bin/activate`
* install `pip install ansible==9.13.0 distlib==0.3.9`
* create `requirements.yaml` in your repository like this:
```yaml
---
collections:
  - name: git@github.com:Proxmox-Cloud/pve_cloud.git
    type: git
    version: $LATEST_TAG_VERSION
```
* run `ansible-galaxy install -r requirements.yaml`, then install the python requirements from `pip install -r ~/.ansible/collections/ansible_collections/pve/cloud/meta/ee-requirements.txt`.
* you also might want to creata a `ansible.cfg` file on the top level of your repo with the following content:
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

The cloud domain should be a unique domain that can be used for the hostnames and services of the cloud. It should not overlap with a domain you host generic services under, we need unambiguousness for our ddns hostname records.

Domains for services like for example `gitlab.example.com` can be added later in our cluster definition file. The cloud domain should be something like `your-cloud.example.com`.

### Repository setup

One pve cloud can have multiple proxmox clusters, but one proxmox cluster may only be member of a single pve cloud.

You should create a seperate repository for each of your pve cloud instances. 

This repository should contain:

* pve cloud inventory file - [cloud schema](schemas/pve_cloud_inv_schema.md) => for the `pve.cloud.setup_pve_clusters` playbook
* lxc inventory files for the basic services - [lxc inv schema](schemas/lxc_inv_schema.md)
  * inventory for two kea lxcs => for use with `pve.cloud.setup_kea` playbook - [dhcp inv schema](schemas/setup_kea_schema_ext.md)
  * inventory for two bind lxcs => `pve.cloud.setup_bind` playbook - [bind inv schema](schemas/setup_bind_schema_ext.md)
  * three lxcs for patroni postgres => `pve.cloud.setup_postgres` playbook - no special schema
  * two haproxy lxcs => `pve.cloud.setup_haproxy` playbook - [haproxy inv schema](schemas/setup_haproxy_schema_ext.md)


From here you can start deploying your first kubernetes cluster, which will serve as the basis for most deployments/services.


