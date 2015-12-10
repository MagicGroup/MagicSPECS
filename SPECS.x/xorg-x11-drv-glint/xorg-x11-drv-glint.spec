%define tarball xf86-video-glint
%define moduledir %(pkg-config xorg-server --variable=moduledir )
%define driverdir	%{moduledir}/drivers

Summary:   Xorg X11 glint video driver
Summary(zh_CN.UTF-8): Xorg X11 glint 显卡驱动
Name:      xorg-x11-drv-glint
Version:   1.2.8
Release:   16%{?dist}
URL:       http://www.x.org
License:   MIT
Group:     User Interface/X Hardware Support
Group(zh_CN.UTF-8): 用户界面/X 硬件支持

Source0:   http://ftp.nara.wide.ad.jp/pub/X11/x.org/individual/driver/%{tarball}-%{version}.tar.bz2
Patch0: 0001-Remove-mibstore.h.patch

ExcludeArch: s390 s390x %{?rhel:ppc ppc64}

BuildRequires: xorg-x11-server-devel >= 1.10.99.902
BuildRequires: autoconf automake libtool

Requires: Xorg %(xserver-sdk-abi-requires ansic)
Requires: Xorg %(xserver-sdk-abi-requires videodrv)

%description 
X.Org X11 glint video driver.

%description -l zh_CN.UTF-8
Xorg X11 glint 显卡驱动。

%prep
%setup -q -n %{tarball}-%{version}
%patch0 -p1

%build
autoreconf -vif
%configure --disable-static --disable-dri
make

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# FIXME: Remove all libtool archives (*.la) from modules directory.  This
# should be fixed in upstream Makefile.am or whatever.
find $RPM_BUILD_ROOT -regex ".*\.la$" | xargs rm -f --

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{driverdir}/glint_drv.so
%{_mandir}/man4/glint.4*

%changelog
* Sun Nov 15 2015 Liu Di <liudidi@gmail.com> - 1.2.8-16
- 为 Magic 3.0 重建

* Fri Nov 06 2015 Liu Di <liudidi@gmail.com> - 1.2.8-15
- 为 Magic 3.0 重建

* Mon Oct 26 2015 Liu Di <liudidi@gmail.com> - 1.2.8-14
- 为 Magic 3.0 重建

* Mon Jan 13 2014 Adam Jackson <ajax@redhat.com> - 1.2.8-13
- 1.15 ABI rebuild

* Tue Dec 17 2013 Adam Jackson <ajax@redhat.com> - 1.2.8-12
- 1.15RC4 ABI rebuild

* Wed Nov 20 2013 Adam Jackson <ajax@redhat.com> - 1.2.8-11
- 1.15RC2 ABI rebuild

* Wed Nov 06 2013 Adam Jackson <ajax@redhat.com> - 1.2.8-10
- 1.15RC1 ABI rebuild

* Fri Oct 25 2013 Adam Jackson <ajax@redhat.com> - 1.2.8-9
- ABI rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 07 2013 Dave Airlie <airlied@redhat.com> 1.2.8-7
- autoreconf for aarch64

* Thu Mar 07 2013 Peter Hutterer <peter.hutterer@redhat.com> - 1.2.8-6
- ABI rebuild

* Fri Feb 15 2013 Peter Hutterer <peter.hutterer@redhat.com> - 1.2.8-5
- ABI rebuild

* Fri Feb 15 2013 Peter Hutterer <peter.hutterer@redhat.com> - 1.2.8-4
- ABI rebuild

* Thu Jan 10 2013 Adam Jackson <ajax@redhat.com> - 1.2.8-3
- ABI rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 18 2012 Dave Airlie <airlied@redhat.com> 1.2.8-1
- latest upstream release 1.2.8

* Fri Apr 27 2012 Adam Jackson <ajax@redhat.com> 1.2.7-1
- glint 1.2.7

* Thu Apr 05 2012 Adam Jackson <ajax@redhat.com> - 1.2.6-9
- RHEL arch exclude updates

* Sat Feb 11 2012 Peter Hutterer <peter.hutterer@redhat.com> - 1.2.6-8
- ABI rebuild

* Fri Feb 10 2012 Peter Hutterer <peter.hutterer@redhat.com> - 1.2.6-7
- ABI rebuild

* Tue Jan 24 2012 Peter Hutterer <peter.hutterer@redhat.com> - 1.2.6-6
- ABI rebuild

* Wed Jan 04 2012 Peter Hutterer <peter.hutterer@redhat.com> - 1.2.6-5
- Rebuild for server 1.12

* Fri Dec 16 2011 Adam Jackson <ajax@redhat.com> - 1.2.6-4
- Drop xinf file

* Mon Nov 14 2011 Adam Jackson <ajax@redhat.com> - 1.2.6-3
- ABI rebuild

* Wed Nov 09 2011 ajax <ajax@redhat.com> - 1.2.6-2
- ABI rebuild

