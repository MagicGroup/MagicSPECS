#!/bin/sh
set -e

if test -z $1
then
  echo "usage: $0 <input-tarball>"
  exit
fi

ORIGDIR=`pwd`
WORKDIR=nss_ecc_strip_working_dir
EXTENSION=`echo $1 | sed -r 's#^(.*)(.tar.bz2|.tbz2|.tar.gz|.tgz)$#\2#'`
BASE=`echo $1 | sed -r 's#^(.*)(.tar.bz2|.tbz2|.tar.gz|.tgz)$#\1#'`
COMPRESS=""

if test "x$EXTENSION" = "x.tar.bz2" || test "x$EXTENSION" = "x.tbz2"
then
  COMPRESS="j"
fi

if test "x$EXTENSION" = "x.tar.gz" || test "x$EXTENSION" = "x.tgz"
then
  COMPRESS="z"
fi

if test "x$COMPRESS" = "x"
then
  echo "unable to process, input file $1 has unsupported extension"
  exit
fi

echo "== extension is $EXTENSION - ok"
echo "== new extension will be $JEXTENSION"
echo "== cleaning old workdir $WORKDIR"

rm -rf $WORKDIR
mkdir $WORKDIR

echo "== extracting input archive $1"
tar -x -$COMPRESS -C $WORKDIR -f $1

echo "changing into $WORKDIR"
pushd $WORKDIR

DIRCOUNT=`ls -1 | wc -l`
if test $DIRCOUNT -ne 1
then
  echo "unable to process, $1 contains more than one toplevel directory"
  exit
fi

TOPDIR=`ls -1`
if test "x$TOPDIR" != "xmozilla"
then
  # try to deal with a single additional subdirectory above "mozilla"
  echo "== skipping toplevel directory $TOPDIR"
  cd $TOPDIR
fi

DIRCOUNT=`ls -1 | wc -l`
if test $DIRCOUNT -ne 1
then
  echo "unable to process, $1 contains more than one second level directory"
  exit
fi

SINGLEDIR=`ls -1`
if test "x$SINGLEDIR" != "xmozilla"
then
  echo "unable to process, first or second level directory is not mozilla"
  exit
fi

echo "== input archive accepted, now processing"

REALFREEBLDIR=mozilla/security/nss/lib/freebl
FREEBLDIR=./$REALFREEBLDIR

rm -rf ./mozilla/security/nss/cmd/ecperf

mv ${FREEBLDIR}/ecl/ecl-exp.h ${FREEBLDIR}/save
rm -rf ${FREEBLDIR}/ecl/tests
rm -rf ${FREEBLDIR}/ecl/CVS
for i in ${FREEBLDIR}/ecl/* ; do
echo clobbering $i
 > $i
done
mv ${FREEBLDIR}/save ${FREEBLDIR}/ecl/ecl-exp.h

for j in ${FREEBLDIR}/ec.*; do
        echo unifdef $j
        cat $j | \
        awk    'BEGIN {ech=1; prt=0;} \
                /^#[ \t]*ifdef.*NSS_ENABLE_ECC/ {ech--; next;} \
                /^#[ \t]*if/ {if(ech < 1) ech--;} \
                {if(ech>0) {;print $0};} \
                /^#[ \t]*endif/ {if(ech < 1) ech++;} \
                {if (prt && (ech<=0)) {;print $0}; } \
                {if (ech>0) {prt=0;} } \
                /^#[ \t]*else/ {if (ech == 0) prt=1;}' > $j.hobbled && \
        mv $j.hobbled $j
done

echo "== returning to original directory"
popd

JCOMPRESS=j
JEXTENSION=.tar.bz2
NEWARCHIVE=$BASE-stripped$JEXTENSION
echo "== finally producing new archive $NEWARCHIVE"
tar -c -$JCOMPRESS -C $WORKDIR -f $NEWARCHIVE $TOPDIR

echo "== all done, listing of old and new archive:"
ls -l $1
ls -l $NEWARCHIVE

LISTING_DIR=""
if test "x$TOPDIR" != "xmozilla"
then
  LISTING_DIR="$TOPDIR/$REALFREEBLDIR/ecl"
else
  LISTING_DIR="$REALFREEBLDIR/ecl"
fi

echo "== FYI, producing listing of stripped dir in new archive"
tar -t -v -$JCOMPRESS -C $WORKDIR -f $NEWARCHIVE $LISTING_DIR


