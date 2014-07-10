# If debug is 1, OpenJDK is built with all debug info present.
%global debug 0

%global icedtea_version_presuffix pre04
%global icedtea_version 2.5
%global hg_tag icedtea-{icedtea_version}

%global aarch64_release 832

%global aarch64			aarch64 arm64 armv8
#sometimes we need to distinguish big and little endian PPC64
%global ppc64le			ppc64le
%global ppc64be			ppc64 ppc64p7
%global multilib_arches %{power64} sparc64 x86_64 mips64el
%global jit_arches		%{ix86} x86_64 sparcv9 sparc64 %{ppc64be} %{aarch64}

#if 0, then links are set forcibly, if 1 ten only if status is auto
%global graceful_links 1

%ifarch x86_64
%global archbuild amd64
%global archinstall amd64
%endif
%ifarch ppc
%global archbuild ppc
%global archinstall ppc
%global archdef PPC
%endif
%ifarch %{ppc64be}
%global archbuild ppc64
%global archinstall ppc64
%global archdef PPC
%endif
%ifarch %{ppc64le}
%global archbuild ppc64le
%global archinstall ppc64le
%global archdef PPC64
%endif
%ifarch %{ix86}
%global archbuild i586
%global archinstall i386
%endif
%ifarch ia64
%global archbuild ia64
%global archinstall ia64
%endif
%ifarch s390
%global archbuild s390
%global archinstall s390
%global archdef S390
%endif
%ifarch s390x
%global archbuild s390x
%global archinstall s390x
%global archdef S390
%endif
%ifarch %{arm}
%global archbuild arm
%global archinstall arm
%global archdef ARM
%endif
%ifarch %{aarch64}
%global archbuild aarch64
%global archinstall aarch64
%global archdef AARCH64
%endif
%ifarch mips64el
%global archbuild mips64el
%global archinstall mips64el
%global archdef MIPS64EL
%endif
# 32 bit sparc, optimized for v9
%ifarch sparcv9
%global archbuild sparc
%global archinstall sparc
%endif
# 64 bit sparc
%ifarch sparc64
%global archbuild sparcv9
%global archinstall sparcv9
%endif
%ifnarch %{jit_arches}
%global archbuild %{_arch}
%global archinstall %{_arch}
%endif

%if %{debug}
%global debugbuild debug_build
%else
%global debugbuild %{nil}
%endif

%if %{debug}
%global buildoutputdir openjdk/build/linux-%{archbuild}-debug
%else
%global buildoutputdir openjdk/build/linux-%{archbuild}
%endif
%ifnarch %{ppc64le}
%global with_pulseaudio 1
%else
%global with_pulseaudio 0
%endif

%ifarch %{jit_arches}
%global with_systemtap 1
%else
%global with_systemtap 0
%endif

# Convert an absolute path to a relative path.  Each symbolic link is
# specified relative to the directory in which it is installed so that
# it will resolve properly within chrooted installations.
%global script 'use File::Spec; print File::Spec->abs2rel($ARGV[0], $ARGV[1])'
%global abs2rel %{__perl} -e %{script}

# Hard-code libdir on 64-bit architectures to make the 64-bit JDK
# simply be another alternative.
%global LIBDIR       %{_libdir}
#backuped original one
%ifarch %{multilib_arches}
%global syslibdir       %{_prefix}/lib64
%global _libdir         %{_prefix}/lib
%else
%global syslibdir       %{_libdir}
%endif

# Standard JPackage naming and versioning defines.
%global origin          openjdk
%global updatever       55
%global aarch64_updatever 60
#Fedora have an bogus 60 instead of updatever. Fix when updatever>=60 in version:
%global buildver        13
%global aarch64_buildver 04
# Keep priority on 6digits in case updatever>9
%global priority        1700%{updatever}
%global javaver         1.7.0

%global sdkdir          %{uniquesuffix}
%global jrelnk          jre-%{javaver}-%{origin}-%{version}-%{release}.%{_arch}

%global jredir          %{sdkdir}/jre
%global sdkbindir       %{_jvmdir}/%{sdkdir}/bin
%global jrebindir       %{_jvmdir}/%{jredir}/bin
%global jvmjardir       %{_jvmjardir}/%{uniquesuffix}

%global fullversion     %{name}-%{version}-%{release}

%global uniquesuffix          %{fullversion}.%{_arch}
#we can copy the javadoc to not arched dir, or made it not noarch
%global uniquejavadocdir       %{fullversion}

%global statuscheck		status is auto
%global linkcheck		link currently points to

%ifarch %{jit_arches}
# Where to install systemtap tapset (links)
# We would like these to be in a package specific subdir,
# but currently systemtap doesn't support that, so we have to
# use the root tapset dir for now. To distinquish between 64
# and 32 bit architectures we place the tapsets under the arch
# specific dir (note that systemtap will only pickup the tapset
# for the primary arch for now). Systemtap uses the machine name
# aka build_cpu as architecture specific directory name.
%global tapsetroot /usr/share/systemtap
  %ifarch %{ix86}
    %global tapsetdir %{tapsetroot}/tapset/i386
  %else
    %global tapsetdir %{tapsetroot}/tapset/%{_build_cpu}
  %endif
%endif

# Prevent brp-java-repack-jars from being run.
%global __jar_repack 0

Name:    java-%{javaver}-%{origin}
Version: %{javaver}.60
Release: %{icedtea_version}.0.22.%{icedtea_version_presuffix}%{?dist}.4
# java-1.5.0-ibm from jpackage.org set Epoch to 1 for unknown reasons,
# and this change was brought into RHEL-4.  java-1.5.0-ibm packages
# also included the epoch in their virtual provides.  This created a
# situation where in-the-wild java-1.5.0-ibm packages provided "java =
# 1:1.5.0".  In RPM terms, "1.6.0 < 1:1.5.0" since 1.6.0 is
# interpreted as 0:1.6.0.  So the "java >= 1.6.0" requirement would be
# satisfied by the 1:1.5.0 packages.  Thus we need to set the epoch in
# JDK package >= 1.6.0 to 1, and packages referring to JDK virtual
# provides >= 1.6.0 must specify the epoch, "java >= 1:1.6.0".
Epoch:   1
Summary: OpenJDK Runtime Environment
Group:   Development/Languages

License:  ASL 1.1 and ASL 2.0 and GPL+ and GPLv2 and GPLv2 with exceptions and LGPL+ and LGPLv2 and MPLv1.0 and MPLv1.1 and Public Domain and W3C
URL:      http://openjdk.java.net/

#head
#REPO=http://icedtea.classpath.org/hg/icedtea7-forest
#current release
#REPO=http://icedtea.classpath.org/hg/release/icedtea7-forest-2.4
#aarch64
#REPO=http://hg.openjdk.java.net/aarch64-port/jdk7u
# hg clone $REPO/ openjdk -r %{hg_tag}
# hg clone $REPO/corba/ openjdk/corba -r %{hg_tag}
# hg clone $REPO/hotspot/ openjdk/hotspot -r %{hg_tag}
# hg clone $REPO/jaxp/ openjdk/jaxp -r %{hg_tag}
# hg clone $REPO/jaxws/ openjdk/jaxws -r %{hg_tag}
# hg clone $REPO/jdk/ openjdk/jdk -r %{hg_tag}
# hg clone $REPO/langtools/ openjdk/langtools -r %{hg_tag}
# find openjdk -name ".hg" -exec rm -rf '{}' \;
# sh /git/java-1.7.0-openjdk/fX/fsg.sh
# tar cJf openjdk-icedtea-%{icedtea_version}.tar.xz openjdk
Source0:  openjdk-icedtea-%{icedtea_version}%{icedtea_version_presuffix}.tar.xz
Source1:  aarch64-port-jdk7u%{aarch64_updatever}-b%{aarch64_buildver}-aarch64-%{aarch64_release}.tar.xz

# README file
# This source is under maintainer's/java-team's control
Source2:  README.src

# Sources 6-12 are taken from hg clone http://icedtea.classpath.org/hg/icedtea7
# Unless said differently, there is directory with required sources which should be enough to pack/rename

# Class rewrite to rewrite rhino hierarchy
Source5: class-rewriter.tar.gz

# Systemtap tapsets. Zipped up to keep it small.
# last update from http://icedtea.classpath.org/hg/icedtea7/file/8599fdfc398d/tapset
Source6: systemtap-tapset-2014-03-19.tar.xz

# .desktop files. 
Source7:  policytool.desktop
Source77: jconsole.desktop

# nss configuration file
Source8: nss.cfg

# FIXME: Taken from IcedTea snapshot 877ad5f00f69, but needs to be moved out
# hg clone -r 877ad5f00f69 http://icedtea.classpath.org/hg/icedtea7
Source9: pulseaudio.tar.gz

# Removed libraries that we link instead
Source10: remove-intree-libraries.sh

#http://icedtea.classpath.org/hg/icedtea7/file/933d082ec889/fsg.sh
# file to clean tarball, should be ketp updated as possible
Source1111: fsg.sh

# Ensure we aren't using the limited crypto policy
Source12: TestCryptoLevel.java

Source13: java-abrt-luncher

# Remove $ORIGIN from RPATHS
Source14: remove-origin-from-rpaths

# RPM/distribution specific patches

# Allow TCK to pass with access bridge wired in
Patch1:   java-1.7.0-openjdk-java-access-bridge-tck.patch

# Disable access to access-bridge packages by untrusted apps
Patch3:   java-1.7.0-openjdk-java-access-bridge-security.patch

# Ignore AWTError when assistive technologies are loaded 
Patch4:   java-1.7.0-openjdk-accessible-toolkit.patch

# Build docs even in debug
Patch5:   java-1.7.0-openjdk-debugdocs.patch

# Add debuginfo where missing
Patch6:   %{name}-debuginfo.patch

#
# OpenJDK specific patches
#

# Add rhino support
Patch100: rhino.patch
Patch1000: rhino-aarch64.patch

Patch106: %{name}-freetype-check-fix.patch

# allow to create hs_pid.log in tmp (in 700 permissions) if working directory is unwritable
Patch200: abrt_friendly_hs_log_jdk7.patch

#
# Optional component packages
#

# Make the ALSA based mixer the default when building with the pulseaudio based
# mixer
Patch300: pulse-soundproperties.patch

# Temporary patches

Patch403: PStack-808293.patch
Patch4030: PStack-808293-aarch64.patch
# Add hardcoded RPATHS to ELF files
Patch412: add-final-location-rpaths.patch
Patch4120: add-final-location-rpaths-aarch64.patch
# End of tmp patches

# Temporary copy of RH1064383 fix; remove after release of 2.4.8
Patch413: rh1064383-prelink_fix.patch

# mips64el fix
Patch500: java-1.7.0-openjdk-1.7.0.60-mips64el-fix.patch

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: gcc-c++
BuildRequires: alsa-lib-devel
BuildRequires: chrpath
BuildRequires: cups-devel
BuildRequires: desktop-file-utils
BuildRequires: giflib-devel
BuildRequires: lcms2-devel >= 2.5
BuildRequires: libX11-devel
BuildRequires: libXi-devel
BuildRequires: libXp-devel
BuildRequires: libXt-devel
BuildRequires: libXtst-devel
BuildRequires: libjpeg-devel
BuildRequires: libpng-devel
BuildRequires: wget
BuildRequires: libxslt
BuildRequires: xorg-x11-proto-devel
BuildRequires: ant
BuildRequires: libXinerama-devel
BuildRequires: rhino
%ifnarch mips64el
BuildRequires: redhat-lsb
%endif
BuildRequires: zip
BuildRequires: fontconfig
BuildRequires: xorg-x11-fonts-Type1
BuildRequires: zlib > 1.2.3-6
BuildRequires: java-1.7.0-openjdk-devel
BuildRequires: fontconfig
BuildRequires: at-spi-devel
BuildRequires: gawk
BuildRequires: pkgconfig >= 0.9.0
BuildRequires: xorg-x11-utils
BuildRequires: nss-devel
BuildRequires: libattr-devel
BuildRequires: python
# PulseAudio build requirements.
%if %{with_pulseaudio}
BuildRequires: pulseaudio-libs-devel >= 0.9.11
%endif
# Zero-assembler build requirement.
%ifnarch %{jit_arches}
BuildRequires: libffi-devel >= 3.0.10
%endif

