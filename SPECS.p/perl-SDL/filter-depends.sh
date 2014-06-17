#!/bin/sh
/usr/lib/rpm/magic/find-requires "$@" | grep -v Pod::ToDemo
