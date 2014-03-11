%define rversion %{kde4_kdelibs_version}
%define release_number 1
%define real_name kdegames

%define kde4_enable_final_bool OFF

Name: kdegames4
Summary: The KDE Games Components
Summary(zh_CN.UTF-8): KDE 游戏组件
License: LGPL v2 or later
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
URL: http://www.kde.org/
Version: %{rversion}
Release: %{release_number}%{?dist}
Source0: http://mirror.bjtu.edu.cn/kde/stable/%{rversion}/src/%{real_name}-%{rversion}.tar.xz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: libkdelibs4-devel
BuildRequires: qt4-devel >= 4.4.3


# ggz gaming zone 支持
BuildRequires: libggz-devel
BuildRequires: ggz-client-libs-devel
# kajongg
BuildRequires: python-twisted-core
BuildRequires: openal-soft-devel

Requires: %{name}-bovo = %{version}
Requires: %{name}-katomic = %{version}
Requires: %{name}-kbattleship = %{version}
Requires: %{name}-kblackbox = %{version}
Requires: %{name}-kbounce = %{version}
Requires: %{name}-kfourinline = %{version}
Requires: %{name}-kgoldrunner = %{version}
Requires: %{name}-kiriki = %{version}
Requires: %{name}-kjumpingcube = %{version}
Requires: %{name}-klines = %{version}
Requires: %{name}-kmahjongg = %{version}
Requires: %{name}-kmines = %{version}
Requires: %{name}-knetwalk = %{version}
Requires: %{name}-kolf = %{version}
Requires: %{name}-konquest = %{version}
Requires: %{name}-kpat = %{version}
Requires: %{name}-kreversi = %{version}
Requires: %{name}-klickety = %{version}
Requires: %{name}-kshisen = %{version}
Requires: %{name}-kspaceduel = %{version}
Requires: %{name}-ksquares = %{version}
Requires: %{name}-ksudoku = %{version}
Requires: %{name}-ktuberling = %{version}
Requires: %{name}-libkdegames = %{version}
Requires: %{name}-libkmahjongg = %{version}
Requires: %{name}-lskat = %{version}
Requires: %{name}-kdiamond = %{version}
Requires: %{name}-kollision = %{version}
Requires: %{name}-kubrick = %{version}
Requires: %{name}-kblocks = %{version}
Requires: %{name}-kbreakout = %{version}
Requires: %{name}-ksirk = %{version}
Requires: %{name}-bomber = %{version}
Requires: %{name}-kapman = %{version}
Requires: %{name}-killbots = %{version}
Requires: %{name}-ktron = %{version}
Requires: %{name}-granatier = %{version}
Requires: %{name}-kigo = %{version}
Requires: %{name}-palapeli = %{version}
Requires: %{name}-kajongg = %{version}


Patch800: kdegames-4.4.0-enablefinal.patch

%description
The KDE Games Components.

%description -l zh_CN.UTF-8
KDE 游戏组件。

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- 开发包
%package -n %{name}-devel
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: KDE Games Libraries: Build Environment
Requires: libkdelibs4-devel
Requires: %{name} = %{version}

%description -n %{name}-devel
This package contains all necessary include files and libraries needed
to develop KDE Games applications.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- bovo
%package -n %{name}-bovo
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: bovo

%description -n %{name}-bovo
bovo.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- katomic
%package -n %{name}-katomic
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: katomic

%description -n %{name}-katomic
katomic.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- kbattleship
%package -n %{name}-kbattleship
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: kbattleship

%description -n %{name}-kbattleship
kbattleship.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- kblackbox
%package -n %{name}-kblackbox
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: kblackbox

%description -n %{name}-kblackbox
kblackbox.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- kbounce
%package -n %{name}-kbounce
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: kbounce

%description -n %{name}-kbounce
kbounce.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- kfourinline
%package -n %{name}-kfourinline
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: kfourinline

%description -n %{name}-kfourinline
kfourinline.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- kgoldrunner
%package -n %{name}-kgoldrunner
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: kgoldrunner

%description -n %{name}-kgoldrunner
kgoldrunner.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- kiriki
%package -n %{name}-kiriki
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: kiriki

%description -n %{name}-kiriki
kiriki.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- kjumpingcube
%package -n %{name}-kjumpingcube
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: kjumpingcube

