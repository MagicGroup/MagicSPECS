%global __os_install_post /usr/lib/rpm/brp-compress %{nil}

# Set this to one when mingw-crt isn't built yet
%global bootstrap 0

# C++11 threads requires winpthreads so this can only be enabled once winpthreads is built
%if 0%{?fedora} >= 21
%global enable_winpthreads 1
%else
%global enable_winpthreads 0
%endif

# Libgomp requires pthreads-w32 or winpthreads so this can only be
# enabled once pthreads-w32 or winpthreads is built. If enable_libgomp
# is set to 1 and enable_winpthreads is set to 0 then pthreads-w32 will
# be used as pthreads implementation
%global enable_libgomp 1

# Run the testsuite
%global enable_tests 0

# If enabled, build from a snapshot
#%%global snapshot_date 20130310
#%%global snapshot_rev 196584

# When building from a snapshot the name of the source folder is different
%if 0%{?snapshot_date}
%global source_folder gcc-4.8-%{snapshot_date}
%else
%global source_folder gcc-%{version}
%endif

Name:           mingw-gcc
Version:        4.8.2
Release:        3%{?snapshot_date:.svn.%{snapshot_date}.r%{snapshot_rev}}%{?dist}
Summary:        MinGW Windows cross-compiler (GCC) for C

License:        GPLv3+ and GPLv3+ with exceptions and GPLv2+ with exceptions
Group:          Development/Languages
URL:            http://gcc.gnu.org
%if 0%{?snapshot_date}
Source0:        ftp://ftp.nluug.nl/mirror/languages/gcc/snapshots/4.8-%{snapshot_date}/gcc-4.8-%{snapshot_date}.tar.bz2
%else
Source0:        ftp://ftp.gnu.org/gnu/gcc/gcc-%{version}/gcc-%{version}.tar.bz2
%endif


BuildRequires:  texinfo
BuildRequires:  mingw32-filesystem >= 95
BuildRequires:  mingw64-filesystem >= 95
BuildRequires:  mingw32-binutils
BuildRequires:  mingw64-binutils
BuildRequires:  mingw32-headers
BuildRequires:  mingw64-headers
BuildRequires:  gmp-devel
BuildRequires:  mpfr-devel
BuildRequires:  libmpc-devel
BuildRequires:  libgomp
BuildRequires:  flex
BuildRequires:  zlib-devel
%if 0%{?fedora}
BuildRequires:  cloog-ppl cloog-ppl-devel
%endif
%if 0%{bootstrap} == 0
BuildRequires:  mingw32-crt
BuildRequires:  mingw64-crt
%if 0%{enable_winpthreads}
BuildRequires:  mingw32-winpthreads
BuildRequires:  mingw64-winpthreads
%else
%if 0%{enable_libgomp}
BuildRequires:  mingw32-pthreads
BuildRequires:  mingw64-pthreads
%endif
%endif
%if 0%{enable_tests}
BuildRequires:  wine
BuildRequires:  autogen
BuildRequires:  dejagnu
BuildRequires:  sharutils
%endif
%endif
Provides: bundled(libiberty)

%description
MinGW Windows cross-compiler (GCC) for C.

###############################################################################
# Mingw32
###############################################################################
%package -n mingw32-gcc
Summary:        MinGW Windows cross-compiler (GCC) for C for the win32 target
Requires:       mingw32-binutils
Requires:       mingw32-headers
Requires:       mingw32-cpp
%if 0%{bootstrap} == 0
Requires:       mingw32-crt
%endif

# The RPM version used by RHEL6 can't automatically add the
# correct provides tags during the build so we add these manually
%if 0%{bootstrap} == 0 && 0%{?rhel} == 6
Provides:       mingw32(libgcc_s_sjlj-1.dll)
Provides:       mingw32(libssp-0.dll)
Provides:       mingw32(libquadmath-0.dll)
%endif

%description -n mingw32-gcc
MinGW Windows cross-compiler (GCC) for C for the win32 target.

%package -n mingw32-cpp
Summary:        MinGW Windows cross-C Preprocessor for the win32 target

# NB: Explicit mingw32-filesystem dependency is REQUIRED here.
Requires:       mingw32-filesystem >= 95

