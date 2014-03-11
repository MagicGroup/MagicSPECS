%?mingw_package_header

%global snapshot_date 20140124
%global snapshot_rev 6475
%global branch trunk

# Run the testsuite
%global enable_tests 0

Name:           mingw-winpthreads
Version:        3.1.999
Release:        0.2.%{branch}.r%{snapshot_rev}.%{snapshot_date}%{?dist}
Summary:        MinGW pthread library
# The main license of winpthreads is MIT, but parts of this library
# are derived from the "Posix Threads library for Microsoft Windows"
# http://locklessinc.com/articles/pthreads_on_windows/
License:        MIT and BSD
Group:          Development/Libraries

URL:            http://mingw-w64.sourceforge.net/
%if 0%{?snapshot_date}
# To regerenate a snapshot:
# Use your regular webbrowser to open http://sourceforge.net/p/mingw-w64/code/%{snapshot_rev}/tarball?path=/trunk
# This triggers the SourceForge instructure to generate a snapshot
# After that you can pull in the archive with:
# spectool -g mingw-winpthreads.spec
Source0:        http://sourceforge.net/code-snapshots/svn/m/mi/mingw-w64/code/mingw-w64-code-%{snapshot_rev}-%{branch}.zip
%else
Source0:        http://downloads.sourceforge.net/mingw-w64/mingw-w64-v%{version}.tar.bz2
%endif


BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 95
BuildRequires:  mingw64-filesystem >= 95
BuildRequires:  mingw32-gcc-c++
BuildRequires:  mingw64-gcc-c++

%if 0%{?enable_tests}
BuildRequires:  wine-wow
%endif


%description
The POSIX 1003.1-2001 standard defines an application programming
interface (API) for writing multithreaded applications. This interface
is known more commonly as pthreads. A good number of modern operating
systems include a threading library of some kind: Solaris (UI)
threads, Win32 threads, DCE threads, DECthreads, or any of the draft
revisions of the pthreads standard. The trend is that most of these
systems are slowly adopting the pthreads standard API, with
application developers following suit to reduce porting woes.

Win32 does not, and is unlikely to ever, support pthreads
natively. This project seeks to provide a freely available and
high-quality solution to this problem.

# Win32
%package -n mingw32-winpthreads
Summary:        MinGW pthread library for the win32 target
Obsoletes:      mingw32-pthreads < 2.8.0-25.20110511cvs
Provides:       mingw32-pthreads = 2.8.0-25.20110511cvs
Conflicts:      mingw32-headers < 2.0.999-0.22.trunk.20130428

%description -n mingw32-winpthreads
The POSIX 1003.1-2001 standard defines an application programming
interface (API) for writing multithreaded applications. This interface
is known more commonly as pthreads. A good number of modern operating
systems include a threading library of some kind: Solaris (UI)
threads, Win32 threads, DCE threads, DECthreads, or any of the draft
revisions of the pthreads standard. The trend is that most of these
systems are slowly adopting the pthreads standard API, with
application developers following suit to reduce porting woes.

Win32 does not, and is unlikely to ever, support pthreads
natively. This project seeks to provide a freely available and
high-quality solution to this problem.

%package -n mingw32-winpthreads-static
Summary:        Static version of the MinGW Windows pthreads library
Requires:       mingw32-winpthreads = %{version}-%{release}
Obsoletes:      mingw32-pthreads-static < 2.8.0-25.20110511cvs
Provides:       mingw32-pthreads-static = 2.8.0-25.20110511cvs

%description -n mingw32-winpthreads-static
Static version of the MinGW Windows pthreads library.

# Win64
%package -n mingw64-winpthreads
Summary:        MinGW pthread library for the win64 target
Obsoletes:      mingw64-pthreads < 2.8.0-25.20110511cvs
Provides:       mingw64-pthreads = 2.8.0-25.20110511cvs
Conflicts:      mingw64-headers < 2.0.999-0.22.trunk.20130428

%description -n mingw64-winpthreads
The POSIX 1003.1-2001 standard defines an application programming
interface (API) for writing multithreaded applications. This interface
is known more commonly as pthreads. A good number of modern operating
systems include a threading library of some kind: Solaris (UI)
threads, Win32 threads, DCE threads, DECthreads, or any of the draft
revisions of the pthreads standard. The trend is that most of these
systems are slowly adopting the pthreads standard API, with
application developers following suit to reduce porting woes.

Win32 does not, and is unlikely to ever, support pthreads
natively. This project seeks to provide a freely available and
high-quality solution to this problem.

