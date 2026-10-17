import logging

import pytest
import yaml
from fixtures import *
from kubernetes import client
from kubernetes.stream import stream
from pve_cloud_test.cloud_fixtures import (run_integration_playbook,
                                           run_playbook)
from pve_cloud_test.integration import launch_containers

logger = logging.getLogger(__name__)


def test_setup_acme_certs(request, integration_config, setup_postgres_container):
    logger.info("test setup acme certs")

    kubeconfig_path, _, v1, namespace = integration_config

    postgres_host, pg_conn_str = setup_postgres_container

    # write custom playbook for creation of read only
    # row scoped access to postgres
    ro_role_playbook = [
        {
            "name": "Temp create ro role",
            "hosts": "localhost",
            "vars": {
                "postgres_host": postgres_host["pxc-postgres"]["ansible_host"],
                "postgres_password": "integration-test-123",
                "pg_conn_str": pg_conn_str,
                "pve_cloud_domain": "pxc.integration.test",
                "stack_name": "test_setup_acme_certs",
            },
            "roles": ["pxc.cloud.postgres_acme_ro_access"],
            # insert mock certifcate for later sync
            "tasks": [
                {
                    "pxc.cloud.alchemy_write": {
                        "pg_conn_str": pg_conn_str,
                        "table": "acme_x509",
                        "rows": [
                            {
                                "stack_fqdn": "test_setup_acme_certs.pxc.integration.test",
                                "ec_crt": {
                                    "crt": "-----BEGIN CERTIFICATE-----\nTESTTEST\n-----END CERTIFICATE-----"
                                },
                            }
                        ],
                    },
                    "delegate_to": "pxc-executor-host",
                }
            ],
        }
    ]

    with run_integration_playbook(request, ro_role_playbook):
        pass

    # write tempfile playbook and execute
    logger.info("launching qemus mock")
    with launch_containers(
        namespace,
        v1,
        {"test": {"image_kind": "qemus", "user": "root"}},
        kubeconfig_path,
    ) as inv:

        logger.info(inv)

        sync_job_playbook = [
            {
                "name": "Temp sync job playbook",
                "hosts": "qemus",
                "vars": {
                    "pg_conn_str": pg_conn_str,
                    "pve_cloud_domain": "pxc.integration.test",
                    "stack_name": "test_setup_acme_certs",
                    "postgres_port": 5432,
                    "postgres_host": postgres_host["pxc-postgres"]["k8s_pod_ip"],
                    "stack_cert_sync_paths": [
                        {
                            "path": "/tmp/test.crt",
                            "owner": "root",
                            "group": "root",
                            "mode": "0777",
                        }
                    ],
                },
                "roles": ["pxc.cloud.setup_acme_ro_sync_job"],
                "tasks": [{"name": "test", "debug": {"msg": "test"}}],
            }
        ]
        sync_job_inventory = {"qemus": {"hosts": inv}}

        with run_integration_playbook(request, sync_job_playbook, sync_job_inventory):
            # manually invoke the sync script
            sync_result = stream(
                v1.connect_get_namespaced_pod_exec,
                name="test",
                namespace=namespace,
                command=["/opt/pxc-acme/pxc-acme-sync.sh"],
                stderr=True,
                stdin=False,
                stdout=True,
                tty=False,
            )

            # assert that the sync script printed a success message
            assert "SUCCESS: ACME certificates synced successfully" in sync_result

            # check if crt got synced
            result = stream(
                v1.connect_get_namespaced_pod_exec,
                name="test",
                namespace=namespace,
                command=["cat", "/tmp/test.crt"],
                stderr=True,
                stdin=False,
                stdout=True,
                tty=False,
            )

            assert result.strip()
