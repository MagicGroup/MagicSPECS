%define debug 0

%define final 1

%define qt_version 3.3.8

%define libtool 1
%define alsa 1
%define juk 1
%define arts 1
%define prefix /usr
%define relver 529030
%define _iconsdir %_datadir/icons

%define git 1
%define gitdate 20111223

Summary: Multimedia applications for the K Desktop Environment (KDE). 
Summary(zh_CN.UTF-8): K 桌面环境 (KDE) 的多媒体程序。
Name:          tdemultimedia
Version:       3.5.14
%if %{git}
Release:	0.git%{?gitdate}%{?dist}
%else
Release:       0.1%{?dist}
%endif
License:     GPL
URL: http://www.kde.org
Group:         Applications/Multimedia
Group(zh_CN.UTF-8):  应用程序/多媒体
BuildRoot:   %{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)
%if %{git}
Source:	%{name}-git%{gitdate}.tar.xz
%else
Source:    ftp://ftp.kde.org/pub/kde/stable/%{version}/src/%{name}-%{version}.tar.bz2
%endif
Patch: kdemultimedia-kmix.patch
Patch1: tdemultimedia-libtool.patch
Patch3: k-mp3meta.patch
Patch4: juk-3.3-cjk.patch
Patch5: kdemultimedia-3.2.2-mpeglib-buffer.patch
Patch6: kdemultimedia-newarts.patch
Patch7: kdemultimedia-tunepimp.patch
Patch8: tdemultimedia-arts.patch
Requires: qt, arts, tdelibs, tdebase, id3lib, xine-lib

BuildRequires: zlib-devel
BuildRequires: kdebase-devel >= %{version}
BuildRequires: libjpeg-devel
BuildRequires: gcc-c++
BuildRequires: glibc-devel
BuildRequires: perl
BuildRequires: libvorbis-devel
BuildRequires: audiofile-devel
BuildRequires: glib2-devel
BuildRequires: libmng-devel
%if %{alsa}
BuildRequires: alsa-lib-devel >= 1.0.2
%endif
%if %{juk}
BuildRequires: taglib => 1.3
%endif
%if %{juk}
Obsoletes: juk
%endif

%description
The K Desktop Environment (KDE) is a GUI desktop for the X Window
System. The kdemultimedia package contains multimedia applications for
KDE, including:

  kmid, a midi player
  kmidi, a midi-to-wav player/converter
  kmix, an audio mixer
  arts, additional functionality for the aRts sound system
  kaboodle, a media player
  noatun, a media player
  krec, a recording tool
  kscd, an Audio-CD player
  kaudiocreator, a graphical frontend for audio file creation 

%description -l zh_CN.UTF-8
K 桌面环境 (KDE) 是一个 X 窗口系统的 GUI 桌面。kdemultimedia 包
包含了 KDE 的多媒体应用程序，包括 ：
  
  kmid, 一个 midi 播放器
  kmidi, 一个 midi 到 wav 播放器/转换器
  kmix, 一个声音混音器
  arts, aRts 声音系统的附加功能
  kaboodle, 一个媒体播放器
  noatun, 一个媒体播放器
  krec, 一个录音工具
  kscd, 一个音频 CD 播放器
  kaudiocreator, 一个创建声音文件的图形前端

%package common
Summary:        Common files for kdemultimedia
Summary(zh_CN.UTF-8): %{name} 的公用文件
Group:          Applications/Multimedia
Group(zh_CN.UTF-8):  应用程序/多媒体
Requires:       arts, vorbis-tools
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils
Requires: magic-kde-config
Requires: %{name}-kmix
Requires: %{name}-arts

%description common
Common files for kdemultimedia

%description common -l zh_CN.UTF-8
%{name} 的公用文件。

#----------------------------------------------------------------------------------

%package juk
Summary:       JuK is a jukebox and music manager for the KDE desktop
Summary(zh_CN.UTF-8): Juk 是 KDE 桌面下的一个音乐播放和管理程序
Group:         Applications/Multimedia
Group(zh_CN.UTF-8):  应用程序/多媒体
Requires:      tdemultimedia-common = %version-%release
Provides:       juk
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils
 
