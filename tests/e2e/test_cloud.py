import asyncio
import logging
import os
import tempfile

import dns.query
import dns.rcode
import dns.resolver
import dns.tsigkeyring
import dns.update
import paramiko
import psycopg2
import pytest
import redis
import yaml
from fixtures import *
from pve_cloud.cli.pvclu import (get_ssh_master_kubeconfig,
                                 get_ssh_remote_master_kubeconfig)
from pve_cloud.cli.pxrpc import launch_pxrpc, launch_pxrpc_async
from pve_cloud.lib.inventory import (get_cloud_domain, get_cluster_vars,
                                     get_online_pve_host, get_pve_inventory,
                                     get_target_cluster)
from pve_cloud.lib.ssh import connect_host
from pve_cloud.orm.alchemy import AcmeX509
from pve_cloud_test.k8s_fixtures import (construct_k0s_ext_hosts_inv,
                                         get_e2e_limit_feature,
                                         get_kubespray_inv,
                                         get_secondary_kubespray_inv)
from pve_cloud_test.tdd_watchdog import get_ipv4
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


@pytest.mark.asyncio
async def test_pxrpc_tunnel(get_test_env):

    first_test_host = get_test_env["pve_test_cluster_hosts"][
        next(iter(get_test_env["pve_test_cluster_hosts"]))
    ]
    logger.info(first_test_host["ansible_host"])
    # run the remote connect cluster functionality if jumphost is specified, otherwise normal connect cluster
    if "pve_test_cluster_jump_host" in get_test_env:
        logger.info("initializing local ~/.pve-cloud-e2e-dyn-inv.yaml with jumphosts")

        with launch_pxrpc(
            get_test_env["pve_test_cluster_jump_host"],
            first_test_host["ansible_host"],
            init_venv=True,
            local_pypi_ip=get_tdd_ip(),
        ) as (pxrpc, pve_host):
            print("test sync", pxrpc.e2e_return())

        async with launch_pxrpc_async(
            get_test_env["pve_test_cluster_jump_host"], first_test_host["ansible_host"]
        ) as pxrpc:
            res = await pxrpc.e2e_return()
            print("test processpool", res)

            # test paralellism
            tasks = []
            for _ in range(5):
                tasks.append(pxrpc.e2e_return())

            await asyncio.gather(*tasks)

            logger.info(tasks)

        print("closed")


def test_control_node(setup_control_node):
    logger.info("test control node")
    # tested via fixture, add more tests here


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


def test_mirror_vm(setup_mirror_vm):
    logger.info("test mirror vm")


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
                + get_test_env["cloud_inventory"]["pve_cloud_domain"],
                "stack_name": "pytest-lxcs",
                "lxcs": [
                    {
                        "parameters": {
                            "rootfs": f"volume={get_test_env['pve_vm_storage_id']}:10",
                            "cores": 1,
                            "memory": 256,
                            "net0": f"name=pve,bridge=vmbr0,firewall=1,ip=dhcp"
                            + f"{get_test_env['net0_vlan_tag_rendered'] if 'net0_vlan_tag_rendered' in get_test_env else ''}",
                        }
                    },
                    {
                        "parameters": {
                            "rootfs": f"volume={get_test_env['pve_vm_storage_id']}:10",
                            "cores": 1,
                            "memory": 256,
                            "net0": f"name=pve,bridge=vmbr0,firewall=1,ip=dhcp"
                            + f"{get_test_env['net0_vlan_tag_rendered'] if 'net0_vlan_tag_rendered' in get_test_env else ''}",
                        }
                    },
                ],
                "target_pve_hosts": list(get_test_env["pve_test_cluster_hosts"].keys()),
                "root_ssh_pub_key": get_test_env["ssh_pub_key"],
            },
            temp_dyn_lxcs_inv,
        )
        temp_dyn_lxcs_inv.flush()

        with run_playbook(
            request,
            temp_dyn_lxcs_inv.name,
            "playbooks/sync_lxcs.yaml",
            "playbooks/get_blakes.yaml",
            destroy_playbook="playbooks/destroy_lxcs.yaml",
        ):

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
            resolver.nameservers = [get_test_env["cloud_inventory"]["bind_master_ip"]]

            ddns_answer = resolver.resolve(
                f"{test_lxc['name']}.{get_test_env['cloud_inventory']['pve_cloud_domain']}"
            )
            ddns_ips = [rdata.to_text() for rdata in ddns_answer]
            logger.info(ddns_ips)
            assert ddns_ips  # assert ddns response


