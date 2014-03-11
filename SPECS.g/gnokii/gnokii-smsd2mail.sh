#!/bin/sh
TO=root@localhost
( echo From: $1 ; echo Date: $2 ; echo ; cat ) | mail -s "SMS from $1" $TO
