%global nspr_version 4.10.2
%global nss_name nss
%global nss_util_version 3.15.5
%global unsupported_tools_directory %{_libdir}/nss/unsupported-tools
%global saved_files_dir %{_libdir}/nss/saved

# Produce .chk files for the final stripped binaries
#
# NOTE: The LD_LIBRARY_PATH line guarantees shlibsign links
# against the freebl that we just built. This is necessary
# because the signing algorithm changed on 3.14 to DSA2 with SHA256
# whereas we previously signed with DSA and SHA1. We must Keep this line
# until all mock platforms have been updated.
# After %%{__os_install_post} we would add
# export LD_LIBRARY_PATH=$RPM_BUILD_ROOT/%%{_libdir}
%define __spec_install_post \
    %{?__debug_package:%{__debug_install_post}} \
    %{__arch_install_post} \
    %{__os_install_post} \
    $RPM_BUILD_ROOT/%{unsupported_tools_directory}/shlibsign -i $RPM_BUILD_ROOT/%{_libdir}/libsoftokn3.so \
    $RPM_BUILD_ROOT/%{unsupported_tools_directory}/shlibsign -i $RPM_BUILD_ROOT/%{_libdir}/libfreebl3.so \
    $RPM_BUILD_ROOT/%{unsupported_tools_directory}/shlibsign -i $RPM_BUILD_ROOT/%{_libdir}/libnssdbm3.so \
%{nil}

Summary:          Network Security Services Softoken Module
Name:             nss-softokn
Version:          3.15.5
Release:          2%{?dist}
License:          MPLv2.0
URL:              http://www.mozilla.org/projects/security/pki/nss/
Group:            System Environment/Libraries
Requires:         nspr >= %{nspr_version}
Requires:         nss-util >= %{nss_util_version}
Requires:         nss-softokn-freebl%{_isa} >= %{version}
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:    nspr-devel >= %{nspr_version}
BuildRequires:    nss-util-devel >= %{nss_util_version}
BuildRequires:    sqlite-devel
BuildRequires:    zlib-devel
BuildRequires:    pkgconfig
BuildRequires:    gawk
BuildRequires:    psmisc
BuildRequires:    perl

Source0:          %{name}-%{version}.tar.gz
# The nss-softokn tar ball is a subset of nss-{version}.tar.gz.
# We use the nss-split-softokn.sh script to keep only what we need
# via via nss-split-softokn.sh ${version}
# Detailed Steps:
# fedpkg clone nss-softokn
# cd nss-softokn
# Split off nss-softokn out of the full nss source tar ball:
# sh ./nss-split-softokn.sh ${version}
# A file named {name}-{version}.tar.gz should appear
# which is ready for uploading to the lookaside cache.
Source1:          nss-split-softokn.sh
Source2:          nss-softokn.pc.in
Source3:          nss-softokn-config.in

Patch1:           build-nss-softoken-only.patch
# Build only the softoken and freebl related tools
Patch8:           softoken-minimal-test-dependencies.patch
# Select the tests to run based on the type of build
# Upstream: https://bugzilla.mozilla.org/show_bug.cgi?id=902171
Patch9:           nss-versus-softoken-tests.patch
# This patch uses the gcc-iquote dir option documented at
# http://gcc.gnu.org/onlinedocs/gcc/Directory-Options.html#Directory-Options
# to place the in-tree directories at the head of the list on list of directories
# to be searched for for header files. This ensures a build even when system freebl 
# headers are older. Such is the case when we are starting a major update.
# NSSUTIL_INCLUDE_DIR, after all, contains both util and freebl headers. 
# Once has been bootstapped the patch may be removed, but it doesn't hurt to keep it.
Patch10:           iquote.patch
# Upstream: https://bugzilla.mozilla.org/show_bug.cgi?id=972450
# Define -DMP_USE_UINT_DIGIT for Linux x86 because mpi_x86.s
# requires mp_digit to be an unsigned int. The MP_USE_UINT_DIGIT macro
# ensures that. We were previously relying on ULLONG_MAX being undefined
# in the compilation environment, which isn't true in C99 mode.
Patch11:           mozbug-972450.patch

%description
Network Security Services Softoken Cryptographic Module

%package freebl
Summary:          Freebl library for the Network Security Services
Group:            System Environment/Base
Conflicts:        nss < 3.12.2.99.3-5
Conflicts:        prelink < 0.4.3
Conflicts:        filesystem < 3

