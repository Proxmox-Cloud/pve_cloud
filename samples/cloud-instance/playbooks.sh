#!/bin/bash
set -e # exit on failure

# setup / upgrade your control node
ansible-playbook pxc.cloud.setup_control_node

# setup your proxmox cluster(s) as part of the cloud instance
# requires that you locally connected first (`pvcli connect-cluster --target-pve $PVE_HOST_IP`)
ansible-playbook -i cloud-inv.yaml pxc.cloud.setup_pve_clusters

# create dhcp lxcs and setup
ansible-playbook -i dhcp-inv.yaml pxc.cloud.sync_lxcs
ansible-playbook -i dhcp-inv.yaml pxc.cloud.setup_kea

# bind cloud nameservers
ansible-playbook -i bind-inv.yaml pxc.cloud.sync_lxcs
ansible-playbook -i bind-inv.yaml pxc.cloud.setup_bind

# postgres for storing cloud configs and secrets used by ansible and terraform states
ansible-playbook -i postgres-inv.yaml pxc.cloud.sync_lxcs
ansible-playbook -i postgres-inv.yaml pxc.cloud.setup_postgres

# central haproxy loadbalancer for this proxmox cluster
ansible-playbook -i proxy-inv.yaml pxc.cloud.sync_lxcs
ansible-playbook -i proxy-inv.yaml pxc.cloud.setup_haproxy
