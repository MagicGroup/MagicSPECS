%define app_defaults_dir %{_datadir}/X11/app-defaults

Summary: An X Window System tool for drawing basic vector graphics
Summary(zh_CN.UTF-8): 描绘基本向量图形的 X 窗口系统工具
Name: xfig
Version: 3.2.5
Release: 35.c%{?dist}
License: MIT
Group: Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
URL: http://www.xfig.org/
Source0: http://downloads.sourceforge.net/mcj/xfig.%{version}c.full.tar.gz
Source1: xfig-icons.tar.gz
Source2: xfig.desktop
Source3: xfig.sh

Patch0: xfig-3.2.5a-default-apps.patch
Patch1: xfig-3.2.5-Imakefile.patch
Patch2: xfig-3.2.5-disable-Xaw3d.patch
Patch3: xfig-3.2.5-urwfonts.patch
Patch4: 31_spelling.patch
Patch5: 33_pdfimport_mediabox.patch
# xfig_man.html is not in 3.2.5c tarball from some reason,
# but makefile still tries to install it
Patch6: 38_formatstring.patch
Patch7: 39_add_xfig_man_html.patch
Patch8: 40_fix_dash_list_for_different_styles.patch
Patch9: xfig-3.2.5-rhbz1046102.patch
patch10: xfig-3.2.5-libpng16.patch

BuildRequires: libjpeg-devel
BuildRequires: libpng-devel
BuildRequires: imake
BuildRequires: libICE-devel
BuildRequires: libSM-devel
BuildRequires: libX11-devel
BuildRequires: libXaw-devel
BuildRequires: libXext-devel
BuildRequires: libXi-devel
BuildRequires: libXmu-devel
BuildRequires: libXpm-devel
BuildRequires: libXt-devel
BuildRequires: Xaw3d-devel
BuildRequires: desktop-file-utils

Requires: %{name}-common = %{version}-%{release}
Provides: %{name}-executable = %{version}-%{release}
# Xaw3d used to be the one in a subpackage, now the plain Xaw version is
Obsoletes: %{name}-Xaw3d <= 3.2.5-7.fc8
Provides: %{name}-Xaw3d = %{version}-%{release}

%description
Xfig is an X Window System tool for creating basic vector graphics,
including bezier curves, lines, rulers and more.  The resulting
graphics can be saved, printed on PostScript printers or converted to
a variety of other formats (e.g., X11 bitmaps, Encapsulated
PostScript, LaTeX).

You should install xfig if you need a simple program to create vector
graphics.

%description -l zh_CN.UTF-8
描绘基本向量图形的 X 窗口系统工具。

%package plain
Summary:        Plain Xaw version of xfig
Summary(zh_CN.UTF-8): xfig 的朴素版本
Group:          Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
Requires:       %{name}-common = %{version}-%{release}
Provides:       %{name}-executable = %{version}-%{release}

%description plain
Plain Xaw version of xfig, an X Window System tool for creating basic vector
graphics, including bezier curves, lines, rulers and more. The normal xfig
package uses the more modern / prettier looking Xaw3d toolkit, whereas this
version uses the very basic Xaw toolkit. Unless you really know you want this
version you probably don't want this version.

%description plain -l zh_CN.UTF-8
%{name} 的朴素版本。

%package common
Summary:        Common xfig files
Summary(zh_CN.UTF-8): %{name} 的公用文件
Group:          Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
Requires:       transfig >= 1:3.2.5, xdg-utils, enchant, urw-fonts
Requires:       hicolor-icon-theme
Requires:       xorg-x11-fonts-base
# So that this will get uninstalled together with xfig / xfig-Xaw3d
Requires:       %{name}-executable = %{version}-%{release}
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils

%description common
Files common to both the plain Xaw and the Xaw3d version of xfig.
%description common -l zh_CN.UTF-8
%{name} 的公用文件。

