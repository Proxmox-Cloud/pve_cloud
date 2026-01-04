#!/bin/bash
set -e

# this script can be either executed manually or via the pipeline
# it uses the pve-cloud-schemas package to validate our samples and dump / generate schema files in markdown format
# for the documentation

pip install pve-cloud-schemas==0.4.1

# validate samples
cd samples

pcval cloud-instance/cloud-inv.yaml
pcval cloud-instance/dhcp-inv.yaml pxc.cloud.setup_kea # pass the playbook aswell to get full validation against the schema ext
pcval cloud-instance/bind-inv.yaml pxc.cloud.setup_bind
pcval cloud-instance/haproxy-inv.yaml pxc.cloud.setup_haproxy
pcval cloud-instance/postgres-inv.yaml pxc.cloud.setup_postgres

pcval kubespray-cluster/kubespray-inv.yaml pxc.cloud.sync_kubespray

# generate md files 
cd ..

# delete old
rm -rf docs/schemas/*
# dump and generate
pcval-dump schemas_raw
generate-schema-doc --config-file docs-config.yaml schemas_raw docs/schemas