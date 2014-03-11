Name: rekonq
Version: 0.8.71
Release: 2%{?dist}
Group: Applications/Internet
Group(zh_CN.UTF-8):  应用程序/互联网
License: GPLv2+
Summary: KDE browser based on QtWebkit
Summary(zh_CN.UTF-8): 基于 QtWebkit 的 KDE 浏览器
URL: http://rekonq.sourceforge.net/
Source0: http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# 修正 rekonq 配置对话框左侧目录文字乱码
Patch1: rekonq-0.6.1-utf8_setting_pagename.patch
# 双击标签关闭支持
Patch2: rekonq-0.4.0-dbclick_close_tab.patch
Patch3: rekonq-0.4.0-zh_CN.patch
Patch4: rekonq-0.4.0-default_bookmarks.patch
# 拖拽标签时禁用预览功能以解决拖动时卡的问题
Patch5: rekonq-0.3.0-no_preview_when_dragging.patch

BuildRequires: libkdelibs4-devel >= 4.3.1
BuildRequires: kdebase4-workspace-devel >= 4.3.1
BuildRequires: gettext
BuildRequires: qtwebkit-devel >= 2.2.0


Requires: kdebase4-workspace >= 4.3.1
# cookies / proxy 配置模块
Requires: kcm_kio
# 速搜配置模块
Requires: kcm_kurifilt
Requires: qt4-webkit

%description
rekonq is a KDE browser based on QtWebkit. Its code is based on Nokia
QtDemoBrowser. It's implementation is going to embrace
KDE technologies to have a full-featured KDE web browser.

%description -l zh_CN.UTF-8
rekonq 是款基于 QtWebkit 的 KDE 浏览器。代码基于 Nokia 的 QtDemoBrowser。
拥有完整 KDE 技术特性的 KDE 网页浏览器。

%prep
%setup -q

#%patch1 -p1 -b .orig
#%patch2 -p1 -b .orig
#%patch3 -p1 -b .orig
#%patch4 -p1 -b .orig

#%patch5 -p1 -b .orig
# 去除文档
rm -rf doc

%build
mkdir build
cd build
%cmake_kde4 ..

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
cd build
make DESTDIR=%{buildroot} install

magic_rpm_clean.sh

%clean_kde4_desktop_files

%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files
%defattr (-,root,root,-)
%doc AUTHORS COPYING
%{kde4_bindir}/%{name}
%{kde4_bindir}/kwebapp
%{kde4_libdir}/libkdeinit4_rekonq.so
%dir %{kde4_appsdir}/%{name}
%{kde4_appsdir}/%{name}/*
%{kde4_kcfgdir}/%{name}.kcfg
%{kde4_iconsdir}/hicolor/*/apps/%{name}.*
%{kde4_xdgappsdir}/%{name}.desktop
%{kde4_localedir}/*

%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 0.8.71-2
- 为 Magic 3.0 重建

* Sat Jan 16 2010 Ni Hui <shuizhuyuanluo@126.com> - 0.3.0-1mgc
- 首次生成 RPM 包
- 修正 rekonq 配置对话框左侧目录文字乱码
- 双击标签关闭支持
