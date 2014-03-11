%global nspr_version 4.10.2
%global nss_util_version 3.15.5
%global nss_softokn_version 3.15.4
%global unsupported_tools_directory %{_libdir}/nss/unsupported-tools
%global allTools "certutil cmsutil crlutil derdump modutil pk12util pp signtool signver ssltap vfychain vfyserv"

# solution taken from icedtea-web.spec
%define multilib_arches ppc64 sparc64 x86_64 ppc64le
%ifarch %{multilib_arches}
%define alt_ckbi  libnssckbi.so.%{_arch}
%else
%define alt_ckbi  libnssckbi.so
%endif

# Define if using a source archive like "nss-version.with.ckbi.version".
# To "disable", add "#" to start of line, AND a space after "%".
#% define nss_ckbi_suffix .with.ckbi.1.93

Summary:          Network Security Services
Name:             nss
Version:          3.15.5
Release:          1%{?dist}
License:          MPLv2.0
URL:              http://www.mozilla.org/projects/security/pki/nss/
Group:            System Environment/Libraries
Requires:         nspr >= %{nspr_version}
Requires:         nss-util >= %{nss_util_version}
# TODO: revert to same version as nss once we are done with the merge
Requires:         nss-softokn%{_isa} >= %{nss_softokn_version}
Requires:         nss-system-init
Requires(post):   %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:    nspr-devel >= %{nspr_version}
# TODO: revert to same version as nss once we are done with the merge
# Using '>=' but on RHEL the requires should be '='
BuildRequires:    nss-softokn-devel >= %{nss_softokn_version}
BuildRequires:    nss-util-devel >= %{nss_util_version}
BuildRequires:    sqlite-devel
BuildRequires:    zlib-devel
BuildRequires:    pkgconfig
BuildRequires:    gawk
BuildRequires:    psmisc
BuildRequires:    perl

%{!?nss_ckbi_suffix:%define full_nss_version %{version}}
%{?nss_ckbi_suffix:%define full_nss_version %{version}%{nss_ckbi_suffix}}

Source0:          %{name}-%{full_nss_version}.tar.gz
Source1:          nss.pc.in
Source2:          nss-config.in
Source3:          blank-cert8.db
Source4:          blank-key3.db
Source5:          blank-secmod.db
Source6:          blank-cert9.db
Source7:          blank-key4.db
Source8:          system-pkcs11.txt
Source9:          setup-nsssysinit.sh
Source10:         PayPalEE.cert
Source12:         %{name}-pem-20140125.tar.bz2
Source17:         TestCA.ca.cert
Source18:         TestUser50.cert
Source19:         TestUser51.cert
Source20:         nss-config.xml
Source21:         setup-nsssysinit.xml
Source22:         pkcs11.txt.xml
Source23:         cert8.db.xml
Source24:         cert9.db.xml
Source25:         key3.db.xml
Source26:         key4.db.xml
Source27:         secmod.db.xml

Patch2:           add-relro-linker-option.patch
Patch3:           renegotiate-transitional.patch
Patch6:           nss-enable-pem.patch
Patch16:          nss-539183.patch
Patch18:          nss-646045.patch
# must statically link pem against the freebl in the buildroot
# Needed only when freebl on tree has new APIS
Patch25:          nsspem-use-system-freebl.patch
# TODO: Remove this patch when the ocsp test are fixed
Patch40:          nss-3.14.0.0-disble-ocsp-test.patch
# Fedora / RHEL-only patch, the templates directory was originally introduced to support mod_revocator
Patch47:          utilwrap-include-templates.patch
# Upstream: https://bugzilla.mozilla.org/show_bug.cgi?id=902171
Patch48:          nss-versus-softoken-tests.patch
# TODO remove when we switch to building nss without softoken
Patch49:          nss-skip-bltest-and-fipstest.patch
# This patch uses the gcc-iquote dir option documented at
# http://gcc.gnu.org/onlinedocs/gcc/Directory-Options.html#Directory-Options
# to place the in-tree directories at the head of the list of list of directories
# to be searched for for header files. This ensures a build even when system 
# headers are older. Such is the case when starting an update with API changes or even private export changes.
# Once the buildroot aha been bootstrapped the patch may be removed but it doesn't hurt to keep it.
Patch50:          iquote.patch

%description
Network Security Services (NSS) is a set of libraries designed to
support cross-platform development of security-enabled client and
server applications. Applications built with NSS can support SSL v2
and v3, TLS, PKCS #5, PKCS #7, PKCS #11, PKCS #12, S/MIME, X.509
v3 certificates, and other security standards.

%package tools
Summary:          Tools for the Network Security Services
Group:            System Environment/Base
Requires:         %{name}%{?_isa} = %{version}-%{release}

%description tools
Network Security Services (NSS) is a set of libraries designed to
support cross-platform development of security-enabled client and
server applications. Applications built with NSS can support SSL v2
and v3, TLS, PKCS #5, PKCS #7, PKCS #11, PKCS #12, S/MIME, X.509
v3 certificates, and other security standards.

Install the nss-tools package if you need command-line tools to
manipulate the NSS certificate and key database.

%package sysinit
Summary:          System NSS Initialization
Group:            System Environment/Base
# providing nss-system-init without version so that it can
# be replaced by a better one, e.g. supplied by the os vendor
Provides:         nss-system-init
Requires:         nss = %{version}-%{release}
Requires(post):   coreutils, sed

%description sysinit
Default Operating System module that manages applications loading
NSS globally on the system. This module loads the system defined
PKCS #11 modules for NSS and chains with other NSS modules to load
any system or user configured modules.

%package devel
Summary:          Development libraries for Network Security Services
Group:            Development/Libraries
Provides:         nss-static = %{version}-%{release}
Requires:         nss = %{version}-%{release}
Requires:         nss-util-devel
Requires:         nss-softokn-devel
Requires:         nspr-devel >= %{nspr_version}
Requires:         pkgconfig
BuildRequires:    xmlto

%description devel
Header and Library files for doing development with Network Security Services.


%package pkcs11-devel
Summary:          Development libraries for PKCS #11 (Cryptoki) using NSS
Group:            Development/Libraries
Provides:         nss-pkcs11-devel-static = %{version}-%{release}
Requires:         nss-devel = %{version}-%{release}
# TODO: revert to using nss_softokn_version once we are done with
# the merge into to new rhel git repo
# For RHEL we should have '=' instead of '>='
Requires:         nss-softokn-freebl-devel >= %{nss_softokn_version}

%description pkcs11-devel
Library files for developing PKCS #11 modules using basic NSS 
low level services.


%prep
%setup -q
%{__cp} %{SOURCE10} -f ./nss/tests/libpkix/certs
%{__cp} %{SOURCE17} -f ./nss/tests/libpkix/certs
%{__cp} %{SOURCE18} -f ./nss/tests/libpkix/certs
%{__cp} %{SOURCE19} -f ./nss/tests/libpkix/certs
%setup -q -T -D -n %{name}-%{version} -a 12

%patch2 -p0 -b .relro
%patch3 -p0 -b .transitional
%patch6 -p0 -b .libpem
%patch16 -p0 -b .539183
%patch18 -p0 -b .646045
# link pem against buildroot's freebl, essential when mixing and matching
%patch25 -p0 -b .systemfreebl
%patch40 -p0 -b .noocsptest
%patch47 -p0 -b .templates
%patch48 -p0 -b .crypto
%patch49 -p0 -b .skipthem
%patch50 -p0 -b .iquote

#########################################################
# Higher-level libraries and test tools need access to
# module-private headers from util, freebl, and softoken
# until fixed upstream we must copy some headers locally
#########################################################

pemNeedsFromSoftoken="lowkeyi lowkeyti softoken softoknt"
for file in ${pemNeedsFromSoftoken}; do
    %{__cp} ./nss/lib/softoken/${file}.h ./nss/lib/ckfw/pem/
done

# Copying these header util the upstream bug is accepted
# Upstream https://bugzilla.mozilla.org/show_bug.cgi?id=820207
%{__cp} ./nss/lib/softoken/lowkeyi.h ./nss/cmd/rsaperf
%{__cp} ./nss/lib/softoken/lowkeyti.h ./nss/cmd/rsaperf


%build

NSS_NO_PKCS11_BYPASS=1
export NSS_NO_PKCS11_BYPASS

FREEBL_NO_DEPEND=1
export FREEBL_NO_DEPEND

# Enable compiler optimizations and disable debugging code
BUILD_OPT=1
export BUILD_OPT

# Uncomment to disable optimizations
#RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed -e 's/-O2/-O0/g'`
#export RPM_OPT_FLAGS

# Generate symbolic info for debuggers
XCFLAGS=$RPM_OPT_FLAGS
export XCFLAGS

PKG_CONFIG_ALLOW_SYSTEM_LIBS=1
PKG_CONFIG_ALLOW_SYSTEM_CFLAGS=1

export PKG_CONFIG_ALLOW_SYSTEM_LIBS
export PKG_CONFIG_ALLOW_SYSTEM_CFLAGS

NSPR_INCLUDE_DIR=`/usr/bin/pkg-config --cflags-only-I nspr | sed 's/-I//'`
NSPR_LIB_DIR=%{_libdir}

export NSPR_INCLUDE_DIR
export NSPR_LIB_DIR

export NSSUTIL_INCLUDE_DIR=`/usr/bin/pkg-config --cflags-only-I nss-util | sed 's/-I//'`
export NSSUTIL_LIB_DIR=%{_libdir}

export FREEBL_INCLUDE_DIR=`/usr/bin/pkg-config --cflags-only-I nss-softokn | sed 's/-I//'`
export FREEBL_LIB_DIR=%{_libdir}
export USE_SYSTEM_FREEBL=1
# FIXME choose one or the other style and submit a patch upstream
# wtc has suggested using NSS_USE_SYSTEM_FREEBL
export NSS_USE_SYSTEM_FREEBL=1

