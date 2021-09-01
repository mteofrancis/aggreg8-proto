#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# aggreg8.git:aggreg8/main.py
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

import os
import sys

import time

import atexit

import collections

# Program filename
PROG_NAME = os.path.basename(sys.argv[0])

## {{{ ---- [ Functions ] --------------------------------------------------------------------------

## {{{ func_name()
def func_name(frame=1):
  return sys._getframe(frame).f_code.co_name
## }}}

## {{{ pout()
def pout(s, end='\n', flush=True):
  print(s, file=sys.stdout, end=end, flush=flush)
## }}}

## {{{ perr()
def perr(s, end='\n', flush=True):
  print(s, file=sys.stderr, end=end, flush=flush)
## }}}

## {{{ debug()
def debug(message):
  perr(f'{PROG_NAME}: debug: {func_name(2)}: {message}')
## }}}

## {{{ warning()
def warning(message):
  perr(f'{PROG_NAME}: warning: {message}')
## }}}

## {{{ error()
def error(message):
  perr(f'{PROG_NAME}: error: {message}')
## }}}

## {{{ die()
def die(message):
  error(message)
  exit(1)
## }}}

## {{{ die_internal()
def die_internal(message):
  perr(f'{PROG_NAME}: internal error: {message}')
  exit(1)
## }}}

## {{{ default_exit_handler()
def default_exit_handler(arg):
  pass
## }}}

## {{{ time_diff()
def time_diff(t1, t2):
  return t1 - t2
## }}}

## {{{ time_now()
def time_now():
  return int(time.time())
## }}}

## }}} ---- [ Functions ] --------------------------------------------------------------------------

## {{{ ---- [ Classes ] ----------------------------------------------------------------------------

## {{{ class Dict

class Dict(collections.UserDict):

  def __setattr__(self, name, value):
    super().__setattr__(name, value)

  def __getattr__(self, name):
    return super().__getattr__(name)

## class Dict }}}

## {{{ class A8Base

class A8Base:

  argv = None
  verbose = None
  quiet = None

  ## {{{ A8Base.__init__()
  def __init__(self, argv=sys.argv):
    # Duplicate argv
    self.argv = argv[:]

    # Set a restricted umask nice and early
    os.umask(0o077)

    # Be quiet by default
    self.verbose = 0
    self.quiet = True

    # Register function to be called at exit
    atexit.register(default_exit_handler, self)
  ## }}}

  ## {{{ A8Base.parse_argv()
  def parse_argv(self):
    opts = []
    args = []

    argv = self.argv[1:]
    pos = 0
    while len(argv) > 0:
      arg = argv.pop(0)
      if arg.startswith('-'):
        # Option argument
        opts.append(arg)
        continue

      # Non-option argument
      args = [arg] + argv
      break

    return opts, args
  ## }}}

  ## {{{ A8Base.check_env()
  def check_env(self):
    if 'A8_INSTANCE_DIR' not in os.environ.keys():
      die_internal('A8_INSTANCE_DIR has not been set in environment')
    elif not os.path.isfile(f"{os.environ['A8_INSTANCE_DIR']}/bin/a8"):
      die_internal('A8_INSTANCE_DIR has not been set correctly in environment')

    if 'A8_COMMAND' not in os.environ.keys():
      die_internal('A8_COMMAND has not been set in environment')

    me = os.environ['A8_COMMAND']
    if PROG_NAME.split('-')[1] != me:
      die_internal('A8_COMMAND has not been set correctly in environment')
  ## }}}

## class A8Base }}}

## }}} ---- [ Classes ] ----------------------------------------------------------------------------

##
# vim: ts=2 sw=2 tw=100 et fdm=marker :
##
