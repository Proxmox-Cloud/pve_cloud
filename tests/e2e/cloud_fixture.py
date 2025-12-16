import pytest
import ansible_runner
import os
import yaml
import tempfile
import logging
from proxmoxer import ProxmoxAPI
import jsonschema
from pve_cloud_test.cloud_fixtures import *


logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def setup_pve_hosts(request, get_test_env):
  logger.info("setup cloud")
  
  # run the pve cluster setup on the test environment
  with tempfile.NamedTemporaryFile('w', suffix='.yaml', delete=False) as temp_cloud_inv:
    # write pve cloud inventory file for main pve cluster setup playbook
    yaml.dump({
      "plugin": "pxc.cloud.pve_cloud_inv",
      "pve_cloud_domain": get_test_env["pve_test_cloud_domain"],
      "pve_clusters": {
        get_test_env["pve_test_cluster_name"]: {
          "pve_unique_cloud_services": [
            "dns", "dhcp", "psql-state"
          ],
          "pve_host_vars" : get_test_env["pve_test_host_vars"] if "pve_test_host_vars" in get_test_env else {}
        } | get_test_env["pve_test_cloud_inv_cluster"]
      }
    } | get_test_env["pve_test_cloud_inv"], temp_cloud_inv)
    temp_cloud_inv.flush()

    if not request.config.getoption("--skip-fixture-init"):
      # run the main playbook
      logger.info("run pve cluster setup")
      setup_run = ansible_runner.run(
        project_dir=os.getcwd(),
        playbook="playbooks/setup_pve_clusters.yaml",
        inventory=temp_cloud_inv.name,
        verbosity=request.config.getoption("--ansible-verbosity")
      )

      assert setup_run.rc == 0

    yield

    if request.config.getoption("--skip-cleanup"):
      return

    logger.info("uninstall pve hosts")

    uninstall_run = ansible_runner.run(
      project_dir=os.getcwd(),
      playbook="playbooks/uninstall_pve_clusters.yaml",
      inventory=temp_cloud_inv.name,
      verbosity=request.config.getoption("--ansible-verbosity")
    )
    assert uninstall_run.rc == 0


@pytest.fixture(scope="session")
def setup_dhcp_lxcs(request, get_test_env, setup_pve_hosts):
  logger.info("setup dhcp")

  test_vm_subnet_mask = get_test_env['pve_test_cloud_inv']['pve_vm_subnet'].split('/')[1]

  with tempfile.NamedTemporaryFile('w', suffix='.yaml', delete=False) as temp_kea_lxcs_inv:
    logger.info("create kea lxcs")
    yaml.dump({
      "plugin": "pxc.cloud.lxc_inv",
      "target_pve": get_test_env["pve_test_cluster_name"] + "." + get_test_env["pve_test_cloud_domain"],
      "stack_name": "ha-dhcp",
      "lxcs": [
        {
          "hostname": "main",
          "parameters" : {
            "rootfs": f"volume={get_test_env["pve_test_disk_storage_id"]}:10",
            "cores": 1,
            "memory": 512,
            "net0": f"name=pve,bridge=vmbr0,firewall=1,ip={get_test_env['pve_test_cloud_inv']['kea_dhcp_main_ip']}/{test_vm_subnet_mask},gw={get_test_env['pve_test_service_lxcs_gateway']}",
            "nameserver": get_test_env['pve_test_service_lxcs_nameserver']
          },
          "vars": {
            "kea_dhcp_main": True
          }
        },
        {
          "hostname": "failover",
          "parameters" : {
            "rootfs": f"volume={get_test_env["pve_test_disk_storage_id"]}:10",
            "cores": 1,
            "memory": 512,
            "net0": f"name=pve,bridge=vmbr0,firewall=1,ip={get_test_env['pve_test_cloud_inv']['kea_dhcp_failover_ip']}/{test_vm_subnet_mask},gw={get_test_env['pve_test_service_lxcs_gateway']}",
            "nameserver": get_test_env['pve_test_service_lxcs_nameserver']
          },
          "vars": {
            "kea_dhcp_main": False
          }
        }
      ],
      "lxc_global_vars": {
        "install_prom_systemd_exporter": True
      },
      "lxc_base_parameters": {
        "onboot": 1
      },
      "target_pve_hosts": list(get_test_env["pve_test_hosts"].keys()),
      "root_ssh_pub_key": get_test_env['pve_test_ssh_pub_key']
    }, temp_kea_lxcs_inv)
    temp_kea_lxcs_inv.flush()

    if not request.config.getoption("--skip-fixture-init"):
      sync_lxcs_kea = ansible_runner.run(
        project_dir=os.getcwd(),
        playbook="playbooks/sync_lxcs.yaml",
        inventory=temp_kea_lxcs_inv.name,
        verbosity=request.config.getoption("--ansible-verbosity")
      )
      assert sync_lxcs_kea.rc == 0

      logger.info("setup kea lxcs")
      setup_kea_run = ansible_runner.run(
        project_dir=os.getcwd(),
        playbook="playbooks/setup_kea.yaml",
        inventory=temp_kea_lxcs_inv.name,
        verbosity=request.config.getoption("--ansible-verbosity")
      )
      assert setup_kea_run.rc == 0

    yield
    
    if request.config.getoption("--skip-cleanup"):
      return # otherwise destroy the dhcp again
    
    logger.info("destroy kea lxcs")
    destroy_kea_lxcs_run = ansible_runner.run(
      project_dir=os.getcwd(),
      playbook="playbooks/destroy_lxcs.yaml",
      inventory=temp_kea_lxcs_inv.name,
      verbosity=request.config.getoption("--ansible-verbosity")
    )
    assert destroy_kea_lxcs_run.rc == 0


