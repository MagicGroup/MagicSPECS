%define snapshot 0
%define snapver 642131
%define git 1
%define gitdate 20111213
%define debug 0
%define final 0
%define pie 0

%define qt_version 3.3.8d
%define arts_version 1.5.14
%define kde_version 3.5.14

%define libtool 1
%define arts 1
%define java 1

Summary: K Desktop Environment - core files
Summary(zh_CN.UTF-8): K 桌面环境 - 核心文件
Name:          tdebase
Version:       3.5.14
%if %{git}
Release:       0.git%{gitdate}%{?dist}
%else
Release:       0.1%{?dist}
%endif
License:     GPL
URL: 		http://www.kde.org
Group:         User Interface/Desktops
Group(zh_CN.UTF-8):  用户界面/桌面
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)
%if %{git}
Source:      %{name}-git%{gitdate}.tar.xz
%else
Source:	     %{name}-%{version}.tar.bz2
%endif
#Source1:     magic_conf.tar.gz
Source1:    addwav.tar.bz2

Source5:     socket.png 
Source6:     kded.png
Source7:     smserver.png
Source8:     calendars.png


#Source9:     startkde
#Source10:    wallpapers.tar.gz
Source11:    magic-panel.png
Source12:	kde-np.pamd
Source13:	rm-kdeconfig.sh
Source14:	kde.pamd

Source100:	make_tdebase_git_package.sh

Patch1:		kdebase-3.5.10-gcc44.patch
Patch2:        kdebase-kcmlauch.patch
Patch8:         kdebase-kcookiespolicy.patch
Patch9: 	kdebase-genkdmconf-magic.patch
Patch10:	kdebase-startkde-magic.patch
Patch14:       kdebase-nodate.patch 
Patch22: kdebase-java-check.patch
#Patch23: kcontrol-fontname.patch
Patch24: konqueror-dbclick_closetab.patch
#Patch25: kdebase-3.4.2_autoplay.patch
Patch26: kdebase-kde-internet.directory-translate.patch
#Patch30: kicker_crash.patch
Patch31: kdebase-pluginscan.patch
Patch32: kdebase-nsplugin.patch
Patch33: kdebase-3.4.90-drkonqi.patch
#Patch34: kdebase-3.5-refine-viewmode-toolbar-button.patch
Patch35: kdebase-init_keyboard_layout.patch
Patch36: kdebase-KioFonts_font_path.patch
Patch37: kdebase-kiotrash-ugly-fix-for-chinese-filename.patch
Patch38: kdebase-extra_function.patch
Patch39: kdebase-opengl_compile_fix.patch

#Patch51: kdebase-3.5.3-dbus.patch
Patch52: kdebase-3.5.1-kdm-readme.patch
Patch53: kdebase-3.5.1-konsole-fonts.patch
#Patch54: kdebase-3.3.1-pam_krb5-bz#191049.patch
Patch55: kdebase-3.5.2-kconf_update-klipper.patch
Patch56: kdebase-3.5.3-keyinit.patch
Patch57: kdebase-3.5.3-khelpcenter-sort.patch
Patch58: kdebase-3.5.4-htdig.patch
#Patch59: kdebase-3.5.4-antialias.patch
Patch60: kdebase-3.5.5-kdeeject.patch

Patch61: kdebase-3.5.5-dbus.patch
Patch62: kdebase-kioslave-detect-media-types.patch

Patch63: kdebase-knotify-volume.patch

Patch64: kdebase-3.5.5-redhat-pam.patch
Patch65: kdebase-3.5.7-kio_media_mounthelper.patch
Patch66: kdebase-3.5.8-konsole-bz#244906.patch
Patch67: kdebase-3.5.9-lmsensors.patch
Patch68: kdebase-3.5.9-userdiskmount.patch

Patch69: tdebase-git20111213-localtdedir.patch
Patch70: tdebase-git20111213-xtst.patch

# from everest
Patch100:kdebase-3.5.1-convert-ogg-to-wav.patch
Patch101:kdebase-3.5.1-fix-kwin-eventsrc-to-wav.patch
Patch102:kdebase-3.5.1-fix-konsole-eventsrc-to-wav.patch


#kicker may be crash, but it took us a lot of time to handle the crash, just let it crash!!
Patch104:kdebase-just-make-kicker-crash-easy.patch
Patch105: kdebase-fix-ntp-server-add-timezone-search.patch
Patch106: konqueror-closelasttab.patch

# upstream patches
# security patches
Patch1000: post-3.5.7-kdebase-kdm.diff
Patch1001: post-3.5.7-kdebase-konqueror-2.diff

#taskbartip 的补丁，来自 lovewilliam(stdio)
Patch2000: kdebase-3.5.9-taskbarTipFixer.patch
Patch2001: kdebase-3.5.9-taskbarTipFixerKCM.patch

Patch2002: kdebase-3.5.13-gcc45.patch

Requires: kdelibs, libxml2, xinitrc, shadow-utils, fileutils, glibc, sh-utils, bash, arts, audiofile, openssl, freetype, fontconfig, samba, expect
Requires: %{name}-core
Requires: %{name}-nsplugins
Requires: %{name}-kate
Requires: %{name}-konsole
Requires: %{name}-kmenuedit

Provides: kdebase

%description
Core applications for the K Desktop Environment.  Included are: kdm
(replacement for xdm), twin (window manager), konqueror (filemanager,
web browser, ftp client, ...), konsole (xterm replacement), kpanel
(application starter and desktop pager), kaudio (audio server),
kdehelp (viewer for kde help files, info and man pages), kthememgr
(system for managing alternate theme packages) plus other KDE
components (kcheckpass, kikbd, kscreensaver, kcontrol, kfind,
kfontmanager, kmenuedit).

%description -l zh_CN.UTF-8
Kdebase 是 K 桌面环境(KDE)的核心应用程序。包括：kdm（xdm的替代品），twin（窗口管理器），
konqueor（文件管理器，网页浏览器，ftp 客户端，...），konsole（xterm 的替代品），
kpanel（应用程序启动器和桌面页），kaudio（声音服务），kdehelp（kde 帮助文件，info
和手册页的查看器），kthememgr（管理主题包的系统），其它的 KDE 组件(kcheckpass, 
kikbd, kscreensaver, kcontrol, kfind,kfontmanager, kmenuedit).

%package devel
Summary: Development files for kdebase
Summary(zh_CN.UTF-8): kdebase的开发文件
Requires: kdebase
Requires: kdelibs-devel = %{version}
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库

Provides: kdebase-devel

%description devel
Header files for developing applications using kdebase.
Install kdebase-devel if you want to develop or compile Konqueror,
Kate plugins or KWin styles.

%description devel -l zh_CN.UTF-8
使用 kdebase 开发应用程序所需要的头文件。


%package core
Summary: kdebase core file
Summary(zh_CN.UTF-8): Kdebase 的核心文件
Group: User Interface/Desktops
Group(zh_CN.UTF-8):  用户界面/桌面
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils

Provides: kdebase-core
 
%description core
kdebase core file.
 
%description core -l zh_CN.UTF-8
Kdebase 的核心文件。

#************************************************************************8

%package ksysguard
Summary: Ksysguard
Summary(zh_CN.UTF-8): Ksysguard
Group: User Interface/Desktops
Group(zh_CN.UTF-8):  用户界面/桌面
Provides: ksysguard
Provides: kdebase-ksysguard
Requires: tdebase-core = %version-%release
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils
 
%description ksysguard
KDE System Guard Daemon is the daemon part of ksysguard. The daemon can
be installed on a remote machine to enable ksysguard on another machine
to monitor it through the daemon running there.

%description ksysguard -l zh_CN.UTF-8
KDE 系统防护服务是 ksysguard 的服务部分。这个服务可以安装到远程机器，从而
从其它机器通过这个服务来监视 ksysguard。

#*************************************************************************

%package konsole
Summary:        Konsole
Summary(zh_CN.UTF-8): KDE 终端程序
Group:          User Interface/Desktops
Group(zh_CN.UTF-8):   用户界面/桌面
Requires:       tdebase-core = %version-%release
Provides:       konsole
Provides:	kdebase-konsole
Requires: 	fontconfig
 
%description konsole
A shell program similar to xterm for KDE

%description konsole -l zh_CN.UTF-8
KDE 下的外壳程序，类似 xterm。
 
%post konsole
/sbin/ldconfig
/usr/sbin/update-alternatives --install /usr/bin/xvt xvt /usr/bin/konsole 35
/usr/bin/fc-cache
 
%postun konsole
/sbin/ldconfig
if [ "$1" = "0" ]; then
   /usr/sbin/update-alternatives --remove xvt /usr/bin/konsole
fi

#****************************************************************************

%package kdeprintfax
Summary:        Kdeprintfax
Summary(zh_CN.UTF-8): 发送传真的 KDE 程序
Group:          User Interface/Desktops
Group(zh_CN.UTF-8):   用户界面/桌面
Requires:       %name-core = %version-%release
Provides:       kdeprintfax
Provides:	kdebase-kdeprintfax
Requires:       enscript
Requires:       efax
 
%description kdeprintfax
Programm to send fax

%description kdeprintfax -l zh_CN.UTF-8
发送传真的程序。

#*****************************************************************************

%package kate
Summary:        Kate
Summary(zh_CN.UTF-8): KDE 下的高级文本编辑器
Group:          User Interface/Desktops
Group(zh_CN.UTF-8):   用户界面/桌面
Requires:       %name-core = %version-%release
Provides:       kate
Provides:	kdebase-kate
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils
 
%description kate
A fast and advanced text editor with nice plugins

%description kate -l zh_CN.UTF-8
KDE 下的高级文本编辑器。

#*****************************************************************************

%package nsplugins
Summary:        Netscape Plugins for kdebase
Summary(zh_CN.UTF-8):	kdebase 的 Netscape 插件
Group:          User Interface/Desktops
Group(zh_CN.UTF-8):   用户界面/桌面
Requires:       %name-core = %version-%release
 
%description nsplugins
This package contains the Netscape plugins for konqueror files.

%description nsplugins -l zh_CN.UTF-8
这个包包含了 Konqueror 的 Netscape 插件支持。

#*****************************************************************************

%package kmenuedit
Summary:    kmenuedit
Summary(zh_CN.UTF-8): KDE 菜单编辑器
Group:      User Interface/Desktops
Group(zh_CN.UTF-8):   用户界面/桌面
Requires:       %name-core = %version-%release
Provides:       kmenuedit
 
%description kmenuedit
Kmenuedit for kdebase
 
%description kmenuedit -l zh_CN.UTF-8
KDE 的 K 菜单编辑器

#*****************************************************************************

%package kdm
Summary:    kdm for kdebase
Summary(zh_CN.UTF-8): KDE 的登录管理器
Group:      User Interface/Desktops
Group(zh_CN.UTF-8):   用户界面/桌面
Requires:       magic-kdm-config
Provides:       kdm
Requires:       xinitrc
Requires:       kdebase-core = %version-%release
 
%description kdm
This package contains kdm.

%description kdm -l zh_CN.UTF-8
KDE 的登录管理器。

%prep
%if %git
%setup -q -n %{name}-git%{gitdate} -a 1
%else
%setup -q -a 1
%endif

#%patch1 -p1
#%patch2 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1 -b .orig
%patch14 -p1
%patch22 -p1 -b .javacheck
#patch23 -p1 -b .fontname
%patch24 -p1 -b .closetab
#patch25 -p1 -b .autoplay
%patch26 -p1 -b .translate
#patch30 -p1 -b .kicker
%patch31 -p1 -b .pluginscan
%patch32 -p1 -b .nsplugin
%patch33 -p1 -b .drkonqi
#patch34 -p1 -b .toolbar
%patch35 -p1 -b .init_keyboard
%patch36 -p1 -b .kiofont
%patch37 -p1 -b .kiotrash
%patch38 -p1 -b .extra
%patch39 -p1 -b .opengl

#patch51 -p1
%patch52 -p1
%patch53 -p1
#patch54 -p1
%patch55 -p1
%patch56 -p1
%patch57 -p1
#%patch58 -p1
#patch59 -p1
%patch60 -p1 -b .kdeeject

%patch61 -p1
%patch62 -p0 -b .cd_check
%patch63 -p1

%patch64 -p1
#%patch65 -p1
#%patch66 -p1
#%patch67 -p0
#%patch68 -p1
%patch69 -p1
%patch70 -p1

%patch100 -p1
%patch101 -p1
%patch102 -p1
%patch104 -p1
%patch105 -p1
%patch106 -p1 -b .closelasttab

%patch2000 -p1
%patch2001 -p1

#%patch2002 -p1

%Build
# set some default enviroments
unset QTDIR && . /etc/profile.d/qt.sh
FLAGS="$RPM_OPT_FLAGS"

export CXXFLAGS="$FLAGS"
export CFLAGS="$FLAGS"
export KDEDIR=%{_prefix}

if pkg-config openssl ; then
   CFLAGS="$CFLAGS `pkg-config --cflags openssl`"
   CXXFLAGS="$CXXFLAGS `pkg-config --cflags openssl`"
   CPPFLAGS="$CPPFLAGS `pkg-config --cflags-only-I openssl`"
   LDFLAGS="$LDFLAGS `pkg-config --libs-only-L openssl`"
fi

cp %{SOURCE12} .

mkdir build
cd build
%cmake  -DBUILD_ALL=ON \
	-DWITH_SASL=ON \
	-DWITH_LDAP=ON \
	-DWITH_SAMBA=ON \
	-DWITH_OPENEXR=ON \
	-DWITH_OPENEXR=ON \
	-DWITH_XCURSOR=ON \
	-DWITH_XFIXES=ON \
	-DWITH_XRANDR=ON \
	-DWITH_XRENDER=ON \
	-DWITH_XDAMAGE=ON \
	-DWITH_XEXT=ON \
	-DWITH_LIBUSB=ON \
	-DWITH_LIBRAW1394=ON \
	-DWITH_SUDO_TDESU_BACKEND=ON \
	-DWITH_PAM=ON \
	-DWITH_SHADOW=ON \
	-DWITH_XDMCP=ON \
	-DWITH_XTST=ON \
	-DWITH_XINERAMA=ON \
	-DWITH_ARTS=ON \
	-DWITH_I8K=ON \
	-DWITH_HAL=ON ..
	
# 临时措施
sed -i 's/lXcomposite/lXcomposite\ \-lXtst/g' kioslave/trash/CMakeFiles/kio_trash-module.dir/link.txt

# use unsermake instead of make, don't use %{?_smp_mflags}
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
mkdir -p $RPM_BUILD_ROOT
cd build
make DESTDIR=$RPM_BUILD_ROOT install

# Fix up permissions on some things
chmod 755 $RPM_BUILD_ROOT%{_bindir}/kcheckpass
chmod 755 $RPM_BUILD_ROOT%{_bindir}/tdesud
chmod 755 $RPM_BUILD_ROOT%{_bindir}/starttde

#install pam configuration file
mkdir -p $RPM_BUILD_ROOT/etc/pam.d
install -p -m644 -D %{SOURCE14} $RPM_BUILD_ROOT/etc/pam.d/kscreensaver
install -p -m644 -D %{SOURCE14} $RPM_BUILD_ROOT/etc/pam.d/kcheckpass

cp -r %{SOURCE5} $RPM_BUILD_ROOT/usr/share/icons/crystalsvg/16x16/apps/
cp -r %{SOURCE6} $RPM_BUILD_ROOT/usr/share/icons/crystalsvg/16x16/apps/
cp -r %{SOURCE7} $RPM_BUILD_ROOT/usr/share/icons/crystalsvg/16x16/apps/
cp -r %{SOURCE8} $RPM_BUILD_ROOT/usr/share/icons/crystalsvg/16x16/apps/

# replace the panel's default background
rm -rf $RPM_BUILD_ROOT/usr/share/apps/kicker/wallpapers/default.png
cp %{SOURCE11} $RPM_BUILD_ROOT/usr/share/apps/kicker/wallpapers/default.png
%{SOURCE13}

