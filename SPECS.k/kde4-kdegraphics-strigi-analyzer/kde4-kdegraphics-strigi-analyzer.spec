%define rversion %{kde4_kdelibs_version}
#define svn_number rc1
%define real_name kdegraphics-strigi-analyzer

%define kde4_enable_final_bool ON

Name: kde4-%{real_name}
Summary: Strigi analyzers for various graphic types
Summary(zh_CN.UTF-8): 多种图形的 Strigi 分析器
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
Strigi analyzers for various graphic types, including: tiff, dvi

%description -l zh_CN.UTF-8
多种图形格式（包括 dvi, tiff）的 Strigi 分析器

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
mkdir build
cd build
%cmake_kde4 ..

make %{?_smp_mflags}

%install
cd build
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

magic_rpm_clean.sh

%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING
#%{kde4_bindir}/*
#%{kde4_plugindir}/*
%{kde4_libdir}/strigi/*.so
#%{kde4_appsdir}/ktorrent
#%{kde4_iconsdir}/hicolor/*
#%{kde4_xdgappsdir}/ktorrent.desktop
#%{kde4_servicesdir}/*
#%{kde4_servicetypesdir}/*
#%{kde4_localedir}/*

%if 0
%files devel
%defattr(-,root,root,-)
%{kde4_libdir}/*.so
%endif

%changelog
* Thu Apr 24 2014 Liu Di <liudidi@gmail.com> - 4.13.0-2
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 4.9.3-2
- 为 Magic 3.0 重建

* Tue Aug 11 2009 Ni Hui <shuizhuyuanluo@126.com> - 3.2.3-1mgc
- 更新至 3.2.3
- 拆出开发包
- 己丑  六月廿一
