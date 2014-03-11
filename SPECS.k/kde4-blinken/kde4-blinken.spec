%define rversion %{kde4_kdelibs_version}
#define svn_number rc1
%define real_name blinken

%define kde4_enable_final_bool OFF

Name: kde4-%{real_name}
Summary: Blinken is the KDE version of the well-known game Simon Says.
Summary(zh_CN.UTF-8): Blinken 是一款著名游戏 Simon Says 的 KDE 版本。 
License: GPL v2 or Later
Group: Applications/Internet
Group(zh_CN.UTF-8): 应用程序/互联网
URL: http://ktorrent.org
Version: %{rversion}
Release: 1%{?dist}
Source0:  http://mirror.bjtu.edu.cn/kde/stable/%{rversion}/src/%{real_name}-%{rversion}.tar.xz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: cmake >= 2.6.2
BuildRequires: gettext
BuildRequires: libkdelibs4-devel >= 4.0.82

Requires:      sj-stevehand-fonts

%description
Blinken is the KDE version of the well-known game Simon Says.
Follow the pattern of sounds and lights as long as you can! 
Press the start game button to begin. Watch the computer and 
copy the pattern it makes. Complete the sequence in the right 
order to win.

%description -l zh_CN.UTF-8
Blinken 是一款著名游戏 Simon Says 的 KDE 版本。

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

%clean_kde4_desktop_files

%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING
%{kde4_bindir}/*
%{kde4_iconsdir}/hicolor/*
%{kde4_xdgappsdir}/blinken.desktop
%{kde4_appsdir}/blinken/*
%{kde4_kcfgdir}/blinken.kcfg
%{kde4_htmldir}/en/*


%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 4.9.3-2
- 为 Magic 3.0 重建

* Tue Aug 11 2009 Ni Hui <shuizhuyuanluo@126.com> - 3.2.3-1mgc
- 更新至 3.2.3
- 拆出开发包
- 己丑  六月廿一