%prep
%setup -q -n xfig.%{version}c -a 1
%patch0 -p1
%patch1 -p1
%patch2 -p1 -b .with-Xaw3d
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
iconv -f ISO-8859-1 -t UTF8 CHANGES > tmp; touch -r CHANGES tmp; mv tmp CHANGES
rm Doc/html/images/sav1a0.tmp
chmod -x `find -type f`


%build
# First build the normal Xaw version
xmkmf
# make sure cmdline option parsing still works despite us renaming the binary
sed -i 's/"xfig"/"xfig-plain"/' main.c
make CDEBUGFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE -D_DEFAULT_SOURCE -fno-strength-reduce -fno-strict-aliasing"
mv xfig xfig-plain
make distclean

# And then build the Xaw3d version
mv Imakefile.with-Xaw3d Imakefile
xmkmf
# make sure cmdline option parsing still works despite us renaming the binary
sed -i 's/"xfig-plain"/"xfig-Xaw3d"/' main.c
make CDEBUGFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE -D_DEFAULT_SOURCE -fno-strength-reduce -fno-strict-aliasing"


%install
rm -rf %{buildroot}
make DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p" install.all
install -p -m 644 CHANGES README LATEX.AND.XFIG* FIGAPPS \
  $RPM_BUILD_ROOT%{_docdir}/%{name}

# remove the map generation scripts, these are for xfig developers only
rm $RPM_BUILD_ROOT%{_datadir}/%{name}/Libraries/Maps/{USA,Canada}/assemble
# remove app-defaults symlink which gets installed
rm $RPM_BUILD_ROOT%{_prefix}/lib*/X11/app-defaults

# install both Xaw and Xaw3d versions and the wrapper for the .desktop file
mv $RPM_BUILD_ROOT%{_bindir}/%{name} $RPM_BUILD_ROOT%{_bindir}/%{name}-Xaw3d
install -p -m 755 %{SOURCE3} $RPM_BUILD_ROOT%{_bindir}/%{name}
install -m 755 %{name}-plain $RPM_BUILD_ROOT%{_bindir}

install -D -p -m 644 %{name}16x16.xpm \
  $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/16x16/apps/%{name}.xpm
install -D -p -m 644 %{name}32x32.xpm \
  $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/32x32/apps/%{name}.xpm
install -D -p -m 644 %{name}64x64.xpm \
  $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/32x32/apps/%{name}.xpm

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
desktop-file-install          \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications %{SOURCE2}

%post common
update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
   %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%postun common
update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
   %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%files
%defattr(-,root,root,-)
%{_bindir}/%{name}-Xaw3d

%files plain
%defattr(-,root,root,-)
%{_bindir}/%{name}-plain

