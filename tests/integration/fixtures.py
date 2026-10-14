import logging

import pytest
import yaml
from pve_cloud.orm.alchemy import migrate
from pve_cloud_test.cloud_fixtures import (run_integration_playbook,
                                           run_playbook)
from pve_cloud_test.integration import integration_config, launch_containers

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def setup_postgres_container(request, integration_config):
    logger.info("setting up postgres")

    namespace, v1 = integration_config

    # with launch containers() via test lib
    # boostrap container / build images
    # return list of ansible_host / ansible_user grouped
    with launch_containers(
        namespace,
        v1,
        {
            "pxc-postgres": {
                "image": "postgres:17-bookworm",
                "ports": ["5432:5432"],
                "user": "root",
                "env": {"POSTGRES_PASSWORD": "integration-test-123"},
                "readiness_probe": {
                    "command": [
                        "pg_isready",
                        "-U",
                        "postgres",
                        "-h",
                        "127.0.0.1",
                        "-p",
                        "5432",
                    ],
                    "args": {"initial_delay_seconds": 5, "period_seconds": 3},
                },
            }
        },
    ) as postgres_host:
        pg_conn_str = f"postgresql+psycopg2://postgres:integration-test-123@{postgres_host['pxc-postgres']['ansible_host']}:5432/pve_cloud?sslmode=disable"
        logger.info(pg_conn_str)

        # temp playbook taht simply calls the migration module
        # cannot call migration function directly as it fucks with pytest logging!
        migrate_playbook = [
            {
                "name": "Temp create ro role",
                "hosts": "pxc-executor-host",
                "tasks": [
                    {
                        "community.postgresql.postgresql_db": {
                            "name": "pve_cloud",
                            "login_password": "integration-test-123",
                            "login_host": postgres_host["pxc-postgres"]["ansible_host"],
                            "port": 5432,
                        }
                    },
                    {"pxc.cloud.alchemy_migrate": {"pg_conn_str": pg_conn_str}},
                ],
            }
        ]

        with run_integration_playbook(request, migrate_playbook):
            logger.info("done migrating")

            yield postgres_host, pg_conn_str
