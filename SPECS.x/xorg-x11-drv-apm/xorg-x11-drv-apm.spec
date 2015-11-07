%define tarball xf86-video-apm
%define moduledir %(pkg-config xorg-server --variable=moduledir )
%define driverdir %{moduledir}/drivers

Summary:   Xorg X11 apm video driver
Summary(zh_CN.UTF-8): Xorg X11 apm 显卡驱动
Name:      xorg-x11-drv-apm
Version: 1.2.5
Release: 17%{?dist}
URL:       http://www.x.org
License:   MIT
Group:     User Interface/X Hardware Support
Group(zh_CN.UTF-8): 用户界面/X 硬件支持

Source0:   http://ftp.nara.wide.ad.jp/pub/X11/x.org/individual/driver/%{tarball}-%{version}.tar.bz2
ExcludeArch: s390 s390x %{?rhel:ppc ppc64}
Patch0:	    0001-Remove-include-mibstore.h.patch

BuildRequires: xorg-x11-server-devel >= 1.10.99.902

BuildRequires: autoconf automake libtool

Requires:  Xorg %(xserver-sdk-abi-requires ansic)
Requires:  Xorg %(xserver-sdk-abi-requires videodrv)

%description 
X.Org X11 apm video driver.

%description -l zh_CN.UTF-8
Xorg X11 apm 显卡驱动。

%prep
%setup -q -n %{tarball}-%{version}
%patch0 -p1 -b .mibstore

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
%{driverdir}/apm_drv.so
%{_mandir}/man4/apm.4*

%changelog
* Fri Nov 06 2015 Liu Di <liudidi@gmail.com> - 1.2.5-17
- 为 Magic 3.0 重建

* Mon Oct 26 2015 Liu Di <liudidi@gmail.com> - 1.2.5-16
- 为 Magic 3.0 重建

* Sun Oct 25 2015 Liu Di <liudidi@gmail.com> - 1.2.5-15
- 为 Magic 3.0 重建

* Mon Jan 13 2014 Adam Jackson <ajax@redhat.com> - 1.2.5-14
- 1.15 ABI rebuild

* Tue Dec 17 2013 Adam Jackson <ajax@redhat.com> - 1.2.5-13
- 1.15RC4 ABI rebuild

* Wed Nov 20 2013 Adam Jackson <ajax@redhat.com> - 1.2.5-12
- 1.15RC2 ABI rebuild

* Wed Nov 06 2013 Adam Jackson <ajax@redhat.com> - 1.2.5-11
- 1.15RC1 ABI rebuild

* Fri Oct 25 2013 Adam Jackson <ajax@redhat.com> - 1.2.5-10
- ABI rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 07 2013 Dave Airlie <airlied@redhat.com> 1.2.5-8
- bump for autoreconf - aarch64 support

* Thu Mar 07 2013 Peter Hutterer <peter.hutterer@redhat.com> - 1.2.5-7
- require xorg-x11-server-devel, not -sdk

* Thu Mar 07 2013 Peter Hutterer <peter.hutterer@redhat.com> - 1.2.5-6
- ABI rebuild

* Fri Feb 15 2013 Peter Hutterer <peter.hutterer@redhat.com> - 1.2.5-5
- ABI rebuild

* Fri Feb 15 2013 Peter Hutterer <peter.hutterer@redhat.com> - 1.2.5-4
- ABI rebuild

* Thu Jan 10 2013 Adam Jackson <ajax@redhat.com> - 1.2.5-3
- ABI rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 17 2012 Dave Airlie <airlied@redhat.com> 1.2.5-1
- upstream 1.2.5 release

* Sat Feb 11 2012 Peter Hutterer <peter.hutterer@redhat.com> - 1.2.3-15
- ABI rebuild

* Fri Feb 10 2012 Peter Hutterer <peter.hutterer@redhat.com> - 1.2.3-14
- ABI rebuild

* Tue Jan 24 2012 Peter Hutterer <peter.hutterer@redhat.com> - 1.2.3-13
- ABI rebuild

* Wed Jan 04 2012 Peter Hutterer <peter.hutterer@redhat.com> - 1.2.3-12
- Rebuild for server 1.12

* Thu Dec 15 2011 Adam Jackson <ajax@redhat.com> 1.2.3-11
- Drop xinf file

* Wed Nov 16 2011 Adam Jackson <ajax@redhat.com> 1.2.3-10
- apm-1.2.3-git.patch: sync with git for new ABI

