%define real_name kdeplasma-addons

# whether to build lancelot applet
%define build_lancelot 1

%define KEXIV2_INCLUDE_DIR %{kde4_includedir}/libkexiv2
%define KEXIV2_LIBRARIES %{kde4_libdir}/libkexiv2.so

Name: kdeplasma-addons
Summary: The KDE plasmoids Components
License: LGPL v2 or later
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
URL: http://www.kde.org/
Version: 4.14.3
Release: 2%{?dist}
Source0: http://download.kde.org/stable/%{version}/src/%{real_name}-%{version}.tar.xz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: libkdelibs4-devel >= 4.2.69
BuildRequires: kdebase4-workspace-devel >= 4.2.69
BuildRequires: gettext
%if %build_lancelot
BuildRequires: python >= 2.5
%endif
# 相框自动根据 exif 元数据旋转支持
BuildRequires: kde4-libkexiv2-devel >= %{version}
BuildRequires: eigen2 >= 2.0.3
BuildConflicts: eigen2-devel < 2.0.3
# marble 世界地图桌面背景
BuildRequires: libkdeedu4-devel
BuildRequires: attica-devel
BuildRequires: qjson-devel
BuildRequires: qoauth-devel
BuildRequires: kde4-marble-devel >= %{version}

Requires: kdebase4-workspace

# dict plasmoid dict.cn 支持
Patch1: kdeplasma-addons-4.3.4-applet_dict_dictcn.patch

Patch60: kdeplasma-addons-4.4.2-kimpanel-disable_mouse_select_candidates.patch
Patch61: kdeplasma-addons-4.4.2-kimpanel-screenpos.patch
Patch62: kdeplasma-addons-4.4.2-kimpanel-uglyfix.patch


Patch1000: kdeplasma-addons-no_lancelot.diff


Requires: kdeplasma-addons-krunner-plugins
Requires: kdeplasma-addons-krunner-plugins-konquerorsessions
Requires: kdeplasma-addons-wallpaper-plugins
Requires: kdeplasma-addons-wallpaper-plugins-marble
Requires: kdeplasma-addons-desktoptheme
Requires: kdeplasma-addons-libplasmaweather
Requires: kde-plasma-lancelot
Requires: kde-plasma-bball
Requires: kde-plasma-binaryclock
Requires: kde-plasma-bubblemon
Requires: kde-plasma-calculator
Requires: kde-plasma-charselect
Requires: kde-plasma-comic
Requires: kde-plasma-dict
Requires: kde-plasma-eyes
Requires: kde-plasma-fifteenPuzzle
Requires: kde-plasma-fileWatcher
Requires: kde-plasma-frame
Requires: kde-plasma-fuzzy_clock
Requires: kde-plasma-incomingmsg
Requires: kde-plasma-kolourpicker
Requires: kde-plasma-konqprofiles
Requires: kde-plasma-konsoleprofiles
Requires: kde-plasma-leavenote
Requires: kde-plasma-life
Requires: kde-plasma-luna
Requires: kde-plasma-magnifique
Requires: kde-plasma-mediaplayer
Requires: kde-plasma-microblog
Requires: kde-plasma-news
Requires: kde-plasma-notes
Requires: kde-plasma-nowplaying
Requires: kde-plasma-opendesktop
Requires: kde-plasma-paste
Requires: kde-plasma-pastebin
Requires: kde-plasma-previewer
Requires: kde-plasma-rssnow
Requires: kde-plasma-rtm
Requires: kde-plasma-showdashboard
Requires: kde-plasma-showdesktop
Requires: kde-plasma-systemloadviewer
Requires: kde-plasma-timer
Requires: kde-plasma-unitconverter
Requires: kde-plasma-weather
Requires: kde-plasma-weatherstation

Requires: kde-plasma-blackboard
Requires: kde-plasma-kdeobservatory
Requires: kde-plasma-kimpanel
Requires: kde-plasma-knowledgebase
Requires: kde-plasma-opendesktop_activities
Requires: kde-plasma-plasmaboard
Requires: kde-plasma-qalculate
Requires: kde-plasma-spellcheck
Requires: kde-plasma-webslice
Requires: kde-plasma-bookmarks

%description
The KDE plasmoids Components.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- 开发包
%package -n %{name}-devel
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Summary: KDE plasmoids Libraries: Build Environment
Requires: libkdelibs4-devel
Requires: %{name} = %{version}

%description -n %{name}-devel
This package contains all necessary include files and libraries needed
to develop KDE plasmoids applications.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

%package krunner-plugins
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Summary: krunner-plugins
Requires: libkdelibs4

%description krunner-plugins
krunner-plugins.


%package krunner-plugins-konquerorsessions
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Summary: krunner-plugins-konquerorsessions
Requires: libkdelibs4

%description krunner-plugins-konquerorsessions
krunner-plugins-konquerorsessions.


%package wallpaper-plugins
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Summary: wallpaper-plugins
Requires: libkdelibs4
Requires: kdeplasma-addons-libplasmaweather

%description wallpaper-plugins
wallpaper-plugins.