export FREEBL_LIBS=`/usr/bin/pkg-config --libs nss-softokn`

export SOFTOKEN_LIB_DIR=%{_libdir}
# use the system ones
export USE_SYSTEM_NSSUTIL=1
export USE_SYSTEM_SOFTOKEN=1

# tell the upstream build system what we are doing
export NSS_BUILD_WITHOUT_SOFTOKEN=1

NSS_USE_SYSTEM_SQLITE=1
export NSS_USE_SYSTEM_SQLITE

%ifarch x86_64 ppc64 ia64 s390x sparc64 aarch64 ppc64le
USE_64=1
export USE_64
%endif

# uncomment if the iquote patch is activated
export IN_TREE_FREEBL_HEADERS_FIRST=1

##### phase 1: remove util/freebl/softoken and low level tools
#
######## Remove freebl, softoken and util
%{__rm} -rf ./mozilla/security/nss/lib/freebl
%{__rm} -rf ./mozilla/security/nss/lib/softoken
%{__rm} -rf ./mozilla/security/nss/lib/util
######## Remove nss-softokn test tools
%{__rm} -rf ./mozilla/security/nss/cmd/bltest
%{__rm} -rf ./mozilla/security/nss/cmd/fipstest
%{__rm} -rf ./mozilla/security/nss/cmd/rsaperf_low

##### phase 2: build the rest of nss
# nss supports pluggable ecc
NSS_ENABLE_ECC=1
export NSS_ENABLE_ECC
NSS_ECC_MORE_THAN_SUITE_B=1
export NSS_ECC_MORE_THAN_SUITE_B

export NSS_BLTEST_NOT_AVAILABLE=1
%{__make} -C ./nss/coreconf
%{__make} -C ./nss/lib/dbm
%{__make} -C ./nss
unset NSS_BLTEST_NOT_AVAILABLE

# build the man pages clean
pushd ./nss
%{__make} clean_docs build_docs
popd

# and copy them here
for m in "%{allTools}"; do 
  cp ./nss/doc/nroff/${m}.1 .
done

# Set up our package file
# The nspr_version and nss_{util|softokn}_version globals used
# here match the ones nss has for its Requires. 
# Using the current %%{nss_softokn_version} for fedora again
%{__mkdir_p} ./dist/pkgconfig
%{__cat} %{SOURCE1} | sed -e "s,%%libdir%%,%{_libdir},g" \
                          -e "s,%%prefix%%,%{_prefix},g" \
                          -e "s,%%exec_prefix%%,%{_prefix},g" \
                          -e "s,%%includedir%%,%{_includedir}/nss3,g" \
                          -e "s,%%NSS_VERSION%%,%{version},g" \
                          -e "s,%%NSPR_VERSION%%,%{nspr_version},g" \
                          -e "s,%%NSSUTIL_VERSION%%,%{nss_util_version},g" \
                          -e "s,%%SOFTOKEN_VERSION%%,%{nss_softokn_version},g" > \
                          ./dist/pkgconfig/nss.pc

NSS_VMAJOR=`cat nss/lib/nss/nss.h | grep "#define.*NSS_VMAJOR" | awk '{print $3}'`
NSS_VMINOR=`cat nss/lib/nss/nss.h | grep "#define.*NSS_VMINOR" | awk '{print $3}'`
NSS_VPATCH=`cat nss/lib/nss/nss.h | grep "#define.*NSS_VPATCH" | awk '{print $3}'`

export NSS_VMAJOR
export NSS_VMINOR
export NSS_VPATCH

%{__cat} %{SOURCE2} | sed -e "s,@libdir@,%{_libdir},g" \
                          -e "s,@prefix@,%{_prefix},g" \
                          -e "s,@exec_prefix@,%{_prefix},g" \
                          -e "s,@includedir@,%{_includedir}/nss3,g" \
                          -e "s,@MOD_MAJOR_VERSION@,$NSS_VMAJOR,g" \
                          -e "s,@MOD_MINOR_VERSION@,$NSS_VMINOR,g" \
                          -e "s,@MOD_PATCH_VERSION@,$NSS_VPATCH,g" \
                          > ./dist/pkgconfig/nss-config

chmod 755 ./dist/pkgconfig/nss-config

%{__cat} %{SOURCE9} > ./dist/pkgconfig/setup-nsssysinit.sh
chmod 755 ./dist/pkgconfig/setup-nsssysinit.sh

%{__cp} ./nss/lib/ckfw/nssck.api ./dist/private/nss/

date +"%e %B %Y" | tr -d '\n' > date.xml
echo -n %{version} > version.xml

# configuration files and setup script
for m in %{SOURCE20} %{SOURCE21} %{SOURCE22}; do
  cp ${m} .
done
for m in nss-config.xml setup-nsssysinit.xml pkcs11.txt.xml; do
  xmlto man ${m}
done

# nss databases considered to be configuration files
for m in %{SOURCE23} %{SOURCE24} %{SOURCE25} %{SOURCE26} %{SOURCE27}; do
  cp ${m} .
done
for m in cert8.db.xml cert9.db.xml key3.db.xml key4.db.xml secmod.db.xml; do
  xmlto man ${m}
done
 

%check
if [ $DISABLETEST -eq 1 ]; then
  echo "testing disabled"
  exit 0
fi

# Begin -- copied from the build section
FREEBL_NO_DEPEND=1
export FREEBL_NO_DEPEND

BUILD_OPT=1
export BUILD_OPT

%ifarch x86_64 ppc64 ia64 s390x sparc64 aarch64 ppc64le
USE_64=1
export USE_64
%endif

export NSS_BLTEST_NOT_AVAILABLE=1

# needed for the fips manging test
export SOFTOKEN_LIB_DIR=%{_libdir}

# End -- copied from the build section

# enable the following line to force a test failure
# find ./nss -name \*.chk | xargs rm -f

# Run test suite.
# In order to support multiple concurrent executions of the test suite
# (caused by concurrent RPM builds) on a single host,
# we'll use a random port. Also, we want to clean up any stuck
# selfserv processes. If process name "selfserv" is used everywhere,
# we can't simply do a "killall selfserv", because it could disturb
# concurrent builds. Therefore we'll do a search and replace and use
# a different process name.
# Using xargs doesn't mix well with spaces in filenames, in order to
# avoid weird quoting we'll require that no spaces are being used.

SPACEISBAD=`find ./nss/tests | grep -c ' '` ||:
if [ $SPACEISBAD -ne 0 ]; then
  echo "error: filenames containing space are not supported (xargs)"
  exit 1
fi
MYRAND=`perl -e 'print 9000 + int rand 1000'`; echo $MYRAND ||:
RANDSERV=selfserv_${MYRAND}; echo $RANDSERV ||:
DISTBINDIR=`ls -d ./dist/*.OBJ/bin`; echo $DISTBINDIR ||:
pushd `pwd`
cd $DISTBINDIR
ln -s selfserv $RANDSERV
popd
# man perlrun, man perlrequick
# replace word-occurrences of selfserv with selfserv_$MYRAND
find ./nss/tests -type f |\
  grep -v "\.db$" |grep -v "\.crl$" | grep -v "\.crt$" |\
  grep -vw CVS  |xargs grep -lw selfserv |\
  xargs -l perl -pi -e "s/\bselfserv\b/$RANDSERV/g" ||:

killall $RANDSERV || :

rm -rf ./tests_results
cd ./nss/tests/
# all.sh is the test suite script

#  don't need to run all the tests when testing packaging
#  nss_cycles: standard pkix upgradedb sharedb
nss_tests="cipher libpkix cert dbtests tools fips sdr crmf smime ssl ocsp merge pkits chains"
#  nss_ssl_tests: crl bypass_normal normal_bypass normal_fips fips_normal iopr
#  nss_ssl_run: cov auth stress
#
# Uncomment these lines if you need to temporarily
# disable some test suites for faster test builds
# global nss_ssl_tests "normal_fips"
# global nss_ssl_run "cov auth"

HOST=localhost DOMSUF=localdomain PORT=$MYRAND NSS_CYCLES=%{?nss_cycles} NSS_TESTS=%{?nss_tests} NSS_SSL_TESTS=%{?nss_ssl_tests} NSS_SSL_RUN=%{?nss_ssl_run} ./all.sh

cd ../../

killall $RANDSERV || :

TEST_FAILURES=`grep -c FAILED ./tests_results/security/localhost.1/output.log` || :
if [ $TEST_FAILURES -ne 0 ]; then
  echo "error: test suite returned failure(s)"
  exit 1
fi
echo "test suite completed"

%install

%{__rm} -rf $RPM_BUILD_ROOT

# There is no make install target so we'll do it ourselves.

%{__mkdir_p} $RPM_BUILD_ROOT/%{_includedir}/nss3
%{__mkdir_p} $RPM_BUILD_ROOT/%{_includedir}/nss3/templates
%{__mkdir_p} $RPM_BUILD_ROOT/%{_bindir}
%{__mkdir_p} $RPM_BUILD_ROOT/%{_libdir}
%{__mkdir_p} $RPM_BUILD_ROOT/%{unsupported_tools_directory}
%{__mkdir_p} $RPM_BUILD_ROOT/%{_libdir}/pkgconfig

mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man5

