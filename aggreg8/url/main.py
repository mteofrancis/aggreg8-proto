#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# aggreg8.git:aggreg8/url/main.py
##

## {{{ ---- [ Header ] -----------------------------------------------------------------------------

##
# Copyright (c) 2021 Francis M <francism@destinatech.com>
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2.0 as published by the
# Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to:
#
#   Free Software Foundation
#   51 Franklin Street, Fifth Floor
#   Boston, MA 02110
#   USA
##

## }}} ---- [ Header ] -----------------------------------------------------------------------------

import urllib.request

import gzip

import hashlib

from .errors import UrlRequestError

## {{{ class UrlRequest

class UrlRequest:

  url = None

  request = None
  request_headers = None

  response = None
  response_headers = None

  status = None

  content = None
  content_hash_alg = None
  content_hash = None

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

    self.content_hash_alg = 'sha256'
    self.content_hash = hashlib.sha256(self.content).hexdigest()

    # Finally, convert self.content to UTF-8
    self.content = self.content.decode('utf-8')

## class UrlRequest }}}

##
# vim: ts=2 sw=2 tw=100 et fdm=marker :
##
