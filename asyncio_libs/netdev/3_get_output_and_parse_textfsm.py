import asyncio
from pprint import pprint
from concurrent.futures import ThreadPoolExecutor

import clitable
import yaml
import netdev

#https://stackoverflow.com/questions/44345139/python-asyncio-add-done-callback-with-async-def

async def send_show_commands_to_cisco(device_params, command):
    async with netdev.create(**device_params) as ssh:
        output = await ssh.send_command(command)
    return device_params, command, output


def parse_command_dynamic(command_output, attributes,
                          index_file='index', templ_path='templates'):

    cli_table = clitable.CliTable(index_file, templ_path)
    cli_table.ParseCmd(command_output, attributes)
    return [dict(zip(cli_table.header, row)) for row in cli_table]


def textfsm_callback(future):
    params, command, output = future.result()
    attributes_dict = {'Command': command, 'Vendor': params['device_type']}
    result = parse_command_dynamic(output, attributes_dict)
    print('Done')
    return result


async def run(devices, show_commands):
    tasks = []
    for device in devices:
        task = asyncio.ensure_future(send_show_commands_to_cisco(device, show_commands))
        task.add_done_callback(textfsm_callback)
        tasks.append(task)
    result = await asyncio.gather(*tasks)
    return result


if __name__ == '__main__':
    with open('devices.yaml') as f:
        devices = yaml.load(f)

    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(run(devices, 'sh ip int br'))
    pprint(results)
    loop.close()

