%define tarball xf86-video-trident
%define moduledir %(pkg-config xorg-server --variable=moduledir )
%define driverdir	%{moduledir}/drivers

Summary:    Xorg X11 trident video driver
Summary(zh_CN.UTF-8): Xorg X11 trident 显卡驱动
Name:       xorg-x11-drv-trident
Version:	1.3.7
Release:	4%{?dist}
URL:        http://www.x.org
License:    MIT
Group:      User Interface/X Hardware Support
Group(zh_CN.UTF-8): 用户界面/X 硬件支持

Source0:    http://ftp.nara.wide.ad.jp/pub/X11/x.org/individual/driver/%{tarball}-%{version}.tar.bz2

ExcludeArch: s390 s390x %{?rhel:ppc ppc64}

BuildRequires: xorg-x11-server-devel >= 1.10.99.902
BuildRequires: autoconf automake libtool

Requires: Xorg %(xserver-sdk-abi-requires ansic)
Requires: Xorg %(xserver-sdk-abi-requires videodrv)

%description 
X.Org X11 trident video driver.

%description -l zh_CN.UTF-8
Xorg X11 trident 显卡驱动。

%prep
%setup -q -n %{tarball}-%{version}

%build
autoreconf -vif
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
%{driverdir}/trident_drv.so
%{_mandir}/man4/trident.4*

%changelog
* Sun Nov 15 2015 Liu Di <liudidi@gmail.com> - 1.3.7-4
- 为 Magic 3.0 重建

* Fri Nov 06 2015 Liu Di <liudidi@gmail.com> - 1.3.7-3
- 为 Magic 3.0 重建

* Mon Oct 26 2015 Liu Di <liudidi@gmail.com> - 1.3.7-2
- 更新到 1.3.7

* Mon Jan 13 2014 Adam Jackson <ajax@redhat.com> - 1.3.6-14
- 1.15 ABI rebuild

* Tue Dec 17 2013 Adam Jackson <ajax@redhat.com> - 1.3.6-13
- 1.15RC4 ABI rebuild

* Wed Nov 20 2013 Adam Jackson <ajax@redhat.com> - 1.3.6-12
- 1.15RC2 ABI rebuild

* Wed Nov 06 2013 Adam Jackson <ajax@redhat.com> - 1.3.6-11
- 1.15RC1 ABI rebuild

* Fri Oct 25 2013 Adam Jackson <ajax@redhat.com> - 1.3.6-10
- ABI rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 07 2013 Dave Airlie <airlied@redhat.com> 1.3.6-8
- autoreconf for aarch64

* Thu Mar 07 2013 Peter Hutterer <peter.hutterer@redhat.com> - 1.3.6-7
- require xorg-x11-server-devel, not -sdk

* Thu Mar 07 2013 Peter Hutterer <peter.hutterer@redhat.com> - 1.3.6-6
- ABI rebuild

* Fri Feb 15 2013 Peter Hutterer <peter.hutterer@redhat.com> - 1.3.6-5
- ABI rebuild

* Fri Feb 15 2013 Peter Hutterer <peter.hutterer@redhat.com> - 1.3.6-4
- ABI rebuild

* Thu Jan 10 2013 Adam Jackson <ajax@redhat.com> - 1.3.6-3
- ABI rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 18 2012 Dave Airlie <airlied@redhat.com> 1.3.6-1
- trident 1.3.6

* Thu Apr 05 2012 Adam Jackson <ajax@redhat.com> - 1.3.4-15
- RHEL arch exclude updates

* Sat Feb 11 2012 Peter Hutterer <peter.hutterer@redhat.com> - 1.3.4-14
- ABI rebuild

* Fri Feb 10 2012 Peter Hutterer <peter.hutterer@redhat.com> - 1.3.4-13
- ABI rebuild

* Tue Jan 24 2012 Peter Hutterer <peter.hutterer@redhat.com> - 1.3.4-12
- ABI rebuild

* Wed Jan 04 2012 Peter Hutterer <peter.hutterer@redhat.com> - 1.3.4-11
- Rebuild for server 1.12

* Fri Dec 16 2011 Adam Jackson <ajax@redhat.com> - 1.3.4-10
- Drop xinf file

* Mon Nov 14 2011 Adam Jackson <ajax@redhat.com> - 1.3.4-9
- ABI rebuild

* Thu Nov 10 2011 Adam Jackson <ajax@redhat.com> 1.3.4-8
- ABI rebuild
- trident-1.3.4-git.patch: Sync with git for new ABI

* Thu Aug 18 2011 Adam Jackson <ajax@redhat.com> - 1.3.4-7
- Rebuild for xserver 1.11 ABI

* Wed May 11 2011 Peter Hutterer <peter.hutterer@redhat.com> - 1.3.4-6
- Rebuild for server 1.11

