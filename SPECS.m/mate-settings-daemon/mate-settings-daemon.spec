
Name:		mate-settings-daemon
Version:	1.4.0
Release:	7%{?dist}
Summary:	MATE Desktop settings daemon
License:	GPLv2+
URL:		http://mate-desktop.org
Source0:	http://pub.mate-desktop.org/releases/1.4/%{name}-%{version}.tar.xz

BuildRequires:	clutter-gst-devel icon-naming-utils mate-common mate-conf-devel mate-corba-devel mate-desktop-devel dbus-glib-devel gtk2-devel libSM-devel libmatekbd-devel libmatenotify-devel libxklavier-devel nss-devel polkit-devel mate-polkit-devel

Requires(pre):  mate-conf
Requires(post): mate-conf
Requires(preun):mate-conf
Requires: mate-icon-theme

%description
MATE Desktop settings daemon

%package devel
Summary:	Development files for mate-settings-daemon
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for mate-panel

%prep
%setup -q
NOCONFIGURE=1 ./autogen.sh


%build
%configure --disable-static --enable-polkit --enable-gstreamer --enable-profiling --with-x --with-nssdb
make %{?_smp_mflags} V=1


%install
export MATECONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make install DESTDIR=%{buildroot}
magic_rpm_clean.sh
%find_lang %{name}

rm -fv %{buildroot}%{_libdir}/lib*.la


%pre
%mateconf_schema_prepare apps_mate_settings_daemon_housekeeping
%mateconf_schema_prepare apps_mate_settings_daemon_keybindings
%mateconf_schema_prepare apps_mate_settings_daemon_xrandr
%mateconf_schema_prepare desktop_mate_font_rendering
%mateconf_schema_prepare desktop_mate_keybindings
%mateconf_schema_prepare desktop_mate_peripherals_smartcard
%mateconf_schema_prepare desktop_mate_peripherals_touchpad
%mateconf_schema_prepare mate-settings-daemon

%post
/usr/sbin/ldconfig
touch --no-create %{_datadir}/icons/mate &> /dev/null || :
%mateconf_schema_upgrade apps_mate_settings_daemon_housekeeping
%mateconf_schema_upgrade apps_mate_settings_daemon_keybindings
%mateconf_schema_upgrade apps_mate_settings_daemon_xrandr
%mateconf_schema_upgrade desktop_mate_font_rendering
%mateconf_schema_upgrade desktop_mate_keybindings
%mateconf_schema_upgrade desktop_mate_peripherals_smartcard
%mateconf_schema_upgrade desktop_mate_peripherals_touchpad
%mateconf_schema_upgrade mate-settings-daemon

%postun
/usr/sbin/ldconfig
if [ $1 -eq 0 ] ; then
touch --no-create %{_datadir}/icons/mate &> /dev/null
gtk-update-icon-cache %{_datadir}/icons/mate &> /dev/null || :
fi
%mateconf_schema_remove apps_mate_settings_daemon_housekeeping
%mateconf_schema_remove apps_mate_settings_daemon_keybindings
%mateconf_schema_remove apps_mate_settings_daemon_xrandr
%mateconf_schema_remove desktop_mate_font_rendering
%mateconf_schema_remove desktop_mate_keybindings
%mateconf_schema_remove desktop_mate_peripherals_smartcard
%mateconf_schema_remove desktop_mate_peripherals_touchpad
%mateconf_schema_remove mate-settings-daemon

%posttrans
gtk-update-icon-cache %{_datadir}/icons/mate &>/dev/null || :

%files -f %{name}.lang
%doc AUTHORS COPYING README
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.mate.SettingsDaemon.DateTimeMechanism.conf
%config(noreplace) %{_sysconfdir}/mateconf/schemas/apps_mate_settings_daemon_housekeeping.schemas
%config(noreplace) %{_sysconfdir}/mateconf/schemas/apps_mate_settings_daemon_keybindings.schemas
%config(noreplace) %{_sysconfdir}/mateconf/schemas/apps_mate_settings_daemon_xrandr.schemas
%config(noreplace) %{_sysconfdir}/mateconf/schemas/desktop_mate_font_rendering.schemas
%config(noreplace) %{_sysconfdir}/mateconf/schemas/desktop_mate_keybindings.schemas
%config(noreplace) %{_sysconfdir}/mateconf/schemas/desktop_mate_peripherals_smartcard.schemas
%config(noreplace) %{_sysconfdir}/mateconf/schemas/desktop_mate_peripherals_touchpad.schemas
%config(noreplace) %{_sysconfdir}/mateconf/schemas/mate-settings-daemon.schemas
%config(noreplace) %{_sysconfdir}/xdg/autostart/mate-settings-daemon.desktop
%{_libdir}/mate-settings-daemon-1.4.0/
%{_libexecdir}/mate-settings-daemon
%{_libexecdir}/msd-datetime-mechanism
%{_libexecdir}/msd-locate-pointer
%{_datadir}/dbus-1/services/org.mate.SettingsDaemon.service
%{_datadir}/dbus-1/system-services/org.mate.SettingsDaemon.DateTimeMechanism.service
%{_datadir}/icons/mate/*/*/*
%{_datadir}/mate-control-center/
%{_datadir}/mate-settings-daemon/
%{_datadir}/polkit-1/actions/org.mate.settingsdaemon.datetimemechanism.policy

%files devel
%{_includedir}/mate-settings-daemon/
%{_libdir}/pkgconfig/mate-settings-daemon.pc


%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.4.0-7
- 为 Magic 3.0 重建

* Wed Oct 10 2012 Rex Dieter <rdieter@fedoraproject.org> 1.4.0-6
- fix icon scriptlets

* Fri Sep 28 2012 Rex Dieter <rdieter@fedoraproject.org> - 1.4.0-5
- remove local quirks not needed for fedora buildsys
- simplify %%files, fix some dir-ownership
- cosmetics: move scriptlets to be next to %%files

* Tue Sep 25 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-4
- Own mate-settings-daemon directory, update build requires and configure flags

* Tue Sep 25 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-3
- Fix mateconf scritplets, switch back to upstream source.

* Sat Sep 15 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-2
- Move shared libs to main package and update buildrequires to add libSM-devel add mateconf scriptlets

* Sat Sep 01 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-1
- Initial build
