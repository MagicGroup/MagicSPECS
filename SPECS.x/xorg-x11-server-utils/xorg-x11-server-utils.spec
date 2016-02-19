%define pkgname server-utils
# doesn't work yet, needs more nickle bindings
%define with_xkeystone 0

Summary: X.Org X11 X server utilities
Summary(zh_CN.UTF-8): X.Org X11 X 服务器工具
Name: xorg-x11-%{pkgname}
Version: 7.5
Release: 14%{?dist}
License: MIT
Group: User Interface/X
Group(zh_CN.UTF-8): 用户界面/X
URL: http://www.x.org

Source0:  http://www.x.org/pub/individual/app/iceauth-1.0.7.tar.bz2
Source2:  http://www.x.org/pub/individual/app/rgb-1.0.6.tar.bz2
Source3:  http://www.x.org/pub/individual/app/sessreg-1.1.0.tar.bz2
Source5:  http://www.x.org/pub/individual/app/xgamma-1.0.6.tar.bz2
Source6:  http://www.x.org/pub/individual/app/xhost-1.0.7.tar.bz2
Source7:  http://www.x.org/pub/individual/app/xmodmap-1.0.9.tar.bz2
Source8:  http://www.x.org/pub/individual/app/xrandr-1.4.3.tar.bz2
Source9:  http://www.x.org/pub/individual/app/xrdb-1.1.0.tar.bz2
Source10: http://www.x.org/pub/individual/app/xrefresh-1.0.5.tar.bz2
Source11: http://www.x.org/pub/individual/app/xset-1.2.3.tar.bz2
Source12: http://www.x.org/pub/individual/app/xsetmode-1.0.0.tar.bz2
Source13: http://www.x.org/pub/individual/app/xsetpointer-1.0.1.tar.bz2
Source14: http://www.x.org/pub/individual/app/xsetroot-1.1.1.tar.bz2
Source15: http://www.x.org/pub/individual/app/xstdcmap-1.0.3.tar.bz2
Source16: http://www.x.org/pub/individual/app/xkill-1.0.4.tar.bz2
Source17: http://www.x.org/pub/individual/app/xinput-1.6.2.tar.bz2

# NOTE: Each upstream tarball has its own "PatchN" section, taken from
# multiplying the "SourceN" line times 100.  Please keep them in this
# order.  Also, please keep each patch specific to a single upstream tarball,
# so that they don't have to be split in half when submitting upstream.
#
# iceauth section
#Patch0: 

Patch0: sessreg-gcc5.patch

BuildRequires: xorg-x11-util-macros

BuildRequires: pkgconfig(xmu) pkgconfig(xext) pkgconfig(xrandr)
BuildRequires: pkgconfig(xxf86vm) pkgconfig(xrender) pkgconfig(xi)
BuildRequires: pkgconfig(xt) pkgconfig(xpm) pkgconfig(xxf86misc)
# xsetroot requires xbitmaps-devel (which was renamed now)
BuildRequires: xorg-x11-xbitmaps
# xsetroot
BuildRequires: libXcursor-devel

# xrdb, sigh
Requires: mcpp
# older -apps had xinput and xkill, moved them here because they're
# a) universally useful and b) don't require Xaw
Conflicts: xorg-x11-apps < 7.6-4

Provides: iceauth rgb sessreg xgamma xhost
Provides: xmodmap xrandr xrdb xrefresh xset xsetmode xsetpointer
Provides: xsetroot xstdcmap xinput xkill

%description
A collection of utilities used to tweak and query the runtime configuration
of the X server.

%if %{with_xkeystone}
%package -n xkeystone
Summary: X display keystone correction
Group: User Interface/X
Requires: nickle

%description -n xkeystone
Utility to perform keystone adjustments on X screens.
%endif

%prep
%setup -q -c %{name}-%{version} -a2 -a3 -a5 -a6 -a7 -a8 -a9 -a10 -a11 -a12 -a13 -a14 -a15 -a16 -a17
%patch0 -p1

%build

