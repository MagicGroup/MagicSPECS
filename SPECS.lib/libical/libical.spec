Summary:	Reference implementation of the iCalendar data type and serialization format
Name:		libical
Version:	0.48
Release:	2%{?dist}
License:	LGPLv2 or MPLv1.1
Group:		System Environment/Libraries
URL:		http://freeassociation.sourceforge.net/
Source:		http://downloads.sourceforge.net/freeassociation/%{name}-%{version}.tar.gz
Requires:	tzdata
BuildRequires:	bison, byacc, flex
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Reference implementation of the iCalendar data type and serialization format
used in dozens of calendaring and scheduling products.

%package devel
Summary:	Development files for libical
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}, pkgconfig

%description devel
The libical-devel package contains libraries and header files for developing 
applications that use libical.

%prep
%setup -q

%build
%configure --disable-static --enable-reentrant --with-backtrace
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p' install

# Don't install any libtool .la files
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc LICENSE README THANKS
%{_libdir}/%{name}.so.*
%{_libdir}/libicalss.so.*
%{_libdir}/libicalvcal.so.*

%files devel
%defattr(-,root,root,-)
%doc doc/UsingLibical.txt
%{_includedir}/ical.h
%{_libdir}/%{name}.so
%{_libdir}/libicalss.so
%{_libdir}/libicalvcal.so
%{_libdir}/pkgconfig/libical.pc
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/ical*.h
%{_includedir}/%{name}/pvl.h
%{_includedir}/%{name}/sspm.h
%{_includedir}/%{name}/port.h
%{_includedir}/%{name}/vcaltmp.h
%{_includedir}/%{name}/vcc.h
%{_includedir}/%{name}/vobject.h

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.48-2
- 为 Magic 3.0 重建

* Sat Dec 17 2011 Robert Scheck <robert@fedoraproject.org> 0.48-1
- Upgrade to 0.48 (#664412, #696891, #743236)

* Mon Oct 24 2011 Robert Scheck <robert@fedoraproject.org> 0.47-1
- Upgrade to 0.47 (#743236)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.46-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Dec 19 2010 Robert Scheck <robert@fedoraproject.org> 0.46-2
- Added patch to work around upstream's broken AC_PROG_MKDIR_P

* Sun Dec 19 2010 Robert Scheck <robert@fedoraproject.org> 0.46-1
- Upgrade to 0.46 (#525933, #628893)
- Fixed race in populating builtin timezone components (#637150)
- Fixed wrong ICAL_ERRORS_ARE_FATAL preprocessor check (#575715)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.43-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Mar 15 2009 Debarshi Ray <rishi@fedoraproject.org> - 0.43-4
- Updated patch to fix #includes in the headers to work with
  'pkg-config --cflags libical'. (Red Hat Bugzilla #484091)

* Wed Feb 25 2009 Release Engineering <rel-eng@.fedoraproject.org> - 0.43-3
- Autorebuild for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 17 2009 Debarshi Ray <rishi@fedoraproject.org> - 0.43-2
- Added patch to fix CFLAGS in libical.pc. (Red Hat Bugzilla #484091)

* Tue Jan 13 2009 Debarshi Ray <rishi@fedoraproject.org> - 0.43-1
- Version bump to 0.43.
- Added patch to fix implicit pointer conversion from Debian. (Debian BTS
  #511598)
- Upstream has switched off ICAL_ERRORS_ARE_FATAL by default. This behaviour
  is being retained across all distributions, including Fedora 11.
- Added 'Requires: tzdata'.
- Enabled backtrace dumps in the syslog.

* Thu Jan 08 2009 Debarshi Ray <rishi@fedoraproject.org> - 0.41-2
- Switched off ICAL_ERRORS_ARE_FATAL for all distributions, except Fedora 11.
  (Red Hat Bugzilla #478331)

* Sun Nov 23 2008 Debarshi Ray <rishi@fedoraproject.org> - 0.41-1
- Version bump to 0.41. (Red Hat Bugzilla #469252)
- Disabled C++ bindings.

* Tue Oct 28 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0.40-1
- Version bump to 0.40. (Red Hat Bugzilla #466359)
- Add patch from upstream to fix crash in icalvalue.c.
- Update makefile patch, remove the test part (already applied).
- Package libical.pc, add Requires: pkgconfig to -devel.

* Tue Sep 03 2008 Debarshi Ray <rishi@fedoraproject.org> - 0.32-1
- Version bump to 0.32.
- Parallel build problems fixed.

* Sun Jul 27 2008 Jeff Perry <jeffperry_fedora@sourcesink.com> - 0.31-3
- Added 'BuildRequires: bison byacc flex'.

* Sun Jul 27 2008 Debarshi Ray <rishi@fedoraproject.org> - 0.31-2
- Fixed linkage problems and disabled parallel build till upstream accepts fix.

* Thu Jul 17 2008 Jeff Perry <jeffperry_fedora@sourcesink.com> - 0.31-1
- Version bump to 0.31.

* Thu Jul 17 2008 Debarshi Ray <rishi@fedoraproject.org> - 0.30-4
- Changed value of License according to Fedora licensing guidelines.
- Enabled reentrant system calls and C++ bindings.
- Omitted unused direct shared library dependencies.
- Added ChangeLog, COPYING, LICENSE, NEWS and README to doc and dropped
  examples.

* Wed Apr 02 2008 Jakub 'Livio' Rusinek <jakub.rusinek@gmail.com> - 0.30-3
- Source URL... Fixed

* Wed Apr 02 2008 Jakub 'Livio' Rusinek <jakub.rusinek@gmail.com> - 0.30-2
- Removed untrue note about libical's homepage (to get rid of eventuall mess)

* Sat Feb 23 2008 David Nielsen <gnomeuser@gmail.com> - 0.30-1
- Switch to freeassociation libical
- bump to 0.30

* Sat Feb 09 2008 Jakub 'Livio' Rusinek <jakub.rusinek@gmail.com> - 0.27-5
- Mass rebuild for new GCC... Done

* Sat Jan 19 2008 Jakub 'Livio' Rusinek <jakub.rusinek@gmail.com> - 0.27-4
- Licence... Fixed

* Fri Jan 18 2008 Jakub 'Livio' Rusinek <jakub.rusinek@gmail.com> - 0.27-3
- Files section... Fixed

* Thu Jan 17 2008 Jakub 'Livio' Rusinek <jakub.rusinek@gmail.com> - 0.27-2
- Source... Changed
- Debug information in libical main package... Excluded
- Non-numbered .so files in libical main package... Moved
- libical-devel documentation... Added

* Mon Dec 24 2007 Jakub 'Livio' Rusinek <jakub.rusinek@gmail.com> - 0.27-1
- Initial release
