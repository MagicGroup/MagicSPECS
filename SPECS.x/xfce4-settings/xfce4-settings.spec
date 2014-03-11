%global xfceversion 4.10

Name:           xfce4-settings
Version:        4.10.0
Release:        4%{?dist}
Summary:        Settings Manager for Xfce

Group:          User Interface/Desktops
License:        GPLv2+
URL:            http://www.xfce.org/
#VCS git:git://git.xfce.org/xfce/xfce4-settings
Source0:        http://archive.xfce.org/src/xfce/%{name}/%{xfceversion}/%{name}-%{version}.tar.bz2
# Add patch to handle position settings on multi monitor setups
# https://bugzilla.xfce.org/show_bug.cgi?id=7465
Patch0:         xfce4-settings-4.8.3-monitor-position.patch
# Fix GTK3 theme handling
# https://bugzilla.xfce.org/show_bug.cgi?id=9272
# http://git.xfce.org/xfce/xfce4-settings/commit/?id=8032dd77
Patch1:         xfce4-settings-4.10.0-gtk3-theme-detection.patch
# Prevent accidental shutdown of xfsettingsd
# https://bugzilla.xfce.org/show_bug.cgi?id=9273
# http://git.xfce.org/xfce/xfce4-settings/commit/?id=2ec63604
Patch2:         xfce4-settings-4.10.0-NameOwnerChanged.patch
## Downstream patches
# Use Fedora theme and font settings
Patch10:         xfce4-settings-4.9.4-fedora.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gettext
BuildRequires:  intltool
BuildRequires:  exo-devel >= 0.5.0
BuildRequires:  libxfce4ui-devel >= %{xfceversion}
BuildRequires:  libxfce4util-devel >= %{xfceversion}
BuildRequires:  xfconf-devel >= %{xfceversion}
BuildRequires:  libglade2-devel
BuildRequires:  libwnck-devel
BuildRequires:  desktop-file-utils >= 0.7
BuildRequires:  libnotify-devel
BuildRequires:  libcanberra-devel
BuildRequires:  libxklavier-devel
BuildRequires:  libXrandr-devel
BuildRequires:  garcon-devel >= 0.1.10
Requires:       xfconf
%if 0%{?rhel}
Requires:       gnome-icon-theme
%endif

Obsoletes:      xfce-mcs-manager < 4.4.3-2
Obsoletes:      xfce-mcs-plugins < 4.4.3-2
Obsoletes:      xfce-mcs-plugin-gsynaptics < 2.0-5
Obsoletes:      xfce-mcs-plugins-extra < 2.0-3
Obsoletes:      xfce4-gsynaptics-mcs-plugin < 1.0.0-3

%description
This package includes the settings manager applications for the Xfce desktop. 

%prep
%setup -q
%patch0 -p1 -b .multi-monitor-position
%patch1 -p1 -b .gtk3-theme
%patch2 -p1 -b .NameOwnerChanged
%patch10 -p1 -b .fedora


%build
# add --enable-maintainer-mode to regen after multi monitor setup patch.
%configure --enable-maintainer-mode --enable-sound-settings --enable-pluggable-dialogs
make %{?_smp_mflags} V=1


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} INSTALL='install -p'