@pytest.fixture(scope="session")
def setup_bind_lxcs(request, get_test_env, setup_dhcp_lxcs):
  logger.info("setup bind")

  test_vm_subnet_mask = get_test_env['pve_test_cloud_inv']['pve_vm_subnet'].split('/')[1]

  with tempfile.NamedTemporaryFile('w', suffix='.yaml', delete=False) as temp_bind_lxcs_inv:
    logger.info("create bind lxcs")
    yaml.dump({
      "plugin": "pxc.cloud.lxc_inv",
      "target_pve": get_test_env["pve_test_cluster_name"] + "." + get_test_env["pve_test_cloud_domain"],
      "stack_name": "ha-bind",
      "lxcs": [
        {
          "hostname": "master",
          "parameters" : {
            "rootfs": f"volume={get_test_env["pve_test_disk_storage_id"]}:10",
            "cores": 1,
            "memory": 512,
            "net0": f"name=pve,bridge=vmbr0,firewall=1,ip={get_test_env['pve_test_cloud_inv']['bind_master_ip']}/{test_vm_subnet_mask},gw={get_test_env['pve_test_service_lxcs_gateway']}",
            "nameserver": get_test_env['pve_test_service_lxcs_nameserver']
          },
          "vars": {
            "bind_master": True
          }
        },
        {
          "hostname": "failover",
          "parameters" : {
            "rootfs": f"volume={get_test_env["pve_test_disk_storage_id"]}:10",
            "cores": 1,
            "memory": 512,
            "net0": f"name=pve,bridge=vmbr0,firewall=1,ip={get_test_env['pve_test_cloud_inv']['bind_slave_ip']}/{test_vm_subnet_mask},gw={get_test_env['pve_test_service_lxcs_gateway']}",
            "nameserver": get_test_env['pve_test_service_lxcs_nameserver']
          },
          "vars": {
            "bind_master": False
          }
        }
      ],
      "lxc_global_vars": {
        "install_prom_systemd_exporter": True
      },
      "lxc_base_parameters": {
        "onboot": 1
      },
      "target_pve_hosts": list(get_test_env["pve_test_hosts"].keys()),
      "root_ssh_pub_key": get_test_env['pve_test_ssh_pub_key']
    }, temp_bind_lxcs_inv)
    temp_bind_lxcs_inv.flush()

    if not request.config.getoption("--skip-fixture-init"):
      sync_bind_lxcs_run = ansible_runner.run(
        project_dir=os.getcwd(),
        playbook="playbooks/sync_lxcs.yaml",
        inventory=temp_bind_lxcs_inv.name,
        verbosity=request.config.getoption("--ansible-verbosity")
      )
      assert sync_bind_lxcs_run.rc == 0

      logger.info("setup bind lxcs")
      setup_bind_run = ansible_runner.run(
        project_dir=os.getcwd(),
        playbook="playbooks/setup_bind.yaml",
        inventory=temp_bind_lxcs_inv.name,
        verbosity=request.config.getoption("--ansible-verbosity")
      )
      assert setup_bind_run.rc == 0

    yield

    if request.config.getoption("--skip-cleanup"):
      return

    logger.info("destroy bind lxcs")
    destroy_bind_lxcs_run = ansible_runner.run(
      project_dir=os.getcwd(),
      playbook="playbooks/destroy_lxcs.yaml",
      inventory=temp_bind_lxcs_inv.name,
      verbosity=request.config.getoption("--ansible-verbosity")
    )
    assert destroy_bind_lxcs_run.rc == 0


