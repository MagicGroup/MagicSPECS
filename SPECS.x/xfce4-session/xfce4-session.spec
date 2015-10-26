%global xfceversion 4.10

Name:           xfce4-session
Version:	4.12.1
Release: 3%{?dist}
Summary:        Xfce session manager
Summary(zh_CN.UTF-8): Xfce 会话管理器

Group:          User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
License:        GPLv2+
URL:            http://www.xfce.org/
#VCS git:git://git.xfce.org/xfce/xfce4-session
%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
Source0:        http://archive.xfce.org/src/xfce/%{name}/%{majorver}/%{name}-%{version}.tar.bz2
# taken from polkit-gnome, license is LGPLv2+, requires because of
# http://lists.fedoraproject.org/pipermail/devel-announce/2011-February/000758.html
Source1:        polkit-gnome-authentication-agent-1.desktop

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  dbus-devel >= 1.1.0
BuildRequires:  dbus-glib-devel >= 0.84
BuildRequires:  glib2-devel >= 2.24.0
BuildRequires:  libSM-devel
BuildRequires:  libwnck-devel >= 2.30
BuildRequires:  libxfce4ui-devel >= %{xfceversion}
BuildRequires:  startup-notification-devel
BuildRequires:  xfce4-panel-devel >= %{xfceversion}
BuildRequires:  xfconf-devel >= %{xfceversion}
BuildRequires:  xorg-x11-server-utils
# GNOME compatibility
BuildRequires:  GConf2-devel
BuildRequires:  gnome-keyring-devel
# Build tools
BuildRequires:  desktop-file-utils
BuildRequires:  gettext 
BuildRequires:  intltool
BuildRequires:  libxslt
BuildRequires:  gnome-doc-utils
#BuildRequires:  libxml2
BuildRequires:  xfce4-dev-tools
Requires:       xorg-x11-server-utils
Requires:       polkit-gnome

Obsoletes:      xfce-utils < 4.8.3-7.fc18

%description
xfce4-session is the session manager for the Xfce desktop environment.

%description -l zh_CN.UTF-8
Xfce 会话管理器。

%package        devel
Summary:        Development files for xfce4-session
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name} = %{version}-%{release}
Requires:       libxfce4ui-devel >= %{xfceversion}

%description    devel
Header files for the Xfce Session Manager.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package        engines
Summary:        Additional engines for xfce4-session
Summary(zh_CN.UTF-8): %{name} 的附加引擎
Group:          User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Requires:       %{name} = %{version}-%{release}

%description    engines
Additional splash screen engines for the Xfce Session Manager.

%description engines -l zh_CN.UTF-8
%{name} 的附加引擎。

%prep
%setup -q

%build
%configure --disable-static \
    --enable-gnome \
    --enable-libgnome-keyring \
    --enable-session-screenshots \
    --enable-panel-plugin 
    
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags} V=1


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p'
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
magic_rpm_clean.sh
%find_lang %{name}

# install autostart file for polkit-gnome-authentication-agent-1
desktop-file-install --vendor="xfce" \
	--add-category="X-XFCE;" \
	--dir=$RPM_BUILD_ROOT%{_sysconfdir}/xdg/autostart/ \
	%{SOURCE1}


%clean
rm -rf $RPM_BUILD_ROOT


%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
/sbin/ldconfig


%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
/sbin/ldconfig


%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS BUGS COPYING ChangeLog NEWS README TODO
%doc doc/FAQ doc/NEWS.pre-4.3 doc/README.Kiosk
%{_sysconfdir}/xdg/xfce4
%{_sysconfdir}/xdg/autostart/xscreensaver.desktop
%config(noreplace) %{_sysconfdir}/xdg/autostart/xfce-polkit-gnome-authentication-agent-1.desktop
%{_bindir}/*
%{_libdir}/lib*.so.*
%dir %{_libdir}/xfce4/session/
%dir %{_libdir}/xfce4/session/splash-engines
%{_libdir}/xfce4/session/splash-engines/libmice.so
%{_libdir}/xfce4/session/xfsm-shutdown-helper
%{_datadir}/applications/*.desktop
%{_datadir}/xsessions/xfce.desktop
%{_datadir}/icons/hicolor/*/*/*
%{_datadir}/polkit-1/actions/org.xfce.session.policy
%{_mandir}/man1/*

%files devel
%defattr(-,root,root,-)
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/xfce4/xfce4-session-*/

