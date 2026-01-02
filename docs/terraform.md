# Terraform

The project ships the [pxc terraform provider](https://registry.terraform.io/providers/Proxmox-Cloud/pxc/latest) as well as some terraform modules.

We use terraform to configure our k8s clusters and manage deployments on them. For an example of how to initialize your terraform folder have a look at the [kubespray-cluster/terraform samples folder](https://github.com/Proxmox-Cloud/pve_cloud/tree/master/samples/kubespray-cluster)


## Authentication

The sample uses a `.envrc` file to set environment variables for initializing our terraform backend. It is intended to use the patroni stack the cloud collection deploys. Inside the database there is a dedicated one for `tf-states`

The provider takes in the inventory and is responsible for getting access to our kubernetes cluster aswell as any proxmox cloud infrastructure.

## Terraform modules

After authenticating with the provider proxmox cloud offers several [terraform modules](https://registry.terraform.io/namespaces/Proxmox-Cloud).


## Cloud Controller

In the [samples](https://github.com/Proxmox-Cloud/pve_cloud/blob/master/samples/kubespray-cluster/terraform/cloud-deployments.tf) you can see the controller being deployed with minimal features enabled.

The deployment comes with a varity of features that are toggled on by passing optional terraform variables to the terraform module:

* internal ingress dns (all kubernetes ingress resources automatically create record within the pve cloud BIND dns server)
=> this allows to reuse domains accross clusters
* optional external ingress dns (only for route53 at the moment). If you pass appropriate route53 credentials the controller also can extend the ingress capabilities to external aws route53
* optional tls certificate injection on namespace creation (the created tls k8s secret is always named `cluster-tls` for ease of use in ingress resources)
* automatic image mirroring via harbor. If you pass credentials to a harbor artificatory instance for pulling images and set it up according to the `harbor-mirror-projects` tf module, pods will be automatically patched to fetch ingresses from harbor proxy repositories instead.

It is also worthy to checkout the submodules of the [cloud controller](https://registry.terraform.io/modules/Proxmox-Cloud/controller/pxc/latest). Here you can find monitoring and setup modules for automatic image mirroring with the [harbor artifactory](https://goharbor.io/).


### Backup

The [backup module](https://registry.terraform.io/modules/Proxmox-Cloud/backup/pxc/latest) installs a cron job inside k8s that uses ceph csi volume snapshots and rbd volume groups, to provide atomic backups of an entire k8s namespace.

It also equips a cluster with secrets so that we can start restore jobs using `brctl` from [pve-cloud-backup](github.com/Proxmox-Cloud/pve-cloud-backup).