Summary: X.Org X11 ICE runtime library
Name: libICE
Version: 1.0.8
Release: 2%{?dist}
License: MIT
Group: System Environment/Libraries
URL: http://www.x.org

Source0: ftp://ftp.x.org/pub/individual/lib/%{name}-%{version}.tar.bz2

BuildRequires: pkgconfig
BuildRequires: xorg-x11-proto-devel
BuildRequires: xorg-x11-xtrans-devel >= 1.0.3-5

%description
The X.Org X11 ICE (Inter-Client Exchange) runtime library.

%package devel
Summary: X.Org X11 ICE development package
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
The X.Org X11 ICE (Inter-Client Exchange) development package.

%prep
%setup -q

%build
%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# We intentionally don't ship *.la files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog
%{_libdir}/libICE.so.6
%{_libdir}/libICE.so.6.3.0

%files devel
%defattr(-,root,root,-)
%{_docdir}/%{name}
%{_includedir}/X11/ICE
%{_libdir}/libICE.so
%{_libdir}/pkgconfig/ice.pc

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.0.8-2
- 为 Magic 3.0 重建

* Mon Mar 05 2012 Adam Jackson <ajax@redhat.com> 1.0.8-1
- libICE 1.0.8

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Adam Jackson <ajax@redhat.com> 1.0.7-1
- libICE 1.0.7

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Dec 12 2009 Robert Scheck <robert@fedoraproject.org> 1.0.6-2
- Own the /usr/include/X11/ICE directory including its content

* Fri Aug 28 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.0.6-1
- libICE 1.0.6

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 23 2009 Adam Jackson <ajax@redhat.com> 1.0.4-8
- Remove useless %%dir

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb 21 2009 Jason L Tibbitts III <tibbs@math.uh.edu> - 1.0.4-6
- Minor tweaks to summaries and descriptions.
- Don't own /usr/include/X11.
- Use a regular, unversioned dep on xorg-x11-filesystem.

* Sat Feb 21 2009 Adam Jackson <ajax@redhat.com> 1.0.4-5
- Merge review cleanups. (#226027)

* Tue Jul 15 2008 Adam Jackson <ajax@redhat.com> 1.0.4-4
- Fix license tag.

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.4-3
- Autorebuild for GCC 4.3

* Mon Oct 01 2007 Adam Jackson <ajax@redhat.com> 1.0.4-2
- Rebuild against xtrans 1.0.3-5 to pick up gethostname() avoidance.

* Mon Sep 24 2007 Adam Jackson <ajax@redhat.com> 1.0.4-1
- libICE 1.0.4

* Thu Sep 20 2007 Adam Jackson <ajax@redhat.com> 1.0.3-5
- Update xtrans dep and rebuild.

* Mon Sep 17 2007 Adam Jackson <ajax@redhat.com> 1.0.3-4
- Rebuild for abstract socket support.

* Tue Aug 21 2007 Adam Jackson <ajax@redhat.com> - 1.0.3-3
- Rebuild for build id

* Sat Apr 21 2007 Matthias Clasen <mclasen@redhat.com> 1.0.3-2
- Don't install INSTALL

* Fri Jan 05 2007 Adam Jackson <ajax@redhat.com> 1.0.3-1
- Update to 1.0.3

* Mon Nov 20 2006 Adam Jackson <ajackson@redhat.com> 1.0.2-1
- Update to 1.0.2.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> 1.0.1-2.1
- rebuild

* Mon Jun 05 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-2
- Added "Requires: xorg-x11-proto-devel"
- Replace "makeinstall" with "make install DESTDIR=..."
- Remove package ownership of mandir/libdir/etc.

* Thu Apr 27 2006 Adam Jackson <ajackson@redhat.com> 1.0.1-1
- Update to 1.0.1

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> 1.0.0-2.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> 1.0.0-2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Jan 23 2006 Mike A. Harris <mharris@redhat.com> 1.0.0-2
- Bumped and rebuilt

* Fri Dec 16 2005 Mike A. Harris <mharris@redhat.com> 1.0.0-1
- Updated libICE to version 1.0.0 from X11R7 RC4

* Tue Dec 13 2005 Mike A. Harris <mharris@redhat.com> 0.99.2-1
- Updated libICE to version 0.99.2 from X11R7 RC3
- Added "Requires(pre): xorg-x11-filesystem >= 0.99.2-3", to ensure
  that /usr/lib/X11 and /usr/include/X11 pre-exist.
- Removed 'x' suffix from manpage directories to match RC3 upstream.

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Nov 11 2005 Mike A. Harris <mharris@redhat.com> 0.99.1-1
- Updated libICE to version 0.99.1 from X11R7 RC2
- Changed 'Conflicts: XFree86-devel, xorg-x11-devel' to 'Obsoletes'
- Changed 'Conflicts: XFree86-libs, xorg-x11-libs' to 'Obsoletes'


* Mon Oct 24 2005 Mike A. Harris <mharris@redhat.com> 0.99.0-5
- Updated libICE to version 0.99.0 from X11R7 RC1

* Thu Sep 29 2005 Mike A. Harris <mharris@redhat.com> 0.99.0-4
- Added BuildRequires: pkgconfig

* Thu Sep 29 2005 Mike A. Harris <mharris@redhat.com> 0.99.0-3
- Renamed package to remove "xorg-x11" from the name due to unanimous decision
  between developers.
- Use Fedora Extras style BuildRoot tag.
- Disable static library creation by default.
- Add missing defattr to devel subpackage
- Add missing documentation files to doc macro

* Tue Aug 23 2005 Mike A. Harris <mharris@redhat.com> 0.99.0-2
- Renamed package to prepend "xorg-x11" to the name for consistency with
  the rest of the X11R7 packages.
- Added "Requires: %%{name} = %%{version}-%%{release}" dependency to devel
  subpackage to ensure the devel package matches the installed shared libs.
- Added virtual "Provides: lib<name>" and "Provides: lib<name>-devel" to
  allow applications to use implementation agnostic dependencies.
- Added post/postun scripts which call ldconfig.
- Added Conflicts with XFree86-libs and xorg-x11-libs to runtime package,
  and Conflicts with XFree86-devel and xorg-x11-devel to devel package.

* Mon Aug 22 2005 Mike A. Harris <mharris@redhat.com> 0.99.0-1
- Initial build.
