%define tarball xf86-video-vmware
%define moduledir %(pkg-config xorg-server --variable=moduledir )
%define driverdir	%{moduledir}/drivers
#define gitdate 20131207
%define gitversion a40cbd7b

%if 0%{?gitdate}
%define gver .%{gitdate}git%{gitversion}
%endif

Summary:    Xorg X11 vmware video driver
Summary(zh_CN.UTF-8): Xorg X11 vmware 显卡驱动
Name:	    xorg-x11-drv-vmware
Version:	13.1.0
Release:	2%{?dist}
URL:	    http://www.x.org
License:    MIT
Group:	    User Interface/X Hardware Support
Group(zh_CN.UTF-8): 用户界面/X 硬件支持

%if 0%{?gitdate}
Source0: %{tarball}-%{gitdate}.tar.bz2
%else
Source0:   http://ftp.nara.wide.ad.jp/pub/X11/x.org/individual/driver/%{tarball}-%{version}.tar.bz2
%endif

ExclusiveArch: %{ix86} x86_64 ia64

%if 0%{?gitdate}
BuildRequires: autoconf automake libtool
%endif
BuildRequires: xorg-x11-server-devel >= 1.10.99.902
BuildRequires: libdrm-devel pkgconfig(xext) pkgconfig(x11)
BuildRequires: mesa-libxatracker-devel >= 8.0.1-4

Requires: Xorg %(xserver-sdk-abi-requires ansic)
Requires: Xorg %(xserver-sdk-abi-requires videodrv)
Requires: libxatracker >= 8.0.1-4

%description 
X.Org X11 vmware video driver.

%description -l zh_CN.UTF-8
Xorg X11 vmware 显卡驱动。

%prep
%setup -q -n %{tarball}-%{?gitdate:%{gitdate}}%{!?gitdate:%{version}}

%build
%if 0%{?gitdate}
autoreconf -v --install || exit 1
%endif
%configure --disable-static
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
%{driverdir}/vmware_drv.so
%{_mandir}/man4/vmware.4*

%changelog
* Mon Oct 26 2015 Liu Di <liudidi@gmail.com> - 13.1.0-2
- 更新到 13.1.0

* Mon Jan 13 2014 Adam Jackson <ajax@redhat.com> - 13.0.1-9.20131207gita40cbd7b
- 1.15 ABI rebuild

* Tue Dec 17 2013 Adam Jackson <ajax@redhat.com> - 13.0.1-8.20131207gita40cbd7b
- 1.15RC4 ABI rebuild

* Sat Dec 07 2013 Dave Airlie <airlied@redhat.com> 13.0.1-7
- snapshot master to build against latest mesa

* Wed Nov 20 2013 Adam Jackson <ajax@redhat.com> - 13.0.1-6
- 1.15RC2 ABI rebuild

* Wed Nov 06 2013 Adam Jackson <ajax@redhat.com> - 13.0.1-5
- 1.15RC1 ABI rebuild

* Fri Oct 25 2013 Adam Jackson <ajax@redhat.com> - 13.0.1-4
- ABI rebuild

* Thu Oct 24 2013 Adam Jackson <ajax@redhat.com> 13.0.1-3
- xserver 1.15 API compat

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 13.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Apr 23 2013 Peter Hutterer <peter.hutterer@redhat.com> 13.0.1-1
- vmware 13.0.1

* Thu Mar 07 2013 Peter Hutterer <peter.hutterer@redhat.com> - 12.0.99.901-5.20130109gitadf375f3
- require xorg-x11-server-devel, not -sdk

* Thu Mar 07 2013 Peter Hutterer <peter.hutterer@redhat.com> - 12.0.99.901-4.20130109gitadf375f3
- ABI rebuild

* Fri Feb 15 2013 Peter Hutterer <peter.hutterer@redhat.com> - 12.0.99.901-3.20130109gitadf375f3
- ABI rebuild

* Fri Feb 15 2013 Peter Hutterer <peter.hutterer@redhat.com> - 12.0.99.901-2.20130109gitadf375f3
- ABI rebuild

* Wed Jan 09 2013 Adam Jackson <ajax@redhat.com> 12.0.99.901-1
- vmware 12.0.99.901

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12.0.2-3.20120718gite5ac80d8f
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 18 2012 Dave Airlie <airlied@redhat.com> 12.0.2-1.20120718gite5ac80d8f
- snapshot latest git for api changes

* Fri Apr 20 2012 Adam Jackson <ajax@redhat.com> 12.0.2-1
- vmware 12.0.2

