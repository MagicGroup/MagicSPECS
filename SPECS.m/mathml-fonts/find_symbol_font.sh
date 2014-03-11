#!/bin/bash
# $Id: find_symbol_font.sh,v 1.3 2005/09/15 19:37:56 rdieter Exp $

if [ -f /etc/sysconfig/mathml-fonts ]; then
 source /etc/sysconfig/mathml-fonts
fi

fontdir=${MATHML_FONTS_DIR:-/usr/share/fonts/mathml}

while true
do
  case "$1" in
  -v|--verbose) VERBOSE=1 
  ;;
  -?*)
    echo "Usage: `basename $0` [-v|--verbose] [acrobat_home_dir]" 1>&2
    exit 1
  ;;
  *)  break ;;
  esac
  shift
done

find_font() {
DIR=$1
SRC=$2
DST=${3:-${SRC}}

if [ -e $DIR/Resource/Font/$SRC ] ; then
  [ ! -z "$VERBOSE" ] && echo "Found $DIR/Resource/Font/$SRC"

  if [ -e ${fontdir}/$DST ]; then
    [ ! -z "$VERBOSE" ] && echo "${fontdir}/$DST valid symlink already exists."
  else
    ln -s $DIR/Resource/Font/$SRC ${fontdir}/$DST  ||:
    fc-cache -f ${fontdir} ||:
  fi
fi
}

for acrordr_home in ${@:-/usr/lib/acroread /usr/local/Adobe/Acrobat7.0 /usr/local/Acrobat5} ; do

  find_font $acrordr_home SY______.PFB
  find_font $acrordr_home Symbol Symbol.pfa

done