%description -n mingw32-cpp
MinGW Windows cross-C Preprocessor for the win32 target.

%package -n mingw32-gcc-c++
Summary:        MinGW Windows cross-compiler for C++ for the win32 target
Requires:       mingw32-gcc = %{version}-%{release}

%if 0%{bootstrap} == 0 && 0%{?rhel} == 6
Provides:       mingw32(libstdc++-6.dll)
%endif

%description -n mingw32-gcc-c++
MinGW Windows cross-compiler for C++ for the win32 target.

%package -n mingw32-gcc-objc
Summary:        MinGW Windows cross-compiler support for Objective C for the win32 target
Requires:       mingw32-gcc = %{version}-%{release}

%if 0%{bootstrap} == 0 && 0%{?rhel} == 6
Provides:       mingw32(libobjc-4.dll)
%endif

%description -n mingw32-gcc-objc
MinGW Windows cross-compiler support for Objective C for the win32 target.

%package -n mingw32-gcc-objc++
Summary:        MinGW Windows cross-compiler support for Objective C++ for the win32 target
Requires:       mingw32-gcc-c++ = %{version}-%{release}
Requires:       mingw32-gcc-objc = %{version}-%{release}

%description -n mingw32-gcc-objc++
MinGW Windows cross-compiler support for Objective C++ for the win32 target.

%package -n mingw32-gcc-gfortran
Summary:        MinGW Windows cross-compiler for FORTRAN for the win32 target
Requires:       mingw32-gcc = %{version}-%{release}

%if 0%{bootstrap} == 0 && 0%{?rhel} == 6
Provides:       mingw32(libgfortran-3.dll)
Requires:       mingw32(libquadmath-0.dll)
%endif

%description -n mingw32-gcc-gfortran
MinGW Windows cross-compiler for FORTRAN for the win32 target.

%if 0%{enable_libgomp}
%package -n mingw32-libgomp
Summary:        GCC OpenMP v3.0 shared support library for the win32 target
Requires:       mingw32-gcc = %{version}-%{release}

%if 0%{?rhel} == 6
# libgomp dll is linked with pthreads, but since we don't run the
# automatic dependency scripts, it doesn't get picked up automatically.
Requires:       mingw32-pthreads
Provides:       mingw32(libgomp-1.dll)
%endif

%description -n mingw32-libgomp
This package contains GCC shared support library which is
needed for OpenMP v3.0 support for the win32 target.
%endif

###############################################################################
# Mingw64
###############################################################################
%package -n mingw64-gcc
Summary:        MinGW Windows cross-compiler (GCC) for C for the win64 target
Requires:       mingw64-binutils
Requires:       mingw64-headers
Requires:       mingw64-cpp
%if 0%{bootstrap} == 0
Requires:       mingw64-crt
%endif

%if 0%{bootstrap} == 0 && 0%{?rhel} == 6
Provides:       mingw64(libgcc_s_seh-1.dll)
Provides:       mingw64(libssp-0.dll)
Provides:       mingw64(libquadmath-0.dll)
%endif

%description -n mingw64-gcc
MinGW Windows cross-compiler (GCC) for C for the win64 target.

%package -n mingw64-cpp
Summary:        MinGW Windows cross-C Preprocessor for the win64 target.

# NB: Explicit mingw64-filesystem dependency is REQUIRED here.
Requires:       mingw64-filesystem >= 95

%description -n mingw64-cpp
MinGW Windows cross-C Preprocessor for the win64 target

%package -n mingw64-gcc-c++
Summary:        MinGW Windows cross-compiler for C++ for the win64 target
Requires:       mingw64-gcc = %{version}-%{release}

%if 0%{bootstrap} == 0 && 0%{?rhel} == 6
Provides:       mingw64(libstdc++-6.dll)
%endif

%description -n mingw64-gcc-c++
MinGW Windows cross-compiler for C++ for the win64 target.

%package -n mingw64-gcc-objc
Summary:        MinGW Windows cross-compiler support for Objective C for the win64 target
Requires:       mingw64-gcc = %{version}-%{release}

%if 0%{bootstrap} == 0 && 0%{?rhel} == 6
Provides:       mingw64(libobjc-4.dll)
%endif

