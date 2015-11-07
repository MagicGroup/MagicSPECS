%define tarball xf86-video-mga
%define moduledir %(pkg-config xorg-server --variable=moduledir )
%define driverdir	%{moduledir}/drivers

#global gitdate 20120104
#global gitversion 9223c44a7

Summary:   Xorg X11 mga video driver
Summary(zh_CN.UTF-8): Xorg X11 mga 显卡驱动
Name:      xorg-x11-drv-mga
Version:	1.6.4
Release:	3%{?dist}
URL:       http://www.x.org
License: MIT
Group:     User Interface/X Hardware Support
Group(zh_CN.UTF-8): 用户界面/X 硬件支持

%if 0%{?gitdate}
Source0:    %{tarball}-%{gitdate}.tar.bz2
Source1:    make-git-snapshot.sh
Source2:    commitid
%else
Source0:   http://x.org/pub/individual/driver/%{tarball}-%{version}.tar.bz2
%endif

Patch0: mga-1.4.5-no-hal-advertising.patch
Patch2: mga-1.4.12-bigendian.patch
Patch4: mga-1.6.2-shadowfb.patch

ExcludeArch: s390 s390x %{?rhel:ppc ppc64}

BuildRequires: autoconf automake libtool
BuildRequires: xorg-x11-server-devel >= 1.10.99.902
BuildRequires: mesa-libGL-devel >= 6.4-4
BuildRequires: libdrm-devel >= 2.0-1

Requires: Xorg %(xserver-sdk-abi-requires ansic)
Requires: Xorg %(xserver-sdk-abi-requires videodrv)

%description 
X.Org X11 mga video driver.

%description -l zh_CN.UTF-8
Xorg X11 mga 显卡驱动。

%prep
%setup -q -n %{tarball}-%{?gitdate:%{gitdate}}%{!?gitdate:%{version}}
%patch0 -p1 -b .hal
%patch2 -p1 -b .bigendian
%patch4 -p1 -b .shadowfb

%build
autoreconf -fisv
%configure --disable-static --disable-dri
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -regex ".*\.la$" | xargs rm -f --

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{driverdir}/mga_drv.so
%{_mandir}/man4/mga.4*

%changelog
* Fri Nov 06 2015 Liu Di <liudidi@gmail.com> - 1.6.4-3
- 为 Magic 3.0 重建

* Mon Oct 26 2015 Liu Di <liudidi@gmail.com> - 1.6.4-2
- 更新到 1.6.4

* Mon Jan 13 2014 Adam Jackson <ajax@redhat.com> - 1.6.2-13
- 1.15 ABI rebuild

* Tue Dec 17 2013 Adam Jackson <ajax@redhat.com> - 1.6.2-12
- 1.15RC4 ABI rebuild

* Wed Nov 20 2013 Adam Jackson <ajax@redhat.com> - 1.6.2-11
- 1.15RC2 ABI rebuild

* Wed Nov 06 2013 Adam Jackson <ajax@redhat.com> - 1.6.2-10
- 1.15RC1 ABI rebuild

* Fri Oct 25 2013 Adam Jackson <ajax@redhat.com> - 1.6.2-9
- ABI rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon May 20 2013 Adam Jackson <ajax@redhat.com> 1.6.2-7
- mga-1.6.2-shadowfb.patch: Default to shadowfb.

* Wed Apr 03 2013 Adam Jackson <ajax@redhat.com> 1.6.2-6
- Only refuse to bind on G200 server chips. 

* Thu Mar 07 2013 Peter Hutterer <peter.hutterer@redhat.com> - 1.6.2-5
- require xorg-x11-server-devel, not -sdk

* Thu Mar 07 2013 Peter Hutterer <peter.hutterer@redhat.com> - 1.6.2-4
- ABI rebuild

* Fri Feb 15 2013 Peter Hutterer <peter.hutterer@redhat.com> - 1.6.2-3
- ABI rebuild

* Fri Feb 15 2013 Peter Hutterer <peter.hutterer@redhat.com> - 1.6.2-2
- ABI rebuild

* Wed Jan 09 2013 Adam Jackson <ajax@redhat.com> 1.6.2-1
- mga 1.6.2

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 18 2012 Dave Airlie <airlied@redhat.com> 1.6.1-1
- mga 1.6.1

