%define rversion %{kde4_kdelibs_version}
%define release_number 1
%define real_name kdeutils

# do not enable final...
# I'm lazy to make a patch for this..
# too many errors...
%define kde4_enable_final_bool OFF


Name: kdeutils4
Summary: The KDE UTIL Components
Summary(zh_CN.UTF-8): KDE 工具组件
License: LGPL v2 or later
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
URL: http://www.kde.org/
Version: %{rversion}
Release: %{release_number}%{?dist}
Source0: %{real_name}-%{rversion}.tar.bz2

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: libkdelibs4-devel
BuildRequires: libkdepimlibs4-devel
BuildRequires: qimageblitz-devel
BuildRequires: gmp

# <= 0.9.4 版本会出错
BuildRequires: libXrender-devel >= 0.9.4
# ark 的 zip 文件支持
BuildRequires: libzip-devel >= 0.8
# ark 的其他归档文件支持
BuildRequires: libarchive-devel >= 2.4.10

BuildRequires: qjson-devel
# Thinkpad 支持(kmilo 所需，已移除)
#BuildRequires: tpctl-devel >= 4.17
# printer-applet 编译依赖
BuildRequires: python-devel
BuildRequires: PyQt4-devel
BuildRequires: PyKDE4-devel
BuildRequires: system-config-printer-libs

Requires: %{name}-ark = %{version}
Requires: %{name}-kremotecontrol = %{version}
Requires: %{name}-kcalc = %{version}
Requires: %{name}-kcharselect = %{version}
#Requires: %{name}-kdessh = %{version}
Requires: %{name}-kdf = %{version}
Requires: %{name}-kfloppy = %{version}
Requires: %{name}-kgpg = %{version}
#Requires: %{name}-kmilo = %{version}
Requires: %{name}-ktimer = %{version}
Requires: %{name}-kwalletmanager = %{version}
Requires: %{name}-kwikdisk = %{version}
#Requires: %{name}-okteta = %{version}
Requires: %{name}-printer-applet = %{version}
Requires: %{name}-superkaramba = %{version}
Requires: %{name}-sweeper = %{version}

# kde brunch 代码更新
#Patch1: kdeutils-4.0.1-768945_to_773078.diff

%description
The KDE UTIL Components.

%description -l zh_CN.UTF-8
KDE 工具组件。

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- 开发包
%package -n %{name}-devel
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: KDE UTIL Libraries: Build Environment
Requires: libkdelibs4-devel cyrus-sasl-devel openldap-devel boost-devel
Requires: %{name} = %{version}

%description -n %{name}-devel
This package contains all necessary include files and libraries needed
to develop KDE UTIL applications.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- ark
%package -n %{name}-ark
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: ark

%description -n %{name}-ark
ark.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- kcalc
%package -n %{name}-kcalc
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: kcalc

%description -n %{name}-kcalc
kcalc.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- kcharselect
%package -n %{name}-kcharselect
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: kcharselect

%description -n %{name}-kcharselect
kcharselect.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- kdessh
#%package -n %{name}-kdessh
#Group: System/GUI/KDE
#Group(zh_CN.UTF-8): 系统/GUI/KDE
#Summary: kdessh
#
#%description -n %{name}-kdessh
#kdessh.
#
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- kdf
%package -n %{name}-kdf
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: kdf

%description -n %{name}-kdf
kdf.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- kfloppy
%package -n %{name}-kfloppy
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: kfloppy

%description -n %{name}-kfloppy
kfloppy.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- kgpg
%package -n %{name}-kgpg
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: kgpg

%description -n %{name}-kgpg
kgpg.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- ktimer
%package -n %{name}-ktimer
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: ktimer

%description -n %{name}-ktimer
ktimer.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- kwalletmanager
%package -n %{name}-kwalletmanager
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: kwalletmanager

Provides: %{name}-kwallet = %{version}

%description -n %{name}-kwalletmanager
kwalletmanager.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- kwikdisk
%package -n %{name}-kwikdisk
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: kwikdisk

%description -n %{name}-kwikdisk
kwikdisk.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- sweeper
%package -n %{name}-sweeper
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: sweeper

%description -n %{name}-sweeper
sweeper.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- kmilo
#%package -n %{name}-kmilo
#Group: System/GUI/KDE
#Group(zh_CN.UTF-8): 系统/GUI/KDE
#Summary: kmilo
#
#%description -n %{name}-kmilo
#kmilo.
#
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- superkaramba
%package -n %{name}-superkaramba
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: superkaramba

%description -n %{name}-superkaramba
superkaramba.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- okteta
%package -n %{name}-okteta
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: okteta

%description -n %{name}-okteta
okteta.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- filelight
%package -n %{name}-filelight
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: filelight