%package wallpaper-plugins-marble
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Summary: wallpaper-plugins-marble
Requires: libkdelibs4

%description wallpaper-plugins-marble
wallpaper-plugins-marble.


%package desktoptheme
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Summary: desktoptheme
Requires: libkdelibs4

%description desktoptheme
desktoptheme.


%package libplasmaweather
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Summary: libplasmaweather
Requires: libkdelibs4

%description libplasmaweather
libplasmaweather.


%package -n kde-plasma-lancelot
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Summary: kde-plasma-lancelot
Requires: libkdelibs4

%description -n kde-plasma-lancelot
kde-plasma-lancelot.


%package -n kde-plasma-bball
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Summary: kde-plasma-bball
Requires: libkdelibs4

%description -n kde-plasma-bball
kde-plasma-bball.


%package -n kde-plasma-binaryclock
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Summary: kde-plasma-binaryclock
Requires: libkdelibs4

%description -n kde-plasma-binaryclock
kde-plasma-binaryclock.


%package -n kde-plasma-bubblemon
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Summary: kde-plasma-bubblemon
Requires: libkdelibs4

%description -n kde-plasma-bubblemon
kde-plasma-bubblemon.


%package -n kde-plasma-calculator
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Summary: kde-plasma-calculator
Requires: libkdelibs4

%description -n kde-plasma-calculator
kde-plasma-calculator.


%package -n kde-plasma-charselect
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Summary: kde-plasma-charselect
Requires: libkdelibs4

%description -n kde-plasma-charselect
kde-plasma-charselect.


%package -n kde-plasma-comic
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Summary: kde-plasma-comic
Requires: libkdelibs4

%description -n kde-plasma-comic
kde-plasma-comic.


%package -n kde-plasma-dict
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Summary: kde-plasma-dict
Requires: libkdelibs4

%description -n kde-plasma-dict
kde-plasma-dict.


%package -n kde-plasma-eyes
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Summary: kde-plasma-eyes
Requires: libkdelibs4

%description -n kde-plasma-eyes
kde-plasma-eyes.


%package -n kde-plasma-fifteenPuzzle
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Summary: kde-plasma-fifteenPuzzle
Requires: libkdelibs4

%description -n kde-plasma-fifteenPuzzle
kde-plasma-fifteenPuzzle.


%package -n kde-plasma-fileWatcher
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Summary: kde-plasma-fileWatcher
Requires: libkdelibs4

%description -n kde-plasma-fileWatcher
kde-plasma-fileWatcher.


%package -n kde-plasma-frame
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Summary: kde-plasma-frame
Requires: libkdelibs4

%description -n kde-plasma-frame
kde-plasma-frame.


%package -n kde-plasma-fuzzy_clock
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Summary: kde-plasma-fuzzy_clock
Requires: libkdelibs4

%description -n kde-plasma-fuzzy_clock
kde-plasma-fuzzy_clock.


%package -n kde-plasma-incomingmsg
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Summary: kde-plasma-incomingmsg
Requires: libkdelibs4

%description -n kde-plasma-incomingmsg
kde-plasma-incomingmsg.


%package -n kde-plasma-kolourpicker
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Summary: kde-plasma-kolourpicker
Requires: libkdelibs4

%description -n kde-plasma-kolourpicker
kde-plasma-kolourpicker.


%package -n kde-plasma-konqprofiles
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Summary: kde-plasma-konqprofiles
Requires: libkdelibs4

%description -n kde-plasma-konqprofiles
kde-plasma-konqprofiles.


%package -n kde-plasma-konsoleprofiles
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Summary: kde-plasma-konsoleprofiles
Requires: libkdelibs4

%description -n kde-plasma-konsoleprofiles
kde-plasma-konsoleprofiles.


%package -n kde-plasma-leavenote
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Summary: kde-plasma-leavenote
Requires: libkdelibs4

%description -n kde-plasma-leavenote
kde-plasma-leavenote.


%package -n kde-plasma-life
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Summary: kde-plasma-life
Requires: libkdelibs4

%description -n kde-plasma-life
kde-plasma-life.


%package -n kde-plasma-luna
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Summary: kde-plasma-luna
Requires: libkdelibs4

%description -n kde-plasma-luna
kde-plasma-luna.


%package -n kde-plasma-magnifique
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Summary: kde-plasma-magnifique
Requires: libkdelibs4

%description -n kde-plasma-magnifique
kde-plasma-magnifique.


%package -n kde-plasma-mediaplayer
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Summary: kde-plasma-mediaplayer
Requires: libkdelibs4

%description -n kde-plasma-mediaplayer
kde-plasma-mediaplayer.


%package -n kde-plasma-microblog
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Summary: kde-plasma-microblog
Requires: libkdelibs4

%description -n kde-plasma-microblog
kde-plasma-microblog.


%package -n kde-plasma-news
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Summary: kde-plasma-news
Requires: libkdelibs4

%description -n kde-plasma-news
kde-plasma-news.


%package -n kde-plasma-notes
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Summary: kde-plasma-notes
Requires: libkdelibs4

