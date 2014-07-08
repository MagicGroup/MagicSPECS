# Review: https://bugzilla.redhat.com/show_bug.cgi?id=219930

Name:           lxpanel
Version:        0.6.1
Release:        3%{?dist}
Summary:        A lightweight X11 desktop panel

Group:          User Interface/Desktops
License:        GPLv2+
URL:            http://lxde.org/
#VCS: git:git://lxde.git.sourceforge.net/gitroot/lxde/lxpanel
Source0:        http://downloads.sourceforge.net/sourceforge/lxde/%{name}-%{version}.tar.gz

# Fedora bug: https://bugzilla.redhat.com/show_bug.cgi?id=746063
Patch0:         lxpanel-0.5.6-Fix-pager-scroll.patch

## distro specific patches
# default configuration
Patch100:       lxpanel-0.5.9-default.patch
# use nm-connection-editor to edit network connections
Patch101:       lxpanel-0.3.8.1-nm-connection-editor.patch
# use zenity instead of xmessage to display low battery warning
Patch102:       lxpanel-0.5.12-battery-plugin-use-zenity.patch


BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

#BuildRequires:  docbook-utils
BuildRequires:  gettext
BuildRequires:  gtk2-devel 
BuildRequires:  intltool
BuildRequires:  pkgconfig(xpm)
BuildRequires:  pkgconfig(libstartup-notification-1.0)
# required for alsa mixer plugin
BuildRequires:  pkgconfig(alsa)
# required for netstatus plugin
BuildRequires:  wireless-tools-devel
BuildRequires:  pkgconfig(libmenu-cache) >= 0.3.0
BuildRequires:  pkgconfig(libwnck-1.0)
# required for the battery plugin with Patch102
Requires:       zenity


%description
lxpanel is a lightweight X11 desktop panel. It works with any ICCCM / NETWM 
compliant window manager (eg sawfish, metacity, xfwm4, kwin) and features a 
tasklist, pager, launchbar, clock, menu and sytray.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       gtk2-devel 
Requires:       libXpm-devel

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q
%patch0 -p1 -b .revert

%patch100 -p1 -b .default
%patch101 -p1 -b .system-config-network
%patch102 -p1 -b .zenity

# Fedora >= 19 doesn't use vendor prefixes for desktop files. Instead of
# maintaining two patches we just strip the prefixes from the files we just
# patched with patch 100.
%if (0%{?fedora} && 0%{?fedora} >= 19) || (0%{?rhel} && 0%{?rhel} >= 7)
sed -i 's|id=fedora-|id=|' data/default/panels/panel.in \
    data/two_panels/panels/bottom.in \
    data/two_panels/panels/top.in
%endif


%build
%configure
make %{?_smp_mflags} V=1


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING README
%{_bindir}/lxpanel*
%{_datadir}/lxpanel/
%{_libdir}/lxpanel/
%{_mandir}/man1/lxpanel*

%files devel
%defattr(-,root,root,-)
%{_includedir}/lxpanel/
%{_libdir}/pkgconfig/lxpanel.pc

