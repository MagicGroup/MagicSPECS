%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%define rversion %{kde4_kdelibs_version}
%define release_number 1
%define real_name kde-workspace

%define build_wallpaper_smallsize 1

Name: kdebase4-workspace
Summary: The KDE Workspace Components
Summary(zh_CN.UTF-8): KDE 工作空间组件
License: GPL v2 or later
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
URL: http://www.kde.org/
Version: %{rversion}
Release: %{release_number}%{?dist}.1
Source0: http://download.kde.org/stable/4.12.4/src/%{real_name}-4.11.8.tar.xz
Source1: extras.tar.gz
# magic logo for kwin decoration
Source2: magic.png
Source3: desenhoct1920x1200.png
# new air wallpaper for mgc 2.5+
Source4: newair1600x1200.jpg
Source5: newair1600x1200metadata.desktop

Source10: kcheckpass.pam
Source11: kdm.pam
Source12: kdm-np.pam
Source13: kscreensaver.pam

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# 添加原 kde4-session 中 startkde 脚本内容
# patch 1 written by nihui, Jun.19th, 2008
# 以下补丁暂时废弃
Patch900: kdebase-workspace-4.2.85-startkde_environment_variable_export.patch
Patch960: kdm-cope-with-new-grub.diff
Patch961: kdm-make_it_cool.diff


# fedora patches
# add konsole menuitem
# FIXME?  only show menu when/if konsole is installed? then we can drop the hard-dep
Patch2: kde-workspace-4.9.90-plasma_konsole.patch
Requires: kde4-konsole
Patch3: kdebase-workspace-4.6.80-krdb.patch
Patch4: kdebase-workspace-4.2.85-klipper-url.patch
# 434824: KDE4 System Settings - No Method To Enter Administrative Mode
Patch5: kdebase-workspace-4.4.90-rootprivs.patch
# show the remaining time in the battery plasmoid's popup (as in 4.2) (#515166)
Patch6: kde-workspace-4.8.80-battery-plasmoid-showremainingtime.patch
# kio_sysinfo based on OpenSUSE's patch
Patch7: kdebase-workspace-4.3.75-kio_sysinfo.patch
# allow adding a "Leave..." button which brings up the complete shutdown dialog
# to the classic menu (as in KDE <= 4.2.x); the default is still the upstream
# default Leave submenu
Patch8: kde-workspace-4.7.80-classicmenu-logout.patch

# kubuntu kudos! bulletproof-X bits ripped out
Patch19: kdebase-workspace-4.4.92-kdm_plymouth081.patch
Patch20: kdebase-workspace-4.4.92-xsession_errors_O_APPEND.patch

# support the widgetStyle4 hack in the Qt KDE platform plugin
Patch21: kdebase-workspace-4.3.98-platformplugin-widgetstyle4.patch

# revert patch adding broken browser launcher
# https://projects.kde.org/projects/kde/kde-workspace/repository/revisions/2bbbbdd8fe5a38ae27bab44c9515b2ba78f75277
# https://bugzilla.redhat.com/show_bug.cgi?id=747982
# https://bugs.kde.org/show_bug.cgi?id=284628
Patch25: kde-workspace-4.10.3-bz#747982-launchers.patch

# add org.kde.ktp-presence applet to default systray
Patch26: kde-workspace-4.10.2-systray_org.kde.ktp-presence.patch

# add support for automatic multi-seat provided by systemd using existing reserve seats in KDM
# needs having ServerCmd=/usr/lib/systemd/systemd-multi-seat-x set in /etc/kde/kdm/kdmrc
Patch27: kde-workspace-4.10.2-kdm-logind-multiseat.patch

## upstreamable patches:
# "keyboard stops working", https://bugs.kde.org/show_bug.cgi?id=171685#c135
Patch50: kde-workspace-4.7.80-kde#171685.patch

# use /etc/login.defs to define a 'system' account instead of hard-coding 500 
Patch52: kde-workspace-4.8.2-bz#732830-login.patch

# kdm overwrites ~/.Xauthority with wrong SELinux context on logout
# http://bugzilla.redhat.com/567914
# http://bugs.kde.org/242065
Patch53: kde-workspace-4.7.95-kdm_xauth.patch

# don't modify font settings on load (without explicit save)
# http://bugs.kde.org/105797
Patch54: kde-workspace-kcm_fonts_dont_change_on_load.patch

# support BUILD_KCM_RANDR (default ON) option
Patch55: kde-workspace-4.10.2-BUILD_KCM_RANDR.patch

# pam/systemd bogosity: kdm restart/shutdown does not work 
# http://bugzilla.redhat.com/796969
Patch57: kde-workspace-4.8.0-bug796969.patch

# merged patches: systemd-switch-user{,2} systemd-shutdown
# Support for systemd AND ConsoleKit in kworkspace
# contains a small hack, to be fixed properly soon
Patch63: kde-workspace-4.10.2-systemd-displaymanager.patch


## trunk patches
# kdm 文字空格优化
Patch60:        kdm-4.10.3-wordbreak.diff
# tablet pc 屏幕翻转支持
Patch82:        rotate-wacom-pointers.diff

# 活动窗口背景装饰颜色更换
# 这个还得看看实际效果
Patch85:        kdebase4-workspace-windeco-color.diff

## opensuse project patches:

# X 服务标准路径启动支持
Patch301: kde-workspace-4.10.3-_kdm_X_path.diff

Patch413: kubuntu_13_startkde_set_country.diff
Patch419: kubuntu_19_always_show_kickoff_subtext.diff
Patch463: kubuntu_63_ksplash_fix.diff

# Decrease bouncing cursor timeout to 10 secs. 30 is too high
Patch704: decrease-cursor-bounce-timeout.diff

# kwin logo 装饰
# patch 103 imported by nihui, Jun.13th, 2009
# 此补丁暂时放弃
Patch103: kdebase-workspace-4.2.88-icon_in_oxygen_title_bar.patch

#运行系统脚本
Patch104: kdm4-genkdmconfig.patch

# plasma 面板虚假半透明支持(无桌面混成时)
# 变化较大，暂不使用
Patch106: kdebase-workspace-4.4.86-plasma_transparent_panel_v3.diff
# plasma 默认面板程序布置
Patch107: kdebase-workspace-4.10.3-plasma-panel-defaultapplets.patch
# plasma kickoff 程序启动器徽标
Patch108: kdebase-workspace-4.4.85-kickoff-magic-logo.patch
# plasma dict 数据引擎 dict.cn 支持
Patch109: kdebase-workspace-4.10.3-dataengine_dict_dictcn.patch

Patch110: kickoff-favorites.diff
# 字号配置
Patch111: kdebase-workspace-4.10.3-increase-default-fontsize.patch
# 时间日期配置模块自动同步时间服务器
Patch112: kdebase-workspace-4.5.2-kcmdateandtime-ntpdate-para.patch

# upstream


BuildRequires: bluez-libs
BuildRequires: libkdelibs4-devel
BuildRequires: libxklavier-devel
BuildRequires: kde4-kactivities-devel
BuildRequires: libusb-devel
BuildRequires: libXrandr-devel >= 1.2.2
BuildRequires: qimageblitz-devel >= 0.0.4
BuildRequires: strigi-devel >= 0.6.3
BuildRequires: qt4-devel >= 4.4.3
BuildRequires: ConsoleKit-devel
# 网络连接管理功能
# 纳入支持  by nihui, Apr 4th,2008
BuildRequires: NetworkManager-devel >= 0.7.0
# 实时捕捉录像功能
# 纳入支持  by nihui, Jan 11th,2008
BuildRequires: capseo-devel
BuildRequires: libcaptury-devel
# plasma python 部件支持
#BuildRequires: kdebindings4 >= 4.1.0
# plasma google gadgets 部件支持
BuildRequires: libggadget-devel >= 0.11.0
BuildRequires: libggadget-qt-devel >= 0.11.0
# plasma qedje 部件支持
BuildRequires: eet-devel >= 1.1.0
BuildRequires: qzion-devel >= 0.4.0
BuildRequires: qedje-devel >= 0.4.0
# policykit 整合
BuildRequires: polkit-qt-1-devel >= 0.9.2
BuildRequires: libqalculate-devel
BuildRequires: xmms-devel
BuildRequires: gpsd-devel
# akonadi
BuildRequires: akonadi-devel
BuildRequires: prison-devel
BuildRequires: libkdepimlibs4-devel
BuildRequires: mesa-libGLES-devel
BuildRequires: mesa-libEGL-devel

BuildRequires: xcb-util-renderutil-devel
BuildRequires: xcb-util-image-devel

