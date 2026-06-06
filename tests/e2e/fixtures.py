import json
import logging
import os
import re
import subprocess
import tempfile

import ansible_runner
import dns.query
import dns.rcode
import dns.resolver
import dns.tsigkeyring
import dns.update
import paramiko
import psycopg2
import pytest
import yaml
from pve_cloud.cli.pvcli import (connect_cluster, connect_remote_cluster,
                                 get_parser)
from pve_cloud.cli.pxrpc import launch_pxrpc
from pve_cloud.lib.inventory import (get_cloud_domain, get_online_pve_host,
                                     get_pve_inventory, get_target_cluster)
from pve_cloud.lib.ssh import connect_host
from pve_cloud.orm.alchemy import AcmeX509
from pve_cloud_test.cloud_fixtures import *
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


def fetch_default_gw_ns(test_env):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    pve_host = test_env["pve_test_cluster_hosts"][
        next(iter(test_env["pve_test_cluster_hosts"]))
    ]

    client.connect(pve_host["ansible_host"], username="root")

    _, stdout, _ = client.exec_command(
        "ip route show default 2>/dev/null | awk '{print $3}'"
    )
    gateway = stdout.read().decode("utf-8").strip()
    logger.info(gateway)

    _, stdout, _ = client.exec_command(
        "grep -E '^nameserver [0-9]+' /etc/resolv.conf 2>/dev/null | awk '{print $2}'"
    )
    nameservers = stdout.read().decode("utf-8").strip().splitlines()
    logger.info(nameservers)

    return gateway, " ".join(nameservers)


@cloud_fixture("localhost")
def setup_control_node(request, get_test_env):
    if not request.config.getoption("--skip-fixture-init"):
        # install galaxy requirements

        # dump them in installable format
        with open("galaxy.yml") as f:
            galaxy = yaml.safe_load(f)

        deps = galaxy.get("dependencies", {})

        req = {"collections": []}

        for name, version in deps.items():
            entry = {}
            entry["name"] = name
            entry["version"] = version

            req["collections"].append(entry)

        with open("tdd-requirements.yml", "w") as f:
            yaml.safe_dump(req, f, sort_keys=False)

        subprocess.run(
            ["ansible-galaxy", "install", "-r", "tdd-requirements.yml"],
            check=True,
        )

        extra_vars = {}
        tdd_ip = get_tdd_ip()
        if tdd_ip:
            extra_vars["test_repos_ip"] = tdd_ip

        # run the main playbook
        logger.info("run control node setup")
        setup_run = ansible_runner.run(
            project_dir=os.getcwd(),
            playbook="playbooks/setup_control_node.yaml",
            verbosity=request.config.getoption("--ansible-verbosity"),
            extravars=extra_vars,
        )

        assert setup_run.rc == 0
        first_test_host = get_test_env["pve_test_cluster_hosts"][
            next(iter(get_test_env["pve_test_cluster_hosts"]))
        ]

        # run the remote connect cluster functionality if jumphost is specified, otherwise normal connect cluster
        if "pve_test_cluster_jump_host" in get_test_env:
            logger.info("initializing local ~/.pve-cloud-dyn-inv.yaml with jumphosts")
            parsed_args = get_parser().parse_args(
                [
                    "connect-remote-cluster",
                    "--jump-hosts",
                    get_test_env["pve_test_cluster_jump_host"],
                    "--force",
                    "--pve-cloud-domain",
                    get_test_env["cloud_inventory"]["pve_cloud_domain"],
                    "--pve-host",
                    first_test_host["ansible_host"],
                ]
                + ["--local-pypi-ip", tdd_ip]
                if tdd_ip
                else []
            )
            connect_remote_cluster(parsed_args)
        else:
            logger.info(
                "initializing local ~/.pve-cloud-dyn-inv.yaml with direct access"
            )
            parsed_args = get_parser().parse_args(
                [
                    "connect-cluster",
                    "--pve-host",
                    first_test_host["ansible_host"],
                    "--force",
                    "--pve-cloud-domain",
                    get_test_env["cloud_inventory"]["pve_cloud_domain"],
                ]
            )
            connect_cluster(parsed_args)

    yield