%files common
%defattr(-,root,root,-)
%doc %{_docdir}/%{name}
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_mandir}/*/*
%{app_defaults_dir}/*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/??x??/apps/%{name}.xpm


%changelog
* Sat Nov 14 2015 Liu Di <liudidi@gmail.com> - 3.2.5-35.c
- 为 Magic 3.0 重建

* Fri Nov 06 2015 Liu Di <liudidi@gmail.com> - 3.2.5-34.c
- 为 Magic 3.0 重建

* Fri Oct 23 2015 Liu Di <liudidi@gmail.com> - 3.2.5-33.b
- 为 Magic 3.0 重建

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 3.2.5-32.b
- 为 Magic 3.0 重建

* Tue Nov 13 2012 Liu Di <liudidi@gmail.com> - 3.2.5-31.b
- 为 Magic 3.0 重建

* Sun Feb 26 2012 Orion Poplawski <orion@cora.nwra.com> - 3.2.5-30.b
- Rebuild with Xaw3d 1.6.1

* Tue Feb 14 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 3.2.5-29.b
- Add patch from Debian for libpng 1.5

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.5-28.b
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 3.2.5-27.b
- Rebuild for new libpng

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.5-26.b
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec  6 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.2.5-25.b
- Fix buffer overflow when opening malicious fig files

* Thu Nov 25 2010 Hans de Goede <hdegoede@redhat.com> 3.2.5-24.b
- Fix importing of eps files (#657290)

* Wed Sep 30 2009 Hans de Goede <hdegoede@redhat.com> 3.2.5-23.b
- New upstream 3.2.5b release
- Drop many merged patches

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.5-22.a
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jun 28 2009 Caolán McNamara <caolanm@redhat.com> 3.2.5-21.a
- Resolves: rhbz#506791 make xfig spellchecking work

* Wed Jun  3 2009 Hans de Goede <hdegoede@redhat.com> 3.2.5-20.a
- Fix eps preview (#503911)

* Wed Apr  8 2009 Hans de Goede <hdegoede@redhat.com> 3.2.5-19.a
- Fix crash when printing (#494193), thanks to Ian Dall for the patch

* Fri Mar 27 2009 Hans de Goede <hdegoede@redhat.com> 3.2.5-18.a
- Rebase to new upstream 3.2.5a release, this was made available to me by
  the Debian maintainer who is in contact with upstream, which appearantly
  is still somewhat alive (but not alive enough to put the tarbal on the
  homepage ??)

* Sun Mar 15 2009 Hans de Goede <hdegoede@redhat.com> 3.2.5-17
- Add various patches from Debian (doc updates, new figures in the lib,
  better fix for modepanel resizing)
- Do not crash when inserting a character from the charmap into a text string

* Sun Mar 15 2009 Hans de Goede <hdegoede@redhat.com> 3.2.5-16
- Fix Text size field inserts characters on left instead of right (#490257)
- Fix xfig-Xaw3d does not display messages in message panel (#490259)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.5-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Feb 22 2009 Hans de Goede <hdegoede@redhat.com> 3.2.5-14
- Add missing Requires: xorg-x11-fonts-base (#486701)

* Mon Nov 10 2008 Stepan Kasal <skasal@redhat.com> - 3.2.5-13
- fix the Obsoletes tag to <= 3.2.5-7.fc8, which is the last
  release with Xaw3d subpackage

* Tue Nov  4 2008 Hans de Goede <hdegoede@redhat.com> 3.2.5-12
- Various small specfile cleanups from merge review

* Mon Jul 14 2008 Ian Hutchinson <ihutch@mit.edu> 3.2.5-11
- Fix incorrect height of modepanel.

* Thu Apr  3 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 3.2.5-10
- Fix missing prototype compiler warnings

* Thu Feb 28 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 3.2.5-9
- Fix cmdline parsing (broken by renaming the binary) (bz 435097)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.2.5-8
- Autorebuild for GCC 4.3

* Wed Dec 12 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 3.2.5-7
- Fix xfig crashing when zooming in a lot (bz 420411)

* Sat Nov 17 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 3.2.5-6
- Put the Xaw3d version in the main xfig package, put the plain Xaw version
  in a -plain subpackage

* Fri Nov 16 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 3.2.5-5
- Also compile a version against Xaw3d instead of plain Xaw, available in the
  new xfig-Xaw3d package
- Various specfile cleanups for packaging guidelines compliance
- Remove spurious executable permissions on various files (bz 247424)
- Apply patch fixing problems with xfig not finding fonts (bz 210278)

* Thu Nov 15 2007 Than Ngo <than@redhat.com> 3.2.5-4
- fix #201992, xfig crashes in the edit function

* Thu Nov 15 2007 Than Ngo <than@redhat.com> 3.2.5-3
- fix #201992, xfig crashes in the edit function

* Fri Oct 05 2007 Than Ngo <than@redhat.com> - 3.2.5-2
- rh#313321, use xdg-open

* Mon Apr 16 2007 Than Ngo <than@redhat.com> - 3.2.5-1.fc7
- 3.2.5

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 3.2.4-21.1
- rebuild

* Tue May 16 2006 Than Ngo <than@redhat.com> 3.2.4-21
- fix #191816, Xaw3d build problem

* Fri May 05 2006 Than Ngo <than@redhat.com> 3.2.4-20
- fix #169330, wrong docdir
- fix #187902, no parameter negotiation for xfig
- fix #182451, switch xfig's pdf viewer to evince

* Tue Apr 25 2006 Adam Jackson <ajackson@redhat.com> 3.2.4-19
- Rebuild for updated imake build rules

* Tue Apr 04 2006 Than Ngo <than@redhat.com> 3.2.4-18
- no parameter negotiation for xfig, fix #187902

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 3.2.4-17.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 3.2.4-17.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Dec 21 2005 Than Ngo <than@redhat.com> 3.2.4-17
- workaround for utf8

* Sun Dec 18 2005 Than Ngo <than@redhat.com> 3.2.4-16
- add correct app-defaults directory

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Nov 15 2005 Than Ngo <than@redhat.com> 3.2.4-15
- fix for modular X

* Mon Oct 24 2005 Than Ngo <than@redhat.com> 3.2.4-14
- enable xpm support #158422

* Tue Jul 19 2005 Than Ngo <than@redhat.com> 3.2.4-13
- buildrequires on xorg-x11-devel

* Mon Jul 18 2005 Than Ngo <than@redhat.com> 3.2.4-12
- fix another buffer overflow #163413

* Thu May 19 2005 Than Ngo <than@redhat.com> 3.2.4-11
- apply patch to fix buffer overflow #158088

* Mon Mar 21 2005 Than Ngo <than@redhat.com> 3.2.4-10
- fix font warning #116542

* Mon Mar 07 2005 Than Ngo <than@redhat.com> 3.2.4-9
- cleanup

* Sat Mar 05 2005 Than Ngo <than@redhat.com> 3.2.4-8
- rebuilt

* Wed Feb 09 2005 Than Ngo <than@redhat.com> 3.2.4-7
- rebuilt

* Sat Sep 25 2004 Than Ngo <than@redhat.com> 3.2.4-6
- add mimetype spec #131629

* Mon Sep 13 2004 Than Ngo <than@redhat.com> 3.2.4-5
- fix desktop file #131983

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun  3 2003 Jeff Johnson <jbj@redhat.com>
- add explicit epoch's where needed.

* Tue May  6 2003 Than Ngo <than@redhat.com> 3.2.4-1
- 3.2.4

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Nov  7 2002 Than Ngo <than@redhat.com> 3.2.3d-11
- rebuild in new enviroment

* Thu Aug 22 2002 Than Ngo <than@redhat.com> 3.2.3d-10
- close should get fd, not filename

* Wed Jul 31 2002 Than Ngo <than@redhat.com> 3.2.3d-9
- Fixed typo bug (bug #70347)

* Wed Jul 24 2002 Than Ngo <than@redhat.com> 3.2.3d-8
- desktop file issue (bug #69543)

* Tue Jun 25 2002 Than Ngo <than@redhat.com> 3.2.3d-7
- add patch file using mkstemp (bug #67351)

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Jul 13 2001 Than Ngo <than@redhhat.com> 3.2.3d-3
- fix build dependencies (bug #48910)

* Tue Jul 03 2001 Than Ngo <than@redhat.com>
- fix export to eps when i18n set (bug #45114)
- requires transfig-3.2.3d

* Fri Jun 15 2001 Than Ngo <than@redhat.com>
- update to 3.2.3d release

* Tue Jun 12 2001 Than Ngo <than@redhat.com>
- fix to build against XFree86-4.1.0

* Tue May 29 2001 Than Ngo <than@redhat.com>
- update to 3.2.3d beta2 fixes (Bug #42597, #42556)
- fix bug when LANG is set, launching help gives a spurious error (Bug #42596)
- fix bug in resource setting (Bug #42595)
- remove some patches, which are included in 3.2.3d beta2
- fix wrong version number
- use make install.all
- fix fhs problem

* Wed May  9 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Don't require Netscape at all - use htmlview (which automatically launches
  Netscape, Mozilla or Konqueror depending on what is installed/running).
  No need to depend on proprietary stuff...

* Thu Apr 26 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- do the same for s390x

* Sat Jan 06 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- only require /usr/bin/netscape if not on S390

* Tue Dec 20 2000 Yukihiro Nakai <ynakai@redhat.com>
- Delete enable_japanese macro and set i18n default.
- Fix Japanese translation in .desktop file

* Mon Nov 20 2000 Than Ngo <than@redhat.com>
- rebuilt to fix bad dir perms

* Thu Nov 9 2000 Than Ngo <than@redhat.com>
- fixed f_read, which made xfig stop reading the file after
  removing such bad objects.

* Fri Oct 13 2000 Preston Brown <pbrown@redhat.com>
- improved .desktop entry

* Thu Aug 24 2000 Yukihiro Nakai <ynakai@redhat.com>
- Add Japanese patch

* Tue Aug 08 2000 Than Ngo <than@redhat.de>
- fixed dependency problem
- fixed starting xpdf

* Mon Aug 07 2000 Than Ngo <than@redhat.de>
- fixed for using xpdf instead acroreader (Bug #15621)
- add requires: netscape, display

* Sat Aug 05 2000 Than Ngo <than@redhat.de>
- update to 3.2.3c (bugs fixed released)
- fix parse_printcap broken (Bug #11147)

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Fri Jun 23 2000 Than Ngo <than@redhat.de>
- xfig crash, if a menu item was clicked (Bug #12855)

* Sun Jun 18 2000 Than Ngo <than@redhat.de>
- rebuilt in the new build environment
- enable optimization

* Sat Jun 03 2000 Than Ngo <than@redhat.de>
- fix requires, xfig-3.2.3a requires transfig-2.2.3 or newer
- disable optimization -O2 (gcc-2.96 Bug) on i386

* Thu May 18 2000 Preston Brown <pbrown@redhat.com>
- fix buildroot issue in Imakefile

* Mon May  8 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- rebuild with current libXaw3d
- update to 3.2.3a

* Mon Feb 07 2000 Preston Brown <pbrown@redhat.com>
- rebuild to gzip man pages

* Fri Jan 14 2000 Preston Brown <pbrown@redhat.com>
- upgrade to beta1 of 2.2.3.  Hopefully this fixes outstanding issues.
- no need for vararg fix, commented out

* Thu Sep 23 1999 Preston Brown <pbrown@redhat.com>
- add icon
- don't compile with optimization on alpha

* Mon Aug 30 1999 Preston Brown <pbrown@redhat.com>
- converted to use a .desktop file

* Fri Mar 26 1999 Michael Maher <mike@redhat.com>
- added files that were missing.

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com>
- auto rebuild in the new build environment (release 4)
- varargs fix

* Thu Feb 18 1999 Jeff Johnson <jbj@redhat.com>
- correct DESTDIRR typo (#962)

* Wed Dec 30 1998 Cristian Gafton <gafton@redhat.com>
- build for glibc 2.1

* Tue Jul  7 1998 Jeff Johnson <jbj@redhat.com>
- updated to 3.2.2.

* Wed Jun 10 1998 Prospector System <bugs@redhat.com>
- translations modified for de

* Fri May 08 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Sat Apr 11 1998 Cristian Gafton <gafton@redhat.com>
- updated for manhattan
- buildroot

* Thu Oct 23 1997 Marc Ewing <marc@redhat.com>
- new version
- messed with config for 5.0
- updated Requires and Copyright
- added wmconfig

* Mon Jul 21 1997 Erik Troan <ewt@redhat.com>
- built against glibc
