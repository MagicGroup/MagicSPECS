# Conditional for release and snapshot builds. Uncomment for release-builds.
%global rel_build 1

# This is needed, because src-url contains branched part of versioning-scheme.
%global branch 1.12

# Settings used for build from snapshots.
%{!?rel_build:%global commit 7ba7e03f4d5e2ecd3c77f9d9394521b7608ca05f}
%{!?rel_build:%global commit_date 20131212}
%{!?rel_build:%global shortcommit %(c=%{commit};echo ${c:0:7})}
%{!?rel_build:%global git_ver git%{commit_date}-%{shortcommit}}
%{!?rel_build:%global git_rel .git%{commit_date}.%{shortcommit}}
%{!?rel_build:%global git_tar %{name}-%{version}-%{git_ver}.tar.xz}

Name:          eom
Version:       %{branch}.1
%if 0%{?rel_build}
Release:       1%{?dist}
%else
Release:       0.2%{?git_rel}%{?dist}
%endif
Summary:       Eye of MATE image viewer
License:       GPLv2+ and LGPLv2+ 
URL:           http://mate-desktop.org 

# for downloading the tarball use 'spectool -g -R eom.spec'
# Source for release-builds.
%{?rel_build:Source0:     http://pub.mate-desktop.org/releases/%{branch}/%{name}-%{version}.tar.xz}
# Source for snapshot-builds.
%{!?rel_build:Source0:    http://git.mate-desktop.org/%{name}/snapshot/%{name}-%{commit}.tar.xz#/%{git_tar}}

# https://github.com/mate-desktop/eom/pull/113
Patch0:        eom_fix-gir-compilation.patch

BuildRequires: zlib-devel
BuildRequires: cairo-gobject-devel
BuildRequires: gtk2-devel
BuildRequires: libexif-devel
BuildRequires: exempi-devel
BuildRequires: gobject-introspection-devel
BuildRequires: libxml2-devel
BuildRequires: librsvg2-devel
BuildRequires: mate-desktop-devel
BuildRequires: lcms2-devel
BuildRequires: pygtk2-devel
BuildRequires: dbus-glib-devel
BuildRequires: libjpeg-turbo-devel
BuildRequires: desktop-file-utils
BuildRequires: mate-common

#fix rhbz (#1008249)
Requires:      mate-desktop-libs

%if 0%{?fedora} && 0%{?fedora} > 19
Provides: mate-image-viewer%{?_isa} = %{version}-%{release}
Provides: mate-image-viewer = %{version}-%{release}
Obsoletes: mate-image-viewer < %{version}-%{release}
%endif

%description
The Eye of MATE (eom) is the official image viewer for the
MATE desktop. It can view single image files in a variety of formats, as
well as large image collections.
Eye of Mate is extensible through a plugin system.

%package devel
Summary:  Support for developing plugins for the eom image viewer
Group:    Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
%if 0%{?fedora} && 0%{?fedora} > 19
Provides: mate-image-viewer-devel%{?_isa} = %{version}-%{release}
Provides: mate-image-viewer-devel = %{version}-%{release}
Obsoletes: mate-image-viewer-devel < %{version}-%{release}
%endif

%description devel
Development files for eom


%prep
%setup -q%{!?rel_build:n %{name}-%{commit}}

%patch0 -p1 -b .fix-gir-compilation
NOCONFIGURE=1 ./autogen.sh

%if 0%{?rel_build}
#NOCONFIGURE=1 ./autogen.sh
%else # 0%{?rel_build}
# needed for git snapshots
NOCONFIGURE=1 ./autogen.sh
%endif # 0%{?rel_build}

%build
%configure \
   --with-gtk=2.0 \
   --enable-python \
   --with-x \
   --disable-schemas-compile \
   --enable-introspection=yes
           
make %{?_smp_mflags} V=1

%install
%{make_install}

desktop-file-install                               \
  --delete-original                                \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications    \
$RPM_BUILD_ROOT%{_datadir}/applications/eom.desktop

find ${RPM_BUILD_ROOT} -type f -name "*.la" -exec rm -f {} ';'

%find_lang %{name} --with-gnome --all-name

# remove needless gsettings convert file
rm -f  $RPM_BUILD_ROOT%{_datadir}/MateConf/gsettings/eom.convert


%post
/usr/bin/update-desktop-database &> /dev/null || :
/bin/touch --no-create %{_datadir}/icons/hicolor >&/dev/null || :


%postun
/usr/bin/update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ]; then
  /bin/touch --no-create %{_datadir}/icons/hicolor >&/dev/null || :
  /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor >&/dev/null || :
  /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor >&/dev/null || :
/usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :


%files -f %{name}.lang
%doc AUTHORS COPYING NEWS README
%{_mandir}/man1/*
%{_bindir}/eom
%dir %{_libdir}/eom
%dir %{_libdir}/eom/plugins
%{_libdir}/eom/plugins/*
%{_libdir}/girepository-1.0/Eom-1.0.typelib
%{_datadir}/applications/eom.desktop
%{_datadir}/eom/
%{_datadir}/icons/hicolor/*
%{_datadir}/glib-2.0/schemas/org.mate.eom.gschema.xml
%{_datadir}/glib-2.0/schemas/org.mate.eom.enums.xml
%{_datadir}/appdata/eom.appdata.xml

%files devel
%{_libdir}/pkgconfig/eom.pc
%dir %{_includedir}/eom-2.20
%dir %{_includedir}/eom-2.20/eom
%{_includedir}/eom-2.20/eom/*.h
%{_datadir}/gtk-doc/html/eom/
%{_datadir}/gir-1.0/*.gir


%changelog
* Mon Dec 14 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.12.1-1
- update to 1.12.1 release
- fix gir compilation

* Fri Nov 06 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.12.0-1
- update to 1.12.0 release

* Thu Oct 22 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.11.0-1
- update to 1.11.0 release

* Thu Oct 08 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.10.5-1
- update to 1.10.5 release

* Tue Jul 14 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.10.3.1
- update to 1.10.3 release
- remove upstreamed patches

* Sat Jun 27 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.10.2-2
- fix rhbz (#1230244)

* Wed Jun 17 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.10.2-1
- update to 1.10.2 release

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 15 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.10.1.2
- fix broken translations in gsettings key
- fix issue in finen and korean laguages
- fix build with --strict option
- fix a eom-critical warning

* Fri Jun 12 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.10.1.1
- update to 1.10.1 release

* Tue May 05 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.10.0-1
- update to 1.10.0 release
- fix glib-compile-schemas

* Sun Apr 05 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.90-1
- update to 1.9.90 release
- add BR cairo-gobject-devel
- disable introspection build temporarily

* Thu Jan 22 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.1-1
- update to 1.9.1 release
- enable inrospection build

* Sun Oct 26 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.0-1
- update to 1.9.0
- support gnome-software

* Tue Sep 30 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.8.1-1
- update to 1.8.1 release
- fix obsoletes/provides

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jul 18 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.8.0.3
- fix obsoletes/provides for -devel subpackage

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Mar 05 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 1.8.0-1
- Update to 1.8.0

* Wed Feb 19 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.90-1
- update to 1.7.90

* Thu Feb 13 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.0-1
- update to 1.7.0
- add --with-x configure flag
- use -devel subpackage for release builds

* Wed Dec 18 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.0-0.1.git20131212.7ba7e03
- rename mate-image-viewer to eom
- use latest git snapshot
- make maintainers life easier and use better git snapshot usage, thanks to Björn Esser
- use --with-gnome --all-name for find locale

* Fri Dec 06 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.0-1
- Update to 1.7.0 from mate-desktop git

* Mon Sep 16 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-2
- add mate-desktop-libs runtime require, fix rhbz (#1008249)
- remove gsettings-desktop-schemas BR and runtime require
- add BR pkgconfig(zlib)
- cleanup BRs
- update descriptions
- use modern make install macro
- remove needless check for "*.a" files
- remove needless --with-gnome from find locale
- remove needless 'save space by linking identical images in translated docs'
- remove needless gsettings convert file
- fix rpm scriptlets
- add omf directory
- own directories
- add python-libdir patch

* Mon Jul 29 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.1-1
- Update to latest 1.6.1 stable release.

* Wed Apr 03 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.0-1
- Update to latest 1.6.0 stable release.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 1.5.0-3
- rebuild due to "jpeg8-ABI" feature drop

* Tue Nov 06 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.0-2
- Fix scriptlet mistake

* Mon Nov 05 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.0-1
- Initial build

