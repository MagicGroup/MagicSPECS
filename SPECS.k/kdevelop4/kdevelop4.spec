%define real_name kdevelop

%define kdevplatform_home %{kde4_libdir}/cmake/kdevplatform

Name: kdevelop4
Summary: KDevelop IDE
License: LGPL v2 or later
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
URL: http://www.kde.org/
Version: 4.7.2
Release: 2%{?dist}
Source0: http://mirror.bjtu.edu.cn/kde/stable/kdevelop/%{version}/src/%{real_name}-%{version}.tar.xz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: libkdelibs4-devel >= 4.1.60
BuildRequires: gettext
BuildRequires: boost-devel
BuildRequires: subversion-devel
BuildRequires: kdevplatform-devel >= 1.1.0

%description
KDevelop IDE.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- 开发包
%package -n %{name}-devel
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Summary: KDevelop IDE: Build Environment
Requires: libkdelibs4-devel
Requires: %{name} = %{version}

%description -n %{name}-devel
This package contains all necessary include files and libraries needed
to develop KDevelop IDE.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

%prep
%setup -q -n %{real_name}-%{version}

%build
mkdir build
cd build
%cmake_kde4 \
    -DKDevPlatform_DIR=%kdevplatform_home \
    ..

make %{?_smp_mflags}

%install
cd build
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

magic_rpm_clean.sh

%clean_kde4_desktop_files
%clean_kde4_notifyrc_files
%adapt_kde4_notifyrc_files


rm -f %{buildroot}%{kde4_appsdir}/kdevappwizard/templates/qmake_qt4guiapp.tar.bz2

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files
%defattr(-,root,root)
%doc COPYING.*
%{kde4_bindir}/*
%{kde4_plugindir}/*.so
%{kde4_libdir}/*.so
%{kde4_appsdir}/*
%{kde4_datadir}/mime/packages/kdevelop.xml
%config %{kde4_configdir}/kdeveloprc
%{kde4_iconsdir}/*
%{kde4_xdgappsdir}/*.desktop
%{kde4_servicesdir}/*
%{kde4_localedir}/*
%{kde4_configdir}/*

%files -n %{name}-devel
%defattr(-,root,root)
%{kde4_includedir}/*
%{kde4_htmldir}/en/kdevelop/*

%changelog
* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 4.7.2-2
- 更新到 4.7.2

* Fri Jun 06 2014 Liu Di <liudidi@gmail.com> - 4.6.0-1
- 更新到 4.6.0

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 4.2.3-1.1
- 为 Magic 3.0 重建

* Fri Aug 21 2009 Ni Hui <shuizhuyuanluo@126.com> - 3.9.95-1mgc
- 更新至 3.9.95
- 己丑  七月初二

* Tue Jun 30 2009 Ni Hui <shuizhuyuanluo@126.com> - 3.9.94-1mgc
- 更新至 3.9.94
- 己丑  闰五月初八

* Fri May 29 2009 Ni Hui <shuizhuyuanluo@126.com> - 3.9.93-1mgc
- 更新至 3.9.93
- 己丑  五月初六

* Sat Apr 4 2009 Ni Hui <shuizhuyuanluo@126.com> - 3.9.91-1mgc
- 更新至 3.9.91
- 己丑  三月初九  [清明]

* Thu Jan 15 2009 Ni Hui <shuizhuyuanluo@126.com> - 3.9.85-0.1mgc
- 首次生成 rpm 包
- 戊子  十二月二十