* Mon Mar 19 2012 Adam Jackson <ajax@redhat.com> 12.0.1-2
- vmware-12.0.1-vgahw.patch: Fix a different crash at start (#782995)
- vmware-12.0.1-git.patch: Backport a garbage-free fix from git.

* Thu Mar 15 2012 Dave Airlie <airlied@redhat.com> 12.0.1-1
- update to latest upstream release

* Mon Mar 12 2012 Adam Jackson <ajax@redhat.com> 11.0.3-14
- vmware-11.0.3-vgahw.patch: Fix crash at start. (#801546)

* Sat Feb 11 2012 Peter Hutterer <peter.hutterer@redhat.com> - 11.0.3-13
- ABI rebuild

* Fri Feb 10 2012 Peter Hutterer <peter.hutterer@redhat.com> - 11.0.3-12
- ABI rebuild

* Tue Jan 24 2012 Peter Hutterer <peter.hutterer@redhat.com> - 11.0.3-11
- ABI rebuild

* Wed Jan 04 2012 Peter Hutterer <peter.hutterer@redhat.com> - 11.0.3-10
- Rebuild for server 1.12

* Fri Dec 16 2011 Adam Jackson <ajax@redhat.com> - 11.0.3-9
- Drop xinf file

* Wed Nov 16 2011 Adam Jackson <ajax@redhat.com> 11.0.3-8
- ABI rebuild
- vmware-11.0.3-abi12.patch: Compensate for videoabi 12.
- vmware-11.0.3-unbreak-xinerama.patch: Unbreak swapped dispatch in the
  fake-xinerama code.

* Wed Nov 09 2011 ajax <ajax@redhat.com> - 11.0.3-7
- ABI rebuild

* Thu Aug 18 2011 Adam Jackson <ajax@redhat.com> - 11.0.3-6
- Rebuild for xserver 1.11 ABI

* Wed May 11 2011 Peter Hutterer <peter.hutterer@redhat.com> - 11.0.3-5
- Rebuild for server 1.11

* Mon Feb 28 2011 Peter Hutterer <peter.hutterer@redhat.com> - 11.0.3-4
- Rebuild for server 1.10

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 11.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 02 2010 Peter Hutterer <peter.hutterer@redhat.com> - 11.0.3-2
- Rebuild for server 1.10

* Tue Nov 09 2010 Adam Jackson <ajax@redhat.com> 11.0.3-1
- vmware 11.0.3

* Wed Oct 27 2010 Adam Jackson <ajax@redhat.com> 11.0.1-2
- Add ABI requires magic (#542742)

* Tue Aug 10 2010 Dave Airlie <airlied@redhat.com> 11.0.1-1
- Latest upstream release.

* Mon Jul 05 2010 Peter Hutterer <peter.hutterer@redhat.com> - 10.16.7-4
- rebuild for X Server 1.9

* Thu Jan 21 2010 Peter Hutterer <peter.hutterer@redhat.com> - 10.16.7-3
- Rebuild for server 1.8

* Fri Aug 07 2009 Adam Jackson <ajax@redhat.com> 10.16.7-2
- fix for symbol list removal.

* Tue Aug 04 2009 Dave Airlie <airlied@redhat.com> 10.16.7-1
- vmware 10.16.7 + new abi patch

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10.16.0-5.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 15 2009 Adam Jackson <ajax@redhat.com> - 10.16.0-4.1
- ABI bump

* Tue Jun 23 2009 Dave Airlie <airlied@redhat.com> 10.16.0-4
- abi.patch: patch for new server ABI

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10.16.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Dec 24 2008 Dave Airlie <airlied@redhat.com> 10.16.0-2
- bump build for new server API

* Thu Mar 20 2008 Dave Airlie <airlied@redhat.com> 10.16.0-1
- Latest upstream release

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 10.15.2-100.1
- Autorebuild for GCC 4.3

* Tue Jan 22 2008 Adam Jackson <ajax@redhat.com> 10.15.2-99.1
- Update to git snapshot for pciaccess conversion. (#428613)

* Thu Oct 11 2007 Adam Jackson <ajax@redhat.com> 10.15.2-1
- xf86-video-vmware 10.15.2

* Mon Sep 24 2007 Adam Jackson <ajax@redhat.com> 10.15.1-1
- xf86-video-vmware 10.15.1

* Fri Aug 24 2007 Adam Jackson <ajax@redhat.com> - 10.14.1-3
- Rebuild for build ID

* Mon Jun 18 2007 Adam Jackson <ajax@redhat.com> 10.14.1-2
- Update Requires and BuildRequires.  Disown the module directories.  Add
  Requires: hwdata.

* Fri Jan 05 2007 Adam Jackson <ajax@redhat.com> 10.14.1-1.fc7
- Update to 10.14.1

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - sh: line 0: fg: no job control
- rebuild

* Tue May 23 2006 Adam Jackson <ajackson@redhat.com> 10.13.0-2
- Rebuild for 7.1 ABI fix.

* Sun Apr  9 2006 Adam Jackson <ajackson@redhat.com> 10.13.0-1
- Update to 10.13.0 from 7.1RC1.

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 10.11.1.3-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan 18 2006 Mike A. Harris <mharris@redhat.com> 10.11.1.3-1
- Updated xorg-x11-drv-vmware to version 10.11.1.3 from X11R7.0

* Tue Dec 20 2005 Mike A. Harris <mharris@redhat.com> 10.11.1.2-1
- Updated xorg-x11-drv-vmware to version 10.11.1.2 from X11R7 RC4
- Removed 'x' suffix from manpage dirs to match RC4 upstream.

* Wed Nov 16 2005 Mike A. Harris <mharris@redhat.com> 10.11.1-1
- Updated xorg-x11-drv-vmware to version 10.11.1 from X11R7 RC2

* Fri Nov 4 2005 Mike A. Harris <mharris@redhat.com> 10.11.0.1-1
- Updated xorg-x11-drv-vmware to version 10.11.0.1 from X11R7 RC1
- Fix *.la file removal.

* Tue Oct 4 2005 Mike A. Harris <mharris@redhat.com> 10.10.2-1
- Update BuildRoot to use Fedora Packaging Guidelines.
- Deglob file manifest.
- Limit "ExclusiveArch" to x86, x86_64, ia64

* Fri Sep 2 2005 Mike A. Harris <mharris@redhat.com> 10.10.2-0
- Initial spec file for vmware video driver generated automatically
  by my xorg-driverspecgen script.
