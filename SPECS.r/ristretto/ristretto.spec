# Review at https://bugzilla.redhat.com/show_bug.cgi?id=351531

%global xfceversion 4.8.0


Name:           ristretto
Version:	0.8.0
Release:	4%{?dist}
Summary:        Image-viewer for the Xfce desktop environment
Summary(zh_CN.UTF-8): Xfce 桌面环境下的图像查看器

Group:          User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
License:        GPLv2+
URL:            http://goodies.xfce.org/projects/applications/ristretto/
%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
Source0:        http://archive.xfce.org/src/apps/%{name}/%{majorver}/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  dbus-glib-devel >= 0.34
BuildRequires:  gtk2-devel >= 2.20.0
BuildRequires:  exo-devel >= 0.4.0
BuildRequires:  libexif-devel >= 0.6.0
BuildRequires:  libxfce4ui-devel >= %{xfceversion}
BuildRequires:  xfconf-devel >= %{xfceversion}
BuildRequires:  desktop-file-utils, gettext, intltool
Requires:       tumbler


%description
Ristretto is a fast and lightweight image-viewer for the Xfce desktop 
environment.

%description -l zh_CN.UTF-8
Ristretto 是 Xfce 桌面环境下的快速轻量的图像查看器。

%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
magic_rpm_clean.sh
%find_lang %{name}
desktop-file-install --vendor magic \
        --dir %{buildroot}%{_datadir}/applications \
        --add-mime-type=image/x-bmp \
        --add-mime-type=image/x-png \
        --add-mime-type=image/x-pcx \
        --add-mime-type=image/x-tga \
        --add-mime-type=image/xpm \
        --delete-original \
        %{buildroot}%{_datadir}/applications/%{name}.desktop


%clean
rm -rf %{buildroot}


%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
update-desktop-database &> /dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
update-desktop-database &> /dev/null || :


%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog README
%{_bindir}/%{name}
%{_datadir}/applications/magic-%{name}.desktop
%{_datadir}/icons/hicolor/*/*/*
%{_datadir}/appdata/ristretto.appdata.xml

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.8.0-4
- 为 Magic 3.0 重建

* Sat Oct 24 2015 Liu Di <liudidi@gmail.com> - 0.8.0-3
- 为 Magic 3.0 重建

* Fri Oct 23 2015 Liu Di <liudidi@gmail.com> - 0.8.0-2
- 为 Magic 3.0 重建

* Sat Sep 12 2015 Liu Di <liudidi@gmail.com> - 0.8.0-1
- 更新到 0.8.0

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 0.3.4-2
- 为 Magic 3.0 重建

* Sat Jan 28 2012 Christoph Wickert <cwickert@fedoraproject.org> - 0.3.4-1
- Update to 0.3.4

* Sat Jan 14 2012 Christoph Wickert <cwickert@fedoraproject.org> - 0.3.2-1
- Update to 0.3.2

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 08 2011 Christoph Wickert <cwickert@fedoraproject.org> - 0.3.0-2
- Require tumbler for thumbnail generation

* Sun Nov 06 2011 Christoph Wickert <cwickert@fedoraproject.org> - 0.3.0-1
- Update to 0.3.0

