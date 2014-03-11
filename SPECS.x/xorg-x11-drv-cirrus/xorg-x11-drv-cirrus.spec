%define tarball xf86-video-cirrus
%define moduledir %(pkg-config xorg-server --variable=moduledir )
%define driverdir	%{moduledir}/drivers

Summary:   Xorg X11 cirrus video driver
Name:      xorg-x11-drv-cirrus
Version:   1.5.2
Release:   6%{?dist}
URL:       http://www.x.org
License:   MIT
Group:     User Interface/X Hardware Support

ExcludeArch: s390 s390x %{?rhel:ppc ppc64}

Source0:   http://ftp.nara.wide.ad.jp/pub/X11/x.org/individual/driver/%{tarball}-%{version}.tar.bz2

Patch0:	    cirrus-1.2.0-qemu.patch
Patch3:	    cirrus-1.3.2-virt-16bpp.patch

BuildRequires: xorg-x11-server-devel >= 1.10.99.902
BuildRequires: xorg-x11-util-macros >= 1.1.5
BuildRequires: autoconf automake libtool

Requires: Xorg %(xserver-sdk-abi-requires ansic)
Requires: Xorg %(xserver-sdk-abi-requires videodrv)

%description 
X.Org X11 cirrus video driver.

%prep
%setup -q -n %{tarball}-%{version}
%patch0 -p1 -b .qemu
%patch3 -p1 -b .16bpp

%build
autoreconf -vif
%configure --disable-static
make -s %{_smp_mflags}

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
%{driverdir}/cirrus_drv.so
%{driverdir}/cirrus_alpine.so
%{driverdir}/cirrus_laguna.so
%{_mandir}/man4/cirrus.4*

%changelog
* Mon Jan 13 2014 Adam Jackson <ajax@redhat.com> - 1.5.2-6
- 1.15 ABI rebuild

* Tue Dec 17 2013 Adam Jackson <ajax@redhat.com> - 1.5.2-5
- 1.15RC4 ABI rebuild

* Wed Nov 20 2013 Adam Jackson <ajax@redhat.com> - 1.5.2-4
- 1.15RC2 ABI rebuild

* Wed Nov 06 2013 Adam Jackson <ajax@redhat.com> - 1.5.2-3
- 1.15RC1 ABI rebuild

* Fri Oct 25 2013 Adam Jackson <ajax@redhat.com> - 1.5.2-2
- ABI rebuild

* Wed Aug 28 2013 Adam Jackson <ajax@redhat.com> 1.5.2-1
- cirrus 1.5.2

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 07 2013 Dave Airlie <airlied@redhat.com> 1.5.1-9
- autoreconf for aarch64

* Thu Mar 07 2013 Peter Hutterer <peter.hutterer@redhat.com> - 1.5.1-8
- require xorg-x11-server-devel, not -sdk

* Thu Mar 07 2013 Peter Hutterer <peter.hutterer@redhat.com> - 1.5.1-7
- ABI rebuild

* Fri Feb 15 2013 Peter Hutterer <peter.hutterer@redhat.com> - 1.5.1-6
- ABI rebuild

* Fri Feb 15 2013 Peter Hutterer <peter.hutterer@redhat.com> - 1.5.1-5
- ABI rebuild

* Thu Jan 10 2013 Adam Jackson <ajax@redhat.com> - 1.5.1-4
- ABI rebuild

* Mon Aug 20 2012 Dave Airlie <airlied@redhat.com> 1.5.1-3
- fix slot unclaim if cirrus loads before modeset

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 18 2012 Dave Airlie <airlied@redhat.com> 1.5.1-1
- latest upstream release

* Fri May 25 2012 Dave Airlie <airlied@redhat.com> 1.4.0-2
- don't load the cirrus driver if kms driver loaded.

* Thu Apr 26 2012 Adam Jackson <ajax@redhat.com> 1.4.0-1
- cirrus 1.4.0

* Thu Apr 05 2012 Adam Jackson <ajax@redhat.com> - 1.3.2-20
- RHEL arch exclude updates

* Mon Apr 02 2012 Adam Jackson <ajax@redhat.com> 1.3.2-19
- cirrus-1.3.2-virt-16bpp.patch: Default to 16bpp in virt

* Sat Feb 11 2012 Peter Hutterer <peter.hutterer@redhat.com> - 1.3.2-18
- ABI rebuild

* Fri Feb 10 2012 Peter Hutterer <peter.hutterer@redhat.com> - 1.3.2-17
- ABI rebuild

* Tue Jan 24 2012 Peter Hutterer <peter.hutterer@redhat.com> - 1.3.2-16
- ABI rebuild

* Wed Jan 04 2012 Peter Hutterer <peter.hutterer@redhat.com> - 1.3.2-15
- Rebuild for server 1.12

* Fri Dec 16 2011 Adam Jackson <ajax@redhat.com> - 1.3.2-14
- Drop xinf file

* Tue Nov 29 2011 Adam Jackson <ajax@redhat.com> 1.3.2-13
- cirrus-1.3.2-vgahw.patch: Adapt to new vgahw API

* Mon Nov 14 2011 Adam Jackson <ajax@redhat.com> - 1.3.2-12
- ABI rebuild

* Wed Nov 09 2011 Adam Jackson <ajax@redhat.com> 1.3.2-11
- ABI rebuild
- cirrus-1.3.2-git.patch: Sync with git for new ABI

* Thu Aug 18 2011 Adam Jackson <ajax@redhat.com> - 1.3.2-10
- Rebuild for xserver 1.11 ABI

