%global xfceversion 4.8

Name:           xfce4-mixer
Version:        4.8.0
Release:        4%{?dist}
Summary:        Volume control plugin for the Xfce 4 panel

Group:          User Interface/Desktops
License:        GPLv2+
URL:            http://www.xfce.org/
Source0:        http://archive.xfce.org/src/apps/%{name}/%{xfceversion}/%{name}-%{version}.tar.bz2
Patch0:         xfce4-mixer-4.6.1-xfce4-panel-4.7.7.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libxfce4util-devel >= %{xfceversion}
BuildRequires:  libxfce4ui-devel >= %{xfceversion}
BuildRequires:  xfce4-panel-devel >= %{xfceversion}
BuildRequires:  xfconf-devel
BuildRequires:  libxml2-devel >= 2.4.0
BuildRequires:  startup-notification-devel
BuildRequires:  alsa-lib-devel
BuildRequires:  gstreamer-devel
BuildRequires:  gstreamer-plugins-base-devel
BuildRequires:  gettext intltool
BuildRequires:  desktop-file-utils
Requires:       xfce4-panel >= %{xfceversion}

%description
The Xfce mixer is a volume control application for the Xfce Desktop Environment.
It provides both a volume control plugin for the Xfce Panel and a standalone 
mixer application.


%prep
%setup -q
%patch0 -p1 -b .xfce4-panel-4.7.7.patch


%build
%configure --with-sound=alsa
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
%find_lang %{name}

desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop


%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc README TODO ChangeLog COPYING AUTHORS NEWS
%{_bindir}/xfce4-mixer
%{_datadir}/applications/xfce4-mixer.desktop
%{_libexecdir}/xfce4/panel-plugins/xfce4-mixer-plugin
%{_datadir}/pixmaps/xfce4-mixer/
%{_datadir}/xfce4-mixer/
%{_datadir}/xfce4/panel/plugins/*.desktop

%changelog
* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 4.8.0-4
- 为 Magic 3.0 重建

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Oct 10 2011 Christoph Wickert <cwickert@fedoraproject.org> - 4.8.0-2
- Own %%{_datadir}/xfce4-mixer/
- Remove useless gtk-icon-cache scriptlets

* Fri Feb 25 2011 Christoph Wickert <cwickert@fedoraproject.org> - 4.8.0-1
- Update to 4.8.0

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.6.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 02 2011 Christoph Wickert <cwickert@fedoraproject.org> - 4.6.1-4
- Patch for xfce4-panel >= 4.7.7

* Mon Dec 06 2010 Christoph Wickert <cwickert@fedoraproject.org> - 4.6.1-3
- Rebuild for Xfce 4.8 pre2
- Update gtk-icon-cache scriptlets

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Apr 19 2009 Kevin Fenzi <kevin@tummy.com> - 4.6.1-1
- Update to 4.6.1

* Thu Feb 26 2009 Kevin Fenzi <kevin@tummy.com> - 4.6.0-1
- Update to 4.6.0

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.5.99.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jan 26 2009 Kevin Fenzi <kevin@tummy.com> - 4.5.99.1-1
- Update to 4.5.99.1

* Tue Jan 13 2009 Kevin Fenzi <kevin@tummy.com> - 4.5.93-1
- Update to 4.5.93

* Sat Dec 27 2008 Kevin Fenzi <kevin@tummy.com> - 4.5.92-1
- Update to 4.5.92

* Sat Nov 15 2008 Christoph Wickert <cwickert@fedoraproject.org> - 4.4.3-2
- Fix desktop file (bugzilla.xfce.org #4538)

* Mon Oct 27 2008 Christoph Wickert <cwickert@fedoraproject.org> - 4.4.3-1
- Update to 4.4.3
- Update gtk-update-icon-cache scriptlets
- Add xfce4-mixer menu entry in the Xfce menu

* Sun Feb 10 2008 Kevin Fenzi <kevin@tummy.com> - 4.4.2-2
- Rebuild for gcc43

* Sun Nov 18 2007 Kevin Fenzi <kevin@tummy.com> - 4.4.2-1
- Update to 4.4.2

* Mon Aug 27 2007 Kevin Fenzi <kevin@tummy.com> - 4.4.1-3
- Updated License tag

* Wed May 30 2007 Kevin Fenzi <kevin@tummy.com> - 4.4.1-2
- Build with ALSA instead of OSS (fixes bug #239513)

* Wed Apr 11 2007 Kevin Fenzi <kevin@tummy.com> - 4.4.1-1
- Update to 4.4.1

* Tue Apr  3 2007 Kevin Fenzi <kevin@tummy.com> - 4.4.0-2
- Do not own the %%{_libdir}/xfce4/mcs-plugins directory. 

* Sun Jan 21 2007 Kevin Fenzi <kevin@tummy.com> - 4.4.0-1
- Update to 4.4.0

* Fri Nov 10 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.99.2-1
- Update to 4.3.99.2

* Thu Oct  5 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.99.1-3
- Fix defattr
- Add period to the end of description
- Add gtk-update-icon-cache

* Wed Oct  4 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.99.1-2
- Bump release for devel checkin

* Sun Sep  3 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.99.1-1
- Upgrade to 4.3.99.1
- Fix macros in changelog

* Wed Jul 12 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.90.2-1
- Upgrade to 4.3.90.2

* Thu Apr 27 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.90.1-1
- Upgrade to 4.3.90.1

* Thu Feb 16 2006 Kevin Fenzi <kevin@tummy.com> - 4.2.3-2.fc5
- Rebuild for fc5

* Mon Nov  7 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.3-1.fc5
- Update to 4.2.3
- Added dist tag

* Tue May 17 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.2-1.fc4
- Update to 4.2.2

* Sun May  8 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.1-5.fc4
- Fix libxml2 buildrequires to be libxml2-devel

* Fri Mar 25 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.1-4.fc4
- lowercase Release

* Fri Mar 25 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.1-3.FC4
- Removed unneeded la files

* Sun Mar 20 2005 Warren Togami <wtogami@redhat.com> - 4.2.1-2
- fix BuildReqs

* Tue Mar 15 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.1-1
- Updated to 4.2.1 version

* Tue Mar  8 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.0-2
- Fixed to use %%find_lang
- Removed generic INSTALL from %%doc

* Sun Mar  6 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.0-1
- Inital Fedora Extras version