%description -n %{name}-filelight
filelight.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- printer-applet
%package -n %{name}-printer-applet
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: printer-applet
Requires: PyQt4
Requires: PyKDE4
Requires: system-config-printer-libs

%description -n %{name}-printer-applet
printer-applet.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- kremotecontrol
%package -n %{name}-kremotecontrol
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: kremotecontrol
Obsoletes: %{name}-irkick < 4.4.90

%description -n %{name}-kremotecontrol
kremotecontrol.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#  

%prep
%setup -q -n %{real_name}-%{rversion}

#%patch1 -p1

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

%post -n %{name}-ark -p /sbin/ldconfig
%postun -n %{name}-ark -p /sbin/ldconfig

%post -n %{name}-kremotecontrol -p /sbin/ldconfig
%postun -n %{name}-kremotecontrol -p /sbin/ldconfig

%post -n %{name}-okteta -p /sbin/ldconfig
%postun -n %{name}-okteta -p /sbin/ldconfig

%post -n %{name}-superkaramba -p /sbin/ldconfig
%postun -n %{name}-superkaramba -p /sbin/ldconfig

%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files -n %{name}-devel
%defattr(-,root,root)
#%{kde4_includedir}/*
%{kde4_libdir}/*.so
#%{kde4_plugindir}/plugins/designer/oktetadesignerplugin.so
%exclude %{kde4_libdir}/libkdeinit4_*.so

%files
%defattr(-,root,root)
%doc COPYING COPYING.LIB

%files -n %{name}-ark
%defattr(-,root,root)
%{kde4_bindir}/ark
%{kde4_plugindir}/kerfuffle_*.so
%{kde4_plugindir}/arkpart.so
%{kde4_plugindir}/libextracthere.so
%{kde4_libdir}/libkerfuffle.so.*
%{kde4_appsdir}/ark/*
%{kde4_kcfgdir}/ark.kcfg
%{kde4_xdgappsdir}/ark.desktop
%{kde4_servicesdir}/ark_*.desktop
%{kde4_servicesdir}/kerfuffle_*.desktop
%{kde4_servicesdir}/ServiceMenus/ark_*.desktop
%{kde4_servicetypesdir}/kerfuffle*.desktop
%{kde4_mandir}/man1/ark.1
%doc %lang(en) %{kde4_htmldir}/en/ark

%files -n %{name}-kremotecontrol
%defattr(-,root,root)
%{kde4_bindir}/krcdnotifieritem
%{kde4_plugindir}/kcm_remotecontrol.so
%{kde4_plugindir}/kded_kremotecontroldaemon.so
%{kde4_plugindir}/plasma_engine_kremoteconrol.so
%{kde4_plugindir}/kremotecontrol_lirc.so
%{kde4_libdir}/liblibkremotecontrol.so.*
%{kde4_appsdir}/kremotecontrol/*
%{kde4_appsdir}/kremotecontroldaemon/*
%{kde4_iconsdir}/hicolor/*/devices/infrared-remote.*
%{kde4_iconsdir}/hicolor/*/actions/krcd_flash.*
%{kde4_iconsdir}/hicolor/*/actions/krcd_off.*
%{kde4_iconsdir}/hicolor/*/apps/krcd.*
%{kde4_xdgappsdir}/krcdnotifieritem.desktop
%{kde4_servicesdir}/kremotecontrolbackends/kremotecontrol_lirc.desktop
%{kde4_servicesdir}/kcm_remotecontrol.desktop
%{kde4_servicesdir}/kded/kremotecontroldaemon.desktop
%{kde4_servicesdir}/plasma-engine-kremotecontrol.desktop
%{kde4_servicetypesdir}/kremotecontrolmanager.desktop
%doc %lang(en) %{kde4_htmldir}/en/kcontrol/kremotecontrol

%files -n %{name}-kcalc
%defattr(-,root,root)
%{kde4_bindir}/kcalc
%{kde4_libdir}/libkdeinit4_kcalc.so
%{kde4_appsdir}/kcalc/*
%{kde4_appsdir}/kconf_update/kcalcrc.upd
%{kde4_kcfgdir}/kcalc.kcfg
#%{kde4_iconsdir}/hicolor/*/apps/kcalc.*
%{kde4_xdgappsdir}/kcalc.desktop
%doc %lang(en) %{kde4_htmldir}/en/kcalc

%files -n %{name}-kcharselect
%defattr(-,root,root)
%{kde4_bindir}/kcharselect
%{kde4_appsdir}/kcharselect/*
%{kde4_appsdir}/kconf_update/kcharselect.upd
%{kde4_xdgappsdir}/KCharSelect.desktop
%doc %lang(en) %{kde4_htmldir}/en/kcharselect

%files -n %{name}-filelight
%defattr(-,root,root)
%{kde4_bindir}/filelight
%{kde4_plugindir}/filelightpart.so
%{kde4_xdgappsdir}/filelight.desktop
%{kde4_appsdir}/filelight/filelightui.rc
%{kde4_appsdir}/filelightpart/filelightpartui.rc
%{kde4_configdir}/filelightrc
%{kde4_htmldir}/en/filelight/*
%{kde4_iconsdir}/hicolor/*/apps/filelight.png
%{kde4_iconsdir}/hicolor/32x32/actions/view_filelight.png
%{kde4_servicesdir}/filelightpart.desktop

