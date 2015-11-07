%global snapshot %{nil}
%global ppp_version %(rpm -q ppp --queryformat '%{VERSION}')

Summary:   NetworkManager VPN plugin for PPTP
Summary(zh_CN.UTF-8): NetWorkManager 的 PPTP VPN 插件
Name:      NetworkManager-pptp
Epoch:     1
Version:	1.0.6
Release:	2%{?dist}
License:   GPLv2+
URL:       http://www.gnome.org/projects/NetworkManager/
Group:     System Environment/Base
Group(zh_CN.UTF-8): 系统环境/基本
%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
Source0:   http://ftp.gnome.org/pub/GNOME/sources/%{name}/%{majorver}/%{name}-%{version}%{snapshot}.tar.xz

BuildRequires: gtk3-devel
BuildRequires: dbus-devel
BuildRequires: NetworkManager-devel
BuildRequires: NetworkManager-glib-devel
BuildRequires: glib2-devel
BuildRequires: ppp-devel
BuildRequires: libtool intltool gettext
BuildRequires: libgnome-keyring-devel

Requires: gtk3
Requires: dbus
Requires: NetworkManager
Requires: pptp
Requires: ppp
Requires: shared-mime-info
Requires: libgnome-keyring
Obsoletes: NetworkManager-pptp < 1:0.9.8.2-3

%global _privatelibs libnm-pptp-properties[.]so.*
%global __provides_exclude ^(%{_privatelibs})$
%global __requires_exclude ^(%{_privatelibs})$

%description
This package contains software for integrating VPN capabilities with
the PPTP server with NetworkManager.

%description -l zh_CN.UTF-8
NetWorkManager 的 PPTP VPN 插件。

%package -n NetworkManager-pptp-gnome
Summary: NetworkManager VPN plugin for PPTP - GNOME files
Summary(zh_CN.UTF-8): NetWorkManager 的 PPTP VPN 插件 - GNOME 文件 
Group:   System Environment/Base
Group(zh_CN.UTF-8): 系统环境/基本

Requires: NetworkManager-pptp = %{epoch}:%{version}-%{release}
Requires: nm-connection-editor
Obsoletes: NetworkManager-pptp < 1:0.9.8.2-3

%description -n NetworkManager-pptp-gnome
This package contains software for integrating VPN capabilities with
the PPTP server with NetworkManager (GNOME files).

%description -n NetworkManager-pptp-gnome -l zh_CN.UTF-8
NetWorkManager 的 PPTP VPN 插件 - GNOME 文件。

%prep
%setup -q -n %{name}-%{version}

%build
if [ ! -f configure ]; then
  ./autogen.sh
fi
%configure \
	--disable-static \
	--enable-more-warnings=yes \
	--with-pppd-plugin-dir=%{_libdir}/pppd/%{ppp_version}
make %{?_smp_mflags}

%check
make check

%install
make install DESTDIR=%{buildroot} INSTALL="%{__install} -p"

