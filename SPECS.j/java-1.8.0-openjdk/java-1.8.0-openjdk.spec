# If debug is 1, OpenJDK is built with all debug info present.
%global debug 0

%global aarch64_hg_tag  992

%global aarch64         aarch64 arm64 armv8
%global multilib_arches %{power64} sparc64 x86_64 %{aarch64} mips64el
%global jit_arches      %{ix86} x86_64 sparcv9 sparc64 %{aarch64}

# sometimes we need to distinguish big and little endian PPC64
# taken from the openjdk-1.7 spec
%global ppc64le                 ppc64le
%global ppc64be                 ppc64 ppc64p7

%ifarch x86_64
%global archinstall amd64
%endif
%ifarch ppc
%global archinstall ppc
%endif
%ifarch %{power64}
%global archinstall ppc64
%endif
%ifarch %{ppc64le}
%global archinstall ppc64le
%endif
%ifarch %{ix86}
%global archinstall i386
%endif
%ifarch ia64
%global archinstall ia64
%endif
%ifarch s390
%global archinstall s390
%endif
%ifarch s390x
%global archinstall s390x
%endif
%ifarch %{arm}
%global archinstall arm
%endif
%ifarch %{aarch64}
%global archinstall aarch64
%endif
%ifarch mips64el
%global archinstall mips64el
%endif
# 32 bit sparc, optimized for v9
%ifarch sparcv9
%global archinstall sparc
%endif
# 64 bit sparc
%ifarch sparc64
%global archinstall sparcv9
%endif
%ifnarch %{jit_arches}
%global archinstall %{_arch}
%endif

%if %{debug}
%global debugbuild slowdebug
%else
%global debugbuild release
%endif

%global buildoutputdir jdk8/build/jdk8.build

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
%global LIBDIR %{_libdir}
#backuped original one
%ifarch %{multilib_arches}
%global syslibdir       %{_prefix}/lib64
%global _libdir         %{_prefix}/lib
%global archname        %{name}.%{_arch}
%else
%global syslibdir       %{_libdir}
%global archname        %{name}
%endif

# Standard JPackage naming and versioning defines.
%global origin          openjdk
%global updatever       5
%global buildver        b13
%global aarch64_updatever 0
%global aarch64_buildver b128
# priority must be 6 digits in total
%global priority        18000%{updatever}
%global javaver         1.8.0

# Standard JPackage directories and symbolic links.
# Make 64-bit JDKs just another alternative on 64-bit architectures.
%ifarch %{multilib_arches}
%global sdklnk          java-%{javaver}-%{origin}.%{_arch}
%global jrelnk          jre-%{javaver}-%{origin}.%{_arch}
%global sdkdir          %{name}-%{version}.%{_arch}
%else
%global sdklnk          java-%{javaver}-%{origin}
%global jrelnk          jre-%{javaver}-%{origin}
%global sdkdir          %{name}-%{version}
%endif
%global jredir          %{sdkdir}/jre
%global sdkbindir       %{_jvmdir}/%{sdklnk}/bin
%global jrebindir       %{_jvmdir}/%{jrelnk}/bin
%ifarch %{multilib_arches}
%global jvmjardir       %{_jvmjardir}/%{name}-%{version}.%{_arch}
%else
%global jvmjardir       %{_jvmjardir}/%{name}-%{version}
%endif

%if %{with_systemtap}
# Where to install systemtap tapset (links)
# We would like these to be in a package specific subdir,
# but currently systemtap doesn't support that, so we have to
# use the root tapset dir for now. To distinquish between 64
# and 32 bit architectures we place the tapsets under the arch
# specific dir (note that systemtap will only pickup the tapset
# for the primary arch for now). Systemtap uses the machine name
# aka build_cpu as architecture specific directory name.
%global tapsetroot /usr/share/systemtap
%global tapsetdir %{tapsetroot}/tapset/%{_build_cpu}
%endif

# Prevent brp-java-repack-jars from being run.
%global __jar_repack 0

Name:    java-%{javaver}-%{origin}
Version: %{javaver}.%{updatever}
Release: 14.%{buildver}%{?dist}
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

# Source from upstrem OpenJDK8 project. To regenerate, use
# ./generate_source_tarball.sh jdk8u jdk8u jdk8u%{updatever}-%{buildver}
# ./generate_source_tarball.sh aarch64-port jdk8 %{aarch64_hg_tag}
Source0:  jdk8u-jdk8u%{updatever}-%{buildver}.tar.xz
Source1:  aarch64-port-jdk8-%{aarch64_buildver}-aarch64-%{aarch64_hg_tag}.tar.xz

# Custom README for -src subpackage
Source2:  README.src

Source3:  java-abrt-launcher.in

# Use 'generate_tarballs.sh' to generate the following tarballs
# They are based on code contained in the IcedTea7 project.

# Systemtap tapsets. Zipped up to keep it small.
Source8: systemtap-tapset.tar.gz

# Desktop files. Adapated from IcedTea.
Source9: jconsole.desktop.in
Source10: policytool.desktop.in

# nss configuration file
Source11: nss.cfg

# Removed libraries that we link instead
Source12: remove-intree-libraries.sh

# Ensure we aren't using the limited crypto policy
Source13: TestCryptoLevel.java

# New versions of config files with aarch64 support. This is not upstream yet.
Source100: config.guess
Source101: config.sub

# RPM/distribution specific patches

# Ignore AWTError when assistive technologies are loaded 
Patch1:   %{name}-accessible-toolkit.patch

# RHBZ 1015432
Patch2: 1015432.patch
# Restrict access to java-atk-wrapper classes
Patch3: java-atk-wrapper-security.patch
# RHBZ 808293
Patch4: PStack-808293.patch
# Allow multiple initialization of PKCS11 libraries
Patch5: multiple-pkcs11-library-init.patch
# Disable doclint for compatibility
Patch6: disable-doclint-by-default.patch
# Include all sources in src.zip
Patch7: include-all-srcs.patch
# Fix window activation in gnome-shell
Patch8: set-active-window.patch