%files -n %{name}-kdf
%defattr(-,root,root)
%{kde4_bindir}/kdf
%{kde4_plugindir}/kcm_kdf.so
%{kde4_appsdir}/kdf/*
%{kde4_iconsdir}/hicolor/*/apps/kdf.*
%{kde4_iconsdir}/oxygen/*/apps/kcmdf.*
%{kde4_xdgappsdir}/kdf.desktop
%{kde4_servicesdir}/kcmdf.desktop
%doc %lang(en) %{kde4_htmldir}/en/kdf

%files -n %{name}-kfloppy
%defattr(-,root,root)
%{kde4_bindir}/kfloppy
%{kde4_iconsdir}/hicolor/*/apps/kfloppy.*
%{kde4_xdgappsdir}/KFloppy.desktop
#%{kde4_servicesdir}/ServiceMenus/floppy_format.desktop
%doc %lang(en) %{kde4_htmldir}/en/kfloppy

%files -n %{name}-kgpg
%defattr(-,root,root)
%{kde4_bindir}/kgpg
%{kde4_appsdir}/kgpg/*
%{kde4_datadir}/autostart/kgpg.desktop
%{kde4_kcfgdir}/kgpg.kcfg
%{kde4_dbus_interfacesdir}/org.kde.kgpg*.xml
%{kde4_iconsdir}/hicolor/*/apps/kgpg.*
%{kde4_xdgappsdir}/kgpg.desktop
%{kde4_servicesdir}/ServiceMenus/encrypt*.desktop
%{kde4_servicesdir}/ServiceMenus/viewdecrypted.desktop
%doc %lang(en) %{kde4_htmldir}/en/kgpg

%files -n %{name}-ktimer
%defattr(-,root,root)
%{kde4_bindir}/ktimer
%{kde4_iconsdir}/hicolor/*/apps/ktimer.*
%{kde4_xdgappsdir}/ktimer.desktop
%doc %lang(en) %{kde4_htmldir}/en/ktimer

%files -n %{name}-kwalletmanager
%defattr(-,root,root)
%{kde4_bindir}/kwalletmanager
%{kde4_plugindir}/kcm_kwallet.so
%{kde4_appsdir}/kwalletmanager/*
%{kde4_iconsdir}/hicolor/*/apps/kwalletmanager*.*
%{kde4_xdgappsdir}/kwalletmanager*.desktop
%{kde4_servicesdir}/kwallet*.desktop
%doc %lang(en) %{kde4_htmldir}/en/kwallet

%files -n %{name}-kwikdisk
%defattr(-,root,root)
%{kde4_bindir}/kwikdisk
%{kde4_iconsdir}/hicolor/*/apps/kwikdisk.*
%{kde4_xdgappsdir}/kwikdisk.desktop
%doc %lang(en) %{kde4_htmldir}/en/kcontrol/blockdevices

%files -n %{name}-sweeper
%defattr(-,root,root)
%{kde4_bindir}/sweeper
%{kde4_appsdir}/sweeper/*
%{kde4_dbus_interfacesdir}/org.kde.sweeper.xml
%{kde4_xdgappsdir}/sweeper.desktop
%doc %lang(en) %{kde4_htmldir}/en/sweeper

#%files -n %{name}-kmilo
#%defattr(-,root,root)
#%doc COPYING COPYING.LIB
#%{kde4_plugindir}/kcm_kvaio.so
#%{kde4_plugindir}/kcm_thinkpad.so
#%{kde4_plugindir}/kded_kmilod.so
#%{kde4_plugindir}/kmilo_*.so
#%{kde4_libdir}/libkmilo.so.*
#%{kde4_dbus_interfacesdir}/org.kde.kmilod.xml
#%{kde4_servicesdir}/kded/kmilod.desktop
#%{kde4_servicesdir}/kmilo/kmilo_*.desktop
#%{kde4_servicesdir}/kvaio.desktop
#%{kde4_servicesdir}/thinkpad.desktop
#%{kde4_servicetypesdir}/kmilo/kmilo*.desktop

%files -n %{name}-printer-applet
%defattr(-,root,root)
%{kde4_bindir}/printer-applet
%{kde4_appsdir}/printer-applet/*
%{kde4_datadir}/autostart/printer-applet.desktop
%doc %lang(en) %{kde4_htmldir}/en/printer-applet

%files -n %{name}-superkaramba
%defattr(-,root,root)
%{kde4_bindir}/superkaramba
%{kde4_libdir}/libsuperkaramba.so.*
%{kde4_plugindir}/plasma_*_superkaramba.so
%{kde4_appsdir}/superkaramba/*
%config %{kde4_configdir}/superkaramba.knsrc
%{kde4_dbus_interfacesdir}/org.kde.superkaramba.xml
%{kde4_iconsdir}/hicolor/*/apps/superkaramba.*
%{kde4_xdgappsdir}/superkaramba.desktop
%{kde4_servicesdir}/plasma-*-superkaramba.desktop
#%doc %lang(en) %{kde4_htmldir}/en/superkaramba

