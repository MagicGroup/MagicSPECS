Summary:        Power Management Service
Name:           upower
Version:        0.99.0
Release:        2%{?dist}
License:        GPLv2+
Group:          System Environment/Libraries
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
BuildRequires:  polkit-devel >= 0.92
BuildRequires:  gobject-introspection-devel
BuildRequires:  gtk-doc
Requires:       polkit >= 0.92
Requires:       udev
Requires:       gobject-introspection

Patch0: 0001-lib-Fix-segfault-on-getting-property-when-daemon-is-.patch

%description
UPower (formerly DeviceKit-power) provides a daemon, API and command
line tools for managing power devices attached to the system.

%package devel
Summary: Headers and libraries for UPower
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Obsoletes: DeviceKit-power-devel < 1:0.9.0-2

%description devel
Headers and libraries for UPower.

%prep
%setup -q
%patch0 -p1

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

%find_lang upower

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f upower.lang
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
%{_datadir}/gtk-doc
%dir %{_datadir}/gtk-doc/html/UPower
%{_datadir}/gtk-doc/html/UPower/*
%{_libdir}/libupower-glib.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gir-1.0/*.gir
%dir %{_includedir}/libupower-glib
%{_includedir}/libupower-glib/up-*.h
%{_includedir}/libupower-glib/upower.h

%changelog
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
