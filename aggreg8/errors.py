#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# aggreg8.git:aggreg8/errors.py
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

## {{{ class A8Error

class A8Error(Exception):

  """Base class for all of Aggreg8's exceptions"""

  message = None

  ## {{{ Error.__init__()
  def __init__(self, message):
    self.message = message
  ## }}}

## class Error }}}

##
# vim: ts=2 sw=2 tw=100 et fdm=marker :
##
