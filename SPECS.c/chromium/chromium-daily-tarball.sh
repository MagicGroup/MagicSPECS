#!/bin/bash

# This script checks out chromium source from svn, using the gclient tool.

LOCALDIR=`pwd`
REMOVE=false
TODAYSDATE=`date +%Y%m%d`
USAGE="Usage: chromium-daily-tarball.sh [-hrv]"
VERBOSE=false
CLEAN=false
BETA_CHANNEL=false
DEV_CHANNEL=false
CHANNEL_HACK=false
CHANNELS_URL=http://src.chromium.org/svn/releases/LATEST.txt
CHROMIUM_URL=http://src.chromium.org/svn/trunk/src
VERSION=

while getopts "bcdhrv" opt; do
   case $opt in
      b  ) BETA_CHANNEL=true
           CHANNEL_HACK=true ;;
      c  ) CLEAN=true ;;
      d  ) DEV_CHANNEL=true 
           CHANNEL_HACK=true ;;
      h  ) printf "$USAGE\n"
           printf "\nAvailable command line options:\n"
           printf "%b\t-b\t\tuse beta channel source\n"
           printf "%b\t-c\t\tmake tarball of clean source, nothing removed/altered\n"
           printf "%b\t-d\t\tuse dev channel source\n"
           printf "%b\t-h\t\tthis help\n"
           printf "%b\t-r\t\tremove conflicting chromium files/directories\n"
           printf "%b\t-v\t\tverbose output\n\n"
           exit 1 ;;
      r  ) REMOVE=true ;;
      v  ) VERBOSE=true
           printf "[VERBOSE]: Enabled\n" ;;
      \? ) printf "$USAGE\n"
           exit 1 ;;
   esac
done

# Prerequisites:
#  gclient
printf "Looking for gclient in your PATH: " 
which gclient
RETVAL=$?
if [ $RETVAL -ne 0 ]; then
   printf "[ERROR]: Could not find gclient in PATH. Please install it first.\n"
   exit 2
else
   printf "Found it! Lets get to work.\n"
fi

# First, lets look for the directory, without svnrev.
if [ -d chromium-$TODAYSDATE ]; then
   if [ "$REMOVE" = "true" ]; then
      if [ "$VERBOSE" = "true" ]; then
         printf "[VERBOSE]: Removing conflicting directory: chromium-$TODAYSDATE/\n"
      fi
      rm -rf chromium-$TODAYSDATE/
      if [ "$VERBOSE" = "true" ]; then
         printf "[VERBOSE]: Removed conflicting directory: chromium-$TODAYSDATE/\n"
      fi
   else
      printf "[ERROR]: chromium-$TODAYSDATE/ exists, use -r option to remove it\n"
      exit 2
   fi
fi

# At this point, we know the chromium daily directory does not exist, time to make it.
if [ "$VERBOSE" = "true" ]; then
   printf "[VERBOSE]: Creating directory: chromium-$TODAYSDATE/\n"
fi
mkdir -p chromium-$TODAYSDATE

# go into the chromium dir
pushd chromium-$TODAYSDATE/

if [ "$CHANNEL_HACK" = "true" ]; then
   if [ "$BETA_CHANNEL" = "true" ]; then
      VERSION=`wget -qO - http://src.chromium.org/svn/releases/LATEST.txt | grep -A3 "Beta Channel" | grep Linux | cut -d ":" -f 2 | sed 's| ||g'`
   else 
      if [ "$DEV_CHANNEL" = "true" ]; then
         VERSION=`wget -qO - http://src.chromium.org/svn/releases/LATEST.txt | grep -A3 "Dev Channel" | grep Linux | cut -d ":" -f 2 | sed 's| ||g'`
      else
         printf "How did you get here? This computer stuff is hard.\n"
         exit 1
      fi
   fi
   CHROMIUM_URL=http://src.chromium.org/svn/releases/$VERSION
   svnadmin create repo
   svn co file://`pwd`/repo repo2
   svn export $CHROMIUM_URL/DEPS repo2/DEPS
   sed -i -e "s%'/%'http://src.chromium.org/svn/%" repo2/DEPS
   svn add repo2/DEPS
   svn commit -m '' repo2/DEPS
fi

# Make the gclient config
if [ "$VERBOSE" = "true" ]; then
   printf "[VERBOSE]: Generating gclient config\n"
fi

if [ "$VERBOSE" = "true" ]; then
   printf "[VERBOSE]: gclient config $CHROMIUM_URL\n"
fi
gclient config $CHROMIUM_URL