@pytest.fixture(scope="session")
def setup_patroni_lxcs(request, get_test_env, setup_bind_lxcs):

  # next we deploy create core lxcs
  with tempfile.NamedTemporaryFile('w', suffix='.yaml', delete=False) as temp_postgres_lxcs_inv:

    logger.info("create patroni lxcs")
    yaml.dump({
      "plugin": "pxc.cloud.lxc_inv",
      "target_pve": get_test_env["pve_test_cluster_name"] + "." + get_test_env["pve_test_cloud_domain"],
      "stack_name": "ha-postgres",
      "lxcs": [
        {
          "parameters" : {
            "rootfs": f"volume={get_test_env["pve_test_disk_storage_id"]}:10",
            "cores": 1,
            "memory": 512,
            "net0": f"name=pve,bridge=vmbr0,firewall=1,ip=dhcp",
          }
        },
        {
          "parameters" : {
            "rootfs": f"volume={get_test_env["pve_test_disk_storage_id"]}:10",
            "cores": 1,
            "memory": 512,
            "net0": f"name=pve,bridge=vmbr0,firewall=1,ip=dhcp",
          }
        },
        {
          "parameters" : {
            "rootfs": f"volume={get_test_env["pve_test_disk_storage_id"]}:10",
            "cores": 1,
            "memory": 512,
            "net0": f"name=pve,bridge=vmbr0,firewall=1,ip=dhcp",
          }
        },
      ],
      "lxc_global_vars": {
        "install_prom_systemd_exporter": True
      },
      "target_pve_hosts": list(get_test_env["pve_test_hosts"].keys()),
      "root_ssh_pub_key": get_test_env['pve_test_ssh_pub_key']
    }, temp_postgres_lxcs_inv)
    temp_postgres_lxcs_inv.flush()

    if not request.config.getoption("--skip-fixture-init"):
      sync_lxcs_postgres = ansible_runner.run(
        project_dir=os.getcwd(),
        playbook="playbooks/sync_lxcs.yaml",
        inventory=temp_postgres_lxcs_inv.name,
        verbosity=request.config.getoption("--ansible-verbosity")
      )
      assert sync_lxcs_postgres.rc == 0

      logger.info("setup postgres lxcs")
      setup_postgres_run = ansible_runner.run(
        project_dir=os.getcwd(),
        playbook="playbooks/setup_postgres.yaml",
        inventory=temp_postgres_lxcs_inv.name,
        verbosity=request.config.getoption("--ansible-verbosity")
      )
      assert setup_postgres_run.rc == 0

    yield

    if request.config.getoption("--skip-cleanup"):
      return
    
    logger.info("destroy postgres lxcs")
    destroy_postgres_lxcs_run = ansible_runner.run(
      project_dir=os.getcwd(),
      playbook="playbooks/destroy_lxcs.yaml",
      inventory=temp_postgres_lxcs_inv.name,
      verbosity=request.config.getoption("--ansible-verbosity")
    )
    assert destroy_postgres_lxcs_run.rc == 0