# Build all apps
{
   for app in * ; do
      pushd $app
      case $app in
         rgb-*)
            # FIXME: run autotools junk to kick in our patch
            #aclocal --force
            #automake -f
            #autoconf
            %configure ;# --with-rgb-db=%{_datadir}/X11
            ;;
	 xset-*)
	    # FIXME: run autotools junk to kick in our patch
	    #aclocal --force
	    #automake -f
	    #autoconf
	    %configure
	    ;;
         *)
            %configure --with-cpp=/usr/bin/mcpp
            ;;
      esac

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
      case $app in
         *)
            make install DESTDIR=$RPM_BUILD_ROOT
            ;;
      esac
      popd
   done
}
%if !%{with_xkeystone}
rm -f $RPM_BUILD_ROOT/usr/bin/xkeystone
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc
%{_bindir}/iceauth
%{_bindir}/sessreg
%{_bindir}/showrgb
%{_bindir}/xgamma
%{_bindir}/xhost
%{_bindir}/xinput
%{_bindir}/xkill
%{_bindir}/xmodmap
%{_bindir}/xrandr
%{_bindir}/xrdb
%{_bindir}/xrefresh
%{_bindir}/xset
%{_bindir}/xsetmode
%{_bindir}/xsetpointer
%{_bindir}/xsetroot
%{_bindir}/xstdcmap
%{_datadir}/X11/rgb.txt
%{_mandir}/man1/iceauth.1*
%{_mandir}/man1/sessreg.1*
%{_mandir}/man1/showrgb.1*
%{_mandir}/man1/xgamma.1*
%{_mandir}/man1/xhost.1*
%{_mandir}/man1/xinput.1*
%{_mandir}/man1/xkill.1*
%{_mandir}/man1/xmodmap.1*
%{_mandir}/man1/xrandr.1*
%{_mandir}/man1/xrdb.1*
%{_mandir}/man1/xrefresh.1*
%{_mandir}/man1/xset.1*
%{_mandir}/man1/xsetmode.1*
%{_mandir}/man1/xsetpointer.1*
%{_mandir}/man1/xsetroot.1*
%{_mandir}/man1/xstdcmap.1*

%if %{with_xkeystone}
%files -n xkeystone
%defattr(-,root,root,-)
%{_bindir}/xkeystone
%endif

%changelog
* Sun Nov 15 2015 Liu Di <liudidi@gmail.com> - 7.5-14
- 为 Magic 3.0 重建

* Fri Nov 06 2015 Liu Di <liudidi@gmail.com> - 7.5-13
- 为 Magic 3.0 重建

* Tue Oct 27 2015 Liu Di <liudidi@gmail.com> - 7.5-12
- 为 Magic 3.0 重建

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 7.5-11
- 为 Magic 3.0 重建

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.5-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 22 2011 Peter Hutterer <peter.hutterer@redhat.com> 7.5-9
- xinput 1.5.4

* Thu Nov 10 2011 Adam Jackson <ajax@redhat.com> 7.5-8
- Move xinput and xkill here from xorg-x11-apps