# cacerts build requirement.
BuildRequires: openssl
# execstack build requirement.
# no prelink on ARM yet
%ifnarch %{arm} %{aarch64} %{ppc64le}
BuildRequires: prelink
%endif
%ifarch %{jit_arches}
#systemtap build requirement.
BuildRequires: systemtap-sdt-devel
%endif

Requires: fontconfig
Requires: xorg-x11-fonts-Type1
#requires rest of java
Requires: %{name}-headless = %{epoch}:%{version}-%{release}
OrderWithRequires: %{name}-headless = %{epoch}:%{version}-%{release}


# Standard JPackage base provides.
Provides: jre-%{javaver}-%{origin} = %{epoch}:%{version}-%{release}
Provides: jre-%{origin} = %{epoch}:%{version}-%{release}
Provides: jre-%{javaver} = %{epoch}:%{version}-%{release}
Provides: java-%{javaver} = %{epoch}:%{version}-%{release}
Provides: jre = %{javaver}
Provides: java-%{origin} = %{epoch}:%{version}-%{release}
Provides: java = %{epoch}:%{javaver}
# Standard JPackage extensions provides.
Provides: java-fonts = %{epoch}:%{version}

# Obsolete older 1.6 packages as it cannot use the new bytecode
Obsoletes: java-1.6.0-openjdk
Obsoletes: java-1.6.0-openjdk-demo
Obsoletes: java-1.6.0-openjdk-devel
Obsoletes: java-1.6.0-openjdk-javadoc
Obsoletes: java-1.6.0-openjdk-src

%description
The OpenJDK runtime environment.

%package headless
Summary: The OpenJDK runtime environment without audio and video support
Group:   Development/Languages

Requires: lcms2 >= 2.5
Requires: libjpeg = 6b
# Require /etc/pki/java/cacerts.
Requires: ca-certificates
# Require jpackage-utils for ant.
Requires: jpackage-utils >= 1.7.3-1jpp.2
# Require zoneinfo data provided by tzdata-java subpackage.
Requires: tzdata-java
# Post requires alternatives to install tool alternatives.
Requires(post):   %{_sbindir}/alternatives
# Postun requires alternatives to uninstall tool alternatives.
Requires(postun): %{_sbindir}/alternatives

Provides: jre-%{javaver}-%{origin}-headless = %{epoch}:%{version}-%{release}
Provides: jre-%{origin}-headless = %{epoch}:%{version}-%{release}
Provides: jre-%{javaver}-headless = %{epoch}:%{version}-%{release}
Provides: java-%{javaver}-headless = %{epoch}:%{version}-%{release}
Provides: jre-headless = %{epoch}:%{javaver}
Provides: java-%{origin}-headless = %{epoch}:%{version}-%{release}
Provides: java-headless = %{epoch}:%{javaver}
# Standard JPackage extensions provides.
Provides: jndi = %{epoch}:%{version}
Provides: jndi-ldap = %{epoch}:%{version}
Provides: jndi-cos = %{epoch}:%{version}
Provides: jndi-rmi = %{epoch}:%{version}
Provides: jndi-dns = %{epoch}:%{version}
Provides: jaas = %{epoch}:%{version}
Provides: jsse = %{epoch}:%{version}
Provides: jce = %{epoch}:%{version}
Provides: jdbc-stdext = 4.1
Provides: java-sasl = %{epoch}:%{version}

%description headless
The OpenJDK runtime environment without audio and video 

%package devel
Summary: OpenJDK Development Environment
Group:   Development/Tools

# Require base package.
Requires:         %{name} = %{epoch}:%{version}-%{release}
OrderWithRequires: %{name}-headless = %{epoch}:%{version}-%{release}
# Post requires alternatives to install tool alternatives.
Requires(post):   %{_sbindir}/alternatives
# Postun requires alternatives to uninstall tool alternatives.
Requires(postun): %{_sbindir}/alternatives

# Standard JPackage devel provides.
Provides: java-sdk-%{javaver}-%{origin} = %{epoch}:%{version}
Provides: java-sdk-%{javaver} = %{epoch}:%{version}
Provides: java-sdk-%{origin} = %{epoch}:%{version}
Provides: java-sdk = %{epoch}:%{javaver}
Provides: java-%{javaver}-devel = %{epoch}:%{version}
Provides: java-devel-%{origin} = %{epoch}:%{version}
Provides: java-devel = %{epoch}:%{javaver}


%description devel
The OpenJDK development tools.

%package demo
Summary: OpenJDK Demos
Group:   Development/Languages

Requires: %{name} = %{epoch}:%{version}-%{release}
OrderWithRequires: %{name}-headless = %{epoch}:%{version}-%{release}

%description demo
The OpenJDK demos.

%package src
Summary: OpenJDK Source Bundle
Group:   Development/Languages

Requires: %{name} = %{epoch}:%{version}-%{release}

%description src
The OpenJDK source bundle.

%package javadoc
Summary: OpenJDK API Documentation
Group:   Documentation
Requires: jpackage-utils
BuildArch: noarch

OrderWithRequires: %{name}-headless = %{epoch}:%{version}-%{release}
# Post requires alternatives to install javadoc alternative.
Requires(post):   %{_sbindir}/alternatives
# Postun requires alternatives to uninstall javadoc alternative.
Requires(postun): %{_sbindir}/alternatives

# Standard JPackage javadoc provides.
Provides: java-javadoc = %{epoch}:%{version}-%{release}
Provides: java-%{javaver}-javadoc = %{epoch}:%{version}-%{release}

%description javadoc
The OpenJDK API documentation.

%package accessibility
Summary: OpenJDK accessibility connector
Requires: java-atk-wrapper
Requires: %{name} = %{epoch}:%{version}-%{release}
OrderWithRequires: %{name}-headless = %{epoch}:%{version}-%{release}

%description accessibility
Enables accessibility support in OpenJDK by using java-at-wrapper. This allows compatible at-spi2 based accessibility programs to work for AWT and Swing-based programs.
Please note, the java-atk-wrapper is still in beta, and also OpenJDK itself is still in phase of tuning to be working with accessibility features.
Although working pretty fine, there are known issues with accessibility on, so do not rather install this package unless you really need.

%prep
%ifarch %{aarch64}
%global source_num 1
%else
%global source_num 0
%endif

%setup -q -c -n %{uniquesuffix} -T -a %{source_num}
cp %{SOURCE2} .

# OpenJDK patches
%ifarch %{aarch64}
%patch1000
%else
%patch100
%endif

# pulseaudio support
%if %{with_pulseaudio}
%patch300
%endif

# Add systemtap patches if enabled
%if %{with_systemtap}
%endif

# Remove libraries that are linked
%ifarch %{aarch64}
#remove the conditiona lso from  remove-in-tree-libraries
#sh %{SOURCE10}  CHANGE_JPG
#tempraryly disabled
%else
sh %{SOURCE10} 
%endif

# Copy jaxp, jaf and jaxws drops
mkdir drops/

# Extract the rewriter (to rewrite rhino classes)
tar xzf %{SOURCE5}

# Extract systemtap tapsets
%if %{with_systemtap}

tar xf %{SOURCE6}