%description freebl
NSS Softoken Cryptographic Module Freelb Library

Install the nss-softokn-freebl package if you need the freebl 
library.

%package freebl-devel
Summary:          Header and Library files for doing development with the Freebl library for NSS
Group:            System Environment/Base
Provides:         nss-softokn-freebl-static = %{version}-%{release}
Requires:         nss-softokn-freebl%{?_isa} = %{version}-%{release}

%description freebl-devel
NSS Softoken Cryptographic Module Freelb Library Development Tools
This package supports special needs of some PKCS #11 module developers and
is otherwise considered private to NSS. As such, the programming interfaces
may change and the usual NSS binary compatibility commitments do not apply.
Developers should rely only on the officially supported NSS public API.

%package devel
Summary:          Development libraries for Network Security Services
Group:            Development/Libraries
Requires:         nss-softokn%{?_isa} = %{version}-%{release}
Requires:         nss-softokn-freebl-devel%{?_isa} = %{version}-%{release}
Requires:         nspr-devel >= %{nspr_version}
Requires:         nss-util-devel >= %{nss_util_version}
Requires:         pkgconfig
BuildRequires:    nspr-devel >= %{nspr_version}
BuildRequires:    nss-util-devel >= %{nss_util_version}
# require nss at least the version when we split via subpackages

%description devel
Header and library files for doing development with Network Security Services.


%prep
%setup -q

%patch1 -p0 -b .softokenonly
%patch8 -p0 -b .crypto
%patch9 -p0 -b .cryptotests
# activate if needed when doing a major update with new apis
%patch10 -p0 -b .iquote
pushd nss
%patch11 -p1 -b .fixsegfault
popd


%build

# partial RELRO support as a security enhancement
LDFLAGS+=-Wl,-z,relro
export LDFLAGS

FREEBL_NO_DEPEND=1
export FREEBL_NO_DEPEND

# Must export FREEBL_LOWHASH=1 for nsslowhash.h so that it gets
# copied to dist and the rpm install phase can find it
# This due of the upstream changes to fix
# https://bugzilla.mozilla.org/show_bug.cgi?id=717906
FREEBL_LOWHASH=1
export FREEBL_LOWHASH

FREEBL_USE_PRELINK=1
export FREEBL_USE_PRELINK

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
NSPR_LIB_DIR=`/usr/bin/pkg-config --libs-only-L nspr | sed 's/-L//'`

export NSPR_INCLUDE_DIR
export NSPR_LIB_DIR

export NSSUTIL_INCLUDE_DIR=`/usr/bin/pkg-config --cflags-only-I nss-util | sed 's/-I//'`
export NSSUTIL_LIB_DIR=%{_libdir}

NSS_USE_SYSTEM_SQLITE=1
export NSS_USE_SYSTEM_SQLITE

%ifarch x86_64 ppc64 ia64 s390x sparc64 aarch64 ppc64le mips64el
USE_64=1
export USE_64
%endif

export NSS_ENABLE_ECC=1

# uncomment if the iquote patch is activated
export IN_TREE_FREEBL_HEADERS_FIRST=1

# Use only the basicutil subset for sectools.a
export NSS_BUILD_SOFTOKEN_ONLY=1

# display processor information
CPU_INFO=`cat /proc/cpuinfo`
echo "############## CPU INFO ##################"
echo "${CPU_INFO}"
echo "##########################################"

# Compile softokn plus needed support
%{__make} -C ./nss/coreconf
%{__make} -C ./nss/lib/dbm
%{__make} -C ./nss

# Set up our package file
# The nspr_version and nss_util_version globals used here
# must match the ones nss-softokn has for its Requires. 
%{__mkdir_p} ./dist/pkgconfig
%{__cat} %{SOURCE2} | sed -e "s,%%libdir%%,%{_libdir},g" \
                          -e "s,%%prefix%%,%{_prefix},g" \
                          -e "s,%%exec_prefix%%,%{_prefix},g" \
                          -e "s,%%includedir%%,%{_includedir}/nss3,g" \
                          -e "s,%%NSPR_VERSION%%,%{nspr_version},g" \
                          -e "s,%%NSSUTIL_VERSION%%,%{nss_util_version},g" \
                          -e "s,%%SOFTOKEN_VERSION%%,%{version},g" > \
                          ./dist/pkgconfig/nss-softokn.pc

