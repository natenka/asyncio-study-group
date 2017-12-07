import asyncio
from pprint import pprint
from concurrent.futures import ThreadPoolExecutor
import datetime

import clitable
import yaml
import netdev


async def send_show_and_parse(loop, device_params, command):
    print('{:15}{}'.format(device_params['host'], datetime.datetime.now()))
    attributes_dict = {'Command': command,
                       'Vendor': device_params['device_type']}
    async with netdev.create(**device_params) as ssh:
        output = await ssh.send_command(command)
        parsed = await loop.run_in_executor(None, parse_command_dynamic,
                                            output, attributes_dict)
        print('{:15}{}'.format('parsed', datetime.datetime.now()))
    return parsed


def parse_command_dynamic(command_output, attributes,
                          index_file='index', templ_path='templates'):

    cli_table = clitable.CliTable(index_file, templ_path)
    cli_table.ParseCmd(command_output, attributes)
    return [dict(zip(cli_table.header, row)) for row in cli_table]


if __name__ == '__main__':
    with open('devices.yaml') as f:
        devices = yaml.load(f)

    loop = asyncio.get_event_loop()
    tasks = [asyncio.ensure_future(send_show_and_parse(loop, device, 'sh ip int br'))
             for device in devices]
    results = loop.run_until_complete(asyncio.gather(*tasks))

    #pprint(results)
    loop.close()