%if 0
%files -n %{name}-okteta
%defattr(-,root,root)
%{kde4_bindir}/okteta
%{kde4_libdir}/libokteta*.so.*
%{kde4_libdir}/libkastencontrollers.so.*
%{kde4_libdir}/libkastencore.so.*
%{kde4_libdir}/libkastengui.so.*
%{kde4_plugindir}/libkbytearrayedit.so
%{kde4_plugindir}/oktetapart.so
%{kde4_appsdir}/okteta*/*
%{kde4_datadir}/mime/packages/okteta.xml
%{kde4_kcfgdir}/structviewpreferences.kcfg
%config %{kde4_configdir}/okteta-structures.knsrc
%{kde4_iconsdir}/hicolor/*/apps/okteta.*
%{kde4_xdgappsdir}/okteta.desktop
%{kde4_servicesdir}/kbytearrayedit.desktop
%{kde4_servicesdir}/oktetapart.desktop
%doc %lang(en) %{kde4_htmldir}/en/okteta
%endif

%changelog
* Wed Aug 5 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.3.0-1mgc
- 更新至 4.3.0
- 己丑  六月十五

* Tue Jun 30 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.95-1mgc
- 更新至 4.2.95(KDE 4.3 RC1)
- 己丑  闰五月初八

* Sat Jun 13 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.91-1mgc
- 更新至 4.2.91
- 己丑  五月廿一

* Sat May 16 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.85-1mgc
- 更新至 4.2.85(KDE 4.3 beta1)
- 己丑  四月廿二

* Sun Apr 5 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.2-1mgc
- 更新至 4.2.2
- 纳入 printer-applet 组件编译
- 己丑  三月初十

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

* Sun Dec 1 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.1.80-0.1mgc
- 更新至 4.1.80
- 戊子  十一月初三

* Fri Nov 07 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.1.3-0.1mgc
- 更新至 4.1.3
- 戊子  十月初十  [立冬]

* Mon Sep 29 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.1.2-0.1mgc
- 更新至 4.1.2
- 戊子  九月初一

* Sat Aug 30 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.1.1-0.1mgc
- 更新至 4.1.1
- 戊子  七月三十

* Fri Jul 25 2008 Liu Di <liudidi@gmail.com> - 4.1.0-1mgc
- 更新到 4.1.0(KDE 4.1 正式版)

* Fri Jul 11 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.98-0.1mgc
- 更新至 4.0.98(KDE 4.1 RC1)
- 戊子  六月初九

* Sat Jun 28 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.84-0.1mgc
- 更新至 4.0.84
- 戊子  五月廿五

* Thu Jun 19 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.83-0.1mgc
- 更新至 4.0.83-try1(第一次 tag 4.1.0-beta2 内部版本)
- 戊子  五月十六

* Thu Jun 12 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.82-0.1mgc
- 更新至 4.0.82
- 戊子  五月初九

* Wed Jun 4 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.81-0.1mgc
- 更新至 4.0.81
- 戊子  五月初一

* Sat May 24 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.80-0.1mgc
- 更新至 4.0.80(try1 内部版本)
- kjots 被移入 kdepim 组件
- 戊子  四月二十

* Fri May 16 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.74-0.1mgc
- 更新至 4.0.74
- 上游因 kmilo 质量不过关而移除
- 戊子  四月十二

* Sat Apr 26 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.71-0.1mgc
- 更新至 4.0.71
- 戊子  三月廿一

* Sat Apr 19 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.70-0.1mgc
- 更新至 4.0.70
- 戊子  三月十四

* Sun Feb 10 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.1-0.1mgc
- 更新至 4.0.1

* Wed Jan 16 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.0-0.1mgc
- 更新至 4.0.0
- 纳入 libzip 支持
- 纳入 libarchive 支持
- 纳入 tpctl 支持

* Sat Nov 24 2007 Ni Hui <shuizhuyuanluo@126.com> - 3.96.0-0.1mgc
- 更新至 3.96.0 (KDE4-RC1)

* Sat Oct 20 2007 Ni Hui <shuizhuyuanluo@126.com> - 3.94.0-0.1mgc
- 首次生成 rpm 包
