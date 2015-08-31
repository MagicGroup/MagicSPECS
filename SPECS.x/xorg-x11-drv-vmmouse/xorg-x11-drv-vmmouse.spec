%global tarball xf86-input-vmmouse
%global moduledir %(pkg-config xorg-server --variable=moduledir )
%global driverdir %{moduledir}/input

#global gitdate 20101209
#global gitversion 07232feb6

Summary:    Xorg X11 vmmouse input driver
Name:	    xorg-x11-drv-vmmouse
Version:    13.1.0
Release:    5%{?gitdate:.%{gitdate}git%{gitversion}}%{?dist}
URL:	    http://www.x.org
License:    MIT
Group:	    User Interface/X Hardware Support

%if 0%{?gitdate}
Source0:    %{tarball}-%{gitdate}.tar.bz2
Source1:    make-git-snapshot.sh
Source2:    commitid
%else
Source0:    ftp://ftp.x.org/pub/individual/driver/%{tarball}-%{version}.tar.bz2
%endif

# Yes, this is not the same as vmware.  Yes, this is intentional.
ExclusiveArch: %{ix86} x86_64

BuildRequires: xorg-x11-server-devel >= 1.10.99.902 systemd-devel
BuildRequires: automake autoconf libtool

Requires: Xorg %(xserver-sdk-abi-requires ansic)
Requires: Xorg %(xserver-sdk-abi-requires xinput)
Requires: xorg-x11-server-Xorg

%description 
X.Org X11 vmmouse input driver.

%prep
%setup -q -n %{tarball}-%{?gitdate:%{gitdate}}%{!?gitdate:%{version}}

%build
autoreconf -v --install --force || exit 1
%configure --disable-static --disable-silent-rules \
    --with-xorg-conf-dir='%{_datadir}/X11/xorg.conf.d' \
    --with-udev-rules-dir=%{_prefix}/lib/udev/rules.d
make %{?_smp_mflags}

%install
%make_install

# FIXME: Remove all libtool archives (*.la) from modules directory.  This
# should be fixed in upstream Makefile.am or whatever.
find $RPM_BUILD_ROOT -regex ".*\.la$" | xargs rm -f --

# Don't need HAL no more
rm -rf $RPM_BUILD_ROOT/%{_libdir}/hal/hal-probe-vmmouse
rm -rf $RPM_BUILD_ROOT/%{_datadir}/hal/fdi/

