%define rversion %{kde4_kdelibs_version}
%define release_number 1
%define real_name kdemultimedia


Name: kdemultimedia4
Summary: The KDE Multimedia Components
Summary(zh_CN.UTF-8): KDE 多媒体组件
License: LGPL v2 or later
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
URL: http://www.kde.org/
Version: %{rversion}
Release: %{release_number}%{?dist}
Source0: http://mirror.bjtu.edu.cn/kde/stable/%{rversion}/src/%{real_name}-%{rversion}.tar.xz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: libkdelibs4-devel
BuildRequires: taglib-devel >= 1.5
BuildRequires: libogg-devel
BuildRequires: libmusicbrainz-devel
BuildRequires: libtunepimp-devel
BuildRequires: cdparanoia-devel
BuildRequires: flac-devel
BuildRequires: ffmpeg-devel

Requires: %{name}-juk = %{version}
Requires: %{name}-kmix = %{version}
Requires: %{name}-kscd = %{version}
Requires: %{name}-libkcddb = %{version}
Requires: %{name}-libkcompactdisc = %{version}
Requires: %{name}-kioslave_audiocd = %{version}
Requires: %{name}-dragonplayer = %{version}
Requires: %{name}-mplayerthumbs = %{version}
Requires: %{name}-ffmpegthumbs = %{version}

#Patch1: kdemultimedia-4.0.1-768945_to_772637.diff

# juk mp3 编码补丁
# patch rewritten by nihui, Jul.5th, 2008
Patch11: kdemultimedia-4.3.95-juk-detect_mp3_tag_charset.patch
# 缩小 kmix 主窗口和停靠部件的留白边距
# patch 12 written by nihui, Aug.30th, 2010
Patch12: kdemultimedia-4.5.0-kmix-shrink-layout.patch

%description
The KDE Multimedia Components.

%description -l zh_CN.UTF-8
KDE 多媒体组件。

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- 开发包
%package -n %{name}-devel
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: KDE Multimedia Libraries: Build Environment
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires: libkdelibs4-devel
Requires: %{name} = %{version}

%description -n %{name}-devel
This package contains all necessary include files and libraries needed
to develop KDE Multimedia applications.

%description -n %{name}-devel -l zh_CN.UTF-8
%{name} 的开发包。

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- juk
%package -n %{name}-juk
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: juk

%description -n %{name}-juk
juk.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- kmix
%package -n %{name}-kmix
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: kmix

%description -n %{name}-kmix
kmix.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- kscd
%package -n %{name}-kscd
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: kscd

%description -n %{name}-kscd
kscd.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- libkcddb
%package -n %{name}-libkcddb
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: libkcddb

%description -n %{name}-libkcddb
libkcddb.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- libkcompactdisc
%package -n %{name}-libkcompactdisc
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: libkcompactdisc

%description -n %{name}-libkcompactdisc
libkcompactdisc.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- kioslave_audiocd
%package -n %{name}-kioslave_audiocd
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: kioslave_audiocd

%description -n %{name}-kioslave_audiocd
kioslave_audiocd.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- dragonplayer
%package -n %{name}-dragonplayer
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: dragonplayer

%description -n %{name}-dragonplayer
dragonplayer.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- mplayerthumbs
%package -n %{name}-mplayerthumbs
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: mplayerthumbs

%description -n %{name}-mplayerthumbs
mplayerthumbs.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- ffmpegthumbs
%package -n %{name}-ffmpegthumbs
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: ffmpegthumbs

%description -n %{name}-ffmpegthumbs
ffmpegthumbs.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
%prep
%setup -q -n %{real_name}-%{rversion}

%patch11 -p1 -b .orig
#%patch12 -p1 -b .kmix_shrink

%build
mkdir build
cd build
%cmake_kde4 ..

make %{?_smp_mflags}

%install
cd build
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

%clean_kde4_desktop_files
%clean_kde4_notifyrc_files
%adapt_kde4_notifyrc_files
magic_rpm_clean.sh

%post -n %{name}-kmix -p /sbin/ldconfig
%postun -n %{name}-kmix -p /sbin/ldconfig

%post -n %{name}-libkcddb -p /sbin/ldconfig
%postun -n %{name}-libkcddb -p /sbin/ldconfig

%post -n %{name}-libkcompactdisc -p /sbin/ldconfig
%postun -n %{name}-libkcompactdisc -p /sbin/ldconfig

%post -n %{name}-kioslave_audiocd -p /sbin/ldconfig
%postun -n %{name}-kioslave_audiocd -p /sbin/ldconfig

