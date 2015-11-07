%define tarball xf86-video-vesa
%define moduledir %(pkg-config xorg-server --variable=moduledir )
%define driverdir	%{moduledir}/drivers

Summary:   Xorg X11 vesa video driver
Summary(zh_CN.UTF-8): Xorg X11 vesa 显卡驱动
Name:      xorg-x11-drv-vesa
Version:	2.3.4
Release:	3%{?dist}
URL:       http://www.x.org
Source0:   http://xorg.freedesktop.org/releases/individual/driver/%{tarball}-%{version}.tar.bz2
License: MIT
Group:     User Interface/X Hardware Support
Group(zh_CN.UTF-8): 用户界面/X 硬件支持

Patch0:	    vesa-2.3.0-24bpp-sucks.patch
ExclusiveArch: %{ix86} x86_64 mips64el

BuildRequires: xorg-x11-server-devel >= 1.10.99.902
BuildRequires: autoconf automake libtool

Requires: Xorg %([ -e /usr/bin/xserver-sdk-abi-requires ] && xserver-sdk-abi-requires ansic)
Requires: Xorg %([ -e /usr/bin/xserver-sdk-abi-requires ] && xserver-sdk-abi-requires videodrv)

%description 
X.Org X11 vesa video driver.

%description -l zh_CN.UTF-8
Xorg X11 vesa 显卡驱动。

%prep
%setup -q -n %{tarball}-%{version}
%patch0 -p1 -b .24

%build
autoreconf -v --install || exit 1
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
%{driverdir}/vesa_drv.so
%{_mandir}/man4/vesa.4*

%changelog
* Fri Nov 06 2015 Liu Di <liudidi@gmail.com> - 2.3.4-3
- 为 Magic 3.0 重建

* Mon Oct 26 2015 Liu Di <liudidi@gmail.com> - 2.3.4-2
- 更新到 2.3.4

* Mon Jan 13 2014 Adam Jackson <ajax@redhat.com> - 2.3.2-15
- 1.15 ABI rebuild

* Tue Dec 17 2013 Adam Jackson <ajax@redhat.com> - 2.3.2-14
- 1.15RC4 ABI rebuild

* Wed Nov 20 2013 Adam Jackson <ajax@redhat.com> - 2.3.2-13
- 1.15RC2 ABI rebuild

* Wed Nov 06 2013 Adam Jackson <ajax@redhat.com> - 2.3.2-12
- 1.15RC1 ABI rebuild

* Fri Oct 25 2013 Adam Jackson <ajax@redhat.com> - 2.3.2-11
- ABI rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 07 2013 Dave Airlie <airlied@redhat.com> 2.3.2-9
- autoreconf for aarch64

* Thu Mar 07 2013 Peter Hutterer <peter.hutterer@redhat.com> - 2.3.2-8
- require xorg-x11-server-devel, not -sdk

* Thu Mar 07 2013 Peter Hutterer <peter.hutterer@redhat.com> - 2.3.2-7
- ABI rebuild

* Fri Feb 15 2013 Peter Hutterer <peter.hutterer@redhat.com> - 2.3.2-6
- ABI rebuild

* Fri Feb 15 2013 Peter Hutterer <peter.hutterer@redhat.com> - 2.3.2-5
- ABI rebuild

* Thu Jan 10 2013 Adam Jackson <ajax@redhat.com> - 2.3.2-4
- ABI rebuild

* Wed Aug 15 2012 Adam Jackson <ajax@redhat.com> 2.3.2-3
- Only build on arches where xserver builds VBE support

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 18 2012 Dave Airlie <airlied@redhat.com> 2.3.2-1
- vesa 2.3.2

* Thu Apr 26 2012 Adam Jackson <ajax@redhat.com> 2.3.1-1
- vesa 2.3.1

* Thu Apr 05 2012 Adam Jackson <ajax@redhat.com> - 2.3.0-16
- RHEL arch exclude updates

* Sat Feb 11 2012 Peter Hutterer <peter.hutterer@redhat.com> - 2.3.0-15
- ABI rebuild

* Fri Feb 10 2012 Peter Hutterer <peter.hutterer@redhat.com> - 2.3.0-14
- ABI rebuild

