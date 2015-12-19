%define real_name kde-runtime

#define kde4_enable_final_bool OFF

Name: kdebase4-runtime
Summary: The KDE Runtime Components
Summary(zh_CN.UTF-8): KDE 运行环境组件
License: GPL v2 or later
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
URL: http://www.kde.org/
Version: 15.08.3
Release: 4%{?dist}
%define rversion %version
Source0: http://download.kde.org/stable/applications/%{rversion}/src/%{real_name}-%{rversion}.tar.xz
Source1: im.png
Source2: extract_rpm.desktop
Source3: magic-kde4soundtheme.tar.gz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# FIXME: post installation requirement
Requires: vorbis-tools

# default knotify external player for magiclinux
#Requires: sox

BuildRequires: bluez-libs
BuildRequires: libkdelibs4-devel
BuildRequires: libkdepimlibs4-devel
BuildRequires: qimageblitz-devel >= 0.0.4
BuildRequires: libsmbclient-devel
BuildRequires: libusb-devel
BuildRequires: exiv2-devel
BuildRequires: ntrack-devel
BuildRequires: soprano-devel >= 2.3.70
BuildRequires: strigi >= 0.6.3
BuildRequires: qt4-devel >= 4.6.0
BuildRequires: clucene-core-devel >= 0.9.20
BuildRequires: openexr-devel
BuildRequires: automoc4 >= 0.9.87
BuildRequires: phonon-devel >= 4.3.80
BuildRequires: openslp-devel
BuildRequires: xz-devel
BuildRequires: libssh-devel >= 0.4.0
BuildRequires: gpgme-devel
BuildRequires: libcanberra-devel
BuildRequires: libwebp-devel

# xine 版本低于 1.1.9 时会出现播放短文件卡机问题
#BuildRequires: xine-lib-devel >= 1.1.9


# 搜索引擎项
Patch1: kdebase-runtime-4.2.x-searchproviders-shortcuts.patch
# from fedora project
Patch4: kdebase-runtime-4.3.0-nepomuk-autostart.patch

# kde brunch 代码更新
#Patch1: kdebase-runtime-4.0.2-780207_to_782891.diff
Patch3: kdebase-runtime-4.1.2-hotplug-kde3.diff
Patch6: kdebase-runtime-4.1.2-simple-ccsm-kde.diff

# correct path for htsearch
Patch7: kdebase-runtime-4.5.3-htsearch.patch

# Launch compiz via compiz-manager so we get window decorations and
# other such decadent luxuries (AdamW 2011/01)
Patch8: kdebase-runtime-4.5.95-compiz.patch

# msn im 小图标支持
# patch 101 ported to KDE4 by nihui, Jan.17th, 2009
Patch101: kdebase-runtime-4.1.96-emoticons_im.patch
# 速搜编码转换
# patch 102 written by nihui, Jan.17th, 2009
Patch102: kdebase-runtime-4.2.85-kuriikwsfiltereng_convert_string_encoding.patch
# khelpcenter 左侧树形目录编码设定
# patch 103 written by nihui, Jul.11st, 2009
Patch103: kdebase-runtime-4.2.95-khelpcenter-utf8_cache_xml.patch
# 设定 knotify 默认播放器
# patch 104 written by nihui, Aug 14th, 2010
Patch104: kdebase-runtime-4.5.0-knotify-preference.patch
# 文本文件缩略图编码探测
# patch 105 written by nihui, Aug.29th, 2010
Patch105: kdebase-runtime-4.5.0-textthumbnail_prober_encoding.patch

Patch800: kdebase-runtime-4.3.90-enablefinal.patch

# upstream

%description
This package contains all run-time dependencies of KDE applications.

%description -l zh_CN.UTF-8
KDE 应用程序的所有运行库依赖。

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
%package devel
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: The KDE Runtime Components: Build Environment
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires: kdepimlibs4 >= %{version} libkdelibs4-devel
Requires: libkdepimlibs4 >= %{version}
Requires: kdebase4-runtime >= %{version}

%description devel
This package contains all necessary include files and libraries needed
to develop KDE Runtime applications.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
%package kwalletd
Summary: KDE Runtime Components kwallet support files
Summary(zh_CN.UTF-8): KDE 运行时 kwallet 支持文件
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE

%description kwalletd
%{summary}.