* Wed Sep 07 2011 Matěj Cepl <mcepl@redhat.com> - 1.2.6-1
- New upstream release.

* Thu Aug 18 2011 Adam Jackson <ajax@redhat.com> - 1.2.5-2
- Rebuild for xserver 1.11 ABI

* Tue Jun 21 2011 Adam Jackson <ajax@redhat.com> 1.2.5-1
- glint 1.2.5

* Wed May 11 2011 Peter Hutterer <peter.hutterer@redhat.com> - 1.2.4-8
- Rebuild for server 1.11

* Mon Feb 28 2011 Peter Hutterer <peter.hutterer@redhat.com> - 1.2.4-7
- Rebuild for server 1.10

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 02 2010 Peter Hutterer <peter.hutterer@redhat.com> - 1.2.4-5
- Rebuild for server 1.10

* Wed Oct 27 2010 Adam Jackson <ajax@redhat.com> 1.2.4-4
- Add ABI requires magic. (#542742)

* Mon Jul 05 2010 Peter Hutterer <peter.hutterer@redhat.com> - 1.2.4-3
- rebuild for X Server 1.9

* Thu Jan 21 2010 Peter Hutterer <peter.hutterer@redhat.com> - 1.2.4-2
- Rebuild for server 1.8

* Tue Aug 04 2009 Dave Airlie <airlied@redhat.com> 1.2.4-1
- glint 1.2.4

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 15 2009 Adam Jackson <ajax@redhat.com> - 1.2.3-1.1
- ABI bump

* Thu Jul 02 2009 Adam Jackson <ajax@redhat.com> 1.2.3-1
- glint 1.2.3

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 22 2008 Dave Airlie <airlied@redhat.com> 1.2.2-1
- Latest upstream release

* Thu Mar 20 2008 Dave Airlie <airlied@redhat.com> 1.2.0-1
- Latest upstream release

* Tue Mar 11 2008 Dave Airlie <airlied@gmail.com> 1.1.1-9
- pciaccess conversion

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.1.1-8
- Autorebuild for GCC 4.3

* Wed Aug 22 2007 Adam Jackson <ajax@redhat.com> - 1.1.1-7
- Rebuild for PPC toolchain bug

* Mon Jun 18 2007 Adam Jackson <ajax@redhat.com> 1.1.1-6
- Update Requires and BuildRequires.  Disown the module directories.  Add
  Requires: hwdata.

* Fri Feb 16 2007 Adam Jackson <ajax@redhat.com> 1.1.1-5
- ExclusiveArch -> ExcludeArch

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - sh: line 0: fg: no job control
- rebuild

* Fri May 26 2006 Mike A. Harris <mharris@redhat.com> 1.1.1-4
- Re-enable with_dri, as --disable-dri builds are broken (fdo#7405)

* Fri May 26 2006 Mike A. Harris <mharris@redhat.com> 1.1.1-3
- Added with_dri conditionalization, defaulted to DRI being disabled.
- Added "BuildRequires: libdrm-devel >= 2.0-1" for (#192358).
- Added "BuildRequires: mesa-libGL-devel >= 6.4-4".
- Bumped sdk dep to pick up proto-devel indirectly.

* Tue May 23 2006 Adam Jackson <ajackson@redhat.com> 1.1.1-2
- Rebuild for 7.1 ABI fix.

* Sun Apr  9 2006 Adam Jackson <ajackson@redhat.com> 1.1.1-1
- Update to 1.1.1 from 7.1RC1.

* Wed Feb 22 2006 Mike A. Harris <mharris@redhat.com> 1.0.1.3-2
- Install glint.xinf, which was inadvertently left out of packaging (#182502)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> 1.0.1.3-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan 18 2006 Mike A. Harris <mharris@redhat.com> 1.0.1.3-1
- Updated xorg-x11-drv-glint to version 1.0.1.3 from X11R7.0

* Tue Dec 20 2005 Mike A. Harris <mharris@redhat.com> 1.0.1.2-1
- Updated xorg-x11-drv-glint to version 1.0.1.2 from X11R7 RC4
- Removed 'x' suffix from manpage dirs to match RC4 upstream.

* Wed Nov 16 2005 Mike A. Harris <mharris@redhat.com> 1.0.1-1
- Updated xorg-x11-drv-glint to version 1.0.1 from X11R7 RC2

* Fri Nov 4 2005 Mike A. Harris <mharris@redhat.com> 1.0.0.1-1
- Updated xorg-x11-drv-glint to version 1.0.0.1 from X11R7 RC1
- Fix *.la file removal.

* Mon Oct 3 2005 Mike A. Harris <mharris@redhat.com> 1.0.0-1
- Update BuildRoot to use Fedora Packaging Guidelines.
- Deglob file manifest.
- Limit "ExclusiveArch" to i386, alpha

* Fri Sep 2 2005 Mike A. Harris <mharris@redhat.com> 1.0.0-0
- Initial spec file for glint video driver generated automatically
  by my xorg-driverspecgen script.
