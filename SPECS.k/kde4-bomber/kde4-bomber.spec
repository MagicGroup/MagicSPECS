#define svn_number rc1
%define real_name bomber

%define kde4_enable_final_bool ON

Name: kde4-%{real_name}
Summary: Arcade bombing game
Summary(zh_CN.UTF-8): 街机的炸弹游戏
Group: Amusements/Games
Group(zh_CN.UTF-8): 娱乐/游戏
Version: 4.13.1
Release: 1%{?dist}
License: LGPL
URL: http://extragear.kde.org/apps/kipi
%define rversion %version
Source0:  http://download.kde.org/stable/%{rversion}/src/%{real_name}-%{version}.tar.xz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: gettext
BuildRequires: cmake >= 2.6.2
BuildRequires: gettext
BuildRequires: libkdelibs4-devel >= 4.0.82
BuildRequires: kde4-libkdegames-devel >= 4.10.3

%description
Bomber is a single player arcade game. The player is invading various
cities in a plane that is decreasing in height. The goal of the game is
to destroy all the buildings and advance to the next level. Each level
gets a harder by increasing the speed of the plane and the height of the
buildings.

%description -l zh_CN.UTF-8
一个街机炸弹游戏。

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
%{kde4_kcfgdir}/*
%{kde4_htmldir}/en/*
#%{kde4_mandir}/*
#%{kde4_libdir}/*.so
%{kde4_iconsdir}/*/*/a*/*

%changelog
* Fri May 23 2014 Liu Di <liudidi@gmail.com> - 4.13.1-1
- 更新到 4.13.1

* Sun Apr 27 2014 Liu Di <liudidi@gmail.com> - 4.13.0-2
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 4.9.3-2
- 为 Magic 3.0 重建

* Tue Aug 11 2009 Ni Hui <shuizhuyuanluo@126.com> - 3.2.3-1mgc
- 更新至 3.2.3
- 拆出开发包
- 己丑  六月廿一