%description kwalletd -l zh_CN.UTF-8
KDE 运行时 kwallet 支持文件。

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

%prep
%setup -q -n %{real_name}-%{rversion}

%patch1 -p1

%patch3
#%patch6 
#%patch7 -p1
#%patch8 -p1

%patch101 -p1
%patch103 -p1
#这个暂时不修改，看看结果
#%patch104 -p0
%patch105 -p1


# compile fix
# %patch800 -p1

# upstream

%build
mkdir build
cd build
%cmake_kde4 ..

make %{?_smp_mflags}

%install
cd build
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

# fix documentation multilib conflict in index.cache
for f in kioslave/nepomuksearch kcontrol/spellchecking kcontrol/performance \
   kcontrol/kcmnotify kcontrol/kcmcss kcontrol/ebrowsing; do
   bunzip2 %{buildroot}%{_kde4_docdir}/HTML/en/$f/index.cache.bz2
   sed -i -e 's!name="id[a-z]*[0-9]*"!!g' %{buildroot}%{_kde4_docdir}/HTML/en/$f/index.cache
   sed -i -e 's!#id[a-z]*[0-9]*"!!g' %{buildroot}%{_kde4_docdir}/HTML/en/$f/index.cache
   bzip2 -9 %{buildroot}%{_kde4_docdir}/HTML/en/$f/index.cache
done

# kdesu symlink
ln -s %{_kde4_libexecdir}/kdesu %{buildroot}%{_kde4_bindir}/kdesu

# omit hicolor index.theme, use one from hicolor-icon-theme
# 不知道是否有其它影响
rm -f %{buildroot}%{_kde4_iconsdir}/hicolor/index.theme

## im.png 小图标安装
install -m 644 %{SOURCE1} %{buildroot}%{kde4_datadir}/emoticons/kde4/

# 右键释放 rpm 菜单
mkdir -p %{buildroot}%{kde4_servicesdir}/ServiceMenus/
install -m 644 %{SOURCE2} %{buildroot}%{kde4_servicesdir}/ServiceMenus/

# 重命名 air 主题和 oxygen 主题的面板不透明 svg 文件以便使得在未启用桌面特效时让面板半透明
mv %{buildroot}%{kde4_appsdir}/desktoptheme/default/opaque/widgets/panel-background.svgz %{buildroot}%{kde4_appsdir}/desktoptheme/default/opaque/widgets/panel-background.svgz.bak
mv %{buildroot}%{kde4_appsdir}/desktoptheme/oxygen/opaque/widgets/panel-background.svgz %{buildroot}%{kde4_appsdir}/desktoptheme/oxygen/opaque/widgets/panel-background.svgz.bak

# 安装 magic 系统音效主题
tar -xf %{SOURCE3} -C %{buildroot}%{kde4_datadir}/sounds/

# 不进行菜单处理
#  mkdir -p $RPM_BUILD_ROOT/etc/xdg/menus
#  mv %{buildroot}%{kde4_sysconfdir}/xdg/menus/kde-information.menu %{buildroot}%{_sysconfdir}/xdg/menus/kde4-information.menu
#  mv $RPM_BUILD_ROOT/opt/kde4/etc/xdg/menus/kde-kcontrol.menu $RPM_BUILD_ROOT/etc/xdg/menus/kde4-kcontrol.menu
#  mv $RPM_BUILD_ROOT/opt/kde4/etc/xdg/menus/kde-settings.menu $RPM_BUILD_ROOT/etc/xdg/menus/kde4-settings.menu

# clean xdg directory files
find %{buildroot}%{kde4_datadir}/desktop-directories -regex ".*\.directory$" | LC_ALL=zh_CN.UTF-8 xargs \
    sed -i '/^..*\[[^z]..*\]=..*$/d'

# rpaths
# use chrpath hammer for now, find better patching solutions later -- Rex
chrpath --list   %{buildroot}%{_libdir}/kde4/plugins/phonon_platform/kde.so ||:
chrpath --delete %{buildroot}%{_libdir}/kde4/plugins/phonon_platform/kde.so

magic_rpm_clean.sh

%clean_kde4_desktop_files
%clean_kde4_notifyrc_files
%adapt_kde4_notifyrc_files

