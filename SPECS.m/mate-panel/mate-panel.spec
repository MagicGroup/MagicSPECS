# Conditional for release and snapshot builds. Uncomment for release-builds.
%global rel_build 1

# This is needed, because src-url contains branched part of versioning-scheme.
%global branch %(echo %{version} | awk -F. '{print $1"."$2}')

# Settings used for build from snapshots.
%{!?rel_build:%global commit 838555a41dc08a870b408628f529b66e2c8c4054}
%{!?rel_build:%global commit_date 20140222}
%{!?rel_build:%global shortcommit %(c=%{commit};echo ${c:0:7})}
%{!?rel_build:%global git_ver git%{commit_date}-%{shortcommit}}
%{!?rel_build:%global git_rel .git%{commit_date}.%{shortcommit}}
%{!?rel_build:%global git_tar %{name}-%{version}-%{git_ver}.tar.xz}

Name:           mate-panel
Version: 1.11.1
Release: 2%{?dist}
#Release: 1%{?dist}
Summary:        MATE Desktop panel and applets
Summary(zh_CN.UTF-8): MATE 桌面面板和小部件
#libs are LGPLv2+ applications GPLv2+
License:        GPLv2+
URL:            http://mate-desktop.org

# for downloading the tarball use 'spectool -g -R mate-panel.spec'
# Source for release-builds.
%{?rel_build:Source0:     http://pub.mate-desktop.org/releases/%{branch}/%{name}-%{version}.tar.xz}
# Source for snapshot-builds.
%{!?rel_build:Source0:    http://git.mate-desktop.org/%{name}/snapshot/%{name}-%{commit}.tar.xz#/%{git_tar}}

Source1:        mate-panel_fedora.layout

Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
# needed as nothing else requires it
Requires:       mate-session-manager
#for fish
Requires:       fortune-mod
Requires:       hicolor-icon-theme
# rhbz (#1007219)
Requires:       caja-schemas

BuildRequires:  dbus-glib-devel
BuildRequires:  desktop-file-utils
BuildRequires:  gobject-introspection-devel
BuildRequires:  gtk2-devel
BuildRequires:  libcanberra-devel
BuildRequires:  libmateweather-devel
BuildRequires:  libwnck-devel
BuildRequires:  libnm-gtk-devel
BuildRequires:  librsvg2-devel
BuildRequires:  libSM-devel
BuildRequires:  mate-common
BuildRequires:  mate-desktop-devel
BuildRequires:  mate-menus-devel
BuildRequires:  yelp-tools

%description
MATE Desktop panel applets

%description -l zh_CN.UTF-8
MATE 桌面面板和小部件。

%package libs
Summary:     Shared libraries for mate-panel
Summary(zh_CN.UTF-8): %{name} 的运行库
License:     LGPLv2+
Requires:    %{name}%{?_isa} = %{version}-%{release}

%description libs
Shared libraries for libmate-desktop

%description libs -l zh_CN.UTF-8
%{name} 的运行库。

%package devel
Summary:     Development files for mate-panel
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires:    %{name}-libs%{?_isa} = %{version}-%{release}

%description devel
Development files for mate-panel

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q%{!?rel_build:n %{name}-%{commit}}

# To work around rpath
#autoreconf -fi

# needed for git snapshots
NOCONFIGURE=1 ./autogen.sh

%build

#libexecdir needed for gnome conflicts
%configure                                        \
           --disable-static                       \
           --disable-schemas-compile              \
           --with-x                               \
           --enable-network-manager               \
           --libexecdir=%{_libexecdir}/mate-panel \
           --with-gtk=2.0                         \
           --enable-introspection                 \
           --enable-gtk-doc

# remove unused-direct-shlib-dependency
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool

make  %{?_smp_mflags} V=1


%install
%{make_install}

find %{buildroot} -name '*.la' -exec rm -rf {} ';'
find %{buildroot} -name '*.a' -exec rm -rf {} ';'

desktop-file-install \
        --dir=%{buildroot}%{_datadir}/applications \
%{buildroot}%{_datadir}/applications/mate-panel.desktop

install -D -m 0644 %{SOURCE1} %{buildroot}%{_datadir}/mate-panel/layouts/fedora.layout

# remove needless gsettings convert file
rm -f  %{buildroot}%{_datadir}/MateConf/gsettings/mate-panel.convert
magic_rpm_clean.sh
%find_lang %{name} --with-gnome --all-name


%post
/bin/touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :
update-desktop-database &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &> /dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi
update-desktop-database &> /dev/null || :

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
/usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig


%files -f %{name}.lang
%doc AUTHORS COPYING README
%{_mandir}/man1/*
%{_bindir}/mate-desktop-item-edit
%{_bindir}/mate-panel
%{_bindir}/mate-panel-test-applets
%{_libexecdir}/mate-panel
%{_datadir}/glib-2.0/schemas/org.mate.panel.*.xml
%{_datadir}/applications/mate-panel.desktop
%{_datadir}/icons/hicolor/*/*/*
%{_datadir}/mate-panel
%{_datadir}/dbus-1/services/org.mate.panel.applet.ClockAppletFactory.service
%{_datadir}/dbus-1/services/org.mate.panel.applet.FishAppletFactory.service
%{_datadir}/dbus-1/services/org.mate.panel.applet.NotificationAreaAppletFactory.service
%{_datadir}/dbus-1/services/org.mate.panel.applet.WnckletFactory.service

%files libs
%doc COPYING.LIB
%{_libdir}/libmate-panel-applet-4.so.1*
%{_libdir}/girepository-1.0/MatePanelApplet-4.0.typelib

%files devel
%doc %{_datadir}/gtk-doc/html/mate-panel-applet/
%{_libdir}/libmate-panel-applet-4.so
%{_includedir}/mate-panel-4.0
%{_libdir}/pkgconfig/libmatepanelapplet-4.0.pc
%{_datadir}/gir-1.0/MatePanelApplet-4.0.gir


%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 1.11.1-2
- 更新到 1.11.1

* Mon Aug 11 2014 Liu Di <liudidi@gmail.com> - 1.9.1-1
- 更新到 1.9.1

* Wed May 07 2014 Liu Di <liudidi@gmail.com> - 1.8.0-3
- 为 Magic 3.0 重建

* Wed May 07 2014 Liu Di <liudidi@gmail.com> - 1.8.0-2
- 为 Magic 3.0 重建

* Wed Mar 05 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 1.8.0-1
- Update to 1.8.0

* Sat Feb 22 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.91-0.1.git20140222.838555a
- update to git snapshot from 2014.02.22
- use new panel layout file

* Tue Feb 18 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.90-1
- update to 1.7.90
- add --enable-gtk-doc configure flag
- move autoreconf to the right place

* Thu Feb 13 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.2-2
- Add autoreconf -fi to work around rpath.

* Sun Feb 09 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.2-1
- Update to 1.7.2

* Tue Jan 14 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.1-1
- update to 1.7.1 release
- use gtk-docs for release build
- remove obsolete BR --disable-scrollkeeper

* Sat Dec 21 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.1-0.2.git20131212.f4c7c8f
- make Maintainers life easier and use better git snapshot usage, Thanks to Björn Esser
- use requires caja-schemas
- use isa tag for -libs subpackage
- use modern 'make install' macro
- fix usage of %%{buildroot} or $RPM_BUILD_ROOT
- use better macro for SOURCE1
- move rpm scriptlets for -libs subpackage to the right place
- fix unused-direct-shlib-dependency rpmlint warning
- move %%{_libdir}/girepository-1.0/MatePanelApplet-4.0.typelib to -libs subpackage
- improve find language command for yelp-tools

* Thu Dec 12 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.1-0.1.gitbeb21bb
- update to latest git snapshot
- fix refer to cairo-gobject, noticed by M.Schwendt
- fix usage of wrong git snapshot tarball, 1.7.0 is released!
- no need of calling autotools when using autogen.sh

* Fri Dec 06 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.0-1.1.gitd2a24b9
- Update to 1.7.0
- Use latest upstream git as released version fails to build with gtk2 

* Thu Sep 12 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-4
- add runtime require mate-file-manager-schemas, fix rhbz (#1007219)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 19 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-2
- update panel-default-layout.dist for caja-1.6.2

* Thu Jul 18 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-1
- update to 1.6.1
- add upstream patch to fix partially
- https://github.com/mate-desktop/mate-panel/issues/111
- remove needless BR gsettings-desktop-schemas-devel

* Sat Jun 15 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.0-3
- remove gsettings convert file

* Fri May 31 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.0-2
- set default panel layout, add panel-default-layout.dist file
- add requires hicolor-icon-theme

* Wed Apr 03 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.0-1
- Update to latest 1.6.0 stable release.

* Wed Mar 27 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.6-2
- Remove ---with-in-process-applets configure flag as per upstream advice

* Tue Mar 26 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.6-1
- Update to latest upstream release

* Fri Feb 08 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.5-1
-Update to latest upstream release

* Sun Jan 20 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.4-1
- Update to latest upstream release
- Convert back to old BR style and sort BRs

* Fri Dec 21 2012 Nelson Marques <nmarques@fedoraproject.org> - 1.5.3-1
- Update to version 1.5.3
- Remove deprecated patches
- Improved readability without harming current style

* Tue Dec 18 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.5.2-5
- Fix crash on panel delete

* Tue Nov 27 2012 Rex Dieter <rdieter@fedoraproject.org> 1.5.2-4
- fix -libs subpkg, %%doc COPYING.LIB
- spec cleanup (whitespace mostly)
- fix icon scriptlet

* Mon Nov 26 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.2-2
- Move libmate-panel-applet-4.so to separate libs package as mate-power-manager depends on it

* Thu Nov 22 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.2-1
- Update to 1.5.2 release

* Mon Oct 29 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.1-1
- update to 1.5.1 release
- add schema scriptlets and remove mateconf scriptlets
- add requires gsettings-desktop-schemas
- add build requires gsettings-desktop-schemas-devel and dconf-devel
- move .gir file to devel package
- clean up spec file
- patch for new dconf api

* Mon Oct 22 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.4.0-12
- Remove un-needed %%check section

* Mon Oct 22 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.4.0-11
- add requires mate-session-manager
- change style for build requirements

* Wed Oct 10 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.4.0-10
- remove ugly hack
- set panel-default-setup.entries

* Sun Oct 07 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.4.0-9
- Change %%define to %%global
- Tidy up schema scriplets
- Tidy up %%build section

* Sun Oct 07 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-8
- Add ugly hack for panel-default-setup.entries

* Sat Oct 06 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-7
- Add enable-introspection and --with-x to configure flags
- Update desktop-file-install macro
- Update BR
- Turn desktop-file-validate back on
- Add fortune-mod to requires for fish to work properly.

* Wed Oct 03 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-6
- Add posttrans scriptlet to update icon cache and fix ordering of scriptlets
- Add comment about licensing

* Wed Oct 03 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-5
- Fix typo for netowrkmanager devel package on f18 

* Tue Oct 02 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-4
- Fix directory ownership, fix libexec configure flag
- Fix schema installation.. totally off

* Tue Oct 02 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-3
- Fix buildrequires for networkmanager rename in f18 as per juhp

* Wed Sep 26 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-2
- Fix mateconf scriptlets

* Sat Sep 01 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-1
-Initial build

