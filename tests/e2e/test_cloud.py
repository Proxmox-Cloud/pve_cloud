import pytest
import ansible_runner
import os
import yaml
import tempfile
import logging
from cloud_fixture import *
import dns.resolver
import paramiko
from pve_cloud.cli.pvclu import get_ssh_master_kubeconfig
import redis
from pve_cloud_test.tdd_watchdog import get_ipv4


logger = logging.getLogger(__name__)


def test_pve_host_setup(setup_pve_hosts):
  logger.info("test pve hosts")
  # tested via fixture, add more tests here


def test_dhcp(setup_dhcp_lxcs):
  logger.info("test dhcp")
  # tested via fixture, add more tests here


def test_bind(setup_bind_lxcs):
  logger.info("test bind")
  # tested via fixture, add more tests here


def test_patroni(setup_patroni_lxcs):
  logger.info("test patroni")
  # tested via fixture, add more tests here


def test_haproxy(setup_haproxy_lxcs):
  logger.info("test haproxy")
  # tested via fixture, add more tests here


def test_cache(setup_cache_lxcs):
  logger.info("test cache")
  # tested via fixture, add more tests here


def test_create_lxc(request, get_proxmoxer, get_test_env, setup_haproxy_lxcs):
  logger.info("test create dynamic lxc")

  with tempfile.NamedTemporaryFile('w', suffix='.yaml', delete=False) as temp_dyn_lxcs_inv:
    yaml.dump({
      "plugin": "pve.cloud.lxc_inv",
      "target_pve": get_test_env["pve_test_cluster_name"] + "." + get_test_env["pve_test_cloud_domain"],
      "stack_name": "pytest-lxcs",
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
      ],
      "root_ssh_pub_key": get_test_env['pve_test_ssh_pub_key']
    }, temp_dyn_lxcs_inv)
    temp_dyn_lxcs_inv.flush()

    try:
      create_dyn_lxcs_run = ansible_runner.run(
        private_data_dir=os.getcwd(),
        playbook="playbooks/sync_lxcs.yaml",
        inventory=temp_dyn_lxcs_inv.name,
        verbosity=request.config.getoption("--ansible-verbosity")
      )

      # always run the destroy run
      assert create_dyn_lxcs_run.rc == 0

      # assert that the lxc was created and ddns works
      
      # search for one test lxc (we need to find teh random petname)
      test_lxc = None
      for node in get_proxmoxer.nodes.get():
        for lxc in get_proxmoxer.nodes(node["node"]).lxc.get():
          if "pytest-lxcs" in lxc["name"]:
            test_lxc = lxc

      assert test_lxc

      logger.info(test_lxc)

      resolver = dns.resolver.Resolver()
      resolver.nameservers = [get_test_env['pve_test_cloud_inv']['bind_master_ip']]

      ddns_answer = resolver.resolve(f"{test_lxc['name']}.{get_test_env['pve_test_cloud_domain']}")
      ddns_ips = [rdata.to_text() for rdata in ddns_answer]
      logger.info(ddns_ips)
      assert ddns_ips # assert ddns response

    finally:

      if not request.config.getoption("--skip-cleanup"):
        # always run the destroy
        destroy_lxcs_run = ansible_runner.run(
          private_data_dir=os.getcwd(),
          playbook="playbooks/destroy_lxcs.yaml",
          inventory=temp_dyn_lxcs_inv.name,
          verbosity=request.config.getoption("--ansible-verbosity")
        )
        assert destroy_lxcs_run.rc == 0