def test_create_qemu(request, get_test_env, setup_mirror_vm):
    logger.info("test create dynamic qemu")

    with tempfile.NamedTemporaryFile(
        "w", suffix=".yaml", delete=False
    ) as temp_qemu_inv:
        yaml.dump(
            {
                "plugin": "pxc.cloud.qemu_inv",
                "target_pve": get_test_env["pve_test_cluster_name"]
                + "."
                + get_test_env["cloud_inventory"]["pve_cloud_domain"],
                "stack_name": "pytest-qemu",
                "qemu_base_parameters": {
                    "cpu": "host",
                    "net0": "virtio,bridge=vmbr0,firewall=1"
                    + f"{get_test_env['net0_vlan_tag_rendered'] if 'net0_vlan_tag_rendered' in get_test_env else ''}",
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
                        "zone": get_test_env["cloud_inventory"]["pve_cloud_domain"],
                        "names": ["mail-example", "other-service-example"],
                        "external": True,
                    }
                ],
                "static_includes": {
                    "dhcp_stack": "ha-dhcp."
                    + get_test_env["cloud_inventory"]["pve_cloud_domain"],
                    "proxy_stack": "ha-haproxy."
                    + get_test_env["cloud_inventory"]["pve_cloud_domain"],
                    "postgres_stack": "ha-postgres."
                    + get_test_env["cloud_inventory"]["pve_cloud_domain"],
                    "bind_stack": "ha-bind."
                    + get_test_env["cloud_inventory"]["pve_cloud_domain"],
                },
                "qemus": [
                    {
                        "hostname": "test-vm",
                        "disk": {
                            "size": "25G",
                            "options": {
                                "discard": "on",
                                "iothread": "on",
                                "ssd": "on",
                                "cache": "unsafe",
                            },
                            "pool": get_test_env["pve_vm_storage_id"],
                        },
                        "parameters": {
                            "cores": 2,
                            "memory": 1024,
                        },
                    },
                ],
                "target_pve_hosts": list(get_test_env["pve_test_cluster_hosts"].keys()),
                "root_ssh_pub_key": get_test_env["ssh_pub_key"],
            },
            temp_qemu_inv,
        )
        temp_qemu_inv.flush()

        with run_playbook(
            request,
            temp_qemu_inv.name,
            "playbooks/sync_qemus.yaml",
            "playbooks/get_blakes.yaml",
            destroy_playbook="playbooks/destroy_qemus.yaml",
        ):
            pass


