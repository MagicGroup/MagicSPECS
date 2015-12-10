%define tarball xf86-video-nouveau
%define moduledir %(pkg-config xorg-server --variable=moduledir )
%define driverdir %{moduledir}/drivers
#define gitdate 20120816

Summary:   Xorg X11 nouveau video driver for NVIDIA graphics chipsets
Summary(zh_CN.UTF-8): Xorg X11 NVIDIA 显卡的驱动
Name:      xorg-x11-drv-nouveau
# need to set an epoch to get version number in sync with upstream
Epoch:     1
Version:	1.0.11
Release:	4%{?dist}
URL:       http://www.x.org
License:   MIT
Group:     User Interface/X Hardware Support
Group(zh_CN.UTF-8): 用户界面/X 硬件支持

# Fedora specific snapshot no upstream release
%if 0%{?gitdate}
Source0: xf86-video-nouveau-%{gitdate}.tar.xz
%else
Source0: http://xorg.freedesktop.org/archive/individual/driver/xf86-video-nouveau-%{version}.tar.bz2
%endif
Source1: make-git-snapshot.sh

Patch0: 0001-nouveau-fix-build-on-ppc-by-wrapping-immintrin-inclu.patch
Patch1: 0002-nouveau-add-gpu-identifier-to-connector-names-for-se.patch

ExcludeArch: s390 s390x

Obsoletes: xorg-x11-drv-nv < 2.1.20-3

BuildRequires: libtool automake autoconf
BuildRequires: xorg-x11-server-devel >= 1.14.2-8
BuildRequires: libdrm-devel >= 2.4.24-0.1.20110106
BuildRequires: mesa-libGL-devel
BuildRequires: systemd-devel

Requires: Xorg %(xserver-sdk-abi-requires ansic)
Requires: Xorg %(xserver-sdk-abi-requires videodrv)
Requires:  libdrm >= 2.4.33-0.1

%description 
X.Org X11 nouveau video driver.

%description -l zh_CN.UTF-8
Xorg X11 NVIDIA 显卡的驱动。

%if 0%{?gitdate}
%define dirsuffix %{gitdate}
%else
%define dirsuffix %{version}
%endif

%prep
%setup -q -n xf86-video-nouveau-%{dirsuffix}

%build
autoreconf -v --install
%configure --disable-static

make

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -regex ".*\.la$" | xargs rm -f --

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{driverdir}/nouveau_drv.so
%{_mandir}/man4/nouveau.4*

%changelog
* Sun Nov 15 2015 Liu Di <liudidi@gmail.com> - 1:1.0.11-4
- 为 Magic 3.0 重建

* Fri Nov 06 2015 Liu Di <liudidi@gmail.com> - 1:1.0.11-3
- 为 Magic 3.0 重建

* Mon Oct 26 2015 Liu Di <liudidi@gmail.com> - 1:1.0.11-2
- 更新到 1.0.11

* Mon Jan 13 2014 Adam Jackson <ajax@redhat.com> - 1:1.0.9-7
- 1.15 ABI rebuild

* Tue Dec 17 2013 Adam Jackson <ajax@redhat.com> - 1:1.0.9-6
- 1.15RC4 ABI rebuild

* Wed Nov 20 2013 Adam Jackson <ajax@redhat.com> - 1:1.0.9-5
- 1.15RC2 ABI rebuild

* Wed Nov 06 2013 Adam Jackson <ajax@redhat.com> - 1:1.0.9-4
- 1.15RC1 ABI rebuild

* Fri Oct 25 2013 Adam Jackson <ajax@redhat.com> - 1:1.0.9-3
- ABI rebuild

* Tue Oct 22 2013 Kyle McMartin <kyle@fedoraproject.org> 1.0.9-3
- Remove artificial kernel-drm-nouveau Requires, which dates from when
  nouveau.ko was out of tree.

* Wed Jul 31 2013 Dave Airlie <airlied@redhat.com> 1.0.9-2
- fix powerpc build - fix name collisions in randr

