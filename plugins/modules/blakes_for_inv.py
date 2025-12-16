#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.pxc.cloud.plugins.module_utils.identity import sort_and_hash

def run_module():
    module_args = dict(
        vms=dict(type='list', required=True),
    )
    module = AnsibleModule(argument_spec=module_args)


    result = dict(
        blakes=[(f"{sort_and_hash(vm)}-blake", vm) for vm in module.params['vms']]
    )

    module.exit_json(**result)


if __name__ == '__main__':
    run_module()

