%global xfceversion 4.8
%global xsessiondir %{_datadir}/xsessions

Name:           xfce-utils
Version:        4.8.3
Release:        6%{?dist}
Summary:        Utilities for the Xfce Desktop Environment

Group:          User Interface/Desktops
License:        GPLv2+
URL:            http://www.xfce.org/
Source0:        http://archive.xfce.org/src/xfce/%{name}/%{xfceversion}/%{name}-%{version}.tar.bz2
Patch0:         xfce-utils-4.7.3-pulseaudio.patch
Patch1:         xfce-utils-4.4.3-xfterm4-bug.patch
# modfied version of http://bugzilla.xfce.org/show_bug.cgi?id=3770
Patch2:         xfce-utils-4.7.1-test-running-screensver.patch
Patch3:         xfce-utils-4.8.0-fix-desktop-categories.patch
# Already upstream: http://git.xfce.org/xfce/xfce-utils/commit/?id=9b6d7d17b466d605e6cd3febd7291cc0f38c0336
# Prevents gnome from running the 4.6 migration on gnome login and fixes the .pl migration tool.
Patch4:         xfce-utils-4.8.3-46-migration-gnome.patch
# taken from https://bugzilla.xfce.org/show_bug.cgi?id=8154
Patch5:         xfce-utils-4.8.3-check_if_userdir_is_home.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:  libxfce4ui-devel >= %{xfceversion}
BuildRequires:  gettext
BuildRequires:  desktop-file-utils
BuildRequires:  dbus-devel 
BuildRequires:  dbus-glib-devel
BuildRequires:  perl(XML::Parser)
BuildRequires:  intltool
Requires:       xfwm4
Requires:       xfdesktop
Requires:       xfce4-doc
Requires:       xfce4-settings
Requires:       /usr/bin/id


%description
This package includes utilities for the Xfce Desktop Environment.

%package -n     xfce4-doc
Summary:        Basic documentation for the Xfce Desktop Environment
Group:          Documentation
BuildArch:      noarch

%description -n xfce4-doc
This package includes common docs for the Xfce Desktop Environment.

%prep
%setup -q
%patch0 -p1 -b .pulseaudio
%patch1 -p1 -b .xfterm4-bug
%patch2 -p1 -b .gnome-screensaver
%patch3 -p1 -b .desktop-categories
%patch4 -p1 -b .46-migration-gnome
%patch5 -p1 -b .check_if_userdir_is_home


%build
%configure --disable-static

make %{?_smp_mflags}


%install
rm -rf %{buildroot}

make install DESTDIR=%{buildroot} INSTALL='install -p'
%find_lang %{name}

desktop-file-install --vendor="" --delete-original \
	--add-category="Documentation" \
	--remove-category="X-Xfce-Toplevel" \
	--dir=%{buildroot}%{_datadir}/applications \
	%{buildroot}%{_datadir}/applications/xfce4-about.desktop

desktop-file-install --vendor="" --delete-original \
	--add-category="Documentation" \
	--remove-category="X-Xfce-Toplevel" \
	--dir=%{buildroot}%{_datadir}/applications \
	%{buildroot}%{_datadir}/applications/xfhelp4.desktop

desktop-file-validate %{buildroot}%{_datadir}/applications/xfrun4.desktop

desktop-file-validate %{buildroot}%{_sysconfdir}/xdg/autostart/xfconf-migration-4.6.desktop
    
# we need the doc package to own these 
mkdir -p %{buildroot}%{_datadir}/xfce4/doc/{ast,C,ca,da,es,fr,gl,id,it,ja,pt,tr,zh_CN}/images

# xfrun4 is part of xfce4-appfinder Fedora > 17
%if 0%{?fedora} >= 17
rm -f %{buildroot}%{_bindir}/xfrun4
%endif


%clean
rm -rf %{buildroot}


%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
	touch --no-create %{_datadir}/icons/hicolor &>/dev/null
	gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi


%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc README ChangeLog NEWS COPYING AUTHORS
%attr(0755,root,root) 
%config(noreplace) %{_sysconfdir}/xdg/xfce4/xinitrc
%config(noreplace) %{_sysconfdir}/xdg/xfce4/Xft.xrdb
%config(noreplace) %{_sysconfdir}/xdg/autostart/xfconf-migration-4.6.desktop
%{_bindir}/startxfce4
%{_bindir}/xfbrowser4
%{_bindir}/xfce4-about
%{_bindir}/xflock4
%{_bindir}/xfmountdev4

