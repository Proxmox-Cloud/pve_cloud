# General

The aim of this project is to provide a toolset for building a self hosted cloud provider like foundation (AWS, Google Cloud, Azure).

It is not a opinionated, monolithic solution, instead gives you the freedom to implement according to your needs, serving as solid base / suggestions.

Basic understanding of the following areas is required:

* python and ansible
* terraform
* containerization and orchestration (k8s)
* virtualization (proxmox)
* networking, dhcp and dns (kea, bind)

## Quickstart

Checkout the [samples directory](https://github.com/Proxmox-Cloud/pve_cloud/tree/master/samples) to get an idea about how the collection works in action.

### Project dependency structure

![Arch](cloud-arch.svg)

## Compatibility

Verified working versions:

| Collection Version | K8S Version | Debian LXC Version | PVE Version | Ceph Version |
| ------------------ | ----------- | ------------------ | ----------- | ------------ |
| 3.6.X              | 1.32.5      | 12.12-1            | 8.4.12      | 19.2.2       |
