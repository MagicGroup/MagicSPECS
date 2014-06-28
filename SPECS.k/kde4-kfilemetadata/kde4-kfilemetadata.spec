#define svn_number rc1
%define real_name kfilemetadata

%define kde4_enable_final_bool ON

Name: kde4-%{real_name}
Summary: A library for extracting file metadata
Summary(zh_CN.UTF-8): 解压文件元数据的库
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Version: 4.13.2
Release: 1%{?dist}
License: LGPL
URL: http://extragear.kde.org/apps/kipi
%define rversion %version
Source0: http://download.kde.org/stable/%{rversion}/src/%{real_name}-%{version}.tar.xz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: gettext
BuildRequires: cmake >= 2.6.2
BuildRequires: gettext
BuildRequires: libkdelibs4-devel >= 4.0.82

%description
Kfilemetadata is a framework for searching and managing metadata.

%description -l zh_CN.UTF-8
这是搜索和管理元数据的框架。

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

#临时解决措施
for i in `grep -r "no-exceptions" * -l`;do sed -i 's/\-fno\-exceptions/\-fexceptions/g' $i;done
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
%{kde4_plugindir}/*
%{kde4_libdir}/*.so.*
%{kde4_servicesdir}/*
%{kde4_servicetypesdir}/*

%files devel
%defattr(-,root,root,-)
%{kde4_libdir}/*.so
%{kde4_includedir}/*
%{_libdir}/cmake/*

%changelog
* Wed Jun 18 2014 Liu Di <liudidi@gmail.com> - 4.13.2-1
- 更新到 4.13.2

* Fri May 23 2014 Liu Di <liudidi@gmail.com> - 4.13.1-1
- 更新到 4.13.1

* Wed Apr 23 2014 Liu Di <liudidi@gmail.com> - 4.13.0-2
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 4.9.3-2
- 为 Magic 3.0 重建

* Tue Aug 11 2009 Ni Hui <shuizhuyuanluo@126.com> - 3.2.3-1mgc
- 更新至 3.2.3
- 拆出开发包
- 己丑  六月廿一
