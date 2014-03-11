%define pkgname apps

Summary: X.Org X11 applications
Name: xorg-x11-%{pkgname}
# NOTE: The package version should be set to the X11 major release from which
# the OS release is based upon.
Version: 7.6
Release: 6%{?dist}
License: MIT
Group: User Interface/X
URL: http://www.x.org

# Clock apps
Source0:  http://ftp.nara.wide.ad.jp/pub/X11/x.org/individual/app/oclock-1.0.2.tar.bz2
Source1:  http://ftp.nara.wide.ad.jp/pub/X11/x.org/individual/app/xclock-1.0.5.tar.bz2
# X Window Dump (xwd) utilities
Source2:  http://ftp.nara.wide.ad.jp/pub/X11/x.org/individual/app/xwd-1.0.4.tar.bz2
Source3:  http://ftp.nara.wide.ad.jp/pub/X11/x.org/individual/app/xwud-1.0.3.tar.bz2
Source4:  http://ftp.nara.wide.ad.jp/pub/X11/x.org/individual/app/xpr-1.0.3.tar.bz2
# Miscellaneous other applications
Source5:  http://ftp.nara.wide.ad.jp/pub/X11/x.org/individual/app/luit-1.1.0.tar.bz2
Source6:  http://ftp.nara.wide.ad.jp/pub/X11/x.org/individual/app/x11perf-1.5.3.tar.bz2
Source7:  http://ftp.nara.wide.ad.jp/pub/X11/x.org/individual/app/xbiff-1.0.2.tar.bz2
Source8:  http://ftp.nara.wide.ad.jp/pub/X11/x.org/individual/app/xclipboard-1.1.1.tar.bz2
Source9:  http://ftp.nara.wide.ad.jp/pub/X11/x.org/individual/app/xconsole-1.0.4.tar.bz2
Source10: http://ftp.nara.wide.ad.jp/pub/X11/x.org/individual/app/xcursorgen-1.0.4.tar.bz2
Source11: http://ftp.nara.wide.ad.jp/pub/X11/x.org/individual/app/xeyes-1.1.1.tar.bz2
Source13: http://ftp.nara.wide.ad.jp/pub/X11/x.org/individual/app/xload-1.1.0.tar.bz2
Source14: http://ftp.nara.wide.ad.jp/pub/X11/x.org/individual/app/xlogo-1.0.3.tar.bz2
Source15: http://ftp.nara.wide.ad.jp/pub/X11/x.org/individual/app/xmag-1.0.4.tar.bz2
Source16: http://ftp.nara.wide.ad.jp/pub/X11/x.org/individual/app/xmessage-1.0.3.tar.bz2
Source18: http://ftp.nara.wide.ad.jp/pub/X11/x.org/individual/app/xfd-1.1.0.tar.bz2
Source19: http://ftp.nara.wide.ad.jp/pub/X11/x.org/individual/app/xfontsel-1.0.3.tar.bz2
Source20: http://ftp.nara.wide.ad.jp/pub/X11/x.org/individual/app/xvidtune-1.0.2.tar.bz2

Patch0: x11perf-1.4.1-x11perf-datadir-cleanups.patch
Patch2: xconsole-1.0.3-streams-me-softer.patch
Patch6: xbiff-1.0.2-xmu-configure.patch

BuildRequires: autoconf automake

BuildRequires: xorg-x11-util-macros
# xfd needs gettext
BuildRequires: gettext
BuildRequires: zlib-devel
BuildRequires: libfontenc-devel
BuildRequires: libX11-devel
BuildRequires: libXmu-devel
BuildRequires: libXext-devel
BuildRequires: libXt-devel
BuildRequires: libXaw-devel
BuildRequires: libXpm-devel
BuildRequires: libXft-devel
BuildRequires: libXrender-devel
BuildRequires: libxkbfile-devel
BuildRequires: libXcursor-devel
BuildRequires: libpng-devel
BuildRequires: libXfixes-devel
BuildRequires: libXi-devel >= 1.2
BuildRequires: libXxf86vm-devel
BuildRequires: xorg-x11-xbitmaps

Provides: luit oclock x11perf xbiff xclipboard xclock xconsole xcursorgen
Provides: xeyes xload xlogo xmag xmessage xpr xwd xwud
Provides: xfd xfontsel xvidtune

# NOTE: xwd, xwud, luit used to be in these.
Obsoletes: XFree86, xorg-x11
# NOTE: x11perf, xclipboard used to be in these.
Obsoletes: XFree86-tools, xorg-x11-tools
# Xaw app moves
Conflicts: xorg-x11-utils < 7.4-5.fc12
Conflicts: xorg-x11-server-utils < 7.4-8.fc12

