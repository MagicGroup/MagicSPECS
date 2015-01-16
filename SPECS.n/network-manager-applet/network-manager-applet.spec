%define gtk3_version    3.0.1
%define glib2_version   2.32.0
%define dbus_version    1.4
%define dbus_glib_version 0.86
%define nm_version      1:0.9.9.95
%define obsoletes_ver   1:0.9.7

%define snapshot %{nil}
%define git_sha %{nil}
%define realversion 1.0.0

Name: network-manager-applet
Summary: A network control and status applet for NetworkManager
Version: 1.0.0
Release: 1%{snapshot}%{git_sha}%{?dist}
Group: Applications/System
License: GPLv2+
URL: http://www.gnome.org/projects/NetworkManager/
Obsoletes: NetworkManager-gnome < %{obsoletes_ver}

Source: https://download.gnome.org/sources/network-manager-applet/1.0/%{name}-%{realversion}%{snapshot}%{git_sha}.tar.xz
Patch0: nm-applet-no-notifications.patch
Patch1: nm-applet-wifi-dialog-ui-fixes.patch
Patch2: applet-ignore-deprecated.patch

Requires: NetworkManager >= %{nm_version}
Requires: NetworkManager-glib >= %{nm_version}
Requires: libnm-gtk = %{version}-%{release}
Requires: dbus >= 1.4
Requires: dbus-glib >= 0.100
Requires: libnotify >= 0.4.3
Requires: nm-connection-editor = %{version}-%{release}

BuildRequires: NetworkManager-devel >= %{nm_version}
BuildRequires: NetworkManager-glib-devel >= %{nm_version}
BuildRequires: ModemManager-glib-devel >= 1.0
BuildRequires: dbus-devel >= %{dbus_version}
BuildRequires: dbus-glib-devel >= %{dbus_glib_version}
BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: gtk3-devel >= %{gtk3_version}
BuildRequires: libsecret-devel
BuildRequires: gobject-introspection-devel >= 0.10.3
BuildRequires: gettext-devel
BuildRequires: /usr/bin/autopoint
BuildRequires: pkgconfig
BuildRequires: libnotify-devel >= 0.4
BuildRequires: automake autoconf intltool libtool
BuildRequires: gtk-doc
BuildRequires: desktop-file-utils
BuildRequires: iso-codes-devel
BuildRequires: libgudev1-devel >= 147
BuildRequires: libsecret-devel >= 0.12

%description
This package contains a network control and status notification area applet
for use with NetworkManager.

%package -n nm-connection-editor
Summary: A network connection configuration editor for NetworkManager
Requires: NetworkManager-glib >= %{nm_version}
Requires: libnm-gtk = %{version}-%{release}
Requires: dbus >= 1.4
Requires: dbus-glib >= 0.94
Requires(post): /usr/bin/gtk-update-icon-cache

%description -n nm-connection-editor
This package contains a network configuration editor and Bluetooth modem
utility for use with NetworkManager.


%package -n libnm-gtk
Summary: Private libraries for NetworkManager GUI support
Group: Development/Libraries
Requires: gtk3 >= %{gtk3_version}
Requires: mobile-broadband-provider-info >= 0.20090602
Obsoletes: NetworkManager-gtk < %{obsoletes_ver}

%description -n libnm-gtk
This package contains private libraries to be used only by nm-applet,
nm-connection editor, and the GNOME Control Center.

%package -n libnm-gtk-devel
Summary: Private header files for NetworkManager GUI support
Group: Development/Libraries
Requires: NetworkManager-devel >= %{nm_version}
Requires: NetworkManager-glib-devel >= %{nm_version}
Obsoletes: NetworkManager-gtk-devel < %{obsoletes_ver}
Requires: libnm-gtk = %{version}-%{release}
Requires: gtk3-devel
Requires: pkgconfig

%description -n libnm-gtk-devel
This package contains private header and pkg-config files to be used only by
nm-applet, nm-connection-editor, and the GNOME control center.


