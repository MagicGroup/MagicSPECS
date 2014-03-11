%define rversion %{kde4_kdelibs_version}
%define release_number 1
%define real_name kde-baseapps


Name: kdebase4
Summary: The KDE Base Components
Summary(zh_CN.UTF-8): K 桌面环境的基本组件
License: GPL v2 or later
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
URL: http://www.kde.org/
Version: %{rversion}
Release: %{release_number}%{?dist}
Source0: http://mirror.bjtu.edu.cn/kde/stable/%{rversion}/src/%{real_name}-%{rversion}.tar.xz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires: kdebase4-runtime >= %{version}
BuildRequires: libkdelibs4-devel
BuildRequires: libkdepimlibs4-devel
BuildRequires: qimageblitz-devel >= 0.0.4
BuildRequires: libxklavier-devel
BuildRequires: soprano-devel >= 2.3.0
BuildRequires: strigi-devel >= 0.6.3
BuildRequires: qt4-devel >= 4.4.3
BuildRequires: automoc4 >= 0.9.87
BuildRequires: kdebase4-workspace-devel >= 4.2.80
BuildRequires: nepomuk-widgets-devel 

Patch600: dolphin-defaults.diff
Patch601: dolphin-go_up.diff

# dolphin 信息栏 mp3 id3v1 元数据编码转换
# 双击 konqueror 标签关闭当前标签页
Patch102: kdebase-4.10.3-konqueror-doubleclick_close_tab.patch

# fedora patches
## upstreamable patches
# search path for plugins
Patch0: kdebase-4.1.80-nsplugins-paths.patch

# fix disabling automatic spell checking in the Konqueror UI (kde#228593)
Patch3: kdebase-4.4.0-konqueror-kde#228593.patch

# Password & User account becomes non responding
Patch4: kdebase-4.3.4-bz#609039-chfn-parse.patch

# add x-scheme-handler/http for konqueror so it can be set
# as default browser in GNOME
Patch5: kde-baseapps-4.9.2-konqueror-mimetyp.patch

# upstream patches

%description
This package contains the basic packages for a K Desktop Environment
workspace.

%description -l zh_CN.UTF-8
K 桌面环境的基本包。

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
%package devel
Summary: The KDE Base Components: Build Environment
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Requires: kdebase4 >= %{version}

%description devel
This package contains all necessary include files and libraries needed
to develop applications that require these.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
%package konqueror
Summary: The KDE web browser
Summary(zh_CN.UTF-8): KDE 网页浏览器
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Requires: kdebase4-runtime >= %{version}

%description konqueror
konqueror.

%description konqueror -l zh_CN.UTF-8
konqueror。

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
%package -n kcm_kio
Summary: KIO kcontrol module
Summary(zh_CN.UTF-8): KIO 控制中心模块
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Requires: kdebase4-runtime >= %{version}

%description -n kcm_kio
KIO kcontrol module.

%description -n kcm_kio -l zh_CN.UTF-8
KIO 控制中心模块。

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
%package -n kcm_kurifilt
Summary: kurifilt kcontrol module
Summary(zh_CN.UTF-8): 速搜控制中心模块
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Requires: kdebase4-runtime >= %{version}

%description -n kcm_kurifilt
kurifilt kcontrol module.

%description -n kcm_kurifilt -l zh_CN.UTF-8
速搜控制中心模块。

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
%package -n kcm_konqhtml
Summary: KHTML kcontrol module
Summary(zh_CN.UTF-8): KHTML 控制中心模块
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Requires: kdebase4-runtime >= %{version}

%description -n kcm_konqhtml
KHTML kcontrol module.

%description -n kcm_konqhtml -l zh_CN.UTF-8
KHTML 控制中心模块。

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
%package keditbookmarks
Summary: KDE bookmark editor
Summary(zh_CN.UTF-8): KDE 书签编辑器
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Requires: kdebase4-runtime >= %{version}

%description keditbookmarks
KDE bookmark editor.

