import yaml
from pprint import pprint
from concurrent.futures import ThreadPoolExecutor, as_completed

from netmiko import ConnectHandler


def send_show_commands_to_cisco(device_params, commands):
    results = {device_params['ip']: {}}
    with ConnectHandler(**device_params) as ssh:
        for command in commands:
            ssh.enable()
            output = ssh.send_command(command)
            results[device_params['ip']][command] = output
    return results


def send_cfg_commands_to_cisco(device_params, commands):
    results = {}
    with ConnectHandler(**device_params) as ssh:
        ssh.enable()
        output = ssh.send_config_set(commands)
        results[device_params['ip']] = output
    return results


def run(devices, show_commands=None, cfg_commands=None, threads=8):
    futures = []
    with ThreadPoolExecutor(max_workers=threads) as executor:
        if show_commands:
            futures += [executor.submit(send_show_commands_to_cisco,
                                        device, show_commands)
                        for device in devices]
        if cfg_commands:
            futures += [executor.submit(send_cfg_commands_to_cisco,
                                        device, cfg_commands)
                        for device in devices]
        results = [f.result() for f in as_completed(futures)]
    return results


if __name__ == '__main__':
    with open('devices_netmiko.yaml') as f:
        devices = yaml.load(f)
    sh_commands = ['show clock', 'sh ip arp', 'sh ip int br']
    cfg_commands = ['ip access-list extended TEST','permit ip any any']

    all_results = run(devices['routers'], sh_commands)
    pprint(all_results)

    #all_cfg_results = run(devices['routers'], cfg_commands=cfg_commands)
    #pprint(all_cfg_results)

