#define svn_number rc1
%define real_name kshisen

%define kde4_enable_final_bool ON

Name: kde4-%{real_name}
Summary: Shisen-Sho Mahjongg-like tile game
Summary(zh_CN.UTF-8): 连连看游戏
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Version: 4.13.1
Release: 2%{?dist}
License: LGPL
URL:     https://projects.kde.org/projects/kde/kdegames/%{name}
Source0: http://download.kde.org/stable/%{version}/src/%{real_name}-%{version}.tar.xz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: gettext
BuildRequires: cmake >= 2.6.2
BuildRequires: gettext
BuildRequires: libkdelibs4-devel >= 4.0.82

BuildRequires: desktop-file-utils
BuildRequires: kde4-libkdegames-devel >= %{version}
BuildRequires: kde4-libkmahjongg-devel >= %{version}

Requires: kde4-libkdegames%{?_isa} >= %{_kde4_version}
Requires: kde4-libkmahjongg%{?_isa} >= %{_kde4_version}


%description
Shisen-Sho is a solitaire-like game played using the standard set of Mahjong
tiles. Unlike Mahjong however, Shisen-Sho has only one layer of scrambled tiles.
You can remove matching pieces if they can be connected with a line with at most
two bends in it. At the same time, the line must not cross any other tiles.
To win a game of Shisen-Sho the player has to remove all the tiles from the
game board

%description -l zh_CN.UTF-8
连连看游戏。

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
%{kde4_datadir}/sounds/*

%changelog
* Sun Jun 01 2014 Liu Di <liudidi@gmail.com> - 4.13.1-2
- 更新到 4.13.1

* Sun Jun 01 2014 Liu Di <liudidi@gmail.com> - 4.13.0-2
- 为 Magic 3.0 重建

* Mon Apr 28 2014 Liu Di <liudidi@gmail.com> - 4.13.0-2
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 4.9.3-2
- 为 Magic 3.0 重建

* Tue Aug 11 2009 Ni Hui <shuizhuyuanluo@126.com> - 3.2.3-1mgc
- 更新至 3.2.3
- 拆出开发包
- 己丑  六月廿一