%description -n kde-plasma-notes
kde-plasma-notes.


%package -n kde-plasma-nowplaying
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Summary: kde-plasma-nowplaying
Requires: libkdelibs4

%description -n kde-plasma-nowplaying
kde-plasma-nowplaying.


%package -n kde-plasma-opendesktop
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Summary: kde-plasma-opendesktop
Requires: libkdelibs4

%description -n kde-plasma-opendesktop
kde-plasma-opendesktop.


%package -n kde-plasma-paste
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Summary: kde-plasma-paste
Requires: libkdelibs4

%description -n kde-plasma-paste
kde-plasma-paste.


%package -n kde-plasma-pastebin
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Summary: kde-plasma-pastebin
Requires: libkdelibs4

%description -n kde-plasma-pastebin
kde-plasma-pastebin.


%package -n kde-plasma-previewer
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Summary: kde-plasma-previewer
Requires: libkdelibs4

%description -n kde-plasma-previewer
kde-plasma-previewer.


%package -n kde-plasma-rssnow
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Summary: kde-plasma-rssnow
Requires: libkdelibs4

%description -n kde-plasma-rssnow
kde-plasma-rssnow.


%package -n kde-plasma-rtm
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Summary: kde-plasma-rtm
Requires: libkdelibs4

%description -n kde-plasma-rtm
kde-plasma-rtm.


%package -n kde-plasma-showdashboard
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Summary: kde-plasma-showdashboard
Requires: libkdelibs4

%description -n kde-plasma-showdashboard
kde-plasma-showdashboard.


%package -n kde-plasma-showdesktop
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Summary: kde-plasma-showdesktop
Requires: libkdelibs4

%description -n kde-plasma-showdesktop
kde-plasma-showdesktop.


%package -n kde-plasma-systemloadviewer
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Summary: kde-plasma-systemloadviewer
Requires: libkdelibs4

%description -n kde-plasma-systemloadviewer
kde-plasma-systemloadviewer.


%package -n kde-plasma-timer
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Summary: kde-plasma-timer
Requires: libkdelibs4

%description -n kde-plasma-timer
kde-plasma-timer.


%package -n kde-plasma-unitconverter
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Summary: kde-plasma-unitconverter
Requires: libkdelibs4

%description -n kde-plasma-unitconverter
kde-plasma-unitconverter.


%package -n kde-plasma-weather
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Summary: kde-plasma-weather
Requires: libkdelibs4
Requires: kdeplasma-addons-libplasmaweather

%description -n kde-plasma-weather
kde-plasma-weather.


%package -n kde-plasma-weatherstation
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Summary: kde-plasma-weatherstation
Requires: libkdelibs4
Requires: kdeplasma-addons-libplasmaweather

%description -n kde-plasma-weatherstation
kde-plasma-weatherstation.


%package -n kde-plasma-blackboard
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Summary: kde-plasma-blackboard
Requires: libkdelibs4

%description -n kde-plasma-blackboard
kde-plasma-blackboard.


%package -n kde-plasma-kdeobservatory
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Summary: kde-plasma-kdeobservatory
Requires: libkdelibs4

%description -n kde-plasma-kdeobservatory
kde-plasma-kdeobservatory.


%package -n kde-plasma-kimpanel
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Summary: kde-plasma-kimpanel
Requires: libkdelibs4

%description -n kde-plasma-kimpanel
kde-plasma-kimpanel.


%package -n kde-plasma-knowledgebase
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Summary: kde-plasma-knowledgebase
Requires: libkdelibs4

%description -n kde-plasma-knowledgebase
kde-plasma-knowledgebase.


%package -n kde-plasma-opendesktop_activities
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Summary: kde-plasma-opendesktop_activities
Requires: libkdelibs4

%description -n kde-plasma-opendesktop_activities
kde-plasma-opendesktop_activities.


%package -n kde-plasma-plasmaboard
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Summary: kde-plasma-plasmaboard
Requires: libkdelibs4

%description -n kde-plasma-plasmaboard
kde-plasma-plasmaboard.


%package -n kde-plasma-qalculate
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Summary: kde-plasma-qalculate
Requires: libkdelibs4

%description -n kde-plasma-qalculate
kde-plasma-qalculate.


%package -n kde-plasma-spellcheck
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Summary: kde-plasma-spellcheck
Requires: libkdelibs4

%description -n kde-plasma-spellcheck
kde-plasma-spellcheck.


%package -n kde-plasma-webslice
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Summary: kde-plasma-webslice
Requires: libkdelibs4

%description -n kde-plasma-webslice
kde-plasma-webslice.



%package -n kde-plasma-bookmarks
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Summary: kde-plasma-bookmarks
Requires: libkdelibs4

%description -n kde-plasma-bookmarks
kde-plasma-bookmarks.


%prep
%setup -q -n %{real_name}-%{version}

#pushd applets/dict
#%patch1 -p1
#popd

#%patch60 -p1
#%patch61 -p1
#%patch62 -p1


%if !%build_lancelot
%patch1000 -p0 -b .no_lancelot
%endif

