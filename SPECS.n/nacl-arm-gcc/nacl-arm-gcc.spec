%global gitver 336bd0b
%global gcc_target_platform arm-nacl
%global bootstrap 0

Name:		nacl-arm-gcc
Summary:	Various compilers (C, C++) for nacl (ARM)
Version:	4.9.2
Release:	7.git%{gitver}%{?dist}
# Generated from git
# git clone https://chromium.googlesource.com/native_client/nacl-gcc
# (Checkout ID taken from native_client/toolchain_build/toolchain_build.py
# cd nacl-gcc
# git checkout 336bd0bc1724efd6f8b2a4d7228e389dc1bc48da
# cd ..
# For gcc version, cat gcc/BASE-VER
# mv nacl-gcc nacl-arm-gcc-4.9.2-git336bd0b
# tar --exclude-vcs -cjf nacl-arm-gcc-4.9.2-git336bd0b.tar.bz2 nacl-arm-gcc-4.9.2-git336bd0b
License:	GPLv3+ and GPLv3+ with exceptions and GPLv2+ with exceptions
Source0:	nacl-arm-gcc-%{version}-git%{gitver}.tar.bz2
URL:		http://sourceware.org/gcc/
%if 0%{?fedora} <= 19
BuildRequires:	cloog-ppl-devel
%endif
BuildRequires:	gmp-devel, mpfr-devel, libmpc-devel
BuildRequires:	ppl-pwl-devel, elfutils-devel
BuildRequires:  zlib-devel, gettext, dejagnu, bison, flex, sharutils
BuildRequires:  texinfo, texinfo-tex, /usr/bin/pod2man, gcc-c++
BuildRequires:	nacl-arm-binutils
%if %{bootstrap} < 1
BuildRequires:	nacl-arm-newlib
%endif
ExclusiveArch:	i686 x86_64

%description
The gcc package contains the GNU Compiler Collection version 4.4.3.
You'll need this package in order to compile C code. This provides support
for nacl targets.

%prep
%setup -q -n %{name}-%{version}-git%{?gitver}

%build
rm -fr obj-%{gcc_target_platform}
mkdir obj-%{gcc_target_platform}
cd obj-%{gcc_target_platform}
CC=gcc
OPT_FLAGS=`echo %{optflags}|sed -e 's/\(-Wp,\)\?-D_FORTIFY_SOURCE=[12]//g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-m64//g;s/-m32//g;s/-m31//g'`
%ifarch %{ix86}
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-march=i.86//g'`
%endif
OPT_FLAGS=`echo "$OPT_FLAGS" | sed -e 's/[[:blank:]]\+/ /g'`
OPT_FLAGS=`echo "$OPT_FLAGS" | sed -e 's/-Werror=format-security//g'`
case "$OPT_FLAGS" in
  *-fasynchronous-unwind-tables*)
    sed -i -e 's/-fno-exceptions /-fno-exceptions -fno-asynchronous-unwind-tables/' \
      ../gcc/Makefile.in
    ;;
esac
GCC_DEFINES="-Dinhibit_libc -D__gthr_posix_h"
../configure --prefix=%{_prefix} --mandir=%{_mandir} --infodir=%{_infodir} \
	--enable-checking=release \
	--with-system-zlib --enable-__cxa_atexit --disable-libunwind-exceptions \
	--enable-gnu-unique-object \
	--disable-decimal-float \
	--disable-libgomp \
	--disable-libmudflap \
	--disable-libssp \
	--disable-libstdcxx-pch \
	--disable-shared \
%if 0%{?fedora} <= 19
	--with-ppl --with-cloog \
%endif
	CC="$CC" \
	CFLAGS="$OPT_FLAGS $GCC_DEFINES" \
	CXXFLAGS="`echo $OPT_FLAGS | sed 's/ -Wall / /g'`" \
	XCFLAGS="$OPT_FLAGS" \
%if %{bootstrap}
	--disable-threads \
	--enable-languages="c" \
	--without-headers \
	CFLAGS_FOR_TARGET="-O2 -g" \
	CXXFLAGS_FOR_TARGET="-O2 -g" \
%else
	CFLAGS_FOR_TARGET="-O2 -g -I/usr/arm-nacl/include/" \
	CXXFLAGS_FOR_TARGET="-O2 -g -I/usr/arm-nacl/include/" \
	--enable-languages="c,c++,lto" \
        --with-linker-hash-style=gnu \
        --enable-linker-build-id \
	--with-newlib \
%endif
	--target=%{gcc_target_platform} \
        --with-tune=cortex-a15 \
%if 0%{?fedora} >= 19
        --with-host-libstdcxx="-lstdc++ -lm" \
%else
	--with-host-libstdcxx="-lpwl -lstdc++ -lm" \
%endif
	--disable-ppl-version-check \
	--disable-libgcj

%if %{bootstrap}
make BOOT_CFLAGS="$OPT_FLAGS" all-gcc all-target-libgcc
%else
make BOOT_CFLAGS="$OPT_FLAGS" all
%endif

%install
cd obj-%{gcc_target_platform}
%if %{bootstrap}
make DESTDIR=%{buildroot} install-gcc install-target-libgcc
%else
make DESTDIR=%{buildroot} install
%endif

# Delete supplemental files that would conflict with the core toolchain
rm -rf %{buildroot}%{_infodir}
rm -rf %{buildroot}%{_mandir}/man7/
# I suspect that the core toolchain locale files will work with this reasonably well.
rm -rf %{buildroot}%{_datadir}/locale/

# Don't dupe the system libiberty.a
rm -rf %{buildroot}%{_libdir}/libiberty.a

# Don't package these unused (and conflicting) python bits
rm -rf %{buildroot}%{_datadir}/gcc-%{version}

%files
%doc gcc/README* gcc/COPYING*
%{_bindir}/%{gcc_target_platform}-gcc-ar
%{_bindir}/%{gcc_target_platform}-gcc-nm
%{_bindir}/%{gcc_target_platform}-gcc-ranlib
%{_bindir}/%{gcc_target_platform}-cpp
%{_bindir}/%{gcc_target_platform}-gcc
%{_bindir}/%{gcc_target_platform}-gcc-%{version}
%{_bindir}/%{gcc_target_platform}-gcov
%{_prefix}/%{gcc_target_platform}/lib/nacl-arm-macros.s
%{_prefix}/lib/gcc/%{gcc_target_platform}/
%{_libexecdir}/gcc/%{gcc_target_platform}/
%{_mandir}/man1/%{gcc_target_platform}-cpp.*
%{_mandir}/man1/%{gcc_target_platform}-gcc.*
%{_mandir}/man1/%{gcc_target_platform}-gcov.*
%if %{bootstrap} < 1
%{_bindir}/%{gcc_target_platform}-c++
%{_bindir}/%{gcc_target_platform}-g++
%{_prefix}/%{gcc_target_platform}/include/c++/
%{_prefix}/%{gcc_target_platform}/lib*/
%{_mandir}/man1/%{gcc_target_platform}-g++.*
%endif

%changelog
* Wed Nov 25 2015 Liu Di <liudidi@gmail.com> - 4.9.2-7.git336bd0b
- 为 Magic 3.0 重建

* Wed Nov 25 2015 Liu Di <liudidi@gmail.com> - 4.9.2-6.git336bd0b
- 为 Magic 3.0 重建

* Thu Oct  1 2015 Tom Callaway <spot@fedoraproject.org> 4.9.2-5.git336bd0b
- bootstrap off

* Thu Oct  1 2015 Tom Callaway <spot@fedoraproject.org> 4.9.2-4.git336bd0b
- update to chromium 45
- bootstrap on

* Thu Jun  4 2015 Tom Callaway <spot@fedoraproject.org> 4.9.2-3.gitb23dd79
- nuke conflicting (and unused) python files

* Wed Jun  3 2015 Tom Callaway <spot@fedoraproject.org> 4.9.2-2.gitb23dd79
- bootstrap off

* Fri May 22 2015 Tom Callaway <spot@fedoraproject.org> 4.9.2-1.gitb23dd79
- arm version of nacl toolchain
- bootstrap on
