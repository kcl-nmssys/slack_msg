#!/usr/bin/env python3

import argparse
import os
import platform
import requests
import sys
import yaml

options = ['url', 'channel', 'username', 'icon']
config_file = '/etc/slack_msg.yaml'

config = {
    'username': platform.node(),
    'icon': 'robot_face'
}

if os.path.exists(config_file):
    try:
        with open(config_file) as fh:
            config = yaml.load(fh, Loader=yaml.SafeLoader)
    except Exception as e:
        sys.stderr.write('Failed to load %s: %s\n' % (config_file, e))
        sys.exit(1)

parser = argparse.ArgumentParser()
parser.add_argument('--message', required=True)
for option in options:
    parser.add_argument('--%s' % option)

args = vars(parser.parse_args())
for option in options:
    if args[option] is not None:
        config[option] = args[option]

    if option not in config:
        sys.stderr.write('Missing setting: %s\n' % option)
        sys.exit(1)

payload = {
    'channel': config['channel'],
    'username': config['username'],
    'icon_emoji': ':%s:' % config['icon'],
    'text': args['message']
}

requests.post(config['url'], json=payload)
