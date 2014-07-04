# Review:       https://bugzilla.redhat.com/487973

Name:           lxmenu-data
Version:        0.1.1
Release:        7%{?dist}
Summary:        Data files for the LXDE menu
Summary(zh_CN.UTF-8): LXDE 菜单的数据文件
Group:          User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
License:        LGPLv2+
URL:            http://lxde.org
Source0:        http://downloads.sourceforge.net/lxde/%{name}-%{version}.tar.gz
Source1:        lxmenu-data-0.1-COPYING
Patch0:         lxmenu-data-0.1.1-menu.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  intltool >= 0.40.0
Requires:       magic-menus
BuildArch:      noarch

%description
The lxmenu-data contains files used to build the menu in LXDE according to 
the freedesktop-org menu spec. Currently it's used by LXPanel and LXLauncher.

%description -l zh_CN.UTF-8
LXDE 菜单的数据文件，LXPanel 和 LXLauncher 需要它。

%prep
%setup -q
%patch0 -p1 -b .orig
# install correct license
rm -f COPYING
cp %{SOURCE1} COPYING


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
#FIXME: add changelog when there is one
%doc AUTHORS COPYING README TODO
%config(noreplace) %{_sysconfdir}/xdg/menus/lxde-applications.menu
%{_datadir}/desktop-directories/lxde-*.directory


%changelog
* Fri Jul 04 2014 Liu Di <liudidi@gmail.com> - 0.1.1-7
- 为 Magic 3.0 重建

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Dec 06 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.1.1-3
- Move Accessibility to Utilities

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 06 2009 Christoph Wickert <cwickert@fedoraproject.org> 0.1.1-1
- Update to 0.1.1

* Sun Mar 22 2009 Christoph Wickert <cwickert@fedoraproject.org> 0.1-2
- Change menu structure to vendor default
- Fix license

* Fri Dec 12 2008 Christoph Wickert <cwickert@fedoraproject.org> 0.1-1
- Initial Fedora package
