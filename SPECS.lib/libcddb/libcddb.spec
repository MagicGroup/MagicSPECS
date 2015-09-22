Summary:	Library (C API) for accessing CDDB servers
Summary(zh_CN.UTF-8): 访问 CDDB 服务的库 (C API)
Name:		libcddb
Version:	1.3.2
Release:	10%{?dist}
License: 	LGPLv2+
Group: 		System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL: 		http://libcddb.sourceforge.net/
Source0: 	http://downloads.sourceforge.net/libcddb/%{name}-%{version}.tar.bz2
Patch0:		libcddb-1.3.0-multilib.patch
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)
BuildRequires:	pkgconfig, libcdio-devel >= 0.67

%description
Libcddb is a library that implements the different protocols (CDDBP,
HTTP, SMTP) to access data on a CDDB server (e.g http://freedb.org/).

%description -l zh_CN.UTF-8
这是一个实现通过不同协议 (CDDBP, HTTP, SMTP) 访问 CDDB 的库。

%package devel
Summary:	Development files for libcddb
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:	%{name} = %{version}-%{release}
Requires:	pkgconfig

%description devel
Libcddb is a library that implements the different protocols (CDDBP,
HTTP, SMTP) to access data on a CDDB server (e.g http://freedb.org/).
This package contains development files (static libraries, headers)
for libcddb.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q
%patch0 -p1
iconv -f ISO_8859-1 -t UTF-8 THANKS > THANKS.tmp
touch -r THANKS THANKS.tmp
mv THANKS.tmp THANKS
iconv -f ISO_8859-1 -t UTF-8 ChangeLog > ChangeLog.tmp
touch -r ChangeLog ChangeLog.tmp
mv ChangeLog.tmp ChangeLog


%build
%configure --disable-static
# Don't use rpath!
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS README THANKS ChangeLog TODO
%{_libdir}/libcddb.so.*
%{_bindir}/cddb_query

%files devel
%defattr(-,root,root,-)
%{_libdir}/libcddb.so
%{_includedir}/cddb
%{_libdir}/pkgconfig/libcddb.pc


%changelog
* Tue Sep 22 2015 Liu Di <liudidi@gmail.com> - 1.3.2-10
- 为 Magic 3.0 重建

* Fri Jul 11 2014 Liu Di <liudidi@gmail.com> - 1.3.2-9
- 为 Magic 3.0 重建

* Wed Apr 30 2014 Liu Di <liudidi@gmail.com> - 1.3.2-8
- 为 Magic 3.0 重建

* Tue Jan 15 2013 Liu Di <liudidi@gmail.com> - 1.3.2-7
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.3.2-6
- 为 Magic 3.0 重建

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 22 2010 Adrian Reber <adrian@lisas.de> 1.3.2-4
- Rebuilt for new libcdio

* Sun Jan 17 2010 Hans de Goede <hdegoede@redhat.com> - 1.3.2-3
- Drop static lib (#556063)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Apr  7 2009 Hans de Goede <hdegoede@redhat.com> 1.3.2-1
- New upstream release 1.3.2

* Mon Mar  9 2009 Hans de Goede <hdegoede@redhat.com> 1.3.1-1
- New upstream release 1.3.1

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan 13 2009 Adrian Reber <adrian@lisas.de> 1.3.0-6
- Rebuild for new libcdio

* Tue Feb 19 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 1.3.0-5
- Fix Source0 URL

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.3.0-4
- Autorebuild for GCC 4.3

* Sun Oct 21 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1.3.0-3
- Fix multilib conflict in version.h (bz 341971)

* Mon Aug 13 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1.3.0-2
- Update License tag for new Licensing Guidelines compliance

* Fri Oct 27 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.3.0-1
- New upstream release 1.3.0

* Sun Oct  1 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.2.2-1
- New upstream release 1.2.2

* Sun Sep 23 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.2.1-5
- Rebuild for new libcdio

* Mon Aug 28 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.2.1-4
- FE6 Rebuild

* Sun Jul 23 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.2.1-3
- Taking over as maintainer since Anvil has other priorities
- Long long due rebuild with new gcc for FC-5, it seems this may have already
  been done, since the last rebuild was of March 16 and the Rebuild Request
  bug of March 19? Rebuilding anyway to be sure (bug 185873)

* Thu Mar 16 2006 Dams <anvil[AT]livna.org> - 1.2.1-2.fc5
- Rebuild

* Tue Aug 23 2005 Dams <anvil[AT]livna.org> - 1.2.1
- Updated to 1.2.1

* Tue Jul 26 2005 Adrian Reber <adrian@lisas.de> - 1.2.0-3
- Rebuild against new libcdio (again)

* Tue Jul 26 2005 Dams <anvil[AT]livna.org> - 1.2.0-2
- Rebuild against new libcdio

* Tue Jul 26 2005 Dams <anvil[AT]livna.org> - 1.2.0-1
- Updated to 1.2.0

* Thu Jul 21 2005 Dams <anvil[AT]livna.org> - 1.1.0-1
- Updated to 1.1.0

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 1.0.2-2
- rebuild on all arches

* Wed May 11 2005 Dams <anvil[AT]livna.org> - 0:1.0.2-1.4
- Rebuilt for FC4

* Wed May 11 2005 Dams <anvil[AT]livna.org> - 0:1.0.2-1
- Added libcdio and pkgconfig buildreq
- Updated to 1.0.2
- Fixed URL in Source0

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sat Jul  3 2004 Dams <anvil[AT]livna.org> 0:0.9.4-0.fdr.2
- added missing scriptlets
- Added URL in Source0
- Added additionnal files as doc

* Tue Mar  9 2004 Dams <anvil[AT]livna.org>
- Initial build.