%prep
%setup -q -n network-manager-applet-%{realversion}

%patch0 -p1 -b .no-notifications
%patch1 -p1 -b .applet-wifi-ui
%patch2 -p1 -b .no-deprecated

%build
autoreconf -i -f
intltoolize --force
%configure \
    --disable-static \
    --without-bluetooth \
    --with-modem-manager-1=yes \
    --enable-more-warnings=yes \
    --disable-migration
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_datadir}/gnome-vpn-properties

%find_lang nm-applet
cat nm-applet.lang >> %{name}.lang

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

# validate .desktop and autostart files
desktop-file-validate $RPM_BUILD_ROOT%{_sysconfdir}/xdg/autostart/nm-applet.desktop
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/nm-connection-editor.desktop


%post	-n libnm-gtk -p /sbin/ldconfig
%postun	-n libnm-gtk -p /sbin/ldconfig

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%post -n nm-connection-editor
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :

%postun -n nm-connection-editor
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :

%posttrans -n nm-connection-editor
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :

%files
%defattr(-,root,root,0755)
%doc COPYING NEWS AUTHORS README CONTRIBUTING
%dir %{_datadir}/nm-applet
%{_bindir}/nm-applet
%{_datadir}/applications/nm-applet.desktop
%{_datadir}/nm-applet/8021x.ui
%{_datadir}/nm-applet/info.ui
%{_datadir}/nm-applet/gsm-unlock.ui
%{_datadir}/nm-applet/keyring.png
%{_datadir}/icons/hicolor/22x22/apps/nm-adhoc.png
%{_datadir}/icons/hicolor/22x22/apps/nm-mb-roam.png
%{_datadir}/icons/hicolor/22x22/apps/nm-secure-lock.png
%{_datadir}/icons/hicolor/22x22/apps/nm-signal-*.png
%{_datadir}/icons/hicolor/22x22/apps/nm-stage*-connecting*.png
%{_datadir}/icons/hicolor/22x22/apps/nm-tech-*.png
%{_datadir}/icons/hicolor/22x22/apps/nm-vpn-active-lock.png
%{_datadir}/icons/hicolor/22x22/apps/nm-vpn-connecting*.png
%{_datadir}/icons/hicolor/22x22/apps/nm-wwan-tower.png
%{_datadir}/GConf/gsettings/nm-applet.convert
%{_sysconfdir}/xdg/autostart/nm-applet.desktop
%{_mandir}/man1/nm-applet*

# Yes, lang files for the applet go in nm-connection-editor RPM since it
# is the RPM that everything else depends on
%files -n nm-connection-editor -f %{name}.lang
%dir %{_datadir}/nm-applet
%{_bindir}/nm-connection-editor
%{_datadir}/applications/nm-connection-editor.desktop
%{_datadir}/nm-applet/ce-*.ui
%{_datadir}/nm-applet/eap-method-*.ui
%{_datadir}/nm-applet/ws-*.ui
%{_datadir}/nm-applet/nm-connection-editor.ui
%{_datadir}/icons/hicolor/*/apps/nm-device-*.*
%{_datadir}/icons/hicolor/*/apps/nm-no-connection.*
%{_datadir}/icons/hicolor/16x16/apps/nm-vpn-standalone-lock.png
%{_datadir}/glib-2.0/schemas/org.gnome.nm-applet.gschema.xml
%{_mandir}/man1/nm-connection-editor*
%dir %{_datadir}/gnome-vpn-properties

