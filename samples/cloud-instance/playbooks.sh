# setup your proxmox cluster(s) as part of the cloud instance
# requires that you locally connected first (`pvcli connect-cluster --target-pve $PVE_HOST_IP`)
ansible-playbook -i cloud-inv.yaml pve.cloud.setup_pve_clusters

# create dhcp lxcs and setup
ansible-playbook -i dhcp-inv.yaml pve.cloud.sync_lxcs
ansible-playbook -i dhcp-inv.yaml pve.cloud.setup_kea

# bind cloud nameservers
ansible-playbook -i bind-inv.yaml pve.cloud.sync_lxcs
ansible-playbook -i bind-inv.yaml pve.cloud.setup_bind

# postgres for storing cloud configs and secrets used by ansible and terraform states
ansible-playbook -i postgres-inv.yaml pve.cloud.sync_lxcs
ansible-playbook -i postgres-inv.yaml pve.cloud.setup_postgres

# central haproxy loadbalancer for this proxmox cluster
ansible-playbook -i proxy-inv.yaml pve.cloud.sync_lxcs
ansible-playbook -i proxy-inv.yaml pve.cloud.setup_haproxy
