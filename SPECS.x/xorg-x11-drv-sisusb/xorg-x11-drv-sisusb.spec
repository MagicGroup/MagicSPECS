%define tarball xf86-video-sisusb
%define moduledir %(pkg-config xorg-server --variable=moduledir )
%define driverdir	%{moduledir}/drivers

Summary:    Xorg X11 sisusb video driver
Summary(zh_CN.UTF-8): Xorg X11 sisusb 显卡驱动
Name:	    xorg-x11-drv-sisusb
Version:    0.9.6
Release:    17%{?dist}
URL:	    http://www.x.org
License:    MIT
Group:	    User Interface/X Hardware Support
Group(zh_CN.UTF-8): 用户界面/X 硬件支持

Source0:    http://ftp.nara.wide.ad.jp/pub/X11/x.org/individual/driver/%{tarball}-%{version}.tar.bz2

Patch1:	0001-Remove-mibstore.h.patch

ExcludeArch: s390 s390x %{?rhel:ppc ppc64}

BuildRequires: xorg-x11-server-devel >= 1.10.99.902
BuildRequires: autoconf automake libtool

Requires: Xorg %(xserver-sdk-abi-requires ansic)
Requires: Xorg %(xserver-sdk-abi-requires videodrv)

%description 
X.Org X11 sisusb video driver.

%description -l zh_CN.UTF-8
Xorg X11 sisusb 显卡驱动。

%prep
%setup -q -n %{tarball}-%{version}
%patch1 -p1

%build
autoreconf -vif
%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
# FIXME: This should be using makeinstall macro instead.  Please test
# makeinstall with this driver, and if it works, check it into CVS. If
# it fails, fix it in upstream sources and file a patch upstream.
make install DESTDIR=$RPM_BUILD_ROOT

