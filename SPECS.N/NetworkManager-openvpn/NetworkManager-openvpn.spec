%global snapshot .git20140128

Summary:   NetworkManager VPN plugin for OpenVPN
Name:      NetworkManager-openvpn
Epoch:     1
Version:   0.9.9.0
Release:   0.1%{snapshot}%{?dist}
License:   GPLv2+
URL:       http://www.gnome.org/projects/NetworkManager/
Group:     System Environment/Base
Source0:   http://ftp.gnome.org/pub/GNOME/sources/%{name}/0.9/%{name}-%{version}%{snapshot}.tar.bz2

BuildRequires: gtk3-devel
BuildRequires: dbus-devel
BuildRequires: NetworkManager-devel
BuildRequires: NetworkManager-glib-devel
BuildRequires: glib2-devel
BuildRequires: libtool intltool gettext
BuildRequires: libgnome-keyring-devel
BuildRequires: libnm-gtk-devel >= 0.9.9.0
BuildRequires: libsecret-devel

Requires: gtk3
Requires: dbus
Requires: NetworkManager
Requires: openvpn
Requires: shared-mime-info
Requires: libgnome-keyring
Obsoletes: NetworkManager-openvpn < 1:0.9.8.2-3

%global _privatelibs libnm-openvpn-properties[.]so.*
%global __provides_exclude ^(%{_privatelibs})$
%global __requires_exclude ^(%{_privatelibs})$

%description
This package contains software for integrating VPN capabilities with
the OpenVPN server with NetworkManager.

%package -n NetworkManager-openvpn-gnome
Summary: NetworkManager VPN plugin for OpenVPN - GNOME files
Group:   System Environment/Base

Requires: NetworkManager-openvpn = %{epoch}:%{version}-%{release}
%if 0%{?fedora} > 17
Requires: nm-connection-editor
%else
Requires: NetworkManager-gnome
%endif
Obsoletes: NetworkManager-openvpn < 1:0.9.8.2-3

%description -n NetworkManager-openvpn-gnome
This package contains software for integrating VPN capabilities with
the OpenVPN server with NetworkManager (GNOME files).

%prep
%setup -q -n %{name}-%{version}

%build
if [ ! -f configure ]; then
  ./autogen.sh
fi
%configure \
	--disable-static \
	--disable-dependency-tracking \
	--enable-more-warnings=yes \
	--with-gnome
make %{?_smp_mflags}

%check
make check

%install
make install DESTDIR=%{buildroot} INSTALL="%{__install} -p"

rm -f %{buildroot}%{_libdir}/NetworkManager/lib*.la

%find_lang %{name}

%files -f %{name}.lang
%doc COPYING AUTHORS README ChangeLog
%{_sysconfdir}/dbus-1/system.d/nm-openvpn-service.conf
%{_sysconfdir}/NetworkManager/VPN/nm-openvpn-service.name
%{_libexecdir}/nm-openvpn-service
%{_libexecdir}/nm-openvpn-auth-dialog
%{_libexecdir}/nm-openvpn-service-openvpn-helper

%files -n NetworkManager-openvpn-gnome
%doc COPYING AUTHORS README ChangeLog
%{_libdir}/NetworkManager/lib*.so*
%dir %{_datadir}/gnome-vpn-properties/openvpn
%{_datadir}/gnome-vpn-properties/openvpn/nm-openvpn-dialog.ui