%description -n %{name}-kjumpingcube
kjumpingcube.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- klines
%package -n %{name}-klines
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: klines

%description -n %{name}-klines
klines.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- kmahjongg
%package -n %{name}-kmahjongg
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: kmahjongg

%description -n %{name}-kmahjongg
kmahjongg.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- kmines
%package -n %{name}-kmines
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: kmines

%description -n %{name}-kmines
kmines.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- knetwalk
%package -n %{name}-knetwalk
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: knetwalk

%description -n %{name}-knetwalk
knetwalk.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- kolf
%package -n %{name}-kolf
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: kolf

%description -n %{name}-kolf
kolf.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- konquest
%package -n %{name}-konquest
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: konquest

%description -n %{name}-konquest
konquest.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- kpat
%package -n %{name}-kpat
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: kpat

%description -n %{name}-kpat
kpat.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- kreversi
%package -n %{name}-kreversi
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: kreversi

%description -n %{name}-kreversi
kreversi.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- klickety
%package -n %{name}-klickety
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: klickety

%description -n %{name}-klickety
klickety.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- kshisen
%package -n %{name}-kshisen
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: kshisen

%description -n %{name}-kshisen
kshisen.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- kspaceduel
%package -n %{name}-kspaceduel
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: kspaceduel

%description -n %{name}-kspaceduel
kspaceduel.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- ksquares
%package -n %{name}-ksquares
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: ksquares

%description -n %{name}-ksquares
ksquares.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- ksudoku
%package -n %{name}-ksudoku
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: ksudoku

%description -n %{name}-ksudoku
ksudoku.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- ktuberling
%package -n %{name}-ktuberling
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: ktuberling

%description -n %{name}-ktuberling
ktuberling.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- libkdegames
%package -n %{name}-libkdegames
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: libkdegames

%description -n %{name}-libkdegames
libkdegames.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- libkmahjongg
%package -n %{name}-libkmahjongg
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: libkmahjongg

%description -n %{name}-libkmahjongg
libkmahjongg.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- lskat
%package -n %{name}-lskat
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: lskat

%description -n %{name}-lskat
lskat.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- kdiamond
%package -n %{name}-kdiamond
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: kdiamond

%description -n %{name}-kdiamond
kdiamond.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- kollision
%package -n %{name}-kollision
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: kollision

%description -n %{name}-kollision
kollision.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- kubrick
%package -n %{name}-kubrick
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: kubrick

%description -n %{name}-kubrick
kubrick.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- kblocks
%package -n %{name}-kblocks
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: kblocks

%description -n %{name}-kblocks
kblocks.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- kbreakout
%package -n %{name}-kbreakout
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: kbreakout

%description -n %{name}-kbreakout
kbreakout.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- ksirk
%package -n %{name}-ksirk
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: ksirk

%description -n %{name}-ksirk
ksirk.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- bomber
%package -n %{name}-bomber
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: bomber

%description -n %{name}-bomber
bomber.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- kapman
%package -n %{name}-kapman
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: kapman

%description -n %{name}-kapman
kapman.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- killbots
%package -n %{name}-killbots
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: killbots

%description -n %{name}-killbots
killbots.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- ktron
%package -n %{name}-ktron
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: ktron

%description -n %{name}-ktron
ktron.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- granatier
%package -n %{name}-granatier
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: granatier

%description -n %{name}-granatier
granatier.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- kigo
%package -n %{name}-kigo
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: kigo

%description -n %{name}-kigo
kigo.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- palapeli
%package -n %{name}-palapeli
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: palapeli

%description -n %{name}-palapeli
palapeli.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- kajongg
%package -n %{name}-kajongg
Group: System/GUI/KDE
Group(zh_CN.UTF-8): 系统/GUI/KDE
Summary: kajongg
Requires: PyKDE4
Requires: python-twisted-core

%description -n %{name}-kajongg
kajongg.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
%prep
%setup -q -n %{real_name}-%{rversion}

# compile fix
#%patch800 -p1

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

%post -n %{name}-kolf -p /sbin/ldconfig
%postun -n %{name}-kolf -p /sbin/ldconfig

%post -n %{name}-ksirk -p /sbin/ldconfig
%postun -n %{name}-ksirk -p /sbin/ldconfig

