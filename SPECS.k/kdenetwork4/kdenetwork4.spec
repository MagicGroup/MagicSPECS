%define rversion %{kde4_kdelibs_version}
%define release_number 1
%define real_name kdenetwork

%define kde4_enable_final_bool OFF

# kopete telepathy protocol support
%define with_telepathy 1
# kopete irc protocol support
%define with_irc 0

%define MOZPLUGIN_INSTALL_DIR %{_libdir}/mozilla/plugins/

%define LIBGADU_LIBRARIES %{_libdir}/libgadu.so
%define LIBGADU_INCLUDE_DIR %{_includedir}
#%define LIBNXCL_LIBRARIES %{_libdir}/libnxcl.so
#%define LIBNXCL_INCLUDE_DIR %{_includedir}/nxcl/nxclientlib.h

Name: kdenetwork4
Summary: The KDE Network Components
License: LGPL v2 or later
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
URL: http://www.kde.org/
Version: %{rversion}
Release: %{release_number}%{?dist}
Source0: http://download.kde.org/stable/%{rversion}/src/%{real_name}-%{rversion}.tar.xz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# FIXME: post installation requirement
Requires: vorbis-tools

BuildRequires: libkdelibs4-devel
BuildRequires: libkdepimlibs4-devel
BuildRequires: libjpeg-devel
BuildRequires: openslp-devel
BuildRequires: libidn-devel
BuildRequires: sqlite-devel
BuildRequires: openssl-devel
BuildRequires: libxml2-devel
BuildRequires: libxslt-devel
# kopete gadugadu 协议支持
BuildRequires: libgadu-devel >= 1.8.0
# kopete v4l 摄像头支持
BuildRequires: libv4l-devel
# krdc/krfb 的 vnc 支持
BuildRequires: LibVNCServer-devel >= 0.9.1
# zeroconf 支持
BuildRequires: avahi-compat-libdns_sd-devel
# kopete otr 插件的离线消息加密支持
BuildRequires: libotr-devel >= 3.2.0
# kopete windows live messenger 协议支持
BuildRequires: libmsn-devel >= 0.4
# kopete sametime/meanwhile 协议支持
BuildRequires: meanwhile-devel >= 1.0.0
# kopete jabber 协议 jingle 库支持
BuildRequires: ortp-devel >= 0.14
# krdc nx 协议支持
BuildRequires: nxcl-devel >= 0.9
%if %with_telepathy
# kopete telepathy 协议支持
BuildRequires: telepathy-qt4-devel
%endif
# plasma 部件支持
BuildRequires: kdebase4-workspace-devel
# kopete jabber/gtalk 协议依赖
BuildRequires: qca2-devel >= 2.0.0
# kget wenkit part 支持
BuildRequires: kwebkitpart
# kget BT 支持
BuildRequires: kde4-libktorrent-devel >= 1.0.1
# kopete 音频/视频支持
BuildRequires: linphone-devel

Requires: %{name}-filesharing = %{version}
Requires: %{name}-kdnssd = %{version}
Requires: %{name}-kget = %{version}
Requires: %{name}-kopete = %{version}
Requires: %{name}-kppp = %{version}
Requires: %{name}-krdc = %{version}
Requires: %{name}-krfb = %{version}

# kde brunch 代码更新
#Patch1: kdenetwork-4.0.1-768945_to_772589.diff
Patch1: kdenetwork-4.2.98-kdrc-icon.patch
# rhbz#540433 - KPPP is unable to add DNS entries to /etc/resolv.conf
Patch2: kdenetwork-4.3.3-resolv-conf-path.patch
# upstream patches (4.4 branch):

Patch3:	kdenetwork-4.7.97-fix-for-g++47.patch

Patch800: kdenetwork-4.3.4-enablefinal.patch

# kopete 群消息显示用户名
# ported to Qt4/KDE4 by nihui, Jun.12th, 2008
Patch10: kdenetwork-4.0.80-kopete_add_msngroup.patch
# kopete 工具栏分为两栏，以使搜索条可用
Patch11: kdenetwork-4.2.2-kopete-searchbar_new_line.patch
# kopete qq 协议登录问题修正
Patch12: kopete-qq-login.patch
# 删除 krdc 中的 nx xid 支持
Patch100: kdenetwork-4.1.85-krdc-remove_nx_xid.patch
# Kget 在新 webkitkde 上编译的头文件不对
Patch101: kdenetwork-4.3.3-webkitkde.patch