@cloud_fixture("hosts")
def setup_pve_hosts(request, get_test_env, setup_control_node):
    logger.info("setup cloud")

    # run the pve cluster setup on the test environment
    with tempfile.NamedTemporaryFile(
        "w", suffix=".yaml", delete=False
    ) as temp_cloud_inv:
        # write pve cloud inventory file for main pve cluster setup playbook
        pve_clusters = {
            get_test_env["pve_test_cluster_name"]: {
                "pve_unique_cloud_services": ["dns", "dhcp", "psql-state"],
                "pve_host_vars": (
                    get_test_env["pve_test_cluster_host_vars"]
                    if "pve_test_cluster_host_vars" in get_test_env
                    else {}
                ),
                "pve_haproxy_floating_ip_external": get_test_env[
                    "pve_test_cluster_floating_external"
                ],
                "pve_haproxy_floating_ip_internal": get_test_env[
                    "pve_test_cluster_floating_internal"
                ],
            }
        }

        yaml.dump(
            {
                "plugin": "pxc.cloud.pve_cloud_inv",
                "pve_cloud_domain": get_test_env["cloud_inventory"]["pve_cloud_domain"],
                "pve_clusters": pve_clusters,
            }
            | get_test_env["cloud_inventory"],
            temp_cloud_inv,
        )
        temp_cloud_inv.flush()

        logger.info(f"pve cloud inventory tmp path: {temp_cloud_inv.name}")

        extra_vars = {}
        py_pve_cloud_vers, tdd_ip = get_tdd_version("py-pve-cloud")
        if py_pve_cloud_vers:
            extra_vars["test_repos_ip"] = tdd_ip
            extra_vars["py_pve_cloud_version"] = py_pve_cloud_vers

        if not request.config.getoption("--skip-fixture-init"):
            # run the main playbook
            logger.info("run pve cluster setup")
            setup_run = ansible_runner.run(
                project_dir=os.getcwd(),
                playbook="playbooks/setup_pve_clusters.yaml",
                inventory=temp_cloud_inv.name,
                verbosity=request.config.getoption("--ansible-verbosity"),
                extravars=extra_vars,
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
            verbosity=request.config.getoption("--ansible-verbosity"),
        )
        assert uninstall_run.rc == 0


@cloud_fixture("dhcp")
def setup_dhcp_lxcs(request, get_test_env, setup_bind_lxcs):
    logger.info("setup dhcp")

    test_vm_subnet_mask = get_test_env["cloud_inventory"]["pve_vm_subnet"].split("/")[1]

    gateway, nameservers = fetch_default_gw_ns(get_test_env)

    with tempfile.NamedTemporaryFile(
        "w", suffix=".yaml", delete=False
    ) as temp_kea_lxcs_inv:
        logger.info("create kea lxcs")
        yaml.dump(
            {
                "plugin": "pxc.cloud.lxc_inv",
                "target_pve": get_test_env["pve_test_cluster_name"]
                + "."
                + get_test_env["cloud_inventory"]["pve_cloud_domain"],
                "stack_name": "ha-dhcp",
                "lxcs": [
                    {
                        "hostname": "main",
                        "parameters": {
                            "rootfs": f"volume={get_test_env['pve_vm_storage_id']}:10",
                            "cores": 1,
                            "memory": 512,
                            "net0": f"name=pve,bridge=vmbr0,firewall=1,ip={get_test_env['cloud_inventory']['kea_dhcp_main_ip']}/{test_vm_subnet_mask},gw={gateway}"
                            + f"{get_test_env['net0_vlan_tag_rendered'] if 'net0_vlan_tag_rendered' in get_test_env else ''}",
                            "nameserver": nameservers,
                        },
                        "vars": {"kea_dhcp_main": True},
                    },
                    {
                        "hostname": "failover",
                        "parameters": {
                            "rootfs": f"volume={get_test_env['pve_vm_storage_id']}:10",
                            "cores": 1,
                            "memory": 512,
                            "net0": f"name=pve,bridge=vmbr0,firewall=1,ip={get_test_env['cloud_inventory']['kea_dhcp_failover_ip']}/{test_vm_subnet_mask},gw={gateway}"
                            + f"{get_test_env['net0_vlan_tag_rendered'] if 'net0_vlan_tag_rendered' in get_test_env else ''}",
                            "nameserver": nameservers,
                        },
                        "vars": {"kea_dhcp_main": False},
                    },
                ],
                "lxc_global_vars": {"install_prom_systemd_exporter": True},
                "lxc_base_parameters": {"onboot": 1},
                "target_pve_hosts": list(get_test_env["pve_test_cluster_hosts"].keys()),
                "root_ssh_pub_key": get_test_env["ssh_pub_key"],
            },
            temp_kea_lxcs_inv,
        )
        temp_kea_lxcs_inv.flush()

        if not request.config.getoption("--skip-fixture-init"):
            sync_lxcs_kea = ansible_runner.run(
                project_dir=os.getcwd(),
                playbook="playbooks/sync_lxcs.yaml",
                inventory=temp_kea_lxcs_inv.name,
                verbosity=request.config.getoption("--ansible-verbosity"),
            )
            assert sync_lxcs_kea.rc == 0

            logger.info("setup kea lxcs")
            setup_kea_run = ansible_runner.run(
                project_dir=os.getcwd(),
                playbook="playbooks/setup_kea.yaml",
                inventory=temp_kea_lxcs_inv.name,
                verbosity=request.config.getoption("--ansible-verbosity"),
            )
            assert setup_kea_run.rc == 0

        yield

        if request.config.getoption("--skip-cleanup"):
            return  # otherwise destroy the dhcp again

        logger.info("destroy kea lxcs")
        destroy_kea_lxcs_run = ansible_runner.run(
            project_dir=os.getcwd(),
            playbook="playbooks/destroy_lxcs.yaml",
            inventory=temp_kea_lxcs_inv.name,
            verbosity=request.config.getoption("--ansible-verbosity"),
        )
        assert destroy_kea_lxcs_run.rc == 0


