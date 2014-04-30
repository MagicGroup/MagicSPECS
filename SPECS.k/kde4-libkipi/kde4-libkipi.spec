%define rversion %{kde4_kdelibs_version}
#define svn_number rc1
%define real_name libkipi

%define kde4_enable_final_bool OFF

Name: kde4-%{real_name}
Summary: Common plugin infrastructure for KDE image applications
Summary(zh_CN.UTF-8): KDE 图像程序的公共插件基础构架
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Version: %{rversion}
Release: 2%{?dist}
License: LGPL
URL: http://extragear.kde.org/apps/kipi
Source0: http://mirror.bjtu.edu.cn/kde/stable/%{rversion}/src/%{real_name}-%{version}.tar.xz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: gettext
BuildRequires: cmake >= 2.6.2
BuildRequires: gettext
BuildRequires: libkdelibs4-devel >= 4.0.82

%description
Kipi (KDE Image Plugin Interface) is an effort to develop a common plugin
structure for Digikam, KimDaBa, Showimg and Gwenview. Its aim is to share
image plugins among graphic applications.

%description -l zh_CN.UTF-8
Kipi (KDE 图像插件接口) 是为 Digikam，KimDaBa，Showimg 和 Gwenview 开发公
共插件构架的。其旨在和图像程序之间共享图像插件。

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
%setup -q -n %{real_name}-%{rversion}

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
rm -rf %{buildroot}

make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

magic_rpm_clean.sh

%clean_kde4_desktop_files

%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING
%{kde4_libdir}/*.so.*
%{kde4_iconsdir}/hicolor/*
%{kde4_servicetypesdir}/*.desktop
%{kde4_appsdir}/kipi/*

%files devel
%defattr(-,root,root,-)
%{kde4_libdir}/*.so
%{kde4_includedir}/libkipi/*
%{_libdir}/pkgconfig/*.pc

%changelog
* Wed Apr 23 2014 Liu Di <liudidi@gmail.com> - 4.13.0-2
- 为 Magic 3.0 重建

* Sun Apr 28 2013 Liu Di <liudidi@gmail.com> - 4.10.2-3
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 4.9.3-2
- 为 Magic 3.0 重建

* Tue Aug 11 2009 Ni Hui <shuizhuyuanluo@126.com> - 3.2.3-1mgc
- 更新至 3.2.3
- 拆出开发包
- 己丑  六月廿一