%build
mkdir build
cd build
%cmake_kde4 \
    -DKEXIV2_INCLUDE_DIR=%{KEXIV2_INCLUDE_DIR} \
    -DKEXIV2_LIBRARIES=%{KEXIV2_LIBRARIES} \
    ..

make %{?_smp_mflags}

%install
cd build
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

%clean_kde4_desktop_files
%clean_kde4_notifyrc_files
%adapt_kde4_notifyrc_files
magic_rpm_clean.sh

%post libplasmaweather -p /sbin/ldconfig
%postun libplasmaweather -p /sbin/ldconfig

%post -n kde-plasma-lancelot -p /sbin/ldconfig
%postun -n kde-plasma-lancelot -p /sbin/ldconfig

%post -n kde-plasma-comic -p /sbin/ldconfig
%postun -n kde-plasma-comic -p /sbin/ldconfig

%post -n kde-plasma-frame -p /sbin/ldconfig
%postun -n kde-plasma-frame -p /sbin/ldconfig

%post -n kde-plasma-rtm -p /sbin/ldconfig
%postun -n kde-plasma-rtm -p /sbin/ldconfig

%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files -n %{name}-devel
%defattr(-,root,root)
%{kde4_libdir}/*.so
%if %build_lancelot
%{kde4_includedir}/lancelot
%{kde4_includedir}/lancelot-datamodels
%{kde4_includedir}/KDE/Lancelot
%{kde4_appsdir}/cmake/modules/FindLancelot-Datamodels.cmake
%{kde4_appsdir}/cmake/modules/FindLancelot.cmake
%endif

%files
%defattr(-,root,root)
%doc COPYING

%files krunner-plugins
%defattr(-,root,root)
%{kde4_plugindir}/kcm_krunner_charrunner.so
%{kde4_plugindir}/kcm_krunner_spellcheck.so
%{kde4_plugindir}/kcm_krunner_audioplayercontrol.so
%{kde4_plugindir}/krunner_audioplayercontrol.so
%{kde4_plugindir}/krunner_charrunner.so
%{kde4_plugindir}/krunner_kopete.so
%{kde4_plugindir}/krunner_mediawiki.so
%{kde4_plugindir}/krunner_browserhistory.so
%{kde4_plugindir}/krunner_contacts.so
%{kde4_plugindir}/krunner_katesessions.so
%{kde4_plugindir}/krunner_konsolesessions.so
%{kde4_plugindir}/krunner_spellcheckrunner.so
%{kde4_plugindir}/plasma_runner_datetime.so
%{kde4_plugindir}/kcm_plasma_runner_events.so
%{kde4_plugindir}/plasma_containment_griddesktop.so
%{kde4_plugindir}/plasma_containment_groupingdesktop.so
%{kde4_plugindir}/plasma_containment_groupingpanel.so
%{kde4_plugindir}/plasma_runner_events.so
%{kde4_libdir}/libplasma_groupingcontainment.so.4*
%{kde4_servicesdir}/CharRunner_config.desktop
%{kde4_servicesdir}/CharacterRunner.desktop
%{kde4_servicesdir}/browserhistory.desktop
%{kde4_servicesdir}/katesessions.desktop
%{kde4_servicesdir}/konsolesessions.desktop
%{kde4_servicesdir}/plasma-runner-contacts.desktop
%{kde4_servicesdir}/plasma-runner-datetime.desktop
%{kde4_servicesdir}/plasma-runner-spellchecker.desktop
%{kde4_servicesdir}/plasma-runner-spellchecker_config.desktop
%{kde4_servicesdir}/plasma-runner-audioplayercontrol.desktop
%{kde4_servicesdir}/plasma-runner-audioplayercontrol_config.desktop
%{kde4_servicesdir}/plasma-runner-kopete.desktop
%{kde4_servicesdir}/plasma-runner-techbase.desktop
%{kde4_servicesdir}/plasma-runner-wikipedia.desktop
%{kde4_servicesdir}/plasma-runner-wikitravel.desktop
%{kde4_servicesdir}/plasma-runner-events.desktop
%{kde4_servicesdir}/plasma-runner-events_config.desktop
%{kde4_servicesdir}/plasma-containment-*.desktop

%{kde4_plugindir}/krunner_youtube.so
%{kde4_servicesdir}/plasma-runner-youtube.desktop

#需要调整分包
%{kde4_plugindir}/plasma_applet_icontasks.so
%{kde4_plugindir}/plasma_wallpaper_potd.so
%{kde4_appsdir}/kdeplasma-addons/mediabuttonsrc
%{kde4_iconsdir}/hicolor/*/actions/krunner_youtube.*
%{kde4_servicesdir}/plasma-applet-icontasks.desktop
%{kde4_servicesdir}/plasma-wallpaper-potd.desktop

