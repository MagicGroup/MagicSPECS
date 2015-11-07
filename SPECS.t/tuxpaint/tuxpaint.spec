Name:           tuxpaint
Version:	0.9.22
Release:	2%{?dist}

Epoch:          1
Summary:        Drawing program designed for young children
Summary(zh_CN.UTF-8): 儿童用的绘画程序

Group:          Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
License:        GPLv2+
URL:            http://www.tuxpaint.org/
Source0:        http://download.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Patch0:         tuxpaint-utf8.patch
Patch1:         tuxpaint-0.9.21-fix-desktop-file.patch
Patch2:         tuxpaint-0.9.21-link.patch
Patch3:         tuxpaint-0.9.21-makej.patch
Patch4:         tuxpaint-0.9.21-memset.patch
Patch5:         tuxpaint-0.9.21-png15.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  SDL-devel >= 1.2.4
BuildRequires:  SDL_image-devel
BuildRequires:  SDL_mixer-devel
BuildRequires:  SDL_ttf-devel
BuildRequires:  SDL_Pango-devel
BuildRequires:  desktop-file-utils
BuildRequires:  freetype-devel >= 2.0
BuildRequires:  gettext
BuildRequires:  libpaper-devel
BuildRequires:  libpng-devel
BuildRequires:  librsvg2-devel
BuildRequires:  netpbm-devel
BuildRequires:	fribidi-devel

# This should guarantee the proper permissions on
# all of the /usr/share/icons/hicolor/* directories.
Requires:       hicolor-icon-theme

%description
"Tux Paint" is a free drawing program designed for young children
(kids ages 3 and up). It has a simple, easy-to-use interface,
fun sound effects, and a cartoon mascot who helps you along.

%description -l zh_CN.UTF-8
儿童用的绘画程序。

%package devel
Summary:	Development files for tuxpaint extensions/plugins
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description devel
Development files for tuxpaint extensions/plugins

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q
%patch0 -p1
#%patch1 -p0 -b .fixdesktopfile
#%patch2 -p1 -b .link
#%patch3 -p1 -b .makej
#%patch4 -p1 -b .memset
#%patch5 -p1 -b .png15

sed -i -e '/\/gnome\/apps\/Graphics/d' Makefile
find docs -type f -exec perl -pi -e 's/\r\n/\n/' {} \;
find docs -type f -perm /100 -exec chmod a-x {} \;

make PREFIX=/usr MAGIC_PREFIX=%{_libdir}/tuxpaint/plugins tp-magic-config

%build
make %{?_smp_mflags} \
    PREFIX=/usr \
    CFLAGS="$RPM_OPT_FLAGS" \
    MAGIC_PREFIX=%{_libdir}/tuxpaint/plugins

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_bindir}
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/%{name}
make install PKG_ROOT=$RPM_BUILD_ROOT PREFIX=%{_usr} \
    X11_ICON_PREFIX=$RPM_BUILD_ROOT%{_datadir}/pixmaps/ \
    GNOME_PREFIX=/usr \
    KDE_PREFIX="" \
    KDE_ICON_PREFIX=/usr/share/icons \
    MAGIC_PREFIX=$RPM_BUILD_ROOT%{_libdir}/tuxpaint/plugins
find $RPM_BUILD_ROOT -type d|xargs chmod 0755
magic_rpm_clean.sh
%find_lang %{name}

desktop-file-install --dir $RPM_BUILD_ROOT/%{_datadir}/applications \
    --add-category KidsGame \
    --delete-original \
    $RPM_BUILD_ROOT%{_datadir}/applications/tuxpaint.desktop

# Register as an application to be visible in the software center
#
# NOTE: It would be *awesome* if this file was maintained by the upstream
# project, translated and installed into the right place during `make install`.
#
# See http://www.freedesktop.org/software/appstream/docs/ for more details.
#
mkdir -p $RPM_BUILD_ROOT%{_datadir}/appdata
cat > $RPM_BUILD_ROOT%{_datadir}/appdata/%{name}.appdata.xml <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!-- Copyright 2014 Richard Hughes <richard@hughsie.com> -->
<!--
BugReportURL: https://sourceforge.net/p/tuxpaint/feature-requests/172/
SentUpstream: 2014-09-18
-->
<application>
  <id type="desktop">tuxpaint.desktop</id>
  <metadata_license>CC0-1.0</metadata_license>
  <summary>A drawing program for children</summary>
  <description>
    <p>
      Tux Paint is a free, award-winning drawing program for children ages 3 to
      12.
      Tux Paint is used in schools around the world as a computer literacy
      drawing activity.
      It combines an easy-to-use interface, fun sound effects, and an
      encouraging cartoon mascot who guides children as they use the program.
    </p>
    <p>
      Kids are presented with a blank canvas and a variety of drawing tools to
      help them be creative.
    </p>
  </description>
  <url type="homepage">http://tuxpaint.org/</url>
  <screenshots>
    <screenshot type="default">http://tuxpaint.org/screenshots/starter-coloringbook.png</screenshot>
    <screenshot>http://tuxpaint.org/screenshots/example_simple.png</screenshot>
    <screenshot>http://tuxpaint.org/screenshots/example_space.png</screenshot>
  </screenshots>
  <updatecontact>tuxpaint-devel@lists.sourceforge.net</updatecontact>
</application>
EOF

