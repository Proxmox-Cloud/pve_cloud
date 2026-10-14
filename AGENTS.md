# Agent Instructions

This is the ansible collection at the heart of the Proxmox Cloud project.

## Running Tests

For running tests you should strictly focus on the integration tests located under `tests/integration`. Never execute any e2e tests!

To run tests you have to do the following:

1. Run the `tests/setup-integration-env.sh` bash script. This sets up the python enviroment and any needed dependencies.
2. Run `source ~/.pxc-integration-venv/bin/activate` to activate the virtual environment.
3. Run the integration tests:
```bash
# run the entire integration testing suite
pytest -s tests/integration/

# run specific tests
pytest -s tests/integration/test_cloud.py::test_setup_acme_certs
```

## Writing Tests

Features you create should make use of the integration testing library. You should create integration tests and execute them to validate your changes!

To understand how to write them you may analyze the existing tests in `tests/integration`.

## Creating Ansible Roles

Creating roles should always be done using `ansible-galaxy init ROLE_NAME` inside the `roles/` directory of this collection:

```bash
cd roles
ansible-galaxy init ROLE_NAME
```

