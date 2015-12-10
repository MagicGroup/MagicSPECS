# Turn off the brp-python-bytecompile script
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')

# Enable hardened build, as the udev part runs with privilege.
%define _hardened_build 1

Summary: A printer administration tool
Summary(zh_CN.UTF-8): 打印机管理工具
Name: system-config-printer
Version: 1.5.7
Release: 8%{?dist}
License: GPLv2+
URL: http://cyberelk.net/tim/software/system-config-printer/
Group: System Environment/Base
Group(zh_CN.UTF-8): 系统环境/基本
Source0: http://cyberelk.net/tim/data/system-config-printer/1.5/%{name}-%{version}.tar.xz
Patch1: system-config-printer-shbang.patch
Patch2: system-config-printer-device-sorting.patch

BuildRequires: cups-devel >= 1.2
BuildRequires: desktop-file-utils >= 0.2.92
BuildRequires: gettext-devel
BuildRequires: intltool
BuildRequires: libusb1-devel
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: xmlto
BuildRequires: systemd-units, systemd-devel
BuildRequires: python3-devel

Requires: python3-gobject%{?_isa}
Requires: gtk3%{?_isa}
Requires: desktop-file-utils >= 0.2.92
Requires: dbus-x11
Requires: python3-dbus%{?_isa}
Requires: system-config-printer-libs = %{version}-%{release}
Requires: desktop-notification-daemon
Requires: libnotify%{?_isa}
Requires: libgnome-keyring%{?_isa}
Requires: python3-cairo%{?_isa}
Requires: python3-firewall
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

%description
system-config-printer is a graphical user interface that allows
the user to configure a CUPS print server.

%description -l zh_CN.UTF-8
打印机管理工具。

%package libs
Summary: Libraries and shared code for printer administration tool
Summary(zh_CN.UTF-8): %{name} 的运行库
Group: System Environment/Base
Group(zh_CN.UTF-8): 系统环境/基本
Requires: python3-cups >= 1.9.60
Requires: python3-pycurl
Requires: gobject-introspection
Requires: python3-gobject
Requires: gtk3
Requires: python3-dbus
Requires: python3-requests
Suggests: python-smbc
BuildArch: noarch
Obsoletes: %{name}-libs < 1.3.12-10

%description libs
The common code used by both the graphical and non-graphical parts of
the configuration tool.

%description libs -l zh_CN.UTF-8
%{name} 的运行库。

%package applet
Summary: Print job notification applet
Summary(zh_CN.UTF-8): 打印任务通知小程序
Group: System Environment/Base
Group(zh_CN.UTF-8): 系统环境/基本
Requires: %{name}-libs

%description applet
Print job notification applet.

%description applet -l zh_CN.UTF-8
打印任务通知小程序。

%package udev
Summary: Rules for udev for automatic configuration of USB printers
Summary(zh_CN.UTF-8): 自动配置 USB 打印机的 udev 规则
Group: System Environment/Base
Group(zh_CN.UTF-8): 系统环境/基本
Requires: system-config-printer-libs = %{version}-%{release}
Obsoletes: hal-cups-utils < 0.6.20
Provides: hal-cups-utils = 0.6.20

%description udev
The udev rules and helper programs for automatically configuring USB
printers.

%description udev -l zh_CN.UTF-8
自动配置 USB 打印机的 udev 规则。

%prep
%setup -q

# Fixed shbang line in udev-add-printer (trac #244).
%patch1 -p1 -b .shbang

# Fixed device sorting (bug #1210733).
%patch2 -p1 -b .device-sorting

%build
%configure --with-udev-rules
make %{?_smp_mflags}

%install
make DESTDIR=%buildroot install

%{__mkdir_p} %buildroot%{_localstatedir}/run/udev-configure-printer
touch %buildroot%{_localstatedir}/run/udev-configure-printer/usb-uris

# Manually invoke the python byte compile macro for each path that
# needs byte compilation
%py_byte_compile %{__python3} %%{buildroot}%{python3_sitelib}/cupshelpers
%py_byte_compile %{__python3} %%{buildroot}%{datadir}/system-config-printer
magic_rpm_clean.sh
%find_lang system-config-printer

