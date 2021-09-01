CREATE TABLE IF NOT EXISTS rss_feeds
(
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL UNIQUE,
  proper_name TEXT NOT NULL,
  url TEXT NOT NULL UNIQUE,
  update_interval INTEGER DEFAULT 60,
  date_added INTEGER NOT NULL,
  last_updated INTEGER NOT NULL,

  -- JSON payloads
  entries TEXT NOT NULL DEFAULT '[]',
  context TEXT NOT NULL DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS rss_feed_cache
(
  id INTEGER PRIMARY KEY,
  feed_id INTEGER NOT NULL UNIQUE,
  url TEXT NOT NULL UNIQUE,
  date_added INTEGER NOT NULL,
  last_updated INTEGER NOT NULL,
  content TEXT NOT NULL,
  content_hash TEXT NOT NULL
);

/*

CREATE TABLE IF NOT EXISTS log_domains
(
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS logs
(
  id INTEGER PRIMARY KEY,
  domain INTEGER NOT NULL,
  time_stamp INTEGER NOT NULL,
  entry TEXT NOT NULL,
  entry_hash TEXT NOT NULL,

  -- JSON payloads
  context TEXT NOT NULL DEFAULT ''
);

*/

--
-- vim: ts=2 sw=2 tw=100 et fdm=marker :
--
