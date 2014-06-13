%global         git_commit 043bbae
Name:           kde-plasma-nm
Version:        0.9.3.4
Release:        7.20140520git%{git_commit}%{?dist}
Summary:        Plasma applet written in QML for managing network connections
License:        LGPLv2+ and GPLv2+
URL:            https://projects.kde.org/projects/playground/network/plasma-nm
# Source0:        http://download.kde.org/unstable/plasma-nm//plasma-nm-%{version}.tar.xz
# # Package from git snapshots using releaseme scripts
Source0:        plasma-nm-%{version}.tar.xz

# Add plasma-nm to default systray if needed, for upgraders...
Source10: 01-fedora-plasma-nm.js


BuildRequires:  gettext
BuildRequires:  kdelibs4-devel
BuildRequires:  kdebase4-workspace-devel
BuildRequires:  libmm-qt-devel >= 1.0.2
BuildRequires:  libnm-qt-devel >= 2:0.9.8.2
BuildRequires:  pkgconfig(NetworkManager) >= 0.9.8
BuildRequires:  pkgconfig(ModemManager) >= 1.0.0
BuildRequires:  pkgconfig(libnm-glib) pkgconfig(libnm-util)
%if 0%{?fedora} || 0%{?epel}
BuildRequires:  pkgconfig(openconnect) >= 4.00
%endif

Requires:  NetworkManager >= 0.9.8
Requires:  libnm-qt >= 2:0.9.8.2

Obsoletes: kde-plasma-networkmanagement < 1:0.9.1.0
Obsoletes: kde-plasma-networkmanagement-libs < 1:0.9.1.0
Provides:  kde-plasma-networkmanagement = 1:%{version}-%{release}
Provides:  kde-plasma-networkmanagement-libs = 1:%{version}-%{release}

%description
Plasma applet and editor for managing your network connections in KDE 4 using
the default NetworkManager service.

# Required for properly working GMS/CDMA connections
%package mobile
Summary: Mobile support for %{name}
Requires:  ModemManager
Requires:  mobile-broadband-provider-info
Requires:  libmm-qt >= 1.0.2
Obsoletes: kde-plasma-networkmanagement-mobile < 1:0.9.1.0
Provides:  kde-plasma-networkmanagement-mobile = 1:%{version}-%{release}
%description mobile
%{summary}.

%if 0%{?fedora} || 0%{?epel}
%package openvpn
Summary:        OpenVPN support for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release} 
Requires:       NetworkManager-openvpn
Obsoletes:      kde-plasma-networkmanagement-openvpn < 1:0.9.1.0
Provides:       kde-plasma-networkmanagement-openvpn = 1:%{version}-%{release}
%description openvpn
%{summary}.

%package vpnc
Summary:        Vpnc support for %{name} 
Requires:       %{name}%{?_isa} = %{version}-%{release} 
Requires:       NetworkManager-vpnc
Obsoletes:      kde-plasma-networkmanagement-vpnc < 1:0.9.1.0
Provides:       kde-plasma-networkmanagement-vpnc = 1:%{version}-%{release}
%description vpnc
%{summary}.

%package openconnect
Summary:        OpenConnect support for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release} 
Requires:       NetworkManager-openconnect
Obsoletes:      kde-plasma-networkmanagement-openconnect < 1:0.9.1.0
Provides:       kde-plasma-networkmanagement-openconnect = 1:%{version}-%{release}
%description openconnect
%{summary}.

%package openswan
Summary:        Openswan support for %{name} 
Requires:       %{name}%{?_isa} = %{version}-%{release} 
Requires:       NetworkManager-openswan
%description openswan
%{summary}.

%package strongswan
Summary:        Strongswan support for %{name} 
Requires:       %{name}%{?_isa} = %{version}-%{release} 
Requires:       strongswan
%description strongswan
%{summary}.

%package l2tp
Summary:        L2TP support for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release} 
Requires:       NetworkManager-l2tp
%description l2tp
%{summary}.

%package pptp
Summary:        PPTP support for %{name} 
Requires:       %{name}%{?_isa} = %{version}-%{release} 
Requires:       NetworkManager-pptp
Obsoletes:      kde-plasma-networkmanagement-pptp < 1:0.9.1.0
Provides:       kde-plasma-networkmanagement-pptp = 1:%{version}-%{release}
%description pptp
%{summary}.
%endif

%prep
%setup -qn plasma-nm-%{version}


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
rm -rf %{buildroot}

make install/fast  DESTDIR=%{buildroot} -C %{_target_platform}
magic_rpm_clean.sh

%find_lang plasma_applet_org.kde.networkmanagement
%find_lang plasmanetworkmanagement-kded
%find_lang kde-nm-connection-editor
%find_lang libplasmanetworkmanagement-editor
%find_lang plasmanetworkmanagement_vpncui
%find_lang plasmanetworkmanagement_openvpnui
%find_lang plasmanetworkmanagement_openconnectui
%find_lang plasmanetworkmanagement_openswanui
%find_lang plasmanetworkmanagement_strongswanui
%find_lang plasmanetworkmanagement_l2tpui
%find_lang plasmanetworkmanagement_pptpui

