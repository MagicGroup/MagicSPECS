%global gitver 093bbb4
%global gcc_target_platform x86_64-nacl
%global bootstrap 0

Name:		nacl-gcc
Summary:	Various compilers (C, C++) for nacl
Version:	4.4.3
Release:	10.git%{gitver}%{?dist}
# Generated from git
# git clone http://git.chromium.org/native_client/nacl-gcc.git
# (Checkout ID taken from chromium-35.0.1916.114/native_client/tools/REVISIONS)
# cd nacl-gcc
# git checkout 093bbb415942cc3406656f90a3a5b2f0aef58d06
# cd ..
# For gcc version, cat gcc/BASE-VER
# mv nacl-gcc nacl-gcc-4.4.3-git093bbb4
# tar --exclude-vcs -cjf nacl-gcc-4.4.3-git093bbb4.tar.bz2 nacl-gcc-4.4.3-git093bbb4
License:	GPLv3+ and GPLv3+ with exceptions and GPLv2+ with exceptions
Source0:	nacl-gcc-%{version}-git%{gitver}.tar.bz2
Patch0:		nacl-gcc-4.4.3-git0622fce-tex-fixes.patch
URL:		http://sourceware.org/gcc/
BuildRequires:	gmp-devel, mpfr-devel, cloog-devel
BuildRequires:	ppl-pwl-devel, elfutils-devel
BuildRequires:	nacl-binutils
%if %{bootstrap} < 1
BuildRequires:	nacl-newlib
%endif
ExclusiveArch:	i686 x86_64

%description
The gcc package contains the GNU Compiler Collection version 4.4.3.
You'll need this package in order to compile C code. This provides support
for nacl targets.

%prep
%setup -q -n %{name}-%{version}-git%{?gitver}
%patch0 -p1 -b .texfix

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
	--with-ppl --with-cloog \
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
	CFLAGS_FOR_TARGET="-O2 -g -mtls-use-call -I/usr/x86_64-nacl/include/" \
	CXXFLAGS_FOR_TARGET="-O2 -g -mtls-use-call -I/usr/x86_64-nacl/include/" \
	--enable-threads=nacl \
	--enable-languages="c,c++,objc" \
	--enable-tls \
	--with-newlib \
%endif
	--target=%{gcc_target_platform} \
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

%files
%doc gcc/README* gcc/COPYING*
%{_bindir}/%{gcc_target_platform}-cpp
%{_bindir}/%{gcc_target_platform}-gcc
%{_bindir}/%{gcc_target_platform}-gcc-%{version}
%{_bindir}/%{gcc_target_platform}-gccbug
%{_bindir}/%{gcc_target_platform}-gcov
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
* Mon Aug 03 2015 Liu Di <liudidi@gmail.com> - 4.4.3-10.git093bbb4
- 为 Magic 3.0 重建

* Tue Jan 20 2015 Liu Di <liudidi@gmail.com> - 4.4.3-9.git093bbb4
- 为 Magic 3.0 重建

* Mon Jun  2 2014 Tom Callaway <spot@fedoraproject.org> 4.4.3-8.git093bbb4
- update for chromium 35

* Wed Mar 27 2013 Tom Callaway <spot@fedoraproject.org> 4.4.3-7.git0622fce
- update for chromium 25

* Thu Dec 13 2012 Tom Callaway <spot@fedoraproject.org> 4.4.3-6.git455063d
- update for chromium 23

* Tue Aug 28 2012 Tom Callaway <spot@fedoraproject.org> 4.4.3-5.git3937565
- update for chromium 21

* Tue Jun 12 2012 Tom Callaway <spot@fedoraproject.org> 4.4.3-4.gitc69a5b7
- update to chromium 19

* Mon Feb 13 2012 Tom Callaway <spot@fedoraproject.org> 4.4.3-3.git82ea71e
- update to chromium 17

* Fri Oct 28 2011 Tom Callaway <spot@fedoraproject.org> 4.4.3-2.gitcff9ac88
- rebuild in non-bootstrap pass

* Thu Oct 27 2011 Tom Callaway <spot@fedoraproject.org> 4.4.3-1.gitcff9ac88
- initial package