# delete the sound theme's *.ogg files, leave the *.wav files, since ogg files are too slow to play!
rm -f %{buildroot}/usr/share/sounds/*.ogg

# the following content are provided by magic-artwork package
rm -rf %{buildroot}%{_datadir}/apps/kthememanager/themes/*
rm -rf %{buildroot}%{_datadir}/apps/ksplash/Themes
rm -rf %{buildroot}%{_datadir}/apps/kicker/pics/kside.png
rm -rf %{buildroot}%{_datadir}/apps/kicker/pics/kside_tile.png
rm -rf %{buildroot}%{_datadir}/apps/kdm/themes
rm -rf %{buildroot}%{_datadir}/wallpapers
# the following content are provided by magic-kde-config package
rm -rf %{buildroot}%{_datadir}/config


%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%post kate
/sbin/ldconfig

%postun kate 
/sbin/ldconfig

%post kmenuedit
/sbin/ldconfig

%postun kmenuedit
/sbin/ldconfig

%clean 
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files
%defattr(-,root,root)

%files devel
%defattr(-,root,root)
%{_includedir}/*

%files ksysguard
%defattr(-,root,root)
%_bindir/ksysguardd
%_bindir/ksysguard
%dir %_datadir/apps/ksysguard/
%_datadir/apps/ksysguard/*
%_datadir/applications/kde/ksysguard.desktop
%_datadir/apps/kicker/applets/ksysguardapplet.desktop
%_datadir/mimelnk/application/x-ksysguard.desktop
%_datadir/icons/crystalsvg/*x*/apps/ksysguard.png
#%doc %_docdir/HTML/en/ksysguard
%config(noreplace) %_sysconfdir/ksysguarddrc

%files konsole
%defattr(-,root,root)
%_bindir/konsole
%dir %_datadir/apps/konsole/
%_datadir/apps/konsole/*
%_datadir/applications/kde/konsole.desktop
%_datadir/applications/kde/konsolesu.desktop
%_datadir/applnk/.hidden/kcmkonsole.desktop
%_datadir/apps/kconf_update/konsole.upd
%_datadir/apps/kicker/menuext/konsolemenu.desktop
%_datadir/apps/konqueror/servicemenus/konsolehere.desktop
%_datadir/icons/hicolor/*x*/apps/konsole.png
%_datadir/icons/hicolor/scalable/apps/konsole.svgz
%_datadir/mimelnk/application/x-konsole.desktop
%_datadir/services/konsole*.desktop
%doc %_docdir/kde/HTML/en/kcontrol/kcmkonsole
%doc %_docdir/kde/HTML/en/konsole
%_libdir/libtdeinit_konsole.*
%_libdir/trinity/kcm_konsole.*
%_libdir/trinity/kickermenu_konsole.*
%_libdir/trinity/libkonsolepart.*
%_libdir/trinity/konsole.*

%files kdeprintfax
%defattr(-,root,root)
%_bindir/tdeprintfax
%dir %_datadir/apps/tdeprintfax
%_datadir/apps/tdeprintfax/*
%_datadir/applications/kde/tdeprintfax.desktop
%_datadir/icons/hicolor/*x*/apps/tdeprintfax.png

%files kate
%defattr(-,root,root)
%_bindir/kate
%doc %_docdir/kde/HTML/en/kate
%dir %_datadir/apps/kate/
%_datadir/apps/kate/*
%_datadir/applications/kde/kate.desktop
%_libdir/trinity/kate.*
%_libdir/libtdeinit_kate.*
%_libdir/libkateinterfaces.*
%_libdir/libkateutils.*
%_libdir/trinity/kickermenu_kate.*
%_datadir/apps/kconf_update/kate-2.4.upd
%_datadir/apps/kicker/menuext/katesessionmenu.desktop
#%_docdir/HTML/en/kdebase-apidocs/kate/html
%_datadir/icons/hicolor/*x*/apps/kate.png
%_datadir/icons/hicolor/scalable/apps/kate2.svgz
#%_mandir/man1/kate.1.gz
%_datadir/servicetypes/kateplugin.desktop

%files nsplugins
%defattr(-,root,root)
%_bindir/nspluginscan
%_bindir/nspluginviewer
%_datadir/applnk/Settings/WebBrowsing/nsplugin.desktop
%_datadir/apps/plugin/nspluginpart.rc
%_libdir/trinity/libnsplugin.*
%_libdir/trinity/kcm_nsplugins.*
%_docdir/kde/HTML/en/kcontrol/khtml/nsplugin.docbook

%files kmenuedit
%defattr(-,root,root)
%_bindir/kmenuedit
%doc %_docdir/kde/HTML/en/kmenuedit
%dir %_datadir/apps/kmenuedit/
%_datadir/apps/kmenuedit/*
%_datadir/applications/kde/kmenuedit.desktop
%_datadir/applnk/System/kmenuedit.desktop
%_datadir/icons/hicolor/*x*/apps/kmenuedit.png
%_libdir/trinity/kmenuedit.*
%_libdir/libtdeinit_kmenuedit.*

%files kdm
%defattr(-,root,root)
%_bindir/kdm
%_bindir/kdmctl
%_bindir/kdm_config
%_bindir/kdm_greet
%_bindir/krootimage
%_bindir/genkdmconf
%dir %_datadir/apps/kdm
%_datadir/apps/kdm/*
%dir %_docdir/kde/HTML/en/kcontrol/kdm
%_docdir/kde/HTML/en/kcontrol/kdm/*
%dir %_docdir/kde/HTML/en/kdm
%_docdir/kde/HTML/en/kdm/*
%_datadir/applications/kde/kdm.desktop
%_libdir/trinity/kgreet_winbind.*
%_libdir/trinity/kgreet_classic.*
%_libdir/trinity/kcm_kdm.*
%_datadir/icons/crystalsvg/*x*/apps/kdmconfig.png

