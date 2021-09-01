#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import requests

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/..'))

from aggreg8 import *

if len(sys.argv) != 2:
  perr(f"Usage: {PROG_NAME} <url>")
  exit(1)

url = sys.argv[1]
if not url.startswith('http://') and not url.startswith('https://'):
  die(f"invalid URL '{url}': valid URLs start with http[s]://")
elif not url.split('://')[1]:
  die(f"invalid URL '{url}': missing server name")

pout(f'HEAD {url}')
response = requests.head(url)
for header, value in response.headers.items():
  pout(f'{header}: {value}')

##
# vim: ts=2 sw=2 tw=100 et fdm=marker :
##
