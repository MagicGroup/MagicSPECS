%define real_name kdeartwork

%define kde4_wallpapersdir %{kde4_datadir}/wallpapers
%define kde4_emoticonsdir %{kde4_datadir}/emoticons
%define kde4_soundsdir %{kde4_datadir}/sounds

Name: kdeartwork4
Summary: Artworks for KDE4
Summary(zh_CN.UTF-8): KDE 4 的美化包
License: LGPL v2 or later
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
URL: http://www.kde.org/
Version: 4.13.1
Release: 1%{?dist}
Source0: http://download.kde.org/stable/%{version}/src/%{real_name}-%{version}.tar.xz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: libkdelibs4-devel
BuildRequires: kdebase4-workspace-devel
BuildRequires: kde4-libkexiv2-devel
BuildRequires: xscreensaver

Requires: %{name}-wallpapers
Requires: %{name}-ColorSchemes
Requires: %{name}-IconThemes
Requires: %{name}-desktopthemes
Requires: %{name}-emoticons
Requires: %{name}-kscreensaver
Requires: %{name}-styles

%description
Artworks for KDE4

%description -l zh_CN.UTF-8
KDE 4 的美化包。


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
%package wallpapers
Summary: KDE Wallpapers
Summary(zh_CN.UTF-8): KDE 墙纸
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面

%description wallpapers
%{summary}.

%description wallpapers -l zh_CN.UTF-8
KDE 墙纸。

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
%package IconThemes
Summary: KDE Icon Themes
Summary(zh_CN.UTF-8): KDE 图标主题
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面

%description IconThemes
%{summary}.

%description IconThemes -l zh_CN.UTF-8
KDE 图标主题。

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
%package ColorSchemes
Summary: KDE Color Schemes
Summary(zh_CN.UTF-8): KDE 配色方案
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面

%description ColorSchemes
%{summary}.

%description ColorSchemes -l zh_CN.UTF-8
KDE 配色方案。

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
%package desktopthemes
Summary: KDE Desktop Themes
Summary(zh_CN.UTF-8): KDE 桌面主题
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面

%description desktopthemes
%{summary}.

%description desktopthemes -l zh_CN.UTF-8
KDE 桌面主题。

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
%package emoticons
Summary: KDE Emotion Icons
Summary(zh_CN.UTF-8): KDE 表情图标集
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面

%description emoticons
%{summary}.

%description emoticons -l zh_CN.UTF-8
KDE 表情图标集。

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
%package kscreensaver
Summary: KDE Screensaver
Summary(zh_CN.UTF-8): KDE 屏幕保护
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面

%description kscreensaver
%{summary}.

%description kscreensaver -l zh_CN.UTF-8
KDE 屏幕保护。

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
%package styles
Summary: KDE Control Styles
Summary(zh_CN.UTF-8): KDE 控件风格
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面

%description styles
%{summary}.

%description styles -l zh_CN.UTF-8
KDE 控件风格。

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
%prep
%setup -q -n %{real_name}-%{version}

%build
mkdir build
cd build
# export pkgconfig path for detecting library properly
export PKG_CONFIG_PATH="$PKG_CONFIG_PATH:%{kde4_libdir}/pkgconfig" ;
%cmake_kde4 ..

make %{?_smp_mflags}

%install
cd build
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

%clean_kde4_desktop_files
magic_rpm_clean.sh

%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files
%defattr(-,root,root)

%files wallpapers
%defattr(-,root,root)
%{kde4_wallpapersdir}/*

%files ColorSchemes
%defattr(-,root,root)
%{kde4_appsdir}/color-schemes/*

%files IconThemes
%defattr(-,root,root)
%{kde4_iconsdir}/*

%files desktopthemes
%defattr(-,root,root)
%{kde4_appsdir}/desktoptheme/*

%files emoticons
%defattr(-,root,root)
%{kde4_emoticonsdir}/*

%files kscreensaver
%defattr(-,root,root)
%{kde4_bindir}/*.kss
%{kde4_bindir}/kxsconfig
%{kde4_bindir}/kxsrun
%{kde4_appsdir}/kfiresaver/*
%{kde4_appsdir}/kscreensaver/*
%{kde4_servicesdir}/ScreenSavers/*

%if 0
%files sounds
%defattr(-,root,root)
%{kde4_soundsdir}/*
%endif

%files styles
%defattr(-,root,root)
%{kde4_plugindir}/kstyle_phase_config.so
%{kde4_plugindir}/plugins/styles/phasestyle.so
%{kde4_plugindir}/kwin3_*.so
%{kde4_plugindir}/kwin_*.so
%{kde4_appsdir}/kwin/*
%{kde4_appsdir}/kstyle/*
# FIXME: sub pkg for aurorae themes ?  --- nihui
#%{kde4_appsdir}/aurorae/*

%changelog
* Thu Jun 05 2014 Liu Di <liudidi@gmail.com> - 4.13.1-1
- 更新到 4.13.1

* Thu Apr 24 2014 Liu Di <liudidi@gmail.com> - 4.13.0-1.1
- 为 Magic 3.0 重建

* Wed Aug 5 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.3.0-1mgc
- 更新至 4.3.0
- 己丑  六月十五

* Tue Jun 30 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.95-1mgc
- 更新至 4.2.95(KDE 4.3 RC1)
- 己丑  闰五月初八

* Sat Apr 4 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.2-1mgc
- 更新至 4.2.2
- 己丑  三月初九  [清明]

* Sun Mar 8 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.1-0.1mgc
- 更新至 4.2.1
- 己丑  二月十二

* Sun Jan 25 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.0-0.1mgc
- 更新至 4.2.0
- 戊子  十二月三十

* Thu Jan 15 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.1.96-0.1mgc
- 更新至 4.1.96(KDE 4.2 RC1)
- relwithdeb 编译模式
- 戊子  十二月二十

* Fri Jul 25 2008 Liu Di <liudidi@gmail.com> - 4.1.0-0.1mgc
- 更新到 4.1.0
- 首次生成 rpm 包
