#!/bin/sh

/usr/lib/rpm/find-requires $* | grep -v 'perl(w3mhelp-'