%{kde4_plugindir}/kcm_krunner_dictionary.so
%{kde4_plugindir}/krunner_dictionary.so
%{kde4_plugindir}/plasma_wallpaper_qml.so
%{kde4_appsdir}/plasma/packages/*
%{kde4_appsdir}/plasma/plasmoids/calculator/*
%{kde4_appsdir}/plasma/wallpapers/*
%{kde4_servicesdir}/plasma-runner-dictionary.desktop
%{kde4_servicesdir}/plasma-runner-dictionary_config.desktop
%{kde4_servicesdir}/plasma-wallpaper-qml.desktop

%{kde4_plugindir}/krunner_translator.so
%{kde4_plugindir}/plasma_potd_natgeoprovider.so
%{kde4_servicesdir}/natgeoprovider.desktop
%{kde4_servicesdir}/plasma-runner-translator.desktop

%files krunner-plugins-konquerorsessions
%defattr(-,root,root)
%{kde4_plugindir}/krunner_konquerorsessions.so
%{kde4_servicesdir}/konquerorsessions.desktop

%files wallpaper-plugins
%defattr(-,root,root)
%{kde4_plugindir}/plasma_wallpaper_mandelbrot.so
%{kde4_plugindir}/plasma_wallpaper_pattern.so
%{kde4_plugindir}/plasma_wallpaper_virus.so
%{kde4_plugindir}/plasma_wallpaper_weather.so
%{kde4_appsdir}/plasma_wallpaper_pattern
%config %{kde4_configdir}/virus_wallpaper.knsrc
%{kde4_servicesdir}/plasma-wallpaper-mandelbrot.desktop
%{kde4_servicesdir}/plasma-wallpaper-pattern.desktop
%{kde4_servicesdir}/plasma-wallpaper-virus.desktop
%{kde4_servicesdir}/plasma-wallpaper-weather.desktop

%files wallpaper-plugins-marble
%defattr(-,root,root)
%{kde4_plugindir}/plasma_wallpaper_marble.so
%{kde4_servicesdir}/plasma-wallpaper-marble.desktop

%files desktoptheme
%defattr(-,root,root)
%{kde4_appsdir}/desktoptheme

%files libplasmaweather
%defattr(-,root,root)
%{kde4_libdir}/libplasmaweather.so.*
%config %{kde4_configdir}/plasmaweather.knsrc

%files -n kde-plasma-lancelot
%defattr(-,root,root)
%{kde4_bindir}/lancelot
%{kde4_plugindir}/plasma_applet_lancelot_launcher.so
%{kde4_plugindir}/plasma_applet_lancelot_part.so
%{kde4_libdir}/liblancelot.so.*
%{kde4_libdir}/liblancelot-datamodels.so.*
%{kde4_appsdir}/lancelot
#%{kde4_dbus_servicesdir}/org.kde.lancelot.service
%{kde4_iconsdir}/hicolor/*/apps/lancelot.*
%{kde4_iconsdir}/hicolor/*/apps/lancelot-start.*
%{kde4_iconsdir}/hicolor/*/apps/plasmaapplet-shelf.*
%{kde4_servicesdir}/plasma-applet-lancelot-launcher.desktop
%{kde4_servicesdir}/plasma-applet-lancelot-part.desktop
%{kde4_datadir}/mime/packages/lancelotpart-mime.xml
%{kde4_servicesdir}/lancelot.desktop

%files -n kde-plasma-bball
%defattr(-,root,root)
%{kde4_plugindir}/plasma_applet_bball.so
%{kde4_appsdir}/bball
%{kde4_iconsdir}/hicolor/*/apps/bball.*
%{kde4_servicesdir}/plasma-applet-bball.desktop

%files -n kde-plasma-binaryclock
%defattr(-,root,root)
%{kde4_plugindir}/plasma_applet_binaryclock.so
%{kde4_servicesdir}/plasma-applet-binaryclock.desktop

%files -n kde-plasma-bubblemon
%defattr(-,root,root)
%{kde4_plugindir}/plasma_applet_bubblemon.so
%{kde4_servicesdir}/plasma-applet-bubblemon.desktop

%files -n kde-plasma-calculator
%defattr(-,root,root)
%{kde4_servicesdir}/plasma-applet-calculator.desktop

%files -n kde-plasma-charselect
%defattr(-,root,root)
%{kde4_plugindir}/plasma_applet_charselect.so
%{kde4_servicesdir}/plasma-applet-charselect.desktop

%files -n kde-plasma-comic
%defattr(-,root,root)
%{kde4_plugindir}/plasma_applet_comic.so
%{kde4_plugindir}/plasma_comic_krossprovider.so
%{kde4_plugindir}/plasma_engine_comic.so
%{kde4_plugindir}/plasma_packagestructure_comic.so
%{kde4_libdir}/libplasmacomicprovidercore.so.*
%config %{kde4_configdir}/comic.knsrc
%{kde4_servicesdir}/plasma-comic-default.desktop
%{kde4_servicesdir}/plasma-dataengine-comic.desktop
%{kde4_servicesdir}/plasma-packagestructure-comic.desktop
%{kde4_servicetypesdir}/plasma_comicprovider.desktop

%files -n kde-plasma-dict
%defattr(-,root,root)
%{kde4_plugindir}/plasma_applet_dict.so
%{kde4_iconsdir}/hicolor/*/apps/accessories-dictionary.*
%{kde4_servicesdir}/plasma-dict-default.desktop