@cloud_fixture("dhcp")
def setup_ceph_dhcp_lxcs(request, get_test_env, setup_dhcp_lxcs):

    # conditional ceph dhcp creation
    if "pve_ceph_frontend_dhcp_iface" in get_test_env:
        with tempfile.NamedTemporaryFile(
            "w", suffix=".yaml", delete=False
        ) as temp_kea_lxcs_inv:
            logger.info("create ceph frontend kea lxc")
            yaml.dump(
                {
                    "plugin": "pxc.cloud.lxc_inv",
                    "target_pve": get_test_env["pve_test_cluster_name"]
                    + "."
                    + get_test_env["cloud_inventory"]["pve_cloud_domain"],
                    "stack_name": "ceph-dhcp",
                    "lxcs": [
                        {
                            "parameters": {
                                "rootfs": f"volume={get_test_env['pve_vm_storage_id']}:10",
                                "cores": 1,
                                "memory": 512,
                                "net0": f"name=pve,bridge=vmbr0,firewall=1,ip=dhcp"
                                + f"{get_test_env['net0_vlan_tag_rendered'] if 'net0_vlan_tag_rendered' in get_test_env else ''}",
                                "net1": f"name=cephfe,bridge={get_test_env['pve_ceph_frontend_dhcp_iface']},firewall=1,ip={get_test_env['pve_ceph_frontend_dhcp_net']}",
                            },
                            "vars": {
                                "kea_dhcp_ceph_frontend_subnet": get_test_env[
                                    "pve_ceph_frontend_dhcp_net"
                                ],
                                "kea_dhcp_ceph_frontend_pool": get_test_env[
                                    "pve_ceph_frontend_dhcp_pool"
                                ],
                            },
                        }
                    ],
                    "lxc_global_vars": {"install_prom_systemd_exporter": True},
                    "lxc_base_parameters": {"onboot": 1},
                    "target_pve_hosts": list(
                        get_test_env["pve_test_cluster_hosts"].keys()
                    ),
                    "root_ssh_pub_key": get_test_env["ssh_pub_key"],
                },
                temp_kea_lxcs_inv,
            )
            temp_kea_lxcs_inv.flush()

            if not request.config.getoption("--skip-fixture-init"):
                sync_lxcs_kea = ansible_runner.run(
                    project_dir=os.getcwd(),
                    playbook="playbooks/sync_lxcs.yaml",
                    inventory=temp_kea_lxcs_inv.name,
                    verbosity=request.config.getoption("--ansible-verbosity"),
                )
                assert sync_lxcs_kea.rc == 0

                logger.info("setup kea lxcs")
                setup_kea_run = ansible_runner.run(
                    project_dir=os.getcwd(),
                    playbook="playbooks/setup_ceph_kea.yaml",
                    inventory=temp_kea_lxcs_inv.name,
                    verbosity=request.config.getoption("--ansible-verbosity"),
                )
                assert setup_kea_run.rc == 0

        yield

        if request.config.getoption("--skip-cleanup"):
            return  # otherwise destroy the dhcp again

        logger.info("destroy ceph kea lxcs")
        destroy_kea_lxcs_run = ansible_runner.run(
            project_dir=os.getcwd(),
            playbook="playbooks/destroy_lxcs.yaml",
            inventory=temp_kea_lxcs_inv.name,
            verbosity=request.config.getoption("--ansible-verbosity"),
        )
        assert destroy_kea_lxcs_run.rc == 0
    else:
        yield


