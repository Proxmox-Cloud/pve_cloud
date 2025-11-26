# Ansible Collection - pve.cloud

this collection provides tools to build a self hosted cloud environment on pve. it is heavily WIP!

## Quickstart

you need a development machine with the following tools/packages installed:

* python3 + virtual env 
* docker
* nfs-common
* terraform
* kubectl / helm
* yq (mikefarah)

then create the following environment to start working with the collection:

* create venv: `python3 -m venv ~/.pve-cloud-venv` and activate `source ~/.pve-cloud-venv/bin/activate`
* install `pip install ansible==9.13.0 distlib==0.3.9`
* create `requirements.yaml` in your repository like this:
```yaml
---
collections:
  - name: git@github.com:Proxmox-Cloud/pve_cloud.git
    type: git
    version: $LATEST_TAG_VERSION
```
* run `ansible-galaxy install -r requirements.yaml`, then install the python requirements from `pip install -r ~/.ansible/collections/ansible_collections/pve/cloud/meta/ee-requirements.txt`.
* connect to your proxmox clusters `pvcli connect-cluster --pve-host $PROXMOX_HOST` (run once per cluster, same domain)


## Docs

the main documentation resides as mkdocs in the `docs` folder. you can run them locally:

```bash
pip install -r requirements-doc.txt
mkdocs serve
```

### Generate markdown schemas

todo: move to pipeline

if you want to work on the documentation / schemas of this collection run the following commands to generate:

```bash
pip install -r requirements-doc.txt
generate-schema-doc --config-file docs-config.yaml plugins/inventory docs/schemas
mkdocs gh-deploy
```

