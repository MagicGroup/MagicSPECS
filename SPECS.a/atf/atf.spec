Summary: Automated Testing Framework
Name: atf
Version: 0.20
Release: 1%{?dist}
License: BSD
Group: Development/Tools
URL: http://code.google.com/p/kyua/wiki/ATF
Source0: https://github.com/jmmv/atf/releases/download/%{name}-%{version}/%{name}-%{version}.tar.gz
Source1: README.Fedora

%define _testsdir %{_libexecdir}/atf/tests

%define common_description The Automated Testing Framework (ATF) is a collection of libraries to \
implement test programs in a variety of languages.  At the moment, ATF \
offers C, C++ and POSIX shell bindings with which to implement tests. \
These bindings all offer a similar set of functionality and any test \
program written with them exposes a consistent user interface. \
\
ATF-based test programs rely on a separate runtime engine to execute them. \
The runtime engine is in charge of isolating the test programs from the \
rest of the system to ensure that their results are deterministic and that \
they cannot affect the running system.  The runtime engine is also \
responsible for gathering the results of all tests and composing reports. \
The current runtime of choice is Kyua.

%description
There is no main package being built here.  This is unused.

%prep
%setup -q

# Put the README.Fedora file in the top-level directory of the source tree so
# that the %doc call below can pick it up.
cp -p %{SOURCE1} README.Fedora

%build
%configure INSTALL="/usr/bin/install -p" --disable-static
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags} pkgtestsdir=%{_testsdir} testsdir=%{_testsdir}

%check
make check

%install
make install DESTDIR=%{buildroot} doc_DATA= \
             pkgtestsdir=%{_testsdir} testsdir=%{_pkgtestsdir}
rm %{buildroot}%{_libdir}/libatf*.la

%changelog
* Mon Feb 10 2014 Julio Merino <julio@meroh.net> 0.20-1
- Update to new upstream version 0.20.
- The atf binary package, which used to provide the deprecated binary
  tools (atf-config, atf-report, atf-run and atf-version), is now gone.
- The libatf-c package now installs the atf-test-program(1) and
  atf-test-case(4) manual pages and the package documentation files.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Julio Merino <julio@meroh.net> 0.17-1
- Update to new upstream version 0.17.

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Julio Merino <julio@meroh.net> 0.16-1
- Updated to new upstream version 0.16.

* Mon Jun 18 2012 Julio Merino <jmmv@julipedia.org> 0.15-2
- Added the atf-tests package, which provides the run-time tests of ATF
  readily runnable by the end users.
- Made the installation of the package preserve the build times of the files.
- Fixed URL to the project's page.

* Thu May 3 2012 Julio Merino <jmmv@julipedia.org> 0.15-1
- Initial release for Fedora.


# Ideally, we would ship one tests package for every component, namely
# libatf-c-tests, libatf-c++-tests and libatf-sh-tests.  However, the test
# suite of ATF has not been written with this in mind, and the tests of one
# component often have dependencies on the rest of the components.  It is
# much easier to ship a single package with the whole test suite rather
# than attempting to fight this fact.
%package tests
Summary: Automated Testing Framework - Test suite
Requires: libatf-c = %{version}-%{release}
Requires: libatf-c++ = %{version}-%{release}
Requires: libatf-sh = %{version}-%{release}
Requires: libatf-c-devel = %{version}-%{release}
Requires: libatf-c++-devel = %{version}-%{release}
Requires: libatf-sh-devel = %{version}-%{release}

%description tests
%{common_description}

This package installs the run-time tests for all the components of ATF, which
include tests for the C, C++ and POSIX shell libraries and the run-time tools.
Please see the README.Fedora file in the documentation directory for further
details on how to run the installed tests.

%files tests
%doc README.Fedora
%{_testsdir}


%package -n libatf-c
Summary: Automated Testing Framework - C bindings

%description -n libatf-c
%{common_description}

This package provides the run-time libraries to run tests that use the
ATF C bindings.

%files -n libatf-c
%{_libdir}/libatf-c.so.0
%{_libdir}/libatf-c.so.0.0.0
%{_datadir}/man/man1/atf-test-program.1.gz
%{_datadir}/man/man4/atf-test-case.4.gz

%post -n libatf-c -p /sbin/ldconfig
%postun -n libatf-c -p /sbin/ldconfig


%package -n libatf-c-devel
Summary: Automated Testing Framework - C bindings (headers)
Requires: libatf-c = %{version}-%{release}

%description -n libatf-c-devel
%{common_description}

This package provides the libraries, header files and documentation to
develop tests that use the ATF C bindings.

%files -n libatf-c-devel
%{_datadir}/aclocal/atf-c.m4
%{_datadir}/aclocal/atf-common.m4
%{_includedir}/atf-c.h
%{_includedir}/atf-c
%{_libdir}/libatf-c.so
%{_libdir}/pkgconfig/atf-c.pc
%{_mandir}/man3/atf-c-api.3.gz


%package -n libatf-c++
Summary: Automated Testing Framework - C++ bindings

%description -n libatf-c++
%{common_description}

This package provides the run-time libraries to run tests that use the
ATF C++ bindings.

%files -n libatf-c++
%{_libdir}/libatf-c++.so.1
%{_libdir}/libatf-c++.so.1.0.0

%post -n libatf-c++ -p /sbin/ldconfig
%postun -n libatf-c++ -p /sbin/ldconfig


%package -n libatf-c++-devel
Summary: Automated Testing Framework - C++ bindings (headers)
Requires: libatf-c = %{version}-%{release}
Requires: libatf-c-devel = %{version}-%{release}
Requires: libatf-c++ = %{version}-%{release}

%description -n libatf-c++-devel
%{common_description}

This package provides the libraries, header files and documentation to
develop applications that use the ATF C++ bindings.

%files -n libatf-c++-devel
%{_datadir}/aclocal/atf-c++.m4
%{_includedir}/atf-c++.hpp
%{_includedir}/atf-c++
%{_libdir}/libatf-c++.so
%{_libdir}/pkgconfig/atf-c++.pc
%{_mandir}/man3/atf-c++-api.3.gz


%package -n libatf-sh
Summary: Automated Testing Framework - POSIX shell bindings
Requires: libatf-c++ = %{version}-%{release}

%description -n libatf-sh
%{common_description}

This package provides the run-time libraries to run tests that use the
ATF POSIX shell bindings.

%files -n libatf-sh
%{_bindir}/atf-sh
# Cheat a bit: While this directory should be supposedly owned by the main
# 'atf' package, 'atf' depends on libatf-sh.  Therefore, it's easier to handle
# ownership here.
%{_datadir}/atf
%{_libexecdir}/atf-check
%{_mandir}/man1/atf-sh.1.gz


%package -n libatf-sh-devel
Summary: Automated Testing Framework - POSIX shell bindings (headers)
Requires: libatf-sh = %{version}-%{release}

%description -n libatf-sh-devel
%{common_description}

This package provides the supporting files and documentation to develop
applications that use the ATF POSIX shell bindings.

%files -n libatf-sh-devel
%{_datadir}/aclocal/atf-sh.m4
%{_libdir}/pkgconfig/atf-sh.pc
%{_mandir}/man1/atf-check.1.gz
%{_mandir}/man3/atf-sh-api.3.gz