@cloud_fixture("bind")
def setup_bind_lxcs(request, get_test_env, setup_pve_hosts):
    logger.info("setup bind")

    test_vm_subnet_mask = get_test_env["cloud_inventory"]["pve_vm_subnet"].split("/")[1]

    gateway, nameservers = fetch_default_gw_ns(get_test_env)

    with tempfile.NamedTemporaryFile(
        "w", suffix=".yaml", delete=False
    ) as temp_bind_lxcs_inv:
        logger.info("create bind lxcs")
        yaml.dump(
            {
                "plugin": "pxc.cloud.lxc_inv",
                "target_pve": get_test_env["pve_test_cluster_name"]
                + "."
                + get_test_env["cloud_inventory"]["pve_cloud_domain"],
                "stack_name": "ha-bind",
                "lxcs": [
                    {
                        "hostname": "master",
                        "parameters": {
                            "rootfs": f"volume={get_test_env['pve_vm_storage_id']}:10",
                            "cores": 1,
                            "memory": 512,
                            "net0": f"name=pve,bridge=vmbr0,firewall=1,ip={get_test_env['cloud_inventory']['bind_master_ip']}/{test_vm_subnet_mask},gw={gateway}"
                            + f"{get_test_env['net0_vlan_tag_rendered'] if 'net0_vlan_tag_rendered' in get_test_env else ''}",
                            "nameserver": nameservers,
                        },
                        "vars": {"bind_master": True},
                    },
                    {
                        "hostname": "failover",
                        "parameters": {
                            "rootfs": f"volume={get_test_env['pve_vm_storage_id']}:10",
                            "cores": 1,
                            "memory": 512,
                            "net0": f"name=pve,bridge=vmbr0,firewall=1,ip={get_test_env['cloud_inventory']['bind_slave_ip']}/{test_vm_subnet_mask},gw={gateway}"
                            + f"{get_test_env['net0_vlan_tag_rendered'] if 'net0_vlan_tag_rendered' in get_test_env else ''}",
                            "nameserver": nameservers,
                        },
                        "vars": {"bind_master": False},
                    },
                ],
                "lxc_global_vars": {"install_prom_systemd_exporter": True},
                "lxc_base_parameters": {"onboot": 1},
                "target_pve_hosts": list(get_test_env["pve_test_cluster_hosts"].keys()),
                "root_ssh_pub_key": get_test_env["ssh_pub_key"],
            },
            temp_bind_lxcs_inv,
        )
        temp_bind_lxcs_inv.flush()

        if not request.config.getoption("--skip-fixture-init"):
            sync_bind_lxcs_run = ansible_runner.run(
                project_dir=os.getcwd(),
                playbook="playbooks/sync_lxcs.yaml",
                inventory=temp_bind_lxcs_inv.name,
                verbosity=request.config.getoption("--ansible-verbosity"),
            )
            assert sync_bind_lxcs_run.rc == 0

            logger.info("setup bind lxcs")
            setup_bind_run = ansible_runner.run(
                project_dir=os.getcwd(),
                playbook="playbooks/setup_bind.yaml",
                inventory=temp_bind_lxcs_inv.name,
                verbosity=request.config.getoption("--ansible-verbosity"),
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
            verbosity=request.config.getoption("--ansible-verbosity"),
        )
        assert destroy_bind_lxcs_run.rc == 0