def test_create_secondary_kubespray(
    request,
    get_test_env,
    get_secondary_kubespray_inv,
    setup_prepare_kubespray,
    setup_mirror_vm,
    get_cloud_secrets,
):
    extra_vars = {}
    tdd_ip = get_tdd_ip()
    if tdd_ip:
        extra_vars["test_repos_ip"] = tdd_ip

    with run_playbook(
        request,
        get_secondary_kubespray_inv,
        "playbooks/sync_kubespray.yaml",
        destroy_playbook="playbooks/destroy_kubespray.yaml",
        extra_vars=extra_vars,
    ):

        # set manual cp records (only for testing prod is manually manged)
        dns_update = dns.update.Update(
            get_test_env["kubernetes"]["deployments_domain"],
            keyring=dns.tsigkeyring.from_text(
                {"internal.": get_cloud_secrets["bind_internal_key"]}
            ),
            keyname="internal.",
            keyalgorithm="hmac-sha256",
        )

        # secondary k8s
        dns_update.replace(
            "cp-pytest-secondary",
            300,
            "A",
            get_test_env["pve_test_cluster_floating_external"],
        )
        response = dns.query.tcp(
            dns_update, get_test_env["cloud_inventory"]["bind_master_ip"]
        )
        logger.info(f"response code creating dns secondary {response.rcode()}")
        assert response.rcode() == 0

    # write kubeconfig if cleanup is skipped
    if request.config.getoption("--skip-cleanup"):

        # write kubeconfig if cleanup is skipped
        first_test_host = get_test_env["pve_test_cluster_hosts"][
            next(iter(get_test_env["pve_test_cluster_hosts"]))
        ]["ansible_host"]

        if "pve_test_cluster_jump_host" in get_test_env:
            with open(".test-secondary-kubeconfig.yaml", "w") as tk:
                tk.write(
                    get_ssh_remote_master_kubeconfig(
                        "pytest-secondary-k8s",
                        f"cp-pytest-secondary.{get_test_env["kubernetes"]["deployments_domain"]}",
                        get_test_env["pve_test_cluster_jump_host"],
                        first_test_host,
                    )
                )
        else:
            cluster_vars = get_cluster_vars(first_test_host)
            with open(".test-secondary-kubeconfig.yaml", "w") as tk:
                tk.write(
                    get_ssh_master_kubeconfig(cluster_vars, "pytest-secondary-k8s")
                )


def test_create_kubespray(
    request, get_test_env, get_kubespray_inv, setup_prepare_kubespray, get_cloud_secrets
):
    logger.info("create kubespray")

    # create custom kubespray vars for testing mem limits on worker
    k8s_cluster_vars_path = "/tmp/group_vars/kube_node.yaml"
    os.makedirs(os.path.dirname(k8s_cluster_vars_path), exist_ok=True)
    if os.path.exists(k8s_cluster_vars_path):
        os.remove(k8s_cluster_vars_path)

    # according to the kubernetes.md documentation
    yaml_content = """
kube_reserved: true
kube_reserved_cgroups_for_service_slice: kube.slice
kube_reserved_cgroups: "/{{ kube_reserved_cgroups_for_service_slice }}"
kube_memory_reserved: 256Mi

system_reserved: true
system_reserved_cgroups_for_service_slice: system.slice
system_reserved_cgroups: "/{{ system_reserved_cgroups_for_service_slice }}"
system_memory_reserved: 500Mi

eviction_hard:
  memory.available: 1Gi

"""

    with open(k8s_cluster_vars_path, "w") as file:
        file.write(yaml_content)

    extra_vars = {}
    tdd_ip = get_tdd_ip()
    if tdd_ip:
        extra_vars["test_repos_ip"] = tdd_ip

    with run_playbook(
        request,
        get_kubespray_inv,
        "playbooks/sync_kubespray.yaml",
        destroy_playbook="playbooks/destroy_kubespray.yaml",
        extra_vars=extra_vars,
    ):
        # set manual cp records (only for testing prod is manually manged)
        dns_update = dns.update.Update(
            get_test_env["kubernetes"]["deployments_domain"],
            keyring=dns.tsigkeyring.from_text(
                {"internal.": get_cloud_secrets["bind_internal_key"]}
            ),
            keyname="internal.",
            keyalgorithm="hmac-sha256",
        )

        # main k8s
        dns_update.replace(
            "cp-pytest",
            300,
            "A",
            get_test_env["pve_test_cluster_floating_external"],
        )
        response = dns.query.tcp(
            dns_update, get_test_env["cloud_inventory"]["bind_master_ip"]
        )
        logger.info(f"response code creating dns {response.rcode()}")
        assert response.rcode() == 0

        # always cleanup custom vars
        if os.path.exists(k8s_cluster_vars_path):
            os.remove(k8s_cluster_vars_path)

    if request.config.getoption("--skip-cleanup"):
        # write kubeconfig if cleanup is skipped
        first_test_host = get_test_env["pve_test_cluster_hosts"][
            next(iter(get_test_env["pve_test_cluster_hosts"]))
        ]["ansible_host"]

        if "pve_test_cluster_jump_host" in get_test_env:
            with open(".test-kubeconfig.yaml", "w") as tk:
                tk.write(
                    get_ssh_remote_master_kubeconfig(
                        "pytest-k8s",
                        f"cp-pytest.{get_test_env["kubernetes"]["deployments_domain"]}",
                        get_test_env["pve_test_cluster_jump_host"],
                        first_test_host,
                    )
                )
        else:
            cluster_vars = get_cluster_vars(first_test_host)
            with open(".test-kubeconfig.yaml", "w") as tk:
                tk.write(get_ssh_master_kubeconfig(cluster_vars, "pytest-k8s"))


