#!/bin/sh
/usr/lib/rpm/redhat/find-provides "$@" | \
  grep -vE 'perl\(Walker\)|\.so'