#
# OpenJDK specific patches
#

# Allow icedtea-web to build
Patch99: applet-hole.patch

# JVM heap size changes for s390 (thanks to aph)
Patch100: %{name}-s390-java-opts.patch
# Type fixing for s390
Patch102: %{name}-size_t.patch

# Patch for PPC/PPC64
Patch103: %{name}-ppc-zero-hotspot.patch

Patch201: system-libjpeg.patch
Patch202: system-libpng.patch
Patch203: system-lcms.patch

Patch999: 0001-PPC64LE-arch-support-in-openjdk-1.8.patch
Patch1000: java-1.8.0-openjdk-mips64el-fix.patch

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: alsa-lib-devel
BuildRequires: binutils
BuildRequires: cups-devel
BuildRequires: desktop-file-utils
BuildRequires: fontconfig
BuildRequires: freetype-devel
BuildRequires: giflib-devel
BuildRequires: gcc-c++
BuildRequires: gtk2-devel
BuildRequires: lcms2-devel
BuildRequires: libjpeg-devel
BuildRequires: libpng-devel
BuildRequires: libxslt
BuildRequires: libX11-devel
BuildRequires: libXi-devel
BuildRequires: libXinerama-devel
BuildRequires: libXt-devel
BuildRequires: libXtst-devel
BuildRequires: pkgconfig
BuildRequires: xorg-x11-proto-devel
#BuildRequires: redhat-lsb
BuildRequires: zip
BuildRequires: java-1.8.0-openjdk-devel
# Zero-assembler build requirement.
%ifnarch %{jit_arches}
BuildRequires: libffi-devel
%endif

# cacerts build requirement.
BuildRequires: openssl
# execstack build requirement.
# no prelink on ARM yet
%ifnarch %{arm} %{aarch64} ppc64le
BuildRequires: prelink
%endif
%if %{with_systemtap}
BuildRequires: systemtap-sdt-devel
%endif

Requires: fontconfig
Requires: xorg-x11-fonts-Type1

# Requires rest of java
Requires: %{name}-headless = %{epoch}:%{version}-%{release}

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

%description
The OpenJDK runtime environment.


%package headless
Summary: OpenJDK Runtime Environment
Group:   Development/Languages

# Require /etc/pki/java/cacerts.
Requires: ca-certificates
# Require jpackage-utils for ownership of /usr/lib/jvm/
Requires: jpackage-utils
# Require zoneinfo data provided by tzdata-java subpackage.
Requires: tzdata-java
# Post requires alternatives to install tool alternatives.
Requires(post):   %{_sbindir}/alternatives
# Postun requires alternatives to uninstall tool alternatives.
Requires(postun): %{_sbindir}/alternatives

# Standard JPackage base provides.
Provides: jre-%{javaver}-%{origin}-headless = %{epoch}:%{version}-%{release}
Provides: jre-%{origin}-headless = %{epoch}:%{version}-%{release}
Provides: jre-%{javaver}-headless = %{epoch}:%{version}-%{release}
Provides: java-%{javaver}-headless = %{epoch}:%{version}-%{release}
Provides: jre-headless = %{javaver}
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
The OpenJDK runtime environment without audio and video support.


%package devel
Summary: OpenJDK Development Environment
Group:   Development/Tools

# Require base package.
Requires:         %{name} = %{epoch}:%{version}-%{release}
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

%description accessibility
Enables accessibility support in OpenJDK by using java-atk-wrapper. This allows
compatible at-spi2 based accessibility programs to work for AWT and Swing-based
programs.

Please note, the java-atk-wrapper is still in beta, and OpenJDK itself is still
being tuned to be working with accessibility features. There are known issues
with accessibility on, so please do not install this package unless you really
need to.


%prep
%ifarch %{aarch64}
%global source_num 1
%else
%global source_num 0
%endif

%setup -q -c -n %{name} -T -a %{source_num}
cp %{SOURCE2} .

# replace outdated configure guess script
#
# the configure macro will do this too, but it also passes a few flags not
# supported by openjdk configure script
cp %{SOURCE100} jdk8/common/autoconf/build-aux/
cp %{SOURCE101} jdk8/common/autoconf/build-aux/

# OpenJDK patches

# Remove libraries that are linked
sh %{SOURCE12}

%patch201
%patch202
%patch203


%patch1
%patch2
%patch3
%patch4
%patch5
%patch6
%patch7
%patch8

%patch99

# s390 build fixes
%ifarch s390
%patch100
%patch102
%endif

%ifarch ppc %{power64}
# PPC fixes
%patch103
%patch999 -p1
%endif

%ifarch mips64el
%patch1000
%endif

# Extract systemtap tapsets
%if %{with_systemtap}

tar xzf %{SOURCE8}

