#!/bin/sh

if [ ! -f /etc/nxserver/users.id_dsa ] ; then
    logger -s -p daemon.err -t freenx-server.service \
        'FreeNX server not set up, run "nxsetup --install"'
    exit 6
fi
