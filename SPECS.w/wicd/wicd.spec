%{!?_systemd_unitdir: %global _systemd_unitdir %(pkg-config systemd --variable=systemdsystemunitdir)}

%define debug_package %{nil}

Name:                wicd
Version:             1.7.3
Release:             3%{?dist}
Summary:             Wireless and wired network connection manager
Summary(zh_CN.UTF-8): 无线和有线网络连接管理程序

Group:               System Environment/Base
Group(zh_CN.UTF-8): 系统环境/基本
License:             GPLv2+
URL:                 https://launchpad.net/wicd/
Source0:             https://launchpad.net/wicd/1.7/%{version}/+download/%{name}-%{version}.tar.gz
Source1:             org.wicd.daemon.service

Patch0:              wicd-1.7.3-remove-WHEREAREMYFILES.patch
Patch1:              wicd-1.7.3-dbus-failure.patch
Patch2:              wicd-1.7.2.4-dbus-policy.patch
Patch3:              wicd-1.7.3-DaemonClosing.patch
Patch4:              wicd-1.7.3-unicode.patch
Patch5:              wicd-1.7.3-sanitize.patch

BuildRoot:           %{_tmppath}/%{name}-%{version}-%{release}-root-%(id -u -n)
BuildRequires:       babel
BuildRequires:       python2-devel
BuildRequires:       desktop-file-utils
BuildRequires:       pkgconfig
BuildRequires:       systemd-units
BuildRequires:       gettext

Requires:            %{name}-common = %{version}-%{release}

%description
Wicd is designed to give the user as much control over behavior of network
connections as possible.  Every network, both wired and wireless, has its
own profile with its own configuration options and connection behavior.
Wicd will try to automatically connect only to networks the user specifies
it should try, with a preference first to a wired network, then to wireless.

This package provides the architecture-dependent components of wicd.

%description -l zh_CN.UTF-8
无线和有线网络连接管理程序。

%package common
Summary:             Wicd common files
Summary(zh_CN.UTF-8): %{name} 的公用文件
Group:               System Environment/Base
Group(zh_CN.UTF-8): 系统环境/基本
BuildArch:           noarch
Requires:            dbus
Requires:            dbus-python
Requires:            dhclient
Requires:            ethtool
Requires:            iproute
Requires:            logrotate
Requires:            net-tools
Requires:            wireless-tools
Requires:            wpa_supplicant
Requires:            pygobject2
Requires(post):      systemd-units
Requires(preun):     systemd-units
Requires(postun):    systemd-units

%description common
This package provides the main wicd daemon and the wicd-cli front-end.

%description common -l zh_CN.UTF-8
%{name} 的公用文件。

%package curses
Summary:             Curses client for wicd
Summary(zh_CN.UTF-8): %{name} 的控制台客户端
Group:               Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
BuildArch:           noarch
Requires:            %{name}-common = %{version}-%{release}
Requires:            python-urwid >= 0.9.8.3
Requires:            %{name}-gtk = %{version}-%{release}

%description curses
Client program for wicd that uses a curses interface.

%description curses -l zh_CN.UTF-8
%{name} 的控制台客户端。

%package gtk
Summary:             GTK+ client for wicd
Summary(zh_CN.UTF-8): %{name} 的 GTK+ 客户端
Group:               Applications/Internet
Group(zh_CN.UTF-8): 应用程序/互联网
BuildArch:           noarch
Requires:            %{name}-common = %{version}-%{release}
Requires:            notify-python
Requires:            pygtk2-libglade >= 2.10

%description gtk
Client program for wicd that uses a GTK+ interface.

%description gtk -l zh_CN.UTF-8
%{name} 的 GTK+ 客户端。

%prep
%setup -q

# Remove the WHEREAREMYFILES and resetting of ~/.wicd/WHEREAREMYFILES
# This is pointless.  The documentation can just provide WHEREAREMYFILES,
# which we do in this package.
%patch0 -p1

# Handle D-Bus connection failures a little better
%patch1 -p1

# Allow users at the console to control wicd
%patch2 -p1

# Work around bug in DaemonClosing() calls
%patch3 -p1

# Unicode string handling problems
%patch4 -p1 -b .orig

# Prevent crash when saving network settings
# Upstream bug report and patch:
# https://bugs.launchpad.net/wicd/+bug/993912
%patch5 -p1

%build
rm -f po/ast.po
%{__python} setup.py configure \
    --distro redhat \
    --lib %{_libdir} \
    --share %{_datadir}/wicd \
    --etc %{_sysconfdir}/wicd \
    --bin %{_bindir} \
    --log %{_localstatedir}/log \
    --systemd %{_systemd_unitdir} \
    --no-install-init \
    --no-install-pmutils \
    --no-install-gnome-shell-extensions