%files -n kde-plasma-eyes
%defattr(-,root,root)
%{kde4_plugindir}/plasma_applet_eyes.so
%{kde4_servicesdir}/plasma-applet-eyes.desktop
%{kde4_iconsdir}/hicolor/*/apps/eyes*

%files -n kde-plasma-fifteenPuzzle
%defattr(-,root,root)
%{kde4_plugindir}/plasma_applet_fifteenPuzzle.so
%{kde4_iconsdir}/hicolor/*/apps/fifteenpuzzle.*
%{kde4_servicesdir}/plasma-applet-fifteenPuzzle.desktop

%files -n kde-plasma-fileWatcher
%defattr(-,root,root)
%{kde4_plugindir}/plasma_applet_fileWatcher.so
%{kde4_servicesdir}/plasma-fileWatcher-default.desktop

%files -n kde-plasma-frame
%defattr(-,root,root)
%{kde4_plugindir}/plasma_applet_frame.so
%{kde4_plugindir}/plasma_engine_potd.so
%{kde4_plugindir}/plasma_potd_apodprovider.so
%{kde4_plugindir}/plasma_potd_epodprovider.so
%{kde4_plugindir}/plasma_potd_flickrprovider.so
%{kde4_plugindir}/plasma_potd_oseiprovider.so
%{kde4_plugindir}/plasma_potd_wcpotdprovider.so
%{kde4_libdir}/libplasmapotdprovidercore.so.*
%{kde4_appsdir}/plasma-applet-frame
%{kde4_servicesdir}/plasma-frame-default.desktop
%{kde4_servicesdir}/plasma-dataengine-potd.desktop
%{kde4_servicesdir}/apodprovider.desktop
%{kde4_servicesdir}/epodprovider.desktop
%{kde4_servicesdir}/flickrprovider.desktop
%{kde4_servicesdir}/oseiprovider.desktop
%{kde4_servicesdir}/wcpotdprovider.desktop
%{kde4_servicetypesdir}/plasma_potdprovider.desktop

%files -n kde-plasma-fuzzy_clock
%defattr(-,root,root)
%{kde4_plugindir}/plasma_applet_fuzzy_clock.so
%{kde4_servicesdir}/plasma-clock-fuzzy.desktop

%files -n kde-plasma-incomingmsg
%defattr(-,root,root)
%{kde4_plugindir}/plasma_applet_incomingmsg.so
%{kde4_servicesdir}/plasma-applet-incomingmsg.desktop

%files -n kde-plasma-kolourpicker
%defattr(-,root,root)
%{kde4_plugindir}/plasma_applet_kolourpicker.so
%{kde4_servicesdir}/plasma-kolourpicker-default.desktop

%files -n kde-plasma-konqprofiles
%defattr(-,root,root)
%{kde4_plugindir}/plasma_*_konqprofiles.so
%{kde4_servicesdir}/plasma-*-konqprofiles.desktop
%{kde4_appsdir}/plasma/plasmoids/konqprofiles/
%{kde4_appsdir}/plasma/services/org.kde.plasma.dataengine.konqprofiles.operations

%files -n kde-plasma-konsoleprofiles
%defattr(-,root,root)
%{kde4_plugindir}/plasma_*_konsoleprofiles.so
%{kde4_servicesdir}/plasma-*-konsoleprofiles.desktop
%{kde4_appsdir}/plasma/plasmoids/konsoleprofiles/
%{kde4_appsdir}/plasma/services/org.kde.plasma.dataengine.konsoleprofiles.operations

%files -n kde-plasma-leavenote
%defattr(-,root,root)
%{kde4_plugindir}/plasma_applet_leavenote.so
%{kde4_servicesdir}/plasma-applet-leavenote.desktop

%files -n kde-plasma-life
%defattr(-,root,root)
%{kde4_plugindir}/plasma_applet_life.so
%{kde4_servicesdir}/plasma-applet-life.desktop
%{kde4_iconsdir}/hicolor/*/apps/lifegame*

%files -n kde-plasma-luna
%defattr(-,root,root)
%{kde4_plugindir}/plasma_applet_luna.so
%{kde4_servicesdir}/plasma-applet-luna.desktop
%{kde4_iconsdir}/hicolor/*/apps/luna*

%files -n kde-plasma-magnifique
%defattr(-,root,root)
%{kde4_plugindir}/plasma_applet_magnifique.so
%{kde4_servicesdir}/plasma-applet-magnifique.desktop

%files -n kde-plasma-mediaplayer
%defattr(-,root,root)
%{kde4_plugindir}/plasma_applet_mediaplayer.so
%{kde4_servicesdir}/plasma-applet-mediaplayer.desktop

%files -n kde-plasma-microblog
%defattr(-,root,root)
%{kde4_plugindir}/plasma_applet_microblog.so
%{kde4_plugindir}/plasma_engine_microblog.so
%{kde4_appsdir}/plasma/services/tweet.operations
%{kde4_servicesdir}/plasma-applet-microblog.desktop
%{kde4_servicesdir}/plasma-dataengine-microblog.desktop

