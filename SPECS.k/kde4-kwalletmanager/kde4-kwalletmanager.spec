#define svn_number rc1
%define real_name kwalletmanager

%define kde4_enable_final_bool ON

Name: kde4-%{real_name}
Summary: Manage KDE passwords 
Summary(zh_CN.UTF-8): 管理 KDE4 的密码
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Version: 4.13.1
Release: 1%{?dist}
License: LGPL
URL: http://extragear.kde.org/apps/kipi
Source0: http://mirrors.ustc.edu.cn/kde/stable/%{version}/src/%{real_name}-%{version}.tar.xz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: gettext
BuildRequires: cmake >= 2.6.2
BuildRequires: gettext
BuildRequires: libkdelibs4-devel >= 4.0.82

Requires: kdebase4-runtime-kwalletd >= %{version}

Obsoletes: kde4-kwallet < 4.13.0
Provides: kde4-kwallet = %{version}

%description
KDE Wallet Manager is a tool to manage the passwords on your KDE system.

%description -l zh_CN.UTF-8
管理 KDE4 的密码。

%prep
%setup -q -n %{real_name}-%{version}

%build
mkdir build
cd build
%cmake_kde4 ..

make %{?_smp_mflags}

%install
cd build
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

magic_rpm_clean.sh

%clean_kde4_desktop_files

%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING
%{kde4_bindir}/*
%{kde4_plugindir}/*
%{kde4_appsdir}/*
%{kde4_xdgappsdir}/*.desktop
%{kde4_servicesdir}/*
%{kde4_htmldir}/en/*
%{kde4_iconsdir}/*
%{_sysconfdir}/dbus-1/system.d/org.kde.kcontrol.kcmkwallet.conf
%{kde4_datadir}/dbus-1/system-services/org.kde.kcontrol.kcmkwallet.service
%{kde4_datadir}/polkit-1/actions/org.kde.kcontrol.kcmkwallet.policy

%changelog
* Tue Jun 03 2014 Liu Di <liudidi@gmail.com> - 4.13.1-1
- 更新到 4.13.1

* Sun Apr 27 2014 Liu Di <liudidi@gmail.com> - 4.13.0-5
- 为 Magic 3.0 重建

* Sun Apr 27 2014 Liu Di <liudidi@gmail.com> - 4.13.0-4
- 为 Magic 3.0 重建

* Sun Apr 27 2014 Liu Di <liudidi@gmail.com> - 4.13.0-3
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 4.9.3-2
- 为 Magic 3.0 重建

* Tue Aug 11 2009 Ni Hui <shuizhuyuanluo@126.com> - 3.2.3-1mgc
- 更新至 3.2.3
- 拆出开发包
- 己丑  六月廿一