# We rewrite .gclient to take out the LayoutTests for size considerations
cat > .gclient <<'EOF'
# An element of this array (a "solution") describes a repository directory
# that will be checked out into your working copy.  Each solution may
# optionally define additional dependencies (via its DEPS file) to be
# checked out alongside the solution's directory.  A solution may also
# specify custom dependencies (via the "custom_deps" property) that
# override or augment the dependencies specified by the DEPS file.
# If a "safesync_url" is specified, it is assumed to reference the location of
# a text file which contains nothing but the last known good SCM revision to
# sync against. It is fetched if specified and used unless --head is passed
solutions = [
  { "name"        : "src",
    "url"         : "http://src.chromium.org/svn/trunk/src",
    "custom_deps" : {
      # To use the trunk of a component instead of what's in DEPS:
      #"component": "https://svnserver/component/trunk/",
      # To exclude a component from your working copy:
      #"data/really_large_component": None,
      "src/webkit/data/layout_tests/LayoutTests": None,
      "src/third_party/WebKit/LayoutTests/": None,
    },
    "safesync_url": ""
  }
]
EOF

if [ "$CHANNEL_HACK" = "true" ]; then
   sed -i 's|http://src.chromium.org/svn/trunk/src|file://'`pwd`'/repo|' .gclient
   sed -i 's|"src",|"fake",|' .gclient
fi

printf "Checking out the source tree. This will take some time.\n"

if [ "$VERBOSE" = "true" ]; then
   # gclient sync --force
   printf "gclient update\n"
   gclient update
else
   gclient update &>/dev/null
   # gclient sync --force &>/dev/null
fi

if [ "$CHANNEL_HACK" = "true" ]; then
   # cleanup
   rm -rf repo repo2
fi

# Determine SVN rev and Version of chromium (we don't care about the other sub-checkouts)
pushd src/chrome
SVNREV=`svnversion`   
CHROME_VERSION=`cat VERSION | cut -f2 -d= |while read i; do echo -n $i\. ; done | cut -f1-4 -d.`
popd

printf "Chromium ($CHROME_VERSION) svn$SVNREV [$TODAYSDATE] checked out\n"

FULLVER=`echo ${CHROME_VERSION}-${TODAYSDATE}svn${SVNREV}`

# Get rid of courgette.
rm -rf src/courgette

if [ "$CLEAN" = "true" ]; then
   printf "[CLEAN] Not removing unused bits\n"
else

# Remove unused bits
if [ "$VERBOSE" = "true" ]; then
   printf "[VERBOSE]: Removing unused bits\n"
fi

rm -rf src/o3d/
rm -rf src/third_party/WebKit/WebKitTools/Scripts/webkitpy/layout_tests/
rm -rf src/webkit/data/layout_tests/
rm -rf src/third_party/hunspell/dictionaries/
rm -rf src/chrome/test/data/
rm -rf src/native_client/tests/
rm -rf src/third_party/WebKit/LayoutTests/

fi

if [ "$CLEAN" = "true" ]; then
   printf "[CLEAN] Not removing unnecessary third_party bits\n"
else

# Remove third party bits that we have on the system
if [ "$VERBOSE" = "true" ]; then
   printf "[VERBOSE]: Removing unnecessary third_party bits\n"
fi

rm -rf src/v8/include src/v8/src/

pushd src/third_party