%files -n kde-plasma-news
%defattr(-,root,root)
%{kde4_plugindir}/plasma_applet_news.so
%{kde4_servicesdir}/plasma-applet-news.desktop

%files -n kde-plasma-notes
%defattr(-,root,root)
%{kde4_plugindir}/plasma_applet_notes.so
%{kde4_servicesdir}/plasma-notes-default.desktop

%files -n kde-plasma-nowplaying
%defattr(-,root,root)
#%{kde4_plugindir}/plasma_applet_nowplaying.so
%{kde4_servicesdir}/plasma-applet-nowplaying.desktop
%{kde4_datadir}/apps/plasma/plasmoids/nowplaying/

%files -n kde-plasma-opendesktop
%defattr(-,root,root)
%{kde4_plugindir}/plasma_applet_opendesktop.so
%{kde4_appsdir}/plasma-applet-opendesktop
%{kde4_servicesdir}/plasma-applet-opendesktop.desktop

%files -n kde-plasma-paste
%defattr(-,root,root)
%{kde4_plugindir}/plasma_engine_ocs.so
%{kde4_plugindir}/plasma_applet_paste.so
%{kde4_servicesdir}/plasma-applet-paste.desktop
%{kde4_servicesdir}/plasma-dataengine-ocs.desktop

%files -n kde-plasma-pastebin
%defattr(-,root,root)
%{kde4_plugindir}/plasma_applet_pastebin.so
#%{kde4_plugindir}/plasma_engine_pastebin.so
%{kde4_appsdir}/plasma_pastebin
%{kde4_appsdir}/plasma/services/ocsPerson.operations
#%{kde4_appsdir}/plasma/services/pastebin.operations
%{kde4_servicesdir}/plasma-applet-pastebin.desktop
#%{kde4_servicesdir}/plasma-engine-pastebin.desktop
%{kde4_configdir}/pastebin.knsrc

%files -n kde-plasma-previewer
%defattr(-,root,root)
%{kde4_plugindir}/plasma_applet_previewer.so
%{kde4_iconsdir}/hicolor/*/apps/previewer.*
%{kde4_servicesdir}/ServiceMenus/preview.desktop
%{kde4_servicesdir}/plasma-applet-previewer.desktop

%files -n kde-plasma-rssnow
%defattr(-,root,root)
%{kde4_plugindir}/plasma_applet_rssnow.so
%{kde4_appsdir}/rssnow
%{kde4_servicesdir}/plasma-applet-rssnow.desktop

%files -n kde-plasma-rtm
%defattr(-,root,root)
%{kde4_plugindir}/plasma_engine_rtm.so
%{kde4_plugindir}/plasma_applet_rtm.so
%{kde4_libdir}/librtm.so.*
%{kde4_appsdir}/plasma/services/rtmauth.operations
%{kde4_appsdir}/plasma/services/rtmtask.operations
%{kde4_appsdir}/plasma/services/rtmtasks.operations
%{kde4_servicesdir}/plasma-applet-rememberthemilk.desktop
%{kde4_servicesdir}/plasma-engine-rtm.desktop

%files -n kde-plasma-showdashboard
%defattr(-,root,root)
%{kde4_plugindir}/plasma_applet_showdashboard.so
%{kde4_servicesdir}/plasma-applet-showdashboard.desktop

%files -n kde-plasma-showdesktop
%defattr(-,root,root)
%{kde4_plugindir}/plasma_applet_showdesktop.so
%{kde4_servicesdir}/plasma-applet-showdesktop.desktop

%files -n kde-plasma-systemloadviewer
%defattr(-,root,root)
%{kde4_plugindir}/plasma-applet_systemloadviewer.so
%{kde4_servicesdir}/plasma-applet-systemloadviewer.desktop

%files -n kde-plasma-timer
%defattr(-,root,root)
%{kde4_plugindir}/plasma_applet_timer.so
%{kde4_servicesdir}/plasma-applet-timer.desktop

%files -n kde-plasma-unitconverter
%defattr(-,root,root)
%{kde4_plugindir}/krunner_converter.so
%{kde4_plugindir}/plasma_applet_unitconverter.so
%{kde4_servicesdir}/plasma-applet-unitconverter.desktop
%{kde4_servicesdir}/plasma-runner-converter.desktop

%files -n kde-plasma-weather
%defattr(-,root,root)
%{kde4_plugindir}/plasma_applet_weather.so
%{kde4_servicesdir}/plasma-applet-weather.desktop

%files -n kde-plasma-weatherstation
%defattr(-,root,root)
%{kde4_plugindir}/plasma_applet_weatherstation.so
%{kde4_servicesdir}/plasma-applet-weatherstation.desktop

%files -n kde-plasma-blackboard
%defattr(-,root,root)
%{kde4_plugindir}/plasma_applet_blackboard.so
%{kde4_servicesdir}/plasma-applet-blackboard.desktop

%files -n kde-plasma-kdeobservatory
%defattr(-,root,root)
#%{kde4_plugindir}/plasma_applet_kdeobservatory.so
%{kde4_plugindir}/plasma_engine_kdeobservatory.so
%{kde4_appsdir}/plasma/services/kdeobservatory.operations
#%{kde4_iconsdir}/hicolor/*/apps/kdeobservatory.*
#%{kde4_servicesdir}/plasma-applet-kdeobservatory.desktop
%{kde4_servicesdir}/plasma-engine-kdeobservatory.desktop

