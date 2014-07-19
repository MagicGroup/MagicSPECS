Summary: Database Independent Abstraction Layer for C
Summary(zh_CN.UTF-8): C 下的数据库无关抽象层
Name: libdbi
Version: 0.9.0
Release: 6%{?dist}
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
License: LGPLv2+
URL: http://libdbi.sourceforge.net/

Source: http://prdownloads.sourceforge.net/libdbi/%{name}-%{version}.tar.gz
Patch1: libdbi-aarch64.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: autoconf openjade docbook-style-dsssl
Conflicts: libdbi-dbd-mysql < 0.8
Conflicts: libdbi-dbd-pgsql < 0.8

%description
libdbi implements a database-independent abstraction layer in C, similar to the
DBI/DBD layer in Perl. Writing one generic set of code, programmers can
leverage the power of multiple databases and multiple simultaneous database
connections by using this framework.

The libdbi package contains just the libdbi framework.  To make use of
libdbi you will also need one or more plugins from libdbi-drivers, which
contains the plugins needed to interface to specific database servers.

%description -l zh_CN.UTF-8
C 下的数据库无关抽象层，类似 Perl 下的 DBI/DBD 层。

%package devel
Summary: Development files for libdbi (Database Independent Abstraction Layer for C)
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:	%{name} = %{version}-%{release}

%description devel
The libdbi-devel package contains the header files and documentation
needed to develop applications with libdbi.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%clean 
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%prep
%setup -q -n %{name}-%{version}

%patch1 -p1

autoconf

%build
%configure

make %{?_smp_mflags}

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

rm -f ${RPM_BUILD_ROOT}%{_libdir}/libdbi.a
rm -f ${RPM_BUILD_ROOT}%{_libdir}/libdbi.la
magic_rpm_clean.sh

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc AUTHORS
%doc ChangeLog
%doc COPYING
%doc README
%{_libdir}/libdbi.so.*

%files devel
%defattr(-,root,root)
%doc TODO
%doc doc/programmers-guide.pdf
%doc doc/programmers-guide/
%doc doc/driver-guide.pdf
%doc doc/driver-guide/
%{_includedir}/dbi/
%{_libdir}/libdbi.so
%{_libdir}/pkgconfig/dbi.pc
%{_docdir}/libdbi-%{version}

%changelog
* Mon Jul 14 2014 Liu Di <liudidi@gmail.com> - 0.9.0-6
- 更新到 0.9.0

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.8.3-6
- 为 Magic 3.0 重建

* Thu Jan 05 2012 Liu Di <liudidi@gmail.com> - 0.8.3-5
- 为 Magic 3.0 重建

* Fri Sep  3 2010 Tom Lane <tgl@redhat.com> 0.8.3-4
- Do not use -ffast-math; it breaks things and seems quite unlikely to offer
  any useful performance benefit for this type of package, anyway
Resolves: #629964

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 11 2008 Tom Lane <tgl@redhat.com> 0.8.3-1
- Update to version 0.8.3.

* Tue Oct 30 2007 Tom Lane <tgl@redhat.com> 0.8.2-3
- Fix package's selection of CFLAGS to include RPM_OPT_FLAGS
Resolves: #330681

* Thu Aug  2 2007 Tom Lane <tgl@redhat.com> 0.8.2-2
- Fix typo in Release field.

* Thu Aug  2 2007 Tom Lane <tgl@redhat.com> 0.8.2-1
- Update to version 0.8.2.
- Update License tag to match code.
- Remove static library and .la file, per packaging guidelines.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.8.1-2.1
- rebuild

* Wed Jun  7 2006 Jeremy Katz <katzj@redhat.com> - 0.8.1-2
- rebuild for -devel deps

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.8.1-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.8.1-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Sat Nov 12 2005 Tom Lane <tgl@redhat.com> 0.8.1-1
- Update to version 0.8.1.

* Fri Mar 11 2005 Tom Lane <tgl@redhat.com> 0.7.2-2
- Packaging improvements per discussion with sopwith.

* Thu Mar 10 2005 Tom Lane <tgl@redhat.com> 0.7.2-1
- Import new libdbi version, splitting libdbi-drivers into a separate SRPM
  so we can track new upstream packaging.

* Sun Mar  6 2005 Tom Lane <tgl@redhat.com> 0.6.5-11
- Rebuild with gcc4.

* Mon Nov 08 2004 Tom Lane <tgl@redhat.com> 0.6.5-10
- build against mysqlclient10, not mysql, for license reasons

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Jul 03 2003 Patrick Macdonald <patrickm@redhat.com> 0.6.5-7
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Jan 24 2003 Tom Lane <tgl@redhat.com>
- /usr/include/dbi should be owned

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Sun Dec 01 2002 Elliot Lee <sopwith@redhat.com> 0.6.5-3
- multilibify

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Jun 18 2002 Trond Eivind Glomsrd <teg@redhat.com> 0.6.5-1
- 0.6.5

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Mar 13 2002 Trond Eivind Glomsrd <teg@redhat.com> 0.6.4-2
- 0.6.4

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Sep 20 2001 Trond Eivind Glomsrd <teg@redhat.com> 0.6.2-1
- Sanitize, prepare for distribution

* Sat Aug 4 2001 David Parker <david@neongoat.com>
- initial spec file created