%changelog
* Tue Jan 28 2014 Dan Williams <dcbw@redhat.com> - 1:0.9.9.0-0.1
- core: add support for IPv6 inside tunnels (rh #1033868)
- auth: add support for interactive mode

* Tue Jan  7 2014 Jiří Klimeš <jklimes@redhat.com> - 1:0.9.8.2-4
- properties: fix an endless loop when selecting PKCS12 file (rh #997255)

* Fri Jul 26 2013 Jiří Klimeš <jklimes@redhat.com> - 1:0.9.8.2-3
- Fixing Obsoletes to ensure NetworkManager-openvpn-gnome installs on update (rh #988131)

* Wed Jul 17 2013 Stef Walter <stefw@gnome.org> - 1:0.9.8.2-2
- Depend on libgnome-keyring (the client library), not gnome-keyring (daemon) (rh #811931)

* Tue Jul 16 2013 Jiří Klimeš <jklimes@redhat.com> - 1:0.9.8.2-1
- Update to 0.9.8.2 release

* Sat Apr 06 2013 Dan Fruehauf <malkodan@gmail.com> - 1:0.9.8.0-1
- Refactored spec file

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.9.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Sep 28 2012 Dan Williams - 1:0.9.6.0-1
- Update to 0.9.6.0

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.9.3.997-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Ville Skyttä <ville.skytta@iki.fi> - 1:0.9.3.997-2
- Remove unnecessary ldconfig calls from scriptlets (#737330).
- Escape macros in changelog.

* Mon Mar 19 2012 Dan Williams <dcbw@redhat.com> - 1:0.9.3.997-1
- Update to 0.9.3.997 (0.9.4-rc1)

* Fri Mar  2 2012 Dan Williams <dcbw@redhat.com> - 1:0.9.3.995-1
- Update to 0.9.3.995 (0.9.4-beta1)
- ui: allow setting Cipher and HMAC options in Static Key mode
- ui: add support for external UI mode, eg GNOME Shell

* Sun Feb 26 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1:0.9.0-4
- Update for unannounced gnome-keyring devel changes

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 07 2011 Adam Jackson <ajax@redhat.com> 0.9.0-2
- Rebuild for new libpng
- Build with -Wno-error=deprecated-declarations for now

* Fri Aug 26 2011 Dan Williams <dcbw@redhat.com> - 1:0.9.0-1
- ui: updated translations

* Thu Jul 21 2011 Dan Williams <dcbw@redhat.com> - 1:0.8.9997-2
- ui: ensure secrets are saved when required and not saved when not required
- ui: add explicit secret saving options

* Thu Jul 07 2011 Dan Williams <dcbw@redhat.com> - 1:0.8.9997-1
- Update to 0.8.9997 (0.9-rc3)
- ui: ensure saved secrets are passed back to NM
- ui: updated translations
- ui: add RSA-MD4 HMAC digest algorithm

* Tue May 03 2011 Dan Williams <dcbw@redhat.com> - 1:0.8.999-1
- Update to 0.8.999 (0.9-rc2)
- ui: default to user-stored secrets for new connections
- ui: updated translations
- ui: fix HTTP proxy authentication autodetection during import

* Tue Apr 05 2011 Dan Williams <dcbw@redhat.com> - 1:0.8.998-1.git20110405
- Update to 0.8.998 (0.9.0-rc1)
- Fix importing of configs with TLS Auth direction
- Fix handling of user-session-owned secrets
- Export HTTP Proxy auth file when appropriate

* Thu Mar 24 2011 Dan Williams <dcbw@redhat.com> - 1:0.8.995-1
- Update to 0.8.995 (0.9-beta1)

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jul 27 2010 Dan Williams <dcbw@redhat.com> - 1:0.8.1-1
- Update to 0.8.1 release
- Updated translations
- Fix crash when checking whether some private keys are encrypted

* Wed Jun  9 2010 Dan Williams <dcbw@redhat.com> - 1:0.8.1-0.1.git20100609
- Add support for PKCS#8 private keys
- Add support for unencrypted private keys (rh #497454)

* Sun Apr 11 2010 Dan Williams <dcbw@redhat.com> - 1:0.8-2
- Add support for more HMAC authentication algorithms
- Fix requests for private key passwords for certificates (rh #549961)

* Tue Mar 2 2010 Huzaifa Sidhpurwala <huzaifas@redhat.com> - 1:0.8-1
- Fix handling of remote peer address for shared-key connections (rh #564068)
- Add support for the "TLS Remote", tun-mtu, fragment, and mss-fix options
- Various import/export fixes (tls-auth, port/rport)
- Add support for PKCS#12 encoded certificates and private keys
- Update to 0.8

* Mon Dec 14 2009 Dan Williams <dcbw@redhat.com> - 1:0.7.997-1
- Implement export capability
- Fix some import bugs
- Correctly handle PEM certificates without an ending newline (rh #507315)

* Mon Oct  5 2009 Dan Williams <dcbw@redhat.com> - 1:0.7.996-4.git20090923
- Rebuild for updated NetworkManager

* Wed Sep 23 2009 Dan Williams <dcbw@redhat.com> - 1:0.7.996-3.git20090923
- Add GUI option for reneg-sec config option (rh #490971)

* Mon Sep 21 2009 Dan Williams <dcbw@redhat.com> - 1:0.7.996-2
- Rebuild for updated NetworkManager

* Fri Aug 28 2009 Dan Williams <dcbw@redhat.com> - 1:0.7.996-1
- Rebuild for updated NetworkManager

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.7.1-2.git20090714
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 14 2009 Dan Williams <dcbw@redhat.com> - 1:0.7.1-1.20090714
- Fix a misconfiguration with 'subnet' topology
- Fix detection of password requests by the OpenVPN management interface

* Mon Jul 13 2009 Dan Williams <dcbw@redhat.com> - 1:0.7.1-1.20090713
- Update to 0.7.1
- Translation updates

* Thu Mar  5 2009 Dan Williams <dcbw@redhat.com> 1:0.7.0.99-1
- Update to 0.7.1rc3

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.7.0.97-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 19 2009 Dan Williams <dcbw@redhat.com> 1:0.7.0.97-1
- Update to 0.7.1rc1
- Handle HMAC Authentication (--auth)
- Handle TAP device subnet masks correctly
- Don't segfault if the connection type is invalid

* Sat Jan  3 2009 Dan Williams <dcbw@redhat.com> 1:0.7.0-18.svn11
- Rebuild for updated NetworkManager
- Fix some specfile issues (rh #477149)

* Sat Dec 20 2008 Christoph Höger <choeger@cs.tu-berlin.de> 0.7.0-17.svn4326
- removed libpng-devel from BuildRequires, added %%{_datadir}/gnome-vpn-properties/openvpn/ (rh #477149)

* Fri Nov 21 2008 Dan Williams <dcbw@redhat.com> 1:0.7.0-16.svn4326
- Rebuild for updated NetworkManager

* Mon Oct 27 2008 Dan Williams <dcbw@redhat.com> 1:0.7.0-16.svn4229
- Rebuild for updated NetworkManager

* Sun Oct 12 2008 Dan Williams <dcbw@redhat.com> 1:0.7.0-16.svn4175
- Rebuild for updated NetworkManager
- Allow changing passwords from the connection editor
- Honor OpenVPN's 'route-vpn-gateway' option

* Tue Sep 30 2008 Dan Williams <dcbw@redhat.com> 1:0.7.0-16.svn4027
- Fix order of Password TLS certificate choosers (rh #464765)
- Use %%find_lang for locale-specific files (rh #448551)
- Fix --script-security issues with OpenVPN 2.1-rc9 and later (rh #460754)

* Fri Aug 29 2008 Dan Williams <dcbw@redhat.com> 1:0.7.0-15.svn4027
- Rebuild for updated NetworkManager

* Mon Aug 11 2008 Dan Williams <dcbw@redhat.com> 1:0.7.0-15.svn3930
- Rebuild for updated NetworkManager

* Thu Jul 24 2008 Dan Williams <dcbw@redhat.com> 1:0.7.0-15.svn3846
- Rebuild to sync with F9 release number

* Thu Jul 24 2008 Dan Williams <dcbw@redhat.com> 1:0.7.0-11.svn3846
- Fix TLS Authentication direction combo
- Only update settings if the advanced dialog's OK button is pressed

* Fri Jul 18 2008 Dan Williams <dcbw@redhat.com> 1:0.7.0-11.svn3832
- Update for NM netmask -> prefix changes

* Wed Jul 02 2008 Dan Williams <dcbw@redhat.com> 1:0.7.0-11.svn3801
- Update for moving VPN editing into connection manager
- Import OpenVPN configuration files rather than old custom format

* Mon May 05 2008 Dan Williams <dcbw@redhat.com> 1:0.7.0-10.svn3632
- Fix issue with location of the VPN plugin

* Thu May 01 2008 Dan Williams <dcbw@redhat.com> 1:0.7.0-10.svn3627
- Update for compat with new NM bits

* Wed Apr 23 2008 Christoph Höger <choeger@cs.tu-berlin.de> 1:0.7.0-10.svn3549
- (Hopefully) Fix generation of nm-openvpn-service.name (#443389)
 
* Wed Apr 09 2008 Dan Williams <dcbw@redhat.com> 1:0.7.0-9.svn3549
- Update for compat with new NM bits

* Mon Mar 03 2008 Tim Niemueller <tim@niemueller.de> 1:0.7.0-9.svn3302
- Mute %%post and %%postun scripts

* Fri Feb 08 2008 Tim Niemueller <tim@niemueller.de> 1:0.7.0-8.svn3302
- Update to latest SVN snapshot
- Fixes rhbz#429816 (port was not saved correctly)
- Respects DNS search string from OpenVPN server

* Fri Jan 18 2008 Tim Niemueller <tim@niemueller.de> 1:0.7.0-7.svn3169
- Use install -p during "make install" to fix #342701

* Thu Dec 13 2007 Tim Niemueller <tim@niemueller.de> 1:0.7.0-6.svn3169
- Update to latest SVN snapshot

* Thu Dec  6 2007 Dan Williams <dcbw@redhat.com> 1:0.7.0-5.svn3140
- Update to latest SVN snapshot to get stuff working

* Fri Nov 23 2007 Tim Niemueller <tim@niemueller.de> 1:0.7.0-4.svn3047
- BuildRequire libtool and glib2-devel since we call autogen.sh now

* Fri Nov 23 2007 Tim Niemueller <tim@niemueller.de> 1:0.7.0-3.svn3047
- Fixed #320941
- Call autogen, therefore BuildRequire gnome-common
- Use plain 3047 from repo and use a patch, we cannot use trunk at the
  moment since it is in flux and incompatible with NM available for F8

* Wed Oct 31 2007 Tim Niemueller <tim@niemueller.de> 1:0.7.0-2.svn3047.fc8
- BuildRequire gettext

* Tue Oct 30 2007 Tim Niemueller <tim@niemueller.de> 1:0.7.0-1.svn3047.fc8
- Upgrade to trunk, needed to be compatible with NM 0.7.0, rebuild for F-8

* Fri Sep 15 2006 Tim Niemueller <tim@niemueller.de> 0.3.2-7
- Rebuild for FC6

* Sat Aug 19 2006 Tim Niemueller <tim@niemueller.de> 0.3.2-5
- Added perl-XML-Parser as a build requirement, needed for intltool

* Tue Aug 15 2006 Tim Niemueller <tim@niemueller.de> 0.3.2-4
- Added instructions how to build the source package
- removed a rm line

* Wed Aug 09 2006 Tim Niemueller <tim@niemueller.de> 0.3.2-3
- Added URL

* Fri Aug 04 2006 Tim Niemueller <tim@niemueller.de> 0.3.2-2
- Upgrade to current upstream version (0.3.2 on 0.6 branch)

* Mon Jul 10 2006 Tim Niemueller <tim@niemueller.de> 0.3.2-1
- Upgraded to 0.3.2 for 0.6 branch

* Tue Dec 06 2005 Tim Niemueller <tim@niemueller.de> 0.3-1
- Initial revision based on NetworkManager-vpnc spec

