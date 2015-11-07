Summary: Additional GNOME icons
Summary(zh_CN.UTF-8): 额外的 GNOME 图标
Name: gnome-icon-theme-extras
Version:	3.12.0
Release: 3%{?dist}
#VCS: git:git://git.gnome.org/gnome-icon-theme-extras
%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
Source0: http://download.gnome.org/sources/gnome-icon-theme-extras/%{majorver}/%{name}-%{version}.tar.xz
License: CC-BY-SA
BuildArch: noarch
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
BuildRequires: icon-naming-utils >= 0.8.7
Requires: gnome-icon-theme

%description
This package contains extra device and mime-type icons for use by
the GNOME desktop.

%description -l zh_CN.UTF-8
额外的 GNOME 图标，包括附加设备和 MIME 类型图标。

%prep
%setup -q

%build
%configure

%install
make install DESTDIR=$RPM_BUILD_ROOT
magic_rpm_clean.sh

%post
touch --no-create %{_datadir}/icons/gnome &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/gnome &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/gnome &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/gnome &>/dev/null || :

%files
%doc COPYING AUTHORS
%{_datadir}/icons/gnome/*


%changelog
* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 3.12.0-3
- 为 Magic 3.0 重建

* Wed Apr 09 2014 Liu Di <liudidi@gmail.com> - 3.12.0-2
- 更新到 3.12.0

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Nov 14 2012 Kalev Lember <kalevlember@gmail.com> - 3.6.2-1
- Update to 3.6.2

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Mar 28 2012 Richard Hughes <hughsient@gmail.com> - 3.4.0-1
- Update to 3.4.0

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat May 07 2011 Christopher Aillon <caillon@redhat.com> - 3.0.0-2
- Update icon cache scriptlet

* Tue Apr  5 2011 Christopher Aillon <caillon@redhat.com> 3.0.0-1
- Update to 3.0.0

* Tue Feb 22 2011 Matthias Clasen <mclasen@redhat.com> - 2.90.7-1
- Update to 2.90.7

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.30.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri May 28 2010 Bastien Nocera <bnocera@redhat.com> 2.30.1-2
- Add iPad icons

* Tue Apr 20 2010 Bastien Nocera <bnocera@redhat.com> 2.30.1-1
- Update to 2.30.1

* Tue Apr  6 2010 Matthias Clasen <mclasen@redhat.com> 2.30.0-1
- Update to 2.30.0

* Thu Apr 01 2010 Bastien Nocera <bnocera@redhat.com> 2.29.0-4
- Fix license tag

* Thu Mar 25 2010 Bastien Nocera <bnocera@redhat.com> 2.29.0-3
- Update tarball

* Tue Mar 23 2010 Bastien Nocera <bnocera@redhat.com> 2.29.0-2
- Fix scriptlets

* Tue Mar 23 2010 Bastien Nocera <bnocera@redhat.com> 2.29.0-1
- First build

