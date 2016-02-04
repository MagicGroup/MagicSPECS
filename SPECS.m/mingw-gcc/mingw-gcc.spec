%global __os_install_post /usr/lib/rpm/brp-compress %{nil}

# Set this to one when mingw-crt isn't built yet
%global bootstrap 0

# C++11 threads requires winpthreads so this can only be enabled once winpthreads is built
%if 0%{?fedora} >= 21 || 0%{?rhel} >= 7
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
#%%global snapshot_date 20150405
#%%global snapshot_rev 221873

# When building from a snapshot the name of the source folder is different
%if 0%{?snapshot_date}
%global source_folder gcc-5-%{snapshot_date}
%else
%global source_folder gcc-%{version}
%endif

Name:           mingw-gcc
Version:        5.3.0
Release:        1%{?snapshot_date:.svn.%{snapshot_date}.r%{snapshot_rev}}%{?dist}
Summary:        MinGW Windows cross-compiler (GCC) for C

License:        GPLv3+ and GPLv3+ with exceptions and GPLv2+ with exceptions
Group:          Development/Languages
URL:            http://gcc.gnu.org
%if 0%{?snapshot_date}
Source0:        ftp://ftp.nluug.nl/mirror/languages/gcc/snapshots/5-%{snapshot_date}/gcc-5-%{snapshot_date}.tar.bz2
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
%if 0%{?fedora} > 0
%if 0%{?fedora} >= 21
BuildRequires:  cloog-devel
%else
BuildRequires:  cloog-ppl cloog-ppl-devel
%endif
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
echo 'Fedora MinGW %{version}-%{release}' > gcc/DEV-PHASE


%build
# Default configure arguments
configure_args="\
    --prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --includedir=%{_includedir} \
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
%if 0%{fedora} == 22
    --with-default-libstdcxx-abi=c++98 \
%endif
    --with-bugurl=http://bugzilla.redhat.com/bugzilla"

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
configure_args="$configure_args --enable-threads=posix"
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
# Code taken from the native Fedora GCC package to collect testsuite results
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
mv    $RPM_BUILD_ROOT%{_prefix}/%{mingw32_target}/lib/libatomic-1.dll \
      $RPM_BUILD_ROOT%{_prefix}/%{mingw32_target}/lib/libgcc_s_sjlj-1.dll \
      $RPM_BUILD_ROOT%{_prefix}/%{mingw32_target}/lib/libssp-0.dll \
      $RPM_BUILD_ROOT%{_prefix}/%{mingw32_target}/lib/libstdc++-6.dll \
      $RPM_BUILD_ROOT%{_prefix}/%{mingw32_target}/lib/libobjc-4.dll \
      $RPM_BUILD_ROOT%{_prefix}/%{mingw32_target}/lib/libgfortran-3.dll \
      $RPM_BUILD_ROOT%{_prefix}/%{mingw32_target}/lib/libquadmath-0.dll \
      $RPM_BUILD_ROOT%{_prefix}/%{mingw32_target}/lib/libvtv-0.dll \
      $RPM_BUILD_ROOT%{_prefix}/%{mingw32_target}/lib/libvtv_stubs-0.dll \
%if 0%{enable_libgomp}
      $RPM_BUILD_ROOT%{_prefix}/%{mingw32_target}/lib/libgomp-1.dll \
      $RPM_BUILD_ROOT%{_prefix}/%{mingw32_target}/lib/libgomp-plugin-host_nonshm-1.dll \
%endif
      $RPM_BUILD_ROOT%{mingw32_bindir}

mkdir -p $RPM_BUILD_ROOT%{mingw64_bindir}
mv    $RPM_BUILD_ROOT%{_prefix}/%{mingw64_target}/lib/libatomic-1.dll \
      $RPM_BUILD_ROOT%{_prefix}/%{mingw64_target}/lib/libgcc_s_seh-1.dll \
      $RPM_BUILD_ROOT%{_prefix}/%{mingw64_target}/lib/libssp-0.dll \
      $RPM_BUILD_ROOT%{_prefix}/%{mingw64_target}/lib/libstdc++-6.dll \
      $RPM_BUILD_ROOT%{_prefix}/%{mingw64_target}/lib/libobjc-4.dll \
      $RPM_BUILD_ROOT%{_prefix}/%{mingw64_target}/lib/libgfortran-3.dll \
      $RPM_BUILD_ROOT%{_prefix}/%{mingw64_target}/lib/libquadmath-0.dll \
      $RPM_BUILD_ROOT%{_prefix}/%{mingw64_target}/lib/libvtv-0.dll \
      $RPM_BUILD_ROOT%{_prefix}/%{mingw64_target}/lib/libvtv_stubs-0.dll \