for file in tapset/*.in; do

    OUTPUT_FILE=`echo $file | sed -e s:\.in$::g`
    sed -e s:@ABS_SERVER_LIBJVM_SO@:%{_jvmdir}/%{sdkdir}/jre/lib/%{archinstall}/server/libjvm.so:g $file > $file.1
# TODO find out which architectures other than ix86 have a client vm
%ifarch %{ix86}
    sed -e s:@ABS_CLIENT_LIBJVM_SO@:%{_jvmdir}/%{sdkdir}/jre/lib/%{archinstall}/client/libjvm.so:g $file.1 > $OUTPUT_FILE
%else
    sed -e '/@ABS_CLIENT_LIBJVM_SO@/d' $file.1 > $OUTPUT_FILE
%endif
    sed -i -e s:@ABS_JAVA_HOME_DIR@:%{_jvmdir}/%{sdkdir}:g $OUTPUT_FILE
    sed -i -e s:@INSTALL_ARCH_DIR@:%{archinstall}:g $OUTPUT_FILE

done

%endif

# Prepare desktop files
for file in %{SOURCE9} %{SOURCE10} ; do
    OUTPUT_FILE=`basename $file | sed -e s:\.in$::g`
    sed -e s:@JAVA_HOME@:%{_jvmdir}/%{sdkdir}:g $file > $OUTPUT_FILE
    sed -i -e s:@VERSION@:%{version}-%{release}.%{_arch}:g $OUTPUT_FILE
done

%build
# How many cpu's do we have?
export NUM_PROC=`/usr/bin/getconf _NPROCESSORS_ONLN 2> /dev/null || :`
export NUM_PROC=${NUM_PROC:-1}

# Build IcedTea and OpenJDK.
%ifarch s390x sparc64 alpha %{power64}
export ARCH_DATA_MODEL=64
%endif
%ifarch alpha
export CFLAGS="$CFLAGS -mieee"
%endif

(cd jdk8/common/autoconf
 bash ./autogen.sh
)

mkdir -p %{buildoutputdir}

pushd %{buildoutputdir}

bash ../../configure \
%ifnarch %{jit_arches}
    --with-jvm-variants=zero \
%endif
%ifarch %{aarch64}
    --with-jvm-variants=client \
    --disable-precompiled-headers \
%endif
    --disable-zip-debug-info \
    --with-milestone="fcs" \
%ifnarch %{aarch64}
    --with-update-version=%{updatever} \
    --with-build-number=%{buildver} \
%else
    --with-build-number=%{aarch64_buildver} \
    --with-user-release-suffix="aarch64-%{aarch64_hg_tag}" \
%endif
    --with-boot-jdk=/usr/lib/jvm/java-openjdk \
    --with-debug-level=%{debugbuild} \
    --enable-unlimited-crypto \
    --with-zlib=system \
    --with-libjpeg=system \
    --with-giflib=system \
    --with-libpng=system \
    --with-lcms=system \
    --with-stdc++lib=dynamic \
    --with-num-cores="$NUM_PROC" \
    --with-extra-cflags="-fno-devirtualize" \
    --with-extra-cxxflags="-fno-devirtualize"

# The combination of FULL_DEBUG_SYMBOLS=0 and ALT_OBJCOPY=/does_not_exist
# disables FDS for all build configs and reverts to pre-FDS make logic.
# STRIP_POLICY=none says don't do any stripping. DEBUG_BINARIES=true says
# ignore all the other logic about which debug options and just do '-g'.

make \
    DEBUG_BINARIES=true \
    STRIP_POLICY=no_strip \
    POST_STRIP_CMD="" \
    LOG=trace \
    all

# the build (erroneously) removes read permissions from some jars
# this is a regression in OpenJDK 7 (our compiler):
# http://icedtea.classpath.org/bugzilla/show_bug.cgi?id=1437
find images/j2sdk-image -iname '*.jar' -exec chmod ugo+r {} \;
chmod ugo+r images/j2sdk-image/lib/ct.sym

# remove redundant *diz and *debuginfo files
find images/j2sdk-image -iname '*.diz' -exec rm {} \;
find images/j2sdk-image -iname '*.debuginfo' -exec rm {} \;

popd >& /dev/null

export JAVA_HOME=$(pwd)/%{buildoutputdir}/images/j2sdk-image

# Install java-abrt-luncher
mv $JAVA_HOME/jre/bin/java $JAVA_HOME/jre/bin/java-abrt
cat %{SOURCE3} | sed -e s:@JAVA_PATH@:%{_jvmdir}/%{jredir}/bin/java-abrt:g -e s:@LIB_DIR@:%{LIBDIR}/libabrt-java-connector.so:g > $JAVA_HOME/jre/bin/java
chmod 755 $JAVA_HOME/jre/bin/java


# Copy tz.properties
echo "sun.zoneinfo.dir=/usr/share/javazi" >> $JAVA_HOME/jre/lib/tz.properties

# Check unlimited policy has been used
$JAVA_HOME/bin/javac -d . %{SOURCE13}
$JAVA_HOME/bin/java TestCryptoLevel

# Check debug symbols are present and can identify code
SERVER_JVM="$JAVA_HOME/jre/lib/%{archinstall}/server/libjvm.so"
if [ -f "$SERVER_JVM" ] ; then
  nm -aCl "$SERVER_JVM" | grep javaCalls.cpp
fi
CLIENT_JVM="$JAVA_HOME/jre/lib/%{archinstall}/client/libjvm.so"
if [ -f "$CLIENT_JVM" ] ; then
  nm -aCl "$CLIENT_JVM" | grep javaCalls.cpp
fi
ZERO_JVM="$JAVA_HOME/jre/lib/%{archinstall}/zero/libjvm.so"
if [ -f "$ZERO_JVM" ] ; then
  nm -aCl "$ZERO_JVM" | grep javaCalls.cpp
fi

%install
rm -rf $RPM_BUILD_ROOT
STRIP_KEEP_SYMTAB=libjvm*

# Install symlink to default soundfont
install -d -m 755 $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}/lib/audio
pushd $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}/lib/audio
ln -s %{_datadir}/soundfonts/default.sf2
popd

pushd %{buildoutputdir}/images/j2sdk-image

  # Install main files.
  install -d -m 755 $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}
  cp -a bin include lib src.zip $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}
  install -d -m 755 $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}
  cp -a jre/bin jre/lib $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}

%if %{with_systemtap}
  # Install systemtap support files.
  install -dm 755 $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}/tapset
  cp -a $RPM_BUILD_DIR/%{name}/tapset/*.stp $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}/tapset/
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
  install -d -m 755 $RPM_BUILD_ROOT%{_jvmprivdir}/%{archname}/jce/vanilla

  # Install versionless symlinks.
  pushd $RPM_BUILD_ROOT%{_jvmdir}
    ln -sf %{jredir} %{jrelnk}
    ln -sf %{sdkdir} %{sdklnk}
  popd

  pushd $RPM_BUILD_ROOT%{_jvmjardir}
    ln -sf %{sdkdir} %{jrelnk}
    ln -sf %{sdkdir} %{sdklnk}
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
      $manpage .1)-%{name}.1
  done

  # Install demos and samples.
  cp -a demo $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}
  mkdir -p sample/rmi
  mv bin/java-rmi.cgi sample/rmi
  cp -a sample $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}

popd


# Install nss.cfg
install -m 644 %{SOURCE11} $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}/lib/security/


# Install Javadoc documentation.
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}
cp -a %{buildoutputdir}/docs $RPM_BUILD_ROOT%{_javadocdir}/%{name}

# Install icons and menu entries.
for s in 16 24 32 48 ; do
  install -D -p -m 644 \
    jdk8/jdk/src/solaris/classes/sun/awt/X11/java-icon${s}.png \
    $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${s}x${s}/apps/java-%{javaver}.png
done

# Install desktop files.
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/{applications,pixmaps}
for e in jconsole policytool ; do
    desktop-file-install --vendor=%{name} --mode=644 \
        --dir=$RPM_BUILD_ROOT%{_datadir}/applications $e.desktop
done

# Find JRE directories.
find $RPM_BUILD_ROOT%{_jvmdir}/%{jredir} -type d \
  | grep -v jre/lib/security \
  | sed 's|'$RPM_BUILD_ROOT'|%dir |' \
  > %{name}.files.headless
# Find JRE files.
find $RPM_BUILD_ROOT%{_jvmdir}/%{jredir} -type f -o -type l \
  | grep -v jre/lib/security \
  | sed 's|'$RPM_BUILD_ROOT'||' \
  >> %{name}.files.all
#split %{name}.files to %{name}.files-headless and %{name}.files
#see https://bugzilla.redhat.com/show_bug.cgi?id=875408
NOT_HEADLESS=\
"%{_jvmdir}/%{jredir}/lib/%{archinstall}/libjsoundalsa.so
%{_jvmdir}/%{jredir}/lib/%{archinstall}/libpulse-java.so
%{_jvmdir}/%{jredir}/lib/%{archinstall}/libsplashscreen.so
%{_jvmdir}/%{jredir}/lib/%{archinstall}/libawt_xawt.so
%{_jvmdir}/%{jredir}/lib/%{archinstall}/libjawt.so"
#filter %{name}.files from %{name}.files.all to %{name}.files-headless
ALL=`cat %{name}.files.all`
for file in $ALL ; do
    INLCUDE="NO" ;
    for blacklist in $NOT_HEADLESS ; do
    # we can not match normally, because rpmbuild will evaluate !0 result as script failure
    q=`expr match "$file" "$blacklist"` || :
    l=`expr length "$blacklist"` || :
    if [ $q -eq $l ]; then
        INLCUDE="YES" ;
    fi;
done
if [ "x$INLCUDE" = "xNO" ]; then
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

%post
update-desktop-database %{_datadir}/applications &> /dev/null || :
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
exit 0

# FIXME: identical binaries are copied, not linked. This needs to be
# fixed upstream.
%post headless
ext=.gz
alternatives \
  --install %{_bindir}/java java %{jrebindir}/java %{priority} \
  --slave %{_jvmdir}/jre jre %{_jvmdir}/%{jrelnk} \
  --slave %{_jvmjardir}/jre jre_exports %{_jvmjardir}/%{jrelnk} \
  --slave %{_bindir}/jjs jjs %{jrebindir}/jjs \
  --slave %{_bindir}/keytool keytool %{jrebindir}/keytool \
  --slave %{_bindir}/orbd orbd %{jrebindir}/orbd \
  --slave %{_bindir}/pack200 pack200 %{jrebindir}/pack200 \
  --slave %{_bindir}/rmid rmid %{jrebindir}/rmid \
  --slave %{_bindir}/rmiregistry rmiregistry %{jrebindir}/rmiregistry \
  --slave %{_bindir}/servertool servertool %{jrebindir}/servertool \
  --slave %{_bindir}/tnameserv tnameserv %{jrebindir}/tnameserv \
  --slave %{_bindir}/unpack200 unpack200 %{jrebindir}/unpack200 \
  --slave %{_mandir}/man1/java.1$ext java.1$ext \
  %{_mandir}/man1/java-%{name}.1$ext \
  --slave %{_mandir}/man1/jjs.1$ext jjs.1$ext \
  %{_mandir}/man1/jjs-%{name}.1$ext \
  --slave %{_mandir}/man1/keytool.1$ext keytool.1$ext \
  %{_mandir}/man1/keytool-%{name}.1$ext \
  --slave %{_mandir}/man1/orbd.1$ext orbd.1$ext \
  %{_mandir}/man1/orbd-%{name}.1$ext \
  --slave %{_mandir}/man1/pack200.1$ext pack200.1$ext \
  %{_mandir}/man1/pack200-%{name}.1$ext \
  --slave %{_mandir}/man1/rmid.1$ext rmid.1$ext \
  %{_mandir}/man1/rmid-%{name}.1$ext \
  --slave %{_mandir}/man1/rmiregistry.1$ext rmiregistry.1$ext \
  %{_mandir}/man1/rmiregistry-%{name}.1$ext \
  --slave %{_mandir}/man1/servertool.1$ext servertool.1$ext \
  %{_mandir}/man1/servertool-%{name}.1$ext \
  --slave %{_mandir}/man1/tnameserv.1$ext tnameserv.1$ext \
  %{_mandir}/man1/tnameserv-%{name}.1$ext \
  --slave %{_mandir}/man1/unpack200.1$ext unpack200.1$ext \
  %{_mandir}/man1/unpack200-%{name}.1$ext

alternatives \
  --install %{_jvmdir}/jre-%{origin} \
  jre_%{origin} %{_jvmdir}/%{jrelnk} %{priority} \
  --slave %{_jvmjardir}/jre-%{origin} \
  jre_%{origin}_exports %{_jvmjardir}/%{jrelnk}

alternatives \
  --install %{_jvmdir}/jre-%{javaver} \
  jre_%{javaver} %{_jvmdir}/%{jrelnk} %{priority} \
  --slave %{_jvmjardir}/jre-%{javaver} \
  jre_%{javaver}_exports %{_jvmjardir}/%{jrelnk}

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
if [ $1 -eq 0 ]
then
  alternatives --remove java %{jrebindir}/java
  alternatives --remove jre_%{origin} %{_jvmdir}/%{jrelnk}
  alternatives --remove jre_%{javaver} %{_jvmdir}/%{jrelnk}
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%post devel
ext=.gz
alternatives \
  --install %{_bindir}/javac javac %{sdkbindir}/javac %{priority} \
  --slave %{_jvmdir}/java java_sdk %{_jvmdir}/%{sdklnk} \
  --slave %{_jvmjardir}/java java_sdk_exports %{_jvmjardir}/%{sdklnk} \
  --slave %{_bindir}/appletviewer appletviewer %{sdkbindir}/appletviewer \
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
  --slave %{_bindir}/jdeps jdeps %{sdkbindir}/jdeps \
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
  %{_mandir}/man1/appletviewer-%{name}.1$ext \
  --slave %{_mandir}/man1/extcheck.1$ext extcheck.1$ext \
  %{_mandir}/man1/extcheck-%{name}.1$ext \
  --slave %{_mandir}/man1/idlj.1$ext idlj.1$ext \
  %{_mandir}/man1/idlj-%{name}.1$ext \
  --slave %{_mandir}/man1/jar.1$ext jar.1$ext \
  %{_mandir}/man1/jar-%{name}.1$ext \
  --slave %{_mandir}/man1/jarsigner.1$ext jarsigner.1$ext \
  %{_mandir}/man1/jarsigner-%{name}.1$ext \
  --slave %{_mandir}/man1/javac.1$ext javac.1$ext \
  %{_mandir}/man1/javac-%{name}.1$ext \
  --slave %{_mandir}/man1/javadoc.1$ext javadoc.1$ext \
  %{_mandir}/man1/javadoc-%{name}.1$ext \
  --slave %{_mandir}/man1/javah.1$ext javah.1$ext \
  %{_mandir}/man1/javah-%{name}.1$ext \
  --slave %{_mandir}/man1/javap.1$ext javap.1$ext \
  %{_mandir}/man1/javap-%{name}.1$ext \
  --slave %{_mandir}/man1/jcmd.1$ext jcmd.1$ext \
  %{_mandir}/man1/jcmd-%{name}.1$ext \
  --slave %{_mandir}/man1/jconsole.1$ext jconsole.1$ext \
  %{_mandir}/man1/jconsole-%{name}.1$ext \
  --slave %{_mandir}/man1/jdb.1$ext jdb.1$ext \
  %{_mandir}/man1/jdb-%{name}.1$ext \
  --slave %{_mandir}/man1/jdeps.1$ext jdeps.1$ext \
  %{_mandir}/man1/jdeps-%{name}.1$ext \
  --slave %{_mandir}/man1/jhat.1$ext jhat.1$ext \
  %{_mandir}/man1/jhat-%{name}.1$ext \
  --slave %{_mandir}/man1/jinfo.1$ext jinfo.1$ext \
  %{_mandir}/man1/jinfo-%{name}.1$ext \
  --slave %{_mandir}/man1/jmap.1$ext jmap.1$ext \
  %{_mandir}/man1/jmap-%{name}.1$ext \
  --slave %{_mandir}/man1/jps.1$ext jps.1$ext \
  %{_mandir}/man1/jps-%{name}.1$ext \
  --slave %{_mandir}/man1/jrunscript.1$ext jrunscript.1$ext \
  %{_mandir}/man1/jrunscript-%{name}.1$ext \
  --slave %{_mandir}/man1/jsadebugd.1$ext jsadebugd.1$ext \
  %{_mandir}/man1/jsadebugd-%{name}.1$ext \
  --slave %{_mandir}/man1/jstack.1$ext jstack.1$ext \
  %{_mandir}/man1/jstack-%{name}.1$ext \
  --slave %{_mandir}/man1/jstat.1$ext jstat.1$ext \
  %{_mandir}/man1/jstat-%{name}.1$ext \
  --slave %{_mandir}/man1/jstatd.1$ext jstatd.1$ext \
  %{_mandir}/man1/jstatd-%{name}.1$ext \
  --slave %{_mandir}/man1/native2ascii.1$ext native2ascii.1$ext \
  %{_mandir}/man1/native2ascii-%{name}.1$ext \
  --slave %{_mandir}/man1/policytool.1$ext policytool.1$ext \
  %{_mandir}/man1/policytool-%{name}.1$ext \
  --slave %{_mandir}/man1/rmic.1$ext rmic.1$ext \
  %{_mandir}/man1/rmic-%{name}.1$ext \
  --slave %{_mandir}/man1/schemagen.1$ext schemagen.1$ext \
  %{_mandir}/man1/schemagen-%{name}.1$ext \
  --slave %{_mandir}/man1/serialver.1$ext serialver.1$ext \
  %{_mandir}/man1/serialver-%{name}.1$ext \
  --slave %{_mandir}/man1/wsgen.1$ext wsgen.1$ext \
  %{_mandir}/man1/wsgen-%{name}.1$ext \
  --slave %{_mandir}/man1/wsimport.1$ext wsimport.1$ext \
  %{_mandir}/man1/wsimport-%{name}.1$ext \
  --slave %{_mandir}/man1/xjc.1$ext xjc.1$ext \
  %{_mandir}/man1/xjc-%{name}.1$ext

alternatives \
  --install %{_jvmdir}/java-%{origin} \
  java_sdk_%{origin} %{_jvmdir}/%{sdklnk} %{priority} \
  --slave %{_jvmjardir}/java-%{origin} \
  java_sdk_%{origin}_exports %{_jvmjardir}/%{sdklnk}

alternatives \
  --install %{_jvmdir}/java-%{javaver} \
  java_sdk_%{javaver} %{_jvmdir}/%{sdklnk} %{priority} \
  --slave %{_jvmjardir}/java-%{javaver} \
  java_sdk_%{javaver}_exports %{_jvmjardir}/%{sdklnk}

update-desktop-database %{_datadir}/applications &> /dev/null || :
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

exit 0

%postun devel
if [ $1 -eq 0 ]
then
  alternatives --remove javac %{sdkbindir}/javac
  alternatives --remove java_sdk_%{origin} %{_jvmdir}/%{sdklnk}
  alternatives --remove java_sdk_%{javaver} %{_jvmdir}/%{sdklnk}
fi

update-desktop-database %{_datadir}/applications &> /dev/null || :

if [ $1 -eq 0 ] ; then
  /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
  /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi


exit 0

%posttrans devel
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%post javadoc
alternatives \
  --install %{_javadocdir}/java javadocdir %{_javadocdir}/%{name}/api \
  %{priority}

exit 0

%postun javadoc
if [ $1 -eq 0 ]
then
  alternatives --remove javadocdir %{_javadocdir}/%{name}/api
fi

exit 0


%files -f %{name}.files
%{_datadir}/icons/hicolor/*x*/apps/java-%{javaver}.png


