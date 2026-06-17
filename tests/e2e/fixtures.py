import json
import logging
import os
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
from pve_cloud.orm.alchemy import AcmeX509, ProxmoxCloudSecrets
from pve_cloud_test.cloud_fixtures import *
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


@cloud_fixture("localhost", "control-node")
def setup_control_node(request, get_test_env):
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

    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as tmp_reqs:
        temp_reqs_path = tmp_reqs.name

        # modify ee-requirements.txt which are used as base setup dependencies for the control node
        with open("meta/ee-requirements.txt") as ee_reqs:

            write_toggle = True
            for rl in ee_reqs:
                if rl.startswith("# PXC E2E EXCLUDE BLOCK START"):
                    write_toggle = False
                elif rl.startswith("# PXC E2E EXCLUDE BLOCK END"):
                    write_toggle = True

                if write_toggle:
                    tmp_reqs.write(rl)

    # control node setup adjustments
    extra_vars = {"custom_ee_reqs_path": temp_reqs_path}

    # run the main playbook
    logger.info("run control node setup")
    setup_run = ansible_runner.run(
        project_dir=os.getcwd(),
        playbook="playbooks/setup_control_node.yaml",
        verbosity=request.config.getoption("--ansible-verbosity"),
        extravars=extra_vars,
    )

    assert setup_run.rc == 0

    # initialize the locally kept inventory for pxc clouds and their pve clusters
    tdd_ip = get_tdd_ip()
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
        logger.info("initializing local ~/.pve-cloud-dyn-inv.yaml with direct access")
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


@cloud_fixture("hosts", "pve")
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


@cloud_fixture("dhcp", "kea")
def setup_dhcp_lxcs(request, get_test_env, fetch_default_gw_ns, setup_bind_lxcs):
    logger.info("setup dhcp")

    test_vm_subnet_mask = get_test_env["cloud_inventory"]["pve_vm_subnet"].split("/")[1]

    gateway, nameservers = fetch_default_gw_ns

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
                            "memory": 256,
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
                            "memory": 256,
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

        logger.info("destroy kea lxcs")
        destroy_kea_lxcs_run = ansible_runner.run(
            project_dir=os.getcwd(),
            playbook="playbooks/destroy_lxcs.yaml",
            inventory=temp_kea_lxcs_inv.name,
            verbosity=request.config.getoption("--ansible-verbosity"),
        )
        assert destroy_kea_lxcs_run.rc == 0


@cloud_fixture("dhcp", "ceph", "kea")
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
                                "memory": 256,
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


@cloud_fixture("bind", "dns")
def setup_bind_lxcs(request, get_test_env, fetch_default_gw_ns, setup_pve_hosts):
    logger.info("setup bind")

    test_vm_subnet_mask = get_test_env["cloud_inventory"]["pve_vm_subnet"].split("/")[1]

    gateway, nameservers = fetch_default_gw_ns

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
                            "memory": 256,
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
                            "memory": 256,
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

        logger.info("destroy bind lxcs")
        destroy_bind_lxcs_run = ansible_runner.run(
            project_dir=os.getcwd(),
            playbook="playbooks/destroy_lxcs.yaml",
            inventory=temp_bind_lxcs_inv.name,
            verbosity=request.config.getoption("--ansible-verbosity"),
        )
        assert destroy_bind_lxcs_run.rc == 0


@cloud_fixture("patroni", "postgres")
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
                "lxc_global_vars": {"install_prom_systemd_exporter": True},
                "target_pve_hosts": list(get_test_env["pve_test_cluster_hosts"].keys()),
                "root_ssh_pub_key": get_test_env["ssh_pub_key"],
            },
            temp_postgres_lxcs_inv,
        )
        temp_postgres_lxcs_inv.flush()

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

        logger.info("destroy postgres lxcs")
        destroy_postgres_lxcs_run = ansible_runner.run(
            project_dir=os.getcwd(),
            playbook="playbooks/destroy_lxcs.yaml",
            inventory=temp_postgres_lxcs_inv.name,
            verbosity=request.config.getoption("--ansible-verbosity"),
        )
        assert destroy_postgres_lxcs_run.rc == 0


