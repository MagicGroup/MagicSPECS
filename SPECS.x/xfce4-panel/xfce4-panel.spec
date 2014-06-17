
Name:           xfce4-panel
Version:	4.11.0
Release:        3%{?dist}
Summary:        Next generation panel for Xfce
Summary(zh_CN.UTF-8): Xfce 的下一代面板

Group:          User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
License:        GPLv2+ and LGPLv2+
URL:            http://www.xfce.org/
#VCS git:git://git.xfce.org/xfce/xfce4-panel
%global xfceversion %(echo %{version} | awk -F. '{print $1"."$2}')
Source0:        http://archive.xfce.org/src/xfce/%{name}/%{xfceversion}/%{name}-%{version}.tar.bz2
# clock icon taken from system-config-date, license is GPLv2+
Source1:        xfce4-clock.png
Source2:        xfce4-clock.svg
Patch1:         xfce4-panel-4.9.1-fix-desktopfile.patch
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires:  libxfce4ui-devel >= %{xfceversion}
BuildRequires:  xfconf-devel >= 4.10
BuildRequires:  garcon-devel >= 0.1.5
BuildRequires:  libxml2-devel >= 2.4.0
BuildRequires:  startup-notification-devel
BuildRequires:  exo-devel >= 0.3.93
BuildRequires:  libwnck-devel >= 2.30
BuildRequires:  gettext
BuildRequires:  intltool
BuildRequires:  desktop-file-utils
BuildRequires:  gtk-doc

# xfce4-iconbox isn't in Xfce 4.4
Obsoletes:      xfce4-iconbox <= 4.2.3-4.fc6
# xfce4-systray isn't in Xfce 4.4
Obsoletes:      xfce4-systray <= 4.2.3-3.fc6
# xfce4-toys isn't in Xfce 4.4
Obsoletes:      xfce4-toys <= 4.2.3-3.fc6
# xfce4-trigger-launcher isn't in Xfce 4.4
Obsoletes:      xfce4-trigger-launcher <= 4.2.3-3.fc6
# xfce4-showdesktop-plugin isn't in Xfce 4.4
Obsoletes:      xfce4-showdesktop-plugin <= 0.4.0-7.fc6
# xfce4-taskbar-plugin isn't in Xfce 4.4
Obsoletes:      xfce4-taskbar-plugin <= 0.2.2-7.fc6
# xfce4-windowlist-plugin isn't in Xfce 4.4
Obsoletes:      xfce4-windowlist-plugin <= 0.1.0-7.fc6
# xfce4-xmms-plugin isn't in F11
Obsoletes:      xfce4-xmms-plugin <= 0.5.1-3.fc11
# xfce4-volstatus-icon isn't in F15
Obsoletes:      xfce4-volstatus-icon <= 0.1.0-7.fc15
# xfce4-stopwatch-plugin isn't in F15
Obsoletes:      xfce4-stopwatch-plugin <= 0.2.0-3.fc15
# xfce4-xfapplet-plugin isn't in F15
Obsoletes:      xfce4-xfapplet-plugin <= 0.1.0-10.fc15


%description
This package includes the panel for the Xfce desktop environment.

%description -l zh_CN.UTF-8
Xfce 桌面环境的面板。

%package devel
Summary:        Development headers for xfce4-panel
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig
Requires:       libxfce4util-devel >= %{xfceversion}
Requires:       libxfce4ui-devel >= %{xfceversion}

%description devel
This package includes the header files you will need to build
plugins for xfce4-panel.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q

%build
%configure --enable-gtk-doc --disable-static

# Remove rpaths
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

# The LD_LIBRARY_PATH hack is needed for --enable-gtk-doc
# because lt-libxfce4panel-scan is linked against libxfce4panel
export LD_LIBRARY_PATH=$( pwd )/libxfce4panel/.libs

make %{?_smp_mflags} V=1


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

# remove duplicate docs
rm -f $RPM_BUILD_ROOT/%{_docdir}/xfce4-panel/README.gtkrc-2.0

# FIXME: We need to own these dirs until all plugins are ported to Xfce 4.8
mkdir -p $RPM_BUILD_ROOT%{_libexecdir}/xfce4/panel-plugins
mkdir -p $RPM_BUILD_ROOT%{_libdir}/xfce4/panel-plugins
mkdir -p $RPM_BUILD_ROOT%{_datadir}/xfce4/panel-plugins
magic_rpm_clean.sh
%find_lang %{name}

