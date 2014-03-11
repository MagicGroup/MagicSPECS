#!/bin/sh
# Munge Perl requirements:
# - remove dependency on DCOP
/usr/lib/rpm/perl.req $* | 
sed -e '/perl(DCOP)/d'