@cloud_fixture("haproxy", "proxy")
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
                            "memory": 256,
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
                            "memory": 256,
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

        logger.info("destroy haproxy lxcs")
        destroy_haproxy_lxcs_run = ansible_runner.run(
            project_dir=os.getcwd(),
            playbook="playbooks/destroy_lxcs.yaml",
            inventory=temp_haproxy_lxcs_inv.name,
            verbosity=request.config.getoption("--ansible-verbosity"),
        )
        assert destroy_haproxy_lxcs_run.rc == 0


@cloud_fixture("kubespray", "k8s")
def setup_prepare_kubespray(
    request,
    get_test_env,
    get_cloud_secrets,
    setup_haproxy_lxcs,
    setup_ceph_dhcp_lxcs,
):
    logger.info("setup environment for kubespray playbooks")

    # copy tls
    copy_cloud_domain = get_cloud_domain(get_test_env["kubernetes"]["copy_target_pve"])
    copy_pve_inventory = get_pve_inventory(copy_cloud_domain)
    copy_target_cluster = get_target_cluster(
        copy_pve_inventory,
        get_test_env["kubernetes"]["copy_target_pve"],
        copy_cloud_domain,
    )

    copy_pve_host, copy_jump_host = get_online_pve_host(
        copy_pve_inventory, copy_target_cluster
    )

    # copy target has to be a directly accessible proxmox cluster (no jump hosts allowed)
    assert (
        copy_jump_host is None
    ), "Copy target pve for tls and harbor creds needs to be directly accessible! Jump host not yet supported."

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
                f"{get_test_env['kubernetes']['tls_copy_stack_name']}.{cluster_vars['pve_cloud_domain']}",
            ),
        )
        record = cur.fetchone()

        assert record
        logger.info(record)

    # next the record needs to be inserted, for that we connect to our test cluster and fetch the secrets needed
    first_test_host = get_test_env["pve_test_cluster_hosts"][
        next(iter(get_test_env["pve_test_cluster_hosts"]))
    ]["ansible_host"]

    # start pxrpc server for injecting
    if "pve_test_cluster_jump_host" in get_test_env:
        with launch_pxrpc(
            get_test_env["pve_test_cluster_jump_host"],
            first_test_host,
        ) as (pxrpc, jump_host):
            pxrpc.e2e_inject_cert(
                f"pytest-k8s.{get_test_env['cloud_inventory']['pve_cloud_domain']}",
                json.dumps(record[0]),
            )
    else:
        engine = create_engine(get_cloud_secrets["pg_conn_str_orm"])

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

    # copy harbor mirror credentials iif specified in test env
    if "harbor_copy_mirror_host" in get_test_env["kubernetes"]:
        logger.info("copying external harbor mirror credentials")

        with conn.cursor() as cur:
            # query harbor admin creds
            cur.execute(
                "SELECT secret_data FROM px_cloud_secrets WHERE secret_name = %s;",
                (f"{get_test_env['kubernetes']['harbor_copy_mirror_host']}-admin",),
            )
            admin_secret = cur.fetchone()

            assert admin_secret
            logger.info(admin_secret)

            cur.execute(
                "SELECT secret_data FROM px_cloud_secrets WHERE secret_name = %s;",
                (f"{get_test_env['kubernetes']['harbor_copy_mirror_host']}-mirror",),
            )
            mirror_secret = cur.fetchone()

            assert mirror_secret
            logger.info(mirror_secret)

        # next we inject the secrets
        if "pve_test_cluster_jump_host" in get_test_env:
            with launch_pxrpc(
                get_test_env["pve_test_cluster_jump_host"],
                first_test_host,
            ) as (pxrpc, jump_host):
                assert pxrpc.merge_cloud_secret(
                    get_test_env["cloud_inventory"][
                        "pve_cloud_domain"
                    ],  # fake the cloud domain
                    f"{get_test_env['kubernetes']['harbor_copy_mirror_host']}-admin",
                    json.dumps(admin_secret[0]),
                    "harbor-admin-auth",
                )

                assert pxrpc.merge_cloud_secret(
                    get_test_env["cloud_inventory"]["pve_cloud_domain"],
                    f"{get_test_env['kubernetes']['harbor_copy_mirror_host']}-mirror",
                    json.dumps(mirror_secret[0]),
                    "harbor-mirror-auth",
                )
        else:
            engine = create_engine(get_cloud_secrets["pg_conn_str_orm"])

            # update certs and mirror pull secret
            with Session(engine) as session:
                copy_admin = ProxmoxCloudSecrets(
                    cloud_domain=get_test_env["cloud_inventory"]["pve_cloud_domain"],
                    secret_name=f"{get_test_env['kubernetes']['harbor_copy_mirror_host']}-admin",
                    secret_data=admin_secret[0],
                    secret_type="harbor-admin-auth",
                )
                session.merge(copy_admin)

                copy_mirror = ProxmoxCloudSecrets(
                    cloud_domain=get_test_env["cloud_inventory"]["pve_cloud_domain"],
                    secret_name=f"{get_test_env['kubernetes']['harbor_copy_mirror_host']}-mirror",
                    secret_data=mirror_secret[0],
                    secret_type="harbor-mirror-auth",
                )
                session.merge(copy_mirror)

                session.commit()

    yield