@pytest.fixture(scope="session")
def setup_haproxy_lxcs(request, get_test_env, setup_patroni_lxcs):

 # next we deploy create core lxcs
  with tempfile.NamedTemporaryFile('w', suffix='.yaml', delete=False) as temp_haproxy_lxcs_inv:

    # haproxy
    logger.info("create haproxy lxcs")
    yaml.dump({
      "plugin": "pxc.cloud.lxc_inv",
      "target_pve": get_test_env["pve_test_cluster_name"] + "." + get_test_env["pve_test_cloud_domain"],
      "stack_name": "ha-haproxy",
      "static_includes": {
        "postgres_stack": "ha-postgres." + get_test_env["pve_test_cloud_domain"],
      },
      "lxcs": [
        {
          "hostname": "master",
          "parameters" : {
            "rootfs": f"volume={get_test_env["pve_test_disk_storage_id"]}:10",
            "cores": 1,
            "memory": 512,
            # todo: schema ext fix iface name
            "net0": f"name=eth0,bridge=vmbr0,firewall=1,ip=dhcp",
          },
          "vars": {
            "keepalived_master": True
          }
        },
        {
          "hostname": "failover",
          "parameters" : {
            "rootfs": f"volume={get_test_env["pve_test_disk_storage_id"]}:10",
            "cores": 1,
            "memory": 512,
            "net0": f"name=eth0,bridge=vmbr0,firewall=1,ip=dhcp",
          },
          "vars": {
            "keepalived_master": False
          }
        },
      ],
      "lxc_global_vars": {
        "auto_http_redirect": False, # allow https for testing#
        "install_prom_systemd_exporter": True
      },
      "target_pve_hosts": list(get_test_env["pve_test_hosts"].keys()),
      "root_ssh_pub_key": get_test_env['pve_test_ssh_pub_key']
    }, temp_haproxy_lxcs_inv)
    temp_haproxy_lxcs_inv.flush()

    if not request.config.getoption("--skip-fixture-init"):
      sync_lxcs_haproxy = ansible_runner.run(
        project_dir=os.getcwd(),
        playbook="playbooks/sync_lxcs.yaml",
        inventory=temp_haproxy_lxcs_inv.name,
        verbosity=request.config.getoption("--ansible-verbosity")
      )
      assert sync_lxcs_haproxy.rc == 0

      logger.info("setup haproxy lxcs")
      setup_haproxy_run = ansible_runner.run(
        project_dir=os.getcwd(),
        playbook="playbooks/setup_haproxy.yaml",
        inventory=temp_haproxy_lxcs_inv.name,
        verbosity=request.config.getoption("--ansible-verbosity")
      )
      assert setup_haproxy_run.rc == 0

    yield

    if request.config.getoption("--skip-cleanup"):
      return
    
    logger.info("destroy haproxy lxcs")
    destroy_haproxy_lxcs_run = ansible_runner.run(
      project_dir=os.getcwd(),
      playbook="playbooks/destroy_lxcs.yaml",
      inventory=temp_haproxy_lxcs_inv.name,
      verbosity=request.config.getoption("--ansible-verbosity")
    )
    assert destroy_haproxy_lxcs_run.rc == 0



@pytest.fixture(scope="session")
def setup_cache_lxcs(request, get_test_env, setup_bind_lxcs):

  # next we deploy create core lxcs
  with tempfile.NamedTemporaryFile('w', suffix='.yaml', delete=False) as temp_cache_lxcs_inv:
    # cache
    logger.info("create cache lxc")
    yaml.dump({
      "plugin": "pxc.cloud.lxc_inv",

      "target_pve": get_test_env["pve_test_cluster_name"] + "." + get_test_env["pve_test_cloud_domain"],
      "stack_name": "cloud-cache",
      "lxcs": [
        {
          "hostname": "main",
          "parameters" : {
            "rootfs": f"volume={get_test_env["pve_test_disk_storage_id"]}:200",
            "cores": 2,
            "memory": 1024,
            "net0": f"name=eth0,bridge=vmbr0,firewall=1,ip=dhcp",
            # mount perms for nfs and future docker
            # todo: put into schema
            "features": "nesting=1",
            "unprivileged": 0
          }
        },
      ],
      "target_pve_hosts": list(get_test_env["pve_test_hosts"].keys()),
      "root_ssh_pub_key": get_test_env['pve_test_ssh_pub_key']
    }, temp_cache_lxcs_inv)
    temp_cache_lxcs_inv.flush()

    if not request.config.getoption("--skip-fixture-init"):
      sync_lxcs = ansible_runner.run(
        project_dir=os.getcwd(),
        playbook="playbooks/sync_lxcs.yaml",
        inventory=temp_cache_lxcs_inv.name,
        verbosity=request.config.getoption("--ansible-verbosity")
      )
      assert sync_lxcs.rc == 0

      logger.info("setup cache lxcs")
      setup_run = ansible_runner.run(
        project_dir=os.getcwd(),
        playbook="playbooks/setup_cloud_cache.yaml",
        inventory=temp_cache_lxcs_inv.name,
        verbosity=request.config.getoption("--ansible-verbosity")
      )
      assert setup_run.rc == 0

    yield

    if request.config.getoption("--skip-cleanup"):
      return
    
    logger.info("destroy cache lxcs")
    destroy_lxcs_run = ansible_runner.run(
      project_dir=os.getcwd(),
      playbook="playbooks/destroy_lxcs.yaml",
      inventory=temp_cache_lxcs_inv.name,
      verbosity=request.config.getoption("--ansible-verbosity")
    )
    assert destroy_lxcs_run.rc == 0

