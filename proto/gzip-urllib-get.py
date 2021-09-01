#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import traceback

import urllib.request

import gzip

# Script name
SCRIPT_NAME = os.path.basename(sys.argv[0])

# Owner e-mail address
OWNER_EMAIL = 'mteofrancis@gmail.com'

# HTTP "User-Agent" string
USER_AGENT = f'Aggreg8: news aggregation bot (contact my owner via e-mail: {OWNER_EMAIL})'

## {{{ pout()
def pout(s, end='\n', flush=True):
  print(s, file=sys.stdout, end=end, flush=flush)
## }}}

## {{{ perr()
def perr(s, end='\n', flush=True):
  print(s, file=sys.stderr, end=end, flush=flush)
## }}}

## {{{ error()
def error(message):
  perr(f'{SCRIPT_NAME}: Error: {message}')
## }}}

## {{{ die()
def die(message, status=1):
  error(message)
  exit(status)
## }}}

## {{{ die_stack()
def die_stack():
  etype, ex, tb = sys.exc_info()
  error(f'unhandled {etype.__name__} exception:\n')
  traceback.print_exception(etype, ex, tb, file=sys.stderr)
  exit(1)
## }}}

## {{{ class UrlRequestError

class UrlRequestError(Exception):

  message = None

  def __init__(self, message):
    self.message = message

## class UrlRequestError }}}

## {{{ class UrlRequest

class UrlRequest:

  url = None

  request = None
  request_headers = None

  response = None
  response_headers = None

  status = None

  content = None

  gzip = False
  deflate = False

  def __init__(self, url, headers=None):
    self.url = url

    if headers is None:
      self.request = urllib.request.Request(url)
    else:
      self.request_headers = headers
      self.request = urllib.request.Request(url, headers=headers)

    self.response = urllib.request.urlopen(self.request)
    self.status = self.response.status

    self.response_headers = {}
    for header, value in self.response.getheaders():
      self.response_headers[header] = value

    encoding = self.response.info().get('Content-Encoding')
    if encoding not in ['gzip', 'deflate']:
      raise UrlRequestError((f"unexpected content-encoding type '{encoding}'"))

    if encoding == 'gzip':
      self.content = gzip.decompress(self.response.read())
      self.gzip = True
    elif encoding == 'deflate':
      self.deflate = True
      self.content = self.response.read()
    else:
      self.content = self.response.read()

## class UrlRequest }}}

if len(sys.argv) != 2 or not sys.argv[1]:
  print(f'Usage: {os.path.basename(sys.argv[0])} <url>')
  exit(1)

url = sys.argv[1]
if not url.startswith('http://') and not url.startswith('https://'):
  die(f'invalid URL: {url}')

headers = {
  'Accept-Encoding': 'gzip, deflate',
  'User-Agent': USER_AGENT,
}

try:
  u = UrlRequest(url, headers=headers)

  perr(f'URL {u.url}')
  perr(f'Status: {u.status}')

  for header, value in u.response_headers.items():
    perr(f'{header}: {value}')
  perr('')

  pout(u.content.decode('utf-8'))
except:
  die_stack()

exit(0)

##
# vim: ts=2 sw=2 tw=100 et fdm=marker :
##