# migrate to nm plasmoid
install -m644 -p -D %{SOURCE10} %{buildroot}%{_kde4_appsdir}/plasma-desktop/updates/01-fedora-plasma-nm.js

# clean unpackaged VPN related files in RHEL
%if 0%{?rhel}
rm -fv %{buildroot}%{_kde4_libdir}/kde4/networkmanagement_open*
rm -fv %{buildroot}%{_kde4_libdir}/kde4/networkmanagement_vpnc*
rm -fv %{buildroot}%{_kde4_libdir}/kde4/networkmanagement_l2tp*
rm -fv %{buildroot}%{_kde4_libdir}/kde4/networkmanagement_pptp*
rm -fv %{buildroot}%{_kde4_datadir}/kde4/services/networkmanagement_open*
rm -fv %{buildroot}%{_kde4_datadir}/kde4/services/networkmanagement_vpnc*
rm -fv %{buildroot}%{_kde4_datadir}/kde4/services/networkmanagement_l2tp*
rm -fv %{buildroot}%{_kde4_datadir}/kde4/services/networkmanagement_pptp*
%endif

%post
touch --no-create %{_kde4_iconsdir}/oxygen &> /dev/null || :

%posttrans
gtk-update-icon-cache %{_kde4_iconsdir}/oxygen &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
touch --no-create %{_kde4_iconsdir}/oxygen &> /dev/null || :
gtk-update-icon-cache %{_kde4_iconsdir}/oxygen &> /dev/null || :
fi

