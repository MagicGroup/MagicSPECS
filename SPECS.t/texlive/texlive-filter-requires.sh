#!/bin/sh
/usr/lib/rpm/perl.req "$@" | grep -v 'perl(\(Tk\|Win32\|only\|path_tre\|just\|Htex\|Pts\|a\|Reg_macro\)'
