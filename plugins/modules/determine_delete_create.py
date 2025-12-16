#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
import copy

from ansible_collections.pxc.cloud.plugins.module_utils.identity import stack_vm_get_blake


def run_module():
    module_args = dict(
        inventory_vms=dict(type='list', required=True),
        stack_vms=dict(type='list', required=True)
    )
    module = AnsibleModule(argument_spec=module_args)

    inventory_vms = module.params['inventory_vms']
    stack_vms = module.params['stack_vms']

    existing_blake_ids = [stack_vm_get_blake(vm) for vm in stack_vms if stack_vm_get_blake(vm) is not None]

    # get nodes that we have to create
    vms_to_create = copy.deepcopy(inventory_vms)

    # keep substracting until only vms that we need to create are left
    for blake_id in existing_blake_ids:
        for i, vm in enumerate(vms_to_create):
            if vm[0] == blake_id:
                vms_to_create.pop(i)
                break


    # determine nodes we have to delete, by substracting the inventory from what exists, the leftovers are what we need to delete
    vms_to_delete = copy.deepcopy(stack_vms)

    for inventory_vm in inventory_vms:
        for i, stack_vm in enumerate(vms_to_delete):
            if inventory_vm[0] == stack_vm_get_blake(stack_vm):
                vms_to_delete.pop(i)
                break


    result = dict(
        changed=True,
        vms_to_create=vms_to_create,
        vms_to_delete=vms_to_delete
    )

    module.exit_json(**result)


if __name__ == '__main__':
    run_module()