Requires: kdebase4-runtime
Requires: libkdelibs4
Requires: libkdepimlibs4

# FIXME: for post installation requirement
BuildRequires: ImageMagick
Requires: ImageMagick

# kde upnp deamon, move to kdebase-runtime? --- nihui
Requires: cagibi

Obsoletes: magic-kdm4-config <= 4.3

%description
This package contains the basic packages for a K Desktop Environment
workspace.

%description -l zh_CN.UTF-8
K 桌面环境工作空间的基本程序包。

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
%package devel
Summary: The KDE Workspace Components
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Requires: libkdelibs4-devel
Requires: libkdepimlibs4-devel
Requires: kdebase4-workspace >= %{version}
Requires: kdebase4-runtime-devel >= %{version}

%description devel
This package contains the basic packages for a K Desktop Environment
workspace.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
%package -n kde4-kdm
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: KDE login and display manager
Summary(zh_CN.UTF-8): KDE 的登录和显示管理器
Requires: kdebase4-runtime

%description -n kde4-kdm
This package contains kdm, the login and session manager for KDE.

%description -n kde4-kdm
KDE 的登录和显示管理器。

%if 0
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
%package googlegadgets
Summary: Google Desktop Gadgets
Summary(zh_CN.UTF-8): Google 桌面部件
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面

%description googlegadgets
%{summary}.

%description googlegadgets -l zh_CN.UTF-8
Google 桌面部件。
%endif

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
%package python-applet
Summary: Plasma widget in Python
Summary(zh_CN.UTF-8): Plasma Python 部件支持
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Requires: PyKDE4 >= %{version}

%description python-applet
%{summary}.

%description python-applet -l zh_CN.UTF-8
Plasma Python 部件支持。

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
%package qedje
Summary: Plasma widget in qedje
Summary(zh_CN.UTF-8): Plasma qedje 部件支持
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面

%description qedje
%{summary}.

%description qedje -l zh_CN.UTF-8
Plasma qedje 部件支持。

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
%package akonadi
Summary: KDE Workspace Components akonadi support files
Summary(zh_CN.UTF-8): KDE 工作空间 akonadi 支持文件
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面

%description akonadi
%{summary}.

%description akonadi -l zh_CN.UTF-8
KDE 工作空间 akonadi 支持文件。

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
%package nepomuk
Summary: KDE Workspace Components nepomuk support files
Summary(zh_CN.UTF-8): KDE 工作空间 nepomuk 支持文件
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面

%description nepomuk
%{summary}.

%description nepomuk -l zh_CN.UTF-8
KDE 工作空间 nepomuk 支持文件。

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
%package wallpapers
Summary: KDE wallpapers
Summary(zh_CN.UTF-8): KDE 的墙纸
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面

%description wallpapers
%{summary}.

%description wallpapers -l zh_CN.UTF-8
KDE 的墙纸。

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
%if %build_wallpaper_smallsize
%package wallpapers-smallsize
Summary: KDE wallpapers
Summary(zh_CN.UTF-8): KDE 的墙纸小体积版本
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Provides: kdebase4-workspace-wallpapers = %{version}-%{release}
Requires: ImageMagick

%description wallpapers-smallsize
%{summary}.

%description wallpapers-smallsize -l zh_CN.UTF-8
KDE 的墙纸。小体积版本。

%endif
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
%package -n oxygen-cursor-themes
Summary: Oxygen cursor themes
Summary(zh_CN.UTF-8): Oxygen 光标主题
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面

%description -n oxygen-cursor-themes
%{summary}.

%description -n oxygen-cursor-themes -l zh_CN.UTF-8
Oxygen 光标主题。

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

%package -n ksysguard
Summary: KDE System Monitor
Requires: ksysguardd = %{version}-%{release}
Requires: ksysguard-libs%{?_isa} = %{version}-%{release}
%description -n ksysguard
%{summary}.

%package -n ksysguard-libs
Summary: Runtime libraries for ksysguard
# when spilt occurred
Conflicts: kdebase-workspace-libs < 4.7.2-2
Requires: kdelibs4%{?_isa} >= %{version}
%description -n ksysguard-libs
%{summary}.

%package -n ksysguardd
Summary: Performance monitor daemon
%description -n ksysguardd
%{summary}.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

%prep
%setup -q -n %{real_name}-4.11.8

%patch60 -p1

#%patch82
#%patch85

%patch2 -p1
%patch3 -p1
%patch4 -p1 -b .klipper-url
%patch5 -p1 -b .rootprivs
#%patch6 -p1 -b .showremainingtime
%patch7 -p1
%patch8 -p1
%patch19 -p1 -b .kdm_plymouth
%patch20 -p1 -b .xsession_errors_O_APPEND
%patch21 -p1 -b .platformplugin-widgetstyle4
%patch25 -p1 -b .bz#747982-launchers
%patch26 -p1 -b .systray_org.kde.ktp-presence
#%patch27 -p1 -b .kdm_logind

# upstreamable patches
#%patch50 -p1 -b .kde#171685
#%patch52 -p1 -b .bz#732830-login
#%patch53 -p1 -b .kdm_xauth
#%patch54 -p1 -b .kcm_fonts_dont_change_on_load
#%patch55 -p1 -b .BUILD_KCM_RANDR
#%patch57 -p1 -b .bug796969
#%patch63 -p1 -b .systemd-displaymanager


%patch301 -p1

#%patch413 -p1
pushd plasma/desktop
#%patch419 -p2
popd
%patch463 -p1

#%patch704 -p1

%patch104 -p1
#以下部分需要更新!!!!
#pushd plasma
#%patch106 -p0
#popd
%patch107 -p1 -b .orig
#%patch108 -p0
# FIXME: rediff needed !
%patch109 -p1
%patch110 -p1

%patch111 -p1
%patch112 -p1


%build
mkdir build
cd build
%cmake_kde4 \
    -DPYTHON_SITE_PACKAGES_INSTALL_DIR=%{python_sitearch} \
    -DKDE4_KDM_PAM_SERVICE=kdm \
    -DKDE4_KCHECKPASS_PAM_SERVICE=kcheckpass \
    -DKDE4_KSCREENSAVER_PAM_SERVICE=kscreensaver ..

make %{?_smp_mflags}

%install
cd build
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

# install pam modules
install -D -m644 %{SOURCE10} %{buildroot}%{_sysconfdir}/pam.d/kcheckpass
install -D -m644 %{SOURCE11} %{buildroot}%{_sysconfdir}/pam.d/kdm
install -D -m644 %{SOURCE12} %{buildroot}%{_sysconfdir}/pam.d/kdm-np
install -D -m644 %{SOURCE13} %{buildroot}%{_sysconfdir}/pam.d/kscreensaver

%clean_kde4_desktop_files
%clean_kde4_notifyrc_files
%adapt_kde4_notifyrc_files

# trash the default ksplash theme background images
# we will generate them from kdm theme background image in post installation
for i in 1024x768 1280x1024 1600x1200 1920x1200 600x400 800x600; do
    rm -f %{buildroot}%{kde4_appsdir}/ksplash/Themes/Simple/$i/background.png;
done

mkdir -p %{buildroot}%{kde4_appsdir}/ksplash/Themes/Simple/1920x1200/
cp %{SOURCE3} %{buildroot}%{kde4_appsdir}/ksplash/Themes/Simple/1920x1200/background.png

# 不进行 etc 目录的配置文件转移
#  mkdir -p $RPM_BUILD_ROOT/etc
#  mv $RPM_BUILD_ROOT/usr/etc/ksysguarddrc $RPM_BUILD_ROOT/etc/
#  mv $RPM_BUILD_ROOT/usr/etc/systemsettingsrc $RPM_BUILD_ROOT/etc/

# oxygen 墙纸补遗
#tar -xf %{SOURCE1} -C %{buildroot}%{kde4_datadir}/wallpapers/

# for New_Air wallpaper
mkdir -p %{buildroot}%{kde4_datadir}/wallpapers/New_Air/contents/images/
cp %{SOURCE4} %{buildroot}%{kde4_datadir}/wallpapers/New_Air/contents/images/1600x1200.jpg
cp %{SOURCE5} %{buildroot}%{kde4_datadir}/wallpapers/New_Air/metadata.desktop
pushd %{buildroot}%{kde4_datadir}/wallpapers/New_Air/contents/images/
    convert -resize 1024x768^ -gravity Center -crop 1024x768+0+0 +repage 1600x1200.jpg 1024x768.jpg
    convert -resize 1440x900 1600x1200.jpg 1440x900.jpg
    convert -resize 1280x800 1600x1200.jpg 1280x800.jpg
    convert -resize 1280x1024^ -gravity Center -crop 1280x1024+0+0 +repage 1600x1200.jpg 1280x1024.jpg
