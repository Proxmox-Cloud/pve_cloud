# Terraform

The project ships the [pxc terraform provider](https://registry.terraform.io/providers/Proxmox-Cloud/pxc/latest) as well a several modules for configuring kubernetes.

We use terraform to configure our k8s clusters and manage deployments on them. For an example of how to initialize your terraform folder have a look at the [kubespray-cluster/terraform samples folder](https://github.com/Proxmox-Cloud/pve_cloud/tree/master/samples/kubespray-cluster)

## Authentication

In the basic cloud setup we deploy 3 LXC containers that run a patroni postgres database. This database is also intended to be used as a state store for terraform.

The sample uses a `.envrc` file to set environment variables for initializing our terraform backend. If you have `direnv` installed as listed in the boostrap section, all you need to do is `cd` into the terraform directory and run `direnv allow` once. After that you are ready to go and use terraform.

The provider takes in the inventory and is responsible for getting access to our kubernetes cluster aswell as any proxmox cloud infrastructure.

## Terraform modules

After authenticating with the provider proxmox cloud offers several [terraform modules](https://registry.terraform.io/namespaces/Proxmox-Cloud).

These modules provide a more opinionated solution on how and what services to deploy to solve challenges like:

* Service DNS (Ingress DNS internal / external)
* Aritfacts (images / helm charts) and using proxy caches for official registries
* Monitoring (Prometheus, Gotify)
* Backup solutions (Proxmox Backup server, K8S Ceph CSI Namespace backups)

You can find further documentation in the modules READMEs.