Patch99: kdenetwork-4.7.0-openssl-tmp.patch


Patch1000: 1138807.diff


%description
The KDE Network Components.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- 开发包
%package -n %{name}-devel
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: KDE Network Libraries: Build Environment
Requires: %{name} = %{version} libkdelibs4-devel
Requires: %{name} = %{version}

%description -n %{name}-devel
This package contains all necessary include files and libraries needed
to develop KDE Network applications.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- filesharing
%package -n %{name}-filesharing
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: filesharing

%description -n %{name}-filesharing
filesharing.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- kdnssd
%package -n %{name}-kdnssd
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: kdnssd

%description -n %{name}-kdnssd
kdnssd.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- kget
%package -n %{name}-kget
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: kget

%description -n %{name}-kget
kget.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- kopete
%package -n %{name}-kopete
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: kopete
Requires: qca2

%description -n %{name}-kopete
kopete.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- kppp
%package -n %{name}-kppp
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: kppp
Requires: ppp

%description -n %{name}-kppp
kppp.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- krdc
%package -n %{name}-krdc
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: krdc
Requires: rdesktop

%description -n %{name}-krdc
krdc.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- krfb
%package -n %{name}-krfb
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: krfb

%description -n %{name}-krfb
krfb.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
%prep
%setup -q -n %{real_name}-%{rversion}

%patch1 -p1 -b .icon
%patch2 -p1 -b .resolv-conf-path
%patch3 -p1
chmod +x kopete/kopete/kconf_update/kopete-update_yahoo_server.pl

#%patch800 -p1

#%if %with_msn
#%patch10 -p1
#%endif
%patch11 -p1
pushd kopete/protocols/qq/
%patch12 -p0
popd

#%patch100 -p1 -b .orig
#%patch101 -p1 

%patch99 -p1
#%patch1000 -p0

%build
mkdir build
cd build
%cmake_kde4 \
	-DWITH_JINGLE=TRUE \
	-DMOZPLUGIN_INSTALL_DIR=%MOZPLUGIN_INSTALL_DIR \
	-DLIBGADU_LIBRARIES=%LIBGADU_LIBRARIES \
	-DLIBGADU_INCLUDE_DIR=%LIBGADU_INCLUDE_DIR \
%if %with_irc
	-DWITH_irc=ON \
%endif
	..

#	-DLIBNXCL_LIBRARIES=%{LIBNXCL_LIBRARIES} \
#	-DLIBNXCL_INCLUDE_DIR=%{LIBNXCL_INCLUDE_DIR} \

make %{?_smp_mflags}

%install
cd build
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

%clean_kde4_desktop_files
%clean_kde4_notifyrc_files
%adapt_kde4_notifyrc_files
magic_rpm_clean.sh

%post -n %{name}-kget -p /usr/sbin/ldconfig
%postun -n %{name}-kget -p /usr/sbin/ldconfig

%post -n %{name}-kopete
/usr/sbin/ldconfig
# convert ogg sound files to wav format
pushd "/opt/kde4/share/sounds/"
for oggfile in `ls Kopete_*.ogg`; do
    wavfile=${oggfile%.ogg}.wav;
    oggdec -Q $oggfile -o $wavfile;
done
popd

%postun -n %{name}-kopete -p /usr/sbin/ldconfig

%post -n %{name}-krdc -p /usr/sbin/ldconfig
%postun -n %{name}-krdc -p /usr/sbin/ldconfig

%post -n %{name}-krfb -p /usr/sbin/ldconfig
%postun -n %{name}-krfb -p /usr/sbin/ldconfig

