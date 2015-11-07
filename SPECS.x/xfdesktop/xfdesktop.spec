
Name:           xfdesktop
Version:	4.12.3
Release:        7%{?dist}
Summary:        Desktop manager for the Xfce Desktop Environment
Summary(zh_CN.UTF-8): Xfce 桌面环境的桌面管理器

Group:          User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
License:        GPLv2+
URL:            http://www.xfce.org/
#VCS: git:git://git.xfce.org/xfce/xfdesktop
%global xfceversion %(echo %{version} | awk -F. '{print $1"."$2}')
Source0:        http://archive.xfce.org/src/xfce/%{name}/%{xfceversion}/%{name}-%{version}.tar.bz2
# Fix desktop file
Patch1:         xfdesktop-4.9.2-fix-desktop.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libxfce4ui-devel >= %{xfceversion}
BuildRequires:  gettext
BuildRequires:  exo-devel >= 0.7.0
BuildRequires:  libgudev1-devel >= 145
BuildRequires:  Thunar-devel >= 1.2.0
BuildRequires:  dbus-glib-devel >= 0.84
BuildRequires:  garcon-devel >= 0.1.2
BuildRequires:  libwnck-devel >= 2.30
BuildRequires:  libnotify-devel >= 0.4.0
BuildRequires:  xfconf-devel >= 4.10
BuildRequires:  intltool
BuildRequires:  desktop-file-utils
BuildRequires:  libSM-devel
BuildRequires:  libICE-devel
Requires:       xfwm4 >= %{xfceversion}
Requires:       xfce4-panel >= %{xfceversion}
Requires:       magic-menus

%description
This package includes a desktop manager for the Xfce Desktop Environment.

%description -l zh_CN.UTF-8
Xfce 桌面环境的桌面管理器。

%prep
%setup -q

%patch1 -p1 -b .fix

%build
%configure

make %{?_smp_mflags} V=1

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p'

find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

desktop-file-validate \
    $RPM_BUILD_ROOT/%{_datadir}/applications/xfce-backdrop-settings.desktop
magic_rpm_clean.sh
%find_lang %{name}


