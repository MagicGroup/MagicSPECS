#!/bin/bash

. /etc/rc.d/init.d/functions

# This script generates /etc/rndc.key if doesn't exist AND if there is no rndc.conf

if [ ! -s /etc/rndc.key -a ! -s /etc/rndc.conf ]; then
  echo -n $"Generating /etc/rndc.key:"
  if /usr/sbin/rndc-confgen -a > /dev/null 2>&1; then
    chmod 640 /etc/rndc.key
    chown root.named /etc/rndc.key
    [ -x /sbin/restorecon ] && /sbin/restorecon /etc/rndc.key
    success $"/etc/rndc.key generation"
    echo
  else
    failure $"/etc/rndc.key generation"
    echo
  fi
fi
