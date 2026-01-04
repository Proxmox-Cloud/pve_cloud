#!/usr/bin/python

import math
from itertools import permutations

from ansible.module_utils.basic import AnsibleModule


# Function to calculate remaining memory after each VM is allocated to the host with the most available memory
def calculate_remaining_memory_dynamic(vms_distribution, hosts):
    remaining_memory = [
        host["mem_total"] - host["reserved"] for host in hosts
    ]  # Extract the memory values
    fitted_hosts = []

    for vm in vms_distribution:
        vm_memory = vm[1]["parameters"]["memory"]  # Extract memory from parameters
        # Find the host with the most available memory and allocate the VM to it
        max_index = remaining_memory.index(max(remaining_memory))
        remaining_memory[
            max_index
        ] -= vm_memory  # Subtract the VM memory from the selected host
        fitted_hosts.append(
            hosts[max_index]["hostname"]
        )  # Map the VM index to the host's hostname

    return remaining_memory, fitted_hosts


# Function to calculate the balance (how evenly memory is distributed)
def calculate_memory_balance(remaining_memory):
    return max(remaining_memory) - min(remaining_memory)


def run_module():
    module_args = dict(
        host_mem_list=dict(type="list", required=True),
        nodes_to_create=dict(type="list", required=True),
    )
    module = AnsibleModule(argument_spec=module_args)

    hosts = module.params["host_mem_list"]

    # some nodes might have a specific target host set, those wont be fittet randomly

    nodes = [
        node
        for node in module.params["nodes_to_create"]
        if "target_host" not in node[1]
    ]

    best_distribution = None
    best_fitted_hosts = None
    best_balance = math.inf

    for vm_distribution in permutations(nodes):
        remaining_memory, fitted_hosts = calculate_remaining_memory_dynamic(
            vm_distribution, hosts
        )
        balance = calculate_memory_balance(remaining_memory)

        # Keep track of the best distribution
        if balance < best_balance:
            best_balance = balance
            best_distribution = list(vm_distribution)
            best_fitted_hosts = fitted_hosts

    # extend results by vms that want to be on a specific host
    best_distribution.extend(
        [node for node in module.params["nodes_to_create"] if "target_host" in node[1]]
    )
    best_fitted_hosts.extend(
        [
            node[1]["target_host"]
            for node in module.params["nodes_to_create"]
            if "target_host" in node[1]
        ]
    )

    result = dict(
        changed=True,
        best_fitted_hosts=best_fitted_hosts,
        best_distribution=best_distribution,
    )

    module.exit_json(**result)


if __name__ == "__main__":
    run_module()