# generate screen shot image
    convert -resize 400x250^ -gravity Center -crop 400x250+0+0 +repage 1600x1200.jpg ../screenshot.png
popd

# 安装 kwin 装饰 logo
#cp %{SOURCE2} %{buildroot}%{kde4_appsdir}/kwin/magic.png

# 安装 xseesion 支持菜单项
mkdir -p %{buildroot}%{_datadir}/xsessions/
cp %{buildroot}%{kde4_appsdir}/kdm/sessions/kde-plasma.desktop %{buildroot}%{_datadir}/xsessions/kde4.desktop
# 将 KDE 更改为 KDE 4
sed -i s/Name\=KDE/Name\=KDE\ 4/g %{buildroot}%{_datadir}/xsessions/kde4.desktop

%post
/usr/sbin/ldconfig
# generate ksplash background images
echo "Generating ksplash background images..."
pushd "%{kde4_appsdir}"
convert -resize 1600x1200^ -gravity Center -crop 1600x1200+0+0 +repage ksplash/Themes/Simple/1920x1200/background.png \
    ksplash/Themes/Simple/1600x1200/background.png
convert -resize 1024x768^ -gravity Center -crop 1024x768+0+0 +repage ksplash/Themes/Simple/1920x1200/background.png \
    ksplash/Themes/Simple/1024x768/background.png
convert -resize 1280x1024^ -gravity Center -crop 1280x1024+0+0 +repage ksplash/Themes/Simple/1920x1200/background.png \
    ksplash/Themes/Simple/1280x1024/background.png
convert -resize 600x400^ -gravity Center -crop 600x400+0+0 +repage ksplash/Themes/Simple/1920x1200/background.png \
    ksplash/Themes/Simple/600x400/background.png
convert -resize 800x600^ -gravity Center -crop 800x600+0+0 +repage ksplash/Themes/Simple/1920x1200/background.png \
    ksplash/Themes/Simple/800x600/background.png
popd

magic_rpm_clean.sh

%postun -p /usr/sbin/ldconfig

%post -n kde4-kdm
%{_bindir}/genkdmconf
#if test -f /etc/sysconfig/displaymanager ; then
#  . /etc/sysconfig/displaymanager
#fi
#if test -n "$KDM_SHUTDOWN" ; then
#  if test "$KDM_SHUTDOWN" = "local" ; then
#    KDM_SHUTDOWN=all
#  fi
#  case "$KDM_SHUTDOWN" in
#  "auto" | "none" | "root")
#    sed -i -e "s/^DISPLAYMANAGER_SHUTDOWN=.*/DISPLAYMANAGER_SHUTDOWN=\"$KDM_SHUTDOWN\"/" /etc/sysconfig/displaymanager
#    ;;
#  esac
#fi
/usr/sbin/ldconfig

%postun -n kde4-kdm
/usr/sbin/ldconfig

