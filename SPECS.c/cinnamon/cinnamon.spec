#global _internal_version  8a53cfb

Name:           cinnamon
Version:        2.2.5
Release:        1%{?dist}
Summary:        Window management and application launching for GNOME
License:        GPLv2+ and LGPLv2+
URL:            http://cinnamon.linuxmint.com 
#Because linuxmint upstream refuses to host pristine upstream tarballs
# To generate tarball
# wget https://github.com/linuxmint/Cinnamon/archive/%%{version}.tar.gz -O cinnamon-%%{version}.tar.gz
# for git
# wget https://github.com/linuxmint/Cinnamon/tarball/%%{_internal_version} -O cinnamon-%%{version}.git%%{_internal_version}.tar.gz
Source0:        http://leigh123linux.fedorapeople.org/pub/%{name}/source/Cinnamon-%{version}.tar.gz
Source1:        polkit-cinnamon-authentication-agent-1.desktop
Source2:        cinnamon-fedora.gschema.override
Source3:        cinnamon-redhat.gschema.override

Patch0:         background.patch
Patch1:         autostart.patch
Patch2:         cinnamon-settings-apps.patch
%if (0%{?rhel} && 0%{?rhel} < 7) || (0%{?fedora} && 0%{?fedora} < 20)
Patch3:         bluetooth.patch
%endif
%if 0%{?fedora} > 20
Patch4:         upower_calender_fix.patch
%endif
%if (0%{?rhel} && 0%{?rhel} <= 7) || (0%{?fedora} && 0%{?fedora} > 19)
Patch5:         remove_bluetootoh.patch
%endif
Patch6:         set_wheel.patch

%global clutter_version 1.12.2
%global cjs_version 2.2.0
%global cinnamon_desktop_version 2.2.0
%global gobject_introspection_version 1.34.2
%global muffin_version 2.2.0
%global json_glib_version 0.13.2

BuildRequires:  pkgconfig(clutter-1.0) >= %{clutter_version}
BuildRequires:  pkgconfig(dbus-glib-1)
BuildRequires:  desktop-file-utils
BuildRequires:  pkgconfig(cjs-1.0) >= %{cjs_version}
BuildRequires:  pkgconfig(gconf-2.0)
BuildRequires:  pkgconfig(libgnome-menu-3.0)
BuildRequires:  cinnamon-menus-devel
BuildRequires:  pkgconfig(cinnamon-desktop) >= %{cinnamon_desktop_version}
BuildRequires:  gobject-introspection >= %{gobject_introspection_version}
BuildRequires:  pkgconfig(json-glib-1.0) >= %{json_glib_version}
BuildRequires:  pkgconfig(upower-glib)
BuildRequires:  pkgconfig(libnm-glib)
BuildRequires:  pkgconfig(polkit-agent-1)
BuildRequires:  pkgconfig(gudev-1.0)
# for screencast recorder functionality
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  intltool
BuildRequires:  pkgconfig(libcanberra)
BuildRequires:  pkgconfig(libcroco-0.6)
BuildRequires:  pkgconfig(gnome-keyring-1)
BuildRequires:  pkgconfig(libsoup-2.4)
# used in unused BigThemeImage
BuildRequires:  pkgconfig(librsvg-2.0)
BuildRequires:  pkgconfig(libmuffin) >= %{muffin_version}
BuildRequires:  pkgconfig(libpulse)
%if (0%{?rhel} && 0%{?rhel} < 7) || (0%{?fedora} && 0%{?fedora} < 20)
%ifnarch s390 s390x
BuildRequires:  pkgconfig(gnome-bluetooth-1.0) >= 2.91
BuildRequires:  gnome-bluetooth >= 2.91
%endif
%endif
# Bootstrap requirements
BuildRequires:  pkgconfig(gtk-doc) 
BuildRequires:  gnome-common
# mediia keys
BuildRequires:  pkgconfig(libnotify)
BuildRequires:  pkgconfig(lcms2)
BuildRequires:  pkgconfig(colord)
%ifnarch s390 s390x %{?rhel:ppc ppc64}
BuildRequires:  pkgconfig(libwacom)
BuildRequires:  pkgconfig(xorg-wacom)
%endif
BuildRequires:  pkgconfig(xtst)

