import asyncio
import netdev
import yaml
from pprint import pprint


async def send_show_commands_to_cisco(device_params, commands):
    results = {device_params['host']: {}}
    async with netdev.create(**device_params) as ssh:
        for command in commands:
            output = await ssh.send_command(command)
            results[device_params['host']][command] = output
    return results


async def send_cfg_commands_to_cisco(device_params, commands):
    results = {}
    async with netdev.create(**device_params) as ssh:
        output = await ssh.send_config_set(commands)
        results[device_params['host']] = output
    return results


async def run(devices, show_commands=None, cfg_commands=None):
    tasks = []
    if show_commands:
        tasks += [send_show_commands_to_cisco(device, show_commands)
                  for device in devices]
    if cfg_commands:
        tasks += [send_cfg_commands_to_cisco(device, cfg_commands)
                  for device in devices]
    result = await asyncio.gather(*tasks)
    return result


if __name__ == '__main__':
    with open('devices.yaml') as f:
        devices = yaml.load(f)
    sh_commands = ['show clock', 'sh ip arp', 'sh ip int br']
    cfg_commands = ['ip access-list extended TEST','permit ip any any']

    loop = asyncio.get_event_loop()
    all_results = loop.run_until_complete(run(devices['routers'], sh_commands))
    #pprint(all_results)

    #all_cfg_results = loop.run_until_complete(run(devices['routers'],
    #                                              cfg_commands=cfg_commands))
    #pprint(all_cfg_results)
    loop.close()

