#!/bin/sh
# Author: Jan Vcelak <jvcelak@redhat.com>

. /usr/libexec/openldap/functions

function help()
{
	error "usage: %s [-f config-file] [-F config-dir]\n" "`basename $0`"
	exit 2
}

load_sysconfig

while getopts :f:F: opt; do
	case "$opt" in
	f)
		SLAPD_CONFIG_FILE="$OPTARG"
		;;
	F)
		SLAPD_CONFIG_DIR="$OPTARG"
		;;
	*)
		help
		;;
	esac
done
shift $((OPTIND-1))
[ -n "$1" ] && help

# check source, target

if [ ! -f "$SLAPD_CONFIG_FILE" ]; then
	error "Source configuration file '%s' not found." "$SLAPD_CONFIG_FILE"
	exit 1
fi

if grep -iq '^dn: cn=config$' "$SLAPD_CONFIG_FILE"; then
	SLAPD_CONFIG_FILE_FORMAT=ldif
else
	SLAPD_CONFIG_FILE_FORMAT=conf
fi

if [ -d "$SLAPD_CONFIG_DIR" ]; then
	if [ `find "$SLAPD_CONFIG_DIR" -maxdepth 0 -empty | wc -l` -eq 0 ]; then
		error "Target configuration directory '%s' is not empty." "$SLAPD_CONFIG_DIR"
		exit 1
	fi
fi

# perform the conversion

tmp_convert=`mktemp`

if [ `id -u` -eq 0 ]; then
	install -d --owner $SLAPD_USER --group `id -g $SLAPD_USER` --mode 0700 "$SLAPD_CONFIG_DIR" &>>$tmp_convert
	if [ $SLAPD_CONFIG_FILE_FORMAT = ldif ]; then
		run_as_ldap "/usr/sbin/slapadd -F \"$SLAPD_CONFIG_DIR\" -n 0 -l \"$SLAPD_CONFIG_FILE\"" &>>$tmp_convert
	else
		run_as_ldap "/usr/sbin/slaptest -f \"$SLAPD_CONFIG_FILE\" -F \"$SLAPD_CONFIG_DIR\"" &>>$tmp_convert
	fi
	retcode=$?
else
	error "You are not root! Permission will not be set."
	install -d --mode 0700 "$SLAPD_CONFIG_DIR" &>>$tmp_convert
	if [ $SLAPD_CONFIG_FILE_FORMAT = ldif ]; then
		/usr/sbin/slapadd -F "$SLAPD_CONFIG_DIR" -n 0 -l "$SLAPD_CONFIG_FILE" &>>$tmp_convert
	else
		/usr/sbin/slaptest -f "$SLAPD_CONFIG_FILE" -F "$SLAPD_CONFIG_DIR" &>>$tmp_convert
	fi
	retcode=$?
fi

if [ $retcode -ne 0 ]; then
	error "Configuration conversion failed:"
	cat $tmp_convert >&2
fi

rm $tmp_convert
exit $retcode
