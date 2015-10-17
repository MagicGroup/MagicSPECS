Summary:        Power Management Service
Summary(zh_CN.UTF-8): 电源管理服务
Name:           upower
Version:	0.99.3
Release:	1%{?dist}
License:        GPLv2+
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL:            http://upower.freedesktop.org/
Source0:        http://upower.freedesktop.org/releases/upower-%{version}.tar.xz
BuildRequires:  sqlite-devel
BuildRequires:  libtool
BuildRequires:  intltool
BuildRequires:  gettext
BuildRequires:  libgudev1-devel
%ifnarch s390 s390x
BuildRequires:  libusb1-devel
BuildRequires:  libimobiledevice-devel
%endif
BuildRequires:  glib2-devel >= 2.6.0
BuildRequires:  dbus-devel  >= 1.2
BuildRequires:  dbus-glib-devel >= 0.82
BuildRequires:  gobject-introspection-devel
BuildRequires:  gtk-doc
Requires:       udev
Requires:       gobject-introspection

# From rhughes-f20-gnome-3-12 copr
Obsoletes:      compat-upower09 < 0.99

%description
UPower (formerly DeviceKit-power) provides a daemon, API and command
line tools for managing power devices attached to the system.

%description -l zh_CN.UTF-8
电源管理服务。

%package devel
Summary: Headers and libraries for UPower
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}

%description devel
Headers and libraries for UPower.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package devel-docs
Summary: Headers and libraries for UPower
Summary(zh_CN.UTF-8): %{name} 的开发文档
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description devel-docs
Developer documentation for for libupower-glib.

%description devel-docs -l zh_CN.UTF-8
%{name} 的开发文档。

%prep
%setup -q

%build
%configure \
        --enable-gtk-doc \
        --disable-static \
        --enable-introspection \
%ifarch s390 s390x
	--with-backend=dummy
%endif

