%global tarball xf86-input-keyboard
%global moduledir %(pkg-config xorg-server --variable=moduledir )
%global driverdir %{moduledir}/input

#global gitdate 20101201

Summary:    Xorg X11 keyboard input driver
Name:       xorg-x11-drv-keyboard
Version:    1.8.0
Release:    5%{?gitdate:.%{gitdate}}%{?dist}
URL:        http://www.x.org
License:    MIT
Group:      User Interface/X Hardware Support

%if 0%{?gitdate}
Source0:   %{tarball}-%{gitdate}.tar.bz2
Source1:   make-git-snapshot.sh
Source2:   commitid
%else
Source0:   http://ftp.nara.wide.ad.jp/pub/X11/x.org/individual/driver/%{tarball}-%{version}.tar.bz2
%endif

ExcludeArch: s390 s390x %{?rhel:ppc ppc64}

BuildRequires: autoconf automake libtool
BuildRequires: xorg-x11-server-devel >= 1.10.99.902
BuildRequires: xorg-x11-util-macros >= 1.3.0

Requires:  xkeyboard-config >= 1.2-2
Requires: Xorg %(xserver-sdk-abi-requires ansic)
Requires: Xorg %(xserver-sdk-abi-requires xinput)

%description
X.Org X11 keyboard input driver.

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
%{driverdir}/kbd_drv.so
%{_mandir}/man4/kbd.4*

%changelog
* Mon Jan 13 2014 Adam Jackson <ajax@redhat.com> - 1.8.0-5
- 1.15 ABI rebuild

* Tue Dec 17 2013 Adam Jackson <ajax@redhat.com> - 1.8.0-4
- 1.15RC4 ABI rebuild

* Wed Nov 20 2013 Adam Jackson <ajax@redhat.com> - 1.8.0-3
- 1.15RC2 ABI rebuild

* Wed Nov 06 2013 Adam Jackson <ajax@redhat.com> - 1.8.0-2
- 1.15RC1 ABI rebuild

* Fri Nov 01 2013 Peter Hutterer <peter.hutterer@redhat.com> 1.8.0-1
- xf86-input-keyboard 1.8.0

* Fri Oct 25 2013 Adam Jackson <ajax@redhat.com> - 1.7.0-3
- ABI rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 27 2013 Peter Hutterer <peter.hutterer@redhat.com> 1.7.0-1
- keyboard 1.7.0

* Thu Mar 07 2013 Peter Hutterer <peter.hutterer@redhat.com> - 1.6.2-8
- require xorg-x11-server-devel, not -sdk

* Thu Mar 07 2013 Peter Hutterer <peter.hutterer@redhat.com> - 1.6.2-7
- ABI rebuild

* Fri Feb 15 2013 Peter Hutterer <peter.hutterer@redhat.com> - 1.6.2-6
- ABI rebuild

* Fri Feb 15 2013 Peter Hutterer <peter.hutterer@redhat.com> - 1.6.2-5
- ABI rebuild

* Thu Jan 10 2013 Adam Jackson <ajax@redhat.com> - 1.6.2-4
- ABI rebuild

* Wed Oct 31 2012 Peter Hutterer <peter.hutterer@redhat.com> - 1.6.2-3
- Fix {?dist} tag

* Thu Aug 02 2012 Peter Hutterer <peter.hutterer@redhat.com> 1.6.2-2
- Force autoreconf to avoid libtool versioning errors

* Tue Jul 24 2012 Peter Hutterer <peter.hutterer@redhat.com> 1.6.2-1
- keyboard 1.6.2

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 18 2012 Dave Airlie <airlied@redhat.com> - 1.6.1-6
- ABI rebuild

* Thu Apr 05 2012 Adam Jackson <ajax@redhat.com> - 1.6.1-5
- RHEL arch exclude updates

* Sat Feb 11 2012 Peter Hutterer <peter.hutterer@redhat.com> - 1.6.1-4
- ABI rebuild

* Fri Feb 10 2012 Peter Hutterer <peter.hutterer@redhat.com> - 1.6.1-3
- ABI rebuild

* Tue Jan 24 2012 Peter Hutterer <peter.hutterer@redhat.com> - 1.6.1-2
- ABI rebuild

* Wed Jan 04 2012 Peter Hutterer <peter.hutterer@redhat.com> 1.6.1-1
- keyboard 1.6.1

* Mon Nov 14 2011 Adam Jackson <ajax@redhat.com> - 1.6.0-4
- ABI rebuild

* Wed Nov 09 2011 ajax <ajax@redhat.com> - 1.6.0-3
- ABI rebuild

* Thu Aug 18 2011 Adam Jackson <ajax@redhat.com> - 1.6.0-2
- Rebuild for xserver 1.11 ABI

* Thu Jul 07 2011 Peter Hutterer <peter.hutterer@redhat.com>
- Disable silent rules on build, build with _smp_mflags

* Tue Mar 08 2011 Peter Hutterer <peter.hutterer@redhat.com> 1.6.0-1
- keyboard 1.6.0

* Mon Feb 21 2011 Peter Hutterer <peter.hutterer@redhat.com> 1.5.99.901-1
- xf86-input-keyboard 1.6RC1

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-4.20101201
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 01 2010 Peter Hutterer <peter.hutterer@redhat.com> - 1.5.0-3.20101201
- Rebuild for server 1.10

* Wed Dec 01 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.5.0-2.20101201
- Add git hooks
- Update to today's git snapshot

* Mon Nov 01 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.5.0-1
- keyboard 1.5.0

* Wed Oct 27 2010 Adam Jackson <ajax@redhat.com> 1.4.0-6
- Add ABI requires magic (#542742)

* Mon Jul 05 2010 Peter Hutterer <peter.hutterer@redhat.com> - 1.4.0-5
- rebuild for X Server 1.9

* Thu Jan 21 2010 Peter Hutterer <peter.hutterer@redhat.com> - 1.4.0-4
- Rebuild for server 1.8

* Thu Jan 07 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.4.0-3
- Use global instead of define as per Packaging Guidelines.
- Fix tab/spaces mixup.
- Remove unused files from old keyboard driver.

* Fri Nov 20 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.4.0-2
- BuildRequires xorg-x11-util-macros 1.3.0

* Wed Oct 07 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.4.0-1
- keyboard 1.4.0

* Wed Sep 09 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.3.99.1-1
- keyboard 1.3.99.1

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.99-3.20090715.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 15 2009 Adam Jackson <ajax@redhat.com> - 1.3.99-2.20090715.1
- ABI bump

* Wed Jul 15 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.3.99-2.20090715
- Rebuild, this time with the right tarball.

* Wed Jul 15 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.3.99-1.20090715
- Today's git snapshot.
- keyboard-1.3.2-terminate.patch: Drop.

* Wed Apr 08 2009 Peter Hutterer <peter.hutterer@redhat.com> - 1.3.2-3
- keyboard-1.3.2-terminate.patch: dont handle C-A-B zapping in the driver.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 08 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.3.2-1
- keyboard 1.3.2

* Mon Dec 22 2008 Peter Hutterer <peter.hutterer@redhat.com> 1.3.1-1.20081222
- Today's git snapshot.

* Mon Dec 22 2008 Peter Hutterer <peter.hutterer@redhat.com> 1.3.1-1
- keyboard 1.3.1

* Wed Apr  9 2008 Kristian Høgsberg <krh@redhat.com> - 1.3.0-3
- Drop us+inet patch and require xkeyboard-config-1.2-2 instead.

* Wed Mar 26 2008 Adam Jackson <ajax@redhat.com> 1.3.0-2
- kbd-1.3.0-us-inet.patch: Switch default layout to us+inet.

* Thu Mar 20 2008 Adam Jackson <ajax@redhat.com> 1.3.0-1
- keyboard 1.3.0

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.2.2-4
- Autorebuild for GCC 4.3

* Tue Nov 13 2007 Adam Jackson <ajax@redhat.com> 1.2.2-3
- BuildReq: xserver 1.4.99.1

* Tue Oct 09 2007 Adam Jackson <ajax@redhat.com> 1.2.2-2
- kbd-1.2.2-no-sleeping-on-the-job.patch: Don't sleep(1) on VT switch.
  Makes startup faster and prettier.

* Mon Sep 24 2007 Adam Jackson <ajax@redhat.com> 1.2.2-1
- xf86-input-keyboard 1.2.2

* Wed Aug 22 2007 Adam Jackson <ajax@redhat.com> - 1.1.0-5
- Rebuild for PPC toolchain bug

* Mon Jun 18 2007 Adam Jackson <ajax@redhat.com> 1.1.0-4
- Update Requires and BuildRequires.  Disown the module directories.

* Fri Feb 16 2007 Adam Jackson <ajax@redhat.com> 1.1.0-3
- ExclusiveArch -> ExcludeArch

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - sh: line 0: fg: no job control
- rebuild

* Tue Jun 13 2006 Adam Jackson <ajackson@redhat.com> 1.1.0-2
- Build on ppc64

* Sun Apr  9 2006 Adam Jackson <ajackson@redhat.com> 1.1.0-1
- Update to 1.1.0 from 7.1RC1.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.0.1.3-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.0.1.3-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan 18 2006 Mike A. Harris <mharris@redhat.com> 1.0.1.3-1
- Updated xorg-x11-drv-keyboard to version 1.0.1.3 from X11R7.0
- Added alpha/sparc/sparc64 to ExclusiveArch list (#176590)

* Tue Dec 20 2005 Mike A. Harris <mharris@redhat.com> 1.0.1.2-1
- Updated xorg-x11-drv-keyboard to version 1.0.1.2 from X11R7 RC4
- Removed 'x' suffix from manpage dirs to match RC4 upstream.

* Wed Nov 16 2005 Mike A. Harris <mharris@redhat.com> 1.0.1-1
- Updated xorg-x11-drv-keyboard to version 1.0.1 from X11R7 RC2

* Fri Nov 4 2005 Mike A. Harris <mharris@redhat.com> 1.0.0.1-1
- Updated xorg-x11-drv-keyboard to version 1.0.0.1 from X11R7 RC1
- Fix *.la file removal.

* Fri Sep 2 2005 Mike A. Harris <mharris@redhat.com> 1.0.0-0
- Initial spec file for keyboard input driver generated automatically
  by my xorg-driverspecgen script.
