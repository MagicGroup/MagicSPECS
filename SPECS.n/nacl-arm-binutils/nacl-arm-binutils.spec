# rpmbuild parameters:
# --define "binutils_target arm-linux-gnu" to create arm-linux-gnu-binutils.
# --with debug: Build without optimizations and without splitting the debuginfo.
# --without testsuite: Do not run the testsuite.  Default is to run it.
# --with testsuite: Run the testsuite.  Default --with debug is not to run it.

# For NaCl, the crossarch is x86_64-nacl
# ... except now we need it for arm-nacl too.

%global binutils_target arm-nacl
%global gitver cde986c

# Hypothetically, this can be built on any target, but Chromium only cares about x86_64.
ExclusiveArch: x86_64

%if 0%{!?binutils_target:1}
%define binutils_target %{_target_platform}
%define isnative 1
%define enable_shared 1
%else
%define cross %{binutils_target}-
%define isnative 0
%define enable_shared 0
%endif

Summary: A GNU collection of binary utilities
Name: nacl-arm-binutils%{?_with_debug:-debug}
Version: 2.25.2
Release: 2.git%{gitver}%{?dist}
License: GPLv3+
Group: Development/Tools
URL: http://sources.redhat.com/binutils
# Generated from git
# git clone https://chromium.googlesource.com/native_client/nacl-binutils
# (Checkout ID taken from native_client/toolchain_build/toolchain_build.py)
# cd nacl-binutils
# git checkout cde986cc330c6d7ebd68e416ab66e0929abe4c8f
# cd ..
# For binutils version, grep PACKAGE_VERSION= bfd/configure
# mv nacl-binutils nacl-binutils-2.25.2-gitcde986c
# tar --exclude-vcs -cjf nacl-binutils-2.25.2-gitcde986c.tar.bz2 nacl-binutils-2.25.2-gitcde986c
Source: nacl-binutils-%{version}-git%{gitver}.tar.bz2
Source2: binutils-2.19.50.0.1-output-format.sed

# build_gold for nacl is no
%global build_gold no

%if 0%{?_with_debug:1}
# Define this if you want to skip the strip step and preserve debug info.
# Useful for testing.
%define __debug_install_post : > %{_builddir}/%{?buildsubdir}/debugfiles.list
%define debug_package %{nil}
%define run_testsuite 0%{?_with_testsuite:1}
%else
%define run_testsuite 0%{!?_without_testsuite:1}
%endif

# Disable testsuite for nacl build
%define run_testsuite 0

BuildRequires: texinfo >= 4.0, gettext, flex, bison, zlib-devel, ncurses-devel
# Required for: ld-bootstrap/bootstrap.exp bootstrap with --static
# It should not be required for: ld-elf/elf.exp static {preinit,init,fini} array
%if %{run_testsuite}
BuildRequires: dejagnu, zlib-static, glibc-static, sharutils
%endif
Conflicts: gcc-c++ < 4.0.0
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
%ifarch ia64
Obsoletes: gnupro <= 1117-1
%endif

# The higher of these two numbers determines the default ld.
%{!?ld_bfd_priority: %global ld_bfd_priority	50}
%{!?ld_gold_priority:%global ld_gold_priority	30}

%if "%{build_gold}" == "both"
Requires(post): coreutils
Requires(post): %{_sbindir}/alternatives
Requires(preun): %{_sbindir}/alternatives
%endif

# On ARM EABI systems, we do want -gnueabi to be part of the
# target triple.
%ifnarch %{arm}
%define _gnu %{nil}
%endif

%description
Binutils is a collection of binary utilities, including ar (for
creating, modifying and extracting from archives), as (a family of GNU
assemblers), gprof (for displaying call graph profile data), ld (the
GNU linker), nm (for listing symbols from object files), objcopy (for
copying and translating object files), objdump (for displaying
information from object files), ranlib (for generating an index for
the contents of an archive), readelf (for displaying detailed
information about binary files), size (for listing the section sizes
of an object or archive file), strings (for listing printable strings
from files), strip (for discarding symbols), and addr2line (for
converting addresses to file and line).

