#!/usr/bin/perl -w
#===============================================================================
#
#         FILE: lastmod.pl
#
#        USAGE: lastmod.pl url
#
#  DESCRIPTION: Fetch an HTTP URL's HEAD and dump its Last-Modified field in
#               local time format (e.g. seconds since the epoch).
#
#      OPTIONS: none
# REQUIREMENTS: File::Basename, Net::HTTP, URI, HTTP::Headers
#         BUGS: unknown
#        NOTES: none
#       AUTHOR: Philip Prindeville <philipp@fedoraproject.org>
# ORGANIZATION: Fedora Project
#      VERSION: 1.0
#      CREATED: 08/06/2013 12:52:32 PM
#     REVISION: 0
#===============================================================================

use strict;
use warnings;

use File::Basename;
use Net::HTTP;
use URI;
use HTTP::Headers;

if (@ARGV != 1) {
    die "usage: " . basename($0) . " url\n";
}

my $uri = URI->new($ARGV[0]) || die "Couldn't parse URL\n";

die "Not an HTTP URL\n" unless ($uri->scheme eq 'http');

my $host = $uri->host() || die "No host in URL\n";

my $s = Net::HTTP->new(Host => $host) || die "Can't construct Net::HTTP object\n";

$s->write_request(HEAD => $uri->as_string()) || die "Can't send HEAD request\n";

my ($code, $mess, %h) = $s->read_response_headers;

if ($code ne '200') {
    die "Response: " . $code . ": " . $mess . "\n";
}

my $h = HTTP::Headers->new(%h) || die "Couldn't parse headers\n";

print $h->last_modified(), "\n";

exit 0;

# vim:ts=4