%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files devel
%defattr(-,root,root)
%{kde4_includedir}/*
%{kde4_appsdir}/cmake
%{kde4_libdir}/*.so
# internal cmake module
%{kde4_libdir}/cmake
%{kde4_plugindir}/plugins/designer/ksysguardwidgets.so
%{kde4_plugindir}/plugins/designer/ksysguardlsofwidgets.so
%{kde4_plugindir}/plugins/designer/ksignalplotterwidgets.so

%exclude %{kde4_libdir}/libkdeinit4_kwin*.so
%exclude %{kde4_libdir}/libkdeinit4_ksysguard.so
%exclude %{kde4_libdir}/libkdeinit4_kcminit.so
%exclude %{kde4_libdir}/libkdeinit4_kcminit_startup.so
%exclude %{kde4_libdir}/libkdeinit4_krunner.so
%exclude %{kde4_libdir}/libkdeinit4_plasma-desktop.so
%exclude %{kde4_libdir}/libkdeinit4_plasma-netbook.so
%exclude %{kde4_libdir}/libkdeinit4_plasma-windowed.so
%exclude %{kde4_libdir}/libkdeinit4_kaccess.so
%exclude %{kde4_libdir}/libkdeinit4_kmenuedit.so
%exclude %{kde4_libdir}/libkdeinit4_ksmserver.so
%exclude %{kde4_libdir}/libkdeinit4_klipper.so
#FIXME: unversioned library
%exclude %{kde4_libdir}/libkickoff.so


%files -n kde4-kdm
%defattr(-,root,root)
%{_sysconfdir}/pam.d/kdm
%{_sysconfdir}/pam.d/kdm-np
%{kde4_bindir}/genkdmconf
%{kde4_bindir}/kdm
%{kde4_bindir}/kdmctl
%{kde4_plugindir}/libexec/kdm_config
%{kde4_plugindir}/libexec/kdm_greet
%{kde4_plugindir}/libexec/krootimage
## from universe
%{kde4_plugindir}/kgreet_classic.so
%{kde4_plugindir}/kgreet_generic.so
%{kde4_plugindir}/kgreet_winbind.so
## from kcontrol
%{kde4_plugindir}/libexec/kcmkdmhelper
%{_sysconfdir}/dbus-1/system.d/org.kde.kcontrol.kcmkdm.conf
%{kde4_dbus_system_servicesdir}/org.kde.kcontrol.kcmkdm.service
#%{kde4_auth_policy_filesdir}/org.kde.kcontrol.kcmkdm.policy
%{kde4_plugindir}/kcm_kdm.so
%dir %{kde4_configdir}/kdm
%{kde4_configdir}/kdm/*
%config %{kde4_configdir}/kdm.knsrc
%dir %{kde4_appsdir}/doc
%dir %{kde4_appsdir}/doc/kdm
%{kde4_appsdir}/doc/kdm/*
%{kde4_appsdir}/kdm
%{kde4_servicesdir}/kdm.desktop
%doc %lang(en) %{kde4_htmldir}/en/kdm
# default kdm background
%{kde4_datadir}/wallpapers/stripes.*
# kdm-kde3
%{_datadir}/xsessions/kde4.desktop

%if 0
%files googlegadgets
%defattr(-,root,root,-)
%{kde4_plugindir}/plasma_package_ggl.so
%{kde4_plugindir}/plasma_scriptengine_ggl.so
%{kde4_servicesdir}/*googlegadgets.desktop
%endif

%files python-applet
%defattr(-,root,root,-)
%{python_sitearch}/PyKDE4/plasmascript.py*
%{kde4_appsdir}/plasma_scriptengine_python
%{kde4_servicesdir}/plasma-scriptengine*python.desktop

%files akonadi
%defattr(-,root,root,-)
%{kde4_plugindir}/plasma_engine_akonadi.so
%{kde4_plugindir}/plasma_engine_calendar.so
%{kde4_servicesdir}/plasma-engine-akonadi.desktop
%{kde4_servicesdir}/plasma-dataengine-calendar.desktop

%files nepomuk
%defattr(-,root,root,-)
%{kde4_plugindir}/krunner_nepomuksearchrunner.so
%{kde4_servicesdir}/plasma-runner-nepomuksearch.desktop
%{kde4_plugindir}/plasma_engine_metadata.so
%{kde4_servicesdir}/plasma-engine-metadata.desktop

%files wallpapers
%defattr(-,root,root,-)
%{kde4_datadir}/wallpapers/*
# exclude for kdm default background
%exclude %{kde4_datadir}/wallpapers/stripes.*

%if %build_wallpaper_smallsize
%files wallpapers-smallsize
%defattr(-,root,root,-)
#%{kde4_datadir}/wallpapers/*/contents/images/1920x1200.*
%{kde4_datadir}/wallpapers/*/metadata.desktop
%{kde4_datadir}/wallpapers/New_Air/contents/images/1600x1200.jpg
%endif

%files -n oxygen-cursor-themes
%defattr(-,root,root,-)
%{kde4_iconsdir}/Oxygen_Black/
%{kde4_iconsdir}/Oxygen_Blue/
%{kde4_iconsdir}/Oxygen_White/
%{kde4_iconsdir}/Oxygen_Yellow/
%{kde4_iconsdir}/Oxygen_Zion/

%files
%defattr(-,root,root)
######################################### kwin
%{kde4_bindir}/kwin*
%{kde4_libdir}/kconf_update_bin/kwin_update_*
%{kde4_plugindir}/kcm_kwin*.so
%{kde4_plugindir}/kwin*.so
%{kde4_libdir}/libkdeinit4_kwin*.so
%{kde4_libdir}/libkdecorations.so.*
%{kde4_plugindir}/imports/org/kde/kwin/decoration/*
%{kde4_plugindir}/imports/org/kde/kwin/decorations/*
%{kde4_libdir}/libkwineffects.so.*
#%{kde4_libdir}/libkwinnvidiahack.so.*
%{kde4_plugindir}/libexec/kwin_killer_helper
%{kde4_plugindir}/libexec/kwin_opengl_test
%{kde4_plugindir}/libexec/kwin_rules_dialog
%doc %lang(en) %{kde4_htmldir}/en/kcontrol/kwin*
%{kde4_iconsdir}/oxygen/*/apps/kcmkwm.*
%{kde4_iconsdir}/oxygen/*/apps/kwin.*
%{kde4_appsdir}/kconf_update/kwin*.*
#%{kde4_appsdir}/kconf_update/on-off_to_true-false.sh
#%{kde4_appsdir}/kconf_update/pluginlibFix.pl
%{kde4_appsdir}/kwin
%{kde4_kcfgdir}/kwin.kcfg
%{kde4_servicesdir}/desktop.desktop
%{kde4_servicesdir}/kwin*
%{kde4_servicetypesdir}/kwineffect.desktop
%{kde4_datadir}/sounds/pop.wav
%{kde4_dbus_interfacesdir}/org.kde.KWin.xml
######################################### ksysguard
%{_sysconfdir}/dbus-1/system.d/org.kde.ksysguard.processlisthelper.conf
%{kde4_dbus_system_servicesdir}/org.kde.ksysguard.processlisthelper.service
#%{kde4_auth_policy_filesdir}/org.kde.ksysguard.processlisthelper.policy

%{kde4_iconsdir}/KDE_Classic/*

%{kde4_bindir}/ksysguard
#%{kde4_bindir}/setscheduler
%{kde4_plugindir}/libexec/ksysguardprocesslist_helper
%{kde4_libdir}/libkdeinit4_ksysguard.so
%{kde4_libdir}/libksgrd.so.*
%{kde4_libdir}/liblsofui.so.*
%{kde4_libdir}/libksignalplotter.so.*
%{kde4_libdir}/libprocesscore.so.*
%{kde4_libdir}/libprocessui.so.*
%{kde4_iconsdir}/oxygen/16x16/apps/computer.png
%{kde4_iconsdir}/oxygen/16x16/apps/daemon.png
%{kde4_iconsdir}/oxygen/16x16/apps/kdeapp.png
%{kde4_iconsdir}/oxygen/16x16/apps/kernel.png
%{kde4_iconsdir}/oxygen/16x16/apps/running.png
%{kde4_iconsdir}/oxygen/16x16/apps/shell.png
%{kde4_iconsdir}/oxygen/16x16/apps/unknownapp.png
%{kde4_iconsdir}/oxygen/16x16/apps/waiting.png
######################################### kcminit
%{kde4_bindir}/kcminit
%{kde4_bindir}/kcminit_startup
%{kde4_libdir}/libkdeinit4_kcminit.so
%{kde4_libdir}/libkdeinit4_kcminit_startup.so
######################################### kscreensaver
%{_sysconfdir}/pam.d/kscreensaver
%{kde4_bindir}/kblankscrn.kss
%{kde4_bindir}/krandom.kss
%{kde4_libdir}/libkscreensaver.so.*
%{kde4_servicesdir}/ScreenSavers/kblank.desktop
%{kde4_servicesdir}/ScreenSavers/krandom.desktop
%{kde4_servicetypesdir}/screensaver.desktop
######################################### khotkeys
%{kde4_plugindir}/kcm_hotkeys.so
%{kde4_plugindir}/kded_khotkeys.so
%{kde4_libdir}/libkhotkeysprivate.so.*
%{kde4_appsdir}/khotkeys
%{kde4_dbus_interfacesdir}/org.kde.khotkeys.xml
%{kde4_servicesdir}/khotkeys.desktop
%{kde4_servicesdir}/kded/khotkeys.desktop
# come from systemsettings file list
# %{kde4_servicesdir}/settings-input-actions.desktop
######################################## kcheckpass
%{_sysconfdir}/pam.d/kcheckpass
%{kde4_plugindir}/libexec/kcheckpass
######################################## krunner
%{kde4_bindir}/krunner
%{kde4_libdir}/libkdeinit4_krunner.so
%{kde4_datadir}/autostart/krunner.desktop
%{kde4_kcfgdir}/klaunch.kcfg
#%{kde4_kcfgdir}/kscreensaversettings.kcfg
#%{kde4_dbus_interfacesdir}/org.freedesktop.ScreenSaver.xml
%{kde4_dbus_interfacesdir}/org.kde.krunner.App.xml
#%{kde4_dbus_interfacesdir}/org.kde.screensaver.xml
%{kde4_dbus_servicesdir}/org.kde.krunner.service
######################################## plasma
%{kde4_bindir}/plasma-desktop
%{kde4_bindir}/plasma-netbook
%{kde4_bindir}/plasma-overlay
%{kde4_bindir}/plasma-windowed
%{kde4_appsdir}/plasma/*
#%{kde4_bindir}/plasmaengineexplorer
#%{kde4_bindir}/plasmawallpaperviewer
#%{kde4_bindir}/plasmoidviewer
%{kde4_libdir}/kconf_update_bin/plasma-add-shortcut-to-menu
%{kde4_libdir}/kconf_update_bin/plasma-to-plasma-desktop
%{kde4_plugindir}/kcm_desktoptheme.so
%{kde4_plugindir}/kcm_krunner_kill.so
%{kde4_plugindir}/kcm_workspaceoptions.so
%{kde4_plugindir}/kded_freespacenotifier.so
%{kde4_plugindir}/kded_kephal.so
%{kde4_plugindir}/kded_statusnotifierwatcher.so
%{kde4_plugindir}/krunner_*.so
%{kde4_plugindir}/ion_*.so
%{kde4_plugindir}/plasma_*.so
%{kde4_plugindir}/plasma-geolocation-*.so
#%{kde4_plugindir}/libexec/kscreenlocker
%{kde4_libdir}/libkdeinit4_plasma-desktop.so
%{kde4_libdir}/libkdeinit4_plasma-netbook.so
%{kde4_libdir}/libkdeinit4_plasma-windowed.so
%{kde4_libdir}/libkephal.so.*
%{kde4_libdir}/libkworkspace.so.*
%{kde4_libdir}/libplasma_applet-system-monitor.so.*
%{kde4_libdir}/libplasmaclock.so.*
%{kde4_libdir}/libplasmagenericshell.so.*
%{kde4_libdir}/libplasma-geolocation-interface.so.*
%{kde4_libdir}/libtaskmanager.so.*
#%{kde4_libdir}/libtime_solar.so.*
%{kde4_libdir}/libweather_ion.so.*
# FIXME: unversioned library
%{kde4_libdir}/libkickoff.so
%{kde4_appsdir}/desktoptheme/default
%{kde4_appsdir}/desktoptheme/air-netbook
%{kde4_appsdir}/kconf_update/plasma-add-shortcut-to-menu.upd
%{kde4_appsdir}/kconf_update/plasma-to-plasmadesktop-shortcuts.upd
%{kde4_appsdir}/kconf_update/plasmarc-to-plasmadesktoprc.upd
#%{kde4_appsdir}/plasma/dashboard
#%{kde4_appsdir}/plasma/layout-templates/*
#%{kde4_appsdir}/plasma/services/*.operations
%{kde4_appsdir}/plasma-desktop/*
%{kde4_appsdir}/plasma-netbook/*
%{kde4_appsdir}/plasma_scriptengine_*
%{kde4_datadir}/autostart/plasma.desktop
%{kde4_datadir}/autostart/plasma-desktop.desktop
%{kde4_kcfgdir}/plasma-shell-desktop.kcfg
%config %{kde4_configdir}/plasma-overlayrc
%config %{kde4_configdir}/plasma-themes.knsrc
%config %{kde4_configdir}/wallpaper.knsrc
%doc %lang(en) %{kde4_htmldir}/en/plasma-desktop
%doc %lang(en) %{kde4_htmldir}/en/kcontrol/desktopthemedetails
%doc %lang(en) %{kde4_htmldir}/en/kcontrol/desktop
%doc %lang(en) %{kde4_htmldir}/en/kcontrol/workspaceoptions
%doc %lang(en) %{kde4_htmldir}/en/kcontrol/khotkeys
#%doc %lang(en) %{kde4_htmldir}/en/kcontrol/multiplemonitors
%{kde4_servicesdir}/desktoptheme.desktop
%{kde4_servicesdir}/ion-*.desktop
%{kde4_servicesdir}/plasma-*.desktop
%{kde4_servicesdir}/plasma_applet_keyboard.desktop
%{kde4_servicesdir}/plasma_engine_statusnotifieritem.desktop
%{kde4_servicesdir}/workspaceoptions.desktop
%{kde4_servicesdir}/recentdocuments.desktop
%{kde4_servicesdir}/kded/freespacenotifier.desktop
%{kde4_servicesdir}/kded/kephal.desktop
%{kde4_servicesdir}/kded/statusnotifierwatcher.desktop
%{kde4_servicetypesdir}/plasma-layout-template.desktop
%{kde4_servicetypesdir}/plasma-sal-menu.desktop
%{kde4_servicetypesdir}/plasma-geolocationprovider.desktop
#%{kde4_mandir}/man1/plasmaengineexplorer.1*

%{kde4_appsdir}/katepart/syntax/plasma-desktop-js.xml

# googlegadgets
#%exclude %{kde4_plugindir}/plasma_package_ggl.so
#%exclude %{kde4_plugindir}/plasma_scriptengine_ggl.so
#%exclude %{kde4_servicesdir}/*googlegadgets.desktop

# these things need python bindings
%exclude %{kde4_appsdir}/plasma_scriptengine_python
%exclude %{kde4_servicesdir}/plasma-scriptengine*python.desktop

# qedje sub package
#%exclude %{kde4_plugindir}/plasma_appletscript_qedje.so
#%exclude %{kde4_plugindir}/plasma_package_qedje.so
#%exclude %{kde4_servicesdir}/plasma-appletscript-qedje.desktop
#%exclude %{kde4_servicesdir}/plasma-packagestructure-qedje.desktop

# akonadi sub package
%exclude %{kde4_plugindir}/plasma_engine_akonadi.so
%exclude %{kde4_plugindir}/plasma_engine_calendar.so
%exclude %{kde4_servicesdir}/plasma-engine-akonadi.desktop
%exclude %{kde4_servicesdir}/plasma-dataengine-calendar.desktop

# nepomuk sub package
%exclude %{kde4_plugindir}/krunner_nepomuksearchrunner.so
%exclude %{kde4_servicesdir}/plasma-runner-nepomuksearch.desktop
%exclude %{kde4_plugindir}/plasma_engine_metadata.so
%exclude %{kde4_servicesdir}/plasma-engine-metadata.desktop


######################################## systemsettings
%{kde4_bindir}/systemsettings
%{kde4_plugindir}/classic_mode.so
%{kde4_plugindir}/icon_mode.so
%{kde4_libdir}/libsystemsettingsview.so.*
%{kde4_appsdir}/systemsettings
%{kde4_xdgappsdir}/systemsettings.desktop
%{kde4_servicesdir}/settings-*.desktop
%{kde4_servicetypesdir}/systemsettingsexternalapp.desktop
%{kde4_servicetypesdir}/systemsettingscategory.desktop
%{kde4_servicetypesdir}/systemsettingsview.desktop
%doc %lang(en) %{kde4_htmldir}/en/systemsettings
# exclude to khotkeys
# %{kde4_servicesdir}/settings-input-actions.desktop
######################################## powerdevil
%{kde4_plugindir}/kded_powerdevil.so
%{kde4_plugindir}/kcm_powerdevil*.so
%{kde4_plugindir}/powerdevil*.so
%{kde4_libdir}/libpowerdevil*.so.*
%{kde4_appsdir}/powerdevil
%{kde4_dbus_system_servicesdir}/org.kde.powerdevil.backlighthelper.service
#%{kde4_dbus_interfacesdir}/org.kde.PowerDevil.xml
%{kde4_servicesdir}/kded/powerdevil.desktop
%{kde4_servicesdir}/powerdevil*.desktop
%{kde4_servicetypesdir}/powerdevil*.desktop
%{kde4_auth_policy_filesdir}/org.kde.powerdevil.backlighthelper.policy
%{_sysconfdir}/dbus-1/system.d/org.kde.powerdevil.backlighthelper.conf
%doc %lang(en) %{kde4_htmldir}/en/kcontrol/powerdevil
######################################## kcontrol related
%{_sysconfdir}/dbus-1/system.d/org.kde.kcontrol.kcmclock.conf
%{kde4_dbus_system_servicesdir}/org.kde.kcontrol.kcmclock.service
%{kde4_auth_policy_filesdir}/org.kde.kcontrol.kcmclock.policy
%{kde4_auth_policy_filesdir}/org.kde.kcontrol.kcmkdm.policy
%{_sysconfdir}/dbus-1/system.d/org.kde.fontinst.conf
%{kde4_dbus_system_servicesdir}/org.kde.fontinst.service
#%{kde4_auth_policy_filesdir}/org.kde.fontinst.policy

%{kde4_bindir}/kaccess
%{kde4_bindir}/kapplymousetheme
%{kde4_bindir}/kfontinst
%{kde4_bindir}/kfontview
%{kde4_bindir}/krandrtray
%{kde4_bindir}/krdb
#%{kde4_bindir}/kxkb
%{kde4_bindir}/oxygen-demo
%{kde4_bindir}/oxygen-settings
%{kde4_libdir}/liboxygenstyle.so.*
%{kde4_libdir}/kconf_update_bin/krdb_clearlibrarypath
%{kde4_plugindir}/fontthumbnail.so
%{kde4_plugindir}/kcm_access.so
%{kde4_plugindir}/kcm_autostart.so
%{kde4_plugindir}/kcm_bell.so
%{kde4_plugindir}/kcm_clock.so
%{kde4_plugindir}/kcm_colors.so
%{kde4_plugindir}/kcm_desktoppaths.so
%{kde4_plugindir}/kcm_display.so
%{kde4_plugindir}/kcm_fonts.so
%{kde4_plugindir}/kcm_fontinst.so
%{kde4_plugindir}/kcm_input.so
%{kde4_plugindir}/kcm_joystick.so
%{kde4_plugindir}/kcm_keyboard.so
#%{kde4_plugindir}/kcm_keyboard_layout.so
%{kde4_plugindir}/kcm_keys.so
%{kde4_plugindir}/kcm_launch.so
%{kde4_plugindir}/kcm_randr.so
%{kde4_plugindir}/kcm_screensaver.so
%{kde4_plugindir}/kcm_standard_actions.so
%{kde4_plugindir}/kcm_style.so
#%{kde4_plugindir}/kcm_xinerama.so
%{kde4_plugindir}/kded_randrmonitor.so
%{kde4_plugindir}/kded_keyboard.so
%{kde4_plugindir}/keyboard_layout_widget.so
%{kde4_plugindir}/kfontviewpart.so
%{kde4_plugindir}/kio_fonts.so
#%{kde4_plugindir}/kstyle_keramik_config.so
%{kde4_plugindir}/kstyle_oxygen_config.so
%{kde4_plugindir}/libexec/kcmdatetimehelper
%{kde4_plugindir}/libexec/fontinst
%{kde4_plugindir}/libexec/fontinst_helper
%{kde4_plugindir}/libexec/fontinst_x11
%{kde4_plugindir}/libexec/kfontprint
#%{kde4_plugindir}/libexec/test_kcm_xinerama
%{kde4_plugindir}/plugins/styles/oxygen.so
%{kde4_libdir}/libkdeinit4_kaccess.so
#%{kde4_libdir}/libkdeinit4_kxkb.so
%{kde4_libdir}/libkfontinst.so.*
%{kde4_libdir}/libkfontinstui.so.*
%{kde4_libdir}/strigi/strigita_font.so
%{kde4_xdgappsdir}/kfontview.desktop
%{kde4_xdgappsdir}/krandrtray.desktop
%{kde4_appsdir}/color-schemes/*.colors
%{kde4_appsdir}/kaccess
%{kde4_appsdir}/kcminput
%{kde4_appsdir}/kcmkeys/*.kksrc
#%{kde4_appsdir}/kconf_update/convertShortcuts.pl
#%{kde4_appsdir}/kconf_update/kaccel.upd
#%{kde4_appsdir}/kconf_update/kcmdisplayrc.upd
#%{kde4_appsdir}/kconf_update/krdb.upd
#%{kde4_appsdir}/kconf_update/mouse_cursor_theme.upd
%{kde4_appsdir}/kcontrol/pics/*.png
%{kde4_appsdir}/kdisplay/app-defaults/*.ad
%{kde4_appsdir}/kfontinst
%{kde4_appsdir}/kfontview
%{kde4_appsdir}/konqsidebartng/virtual_folders/services/fonts.desktop
%{kde4_appsdir}/kstyle/themes/*.themerc
%{kde4_appsdir}/kthememanager/themes
%{kde4_dbus_servicesdir}/org.kde.fontinst.service
%config %{kde4_configdir}/background.knsrc
%config %{kde4_configdir}/colorschemes.knsrc
#%{kde4_iconsdir}/hicolor/*/apps/kxkb.*
%{kde4_iconsdir}/oxygen/*/mimetypes/fonts-package.*
%{kde4_iconsdir}/oxygen/*/apps/kfontview.*
%{kde4_iconsdir}/oxygen/*/apps/preferences-desktop-font-installer.*
%{kde4_servicesdir}/autostart.desktop
%{kde4_servicesdir}/bell.desktop
%{kde4_servicesdir}/clock.desktop
%{kde4_servicesdir}/colors.desktop
%{kde4_servicesdir}/display.desktop
%{kde4_servicesdir}/desktoppath.desktop
%{kde4_servicesdir}/fontinst.desktop
%{kde4_servicesdir}/fonts.desktop
%{kde4_servicesdir}/fonts.protocol
%{kde4_servicesdir}/fontthumbnail.desktop
%{kde4_servicesdir}/joystick.desktop
%{kde4_servicesdir}/kaccess.desktop
%{kde4_servicesdir}/kcmaccess.desktop
%{kde4_servicesdir}/kcmlaunch.desktop
#%{kde4_servicesdir}/keyboard.desktop
%{kde4_servicesdir}/kcm_keyboard.desktop
#%{kde4_servicesdir}/keyboard_layout.desktop
%{kde4_servicesdir}/keys.desktop
%{kde4_servicesdir}/kfontviewpart.desktop
%{kde4_servicesdir}/mouse.desktop
%{kde4_servicesdir}/randr.desktop
%{kde4_servicesdir}/kded/keyboard.desktop
%{kde4_servicesdir}/kded/randrmonitor.desktop
%{kde4_servicesdir}/screensaver.desktop
%{kde4_servicesdir}/standard_actions.desktop
%{kde4_servicesdir}/style.desktop
#%{kde4_servicesdir}/xinerama.desktop
%{kde4_servicesdir}/ServiceMenus/installfont.desktop
%doc %lang(en) %{kde4_htmldir}/en/kfontview
#%doc %lang(en) %{kde4_htmldir}/en/kxkb
%doc %lang(en) %{kde4_htmldir}/en/kcontrol/autostart
%doc %lang(en) %{kde4_htmldir}/en/kcontrol/bell
%doc %lang(en) %{kde4_htmldir}/en/kcontrol/clock
%doc %lang(en) %{kde4_htmldir}/en/kcontrol/colors
%doc %lang(en) %{kde4_htmldir}/en/kcontrol/fontinst
%doc %lang(en) %{kde4_htmldir}/en/kcontrol/fonts
%doc %lang(en) %{kde4_htmldir}/en/kcontrol/joystick
%doc %lang(en) %{kde4_htmldir}/en/kcontrol/kcmaccess
#%doc %lang(en) %{kde4_htmldir}/en/kcontrol/kcmdisplay
%doc %lang(en) %{kde4_htmldir}/en/kcontrol/kcmstyle
%doc %lang(en) %{kde4_htmldir}/en/kcontrol/keyboard
%doc %lang(en) %{kde4_htmldir}/en/kcontrol/keys
%doc %lang(en) %{kde4_htmldir}/en/kcontrol/mouse
%doc %lang(en) %{kde4_htmldir}/en/kcontrol/paths
%doc %lang(en) %{kde4_htmldir}/en/kcontrol/screensaver
%doc %lang(en) %{kde4_htmldir}/en/kcontrol/splashscreen
%doc %lang(en) %{kde4_htmldir}/en/kcontrol/windowbehaviour
%doc %lang(en) %{kde4_htmldir}/en/kcontrol/windowspecific
############################################ kmenuedit
%{kde4_bindir}/kmenuedit
%{kde4_libdir}/libkdeinit4_kmenuedit.so
%{kde4_appsdir}/kmenuedit
%{kde4_iconsdir}/hicolor/*/apps/kmenuedit.*
%{kde4_xdgappsdir}/kmenuedit.desktop
%doc %lang(en) %{kde4_htmldir}/en/kmenuedit
############################################ ksmserver
%{kde4_bindir}/kcheckrunning
%{kde4_bindir}/ksmserver
%{kde4_plugindir}/kcm_smserver.so
%{kde4_libdir}/libkdeinit4_ksmserver.so
%{kde4_appsdir}/ksmserver/*
#%{kde4_appsdir}/kconf_update/ksmserver.upd
%{kde4_appsdir}/kconf_update/ksmserver_shortcuts.upd
#%{kde4_appsdir}/kconf_update/move_session_config.sh
%{kde4_dbus_interfacesdir}/org.kde.KSMServerInterface.xml
%{kde4_servicesdir}/kcmsmserver.desktop
%doc %lang(en) %{kde4_htmldir}/en/kcontrol/kcmsmserver
############################################ ksplash
%{kde4_bindir}/ksplashsimple
%{kde4_bindir}/ksplashx
%{kde4_bindir}/ksplashx_scale
%{kde4_plugindir}/kcm_ksplashthemes.so
%{kde4_appsdir}/ksplash/Themes
%config %{kde4_configdir}/ksplash.knsrc
%{kde4_iconsdir}/hicolor/*/apps/ksplash.*
%{kde4_servicesdir}/ksplashthememgr.desktop
############################################ kstartupconfig
%{kde4_bindir}/kdostartupconfig4
%{kde4_bindir}/kstartupconfig4
############################################ ksystraycmd
%{kde4_bindir}/ksystraycmd
############################################ kwrited
%{kde4_plugindir}/kded_kwrited.so
%{kde4_appsdir}/kwrited
%{kde4_servicesdir}/kded/kwrited.desktop
############################################ solid
%{kde4_bindir}/solid-action-desktop-gen
#%{kde4_bindir}/solid-bluetooth
#%{kde4_bindir}/solid-network
#%{kde4_bindir}/solid-powermanagement
#%{kde4_libdir}/libsolidcontrol.so.*
#%{kde4_libdir}/libsolidcontrolifaces.so.*
#%{kde4_plugindir}/kcm_solid.so
%{kde4_plugindir}/kcm_solid_actions.so
#%{kde4_plugindir}/kded_networkstatus.so
#%{kde4_plugindir}/solid_*.so
%{kde4_appsdir}/solid*
%{kde4_appsdir}/kcmsolidactions/solid-action-template.desktop
#%{kde4_iconsdir}/oxygen/*/apps/networkmanager.*
#%{kde4_servicesdir}/kcm_solid.desktop
%{kde4_servicesdir}/solid-actions.desktop
#%{kde4_servicesdir}/solidbackends/solid_*.desktop
#%{kde4_servicesdir}/kded/networkstatus.desktop
#%{kde4_servicetypesdir}/solid*manager.desktop
%{kde4_servicetypesdir}/solid-device-type.desktop
%doc %lang(en) %{kde4_htmldir}/en/kcontrol/solid-actions
%doc %lang(en) %{kde4_htmldir}/en/kcontrol/solid-hardware
############################################ klipper
%{kde4_bindir}/klipper
%{kde4_libdir}/libkdeinit4_klipper.so
%{kde4_appsdir}/kconf_update/klipper-kconfigxt.upd
%{kde4_xdgappsdir}/klipper.desktop
%{kde4_datadir}/autostart/klipper.desktop
%doc %lang(en) %{kde4_htmldir}/en/klipper
############################################ kinfocenter
%{kde4_bindir}/kinfocenter
%{kde4_plugindir}/devinfo.so
%{kde4_plugindir}/kcm_info.so
%{kde4_plugindir}/kcm_infosummary.so
%{kde4_plugindir}/kcm_memory.so
%{kde4_plugindir}/kcm_nic.so
%{kde4_plugindir}/kcm_opengl.so
%{kde4_plugindir}/kcm_pci.so
%{kde4_plugindir}/kcm_samba.so
%{kde4_plugindir}/kcm_usb.so
%{kde4_plugindir}/kcm_view1394.so
%{kde4_appsdir}/kcmusb/*
%{kde4_appsdir}/kcmview1394/*
%{kde4_appsdir}/kinfocenter/*
%{kde4_xdgappsdir}/kinfocenter.desktop
%{kde4_servicesdir}/deviceinfocategory.desktop
%{kde4_servicesdir}/graphicalinfocategory.desktop
%{kde4_servicesdir}/lostfoundcategory.desktop
%{kde4_servicesdir}/networkinfocategory.desktop
%{kde4_servicetypesdir}/kinfocentercategory.desktop
%{kde4_servicesdir}/devinfo.desktop
%{kde4_servicesdir}/dma.desktop
%{kde4_servicesdir}/interrupts.desktop
%{kde4_servicesdir}/ioports.desktop
%{kde4_servicesdir}/kcm_infosummary.desktop
%{kde4_servicesdir}/kcm_memory.desktop
%{kde4_servicesdir}/kcm_pci.desktop
%{kde4_servicesdir}/kcmusb.desktop
%{kde4_servicesdir}/kcmview1394.desktop
%{kde4_servicesdir}/nic.desktop
%{kde4_servicesdir}/opengl.desktop
%{kde4_servicesdir}/scsi.desktop
%{kde4_servicesdir}/smbstatus.desktop
%{kde4_servicesdir}/xserver.desktop
%doc %lang(en) %{kde4_htmldir}/en/kinfocenter
############################################ policykit-kde
#%{kde4_bindir}/polkit-kde-authorization
#%{kde4_libdir}/libpolkitkdeprivate.so.*
#%{kde4_plugindir}/kcm_pkk_authorization.so
#%{kde4_plugindir}/libexec/polkit-kde-manager
#%{kde4_dbus_servicesdir}/*PolicyKit*.service
#%{kde4_servicesdir}/kcm_pkk_authorization.desktop
#%doc %lang(en) %{kde4_htmldir}/en/PolicyKit-kde
############################################ launching scripts
#%{kde4_bindir}/safestartkde
%{kde4_bindir}/startkde

%{kde4_bindir}/krandrstartup
%{kde4_bindir}/ksplashqml
%{kde4_bindir}/oxygen-shadow-demo
%{kde4_libdir}/kconf_update_bin/force_krunner_lock_shortcut_unreg
%{kde4_libdir}/kconf_update_bin/notifications-to-orgkdenotifications
%{kde4_plugindir}/kcm_cursortheme.so
%{kde4_plugindir}/kded_appmenu.so
%{kde4_plugindir}/kded_ktouchpadenabler.so
%{_kde4_libexecdir}/backlighthelper
%{_kde4_libexecdir}/kscreenlocker_greet
%{kde4_libdir}/libkwinglesutils.so.*
%{kde4_libdir}/libkwinglutils.so.*
%{kde4_libdir}/liboxygenstyleconfig.so.*
%{kde4_xdgappsdir}/kdesystemsettings.desktop
%{kde4_appsdir}/kcmkeyboard/pics/epo.png
%{kde4_appsdir}/kcmstyle/kcmstyle.notifyrc
%{kde4_appsdir}/kconf_update/krdb_libpathwipe.upd
%{kde4_appsdir}/kconf_update/kscreenlocker_locksession-shortcut.upd
%{kde4_appsdir}/kconf_update/notifications-to-orgkdenotifications.upd
%{kde4_configdir}/activities.knsrc
%{kde4_configdir}/kfontinst.knsrc
%{kde4_configdir}/kwineffect.knsrc
%{kde4_configdir}/kwinscripts.knsrc
%{kde4_configdir}/kwinswitcher.knsrc
%{kde4_configdir}/xcursor.knsrc
%{kde4_dbus_interfacesdir}/com.canonical.AppMenu.Registrar.xml
%{kde4_dbus_interfacesdir}/org.kde.kded.appmenu.xml
%{kde4_htmldir}/en/kcontrol/cursortheme/*
#%{kde4_iconsdir}/oxygen/22x22/apps/networkmanager.png
#%{kde4_iconsdir}/oxygen/32x32/apps/networkmanager.png
#%{kde4_iconsdir}/oxygen/64x64/apps/networkmanager.png
%{kde4_servicesdir}/cursortheme.desktop
%{kde4_servicesdir}/kded/appmenu.desktop
%{kde4_servicesdir}/kded/ktouchpadenabler.desktop
%{kde4_servicetypesdir}/kwindecoration.desktop
%{kde4_servicetypesdir}/kwinscript.desktop
%{kde4_servicetypesdir}/kwinwindowswitcher.desktop
%{kde4_servicetypesdir}/plasma_shareprovider.desktop
%{kde4_auth_policy_filesdir}/org.kde.fontinst.policy

#FIXME: undecided stuff ...
%{kde4_plugindir}/plugins/gui_platform/libkde.so
#%{kde4_appsdir}/kscreenlocker/kscreenlocker.notifyrc
%config %{kde4_configdir}/aurorae.knsrc
%{kde4_appsdir}/freespacenotifier/freespacenotifier.notifyrc
%{kde4_datadir}/config.kcfg/freespacenotifier.kcfg

%{kde4_appsdir}/kconf_update/oxygen.upd
%{kde4_appsdir}/kconf_update/update_oxygen.pl
%{kde4_servicetypesdir}/kwindesktopswitcher.desktop

%post -n ksysguard
touch --no-create %{_kde4_iconsdir}/oxygen &> /dev/null || :

%posttrans -n ksysguard
gtk-update-icon-cache %{_kde4_iconsdir}/oxygen &> /dev/null || :

%postun -n ksysguard
if [ $1 -eq 0 ] ; then
touch --no-create %{_kde4_iconsdir}/oxygen &> /dev/null || :
gtk-update-icon-cache %{_kde4_iconsdir}/oxygen &> /dev/null || :
fi

%files -n ksysguard
#doc %{name}-%{version}/ksysguard/README
%{_kde4_bindir}/ksysguard
%{_kde4_libdir}/libkdeinit4_ksysguard.so
%{_kde4_appsdir}/ksysguard/
%{_kde4_configdir}/ksysguard.knsrc
%{_kde4_datadir}/applications/kde4/ksysguard.desktop
%{_kde4_docdir}/HTML/en/ksysguard/
%{_kde4_iconsdir}/oxygen/*/apps/computer.*
%{_kde4_iconsdir}/oxygen/*/apps/daemon.*
%{_kde4_iconsdir}/oxygen/*/apps/kdeapp.*
%{_kde4_iconsdir}/oxygen/*/apps/kernel.*
%{_kde4_iconsdir}/oxygen/*/apps/ksysguardd.*
%{_kde4_iconsdir}/oxygen/*/apps/running.*
%{_kde4_iconsdir}/oxygen/*/apps/shell.*
%{_kde4_iconsdir}/oxygen/*/apps/unknownapp.*
%{_kde4_iconsdir}/oxygen/*/apps/waiting.*
%{_kde4_libexecdir}/ksysguardprocesslist_helper
%{_polkit_qt_policydir}/org.kde.ksysguard.processlisthelper.policy
%{_sysconfdir}/dbus-1/system.d/org.kde.ksysguard.processlisthelper.conf
%{_datadir}/dbus-1/system-services/org.kde.ksysguard.processlisthelper.service