%package devel
Summary: BFD and opcodes static and dynamic libraries and header files
Group: System Environment/Libraries
Provides: binutils-static = %{version}-%{release}
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
Requires: zlib-devel

%description devel
This package contains BFD and opcodes static and dynamic libraries.

The dynamic libraries are in this package, rather than a seperate
base package because they are actually linker scripts that force
the use of the static libraries.  This is because the API of the
BFD library is too unstable to be used dynamically.

The static libraries are here because they are now needed by the
dynamic libraries.

Developers starting new projects are strongly encouraged to consider
using libelf instead of BFD.

%prep
%setup -q -n nacl-binutils-%{version}-git%{gitver}

# We cannot run autotools as there is an exact requirement of autoconf-2.59.

# On ppc64 we might use 64KiB pages
sed -i -e '/#define.*ELF_COMMONPAGESIZE/s/0x1000$/0x10000/' bfd/elf*ppc.c
# LTP sucks
perl -pi -e 's/i\[3-7\]86/i[34567]86/g' */conf*
sed -i -e 's/%''{release}/%{release}/g' bfd/Makefile{.am,.in}
sed -i -e '/^libopcodes_la_\(DEPENDENCIES\|LIBADD\)/s,$, ../bfd/libbfd.la,' opcodes/Makefile.{am,in}
# Build libbfd.so and libopcodes.so with -Bsymbolic-functions if possible.
if gcc %{optflags} -v --help 2>&1 | grep -q -- -Bsymbolic-functions; then
sed -i -e 's/^libbfd_la_LDFLAGS = /&-Wl,-Bsymbolic-functions /' bfd/Makefile.{am,in}
sed -i -e 's/^libopcodes_la_LDFLAGS = /&-Wl,-Bsymbolic-functions /' opcodes/Makefile.{am,in}
fi
# $PACKAGE is used for the gettext catalog name.
sed -i -e 's/^ PACKAGE=/ PACKAGE=%{?cross}/' */configure
# Undo the name change to run the testsuite.
for tool in binutils gas ld
do
  sed -i -e "2aDEJATOOL = $tool" $tool/Makefile.am
  sed -i -e "s/^DEJATOOL = .*/DEJATOOL = $tool/" $tool/Makefile.in
done
touch */configure

%build
echo target is %{binutils_target}
export CFLAGS="$RPM_OPT_FLAGS"
CARGS=

case %{binutils_target} in i?86*|sparc*|ppc*|s390*|sh*|arm*)
  CARGS="$CARGS --enable-64-bit-bfd"
  ;;
esac

case %{binutils_target} in ia64*)
  CARGS="$CARGS --enable-targets=i386-linux"
  ;;
esac

case %{binutils_target} in ppc*|ppc64*)
  CARGS="$CARGS --enable-targets=spu"
  ;;
esac

%if 0%{?_with_debug:1}
CFLAGS="$CFLAGS -O0 -ggdb2"
%define enable_shared 0
%endif

# We could optimize the cross builds size by --enable-shared but the produced
# binaries may be less convenient in the embedded environment.
%configure \
  --build=%{_target_platform} --host=%{_target_platform} \
  --target=%{binutils_target} \
%ifarch %gold_arches
%if "%{build_gold}" == "both"
  --enable-gold=default --enable-ld \
%else
  --enable-gold \
%endif
%endif
%if !%{isnative}
  --enable-targets=%{_host} \
  --with-sysroot=%{_prefix}/%{binutils_target}/sys-root \
  --program-prefix=%{cross} \
%endif
%if %{enable_shared}
  --enable-shared \
%else
  --disable-shared \
%endif
  $CARGS \
  --disable-werror \
  --enable-plugins \
  --with-bugurl=http://bugzilla.redhat.com/bugzilla/
make %{_smp_mflags} tooldir=%{_prefix} all
make %{_smp_mflags} tooldir=%{_prefix} info

# Do not use %%check as it is run after %%install where libbfd.so is rebuild
# with -fvisibility=hidden no longer being usable in its shared form.
%if !%{run_testsuite}
echo ====================TESTSUITE DISABLED=========================
%else
make -k check < /dev/null || :
echo ====================TESTING=========================
cat {gas/testsuite/gas,ld/ld,binutils/binutils}.sum
echo ====================TESTING END=====================
for file in {gas/testsuite/gas,ld/ld,binutils/binutils}.{sum,log}
do
  ln $file binutils-%{_target_platform}-$(basename $file) || :