%changelog
* Fri Nov 29 2013 Christoph Wickert <cwickert@fedoraproject.org> - 0.6.1-3
- Rebuild against menu-cache 0.5.x (#1035902)

* Tue Nov 26 2013  Christoph Wickert <cwickert@fedoraproject.org> - 0.6.1-2
- Fix conditional to actually apply the fix for the quicklauncher (#1035004)

* Mon Nov 11 2013 Christoph Wickert <cwickert@fedoraproject.org> - 0.6.1-1
- Update to 0.6.1
- Fix some changelog dates

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Aug 03 2013 Christoph Wickert <cwickert@fedoraproject.org> - 0.5.12-3
- Use zenity instead of xmessage to display low battery warnings

* Sun May 12 2013 Christoph Wickert <cwickert@fedoraproject.org> - 0.5.12-2
- Another patch for to fix the "flash_window_timeout" crash (#587430)
- Make sure launchers in default config work on Fedora >= 19

* Tue Feb 12 2013 Christoph Wickert <cwickert@fedoraproject.org> - 0.5.12-1
- Update to 0.5.12, should finally fix #587430 (fingers crossed)

* Sun Nov 25 2012 Christoph Wickert <cwickert@fedoraproject.org> - 0.5.10-3
- Fix annoying crash of the taskbar (#587430)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Christoph Wickert <cwickert@fedoraproject.org> - 0.5.10-1
- Update to 0.5.10

* Sun Jun 10 2012 Christoph Wickert <cwickert@fedoraproject.org> - 0.5.9-1
- Update to 0.5.9 (#827779)
- Fix the netstat plugin (#750400)
- Correctly show 'Application launch bar' settings window (#830198)
- Reverse scrolling direction in workspace switcher (#746063)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Oct 09 2011 Christoph Wickert <cwickert@fedoraproject.org> - 0.5.8-1
- Update to 0.5.8
- Drop upstreamed fix-build-issue... patch

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 23 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.5.6-1
- Update to 0.5.6 (fixes at least #600763 and #607129, possibly more) 
- Remove all patches from GIT

* Sat Mar 20 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.5.5-3
- Fix two race conditions (#554174 and #575053)
- Hide empty menus
- Lots of fixes
- Update translations from Transifex

* Sat Feb 27 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.5.5-2
- Rebuild for menu-cache 0.3.2 soname bump
- Add some more menu code changes from git
- New 'lxpanelctl config' command

* Sun Feb 21 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.5.5-1
- Update to 0.5.5 and rebuild against menu-cache 0.3.1
- Drop upstreamed patches
- Add patch to fix DSO linking (#564746)

* Sun Jan 31 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.5.4.1-2
- Fix windows Raise/Focus problem
- Make autohidden panels blink when there is a popup from a systray icon
- Remove debugging output

* Wed Dec 16 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.5.4.1-1
- Update to 0.5.4.1
- Remove upstreamed patches

* Fri Dec 11 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.5.4-1
- Update to 0.5.4
- Restore toggle functionality of the show deskop plugin

* Thu Aug 06 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.5.3-1
- Update to 0.5.3, fixes vertical panel size (#515748)

* Thu Aug 06 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.5.2-1
- Update to 0.5.2

* Sun Aug 02 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.5.1-1
- Update to 0.5.1
- Remove cpu-history.patch and manpages.patch, fixed upstream

- Thu Jul 27 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.5.0-1
- Update to 0.5.0

* Sat Jul 25 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.4.1-2
- Patch to fix CPU usage monitor history
- Make netstatus plugin prefer nm-connetction-editor over system-config-network
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue May 05 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.4.1-1
- Update to 0.4.1

* Fri Apr 24 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.4.0-1
- Update to 0.4.0 final (fixes #496833)

* Sun Mar 22 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.3.999-1
- Update to 0.4.0 Beta 2
- Build alsa mixer plugin
- BR wireless-tools-devel

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.8.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 01 2008 Christoph Wickert <cwickert@fedoraproject.org> 0.3.8.1-3
- Add battery callback patch
- Add gnome-run icon and update default patch

* Thu Aug 28 2008 Sebastian Vahl <fedora@deadbabylon.de> 0.3.8.1-2
- re-create patches for rpmbuild's fuzz=0

* Tue Jul 08 2008 Sebastian Vahl <fedora@deadbabylon.de> 0.3.8.1-1
- new upstream version: 0.3.8.1

* Fri Jul 04 2008 Sebastian Vahl <fedora@deadbabylon.de> 0.3.8-1
- new upstream version: 0.3.8
- new BR in this version: intltool

* Sun Jun 15 2008 Sebastian Vahl <fedora@deadbabylon.de> 0.3.7-1
- new upstream version: 0.3.7

* Mon May 05 2008 Sebastian Vahl <fedora@deadbabylon.de> 0.3.5.4-1
- new upstream version: 0.3.5.4
- update lxpanel-default.patch

* Mon Mar 31 2008 Sebastian Vahl <fedora@deadbabylon.de> - 0.2.9.0-1
- new upstream version: 0.2.9.0

* Wed Mar 26 2008 Sebastian Vahl <fedora@deadbabylon.de> - 0.2.8-2
- BR: docbook-utils

* Thu Mar 20 2008 Sebastian Vahl <fedora@deadbabylon.de> - 0.2.8-1
- new upstream version: 0.2.8
- add lxpanel-0.2.8-manpage.patch

* Thu Mar 13 2008 Sebastian Vahl <fedora@deadbabylon.de> - 0.2.7.2-1
- new upstream version: 0.2.7.2
- update lxpanel-default.patch

* Mon Feb 25 2008 Sebastian Vahl <fedora@deadbabylon.de> - 0.2.6-1
- new upstream version: 0.2.6
- update lxpanel-default.patch

* Sat Feb 09 2008 Sebastian Vahl <fedora@deadbabylon.de> - 0.2.4-6
- rebuild for new gcc-4.3

* Thu Aug 16 2007 Sebastian Vahl <fedora@deadbabylon.de> - 0.2.4-5
- Change License to GPLv2+

* Mon Jan 08 2007 Sebastian Vahl <fedora@deadbabylon.de> - 0.2.4-4
- Fixed some minor issues from the review process (#219930)

* Sun Dec 17 2006 Sebastian Vahl <fedora@deadbabylon.de> - 0.2.4-3
- BR: startup-notification-devel
- Added Patch1 from Chung-Yen to fix wrong starters in default config
- Removed pcmanfm.desktop from the default config for the moment

* Fri Dec 01 2006 Sebastian Vahl <fedora@deadbabylon.de> - 0.2.4-2
- BR: gettext

* Wed Nov 29 2006 Sebastian Vahl <fedora@deadbabylon.de> - 0.2.4-1
- New upstream version: 0.2.4

* Sun Nov 05 2006 Sebastian Vahl <fedora@deadbabylon.de> - 0.2.2-1
- New upstream version: 0.2.1

* Fri Nov 03 2006 Sebastian Vahl <fedora@deadbabylon.de> - 0.2.0-1
- New upstream version: 0.2.0

* Wed Oct 25 2006 Sebastian Vahl <fedora@deadbabylon.de> - 0.1.1-2
- Rebuild for FC6

* Thu Oct 14 2006 Sebastian Vahl <fedora@deadbabylon.de> - 0.1.1-1
- Initial Release