%package -n mingw64-winpthreads-static
Summary:        Static version of the MinGW Windows pthreads library
Requires:       mingw64-winpthreads = %{version}-%{release}
Obsoletes:      mingw64-pthreads-static < 2.8.0-25.20110511cvs
Provides:       mingw64-pthreads-static = 2.8.0-25.20110511cvs

%description -n mingw64-winpthreads-static
Static version of the MinGW Windows pthreads library.


%?mingw_debug_package


%prep
%if 0%{?snapshot_date}
rm -rf mingw-w64-v%{version}
mkdir mingw-w64-v%{version}
cd mingw-w64-v%{version}
unzip %{S:0}
%setup -q -D -T -n mingw-w64-v%{version}/mingw-w64-code-%{snapshot_rev}-%{branch}
%else
%setup -q -n mingw-w64-v%{version}
%endif


%build
pushd mingw-w64-libraries/winpthreads
    %mingw_configure
    %mingw_make %{?smp_mflags}
popd


%if 0%{?enable_tests}

%check
# Prepare a wine prefix
export WINEPREFIX=/tmp/wine-winpthreads
mkdir $WINEPREFIX
winecfg || :

# Run the tests
pushd mingw-w64-libraries/winpthreads
    %mingw_make check -k || :
popd

# Clean up the wine prefix
wineserver --kill || :
rm -rf /tmp/wine-winpthreads

%endif


%install
pushd mingw-w64-libraries/winpthreads
    %mingw_make install DESTDIR=$RPM_BUILD_ROOT
popd

# Drop all .la files
find $RPM_BUILD_ROOT -name "*.la" -delete


# Win32
%files -n mingw32-winpthreads
%doc COPYING
%{mingw32_bindir}/libwinpthread-1.dll
%{mingw32_libdir}/libwinpthread.dll.a
%{mingw32_libdir}/libpthread.dll.a
%{mingw32_includedir}/pthread.h
%{mingw32_includedir}/pthread_compat.h
%{mingw32_includedir}/pthread_signal.h
%{mingw32_includedir}/pthread_time.h
%{mingw32_includedir}/pthread_unistd.h
%{mingw32_includedir}/sched.h
%{mingw32_includedir}/semaphore.h

%files -n mingw32-winpthreads-static
%{mingw32_libdir}/libwinpthread.a
%{mingw32_libdir}/libpthread.a

# Win64
%files -n mingw64-winpthreads
%doc COPYING 
%{mingw64_bindir}/libwinpthread-1.dll
%{mingw64_libdir}/libwinpthread.dll.a
%{mingw64_libdir}/libpthread.dll.a
%{mingw64_includedir}/pthread.h
%{mingw64_includedir}/pthread_compat.h
%{mingw64_includedir}/pthread_signal.h
%{mingw64_includedir}/pthread_time.h
%{mingw64_includedir}/pthread_unistd.h
%{mingw64_includedir}/sched.h
%{mingw64_includedir}/semaphore.h

%files -n mingw64-winpthreads-static
%{mingw64_libdir}/libwinpthread.a
%{mingw64_libdir}/libpthread.a


%changelog
* Fri Jan 24 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 3.1.999-0.2.trunk.r6460.20140124
- Update to r6460 (20140124 snapshot)

* Thu Jan  9 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 3.1.999-0.1.trunk.r6432.20140104
- Bump version to keep working upgrade path

* Mon Jan  6 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 3.0.999-0.2.trunk.r6432.20140104
- Update to r6432 (20140104 snapshot)

* Wed Nov 20 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 3.0.999-0.1.trunk.r6379.20131120
- Update to r6379 (20131120 snapshot)

* Fri Sep 20 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 3.0.0-1
- Update to 3.0.0

* Sat Sep  7 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.7.trunk.r6233.20130907
- Update to r6233 (20130907)
- Fixes mingw-libvirt build failure

* Fri Aug 16 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.6.trunk.r6069.20130810
- Update to r6069 (20130810 snapshot)

* Fri Jun 28 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.5.trunk.r5915.20130628
- Update to r5915 (20130628 snapshot)

* Sat May 11 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.4.trunk.20130509
- Simplified the BuildRequires
- Added a clarification for the combined license
- Added conflicts for mingw{32,64}-headers versions which also provide pthread headers

* Thu May  9 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.3.trunk.20130509
- Added -static subpackages
- Changed license to MIT and BSD

* Thu May  9 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.2.trunk.20130509
- Update to 20130509 snapshot
- Make the testsuite optional

* Mon Apr 29 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.1.trunk.20130429
- Update to 20130429 snapshot

* Fri Feb 24 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 0-0.1.20120224
- Initial package

