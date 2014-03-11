#!/bin/sh

/usr/lib/rpm/find-provides $* | egrep -v 'perl\(Automake' | sort -u
