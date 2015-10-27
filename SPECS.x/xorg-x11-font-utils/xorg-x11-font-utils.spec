%define pkgname font-utils
%define mkfontscale 1.1.2

Summary: X.Org X11 font utilities
Summary(zh_CN.UTF-8): X.Org X11 字体工具
Name: xorg-x11-%{pkgname}
# IMPORTANT: If package ever gets renamed to something else, remove the Epoch line!
Epoch: 1
Version: 7.7
Release: 3%{?dist}
License: MIT
Group: User Interface/X
URL: http://www.x.org

Source0: http://ftp.nara.wide.ad.jp/pub/X11/x.org/individual/app/bdftopcf-1.0.5.tar.bz2
Source1: http://ftp.nara.wide.ad.jp/pub/X11/x.org/individual/app/fonttosfnt-1.0.4.tar.bz2
Source2: http://ftp.nara.wide.ad.jp/pub/X11/x.org/individual/app/mkfontdir-1.0.7.tar.bz2
Source3: http://ftp.nara.wide.ad.jp/pub/X11/x.org/individual/app/mkfontscale-%{mkfontscale}.tar.bz2
Source4: http://ftp.nara.wide.ad.jp/pub/X11/x.org/individual/font/font-util-1.3.1.tar.bz2
# helper script used in %post for xorg-x11-fonts
Source5: xorg-x11-fonts-update-dirs

Patch0: font-util-1.0.1-mapdir-use-datadir-fix.patch
Patch1: font-util-1.0.1-autoconf-add-with-fontdir-option.patch
Patch2: mkfontscale-examine-all-encodings.patch

BuildRequires: pkgconfig(xfont) pkgconfig(x11)
BuildRequires: libfontenc-devel >= 0.99.2-2
BuildRequires: freetype-devel
BuildRequires: zlib-devel
BuildRequires: autoconf

Provides: %{pkgname}
Provides: bdftopcf, fonttosfnt, mkfontdir, mkfontscale, ucs2any

%description
X.Org X11 font utilities required for font installation, conversion,
and generation.

%package -n bdftruncate
Summary: Generate truncated BDF font from ISO 10646-1 encoded BDF font
Group:   Applications/System

%description -n bdftruncate
bdftruncate allows one to generate from an ISO10646-1 encoded BDF font
other ISO10646-1 BDF fonts in which all characters above a threshold
code value are stored unencoded. This is often desirable because the
Xlib API and X11 protocol data structures used for representing font
metric information are extremely inefficient when handling sparsely
populated fonts.

%prep
%setup -q -c %{name}-%{version} -a1 -a2 -a3 -a4
#patch0 -p0 -b .font-util-mapdir-use-datadir-fix
#patch1 -p0 -b .autoconf-add-with-fontdir-option
oldpwd=$(pwd)
cd mkfontscale-%{mkfontscale}
#%patch2 -p1 -b .all-encodings
cd ${oldpwd}

%build
# Build all apps
{
   for app in bdftopcf fonttosfnt mkfontdir mkfontscale font-util ; do
      oldpwd=$(pwd)
      cd $app-*
      # FIXME: We run autoconf to activate font-util-0.99.1-mapdir-use-datadir-fix.patch
      case $app in
         font-util)
            autoconf
            ;;
      esac
      # this --with-mapdir should be redundant?
      %configure --with-mapdir=%{_datadir}/X11/fonts/util
      make
      cd ${oldpwd}
   done
}

%install
rm -rf $RPM_BUILD_ROOT
# Install all apps
{
    for app in bdftopcf fonttosfnt mkfontdir mkfontscale font-util; do
		oldpwd=$(pwd)
		cd $app-*
		make install DESTDIR=$RPM_BUILD_ROOT
		cd ${oldpwd}
	done
	for i in */README ; do
		[ -s $i ] && cp $i README-$(echo $i | sed 's/-[0-9].*//')
	done
	for i in */COPYING ; do
		grep -q stub $i || cp $i COPYING-$(echo $i | sed 's/-[0-9].*//')
	done

    # bdftruncate is part of font-util
    cp font-util-*/COPYING COPYING-bdftruncate
}