done
tar cjf binutils-%{_target_platform}.tar.bz2 binutils-%{_target_platform}-*.{sum,log}
uuencode binutils-%{_target_platform}.tar.bz2 binutils-%{_target_platform}.tar.bz2
rm -f binutils-%{_target_platform}.tar.bz2 binutils-%{_target_platform}-*.{sum,log}
%endif

%install
make install DESTDIR=%{buildroot}
pushd ld
make install DESTDIR=%{buildroot} install-data-local
popd
%if %{isnative}
make prefix=%{buildroot}%{_prefix} infodir=%{buildroot}%{_infodir} install-info

# Rebuild libiberty.a with -fPIC.
# Future: Remove it together with its header file, projects should bundle it.
make -C libiberty clean
make CFLAGS="-g -fPIC $RPM_OPT_FLAGS" -C libiberty

# Rebuild libbfd.a with -fPIC.
# Without the hidden visibility the 3rd party shared libraries would export
# the bfd non-stable ABI.
make -C bfd clean
make CFLAGS="-g -fPIC $RPM_OPT_FLAGS -fvisibility=hidden" -C bfd

# Rebuild libopcodes.a with -fPIC.
make -C opcodes clean
make CFLAGS="-g -fPIC $RPM_OPT_FLAGS" -C opcodes

install -m 644 bfd/libbfd.a %{buildroot}%{_libdir}
install -m 644 libiberty/libiberty.a %{buildroot}%{_libdir}
install -m 644 include/libiberty.h %{buildroot}%{_prefix}/include
install -m 644 opcodes/libopcodes.a %{buildroot}%{_libdir}
# Remove Windows/Novell only man pages
rm -f %{buildroot}%{_mandir}/man1/{dlltool,nlmconv,windres}*

%if %{enable_shared}
chmod +x %{buildroot}%{_libdir}/lib*.so*
%endif

# Prevent programs from linking against libbfd and libopcodes
# dynamically, as they are change far too often.
rm -f %{buildroot}%{_libdir}/lib{bfd,opcodes}.so

# Remove libtool files, which reference the .so libs
rm -f %{buildroot}%{_libdir}/lib{bfd,opcodes}.la

# Sanity check --enable-64-bit-bfd really works.
grep '^#define BFD_ARCH_SIZE 64$' %{buildroot}%{_prefix}/include/bfd.h
# Fix multilib conflicts of generated values by __WORDSIZE-based expressions.
%ifarch %{ix86} x86_64 ppc ppc64 s390 s390x sh3 sh4 sparc sparc64 arm
sed -i -e '/^#include "ansidecl.h"/{p;s~^.*$~#include <bits/wordsize.h>~;}' \
    -e 's/^#define BFD_DEFAULT_TARGET_SIZE \(32\|64\) *$/#define BFD_DEFAULT_TARGET_SIZE __WORDSIZE/' \
    -e 's/^#define BFD_HOST_64BIT_LONG [01] *$/#define BFD_HOST_64BIT_LONG (__WORDSIZE == 64)/' \
    -e 's/^#define BFD_HOST_64_BIT \(long \)\?long *$/#if __WORDSIZE == 32\
#define BFD_HOST_64_BIT long long\
#else\
#define BFD_HOST_64_BIT long\
#endif/' \
    -e 's/^#define BFD_HOST_U_64_BIT unsigned \(long \)\?long *$/#define BFD_HOST_U_64_BIT unsigned BFD_HOST_64_BIT/' \
    %{buildroot}%{_prefix}/include/bfd.h
%endif
touch -r bfd/bfd-in2.h %{buildroot}%{_prefix}/include/bfd.h

# Generate .so linker scripts for dependencies; imported from glibc/Makerules:

# This fragment of linker script gives the OUTPUT_FORMAT statement
# for the configuration we are building.
OUTPUT_FORMAT="\
/* Ensure this .so library will not be used by a link for a different format
   on a multi-architecture system.  */
