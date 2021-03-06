%global tarball xf86-input-wacom
%global moduledir %(pkg-config xorg-server --variable=moduledir )
%global driverdir %{moduledir}/input

# Disable gitdate to build from a fixed release
#global gitdate 20111110
#global gitversion 12345689

Summary:    Xorg X11 wacom input driver
Summary(zh_CN.UTF-8): Xorg X11 wacom 输入驱动
Name:       xorg-x11-drv-wacom
Version:	0.31.0
Release:	4%{?dist}
URL:        http://www.x.org
License:    GPLv2+
Group:      User Interface/X Hardware Support
Group(zh_CN.UTF-8): 用户界面/X 硬件支持

%if 0%{?gitdate}
Source0: %{tarball}-%{gitdate}.tar.bz2
Source1: make-git-snapshot.sh
Source2: commitid
%else
Source0: http://prdownloads.sourceforge.net/linuxwacom/xf86-input-wacom-%{version}.tar.bz2
%endif
Source3: 70-wacom.rules

ExcludeArch: s390 s390x

BuildRequires: xorg-x11-server-devel >= 1.10.99.902
BuildRequires: xorg-x11-util-macros >= 1.3.0
BuildRequires: libX11-devel libXi-devel libXrandr-devel libXinerama-devel
BuildRequires: autoconf automake libtool
BuildRequires: systemd-devel

Requires: Xorg %(xserver-sdk-abi-requires ansic)
Requires: Xorg %(xserver-sdk-abi-requires xinput)

Provides:  linuxwacom = %{version}-%{release}
Obsoletes: linuxwacom <= 0.8.4.3

%description
X.Org X11 wacom input driver for Wacom tablets.

%description -l zh_CN.UTF-8
Xorg X11 wacom 输入驱动。

%prep

%setup -q -n %{tarball}-%{?gitdate:%{gitdate}}%{!?gitdate:%{version}}

%build
autoreconf --force -v --install || exit 1
%configure --disable-static --disable-silent-rules --enable-debug \
	   --with-systemd-unit-dir=%{_unitdir} \
           --with-udev-rules-dir=%{_prefix}/lib/udev/rules.d/