* Wed Nov 09 2011 Adam Jackson <ajax@redhat.com> - 1.2.3-9
- ABI rebuild

* Thu Aug 18 2011 Adam Jackson <ajax@redhat.com> - 1.2.3-8
- Rebuild for xserver 1.11 ABI

* Wed May 11 2011 Peter Hutterer <peter.hutterer@redhat.com> - 1.2.3-7
- Rebuild for server 1.11

* Mon Feb 28 2011 Peter Hutterer <peter.hutterer@redhat.com> - 1.2.3-6
- Rebuild for server 1.10

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 02 2010 Peter Hutterer <peter.hutterer@redhat.com> - 1.2.3-4
- Rebuild for server 1.10

* Wed Dec 01 2010 Adam Williamson <awilliam@redhat.com> 1.2.3-3
- rebuild for new X server

* Wed Oct 27 2010 Adam Jackson <ajax@redhat.com> 1.2.3-2
- Add ABI requires magic. (#542742)

* Sun Jul 25 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.2.3-1
- rebase to upstream release 1.2.3

* Tue Aug 04 2009 Dave Airlie <airlied@redhat.com> 1.2.2-1
- rebase to new upstream releae 1.2.2

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-4.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 15 2009 Adam Jackson <ajax@redhat.com> - 1.2.1-3.1
- ABI bump

* Mon Jun 22 2009 Adam Jackson <ajax@redhat.com> 1.2.1-3
- Fix ABI for new server

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 22 2008 Dave Airlie <airlied@redhat.com> 1.2.1-1
- upgrade to latest upstream release

* Mon Dec 22 2008 Dave Airlie <airlied@redhat.com> 1.2.0-2
- rebuild for server API change

* Thu Mar 20 2008 Dave Airlie <airlied@redhat.com> 1.2.0-1
- Upgrade to latest upstream release

* Tue Mar 11 2008 Dave Airlie <airlied@redhat.com> 1.1.1-9
- pciaccess conversion

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.1.1-8
- Autorebuild for GCC 4.3

* Wed Aug 22 2007 Adam Jackson <ajax@redhat.com> - 1.1.1-7
- Rebuild for PPC toolchain bug

* Mon Jun 18 2007 Adam Jackson <ajax@redhat.com> 1.1.1-6
- Update Requires and BuildRequires.

* Sat May 26 2007 Adam Jackson <ajax@redhat.com> 1.1.1-5
- Yet more merge review changes. (#226577)

* Thu May 24 2007 Adam Jackson <ajax@redhat.com> 1.1.1-4
- Merge review changes. (#226577)

* Thu Feb 15 2007 Adam Jackson <ajax@redhat.com> 1.1.1-3
- ExclusiveArch -> ExcludeArch

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - sh: line 0: fg: no job control
- rebuild

* Tue May 23 2006 Adam Jackson <ajackson@redhat.com> 1.1.1-2
- Rebuild for 7.1 ABI fix.

* Sun Apr  9 2006 Adam Jackson <ajackson@redhat.com> 1.1.1-1
- Update to 1.1.1 from 7.1RC1.

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.0.1.5-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan 18 2006 Mike A. Harris <mharris@redhat.com> 1.0.1.5-1
- Updated xorg-x11-drv-apm to version 1.0.1.5 from X11R7.0
- Added apm.xinf videoalias file.

* Tue Dec 20 2005 Mike A. Harris <mharris@redhat.com> 1.0.1.4-1
- Updated xorg-x11-drv-apm to version 1.0.1.4 from X11R7 RC4
- Removed 'x' suffix from manpage dirs to match RC4 upstream.

* Wed Nov 16 2005 Mike A. Harris <mharris@redhat.com> 1.0.1.2-1
- Updated xorg-x11-drv-apm to version 1.0.1.2 from X11R7 RC2

* Fri Nov 4 2005 Mike A. Harris <mharris@redhat.com> 1.0.1.1-1
- Updated xorg-x11-drv-apm to version 1.0.1.1 from X11R7 RC1
- Fix *.la file removal.

* Mon Oct 3 2005 Mike A. Harris <mharris@redhat.com> 1.0.0-1
- Set "ExclusiveArch: %%{ix86}" to match what was shipped in previous OS
  releases.

* Fri Sep 2 2005 Mike A. Harris <mharris@redhat.com> 1.0.0-0
- Initial spec file for apm video driver generated automatically
  by my xorg-driverspecgen script.