%description keditbookmarks -l zh_CN.UTF-8
KDE 书签编辑器。

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
%package nsplugin
Summary: The KDE web browser Netscape Plugin support
Summary(zh_CN.UTF-8): KDE 网页浏览器 Netscape 插件支持
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Requires: kdebase4-runtime >= %{version}

%description nsplugin
The KDE web browser Netscape Plugin support.

%description nsplugin -l zh_CN.UTF-8
KDE 网页浏览器 Netscape 插件支持。

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
%prep
%setup -q -n %{real_name}-%{rversion}


%patch600 -p1
%patch601 -p1

%patch102 -p1

%patch0 -p2 -b .nsplugins-paths
%patch3 -p2 -b .kde#228593
#%patch4 -p2 -b .bz#631481
%patch5 -p1 -b .mimetyp.patch

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
for f in konqueror dolphin ; do
   bunzip2 %{buildroot}%{_kde4_docdir}/HTML/en/$f/index.cache.bz2
   sed -i -e 's!name="id[a-z]*[0-9]*"!!g' %{buildroot}%{_kde4_docdir}/HTML/en/$f/index.cache
   sed -i -e 's!#id[a-z]*[0-9]*"!!g' %{buildroot}%{_kde4_docdir}/HTML/en/$f/index.cache
   bzip2 -9 %{buildroot}%{_kde4_docdir}/HTML/en/$f/index.cache
done

## unpackaged files
# libs for which there is no (public) api
rm -f %{buildroot}%{_libdir}/lib{dolphin,kbookmarkmodel_,konqueror}private.so

magic_rpm_clean.sh
%clean_kde4_desktop_files

# 不进行菜单处理
#  mkdir -p $RPM_BUILD_ROOT/etc/xdg/menus
#  mv $RPM_BUILD_ROOT/opt/kde4/etc/xdg/menus/kde-information.menu $RPM_BUILD_ROOT/etc/xdg/menus/kde4-information.menu
#  mv $RPM_BUILD_ROOT/opt/kde4/etc/xdg/menus/kde-kcontrol.menu $RPM_BUILD_ROOT/etc/xdg/menus/kde4-kcontrol.menu
#  mv $RPM_BUILD_ROOT/opt/kde4/etc/xdg/menus/kde-settings.menu $RPM_BUILD_ROOT/etc/xdg/menus/kde4-settings.menu

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post konqueror -p /sbin/ldconfig
%postun konqueror -p /sbin/ldconfig

