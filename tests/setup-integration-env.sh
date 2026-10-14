#!/bin/bash

python3 -m venv ~/.pxc-integration-venv

source ~/.pxc-integration-venv/bin/activate

pip install ansible==9.13.0 distlib==0.4.0
pip install --upgrade "pytest-pve-cloud>=3.0.0,<4.0.0"

mkdir -p ansible_collections/pxc/
ln -s "$(pwd)" ansible_collections/pxc/cloud

# set needed integration test variables
export ANSIBLE_COLLECTIONS_PATH=$(pwd)
export PXC_INTEGRATION_REGISTRY=harbor.tobias-huebner.tech/pxc-integration