@cloud_fixture("postgres")
def setup_patroni_lxcs(request, get_test_env, setup_dhcp_lxcs):

    # next we deploy create core lxcs
    with tempfile.NamedTemporaryFile(
        "w", suffix=".yaml", delete=False
    ) as temp_postgres_lxcs_inv:

        logger.info("create patroni lxcs")
        yaml.dump(
            {
                "plugin": "pxc.cloud.lxc_inv",
                "target_pve": get_test_env["pve_test_cluster_name"]
                + "."
                + get_test_env["cloud_inventory"]["pve_cloud_domain"],
                "stack_name": "ha-postgres",
                "lxcs": [
                    {
                        "parameters": {
                            "rootfs": f"volume={get_test_env['pve_vm_storage_id']}:10",
                            "cores": 1,
                            "memory": 512,
                            "net0": f"name=pve,bridge=vmbr0,firewall=1,ip=dhcp"
                            + f"{get_test_env['net0_vlan_tag_rendered'] if 'net0_vlan_tag_rendered' in get_test_env else ''}",
                        }
                    },
                    {
                        "parameters": {
                            "rootfs": f"volume={get_test_env['pve_vm_storage_id']}:10",
                            "cores": 1,
                            "memory": 512,
                            "net0": f"name=pve,bridge=vmbr0,firewall=1,ip=dhcp"
                            + f"{get_test_env['net0_vlan_tag_rendered'] if 'net0_vlan_tag_rendered' in get_test_env else ''}",
                        }
                    },
                    {
                        "parameters": {
                            "rootfs": f"volume={get_test_env['pve_vm_storage_id']}:10",
                            "cores": 1,
                            "memory": 512,
                            "net0": f"name=pve,bridge=vmbr0,firewall=1,ip=dhcp"
                            + f"{get_test_env['net0_vlan_tag_rendered'] if 'net0_vlan_tag_rendered' in get_test_env else ''}",
                        }
                    },
                ],
                "lxc_global_vars": {"install_prom_systemd_exporter": True},
                "target_pve_hosts": list(get_test_env["pve_test_cluster_hosts"].keys()),
                "root_ssh_pub_key": get_test_env["ssh_pub_key"],
            },
            temp_postgres_lxcs_inv,
        )
        temp_postgres_lxcs_inv.flush()

        if not request.config.getoption("--skip-fixture-init"):
            sync_lxcs_postgres = ansible_runner.run(
                project_dir=os.getcwd(),
                playbook="playbooks/sync_lxcs.yaml",
                inventory=temp_postgres_lxcs_inv.name,
                verbosity=request.config.getoption("--ansible-verbosity"),
            )
            assert sync_lxcs_postgres.rc == 0

            logger.info("setup postgres lxcs")
            setup_postgres_run = ansible_runner.run(
                project_dir=os.getcwd(),
                playbook="playbooks/setup_postgres.yaml",
                inventory=temp_postgres_lxcs_inv.name,
                verbosity=request.config.getoption("--ansible-verbosity"),
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
            verbosity=request.config.getoption("--ansible-verbosity"),
        )
        assert destroy_postgres_lxcs_run.rc == 0