%files headless -f %{name}.files-headless
%defattr(-,root,root,-)
%doc %{buildoutputdir}/images/j2sdk-image/jre/ASSEMBLY_EXCEPTION
%doc %{buildoutputdir}/images/j2sdk-image/jre/LICENSE
%doc %{buildoutputdir}/images/j2sdk-image/jre/THIRD_PARTY_README

%dir %{_jvmdir}/%{sdkdir}
%{_jvmdir}/%{jrelnk}
%{_jvmjardir}/%{jrelnk}
%{_jvmprivdir}/*
%{jvmjardir}
%dir %{_jvmdir}/%{jredir}/lib/security
%{_jvmdir}/%{jredir}/lib/security/cacerts
%config(noreplace) %{_jvmdir}/%{jredir}/lib/security/java.policy
%config(noreplace) %{_jvmdir}/%{jredir}/lib/security/java.security
%config(noreplace) %{_jvmdir}/%{jredir}/lib/security/blacklisted.certs
%{_mandir}/man1/java-%{name}.1*
%{_mandir}/man1/jjs-%{name}.1*
%{_mandir}/man1/keytool-%{name}.1*
%{_mandir}/man1/orbd-%{name}.1*
%{_mandir}/man1/pack200-%{name}.1*
%{_mandir}/man1/rmid-%{name}.1*
%{_mandir}/man1/rmiregistry-%{name}.1*
%{_mandir}/man1/servertool-%{name}.1*
%{_mandir}/man1/tnameserv-%{name}.1*
%{_mandir}/man1/unpack200-%{name}.1*
%{_jvmdir}/%{jredir}/lib/security/nss.cfg
%{_jvmdir}/%{jredir}/lib/audio/
%{_jvmdir}/%{jredir}/lib/security/US_export_policy.jar
%{_jvmdir}/%{jredir}/lib/security/local_policy.jar

%files devel
%defattr(-,root,root,-)
%doc %{buildoutputdir}/images/j2sdk-image/ASSEMBLY_EXCEPTION
%doc %{buildoutputdir}/images/j2sdk-image/LICENSE
%doc %{buildoutputdir}/images/j2sdk-image/THIRD_PARTY_README
%dir %{_jvmdir}/%{sdkdir}/bin
%dir %{_jvmdir}/%{sdkdir}/include
%dir %{_jvmdir}/%{sdkdir}/lib
%if %{with_systemtap}
%dir %{_jvmdir}/%{sdkdir}/tapset
%endif
%{_jvmdir}/%{sdkdir}/bin/*
%{_jvmdir}/%{sdkdir}/include/*
%{_jvmdir}/%{sdkdir}/lib/*
%if %{with_systemtap}
%{_jvmdir}/%{sdkdir}/tapset/*.stp
%endif
%{_jvmdir}/%{sdklnk}
%{_jvmjardir}/%{sdklnk}
%{_datadir}/applications/*jconsole.desktop
%{_datadir}/applications/*policytool.desktop
%{_mandir}/man1/appletviewer-%{name}.1*
%{_mandir}/man1/extcheck-%{name}.1*
%{_mandir}/man1/idlj-%{name}.1*
%{_mandir}/man1/jar-%{name}.1*
%{_mandir}/man1/jarsigner-%{name}.1*
%{_mandir}/man1/javac-%{name}.1*
%{_mandir}/man1/javadoc-%{name}.1*
%{_mandir}/man1/javah-%{name}.1*
%{_mandir}/man1/javap-%{name}.1*
%{_mandir}/man1/jconsole-%{name}.1*
%{_mandir}/man1/jcmd-%{name}.1*
%{_mandir}/man1/jdb-%{name}.1*
%{_mandir}/man1/jdeps-%{name}.1*
%{_mandir}/man1/jhat-%{name}.1*
%{_mandir}/man1/jinfo-%{name}.1*
%{_mandir}/man1/jmap-%{name}.1*
%{_mandir}/man1/jps-%{name}.1*
%{_mandir}/man1/jrunscript-%{name}.1*
%{_mandir}/man1/jsadebugd-%{name}.1*
%{_mandir}/man1/jstack-%{name}.1*
%{_mandir}/man1/jstat-%{name}.1*
%{_mandir}/man1/jstatd-%{name}.1*
%{_mandir}/man1/native2ascii-%{name}.1*
%{_mandir}/man1/policytool-%{name}.1*
%{_mandir}/man1/rmic-%{name}.1*
%{_mandir}/man1/schemagen-%{name}.1*
%{_mandir}/man1/serialver-%{name}.1*
%{_mandir}/man1/wsgen-%{name}.1*
%{_mandir}/man1/wsimport-%{name}.1*
%{_mandir}/man1/xjc-%{name}.1*
%if %{with_systemtap}
%{tapsetroot}
%endif

%files demo -f %{name}-demo.files
%defattr(-,root,root,-)
%doc %{buildoutputdir}/images/j2sdk-image/jre/LICENSE

%files src
%defattr(-,root,root,-)
%doc README.src
%{_jvmdir}/%{sdkdir}/src.zip

%files javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/%{name}
%doc %{buildoutputdir}/images/j2sdk-image/jre/LICENSE

%files accessibility
%{_jvmdir}/%{jredir}/lib/%{archinstall}/libatk-wrapper.so
%{_jvmdir}/%{jredir}/lib/ext/java-atk-wrapper.jar
%{_jvmdir}/%{jredir}/lib/accessibility.properties

%changelog
* Mon Jun 09 2014 Liu Di <liudidi@gmail.com> - 1:1.8.0.5-14.b13
- 为 Magic 3.0 重建

* Mon Jun 09 2014 Liu Di <liudidi@gmail.com> - 1:1.8.0.5-13.b13
- 为 Magic 3.0 重建

* Mon Jun 09 2014 Liu Di <liudidi@gmail.com> - 1:1.8.0.5-12.b13
- 为 Magic 3.0 重建

* Mon Jun 09 2014 Liu Di <liudidi@gmail.com> - 1:1.8.0.5-11.b13
- 为 Magic 3.0 重建

* Mon Jun 09 2014 Liu Di <liudidi@gmail.com> - 1:1.8.0.5-10.b13
- 为 Magic 3.0 重建

* Mon Jun 02 2014 Omair Majid <omajid@redhat.com> - 1:1.8.0.5-9.b13
- Build with OpenJDK 8

* Wed May 28 2014 Omair Majid <omajid@redhat.com> - 1:1.8.0.5-8.b13
- Backport fix for JDK-8012224

* Wed May 28 2014 Omair Majid <omajid@redhat.com> - 1:1.8.0.5-7.b13
- Require fontconfig and minimal fonts (xorg-x11-fonts-Type1) explicitly
- Resolves rhbz#1101394

* Fri May 23 2014 Dan Horák <dan[at]danny.cz> - 1:1.8.0.5-6.b13
- Enable build on s390/s390x

* Tue May 20 2014 Omair Majid <omajid@redhat.com> - 1:1.8.0.5-5.b13
- Only check for debug symbols in libjvm if it exists.

* Fri May 16 2014 Omair Majid <omajid@redhat.com> - 1:1.8.0.5-4.b13
- Include all sources in src.zip

* Mon Apr 28 2014 Omair Majid <omajid@redhat.com> - 1:1.8.0.5-4.b13
- Check for debug symbols in libjvm.so

* Thu Apr 24 2014 Brent Baude <baude@us.ibm.com> - 1:1.8.0.5-3.b13
- Add ppc64le support, bz# 1088344

* Wed Apr 23 2014 Omair Majid <omajid@redhat.com> - 1:1.8.0.5-2.b13
- Build with -fno-devirtualize
- Don't strip debuginfo from files

* Wed Apr 16 2014 Omair Majid <omajid@redhat.com> - 1:1.8.0.5-1.b13
- Instrument build with various sanitizers.

* Tue Apr 15 2014 Omair Majid <omajid@redhat.com> - 1:1.8.0.5-1.b13
- Update to the latest security release: OpenJDK8 u5 b13

* Fri Mar 28 2014 Omair Majid <omajid@redhat.com> - 1:1.8.0.0-2.b132
- Include version information in desktop files
- Move desktop files from tarball to top level source

* Tue Mar 25 2014 Omair Majid <omajid@redhat.com> - 1:1.8.0.0-1.0.b132
- Switch from java8- style provides to java- style
- Bump priority to reflect java version

* Fri Mar 21 2014 Omair Majid <omajid@redhat.com> - 1:1.8.0.0-0.35.b132
- Disable doclint for compatiblity
- Patch contributed by Andrew John Hughes

* Tue Mar 11 2014 Omair Majid <omajid@redhat.com> - 1:1.8.0.0-0.34.b132
- Include jdeps and jjs for aarch64. These are present in b128.

* Mon Mar 10 2014 Omair Majid <omajid@redhat.com> - 1:1.8.0.0-0.33.b132
- Update aarch64 tarball to the latest upstream release

* Fri Mar 07 2014 Omair Majid <omajid@redhat.com> - 1:1.8.0.0-0.32.b132
- Fix `java -version` output

* Fri Mar 07 2014 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.0-0.31.b132
- updated to rc4 aarch64 tarball
- outdated removed: patch2031 system-lcmsAARCH64.patch patch2011 system-libjpeg-aarch64.patch
  patch2021 system-libpng-aarch64.patch

* Thu Mar 06 2014 Omair Majid <omajid@redhat.com> - 1:1.8.0.0-0.30.b132
- Update to b132

* Thu Mar 06 2014 Omair Majid <omajid@redhat.com> - 1:1.8.0.0-0.29.b129
- Fix typo in STRIP_POLICY

* Mon Mar 03 2014 Omair Majid <omajid@redhat.com> - 1:1.8.0.0-0.28.b129
- Remove redundant debuginfo files
- Generate complete debug information for libjvm

* Tue Feb 25 2014 Omair Majid <omajid@redhat.com> - 1:1.8.0.0-0.27.b129
- Fix non-headless libraries

* Tue Feb 25 2014 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.0-0.26.b129
- Fix incorrect Requires

* Thu Feb 13 2014 Omair Majid <omajid@redhat.com> - 1:1.8.0.0-0.26.b129
- Add -headless subpackage based on java-1.7.0-openjdk
- Add abrt connector support
- Add -accessibility subpackage

* Thu Feb 13 2014 Omair Majid <omajid@redhat.com> - 1:1.8.0.0-0.26.b129
- Update to b129.

* Fri Feb 07 2014 Omair Majid <omajid@redhat.com> - 1:1.8.0.0-0.25.b126
- Update to candidate Reference Implementation release.

* Fri Jan 31 2014 Omair Majid <omajid@redhat.com> - 1:1.8.0.0-0.24.b123
- Forward port more patches from java-1.7.0-openjdk

* Mon Jan 20 2014 Omair Majid <omajid@redhat.com> - 1:1.8.0.0-0.23.b123
- Update to jdk8-b123

* Thu Nov 14 2013 Omair Majid <omajid@redhat.com> - 1:1.8.0.0-0.22.b115
- Update to jdk8-b115

* Wed Oct 30 2013 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.0-0.21.b106
- added jre/lib/security/blacklisted.certs for aarch64
- updated to preview_rc2 aarch64 tarball

* Sun Oct 06 2013 Omair Majid <omajid@redhat.com> - 1:1.8.0.0-0.20.b106
- Fix paths in tapsets to work on non-x86_64
- Use system libjpeg

* Thu Sep 05 2013 Omair Majid <omajid@redhat.com> - 1:1.8.0.0-0.19.b106
- Fix with_systemtap conditionals

* Thu Sep 05 2013 Omair Majid <omajid@redhat.com> - 1:1.8.0.0-0.18.b106
- Update to jdk8-b106

* Tue Aug 13 2013 Deepak Bhole <dbhole@redhat.com> - 1:1.8.0.0-0.17.b89x
- Updated aarch64 to latest head
- Dropped upstreamed patches

* Wed Aug 07 2013 Omair Majid <omajid@redhat.com> - 1:1.8.0.0-0.16.b89x
- The zero fix only applies on b89 tarball

* Tue Aug 06 2013 Omair Majid <omajid@redhat.com> - 1:1.8.0.0-0.16.b89x
- Add patch to fix zero on 32-bit build

* Mon Aug 05 2013 Omair Majid <omajid@redhat.com> - 1:1.8.0.0-0.16.b89x
- Added additional build fixes for aarch64

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.8.0.0-0.16.b89x
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Aug 02 2013 Deepak Bhole <dbhole@redhat.com> - 1:1.8.0.0-0.15.b89
- Added a missing includes patch (#302/%{name}-arm64-missing-includes.patch)
- Added --disable-precompiled-headers for arm64 build

* Mon Jul 29 2013 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.0-0.14.b89
- added patch 301 - removeMswitchesFromx11.patch

* Fri Jul 26 2013 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.0-0.13.b89
- added new aarch64 tarball

* Thu Jul 25 2013 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.0-0.12.b89
- ifarchaarch64 then --with-jvm-variants=client

* Tue Jul 23 2013 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.0-0.11.b89
- prelink dependence excluded also for aaech64
- arm64 added to jitarches
- added source100 config.guess to repalce the outdated one in-tree
- added source101 config.sub  to repalce the outdated one in-tree
- added patch2011 system-libjpegAARCH64.patch (as aarch64-port is little bit diferent)
- added patch2031 system-lcmsAARCH64.patch (as aarch64-port is little bit diferent)
- added gcc-c++ build depndece so builddep will  result to better situation

* Tue Jul 23 2013 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.0-0.10.b89
- moved to latest working osurces

* Tue Jul 23 2013 Omair Majid <omajid@redhat.com> - 1:1.8.0.0-0.10.b89
- Moved  to hg clone for generating sources.

* Sun Jul 21 2013 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.0-0.9.b89
- added aarch 64 tarball, proposed usage of clone instead of tarballs

* Mon Jul 15 2013 Omair Majid <omajid@redhat.com> - 1:1.8.0.0-0.9.b89
- Switch to xz for compression
- Fixes RHBZ#979823

* Mon Jul 15 2013 Omair Majid <omajid@redhat.com> - 1:1.8.0.0-0.9.b89
- Priority should be 0 until openjdk8 is released by upstream
- Fixes RHBZ#964409

* Mon Jun 3 2013 Omair Majid <omajid@redhat.com> - 1:1.8.0.0-0.8.b89
- Fix incorrect permissions on ct.sym

* Mon May 20 2013 Omair Majid <omajid@redhat.com> - 1:1.8.0.0-0.7.b89
- Fix incorrect permissions on jars

* Fri May 10 2013 Adam Williamson <awilliam@redhat.com>
- update scriptlets to follow current guidelines for updating icon cache

* Tue Apr 30 2013 Omair Majid <omajid@redhat.com> 1:1.8.0.0-0.5.b87
- Update to b87
- Remove all rhino support; use nashorn instead
- Remove upstreamed/unapplied patches

* Tue Apr 23 2013 Karsten Hopp <karsten@redhat.com> 1:1.8.0.0-0.4.b79
- update java-1.8.0-openjdk-ppc-zero-hotspot patch
- use power64 macro

* Thu Mar 28 2013 Omair Majid <omajid@redhat.com> 1:1.8.0.0-0.3.b79
- Add build fix for zero
- Drop gstabs fixes; enable full debug info instead

* Wed Mar 13 2013 Omair Majid <omajid@redhat.com> 1:1.8.0.0-0.2.b79
- Fix alternatives priority

* Tue Mar 12 2013 Omair Majid <omajid@redhat.com> 1:1.8.0.0-0.1.b79.f19
- Update to jdk8-b79
- Initial version for Fedora 19

* Tue Sep 04 2012 Andrew John Hughes <gnu.andrew@redhat.com> - 1:1.8.0.0-b53.1
- Initial build from java-1.7.0-openjdk RPM
