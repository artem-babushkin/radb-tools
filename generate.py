#!/usr/bin/env python3
from sys import argv
import yaml

try:
    with open(argv[1], 'r') as f:
        cfg = yaml.save_load(f)
except Exception as ex:
    print(f'Failed to load config file.\nUsage: {argv[0]} path-to-config-file.yaml\n\n')
    raise ex


