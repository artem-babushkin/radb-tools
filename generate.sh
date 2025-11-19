#!/usr/bin/env bash
rm -f rib*.bz2
curl -O -L https://ftp.ripe.net/ripe/asnames/asn.txt
pyasn_util_download.py --latest
pyasn_util_convert.py --single $(find . -maxdepth 1 -name "rib*.bz2" -print0) ipasn.lst
./filter.py config.yaml
