%define tarball xf86-video-sis
%define moduledir %(pkg-config xorg-server --variable=moduledir )
%define driverdir	%{moduledir}/drivers

Summary:   Xorg X11 sis video driver
Summary(zh_CN.UTF-8): Xorg X11 sis 显卡驱动
Name:      xorg-x11-drv-sis
Version:	0.10.8
Release:	2%{?dist}
URL:       http://www.x.org
License:   MIT
Group:     User Interface/X Hardware Support
Group(zh_CN.UTF-8): 用户界面/X 硬件支持

Source0:   http://ftp.nara.wide.ad.jp/pub/X11/x.org/individual/driver/%{tarball}-%{version}.tar.bz2

ExcludeArch: s390 s390x %{?rhel:ppc ppc64}

BuildRequires: xorg-x11-server-devel >= 1.10.99.902
BuildRequires: mesa-libGL-devel >= 6.4-4
BuildRequires: libdrm-devel >= 2.0-1
BuildRequires: autoconf automake libtool

Requires: Xorg %(xserver-sdk-abi-requires ansic)
Requires: Xorg %(xserver-sdk-abi-requires videodrv)

%description 
X.Org X11 sis video driver.

%description -l zh_CN.UTF-8
Xorg X11 sis 显卡驱动。

%prep
%setup -q -n %{tarball}-%{version}

%build
autoreconf -vif
%configure --disable-static --disable-dri
make %{?_smp_mflags}

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
%{driverdir}/sis_drv.so
%{_mandir}/man4/sis.4*

%changelog
* Mon Oct 26 2015 Liu Di <liudidi@gmail.com> - 0.10.8-2
- 更新到 0.10.8

* Mon Jan 13 2014 Adam Jackson <ajax@redhat.com> - 0.10.7-15
- 1.15 ABI rebuild

* Tue Dec 17 2013 Adam Jackson <ajax@redhat.com> - 0.10.7-14
- 1.15RC4 ABI rebuild

* Fri Nov 22 2013 Peter Hutterer <peter.hutterer@redhat.com> 0.10.7-13
- Fix format security warnings

* Wed Nov 20 2013 Adam Jackson <ajax@redhat.com> - 0.10.7-12
- 1.15RC2 ABI rebuild

* Wed Nov 06 2013 Adam Jackson <ajax@redhat.com> - 0.10.7-11
- 1.15RC1 ABI rebuild

* Fri Oct 25 2013 Adam Jackson <ajax@redhat.com> - 0.10.7-10
- ABI rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.7-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 07 2013 Dave Airlie <airlied@redhat.com> 0.10.7-8
- autoreconf for aarch64

* Thu Mar 07 2013 Peter Hutterer <peter.hutterer@redhat.com> - 0.10.7-7
- require xorg-x11-server-devel, not -sdk

* Thu Mar 07 2013 Peter Hutterer <peter.hutterer@redhat.com> - 0.10.7-6
- ABI rebuild

* Fri Feb 15 2013 Peter Hutterer <peter.hutterer@redhat.com> - 0.10.7-5
- ABI rebuild

* Fri Feb 15 2013 Peter Hutterer <peter.hutterer@redhat.com> - 0.10.7-4
- ABI rebuild

* Thu Jan 10 2013 Adam Jackson <ajax@redhat.com> - 0.10.7-3
- ABI rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 18 2012 Dave Airlie <airlied@redhat.com> 0.10.7-1
- sis 0.10.7

* Fri Apr 27 2012 Adam Jackson <ajax@redhat.com> 0.10.4-1
- sis 0.10.4

* Thu Apr 05 2012 Adam Jackson <ajax@redhat.com> - 0.10.3-17
- RHEL arch exclude updates

* Sat Feb 11 2012 Peter Hutterer <peter.hutterer@redhat.com> - 0.10.3-16
- ABI rebuild

* Fri Feb 10 2012 Peter Hutterer <peter.hutterer@redhat.com> - 0.10.3-15
- ABI rebuild

* Tue Jan 24 2012 Peter Hutterer <peter.hutterer@redhat.com> - 0.10.3-14
- ABI rebuild

* Wed Jan 04 2012 Peter Hutterer <peter.hutterer@redhat.com> 0.10.3-13
- Sync with latest git again
- Add a hack to replace the now-removed miPointerAbsoluteCursor
- Add a hack to allow build without DRI

* Wed Jan 04 2012 Peter Hutterer <peter.hutterer@redhat.com> - 0.10.3-12
- Rebuild for server 1.12

* Fri Dec 16 2011 Adam Jackson <ajax@redhat.com> - 0.10.3-11
- Drop xinf file

* Thu Nov 17 2011 Adam Jackson <ajax@redhat.com> 0.10.3-10
- Disable DRI1

* Mon Nov 14 2011 Adam Jackson <ajax@redhat.com> - 0.10.3-9
- ABI rebuild

* Thu Nov 10 2011 Adam Jackson <ajax@redhat.com> 0.10.3-8
- ABI rebuild
- sis-0.10.3-git.patch: Sync with git for new ABI

* Thu Aug 18 2011 Adam Jackson <ajax@redhat.com> - 0.10.3-7
- Rebuild for xserver 1.11 ABI

* Wed May 11 2011 Peter Hutterer <peter.hutterer@redhat.com> - 0.10.3-6
- Rebuild for server 1.11