%description juk
JuK is a jukebox and music manager for the KDE desktop similar to
jukebox software on other platforms such as iTunes or RealOne.
Its features include support for Ogg Vorbis and MP3 formats,
tag editing support for both formats (including ID3v2 for MP3 files),
output to aRts or GStreamer, multiple playlists, and lots of other
groovy stuff.

%description juk -l zh_CN.UTF-8
Juk 是 KDE 桌面下的一个音乐播放和管理程序，类似其它平台上的同类软件，
比如 iTunes 和 RealOne。

#---------------------------------------------------------------------------------

%package kmix
Summary:       Kmix, kmixctrl program
Summary(zh_CN.UTF-8): KDE 下的音量调节程序
Group:          Applications/Multimedia
Group(zh_CN.UTF-8):  应用程序/多媒体
Provides:       kmix, kmixctrl
Requires:       arts
Requires:        alsa-utils
Requires:       %name-common = %version-%release 

%description kmix
The audio mixer as a standalone program and Kicker applet

%description kmix -l zh_CN.UTF-8
KDE 下的音量调节程序。

#----------------------------------------------------------------------------------

%package krec
Summary:       Krec program
Summary(zh_CN.UTF-8): KDE 下的录音程序
Group:          Applications/Multimedia
Group(zh_CN.UTF-8):  应用程序/多媒体
Requires:       %name-common = %version-%release
Provides:       krec
 
%description krec
A recording frontend using aRts

%description krec -l zh_CN.UTF-8
使用 aRts 的录音前端。

#---------------------------------------------------------------------------------
%package kaudiocreator
Summary:       Kaudiocreator program
Summary(zh_CN.UTF-8): KDE 下的 CD 抓音轨工具
Group:         Applications/Multimedia
Group(zh_CN.UTF-8):  应用程序/多媒体
Provides:       kaudiocreator
Requires:       arts
Requires:       %name-common = %version-%release
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils

%description kaudiocreator
CD ripper and audio encoder frontend.

%description kaudiocreator -l zh_CN.UTF-8
CD音轨抓取/编码软件。辅助Lame、oggenc、FLAC等第三方工具可以将您喜爱的CD专辑以压缩格式转储到外部可写介质上，编码格式可采用MP3、Ogg Vorbis、FLAC三者之一。KAudioCreater支持通过互联网上的CDDB服务器查询CD专辑信息，对正规出版的一些专辑较为有用。

#----------------------------------------------------------------------------------

%package kscd
Summary:       Kscd program
Summary(zh_CN.UTF-8): KDE 下载的 CD 播放器
Group:         Applications/Multimedia
Group(zh_CN.UTF-8):  应用程序/多媒体
Provides:       kscd
Requires:       arts
Requires:       %name-common = %version-%release
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils
 
%description kscd
A CD player with an interface to the internet CDDB database

%description kscd -l zh_CN.UTF-8
带有互联网 CDDB 数据库接口的 CD 播放器。

#-------------------------------------------------------------------------------

%package kmid
Summary:       Kmid program
Summary(zh_CN.UTF-8): KDE 下的 midi 播放器
Group:         Applications/Multimedia
Group(zh_CN.UTF-8):  应用程序/多媒体
Provides: kmid
Provides: kmidi
Requires:       %name-common = %version-%release
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils
 
%description kmid
Kmid program

%description kmid -l zh_CN.UTF-8
KDE 下的 MIDI 播放器。

#---------------------------------------------------------------------------------

%package kaboodle
Summary: Kaboodle program
Summary(zh_CN.UTF-8): 轻量级媒体播放器
Group: Applications/Multimedia
Group(zh_CN.UTF-8):  应用程序/多媒体
Provides: kaboodle
Requires: arts
Requires:       %name-common = %version-%release
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils
 
%description kaboodle
Light media player

%description kaboodle -l zh_CN.UTF-8
轻量级媒体播放器。

#--------------------------------------------------------------------------------

%package arts
Summary: Arts synth control programs
Summary(zh_CN.UTF-8): Arts 同步控制程序
Group: 　Applications/Multimedia
Group(zh_CN.UTF-8):  应用程序/多媒体
Requires: %name-common = %version-%release
 
%description arts
A synthesizer control programs

