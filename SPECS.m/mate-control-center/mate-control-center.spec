# Conditional for release and snapshot builds. Uncomment for release-builds.
%global rel_build 1

# This is needed, because src-url contains branched part of versioning-scheme.
%global branch 1.8

# Settings used for build from snapshots.
%{!?rel_build:%global commit 922d0e0219b1bedcece8624e4b5fd7e15e7a9bd5}
%{!?rel_build:%global commit_date 20131113}
%{!?rel_build:%global shortcommit %(c=%{commit};echo ${c:0:7})}
%{!?rel_build:%global git_ver git%{commit_date}-%{shortcommit}}
%{!?rel_build:%global git_rel .git%{commit_date}.%{shortcommit}}
%{!?rel_build:%global git_tar %{name}-%{version}-%{git_ver}.tar.xz}

Name:          mate-control-center
Version:       %{branch}.1
Release:       4%{?dist}
#Release:       0.6%{?git_rel}%{?dist}
Summary:       MATE Desktop control-center
License:       LGPLv2+ and GPLv2+
URL:           http://mate-desktop.org

# for downloading the tarball use 'spectool -g -R mate-control-center.spec'
# Source for release-builds.
%{?rel_build:Source0:     http://pub.mate-desktop.org/releases/%{branch}/%{name}-%{version}.tar.xz}
# Source for snapshot-builds.
%{!?rel_build:Source0:    http://git.mate-desktop.org/%{name}/snapshot/%{name}-%{commit}.tar.xz#/%{git_tar}}

# rhbz (#1089461)
Patch0:        mate-control-center_typo-in-gsettings-key.patch

BuildRequires: dconf-devel
BuildRequires: desktop-file-utils
BuildRequires: gtk2-devel
BuildRequires: libcanberra-devel
BuildRequires: libmatekbd-devel
BuildRequires: librsvg2-devel
BuildRequires: libSM-devel
BuildRequires: libXScrnSaver-devel
BuildRequires: libXxf86misc-devel
BuildRequires: mate-common
BuildRequires: mate-desktop-devel
BuildRequires: mate-menus-devel
BuildRequires: mate-settings-daemon-devel
BuildRequires: marco-devel
BuildRequires: unique-devel

Requires: gsettings-desktop-schemas
Requires: hicolor-icon-theme
# keyring support
%if 0%{?fedora} > 19
Requires: gnome-keyring
%else
Requires: mate-keyring
%endif
Requires: %{name}-filesystem%{?_isa} = %{version}-%{release}


%description 
MATE Control Center configures system settings such as themes,
keyboards shortcuts, etc.

%package filesystem
Summary:      MATE Control Center directories
# NOTE: this is an "inverse dep" subpackage. It gets pulled in
# NOTE: by the main package an MUST not depend on the main package

%description filesystem
The MATE control-center provides a number of extension points
for applications. This package contains directories where applications
can install configuration files that are picked up by the control-center
utilities.

%package devel
Summary:      Development files for mate-settings-daemon
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for mate-control-center


%prep
%setup -q%{!?rel_build:n %{name}-%{commit}}

%patch0 -p1 -b .gsettings

# To work around rpath
autoreconf -fi

# needed for git snapshots
#NOCONFIGURE=1 ./autogen.sh

%build
%configure                           \
           --disable-static          \
           --disable-schemas-compile \
           --disable-update-mimedb

# remove unused-direct-shlib-dependency
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool

make %{?_smp_mflags} V=1


%install
%{make_install}

find %{buildroot} -name '*.la' -exec rm -rf {} ';'
find %{buildroot} -name '*.a' -exec rm -rf {} ';'

desktop-file-install                                \
    --delete-original                               \
    --dir=%{buildroot}%{_datadir}/applications      \
%{buildroot}%{_datadir}/applications/*.desktop

# delete mime cache
rm %{buildroot}%{_datadir}/applications/mimeinfo.cache

# remove needless gsettings convert file
rm -f  %{buildroot}%{_datadir}/MateConf/gsettings/mate-control-center.convert

%find_lang %{name} --with-gnome --all-name


%post
/sbin/ldconfig
/usr/bin/update-desktop-database &> /dev/null || :
/usr/bin/update-mime-database %{_datadir}/mime &> /dev/null || :
/bin/touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :

%postun
/sbin/ldconfig
/usr/bin/update-desktop-database &> /dev/null || :
/usr/bin/update-mime-database %{_datadir}/mime &> /dev/null || :
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &> /dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
/usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :


%files -f %{name}.lang
%doc AUTHORS COPYING README
%config %{_sysconfdir}/xdg/menus/matecc.menu
%{_bindir}/mate-*
%{_libdir}/libmate-window-settings.so.*
%{_libdir}/window-manager-settings
%{_libdir}/libslab.so.*
%{_sbindir}/mate-display-properties-install-systemwide
%{_datadir}/applications/*.desktop
%{_datadir}/desktop-directories/matecc.directory
%{_datadir}/icons/hicolor/*/apps/*.png
%{_datadir}/icons/hicolor/scalable/apps/mate-*.svg
%{_datadir}/glib-2.0/schemas/org.mate.*.xml
%{_datadir}/mate-control-center/*
%{_datadir}/mate/cursor-fonts/*.pcf
%{_datadir}/mime/packages/mate-theme-package.xml
%{_datadir}/thumbnailers/mate-font-viewer.thumbnailer
%{_datadir}/polkit-1/actions/org.mate.randr.policy
%{_mandir}/man1/mate-about-me.1.*
%{_mandir}/man1/mate-appearance-properties.1.*
%{_mandir}/man1/mate-default-applications-properties.1.*

%files filesystem
%dir %{_datadir}/mate-control-center
%dir %{_datadir}/mate-control-center/keybindings

%files devel
%{_includedir}/mate-window-settings-2.0
%{_libdir}/pkgconfig/mate-window-settings-2.0.pc
%{_libdir}/libmate-window-settings.so
%{_libdir}/pkgconfig/mate-default-applications.pc
%{_libdir}/pkgconfig/mate-keybindings.pc
%{_includedir}/libslab
%{_libdir}/libslab.so
%{_libdir}/pkgconfig/libslab.pc


%changelog
* Wed May 07 2014 Liu Di <liudidi@gmail.com> - 1.8.1-4
- 为 Magic 3.0 重建

* Wed May 07 2014 Liu Di <liudidi@gmail.com> - 1.8.1-3
- 为 Magic 3.0 重建

* Sat Apr 19 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.8.1-2
- typo in gsettings key, rhbz (#1089461)

* Sun Mar 16 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.8.1-1
- update to 1.8.1 release
- use wildcards for man files extensions
- remove --disable-scrollkeeper configure flag

* Wed Mar 05 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 1.8.0-1
- Update to 1.8.0

* Wed Feb 19 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.90-1
- update to 1.7.90
- repair usage of git snapshots
- improve find language command for yelp-tools
- move autoreconf to the right place

* Thu Feb 13 2014 Dan Mashal <dan.mashal@fedoraproject.org> 1.7.0-2
- Add autoreconf to work around rpath.

* Sun Feb 09 2014 Dan Mashal <dan.mashal@fedoraproject.org> 1.7.0-1
- Update to 1.7.0 release.

* Sat Dec 21 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.0-0.2.git20131113.922d0e0
- make Maintainers life easier and use better git snapshot usage, Thanks to Björn Esser
- use BR marco-devel
- remove Obsoletes: libslab line, no need anymore
- fix mixed usage of tabs and spaces
- use modern 'make install' macro
- make configure command better readable

* Fri Dec 06 2013 Dan Mashal <dan.mashal@fedoraproject.org> 1.7.0-1.1.git922d0e0
- Update to 1.7.0

* Sat Oct 19 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-3
- switch to gnome-keyring for > f19

* Wed Jul 31 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-2
- add mate-control-center-file-system subpackage
- add requires hicolor-icon-theme

* Tue Jul 30 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-1
- update to 1.6.1 release
- remove NOCONFIGURE=1 ./autogen.sh
- update file section
- remove old remnants from spec file

* Sat Jun 29 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.0-2
- add runtime require gsettings-desktop-schemas to have proxy support
- from gnome gsettings schema
- remove needless mate-control-center.convert file
- remove unused-direct-shlib-dependency to avoid rpmlint warnings
- cleanup BR's

* Wed Apr 03 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.0-1
- Update to latest 1.6.0 stable release.

* Mon Mar 25 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.5-3
- Readd desktop file install and remove desktop file validate
- Own proper dirs
- Use buildroot macro instead of rpm_build_root

* Mon Mar 25 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.5.5-2
- bump version in spec file

* Sun Mar 24 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.5.5-1
- update to new upstream release
- remove desktop-file-install command
- add desktop-file-validate command
- fix icon cache rpm scriptlet

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jan 17 2013 Rex Dieter <rdieter@fedoraproject.org> 1.5.3-3
- fix obsoletes
- sort BuildRequires

* Wed Jan 16 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.3-2
- Fix conflicts

* Tue Jan 15 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.3-1
- Update to latest upstream release.

* Fri Jan 11 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.2-2
- Switch back to old BR scheme.
- Drop unneeded BR's
- Add upstream patch to fix tielbar actions

* Fri Dec 21 2012 Nelson Marques <nmarques@fedoraproject.org> - 1.5.2-1
- Update to version 1.5.2 so we can receive mate-panel 1.5.3
- Remove dropped BRs: MateCORBA-2.0 
- Split out libslab (now distributed)
- Minor rework for readibility and ordered BuildRequires

* Sun Nov 25 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.1-1
- Bump to 1.5.1 release

* Thu Nov 08 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.0-2
- patch with latest upstream fixes

* Mon Oct 29 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.0-1
- update to 1.5.0 release
- change build requires and change style
- add requires gsettings-desktop-schemas
- add build requires gsettings-desktop-schemas-devel
- add schema scriptlets
- add build requires dconf-devel 

* Tue Oct 16 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.4.0-9
- move unversioned .so back to main package
- fix directory ownership
- fix scriplets
- add missing build requires

* Wed Oct 03 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-8
- Add disable-update-mimedb to configure flag and update files section

* Wed Oct 03 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-7
- Remove noreplace bit for schemas 
- Remove ownership of XMLnamespaces and aliases folders
- Remove desktop-file-utils from post and postun requires field
- Add mate-conf to post requires field

* Tue Oct 02 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-6
- Remove unnecessary explicit libexecdir configure flag, remove explicit requires field

* Tue Oct 02 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-5
- Fix spelling error on schema install.

* Sun Sep 30 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-4
- Update BR and remove about-me

* Wed Sep 26 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-3
- Add excludes to files section as per package review.

* Tue Sep 25 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-2
- Update files section as per review, update build requires.

* Sat Sep 01 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-1
- Initial build

