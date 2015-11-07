%define tarball xf86-video-v4l
%define moduledir %(pkg-config xorg-server --variable=moduledir )
%define driverdir	%{moduledir}/drivers

Summary:   Xorg X11 v4l video driver
Summary(zh_CN.UTF-8): Xorg X11 v4l 显卡驱动
Name:      xorg-x11-drv-v4l
Version:   0.2.0
Release:   38%{?dist}
URL:       http://www.x.org
License:   GPLv2+
Group:     User Interface/X Hardware Support
Group(zh_CN.UTF-8): 用户界面/X 硬件支持

Source0:   http://ftp.nara.wide.ad.jp/pub/X11/x.org/individual/driver/%{tarball}-%{version}.tar.bz2
Patch0:    xorg-x11-drv-v4l-support_v4l2_only_drivers.patch

ExcludeArch: s390 s390x

BuildRequires: xorg-x11-server-devel >= 1.10.99.902
BuildRequires: autoconf automake libtool

Requires: Xorg %([ -e /usr/bin/xserver-sdk-abi-requires ] && xserver-sdk-abi-requires ansic || :)
Requires: Xorg %([ -e /usr/bin/xserver-sdk-abi-requires ] && xserver-sdk-abi-requires videodrv || :)

%description 
X.Org X11 v4l video driver.

%description -l zh_CN.UTF-8
Xorg X11 v4l 显卡驱动。

%prep
%setup -q -n %{tarball}-%{version}
%patch0 -p1

%build
autoreconf -vif
%configure --disable-static
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
%{driverdir}/v4l_drv.so
%{_mandir}/man4/v4l.4*

%changelog
* Fri Nov 06 2015 Liu Di <liudidi@gmail.com> - 0.2.0-38
- 为 Magic 3.0 重建

* Mon Oct 26 2015 Liu Di <liudidi@gmail.com> - 0.2.0-37
- 为 Magic 3.0 重建

* Mon Jan 13 2014 Adam Jackson <ajax@redhat.com> - 0.2.0-36
- 1.15 ABI rebuild

* Tue Dec 17 2013 Adam Jackson <ajax@redhat.com> - 0.2.0-35
- 1.15RC4 ABI rebuild

* Wed Nov 20 2013 Adam Jackson <ajax@redhat.com> - 0.2.0-34
- 1.15RC2 ABI rebuild

* Wed Nov 06 2013 Adam Jackson <ajax@redhat.com> - 0.2.0-33
- 1.15RC1 ABI rebuild

* Fri Oct 25 2013 Adam Jackson <ajax@redhat.com> - 0.2.0-32
- ABI rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Mar 19 2013 Adam Jackson <ajax@redhat.com> 0.2.0-30
- Less RHEL customization

* Thu Mar 07 2013 Dave Airlie <airlied@redhat.com> 0.2.0-29
- autoreconf for aarch64

* Thu Mar 07 2013 Peter Hutterer <peter.hutterer@redhat.com> - 0.2.0-28
- require xorg-x11-server-devel, not -sdk

* Thu Mar 07 2013 Peter Hutterer <peter.hutterer@redhat.com> - 0.2.0-27
- ABI rebuild

* Fri Feb 15 2013 Peter Hutterer <peter.hutterer@redhat.com> - 0.2.0-26
- ABI rebuild

* Fri Feb 15 2013 Peter Hutterer <peter.hutterer@redhat.com> - 0.2.0-25
- ABI rebuild

* Thu Jan 10 2013 Adam Jackson <ajax@redhat.com> - 0.2.0-24
- ABI rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 18 2012 Dave Airlie <airlied@redhat.com> - 0.2.0-22
- ABI rebuild

* Thu Apr 05 2012 Adam Jackson <ajax@redhat.com> - 0.2.0-21
- RHEL arch exclude updates

* Sat Feb 11 2012 Peter Hutterer <peter.hutterer@redhat.com> - 0.2.0-20
- ABI rebuild

* Fri Feb 10 2012 Peter Hutterer <peter.hutterer@redhat.com> - 0.2.0-19
- ABI rebuild

* Tue Jan 24 2012 Peter Hutterer <peter.hutterer@redhat.com> - 0.2.0-18
- ABI rebuild

* Wed Jan 04 2012 Peter Hutterer <peter.hutterer@redhat.com> - 0.2.0-17
- Rebuild for server 1.12

