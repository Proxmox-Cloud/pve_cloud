import logging
import os
import tempfile

import ansible_runner
import dns.resolver
import paramiko
import psycopg2
import pytest
import redis
import yaml
from cloud_fixture import *
from pve_cloud.cli.pvclu import get_ssh_master_kubeconfig
from pve_cloud.lib.inventory import get_online_pve_host
from pve_cloud.orm.alchemy import AcmeX509
from pve_cloud_test.tdd_watchdog import get_ipv4
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

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

    with tempfile.NamedTemporaryFile(
        "w", suffix=".yaml", delete=False
    ) as temp_dyn_lxcs_inv:
        yaml.dump(
            {
                "plugin": "pxc.cloud.lxc_inv",
                "target_pve": get_test_env["pve_test_cluster_name"]
                + "."
                + get_test_env["pve_test_cloud_domain"],
                "stack_name": "pytest-lxcs",
                "lxcs": [
                    {
                        "parameters": {
                            "rootfs": f"volume={get_test_env["pve_test_disk_storage_id"]}:10",
                            "cores": 1,
                            "memory": 512,
                            "net0": f"name=pve,bridge=vmbr0,firewall=1,ip=dhcp",
                        }
                    },
                    {
                        "parameters": {
                            "rootfs": f"volume={get_test_env["pve_test_disk_storage_id"]}:10",
                            "cores": 1,
                            "memory": 512,
                            "net0": f"name=pve,bridge=vmbr0,firewall=1,ip=dhcp",
                        }
                    },
                ],
                "target_pve_hosts": list(get_test_env["pve_test_hosts"].keys()),
                "root_ssh_pub_key": get_test_env["pve_test_ssh_pub_key"],
            },
            temp_dyn_lxcs_inv,
        )
        temp_dyn_lxcs_inv.flush()

        try:
            create_dyn_lxcs_run = ansible_runner.run(
                project_dir=os.getcwd(),
                playbook="playbooks/sync_lxcs.yaml",
                inventory=temp_dyn_lxcs_inv.name,
                verbosity=request.config.getoption("--ansible-verbosity"),
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
            resolver.nameservers = [
                get_test_env["pve_test_cloud_inv"]["bind_master_ip"]
            ]

            ddns_answer = resolver.resolve(
                f"{test_lxc['name']}.{get_test_env['pve_test_cloud_domain']}"
            )
            ddns_ips = [rdata.to_text() for rdata in ddns_answer]
            logger.info(ddns_ips)
            assert ddns_ips  # assert ddns response

        finally:

            if not request.config.getoption("--skip-cleanup"):
                # always run the destroy
                destroy_lxcs_run = ansible_runner.run(
                    project_dir=os.getcwd(),
                    playbook="playbooks/destroy_lxcs.yaml",
                    inventory=temp_dyn_lxcs_inv.name,
                    verbosity=request.config.getoption("--ansible-verbosity"),
                )
                assert destroy_lxcs_run.rc == 0


def test_create_qemu(request, get_test_env, setup_haproxy_lxcs):
    logger.info("test create dynamic qemu")

    with tempfile.NamedTemporaryFile(
        "w", suffix=".yaml", delete=False
    ) as temp_qemu_inv:
        yaml.dump(
            {
                "plugin": "pxc.cloud.qemu_inv",
                "target_pve": get_test_env["pve_test_cluster_name"]
                + "."
                + get_test_env["pve_test_cloud_domain"],
                "stack_name": "pytest-qemu",
                "qemu_base_parameters": {
                    "cpu": "x86-64-v2-AES",
                    "net0": "virtio,bridge=vmbr0,firewall=1",
                    "sockets": 1,
                },
                "tcp_proxies": [
                    {
                        "proxy_name": "vm-tcp-test",
                        "haproxy_port": 7432,
                        "node_port": 5432,
                        "external": True,
                    }
                ],
                "ingress_domains": [
                    {
                        "zone": get_test_env["pve_test_deployments_domain"],
                        "names": ["mail-example", "other-service-example"],
                        "external": True,
                    }
                ],
                "static_includes": {
                    "dhcp_stack": "ha-dhcp." + get_test_env["pve_test_cloud_domain"],
                    "proxy_stack": "ha-haproxy."
                    + get_test_env["pve_test_cloud_domain"],
                    "postgres_stack": "ha-postgres."
                    + get_test_env["pve_test_cloud_domain"],
                    "bind_stack": "ha-bind." + get_test_env["pve_test_cloud_domain"],
                },
                "qemus": [
                    {
                        "hostname": "test-vm",
                        "disk": {
                            "size": "25G",
                            "options": {"discard": "on", "iothread": "on", "ssd": "on"},
                            "pool": get_test_env["pve_test_disk_storage_id"],
                        },
                        "parameters": {
                            "cores": 4,
                            "memory": 4096,
                        },
                    },
                ],
                "target_pve_hosts": list(get_test_env["pve_test_hosts"].keys()),
                "root_ssh_pub_key": get_test_env["pve_test_ssh_pub_key"],
            },
            temp_qemu_inv,
        )
        temp_qemu_inv.flush()

        qemu_run = ansible_runner.run(
            project_dir=os.getcwd(),
            playbook="playbooks/sync_qemus.yaml",
            inventory=temp_qemu_inv.name,
            verbosity=request.config.getoption("--ansible-verbosity"),
        )

        assert qemu_run.rc == 0

        if not request.config.getoption("--skip-cleanup"):
            qemu_destroy_run = ansible_runner.run(
                project_dir=os.getcwd(),
                playbook="playbooks/destroy_qemus.yaml",
                inventory=temp_qemu_inv.name,
                verbosity=request.config.getoption("--ansible-verbosity"),
            )
            assert qemu_destroy_run.rc == 0


def test_create_kubespray(
    request, get_test_env, get_kubespray_inv, setup_haproxy_lxcs, setup_cache_lxcs
):
    logger.info("create kubespray")

    # first we check if the pve_test_k8s_tls_copy_fqdn is specified.
    # in this case we copy an existing prod cert
    if (
        "pve_test_k8s_tls_copy_target_pve" in get_test_env
        and "pve_test_k8s_tls_copy_stack_name" in get_test_env
    ):
        pve_host = get_online_pve_host(get_test_env["pve_test_k8s_tls_copy_target_pve"])
        logger.info(pve_host)

        # we connect to the test host to get the patroni secret of the cluster, aswell as the vars
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            pve_host,
            username="root",
        )

        # since we need root we cant use sftp and root via ssh is disabled
        _, stdout, _ = ssh.exec_command("cat /etc/pve/cloud/cluster_vars.yaml")

        cluster_vars = yaml.safe_load(stdout.read().decode("utf-8"))

        _, stdout, _ = ssh.exec_command("cat /etc/pve/cloud/secrets/patroni.pass")

        patroni_pass = stdout.read().decode("utf-8")
        logger.info(patroni_pass)

        conn = psycopg2.connect(
            dbname="pve_cloud",
            user="postgres",
            password=patroni_pass,
            host=cluster_vars["pve_haproxy_floating_ip_internal"],
            port=5000,
        )

        with conn.cursor() as cur:
            query = "SELECT k8s FROM acme_x509 WHERE stack_fqdn = %s;"

            cur.execute(
                query,
                (
                    f"{get_test_env["pve_test_k8s_tls_copy_stack_name"]}.{cluster_vars["pve_cloud_domain"]}",
                ),
            )
            record = cur.fetchone()

            assert record
            logger.info(record)

        # now we inject the record into our test patroni database
        first_test_host = get_test_env["pve_test_hosts"][
            next(iter(get_test_env["pve_test_hosts"]))
        ]

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(first_test_host["ansible_host"], username="root")

        _, stdout, _ = ssh.exec_command("sudo cat /etc/pve/cloud/secrets/patroni.pass")
        patroni_pass = stdout.read().decode("utf-8")

        pg_conn_str_orm = f"postgresql+psycopg2://postgres:{patroni_pass}@{get_test_env['pve_test_cloud_inv_cluster']['pve_haproxy_floating_ip_internal']}:5000/pve_cloud?sslmode=disable"

        engine = create_engine(pg_conn_str_orm)

        # update certs and mirror pull secret
        with Session(engine) as session:
            copy_cert = AcmeX509(
                stack_fqdn=f"pytest-k8s.{get_test_env["pve_test_cloud_domain"]}",
                config={},
                ec_csr={},
                ec_crt={},
                k8s=record[0],
            )
            session.merge(copy_cert)
            session.commit()

    # for local tdd with development watchdogs
    extra_vars = {}
    tdd_ip = get_tdd_ip()
    if tdd_ip:
        extra_vars["test_repos_ip"] = tdd_ip

    kubespray_run = ansible_runner.run(
        project_dir=os.getcwd(),
        playbook="playbooks/sync_kubespray.yaml",
        inventory=get_kubespray_inv,
        verbosity=request.config.getoption("--ansible-verbosity"),
        extravars=extra_vars,
    )

    assert kubespray_run.rc == 0

    if not request.config.getoption("--skip-cleanup"):
        kubespray_destroy_run = ansible_runner.run(
            project_dir=os.getcwd(),
            playbook="playbooks/destroy_kubespray.yaml",
            inventory=get_kubespray_inv,
            verbosity=request.config.getoption("--ansible-verbosity"),
        )
        assert kubespray_destroy_run.rc == 0
    else:
        # write the local kubeconfig for developer access
        first_host = list(list(get_test_env["pve_test_hosts"].keys()))[0]

        # connect to the first pve host in the dyn inv, assumes they are all online
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            get_test_env["pve_test_hosts"][first_host]["ansible_host"],
            username="root",
        )

        # since we need root we cant use sftp and root via ssh is disabled
        _, stdout, _ = ssh.exec_command("cat /etc/pve/cloud/cluster_vars.yaml")

        cluster_vars = yaml.safe_load(stdout.read().decode("utf-8"))

        with open(".test-kubeconfig.yaml", "w") as tk:
            tk.write(get_ssh_master_kubeconfig(cluster_vars, "pytest-k8s"))