SOFTOKEN_VMAJOR=`cat nss/lib/softoken/softkver.h | grep "#define.*SOFTOKEN_VMAJOR" | awk '{print $3}'`
SOFTOKEN_VMINOR=`cat nss/lib/softoken/softkver.h | grep "#define.*SOFTOKEN_VMINOR" | awk '{print $3}'`
SOFTOKEN_VPATCH=`cat nss/lib/softoken/softkver.h | grep "#define.*SOFTOKEN_VPATCH" | awk '{print $3}'`

export SOFTOKEN_VMAJOR
export SOFTOKEN_VMINOR
export SOFTOKEN_VPATCH

%{__cat} %{SOURCE3} | sed -e "s,@libdir@,%{_libdir},g" \
                          -e "s,@prefix@,%{_prefix},g" \
                          -e "s,@exec_prefix@,%{_prefix},g" \
                          -e "s,@includedir@,%{_includedir}/nss3,g" \
                          -e "s,@MOD_MAJOR_VERSION@,$SOFTOKEN_VMAJOR,g" \
                          -e "s,@MOD_MINOR_VERSION@,$SOFTOKEN_VMINOR,g" \
                          -e "s,@MOD_PATCH_VERSION@,$SOFTOKEN_VPATCH,g" \
                          > ./dist/pkgconfig/nss-softokn-config

chmod 755 ./dist/pkgconfig/nss-softokn-config


%check

# Begin -- copied from the build section
FREEBL_NO_DEPEND=1
export FREEBL_NO_DEPEND

BUILD_OPT=1
export BUILD_OPT

%ifarch x86_64 ppc64 ia64 s390x sparc64 aarch64 ppc64le mips64el
USE_64=1
export USE_64
%endif

# to test for the last tool built correctly
export NSS_BUILD_SOFTOKEN_ONLY=1

export NSS_ENABLE_ECC=1

# End -- copied from the build section

# enable the following line to force a test failure
# find . -name \*.chk | xargs rm -f

# Run test suite.

SPACEISBAD=`find ./nss/tests | grep -c ' '` ||:
if [ $SPACEISBAD -ne 0 ]; then
  echo "error: filenames containing space are not supported (xargs)"
  exit 1
fi

rm -rf ./tests_results
cd ./nss/tests/
# all.sh is the test suite script

# only run cipher tests for nss-softokn
%global nss_cycles "standard"
%global nss_tests "cipher"
%global nss_ssl_tests " "
%global nss_ssl_run " "

HOST=localhost DOMSUF=localdomain PORT=$MYRAND NSS_CYCLES=%{?nss_cycles} NSS_TESTS=%{?nss_tests} NSS_SSL_TESTS=%{?nss_ssl_tests} NSS_SSL_RUN=%{?nss_ssl_run} ./all.sh

cd ../../../../

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
%{__mkdir_p} $RPM_BUILD_ROOT/%{_bindir}
%{__mkdir_p} $RPM_BUILD_ROOT/%{_libdir}
%{__mkdir_p} $RPM_BUILD_ROOT/%{unsupported_tools_directory}
%{__mkdir_p} $RPM_BUILD_ROOT/%{_libdir}/pkgconfig
%{__mkdir_p} $RPM_BUILD_ROOT/%{saved_files_dir}

