# Review: https://bugzilla.redhat.com/show_bug.cgi?id=442270

# Review at https://bugzilla.redhat.com/show_bug.cgi?id=540034

%global git_snapshot 1

%if 0%{?git_snapshot}
%global git_rev 87c368d79eddf272cd356837256495168c5c72a2
%global git_date 20110328
%global git_short %(echo %{git_rev} | cut -c-8)
%global git_version %{git_date}git%{git_short}
%endif

# Source0 was generated as follows: 
# git clone git://lxde.git.sourceforge.net/gitroot/lxde/%{name}
# cd %{name}
# git archive --format=tar --prefix=%{name}/ %{git_short} | bzip2 > %{name}-%{?git_version}.tar.bz2

Name:           lxde-common
Version:        0.5.5
Release:        0.6%{?git_version:.%{?git_version}}%{?dist}
Summary:        Default configuration files for LXDE

Group:          User Interface/Desktops
License:        GPLv2+
URL:            http://lxde.sourceforge.net/
%if 0%{?git_snapshot}
Source0:        %{name}-%{?git_version}.tar.bz2
%else
Source0:        http://downloads.sourceforge.net/sourceforge/lxde/%{name}-%{version}.tar.gz
%endif
Source1:        lxde-lock-screen.desktop
Source2:        lxde-desktop-preferences.desktop
# Distro specific patches
Patch10:        %{name}-0.5.5-pcmanfm-config.patch
Patch11:        %{name}-0.5.5-lxpanel-config.patch
Patch12:        %{name}-0.5.5-openbox-menu.patch
Patch13:        %{name}-0.3.2.1-logout-banner.patch
Patch15:        %{name}-0.5.5-vendor.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  desktop-file-utils
# because of some patches:
BuildRequires:  automake
Requires:       lxsession >= 0.4.0
Requires:       lxpanel pcmanfm openbox xdg-utils 
Requires:       lxmenu-data
Requires:       xorg-x11-server-utils
Requires:       xorg-x11-xinit
# needed because of new gdm
Requires:       xorg-x11-utils
# Use vendor's artwork
Requires:       system-logos
%if 0%{?fedora} < 9
Requires:       desktop-backgrounds-basic
%else
Requires:       desktop-backgrounds-compat
%endif
Obsoletes:      %{name}-data <= 0.3.2.1-5
# needed because the lxde-common and lxde-common-data 
# required each other with full n-v-r on F-11
Provides:       %{name} = 0.3.2.1-4.fc11
Provides:       %{name}-data = 0.3.2.1-4.fc11
BuildArch:      noarch

%description
This package contains the configuration files for LXDE, the Lightweight X11 
Desktop Environment.


%prep
%setup -q %{?git_version:-n %{name}}

%patch10 -p1 -b .orig
%patch11 -p1 -b .orig
%patch12 -p1 -b .orig
%patch13 -p1 -b .logout-banner
%patch15 -p1 -b .vendor

# Calling autotools must be done before executing
# configure if needed
autoreconf -fi

%build
%configure


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p'
desktop-file-install                                           \
      --remove-key=Encoding                                    \
      --dir=%{buildroot}%{_datadir}/applications               \
      lxde-logout.desktop
desktop-file-install                                           \
      --dir=%{buildroot}%{_datadir}/applications               \
      %{SOURCE1}