%files
%{driverdir}/vmmouse_drv.so
%{_mandir}/man4/vmmouse.4*
%{_mandir}/man1/vmmouse_detect.1*
%{_bindir}/vmmouse_detect
%{_datadir}/X11/xorg.conf.d/50-vmmouse.conf
%{_prefix}/lib/udev/rules.d/*.rules

%changelog
* Fri Aug 28 2015 Liu Di <liudidi@gmail.com> - 13.1.0-5
- 为 Magic 3.0 重建

* Fri Aug 28 2015 Liu Di <liudidi@gmail.com> - 13.1.0-4
- 为 Magic 3.0 重建

* Fri Aug 28 2015 Liu Di <liudidi@gmail.com> - 13.1.0-3
- 为 Magic 3.0 重建

* Wed Jul 29 2015 Dave Airlie <airlied@redhat.com> - 13.1.0-2
- 1.15 ABI rebuild

* Fri Jun 26 2015 Peter Hutterer <peter.hutterer@redhat.com> 13.1.0-1
- vmmouse 13.1.0

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 13.0.99-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri May 15 2015 Hans de Goede <hdegoede@redhat.com> - 13.0.99-1
- vmmouse 13.0.99
- This ensures that xorg-x11-drv-vmmouse plays nice together with the
  upcoming vmmouse kernel driver (related rhbz#1214474)

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 13.0.0-15
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 13.0.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 13.0.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Apr 28 2014 Hans de Goede <hdegoede@redhat.com> - 13.0.0-12
- xserver 1.15.99-20140428 git snapshot ABI rebuild

* Mon Jan 13 2014 Adam Jackson <ajax@redhat.com> - 13.0.0-11
- 1.15 ABI rebuild

* Tue Dec 17 2013 Adam Jackson <ajax@redhat.com> - 13.0.0-10
- 1.15RC4 ABI rebuild

* Wed Nov 20 2013 Adam Jackson <ajax@redhat.com> - 13.0.0-9
- 1.15RC2 ABI rebuild

* Wed Nov 06 2013 Adam Jackson <ajax@redhat.com> - 13.0.0-8
- 1.15RC1 ABI rebuild

* Fri Oct 25 2013 Adam Jackson <ajax@redhat.com> - 13.0.0-7
- ABI rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 13.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 07 2013 Peter Hutterer <peter.hutterer@redhat.com> - 13.0.0-5
- require xorg-x11-server-devel, not -sdk

* Thu Mar 07 2013 Peter Hutterer <peter.hutterer@redhat.com> - 13.0.0-4
- ABI rebuild

* Fri Feb 15 2013 Peter Hutterer <peter.hutterer@redhat.com> - 13.0.0-3
- ABI rebuild

* Fri Feb 15 2013 Peter Hutterer <peter.hutterer@redhat.com> - 13.0.0-2
- ABI rebuild

* Wed Jan 16 2013 Peter Hutterer <peter.hutterer@redhat.com> 13.0.0-1
- vmmouse 13.0.0

* Thu Jan 10 2013 Adam Jackson <ajax@redhat.com> - 12.9.0-8
- ABI rebuild

* Wed Oct 31 2012 Peter Hutterer <peter.hutterer@redhat.com> - 12.9.0-7
- Fix {?dist} tag

* Mon Aug 20 2012 Adam Jackson <ajax@redhat.com> 12.9.0-6
- vmmouse-12.9.0-unsafe-logging.patch: Stifle some unsafe logging on the
  read_input path.

* Sun Aug 05 2012 Peter Hutterer <peter.hutterer@redhat.com> 12.9.0-5
- Get the udev rules dir from udev.pc instead of manually patching it

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12.9.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 18 2012 Dave Airlie <airlied@redhat.com> - 12.9.0-3
- ABI rebuild

* Thu Jun 07 2012 Peter Hutterer <peter.hutterer@redhat.com> 12.9.0-2
- replace udev with systemd, install rules files with prefix

* Wed May 23 2012 Peter Hutterer <peter.hutterer@redhat.com> 12.9.0-1
- vmmouse 12.9.0

* Fri Mar 09 2012 Peter Hutterer <peter.hutterer@redhat.com> 12.8.0-1
- vmmouse 12.8.0

* Sat Feb 11 2012 Peter Hutterer <peter.hutterer@redhat.com> - 12.7.0-9
- ABI rebuild

* Fri Feb 10 2012 Peter Hutterer <peter.hutterer@redhat.com> - 12.7.0-8
- ABI rebuild

* Tue Jan 24 2012 Peter Hutterer <peter.hutterer@redhat.com> - 12.7.0-7
- ABI rebuild

* Wed Jan 04 2012 Peter Hutterer <peter.hutterer@redhat.com> - 12.7.0-6
- Rebuild for server 1.12

* Mon Nov 14 2011 Adam Jackson <ajax@redhat.com> - 12.7.0-5
- ABI rebuild

* Thu Nov 10 2011 Peter Hutterer <peter.hutterer@redhat.com> 12.7.0-4
- Deal with input ABI 14 option types

* Wed Nov 09 2011 ajax <ajax@redhat.com> - 12.7.0-3
- ABI rebuild

* Thu Aug 18 2011 Adam Jackson <ajax@redhat.com> - 12.7.0-2
- Rebuild for xserver 1.11 ABI

* Thu Jul 07 2011 Peter Hutterer <peter.hutterer@redhat.com>
- Disable silent rules on build, build with _smp_mflags

* Thu Mar 03 2011 Peter Hutterer <peter.hutterer@redhat.com> 12.7.0-1
- vmmouse 12.7.0

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12.6.99.901-2.20101209git07232feb6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 09 2010 Peter Hutterer <peter.hutterer@redhat.com> 12.6.99.901-1.20101209git07232feb6
- 12.7RC1 snapshot from git
- add a few missing git snapshot bits

* Thu Nov 25 2010 Peter Hutterer <peter.hutterer@redhat.com> - 12.6.10-3.20101125
- Rebuild for server 1.10

* Thu Nov 25 2010 Peter Hutterer <peter.hutterer@redhat.com> 12.6.10-2.20101125
- add git snapshotting hooks
- update to today's git snapshot

* Wed Oct 27 2010 Adam Jackson <ajax@redhat.com> 12.6.10-2
- Add ABI requires magic (#542742)

* Thu Aug 12 2010 Peter Hutterer <peter.hutterer@redhat.com> 12.6.10-1
- vmmouse 12.6.10

* Mon Jul 05 2010 Peter Hutterer <peter.hutterer@redhat.com> - 12.6.9-5
- rebuild for X Server 1.9

* Thu Jul 01 2010 Peter Hutterer <peter.hutterer@redhat.com> 12.6.9-4
- vmmouse-12.6.9-iopl-revert.patch: revert removal of iopl(2) call (#640660)

* Fri Jun 18 2010 Peter Hutterer <peter.hutterer@redhat.com> 12.6.9-3
- vmmouse-12.6.9-single-udev-match.patch: only match event devices once.

* Thu Apr 15 2010 Peter Hutterer <peter.hutterer@redhat.com> 12.6.9-2
- Install config snippet in $datadir/X11/xorg.conf.d.

* Fri Apr 09 2010 Peter Hutterer <peter.hutterer@redhat.com> 12.6.9-1
- vmmouse 12.6.9, installs udev rules and xorg.conf.d snippets
- Require xserver 1.7.99.1 or later and udev.

* Fri Mar 19 2010 Peter Hutterer <peter.hutterer@redhat.com> 12.6.7-1
- vmmouse 12.6.7

* Wed Feb 10 2010 Peter Hutterer <peter.hutterer@redhat.com> 12.6.6-1
- vmmouse 12.6.6
- abi.patch: drop, merged upstream.

* Thu Jan 21 2010 Peter Hutterer <peter.hutterer@redhat.com> - 12.6.5-4
- Rebuild for server 1.8

* Wed Jan 06 2010 Peter Hutterer <peter.hutterer@redhat.com> 12.6.5-3
- Use global instead of define as per Packaging Guidelines

* Thu Aug 27 2009 Adam Jackson <ajax@redhat.com> 12.6.5-2
- abi.patch: Re-add. (#518589)

* Fri Aug 07 2009 Peter Hutterer <peter.hutterer@redhat.com> 12.6.5-1
- vmmouse 12.6.5
- vmmouse-12.6.4-abi.patch: Drop.

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12.6.4-3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 15 2009 Adam Jackson <ajax@redhat.com> - 12.6.4-2.1
- ABI bump

* Thu Jul 09 2009 Adam Jackson <ajax@redhat.com> 12.6.4-2
- Port to new server ABI (#509682)

* Wed May 13 2009 Peter Hutterer <peter.hutterer@redhat.com> 12.6.4-1
- vmmouse 12.6.4

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12.6.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 12 2009 Peter Hutterer <peter.hutterer@redhat.com> 12.6.3-3
- Revert last commit, this is against Fedora policy.
  https://fedoraproject.org/wiki/Packaging:Guidelines#Configuration_files

* Mon Feb 09 2009 Peter Hutterer <peter.hutterer@redhat.com> 12.6.3-2
- Don't overwrite the fdi file on upgrade.

* Mon Dec 22 2008 Peter Hutterer <peter.hutterer@redhat.com> 12.6.3-1
- vmmouse 12.6.3

* Mon Nov 17 2008 Peter Hutterer <peter.hutterer@redhat.com> 12.6.2-1
- vmmouse 12.6.2

* Mon Oct 27 2008 Peter Hutterer <peter.hutterer@redhat.com> 12.6.1-1
- vmmouse 12.6.1

* Tue Oct 21 2008 Peter Hutterer <peter.hutterer@redhat.com> 12.5.2-1
- vmmouse 12.5.2

* Thu Mar 20 2008 Adam Jackson <ajax@redhat.com> 12.5.0-1
- vmmouse 12.5.0

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 12.4.3-4
- Autorebuild for GCC 4.3

* Wed Jan  2 2008 Jeremy Katz <katzj@redhat.com> - 12.4.3-3
- Add workaround for xserver not calling convert_proc in input drivers 
  anymore (patch from Joerg Platte on debian xmaint list)

* Tue Dec 18 2007 Jeremy Katz <katzj@redhat.com> - 12.4.3-2
- Rebuild for new xserver

* Thu Oct 11 2007 Adam Jackson <ajax@redhat.com> 12.4.3-1
- xf86-input-vmmouse 12.4.3

* Mon Sep 24 2007 Adam Jackson <ajax@redhat.com> 12.4.2-1
- xf86-input-vmmouse 12.4.2

* Fri Aug 24 2007 Adam Jackson <ajax@redhat.com> - 12.4.0-4
- Rebuild for build ID

* Mon Jun 18 2007 Adam Jackson <ajax@redhat.com> 12.4.0-3
- Update Requires and BuildRequires.  Disown the module directories. 

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - sh: line 0: fg: no job control
- rebuild

* Sun Apr  9 2006 Adam Jackson <ajackson@redhat.com> 12.4.0-1
- Update to 12.4.0 from 7.1RC1.

* Wed Mar 29 2006 Adam Jackson <ajackson@redhat.com> 12.3.2.0-4
- Don't build on ia64, as per comments in the source.

* Wed Mar 29 2006 Adam Jackson <ajackson@redhat.com> 12.3.2.0-3
- Rebump to appease beehive.

* Wed Mar 29 2006 Adam Jackson <ajackson@redhat.com> 12.3.2.0-1
- Bump to 12.3.2.0 from upstream (LP64 fixes).

* Sun Feb  5 2006 Mike A. Harris <mharris@redhat.com> 12.3.1.0-1
- Initial spec file for vmmouse input driver, using xorg-x11-drv-mouse.spec
  version 1.0.3.1-1 as a template.