* Tue Jan 24 2012 Peter Hutterer <peter.hutterer@redhat.com> - 2.3.0-13
- ABI rebuild

* Wed Jan 04 2012 Peter Hutterer <peter.hutterer@redhat.com> - 2.3.0-12
- Rebuild for server 1.12

* Mon Nov 14 2011 Adam Jackson <ajax@redhat.com> - 2.3.0-11
- ABI rebuild

* Thu Nov 10 2011 Adam Jackson <ajax@redhat.com> 2.3.0-10
- vesa-2.3.0-git.patch: Sync with git for new ABI.

* Thu Aug 18 2011 Adam Jackson <ajax@redhat.com> - 2.3.0-9
- Rebuild for xserver 1.11 ABI

* Wed May 11 2011 Peter Hutterer <peter.hutterer@redhat.com> - 2.3.0-8
- Rebuild for server 1.11

* Mon Feb 28 2011 Peter Hutterer <peter.hutterer@redhat.com> - 2.3.0-7
- Rebuild for server 1.10

* Mon Feb 21 2011 Adam Jackson <ajax@redhat.com> 2.3.0-6
- vesa-2.3.0-no-virt-shadowfb.patch: Disable shadowfb on virt hardware, just
  makes things slower.
- vesa-2.3.0-kms-anathema.patch: Refuse to bind to devices with a kernel
  driver.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 02 2010 Peter Hutterer <peter.hutterer@redhat.com> - 2.3.0-4
- Rebuild for server 1.10

