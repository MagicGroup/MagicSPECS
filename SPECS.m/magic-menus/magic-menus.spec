%define gettext_package redhat-menus

Summary: Configuration and data files for the desktop menus
Summary(zh_CN.UTF-8): 桌面菜单的配置和数据文件
Name: magic-menus
Version: 12.0.2
Release: 9%{?dist}
URL: http://www.magiclinux.org
Source0: %{name}-%{version}.tar.xz
License: GPL+
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
BuildArch: noarch
BuildRequires: desktop-file-utils
BuildRequires: intltool

%description
This package contains the XML files that describe the menu layout for
GNOME and KDE, and the .desktop files that define the names and icons
of "subdirectories" in the menus.

%description -l zh_CN.UTF-8
桌面菜单的配置和数据文件。

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
mv $RPM_BUILD_ROOT%{_sysconfdir}/xdg/menus/applications.menu \
   $RPM_BUILD_ROOT%{_sysconfdir}/xdg/menus/magic-applications.menu

magic_rpm_clean.sh

%find_lang %{gettext_package}

# create the settings-merged to prevent gamin from looking for it
# in a loop
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/xdg/menus/settings-merged ||:



%post
update-desktop-database &> /dev/null || :

%postun
update-desktop-database &> /dev/null || :

%files  -f %{gettext_package}.lang
%defattr(-,root,root,-)
%doc COPYING
%dir %{_sysconfdir}/xdg/menus
%dir %{_sysconfdir}/xdg/menus/applications-merged
%dir %{_sysconfdir}/xdg/menus/preferences-merged
%dir %{_sysconfdir}/xdg/menus/preferences-post-merged
%dir %{_sysconfdir}/xdg/menus/settings-merged
%config %{_sysconfdir}/xdg/menus/*.menu
%exclude %{_datadir}/desktop-menu-patches/*.desktop
%{_datadir}/desktop-directories/*.directory

%changelog
* Fri Aug 08 2014 Liu Di <liudidi@gmail.com> - 12.0.2-9
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 12.0.2-7
- 为 Magic 3.0 重建

* Fri May 04 2012 Liu Di <liudidi@gmail.com> - 12.0.2-6
- 为 Magic 3.0 重建

* Sun Mar 25 2012 Liu Di <liudidi@gmail.com> - 12.0.2-5
- 为 Magic 3.0 重建


