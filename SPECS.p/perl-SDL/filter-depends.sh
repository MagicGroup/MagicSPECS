#!/bin/sh
/usr/lib/rpm/redhat/find-requires "$@" | grep -v Pod::ToDemo