desktop-file-validate $RPM_BUILD_ROOT/%{_datadir}/applications/panel-desktop-handler.desktop
desktop-file-validate $RPM_BUILD_ROOT/%{_datadir}/applications/panel-preferences.desktop

# install additional icons
install -pm 0644 %{SOURCE1} ${RPM_BUILD_ROOT}%{_datadir}/icons/hicolor/48x48/apps/
install -pm 0644 %{SOURCE2} ${RPM_BUILD_ROOT}%{_datadir}/icons/hicolor/scalable/apps/

%clean
rm -rf $RPM_BUILD_ROOT


%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

/usr/sbin/ldconfig


%postun
if [ $1 -eq 0 ] ; then
  touch --no-create %{_datadir}/icons/hicolor &>/dev/null
  gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

/usr/sbin/ldconfig


%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc COPYING AUTHORS ChangeLog NEWS README docs/README.gtkrc-2.0
%config(noreplace) %{_sysconfdir}/xdg/xfce4/panel/default.xml
%{_bindir}/*
%{_libdir}/libxfce4panel-*.so.*
%{_libdir}/xfce4/panel/
%{_datadir}/icons/hicolor/*/*/*
%{_datadir}/xfce4/panel/
%{_datadir}/applications/*.desktop
# FIXME: Remove these when no longer needed
%dir %{_libexecdir}/xfce4/panel-plugins/
%dir %{_libdir}/xfce4/panel-plugins
%dir %{_datadir}/xfce4/panel-plugins

%files devel
%defattr(-, root,root,-)
%{_libdir}/pkgconfig/*
%{_libdir}/libxfce4panel-*.so
%doc %{_datadir}/gtk-doc/html/libxfce4panel-*/
%{_includedir}/xfce4/libxfce4panel-*/

%changelog
* Wed Jun 11 2014 Liu Di <liudidi@gmail.com> - 4.11.0-3
- 更新到 4.11.0

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 4.10.0-3
- 为 Magic 3.0 重建

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Apr 29 2012 Christoph Wickert <cwickert@fedoraproject.org> - 4.10.0-1
- Update to 4.10.0 final
- Make build verbose
- Add VCS key

* Sat Apr 14 2012 Kevin Fenzi <kevin@scrye.com> - 4.9.2-1
- Update to 4.9.2 (Xfce 4.10pre2)

* Mon Apr 02 2012 Kevin Fenzi <kevin@scrye.com> - 4.9.1-1
- Update to 4.9.1

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.6-3
- Rebuilt for glibc bug#747377