%{__python} setup.py build
%{__python} setup.py compile_translations

%install
rm -rf %{buildroot}
%{__python} setup.py install --skip-build --no-compile --root %{buildroot}
sed -i -e '/^#!\//, 1d'  %{buildroot}%{_datadir}/wicd/backends/be-external.py
sed -i -e '/^#!\//, 1d'  %{buildroot}%{_datadir}/wicd/backends/be-ioctl.py
sed -i -e '/^#!\//, 1d'  %{buildroot}%{_datadir}/wicd/cli/wicd-cli.py
sed -i -e '/^#!\//, 1d'  %{buildroot}%{_datadir}/wicd/curses/curses_misc.py
sed -i -e '/^#!\//, 1d'  %{buildroot}%{_datadir}/wicd/curses/netentry_curses.py
sed -i -e '/^#!\//, 1d'  %{buildroot}%{_datadir}/wicd/curses/prefs_curses.py
sed -i -e '/^#!\//, 1d'  %{buildroot}%{_datadir}/wicd/daemon/wicd-daemon.py
sed -i -e '/^#!\//, 1d'  %{buildroot}%{_datadir}/wicd/gtk/gui.py
sed -i -e '/^#!\//, 1d'  %{buildroot}%{_datadir}/wicd/gtk/prefs.py
sed -i -e '/^#!\//, 1d'  %{buildroot}%{_datadir}/wicd/gtk/wicd-client.py

rm -f %{buildroot}%{_localstatedir}/lib/wicd/WHEREAREMYFILES
rm -rf %{buildroot}%{_datadir}/doc
find %{buildroot} -type f -name ".empty_on_purpose" | xargs rm

