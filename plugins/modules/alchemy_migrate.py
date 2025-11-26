#!/usr/bin/python
from ansible.module_utils.basic import AnsibleModule
from pve_cloud.orm.alchemy import migrate


def run_module():
    module_args = dict(
        pg_conn_str=dict(type='str', required=True),
    )
    module = AnsibleModule(argument_spec=module_args)

    # todo parse migration result and return changed only when actually run
    migrate(module.params["pg_conn_str"])

    result = dict(
        changed=True
    )

    module.exit_json(**result)


if __name__ == '__main__':
    run_module()