%description arts -l zh_CN.UTF-8
一个同步控制程序。

#--------------------------------------------------------------------------------

%package noatun
Summary:       Noatun program
Summary(zh_CN.UTF-8): 媒体播放程序
Group:         Applications/Multimedia
Group(zh_CN.UTF-8):  应用程序/多媒体
Requires:       %name-common = %version-%release
Provides:       noatun
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils
 
%description noatun
A multimedia player for sound and movies, very extensible due to
it's plugin interface

%description noatun -l zh_CN.UTF-8
播放音频和视频的多媒体播放器，有可扩展的插件接口。

#-------------------------------------------------------------------------------

%package devel
Summary: Development files for aRts plugins
Summary(zh_CN.UTF-8): aRts 插件的开发文件
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: kdebase-devel

%description devel
Development files for aRts and noatun plugins.
Install kdemultimedia-devel if you wish to develop or compile any
applications using aRtsbuilder, aRtsmidi, aRtskde, aRts modules or
noatun plugins.

%description devel -l zh_CN.UTF-8
aRts 和 noatun 插件的开发文件。
如果你想开发或编译使用 aRtsbuilder, aRtsmidi, aRtskde, aRts 模块
或 noatun 插件的应用程序，你需要安装 kdemultimedia-devel 包。

%prep
%if %{git}
%setup -q -n %{name}-git%{gitdate}
%else
%setup -q -n %{name}-%{version}
%endif
%patch -p1
%patch1 -p1
#%patch3 -p1
#%patch4 -p1
%patch5 -p1
#此补丁是有问题的，lgsl是不存在的
#%patch6 -p1
#%patch7 -p1
%patch8 -p1

%Build
make -f admin/Makefile.common

unset QTDIR || : ; . /etc/profile.d/qt.sh
FLAGS="$RPM_OPT_FLAGS -DNDEBUG"
export KDEDIR=%{prefix}
#export PATH=%{prefix}/bin:$PATH
export CFLAGS="$FLAGS"
#export CXXFLAGS="$FLAGS -fno-use-cxa-atexit"

%if %{arts}
export CFLAGS="$CFLAGS `artsc-config --cflags`"
export CXXFLAGS="$CXXFLAGS `artsc-config --cflags`"
export CPPFLAGS="$CPPFLAGS `artsc-config --cflags`"
export LDFLAGS="$LDFLAGS `artsc-config --libs`"
%endif
#CFLAGS="$CFLAGS -lXext -lkparts -lgsl -lsoundserver_idl -lkmedia2_idl -lartsflow_idl -lmcop -ldl -lkdecore -lkdeui -lkdesu -lX11 -lDCOP -lkio -lkdefx" \
#CXXFLAGS="$CXXFLAGS -lXext -lkparts -lgsl -lsoundserver_idl -lkmedia2_idl -lartsflow_idl -lmcop -ldl -lkdecore -lkdeui -lkdesu -lX11 -lDCOP -lkio -lkdefx" \
%configure --prefix=%{prefix} \
           --with-qt-libraries=$QTDIR/lib \
           --disable-motif \
	   --enable-closure \
           --with-motif-includes=none \
           --with-motif-libraries=none \
           --disable-debug \
           --without-debug \
%if %{arts} == 0
           --without-arts \
%endif
%if %{alsa}
           --with-alsa \
%if %{arts}
           --with-arts-alsa \
%endif
%endif
           --disable-rpath \
           --with-xinerama \
%if %{final}
           --enable-final \
%endif
           --disable-xaw

# use unsermake instead of make, don't use %{?_smp_mflags}
make

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install
# make -C juk install DESTDIR=%{buildroot}
mkdir -p %{buildroot}%{_datadir}/autostart
cp -f %{buildroot}/usr/share/applications/kde/kmix.desktop %{buildroot}/usr/share/autostart

# find %{buildroot}/%{_libdir}/ -name *.la -exec rm -rf {} \;

%files
%defattr(-,root,root)