* Tue Jul 30 2013 Dave Airlie <airlied@redhat.com> 1.0.9-1
- add upstream 1.0.9 release - fixes dual head offload + nvf0 support

* Fri Apr 12 2013 Dave Airlie <airlied@redhat.com> 1.0.7-1
- add upstream 1.0.7 release

* Tue Mar 19 2013 Adam Jackson <ajax@redhat.com> 1.0.6-7
- Less RHEL customization

* Thu Mar 07 2013 Peter Hutterer <peter.hutterer@redhat.com> - 1:1.0.6-6
- ABI rebuild

* Fri Feb 15 2013 Peter Hutterer <peter.hutterer@redhat.com> - 1:1.0.6-5
- ABI rebuild

* Fri Feb 15 2013 Peter Hutterer <peter.hutterer@redhat.com> - 1:1.0.6-4
- ABI rebuild

* Thu Jan 10 2013 Adam Jackson <ajax@redhat.com> 1.0.6-3
- Obsoletes: nv in F19 and up

* Thu Jan 10 2013 Adam Jackson <ajax@redhat.com> - 1:1.0.6-2
- ABI rebuild

* Mon Jan 07 2013 Ben Skeggs <bskeggs@redhat.com> 1.0.6-1
- nouveau 1.0.6

* Fri Nov 09 2012 Ben Skeggs <bskeggs@redhat.com> 1.0.4-1
- nouveau 1.0.4

* Thu Oct 25 2012 Dave Airlie <airlied@redhat.com> 1.0.3-1
- nouveau 1.0.3 - fix shadowfb crash

* Wed Sep 12 2012 Adam Jackson <ajax@redhat.com> 1.0.2-1
- nouveau 1.0.2

* Fri Aug 17 2012 Dave Airlie <airlied@redhat.com> 1.0.1-6
- fix dri2 tfp rendering since prime support broke it.

* Thu Aug 16 2012 Dave Airlie <airlied@redhat.com> 1.0.1-5
- upstream snapshot + prime support

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 18 2012 Dave Airlie <airlied@redhat.com> - 1:1.0.1-3
- ABI rebuild

* Mon Jul 02 2012 Karsten Hopp <karsten@redhat.com> 1.0.1-2
- we don't have vbe.h and xf86int10.h in xorg-x11-server-devel for ppc(64)

* Tue Jun 19 2012 Ben Skeggs <bskeggs@redhat.com> 1.0.1-1
- nouveau 1.0.1

* Mon Jun 18 2012 Ben Skeggs <bskeggs@redhat.com> 1.0.0-1
- nouveau 1.0.0

* Thu Jun 14 2012 Ben Skeggs <bskeggs@redhat.com> 0.0.16-39.20120426git174f170
- Drop explicit Requires on libudev

* Tue Jun 05 2012 Adam Jackson <ajax@redhat.com> 0.0.16-38.20120426git174f170
- Rebuild for new libudev
- Conditional BuildReqs for {libudev,systemd}-devel

* Thu Apr 26 2012 Dave Airlie <airlied@redhat.com> 1:0.0.16-37.20120426git174f170
- rebase to master

* Thu Apr 05 2012 Adam Jackson <ajax@redhat.com> - 1:0.0.16-36.20120306gitf5d1cd2
- RHEL arch exclude updates

* Tue Mar 06 2012 Ben Skeggs <bskeggs@redhat.com> - 1:0.0.16-35.20120306gitf5d1cd2
- pull in latest upstream code

* Sat Feb 11 2012 Peter Hutterer <peter.hutterer@redhat.com> - 1:0.0.16-34.20110720gitb806e3f
- ABI rebuild

* Fri Feb 10 2012 Peter Hutterer <peter.hutterer@redhat.com> - 1:0.0.16-33.20110720gitb806e3f
- ABI rebuild

* Tue Jan 24 2012 Peter Hutterer <peter.hutterer@redhat.com> - 1:0.0.16-32.20110720gitb806e3f
- ABI rebuild

* Tue Jan 03 2012 Peter Hutterer <peter.hutterer@redhat.com> - 1:0.0.16-31.20110720gitb806e3f
- Rebuild for server 1.12