%description
A collection of common X Window System applications.

%prep
%setup -q -c %{name}-%{version} -a1 -a2 -a3 -a4 -a5 -a6 -a7 -a8 -a9 -a10 -a11 -a13 -a14 -a15 -a16 -a18 -a19 -a20
%patch0 -p0 -b .x11perf-datadir-cleanups
#%patch2 -p0 -b .streams-me-softer
%patch6 -p1 -b .xmu-configure

%build
# Build all apps
{
for app in * ; do
	pushd $app
		sed -i '/XAW_/ s/)/, xaw7)/; /XAW_/ s/XAW_CHECK_XPRINT_SUPPORT/PKG_CHECK_MODULES/' configure.ac
		autoreconf -v --install
		%configure --disable-xprint
		make
	popd
done
}

%install
rm -rf $RPM_BUILD_ROOT
# Install all apps
{
for app in * ; do
	pushd $app
	make install DESTDIR=$RPM_BUILD_ROOT
	popd
done
}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
#%doc
%{_bindir}/luit
%{_bindir}/oclock
%{_bindir}/x11perf
%{_bindir}/x11perfcomp
%{_bindir}/xbiff
%{_bindir}/xclipboard
%{_bindir}/xclock
%{_bindir}/xconsole
%{_bindir}/xcursorgen
%{_bindir}/xcutsel
%{_bindir}/xdpr
%{_bindir}/xeyes
%{_bindir}/xfd
%{_bindir}/xfontsel
%{_bindir}/xload
%{_bindir}/xlogo
%{_bindir}/xmag
%{_bindir}/xmessage
%{_bindir}/xpr
%{_bindir}/xvidtune
%{_bindir}/xwd
%{_bindir}/xwud
%{_datadir}/X11/app-defaults/Clock-color
%{_datadir}/X11/app-defaults/XClipboard
%{_datadir}/X11/app-defaults/XClock
%{_datadir}/X11/app-defaults/XClock-color
%{_datadir}/X11/app-defaults/XConsole
%{_datadir}/X11/app-defaults/XFontSel
%{_datadir}/X11/app-defaults/Xfd
%{_datadir}/X11/app-defaults/XLoad
%{_datadir}/X11/app-defaults/XLogo
%{_datadir}/X11/app-defaults/XLogo-color
%{_datadir}/X11/app-defaults/Xmag
%{_datadir}/X11/app-defaults/Xmessage
%{_datadir}/X11/app-defaults/Xmessage-color
%{_datadir}/X11/app-defaults/Xvidtune
%dir %{_datadir}/X11/x11perfcomp
%{_datadir}/X11/x11perfcomp/Xmark
%{_datadir}/X11/x11perfcomp/fillblnk
%{_datadir}/X11/x11perfcomp/perfboth
%{_datadir}/X11/x11perfcomp/perfratio
#%dir %{_mandir}/man1x
%{_mandir}/man1/xcursorgen.1*
%{_mandir}/man1/Xmark.1*
%{_mandir}/man1/luit.1*
%{_mandir}/man1/oclock.1*
%{_mandir}/man1/x11perf.1*
%{_mandir}/man1/x11perfcomp.1*
%{_mandir}/man1/xbiff.1*
%{_mandir}/man1/xclipboard.1*
%{_mandir}/man1/xclock.1*
%{_mandir}/man1/xconsole.1*
%{_mandir}/man1/xcutsel.1*
%{_mandir}/man1/xdpr.1*
%{_mandir}/man1/xeyes.1*
%{_mandir}/man1/xfd.1*
%{_mandir}/man1/xfontsel.1*
%{_mandir}/man1/xload.1*
%{_mandir}/man1/xlogo.1*
%{_mandir}/man1/xmag.1*
%{_mandir}/man1/xmessage.1*
%{_mandir}/man1/xpr.1*
%{_mandir}/man1/xvidtune.1*
%{_mandir}/man1/xwd.1*
%{_mandir}/man1/xwud.1*

%changelog
* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 7.6-6
- 为 Magic 3.0 重建

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Nov 10 2011 Adam Jackson <ajax@redhat.com> 7.6-4
- Move xinput and xkill to xorg-x11-server-utils

* Mon Nov 07 2011 Adam Jackson <ajax@redhat.com> 7.6-3
- Rebuild for libpng 1.5

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 06 2011 Adam Jackson <ajax@redhat.com> 7.6-1
- x11perf 1.5.3

