#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# aggreg8.git:aggreg8/database/main.py
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

import sqlite3

from .errors import DatabaseError

## {{{ ---- [ Functions ] --------------------------------------------------------------------------

## {{{ factory()
def factory(driver):
  if driver == 'sqlite':
    return SqliteDatabase()
  else:
    raise DatabaseError(f"invalid database driver '{driver}'")
## }}}

## }}} ---- [ Functions ] --------------------------------------------------------------------------

## {{{ ---- [ Classes ] ----------------------------------------------------------------------------

## {{{ class Database

class Database:

  """Base class for Aggreg8's database drivers"""

  _con = None

## class Database }}}

## {{{ class SqliteDatabase

class SqliteDatabase(Database):

  def connect(self, path):
    # Create database file if it doesn't exist
    fd = os.open(path, os.O_RDONLY | os.O_CREAT, 0o600)
    os.close(fd)

    # Ensure the file mode is secore, zeroing group/other mode bits
    #
    # FIXME: this should be configurable
    #
    os.chmod(path, 0o600)

    # Open the database file
    #
    try:
      self._con = sqlite3.connect(path)
    except sqlite3.DatabaseError as ex:
      raise DatabaseError(ex, f'{path}: sqlite3.connect() failed')

    # Finally, set the connection's row factory
    self._con.row_factory = sqlite3.Row

  def cursor(self):
    try:
      return self._con.cursor()
    except sqlite3.DatabaseError as ex:
      raise DatabaseError(ex, f'sqlite3.Connection.cursor() failed')

  def commit(self):
    try:
      self._con.commit()
    except sqlite3.DatabaseError as ex:
      raise DatabaseError(ex, f'sqlite3.Connection.commit() failed')

  def rollback(self):
    try:
      return self._con.rollback()
    except sqlite3.DatabaseError as ex:
      raise DatabaseError(ex, f'sqlite3.Connection.rollback() failed')

  def close(self):
    # Automatically commit on close
    try:
      self._con.commit()
    except sqlite3.DatabaseError as ex:
      raise DatabaseError(ex, f'sqlite3.Connection.commit() failed')

    try:
      self._con.close()
    except sqlite3.DatabaseError as ex:
      raise DatabaseError(ex, f'sqlite3.Connection.close() failed')

  def execute(self, sql, parameters=None):
    try:
      if parameters is None:
        return self._con.execute(sql)
      else:
        return self._con.execute(sql, parameters)
    except sqlite3.DatabaseError as ex:
      raise DatabaseError(ex, f'sqlite3.Connection.execute() failed')

  def executemany(self, sql, parameters=None):
    try:
      if parameters is None:
        return self._con.executemany(sql)
      else:
        return self._con.executemany(sql, parameters)
    except sqlite3.DatabaseError as ex:
      raise DatabaseError(ex, f'sqlite3.Connection.executemany() failed')

  def executescript(self, str):
    try:
      return self._con.executescript(str)
    except sqlite3.DatabaseError as ex:
      raise DatabaseError(ex, f'sqlite3.Connection.executescript() failed')

## class SqliteDatabase }}}

## {{{ class SqlStatement

class SqlStatement():

  _sql = None
  _sep = None

  def __init__(self, *args, sep=' '):
    self._sep = sep
    self._sql = []
    for arg in args:
      self._sql.append(arg)

  def __str__(self):
    return self._sep.join(self._sql)

## class SqliteDatabase }}}

## }}} ---- [ Classes ] ----------------------------------------------------------------------------

##
# vim: ts=2 sw=2 tw=100 et fdm=marker :
##