* Fri May 25 2012 Dave Airlie <airlied@redhat.com> 1.5.0-1
- rebase to 1.5.0 + add don't bind to KMS driver support

* Thu Apr 05 2012 Adam Jackson <ajax@redhat.com> - 1.4.13-20.20120104git9223c44a7
- RHEL arch exclude updates

* Sat Feb 11 2012 Peter Hutterer <peter.hutterer@redhat.com> - 1.4.13-19.20120104git9223c44a7
- ABI rebuild

* Fri Feb 10 2012 Peter Hutterer <peter.hutterer@redhat.com> - 1.4.13-18.20120104git9223c44a7
- ABI rebuild

* Tue Jan 24 2012 Peter Hutterer <peter.hutterer@redhat.com> - 1.4.13-17.20120104git9223c44a7
- ABI rebuild

* Wed Jan 04 2012 Peter Hutterer <peter.hutterer@redhat.com> 1.4.13-16.20120104git9223c44a7
- git add the patch this time

* Wed Jan 04 2012 Peter Hutterer <peter.hutterer@redhat.com> 1.4.13-15.20120104git9223c44a7
- Update to git snapshot
- mga-1.4.6.1-get-client-pointer.patch: drop, file removed upstream
- add hack to build with --disable-dri
- amazingly, mga(4) now resides in man4.

* Wed Jan 04 2012 Peter Hutterer <peter.hutterer@redhat.com> - 1.4.13-14
- Rebuild for server 1.12

* Fri Dec 16 2011 Adam Jackson <ajax@redhat.com> - 1.4.13-13
- Drop xinf file

* Thu Nov 17 2011 Adam Jackson <ajax@redhat.com> 1.4.13-12
- Disable DRI1

* Mon Nov 14 2011 Adam Jackson <ajax@redhat.com> - 1.4.13-11
- ABI rebuild

* Wed Nov 09 2011 ajax <ajax@redhat.com> - 1.4.13-10
- ABI rebuild