* Fri Nov 26 2010 Peter Hutterer <peter.hutterer@redhat.com> 7.5-5
- xeyes 1.1.1

* Fri Nov 12 2010 Peter Hutterer <peter.hutterer@redhat.com> 7.5-4
- xinput 1.5.3
- xkill 1.0.3

* Wed Nov 10 2010 Peter Hutterer <peter.hutterer@redhat.com> 7.5-3
- xclipboard 1.1.1

* Mon Nov 08 2010 Peter Hutterer <peter.hutterer@redhat.com> 7.5-2
- oclock 1.0.2
- xclock 1.0.5
- xconsole 1.0.4
- xbiff 1.0.2
- luit 1.1.0
- x11perf 1.5.2
- xcursorgen 1.0.4
- xeyes 1.1.0
- xload 1.1.0
- xlogo 1.0.3
- xmag 1.0.4
- xmessage 1.0.3
- xfd 1.1.0
- xfontsel 1.0.3
- xvidtune 1.0.2

* Mon Nov 08 2010 Peter Hutterer <peter.hutterer@redhat.com> 7.5-1
- xwd 1.0.4
- xwud 1.0.3

* Fri Jun 04 2010 Peter Hutterer <peter.hutterer@redhat.com> 7.4-14
- xinput 1.5.2

* Mon Mar 15 2010 Peter Hutterer <peter.hutterer@redhat.com> 7.4-13
- xinput 1.5.1

* Fri Mar 05 2010 Matěj Cepl <mcepl@redhat.com> - 7.4-12
- Add missing BR xorg-x11-xbitmaps

* Thu Mar 04 2010 Matěj Cepl <mcepl@redhat.com> - 7.4-11
- Don't steal directory owned by filesystem package

* Tue Feb 09 2010 Adam Jackson <ajax@redhat.com> 7.4-10
- xlogo-1.0.1-add-needed.patch: Fix FTBFS for --no-add-needed

* Mon Oct 19 2009 Adam Jackson <ajax@redhat.com> 7.4-9
- xclipboard 1.1.0
- xcursorgen 1.0.3
- xpr 1.0.3
- xwd 1.0.3
- x11perf 1.5.1

* Tue Oct 13 2009 Peter Hutterer <peter.hutterer@redhat.com> 7.4-8
- xinput 1.5.0
- xwud 1.0.2
- xkill 1.0.2
- xmag 1.0.3

* Wed Oct 07 2009 Adam Jackson <ajax@redhat.com> 7.4-7
- xeyes 1.0.991

* Tue Oct 06 2009 Adam Jackson <ajax@redhat.com> 7.4-6
- luit 1.0.4

* Thu Sep 24 2009 Peter Hutterer <peter.hutterer@redhat.com> 7.4-5
- xclock 1.0.4
- xinput 1.4.99.3

* Mon Aug 03 2009 Peter Hutterer <peter.hutterer@redhat.com> 7.4-4
- xinput 1.4.99.2

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 23 2009 Adam Jackson <ajax@redhat.com> 7.4-2
- Un-require xorg-x11-filesystem

* Thu Jul 02 2009 Adam Jackson <ajax@redhat.com> 7.4-1
- Add xfd, xfontsel, and xvidtune

* Mon Jun 22 2009 Peter Hutterer <peter.hutterer@redhat.com> 7.3-10
- xinput 1.4.99.1

* Thu May 07 2009 Peter Hutterer <peter.hutterer@redhat.com> 7.3-9
- xinput 1.4.2

* Mon Apr 06 2009 Peter Hutterer <peter.hutterer@redhat.com> 7.3-8
- xinput 1.4.1

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 16 2009 Peter Hutterer <peter.hutterer@redhat.com> 7.3-6
- xinput 1.4.0

* Tue Sep 9 2008 Peter Hutterer <peter.hutterer@redhat.com> 7.3-5
- Add xinput tool.

* Tue Jul 15 2008 Adam Jackson <ajax@redhat.com> 7.3-4
- Fix license tag.

