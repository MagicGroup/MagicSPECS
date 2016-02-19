%global tarball xf86-input-evdev
%global moduledir %(pkg-config xorg-server --variable=moduledir )
%global driverdir %{moduledir}/input

#global gitdate 20130214
%global gitversion c085c8b6c

Summary:    Xorg X11 evdev input driver
Summary(zh_CN.UTF-8): Xorg X11 evdev 输入驱动
Name:       xorg-x11-drv-evdev
Version:	2.10.1
Release:	1%{?dist}
URL:        http://www.x.org
License:    MIT
Group:      User Interface/X Hardware Support
Group(zh_CN.UTF-8): 用户界面/X 硬件支持

%if 0%{?gitdate}
Source0:    %{tarball}-%{gitdate}.tar.bz2
Source1:    make-git-snapshot.sh
Source2:    commitid
%else
Source0:    http://xorg.freedesktop.org/releases/individual/driver/%{tarball}-%{version}.tar.bz2
%endif

ExcludeArch: s390 s390x

BuildRequires: autoconf automake libtool
BuildRequires: xorg-x11-server-devel >= 1.10.99.902
BuildRequires: libudev-devel mtdev-devel
BuildRequires: xorg-x11-util-macros >= 1.3.0

Requires: Xorg %(xserver-sdk-abi-requires ansic)
Requires: Xorg %(xserver-sdk-abi-requires xinput)
Requires:  xkeyboard-config >= 1.4-1
Requires: mtdev

%description
X.Org X11 evdev input driver.

%description -l zh_CN.UTF-8
Xorg X11 evdev 输入驱动。

%prep
%setup -q -n %{tarball}-%{?gitdate:%{gitdate}}%{!?gitdate:%{version}}

%build
autoreconf --force -v --install || exit 1
%configure --disable-static --disable-silent-rules
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
%doc COPYING
%{driverdir}/evdev_drv.so
%{_mandir}/man4/evdev.4*


%package devel
Summary:    Xorg X11 evdev input driver development package.
Group:      Development/Libraries
Requires:   pkgconfig
%description devel
X.Org X11 evdev input driver development files.

%files devel
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/pkgconfig/xorg-evdev.pc
%dir %{_includedir}/xorg
%{_includedir}/xorg/evdev-properties.h
%{_datadir}/X11/xorg.conf.d/10-evdev.conf

%changelog
* Sun Nov 15 2015 Liu Di <liudidi@gmail.com> - 2.10.0-3
- 为 Magic 3.0 重建

* Fri Nov 06 2015 Liu Di <liudidi@gmail.com> - 2.10.0-2
- 更新到 2.10.0

* Mon Oct 26 2015 Liu Di <liudidi@gmail.com> - 2.9.2-2
- 更新到 2.9.2

* Mon Jan 13 2014 Adam Jackson <ajax@redhat.com> - 2.8.2-6
- 1.15 ABI rebuild

* Tue Dec 17 2013 Adam Jackson <ajax@redhat.com> - 2.8.2-5
- 1.15RC4 ABI rebuild

* Wed Nov 20 2013 Adam Jackson <ajax@redhat.com> - 2.8.2-4
- 1.15RC2 ABI rebuild

* Wed Nov 06 2013 Adam Jackson <ajax@redhat.com> - 2.8.2-3
- 1.15RC1 ABI rebuild

* Fri Oct 25 2013 Adam Jackson <ajax@redhat.com> - 2.8.2-2
- ABI rebuild

* Mon Oct 07 2013 Peter Hutterer <peter.hutterer@redhat.com> 2.8.2-1
- evdev 2.8.2

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 12 2013 Peter Hutterer <peter.hutterer@redhat.com> 2.8.1-2
- Fix changelog - 'percent signs in specfile changelog should be escaped'

* Thu Jul 11 2013 Peter Hutterer <peter.hutterer@redhat.com> 2.8.1-1
- evdev 2.8.1

* Mon Apr 15 2013 Peter Hutterer <peter.hutterer@redhat.com> 2.8.0-3
- With the patch file

* Mon Apr 15 2013 Peter Hutterer <peter.hutterer@redhat.com> 2.8.0-2
- Add option Type name to auto-assign XI_TRACKBALL

* Tue Mar 26 2013 Peter Hutterer <peter.hutterer@redhat.com> 2.8.0-1
- evdev 2.8.0