%post -n ksysguard-libs -p /sbin/ldconfig
%postun -n ksysguard-libs -p /sbin/ldconfig

%files -n ksysguard-libs
%{_kde4_libdir}/kde4/plugins/designer/ksignalplotterwidgets.so
%{_kde4_libdir}/libksignalplotter.so.4*
%{_kde4_libdir}/kde4/plugins/designer/ksysguardwidgets.so
%{_kde4_libdir}/kde4/plugins/designer/ksysguardlsofwidgets.so
%{_kde4_libdir}/libksgrd.so.4*
%{_kde4_libdir}/liblsofui.so.4*
%{_kde4_libdir}/libprocesscore.so.4*
%{_kde4_libdir}/libprocessui.so.4*

%files -n ksysguardd
%config(noreplace) %{_kde4_sysconfdir}/ksysguarddrc
%{_kde4_bindir}/ksysguardd

#重打包时要重新处理

%changelog
* Wed Apr 23 2014 Liu Di <liudidi@gmail.com> - 4.13.0-1.1
- 为 Magic 3.0 重建

* Sat Dec 5 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.3.4-1mgc
- 更新至 4.3.4
- 修改 kickoff 徽标(patch 108)
- 乙丑  十月十九

* Tue Aug 18 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.3.0-4mgc
- 任务栏面板非桌面混成模式半透明支持(patch 106 imported from reviewboard)
- 己丑  六月廿八