%clean
rm -rf $RPM_BUILD_ROOT


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
%doc README TODO ChangeLog NEWS COPYING AUTHORS
%{_bindir}/*
%{_datadir}/applications/*
%{_datadir}/icons/hicolor/*/*/*
%{_datadir}/pixmaps/*
%{_datadir}/backgrounds/xfce
%{_mandir}/man1/*


%changelog
* Fri Nov 06 2015 Liu Di <liudidi@gmail.com> - 4.12.3-7
- 为 Magic 3.0 重建

* Sat Oct 24 2015 Liu Di <liudidi@gmail.com> - 4.12.3-6
- 为 Magic 3.0 重建

* Fri Oct 23 2015 Liu Di <liudidi@gmail.com> - 4.12.3-5
- 更新到 4.12.3

* Tue Jun 10 2014 Liu Di <liudidi@gmail.com> - 4.11.6-4
- 更新到 4.11.6

* Sat Oct 06 2012 Christoph Wickert <cwickert@fedoraproject.org> - 4.10.0-4
- Search new background location in list (bugzilla.xfce.org #8799)

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat May 19 2012 Kevin Fenzi <kevin@scrye.com> - 4.10.0-2
- Drop requirement for xfce4-doc which no longer exists. 

* Sun Apr 29 2012 Christoph Wickert <cwickert@fedoraproject.org> - 4.10.0-1
- Update to 4.10.0 final
- Remove obsolete BuildRequirements
- Make build verbose
- Add VCS key

* Sat Apr 14 2012 Kevin Fenzi <kevin@scrye.com> - 4.9.3-1
- Update to 4.9.3 (Xfce 4.10pre2)

* Tue Apr 03 2012 Kevin Fenzi <kevin@scrye.com> - 4.9.2-1
- Update to 4.9.2

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Sep 13 2011 Christoph Wickert <cwickert@fedoraproject.org> - 4.8.3-1
- Update to 4.8.3

* Thu May 19 2011 Orion Poplawski <orion@cora.nwra.com> - 4.8.2-2
- Drop BR on libxfce4menu-devel

* Fri Apr 22 2011 Kevin Fenzi <kevin@scrye.com> - 4.8.2-1
- Update to 4.8.2

* Tue Feb 08 2011 Kevin Fenzi <kevin@tummy.com> - 4.8.1-3
- Fix requires and rebuild. 

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 30 2011 Kevin Fenzi <kevin@tummy.com> - 4.8.1-1
- Update to 4.8.1

* Sun Jan 16 2011 Kevin Fenzi <kevin@tummy.com> - 4.8.0-1
- Update to 4.8.0

* Sun Jan 02 2011 Christoph Wickert <cwickert@fedoraproject.org> - 4.7.5-1
- Update to 4.7.5

* Sun Dec 05 2010 Christoph Wickert <cwickert@fedoraproject.org> - 4.7.4-1
- Update to 4.7.4
- Drop libnotify fix (upstreamed)

* Sat Dec 04 2010 Christoph Wickert <cwickert@fedoraproject.org> - 4.7.3-1
- Update to 4.7.3
- Fix for libnotify 0.7.0 (bugzilla.xfce.org #6915)

* Sat Nov 13 2010 Christoph Wickert <cwickert@fedoraproject.org> - 4.7.2-1
- Update to 4.7.2

* Wed Sep 29 2010 Jesse Keating <jkeating@fedpraproject.org> - 4.6.2-3
- Rebuilt for gcc bug 634757

* Sun Sep 19 2010 Christoph Wickert <cwickert@fedoraproject.org> - 4.6.2-2
- Fix backdrop-image.patch for F14 artwork (#635399)

* Fri May 21 2010 Kevin Fenzi <kevin@tummy.com> - 4.6.2-1
- Update to 4.6.2

* Sat Apr 17 2010 Christoph Wickert <cwickert@fedoraproject.org> - 4.6.1-6
- Adjustments for recent Goddard artwork changes

* Sun Feb 14 2010 Kevin Fenzi <kevin@tummy.com> - 4.6.1-5
- Add patch for DSO linking. Fixes bug #564826

* Sun Dec 20 2009 Christoph Wickert <cwickert@fedoraproject.org> - 4.6.1-4
- Menu fixes

* Sun Nov 01 2009 Christoph Wickert <cwickert@fedoraproject.org> - 4.6.1-3
- Fix dependency for default background image

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Apr 19 2009 Kevin Fenzi <kevin@tummy.com> - 4.6.1-1
- Update to 4.6.1

* Mon Apr 13 2009 Christoph Wickert <cwickert@fedoraproject.org> - 4.6.0-4
- Exclude gnome-default-applications from menu to avoid duplicates (#488558)

* Mon Mar 02 2009 Christoph Wickert <cwickert@fedoraproject.org> - 4.6.0-3
- Fix directory ownership problems
- Require xfce4-doc and redhat-menus
- Tweak and clean up Xfce menu

* Fri Feb 27 2009 Kevin Fenzi <kevin@tummy.com> - 4.6.0-2
- Add libSM-devel to BuildRequires

* Thu Feb 26 2009 Kevin Fenzi <kevin@tummy.com> - 4.6.0-1
- Update to 4.6.0
- Remove unneeded BuildRequires

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.5.99.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jan 26 2009 Kevin Fenzi <kevin@tummy.com> - 4.5.99.1-1
- Update to 4.5.99.1

* Tue Jan 13 2009 Kevin Fenzi <kevin@tummy.com> - 4.5.93-1
- Update to 4.5.93

* Sun Dec 28 2008 Kevin Fenzi <kevin@tummy.com> - 4.5.92-1
- Update 4.5.92

* Sun Aug 31 2008 Christoph Wickert <fedora@christoph-wickert.de> - 4.4.2-6
- Update xdg-userdir-compat.patch to use upstream's variable names

* Wed Aug 27 2008 Christoph Wickert <fedora@christoph-wickert.de> - 4.4.2-5
- Use Fedora icon for desktop menu plugin (#445986)
- Respect xdg user directory paths (#457740)
- Fix menu icons
- Fix CRITICAL register message on startup
- Fix for x86_64
- Simplify g_list_free code

* Mon Aug 11 2008 Kevin Fenzi <kevin@tummy.com> - 4.4.2-4
- Add partial memory leak patch (partially fixes #428662)

* Tue Feb 19 2008 Kevin Fenzi <kevin@tummy.com> - 4.4.2-3
- Rebuild for gcc43
- Add patch for gcc43

* Mon Dec 17 2007 Kevin Fenzi <kevin@tummy.com> - 4.4.2-2
- Apply patch to show default backdrop

* Sun Nov 18 2007 Kevin Fenzi <kevin@tummy.com> - 4.4.2-1
- Update to 4.4.2

* Mon Aug 27 2007 Kevin Fenzi <kevin@tummy.com> - 4.4.1-3
- Update License tag
- Update patch to have correct desktop image filename

* Tue Jul  9 2007 Kevin Fenzi <kevin@tummy.com> - 4.4.1-2
- Add patch to fix menu lockups with new gtk2

* Wed Apr 11 2007 Kevin Fenzi <kevin@tummy.com> - 4.4.1-1
- Update to 4.4.1

* Tue Apr  3 2007 Kevin Fenzi <kevin@tummy.com> - 4.4.0-2
- Own %%{_libdir}/xfce4/modules/
- Own %%{_datadir}/xfce4-menueditor/

* Sun Jan 21 2007 Kevin Fenzi <kevin@tummy.com> - 4.4.0-1
- Update to 4.4.0

* Fri Nov 10 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.99.2-1
- Update to 4.3.99.2

* Thu Oct  5 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.99.1-5
- Fix defattr
- Add period to the end of description
- Add gtk-update-icon-cache

* Wed Oct  4 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.99.1-4
- Bump release for devel checkin

* Sun Sep 17 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.99.1-3
- Don't own datadir/xfce4/panel-plugins as thats owned by xfce4-panel

* Sat Sep  9 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.99.1-2
- Add exo, dbus-glib and Thunar-devel BuildRequires

* Sun Sep  3 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.99.1-1
- Update to 4.3.99.1

* Wed Jul 12 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.90.2
- Update to 4.3.90.2

* Mon May  8 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.90.1
- Update to 4.3.90.1

* Mon Nov  7 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.3-1.fc5
- Update to 4.2.3
- Added dist tag

* Tue May 17 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.2-1.fc4
- Update to 4.2.2

* Fri Mar 25 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.1-3.fc4
- lowercase Release

* Wed Mar 23 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.1-2.FC4
- Removed unneeded a/la files
- Rediffed xfdesktop-image patch against current version and applied

* Tue Mar 15 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.1-1
- Updated to 4.2.1 version

* Thu Jan 27 2005 Than Ngo <than@redhat.com> 4.2.0-1
- 4.2.0

* Wed Sep 01 2004 Than Ngo <than@redhat.com> 4.0.6-2
- get rid useless static library #131485

* Tue Jul 20 2004 Than Ngo <than@redhat.com> 4.0.6-1
- update to 4.0.6
- fix bug #122743, #124951, #125058

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Apr 20 2004 Than Ngo <than@redhat.com> 4.0.5-2
- Change defaults for fedora, thanks to Olivier Fourdan <fourdan@xfce.org>

* Thu Apr 15 2004 Than Ngo <than@redhat.com> 4.0.5-1
- update to 4.0.5

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jan 27 2004 Than Ngo <than@redhat.com> 4.0.3-2
- fixed dependant libraries check on x86_64

* Wed Jan 14 2004 Than Ngo <than@redhat.com> 4.0.3-1
- 4.0.3 release

* Thu Dec 25 2003 Than Ngo <than@redhat.com> 4.0.2-1
- 4.0.2 release

* Tue Dec 16 2003 Than Ngo <than@redhat.com> 4.0.1-1
- initial build
