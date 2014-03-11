#!/bin/bash
# Author: Jan Vcelak <jvcelak@redhat.com>

set -e

# default options

CERTDB_DIR=/etc/openldap/certs
CERT_NAME="OpenLDAP Server"
PASSWORD_FILE=
HOSTNAME_FQDN="$(hostname --fqdn)"
ALT_NAMES=
ONCE=0

# internals

RANDOM_SOURCE=/dev/urandom
CERT_RANDOM_BYTES=256
CERT_KEY_TYPE=rsa
CERT_KEY_SIZE=1024
CERT_VALID_MONTHS=12

# parse arguments

usage() {
	printf "usage: generate-server-cert.sh [-d certdb-dir] [-n cert-name]\n" >&2
	printf "                               [-p password-file] [-h hostnames]\n" >&2
	pritnf "                               [-a dns-alt-names] [-o]\n" >&2
	exit 1
}

while getopts "d:n:p:h:a:o" opt; do
	case "$opt" in
	d)
		CERTDB_DIR="$OPTARG"
		;;
	n)
		CERT_NAME="$OPTARG"
		;;
	p)
		PASSWORD_FILE="$OPTARG"
		;;
	h)
		HOSTNAME_FQDN="$OPTARG"
		;;
	a)
		ALT_NAMES="$OPTARG"
		;;
	o)
		ONCE=1
		;;
	\?)
		usage
		;;
	esac
done

[ "$OPTIND" -le "$#" ] && usage

# generated options

ONCE_FILE="$CERTDB_DIR/.slapd-leave"
PASSWORD_FILE="${PASSWORD_FILE:-${CERTDB_DIR}/password}"
ALT_NAMES="${ALT_NAMES:-${HOSTNAME_FQDN},localhost,localhost.localdomain}"

# verify target location

if [ "$ONCE" -eq 1 -a -f "$ONCE_FILE" ]; then
	printf "Skipping certificate generating, '%s' exists.\n" "$ONCE_FILE" >&2
	exit 0
fi

if ! certutil -d "$CERTDB_DIR" -U &>/dev/null; then
	printf "Directory '%s' is not a valid certificate database.\n" "$CERTDB_DIR" >&2
	exit 1
fi

printf "Creating new server certificate in '%s'.\n" "$CERTDB_DIR" >&2

if [ ! -r "$PASSWORD_FILE" ]; then
	printf "Password file '%s' is not readable.\n" "$PASSWORD_FILE" >&2
	exit 1
fi

if certutil -d "$CERTDB_DIR" -L -a -n "$CERT_NAME" &>/dev/null; then
	printf "Certificate '%s' already exists in the certificate database.\n" "$CERT_NAME" >&2
	exit 1
fi

# generate server certificate (self signed)


CERT_RANDOM=$(mktemp)
dd if=$RANDOM_SOURCE bs=$CERT_RANDOM_BYTES count=1 of=$CERT_RANDOM &>/dev/null

certutil -d "$CERTDB_DIR" -f "$PASSWORD_FILE" -z "$CERT_RANDOM" \
	-S -x -n "$CERT_NAME" \
	-s "CN=$HOSTNAME_FQDN" \
	-t TC,, \
	-k $CERT_KEY_TYPE -g $CERT_KEY_SIZE \
	-v $CERT_VALID_MONTHS \
	-8 "$ALT_NAMES" \
	&>/dev/null

rm -f $RANDOM_DATA

# tune permissions

if [ "$(id -u)" -eq 0 ]; then
	chgrp ldap "$PASSWORD_FILE"
	chmod g+r "$PASSWORD_FILE"
else
	printf "WARNING: The server requires read permissions on the password file in order to\n" >&2
	printf "         load it's private key from the certificate database.\n" >&2
fi

touch "$ONCE_FILE"
exit 0