for lib in %{buildroot}%{python_sitelib}/wicd/*.py ; do
    sed '/\/usr\/bin\/env/d' $lib > $lib.new &&
    touch -r $lib $lib.new &&
    mv $lib.new $lib
done

mkdir -p %{buildroot}%{_datadir}/dbus-1/system-services
install -m 0644 %{SOURCE1} %{buildroot}%{_datadir}/dbus-1/system-services/org.wicd.daemon.service

mv %{buildroot}%{_sysconfdir}/logrotate.d/%{name}.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

desktop-file-install \
    --remove-category="Application" \
    --delete-original \
    --dir=%{buildroot}%{_datadir}/applications \
    %{buildroot}%{_datadir}/applications/wicd.desktop

desktop-file-install \
    --dir=%{buildroot}%{_sysconfdir}/xdg/autostart \
    %{buildroot}%{_sysconfdir}/xdg/autostart/wicd-tray.desktop
magic_rpm_clean.sh
%find_lang %{name} || :

%clean
rm -rf %{buildroot}

%post common
%systemd_post wicd.service

%preun common
%systemd_preun wicd.service

%postun common
%systemd_postun_with_restart wicd.service

%post gtk
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun gtk
if [ $1 -eq 0 ]; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans gtk
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%defattr(-,root,root,-)
%doc AUTHORS CHANGES LICENSE NEWS README other/WHEREAREMYFILES

%files common -f %{name}.lang
%defattr(-,root,root,-)
%dir %{python_sitelib}/wicd
%dir %{_sysconfdir}/wicd
%dir %{_sysconfdir}/wicd/encryption
%dir %{_sysconfdir}/wicd/encryption/templates
%dir %{_sysconfdir}/wicd/scripts
%dir %{_sysconfdir}/wicd/scripts/postconnect
%dir %{_sysconfdir}/wicd/scripts/postdisconnect
%dir %{_sysconfdir}/wicd/scripts/preconnect
%dir %{_sysconfdir}/wicd/scripts/predisconnect
%{_sysconfdir}/acpi/resume.d/80-wicd-connect.sh
%{_sysconfdir}/acpi/suspend.d/50-wicd-suspend.sh
%config(noreplace) %{_sysconfdir}/logrotate.d/wicd
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/wicd.conf
%config(noreplace) %{_sysconfdir}/wicd/dhclient.conf.template.default
%config(noreplace) %{_sysconfdir}/wicd/encryption/templates/active
%config(noreplace) %{_sysconfdir}/wicd/encryption/templates/active_wired
%config(noreplace) %{_sysconfdir}/wicd/encryption/templates/eap
%config(noreplace) %{_sysconfdir}/wicd/encryption/templates/eap-tls
%config(noreplace) %{_sysconfdir}/wicd/encryption/templates/leap
%config(noreplace) %{_sysconfdir}/wicd/encryption/templates/peap
%config(noreplace) %{_sysconfdir}/wicd/encryption/templates/peap-tkip
%config(noreplace) %{_sysconfdir}/wicd/encryption/templates/psu
%config(noreplace) %{_sysconfdir}/wicd/encryption/templates/ttls
%config(noreplace) %{_sysconfdir}/wicd/encryption/templates/wep-hex
%config(noreplace) %{_sysconfdir}/wicd/encryption/templates/wep-passphrase
%config(noreplace) %{_sysconfdir}/wicd/encryption/templates/wep-shared
%config(noreplace) %{_sysconfdir}/wicd/encryption/templates/wired_8021x
%config(noreplace) %{_sysconfdir}/wicd/encryption/templates/wpa
%config(noreplace) %{_sysconfdir}/wicd/encryption/templates/wpa-psk
%config(noreplace) %{_sysconfdir}/wicd/encryption/templates/wpa-psk-hex
%config(noreplace) %{_sysconfdir}/wicd/encryption/templates/wpa-peap
%config(noreplace) %{_sysconfdir}/wicd/encryption/templates/wpa2-leap
%config(noreplace) %{_sysconfdir}/wicd/encryption/templates/wpa2-peap
%{_systemd_unitdir}/wicd.service
%{python_sitelib}/wicd/*
%{python_sitelib}/wicd-%{version}*.egg-info
%{_bindir}/wicd-cli
%{_bindir}/wicd-client
%{_sbindir}/wicd
%{_datadir}/applications/wicd.desktop
%{_datadir}/dbus-1/system-services/org.wicd.daemon.service
%{_datadir}/man/man1/wicd-client.1*
%{_datadir}/man/man5/wicd-manager-settings.conf.5*
%{_datadir}/man/man5/wicd-wired-settings.conf.5*
%{_datadir}/man/man5/wicd-wireless-settings.conf.5*
%{_datadir}/man/man8/wicd-cli.8*
%{_datadir}/man/man8/wicd.8*
%dir %{_datadir}/wicd
%dir %{_datadir}/wicd/backends
%dir %{_datadir}/wicd/cli
%dir %{_datadir}/wicd/daemon
%{_datadir}/wicd/backends/*
%{_datadir}/wicd/cli/*
%{_datadir}/wicd/daemon/*
%dir %{_localstatedir}/lib/wicd
%dir %{_localstatedir}/lib/wicd/configurations

%files curses
%defattr(-,root,root,-)
%dir %{_datadir}/wicd/curses
%{_datadir}/wicd/curses/*
%{_bindir}/wicd-curses
%{_datadir}/man/man8/wicd-curses.8*

%files gtk
%defattr(-,root,root,-)
%dir %{_datadir}/wicd/gtk
%{_sysconfdir}/xdg/autostart/wicd-tray.desktop
%{_datadir}/pixmaps/wicd-gtk.xpm
%{_datadir}/wicd/gtk/*
%{_bindir}/wicd-gtk
%{_datadir}/icons/hicolor/*/apps/wicd-gtk.png
%{_datadir}/icons/hicolor/scalable/apps/wicd-gtk.svg
%dir %{_datadir}/wicd/icons
%{_datadir}/wicd/icons/*
%{_datadir}/autostart/wicd-tray.desktop

%changelog
* Tue Oct 20 2015 Liu Di <liudidi@gmail.com> - 1.7.3-3
- 为 Magic 3.0 重建

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Apr 09 2015 David Cantrell <dcantrell@redhat.com> - 1.7.3-1
- Upgrade to wicd-1.7.3 (#1176990)

* Thu Apr 09 2015 David Cantrell <dcantrell@redhat.com> - 1.7.2.4-16
- Remove dependency on pm-utils (#1208313)

* Tue Nov 25 2014 David Cantrell <dcantrell@redhat.com> - 1.7.2.4-15
- self.prog_name -> self.prof_name in netentry_curses.py (#1162118)

* Mon Sep 29 2014 David Cantrell <dcantrell@redhat.com> - 1.7.2.4-14
- Remove check for daemon patch (#1074315)

* Thu Sep 25 2014 David Cantrell <dcantrell@redhat.com> - 1.7.2.4-13
- Fix string.translate() usage in misc.py (#1005515)

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.2.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jul 02 2014 David Cantrell <dcantrell@redhat.com> - 1.7.2.4-11
- Prevent crash when saving network settings (#996693)

* Mon Jun 30 2014 David Cantrell <dcantrell@redhat.com> - 1.7.2.4-10
- Do not assume wicd-daemon is running when wicd-client runs (#1074315)
- Fix wicd-curses crash on startup (#894646)
- Edit default D-Bus policy file to allow 'users' group members to run
  wicd client programs (#1074372)

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.2.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Dec 09 2013 David Cantrell <dcantrell@redhat.com> - 1.7.2.4-8
- Apply upstream patch to fix exception when changing properties in
  wicd-gtk (#981667)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.2.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Apr 01 2013 David Cantrell <dcantrell@redhat.com> - 1.7.2.4-6
- systemd_post_with_restart -> systemd_postun_with_restart (#901753)

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.2.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 23 2012 David Cantrell <dcantrell@redhat.com> - 1.7.2.4-4
- Fix some Unicode string handling and display problems (#845749)

* Tue Oct 23 2012 David Cantrell <dcantrell@redhat.com> - 1.7.2.4-3
- Use new systemd macros in trigger scripts (#850367)

* Thu Aug 02 2012 David Cantrell <dcantrell@redhat.com> - 1.7.2.4-2
- Updated duplicate logrotate file fix (#820139)

* Thu Aug 02 2012 David Cantrell <dcantrell@redhat.com> - 1.7.2.4-1
- Upgrade to wicd-1.7.2.4
- Remove duplicate logrotate file (#820139)
- The curses package requires some code from the gtk module, so add explicit
  dependency (#831309)

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Apr 13 2012 David Cantrell <dcantrell@redhat.com> - 1.7.2.1-1
- Upgrade to wicd-1.7.2.1 to fix CVE-2012-2095 (#811763)

* Mon Mar 26 2012 David Cantrell <dcantrell@redhat.com> - 1.7.1-5
- Remove our wicd.service file, this is provided by upstream now

* Mon Mar 26 2012 David Cantrell <dcantrell@redhat.com> - 1.7.1-4
- Make sure systemd unit files go to /usr/lib/systemd
- Stop mangling logfile.py so bytecompiling will actually work
- 91wicd -> 55wicd
- Pick up new encryption template files in the %%files list

* Thu Mar 22 2012 David Cantrell <dcantrell@redhat.com> - 1.7.1-3
- BR babel
- Remove po/ast.po because babel doesn't understand it

* Thu Mar 22 2012 David Cantrell <dcantrell@redhat.com> - 1.7.1-2
- Ensure wpath.etc is set to /etc/wicd, not /etc/dhcp (#754412)
- Initialize child_pid to None in wicd-daemon.py (#798692)
- Make wicd-gtk subpackage require notify-python (#748258)
- Work around no-op problem in DaemonClosing calls (#740317)

* Fri Feb 10 2012 David Cantrell <dcantrell@redhat.com> - 1.7.1-1
- Upgrade to wicd-1.7.1 final release (#789380)
- Have wicd-common require pygobject2 (#754416)
- Remove patches that have been incorporated upstream

* Fri Jan 27 2012 David Cantrell <dcantrell@redhat.com> - 1.7.1b2-0.3
- Fix CVE-2012-0813 (#785147)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.1-0.2.b2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Aug 19 2011 David Cantrell <dcantrell@redhat.com> - 1.7.1b2-0.1
- Upgrade to wicd-1.7.1b2

* Fri Aug 19 2011 David Cantrell <dcantrell@redhat.com> - 1.7.0-9
- Initialize appGui._wired_showing in __init__ (#723553)
- Make sure check and message in wicd-cli are a lambda (#712435)
- Correct systemd unit file for wicd, add D-Bus service file (#699116)
- Move docs to the wicd-common subpackage
- Correct /etc/dbus-1/system.d/wicd.conf (#699116)

* Mon May 09 2011 Bill Nottingham <notting@redhat.com> - 1.7.0-8
- fix systemd scriptlets for upgrade

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 15 2011 David Cantrell <dcantrell@redhat.com> - 1.7.0-6
- Correct typo with _systemd_unitdir macro usage in spec file

* Sat Jan 15 2011 David Cantrell <dcantrell@redhat.com> - 1.7.0-5
- Replace existing init script with systemd unit file (#661226)

* Fri Oct 22 2010 David Cantrell <dcantrell@redhat.com> - 1.7.0-4
- Use cPickle instead of deepcopy in configmanager.py (#645251)

* Wed Aug 25 2010 David Cantrell <dcantrell@redhat.com> - 1.7.0-3
- Remove hard dependency on the base package by wicd-common.  The
  base package is arch-specific and contains optional components
  for wicd.  If it is present, wicd will make use of it, but it is
  not required for normal functionality.

* Fri Jul 30 2010 Thomas Spura <tomspur@fedoraproject.org> - 1.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon Jun 21 2010 David Cantrell <dcantrell@redhat.com> - 1.7.0-1
- Initial package
