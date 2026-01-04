#!/usr/bin/python
from ansible.module_utils.basic import AnsibleModule
from pve_cloud.orm.alchemy import alch_write


def run_module():
    module_args = dict(
        pg_conn_str=dict(type="str", required=True),
        table=dict(type="str", required=True),
        rows=dict(type="list", required=True),
    )
    module = AnsibleModule(argument_spec=module_args)

    alch_write(
        module.params["pg_conn_str"], module.params["table"], module.params["rows"]
    )

    result = dict(changed=True)

    module.exit_json(**result)


if __name__ == "__main__":
    run_module()