@cloud_fixture("proxy")
def setup_haproxy_lxcs(request, get_test_env, setup_patroni_lxcs):

    # next we deploy create core lxcs
    with tempfile.NamedTemporaryFile(
        "w", suffix=".yaml", delete=False
    ) as temp_haproxy_lxcs_inv:

        # haproxy
        logger.info("create haproxy lxcs")
        yaml.dump(
            {
                "plugin": "pxc.cloud.lxc_inv",
                "target_pve": get_test_env["pve_test_cluster_name"]
                + "."
                + get_test_env["cloud_inventory"]["pve_cloud_domain"],
                "stack_name": "ha-haproxy",
                "static_includes": {
                    "postgres_stack": "ha-postgres."
                    + get_test_env["cloud_inventory"]["pve_cloud_domain"],
                },
                "lxcs": [
                    {
                        "hostname": "master",
                        "parameters": {
                            "rootfs": f"volume={get_test_env['pve_vm_storage_id']}:10",
                            "cores": 1,
                            "memory": 512,
                            # todo: schema ext fix iface name
                            "net0": f"name=eth0,bridge=vmbr0,firewall=1,ip=dhcp"
                            + f"{get_test_env['net0_vlan_tag_rendered'] if 'net0_vlan_tag_rendered' in get_test_env else ''}",
                        },
                        "vars": {"keepalived_master": True},
                    },
                    {
                        "hostname": "failover",
                        "parameters": {
                            "rootfs": f"volume={get_test_env['pve_vm_storage_id']}:10",
                            "cores": 1,
                            "memory": 512,
                            "net0": f"name=eth0,bridge=vmbr0,firewall=1,ip=dhcp"
                            + f"{get_test_env['net0_vlan_tag_rendered'] if 'net0_vlan_tag_rendered' in get_test_env else ''}",
                        },
                        "vars": {"keepalived_master": False},
                    },
                ],
                "lxc_global_vars": {
                    "install_prom_systemd_exporter": True,
                    "haproxy_defaults_section": "timeout client 3m\ntimeout server 3m",
                },
                "target_pve_hosts": list(get_test_env["pve_test_cluster_hosts"].keys()),
                "root_ssh_pub_key": get_test_env["ssh_pub_key"],
            },
            temp_haproxy_lxcs_inv,
        )
        temp_haproxy_lxcs_inv.flush()

        if not request.config.getoption("--skip-fixture-init"):
            sync_lxcs_haproxy = ansible_runner.run(
                project_dir=os.getcwd(),
                playbook="playbooks/sync_lxcs.yaml",
                inventory=temp_haproxy_lxcs_inv.name,
                verbosity=request.config.getoption("--ansible-verbosity"),
            )
            assert sync_lxcs_haproxy.rc == 0

            logger.info("setup haproxy lxcs")
            setup_haproxy_run = ansible_runner.run(
                project_dir=os.getcwd(),
                playbook="playbooks/setup_haproxy.yaml",
                inventory=temp_haproxy_lxcs_inv.name,
                verbosity=request.config.getoption("--ansible-verbosity"),
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
            verbosity=request.config.getoption("--ansible-verbosity"),
        )
        assert destroy_haproxy_lxcs_run.rc == 0


@cloud_fixture("cache")
def setup_cache_lxcs(request, get_test_env, setup_dhcp_lxcs):

    # next we deploy create core lxcs
    with tempfile.NamedTemporaryFile(
        "w", suffix=".yaml", delete=False
    ) as temp_cache_lxcs_inv:
        # cache
        logger.info("create cache lxc")
        yaml.dump(
            {
                "plugin": "pxc.cloud.lxc_inv",
                "target_pve": get_test_env["pve_test_cluster_name"]
                + "."
                + get_test_env["cloud_inventory"]["pve_cloud_domain"],
                "stack_name": "cloud-cache",
                "lxcs": [
                    {
                        "hostname": "main",
                        "parameters": {
                            "rootfs": f"volume={get_test_env['pve_vm_storage_id']}:200",
                            "cores": 2,
                            "memory": 256,
                            "net0": f"name=eth0,bridge=vmbr0,firewall=1,ip=dhcp"
                            + f"{get_test_env['net0_vlan_tag_rendered'] if 'net0_vlan_tag_rendered' in get_test_env else ''}",
                            # mount perms for nfs and future docker
                            # todo: put into schema
                            "features": "nesting=1",
                            "unprivileged": 0,
                        },
                    },
                ],
                "target_pve_hosts": list(get_test_env["pve_test_cluster_hosts"].keys()),
                "root_ssh_pub_key": get_test_env["ssh_pub_key"],
            },
            temp_cache_lxcs_inv,
        )
        temp_cache_lxcs_inv.flush()

        if not request.config.getoption("--skip-fixture-init"):
            sync_lxcs = ansible_runner.run(
                project_dir=os.getcwd(),
                playbook="playbooks/sync_lxcs.yaml",
                inventory=temp_cache_lxcs_inv.name,
                verbosity=request.config.getoption("--ansible-verbosity"),
            )
            assert sync_lxcs.rc == 0

            logger.info("setup cache lxcs")
            setup_run = ansible_runner.run(
                project_dir=os.getcwd(),
                playbook="playbooks/setup_cloud_cache.yaml",
                inventory=temp_cache_lxcs_inv.name,
                verbosity=request.config.getoption("--ansible-verbosity"),
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
            verbosity=request.config.getoption("--ansible-verbosity"),
        )
        assert destroy_lxcs_run.rc == 0


