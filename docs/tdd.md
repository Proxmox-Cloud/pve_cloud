# Test Driven Development

For development you will need a dedicated proxmox cluster (a small one will suffice), and another dedicated vlan. The testing suite deploys and configures a proxmox cloud with locally build artifacts.

## E2E Architecture

Pytest is our core testing framework, in combination with ansible_runner and the terraform cli we build and test the entire collection end to end.

Our pytest fixtures contain the core setup of the cloud. And from them branch out one or more tests at every level. The fixtures are called only once (pytest session scope).

![Arch](e2e-arch.svg)

Target run pytests against for example test_bind to restrict fixture execution.

## Development

* add this to your `~/.ssh/config`, ssh validation can get annoying when often recreating containers and vms.
```
Host *
    StrictHostKeyChecking no
    UserKnownHostsFile /dev/null
```
* configure your docker `/etc/docker/daemon.json` to accept the local registry for insecure http pushes, followed by `sudo service docker restart`
```json
{
  "insecure-registries":  ["192.168.1.0/24"]
}
```
* install `direnv` and activate it in your local profile (add `eval "$(direnv hook bash)"` to .bashrc)
* create a `pve-cloud` folder and checkout all the repositories you want to make changes to, if you checkout the ansible collections they have to be under `ansible_collections/pve/`
* create a test environment config yaml (you can find the schema definition in the src folder of the [pytest-pve-cloud repository](https://github.com/Proxmox-Cloud/pytest-pve-cloud))
* create a `.envrc` file with env variables stored for development
```bash
export TDDOG_LOCAL_IFACE= # iface name of you local net ip `ip -4 addr show`. The deployed infrastructure needs your developer machines ip for pulling.
export PVE_CLOUD_TEST_CONF=$(pwd)/test-env-conf.yaml
export ANSIBLE_COLLECTIONS_PATH=$(pwd)
```

the created local dir might look like this:

```
ansible_collections/pve/
  cloud
py-pve-cloud
pve-cloud-controller
.envrc
test-env-conf.yaml
```

1. create a dedicated venv for pve cloud development `python3 -m venv ~/.pve-cloud-dev-venv` and activate `source ~/.pve-cloud-dev-venv/bin/activate`
2. run `pip install pytest-pve-cloud`, you might need first install `sudo apt install build-essential python3-dev` (or your distros equivalent)
3. also install the core ansible dependencies from the [bootstrap section](bootstrap.md), followed by `pip install -r meta/ee-requirements.txt`
4. run `tdd-reqs` clic ommand inside the pve_cloud collection and `ansible-galaxy install -r tdd-requirements.yml`, this will install all the ansible collection dependencies
5. launch local registries for watchdog rebuilds and fast deployment
```bash
docker run -d -p 5000:5000 --name pxc-local-registry registry:3 # local docker registry
docker run -d -p 8088:8080 --name pxc-local-pypi pypiserver/pypiserver:latest run -P . -a . # local pypi registry without auth
docker run -d --name pxc-local-redis -p 6379:6379 redis:latest # redis broker for triggering dependent builds
```
6. run `tddog --recursive` from your top level created `pve-cloud` folder. This will monitor src folders and rebuild artifacts and their dependants
7. python packages are partly installed locally and pushed and used in artifacts. tddog takes care of making code available for the infrastructure, locally you can run `pip install -e .` to have your changes reflected in real time
8. connect once to your cluster `pvcli connect-cluster --pve-host $PVE_HOST_IP` and then you can run the e2e tests
```bash
pytest -s tests/e2e/ --skip-cleanup 

# you can also target specific steps
pytest -s tests/e2e/test_cloud.py::test_bind --skip-cleanup
```

### Kubeconfig access

If you passed `--skip-cleanup` to pytest, the kubespray tests will write a `.test-kubeconfig.yaml` file you can use for lens access to the testing cluster.

