# svn = 0 or 1 
%define svn 0

#%define build_qtscript_generator 0

%define rversion 887026
%define real_name multimedia


Name: amarok2
Summary: Amarok - the audio player for KDE
Summary(zh_CN.UTF-8): KDE 下的媒体播放器
License: LGPL v2 or later
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
URL: http://amarok.kde.org/
Version:	2.8.0
%if %{svn}
Release: 0.svn%rversion.1%{?dist}.5
%else
Release: 4%{?dist}
%endif

%if %{svn}
Source0: %{real_name}.tar.bz2
Source1: amarok.po
%else
Source0: http://download.kde.org/stable/amarok/%{version}/src/amarok-%{version}.tar.bz2

Source1: amarok.po
%endif

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

#AutoReq: no
Requires: libkdelibs4 >= 4.0.60
Requires: taglib >= 1.6
Requires: strigi-libs >= 0.5.9
Requires: mysql-libs
Requires: mysql-embedded
Requires: loudmouth
Requires: phonon >= 4.1.83
Requires: phonon-backend%{?_isa}
Requires: libgcrypt
Requires: libgpod
Requires: libmtp

BuildRequires: libkdelibs4-devel >= 4.0.60
BuildRequires: strigi-devel >= 0.5.9
BuildRequires: xine-lib-devel >= 1.1.5
BuildRequires: qt4-devel >= 4.4.0
BuildRequires: taglib-devel >= 1.6
BuildRequires: taglib-extras
BuildRequires: ruby-devel >= 1.8.6
BuildRequires: libifp-devel >= 1.0.0.2
BuildRequires: libvisual-devel >= 0.4.0
BuildRequires: libxcb-devel >= 1.0
BuildRequires: glib2-devel >= 2.14.4
BuildRequires: automoc4 >= 0.9.83
BuildRequires: phonon-devel >= 4.1.83
BuildRequires: libnjb-devel >= 2.2.1
BuildRequires: libmtp-devel >= 0.3.0
BuildRequires: loudmouth-devel >= 1.0.0
BuildRequires: libaio-devel
BuildRequires: mysql-embedded-devel
BuildRequires: libgpod-devel

# gb18030 编码补丁
# patched by nihui, Jun. 13rd, 2008
Patch1: amarok-1.83-taglocal-fix_flac.patch
Patch2: amarok2-fix_flac_tag_decoding.patch

Patch3: amarok-2.3.0.90-improve-charset-dectection.patch

# redecode option in config dialog
Patch5: amarok-2.0-redecode_option.patch
# autodetect mp3 id3v1/id3v2 tag
Patch6: amarok-2.0-id3v1_assume_detect_encoding.patch

# libgpod 0.7 的补丁
Patch101: amarok-libgpod-0.7.0.patch

Patch800: amarok-2.2.1-enablefinal.patch

Patch10000: amarok-2.0.96-always_find_qtscriptbindings.patch
# upstream patch

%description
Amarok - the audio player for KDE

%description -l zh_CN.UTF-8.GB18030
KDE 下的媒体播放器。

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
%package -n %{name}-devel
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: Amarok - the audio player for KDE: Build Environment
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires: %{name} = %{version} libkdelibs4-devel

%description -n %{name}-devel
This package contains all necessary include files and libraries needed
to develop Amarok applications.

%description devel -l zh_CN.UTF-8.GB18030
%{name} 的开发包。

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
%package extras
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: Amarok - the audio player for KDE: Extra components
Summary(zh_CN.UTF-8): %{name} 的其它组件
Requires: %{name} = %{version}

%description extras
This package contains extra components of Amarok applications.

%prep

%if %{svn}
%setup -q -n %{real_name}
%else
%setup -q -n amarok-%{version}
%endif


#%patch3 -p1

#%patch10000 -p1
#%patch1 -p1 -b .fixtaglocal
#%if %{svn}
#pushd amarok
#%endif
#%patch2 -p1
#%patch3 -p1
#%patch4 -p0
#%if %{svn}
#popd
#%endif

