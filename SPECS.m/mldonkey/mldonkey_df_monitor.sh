#!/bin/sh

CACHEDIR="/var/cache/mldonkey"
MINFREE=102400
EMAIL="root@localhost"

. /etc/sysconfig/mldonkey

[ ! "$ENABLE_DF_MONITOR" = "yes" ] && exit

send_email() {
	mail -s "mldonkey, disk space warning" $EMAIL << EOF

your $CACHEDIR has only $CURFREE KiB free space left
all downloads paused

BTW: you can control this check by editing /etc/sysconfig/mldonkey.
EOF
}


CURFREE=`df -P -k $CACHEDIR | tail -n 1 | awk '{ print $4 }'`
if [ $CURFREE -lt $MINFREE ] ; then
	/etc/init.d/mldonkey pause > /dev/null
	send_email
fi