# cannot use desktop-file-utils because it is out of date
install -pm 0644 %{SOURCE2} %{buildroot}%{_datadir}/applications/


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING
%dir %{_sysconfdir}/xdg/lxsession/LXDE/
%config(noreplace) %{_sysconfdir}/xdg/lxsession/LXDE/autostart
%config(noreplace) %{_sysconfdir}/xdg/lxsession/LXDE/desktop.conf
%dir %{_sysconfdir}/xdg/pcmanfm/
%config(noreplace) %{_sysconfdir}/xdg/pcmanfm/LXDE/pcmanfm.conf
%{_bindir}/startlxde
%{_bindir}/lxde-logout
%{_bindir}/openbox-lxde
%{_datadir}/lxde/
%{_datadir}/lxpanel/profile/LXDE/
%{_mandir}/man1/*.1.gz
%{_datadir}/xsessions/LXDE.desktop
%{_datadir}/applications/lxde-*.desktop


%changelog
* Tue Jan 15 2013 Liu Di <liudidi@gmail.com> - 0.5.5-0.6.20110328git87c368d7
- 为 Magic 3.0 重建

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.5-0.5.20110328git87c368d7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.5-0.4.20110328git87c368d7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jul 11 2011 Christoph Wickert <cwickert@fedoraproject.org> - 0.5.5-0.3
- Drop pulseaudio patch (fixes #713292)

* Tue Apr 05 2011 Christoph Wickert <cwickert@fedoraproject.org> - 0.5.5-0.2
- Switch to Adwaita GTK theme

* Mon Mar 28 2011 Christoph Wickert <cwickert@fedoraproject.org> - 0.5.5-0.1
- Update to git snapshot to get rid of all upstreamed patches
- Fix pcmanfm config file location
- Adjust distro specific config files for F15

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Sep 19 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.5.4-3
- Fix backdrop-image.patch for F14 artwork (#635398)

* Sun Jun 13 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.5.4-2
- Adjusting autostart to respect pcmanfm 0.9.7 side rename
  (that pcmanfm2 binary was renamed to pcmanfm) (#603468)
- Explicitly call autotools before configure

* Thu Apr 29 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.5.4-1
- Bump version to 0.5.4 to indicate changes for pcmanfm2
- Adjustments for recent Goddard artwork changes

* Thu Mar 25 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.5.0-3
- Updates for pcmanfm2

* Tue Dec 15 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.5.0-2
- Restore toggle functionality of the show deskop plugin
- Drop requirement for obsolete lxde-settings-daemon

* Fri Dec 11 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.5.0-1
- Update to 0.5.0

* Tue Oct 27 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.4.2-2
- Final tweaks for the LXDE Spin

* Sat Jul 25 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.4.2-1
- Update to 0.4.2
- Disable OLPC keyboard shortcuts for now, they interfere with OpenOffice
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jun 13 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.4.1-3
- Add XO keyboard shortcuts

* Sat Jun 13 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.4.1-2
- Include logout and screenlock buttons (#503919)

* Mon May 18 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.4.1-1
- Update to 0.4.1

* Mon May 11 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.4-2
- Fix Provides to allow proper upgrade

* Tue Apr 28 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.4-1
- Update to 0.4
- Require lxmenu-data and lxde-settings-daemon
- Drop obsolete config file /etc/xdg/lxsession/LXDE/default

* Fri Mar 06 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.3.2.1-4
- Workaround for new gdm
- Add Pulseaudio support
- Add mixer plugin to the panel
- Require xdg-utils

* Fri Oct 10 2008 Christoph Wickert <cwickert@fedoraproject.org> - 0.3.2.1-3
- Require fedora-icon-theme and system-logos

* Thu Oct 09 2008 Christoph Wickert <cwickert@fedoraproject.org> - 0.3.2.1-2
- Rebase patches for rpm's new fuzz=0 behaviour

* Thu Jul 10 2008 Christoph Wickert <cwickert@fedoraproject.org> - 0.3.2.1-1
- Update to 0.3.2.1
- Switch from ROXTerm to LXterminal
- Rebased most patches
- Add mixer to the panel 

* Mon Apr 14 2008 Christoph Wickert <cwickert@fedoraproject.org> - 0.3.0.1-2
- Make a separate package for lxde-icon-theme

* Sat Apr 12 2008 Christoph Wickert <cwickert@fedoraproject.org> - 0.3.0.1-1
- Update to 0.3.0.1
- Use distros default artwork

* Sat Mar 29 2008 Christoph Wickert <cwickert@fedoraproject.org> - 0.3.0.0-1
- Initial Fedora RPM
- Use roxterm instead of gnome-terminal and xterm
- Patch default panel config