* Tue Mar 19 2013 Adam Jackson <ajax@redhat.com> 2.7.99-6.20130214gitc085c8b6c
- Less RHEL customization

* Thu Mar 07 2013 Peter Hutterer <peter.hutterer@redhat.com> - 2.7.99-5.20130214gitc085c8b6c
- require xorg-x11-server-devel, not -sdk

* Thu Mar 07 2013 Peter Hutterer <peter.hutterer@redhat.com> - 2.7.99-4.20130214gitc085c8b6c
- ABI rebuild

* Fri Feb 15 2013 Peter Hutterer <peter.hutterer@redhat.com> - 2.7.99-3.20130214gitc085c8b6c
- ABI rebuild

* Fri Feb 15 2013 Peter Hutterer <peter.hutterer@redhat.com> - 2.7.99-2.20130214gitc085c8b6c
- ABI rebuild

* Thu Feb 14 2013 Peter Hutterer <peter.hutterer@redhat.com> 2.7.99-1.20130214gitc085c8b6c
- Today's git snapshot

* Mon Jan 14 2013 Peter Hutterer <peter.hutterer@redhat.com> 2.7.3-5
- Fix device rotation through SwapAxes/Invert{X|Y} for touch devices

* Thu Jan 10 2013 Adam Jackson <ajax@redhat.com> - 2.7.3-4
- ABI rebuild

* Tue Jan 08 2013 Peter Hutterer <peter.hutterer@redhat.com> 2.7.3-3
- Ignore joysticks with MT axes

* Wed Oct 31 2012 Peter Hutterer <peter.hutterer@redhat.com> 2.7.3-2
- Fix {?dist} tag

* Mon Aug 13 2012 Peter Hutterer <peter.hutterer@redhat.com> 2.7.3-1
- evdev 2.7.3

* Wed Aug 08 2012 Peter Hutterer <peter.hutterer@redhat.com> 2.7.2-6
- Fix broken ButtonMapping option (regression in 2.7.2)

* Mon Aug 06 2012 Peter Hutterer <peter.hutterer@redhat.com> 2.7.2-5
- Drop libxkbfile-devel BuildRequires, not needed anymore

* Sat Aug 04 2012 Peter Hutterer <peter.hutterer@redhat.com> 2.7.2-4
- Force autoreconf to avoid spurious libtool errors

* Sat Aug 04 2012 Peter Hutterer <peter.hutterer@redhat.com> 2.7.2-3
- Don't delete the device on ENODEV to avoid free in signal handler

* Sat Aug 04 2012 Peter Hutterer <peter.hutterer@redhat.com> 2.7.2-2
- Add missing changelog message.

* Sat Aug 04 2012 Peter Hutterer <peter.hutterer@redhat.com> 2.7.2-1
- evdev 2.7.2

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.0-6.20120718gitf5ede9808
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 18 2012 Dave Airlie <airlied@redhat.com> 2.7.0-5.20120718gitf5ede9808
- git snapshot evdev, for ABI rebuild

* Wed Jul 04 2012 Peter Hutterer <peter.hutterer@redhat.com> 2.7.0-4
- Don't leak mtdev data

* Thu Apr 05 2012 Adam Jackson <ajax@redhat.com> - 2.7.0-3
- RHEL arch exclude updates

