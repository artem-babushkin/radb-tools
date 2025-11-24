#!/usr/bin/env bash
cd "$(dirname $0)"
if [[ $RADBKEEPCACHE == 0 ]]; then
  printf 'Clear cache\n'
  rm -rf cache
  #rm -f rib*.bz2
fi
mkdir -p cache && cd cache
if [[ ! -f asn.txt ]]; then
  printf 'Download ASN names\n'
  curl -O -L https://ftp.ripe.net/ripe/asnames/asn.txt || exit 1
fi
if [[ ! -f ipasn.lst ]]; then
  printf 'Download RIB\n'
  timeout 600 pyasn_util_download.py --latest || exit 1
  printf 'Convert RIB\n'
  pyasn_util_convert.py --single $(find . -maxdepth 1 -name "rib*.bz2" -print0) ipasn.lst
fi
cd ..
printf 'Filter RIB\n'
./filter.py config.yaml
