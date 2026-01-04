import asyncio

from ansible.utils.display import Display

display = Display()


# determine online pve hosts
async def check_host_ssh_online(pve_host):
    try:
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(pve_host.params["ansible_host"], 22), timeout=1
        )
        writer.close()
        await writer.wait_closed()

        return True, pve_host
    except (asyncio.TimeoutError, OSError, ConnectionRefusedError) as e:
        display.v(f"Error checking host online {e} {type(e)}")
        return False, pve_host


# waits for ssh to come up (for containers / vms in creating)
async def wait_for_ssh_open(ip):
    retries = 0
    max_retries = 30
    ports = (2222, 22)  # test custom port first

    while retries < max_retries:
        for ssh_port in ports:
            try:
                reader, writer = await asyncio.wait_for(
                    asyncio.open_connection(ip, ssh_port), timeout=1
                )
                writer.close()
                await writer.wait_closed()
                display.v(f"SSH is open on {ip}:{ssh_port}")
                return ssh_port
            except (asyncio.TimeoutError, OSError, ConnectionRefusedError) as e:
                display.v(f"Error waiting for ssh {e} {type(e)}")
                retries += 1
                await asyncio.sleep(1)

    return None