%files -n libnm-gtk
%defattr(-,root,root,0755)
%{_libdir}/libnm-gtk.so.*
%dir %{_datadir}/libnm-gtk
%{_datadir}/libnm-gtk/*.ui
%{_libdir}/girepository-1.0/NMGtk-1.0.typelib

%files -n libnm-gtk-devel
%defattr(-,root,root,0755)
%dir %{_includedir}/libnm-gtk
%{_includedir}/libnm-gtk/*.h
%{_libdir}/pkgconfig/libnm-gtk.pc
%{_libdir}/libnm-gtk.so
%{_datadir}/gir-1.0/NMGtk-1.0.gir

%changelog
* Mon Dec 22 2014 Dan Williams <dcbw@redhat.com> - 1.0.0-1
- Update to 1.0

* Mon Dec  1 2014 Jiří Klimeš <jklimes@redhat.com> - 0.9.10.1-1.git20141201.be5a9db
- update to latest git snapshot of 0.9.10 (git20141201 sha:be5a9db)

* Wed Sep 03 2014 Kalev Lember <kalevlember@gmail.com> - 0.9.9.0-15.git20140424
- Backport a patch to hide nm-connection-editor launcher in GNOME

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.9.0-14.git20140424
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 0.9.9.0-13.git20140424
- Rebuilt for gobject-introspection 1.41.4

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.9.0-12.git20140424
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 07 2014 Kalev Lember <kalevlember@gmail.com> - 0.9.9.0-11.git20140424
- Drop gnome-icon-theme dependency

* Thu Apr 24 2014 Jiří Klimeš <jklimes@redhat.com> - 0.9.9.0-10.git20140424
- update to latest git snapshot (git20140424 sha:9ba9c3e)

* Mon Mar 24 2014 Dan Winship <danw@redhat.com> - 0.9.9.0-9.git20140123
- Add ModemManager-glib-devel to BuildRequires

* Thu Jan 23 2014 Jiří Klimeš <jklimes@redhat.com> - 0.9.9.0-8.git20140123
- update to latest git snapshot (git20140123 sha:5d4f17e)
- applet: fix crash when "CA certificate is not required" (rh #1055535)

* Fri Dec 20 2013 Kevin Fenzi <kevin@scrye.com> 0.9.9.0-8.git20131028
- Remove bluetooth plugin, doesn't work with new gnome-bluetooth/bluez5

* Mon Oct 28 2013 Dan Winship <danw@redhat.com> - 0.9.9.0-7.git20131028
- update to latest git snapshot
- re-enable nm-applet on certain non-GNOME-Shell desktops (rh #1017471)

* Fri Sep 13 2013 Dan Williams <dcbw@redhat.com> - 0.9.9.0-6.git20130906
- libnm-gtk: fix for enabling the Apply button for PEAP and TTLS (rh #1000564)
- libnm-gtk: only save CA certificate ignored value when connection is saved
- editor: fix display of VLAN parent interface

* Fri Sep 06 2013 Dan Williams <dcbw@redhat.com> - 0.9.9.0-5.git20130906
- editor: fix missing user/password when re-editing a connection (rh #1000564)
- editor: fix handling of missing CA certificate prompts (rh #758076) (rh #809489)
- editor: fix handling of bonding modes (rh #953076)
- applet/editor: add InfiniBand device support (rh #867273)

* Tue Aug 06 2013 Dennis Gilmore <dennis@ausil.us> - 0.9.9.0-4.git20130515
- rebuild for soname bump in gnome-bluetooth

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.9.0-3.git20130515
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Dan Williams <dcbw@redhat.com> - 0.9.9.0-2
- Disable migration tool and remove dependencies on GConf and gnome-keyring

* Wed May 15 2013 Dan Williams <dcbw@redhat.com> - 0.9.9.0-1.git20130515
- Update to 0.9.10 snapshot

* Tue Apr 30 2013 Dan Williams <dcbw@redhat.com> - 0.9.8.1-3.git20130430
- editor: fix possible crash canceling connection edit dialog
- applet: only request secrets from the user when allowed to
- applet: fix signal icons with newer libpng
- applet: fix possible crash getting secrets with libsecret

* Thu Apr 18 2013 Jiří Klimeš <jklimes@redhat.com> - 0.9.8.1-2.git20130327
- applet: fix crash while getting a PIN to unlock a modem (rh #950925)

* Wed Mar 27 2013 Dan Williams <dcbw@redhat.com> - 0.9.8.1-1.git20130327
- Update to 0.9.8.2 snapshot
- Updated translations
- editor: don't overwrite bridge/bond master interface name with UUID
- applet: fix WWAN PIN dialog invalid "label1" entry widget
- editor: fix allowed values for VLAN ID and MTU
- editor: preserve existing PPP connection LCP echo failure and reply values
- editor: ensure changes to the STP checkbox are saved
- editor: hide BSSID for AdHoc connection (rh #906133)
- editor: fix random data sneaking into IPv6 route gateway fields
- editor: fix handling of initial entry for MAC address widgets

* Wed Feb 27 2013 Jiří Klimeš <jklimes@redhat.com> - 0.9.8.0-1
- Update to 0.9.8.0

* Fri Feb  8 2013 Dan Williams <dcbw@redhat.com> - 0.9.7.997-1
- Update to 0.9.7.997 (0.9.8-beta2)
- editor: better handling of gateway entry for IPv4
- editor: fix some mnemonics (rh #893466)
- editor: fix saving connection when ignoring CA certificate
- editor: enable Bridge connection editing
- editor: hide widgets not relevant for VPN connections

* Tue Dec 11 2012 Jiří Klimeš <jklimes@redhat.com> - 0.9.7.0-6.git20121211
- editor: fix populating Firewall zone in 'General' tab

* Tue Dec 11 2012 Jiří Klimeš <jklimes@redhat.com> - 0.9.7.0-5.git20121211
- Update to git snapshot (git20121211) without bridges

* Thu Nov 08 2012 Kalev Lember <kalevlember@gmail.com> - 0.9.7.0-4.git20121016
- Update the versioned obsoletes for the new F17 NM build

* Tue Oct 16 2012 Jiří Klimeš <jklimes@redhat.com> - 0.9.7.0-3.git20121016
- Update to git snapshot (git20121016)
- editor: fix a crash when no VPN plugins are installed

* Thu Oct  4 2012 Dan Winship <danw@redhat.com> - 0.9.7.0-3.git20121004
- Update to git snapshot

* Wed Sep 12 2012 Jiří Klimeš <jklimes@redhat.com> - 0.9.7.0-3.git20120820
- move GSettings schema XML to nm-connection-editor rpm (rh #852792)

* Thu Aug 30 2012 Jiří Klimeš <jklimes@redhat.com> - 0.9.7.0-2.git20120820
- run glib-compile-schemas in %post scriplet (rh #852792)

* Tue Aug 21 2012 Dan Winship <danw@redhat.com> - 0.9.7.0-1.git20120820
- Update to 0.9.7.0 snapshot

* Tue Aug 14 2012 Daniel Drake <dsd@laptop.org> - 0.9.5.96-2
- Rebuild for libgnome-bluetooth.so.11

* Mon Jul 23 2012 Dan Williams <dcbw@redhat.com> - 0.9.5.96-1
- Update to 0.9.6-rc2
- lib: recognize PKCS#12 files exported from Firefox
- lib: fix some wireless dialog crashes

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.5.95-3.git20120713
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jul 14 2012 Kalev Lember <kalevlember@gmail.com> - 0.9.5.95-2.git20120713
- Fix the versioned obsoletes

* Fri Jul 13 2012 Jiří Klimeš <jklimes@redhat.com> - 0.9.5.95-1.git20120713
- update to 0.9.5.95 (0.9.6-rc1)  snapshot
- editor: fixed UI mnemonics
- editor: fix defaults for PPP echo values
- applet: various crash and stability fixes
- applet: show IPv6 addressing page for VPN plugins that support it
- applet: port to GSettings and split out 0.8 -> 0.9 migration code into standalone tool

* Mon May 21 2012 Jiří Klimeš <jklimes@redhat.com> - 0.9.4-4
- update to git snapshot

* Wed May  2 2012 Jiří Klimeš <jklimes@redhat.com> - 0.9.4-3
- update to git snapshot

* Mon Mar 19 2012 Dan Williams <dcbw@redhat.com> - 0.9.3.997-1
- Initial package split from NetworkManager

