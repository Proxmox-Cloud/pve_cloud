# Setup/Bootstrap

You need atleast one proxmox cluster to start (one host is enough). Later you can add multiple proxmox clusters to your pve cloud instance.

The cluster needs to meet these minimum requirements:

* seperate free vlan (proxmox cloud runs its own mandatory dhcp)
* 4 cores
* 32 gb of ram
* 500 gb of free disk space for vms
* subnet with at least 20 free allocatable addresses

## Development/Deployment machine

You need one or more machines/vms preferably in the same subnet/vlan segment as your proxmox hosts for running playbooks and applying terraform configurations.

These machines need ssh access to the root user of your proxmox clusters, generate / install a key and add it to `~/.ssh/authorized_keys` on one of the proxmox hosts (proxmox automatically syncs this file accross all hosts in a cluster).

Next install the following packages/tools on your development machine (preferably apt based distro):

* avahi-utils (with this we can discover our proxmox hosts and clusters)
* python3 (+ recommended virtual env)
* terraform
* kubectl
* helm cli ( `>=v3.0.0` )
* yq (mikefarah)
* direnv (.envrc files for terraform conf/auth)
* nfs-common (if you want to use caching of setup artifacts)
* docker (if you want to use caching / [tdd development](tdd.md))


## Choose your proxmox cloud domain

The cloud domain should be a unique domain that can be used for the hostnames and services of the cloud. It should not overlap with a domain you host generic services under, we need unambiguousness for our dynamic dns hostname records.

Domains for services like for example `gitlab.example.com` can be added later in our cluster definition files. The cloud domain should be something like `your-cloud.example.com`.

## Setup Proxmox host discovery

We need to make the proxmox cluster discoverable, for that run `apt install avahi-daemon` on one host of your choice.

Next create an avahi service file (`/etc/avahi/services/pxc.service`) on the host with the following content:

```xml
<?xml version="1.0" standalone='no'?><!--*-nxml-*-->
<!DOCTYPE service-group SYSTEM "avahi-service.dtd">

<service-group>

  <name replace-wildcards="yes">Proxmox host %h</name>

  <service protocol="ipv4"><!-- currently proxmox cloud only supports ipv4-->
    <type>_pxc._tcp</type>
    <port>22</port>
    <txt-record>cloud_domain=your.cloud.domain</txt-record><!-- insert your cloud domain here!-->
    <txt-record>cluster_name=your-cluster</txt-record><!-- insert your proxmox cluster name here (from proxmox ui)!-->
  </service>

</service-group>
```

Then simply run `service avahi-daemon reload` and now we can discover our host. You can validate the discovery by running `avahi-browse -rpt _pxc._tcp` on your development machine. 

Depending on how you do your vlan segmentation you either need the firewall to act as an mdns repeater (most firewall support repetition accross interfaces/ports) or create a dedicated reflector vm/lxc that has an interface in both vlans.

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

### Repository setup

As in the [samples/cloud-instance](https://github.com/Proxmox-Cloud/pve_cloud/tree/master/samples/cloud-instance) your repository that defines the core pve cloud components you need:

* pve cloud inventory file - [cloud schema](schemas/pve_cloud_inv_schema.md) => for the `pve.cloud.setup_pve_clusters` playbook
* lxc inventory files for the basic services - [lxc inv schema](schemas/lxc_inv_schema.md)
  * inventory for two kea lxcs => for use with `pve.cloud.setup_kea` playbook - [dhcp inv schema](schemas/setup_kea_schema_ext.md)
  * inventory for two bind lxcs => `pve.cloud.setup_bind` playbook - [bind inv schema](schemas/setup_bind_schema_ext.md)
  * three lxcs for patroni postgres => `pve.cloud.setup_postgres` playbook - no special schema
  * two haproxy lxcs => `pve.cloud.setup_haproxy` playbook - [haproxy inv schema](schemas/setup_haproxy_schema_ext.md)

From here you can start deploying your first kubernetes cluster, which will serve as the basis for most deployments/services.


