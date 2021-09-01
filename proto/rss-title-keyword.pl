#!/usr/bin/env perl

use strict;
use warnings;

use DBI;
use JSON;

use Date::Parse;

use Data::Dumper;

## {{{ ---- [ Constants ] --------------------------------------------------------------------------

use constant PROG_NAME => substr($0, index($0, '/') + 1);

use constant STATUS_WINDOW => '(status)';
use constant MAIN_WINDOW   => '(monitor)';
use constant DEBUG_WINDOW  => '(debug)';

use constant DB_DRIVER   => 'SQLite';
use constant DB_NAME     => 'data/aggreg8.sqlite';
use constant DB_USERNAME => '';
use constant DB_PASSWORD => '';

## }}} ---- [ Constants ] --------------------------------------------------------------------------

## {{{ ---- [ Subroutines ] ------------------------------------------------------------------------

## {{{ debug($message)
#
# Print $message to debug window

sub debug
{
  my $message = shift @_;
  print STDERR sprintf "%s: debug: %s\n", $message;
}

## }}}

## {{{ warning($message)
#
# Print warning $message to status window

sub warning
{
  my $message = shift @_;
  print STDERR sprintf "%s: warning: %s\n", $message;
}

## }}}

## {{{ error($message)
#
# Print error $message to status window

sub error
{
  my $message = shift @_;
  print STDERR sprintf "%s: error: %s\n", $message;
}

## }}}

## {{{ db_connect()
sub db_connect
{
  my $dsn = sprintf 'DBI:%s:dbname=%s', DB_DRIVER, DB_NAME;
  my $dbh = DBI->connect($dsn, DB_USERNAME, DB_PASSWORD, {RaiseError => 1, AutoCommit => 1})
    or die "Failed to connect to database: $dsn: " . $DBI::errstr;

  return $dbh;
}
## }}}

## {{{ db_init($db)
sub db_init
{
  my $db = shift @_;

  my $sql =
    "CREATE TABLE IF NOT EXISTS messages ("
    . "id INTEGER PRIMARY KEY,"
    . "message TEXT NOT NULL,"
    . "processed BOOLEAN DEFAULT FALSE,"
    . "timestamp DATE NOT NULL DEFAULT CURRENT_TIMESTAMP"
    . ")";

  my $sth;
  $sth = $db->prepare($sql) or die "Init prepare() failed: " . $sth->err;
  $sth->execute() or die "Init execute() failed: " . $sth->err;
}
## }}}

## {{{ db_disconnect($db)
sub db_disconnect
{
  my $db = shift @_;

  $db->disconnect();
}
## }}}

## }}} ---- [ Subroutines ] ------------------------------------------------------------------------

# SQLite database handle
my $dbh = undef;

# Check we've been given the one argument we require
unless ($#ARGV != 2)
{
  print STDERR sprintf "Usage: %s <feed> <keyword>\n", PROG_NAME;
  exit 1;
}

# Feed to look up
my $feed = $ARGV[0];
my $keyword = $ARGV[1];
my $entries = undef;

# Open SQLite database file
$dbh = db_connect();

my $sql =
  "SELECT "
  . "entries "
  . "FROM "
  . "rss_feeds "
  . "WHERE "
  . "name=?";

my $sth = $dbh->prepare($sql) or die "dbh->prepare failed: $DBI::errstr";
$sth->execute($feed) or die "sth->execute failed: $DBI::errstr";

while (my $row = $sth->fetchrow_hashref())
{
  $entries = $row->{entries};
  next;
}

unless (defined $entries)
{
  error(sprintf "feed '%s' not found", $feed);
  exit 1;
}

my $results = [];

for my $entry (@{decode_json($entries)})
{
  next unless $entry->{title} =~ /$keyword/i;

  push @{$results}, {
    id => $entry->{id},
    link => $entry->{link},
    title => $entry->{title},
  };
}

my $num_results = scalar @{$results};
unless ($num_results > 0)
{
  error(sprintf "feed '%s' doesn't contain any entries with word '%s'", $feed, $keyword);
  exit 1;
}

print sprintf "Found %d result(s)\n", $num_results;
for my $result (@{$results})
{
  printf "Title: %s\n", $result->{title};
  printf "Link: %s\n", $result->{link};
}

exit 0;

##
# vim: ts=2 sw=2 tw=100 et fdm=marker :
##