%post -n %{name}-libkdegames -p /sbin/ldconfig
%postun -n %{name}-libkdegames -p /sbin/ldconfig

%post -n %{name}-libkmahjongg -p /sbin/ldconfig
%postun -n %{name}-libkmahjongg -p /sbin/ldconfig

%post -n %{name}-palapeli -p /sbin/ldconfig
%postun -n %{name}-palapeli -p /sbin/ldconfig

%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files -n %{name}-devel
%defattr(-,root,root)
%{kde4_includedir}/*
%{kde4_libdir}/*.so
%{kde4_libdir}/libpala/*.cmake
%{kde4_libdir}/cmake/KDEGames/*.cmake

%files
%defattr(-,root,root)

%files -n %{name}-bovo
%defattr(-,root,root)
%{kde4_bindir}/bovo
%{kde4_appsdir}/bovo/*
%{kde4_iconsdir}/hicolor/*/apps/bovo.*
%{kde4_xdgappsdir}/bovo.desktop
%doc %lang(en) %{kde4_htmldir}/en/bovo

%files -n %{name}-katomic
%defattr(-,root,root)
%{kde4_bindir}/katomic
%{kde4_appsdir}/katomic/*
%{kde4_appsdir}/kconf_update/katomic*
%config %{kde4_configdir}/katomic.knsrc
%{kde4_iconsdir}/hicolor/*/apps/katomic.*
%{kde4_xdgappsdir}/katomic.desktop
%doc %lang(en) %{kde4_htmldir}/en/katomic

%files -n %{name}-kbattleship
%defattr(-,root,root)
%{kde4_bindir}/kbattleship
%{kde4_appsdir}/kbattleship/*
%{kde4_iconsdir}/hicolor/*/apps/kbattleship.*
%{kde4_xdgappsdir}/kbattleship.desktop
%{kde4_servicesdir}/kbattleship.protocol
%doc %lang(en) %{kde4_htmldir}/en/kbattleship

%files -n %{name}-kblackbox
%defattr(-,root,root)
%{kde4_bindir}/kblackbox
%{kde4_appsdir}/kblackbox/*
%{kde4_iconsdir}/hicolor/*/apps/kblackbox.*
%{kde4_xdgappsdir}/kblackbox.desktop
%doc %lang(en) %{kde4_htmldir}/en/kblackbox

%files -n %{name}-kbounce
%defattr(-,root,root)
%{kde4_bindir}/kbounce
%{kde4_appsdir}/kbounce/*
%{kde4_iconsdir}/hicolor/*/apps/kbounce.*
%{kde4_xdgappsdir}/kbounce.desktop
%doc %lang(en) %{kde4_htmldir}/en/kbounce

%files -n %{name}-kfourinline
%defattr(-,root,root)
%{kde4_bindir}/kfourinline*
%{kde4_appsdir}/kfourinline/*
%{kde4_kcfgdir}/kwin4.kcfg
%{kde4_iconsdir}/hicolor/*/apps/kfourinline.*
%{kde4_xdgappsdir}/kfourinline.desktop
%doc %lang(en) %{kde4_htmldir}/en/kfourinline

%files -n %{name}-kgoldrunner
%defattr(-,root,root)
%{kde4_bindir}/kgoldrunner
%{kde4_appsdir}/kgoldrunner/*
%config %{kde4_configdir}/kgoldrunner.knsrc
%{kde4_iconsdir}/hicolor/*/apps/kgoldrunner.*
%{kde4_xdgappsdir}/KGoldrunner.desktop
%doc %lang(en) %{kde4_htmldir}/en/kgoldrunner

%files -n %{name}-kiriki
%defattr(-,root,root)
%{kde4_bindir}/kiriki
%{kde4_appsdir}/kiriki/*
%{kde4_iconsdir}/hicolor/*/apps/kiriki.*
%{kde4_xdgappsdir}/kiriki.desktop
%doc %lang(en) %{kde4_htmldir}/en/kiriki

%files -n %{name}-kjumpingcube
%defattr(-,root,root)
%{kde4_bindir}/kjumpingcube
%{kde4_appsdir}/kjumpingcube/*
%{kde4_kcfgdir}/kjumpingcube.kcfg
%{kde4_iconsdir}/hicolor/*/apps/kjumpingcube.*
%{kde4_xdgappsdir}/kjumpingcube.desktop
%doc %lang(en) %{kde4_htmldir}/en/kjumpingcube

