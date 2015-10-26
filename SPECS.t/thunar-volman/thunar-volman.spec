# review at https://bugzilla.redhat.com/show_bug.cgi?id=229930

%global thunarversion 1.3
%global xfceversion 4.10
%global minorversion 0.8


Name:           thunar-volman
Version:	0.8.1
Release:	3%{?dist}
Summary:        Automatic management of removable drives and media for Thunar
Summary(zh_CN.UTF-8): Thunar 的自动管理可移动磁盘和媒体的插件

Group:          User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
License:        GPLv2+
URL:            http://goodies.xfce.org/projects/thunar-plugins/%{name}
#VCS: git:git://git.xfce.org/xfce/thunar-volman
Source0:        http://archive.xfce.org/src/xfce/%{name}/%{minorversion}/%{name}-%{version}.tar.bz2
Patch1:         thunar-volman-0.7.0-desktop-fix.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  exo-devel >= 0.6.0
BuildRequires:  xfconf >= %{xfceversion}
BuildRequires:  libxfce4ui-devel >= %{xfceversion}
BuildRequires:  libgudev1-devel >= 145
BuildRequires:  libnotify-devel >= 0.4.0
BuildRequires:  gettext
BuildRequires:  intltool
BuildRequires:  desktop-file-utils
Requires:       Thunar >= %{thunarversion}

%description
The Thunar Volume Manager is an extension for the Thunar file manager, which 
enables automatic management of removable drives and media. For example, if 
thunar-volman is installed and configured properly, and you plug in your 
digital camera, it will automatically launch your preferred photo application 
and import the new pictures from the camera into your photo collection.

%description -l zh_CN.UTF-8
Thunar 的自动管理可移动磁盘和媒体的插件。

%prep
%setup -q
%patch1 -p1


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p'
magic_rpm_clean.sh
%find_lang %{name}
desktop-file-install --vendor fedora                        \
    --dir ${RPM_BUILD_ROOT}%{_datadir}/applications         \
    --add-only-show-in=XFCE                                 \
    --delete-original                                       \
    ${RPM_BUILD_ROOT}%{_datadir}/applications/%{name}-settings.desktop


%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :


%postun
if [ "$1" -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi


%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README THANKS
%{_bindir}/thunar-volman
%{_bindir}/thunar-volman-settings
%{_datadir}/icons/*/*/*/*
%{_datadir}/applications/fedora-thunar-volman-settings.desktop


%changelog
* Sat Oct 24 2015 Liu Di <liudidi@gmail.com> - 0.8.1-3
- 为 Magic 3.0 重建

* Fri Oct 23 2015 Liu Di <liudidi@gmail.com> - 0.8.1-2
- 为 Magic 3.0 重建

* Wed Sep 30 2015 Liu Di <liudidi@gmail.com> - 0.8.1-1
- 更新到 0.8.1

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Apr 29 2012 Christoph Wickert <cwickert@fedoraproject.org> - 0.8.0-1
- Update to 0.8.0 (Xfce 4.10 final)
- Add VCS key and review #

* Sat Apr 14 2012 Kevin Fenzi <kevin@scrye.com> - 0.7.1-1
- Update to 0.7.1 (Xfce 4.10pre2)

* Tue Apr 03 2012 Kevin Fenzi <kevin@scrye.com> - 0.7.0-1
- Update to 0.7.0

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 16 2011 Kevin Fenzi <kevin@tummy.com> - 0.6.0-1
- Update to 0.6.0 (for Thunar 1.2.0 on Xfce 4.8 final)

* Sun Dec 05 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.5.3-1
- Update to 0.5.3 (for Thunar 1.1.5 on Xfce 4.8 pre2)

* Mon Nov 06 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.5.2-1
- Update to 0.5.2 (for Thunar 1.1.4 on Xfce 4.8 pre1)
- BR libgudev1-devel
- Fix for libnotify 0.7.0 (bugzilla.xfce.org #6916)

* Sat Nov 06 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.3.80-5
- Fix missing icons (#650504)

* Sun Oct 03 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.3.80-4
- Fix the parole patch (#639484)
- Update gtk-icon-cache scriptlets

* Sat Oct 02 2010 Kevin Fenzi <kevin@tummy.om> - 0.3.80-3
- Add patch to default to parole for video/audio (#639484)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.80-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Feb 28 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.3.80-1
- Update to 0.3.80
- Add Category X-XfceSettingsDialog

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.2.0-2
- Autorebuild for GCC 4.3

* Mon Dec 03 2007 Christoph Wickert <cwickert@fedoraproject.org> - 0.2.0-1
- Update to 0.2.0 and Thunar 0.9.0

* Tue Aug 21 2007 Christoph Wickert <cwickert@fedoraproject.org> - 0.1.2-2
- Rebuild for BuildID feature

* Sun Jan 21 2007 Christoph Wickert <cwickert@fedoraproject.org> - 0.1.2-1
- Update to 0.1.2.

* Wed Jan 17 2007 Christoph Wickert <cwickert@fedoraproject.org> - 0.1.0-1
- Initial packaging.
