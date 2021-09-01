#!/bin/bash

source /usr/local/lib/functions.bash || exit 1

type -P realpath >/dev/null 2>&1 || die "realpath(1) not found in PATH"

INSTANCE_DIR="$(realpath "$(dirname "$0")")"
export PATH="$INSTANCE_DIR/bin:$PATH"

function a8()
{
  local a8="$(type -P a8)"
  echo -e "\n>> Executing: $a8" "$@"
  set -- "$a8" "$@"
  "$@"
  return $?
}

# Clear the screen
clear

a8 init -f || die 'a8 init failed'

a8 rss add aljazeera 'Al Jazeera' 'https://www.aljazeera.com/xml/rss/all.xml' \
  || die 'a8 rss add failed'

a8 rss add bbcnews 'BBC News' 'http://feeds.bbci.co.uk/news/rss.xml' \
  || die 'a8 rss add failed'

#a8 rss list

a8 rss poll

##
# vim: ts=2 sw=2 tw=100 et fdm=marker :
##