%files -n %{name}-klines
%defattr(-,root,root)
%{kde4_bindir}/klines
%{kde4_appsdir}/klines/*
%{kde4_kcfgdir}/klines.kcfg
%{kde4_iconsdir}/hicolor/*/apps/klines.*
%{kde4_xdgappsdir}/klines.desktop
%doc %lang(en) %{kde4_htmldir}/en/klines

%files -n %{name}-kmahjongg
%defattr(-,root,root)
%{kde4_bindir}/kmahjongg
%{kde4_appsdir}/kmahjongg/*
%{kde4_kcfgdir}/kmahjongg.kcfg
%{kde4_iconsdir}/hicolor/*/apps/kmahjongg.*
%{kde4_xdgappsdir}/kmahjongg.desktop
%doc %lang(en) %{kde4_htmldir}/en/kmahjongg

%files -n %{name}-kmines
%defattr(-,root,root)
%{kde4_bindir}/kmines
%{kde4_appsdir}/kmines/*
%config %{kde4_configdir}/kmines.knsrc
%{kde4_iconsdir}/hicolor/*/apps/kmines.*
%{kde4_xdgappsdir}/kmines.desktop
%doc %lang(en) %{kde4_htmldir}/en/kmines

%files -n %{name}-knetwalk
%defattr(-,root,root)
%{kde4_bindir}/knetwalk
%{kde4_appsdir}/knetwalk/*
%{kde4_iconsdir}/hicolor/*/apps/knetwalk.*
%{kde4_xdgappsdir}/knetwalk.desktop
%doc %lang(en) %{kde4_htmldir}/en/knetwalk

%files -n %{name}-kolf
%defattr(-,root,root)
%{kde4_bindir}/kolf
%{kde4_libdir}/libkolfprivate.so.*
%{kde4_appsdir}/kolf/*
%{kde4_iconsdir}/hicolor/*/apps/kolf.*
%{kde4_xdgappsdir}/kolf.desktop
%doc %lang(en) %{kde4_htmldir}/en/kolf

%files -n %{name}-konquest
%defattr(-,root,root)
%{kde4_bindir}/konquest
%{kde4_appsdir}/konquest/*
%{kde4_iconsdir}/hicolor/*/apps/konquest.*
%{kde4_xdgappsdir}/konquest.desktop
%doc %lang(en) %{kde4_htmldir}/en/konquest

%files -n %{name}-kpat
%defattr(-,root,root)
%{kde4_bindir}/kpat
%{kde4_appsdir}/kpat/*
%{kde4_kcfgdir}/kpat.kcfg
%config %{kde4_configdir}/kpat.knsrc
%{kde4_iconsdir}/hicolor/*/apps/kpat.*
%{kde4_xdgappsdir}/kpat.desktop
%doc %lang(en) %{kde4_htmldir}/en/kpat

%files -n %{name}-kreversi
%defattr(-,root,root)
%{kde4_bindir}/kreversi
%{kde4_appsdir}/kreversi/*
%{kde4_iconsdir}/hicolor/*/apps/kreversi.*
%{kde4_iconsdir}/oxygen/*/actions/lastmoves.*
%{kde4_iconsdir}/oxygen/*/actions/legalmoves.*
%{kde4_xdgappsdir}/kreversi.desktop
%doc %lang(en) %{kde4_htmldir}/en/kreversi

%files -n %{name}-klickety
%defattr(-,root,root)
%{kde4_bindir}/klickety
%{kde4_appsdir}/klickety/*
%{kde4_iconsdir}/hicolor/*/apps/klickety.*
%{kde4_xdgappsdir}/klickety.desktop
%{kde4_xdgappsdir}/ksame.desktop
%{kde4_appsdir}/kconf_update/*
%{kde4_iconsdir}/hicolor/*/apps/ksame.*
%doc %lang(en) %{kde4_htmldir}/en/klickety