Requires:       muffin%{?_isa} >= %{muffin_version}
Requires:       gnome-menus%{?_isa} >= 3.0.0-2
# wrapper script uses to restart old GNOME session if run --replace
# from the command line
Requires:       gobject-introspection%{?_isa} >= %{gobject_introspection_version}
# needed for loading SVG's via gdk-pixbuf
Requires:       librsvg2%{?_isa}
# needed as it is now split from Clutter
Requires:       json-glib%{?_isa} >= %{json_glib_version}
Requires:       upower%{?_isa}
Requires:       polkit%{?_isa} >= 0.100
# needed for session files
Requires:       cinnamon-session
# needed for schemas
Requires:       at-spi2-atk%{?_isa}
# needed for on-screen keyboard
Requires:       caribou%{?_isa}
# needed for the user menu
Requires:       accountsservice-libs
# needed for settings
Requires:       pygobject2
Requires:       dbus-python
Requires:       python-lxml
Requires:       gnome-python2-gconf
Requires:       python-pillow
Requires:       PyPAM
Requires:       mintlocale
%if 0%{?fedora}
Requires:       python-pexpect
%else
Requires:       pexpect
%endif
Requires:       opencv-python
Requires:       cinnamon-control-center
Requires:       cinnamon-translations
# RequiredComponents in the session files
Requires:       nemo
Requires:       cinnamon-screensaver

# metacity is needed for fallback
Requires:       metacity
%if 0%{?fedora}
Requires:       tint2

# needed for theme overrides
Requires:       zukitwo-gtk2-theme
Requires:       zukitwo-gtk3-theme
Requires:       gnome-themes
%endif

# re-add bluetooth support for F19
%if (0%{?rhel} && 0%{?rhel} < 7) || (0%{?fedora} && 0%{?fedora} < 20)
Requires:       blueman
%endif

# required for keyboard applet
Requires:       gucharmap

# required for network applet
Requires:       nm-connection-editor
Requires:       network-manager-applet

Provides:       desktop-notification-daemon
Obsoletes:      cinnamon-2d
Obsoletes:      cinnamon-settings
Obsoletes:      cinnamon-menu-editor
Obsoletes:      cinnamon <= 1.8.0-1


%description
Cinnamon is a Linux desktop which provides advanced
 innovative features and a traditional user experience.

The desktop layout is similar to Gnome 2. 
The underlying technology is forked from Gnome Shell.
The emphasis is put on making users feel at home and providing
 them with an easy to use and comfortable desktop experience.

%prep
%autosetup -p1 -n Cinnamon-%{version}

NOCONFIGURE=1 ./autogen.sh

%build
%configure \
 --disable-static \
 --disable-rpath \
 --disable-schemas-compile \
 --enable-introspection=yes \
 --enable-compile-warnings=no

make %{?_smp_mflags} V=1

%install
%{make_install}

# Remove .la file
rm -rf $RPM_BUILD_ROOT/%{_libdir}/cinnamon/libcinnamon.la

%if 0%{?fedora}
install -D -m 0644 %{SOURCE2} $RPM_BUILD_ROOT/%{_datadir}/glib-2.0/schemas/cinnamon-fedora.gschema.override
%else
install -D -m 0644 %{SOURCE3} $RPM_BUILD_ROOT/%{_datadir}/glib-2.0/schemas/cinnamon-redhat.gschema.override
%endif
# install polkik autostart desktop file
install -D -p -m 0644 %{SOURCE1} $RPM_BUILD_ROOT/%{_datadir}/applications/

desktop-file-validate $RPM_BUILD_ROOT/%{_datadir}/applications/cinnamon.desktop
desktop-file-validate $RPM_BUILD_ROOT/%{_datadir}/applications/cinnamon2d.desktop
desktop-file-validate $RPM_BUILD_ROOT/%{_datadir}/applications/cinnamon-add-panel-launcher.desktop
desktop-file-validate $RPM_BUILD_ROOT/%{_datadir}/applications/cinnamon-settings*.desktop
desktop-file-validate $RPM_BUILD_ROOT/%{_datadir}/applications/cinnamon-menu-editor.desktop
desktop-file-validate $RPM_BUILD_ROOT/%{_datadir}/applications/polkit-cinnamon-authentication-agent-1.desktop

# fix hard coded path
%ifarch x86_64 ppc64
sed -i -e 's@/usr/lib/cinnamon-control-center@/usr/lib64/cinnamon-control-center@g' \
$RPM_BUILD_ROOT/%{_prefix}/lib/cinnamon-settings/bin/capi.py
%endif

# create directory for lang files
install -m 0755 -d $RPM_BUILD_ROOT/%{_datadir}/cinnamon/locale/


