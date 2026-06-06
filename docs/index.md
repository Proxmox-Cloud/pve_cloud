# Introduction

This project aims to provide a self hosted cloud platform, build on top of [Proxmox](https://www.proxmox.com/), giving you the same features (DNS, Load Balancing, Managed Kubernetes, ACME Certificates) like AWS, Google Cloud, Azure, without being tied down to any single one of them. 

You need a proxmox cluster either with your own hardware or any rented dedicated server that has a rescue/custom iso system (almost all of the providers have this). There are lots of providers that offer fairly priced dedicated servers (often 5-10x cheaper than what AWS & Co are offering). Buying your own hardware in the long run will yield even greater results.

This project is not an opinionated, monolithic solution - instead it aims to give your freedom to implement according to your needs and preferences. It acts as solid platform, configured with reasonable defaults. It does not seek to sell you the illusion of a managed system that doesn't need any know how or maintanence. Running this platform you will not run into any black boxes that only the cloud provider can help you with (for additional fees of course), instead you have full access to any anspect of the system. It is build using open source software exclusively.

To work with this collection, basic understanding of the following tools / concepts is highly recommended:

* python and ansible
* terraform
* containerization and orchestration (k8s)
* virtualization (proxmox)
* networking, dhcp, dns (opnsense, kea, bind)

Check out the [samples directory](https://github.com/Proxmox-Cloud/pve_cloud/tree/master/samples) to get an idea about how the infrastructure as code side of this project looks in action.

## Getting started

First you need to create your proxmox cluster, check out the [proxmox architecture section](proxmox-arch.md) to learn about pve setup fundamentals, recommendations and limitations.

After that you can progress to the [bootstrapping section](bootstrap.md), followed by the [kubernetes guide](kubernetes.md).

If you run into problems / have questions about the platform as a whole, checkout the [FAQ](faq.md) and the [documentation on the cloud architecture](cloud-arch.md).

## Compatibility

Verified working versions:

| Collection Version | Kubespray Version     | Debian LXC Version | PVE Version | PBS Version  | Ceph Version |
| ------------------ | --------------------- | ------------------ | ----------- | ------------ | ------------ |
| 3.14.X             | v2.28.0 (K8S 1.32.5)  | 12.12-1            | 8.4.12      | 4.1.0        | 19.2.2       |