%files -f plasma_applet_org.kde.networkmanagement.lang -f plasmanetworkmanagement-kded.lang -f kde-nm-connection-editor.lang -f libplasmanetworkmanagement-editor.lang
%defattr(-,root,root,-)
# kde-nm-connection-editor
%{_kde4_bindir}/kde-nm-connection-editor
%{_kde4_libdir}/libplasmanetworkmanagement-editor.so
%{_kde4_datadir}/apps/kde-nm-connection-editor/kde-nm-connection-editorui.rc
%{_kde4_datadir}/applications/kde4/kde-nm-connection-editor.desktop
# plasma-nm applet
%{_kde4_libdir}/kde4/imports/org/kde/networkmanagement/libplasmanetworkmanagementplugins.so
%{_kde4_libdir}/kde4/imports/org/kde/networkmanagement/qmldir
%dir %{_kde4_datadir}/apps/plasma/plasmoids/org.kde.networkmanagement/
%{_kde4_datadir}/apps/plasma/plasmoids/org.kde.networkmanagement/contents
%{_kde4_datadir}/apps/plasma/plasmoids/org.kde.networkmanagement/metadata.desktop
%{_kde4_datadir}/kde4/services/plasma-applet-networkmanagement.desktop
%{_kde4_libdir}/kde4/plugins/designer/plasmanetworkmanagementwidgets.so
%{_kde4_appsdir}/desktoptheme/default/icons/plasma-networkmanagement2.svgz
%{_kde4_iconsdir}/oxygen/*/*/*
%{_kde4_appsdir}/plasma-desktop/updates/*.js
# plasma-nm notifications
%{_kde4_datadir}/kde4/services/networkmanagement_notifications.desktop
%{_kde4_libdir}/kde4/networkmanagement_notifications.so
%{_kde4_datadir}/apps/networkmanagement/networkmanagement.notifyrc
# plasma-nm kded
%{_kde4_libdir}/kde4/kded_networkmanagement.so
%{_kde4_datadir}/kde4/services/kded/networkmanagement.desktop
# plasma-nm other
%{_kde4_libdir}/libplasmanetworkmanagement-internal.so
%{_kde4_datadir}/kde4/servicetypes/plasma-networkmanagement-vpnuiplugin.desktop


%files mobile

%if 0%{?fedora} || 0%{?epel}
%files openvpn -f plasmanetworkmanagement_openvpnui.lang
%{_kde4_libdir}/kde4/plasmanetworkmanagement_openvpnui.so
%{_kde4_datadir}/kde4/services/plasmanetworkmanagement_openvpnui.desktop

%files vpnc -f plasmanetworkmanagement_vpncui.lang
%{_kde4_libdir}/kde4/plasmanetworkmanagement_vpncui.so
%{_kde4_datadir}/kde4/services/plasmanetworkmanagement_vpncui.desktop

%files openconnect -f plasmanetworkmanagement_openconnectui.lang
%{_kde4_libdir}/kde4/plasmanetworkmanagement_openconnectui.so
%{_kde4_datadir}/kde4/services/plasmanetworkmanagement_openconnectui.desktop

%files openswan -f plasmanetworkmanagement_openswanui.lang
%{_kde4_libdir}/kde4/plasmanetworkmanagement_openswanui.so
%{_kde4_datadir}/kde4/services/plasmanetworkmanagement_openswanui.desktop

%files strongswan -f plasmanetworkmanagement_strongswanui.lang
%{_kde4_libdir}/kde4/plasmanetworkmanagement_strongswanui.so
%{_kde4_datadir}/kde4/services/plasmanetworkmanagement_strongswanui.desktop

%files l2tp -f plasmanetworkmanagement_l2tpui.lang
%{_kde4_libdir}/kde4/plasmanetworkmanagement_l2tpui.so
%{_kde4_datadir}/kde4/services/plasmanetworkmanagement_l2tpui.desktop

%files pptp -f plasmanetworkmanagement_pptpui.lang
%{_kde4_libdir}/kde4/plasmanetworkmanagement_pptpui.so
%{_kde4_datadir}/kde4/services/plasmanetworkmanagement_pptpui.desktop
%endif

%changelog
* Fri Jun 06 2014 Liu Di <liudidi@gmail.com> - 0.9.3.4-7.20140520git043bbae
- 为 Magic 3.0 重建

* Fri Jun 06 2014 Liu Di <liudidi@gmail.com> - 0.9.3.4-6.20140520git043bbae
- 为 Magic 3.0 重建

* Fri Jun 06 2014 Liu Di <liudidi@gmail.com> - 0.9.3.4-5.20140520git043bbae
- 为 Magic 3.0 重建

* Fri Jun 06 2014 Liu Di <liudidi@gmail.com> - 0.9.3.4-4.20140520git043bbae
- 为 Magic 3.0 重建

* Thu May 29 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0.9.3.4-3.20140522git043bbae
- fix libnm-qt versioned dependencies (missing Epoch)

* Fri May 23 2014 Jan Grulich <jgrulich@redhat.com> - 0.9.3.4-2.20140522git043bbae
- Update translations

* Thu May 22 2014 Jan Grulich <jgrulich@redhat.com> - 0.9.3.4-1.20140522git043bbae
- Update to 0.9.3.4 (git snapshot)

* Tue Apr 15 2014 Jan Grulich <jgrulich@redhat.com> - 0.9.3.3-4
- use correct bluetooth icon

* Mon Mar 10 2014 Jan Grulich <jgrulich@redhat.com> - 0.9.3.3-3
- fix connection status for mobile connections

* Fri Mar 07 2014 Jan Grulich <jgrulich@redhat.com> - 0.9.3.3-2
- fix build with openconnect

* Wed Feb 26 2014 Jan Grulich <jgrulich@redhat.com> - 0.9.3.3-1
- Update to 0.9.3.3

* Thu Feb 13 2014 Rex Dieter <rdieter@fedoraproject.org> - 0.9.3.2-4
- add icon scriptlets

* Fri Jan 03 2014 Jan Grulich <jgrulich@redhat.com> - 0.9.3.2-3
- More upstream fixes

* Thu Jan 02 2014 Jan Grulich <jgrulich@redhat.com> - 0.9.3.2-2
- Pickup some upstream fixes

* Thu Nov 21 2013 Jan Grulich <jgrulich@redhat.com> - 0.9.3.2-1
- Update to 0.9.3.2

* Wed Oct 30 2013 Jan Grulich <jgrulich@redhat.com> - 0.9.3.1-6
- add some upstream fixes and changes

* Wed Oct 23 2013 Jan Grulich <jgrulich@redhat.com> - 0.9.3.1-5
- pickup some upstream fixes

* Mon Oct 14 2013 Jan Grulich <jgrulich@redhat.com> - 0.9.3.1-4
- Update to 0.9.3.1

* Mon Oct 14 2013 Jan Grulich <jgrulich@redhat.com> - 0.9.3.1-3.20131009git82dab6e
- Fix obsoletes

* Thu Oct 10 2013 Jan Grulich <jgrulich@redhat.com> - 0.9.3.1-2.20131009git82dab6e
- Add obsoletes for kde-plasma-networkmanagement
- Add rename script

* Wed Oct 9 2013 Jan Grulich <jgrulich@redhat.com> - 0.9.3.1-1.20131009git82dab6e
- Update to current git snapshot

* Tue Oct 1 2013 Jan Grulich <jgrulich@redhat.com> - 0.9.3.0-7
- Make ModemManager as runtime dependency installed with -mobile subpkg
- Resolves #1013838

* Wed Sep 11 2013 Jan Grulich <jgrulich@redhat.com> - 0.9.3.0-6
- Update to first official release (0.9.3.0)

* Tue Aug 20 2013 Jan Grulich <jgrulich@redhat.com> - 0.9.3.0-5.20130812git707b2b
- add javascript to automatically add plasma-nm to the systray

* Mon Aug 12 2013 Lukas Tinkl <ltinkl@redhat.com> - 0.9.3.0-4.20130812git707b2b
- Update to current git snapshots
- simplified applet based on usability study from Akademy

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3.0-3.20130613git6a4c385
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jun 13 2013 Jan Grulich <jgrulich@redhat.com> - 0.9.3.0-2.20130613git6a4c385
- Update to the current git snapshot
- Add Openswan, Openconnect, L2TP, PPTP VPN plugins

* Tue Jun 4 2013 Jan Grulich <jgrulich@redhat.com> - 0.9.3.0-1.20130604git649e5f4
- Initial package
- Based on git snapshot 649e5f4b3e5b4f30df19aa0f908234355912eea7
