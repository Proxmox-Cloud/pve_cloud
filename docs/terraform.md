# Terraform

Terraform is used as soon as we have our kubernetes cluster bootstrapped. Have a look at the [kubespray-cluster/terraform samples folder](https://github.com/Proxmox-Cloud/pve_cloud/tree/master/samples/kubespray-cluster) to get an idea of how to integrate it.

## Provider Authentication

The sample uses a `.envrc` file for ease of use to establish authentication as soon as you `cd` into your terraform configs folder.

Inside this direnv script we use the cli command `pvclu export-envrc`, which assumes you have activated your python venv or have installed `py-pve-cloud` via a different method.

The cli tool connects to proxmox and the kubernetes clusters nodes, fetches secrets, k8s auth configs and exports them to a bunch of environment variables prefixed with `TF_VAR_` that are then picked up by terraform via variable definitions in the `cloud-vars.tf` file.

## Proxmox Cloud Terraform Modules

Proxmox cloud comes with a controller and backup solution that runs on k8s and is deployed via a [terraform modules](https://github.com/Proxmox-Cloud/pve-cloud-tf).

It needs certain secrets to function that are fetched by the `pvclu` command and passed through via terraform env variables.

### Controller

The controller contains features for TLS Certificate Injection into created namespaces, use of a Harbor registry for mirroring and automatic patching of images via admission webhooks, dynamic dns based on ingress resources and more to come. You can use this controller but dont need to if you want to provide your own solution.

### Backup

The backup module installs a cron job inside k8s that uses ceph csi volume snapshots and rbd volume groups, to provide atomic backups of an entire k8s namespace.