* Mon Feb 28 2011 Peter Hutterer <peter.hutterer@redhat.com> - 0.10.3-5
- Rebuild for server 1.10

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 02 2010 Peter Hutterer <peter.hutterer@redhat.com> - 0.10.3-3
- Rebuild for server 1.10

* Wed Oct 27 2010 Adam Jackson <ajax@redhat.com> 0.10.3-2
- Add ABI requires magic (#542742)

* Mon Jul 05 2010 Dave Airlie <airlied@redhat.com> 0.10.3-1
- sis 0.10.3 - build for 1.9

* Mon Jul 05 2010 Peter Hutterer <peter.hutterer@redhat.com> - 0.10.2-3
- rebuild for X Server 1.9

* Thu Jan 21 2010 Peter Hutterer <peter.hutterer@redhat.com> - 0.10.2-2
- Rebuild for server 1.8

* Tue Aug 04 2009 Dave Airlie <airlied@redhat.com> 0.10.2-1
- sis 0.10.2

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.1-4.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 15 2009 Adam Jackson <ajax@redhat.com> - 0.10.1-3.1
- ABI bump

* Tue Jun 23 2009 Dave Airlie <airlied@redhat.com> 0.10.1-3
- abi.patch: fixup for new server ABI

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 22 2008 Dave Airlie <airlied@redhat.com> 0.10.1-1
- Latest upstream release

* Thu Mar 20 2008 Dave Airlie <airlied@redhat.com> 0.10.0-1
- Latest upstream release

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.9.4-4
- Autorebuild for GCC 4.3

* Thu Jan 17 2008 Dave Airlie <airlied@redhat.com> - 0.9.4-3
- fix more bugs in pciaccess port - tested on actual hardware.

* Wed Jan 16 2008 Dave Airlie <airlied@redhat.com> - 0.9.4-2
- fixup bugs in pciaccess port

* Wed Jan 16 2008 Dave Airlie <airlied@redhat.com> - 0.9.4-1
- new upstream version
- sis-pciaccess.patch - add initial pciaccess port

* Wed Aug 22 2007 Adam Jackson <ajax@redhat.com> - 0.9.3-4
- Rebuild for PPC toolchain bug

* Mon Jun 18 2007 Adam Jackson <ajax@redhat.com> 0.9.3-3
- Update Requires and BuildRequires.  Disown the module directories.  Add
  Requires: hwdata.

* Fri Feb 16 2007 Adam Jackson <ajax@redhat.com> 0.9.3-2
- ExclusiveArch -> ExcludeArch

* Fri Dec 1 2006 Adam Jackson <ajax@redhat.com> 0.9.3-1
- Update to 0.9.3

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 0.9.1-7
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Wed Sep 20 2006 Adam Jackson <ajackson@redhat.com> 0.9.1-6
- sis-0.9.1-assert.patch: Include assert.h so we don't crash.

* Thu Aug 17 2006 Bill Nottingham <notting@redhat.com> 0.9.1-5
- fix sis.xinf for XGI (case sensitive)

* Mon Jul 24 2006 Adam Jackson <ajackson@redhat.com> 0.9.1-4
- Update sis.xinf for XGI cards.  (#186024)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> 0.9.1-3.1
- rebuild

* Fri May 26 2006 Mike A. Harris <mharris@redhat.com> 0.9.1-3
- Added "BuildRequires: libdrm-devel >= 2.0-1" for (#192358)
- Bumped sdk dep to pick up proto-devel indirectly.

* Tue May 23 2006 Adam Jackson <ajackson@redhat.com> 0.9.1-2
- Rebuild for 7.1 ABI fix.

* Sun Apr  9 2006 Adam Jackson <ajackson@redhat.com> 0.9.1-1
- Update to 0.9.1 from 7.1RC1.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.8.1.3-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.8.1.3-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan 18 2006 Mike A. Harris <mharris@redhat.com> 0.8.1.3-1
- Updated xorg-x11-drv-sis to version 0.8.1.3 from X11R7.0

* Tue Dec 20 2005 Mike A. Harris <mharris@redhat.com> 0.8.1.2-1
- Updated xorg-x11-drv-sis to version 0.8.1.2 from X11R7 RC4
- Removed 'x' suffix from manpage dirs to match RC4 upstream.

* Wed Nov 16 2005 Mike A. Harris <mharris@redhat.com> 0.8.1-1
- Updated xorg-x11-drv-sis to version 0.8.1 from X11R7 RC2
- Added "BuildRequires: mesa-libGL-devel >= 6.4-4" for DRI-enabled builds.

* Fri Nov 4 2005 Mike A. Harris <mharris@redhat.com> 0.8.0.1-1
- Updated xorg-x11-drv-sis to version 0.8.0.1 from X11R7 RC1
- Fix *.la file removal.

* Tue Oct 4 2005 Mike A. Harris <mharris@redhat.com> 0.7.0-1
- Update BuildRoot to use Fedora Packaging Guidelines.
- Deglob file manifest.
- Limit "ExclusiveArch" to x86, x86_64, ppc

* Fri Sep 2 2005 Mike A. Harris <mharris@redhat.com> 0.7.0-0
- Initial spec file for sis video driver generated automatically
  by my xorg-driverspecgen script.