%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files devel
%defattr(-,root,root)
%{kde4_includedir}/*
%{kde4_libdir}/*.so
%exclude %{kde4_libdir}/libkdeinit4_*.so

# konqueror sub package
%exclude %{kde4_includedir}/konqsidebarplugin.h
%exclude %{kde4_libdir}/libkonqsidebarplugin.so

%files konqueror
%defattr(-,root,root)
%{kde4_includedir}/konqsidebarplugin.h
%{kde4_bindir}/kfmclient
%{kde4_bindir}/konqueror
%{kde4_plugindir}/kcm_history.so
%{kde4_plugindir}/kcm_konq.so
%{kde4_plugindir}/kcm_performance.so
%{kde4_plugindir}/kded_konqy_preloader.so
%{kde4_plugindir}/khtmlkttsdplugin.so
%{kde4_plugindir}/konq_aboutpage.so
%{kde4_plugindir}/konq_shellcmdplugin.so
%{kde4_plugindir}/konq_sidebar.so
%{kde4_plugindir}/konqsidebar_places.so
%{kde4_plugindir}/konq_sidebartree_bookmarks.so
%{kde4_plugindir}/konq_sidebartree_dirtree.so
%{kde4_plugindir}/konq_sound.so
%{kde4_plugindir}/konqsidebar_history.so
%{kde4_plugindir}/konqsidebar_tree.so
%{kde4_plugindir}/konqsidebar_web.so
%{kde4_libdir}/libkdeinit4_kfmclient.so
%{kde4_libdir}/libkdeinit4_konqueror.so
%{kde4_libdir}/libkonqsidebarplugin.so
%{kde4_libdir}/libkonqsidebarplugin.so.*
%{kde4_libdir}/libkonquerorprivate.so.*
%{kde4_xdgappsdir}/Home.desktop
%{kde4_xdgappsdir}/kfmclient*.desktop
%{kde4_xdgappsdir}/konqbrowser.desktop
%{kde4_xdgappsdir}/konquerorsu.desktop
%{kde4_appsdir}/dolphinpart/kpartplugins/kshellcmdplugin.desktop
%{kde4_appsdir}/dolphinpart/kpartplugins/kshellcmdplugin.rc
%{kde4_appsdir}/kcmcss/template.css
%{kde4_appsdir}/kcontrol/pics/onlyone.png
%{kde4_appsdir}/kcontrol/pics/overlapping.png
%{kde4_appsdir}/khtml/kpartplugins/khtmlkttsd.*
%{kde4_appsdir}/konqsidebartng/*
%{kde4_appsdir}/konqueror/*
#%{kde4_appsdir}/webkitpart/kpartplugins/khtmlkttsd.*
%{kde4_kcfgdir}/konqueror.kcfg
%{kde4_datadir}/autostart/konqy_preload.desktop
%config %{kde4_configdir}/konqsidebartngrc
%{kde4_dbus_interfacesdir}/org.kde.Konqueror.*.xml
%{kde4_dbus_interfacesdir}/org.kde.konqueror.*.xml
%{kde4_iconsdir}/hicolor/*/apps/konqueror.*
#%{kde4_servicesdir}/desktoppath.desktop
%{kde4_servicesdir}/filebehavior.desktop
%{kde4_servicesdir}/kcmhistory.desktop
%{kde4_servicesdir}/kcmperformance.desktop
%{kde4_servicesdir}/kcmkonqyperformance.desktop
%{kde4_servicesdir}/kded/konqy_preloader.desktop
%{kde4_servicesdir}/konq_aboutpage.desktop
%{kde4_servicesdir}/konq_sidebartng.desktop
%{kde4_servicesdir}/konqueror.desktop
%{kde4_servicetypesdir}/konqaboutpage.desktop
%doc %lang(en) %{kde4_htmldir}/en/konqueror

