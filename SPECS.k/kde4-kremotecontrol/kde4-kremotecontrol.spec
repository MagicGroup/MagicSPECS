#define svn_number rc1
%define real_name kremotecontrol

%define kde4_enable_final_bool ON

Name: kde4-%{real_name}
Summary: KDE frontend for your remote controls
Summary(zh_CN.UTF-8): 遥控器的 KDE4 前端
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Version: 4.13.2
Release: 1%{?dist}
License: LGPL
URL: http://extragear.kde.org/apps/kipi
Source0: http://mirrors.ustc.edu.cn/kde/stable/%{version}/src/%{real_name}-%{version}.tar.xz

## upstreamable patches
# lib namelink_skip
Patch50: kremotecontrol-4.7.90-namelink_skip.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: gettext
BuildRequires: cmake >= 2.6.2
BuildRequires: gettext
BuildRequires: libkdelibs4-devel >= 4.0.82

%description
KRemoteControl (formerly known as KDELirc) is a KDE frontend for your
remote controls. It allows to configure actions for button presses on
remotes. All types of remotes supported by the Solid module in the KDE
platform are also supported by KRemoteControl (e.g. with the Linux
Infrared Remote Control system (LIRC) as backend).
 

%description -l zh_CN.UTF-8
可以设置遥控器的按键的工具。

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
%package devel
Summary: Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发文件
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}

%description devel
Contains the development files.

%description devel -l zh_CN.UTF-8
%{name} 的开发文件。包含 libbtcore 的开发文件。

%prep
%setup -q -n %{real_name}-%{version}

%patch50 -p1 -b .namelink_skip

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
%{kde4_libdir}/*.so.*
%{kde4_plugindir}/*
%{kde4_appsdir}/*
%{kde4_xdgappsdir}/*.desktop
%{kde4_htmldir}/en/*
%{kde4_iconsdir}/*
%{kde4_servicesdir}/*
%{kde4_servicetypesdir}/*

%changelog
* Thu Jun 19 2014 Liu Di <liudidi@gmail.com> - 4.13.2-1
- 更新到 4.13.2

* Sun Jun 01 2014 Liu Di <liudidi@gmail.com> - 4.13.1-1
- 更新到 4.13.1

* Sat Apr 26 2014 Liu Di <liudidi@gmail.com> - 4.13.0-2
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 4.9.3-2
- 为 Magic 3.0 重建

* Tue Aug 11 2009 Ni Hui <shuizhuyuanluo@126.com> - 3.2.3-1mgc
- 更新至 3.2.3
- 拆出开发包
- 己丑  六月廿一