def test_create_qemu(request, get_test_env, setup_haproxy_lxcs):
  logger.info("test create dynamic qemu")

  with tempfile.NamedTemporaryFile('w', suffix='.yaml', delete=False) as temp_qemu_inv:
    yaml.dump({
      "plugin": "pve.cloud.qemu_inv",

      "target_pve": get_test_env["pve_test_cluster_name"] + "." + get_test_env["pve_test_cloud_domain"],
      "stack_name": "pytest-qemu",
      "qemu_base_parameters": {
        "cpu": "x86-64-v2-AES",
        "net0": "virtio,bridge=vmbr0,firewall=1",
        "sockets": 1
      },
      "qemus": [
        { 
          "hostname": "test-vm",
          "disk": {
            "size": "25G",
            "options": {
              "discard": "on",
              "iothread": "on",
              "ssd": "on"
            },
            "pool": get_test_env["pve_test_disk_storage_id"]
          },
          "parameters" : {
            "cores": 4,
            "memory": 4096,
          }
        },
      ],
      "root_ssh_pub_key": get_test_env['pve_test_ssh_pub_key']
    }, temp_qemu_inv)
    temp_qemu_inv.flush()

    qemu_run = ansible_runner.run(
      private_data_dir=os.getcwd(),
      playbook="playbooks/sync_qemus.yaml",
      inventory=temp_qemu_inv.name,
      verbosity=request.config.getoption("--ansible-verbosity")
    )

    assert qemu_run.rc == 0

    if not request.config.getoption("--skip-cleanup"):
      qemu_destroy_run = ansible_runner.run(
        private_data_dir=os.getcwd(),
        playbook="playbooks/destroy_qemus.yaml",
        inventory=temp_qemu_inv.name,
        verbosity=request.config.getoption("--ansible-verbosity")
      )
      assert qemu_destroy_run.rc == 0


def test_create_kubespray(request, get_test_env, setup_haproxy_lxcs, setup_cache_lxcs):
  logger.info("create kubespray")
  
  with tempfile.NamedTemporaryFile('w', suffix='.yaml', delete=False) as temp_kubespray_inv:
    yaml.dump({
      "plugin": "pve.cloud.kubespray_inv",
      "target_pve": get_test_env["pve_test_cluster_name"] + "." + get_test_env["pve_test_cloud_domain"],
      "extra_control_plane_sans": [
        "control-plane.external.example.com"
      ],
      "stack_name": "pytest-k8s",
      "static_includes": {
        "dhcp_stack": "ha-dhcp." + get_test_env["pve_test_cloud_domain"],
        "proxy_stack": "ha-haproxy." + get_test_env["pve_test_cloud_domain"],
        "bind_stack": "ha-bind." + get_test_env["pve_test_cloud_domain"],
        "postgres_stack": "ha-postgres." + get_test_env["pve_test_cloud_domain"],
        "cache_stack": "cloud-cache." + get_test_env["pve_test_cloud_domain"],
      },
      "tcp_proxies": [],
      "external_domains": [],
      "cluster_cert_entries": [
        {
          "zone": get_test_env["pve_test_deployments_domain"],
          "authoritative_zone": True,
          "names": ["*"]
        }
      ],
      "ceph_csi_sc_pools": [
        {
          "name": get_test_env["pve_test_ceph_csi_storage_id"],
          "default": True,
          "mount_options": [ "discard" ]
        }
      ],
      "qemu_base_parameters": {
        "cpu": "x86-64-v2-AES",
        "net0": "virtio,bridge=vmbr0,firewall=1",
        "sockets": 1
      },
      "qemus": [
        { 
          "k8s_roles": [ "master" ],
          "disk": {
            "size": "25G",
            "options": {
              "discard": "on",
              "iothread": "on",
              "ssd": "on"
            },
            "pool": get_test_env["pve_test_disk_storage_id"]
          },
          "parameters" : {
            "cores": 4,
            "memory": 4096,
          }
        },
        { 
          "k8s_roles": [ "worker" ],
          "disk": {
            "size": "25G",
            "options": {
              "discard": "on",
              "iothread": "on",
              "ssd": "on"
            },
            "pool": get_test_env["pve_test_disk_storage_id"]
          },
          "parameters" : {
            "cores": 4,
            "memory": 8192,
          }
        },
      ],
      "root_ssh_pub_key": get_test_env['pve_test_ssh_pub_key']
    }, temp_kubespray_inv)
    temp_kubespray_inv.flush()

    # for local tdd with development watchdogs
    extra_vars = {}
    if os.getenv("TDDOG_LOCAL_IFACE"):
      extra_vars["test_repos_ip"] = get_ipv4(os.getenv("TDDOG_LOCAL_IFACE"))

    kubespray_run = ansible_runner.run(
      private_data_dir=os.getcwd(),
      playbook="playbooks/sync_kubespray.yaml",
      inventory=temp_kubespray_inv.name,
      verbosity=request.config.getoption("--ansible-verbosity"),
      extravars=extra_vars
    )

    assert kubespray_run.rc == 0

    if not request.config.getoption("--skip-cleanup"):
      kubespray_destroy_run = ansible_runner.run(
        private_data_dir=os.getcwd(),
        playbook="playbooks/destroy_kubespray.yaml",
        inventory=temp_kubespray_inv.name,
        verbosity=request.config.getoption("--ansible-verbosity")
      )
      assert kubespray_destroy_run.rc == 0
    else:
      # write the local kubeconfig for developer access
      first_host = list(get_test_env["pve_test_hosts"].keys())[0]

      # connect to the first pve host in the dyn inv, assumes they are all online
      ssh = paramiko.SSHClient()
      ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
      ssh.connect(get_test_env["pve_test_hosts"][first_host]["ansible_host"], username="root")

      # since we need root we cant use sftp and root via ssh is disabled
      _, stdout, _ = ssh.exec_command("cat /etc/pve/cloud/cluster_vars.yaml")

      cluster_vars = yaml.safe_load(stdout.read().decode('utf-8'))

      with open(".test-kubeconfig.yaml", "w") as tk:
        tk.write(get_ssh_master_kubeconfig(cluster_vars, "pytest-k8s"))



