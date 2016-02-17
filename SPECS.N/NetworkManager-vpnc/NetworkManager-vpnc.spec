%global snapshot %{nil}

Summary:   NetworkManager VPN plugin for vpnc
Summary(zh_CN.UTF-8): NetworkManaget 的 vpnc 插件
Name:      NetworkManager-vpnc
Epoch:     1
Version:	1.0.0
Release:	5%{?dist}
License:   GPLv2+
URL:       http://www.gnome.org/projects/NetworkManager/
Group:     System Environment/Base
Group(zh_CN.UTF-8): 系统环境/基本
%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
Source0:   https://download.gnome.org/sources/NetworkManager-vpnc/%{majorver}/%{name}-%{version}%{snapshot}.tar.xz

BuildRequires: gtk3-devel
BuildRequires: dbus-devel
BuildRequires: NetworkManager-devel
BuildRequires: NetworkManager-glib-devel >= 1:0.9.9.0
BuildRequires: intltool gettext
BuildRequires: libnm-gtk-devel >= 0.9.9.0
BuildRequires: libsecret-devel

Requires: gtk3
Requires: dbus
Requires: NetworkManager >= 1:0.9.9.0
Requires: vpnc
Requires: shared-mime-info
Requires: gnome-keyring
Obsoletes: NetworkManager-vpnc < 1:0.9.8.2-2

%global _privatelibs libnm-vpnc-properties[.]so.*
%global __provides_exclude ^(%{_privatelibs})$
%global __requires_exclude ^(%{_privatelibs})$

%description
This package contains software for integrating VPN capabilities with
the vpnc server with NetworkManager.

%description -l zh_CN.UTF-8
NetworkManaget 的 vpnc 插件。

%package -n NetworkManager-vpnc-gnome
Summary: NetworkManager VPN plugin for vpnc - GNOME files
Summary(zh_CN.UTF-8): NetworkManaget 的 vpnc 插件 - GNOME 文件
Group:   System Environment/Base
Group(zh_CN.UTF-8): 系统环境/基本

Requires: NetworkManager-vpnc = %{epoch}:%{version}-%{release}
Requires: nm-connection-editor
Obsoletes: NetworkManager-vpnc < 1:0.9.8.2-2

%description -n NetworkManager-vpnc-gnome
This package contains software for integrating VPN capabilities with
the vpnc server with NetworkManager (GNOME files).

%description -n NetworkManager-vpnc-gnome -l zh_CN.UTF-8
NetworkManaget 的 vpnc 插件 - GNOME 文件。

%prep
%setup -q -n %{name}-%{version}


%build
export CFLAGS="$RPM_OPT_FLAGS -Wno-error=deprecated-declarations"
%configure --enable-more-warnings=yes --with-gtkver=3 --with-tests=yes
make %{?_smp_mflags}

%check
make check

%install
make install DESTDIR=%{buildroot} INSTALL="%{__install} -p"

rm -f %{buildroot}%{_libdir}/NetworkManager/lib*.la
rm -f %{buildroot}%{_libdir}/NetworkManager/lib*.a
magic_rpm_clean.sh
%find_lang %{name}


%post
update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -f %{name}.lang

%doc AUTHORS ChangeLog
%{_libexecdir}/nm-vpnc-auth-dialog
%{_sysconfdir}/dbus-1/system.d/nm-vpnc-service.conf
%{_sysconfdir}/NetworkManager/VPN/nm-vpnc-service.name
%{_libexecdir}/nm-vpnc-service
%{_libexecdir}/nm-vpnc-service-vpnc-helper
%{_datadir}/applications/nm-vpnc-auth-dialog.desktop
%{_datadir}/icons/hicolor/48x48/apps/gnome-mime-application-x-cisco-vpn-settings.png

%files -n NetworkManager-vpnc-gnome
%doc AUTHORS ChangeLog
%{_libdir}/NetworkManager/lib*.so*
%dir %{_datadir}/gnome-vpn-properties/vpnc
%{_datadir}/gnome-vpn-properties/vpnc/nm-vpnc-dialog.ui

%changelog
* Mon Feb 15 2016 Liu Di <liudidi@gmail.com> - 1:1.0.0-5
- 为 Magic 3.0 重建

* Mon Feb 15 2016 Liu Di <liudidi@gmail.com> - 1:1.0.0-4
- 为 Magic 3.0 重建

* Wed Nov 11 2015 Liu Di <liudidi@gmail.com> - 1:1.0.6-3
- 为 Magic 3.0 重建

* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 1:1.0.6-2
- 更新到 1.0.6

* Fri Jan 16 2015 Liu Di <liudidi@gmail.com> - 1:1.0.0-3
- 为 Magic 3.0 重建

* Fri Jan 16 2015 Liu Di <liudidi@gmail.com> - 1:1.0.0-2
- 为 Magic 3.0 重建