%files libs -f system-config-printer.lang
%doc COPYING
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/com.redhat.NewPrinterNotification.conf
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/com.redhat.PrinterDriversInstaller.conf
%{_datadir}/dbus-1/interfaces/*.xml
%{_datadir}/dbus-1/services/*.service
%{_bindir}/scp-dbus-service
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/asyncconn.py*
%{_datadir}/%{name}/asyncipp.py*
%{_datadir}/%{name}/asyncpk1.py*
%{_datadir}/%{name}/authconn.py*
%{_datadir}/%{name}/config.py*
%{_datadir}/%{name}/cupspk.py*
%{_datadir}/%{name}/debug.py*
%{_datadir}/%{name}/dnssdresolve.py*
%{_datadir}/%{name}/errordialogs.py*
%{_datadir}/%{name}/firewallsettings.py*
%{_datadir}/%{name}/gtkinklevel.py*
%{_datadir}/%{name}/gui.py*
%{_datadir}/%{name}/installpackage.py*
%{_datadir}/%{name}/jobviewer.py*
%{_datadir}/%{name}/killtimer.py*
%{_datadir}/%{name}/monitor.py*
%{_datadir}/%{name}/newprinter.py*
%{_datadir}/%{name}/options.py*
%{_datadir}/%{name}/optionwidgets.py*
%{_datadir}/%{name}/OpenPrintingRequest.py*
%{_datadir}/%{name}/PhysicalDevice.py*
%{_datadir}/%{name}/ppdcache.py*
%{_datadir}/%{name}/ppdippstr.py*
%{_datadir}/%{name}/ppdsloader.py*
%{_datadir}/%{name}/printerproperties.py*
%{_datadir}/%{name}/probe_printer.py*
%{_datadir}/%{name}/pysmb.py*
%{_datadir}/%{name}/scp-dbus-service.py*
%{_datadir}/%{name}/smburi.py*
%{_datadir}/%{name}/statereason.py*
%{_datadir}/%{name}/timedops.py*
%dir %{_sysconfdir}/cupshelpers
%config(noreplace) %{_sysconfdir}/cupshelpers/preferreddrivers.xml
%{python3_sitelib}/cupshelpers
%{python3_sitelib}/*.egg-info

%files applet
%{_bindir}/%{name}-applet
%{_datadir}/%{name}/applet.py*
%{_sysconfdir}/xdg/autostart/print-applet.desktop
%{_mandir}/man1/%{name}-applet.1*

%files udev
%{_prefix}/lib/udev/rules.d/*.rules
%{_prefix}/lib/udev/udev-*-printer
%ghost %dir %{_localstatedir}/run/udev-configure-printer
%ghost %verify(not md5 size mtime) %config(noreplace,missingok) %attr(0644,root,root) %{_localstatedir}/run/udev-configure-printer/usb-uris
%{_unitdir}/configure-printer@.service

%files
%doc ChangeLog README
%{_bindir}/%{name}
%{_bindir}/install-printerdriver
%{_datadir}/%{name}/check-device-ids.py*
%{_datadir}/%{name}/HIG.py*
%{_datadir}/%{name}/SearchCriterion.py*
%{_datadir}/%{name}/serversettings.py*
%{_datadir}/%{name}/system-config-printer.py*
%{_datadir}/%{name}/ToolbarSearchEntry.py*
%{_datadir}/%{name}/userdefault.py*
%{_datadir}/%{name}/troubleshoot
%{_datadir}/%{name}/icons
%{_datadir}/%{name}/install-printerdriver.py*
%dir %{_datadir}/%{name}/xml
%{_datadir}/%{name}/xml/*.rng
%{_datadir}/%{name}/xml/validate.py*
%dir %{_datadir}/%{name}/ui
%{_datadir}/%{name}/ui/*.ui
%{_datadir}/applications/system-config-printer.desktop
%{_datadir}/appdata/*.appdata.xml
%{_mandir}/man1/%{name}.1*

%post
/bin/rm -f /var/cache/foomatic/foomatic.pickle
exit 0

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 1.5.7-8
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 1.5.7-7
- 为 Magic 3.0 重建

* Tue Sep 29 2015 Liu Di <liudidi@gmail.com> - 1.5.7-6
- 为 Magic 3.0 重建

* Tue Jul 21 2015 Jiri Popelka <jpopelka@redhat.com> - 1.5.7-5
- libs subpackage Suggests: python-smbc

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 26 2015 Tim Waugh <twaugh@redhat.com> - 1.5.7-3
- Fixed device sorting (bug #1210733).

* Tue May 26 2015 Tim Waugh <twaugh@redhat.com> - 1.5.7-2
- Fixed shbang line in udev-add-printer (trac #244).

* Wed Apr 29 2015 Tim Waugh <twaugh@redhat.com> - 1.5.7-1
- 1.5.7:
  - Increase bus settle time for usb_modeswitch devices (bug #1206808).
  - Set use_underline=True for previously-stock buttons (bug #1210859).
  - Fixed traceback (bug #1213136).
  - Fixes for appdata file.

* Tue Mar 17 2015 Tim Waugh <twaugh@redhat.com> - 1.5.6-1
- 1.5.6:
  - Don't show traceback messages for missing probe helpers (bug #1194101).
  - Don't try writing bytecache when running udev-add-printer
    (bug #1196183).
  - Don't try decoding already-decoded Unicode (bug #1195974).
  - Fixes for CMD matching (bug #1177978, bug #1171874).
  - Fixed 'Apply' sensitivity when downloading driver (trac #238).
  - Avoid deprecated things.
  - Handle missing 'functionality' field in returned data for driver.
  - Some fixes for the New Printer dialog.
  - Don't install an OpenPrinting driver if the license is not
    accepted (trac #240).

* Sat Feb  7 2015 Tim Waugh <twaugh@redhat.com> - 1.5.5-2
- Requires python3-firewall.

* Fri Feb  6 2015 Tim Waugh <twaugh@redhat.com> - 1.5.5-1
- 1.5.5:
  - No longer requires gnome-icon-theme (bug #1163928).
  - Fixed race condition when fetching devices (bug #1176443).
  - Fixed typo preventing retrieve/reprint from working.
  - Driver installation fixes.
  - Various other fixes.

* Tue Nov  4 2014 Tim Waugh <twaugh@redhat.com> - 1.5.4-1
- 1.5.4:
  - Extract hostname from hp:/net/...?hostname= URIs when grouping by
    physical device (bug #1154686).
  - Tell user how to retrieve journal entries as root in
    troubleshooter (bug #1157253).
  - Codec fix for AuthDialog.get_auth_info (bug #1060453).
  - Catch IPPError when writing server settings (bug #1159584).
  - Several other fixes.

* Fri Oct 17 2014 Tim Waugh <twaugh@redhat.com> - 1.5.3-1
- 1.5.3.

* Fri Oct 10 2014 Tim Waugh <twaugh@redhat.com> - 1.5.2-2
- Use items() instead of iteritems() with Python 3 dicts (bug #1151457).

* Fri Oct 10 2014 Tim Waugh <twaugh@redhat.com> - 1.5.2-1
- 1.5.2.

* Thu Sep 11 2014 Tim Waugh <twaugh@redhat.com> - 1.5.1-3
- Python3 fixes from upstream.

* Sat Sep  6 2014 Tim Waugh <twaugh@redhat.com> - 1.5.1-2
- Take the gdk lock before entering gtk_main() (bug #1052203 comment #24).

* Tue Sep  2 2014 Tim Waugh <twaugh@redhat.com> - 1.5.1-1
- 1.5.1, with some Python3 fixes (bug #1136470),
  udev-configure-printer fixes, and a fix for a D-Bus service
  hang (bug #1116756).

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Aug 15 2014 Tim Waugh <twaugh@redhat.com> 1.5.0-7
- Enable hardened build, as the udev part runs with privilege.

* Sun Aug  3 2014 Tim Waugh <twaugh@redhat.com> 1.5.0-6
- Explicitly use /usr/bin/python3 in udev-add-printer (bug #1126149).

* Fri Jul 25 2014 Tim Waugh <twaugh@redhat.com> 1.5.0-5
- More python3 dependency changes:
  - pygobject3-base -> python3-gobject
  - pycairo -> python3-cairo

* Thu Jul 24 2014 Tim Waugh <twaugh@redhat.com> 1.5.0-4
- The applet is now in its own sub-package.

* Sun Jul 20 2014 Tim Waugh <twaugh@redhat.com> 1.5.0-3
- Also require python3 bindings for pycurl (bug #1121177).

* Sat Jul 19 2014 Tim Waugh <twaugh@redhat.com> 1.5.0-2
- Require python3 bindings for cups and dbus (bug #1121177).

* Thu Jul 17 2014 Tim Waugh <twaugh@redhat.com> 1.5.0-1
- 1.5.0 (now Python3).

* Mon Jul 14 2014 Tim Waugh <twaugh@redhat.com> 1.4.5-3
- Fix job retrieval (bug #1119222).

* Fri Jul 11 2014 Tim Waugh <twaugh@redhat.com> 1.4.5-2
- Handle failure when cups-pk-helper not installed (bug #1118836).

* Fri Jul  4 2014 Tim Waugh <twaugh@redhat.com> 1.4.5-1
- 1.4.5:
  - Some codec fixes (bug #968142, bug #1023968, bug #1094037).
  - Traceback fixes (bug #982071, bug #1090479, bug #1105229).
  - IPv6 address entry fix (bug #1074245).
  - Auth info saving improvement (bug #1089029).
  - Use LockButton for fewer auth dialogs (bug #714820).

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 22 2014 Jiri Popelka <jpopelka@redhat.com> - 1.4.4-3
- 1.4.x requires gtk3 instead of gtk2 (#1099611)

* Thu May  1 2014 Tim Waugh <twaugh@redhat.com> 1.4.4-2
- Prevent the D-Bus service from freezing by disabling openprinting
  driver downloads in that service (bug #1052203).

* Wed Mar 12 2014 Jaromír Končický <jkoncick@redhat.com> - 1.4.4-1
- 1.4.4.

* Mon Mar 10 2014 Jiri Popelka <jpopelka@redhat.com> - 1.4.3-9
- BuildRequires: pkgconfig(glib-2.0) instead of glib2-devel

* Fri Feb 28 2014 Tim Waugh <twaugh@redhat.com> 1.4.3-8
- Don't override CFLAGS in Makefile.am.

* Fri Dec  6 2013 Tim Waugh <twaugh@redhat.com> 1.4.3-7
- Include upstream Makefile fixes for udev directories.

* Fri Dec  6 2013 Tim Waugh <twaugh@redhat.com> 1.4.3-6
- Use _smp_mflags for consistency's sake (patch from upstream needed).

* Thu Dec  5 2013 Tim Waugh <twaugh@redhat.com> 1.4.3-5
- Actually run make in the %%build section.

* Fri Nov  8 2013 Tim Waugh <twaugh@redhat.com> 1.4.3-4
- Requires pycairo (bug #1028180).
- Reverted last change as it did not fix the problem.

* Wed Oct 30 2013 Tim Waugh <twaugh@redhat.com> 1.4.3-3
- Fixed encoding issue (bug #1023968).

* Fri Oct 25 2013 Tim Waugh <twaugh@redhat.com> 1.4.3-2
- Fixed typo in D-Bus signature decorator (bug #1023449).

* Tue Oct 22 2013 Tim Waugh <twaugh@redhat.com> 1.4.3-1
- 1.4.3.

* Tue Aug 20 2013 Tim Waugh <twaugh@redhat.com> 1.4.2-1
- 1.4.2.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul  4 2013 Tim Waugh <twaugh@redhat.com> 1.4.1-9
- Fixed source URL.

* Tue Jul  2 2013 Tim Waugh <twaugh@redhat.com> 1.4.1-8
- Fixed misplaced parenthesis (bug #979119).
- Fixed another codec issue (bug #978970).
- Avoid race when renaming printer (bug #975705).
- Don't check for missing drivers in remote printers (bug #975058)
- Another fix from the move to gi.repository (bug #973662).
- Fixed another codec issue (bug #971973).

* Thu Jun 20 2013 Jiri Popelka <jpopelka@redhat.com> - 1.4.1-7
- Fix Notify.Notification creation (bug #974845).
- Really apply patch for bug #971404.

* Fri Jun  7 2013 Tim Waugh <twaugh@redhat.com> 1.4.1-6
- Use the right signal for spotting when editing is done when renaming
  a printer (bug #971404).
- More fixes for UTF-8 encoding issues (bug #968142).
- Fixed new printer dialog traceback (bug #969916).

* Fri Jun  7 2013 Tim Waugh <twaugh@redhat.com> 1.4.1-5
- More fixes for UTF-8 encoding issues (bug #971548).

* Thu Jun  6 2013 Tim Waugh <twaugh@redhat.com> 1.4.1-4
- Removed old pointer/keyboard grabbing code as it no longer
  works (bug #971459).
- Notify urgencies have new names with gi.repository (bug #970646).
- More fixes for UTF-8 encoding issues (bug #969846, bug #971417).

* Wed May 22 2013 Tim Waugh <twaugh@redhat.com> 1.4.1-3
- Fixed typo introduced in previous change (for bug #962207), and
  fixed another UTF-8 encoding issue (bug #965771).

* Tue May 21 2013 Tim Waugh <twaugh@redhat.com> 1.4.1-2
- Fixed typo which could cause a traceback (bug #965678).
- Fixes for UTF-8 encoding issues (bug #957444, bug #961882,
  bug #962207, bug #964673, bug #965578).

* Thu May  9 2013 Tim Waugh <twaugh@redhat.com> 1.4.1-1
- 1.4.1:
  - Don't call into Gtk directly from scp-dbus-service (bug #951710).
  - Handle errors from Gdk.color_parse() correctly.
  - Fix creating of empty pixbuf.
  - Make man page and --help output consistent.
  - Some codec fixes (bug #957343, bug #957444, bug #960567).
  - Updated translations (bug #951647).
  - Use xxx-supported values for number-up and sides options
    (bug #923841).

* Mon Apr 15 2013 Tim Waugh <twaugh@redhat.com> 1.4.0-4
- Don't call into Gtk directly from scp-dbus-service (bug #951710).
- Adjusted dependencies now we use GObject introspection.

* Fri Apr 12 2013 Tim Waugh <twaugh@redhat.com> 1.4.0-3
- Don't delete mainlist too early when quitting (bug #915483).

* Thu Apr 11 2013 Tim Waugh <twaugh@redhat.com> 1.4.0-2
- Fixed changelog date.
- Fixed some printer name encoding issues (bug #950162).
- Better behaviour when trying to run without valid DISPLAY (bug # #948240).

* Wed Mar 27 2013 Tim Waugh <twaugh@redhat.com> 1.4.0-1
- 1.4.0.

* Wed Mar 27 2013 Tim Waugh <twaugh@redhat.com> 1.3.13-1
- 1.3.13.

* Tue Mar 19 2013 Tim Waugh <twaugh@redhat.com> 1.3.12-11
- The libs sub-package is now noarch (bug #921514).

* Fri Mar 15 2013 Tim Waugh <twaugh@redhat.com> 1.3.12-10
- Removed python-smbc as a dependency as it is not required in all
  situations (bug #921132).

* Wed Feb 27 2013 Tim Waugh <twaugh@redhat.com> 1.3.12-9
- Disable the print applet in KDE again.

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.12-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 26 2012 Tim Waugh <twaugh@redhat.com> 1.3.12-7
- Enable the print applet in KDE (only on Red Hat Enterprise Linux).

* Wed Nov 21 2012 Tim Waugh <twaugh@redhat.com> 1.3.12-6
- Avoid traceback in most recent change (bug #878527).

* Mon Nov 19 2012 Tim Waugh <twaugh@redhat.com> 1.3.12-4
- Fixed dialog modality problem which prevented e.g. changing drivers.

* Thu Oct 25 2012 Tim Waugh <twaugh@redhat.com> 1.3.12-3
- Avoid crash with certain types of dnssd device URI (bug #870000).

* Tue Oct 23 2012 Tim Waugh <twaugh@redhat.com> 1.3.12-2
- Fixed systemd config file (bug #862186).

* Fri Oct  5 2012 Tim Waugh <twaugh@redhat.com> 1.3.12-1
- 1.3.12.

* Fri Sep 21 2012 Jiri Popelka <jpopelka@redhat.com> 1.3.11-5
- FirewallD support once again (use D-Bus instead of FirewallD client module)

* Tue Sep 18 2012 Jiri Popelka <jpopelka@redhat.com> 1.3.11-4
- revert previous change for now, the patch needs more work

* Thu Sep 06 2012 Jiri Popelka <jpopelka@redhat.com> 1.3.11-3
- FirewallD support

* Wed Aug 22 2012 Jiri Popelka <jpopelka@redhat.com> 1.3.11-2
- use new systemd-rpm macros (#850334)

* Fri Aug  3 2012 Tim Waugh <twaugh@redhat.com> 1.3.11-1
- 1.3.11.

* Wed Aug  1 2012 Tim Waugh <twaugh@redhat.com> 1.3.10-1
- 1.3.10.
- Build requirement for libusb has changed to libusb1-devel.

* Tue Jul 31 2012 Tim Waugh <twaugh@redhat.com> 1.3.9-5
- Reverted previous change. New systemd-devel does provide libudev.pc
  after all.

* Tue Jul 31 2012 Tim Waugh <twaugh@redhat.com> 1.3.9-4
- Fixed build against systemd-devel now there is no libudev-devel.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 05 2012 Jiri Popelka <jpopelka@redhat.com> 1.3.9-2
- BuildRequires systemd-devel instead of udev-devel
- replace udev_get_sys_path() with hard-coded "/sys"

* Thu Mar  1 2012 Tim Waugh <twaugh@redhat.com> 1.3.9-1
- 1.3.9:
  - Updated translations.
  - Improved check-device-ids output.
  - Removed incorrect warning when using CUPS >= 1.5.3.

* Thu Feb 23 2012 Tim Waugh <twaugh@redhat.com> 1.3.8-4
- Added version to python-cups dependency (bug #796678).

* Fri Feb  3 2012 Tim Waugh <twaugh@redhat.com> 1.3.8-3
- Upstream patch to fix ppdcache traceback (bug #786232).

* Mon Jan 30 2012 Jiri Popelka <jpopelka@redhat.com> 1.3.8-2
- Fixed several debugprints (#785581).
- Clean up and modernize spec file.

* Tue Jan 24 2012 Tim Waugh <twaugh@redhat.com> 1.3.8-1
- 1.3.8:
  - Avoid AttributeError in on_btnNPApply_clicked() (bug #772112).
  - Added debugging when jobviewer not found (bug #757520).
  - Applied patch from Till Kamppeter to use pycurl 'https' support
    for openprinting (CVE-2011-4405).
  - Always use a sequence as args for timedops.TimedSubprocess()
    (patch from Vincent Untz).
  - Added some firewall debugging for bug #755913.
  - Fixed typo (Ubuntu #844976).
  - Run probe_printer.py with an argument to run PrinterFinder by hand.
  - More debugging output in PrinterFinder.
  - Really fix SMB probing in PrinterFinder.
  - LpdServer class: spot when we can't connect, and give up (likewise
    in PrinterFinder).
  - Ignore ' All-in-one' suffix for printer model names when comparing
    them (bug #751610).
  - Handle HTTP errors from openprinting.org (seen in bug #743446).
  - Don't re-open PPD when already available, just to localize marker
    names.
  - Use the monitor's PPD cache in the properties dialog.
  - monitor: provide method for sharing the monitor's PPD cache.
  - cupshelpers: avoid re-opening PPD when not needed (not a leak).
  - Fixed file descriptor leak in PPDCache (Ubuntu #874445).
  - Fixed typo in check-device-ids.py when looking for ID-less
    matches.
  - Require newer pycups; drop compatibility code.
  - Do not connect to CUPS with an empty user name.
  - On asynchronous IPP connections make sure that the password dialog
    is repeated if a wrong password is entered (Ubuntu #653132).
  - Several fixes on credential caching for IPP authentication (Ubuntu
    bug 653132).
  - Don't penalise pxlmono now that bug #661814 is fixed in
    ghostscript-9.04.
  - Handle new CUPS 1.5 IPP error response IPP_AUTHENTICATION_CANCELED
    (Ubuntu #653132).

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov  4 2011 Tim Waugh <twaugh@redhat.com> 1.3.7-3
- Use arch-specific requirements where appropriate (bug #749834).

* Mon Oct 17 2011 Tim Waugh <twaugh@redhat.com> 1.3.7-2
- Fixed typo in check-device-ids.py when looking for ID-less matches.
- Handle new CUPS 1.5 IPP error response IPP_AUTHENTICATION_CANCELED
  (Ubuntu #653132).

* Wed Oct  5 2011 Tim Waugh <twaugh@redhat.com> 1.3.7-1
- 1.3.7:
  - Show private job attributes for "my jobs" (bug #742279).
  - Enable Test Page button when application/postscript is supported.
  - Some preferreddrivers.xml fixes (Ubuntu #855412).
  - Handle errors saving troubleshoot.txt (Ubuntu #789602).
  - Removed some stale code.
  - Make connections list more easily accessible (Ubuntu #842092).
  - Improved handling of remote CUPS queues via DNS-SD, and IPP devices.
  - Better display of CUPS servers from "Find Network Printer".
  - Fixed SMB method for printer finder.
  - Don't handle tooltips during mainloop recursion (bug #664044,
    bug #739734).
  - Fixed bold print of tab labels on option conflicts.
  - Preserve installable options on driver change.
  - Update printer properties dialog correctly when PPD changed.
  - Fixed typo triggered by private job attributes (Ubuntu #827573).
  - Marked some translatable strings that weren't (bug #734313).

* Mon Aug 22 2011 Tim Waugh <twaugh@redhat.com> 1.3.6-1
- 1.3.6:
  - Updated translations.
  - IPPAuthConnection: avoid traceback (Ubuntu #828030).
  - Allow entering @,?,=,& characters in Device URI text field
    (Ubuntu #826958).
  - Removed PackageKit client code in missingPackagesAndExecutables
    (bug #726938).
  - Properties dialog: make OK button sensitive even when no changes
    to save (Ubuntu #444280).

* Mon Aug 15 2011 Tim Waugh <twaugh@redhat.com> 1.3.5-4
- Removed redundant macros, spotted by Jiri Popelka.

* Tue Aug  2 2011 Tim Waugh <twaugh@redhat.com> 1.3.5-3
- Removed problematic PackageKit client support (bug #726996, bug #726938).

* Mon Aug  1 2011 Tim Waugh <twaugh@redhat.com> 1.3.5-2
- Make PackageKit optional (bug #726996).

* Fri Jul 29 2011 Tim Waugh <twaugh@redhat.com> 1.3.5-1
- 1.3.5:
  - Driver selection, missing executables checking, and physical
    device grouping now exposed via D-Bus.
  - Fixed cupsFilter search in missing executables check.
  - Use PackageKit to resolve missing executable filenames to
    packages.
  - Fixed DNSSD hostname resolution.
  - Fixed firewall code to handle json errors when used with the older
    system-config-firewall D-Bus service.
  - Fixed LPD probing (726383).
  - Use "hostname" instead of "IP address" when asking for names of
    browse servers (bug #726134).
  - Updated translations.
- Also: applied patch to fix serversettings traceback, from upstream
  post-1.3.5 (bug #726682).
- Move files around so the libs sub-package provides the D-Bus service.

* Thu Jul 21 2011 Tim Waugh <twaugh@redhat.com> 1.3.4-2
- No longer requires glade (uses GtkBuilder instead).

* Fri Jul 15 2011 Tim Waugh <twaugh@redhat.com> 1.3.4-1
- 1.3.4:
  - Don't rely on retriggering printers; enumerate them from systemd
    instead.
  - Don't complain about missing/invalid device ID for devices we've
    already handled.
  - Removed unused Printer Groups feature.
  - Don't show "No printers configured" page if the printers are
    filtered in any way.
  - URL-quote URIs when using "Find Network Printer" (Ubuntu #808137).
  - Downloadable drivers: don't display printers for which there are
    no drivers (bug #668154).
  - Kerberos support for the SMB 'Verify' button (requires new enough
    pycups).
  - Removed IPP/HTTP device screen in favour of "Enter URI"
    (bug #685091).
  - Converted ComboBoxEntry widgets to Entry+EntryCompletion in
    NewPrinterWindow.ui.
  - Robustness in ppdsloader in the face of errors (Ubuntu #766818).
  - Changed Make/Model/State labels into GtkEntry widgets so contents
    are always fully selectable (bug #719217).
  - Convert iters to paths before comparing (bug #717062, Ubuntu #791690,
    trac #221).
  - Set translation domain in D-Bus service (Ubuntu #783967).
  - Ensure consistency in jobviewer if add_job fails (bug #693055,
    bug #632551).
  - Avoid PostScript for HP LaserJet 2100 Series (bug #710231).
  - Raised priority for SpliX driver (Ubuntu bug #793741).
  - Updated Free Software Foundation (FSF) address.
  - Adjusted test code in asyncpk1.py so it doesn't look like a
    tempfile vulnerability.

* Fri Jun 03 2011 Jiri Popelka <jpopelka@redhat.com> 1.3.3-1
- 1.3.3:
  - Set translation domain for ServerSettingsDialog (Ubuntu #777188).
  - scp-dbus-service: Ignore setlocale() errors (Ubuntu #748964).
  - Renamed ui/*.glade to ui/*.ui again (Ubuntu #759811).
  - Allow % character in SMB URI (Ubuntu #747400).
  - More error handling (Ubuntu #744783).
  - Avoid traceback if printer duplication fails (bug #694629).
  - Fixed off-by-one error in monitor.
  - Fixed printer renaming (Ubuntu #726954).
  - Added PrinterModified D-Bus signal to printer properties interface.
  - More robustness for printer properties dialog
    when printer removed (Ubuntu #741987).
  - Fixed PPDs loader when using CUPS remotely or
    when DBus not available (bug #693515).
  - Handle failure to load PPDs more gracefully (Ubuntu #742409).
  - Avoid traceback when cancelling New Printer dialog after failure.
  - Make sure everything is ready before handlers might be called (bug #689336).
  - Ensure consistency in jobviewer if add_job fails (bug #693055, bug #632551).
  - Be defensive against CUPS returning incorrect job IDs (Ubuntu #721051).
  - Job viewer's attribute window: Convert job numbers and
    attribute values to strings (Ubuntu bug #733088).
  - udev-configure-printer: be more defensive when
    parsing CUPS response (Ubuntu #760661).

* Tue Mar 22 2011 Tim Waugh <twaugh@redhat.com> 1.3.2-2
- Fixed traceback in newprinter.py (bug #680683).
- Improvements for check-device-ids from upstream.
- Don't start the applet in GNOME at all (bug #677676), now that GNOME
  Shell is capable of handling New Printer notifications. (Note that
  automatic driver installation won't work until GNOME Shell implements
  that part.)

* Fri Mar 18 2011 Tim Waugh <twaugh@redhat.com> 1.3.2-1
- 1.3.2:
  - Set connected state when connecting to server fails (bug #685098).
  - Handle the situation where cupsd has died/restarted more gracefully.
  - Renamed ui/*.ui -> ui/*.glade again, fixing translations.
  - Just hide Printer Properties dialog on delete-event (Ubuntu #729966).
  - Extra job options: print-quality, printer-resolution, output-bin.
  - Automatically show horizontal scrollbar in job options screen.
  - Ignore "output-mode-default" attribute as it is not settable.
  - Handle IPP_TAG_RESOLUTION types (requires pycups-1.9.55).
  - Don't traceback if option value cannot be handled.
  - Fixed traceback in options.py (bug #679103).
  - Handle URIs in Find Network Printer entry, and use 'Enter URI'
    instead of 'Other' (bug #685091).
  - Use "Do It Later" instead of "Cancel" for adjust firewall dialog
    (trac #213).
  - Fixed an instance where NewPrinterGUI might not have self.printers
    set (bug #680683).
  - IPPHostname can contain colon (to specify port).
  - Fixed automatic driver installation when changing the driver.
  - Removed stale code left over from conversion to gobjects.
  - Ensure all uses of ppdsloader supply the Device ID.
  - Fixed some small typos in newprinter --help output.
  - Prevent traceback after 2nd drivers search dialog is cancelled
    (bug #680288).
  - Activated and fixed testing mode for device ID/driver association
  - Match HP-Fax2/3/... PPDs, as well as Ubuntu/Debian hpijs-ppds
    packages.
  - preferreddrivers.xml: Identify hpcups and hpijs fax PPDs.
  - Match native hpijs driver (drv:///hp/hpijs.drv/...) as "hpijs".
  - Handle Ubuntu locations of hpcups.drv and hpijs.drv.
  - preferreddrivers.xml: match OpenPrinting gutenprint PPD names as
    gutenprint.
  - Removed DES field check altogether.
  - xmldriverprefs.test: show order more clearly.
  - Make xmldriverprefs.test() debugging optional.
  - More debugging during PPD selection.
  - Prefer foomatic PostScript drivers before PCL drivers (except
    foomatic-recommended ones).

* Thu Feb 17 2011 Tim Waugh <twaugh@redhat.com> 1.3.1-1
- 1.3.1:
  - Fixed page sequence when adding a printer with an exactly-matching
    driver.
  - firewall: fixed cache behaviour.
  - Defer calls to populateList initiated by monitor.
  - Removed duplicate method definition.
  - monitor: always set self.bus even when D-Bus not available.

* Thu Feb 17 2011 Tim Waugh <twaugh@redhat.com> 1.3.0-3
- Prevent traceback during libsane-hpaio installation check.

* Wed Feb 16 2011 Tim Waugh <twaugh@redhat.com> 1.3.0-2
- Don't show job notifications from the applet, just do New Printer
  notifications and handle requests to install printer drivers
  (bug #677676).

* Wed Feb 16 2011 Tim Waugh <twaugh@redhat.com> 1.3.0-1
- 1.3.0:
  - Prevent look-up failures in dnssdresolve (Ubuntu #716357).
  - Install libsane-hpaio when appropriate (bug #585362).
  - Avoid double-checking networked HPLIP-able devices.
  - Use #!/usr/bin/python throughout, even for non-executables.
  - Don't display tooltips in the jobviewer as they do not work at
    all.
  - Translation updates.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.97-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb 09 2011 Jiri Popelka <jpopelka@redhat.com> 1.2.97-1
- 1.2.97:
  - Handle failure to connect in PrinterURIIndex (bug #668568).
  - Fixed bugs in gtk_label_autowrap.py (bug #637829).
  - Avoid Foomatic/pxlmono until output size issue is fixed (bug #661814).
  - Avoid traceback when notification daemon has persistence (bug #671375).
  - Don't crash when DISPLAY is unset (bug #676339, #676343).
  - Improvements for DNS-SD support from Till Kamppeter
  - troubleshoot: handle wrong server name but right IP address.
  - Update printer properties after NewPrinter dialog has changed PPD/device.
  - Don't rely on CUPS_PRINTER_COMMANDS alone.
  - Use set_autowrap() from slip.gtk module when possible.

* Fri Jan 21 2011 Jiri Popelka <jpopelka@redhat.com> 1.2.96-3
- Fixed driver selection when there are duplicate PPDs available. (#667571)
- Grabbing focus for editing breaks it (bug #650995).

* Tue Jan 18 2011 Jiri Popelka <jpopelka@redhat.com> 1.2.96-2
- Allow %, ( and ) characters in dnssd URI (bug #669820).

* Mon Jan 17 2011 Jiri Popelka <jpopelka@redhat.com> 1.2.96-1
- 1.2.96:
  - Remove reference to current printer on exit (bug #556548).
  - Handle cups.Connection() failure in PrinterURIIndexr (bug #648014).
  - Block unwanted characters when editing queue name (bug #658550).
  - Initialise D-Bus threading in timedops module (bug #662047).
  - many other fixes

* Thu Dec  2 2010 Tim Waugh <twaugh@redhat.com> - 1.2.95-4
- Grab focus on the IconView after setting it editable (bug #650995).

* Tue Nov 30 2010 Tim Waugh <twaugh@redhat.com> - 1.2.95-3
- Removed calls to pynotify.Notification.attach_to_status_icon()
  (bug #657722).

* Fri Nov 26 2010 Jiri Popelka <jpopelka@redhat.com> 1.2.95-2
- Added %%ghost to /var/run/udev-configure-printer/usb-uris (bug #656698).

* Thu Nov 25 2010 Tim Waugh <twaugh@redhat.com> - 1.2.95-1
- 1.2.95.
- Removed pycups and pysmbc tarballs as they are now packaged
  separately as python-cups and python-smbc.

* Mon Nov 22 2010 Tim Waugh <twaugh@redhat.com> - 1.2.5-8
- Added in missing part of patch for last change (bug #655317).

* Wed Nov  3 2010 Tim Waugh <twaugh@redhat.com> - 1.2.5-7
- Don't use status icon if notification server supports persistence.

* Fri Oct 29 2010 Tim Waugh <twaugh@redhat.com> - 1.2.5-6
- Make sure InstallPrinterDrivers gets correctly typed values (bug #647270).

* Sun Oct 24 2010 Jiri Popelka <jpopelka@redhat.com> 1.2.5-5
- Correct newly added NPTLpdQueue.patch (bug #646002).

* Fri Oct 22 2010 Jiri Popelka <jpopelka@redhat.com> 1.2.5-4
- Don't check ComboBoxEntry for allowed characters (bug #644131).

* Thu Oct 14 2010 Tim Waugh <twaugh@redhat.com> - 1.2.5-3
- Always use MFG and MDL fields for InstallPrinterDrivers interface
  (bug #643073).

* Thu Oct 14 2010 Tim Waugh <twaugh@redhat.com> - 1.2.5-2
- Show debug output whenever InstallPrinterDrivers is called.

* Wed Oct 13 2010 Tim Waugh <twaugh@redhat.com> - 1.2.5-1
- 1.2.5:
  - CMD-field matching for PPDs (bug #630058).
  - Avoid crash in jobviewer (bug #640904).
  - Don't try to modify firewall for SNMP broadcast responses
    as it doesn't work (trac #214).
  - Correctly parse snmp backend output when fetching
    Device ID (bug #639394).
  - XmlHelper: Don't indent output when saving to file (bug #639586).
  - GroupsPaneModel: Avoid crash when removing queue (bug #639586).
  - Use "Do It Later" instead of "Cancel" for adjust firewall
    dialog (trac #213).
  - Delete Bluetooth printer's queue when unpaired.
  - Show examples of IPP URIs (bug #575795).
  - Use actual Device ID strings in 'no match' debug
    message (bug #630350).
  - Prevent disallowed characters in text entry fields when adding
    new printer (bug #621199).
  - Fixed race condition while renaming printer (bug #625502).
  - Request required job attributes rather than assuming they will
    be present in response (bug #635719).
  - Discard disallowed characters when renaming (bug #612315).
  - Mark more translatable strings (bug #634436).

* Wed Sep 29 2010 jkeating - 1.2.4-3
- Rebuilt for gcc bug 634757

* Mon Sep 13 2010 Tim Waugh <twaugh@redhat.com> - 1.2.4-2
- Rebuilt with updated translations.

* Thu Aug 26 2010 Jiri Popelka <jpopelka@redhat.com> 1.2.4-1
- Updated to 1.2.4:
  - Error checking in on_job_cancel_prompt_response (bug #608283).
  - Fixed UDEV_RULES conditional; also, avoid unnecessary tests.
  - Fill in username before calling set_auth_info (bug #609515).
  - Make the 'Add' button actually do something.
  - Initialise downloadable_drivers dict earlier (bug #608815).
  - Strip ' BR-Script3' from the names of Brother PPDs.
  - Sanitize loading of non-existing icon (bug #612415).
  - udev helper: use CUPS defaults when connecting.
  - Blacklist certain printer state reasons (bug #520815).
  - Exclude dnssd backend from udev search.
  - Avoid double-destroy in ppdsloader.
  - Catch KeyError in jobviewer when printer uri not known (bug #615727).
  - Changed shebang in executables (bug #618357).
  - Make udev-configure-printer work for Bluetooth (Bastien Nocera).
  - Merged Till Kamppeter's patches.
    - Access OpenPrinting via the web query API with redirect support.
    - Prioritize DNS-SD-based URIs against IP-based URIs.
    - Added missing "import gobject" to probe_printer.py.
    - On discovered network printers do not only cache make and model but also the device ID.
    - Fix recognition of remote CUPS queues when setting up an IPP queue.
    - Added delay to the auto-start of the applet.
    - Do not error out on missing firewall D-Bus service.
    - Make multi-threaded driver package search via Jockey work.
    - Prioritize HP's hpcups driver against HPIJS.
    - Silence error messages of missing PrinterDriversInstaller D-Bus service.
    - Improvements for setting up Bluetooth printers.
    - udev-configure-printer: Match usblp, libusb, HPLIP, and USB device file URIs.
    - Fill the queue list when clicking "Probe" in LPD printer setup screen.
    - Remove the ":9100" from discovered "socket://..." URIs.
    - Integration of the dnssd CUPS backend and assosiation of DNS-SD names and IPs.
    - When setting up a printer search for local drivers before searching the internet.

* Sun Aug 22 2010 Tim Waugh <twaugh@redhat.com> - 1.2.3-6
- Updated pysmbc to 1.0.9.

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 1.2.3-5
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon Jul 12 2010 Jiri Popelka <jpopelka@redhat.com> 1.2.3-4
- Moved COPYING file to libs sub-package.

* Fri Jun 25 2010 Tim Waugh <twaugh@redhat.com> - 1.2.3-3
- Updated pycups to 1.9.51 (bug #584991).

* Thu Jun 24 2010 Tim Waugh <twaugh@redhat.com> - 1.2.3-1
- Updated to 1.2.3:
  - Use toolbar instead of menubar in JobsViewer (trac #205).
  - Fixed HTTPError status code handling when changing server
    settings.
  - Fixed traceback with driver auto-selection (bug #590193).
  - Only local filenames can be selected for troubleshoot.txt
    (bug #590529).
  - Fixed cups-pk-helper FileGet usage (bug #587744).
  - Escape printer names in error dialog markup (Ubuntu #567324).
  - Avoid traceback changing PPD for queue with bad PPD.
  - Attempt to translate backend device-info strings (Ubuntu #557199).
  - Don't buffer debugging output.
  - Avoid leaking Connection objects when cancelling jobs.
  - Threading fixes (trac #206).
  - Canon naming fixes from vendor.
  - Make deep copy of list of job ids to cancel (bug #598249).
  - Bluetooth auto-config support.
  - Restored keybindings/tooltips lost in switch to action groups
    (trac #208).
  - Spinner icon has to have more than one frame (bug #603034).
  - Add job to active_jobs only if we're interested in it
    (bug #604492).
  - Make sure automatically-created queues will work; delete queue if
    missing executables.
  - Don't add queues for Graphtec devices (bug #547171).
  - Avoid KeyError in AdvancedServerSettings.py (bug #606798).
  - Handle empty notify-subscribed-event subscription attributes
    (bug #606909).

* Wed Jun 02 2010 Jiri Popelka <jpopelka@redhat.com> 1.2.2-4
- Initialise auto_make to the empty string (bug #590193).

* Tue May 18 2010 Tim Waugh <twaugh@redhat.com> - 1.2.2-3
- Updated pycups to 1.9.50.
- Updated pysmbc to 1.0.7.

* Thu May 13 2010 Tim Waugh <twaugh@redhat.com> - 1.2.2-2
- cups-pk-helper FileGet method requires directory it can write to
  (bug #587744).

* Fri May  7 2010 Tim Waugh <twaugh@redhat.com> - 1.2.2-1
- Updated to 1.2.2:
  - Check we are connected to the local server for server firewall
    changes and package installation.
  - Avoid Yes/No buttons (trac #204).
  - Set gettext domain for new printer dialog (Ubuntu #557199).
  - Make sure the printer we are changing the PPD for still exists
    and close New Printer window if not (bug #581668).
  - Specify requested_attributes in getJobs if possible (bug #584806).
  - Resolve DNS-SD hostnames for physical device comparision
    (trac #179).
  - jobviewer: PrinterURIIndex fix when no initial printer names and
    when looking up by name.
  - Don't fetch Device ID from network printer if we already know it.
  - Applet module no longer needs to import statereason.
  - Removed doubled-up 'translatable' attribute in UI file
    (Ubuntu #571662).
  - Fixed indentation in PK1Connection.getDevices.
  - No need to introspect CupsPkHelper every time, just once.
  - troubleshoot: turn off debugging before fetching error log.
  - Fixed localized state reasons (bug #587718).
  - Match Kyocera as manufacturer when only model name reported
    (Ubuntu #564633).
  - Fixed TreeIter handling in update_job_creation_times (bug #588409).
  - Make Verify buttons auto-sized (Ubuntu #575048).
  - Fixed a troubleshooter string and some SMB auth dialog strings
    that were not being translated (Ubuntu #557199).
  - Show unmatched IEEE 1284 Device IDs in less confusing format.
  - check-device-ids: run SNMP query for lpd URIs too.
  - Handle HTTPError from AdvancedServerSettingsDialog, and treat any
    HTTP errors as failures (bug #587744).
  - asyncconn/asyncipp: some fixes for connection/reconnection
    failures.
  - ppdsloader: watch out for errors when connecting.
  - Initialise GUI.printers in constructor (bug #589793).
  - Always use close_fds=True in subprocess.Popen calls (bug #587830).
  - Translation updates.

* Thu Apr 22 2010 Tim Waugh <twaugh@redhat.com> - 1.2.1-2
- Specify requested attributes in getJobs if possible (bug #584806).
- Added optional requested_attributes argument to Connection.getJobs
  (bug #584806).

* Thu Apr 15 2010 Tim Waugh <twaugh@redhat.com> - 1.2.1-1
- Updated to 1.2.1:
  - Fixed missing translations (bug #580442).
  - Offer to adjust firewall when necessary.
  - Avoid tracebacks when adjusting server settings.
  - Handle IPP failure fetching printer attributes for completed jobs
    (Ubuntu #562679).
  - monitor: don't crash if job-state attribute is missing
    (Ubuntu #562441).
  - troubleshoot: handle IPPError in PrintTestPage module (bug #579957).
  - Lots of check-device-ids fixes.

* Mon Apr 12 2010 Tim Waugh <twaugh@redhat.com> - 1.2.0-13
- Use JobCancel compatibility method until cups-pk-helper-0.1.0 is
  packaged (bug #581315).

* Sat Mar 27 2010 Tim Waugh <twaugh@redhat.com> - 1.2.0-12
- check-device-ids: use make-and-model field for best-matching.
- Use upstream fix for async bugs.

* Fri Mar 26 2010 Tim Waugh <twaugh@redhat.com> - 1.2.0-11
- More async traceback fixes (Ubuntu #547075).

* Fri Mar 26 2010 Tim Waugh <twaugh@redhat.com> - 1.2.0-10
- Better inklevel 25/50/75 markers.
- Fixed window transience for 'Change Device URI'.
- More async traceback fixes (Ubuntu #547075).

* Thu Mar 25 2010 Tim Waugh <twaugh@redhat.com> - 1.2.0-9
- check-device-ids: use correct paths for LSB model URIs.
- Fixed cdi-search-harder patch.

* Thu Mar 25 2010 Tim Waugh <twaugh@redhat.com> - 1.2.0-8
- Fixed traceback in asyncipp (bug #576932).
- check-device-ids: search harder for missing Device IDs.
- Make inklevel widget easier to read (bug #576930).

* Wed Mar 24 2010 Tim Waugh <twaugh@redhat.com> - 1.2.0-7
- Use new JobCancelPurge cups-pk-helper method (bug #576496).

* Mon Mar 22 2010 Tim Waugh <twaugh@redhat.com> - 1.2.0-6
- Initialize downloadable_drivers when OpenPrinting query fails (bug #574562).

* Mon Mar 22 2010 Tim Waugh <twaugh@redhat.com> - 1.2.0-5
- Fixed pycups build with new distutils.
- Fixed reconnection error handling in IPPAuthOperation class (bug #575198).

* Fri Mar 19 2010 Tim Waugh <twaugh@redhat.com> - 1.2.0-4
- check-device-ids.py: Fixed driver-URI to filename mapping.

* Fri Mar 19 2010 Tim Waugh <twaugh@redhat.com> - 1.2.0-3
- The canonical name for Kyocera is Kyocera Mita.
- Show CMD field in check-device-ids.py.

* Thu Mar 18 2010 Tim Waugh <twaugh@redhat.com> - 1.2.0-2
- Fixed traceback in check-driver-ids.py when no drivers are found
  (bug #574827).

* Wed Mar 17 2010 Tim Waugh <twaugh@redhat.com> - 1.2.0-1
- Updated to pycups-1.9.49.
- 1.2.0:
  - Another error handling fix in check-device-ids.py.
  - Added StartupNotify=true to 'manage print jobs' desktop file.

* Tue Mar 16 2010 Tim Waugh <twaugh@redhat.com> - 1.1.93-7
- Import modules we catch exceptions from (bug #574117).

* Mon Mar  8 2010 Jiri Popelka <jpopelka@redhat.com> 1.1.93-6
- Fixed pycups to be more cautious when removing
  the Connection object from the list (bug #567386).

* Wed Mar  3 2010 Tim Waugh <twaugh@redhat.com> - 1.1.93-5
- Added comments for all sources and patches.
- Ship COPYING files.

* Mon Mar  1 2010 Tim Waugh <twaugh@redhat.com> - 1.1.93-4
- Use icon name 'printer' instead of 'gnome-dev-printer'.

* Mon Mar  1 2010 Tim Waugh <twaugh@redhat.com> - 1.1.93-3
- Attempt to install drivers in the Device ID checker.

* Sun Feb 28 2010 Tim Waugh <twaugh@redhat.com> - 1.1.93-2
- Import gobject in gtkspinner.py.

* Sat Feb 27 2010 Tim Waugh <twaugh@redhat.com> - 1.1.93-1
- 1.1.93.

* Mon Feb 22 2010 Tim Waugh <twaugh@redhat.com> - 1.1.92-4
- Removed Device ID hacks for Kyocera and HP.  This avoids a false
  positive for the incorrect-Device-ID warning.

* Mon Feb 22 2010 Jiri Popelka <jpopelka@redhat.com> 1.1.92-3
- Catch RuntimeError in statereason.py when cupsGetPPD2 fails (bug #566938).

* Sun Feb 21 2010 Tim Waugh <twaugh@redhat.com> - 1.1.92-2
- Display a warning when the wrong IEEE 1284 Device ID is detected.

* Fri Feb 19 2010 Tim Waugh <twaugh@redhat.com> - 1.1.92-1
- 1.1.92.

* Wed Feb 17 2010 Tim Waugh <twaugh@redhat.com> - 1.1.91-3
- Convert MFG and MDL to lowercase before D-Bus call to work around
  bug #566217.

* Thu Feb 11 2010 Tim Waugh <twaugh@redhat.com> - 1.1.91-2
- Avoid clearing device settings when adding printer (bug #563989).

* Mon Feb  8 2010 Tim Waugh <twaugh@redhat.com> - 1.1.91-1
- 1.1.91.
- No longer requires usermode (bug #562270).

* Mon Jan 25 2010 Tim Waugh <twaugh@redhat.com> - 1.1.90-3
- Set model for LPD queue ComboEntry (bug #558484).
- Only add current device to list when all devices found (bug #558524).
- Fixed statereason localization for raw queues (bug #558156).
- Fixed async fallback again (bug #557854).

* Thu Jan 21 2010 Tim Waugh <twaugh@redhat.com> - 1.1.90-2
- Added GtkAdjustments for all XML-declared SpinButtons.
- Fixed traceback when renaming a printer.

* Tue Jan 19 2010 Tim Waugh <twaugh@redhat.com> - 1.1.90-1
- 1.1.90 development release.

* Tue Jan 19 2010 Tim Waugh <twaugh@redhat.com> - 1.1.16-10
- Update pycups to 1.9.48.

* Mon Jan 18 2010 Tim Waugh <twaugh@redhat.com> - 1.1.16-9
- Clean up temporary files when localizing statereason (bug #552768).
- Make sure serial device widgets are always initialized (bug #556488).
- Handle errors more gracefully in userdefault.py (bug #556345).
- Don't rely on cups-pk-helper being around (bug #556170).
- Avoid traceback when checking on connecting backends (bug #555552).

* Mon Jan 11 2010 Tim Waugh <twaugh@redhat.com> - 1.1.16-8
- Fixed traceback when copying printer with certain job options
  set (bug #554268).

* Mon Jan 11 2010 Tim Waugh <twaugh@redhat.com> - 1.1.16-7
- Fixed traceback introduced in recent fix (bug #554372).

* Thu Jan  7 2010 Tim Waugh <twaugh@redhat.com> - 1.1.16-6
- Fixed crash when using keyring for auth without password (bug #553141).

* Thu Jan  7 2010 Tim Waugh <twaugh@redhat.com> - 1.1.16-5
- Fixed typo introduced in recent fix (bug #551436).

* Wed Jan  6 2010 Tim Waugh <twaugh@redhat.com> - 1.1.16-4
- Use %%global instead of %%define.

* Wed Jan  6 2010 Tim Waugh <twaugh@redhat.com> - 1.1.16-3
- Fixed pycups IPPRequest attribute handling bug.
- Make sure there are enough ink level values (bug #541882).
- Make sure the printer we added still exists before selecting it
  (bug #551436).
- Set notification timeouts appropriately (bug #550829).
- Avoid traceback in NewPrinterGUI.init (bug #550442).
- Avoid traceback in on_jobviewer_exit (bug #550437).

* Wed Dec 23 2009 Tim Waugh <twaugh@redhat.com> - 1.1.16-2
- Prefer foomatic-recommended drivers (bug #550108).
- Pre-select correct driver when adding or changing a queue (bug #550075).
- Fixed typo (bug #550096).

* Tue Dec 22 2009 Tim Waugh <twaugh@redhat.com> - 1.1.16-1
- Updated pycups to 1.9.47.
- 1.1.16:
  - Ignore com.apple.print.recoverable state reason.
  - Prevent traceback in found_network_printer_callback (bug #547765).
  - Use asynchronous connection class for fetching device lists
    (bug #549749).
  - Prefer Foomatic/hpijs to hpcups for the time being.
  - Clear device screen each time a new dialog is presented.
  - Constraints handling fix.

* Fri Dec 18 2009 Jiri Popelka <jpopelka@redhat.com> 1.1.15-9
- Prevent traceback when no downloadable driver selected (#548449).

* Mon Dec 14 2009 Jiri Popelka <jpopelka@redhat.com> 1.1.15-8
- Prevent traceback when cancel button in troubleshooter pressed (#546821).

* Wed Dec  9 2009 Tim Waugh <twaugh@redhat.com> - 1.1.15-7
- Fixed jobviewer traceback with short-lived state reasons (bug #545733).

* Tue Dec  8 2009 Tim Waugh <twaugh@redhat.com> - 1.1.15-6
- Fixed traceback with short lpd device URIs (bug #545397).

* Mon Dec  7 2009 Tim Waugh <twaugh@redhat.com> - 1.1.15-5
- Fixed traceback when troubleshooter operation is cancelled (bug #544356).

* Thu Dec  3 2009 Tim Waugh <twaugh@redhat.com> - 1.1.15-3
- Fixed cupsd.conf parsing when lines begin with blanks (bug #544003).
- Don't overwrite BrowsePoll settings in basic settings dialog (bug #543986).

* Thu Dec  3 2009 Tim Waugh <twaugh@redhat.com> - 1.1.15-2
- Handle RuntimeError when localizing state reason (bug #543937).

* Mon Nov 30 2009 Tim Waugh <twaugh@redhat.com> 1.1.15-1
- 1.1.15:
  - Fixed traceback introduced by fix to bug #541882.

* Fri Nov 27 2009 Tim Waugh <twaugh@redhat.com> 1.1.14-1
- 1.1.14:
  - Retry when reconnection fails (bug #541741).
  - Prevent traceback with bad marker-levels attribute (bug #541882).

* Thu Nov 26 2009 Tim Waugh <twaugh@redhat.com> 1.1.13-12
- Prevent display of marker levels from making the properties dialog
  too big (bug #540826).
- Place the window in the middle of the screen (bug #539876).
- Fixed editability of PPD options for explicit IPP queues
  (bug #541588).

* Mon Nov 23 2009 Jiri Popelka <jpopelka@redhat.com> 1.1.13-11
- Prevent traceback when PackageKit is not installed (bug #540230).

* Wed Nov 11 2009 Tim Waugh <twaugh@redhat.com> 1.1.13-10
- Suggest installing foomatic-db-ppds when appropriate (bug #536831).

* Thu Nov  5 2009 Tim Waugh <twaugh@redhat.com> 1.1.13-9
- Release bump.

* Thu Nov  5 2009 Tim Waugh <twaugh@redhat.com> 1.1.13-8
- Fail gracefully if the new printer has disappeared before the user
  has responded to the test page prompt (bug #533109).

* Mon Nov  2 2009 Tim Waugh <twaugh@redhat.com> 1.1.13-7
- Fixed typo in de.po (bug #532371).

* Fri Oct 30 2009 Tim Waugh <twaugh@redhat.com> 1.1.13-6
- Avoid traceback in IPP notification handlers (bug #530641).
- Avoid epydoc dependency.

* Thu Oct 29 2009 Tim Waugh <twaugh@redhat.com> 1.1.13-5
- Added upstream patch for custom state reasons (bug #531872).
- Strip 'zjs' from make-and-model as well (bug #531869).

* Wed Oct 28 2009 Tim Waugh <twaugh@redhat.com> 1.1.13-4
- Troubleshoot: connect to the right server when choosing a network
  queue (bug #531482).
- Strip 'zxs' and 'pcl3' from make-and-model (bug #531048).
- Fixed visibility tracking for jobs window (bug #531438).
- Don't display properties dialog for first test page (bug #531490).
- Determine make/model for network printers (bug #524321).
- Auto-select the correct driver entry for raw queues.
- Avoid traceback in PhysicalDevice.py.
- Let Return key activate the Find button for Find Network Printer.

* Tue Sep 22 2009 Tim Waugh <twaugh@redhat.com> 1.1.13-3
- Fixed missing import in probe_printer module.
- Fixed race when fetching device list (bug #521110).

* Fri Sep 18 2009 Tim Waugh <twaugh@redhat.com> 1.1.13-2
- Iconify jobs window into status icon.
- Avoid showing the publish-printers dialog when not necessary.
- Fixed traceback when cancelling change-driver dialog.
- Fixed data button state.

* Mon Sep 14 2009 Tim Waugh <twaugh@redhat.com> 1.1.13-1
- 1.1.13:
  - Translation updates (bug #522451).

* Fri Sep  4 2009 Tim Waugh <twaugh@redhat.com> 1.1.12-8
- Further speed improvement when fetching devices.

* Thu Sep  3 2009 Tim Waugh <twaugh@redhat.com> 1.1.12-7
- Speed improvement when fetching devices.
- Allow raw devices to be changed.

* Fri Aug 28 2009 Tim Waugh <twaugh@redhat.com> 1.1.12-6
- Fixed PPD/IPP string translation.
- Fixed proxy authentication.

* Thu Aug 27 2009 Tim Waugh <twaugh@redhat.com> 1.1.12-4
- Ported to polkit-1.

* Wed Aug 26 2009 Tim Waugh <twaugh@redhat.com> 1.1.12-3
- Handle icon load failure gracefully.
- Fixed statereason icon names.

* Wed Aug 26 2009 Tim Waugh <twaugh@redhat.com> 1.1.12-2
- Fixed traceback in on_tvNPDeviceURIs_cursor_changed (bug #519367).

* Tue Aug 25 2009 Tim Waugh <twaugh@redhat.com> 1.1.12-1
- 1.1.12:
  - Troubleshooting fix.
  - Fixed applet traceback when printing test page.
  - Removed completed job notifications (trac #181).
  - Show printer status in printer icons (bug #518020).
  - Use paused icon when printer state reason is 'paused'.
  - Driver preference order fixes.
  - Job status icon and state reason display in jobs list
    (bug #518070).
  - Fixed overactive job creation times update timer.
  - Use preferred D-Bus object path for AuthenticationAgent
    (bug #518427).
  - Fixed disabling a printer when PolicyKit call fails.
  - Set appropriate status icon tooltip when configuration printer
    (bug #518007).
  - Use separate thread for verifying IPP queue (bug #518065).
  - Use newer tooltip API to avoid deprecation warnings.
  - Compare MFG/MDL case-insensitively in udev rule.
  - Support for cups-pk-helper's DevicesGet method.
  - Don't attempt to use PolicyKit if running as root.
  - Support for localized marker names (trac #183).
  - Other small fixes.

* Thu Aug 20 2009 Tim Waugh <twaugh@redhat.com> 1.1.11-6
- Applied patch from 1.1.x (52a73b6).
  - Better printer icons representing status (bug #518020).
  - Use paused ico nwhen printer state reason is 'paused'.
  - Job status icon and state reason in jobs treeview (bug #518070).
  - Job creation times display fixes.
  - Use preferred object path for AuthenticationAgent (bug #518427).

* Wed Aug 19 2009 Tim Waugh <twaugh@redhat.com> 1.1.11-5
- Applied patch from 1.1.x (3f45e96):
  - Show a 'paused' emblem for rejecting/disabled printers
    (bug #518020).
  - Set appropriate tooltip when configuring printer (bug #518007).
  - Use separate thread for verifying IPP queue (part of bug #518065).
  - Better driver preference order (bug #518045).

* Fri Aug 14 2009 Tim Waugh <twaugh@redhat.com> 1.1.11-4
- Compare MFG and MDL fields case insensitively when adding automatic
  queues, because HPLIP provides them with different case than the
  actual devices do.  Upstream HPLIP bug:
  https://bugs.launchpad.net/hplip/+bug/405804

* Fri Aug 14 2009 Tim Waugh <twaugh@redhat.com> 1.1.11-3
- Own /var/run/udev-configure-printer.

* Thu Aug 13 2009 Tim Waugh <twaugh@redhat.com> 1.1.11-2
- Updated cupspk DevicesGet call for accepted API.

* Fri Aug  7 2009 Tim Waugh <twaugh@redhat.com> 1.1.11-1
- 1.1.11:
  - Several udev-configure-printer fixes.
  - Use case-insensitive PPD matching.
  - Better URI validity testing.
  - Another stale printer status icon fix.
  - Notice when jobs stop due to backend errors.
  - Warn about job history when renaming printers.
  - Small UI improvements.

* Tue Aug  4 2009 Tim Waugh <twaugh@redhat.com> 1.1.10-8
- Dropped foomatic dependency from libs package.

* Fri Jul 31 2009 Tim Waugh <twaugh@redhat.com> 1.1.10-7
- Sync with 1.1.x.
- Added patch for cupspk DevicesGet method call.

* Mon Jul 27 2009 Matthias Clasen <mclasen@redhat.com> 1.1.10-6
- Drop no-longer-used python-sexy dep

* Sun Jul 26 2009 Tim Waugh <twaugh@redhat.com> 1.1.10-5
- Split out D-Bus service for udev helper.  Build requires
  dbus-glib-devel.

* Fri Jul 24 2009 Tim Waugh <twaugh@redhat.com> 1.1.10-3
- Removed gnome-packagekit dependency.  The presence of
  gpk-install-package-name is detected at run-time, and the program
  acts accordingly.

* Thu Jul 23 2009 Tim Waugh <twaugh@redhat.com> 1.1.10-2
- Applied some udev-configure-printer fixes from upstream.

* Wed Jul 22 2009 Tim Waugh <twaugh@redhat.com> 1.1.10-1
- 1.1.10:
  - New udev rules for adding/enabling/disabling USB printers
    automatically.
  - Now uses gnome-packagekit utility to install packages
    instead of the D-Bus API.
  - Fixed detection of stopped jobs with CUPS 1.4.
  - Fixed tracebacks when adding a new printer and when receiving
    IPP notifications.
  - Fixed 'location' field for printers added on remote CUPS servers.
  - Fixed handling of incorrect authentication.
  - Some UI and troubleshooter fixes have been made.

* Mon Jul  6 2009 Tim Waugh <twaugh@redhat.com> 1.1.8-6
- Requires gnome-packagekit for gpk-install-package-name.

* Fri Jul  3 2009 Tim Waugh <twaugh@redhat.com> 1.1.8-5
- Use gpk-install-package-name instead of trying to use the D-Bus API.
- Spot stopped jobs with CUPS 1.4 as well (trac #177).  This, along
  with the previous fix, addresses bug #509177.
- Map gutenprint filenames to the package name.
- Fixed sensitivity of class member selection arrows (bug #508653).

* Thu Jun 25 2009 Tim Waugh <twaugh@redhat.com> 1.1.8-3
- Use correct 'location' field for printers added remotely.
- Parse nmblookup failures correctly in troubleshooter.
- Prevent traceback on IPP notification after properties dialog
  cancelled.
- Fixed handling of incorrect authentication when not using
  PolicyKit (bug #508102).

* Wed Jun 24 2009 Tim Waugh <twaugh@redhat.com> 1.1.8-2
- Make sure we find https URIs from https backend (bug #507628).
- Avoid showing a non-fatal exception when adding an IPP printer
  (bug #507629).
- Fixed traceback when adding/modifying printer which could lead to
  display bugs (bug #507489).

* Thu Jun 18 2009 Tim Waugh <twaugh@redhat.com> 1.1.8-1
- Updated pycups to 1.9.46.
- Updated to 1.1.8:
  - Select a printer after adding it (trac #145).
  - Make sure the job and printer context menus cannot get out of date
    (trac #175, trac #172).
  - Fixed displayed hold time for held jobs.
  - Use grey ink-drop when there is no marker-colors value instead of
    crashing (bug #505399).
  - Scroll job list window to new job when appropriate.
  - Clean up temporary PPD files (bug #498743).
  - Fixed XML crash (Ubuntu #370469).
  - Fixed automatic printer model selection.
  - Fixed cupspk crash due to missing debugprint import (bug #496722,
    trac #161). 
  - Fixed PhysicalDevice crash (bug #496722, trac #161).
  - Adjusted border padding for New Printer window (bug #493862).
  - Set glade's textdomain in the job viewer (Ubuntu #341765).
  - Fixed URI parsing when verifying IPP URIs.
  - Set relaxed PPD conformance (trac #159).
  - Make troubleshooter work again by disabling cupspk for it.

* Wed May 13 2009 Tim Waugh <twaugh@redhat.com> 1.1.7-4
- Changed requirement on notification-daemon to
  desktop-notification-daemon to allow for other implementations
  (bug #500587).

* Tue Apr 21 2009 Tim Waugh <twaugh@redhat.com> 1.1.7-3
- Moved them back again, as they are not part of the exported
  interface (bug #496808).

* Tue Apr 21 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> 1.1.7-2
- Move files required by system-config-printer-kde to -libs (#496646)

* Tue Apr 14 2009 Tim Waugh <twaugh@redhat.com> 1.1.7-1
- Requires dbus-python (bug #495392).
- Updated to 1.1.7:
  - Updated translations.
  - Don't abort if the jobviewer couldn't show a notification.
  - Don't use setlocale() for locale-independent case conversion.
  - Don't assume the notification daemon can show action buttons.
  - Use case-insensitive matching for model names.
  - HPLIP compatibility fixes.
  - Fixed typo in jobviewer keyring support (Ubuntu #343156).
  - Added support for https device URIs (bug #478677).
  - Prevent traceback in monitor when connection failed (Ubuntu #343387).

* Fri Mar 13 2009 Tim Waugh <twaugh@redhat.com> 1.1.6-1
- No longer requires gnome-python2-gnome.
- Updated to 1.1.6:
  - Translatable string fix for authconn.
  - Romanian allow/deny translation fix (bug #489748).
  - Set glade's textdomain in the jobviewer (Ubuntu #341765).

* Tue Mar 10 2009 Tim Waugh <twaugh@redhat.com> 1.1.5-2
- Added patch for changes in 1.1.x since 1.1.5:
  - Strip " hpijs" from PPD names.
  - Handle there being no operation name set when authentication/retry
    is required.
  - Mark "Unauthorized" PolicyKit dialog strings for translation, and
    change that dialog to an error.
  - Work around marker-* attributes not being presented as lists
    (bug #489512).
  - D-Bus policy tweak.
  - Better PPD fallback searching.
  - Fixed model search oddity when no digits in model name.
  - Fixed locale save/restore in cupshelpers (bug #489313).
  - Use gtk.show_uri() instead of gnome.url_show() (trac #147).
  - Removed HPLIP probe screen (no longer needed).
  - Be certain of having the right cell when starting a rename
    (Ubuntu #333260).
  - Fixed strftime call (Ubuntu #334859).
  - Check dict before use when handling auth-info-required.
  - Handle timed operations being cancelled in the troubleshooter test
    print page (Ubuntu #325084).
  - Put pycups version requirement in monitor module.

* Tue Mar  3 2009 Tim Waugh <twaugh@redhat.com> 1.1.5-1
- 1.1.5.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Tim Waugh <twaugh@redhat.com> 1.1.4-2
- Updated from git:
  - Prevent traceback when adding new printer (bug #486587).

* Wed Feb 18 2009 Tim Waugh <twaugh@redhat.com> 1.1.4-1
- 1.1.4:
  - Skip model selection screen when adding a new printer for which we
    know the exact model.
  - Better integration for HPLIP hp and hpfax queues.
  - Work around HPLIP option parsing bug.
  - Pre-select the current device correctly.
  - Better descriptions for types of available connection.
  - Perform lowercase operations in a locale-independent manner (trac #151).

* Wed Feb 11 2009 Tim Waugh <twaugh@redhat.com> 1.1.3-7
- Updated from git:
  - Avoid tracebacks in main application (bug #484130) and job viewer.
  - Avoid unnecessary modal dialog when adding printer (bug #484960).
  - Don't use notification when authentication is required, just
    display the dialog.

* Tue Feb 10 2009 Tim Waugh <twaugh@redhat.com> 1.1.3-6
- Updated from git:
  - Better make/model discovery for multiple devices (bug #484130).

* Tue Feb 10 2009 Tim Waugh <twaugh@redhat.com> 1.1.3-5
- Updated from git:
  - Handle D-Bus failures when querying Jockey (bug #484402).
  - Set operation when fetching PPD from server (bug #484130).
  - Don't allow prompting when updating the UI for a server failure
    (bug #484130).
  - Fixed printing a test page from the applet (bug #484130).

* Mon Feb  9 2009 Tim Waugh <twaugh@redhat.com> 1.1.3-4
- Requires libxml2-python.

* Sat Feb  7 2009 Tim Waugh <twaugh@redhat.com> 1.1.3-3
- Ship the missing cupspk file (bug #484461).

* Thu Feb  5 2009 Tim Waugh <twaugh@redhat.com> 1.1.3-2
- Added in cups-pk-helper support from upstream.

* Tue Feb  3 2009 Tim Waugh <twaugh@redhat.com> 1.1.3-1
- Requires python-sexy.
- 1.1.3.

* Thu Jan 15 2009 Tim Waugh <twaugh@redhat.com> 1.1.2-1
- 1.1.2.
- Requires gnome-python2-gnomekeyring.

* Thu Jan  8 2009 Tim Waugh <twaugh@redhat.com> 1.1.1-2
- Updated pycups to 1.9.45.

* Sat Dec 20 2008 Tim Waugh <twaugh@redhat.com> 1.1.1-1
- 1.1.1.

* Fri Dec 19 2008 Tim Waugh <twaugh@redhat.com> 1.1.0-1
- 1.1.0.

* Fri Dec 19 2008 Tim Waugh <twaugh@redhat.com> 1.0.12-7
- Updated patch for 1.0.x changes:
  - Fixed stub scripts (bug #477107).

* Fri Dec 19 2008 Tim Waugh <twaugh@redhat.com> 1.0.12-6
- Updated patch for 1.0.x changes:
  - Look harder for locale/page size issues in the troubleshooter
    (trac #118).
  - Troubleshooter speed improvement (trac #123).
  - Localization fixes for authentication dialog (trac #122).
  - Character encoding fixes (trac #124).
  - Handle model names with more than one set of digits (Ubuntu #251244).
  - Catch unable-to-connect error when trying to print a test page
    (Ubuntu #286943).
  - Prevent crash when copying PPD options (Ubuntu #285133).
  - Use get_cursor for the printer properties treeview (Ubuntu #282634).
  - Fix IPP browser when trying to connect to host:port (bug #476396).
  - Make sure we're authenticating as the correct user in authconn.
  - Prevent traceback when adding printer driven by HPLIP
    (bug #477107).
  - Better display of available local HP fax devices.

* Wed Dec 17 2008 Tim Waugh <twaugh@redhat.com> 1.0.12-5
- Added patch for pycups git changes since 1.9.44:
  - Look for test page file in new location for CUPS 1.4 (bug #476612).

* Fri Dec 12 2008 Tim Waugh <twaugh@redhat.com> 1.0.12-4
- Updated patch for 1.0.x changes:
  - Fix for advanced server settings dialog.
  - Fixes for troubleshooter to restore error_log fetching.

* Wed Dec 10 2008 Tim Waugh <twaugh@redhat.com> 1.0.12-3
- Updated patch for 1.0.x changes:
  - Fixed problem that prevented authentication prompt being
    displayed.

* Fri Dec  5 2008 Tim Waugh <twaugh@redhat.com> 1.0.12-2
- Added patch for 1.0.x changes since 1.0.12:
  - Smarter PPD cache in cupshelpers module.
  - Don't write back localized versions of globalized PPDs.

* Mon Dec  1 2008 Tim Waugh <twaugh@redhat.com> 1.0.12-1
- Updated to 1.0.12:
  - Don't automatically replace network printer URIs with
    HPLIP URIs (bug #473129).
  - Fixed some file descriptor and temporary file leaks.
- Updated pycups to 1.9.44.

* Fri Nov 21 2008 Tim Waugh <twaugh@redhat.com> 1.0.11-1
- Updated to 1.0.11.
- Updated pycups to 1.9.43.

* Wed Nov 12 2008 Tim Waugh <twaugh@redhat.com> 1.0.10-2
- Updated to 1.0.10.  Applied patch from git.
- Applied pycups patch from git.

* Tue Oct 21 2008 Tim Waugh <twaugh@redhat.com> 1.0.9-1
- Updated to 1.0.9 for translations.
- Updated pysmbc to 1.0.6.  No longer need pysmbc-git patch.

* Fri Oct 17 2008 Tim Waugh <twaugh@redhat.com> 1.0.8-7
- Added patch for pysmbc changes in git to prevent getdents crashing
  (bug #465975).

* Thu Oct 16 2008 Tim Waugh <twaugh@redhat.com> 1.0.8-6
- Updated patch for 1.0.x changes:
  - Fixed SMB authentication dialog's cancel button (bug #467127).
  - Work around samba bug #5805 by sending debug output to stderr
    instead of stdout.

* Wed Oct 15 2008 Tim Waugh <twaugh@redhat.com> 1.0.8-5
- Updated patch for 1.0.x changes:
  - Fixed SMB authentication (bug #464003).

* Wed Oct 15 2008 Tim Waugh <twaugh@redhat.com> 1.0.8-4
- Updated patch for 1.0.x changes:
  - Removed unneeded debugging output.
  - Don't show the applet in KDE (bug #466945).
  - Auth/error dialog improvements for SMB as for IPP (bug #465407).

* Mon Oct 13 2008 Tim Waugh <twaugh@redhat.com> 1.0.8-3
- Added patch for 1.0.x changes since 1.0.8:
  - Don't use a LinkButton for the 'Problems?' button (bug #465407).
  - Don't use a separator for the server settings dialog (bug
    #465407).
  - Don't set non-zero page size for SpinButtons.
  - Don't show an error dialog if an IPP operation's authentication
    dialog is cancelled by the user, but show an error dialog if the
    password was incorrect (bug #465407).
  - Set Server Settings... menu entry sensitive depending on whether
    we are connected to a server (Ubuntu #280736).
  - Lots of translations updated.

* Mon Sep 29 2008 Tim Waugh <twaugh@redhat.com> 1.0.8-2
- Removed patch (no longer needed).

* Mon Sep 29 2008 Tim Waugh <twaugh@redhat.com> 1.0.8-1
- 1.0.8:
  - Use modelName from custom PPD to suggest name for new printer
    (trac #97).
  - Avoid display problem with installable options.
  - Better matching for Lexmark printers.
  - Catch exceptions from advanced server settings dialog (Ubuntu
    #267557).
  - Added some missing OpenPrinting query fields.
  - Jockey support added.
  - Lots of translations updated.

* Sat Aug 30 2008 Tim Waugh <twaugh@redhat.com> 1.0.7-2
- Handle IPP_FORBIDDEN (bug #460670).

* Fri Aug 29 2008 Tim Waugh <twaugh@redhat.com> 1.0.7-1
- 1.0.7:
  - Efficiency improvements.
  - Small UI improvements for the New Printer dialog.
  - Other small fixes.

* Fri Aug 29 2008 Tim Waugh <twaugh@redhat.com>
- Updated pysmbc to 1.0.5.
- Updated pycups to 1.9.42.

* Tue Aug 26 2008 Tim Waugh <twaugh@redhat.com> 1.0.6-1
- Requires gnome-python2-gnome (bug #460021).
- 1.0.6:
  - More delete-event fixes.
  - Fixed temporary file leak.
  - Fixed dialog leaks.
  - Small UI improvements for the New Printer dialog.
  - Other small fixes.

* Thu Aug 14 2008 Tim Waugh <twaugh@redhat.com> 1.0.5-3
- Include other fixes from upstream including:
  - OpenPrinting API change (trac #74).
  - libnotify API change for 'closed' signal.
  - Notification for job authentication (trac #91).
  - Glade delete-event fixes (trac #88).
  - Pre-fill username in job authentication dialog (trac #87).

* Wed Aug 13 2008 Tim Waugh <twaugh@redhat.com> 1.0.5-2
- Handle HTTP_FORBIDDEN.

* Mon Aug 11 2008 Tim Waugh <twaugh@redhat.com> 1.0.5-1
- 1.0.5.
- Updated pycups to 1.9.41.

* Thu Jul 10 2008 Tim Waugh <twaugh@redhat.com> 1.0.4-1
- 1.0.4.
- Applied upstream patch for pycups to fix getPrinterAttributes when
  requested_attributes is specified.

* Tue Jul  8 2008 Tim Waugh <twaugh@redhat.com> 1.0.3-2
- Better debugging for pysmbc.

* Mon Jun 30 2008 Tim Waugh <twaugh@redhat.com> 1.0.3-1
- Updated pycups to 1.9.40.
- 1.0.3.

* Fri Jun 20 2008 Tim Waugh <twaugh@redhat.com>
- Updated pysmbc to 1.0.4.

* Tue Jun 10 2008 Tim Waugh <twaugh@redhat.com> 1.0.2-1
- 1.0.2.

* Mon Jun  9 2008 Tim Waugh <twaugh@redhat.com> 1.0.1-1
- Updated pysmbc to 1.0.3.
- 1.0.1 (bug #450119).

* Thu Jun  5 2008 Tim Waugh <twaugh@redhat.com>
- Requires notify-python (bug #450139).

* Thu Jun  5 2008 Tim Waugh <twaugh@redhat.com> 1.0.0-3
- Applied patches from upstream (bug #450120).

* Tue Jun  3 2008 Tim Waugh <twaugh@redhat.com> 1.0.0-2
- Applied patches from upstream (bug #449753).

* Thu May 29 2008 Tim Waugh <twaugh@redhat.com>
- Updated pycups to 1.9.39.
- Updated libs summary.

* Tue May 27 2008 Tim Waugh <twaugh@redhat.com> 1.0.0-1
- 1.0.0.

* Fri May 23 2008 Tim Waugh <twaugh@redhat.com> 0.9.93-2
- Fixed small UI problem in SMB browser.

* Fri May 23 2008 Tim Waugh <twaugh@redhat.com> 0.9.93-1
- 0.9.93.

* Tue May 20 2008 Tim Waugh <twaugh@redhat.com> 0.9.92-1
- 0.9.92.

* Tue May 20 2008 Tim Waugh <twaugh@redhat.com> 0.9.91-3
- Sync to trunk.
- Updated pysmbc to 1.0.2.

* Sun May 18 2008 Tim Waugh <twaugh@redhat.com> 0.9.91-2
- Fixed icon search path.

* Fri May 16 2008 Tim Waugh <twaugh@redhat.com> 0.9.91-1
- No longer requires system-install-packages (bug #444645).
- Added pysmbc.  Build requires libsmbclient-devel.
- Don't install consolehelper bits any more as they are no longer needed.
- 0.9.91:
  - User interface overhaul, part 2.

* Thu Apr  3 2008 Tim Waugh <twaugh@redhat.com> 0.9.90-1
- Updated pycups to 1.9.38.
- 0.9.90:
  - User interface overhaul, part 1.

* Thu Apr  3 2008 Tim Waugh <twaugh@redhat.com> 0.7.82.2-1
- 0.7.82.2:
  - Various bug fixes.
  - Translation updates.

* Mon Mar 17 2008 Tim Waugh <twaugh@redhat.com> 0.7.82.1-3
- Updated pycups to 1.9.37.
- More fixes from upstream.

* Wed Mar  5 2008 Tim Waugh <twaugh@redhat.com> 0.7.82.1-2
- Updated pycups to 1.9.36.
- Some fixes from upstream.

* Mon Mar  3 2008 Tim Waugh <twaugh@redhat.com> 0.7.82.1-1
- Requires /usr/bin/system-install-packages not pirut (bug #435622).
- 0.7.82.1:
  - More trouble-shooting improvements.
  - applet: notify user about failed jobs (bug #168370).

* Tue Feb 19 2008 Tim Waugh <twaugh@redhat.com> 0.7.82-1
- Updated to pycups-1.9.35.
- 0.7.82:
  - More trouble-shooting improvements.

* Wed Feb 13 2008 Tim Waugh <twaugh@redhat.com> 0.7.81-1
- 0.7.81:
  - Trouble-shooting improvements and other minor fixes.

* Mon Feb 11 2008 Tim Waugh <twaugh@redhat.com> 0.7.80-2
- Rebuild for GCC 4.3.

* Mon Feb  4 2008 Tim Waugh <twaugh@redhat.com> 0.7.80-1
- Updated to pycups-1.9.34.
- 0.7.80:
  - Trouble-shooting support.

* Fri Jan 25 2008 Tim Waugh <twaugh@redhat.com> 0.7.79-1
- 0.7.79.

* Wed Jan 23 2008 Tim Waugh <twaugh@redhat.com> 0.7.78-5
- Updated to pycups-1.9.33.

* Wed Jan 16 2008 Tim Waugh <twaugh@redhat.com> 0.7.78-4
- Use config-util from new usermode (bug #428406).

* Thu Dec 20 2007 Tim Waugh <twaugh@redhat.com>
- Requires notification-daemon (Ubuntu #176929).
- Requires gnome-python2 for theme support (Ubuntu #176929).
- Requires gnome-icon-theme for printer icon (Ubuntu #176929).

* Mon Dec 17 2007 Tim Waugh <twaugh@redhat.com> 0.7.78-3
- Install Python egg-info file.
- Updated pycups to 1.9.32.

* Tue Nov 27 2007 Tim Waugh <twaugh@redhat.com> 0.7.78-2
- pycups: Applied patch from SVN to allow fetching printer attributes by URI.
- Sync to SVN 1748.

* Thu Nov 22 2007 Tim Waugh <twaugh@redhat.com> 0.7.78-1
- pycups: Fix job-sheets-default attribute.
- Updated pycups to 1.9.31.
- 0.7.78.

* Wed Nov 21 2007 Tim Waugh <twaugh@redhat.com>
- Applied patch to pycups to avoid reading uninitialised
  memory (bug #390431).

* Mon Nov 19 2007 Tim Waugh <twaugh@redhat.com>
- Updated pycups to 1.9.30.

* Tue Oct 30 2007 Tim Waugh <twaugh@redhat.com> 0.7.77-1
- 0.7.77:
  - Tooltips for the button bar buttons (bug #335601).

* Mon Oct 15 2007 Tim Waugh <twaugh@redhat.com> 0.7.76-1
- 0.7.76.

* Thu Oct  4 2007 Tim Waugh <twaugh@redhat.com> 0.7.75-1
- 0.7.75.

* Wed Oct  3 2007 Tim Waugh <twaugh@redhat.com>
- No need to run update-desktop-database because there are no MimeKey
  lines in the desktop files.
- Consistent macro style.

* Tue Oct  2 2007 Tim Waugh <twaugh@redhat.com> 0.7.74.4-1
- Changed PreReq to Requires.
- Mark console.apps file as a config file.
- Mark pam file as a config file (not replaceable).
- No need to ship empty NEWS file.
- Give cupsd.py executable permissions to satisfy rpmlint.
- Provides system-config-printer-gui.
- Mark D-Bus configuration file as a config file.
- Fixed libs summary.
- Better buildroot tag.
- Better defattr.
- Preserve timestamps on explicitly install files.
- Make example pycups program non-executable.
- 0.7.74.4:
  - Updated translations.
  - Several small bugs fixed.

* Thu Sep 27 2007 Tim Waugh <twaugh@redhat.com> 0.7.74.3-1
- 0.7.74.3:
  - Updated translations.
  - Other small bug fixes.

* Tue Sep 25 2007 Tim Waugh <twaugh@redhat.com> 0.7.74.2-3
- Pull in SVN patch from stable branch for foomatic recommended
  drivers (bug #292021).

* Fri Sep 21 2007 Tim Waugh <twaugh@redhat.com> 0.7.74.2-2
- Pull in SVN patch from stable branch for 'Allow printing from
  the Internet' check-box (bug #221003).

* Wed Sep 19 2007 Tim Waugh <twaugh@redhat.com> 0.7.74.2-1
- Updated pycups to 1.9.27.
- 0.7.74.2:
  - When a class is removed on the server, remove it from the UI.
  - When deleting a printer, select the default printer again.
  - Select newly-copied printer.
  - Updated translation (fi).
  - Better --help message.
  - Use strcoll to sort manufacturer names.
  - Avoid duplicate 'recommended' marks.
  - Remove duplicate device URIs.
  - Handle IPP_TAG_NOVALUE attributes (for CUPS 1.3.x).

* Wed Sep 12 2007 Tim Waugh <twaugh@redhat.com>
- Updated pycups to 1.9.26.
- Build requires epydoc.  Ship HTML documentation.

* Fri Sep  7 2007 Tim Waugh <twaugh@redhat.com> 0.7.74.1-1
- 0.7.74.1:
  - Updated Polish translation (bug #263001).
  - Don't select the default printer after changes to another printer have
    been made.
  - Always construct URI from input fields when changing device (bug #281551).
  - Avoid busy-cursor traceback when window is not yet displayed.

* Thu Aug 30 2007 Tim Waugh <twaugh@redhat.com> 0.7.74-1
- Updated pycups to 1.9.25.
- 0.7.74:
  - Fixed New Class dialog.
  - UI fixes.

* Sat Aug 25 2007 Tim Waugh <twaugh@redhat.com>
- More specific license tag.

* Fri Aug 24 2007 Tim Waugh <twaugh@redhat.com> 0.7.73-1
- 0.7.73.

* Fri Aug 10 2007 Tim Waugh <twaugh@redhat.com> 0.7.72-2
- Ship the applet's desktop file.

* Wed Aug  8 2007 Tim Waugh <twaugh@redhat.com> 0.7.72-1
- 0.7.72:
  - Fixed my-default-printer traceback.
  - Improvements to New Printer wizard (Till Kamppeter).

* Fri Aug  3 2007 Tim Waugh <twaugh@redhat.com> 0.7.71-1
- 0.7.71:
  - Don't discard make/model-matched devices when there are ID-matched
    devices (Till Kamppeter).
  - Fixed fallback if no text-only driver is available (Till Kamppeter).
  - Initialise the make/model list when an ID match failed (Till Kamppeter).
  - Better error-handling in default-print application (Ubuntu #129901).
  - UI tweak in admin tool (Ubuntu #128263).
  - Handle socket: URIs (Ubuntu #127074).

* Mon Jul 23 2007 Tim Waugh <twaugh@redhat.com> 0.7.70-2
- Obsoletes/provides desktop-printing.

* Mon Jul  9 2007 Tim Waugh <twaugh@redhat.com> 0.7.70-1
- Requires pirut for system-install-packages.
- 0.7.70:
  - Increased GetReady->NewPrinter timeout.
  - More binary names mapped to package named.
  - Run system-install-packages to install missing drivers (bug #246726).
  - Less debug output.
  - Desktop file fixes for KDE (bug #247299).

* Thu Jun 28 2007 Tim Waugh <twaugh@redhat.com> 0.7.69-1
- No longer requires PyXML (bug #233146).
- Moved applet to main package.
- 0.7.69:
  - Use HardwareSettings category for my-default-printer desktop
    file (bug #244935).
  - Removed unused code.
  - Filter PPDs by natural language (bug #244173).

* Mon Jun 25 2007 Tim Waugh <twaugh@redhat.com>
- The applet requires dbus-x11 (Ubuntu #119570).

* Fri Jun 15 2007 Tim Waugh <twaugh@redhat.com> 0.7.68-1
- 0.7.68:
  - Fixed the notification bubbles.
  - Ship my-default-printer utility.

* Fri Jun  8 2007 Tim Waugh <twaugh@redhat.com> 0.7.67-1
- Don't put TrayIcon or SystemSetup categories in the desktop file.
- Updated pycups to 1.9.24.
- 0.7.67:
  - Fixed desktop files to have capital letters at the start of each
    word in the Name field (bug #242859).
  - Fixed crash when saving unapplied changes.
  - Fixed Device ID parser to always split the CMD field at commas.
  - New PPDs class means we no longer parse the foomatic XML database.

* Wed May 30 2007 Tim Waugh <twaugh@redhat.com> 0.7.66-1
- 0.7.66:
  - Allow job-hold-until to be set (bug #239776).
  - Implement new printer notifications.

* Tue May 22 2007 Tim Waugh <twaugh@redhat.com> 0.7.65-1
- Build requires xmlto.
- Updated to pycups-1.9.22.
- 0.7.65:
  - Use urllib for quoting/unquoting (Val Henson, Ubuntu #105022).
  - Added kn translation.
  - Better permissions on non-scripts.
  - Added man pages.
  - Applet: status feedback.
  - Applet: fixed relative time descriptions.
  - Applet: limit refresh frequency.

* Mon Apr 16 2007 Tim Waugh <twaugh@redhat.com> 0.7.63.1-1
- 0.7.63.1:
  - Small applet fixes.

* Thu Apr  5 2007 Tim Waugh <twaugh@redhat.com> 0.7.63-1
- 0.7.63:
  - Translation updates.
  - Checked in missing file.

* Wed Apr  4 2007 Tim Waugh <twaugh@redhat.com>
- Updated to pycups-1.9.20 for printer-state-reasons fix.

* Mon Apr  2 2007 Tim Waugh <twaugh@redhat.com> 0.7.62-1
- 0.7.62:
  - Use standard icon for admin tool desktop file.
  - Fixed env path in Python scripts.
  - Applet: stop running when the session ends.
  - Prevent a traceback in the SMB browser (bug #225351).
  - 'Manage print jobs' desktop file.

* Fri Mar 30 2007 Tim Waugh <twaugh@redhat.com> 0.7.61-1
- 0.7.61:
  - Fixed retrieval of SMB authentication details (bug #203539).

* Tue Mar 27 2007 Tim Waugh <twaugh@redhat.com> 0.7.60-1
- Updated to pycups-1.9.19.
- Avoid %%makeinstall.
- 0.7.60:
  - Handle reconnection failure.
  - New applet name.

* Mon Mar 26 2007 Tim Waugh <twaugh@redhat.com> 0.7.59-1
- 0.7.59:
  - Fixed a translatable string.
  - Set a window icon (bug #233899).
  - Handle failure to start the D-Bus service.
  - Ellipsize the document and printer named (bug #233899).
  - Removed the status bar (bug #233899).
  - Added an icon pop-up menu for 'Hide' (bug #233899).

* Wed Mar 21 2007 Tim Waugh <twaugh@redhat.com> 0.7.57-1
- Added URL tag.
- 0.7.57:
  - Prevent traceback when removing temporary file (Ubuntu #92914).
  - Added print applet.

* Sun Mar 18 2007 Tim Waugh <twaugh@redhat.com> 0.7.56-2
- Updated to pycups-1.9.18.

* Fri Mar 16 2007 Tim Waugh <twaugh@redhat.com> 0.7.56-1
- 0.7.56:
  - Parse Boolean strings correctly in job options.
  - Small command-set list/string fix (bug #230665).
  - Handle hostname look-up failures.
  - Updated filter-to-driver map.
  - Don't parse printers.conf (bug #231826).

* Tue Feb 27 2007 Tim Waugh <twaugh@redhat.com> 0.7.55-1
- 0.7.55:
  - Use converted value for job option widgets.

* Tue Feb 27 2007 Tim Waugh <twaugh@redhat.com> 0.7.54-1
- 0.7.54:
  - Removed debugging code.

* Tue Feb 27 2007 Tim Waugh <twaugh@redhat.com> 0.7.53-1
- No longer requires rhpl (since 0.7.53).
- 0.7.53:
  - Use gettext instead of rhpl.translate.
  - Better layout for PPD options.
  - Added scrollbars to main printer list (bug #229453).
  - Set maximum width of default printer label (bug #229453).
  - Handle applying changes correctly when switching to another
    printer (bug #229378).
  - Don't crash when failing to fetch the PPD (bug #229406).
  - Make the text entry boxes sensitive but not editable for remote
    printers (bug #229381).
  - Better job options screen layout (bug #222272).

* Tue Feb 13 2007 Tim Waugh <twaugh@redhat.com> 0.7.52-1
- 0.7.52:
  - Sort models using cups.modelSort before scanning for a close
    match (bug #228505).
  - Fixed matching logic (bug #228505).

* Fri Feb  9 2007 Tim Waugh <twaugh@redhat.com> 0.7.51-1
- 0.7.51:
  - Prevent display glitch in job options list when clicking on a printer
    repeatedly.
  - List conflicting PPD options, and embolden the relevant tab
    labels (bug #226368).
  - Fixed typo in 'set default' handling that caused a traceback (bug #227936).
  - Handle interactive search a little better (bug #227935).

* Wed Feb  7 2007 Tim Waugh <twaugh@redhat.com> 0.7.50-1
- 0.7.50:
  - Fixed hex digits list (bug #223770).
  - Added bs translation.
  - Don't put the ellipsis in the real device URI (bug #227643).
  - Don't check for existing drivers for complex command lines (bug #225104).
  - Allow floating point job options (bug #224651).
  - Prevent shared/published confusion (bug #225081).
  - Fixed PPD page size setting.
  - Avoid os.remove exception (bug #226703).
  - Handle unknown job options (bug #225538).

* Tue Jan 16 2007 Tim Waugh <twaugh@redhat.com> 0.7.49-1
- 0.7.49:
  - Fixed a traceback in the driver check code.
  - Fixed a typo in the conflicts message.
  - Handle InputSlot/ManualFeed specially because libcups does (bug #222490).

* Mon Jan 15 2007 Tim Waugh <twaugh@redhat.com> 0.7.48-1
- 0.7.48:
  - Updated translations.

* Fri Jan 12 2007 Tim Waugh <twaugh@redhat.com> 0.7.47-1
- 0.7.47:
  - Fixed minor text bugs (bug #177433).
  - Handle shell builtins in the driver check (bug #222413).

* Mon Jan  8 2007 Tim Waugh <twaugh@redhat.com> 0.7.46-1
- 0.7.46:
  - Fixed page size problem (bug #221702).
  - Added 'ro' to ALL_LINGUAS.

* Wed Jan  3 2007 Tim Waugh <twaugh@redhat.com> 0.7.45-1
- Updated to pycups-1.9.17.
- 0.7.45:
  - Fixed traceback in driver check.

* Tue Jan  2 2007 Tim Waugh <twaugh@redhat.com> 0.7.44-1
- 0.7.44:
  - Fixed traceback in error display (bug #220136).
  - Preserve case in model string when dumping debug output.

* Thu Dec 21 2006 Tim Waugh <twaugh@redhat.com> 0.7.43-1
- 0.7.43:
  - Don't check against IEEE 1284 DES field at all.
  - Merged device matching code (bug #219518).
  - Catch non-fatal errors when auto-matching device.
  - Fixed driver checking bug involving pipelines (bug #220347).
  - Show PPD errors (bug #220136).

* Mon Dec 11 2006 Tim Waugh <twaugh@redhat.com> 0.7.42-1
- 0.7.42:
  - Fixed typo in command set matching code.
  - Case-insensitive matching when Device ID not known to database.

* Thu Dec  7 2006 Jeremy Katz <katzj@redhat.com> - 0.7.41-2
- build against python 2.5

* Thu Dec  7 2006 Tim Waugh <twaugh@redhat.com> 0.7.41-1
- Updated pycups to 1.9.16.
- 0.7.41:
  - Reconnect smoothly after uploading new configuration.
  - Update lpoptions when setting default printer if it conflicts with
    the new setting (bug #217395).
  - Fixed typo in show_HTTP_Error (bug #217537).
  - Don't pre-select make and model when not discoverable for chosen
    device (bug #217518).
  - Set Forward button sensitive on Device screen in new-printer
    dialog (bug #217515).
  - Keep Server Settings selected after applying changes if it was selected
    before.
  - Set Connecting dialog transient for main window.
  - Center Connecting dialog on parent.
  - Optional 'reason' argument for cupshelpers.Printer.setEnabled.
  - Describe devices that have no optional parameters.

* Thu Nov 30 2006 Tim Waugh <twaugh@redhat.com>
- Provide pycups feature.

* Tue Nov 21 2006 Tim Waugh <twaugh@redhat.com> 0.7.40-1
- 0.7.40:
  - Removed username:password from hint string because we add that in
    afterwards.
  - Don't set button widths in create-printer dialog (bug #217025).

* Tue Nov 21 2006 Tim Waugh <twaugh@redhat.com> 0.7.39-1
- 0.7.39:
  - Busy cursor while loading foomatic and PPD list (bug #215527).
  - Make PPD NickName selectable.
  - Added SMB hint label on device screen (bug #212759).

* Tue Nov 14 2006 Tim Waugh <twaugh@redhat.com> 0.7.38-1
- Updated pycups to 1.9.15.
- 0.7.38:
  - Fixed a bug in the 'ieee1284'/'ppd-device-id' parsing code.

* Mon Nov 13 2006 Tim Waugh <twaugh@redhat.com> 0.7.37-1
- 0.7.37:
  - Allow cancellation of test pages (bug #215054).

* Fri Nov 10 2006 Tim Waugh <twaugh@redhat.com> 0.7.36-1
- 0.7.36:
  - Match against commandset (bug #214181).
  - Parse 'ieee1284' foomatic autodetect entries (bug #214761).
  - Don't remove foomatic PPDs from the list (bug #197331).

* Tue Nov  7 2006 Tim Waugh <twaugh@redhat.com> 0.7.35-1
- 0.7.35.

* Thu Nov  2 2006 Tim Waugh <twaugh@redhat.com>
- Updated to pycups-1.9.14 (bug #213136).

* Tue Oct 31 2006 Tim Waugh <twaugh@redhat.com>
- Update desktop database (bug #213249).

* Tue Oct 24 2006 Tim Waugh <twaugh@redhat.com>
- Build requires Python 2.4.

* Mon Oct  2 2006 Tim Waugh <twaugh@redhat.com> 0.7.32-1
- Updated to pycups-1.9.13 for HTTP_FORBIDDEN.
- 0.7.32:
  - Handle HTTP errors during connection (bug #208824).
  - Updated translations (bug #208873).

* Fri Sep 29 2006 Tim Waugh <twaugh@redhat.com> 0.7.31-1
- 0.7.31:
  - Select recommended driver automatically (bug #208606).
  - Better visibility of driver list (bug #203907).

* Fri Sep 29 2006 Tim Waugh <twaugh@redhat.com> 0.7.30-1
- 0.7.30:
  - Translations fixed properly (bug #206622).
  - Button widths corrected (bug #208556).

* Tue Sep 26 2006 Tim Waugh <twaugh@redhat.com> 0.7.28-1
- 0.7.28.  Translations fixed (bug #206622).

* Wed Aug 30 2006 Tim Waugh <twaugh@redhat.com> 0.7.27-1
- Build requires intltool.
- 0.7.27.

* Wed Aug 23 2006 Tim Waugh <twaugh@redhat.com> 0.7.26-1
- 0.7.26.  Fixes bug # 203149.

* Mon Aug 14 2006 Florian Festi <ffesti@redhat.com> 0.7.25-1
- 0.7.25. (bug #202060)

* Fri Aug 11 2006 Tim Waugh <twaugh@redhat.com>
- Fixed description (bug #202189).

* Thu Aug  3 2006 Tim Waugh <twaugh@redhat.com> 0.7.24-1
- 0.7.24.

* Mon Jul 24 2006 Tim Waugh <twaugh@redhat.com> 0.7.23-1
- 0.7.23.  Fixes bug #197866.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.7.22-1.1
- rebuild

* Fri Jul  7 2006 Tim Waugh <twaugh@redhat.com> 0.7.22-1
- 0.7.22.

* Wed Jul  5 2006 Tim Waugh <twaugh@redhat.com> 0.7.21-1
- Updated to pycups-1.9.12.
- 0.7.21.

* Mon Jul  3 2006 Tim Waugh <twaugh@redhat.com> 0.7.20-1
- 0.7.20.

* Fri Jun 30 2006 Tim Waugh <twaugh@redhat.com> 0.7.19-1
- 0.7.19.
- Remove foomatic pickle file post-install.

* Tue Jun 27 2006 Tim Waugh <twaugh@redhat.com> 0.7.18-1
- 0.7.18.
- Ship translations with libs subpackage.

* Fri Jun 23 2006 Tim Waugh <twaugh@redhat.com> 0.7.17-1
- 0.7.17.

* Fri Jun 23 2006 Tim Waugh <twaugh@redhat.com> 0.7.16-1
- 0.7.16, now with SMB browser.

* Thu Jun 22 2006 Tim Waugh <twaugh@redhat.com> 0.7.15-1
- 0.7.15.
- Build requires gettext-devel.
- Ship translations.

* Tue Jun 20 2006 Tim Waugh <twaugh@redhat.com> 0.7.14-1
- 0.7.14.

* Mon Jun 19 2006 Tim Waugh <twaugh@redhat.com> 0.7.13-1
- 0.7.13.

* Fri Jun  9 2006 Tim Waugh <twaugh@redhat.com> 0.7.12-1
- 0.7.12.

* Thu Jun  1 2006 Tim Waugh <twaugh@redhat.com> 0.7.11-3
- Fix libs dependency.

* Thu Jun  1 2006 Tim Waugh <twaugh@redhat.com> 0.7.11-2
- Moved the gtk_html2pango module to the libs package (needed by
  foomatic.py).

* Wed May 31 2006 Tim Waugh <twaugh@redhat.com> 0.7.11-1
- Split out system-config-printer-libs.
- Updated to system-config-printer-0.7.11.

* Sat May 27 2006 Tim Waugh <twaugh@redhat.com> 0.7.10-2
- Requires gobject2 (bug #192764).

* Fri May 26 2006 Tim Waugh <twaugh@redhat.com> 0.7.10-1
- Require foomatic (bug #192764).
- Updated to system-config-printer-0.7.10.

* Thu May 25 2006 Tim Waugh <twaugh@redhat.com> 0.7.9-1
- Updated to pycups-1.9.11.
- Updated to system-config-printer-0.7.9.

* Mon May 15 2006 Tim Waugh <twaugh@redhat.com> 0.7.8-1
- Updated to pycups-1.9.10.
- Updated to system-config-printer-0.7.8.

* Fri May  5 2006 Tim Waugh <twaugh@redhat.com>
- Fix pycups segfault.

* Fri May  5 2006 Tim Waugh <twaugh@redhat.com> 0.7.7-2
- Ship PAM and userhelper files.
- Requires usermode.
- Added missing options.py file.
- Fix getClasses() in pycups.

* Thu May  4 2006 Tim Waugh <twaugh@redhat.com> 0.7.7-1
- Updated to system-config-printer-0.7.7.
- Updated to pycups-1.9.9.
- Desktop file.
- Requires PyXML.

* Fri Apr 28 2006 Tim Waugh <twaugh@redhat.com>
- Make it actually run.

* Fri Apr 21 2006 Tim Waugh <twaugh@redhat.com>
- Build requires CUPS 1.2.

* Thu Apr 20 2006 Tim Waugh <twaugh@redhat.com> 0.7.5-1
- Updated to pycups-1.9.8.  No longer need threads patch.
- Updated to system-config-printer-0.7.5.

* Sat Apr 15 2006 Tim Waugh <twaugh@redhat.com>
- Updated to pycups-1.9.7.

* Thu Apr 13 2006 Tim Waugh <twaugh@redhat.com> 0.7.4-2
- Obsoletes: system-config-printer-gui <= 0.6.152

* Wed Apr 12 2006 Tim Waugh <twaugh@redhat.com> 0.7.4-1
- Updated to system-config-printer-0.7.4.

* Fri Apr  7 2006 Tim Waugh <twaugh@redhat.com> 0.7.3-1
- Added threads patch from pycups CVS.
- Updated to system-config-printer-0.7.3.

* Tue Apr  4 2006 Tim Waugh <twaugh@redhat.com>
- Updated to pycups-1.9.6.

* Fri Mar 24 2006 Tim Waugh <twaugh@redhat.com>
- Updated to pycups-1.9.5.

* Fri Mar 17 2006 Tim Waugh <twaugh@redhat.com>
- Package the actual system-config-printer command.

* Thu Mar 16 2006 Tim Waugh <twaugh@redhat.com> 0.7.1-1
- Include s-c-printer tarball.
- Updated to pycups-1.9.4.

* Wed Mar 15 2006 Tim Waugh <twaugh@redhat.com> 0.7.0-1
- Initial spec file.