%files -n kde-plasma-kimpanel
%defattr(-,root,root)
%{kde4_plugindir}/libexec/kimpanel-*-panel
%{kde4_plugindir}/plasma_*_kimpanel.so
%{kde4_appsdir}/plasma/services/kimpanel.operations
%{kde4_kcfgdir}/kimpanelconfig.kcfg
%{kde4_servicesdir}/plasma-*-kimpanel.desktop
%{kde4_datadir}/ibus/component/kimpanel.xml

%files -n kde-plasma-knowledgebase
%defattr(-,root,root)
%{kde4_plugindir}/plasma_applet_knowledgebase.so
%{kde4_servicesdir}/plasma-applet-knowledgebase.desktop

%files -n kde-plasma-opendesktop_activities
%defattr(-,root,root)
%{kde4_plugindir}/plasma_applet_opendesktop_activities.so
%{kde4_appsdir}/plasma-applet-opendesktop-activities
%{kde4_servicesdir}/plasma-applet-opendesktop-activities.desktop

%files -n kde-plasma-plasmaboard
%defattr(-,root,root)
%{kde4_plugindir}/plasma_applet_plasmaboard.so
%{kde4_appsdir}/plasmaboard
%{kde4_servicesdir}/plasma_applet_plasmaboard.desktop

%files -n kde-plasma-qalculate
%defattr(-,root,root)
%{kde4_plugindir}/plasma_applet_qalculate.so
%{kde4_iconsdir}/hicolor/*/apps/qalculate-applet.*
%{kde4_servicesdir}/plasma-applet-qalculate.desktop

%files -n kde-plasma-spellcheck
%defattr(-,root,root)
%{kde4_plugindir}/plasma_applet_spellcheck.so
%{kde4_servicesdir}/plasma-applet-spellcheck.desktop

%files -n kde-plasma-webslice
%defattr(-,root,root)
%{kde4_plugindir}/plasma_applet_webslice.so
%{kde4_servicesdir}/plasma-applet-webslice.desktop

%files -n kde-plasma-bookmarks
%defattr(-,root,root)
%{kde4_plugindir}/plasma_applet_bookmarks.so
%{kde4_servicesdir}/plasma-applet-bookmarks.desktop

%changelog
* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 4.14.3-2
- 为 Magic 3.0 重建

* Tue Dec 30 2014 Liu Di <liudidi@gmail.com> - 4.14.3-1
- 更新到 4.14.3

* Fri Oct 24 2014 Liu Di <liudidi@gmail.com> - 4.14.2-1
- 更新到 4.14.2

* Fri Jul 18 2014 Liu Di <liudidi@gmail.com> - 4.13.3-1
- 更新到 4.13.3

* Thu Jun 19 2014 Liu Di <liudidi@gmail.com> - 4.13.2-1
- 更新到 4.13.2

* Fri Jun 06 2014 Liu Di <liudidi@gmail.com> - 4.13.1-1
- 更新到 4.13.1

* Fri Apr 25 2014 Liu Di <liudidi@gmail.com> - 4.13.0-1.2
- 为 Magic 3.0 重建

* Fri Apr 25 2014 Liu Di <liudidi@gmail.com> - 4.13.0-1.1
- 为 Magic 3.0 重建

* Mon Dec 28 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.3.4-3mgc
- 拆出 marble 和 konqueror 支持部件
- dict plasmoid dict.cn 支持
- 乙丑  十一月十三

* Thu Dec 10 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.3.4-2mgc
- 拆包
- 乙丑  十月廿四

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
- 不编译 lancelot(需要 python 2.5)
- 戊子  十一月初二

* Sun Oct 12 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.1.69-0.1mgc
- 更新至 4.1.69
- 戊子  九月十四

* Mon Sep 29 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.1.2-0.1mgc
- 更新至 4.1.2
- 戊子  九月初一

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
- 修改名称为 kdeplasmoids，extragear-plasma died~~~
- 新设立 devel 开发包
- 戊子  五月初一

* Fri May 23 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.80-0.1mgc
- 更新至 4.0.80(try1 内部版本)
- 打包没有加入非中文语言翻译文件
- 戊子  四月十九

* Sat Apr 12 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.69.svn795714-0.1mgc
- 更新至 4.0.69.svn795714
- 戊子  三月初七

* Fri Feb 8 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.1-0.1mgc
- 更新至 4.0.1

* Sat Jan 12 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.0-0.1mgc
- 更新至 4.0.0

* Sat Dec 15 2007 Ni Hui <shuizhuyuanluo@126.com> - 3.97.0-0.1mgc
- 更新至 3.97.0 (KDE4-RC2)
- 首次生成 rpm 包
