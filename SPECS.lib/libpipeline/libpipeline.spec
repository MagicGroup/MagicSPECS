%global gnulib_ver 20120404-stable

Summary: A pipeline manipulation library
Name: libpipeline
Version: 1.2.2
Release: 2%{?dist}
License: GPLv3+
Group: Development/Libraries
URL: http://libpipeline.nongnu.org/
Source: http://download.savannah.gnu.org/releases/libpipeline/libpipeline-%{version}.tar.gz

# resolves: #876108
Patch: libpipeline-1.2.2-peek-offset.patch

BuildRequires: libtool, check-devel

# FPC exception for gnulib - copylib - https://fedorahosted.org/fpc/ticket/174
Provides: bundled(gnulib) = %{gnulib_ver}

%description
libpipeline is a C library for setting up and running pipelines of
processes, without needing to involve shell command-line parsing which is
often error-prone and insecure. This alleviates programmers of the need to
laboriously construct pipelines using lower-level primitives such as fork(2)
and execve(2).

%package devel
Summary: Header files and libraries for pipeline manipulation library
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: pkgconfig

%description devel
libpipeline-devel contains the header files and libraries needed
to develop programs that use libpipeline library.

%prep
%setup -q
%patch -p1 -b .peek-offset

%build
%{configure}
make %{?_smp_mflags}

%check
make check

%install
make install DESTDIR=$RPM_BUILD_ROOT prefix=%{_prefix} INSTALL='install -p'
rm $RPM_BUILD_ROOT/%{_libdir}/libpipeline.la

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc COPYING README ChangeLog NEWS
%{_libdir}/libpipeline.so.*

%files devel
%{_libdir}/libpipeline.so
%{_libdir}/pkgconfig/libpipeline.pc
%{_includedir}/*.h
%{_mandir}/man3/*

%changelog
* Fri Nov 30 2012 Peter Schiffer <pschiffe@redhat.com> - 1.2.2-2
- resolves: #876108
  fixed size_t underflow in pipeline_readline() function

* Thu Oct 18 2012 Peter Schiffer <pschiffe@redhat.com> - 1.2.2-1
- updated to 1.2.2

* Thu Sep 06 2012 Peter Schiffer <pschiffe@redhat.com> - 1.2.1-2
- enabled test suite at build time
- cleaned .spec file

* Mon Jul 23 2012 Peter Schiffer <pschiffe@redhat.com> - 1.2.1-1
- update to 1.2.1
- fixed FTBFS caused by gnulib

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Apr 19 2011 Ivana Hutarova Varekova <varekova@redhat.com> - 1.2.0-1
- initial build