touch $RPM_BUILD_ROOT%{_libdir}/libnssckbi.so
%{__install} -p -m 755 dist/*.OBJ/lib/libnssckbi.so $RPM_BUILD_ROOT/%{_libdir}/nss/libnssckbi.so

# Copy the binary libraries we want
for file in libnss3.so libnsspem.so libnsssysinit.so libsmime3.so libssl3.so
do
  %{__install} -p -m 755 dist/*.OBJ/lib/$file $RPM_BUILD_ROOT/%{_libdir}
done

# Install the empty NSS db files
# Legacy db
%{__mkdir_p} $RPM_BUILD_ROOT/%{_sysconfdir}/pki/nssdb
%{__install} -p -m 644 %{SOURCE3} $RPM_BUILD_ROOT/%{_sysconfdir}/pki/nssdb/cert8.db
%{__install} -p -m 644 %{SOURCE4} $RPM_BUILD_ROOT/%{_sysconfdir}/pki/nssdb/key3.db
%{__install} -p -m 644 %{SOURCE5} $RPM_BUILD_ROOT/%{_sysconfdir}/pki/nssdb/secmod.db
# Shared db
%{__install} -p -m 644 %{SOURCE6} $RPM_BUILD_ROOT/%{_sysconfdir}/pki/nssdb/cert9.db
%{__install} -p -m 644 %{SOURCE7} $RPM_BUILD_ROOT/%{_sysconfdir}/pki/nssdb/key4.db
%{__install} -p -m 644 %{SOURCE8} $RPM_BUILD_ROOT/%{_sysconfdir}/pki/nssdb/pkcs11.txt
     
# Copy the development libraries we want
for file in libcrmf.a libnssb.a libnssckfw.a
do
  %{__install} -p -m 644 dist/*.OBJ/lib/$file $RPM_BUILD_ROOT/%{_libdir}
done

# Copy the binaries we want
for file in certutil cmsutil crlutil modutil pk12util signtool signver ssltap
do
  %{__install} -p -m 755 dist/*.OBJ/bin/$file $RPM_BUILD_ROOT/%{_bindir}
done

# Copy the binaries we ship as unsupported
for file in atob btoa derdump ocspclnt pp selfserv strsclnt symkeyutil tstclnt vfyserv vfychain
do
  %{__install} -p -m 755 dist/*.OBJ/bin/$file $RPM_BUILD_ROOT/%{unsupported_tools_directory}
done

# Copy the include files we want
for file in dist/public/nss/*.h
do
  %{__install} -p -m 644 $file $RPM_BUILD_ROOT/%{_includedir}/nss3
done

# Copy the template files we want
for file in dist/private/nss/nssck.api
do
  %{__install} -p -m 644 $file $RPM_BUILD_ROOT/%{_includedir}/nss3/templates
done

# Copy the package configuration files
%{__install} -p -m 644 ./dist/pkgconfig/nss.pc $RPM_BUILD_ROOT/%{_libdir}/pkgconfig/nss.pc
%{__install} -p -m 755 ./dist/pkgconfig/nss-config $RPM_BUILD_ROOT/%{_bindir}/nss-config
# Copy the pkcs #11 configuration script
%{__install} -p -m 755 ./dist/pkgconfig/setup-nsssysinit.sh $RPM_BUILD_ROOT/%{_bindir}/setup-nsssysinit.sh
# install a symbolic link to it, without the ".sh" suffix,
# that matches the man page documentation
ln -r -s -f $RPM_BUILD_ROOT/%{_bindir}/setup-nsssysinit.sh $RPM_BUILD_ROOT/%{_bindir}/setup-nsssysinit

# Copy the man pages for scripts
for f in nss-config setup-nsssysinit; do 
   install -c -m 644 ${f}.1 $RPM_BUILD_ROOT%{_mandir}/man1/${f}.1
done
# Copy the man pages for the nss tools
for f in "%{allTools}"; do 
   install -c -m 644 ${f}.1 $RPM_BUILD_ROOT%{_mandir}/man1/${f}.1
done
# Copy the man pages for the configuration files
for f in pkcs11.txt; do 
   install -c -m 644 ${f}.5 $RPM_BUILD_ROOT%{_mandir}/man5/${f}.5
done
# Copy the man pages for the nss databases
for f in cert8.db cert9.db key3.db key4.db secmod.db; do 
   install -c -m 644 ${f}.5 $RPM_BUILD_ROOT%{_mandir}/man5/${f}.5
done

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%triggerpostun -n nss-sysinit -- nss-sysinit < 3.12.8-3
# Reverse unwanted disabling of sysinit by faulty preun sysinit scriplet
# from previous versions of nss.spec
/usr/bin/setup-nsssysinit.sh on

%post
# If we upgrade, and the shared filename is a regular file, then we must
# remove it, before we can install the alternatives symbolic link.
if [ $1 -gt 1 ] ; then
  # when upgrading or downgrading
  if ! test -L %{_libdir}/libnssckbi.so; then
    rm -f %{_libdir}/libnssckbi.so
  fi
fi
# Install the symbolic link
# FYI: Certain other packages use alternatives --set to enforce that the first
# installed package is preferred. We don't do that. Highest priority wins.
%{_sbindir}/update-alternatives --install %{_libdir}/libnssckbi.so \
  %{alt_ckbi} %{_libdir}/nss/libnssckbi.so 10
/sbin/ldconfig

%postun
if [ $1 -eq 0 ] ; then
  # package removal
  %{_sbindir}/update-alternatives --remove %{alt_ckbi} %{_libdir}/nss/libnssckbi.so
else
  # upgrade or downgrade
  # If the new installed package uses a regular file (not a symblic link),
  # then cleanup the alternatives link.
  if ! test -L %{_libdir}/libnssckbi.so; then
    %{_sbindir}/update-alternatives --remove %{alt_ckbi} %{_libdir}/nss/libnssckbi.so
  fi
fi
/sbin/ldconfig

%posttrans
# An earlier version of this package had an incorrect %%postun script (3.14.3-9).
# (The incorrect %%postun always called "update-alternatives --remove",
# because it incorrectly assumed that test -f returns false for symbolic links.)
# The only possible remedy to fix the mistake that "always removes on upgrade"
# made by the older %%postun script, is to repair it in %%posttrans of the new package.
# Strategy:
# %%posttrans is never called when uninstalling.
# %%posttrans is only called when installing or upgrading a package.
# Because %%posttrans is the very last action of a package install,
# %%{_libdir}/libnssckbi.so must exist.
# If it does not, it's the result of the incorrect removal from a broken %%postun.
# In this case, we repeat installation of the alternatives link.
if ! test -e %{_libdir}/libnssckbi.so; then
  %{_sbindir}/update-alternatives --install %{_libdir}/libnssckbi.so \
    %{alt_ckbi} %{_libdir}/nss/libnssckbi.so 10
fi


%files
%defattr(-,root,root)
%{_libdir}/libnss3.so
%{_libdir}/libssl3.so
%{_libdir}/libsmime3.so
%ghost %{_libdir}/libnssckbi.so
%{_libdir}/nss/libnssckbi.so
%{_libdir}/libnsspem.so
%dir %{_sysconfdir}/pki/nssdb
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/pki/nssdb/cert8.db
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/pki/nssdb/key3.db
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/pki/nssdb/secmod.db
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/pki/nssdb/cert9.db
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/pki/nssdb/key4.db
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/pki/nssdb/pkcs11.txt
%attr(0644,root,root) %doc /usr/share/man/man5/cert8.db.5.gz
%attr(0644,root,root) %doc /usr/share/man/man5/key3.db.5.gz
%attr(0644,root,root) %doc /usr/share/man/man5/secmod.db.5.gz
%attr(0644,root,root) %doc /usr/share/man/man5/cert9.db.5.gz
%attr(0644,root,root) %doc /usr/share/man/man5/key4.db.5.gz
%attr(0644,root,root) %doc /usr/share/man/man5/pkcs11.txt.5.gz

%files sysinit
%defattr(-,root,root)
%{_libdir}/libnsssysinit.so
%{_bindir}/setup-nsssysinit.sh
# symbolic link to setup-nsssysinit.sh
%{_bindir}/setup-nsssysinit
%attr(0644,root,root) %doc /usr/share/man/man1/setup-nsssysinit.1.gz

%files tools
%defattr(-,root,root)
%{_bindir}/certutil
%{_bindir}/cmsutil
%{_bindir}/crlutil
%{_bindir}/modutil
%{_bindir}/pk12util
%{_bindir}/signtool
%{_bindir}/signver
%{_bindir}/ssltap
%{unsupported_tools_directory}/atob
%{unsupported_tools_directory}/btoa
%{unsupported_tools_directory}/derdump
%{unsupported_tools_directory}/ocspclnt
%{unsupported_tools_directory}/pp
%{unsupported_tools_directory}/selfserv
%{unsupported_tools_directory}/strsclnt
%{unsupported_tools_directory}/symkeyutil
%{unsupported_tools_directory}/tstclnt
%{unsupported_tools_directory}/vfyserv
%{unsupported_tools_directory}/vfychain
# instead of %%{_mandir}/man*/* let's list them explicitely
# supported tools
%attr(0644,root,root) %doc /usr/share/man/man1/certutil.1.gz
%attr(0644,root,root) %doc /usr/share/man/man1/cmsutil.1.gz
%attr(0644,root,root) %doc /usr/share/man/man1/crlutil.1.gz
%attr(0644,root,root) %doc /usr/share/man/man1/modutil.1.gz
%attr(0644,root,root) %doc /usr/share/man/man1/pk12util.1.gz
%attr(0644,root,root) %doc /usr/share/man/man1/signtool.1.gz
%attr(0644,root,root) %doc /usr/share/man/man1/signver.1.gz
# unsupported tools
%attr(0644,root,root) %doc /usr/share/man/man1/derdump.1.gz
%attr(0644,root,root) %doc /usr/share/man/man1/pp.1.gz
%attr(0644,root,root) %doc /usr/share/man/man1/ssltap.1.gz
%attr(0644,root,root) %doc /usr/share/man/man1/vfychain.1.gz
%attr(0644,root,root) %doc /usr/share/man/man1/vfyserv.1.gz