* Wed Oct 27 2010 Adam Jackson <ajax@redhat.com> 2.3.0-3
- Add ABI requires magic (#542742)

* Mon Oct 11 2010 Adam Jackson <ajax@redhat.com> 2.3.0-2
- vesa-2.3.0-24bpp-sucks.patch: Prefer 16bpp to 24bpp. (#533879)

* Mon Jul 05 2010 Dave Airlie <airlied@redhat.com> 2.3.0-1
- pull in latest vesa

* Mon Jul 05 2010 Peter Hutterer <peter.hutterer@redhat.com> - 2.2.1-3
- rebuild for X Server 1.9

* Thu Jan 21 2010 Peter Hutterer <peter.hutterer@redhat.com> - 2.2.1-2
- Rebuild for server 1.8

* Tue Aug 04 2009 Dave Airlie <airlied@redhat.com> 2.2.1-1
- vesa 2.2.1

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-4.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 15 2009 Adam Jackson <ajax@redhat.com> - 2.2.0-3.1
- ABI bump

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Adam Jackson <ajax@redhat.com> 2.2.0-2
- Check VBE PanelID if DDC fails.

* Tue Feb 17 2009 Adam Jackson <ajax@redhat.com> 2.2.0-1
- vesa 2.2.0

* Mon Dec 22 2008 Dave Airlie <airlied@redhat.com> 2.1.0-1
- Update to new upstream release

* Mon Dec 22 2008 Dave Airlie <airlied@redhat.com> 2.0.0-2
- bump for new server API

* Tue Jul 01 2008 Adam Jackson <ajax@redhat.com> 2.0.0-1
- vesa 2.0.0

* Tue Apr 29 2008 Adam Jackson <ajax@redhat.com> 1.3.0-15.20080404
- vesa-1.9-32bpp-dammit.patch: Prefer 24+32 instead of 24+24. (#427383)

* Fri Apr 04 2008 Adam Jackson <ajax@redhat.com> 1.3.0-14.20080404
- Today's git snapshot for FTBFS and other.  (#440720)

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.3.0-13.20071113
- Autorebuild for GCC 4.3

* Tue Jan 08 2008 Adam Jackson <ajax@redhat.com> 1.3.0-12.20071113
- Rebuild for new ABI.

* Tue Nov 13 2007 Adam Jackson <ajax@redhat.com> 1.3.0-11.20071113
- Update to git snapshot for pciaccess goodness.
- Rip out legacy framebuffer support.

* Thu Aug 23 2007 Adam Jackson <ajax@redhat.com> - 1.3.0-10
- Rebuild for ppc toolchain bug

* Mon Jun 18 2007 Adam Jackson <ajax@redhat.com> 1.3.0-9
- Update Requires and BuildRequires.

* Thu May 31 2007 Adam Jackson <ajax@redhat.com> 1.3.0-8
- vesa-1.3.0-mode-heuristics.patch: Fix a typo that would crash on
  some cards. (#241491)

* Wed May 09 2007 Adam Jackson <ajax@redhat.com> 1.3.0-6
- Re-add the sync range hack. (#235066)

* Tue Mar 20 2007 Adam Jackson <ajax@redhat.com> 1.3.0-5
- vesa-1.3.0-mode-heuristics.patch: If strict intersection of VBE and EDID
  modes leaves no modes remaining after validation, try again with just
  range and VBE checks.  Replaces earlier range-hack and validmode patches.

* Tue Feb 27 2007 Adam Jackson <ajax@redhat.com> 1.3.0-4
- vesa-1.3.0-range-hack.patch: Work around broken ATI video BIOSes.
- Disown the module dir
- Fix the License

* Fri Feb 16 2007 Adam Jackson <ajax@redhat.com> 1.3.0-3
- ExclusiveArch -> ExcludeArch

* Wed Jan 24 2007 Adam Jackson <ajax@redhat.com> 1.3.0-2
- vesa-1.2.1-validmode.patch: Strictly limit runtime modes to the intersection
  of the BIOS and DDC lists, if a DDC list exists; fixes cases where we'd
  choose 1600x1200 on 1680x1050 panel.  Conversely, be more forgiving when
  validating the resulting set against the sync ranges; fixes 640x480 syndrome
  when the monitor has broken DDC.  Don't be deceived though, vesa still sucks.

* Mon Dec 4 2006 Adam Jackson <ajax@redhat.com> 1.3.0-1
- Update to 1.3.0
- vesa-1.2.1-validmode.patch: Implement a ValidMode driver hook, which rejects
  modes not present in the BIOS or outside the capability of the monitor.

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 1.2.1-4
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Tue Sep 19 2006 Adam Jackson <ajackson@redhat.com> 1.2.1-3
- vesa-1.2.1-fix-shadowfb.patch: Fix massive performance regression relative
  to FC5.

* Fri Jul 28 2006 Adam Jackson <ajackson@redhat.com> 1.2.1-2
- vesa-1.2.1-randr-crash.patch: Fix a RANDR crash.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> 1.2.1-1.1
- rebuild

* Sat Jun 17 2006 Mike A. Harris <mharris@redhat.com> 1.2.1-1
- Updated to version 1.2.1 for X11R7.1 server.

* Tue Jun 13 2006 Adam Jackson <ajackson@redhat.com> 1.2.0-2
- Build on ppc64

* Tue May 30 2006 Adam Jackson <ajackson@redhat.com> 1.2.0-1
- Update to 1.2.0 from 7.1.

* Sun Apr 09 2006 Adam Jackson <ajackson@redhat.com> 1.1.0-1
- Update to 1.1.0 from 7.1RC1.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> 1.0.1.3-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> 1.0.1.3-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan 18 2006 Mike A. Harris <mharris@redhat.com> 1.0.1.3-1
- Updated xorg-x11-drv-vesa to version 1.0.1.3 from X11R7.0

* Tue Dec 20 2005 Mike A. Harris <mharris@redhat.com> 1.0.1.2-1
- Updated xorg-x11-drv-vesa to version 1.0.1.2 from X11R7 RC4
- Removed 'x' suffix from manpage dirs to match RC4 upstream.

* Wed Nov 16 2005 Mike A. Harris <mharris@redhat.com> 1.0.1-1
- Updated xorg-x11-drv-vesa to version 1.0.1 from X11R7 RC2

* Fri Nov 04 2005 Mike A. Harris <mharris@redhat.com> 1.0.0.1-1
- Updated xorg-x11-drv-vesa to version 1.0.0.1 from X11R7 RC1
- Fix *.la file removal.

* Tue Oct 04 2005 Mike A. Harris <mharris@redhat.com> 1.0.0-1
- Update BuildRoot to use Fedora Packaging Guidelines.
- Deglob file manifest.
- Limit "ExclusiveArch" to x86, x86_64 ia64 ppc alpha sparc sparc64

* Fri Sep 02 2005 Mike A. Harris <mharris@redhat.com> 1.0.0-0
- Initial spec file for vesa video driver generated automatically
  by my xorg-driverspecgen script.
