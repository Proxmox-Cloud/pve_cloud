import logging
import os
import subprocess
import tempfile

import ansible_runner
import paramiko
import pytest
import yaml
from pve_cloud_test.cloud_fixtures import *

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

        # run the main playbook
        logger.info("run control node setup")
        setup_run = ansible_runner.run(
            project_dir=os.getcwd(),
            playbook="playbooks/setup_control_node.yaml",
            verbosity=request.config.getoption("--ansible-verbosity"),
        )

        assert setup_run.rc == 0

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

        if not request.config.getoption("--skip-fixture-init"):
            # run the main playbook
            logger.info("run pve cluster setup")
            setup_run = ansible_runner.run(
                project_dir=os.getcwd(),
                playbook="playbooks/setup_pve_clusters.yaml",
                inventory=temp_cloud_inv.name,
                verbosity=request.config.getoption("--ansible-verbosity"),
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