make %{_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# FIXME: Remove all libtool archives (*.la) from modules directory.  This
# should be fixed in upstream Makefile.am or whatever.
find $RPM_BUILD_ROOT -regex ".*\.la$" | xargs rm -f --
mv $RPM_BUILD_ROOT/%{_prefix}/lib/udev/rules.d/wacom.rules $RPM_BUILD_ROOT/%{_prefix}/lib/udev/rules.d/70-wacom.rules

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc AUTHORS README GPL
%if !0%{?gitdate}
# ChangeLog is autogenerated by make dist, we don't run it from git builds
%doc ChangeLog
%endif
%{driverdir}/wacom_drv.so
%{_mandir}/man4/wacom.4*
%{_mandir}/man1/xsetwacom.1*
%{_datadir}/X11/xorg.conf.d/50-wacom.conf
%{_bindir}/xsetwacom
%{_prefix}/lib/udev/rules.d/70-wacom.rules
%{_bindir}/isdv4-serial-inputattach
%{_unitdir}/wacom-inputattach@.service
%{_udevrulesdir}/70-wacom.rules

%package devel
Summary:    Xorg X11 wacom input driver development package
Group:      Development/Libraries

Requires: xorg-x11-server-devel >= 1.7.0
Requires: pkgconfig

%description devel
X.Org X11 wacom input driver development files.

%files devel
%defattr(-,root,root,-)
%doc GPL
%{_libdir}/pkgconfig/xorg-wacom.pc
%{_includedir}/xorg/Xwacom.h
%{_includedir}/xorg/wacom-properties.h
%{_includedir}/xorg/wacom-util.h
%{_includedir}/xorg/isdv4.h
%{_bindir}/isdv4-serial-debugger

%changelog
* Sun Nov 15 2015 Liu Di <liudidi@gmail.com> - 0.31.0-4
- 为 Magic 3.0 重建

* Fri Nov 06 2015 Liu Di <liudidi@gmail.com> - 0.31.0-3
- 为 Magic 3.0 重建

* Mon Oct 26 2015 Liu Di <liudidi@gmail.com> - 0.31.0-2
- 更新到 0.31.0

* Tue Apr 30 2013 Peter Hutterer <peter.hutterer@redhat.com> 0.21.0-1
- wacom 0.21.0

* Tue Apr 23 2013 Peter Hutterer <peter.hutterer@redhat.com> 0.20.99.1-1
- wacom 0.20.99.1

* Tue Mar 19 2013 Adam Jackson <ajax@redhat.com> 0.20.0-4
- Less RHEL customization

* Thu Mar 07 2013 Peter Hutterer <peter.hutterer@redhat.com> - 0.20.0-3
- require xorg-x11-server-devel, not -sdk

* Thu Mar 07 2013 Peter Hutterer <peter.hutterer@redhat.com> - 0.20.0-2
- ABI rebuild

* Tue Mar 05 2013 Peter Hutterer <peter.hutterer@redhat.com> 0.20.0-1
- wacom 0.20.0

* Wed Feb 27 2013 Peter Hutterer <peter.hutterer@redhat.com> 0.19.99.1-1
- wacom 0.19.99.1

* Fri Feb 15 2013 Peter Hutterer <peter.hutterer@redhat.com> - 0.19.0-4
- ABI rebuild

* Fri Feb 15 2013 Peter Hutterer <peter.hutterer@redhat.com> - 0.19.0-3
- ABI rebuild

* Thu Jan 10 2013 Adam Jackson <ajax@redhat.com> - 0.19.0-2
- ABI rebuild

* Fri Jan 04 2013 Peter Hutterer <peter.hutterer@redhat.com> 0.19.0-1
- wacom 0.19.0

* Thu Dec 20 2012 Peter Hutterer <peter.hutterer@redhat.com> 0.18.99.1-1
- wacom 0.18.99.1

* Wed Oct 31 2012 Peter Hutterer <peter.hutterer@redhat.com> - 0.18.0-2
- Fix %{?dist} tag

* Tue Oct 30 2012 Peter Hutterer <peter.hutterer@redhat.com> 0.18.0-1
- wacom 0.18.0

* Mon Oct 22 2012 Peter Hutterer <peter.hutterer@redhat.com> 0.17.99.1-1
- wacom 0.17.99.1

* Wed Sep 26 2012 Peter Hutterer <peter.hutterer@redhat.com> 0.17.0-1
- wacom 0.17.0

* Mon Aug 27 2012 Peter Hutterer <peter.hutterer@redhat.com> 0.16.1-1
- wacom 0.16.1

* Thu Aug 23 2012 Peter Hutterer <peter.hutterer@redhat.com> 0.16.0-6
- Pre-allocate the tap timer to avoid malloc locks in SIGIO handler
- Log in signal-safe manner

* Sun Aug 05 2012 Peter Hutterer <peter.hutterer@redhat.com> 0.16.0-5
- Align git snapshot building with other drivers
- Add autotools/libtool to BuildRequires, we need those when building git
  snapshots
- Always run autoreconf

* Sun Aug 05 2012 Peter Hutterer <peter.hutterer@redhat.com> 0.16.0-4
- Add support for Cintiq 22HD

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 18 2012 Dave Airlie <airlied@redhat.com> - 0.16.0-2
- ABI rebuild

* Tue Jul 10 2012 Peter Hutterer <peter.hutterer@redhat.com> 0.16.0-1
- wacom 0.16.0

* Thu Jun 07 2012 Peter Hutterer <peter.hutterer@redhat.com> 0.15.0-2
- Replace udev with systemd, use prefix for udev rules

* Fri May 04 2012 Peter Hutterer <peter.hutterer@redhat.com> 0.15.0-1
- wacom 0.15.0

* Mon Apr 23 2012 Peter Hutterer <peter.hutterer@redhat.com> 0.14.0-4
- Update rules to start inputattach automatically

* Thu Apr 05 2012 Adam Jackson <ajax@redhat.com> - 0.14.0-3
- RHEL arch exclude updates

* Mon Mar 26 2012 Peter Hutterer <peter.hutterer@redhat.com> 0.14.0-2
- Bump version number so F18 version is >= F17 version.

* Mon Mar 12 2012 Peter Hutterer <peter.hutterer@redhat.com> 0.14.0-1
- wacom 0.14.0

* Wed Mar 07 2012 Peter Hutterer <peter.hutterer@redhat.com> 0.13.99.2-1
- wacom 0.13.99.2

* Thu Mar 01 2012 Peter Hutterer <peter.hutterer@redhat.com> 0.13.99.1-1
- wacom 0.13.99.1

* Sat Feb 11 2012 Peter Hutterer <peter.hutterer@redhat.com> - 0.13.0-4
- ABI rebuild

* Fri Feb 10 2012 Peter Hutterer <peter.hutterer@redhat.com> - 0.13.0-3
- ABI rebuild

* Tue Jan 24 2012 Peter Hutterer <peter.hutterer@redhat.com> - 0.13.0-2
- ABI rebuild

* Tue Jan 17 2012 Peter Hutterer <peter.hutterer@redhat.com> 0.13.0-1
- wacom 0.13.0

* Wed Jan 04 2012 Peter Hutterer <peter.hutterer@redhat.com> 0.12.99.1-3
- Fix changelog, dates got mixed up

* Wed Jan 04 2012 Peter Hutterer <peter.hutterer@redhat.com> - 0.12.99.1-2
- Rebuild for server 1.12

* Wed Jan 04 2012 Peter Hutterer <peter.hutterer@redhat.com> 0.12.99.1-1
- wacom 0.12.99.1

* Tue Nov 29 2011 Peter Hutterer <peter.hutterer@redhat.com> 0.12-1
- wacom 0.12.0

* Mon Nov 14 2011 Adam Jackson <ajax@redhat.com> - 0.11.99.1-6.20111110
- ABI rebuild

* Thu Nov 10 2011 Peter Hutterer <peter.hutterer@redhat.com> 0.11.99.1-5.2011110
- And another snapshot, this time with the build fixes.

* Thu Nov 10 2011 Peter Hutterer <peter.hutterer@redhat.com> 0.11.99.1-4.2011110
- Update to latest git snapshot

* Wed Nov 09 2011 ajax <ajax@redhat.com> - 0.11.99.1-3.20111031
- ABI rebuild

* Tue Nov 01 2011 Peter Hutterer <peter.hutterer@redhat.com> 0.11.99.1-2
- libXinerama is now needed to build too

* Tue Nov 01 2011 Peter Hutterer <peter.hutterer@redhat.com> 0.11.99.1
- Update to 0.11.99.1 (from git)

* Thu Aug 18 2011 Adam Jackson <ajax@redhat.com> - 0.11.99-4.20110527
- Rebuild for xserver 1.11 ABI

* Thu Jul 21 2011 Peter Hutterer <peter.hutterer@redhat.com> * 0.11.99-3.20110527
- Fix udev rules file again:
  - use ==, not = to compare subsystems
  - assign ENV{NAME} even though we shouldn't, the server currently requires it
  - assign the lot to subsystem pnp too, that's where the server reads it
    from

* Wed Jul 20 2011 Peter Hutterer <peter.hutterer@redhat.com> 0.11.99-2.20110527
- Fix udev rules file (thanks to Lennart):
  - The subsystem cannot be assigned.
  - Append the attrs to the device name
  - Match only on tty/pnp

* Thu Jul 07 2011 Peter Hutterer <peter.hutterer@redhat.com>
- Disable silent rules on build

* Fri May 27 2011 Peter Hutterer <peter.hutterer@redhat.com> 0.11.99-1.20110527
- Update to current git

* Tue Apr 19 2011 Peter Hutterer <peter.hutterer@redhat.com> 0.11.0-1
- wacom 0.11.0

* Fri Apr 08 2011 Peter Hutterer <peter.hutterer@redhat.com> 0.10.99.2-1.20110408
- 0.10.99.2 from git

* Fri Apr 01 2011 Peter Hutterer <peter.hutterer@redhat.com> 0.10.99.1-2.20110401
- Require libudev

* Fri Apr 01 2011 Peter Hutterer <peter.hutterer@redhat.com> 0.10.99.1-1.20110401
- 0.10.99.1 from git

* Tue Mar 15 2011 Peter Hutterer <peter.hutterer@redhat.com> 0.10.99-1.20110315
- Today's git snapshot

* Thu Feb 17 2011 Peter Hutterer <peter.hutterer@redhat.com> 0.10.11-1
- wacom 0.10.11

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.10-3.20101122
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Nov 25 2010 Peter Hutterer <peter.hutterer@redhat.com> - 0.10.10-2.20101122
- Rebuild for server 1.10

* Mon Nov 22 2010 Peter Hutterer <peter.hutterer@redhat.com> 0.10.10-1
- Update to today's git snapshot (0.10.10), an emergency release.

* Fri Nov 19 2010 Peter Hutterer <peter.hutterer@redhat.com> 0.10.9-2
- require libXrandr-devel for xsetwacom

* Fri Nov 19 2010 Peter Hutterer <peter.hutterer@redhat.com> 0.10.9-1
- Update to today's git snapshot (0.10.9)

* Wed Oct 27 2010 Adam Jackson <ajax@redhat.com> 0.10.8-3
- Add ABI requires magic (#542742)


* Mon Aug 02 2010 Peter Hutterer <peter.hutterer@redhat.com> 0.10.8-2
- Update to today's git snapshot.

* Mon Jul 26 2010 Peter Hutterer <peter.hutterer@redhat.com> 0.10.8-1
- wacom 0.10.8 (from git)

* Thu Jul 08 2010 Adam Jackson <ajax@redhat.com> 0.10.7-4
- Install GPL in -devel too

* Mon Jul 05 2010 Peter Hutterer <peter.hutterer@redhat.com> 0.10.7-3.20100705
- Update to git to build against newest X server.

* Mon Jul 05 2010 Peter Hutterer <peter.hutterer@redhat.com> - 0.10.7-2.20100621
- rebuild for X Server 1.9

* Mon Jun 21 2010 Peter Hutterer <peter.hutterer@redhat.com> 0.10.7-1.20100621
- Update to 0.10.7 from git.

* Wed Jun 16 2010 Peter Hutterer <peter.hutterer@redhat.com> 0.10.6-6.20100616
- Update to today's git snapshot.

* Thu Jun 03 2010 Peter Hutterer <peter.hutterer@redhat.com> 0.10.6-5.2010603
- Update to today's git snapshot.

* Thu Jun 03 2010 Peter Hutterer <peter.hutterer@redhat.com> 0.10.6-5.20100521
- Update udev rules file to include Fujitsu serial tablets. (#598168)
- Update udev rules file to set ID_INPUT_TABLET

* Fri May 21 2010 Peter Hutterer <peter.hutterer@redhat.com> 0.10.6-4.20100521
- Update to today's git snapshot.
- wacom-0.10.6-serial-identifiers.patch: drop, upstream.

* Tue May 18 2010 Peter Hutterer <peter.hutterer@redhat.com> 0.10.6-3.20100427
- Install wacom udev rules file to identify serial devices.

* Tue Apr 27 2010 Peter Hutterer <peter.hutterer@redhat.com> 0.10.6-2.20100427
- wacom-0.10.6-serial-identifiers.patch: add some more serial IDs to the
  config file.

* Tue Apr 27 2010 Peter Hutterer <peter.hutterer@redhat.com> 0.10.6-1.20100427
- wacom 0.10.6 (from git)

* Thu Apr 15 2010 Peter Hutterer <peter.hutterer@redhat.com> 0.10.5-5.20100325
- Fix up missing directory change from last commit.

* Thu Apr 15 2010 Peter Hutterer <peter.hutterer@redhat.com> 0.10.5-4.20100325
- Install config snippet in $datadir/X11/xorg.conf.d
- rename to 50-wacom.conf to match upstream naming

* Thu Mar 25 2010 Peter Hutterer <peter.hutterer@redhat.com> 0.10.5-3.20100325
- Update to today's git snapshot.

* Tue Mar 23 2010 Peter Hutterer <peter.hutterer@redhat.com> 0.10.5-2.20100319
- Enable the debug properties.

* Fri Mar 19 2010 Peter Hutterer <peter.hutterer@redhat.com> 0.10.5-1.20100319
- Update to today's git snapshot (0.10.5)

* Tue Mar 16 2010 Peter Hutterer <peter.hutterer@redhat.com> 0.10.4-7.20100316
- Update to today's git snapshot.

* Fri Mar 05 2010 Peter Hutterer <peter.hutterer@redhat.com> 0.10.4-6.20100305
- Update to today's git snapshot.

* Thu Mar 04 2010 Peter Hutterer <peter.hutterer@redhat.com> 0.10.4-5.20100219
- Fix 10-wacom.conf for N-Trig devices: rename the class (copy/paste error)
  and only take event devices. (Related #526270)

* Fri Feb 19 2010 Peter Hutterer <peter.hutterer@redhat.com> 0.10.4-4.20100219
- Add stuff required to build from upstream git.
- Update to today's git snapshot.

* Wed Feb 17 2010 Peter Hutterer <peter.hutterer@redhat.com> 0.10.4-3
- Add 10-wacom.conf, the fdi file doesn't work anymore.
- Drop hal requires.

* Wed Feb 03 2010 Peter Hutterer <peter.hutterer@redhat.com> 0.10.4-2
- Update sources to sourceforge, 0.10.4 was released on sf only.
- Remove wacom.fdi, we're just using the one shipped by the driver now.

* Thu Jan 21 2010 Peter Hutterer <peter.hutterer@redhat.com> 0.10.4-1
- wacom 0.10.4

* Thu Jan 21 2010 Peter Hutterer <peter.hutterer@redhat.com> - 0.10.3-3
- Rebuild for server 1.8

* Tue Jan 05 2010 Peter Hutterer <peter.hutterer@redhat.com> 0.10.3-2
- BuildRequires and Requires libX11 and libXi for xsetwacom.

* Tue Jan 05 2010 Peter Hutterer <peter.hutterer@redhat.com> 0.10.3-1
- wacom 0.10.3

* Thu Dec 03 2009 Peter Hutterer <peter.hutterer@redhat.com> 0.10.2-1
- wacom 0.10.2

* Fri Nov 20 2009 Peter Hutterer <peter.hutterer@redhat.com> 0.10.1-2
- cvs add 10-wacom.fdi, this time really.

* Fri Nov 20 2009 Peter Hutterer <peter.hutterer@redhat.com> 0.10.1-1
- wacom 0.10.1
- BuildRequires xorg-x11-util-macros 1.3.0
- Remove unnecessary 'find' directive, changed upstream.
- Add GPL document
- Install 10-wacom.fdi file.
- Provides: linuxwacom

* Thu Nov 19 2009 Peter Hutterer <peter.hutterer@redhat.com> 0.10.0-3
- Use smp_mflags when building.

* Wed Nov 18 2009 Peter Hutterer <peter.hutterer@redhat.com> 0.10.0-2
- Obsolete linuxwacom, don't Conflict with it.
- Remove trailing dot from summary (rpmlint warning).
- Remove spurious executable bits from source files (rpmlint warning).
- Add AUTHORS, ChangeLog, README to doc

* Mon Oct 19 2009 Peter Hutterer <peter.hutterer@redhat.com> 0.10.0-1
- Initial import

