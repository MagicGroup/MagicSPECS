%define real_name kdepim-runtime

%define kde4_enable_final_bool OFF

Name: kdepim4-runtime
Summary: The KDE PIM Runtime Components
Summary(zh_CN.UTF-8): KDE 个人信息套件运行时
License: LGPL v2 or later
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
URL: http://www.kde.org/
Version: 4.13.3
Release: 1%{?dist}
Source0: http://download.kde.org/stable/%{version}/src/%{real_name}-%{version}.tar.xz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: libkdelibs4-devel
BuildRequires: libkdepimlibs4-devel
BuildRequires: boost-devel
BuildRequires: libxml2-devel
BuildRequires: akonadi-devel >= 1.1.95
BuildRequires: strigi-devel >= 0.6.3
BuildRequires: soprano-devel >= 2.2.69
BuildRequires: libkolab-devel 
BuildRequires: libkolabxml-devel

Provides: kdepim4-akonadi = %{version}-%{release}
Conflicts: kdepim4-akonadi <= 4.2.91

Patch800: kdepim-runtime-4.3.4-enablefinal.patch

# dirty hack drop mailtransport stuff
# FIXME: disabled in 4.4.7 --- nihui
Patch801: kdepim-runtime-4.4.2-drop-mailtransport.patch

%description
The KDE PIM Runtime Components.

%description -l zh_CN.UTF-8
KDE 个人信息套件运行时。

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
%package -n %{name}-devel
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Summary: The KDE PIM Runtime Components: Build Environment
Requires: libkdelibs4-devel
Requires: akonadi-devel
Requires: %{name} = %{version}

%description -n %{name}-devel
This package contains all necessary include files and libraries needed
to develop KDE PIM Components applications.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
%prep
%setup -q -n %{real_name}-%{version}

# compile fix
#%patch800 -p1

# %patch801 -p1

%build
mkdir build
cd build
%cmake_kde4 ..

make %{?_smp_mflags}

%install
cd build
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

%clean_kde4_desktop_files
magic_rpm_clean.sh

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files -n %{name}-devel
%defattr(-,root,root)
#%{kde4_includedir}/*
%{kde4_libdir}/*.so

%files
%defattr(-,root,root)
#%doc COPYING COPYING.LIB
%{kde4_bindir}/*
%{kde4_libdir}/*.so.*
%{kde4_plugindir}/*.so
%{kde4_datadir}/*
%{kde4_dbus_interfacesdir}/org.kde.Akonadi.*.Settings.xml
%{kde4_plugindir}/imports/org/kde/*

%changelog
* Fri Jul 18 2014 Liu Di <liudidi@gmail.com> - 4.13.3-1
- 更新到 4.13.3

* Thu Jun 19 2014 Liu Di <liudidi@gmail.com> - 4.13.2-1
- 更新到 4.13.2

* Fri Jun 06 2014 Liu Di <liudidi@gmail.com> - 4.13.1-1
- 更新到 4.13.1

* Thu Apr 24 2014 Liu Di <liudidi@gmail.com> - 4.13.0-11111111112
- 为 Magic 3.0 重建

* Thu Apr 24 2014 Liu Di <liudidi@gmail.com> - 4.13.0-1.1
- 为 Magic 3.0 重建

* Tue Aug 4 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.3.0-1mgc
- 更新至 4.3.0
- 己丑  六月十四

* Tue Jun 30 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.95-1mgc
- kdepim-akonadi 自 KDE 4.3 RC1 起独立
- 首次生成 rpm 包
- 己丑  闰五月初八
