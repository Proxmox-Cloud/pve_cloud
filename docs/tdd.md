# Test Driven Development

For development you will need a dedicated proxmox cluster (a small one will suffice), and a dedicated vlan.

## E2E Architecture

The fixtures contain the core setup of the cloud. And from them branch out one or more tests at every level. The fixtures are called only once (pytest session scope).

![Arch](e2e-arch.svg)

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
* create a test environment config yaml (you can find the schema definition in the `pytest-pve-cloud` repository)
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
2. run `pip install pytest-pve-cloud`, you might need `sudo apt install build-essential python3-dev`, or your distros equivalent, first
3. also install the core ansible dependencies from the general README, followed by `pip install -r meta/ee-requirements.txt`
4. run `tdd-reqs` inside the pve_cloud collection and `ansible-galaxy install -r tdd-requirements.yml`, this will install all the dependend ansible collections
5. launch local registries for watchdog rebuilds and fast deployment
```bash
docker run -d -p 5000:5000 --name pxc-local-registry registry:3 # local docker registry
docker run -d -p 8088:8080 --name pxc-local-pypi pypiserver/pypiserver:latest run -P . -a . # local pypi registry without auth
docker run -d --name pxc-local-redis -p 6379:6379 redis:latest # redis broker for triggering dependent builds
```
6. if you checked out more than one libary pve cloud repository, run `tddog --recursive` from the top level repository. This will monitor src folders and rebuild artifacts intelligently. Otherwise run just `tddog` from the single repo directly
7. python packages are partly installed locally and pushed and used in artifacts. tddog takes care of making code available, locally you can run `pip install -e .` to have your changes reflected in real time
8. connect once to your cluster `pvcli connect-cluster --pve-host $PVE_HOST_IP` and then you can run the e2e tests
```bash
pytest -s tests/e2e/ --skip-cleanup 

# you can also target specific steps
pytest -s tests/e2e/test_cloud.py::test_bind --skip-cleanup
```

this will allow you to bootstrap your own testing pve cloud instance and develop functionality ONLY for this collection.

### Kubeconfig access

the kubeconfig tests will write a `.test-kubeconfig.yaml` file you can use for lens access, if you passed `--skip-cleanup` to pytest.

## Publishing / CI

After having successfully tested, there are gitlab pipelines for publishing to official registries (this section now is only relevant for maintainers). Please read the [Contributing Section](./contributing.md) and open a pr.

All projects come with gitlab ci pipelines that trigger into required downstream repos.

### Setup CI

* create `PYPI_TOKEN` and `DOCKER_AUTH_CONFIG_B64` gitlab ci variables for the pve-cloud repository group.

the docker auth variable can be formatted using this bash script:

```bash
TOKEN=
USERNAME= # docker hub username

AUTH=$(echo -n "$USERNAME:$TOKEN" | base64)

cat <<EOF | base64 -w 0
{
  "auths": {
    "https://index.docker.io/v1/": {
      "username": "$USERNAME",
      "password": "$TOKEN",
      "auth": "$AUTH"
    }
  }
}
EOF
```

* add `*.*.*` as protected tag pattern under Repository settings in gitlab for each repository with a pipeline.
* allow job ci tokens to make push changes to the repositories, CI/CD settings => Job token permissions => Allow git push

### Releasing

after having build and tested everything locally (using tdd e2e tests), commit all your changes and use the following tags as triggers for a release:

* `release-patch` / `release-minor` / `release-major` 

these tags are reused so we have to force push them for example `git tag -f release-patch && git push -f origin release-patch`.

these tags will release and update all dependant projects, update dependencies and trigger a release there aswell, meaning if you made changes to the pve_cloud collection and the py-pve-cloud package, it is enough push a release tag to the package.

