#!/bin/bash
#
#       run the misc tests: we need to do this in a script since
#       these are expected to fail which would normally cause %check
#       to stop.  however, this is expected behavior.  we are running
#       iasl precisely because we expect it to stop when presented with
#       faulty ASL.
#
#       this script assumes it is in the source 'tests' directory at
#       start.
#

set -x

BINDIR="$1"
VERSION="$2"

# create files to compare against
$BINDIR/iasl -h

m=`uname -m`
case $m in
    s390x | ppc64le | \
    *64) BITS=64
         ;;
    *)   BITS=32
         ;;
esac

# if a build starts before midnight, but ends after midnight, this
# test can get confused.  grab the date from the iasl file we just
# built so they match regardless.
FDATE=`stat --format="%Y" $BINDIR/iasl | cut -d" " -f1`
WHEN=`date --date="@$FDATE" +"%b %_d %Y"`

sed -e "s/XXXXXXXXXXX/$WHEN/" \
    -e "s/YYYY/$BITS/" \
    -e "s/VVVVVVVV/$VERSION/" \
    ../badcode.asl.result > misc/badcode.asl.result
sed -e "s/XXXXXXXXXXX/$WHEN/" \
    -e "s/YYYY/$BITS/" \
    -e "s/VVVVVVVV/$VERSION/" \
    ../grammar.asl.result > misc/grammar.asl.result

cd misc

# see if badcode.asl failed as expected
# NB: the -f option is required so we can see all of the errors
$BINDIR/iasl -f badcode.asl 2>&1 | tee badcode
diff badcode badcode.asl.result >/dev/null 2>&1
[ $? -eq 0 ] || exit 1

# see if grammar.asl failed as expected
# NB: the -f option is required so we can see all of the errors
$BINDIR/iasl -f -of grammar.asl 2>&1 | tee grammar
diff grammar grammar.asl.result >/dev/null 2>&1
[ $? -eq 0 ] || exit 1

exit 0
