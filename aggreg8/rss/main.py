#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# aggreg8.git:aggreg8/rss/main.py
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

## {{{ ---- [ Imports ] ----------------------------------------------------------------------------

import string

import dataclasses

import feedparser

from .. import (
  debug,
  func_name,
  time_now,
  A8Error,
  Dict,
)

from ..database import SqlStatement

from .errors import RssFeedError

## }}} ---- [ Imports ] ----------------------------------------------------------------------------

## {{{ ---- [ Constants ] --------------------------------------------------------------------------

_ALPHANUMERIC = string.ascii_letters + string.digits

# Valid feed name/identifier characters
VALID_NAME_CHARS = _ALPHANUMERIC + '-_'

# Valid feed proper name characters
VALID_PROPER_NAME_CHARS = _ALPHANUMERIC + "'- "

# Valid URL characters
#
# FIXME: there's surely a module exposing an infinitely better list of
# valid URL characters...
#
VALID_URL_CHARS = _ALPHANUMERIC + ':/.?-_%='

## }}} ---- [ Constants ] --------------------------------------------------------------------------

## {{{ ---- [ Functions ] --------------------------------------------------------------------------

## {{{ def parse()
def parse(str):
  return feedparser.parse(str).entries
## }}}

## }}} ---- [ Functions ] --------------------------------------------------------------------------

## {{{ ---- [ Classes ] ----------------------------------------------------------------------------

## {{{ class RssFeedSpec

@dataclasses.dataclass
class RssFeedSpec:

  name: str
  proper_name: str
  url: str

  id: int = 0
  update_interval: int = 0
  date_added: int = 0
  last_updated: int = 0
  entries: str = '[]'
  context: str = '{}'

## class RssFeedSpec }}}

## {{{ class RssFeed

class RssFeed:

  _spec = None

  ## {{{ RssFeed.__init__()
  def __init__(self, name, proper_name, url):
    if not self._valid_feed_name(name):
      raise RssFeedError(f"invalid feed name '{feed_name}'")
    if not self._valid_feed_proper_name(proper_name):
      raise RssFeedError(f"invalid feed proper name '{feed_proper_name}'")
    if not self._valid_feed_url(url):
      raise RssFeedError(f"invalid feed URL '{feed_url}'")

    self._spec = RssFeedSpec(name, proper_name, url)
  ## }}}

  def __repr__(self):
    return f"RssFeed('{self._spec.name}', '{self._spec.proper_name}', '{self._spec.url}')"

  ## {{{ RssFeed._valid_feed_name()
  def _valid_feed_name(self, name):
    # FIXME: perform proper TLV validation
    for char in name:
      if char not in VALID_NAME_CHARS:
        warning(f"invalid feed name character '{char}'")
        return False
    return True
  ## }}}

  ## {{{ RssFeed._valid_feed_proper_name()
  def _valid_feed_proper_name(self, name):
    # FIXME: perform proper TLV validation
    for char in name:
      if char not in VALID_PROPER_NAME_CHARS:
        warning(f"invalid feed proper name character '{char}'")
        return False
    return True
  ## }}}

  ## {{{ RssFeed._valid_feed_url()
  def _valid_feed_url(self, url):
    if not url.startswith('http://') and not url.startswith('https://'):
      return False

    # FIXME: perform proper TLV validation
    for char in url:
      if char not in VALID_URL_CHARS:
        warning(f"invalid feed URL character '{char}'")
        return False
    return True
  ## }}}

  def get(self, name):
    return getattr(self._spec, name)

  def set(self, name, value):
    return setattr(self._spec, name, value)

  ## {{{ [static] RssFeed.feeds()
  @staticmethod
  def feeds(dbd):
    cursor = dbd.cursor()

    sql = SqlStatement('SELECT * FROM rss_feeds')

    #debug(f"executing: {sql}")
    cursor.execute(str(sql))

    feed_list = []
    for row in cursor.execute(str(sql)):
      row = tuple(row)

      ## Columns:
      #
      # 0 = id
      # 1 = name
      # 2 = proper_name
      # 3 = url
      # 4 = update_interval
      # 5 = date_added
      # 6 = last_updated
      # 7 = entries
      # 8 = context
      #

      feed = RssFeed(row[1], row[2], row[3])

      feed.set('id', row[0])
      feed.set('update_interval', row[4])
      feed.set('date_added', row[5])
      feed.set('last_updated', row[6])
      feed.set('entries', row[7])
      feed.set('context', row[8])

      feed_list.append(feed)

    return feed_list
  ## }}}

  ## {{{ RssFeed.insert()
  def insert(self, dbd):
    cursor = dbd.cursor()

    columns = 'name, proper_name, url, date_added, last_updated'

    sql = SqlStatement(
      'INSERT',
      'INTO',
      'rss_feeds',
      f'({columns})',
      'VALUES(?, ?, ?, ?, ?)'
    )

    now = time_now()
    values = (self._spec.name, self._spec.proper_name, self._spec.url, now, now)

    #debug(f"executing: {sql}")
    cursor.execute(str(sql), values)

    dbd.commit()
  ## }}}

  def update(self, dbd):
    raise A8Error(f"method RssFeed.{func_name()}() isn't implemented yet")

  def delete(self, dbd):
    raise A8Error(f"method RssFeed.{func_name()}() isn't implemented yet")

## class RssFeed }}}

## }}} ---- [ Classes ] ----------------------------------------------------------------------------

##
# vim: ts=2 sw=2 tw=100 et fdm=marker :
##