for file in tapset/*.in; do

    OUTPUT_FILE=`echo $file | sed -e s:%{javaver}\.stp\.in$:%{version}-%{release}.stp:g`
    sed -e s:@ABS_SERVER_LIBJVM_SO@:%{_jvmdir}/%{sdkdir}/jre/lib/%{archinstall}/server/libjvm.so:g $file > $file.1
# FIXME this should really be %if %{has_client_jvm}
%ifarch %{ix86}
    sed -e s:@ABS_CLIENT_LIBJVM_SO@:%{_jvmdir}/%{sdkdir}/jre/lib/%{archinstall}/client/libjvm.so:g $file.1 > $OUTPUT_FILE
%else
    sed -e '/@ABS_CLIENT_LIBJVM_SO@/d' $file.1 > $OUTPUT_FILE
%endif
    sed -i -e s:@ABS_JAVA_HOME_DIR@:%{_jvmdir}/%{sdkdir}:g $OUTPUT_FILE
    sed -i -e s:@INSTALL_ARCH_DIR@:%{archinstall}:g $OUTPUT_FILE

done

%endif

# Pulseaudio
%if %{with_pulseaudio}
tar xzf %{SOURCE9}
%endif


%patch3
%patch4

%if %{debug}
%patch5
%patch6
%endif

%patch106
%ifnarch %{aarch64}
#friendly hserror is not applicable in head, needs to be revisited
%patch200
%endif

%ifarch %{aarch64}
%patch4030
%else
%patch403
%endif

%ifarch %{aarch64}
%patch4120
%else
%patch412
%endif

%patch413

%patch500

%build
# How many cpu's do we have?
export NUM_PROC=`/usr/bin/getconf _NPROCESSORS_ONLN 2> /dev/null || :`
export NUM_PROC=${NUM_PROC:-1}

# Build IcedTea and OpenJDK.
%ifarch s390x sparc64 alpha %{power64} %{aarch64} mips64el
export ARCH_DATA_MODEL=64
%endif
%ifarch alpha
export CFLAGS="$CFLAGS -mieee"
%endif

export CFLAGS="$CFLAGS -fstack-protector-strong"

# Build the re-written rhino jar
mkdir -p rhino/{old,new}

# Compile the rewriter
(cd rewriter 
 javac com/redhat/rewriter/ClassRewriter.java
)

# Extract rhino.jar contents and rewrite
(cd rhino/old 
 jar xf /usr/share/java/rhino.jar
)

java -cp rewriter com.redhat.rewriter.ClassRewriter \
    $PWD/rhino/old \
    $PWD/rhino/new \
    org.mozilla \
    sun.org.mozilla

(cd rhino/old
 for file in `find -type f -not -name '*.class'` ; do
     new_file=../new/`echo $file | sed -e 's#org#sun/org#'`
     mkdir -pv `dirname $new_file`
     cp -v $file $new_file
     sed -ie 's#org\.mozilla#sun.org.mozilla#g' $new_file
 done
)

(cd rhino/new
   jar cfm ../rhino.jar META-INF/MANIFEST.MF sun
)

export JDK_TO_BUILD_WITH=/usr/lib/jvm/java-1.7.0-openjdk



pushd openjdk >& /dev/null

export ALT_DROPS_DIR=$PWD/../drops
export ALT_BOOTDIR="$JDK_TO_BUILD_WITH"

# Save old umask as jdk_generic_profile overwrites it
oldumask=`umask`

# Set generic profile
%ifnarch %{jit_arches}
export ZERO_BUILD=true
%endif
source jdk/make/jdk_generic_profile.sh

# Restore old umask
umask $oldumask

# aarch64 is not based on icedtea, but on upstream 7u instead. Adjust
# JDK_UPDATE_VERSION/BUILD_NUMBER/USER_RELEASE_SUFFIX to get an appropriate
# version string.

make \
  DISABLE_INTREE_EC=true \
  UNLIMITED_CRYPTO=true \
  ANT="/usr/bin/ant" \
%ifnarch %{aarch64}
  DISTRO_NAME="Fedora" \
  DISTRO_PACKAGE_VERSION="fedora-%{release}-%{_arch} u%{updatever}-b%{buildver}" \
  JDK_UPDATE_VERSION=`printf "%02d" %{updatever}` \
  JDK_BUILD_NUMBER=b`printf "%02d" %{buildver}` \
  JRE_RELEASE_VERSION=%{javaver}_`printf "%02d" %{updatever}`-b`printf "%02d" %{buildver}` \
%else
  JDK_UPDATE_VERSION="%{aarch64_updatever}" \
  BUILD_NUMBER="b%{aarch64_buildver}" \
  USER_RELEASE_SUFFIX="aarch64-%{aarch64_release}" \
%endif
  MILESTONE="fcs" \
  ALT_PARALLEL_COMPILE_JOBS="$NUM_PROC" \
  HOTSPOT_BUILD_JOBS="$NUM_PROC" \
  STATIC_CXX="false" \
  RHINO_JAR="$PWD/../rhino/rhino.jar" \
  GENSRCDIR="$PWD/generated.build" \
  FT2_CFLAGS="`pkg-config --cflags freetype2` " \
  FT2_LIBS="`pkg-config --libs freetype2` " \
  DEBUG_CLASSFILES="true" \
  DEBUG_BINARIES="true" \
  STRIP_POLICY="no_strip" \
  JAVAC_WARNINGS_FATAL="false" \
  INSTALL_LOCATION=%{_jvmdir}/%{sdkdir} \
  %{debugbuild}

popd >& /dev/null

if [ -e $(pwd)/%{buildoutputdir}/j2sdk-image/lib/sa-jdi.jar ]; then 
  chmod 644 $(pwd)/%{buildoutputdir}/j2sdk-image/lib/sa-jdi.jar;
fi

export JAVA_HOME=$(pwd)/%{buildoutputdir}/j2sdk-image

# Install java-abrt-luncher
mkdir  $JAVA_HOME/jre-abrt
mkdir  $JAVA_HOME/jre-abrt/bin
mv  $JAVA_HOME/jre/bin/java $JAVA_HOME/jre-abrt/bin/java
ln -s %{_jvmdir}/%{sdkdir}/jre/lib $JAVA_HOME/jre-abrt/lib
cat %{SOURCE13} | sed -e s:@JAVA_PATH@:%{_jvmdir}/%{sdkdir}/jre-abrt/bin/java:g -e s:@LIB_DIR@:%{LIBDIR}/libabrt-java-connector.so:g >  $JAVA_HOME/jre/bin/java
chmod 755 $JAVA_HOME/jre/bin/java

# Build pulseaudio and install it to JDK build location
%if %{with_pulseaudio}
pushd pulseaudio
make JAVA_HOME=$JAVA_HOME -f Makefile.pulseaudio
cp -pPRf build/native/libpulse-java.so $JAVA_HOME/jre/lib/%{archinstall}/
cp -pPRf build/pulse-java.jar $JAVA_HOME/jre/lib/ext/
popd
%endif

# Copy tz.properties
echo "sun.zoneinfo.dir=/usr/share/javazi" >> $JAVA_HOME/jre/lib/tz.properties

#remove all fontconfig files. This change should be usptreamed soon
rm -f %{buildoutputdir}/j2re-image/lib/fontconfig*.properties.src
rm -f %{buildoutputdir}/j2re-image/lib/fontconfig*.bfc
rm -f %{buildoutputdir}/j2sdk-image/jre/lib/fontconfig*.properties.src
rm -f %{buildoutputdir}/j2sdk-image/jre/lib/fontconfig*.bfc
rm -f %{buildoutputdir}/lib/fontconfig*.properties.src
rm -f %{buildoutputdir}/lib/fontconfig*.bfc

# Check unlimited policy has been used
$JAVA_HOME/bin/javac -d . %{SOURCE12}
$JAVA_HOME/bin/java TestCryptoLevel

files=$(find $(pwd)/%{buildoutputdir}/j2sdk-image/ -type f | xargs file | grep ELF | cut -d: -f1)
python %{SOURCE14} $files

%install
rm -rf $RPM_BUILD_ROOT
STRIP_KEEP_SYMTAB=libjvm*

# Install symlink to default soundfont
install -d -m 755 $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}/lib/audio
pushd $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}/lib/audio
ln -s %{_datadir}/soundfonts/default.sf2
popd

pushd %{buildoutputdir}/j2sdk-image

#install jsa directories so we can owe them
mkdir -p $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}/lib/%{archinstall}/server/
mkdir -p $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}/lib/%{archinstall}/client/

  # Install main files.
  install -d -m 755 $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}
  cp -a jre-abrt bin include lib src.zip $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}
  install -d -m 755 $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}
  cp -a jre/bin jre/lib $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}
  cp -a ASSEMBLY_EXCEPTION LICENSE THIRD_PARTY_README $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}

%ifarch %{jit_arches}
  # Install systemtap support files.
  install -dm 755 $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}/tapset
  cp -a $RPM_BUILD_DIR/%{uniquesuffix}/tapset/*.stp $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}/tapset/
  install -d -m 755 $RPM_BUILD_ROOT%{tapsetdir}
  pushd $RPM_BUILD_ROOT%{tapsetdir}
    RELATIVE=$(%{abs2rel} %{_jvmdir}/%{sdkdir}/tapset %{tapsetdir})
    ln -sf $RELATIVE/*.stp .
  popd
%endif

  # Install cacerts symlink.
  rm -f $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}/lib/security/cacerts
  pushd $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}/lib/security
    RELATIVE=$(%{abs2rel} %{_sysconfdir}/pki/java \
      %{_jvmdir}/%{jredir}/lib/security)
    ln -sf $RELATIVE/cacerts .
  popd

  # Install extension symlinks.
  install -d -m 755 $RPM_BUILD_ROOT%{jvmjardir}
  pushd $RPM_BUILD_ROOT%{jvmjardir}
    RELATIVE=$(%{abs2rel} %{_jvmdir}/%{jredir}/lib %{jvmjardir})
    ln -sf $RELATIVE/jsse.jar jsse-%{version}.jar
    ln -sf $RELATIVE/jce.jar jce-%{version}.jar
    ln -sf $RELATIVE/rt.jar jndi-%{version}.jar
    ln -sf $RELATIVE/rt.jar jndi-ldap-%{version}.jar
    ln -sf $RELATIVE/rt.jar jndi-cos-%{version}.jar
    ln -sf $RELATIVE/rt.jar jndi-rmi-%{version}.jar
    ln -sf $RELATIVE/rt.jar jaas-%{version}.jar
    ln -sf $RELATIVE/rt.jar jdbc-stdext-%{version}.jar
    ln -sf jdbc-stdext-%{version}.jar jdbc-stdext-3.0.jar
    ln -sf $RELATIVE/rt.jar sasl-%{version}.jar
    for jar in *-%{version}.jar
    do
      if [ x%{version} != x%{javaver} ]
      then
        ln -sf $jar $(echo $jar | sed "s|-%{version}.jar|-%{javaver}.jar|g")
      fi
      ln -sf $jar $(echo $jar | sed "s|-%{version}.jar|.jar|g")
    done
  popd

  # Install JCE policy symlinks.
  install -d -m 755 $RPM_BUILD_ROOT%{_jvmprivdir}/%{uniquesuffix}/jce/vanilla

  # Install versioned symlinks.
  pushd $RPM_BUILD_ROOT%{_jvmdir}
    ln -sf %{jredir} %{jrelnk}
  popd

  pushd $RPM_BUILD_ROOT%{_jvmjardir}
    ln -sf %{sdkdir} %{jrelnk}
  popd

  # Remove javaws man page
  rm -f man/man1/javaws*

  # Install man pages.
  install -d -m 755 $RPM_BUILD_ROOT%{_mandir}/man1
  for manpage in man/man1/*
  do
    # Convert man pages to UTF8 encoding.
    iconv -f ISO_8859-1 -t UTF8 $manpage -o $manpage.tmp
    mv -f $manpage.tmp $manpage
    install -m 644 -p $manpage $RPM_BUILD_ROOT%{_mandir}/man1/$(basename \
      $manpage .1)-%{uniquesuffix}.1
  done

  # Install demos and samples.
  cp -a demo $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}
  mkdir -p sample/rmi
  mv bin/java-rmi.cgi sample/rmi
  cp -a sample $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}

popd


# Install nss.cfg
install -m 644 %{SOURCE8} $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}/lib/security/


# Install Javadoc documentation.
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}
cp -a %{buildoutputdir}/docs $RPM_BUILD_ROOT%{_javadocdir}/%{uniquejavadocdir}

# Install icons and menu entries.
for s in 16 24 32 48 ; do
  install -D -p -m 644 \
    openjdk/jdk/src/solaris/classes/sun/awt/X11/java-icon${s}.png \
    $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${s}x${s}/apps/java-%{javaver}.png
done

# Install desktop files.
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/{applications,pixmaps}
for e in %{SOURCE7} %{SOURCE77} ; do
    sed -i "s/#ARCH#/%{_arch}-%{release}/g" $e
    sed -i "s|/usr/bin|%{sdkbindir}/|g" $e
    desktop-file-install --vendor=%{uniquesuffix} --mode=644 \
        --dir=$RPM_BUILD_ROOT%{_datadir}/applications $e
done

# Install /etc/.java/.systemPrefs/ directory
# See https://bugzilla.redhat.com/show_bug.cgi?id=741821
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/.java/.systemPrefs

# Find JRE directories.
find $RPM_BUILD_ROOT%{_jvmdir}/%{jredir} -type d \
  | grep -v jre/lib/security \
  | sed 's|'$RPM_BUILD_ROOT'|%dir |' \
  > %{name}.files-headless
# Find JRE files.
find $RPM_BUILD_ROOT%{_jvmdir}/%{jredir} -type f -o -type l \
  | grep -v jre/lib/security \
  | sed 's|'$RPM_BUILD_ROOT'||' \
  > %{name}.files.all
#split %{name}.files to %{name}.files-headless and %{name}.files
#see https://bugzilla.redhat.com/show_bug.cgi?id=875408
NOT_HEADLESS=\
"%{_jvmdir}/%{uniquesuffix}/jre/lib/%{archinstall}/libjsoundalsa.so 
%{_jvmdir}/%{uniquesuffix}/jre/lib/%{archinstall}/libpulse-java.so 
%{_jvmdir}/%{uniquesuffix}/jre/lib/%{archinstall}/libsplashscreen.so 
%{_jvmdir}/%{uniquesuffix}/jre/lib/%{archinstall}/xawt/libmawt.so
%{_jvmdir}/%{uniquesuffix}/jre-abrt/lib/%{archinstall}/libjsoundalsa.so 
%{_jvmdir}/%{uniquesuffix}/jre-abrt/lib/%{archinstall}/libpulse-java.so 
%{_jvmdir}/%{uniquesuffix}/jre-abrt/lib/%{archinstall}/libsplashscreen.so 
%{_jvmdir}/%{uniquesuffix}/jre-abrt/lib/%{archinstall}/xawt/libmawt.so"
#filter  %{name}.files from  %{name}.files.all to  %{name}.files-headless
ALL=`cat %{name}.files.all`
for file in $ALL ; do 
  INLCUDE="NO" ; 
  for blacklist in $NOT_HEADLESS ; do
#we can not match normally, because rpmbuild will evaluate !0 result as script failure
    q=`expr match "$file" "$blacklist"` || :
    l=`expr length  "$blacklist"` || :
    if [ $q -eq $l  ]; then 
      INLCUDE="YES" ; 
    fi;
  done
    if [ "x$INLCUDE" = "xNO"  ]; then 
      echo "$file" >> %{name}.files-headless
    else
      echo "$file" >> %{name}.files
    fi
done
# Find demo directories.
find $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}/demo \
  $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}/sample -type d \
  | sed 's|'$RPM_BUILD_ROOT'|%dir |' \
  > %{name}-demo.files

# FIXME: remove SONAME entries from demo DSOs.  See
# https://bugzilla.redhat.com/show_bug.cgi?id=436497

# Find non-documentation demo files.
find $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}/demo \
  $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}/sample \
  -type f -o -type l | sort \
  | grep -v README \
  | sed 's|'$RPM_BUILD_ROOT'||' \
  >> %{name}-demo.files
# Find documentation demo files.
find $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}/demo \
  $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}/sample \
  -type f -o -type l | sort \
  | grep README \
  | sed 's|'$RPM_BUILD_ROOT'||' \
  | sed 's|^|%doc |' \
  >> %{name}-demo.files

# intentionally after the files generation, as it goes to separate package
# Create links which leads to separately installed java-atk-bridge and allow configuration
# links points to java-atk-wrapper - an dependence
  pushd $RPM_BUILD_ROOT/%{_jvmdir}/%{jredir}/lib/%{archinstall}
    ln -s %{syslibdir}/java-atk-wrapper/libatk-wrapper.so.0 libatk-wrapper.so
  popd
  pushd $RPM_BUILD_ROOT/%{_jvmdir}/%{jredir}/lib/ext
     ln -s %{syslibdir}/java-atk-wrapper/java-atk-wrapper.jar  java-atk-wrapper.jar
  popd
  pushd $RPM_BUILD_ROOT/%{_jvmdir}/%{jredir}/lib/
    echo "#Config file to  enable java-atk-wrapper" > accessibility.properties
    echo "" >> accessibility.properties
    echo "assistive_technologies=org.GNOME.Accessibility.AtkWrapper" >> accessibility.properties
    echo "" >> accessibility.properties
  popd

%pretrans headless -p <lua>
-- see https://bugzilla.redhat.com/show_bug.cgi?id=1038092 for whole issue 

local posix = require "posix"

local currentjvm = "%{uniquesuffix}"
local jvmdir = "%{_jvmdir}"
local jvmDestdir = jvmdir
local origname = "%{name}"
local origjavaver = "%{javaver}"
--trasnform substitute names to lua patterns
--all percentages must be doubled for case of RPM escapingg
local name = string.gsub(string.gsub(origname, "%%-", "%%%%-"), "%%.", "%%%%.")
local javaver = string.gsub(origjavaver, "%%.", "%%%%.")
local arch ="%{_arch}"
local  debug = false;

local jvms = { }

local caredFiles = {"jre/lib/calendars.properties",
              "jre/lib/content-types.properties",
              "jre/lib/flavormap.properties",
              "jre/lib/logging.properties",
              "jre/lib/net.properties",
              "jre/lib/psfontj2d.properties",
              "jre/lib/sound.properties",
              "jre/lib/tz.properties",
              "jre/lib/deployment.properties",
              "jre/lib/deployment.config",
              "jre/lib/security/US_export_policy.jar",
              "jre/lib/security/java.policy",
              "jre/lib/security/java.security",
              "jre/lib/security/local_policy.jar",
              "jre/lib/security/nss.cfg,",
              "jre/lib/ext"}

function splitToTable(source, pattern)
  local i1 = string.gmatch(source, pattern) 
  local l1 = {}
  for i in i1 do
    table.insert(l1, i)
  end
  return l1
end

if (debug) then
  print("started")
end;

foundJvms = posix.dir(jvmdir);
if (foundJvms == nil) then
  if (debug) then
    print("no, or nothing in "..jvmdir.." exit")
  end;
  return
end

if (debug) then
  print("found "..#foundJvms.."jvms")
end;

for i,p in pairs(foundJvms) do
-- regex similar to %{_jvmdir}/%{name}-%{javaver}*%{_arch} bash command
--all percentages must be doubled for case of RPM escapingg
  if (string.find(p, name.."%%-"..javaver..".*"..arch) ~= nil ) then
    if (debug) then
      print("matched:  "..p)
    end;
    if (currentjvm ==  p) then
      if (debug) then
        print("this jdk is already installed. exiting lua script")
      end;
      return
    end ;
    table.insert(jvms, p)
  else
    if (debug) then
      print("NOT matched:  "..p)
    end;
  end
end

if (#jvms <=0) then 
  if (debug) then
    print("no matching jdk in "..jvmdir.." exit")
  end;
  return
end;

if (debug) then
  print("matched "..#jvms.." jdk in "..jvmdir)
end;

--full names are like java-1.7.0-openjdk-1.7.0.60-2.4.5.1.fc20.x86_64
table.sort(jvms , function(a,b) 
-- version-sort
-- split on non word: . - 
  local l1 = splitToTable(a, "[^%.-]+") 
  local l2 = splitToTable(b, "[^%.-]+") 
  for x = 1, math.min(#l1, #l2) do
    local l1x = tonumber(l1[x])
    local l2x = tonumber(l2[x])
    if (l1x ~= nil and l2x ~= nil)then
--if hunks are numbers, go with them 
      if (l1x < l2x) then return true; end
      if (l1x > l2x) then return false; end
    else
      if (l1[x] < l2[x]) then return true; end
      if (l1[x] > l2[x]) then return false; end
    end
-- if hunks are equals then move to another pair of hunks
  end
return a<b

end)

if (debug) then
  print("sorted lsit of jvms")
  for i,file in pairs(jvms) do
    print(file)
  end
end

latestjvm = jvms[#jvms]


for i,file in pairs(caredFiles) do
  local SOURCE=jvmdir.."/"..latestjvm.."/"..file
  local DEST=jvmDestdir.."/"..currentjvm.."/"..file
  if (debug) then
    print("going to copy "..SOURCE)
    print("to  "..DEST)
  end;
  local stat1 = posix.stat(SOURCE, "type");
  if (stat1 ~= nil) then
  if (debug) then
    print(SOURCE.." exists")
  end;
  local s = ""
  local dirs = splitToTable(DEST, "[^/]+") 
  for i,d in pairs(dirs) do
    if (i == #dirs) then
      break
    end
    s = s.."/"..d
    local stat2 = posix.stat(s, "type");
    if (stat2 == nil) then
      if (debug) then
        print(s.." does not exists, creating")
      end;
      posix.mkdir(s)
    else
      if (debug) then
        print(s.." exists,not creating")
      end;
    end
  end
-- Copy with -a to keep everything intact
    local exe = "cp".." -ar "..SOURCE.." "..DEST
    if (debug) then
      print("executing "..exe)
    end;    
    os.execute(exe)
  else
    if (debug) then
      print(SOURCE.." does not exists")
    end;
  end
end


%post 
update-desktop-database %{_datadir}/applications &> /dev/null || :
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
exit 0


# FIXME: identical binaries are copied, not linked. This needs to be
# fixed upstream.
%post headless
%ifarch %{jit_arches}
#see https://bugzilla.redhat.com/show_bug.cgi?id=513605
%{jrebindir}/java -Xshare:dump >/dev/null 2>/dev/null
%endif

# Note current status of alternatives
MAKE_THIS_DEFAULT=0
ID="%{_jvmdir}/\(\(jre\)\|\(java\)\)-%{javaver}-%{origin}.*bin/java"
COMMAND=java
alternatives --display $COMMAND | head -n 1 | grep -q "%{statuscheck}"
if [ $? -ne 0 ]; then
  alternatives --display $COMMAND | grep -q "%{linkcheck}"".*""$ID"
  if [ $? -eq 0 ]; then
    MAKE_THIS_DEFAULT=1
  fi
fi


ext=.gz
alternatives \
  --install %{_bindir}/java java %{jrebindir}/java %{priority} \
  --slave %{_jvmdir}/jre jre %{_jvmdir}/%{jredir} \
  --slave %{_jvmjardir}/jre jre_exports %{jvmjardir} \
  --slave %{_bindir}/keytool keytool %{jrebindir}/keytool \
  --slave %{_bindir}/orbd orbd %{jrebindir}/orbd \
  --slave %{_bindir}/pack200 pack200 %{jrebindir}/pack200 \
  --slave %{_bindir}/rmid rmid %{jrebindir}/rmid \
  --slave %{_bindir}/rmiregistry rmiregistry %{jrebindir}/rmiregistry \
  --slave %{_bindir}/servertool servertool %{jrebindir}/servertool \
  --slave %{_bindir}/tnameserv tnameserv %{jrebindir}/tnameserv \
  --slave %{_bindir}/unpack200 unpack200 %{jrebindir}/unpack200 \
  --slave %{_mandir}/man1/java.1$ext java.1$ext \
  %{_mandir}/man1/java-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/keytool.1$ext keytool.1$ext \
  %{_mandir}/man1/keytool-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/orbd.1$ext orbd.1$ext \
  %{_mandir}/man1/orbd-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/pack200.1$ext pack200.1$ext \
  %{_mandir}/man1/pack200-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/rmid.1$ext rmid.1$ext \
  %{_mandir}/man1/rmid-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/rmiregistry.1$ext rmiregistry.1$ext \
  %{_mandir}/man1/rmiregistry-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/servertool.1$ext servertool.1$ext \
  %{_mandir}/man1/servertool-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/tnameserv.1$ext tnameserv.1$ext \
  %{_mandir}/man1/tnameserv-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/unpack200.1$ext unpack200.1$ext \
  %{_mandir}/man1/unpack200-%{uniquesuffix}.1$ext

%if %{graceful_links}
# Gracefully update to this one if needed
if [ $MAKE_THIS_DEFAULT -eq 1 ]; then
%endif
  alternatives --set $COMMAND %{jrebindir}/java
%if %{graceful_links}
fi
%endif

for X in %{origin} %{javaver} ; do
  # Note current status of alternatives
  MAKE_THIS_DEFAULT=0
  ID="%{_jvmdir}/\(\(jre\)\|\(java\)\)-%{javaver}-%{origin}"
  COMMAND=jre_$X
  alternatives --display $COMMAND | head -n 1 | grep -q "%{statuscheck}"
  if [ $? -ne 0 ]; then
    alternatives --display $COMMAND | grep -q "%{linkcheck}"".*""$ID"
    if [ $? -eq 0 ]; then
      MAKE_THIS_DEFAULT=1
    fi
  fi

  alternatives \
    --install %{_jvmdir}/jre-"$X" \
    jre_"$X" %{_jvmdir}/%{jredir} %{priority} \
    --slave %{_jvmjardir}/jre-"$X" \
    jre_"$X"_exports %{jvmjardir}
%if %{graceful_links}
  # Gracefully update to this one if needed
  if [ $MAKE_THIS_DEFAULT -eq 1 ]; then
%endif
    alternatives --set $COMMAND %{_jvmdir}/%{jredir}
%if %{graceful_links}
  fi
%endif
done

update-alternatives --install %{_jvmdir}/jre-%{javaver}-%{origin} jre_%{javaver}_%{origin} %{_jvmdir}/%{jrelnk} %{priority} \
--slave %{_jvmjardir}/jre-%{javaver}       jre_%{javaver}_%{origin}_exports      %{jvmjardir}

update-desktop-database %{_datadir}/applications &> /dev/null || :

/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

exit 0

%postun
update-desktop-database %{_datadir}/applications &> /dev/null || :

if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

exit 0


%postun headless
  alternatives --remove java %{jrebindir}/java
  alternatives --remove jre_%{origin} %{_jvmdir}/%{jredir}
  alternatives --remove jre_%{javaver} %{_jvmdir}/%{jredir}
  alternatives --remove jre_%{javaver}_%{origin} %{_jvmdir}/%{jrelnk}

  # avoid unnecessary failure
  if [ -e %{_jvmdir}/%{uniquesuffix} ]  ; then 
    # as lua copied all necessary config files, we do not wont the double rpmnew and rpm.save
    rm -rf %{_jvmdir}/%{uniquesuffix}  
  fi
exit 0

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%post devel
# Note current status of alternatives
MAKE_THIS_DEFAULT=0
ID="%{_jvmdir}/java-%{javaver}-%{origin}.*bin/javac"
COMMAND=javac
alternatives --display $COMMAND | head -n 1 | grep -q "%{statuscheck}"
if [ $? -ne 0 ]; then
  alternatives --display $COMMAND | grep -q "%{linkcheck}"".*""$ID"
  if [ $? -eq 0 ]; then
    MAKE_THIS_DEFAULT=1
  fi
fi


ext=.gz
alternatives \
  --install %{_bindir}/javac javac %{sdkbindir}/javac %{priority} \
  --slave %{_jvmdir}/java java_sdk %{_jvmdir}/%{sdkdir} \
  --slave %{_jvmjardir}/java java_sdk_exports %{_jvmjardir}/%{sdkdir} \
  --slave %{_bindir}/appletviewer appletviewer %{sdkbindir}/appletviewer \
  --slave %{_bindir}/apt apt %{sdkbindir}/apt \
  --slave %{_bindir}/extcheck extcheck %{sdkbindir}/extcheck \
  --slave %{_bindir}/idlj idlj %{sdkbindir}/idlj \
  --slave %{_bindir}/jar jar %{sdkbindir}/jar \
  --slave %{_bindir}/jarsigner jarsigner %{sdkbindir}/jarsigner \
  --slave %{_bindir}/javadoc javadoc %{sdkbindir}/javadoc \
  --slave %{_bindir}/javah javah %{sdkbindir}/javah \
  --slave %{_bindir}/javap javap %{sdkbindir}/javap \
  --slave %{_bindir}/jcmd jcmd %{sdkbindir}/jcmd \
  --slave %{_bindir}/jconsole jconsole %{sdkbindir}/jconsole \
  --slave %{_bindir}/jdb jdb %{sdkbindir}/jdb \
  --slave %{_bindir}/jhat jhat %{sdkbindir}/jhat \
  --slave %{_bindir}/jinfo jinfo %{sdkbindir}/jinfo \
  --slave %{_bindir}/jmap jmap %{sdkbindir}/jmap \
  --slave %{_bindir}/jps jps %{sdkbindir}/jps \
  --slave %{_bindir}/jrunscript jrunscript %{sdkbindir}/jrunscript \
  --slave %{_bindir}/jsadebugd jsadebugd %{sdkbindir}/jsadebugd \
  --slave %{_bindir}/jstack jstack %{sdkbindir}/jstack \
  --slave %{_bindir}/jstat jstat %{sdkbindir}/jstat \
  --slave %{_bindir}/jstatd jstatd %{sdkbindir}/jstatd \
  --slave %{_bindir}/native2ascii native2ascii %{sdkbindir}/native2ascii \
  --slave %{_bindir}/policytool policytool %{sdkbindir}/policytool \
  --slave %{_bindir}/rmic rmic %{sdkbindir}/rmic \
  --slave %{_bindir}/schemagen schemagen %{sdkbindir}/schemagen \
  --slave %{_bindir}/serialver serialver %{sdkbindir}/serialver \
  --slave %{_bindir}/wsgen wsgen %{sdkbindir}/wsgen \
  --slave %{_bindir}/wsimport wsimport %{sdkbindir}/wsimport \
  --slave %{_bindir}/xjc xjc %{sdkbindir}/xjc \
  --slave %{_mandir}/man1/appletviewer.1$ext appletviewer.1$ext \
  %{_mandir}/man1/appletviewer-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/apt.1$ext apt.1$ext \
  %{_mandir}/man1/apt-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/extcheck.1$ext extcheck.1$ext \
  %{_mandir}/man1/extcheck-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/jar.1$ext jar.1$ext \
  %{_mandir}/man1/jar-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/jarsigner.1$ext jarsigner.1$ext \
  %{_mandir}/man1/jarsigner-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/javac.1$ext javac.1$ext \
  %{_mandir}/man1/javac-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/javadoc.1$ext javadoc.1$ext \
  %{_mandir}/man1/javadoc-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/javah.1$ext javah.1$ext \
  %{_mandir}/man1/javah-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/javap.1$ext javap.1$ext \
  %{_mandir}/man1/javap-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/jconsole.1$ext jconsole.1$ext \
  %{_mandir}/man1/jconsole-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/jdb.1$ext jdb.1$ext \
  %{_mandir}/man1/jdb-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/jhat.1$ext jhat.1$ext \
  %{_mandir}/man1/jhat-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/jinfo.1$ext jinfo.1$ext \
  %{_mandir}/man1/jinfo-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/jmap.1$ext jmap.1$ext \
  %{_mandir}/man1/jmap-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/jps.1$ext jps.1$ext \
  %{_mandir}/man1/jps-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/jrunscript.1$ext jrunscript.1$ext \
  %{_mandir}/man1/jrunscript-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/jsadebugd.1$ext jsadebugd.1$ext \
  %{_mandir}/man1/jsadebugd-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/jstack.1$ext jstack.1$ext \
  %{_mandir}/man1/jstack-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/jstat.1$ext jstat.1$ext \
  %{_mandir}/man1/jstat-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/jstatd.1$ext jstatd.1$ext \
  %{_mandir}/man1/jstatd-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/native2ascii.1$ext native2ascii.1$ext \
  %{_mandir}/man1/native2ascii-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/policytool.1$ext policytool.1$ext \
  %{_mandir}/man1/policytool-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/rmic.1$ext rmic.1$ext \
  %{_mandir}/man1/rmic-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/schemagen.1$ext schemagen.1$ext \
  %{_mandir}/man1/schemagen-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/serialver.1$ext serialver.1$ext \
  %{_mandir}/man1/serialver-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/wsgen.1$ext wsgen.1$ext \
  %{_mandir}/man1/wsgen-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/wsimport.1$ext wsimport.1$ext \
  %{_mandir}/man1/wsimport-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/xjc.1$ext xjc.1$ext \
  %{_mandir}/man1/xjc-%{uniquesuffix}.1$ext

# Gracefully update to this one if needed
%if %{graceful_links}
if [ $MAKE_THIS_DEFAULT -eq 1 ]; then
%endif
  alternatives --set $COMMAND %{sdkbindir}/javac
%if %{graceful_links}
fi
%endif

for X in %{origin} %{javaver} ; do
  # Note current status of alternatives
  MAKE_THIS_DEFAULT=0
  ID="%{_jvmdir}/java-%{javaver}-%{origin}"
  COMMAND=java_sdk_$X
  alternatives --display $COMMAND | head -n 1 | grep -q "%{statuscheck}"
  if [ $? -ne 0 ]; then
    alternatives --display $COMMAND | grep -q "%{linkcheck}"".*""$ID"
    if [ $? -eq 0 ]; then
      MAKE_THIS_DEFAULT=1
    fi
  fi

  alternatives \
    --install %{_jvmdir}/java-"$X" \
    java_sdk_"$X" %{_jvmdir}/%{sdkdir} %{priority} \
    --slave %{_jvmjardir}/java-"$X" \
    java_sdk_"$X"_exports %{_jvmjardir}/%{sdkdir}

%if %{graceful_links}
  # Gracefully update to this one if needed
  if [ $MAKE_THIS_DEFAULT -eq 1 ]; then
%endif
    alternatives --set $COMMAND %{_jvmdir}/%{sdkdir}
%if %{graceful_links}
  fi
%endif
done

update-alternatives --install %{_jvmdir}/java-%{javaver}-%{origin} java_sdk_%{javaver}_%{origin} %{_jvmdir}/%{sdkdir} %{priority} \
--slave %{_jvmjardir}/java-%{javaver}-%{origin}       java_sdk_%{javaver}_%{origin}_exports      %{_jvmjardir}/%{sdkdir}

update-desktop-database %{_datadir}/applications &> /dev/null || :
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

exit 0

%postun devel
  alternatives --remove javac %{sdkbindir}/javac
  alternatives --remove java_sdk_%{origin} %{_jvmdir}/%{sdkdir}
  alternatives --remove java_sdk_%{javaver} %{_jvmdir}/%{sdkdir}
  alternatives --remove java_sdk_%{javaver}_%{origin} %{_jvmdir}/%{sdkdir}

update-desktop-database %{_datadir}/applications &> /dev/null || :

if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

exit 0

%posttrans  devel
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%post javadoc
MAKE_THIS_DEFAULT=0
ID="%{_javadocdir}/java-%{javaver}-%{origin}.*/api"
COMMAND=javadocdir
alternatives --display $COMMAND | head -n 1 | grep -q "%{statuscheck}"
if [ $? -ne 0 ]; then
  alternatives --display $COMMAND | grep -q "%{linkcheck}"".*""$ID"
  if [ $? -eq 0 ]; then
    MAKE_THIS_DEFAULT=1
  fi