%files devel
%defattr(-,root,root,-)
%{_includedir}/*

%files juk
%defattr(-,root,root,-)
%doc %_docdir/HTML/en/juk
%_bindir/juk
%_datadir/applications/kde/juk.desktop
%_iconsdir/*/*/*/juk*
%dir %_datadir/apps/juk
%_datadir/apps/juk/*
%_datadir/apps/konqueror/servicemenus/jukservicemenu.desktop

%files kmix
%defattr(-,root,root,-)
%_bindir/kmix
%_bindir/kmixctrl
%doc %_docdir/HTML/en/kmix
%_libdir/trinity/kmix*.so
%_libdir/trinity/kmix*.la
%_datadir/autostart/restore_kmix_volumes.desktop
%_iconsdir/*/*/*/kmix*
%_datadir/services/kmixctrl_restore.desktop
%_datadir/applications/kde/kmix.desktop
%dir %_datadir/apps/kmix/
%_datadir/apps/kmix/*
%_datadir/apps/kicker/applets/kmixapplet.desktop
%_libdir/libtdeinit_kmix.*
%_libdir/libtdeinit_kmixctrl.*

%files krec
%defattr(-,root,root,-)
%doc %_docdir/HTML/en/krec
%_bindir/krec
%dir %_datadir/apps/krec/
%_datadir/apps/krec/*
%_datadir/applications/kde/krec.desktop
%_iconsdir/*/*/*/krec.*
%_libdir/trinity/kcm_krec_files.*
%_libdir/trinity/krec.*
%_libdir/trinity/kcm_krec.*
%_libdir/trinity/libkrecexport_*
%_libdir/libtdeinit_krec.*
%_datadir/services/krec_*
%_datadir/services/kcm_krec*
%_datadir/servicetypes/krec_*

%files kscd
%defattr(-,root,root,-)
%doc %_docdir/HTML/en/kscd
%_bindir/kscd
%_bindir/workman2cddb.pl
%_iconsdir/*/*/*/kscd*
%_datadir/config.kcfg/kscd.kcfg
%_datadir/config.kcfg/libkcddb.kcfg
%_datadir/applications/kde/libkcddb.desktop
%_datadir/applications/kde/kscd.desktop
%dir %_datadir/apps/kscd/
%_datadir/apps/kscd/*
%_datadir/apps/profiles/kscd.profile.xml
%_datadir/apps/kconf_update/kcmcddb-emailsettings.upd
%_libdir/trinity/kcm_cddb.*
%_datadir/mimelnk/text/xmcd.desktop

%files kmid
%defattr(-,root,root,-)
%doc %_docdir/HTML/en/kmid
%_bindir/kmid
%_iconsdir/*/*/*/kmid.*
%_libdir/trinity/libkmidpart.*
%dir %_datadir/apps/kmid/
%_datadir/apps/kmid/*
%_datadir/mimelnk/audio/x-karaoke.desktop
%_datadir/servicetypes/audiomidi.desktop
%_datadir/applications/kde/kmid.desktop

%files kaboodle
%defattr(-,root,root,-)
%doc %_docdir/HTML/en/kaboodle
%_bindir/kaboodle
%_datadir/services/kaboodle*
%_datadir/applications/kde/kaboodle.desktop
%_iconsdir/*/*/*/kaboodle*
%_libdir/trinity/libkaboodlepart.*
%dir %_datadir/apps/kaboodle/
%_datadir/apps/kaboodle/*

%files arts
%defattr(-,root,root,-)
%_bindir/artsbuilder
%_bindir/artscontrol
%_bindir/midisend
%dir %_datadir/apps/artsbuilder
%_datadir/apps/artsbuilder/*
%dir %_datadir/apps/artscontrol
%_datadir/apps/artscontrol/*
%doc %_docdir/HTML/en/artsbuilder
%_datadir/apps/kicker/applets/artscontrolapplet.desktop
%_datadir/mimelnk/application/x-artsbuilder.desktop
%_datadir/applications/kde/artsbuilder.desktop
%_datadir/applications/kde/artscontrol.desktop
%dir %_libdir/mcop/Arts
%_libdir/mcop/Arts/*
%_libdir/mcop/artsmodulescommon.*
%_libdir/mcop/artsbuilder.*
%_libdir/mcop/artsmodules.*
%_libdir/mcop/artsmodulesmixers.*
%_libdir/mcop/artsmodulessynth.*
%_libdir/mcop/artsmoduleseffects.*
%_libdir/mcop/artsmidi.*
%_libdir/mcop/artsgui.*
%_libdir/mcop/akodeFFMPEGPlayObject.mcopclass
%_libdir/libartsbuilder.la
%_libdir/libartsbuilder.so.*
%_libdir/libartscontrolapplet.la
%_libdir/libartscontrolapplet.so.*
%_libdir/libartscontrolsupport.la
%_libdir/libartscontrolsupport.so.*
%_libdir/libartsgui_idl.la
%_libdir/libartsgui_idl.so.*
%_libdir/libartsgui_kde.la
%_libdir/libartsgui_kde.so.*
%_libdir/libartsgui.la
%_libdir/libartsgui.so.*
%_libdir/libartsmidi_idl.la
%_libdir/libartsmidi_idl.so.*
%_libdir/libartsmidi.la
%_libdir/libartsmidi.so.*
%_libdir/libartsmodulescommon.la
%_libdir/libartsmodulescommon.so.*
%_libdir/libartsmoduleseffects.la
%_libdir/libartsmoduleseffects.so.*
%_libdir/libartsmodules.la
%_libdir/libartsmodulesmixers.la
%_libdir/libartsmodulesmixers.so.*
%_libdir/libartsmodules.so.*
%_libdir/libartsmodulessynth.la
%_libdir/libartsmodulessynth.so.*
%_libdir/libartsbuilder.so
%_libdir/libartscontrolapplet.so
%_libdir/libartscontrolsupport.so
%_libdir/libartsgui_idl.so
%_libdir/libartsgui_kde.so
%_libdir/libartsgui.so
%_libdir/libartsmidi_idl.so
%_libdir/libartsmidi.so
%_libdir/libartseffects.so
%_libdir/libartsmodulescommon.so
%_libdir/libartsmoduleseffects.so
%_libdir/libartsmodules.so
%_libdir/libartsmodulesmixers.so
%_libdir/libartsmodulessynth.so


%files noatun
%defattr(-,root,root,-)
%_bindir/noatun
%doc %_docdir/HTML/en/noatun
%dir %_datadir/apps/noatun
%_datadir/apps/noatun/*
%_libdir/trinity/noatun*.*
%_iconsdir/*/*/*/noatun*
%_datadir/applications/kde/noatun.desktop
%_datadir/mimelnk/interface/x-winamp-skin.desktop
%{_libdir}/kconf_update_bin/noatun20update
%_datadir/apps/kconf_update/noatun.upd
%dir %_libdir/mcop/Noatun/
%_libdir/mcop/Noatun/*
%_libdir/mcop/artseffects.mcopclass
%_libdir/mcop/VoiceRemoval.mcopclass
%_libdir/mcop/artseffects.mcoptype
%_libdir/mcop/noatunarts.mcopclass
%_libdir/mcop/winskinvis.mcopclass
%_libdir/mcop/ExtraStereoGuiFactory.mcopclass
%_libdir/mcop/noatunarts.mcoptype
%_libdir/mcop/winskinvis.mcoptype
%_libdir/mcop/ExtraStereo.mcopclass
%_libdir/mcop/RawWriter.mcopclass
%_libdir/libartseffects.la*
%_libdir/libnoatuncontrols.so.*
%_libdir/libnoatuntags.so.*
%_libdir/libnoatunarts.la*
%_libdir/libnoatun.la*
%_libdir/libwinskinvis.la*
%_libdir/libnoatun.so.*
%_libdir/libnoatuncontrols.la*
%_libdir/libnoatuntags.la*
%_libdir/libtdeinit_noatun.la
%_libdir/libtdeinit_noatun.so
%_libdir/libnoatunarts.so
%_libdir/libnoatuncontrols.so
%_libdir/libnoatun.so
%_libdir/libnoatuntags.so
%_libdir/libwinskinvis.so

%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files common
%defattr(-,root,root)
/etc/xdg/menus/applications-merged/kde-multimedia-music.menu
#/usr/bin/mpeglibartsplay
#/usr/bin/yaf-cdda
#/usr/bin/yaf-mpgplay
#/usr/bin/yaf-splay
#/usr/bin/yaf-tplay
#/usr/bin/yaf-vorbis
#/usr/bin/yaf-yuv
/usr/lib/trinity/kfile_au.la
/usr/lib/trinity/kfile_au.so
/usr/lib/trinity/kfile_avi.la
/usr/lib/trinity/kfile_avi.so
/usr/lib/trinity/kfile_flac.la
/usr/lib/trinity/kfile_flac.so
/usr/lib/trinity/kfile_m3u.la
/usr/lib/trinity/kfile_m3u.so
/usr/lib/trinity/kfile_mp3.la
/usr/lib/trinity/kfile_mp3.so
/usr/lib/trinity/kfile_mpc.la
/usr/lib/trinity/kfile_mpc.so
/usr/lib/trinity/kfile_mpeg.la
/usr/lib/trinity/kfile_mpeg.so
/usr/lib/trinity/kfile_ogg.la
/usr/lib/trinity/kfile_ogg.so
/usr/lib/trinity/kfile_sid.la
/usr/lib/trinity/kfile_sid.so
/usr/lib/trinity/kfile_theora.la
/usr/lib/trinity/kfile_theora.so
/usr/lib/trinity/kfile_wav.la
/usr/lib/trinity/kfile_wav.so
/usr/lib/trinity/videothumbnail.la
/usr/lib/trinity/videothumbnail.so
/usr/lib/libarts_akode.la
/usr/lib/libarts_akode.so
/usr/lib/libarts_akode.so.0
/usr/lib/libarts_akode.so.0.0.0
/usr/lib/libarts_audiofile.la
/usr/lib/libarts_audiofile.so
/usr/lib/libarts_audiofile.so.0
/usr/lib/libarts_audiofile.so.0.0.0
/usr/lib/libarts_xine.la
/usr/lib/libarts_xine.so
/usr/lib/libarts_xine.so.0
/usr/lib/libarts_xine.so.0.0.0
/usr/lib/libkcddb.la
/usr/lib/libkcddb.so
/usr/lib/libkcddb.so.1
/usr/lib/libkcddb.so.1.0.0
/usr/lib/libkmidlib.la
/usr/lib/libkmidlib.so
/usr/lib/libkmidlib.so.0
/usr/lib/libkmidlib.so.0.0.0
/usr/lib/mcop/akodeMPCPlayObject.mcopclass
/usr/lib/mcop/akodeMPEGPlayObject.mcopclass
/usr/lib/mcop/akodePlayObject.mcopclass
/usr/lib/mcop/akodeSpeexStreamPlayObject.mcopclass
/usr/lib/mcop/akodeVorbisStreamPlayObject.mcopclass
/usr/lib/mcop/akodeXiphPlayObject.mcopclass
/usr/lib/mcop/akodearts.mcopclass
/usr/lib/mcop/akodearts.mcoptype
/usr/lib/mcop/audiofilearts.mcopclass
/usr/lib/mcop/audiofilearts.mcoptype
/usr/lib/mcop/xineAudioPlayObject.mcopclass
/usr/lib/mcop/xineVideoPlayObject.mcopclass
/usr/share/apps/kappfinder/apps/Multimedia/ams.desktop
/usr/share/apps/kappfinder/apps/Multimedia/amsynth.desktop
/usr/share/apps/kappfinder/apps/Multimedia/ardour.desktop
/usr/share/apps/kappfinder/apps/Multimedia/djplay.desktop
/usr/share/apps/kappfinder/apps/Multimedia/ecamegapedal.desktop
/usr/share/apps/kappfinder/apps/Multimedia/freebirth.desktop
/usr/share/apps/kappfinder/apps/Multimedia/freqtweak.desktop
/usr/share/apps/kappfinder/apps/Multimedia/galan.desktop
/usr/share/apps/kappfinder/apps/Multimedia/hydrogen.desktop
/usr/share/apps/kappfinder/apps/Multimedia/jack-rack.desktop
/usr/share/apps/kappfinder/apps/Multimedia/jamin.desktop
/usr/share/apps/kappfinder/apps/Multimedia/meterbridge.desktop
/usr/share/apps/kappfinder/apps/Multimedia/mixxx.desktop
/usr/share/apps/kappfinder/apps/Multimedia/muse.desktop
/usr/share/apps/kappfinder/apps/Multimedia/qjackctl.desktop
/usr/share/apps/kappfinder/apps/Multimedia/qsynth.desktop
/usr/share/apps/kappfinder/apps/Multimedia/vkeybd.desktop
/usr/share/apps/kappfinder/apps/Multimedia/zynaddsubfx.desktop
/usr/share/apps/konqueror/servicemenus/audiocd_play.desktop
/usr/share/apps/videothumbnail/sprocket-large.png
/usr/share/apps/videothumbnail/sprocket-medium.png
/usr/share/apps/videothumbnail/sprocket-small.png
/usr/share/autostart/kmix.desktop
/usr/share/desktop-directories/kde-multimedia-music.directory
/usr/share/doc/HTML/en/kaudiocreator/cdconfiguration.png
/usr/share/doc/HTML/en/kaudiocreator/cddbconfigurationlookup.png
/usr/share/doc/HTML/en/kaudiocreator/cddbconfigurationsubmit.png
/usr/share/doc/HTML/en/kaudiocreator/cdinserted.png
/usr/share/doc/HTML/en/kaudiocreator/common
/usr/share/doc/HTML/en/kaudiocreator/confirmartistcarryover.png
/usr/share/doc/HTML/en/kaudiocreator/encoderconfiguration.png
/usr/share/doc/HTML/en/kaudiocreator/encodernotfound.png
/usr/share/doc/HTML/en/kaudiocreator/entersong1.png
/usr/share/doc/HTML/en/kaudiocreator/generalconfiguration.png
/usr/share/doc/HTML/en/kaudiocreator/index.cache.bz2
/usr/share/doc/HTML/en/kaudiocreator/index.docbook
/usr/share/doc/HTML/en/kaudiocreator/jobcontrol.png
/usr/share/doc/HTML/en/kaudiocreator/jobshavestarted.png
/usr/share/doc/HTML/en/kaudiocreator/kaudiocreatormainwindow800.png
/usr/share/doc/HTML/en/kaudiocreator/lameconfiguration.png
/usr/share/doc/HTML/en/kaudiocreator/readytorip.png
/usr/share/doc/HTML/en/kaudiocreator/ripperconfiguration.png
/usr/share/doc/HTML/en/kaudiocreator/rippingandencoding.png
/usr/share/doc/HTML/en/kaudiocreator/rippingandencoding2.png
/usr/share/doc/HTML/en/kaudiocreator/setalbumcategory.png
/usr/share/doc/HTML/en/kaudiocreator/startalbumeditor.png
/usr/share/doc/HTML/en/kioslave/audiocd.docbook
/usr/share/icons/crystalsvg/128x128/actions/artsaudiomanager.png
/usr/share/icons/crystalsvg/128x128/actions/artsenvironment.png
/usr/share/icons/crystalsvg/128x128/actions/artsfftscope.png
/usr/share/icons/crystalsvg/128x128/actions/artsmediatypes.png
/usr/share/icons/crystalsvg/128x128/actions/artsmidimanager.png
/usr/share/icons/crystalsvg/16x16/actions/artsaudiomanager.png
/usr/share/icons/crystalsvg/16x16/actions/artsbuilderexecute.png
/usr/share/icons/crystalsvg/16x16/actions/artsenvironment.png
/usr/share/icons/crystalsvg/16x16/actions/artsfftscope.png
/usr/share/icons/crystalsvg/16x16/actions/artsmediatypes.png
/usr/share/icons/crystalsvg/16x16/actions/artsmidimanager.png
/usr/share/icons/crystalsvg/22x22/actions/artsaudiomanager.png
/usr/share/icons/crystalsvg/22x22/actions/artsbuilderexecute.png
/usr/share/icons/crystalsvg/22x22/actions/artsenvironment.png
/usr/share/icons/crystalsvg/22x22/actions/artsfftscope.png
/usr/share/icons/crystalsvg/22x22/actions/artsmediatypes.png
/usr/share/icons/crystalsvg/22x22/actions/artsmidimanager.png
/usr/share/icons/crystalsvg/32x32/actions/artsaudiomanager.png
/usr/share/icons/crystalsvg/32x32/actions/artsenvironment.png
/usr/share/icons/crystalsvg/32x32/actions/artsfftscope.png
/usr/share/icons/crystalsvg/32x32/actions/artsmediatypes.png
/usr/share/icons/crystalsvg/32x32/actions/artsmidimanager.png
/usr/share/icons/crystalsvg/48x48/actions/artsaudiomanager.png
/usr/share/icons/crystalsvg/48x48/actions/artsenvironment.png
/usr/share/icons/crystalsvg/48x48/actions/artsfftscope.png
/usr/share/icons/crystalsvg/48x48/actions/artsmediatypes.png
/usr/share/icons/crystalsvg/48x48/actions/artsmidimanager.png
/usr/share/icons/crystalsvg/64x64/actions/artsaudiomanager.png
/usr/share/icons/crystalsvg/64x64/actions/artsenvironment.png
/usr/share/icons/crystalsvg/64x64/actions/artsfftscope.png
/usr/share/icons/crystalsvg/64x64/actions/artsmediatypes.png
/usr/share/icons/crystalsvg/64x64/actions/artsmidimanager.png
/usr/share/icons/crystalsvg/scalable/actions/artsaudiomanager.svgz
/usr/share/icons/crystalsvg/scalable/actions/artsenvironment.svgz
/usr/share/icons/crystalsvg/scalable/actions/artsfftscope.svgz
/usr/share/icons/crystalsvg/scalable/actions/artsmediatypes.svgz
/usr/share/icons/crystalsvg/scalable/actions/artsmidimanager.svgz
/usr/share/icons/hicolor/128x128/apps/artscontrol.png
/usr/share/icons/hicolor/16x16/apps/artsbuilder.png
/usr/share/icons/hicolor/16x16/apps/artscontrol.png
/usr/share/icons/hicolor/22x22/apps/artscontrol.png
/usr/share/icons/hicolor/32x32/apps/artscontrol.png
/usr/share/icons/hicolor/48x48/apps/artscontrol.png
/usr/share/icons/hicolor/64x64/apps/artscontrol.png
/usr/share/icons/hicolor/scalable/apps/artsbuilder.svgz
/usr/share/icons/hicolor/scalable/apps/artscontrol.svgz
/usr/share/services/kfile_au.desktop
/usr/share/services/kfile_avi.desktop
/usr/share/services/kfile_flac.desktop
/usr/share/services/kfile_m3u.desktop
/usr/share/services/kfile_mp3.desktop
/usr/share/services/kfile_mpc.desktop
/usr/share/services/kfile_mpeg.desktop
/usr/share/services/kfile_ogg.desktop
/usr/share/services/kfile_sid.desktop
/usr/share/services/kfile_theora.desktop
/usr/share/services/kfile_wav.desktop
/usr/share/services/videothumbnail.desktop
   /usr/bin/mpeglibartsplay
   /usr/bin/yaf-cdda
   /usr/bin/yaf-mpgplay
   /usr/bin/yaf-splay
   /usr/bin/yaf-tplay
   /usr/bin/yaf-vorbis
   /usr/bin/yaf-yuv
   /usr/lib/libarts_mpeglib-0.3.0.so.0
   /usr/lib/libarts_mpeglib-0.3.0.so.0.0.3
   /usr/lib/libarts_mpeglib.la
   /usr/lib/libarts_mpeglib.so
   /usr/lib/libarts_splay.la
   /usr/lib/libarts_splay.so
   /usr/lib/libarts_splay.so.0
   /usr/lib/libarts_splay.so.0.0.0
   /usr/lib/libmpeg-0.3.0.so
   /usr/lib/libmpeg.la
   /usr/lib/libmpeg.so
   /usr/lib/libyafcore.la
   /usr/lib/libyafcore.so
   /usr/lib/libyafxplayer.la
   /usr/lib/libyafxplayer.so
   /usr/lib/mcop/CDDAPlayObject.mcopclass
   /usr/lib/mcop/MP3PlayObject.mcopclass
   /usr/lib/mcop/NULLPlayObject.mcopclass
   /usr/lib/mcop/OGGPlayObject.mcopclass
   /usr/lib/mcop/SplayPlayObject.mcopclass
   /usr/lib/mcop/WAVPlayObject.mcopclass