%files devel
%defattr(-,root,root)
%{_libdir}/libcrmf.a
%{_libdir}/pkgconfig/nss.pc
%{_bindir}/nss-config
%attr(0644,root,root) %doc /usr/share/man/man1/nss-config.1.gz

%dir %{_includedir}/nss3
%{_includedir}/nss3/cert.h
%{_includedir}/nss3/certdb.h
%{_includedir}/nss3/certt.h
%{_includedir}/nss3/cmmf.h
%{_includedir}/nss3/cmmft.h
%{_includedir}/nss3/cms.h
%{_includedir}/nss3/cmsreclist.h
%{_includedir}/nss3/cmst.h
%{_includedir}/nss3/crmf.h
%{_includedir}/nss3/crmft.h
%{_includedir}/nss3/cryptohi.h
%{_includedir}/nss3/cryptoht.h
%{_includedir}/nss3/sechash.h
%{_includedir}/nss3/jar-ds.h
%{_includedir}/nss3/jar.h
%{_includedir}/nss3/jarfile.h
%{_includedir}/nss3/key.h
%{_includedir}/nss3/keyhi.h
%{_includedir}/nss3/keyt.h
%{_includedir}/nss3/keythi.h
%{_includedir}/nss3/nss.h
%{_includedir}/nss3/nssckbi.h
%{_includedir}/nss3/nsspem.h
%{_includedir}/nss3/ocsp.h
%{_includedir}/nss3/ocspt.h
%{_includedir}/nss3/p12.h
%{_includedir}/nss3/p12plcy.h
%{_includedir}/nss3/p12t.h
%{_includedir}/nss3/pk11func.h
%{_includedir}/nss3/pk11pqg.h
%{_includedir}/nss3/pk11priv.h
%{_includedir}/nss3/pk11pub.h
%{_includedir}/nss3/pk11sdr.h
%{_includedir}/nss3/pkcs12.h
%{_includedir}/nss3/pkcs12t.h
%{_includedir}/nss3/pkcs7t.h
%{_includedir}/nss3/preenc.h
%{_includedir}/nss3/secmime.h
%{_includedir}/nss3/secmod.h
%{_includedir}/nss3/secmodt.h
%{_includedir}/nss3/secpkcs5.h
%{_includedir}/nss3/secpkcs7.h
%{_includedir}/nss3/smime.h
%{_includedir}/nss3/ssl.h
%{_includedir}/nss3/sslerr.h
%{_includedir}/nss3/sslproto.h
%{_includedir}/nss3/sslt.h


%files pkcs11-devel
%defattr(-, root, root)
%{_includedir}/nss3/nssbase.h
%{_includedir}/nss3/nssbaset.h
%{_includedir}/nss3/nssckepv.h
%{_includedir}/nss3/nssckft.h
%{_includedir}/nss3/nssckfw.h
%{_includedir}/nss3/nssckfwc.h
%{_includedir}/nss3/nssckfwt.h
%{_includedir}/nss3/nssckg.h
%{_includedir}/nss3/nssckmdt.h
%{_includedir}/nss3/nssckt.h
%{_includedir}/nss3/templates/nssck.api
%{_libdir}/libnssb.a
%{_libdir}/libnssckfw.a


%changelog
* Wed Feb 19 2014 Elio Maldonado <emaldona@redhat.com> - 3.15.5-1
- Update to nss-3.15.5
- Temporarily requiring only nss_softokn_version >= 3.15.4
- Fix location of sharedb files and their manpages
- Move cert9.db, key4.db, and pkcs11.txt to the main package
- Move nss-sysinit manpages tar archives to the main package
- Resolves: Bug 1066877 - nss-3.15.5 is available
- Resolves: Bug 1067091 - Move sharedb files to the %%files section

* Thu Feb 06 2014 Elio Maldonado <emaldona@redhat.com> - 3.15.4-5
- Revert previous change that moved some sysinit manpages
- Restore nss-sysinit manpages tar archives to %%files sysinit
- Removing spurious wildcard entry was the only change needed

* Mon Jan 27 2014 Elio Maldonado <emaldona@redhat.com> - 3.15.4-4
- Add explanatory comments for iquote.patch as was done on f20

* Sat Jan 25 2014 Elio Maldonado <emaldona@redhat.com> - 3.15.4-3
- Update pem sources to latest from nss-pem upstream
- Pick up pem fixes verified on RHEL and applied upstream
- Fix a problem where same files in two rpms created rpm conflict
- Move some nss-sysinit manpages tar archives to the %%files the
- All man pages are listed by name so there shouldn't be wildcard inclusion
- Add support for ppc64le, Resolves: Bug 1052545

* Mon Jan 20 2014 Peter Robinson <pbrobinson@fedoraproject.org> 3.15.4-2
- ARM tests pass so remove ARM conditional

* Tue Jan 07 2014 Elio Maldonado <emaldona@redhat.com> - 3.15.4-1
- Update to nss-3.15.4 (hg tag NSS_3_15_4_RTM)
- Resolves: Bug 1049229 - nss-3.15.4 is available
- Update pem sources to latest from the interim upstream for pem
- Remove no longer needed patches
- Update pem/rsawrapr.c patch on account of upstream changes to freebl/softoken
- Update iquote.patch on account of upstream changes

* Wed Dec 11 2013 Elio Maldonado <emaldona@redhat.com> - 3.15.3.1-1
- Update to nss-3.15.3.1 (hg tag NSS_3_15_3_1_RTM)
- Resolves: Bug 1040282 - nss: Mis-issued ANSSI/DCSSI certificate (MFSA 2013-117)
- Resolves: Bug 1040192 - nss-3.15.3.1 is available

* Tue Dec 03 2013 Elio Maldonado <emaldona@redhat.com> - 3.15.3-2
- Bump the release tag

* Sun Nov 24 2013 Elio Maldonado <emaldona@redhat.com> - 3.15.3-1
- Update to NSS_3_15_3_RTM
- Resolves: Bug 1031897 - CVE-2013-5605 CVE-2013-5606 CVE-2013-1741 nss: various flaws
- Fix option descriptions for setup-nsssysinit manpage
- Fix man page of nss-sysinit wrong path and other flaws
- Document email option for certutil manpage
- Remove unused patches

* Sun Oct 27 2013 Elio Maldonado <emaldona@redhat.com> - 3.15.2-3
- Revert one change from last commit to preserve full nss pluggable ecc supprt [1019245]

* Wed Oct 23 2013 Elio Maldonado <emaldona@redhat.com> - 3.15.2-2
- Use the full sources from upstream
- Bug 1019245 - ECDHE in openssl available -> NSS needs too for Firefox/Thunderbird

* Thu Sep 26 2013 Elio Maldonado <emaldona@redhat.com> - 3.15.2-1
- Update to NSS_3_15_2_RTM
- Update iquote.patch on account of modified prototype on cert.h installed by nss-devel

* Wed Aug 28 2013 Elio Maldonado <emaldona@redhat.com> - 3.15.1-7
- Update pem sources to pick up a patch applied upstream which a faulty merge had missed
- The pem module should not require unique file basenames

* Tue Aug 27 2013 Elio Maldonado <emaldona@redhat.com> - 3.15.1-6
- Update pem sources to the latest from interim upstream

* Mon Aug 19 2013 Elio Maldonado <emaldona@redhat.com> - 3.15.1-5
- Resolves: rhbz#996639 - Minor bugs in nss man pages
- Fix some typos and improve description and see also sections

* Sun Aug 11 2013 Elio Maldonado <emaldona@redhat.com> - 3.15.1-4
- Cleanup spec file to address most rpmlint errors and warnings
- Using double percent symbols to fix macro-in-comment warnings
- Ignore unversioned-explicit-provides nss-system-init per spec comments
- Ignore invalid-url Source0 as it comes from the git lookaside cache
- Ignore invalid-url Source12 as it comes from the git lookaside cache

* Thu Jul 25 2013 Elio Maldonado <emaldona@redhat.com> - 3.15.1-3
- Add man page for pkcs11.txt configuration file and cert and key databases
- Resolves: rhbz#985114 - Provide man pages for the nss configuration files

* Fri Jul 19 2013 Elio Maldonado <emaldona@redhat.com> - 3.15.1-2
- Fix errors in the man pages
- Resolves: rhbz#984106 - Add missing option descriptions to man pages for {cert|cms|crl}util
- Resolves: rhbz#982856 - Fix path to script in man page for nss-sysinit

* Tue Jul 02 2013 Elio Maldonado <emaldona@redhat.com> - 3.15.1-1
- Update to NSS_3_15_1_RTM
- Enable the iquote.patch to access newly introduced types

* Wed Jun 19 2013 Elio Maldonado <emaldona@redhat.com> - 3.15-5
- Install man pages for nss-tools and the nss-config and setup-nsssysinit scripts
- Resolves: rhbz#606020 - nss security tools lack man pages

* Tue Jun 18 2013 emaldona <emaldona@redhat.com> - 3.15-4
- Build nss without softoken or util sources in the tree
- Resolves: rhbz#689918

* Mon Jun 17 2013 emaldona <emaldona@redhat.com> - 3.15-3
- Update ssl-cbc-random-iv-by-default.patch

* Sun Jun 16 2013 Elio Maldonado <emaldona@redhat.com> - 3.15-2
- Fix generation of NSS_VMAJOR, NSS_VMINOR, and NSS_VPATCH for nss-config

* Sat Jun 15 2013 Elio Maldonado <emaldona@redhat.com> - 3.15-1
- Update to NSS_3_15_RTM

* Wed Apr 24 2013 Elio Maldonado <emaldona@redhat.com> - 3.15-0.1.beta1.2
- Fix incorrect path that hid failed test from view
- Add ocsp to the test suites to run but ...
- Temporarily disable the ocsp stapling tests
- Do not treat failed attempts at ssl pkcs11 bypass as fatal errors

