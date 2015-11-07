%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name: btparser
Version: 0.25
Release: 3%{?dist}
Summary: Parser and analyzer for backtraces produced by GDB
Group: Development/Libraries
License: GPLv2+
URL: http://fedorahosted.org/btparser
Source0: https://fedorahosted.org/released/btparser/btparser-%{version}.tar.xz
# remove after packaging version > 0.25
Patch0: btparser-0.25-strict-aliasing.patch
BuildRequires: glib2-devel >= 2.21
%if 0%{?suse_version}
BuildRequires: python-devel
BuildRequires: libelf-devel
Requires: libelf
%else
BuildRequires: python2-devel
BuildRequires: elfutils-devel
BuildRequires: elfutils-libelf-devel
Requires: elfutils-libs
Requires: elfutils-libelf
%endif
BuildRequires: binutils-devel
Requires: glib2 >= 2.21
Requires: binutils

%description
Btparser is a backtrace parser and analyzer, which works with
backtraces produced by the GNU Project Debugger. It can parse a text
file with a backtrace to a tree of C structures, allowing to analyze
the threads and frames of the backtrace and work with them.

Btparser also contains some backtrace manipulation and extraction
routines:
- it can find a frame in the crash-time backtrace where the program
  most likely crashed (a chance is that the function described in that
  frame is buggy)
- it can produce a duplication hash of the backtrace, which helps to
  discover that two crash-time backtraces are duplicates, triggered by
  the same flaw of the code
- it can "rate" the backtrace quality, which depends on the number of
  frames with and without the function name known (missing function
  name is caused by missing debugging symbols)

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
%configure --disable-static
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

# Remove all libtool archives (*.la) from modules directory.
find %{buildroot} -regex ".*\.la$" | xargs rm -f --

%check
make check

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc README NEWS COPYING TODO ChangeLog
%{_bindir}/btparser
%{_mandir}/man1/%{name}.1.gz
%{_libdir}/lib*.so.*

%files devel
%{_includedir}/*
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*

%files python
%dir %{python_sitearch}/%{name}
%{python_sitearch}/%{name}/*

%changelog
* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 0.25-3
- 为 Magic 3.0 重建

* Wed Mar 06 2013 Martin Milata <mmilata@redhat.com> - 0.25-2
- Fix strict aliasing warning

* Fri Feb 01 2013 Jakup Filak <jfilak@redhat.com> - 0.25-1
- New upstream release

* Wed Dec 19 2012 Jiri Moskovcak <jfilak@redhat.com> - 0.24-1
- New upstream release

* Wed Nov 14 2012 Jakub Filak <jfilak@redhat.com> - 0.23-1
- New upstream release

* Thu Nov 01 2012 Jakub Filak <jfilak@redhat.com> - 0.22-1
- New upstream release

* Wed Oct 24 2012 Jakub Filak <jfilak@redhat.com> - 0.21-1
- New upstream release

* Thu Oct 11 2012 Jakub Filak <jfilak@redhat.com> - 0.20-1
- New upstream release

* Fri Sep 21 2012 Jiri Moskovcak <jmoskovc@redhat.com> - 0.19-1
- New upstream release

* Thu Aug 02 2012 Jiri Moskovcak <jmoskovc@redhat.com> - 0.18-2
- build fixes

* Tue Jul 31 2012 Jiri Moskovcak <jmoskovc@redhat.com> - 0.18-1
- New upstream release

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Mar 19 2012 Karel Klíč <kklic@redhat.com> - 0.17-1
- New upstream release.

* Wed Feb  8 2012 Karel Klíč <kklic@redhat.com> - 0.16-1
- New upstream release

* Tue Jan  3 2012 Karel Klíč <kklic@redhat.com> - 0.15-1
- New upstream release

* Wed Nov 23 2011 Karel Klíč <kklic@redhat.com> - 0.14-1
- New upstream release

* Mon May 16 2011 Karel Klíč <kklic@redhat.com> - 0.13-1
- Initial packaging
