%global xfceversion 4.10

Name:           xfce4-power-manager
Version:	1.5.2
Release: 4%{?dist}
Summary:        Power management for the Xfce desktop environment
Summary(zh_CN.UTF-8): Xfce 桌面环境的电源管理程序

Group:          User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
License:        GPLv2+
URL:            http://goodies.xfce.org/projects/applications/%{name}
#VCS: git:git://git.xfce.org/xfce/xfce4-power-manager
%define minorversion %(echo %{version} | awk -F. '{print $1"."$2}')
Source0:        http://archive.xfce.org/src/apps/%{name}/%{minorversion}/%{name}-%{version}.tar.bz2
# Fix XFCE category
Patch1:	        xfce4-power-manager-1.1.0-fix-desktop.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  pkgconfig(libxfconf-0) >= 4.6.0
BuildRequires:  pkgconfig(libxfce4ui-1) >= 4.7.0
BuildRequires:  pkgconfig(libxfce4panel-1.0) >= 4.6.0
BuildRequires:  pkgconfig(dbus-1) >= 0.60
BuildRequires:  pkgconfig(dbus-glib-1) >= 0.70
BuildRequires:  pkgconfig(libnotify) >= 0.4.1
BuildRequires:  pkgconfig(xrandr) >= 1.2.0
BuildRequires:  xorg-x11-proto-devel >= 1.0.0
BuildRequires:  gettext
BuildRequires:  intltool
BuildRequires:  desktop-file-utils
Requires:       xfce4-panel >= %{xfceversion}
Requires:       polkit

%description
Xfce Power Manager uses the information and facilities provided by HAL to 
display icons and handle user callbacks in an interactive Xfce session.
Xfce Power Preferences allows authorised users to set policy and change 
preferences.

%description -l zh_CN.UTF-8
Xfce 桌面环境的电源管理程序。

%prep
%setup -q
%patch1 -p1

%build
%configure
make %{?_smp_mflags} V=1

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p'
magic_rpm_clean.sh
%find_lang %{name}
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/%{name}-settings.desktop      


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
%doc AUTHORS COPYING ChangeLog NEWS README TODO
%{_bindir}/%{name}
%{_bindir}/%{name}-settings
%{_sbindir}/xfpm-power-backlight-helper
%{_sbindir}/xfce4-pm-helper
%config %{_sysconfdir}/xdg/autostart/%{name}.desktop
%{_datadir}/appdata/xfce4-power-manager.appdata.xml
%{_datadir}/applications/%{name}-settings.desktop
%{_datadir}/icons/hicolor/*/*/*.*
%{_datadir}/polkit-1/actions/org.xfce.power.policy
%{_mandir}/man1/%{name}-settings.1.*
%{_mandir}/man1/%{name}.1.*


%changelog
* Fri Nov 06 2015 Liu Di <liudidi@gmail.com> - 1.5.2-4
- 为 Magic 3.0 重建

* Sat Oct 24 2015 Liu Di <liudidi@gmail.com> - 1.5.2-3
- 为 Magic 3.0 重建

* Fri Oct 23 2015 Liu Di <liudidi@gmail.com> - 1.5.2-2
- 更新到 1.5.2

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Apr 29 2012 Christoph Wickert <cwickert@fedoraproject.org> - 1.2.0-1
- Update to 1.2.0 (Xfce 4.10 final)

* Sat Apr 14 2012 Kevin Fenzi <kevin@scrye.com> - 1.1.0-1
- Update to 1.1.0 (Xfce 4.10pre2)

* Tue Apr 03 2012 Kevin Fenzi <kevin@scrye.com> - 1.0.11-1
- Update to 1.0.11

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 10 2011 Christoph Wickert <cwickert@fedoraproject.org> - 1.0.10-2
- Fix crash in brightness management (#736727 and #736964)
- Fix expanding of battery icon after resume (#765726)
- No longer depend on xfce4-doc (#721291)
- Include various patches from GIT
- Update translations from transifex

* Sun Feb 20 2011 Christoph Wickert <cwickert@fedoraproject.org> - 1.0.10-1
- Update to 1.0.10

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 04 2011 Christoph Wickert <cwickert@fedoraproject.org> - 1.0.3-1
- Update to 1.0.3
- No longer require hal because the brightness backend was removed
- Require polkit

* Sun Dec 19 2010 Christoph Wickert <cwickert@fedoraproject.org> - 1.0.2-1
- Update to 1.0.2

* Thu Dec 16 2010 Christoph Wickert <cwickert@fedoraproject.org> - 1-0.1-1
- Update to 1.0.1 on Xfce 4.8 pre2

* Sat Nov 06 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.8.5-1
- Update to 0.8.5
- Fix for libnotify 0.7.0
- Make build verbose

* Sat Nov 21 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.8.4.2-1
- Update to 0.8.4.2

* Mon Nov 02 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.8.4.1-1
- Update to 0.8.4.1

* Tue Sep 29 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.8.4-1
- Update to 0.8.4
- Drop xfpm_session_set_client_id patch, fixed upstream

* Wed Sep 09 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.8.3.1-2
- Fix segfault in xfpm_session_set_client_id

* Sun Aug 09 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.8.3.1-1
- Update to 0.8.3.1

* Sat Aug 01 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.8.3-1
- Update to 0.8.3

* Thu Jul 30 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.8.2-3
- Patch to include dpmsconst.h instead of dpms.h

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 09 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.8.2-1
- Update to 0.8.2

* Mon Jul 06 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.8.1.1-1
- Update to 0.8.1.1

* Fri Jul 03 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.8.1-1
- Update to 0.8.1
- Drop libglade2 requirement

* Wed Jun 10 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.8.0-1
- Update to 0.8.0 final
- Update gtk-icon-cache scriptlets

* Wed May 20 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.8.0-0.3.RC2
- Update to 0.8.0RC2

* Tue Apr 28 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.8.0-0.3.RC1
- Update to 0.8.0RC1

* Mon Apr 13 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.8.0-0.2.beta2
- Update to 0.8.0beta2
- Drop xfpm-button-hal.patch, no longer necessary

* Mon Apr 13 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.8.0-0.2.beta1
- Add xfpm-button-hal.patch by Mike Massonnet

* Sun Apr 12 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.8.0-0.1.beta1
- Update to 0.8.0beta1

* Thu Apr 09 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.8.0-0.1.alpha2
- Update to 0.8.0alpha2

* Thu Apr 02 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.8.0-0.1.alpha
- Update to 0.8.0alpha 

* Tue Mar 24 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.6.5-1
- Update to 0.6.5
- Remove custom autostart file

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 19 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.6.2-1
- Update to 0.6.2

* Sat Feb  7 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.6.1-1
- Update to 0.6.1
- Include additional desktop file for autostarting the app

* Mon Nov 10 2008 Christoph Wickert <cwickert@fedoraproject.org> - 0.6.0-0.1.RC1
- Update to 0.6.0 RC1

* Fri Oct 31 2008 Christoph Wickert <cwickert@fedoraproject.org> - 0.6.0-0.1.0.beta1
- Initial Fedora package