%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files -n %{name}-devel
%defattr(-,root,root)
%{kde4_includedir}/*
%{kde4_libdir}/*.so
%exclude %{kde4_libdir}/libkdeinit4_kmix*.so

%files
%defattr(-,root,root)
%doc COPYING COPYING.LIB

%files -n %{name}-juk
%defattr(-,root,root)
%{kde4_bindir}/juk
%{kde4_appsdir}/juk/*
%{kde4_dbus_interfacesdir}/org.kde.juk.*.xml
%{kde4_iconsdir}/hicolor/*/apps/juk.*
%{kde4_xdgappsdir}/juk.desktop
%{kde4_servicesdir}/ServiceMenus/jukservicemenu.desktop
%doc %lang(en) %{kde4_htmldir}/en/juk

%files -n %{name}-kmix
%defattr(-,root,root)
%{kde4_bindir}/kmix*
%{kde4_libdir}/libkdeinit4_kmix*.so
%{kde4_appsdir}/kmix/*
%{kde4_datadir}/autostart/restore_kmix_volumes.desktop
%{kde4_datadir}/autostart/kmix_autostart.desktop
#%{kde4_dbus_interfacesdir}/org.kde.KMix.xml
%{kde4_iconsdir}/hicolor/*/apps/kmix.*
%{kde4_xdgappsdir}/kmix.desktop
%{kde4_servicesdir}/kmixctrl_restore.desktop
%{kde4_plugindir}/kded_kmixd.so
%{kde4_plugindir}/plasma_engine_mixer.so
%{kde4_appsdir}/plasma/services/mixer.operations
%{kde4_servicesdir}/kded/kmixd.desktop
%{kde4_servicesdir}/plasma-engine-mixer.desktop
%{kde4_dbus_interfacesdir}/org.kde.kmix.control.xml
%{kde4_dbus_interfacesdir}/org.kde.kmix.mixer.xml
%{kde4_dbus_interfacesdir}/org.kde.kmix.mixset.xml
%doc %lang(en) %{kde4_htmldir}/en/kmix

