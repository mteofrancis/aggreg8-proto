#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

# Path to aggreg8 instance directory
A8_INSTANCE_DIR = os.path.abspath(os.path.dirname(__file__))

# Top-level instance directories
A8_BIN_DIR = os.path.join(A8_INSTANCE_DIR, 'bin')
A8_DATA_DIR = os.path.join(A8_INSTANCE_DIR, 'data')

# Database driver
A8_DATABASE_DRIVER = 'sqlite'

# Path to SQLite database file
A8_SQLITE_DATABASE = os.path.join(A8_DATA_DIR, 'aggreg8.sqlite')

##
# vim: ts=2 sw=2 tw=100 et fdm=marker :
##