* Wed May 11 2011 Peter Hutterer <peter.hutterer@redhat.com> - 1.3.2-9
- Rebuild for server 1.11

* Tue Apr 19 2011 Adam Jackson <ajax@redhat.com> 1.3.2-8
- cirrus-1.2.0-qemu.patch: Remove the 10x7 heuristic, since the server
  has equivalent code now.  Instead, disable "acceleration" under qemu,
  since taking the hypercall trap is really quite expensive and you're
  better off doing noaccel.

* Mon Feb 28 2011 Peter Hutterer <peter.hutterer@redhat.com> - 1.3.2-7
- Rebuild for server 1.10

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 02 2010 Peter Hutterer <peter.hutterer@redhat.com> - 1.3.2-5
- Rebuild for server 1.10

* Wed Oct 27 2010 Adam Jackson <ajax@redhat.com> 1.3.2-4
- Add ABI requires magic. (#542742)

* Mon Jul 05 2010 Peter Hutterer <peter.hutterer@redhat.com> - 1.3.2-3
- rebuild for X Server 1.9

* Thu Jan 21 2010 Peter Hutterer <peter.hutterer@redhat.com> - 1.3.2-2
- Rebuild for server 1.8

* Tue Aug 04 2009 Dave Airlie <airlied@redhat.com> 1.3.2-1
- cirrus 1.3.2

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 15 2009 Adam Jackson <ajax@redhat.com> - 1.3.1-1.1
- ABI bump

* Thu Jul 02 2009 Adam Jackson <ajax@redhat.com> 1.3.1-1
- cirrus 1.3.1

* Mon Jun 22 2009 Adam Jackson <ajax@redhat.com> 1.3.0-2
- Fix ABI for new server

* Mon May 18 2009 Adam Jackson <ajax@redhat.com> 1.3.0-1
- cirrus 1.3.0

* Fri Feb 27 2009 Adam Jackson <ajax@redhat.com> 1.2.0-6
- Fix the qemu patch to, uh, work.

* Fri Feb 27 2009 Adam Jackson <ajax@redhat.com> 1.2.0-5
- cirrus-1.2.0-qemu.patch: Detect qemu virtual video when we can, and default
  to 1024x768 in that case. (#251264)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Feb 08 2009 Adam Jackson <ajax@redhat.com> 1.2.0-3
- Re-bump, previous build didn't get the right buildroot.

* Mon Dec 22 2008 Dave Airlie <airlied@redhat.com> 1.2.0-2
- bump for server API

* Thu Mar 20 2008 Dave Airlie <airlied@redhat.com> 1.2.0-1
- Latest upstream release

* Thu Mar 13 2008 Dave Airlie <airlied@redhat.com> 1.1.0-9
- fix cirrus with no xorg.conf in qemu

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.1.0-8
- Autorebuild for GCC 4.3

* Mon Jan 21 2008 Dave Airlie <airlied@redhat.com> - 1.1.0-7
- make cirrus work with pciaccess in qemu

* Thu Jan 17 2008 Dave Airlie <airlied@redhat.com> - 1.1.0-6
- update for new server build and pciaccess

* Wed Aug 22 2007 Adam Jackson <ajax@redhat.com> - 1.1.0-5
- Rebuild for PPC toolchain bug

* Mon Jun 18 2007 Adam Jackson <ajax@redhat.com> 1.1.0-4
- Update Requires and BuildRequires.  Disown the module directories.  Add
  Requires: hwdata.

* Thu Feb 15 2007 Adam Jackson <ajax@redhat.com> 1.1.0-3
- ExclusiveArch -> ExcludeArch

* Mon Aug 21 2006 Adam Jackson <ajackson@redhat.com> 1.1.0-2.fc6
- Un-ExclusiveArch x86, as it should work everywhere and makes qemu much
  happier.  (#203373)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> 1.1.0-1.1
- rebuild

* Sun Apr  9 2006 Adam Jackson <ajackson@redhat.com> 1.1.0-1
- Update to 1.1.0 from 7.1RC1.

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.0.0.5-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan 18 2006 Mike A. Harris <mharris@redhat.com> 1.0.0.5-1
- Updated xorg-x11-drv-cirrus to version 1.0.0.5 from X11R7.0

* Tue Dec 20 2005 Mike A. Harris <mharris@redhat.com> 1.0.0.4-1
- Updated xorg-x11-drv-cirrus to version 1.0.0.4 from X11R7 RC4
- Removed 'x' suffix from manpage dirs to match RC4 upstream.
- Added cirrus_alpine.so, cirrus_laguna.so to the file manifest.

* Wed Nov 16 2005 Mike A. Harris <mharris@redhat.com> 1.0.0.2-1
- Updated xorg-x11-drv-cirrus to version 1.0.0.2 from X11R7 RC2

* Fri Nov 4 2005 Mike A. Harris <mharris@redhat.com> 1.0.0.1-1
- Updated xorg-x11-drv-cirrus to version 1.0.0.1 from X11R7 RC1
- Fix *.la file removal.

* Mon Oct 3 2005 Mike A. Harris <mharris@redhat.com> 1.0.0-1
- Update BuildRoot to use Fedora Packaging Guidelines.
- Deglob file manifest.
- Set "ExclusiveArch: %{ix86}"

* Fri Sep 2 2005 Mike A. Harris <mharris@redhat.com> 1.0.0-0
- Initial spec file for cirrus video driver generated automatically
  by my xorg-driverspecgen script.