@pytest.fixture(scope="session")
def setup_prepare_kubespray(
    get_test_env,
    setup_haproxy_lxcs,
    setup_cache_lxcs,
    setup_ceph_dhcp_lxcs,
):
    logger.info("setup environment for kubespray playbooks")

    copy_cloud_domain = get_cloud_domain(
        get_test_env["kubernetes"]["k8s_tls_copy_target_pve"]
    )
    copy_pve_inventory = get_pve_inventory(copy_cloud_domain)
    copy_target_cluster = get_target_cluster(
        copy_pve_inventory,
        get_test_env["kubernetes"]["k8s_tls_copy_target_pve"],
        copy_cloud_domain,
    )

    copy_pve_host, copy_jump_host = get_online_pve_host(
        copy_pve_inventory, copy_target_cluster
    )

    # copy target has to be a directly accessible proxmox cluster (no jump hosts allowed)
    assert copy_jump_host is None

    # we connect to the test host to get the patroni secret of the cluster, aswell as the vars
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(
        copy_pve_host,
        username="root",
    )

    # since we need root we cant use sftp and root via ssh is disabled
    _, stdout, _ = ssh.exec_command("cat /etc/pve/cloud/cluster_vars.yaml")

    cluster_vars = yaml.safe_load(stdout.read().decode("utf-8"))
    logger.info(cluster_vars["pve_haproxy_floating_ip_internal"])
    _, stdout, _ = ssh.exec_command("cat /etc/pve/cloud/secrets/patroni.pass")

    patroni_pass = stdout.read().decode("utf-8").strip()
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
                f"{get_test_env['kubernetes']['k8s_tls_copy_stack_name']}.{cluster_vars['pve_cloud_domain']}",
            ),
        )
        record = cur.fetchone()

        assert record
        logger.info(record)

    # next the record needs to be inserted, for that we connect to our test cluster and fetch the secrets needed
    first_test_host = get_test_env["pve_test_cluster_hosts"][
        next(iter(get_test_env["pve_test_cluster_hosts"]))
    ]["ansible_host"]

    with connect_host(
        first_test_host, get_test_env.get("pve_test_cluster_jump_host")
    ) as ssh:
        _, stdout, _ = ssh.exec_command("cat /etc/pve/cloud/secrets/internal.key")
        bind_ns_update_key = re.search(
            r'secret\s+"([^"]+)";', stdout.read().decode("utf-8")
        ).group(1)

        logger.info(bind_ns_update_key)

        _, stdout, _ = ssh.exec_command("cat /etc/pve/cloud/secrets/patroni.pass")
        patroni_pass = stdout.read().decode("utf-8")

    pg_conn_str_orm = f"postgresql+psycopg2://postgres:{patroni_pass}@{get_test_env['pve_test_cluster_floating_internal']}:5000/pve_cloud?sslmode=disable"

    # start pxrpc server for injecting
    if "pve_test_cluster_jump_host" in get_test_env:
        with launch_pxrpc(
            get_test_env["pve_test_cluster_jump_host"],
            first_test_host,
        ) as (pxrpc, jump_host):
            pxrpc.e2e_inject_cert(
                pg_conn_str_orm,
                f"pytest-k8s.{get_test_env['cloud_inventory']['pve_cloud_domain']}",
                json.dumps(record[0]),
            )
    else:
        engine = create_engine(pg_conn_str_orm)

        # update certs and mirror pull secret
        with Session(engine) as session:
            copy_cert = AcmeX509(
                stack_fqdn=f"pytest-k8s.{get_test_env['cloud_inventory']['pve_cloud_domain']}",
                config={},
                ec_csr={},
                ec_crt={},
                k8s=record[0],
            )
            session.merge(copy_cert)
            session.commit()

    # set manual cp records (only for testing prod is manually manged)
    dns_update = dns.update.Update(
        get_test_env["kubernetes"]["deployments_domain"],
        keyring=dns.tsigkeyring.from_text({"internal.": bind_ns_update_key}),
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
    logger.info(response.rcode())

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
    logger.info(response.rcode())