for file in %{buildroot}%{_datadir}/applications/*.desktop ; do
    desktop-file-install \
        --add-category="X-XFCE" \
        --remove-category="XFCE" \
        --delete-original \
        --dir=%{buildroot}%{_datadir}/applications \
        $file
done
magic_rpm_clean.sh
        
%find_lang %{name}

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog NEWS TODO COPYING
%config(noreplace) %{_sysconfdir}/xdg/xfce4/xfconf/xfce-perchannel-xml/xsettings.xml
%config(noreplace) %{_sysconfdir}/xdg/autostart/xfsettingsd.desktop
%config(noreplace) %{_sysconfdir}/xdg/menus/xfce-settings-manager.menu
%{_bindir}/xfce4-*-settings
%{_bindir}/xfce4-settings-editor
%{_bindir}/xfce4-settings-manager
%{_bindir}/xfsettingsd
%{_datadir}/applications/xfce*.desktop
%{_libdir}/xfce4/settings

%changelog
* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 4.10.0-4
- 为 Magic 3.0 重建

* Sat Oct 06 2012 Christoph Wickert <cwickert@fedoraproject.org> - 4.10.0-3
- Add patch to prevent accidental shutdown of xfsettingsd
- Add patch to fix GTK3 theme handling

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Apr 29 2012 Christoph Wickert <cwickert@fedoraproject.org> - 4.10.0-1
- Update to 4.10.0 final
- Make build verbose
- Add VCS key

* Sat Apr 14 2012 Kevin Fenzi <kevin@scrye.com> - 4.9.5-1
- Update to 4.9.5 (Xfce 4.10pre2)

* Mon Apr 02 2012 Kevin Fenzi <kevin@scrye.com> - 4.9.4-1
- Update to 4.9.4

* Sun Feb 19 2012 Kevin Fenzi <kevin@scrye.com> - 4.8.3-4
- Add patch for keyboard default clearing. Fixes bug #753319

* Sat Jan 21 2012 Kevin Fenzi <kevin@scrye.com> - 4.8.3-3
- Add patch for multi monitor position settings. Fixes bug #773780

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Sep 23 2011 Kevin Fenzi <kevin@scrye.com> - 4.8.3-1
- Update to 4.8.3

* Thu May 19 2011 Orion Poplawski <orion@cora.nwra.com> - 4.8.2-2
- Require gnome-icon-theme on EL

* Thu May 19 2011 Christoph Wickert <wickert@kolabsys.com> - 4.8.2-1
- Update to 4.8.2
- Remove helper-crash.patch (included in this version)

* Mon May 09 2011 Kevin Fenzi <kevin@scrye.com> - 4.8.1-4
- Add patch to fix crash in helper when screenshooter isn't installed. 
- Fixes bug #701550

* Fri Apr 08 2011 Christoph Wickert <cwickert@fedoraproject.org> - 4.8.1-3
- Change default theme to Adwaita (#694889)

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 30 2011 Kevin Fenzi <kevin@tummy.com> - 4.8.1-1
- Update to 4.8.1

* Thu Jan 27 2011 Kevin Fenzi <kevin@tummy.com> - 4.8.0-2
- Add patch to fix double free. (fixes #670522)

* Sun Jan 16 2011 Kevin Fenzi <kevin@tummy.com> - 4.8.0-1
- Update to 4.8.0

* Sun Jan 02 2011 Christoph Wickert <cwickert@fedoraproject.org> - 4.7.7-1
- Update to 4.7.7

* Sun Dec 05 2010 Christoph Wickert <cwickert@fedoraproject.org> - 4.7.6-1
- Update to 4.7.6
- Drop libnotify fix (upstreamed)

* Fri Dec 03 2010 Christoph Wickert <cwickert@fedoraproject.org> - 4.7.5-1
- Update to 4.7.5

* Mon Nov 08 2010 Christoph Wickert <cwickert@fedoraproject.org> - 4.7.4-1
- Update to 4.7.4

* Fri Nov 05 2010 Kevin Fenzi <kevin@tummy.com> - 4.6.5-2
- Update for new libnotify 

* Fri May 21 2010 Kevin Fenzi <kevin@tummy.com> - 4.6.5-1
- Update to 4.6.5

* Sun Feb 14 2010 Kevin Fenzi <kevin@tummy.com> - 4.6.4-3
- Add patch to fix DSO linking. Fixes bug #564803

* Sat Jan 23 2010 Christoph Wickert <cwickert@fedoraproject.org> - 4.6.4-2
- Add patch for libxklavier 5.0. Thanks to Caolan McNamara (#558081)
- Use Clearlooks theme by default

* Sat Jan 02 2010 Christoph Wickert <cwickert@fedoraproject.org> - 4.6.4-1
- Update to 4.6.4
- Drop xi2 patch, fixed upstream

* Tue Nov 10 2009 Christoph Wickert <cwickert@fedoraproject.org> - 4.6.3-2
- Patch xfce4-mouse-settings for newer libXi (#525501)

* Tue Sep 29 2009 Christoph Wickert <cwickert@fedoraproject.org> - 4.6.3-1
- Update to 4.6.3
- Drop patches that were upstreamed

* Sat Sep 26 2009 Kevin Fenzi <kevin@tummy.com> - 4.6.1-5
- Add patch for restoring display resolution on login (bug #504908)

* Wed Sep 09 2009 Christoph Wickert <cwickert@fedoraproject.org> - 4.6.1-4
- Fix xfconf channel for keyboard repeat rate setting
- Avoid timing out xfce4-session on startup (bugzilla.xfce.org #5040)
- Make sure xfce4-settings-helper only gets started in Xfce
- Fix directory ownership issue

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 03 2009 Kevin Fenzi <kevin@tummy.com> - 4.6.1-2
- Update for new libxklavier

* Sun Apr 19 2009 Kevin Fenzi <kevin@tummy.com> - 4.6.1-1
- Update to 4.6.1

* Thu Apr 16 2009 Kevin Fenzi <kevin@tummy.com> - 4.6.0-6
- Have to add Antialias type to really enable by default. 

* Wed Apr 15 2009 Kevin Fenzi <kevin@tummy.com> - 4.6.0-5
- Bump to fix tagging mistake. 

* Wed Apr 15 2009 Kevin Fenzi <kevin@tummy.com> - 4.6.0-4
- Make Antialias default (bug #495700)

* Thu Mar 19 2009 Kevin Fenzi <kevin@tummy.com> - 4.6.0-3
- display settings fixes from upstream svn. 

* Fri Feb 27 2009 Kevin Fenzi <kevin@tummy.com> - 4.6.0-2
- Rebase patch for artwork

* Thu Feb 26 2009 Kevin Fenzi <kevin@tummy.com> - 4.6.0-1
- Update to 4.6.0

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.5.99.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Kevin Fenzi <kevin@tummy.com> - 4.5.99.1-2
- Add patch to fix imsettings (bug #478669)

* Mon Jan 26 2009 Kevin Fenzi <kevin@tummy.com> - 4.5.99.1-1
- Update to 4.5.99.1

* Thu Jan 22 2009 Christoph Wickert <cwickert@fedoraproject.org> - 4.5.93-2
- Add Obsoletes for mcs packages to make sure xfce4-settings gets installed
- Don't package desktop files twice
- Require xfconf
- Use Nodoka theme and Fedora icons
- Add docs

* Tue Jan 13 2009 Kevin Fenzi <kevin@tummy.com> - 4.5.93-1
- Update to 4.5.93

* Sat Dec 27 2008 Kevin Fenzi <kevin@tummy.com> - 4.5.92-2
- Cleaned up desktop-file-install
- Added some BuildRequires. 

* Fri Dec 26 2008 Kevin Fenzi <kevin@tummy.com> - 4.5.92-1
- Initial version for Fedora. 