%post
/usr/sbin/ldconfig
# convert ogg sound files to wav format
pushd "/usr/share/sounds/"
for oggfile in `ls *.ogg`; do
    wavfile=${oggfile%.ogg}.wav;
    oggdec -Q $oggfile -o $wavfile;
done
popd

%postun
/usr/sbin/ldconfig
# no need to remove the wav files generated when installing
# --- nihui

%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files devel
%defattr(-,root,root)
%{kde4_libdir}/*.so
%{kde4_appsdir}/cmake/*
%exclude %{kde4_libdir}/libkdeinit4_*.so
%{kde4_includedir}/*.h
#%{kde4_includedir}/nepomuk/*

# kwalletd sub package
%exclude %{kde4_libdir}/libkwalletbackend.so
%exclude %{kde4_libdir}/libknotifyplugin.so

%files kwalletd
%defattr(-,root,root)
%{kde4_bindir}/kwalletd
%{kde4_libdir}/libkdeinit4_kwalletd.so
%{kde4_libdir}/libkwalletbackend.so
%{kde4_libdir}/libkwalletbackend.so.*
%{kde4_appsdir}/kwalletd/*
%{kde4_servicesdir}/kwalletd.desktop

%files
%defattr(-,root,root)
%{kde4_bindir}/*
%{_sysconfdir}/xdg/menus/kde-information.menu
%{kde4_plugindir}/*.so
%{kde4_libdir}/kconf_update_bin/phonon_devicepreference_update
%{kde4_libdir}/kconf_update_bin/phonon_deviceuids_update
%{kde4_plugindir}/libexec/*
#%dir %{kde4_plugindir}/plugins/styles
#%{kde4_plugindir}/plugins/styles/*.so
%{kde4_libdir}/libknotifyplugin.so
%{kde4_plugindir}/plugins/phonon_platform/kde.so
%{kde4_libdir}/*.so.*
%{kde4_libdir}/libkdeinit4_*.so
#%{kde4_libdir}/strigi/strigiindex_nepomukbackend.so
%{kde4_xdgappsdir}/*.desktop
%{kde4_appsdir}/*
%{kde4_kcfgdir}/khelpcenter.kcfg
%config %{kde4_configdir}/khotnewstuff*.knsrc
%config %{kde4_configdir}/kshorturifilterrc
%config %{kde4_configdir}/emoticons.knsrc
%config %{kde4_configdir}/icons.knsrc
%{kde4_dbus_servicesdir}/org.kde.knotify.service
%{kde4_dbus_interfacesdir}/org.kde.khelpcenter.kcmhelpcenter.xml
%{kde4_dbus_interfacesdir}/org.kde.KTimeZoned.xml
%{kde4_dbus_interfacesdir}/org.kde.network.kioslavenotifier.xml
%dir %{kde4_datadir}/desktop-directories
%{kde4_datadir}/desktop-directories/*
%{kde4_datadir}/mime/packages/network.xml
%{kde4_servicesdir}/*
%{kde4_servicetypesdir}/*
%{kde4_localedir}/*
%{kde4_mandir}/man*/kdesu.1*
%{kde4_mandir}/man*/plasmapkg.1*
%{kde4_datadir}/emoticons
%{kde4_datadir}/sounds/*
%doc %lang(en) %{kde4_htmldir}/en/*
%exclude %{kde4_appsdir}/cmake
%{kde4_iconsdir}/hicolor/*/apps/*
%{kde4_iconsdir}/default.kde4

%{_sysconfdir}/dbus-1/system.d/org.kde.kcontrol.kcmremotewidgets.conf
%{kde4_dbus_servicesdir}/org.kde.kuiserver.service
%{kde4_dbus_system_servicesdir}/org.kde.kcontrol.kcmremotewidgets.service
#%{kde4_auth_policy_filesdir}/org.kde.kcontrol.kcmremotewidgets.policy
%{kde4_libdir}/kde4/imports/org/kde/*
%{kde4_datadir}/config.kcfg/jpegcreatorsettings.kcfg
#%{kde4_datadir}/ontology/kde/*

%{kde4_plugindir}/platformimports/touch/org/kde/plasma/components/

%{kde4_datadir}/polkit-1/actions/org.kde.kcontrol.kcmremotewidgets.policy

%{kde4_plugindir}/plugins/imageformats/kimg_webp.so
%{kde4_datadir}/mime/packages/webp.xml

# kwalletd sub package
%exclude %{kde4_bindir}/kwalletd
%exclude %{kde4_libdir}/libkdeinit4_kwalletd.so
%exclude %{kde4_libdir}/libkwalletbackend.so.*
%exclude %{kde4_appsdir}/kwalletd/*
%exclude %{kde4_servicesdir}/kwalletd.desktop




# 需要进一步处理
%changelog
* Mon Nov 09 2015 Liu Di <liudidi@gmail.com> - 4.14.3-4
- 为 Magic 3.0 重建

* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 4.14.3-3
- 为 Magic 3.0 重建

* Mon Mar 02 2015 Liu Di <liudidi@gmail.com> - 4.14.3-2
- 为 Magic 3.0 重建

* Tue Dec 30 2014 Liu Di <liudidi@gmail.com> - 4.14.3-1
- 更新到 4.14.3

* Wed Oct 22 2014 Liu Di <liudidi@gmail.com> - 4.14.2-1
- 更新到 4.14.2

* Fri Jul 18 2014 Liu Di <liudidi@gmail.com> - 4.13.3-1
- 更新到 4.13.3

* Wed Jun 18 2014 Liu Di <liudidi@gmail.com> - 4.13.2-1
- 更新到 4.13.2

* Thu May 22 2014 Liu Di <liudidi@gmail.com> - 4.13.1-1
- 更新到 4.13.1

* Wed Apr 23 2014 Liu Di <liudidi@gmail.com> - 4.13.0-1.2
- 为 Magic 3.0 重建

* Wed Apr 23 2014 Liu Di <liudidi@gmail.com> - 4.13.0-1.1
- 为 Magic 3.0 重建

* Sat Dec 5 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.3.4-1mgc
- 更新至 4.3.4
- 乙丑  十月十九

* Tue Aug 18 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.3.0-3mgc
- 添加右键释放 rpm 菜单
- 强制使用 oxygen/air plasma 半透明面板主题文件
- 乙丑  六月廿八

* Wed Aug 5 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.3.0-2mgc
- 更新至 4.3.0(KDE 4.3 final)
- 己丑  六月十五

* Fri Jul 31 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.3.0-1mgc
- 更新至 4.3.0(KDE 4.3 try2)
- nepomukserver 仅在启用时自动启动服务(patch 4 imported from fedora project)
- 己丑  六月初十

* Sat Jul 11 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.96-2mgc
- 修正 K 帮助中心左侧树形索引中文乱码问题(patch 103 rewritten by nihui)
- 己丑  闰五月十九

* Fri Jul 10 2009 Liu Di <liudidi@gmail.com> - 4.2.96-1
- 更新到 4.2.96

* Mon Jun 29 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.95-1mgc
- 更新至 4.2.95(KDE 4.3 RC1)
- 己丑  闰五月初七

* Thu Jun 11 2009 Liu Di <liudidi@gmail.com> - 4.2.90-1
- 更新到 4.2.90 ( 4.3 beta 2)
- 已丑　五月十九

* Fri May 29 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.88-1mgc
- 更新至 4.2.88
- 己丑  五月初六

* Sat May 16 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.85-1mgc
- 更新至 4.2.85(KDE 4.3 Beta1)
- 去除 oxygen 图标主题包
- 己丑  四月廿二

* Sat Apr 4 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.2-1mgc
- 更新至 4.2.2
- %{kde4_iconsdir}/default.kde4 从主包移入 oxygen 子包
- 禁用 patch 103(need review...)
- 己丑  三月初九  [清明]

* Sun Mar 8 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.1-0.1mgc
- 更新至 4.2.1
- 己丑  二月十二

* Tue Jan 27 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.0-0.3mgc
- 注销对话框的月亮图像授权协议问题修正源码包更新(KDE 4.2 final)
- 己丑  正月初二

* Fri Jan 23 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.0-0.2mgc
- 更新 patch 102，百度/淘宝搜索可以正常工作了~~
- patch 103 need more work ....
- 戊子  十二月廿八

* Thu Jan 22 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.0-0.1mgc
- 更新至 4.2.0(KDE 4.2 try1)
- msn im 小图标支持(patch 101 ported to KDE4 by nihui)
- 速搜编码转换(patch 102 written by nihui)
- khelpcenter 左侧树形目录编码设定(patch 103 written by nihui)
- 戊子  十二月廿七

* Tue Jan 13 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.1.96-0.1mgc
- 更新至 4.1.96(KDE 4.2 RC1)
- relwithdeb 编译模式
- 戊子  十二月十八

* Fri Dec 12 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.1.85-0.1mgc
- 更新至 4.1.85(KDE 4.2 Beta2)
- 戊子  十一月十五

* Sun Nov 23 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.1.80-0.1mgc
- 更新至 4.1.80
- 戊子  十月廿六

* Sun Oct 12 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.1.69-0.1mgc
- 更新至 4.1.69
- debugfull 编译模式
- 去除 phonon-xine
- 戊子  九月十四

* Mon Sep 29 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.1.2-0.1mgc
- 更新至 4.1.2
- kde3 应用程序热插拔支持(patch 3 from opensuse project)
- 系统设置/窗口管理器切换功能(patch 6/7 from opensuse project)
- 拆出 phonon-xine 包
- 戊子  九月初一

* Fri Aug 29 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.1.1-0.1mgc
- 更新至 4.1.1-try1(内部版本)
- 戊子  七月廿九

* Thu Jul 24 2008 Liu Di <liudidi@gmail.com> - 4.1.0-0.1mgc
- 更新到 4.1.0(KDE 4.1 正式版)

* Thu Jul 10 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.98-0.1mgc
- 更新至 4.0.98(KDE 4.1 RC1)
- release 模式编译(build_type release)
- 戊子  六月初八

* Sat Jul 5 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.85-0.1mgc
- 更新至 4.0.85
- 戊子  六月初三

* Fri Jun 27 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.84-0.1mgc
- 更新至 4.0.84
- 戊子  五月廿四

* Thu Jun 19 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.83-0.1mgc
- 更新至 4.0.83-try1(第一次 tag 4.1.0-beta2 内部版本)
- 戊子  五月十六

* Wed Jun 11 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.82-0.1mgc
- 更新至 4.0.82
- 戊子  五月初八

* Wed Jun 4 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.81-0.1mgc
- 更新至 4.0.81
- 戊子  五月初一

* Fri May 23 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.80-0.1mgc
- 更新至 4.0.80(try1 内部版本)
- 戊子  四月十九

* Fri May 16 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.74-0.1mgc
- 更新至 4.0.74
- 戊子  四月十二

* Sat May 10 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.73-0.1mgc
- 更新至 4.0.73
- 戊子  四月初六

* Sun May 4 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.72-0.1mgc
- 更新至 4.0.72
- 戊子  三月廿九

* Sat Apr 26 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.71-0.1mgc
- 更新至 4.0.71
- 修正 phonon_xine 的 mrl 编码问题(patch 20)
- 戊子  三月廿一

* Sat Apr 19 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.70-0.1mgc
- 更新至 4.0.70
- 戊子  三月十四

* Sat Apr 12 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.69-0.1mgc
- 更新至 4.0.69
- 戊子  三月初七

* Mon Mar 31 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.3-0.1mgc
- 更新至 4.0.3
- 定义 kde4 路径
- 拆出 oxygen 和 devel 包
- 戊子  二月廿四

* Fri Mar 7 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.2-0.2mgc
- 更新 brunch 代码
- 关闭 verbose 编译模式(cmake_verbose_build = 0)
- 戊子  正月三十

* Sun Mar 2 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.2-0.1mgc
- 更新至 4.0.2
- 戊子  正月廿五

* Wed Feb 6 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.1-0.1mgc
- 更新至 4.0.1

* Fri Jan 18 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.0-0.2mgc
- 添加 brunch 代码更新

* Fri Jan 11 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.0-0.1mgc
- 更新至 4.0.0

* Wed Dec 12 2007 Ni Hui <shuizhuyuanluo@126.com> - 3.97.0-0.1mgc
- 更新至 3.97.0 (KDE4-RC2)
- 简化 spec 文件 %file 字段

* Sat Nov 24 2007 Ni Hui <shuizhuyuanluo@126.com> - 3.96.0-0.1mgc
- 更新至 3.96.0 (KDE4-RC1)

* Sat Oct 20 2007 Ni Hui <shuizhuyuanluo@126.com> - 3.94.0-0.1mgc
- 首次生成 rpm 包
