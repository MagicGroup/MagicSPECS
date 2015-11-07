#define svn_number rc1
%define real_name klines

%define kde4_enable_final_bool ON

Name: kde4-%{real_name}
Summary: Color lines game
Summary(zh_CN.UTF-8): 彩色连线游戏
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Version: 4.14.3
Release: 2%{?dist}
License: LGPL
URL: http://extragear.kde.org/apps/kipi
Source0: http://download.kde.org/stable/%{version}/src/%{real_name}-%{version}.tar.xz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: gettext
BuildRequires: cmake >= 2.6.2
BuildRequires: gettext
BuildRequires: libkdelibs4-devel >= 4.0.82

BuildRequires: desktop-file-utils
BuildRequires: kde4-libkdegames-devel >= %{version}

Requires: kde4-libkdegames%{?_isa} >= %{_kde4_version}

%description
The goal of Kolor Lines is quite plain. The player has to move the
colored balls around the game board, gathering them into the lines
of the same color by five. Once the line is complete it is removed
from the board, therefore freeing precious space. In the same time
the new balls keep arriving by three after each move, filling up the
game board.  

Kolor Lines cannot be won, and is played against the high score
exclusively. The game ends once the whole game board is filled up with
balls

%description -l zh_CN.UTF-8
彩色连线游戏。

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

%changelog
* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 4.14.3-2
- 为 Magic 3.0 重建

* Wed Dec 31 2014 Liu Di <liudidi@gmail.com> - 4.14.3-1
- 更新到 4.14.3

* Fri Oct 31 2014 Liu Di <liudidi@gmail.com> - 4.14.2-1
- 更新到 4.14.2

* Fri Jul 18 2014 Liu Di <liudidi@gmail.com> - 4.13.3-1
- 更新到 4.13.3

* Thu Jun 19 2014 Liu Di <liudidi@gmail.com> - 4.13.2-1
- 更新到 4.13.2

* Thu May 29 2014 Liu Di <liudidi@gmail.com> - 4.13.1-1
- 更新到 4.13.1

* Mon Apr 28 2014 Liu Di <liudidi@gmail.com> - 4.13.0-2
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 4.9.3-2
- 为 Magic 3.0 重建

* Tue Aug 11 2009 Ni Hui <shuizhuyuanluo@126.com> - 3.2.3-1mgc
- 更新至 3.2.3
- 拆出开发包
- 己丑  六月廿一