%description -n mingw64-gcc-objc
MinGW Windows cross-compiler support for Objective C for the win64 target.

%package -n mingw64-gcc-objc++
Summary:        MinGW Windows cross-compiler support for Objective C++ for the win64 target
Requires:       mingw64-gcc-c++ = %{version}-%{release}
Requires:       mingw64-gcc-objc = %{version}-%{release}

%description -n mingw64-gcc-objc++
MinGW Windows cross-compiler support for Objective C++ for the win64 target.

%package -n mingw64-gcc-gfortran
Summary:        MinGW Windows cross-compiler for FORTRAN for the win64 target
Requires:       mingw64-gcc = %{version}-%{release}

%if 0%{bootstrap} == 0 && 0%{?rhel} == 6
Provides:       mingw64(libgfortran-3.dll)
Requires:       mingw64(libquadmath-0.dll)
%endif

%description -n mingw64-gcc-gfortran
MinGW Windows cross-compiler for FORTRAN for the win64 target.

%if 0%{enable_libgomp}
%package -n mingw64-libgomp
Summary:        GCC OpenMP v3.0 shared support library for the win64 target
Requires:       mingw64-gcc = %{version}-%{release}

%if 0%{bootstrap} == 0 && 0%{?rhel} == 6
# libgomp dll is linked with pthreads, but since we don't run the
# automatic dependency scripts, it doesn't get picked up automatically.
Requires:       mingw64-pthreads
Provides:       mingw64(libgomp-1.dll)
%endif

%description -n mingw64-libgomp
This package contains GCC shared support library which is
needed for OpenMP v3.0 support for the win32 target.
%endif


%prep
%setup -q -n %{source_folder}
echo 'Magic MinGW %{version}-%{release}' > gcc/DEV-PHASE


%build
# Default configure arguments
configure_args="\
    --prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --includedir=%{_includedir} \
    --libdir=%{_libdir} \
    --mandir=%{_mandir} \
    --infodir=%{_infodir} \
    --datadir=%{_datadir} \
    --build=%_build --host=%_host \
    --with-gnu-as --with-gnu-ld --verbose \
    --without-newlib \
    --disable-multilib \
    --disable-plugin \
    --with-system-zlib \
    --disable-nls --without-included-gettext \
    --disable-win32-registry \
    --enable-languages="c,c++,objc,obj-c++,fortran" \
    --with-bugurl=http://www.magiclinux.org/bugs"

# PPL/CLOOG optimalisations are only available on Fedora
%if 0%{?fedora}
configure_args="$configure_args --with-cloog"
%endif

# When bootstrapping, disable LTO support as it causes errors while building any binary
# $ i686-w64-mingw32-gcc -o conftest    conftest.c  >&5
# i686-w64-mingw32-gcc: fatal error: -fuse-linker-plugin, but liblto_plugin.so not found
%if 0%{bootstrap}
configure_args="$configure_args --disable-lto"
%endif

%if 0%{enable_winpthreads}
configure_args="$configure_args --with-threads=posix"
%endif

%if 0%{enable_libgomp}
configure_args="$configure_args --enable-libgomp"
%endif

# The %%configure macro can't be used for out of source builds
# without overriding other variables and causes unwanted side
# effects so make sure the right compiler flags are used
export CC="%{__cc} ${RPM_OPT_FLAGS}"

# Win32
mkdir build_win32
pushd build_win32
    ../configure $configure_args --target=%{mingw32_target} --with-sysroot=%{mingw32_sysroot} --with-gxx-include-dir=%{mingw32_includedir}/c++
popd

# Win64
mkdir build_win64
pushd build_win64
    ../configure $configure_args --target=%{mingw64_target} --with-sysroot=%{mingw64_sysroot} --with-gxx-include-dir=%{mingw64_includedir}/c++
popd

# If we're bootstrapping, only build the GCC core
%if 0%{bootstrap}
%mingw_make %{?_smp_mflags} all-gcc
%else
%mingw_make %{?_smp_mflags} all
%endif


%if 0%{enable_tests}
%check
# Win32
# Create a seperate wine prefix
export WINEPREFIX=/tmp/.wine_gcc_testsuite
rm -rf $WINEPREFIX
mkdir $WINEPREFIX