rm -f %{buildroot}%{_libdir}/NetworkManager/lib*.la
rm -f %{buildroot}%{_libdir}/NetworkManager/lib*.a
rm -f %{buildroot}%{_libdir}/pppd/%{ppp_version}/*.la
magic_rpm_clean.sh
%find_lang %{name}

%files -f %{name}.lang
%doc COPYING AUTHORS README ChangeLog
%{_sysconfdir}/dbus-1/system.d/nm-pptp-service.conf
%{_sysconfdir}/NetworkManager/VPN/nm-pptp-service.name
%{_libexecdir}/nm-pptp-service
%{_libexecdir}/nm-pptp-auth-dialog
%{_libdir}/pppd/%{ppp_version}/nm-pptp-pppd-plugin.so

%files -n NetworkManager-pptp-gnome
%doc COPYING AUTHORS README ChangeLog
%{_libdir}/NetworkManager/lib*.so*
%dir %{_datadir}/gnome-vpn-properties/pptp
%{_datadir}/gnome-vpn-properties/pptp/nm-pptp-dialog.ui

%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 1:1.0.6-2
- 更新到 1.0.6

* Fri Jan 16 2015 Liu Di <liudidi@gmail.com> - 1:1.0.0-1
- 更新到 1.0.0

* Fri Jul 26 2013 Jiří Klimeš <jklimes@redhat.com> - 1:0.9.8.2-3
- Fixing Obsoletes to ensure NetworkManager-pptp-gnome installs on update (rh #986368)

* Thu Jul 11 2013 Stef Walter <stefw@gnome.org> - 1:0.9.8.2-2
- Depend on libgnome-keyring (the client library), not gnome-keyring (daemon) (rh #811930)

* Thu Jul 11 2013 Jiří Klimeš <jklimes@redhat.com> - 1:0.9.8.2-1
- Update to 0.9.8.2 release

* Sun Apr 07 2013 Dan Fruehauf <malkodan@gmail.com> - 1:0.9.8.0-1
- Refactored spec file

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.9.3.997-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.9.3.997-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Ville Skyttä <ville.skytta@iki.fi> - 1:0.9.3.997-2
- Remove unnecessary ldconfig calls from scriptlets (#737333).

* Mon Mar 19 2012 Dan Williams <dcbw@redhat.com> - 1:0.9.3.997-1
- Update to 0.9.3.997 (0.9.4-rc1)

* Fri Mar  2 2012 Dan Williams <dcbw@redhat.com> - 1:0.9.3.995-1
- Update to 0.9.3.995 (0.9.4-beta1)
- ui: add support for external UI mode, eg GNOME Shell
- ui: tooltips now refer to pppd/pptp config options

* Thu Mar  1 2012 Bill Nottingham <notting@redhat.com> - 1:0.9.0-5
- Remove obsolete and broken gtk2 requirement

* Sun Feb 26 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1:0.9.0-4
- Update for unannounced gnome-keyring devel changes

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 07 2011 Adam Jackson <ajax@redhat.com> 0.9.0-2
- Rebuild for new libpng
- Build with -Wno-error=deprecated-declarations for now

* Fri Aug 26 2011 Dan Williams <dcbw@redhat.com> - 1:0.9.0-1
- Update to 0.9.0 release
- ui: updated translations

* Thu Jul 21 2011 Dan Williams <dcbw@redhat.com> - 1:0.8.999-2.git20110721
- ui: ensure secrets are saved when required and not saved when not required

* Tue May 03 2011 Dan Williams <dcbw@redhat.com> - 1:0.8.999-1
- Update to 0.8.999 (0.9-rc2)
- ui: default to user-stored secrets for new connections
- ui: updated translations

* Tue Apr 05 2011 Dan Williams <dcbw@redhat.com> - 1:0.8.998-1
- Update to 0.8.998 (0.9.0-rc1)
- Fix issues with secrets flags and password saving/retrieval
- Fix issues with PPTP pools using the same DNS name for different servers

* Sat Mar 26 2011 Christopher Aillon <caillon@redhat.com> - 1:0.8.995-1
- Update to 0.8.995

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jul 27 2010 Dan Williams <dcbw@redhat.com> - 1:0.8.1-1
- Update to 0.8.1 release
- MPPE auth method UI fixes
- Lower default pptp log level and add debugging capability

* Sun Apr 11 2010 Dan Williams <dcbw@redhat.com> - 1:0.8.0-1
- Fix saving of MPPE security levels
- Updated translations

* Mon Feb  1 2010 Dan Williams <dcbw@redhat.com> - 1:0.7.997-3.git20100120
- Really fix pppd plugin directory path

* Wed Jan 20 2010 Dan Williams <dcbw@redhat.com> - 1:0.7.997-2.git20100120
- Rebuild for new pppd

* Mon Dec 14 2009 Dan Williams <dcbw@redhat.com> - 1:0.7.997-1
- Add debugging helpers
- Fix saving MPPE-related settings from the properties dialog
- Resolve PPTP gateway hostname if necessary

* Mon Oct  5 2009 Dan Williams <dcbw@redhat.com> - 1:0.7.996-4.git20090921
- Rebuild for updated NetworkManager

* Mon Sep 21 2009 Dan Williams <dcbw@redhat.com> - 1:0.7.996-2
- Rebuild for updated NetworkManager

* Fri Aug 28 2009 Dan Williams <dcbw@redhat.com> - 1:0.7.996-1
- Rebuild for updated NetworkManager
- Fix window title of Advanced dialog

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.7.0.99-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.7.0.99-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Mar  5 2009 Dan Williams <dcbw@redhat.com> 1:0.7.0.99-1
- Update to 0.7.1rc3

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.7.0.97-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 19 2009 Dan Williams <dcbw@redhat.com> 1:0.7.0.97-1
- Update to 0.7.1rc1
- Set a reasonable MTU
- Ensure 'noauth' is used
- Fix domain-based logins
- Fix saving MPPE values in connection editor

* Sat Jan  3 2009 Dan Williams <dcbw@redhat.com> 1:0.7.0-1.svn16
- Rebuild for updated NetworkManager
- Fix some specfile issues (rh #477153)
- Allow the EAP authentication method

* Fri Nov 21 2008 Dan Williams <dcbw@redhat.com> 1:0.7.0-12.svn4326
- Rebuild for updated NetworkManager

* Wed Oct 29 2008 Dan Williams <dcbw@redhat.com> 1:0.7.0-12.svn4229
- Fix hang in auth dialog (rh #467007)

* Mon Oct 27 2008 Dan Williams <dcbw@redhat.com> 1:0.7.0-11.svn4229
- Rebuild for updated NetworkManager
- Ensure that certain PPP options are always overriden

* Sun Oct 12 2008 Dan Williams <dcbw@redhat.com> 1:0.7.0-11.svn4178
- Rebuild for updated NetworkManager
- Allow changing passwords from the connection editor

* Sun Oct 05 2008 Lubomir Rintel <lkundrak@v3.sk> 1:0.7.0-11.svn4027
- Add pptp dependency (#465644)

* Fri Aug 29 2008 Dan Williams <dcbw@redhat.com> 1:0.7.0-10.svn4027
- Resurrect from the dead

* Mon Apr 21 2008 Lubomir Kundrak <lkundrak@redhat.com> 0.6.4-2
- Take Dan Horak's review into account (#443807):
- Do not install versioned .so-s for properties module
- Do not do useless ldconfigs
- Remove leftover dependencies

* Mon Apr 21 2008 Lubomir Kundrak <lkundrak@redhat.com> 0.6.4-1
- Branch this for EPEL, go back to:
- 0.6.4
- NetworkManager-pptp from NetworkManager-ppp_vpn
- Install pppd plugin correctly

* Wed Nov 21 2007 Lubomir Kundrak <lkundrak@redhat.com> 0.7.0-0.3.svn3549
- Update against trunk

* Wed Nov 21 2007 Lubomir Kundrak <lkundrak@redhat.com> 0.7.0-0.2.svn3085
- Do not exclude .so for NM, and properly generate the .name file

* Thu Nov 15 2007 Lubomir Kundrak <lkundrak@redhat.com> 0.7.0-0.1.svn3085
- Initial packaging attempt, inspired by NetworkManager-openvpn
- Nearly completly rewritten spec, all bugs in it are solely my responsibility