# First, just take out the sources for the items which have already been conditionalized so we're sure we're not using them.
# We need to leave the .gyp files since this is how it finds the system libs.
# bzip2
rm -rf bzip2/*.c bzip2/*.h bzip2/LICENSE 

# libjpeg
rm -rf libjpeg/*.c libjpeg/README* 

# libpng
rm -rf libpng/*.c libpng/*.h libpng/README* libpng/LICENSE 

# zlib
rm -rf zlib/*.c zlib/*.h zlib/contrib/ zlib/README*

# libevent 
rm -rf libevent/*.c libevent/*.h libevent/*sh libevent/config* libevent/*.3 libevent/README libevent/compat libevent/linux libevent/mac libevent/sample libevent/test libevent/ChangeLog libevent/Makefile.* libevent/aclocal.m4 libevent/*.py libevent/mising libevent/mkinstalldirs

# libxml
rm -rf libxml/*c libxml/*.h libxml/*.in libxml/*sh libxml/*.m4 libxml/*.py libxml/*.xml libxml/missing libxml/mkinstalldirs libxml/*.1 libxml/build libxml/include libxml/linux libxml/mac libxml/win32 libxml/AUTHORS libxml/COPYING libxml/ChangeLog libxml/Copyright libxml/INSTALL libxml/NEWS libxml/README libxml/README.tests libxml/TODO* libxml/config* libxml/*.pl

# libxslt
rm -rf libxslt/build libxslt/libexslt libxslt/libxslt libxslt/linux libxslt/mac libxslt/win32 libxslt/AUTHORS libxslt/COPYING libxslt/ChangeLog libxslt/FEATURES libxslt/INSTALL libxslt/NEWS libxslt/README libxslt/TODO libxslt/*.h libxslt/*.m4 libxslt/compile libxslt/config* libxslt/depcomp libxslt/*sh libxslt/*.in libxslt/*.spec libxslt/missing

# libjingle
rm -rf third_party/libjingle/

# Next, nuke the whole directories for things not yet conditionalized:
rm -rf nss/ nspr/ icu/ glew/

# expat is only built on windows
rm -rf expat/files

# Also, get rid of the bad bits of the ffmpeg source (stupid google)
rm -rf ffmpeg/patched-ffmpeg-mt/*.c ffmpeg/patched-ffmpeg-mt/*.h ffmpeg/patched-ffmpeg-mt/doc ffmpeg/patched-ffmpeg-mt/ffpresets ffmpeg/patched-ffmpeg-mt/mt-work
rm -rf ffmpeg/patched-ffmpeg-mt/libavformat/*.c ffmpeg/patched-ffmpeg-mt/libavcodec/*.c ffmpeg/patched-ffmpeg-mt/tools ffmpeg/patched-ffmpeg-mt/tests
rm -rf ffmpeg/patched-ffmpeg-mt/libavutil/*.c ffmpeg/patched-ffmpeg-mt/libavfilter/*.c ffmpeg/patched-ffmpeg-mt/libavdevice/*.c ffmpeg/patched-ffmpeg-mt/libpostproc/*.c ffmpeg/patched-ffmpeg-mt/libswscale/*.c

# Lastly, get rid of the ffmpeg binaries
rm -rf ffmpeg/binaries
popd

# Another copy of zlib? Unpossible!
rm -rf src/third_party/WebKit/WebCore/platform/image-decoders/zlib/

# Get rid of .svn bits to save space
# if [ "$VERBOSE" = "true" ]; then
#   printf "[VERBOSE]: Removing unnecessary .svn bits\n"
#fi
#find src -depth -name .svn -type d -exec rm -rf {} \;

# Get rid of reference_build prebuilt binaries
if [ "$VERBOSE" = "true" ]; then
   printf "[VERBOSE]: Removing reference_build prebuilt binaries\n"
fi
find src -depth -name reference_build -type d -exec rm -rf {} \;

# Clean
fi

# Gclient embeds the full checkout path all over the .scons files. We'll replace it with a known dummy tree, which we can sed out
# in the rpm spec.
# FIXME: There has to be a better way to prevent this .scons mangling.
for i in `find . |grep "\.scons"`; do
   sed -i "s|$LOCALDIR/chromium-$TODAYSDATE/|/home/spot/sandbox/chromium-$TODAYSDATE/|g" $i
done

popd

# Now, lets look for the final target directory, without svnrev.
if [ -d chromium-$FULLVER ]; then
   if [ "$REMOVE" = "true" ]; then
      if [ "$VERBOSE" = "true" ]; then
         printf "[VERBOSE]: Removing conflicting directory: chromium-$FULLVER/\n"
      fi
      rm -rf chromium-$FULLVER/
      if [ "$VERBOSE" = "true" ]; then
         printf "[VERBOSE]: Removed conflicting directory: chromium-$FULLVER/\n"
      fi
   else
      printf "[ERROR]: chromium-$FULLVER/ exists, use -r option to remove it\n"
      exit 2
   fi
fi

# At this point, we know the chromium target directory does not exist, time to rename the checkout
if [ "$VERBOSE" = "true" ]; then
   printf "[VERBOSE]: Renaming checkout directory from: chromium-$TODAYSDATE/ to: chromium-$FULLVER/\n"
fi
mv chromium-$TODAYSDATE/ chromium-$FULLVER/

# Now, lets look for the tarball.
if [ -f chromium-$FULLVER.tar.lzma ]; then
   if [ "$VERBOSE" = "true" ]; then
      printf "[VERBOSE]: Found tarball matching chromium-$FULLVER.tar.lzma\n"
   fi
   if [ "$REMOVE" = "true" ]; then
      if [ "$VERBOSE" = "true" ]; then
         printf "[VERBOSE]: Removing conflicting file: chromium-$FULLVER.tar.lzma\n"
      fi
      rm -f chromium-$FULLVER.tar.lzma
      if [ "$VERBOSE" = "true" ]; then
         printf "[VERBOSE]: Removed conflicting file: chromium-$FULLVER.tar.lzma\n"
      fi
   else
      printf "[ERROR]: chromium-$FULLVER.tar.lzma exists, use -r option to remove it\n"
      exit 2
   fi
fi
         
if [ "$VERBOSE" = "true" ]; then
   printf "[VERBOSE]: Creating tarball: chromium-$FULLVER.tar.lzma\n"
fi
tar --exclude=\.svn -cf - chromium-$FULLVER | xz -9 -F lzma > chromium-$FULLVER.tar.lzma

# find src -depth -name .svn -type d -exec rm -rf {} \;

# All done.
printf "Daily chromium source processed and ready: chromium-$FULLVER.tar.lzma\n"
exit 0