fi

alternatives \
  --install %{_javadocdir}/java javadocdir %{_javadocdir}/%{uniquejavadocdir}/api \
  %{priority}

%if %{graceful_links}
# Gracefully update to this one if needed
if [ $MAKE_THIS_DEFAULT -eq 1 ]; then
%endif
  alternatives --set $COMMAND %{_javadocdir}/%{uniquejavadocdir}/api
%if %{graceful_links}
fi
%endif

exit 0

%postun javadoc
  alternatives --remove javadocdir %{_javadocdir}/%{uniquejavadocdir}/api

exit 0


%files -f %{name}.files
%{_datadir}/icons/hicolor/*x*/apps/java-%{javaver}.png

# important note, see https://bugzilla.redhat.com/show_bug.cgi?id=1038092 for whole issue 
# all config/norepalce files (and more) have to be declared in pretrans. See pretrans
%files headless  -f %{name}.files-headless
%defattr(-,root,root,-)
%doc %{_jvmdir}/%{sdkdir}/ASSEMBLY_EXCEPTION
%doc %{_jvmdir}/%{sdkdir}/LICENSE
%doc %{_jvmdir}/%{sdkdir}/THIRD_PARTY_README
%dir %{_jvmdir}/%{sdkdir}
%dir %{_jvmdir}/%{sdkdir}/jre/lib/
%dir %{_jvmdir}/%{sdkdir}/jre/lib/%{archinstall}
%ifarch x86_64
%dir %{_jvmdir}/%{sdkdir}/jre/lib/%{archinstall}/xawt
%endif
%{_jvmdir}/%{jrelnk}
%{_jvmjardir}/%{jrelnk}
%{_jvmprivdir}/*
%{jvmjardir}
%dir %{_jvmdir}/%{jredir}/lib/security
%{_jvmdir}/%{jredir}/lib/security/cacerts
%config(noreplace) %{_jvmdir}/%{jredir}/lib/security/US_export_policy.jar
%config(noreplace) %{_jvmdir}/%{jredir}/lib/security/local_policy.jar
%config(noreplace) %{_jvmdir}/%{jredir}/lib/security/java.policy
%config(noreplace) %{_jvmdir}/%{jredir}/lib/security/java.security
%config(noreplace) %{_jvmdir}/%{jredir}/lib/logging.properties
%{_mandir}/man1/java-%{uniquesuffix}.1*
%{_mandir}/man1/keytool-%{uniquesuffix}.1*
%{_mandir}/man1/orbd-%{uniquesuffix}.1*
%{_mandir}/man1/pack200-%{uniquesuffix}.1*
%{_mandir}/man1/rmid-%{uniquesuffix}.1*
%{_mandir}/man1/rmiregistry-%{uniquesuffix}.1*
%{_mandir}/man1/servertool-%{uniquesuffix}.1*
%{_mandir}/man1/tnameserv-%{uniquesuffix}.1*
%{_mandir}/man1/unpack200-%{uniquesuffix}.1*
%config(noreplace) %{_jvmdir}/%{jredir}/lib/security/nss.cfg
%{_jvmdir}/%{jredir}/lib/audio/
%ifarch %{jit_arches}
%attr(664, root, root) %ghost %{_jvmdir}/%{jredir}/lib/%{archinstall}/server/classes.jsa
%attr(664, root, root) %ghost %{_jvmdir}/%{jredir}/lib/%{archinstall}/client/classes.jsa
%endif
%{_jvmdir}/%{jredir}/lib/%{archinstall}/server/
%{_jvmdir}/%{jredir}/lib/%{archinstall}/client/
%{_sysconfdir}/.java/
%{_sysconfdir}/.java/.systemPrefs
%{_jvmdir}/%{sdkdir}/jre-abrt


%files devel
%defattr(-,root,root,-)
%doc %{_jvmdir}/%{sdkdir}/ASSEMBLY_EXCEPTION
%doc %{_jvmdir}/%{sdkdir}/LICENSE
%doc %{_jvmdir}/%{sdkdir}/THIRD_PARTY_README
%dir %{_jvmdir}/%{sdkdir}/bin
%dir %{_jvmdir}/%{sdkdir}/include
%dir %{_jvmdir}/%{sdkdir}/lib
%ifarch %{jit_arches}
%dir %{_jvmdir}/%{sdkdir}/tapset
%endif
%{_jvmdir}/%{sdkdir}/bin/*
%{_jvmdir}/%{sdkdir}/include/*
%{_jvmdir}/%{sdkdir}/lib/*
%ifarch %{jit_arches}
%{_jvmdir}/%{sdkdir}/tapset/*.stp
%endif
%{_jvmjardir}/%{sdkdir}
%{_datadir}/applications/*jconsole.desktop
%{_datadir}/applications/*policytool.desktop
%{_mandir}/man1/appletviewer-%{uniquesuffix}.1*
%{_mandir}/man1/apt-%{uniquesuffix}.1*
%{_mandir}/man1/extcheck-%{uniquesuffix}.1*
%{_mandir}/man1/idlj-%{uniquesuffix}.1*
%{_mandir}/man1/jar-%{uniquesuffix}.1*
%{_mandir}/man1/jarsigner-%{uniquesuffix}.1*
%{_mandir}/man1/javac-%{uniquesuffix}.1*
%{_mandir}/man1/javadoc-%{uniquesuffix}.1*
%{_mandir}/man1/javah-%{uniquesuffix}.1*
%{_mandir}/man1/javap-%{uniquesuffix}.1*
%{_mandir}/man1/jconsole-%{uniquesuffix}.1*
%{_mandir}/man1/jcmd-%{uniquesuffix}.1*
%{_mandir}/man1/jdb-%{uniquesuffix}.1*
%{_mandir}/man1/jhat-%{uniquesuffix}.1*
%{_mandir}/man1/jinfo-%{uniquesuffix}.1*
%{_mandir}/man1/jmap-%{uniquesuffix}.1*
%{_mandir}/man1/jps-%{uniquesuffix}.1*
%{_mandir}/man1/jrunscript-%{uniquesuffix}.1*
%{_mandir}/man1/jsadebugd-%{uniquesuffix}.1*
%{_mandir}/man1/jstack-%{uniquesuffix}.1*
%{_mandir}/man1/jstat-%{uniquesuffix}.1*
%{_mandir}/man1/jstatd-%{uniquesuffix}.1*
%{_mandir}/man1/native2ascii-%{uniquesuffix}.1*
%{_mandir}/man1/policytool-%{uniquesuffix}.1*
%{_mandir}/man1/rmic-%{uniquesuffix}.1*
%{_mandir}/man1/schemagen-%{uniquesuffix}.1*
%{_mandir}/man1/serialver-%{uniquesuffix}.1*
%{_mandir}/man1/wsgen-%{uniquesuffix}.1*
%{_mandir}/man1/wsimport-%{uniquesuffix}.1*
%{_mandir}/man1/xjc-%{uniquesuffix}.1*
%ifarch %{jit_arches}
%{tapsetroot}
%endif

%files demo -f %{name}-demo.files
%defattr(-,root,root,-)
%doc %{_jvmdir}/%{sdkdir}/LICENSE

%files src
%defattr(-,root,root,-)
%doc README.src
%{_jvmdir}/%{sdkdir}/src.zip

%files javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/%{uniquejavadocdir}
%doc %{buildoutputdir}/j2sdk-image/jre/LICENSE

%files accessibility
%{_jvmdir}/%{jredir}/lib/%{archinstall}/libatk-wrapper.so
%{_jvmdir}/%{jredir}/lib/ext/java-atk-wrapper.jar
%{_jvmdir}/%{jredir}/lib/accessibility.properties

%changelog
* Wed Jun 11 2014 Liu Di <liudidi@gmail.com> - 1:1.7.0.60-2.5.0.22.pre04.4
- 为 Magic 3.0 重建

* Wed Jun 11 2014 Liu Di <liudidi@gmail.com> - 1:1.7.0.60-2.5.0.22.pre04.3
- 为 Magic 3.0 重建

* Wed Jun 11 2014 Liu Di <liudidi@gmail.com> - 1:1.7.0.60-2.5.0.22.pre04.2
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.7.0.60-2.5.0.22.pre04.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 30 2014 Omair Majid <omajid@redhat.com> - 1.7.0.51-2.5.0.22.f21
- Updated aarch64 tarball

* Fri May 23 2014 Omair Majid <omajid@redhat.com> - 1.7.0.51-2.5.0.21.f21
- Added aarch64-specfic version of the add-final-location-rpaths path

* Thu May 22 2014 Jiri Vanek <jvanek@redhat.com> - 1.7.0.51-2.5.0.19.f21
- python added to line SOURCE14 $files, to prevent access denied
- debug turned off
- added build requires for python
- adde patch413, rh1064383-prelink_fix.patch (gnu_andrew)
- export JDK_TO_BUILD_WITH changed to /usr/lib/jvm/java-1.7.0-openjdk, to use jdk7
  explicitly

* Thu May 22 2014 Jiri Vanek <jvanek@redhat.com> - 1.7.0.51-2.5.0.19.f21
- bumped release
- changed  buildoutputdir to contains "-debug" in case of debug on
- rewritten (long unmaintained) java-1.7.0-openjdk-debugdocs.patch and 
  java-1.7.0-openjdk-debuginfo.patch
- debug turned on (1)
- added   JAVAC_WARNINGS_FATAl="false"  tomakefile options

* Thu Apr 22 2014 Jiri Vanek <jvanek@redhat.com> - 1.7.0.51-2.5.0.18.pre04.f21
- Added Omair's fix for RH1059925
 - added and used Source14, remove-origin-from-rpaths
 - added and applied patch412 add-final-location-rpaths.patch
 - added build requires chrpath
 - adde INSTALL_LOCATION=_jvmdir/sdkdir to make swithces
- added export CFLAGS="$CFLAGS -fstack-protector-strong", fwd from f20
- disabled debug for lua script
- fwd from f20 fix to lua script (do not copy to itself)

* Tue Apr 22 2014 Jiri Vanek <jvanek@redhat.com> - 1.7.0.51-2.5.0.17.pre04.f21
- Updated to pre04
- adapted patch100, rhino.patch
- removed upstreamed patch402 gstackbounds.patch

* Wed Apr 2 2014 Jiri Vanek <jvanek@redhat.com> - 1.7.0.51-2.5.0.16.pre02.f21
- returned rm -rf to posunn of headless
- added OrderWithRequires on headless where possible

* Wed Apr 2 2014 Jiri Vanek <jvanek@redhat.com> - 1.7.0.51-2.5.0.15.pre02.f21
- removed rm -rf to posunn of headless

* Wed Mar 19 2014 Omair Majid <omajid@redhat.com> - 1.7.0.51-2.5.0.14.pre02.f21
- Fix trailing space in filename in systemtap-tapset tarball

* Thu Mar 13 2014 Jiri Vanek <jvanek@redhat.com> - 1.7.0.51-2.5.0.13.pre02.f21
- added debuginfo to lua script
- added rm -rf to posunn of headless

* Thu Mar 13 2014 Jiri Vanek <jvanek@redhat.com> - 1.7.0.51-2.5.0.12.pre02.f21
- all percentage chars in pretrans lua script doubled

* Wed Mar 12 2014 Jiri Vanek <jvanek@redhat.com> - 1.7.0.51-2.5.0.11.pre02.f21
- added pretrans script to copy config files (RH1038092) - lua version

* Mon Mar 10 2014 Omair Majid <omajid@redhat.com> - 1.7.0.51-2.5.0.10.pre02.f21
- Update to latest aarch64 code.

* Fri Mar 07 2014 Omair Majid <omajid@redhat.com> - 1.7.0.51-2.5.0.9.pre02.f21
- Improve output of `java -version` for aarch64

* Thu Mar 06 2014 Jiri Vanek <jvanek@redhat.com> - 1.7.0.51-2.5.0.8.pre02.f21
- updated aarch64 port to upstream rc4

* Thu Mar 06 2014 Jiri Vanek <jvanek@redhat.com> - 1.7.0.51-2.5.0.7.pre02.f21
- chmod of sa-jdi.jar done only if exists

* Fri Feb 28 2014 Jiri Vanek <jvanek@redhat.com> - 1.7.0.51-2.5.0.6.pre02.f21
- removed bash pretrans script. Will be replaced by lua + exec(cp) script

* Wed Feb 26 2014 Jiri Vanek <jvanek@redhat.com> - 1.7.0.51-2.5.0.5.pre02.f21
- updated aarch64 port to upstream rc3

* Fri Feb 21 2014 Jiri Vanek <jvanek@redhat.com> - 1.7.0.51-2.5.0.4.pre02.f21
- updated aarch64 port to upstream rc2

* Fri Feb 21 2014 Jiri Vanek <jvanek@redhat.com> - 1.7.0.51-2.5.0.3.pre02.f21
- updated to upstream prerelease 02

* Mon Feb 17 2014 Jiri Vanek <jvanek@redhat.com> - 1.7.0.51-2.5.0.3.pre01.f21
- added dual tarball with aarch64 port
 - added source1  aarch64-port-preview_rc1.tar.xz
- more owned dirs in JRE (RH1064500) put into if x86_64 condition
- duplicated rhino and pstack patch for aarch64 usage
- CHANGE_JPG flag added to remove-in-tree-libraries
- chmod on sa-jdi.jar not done for aarch64

* Mon Feb 17 2014 Jiri Vanek <jvanek@redhat.com> - 1.7.0.51-2.5.0.2.pre01.f21
- added pretrans script to copy config files (RH1038092)
- owned more dirs in JRE (RH1064500)

* Mon Feb 17 2014 Jiri Vanek <jvanek@redhat.com> - 1.7.0.51-2.5.0.1.pre01.f21
- adapted to icedtea-forest 2.5pre01 (sources based on tag pre01)
- added icedtea_version_presuffix macro to  track this
- added ppc64le and ppc64be macros to distinguish big and little endian PPC64
- added new PPC64 archdef block for ppc64le (gnu_andrew)
- pulseaudio removed from ppc64le build (gnu_andrew)
- removed upstreamed arch-dependent make options (gnu_andrew)
- added build requires libattr-devel (gnu_andrew)
- removed runtime requires rhino (gnu_andrew)

* Thu Jan 30 2014 Jiri Vanek <jvanek@redhat.com> - 1.7.0.51-2.4.5.1.f21
- removed or cleaning alternatives remove in posts

* Thu Jan 30 2014 Jiri Vanek <jvanek@redhat.com> - 1.7.0.51-2.4.5.0.f21
- updated to icedtea 2.4.5
 - http://blog.fuseyism.com/index.php/2014/01/29/icedtea-2-4-5-released/
- removed upstreamed or unwonted patches (thanx to gnu_andrew to pointing them out)
 - patch410 1015432.patch (upstreamed)
 - patch411 1029588.patch
 - patch412 zero-x32.diff
 - patch104 java-1.7.0-ppc-zero-jdk.patch
 - patch105 java-1.7.0-ppc-zero-hotspot.patch
- patch402 gstackbounds.patch and patch403 PStack-808293.patch applied always
 (again thanx to gnu_andrew)
- merged other gnu_andrew's changes
 - FT2_CFLAGS and FT2_LIBS hardoced values replaced by correct pkg-config calls 
 - buildver bumbed to 31
- added build requires  nss-devel
- removed build requires mercurial
- added JRE_RELEASE_VERSION and ALT_PARALLEL_COMPILE_JOBS into make call

* Fri Jan 24 2014 Jiri Vanek <jvanek@redhat.com> - 1.7.0.51-2.4.4.2.f21
- removed buildRequires: pulseaudio >= 0.9.11, as not neccessary
 -  but kept libs-devel)

* Fri Jan 17 2014 Jiri Vanek <jvanek@redhat.com> - 1.7.0.51-2.4.4.1.f21
- removed 2.3 tarball due to security issues (sync with f20)
 - this causes zero arm32 jit to not exists eny more (aprox 30% slowdown)
 - removed declarations:
  - global icedtea_version_arm32 2.3.13
  - source100  openjdk-icedtea-%{icedtea_version_arm32}.tar.xz
 - removed:
  - patch30   java-1.7.0-openjdk-java-access-bridge-security-2.3.patch
  - patch1000 rhino-2.3.patch
  - patch4020 gstackbounds-2.3.patch
  - patch4110 1029588-2.3.patch
  - patch302 systemtap.patch
  - patch401 657854-openjdk7.patch
 - with all follwing  ifarch arm calls
 - patch410 and TestCryptoLevel are now used always
 - US_export_policy.jar and  local_policy.jar are now listed always
 - make: 
  - always used DISABLE_INTREE_EC,  UNLIMITED_CRYPTO
  - removed arm32 specific DISTRO_PACKAGE_VERSION JDK_UPDATE_VERSION  JDK_BUILD_NUMBER
- added patch412 zero-x32.diff to try to fix zero builds build

* Fri Jan 10 2014 Jiri Vanek <jvanek@redhat.com> - 1.7.0.51-2.4.4.0.f21
- updated to security icedtea 2.4.4
- and arm tarball updated to security icedtea 2.3.13
 - icedtea_version set to 2.4.4
 - updatever bumped to       51
 - release reset to 0

* Mon Jan 06 2014 Jiri Vanek <jvanek@redhat.com> - 1.7.0.40-2.4.3.4.f21
- sync with f20
- added and applied patch411 1029588.patch (for 2.4)
- added and applied patch4110 1029588-2.3.patch (for 2.3)
- resolves rhbz#1029588
- added and applied for icedtea 2.4 patch410, 1015432.patch
- resolves rhbz#1015432
- changed Provides: jre-headless = %{javaver}
  to      Provides: jre-headless = %{epoch}:%{javaver}
- resolves rhbz#1046050

* Fri Oct 18 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.40-2.4.3.1.f20
- arm tarball updated to new  CPU sources 2.3.13
- removed upstreamed  patch 501 callerclass-01.patch
- removed upstreamed  patch 502 callerclass-02.patch
- removed upstreamed  patch 503 callerclass-02.patch
- removed upstreamed  patch 504 callerclass-02.patch

* Thu Oct 17 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.40-2.4.3.0.f20
- updated to new  CPU sources 2.4.3
- jdk splitted to headless and rest

* Fri Oct 04 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.40-2.4.2.11.f20
- another tapset fix 

* Fri Oct 04 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.40-2.4.2.10.f20
- abrt changed to soft dependece

* Thu Oct 03 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.40-2.4.2.9.f20
- renamed tapset source to be "versioned"
- improved agent placement

* Wed Oct 02 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.40-2.4.2.8.f20
- updated tapset to current head

* Wed Oct 02 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.40-2.4.2.7.f20
- fixed incorrect  _jvmdir/jre-javaver_origin to  _jvmdir/jre-javaver-origin link

* Tue Oct 01 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.40-2.4.2.6.f20
- added java-abrt connector

* Tue Sep 24 2013 Omair Majid <omajid@rehdat.com> - 1.7.0.40-2.4.2.5.f20
- Fix paths in tapsets for non x86_64 archs
- Allow tapsets to use client jvm on i386

* Thu Sep 19 2013 Dan Horák <dan[at]danny.cz> - 1.7.0.40-2.4.2.4.f20
- don't apply more patches on ARM

* Thu Sep 19 2013 Dan Horák <dan[at]danny.cz> - 1.7.0.40-2.4.2.3.f20
- don't apply the size_t patch on ARM

* Thu Sep 19 2013 Dan Horák <dan[at]danny.cz> - 1.7.0.40-2.4.2.2.f20
- fix build on zero arches (Andrew Hughes <gnu.andrew@redhat.com)

* Wed Sep 11 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.40-2.4.2.1.f20
- buildver replaced by updatever
- buildver reset to 60
- updatever set to 40
- added   JDK_BUILD_NUMBER=b`printf "%02d" buildver to make parameters
- buildversion included in id
- desktop icons extracted to text files

* Fri Sep 06 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.25-2.4.2.0.f20
- updated to icedtea7-forest 2.4.2
- removed upstreamed patch404  aarch64.patch
- adapted patch104 java-1.7.0-openjdk-ppc-zero-jdk.patch
- adapted patch105 java-1.7.0-openjdk-ppc-zero-hotspot.patch
- added patch404 RH661505-toBeReverted.patch, to be *reverted* during prep for non arm32 tarball
- buildver bumbed to 60

* Tue Sep 03 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.25-2.4.1.4.f20
- buildver bumbed to 31 for not arm arch
- switched back to system lcms2
 - removed patch 500 java-1.7.0-openjdk-disable-system-lcms
 - removed patch 5000 java-1.7.0-openjdk-disable-system-lcms-2.3
 - added requires for lcms2 > 2.5
- removed unnecessary patch 112 java-1.7.0-openjdk-doNotUseDisabledEcc.patch
- added and used after build source 11, TestCryptoLevel.java (non arm32 arch)

* Mon Sep 02 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.25-2.4.1.1.f20
- updated to icedtea 2.4
 - added java-1.7.0-openjdk-doNotUseDisabledEcc.patch (2.4 only)
 - added new file fsg.sh - to celan up sources
 - adapted  aarch64.patch
 - adapted  gstackbounds.patch
 - adapted  java-1.7.0-openjdk-disable-system-lcms.patch
 - adapted  java-1.7.0-openjdk-java-access-bridge-security.patch
 - adapted  java-1.7.0-openjdk-ppc-zero-hotspot.patch
 - adapted  java-1.7.0-openjdk-size_t.patch
 - adapted  java-1.7.0-openjdk.spec
 - adapted  rhino.patch
- arm32 is still using icedtea 2.3. Duplicated patches are:
 - Patch30:   java-1.7.0-openjdk-java-access-bridge-security-2.3.patch
 - Patch1000: rhino-2.3.patch
 - Patch4020: gstackbounds-2.3.patch
 - Patch5000: java-1.7.0-openjdk-disable-system-lcms-2.3.patch
 - kept for 2.3 657854-openjdk7.patch
 - kept for 2.3 callerclass-01.patch
 - kept for 2.3 callerclass-02.patch
 - kept for 2.3 callerclass-03.patch
 - kept for 2.3 callerclass-04.patch
 - kept for 2.3 systemtap.patch

* Tue Aug 20 2013 Omair Majid <omajid@redhat.com> -1.7.0.25-2.3.12.4c20
- Backport getCallerClass-related patches from upstream that are not in a release yet

* Sat Jul 27 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.25-2.3.12.3.f20
- setting of alternatives moved into conditional block controlled by graceful_links
- added graceful_links, set to enabled (1)

* Fri Jul 26 2013 Orion Poplawski <orion@cora.nwra.com> - 1.7.0.25-2.3.12.2.fc20
- Fix broken jre_exports alternatives links (bug #979128)

* Fri Jul 26 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.25-2.3.12.1.f20
- refreshed icedtea7-forest 2.3.12

* Fri Jul 26 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.25-2.3.12.0.f20
- bumped to icedtea7-forest 2.3.12
- removed upstreamed patch 405 zeroCtmp.patch
- removed upstreamed patch 406 remove_CC_COMP.patch

* Thu Jul 25 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.25-2.3.11.0.f20
- finally merged arm and main source tarballs
- updated to icedtea 2.3.11
 - http://blog.fuseyism.com/index.php/2013/07/25/icedtea-2-3-11-released/
- added removal of new jre-1.7.0-openjdk and java-1.7.0-openjdk alternatives
- removed patch 400, rhino for 2.1 and other 2.1 conditional stuff
- removed patch 103 arm-fixes.patch
- added ZERO_ARCHFLAG="-D_LITTLE_ENDIAN"  for zero (arm) builds
- temporary added already upstreamed patch 405 zeroCtmp.patch
- revert upstream changes: remove_CC_COMP.patch

* Wed Jul 24 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.25-2.3.10.11.f20
- added support for aarch64
 - aarch64 variable to be used in conditions where necessary
 - patch404  aarch64.patch (author: msalter) to add aarch64 support to makefiles
 (needs more tweeking!)
- added new alternatives jre-1.7.0-openjdk and java-1.7.0-openjdk to keep
 backward comaptibility after uniquesuffix and add/remove alternatives approach
- removed arm_arches variable in favour of standart arm one

* Mon Jul 22 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.25-2.3.10.10.f20
- removed _jvmdir/sdkdir from devel files

* Fri Jul 19 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.25-2.3.10.9.f20
- ID values are now in quotes

* Fri Jul 19 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.25-2.3.10.8.f20
- jrelnk is now just lnk, everything is pointing through jredir
- all alternatives are celaned before new one is added
- alternatives are removed after uninstall
- moved to full-version directory
- moved to add/remove alternatives process
- sdklnk removed, and substitued by  sdkdir

* Wed Jul 03 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.25-2.3.10.7.f20
- moved to xz compression of sources
- updated 2.1 tarball

* Fri Jun 28 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.25-2.3.10.6.f20
- updated java-1.7.0-openjdk-ppc-zero-hotspot.patch to pass without loose patching

* Thu Jun 27 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.25-2.3.10.5.f20
- added uniquejavadocdir to improve diffability
- all patch commands repalced by patch macro

* Thu Jun 27 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.25-2.3.10.4.f20
- Sync with upstream IcedTea7-forest 2.3.10 tag
- Fixes regressions as introduced with previous 1.7.0.25 updates
  - rhbz#978005, rhbz#977979, rhbz#976693, IcedTeaBZ#1487.

* Wed Jun 19 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.25-2.3.10.3.fc20
- update of IcedTea7-forest 2.3.10 tarball

* Thu Jun 13 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.25-2.3.10.2.fc20
- added patch1000 MBeanFix.patch to fix regressions caused by security patches

* Thu Jun 13 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.25-2.3.10.1.fc20
- arm tarball updated to 2.1.9
- build bumped to 25

* Wed Jun 12 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.19-2.3.10.0.fc20
- All full-paths now have arch
- temporarly swithced to intree lcms as it have security fixes (patch 500)
 - added  GENSRCDIR="$PWD/generated.build" to be able to
 - removed (build)requires  lcms2(-devel)
- Updated to latest IcedTea7-forest 2.3.10


* Wed Jun 05 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.19-2.3.9.12.fc20
- Added client/server directories so they can be owned
- More usage of uniquesuffix
- Renamed patch 107 to 200
- Added fix for RH857717, owned /etc/.java/ and /etc/.java/.systemPrefs

* Wed May 22 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.19-2.3.9.11.fc20
- added variable arm_arches as restriction to some cases of not jit_arches
- size_t patch adapted to 2.3 which is now default on all except arm arches

* Fri May 17 2013 Omair Majid <omajid@redhat.com> - 1.7.0.19-2.3.9.10.fc20
- Replace %{name} with %{uniquesuffix} where it's used as a unique suffix.

* Tue May 14 2013 Jiri Vanek <jvanek@redhat.com> 1.7.0.19-2.3.9.9.fc19
- patch402 gstackbounds.patch applied only to jit arches
- patch403 PStack-808293.patch likewise

* Mon May 13 2013 Jiri Vanek <jvanek@redhat.com>
- enhancements to icons
 - now points to openjdk directly instead though alternatives
 - contains full version id

* Fri May 10 2013 Adam Williamson <awilliam@redhat.com>
- update scriptlets to follow current guidelines for updating icon cache

* Tue May 07 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.19-2.3.9.8.fc20
- added patch 401 657854-openjdk7.patch (see 947731)
- fixed icons (see https://bugzilla.redhat.com/show_bug.cgi?id=820619)
- added patch 402 gstackbounds.patch - see (RH902004)
- added patch 403 PStack-808293.patch - to work more about jstack

* Mon Apr 29 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1.7.0.19-2.3.9.7
- Drop ant-nodeps dependency as it's long been provided by ant

* Mon Apr 22 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.19-2.3.9.6.fc20
- sync with f19

* Fri Apr 19 2013 Deepak Bhole <dbhole@redhat.com> - 1.7.0.19-2.3.9.3.fc20
- Updated 2.1.8 tarball
- Forcibly remove bfc files

* Thu Apr 18 2013 Deepak Bhole <dbhole@redhat.com> - 1.7.0.19-2.3.9.2.fc20
- Updated secondary arches to 2.1.8
- Removed upstreamed Zero allocation patch

* Tue Apr 16 2013 Jiri Vanek <jvanek@redhat.com - 1.7.0.19-2.3.9.1.fc20
- updated to IcedTea  2.3.9 with latest security patches
  - updated to updated IcedTea  2.3.9 with fix to one of security fixes
  -  fixed font glyph offset
- added client to ghosted classes.jsa
- buildver sync to b19
- rewritten java-1.7.0-openjdk-java-access-bridge-security.patch

* Wed Apr 10 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.9-2.3.8.6.fc20
- fixed priority (one zero deleted)
- unapplied patch2

* Thu Apr 04 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.9-2.3.8.6.fc20
- added patch107 abrt_friendly_hs_log_jdk7.patch
- removed patch2   java-1.7.0-openjdk-java-access-bridge-idlj.patch

* Wed Apr 03 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.9-2.3.8.5.fc20
- removed redundant rm of classes.jsa, ghost is handling it correctly
- removed access-gnome-bridge as deprecated technology.
 - replaced by linking to optional, install-able,  package java-atk-wrapper
 - all patches kept as valid in same way as for gnome bridge
 - question is java-1.7.0-openjdk-java-access-bridge-idlj if still valid
- commented out mysterious patch2   java-1.7.0-openjdk-java-access-bridge-idlj.patch
 - candidate for deletation

* Fri Mar 29 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.9-2.3.8.4.fc19
- Updated to java-access-bridge-1.26.2.tar.bz2

* Tue Mar 26 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.9-2.3.8.3.fc20
- added manual deletion of classes.jsa
- ghost classes.jsa restricted to jitarches and to full path
- zlib in BuildReq restricted for  1.2.3-7 or higher
 - see https://bugzilla.redhat.com/show_bug.cgi?id=904231

* Tue Mar 26 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.9-2.3.8.2.fc20
- Removed a -icedtea tag from the version
  - package have less and less connections to icedtea7
- Added link to nss as noreplace bug to previous changelog item

* Mon Mar 25 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.9-2.3.8.1.fc20
- Bumped release
- Added and applied patch500 java-1.7.0-openjdk-fixZeroAllocFailure.patch
  - to fix not-jit arches build
  - is already in upstreamed icedtea 2.1
- Added gcc-c++ build dependence. Sometimes caused troubles during rpm -bb
- Added (Build)Requires for fontconfig and xorg-x11-fonts-Type1
  - see https://bugzilla.redhat.com/show_bug.cgi?id=721033 for details
- Removed all fonconfig files. Fonts are now handled differently in JDK 
  and those files are redundant. This is going to be usptreamed.
  - see https://bugzilla.redhat.com/show_bug.cgi?id=902227 for details
- logging.properties marked as config(noreplace)
  - see https://bugzilla.redhat.com/show_bug.cgi?id=679180 for details
- classes.jsa marked as ghost 
  - see https://bugzilla.redhat.com/show_bug.cgi?id=918172 for details
- nss.cfg was marked as config(noreplace) 
  - see https://bugzilla.redhat.com/show_bug.cgi?id=913821 for details

* Mon Mar 04 2013 Omair Majid <omajid@redhat.com> - 1.7.0.9-2.3.8.fc19
- Updated to icedtea7 2.3.8 (forest)
- Removed upstreamed patches.

* Sat Feb 16 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.9-2.3.7.fc19
- Updated to 2.3.7 icedtea7 tarball
- Updated the 2.1.6 icedtea7 tarballfor arm
- Removed testing
 - mauve was outdated and
 - jtreg was icedtea relict
- Added java -Xshare:dump to post (see 513605) fo jitarchs

* Thu Feb 14 2013 Deepak Bhole <dbhole@redhat.com> - 1.7.0.9-2.3.6.fc19
- Updated to 2.3.6
- Updated the 2.1.5 tarball
- Removed upstreamed patches (Patch1000+)

* Thu Feb 14 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1.7.0.9-2.3.5.5.fc19
- rebuild for ARM fix

* Mon Feb 11 2013 Deepak Bhole <dbhole@redhat.com> - 1.7.0.9-2.3.5.4.fc19
- Updated secondary arch tarball to 2.1.5
- Made Patch100* jit-arch specific-only (not needed for 2.1.5)

* Thu Feb 07 2013 Omair Majid <omajid@redhat.com> - 1.7.0.9-2.3.5.3.fc19
- Sync logging fixes with upstream (icedtea7-forest and jdk7u)

* Thu Feb 07 2013 Deepak Bhole <dbhole@redhat.com> - 1.7.0.9-2.3.5.1.fc19
- Added patch for 8005615 to fix regression caused by fix for 6664509

* Wed Feb 06 2013 Deepak Bhole <dbhole@redhat.com> - 1.7.0.9-2.3.5.fc19.1
- Backed out 6664509 and 7201064.patch which cause regressions

* Sun Feb 03 2013 Deepak Bhole <dbhole@redhat.com> - 1.7.0.9-2.3.5.fc19
- Bumped to 2.3.5
- Removed unnecessary GENSRC flag

* Sun Feb 03 2013 Deepak Bhole <dbhole@redhat.com> - 1.7.0.9-2.3.4.2.fc19
- Bumped to 2.3.5pre (2.3.4 + Feb. 2013 CPU)

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 1:1.7.0.9-2.3.4.1.1
- rebuild due to "jpeg8-ABI" feature drop

* Wed Jan 16 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.9-2.3.4.1.fc19
- Added idlj slave to javac
- Added jcmd slave to javac
- Release incremented

* Mon Jan 14 2013 Deepak Bhole <dbhole@redhat.com> - 1.7.0.9-2.3.4.fc19
- Updated to 2.3.4

* Thu Dec 06 2012 jiri Vanek <jvanek@redhat.com> - 1.7.0.6-2.3.2.fc19.2
- introduced tmp-patches source tarball 
- added kerberos fix (see rhbz#871771)
- added OpenOffice crusher fix (see oracle's 8004344)

* Wed Oct 17 2012 Dan Horák <dan[at]danny.cz> - 1.7.0.9-2.3.3.fc19.1
- change the permission of sa-jdi.jar only on jit_arches

* Tue Oct 16 2012 Deepak Bhole <dbhole@redhat.com> - 1.7.0.9-2.3.3.fc19
- Updated to IcedTea7-forest 2.3.3 primary arches
- Updated to IcedTea7-forest 2.1.3 for secondary arches
- Change permission of sa-jdi.jar to 644 (upstream for future)
- Resolves rhbz#s 856124, 865346, 865348, 865350, 865352, 865354, 865357,
  865359, 865363, 865365, 865370, 865428, 865471, 865434, 865511, 865514,
  865519, 865531, 865541, 865568

* Fri Sep 7 2012 jiri Vanek <jvanek@redhat.com> - 1.7.0.6-2.3.1.fc19.3
- Not-jit-archs source tarball updated to openjdk-icedtea-2.1.2.tar.gz

* Thu Aug 30 2012 jiri Vanek <jvanek@redhat.com> - 1.7.0.6-2.3.1.fc19.2
- Updated to IcedTea-Forest 2.3.1
- Resolves rhbz#RH852051, CVE-2012-4681: Reintroduce PackageAccessible checks 
  removed in 6788531.
- Commented out Patch500, java-1.7.0-openjdk-removing_jvisualvm_man.patch as
  as already included in this Iced-Tea.
- Will be nice to verify after next upstream sync if it is still upstreamed

* Tue Aug 28 2012 Orcan Ogetbil <oget.fedora@gmail.com> - 1.7.0.6-2.3.fc19.1
- Add symlink to Fedora's default soundfont rhbz#541466

* Mon Aug 27 2012 Jiri Vanek <jvanek@redhat.com> - 1.7.0.6-2.3.fc19.1
- Updated to latest IcedTea7-forest-2.3
- Current build is u6
- ALT_STRIP_POLICY replaced by STRIP_POLICY
- Patch103 java-1.7.0-opendk-arm-fixes.patch split to itself and new 
  Patch106 java-1.7.0-opendk-freetype-check-fix.patch by meaning. Both applied.
- Added Patch500, java-1.7.0-openjdk-removing_jvisualvm_man.patch to remove 
  jvisualvm manpages from processing

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.7.0.5-2.2.1.10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 09 2012 Deepak Bhole <dbhole@redhat.com> - 1.7.0.5-2.2.1.fc18.9
- Added support to build older (2.1.1/u3/hs22) version on non-jit (secondary)
  arches

* Wed Jun 13 2012 jiri Vanek <jvanek@redhat.com> - 1.7.0.3-2.2.1fc18.8
- Fixed broken provides sections
- Changed java-devel requirement to be self's devel (java-1.7.0-openjdk-devel)

* Mon Jun 11 2012 jiri Vanek <jvanek@redhat.com> - 1.7.0.3-2.2.1fc18.7
- Used newly prepared tarball with security fixes
- Bump to icedtea7-forest-2.2.1
- _mandir/man1/jcmd-name.1 added to alternatives
- Updated rhino.patch
- Modified partially upstreamed patch302 - systemtap.patch
- Temporarly disabled patch102 - java-1.7.0-openjdk-size_t.patch
- Removed already upstreamed patches 104,107,108,301
  - java-1.7.0-openjdk-arm-ftbfs.patch
  - java-1.7.0-openjdk-system-zlib.patch
  - java-1.7.0-openjdk-remove-mimpure-opt.patch
  - systemtap-alloc-size-workaround.patch
- patch 105 (java-1.7.0-openjdk-ppc-zero-jdk.patch) have become 104
- patch 106 (java-1.7.0-openjdk-ppc-zero-hotspot.patch) have become 105
- Added build requires zip, which was untill now  dependence  of dependence
- Access gnome brridge jar forced to be 644

* Fri May 25 2012 Deepak Bhole <dbhole@redhat.com> - 1.7.0.3-2.1.fc17.7
- Miscellaneous fixes brought in from RHEL branch
- Resolves: rhbz#825255: Added ALT_STRIP_POLICY so that debug info is not stripped
- Moved Patch #7 (usage of system zlib) to #107

* Tue May 01 2012 Deepak Bhole <dbhole@redhat.com> - 1.7.0.3-2.1.fc17.6
- Removed VisualVM requirements
- Obsoleted java-1.6.0-openjdk*
- Added BR for zip

* Mon Mar 26 2012 Deepak Bhole <dbhole@redhat.com> - 1.7.0.3-2.1.fc17.5
- Added SystemTap fixes by Mark Wielaard

* Sat Mar 24 2012 Dan HorÃ¡k <dan[at]danny.cz>> - 1.7.0.3-2.1.fc17.4
- update paths in the ppc patches, add missing snippet

* Wed Mar 21 2012 Deepak Bhole <dbhole@redhat.com> - 1.7.0.3-2.1.fc17.3
- Reverted fix for rhbz#740762
- Fixed PPC/PPC64 build (rh804136) -- added patches from Chris Phillips
- Moved OpenJDK specific patches to 1XX series

* Mon Mar 12 2012 Deepak Bhole <dbhole@redhat.com> - 1.7.0.3-2.1.fc17.2
- Resolved rhbz#740762: java.library.path is missing some paths
- Unified spec file for x86, x86_64, ARM and s390
  - Integrated changes from Dan HorÃ¡k <dhorak@redhat.com> for Zero/s390
  - Integrated changes from Chris Phillips <chphilli@redhat.com> for Zero/ARM

* Fri Feb 24 2012 Deepak Bhole <dbhole@redhat.com> - 1.7.0.3-2.1.fc17.1
- Added flag so that debuginfo is built into classfiles (rhbz# 796400)
- Updated rhino.patch to build scripting support (rhbz# 796398)

* Tue Feb 14 2012 Deepak Bhole <dbhole@redhat.com> - 1.7.0.3-2.1
- Updated to OpenJDK7u3/IcedTea7 2.1
- Security fixes:
  - S7112642, CVE-2012-0497: Incorrect checking for graphics rendering object
  - S7082299, CVE-2011-3571: AtomicReferenceArray insufficient array type check
  - S7110687, CVE-2012-0503: Unrestricted use of TimeZone.setDefault
  - S7110700, CVE-2012-0505: Incomplete info in the deserialization exception
  - S7110683, CVE-2012-0502: KeyboardFocusManager focus stealing
  - S7088367, CVE-2011-3563: JavaSound incorrect bounds check
  - S7126960, CVE-2011-5035: Add property to limit number of request headers to the HTTP Server
  - S7118283, CVE-2012-0501: Off-by-one bug in ZIP reading code
  - S7110704, CVE-2012-0506: CORBA fix
- Add patch to fix compilation with GCC 4.7

* Tue Nov 15 2011 Deepak Bhole <dbhole@redhat.com> - 1.7.0.1-2.0.3
- Added patch to fix bug in jdk_generic_profile.sh
- Compile with generic profile to use system libraries
- Made remove-intree-libraries.sh more robust
- Added lcms requirement
- Added patch to fix glibc name clash
- Updated java version to include -icedtea

* Sun Nov 06 2011 Deepak Bhole <dbhole@redhat.com> - 1.7.0.1-2.0.2
- Added missing changelog entry

* Sun Nov 06 2011 Deepak Bhole <dbhole@redhat.com> - 1.7.0.1-2.0.1
- Updated to IcedTea 2.0 tag in the IcedTea OpenJDK7 forest
- Removed obsoleted patches
- Added system timezone support
- Revamp version/release naming scheme to make it proper
- Security fixes
  - S7000600, CVE-2011-3547: InputStream skip() information leak
  - S7019773, CVE-2011-3548: mutable static AWTKeyStroke.ctor
  - S7023640, CVE-2011-3551: Java2D TransformHelper integer overflow
  - S7032417, CVE-2011-3552: excessive default UDP socket limit under SecurityManager
  - S7046823, CVE-2011-3544: missing SecurityManager checks in scripting engine
  - S7055902, CVE-2011-3521: IIOP deserialization code execution
  - S7057857, CVE-2011-3554: insufficient pack200 JAR files uncompress error checks
  - S7064341, CVE-2011-3389: HTTPS: block-wise chosen-plaintext attack against SSL/TLS (BEAST)
  - S7070134, CVE-2011-3558: HotSpot crashes with sigsegv from PorterStemmer
  - S7077466, CVE-2011-3556: RMI DGC server remote code execution
  - S7083012, CVE-2011-3557: RMI registry privileged code execution
  - S7096936, CVE-2011-3560: missing checkSetFactory calls in HttpsURLConnection

* Mon Aug 29 2011 Deepak Bhole <dbhole@redhat.com> - 1.7.0.0-0.1.20110823.1
- Provide a "7" version of items to enfore F-16 policy of no Java 7 builds
- Resolves: rhbz#728706,  patch from Ville Skyttä <ville.skytta at iki dot fi>

* Fri Aug 05 2011 Deepak Bhole <dbhole@redhat.com> - 1.7.0.0-0.1.20110803
- Use a newer snapshot and forest on classpath.org rather than on openjdk.net
- Added in-tree-removal script to remove libraries that we manually link
- Updated snapshots
- Added DISTRO_NAME and FreeType header/lib locations
- Removed application of patch100 and patch 113 (now in forest)

* Wed Aug 03 2011 Deepak Bhole <dbhole@redhat.com> - 1.7.0.0-0.1.20110729
- Initial build from java-1.6.0-openjdk RPM