* Mon Dec 22 2014 Dan Williams <dcbw@redhat.com> - 1:1.0.0-1
- Update to 1.0

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.9.9.0-6.git20140428
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.9.9.0-5.git20140428
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Apr 28 2014 Dan Williams <dcbw@redhat.com> - 1:0.9.9.0-4.git20140428
- Fix interactions with GNOME Shell when no passwords are required (bgo #728681)

* Fri Feb  7 2014 Thomas Haller <thaller@redhat.com> - 1:0.9.9.0-3.git20140131
- Fix passing --pid-file argument to vpnc as separate arguments (rh #1062555)

* Fri Jan 31 2014 Dan Williams <dcbw@redhat.com> - 1:0.9.9.0-2.git20140131
- Fix passing --pid-file argument to vpnc

* Wed Jan 29 2014 Dan Williams <dcbw@redhat.com> - 1:0.9.9.0-1
- Always return found secrets for External UI mode

* Fri Jul 26 2013 Jiří Klimeš <jklimes@redhat.com> - 1:0.9.8.2-2
- Fixing Obsoletes to ensure NetworkManager-vpnc-gnome installs on update (rh #983632)

* Fri Jun  7 2013 Dan Williams <dcbw@redhat.com> - 1:0.9.8.2-1
- Update to 0.9.8.2 release

* Sat Apr 06 2013 Dan Fruehauf <malkodan@gmail.com> - 1:0.9.8.0-1
- Refactored spec file

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.9.3.997-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Ville Skyttä <ville.skytta@iki.fi> - 1:0.9.3.997-2
- Remove unnecessary ldconfig calls from scriptlets (#737331).
- Fix version in gtk3 dependency.

* Mon Mar 19 2012 Dan Williams <dcbw@redhat.com> - 1:0.9.3.997-1
- Update to 0.9.3997 (0.9.4-rc1)
- core: pass all received domains back to NetworkManager
- ui: ensure password request is shown when external UI mode is not used

* Fri Mar  2 2012 Dan Williams <dcbw@redhat.com> - 1:0.9.3.995-1
- Update to 0.9.3.995 (0.9.4-beta1)
- core: add support for Juniper/Netscreen VPN concentrators
- ui: tooltips now refer to vpnc config options
- ui: add support for external UI mode, eg GNOME Shell

* Sun Feb 26 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1:0.9.0-4
- Update for unannounced gnome-keyring devel changes

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 07 2011 Adam Jackson <ajax@redhat.com> 0.9.0-2
- Rebuild for new libpng
- Add -Wno-error=deprecated-declarations for now

* Fri Aug 26 2011 Dan Williams <dcbw@redhat.com> - 1:0.9.0-1
- core: use the right IP prefix for point-to-point tunnels
- ui: fix some translations

* Thu Jul 21 2011 Dan Williams <dcbw@redhat.com> - 1:0.8.999-3
- core: don't claim default route when explicit ones are passed
- core/ui: add support for Hybrid XAUTH (rh #677419)
- ui: ensure secerts are saved when required and not saved when not required
- ui: updated translations

* Sat May 07 2011 Christopher Aillon <caillon@redhat.com> - 1:0.8.999-2
- Update icon cache scriptlet

* Tue May 03 2011 Dan Williams <dcbw@redhat.com> - 1:0.8.999-1
- Update to 0.8.999 (0.9-rc2)
- ui: default to user-stored secrets for new connections
- ui: updated translations

* Tue Apr 05 2011 Dan Williams <dcbw@redhat.com> - 1:0.8.998-1.git20110405
- Update to 0.8.998 (0.9.0-rc1)
- ui: default to user-stored secrets when importing
- ui: add a .desktop file for gnome-shell

* Thu Mar 24 2011 Dan Williams <dcbw@redhat.com> - 1:0.8.996-2
- Rebuild for NM 0.9

* Thu Mar 10 2011 Dan Williams <dcbw@redhat.com> - 1:0.8.996
- Update to 0.8.996 (0.9-beta2)

* Tue Mar 08 2011 Dan Williams <dcbw@redhat.com> - 1:0.8.995
- Update to 0.8.995 (0.9-beta1)

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jul 27 2010 Dan Williams <dcbw@redhat.com> - 1:0.8.1-1
- Update to 0.8.1 release
- Updated translations

* Sun Apr 11 2010 Dan Williams <dcbw@redhat.com> - 1:0.8.0-1
- Handle NAT Traversal importing better
- Default to newer NAT-T instead of deprecated Cisco-UDP
- Add "Force NAT-T" option
- Updated translations

* Mon Dec 14 2009 Dan Williams <dcbw@redhat.com> - 1:0.7.997-1
- Add some debug options (VPNC_DEBUG, --persist)
- Make .desktop file pass validation (rh #489475)

* Mon Sep 21 2009 Dan Williams <dcbw@redhat.com> - 1:0.7.996-3
- Rebuild for updated NetworkManager
- Convert imported files to UTF8 before parsing

* Sun Aug 30 2009 Dan Williams <dcbw@redhat.com> - 1:0.7.996-2
- Fix NM requirement

* Fri Aug 28 2009 Dan Williams <dcbw@redhat.com> - 1:0.7.996-1
- Rebuild for updated NetworkManager
- Allow missing description in imported .pcf files
- Allow the 'Vendor' config option

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
- Handle import/export of "EnableNat", "DHGroup", "SaveUserPassword", and "EnableLocalLAN"

* Sat Jan  3 2009 Dan Williams <dcbw@redhat.com> 1:0.7.0-1
- Rebuild for updated NetworkManager
- Better handling of passwords that shouldn't be saved
- Fix some specfile issues (rh #477151)

* Fri Nov 21 2008 Dan Williams <dcbw@redhat.com> 1:0.7.0-0.11.svn4326
- Rebuild for updated NetworkManager

* Tue Nov 18 2008 Dan Williams <dcbw@redhat.com> 1:0.7.0-0.11.svn4296
- Rebuild for updated NetworkManager

* Mon Nov 17 2008 Dan Williams <dcbw@redhat.com> 1:0.7.0-0.11.svn4293
- Ensure errors are shown when connection fails (rh #331141)
- Fix failures to ask for passwords on connect (rh #429287)
- Fix routing when concentrator specifies routes (rh #449283)
- Pull in upstream support for tokens and not saving passwords

* Mon Oct 27 2008 Dan Williams <dcbw@redhat.com> 1:0.7.0-0.11.svn4229
- Rebuild for updated NetworkManager

* Tue Oct 14 2008 Dan Williams <dcbw@redhat.com> 1:0.7.0-11.svn4175
- Fix password issue with configurations that don't save the user password
	in the keyring (rh #466864)

* Sun Oct 12 2008 Dan Williams <dcbw@redhat.com> 1:0.7.0-10.svn4175
- Rebuild for updated NetworkManager
- Allow changing passwords from the connection editor

* Fri Aug 29 2008 Dan Williams <dcbw@redhat.com> 1:0.7.0-10.svn4024
- Fix regression where username radio buttons were mistakenly shown in the
	auth dialog
- Fix regression where the auth dialog would segfault when cancel was clicked

* Wed Aug 27 2008 Dan Williams <dcbw@redhat.com> 1:0.7.0-10.svn4022
- Rebuild for updated NetworkManager

* Mon Aug 11 2008 Dan Williams <dcbw@redhat.com> 1:0.7.0-10.svn3928
- Rebuild for updated NetworkManager

* Thu Jul 24 2008 Dan Williams <dcbw@redhat.com> 1:0.7.0-10.svn3846
- Rebuild for updated NetworkManager

* Fri Jul 18 2008 Dan Williams <dcbw@redhat.com> 1:0.7.0-10.svn3832
- Update for NM netmask -> prefix changes

* Wed Jul 02 2008 Dan Williams <dcbw@redhat.com> 1:0.7.0-10.svn3801
- Update for moving VPN editing into connection manager
- Add option to disable Dead Peer Detection
- Add option to select NAT Traversal mode

* Thu May 01 2008 Dan Williams <dcbw@redhat.com> 1:0.7.0-7.7.svn3627
- Update for compat with new NM bits

* Wed Apr 09 2008 Dan Williams <dcbw@redhat.com> 1:0.7.0-6.7.svn3549
- Update for compat with new NM bits

* Tue Mar 25 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.6.7.svn3502
- Send suggested MTU to NetworkManager

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1:0.7.0-0.7.7.svn3204
- Autorebuild for GCC 4.3

* Fri Jan  4 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.6.7.svn3204
- Support new vpnc 0.4 Cisco UDP Encapsulation option
- Fix another crash in the properties applet
- Remove upstreamed pcfimport patch

* Mon Nov 26 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.6.3.svn3109
- Rebuild for updated NetworkManager

* Tue Nov 13 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.6.2.svn3083
- Rebuild for updated NetworkManager

* Sat Oct 27 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.4.svn3030
- Fix a crash when editing VPN properties a second time

* Tue Oct 23 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.3.svn3014
- Rebuild

* Wed Oct 17 2007 Bill Nottingham <notting@redhat.com> - 1:0.7.0-0.3.svn2970
- rebuild (#336261)

* Wed Oct 10 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.2.svn2970
- Fix default username

* Fri Sep 28 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.1.svn2914
- Fix .name file on 64-bit systems

* Fri Sep 28 2007 Jesse Keating <jkeating@redhat.com> - 1:0.7.0-0.2.svn2910
- BuildRequire NetworkManager-glib-devel

* Thu Sep 27 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.1.svn2910
- New snapshot; ported to NM 0.7 API

* Fri Aug 17 2007 Denis Leroy <denis@poolshark.org> - 1:0.6.4-4
- Updated License tag
- Added patch to make properties multilib friendly (#243535)

* Thu Mar 22 2007 Denis Leroy <denis@poolshark.org> - 1:0.6.4-3
- Added patch to improve configuration GUI, add NAT traversal and single DES options

* Sun Feb 18 2007 Denis Leroy <denis@poolshark.org> - 1:0.6.4-2
- Readded NAT-keepalive support patch from SVN branch

* Wed Feb 14 2007 Denis Leroy <denis@poolshark.org> - 1:0.6.4-1
- Downgrading to 1:0.6.4 to keep par with core NM version

* Mon Dec  4 2006 Dan Williams <dcbw@redhat.com> - 0.7.0-0.cvs20061204
- Allow "NAT-Keepalive packet interval" config option

* Sat Oct 21 2006 Denis Leroy <denis@poolshark.org> - 0.7.0-0.cvs20060929.3
- Added patch to support saving group password only

* Thu Oct  5 2006 Denis Leroy <denis@poolshark.org> - 0.7.0-0.cvs20060929.2
- Leave .so link alone, needed by nm

* Fri Sep 29 2006 Denis Leroy <denis@poolshark.org> - 0.7.0-0.cvs20060929.1
- Update to CVS snapshot 060929
- Some rpmlint cleanups

* Fri Sep 29 2006 Denis Leroy <denis@poolshark.org> - 0.7.0-0.cvs20060529.4
- Added XML::Parser BR

* Fri Sep 29 2006 Denis Leroy <denis@poolshark.org> - 0.7.0-0.cvs20060529.3
- Added gettext BR

* Wed Sep 27 2006 Warren Togami <wtogami@redhat.com> - 0.7.0-0.cvs20060529.2
- rebuild for FC6

* Thu Jul 20 2006 Warren Togami <wtogami@redhat.com> - 0.7.0-0.cvs20060529.1
- rebuild for new dbus

* Mon May 29 2006 Dan Williams <dcbw@redhat.com> - 0.7.0-0.cvs20060529
- Gnome.org #336913: HIG tweaks for vpn properties pages

* Sun May 21 2006 Dan Williams <dcbw@redhat.com> 0.7.0-0.cvs20060521
- Update to CVS snapshot
- Honor user-specified rekeying intervals

* Mon May 15 2006 Dan Williams <dcbw@redhat.com> 0.6.2-1
- New release for NM 0.6.2 compat

* Fri Apr 21 2006 Dan Williams <dcbw@redhat.com> 0.6.0-3
- Add dist tag to RPM release

* Wed Apr 12 2006 Christopher Aillon <caillon@redhat.com> 0.6.0-2
- Rekey every 2 hours

* Tue Mar 14 2006 Dan Williams <dcbw@redhat.com> - 0.6.0-1
- Update to CVS snapshot of 0.6 for NM compatibility

* Fri Jan 27 2006 Dan Williams <dcbw@redhat.com> - 0.5.0-1
- CVS snapshot for compatibility new NetworkManager

* Tue Dec  6 2005 Jeremy Katz <katzj@redhat.com> - 0.3-3
- rebuild for new dbus

* Mon Oct 17 2005 Dan Williams <dcbw@redhat.com> 0.3-2
- Rebuild to test new Extras buildsystem

* Thu Aug 18 2005 David Zeuthen <davidz@redhat.com> 0.3-1
- New upstream release
- Bump some versions for deps

* Fri Jul  1 2005 David Zeuthen <davidz@redhat.com> 0.2-2
- Add missing changelog entry for last commit
- Temporarily BuildReq libpng-devel as it is not pulled in by gtk2-devel
  (should be fixed in Core shortly)
- Pull in latest D-BUS (which features automatic reloading of policy files)
  so users do not have to restart the messagebus after installing this package

* Thu Jun 30 2005 David Zeuthen <davidz@redhat.com> 0.2-1
- New upsteam version
- Add the new gnome-mime-application-x-cisco-vpn-settings.png icon and call
  gtk-update-icon-cache as appropriate

* Fri Jun 17 2005 David Zeuthen <davidz@redhat.com> 0.1-2.cvs20050617
- Add Prereq: /usr/bin/update-desktop-database
- Nuke .la and .a files
- Use find_lang macro to handle locale files properly
- Add Requires for suitable version of shared-mime-info since our desktop
  file depends on the application/x-cisco-vpn-settings MIME-type

* Fri Jun 17 2005 David Zeuthen <davidz@redhat.com> 0.1-1.cvs20050617
- Latest CVS snapshot

* Thu Jun 16 2005 David Zeuthen <davidz@redhat.com> 0.1-1
- Initial build