def test_create_backup_lxc(request, get_proxmoxer, get_test_env, setup_haproxy_lxcs):
  logger.info("test create backup lxc")

  with tempfile.NamedTemporaryFile('w', suffix='.yaml', delete=False) as temp_dyn_lxcs_inv:
    yaml.dump({
      "plugin": "pve.cloud.lxc_inv",

      "target_pve": get_test_env["pve_test_cluster_name"] + "." + get_test_env["pve_test_cloud_domain"],
      "stack_name": "pytest-backup-lxc",
      "lxcs": [
        {
          "hostname": "main",
          "parameters" : {
            "rootfs": f"volume={get_test_env["pve_test_disk_storage_id"]}:10",
            "cores": 2,
            "memory": 1024,
            "net0": f"name=pve,bridge=vmbr0,firewall=1,ip=dhcp",
            "mp0": f"volume={get_test_env["pve_test_disk_storage_id"]}:20,mp=/mnt/backup-drive"
          },
          "vars": {
            "BACKUP_BASE_DIR": "/mnt/backup-drive"
          }
        }
      ],
      "lxc_global_vars": {
        "install_prom_systemd_exporter": True
      },
      "root_ssh_pub_key": get_test_env['pve_test_ssh_pub_key']
    }, temp_dyn_lxcs_inv)
    temp_dyn_lxcs_inv.flush()

    try:
      create_lxc_run = ansible_runner.run(
        private_data_dir=os.getcwd(),
        playbook="playbooks/sync_lxcs.yaml",
        inventory=temp_dyn_lxcs_inv.name,
        verbosity=request.config.getoption("--ansible-verbosity")
      )

      assert create_lxc_run.rc == 0

      # for local tdd with development watchdogs
      extra_vars = {}
      if os.getenv("TDDOG_LOCAL_IFACE"):
        # get version for image from redis
        r = redis.Redis(host='localhost', port=6379, db=0)
        local_build_backup_version = r.get("version.pve-cloud-backup").decode()

        if local_build_backup_version:
          logger.info(f"found local version {local_build_backup_version}")
          extra_vars["tdd_local_pypi_host"] = get_ipv4(os.getenv("TDDOG_LOCAL_IFACE"))
          extra_vars["py_pve_cloud_backup_version"] = local_build_backup_version
        else:
          logger.warning(f"did not find local build pve cloud build version even though TDDOG_LOCAL_IFACE env var is defined")

      setup_bdd_run = ansible_runner.run(
        private_data_dir=os.getcwd(),
        playbook="playbooks/setup_backup_daemon.yaml",
        inventory=temp_dyn_lxcs_inv.name,
        verbosity=request.config.getoption("--ansible-verbosity"),
        extravars=extra_vars
      )

      assert setup_bdd_run.rc == 0

    finally:
      if not request.config.getoption("--skip-cleanup"):
        # always run the destroy
        destroy_lxcs_run = ansible_runner.run(
          private_data_dir=os.getcwd(),
          playbook="playbooks/destroy_lxcs.yaml",
          inventory=temp_dyn_lxcs_inv.name,
          verbosity=request.config.getoption("--ansible-verbosity")
        )
        assert destroy_lxcs_run.rc == 0
