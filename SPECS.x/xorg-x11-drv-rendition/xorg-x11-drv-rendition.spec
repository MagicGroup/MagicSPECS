%define tarball xf86-video-rendition
%define moduledir %(pkg-config xorg-server --variable=moduledir )
%define driverdir	%{moduledir}/drivers

Summary:    Xorg X11 rendition video driver
Name:	    xorg-x11-drv-rendition
Version:    4.2.5
Release:    14%{?dist}
URL:	    http://www.x.org
License:    MIT
Group:	    User Interface/X Hardware Support

Source0:    http://ftp.nara.wide.ad.jp/pub/X11/x.org/individual/driver/%{tarball}-%{version}.tar.bz2
Patch0:	    0001-Remove-mibstore.h.patch

ExcludeArch: s390 s390x %{?rhel:ppc ppc64}

BuildRequires: xorg-x11-server-devel >= 1.10.99.902
BuildRequires: autoconf automake libtool

Requires: Xorg %(xserver-sdk-abi-requires ansic)
Requires: Xorg %(xserver-sdk-abi-requires videodrv)

%description 
X.Org X11 rendition video driver.

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

find $RPM_BUILD_ROOT -regex ".*\.la$" | xargs rm -f --

rm -f $RPM_BUILD_ROOT%{moduledir}/*.uc

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{driverdir}/rendition_drv.so
%{_mandir}/man4/rendition.4*

%changelog
* Mon Jan 13 2014 Adam Jackson <ajax@redhat.com> - 4.2.5-14
- 1.15 ABI rebuild

* Tue Dec 17 2013 Adam Jackson <ajax@redhat.com> - 4.2.5-13
- 1.15RC4 ABI rebuild

* Wed Nov 20 2013 Adam Jackson <ajax@redhat.com> - 4.2.5-12
- 1.15RC2 ABI rebuild

* Wed Nov 06 2013 Adam Jackson <ajax@redhat.com> - 4.2.5-11
- 1.15RC1 ABI rebuild

* Fri Oct 25 2013 Adam Jackson <ajax@redhat.com> - 4.2.5-10
- ABI rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 07 2013 Dave Airlie <airlied@redhat.com> 4.2.5-8
- autoreconf for aarch64

* Thu Mar 07 2013 Peter Hutterer <peter.hutterer@redhat.com> - 4.2.5-7
- require xorg-x11-server-devel, not -sdk

* Thu Mar 07 2013 Peter Hutterer <peter.hutterer@redhat.com> - 4.2.5-6
- ABI rebuild

* Fri Feb 15 2013 Peter Hutterer <peter.hutterer@redhat.com> - 4.2.5-5
- ABI rebuild

* Fri Feb 15 2013 Peter Hutterer <peter.hutterer@redhat.com> - 4.2.5-4
- ABI rebuild

* Thu Jan 10 2013 Adam Jackson <ajax@redhat.com> - 4.2.5-3
- ABI rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 18 2012 Dave Airlie <airlied@redhat.com> 4.2.5-1
- rendition 4.2.5

* Thu Apr 05 2012 Adam Jackson <ajax@redhat.com> - 4.2.4-15
- RHEL arch exclude updates

* Sat Feb 11 2012 Peter Hutterer <peter.hutterer@redhat.com> - 4.2.4-14
- ABI rebuild

* Fri Feb 10 2012 Peter Hutterer <peter.hutterer@redhat.com> - 4.2.4-13
- ABI rebuild

* Tue Jan 24 2012 Peter Hutterer <peter.hutterer@redhat.com> - 4.2.4-12
- ABI rebuild

* Wed Jan 04 2012 Peter Hutterer <peter.hutterer@redhat.com> - 4.2.4-11
- Rebuild for server 1.12

* Fri Dec 16 2011 Adam Jackson <ajax@redhat.com> - 4.2.4-10
- Drop xinf file

* Mon Nov 14 2011 Adam Jackson <ajax@redhat.com> - 4.2.4-9
- ABI rebuild

* Wed Nov 09 2011 Adam Jackson <ajax@redhat.com> 4.2.4-8
- ABI rebuild
- rendition-4.2.4-git.patch: Sync with git for new ABI

* Thu Aug 18 2011 Adam Jackson <ajax@redhat.com> - 4.2.4-7
- Rebuild for xserver 1.11 ABI

* Wed May 11 2011 Peter Hutterer <peter.hutterer@redhat.com> - 4.2.4-6
- Rebuild for server 1.11

* Mon Feb 28 2011 Peter Hutterer <peter.hutterer@redhat.com> - 4.2.4-5
- Rebuild for server 1.10

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 02 2010 Peter Hutterer <peter.hutterer@redhat.com> - 4.2.4-3
- Rebuild for server 1.10

* Wed Oct 27 2010 Adam Jackson <ajax@redhat.com> 4.2.4-2
- Add ABI requires magic (#542742)

* Mon Jul 05 2010 Dave Airlie <airlied@redhat.com> 4.2.4-1
- upstream release for server 1.9

* Mon Jul 05 2010 Peter Hutterer <peter.hutterer@redhat.com> - 4.2.2-6
- rebuild for X Server 1.9

* Thu Jan 21 2010 Peter Hutterer <peter.hutterer@redhat.com> - 4.2.2-5
- Rebuild for server 1.8

* Tue Aug 18 2009 Adam Jackson <ajax@redhat.com> 4.2.2-4
- rendition-4.2.2-abi.patch: Fix for RAC removal and etc.

* Fri Aug 07 2009 Adam Jackson <ajax@redhat.com> 4.2.2-3
- Un-ship the microcode, it doesn't actually get loaded.

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.2-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 15 2009 Adam Jackson <ajax@redhat.com> - 4.2.2-1.1
- ABI bump

* Thu Jul 02 2009 Adam Jackson <ajax@redhat.com> 4.2.2-1
- rendition 4.2.2

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 24 2009 Adam Jackson <ajax@redhat.com> 4.2.1-1
- rendition 4.2.1

* Thu Mar 20 2008 Dave Airlie <airlied@redhat.com> 4.2.0-1
- Latest upstream release

* Mon Mar 03 2008 Adam Jackson <ajax@redhat.com> 4.1.3-7.20080303
- Git snapshot for pciaccess lovin.

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 4.1.3-6
- Autorebuild for GCC 4.3

* Wed Aug 22 2007 Adam Jackson <ajax@redhat.com> - 4.1.3-5
- Rebuild for PPC toolchain bug

* Mon Jun 18 2007 Adam Jackson <ajax@redhat.com> 4.1.3-4
- Update Requires and BuildRequires.  Add Requires: hwdata.

* Tue May 08 2007 Adam Jackson <ajax@redhat.com> 4.1.3-3
- rendition.xinf: Be non-empty.  And get installed. (#208827)

* Fri Feb 16 2007 Adam Jackson <ajax@redhat.com> 4.1.3-2
- ExclusiveArch -> ExcludeArch

* Fri Jan 05 2007 Adam Jackson <ajax@redhat.com> 4.1.3-1
- Update to 4.1.3

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 4.1.0-3.1
- rebuild

* Tue Jun 27 2006 Adam Jackson <ajackson@redhat.com> 4.1.0-3
- Build on x86_64.

* Tue May 23 2006 Adam Jackson <ajackson@redhat.com> 4.1.0-2
- Rebuild for 7.1 ABI fix.

* Sun Apr 09 2006 Adam Jackson <ajackson@redhat.com> 4.1.0-1
- Update to 4.1.0 from 7.1RC1.

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> 4.0.1.3-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan 18 2006 Mike A. Harris <mharris@redhat.com> 4.0.1.3-1
- Updated xorg-x11-drv-rendition to version 4.0.1.3 from X11R7.0

* Tue Dec 20 2005 Mike A. Harris <mharris@redhat.com> 4.0.1.2-1
- Updated xorg-x11-drv-rendition to version 4.0.1.2 from X11R7 RC4
- Removed 'x' suffix from manpage dirs to match RC4 upstream.
- Remove unnecessary *.data files from moduledir.

* Wed Nov 16 2005 Mike A. Harris <mharris@redhat.com> 4.0.1-1
- Updated xorg-x11-drv-rendition to version 4.0.1 from X11R7 RC2

* Fri Nov 04 2005 Mike A. Harris <mharris@redhat.com> 4.0.0.1-1
- Updated xorg-x11-drv-rendition to version 4.0.0.1 from X11R7 RC1
- Fix *.la file removal.
- Added v10002d.uc, v20002d.uc, vgafont-std.data, vgafont-vrx.data,
  vgapalette.data to file manifest, although these really belong as C files
  in the source, that end up built into the driver.

* Mon Oct 03 2005 Mike A. Harris <mharris@redhat.com> 4.0.0-1
- Update BuildRoot to use Fedora Packaging Guidelines.
- Deglob file manifest.
- Limit "ExclusiveArch" to x86

* Fri Sep 02 2005 Mike A. Harris <mharris@redhat.com> 4.0.0-0
- Initial spec file for rendition video driver generated automatically
  by my xorg-driverspecgen script.
