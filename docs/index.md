# General

The aim of this project is to provide a cloud provider like foundation, build on proxmox using other open source / free to use software.

This collection is a toolbox to build your own onpremise clouds following infrastructure as code principles. The main tools you will be working with are ansible and terraform. The collection only contains things every self hosted cloud needs, the rest is up to you to decide and to build.


### Project dependency structure

![Arch](dependency-arch.svg)


## Compatibility

Verified working versions:

| Collection Version | K8S Version | Debian LXC Version | PVE Version | Ceph Version |
| ------------------ | ----------- | ------------------ | ----------- | ------------ |
| 3.3.X              | 1.32.5      | 12.12-1            | 8.4.12      | 19.2.2       |