* Thu Oct 20 2011 Adam Jackson <ajax@redhat.com> 1.4.13-9
- mga-1.4.12-bigendian.patch: Lame hack to fix color setup on big-endian
  machines. (#746410)

* Thu Aug 18 2011 Adam Jackson <ajax@redhat.com> - 1.4.13-8
- Rebuild for xserver 1.11 ABI

* Wed May 11 2011 Peter Hutterer <peter.hutterer@redhat.com> - 1.4.13-7
- Rebuild for server 1.11

* Mon Feb 28 2011 Peter Hutterer <peter.hutterer@redhat.com> - 1.4.13-6
- Rebuild for server 1.10

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.13-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 02 2010 Peter Hutterer <peter.hutterer@redhat.com> - 1.4.13-4
- Rebuild for server 1.10

* Thu Oct 28 2010 Adam Jackson <ajax@redhat.com> 1.4.13-3
- mga.xinf: updated for yet more embedded G200 variants (#576631)

* Wed Oct 27 2010 Adam Jackson <ajax@redhat.com> 1.4.13-2
- Add ABI requires magic (#542742)

* Thu Aug 12 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.4.13-1
- mga 1.4.13

* Mon Jul 05 2010 Peter Hutterer <peter.hutterer@redhat.com> - 1.4.11-3
- rebuild for X Server 1.9

* Thu Jan 21 2010 Peter Hutterer <peter.hutterer@redhat.com> - 1.4.11-2
- Rebuild for server 1.8

* Tue Aug 04 2009 Dave Airlie <airlied@redhat.com> 1.4.11-1
- mga 1.4.11

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.10-3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 15 2009 Adam Jackson <ajax@redhat.com> - 1.4.10-2.1
- ABI bump

* Tue Jun 23 2009 Dave Airlie <airlied@redhat.com> 1.4.10-2
- fixup ABI for rawhide

* Mon Apr 27 2009 Adam Jackson <ajax@redhat.com> 1.4.10-1
- mga 1.4.10

* Tue Feb 24 2009 Adam Jackson <ajax@redhat.com> 1.4.9-2
- Fix ftbfs

* Sun Feb 08 2009 Adam Jackson <ajax@redhat.com> 1.4.9-1
- mga 1.4.9

* Mon Dec 22 2008 Dave Airlie <airlied@redhat.com> 1.4.8-2
- bump for server API change

* Fri Feb 22 2008 Adam Jackson <ajax@redhat.com> 1.4.8-1
- mga 1.4.8

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.4.7-2.20080102
- Autorebuild for GCC 4.3

* Wed Jan 09 2008 Adam Jackson <ajax@redhat.com> 1.4.7-1.20080102
- Rebuild for new server ABI.

* Wed Jan 02 2008 Adam Jackson <ajax@redhat.com> 1.4.7-0.20080102
- Today's git snapshot for pciaccess goodness.
- mga-1.4.7-death-to-cfb.patch: Remove what little cfb support there was.
- mga-1.4.7-alloca.patch: Fix ALLOCATE_LOCAL references.

* Wed Aug 22 2007 Adam Jackson <ajax@redhat.com> - 1.4.6.1-6
- Rebuild for PPC toolchain bug

* Wed Jun 27 2007 Adam Jackson <ajax@redhat.com> 1.4.6.1-5
- Use %%{?_smp_mflags}.

* Mon Jun 18 2007 Adam Jackson <ajax@redhat.com> 1.4.6.1-4
- Update Requires and BuildRequires.  Add Requires: hwdata.

* Mon Feb 26 2007 Adam Jackson <ajax@redhat.com> 1.4.6.1-3
- Late-bind a call into a loadable module
- Disown the module directory

* Fri Feb 16 2007 Adam Jackson <ajax@redhat.com> 1.4.6.1-2
- ExclusiveArch -> ExcludeArch
- DRI on all arches

* Fri Jan 05 2007 Adam Jackson <ajax@redhat.com> 1.4.6.1-1
- Update to 1.4.6.1

* Mon Dec 4 2006 Adam Jackson <ajax@redhat.com> 1.4.5-2
- mga-1.4.5-no-hal-advertising.patch: Don't link to the HAL module as it's
  non-free.

* Fri Dec 1 2006 Adam Jackson <ajax@redhat.com> 1.4.5-1
- Update to 1.4.5.

* Fri Aug 18 2006 Kristian Høgsberg <krh@redhat.com> 1.4.1-5.fc6
- Add Tilman Sauerbecks patch to fix DRI locking.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> 1.4.1-4.1
- rebuild

* Thu Jul  6 2006 Adam Jackson <ajackson@redhat.com> 1.4.1-4
- mga.xinf updates.  Add G200SE cards, remove Impression and Mistral IDs
  (since they do not and never have worked), and comment each line with
  the appropriate card name.

* Fri May 26 2006 Mike A. Harris <mharris@redhat.com> 1.4.1-3
- Added with_dri conditionalization (not yet working for non-dri case).
- Added "BuildRequires: libdrm-devel >= 2.0-1" for (#192358).
- Added "BuildRequires: mesa-libGL-devel >= 6.4-4".
- Bumped sdk dep to pick up proto-devel indirectly.

* Sun Apr  9 2006 Adam Jackson <ajackson@redhat.com> 1.4.1-2
- Update to 1.4.1 from 7.1RC1.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> 1.2.1.3-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> 1.2.1.3-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan 18 2006 Mike A. Harris <mharris@redhat.com> 1.2.1.3-1
- Updated xorg-x11-drv-mga to version 1.2.1.3 from X11R7.0

* Tue Dec 20 2005 Mike A. Harris <mharris@redhat.com> 1.2.1.2-1
- Updated xorg-x11-drv-mga to version 1.2.1.2 from X11R7 RC4
- Removed 'x' suffix from manpage dirs to match RC4 upstream.

* Wed Nov 16 2005 Mike A. Harris <mharris@redhat.com> 1.2.1-1
- Updated xorg-x11-drv-mga to version 1.2.1 from X11R7 RC2

* Fri Nov 4 2005 Mike A. Harris <mharris@redhat.com> 1.2.0.1-1
- Updated xorg-x11-drv-mga to version 1.2.0.1 from X11R7 RC1
- Fix *.la file removal.
- Remove hardware specific {_bindir}/stormdwg utility.

* Mon Oct 3 2005 Mike A. Harris <mharris@redhat.com> 1.1.2-1
- Update BuildRoot to use Fedora Packaging Guidelines.
- Deglob file manifest.
- Limit "ExclusiveArch" to x86, x86_64, ia64, ppc

* Fri Sep 2 2005 Mike A. Harris <mharris@redhat.com> 1.1.2-0
- Initial spec file for mga video driver generated automatically
  by my xorg-driverspecgen script.