# xfrun4 is part of xfce4-appfinder Fedora > 17
%if 0%{?fedora} < 17
%{_bindir}/xfrun4
%endif

%{_bindir}/xfterm4
%{_libdir}/xfce4/xfconf-migration/
%{_datadir}/icons/hicolor/*/*/*
%{xsessiondir}/*
%{_datadir}/dbus-1/services/org.xfce.RunDialog.service
%{_datadir}/applications/*.desktop

%files -n xfce4-doc
%defattr(-,root,root,-)
%{_bindir}/xfhelp4
%dir %{_datadir}/xfce4/doc
%dir %{_datadir}/xfce4/doc/*
%dir %{_datadir}/xfce4/doc/*/images
%{_docdir}/%{name}/

%changelog
* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 4.8.3-6
- 为 Magic 3.0 重建

* Fri Jan 20 2012 Kevin Fenzi <kevin@scrye.com> 4.8.3-5
- Add fix for the migration perl script to generate correct desktop files. Fixes bug #770313

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 29 2011 Christoph Wickert <cwickert@fedoraproject.org> - 4.8.3-3
- Don't try to remove $HOME if it is an xdg-user-dir (bugzilla.xfce.org #8154)
- xfrun4 is part of xfce4-appfinder in Fedora >= 17

* Fri Dec 09 2011 Kevin Fenzi <kevin@scrye.com> - 4.8.3-2
- Stop gnome from running 4.6 migration on gnome logins. Fixes bug #760621

* Fri Sep 23 2011 Kevin Fenzi <kevin@scrye.com> - 4.8.3-1
- Update to 4.8.3

* Sat Jun 18 2011 Christoph Wickert <cwickert@fedoraproject.org> - 4.8.2-1
- Update to 4.8.2

* Thu May 19 2011 Orion Poplawski <orion@cora.nwra.com> - 4.8.1-3
- Require xfce4-settings

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 30 2011 Kevin Fenzi <kevin@tummy.com> - 4.8.1-1
- Update to 4.8.1

* Sun Jan 16 2011 Kevin Fenzi <kevin@tummy.com> - 4.8.0-1
- Update to 4.8.0

* Sun Jan 02 2011 Christoph Wickert <cwickert@fedoraproject.org> - 4.7.4-1
- Update to 4.7.4

* Sun Dec 05 2010 Christoph Wickert <cwickert@fedoraproject.org> - 4.7.3-1
- Update to 4.7.3

* Fri Dec 03 2010 Christoph Wickert <cwickert@fedoraproject.org> - 4.7.2-1
- Update to 4.7.2
- Update gtk-icon-cache scriptlets

* Sat Nov 13 2010 Christoph Wickert <cwickert@fedoraproject.org> - 4.7.1-1
- Update to 4.7.1

* Sun Sep 05 2010 Christoph Wickert <cwickert@fedoraproject.org> - 4.7.0-1
- Update to 4.7.0

* Wed Jul 07 2010 Kevin Fenzi <kevin@tummy.com> - 4.6.2-2
- Add Copying file to docs in doc subpackage.

* Fri May 21 2010 Kevin Fenzi <kevin@tummy.com> - 4.6.2-1
- Update to 4.6.2

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Apr 19 2009 Kevin Fenzi <kevin@tummy.com> - 4.6.1-1
- Update to 4.6.1

* Mon Mar 02 2009 Christoph Wickert <cwickert@fedoraproject.org> - 4.6.0-2
- Fix directory ownership problems
- Make separate xfce4-doc package

* Thu Feb 26 2009 Kevin Fenzi <kevin@tummy.com> - 4.6.0-1
- Update to 4.6.0
- Remove unneeded BuildRequires

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.5.99.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jan 26 2009 Kevin Fenzi <kevin@tummy.com> - 4.5.99.1-1
- Update to 4.5.99.1

* Tue Jan 13 2009 Kevin Fenzi <kevin@tummy.com> - 4.5.93-1
- Update to 4.5.93

