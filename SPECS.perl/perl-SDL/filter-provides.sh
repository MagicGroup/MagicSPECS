#!/bin/sh
/usr/lib/rpm/magic/find-provides "$@" | \
  grep -vE 'perl\(Walker\)|\.so'
