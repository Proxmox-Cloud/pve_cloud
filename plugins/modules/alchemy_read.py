#!/usr/bin/python
from ansible.module_utils.basic import AnsibleModule
from pve_cloud.orm.alchemy import alch_read


def run_module():
    module_args = dict(
        pg_conn_str=dict(type='str', required=True),
        table=dict(type='str', required=True),
        where=dict(type='dict', default={}),
    )
    module = AnsibleModule(argument_spec=module_args)

    query_result = alch_read(module.params["pg_conn_str"], module.params["table"], module.params["where"])
    result = dict(
        changed=True,
        query_result=query_result,
        rowcount=len(query_result)
    )

    module.exit_json(**result)


if __name__ == '__main__':
    run_module()
