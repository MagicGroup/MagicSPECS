# Conditional for release and snapshot builds. Uncomment for release-builds.
%global rel_build 1

# This is needed, because src-url contains branched part of versioning-scheme.
%global branch 1.12

# Settings used for build from snapshots.
%{!?rel_build:%global commit 5bba3723566489763aafaad3669c77f60a23d2e0}
%{!?rel_build:%global commit_date 20140122}
%{!?rel_build:%global shortcommit %(c=%{commit};echo ${c:0:7})}
%{!?rel_build:%global git_ver git%{commit_date}-%{shortcommit}}
%{!?rel_build:%global git_rel .git%{commit_date}.%{shortcommit}}
%{!?rel_build:%global git_tar %{name}-%{version}-%{git_ver}.tar.xz}

Name:          atril
Version:       %{branch}.2
%if 0%{?rel_build}
Release:       2%{?dist}
%else
Release:       0.2%{?git_rel}%{?dist}
%endif
Summary:       Document viewer
License:       GPLv2+ and LGPLv2+ and MIT
URL:           http://mate-desktop.org

# for downloading the tarball use 'spectool -g -R caja.spec'
# Source for release-builds.
%{?rel_build:Source0:     http://pub.mate-desktop.org/releases/%{branch}/%{name}-%{version}.tar.xz}
# Source for snapshot-builds.
%{!?rel_build:Source0:    http://git.mate-desktop.org/%{name}/snapshot/%{name}-%{commit}.tar.xz#/%{git_tar}}

BuildRequires:  gtk2-devel
BuildRequires:  poppler-glib-devel
BuildRequires:  libXt-devel
BuildRequires:  libsecret-devel
BuildRequires:  libglade2-devel
BuildRequires:  libtiff-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libspectre-devel
BuildRequires:  desktop-file-utils
BuildRequires:  mate-desktop-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  mate-common
BuildRequires:  cairo-gobject-devel
BuildRequires:  yelp-tools

# for the xps back-end
BuildRequires:  libgxps-devel
# for the caja properties page
BuildRequires:  caja-devel
# for the dvi back-end
BuildRequires:  kpathsea-devel
# for the djvu back-end
BuildRequires:  djvulibre-devel
# for epub back-end
BuildRequires:  webkitgtk-devel

Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
#  fix (#974791)
Requires:       mate-desktop-libs
Requires:       mathjax

%if 0%{?fedora} && 0%{?fedora} <= 24
Provides: mate-document-viewe%{?_isa} = %{version}-%{release}
Provides: mate-document-viewer = %{version}-%{release}
Obsoletes: mate-document-viewer < %{version}-%{release}
%endif

%description
Mate-document-viewer is simple document viewer.
It can display and print Portable Document Format (PDF),
PostScript (PS), Encapsulated PostScript (EPS), DVI, DJVU, epub and XPS files.
When supported by the document format, mate-document-viewer
allows searching for text, copying text to the clipboard,
hypertext navigation, table-of-contents bookmarks and editing of forms.


%package libs
Summary: Libraries for the mate-document-viewer
%if 0%{?fedora} && 0%{?fedora} <= 24
Provides: mate-document-viewer-libs%{?_isa} = %{version}-%{release}
Provides: mate-document-viewer-libs = %{version}-%{release}
Obsoletes: mate-document-viewer-libs < %{version}-%{release}
%endif

%description libs
This package contains shared libraries needed for mate-document-viewer.


%package devel
Summary: Support for developing back-ends for the mate-document-viewer
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
%if 0%{?fedora} && 0%{?fedora} <= 24
Provides: mate-document-viewer-devel%{?_isa} = %{version}-%{release}
Provides: mate-document-viewer-devel = %{version}-%{release}
Obsoletes: mate-document-viewer-devel < %{version}-%{release}
%endif

%description devel
This package contains libraries and header files needed for
mate-document-viewer back-ends development.


%package caja
Summary: Mate-document-viewer extension for caja
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: caja
%if 0%{?fedora} && 0%{?fedora} <= 24
Provides: mate-document-viewer-caja%{?_isa} = %{version}-%{release}
Provides: mate-document-viewer-caja = %{version}-%{release}
Obsoletes: mate-document-viewer-caja < %{version}-%{release}
%endif

%description caja
This package contains the mate-document-viewer extension for the
caja file manager.
It adds an additional tab called "Document" to the file properties dialog.

%package thumbnailer
Summary: Atril thumbnailer extension for caja
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: caja

%description thumbnailer
This package contains the atril extension for the
caja file manager.


%prep
%setup -q%{!?rel_build:n %{name}-%{commit}}

%if 0%{?rel_build}
#NOCONFIGURE=1 ./autogen.sh
%else # 0%{?rel_build}
# for snapshots
# needed for git snapshots
NOCONFIGURE=1 ./autogen.sh
%endif # 0%{?rel_build}

%build
%configure \
        --disable-static \
        --disable-schemas-compile \
        --enable-introspection \
        --enable-comics \
        --enable-dvi=yes \
        --enable-djvu=yes \
        --enable-t1lib=no \
        --enable-pixbuf \
        --enable-xps \
        --with-gtk=2.0 \
        --enable-epub

# remove unused-direct-shlib-dependency
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool

make %{?_smp_mflags} V=1


%install
%{make_install}

%find_lang %{name} --with-gnome --all-name

find $RPM_BUILD_ROOT -name '*.la' -exec rm -fv {} ';'

# remove of gsetting,convert file, no need for this in fedora
# because MATE starts with gsetting in fedora.
rm -fv $RPM_BUILD_ROOT%{_datadir}/MateConf/gsettings/atril.convert


%check
desktop-file-validate ${RPM_BUILD_ROOT}%{_datadir}/applications/atril.desktop


%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
/bin/touch --no-create %{_datadir}%{name}/icons/hicolor &>/dev/null || :
/usr/bin/update-desktop-database &> /dev/null || :

%postun
if [ $1 -eq 0 ]; then
  /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
  /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
  /bin/touch --no-create %{_datadir}%{name}/icons/hicolor &>/dev/null
  /usr/bin/gtk-update-icon-cache %{_datadir}%{name}/icons/hicolor &>/dev/null || :
  /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
  /usr/bin/update-desktop-database &> /dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
/usr/bin/gtk-update-icon-cache %{_datadir}%{name}/icons/hicolor &>/dev/null || :
/usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig


%files -f %{name}.lang
%doc README COPYING NEWS AUTHORS
%{_bindir}/*
%dir %{_datadir}/atril
%{_datadir}/atril/*
%{_datadir}/applications/atril.desktop
%{_datadir}/icons/hicolor/*/apps/atril.*
%{_libexecdir}/atril-convert-metadata
%{_libexecdir}/atrild
%{_datadir}/dbus-1/services/org.mate.atril.Daemon.service
%{_datadir}/glib-2.0/schemas/org.mate.Atril.gschema.xml
%{_datadir}/appdata/atril.appdata.xml
%{_mandir}/man1/atril-*.1.*
%{_mandir}/man1/atril.1.*

%files libs
%{_libdir}/libatrilview.so.*
%{_libdir}/libatrildocument.so.*
%{_libdir}/atril/3/backends/
%{_libdir}/girepository-1.0/AtrilDocument-1.5.0.typelib
%{_libdir}/girepository-1.0/AtrilView-1.5.0.typelib

%files caja
%{_libdir}/caja/extensions-2.0/libatril-properties-page.so
%{_datadir}/caja/extensions/libatril-properties-page.caja-extension

%files thumbnailer
%{_datadir}/thumbnailers/atril.thumbnailer

%files devel
%dir %{_includedir}/atril/
%{_includedir}/atril/1.5.0/
%{_libdir}/libatrilview.so
%{_libdir}/libatrildocument.so
%{_libdir}/pkgconfig/atril-view-1.5.0.pc
%{_libdir}/pkgconfig/atril-document-1.5.0.pc
%{_datadir}/gir-1.0/AtrilDocument-1.5.0.gir
%{_datadir}/gir-1.0/AtrilView-1.5.0.gir
%{_datadir}/gtk-doc/html/libatrildocument-1.5.0/
%{_datadir}/gtk-doc/html/libatrilview-1.5.0/
%{_datadir}/gtk-doc/html/atril/


%changelog
* Wed Feb 03 2016 Liu Di <liudidi@gmail.com> - 1.12.2-2
- 为 Magic 3.0 重建

* Sun Dec 27 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.12.2-1
- update to 1.12.2 release

* Wed Dec 02 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.12.1-1
- update to 1.12.1 release
- removed upstreamed patch

* Fri Nov 06 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.12.0-1
- update to 1.12.0 release
- fix regression with dvi documents, https://github.com/mate-desktop/atril/issues/164

* Thu Oct 22 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.11.0-1
- update to 1.11.0 release
- drop runtime require mate-icon-theme
- add runtime require mathjax for epub

* Mon Aug 31 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.10.2-1
- update to 1.10.2 release

* Mon Jul 13 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.10.1-1
- update to 1.10.1 release

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 05 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.10.0-1
- update to 1.10.0 release

* Sat Apr 04 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.90-1
- update to 1.9.90 release

* Thu Jan 22 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.2-1
- update to 1.9.2 release

* Thu Dec 11 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.1-1
- update to 1.9.1 release
- remove atril_epub-mimetypes.patch

* Mon Dec 08 2014 Adam Jackson <ajax@redhat.com> 1.9.0-2
- Don't build against t1lib, freetype is sufficient (#852489)

* Sun Oct 26 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.0-1
- update to 1.9.0
- Add epub support (part of GSoC 2014).
- Use MateAboutDialog from libmate-desktop
- remove upstreamed patches
- add configure patch

* Sat Oct 11 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.8.1-2
- enable thumbnailer support and use a -thumbnailer subpackage for it
- fix rhbz (#1150875)

* Mon Sep 29 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.8.1-1
- update to 1.8.1 release

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Aug 15 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.8.0-7
- disable thumbnailer

* Fri Aug 01 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.8.0-6
- rebuild to obsolete mate-document-viewer correctly

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 1.8.0-5
- Rebuilt for gobject-introspection 1.41.4

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Apr 21 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.8.0-3
- fix rhbz (#1082143)

* Wed Mar 19 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.8.0-2
- fix rhbz (#999912)
- use better conditionals for obsoleting mate-document-viewer

* Wed Mar 05 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 1.8.0-1
- Update to 1.8.0

* Wed Feb 19 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.90-1
- update to 1.7.90
- no need of autoreconf anymore

* Mon Feb 10 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.2.1
- update to 1.7.2 release
- add autoreconf to fix building

* Fri Jan 24 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.1-1
- update to 1.7.1 release
- add gtk-doc dir for release builds

* Wed Jan 22 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.1-0.1.git20140122.26539f8
- update to git snapshot from 2014.01.22

* Wed Dec 18 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.0-0.2.git20131120.26539f8
- make Maintainers life easier and use better git snapshot usage, Thanks to Björn Esser
- use modern 'make install' macro
- limit obsoletes/provides

* Sat Dec 14 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.0-0.1.git26539f8
- rename to atril
- use 1.7 git snaphot
- fix rpm scriptlets

* Sat Oct 12 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-6
- fix rhbz (#1005519)

* Thu Aug 08 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-5
- rebuild for mate-desktop package split
- add runtime require mate-desktop-libs, fix #974791
- change caja subpackage requires
- remove -libs subpackage requires to main package
- add icon cache scriplets for internal icons
- use autoreconf instead of autogen

* Mon Aug 05 2013 Rex Dieter <rdieter@fedoraproject.org> - 1.6.1-4
- fix deps so main pkg isn't multilib'd
- workaround libtool breakage
- .spec cleanup

* Sat Aug 03 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-3
- fix obsoleting old -data subpackage

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Aug 02 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-1
- update to 1.6.1
- remove -data subpackage
- remove NOCONFIGURE=1 ./autogen.sh line

* Sun Jun 16 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.0-6
- add require mate-desktop, fix #974791

* Mon May 13 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.0-5
- remove isa tag from -data subpackage requires

* Sat May 11 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.0-4
- remove gsettings convert file
- create -data noarch subpackage
- move docs in -data subpackage
- move help dir in -data subpackage
- move locale in -data subpackage

* Fri May 10 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.0-3
- remove -dvi, -djvu, -xps subpackages and move the libs to -libs subpackage
- add Requires: %%{name}%%{?_isa} = %%{version}-%%{release} to -libs subpackage
- remove sed commands for desktop file
- add hicolor-icon-theme require
- fix last changelog date
- rename atril to mate-document-viewer in summarys and descriptions
- to avoid rpmlint warnings
- rename evince to mate-document-viewer in description
- update description
- fix mixed-use-of-spaces-and-tabs in spec file
- move additional doc files to valid doc dir

* Thu May 09 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.0-2
- use libmate-keyring-devel as BR instead of mate-keyring-devel
- fix spelling-error in %%description of -devel subpackage
- fix gsettings schema rpm scriptlets

* Wed Apr 03 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.0-1
- update to 1.6.0

* Thu Mar 21 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.5.0-2
- initial build for fedora

* Fri Nov 16 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.5.0-1
- build against official fedora
- update to 1.5.0
- remove scrollkeeper BR
- remove mate-conf schema directory
- remove upstreamed mate-document-viewer_change_ev_api_version.patch
- remove epoch

* Mon Nov 05 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:1.4.0-0102
- add epoch
- add desktop-file-validate
- remove (noreplace) from schema files

* Sat Oct 06 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.4.0-0101
- improve and review spec file
- own include dir
- add mate-document-viewer_change_ev_api_version.patch
- fix license information
- add ChangeLog
- fix description
- fix unused-direct-shlib-dependency
- fix scriplet section

* Mon Aug 27 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.4.0-0100
- build for f18

* Tue Jul 17 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.4.0-2
- rebuild for f17 and f18

* Tue Jul 17 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.4.0-1
- update to 1.4.0

* Tue Jun 19 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.2.1-3
- test build

* Tue Jun 19 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.2.1-2
- Silence rpm scriptlet output in fc17

* Thu Mar 15 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.2.1-1
- update to 1.2.1

* Mon Mar 12 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.2.0-1
- update to 1.2.0

* Tue Jan 17 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.1.1-2
- rebuild for enable builds for .i686

* Tue Jan 17 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.1.1-1
- updated to 1.1.1 version

* Wed Jan 04 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.1.0-1
- atril.spec based on evince-2.32.0-4.fc14 spec