$(gcc $CFLAGS $LDFLAGS -shared -x c /dev/null -o /dev/null -Wl,--verbose -v 2>&1 | sed -n -f "%{SOURCE2}")"

tee %{buildroot}%{_libdir}/libbfd.so <<EOH
/* GNU ld script */

$OUTPUT_FORMAT

/* The libz dependency is unexpected by legacy build scripts.  */
INPUT ( %{_libdir}/libbfd.a -liberty -lz )
EOH

tee %{buildroot}%{_libdir}/libopcodes.so <<EOH
/* GNU ld script */

$OUTPUT_FORMAT

INPUT ( %{_libdir}/libopcodes.a -lbfd )
EOH

%else # !%%{isnative}
# For cross-binutils we drop the documentation.
rm -rf %{buildroot}%{_infodir}
# We keep these as one can have native + cross binutils of different versions.
#rm -rf %%{buildroot}%%{_prefix}/share/locale
#rm -rf %%{buildroot}%%{_mandir}
rm -rf %{buildroot}%{_libdir}/libiberty.a
%endif # !%%{isnative}

# This one comes from gcc
rm -f %{buildroot}%{_infodir}/dir
# rm -rf %%{buildroot}%%{_prefix}/%%{binutils_target}

%find_lang %{?cross}binutils
%find_lang %{?cross}opcodes
%find_lang %{?cross}bfd
%find_lang %{?cross}gas
%find_lang %{?cross}gprof
cat %{?cross}opcodes.lang >> %{?cross}binutils.lang
cat %{?cross}bfd.lang >> %{?cross}binutils.lang
cat %{?cross}gas.lang >> %{?cross}binutils.lang
cat %{?cross}gprof.lang >> %{?cross}binutils.lang

if [ -x ld/ld-new ]; then
  %find_lang %{?cross}ld
  cat %{?cross}ld.lang >> %{?cross}binutils.lang
fi
if [ -x gold/ld-new ]; then
  %find_lang %{?cross}gold
  cat %{?cross}gold.lang >> %{?cross}binutils.lang
fi

# Needed for the nacl-cross-compiler to find its pieces
mkdir -p %{buildroot}%{_prefix}/%{binutils_target}/bin/
pushd %{buildroot}%{_prefix}/%{binutils_target}/bin/
for i in addr2line c++filt gprof readelf size strings; do
  ln -s ../../bin/%{binutils_target}-$i $i
done
popd

