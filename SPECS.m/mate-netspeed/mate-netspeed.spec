Name:           mate-netspeed
Version: 1.11.0
Release: 2%{?dist}
Summary:        MATE netspeed
Summary(zh_CN.UTF-8): MATE 网络速度
License:        GPLv2+
URL:            http://www.mate-desktop.org
%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
Source0:        http://pub.mate-desktop.org/releases/%{majorver}/%{name}-%{version}.tar.xz

BuildRequires:  mate-common
BuildRequires:  libgtop2-devel
BuildRequires:  mate-panel-devel
BuildRequires:  gtk2-devel
BuildRequires:  mate-desktop-devel


%description
MATE netspeed is an applet that shows how much 
traffic occurs on a specified network device. 

%description -l zh_CN.UTF-8
这是一个显示网络流量的小部件。

%prep
%setup -q

%build
%configure                    \
   --disable-static           \
   --disable-schemas-compile  

make %{?_smp_mflags} V=1

%install
%{make_install}

find %{buildroot} -name '*.la' -exec rm -rf {} ';'
find %{buildroot} -name '*.a' -exec rm -rf {} ';'
magic_rpm_clean.sh
%find_lang %{name} --with-gnome --all-name

%post
/sbin/ldconfig
/bin/touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :

%postun
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
    /bin/touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :

fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
/usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :


%files -f %{name}.lang
%doc AUTHORS COPYING README
%{_libexecdir}/mate-netspeed-applet
%{_datadir}/dbus-1/services/org.mate.panel.applet.NetspeedAppletFactory.service
%{_datadir}/glib-2.0/schemas/org.mate.panel.applet.netspeed.gschema.xml
%{_datadir}/icons/hicolor/*x*/apps/*.png
%{_datadir}/icons/hicolor/*x*/devices/*.png
%{_datadir}/help/*/mate_netspeed_applet
%{_datadir}/icons/hicolor/*x*/status/*.png
%{_datadir}/icons/hicolor/scalable/apps/mate-netspeed-applet.svg
%{_datadir}/mate-panel/applets/org.mate.panel.NetspeedApplet.mate-panel-applet
%{_datadir}/mate-panel/ui/netspeed-menu.xml


%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 1.11.0-2
- 更新到 1.11.0

* Mon Aug 11 2014 Liu Di <liudidi@gmail.com> - 1.9.0-2
- 为 Magic 3.0 重建

* Sat Jul 30 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.0-1
- update to 1.9.0 release

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr 30 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.8.0-2
- rebuild for libgtop2 soname bump

* Wed Mar 05 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 1.8.0-1
- Update to 1.8.0

* Wed Feb 19 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.90-1
- update to 1.7.90
- use modern 'make install' macro
- add --with-gnome --all-name for find language
- remove obsolete --disable-scrollkeeper configure flag
- remove runtime requires mate-panel, already called as BR

* Sun Feb 09 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.0-1
- Update to 1.7.0

* Tue Dec 31 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-1
- update to 1.6.1 release

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Apr 03 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.0-1
- Update to latest 1.6.0 stable release.

* Mon Mar 25 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.2-1
- Update to latest upstream release

* Thu Mar 07 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.1-2
- Fix performance issues

* Sat Feb 23 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.1-1
- Update to latest upstream release

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Dec 01 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.0-1
- Initial build
