#!/bin/sh
#
# Splits NSS into nss-util and nss-softokn
# Takes as command line input the version of nss
# and assumes that a file nss-${nss_version}.tar.gz
# exists in the current directory

set -e

if test -z $1
then
  echo "usage: $0 nss-version"
  exit
fi

export name=nss
export version=$1

echo "Extracting ${name}-${version}.tar.gz"

tar -xzf ${name}-${version}.tar.gz

# the directory will be named ${name}-${version}

nss_source_dir=${name}-${version}
softokn_dir=${name}-softokn-${version}

# make_nss_softokn
#-------------------------------------------------
# create the nss-softokn subset consisting of
#   nss/dbm                 full directory
#   nss/coreconf            full directory
#   nss                     top files only
#   nss/lib                 top files only
#   nss/lib/freebl          full directory
#   nss/lib/softoken        full directory
#   nss/lib/softoken/dbm    full directory
#-------------------------------------------------------

WORK=${softokn_dir}-work
rm -rf ${WORK}
mkdir ${WORK}

# copy everything
cp -a ${nss_source_dir} ${WORK}/${softokn_dir}

# remove subdirectories that we don't want
rm -rf ${WORK}/${softokn_dir}/nss/cmd
rm -rf ${WORK}/${softokn_dir}/nss/tests
rm -rf ${WORK}/${softokn_dir}/nss/lib
rm -rf ${WORK}/${softokn_dir}/nss/pkg
# start with an empty lib directory and copy only what we need
mkdir ${WORK}/${softokn_dir}/nss/lib
# copy the top files from nss/lib/
topFilesL=`find ${nss_source_dir}/nss/lib/ -maxdepth 1 -mindepth 1 -type f`
for f in $topFilesL; do
  cp -p $f ${WORK}/${softokn_dir}/nss/lib
done
mkdir ${WORK}/${softokn_dir}/nss/lib/util
# copy entire dbm, freebl and softoken directories recursively
cp -a ${nss_source_dir}/nss/lib/dbm ${WORK}/${softokn_dir}/nss/lib/dbm
cp -a ${nss_source_dir}/nss/lib/freebl ${WORK}/${softokn_dir}/nss/lib/freebl
cp -a ${nss_source_dir}/nss/lib/softoken ${WORK}/${softokn_dir}/nss/lib/softoken
# and some Makefiles and related files from nss
topFilesN=`find ${nss_source_dir}/nss/ -maxdepth 1 -mindepth 1 -type f`
for f in $topFilesN; do
  cp -p $f ${WORK}/${softokn_dir}/nss/
done

# we do need bltest, lib, lowhashtest, and shlibsign from nss/cmd
mkdir ${WORK}/${softokn_dir}/nss/cmd
# copy some files at the top and the slhlib subdirectory
topFilesC=`find ${nss_source_dir}/nss/cmd/ -maxdepth 1 -mindepth 1 -type f`
for f in $topFilesC; do
  cp -p $f ${WORK}/${softokn_dir}/nss/cmd/
done

cp -a ${nss_source_dir}/nss/cmd/bltest ${WORK}/${softokn_dir}/nss/cmd/bltest
cp -a ${nss_source_dir}/nss/cmd/fipstest ${WORK}/${softokn_dir}/nss/cmd/fipstest
cp -a ${nss_source_dir}/nss/cmd/lib ${WORK}/${softokn_dir}/nss/cmd/lib
cp -a ${nss_source_dir}/nss/cmd/lowhashtest ${WORK}/${softokn_dir}/nss/cmd/lowhashtest
cp -a ${nss_source_dir}/nss/cmd/shlibsign ${WORK}/${softokn_dir}/nss/cmd/shlibsign

# plus common, crypto, and lowhash from nss/tests
mkdir ${WORK}/${softokn_dir}/nss/tests
topFilesT=`find ${nss_source_dir}/nss/tests/ -maxdepth 1 -mindepth 1 -type f`
for f in $topFilesT; do
  cp -p $f ${WORK}/${softokn_dir}/nss/tests/
done
keepers="cipher common lowhash"
for t in $keepers; do
  cp -a ${nss_source_dir}/nss/tests/$t ${WORK}/${softokn_dir}/nss/tests/$t
done

pushd ${WORK}
# the compressed tar ball for nss-softokn
tar -czf ../${name}-softokn-${version}.tar.gz ${softokn_dir}
popd

# cleanup after ourselves
rm -fr ${nss_source_dir}
rm -rf ${WORK}