* Sat Dec 27 2008 Kevin Fenzi <kevin@tummy.com> - 4.5.92-1
- Update to 4.5.92

* Mon Oct 27 2008 Christoph Wickert <cwickert@fedoraproject.org> - 4.4.3-1
- Update to 4.4.3
- Prefer gnome-screensaver over xscreensaver if installed
- Make xflock4 check for running screensaver instead of installed ones
- Rework pulseaudio patch
- Configure with --disable-static
- Run gtk-update-icon-cache in %%post and %%postun

* Sun Feb 10 2008 Kevin Fenzi <kevin@tummy.com> - 4.4.2-4
- Rebuild for gcc43

* Mon Jan 14 2008 Kevin Fenzi <kevin@tummy.com> - 4.4.2-3
- Patch correct file

* Wed Jan 02 2008 Kevin Fenzi <kevin@tummy.com> - 4.4.2-2
- Add patch to start pulseaudio if installed

* Sun Nov 18 2007 Kevin Fenzi <kevin@tummy.com> - 4.4.2-1
- Update to 4.4.2

* Mon Aug 27 2007 Kevin Fenzi <kevin@tummy.com> - 4.4.1-3
- Update License tag

* Mon Jul 30 2007 Kevin Fenzi <kevin@tummy.com> - 4.4.1-2
- Add dbus BuildRequires. Thanks to Andy Shevchenko (fixes #250067) 

* Wed Apr 11 2007 Kevin Fenzi <kevin@tummy.com> - 4.4.1-1
- Update to 4.4.1

* Tue Apr  3 2007 Kevin Fenzi <kevin@tummy.com> - 4.4.0-2
- Do not own %%{_sysconfdir}/xdg/xfce4
- Do not ship the switchdesk config

* Sun Jan 21 2007 Kevin Fenzi <kevin@tummy.com> - 4.4.0-1
- Update to 4.4.0

* Fri Nov 10 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.99.2-1
- Update to 4.3.99.2

* Thu Oct  5 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.99.1-5
- Fix defattr

* Wed Oct  4 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.99.1-4
- Bump release for devel checkin

* Sun Sep 24 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.99.1-3
- Don't own doc dirs (xfdesktop does)

* Sun Sep 17 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.99.1-2
- Don't own datadir/xfce4 (xfwm4 already does)

* Sun Sep  3 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.99.1-1
- Upgrade to 4.3.99.1

* Wed Jul 12 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.90.2-1
- Update to 4.3.90.2

* Mon May  8 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.90.1-1
- Update to 4.3.90.1

* Mon Nov  7 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.3-1.fc5
- Update to 4.2.3
- Added dist tag

* Tue May 17 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.2-1.fc4
- Update to 4.2.2

* Fri Mar 25 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.1-3.fc4
- lowercase Release

* Wed Mar 23 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.1-2.FC4
- Removed unneeded la/a files

* Tue Mar 15 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.1-1
- Updated to 4.2.1 version

* Tue Mar  8 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.0-3
- Fixed case on Xfce

* Sun Mar  6 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.0-2
- Removed old misc patch 

* Thu Jan 27 2005 Than Ngo <than@redhat.com> 4.2.0-1
- 4.2.0

* Thu Dec 02 2004 Than Ngo <than@redhat.com> 4.0.6-3
- permission fix #141597

* Mon Nov 22 2004 Than Ngo <than@redhat.com> 4.0.6-2
- add session desktop file from KDE, better translations
- improve xfterm4 #139183

* Mon Jul 19 2004 Than Ngo <than@redhat.com> 4.0.6-1
- update to 4.0.6
- use %%find_lang macros, bug #124950
- fix component deps, bug #125744
- don't run xmodmap twice, bug #115500

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Apr 15 2004 Than Ngo <than@redhat.com> 4.0.5-1
- update to 4.0.5

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jan 27 2004 Than Ngo <than@redhat.com> 4.0.3-2
- fixed dependant libraries check on x86_64

* Tue Jan 13 2004 Than Ngo <than@redhat.com> 4.0.3-1
- 4.0.3 release

* Thu Dec 25 2003 Than Ngo <than@redhat.com> 4.0.2-1
- 4.0.2 release

* Tue Dec 16 2003 Than Ngo <than@redhat.com> 4.0.1-1
- initial build