* Sun Oct 23 2011 Christoph Wickert <cwickert@fedoraproject.org> - 4.8.6-2
- Fix directory menu plugin's 'Open in Terminal' option (#748226)
- No longer depend on xfce4-doc (#721288)

* Thu Sep 22 2011 Christoph Wickert <cwickert@fedoraproject.org> - 4.8.6-1
- Update to 4.8.6

* Tue Jun 21 2011 Christoph Wickert <cwickert@fedoraproject.org> - 4.8.5-1
- Update to 4.8.5

* Sun Jun 19 2011 Christoph Wickert <cwickert@fedoraproject.org> - 4.8.4-1
- Update to 4.8.4

* Sun May 08 2011 Christoph Wickert <wickert@kolabsys.com> - 4.8.3-2
- Add xfce4-clock icons for the 'Add new items' dialog (#694902)

* Wed Apr 06 2011 Christoph Wickert <cwickert@fedoraproject.org> - 4.8.3-1
- Update to 4.8.3
- Remove upstreamed add_button_release_event_to_proxy_item.patch

* Fri Mar 25 2011 Christoph Wickert <cwickert@fedoraproject.org> - 4.8.2-3
- Fix switching grouped windows in the taskbar (#680779)

* Tue Mar 08 2011 Christoph Wickert <cwickert@fedoraproject.org> - 4.8.2-2
- Include mixer in default panel config (#636227)
- Obsolete old plugins (#682491)

* Fri Feb 25 2011 Christoph Wickert <cwickert@fedoraproject.org> - 4.8.2-1
- Update to 4.8.2

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 30 2011 Kevin Fenzi <kevin@tummy.com> - 4.8.1-1
- Update to 4.8.1

* Sun Jan 16 2011 Kevin Fenzi <kevin@tummy.com> - 4.8.0-1
- Update to 4.8.0

* Sun Jan 02 2011 Christoph Wickert <cwickert@fedoraproject.org> - 4.7.7-1
- Update to 4.7.7

* Sun Dec 19 2010 Christoph Wickert <cwickert@fedoraproject.org> - 4.7.6-2
- Own %%{_libexecdir}/xfce4/panel-plugins/ for now

* Sun Dec 05 2010 Christoph Wickert <cwickert@fedoraproject.org> - 4.7.6-1
- Update to 4.7.6

* Sat Dec 04 2010 Christoph Wickert <cwickert@fedoraproject.org> - 4.7.5-1
- Update to 4.7.5

* Mon Nov 08 2010 Christoph Wickert <cwickert@fedoraproject.org> - 4.7.4-1
- Update to 4.7.4

* Sun Sep 05 2010 Christoph Wickert <cwickert@fedoraproject.org> - 4.7.3-1
- Update to 4.7.3
- Update icon-cache scriptlets

* Fri May 21 2010 Kevin Fenzi <kevin@tummy.com> - 4.6.4-1
- Update to 4.6.4

* Sat Feb 13 2010 Kevin Fenzi <kevin@tummy.com> - 4.6.3-2
- Add patch for DSO fix. Fixes bug 564694

* Wed Dec 30 2009 Christoph Wickert <cwickert@fedoraproject.org> - 4.6.3-1
- Update to 4.6.3

* Fri Oct 16 2009 Christoph Wickert <cwickert@fedoraproject.org> - 4.6.2-1
- Update to 4.6.2
- Drop explicit requires on Terminal and mousepad

* Wed Sep 30 2009 Christoph Wickert <cwickert@fedoraproject.org> - 4.6.1-4
- Add xfswitch-plugin to default panel config (#525563)

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jun 12 2009 Christoph Wickert <cwickert@fedoraproject.org> - 4.6.1-2
- Bring back the multilib patch to fix #505165

* Sun Apr 19 2009 Kevin Fenzi <kevin@tummy.com> - 4.6.1-1
- Update to 4.6.1

* Sat Feb 28 2009 Christoph Wickert <cwickert@fedoraproject.org> - 4.6.0-2
- Fix directory ownership problems
- Require xfce4-doc
- Mark gtk-doc files as %%doc
- Obsolete the xfce4-xmms-plugin

* Thu Feb 26 2009 Kevin Fenzi <kevin@tummy.com> - 4.6.0-1
- Update to 4.6.0
- Remove some unneeded BuildRequires

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
- Remove mailwatch-plugin from default panel config again
- BuildRequire intltool
- Update gtk-update-icon-cache scriptlets
- Fix BuildRoot tag

* Thu Oct 02 2008 Christoph Wickert <cwickert@fedoraproject.org> - 4.4.2-5
- Fix FTBFS (#465058)
- Update defaults patch to include mailwatch plugin
- Remove old xfce4-iconbox and xftaskbar dummy files

* Tue Apr 08 2008 Kevin Fenzi <kevin@tummy.com> - 4.4.2-4
- Add defaults patch. See bug 433573

* Sat Feb 23 2008 Kevin Fenzi <kevin@tummy.com> - 4.4.2-3
- Drop dependency on xfce-icon-theme. See bug 433152

* Sun Feb 10 2008 Kevin Fenzi <kevin@tummy.com> - 4.4.2-2
- Rebuild for gcc43

* Sun Dec  2 2007 Kevin Fenzi <kevin@tummy.com> - 4.4.2-1
- Update to 4.4.2 (fixes 382471)
- Drop Provides/Obsoletes for xfce4-modemlights-plugin to come back.

* Mon Aug 27 2007 Kevin Fenzi <kevin@tummy.com> - 4.4.1-4
- Update License tag

* Mon Jul 30 2007 Kevin Fenzi <kevin@tummy.com> - 4.4.1-3
- Own %%{_datadir}/xfce4/

* Wed Jun  6 2007 Kevin Fenzi <kevin@tummy.com> - 4.4.1-2
- Fix multilib issues. Bug #228168

* Wed Apr 11 2007 Kevin Fenzi <kevin@tummy.com> - 4.4.1-1
- Upgrade to 4.4.1

* Tue Apr  3 2007 Kevin Fenzi <kevin@tummy.com> - 4.4.0-2
- Own %%{_libexecdir}/xfce4/
- Do not own %%{_libdir}/xfce4/mcs-plugins

* Sun Jan 21 2007 Kevin Fenzi <kevin@tummy.com> - 4.4.0-1
- Upgrade to 4.4.0

* Sat Nov 11 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.99.2-2
- Require xfce4-icon-theme. 

* Thu Nov  9 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.99.2-1
- Update to 4.3.99.2

* Fri Oct  6 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.99.1-7
- List full old versions in Obsoletes

* Fri Oct  6 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.99.1-6
- Tweak Obsolete versions

* Thu Oct  5 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.99.1-5
- Add Requires libxfcegui4-devel to devel package

* Thu Oct  5 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.99.1-4
- Add period to description
- Fix defattr
- Add gtk-update-icon-cache in post/postun

* Wed Oct  4 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.99.1-3
- Add Requires for mousepad and Terminal
- Bump for devel checkin

* Sun Sep 24 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.99.1-2
- Obsolete some more plugins who's functionality has been pulled in. 
- Own the libexecdir/xfce4/panel-plugins for new plugins. 

* Sun Sep  3 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.99.1-1
- Update to 4.3.99.1
- Add Provides/Obsoletes for xfce4-iconbox, xfce4-systray, xfce4-toys, xfce4-trigger-launcher
- Fix typo in devel subpackage summary
- Add post/postun ldconfig calls

* Thu Aug 24 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.90.2-2
- fix .so in main package
- add Requires for libxfce4util-devel
- don't own includedir/xfce4 (libxfce4util-devel should)

* Tue Jul 11 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.90.2
- Upgrade to 4.3.90.2

* Thu Apr 27 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.90.1.fc6
- Upgrade to 4.3.90.1

* Thu Feb 16 2006 Kevin Fenzi <kevin@tummy.com> - 4.2.3-3.fc5
- Rebuild for fc5

* Tue Jan 31 2006 Kevin Fenzi <kevin@tummy.com> - 4.2.3-2.fc5
- added imake and libXt-devel BuildRequires for modular xorg

* Mon Nov  7 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.3-1.fc5
- Update to 4.2.3
- Added dist tag
- Tweaked panel-htmlview patch to add - in translation

* Tue May 17 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.2-1.fc4
- Update to 4.2.2

* Fri Mar 25 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.1.1-4.fc4
- lowercase Release

* Thu Mar 24 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.1.1-3.FC4
- Added htmlview patch
- Removed unneeded la/a files

* Sat Mar 19 2005 Warren Togami <wtogami@redhat.com> - 4.2.1.1-2
- remove stuff

* Thu Mar 17 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.1.1-1
- Updated to 4.2.1.1 version
- Changed Requires/Buildrequires to 4.2.1, as xfce4-panel was the only package updated to 4.2.1.1

* Tue Mar 15 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.1-1
- Updated to 4.2.1 version

* Tue Mar  8 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.0-4
- Fixed case of Xfce

* Sun Mar  6 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.0-3
- Created a new patch to change mozilla -mail to launchmail
- Moved the includes to the devel subpackage

* Thu Feb 03 2005 Than Ngo <than@redhat.com> 4.2.0-2
- new sub package xfce4-panel-devel

* Tue Jan 25 2005 Than Ngo <than@redhat.com> 4.2.0-1
- 4.2.0

* Wed Dec 08 2004 Than Ngo <than@redhat.com> 4.0.6-2 
- add patch to use lauchmail/htmlview #142160

* Mon Jul 19 2004 Than Ngo <than@redhat.com> 4.0.6-1
- update to 4.0.6
- remove some unneeded patch files

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun 01 2004 Than Ngo <than@redhat.com> 4.0.5-4
- add buildrequires on startup-notification-devel, bug #124948
- use %%find_lang macros, bug #124948

* Mon May 31 2004 Than Ngo <than@redhat.com> 4.0.5-3
- own %%{_libdir}i/xfce4, bug #124826

* Mon Apr 26 2004 Than Ngo <than@redhat.com> 4.0.5-2
- Change more defaults for fedora, use startup notification
  by default, remove "-splash" option from mozilla launcher. Thanks to Olivier Fourdan
- Patch to avoid crash at startup under some rare circumstances
- Change defaults for fedora

* Thu Apr 15 2004 Than Ngo <than@redhat.com> 4.0.5-1
- update to 4.0.5

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jan 27 2004 Than Ngo <than@redhat.com> 4.0.3-2
- fixed dependant libraries check on x86_64

* Fri Jan 09 2004 Than Ngo <than@redhat.com> 4.0.3-1
- 4.0.3 release

* Thu Dec 25 2003 Than Ngo <than@redhat.com> 4.0.2-1
- 4.0.2 release

* Tue Dec 16 2003 Than Ngo <than@redhat.com> 4.0.1-1
- initial build