%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files -n %{name}-devel
%defattr(-,root,root)
%{kde4_includedir}/*
%{kde4_libdir}/*.so
%exclude %{kde4_libdir}/libqgroupwise.so

%files
%defattr(-,root,root)
%doc COPYING COPYING.LIB

%files -n %{name}-filesharing
%defattr(-,root,root)
%{kde4_plugindir}/sambausershareplugin.so
%{kde4_plugindir}/plugins/accessible/chatwindowaccessiblewidgetfactory.so
#%{kde4_plugindir}/kcm_fileshare.so
#%{kde4_plugindir}/kcm_kcmsambaconf.so
#%{kde4_iconsdir}/hicolor/*/apps/kcmsambaconf.*
#%{kde4_servicesdir}/fileshare*.desktop
#%{kde4_servicesdir}/kcmsambaconf.desktop
%{kde4_servicesdir}/sambausershareplugin.desktop

%files -n %{name}-kdnssd
%defattr(-,root,root)
%{kde4_plugindir}/kded_dnssdwatcher.so
%{kde4_plugindir}/kio_zeroconf.so
%{kde4_appsdir}/remoteview/*
%{kde4_dbus_interfacesdir}/org.kde.kdnssd.xml
%{kde4_servicesdir}/kded/dnssdwatcher.desktop
%{kde4_servicesdir}/zeroconf.protocol

%files -n %{name}-kget
%defattr(-,root,root)
%{kde4_bindir}/kget
%{kde4_plugindir}/kget_*.so
%{kde4_plugindir}/kcm_kget_*.so
#%{kde4_plugindir}/khtml_kget.so
%{kde4_plugindir}/plasma_*_kget.so
%{kde4_plugindir}/plasma_kget_*.so
%{kde4_plugindir}/krunner_kget.so
%{kde4_libdir}/libkgetcore.so.*
#%{kde4_appsdir}/desktoptheme/default/widgets/kget.svg
%{kde4_appsdir}/kget/*
%{kde4_appsdir}/khtml/kpartplugins/kget*
%{kde4_appsdir}/dolphinpart/kpartplugins/kget_plug_in.*
%{kde4_appsdir}/kwebkitpart/kpartplugins/kget_plug_in.*
%{kde4_kcfgdir}/kget*.kcfg
%{kde4_dbus_servicesdir}/org.kde.kget.service
%{kde4_iconsdir}/hicolor/*/apps/kget.*
%{kde4_xdgappsdir}/kget.desktop
%{kde4_servicesdir}/kget_*.desktop
%{kde4_servicesdir}/kget*-default.desktop
%{kde4_servicesdir}/plasma*kget*.desktop
%{kde4_servicesdir}/ServiceMenus/kget_*.desktop
%{kde4_servicetypesdir}/kget_plugin.desktop
#%{kde4_datadir}/sounds/KGet_*.ogg
%doc %lang(en) %{kde4_htmldir}/en/kget
%{kde4_datadir}/ontology/kde/kget_history.*

