from ansible_collections.pve.cloud.plugins.module_utils.identity import sort_and_hash

class FilterModule(object):
    def filters(self):
        return {
            'sort_and_hash': sort_and_hash
        }
