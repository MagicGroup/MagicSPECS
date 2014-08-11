#%%global _internal_version  bc54d96

Name:          mate-power-manager
Version:       1.8.0
#Release:       0.4.git%%{_internal_version}%{?dist}
Release:       3%{?dist}
Summary:       MATE power management service
License:       GPLv2+
URL:           http://pub.mate-desktop.org

# To generate tarball
# wget http://git.mate-desktop.org/%%{name}/snapshot/%%{name}-{_internal_version}.tar.xz -O %%{name}-%%{version}.git%%{_internal_version}.tar.xz
#Source0: http://raveit65.fedorapeople.org/Mate/git-upstream/%%{name}-%%{version}.git%%{_internal_version}.tar.xz

Source0:       http://pub.mate-desktop.org/releases/1.8/%{name}-%{version}.tar.xz

# upstream patch
# https://github.com/mate-desktop/mate-power-manager/commit/8cb168b
Patch0:        mate-power-manager_dbus_interface_keyboard_backlight_controls.patch
# https://github.com/mate-desktop/mate-power-manager/commit/2b3cf01
Patch1:        mate-power-manager_avoid-levels-is-0-warning.patch

# upstream fixes for upower-1.0, the order of the series is important
%if 0%{?fedora} > 20
# https://github.com/mate-desktop/mate-power-manager/commit/220a4e0
Patch2:        mate-power-manager_remove-battery-recall-logic.patch
# https://github.com/mate-desktop/mate-power-manager/commit/d59f4b8
Patch3:        mate-power-manager_port-to-upower-0.99-API.patch
# https://github.com/mate-desktop/mate-power-manager/commit/1fb2870
Patch4:        mate-power-manager_improve-UPower1-support.patch
# https://github.com/mate-desktop/mate-power-manager/commit/8f734c6
Patch5:        mate-power-manager_other-round-of-fixes-for-UPower-0.99-API-changes.patch
%endif


BuildRequires: cairo-devel
BuildRequires: dbus-glib-devel
BuildRequires: desktop-file-utils
BuildRequires: libcanberra-devel
BuildRequires: glib2-devel
BuildRequires: gtk2-devel
BuildRequires: libgnome-keyring-devel
BuildRequires: libnotify-devel
BuildRequires: mate-common
BuildRequires: mate-control-center-devel
BuildRequires: mate-panel-devel
BuildRequires: mesa-libGL-devel
BuildRequires: pangox-compat-devel
BuildRequires: popt-devel
BuildRequires: unique-devel
BuildRequires: upower-devel
BuildRequires: xmlto


%description
MATE Power Manager uses the information and facilities provided by UPower
displaying icons and handling user callbacks in an interactive MATE session.


%prep
%setup -q
#%%setup -q -n %{name}-%{_internal_version}

%patch0 -p1 -b .dbus
%patch1 -p1 -b .avoid-levels-is-0-warning
%if 0%{?fedora} > 20
%patch2 -p1 -b .remove-battery-recall-logic
%patch3 -p1 -b .port-to-upower-0.99-API
%patch4 -p1 -b .improve-UPower1-support
%patch5 -p1 -b .other-round-of-fixes-for-UPower-0.99
%endif

# nedded to create configure and make files for dbus patch
NOCONFIGURE=1 ./autogen.sh

%build
%configure \
     --enable-docbook-docs \
     --enable-unique \
     --with-gtk=2.0 \
     --disable-schemas-compile

make %{?_smp_mflags} V=1

%install
%{make_install}

desktop-file-install                               \
     --delete-original                             \
     --dir=%{buildroot}%{_datadir}/applications    \
%{buildroot}%{_datadir}/applications/*.desktop

# remove needless gsettings convert file
rm -f  %{buildroot}%{_datadir}/MateConf/gsettings/mate-power-manager.convert

%find_lang %{name} --with-gnome --all-name


%post
/bin/touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
/usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :


%files  -f %{name}.lang
%doc AUTHORS COPYING README
%{_mandir}/man1/mate-power-*.*
%{_bindir}/mate-power-bugreport.sh
%{_bindir}/mate-power-manager
%{_bindir}/mate-power-preferences
%{_bindir}/mate-power-statistics
%{_sbindir}/mate-power-backlight-helper
%{_datadir}/applications/mate-*.desktop
%{_datadir}/dbus-1/services/*.service
%{_datadir}/mate-power-manager/
%{_datadir}/icons/hicolor/*/apps/mate-*.*
%{_datadir}/polkit-1/actions/org.mate.power.policy
%{_datadir}/mate-2.0/ui/brightness-applet-menu.xml
%{_datadir}/mate-2.0/ui/inhibit-applet-menu.xml
%{_datadir}/mate-panel/applets/org.mate.BrightnessApplet.mate-panel-applet
%{_datadir}/mate-panel/applets/org.mate.InhibitApplet.mate-panel-applet
%{_datadir}/glib-2.0/schemas/org.mate.power-manager.gschema.xml
%{_sysconfdir}/xdg/autostart/mate-power-manager.desktop
%{_libexecdir}/mate-brightness-applet
%{_libexecdir}/mate-inhibit-applet