%files engines
%defattr(-,root,root,-)
%{_libdir}/xfce4/session/splash-engines/libbalou.so
%{_libdir}/xfce4/session/splash-engines/libsimple.so
%{_libdir}/xfce4/session/balou-*
%{_datadir}/themes/Default/balou/

%changelog
* Sat Oct 24 2015 Liu Di <liudidi@gmail.com> - 4.12.1-3
- 为 Magic 3.0 重建

* Fri Oct 23 2015 Liu Di <liudidi@gmail.com> - 4.12.1-2
- 更新到 4.12.1

* Sun Sep 30 2012 Kevin Fenzi <kevin@scrye.com> 4.10.0-4
- Add upstream commit to fix session saves with 2 or more apps that ask to save. 
- https://bugzilla.xfce.org/show_bug.cgi?id=5379

* Fri Sep 14 2012 Kevin Fenzi <kevin@scrye.com> 4.10.0-3
- Drop fortune-mod. No longer used in 4.10. Fixes bug #857404

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Apr 29 2012 Christoph Wickert <cwickert@fedoraproject.org> - 4.10.0-1
- Update to 4.10.0 final
- Make build verbose
- Add VCS key

* Fri Apr 20 2012 Kevin Fenzi <kevin@scrye.com> - 4.9.2-1
- Update to 4.9.2 

* Sat Apr 14 2012 Kevin Fenzi <kevin@scrye.com> - 4.9.1-1
- Update to 4.9.1 (Xfce 4.10pre2)

* Tue Apr 03 2012 Kevin Fenzi <kevin@scrye.com> - 4.9.0-1
- Update to 4.9.0

* Sun Feb 12 2012 Kevin Fenzi <kevin@scrye.com> - 4.8.3-1
- Update to 4.8.3 and drop upstreamed gobject link patch.

* Wed Feb 01 2012 Kevin Fenzi <kevin@scrye.com> - 4.8.2-3
- Add patch to link with gobject. 

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Sep 13 2011 Christoph Wickert <cwickert@fedoraproject.org> - 4.8.2-1
- Update to 4.8.2
- Remove gdmlang.patch and hostname.patch, both upstream

* Wed Jul 27 2011 Kevin Fenzi <kevin@scrye.com> - 4.8.1-5
- Add patch for hostname issue. Fixes bug #706563

