#!/bin/sh

/usr/lib/rpm/perl.req $* | grep -v 'perl(gtkdoc-common.pl)'