* Mon Feb 28 2011 Peter Hutterer <peter.hutterer@redhat.com> - 1.3.4-5
- Rebuild for server 1.10

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 02 2010 Peter Hutterer <peter.hutterer@redhat.com> - 1.3.4-3
- Rebuild for server 1.10

* Wed Oct 27 2010 Adam Jackson <ajax@redhat.com> 1.3.4-2
- Add ABI requires magic (#542742)

* Mon Jul 05 2010 Dave Airlie <airlied@redhat.com> 1.3.4-1
- Update to latest release for server 1.9

* Mon Jul 05 2010 Peter Hutterer <peter.hutterer@redhat.com> - 1.3.3-3
- rebuild for X Server 1.9

* Thu Jan 21 2010 Peter Hutterer <peter.hutterer@redhat.com> - 1.3.3-2
- Rebuild for server 1.8

* Wed Aug 05 2009 Dave Airlie <airlied@redhat.com> 1.3.3-1
- trident 1.3.3

* Tue Aug 04 2009 Adam Jackson <ajax@redhat.com> 1.3.2-3
- trident-1.3.2-dpms.patch: Fix for new DPMS headers

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 15 2009 Adam Jackson <ajax@redhat.com> - 1.3.2-1.1
- ABI bump

* Thu Jul 02 2009 Adam Jackson <ajax@redhat.com> 1.3.2-1
- trident 1.3.2

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 22 2008 Dave Airlie <airlied@redhat.com> 1.3.1-1
- new upstream release

* Mon Dec 22 2008 Dave Airlie <airlied@redhat.com> 1.3.0-2
- new server API

* Thu Mar 20 2008 Dave Airlie <airlied@redhat.com> 1.3.0-1
- Latest upstream release

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.2.3-8
- Autorebuild for GCC 4.3

* Mon Feb 18 2008 Dave Airlie <airlied@redhat.com> - 1.2.3-7
- pciaccess support (#433254)

* Thu Aug 23 2007 Adam Jackson <ajax@redhat.com> - 1.2.3-6
- Rebuild for ppc toolchain bug

* Mon Jun 18 2007 Adam Jackson <ajax@redhat.com> 1.2.3-5
- Update Requires and BuildRequires.  Add Requires: hwdata.

* Mon Feb 26 2007 Adam Jackson <ajax@redhat.com> 1.2.3-4
- Don't compile a dead file

* Fri Feb 16 2007 Adam Jackson <ajax@redhat.com> 1.2.3-3
- ExclusiveArch -> ExcludeArch

* Mon Jan 29 2007 Adam Jackson <ajax@redhat.com> 1.2.3-2
- Rebuild for 6 to 7 upgrade path

* Wed Jan 24 2007 Adam Jackson <ajax@redhat.com> 1.2.3-1
- Update to 1.2.3

* Tue Jul 25 2006 Mike A. Harris <mharris@redhat.com> 1.2.1-3.fc6
- Added trident-missing-symbols-bug168713.patch to fix bug (#168713)
- Remove moduledir/driverdir directory ownership (#198294)
- Added {?dist} tag to Release field.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> 1.2.1-2.1
- rebuild

* Tue May 23 2006 Adam Jackson <ajackson@redhat.com> 1.2.1-2
- Rebuild for 7.1 ABI fix.

* Sun Apr 09 2006 Adam Jackson <ajackson@redhat.com> 1.2.1-1
- Update to 1.2.1 from 7.1RC1.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> 1.0.1.2-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> 1.0.1.2-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan 18 2006 Mike A. Harris <mharris@redhat.com> 1.0.1.2-1
- Updated xorg-x11-drv-trident to version 1.0.1.2 from X11R7.0

* Tue Dec 20 2005 Mike A. Harris <mharris@redhat.com> 1.0.1.1-1
- Updated xorg-x11-drv-trident to version 1.0.1.1 from X11R7 RC4
- Removed 'x' suffix from manpage dirs to match RC4 upstream.

* Wed Nov 16 2005 Mike A. Harris <mharris@redhat.com> 1.0.0.2-1
- Updated xorg-x11-drv-trident to version 1.0.0.2 from X11R7 RC2

* Fri Nov 04 2005 Mike A. Harris <mharris@redhat.com> 1.0.0.1-1
- Updated xorg-x11-drv-trident to version 1.0.0.1 from X11R7 RC1
- Fix *.la file removal.

* Tue Oct 04 2005 Mike A. Harris <mharris@redhat.com> 1.0.0-1
- Update BuildRoot to use Fedora Packaging Guidelines.
- Deglob file manifest.
- Limit "ExclusiveArch" to x86, x86_64, ppc

* Fri Sep 02 2005 Mike A. Harris <mharris@redhat.com> 1.0.0-0
- Initial spec file for trident video driver generated automatically
  by my xorg-driverspecgen script.