* Thu Apr 04 2013 Elio Maldonado <emaldona@redhat.com> - 3.15-0.1.beta1.1
- Update to NSS_3_15_BETA1
- Update spec file, patches, and helper scripts on account of a shallower source tree

* Sun Mar 24 2013 Kai Engert <kaie@redhat.com> - 3.14.3-12
- Update expired test certificates (fixed in upstream bug 852781)

* Fri Mar 08 2013 Kai Engert <kaie@redhat.com> - 3.14.3-10
- Fix incorrect post/postun scripts. Fix broken links in posttrans.

* Wed Mar 06 2013 Kai Engert <kaie@redhat.com> - 3.14.3-9
- Configure libnssckbi.so to use the alternatives system
  in order to prepare for a drop in replacement.

* Fri Feb 15 2013 Elio Maldonado <emaldona@redhat.com> - 3.14.3-1
- Update to NSS_3_14_3_RTM
- sync up pem rsawrapr.c with softoken upstream changes for nss-3.14.3
- Resolves: rhbz#908257 - CVE-2013-1620 nss: TLS CBC padding timing attack
- Resolves: rhbz#896651 - PEM module trashes private keys if login fails
- Resolves: rhbz#909775 - specfile support for AArch64
- Resolves: rhbz#910584 - certutil -a does not produce ASCII output

* Mon Feb 04 2013 Elio Maldonado <emaldona@redhat.com> - 3.14.2-2
- Allow building nss against older system sqlite

* Fri Feb 01 2013 Elio Maldonado <emaldona@redhat.com> - 3.14.2-1
- Update to NSS_3_14_2_RTM

* Wed Jan 02 2013 Kai Engert <kaie@redhat.com> - 3.14.1-3
- Update to NSS_3_14_1_WITH_CKBI_1_93_RTM

* Sat Dec 22 2012 Elio Maldonado <emaldona@redhat.com> - 3.14.1-2
- Require nspr >= 4.9.4
- Fix changelog invalid dates

* Mon Dec 17 2012 Elio Maldonado <emaldona@redhat.com> - 3.14.1-1
- Update to NSS_3_14_1_RTM

* Wed Dec 12 2012 Elio Maldonado <emaldona@redhat.com> - 3.14-12
- Bug 879978 - Install the nssck.api header template where mod_revocator can access it
- Install nssck.api in /usr/includes/nss3/templates

* Tue Nov 27 2012 Elio Maldonado <emaldona@redhat.com> - 3.14-11
- Bug 879978 - Install the nssck.api header template in a place where mod_revocator can access it
- Install nssck.api in /usr/includes/nss3

* Mon Nov 19 2012 Elio Maldonado <emaldona@redhat.com> - 3.14-10
- Bug 870864 - Add support in NSS for Secure Boot

* Sat Nov 10 2012 Elio Maldonado <emaldona@redhat.com> - 3.14-9
- Disable bypass code at build time and return failure on attempts to enable at runtime
- Bug 806588 - Disable SSL PKCS #11 bypass at build time

* Sun Nov 04 2012 Elio Maldonado <emaldona@redhat.com> - 3.14-8
- Fix pk11wrap locking which fixes 'fedpkg new-sources' and 'fedpkg update' hangs
- Bug 872124 - nss-3.14 breaks fedpkg new-sources
- Fix should be considered preliminary since the patch may change upon upstream approval
 
* Thu Nov 01 2012 Elio Maldonado <emaldona@redhat.com> - 3.14-7
- Add a dummy source file for testing /preventing fedpkg breakage
- Helps test the fedpkg new-sources and upload commands for breakage by nss updates
- Related to Bug 872124 - nss 3.14 breaks fedpkg new-sources

* Thu Nov 01 2012 Elio Maldonado <emaldona@redhat.com> - 3.14-6
- Fix a previous unwanted merge from f18
- Update the SS_SSL_CBC_RANDOM_IV patch to match new sources while
- Keeping the patch disabled while we are still in rawhide and
- State in comment that patch is needed for both stable and beta branches
- Update .gitignore to download only the new sources

* Wed Oct 31 2012 Elio Maldonado <emaldona@redhat.com> - 3.14-5
- Fix the spec file so sechash.h gets installed
- Resolves: rhbz#871882 - missing header: sechash.h in nss 3.14

* Sat Oct 27 2012 Elio Maldonado <emaldona@redhat.com> - 3.14-4
- Update the license to MPLv2.0

* Wed Oct 24 2012 Elio Maldonado <emaldona@redhat.com> - 3.14-3
- Use only -f when removing unwanted headers

* Tue Oct 23 2012 Elio Maldonado <emaldona@redhat.com> - 3.14-2
- Add secmodt.h to the headers installed by nss-devel
- nss-devel must install secmodt.h which moved from softoken to pk11wrap with nss-3.14

* Mon Oct 22 2012 Elio Maldonado <emaldona@redhat.com> - 3.14-1
- Update to NSS_3_14_RTM

* Sun Oct 21 2012 Elio Maldonado <emaldona@redhat.com> - 3.14-0.1.rc.1
- Update to NSS_3_14_RC1
- update nss-589636.patch to apply to httpdserv
- turn off ocsp tests for now
- remove no longer needed patches
- remove headers shipped by nss-util

* Fri Oct 05 2012 Kai Engert <kaie@redhat.com> - 3.13.6-1
- Update to NSS_3_13_6_RTM

* Mon Aug 27 2012 Elio Maldonado <emaldona@redhat.com> - 3.13.5-8
- Rebase pem sources to fedora-hosted upstream to pick up two fixes from rhel-6.3
- Resolves: rhbz#847460 - Fix invalid read and free on invalid cert load
- Resolves: rhbz#847462 - PEM module may attempt to free uninitialized pointer 
- Remove unneeded fix gcc 4.7 c++ issue in secmodt.h that actually undoes the upstream fix

* Mon Aug 13 2012 Elio Maldonado <emaldona@redhat.com> - 3.13.5-7
- Fix pluggable ecc support

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.13.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jul 01 2012 Elio Maldonado <emaldona@redhat.com> - 3.13.5-5
- Fix checkin comment to prevent unwanted expansions of percents

* Sun Jul 01 2012 Elio Maldonado <emaldona@redhat.com> - 3.13.5-4
- Resolves: Bug 830410 - Missing Requires %%{?_isa}
- Use Requires: %%{name}%%{?_isa} = %%{version}-%%{release} on tools
- Drop zlib requires which rpmlint reports as error E: explicit-lib-dependency zlib
- Enable sha224 portion of powerup selftest when running test suites
- Require nspr 4.9.1

* Wed Jun 20 2012 Elio Maldonado <emaldona@redhat.com> - 3.13.5-3
- Resolves: rhbz#833529 - revert unwanted change to nss.pc.in

* Tue Jun 19 2012 Elio Maldonado <emaldona@redhat.com> - 3.13.5-2
- Resolves: rhbz#833529 - Remove unwanted space from the Libs: line on nss.pc.in

* Mon Jun 18 2012 Elio Maldonado <emaldona@redhat.com> - 3.13.5-1
- Update to NSS_3_13_5_RTM

* Fri Apr 13 2012 Elio Maldonado <emaldona@redhat.com> - 3.13.4-3
- Resolves: Bug 812423 - nss_Init leaks memory, fix from RHEL 6.3

* Sun Apr 08 2012 Elio Maldonado <emaldona@redhat.com> - 3.13.4-2
- Resolves: Bug 805723 - Library needs partial RELRO support added
- Patch coreconf/Linux.mk as done on RHEL 6.2

* Fri Apr 06 2012 Elio Maldonado <emaldona@redhat.com> - 3.13.4-1
- Update to NSS_3_13_4_RTM
- Update the nss-pem source archive to the latest version
- Remove no longer needed patches
- Resolves: Bug 806043 - use pem files interchangeably in a single process
- Resolves: Bug 806051 - PEM various flaws detected by Coverity
- Resolves: Bug 806058 - PEM pem_CreateObject leaks memory given a non-existing file name

* Wed Mar 21 2012 Elio Maldonado <emaldona@redhat.com> - 3.13.3-4
- Resolves: Bug 805723 - Library needs partial RELRO support added

* Fri Mar 09 2012 Elio Maldonado <emaldona@redhat.com> - 3.13.3-3
- Cleanup of the spec file
- Add references to the upstream bugs
- Fix typo in Summary for sysinit

* Thu Mar 08 2012 Elio Maldonado <emaldona@redhat.com> - 3.13.3-2
- Pick up fixes from RHEL
- Resolves: rhbz#800674 - Unable to contact LDAP Server during winsync
- Resolves: rhbz#800682 - Qpid AMQP daemon fails to load after nss update
- Resolves: rhbz#800676 - NSS workaround for freebl bug that causes openswan to drop connections

* Thu Mar 01 2012 Elio Maldonado <emaldona@redhat.com> - 3.13.3-1
- Update to NSS_3_13_3_RTM

* Mon Jan 30 2012 Tom Callaway <spot@fedoraproject.org> - 3.13.1-13
- fix issue with gcc 4.7 in secmodt.h and C++11 user-defined literals

* Thu Jan 26 2012 Elio Maldonado <emaldona@redhat.com> - 3.13.1-12
- Resolves: Bug 784672 - nss should protect against being called before nss_Init

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.13.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jan 06 2012 Elio Maldonado <emaldona@redhat.com> - 3.13.1-11
- Deactivate a patch currently meant for stable branches only

* Fri Jan 06 2012 Elio Maldonado <emaldona@redhat.com> - 3.13.1-10
- Resolves: Bug 770682 - nss update breaks pidgin-sipe connectivity
- NSS_SSL_CBC_RANDOM_IV set to 0 by default and changed to 1 on user request

* Tue Dec 13 2011 elio maldonado <emaldona@redhat.com> - 3.13.1-9
- Revert to using current nss_softokn_version
- Patch to deal with lack of sha224 is no longer needed

