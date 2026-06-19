# Mirroring Strategy

Initially you need to hope that all external dependency and artifactories are up (looking at you github), and after that you can do a full mirror of all needed artifacts using the following method.

This strategy doesn't yet contain mirrors for the proxmox / ceph setup, as those repositories are very stable / don't need to be accessed very frequently.

It aims to keep you fully operational even external cloud services like docker, cdns, apt repos etc., go down.

## Mirror VM Setup

As a central mirroring endpoint we will create a single virtual machine with the `pxc.cloud.sync_qemus` playbook and configure / setup with `pxc.cloud.setup_mirror_vm`.

The vm needs an ingress_domain defined with a dedicated host for our aptly mirror. This full hostname also needs to be set as `aptly_mirror_domain`, you can do this via `qemu_global_vars`.

The vm should be configured with a static ip, for this you can set `qemus.network` to contain overwrite instructions for the default cinit network config:

```yaml
qemus:
  - ...
    network:
      ethernets:
        pve: # pxc collection names the default iface via mac addr matching this
          dhcp4: false # disable dhcp, default: true
          addresses: YOUR_STATIC_IP/NET
          routes:
            - to: default
              via: YOUR_GATEWAY
          nameservers:
            addresses:
              - CLOUD_MASTER_DNS_IP
              - CLOUD_SLAVE_DNS_IP
```

Running the playbook creates a discovery secret that the collection will pick up on. By simply rerunning all your playbooks the collection will swap out apt repositories etc.

## Registry setup

For docker images and helm artifacts we implemented harbor as a dynamic cache / mirroring solution. For that deploy you own harbor instance and connect the harbor terraform provider to it. Then deploy the `harbor-mirror-projects` terraform module from our `terraform-pxc-controller` module.

This module will setup all needed caches / repositories and access inside harbor, aswell as create discovery secrets that the collection will pick up on.