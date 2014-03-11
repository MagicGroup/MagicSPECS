Summary: X.Org X11 xfs font server
Name: xorg-x11-xfs
Version: 1.1.2
Release: 2%{?dist}
# NOTE: Remove Epoch line if package gets renamed
Epoch: 1
License: MIT
Group: System Environment/Daemons
URL: http://www.x.org

Source0: http://ftp.nara.wide.ad.jp/pub/X11/x.org/individual/app/xfs-%{version}.tar.bz2
Source1: http://ftp.nara.wide.ad.jp/pub/X11/x.org/individual/app/xfsinfo-1.0.3.tar.bz2
Source2: http://ftp.nara.wide.ad.jp/pub/X11/x.org/individual/app/fslsfonts-1.0.3.tar.bz2
Source3: http://ftp.nara.wide.ad.jp/pub/X11/x.org/individual/app/fstobdf-1.0.4.tar.bz2
Source4: http://ftp.nara.wide.ad.jp/pub/X11/x.org/individual/app/showfont-1.0.3.tar.bz2
Source10:  xfs.init
Source11:  xfs.config

BuildRequires: pkgconfig
# xfs needs 'fontsproto' to build, as indicated by ./configure
BuildRequires: xorg-x11-proto-devel
# FIXME: xfs needs xtrans to build, but autotools doesn't detect it missing
BuildRequires: xorg-x11-xtrans-devel
BuildRequires: libFS-devel
BuildRequires: libXfont-devel
BuildRequires: libX11-devel
# FIXME: xfs needs freetype-devel to build, but autotools doesn't detect it missing
BuildRequires: freetype-devel
BuildRequires: libfontenc-devel

# Make sure libXfont provides the catalogue FPE.
Requires: libXfont >= 1.2.9

Provides: xfs

Requires(pre): /sbin/nologin, /usr/sbin/useradd
Requires(post): /sbin/chkconfig, grep, sed, coreutils
Requires(preun): /sbin/service, /sbin/chkconfig
Requires(postun): /sbin/service

# xfs initscript runtime dependencies
Requires: initscripts, fontconfig, sed, /usr/bin/find
Requires: /bin/sort, /usr/bin/uniq
Requires: mkfontdir, mkfontscale, ttmkfdir
# end of xfs initscript runtime dependencies

%description
X.Org X11 xfs font server

%package utils
Summary: X.Org X11 font server utilities
Group: User Interface/X
#Requires: %{name} = %{version}-%{release}

%description utils
X.Org X11 font server utilities

%prep
%setup -q -c %{name}-%{version} -a1 -a2 -a3 -a4

%build
# Build xfs
{
   pushd xfs-*
   %configure 
   # FIXME: Create patch for the following, and submit it upstream.
   # <daniels> mharris: uhm, just set configdir=$(sysconfdir) in Makefile.am
   # <mharris> daniels: Do you mean, change it in Makefile.am, and submit patch to fix?  Or patch it for local use?
   # <daniels> mharris: and submit patch to fix, yeah
   make configdir=%{_sysconfdir}/X11/fs
# CFLAGS='-DDEFAULT_CONFIG_FILE="/etc/X11/fs/config"'
   popd
}

for pkg in xfsinfo fslsfonts fstobdf showfont ; do
   pushd ${pkg}-*
   %configure
   make
   popd
done

%install
rm -rf $RPM_BUILD_ROOT
# Install xfs
{
   pushd xfs-*
   # FIXME: Create patch for the following, and submit it upstream.
   # <daniels> mharris: uhm, just set configdir=$(sysconfdir) in Makefile.am
   # <mharris> daniels: Do you mean, change it in Makefile.am, and submit patch to fix?  Or patch it for local use?
   # <daniels> mharris: and submit patch to fix, yeah
   %makeinstall configdir=$RPM_BUILD_ROOT%{_sysconfdir}/X11/fs
   popd
}

for pkg in xfsinfo fslsfonts fstobdf showfont ; do
   pushd ${pkg}-*
   make install DESTDIR=$RPM_BUILD_ROOT
   popd
done

# Install the Red Hat xfs config file and initscript
{
   mkdir -p $RPM_BUILD_ROOT/etc/{X11/fs,rc.d/init.d}
   install -c -m 755 %{SOURCE10} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/xfs
   install -c -m 644 %{SOURCE11} $RPM_BUILD_ROOT%{_sysconfdir}/X11/fs/config
}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
{
  /usr/sbin/useradd -c "X Font Server" -r -s /sbin/nologin -u 43 -d /etc/X11/fs xfs || :
} &> /dev/null || : # Silence output, and ignore errors (Bug #91822)

%post
{
  # Install section
  /sbin/chkconfig --add xfs
  #------------------------------------------------------------------------
  # Upgrade section
  if [ "$1" -gt "1" ] ; then
    XORG_CONFIG=/etc/X11/xorg.conf
    XFSCONFIG=/etc/X11/fs/config

    # XFS config file upgrade munging
    if [ -f $XFSCONFIG ] ; then
      # Remove Speedo font directories from xfs config if present to avoid
      # bug reports about xfs complaining about empty directories in syslog.
      perl -p -i -e 's#^.*/.*/Speedo.*\n##' $XFSCONFIG
    fi
  fi ; # End Upgrade section
}