* Fri Apr 04 2008 Adam Jackson <ajax@redhat.com> 7.3-3
- xconsole-1.0.3-streams-me-softer.patch: Don't include STREAMS headers,
  since glibc so thoughtfully removed them. (#440717)

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 7.3-2
- Autorebuild for GCC 4.3

* Mon Sep 24 2007 Adam Jackson <ajax@redhat.com> 7.3-1
- xconsole 1.0.3
- xmessage 1.0.2
- Bump to 7.3-1

* Tue Aug 21 2007 Dave Airlie <airlied@redhat.com> 7.2-1
- luit-1.0.2 xclock 1.0.3 xmag 1.0.2 xpr 1.0.2 xload 1.0.2 xcursorgen 1.0.2
- bump to 7.2 version

* Tue Jan 30 2007 Adam Jackson <ajax@redhat.com> 7.1-4
- Fix man page globs and rebuild for FC7.

* Mon Oct 2 2006 Soren Sandmann <sandmann@redhat.com> 7.1-3.fc6
- Fix race condition in luit (Bug 197165).

* Wed Jul 19 2006 Mike A. Harris <mharris@redhat.com> 7.1-2.fc6
- Remove app-defaults dir from file manifest, as it is owned by libXt (#174021)
- Add 'dist' tag to package release string.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> 7.1-1.1
- rebuild

* Tue Jun 20 2006 Mike A. Harris <mharris@redhat.com> 7.1-1
- Added xload-1.0.1-setuid.diff to fix potential security issue (#196094)
- Artificially inflate package version-release to 7.1 to match the X11R7.1
  release that all of the tarballs are taken from.
- Update to xconsole-1.0.2, xcursorgen-1.0.1 from X11R7.1
- Add temporary dependency on autoconf, automake for brew builds.

* Fri May 26 2006 Adam Jackson <ajackson@redhat.com> 1.0.3-2
- Add more BuildRequires to fix mock builds.  (#191896)

* Thu Apr 27 2006 Adam Jackson <ajackson@redhat.com> 1.0.3-1
- Updated xclock and xconsole

* Thu Mar 02 2006 Adam Jackson <ajackson@redhat.com> 1.0.2-1
- Bump x11perf to 1.4.1 from upstream.

* Fri Feb 24 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-2
- Added luit-1.0.1-locale.alias-datadir.patch to fix bug (#181785)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> 1.0.1-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> 1.0.1-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan 18 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-1
- Upgraded all apps to version 1.0.1 from X11R7.0

* Sat Dec 17 2005 Mike A. Harris <mharris@redhat.com> 1.0.0-1
- Upgraded all apps to version 1.0.0 from X11R7 RC4.
- Changed manpage dir from man1x to man1 to match upstream default now.
- Dropped all of the datadir-cleanups patches added in the previous build.
- Added x11perf-1.0.0-x11perf-datadir-cleanups.patch as it is still needed
  to put the helper scripts in datadir.
- Added --disable-xprint to configure, as a great symbolic jesture.

* Wed Nov 22 2005 Mike A. Harris <mharris@redhat.com> 0.99.2-4
- Added "Requires(pre): xorg-x11-filesystem >= 0.99.2-3" to workaround
  (#173384)
- Added the following patches, and invoke aclocal/automake/autoconf on them
  to force app-defaults and other datafiles into _datadir instead of _libdir:
  - oclock-0.99.1-oclock-datadir-cleanups.patch
  - x11perf-0.99.1-x11perf-datadir-cleanups.patch
  - xclipboard-0.99.1-xclipboard-datadir-cleanups.patch
  - xclock-0.99.1-xclock-datadir-cleanups.patch
  - xconsole-0.99.2-xconsole-datadir-cleanups.patch
  - xload-0.99.1-xload-datadir-cleanups.patch
  - xlogo-0.99.1-xlogo-datadir-cleanups.patch
  - xmag-0.99.1-xmag-datadir-cleanups.patch
  - xmessage-0.99.1-xmessage-datadir-cleanups.patch
- Added luit-0.99.1-luit-locale-dir-fix.patch to fix bug (#173702)

* Mon Nov 14 2005 Jeremy Katz <katzj@redhat.com> 0.99.2-3
- add Requires(pre) on newer filesystem package (#172610)

* Sun Nov 13 2005 Mike A. Harris <mharris@redhat.com> 0.99.2-2
- Add "Obsoletes: XFree86, XFree86-tools, xorg-x11, xorg-x11-tools", as 
  various utils have moved here from there in monolithic X packaging.
- Add "BuildRequires: xbitmaps-devel" for xbiff.
- Rebuild against new libXaw 0.99.2-2, which has fixed DT_SONAME. (#173027)

* Fri Nov 11 2005 Mike A. Harris <mharris@redhat.com> 0.99.2-1
- Initial build, with all apps taken from X11R7 RC2.
- Use "make install DESTDIR=$RPM_BUILD_ROOT" as the makeinstall macro fails on
  some packages.
- Temporary hack to move xcursorgen manpage to 'man1' dir.