* Fri Dec 16 2011 Adam Jackson <ajax@redhat.com> - 1:0.0.16-30.20110720gitb806e3f
- Drop xinf file

* Mon Nov 14 2011 Adam Jackson <ajax@redhat.com> - 1:0.0.16-29.20110720gitb806e3f
- ABI rebuild

* Wed Nov 09 2011 ajax <ajax@redhat.com> - 1:0.0.16-28.20110720gitb806e3f
- ABI rebuild

* Tue Aug 23 2011 Ben Skeggs <bskeggs@redhat.com> - 0.0.16-27.20110720gitb806e3f
- git snapshot, minor fixes, nothing exciting

* Thu Aug 18 2011 Adam Jackson <ajax@redhat.com> - 1:0.0.16-26.20110324git8378443
- Rebuild for xserver 1.11 ABI

* Tue May 10 2011 Peter Hutterer <peter.hutterer@redhat.com> - 0.0.16-25.20110324git8378443
- Rebuild for what will be server 1.11 one day

* Wed Mar 23 2011 Ben Skeggs <bskeggs@redhat.com> - 0.0.16-24.20110324git8378443
- nv50-nvc0/exa: fix bug exposed by 2.6.38 kernel

* Thu Mar 10 2011 Adam Jackson <ajax@redhat.com> - 1:0.0.16-23.20110303git92db2bc
- xserver 1.10 ABI rebuild

* Wed Mar 09 2011 Ben Skeggs <bskeggs@redhat.com> - 0.0.16-22
- prevent server crash if dri2 memory allocation fails

* Mon Feb 28 2011 Peter Hutterer <peter.hutterer@redhat.com> - 1:0.0.16-21.20110224gitbc5dec2
- Rebuild for server 1.10