%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Apr 26 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.8.0-2
- use new upower patches from upstream

* Wed Mar 05 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.8.0-1
- update to 1.8.0 release
- remove uptreamed mouse-click-on-brightness-applet patch

* Wed Feb 19 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.90-1
- update to 1.7.90
- remove --disable-scrollkeeper configure flag

* Mon Jan 20 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> 1.7.0-1
- update to 1.7.0 release
- use modern 'make install' macro
- update BR's
- add --with-gnome --all-name for find language
- clean up file section
- remove upstreamed switch-to-gnome-keyring patch for rawhide
- remove upstreamed set-DISABLE_DEPRECATED-to-an-empty-string.patch
- add better comment

* Fri Dec 20 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.3-1
- updated to 1.6.3 release
- fix build, add  mate-power-manager_set-DISABLE_DEPRECATED-to-an-empty-string.patch
- remove BR mate-keyring-devel
- fix bogus date in %%changelog

* Sun Nov 10 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.3-0.4.gitbc54d96
- support for upower-1.0

* Sat Oct 19 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.3-0.3.gitbc54d96
- switch to gnome-keyring for > f19

* Mon Oct 14 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.3-0.2.gitbc54d96
- fix mouse click on brightness applet, rhbz (#1018915)

* Sun Oct 13 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.3-0.1.gitbc54d96
- update to latest snapshot
- removed upstreamed patches, already in snapshot
- add DBUS interface to kbdbacklight control patch, rhbz (#964678)

* Sun Sep 29 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.2-4
- fix suspend on lid close, fix rhbz (#1012718)

* Fri Aug 09 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.2-3
- fix display-to-sleep-when-inactive, rhbz #994232

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 24 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.2-1
- update to 1.6.2 release
- fix systemd-login1 support, (#972881)
- remove runtime require ConsoleKit-x11
- remove gsettings convert file
- remove runtime require ConsoleKit-x11
- remove BR systemd-devel
- remove systemd configure flags
- remove NOCONFIGURE=1 ./autogen.sh

* Thu Jun 20 2013 Rex Dieter <rdieter@fedoraproject.org> 1.6.1-3
- Requires: ConsoleKit-x11 (#972881)

* Tue Jun 18 2013 Dan Mashal <dan.mashal@fedoraproject.org> 1.6.1-2
- Add patch to fix suspend on lid close

* Fri May 10 2013 Dan Mashal <dan.mashal@fedoraproject.org> 1.6.1-1
- Update to latest upstream release
- Add systemd sleep configure flag

* Sun Apr 21 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.0-2
- Add upstream patch to fix suspend on lid close

* Mon Apr 08 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.0-1
- Update to 1.6.0 stable release

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Dec 21 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.5.1-5
- Rework specfile to make it easier to read and pretty.
- Drop duplicate BRs

* Thu Nov 29 2012 Nelson Marques <nmo.marques@gmail.com> - 1.5.1-4
- Add %%name-1.5.1-add_systemd_checks.patch - fixes crasher,
  systemd inhibit requires systemd >= 195, merged upstream

* Mon Nov 26 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.1-3
- Add hard requires to mate-panel-libs to fix dependency issues

* Fri Nov 23 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.1-2
- add br systemd-devel as we need systemd support

* Thu Nov 22 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.1-1
- Update to 1.5.1 release
- Drop patches that already exist in 1.5.1 release

* Wed Nov 14 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.0-2
- add upstream patch to add keyboard backlight support

* Thu Nov 08 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.0-1
- update to 1.5.0 release

* Mon Oct 29 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.4.1-0.1.git543b06f
- update to latest git snapshot
- patch to build against latest mate-panel

* Fri Oct 19 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.4.0-2
- add V=1 to make command
- add mate-conf requires and remove mate-icon-theme

* Fri Oct 19 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.4.0-1
- Initial build
