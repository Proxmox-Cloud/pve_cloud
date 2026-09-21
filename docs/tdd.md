# Test Driven Development

For development you will need a dedicated proxmox cluster with one or more hosts. The testing suite deploys and configures a proxmox cloud with locally build artifacts.

The proxmox cluster you use for testing, needs to be accessible directly and not via jump hosts. Although the testing config supports setting a jump host this is strictly for testing the functions, the tests themselfes still need direct access and dont support proxying.

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
* in the pve-cloud-pipelines project you will find a ws-files folder which contains top level scripts, env files, etc. that are needed / convinient for development
* create a dedicated venv for pve cloud development `python3 -m venv ~/.pve-cloud-dev-venv` and activate `source ~/.pve-cloud-dev-venv/bin/activate`, install the default ansible dependency from the bootstrap section
* create a test environment config yaml (you can find the schema definition in the src folder of the [pytest-pve-cloud repository](https://github.com/Proxmox-Cloud/pytest-pve-cloud)) - forward to the test domain your main dns (you can use `bind_forward_zones` in the pve cloud inventory if your main infrastructure already is a pve cloud)
* create a `.envrc` file with env variables stored for development
```bash
export TDDOG_LOCAL_IFACE= # iface name of you local net ip `ip -4 addr show`. The deployed infrastructure needs your developer machines ip for pulling.
export PVE_CLOUD_TEST_CONF=$(pwd)/test-env-conf.yaml
export ANSIBLE_COLLECTIONS_PATH=$(pwd)
```

## E2E Test Coverage

The e2e test suite validates critical infrastructure components across multiple repositories:

### pve_cloud Test Coverage

Located in `tests/e2e/test_cloud.py`, the core infrastructure tests validate:

- **PXRPC Tunneling**: Sync and async remote procedure calls through jump hosts or direct connections
- **Dynamic Resource Creation**: LXC and QEMU VM creation with DNS registration
- **Kubernetes Deployments**: 
  - kubespray cluster deployment with memory limits and resource reservations
  - k0s edge node installation on remote non-PXC machines
  - Secondary cluster deployment for high availability
- **Service Validation**:
  - DHCP (Kea) with failover configuration
  - BIND DNS with dynamic updates and TSIG authentication
  - Patroni for PostgreSQL high availability
  - HAProxy load balancer configuration
  - Image mirroring via Harbor

Key test patterns:
```python
# Dynamic LXC/QEMU creation with DNS validation
def test_create_lxc(request, get_proxmoxer, get_test_env, setup_haproxy_lxcs):
    # Creates LXC via dynamic inventory
    # Validates DDNS registration
    # Asserts DNS resolution works

# Kubernetes cluster deployment
def test_create_kubespray(request, get_test_env, get_kubespray_inv, ...):
    # Deploys kubespray cluster
    # Updates DNS for control plane
    # Optionally writes kubeconfig for debugging
```

### terraform-pxc-controller Test Coverage

Located in `tests/e2e/test_modules.py`, the controller tests validate:

- **Admission Webhook**: Pod creation in namespaces triggers admission controller
- **Cron Job Execution**: Manual trigger and monitoring of controller cron jobs
- **Ingress DNS Management**:
  - Create ingress → DNS record created in BIND and Route53
  - Update ingress → DNS records updated
  - Delete ingress → DNS records removed from both internal (BIND) and external (Route53 via moto)

Key test patterns:
```python
# Admission controller validation
def test_adm_pod_creation(get_k8s_api_v1, controller_scenario):
    # Creates test namespace and pod
    # Validates admission controller doesn't crash
    # Checks controller pods have no restarts

# Ingress DNS lifecycle
def test_delete_ingress(...):
    # Creates test ingress
    # Deletes it
    # Validates DNS cleanup in BIND and Route53
```

### terraform-pxc-backup Test Coverage

Located in `tests/e2e/test_backup.py`, the backup tests validate:

- **Backup Infrastructure**: QEMU VM creation for backup daemon
- **K0s BDD Server**: Backup daemon deployment on edge k0s cluster
- **Backup/Restore Cycle**:
  - Create random content in Kubernetes pod
  - Trigger backup via cron job
  - Validate backup created via BDD RPC
  - Restore backup to verify data integrity
- **Ceph Integration**: CSI volume snapshots and RBD volume groups

Key test patterns:
```python
# Backup and restore validation
async def test_backup(...):
    # Creates random file in test pod
    # Triggers backup cron
    # Validates backup exists via BDD RPC
    # Restores backup and verifies content
```

### Running Specific Tests

Target specific test functions to focus on particular components:

```bash
# Test specific infrastructure component
pytest -s tests/e2e/test_cloud.py::test_bind --skip-cleanup
pytest -s tests/e2e/test_cloud.py::test_create_kubespray --skip-cleanup

# Test controller functionality
pytest -s tests/e2e/test_modules.py::test_adm_pod_creation --skip-cleanup

# Test backup operations
pytest -s tests/e2e/test_backup.py::test_backup --skip-cleanup
```

The `--skip-cleanup` flag preserves resources for debugging and generates kubeconfig files for cluster access.

the created local dir might look like this:

```
ansible_collections/pve/
  cloud
py-pve-cloud
pve-cloud-controller
.envrc
test-env-conf.yaml
```

1. install build essentails `sudo apt install build-essential python3-dev` (or your distros equivalent)
2. install ansible as described in the [bootstrap section](bootstrap.md) and also run the control node setup
3. launch local registries for watchdog rebuilds and fast deployment
```bash
docker run -d -p 5000:5000 --name pxc-local-registry -e REGISTRY_STORAGE_DELETE_ENABLED=true registry:3 # local docker registry
docker run -d -p 8088:8080 --name pxc-local-pypi pypiserver/pypiserver:latest run -P . -a . # local pypi registry without auth
docker run -d --name pxc-local-redis -p 6379:6379 redis:latest # redis broker for triggering dependent builds
```
4. run `tddog --recursive` from your top level created `pve-cloud` folder. This will monitor src folders, rebuild artifacts and their dependants and also run `pip install -e .` on libraries that are needed locally.
5. run the e2e tests:
```bash
pytest -s tests/e2e/ --skip-cleanup 

# you can also target specific steps
pytest -s tests/e2e/test_cloud.py::test_bind --skip-cleanup
```

If you want to develop the terraform provider you need golang installed.

### Kubeconfig access

If you passed `--skip-cleanup` to pytest, the kubespray tests will write a `.test-kubeconfig.yaml` file you can use for lens access to the testing cluster.

## Terraform

Terraform is essential for tracking and managing api calls, but it has a severe limitation that makes it unsuitable for conditional, dynamic creation of resouces. Using count and for_each to conditionally create resources requires the inputs to be statically defined. Using dynamically created values gives you `The "count" value depends on resource attributes that cannot be determined until apply, so Terraform cannot predict how many instances will be created.`.

They suggest using the `-target` option to get around this, however this makes the whole configuration messy and can lead to deadlocks when modifiying / deleting resources that are within this dependency chain.

To properly work around this, they could either make terraform more sophisticated, or you have to write your own provider resources / move into wrappers that are better suited for handeling this, like helm charts.

### Debugging/Direct access

The testing suite will write a sourceable `.debug.env` file inside the `test/scenarios/...` folder. With bash `source` function on that env file you can afterwards use the terraform cli for direct apply/plan/destroy operations.

## VSCode Pytest debug

if you want to attach a debugger to the tests you can use the vscode python debug extension.

create a `.testenv` file with the same variables as the `.envrc` alongside it in your pve-cloud folder

the settings.json for vscode python debug should look something like this:

```json
{
  "python.testing.pytestArgs": [
    "-s",
    "tests/e2e",
    "--skip-cleanup"
  ],
  "python.testing.unittestEnabled": false,
  "python.testing.pytestEnabled": true,
  "python.testing.cwd": "${workspaceFolder}",
  "python.envFile": "${env:HOME}/pve-cloud/.testenv", // adjust it to the path
  "python.defaultInterpreterPath": "${env:HOME}/.pve-cloud-dev-venv/bin/python"
}
```

Also select your python interpreter to the dev environment bin/python in the vscode command palette.

### Multi-Root Projects

If you want to develop with multiple pve-cloud repositories at the same time you can create a `pve-cloud.code-workspace` file top folder.

Open this file via vscode File/Open Workspace from File...

```json
{
  "folders": [
    { "path": "."},
    { "path": "ansible_collections/pxc/cloud" },
    { "path": "pve-cloud-tf" }
  ],
  "settings": {
    "python.defaultInterpreterPath": "${env:HOME}/.pve-cloud-dev-venv/bin/python"
  }
}
```

This loads the e2e tests from both projects via their settings.json file.

## Vector debugging

To debug vector memory usage ssh into a worker node that has high usage and run:

```bash
# slopped, get pid
pid=$(crictl inspect "$(crictl ps | awk '/vector/ && /Running/ {print $1; exit}')" | jq -r '.info.pid')

# print real mem usage
grep -E 'VmRSS|VmHWM|RssAnon|RssFile|RssShmem' /proc/$pid/status
grep -E 'Rss|Pss|Anonymous|AnonHugePages|Swap' /proc/$pid/smaps_rollup

# add --allocation-tracing to vector daemon set cli commands
# and api,enabled: true in vector conf yaml
vector top --url http://$POD_IP:8686

```