* Tue Mar 27 2012 Peter Hutterer <peter.hutterer@redhat.com> 2.7.0-2
- Fix inverted horizontal scroll
- Fix broken scroll wheels on QEMU tablets (#805902)

* Wed Mar 07 2012 Peter Hutterer <peter.hutterer@redhat.com> 2.7.0-1
- evdev 2.7.0

* Sat Feb 11 2012 Peter Hutterer <peter.hutterer@redhat.com> - 2.6.99.901-9.20120118git9d9c9870c
- ABI rebuild

* Fri Feb 10 2012 Peter Hutterer <peter.hutterer@redhat.com> - 2.6.99.901-8.20120118git9d9c9870c
- ABI rebuild

* Wed Jan 25 2012 Peter Hutterer <peter.hutterer@redhat.com> 2.6.99.901-7.20120118git9d9c9870c
- only force relative x/y to exists if we don't have ABS_X/Y (#784391) 

* Mon Jan 23 2012 Peter Hutterer <peter.hutterer@redhat.com> - 2.6.99.901-6.20120118git9d9c9870c
- ABI rebuild

* Wed Jan 18 2012 Peter Hutterer <peter.hutterer@redhat.com> 2.6.99.901-5.20120118git9d9c9870c
- Update to new git snapshot, includes the two patches now

* Thu Jan 12 2012 Peter Hutterer <peter.hutterer@redhat.com> 2.6.99.901-4.20120103git965338e9d
- Fix axis labelling and single-axis relative devices

* Wed Jan 04 2012 Peter Hutterer <peter.hutterer@redhat.com> 2.6.99.901-3.20120103git965338e9d
- Add mtdev as dependency

* Tue Jan 03 2012 Peter Hutterer <peter.hutterer@redhat.com> 2.6.99.901-2.20120103git965338e9d
- Another snapshot, this time with the right udev dependency

* Tue Jan 03 2012 Peter Hutterer <peter.hutterer@redhat.com> 2.6.99.901-1.20120103git009ac94a8
- 2.6.99.901 from git

* Mon Nov 14 2011 Adam Jackson <ajax@redhat.com> - 2.6.99-4.20111110gita9cdb6590
- ABI rebuild

* Thu Nov 10 2011 Adam Williamson <awilliam@redhat.com> - 2.6.99-3.20111110gita9cdb6590
- latest git again to fix bad breakage in last snapshot

* Wed Nov 09 2011 ajax <ajax@redhat.com> - 2.6.99-2.20111109git745fca03a
- ABI rebuild

* Wed Nov 09 2011 Peter Hutterer <peter.hutterer@redhat.com>  2.6.99-1.20111109git745fca03a
- Today's git snapshot

* Thu Aug 18 2011 Adam Jackson <ajax@redhat.com> - 2.6.99-3.20110601giteaf202531
- Rebuild for xserver 1.11 ABI

* Mon Aug 01 2011 Peter Hutterer <peter.hutterer@redhat.com> 2.6.99-2.20110601giteaf202531
- devel package requires pkg-config.

* Thu Jul 07 2011 Peter Hutterer <peter.hutterer@redhat.com>
- Build verbose, with smp_mflags

* Wed Jun 01 2011 Peter Hutterer <peter.hutterer@redhat.com> 2.6.99-1.20110601giteaf202531
- Today's snapshot from git

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 11 2011 Peter Hutterer <peter.hutterer@redhat.com> 2.6.0-1
- evdev 2.6.0

* Wed Jan 05 2011 Peter Hutterer <peter.hutterer@redhat.com> 2.5.99.903-1.20110105git540a4cce9
- evdev 2.6RC3 snapshot from git

* Wed Dec 08 2010 Peter Hutterer <peter.hutterer@redhat.com> 2.5.99.902-1.20101208git1c5ad6f8a
- evdev 2.6RC1 snapshot from git

* Thu Nov 25 2010 Peter Hutterer <peter.hutterer@redhat.com> - 2.5.99.901-2.20101122
- Rebuild for server 1.10

* Mon Nov 22 2010 Peter Hutterer <peter.hutterer@redhat.com> 2.5.99.901-1
- evdev 2.6RC1 snapshot from git

* Wed Oct 27 2010 Adam Jackson <ajax@redhat.com> 2.5.0-2
- Add ABI requires magic. (#542742)

* Mon Aug 23 2010 Peter Hutterer <peter.hutterer@redhat.com> 2.5.0-1
- evdev 2.5.0 from git

* Mon Aug 23 2010 Peter Hutterer <peter.hutterer@redhat.com>
- automatically use git sources if gitdate is defined

* Thu Aug 19 2010 Peter Hutterer <peter.hutterer@redhat.com> 2.4.99.901-1.20100819
- evdev 2.4.99.901 from git

* Thu Jul 08 2010 Adam Jackson <ajax@redhat.com> 2.4.0-3
- Package COPYING.

* Mon Jul 05 2010 Peter Hutterer <peter.hutterer@redhat.com> - 2.4.0-2.20100406
- rebuild for X Server 1.9

* Tue Apr 06 2010 Peter Hutterer <peter.hutterer@redhat.com> 2.4.0-1.20100406
- evdev 2.4.0, built from git.

* Thu Jan 21 2010 Peter Hutterer <peter.hutterer@redhat.com> - 2.3.99-2.20100108
- Rebuild for server 1.8

* Fri Jan 08 2010 Peter Hutterer <peter.hutterer@redhat.com> 2.3.99-1.20100108
- Update to current git

* Wed Jan 06 2010 Peter Hutterer <peter.hutterer@redhat.com> 2.3.0-1
- evdev 2.3.0
- BuildRequires xorg-x11-util-macros 1.3.0
- Fix tab/spaces mix in spec file.
- Use global instead of define.

* Thu Oct 08 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.2.99.2-1
- evdev 2.2.99.2

* Wed Sep 23 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.2.99-8.20090923
- Update to today's git master (fixes wheel emulation)

* Wed Sep 09 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.2.99-7.20090909
- Update to today's git master

* Fri Aug 14 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.2.99-6.20090814
- Update to today's git master

* Thu Jul 30 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.2.99-5.20090730
- Update to today's git master

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.99-4.20090629.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 15 2009 Adam Jackson <ajax@redhat.com> - 2.2.99-3.20090629.1
- ABI bump

* Thu Jul 09 2009 Adam Jackson <ajax@redhat.com> 2.2.99-3.20090629
- Fix EVR inversion, 1.20090629 < 2.20090619

* Mon Jun 29 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.2.99-1.20090629
- Update to today's git master
- Add commitid file with git's sha1.

* Fri Jun 19 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.2.99-2.20090619
- rebuild for server ABI 7

* Fri Jun 19 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.2.99-1.20090619
- Update to today's git master

* Thu May 21 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.2.99-1.20090521
- Update to today's git master

* Thu May 07 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.2.2-1
- evdev 2.2.2

* Mon Apr 06 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.2.1-2
- evdev-2.2.1-read-deadlock.patch: handle read errors on len <= 0 (#494245)

* Tue Mar 24 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.2.1-1
- evdev 2.2.1 

* Mon Mar 09 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.2.0-1
- evdev 2.2.0

* Mon Mar 02 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.1.99.1-1
- evdev 2.2 snapshot 1

* Thu Feb 26 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.1.99.2.20090226
- Update to today's git master.

* Thu Feb 19 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.1.99-1.20090219
- Update to today's git master.

* Thu Feb 19 2009 Peter Hutterer <peter.hutterer@redhat.com>
- purge obsolete patches.

* Tue Feb 17 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.1.3-1
- evdev 2.1.3

* Mon Feb 02 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.1.2-1
- evdev 2.1.2

* Tue Jan 13 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.1.1-1
- evdev 2.1.1
- update Requires to 1.5.99.1 to make sure the ABI is right.

* Mon Dec 22 2008 Dave Airlie <airlied@redhat.com> 2.1.0-3
- Rebuild again - latest tag wasn't in buildroot

* Mon Dec 22 2008 Peter Hutterer <peter.hutterer@redhat.com> 2.1.0-2
- Rebuild for server 1.6.

* Wed Nov 19 2008 Peter Hutterer <peter.hutterer@redhat.com> 2.1.0-1
- evdev 2.1.0

* Tue Nov 4 2008 Peter Hutterer <peter.hutterer@redhat.com> 2.0.99.3-1
- evdev 2.0.99.3 (evdev 2.1 RC 3)

* Fri Oct 24 2008 Peter Hutterer <peter.hutterer@redhat.com> 2.0.99.2-1
- evdev 2.0.99.2 (evdev 2.1 RC 2)

* Fri Oct 17 2008 Peter Hutterer <peter.hutterer@redhat.com> 2.0.99.1-1
- evdev 2.0.99.1 (evdev 2.1 RC 1)
- Upstream change now requires libxkbfile-devel to build.

* Mon Oct 13 2008 Peter Hutterer <peter.hutterer@redhat.com> 2.0.99-1
- Today's git snapshot.
- Require xkeyboard-config 1.4 and higher for evdev ruleset.
- Provide devel subpackage for evdev header files.

* Fri Oct 3 2008 Peter Hutterer <peter.hutterer@redhat.com> 2.0.6-1
- update to 2.0.6
- remove patches merged upstream.

* Fri Sep 12 2008 Adam Jackson <ajax@redhat.com> 2.0.4-3
- evdev-2.0.4-reopen-device.patch: When arming the reopen timer, stash it in
  the driver private, and explicitly cancel it if the server decides to
  close the device for real.
- evdev-2.0.4-cache-info.patch: Rebase to account for same.

* Thu Aug 28 2008 Peter Hutterer <peter.hutterer@redhat.com> 2.0.4-2
- evdev-2.0.4-reopen-device.patch: try to reopen devices if a read error
  occurs on the fd.
- evdev-2.0.4-cache-info.patch: cache device info to ensure reopened device
  isn't different to previous one.

* Mon Aug 25 2008 Peter Hutterer <peter.hutterer@redhat.com> 2.0.4-1
- evdev 2.0.4

* Fri Aug 1 2008 Peter Hutterer <peter.hutterer@redhat.com> 2.0.3-1
- evdev 2.0.3

* Mon Jul 21 2008 Peter Hutterer <peter.hutterer@redhat.com> 2.0.2-1
- evdev 2.0.2

* Fri Mar 14 2008 Adam Jackson <ajax@redhat.com> 1.99.1-0.5
- Today's snapshot.  Maps REL_DIAL to REL_HWHEEL.

* Wed Mar 12 2008 Adam Jackson <ajax@redhat.com> 1.99.1-0.4
- Today's snapshot.  Fixes mouse button repeat bug, and therefore Apple
  Mighty Mice are usable.  Props to jkeating for the hardware.

* Tue Mar 11 2008 Adam Jackson <ajax@redhat.com> 1.99.1-0.3
- Today's snapshot.  Fixes right/middle button swap hilarity.

* Mon Mar 10 2008 Adam Jackson <ajax@redhat.com> 1.99.1-0.2
- Updated snapshot, minor bug fixes.

* Fri Mar 07 2008 Adam Jackson <ajax@redhat.com> 1.99.1-0.1
- evdev 2.0 git snapshot

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.2.0-2
- Autorebuild for GCC 4.3

* Tue Nov 27 2007 Adam Jackson <ajax@redhat.com> 1.2.0-1
- xf86-input-evdev 1.2.0

* Wed Aug 22 2007 Adam Jackson <ajax@redhat.com> - 1.1.2-5
- Rebuild for PPC toolchain bug

* Mon Jun 18 2007 Adam Jackson <ajax@redhat.com> 1.1.2-4
- Update Requires and BuildRequires.  Disown the module directories.

* Fri Feb 16 2007 Adam Jackson <ajax@redhat.com> 1.1.2-3
- ExclusiveArch -> ExcludeArch

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - sh: line 0: fg: no job control
- rebuild

* Tue Jun 13 2006 Adam Jackson <ajackson@redhat.com> 1.1.2-2
- Build on ppc64

* Mon Jun 05 2006 Adam Jackson <ajackson@redhat.com> 1.1.2-1
- Update to 1.1.2 + CVS fixes.

* Mon Apr 10 2006 Adam Jackson <ajackson@redhat.com> 1.1.0-3
- Work around header pollution on ia64, re-add to arch list.

* Mon Apr 10 2006 Adam Jackson <ajackson@redhat.com> 1.1.0-2
- Disable on ia64 until build issues are sorted.

* Sun Apr  9 2006 Adam Jackson <ajackson@redhat.com> 1.1.0-1
- Update to 1.1.0 from 7.1RC1.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.0.0.5-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.0.0.5-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan 18 2006 Mike A. Harris <mharris@redhat.com> 1.0.0.5-1
- Updated xorg-x11-drv-evdev to version 1.0.0.5 from X11R7.0

* Tue Dec 20 2005 Mike A. Harris <mharris@redhat.com> 1.0.0.4-1
- Updated xorg-x11-drv-evdev to version 1.0.0.4 from X11R7 RC4
- Removed 'x' suffix from manpage dirs to match RC4 upstream.

* Wed Nov 16 2005 Mike A. Harris <mharris@redhat.com> 1.0.0.2-1
- Updated xorg-x11-drv-evdev to version 1.0.0.2 from X11R7 RC2

* Fri Nov 4 2005 Mike A. Harris <mharris@redhat.com> 1.0.0.1-1
- Updated xorg-x11-drv-evdev to version 1.0.0.1 from X11R7 RC1
- Fix *.la file removal.

* Fri Sep 2 2005 Mike A. Harris <mharris@redhat.com> 1.0.0-0
- Initial spec file for evdev input driver generated automatically
  by my xorg-driverspecgen script.
