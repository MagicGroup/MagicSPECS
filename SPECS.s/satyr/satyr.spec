%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

# rhel6's python-sphinx cannot build manual pages
%if 0%{?rhel} && 0%{?rhel} <= 6
  %define enable_python_manpage 0
%else
  %define enable_python_manpage 1
%endif

%if 0%{?suse_version}
  %define python2_devel python-devel
  %define libdw_devel libdw-devel
  %define libelf_devel libelf-devel
%else
  %define python2_devel python2-devel
  %define libdw_devel elfutils-devel
  %define libelf_devel elfutils-libelf-devel
%endif

Name: satyr
Version: 0.13
Release: 4%{?dist}
Summary: Tools to create anonymous, machine-friendly problem reports
Group: System Environment/Libraries
License: GPLv2+
URL: https://github.com/abrt/satyr
Source0: https://fedorahosted.org/released/abrt/satyr-%{version}.tar.xz
BuildRequires: %{python2_devel}
BuildRequires: %{libdw_devel}
BuildRequires: %{libelf_devel}
BuildRequires: binutils-devel
BuildRequires: rpm-devel
BuildRequires: libtool
BuildRequires: pkgconfig
BuildRequires: automake
BuildRequires: gcc-c++
%if %{?enable_python_manpage}
BuildRequires: python-sphinx
%endif

Patch0: satyr-0.13-elfutils-0.158.patch

%description
Satyr is a library that can be used to create and process microreports.
Microreports consist of structured data suitable to be analyzed in a fully
automated manner, though they do not necessarily contain sufficient information
to fix the underlying problem. The reports are designed not to contain any
potentially sensitive data to eliminate the need for review before submission.
Included is a tool that can create microreports and perform some basic
operations on them.

%package devel
Summary: Development libraries for %{name}
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Development libraries and headers for %{name}.

%package python
Summary: Python bindings for %{name}
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description python
Python bindings for %{name}.

%prep
%setup -q
%patch0 -p1

%build
%configure \
%if ! %{?enable_python_manpage}
        --disable-python-manpage \
%endif
        --disable-static

make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

# Remove all libtool archives (*.la) from modules directory.
find %{buildroot} -name "*.la" | xargs rm --

%check
make check

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc README NEWS COPYING
%{_bindir}/satyr
%{_mandir}/man1/%{name}.1*
%{_libdir}/libsatyr.so.3*

%files devel
%{_includedir}/satyr/
%{_libdir}/libsatyr.so
%{_libdir}/pkgconfig/satyr.pc

%files python
%dir %{python_sitearch}/%{name}
%{python_sitearch}/%{name}/*

%if %{?enable_python_manpage}
%{_mandir}/man3/satyr-python.3*
%endif

%changelog
* Tue May 27 2014 Liu Di <liudidi@gmail.com> - 0.13-4
- 为 Magic 3.0 重建

* Thu Jan 09 2014 Rex Dieter <rdieter@fedoraproject.org> 0.13-3
- track api, abi/soname in %%files, so bumps aren't a surprise

* Tue Jan 07 2014 Martin Milata <mmilata@redhat.com> 0.13-2
- Fix build against elfutils-0.158

* Tue Jan 07 2014 Martin Milata <mmilata@redhat.com> 0.13-1
- New upstream version
  - Kerneloops parser support for ppc64 and s390
  - Kerneloops hashing

* Tue Dec 10 2013 Martin Milata <mmilata@redhat.com> 0.12-1
- New upstream version
  - JVM frames normalization
  - Add C++ symbol demangling
  - Unsigned overflow bugfixes
  - Fix malformed uReports for Java

* Sat Oct 26 2013 Jakub Filak <jfilak@redhat.com> 0.11-1
- New upstream version
  - Make all python objects hashable
  - Improve memory management in rpm module
  - Extend the list of normalized functions
  - Add command for debugging duphashes to satyr utility

* Thu Oct 03 2013 Jakub Filak <jfilak@redhat.com> 0.10-1
- New upstream version
  - Fix a segmentation fault in sr_rpm_package_uniq()
  - Respect kernel flavor when parsing package name
  - Parse backtrace without Thread header
  - Fix koops json output if there are no modules
  - Add support for multiple koops stacks

* Wed Sep 11 2013 Jakub Filak <jfilak@redhat.com> 0.9-1
- New upstream version
  - Enrich koops uReport data with koops text and kernel version.
  - Improve koops modules handling.

* Wed Aug 28 2013 Richard Marko<rmarko@redhat.com> 0.8-1
- New upstream version
  - Added support for json de/serialization of reports and stacktraces.
  - Library version number increased, as the interface changed since the last release

* Mon Aug 26 2013 Martin Milata <mmilata@redhat.com> 0.7-1
- New upstream version
  - Fix couple of crashes (#997076, #994747)

* Mon Jul 29 2013 Martin Milata <mmilata@redhat.com> 0.6-1
- New upstream version
  - Do not export internal function symbols.

* Thu Jul 25 2013 Martin Milata <mmilata@redhat.com> 0.5-2
- Remove libunwind dependency altogether, always use GDB for unwinding.

* Thu Jul 25 2013 Jakub Filak <jfilak@redhat.com> 0.5-1
- Added function that creates core stacktrace from GDB output. Several bugfixes.

* Tue Jul 09 2013 Martin Milata <mmilata@redhat.com> 0.4-2
- Fix failing tests (failure manifests only on s390x)

* Mon Jul 08 2013 Martin Milata <mmilata@redhat.com> 0.4-1
- New upstream version
  - Added features needed by ABRT
  - Support for uReport2
  - Major C and Python API changes
- Patch for python-2.6 compatibility

* Tue Apr 02 2013 Dan Horák <dan[at]danny.cz> 0.3-2
- libunwind exists only on selected arches

* Mon Mar 25 2013 Martin Milata <mmilata@redhat.com> 0.3-1
- New upstream version
  - Bug fixes
  - Build fixes for older systems
- Do not require libunwind on rhel

* Mon Mar 18 2013 Martin Milata <mmilata@redhat.com> 0.2-1
- Documentation and spec cleanup
- Build fixes (build against RPM)

* Mon Aug 30 2010 Karel Klic <kklic@redhat.com> 0.1-1
- Upstream package spec file
