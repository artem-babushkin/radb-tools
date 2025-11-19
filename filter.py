#!/usr/bin/env python3
from sys import argv
import yaml
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level = logging.DEBUG)

try:
    with open(argv[1], 'r') as f:
        CONFIG = yaml.safe_load(f)
    logger.info(f'Config loaded from {argv[1]}')
    logger.debug(f'{CONFIG}')
except Exception as ex:
    text = f'Failed to load config file. {ex}'
    logger.error(text)
    raise Exception(f'{text}\nUsage: {argv[0]} path-to-config-file.yaml\n\n')

def main():
    print('Hi there!')


if __name__=='__main__':
    main()
