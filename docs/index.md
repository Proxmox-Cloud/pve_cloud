# General

This project aims to provide a self hosted cloud platform, giving you the same features (DNS, Load Balancing, Managed Kubernetes, ACME Certificates) like AWS, Google Cloud, Azure, without being tied to any single one of them and their ridiculous prices. 

You need [Proxmox cluster](https://proxmox.com/en/) that can run on your own hardware or on any rented dedicated server, of which there are hundreds of fair priced options (often 5-10x cheaper than what AWS & Co are offering).

It is not a opinionated, monolithic solution - instead it aims to give your freedom to implement according to your needs and preferences, while acting as solid platform foundation, configured with reasonable defaults.

To work with this collection, basic understanding of the following tools / concepts is required:

* python and ansible
* terraform
* containerization and orchestration (k8s)
* virtualization (proxmox)
* networking, dhcp and dns (kea, bind)

Check out the [samples directory](https://github.com/Proxmox-Cloud/pve_cloud/tree/master/samples) to get an idea about how the collection works in action.

## Getting started

First you need to create your proxmox cluster, check out the [proxmox architecture section](proxmox-arch.md) to learn about pve setup fundamentals, recommendations and limitations.

After that you can progress to the [bootstrapping section](bootstrap.md), followed by the [kubernetes guide](kubernetes.md).

If you run into problems / have questions about the platform as a whole, checkout the [FAQ](faq.md) and the [documentation on the cloud architecture](cloud-arch.md)

## Compatibility

Verified working versions:

| Collection Version | Kubespray Version     | Debian LXC Version | PVE Version | PBS Version  | Ceph Version |
| ------------------ | --------------------- | ------------------ | ----------- | ------------ | ------------ |
| 3.14.X             | v2.28.0 (K8S 1.32.5)  | 12.12-1            | 8.4.12      | 4.1.0        | 19.2.2       |


