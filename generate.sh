#!/usr/bin/env bash
cd "$(dirname $0)"
printf 'Clear old archive\n'
rm -f rib*.bz2
printf 'Download ASN names\n'
timeout 60 curl -O -L https://ftp.ripe.net/ripe/asnames/asn.txt || exit 1
printf 'Download RIB\n'
timeout 60 pyasn_util_download.py --latest
printf 'Convert RIB\n'
pyasn_util_convert.py --single $(find . -maxdepth 1 -name "rib*.bz2" -print0) ipasn.lst
printf 'Filter RIB\n'
./filter.py config.yaml