# FIXME: Remove all libtool archives (*.la) from modules directory.  This
# should be fixed in upstream Makefile.am or whatever.
find $RPM_BUILD_ROOT -regex ".*.la$" | xargs rm -f --

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{driverdir}/sisusb_drv.so
%{_mandir}/man4/*.4*

%changelog
* Sun Nov 15 2015 Liu Di <liudidi@gmail.com> - 0.9.6-17
- 为 Magic 3.0 重建

* Fri Nov 06 2015 Liu Di <liudidi@gmail.com> - 0.9.6-16
- 为 Magic 3.0 重建

* Mon Oct 26 2015 Liu Di <liudidi@gmail.com> - 0.9.6-15
- 为 Magic 3.0 重建

* Mon Jan 13 2014 Adam Jackson <ajax@redhat.com> - 0.9.6-14
- 1.15 ABI rebuild

* Tue Dec 17 2013 Adam Jackson <ajax@redhat.com> - 0.9.6-13
- 1.15RC4 ABI rebuild

* Wed Nov 20 2013 Adam Jackson <ajax@redhat.com> - 0.9.6-12
- 1.15RC2 ABI rebuild

* Wed Nov 06 2013 Adam Jackson <ajax@redhat.com> - 0.9.6-11
- 1.15RC1 ABI rebuild

* Fri Oct 25 2013 Adam Jackson <ajax@redhat.com> - 0.9.6-10
- ABI rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 07 2013 Dave Airlie <airlied@redhat.com> 0.9.6-8
- autoreconf for aarch64

* Thu Mar 07 2013 Peter Hutterer <peter.hutterer@redhat.com> - 0.9.6-7
- require xorg-x11-server-devel, not -sdk

* Thu Mar 07 2013 Peter Hutterer <peter.hutterer@redhat.com> - 0.9.6-6
- ABI rebuild

* Fri Feb 15 2013 Peter Hutterer <peter.hutterer@redhat.com> - 0.9.6-5
- ABI rebuild

* Fri Feb 15 2013 Peter Hutterer <peter.hutterer@redhat.com> - 0.9.6-4
- ABI rebuild

* Thu Jan 10 2013 Adam Jackson <ajax@redhat.com> - 0.9.6-3
- ABI rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 18 2012 Dave Airlie <airlied@redhat.com> 0.9.6-1
- sisusb 0.9.6

* Thu Apr 05 2012 Adam Jackson <ajax@redhat.com> - 0.9.4-14
- RHEL arch exclude updates

* Sat Feb 11 2012 Peter Hutterer <peter.hutterer@redhat.com> - 0.9.4-13
- ABI rebuild

* Fri Feb 10 2012 Peter Hutterer <peter.hutterer@redhat.com> - 0.9.4-12
- ABI rebuild

* Tue Jan 24 2012 Peter Hutterer <peter.hutterer@redhat.com> - 0.9.4-11
- ABI rebuild

* Wed Jan 04 2012 Peter Hutterer <peter.hutterer@redhat.com> - 0.9.4-10
- Rebuild for server 1.12

* Mon Nov 14 2011 Adam Jackson <ajax@redhat.com> - 0.9.4-9
- ABI rebuild

* Thu Nov 10 2011 Adam Jackson <ajax@redhat.com> 0.9.4-8
- ABI rebuild
- sisusb-0.9.4-git.patch: Sync with git for new ABI

* Thu Aug 18 2011 Adam Jackson <ajax@redhat.com> - 0.9.4-7
- Rebuild for xserver 1.11 ABI

* Wed May 11 2011 Peter Hutterer <peter.hutterer@redhat.com> - 0.9.4-6
- Rebuild for server 1.11

* Mon Feb 28 2011 Peter Hutterer <peter.hutterer@redhat.com> - 0.9.4-5
- Rebuild for server 1.10

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 02 2010 Peter Hutterer <peter.hutterer@redhat.com> - 0.9.4-3
- Rebuild for server 1.10

* Wed Oct 27 2010 Adam Jackson <ajax@redhat.com> 0.9.4-2
- Add ABI requires magic (#542742)

* Mon Jul 05 2010 Peter Hutterer <peter.hutterer@redhat.com> 0.9.4-1
- sisusb 0.9.4

* Mon Jul 05 2010 Peter Hutterer <peter.hutterer@redhat.com> - 0.9.3-3
- rebuild for X Server 1.9

* Thu Jan 21 2010 Peter Hutterer <peter.hutterer@redhat.com> - 0.9.3-2
- Rebuild for server 1.8

* Tue Aug 04 2009 Dave Airlie <airlied@redhat.com> 0.9.3-1
- sisusb 0.9.3

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 15 2009 Adam Jackson <ajax@redhat.com> - 0.9.2-1.1
- ABI bump

* Thu Jul 02 2009 Adam Jackson <ajax@redhat.com> 0.9.2-1
- sisusb 0.9.2

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 24 2009 Adam Jackson <ajax@redhat.com> 0.9.1-1
- sisusb 0.9.1

* Thu Mar 20 2008 Dave Airlie <airlied@redhat.com> 0.9.0-1
- Latest upstream release

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.8.1-10
- Autorebuild for GCC 4.3

* Thu Sep 06 2007 Adam Jackson <ajax@redhat.com> 0.8.1-9
- Disown the manual directory. (#226622)

* Thu Aug 23 2007 Adam Jackson <ajax@redhat.com> - 0.8.1-8
- sisusb-0.8.1-open-is-not-fopen.patch: Despite the similarity, you can not
  pass character literals to open that match the string literals you'd pass
  to fopen.

* Wed Aug 22 2007 Adam Jackson <ajax@redhat.com> - 0.8.1-7
- Rebuild for PPC toolchain bug

* Mon Jun 18 2007 Adam Jackson <ajax@redhat.com> 0.8.1-6
- Update Requires and BuildRequires.  Disown the module directories.

* Fri Feb 16 2007 Adam Jackson <ajax@redhat.com> 0.8.1-5
- ExclusiveArch -> ExcludeArch

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - sh: line 0: fg: no job control
- rebuild

* Thu Jun 29 2006 Adam Jackson <ajackson@redhat.com> 0.8.1-4
- Add builds for ppc and ia64 to satisfy xorg-x11-drivers
  dependencies.  Highly untested.

* Wed Jun 28 2006 Mike A. Harris <mharris@redhat.com> 0.8.1-3
- Remove system owned directories from file manifest.

* Tue May 23 2006 Adam Jackson <ajackson@redhat.com> 0.8.1-2
- Rebuild for 7.1 ABI fix.

* Sun Apr 09 2006 Adam Jackson <ajackson@redhat.com> 0.8.1-1
- Update to 0.8.1 from 7.1RC1.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> 0.7.1.3-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> 0.7.1.3-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan 18 2006 Mike A. Harris <mharris@redhat.com> 0.7.1.3-1
- Updated xorg-x11-drv-sisusb to version 0.7.1.3 from X11R7.0
- Removed 'x' suffix from manpage dirs to match RC4 upstream.

* Tue Dec 20 2005 Mike A. Harris <mharris@redhat.com> 0.7.1.2-1
- Updated xorg-x11-drv-sisusb to version 0.7.1.2 from X11R7 RC4
- Removed 'x' suffix from manpage dirs to match RC4 upstream.

* Wed Nov 16 2005 Mike A. Harris <mharris@redhat.com> 0.7.1-1
- Updated xorg-x11-drv-sisusb to version 0.7.1 from X11R7 RC2

* Fri Nov 04 2005 Mike A. Harris <mharris@redhat.com> 0.7.0.1-1
- Updated xorg-x11-drv-sisusb to version 0.7.0.1 from X11R7 RC1
- Fix *.la file removal.

* Fri Sep 02 2005 Mike A. Harris <mharris@redhat.com> 0.7.0-0
- Initial spec file for sisusb video driver generated automatically
  by my xorg-driverspecgen script.