* Mon Oct 10 2011 Matěj Cepl <mcepl@redhat.com> - 7.5-7
- Fix BuildRequires ... xbitmaps-devel does not exist anymore (RHBZ #744751)
- Upgrade to the latest upstream iceauth, rgb, sessreg, and xrandr

* Mon Aug 01 2011 Peter Hutterer <peter.hutterer@redhat.com> 7.5-6
- xset 1.2.2

* Wed Apr 06 2011 Dave Airlie <airlied@redhat.com> 7.5-5
- xrdb 1.0.9 (CVE-2011-0465)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Nov 12 2010 Peter Hutterer <peter.hutterer@redhat.com> 7.5-3
- xset 1.2.1
- xrefresh 1.0.4
- xgamma 1.0.4
- xrdb 1.0.7

* Mon Nov 01 2010 Peter Hutterer <peter.hutterer@redhat.com> 7.5-2
- xsetroot requires libXcursor-devel now

* Mon Nov 01 2010 Peter Hutterer <peter.hutterer@redhat.com> 7.5-1
- iceauth 1.0.4
- rgb 1.0.4
- xhost 1.0.4
- xmodmap 1.0.5
- xrandr 1.3.4
- xsetroot 1.1.0
- xstdcmap 1.0.2

* Fri Aug 06 2010 Peter Hutterer <peter.hutterer@redhat.com> 7.4-20
- xset 1.2.0

* Sun Jul 25 2010 Peter Hutterer <peter.hutterer@redhat.com> 7.4-19
- xrandr 1.3.3

* Tue Jul 20 2010 Peter Hutterer <peter.hutterer@redhat.com> 7.4-18
- xset 1.1.0

* Mon Jul 12 2010 Dan Horák <dan[at]danny.cz> - 7.4-17
- nothing is patched => don't run autotools (fixes problems with autoconf 2.66)

* Fri Mar 05 2010 Matěj Cepl <mcepl@redhat.com> - 7.4-16
- Fixed bad directory ownership of /usr/share/X11

* Mon Nov 09 2009 Adam Jackson <ajax@redhat.com> 7.4-15
- Also drop xcmsdb virtual Provide.

* Mon Oct 19 2009 Adam Jackson <ajax@redhat.com> 7.4-14
- Drop xcmsdb, no one uses XCMS.
- rgb 1.0.3
- xgamma 1.0.3
- xhost 1.0.3
- xrefresh 1.0.3
- xsetroot 1.0.3

* Tue Oct 13 2009 Adam Jackson <ajax@redhat.com> 7.4-13
- iceauth 1.0.3
- sessreg 1.0.5
- xmodmap 1.0.4
- xrdb 1.0.6

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 07 2009 Adam Jackson <ajax@redhat.com> 7.4-10
- xrandr 1.3.0

* Thu Jul 02 2009 Adam Jackson <ajax@redhat.com> 7.4-9
- Requires: mcpp instead of cpp, and switch xrdb to use it.

* Thu Jul 02 2009 Adam Jackson <ajax@redhat.com> 7.4-8
- Drop xvidtune, move it to -apps to isolate libXaw deps

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb 21 2009 Adam Jackson <ajax@redhat.com> 7.4-6
- Merge review cleanups. (#226644)

* Fri Feb 13 2009 Adam Jackson <ajax@redhat.com> 7.4-5
- Split xkeystone into a subpackage for nickle dependency.  Also, don't build
  it by default, since we don't have the cairo bindings packaged yet.

* Wed Feb 04 2009 Adam Jackson <ajax@redhat.com> 7.4-4
- xrandr 1.2.99.4

* Sun Jul 20 2008 Adam Jackson <ajax@redhat.com> 7.4-3
- Drop libXfontcache buildreq, it's gone gone gone.
- Use http URLs for Source: lines.
- sessreg-1.0.4
- xhost-1.0.2
- xrandr-1.2.3
- xrdb-1.0.5
- xset-1.0.4
- xsetpointer-1.0.1

* Tue Jul 15 2008 Adam Jackson <ajax@redhat.com> 7.4-2
- Fix license tag.

* Mon Jun 30 2008 Adam Jackson <ajax@redhat.com> 7.4-1
- Drop xtrap utils, it's deprecated upstream.

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 7.3-3
- Autorebuild for GCC 4.3

* Thu Nov 29 2007 Dave Airlie <airlied@redhat.com> 7.3-2
- xrandr-1.2.2-reset-other-outputs-using-best-crtc.patch
- xrandr-1.2.2-verify-crtc-against-prev-config.patch
- Patches from upstream to fix some bug in xrandr app

* Mon Sep 24 2007 Adam Jackson <ajax@redhat.com> 7.3-1
- sessreg 1.0.3
- xgamma 1.0.2
- xmodmap 1.0.3
- xrdb 1.0.4
- xset 1.0.3
- xsetroot 1.0.2
- Bump to 7.3

* Thu Aug 23 2007 Adam Jackson <ajax@redhat.com> - 7.2-6
- Rebuild for ppc toolchain bug

* Wed Jul 25 2007 Jeremy Katz <katzj@redhat.com> - 7.2-5
- rebuild for toolchain bug

* Tue Jul 24 2007 Adam Jackson <ajax@redhat.com> 7.2-4
- iceauth 1.0.2

* Wed Jul 11 2007 Adam Jackson <ajax@redhat.com> 7.2-3
- xrandr 1.2.2

* Wed Jun 27 2007 Adam Jackson <ajax@redhat.com> 7.2-2
- xrandr 1.2.1

* Wed Feb 28 2007 Adam Jackson <ajax@redhat.com> 7.2-1
- Superstition bump to 7.2
- xrandr 1.2.0

* Tue Jan 30 2007 Adam Jackson <ajax@redhat.com> 7.1-5
- Fix man page globs and rebuild for FC7.

* Fri Aug  4 2006 Adam Jackson <ajackson@redhat.com> 7.1-4.fc6
- xvidtune-1.0.1-buffer-stomp.patch: Fix a heap smash. (#189146)

* Wed Jul 19 2006 Mike A. Harris <mharris@redhat.com> 7.1-3.fc6
- Remove app-defaults dir from file manifest, as it is owned by libXt (#174021)
- Add 'dist' tag to package release string.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> 7.1-2.1
- rebuild

- Update to rgb-1.0.2 from X11R7.1

* Wed Jun 21 2006 Mike A. Harris <mharris@redhat.com> 7.1-1
- Bump the package version to 7.1 to have it match the X11 release that the
  tarballs came from going forward.
- Update to xrefresh-1.0.2, xtrap-1.0.2 from X11R7.1
- Remove build dependency on liblbxutil-devel, as LBX is no longer supported.

* Mon Jun 05 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-6
- Clean up Source lines in spec file, and other minor cleanups.

* Wed May 17 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-5
- Added a whackload of BuildRequires for bug (#191987)

* Thu Apr 27 2006 Adam Jackson <ajackson@redhat.com> 1.0.1-4
- Updated xmodmap, xrandr, xrdb, and xset.

* Tue Apr 25 2006 Adam Jackson <ajackson@redhat.com> 1.0.1-3
- Eliminate a spurious Xprint dependency from xset.

* Fri Apr 14 2006 Adam Jackson <ajackson@redhat.com> 1.0.1-2
- Drop lbxproxy, LBX is deprecated upstream
- Update to xhost 1.0.1

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> 1.0.1-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> 1.0.1-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan 18 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-1
- Updated all packages to the versions from X11R7.0

* Mon Nov 28 2005 Mike A. Harris <mharris@redhat.com> 1.0.0-1
- Updated all packages to version 1.0.0 from X11R7 RC4
- Changed manpage dirs from man1x to man1 to match upstream RC4 default.
- Updated lbxproxy-datadir-AtomControl-fix.patch
- Updated rgb-1.0.0-datadir-rgbpath-fix.patch
- Removed xvidtune-0.99.1-datadir-app-defaults-fix.patch, now unneeded.

* Mon Nov 28 2005 Mike A. Harris <mharris@redhat.com> 0.99.2-6
- Added "Requires: cpp" as xrdb requires it for proper operation (#174302)

* Wed Nov 22 2005 Mike A. Harris <mharris@redhat.com> 0.99.2-5
- Bump "filesystem" Requires(pre) to 2.3.7-1.

* Fri Nov 18 2005 Mike A. Harris <mharris@redhat.com> 0.99.2-4
- Added lbxproxy-0.99.2-datadir-AtomControl-fix.patch to move architecture
  independent data files from libdir to datadir.
- Added rgb-0.99.2-datadir-rgbpath-fix.patch to move architecture independent
  data files from libdir to datadir.
- Added xvidtune-0.99.1-datadir-app-defaults-fix.patch to move app-defaults
  into datadir.

* Mon Nov 14 2005 Jeremy Katz <katzj@redhat.com> 0.99.2-3
- require newer filesystem package (#172610)

* Sun Nov 13 2005 Mike A. Harris <mharris@redhat.com> 0.99.2-2
- Added "Obsoletes: XFree86, xorg-x11", as these utilities came from there.
- Rebuild against new libXaw 0.99.2-2, which has fixed DT_SONAME. (#173027)

* Fri Nov 11 2005 Mike A. Harris <mharris@redhat.com> 0.99.2-1
- Initial build, with all apps taken from X11R7 RC2
- Use "make install DESTDIR=$RPM_BUILD_ROOT" as the makeinstall macro fails on
  some packages.