%preun
{
  if [ "$1" = "0" ]; then
    /sbin/service xfs stop &> /dev/null || :
# FIXME: The chkconfig call below works properly if uninstalling the package,
#        but it will cause xfs to be de-chkconfig'd if upgrading from one X11
#        implementation to another, as witnessed in the transition from
#        XFree86 to Xorg X11.  If this call is removed however, then xfs will
#        remain visible in ntsysv and similar utilities even after xfs is
#        uninstalled from the system in non-upgrade scenarios.  Not sure how
#        to fix this yet.
    /sbin/chkconfig --del xfs || :
# userdel/groupdel removed because they cause the user/group to get destroyed
# when upgrading from one X11 implementation to another, ie: XFree86 -> Xorg
#    /usr/sbin/userdel xfs 2>/dev/null || :
#    /usr/sbin/groupdel xfs 2>/dev/null || :
  fi
}

%postun
{
  if [ "$1" -gt "1" ]; then
    /sbin/service xfs condrestart &> /dev/null || :
  fi
}

%files
%defattr(-,root,root,-)
%doc xfs-%{version}/COPYING
%{_bindir}/xfs
%dir %{_sysconfdir}/X11/fs
# NOTE: We intentionally override the upstream default config file location
# during build.
# FIXME: Create patch for the following, and submit it upstream.
# Check if this is still relevent:  set configdir=$(sysconfdir) in Makefile.am
# and if so, submit patch upstream to fix.
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/X11/fs/config
#%dir %{_mandir}/man1x
# FIXME: The manpage incorrectly points to /usr/X11R6/...
%{_mandir}/man1/xfs.1*
%{_sysconfdir}/rc.d/init.d/xfs

%files utils
%defattr(-,root,root,-)
# cheating
%doc xfs-%{version}/COPYING
%{_bindir}/fslsfonts
%{_bindir}/fstobdf
%{_bindir}/showfont
%{_bindir}/xfsinfo
#%dir %{_mandir}/man1x
%{_mandir}/man1/fslsfonts.1*
%{_mandir}/man1/fstobdf.1*
%{_mandir}/man1/showfont.1*
%{_mandir}/man1/xfsinfo.1*

