#define svn_number rc1
%define real_name ffmpegthumbs

%define kde4_enable_final_bool OFF

Name: kde4-%{real_name}
Summary: Video thumbnail generator using ffmpeg
Summary(zh_CN.UTF-8): 使用 ffmpeg 的视频缩略图生成程序
License: GPL v2 or Later
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
URL: http://ktorrent.org
Version: 4.13.1
Release: 1%{?dist}
%define rversion %version
Source0:  http://download.kde.org/stable/%{rversion}/src/%{real_name}-%{rversion}.tar.xz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: cmake >= 2.6.2
BuildRequires: gettext
BuildRequires: libkdelibs4-devel >= 4.0.82
BuildRequires: ffmpeg-devel

%description
FFMpegThumbs is a video thumbnail generator for KDE file managers 
like Dolphin and Konqueror. It enables them to show preview images 
of video files using FFMpeg.

This package is part of the KDE multimedia module.

%description -l zh_CN.UTF-8
这是 KDE 文件管理器（如 Dolphin 或 Konqueror）的视频缩略图生成器。
它使用 FFMpeg 来给视频显示一个预览图。

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
#%{kde4_bindir}/*
%{kde4_plugindir}/*
#%{kde4_libdir}/*.so*
#%{kde4_appsdir}/*
#%{kde4_iconsdir}/hicolor/*
#%{kde4_xdgappsdir}/*.desktop
#%{kde4_kcfgdir}/*
%{kde4_servicesdir}/*
#%{kde4_servicetypesdir}/*
#%{kde4_configdir}/*
#%{kde4_datadir}/mime/*
#%{kde4_mandir}/*
#%{kde4_iconsdir}/oxygen/*
#%{kde4_datadir}/autostart/*.desktop
#%{kde4_dbus_interfacesdir}/*.xml
#%{kde4_htmldir}/en/*

%changelog
* Fri May 23 2014 Liu Di <liudidi@gmail.com> - 4.13.1-1
- 更新到 4.13.1

* Fri Apr 25 2014 Liu Di <liudidi@gmail.com> - 4.13.0-3
- 为 Magic 3.0 重建

* Thu Jul 04 2013 Liu Di <liudidi@gmail.com> - 4.10.4-2
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 4.9.3-2
- 为 Magic 3.0 重建

* Tue Aug 11 2009 Ni Hui <shuizhuyuanluo@126.com> - 3.2.3-1mgc
- 更新至 3.2.3
- 拆出开发包
- 己丑  六月廿一
