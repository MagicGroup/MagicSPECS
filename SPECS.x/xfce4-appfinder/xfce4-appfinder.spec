%global xfceversion 4.10

Name:           xfce4-appfinder
Version:	4.12.0
Release: 3%{?dist}
Summary:        Appfinder for the Xfce4 Desktop Environment
Summary(zh_CN.UTF-8): Xfce4 桌面环境的程序查找器

Group:          User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
License:        GPLv2+
URL:            http://www.xfce.org/
#VCS git:git://git.xfce.org/xfce/xfce4-appfinder
%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
Source0:        http://archive.xfce.org/src/xfce/%{name}/%{majorver}/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  pkgconfig(dbus-glib-1) >= 0.84
BuildRequires:  pkgconfig(garcon-1) >= 0.1.7
BuildRequires:  pkgconfig(libxfce4ui-1) >= %{xfceversion}
BuildRequires:  pkgconfig(libxfconf-0) >= %{xfceversion}
BuildRequires:  startup-notification-devel
BuildRequires:  gettext 
BuildRequires:  intltool
BuildRequires:  desktop-file-utils


%description
xfce-appfinder shows system wide installed applications.

%description -l zh_CN.UTF-8
Xfce4 桌面环境的程序查找器。

%prep
%setup -q

%build
%configure

make %{?_smp_mflags} V=1


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} INSTALL='install -p'

desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/xfce4-run.desktop
magic_rpm_clean.sh
%find_lang %{name}


%clean
rm -rf %{buildroot}


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc README TODO ChangeLog COPYING AUTHORS
%{_bindir}/xfce4-appfinder
%{_bindir}/xfrun4
%{_datadir}/applications/xfce4-*.desktop
%{_datadir}/appdata/xfce4-appfinder.appdata.xml

%changelog
* Fri Nov 06 2015 Liu Di <liudidi@gmail.com> - 4.12.0-3
- 为 Magic 3.0 重建

* Sat Oct 24 2015 Liu Di <liudidi@gmail.com> - 4.12.0-2
- 为 Magic 3.0 重建

* Thu Oct 22 2015 Liu Di <liudidi@gmail.com> - 4.12.0-1
- 更新到 4.12.0

* Sat Oct 06 2012 Christoph Wickert <cwickert@fedoraproject.org> - 4.10.0-3
- Use full patch for bugzilla.xfce.org #9109 from upstream (#826486)

* Wed Jul 18 2012 Cristian Ciupitu <cristian.ciupitu@yahoo.com> - 4.10.0-2
- Patch for https://bugzilla.xfce.org/show_bug.cgi?id=9109

* Sun Apr 29 2012 Christoph Wickert <cwickert@fedoraproject.org> - 4.10.0-1
- Update to 4.10.0 final
- Add VCS key

* Sat Apr 14 2012 Kevin Fenzi <kevin@scrye.com> - 4.9.5-1
- Update to 4.9.5 (Xfce 4.10pre2)

* Tue Apr 03 2012 Kevin Fenzi <kevin@scrye.com> - 4.9.4-1
- Update to 4.9.4

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.9.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 29 2011 Christoph Wickert <cwickert@fedoraproject.org> - 4.9.3-1
- Update to 4.9.3
- Make build more verbose
- Switch to pkgconfig-style BuildRequires

* Fri Nov 04 2011 Christoph Wickert <cwickert@fedoraproject.org> - 4.9.2-1
- Update to 4.9.2
- Remove icon-cache scriptlets because this package no longer installs icons

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 16 2011 Kevin Fenzi <kevin@tummy.com> - 4.8.0-1
- Update to 4.8.0

* Sun Jan 02 2011 Christoph Wickert <cwickert@fedoraproject.org> - 4.7.2-1
- Update to 4.7.2

* Mon Nov 08 2010 Christoph Wickert <cwickert@fedoraproject.org> - 4.7.1-1
- Update to 4.7.1

* Sun Sep 05 2010 Christoph Wickert <cwickert@fedoraproject.org> - 4.7.0-1
- Update to 4.7.0
- Update icon-cache scriptlets

* Fri May 21 2010 Kevin Fenzi <kevin@tummy.com> - 4.6.2-1
- Update to 4.6.2

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

* Tue Dec 23 2008 Kevin Fenzi <kevin@tummy.com> - 4.5.92-1
- Update to 4.5.92

* Mon Oct 27 2008 Christoph Wickert <cwickert@fedoraproject.org> - 4.4.3-1
- Update to 4.4.3
- Update gtk-update-icon-cache scriptlets

* Sun Feb 10 2008 Kevin Fenzi <kevin@tummy.com> - 4.4.2-2
- Rebuild for gcc43

* Sun Nov 18 2007 Kevin Fenzi <kevin@tummy.com> - 4.4.2-1
- Update to 4.4.2

* Mon Aug 27 2007 Kevin Fenzi <kevin@tummy.com> - 4.4.1-2
- Update License tag

* Sun Apr 15 2007 Kevin Fenzi <kevin@tummy.com> - 4.4.1-1
- Update to 4.4.1
- Own some unowned directories

* Sun Jan 21 2007 Kevin Fenzi <kevin@tummy.com> - 4.4.0-1
- Update to 4.4.0

* Fri Nov 10 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.99.2-1
- Update to 4.3.99.2

* Thu Oct  5 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.99.1-3
- Add period to description
- Fix defattr
- Add gtk-update-icon-cache

* Wed Oct  4 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.99.1-2
- Bump release for devel checkin

* Sun Sep  3 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.99.1-1
- Upgrade to 4.3.99.1
- Remove 0 length NEWS file
- Clean up macros in changelog

* Wed Jul 12 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.90.2-1
- Upgrade to 4.3.90.2

* Thu May 18 2006 Kevin Fenzi <kevin@tummy.com> - 4.2.3-3
- Add patch to fix crash in information selection (fixes #192195)

* Thu Feb 16 2006 Kevin Fenzi <kevin@tummy.com> - 4.2.3-2.fc5
- Rebuild for fc5 

* Mon Nov  7 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.3-1.fc5
- Update to 4.2.3
- Added dist tag
- Added doc/he

* Tue May 17 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.2-1.fc4
- Update to 4.2.2
- Add doc/fr

* Fri Mar 25 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.1-3.fc4
- lowercase Release

* Sun Mar 20 2005 Warren Togami <wtogami@redhat.com> - 4.2.1-2
- fix BuildReqs

* Tue Mar 15 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.1-1
- Updated to 4.2.1 version
- Fixed %%files section to not list lang files twice

* Tue Mar  8 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.0-2
- Fixed to use %%find_lang
- Removed generic INSTALL from %%doc
- Fixed case on Xfce

* Sun Mar  6 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.0-1
- Inital Fedora Extras version