%files -n kcm_kio
%defattr(-,root,root)
%{kde4_plugindir}/kcm_kio.so
%{kde4_servicesdir}/bookmarks.desktop
%{kde4_servicesdir}/cache.desktop
%{kde4_servicesdir}/cookies.desktop
%{kde4_servicesdir}/proxy.desktop
%{kde4_servicesdir}/smb.desktop
#%{kde4_servicesdir}/lanbrowser.desktop
%{kde4_servicesdir}/netpref.desktop
%{kde4_servicesdir}/useragent.desktop
%{kde4_servicesdir}/useragentstrings/*.desktop
%{kde4_servicetypesdir}/uasprovider.desktop

%files -n kcm_kurifilt
%defattr(-,root,root)
%{kde4_plugindir}/kcm_kurifilt.so
%{kde4_servicesdir}/ebrowsing.desktop

%files -n kcm_konqhtml
%defattr(-,root,root)
%{kde4_plugindir}/kcm_konqhtml.so
%{kde4_servicesdir}/khtml_appearance.desktop
%{kde4_servicesdir}/khtml_behavior.desktop
%{kde4_servicesdir}/khtml_filter.desktop
%{kde4_servicesdir}/khtml_general.desktop
%{kde4_servicesdir}/khtml_java_js.desktop

%files keditbookmarks
%defattr(-,root,root)
%{kde4_bindir}/kbookmarkmerger
%{kde4_bindir}/keditbookmarks
%{kde4_libdir}/libkdeinit4_keditbookmarks.so
%{kde4_libdir}/libkbookmarkmodel_private.so.*
%{kde4_kcfgdir}/keditbookmarks.kcfg
%{kde4_appsdir}/keditbookmarks/*
%{kde4_mandir}/man1/kbookmarkmerger.1*

%files nsplugin
%defattr(-,root,root)
%{kde4_bindir}/nspluginscan
%{kde4_bindir}/nspluginviewer
%{kde4_plugindir}/libkcminit_nsplugins.so
%{kde4_plugindir}/libnsplugin.so
#%{kde4_appsdir}/plugin/nspluginpart.rc
%{kde4_dbus_interfacesdir}/org.kde.nsplugins.*.xml
%{kde4_servicesdir}/khtml_plugins.desktop

%files
%defattr(-,root,root)
%{kde4_bindir}/*
%{kde4_plugindir}/*.so
%{kde4_libdir}/*.so.*
%{kde4_libdir}/libkdeinit4_*.so
%{kde4_xdgappsdir}/*
%{kde4_appsdir}/*
%{kde4_configdir}/translaterc
%dir %{kde4_datadir}/autostart
# dolphin config file
%config %{kde4_configdir}/servicemenu.knsrc
%{kde4_datadir}/autostart/*.desktop
%{kde4_kcfgdir}/*.kcfg
%{kde4_dbus_interfacesdir}/org.kde.*.xml
%{kde4_iconsdir}/hicolor/*/*/*
%{kde4_iconsdir}/oxygen
%{kde4_servicesdir}/*
%{kde4_servicetypesdir}/*
%doc %lang(en) %{kde4_htmldir}/en/*
%{kde4_mandir}/man1/*
# 一些模板
%{kde4_datadir}/templates

# konqueror sub package
%exclude %{kde4_bindir}/kfmclient
%exclude %{kde4_bindir}/konqueror
%exclude %{kde4_plugindir}/kcm_history.so
%exclude %{kde4_plugindir}/kcm_kio.so
%exclude %{kde4_plugindir}/kcm_konqhtml.so
%exclude %{kde4_plugindir}/kcm_konq.so
%exclude %{kde4_plugindir}/kcm_kurifilt.so
%exclude %{kde4_plugindir}/kcm_performance.so
%exclude %{kde4_plugindir}/kded_konqy_preloader.so
%exclude %{kde4_plugindir}/khtmlkttsdplugin.so
%exclude %{kde4_plugindir}/konq_aboutpage.so
%exclude %{kde4_plugindir}/konq_shellcmdplugin.so
%exclude %{kde4_plugindir}/konq_sidebar.so
%exclude %{kde4_plugindir}/konqsidebar_places.so
%exclude %{kde4_plugindir}/konq_sidebartree_bookmarks.so
%exclude %{kde4_plugindir}/konq_sidebartree_dirtree.so
%exclude %{kde4_plugindir}/konq_sound.so
%exclude %{kde4_plugindir}/konqsidebar_history.so
%exclude %{kde4_plugindir}/konqsidebar_tree.so
%exclude %{kde4_plugindir}/konqsidebar_web.so
%exclude %{kde4_libdir}/libkdeinit4_kfmclient.so
%exclude %{kde4_libdir}/libkdeinit4_konqueror.so
%exclude %{kde4_libdir}/libkonqsidebarplugin.so.*
%exclude %{kde4_libdir}/libkonquerorprivate.so.*
%exclude %{kde4_xdgappsdir}/Home.desktop
%exclude %{kde4_xdgappsdir}/kfmclient*.desktop
%exclude %{kde4_xdgappsdir}/konqbrowser.desktop
%exclude %{kde4_xdgappsdir}/konquerorsu.desktop
%exclude %{kde4_appsdir}/dolphinpart/kpartplugins/kshellcmdplugin.desktop
%exclude %{kde4_appsdir}/dolphinpart/kpartplugins/kshellcmdplugin.rc
%exclude %{kde4_appsdir}/kcmcss/template.css
%exclude %{kde4_appsdir}/kcontrol/pics/onlyone.png
%exclude %{kde4_appsdir}/kcontrol/pics/overlapping.png
%exclude %{kde4_appsdir}/khtml/kpartplugins/khtmlkttsd.*
%exclude %{kde4_appsdir}/konqsidebartng/*
%exclude %{kde4_appsdir}/konqueror/*
#%exclude %{kde4_appsdir}/webkitpart/kpartplugins/khtmlkttsd.*
%exclude %{kde4_kcfgdir}/konqueror.kcfg
%exclude %{kde4_datadir}/autostart/konqy_preload.desktop
%exclude %config %{kde4_configdir}/konqsidebartngrc
%exclude %{kde4_dbus_interfacesdir}/org.kde.Konqueror.*.xml
%exclude %{kde4_dbus_interfacesdir}/org.kde.konqueror.*.xml
%exclude %{kde4_iconsdir}/hicolor/*/apps/konqueror.*
%exclude %{kde4_servicesdir}/bookmarks.desktop
%exclude %{kde4_servicesdir}/cache.desktop
%exclude %{kde4_servicesdir}/cookies.desktop
#%exclude %{kde4_servicesdir}/desktoppath.desktop
%exclude %{kde4_servicesdir}/ebrowsing.desktop
%exclude %{kde4_servicesdir}/filebehavior.desktop
%exclude %{kde4_servicesdir}/kcmhistory.desktop
%exclude %{kde4_servicesdir}/kcmkonqyperformance.desktop
%exclude %{kde4_servicesdir}/kcmperformance.desktop
%exclude %{kde4_servicesdir}/kded/konqy_preloader.desktop
%exclude %{kde4_servicesdir}/khtml_appearance.desktop
%exclude %{kde4_servicesdir}/khtml_behavior.desktop
%exclude %{kde4_servicesdir}/khtml_filter.desktop
%exclude %{kde4_servicesdir}/khtml_general.desktop
%exclude %{kde4_servicesdir}/khtml_java_js.desktop
%exclude %{kde4_servicesdir}/konq_aboutpage.desktop
%exclude %{kde4_servicesdir}/konq_sidebartng.desktop
%exclude %{kde4_servicesdir}/konqueror.desktop
#%exclude %{kde4_servicesdir}/lanbrowser.desktop
%exclude %{kde4_servicesdir}/netpref.desktop
%exclude %{kde4_servicesdir}/proxy.desktop
%exclude %{kde4_servicesdir}/smb.desktop
%exclude %{kde4_servicesdir}/useragent.desktop
%exclude %{kde4_servicesdir}/useragentstrings/*.desktop
%exclude %{kde4_servicetypesdir}/konqaboutpage.desktop
%exclude %{kde4_servicetypesdir}/uasprovider.desktop
%exclude %{kde4_htmldir}/en/konqueror

# keditbookmarks sub package
%exclude %{kde4_bindir}/kbookmarkmerger
%exclude %{kde4_bindir}/keditbookmarks
%exclude %{kde4_libdir}/libkdeinit4_keditbookmarks.so
%exclude %{kde4_libdir}/libkbookmarkmodel_private.so.*
%exclude %{kde4_kcfgdir}/keditbookmarks.kcfg
%exclude %{kde4_appsdir}/keditbookmarks/*
%exclude %{kde4_mandir}/man1/kbookmarkmerger.1*

# nsplugin sub package
%exclude %{kde4_bindir}/nspluginscan
%exclude %{kde4_bindir}/nspluginviewer
%exclude %{kde4_plugindir}/libkcminit_nsplugins.so
%exclude %{kde4_plugindir}/libnsplugin.so
#%exclude %{kde4_appsdir}/plugin/nspluginpart.rc
%exclude %{kde4_dbus_interfacesdir}/org.kde.nsplugins.*.xml
%exclude %{kde4_servicesdir}/khtml_plugins.desktop


%changelog
* Mon Dec 28 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.3.4-2mgc
- 拆出 konqueror/keditbookmarks/nsplugin
- 乙丑  十一月十三

* Sat Dec 5 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.3.4-1mgc
- 更新至 4.3.4
- 乙丑  十月十九

* Sun Aug 2 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.3.0-1mgc
- 更新至 4.3.0
- 更改默认的 konsole 终端字体(patch 103 written by nihui)
- 己丑  六月十二

* Sat Jul 11 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.96-2mgc
- 双击 konqueror 标签关闭当前标签页(patch 102 ported by nihui)
- 己丑  闰五月十九

* Fri Jul 10 2009 Liu Di <liudidi@gmail.com> - 4.2.96-1
- 更新到 4.2.96

* Mon Jun 29 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.95-1mgc
- 更新至 4.2.95(KDE 4.3 RC1)
- 己丑  闰五月初七

* Sat Jun 13 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.91-2mgc
- 修正文件分包问题
- 己丑  五月廿一

* Thu Jun 11 2009 Liu Di <liudidi@gmail.com> - 4.2.90-1
- 更新到 4.2.90 ( 4.3 beta2 )
- 已丑　五月十九

* Fri May 29 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.88-1mgc
- 更新至 4.2.88
- 己丑  五月初六

* Sat May 16 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.85-1mgc
- 更新至 4.2.85(KDE 4.3 beta1)
- 己丑  四月廿二

* Sat Apr 4 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.2-1mgc
- 更新至 4.2.2
- 禁用 patch 101(need review...)
- 己丑  三月初九  [清明]

* Sat Mar 14 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.1-0.1mgc
- 更新至 4.2.1
- apply patch to fix regression in konsole, double-click selection works again
- apply patch to fix regression in konsole, layout regression affecting apps using the KPart
- 己丑  二月十八

* Thu Jan 22 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.0-0.1mgc
- 更新至 4.2.0(KDE 4.2 try1)
- dolphin 信息栏 mp3 id3v1 元数据编码转换(patch 101 written by nihui)
- 戊子  十二月廿七

* Wed Jan 14 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.1.96-0.1mgc
- 更新至 4.1.96(KDE 4.2 RC1)
- relwithdeb 编译模式
- 戊子  十二月十九

* Fri Dec 12 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.1.85-0.1mgc
- 更新至 4.1.85(KDE 4.2 Beta2)
- 戊子  十一月十五

* Sun Nov 23 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.1.80-0.1mgc
- 更新至 4.1.80
- %with_webkitkde 开关
- 戊子  十月廿六

* Sun Oct 12 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.1.69-0.1mgc
- 更新至 4.1.69
- debugfull 编译模式
- 戊子  九月十四

* Mon Sep 29 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.1.2-0.1mgc
- 更新至 4.1.2
- 重新引入 webkit 支持
- 戊子  九月初一

* Fri Aug 29 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.1.1-0.1mgc
- 更新至 4.1.1-try1(内部版本)
- 去除编译依赖 kde4-webkitkde
- 戊子  七月廿九

* Thu Jul 24 2008 Liu Di <liudidi@gmail.com> - 4.1.0-0.1mgc
- 更新到 4.1.0(KDE 4.1 正式版)

* Thu Jul 10 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.98-0.1mgc
- 更新至 4.0.98(KDE 4.1 RC1)
- release 模式编译(build_type release)
- 修正 konsole 主菜单项快捷键翻译问题
- 戊子  六月初八

* Sat Jul 5 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.85-0.1mgc
- 更新至 4.0.85
- 戊子  六月初三

* Fri Jun 27 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.84-0.1mgc
- 更新至 4.0.84
- 纳入 webkit 支持
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
- 戊子  二月廿四

* Sat Mar 8 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.2-0.2mgc
- 更新 brunch 代码
- 关闭 verbose 编译模式(cmake_verbose_build = 0)
- 戊子  二月初一

* Sun Mar 2 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.2-0.1mgc
- 更新至 4.0.2
- 戊子  正月廿五

* Wed Feb 6 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.1-0.1mgc
- 更新至 4.0.1

* Fri Jan 18 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.0-0.2mgc
- 更新 brunch 代码补丁

* Fri Jan 11 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.0-0.1mgc
- 更新至 4.0.0

* Wed Dec 12 2007 Ni Hui <shuizhuyuanluo@126.com> - 3.97.0-0.1mgc
- 更新至 3.97.0 (KDE4-RC2)
- 简化 spec 文件 %file 字段

* Sat Nov 24 2007 Ni Hui <shuizhuyuanluo@126.com> - 3.96.0-0.1mgc
- 更新至 3.96.0 (KDE4-RC1)

* Sat Oct 20 2007 Ni Hui <shuizhuyuanluo@126.com> - 3.94.0-0.1mgc
- 首次生成 rpm 包