* Sun Nov 06 2011 Christoph Wickert <cwickert@fedoraproject.org> - 0.2.3-1
- Update to 0.2.3 (fixes #750657)

* Sat Oct 29 2011 Christoph Wickert <cwickert@fedoraproject.org> - 0.2.2-1
- Update to 0.2.2

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-2
- Rebuilt for glibc bug#747377

* Sun Oct 23 2011 Christoph Wickert <cwickert@fedoraproject.org> - 0.2.1-1
- Update to 0.2.1

* Tue Oct 18 2011 Christoph Wickert <cwickert@fedoraproject.org> - 0.2.0-1
- Update to 0.2.0

* Sun Oct 09 2011 Christoph Wickert <cwickert@fedoraproject.org> - 0.1.1-1
- Update to 0.1.1
- Drop DSO patch, fixed upstream

* Thu Oct 06 2011 Christoph Wickert <cwickert@fedoraproject.org> - 0.1.0-1
- Update to 0.1.0

* Wed Aug 16 2011 Christoph Wickert <cwickert@fedoraproject.org> - 0.0.93-2
- Fix two major memory leaks (bugzilla.xfce.org #7882)

* Thu Mar 03 2011 Christoph Wickert <cwickert@fedoraproject.org> - 0.0.93-1
- Update to 0.0.93 (fixes #542141 and #679808)
- No longer require xfce4-doc
- Run update-desktop-database in %%post and %%postun

* Wed Feb 09 2011 Christoph Wickert <cwickert@fedoraproject.org> - 0.0.91-2
- BR xfconf-devel to fix build after Xfce 4.8 update

* Tue Jul 13 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.0.91-1
- Update to 0.0.91 (Development release for next major version)
- Require xfce4-doc for directory ownership of the nex docs

* Wed Feb 17 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.0.22-3
- Add patch to fix DSO linking (#565114)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri May 15 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.0.22-1
- Update to 0.0.22

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Nov 27 2008 Christoph Wickert <cwickert@fedoraproject.org> - 0.0.21-1
- Update to 0.0.21
- Remove marshaller fix, included upstream now

* Tue Jul 01 2008 Christoph Wickert <cwickert@fedoraproject.org> - 0.0.20-2
- Add patch to fix x86_64 bit bug caused by a wrong marshaller (#351531)

* Sat May 24 2008 Christoph Wickert <cwickert@fedoraproject.org> - 0.0.20-1
- Update to 0.0.20

* Sat May 10 2008 Christoph Wickert <cwickert@fedoraproject.org> - 0.0.19-1
- Update to 0.0.19

* Sat Apr 05 2008 Christoph Wickert <cwickert@fedoraproject.org> - 0.0.18-1
- Update to 0.0.18

* Wed Feb 17 2008 Christoph Wickert <cwickert@fedoraproject.org> - 0.0.17-1
- Update to 0.0.17

* Wed Jan 30 2008 Christoph Wickert <cwickert@fedoraproject.org> - 0.0.16-1
- Update to 0.0.16

* Mon Dec 03 2007 Christoph Wickert <cwickert@fedoraproject.org> - 0.0.15-1
- Update to 0.0.15

* Mon Dec 03 2007 Christoph Wickert <cwickert@fedoraproject.org> - 0.0.14-1
- Update to 0.0.14

* Mon Nov 26 2007 Christoph Wickert <cwickert@fedoraproject.org> - 0.0.13-1
- Update to 0.0.13

* Wed Nov 21 2007 Christoph Wickert <cwickert@fedoraproject.org> - 0.0.12-2
- Try manual_adjustments.patch

* Tue Nov 20 2007 Christoph Wickert <cwickert@fedoraproject.org> - 0.0.12-1
- Update to 0.0.12

* Wed Nov 07 2007 Christoph Wickert <cwickert@fedoraproject.org> - 0.0.11-1
- Update to 0.0.11
- BuildRequire dbus-glib-devel

* Sat Nov 03 2007 Christoph Wickert <cwickert@fedoraproject.org> - 0.0.10-1
- Update to 0.0.10
- Add more mimetypes: tiff, x-bmp, x-png, x-pcx, x-tga and xpm
- Correct build requirements

* Fri Oct 19 2007 Christoph Wickert <cwickert@fedoraproject.org> - 0.0.9-1
- Update to 0.0.9

* Sun Oct 14 2007 Christoph Wickert <cwickert@fedoraproject.org> - 0.0.8-1
- Update to 0.0.8

* Sun Sep 30 2007 Christoph Wickert <cwickert@fedoraproject.org> - 0.0.7-1
- Update to 0.0.7

* Sun Sep 09 2007 Christoph Wickert <cwickert@fedoraproject.org> - 0.0.4-1
- Update to 0.0.4

* Wed Sep 05 2007 Christoph Wickert <cwickert@fedoraproject.org> - 0.0.3-1
- Initial RPM package
