
%define real_name kmess
%define svn_number 4577

Name:          kmess2
Version:        2.0.6.2
Release:        4%{?dist}
Summary:        MSN Messenger / Windows Live Messenger client for KDE
Summary(zh_CN.UTF-8): KDE 下的 MSN Messenger / Windows Live Messenger 客户端

Group:          Applications/Networking
Group(zh_CN.UTF-8): 应用程序/互联网
License:        GPLv2+
URL:            http://www.kmess.org/
Source0:        http://downloads.sourceforge.net/project/kmess/Latest%20versions/%{version}/%{real_name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: libkdelibs4-devel
BuildRequires: cmake >= 2.4.5
BuildRequires: gettext
BuildRequires: libxml2-devel
BuildRequires: libxslt-devel
BuildRequires: qca2-devel >= 2.0.1
BuildRequires: qca-ossl >= 2.0.0
BuildRequires: libXScrnSaver-devel
BuildRequires: libisf-qt-devel

Requires: qca-ossl

%description
KMess is a MSN Messenger / Windows Live Messenger client for Linux.
It enables Linux users to chat with friends online who are using
MSN Messenger in Windows or Mac OS. The strength of KMess is it's
integration with the KDE desktop environment, focus on MSN Messenger
specific features and an easy-to-use interface.

Authors:
--------
    Mike K. Bennett       <mkb137 --at-- users.sourceforge.net>
    Michael Curtis        <mdcurtis --at-- users.sourceforge.net>
    Jan Toenjes           <jan.toenjes --at-- web.de>
    Diederik van der Boor <vdboor --at-- codingdomain.com>
    Richard Conway        <richardconway --at-- users.sourceforge.net>
    Valerio Pilo          <amroth --at-- coldshock.net>


%description -l zh_CN.UTF-8
KMess 是一款 Linux 下的 MSN Messenger / Windows Live Messenger 客户端。
它能让 Linux 用户可以与 Windows 或 Mac OS 的用户相互沟通聊天。
KMess 的亮点是与 KDE 桌面环境的整合，对 MSN Messenger 的专注度和用起来十分简单的界面。

作者：
--------
    Mike K. Bennett       <mkb137 --at-- users.sourceforge.net>
    Michael Curtis        <mdcurtis --at-- users.sourceforge.net>
    Jan Toenjes           <jan.toenjes --at-- web.de>
    Diederik van der Boor <vdboor --at-- codingdomain.com>
    Richard Conway        <richardconway --at-- users.sourceforge.net>
    Valerio Pilo          <amroth --at-- coldshock.net>


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


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog FEATURES README TODO
%{kde4_bindir}/*
%{kde4_plugindir}/*
%{kde4_xdgappsdir}/*
%{kde4_appsdir}/kmess/*
%{kde4_configdir}/*
%{kde4_htmldir}/en/*
%{kde4_iconsdir}/*
%{kde4_datadir}/emoticons/*
%{kde4_servicesdir}/*
%{kde4_datadir}/locale/*
%{kde4_datadir}/sounds/*

%changelog
* Mon Nov 09 2015 Liu Di <liudidi@gmail.com> - 2.0.6.2-4
- 为 Magic 3.0 重建

* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 2.0.6.2-3
- 为 Magic 3.0 重建

* Fri Jun 06 2014 Liu Di <liudidi@gmail.com> - 2.0.6.2-2
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 2.0.6.1-2
- 为 Magic 3.0 重建

* Sun Apr 12 2009 Ni Hui <shuizhuyuanluo@126.com> - 2.0-0.svn4577.1mgc
- 更新至 2.0-svn 4577
- 己丑  三月十七

* Sun Feb 1 2009 Ni Hui <shuizhuyuanluo@126.com> - 2.0-0.svn4098.1mgc
- 更新至 2.0-svn 4098
- 己丑  正月初七

* Sun Jun 1 2008 Ni Hui <shuizhuyuanluo@126.com> - 2.0-0.svn3206.1mgc
- 首次生成 rpm 包
- 戊子  四月廿七