%files -n %{name}-kopete
%defattr(-,root,root)
%{kde4_bindir}/kopete
%{kde4_bindir}/kopete_latexconvert.sh
%{kde4_bindir}/winpopup*
%{kde4_bindir}/googletalk-call
#%{kde4_bindir}/skype-action-handler
%{kde4_plugindir}/kcm_kopete_*.so
%{kde4_plugindir}/kopete_*.so
%{kde4_plugindir}/libchattexteditpart.so
%{kde4_libdir}/libkopete*.so.*
%{kde4_libdir}/libkyahoo.so.*
%{kde4_libdir}/liboscar.so.*
%{kde4_libdir}/libqgroupwise.so
%{kde4_appsdir}/kconf_update/*
%{kde4_appsdir}/kopete*
%{kde4_kcfgdir}/historyconfig.kcfg
%{kde4_kcfgdir}/kopete*.kcfg
%{kde4_kcfgdir}/latexconfig.kcfg
%{kde4_kcfgdir}/nowlisteningconfig.kcfg
%{kde4_kcfgdir}/urlpicpreview.kcfg
%{kde4_kcfgdir}/webpresenceconfig.kcfg
%{kde4_kcfgdir}/translatorconfig.kcfg
%config %{kde4_configdir}/kopeterc
%{kde4_dbus_interfacesdir}/org.kde.kopete*.xml
%{kde4_dbus_interfacesdir}/org.kde.Kopete.xml
%{kde4_iconsdir}/hicolor/*/apps/kopete*
%{kde4_iconsdir}/oxygen/*/actions/*
#%{kde4_iconsdir}/oxygen/*/apps/kopete*
#%{kde4_iconsdir}/oxygen/*/mimetypes/kopete*
%{kde4_iconsdir}/oxygen/*/status/object-locked-*.*
%{kde4_xdgappsdir}/kopete.desktop
%{kde4_servicesdir}/aim.protocol
%{kde4_servicesdir}/callto.protocol
%{kde4_servicesdir}/chatwindow.desktop
%{kde4_servicesdir}/emailwindow.desktop
%{kde4_servicesdir}/kconfiguredialog/kopete_*_config.desktop
%{kde4_servicesdir}/kopete_*.desktop
%{kde4_servicesdir}/skype.protocol
%{kde4_servicesdir}/tel.protocol
%{kde4_servicesdir}/xmpp.protocol
%{kde4_servicetypesdir}/kopete*.desktop
%{kde4_datadir}/sounds/Kopete_*.ogg
%{kde4_datadir}/sounds/KDE-Im-Phone-Ring.wav
%doc %lang(en) %{kde4_htmldir}/en/kopete
# firefox skype plugin
%MOZPLUGIN_INSTALL_DIR/skypebuttons.so

%files -n %{name}-kppp
%defattr(-,root,root)
%{kde4_bindir}/kppp
%{kde4_bindir}/kppplogview
%{kde4_appsdir}/kppp/*
%{kde4_dbus_interfacesdir}/org.kde.kppp.xml
%{kde4_iconsdir}/hicolor/*/apps/kppp.*
%{kde4_xdgappsdir}/Kppp.desktop
%{kde4_xdgappsdir}/kppplogview.desktop
%doc %lang(en) %{kde4_htmldir}/en/kppp

%files -n %{name}-krdc
%defattr(-,root,root)
%{kde4_bindir}/krdc
%{kde4_bindir}/krdc_rfb_approver
%{kde4_libdir}/libkrdccore.so.*
%{kde4_plugindir}/kcm_krdc_*plugin.so
%{kde4_plugindir}/krdc_*plugin.so
%{kde4_appsdir}/krdc/*
%{kde4_appsdir}/krdc_rfb_approver/*
%{kde4_kcfgdir}/krdc.kcfg
%{kde4_datadir}/telepathy/clients/krdc_rfb_*.client
%{kde4_dbus_servicesdir}/org.freedesktop.Telepathy.Client.krdc_rfb_*.service
#%{kde4_iconsdir}/hicolor/*/apps/krdc.*
%{kde4_xdgappsdir}/krdc.desktop
%{kde4_servicesdir}/krdc_*.desktop
%{kde4_servicesdir}/rdp.protocol
%{kde4_servicesdir}/vnc.protocol
%{kde4_servicesdir}/ServiceMenus/smb2rdc.desktop
%{kde4_servicetypesdir}/krdc_*.desktop
%doc %lang(en) %{kde4_htmldir}/en/krdc