* Wed Aug 5 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.3.0-2mgc
- 更新至 4.3.0(KDE 4.3 final)
- 己丑  六月十五

* Fri Jul 31 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.3.0-1mgc
- 更新至 4.3.0(KDE 4.3 try2)
- 系统设置管理员模式(patch 11 imported from fedora project)
- 任务栏图标模式(类似于 Window 7 的那种)
- n 多补丁...不详说了，太累了，想看自己看吧...
- 己丑  六月初十

* Mon Jun 29 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.95-1mgc
- 更新至 4.2.95(KDE 4.3 RC1)
- 去除附加墙纸
- 去除 kwin 装饰性 logo(patch 103)
- 己丑  闰五月初七

* Sat Jun 13 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.91-2mgc
- 修正文件分包问题
- kwin 装饰性 logo
- 己丑  五月廿一

* Thu Jun 11 2009 Liu Di <liudidi@gmail.com> - 4.2.90-1
- 更新到 4.2.90
- 已丑　五月十九

* Fri May 29 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.88-1mgc
- 更新至 4.2.88
- 己丑  五月初六

* Sat May 16 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.85-1mgc
- 更新至 4.2.85(KDE 4.3 Beta1)
- 禁用 patch 101( fixed by upstream  ^^ )
- 己丑  四月廿二

