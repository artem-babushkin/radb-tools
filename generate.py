#!/usr/bin/env python3
from sys import argv
import yaml

try:
    with open(argv[1], 'r') as f:
        cfg = yaml.safe_load(f)
except Exception as ex:
    raise Exception(f'Failed to load config file. {ex}\nUsage: {argv[0]} path-to-config-file.yaml\n\n')

cfg