install -m 744 %{SOURCE5} ${RPM_BUILD_ROOT}%{_bindir}/xorg-x11-fonts-update-dirs
sed -i "s:@DATADIR@:%{_datadir}:" ${RPM_BUILD_ROOT}%{_bindir}/xorg-x11-fonts-update-dirs
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc README-* COPYING-bdftopcf COPYING-[c-z]*
%{_bindir}/bdftopcf
%{_bindir}/fonttosfnt
%{_bindir}/mkfontdir
%{_bindir}/mkfontscale
%{_bindir}/ucs2any
%{_bindir}/xorg-x11-fonts-update-dirs
%dir %{_datadir}/X11/fonts
%dir %{_datadir}/X11/fonts/util
%{_datadir}/X11/fonts/util/map-*
%{_datadir}/aclocal/fontutil.m4
%{_libdir}/pkgconfig/fontutil.pc
%{_mandir}/man1/bdftopcf.1*
%{_mandir}/man1/fonttosfnt.1*
%{_mandir}/man1/mkfontdir.1*
%{_mandir}/man1/mkfontscale.1*
%{_mandir}/man1/ucs2any.1*

%files -n bdftruncate
%defattr(-,root,root,-)
%doc COPYING-bdftruncate
%{_bindir}/bdftruncate
%{_mandir}/man1/bdftruncate.1*