* Mon Nov 14 2011 Adam Jackson <ajax@redhat.com> - 0.2.0-16
- ABI rebuild

* Wed Nov 09 2011 ajax <ajax@redhat.com> - 0.2.0-15
- ABI rebuild

* Thu Aug 18 2011 Adam Jackson <ajax@redhat.com> - 0.2.0-14
- Rebuild for xserver 1.11 ABI

* Wed May 11 2011 Peter Hutterer <peter.hutterer@redhat.com> - 0.2.0-13
- Rebuild for server 1.11

* Mon Feb 28 2011 Peter Hutterer <peter.hutterer@redhat.com> - 0.2.0-12
- Rebuild for server 1.10

* Thu Feb 10 2011 Mauro Carvalho Chehab <mchehabr@redhat.com> - 0.2.0-10
- Removed the v4l1 compat layer and converted the driver to direclty use
  the v4l2 API. With this, new standards and new Port Attributes are now
  shown, reflecting what the driver is exporting.

* Wed Feb 09 2011 Adam Jackson <ajax@redhat.com> 0.2.0-10
- Fix License tag to GPLv2+ due to v4l2 patch.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Feb 03 2011 Mauro Carvalho Chehab <mchehabr@redhat.com> - 0.2.0-8
- Make it work with V4L2 drivers

* Thu Dec 02 2010 Peter Hutterer <peter.hutterer@redhat.com> - 0.2.0-7
- Rebuild for server 1.10

* Wed Oct 27 2010 Adam Jackson <ajax@redhat.com> 0.2.0-6
- Add ABI requires magic (#542742)

* Mon Jul 05 2010 Peter Hutterer <peter.hutterer@redhat.com> - 0.2.0-5.1
- rebuild for X Server 1.9

* Thu Jan 21 2010 Peter Hutterer <peter.hutterer@redhat.com> - 0.2.0-4.1
- Rebuild for server 1.8

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 15 2009 Adam Jackson <ajax@redhat.com> - 0.2.0-2.1
- ABI bump

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Mar 20 2008 Dave Airlie <airlied@redhat.com> 0.2.0-1
- Latest upstream release

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.1.1-9
- Autorebuild for GCC 4.3

* Tue Aug 28 2007 Adam Jackson <ajax@redhat.com> 0.1.1-8
- Fix ioctl argument on LP64 machines. (#250070)

* Thu Aug 23 2007 Adam Jackson <ajax@redhat.com> - 0.1.1-7
- Rebuild for ppc toolchain bug

* Mon Jun 18 2007 Adam Jackson <ajax@redhat.com> 0.1.1-6
- Update Requires and BuildRequires.  Disown the module directories.

* Fri Feb 16 2007 Adam Jackson <ajax@redhat.com> 0.1.1-5
- ExclusiveArch -> ExcludeArch

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.1.1-4
- rebuild

* Tue May 23 2006 Adam Jackson <ajackson@redhat.com> 0.1.1-3
- Rebuild for 7.1 ABI fix.

* Fri May 19 2006 Mike A. Harris <mharris@redhat.com> 0.1.1-2
- Added "BuildRequires: xorg-x11-proto-devel" for (#192386)

* Sun Apr  9 2006 Adam Jackson <ajackson@redhat.com> 0.1.1-1
- Update to 0.1.1 from 7.1RC1.

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> 0.0.1.5-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan 18 2006 Mike A. Harris <mharris@redhat.com> 0.0.1.5-1
- Updated xorg-x11-drv-v4l to version 0.0.1.5 from X11R7.0

* Tue Dec 20 2005 Mike A. Harris <mharris@redhat.com> 0.0.1.4-1
- Updated xorg-x11-drv-v4l to version 0.0.1.4 from X11R7 RC4
- Removed 'x' suffix from manpage dirs to match RC4 upstream.

* Fri Nov 4 2005 Mike A. Harris <mharris@redhat.com> 0.0.1.1-1
- Updated xorg-x11-drv-v4l to version 0.0.1.1 from X11R7 RC1.  For some
  unknown reason, the version went backwards from 4.0.0 to 0.0.1.1.
- Fix *.la file removal.

* Mon Oct 3 2005 Mike A. Harris <mharris@redhat.com> 4.0.0-1
- Initial spec file for v4l video driver forked from cirrus driver package.