* Thu Feb 24 2011 Ben Skeggs <bskeggs@redhat.com> 0.0.16-20
- fix bad rotate interaction with page flipping (rhbz#679505)
- man page updates

* Wed Feb 16 2011 Ben Skeggs <bskeggs@redhat.com> 0.0.16-19
- update to today's git, minor bugfixes and nv50 zcomp support

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.0.16-18.20110117git38e8809
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 17 2011 Ben Skeggs <bskeggs@redhat.com> 0.0.16-17
- update to today's git for fermi accel support

* Wed Jan 12 2011 Ben Skeggs <bskeggs@redhat.com> 0.0.16-16
- fix noaccel scanout buffer pitch on nv50+

* Thu Jan 06 2011 Ben Skeggs <bskeggs@redhat.com> 0.0.16-15
- pull upstream git snapshot, drop upstreamed patches

* Wed Dec 01 2010 Peter Hutterer <peter.hutterer@redhat.com>  0.0.16-14
- Rebuild for X Server 1.10

* Mon Nov 30 2010 Ben Skeggs <bskeggs@redhat.com> 0.0.16.13
- fix compiz breakage

* Mon Nov 29 2010 Ben Skeggs <bskeggs@redhat.com> 0.0.16-12
- fix dri2 issues

* Tue Nov 09 2010 Ben Skeggs <bskeggs@redhat.com> 0.0.16-11
- pull upstream git snapshot, require newer libdrm

* Wed Oct 27 2010 Adam Jackson <ajax@redhat.com> 0.0.16-10
- Add ABI requires magic (#542742)

* Mon Jul 05 2010 Peter Hutterer <peter.hutterer@redhat.com> - 1:0.0.16-9.20100615gitdb98ad2
- rebuild for X Server 1.9

* Mon Jul 5 2010 Ben Skeggs <bskeggs@redhat.com> 0.0.16-8.20100615gitdb98ad2
- bring in latest upstream

* Mon Feb 08 2010 Ben Skeggs <bskeggs@redhat.com> 0.0.16-0.20100205gite75dd23 
- pull in latest upstream, no longer any non-kms support

* Thu Jan 21 2010 Peter Hutterer <peter.hutterer@redhat.com> - 1:0.0.15-15.20091217gitbb19478
- Rebuild for server 1.8

* Wed Dec 23 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.15-14.20091217gitbb19478
- update to latest upstream code

* Tue Sep 29 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.15-13.20090929gitdd8339f
- fix driver to work again with recent EXA changes

* Fri Sep 25 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.15-12.20090924gitde0b095
- G80: small performance fix

* Mon Sep 21 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.15-11.20090921gitdf95ebd
- fix an accel pitch issue seen in rh#523281

* Mon Sep 14 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.15-10.20090914git1b72020
- wait for fbcon copy to complete before switching mode (rh#522688)

* Thu Sep 10 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.15-9.20090910git806eaf6
- fix a hang/crash issue that could occur during a modeset
- nouveau-transition-hack.patch: drop, supported with driver pixmaps anyway

* Wed Sep 09 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.15-8.20090904git2b5ec6a
- nouveau-tile7000.patch: workaround some display corruption on G8x

* Fri Sep 04 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.15-7.20090904git2b5ec6a
- fix cursor being left enabled on wrong display

* Thu Aug 27 2009 Adam Jackson <ajax@redhat.com> 0.0.15-6.20090820git569a17a
- nouveau-bgnr.patch: Enable seamless plymouth->gdm transition.

* Fri Aug 21 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.15-5.20090820git569a17a
- a couple more minor fixes

* Thu Aug 20 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.15-4.20090819gitfe2b5e6
- various fixes from upstream, build pending new xorg-x11-server update

* Tue Aug 11 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.15-3.20090810git85b1c86
- wfb fixes, driver pixmaps enabled by default

* Wed Aug 05 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.15-2.20090803git712064e
- dri2 fixes, no wfb without kms, non-kms fb resize fixes, other misc fixes

* Tue Aug 04 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.15-1.20090803git619103a
- upstream update, misc fixes

* Tue Jul 28 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.15-0.20090728git4d20547
- Update to latest upstream

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.0.14-4.20090717gitb1b2330
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 17 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.14-3.20090717gitb1b2330
- somehow missed updated patches to go on top

* Fri Jul 17 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.14-2.20090717gitb1b2330
- build fixes for recent X changes

* Wed Jul 15 2009 Adam Jackson <ajax@redhat.com> - 1:0.0.14-1.20090701git6d14327.1
- ABI bump

* Mon Jul 7 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.14-1.20090701git6d14327
- update from upstream + bring back additional features found in F11

* Fri Jun 26 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.14-0.20090625gitc0bf670
- rebase onto latest upstream.  missing some features that were patched into
  F11, they'll come back soon.

* Fri Apr 17 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.12-29.20090417gitfa2f111
- avoid post-beta hangs experienced by many people (rh#495764, rh#493222).
  - the bug here was relatively harmless, but exposed a more serious issue
    which has been fixed in libdrm-2.4.6-6.fc11
- kms: speed up transitions, they could take a couple of seconds previously
- framebuffer resize support (rh#495838, rh#487356, lots of dups)

* Wed Apr 15 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.12-27.20090413git7100c06
- fix rh#495843

* Mon Apr 13 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.12-26.20090413git7100c06
- nouveau-fedora.patch: split out into indivdual functionality
- nv50: disable acceleration on NVAx chipsets, it won't work properly yet
- drop nouveau-eedid.patch, it's upstream now

* Wed Apr 08 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.12-25.20090408gitd8545e6
- correct logic error in vbios parser (rh#493981)

* Wed Apr 08 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.12-24.20090408git960a5c8
- modify nv50 ddc regs again, fix kms edid property

* Tue Apr 07 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.12-23.20090407git11451ca
- upstream update: rh#492399, nv50 PROM fixes

* Sat Apr 04 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.12-22.20090404git836d985
- use consistent connector names across all modesetting paths
- rh#493981

* Fri Apr 03 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.12-21.20090403git11be9a9
- upstream update, loads of modesetting fixes
- rh#492819, rh#492427, rh#492289, rh#492289

* Mon Mar 30 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.12-20.20090330git9d46930
- xv bugfix

* Mon Mar 30 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.12-19.20090330git9213c39
- fix rh#492239, and various modesetting changes
- nouveau-eedid.patch: remove nv50 hunk, is upstream now

* Fri Mar 27 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.12-18.20090327gitf1907dc
- nv50: add default modes to mode pool for lvds panels (rh#492360)
- kms: fix getting edid blob from kernel

* Fri Mar 27 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.12-17.20090327gitf431e20
- fix partially obscured xv rendering without compmgr (rh#492227,rh#492229,rh#492428)
- fix crash when rotation requested (fdo#20848)
- additional sanity checks for kernel modesetting enabled

* Thu Mar 26 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.12-16.20090326git01cee29
- update, should fix rh#497173

* Mon Mar 23 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.12-15.20090324git4067ab4
- more ppc build fixes

* Mon Mar 23 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.12-14.20090323git3063486
- fix ppc build

* Mon Mar 23 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.12-13.20090323gitd80fe78
- modesetting fixes, should handle rh#487456

* Mon Mar 23 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.12-12.20090318git3e7fa97
- upstream update, various fixes to pre-nv50 modesetting, cleanups

* Fri Mar 13 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.12-11.20090313git79d23d8
- kms: dpms fixes
- kms: nicer reporting of output properties to users
- improve init paths, more robust
- support for multiple xservers (fast user switching)

* Tue Mar 10 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.12-10.20090310git8f9a580
- upstream update, should fix #455194

* Mon Mar 09 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.12-9.20090309gited9bd88
- upstream update, fixes
- store used vbios image in /var/run, will potentially help debugging later

* Thu Mar 05 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.12-8.20090305git42f99e6
- upstream update, fixes
- kms: support gamma and dpms calls
- kms: nicer transition to gdm from plymouth

* Mon Mar 02 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.12-7.20090302gite6c3b98
- upstream update, fixes

* Fri Feb 27 2009 Adam Jackson <ajax@redhat.com> 0.0.12-6.20090224gitd91fc78
- nouveau-eedid.patch: Do EEDID.

* Tue Feb 24 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.12-5.20090224gitd91fc78
- improve description of package

* Tue Feb 24 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.12-4.20090224gitd91fc78
- new upstream snapshot

* Tue Feb 17 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.12-1.20090216git7b25a30
- fixes from upstream
- append git version to tarball filename

* Mon Feb 16 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.12-1.20090213git2573c06
- latest snapshot
- add patches to improve G80/G90 desktop performance 

* Sat Feb 7 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.12-3.20090205git945f0cb
- build with kms paths enabled, so things don't blow up with kms turned on

* Thu Feb 5 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.12-1.20090205git945f0cb
- latest snapshot - kernel interface 0.0.12

* Tue Feb 03 2009 Kyle McMartin <kyle@redhat.com> 0.0.11-2.20090106git133c1a5
- add build-dep on mesa (missing GL/gl.h due to glxint.h)

* Tue Jan 13 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.11-1.20090106git133c1a5
- update to latest snapshot

* Wed Nov 19 2008 Dave Airlie <airlied@redhat.com> 0.0.11-1.20081119git65b956f
- update to latest upstream snapshot

* Tue Sep 02 2008 Dave Airlie <airlied@redhat.com> 0.0.11-1.20080902git6dd8ad4
- update to snapshot with new kernel interface 0.0.11

* Tue May 20 2008 Dave Airlie <airlied@redhat.com> 0.0.10-3.20080520git9c1d87f
- update to latest snapshot - enables randr12

* Tue Apr 08 2008 Dave Airlie <airlied@redhat.com> 0.0.10-2.20080408git0991281
- Update to latest snapshot

* Tue Mar 11 2008 Dave Airlie <airlied@redhat.com> 1:0.0.10-1.20080311git460cb26
- update to latest snapshot

* Fri Feb 29 2008 Dave Airlie <airlied@redhat.com> 1:0.0.10-1.20080221git5db7920
- Initial package for nouveau driver.
