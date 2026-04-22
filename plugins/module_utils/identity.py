import copy
import hashlib
import json


def stack_vm_get_blake(vm):
    for tag in vm["tags"].split(";"):
        if tag.endswith("-blake"):
            return tag.removesuffix("-blake")

    return None  # no blake id found


def sort_and_hash(vm_params, stack_name):
    hash_core = copy.deepcopy(vm_params)

    # delete keys that are irrelevant for the identity
    # we dont use variables for uniqueness of vm
    if "vars" in hash_core:
        del hash_core["vars"]

    # this gives uniqueness to vms with the same parameters in different stacks
    if stack_name:  # none logic for update playbook
        hash_core["stack_name"] = stack_name

    # we are after the sort_keys parameter, which recursively sorts the input nested dict
    json_str = json.dumps(hash_core, separators=(",", ":"), sort_keys=True)

    # Create the hash using the specified algorithm
    hash_obj = hashlib.blake2s(digest_size=10)
    hash_obj.update(json_str.encode("utf-8"))

    return hash_obj.hexdigest()