%files -n %{name}-krfb
%defattr(-,root,root)
%{kde4_bindir}/krfb
%{kde4_libdir}/libkrfbprivate.so.*
%{kde4_plugindir}/krfb_*.so
%{kde4_appsdir}/krfb/*
%{kde4_xdgappsdir}/krfb.desktop
%{kde4_servicesdir}/krfb_*.desktop
%{kde4_servicetypesdir}/krfb-*.desktop
%{kde4_dbus_servicesdir}/org.freedesktop.Telepathy.Client.krfb_rfb_handler.service
%{kde4_datadir}/telepathy/clients/krfb_rfb_handler.client
%doc %lang(en) %{kde4_htmldir}/en/krfb

%changelog
* Tue Aug 4 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.3.0-1mgc
- 更新至 4.3.0
- 己丑  六月十四

* Mon Jun 29 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.95-1mgc
- 更新至 4.2.95(KDE 4.3 RC1)
- kopete QQ 协议登录问题修正(patch 12 imported from bko)
- 己丑  闰五月初七

* Sat Jun 13 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.91-1mgc
- 更新至 4.2.91
- 定义 mozilla 插件安装路径
- 无 jabber 协议 libjingle 支持
- 己丑  五月廿一

* Sun May 17 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.85-1mgc
- 更新至 4.2.85(KDE 4.3 beta1)
- 己丑  四月廿三

* Sat Apr 4 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.2-1mgc
- 更新至 4.2.2
- 纳入 libgadu 和 libv4l 支持
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
- %with_telepathy 开关(关闭)
- %with_irc 开关(关闭)
- %with_msn 开关(关闭)
- 去除 knewsticker(removed by upstream ??)
- 纳入 kopete windows live messenger 协议支持
- 纳入 kopete jabber 协议 jingle 库支持
- 去除 krdc nx 协议的 xid 支持(patch 100 written by nihui, Dec.13th, 2008)
- 戊子  十一月十六

* Sun Dec 1 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.1.80-0.1mgc
- 更新至 4.1.80
- 戊子  十一月初三

* Sun Oct 12 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.1.69-0.1mgc
- 更新至 4.1.69
- krdc nx 协议支持
- 戊子  九月十四

* Mon Sep 29 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.1.2-0.1mgc
- 更新至 4.1.2
- kopete lockdown 支持
- 戊子  九月初一

* Sat Aug 30 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.1.1-0.1mgc
- 更新至 4.1.1
- 戊子  七月三十

* Fri Jul 25 2008 Liu Di <liudidi@gmail.com> - 4.1.0-0.1mgc
- 更新到 4.1.0(KDE 4.1 正式版)

* Fri Jul 11 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.98-0.1mgc
- 更新至 4.0.98(KDE 4.1 RC1)
- 戊子  六月初九

* Sat Jun 28 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.84-0.1mgc
- 更新至 4.0.84
- 纳入 webkit 支持
- 戊子  五月廿五

* Thu Jun 19 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.83-0.1mgc
- 更新至 4.0.83-try1(第一次 tag 4.1.0-beta2 内部版本)
- 戊子  五月十六

* Thu Jun 12 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.82-0.1mgc
- 更新至 4.0.82
- kopete 群消息显示用户名补丁(patch 10 from magic linux project)
- 戊子  五月初九

* Wed Jun 4 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.81-0.1mgc
- 更新至 4.0.81
- 戊子  五月初一

* Sat May 24 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.80-0.1mgc
- 更新至 4.0.80(try1 内部版本)
- 戊子  四月二十

* Fri May 16 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.74-0.1mgc
- 更新至 4.0.74
- 纳入 tapioca-qt 和 telepathy-qt 支持
- 纳入 decibel 支持
- 戊子  四月十二

* Sat Apr 26 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.71-0.1mgc
- 更新至 4.0.71
- 戊子  三月廿一

* Sat Apr 19 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.70-0.1mgc
- 更新至 4.0.70
- 纳入 zeroconf 支持
- 纳入 libotr 支持(kopete otr 插件消息加密)
- 戊子  三月十四

* Wed Apr 2 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.3-0.1mgc
- 更新至 4.0.3
- 定义 kde4 路径
- 细化分包
- 戊子  二月廿六

* Tue Mar 4 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.2-0.1mgc
- 更新至 4.0.2
- 戊子  正月廿七

* Sat Feb 9 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.1-0.1mgc
- 更新至 4.0.1
- 手动添加 qca-ossl 依赖(kopete jabber 协议 ssl 加密支持)

* Wed Jan 16 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.0-0.2mgc
- 纳入 LibVNCServer 支持
- 纳入 qca2 支持
- 更新 brunch 补丁

* Sat Jan 12 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.0-0.1mgc
- 更新至 4.0.0

* Sat Nov 24 2007 Ni Hui <shuizhuyuanluo@126.com> - 3.96.0-0.1mgc
- 更新至 3.96.0 (KDE4-RC1)

* Sat Oct 20 2007 Ni Hui <shuizhuyuanluo@126.com> - 3.94.0-0.1mgc
- 首次生成 rpm 包