%files -n %{name}-kshisen
%defattr(-,root,root)
%{kde4_bindir}/kshisen
%{kde4_appsdir}/kshisen/*
%{kde4_kcfgdir}/kshisen.kcfg
%{kde4_datadir}/sounds/kshisen/*
%{kde4_xdgappsdir}/kshisen.desktop
%{kde4_iconsdir}/hicolor/*/apps/kshisen.*
%doc %lang(en) %{kde4_htmldir}/en/kshisen

%files -n %{name}-kspaceduel
%defattr(-,root,root)
%{kde4_bindir}/kspaceduel
%{kde4_appsdir}/kspaceduel/*
%{kde4_kcfgdir}/kspaceduel.kcfg
%{kde4_iconsdir}/hicolor/*/apps/kspaceduel.*
%{kde4_xdgappsdir}/kspaceduel.desktop
%doc %lang(en) %{kde4_htmldir}/en/kspaceduel

%files -n %{name}-ksquares
%defattr(-,root,root)
%{kde4_bindir}/ksquares
%{kde4_appsdir}/ksquares/*
%{kde4_kcfgdir}/ksquares.kcfg
%{kde4_iconsdir}/hicolor/*/apps/ksquares.*
%{kde4_xdgappsdir}/ksquares.desktop
%doc %lang(en) %{kde4_htmldir}/en/ksquares

%files -n %{name}-ksudoku
%defattr(-,root,root)
%{kde4_bindir}/ksudoku
%{kde4_appsdir}/ksudoku/*
%config %{kde4_configdir}/ksudokurc
%{kde4_iconsdir}/hicolor/*/apps/ksudoku.*
%{kde4_xdgappsdir}/ksudoku.desktop
%doc %lang(en) %{kde4_htmldir}/en/ksudoku

%files -n %{name}-ktuberling
%defattr(-,root,root)
%{kde4_bindir}/ktuberling
%{kde4_appsdir}/ktuberling/*
%{kde4_iconsdir}/hicolor/*/apps/ktuberling.*
%{kde4_iconsdir}/hicolor/*/mimetypes/application-x-tuberling.*
%{kde4_xdgappsdir}/ktuberling.desktop
%doc %lang(en) %{kde4_htmldir}/en/ktuberling

%files -n %{name}-libkdegames
%defattr(-,root,root)
#%{kde4_sysconfdir}/ggz.modules.d/kdegames
%{kde4_libdir}/libkdegames.so.*
%{kde4_libdir}/libkdegamesprivate.so.*
%{kde4_appsdir}/carddecks/*
%config %{kde4_configdir}/kcardtheme.knsrc

%files -n %{name}-libkmahjongg
%defattr(-,root,root)
%{kde4_libdir}/libkmahjongglib.so.*
%{kde4_appsdir}/kmahjongglib/*

%files -n %{name}-lskat
%defattr(-,root,root)
%{kde4_bindir}/lskat
%{kde4_appsdir}/lskat/*
%{kde4_iconsdir}/hicolor/*/apps/lskat.*
%{kde4_xdgappsdir}/lskat.desktop
%doc %lang(en) %{kde4_htmldir}/en/lskat

%files -n %{name}-kdiamond
%defattr(-,root,root)
%{kde4_bindir}/kdiamond
%{kde4_appsdir}/kdiamond/*
%config %{kde4_configdir}/kdiamond.knsrc
%{kde4_iconsdir}/hicolor/*/apps/kdiamond.*
%{kde4_datadir}/sounds/KDiamond-*.ogg
%{kde4_xdgappsdir}/kdiamond.desktop
%doc %lang(en) %{kde4_htmldir}/en/kdiamond

%files -n %{name}-kollision
%defattr(-,root,root)
%{kde4_bindir}/kollision
%{kde4_appsdir}/kollision/*
%{kde4_iconsdir}/hicolor/*/apps/kollision.*
%{kde4_iconsdir}/oxygen/*/apps/kollision.*
%{kde4_xdgappsdir}/kollision.desktop
%doc %lang(en) %{kde4_htmldir}/en/kollision

%files -n %{name}-kubrick
%defattr(-,root,root)
%{kde4_bindir}/kubrick
%{kde4_appsdir}/kubrick/*
%{kde4_iconsdir}/hicolor/*/apps/kubrick.*
%{kde4_xdgappsdir}/kubrick.desktop
%doc %lang(en) %{kde4_htmldir}/en/kubrick

