#define svn_number 971668
%define betatag %{nil}
%define real_name konversation

%define kde4_enable_final_bool OFF

Name: kde4-konversation
Summary: Konversation is a user friendly IRC client for KDE
Summary(zh_CN.UTF-8): Konversation 是一款 KDE 下用户友好 IRC 客户端
License: GPL v2 or Later
Group: Applications/Internet
Group(zh_CN.UTF-8): 应用程序/互联网
URL: http://konversation.kde.org
Version: 1.6
Release: 3%{?dist}
Source0: http://download.kde.org/stable/%{real_name}/%{version}/src/%{real_name}-%{version}.tar.xz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: cmake >= 2.6.2
BuildRequires: gettext
BuildRequires: libkdelibs4-devel >= 4.0.82
BuildRequires: libkdepimlibs4-devel
BuildRequires: phonon-devel

# 默认频道/启用托盘/自动连接, written by nihui, Dec.29th, 2009
Patch101: konversation-1.4-default_preference.patch
# 如果 utf-8 字符串无法解析则回滚到 gb18030 而非 iso-8859-1, written by nihui, Dec.29th, 2009
Patch102: konversation-1.2.3-fallback_to_gb18030.patch
# 默认使用 utf-8 编码, written by nihui, Dec.29th, 2009
Patch103: konversation-1.5-utf8_default_charset.patch


%description
A simple and easy to use IRC client for KDE with support for
strikeout; multi-channel joins; away / unaway messages;
ignore list functionality; (experimental) support for foreign
language characters; auto-connect to server; optional timestamps
to chat windows; configurable background colors and much more.

%description -l zh_CN.UTF-8
一款 KDE 下的简单好用的 IRC 客户端，支持多频道加入、离开/在线
消息、忽略列表功能、多国语言字符(实验中)、自动连接至服务器、
聊天窗口时间戳、可配置的背景颜色以及更多功能。


%prep
%setup -q -n %{real_name}-%{version}

%patch101 -p1 -b .default_preference
%patch102 -p1 -b .fallback_to_gb18030
%patch103 -p1 -b .utf8_default

rm -rf doc-translations/*

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
%clean_kde4_notifyrc_files
%adapt_kde4_notifyrc_files

%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files
%defattr(-,root,root,-)
%doc COPYING README
%{kde4_bindir}/*
%{kde4_appsdir}/*
%{kde4_xdgappsdir}/*.desktop
%{kde4_servicesdir}/*
%{kde4_htmldir}/en/*
%{kde4_iconsdir}/hicolor/*/a*/*
%{kde4_localedir}/*

%changelog
* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 1.6-3
- 更新到 1.6

* Sun Jun 01 2014 Liu Di <liudidi@gmail.com> - 1.5-2
- 为 Magic 3.0 重建

* Sun Jun 01 2014 Liu Di <liudidi@gmail.com> - 1.5-1
- 更新到 1.5

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.4-3
- 为 Magic 3.0 重建

* Tue Dec 29 2009 Ni Hui <shuizhuyuanluo@126.com> - 1.2.1-2mgc
- 默认频道/启用托盘/自动连接(patch 101 written by nihui)
- 如果 utf-8 字符串无法解析则回滚到 gb18030 而非 iso-8859-1(patch 102 written by nihui)
- 默认使用 utf-8 编码(patch 103 written by nihui)
- 乙丑  十一月十四

* Fri Aug 7 2009 Ni Hui <shuizhuyuanluo@126.com> - 1.2-0.alpha5.1mgc
- 更新至 1.2-alpha5
- 己丑  六月十七  [立秋]

* Mon Feb 2 2009 Ni Hui <shuizhuyuanluo@126.com> - 1.1.75-0.svn920004.1mgc
- 更新至 1.1.75-svn 920004
- 己丑  正月初八

* Sat Oct 25 2008 Ni Hui <shuizhuyuanluo@126.com> - 1.1-0.1mgc
- 更新至 1.1(KDE3 告别版本)
- 去除配置文件(移入 magic-kde-config 包)
- 戊子  九月廿七

* Fri Feb 22 2008 Ni Hui <shuizhuyuanluo@126.com> - 1.0.1-3.2mgc
- 添加配置文件
- 戊子  正月十六

* Sat Nov 17 2007 Ni Hui <shuizhuyuanluo@126.com> - 1.0.1-3.1mgc
- rebuild
- 去除多余语言文件

* Wed Aug 08 2007 Ni Hui <shuizhuyuanluo@126.com> - 1.0.1-3mgc
- 修正 common 文件夹的链接关系
- 菜单项中文翻译

* Sat Jul 28 2007 Ni Hui <shuizhuyuanluo@126.com> - 1.0.1-2mgc
- 改善了一点翻译
- 修改 spec 文件，重新建包

* Sun Apr 22 2007 Ni Hui <shuizhuyuanluo@126.com> - 1.0.1-1mgc
- first port to Magiclinux 2.1