%files -n %{name}-kscd
%defattr(-,root,root)
%{kde4_bindir}/kscd
%{kde4_appsdir}/kscd/*
%{kde4_kcfgdir}/kscd.kcfg
%{kde4_dbus_interfacesdir}/org.kde.kscd.*.xml
%{kde4_iconsdir}/hicolor/*/apps/kscd.*
%{kde4_iconsdir}/oxygen/*/actions/kscd-dock.*
%{kde4_xdgappsdir}/kscd.desktop
%doc %lang(en) %{kde4_htmldir}/en/kcontrol/cddbretrieval

%files -n %{name}-libkcddb
%defattr(-,root,root)
%{kde4_plugindir}/kcm_cddb.so
%{kde4_libdir}/libkcddb.so.*
%{kde4_appsdir}/kconf_update/kcmcddb-emailsettings.upd
%{kde4_kcfgdir}/libkcddb.kcfg
%{kde4_servicesdir}/libkcddb.desktop

%files -n %{name}-libkcompactdisc
%defattr(-,root,root)
%{kde4_libdir}/libkcompactdisc.so.*

%files -n %{name}-kioslave_audiocd
%defattr(-,root,root)
%{kde4_plugindir}/kcm_audiocd.so
%{kde4_plugindir}/kio_audiocd.so
%{kde4_plugindir}/libaudiocd_encoder_*.so
%{kde4_libdir}/libaudiocdplugins.so.*
%{kde4_appsdir}/konqsidebartng/virtual_folders/services/audiocd.desktop
%{kde4_appsdir}/kconf_update/audiocd.upd
%{kde4_appsdir}/kconf_update/upgrade-metadata.sh
%{kde4_appsdir}/solid/actions/kscd-play-audiocd.desktop
%{kde4_appsdir}/solid/actions/solid_audiocd.desktop
%{kde4_kcfgdir}/audiocd_*_encoder.kcfg
%{kde4_servicesdir}/audiocd.*
%doc %lang(en) %{kde4_htmldir}/en/kioslave/audiocd

%files -n %{name}-dragonplayer
%defattr(-,root,root)
%{kde4_bindir}/dragon
%{kde4_plugindir}/dragonpart.so
%{kde4_appsdir}/dragonplayer/*
%{kde4_appsdir}/solid/actions/dragonplayer-opendvd.desktop
%config %{kde4_configdir}/dragonplayerrc
%{kde4_iconsdir}/hicolor/*/apps/dragonplayer.*
%{kde4_iconsdir}/oxygen/*/actions/player-volume-muted.*
%{kde4_xdgappsdir}/dragonplayer.desktop
%{kde4_servicesdir}/ServiceMenus/dragonplayer_play_dvd.desktop
%{kde4_servicesdir}/dragonplayer_part.desktop
%doc %lang(en) %{kde4_htmldir}/en/dragonplayer

%files -n %{name}-mplayerthumbs
%defattr(-,root,root)
%{kde4_bindir}/mplayerthumbsconfig
%{kde4_plugindir}/videopreview.so
%{kde4_appsdir}/videothumbnail/*
%{kde4_kcfgdir}/mplayerthumbs.kcfg
%{kde4_servicesdir}/videopreview.desktop

%files -n %{name}-ffmpegthumbs
%defattr(-,root,root)
%{kde4_plugindir}/ffmpegthumbs.so
%{kde4_servicesdir}/ffmpegthumbs.desktop

%changelog
* Sun Aug 2 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.3.0-1mgc
- 更新至 4.3.0
- 己丑  六月十二

* Tue Jun 30 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.95-1mgc
- 更新至 4.2.95(KDE 4.3 RC1)
- 己丑  闰五月初八

* Sat Jun 13 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.91-1mgc
- 更新至 4.2.91
- 己丑  五月廿一

* Sat May 16 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.85-1mgc
- 更新至 4.2.85(KDE 4.3 beta1)
- 己丑  四月廿二

* Sat Apr 4 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.2-1mgc
- 更新至 4.2.2
- 己丑  三月初九  [清明]

* Sun Mar 8 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.1-0.1mgc
- 更新至 4.2.1
- 己丑  二月十二

* Sun Jan 25 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.0-0.1mgc
- 更新至 4.2.0
- 戊子  十二月三十

* Wed Jan 14 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.1.96-0.1mgc
- 更新至 4.1.96(KDE 4.2 RC1)
- relwithdeb 编译模式
- 戊子  十二月十九

* Sat Dec 13 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.1.85-0.1mgc
- 更新至 4.1.85(KDE 4.2 Beta2)
- 戊子  十一月十六

* Sat Nov 29 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.1.80-0.1mgc
- 更新至 4.1.80
- 戊子  十一月初二

* Fri Nov 07 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.1.3-0.1mgc
- 更新至 4.1.3
- 戊子  十月初十  [立冬]

* Mon Sep 29 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.1.2-0.1mgc
- 更新至 4.1.2
- 戊子  九月初一

* Sat Aug 30 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.1.1-0.1mgc
- 更新至 4.1.1
- 戊子  七月三十

* Fri Jul 25 2008 Liu Di <liudidi@gmail.com> - 4.1.0-0.1mgc
- 更新到 4.1.0(KDE 4.1 正式版)

* Fri Jul 11 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.98-0.1mgc
- 更新至 4.0.98(KDE 4.1 RC1)
- 戊子  六月初九

* Sat Jul 5 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.85-0.1mgc
- 更新至 4.0.85
- 更新 juk 标签编码补丁(patch 11 rewritten by nihui)
- 修正 dragonplayer 标题状态栏显示(patch 12 written by nihui)
- 戊子  六月初三

* Sat Jun 28 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.84-0.1mgc
- 更新至 4.0.84
- 戊子  五月廿五

* Thu Jun 19 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.83-0.1mgc
- 更新至 4.0.83-try1(第一次 tag 4.1.0-beta2 内部版本)
- 更新 juk 标签编码补丁
- 戊子  五月十六

* Thu Jun 12 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.82-0.1mgc
- 更新至 4.0.82
- 戊子  五月初九

* Wed Jun 4 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.81-0.1mgc
- 更新至 4.0.81
- 戊子  五月初一

* Fri May 23 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.80-0.1mgc
- 更新至 4.0.80(try1 内部版本)
- 戊子  四月十九

* Fri May 16 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.74-0.1mgc
- 更新至 4.0.74
- 戊子  四月十二

* Sat Apr 26 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.71-0.1mgc
- 更新至 4.0.71
- 修正 juk mp3 标签乱码问题(patch 10)
- 戊子  三月廿一

* Sat Apr 19 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.70-0.1mgc
- 更新至 4.0.70
- 戊子  三月十四

* Tue Apr 1 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.3-0.1mgc
- 更新至 4.0.3
- 定义 kde4 路径
- 细化分包
- 戊子  二月廿五

* Tue Mar 4 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.2-0.1mgc
- 更新至 4.0.2
- 戊子  正月廿七

* Sat Feb 9 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.1-0.1mgc
- 更新至 4.0.1

* Sat Jan 12 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.0-0.1mgc
- 更新至 4.0.0

* Sat Nov 24 2007 Ni Hui <shuizhuyuanluo@126.com> - 3.96.0-0.1mgc
- 更新至 3.96.0 (KDE4-RC1)

* Sat Oct 20 2007 Ni Hui <shuizhuyuanluo@126.com> - 3.94.0-0.1mgc
- 首次生成 rpm 包