* Tue Dec 13 2011 Elio Maldonado <emaldona@redhat.com> - 3.13.1-8
- Resolves: Bug 754771 - [PEM] an unregistered callback causes a SIGSEGV

* Mon Dec 12 2011 Elio Maldonado <emaldona@redhat.com> - 3.13.1-7
- Resolves: Bug 750376 - nss 3.13 breaks sssd TLS
- Fix how pem is built so that nss-3.13.x works with nss-softokn-3.12.y
- Only patch blapitest for the lack of sha224 on system freebl
- Completed the patch to make pem link against system freebl

* Mon Dec 05 2011 Elio Maldonado <emaldona@redhat.com> - 3.13.1-6
- Removed unwanted /usr/include/nss3 in front of the normal cflags include path
- Removed unnecessary patch dealing with CERTDB_TERMINAL_RECORD, it's visible

* Sun Dec 04 2011 Elio Maldonado <emaldona@redhat.com> - 3.13.1-5
- Statically link the pem module against system freebl found in buildroot
- Disabling sha224-related powerup selftest until we update softokn
- Disable sha224 and pss tests which nss-softokn 3.12.x doesn't support

* Fri Dec 02 2011 Elio Maldonado Batiz <emaldona@redhat.com> - 3.13.1-4
- Rebuild with nss-softokn from 3.12 in the buildroot
- Allows the pem module to statically link against 3.12.x freebl
- Required for using nss-3.13.x with nss-softokn-3.12.y for a merge inrto rhel git repo
- Build will be temprarily placed on buildroot override but not pushed in bodhi

* Fri Nov 04 2011 Elio Maldonado <emaldona@redhat.com> - 3.13.1-2
- Fix broken dependencies by updating the nss-util and nss-softokn versions

* Thu Nov 03 2011 Elio Maldonado <emaldona@redhat.com> - 3.13.1-1
- Update to NSS_3_13_1_RTM
- Update builtin certs to those from NSSCKBI_1_88_RTM

* Sat Oct 15 2011 Elio Maldonado <emaldona@redhat.com> - 3.13-1
- Update to NSS_3_13_RTM

* Sat Oct 08 2011 Elio Maldonado <emaldona@redhat.com> - 3.13-0.1.rc0.1
- Update to NSS_3_13_RC0