%files core 
%defattr(-,root,root)
/etc/pam.d/kcheckpass
/etc/pam.d/kscreensaver
/etc/xdg/menus/*
%{_bindir}/appletproxy
%{_bindir}/drkonqi
%{_bindir}/extensionproxy
%{_bindir}/kaccess
%{_bindir}/kappfinder
%{_bindir}/kapplymousetheme
%{_bindir}/kasbar
%{_bindir}/kblankscrn.kss
%{_bindir}/kbookmarkmerger
%{_bindir}/kcheckpass
%{_bindir}/kcheckrunning
%{_bindir}/kcminit
%{_bindir}/kcminit_startup
%{_bindir}/kcontrol
%{_bindir}/kcontroledit
%{_bindir}/kdcop
#%{_bindir}/trinity
%{_bindir}/kdebugdialog
%{_bindir}/kdeeject
%{_bindir}/kdeinstallktheme
%{_bindir}/kdepasswd
%{_bindir}/kdesktop
%{_bindir}/kdesktop_lock
%{_bindir}/tdesu
%{_bindir}/tdesud
%{_bindir}/kdialog
%{_bindir}/keditbookmarks
%{_bindir}/keditfiletype
%{_bindir}/kfind
%{_bindir}/kfmclient
%{_bindir}/kfontinst
%{_bindir}/kfontview
%{_bindir}/khc_docbookdig.pl
%{_bindir}/khc_htdig.pl
%{_bindir}/khc_htsearch.pl
%{_bindir}/khc_indexbuilder
%{_bindir}/khc_mansearch.pl
%{_bindir}/khelpcenter
%{_bindir}/khotkeys
%{_bindir}/kicker
%{_bindir}/kinfocenter
%{_bindir}/kio_media_mounthelper
#%{_bindir}/kio_system_documenthelper
%{_bindir}/kjobviewer
%{_bindir}/klipper
%{_bindir}/klocaldomainurifilterhelper
%{_bindir}/knetattach
#%{_bindir}/kompmgr
%{_bindir}/konqueror
%{_bindir}/kpm
%{_bindir}/kprinter
%{_bindir}/krandom.kss
%{_bindir}/krandrtray
%{_bindir}/krdb
%{_bindir}/kreadconfig
%{_bindir}/ksmserver
%{_bindir}/ksplash
%{_bindir}/ksplashsimple
%{_bindir}/kstart
%{_bindir}/ksystraycmd
%{_bindir}/ktrash
%{_bindir}/kwebdesktop
%{_bindir}/twin
%{_bindir}/twin_killer_helper
%{_bindir}/twin_rules_dialog
%{_bindir}/kwrite
%{_bindir}/kwriteconfig
%{_bindir}/kxkb
%{_bindir}/starttde
%{_libdir}/kconf_update_bin/khotkeys_update
%{_libdir}/kconf_update_bin/kicker-3.4-reverseLayout
%{_libdir}/kconf_update_bin/twin_update_default_rules
%{_libdir}/kconf_update_bin/twin_update_window_settings
%{_libdir}/trinity/appletproxy.la
%{_libdir}/trinity/appletproxy.so
%{_libdir}/trinity/clock_panelapplet.la
%{_libdir}/trinity/clock_panelapplet.so
%{_libdir}/trinity/cursorthumbnail.la
%{_libdir}/trinity/cursorthumbnail.so
%{_libdir}/trinity/djvuthumbnail.la
%{_libdir}/trinity/djvuthumbnail.so
%{_libdir}/trinity/dockbar_panelextension.la
%{_libdir}/trinity/dockbar_panelextension.so
%{_libdir}/trinity/exrthumbnail.la
%{_libdir}/trinity/exrthumbnail.so
%{_libdir}/trinity/extensionproxy.la
%{_libdir}/trinity/extensionproxy.so
%{_libdir}/trinity/fontthumbnail.la
%{_libdir}/trinity/fontthumbnail.so
%{_libdir}/trinity/htmlthumbnail.la
%{_libdir}/trinity/htmlthumbnail.so
%{_libdir}/trinity/imagethumbnail.la
%{_libdir}/trinity/imagethumbnail.so
%{_libdir}/trinity/kaccess.la
%{_libdir}/trinity/kaccess.so
%{_libdir}/trinity/kasbar_panelextension.la
%{_libdir}/trinity/kasbar_panelextension.so
%{_libdir}/trinity/kcm_access.la
%{_libdir}/trinity/kcm_access.so
%{_libdir}/trinity/kcm_arts.la
%{_libdir}/trinity/kcm_arts.so
%{_libdir}/trinity/kcm_background.la
%{_libdir}/trinity/kcm_background.so
%{_libdir}/trinity/kcm_bell.la
%{_libdir}/trinity/kcm_bell.so
%{_libdir}/trinity/kcm_cgi.la
%{_libdir}/trinity/kcm_cgi.so
%{_libdir}/trinity/kcm_clock.la
%{_libdir}/trinity/kcm_clock.so
%{_libdir}/trinity/kcm_colors.la
%{_libdir}/trinity/kcm_colors.so
%{_libdir}/trinity/kcm_componentchooser.la
%{_libdir}/trinity/kcm_componentchooser.so
%{_libdir}/trinity/kcm_crypto.la
%{_libdir}/trinity/kcm_crypto.so
%{_libdir}/trinity/kcm_css.la
%{_libdir}/trinity/kcm_css.so
%{_libdir}/trinity/kcm_display.la
%{_libdir}/trinity/kcm_display.so
%{_libdir}/trinity/kcm_energy.la
%{_libdir}/trinity/kcm_energy.so
%{_libdir}/trinity/kcm_filetypes.la
%{_libdir}/trinity/kcm_filetypes.so
%{_libdir}/trinity/kcm_fontinst.la
%{_libdir}/trinity/kcm_fontinst.so
%{_libdir}/trinity/kcm_fonts.la
%{_libdir}/trinity/kcm_fonts.so
%{_libdir}/trinity/kcm_history.la
%{_libdir}/trinity/kcm_history.so
%{_libdir}/trinity/kcm_icons.la
%{_libdir}/trinity/kcm_icons.so
%{_libdir}/trinity/kcm_info.la
%{_libdir}/trinity/kcm_info.so
%{_libdir}/trinity/kcm_input.la
%{_libdir}/trinity/kcm_input.so
%{_libdir}/trinity/kcm_ioslaveinfo.la
%{_libdir}/trinity/kcm_ioslaveinfo.so
%{_libdir}/trinity/kcm_joystick.la
%{_libdir}/trinity/kcm_joystick.so
%{_libdir}/trinity/kcm_kded.la
%{_libdir}/trinity/kcm_kded.so
%{_libdir}/trinity/kcm_kdnssd.la
%{_libdir}/trinity/kcm_kdnssd.so
%{_libdir}/trinity/kcm_keyboard.la
%{_libdir}/trinity/kcm_keyboard.so
%{_libdir}/trinity/kcm_keys.la
%{_libdir}/trinity/kcm_keys.so
%{_libdir}/trinity/kcm_khotkeys.la
%{_libdir}/trinity/kcm_khotkeys.so
%{_libdir}/trinity/kcm_khotkeys_init.la
%{_libdir}/trinity/kcm_khotkeys_init.so
%{_libdir}/trinity/kcm_kicker.la
%{_libdir}/trinity/kcm_kicker.so
%{_libdir}/trinity/kcm_kio.la
%{_libdir}/trinity/kcm_kio.so
%{_libdir}/trinity/kcm_knotify.la
%{_libdir}/trinity/kcm_knotify.so
%{_libdir}/trinity/kcm_konq.la
%{_libdir}/trinity/kcm_konq.so
%{_libdir}/trinity/kcm_konqhtml.la
%{_libdir}/trinity/kcm_konqhtml.so
%{_libdir}/trinity/kcm_ksplashthemes.la
%{_libdir}/trinity/kcm_ksplashthemes.so
%{_libdir}/trinity/kcm_kthememanager.la
%{_libdir}/trinity/kcm_kthememanager.so
%{_libdir}/trinity/kcm_kurifilt.la
%{_libdir}/trinity/kcm_kurifilt.so
%{_libdir}/trinity/kcm_twindecoration.la
%{_libdir}/trinity/kcm_twindecoration.so
%{_libdir}/trinity/kcm_twinoptions.la
%{_libdir}/trinity/kcm_twinoptions.so
%{_libdir}/trinity/kcm_twinrules.la
%{_libdir}/trinity/kcm_twinrules.so
%{_libdir}/trinity/kcm_launch.la
%{_libdir}/trinity/kcm_launch.so
%{_libdir}/trinity/kcm_locale.la
%{_libdir}/trinity/kcm_locale.so
%{_libdir}/trinity/kcm_media.la
%{_libdir}/trinity/kcm_media.so
%{_libdir}/trinity/kcm_nic.la
%{_libdir}/trinity/kcm_nic.so
%{_libdir}/trinity/kcm_performance.la
%{_libdir}/trinity/kcm_performance.so
%{_libdir}/trinity/kcm_printmgr.la
%{_libdir}/trinity/kcm_printmgr.so
%{_libdir}/trinity/kcm_privacy.la
%{_libdir}/trinity/kcm_privacy.so
%{_libdir}/trinity/kcm_randr.la
%{_libdir}/trinity/kcm_randr.so
%{_libdir}/trinity/kcm_samba.la
%{_libdir}/trinity/kcm_samba.so
%{_libdir}/trinity/kcm_screensaver.la
%{_libdir}/trinity/kcm_screensaver.so
%{_libdir}/trinity/kcm_smserver.la
%{_libdir}/trinity/kcm_smserver.so
%{_libdir}/trinity/kcm_spellchecking.la
%{_libdir}/trinity/kcm_spellchecking.so
%{_libdir}/trinity/kcm_style.la
%{_libdir}/trinity/kcm_style.so
%{_libdir}/trinity/kcm_taskbar.la
%{_libdir}/trinity/kcm_taskbar.so
%{_libdir}/trinity/kcm_usb.la
%{_libdir}/trinity/kcm_usb.so
%{_libdir}/trinity/kcm_useraccount.la
%{_libdir}/trinity/kcm_useraccount.so
%{_libdir}/trinity/kcm_view1394.la
%{_libdir}/trinity/kcm_view1394.so
%{_libdir}/trinity/kcm_xinerama.la
%{_libdir}/trinity/kcm_xinerama.so
%{_libdir}/trinity/kcminit.la
%{_libdir}/trinity/kcminit.so
%{_libdir}/trinity/kcminit_startup.la
%{_libdir}/trinity/kcminit_startup.so
%{_libdir}/trinity/kcontrol.la
%{_libdir}/trinity/kcontrol.so
%{_libdir}/trinity/kcontroledit.la
%{_libdir}/trinity/kcontroledit.so
%{_libdir}/trinity/kded_favicons.la
%{_libdir}/trinity/kded_favicons.so
%{_libdir}/trinity/kded_homedirnotify.la
%{_libdir}/trinity/kded_homedirnotify.so
%{_libdir}/trinity/kded_khotkeys.la
%{_libdir}/trinity/kded_khotkeys.so
%{_libdir}/trinity/kded_konqy_preloader.la
%{_libdir}/trinity/kded_konqy_preloader.so
%{_libdir}/trinity/kded_kwrited.la
%{_libdir}/trinity/kded_kwrited.so
%{_libdir}/trinity/kded_mediamanager.la
%{_libdir}/trinity/kded_mediamanager.so
%{_libdir}/trinity/kded_medianotifier.la
%{_libdir}/trinity/kded_medianotifier.so
%{_libdir}/trinity/kded_remotedirnotify.la
%{_libdir}/trinity/kded_remotedirnotify.so
%{_libdir}/trinity/kded_systemdirnotify.la
%{_libdir}/trinity/kded_systemdirnotify.so
%{_libdir}/trinity/kdesktop.la
%{_libdir}/trinity/kdesktop.so
%{_libdir}/trinity/keditbookmarks.la
%{_libdir}/trinity/keditbookmarks.so
%{_libdir}/trinity/kfile_font.la
%{_libdir}/trinity/kfile_font.so
%{_libdir}/trinity/kfile_media.la
%{_libdir}/trinity/kfile_media.so
%{_libdir}/trinity/kfile_trash.la
%{_libdir}/trinity/kfile_trash.so
%{_libdir}/trinity/kfmclient.la
%{_libdir}/trinity/kfmclient.so
%{_libdir}/trinity/kgreet_classic.la
%{_libdir}/trinity/kgreet_classic.so
%{_libdir}/trinity/kgreet_winbind.la
%{_libdir}/trinity/kgreet_winbind.so
%{_libdir}/trinity/khelpcenter.la
%{_libdir}/trinity/khelpcenter.so
%{_libdir}/trinity/khotkeys.la
%{_libdir}/trinity/khotkeys.so
%{_libdir}/trinity/khotkeys_arts.la
%{_libdir}/trinity/khotkeys_arts.so
%{_libdir}/trinity/kicker.la
%{_libdir}/trinity/kicker.so
%{_libdir}/trinity/kickermenu_find.la
%{_libdir}/trinity/kickermenu_find.so
%{_libdir}/trinity/kickermenu_tdeprint.la
%{_libdir}/trinity/kickermenu_tdeprint.so
%{_libdir}/trinity/kickermenu_konqueror.la
%{_libdir}/trinity/kickermenu_konqueror.so
%{_libdir}/trinity/kickermenu_prefmenu.la
%{_libdir}/trinity/kickermenu_prefmenu.so
%{_libdir}/trinity/kickermenu_recentdocs.la
%{_libdir}/trinity/kickermenu_recentdocs.so
%{_libdir}/trinity/kickermenu_remotemenu.la
%{_libdir}/trinity/kickermenu_remotemenu.so
%{_libdir}/trinity/kickermenu_systemmenu.la
%{_libdir}/trinity/kickermenu_systemmenu.so
%{_libdir}/trinity/kio_about.la
%{_libdir}/trinity/kio_about.so
%{_libdir}/trinity/kio_cgi.la
%{_libdir}/trinity/kio_cgi.so
%{_libdir}/trinity/kio_filter.la
%{_libdir}/trinity/kio_filter.so
%{_libdir}/trinity/kio_finger.la
%{_libdir}/trinity/kio_finger.so
%{_libdir}/trinity/kio_fish.la
%{_libdir}/trinity/kio_fish.so
%{_libdir}/trinity/kio_floppy.la
%{_libdir}/trinity/kio_floppy.so
%{_libdir}/trinity/kio_fonts.la
%{_libdir}/trinity/kio_fonts.so
%{_libdir}/trinity/kio_home.la
%{_libdir}/trinity/kio_home.so
%{_libdir}/trinity/kio_info.la
%{_libdir}/trinity/kio_info.so
%{_libdir}/trinity/kio_ldap.la
%{_libdir}/trinity/kio_ldap.so
%{_libdir}/trinity/kio_mac.la
%{_libdir}/trinity/kio_mac.so
%{_libdir}/trinity/kio_man.la
%{_libdir}/trinity/kio_man.so
%{_libdir}/trinity/kio_media.la
%{_libdir}/trinity/kio_media.so
%{_libdir}/trinity/kio_nfs.la
%{_libdir}/trinity/kio_nfs.so
%{_libdir}/trinity/kio_nntp.la
%{_libdir}/trinity/kio_nntp.so
%{_libdir}/trinity/kio_pop3.la
%{_libdir}/trinity/kio_pop3.so
%{_libdir}/trinity/kio_print.la
%{_libdir}/trinity/kio_print.so
%{_libdir}/trinity/kio_remote.la
%{_libdir}/trinity/kio_remote.so
%{_libdir}/trinity/kio_settings.la
%{_libdir}/trinity/kio_settings.so
%{_libdir}/trinity/kio_sftp.la
%{_libdir}/trinity/kio_sftp.so
%{_libdir}/trinity/kio_smtp.la
%{_libdir}/trinity/kio_smtp.so
%{_libdir}/trinity/kio_system.la
%{_libdir}/trinity/kio_system.so
%{_libdir}/trinity/kio_tar.la
%{_libdir}/trinity/kio_tar.so
%{_libdir}/trinity/kio_thumbnail.la
%{_libdir}/trinity/kio_thumbnail.so
%{_libdir}/trinity/kio_trash.la
%{_libdir}/trinity/kio_trash.so
%{_libdir}/trinity/kjobviewer.la
%{_libdir}/trinity/kjobviewer.so
%{_libdir}/trinity/klipper.la
%{_libdir}/trinity/klipper.so
%{_libdir}/trinity/klipper_panelapplet.la
%{_libdir}/trinity/klipper_panelapplet.so
%{_libdir}/trinity/konq_aboutpage.la
%{_libdir}/trinity/konq_aboutpage.so
%{_libdir}/trinity/konq_iconview.la
%{_libdir}/trinity/konq_iconview.so
%{_libdir}/trinity/konq_listview.la
%{_libdir}/trinity/konq_listview.so
%{_libdir}/trinity/konq_remoteencoding.la
%{_libdir}/trinity/konq_remoteencoding.so
%{_libdir}/trinity/konq_shellcmdplugin.la
%{_libdir}/trinity/konq_shellcmdplugin.so
%{_libdir}/trinity/konq_sidebar.la
%{_libdir}/trinity/konq_sidebar.so
%{_libdir}/trinity/konq_sidebartree_bookmarks.la
%{_libdir}/trinity/konq_sidebartree_bookmarks.so
%{_libdir}/trinity/konq_sidebartree_dirtree.la
%{_libdir}/trinity/konq_sidebartree_dirtree.so
%{_libdir}/trinity/konq_sidebartree_history.la
%{_libdir}/trinity/konq_sidebartree_history.so
%{_libdir}/trinity/konq_sound.la
%{_libdir}/trinity/konq_sound.so
%{_libdir}/trinity/konqsidebar_tree.la
%{_libdir}/trinity/konqsidebar_tree.so
%{_libdir}/trinity/konqsidebar_web.la
%{_libdir}/trinity/konqsidebar_web.so
%{_libdir}/trinity/konqueror.la
%{_libdir}/trinity/konqueror.so
%{_libdir}/trinity/kprinter.la
%{_libdir}/trinity/kprinter.so
%{_libdir}/trinity/ksmserver.la
%{_libdir}/trinity/ksmserver.so
%{_libdir}/trinity/ksplashdefault.la
%{_libdir}/trinity/ksplashdefault.so
%{_libdir}/trinity/ksplashredmond.la
%{_libdir}/trinity/ksplashredmond.so
%{_libdir}/trinity/ksplashstandard.la
%{_libdir}/trinity/ksplashstandard.so
%{_libdir}/trinity/kstyle_keramik_config.la
%{_libdir}/trinity/kstyle_keramik_config.so
%{_libdir}/trinity/twin.la
%{_libdir}/trinity/twin.so
%{_libdir}/trinity/twin3_b2.la
%{_libdir}/trinity/twin3_b2.so
%{_libdir}/trinity/twin3_default.la
%{_libdir}/trinity/twin3_default.so
%{_libdir}/trinity/twin3_keramik.la
%{_libdir}/trinity/twin3_keramik.so
%{_libdir}/trinity/twin3_laptop.la
%{_libdir}/trinity/twin3_laptop.so
%{_libdir}/trinity/twin3_modernsys.la
%{_libdir}/trinity/twin3_modernsys.so
%{_libdir}/trinity/twin3_plastik.la
%{_libdir}/trinity/twin3_plastik.so
%{_libdir}/trinity/twin3_quartz.la
%{_libdir}/trinity/twin3_quartz.so
%{_libdir}/trinity/twin3_redmond.la
%{_libdir}/trinity/twin3_redmond.so
%{_libdir}/trinity/twin3_web.la
%{_libdir}/trinity/twin3_web.so
%{_libdir}/trinity/twin_b2_config.la
%{_libdir}/trinity/twin_b2_config.so
%{_libdir}/trinity/twin_default_config.la
%{_libdir}/trinity/twin_default_config.so
%{_libdir}/trinity/twin_keramik_config.la
%{_libdir}/trinity/twin_keramik_config.so
%{_libdir}/trinity/twin_modernsys_config.la
%{_libdir}/trinity/twin_modernsys_config.so
%{_libdir}/trinity/twin_plastik_config.la
%{_libdir}/trinity/twin_plastik_config.so
%{_libdir}/trinity/twin_quartz_config.la
%{_libdir}/trinity/twin_quartz_config.so
%{_libdir}/trinity/twin_rules_dialog.la
%{_libdir}/trinity/twin_rules_dialog.so
%{_libdir}/trinity/kwrite.la
%{_libdir}/trinity/kwrite.so
%{_libdir}/trinity/kxkb.la
%{_libdir}/trinity/kxkb.so
%{_libdir}/trinity/launcher_panelapplet.la
%{_libdir}/trinity/launcher_panelapplet.so
%{_libdir}/trinity/libtdeprint_part.la
%{_libdir}/trinity/libtdeprint_part.so
%{_libdir}/trinity/libkfindpart.la
%{_libdir}/trinity/libkfindpart.so
%{_libdir}/trinity/libkfontviewpart.la
%{_libdir}/trinity/libkfontviewpart.so
%{_libdir}/trinity/libkhtmlkttsdplugin.la
%{_libdir}/trinity/libkhtmlkttsdplugin.so
%{_libdir}/trinity/libkmanpart.la
%{_libdir}/trinity/libkmanpart.so
%{_libdir}/trinity/libkshorturifilter.la
%{_libdir}/trinity/libkshorturifilter.so
%{_libdir}/trinity/libkuriikwsfilter.la
%{_libdir}/trinity/libkuriikwsfilter.so
%{_libdir}/trinity/libkurisearchfilter.la
%{_libdir}/trinity/libkurisearchfilter.so
%{_libdir}/trinity/liblocaldomainurifilter.la
%{_libdir}/trinity/liblocaldomainurifilter.so
%{_libdir}/trinity/lockout_panelapplet.la
%{_libdir}/trinity/lockout_panelapplet.so
%{_libdir}/trinity/media_panelapplet.la
%{_libdir}/trinity/media_panelapplet.so
%{_libdir}/trinity/media_propsdlgplugin.la
%{_libdir}/trinity/media_propsdlgplugin.so
%{_libdir}/trinity/menu_panelapplet.la
%{_libdir}/trinity/menu_panelapplet.so
%{_libdir}/trinity/minipager_panelapplet.la
%{_libdir}/trinity/minipager_panelapplet.so
%{_libdir}/trinity/naughty_panelapplet.la
%{_libdir}/trinity/naughty_panelapplet.so
%{_libdir}/trinity/run_panelapplet.la
%{_libdir}/trinity/run_panelapplet.so
%{_libdir}/trinity/sidebar_panelextension.la
%{_libdir}/trinity/sidebar_panelextension.so
%{_libdir}/trinity/sysguard_panelapplet.la
%{_libdir}/trinity/sysguard_panelapplet.so
%{_libdir}/trinity/systemtray_panelapplet.la
%{_libdir}/trinity/systemtray_panelapplet.so
%{_libdir}/trinity/taskbar_panelapplet.la
%{_libdir}/trinity/taskbar_panelapplet.so
%{_libdir}/trinity/taskbar_panelextension.la
%{_libdir}/trinity/taskbar_panelextension.so
%{_libdir}/trinity/textthumbnail.la
%{_libdir}/trinity/textthumbnail.so
%{_libdir}/trinity/trash_panelapplet.la
%{_libdir}/trinity/trash_panelapplet.so
%{_libdir}/libkasbar.la
%{_libdir}/libkasbar.so
%{_libdir}/libkasbar.so.1
%{_libdir}/libkasbar.so.1.0.0
%{_libdir}/libtdecorations.la
%{_libdir}/libtdecorations.so
%{_libdir}/libtdecorations.so.1
%{_libdir}/libtdecorations.so.1.0.0
%{_libdir}/libtdeinit_appletproxy.la
%{_libdir}/libtdeinit_appletproxy.so
%{_libdir}/libtdeinit_extensionproxy.la
%{_libdir}/libtdeinit_extensionproxy.so
%{_libdir}/libtdeinit_kaccess.la
%{_libdir}/libtdeinit_kaccess.so
%{_libdir}/libtdeinit_kcminit.la
%{_libdir}/libtdeinit_kcminit.so
%{_libdir}/libtdeinit_kcminit_startup.la
%{_libdir}/libtdeinit_kcminit_startup.so
%{_libdir}/libtdeinit_kcontrol.la
%{_libdir}/libtdeinit_kcontrol.so
%{_libdir}/libtdeinit_kcontroledit.la
%{_libdir}/libtdeinit_kcontroledit.so
%{_libdir}/libtdeinit_kdesktop.la
%{_libdir}/libtdeinit_kdesktop.so
%{_libdir}/libtdeinit_keditbookmarks.la
%{_libdir}/libtdeinit_keditbookmarks.so
%{_libdir}/libtdeinit_kfmclient.la
%{_libdir}/libtdeinit_kfmclient.so
%{_libdir}/libtdeinit_khelpcenter.la
%{_libdir}/libtdeinit_khelpcenter.so
%{_libdir}/libtdeinit_khotkeys.la
%{_libdir}/libtdeinit_khotkeys.so
%{_libdir}/libtdeinit_kicker.la
%{_libdir}/libtdeinit_kicker.so
%{_libdir}/libtdeinit_kjobviewer.la
%{_libdir}/libtdeinit_kjobviewer.so
%{_libdir}/libtdeinit_klipper.la
%{_libdir}/libtdeinit_klipper.so
%{_libdir}/libtdeinit_konqueror.la
%{_libdir}/libtdeinit_konqueror.so
%{_libdir}/libtdeinit_kprinter.la
%{_libdir}/libtdeinit_kprinter.so
%{_libdir}/libtdeinit_ksmserver.la
%{_libdir}/libtdeinit_ksmserver.so
%{_libdir}/libtdeinit_twin.la
%{_libdir}/libtdeinit_twin.so
%{_libdir}/libtdeinit_twin_rules_dialog.la
%{_libdir}/libtdeinit_twin_rules_dialog.so
%{_libdir}/libtdeinit_kwrite.la
%{_libdir}/libtdeinit_kwrite.so
%{_libdir}/libtdeinit_kxkb.la
%{_libdir}/libtdeinit_kxkb.so
%{_libdir}/libkfontinst.la
%{_libdir}/libkfontinst.so
%{_libdir}/libkfontinst.so.0
%{_libdir}/libkfontinst.so.0.0.0
%{_libdir}/libkhotkeys_shared.la
%{_libdir}/libkhotkeys_shared.so
%{_libdir}/libkhotkeys_shared.so.1
%{_libdir}/libkhotkeys_shared.so.1.0.0
%{_libdir}/libkickermain.la
%{_libdir}/libkickermain.so
%{_libdir}/libkickermain.so.1
%{_libdir}/libkickermain.so.1.0.0
%{_libdir}/libkonq.la
%{_libdir}/libkonq.so
%{_libdir}/libkonq.so.4
%{_libdir}/libkonq.so.4.2.0
%{_libdir}/libkonqsidebarplugin.la
%{_libdir}/libkonqsidebarplugin.so
%{_libdir}/libkonqsidebarplugin.so.1
%{_libdir}/libkonqsidebarplugin.so.1.2.0
%{_libdir}/libksgrd.la
%{_libdir}/libksgrd.so
%{_libdir}/libksgrd.so.1
%{_libdir}/libksgrd.so.1.2.0
%{_libdir}/libksplashthemes.la
%{_libdir}/libksplashthemes.so
%{_libdir}/libksplashthemes.so.0
%{_libdir}/libksplashthemes.so.0.0.0
%{_libdir}/libtaskbar.la
%{_libdir}/libtaskbar.so
%{_libdir}/libtaskbar.so.1
%{_libdir}/libtaskbar.so.1.2.0
%{_libdir}/libtaskmanager.la
%{_libdir}/libtaskmanager.so
%{_libdir}/libtaskmanager.so.1
%{_libdir}/libtaskmanager.so.1.0.0
%{_datadir}/applications/kde/Help.desktop
%{_datadir}/applications/kde/Home.desktop
%{_datadir}/applications/kde/KControl.desktop
%{_datadir}/applications/kde/Kfind.desktop
%{_datadir}/applications/kde/arts.desktop
%{_datadir}/applications/kde/background.desktop
%{_datadir}/applications/kde/bell.desktop
%{_datadir}/applications/kde/cache.desktop
%{_datadir}/applications/kde/cdinfo.desktop
%{_datadir}/applications/kde/clock.desktop
%{_datadir}/applications/kde/colors.desktop
%{_datadir}/applications/kde/componentchooser.desktop
%{_datadir}/applications/kde/cookies.desktop
%{_datadir}/applications/kde/crypto.desktop
%{_datadir}/applications/kde/desktop.desktop
%{_datadir}/applications/kde/desktopbehavior.desktop
%{_datadir}/applications/kde/desktoppath.desktop
%{_datadir}/applications/kde/devices.desktop
%{_datadir}/applications/kde/display.desktop
%{_datadir}/applications/kde/dma.desktop
%{_datadir}/applications/kde/ebrowsing.desktop
%{_datadir}/applications/kde/filebrowser.desktop
%{_datadir}/applications/kde/filetypes.desktop
%{_datadir}/applications/kde/fonts.desktop
%{_datadir}/applications/kde/icons.desktop
%{_datadir}/applications/kde/installktheme.desktop
%{_datadir}/applications/kde/interrupts.desktop
%{_datadir}/applications/kde/ioports.desktop
%{_datadir}/applications/kde/ioslaveinfo.desktop
%{_datadir}/applications/kde/joystick.desktop
%{_datadir}/applications/kde/kappfinder.desktop
%{_datadir}/applications/kde/kcm_kdnssd.desktop
%{_datadir}/applications/kde/kcm_useraccount.desktop
%{_datadir}/applications/kde/kcmaccess.desktop
%{_datadir}/applications/kde/kcmcgi.desktop
%{_datadir}/applications/kde/kcmcss.desktop
%{_datadir}/applications/kde/kcmfontinst.desktop
%{_datadir}/applications/kde/kcmhistory.desktop
%{_datadir}/applications/kde/kcmkded.desktop
%{_datadir}/applications/kde/kcmkicker.desktop
%{_datadir}/applications/kde/kcmlaunch.desktop
%{_datadir}/applications/kde/kcmnotify.desktop
%{_datadir}/applications/kde/kcmperformance.desktop
%{_datadir}/applications/kde/kcmsmserver.desktop
%{_datadir}/applications/kde/kcmtaskbar.desktop
%{_datadir}/applications/kde/kcmusb.desktop
%{_datadir}/applications/kde/kcmview1394.desktop
%{_datadir}/applications/kde/kdepasswd.desktop
%{_datadir}/applications/kde/keyboard.desktop
%{_datadir}/applications/kde/keyboard_layout.desktop
%{_datadir}/applications/kde/keys.desktop
%{_datadir}/applications/kde/kfmclient.desktop
%{_datadir}/applications/kde/kfmclient_dir.desktop
%{_datadir}/applications/kde/kfmclient_html.desktop
%{_datadir}/applications/kde/kfmclient_war.desktop
%{_datadir}/applications/kde/kfontview.desktop
%{_datadir}/applications/kde/khotkeys.desktop
%{_datadir}/applications/kde/khtml_behavior.desktop
%{_datadir}/applications/kde/khtml_filter.desktop
%{_datadir}/applications/kde/khtml_fonts.desktop
%{_datadir}/applications/kde/khtml_java_js.desktop
%{_datadir}/applications/kde/khtml_plugins.desktop
%{_datadir}/applications/kde/kinfocenter.desktop
%{_datadir}/applications/kde/kjobviewer.desktop
%{_datadir}/applications/kde/klipper.desktop
%{_datadir}/applications/kde/knetattach.desktop
%{_datadir}/applications/kde/konqbrowser.desktop
%{_datadir}/applications/kde/konquerorsu.desktop
%{_datadir}/applications/kde/krandrtray.desktop
%{_datadir}/applications/kde/ksplashthememgr.desktop
%{_datadir}/applications/kde/kthememanager.desktop
%{_datadir}/applications/kde/twindecoration.desktop
%{_datadir}/applications/kde/twinoptions.desktop
%{_datadir}/applications/kde/twinrules.desktop
%{_datadir}/applications/kde/kwrite.desktop
%{_datadir}/applications/kde/lanbrowser.desktop
%{_datadir}/applications/kde/language.desktop
%{_datadir}/applications/kde/media.desktop
%{_datadir}/applications/kde/memory.desktop
%{_datadir}/applications/kde/mouse.desktop
%{_datadir}/applications/kde/netpref.desktop
%{_datadir}/applications/kde/nic.desktop
%{_datadir}/applications/kde/opengl.desktop
%{_datadir}/applications/kde/panel.desktop
%{_datadir}/applications/kde/panel_appearance.desktop
%{_datadir}/applications/kde/partitions.desktop
%{_datadir}/applications/kde/pci.desktop
%{_datadir}/applications/kde/printers.desktop
%{_datadir}/applications/kde/privacy.desktop
%{_datadir}/applications/kde/processor.desktop
%{_datadir}/applications/kde/proxy.desktop
%{_datadir}/applications/kde/screensaver.desktop
%{_datadir}/applications/kde/scsi.desktop
%{_datadir}/applications/kde/smbstatus.desktop
%{_datadir}/applications/kde/sound.desktop
%{_datadir}/applications/kde/spellchecking.desktop
%{_datadir}/applications/kde/style.desktop
%{_datadir}/applications/kde/useragent.desktop
%{_datadir}/applications/kde/xserver.desktop
%{_datadir}/applnk/.hidden/.directory
%{_datadir}/applnk/.hidden/battery.desktop
%{_datadir}/applnk/.hidden/bwarning.desktop
%{_datadir}/applnk/.hidden/cwarning.desktop
%{_datadir}/applnk/.hidden/email.desktop
%{_datadir}/applnk/.hidden/energy.desktop
%{_datadir}/applnk/.hidden/fileappearance.desktop
%{_datadir}/applnk/.hidden/filebehavior.desktop
%{_datadir}/applnk/.hidden/filepreviews.desktop
%{_datadir}/applnk/.hidden/kcmkonq.desktop
%{_datadir}/applnk/.hidden/kcmkonqyperformance.desktop
%{_datadir}/applnk/.hidden/kcmkxmlrpcd.desktop
%{_datadir}/applnk/.hidden/kicker_config.desktop
%{_datadir}/applnk/.hidden/kicker_config_appearance.desktop
%{_datadir}/applnk/.hidden/kicker_config_arrangement.desktop
%{_datadir}/applnk/.hidden/kicker_config_hiding.desktop
%{_datadir}/applnk/.hidden/kicker_config_menus.desktop
%{_datadir}/applnk/.hidden/konqfilemgr.desktop
%{_datadir}/applnk/.hidden/konqhtml.desktop
%{_datadir}/applnk/.hidden/twinactions.desktop
%{_datadir}/applnk/.hidden/twinadvanced.desktop
%{_datadir}/applnk/.hidden/twinfocus.desktop
%{_datadir}/applnk/.hidden/twinmoving.desktop
%{_datadir}/applnk/.hidden/twintranslucency.desktop
%{_datadir}/applnk/.hidden/passwords.desktop
%{_datadir}/applnk/.hidden/power.desktop
%{_datadir}/applnk/.hidden/randr.desktop
%{_datadir}/applnk/.hidden/smb.desktop
%{_datadir}/applnk/.hidden/socks.desktop
%{_datadir}/applnk/.hidden/userinfo.desktop
%{_datadir}/applnk/.hidden/virtualdesktops.desktop
%{_datadir}/applnk/.hidden/xinerama.desktop
%{_datadir}/applnk/Internet/keditbookmarks.desktop
%{_datadir}/applnk/Settings/LookNFeel/Themes/iconthemes.desktop
%{_datadir}/applnk/Settings/LookNFeel/kcmtaskbar.desktop
%{_datadir}/applnk/Settings/LookNFeel/panel.desktop
%{_datadir}/applnk/Settings/LookNFeel/panel_appearance.desktop
%{_datadir}/applnk/Settings/WebBrowsing/khtml_appearance.desktop
%{_datadir}/applnk/Settings/WebBrowsing/smb.desktop
%{_datadir}/applnk/System/ScreenSavers/KBlankscreen.desktop
%{_datadir}/applnk/System/ScreenSavers/KRandom.desktop
%{_datadir}/applnk/System/kappfinder.desktop
%{_datadir}/applnk/konqueror.desktop
%{_datadir}/apps/clockapplet/*
%{_datadir}/apps/drkonqi/*
%{_datadir}/apps/kaccess/eventsrc
%{_datadir}/apps/kappfinder/*
%{_datadir}/apps/kbookmark/directory_bookmarkbar.desktop
%{_datadir}/apps/kcm_componentchooser/*
%{_datadir}/apps/kcmcss/*
%{_datadir}/apps/kcminput/*
%{_datadir}/apps/kcmkeys/*
%{_datadir}/apps/kcmlocale/pics/background.png
#%{_datadir}/apps/kcmusb/usb.ids
%{_datadir}/apps/kcmview1394/oui.db
%{_datadir}/apps/kconf_update/*
%{_datadir}/apps/kcontrol/*
%{_datadir}/apps/kcontroledit/*
%{_datadir}/apps/kdcop/*
%{_datadir}/apps/tdeprint/*
%{_datadir}/apps/tdeprint_part/tdeprint_part.rc
%{_datadir}/apps/kdesktop/*
%{_datadir}/apps/kdisplay/*
%{_datadir}/apps/keditbookmarks/*
%{_datadir}/apps/kfindpart/*
%{_datadir}/apps/kfontview/*
%{_datadir}/apps/khelpcenter/*
%{_datadir}/apps/khotkeys/*
%{_datadir}/apps/khtml/*
%{_datadir}/apps/kicker/*
%{_datadir}/apps/kinfocenter/kinfocenterui.rc
%{_datadir}/apps/kio_finger/kio_finger.css
%{_datadir}/apps/kio_finger/kio_finger.pl
%{_datadir}/apps/kio_info/kde-info2html
%{_datadir}/apps/kio_info/kde-info2html.conf
%{_datadir}/apps/kio_man/kio_man.css
%{_datadir}/apps/kjobviewer/kjobviewerui.rc
%{_datadir}/apps/konqiconview/*
%{_datadir}/apps/konqlistview/*
%{_datadir}/apps/konqsidebartng/*
%{_datadir}/apps/konqueror/*
%{_datadir}/apps/ksmserver/pics/shutdownkonq.png
%{_datadir}/apps/ksplash/pics/splash.png
%{_datadir}/apps/kthememanager/themes
%{_datadir}/apps/twin/*
%{_datadir}/apps/kwrite/kwriteui.rc
%{_datadir}/apps/naughtyapplet/pics/*.png
%{_datadir}/apps/plugin
%{_datadir}/apps/systemview/*.desktop
%{_datadir}/autostart/*.desktop
%{_datadir}/config.kcfg/*.kcfg
%{_datadir}/desktop-directories/*
%{_datadir}/doc/kde/HTML/en/kcontrol/*
%{_datadir}/doc/kde/HTML/en/kdcop/*
#%{_datadir}/doc/HTML/en/kdebase-apidocs/*
%{_datadir}/doc/kde/HTML/en/kdebugdialog/*
%{_datadir}/doc/kde/HTML/en/tdeprint/*
%{_datadir}/doc/kde/HTML/en/tdesu/*
%{_datadir}/doc/kde/HTML/en/kfind/*
%{_datadir}/doc/kde/HTML/en/khelpcenter/*
%{_datadir}/doc/kde/HTML/en/kicker/*
%{_datadir}/doc/kde/HTML/en/kinfocenter/*
%{_datadir}/doc/kde/HTML/en/kioslave/*
%{_datadir}/doc/kde/HTML/en/klipper/*
%{_datadir}/doc/kde/HTML/en/knetattach/*
%{_datadir}/doc/kde/HTML/en/kompmgr/*
%{_datadir}/doc/kde/HTML/en/konqueror/*
%{_datadir}/doc/kde/HTML/en/kpager/*
%{_datadir}/doc/kde/HTML/en/ksplashml/*
%{_datadir}/doc/kde/HTML/en/kwrite/*
%{_datadir}/doc/kde/HTML/en/kxkb/*
#%{_datadir}/fonts/override/fonts.dir
%{_datadir}/icons/crystalsvg/128x128/apps/access.png
%{_datadir}/icons/crystalsvg/128x128/apps/acroread.png
%{_datadir}/icons/crystalsvg/128x128/apps/applixware.png
%{_datadir}/icons/crystalsvg/128x128/apps/arts.png
%{_datadir}/icons/crystalsvg/128x128/apps/background.png
%{_datadir}/icons/crystalsvg/128x128/apps/bell.png
%{_datadir}/icons/crystalsvg/128x128/apps/cache.png
%{_datadir}/icons/crystalsvg/128x128/apps/clanbomber.png
%{_datadir}/icons/crystalsvg/128x128/apps/clock.png
%{_datadir}/icons/crystalsvg/128x128/apps/colors.png
%{_datadir}/icons/crystalsvg/128x128/apps/date.png
%{_datadir}/icons/crystalsvg/128x128/apps/email.png
%{_datadir}/icons/crystalsvg/128x128/apps/energy.png
%{_datadir}/icons/crystalsvg/128x128/apps/energy_star.png
%{_datadir}/icons/crystalsvg/128x128/apps/filetypes.png
%{_datadir}/icons/crystalsvg/128x128/apps/fonts.png
%{_datadir}/icons/crystalsvg/128x128/apps/gimp.png
%{_datadir}/icons/crystalsvg/128x128/apps/help_index.png
%{_datadir}/icons/crystalsvg/128x128/apps/hwinfo.png
%{_datadir}/icons/crystalsvg/128x128/apps/kcmdevices.png
%{_datadir}/icons/crystalsvg/128x128/apps/kcmdf.png
%{_datadir}/icons/crystalsvg/128x128/apps/kcmkwm.png
%{_datadir}/icons/crystalsvg/128x128/apps/kcmmemory.png
%{_datadir}/icons/crystalsvg/128x128/apps/kcmpartitions.png
%{_datadir}/icons/crystalsvg/128x128/apps/kcmpci.png
%{_datadir}/icons/crystalsvg/128x128/apps/kcontrol.png
%{_datadir}/icons/crystalsvg/128x128/apps/key_bindings.png
%{_datadir}/icons/crystalsvg/128x128/apps/kfm_home.png
%{_datadir}/icons/crystalsvg/128x128/apps/kscreensaver.png
%{_datadir}/icons/crystalsvg/128x128/apps/kthememgr.png
%{_datadir}/icons/crystalsvg/128x128/apps/licq.png
%{_datadir}/icons/crystalsvg/128x128/apps/linuxconf.png
%{_datadir}/icons/crystalsvg/128x128/apps/locale.png
%{_datadir}/icons/crystalsvg/128x128/apps/looknfeel.png
%{_datadir}/icons/crystalsvg/128x128/apps/multimedia.png
%{_datadir}/icons/crystalsvg/128x128/apps/netscape.png
%{_datadir}/icons/crystalsvg/128x128/apps/package.png
%{_datadir}/icons/crystalsvg/128x128/apps/package_applications.png
%{_datadir}/icons/crystalsvg/128x128/apps/package_development.png
%{_datadir}/icons/crystalsvg/128x128/apps/package_favourite.png
%{_datadir}/icons/crystalsvg/128x128/apps/package_games.png
%{_datadir}/icons/crystalsvg/128x128/apps/package_multimedia.png
%{_datadir}/icons/crystalsvg/128x128/apps/package_network.png
%{_datadir}/icons/crystalsvg/128x128/apps/package_settings.png
%{_datadir}/icons/crystalsvg/128x128/apps/package_toys.png
%{_datadir}/icons/crystalsvg/128x128/apps/package_utilities.png
%{_datadir}/icons/crystalsvg/128x128/apps/penguin.png
%{_datadir}/icons/crystalsvg/128x128/apps/personal.png
%{_datadir}/icons/crystalsvg/128x128/apps/phppg.png
%{_datadir}/icons/crystalsvg/128x128/apps/proxy.png
%{_datadir}/icons/crystalsvg/128x128/apps/pysol.png
%{_datadir}/icons/crystalsvg/128x128/apps/randr.png
%{_datadir}/icons/crystalsvg/128x128/apps/samba.png
%{_datadir}/icons/crystalsvg/128x128/apps/staroffice.png
%{_datadir}/icons/crystalsvg/128x128/apps/stylesheet.png
%{_datadir}/icons/crystalsvg/128x128/apps/systemtray.png
%{_datadir}/icons/crystalsvg/128x128/apps/taskbar.png
%{_datadir}/icons/crystalsvg/128x128/apps/terminal.png
%{_datadir}/icons/crystalsvg/128x128/apps/tux.png
%{_datadir}/icons/crystalsvg/128x128/apps/wp.png
%{_datadir}/icons/crystalsvg/128x128/apps/xclock.png
%{_datadir}/icons/crystalsvg/128x128/apps/xfmail.png
%{_datadir}/icons/crystalsvg/128x128/apps/xmag.png
%{_datadir}/icons/crystalsvg/128x128/devices/laptop.png
%{_datadir}/icons/crystalsvg/16x16/actions/newfont.png
%{_datadir}/icons/crystalsvg/16x16/apps/abiword.png
%{_datadir}/icons/crystalsvg/16x16/apps/access.png
%{_datadir}/icons/crystalsvg/16x16/apps/acroread.png
%{_datadir}/icons/crystalsvg/16x16/apps/agent.png
%{_datadir}/icons/crystalsvg/16x16/apps/alevt.png
%{_datadir}/icons/crystalsvg/16x16/apps/applixware.png
%{_datadir}/icons/crystalsvg/16x16/apps/arts.png
%{_datadir}/icons/crystalsvg/16x16/apps/assistant.png
%{_datadir}/icons/crystalsvg/16x16/apps/background.png
%{_datadir}/icons/crystalsvg/16x16/apps/bell.png
%{_datadir}/icons/crystalsvg/16x16/apps/blender.png
%{_datadir}/icons/crystalsvg/16x16/apps/bluefish.png
%{_datadir}/icons/crystalsvg/16x16/apps/cache.png
%{_datadir}/icons/crystalsvg/16x16/apps/calendars.png
%{_datadir}/icons/crystalsvg/16x16/apps/clanbomber.png
%{_datadir}/icons/crystalsvg/16x16/apps/clock.png
%{_datadir}/icons/crystalsvg/16x16/apps/colors.png
%{_datadir}/icons/crystalsvg/16x16/apps/cookie.png
%{_datadir}/icons/crystalsvg/16x16/apps/date.png
%{_datadir}/icons/crystalsvg/16x16/apps/designer.png
%{_datadir}/icons/crystalsvg/16x16/apps/dia.png
%{_datadir}/icons/crystalsvg/16x16/apps/dlgedit.png
%{_datadir}/icons/crystalsvg/16x16/apps/eclipse.png
%{_datadir}/icons/crystalsvg/16x16/apps/edu_languages.png
%{_datadir}/icons/crystalsvg/16x16/apps/edu_mathematics.png
%{_datadir}/icons/crystalsvg/16x16/apps/edu_miscellaneous.png
%{_datadir}/icons/crystalsvg/16x16/apps/edu_science.png
%{_datadir}/icons/crystalsvg/16x16/apps/emacs.png
%{_datadir}/icons/crystalsvg/16x16/apps/email.png
%{_datadir}/icons/crystalsvg/16x16/apps/energy.png
%{_datadir}/icons/crystalsvg/16x16/apps/energy_star.png
%{_datadir}/icons/crystalsvg/16x16/apps/enhanced_browsing.png
%{_datadir}/icons/crystalsvg/16x16/apps/evolution.png
%{_datadir}/icons/crystalsvg/16x16/apps/fifteenpieces.png
%{_datadir}/icons/crystalsvg/16x16/apps/filetypes.png
%{_datadir}/icons/crystalsvg/16x16/apps/fonts.png
%{_datadir}/icons/crystalsvg/16x16/apps/gabber.png
%{_datadir}/icons/crystalsvg/16x16/apps/gaim.png
%{_datadir}/icons/crystalsvg/16x16/apps/gimp.png
%{_datadir}/icons/crystalsvg/16x16/apps/gnome_apps.png
%{_datadir}/icons/crystalsvg/16x16/apps/gnomemeeting.png
%{_datadir}/icons/crystalsvg/16x16/apps/gnucash.png
%{_datadir}/icons/crystalsvg/16x16/apps/gnumeric.png
%{_datadir}/icons/crystalsvg/16x16/apps/gv.png
%{_datadir}/icons/crystalsvg/16x16/apps/gvim.png
%{_datadir}/icons/crystalsvg/16x16/apps/help_index.png
%{_datadir}/icons/crystalsvg/16x16/apps/hwinfo.png
%{_datadir}/icons/crystalsvg/16x16/apps/icons.png
%{_datadir}/icons/crystalsvg/16x16/apps/iconthemes.png
%{_datadir}/icons/crystalsvg/16x16/apps/ieee1394.png
%{_datadir}/icons/crystalsvg/16x16/apps/input_devices_settings.png
%{_datadir}/icons/crystalsvg/16x16/apps/kbinaryclock.png
%{_datadir}/icons/crystalsvg/16x16/apps/kcmdevices.png
%{_datadir}/icons/crystalsvg/16x16/apps/kcmkicker.png
%{_datadir}/icons/crystalsvg/16x16/apps/kcmkwm.png
%{_datadir}/icons/crystalsvg/16x16/apps/kcmmemory.png
%{_datadir}/icons/crystalsvg/16x16/apps/kcmmidi.png
%{_datadir}/icons/crystalsvg/16x16/apps/kcmpartitions.png
%{_datadir}/icons/crystalsvg/16x16/apps/kcmpci.png
%{_datadir}/icons/crystalsvg/16x16/apps/kcmprocessor.png
%{_datadir}/icons/crystalsvg/16x16/apps/kcmscsi.png
%{_datadir}/icons/crystalsvg/16x16/apps/kcmsound.png
%{_datadir}/icons/crystalsvg/16x16/apps/kcmsystem.png
%{_datadir}/icons/crystalsvg/16x16/apps/kcmx.png
%{_datadir}/icons/crystalsvg/16x16/apps/kcontrol.png
%{_datadir}/icons/crystalsvg/16x16/apps/kded.png
%{_datadir}/icons/crystalsvg/16x16/apps/kdisknav.png
%{_datadir}/icons/crystalsvg/16x16/apps/keditbookmarks.png
%{_datadir}/icons/crystalsvg/16x16/apps/key_bindings.png
%{_datadir}/icons/crystalsvg/16x16/apps/keyboard.png
%{_datadir}/icons/crystalsvg/16x16/apps/keyboard_layout.png
%{_datadir}/icons/crystalsvg/16x16/apps/kfm_home.png
%{_datadir}/icons/crystalsvg/16x16/apps/kicker.png
%{_datadir}/icons/crystalsvg/16x16/apps/knotify.png
%{_datadir}/icons/crystalsvg/16x16/apps/kscreensaver.png
%{_datadir}/icons/crystalsvg/16x16/apps/kthememgr.png
%{_datadir}/icons/crystalsvg/16x16/apps/kvirc.png
%{_datadir}/icons/crystalsvg/16x16/apps/twin.png
%{_datadir}/icons/crystalsvg/16x16/apps/licq.png
%{_datadir}/icons/crystalsvg/16x16/apps/linguist.png
%{_datadir}/icons/crystalsvg/16x16/apps/linuxconf.png
%{_datadir}/icons/crystalsvg/16x16/apps/locale.png
%{_datadir}/icons/crystalsvg/16x16/apps/looknfeel.png
%{_datadir}/icons/crystalsvg/16x16/apps/lyx.png
%{_datadir}/icons/crystalsvg/16x16/apps/mac.png
%{_datadir}/icons/crystalsvg/16x16/apps/mathematica.png
%{_datadir}/icons/crystalsvg/16x16/apps/multimedia.png
%{_datadir}/icons/crystalsvg/16x16/apps/nedit.png
%{_datadir}/icons/crystalsvg/16x16/apps/netscape.png
%{_datadir}/icons/crystalsvg/16x16/apps/opera.png
%{_datadir}/icons/crystalsvg/16x16/apps/package.png
%{_datadir}/icons/crystalsvg/16x16/apps/package_application.png
%{_datadir}/icons/crystalsvg/16x16/apps/package_applications.png
%{_datadir}/icons/crystalsvg/16x16/apps/package_development.png
%{_datadir}/icons/crystalsvg/16x16/apps/package_editors.png
%{_datadir}/icons/crystalsvg/16x16/apps/package_edutainment.png
%{_datadir}/icons/crystalsvg/16x16/apps/package_favourite.png
%{_datadir}/icons/crystalsvg/16x16/apps/package_games.png
%{_datadir}/icons/crystalsvg/16x16/apps/package_games_arcade.png
%{_datadir}/icons/crystalsvg/16x16/apps/package_games_board.png
%{_datadir}/icons/crystalsvg/16x16/apps/package_games_card.png
%{_datadir}/icons/crystalsvg/16x16/apps/package_games_strategy.png
%{_datadir}/icons/crystalsvg/16x16/apps/package_graphics.png
%{_datadir}/icons/crystalsvg/16x16/apps/package_multimedia.png
%{_datadir}/icons/crystalsvg/16x16/apps/package_network.png
%{_datadir}/icons/crystalsvg/16x16/apps/package_settings.png
%{_datadir}/icons/crystalsvg/16x16/apps/package_system.png
%{_datadir}/icons/crystalsvg/16x16/apps/package_toys.png
%{_datadir}/icons/crystalsvg/16x16/apps/package_utilities.png
%{_datadir}/icons/crystalsvg/16x16/apps/package_wordprocessing.png
%{_datadir}/icons/crystalsvg/16x16/apps/pan.png
%{_datadir}/icons/crystalsvg/16x16/apps/panel.png
%{_datadir}/icons/crystalsvg/16x16/apps/panel_settings.png
%{_datadir}/icons/crystalsvg/16x16/apps/penguin.png
%{_datadir}/icons/crystalsvg/16x16/apps/personal.png
%{_datadir}/icons/crystalsvg/16x16/apps/phppg.png
%{_datadir}/icons/crystalsvg/16x16/apps/plan.png
%{_datadir}/icons/crystalsvg/16x16/apps/planner.png
%{_datadir}/icons/crystalsvg/16x16/apps/proxy.png
%{_datadir}/icons/crystalsvg/16x16/apps/pybliographic.png
%{_datadir}/icons/crystalsvg/16x16/apps/randr.png
%{_datadir}/icons/crystalsvg/16x16/apps/realplayer.png
%{_datadir}/icons/crystalsvg/16x16/apps/remote.png
%{_datadir}/icons/crystalsvg/16x16/apps/runprocesscatcher.png
%{_datadir}/icons/crystalsvg/16x16/apps/samba.png
%{_datadir}/icons/crystalsvg/16x16/apps/scribus.png
%{_datadir}/icons/crystalsvg/16x16/apps/smserver.png
%{_datadir}/icons/crystalsvg/16x16/apps/socket.png
%{_datadir}/icons/crystalsvg/16x16/apps/sodipodi.png
%{_datadir}/icons/crystalsvg/16x16/apps/style.png
%{_datadir}/icons/crystalsvg/16x16/apps/stylesheet.png
%{_datadir}/icons/crystalsvg/16x16/apps/systemtray.png
%{_datadir}/icons/crystalsvg/16x16/apps/taskbar.png
%{_datadir}/icons/crystalsvg/16x16/apps/terminal.png
%{_datadir}/icons/crystalsvg/16x16/apps/tux.png
%{_datadir}/icons/crystalsvg/16x16/apps/usb.png
%{_datadir}/icons/crystalsvg/16x16/apps/vnc.png
%{_datadir}/icons/crystalsvg/16x16/apps/wabi.png
%{_datadir}/icons/crystalsvg/16x16/apps/window_list.png
%{_datadir}/icons/crystalsvg/16x16/apps/wine.png
%{_datadir}/icons/crystalsvg/16x16/apps/wp.png
%{_datadir}/icons/crystalsvg/16x16/apps/xcalc.png
%{_datadir}/icons/crystalsvg/16x16/apps/xchat.png
%{_datadir}/icons/crystalsvg/16x16/apps/xclipboard.png
%{_datadir}/icons/crystalsvg/16x16/apps/xclock.png
%{_datadir}/icons/crystalsvg/16x16/apps/xconsole.png
%{_datadir}/icons/crystalsvg/16x16/apps/xedit.png
%{_datadir}/icons/crystalsvg/16x16/apps/xemacs.png
%{_datadir}/icons/crystalsvg/16x16/apps/xeyes.png
%{_datadir}/icons/crystalsvg/16x16/apps/xfig.png
%{_datadir}/icons/crystalsvg/16x16/apps/xfmail.png
%{_datadir}/icons/crystalsvg/16x16/apps/xload.png
%{_datadir}/icons/crystalsvg/16x16/apps/xmag.png
%{_datadir}/icons/crystalsvg/16x16/apps/xmms.png
%{_datadir}/icons/crystalsvg/16x16/apps/xosview.png
%{_datadir}/icons/crystalsvg/16x16/apps/xpaint.png
%{_datadir}/icons/crystalsvg/16x16/apps/xv.png
%{_datadir}/icons/crystalsvg/16x16/devices/laptop.png
%{_datadir}/icons/crystalsvg/22x22/actions/newfont.png
%{_datadir}/icons/crystalsvg/22x22/apps/access.png
%{_datadir}/icons/crystalsvg/22x22/apps/agent.png
%{_datadir}/icons/crystalsvg/22x22/apps/arts.png
%{_datadir}/icons/crystalsvg/22x22/apps/background.png
%{_datadir}/icons/crystalsvg/22x22/apps/bell.png
%{_datadir}/icons/crystalsvg/22x22/apps/cache.png
%{_datadir}/icons/crystalsvg/22x22/apps/colors.png
%{_datadir}/icons/crystalsvg/22x22/apps/cookie.png
%{_datadir}/icons/crystalsvg/22x22/apps/date.png
%{_datadir}/icons/crystalsvg/22x22/apps/email.png
%{_datadir}/icons/crystalsvg/22x22/apps/energy.png
%{_datadir}/icons/crystalsvg/22x22/apps/enhanced_browsing.png
%{_datadir}/icons/crystalsvg/22x22/apps/fifteenpieces.png
%{_datadir}/icons/crystalsvg/22x22/apps/filetypes.png
%{_datadir}/icons/crystalsvg/22x22/apps/fonts.png
%{_datadir}/icons/crystalsvg/22x22/apps/hwinfo.png
%{_datadir}/icons/crystalsvg/22x22/apps/icons.png
%{_datadir}/icons/crystalsvg/22x22/apps/iconthemes.png
%{_datadir}/icons/crystalsvg/22x22/apps/ieee1394.png
%{_datadir}/icons/crystalsvg/22x22/apps/kbinaryclock.png
%{_datadir}/icons/crystalsvg/22x22/apps/kcmdevices.png
%{_datadir}/icons/crystalsvg/22x22/apps/kcmkicker.png
%{_datadir}/icons/crystalsvg/22x22/apps/kcmkwm.png
%{_datadir}/icons/crystalsvg/22x22/apps/kcmx.png
%{_datadir}/icons/crystalsvg/22x22/apps/key_bindings.png
%{_datadir}/icons/crystalsvg/22x22/apps/keyboard.png
%{_datadir}/icons/crystalsvg/22x22/apps/kscreensaver.png
%{_datadir}/icons/crystalsvg/22x22/apps/kthememgr.png
%{_datadir}/icons/crystalsvg/22x22/apps/kvirc.png
%{_datadir}/icons/crystalsvg/22x22/apps/locale.png
%{_datadir}/icons/crystalsvg/22x22/apps/nedit.png
%{_datadir}/icons/crystalsvg/22x22/apps/package_development.png
%{_datadir}/icons/crystalsvg/22x22/apps/personal.png
%{_datadir}/icons/crystalsvg/22x22/apps/proxy.png
%{_datadir}/icons/crystalsvg/22x22/apps/randr.png
%{_datadir}/icons/crystalsvg/22x22/apps/runprocesscatcher.png
%{_datadir}/icons/crystalsvg/22x22/apps/samba.png
%{_datadir}/icons/crystalsvg/22x22/apps/style.png
%{_datadir}/icons/crystalsvg/22x22/apps/stylesheet.png
%{_datadir}/icons/crystalsvg/22x22/apps/systemtray.png
%{_datadir}/icons/crystalsvg/22x22/apps/taskbar.png
%{_datadir}/icons/crystalsvg/22x22/devices/laptop.png
%{_datadir}/icons/crystalsvg/32x32/actions/newfont.png
%{_datadir}/icons/crystalsvg/32x32/apps/abiword.png
%{_datadir}/icons/crystalsvg/32x32/apps/access.png
%{_datadir}/icons/crystalsvg/32x32/apps/acroread.png
%{_datadir}/icons/crystalsvg/32x32/apps/agent.png
%{_datadir}/icons/crystalsvg/32x32/apps/alevt.png
%{_datadir}/icons/crystalsvg/32x32/apps/applixware.png
%{_datadir}/icons/crystalsvg/32x32/apps/arts.png
%{_datadir}/icons/crystalsvg/32x32/apps/assistant.png
%{_datadir}/icons/crystalsvg/32x32/apps/background.png
%{_datadir}/icons/crystalsvg/32x32/apps/bell.png
%{_datadir}/icons/crystalsvg/32x32/apps/blender.png
%{_datadir}/icons/crystalsvg/32x32/apps/bluefish.png
%{_datadir}/icons/crystalsvg/32x32/apps/cache.png
%{_datadir}/icons/crystalsvg/32x32/apps/clanbomber.png
%{_datadir}/icons/crystalsvg/32x32/apps/clock.png
%{_datadir}/icons/crystalsvg/32x32/apps/colors.png
%{_datadir}/icons/crystalsvg/32x32/apps/cookie.png
%{_datadir}/icons/crystalsvg/32x32/apps/date.png
%{_datadir}/icons/crystalsvg/32x32/apps/designer.png
%{_datadir}/icons/crystalsvg/32x32/apps/dia.png
%{_datadir}/icons/crystalsvg/32x32/apps/dlgedit.png
%{_datadir}/icons/crystalsvg/32x32/apps/eclipse.png
%{_datadir}/icons/crystalsvg/32x32/apps/edu_languages.png
%{_datadir}/icons/crystalsvg/32x32/apps/edu_mathematics.png
%{_datadir}/icons/crystalsvg/32x32/apps/edu_miscellaneous.png
%{_datadir}/icons/crystalsvg/32x32/apps/edu_science.png
%{_datadir}/icons/crystalsvg/32x32/apps/emacs.png
%{_datadir}/icons/crystalsvg/32x32/apps/email.png
%{_datadir}/icons/crystalsvg/32x32/apps/energy.png
%{_datadir}/icons/crystalsvg/32x32/apps/energy_star.png
%{_datadir}/icons/crystalsvg/32x32/apps/enhanced_browsing.png
%{_datadir}/icons/crystalsvg/32x32/apps/error.png
%{_datadir}/icons/crystalsvg/32x32/apps/evolution.png
%{_datadir}/icons/crystalsvg/32x32/apps/fifteenpieces.png
%{_datadir}/icons/crystalsvg/32x32/apps/filetypes.png
%{_datadir}/icons/crystalsvg/32x32/apps/fonts.png
%{_datadir}/icons/crystalsvg/32x32/apps/gabber.png
%{_datadir}/icons/crystalsvg/32x32/apps/gaim.png
%{_datadir}/icons/crystalsvg/32x32/apps/galeon.png
%{_datadir}/icons/crystalsvg/32x32/apps/gimp.png
%{_datadir}/icons/crystalsvg/32x32/apps/gnome_apps.png
%{_datadir}/icons/crystalsvg/32x32/apps/gnomemeeting.png
%{_datadir}/icons/crystalsvg/32x32/apps/gnucash.png
%{_datadir}/icons/crystalsvg/32x32/apps/gnumeric.png
%{_datadir}/icons/crystalsvg/32x32/apps/gv.png
%{_datadir}/icons/crystalsvg/32x32/apps/gvim.png
%{_datadir}/icons/crystalsvg/32x32/apps/help_index.png
%{_datadir}/icons/crystalsvg/32x32/apps/hwinfo.png
%{_datadir}/icons/crystalsvg/32x32/apps/icons.png
%{_datadir}/icons/crystalsvg/32x32/apps/iconthemes.png
%{_datadir}/icons/crystalsvg/32x32/apps/ieee1394.png
%{_datadir}/icons/crystalsvg/32x32/apps/input_devices_settings.png
%{_datadir}/icons/crystalsvg/32x32/apps/kbinaryclock.png
%{_datadir}/icons/crystalsvg/32x32/apps/kcmdevices.png
%{_datadir}/icons/crystalsvg/32x32/apps/kcmdrkonqi.png
%{_datadir}/icons/crystalsvg/32x32/apps/kcmkicker.png
%{_datadir}/icons/crystalsvg/32x32/apps/kcmkwm.png
%{_datadir}/icons/crystalsvg/32x32/apps/kcmmemory.png
%{_datadir}/icons/crystalsvg/32x32/apps/kcmmidi.png
%{_datadir}/icons/crystalsvg/32x32/apps/kcmpartitions.png
%{_datadir}/icons/crystalsvg/32x32/apps/kcmpci.png
%{_datadir}/icons/crystalsvg/32x32/apps/kcmprocessor.png
%{_datadir}/icons/crystalsvg/32x32/apps/kcmscsi.png
%{_datadir}/icons/crystalsvg/32x32/apps/kcmsound.png
%{_datadir}/icons/crystalsvg/32x32/apps/kcmsystem.png
%{_datadir}/icons/crystalsvg/32x32/apps/kcmx.png
%{_datadir}/icons/crystalsvg/32x32/apps/kcontrol.png
%{_datadir}/icons/crystalsvg/32x32/apps/kdisknav.png
%{_datadir}/icons/crystalsvg/32x32/apps/keditbookmarks.png
%{_datadir}/icons/crystalsvg/32x32/apps/key_bindings.png
%{_datadir}/icons/crystalsvg/32x32/apps/keyboard.png
%{_datadir}/icons/crystalsvg/32x32/apps/keyboard_layout.png
%{_datadir}/icons/crystalsvg/32x32/apps/kfm_home.png
%{_datadir}/icons/crystalsvg/32x32/apps/knotify.png
%{_datadir}/icons/crystalsvg/32x32/apps/kscreensaver.png
%{_datadir}/icons/crystalsvg/32x32/apps/kthememgr.png
%{_datadir}/icons/crystalsvg/32x32/apps/kvirc.png
%{_datadir}/icons/crystalsvg/32x32/apps/twin.png
%{_datadir}/icons/crystalsvg/32x32/apps/licq.png
%{_datadir}/icons/crystalsvg/32x32/apps/linguist.png
%{_datadir}/icons/crystalsvg/32x32/apps/linuxconf.png
%{_datadir}/icons/crystalsvg/32x32/apps/locale.png
%{_datadir}/icons/crystalsvg/32x32/apps/looknfeel.png
%{_datadir}/icons/crystalsvg/32x32/apps/lyx.png
%{_datadir}/icons/crystalsvg/32x32/apps/mac.png
%{_datadir}/icons/crystalsvg/32x32/apps/mathematica.png
%{_datadir}/icons/crystalsvg/32x32/apps/multimedia.png
%{_datadir}/icons/crystalsvg/32x32/apps/nedit.png
%{_datadir}/icons/crystalsvg/32x32/apps/netscape.png
%{_datadir}/icons/crystalsvg/32x32/apps/opera.png
%{_datadir}/icons/crystalsvg/32x32/apps/package.png
%{_datadir}/icons/crystalsvg/32x32/apps/package_applications.png
%{_datadir}/icons/crystalsvg/32x32/apps/package_development.png
%{_datadir}/icons/crystalsvg/32x32/apps/package_editors.png
%{_datadir}/icons/crystalsvg/32x32/apps/package_edutainment.png
%{_datadir}/icons/crystalsvg/32x32/apps/package_favourite.png
%{_datadir}/icons/crystalsvg/32x32/apps/package_games.png
%{_datadir}/icons/crystalsvg/32x32/apps/package_games_arcade.png
%{_datadir}/icons/crystalsvg/32x32/apps/package_games_board.png
%{_datadir}/icons/crystalsvg/32x32/apps/package_games_card.png
%{_datadir}/icons/crystalsvg/32x32/apps/package_games_strategy.png
%{_datadir}/icons/crystalsvg/32x32/apps/package_graphics.png
%{_datadir}/icons/crystalsvg/32x32/apps/package_multimedia.png
%{_datadir}/icons/crystalsvg/32x32/apps/package_network.png
%{_datadir}/icons/crystalsvg/32x32/apps/package_settings.png
%{_datadir}/icons/crystalsvg/32x32/apps/package_system.png
%{_datadir}/icons/crystalsvg/32x32/apps/package_toys.png
%{_datadir}/icons/crystalsvg/32x32/apps/package_utilities.png
%{_datadir}/icons/crystalsvg/32x32/apps/package_wordprocessing.png
%{_datadir}/icons/crystalsvg/32x32/apps/pan.png
%{_datadir}/icons/crystalsvg/32x32/apps/penguin.png
%{_datadir}/icons/crystalsvg/32x32/apps/personal.png
%{_datadir}/icons/crystalsvg/32x32/apps/phppg.png
%{_datadir}/icons/crystalsvg/32x32/apps/pinguin.png
%{_datadir}/icons/crystalsvg/32x32/apps/plan.png
%{_datadir}/icons/crystalsvg/32x32/apps/planner.png
%{_datadir}/icons/crystalsvg/32x32/apps/proxy.png
%{_datadir}/icons/crystalsvg/32x32/apps/pybliographic.png
%{_datadir}/icons/crystalsvg/32x32/apps/pysol.png
%{_datadir}/icons/crystalsvg/32x32/apps/randr.png
%{_datadir}/icons/crystalsvg/32x32/apps/realplayer.png
%{_datadir}/icons/crystalsvg/32x32/apps/runprocesscatcher.png
%{_datadir}/icons/crystalsvg/32x32/apps/samba.png
%{_datadir}/icons/crystalsvg/32x32/apps/scribus.png
%{_datadir}/icons/crystalsvg/32x32/apps/sodipodi.png
%{_datadir}/icons/crystalsvg/32x32/apps/style.png
%{_datadir}/icons/crystalsvg/32x32/apps/stylesheet.png
%{_datadir}/icons/crystalsvg/32x32/apps/systemtray.png
%{_datadir}/icons/crystalsvg/32x32/apps/taskbar.png
%{_datadir}/icons/crystalsvg/32x32/apps/terminal.png
%{_datadir}/icons/crystalsvg/32x32/apps/tux.png
%{_datadir}/icons/crystalsvg/32x32/apps/usb.png
%{_datadir}/icons/crystalsvg/32x32/apps/vnc.png
%{_datadir}/icons/crystalsvg/32x32/apps/wabi.png
%{_datadir}/icons/crystalsvg/32x32/apps/window_list.png
%{_datadir}/icons/crystalsvg/32x32/apps/wine.png
%{_datadir}/icons/crystalsvg/32x32/apps/wp.png
%{_datadir}/icons/crystalsvg/32x32/apps/x.png
%{_datadir}/icons/crystalsvg/32x32/apps/xapp.png
%{_datadir}/icons/crystalsvg/32x32/apps/xawtv.png
%{_datadir}/icons/crystalsvg/32x32/apps/xcalc.png
%{_datadir}/icons/crystalsvg/32x32/apps/xchat.png
%{_datadir}/icons/crystalsvg/32x32/apps/xclipboard.png
%{_datadir}/icons/crystalsvg/32x32/apps/xclock.png
%{_datadir}/icons/crystalsvg/32x32/apps/xconsole.png
%{_datadir}/icons/crystalsvg/32x32/apps/xedit.png
%{_datadir}/icons/crystalsvg/32x32/apps/xemacs.png
%{_datadir}/icons/crystalsvg/32x32/apps/xeyes.png
%{_datadir}/icons/crystalsvg/32x32/apps/xfig.png
%{_datadir}/icons/crystalsvg/32x32/apps/xfmail.png
%{_datadir}/icons/crystalsvg/32x32/apps/xload.png
%{_datadir}/icons/crystalsvg/32x32/apps/xmag.png
%{_datadir}/icons/crystalsvg/32x32/apps/xmms.png
%{_datadir}/icons/crystalsvg/32x32/apps/xosview.png
%{_datadir}/icons/crystalsvg/32x32/apps/xpaint.png
%{_datadir}/icons/crystalsvg/32x32/apps/xv.png
%{_datadir}/icons/crystalsvg/32x32/devices/laptop.png
%{_datadir}/icons/crystalsvg/48x48/apps/abiword.png
%{_datadir}/icons/crystalsvg/48x48/apps/access.png
%{_datadir}/icons/crystalsvg/48x48/apps/acroread.png
%{_datadir}/icons/crystalsvg/48x48/apps/agent.png
%{_datadir}/icons/crystalsvg/48x48/apps/applixware.png
%{_datadir}/icons/crystalsvg/48x48/apps/arts.png
%{_datadir}/icons/crystalsvg/48x48/apps/background.png
%{_datadir}/icons/crystalsvg/48x48/apps/bell.png
%{_datadir}/icons/crystalsvg/48x48/apps/blender.png
%{_datadir}/icons/crystalsvg/48x48/apps/bluefish.png
%{_datadir}/icons/crystalsvg/48x48/apps/cache.png
%{_datadir}/icons/crystalsvg/48x48/apps/clanbomber.png
%{_datadir}/icons/crystalsvg/48x48/apps/clock.png
%{_datadir}/icons/crystalsvg/48x48/apps/colors.png
%{_datadir}/icons/crystalsvg/48x48/apps/cookie.png
%{_datadir}/icons/crystalsvg/48x48/apps/date.png
%{_datadir}/icons/crystalsvg/48x48/apps/designer.png
%{_datadir}/icons/crystalsvg/48x48/apps/dia.png
%{_datadir}/icons/crystalsvg/48x48/apps/eclipse.png
%{_datadir}/icons/crystalsvg/48x48/apps/edu_languages.png
%{_datadir}/icons/crystalsvg/48x48/apps/edu_mathematics.png
%{_datadir}/icons/crystalsvg/48x48/apps/edu_miscellaneous.png
%{_datadir}/icons/crystalsvg/48x48/apps/edu_science.png
%{_datadir}/icons/crystalsvg/48x48/apps/emacs.png
%{_datadir}/icons/crystalsvg/48x48/apps/email.png
%{_datadir}/icons/crystalsvg/48x48/apps/energy.png
%{_datadir}/icons/crystalsvg/48x48/apps/energy_star.png
%{_datadir}/icons/crystalsvg/48x48/apps/enhanced_browsing.png
%{_datadir}/icons/crystalsvg/48x48/apps/evolution.png
%{_datadir}/icons/crystalsvg/48x48/apps/fifteenpieces.png
%{_datadir}/icons/crystalsvg/48x48/apps/filetypes.png
%{_datadir}/icons/crystalsvg/48x48/apps/fonts.png
%{_datadir}/icons/crystalsvg/48x48/apps/gabber.png
%{_datadir}/icons/crystalsvg/48x48/apps/gaim.png
%{_datadir}/icons/crystalsvg/48x48/apps/galeon.png
%{_datadir}/icons/crystalsvg/48x48/apps/gimp.png
%{_datadir}/icons/crystalsvg/48x48/apps/gnome_apps.png
%{_datadir}/icons/crystalsvg/48x48/apps/gnomemeeting.png
%{_datadir}/icons/crystalsvg/48x48/apps/gnucash.png
%{_datadir}/icons/crystalsvg/48x48/apps/gnumeric.png
%{_datadir}/icons/crystalsvg/48x48/apps/gvim.png
%{_datadir}/icons/crystalsvg/48x48/apps/help_index.png
%{_datadir}/icons/crystalsvg/48x48/apps/hwinfo.png
%{_datadir}/icons/crystalsvg/48x48/apps/icons.png
%{_datadir}/icons/crystalsvg/48x48/apps/iconthemes.png
%{_datadir}/icons/crystalsvg/48x48/apps/ieee1394.png
%{_datadir}/icons/crystalsvg/48x48/apps/input_devices_settings.png
%{_datadir}/icons/crystalsvg/48x48/apps/kbinaryclock.png
%{_datadir}/icons/crystalsvg/48x48/apps/kcmdevices.png
%{_datadir}/icons/crystalsvg/48x48/apps/kcmdf.png
%{_datadir}/icons/crystalsvg/48x48/apps/kcmdrkonqi.png
%{_datadir}/icons/crystalsvg/48x48/apps/kcmkwm.png
%{_datadir}/icons/crystalsvg/48x48/apps/kcmmemory.png
%{_datadir}/icons/crystalsvg/48x48/apps/kcmmidi.png
%{_datadir}/icons/crystalsvg/48x48/apps/kcmopengl.png
%{_datadir}/icons/crystalsvg/48x48/apps/kcmpartitions.png
%{_datadir}/icons/crystalsvg/48x48/apps/kcmpci.png
%{_datadir}/icons/crystalsvg/48x48/apps/kcmprocessor.png
%{_datadir}/icons/crystalsvg/48x48/apps/kcmscsi.png
%{_datadir}/icons/crystalsvg/48x48/apps/kcmsystem.png
%{_datadir}/icons/crystalsvg/48x48/apps/kcmx.png
%{_datadir}/icons/crystalsvg/48x48/apps/kcontrol.png
%{_datadir}/icons/crystalsvg/48x48/apps/kdisknav.png
%{_datadir}/icons/crystalsvg/48x48/apps/keditbookmarks.png
%{_datadir}/icons/crystalsvg/48x48/apps/key_bindings.png
%{_datadir}/icons/crystalsvg/48x48/apps/keyboard.png
%{_datadir}/icons/crystalsvg/48x48/apps/keyboard_layout.png
%{_datadir}/icons/crystalsvg/48x48/apps/kfm_home.png
%{_datadir}/icons/crystalsvg/48x48/apps/knotify.png
%{_datadir}/icons/crystalsvg/48x48/apps/kscreensaver.png
%{_datadir}/icons/crystalsvg/48x48/apps/kthememgr.png
%{_datadir}/icons/crystalsvg/48x48/apps/kvirc.png
%{_datadir}/icons/crystalsvg/48x48/apps/twin.png
%{_datadir}/icons/crystalsvg/48x48/apps/licq.png
%{_datadir}/icons/crystalsvg/48x48/apps/linuxconf.png
%{_datadir}/icons/crystalsvg/48x48/apps/locale.png
%{_datadir}/icons/crystalsvg/48x48/apps/looknfeel.png
%{_datadir}/icons/crystalsvg/48x48/apps/multimedia.png
%{_datadir}/icons/crystalsvg/48x48/apps/nedit.png
%{_datadir}/icons/crystalsvg/48x48/apps/netscape.png
%{_datadir}/icons/crystalsvg/48x48/apps/opera.png
%{_datadir}/icons/crystalsvg/48x48/apps/package.png
%{_datadir}/icons/crystalsvg/48x48/apps/package_applications.png
%{_datadir}/icons/crystalsvg/48x48/apps/package_development.png
%{_datadir}/icons/crystalsvg/48x48/apps/package_editors.png
%{_datadir}/icons/crystalsvg/48x48/apps/package_edutainment.png
%{_datadir}/icons/crystalsvg/48x48/apps/package_favourite.png
%{_datadir}/icons/crystalsvg/48x48/apps/package_games.png
%{_datadir}/icons/crystalsvg/48x48/apps/package_games_arcade.png
%{_datadir}/icons/crystalsvg/48x48/apps/package_games_board.png
%{_datadir}/icons/crystalsvg/48x48/apps/package_games_card.png
%{_datadir}/icons/crystalsvg/48x48/apps/package_games_strategy.png
%{_datadir}/icons/crystalsvg/48x48/apps/package_graphics.png
%{_datadir}/icons/crystalsvg/48x48/apps/package_multimedia.png
%{_datadir}/icons/crystalsvg/48x48/apps/package_network.png
%{_datadir}/icons/crystalsvg/48x48/apps/package_settings.png
%{_datadir}/icons/crystalsvg/48x48/apps/package_system.png
%{_datadir}/icons/crystalsvg/48x48/apps/package_toys.png
%{_datadir}/icons/crystalsvg/48x48/apps/package_utilities.png
%{_datadir}/icons/crystalsvg/48x48/apps/package_wordprocessing.png
%{_datadir}/icons/crystalsvg/48x48/apps/pan.png
%{_datadir}/icons/crystalsvg/48x48/apps/penguin.png
%{_datadir}/icons/crystalsvg/48x48/apps/personal.png
%{_datadir}/icons/crystalsvg/48x48/apps/phppg.png
%{_datadir}/icons/crystalsvg/48x48/apps/planner.png
%{_datadir}/icons/crystalsvg/48x48/apps/proxy.png
%{_datadir}/icons/crystalsvg/48x48/apps/pysol.png
%{_datadir}/icons/crystalsvg/48x48/apps/randr.png
%{_datadir}/icons/crystalsvg/48x48/apps/remote.png
%{_datadir}/icons/crystalsvg/48x48/apps/samba.png
%{_datadir}/icons/crystalsvg/48x48/apps/scribus.png
%{_datadir}/icons/crystalsvg/48x48/apps/sodipodi.png
%{_datadir}/icons/crystalsvg/48x48/apps/staroffice.png
%{_datadir}/icons/crystalsvg/48x48/apps/style.png
%{_datadir}/icons/crystalsvg/48x48/apps/stylesheet.png
%{_datadir}/icons/crystalsvg/48x48/apps/systemtray.png
%{_datadir}/icons/crystalsvg/48x48/apps/taskbar.png
%{_datadir}/icons/crystalsvg/48x48/apps/terminal.png
%{_datadir}/icons/crystalsvg/48x48/apps/tux.png
%{_datadir}/icons/crystalsvg/48x48/apps/usb.png
%{_datadir}/icons/crystalsvg/48x48/apps/vnc.png
%{_datadir}/icons/crystalsvg/48x48/apps/window_list.png
%{_datadir}/icons/crystalsvg/48x48/apps/wine.png
%{_datadir}/icons/crystalsvg/48x48/apps/wmaker_apps.png
%{_datadir}/icons/crystalsvg/48x48/apps/wp.png
%{_datadir}/icons/crystalsvg/48x48/apps/xchat.png
%{_datadir}/icons/crystalsvg/48x48/apps/xclock.png
%{_datadir}/icons/crystalsvg/48x48/apps/xedit.png
%{_datadir}/icons/crystalsvg/48x48/apps/xemacs.png
%{_datadir}/icons/crystalsvg/48x48/apps/xfmail.png
%{_datadir}/icons/crystalsvg/48x48/apps/xmag.png
%{_datadir}/icons/crystalsvg/48x48/apps/xv.png
%{_datadir}/icons/crystalsvg/48x48/devices/laptop.png
%{_datadir}/icons/crystalsvg/64x64/apps/access.png
%{_datadir}/icons/crystalsvg/64x64/apps/acroread.png
%{_datadir}/icons/crystalsvg/64x64/apps/applixware.png
%{_datadir}/icons/crystalsvg/64x64/apps/arts.png
%{_datadir}/icons/crystalsvg/64x64/apps/background.png
%{_datadir}/icons/crystalsvg/64x64/apps/bell.png
%{_datadir}/icons/crystalsvg/64x64/apps/cache.png
%{_datadir}/icons/crystalsvg/64x64/apps/clanbomber.png
%{_datadir}/icons/crystalsvg/64x64/apps/clock.png
%{_datadir}/icons/crystalsvg/64x64/apps/colors.png
%{_datadir}/icons/crystalsvg/64x64/apps/cookie.png
%{_datadir}/icons/crystalsvg/64x64/apps/date.png
%{_datadir}/icons/crystalsvg/64x64/apps/email.png
%{_datadir}/icons/crystalsvg/64x64/apps/energy.png
%{_datadir}/icons/crystalsvg/64x64/apps/energy_star.png
%{_datadir}/icons/crystalsvg/64x64/apps/enhanced_browsing.png
%{_datadir}/icons/crystalsvg/64x64/apps/filetypes.png
%{_datadir}/icons/crystalsvg/64x64/apps/fonts.png
%{_datadir}/icons/crystalsvg/64x64/apps/gimp.png
%{_datadir}/icons/crystalsvg/64x64/apps/gvim.png
%{_datadir}/icons/crystalsvg/64x64/apps/help_index.png
%{_datadir}/icons/crystalsvg/64x64/apps/hwinfo.png
%{_datadir}/icons/crystalsvg/64x64/apps/icons.png
%{_datadir}/icons/crystalsvg/64x64/apps/ieee1394.png
%{_datadir}/icons/crystalsvg/64x64/apps/kcmdevices.png
%{_datadir}/icons/crystalsvg/64x64/apps/kcmdf.png
%{_datadir}/icons/crystalsvg/64x64/apps/kcmkwm.png
%{_datadir}/icons/crystalsvg/64x64/apps/kcmmemory.png
%{_datadir}/icons/crystalsvg/64x64/apps/kcmpartitions.png
%{_datadir}/icons/crystalsvg/64x64/apps/kcmpci.png
%{_datadir}/icons/crystalsvg/64x64/apps/kcmx.png
%{_datadir}/icons/crystalsvg/64x64/apps/kcontrol.png
%{_datadir}/icons/crystalsvg/64x64/apps/keditbookmarks.png
%{_datadir}/icons/crystalsvg/64x64/apps/key_bindings.png
%{_datadir}/icons/crystalsvg/64x64/apps/kfm_home.png
%{_datadir}/icons/crystalsvg/64x64/apps/knotify.png
%{_datadir}/icons/crystalsvg/64x64/apps/kscreensaver.png
%{_datadir}/icons/crystalsvg/64x64/apps/kthememgr.png
%{_datadir}/icons/crystalsvg/64x64/apps/kvirc.png
%{_datadir}/icons/crystalsvg/64x64/apps/licq.png
%{_datadir}/icons/crystalsvg/64x64/apps/linuxconf.png
%{_datadir}/icons/crystalsvg/64x64/apps/locale.png
%{_datadir}/icons/crystalsvg/64x64/apps/looknfeel.png
%{_datadir}/icons/crystalsvg/64x64/apps/multimedia.png
%{_datadir}/icons/crystalsvg/64x64/apps/nedit.png
%{_datadir}/icons/crystalsvg/64x64/apps/netscape.png
%{_datadir}/icons/crystalsvg/64x64/apps/package.png
%{_datadir}/icons/crystalsvg/64x64/apps/package_applications.png
%{_datadir}/icons/crystalsvg/64x64/apps/package_development.png
%{_datadir}/icons/crystalsvg/64x64/apps/package_favourite.png
%{_datadir}/icons/crystalsvg/64x64/apps/package_games.png
%{_datadir}/icons/crystalsvg/64x64/apps/package_multimedia.png
%{_datadir}/icons/crystalsvg/64x64/apps/package_network.png
%{_datadir}/icons/crystalsvg/64x64/apps/package_settings.png
%{_datadir}/icons/crystalsvg/64x64/apps/package_toys.png
%{_datadir}/icons/crystalsvg/64x64/apps/package_utilities.png
%{_datadir}/icons/crystalsvg/64x64/apps/penguin.png
%{_datadir}/icons/crystalsvg/64x64/apps/personal.png
%{_datadir}/icons/crystalsvg/64x64/apps/phppg.png
%{_datadir}/icons/crystalsvg/64x64/apps/proxy.png
%{_datadir}/icons/crystalsvg/64x64/apps/pysol.png
%{_datadir}/icons/crystalsvg/64x64/apps/qtella.png
%{_datadir}/icons/crystalsvg/64x64/apps/randr.png
%{_datadir}/icons/crystalsvg/64x64/apps/samba.png
%{_datadir}/icons/crystalsvg/64x64/apps/staroffice.png
%{_datadir}/icons/crystalsvg/64x64/apps/style.png
%{_datadir}/icons/crystalsvg/64x64/apps/stylesheet.png
%{_datadir}/icons/crystalsvg/64x64/apps/systemtray.png
%{_datadir}/icons/crystalsvg/64x64/apps/taskbar.png
%{_datadir}/icons/crystalsvg/64x64/apps/terminal.png
%{_datadir}/icons/crystalsvg/64x64/apps/tux.png
%{_datadir}/icons/crystalsvg/64x64/apps/wp.png
%{_datadir}/icons/crystalsvg/64x64/apps/xclock.png
%{_datadir}/icons/crystalsvg/64x64/apps/xfmail.png
%{_datadir}/icons/crystalsvg/64x64/apps/xmag.png
%{_datadir}/icons/crystalsvg/64x64/devices/laptop.png
%{_datadir}/icons/crystalsvg/scalable/apps/access.svgz
%{_datadir}/icons/crystalsvg/scalable/apps/acroread.svgz
%{_datadir}/icons/crystalsvg/scalable/apps/aim.svgz
%{_datadir}/icons/crystalsvg/scalable/apps/aktion.svgz
%{_datadir}/icons/crystalsvg/scalable/apps/antivirus.svgz
%{_datadir}/icons/crystalsvg/scalable/apps/applixware.svgz
%{_datadir}/icons/crystalsvg/scalable/apps/arts.svgz
%{_datadir}/icons/crystalsvg/scalable/apps/background.svgz
%{_datadir}/icons/crystalsvg/scalable/apps/bell.svgz
%{_datadir}/icons/crystalsvg/scalable/apps/browser.svgz
%{_datadir}/icons/crystalsvg/scalable/apps/cache.svgz
%{_datadir}/icons/crystalsvg/scalable/apps/camera.svgz
%{_datadir}/icons/crystalsvg/scalable/apps/clanbomber.svgz
%{_datadir}/icons/crystalsvg/scalable/apps/clock.svgz
%{_datadir}/icons/crystalsvg/scalable/apps/colors.svgz
%{_datadir}/icons/crystalsvg/scalable/apps/core.svgz
%{_datadir}/icons/crystalsvg/scalable/apps/date.svgz
%{_datadir}/icons/crystalsvg/scalable/apps/display.svgz
%{_datadir}/icons/crystalsvg/scalable/apps/download_manager.svgz
%{_datadir}/icons/crystalsvg/scalable/apps/email.svgz
%{_datadir}/icons/crystalsvg/scalable/apps/energy.svgz
%{_datadir}/icons/crystalsvg/scalable/apps/error.svgz
%{_datadir}/icons/crystalsvg/scalable/apps/fifteenpieces.svgz
%{_datadir}/icons/crystalsvg/scalable/apps/filetypes.svgz
%{_datadir}/icons/crystalsvg/scalable/apps/fonts.svgz
%{_datadir}/icons/crystalsvg/scalable/apps/galeon.svgz
%{_datadir}/icons/crystalsvg/scalable/apps/gnome_apps.svgz
%{_datadir}/icons/crystalsvg/scalable/apps/hardware.svgz
%{_datadir}/icons/crystalsvg/scalable/apps/hwinfo.svgz
%{_datadir}/icons/crystalsvg/scalable/apps/ieee1394.svgz
%{_datadir}/icons/crystalsvg/scalable/apps/kbinaryclock.svgz
%{_datadir}/icons/crystalsvg/scalable/apps/kcmdevices.svgz
%{_datadir}/icons/crystalsvg/scalable/apps/kcmkwm.svgz
%{_datadir}/icons/crystalsvg/scalable/apps/kcmx.svgz
%{_datadir}/icons/crystalsvg/scalable/apps/kfm_home.svgz
%{_datadir}/icons/crystalsvg/scalable/apps/locale.svgz
%{_datadir}/icons/crystalsvg/scalable/apps/my_mac.svgz
%{_datadir}/icons/crystalsvg/scalable/apps/netscape.svgz
%{_datadir}/icons/crystalsvg/scalable/apps/openoffice.svgz
%{_datadir}/icons/crystalsvg/scalable/apps/package_development.svgz
%{_datadir}/icons/crystalsvg/scalable/apps/package_toys.svgz
%{_datadir}/icons/crystalsvg/scalable/apps/penguin.svgz
%{_datadir}/icons/crystalsvg/scalable/apps/personal.svgz
%{_datadir}/icons/crystalsvg/scalable/apps/quicktime.svgz
%{_datadir}/icons/crystalsvg/scalable/apps/realplayer.svgz
%{_datadir}/icons/crystalsvg/scalable/apps/samba.svgz
%{_datadir}/icons/crystalsvg/scalable/apps/shell.svgz
%{_datadir}/icons/crystalsvg/scalable/apps/staroffice.svgz
%{_datadir}/icons/crystalsvg/scalable/apps/stylesheet.svgz
%{_datadir}/icons/crystalsvg/scalable/apps/systemtray.svgz
%{_datadir}/icons/crystalsvg/scalable/apps/terminal.svgz
%{_datadir}/icons/crystalsvg/scalable/apps/tux.svgz
%{_datadir}/icons/crystalsvg/scalable/apps/wine.svgz
%{_datadir}/icons/crystalsvg/scalable/apps/x.svgz
%{_datadir}/icons/crystalsvg/scalable/apps/xapp.svgz
%{_datadir}/icons/crystalsvg/scalable/apps/xcalc.svgz
%{_datadir}/icons/crystalsvg/scalable/apps/xchat.svgz
%{_datadir}/icons/crystalsvg/scalable/apps/xclock.svgz
%{_datadir}/icons/crystalsvg/scalable/apps/xeyes.svgz
%{_datadir}/icons/crystalsvg/scalable/apps/xpaint.svgz
%{_datadir}/icons/crystalsvg/scalable/devices/laptop.svgz
%{_datadir}/icons/hicolor/128x128/apps/kappfinder.png
%{_datadir}/icons/hicolor/128x128/apps/khelpcenter.png
%{_datadir}/icons/hicolor/128x128/apps/kjobviewer.png
%{_datadir}/icons/hicolor/128x128/apps/klipper.png
%{_datadir}/icons/hicolor/128x128/apps/knetattach.png
%{_datadir}/icons/hicolor/128x128/apps/konqueror.png
%{_datadir}/icons/hicolor/128x128/apps/ksplash.png
%{_datadir}/icons/hicolor/128x128/apps/kwrite.png
%{_datadir}/icons/hicolor/128x128/apps/printmgr.png
%{_datadir}/icons/hicolor/16x16/apps/kappfinder.png
%{_datadir}/icons/hicolor/16x16/apps/kfind.png
%{_datadir}/icons/hicolor/16x16/apps/kfm.png
%{_datadir}/icons/hicolor/16x16/apps/khelpcenter.png
%{_datadir}/icons/hicolor/16x16/apps/khotkeys.png
%{_datadir}/icons/hicolor/16x16/apps/kjobviewer.png
%{_datadir}/icons/hicolor/16x16/apps/klipper.png
%{_datadir}/icons/hicolor/16x16/apps/knetattach.png
%{_datadir}/icons/hicolor/16x16/apps/konqueror.png
%{_datadir}/icons/hicolor/16x16/apps/ksplash.png
%{_datadir}/icons/hicolor/16x16/apps/kwrite.png
%{_datadir}/icons/hicolor/16x16/apps/kxkb.png
%{_datadir}/icons/hicolor/16x16/apps/printmgr.png
%{_datadir}/icons/hicolor/22x22/apps/kappfinder.png
%{_datadir}/icons/hicolor/22x22/apps/kfind.png
%{_datadir}/icons/hicolor/22x22/apps/kfm.png
%{_datadir}/icons/hicolor/22x22/apps/khelpcenter.png
%{_datadir}/icons/hicolor/22x22/apps/kjobviewer.png
%{_datadir}/icons/hicolor/22x22/apps/klipper.png
%{_datadir}/icons/hicolor/22x22/apps/knetattach.png
%{_datadir}/icons/hicolor/22x22/apps/konqueror.png
%{_datadir}/icons/hicolor/22x22/apps/ksplash.png
%{_datadir}/icons/hicolor/22x22/apps/kwrite.png
%{_datadir}/icons/hicolor/22x22/apps/printmgr.png
%{_datadir}/icons/hicolor/32x32/apps/kappfinder.png
%{_datadir}/icons/hicolor/32x32/apps/kfind.png
%{_datadir}/icons/hicolor/32x32/apps/kfm.png
%{_datadir}/icons/hicolor/32x32/apps/khelpcenter.png
%{_datadir}/icons/hicolor/32x32/apps/khotkeys.png
%{_datadir}/icons/hicolor/32x32/apps/kjobviewer.png
%{_datadir}/icons/hicolor/32x32/apps/klipper.png
%{_datadir}/icons/hicolor/32x32/apps/knetattach.png
%{_datadir}/icons/hicolor/32x32/apps/konqueror.png
%{_datadir}/icons/hicolor/32x32/apps/ksplash.png
%{_datadir}/icons/hicolor/32x32/apps/kwrite.png
%{_datadir}/icons/hicolor/32x32/apps/kxkb.png
%{_datadir}/icons/hicolor/32x32/apps/printmgr.png
%{_datadir}/icons/hicolor/48x48/apps/kappfinder.png
%{_datadir}/icons/hicolor/48x48/apps/kfind.png
%{_datadir}/icons/hicolor/48x48/apps/kfm.png
%{_datadir}/icons/hicolor/48x48/apps/khelpcenter.png
%{_datadir}/icons/hicolor/48x48/apps/kjobviewer.png
%{_datadir}/icons/hicolor/48x48/apps/klipper.png
%{_datadir}/icons/hicolor/48x48/apps/kmenuedit.png
%{_datadir}/icons/hicolor/48x48/apps/knetattach.png
%{_datadir}/icons/hicolor/48x48/apps/konqueror.png
%{_datadir}/icons/hicolor/48x48/apps/ksplash.png
%{_datadir}/icons/hicolor/48x48/apps/kwrite.png
%{_datadir}/icons/hicolor/48x48/apps/kxkb.png
%{_datadir}/icons/hicolor/48x48/apps/printmgr.png
%{_datadir}/icons/hicolor/64x64/apps/kappfinder.png
%{_datadir}/icons/hicolor/64x64/apps/kfind.png
%{_datadir}/icons/hicolor/64x64/apps/kfm.png
%{_datadir}/icons/hicolor/64x64/apps/khelpcenter.png
%{_datadir}/icons/hicolor/64x64/apps/kjobviewer.png
%{_datadir}/icons/hicolor/64x64/apps/klipper.png
%{_datadir}/icons/hicolor/64x64/apps/knetattach.png
%{_datadir}/icons/hicolor/64x64/apps/konqueror.png
%{_datadir}/icons/hicolor/64x64/apps/ksplash.png
%{_datadir}/icons/hicolor/64x64/apps/kwrite.png
%{_datadir}/icons/hicolor/64x64/apps/printmgr.png
%{_datadir}/icons/hicolor/scalable/apps/khelpcenter.svgz
%{_datadir}/icons/hicolor/scalable/apps/kjobviewer.svgz
%{_datadir}/icons/hicolor/scalable/apps/klipper.svgz
%{_datadir}/icons/hicolor/scalable/apps/knetattach.svgz
%{_datadir}/icons/hicolor/scalable/apps/konqueror.svgz
%{_datadir}/icons/hicolor/scalable/apps/kwrite2.svgz
%{_datadir}/icons/hicolor/scalable/apps/printmgr.svgz
%{_datadir}/locale/*
#%{_datadir}/man/man1/appletproxy.1.gz
#%{_datadir}/man/man1/kappfinder.1.gz
#%{_datadir}/man/man1/kbookmarkmerger.1.gz
#%{_datadir}/man/man1/kdesu.1.gz
#%{_datadir}/man/man1/kfind.1.gz
#%{_datadir}/man/man1/kicker.1.gz
%{_datadir}/mimelnk/application/x-ktheme.desktop
%{_datadir}/mimelnk/fonts/*.desktop
%{_datadir}/mimelnk/inode/*.desktop
%{_datadir}/mimelnk/media/audiocd.desktop
%{_datadir}/mimelnk/media/blankcd.desktop
%{_datadir}/mimelnk/media/blankdvd.desktop
%{_datadir}/mimelnk/media/camera_mounted.desktop
%{_datadir}/mimelnk/media/camera_unmounted.desktop
%{_datadir}/mimelnk/media/cdrom_mounted.desktop
%{_datadir}/mimelnk/media/cdrom_unmounted.desktop
%{_datadir}/mimelnk/media/cdwriter_mounted.desktop
%{_datadir}/mimelnk/media/cdwriter_unmounted.desktop
%{_datadir}/mimelnk/media/dvd_mounted.desktop
%{_datadir}/mimelnk/media/dvd_unmounted.desktop
%{_datadir}/mimelnk/media/dvdvideo.desktop
%{_datadir}/mimelnk/media/floppy5_mounted.desktop
%{_datadir}/mimelnk/media/floppy5_unmounted.desktop
%{_datadir}/mimelnk/media/floppy_mounted.desktop
%{_datadir}/mimelnk/media/floppy_unmounted.desktop
%{_datadir}/mimelnk/media/gphoto2camera.desktop
%{_datadir}/mimelnk/media/hdd_mounted.desktop
%{_datadir}/mimelnk/media/hdd_unmounted.desktop
%{_datadir}/mimelnk/media/nfs_mounted.desktop
%{_datadir}/mimelnk/media/nfs_unmounted.desktop
%{_datadir}/mimelnk/media/removable_mounted.desktop
%{_datadir}/mimelnk/media/removable_unmounted.desktop
%{_datadir}/mimelnk/media/smb_mounted.desktop
%{_datadir}/mimelnk/media/smb_unmounted.desktop
%{_datadir}/mimelnk/media/svcd.desktop
%{_datadir}/mimelnk/media/vcd.desktop
%{_datadir}/mimelnk/media/zip_mounted.desktop
%{_datadir}/mimelnk/media/zip_unmounted.desktop
%{_datadir}/mimelnk/print/class.desktop
%{_datadir}/mimelnk/print/driver.desktop
%{_datadir}/mimelnk/print/folder.desktop
%{_datadir}/mimelnk/print/jobs.desktop
%{_datadir}/mimelnk/print/manager.desktop
%{_datadir}/mimelnk/print/printer.desktop
%{_datadir}/mimelnk/print/printermodel.desktop
%{_datadir}/services/about.protocol
%{_datadir}/services/applications.protocol
%{_datadir}/services/ar.protocol
%{_datadir}/services/bzip.protocol
%{_datadir}/services/bzip2.protocol
%{_datadir}/services/cgi.protocol
%{_datadir}/services/cursorthumbnail.desktop
%{_datadir}/services/djvuthumbnail.desktop
%{_datadir}/services/exrthumbnail.desktop
%{_datadir}/services/finger.protocol
%{_datadir}/services/fish.protocol
%{_datadir}/services/floppy.protocol
%{_datadir}/services/fonts.protocol
%{_datadir}/services/fontthumbnail.desktop
%{_datadir}/services/gzip.protocol
%{_datadir}/services/home.protocol
%{_datadir}/services/htmlthumbnail.desktop
%{_datadir}/services/imagethumbnail.desktop
%{_datadir}/services/info.protocol
%{_datadir}/services/kaccess.desktop
%{_datadir}/services/kded/favicons.desktop
%{_datadir}/services/kded/homedirnotify.desktop
%{_datadir}/services/kded/khotkeys.desktop
%{_datadir}/services/kded/konqy_preloader.desktop
%{_datadir}/services/kded/kwrited.desktop
%{_datadir}/services/kded/mediamanager.desktop
%{_datadir}/services/kded/medianotifier.desktop
%{_datadir}/services/kded/remotedirnotify.desktop
%{_datadir}/services/kded/systemdirnotify.desktop
%{_datadir}/services/tdeprint_part.desktop
%{_datadir}/services/kfile_font.desktop
%{_datadir}/services/kfile_media.desktop
%{_datadir}/services/kfile_trash.desktop
%{_datadir}/services/kfile_trash_system.desktop
%{_datadir}/services/kfindpart.desktop
%{_datadir}/services/kfontviewpart.desktop
%{_datadir}/services/khelpcenter.desktop
%{_datadir}/services/kmanpart.desktop
%{_datadir}/services/konq_aboutpage.desktop
%{_datadir}/services/konq_detailedlistview.desktop
%{_datadir}/services/konq_iconview.desktop
%{_datadir}/services/konq_infolistview.desktop
%{_datadir}/services/konq_multicolumnview.desktop
%{_datadir}/services/konq_sidebartng.desktop
%{_datadir}/services/konq_textview.desktop
%{_datadir}/services/konq_treeview.desktop
%{_datadir}/services/kshorturifilter.desktop
%{_datadir}/services/ksplash.desktop
%{_datadir}/services/ksplashdefault.desktop
%{_datadir}/services/ksplashredmond.desktop
%{_datadir}/services/ksplashstandard.desktop
%{_datadir}/services/kuriikwsfilter.desktop
%{_datadir}/services/kurisearchfilter.desktop
%{_datadir}/services/kwrited.desktop
%{_datadir}/services/kxkb.desktop
%{_datadir}/services/ldap.protocol
%{_datadir}/services/ldaps.protocol
%{_datadir}/services/localdomainurifilter.desktop
%{_datadir}/services/mac.protocol
%{_datadir}/services/man.protocol
%{_datadir}/services/media.protocol
%{_datadir}/services/media_propsdlgplugin.desktop
%{_datadir}/services/nfs.protocol
%{_datadir}/services/nntp.protocol
%{_datadir}/services/nntps.protocol
%{_datadir}/services/nxfish.protocol
%{_datadir}/services/pop3.protocol
%{_datadir}/services/pop3s.protocol
%{_datadir}/services/print.protocol
%{_datadir}/services/printdb.protocol
%{_datadir}/services/programs.protocol
%{_datadir}/services/remote.protocol
%{_datadir}/services/searchproviders/*.desktop
%{_datadir}/services/settings.protocol
%{_datadir}/services/sftp.protocol
%{_datadir}/services/smtp.protocol
%{_datadir}/services/smtps.protocol
%{_datadir}/services/system.protocol
%{_datadir}/services/tar.protocol
%{_datadir}/services/textthumbnail.desktop
%{_datadir}/services/thumbnail.protocol
%{_datadir}/services/trash.protocol
%{_datadir}/services/useragentstrings/*.desktop
%{_datadir}/services/zip.protocol
%{_datadir}/servicetypes/findpart.desktop
%{_datadir}/servicetypes/konqaboutpage.desktop
%{_datadir}/servicetypes/konqpopupmenuplugin.desktop
%{_datadir}/servicetypes/ksplashplugins.desktop
%{_datadir}/servicetypes/searchprovider.desktop
%{_datadir}/servicetypes/terminalemulator.desktop
%{_datadir}/servicetypes/thumbcreator.desktop
%{_datadir}/servicetypes/uasprovider.desktop
%{_datadir}/sounds/*.wav
%{_datadir}/templates/.source/*.desktop
%{_datadir}/templates/*.desktop
%{_libdir}/trinity/kio_smb.*
%{_datadir}/apps/remoteview/smb-network.desktop
%{_datadir}/icons/hicolor/scalable/apps/tdeprintfax.svgz
%{_datadir}/mimelnk/application/x-smb-*.desktop
%{_datadir}/services/smb.protocol
%{_datadir}/templates/.source/HTMLFile.html
%{_datadir}/templates/.source/TextFile.txt
%{_bindir}/khc_beagle_index.pl
%{_bindir}/khc_beagle_search.pl
%{_bindir}/kxdglauncher
%{_libdir}/trinity/kcm_iccconfig.*
%{_libdir}/trinity/kgreet_pam.*
%{_libdir}/libkickoffsearch_interfaces.*
%{_datadir}/applications/kde/iccconfig.desktop
%{_datadir}/applications/kde/showdesktop.desktop
#%{_datadir}/doc/kde/HTML/en/kappfinder/man-kappfinder.1.docbook
%{_datadir}/mimelnk/media/*.desktop
%{_datadir}/servicetypes/kickoffsearchplugin.desktop

%{_bindir}/kdmtsak
%{_bindir}/kpager
%{_bindir}/kpersonalizer
%{_bindir}/krootbacking
%{_bindir}/ktip
%{_bindir}/tsak
%{_libdir}/trinity/kcm_displayconfig.la
%{_libdir}/trinity/kcm_displayconfig.so
%{_libdir}/trinity/kded_kdeintegration.la
%{_libdir}/trinity/kded_kdeintegration.so
%{_libdir}/trinity/ksplashunified.la
%{_libdir}/trinity/ksplashunified.so
%{_libdir}/trinity/plugins/integration/libqtkde.la
%{_libdir}/trinity/plugins/integration/libqtkde.so
%{_libdir}/trinity/plugins/integration/libqtkde.so.0
%{_libdir}/trinity/plugins/integration/libqtkde.so.0.0.0
%{_datadir}/applications/kde/displayconfig.desktop
%{_datadir}/applications/kde/kpager.desktop
%{_datadir}/applications/kde/kpersonalizer.desktop
%{_datadir}/applications/kde/ktip.desktop
%{_datadir}/applnk/System/kpersonalizer.desktop
%{_datadir}/applnk/Toys/ktip.desktop
%{_datadir}/applnk/Utilities/kpager.desktop
%{_datadir}/apps/kdewizard/pics/wizard_small.png
%{_datadir}/apps/kdewizard/tips
%{_datadir}/apps/kpersonalizer/pics/step1.png
%{_datadir}/apps/kpersonalizer/pics/step2.png
%{_datadir}/apps/kpersonalizer/pics/step3.png
%{_datadir}/apps/kpersonalizer/pics/step4.png
%{_datadir}/apps/kpersonalizer/pics/step5.png
%{_datadir}/apps/usb.ids
%{_datadir}/cmake/kicker.cmake
%{_datadir}/cmake/konqueror.cmake
%{_datadir}/cmake/libkonq.cmake
%{_datadir}/cmake/twin.cmake
%{_docdir}/kde/HTML/en/ksysguard/common
%{_docdir}/kde/HTML/en/ksysguard/index.cache.bz2
%{_docdir}/kde/HTML/en/ksysguard/index.docbook
%{_datadir}/icons/crystalsvg/16x16/apps/kpersonalizer.png
%{_datadir}/icons/crystalsvg/32x32/apps/kpersonalizer.png
%{_datadir}/icons/hicolor/128x128/apps/ktip.png
%{_datadir}/icons/hicolor/16x16/apps/kpager.png
%{_datadir}/icons/hicolor/16x16/apps/ktip.png
%{_datadir}/icons/hicolor/22x22/apps/kpager.png
%{_datadir}/icons/hicolor/22x22/apps/ktip.png
%{_datadir}/icons/hicolor/32x32/apps/kpager.png
%{_datadir}/icons/hicolor/32x32/apps/ktip.png
%{_datadir}/icons/hicolor/48x48/apps/kpager.png
%{_datadir}/icons/hicolor/48x48/apps/ktip.png
%{_datadir}/icons/hicolor/64x64/apps/ktip.png
%{_datadir}/icons/hicolor/scalable/apps/ktip.svgz
%{_datadir}/services/kded/kdeintegration.desktop
%{_datadir}/services/ksplashunified.desktop

%changelog
* Mon Mar 16 2009 Liu Di <liudidi@gmail.com> - 3.5.10-4
- 对包进行细分
- 整理 spec。