#%patch5 -p1 -b .redecode_option
#%patch6 -p1 -b .id3v1_assume_detect_encoding

#%patch101 -p0

# compile fix
#%patch800 -p1

# upstream patch
# 因为多语言的原因，这里会出错，反正用处不大，删除了
rm doc -rf

%build
mkdir build
cd build
%cmake_kde4 ..

make %{?_smp_mflags}

%install
cd build
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

#%if %{svn}
#rm -fv %{buildroot}%{kde4_localedir}/zh_CN/LC_MESSAGES/amarok.mo
# 安装简体中文语言文件
#mkdir -p %{buildroot}%{kde4_localedir}/zh_CN/LC_MESSAGES
#msgfmt %{SOURCE1} -o %{buildroot}%{kde4_localedir}/zh_CN/LC_MESSAGES/amarok.mo
#%endif

magic_rpm_clean.sh

# some more cleaning
rm -rfv %{buildroot}%{kde4_localedir}/sr@*

%clean_kde4_desktop_files
%clean_kde4_notifyrc_files
%adapt_kde4_notifyrc_files

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files -n %{name}-devel
%defattr(-,root,root)
%{kde4_libdir}/*.so

%files
%defattr(-,root,root)
%{kde4_bindir}/*
%{kde4_xdgappsdir}/*.desktop
%{kde4_appsdir}
%config %{kde4_configdir}/amarok_homerc
%config %{kde4_configdir}/amarok.knsrc
%config %{kde4_configdir}/amarokapplets.knsrc
%{kde4_kcfgdir}/*.kcfg
%{kde4_dbus_interfacesdir}/org.*.xml
%{kde4_iconsdir}/hicolor/*/apps/*
%{kde4_servicesdir}/*.desktop
%{kde4_servicesdir}/ServiceMenus/*.desktop
%{kde4_servicetypesdir}/*.desktop
%{kde4_servicesdir}/*.protocol
%{kde4_libdir}/*.so.*
%{kde4_plugindir}/*.so
#%{kde4_libdir}/strigi/*
%{kde4_localedir}/*

# move to -extra package
%exclude %{kde4_bindir}/amarokmp3tunesharmonydaemon
%exclude %{kde4_plugindir}/amarok_service_ampache.so
%exclude %{kde4_plugindir}/amarok_service_jamendo.so
%exclude %{kde4_plugindir}/amarok_service_mp3tunes.so
%exclude %{kde4_plugindir}/amarok_service_opmldirectory.so
%exclude %{kde4_plugindir}/kcm_amarok_service_ampache.so
%exclude %{kde4_plugindir}/kcm_amarok_service_mp3tunes.so
%exclude %{kde4_appsdir}/amarok/icons/hicolor/*/actions/view-services-ampache-amarok.png
%exclude %{kde4_appsdir}/amarok/icons/hicolor/*/actions/view-services-jamendo-amarok.png
%exclude %{kde4_appsdir}/amarok/icons/hicolor/*/actions/view-services-librivox-amarok.png
%exclude %{kde4_appsdir}/amarok/icons/hicolor/*/actions/view-services-mp3tunes-amarok.png
%exclude %{kde4_appsdir}/amarok/icons/hicolor/*/actions/view-services-opml-amarok.png
%exclude %{kde4_appsdir}/amarok/images/emblem-ampache-scalable.svgz
%exclude %{kde4_appsdir}/amarok/images/emblem-ampache.png
%exclude %{kde4_appsdir}/amarok/images/emblem-jamendo-scalable.svgz
%exclude %{kde4_appsdir}/amarok/images/emblem-jamendo.png
%exclude %{kde4_appsdir}/amarok/images/emblem-mp3tunes.png
%exclude %{kde4_appsdir}/amarok/images/hover_info_ampache.png
%exclude %{kde4_appsdir}/amarok/images/hover_info_jamendo.png
#%exclude %{kde4_appsdir}/amarok/scripts/librivox_service
#%exclude %{kde4_appsdir}/amarok/scripts/lyrics_lyricwiki
#%exclude %{kde4_appsdir}/amarok/scripts/radio_station_service
%exclude %{kde4_servicesdir}/amarok_service_ampache.desktop
%exclude %{kde4_servicesdir}/amarok_service_ampache_config.desktop
%exclude %{kde4_servicesdir}/amarok_service_jamendo.desktop
%exclude %{kde4_servicesdir}/amarok_service_mp3tunes.desktop
%exclude %{kde4_servicesdir}/amarok_service_mp3tunes_config.desktop
%exclude %{kde4_servicesdir}/amarok_service_opmldirectory.desktop