# Disable SMP build, fails to build docs
make

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
magic_rpm_clean.sh
%find_lang upower || :

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc NEWS COPYING AUTHORS HACKING README
%{_libdir}/libupower-glib.so.*
%{_sysconfdir}/dbus-1/system.d/*.conf
%ifnarch s390 s390x
/usr/lib/udev/rules.d/*.rules
%endif
%dir %{_localstatedir}/lib/upower
%dir %{_sysconfdir}/UPower
%config %{_sysconfdir}/UPower/UPower.conf
%{_bindir}/*
%{_libexecdir}/*
%{_libdir}/girepository-1.0/*.typelib
%{_mandir}/man1/*
%{_mandir}/man7/*
%{_mandir}/man8/*
%{_datadir}/dbus-1/system-services/*.service
/usr/lib/systemd/system/*.service

%files devel
%defattr(-,root,root,-)
%{_datadir}/dbus-1/interfaces/*.xml
%{_libdir}/libupower-glib.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gir-1.0/*.gir
%dir %{_includedir}/libupower-glib
%{_includedir}/libupower-glib/up-*.h
%{_includedir}/libupower-glib/upower.h

%files devel-docs
%defattr(-,root,root,-)
%{_datadir}/gtk-doc
%dir %{_datadir}/gtk-doc/html/UPower
%{_datadir}/gtk-doc/html/UPower/*

%changelog
* Fri Oct 16 2015 Liu Di <liudidi@gmail.com> - 0.99.3-1
- 更新到 0.99.3

* Fri Oct 16 2015 Liu Di <liudidi@gmail.com> - 0.99.2-3
- 为 Magic 3.0 重建

* Tue Dec 23 2014 Liu Di <liudidi@gmail.com> - 0.99.2-2
- 为 Magic 3.0 重建

* Thu Dec 18 2014 Richard Hughes <rhughes@redhat.com> - 0.99.2-1
- New upstream release
- Fix various memory and reference leaks
- Respect the CriticalPowerAction config option
- Set update-time on the aggregate device
- Update display device when battery is removed

* Sun Nov 16 2014 Kalev Lember <kalevlember@gmail.com> - 0.99.1-3
- Obsolete compat-upower09 from rhughes-f20-gnome-3-12 copr

* Wed Oct 15 2014 Peter Robinson <pbrobinson@fedoraproject.org> 0.99.1-2
- Rebuild for libimobiledevice 1.1.7

* Mon Aug 18 2014 Richard Hughes <rhughes@redhat.com> - 0.99.1-1
- New upstream release
- Create the history directory at runtime
- Do not log a critical warning when using _set_object_path_sync()
- Fix API doc for up_client_get_on_battery()
- Fix possible UpHistoryItem leak on failure
- Fix segfault on getting property when daemon is not running
- Fix shutdown on boot on some machines
- Fix small memleak on startup with Logitech devices
- Free the obtained device list array after use
- Remove IsDocked property
- Remove unused polkit dependency

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 0.99.0-6
- Rebuilt for gobject-introspection 1.41.4

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May  5 2014 Peter Robinson <pbrobinson@fedoraproject.org> 0.99.0-4
- Rebuild for libimobiledevice 1.1.6

* Mon Mar 17 2014 Richard Hughes <rhughes@redhat.com> - 0.99.0-3
- Split out a new devel-docs subpackage to fix multilib_policy=all installs.
- Resolves: #1070661

* Fri Nov 08 2013 Bastien Nocera <bnocera@redhat.com> 0.99.0-2
- Fix crash when D-Bus isn't available

* Tue Oct 29 2013 Richard Hughes <rhughes@redhat.com> - 0.99.0-1
- New upstream release
- This version contains major API changes and bumps library soname.
- Add DisplayDevice composite battery
- Add WarningLevel and IconName properties to all devices
- Clamp percentage for overfull batteries
- Emit PropertiesChanged signals
- Enforce critical battery policy on the daemon side
- Reduce client-side and daemon-side wake-ups
- Register objects on the bus once they've been setup
- Remove DeviceChanged and Changed signals
- Remove OnLowBattery property (use WarningLevel instead)
- Remove QoS support
- Remove battery recall support

* Fri Oct 18 2013 Richard Hughes <rhughes@redhat.com> - 0.9.23-1
- New upstream release
- Add missing dbus-glib-1 to private requires
- Avoid trying to close fd that wasn't opened
- Disable Watts-Up devices by default
- Don't guess discharging state for devices
- Fix crasher calling _about_to_sleep_sync()
- Really don't overwrite retval with prop values
- Update and correct Toshiba recall list

* Wed Oct 09 2013 Bastien Nocera <bnocera@redhat.com> 0.9.22-1
- Update to 0.9.22
- Fixes incorrect reporting of some properties
- Fixes battery values for Logitech unifying devices
- Bluetooth input devices support
- Device name fixes

* Fri Jul 26 2013 Richard Hughes <rhughes@redhat.com> - 0.9.21-1
- New upstream release
- Add support for Logitech Wireless (NonUnifying) devices
- Allow clients to call org.freedesktop.DBus.Peer
- Update the upower man page with all the current options
- Use PIE to better secure installed tools and also use full RELRO in the daemon

* Thu Apr 25 2013 Matthias Clasen <mclasen@redhat.com> - 0.9.20-3
- Enabled hardened build
- Don't use /lib/udev in file paths

* Tue Mar 19 2013 Matthias Clasen <mclasen@redhat.com> - 0.9.20-2
- Rebuild

* Mon Mar 11 2013 Richard Hughes <rhughes@redhat.com> - 0.9.20-1
- New upstream release
- Add a --enable-deprecated configure argument to remove pm-utils support
- Deprecate running the powersave scripts
- Factor out the Logitech Unifying support to support other devices
- Require unfixed applications to define UPOWER_ENABLE_DEPRECATED
- Fix batteries which report current energy but full charge
- Fix several small memory leaks

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan 02 2013 Richard Hughes <rhughes@redhat.com> - 0.9.19-1
- New upstream release
- Add a Documentation tag to the service file
- Add support for Logitech Unifying devices
- Do not continue to poll if /proc/timer_stats is not readable
- Fix device matching for recent kernels
- Resolves: #848521

* Wed Oct 24 2012 Dan Horák <dan[at]danny.cz> - 0.9.18-2
- the notify-upower script is not installed with dummy backend on s390(x)

* Wed Aug 08 2012 Richard Hughes <rhughes@redhat.com> - 0.9.18-1
- New upstream release
- Use systemd for suspend and hibernate

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild
