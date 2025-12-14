#!/usr/bin/env python3
from sys import argv
import yaml
import re
import os
import pyasn
from aggregate_prefixes import aggregate_prefixes
import logging
logger = logging.getLogger(__name__)
#logging.basicConfig(level = logging.DEBUG)
logger.setLevel(logging.DEBUG)

try:
    with open(argv[1], 'r') as f:
        CONFIG = yaml.safe_load(f)
    logger.info(f'Config loaded from {argv[1]}')
except Exception as ex:
    text = f'Failed to load config file. {ex}'
    logger.error(text)
    raise Exception(f'{text}\nUsage: {argv[0]} path-to-config-file.yaml\n\n')

logger.debug(f'{CONFIG}')

def main():
    # head ipasn.lst  (asn-db)
    #1.0.6.0/24	38803
    #
    # head asn.txt    (asnames) 
    #0 -Reserved AS-, ZZ
    #1 LVLT-1, US

    workdir = os.path.dirname(os.path.abspath(argv[0]))
    all_ip_asn = pyasn.pyasn(f'{workdir}/{CONFIG["asn-db"]}')
    with open(f'{workdir}/{CONFIG["result-file"]}', 'w') as out, open(f'{workdir}/{CONFIG["asnames-file"]}') as all_as_names:
        target_prefixes = []
        target_asnumbers = [CONFIG['asn']]
        asname_regex_patterns = [re.compile(i) for i in CONFIG['as-name-regex']]
        logger.debug('Parse AS names file')
        as_name_parser = re.compile(r'^(\d+) (.+), (\S+)$')
        for line in all_as_names:
            try:
                asnumber, asname, ascountry = as_name_parser.findall(line)[0]
                for country in CONFIG['country']:
                    if country.lower() == ascountry.strip().lower():
                        logger.debug(f'Country {country} match. AS name: {asname}')
                        target_asnumbers += asnumber
                for pattern in asname_regex_patterns:
                    if pattern.match(asname.lower()):
                        logger.debug(f'AS name regex {pattern.pattern} match. AS name: {asname}')
                        target_asnumbers += asnumber
            except Exception as ex:
                logger.warning(f'Failed to parse AS names file line {line.strip()}. {ex}. ')
        logger.info(f'Found {len(target_asnumbers)} AS numbers')
        for asn in target_asnumbers:
            logging.debug(f'{Processing AS number {asn}')
            try:
                target_prefixes.extend(list(all_ip_asn.get_as_prefixes(asn)))
                logger.debug(f'Add ASN {asn} to target')
            except Exception as ex:
                logger.warning(f'Failed to add prefixes from AS {asn} to target. {ex}')
        number_of_prefixes = 0
        for prefix in list(aggregate_prefixes(target_prefixes)):
        #for prefix in list(target_prefixes):
            #number_of_prefixes += line.num_addresses
            number_of_prefixes += 1
            out.write(f'{prefix}\n')
            #print(str(line), file=out)
        for prefix in CONFIG['prefix']:
            number_of_prefixes += 1
            out.write(f'{prefix}\n')
            #print(prefix, file=out)
    logger.info(f'Found {number_of_prefixes} prefixes')



if __name__=='__main__':
    main()