# The command below will fail, but that's intentional
# We only have to call a wine binary which triggers
# the generation and population of a wine prefix
winecfg || :

# Copy the GCC DLL's inside the wine prefix
SYSTEM32_DIR=$WINEPREFIX/drive_c/windows/syswow64
if [ ! -d $SYSTEM32_DIR ] ; then
    SYSTEM32_DIR=$WINEPREFIX/drive_c/windows/system32
fi
cp build_win32/i686-w64-mingw32/libquadmath/.libs/libquadmath-0.dll $SYSTEM32_DIR
cp build_win32/i686-w64-mingw32/libgfortran/.libs/libgfortran-3.dll $SYSTEM32_DIR
cp build_win32/i686-w64-mingw32/libobjc/.libs/libobjc-4.dll $SYSTEM32_DIR
cp build_win32/i686-w64-mingw32/libssp/.libs/libssp-0.dll $SYSTEM32_DIR
cp build_win32/i686-w64-mingw32/libstdc++-v3/src/.libs/libstdc++-6.dll $SYSTEM32_DIR
cp build_win32/i686-w64-mingw32/libgcc/shlib/libgcc_s_sjlj-1.dll $SYSTEM32_DIR
%if 0%{enable_libgomp}
%if 0%{enable_winpthreads}
cp %{mingw32_bindir}/libwinpthread-1.dll $SYSTEM32_DIR
%else
cp %{mingw32_bindir}/pthreadGC2.dll $SYSTEM32_DIR
%endif
cp build_win32/i686-w64-mingw32/libgomp/.libs/libgomp-1.dll $SYSTEM32_DIR
%endif

SYSTEM64_DIR=$WINEPREFIX/drive_c/windows/system32
cp build_win64/x86_64-w64-mingw32/libquadmath/.libs/libquadmath-0.dll $SYSTEM64_DIR
cp build_win64/x86_64-w64-mingw32/libgfortran/.libs/libgfortran-3.dll $SYSTEM64_DIR
cp build_win64/x86_64-w64-mingw32/libobjc/.libs/libobjc-4.dll $SYSTEM64_DIR
cp build_win64/x86_64-w64-mingw32/libssp/.libs/libssp-0.dll $SYSTEM64_DIR
cp build_win64/x86_64-w64-mingw32/libstdc++-v3/src/.libs/libstdc++-6.dll $SYSTEM64_DIR
cp build_win64/x86_64-w64-mingw32/libgcc/shlib/libgcc_s_seh-1.dll $SYSTEM64_DIR
%if 0%{enable_libgomp}
%if 0%{enable_winpthreads}
cp %{mingw64_bindir}/libwinpthread-1.dll $SYSTEM64_DIR
%else
cp %{mingw64_bindir}/pthreadGC2.dll $SYSTEM64_DIR
%endif
cp build_win64/x86_64-w64-mingw32/libgomp/.libs/libgomp-1.dll $SYSTEM64_DIR
%endif

# According to Kai Tietz (of the mingw-w64 project) it's recommended
# to set the environment variable GCOV_PREFIX_STRIP
export GCOV_PREFIX_STRIP=1000

# Run the testsuite
# Code taken from the native Magic GCC package to collect testsuite results
pushd build_win32
    make -k check %{?_smp_mflags} || :
    echo ====================TESTING WIN32=========================
    ( LC_ALL=C ../contrib/test_summary || : ) 2>&1 | sed -n '/^cat.*EOF/,/^EOF/{/^cat.*EOF/d;/^EOF/d;/^LAST_UPDATED:/d;p;}'
    echo ====================TESTING WIN32 END=====================
    mkdir testlogs-%{mingw32_target}-%{version}-%{release}
    for i in `find . -name \*.log | grep -F testsuite/ | grep -v 'config.log\|acats.*/tests/'`; do
        ln $i testlogs-%{mingw32_target}-%{version}-%{release}/ || :
    done
    tar cf - testlogs-%{mingw32_target}-%{version}-%{release} | bzip2 -9c \
        | uuencode testlogs-%{mingw32_target}.tar.bz2 || :
    rm -rf testlogs-%{mingw32_target}-%{version}-%{release}
popd