%files -n %{name}-kblocks
%defattr(-,root,root)
%{kde4_bindir}/kblocks
%{kde4_appsdir}/kblocks/*
%config %{kde4_configdir}/kblocks.knsrc
%{kde4_kcfgdir}/kblocks.kcfg
%{kde4_iconsdir}/hicolor/*/apps/kblocks.*
%{kde4_xdgappsdir}/kblocks.desktop
%doc %lang(en) %{kde4_htmldir}/en/kblocks

%files -n %{name}-kbreakout
%defattr(-,root,root)
%{kde4_bindir}/kbreakout
%{kde4_appsdir}/kbreakout/*
%{kde4_iconsdir}/hicolor/*/apps/kbreakout.*
%{kde4_xdgappsdir}/kbreakout.desktop
%doc %lang(en) %{kde4_htmldir}/en/kbreakout

%files -n %{name}-ksirk
%defattr(-,root,root)
%{kde4_bindir}/ksirk
%{kde4_bindir}/ksirkskineditor
%{kde4_libdir}/libiris_ksirk.so.*
%{kde4_appsdir}/ksirk/*
%{kde4_appsdir}/ksirkskineditor/*
%config %{kde4_configdir}/ksirk.knsrc
%{kde4_kcfgdir}/ksirksettings.kcfg
%{kde4_kcfgdir}/ksirkskineditorsettings.kcfg
%{kde4_iconsdir}/hicolor/*/apps/ksirk.*
%{kde4_iconsdir}/locolor/*/apps/ksirk.*
%{kde4_xdgappsdir}/ksirk.desktop
%{kde4_xdgappsdir}/ksirkskineditor.desktop
%doc %lang(en) %{kde4_htmldir}/en/ksirk
%doc %lang(en) %{kde4_htmldir}/en/ksirkskineditor

%files -n %{name}-bomber
%defattr(-,root,root)
%{kde4_bindir}/bomber
%{kde4_appsdir}/bomber/*
%{kde4_kcfgdir}/bomber.kcfg
%{kde4_iconsdir}/hicolor/*/apps/bomber.*
%{kde4_xdgappsdir}/bomber.desktop
%doc %lang(en) %{kde4_htmldir}/en/bomber

%files -n %{name}-kapman
%defattr(-,root,root)
%{kde4_bindir}/kapman
%{kde4_appsdir}/kapman/*
%{kde4_iconsdir}/hicolor/*/apps/kapman.*
%{kde4_datadir}/sounds/kapman/*.ogg
%{kde4_xdgappsdir}/kapman.desktop
%doc %lang(en) %{kde4_htmldir}/en/kapman

%files -n %{name}-killbots
%defattr(-,root,root)
%{kde4_bindir}/killbots
%{kde4_appsdir}/killbots/*
%{kde4_kcfgdir}/killbots.kcfg
%{kde4_iconsdir}/hicolor/*/apps/killbots.*
%{kde4_xdgappsdir}/killbots.desktop
%doc %lang(en) %{kde4_htmldir}/en/killbots

%files -n %{name}-ktron
%defattr(-,root,root)
%{kde4_bindir}/kdesnake
%{kde4_bindir}/ktron
%{kde4_appsdir}/ktron/*
%{kde4_kcfgdir}/ktron.kcfg
%config %{kde4_configdir}/ktron.knsrc
%{kde4_iconsdir}/hicolor/*/apps/kdesnake.*
%{kde4_iconsdir}/hicolor/*/apps/ktron.*
%{kde4_xdgappsdir}/kdesnake.desktop
%{kde4_xdgappsdir}/ktron.desktop
%doc %lang(en) %{kde4_htmldir}/en/ktron

%files -n %{name}-granatier
%defattr(-,root,root)
%{kde4_bindir}/granatier
%{kde4_appsdir}/granatier/*
%{kde4_kcfgdir}/granatier.kcfg
%{kde4_iconsdir}/hicolor/*/apps/granatier.*
%{kde4_xdgappsdir}/granatier.desktop
%doc %lang(en) %{kde4_htmldir}/en/granatier

%files -n %{name}-kigo
%defattr(-,root,root)
%{kde4_bindir}/kigo
%{kde4_appsdir}/kigo/*
%config %{kde4_configdir}/kigo*.knsrc
%{kde4_kcfgdir}/kigo.kcfg
%{kde4_iconsdir}/hicolor/*/apps/kigo.*
%{kde4_xdgappsdir}/kigo.desktop
%doc %lang(en) %{kde4_htmldir}/en/kigo

