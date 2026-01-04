DOCUMENTATION = r"""
name: sort_and_hash
short_description: Creates unique hash for vms based on sorted params.
"""

from ansible_collections.pxc.cloud.plugins.module_utils.identity import \
    sort_and_hash


class FilterModule(object):
    def filters(self):
        return {"sort_and_hash": sort_and_hash}