* Sat Apr 4 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.2-1mgc
- 更新至 4.2.2
- 纳入 ConsoleKit 支持
- 己丑  三月初九  [清明]

* Fri Mar 13 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.1-0.1mgc
- 更新至 4.2.1
- 重写 %file 部分
- 己丑  二月十二

* Thu Jan 22 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.0-0.1mgc
- 更新至 4.2.0(KDE 4.2 try1)
- 系统监视器工作表标题编码修正(patch 101 written by nihui)
- kdm 主题设置路径(patch 102 written by nihui)
- oxygen 墙纸补遗  :-D
- 戊子  十二月廿七

* Tue Jan 13 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.1.96-0.1mgc
- 更新至 4.1.96(KDE 4.2 RC1)
- relwithdeb 编译模式
- 清理 spec 文件
- 弱化 kdebase-workspace 对 kdebindings 的编译依赖(patch 302 from debian project)
- 戊子  十二月十八

* Sat Dec 20 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.1.85-0.2mgc
- 更新上游源码包
- 修正 %{kde4_libdir}/libplasma_applet-system-monitor.so 分包错误
- 纳入 plasma google gadgets 部件支持
- 纳入 plasma qedje 部件支持
- 戊子  十一月廿三

* Fri Dec 12 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.1.85-0.1mgc
- 更新至 4.1.85(KDE 4.2 Beta2)
- 戊子  十一月十五