%files extras
%defattr(-,root,root)
%{kde4_bindir}/amarokmp3tunesharmonydaemon
%{kde4_plugindir}/amarok_service_ampache.so
%{kde4_plugindir}/amarok_service_jamendo.so
%{kde4_plugindir}/amarok_service_mp3tunes.so
%{kde4_plugindir}/amarok_service_opmldirectory.so
%{kde4_plugindir}/kcm_amarok_service_ampache.so
%{kde4_plugindir}/kcm_amarok_service_mp3tunes.so
%{kde4_appsdir}/amarok/icons/hicolor/*/actions/view-services-ampache-amarok.png
%{kde4_appsdir}/amarok/icons/hicolor/*/actions/view-services-jamendo-amarok.png
%{kde4_appsdir}/amarok/icons/hicolor/*/actions/view-services-librivox-amarok.png
%{kde4_appsdir}/amarok/icons/hicolor/*/actions/view-services-mp3tunes-amarok.png
%{kde4_appsdir}/amarok/icons/hicolor/*/actions/view-services-opml-amarok.png
%{kde4_appsdir}/amarok/images/emblem-ampache-scalable.svgz
%{kde4_appsdir}/amarok/images/emblem-ampache.png
%{kde4_appsdir}/amarok/images/emblem-jamendo-scalable.svgz
%{kde4_appsdir}/amarok/images/emblem-jamendo.png
%{kde4_appsdir}/amarok/images/emblem-mp3tunes.png
%{kde4_appsdir}/amarok/images/hover_info_ampache.png
%{kde4_appsdir}/amarok/images/hover_info_jamendo.png
#%{kde4_appsdir}/amarok/scripts/librivox_service
#%{kde4_appsdir}/amarok/scripts/lyrics_lyricwiki
#%{kde4_appsdir}/amarok/scripts/radio_station_service
%{kde4_servicesdir}/amarok_service_ampache.desktop
%{kde4_servicesdir}/amarok_service_ampache_config.desktop
%{kde4_servicesdir}/amarok_service_jamendo.desktop
%{kde4_servicesdir}/amarok_service_mp3tunes.desktop
%{kde4_servicesdir}/amarok_service_mp3tunes_config.desktop
%{kde4_servicesdir}/amarok_service_opmldirectory.desktop
%{kde4_datadir}/mime/packages/amzdownloader.xml

%changelog
* Thu Feb 27 2014 Liu Di <liudidi@gmail.com> - 2.8.0-3
- 更新到 2.8.0

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 2.6.0-3
- 为 Magic 3.0 重建

* Tue Dec 04 2012 Liu Di <liudidi@gmail.com> - 2.6.0-3
- 为 Magic 3.0 重建

* Tue Dec 04 2012 Liu Di <liudidi@gmail.com> - 2.6.0-3
- 为 Magic 3.0 重建

* Tue Oct 30 2012 Liu Di <liudidi@gmail.com> - 2.6.0-2
- 为 Magic 3.0 重建

* Tue Oct 30 2012 Liu Di <liudidi@gmail.com> - 2.6.0-2
- 为 Magic 3.0 重建

* Sat May 23 2009 Ni Hui <shuizhuyuanluo@126.com> - 2.0.96-1mgc
- 更新至 2.0.96
- 己丑  四月廿九

* Thu Jan 15 2009 Ni Hui <shuizhuyuanluo@126.com> - 2.0.1.1-0.1mgc
- 更新至 2.0.1.1
- build_qtscript_generator 开关关闭
- 戊子  十二月二十

* Thu Jan 1 2009 Ni Hui <shuizhuyuanluo@126.com> - 2.0-0.1mgc
- 更新至 2.0 正式版
- redecode option(patch 5 written by nihui)(unused)
- 自动探测 mp3 id3v1/id3v2 tag (patch 6 written by nihui)
- 修复更改 tag 导致崩溃的 bug(patch 1000 from upstream)
- 戊子  十二月初六

* Sat Nov 29 2008 Ni Hui <shuizhuyuanluo@126.com> - 1.98-0.svn887026.1mgc
- 更新至 1.98(amarok2-rc1)
- %{kde4_libdir}/libamarok_service_liblastfm.so 分包问题修复
- 去除编译依赖 kdemultimedia4-devel
- 戊子  十一月初二

* Fri Nov 07 2008 Ni Hui <shuizhuyuanluo@126.com> - 1.94-0.svn878209.1mgc
- 更新至 1.94(amarok2-beta3)
- 收藏扫描媒体 tag 编码探测补丁(patch 3 updated by nihui, accepted by upstream)
- mysql 动态链接库编译补丁(patch 4 updated by nihui, accepted by upstream)
- 戊子  十月初十  [立冬]

* Fri Oct 10 2008 Ni Hui <shuizhuyuanluo@126.com> - 1.92.2-0.svn867426.1mgc
- 更新至 1.92.2(amarok2-beta2-fix)
- 戊子  九月十二

* Wed Oct 1 2008 Ni Hui <shuizhuyuanluo@126.com> - 1.92-0.svn866488.1mgc
- 更新至 svn 866488
- 中文化语言文件
- 戊子  九月初三

* Tue Sep 30 2008 Ni Hui <shuizhuyuanluo@126.com> - 1.92-0.svn865043.1mgc
- 更新至 1.92(amarok2-beta2)
- 纳入语言包
- autoreq: no
- 戊子  九月初二

* Sat Sep 20 2008 Ni Hui <shuizhuyuanluo@126.com> - 1.90-1.svn862833.1mgc
- 更新至 svn 862833
- 收藏扫描媒体 tag 编码探测补丁(patch 3 written by nihui, unused)
- 戊子  八月廿一

* Fri Sep 12 2008 Ni Hui <shuizhuyuanluo@126.com> - 1.90-0.1mgc
- 更新至 1.90
- 重写编码补丁，修正 flac 文件 utf8 默认编码问题(patch 2 written by nihui)
- 戊子  八月十三

* Mon Jul 14 2008 Ni Hui <shuizhuyuanluo@126.com> - 1.83-0.svn832047.1mgc
- 更新至 svn 832047
- 纳入所有依赖关系
- 戊子  六月十二

* Fri Jul 11 2008 Ni Hui <shuizhuyuanluo@126.com> - 1.83-0.svn830731.1mgc
- 去除 patch 1(peterzl 已经把 mozilla 的 chardet 并入 amarok 中)
- 戊子  六月初九

* Thu Jul 10 2008 Ni Hui <shuizhuyuanluo@126.com> - 1.83-0.1mgc
- 更新至 1.83
- 重写编码补丁，修正 flac 文件 utf8 默认编码问题
- 戊子  六月初八

* Fri Jun 13 2008 Ni Hui <shuizhuyuanluo@126.com> - 1.80-0.svn815021.2mgc
- 修正 tag 乱码问题(patch 1 written by nihui)
- 戊子  五月初十

* Sun Jun 1 2008 Ni Hui <shuizhuyuanluo@126.com> - 1.80-0.svn815021.1mgc
- 更新至 1.80-svn815021
- 定义 kde4 路径
- 戊子  四月廿七

* Sat Jan 19 2008 Ni Hui <shuizhuyuanluo@126.com> - 0.0.svn762058-0.1mgc
- 首次生成 rpm 包
