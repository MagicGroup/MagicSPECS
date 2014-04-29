%define rversion %{kde4_kdelibs_version}
#define svn_number rc1
%define real_name lskat

%define kde4_enable_final_bool ON

Name: kde4-%{real_name}
Summary: A fun and engaging card game
Summary(zh_CN.UTF-8): 纸牌游戏
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Version: %{rversion}
Release: 2%{?dist}
License: GPLv2+ and GFDL
URL:     https://projects.kde.org/projects/kde/kdegames/%{name}
Source0: http://mirror.bjtu.edu.cn/kde/stable/%{rversion}/src/%{real_name}-%{version}.tar.xz
Patch1:	lskat-4.10.3-fix.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: gettext
BuildRequires: cmake >= 2.6.2
BuildRequires: gettext
BuildRequires: libkdelibs4-devel >= 4.0.82

BuildRequires: desktop-file-utils
BuildRequires: kde4-libkdegames-devel >= %{version}

Requires: kde4-libkdegames%{?_isa} >= %{_kde4_version}

%description
Lieutenant Skat (from German Offiziersskat) is a fun and engaging card
game for two players, where the second player is either live opponent,
or builtin artificial intelligence.

%description -l zh_CN.UTF-8
纸牌游戏。

%prep
%setup -q -n %{real_name}-%{rversion}
%patch1 -p1

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
#%{kde4_configdir}/*
%{kde4_xdgappsdir}/*.desktop
#%{kde4_servicesdir}/*
#%{kde4_servicetypesdir}/*
#%{kde4_kcfgdir}/*
%{kde4_htmldir}/en/*
#%{kde4_mandir}/*
#%{kde4_libdir}/*.so
%{kde4_iconsdir}/*/*/a*/*

%changelog
* Mon Apr 28 2014 Liu Di <liudidi@gmail.com> - 4.13.0-2
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 4.9.3-2
- 为 Magic 3.0 重建

* Tue Aug 11 2009 Ni Hui <shuizhuyuanluo@126.com> - 3.2.3-1mgc
- 更新至 3.2.3
- 拆出开发包
- 己丑  六月廿一