* Sat Apr 16 2011 Christoph Wickert <cwickert@fedoraproject.org> - 4.8.1-4
- Autostart polkit-gnome-authentication-agent-1 (#693152)
- Remove --enable-gen-doc configure option as it requires network access

* Thu Mar 10 2011 Kevin Fenzi <kevin@tummy.com> - 4.8.1-3
- Add patch to fix LANG handling with new gdm. Fixes #683941

* Tue Feb 15 2011 Christoph Wickert <cwickert@fedoraproject.org> - 4.8.1-2
- Fix versioning of the devel package's requirements
 
* Mon Feb 14 2011 Christoph Wickert <cwickert@fedoraproject.org> - 4.8.1-1
- Update to 4.8.1

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 16 2011 Kevin Fenzi <kevin@tummy.com> - 4.8.0-1
- Update to 4.8.0

* Sun Jan 02 2011 Christoph Wickert <cwickert@fedoraproject.org> - 4.7.3-1
- Update to 4.7.3

* Fri Dec 03 2010 Christoph Wickert <cwickert@fedoraproject.org> - 4.7.2-1
- Update to 4.7.2

* Mon Nov 08 2010 Christoph Wickert <cwickert@fedoraproject.org> - 4.7.1-1
- Update to 4.7.1

* Sun Sep 05 2010 Christoph Wickert <cwickert@fedoraproject.org> - 4.7.0-1
- Update to 4.7.0

* Fri May 21 2010 Kevin Fenzi <kevin@tummy.com> - 4.6.2-1
- Update to 4.6.2

* Thu Dec 17 2009 Christoph Wickert <cwickert@fedoraproject.org> - 4.6.1-5
- Remove libtool archives of splash engines

* Wed Nov 11 2009 Kevin Fenzi <kevin@tummy.com> - 4.6.1-4
- Don't own /usr/share/themes (fixes #534107)

* Wed Sep 09 2009 Christoph Wickert <cwickert@fedoraproject.org> - 4.6.1-3
- Fix German text in logout dialog
- Fix shadows in 'simple' splash engine
- Don't ship static lib in -devel package
- configure with --disable-static instead of removing *.a files
- Fix directory ownership issue

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Apr 19 2009 Kevin Fenzi <kevin@tummy.com> - 4.6.1-1
- Update to 4.6.1

* Thu Feb 26 2009 Kevin Fenzi <kevin@tummy.com> - 4.6.0-1
- Update to 4.6.0
- Remove some unneeded BuildRequires

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.5.99.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jan 26 2009 Kevin Fenzi <kevin@tummy.com> - 4.5.99.1-1
- Update to 4.5.99.1

* Tue Jan 13 2009 Kevin Fenzi <kevin@tummy.com> - 4.5.93-1
- Update to 4.5.93

* Fri Dec 26 2008 Kevin Fenzi <kevin@tummy.com> - 4.5.92-1
- Update 4.5.92

* Mon Aug 11 2008 Kevin Fenzi <kevin@tummy.com> - 4.4.2-4
- Fix icon for autostarted applications (fixes #442804)

* Tue Apr 22 2008 Kevin Fenzi <kevin@tummy.com> - 4.4.2-3
- Disable tips by default for now. 

* Sun Feb 10 2008 Kevin Fenzi <kevin@tummy.com> - 4.4.2-2
- Rebuild for gcc43

* Sun Nov 18 2007 Kevin Fenzi <kevin@tummy.com> - 4.4.2-1
- Update to 4.4.2

* Mon Aug 27 2007 Kevin Fenzi <kevin@tummy.com> - 4.4.1-2
- Update License tag

* Wed Apr 11 2007 Kevin Fenzi <kevin@tummy.com> - 4.4.1-1
- Update to 4.4.1
- Own the themes and themes/Default directories. 

* Tue Apr  3 2007 Kevin Fenzi <kevin@tummy.com> - 4.4.0-2
- Own some unowned directories
- Add Requires: redhat-menus for directory ownership

* Sun Jan 21 2007 Kevin Fenzi <kevin@tummy.com> - 4.4.0-1
- Update to 4.4.0

* Mon Nov 27 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.99.2-2
- Add dbus-devel and GConf2-devel to BuildRequires, fixes bug #217082

* Fri Nov 10 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.99.2-1
- Update to 4.3.99.2

* Thu Oct  5 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.99.1-6
- Fix defattr
- Add gtk-update-icon-cache

* Wed Oct  4 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.99.1-5
- Bump release for devel checkin

* Sun Sep 24 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.99.1-4
- Don't own doc directories that xfdesktop owns. 

* Sun Sep 17 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.99.1-3
- Only own icons, not any of the icon dirs. 

* Tue Sep 12 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.99.1-2
- Add Requires for fortune-mod, needed for xfce4-tips

* Sun Sep  3 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.99.1-1
- Upgrade to 4.3.99.1
- Fix macros in changelog
- Add post/postun ldconfig

* Wed Jul 12 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.90.2-1
- Upgrade to 4.3.90.2

* Thu Feb 16 2006 Kevin Fenzi <kevin@tummy.com> - 4.2.3-3.fc5
- Rebuild for fc5

* Tue Jan 31 2006 Kevin Fenzi <kevin@tummy.com> - 4.2.3-2.fc5
- Added xorg-x11-server-utils, imake, libXt-devel BuildRequires
- Added xorg-x11-server-utils to Requires

* Mon Nov  7 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.3-1.fc5
- Update to 4.2.3
- Added dist tag

* Tue May 17 2005 Kevin Fenzi <kevin@tummy.com> 4.2.2-1.fc4
- Update to 4.2.2

* Sun May  8 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.1-5.fc4
- Add xorg-x11 buildrequires for iceauth check in configure

* Fri Mar 25 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.1-4.fc4
- lowercase Release

* Wed Mar 23 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.1-3.FC4
- Removed unneeded la/a files
- Added version to requires in devel and engine subpackages

* Sun Mar 20 2005 Warren Togami <wtogami@redhat.com> - 4.2.1-2
- fix BuildReqs

* Tue Mar 15 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.1-1
- Updated to 4.2.1 version

* Tue Mar  8 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.0-2
- Fixed to use %%find_lang
- Removed generic INSTALL from %%doc

* Sun Mar  6 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.0-1
- Inital Fedora Extras version

