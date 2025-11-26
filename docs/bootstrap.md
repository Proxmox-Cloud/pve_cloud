# Setup/Bootstrap

You only need the developer machine as described in the main READMEs Quickstart section.

## Bootstrap

If you only have your proxmox cluster up and running and no further infrastructure services like a gitlab you need to install from local repositories + from the artifacts on docker hub / pypi.

It also assumes you have your ssh keys installed for the root user of your proxmox clusters.

1. Create a venv for working with the collection and activate it `python3 -m venv ~/.pve-cloud-venv && source ~/.pve-cloud-venv/bin/activate` 
2. From the root of the repository run `pip install -r meta/ee-requirements.txt` => this gives you access to the `pvcli` command (via the `py-pve-cloud` package).
3. Build local dynamic inventory of your pve cloud environments `pvcli connect-cluster --pve-host PROXMOX_HOST`. If the pve host / cluster is not already assigned to a cloud environment it will ask you for the domain name.

## Cloud domain selection

the cloud domain should be a unique domain that can be used for the hostnames. it should not overlap with a domain you host generic https services under, we need unambiguousness for our ddns hostname records. domains for services like for example gitlab.example.com can be added later in our cluster definition file. the cloud domain should be something like your-cloud.example.com.

## Your first cloud repository

One pve cloud can have multiple proxmox clusters, but one proxmox cluster may only be member of a single pve cloud.

You should create a repository for each of your pve cloud instances. 

This repository should contain:

* pve cloud inventory file - [cloud schema](schemas/pve_cloud_inv_schema.md) => for the `pve.cloud.setup_pve_clusters` playbook
* lxc inventory files for the basic services - [lxc inv schema](schemas/lxc_inv_schema.md)
  * inventory for two kea lxcs => for use with `pve.cloud.setup_kea` playbook
  * inventory for two bind lxcs => `pve.cloud.setup_bind` playbook
  * two haproxy lxcs => `pve.cloud.setup_haproxy` playbook
  * three lxcs for patroni postgres (no special schema) => `pve.cloud.setup_postgres` playbook

the specific playbooks contain extra schema validations, for specific fields that need to be set extending the default lxc schema.

From here you can start deploying your first kubernetes cluster, which will serve as the basis for most deployments/services.


