#define svn_number rc1
%define real_name smokekde

%define kde4_enable_final_bool OFF

Name: kde4-%{real_name}
Summary: Bindings for KDE libraries
Summary(zh_CN.UTF-8): KDE 库的绑定
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Version: 4.14.3
Release: 1%{?dist}
License: LGPL
URL: http://extragear.kde.org/apps/kipi
Source0: http://mirrors.ustc.edu.cn/kde/stable/%{version}/src/%{real_name}-%{version}.tar.xz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: gettext
BuildRequires: cmake >= 2.6.2
BuildRequires: libkdelibs4-devel >= 4.0.82
BuildRequires: kde4-kate-devel >= %{version}
BuildRequires: kdepimlibs4-devel >= %{version}
BuildRequires: kde4-okular-devel >= %{version}
BuildRequires: pkgconfig(akonadi)
BuildRequires: smokegen-devel >= %{version}
BuildRequires: smokeqt-devel >= %{version}
BuildRequires: attica-devel >= 0.3.0

Obsoletes: kdebindings < 4.7.0 

# versioned core/runtime deps
Requires: smokegen%{?_isa} >= %{version}
Requires: smokeqt%{?_isa} >= %{version}

%description
Bindings for KDE libraries.

%description -l zh_CN.UTF-8
KDE 库的绑定。

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
%doc AUTHORS COPYING.LIB
%{kde4_libdir}/libsmoke*.so.*

%files devel
%{kde4_libdir}/libsmoke*.so
%{kde4_includedir}/smoke/*
%{kde4_datadir}/smokegen/*

%changelog
* Wed Dec 31 2014 Liu Di <liudidi@gmail.com> - 4.14.3-1
- 更新到 4.14.3

* Fri Oct 31 2014 Liu Di <liudidi@gmail.com> - 4.14.2-1
- 更新到 4.14.2

* Fri Jul 18 2014 Liu Di <liudidi@gmail.com> - 4.13.3-1
- 更新到 4.13.3

* Thu Jun 19 2014 Liu Di <liudidi@gmail.com> - 4.13.2-1
- 更新到 4.13.2

* Wed May 28 2014 Liu Di <liudidi@gmail.com> - 4.13.1-1
- 更新到 4.13.1

* Sun Apr 27 2014 Liu Di <liudidi@gmail.com> - 4.13.0-2
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 4.9.3-2
- 为 Magic 3.0 重建

* Tue Aug 11 2009 Ni Hui <shuizhuyuanluo@126.com> - 3.2.3-1mgc
- 更新至 3.2.3
- 拆出开发包
- 己丑  六月廿一