%changelog
* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Mar 23 2012 Adam Jackson <ajax@redhat.com> 1.1.2-1
- xfs 1.1.2

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 05 2011 Adam Jackson <ajax@redhat.com> 1.1.1-3
- xfs.init: Redact calls to chkfontpath (#665746)
- Remove some monolith-to-modular upgrade path leftovers

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Nov 02 2010 Peter Hutterer <peter.hutterer@redhat.com> 1:1.1.1-1
- xfs 1.1.1
- xfsinfo 1.0.3
- fslsfonts 1.0.3
- fstobdf 1.0.4
- showfont 1.0.3

* Thu Jul 08 2010 Adam Jackson <ajax@redhat.com> 1:1.0.5-8
- Install a COPYING for -utils too
- Remove some XFree86 compat oh my goodness how was that still there.

* Fri Mar 05 2010 Matěj Cepl <mcepl@redhat.com> - 1:1.0.5-7
- Fixed bad directory ownership of /etc/X11

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.0.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Apr 13 2009 Adam Jackson <ajax@redhat.com> 1.0.5-5
- xfs.init: Fix mkdir race (#492517)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.0.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jul 15 2008 Adam Jackson <ajax@redhat.com> 1.0.5-3
- Fix license tag.

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1:1.0.5-2
- Autorebuild for GCC 4.3

* Tue Oct 02 2007 Adam Jackson <ajax@redhat.com> 1:1.0.5-1
- xfs 1.0.5

* Thu Aug 23 2007 Adam Jackson <ajax@redhat.com> - 1:1.0.4-2
- Rebuild for ppc toolchain bug

* Fri Jul 27 2007 Bill Nottingham <notting@redhat.com> - 1:1.0.4-2
- don't run by default any more, as it's not used by default
- remove explicit restorecon dependency (#215142)

* Fri Jun 22 2007 Kristian Høgsberg <krh@hinata.boston.redhat.com> - 1:1.0.4-1
- Require catalogue capable libXfont.
- Drop xfs.config.in, just use catalogue font path.
- Stop xorg.conf munging madness.

* Sat Apr 21 2007 Matthias Clasen <mclasen@redhat.com> - 1:1.0.2-4
- Don't install INSTALL

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1:1.0.2-3.1
- rebuild

* Wed Jun 21 2006 Mike A. Harris <mharris@redhat.com> 1:1.0.2-3
- Added xfs documentation to doc macro.
- Use "make install" instead of makeinstall macro.
- Clean up source file URLs.

* Tue May 30 2006 Adam Jackson <ajackson@redhat.com> 1:1.0.2-2
- Fix BuildRequires (#191856).

* Thu Apr 27 2006 Adam Jackson <ajackson@redhat.com> 1:1.0.2-1
- Update xfs and fstobdf

* Wed Mar 01 2006 Mike A. Harris <mharris@redhat.com> 1:1.0.1-4
- Fix all rpm scriptlets "upgrade" tests to only execute on upgrades.

* Sat Feb 25 2006 Mike A. Harris <mharris@redhat.com> 1:1.0.1-3
- Redirect output of "rm -rf fonts.dir" to /dev/null in xfs.init

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> 1:1.0.1-2.1
- bump again for double-long bug on ppc(64)

* Thu Feb 09 2006 Mike A. Harris <mharris@redhat.com> 1:1.0.1-2
- Removed invocation of fc-cache from xfs initscript for bug (#179362)
- Redirect stderr to /dev/null to squelch an unwanted error xfs.init (#155349)
- Replace "s#^/.*:[a-z]*$##g" with "s#:unscaled$##g" in xfs.init for (#179491)
- Cosmetic cleanups to spec file to satiate the banshees.

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> 1:1.0.1-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan 16 2006 Mike A. Harris <mharris@redhat.com> 1:1.0.1-1
- Updated all tarballs to version 1.0.1 from X11R7.0

* Tue Jan 10 2006 Bill Nottingham <notting@redhat.com> 1:1.0.0-2
- fix rpm post script (#176009, <ville.skytta@iki.fi>)

* Fri Dec 16 2005 Mike A. Harris <mharris@redhat.com> 1:1.0.0-1
- Updated all tarballs to version 1.0.0 from X11R7 RC4.
- Get default X font directory with font-utils package 'fontdir' pkgconfig
  variable.
- Change manpage dir from man1x back to man1 to match upstream.

* Tue Nov 15 2005 Jeremy Katz <katzj@redhat.com> 1:0.99.2-4
- require initscripts instead of /etc/init.d/functions

* Tue Nov 15 2005 Mike A. Harris <mharris@redhat.com> 0.99.2-3
- Updated xfs pre script to check for the existance of the old monolithic
  /usr/X11R6/lib/X11/fs/config xfs config file, and set a migration flag
  file.
- Updated xfs.init to check for the existance of the migration flag file,
  and perform an xfs 'restart' instead of a 'reload' if migrating.  Users
  will now have to restart their X server, or reconnect the xfs server to
  the X server after a migration to modular X.
- Changed upgrade comparison typo from 2 to 1 in xfs post script.

* Mon Nov 14 2005 Mike A. Harris <mharris@redhat.com> 0.99.2-2
- Added temporary "BuildRequires: libXfont-devel >= 0.99.2-3" and
  "Requires: libXfont-devel >= 0.99.2-3" to ensure early-testers of
  pre-rawhide modular X have installed the work around for (#172997).

* Fri Nov 11 2005 Mike A. Harris <mharris@redhat.com> 0.99.2-1
- Updated to xfs-0.99.2 and fstobdf-0.99.2 from X11R7 RC2
- Added Epoch 1 to package, and set the version number to the xfs 0.99.2
  version.

* Thu Nov 10 2005 Mike A. Harris <mharris@redhat.com> 6.99.99.901-2
- Added showfont-0.99.1 from X11R7 RC1 release.

* Wed Nov 09 2005 Mike A. Harris <mharris@redhat.com> 6.99.99.901-1
- Updated all packages to version 0.99.1 from X11R7 RC1.
- Bump package version to 6.99.99.901 (the RC1 CVS tag).
- Change manpage location to 'man1x' in file manifest.
- Converted xfs.config to xfs.config.in, and added code to spec file to
  generate xfs.config depending on what the system _x11fontdir is.
- Complete and total rewrite of xfs postinstall script to use "sed -i"
  and complete restructuring, which removed a lot of the super craptasticness
  that had been sitting there for years.

* Wed Oct 03 2005 Mike A. Harris <mharris@redhat.com> 6.99.99.0-4
- Use Fedora-Extras style BuildRoot tag
- Update BuildRequires to use new library package names
- Remove unnecessary BuildRequires on 'install', and fix pkgconfig dep

* Thu Aug 25 2005 Mike A. Harris <mharris@redhat.com> 6.99.99.0-3
- Install the initscript and xfs config file in the correct location as they
  were inadvertently interchanged in previous builds.

* Wed Aug 24 2005 Mike A. Harris <mharris@redhat.com> 6.99.99.0-2
- Ported the xfs related rpm scripts over from monolithic packaging, and
  added up to date Requires(*) dependencies for all of them.
- Flagged xfs config file as config(noreplace)
- Added build and runtime dependencies to xfs subpackage as best as could be
  determined by analyzing ./configure output, and building in minimalized
  build root environment.

* Wed Aug 24 2005 Mike A. Harris <mharris@redhat.com> 6.99.99.0-1
- Initial build.