* Wed Sep 14 2011 Elio Maldonado <emaldona@redhat.com> - 3.12.11-3
- Fix attempt to free initilized pointer (#717338)
- Fix leak on pem_CreateObject when given non-existing file name (#734760)
- Fix pem_Initialize to return CKR_CANT_LOCK on multi-treaded calls (#736410)

* Tue Sep 06 2011 Kai Engert <kaie@redhat.com> - 3.12.11-2
- Update builtins certs to those from NSSCKBI_1_87_RTM

* Tue Aug 09 2011 Elio Maldonado <emaldona@redhat.com> - 3.12.11-1
- Update to NSS_3_12_11_RTM

* Sat Jul 23 2011 Elio Maldonado <emaldona@redhat.com> - 3.12.10-6
- Indicate the provenance of stripped source tarball (#688015)

* Mon Jun 27 2011 Michael Schwendt <mschwendt@fedoraproject.org> - 3.12.10-5
- Provide virtual -static package to meet guidelines (#609612).

* Fri Jun 10 2011 Elio Maldonado <emaldona@redhat.com> - 3.12.10-4
- Enable pluggable ecc support (#712556)
- Disable the nssdb write-access-on-read-only-dir tests when user is root (#646045)

* Fri May 20 2011 Dennis Gilmore <dennis@ausil.us> - 3.12.10-3
- make the testsuite non fatal on arm arches

* Tue May 17 2011 Elio Maldonado <emaldona@redhat.com> - 3.12.10-2
- Fix crmf hard-coded maximum size for wrapped private keys (#703656)

* Fri May 06 2011 Elio Maldonado <emaldona@redhat.com> - 3.12.10-1
- Update to NSS_3_12_10_RTM

* Wed Apr 27 2011 Elio Maldonado <emaldona@redhat.com> - 3.12.10-0.1.beta1
- Update to NSS_3_12_10_BETA1

* Mon Apr 11 2011 Elio Maldonado <emaldona@redhat.com> - 3.12.9-15
- Implement PEM logging using NSPR's own (#695011)

* Wed Mar 23 2011 Elio Maldonado <emaldona@redhat.com> - 3.12.9-14
- Update to NSS_3.12.9_WITH_CKBI_1_82_RTM

* Thu Feb 24 2011 Elio Maldonado <emaldona@redhat.com> - 3.12.9-13
- Short-term fix for ssl test suites hangs on ipv6 type connections (#539183)

* Fri Feb 18 2011 Elio Maldonado <emaldona@redhat.com> - 3.12.9-12
- Add a missing requires for pkcs11-devel (#675196)

* Tue Feb 15 2011 Elio Maldonado <emaldona@redhat.com> - 3.12.9-11
- Run the test suites in the check section (#677809)

* Thu Feb 10 2011 Elio Maldonado <emaldona@redhat.com> - 3.12.9-10
- Fix cms headers to not use c++ reserved words (#676036)
- Reenabling Bug 499444 patches
- Fix to swap internal key slot on fips mode switches

* Tue Feb 08 2011 Elio Maldonado <emaldona@redhat.com> - 3.12.9-9
- Revert patches for 499444 until all c++ reserved words are found and extirpated

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.12.9-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb 08 2011 Elio Maldonado <emaldona@redhat.com> - 3.12.9-7
- Fix cms header to not use c++ reserved word (#676036)
- Reenable patches for bug 499444

* Tue Feb 08 2011 Christopher Aillon <caillon@redhat.com> - 3.12.9-6
- Revert patches for 499444 as they use a C++ reserved word and
  cause compilation of Firefox to fail

* Fri Feb 04 2011 Elio Maldonado <emaldona@redhat.com> - 3.12.9-5
- Fix the earlier infinite recursion patch (#499444)
- Remove a header that now nss-softokn-freebl-devel ships

* Tue Feb 01 2011 Elio Maldonado <emaldona@redhat.com> - 3.12.9-4
- Fix infinite recursion when encoding NSS enveloped/digested data (#499444)

* Mon Jan 31 2011 Elio Maldonado <emaldona@redhat.com> - 3.12.9-3
- Update the cacert trust patch per upstream review requests (#633043)

* Wed Jan 19 2011 Elio Maldonado <emaldona@redhat.com> - 3.12.9-2
- Fix to honor the user's cert trust preferences (#633043)
- Remove obsoleted patch

* Wed Jan 12 2011 Elio Maldonado <emaldona@redhat.com> - 3.12.9-1
- Update to 3.12.9

* Mon Dec 27 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.9-0.1.beta2
- Rebuilt according to fedora pre-release package naming guidelines

* Fri Dec 10 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.8.99.2-1
- Update to NSS_3_12_9_BETA2
- Fix libpnsspem crash when cacert dir contains other directories (#642433)

* Wed Dec 08 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.8.99.1-1
- Update to NSS_3_12_9_BETA1

* Thu Nov 25 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.8-9
- Update pem source tar with fixes for 614532 and 596674
- Remove no longer needed patches

* Fri Nov 05 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.8-8
- Update PayPalEE.cert test certificate which had expired

* Sun Oct 31 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.8-7
- Tell rpm not to verify md5, size, and modtime of configurations file

* Mon Oct 18 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.8-6
- Fix certificates trust order (#643134)
- Apply nss-sysinit-userdb-first.patch last

* Wed Oct 06 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.8-5
- Move triggerpostun -n nss-sysinit script ahead of the other ones (#639248)

* Tue Oct 05 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.8-4
- Fix invalid %%postun scriptlet (#639248)

* Wed Sep 29 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.8-3
- Replace posttrans sysinit scriptlet with a triggerpostun one (#636787)
- Fix and cleanup the setup-nsssysinit.sh script (#636792, #636801)

* Mon Sep 27 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.8-2
- Add posttrans scriptlet (#636787)

* Thu Sep 23 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.8-1
- Update to 3.12.8
- Prevent disabling of nss-sysinit on package upgrade (#636787)
- Create pkcs11.txt with correct permissions regardless of umask (#636792) 
- Setup-nsssysinit.sh reports whether nss-sysinit is turned on or off (#636801)
- Added provides pkcs11-devel-static to comply with packaging guidelines (#609612)

* Sat Sep 18 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.7.99.4-1
- NSS 3.12.8 RC0

* Sun Sep 05 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.7.99.3-2
- Fix nss-util_version and nss_softokn_version required to be 3.12.7.99.3

* Sat Sep 04 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.7.99.3-1
- NSS 3.12.8 Beta3
- Fix unclosed comment in renegotiate-transitional.patch

* Sat Aug 28 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.7-3
- Change BuildRequries to available version of nss-util-devel

* Sat Aug 28 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.7-2
- Define NSS_USE_SYSTEM_SQLITE and remove unneeded patch
- Add comments regarding an unversioned provides which triggers rpmlint warning
- Build requires nss-softokn-devel >= 3.12.7

* Mon Aug 16 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.7-1
- Update to 3.12.7

* Sat Aug 14 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.6-12
- Apply the patches to fix rhbz#614532

* Mon Aug 09 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.6-11
- Removed pem sourecs as they are in the cache

* Mon Aug 09 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.6-10
- Add support for PKCS#8 encoded PEM RSA private key files (#614532)

* Sat Jul 31 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.6-9
- Fix nsssysinit to return userdb ahead of systemdb (#603313)

* Tue Jun 08 2010 Dennis Gilmore <dennis@ausil.us> - 3.12.6-8
- Require and BuildRequire >= the listed version not =

* Tue Jun 08 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.6-7
- Require nss-softoken 3.12.6

* Sun Jun 06 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.6-6
- Fix SIGSEGV within CreateObject (#596674)

* Mon Apr 12 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.6-5
- Update pem source tar to pick up the following bug fixes:
- PEM - Allow collect objects to search through all objects
- PEM - Make CopyObject return a new shallow copy
- PEM - Fix memory leak in pem_mdCryptoOperationRSAPriv

* Wed Apr 07 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.6-4
- Update the test cert in the setup phase

* Wed Apr 07 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.6-3
- Add sed to sysinit requires as setup-nsssysinit.sh requires it (#576071)
- Update PayPalEE test cert with unexpired one (#580207)

* Thu Mar 18 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.6-2
- Fix ns.spec to not require nss-softokn (#575001)

* Sat Mar 06 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.6-1.2
- rebuilt with all tests enabled

* Sat Mar 06 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.6-1.1
- Using SSL_RENEGOTIATE_TRANSITIONAL as default while on transition period
- Disabling ssl tests suites until bug 539183 is resolved

* Sat Mar 06 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.6-1
- Update to 3.12.6
- Reactivate all tests
- Patch tools to validate command line options arguments

* Mon Jan 25 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.5-8
- Fix curl related regression and general patch code clean up

* Wed Jan 13 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.5-5
-  retagging

* Tue Jan 12 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.5-1.1
- Fix SIGSEGV on call of NSS_Initialize (#553638)

* Wed Jan 06 2010 Elio Maldonado<emaldona@redhat.com> - 3.12.5-1.13.2
- New version of patch to allow root to modify ystem database (#547860)

* Thu Dec 31 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.5-1.13.1
- Temporarily disabling the ssl tests

* Sat Dec 26 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.5-1.13
- Fix nsssysinit to allow root to modify the nss system database (#547860)

* Fri Dec 25 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.5-1.11
- Fix an error introduced when adapting the patch for rhbz #546211

* Sat Dec 19 2009 Elio maldonado<emaldona@redhat.com> - 3.12.5-1.9
- Remove left over trace statements from nsssysinit patching

* Fri Dec 18 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.5-2.7
- Fix a misconstructed patch

* Thu Dec 17 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.5-1.6
- Fix nsssysinit to enable apps to use system cert store, patch contributed by David Woodhouse (#546221)
- Fix spec so sysinit requires coreutils for post install scriplet (#547067)
- Fix segmentation fault when listing keys or certs in the database, patch contributed by Kamil Dudka (#540387)

* Thu Dec 10 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.5-1.5
- Fix nsssysinit to set the default flags on the crypto module (#545779)
- Remove redundant header from the pem module

* Wed Dec 09 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.5-1.1
- Remove unneeded patch

* Thu Dec 03 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.5-1.1
- Retagging to include missing patch

* Thu Dec 03 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.5-1
- Update to 3.12.5
- Patch to allow ssl/tls clients to interoperate with servers that require renogiation

* Fri Nov 20 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.4-14.1
- Retagging

* Tue Oct 20 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.4-13.1
- Require nss-softoken of same architecture as nss (#527867)
- Merge setup-nsssysinit.sh improvements from F-12 (#527051)

* Sat Oct 03 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.4-13
- User no longer prompted for a password when listing keys an empty system db (#527048)
- Fix setup-nsssysinit to handle more general formats (#527051)

* Sun Sep 27 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.4-12
- Fix syntax error in setup-nsssysinit.sh

* Sun Sep 27 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.4-11
- Fix sysinit to be under mozilla/security/nss/lib

* Sat Sep 26 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.4-10
- Add nss-sysinit activation/deactivation script

* Fri Sep 18 2009 Elio Maldonado<emaldona@redhat.com - 3.12.4-9
- Install blank databases and configuration file for system shared database
- nsssysinit queries system for fips mode before relying on environment variable

* Thu Sep 10 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.4-8
- Restoring nssutil and -rpath-link to nss-config for now - 522477

* Tue Sep 08 2009 Elio Maldonado<emaldona@redhat.com - 3.12.4-7
- Add the nss-sysinit subpackage

* Tue Sep 08 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.4-6
- Installing shared libraries to %%{_libdir}

* Mon Sep 07 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.4-5
- Retagging to pick up new sources

* Mon Sep 07 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.4-4
- Update pem enabling source tar with latest fixes (509705, 51209)

* Sun Sep 06 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.4-3
- PEM module implements memory management for internal objects - 509705
- PEM module doesn't crash when processing malformed key files - 512019

* Sat Sep 05 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.4-2
- Remove symbolic links to shared libraries from devel - 521155
- No rpath-link in nss-softokn-config

* Tue Sep 01 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.4-1
- Update to 3.12.4

* Mon Aug 31 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.3.99.3-30
- Fix FORTIFY_SOURCE buffer overflows in test suite on ppc and ppc64 - bug 519766
- Fixed requires and buildrequires as per recommendations in spec file review

* Sun Aug 30 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.3.99.3-29
- Restoring patches 2 and 7 as we still compile all sources
- Applying the nss-nolocalsql.patch solves nss-tools sqlite dependency problems

* Sun Aug 30 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.3.99.3-28
- restore require sqlite

* Sat Aug 29 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.3.99.3-27
- Don't require sqlite for nss

* Sat Aug 29 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.3.99.3-26
- Ensure versions in the requires match those used when creating nss.pc

* Fri Aug 28 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.3.99.3-25
- Remove nss-prelink.conf as signed all shared libraries moved to nss-softokn
- Add a temprary hack to nss.pc.in to unblock builds

* Fri Aug 28 2009 Warren Togami <wtogami@redhat.com> - 3.12.3.99.3-24
- caolan's nss.pc patch

* Thu Aug 27 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.3.99.3-23
- Bump the release number for a chained build of nss-util, nss-softokn and nss

* Thu Aug 27 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.3.99.3-22
- Fix nss-config not to include nssutil
- Add BuildRequires on nss-softokn and nss-util since build also runs the test suite

* Thu Aug 27 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.3.99.3-21
- disabling all tests while we investigate a buffer overflow bug

* Thu Aug 27 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.3.99.3-20
- disabling some tests while we investigate a buffer overflow bug - 519766

* Thu Aug 27 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.3.99.3-19
- remove patches that are now in nss-softokn and
- remove spurious exec-permissions for nss.pc per rpmlint
- single requires line in nss.pc.in

* Wed Aug 26 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.3.99.3-18
- Fix BuildRequires: nss-softokn-devel release number

* Wed Aug 26 2009 Elio Maldonado<emaldona@redhat.com - 3.12.3.99.3-17
- fix nss.pc.in to have one single requires line

* Tue Aug 25 2009 Dennis Gilmore <dennis@ausil.us> - 3.12.3.99.3-16
- cleanups for softokn

* Tue Aug 25 2009 Dennis Gilmore <dennis@ausil.us> - 3.12.3.99.3-15
- remove the softokn subpackages

* Mon Aug 24 2009 Dennis Gilmore <dennis@ausil.us> - 3.12.3.99.3-14
- don install the nss-util pkgconfig bits

* Mon Aug 24 2009 Dennis Gilmore <dennis@ausil.us> - 3.12.3.99.3-13
- remove from -devel the 3 headers that ship in nss-util-devel

* Mon Aug 24 2009 Dennis Gilmore <dennis@ausil.us> - 3.12.3.99.3-12
- kill off the nss-util nss-util-devel subpackages

* Sun Aug 23 2009 Elio Maldonado+emaldona@redhat.com - 3.12.3.99.3-11
- split off nss-softokn and nss-util as subpackages with their own rpms
- first phase of splitting nss-softokn and nss-util as their own packages

* Thu Aug 20 2009 Elio Maldonado <emaldona@redhat.com> - 3.12.3.99.3-10
- must install libnssutil3.since nss-util is untagged at the moment
- preserve time stamps when installing various files

* Thu Aug 20 2009 Dennis Gilmore <dennis@ausil.us> - 3.12.3.99.3-9
- dont install libnssutil3.so since its now in nss-util

* Thu Aug 06 2009 Elio Maldonado <emaldona@redhat.com> - 3.12.3.99.3-7.1
- Fix spec file problems uncovered by Fedora_12_Mass_Rebuild

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.12.3.99.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 22 2009 Elio Maldonado <emaldona@redhat.com> - 3.12.3.99.3-6
- removed two patch files which are no longer needed and fixed previous change log number
* Mon Jun 22 2009 Elio Maldonado <emaldona@redhat.com> - 3.12.3.99.3-5
- updated pem module incorporates various patches
- fix off-by-one error when computing size to reduce memory leak. (483855)
- fix data type to work on x86_64 systems. (429175)
- fix various memory leaks and free internal objects on module unload. (501080)
- fix to not clone internal objects in collect_objects().  (501118)
- fix to not bypass initialization if module arguments are omitted. (501058)
- fix numerous gcc warnings. (500815)
- fix to support arbitrarily long password while loading a private key. (500180) 
- fix memory leak in make_key and memory leaks and return values in pem_mdSession_Login (501191)
* Mon Jun 08 2009 Elio Maldonado <emaldona@redhat.com> - 3.12.3.99.3-4
- add patch for bug 502133 upstream bug 496997
* Fri Jun 05 2009 Kai Engert <kaie@redhat.com> - 3.12.3.99.3-3
- rebuild with higher release number for upgrade sanity
* Fri Jun 05 2009 Kai Engert <kaie@redhat.com> - 3.12.3.99.3-2
- updated to NSS_3_12_4_FIPS1_WITH_CKBI_1_75
* Thu May 07 2009 Kai Engert <kaie@redhat.com> - 3.12.3-7
- re-enable test suite
- add patch for upstream bug 488646 and add newer paypal
  certs in order to make the test suite pass
* Wed May 06 2009 Kai Engert <kaie@redhat.com> - 3.12.3-4
- add conflicts info in order to fix bug 499436
* Tue Apr 14 2009 Kai Engert <kaie@redhat.com> - 3.12.3-3
- ship .chk files instead of running shlibsign at install time
- include .chk file in softokn-freebl subpackage
- add patch for upstream nss bug 488350
* Tue Apr 14 2009 Kai Engert <kaie@redhat.com> - 3.12.3-2
- Update to NSS 3.12.3
* Mon Apr 06 2009 Kai Engert <kaie@redhat.com> - 3.12.2.99.3-7
- temporarily disable the test suite because of bug 494266
* Mon Apr 06 2009 Kai Engert <kaie@redhat.com> - 3.12.2.99.3-6
- fix softokn-freebl dependency for multilib (bug 494122)
* Thu Apr 02 2009 Kai Engert <kaie@redhat.com> - 3.12.2.99.3-5
- introduce separate nss-softokn-freebl package
* Thu Apr 02 2009 Kai Engert <kaie@redhat.com> - 3.12.2.99.3-4
- disable execstack when building freebl
* Tue Mar 31 2009 Kai Engert <kaie@redhat.com> - 3.12.2.99.3-3
- add upstream patch to fix bug 483855
* Tue Mar 31 2009 Kai Engert <kaie@redhat.com> - 3.12.2.99.3-2
- build nspr-less freebl library
* Tue Mar 31 2009 Kai Engert <kaie@redhat.com> - 3.12.2.99.3-1
- Update to NSS_3_12_3_BETA4

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.12.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Oct 22 2008 Kai Engert <kaie@redhat.com> - 3.12.2.0-3
- update to NSS_3_12_2_RC1
- use system zlib
* Tue Sep 30 2008 Dennis Gilmore <dennis@ausil.us> - 3.12.1.1-4
- add sparc64 to the list of 64 bit arches

* Wed Sep 24 2008 Kai Engert <kaie@redhat.com> - 3.12.1.1-3
- bug 456847, move pkgconfig requirement to devel package
* Fri Sep 05 2008 Kai Engert <kengert@redhat.com> - 3.12.1.1-2
- Update to NSS_3_12_1_RC2
* Fri Aug 22 2008 Kai Engert <kaie@redhat.com> - 3.12.1.0-2
- NSS 3.12.1 RC1
* Fri Aug 15 2008 Kai Engert <kaie@redhat.com> - 3.12.0.3-7
- fix bug bug 429175 in libpem module
* Tue Aug 05 2008 Kai Engert <kengert@redhat.com> - 3.12.0.3-6
- bug 456847, add Requires: pkgconfig
* Tue Jun 24 2008 Kai Engert <kengert@redhat.com> - 3.12.0.3-3
- nss package should own /etc/prelink.conf.d folder, rhbz#452062
- use upstream patch to fix test suite abort
* Mon Jun 02 2008 Kai Engert <kengert@redhat.com> - 3.12.0.3-2
- Update to NSS_3_12_RC4
* Mon Apr 14 2008 Kai Engert <kengert@redhat.com> - 3.12.0.1-1
- Update to NSS_3_12_RC2
* Thu Mar 20 2008 Jesse Keating <jkeating@redhat.com> - 3.11.99.5-2
- Zapping old Obsoletes/Provides.  No longer needed, causes multilib headache.
* Mon Mar 17 2008 Kai Engert <kengert@redhat.com> - 3.11.99.5-1
- Update to NSS_3_12_BETA3
* Fri Feb 22 2008 Kai Engert <kengert@redhat.com> - 3.11.99.4-1
- NSS 3.12 Beta 2
- Use /usr/lib{64} as devel libdir, create symbolic links.
* Sat Feb 16 2008 Kai Engert <kengert@redhat.com> - 3.11.99.3-6
- Apply upstream patch for bug 417664, enable test suite on pcc.
* Fri Feb 15 2008 Kai Engert <kengert@redhat.com> - 3.11.99.3-5
- Support concurrent runs of the test suite on a single build host.
* Thu Feb 14 2008 Kai Engert <kengert@redhat.com> - 3.11.99.3-4
- disable test suite on ppc
* Thu Feb 14 2008 Kai Engert <kengert@redhat.com> - 3.11.99.3-3
- disable test suite on ppc64

* Thu Feb 14 2008 Kai Engert <kengert@redhat.com> - 3.11.99.3-2
- Build against gcc 4.3.0, use workaround for bug 432146
- Run the test suite after the build and abort on failures.

* Thu Jan 24 2008 Kai Engert <kengert@redhat.com> - 3.11.99.3-1
* NSS 3.12 Beta 1

* Mon Jan 07 2008 Kai Engert <kengert@redhat.com> - 3.11.99.2b-3
- move .so files to /lib

* Wed Dec 12 2007 Kai Engert <kengert@redhat.com> - 3.11.99.2b-2
- NSS 3.12 alpha 2b

* Mon Dec 03 2007 Kai Engert <kengert@redhat.com> - 3.11.99.2-2
- upstream patches to avoid calling netstat for random data

* Wed Nov 07 2007 Kai Engert <kengert@redhat.com> - 3.11.99.2-1
- NSS 3.12 alpha 2

* Wed Oct 10 2007 Kai Engert <kengert@redhat.com> - 3.11.7-10
- Add /etc/prelink.conf.d/nss-prelink.conf in order to blacklist
  our signed libraries and protect them from modification.

* Thu Sep 06 2007 Rob Crittenden <rcritten@redhat.com> - 3.11.7-9
- Fix off-by-one error in the PEM module

* Thu Sep 06 2007 Kai Engert <kengert@redhat.com> - 3.11.7-8
- fix a C++ mode compilation error

* Wed Sep 05 2007 Bob Relyea <rrelyea@redhat.com> - 3.11.7-7
- Add 3.12 ckfw and libnsspem

* Tue Aug 28 2007 Kai Engert <kengert@redhat.com> - 3.11.7-6
- Updated license tag

* Wed Jul 11 2007 Kai Engert <kengert@redhat.com> - 3.11.7-5
- Ensure the workaround for mozilla bug 51429 really get's built.

* Mon Jun 18 2007 Kai Engert <kengert@redhat.com> - 3.11.7-4
- Better approach to ship freebl/softokn based on 3.11.5
- Remove link time dependency on softokn

* Sun Jun 10 2007 Kai Engert <kengert@redhat.com> - 3.11.7-3
- Fix unowned directories, rhbz#233890

* Fri Jun 01 2007 Kai Engert <kengert@redhat.com> - 3.11.7-2
- Update to 3.11.7, but freebl/softokn remain at 3.11.5.
- Use a workaround to avoid mozilla bug 51429.

* Fri Mar 02 2007 Kai Engert <kengert@redhat.com> - 3.11.5-2
- Fix rhbz#230545, failure to enable FIPS mode
- Fix rhbz#220542, make NSS more tolerant of resets when in the 
  middle of prompting for a user password.

* Sat Feb 24 2007 Kai Engert <kengert@redhat.com> - 3.11.5-1
- Update to 3.11.5
- This update fixes two security vulnerabilities with SSL 2
- Do not use -rpath link option
- Added several unsupported tools to tools package

* Tue Jan  9 2007 Bob Relyea <rrelyea@redhat.com> - 3.11.4-4
- disable ECC, cleanout dead code

* Tue Nov 28 2006 Kai Engert <kengert@redhat.com> - 3.11.4-1
- Update to 3.11.4

* Thu Sep 14 2006 Kai Engert <kengert@redhat.com> - 3.11.3-2
- Revert the attempt to require latest NSPR, as it is not yet available
  in the build infrastructure.

* Thu Sep 14 2006 Kai Engert <kengert@redhat.com> - 3.11.3-1
- Update to 3.11.3

* Thu Aug 03 2006 Kai Engert <kengert@redhat.com> - 3.11.2-2
- Add /etc/pki/nssdb

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 3.11.2-1.1
- rebuild

* Fri Jun 30 2006 Kai Engert <kengert@redhat.com> - 3.11.2-1
- Update to 3.11.2
- Enable executable bit on shared libs, also fixes debug info.

* Wed Jun 14 2006 Kai Engert <kengert@redhat.com> - 3.11.1-2
- Enable Elliptic Curve Cryptography (ECC)

* Fri May 26 2006 Kai Engert <kengert@redhat.com> - 3.11.1-1
- Update to 3.11.1
- Include upstream patch to limit curves

* Wed Feb 15 2006 Kai Engert <kengert@redhat.com> - 3.11-4
- add --noexecstack when compiling assembler on x86_64

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 3.11-3.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 3.11-3.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Thu Jan 19 2006 Ray Strode <rstrode@redhat.com> 3.11-3
- rebuild

* Fri Dec 16 2005 Christopher Aillon <caillon@redhat.com> 3.11-2
- Update file list for the devel packages

* Thu Dec 15 2005 Christopher Aillon <caillon@redhat.com> 3.11-1
- Update to 3.11

* Thu Dec 15 2005 Christopher Aillon <caillon@redhat.com> 3.11-0.cvs.2
- Add patch to allow building on ppc*
- Update the pkgconfig file to Require nspr

* Thu Dec 15 2005 Christopher Aillon <caillon@redhat.com> 3.11-0.cvs
- Initial import into Fedora Core, based on a CVS snapshot of
  the NSS_3_11_RTM tag
- Fix up the pkcs11-devel subpackage to contain the proper headers
- Build with RPM_OPT_FLAGS
- No need to have rpath of /usr/lib in the pc file

* Thu Dec 15 2005 Kai Engert <kengert@redhat.com>
- Adressed review comments by Wan-Teh Chang, Bob Relyea,
  Christopher Aillon.

* Sat Jul  9 2005 Rob Crittenden <rcritten@redhat.com> 3.10-1
- Initial build