%changelog
* Tue Oct 27 2015 Liu Di <liudidi@gmail.com> - 1:7.7-3
- 为 Magic 3.0 重建

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 1:7.7-2
- 为 Magic 3.0 重建

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:7.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:7.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Matěj Cepl <mcepl@redhat.com> - 1:7.5-5
- pushd/popd are slightly evil, removing (#664701, #664699)

* Wed Nov 24 2010 Peter Hutterer <peter.hutterer@redhat.com> 1:7.5-4
- Fix need_ttmkfdir test in xorg-x11-fonts-update-dirs script (#655925)

* Fri Nov 19 2010 Peter Hutterer <peter.hutterer@redhat.com> 1:7.5-3
- Add xorg-x11-fonts-update-dirs, a script to automake mkfontscale and
  friends as well as generate encodings directories during %post (used by
  xorg-x11-fonts). (#634039)

* Mon Nov 08 2010 Peter Hutterer <peter.hutterer@redhat.com> 1:7.5-2
- mkfontdir 1.0.6

* Mon Nov 01 2010 Peter Hutterer <peter.hutterer@redhat.com> 1:7.5-1
- font-util 1.2.0
- mkfontscale 1.0.8
- bdftopcf 1.0.3

* Tue Oct 05 2010 Peter Hutterer <peter.hutterer@redhat.com> 1:7.4-3
- font-util 1.1.2

* Fri Jul 09 2010 Peter Hutterer <peter.hutterer@redhat.com> 1:7.4-2
- Fix build for missing bdftruncate COPYING file.

* Thu Jul 08 2010 Adam Jackson <ajax@redhat.com> 7.4-1
- Install COPYING for bdftruncate too.

* Fri Apr 09 2010 Matěj Cepl <mcepl@redhat.com> - 1:7.2-12
- examine all platform=3 encodings (fixes #578460)

* Tue Nov 10 2009 Adam Jackson <ajax@redhat.com> 7.2-11
- font-util 1.1.0

* Tue Oct 13 2009 Adam Jackson <ajax@redhat.com> 7.2-10
- mkfontscale 1.0.7
- mkfontdir 1.0.5

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:7.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 23 2009 Adam Jackson <ajax@redhat.com> 7.2-8
- Un-require xorg-x11-filesystem
- Other general spec cleanup.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:7.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jul 15 2008 Adam Jackson <ajax@redhat.com> 7.2-6
- Fix license tag.

* Mon Jul 07 2008 Adam Jackson <ajax@redhat.com> 7.2-5
- Fix Source url for font-util.

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1:7.2-4
- Autorebuild for GCC 4.3

* Mon Dec 10 2007 Adam Jackson <ajax@redhat.com> 1:7.2-3
- Move bdftruncate (and its perl dependency) to a subpackage.
- %%doc for the non-empty READMEs and non-stub COPYINGs.

* Tue Aug 21 2007 Adam Jackson <ajax@redhat.com> - 1:7.2-2
- Rebuild for build id

* Thu Apr 26 2007 Adam Jackson <ajax@redhat.com> 1:7.2-1
- bdftopcf 1.0.1
- Superstition bump to 7.2-1

* Mon Mar 26 2007 Adam Jackson <ajax@redhat.com> 1:7.1-5
- mkfontdir 1.0.3

* Fri Jan 05 2007 Adam Jackson <ajax@redhat.com> 1:7.1-4.fc7
- fonttosfnt 1.0.3

* Thu Aug 17 2006 Adam Jackson <ajackson@redhat.com> 1:7.1-3
- Remove X11R6 symlinks.

* Fri Jul 14 2006 Adam Jackson <ajackson@redhat.com> 1:7.1-2
- Added fonttosfnt-1.0.1-freetype22-build-fix.patch to fix a build failure
  with new freetype 2.2.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1:7.1-1.1
- rebuild

* Wed Jun 21 2006 Mike A. Harris <mharris@redhat.com> 1:7.1-1
- Update to font-util-1.0.1 from X11R7.1
- Set package version to X11 release the tarballs are based from.

* Thu Apr 26 2006 Adam Jackson <ajackson@redhat.com> 1:1.0.2-2
- Update mkfontdir

* Wed Feb 22 2006 Mike A. Harris <mharris@redhat.com> 1:1.0.1-3
- Remove "Obsoletes: xorg-x11-font-utils" as the package should not obsolete
  itself.  Leftover from the original package template it seems.  (#182439)

* Fri Feb 17 2006 Mike A. Harris <mharris@redhat.com> 1:1.0.1-2
- Added with_X11R6_compat macro to conditionalize inclusion of mkfontdir and
  mkfontscale symlinks in the old X11R6 locations, pointing to the X11R7
  binaries.  This will provide backward compatibilty for Fedora Core 5, however
  3rd party developers and rpm package maintainers should update to using the
  new X11R7 locations immediately, as these compatibility links are temporary,
  and will be removed from a future OS release.
- Remove system directories from file manifest to appease the banshees.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> 1:1.0.1-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> 1:1.0.1-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan 18 2006 Mike A. Harris <mharris@redhat.com> 1:1.0.1-1
- Updated all utilities to the versions shipped in X11R7.0.

* Thu Dec 15 2005 Mike A. Harris <mharris@redhat.com> 1:1.0.0-1
- Updated all utilities to version 1.0.0 from X11R7 RC4.
- Updated font-util-1.0.0-mapdir-use-datadir-fix.patch to work with RC4.
- Added font-util-1.0.0-autoconf-add-with-fontdir-option.patch to add a new
  variable "fontdir" to the fontutil.pc file which all of the font packages
  can autodetect and use instead of having to put manual fontdir overrides
  in every single rpm package.

* Tue Dec 13 2005 Mike A. Harris <mharris@redhat.com> 1:0.99.2-1
- Updated bdftopcf, fonttosfnt to version 0.99.3, and mkfontdir, mkfontscale,
  and font-util to version 0.99.2 from X11R7 RC3.
- Changed manpage dir from man1x back to man1 due to another upstream change.
- Added fontutil.m4 to file manifest.

* Tue Nov 22 2005 Mike A. Harris <mharris@redhat.com> 1:0.99.1-1
- Changed package version to 0.99.1 to match the upstream font-util tarball
  version, and added "Epoch: 1" to the package for upgrades.
- Added font-util-0.99.1-mapdir-use-datadir-fix.patch to fix the font-util
  mapfiles data to install into datadir instead of libdir (#173943)
- Added "Requires(pre): libfontenc >= 0.99.2-2" to force a version of
  libfontenc to be installed that fixes bug #173453, and to also force it
  to be installed before xorg-x11-font-utils in a multi-package rpm
  transaction, which will ensure that when font packages get installed
  during upgrades via anaconda or yum, that the right libfontenc is being
  used by mkfontscale/mkfontdir.
- Added ">= 0.99.2-2" to BuildRequires for libfontenc, as a convenience to
  people rebuilding xorg-x11-font-utils, as they'll need to install the new
  libfontenc now anyway before they can install the font-utils package.

* Mon Nov 14 2005 Jeremy Katz <katzj@redhat.com> 6.99.99.902-2
- require newer filesystem (#172610)

* Wed Nov 09 2005 Mike A. Harris <mharris@redhat.com> 6.99.99.902-1
- Updated bdftopcf, fonttosfnt, mkfontdir, mkfontscale to version 0.99.1 from
  X11R7 RC1.

* Wed Nov 09 2005 Mike A. Harris <mharris@redhat.com> 6.99.99.901-3
- Glob util/map-* files in file manifest.
- Added missing "Obsoletes: xorg-x11-font-utils".
- Added "BuildRequires: pkgconfig".

* Sun Nov 06 2005 Mike A. Harris <mharris@redhat.com> 6.99.99.901-2
- Added font-util-0.99.1 to package, from X11R7 RC1 release, which provides
  ucs2any, bdftruncate.

* Wed Oct 26 2005 Mike A. Harris <mharris@redhat.com> 6.99.99.901-1
- Updated bdftopcf, fonttosfnt, mkfontdir, mkfontscale to version 0.99.1 from
  X11R7 RC1.
- Bumped package version to 6.99.99.901, the X11R7 RC1 release version tag.
- Updated file manifest to to find the manpages in "man1x".

* Wed Aug 24 2005 Mike A. Harris <mharris@redhat.com> 6.99.99.0-1
- Initial build.