%post
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%doc COPYING README NEWS AUTHORS
%{_bindir}/*
%{_sysconfdir}/xdg/menus/*
%{_datadir}/applications/*
%{_datadir}/dbus-1/services/org.Cinnamon.HotplugSniffer.service
%{_datadir}/desktop-directories/*
%{_datadir}/glib-2.0/schemas/*
%{_datadir}/cinnamon-session/sessions/*
%{_datadir}/icons/hicolor/*/*/cs-*.svg
%{_datadir}/polkit-1/actions/org.cinnamon.settings-users.policy
%{_datadir}/xsessions/*
%{_datadir}/cinnamon/
%{_libdir}/cinnamon/
%{_libexecdir}/cinnamon/
#No choice but to do this. Filing a bug with upstream on this.
%{_prefix}/lib/cinnamon*/
%{_mandir}/man1/*

%changelog
* Sat May 03 2014 Leigh Scott <leigh123linux@googlemail.com> - 2.2.5-1
- update to 2.2.5
- validate all the cinnamon-settings desktop files

* Fri May 02 2014 Leigh Scott <leigh123linux@googlemail.com> - 2.2.4-1
- update to 2.2.4

* Mon Apr 21 2014 Leigh Scott <leigh123linux@googlemail.com> - 2.2.3-3
- add requires mintlocale

* Tue Apr 15 2014 Leigh Scott <leigh123linux@googlemail.com> - 2.2.3-2
- add requires gucharmap
- add required network packages for network applet
- change to gstreamer1

* Mon Apr 14 2014 Leigh Scott <leigh123linux@googlemail.com> - 2.2.3-1
- update to 2.2.3

* Sat Apr 12 2014 Leigh Scott <leigh123linux@googlemail.com> - 2.2.0-1
- update to 2.2.0

* Wed Apr 02 2014 Leigh Scott <leigh123linux@googlemail.com> - 2.0.14-16
- add patch to disable xinput for cinnamon only (bz 873434)

* Wed Mar 05 2014 Leigh Scott <leigh123linux@googlemail.com> - 2.0.14-15
- Fix desktop file editor

* Thu Feb 20 2014 Kalev Lember <kalevlember@gmail.com> - 2.0.14-14
- Rebuilt for cogl soname bump

* Mon Feb 10 2014 Peter Hutterer <peter.hutterer@redhat.com> - 2.0.14-13
- Rebuild for libevdev soname bump

* Sun Feb 09 2014 Leigh Scott <leigh123linux@googlemail.com> - 2.0.14-12
- cinnamon-settings-users: set wheel instead of sudo

* Fri Feb 07 2014 Leigh Scott <leigh123linux@googlemail.com> - 2.0.14-11
- rebuilt for new cogl .so version

* Wed Jan 22 2014 Leigh Scott <leigh123linux@googlemail.com> - 2.0.14-10
- use autosetup for prep
- trim spec file changelog

* Tue Jan 14 2014 Leigh Scott <leigh123linux@googlemail.com> - 2.0.14-9
- change pexpect requires for epel7

* Tue Jan 14 2014 Leigh Scott <leigh123linux@googlemail.com> - 2.0.14-8
- Add conditionals for epel7
- Add redhat overrides schema file

* Sun Dec 22 2013 Leigh Scott <leigh123linux@googlemail.com> - 2.0.14-7
- Remove bluetooth for F20 as well

* Sun Dec 22 2013 Leigh Scott <leigh123linux@googlemail.com> - 2.0.14-6
- Patch calendar applet for upower changes
- Remove bluetooth

* Sat Dec 07 2013 Leigh Scott <leigh123linux@googlemail.com> - 2.0.14-5
- readd requires python-pexpect for ARM

* Tue Dec 03 2013 Leigh Scott <leigh123linux@googlemail.com> - 2.0.14-4
- add requires gnome-themes

* Mon Dec 02 2013 Leigh Scott <leigh123linux@googlemail.com> - 2.0.14-3
- tweak gschema override again

* Tue Nov 26 2013 Leigh Scott <leigh123linux@googlemail.com> - 2.0.14-2
- add compile fix for F21

* Tue Nov 26 2013 Leigh Scott <leigh123linux@googlemail.com> - 2.0.14-1
- update to 2.0.14
- remove conflicts wallpapoz (bz 1029554)
- remove nm-applet from autostart (bz 1034887)

* Sun Nov 24 2013 Leigh Scott <leigh123linux@googlemail.com> - 2.0.13-3
- patch to restore panel icon bounce

* Sun Nov 24 2013 Leigh Scott <leigh123linux@googlemail.com> - 2.0.13-2
- set default theme to zukitwo

* Sun Nov 24 2013 Leigh Scott <leigh123linux@googlemail.com> - 2.0.13-1
- update to 2.0.13
- tweak gschema override again

* Thu Nov 14 2013 Leigh Scott <leigh123linux@googlemail.com> - 2.0.12-2
- add conflicts wallpapoz (bz 1029554)

* Mon Nov 11 2013 Leigh Scott <leigh123linux@googlemail.com> - 2.0.12-1
- update to 2.0.12
- tweak gschema override again

* Sun Nov 10 2013 Leigh Scott <leigh123linux@googlemail.com> - 2.0.11-1
- update to 2.0.11
- remove upstream patch
- tweak gschema override

* Tue Nov 05 2013 Leigh Scott <leigh123linux@googlemail.com> - 2.0.10-2
- add patch to draw desktop background immediately

* Sun Nov 03 2013 Leigh Scott <leigh123linux@googlemail.com> - 2.0.10-1
-  update to 2.0.10

* Fri Nov 01 2013 Leigh Scott <leigh123linux@googlemail.com> - 2.0.8-1
- update to 2.0.8
- add autostart file for polkit

* Wed Oct 30 2013 Leigh Scott <leigh123linux@googlemail.com> - 2.0.7-1
- update to 2.0.7

* Fri Oct 25 2013 Leigh Scott <leigh123linux@googlemail.com> - 2.0.6-1
- update to 2.0.6

* Thu Oct 24 2013 Leigh Scott <leigh123linux@googlemail.com> - 2.0.5-1
- update to 2.0.5

* Fri Oct 18 2013 Leigh Scott <leigh123linux@googlemail.com> - 2.0.3-1
- update to 2.0.3

* Thu Oct 17 2013 Leigh Scott <leigh123linux@googlemail.com> - 2.0.2-3
- add custom nm-applet file as the stock one is set to NotShowIn Gnome

* Thu Oct 10 2013 Leigh Scott <leigh123linux@googlemail.com> - 2.0.2-2
- add policy file for "users and groups" setting
- add nm-applet to required components
- add upstream commits

* Wed Oct 09 2013 Leigh Scott <leigh123linux@googlemail.com> - 2.0.2-1
- update to 2.0.2
- drop upstream patch

* Mon Oct 07 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.9.2-4
- revert ST changes

* Mon Oct 07 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.9.2-3
- patch with upstream commits for
- lightdm and a
- ST crash on user switching

* Tue Oct 01 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.9.2-2
- set some sound defaults

* Mon Sep 30 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.9.2-1
- update to 1.9.2

* Tue Sep 24 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.9.2-0.27.git8a53cfb
- use the right conditional (too much beer)

* Tue Sep 24 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.9.2-0.26.git8a53cfb
- re-add bluetooth support for F19

* Tue Sep 24 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.9.2-0.25.git8a53cfb
- Remove ExcludeArch for ARM
- remove the python-pexpect requires for ARM

* Sat Sep 21 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.9.2-0.24.git8a53cfb
- patch to add input-source switching keybindings

* Thu Sep 19 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.9.2-0.23.git8a53cfb
- patch keyboard applet (also fixes input-switching)

* Wed Sep 18 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.9.2-0.22.git8a53cfb
- update to latest git

* Wed Sep 11 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.9.2-0.21.git2d1ac4d
- ExcludeArch for ARM due to missing dep (python-pexpect)

* Sun Aug 25 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.9.2-0.20.git2d1ac4d
- update to latest git
- Change buildrequires to cinnamon-desktop-devel

* Sat Aug 24 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.9.2-0.19.gitd4305ab
- add requires cinnamon-translations

* Fri Aug 23 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.9.2-0.18.gitd4305ab
- update to latest git
- adjust for new cinnamon-translations package

* Thu Aug 22 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.9.2-0.17.git8bdd61f
- rebuilt

* Tue Aug 20 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.9.2-0.16.git8bdd61f
- update to latest git
- drop upstream patches

* Sat Aug 10 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.9.2-0.15.git19b4b43
- redo gsettings patch

* Sat Aug 10 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.9.2-0.14.git19b4b43
- update to latest git
- drop upstream fixes

* Sat Aug 10 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.9.2-0.13.gita1dd2a1
- add patch to remove obsolete gsettings for menu and button icon till upstream fixes it

* Fri Aug 09 2013 Kalev Lember <kalevlember@gmail.com> - 1.9.2-0.12.gita1dd2a1
- Rebuilt for cogl 1.15.4 soname bump

* Mon Jul 29 2013 leigh <leigh123linux@googlemail.com> - 1.9.2-0.11.gita1dd2a1
- fix bluetooth patch again

* Mon Jul 29 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.9.2-0.10.gita1dd2a1
- remove some fixes and upstream patches
- redo bluetooth patch

* Sun Jul 28 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.9.2-0.9.git39fc3a7
- patch to use cinnamon-control-center bluetooth

* Sun Jul 28 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.9.2-0.8.git39fc3a7
- add virtual provides desktop-notification-daemon
- fix missing settings-users menu icon

* Sat Jul 27 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.9.2-0.7.git39fc3a7
- fix icon path for user and groups

* Fri Jul 26 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.9.2-0.6.git39fc3a7
- drop screensaver patch

* Fri Jul 26 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.9.2-0.5.git39fc3a7
- update to latest git
- fix panel-edit crash

* Thu Jul 25 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.9.2-0.4.git435e7a2
- Fix automake warnings

* Thu Jul 25 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.9.2-0.3.git435e7a2
- update to latest git
- fix default theme
- use fedora firewall in settings
- use beesu for user accounts instead of gksu

* Wed Jul 24 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.9.2-0.2.gitc321232
- fix control-center settings on x86_64
- drop clutter xinput patch
- add missing requirements for cinnamon-settings
- redo screensaver patch to enable/disable lock password

* Tue Jul 23 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.9.2-0.1.gitc321232
- rebase for cinnamon next

* Tue Jul 23 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.9.1-19
- fix permissions on cinnamon3d

* Mon Jul 22 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.9.1-18
- fix permissions on cinnamon-launcher-creator

* Tue Jul 16 2013 leigh scott <leigh123linux@googlemail.com> - 1.9.1-17
- add patch to fix cinnamon-menu-editor

* Fri Jul 12 2013 leigh scott <leigh123linux@googlemail.com> - 1.9.1-16
- remove GC from cinnamon-global.c

* Wed Jul 10 2013 leigh scott <leigh123linux@googlemail.com> - 1.9.1-15
- fix input-source-switcher autostart

* Wed Jul 10 2013 leigh scott <leigh123linux@googlemail.com> - 1.9.1-14
- fix input-source-switcher

* Fri Jun 14 2013 leigh scott <leigh123linux@googlemail.com> - 1.9.1-13
- spec file clean up

* Thu Jun 13 2013 leigh scott <leigh123linux@googlemail.com> - 1.9.1-12
- Fix automount

* Thu Jun 13 2013 Dan Horák <dan[at]danny.cz> - 1.9.1-11
- fix build on s390(x) - no wacom there

* Wed Jun 12 2013 leigh scott <leigh123linux@googlemail.com> - 1.9.1-10
- fix the screensaver tab in cinnamon-settings

* Sun Jun 09 2013 leigh scott <leigh123linux@googlemail.com> - 1.9.1-9
- add requires gnome-screensaver

* Sun Jun 09 2013 leigh scott <leigh123linux@googlemail.com> - 1.9.1-8
- Fix media keys

* Thu Jun 06 2013 leigh scott <leigh123linux@googlemail.com> - 1.9.1-7
- change how the screen lock autostarts

* Thu Jun 06 2013 leigh scott <leigh123linux@googlemail.com> - 1.9.1-6
- add requires nemo

* Thu Jun 06 2013 leigh scott <leigh123linux@googlemail.com> - 1.9.1-5
- autostart nemo differently so we dont squash nautilus

* Thu Jun 06 2013 leigh scott <leigh123linux@googlemail.com> - 1.9.1-4
- Patch so screen lock uses gnome-screensaver
- add gnome-screensaver autostart files
- add patch to remove obex file transfer

* Tue Jun 04 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.9.1-3
- add cinnamon-fedora.gschema.override file

* Tue Jun 04 2013 leigh scott <leigh123linux@googlemail.com> - 1.9.1-2
- patch for mozjs-17 changes

* Sat Jun 01 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.9.1-1
- Update to version 1.9.1

* Sat Jun 01 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.8.7-2
- Re-add build requires versions