pushd build_win64
    make -k check %{?_smp_mflags} || :
    echo ====================TESTING WIN64=========================
    ( LC_ALL=C ../contrib/test_summary || : ) 2>&1 | sed -n '/^cat.*EOF/,/^EOF/{/^cat.*EOF/d;/^EOF/d;/^LAST_UPDATED:/d;p;}'
    echo ====================TESTING WIN64 END=====================
    mkdir testlogs-%{mingw64_target}-%{version}-%{release}
    for i in `find . -name \*.log | grep -F testsuite/ | grep -v 'config.log\|acats.*/tests/'`; do
        ln $i testlogs-%{mingw64_target}-%{version}-%{release}/ || :
    done
    tar cf - testlogs-%{mingw64_target}-%{version}-%{release} | bzip2 -9c \
        | uuencode testlogs-%{mingw64_target}.tar.bz2 || :
    rm -rf testlogs-%{mingw64_target}-%{version}-%{release}
popd

%endif


%install
%if 0%{bootstrap}
%mingw_make DESTDIR=$RPM_BUILD_ROOT install-gcc
%else
%mingw_make_install DESTDIR=$RPM_BUILD_ROOT
%endif

# These files conflict with existing installed files.
rm -rf $RPM_BUILD_ROOT%{_infodir}
rm -f $RPM_BUILD_ROOT%{_libdir}/libiberty*
rm -f $RPM_BUILD_ROOT%{_mandir}/man7/*
rm -rf $RPM_BUILD_ROOT%{_datadir}/gcc-%{version}/python

%if 0%{bootstrap} == 0
# Move the DLL's manually to the correct location
mkdir -p $RPM_BUILD_ROOT%{mingw32_bindir}
mv    $RPM_BUILD_ROOT%{_prefix}/%{mingw32_target}/lib/libgcc_s_sjlj-1.dll \
      $RPM_BUILD_ROOT%{_prefix}/%{mingw32_target}/lib/libssp-0.dll \
      $RPM_BUILD_ROOT%{_prefix}/%{mingw32_target}/lib/libstdc++-6.dll \
      $RPM_BUILD_ROOT%{_prefix}/%{mingw32_target}/lib/libobjc-4.dll \
      $RPM_BUILD_ROOT%{_prefix}/%{mingw32_target}/lib/libgfortran-3.dll \
      $RPM_BUILD_ROOT%{_prefix}/%{mingw32_target}/lib/libquadmath-0.dll \
%if 0%{enable_libgomp}
      $RPM_BUILD_ROOT%{_prefix}/%{mingw32_target}/lib/libgomp-1.dll \
%endif
      $RPM_BUILD_ROOT%{mingw32_bindir}

mkdir -p $RPM_BUILD_ROOT%{mingw64_bindir}
mv    $RPM_BUILD_ROOT%{_prefix}/%{mingw64_target}/lib/libgcc_s_seh-1.dll \
      $RPM_BUILD_ROOT%{_prefix}/%{mingw64_target}/lib/libssp-0.dll \
      $RPM_BUILD_ROOT%{_prefix}/%{mingw64_target}/lib/libstdc++-6.dll \
      $RPM_BUILD_ROOT%{_prefix}/%{mingw64_target}/lib/libobjc-4.dll \
      $RPM_BUILD_ROOT%{_prefix}/%{mingw64_target}/lib/libgfortran-3.dll \
      $RPM_BUILD_ROOT%{_prefix}/%{mingw64_target}/lib/libquadmath-0.dll \
%if 0%{enable_libgomp}
      $RPM_BUILD_ROOT%{_prefix}/%{mingw64_target}/lib/libgomp-1.dll \
%endif
      $RPM_BUILD_ROOT%{mingw64_bindir}

# Various import libraries are placed in the wrong folder
mkdir -p $RPM_BUILD_ROOT%{mingw32_libdir}
mkdir -p $RPM_BUILD_ROOT%{mingw64_libdir}
mv $RPM_BUILD_ROOT%{_prefix}/%{mingw32_target}/lib/* $RPM_BUILD_ROOT%{mingw32_libdir}
mv $RPM_BUILD_ROOT%{_prefix}/%{mingw64_target}/lib/* $RPM_BUILD_ROOT%{mingw64_libdir}

# Don't want the *.la files.
find $RPM_BUILD_ROOT -name '*.la' -delete

%endif

# For some reason there are wrapper libraries created named $target-$target-gcc-$tool
# Drop those files for now as this looks like a bug in GCC
rm -f $RPM_BUILD_ROOT%{_bindir}/%{mingw32_target}-%{mingw32_target}-*
rm -f $RPM_BUILD_ROOT%{_bindir}/%{mingw64_target}-%{mingw64_target}-*


%files -n mingw32-gcc
%{_bindir}/%{mingw32_target}-gcc
%{_bindir}/%{mingw32_target}-gcc-%{version}
%{_bindir}/%{mingw32_target}-gcc-ar
%{_bindir}/%{mingw32_target}-gcc-nm
%{_bindir}/%{mingw32_target}-gcc-ranlib
%{_bindir}/%{mingw32_target}-gcov
%dir %{_libdir}/gcc/%{mingw32_target}/%{version}
%dir %{_libdir}/gcc/%{mingw32_target}/%{version}/include-fixed
%dir %{_libdir}/gcc/%{mingw32_target}/%{version}/include
%dir %{_libdir}/gcc/%{mingw32_target}/%{version}/install-tools
%{_libdir}/gcc/%{mingw32_target}/%{version}/include-fixed/README
%{_libdir}/gcc/%{mingw32_target}/%{version}/include-fixed/*.h
%{_libdir}/gcc/%{mingw32_target}/%{version}/include/*.h
%{_libdir}/gcc/%{mingw32_target}/%{version}/install-tools/*
%{_libexecdir}/gcc/%{mingw32_target}/%{version}/collect2
%{_libexecdir}/gcc/%{mingw32_target}/%{version}/lto-wrapper
%{_libexecdir}/gcc/%{mingw32_target}/%{version}/install-tools
%{_mandir}/man1/%{mingw32_target}-gcc.1*
%{_mandir}/man1/%{mingw32_target}-gcov.1*

# Non-bootstrap files
%if 0%{bootstrap} == 0
%{mingw32_bindir}/libgcc_s_sjlj-1.dll
%{mingw32_bindir}/libssp-0.dll
%{mingw32_libdir}/libgcc_s.a
%{mingw32_libdir}/libssp.a
%{mingw32_libdir}/libssp.dll.a
%{mingw32_libdir}/libssp_nonshared.a
%{_libdir}/gcc/%{mingw32_target}/%{version}/crtbegin.o
%{_libdir}/gcc/%{mingw32_target}/%{version}/crtend.o
%{_libdir}/gcc/%{mingw32_target}/%{version}/crtfastmath.o
%{_libdir}/gcc/%{mingw32_target}/%{version}/libgcc.a
%{_libdir}/gcc/%{mingw32_target}/%{version}/libgcc_eh.a
%{_libdir}/gcc/%{mingw32_target}/%{version}/libgcov.a
%dir %{_libdir}/gcc/%{mingw32_target}/%{version}/include/ssp
%{_libdir}/gcc/%{mingw32_target}/%{version}/include/ssp/*.h
%{_libexecdir}/gcc/%{mingw32_target}/%{version}/lto1
%{_libexecdir}/gcc/%{mingw32_target}/%{version}/liblto_plugin.so
%{_libexecdir}/gcc/%{mingw32_target}/%{version}/liblto_plugin.so.0
%{_libexecdir}/gcc/%{mingw32_target}/%{version}/liblto_plugin.so.0.0.0
%endif

%files -n mingw64-gcc
%{_bindir}/%{mingw64_target}-gcc
%{_bindir}/%{mingw64_target}-gcc-%{version}
%{_bindir}/%{mingw64_target}-gcc-ar
%{_bindir}/%{mingw64_target}-gcc-nm
%{_bindir}/%{mingw64_target}-gcc-ranlib
%{_bindir}/%{mingw64_target}-gcov
%dir %{_libdir}/gcc/%{mingw64_target}/%{version}
%dir %{_libdir}/gcc/%{mingw64_target}/%{version}/include-fixed
%dir %{_libdir}/gcc/%{mingw64_target}/%{version}/include
%dir %{_libdir}/gcc/%{mingw64_target}/%{version}/install-tools
%{_libdir}/gcc/%{mingw64_target}/%{version}/include-fixed/README
%{_libdir}/gcc/%{mingw64_target}/%{version}/include-fixed/*.h
%{_libdir}/gcc/%{mingw64_target}/%{version}/include/*.h
%{_libdir}/gcc/%{mingw64_target}/%{version}/install-tools/*
%{_libexecdir}/gcc/%{mingw64_target}/%{version}/collect2
%{_libexecdir}/gcc/%{mingw64_target}/%{version}/lto-wrapper
%{_libexecdir}/gcc/%{mingw64_target}/%{version}/install-tools
%{_mandir}/man1/%{mingw64_target}-gcc.1*
%{_mandir}/man1/%{mingw64_target}-gcov.1*

# Non-bootstrap files
%if 0%{bootstrap} == 0
%{mingw64_bindir}/libgcc_s_seh-1.dll
%{mingw64_bindir}/libssp-0.dll
%{mingw64_libdir}/libgcc_s.a
%{mingw64_libdir}/libssp.a
%{mingw64_libdir}/libssp.dll.a
%{mingw64_libdir}/libssp_nonshared.a
#%{_libdir}/gcc/%{mingw64_target}/%{version}/crtbegin.o
#%{_libdir}/gcc/%{mingw64_target}/%{version}/crtend.o
%{_libdir}/gcc/%{mingw64_target}/%{version}/crtfastmath.o
%{_libdir}/gcc/%{mingw64_target}/%{version}/libgcc.a
%{_libdir}/gcc/%{mingw64_target}/%{version}/libgcc_eh.a
%{_libdir}/gcc/%{mingw64_target}/%{version}/libgcov.a
%dir %{_libdir}/gcc/%{mingw64_target}/%{version}/include/ssp
%{_libdir}/gcc/%{mingw64_target}/%{version}/include/ssp/*.h
%{_libexecdir}/gcc/%{mingw64_target}/%{version}/lto1
%{_libexecdir}/gcc/%{mingw64_target}/%{version}/liblto_plugin.so
%{_libexecdir}/gcc/%{mingw64_target}/%{version}/liblto_plugin.so.0
%{_libexecdir}/gcc/%{mingw64_target}/%{version}/liblto_plugin.so.0.0.0
%endif

%files -n mingw32-cpp
%{_bindir}/%{mingw32_target}-cpp
%{_mandir}/man1/%{mingw32_target}-cpp.1*
%dir %{_libdir}/gcc/%{mingw32_target}
%dir %{_libdir}/gcc/%{mingw32_target}/%{version}
%dir %{_libexecdir}/gcc/%{mingw32_target}/%{version}
%dir %{_libexecdir}/gcc/%{mingw32_target}
%{_libexecdir}/gcc/%{mingw32_target}/%{version}/cc1

%files -n mingw64-cpp
%{_bindir}/%{mingw64_target}-cpp
%{_mandir}/man1/%{mingw64_target}-cpp.1*
%dir %{_libdir}/gcc/%{mingw64_target}
%dir %{_libdir}/gcc/%{mingw64_target}/%{version}
%dir %{_libexecdir}/gcc/%{mingw64_target}/%{version}
%dir %{_libexecdir}/gcc/%{mingw64_target}
%{_libexecdir}/gcc/%{mingw64_target}/%{version}/cc1

%files -n mingw32-gcc-c++
%{_bindir}/%{mingw32_target}-g++
%{_bindir}/%{mingw32_target}-c++
%{_mandir}/man1/%{mingw32_target}-g++.1*
%{_libexecdir}/gcc/%{mingw32_target}/%{version}/cc1plus

# Non-bootstrap files
%if 0%{bootstrap} == 0
%{mingw32_includedir}/c++/
%{mingw32_bindir}/libstdc++-6.dll
%{mingw32_libdir}/libstdc++.a
%{mingw32_libdir}/libstdc++.dll.a
%{mingw32_libdir}/libstdc++.dll.a-gdb.py
%{mingw32_libdir}/libsupc++.a
%endif

%files -n mingw64-gcc-c++
%{_bindir}/%{mingw64_target}-g++
%{_bindir}/%{mingw64_target}-c++
%{_mandir}/man1/%{mingw64_target}-g++.1*
%{_libexecdir}/gcc/%{mingw64_target}/%{version}/cc1plus

# Non-bootstrap files
%if 0%{bootstrap} == 0
%{mingw64_includedir}/c++/
%{mingw64_bindir}/libstdc++-6.dll
%{mingw64_libdir}/libstdc++.a
%{mingw64_libdir}/libstdc++.dll.a
%{mingw64_libdir}/libstdc++.dll.a-gdb.py
%{mingw64_libdir}/libsupc++.a
%endif

%files -n mingw32-gcc-objc
%{_libexecdir}/gcc/%{mingw32_target}/%{version}/cc1obj
%if 0%{bootstrap} == 0
%{_libdir}/gcc/%{mingw32_target}/%{version}/include/objc/
%{mingw32_bindir}/libobjc-4.dll
%{mingw32_libdir}/libobjc.a
%{mingw32_libdir}/libobjc.dll.a
%endif

%files -n mingw64-gcc-objc
%{_libexecdir}/gcc/%{mingw64_target}/%{version}/cc1obj
%if 0%{bootstrap} == 0
%{_libdir}/gcc/%{mingw64_target}/%{version}/include/objc/
%{mingw64_bindir}/libobjc-4.dll
%{mingw64_libdir}/libobjc.a
%{mingw64_libdir}/libobjc.dll.a
%endif

%files -n mingw32-gcc-objc++
%{_libexecdir}/gcc/%{mingw32_target}/%{version}/cc1objplus

%files -n mingw64-gcc-objc++
%{_libexecdir}/gcc/%{mingw64_target}/%{version}/cc1objplus

%files -n mingw32-gcc-gfortran
%{_bindir}/%{mingw32_target}-gfortran
%{_mandir}/man1/%{mingw32_target}-gfortran.1*
%{_libexecdir}/gcc/%{mingw32_target}/%{version}/f951
%if 0%{bootstrap} == 0
%{mingw32_bindir}/libgfortran-3.dll
%{mingw32_bindir}/libquadmath-0.dll
%{mingw32_libdir}/libgfortran.a
%{mingw32_libdir}/libgfortran.dll.a
%{mingw32_libdir}/libgfortran.spec
%{mingw32_libdir}/libquadmath.a
%{mingw32_libdir}/libquadmath.dll.a
%{_libdir}/gcc/%{mingw32_target}/%{version}/libgfortranbegin.a
%{_libdir}/gcc/%{mingw32_target}/%{version}/libcaf_single.a
%if 0%{enable_libgomp}
%{_libdir}/gcc/%{mingw32_target}/%{version}/finclude
%endif
%endif

%files -n mingw64-gcc-gfortran
%{_bindir}/%{mingw64_target}-gfortran
%{_mandir}/man1/%{mingw64_target}-gfortran.1*
%{_libexecdir}/gcc/%{mingw64_target}/%{version}/f951
%if 0%{bootstrap} == 0
%{mingw64_bindir}/libgfortran-3.dll
%{mingw64_bindir}/libquadmath-0.dll
%{mingw64_libdir}/libgfortran.a
%{mingw64_libdir}/libgfortran.dll.a
%{mingw64_libdir}/libgfortran.spec
%{mingw64_libdir}/libquadmath.a
%{mingw64_libdir}/libquadmath.dll.a
%{_libdir}/gcc/%{mingw64_target}/%{version}/libgfortranbegin.a
%{_libdir}/gcc/%{mingw64_target}/%{version}/libcaf_single.a
%if 0%{enable_libgomp}
%{_libdir}/gcc/%{mingw64_target}/%{version}/finclude
%endif
%endif

%if 0%{enable_libgomp}
%files -n mingw32-libgomp
%{mingw32_bindir}/libgomp-1.dll
%{mingw32_libdir}/libgomp.a
%{mingw32_libdir}/libgomp.dll.a
%{mingw32_libdir}/libgomp.spec

%files -n mingw64-libgomp
%{mingw64_bindir}/libgomp-1.dll
%{mingw64_libdir}/libgomp.a
%{mingw64_libdir}/libgomp.dll.a
%{mingw64_libdir}/libgomp.spec
%endif


%changelog
