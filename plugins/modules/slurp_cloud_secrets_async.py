#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
import asyncio
import aiofiles
import base64
import os


async def slurp_file(path):
    async with aiofiles.open(path, 'rb') as f:
        content = await f.read()
    encoded = base64.b64encode(content).decode('utf-8')
    return {"path": path, "content": encoded}


async def list_and_slurp():
    secret_files = [entry.path for entry in os.scandir("/etc/pve/cloud/secrets") if entry.is_file()]

    tasks = [slurp_file(f) for f in secret_files]

    # also slurp the cluster automation key
    tasks.append(slurp_file("/etc/pve/cloud/automation_id_ed25519.pub"))

    return await asyncio.gather(*tasks)


def run_module():
    module_args = dict(
    )
    module = AnsibleModule(argument_spec=module_args)

    results = asyncio.run(list_and_slurp())

    result = dict(
        changed=True,
        results = results
    )

    module.exit_json(**result)


if __name__ == '__main__':
    run_module()