%if 0%{enable_libgomp}
      $RPM_BUILD_ROOT%{_prefix}/%{mingw64_target}/lib/libgomp-1.dll \
      $RPM_BUILD_ROOT%{_prefix}/%{mingw64_target}/lib/libgomp-plugin-host_nonshm-1.dll \
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
%{_bindir}/%{mingw32_target}-gcov-tool
%dir %{_prefix}/lib/gcc/%{mingw32_target}/%{version}
%dir %{_prefix}/lib/gcc/%{mingw32_target}/%{version}/include-fixed
%dir %{_prefix}/lib/gcc/%{mingw32_target}/%{version}/include
%dir %{_prefix}/lib/gcc/%{mingw32_target}/%{version}/install-tools
%{_prefix}/lib/gcc/%{mingw32_target}/%{version}/include-fixed/README
%{_prefix}/lib/gcc/%{mingw32_target}/%{version}/include-fixed/*.h
%{_prefix}/lib/gcc/%{mingw32_target}/%{version}/include/*.h
%{_prefix}/lib/gcc/%{mingw32_target}/%{version}/install-tools/*
%{_libexecdir}/gcc/%{mingw32_target}/%{version}/collect2
%{_libexecdir}/gcc/%{mingw32_target}/%{version}/lto-wrapper
%{_libexecdir}/gcc/%{mingw32_target}/%{version}/install-tools
%{_mandir}/man1/%{mingw32_target}-gcc.1*
%{_mandir}/man1/%{mingw32_target}-gcov.1*

# Non-bootstrap files
%if 0%{bootstrap} == 0
%{mingw32_bindir}/libatomic-1.dll
%{mingw32_bindir}/libgcc_s_sjlj-1.dll
%{mingw32_bindir}/libssp-0.dll
%{mingw32_bindir}/libvtv-0.dll
%{mingw32_bindir}/libvtv_stubs-0.dll
%{mingw32_libdir}/libatomic.a
%{mingw32_libdir}/libatomic.dll.a
%{mingw32_libdir}/libgcc_s.a
%{mingw32_libdir}/libssp.a
%{mingw32_libdir}/libssp.dll.a
%{mingw32_libdir}/libssp_nonshared.a
%{mingw32_libdir}/libvtv.a
%{mingw32_libdir}/libvtv.dll.a
%{mingw32_libdir}/libvtv_stubs.a
%{mingw32_libdir}/libvtv_stubs.dll.a
%{_prefix}/lib/gcc/%{mingw32_target}/%{version}/crtbegin.o
%{_prefix}/lib/gcc/%{mingw32_target}/%{version}/crtend.o
%{_prefix}/lib/gcc/%{mingw32_target}/%{version}/crtfastmath.o
%{_prefix}/lib/gcc/%{mingw32_target}/%{version}/libgcc.a
%{_prefix}/lib/gcc/%{mingw32_target}/%{version}/libgcc_eh.a
%{_prefix}/lib/gcc/%{mingw32_target}/%{version}/libgcov.a
%dir %{_prefix}/lib/gcc/%{mingw32_target}/%{version}/include/ssp
%{_prefix}/lib/gcc/%{mingw32_target}/%{version}/include/ssp/*.h
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
%{_bindir}/%{mingw64_target}-gcov-tool
%dir %{_prefix}/lib/gcc/%{mingw64_target}/%{version}
%dir %{_prefix}/lib/gcc/%{mingw64_target}/%{version}/include-fixed
%dir %{_prefix}/lib/gcc/%{mingw64_target}/%{version}/include
%dir %{_prefix}/lib/gcc/%{mingw64_target}/%{version}/install-tools
%{_prefix}/lib/gcc/%{mingw64_target}/%{version}/include-fixed/README
%{_prefix}/lib/gcc/%{mingw64_target}/%{version}/include-fixed/*.h
%{_prefix}/lib/gcc/%{mingw64_target}/%{version}/include/*.h
%{_prefix}/lib/gcc/%{mingw64_target}/%{version}/install-tools/*
%{_libexecdir}/gcc/%{mingw64_target}/%{version}/collect2
%{_libexecdir}/gcc/%{mingw64_target}/%{version}/lto-wrapper
%{_libexecdir}/gcc/%{mingw64_target}/%{version}/install-tools
%{_mandir}/man1/%{mingw64_target}-gcc.1*
%{_mandir}/man1/%{mingw64_target}-gcov.1*

# Non-bootstrap files
%if 0%{bootstrap} == 0
%{mingw64_bindir}/libatomic-1.dll
%{mingw64_bindir}/libgcc_s_seh-1.dll
%{mingw64_bindir}/libssp-0.dll
%{mingw64_bindir}/libvtv-0.dll
%{mingw64_bindir}/libvtv_stubs-0.dll
%{mingw64_libdir}/libatomic.a
%{mingw64_libdir}/libatomic.dll.a
%{mingw64_libdir}/libgcc_s.a
%{mingw64_libdir}/libssp.a
%{mingw64_libdir}/libssp.dll.a
%{mingw64_libdir}/libssp_nonshared.a
%{mingw64_libdir}/libvtv.a
%{mingw64_libdir}/libvtv.dll.a
%{mingw64_libdir}/libvtv_stubs.a
%{mingw64_libdir}/libvtv_stubs.dll.a
%{_prefix}/lib/gcc/%{mingw64_target}/%{version}/crtbegin.o
%{_prefix}/lib/gcc/%{mingw64_target}/%{version}/crtend.o
%{_prefix}/lib/gcc/%{mingw64_target}/%{version}/crtfastmath.o
%{_prefix}/lib/gcc/%{mingw64_target}/%{version}/libgcc.a
%{_prefix}/lib/gcc/%{mingw64_target}/%{version}/libgcc_eh.a
%{_prefix}/lib/gcc/%{mingw64_target}/%{version}/libgcov.a
%dir %{_prefix}/lib/gcc/%{mingw64_target}/%{version}/include/ssp
%{_prefix}/lib/gcc/%{mingw64_target}/%{version}/include/ssp/*.h
%{_libexecdir}/gcc/%{mingw64_target}/%{version}/lto1
%{_libexecdir}/gcc/%{mingw64_target}/%{version}/liblto_plugin.so
%{_libexecdir}/gcc/%{mingw64_target}/%{version}/liblto_plugin.so.0
%{_libexecdir}/gcc/%{mingw64_target}/%{version}/liblto_plugin.so.0.0.0
%endif

%files -n mingw32-cpp
%{_bindir}/%{mingw32_target}-cpp
%{_mandir}/man1/%{mingw32_target}-cpp.1*
%dir %{_prefix}/lib/gcc/%{mingw32_target}
%dir %{_prefix}/lib/gcc/%{mingw32_target}/%{version}
%dir %{_libexecdir}/gcc/%{mingw32_target}/%{version}
%dir %{_libexecdir}/gcc/%{mingw32_target}
%{_libexecdir}/gcc/%{mingw32_target}/%{version}/cc1

%files -n mingw64-cpp
%{_bindir}/%{mingw64_target}-cpp
%{_mandir}/man1/%{mingw64_target}-cpp.1*
%dir %{_prefix}/lib/gcc/%{mingw64_target}
%dir %{_prefix}/lib/gcc/%{mingw64_target}/%{version}
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
%{_prefix}/lib/gcc/%{mingw32_target}/%{version}/include/objc/
%{mingw32_bindir}/libobjc-4.dll
%{mingw32_libdir}/libobjc.a
%{mingw32_libdir}/libobjc.dll.a
%endif

%files -n mingw64-gcc-objc
%{_libexecdir}/gcc/%{mingw64_target}/%{version}/cc1obj
%if 0%{bootstrap} == 0
%{_prefix}/lib/gcc/%{mingw64_target}/%{version}/include/objc/
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
%{_prefix}/lib/gcc/%{mingw32_target}/%{version}/libgfortranbegin.a
%{_prefix}/lib/gcc/%{mingw32_target}/%{version}/libcaf_single.a
%if 0%{enable_libgomp}
%{_prefix}/lib/gcc/%{mingw32_target}/%{version}/finclude
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
%{_prefix}/lib/gcc/%{mingw64_target}/%{version}/libgfortranbegin.a
%{_prefix}/lib/gcc/%{mingw64_target}/%{version}/libcaf_single.a
%if 0%{enable_libgomp}
%{_prefix}/lib/gcc/%{mingw64_target}/%{version}/finclude
%endif
%endif

%if 0%{enable_libgomp}
%files -n mingw32-libgomp
%{mingw32_bindir}/libgomp-1.dll
%{mingw32_bindir}/libgomp-plugin-host_nonshm-1.dll
%{mingw32_libdir}/libgomp.a
%{mingw32_libdir}/libgomp.dll.a
%{mingw32_libdir}/libgomp.spec
%{mingw32_libdir}/libgomp-plugin-host_nonshm.dll.a

%files -n mingw64-libgomp
%{mingw64_bindir}/libgomp-1.dll
%{mingw64_bindir}/libgomp-plugin-host_nonshm-1.dll
%{mingw64_libdir}/libgomp.a
%{mingw64_libdir}/libgomp.dll.a
%{mingw64_libdir}/libgomp.spec
%{mingw64_libdir}/libgomp-plugin-host_nonshm.dll.a
%endif


%changelog
* Tue Dec 08 2015 Kalev Lember <klember@redhat.com> - 5.3.0-1
- Update to 5.3.0

* Wed Aug  5 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.2.0-1
- Update to 5.2.0

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 11 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.1.0-2
- Export additional symbols needed to resolve boost build failure with GCC 5
- Resolves RHBZ #1218290, GCC #66030

* Fri Apr 24 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.1.0-1
- Update to 5.1.0

* Sat Apr 11 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0.0-0.4.svn.20150405.r221873
- Switch back to the old libstdcxx c++98 ABI on Fedora 22 only
  (This was also done for the native Fedora GCC package)

* Fri Apr 10 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0.0-0.3.svn.20150405.r221873
- Update to gcc 5 20150405 snapshot (rev 221873)

* Mon Mar 23 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0.0-0.2.svn.20150322.r221575
- Update to gcc 5 20150322 snapshot (rev 221575)

* Sat Mar  7 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0.0-0.1.svn.20150301.r221092
- Update to gcc 5 20150301 snapshot (rev 221092)

* Thu Jan 29 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.9.2-2
- The package cloog-ppl-devel was renamed to cloog-devel in rawhide

* Wed Dec  3 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.9.2-1
- Update to 4.9.2

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.9.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jul 30 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.9.1-3
- Use /usr/lib instead of %%{_libdir} (like also is done in
  the native gcc and cross-gcc packages)

* Mon Jul 28 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.9.1-2
- Really enable std::threads support

* Fri Jul 18 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.9.1-1
- Update to gcc 4.9.1

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr 23 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.9.0-1
- Update to gcc 4.9.0

* Sun Apr 13 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.9.0-0.1.rc1
- Update to gcc 4.9.0 RC1

* Fri Jan 10 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.8.2-2
- Dropped xmmintrin patch as the issue is resolved in mingw-w64 3.1.0

* Sat Oct 19 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.8.2-1
- Update to 4.8.2
- Build with C++11 std::thread support (F21+ only)

* Fri Sep 20 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.8.1-4
- Rebuild against winpthreads

* Sat Aug  3 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.8.1-3
- Own the folders %%{_libexecdir}/gcc/%%{mingw32_target}/%%{version},
  %%{_libexecdir}/gcc/%%{mingw32_target}, %%{_libexecdir}/gcc/%%{mingw64_target}
  and %%{_libexecdir}/gcc/%%{mingw64_target}/%%{version}

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jun 15 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.8.1-1
- Update to 4.8.1

* Sat Jun  1 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.8.0-4
- Revised patch for GCC bug #56742

* Sun Apr 14 2013 Nicola Fontana <ntd@entidi.it> - 4.8.0-3
- Dropped dependency on PPL (#951914)

* Sun Apr 14 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.8.0-2
- Fix optimization bug which can lead to uncaught throw (SEH related) (GCC bug #56742)

* Sat Mar 23 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.8.0-1
- Update to gcc 4.8.0 final

* Mon Mar 11 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.8.0-0.6.svn.20130310.r196584
- Update to gcc 4.8 20130310 snapshot (rev 196584)

* Fri Feb  8 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.8.0-0.5.svn.20130203.r195703
- Update to gcc 4.8 20130203 snapshot (rev 195703)

* Sun Jan 27 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.8.0-0.4.svn.20130120.r195326
- Update to gcc 4.8 20130120 snapshot (rev 195326)

* Fri Jan 18 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.8.0-0.3.svn.20130113.r195137
- Make sure the header xmmintrin.h is C++ compatible. Fixes build
  failure in the mingw-qt5-qtbase package

* Wed Jan 16 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.8.0-0.2.svn.20130113.r195137
- Update to gcc 4.8 20130113 snapshot (rev 195137)

* Sat Jan 12 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.8.0-0.1.svn.20130106.r194954
- Update to gcc 4.8 20130106 snapshot (rev 194954)
- The win64 compiler now uses SEH by default

* Wed Jan  2 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.7.2-7
- Backported imported fix regarding virtual thunks as recommended
  by upstream mingw-w64 developers (gcc bug #55171)

* Tue Dec 04 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.7.2-6
- Re-enable libgomp support

* Mon Dec 03 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.7.2-5
- Temporary build without libgomp support because of the broken circular
  dependency between mingw-gcc and mingw-pthreads which was caused by the
  latest PPL update

* Mon Dec 03 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.7.2-4
- Made this package compatible with RHEL6 and RHEL7
- Build with --disable-ppl-version-check (fixes FTBFS against latest PPL)

* Fri Nov 30 2012 Tom Callaway <spot@fedoraproject.org> - 4.7.2-3
- rebuild for new ppl/cloog

* Mon Oct 15 2012 Jon Ciesla <limbugher@gmail.com> - 4.7.2-2
- Provides: bundled(libiberty)

* Fri Sep 21 2012 Kalev Lember <kalevlember@gmail.com> - 4.7.2-1
- Update to 4.7.2

* Sat Jul 21 2012 Kalev Lember <kalevlember@gmail.com> - 4.7.1-3
- Revert back to 4.7.1 final

* Wed Jul 18 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.7.1-2.20120718
- Update to gcc 4.7 20120718 snapshot

* Sun Jul 15 2012 Kalev Lember <kalevlember@gmail.com> - 4.7.1-1
- Update to 4.7.1

* Wed Apr 04 2012 Kalev Lember <kalevlember@gmail.com> - 4.7.0-2
- Fix the build
- Switch to the release tarball
- Disable the testsuite again to avoid breaking build on arches where
  wine is unavailable

* Wed Mar 28 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.7.0-1.20120322
- Update to gcc 4.7.0 final release (20120322 snapshot)
- Dropped upstreamed patches
- Enable the testsuite

* Tue Mar  6 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.7.0-0.9.20120224
- Re-enable libgomp support

* Tue Mar  6 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.7.0-0.8.20120224
- Perform a regular build

* Tue Mar  6 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.7.0-0.7.20120224
- Added support for both win32 and win64 targets
- Perform a bootstrap build
- Split out the OpenMP pieces to mingw{32,64}-libgomp packages to avoid
  forced dependency on mingw{32,64}-pthreads
- Added support for running the testsuite for both win32 and win64 targets
- Added a %%global called enable_winpthreads which can be used to enable
  C++11 threads support (requires winpthreads instead of pthreads-w32)

* Tue Mar 06 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.7.0-0.6.20120224
- Renamed the source package to mingw-gcc (RHBZ #673788)
- Use mingw macros without leading underscore

* Mon Feb 27 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.7.0-0.5.20120224
- Re-enable libgomp support

* Mon Feb 27 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.7.0-0.4.20120224
- Perform a regular build

* Sat Feb 25 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.7.0-0.3.20120224
- Update to gcc 4.7 20120224 snapshot
- Perform a bootstrap build using mingw-w64
- Dropped the /lib/i686-pc-mingw32-cpp symlink
- Dropped the float.h patch as it isn't needed anymore with mingw-w64
- Added some patches which upstream mingw-w64 recommends us to apply

* Fri Jan 27 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.7.0-0.2.20120126
- Update to gcc 4.7 20120126 snapshot (fixes mingw32-qt build failure)

* Tue Jan 10 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.7.0-0.1.20120106
- Update to gcc 4.7 20120106 snapshot

* Wed Oct 26 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4.6.1-3.2
- rebuild with new gmp without compat lib

* Wed Oct 12 2011 Peter Schiffer <pschiffe@redhat.com> - 4.6.1-3.1
- rebuild with new gmp

* Fri Aug 26 2011 Kalev Lember <kalevlember@gmail.com> - 4.6.1-3
- Fix float.h inclusion when gcc's headers precede mingrt in include path

* Fri Aug 19 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.6.1-2
- Build against ppl and cloog

* Mon Jun 27 2011 Kalev Lember <kalev@smartlink.ee> - 4.6.1-1
- Update to 4.6.1

* Sat May 21 2011 Kalev Lember <kalev@smartlink.ee> - 4.5.3-3
- Rebuilt with automatic dep extraction and removed all manual
  mingw32(...) provides / requires
- Cleaned up the spec file from cruft not needed with latest rpm

* Tue May 10 2011 Kalev Lember <kalev@smartlink.ee> - 4.5.3-2
- Disable plugin support with a configure option, instead of deleting
  the files in the install section
- Use the %%{_mingw32_target} macro in files section

* Sat Apr 30 2011 Kalev Lember <kalev@smartlink.ee> - 4.5.3-1
- Update to 4.5.3

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Aug 05 2010 Kalev Lember <kalev@smartlink.ee> - 4.5.1-1
- Update to 4.5.1

* Thu May 13 2010 Kalev Lember <kalev@smartlink.ee> - 4.5.0-1
- Update to vanilla gcc 4.5.0
- Drop patches specific to Fedora native gcc.
- BuildRequires libmpc-devel and zlib-devel
- Added Provides for additional shared language runtime DLLs

* Thu Dec 17 2009 Chris Bagwell <chris@cnpbagwell.com> - 4.4.2-2
- Enable libgomp support.

* Sun Nov 22 2009 Kalev Lember <kalev@smartlink.ee> - 4.4.2-1
- Update to gcc 4.4.2 20091114 svn 154179, which includes
  VTA backport from 4.5 branch.
- Patches taken from native Fedora gcc-4.4.2-10.

* Fri Sep 18 2009 Kalev Lember <kalev@smartlink.ee> - 4.4.1-3
- Require mingw32-binutils >= 2.19.51.0.14 for %%gnu_unique_object support.

* Thu Sep 03 2009 Kalev Lember <kalev@smartlink.ee> - 4.4.1-2
- Update to gcc 4.4.1 20090902 svn 151328.
- Patches taken from native Fedora gcc-4.4.1-8.
- Another license update to keep it in sync with native gcc package.

* Sun Aug 23 2009 Kalev Lember <kalev@smartlink.ee> - 4.4.1-1
- Update to gcc 4.4.1 20090818 svn 150873.
- Patches taken from native Fedora gcc-4.4.1-6.
- Replaced %%define with %%global and updated %%defattr.
- Changed license to match native Fedora gcc package.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.4.0-0.8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Mar 23 2009 Richard W.M. Jones <rjones@redhat.com> - 4.4.0-0.7
- New native Fedora version gcc 4.4.0 20090319 svn 144967.
- Enable _smp_mflags.

* Wed Mar  4 2009 Richard W.M. Jones <rjones@redhat.com> - 4.4.0-0.6
- Fix libobjc and consequently Objective C and Objective C++ compilers.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.4.0-0.5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Richard W.M. Jones <rjones@redhat.com> - 4.4.0-0.4
- Rebuild for mingw32-gcc 4.4

* Thu Feb 19 2009 Richard W.M. Jones <rjones@redhat.com> - 4.4.0-0.2
- Move to upstream version 4.4.0-20090216 (same as Fedora native version).
- Added FORTRAN support.
- Added Objective C support.
- Added Objective C++ support.

* Mon Nov 24 2008 Richard W.M. Jones <rjones@redhat.com> - 4.3.2-12
- Rebuild against latest filesystem package.

* Fri Nov 21 2008 Richard W.M. Jones <rjones@redhat.com> - 4.3.2-11
- Remove obsoletes for a long dead package.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 4.3.2-10
- Rebuild against mingw32-filesystem 37

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 4.3.2-9
- Rebuild against mingw32-filesystem 36

* Thu Oct 30 2008 Richard W.M. Jones <rjones@redhat.com> - 4.3.2-8
- Don't BR mpfr-devel for RHEL/EPEL-5 (Levente Farkas).

* Thu Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 4.3.2-7
- Rename mingw -> mingw32.

* Thu Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 4.3.2-6
- Use RPM macros from mingw-filesystem.

* Mon Jul  7 2008 Richard W.M. Jones <rjones@redhat.com> - 4.3.2-3
- Initial RPM release, largely based on earlier work from several sources.