rm -rf $RPM_BUILD_ROOT%{_docdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root,-)
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%doc docs
%{_bindir}/*
%{_datadir}/%{name}
%{_datadir}/appdata/*.appdata.xml
%{_datadir}/applications/*
%{_datadir}/pixmaps/*
%{_datadir}/icons/*/*/apps/*
%{_libdir}/%{name}/
%{_mandir}/man1/*
%{_sysconfdir}/bash_completion.d/tuxpaint-completion.bash

%files devel
%defattr(-,root,root,-)
%doc %{_datadir}/doc/%{name}-dev/
%{_includedir}/tuxpaint/

%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 1:0.9.22-2
- 为 Magic 3.0 重建

* Mon Oct 05 2015 Liu Di <liudidi@gmail.com> - 1:0.9.22-1
- 更新到 0.9.22

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.9.21-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Mar 26 2015 Richard Hughes <rhughes@redhat.com> - 1:0.9.21-15
- Add an AppData file for the software center

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.9.21-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.9.21-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Aug 22 2013 Ralf Corsépius <corsepiu@fedoraproject.org> -  1:0.9.21-12
- Use find -perm /<mode> instead of obsolete +<mode> (FTBFS, RHBZ#992825).

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.9.21-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Feb 12 2013 Jon Ciesla <limburgher@gmail.com> - 1:0.9.21-10
- Drop desktop vendor tag.

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.9.21-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Mar 22 2012 Tom Callaway <spot@fedoraproject.org> - 1:0.9.21-8
- fix compile against libpng15

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.9.21-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 1:0.9.21-6
- Rebuild for new libpng

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.9.21-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Aug 11 2010 David Malcolm <dmalcolm@redhat.com> - 1:0.9.21-4
- recompiling .py files against Python 2.7 (rhbz#623414)

* Tue Mar 3 2010 Lubomir Rintel <lkundrak@v3.sk> - 1:0.9.21-3
- Fix link with new linker
- Fix incorrect memset() arguments
- Fix parallel build

* Thu Nov 19 2009 Jon Ciesla <limb@jcomserv.net> - 1:0.9.21-2
- Corrected icon requires, BZ 533965.

* Fri Oct 23 2009 Jon Ciesla <limb@jcomserv.net> - 1:0.9.21-1
- New upstream.
- Corrected desktop patch.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.9.20-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.9.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 01 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1:0.9.20-2
- Rebuild for Python 2.6

* Mon Sep  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1:0.9.20-1
- update to 0.9.20

* Mon Sep  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1:0.9.17-4
- fix license tag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1:0.9.17-3
- Autorebuild for GCC 4.3

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 1:0.9.17-2
- Rebuild for selinux ppc32 issue.

* Sat Jul 07 2007 Steven Pritchard <steve@kspei.com> 1:0.9.17-1
- Update to 0.9.17.
- BR librsvg2-devel and libpaper-devel.
- Add include path for glibconfig.h to CFLAGS.

* Tue Jan 30 2007 Steven Pritchard <steve@kspei.com> 1:0.9.16-4
- Honor $RPM_OPT_FLAGS.
- Fix various rpmlint warnings:
  - Expand tabs in spec.
  - Convert tuxpaint.1 to UTF-8.
  - Get rid of DOS line endings in docs.
  - Nothing in docs should be executable.

* Fri Oct 27 2006 Steven Pritchard <steve@kspei.com> 1:0.9.16-3
- Fix category in tuxpaint.desktop.

* Thu Oct 26 2006 Steven Pritchard <steve@kspei.com> 1:0.9.16-2
- Drop "--add-category X-Fedora".

* Tue Oct 24 2006 Steven Pritchard <steve@kspei.com> 1:0.9.16-1
- Update to 0.9.16.

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 0.9.15b-4
 - rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Thu Sep 21 2006 Steven Pritchard <steve@kspei.com> 1:0.9.15b-3
- Explicitly link libpng.

* Mon Aug 28 2006 Steven Pritchard <steve@kspei.com> 1:0.9.15b-2
- Rebuild.
- Update URL.

* Fri Jun 02 2006 Steven Pritchard <steve@kspei.com> 1:0.9.15b-1
- Update to 0.9.15b
- Convert tuxpaint.desktop to UTF-8
- Drop gnome-libs-devel and kdelibs build dependencies by providing
  appropriate variables to "make install"
- Add docs properly
- Indirectly require hicolor-icon-theme (so that directories are
  owned and have proper permissions)

* Mon Mar 13 2006 Steven Pritchard <steve@kspei.com> 1:0.9.15-1
- Update to 0.9.15
- Drop destdir patch

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 1:0.9.13-3
- rebuild on all arches

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Wed Jun 09 2004 Warren Togami <wtogami@redhat.com> 1:0.9.13-0.fdr.1
- Epoch bump to override old k12ltsp package

* Mon May 31 2004 Panu Matilainen <pmatilai@welho.com> 0:0.9.13-0.fdr.1
- update to 0.9.13
- take a private copy of desktop file and fix it..

* Sun May 30 2004 Panu Matilainen <pmatilai@welho.com> 0:0.9.12-0.fdr.3
- add missing buildrequires desktop-file-utils (#1667)

* Fri Oct 03 2003 Panu Matilainen <pmatilai@welho.com> 0:0.9.12-0.fdr.2
- add missing buildreq's: kdelibs, gnome-libs-devel, SDL_mixer-devel
- remove CVS directories from rpm

* Tue Aug 26 2003 Panu Matilainen <pmatilai@welho.com> 0:0.9.12-0.fdr.1
- Initial RPM release.
