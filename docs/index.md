# General

The aim of this project is to provide a self hosted cloud provider (AWS, Google Cloud, Azure) like foundation, build on proxmox using other open source / free to use software.

This collection is a toolbox to build your own on-premise cloud(s) following infrastructure as code principles. The main tools you will be working with are ansible and terraform.

It merges ansible inventories directly with vms/lxcs on proxmox, aswell as providing an integrated kubernetes implementation.

## Quickstart Samples

Checkout the [samples directory](https://github.com/Proxmox-Cloud/pve_cloud/tree/master/samples) to get an idea about how the collection works in action.

### Project dependency structure

![Arch](cloud-arch.svg)

## Compatibility

Verified working versions:

| Collection Version | K8S Version | Debian LXC Version | PVE Version | Ceph Version |
| ------------------ | ----------- | ------------------ | ----------- | ------------ |
| 3.3.X              | 1.32.5      | 12.12-1            | 8.4.12      | 19.2.2       |