* Sun Nov 23 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.1.80-0.1mgc
- 更新至 4.1.80
- 纳入 pyKDE4 支持
- 戊子  十月廿六

* Sun Oct 12 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.1.69-0.1mgc
- 更新至 4.1.69
- debugfull 编译模式
- 戊子  九月十四

* Mon Sep 29 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.1.2-0.1mgc
- 更新至 4.1.2
- 拆出 墙纸 和 oxygen 鼠标指针 主题包
- cmake 参数：-DKDE4_KDM_PAM_SERVICE=kdm -DKDE4_KCHECKPASS_PAM_SERVICE=kcheckpass -DKDE4_KSCREENSAVER_PAM_SERVICE=kscreensaver
- 戊子  九月初一

* Fri Sep 19 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.1.1-0.2mgc
- 更新 4.1 branch 代码
- kdm 休眠/待机 菜单支持
- kdm 文字空格优化
- Dialog notifying about running low on disk space
- 注销对话框自动倒计时
- tablet pc 屏幕翻转支持
- 热插拔设备根据类型弹出动作对话框
- 活动窗口背景装饰颜色更换
- 优化 系统设置 用户界面
- kwin 桌面立方体特效
- 戊子  八月二十

* Fri Aug 29 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.1.1-0.1mgc
- 更新至 4.1.1-try1(内部版本)
- 引入 kwin 任务栏缩略图特效特性(patch 100/102 from fedora project, backported from 4.2)
- 戊子  七月廿九

* Sat Aug 02 2008 Liu Di <liudidi@gmail.com> - 4.1.0-0.2mgc
- 随上游更新,修正注销的bug

* Thu Jul 24 2008 Liu Di <liudidi@gmail.com> - 4.1.0-0.1mgc
- 更新到 4.1.0(KDE 4.1 正式版)

* Thu Jul 10 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.98-0.1mgc
- 更新至 4.0.98(KDE 4.1 RC1)
- release 模式编译(build_type release)
- 戊子  六月初八

* Sat Jul 5 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.85-0.1mgc
- 更新至 4.0.85
- 去除 patch 5(fixed by upstream)  yay!!
- 新增 oxygen 鼠标指针主题
- 戊子  六月初三

* Fri Jun 27 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.84-0.1mgc
- 更新至 4.0.84
- 戊子  五月廿四

* Thu Jun 19 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.83-0.1mgc
- 更新至 4.0.83-try1(第一次 tag 4.1.0-beta2 内部版本)
- 禁用 patch 0(此特性已整合入 cmake 编译参数当中)
- 添加原 kde4-session 中 startkde 脚本内容(patch 1 written by nihui)
- 更新 patch 50
- 戊子  五月十六

* Wed Jun 11 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.82-0.1mgc
- 更新至 4.0.82
- 更新 dotkde4 补丁
- 戊子  五月初八

* Wed Jun 4 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.81-0.1mgc
- 更新至 4.0.81
- 允许进入系统设置的“管理员模式”(patch 6 from kde-core-devel)
- 修正 klipper url 用 firefox 打开的问题(patch 10 from fedora project)
- 添加 kickoff 休眠特性(patch 204 from opensuse project)
- 戊子  五月初一

* Fri May 23 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.80-0.1mgc
- 更新至 4.0.80(try1 内部版本)
- 更新 patch 50 编译补丁
- 戊子  四月十九

* Fri May 16 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.74-0.1mgc
- 更新至 4.0.74
- 戊子  四月十二

* Sat May 10 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.73-0.1mgc
- 更新至 4.0.73
- 戊子  四月初六

* Sun May 4 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.72-0.1mgc
- 更新至 4.0.72
- %{kde4_libdir}/kde4/plugins/designer/ksysguardwidgets.so 移入 devel 包
- 戊子  三月廿九

* Wed Apr 30 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.71-0.2mgc
- 更新至 4.0.71 正式发布版本
- 上游重新 tag 以修复 plasma 面板在多窗口下崩溃问题和 kdepim 编译问题
- 戊子  三月廿五

* Sat Apr 26 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.71-0.1mgc
- 更新至 4.0.71
- 戊子  三月廿一

* Sat Apr 19 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.70-0.1mgc
- 更新至 4.0.70
- 戊子  三月十四

* Sat Apr 12 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.69-0.1mgc
- 更新至 4.0.69
- 纳入 NetworkManager 支持
- 戊子  三月初七

* Mon Mar 31 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.3-0.1mgc
- 更新至 4.0.3
- 定义 kde4 路径
- 添加 xsession 菜单支持
- 暂时去除 patch 4 (需要 rediffer)
- 戊子  二月廿四

* Tue Mar 11 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.2-0.2mgc
- 更新 brunch 代码
- 修正 kdm 手册分包错误
- 修正 plasma-iconloader 补丁路径
- 关闭 verbose 编译模式(cmake_verbose_build = 0)
- 戊子  二月初四

* Sun Mar 2 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.2-0.1mgc
- 更新至 4.0.2
- 默认虚拟桌面个数恢复为 4 个
- 去除 回收站、显示桌面 plasmoid
- unused patch：添加 kdm console 工具特性(patch 61 from opensuse/fedora project)
- kdm 特性更改
- 面板大小更改补丁更新
- 戊子  正月廿五

* Thu Feb 7 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.1-0.2mgc
- 修正面板快捷方式特性
- 添加两处中文化菜单项
- 更新 brunch 代码补丁 (svn 771962)

* Wed Feb 6 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.1-0.1mgc
- 更新至 4.0.1
- plasma (4.x) 特性补丁

* Mon Jan 28 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.0-0.3mgc
- 更新 brunch 代码补丁 (svn 767569)

* Fri Jan 18 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.0-0.2mgc
- 更新 brunch 代码补丁

* Sat Jan 12 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.0-0.1mgc
- 更新至 4.0.0
- 纳入 libcaptury 支持
- 分离 kde3 会话菜单以及 startkde 脚本

* Fri Dec 14 2007 Ni Hui <shuizhuyuanluo@126.com> - 3.97.0-0.1mgc
- 更新至 3.97.0 (KDE4-RC2)
- 简化 spec 文件之 %file 字段
- 添加 startkde 脚本配置和 kdm-kde3 菜单项
- 未纳入 libcaptury 支持

* Sat Nov 24 2007 Ni Hui <shuizhuyuanluo@126.com> - 3.96.0-0.1mgc
- 更新至 3.96.0 (KDE4-RC1)

* Sat Oct 20 2007 Ni Hui <shuizhuyuanluo@126.com> - 3.94.0-0.1mgc
- 首次生成 rpm 包
