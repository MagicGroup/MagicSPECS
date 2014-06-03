#define svn_number rc1
%define real_name ksirk

%define kde4_enable_final_bool ON

Name: kde4-%{real_name}
Summary: Conquer-the-world strategy game
Summary(zh_CN.UTF-8): 征服世界的战略游戏
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Version: 4.13.1
Release: 3%{?dist}
License: LGPL
URL: http://extragear.kde.org/apps/kipi
Source0: http://download.kde.org/stable/%{version}/src/%{real_name}-%{version}.tar.xz
# use the system iris library
Patch0: ksirk-4.10.0-system-iris.patch
# if using bundled iris, link statically
Patch1: ksirk-4.10.1-iris_static.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: gettext
BuildRequires: cmake >= 2.6.2
BuildRequires: gettext
BuildRequires: libkdelibs4-devel >= 4.0.82

BuildRequires: desktop-file-utils
BuildRequires: kde4-libkdegames-devel >= %{version}
BuildRequires: pkgconfig(qca2)
%if 0
%define system_iris 1
BuildRequires: pkgconfig(iris)
%else
# some default qca plugin(s) for bundled iris
Requires: qca-ossl%{?_isa}
%endif

Requires: kde4-libkdegames%{?_isa} >= %{_kde4_version}

%description
The goal of KSirk is to conquer the World. It is done by attacking your
neighbors with your armies.

%description -l zh_CN.UTF-8
征服世界的战略游戏。

%prep
%setup -q -n %{real_name}-%{version}
%if 0%{?system_iris}
%patch0 -p1 -b .system-iris
mv ksirk/iris ksirk/iris.BAK
%else
%patch1 -p1 -b .iris_static
%endif

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
#%{kde4_plugindir}/*
#%{kde4_libdir}/*.so.*
%{kde4_appsdir}/*
%{kde4_configdir}/*
%{kde4_xdgappsdir}/*.desktop
#%{kde4_servicesdir}/*
#%{kde4_servicetypesdir}/*
%{kde4_kcfgdir}/*
%{kde4_htmldir}/en/*
#%{kde4_mandir}/*
#%{kde4_libdir}/*.so
%{kde4_iconsdir}/*/*/a*/*

%changelog
* Sun Jun 01 2014 Liu Di <liudidi@gmail.com> - 4.13.1-3
- 更新到 4.13.1

* Mon Apr 28 2014 Liu Di <liudidi@gmail.com> - 4.13.0-3
- 为 Magic 3.0 重建

* Mon Apr 28 2014 Liu Di <liudidi@gmail.com> - 4.13.0-2
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 4.9.3-2
- 为 Magic 3.0 重建

* Tue Aug 11 2009 Ni Hui <shuizhuyuanluo@126.com> - 3.2.3-1mgc
- 更新至 3.2.3
- 拆出开发包
- 己丑  六月廿一
