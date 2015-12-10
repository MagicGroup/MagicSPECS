## nepomuk support only for kde < 4.13
%define nepomuk 0

Name: rekonq
Version:	2.4.2
Release:	3%{?dist}
Group: Applications/Internet
Group(zh_CN.UTF-8):  应用程序/互联网
License: GPLv2+
Summary: KDE browser based on QtWebkit
Summary(zh_CN.UTF-8): 基于 QtWebkit 的 KDE 浏览器
URL: http://rekonq.sourceforge.net/
Source0: https://downloads.sourceforge.net/project/rekonq/2.0/%{name}-%{version}.tar.xz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# 修正 rekonq 配置对话框左侧目录文字乱码
Patch1: rekonq-0.6.1-utf8_setting_pagename.patch
# 双击标签关闭支持
Patch2: rekonq-0.4.0-dbclick_close_tab.patch
Patch3: rekonq-0.4.0-zh_CN.patch
Patch4: rekonq-0.4.0-default_bookmarks.patch
# 拖拽标签时禁用预览功能以解决拖动时卡的问题
Patch5: rekonq-0.3.0-no_preview_when_dragging.patch

## upstream patches
Patch101: 0001-Get-sure-fast-typing-work.patch
Patch102: 0002-Fix-rekonqui.rc.patch
Patch104: 0004-Allows-to-build-without-Soprano-and-Nepomuk.patch

BuildRequires: libkdelibs4-devel >= 4.3.1
BuildRequires: kdebase4-workspace-devel >= 4.3.1
BuildRequires: gettext
BuildRequires: qtwebkit-devel >= 2.2.0

%if 0%{?nepomuk}
BuildRequires:	nepomuk-core-devel
%endif

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
%patch101 -p1 -b .0001
%patch102 -p1 -b .0002
%patch104 -p1 -b .0004

# 去除文档
rm -rf doc

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} \
  %{?nepomuk:-DWITH_NEPOMUK:BOOL=ON} \
  ..
popd
make %{?_smp_mflags} -C %{_target_platform}

%install
rm -rf %{buildroot}

make install/fast DESTDIR=%{buildroot} -C %{_target_platform}
magic_rpm_clean.sh
%find_lang %{name} --with-kde --all-name || %define nolang 1

%clean_kde4_desktop_files

%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%postun
if [ $1 -eq 0 ] ; then
touch --no-create %{_kde4_iconsdir}/hicolor/ &>/dev/null
gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &>/dev/null || :

%if 0%{?nolang}
%files
%else
%files -f %{name}.lang
%endif
%defattr (-,root,root,-)
%doc AUTHORS COPYING
%{kde4_bindir}/%{name}
%{kde4_libdir}/libkdeinit4_rekonq.so
%dir %{kde4_appsdir}/%{name}
%{kde4_appsdir}/%{name}/*
%{kde4_kcfgdir}/%{name}.kcfg
%{kde4_iconsdir}/hicolor/*/apps/%{name}.*
%{kde4_xdgappsdir}/%{name}.desktop
%{kde4_localedir}/*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 2.4.2-3
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 2.4.2-2
- 为 Magic 3.0 重建

* Sat Sep 12 2015 Liu Di <liudidi@gmail.com> - 2.4.2-1
- 更新到 2.4.2

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 0.8.71-2
- 为 Magic 3.0 重建

* Sat Jan 16 2010 Ni Hui <shuizhuyuanluo@126.com> - 0.3.0-1mgc
- 首次生成 RPM 包
- 修正 rekonq 配置对话框左侧目录文字乱码
- 双击标签关闭支持