%files -n %{name}-palapeli
%defattr(-,root,root)
%{kde4_bindir}/palapeli
#%{kde4_bindir}/libpala-puzzlebuilder
%{kde4_libdir}/libpala.so.*
%{kde4_plugindir}/palapeli_*.so
%{kde4_plugindir}/palathumbcreator.so
%{kde4_appsdir}/palapeli/*
%config %{kde4_configdir}/palapeli*rc
%{kde4_datadir}/mime/packages/palapeli-mimetypes.xml
%{kde4_iconsdir}/hicolor/*/apps/palapeli.*
%{kde4_iconsdir}/hicolor/*/mimetypes/application-x-palapeli.*
%{kde4_xdgappsdir}/palapeli.desktop
%{kde4_servicesdir}/palapeli_*.desktop
%{kde4_servicesdir}/palathumbcreator.desktop
%{kde4_servicesdir}/ServiceMenus/palapeli_servicemenu.desktop
%{kde4_servicetypesdir}/libpala-*.desktop
%doc %lang(en) %{kde4_htmldir}/en/palapeli
%{kde4_datadir}/mime/packages/kpatience.xml

%files -n %{name}-kajongg
%defattr(-,root,root)
%{kde4_bindir}/kajongg
%{kde4_bindir}/kajonggserver
%{kde4_appsdir}/kajongg/*
%{kde4_iconsdir}/hicolor/*/actions/games-kajongg-law.*
%{kde4_iconsdir}/hicolor/*/apps/kajongg.*
%{kde4_xdgappsdir}/kajongg.desktop
%doc %lang(en) %{kde4_htmldir}/en/kajongg

%changelog
* Wed Aug 5 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.3.0-1mgc
- 更新至 4.3.0(KDE 4.3 final)
- 己丑  六月十五

* Tue Jun 30 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.95-1mgc
- 更新至 4.2.95(KDE 4.3 RC1)
- 己丑  闰五月初八

* Sat Jun 13 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.91-1mgc
- 更新至 4.2.91
- 己丑  五月廿一

* Sun May 17 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.85-1mgc
- 更新至 4.2.85(KDE 4.3 beta1)
- 己丑  四月廿三

* Sat Apr 4 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.2-1mgc
- 更新至 4.2.2
- 己丑  三月初九  [清明]

* Sun Mar 15 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.1-0.1mgc
- 更新至 4.2.1
- 己丑  二月十九

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
- /etc/ggz.modules 不存在...
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

* Thu Jul 24 2008 Liu Di <liudidi@gmail.com> - 4.1.0-0.1mgc
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

* Fri May 23 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.80-0.1mgc
- 更新至 4.0.80(try1 内部版本)
- 戊子  四月十九

* Fri May 16 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.74-0.1mgc
- 更新至 4.0.74
- 戊子  四月十二

* Sat Apr 26 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.71-0.1mgc
- 更新至 4.0.71
- 更改 /etc 安装路径，以便获得网络对战支持
- 戊子  三月廿一

* Sat Apr 19 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.70-0.1mgc
- 更新至 4.0.70
- 纳入 ggz 支持(网络对战游戏支持)
- 戊子  三月十四

* Fri Apr 4 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.3-0.1mgc
- 更新至 4.0.3
- 戊子  二月廿八  [清明]

* Tue Mar 4 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.2-0.1mgc
- 更新至 4.0.2
- 戊子  正月廿七

* Sun Feb 10 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.1-0.1mgc
- 更新至 4.0.1

* Sat Jan 12 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.0-0.1mgc
- 更新至 4.0.0

* Sat Dec 16 2007 Ni Hui <shuizhuyuanluo@126.com> - 3.97.0-0.1mgc
- 更新至 3.97.0 (KDE4-RC2)

* Sat Nov 24 2007 Ni Hui <shuizhuyuanluo@126.com> - 3.96.0-0.1mgc
- 更新至 3.96.0 (KDE4-RC1)

* Sat Oct 20 2007 Ni Hui <shuizhuyuanluo@126.com> - 3.94.0-0.1mgc
- 首次生成 rpm 包