def test_create_k0s_edge(request, get_test_env, setup_mirror_vm):
    logger.info("test create k0s edge")

    with tempfile.NamedTemporaryFile(
        "w", suffix=".yaml", delete=False
    ) as temp_qemu_inv:
        yaml.dump(
            {
                "plugin": "pxc.cloud.qemu_inv",
                "target_pve": get_test_env["pve_test_cluster_name"]
                + "."
                + get_test_env["cloud_inventory"]["pve_cloud_domain"],
                "stack_name": "pytest-k0s-edge",
                "qemu_base_parameters": {
                    "cpu": "host",
                    "net0": "virtio,bridge=vmbr0,firewall=1"
                    + f"{get_test_env['net0_vlan_tag_rendered'] if 'net0_vlan_tag_rendered' in get_test_env else ''}",
                    "sockets": 1,
                },
                "tcp_proxies": [],
                "ingress_domains": [],
                "static_includes": {
                    "dhcp_stack": "ha-dhcp."
                    + get_test_env["cloud_inventory"]["pve_cloud_domain"],
                    "proxy_stack": "ha-haproxy."
                    + get_test_env["cloud_inventory"]["pve_cloud_domain"],
                    "postgres_stack": "ha-postgres."
                    + get_test_env["cloud_inventory"]["pve_cloud_domain"],
                    "bind_stack": "ha-bind."
                    + get_test_env["cloud_inventory"]["pve_cloud_domain"],
                },
                "qemus": [
                    {
                        "hostname": "single",
                        "disk": {
                            "size": "75G",
                            "options": {
                                "discard": "on",
                                "iothread": "on",
                                "ssd": "on",
                                "cache": "unsafe",
                            },
                            "pool": get_test_env["pve_vm_storage_id"],
                        },
                        "additional_disks": [
                            {
                                "size": "50G",
                                "options": {
                                    "discard": "on",
                                    "iothread": "on",
                                    "ssd": "on",
                                    "cache": "unsafe",
                                },
                                "pool": get_test_env["pve_vm_storage_id"],
                            }
                        ],
                        "parameters": {
                            "cores": 2,
                            "memory": 2048,
                        },
                    },
                ],
                "target_pve_hosts": list(get_test_env["pve_test_cluster_hosts"].keys()),
                "root_ssh_pub_key": get_test_env["ssh_pub_key"],
            },
            temp_qemu_inv,
        )
        temp_qemu_inv.flush()

        with run_playbook(
            request,
            temp_qemu_inv.name,
            "playbooks/sync_qemus.yaml",
            destroy_playbook="playbooks/destroy_qemus.yaml",
        ):
            extra_vars = {}
            tdd_ip = get_tdd_ip()
            if tdd_ip:
                extra_vars["test_repos_ip"] = tdd_ip

            k0s_inv, k0s_host = construct_k0s_ext_hosts_inv(get_test_env)
            with run_playbook(
                request,
                k0s_inv,
                "playbooks/install_k0s_edge.yaml",
                extra_vars=extra_vars,
            ):

                if request.config.getoption("--skip-cleanup"):
                    with connect_host(k0s_host, user="admin") as ssh:
                        _, stdout, _ = ssh.exec_command("sudo k0s kubeconfig admin")

                        with open(".test-k0s-kubeconfig.yaml", "w") as tk:
                            tk.write(stdout.read().decode("utf-8"))