rm -rf %{buildroot}%{_datadir}/gdb
rm -rf %{buildroot}%{_mandir}/man5/*
rm -rf %{buildroot}%{_includedir}/gdb

%clean
rm -rf %{buildroot}

%post
%if "%{build_gold}" == "both"
%__rm -f %{_bindir}/%{?cross}ld
%{_sbindir}/alternatives --install %{_bindir}/%{?cross}ld %{?cross}ld \
  %{_bindir}/%{?cross}ld.bfd %{ld_bfd_priority}
%{_sbindir}/alternatives --install %{_bindir}/%{?cross}ld %{?cross}ld \
  %{_bindir}/%{?cross}ld.gold %{ld_gold_priority}
%{_sbindir}/alternatives --auto %{?cross}ld 
%endif
%if %{isnative}
/sbin/ldconfig
# For --excludedocs:
if [ -e %{_infodir}/binutils.info.gz ]
then
  /sbin/install-info --info-dir=%{_infodir} %{_infodir}/as.info.gz
  /sbin/install-info --info-dir=%{_infodir} %{_infodir}/binutils.info.gz
  /sbin/install-info --info-dir=%{_infodir} %{_infodir}/gprof.info.gz
  /sbin/install-info --info-dir=%{_infodir} %{_infodir}/ld.info.gz
  /sbin/install-info --info-dir=%{_infodir} %{_infodir}/standards.info.gz
  /sbin/install-info --info-dir=%{_infodir} %{_infodir}/configure.info.gz
fi
%endif # %%{isnative}
exit 0

%preun
%if "%{build_gold}" == "both"
if [ $1 = 0 ]; then
  %{_sbindir}/alternatives --remove %{?cross}ld %{_bindir}/%{?cross}ld.bfd
  %{_sbindir}/alternatives --remove %{?cross}ld %{_bindir}/%{?cross}ld.gold
fi
%endif
%if %{isnative}
if [ $1 = 0 ]; then
  if [ -e %{_infodir}/binutils.info.gz ]
  then
    /sbin/install-info --delete --info-dir=%{_infodir} %{_infodir}/as.info.gz
    /sbin/install-info --delete --info-dir=%{_infodir} %{_infodir}/binutils.info.gz
    /sbin/install-info --delete --info-dir=%{_infodir} %{_infodir}/gprof.info.gz
    /sbin/install-info --delete --info-dir=%{_infodir} %{_infodir}/ld.info.gz
    /sbin/install-info --delete --info-dir=%{_infodir} %{_infodir}/standards.info.gz
    /sbin/install-info --delete --info-dir=%{_infodir} %{_infodir}/configure.info.gz
  fi
fi
%endif
exit 0

%if %{isnative}
%postun -p /sbin/ldconfig
%endif # %%{isnative}

%files -f %{?cross}binutils.lang
%doc README
%{_bindir}/%{?cross}[!l]*
%if "%{build_gold}" == "both"
%{_bindir}/%{?cross}ld.*
%ghost %{_bindir}/%{?cross}ld
%else
%{_bindir}/%{?cross}ld*
%endif
%{_prefix}/%{binutils_target}/bin/
%{_prefix}/%{binutils_target}/lib/
%{_mandir}/man1/*
%if %{enable_shared}
%{_libdir}/lib*.so
%exclude %{_libdir}/libbfd.so
%exclude %{_libdir}/libopcodes.so
%endif
%{_libdir}/libarm-nacl-sim.a

%if %{isnative}
%{_infodir}/[^b]*info*
%{_infodir}/binutils*info*

%files devel
%{_prefix}/include/*
%{_libdir}/lib*.a
%{_libdir}/libbfd.so
%{_libdir}/libopcodes.so
%{_infodir}/bfd*info*

%endif # %%{isnative}

%changelog
* Wed Nov 25 2015 Liu Di <liudidi@gmail.com> - 2.25.2-2.gitcde986c
- 为 Magic 3.0 重建

* Thu Oct 15 2015 Tom Callaway <spot@fedoraproject.org> - 2.25.2-1.gitcde986c
- update for chromium 46

* Thu Oct  1 2015 Tom Callaway <spot@fedoraproject.org> - 2.25-1.git68b975a
- sneaky chromium, you tricked me

* Thu Oct  1 2015 Tom Callaway <spot@fedoraproject.org> - 2.24-3.git1d8592c
- rebuild for new targets, no code changes

* Mon May  4 2015 Tom Callaway <spot@fedoraproject.org> - 2.24-2.git1d8592c
- update for chromium 42.0.2311.135

* Mon Jun  2 2014 Tom Callaway <spot@fedoraproject.org> - 2.24-1.git7dc2f25
- update for chromium 35

* Thu May 30 2013 Tom Callaway <spot@fedoraproject.org> - 2.20.1-7.gitbd55408
- update to chromium 27 nacl-binutils

* Wed Mar 27 2013 Tom Callaway <spot@fedoraproject.org> - 2.20.1-6.gite0648d3
- fix tex issue

* Thu Dec 13 2012 Tom Callaway <spot@fedoraproject.org> - 2.20.1-5.gite0648d3
- update to chromium 23 nacl-binutils

* Tue Jun 12 2012 Tom Callaway <spot@fedoraproject.org> - 2.20.1-4.gitf412ed5
- update to chromium 19 nacl-binutils

* Tue Feb 21 2012 Tom Callaway <spot@fedoraproject.org> - 2.20.1-3.git73acd6f
- disable testsuite

* Mon Feb 13 2012 Tom Callaway <spot@fedoraproject.org> - 2.20.1-2.git73acd6f
- update to chromium 17 nacl-binutils

* Thu Oct  27 2011 Tom Callaway <spot@fedoraproject.org> - 2.20.1-1.git38c9b31a
- initial nacl-binutils package