# Copy the binary libraries we want
for file in libsoftokn3.so libnssdbm3.so libfreebl3.so
do
  %{__install} -p -m 755 dist/*.OBJ/lib/$file $RPM_BUILD_ROOT/%{_libdir}
done

# Copy the binaries we ship as unsupported
for file in bltest fipstest shlibsign
do
  %{__install} -p -m 755 dist/*.OBJ/bin/$file $RPM_BUILD_ROOT/%{unsupported_tools_directory}
done

# Copy the include files we want
for file in dist/public/nss/*.h
do
  %{__install} -p -m 644 $file $RPM_BUILD_ROOT/%{_includedir}/nss3
done

# Copy some freebl include files we also want
for file in blapi.h alghmac.h
do
  %{__install} -p -m 644 dist/private/nss/$file $RPM_BUILD_ROOT/%{_includedir}/nss3
done

# Copy the static freebl library
for file in libfreebl.a
do
%{__install} -p -m 644 dist/*.OBJ/lib/$file $RPM_BUILD_ROOT/%{_libdir}
done

# Copy the package configuration files
%{__install} -p -m 644 ./dist/pkgconfig/nss-softokn.pc $RPM_BUILD_ROOT/%{_libdir}/pkgconfig/nss-softokn.pc
%{__install} -p -m 755 ./dist/pkgconfig/nss-softokn-config $RPM_BUILD_ROOT/%{_bindir}/nss-softokn-config


%clean
%{__rm} -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/libnssdbm3.so
%{_libdir}/libnssdbm3.chk
%{_libdir}/libsoftokn3.so
%{_libdir}/libsoftokn3.chk
# shared with nss-tools
%dir %{_libdir}/nss
%dir %{saved_files_dir}
%dir %{unsupported_tools_directory}
%{unsupported_tools_directory}/bltest
%{unsupported_tools_directory}/fipstest
%{unsupported_tools_directory}/shlibsign

%files freebl
%defattr(-,root,root)
%{_libdir}/libfreebl3.so
%{_libdir}/libfreebl3.chk

%files freebl-devel
%defattr(-,root,root)
%{_libdir}/libfreebl.a
%{_includedir}/nss3/blapi.h
%{_includedir}/nss3/blapit.h
%{_includedir}/nss3/alghmac.h

%files devel
%defattr(-,root,root)
%{_libdir}/pkgconfig/nss-softokn.pc
%{_bindir}/nss-softokn-config

# co-owned with nss
%dir %{_includedir}/nss3
#
# The following headers are those exported public in
# nss/lib/freebl/manifest.mn and
# nss/lib/softoken/manifest.mn
#
# The following list is short because many headers, such as
# the pkcs #11 ones, have been provided by nss-util-devel
# which installed them before us.
#
%{_includedir}/nss3/ecl-exp.h
%{_includedir}/nss3/nsslowhash.h
%{_includedir}/nss3/shsign.h

%changelog
* Sun Mar 02 2014 Elio Maldonado <emaldona@redhat.com> - 3.15.5-2
- Fix a segmentation fault when signing on i686 that occurs in Rawhide
- Patch contributed by Stephan Bergmann 
- Resolves: Bug 1071679 - Define -DMP_USE_UINT_DIGIT in lib/freebl/Makefile for Linux x86

* Wed Feb 19 2014 Elio Maldonado <emaldona@redhat.com> - 3.15.5-1
- Update to nss-3.15.1 - Resolves: Bug 1066877

* Sat Jan 25 2014 Elio Maldonado <emaldona@redhat.com> - 3.15.4-3
- Add support for ppc64le, Resolves: Bug 1052546 

* Mon Jan 20 2014 Peter Robinson <pbrobinson@fedoraproject.org> 3.15.4-2
- ARM tests pass so remove ARM conditional

* Tue Jan 07 2014 Elio Maldonado <emaldona@redhat.com> - 3.15.3-2
- Update to NSS_3_15_4_RTM
- Resolves: Bug 1049229 - nss-3.15.4 is available

* Tue Nov 26 2013 Elio Maldonado <emaldona@redhat.com> - 3.15.2-3
- Update to NSS_3_15_3_RTM
- Related: Bug 1031897 - CVE-2013-5605 CVE-2013-5606 CVE-2013-1741

* Thu Oct 17 2013 Elio Maldonado <emaldona@redhat.com> - 3.15.2-2
- Split off nss-softokn from the full nss sources as released upstream
- Bug 1019244 - ECDHE in openssl available -> NSS needs too for Firefox/Thunderbird

* Thu Sep 26 2013 Elio Maldonado <emaldona@redhat.com> - 3.15.2-1
- Update to NSS_3_15_2_RTM
- Update softokn splitting script to copy lowhash from full nss sources
- Add lowhash to test suites to run in the %%check section

* Sun Aug 11 2013 Elio Maldonado <emaldona@redhat.com> - 3.15.1-3
- Cleanup spec file to address rpmlint errors and warnings
- Use double percent symbols to fix macro-in-comment warnings

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.15.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 02 2013 Elio Maldonado <emaldona@redhat.com> - 3.15.1-1
- Update to NSS_3_15_1_RTM

* Mon Jun 17 2013 Elio Maldonado <emaldona@redhat.com> - 3.15-3
- Require nspr-4.10 or greater
- Fix patch to select tests to run

* Thu Jun 13 2013 Elio Maldonado <emaldona@redhat.com> - 3.15-2
- Select the tests suite to run based on the build type

* Wed May 29 2013 Elio Maldonado <emaldona@redhat.com> - 3.15-1
- Update to NSS_3_15_RTM

* Tue Apr 23 2013 Elio Maldonado <emaldona@redhat.com> - 3.15-0.1.beta.3
- Reverse the last changes since pk11gcmtest properly belongs to nss

* Tue Apr 23 2013 Elio Maldonado <emaldona@redhat.com> - 3.15-0.1.beta.2
- Add lowhashtest and pk11gcmtest as unsupported tools
- Modify nss-softoken-split script to include them in the split

* Fri Apr 05 2013 Elio Maldonado <emaldona@redhat.com> - 3.15-0.1.beta.1
- Update to NSS_3_15_BETA1
- Update spec file, patches, and helper scrips on account of a shallwer source tree

* Fri Feb 15 2013 Elio Maldonado <emaldona@redhat.com> - 3.14.3-1
- Update to NSS_3_14_3_RTM
- Resolves: rhbz#909781 - specfile support for AArch64

* Mon Feb 04 2013 Elio Maldonado <emaldona@redhat.com> - 3.14.2-3
- Allow building nss-softokn against older system sqlite

* Sat Feb 02 2013 Elio Maldonado <emaldona@redhat.com> - 3.14.2-2
- Update to NSS_3_14_2_RTM
- Restore comments on how to transition when signing algorithm changes
- Remove unused patches

* Fri Feb 01 2013 Elio Maldonado <emaldona@redhat.com> - 3.14.2-1
- Update to NSS_3_14_2_RTM

* Thu Dec 27 2012 Elio Maldonado <emaldona@redhat.com> - 3.14.1-5
- Add RSA performance test for freebl
- Fix bogus date in changelog warnings

* Mon Dec 24 2012 Elio Maldonado <emaldona@redhat.com> - 3.14.1-4
- Fix bogus date warnings in %%changelog

* Sat Dec 22 2012 Elio Maldonado <emaldona@redhat.com> - 3.14.1-3
- Cleanup patches for building softoken only libraries and tests

* Mon Dec 17 2012 Elio Maldonado <emaldona@redhat.com> - 3.14.1-2
- Require nspr version >= 4.9.4

* Mon Dec 17 2012 Elio Maldonado <emaldona@redhat.com> - 3.14.1-1
- Update to NSS_3_14_1_RTM

* Mon Dec 03 2012 Elio Maldonado <emaldona@redhat.com> - 3.14-6
- Bug 883114 - Install bltest and fipstest as unsupported tools

* Mon Nov 19 2012 Elio Maldonado <emaldona@redhat.com> - 3.14-5
- Truly apply the bug 829088 patch this time
- Resolves: rhbz#829088 - Fix failure in sha244 self-test

* Mon Nov 19 2012 Elio Maldonado <emaldona@redhat.com> - 3.14-4
- Apply the bug 829088 patch in question
- Adjust the patch to account for code changes in nss-3.14
- Resolves: rhbz#829088 - Fix failure in sha244 self-test

* Sun Nov 18 2012 Elio Maldonado <emaldona@redhat.com> - 3.14-3
- Resolves: rhbz#829088 - Fix failure in sha244 self-test
- Fixes login failures on fips mode

* Sat Oct 27 2012 Elio Maldonado <emaldona@redhat.com> - 3.14-2
 - Update the license to MPLv2.0

* Mon Oct 22 2012 Elio Maldonado <emaldona@redhat.com> - 3.14-1
- Update to NSS_3_14_RTM

* Sun Oct 21 2012 Elio Maldonado <emaldona@redhat.com> - 3.14-0.1.rc1.2
- Update to NSS_3_14_RC
- Remove the temporary bootstrapping modifications

* Sun Oct 21 2012 Elio Maldonado <emaldona@redhat.com> - 3.14-0.1.rc.1
- Update to NSS_3_14_RC1
- Remove patches rendered obsolete by this update and update others
- Temporarily modifiy the spec file while bootstrapping the buildroot a follows:
- Remove unwanted headers that we lo loger ship
- Modified the post install scriplet to ensure the in-tree freebl library is loaded

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.13.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 20 2012 Elio Maldonado <emaldona@redhat.com> - 3.13.5-2
- Resolves: rhbz#833529 - revert unwanted change to nss-softokn.pc.in

* Mon Jun 18 2012 Elio Maldonado <emaldona@redhat.com> - 3.13.5-1
- Update to NSS_3_13_5_RTM
- Remove unneeded fix for gcc 4.7 c++ issue in secmodt.h which undoes the upstream fix
- Fix Libs: line on nss-softokn.pc.in

* Wed Jun 13 2012 Elio Maldonado <emaldona@redhat.com> - 3.13.4-3
- Resolves: rhbz#745224 - nss-softokn sha224 self-test fails in fips mode

* Tue Apr 10 2012 Elio Maldonado <emaldona@redhat.com> - 3.13.4-2
- Resolves: Bug 801975 Restore use of NSS_NoDB_Init or alternate to fipstest

* Fri Apr 06 2012 Elio Maldonado <emaldona@redhat.com> - 3.13.4-1
- Update to NSS_3_13_4

* Sun Apr 01 2012 Elio Maldonado <emaldona@redhat.com> - 3.13.4-0.1.beta.1
- Update to NSS_3_13_4_BETA1
- Improve steps for splitting off softokn from the full nss

* Wed Mar 21 2012 Elio Maldonado <emaldona@redhat.com> - 3.13.3-2
- Resolves: Bug 805719 - Library needs partial RELRO support added

* Thu Mar 01 2012 Elio Maldonado <emaldona@redhat.com> - 3.13.3-1
- Update to NSS_3_13_3_RTM

* Wed Feb  1 2012 Tom Callaway <spot@fedoraproject.org> 3.13.1-20
- re-enable /usrmove changes

* Wed Feb  1 2012 Tom Callaway <spot@fedoraproject.org> 3.13.1-19.1
- fix issue with gcc 4.7 in secmodt.h and C++11 user-defined literals
- temporarily revert /usrmove changes. they will be restored in -20 for the f17-usrmove tag.

* Wed Jan 25 2012 Harald Hoyer <harald@redhat.com> 3.13.1-19
- add filesystem guard

* Wed Jan 25 2012 Harald Hoyer <harald@redhat.com> 3.13.1-18
- install everything in /usr
  https://fedoraproject.org/wiki/Features/UsrMove

* Fri Jan 13 2012 Elio Maldonado Batiz <emaldona@redhat.com> - 3.13.1-17
- Remove unneeded prelink patch afterthe nss update to 3.13.1

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.13.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec 30 2011 Elio Maldonado <emaldona@redhat.com> - 3.13.1-15
- Bug 770999 - Fix segmentation violation when turning on fips mode
- Reintroduce the iquote patch but don't apply it unless needed

* Tue Dec 13 2011 Elio Maldonado <emaldona@redhat.com> - 3.12.9-14
- Restore the update to 3.13.1
- Update the patch for freebl to deal with prelinked shared libraries
- Add additional dbrg power-up self-tests as required by fips
- Reactivate the tests

* Tue Dec 06 2011 Elio Maldonado <emaldona@redhat.com> - 3.12.9-13
- Bug 757005 Build nss-softokn for rhel 7
- Make it almost like nss-softokn-3.12.9 in rhel 6.2
- Added a patch to build with Linux 3 and higher
- Meant to work with nss and nss-utul 3.1.3.1
- Download only the 3.12.9 sources from the lookaside cache

* Fri Dec 02 2011 Elio Maldonado <emaldona@redhat.com> - 3.12.9-12
- Retagging

* Wed Nov 23 2011 Elio Maldonado <emaldona@redhat.com> - 3.12.9-11
- Downgrading to 3.12.9 for a merge into new RHEL git repo
- This build is for the buildroot for a limited time only
- Do not not push it to update-testing

* Tue Nov 08 2011 Elio Maldonado <emaldona@redhat.com> - 3.13.1-1
- Update to NSS_3_13_1_RTM

* Wed Oct 12 2011 Elio Maldonado <emaldona@redhat.com> - 3.12.10-6
- Fix failure to switch nss-softokn to FIPS mode (#745571)

* Tue Oct 11 2011 Elio Maldonado <emaldona@redhat.com> - 3.13-0.1.rc0.3
- Update to NSS_3_13_RC0 post bootstrapping
- Don't incude util in sources for the lookaside cache
- Reenable building the fipstest tool
- Restore full cli argument parsing in the sectool library

* Sun Oct 09 2011 Elio Maldonado <emaldona@redhat.com> - 3.13-0.1.rc0.2
- Update to NSS_3_13_RC0 bootstrapping the system phase 2
- Reenable the cipher test suite

* Sat Oct 08 2011 Elio Maldonado <emaldona@redhat.com> - 3.13-0.rc0.1
- Update to NSS_3_13_RC0

* Thu Sep  8 2011 Ville Skyttä <ville.skytta@iki.fi> - 3.12.11-3
- Avoid %%post/un shell invocations and dependencies.

* Wed Aug 17 2011 Elio Maldonado <emaldona@redhat.com> - 3.12.10-5
- rebuilt as recommended to deal with an rpm 4.9.1 issue

* Wed Jul 20 2011 Elio Maldonado <emaldona@redhat.com> - 3.12.10-4
- Adjustements from code review (#715402)

* Sun Jun 26 2011 Elio Maldonado <emaldona@redhat.com> - 3.12.10-3
- Add %%{check} section to run crypto tests as part of the build (#715402)

* Tue Jun 14 2011 Elio Maldonado <emaldona@redhat.com> - 3.12.10-2
- Fix intel optimized aes code to deal with case where input and ouput are in the same buffer (#709517)

* Fri May 06 2011 Elio Maldonado <emaldona@redhat.com> - 3.12.10-1
- Update to NSS_3_12_10_RTM

* Wed Apr 27 2011 Elio Maldonado <emaldona@redhat.com> - 3.12.10-0.1.beta1
- Update to NSS_3_12_10_BETA1

* Fri Feb 25 2011 Elio Maldonado <emaldona@redhat.com> - 3.12.9-7
- Add requires nss-softokn-freebl-devel to nss-softokn-devel (#675196)

* Mon Feb 14 2011 Elio Maldonado <emaldona@redhat.com> - 3.12.9-5
- Expand the nss-softokn-freebl-devel package description (#675196)

* Mon Feb 14 2011 Elio Maldonado <emaldona@redhat.com> - 3.12.9-5
- Remove duplicates from the file lists

* Sun Feb 13 2011 Elio Maldonado <emaldona@redhat.com> - 3.12.9-4
- Add blapit.h to headers provided by nss-softokn-freebl-devel (#675196)
- Expand the freebl-devel package description

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.12.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb 04 2011 Elio Maldonado <emaldona@redhat.com> - 3.12.9-2
- Add header for nss-softokn-freebl-devel (#675196)

* Wed Jan 12 2011 Elio Maldonado <emaldona@redhat.com> - 3.12.9-1
- Update to 3.12.9

* Mon Dec 27 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.9-0.1.beta2
- Rebuilt according to fedora pre-release package naming guidelines

* Fri Dec 10 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.8.99.2-1
- Update to NSS_3_12_9_BETA2

* Wed Dec 08 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.8.99.1-1
- Update to NSS_3_12_9_BETA1

* Wed Sep 29 2010 jkeating - 3.12.8-2
- Rebuilt for gcc bug 634757

* Thu Sep 23 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.8-1
- Update to 3.12.8
- Adhere to static library packaging guidelines (#609613)
- Fix nss-util-devel version dependency line
- Shorten freebl and freebl subpackages descriptions

* Sat Sep 18 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.99.4-1
- NSS 3.12.8 RC0

* Sun Sep 12 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.7.99.3-2
- Update the required version of nss-util to 3.12.7.99.3

* Sat Sep 04 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.7.99.3-1
- NSS 3.12.8 Beta 3

* Mon Aug 30 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.7-3
- Update BuildRequires on nspr-devel and nss-util-devel

* Sun Aug 29 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.7-2
- Define NSS_USE_SYSTEM_SQLITE and remove nss-nolocalsql patch
- Fix rpmlint warnings about macros in comments and changelog

* Mon Aug 16 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.7-1
- Update to 3.12.7
- Fix build files to ensure nsslowhash.h is included in public headers

* Tue Jun 08 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.6-3
- Retagging

* Mon Jun 07 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.6-2
- Bump NVR to be greater than those for nss-softokn subpackages in F11 (rhbz#601407)

* Sun Jun 06 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.4-23
- Bump release number

* Fri Jun 04 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.4-22
- Cleanup changelog comments to avoid unwanted macro expansions

* Wed Jun 02 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.4-21
- Retagging

* Wed Jun 02 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.4-20
- Add %%{?_isa} to the requires in the devel packages (#596840)
- Fix typo in the package description (#598295)
- Update nspr version to 4.8.4

* Sat May 08 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.4-19
- Consider the system as not fips enabled when /proc/sys/crypto/fips_enabled isn't present (rhbz#590199)

* Sat May 08 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.4-18
- Fix Conflicts line to prevent update when prelink is not yet the right version (rhbz#590199)

* Mon Apr 19 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.4-17
- Updated prelink patch rhbz#504949

* Thu Apr 15 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.4-16
- allow prelink of softoken and freebl. Change the verify code to use
  prelink -u if prelink is installed. Fix by Robert Relyea rhbz#504949

* Mon Jan 18 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.4-15
- Move libfreebl3.so and its .chk file to /lib{64} (rhbz#561544)

* Mon Jan 18 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.4-13
- Fix in nss-softokn-spec.in 
- Require nss-util >= 3.12.4

* Thu Dec 03 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.4-12
- Require nss-util 3.12.5

* Fri Nov 20 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.4-11
- export freebl devel tools (#538226)

* Wed Sep 23 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.4-10
- Fix paths in nss-softokn-prelink so signed libraries don't get touched, rhbz#524794

* Thu Sep 17 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.4-9
- Add nssdbm3.so to nss-softokn-prelink.conf, rhbz#524077

* Thu Sep 10 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.4-8
- Retagging for a chained build

* Thu Sep 10 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.4-6
- Don't list libraries in nss-softokn-config, dynamic linking required

* Tue Sep 08 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.4-5
- Installing shared libraries to %%{_libdir}

* Sun Sep 06 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.4-4
- Postuninstall scriptlet finishes quietly

* Sat Sep 05 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.4-3
- Remove symblic links to shared libraries from devel, rhbz#521155
- Apply the nss-nolocalsql patch
- No rpath-link in nss-softokn-config

* Fri Sep 04 2009 serstring=Elio Maldonado<emaldona@redhat.cpm> - 3.12.4-2
- Retagging to pick up the correct .cvsignore

* Tue Sep 01 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.4-1
- Update to 3.12.4
- Fix logic on postun
- Don't require sqlite

* Mon Aug 31 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.3.99.3-24
- Fixed test on %%postun to avoid returning 1 when nss-softokn instances still remain

* Sun Aug 30 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.3.99.3-23
- Explicitly state via nss_util_version the nss-util version we require

* Fri Aug 28 2009 Warren Togami <wtogami@redhat.com> - 3.12.3.99.3-22
- caolan's nss-softokn.pc patch

* Thu Aug 27 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.3.99.3-21
- Bump the release number for a chained build of nss-util, nss-softokn and nss

* Thu Aug 27 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.3.99.3-20
- List freebl, nssdbm and softokn libraries in nss-softokn-config and nss-softokn.pc

* Thu Aug 27 2009 Elio Maldonado <emaldona@redhat.com> - 3.12.3.99.3-19
- Determine NSSUTIL_INCLUDE_DIR and NSSUTIL_LIB_DIR with a pkg-config query on nss-util
- Remove the release 17 hack

* Thu Aug 27 2009 Elio maldonado<emaldona@redhat.com> - 3.12.3.99.3-18
- fix spurious executable permissions on nss-softokn.pc

* Thu Aug 27 2009 Adel Gadllah <adel.gadllah@gmail.com> - 3.12.3.99.3-17
- Add hack to fix build

* Tue Aug 25 2009 Dennis Gilmore <dennis@ausil.us> - 3.12.3.99.3-16
- only have a single Requires: line in the .pc file

* Tue Aug 25 2009 Dennis Gilmore <dennis@ausil.us> - 3.12.3.99.3-12
- bump to unique rpm nvr 

* Tue Aug 25 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.3.99.3-10
- Build after nss with subpackages and new nss-util

* Thu Aug 20 2009 Dennis Gilmore <dennis@ausil.us> 3.12.3.99.3-9
- revert to shipping bits

* Wed Aug 19 2009 Elio Maldonado <emaldona@redhat.com> 3.12.3.99.3-8.1
- Disable installing until conflicts are relsoved

* Wed Aug 19 2009 Elio Maldonado <emaldona@redhat.com> 3.12.3.99.3-8
- Initial build