@cloud_fixture("mirror")
def setup_mirror_vm(request, get_test_env, setup_haproxy_lxcs):
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
                "stack_name": "pytest-mirror-vm",
                "qemu_base_parameters": {
                    "cpu": "host",
                    "net0": "virtio,bridge=vmbr0,firewall=1"
                    + f"{get_test_env['net0_vlan_tag_rendered'] if 'net0_vlan_tag_rendered' in get_test_env else ''}",
                    "sockets": 1,
                },
                # "tcp_proxies": [],
                "ingress_domains": [
                    {
                        "zone": get_test_env["cloud_inventory"][
                            "pve_cloud_domain"
                        ],  # we use cloud domain because deployments is not yet initialized
                        "names": ["pxc-aptly"],
                    }
                ],
                "qemu_global_vars": {
                    "aptly_mirror_domain": f"pxc-aptly."
                    + get_test_env["cloud_inventory"]["pve_cloud_domain"]
                },
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
                            "size": "250G",
                            "options": {
                                "discard": "on",
                                "iothread": "on",
                                "ssd": "on",
                                "cache": "unsafe",
                            },
                            # use ceph storage pool since that is for big
                            # stuff in e2e
                            "pool": get_test_env["ceph_csi_storage_pool"],
                        },
                        "parameters": {
                            "cores": 4,
                            "memory": 4096,
                        },
                        # overwrite values for vm interface, to set a static ip instead of default
                        # dhcp4 conf
                        "network_config": yaml.safe_dump(
                            {
                                "network": {
                                    "ethernets": {
                                        "pve": {
                                            "dhcp4": False,
                                            "addresses": [
                                                get_test_env["pve_test_cloud_mirror_ip"]
                                            ],
                                            "routes": [
                                                {
                                                    "to": "default",
                                                    "via": get_test_env[
                                                        "cloud_inventory"
                                                    ]["kea_dhcp_routers"],
                                                }
                                            ],
                                            "nameservers": {
                                                "addresses": [
                                                    get_test_env["cloud_inventory"][
                                                        "bind_master_ip"
                                                    ],
                                                    get_test_env["cloud_inventory"][
                                                        "bind_slave_ip"
                                                    ],
                                                ]
                                            },
                                        }
                                    }
                                }
                            }
                        ),
                    },
                ],
                "target_pve_hosts": list(get_test_env["pve_test_cluster_hosts"].keys()),
                "root_ssh_pub_key": get_test_env["ssh_pub_key"],
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

        # run get blakes on qemus
        setup_mirror_run = ansible_runner.run(
            project_dir=os.getcwd(),
            playbook="playbooks/setup_mirror_vm.yaml",
            inventory=temp_qemu_inv.name,
            verbosity=request.config.getoption("--ansible-verbosity"),
        )

        assert setup_mirror_run.rc == 0

        yield

        qemu_destroy_run = ansible_runner.run(
            project_dir=os.getcwd(),
            playbook="playbooks/destroy_qemus.yaml",
            inventory=temp_qemu_inv.name,
            verbosity=request.config.getoption("--ansible-verbosity"),
        )
        assert qemu_destroy_run.rc == 0
