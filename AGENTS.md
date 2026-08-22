# Agent Instructions

## Creating Ansible Roles

Creating roles should always be done using `ansible-galaxy init ROLE_NAME` inside the `roles/` directory of this collection:

```bash
cd roles
ansible-galaxy init ROLE_NAME
```

Do not create role directories or their structure manually.

## Testing (E2E)

`tests/e2e/fixtures.py` defines session-scoped **cloud fixtures** (`@cloud_fixture(*tags)` from `pve_cloud_test.cloud_fixtures`). Each fixture creates one stack of the test cloud and forms a strict dependency chain:

```
setup_control_node -> setup_pve_hosts -> setup_bind_lxcs -> setup_dhcp_lxcs
  -> setup_ceph_dhcp_lxcs (conditional)
  -> setup_patroni_lxcs -> setup_haproxy_lxcs
       -> setup_prepare_kubespray
       -> setup_mirror_vm -> setup_k0s_ext_vm
```

`--fixture-tags a,b` executes only fixtures whose tags intersect a,b; all other cloud fixtures in the chain are skipped as no-ops (their deps stay satisfied). `--skip-fixture-tags` is the inverse, `--skip-fixtures` skips all fixtures (re-run tests against already deployed state). `--skip-cleanup` keeps the created infra (skips `destroy_*.yaml` teardown). `--runner-tags`/`--skip-runner-tags` pass ansible `--tags`/`--skip-tags` into every playbook run.

### Fixtures, tags, and playbooks

| Fixture | Tags | Playbooks executed | Covers |
|---|---|---|---|
| `setup_control_node` | `localhost`, `control-node` | `setup_control_node.yaml` + `pvcli connect-cluster` / `connect-remote-cluster` | control node setup, init of local dyn inventory `~/.pve-cloud-e2e-dyn-inv.yaml` |
| `setup_pve_hosts` | `hosts`, `pve` | `setup_pve_clusters.yaml` | PVE cluster host setup (cloud services, ceph, floating IPs) |
| `setup_bind_lxcs` | `bind`, `dns` | `sync_lxcs.yaml`, `setup_bind.yaml` (destroy: `destroy_lxcs.yaml`) | HA bind DNS stack (master + failover LXC, stack `ha-bind`) |
| `setup_dhcp_lxcs` | `dhcp`, `kea` | `sync_lxcs.yaml`, `setup_kea.yaml` | HA kea DHCP stack (main + failover, stack `ha-dhcp`) |
| `setup_ceph_dhcp_lxcs` | `dhcp`, `ceph`, `kea` | `sync_lxcs.yaml`, `setup_ceph_kea.yaml` | ceph frontend DHCP (only when `pve_ceph_frontend_dhcp_iface` is in test env) |
| `setup_patroni_lxcs` | `patroni`, `postgres` | `sync_lxcs.yaml`, `setup_postgres.yaml` | 3-node patroni postgres stack (`ha-postgres`) |
| `setup_haproxy_lxcs` | `haproxy`, `proxy` | `sync_lxcs.yaml`, `setup_haproxy.yaml` | HA haproxy + keepalived floating IP (`ha-haproxy`) |
| `setup_prepare_kubespray` | `kubespray`, `k8s` | none (no playbook) | copies k8s ACME cert + harbor mirror creds from the reference cloud into test cloud DB |
| `setup_mirror_vm` | `mirror` | `sync_qemus.yaml`, `setup_mirror_vm.yaml` (destroy: `destroy_qemus.yaml`) | aptly mirror QEMU (`pytest-mirror-vm`) used as local mirror for VM/LXC installs |
| `setup_k0s_ext_vm` | `k0s` | `sync_qemus.yaml` (destroy: `destroy_qemus.yaml`) | k0s edge QEMU (`pytest-k0s-edge`) with local zfs + backup disks |

### Tests and required fixture tags

`tests/e2e/test_cloud.py` — pick the fixture tags matching the stack you changed so unrelated (already deployed) stacks are skipped:

| Test | Fixture tags to pass | What it validates |
|---|---|---|
| `test_pxrpc_tunnel` | none (only `get_test_env`) | pxrpc tunnel launch: sync, async, and parallel calls |
| `test_control_node` | `control-node` (or `localhost`) | control node setup playbook + dyn inventory init |
| `test_pve_host_setup` | `pve` (or `hosts`) | `setup_pve_clusters.yaml` |
| `test_bind` | `bind` (or `dns`) | bind stack creation |
| `test_dhcp` | `dhcp` (runs kea + ceph-kea variants) | kea DHCP stack creation |
| `test_patroni` | `postgres` (or `patroni`) | patroni postgres stack |
| `test_haproxy` | `haproxy` (or `proxy`) | haproxy/keepalived stack |
| `test_mirror_vm` | `mirror` | mirror QEMU creation |
| `test_create_lxc` | `haproxy` | inline dynamic LXC stack `pytest-lxcs` via `sync_lxcs.yaml` + `get_blakes.yaml`; asserts creation + DDNS record in bind |
| `test_create_qemu` | `mirror` | inline dynamic QEMU stack `pytest-qemu` (tcp proxies + external ingress domains) via `sync_qemus.yaml` |
| `test_create_kubespray` | `k8s` (or `kubespray`) | full kubespray cluster `pytest-k8s` (master + worker, ceph CSI pool, tcp proxies, wildcard cert) via `sync_kubespray.yaml` (destroy: `destroy_kubespray.yaml`) |
| `test_create_secondary_kubespray` | `k8s` (or `kubespray`) | secondary cluster `pytest-secondary-k8s` with extra control-plane SAN via `sync_kubespray.yaml`; adds DNS cp record via TSIG |
| `test_create_k0s_edge` | `k0s` | edge k0s install on the external QEMU via `install_k0s_edge.yaml` using an `ext_hosts_inv` inventory |

### Example invocations

```bash
# bind/dns changes
pytest -s tests/e2e/test_cloud.py::test_bind --skip-cleanup --fixture-tags bind

# dhcp/kea changes (includes ceph dhcp variant if configured)
pytest -s tests/e2e/test_cloud.py::test_dhcp --skip-cleanup --fixture-tags dhcp

# patroni/postgres changes
pytest -s tests/e2e/test_cloud.py::test_patroni --skip-cleanup --fixture-tags postgres

# haproxy changes
pytest -s tests/e2e/test_cloud.py::test_haproxy --skip-cleanup --fixture-tags haproxy

# kubespray / k8s changes
pytest -s tests/e2e/test_cloud.py::test_create_kubespray --skip-cleanup --fixture-tags k8s

# k0s edge changes
pytest -s tests/e2e/test_cloud.py::test_create_k0s_edge --skip-cleanup --fixture-tags k0s

# re-run test logic only, against fully deployed infra
pytest -s tests/e2e/test_cloud.py::test_create_lxc --skip-cleanup --skip-fixtures
```
