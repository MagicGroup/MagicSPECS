%define _sysconfdir /etc
%define date 2013-07-02
%define with_gui 1
%define with_vdpau 1

%define svndate %(echo %date | sed -e 's/-//g')

Summary: MPlayer, the Movie Player for Linux.
Summary(zh_CN.UTF-8): MPlayer, Linux 下的媒体播放器
Name: mplayer
Version: 1.0svn%{svndate}
License: GPL
Release: 5%{?dist}
Group: Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
Url: http://www.mplayerhq.hu
Source0:http://www.mplayerhq.hu/MPlayer/releases/mplayer-export-snapshot.tar.bz2
Source1: mplayer.conf
Source2: Abyss-1.6.tar.bz2
Source3: AlienMind-1.2.tar.bz2
Source4: Blue-1.6.tar.bz2
Source5: handheld-1.0.tar.bz2
Source6: OSX-Brushed-2.3.tar.bz2
Source7: phony-1.1.tar.bz2
Source8: plastic-1.2.tar.bz2
Source9: PowerPlayer-1.1.tar.bz2
Source10: QuickSilver-1.0.tar.bz2
Source11: smoothwebby-1.1.tar.bz2
Source12: Terminator3-1.1.tar.bz2
Source13: WMP6-2.2.tar.bz2
Source14: xmmplayer-1.5.tar.bz2
# git clone --depth 1 git://git.videolan.org/ffmpeg.git ffmpeg
# 不使用系统的 ffmpeg
Source15: mplayer-ffmpeg.tar.xz
Patch2: mplayer-1.0svn20070805-i18n.patch
Patch3: mplayer_add_realmedia.patch
Patch4: mplayer-1.0desktop-zh_CN.patch
Patch5: MPlayer-0.90-playlist.patch
Patch6: MPlayer-1.0pre6a-fribidi.patch
#Patch7: MPlayer-1.0pre8-udev.patch
Patch8: mplayer_use_LOCALE_CJK.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)
Requires: aalib, lame, libdv, libdvdcss, libdvdread, libfame, libmad, xvidcore, SDL, libdvdnav

# ffmpeg now has its own rmvb codec
# mplayer-win32codec

BuildRequires: aalib-devel, lame-devel, libdv-devel, libdvdcss-devel, libdvdread-devel, libfame-devel, libmad, xvidcore, SDL-devel

%if %{with_vdpau}
BuildRequires: libvdpau-devel
%endif

%description
MPlayer is a movie player. It plays most video formats as well as DVDs.
Its big feature is the wide range of supported output drivers. There are also
nice antialiased shaded subtitles and OSD.

%description -l zh_CN.UTF-8
MPlayer 是一个电影播放器。它可以播放大多数视频格式。
它最大的特点是其输出驱动的广泛性。同时它还具有美观
的抗锯齿特效字幕和在屏显示(OSD)功能。

%package gui
Summary:  Mplayer's gui support
Summary(zh_CN): Mplayer 的 GUI 支持文件
Group: Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
Requires:	%name

%description gui
Mplayer's gui support

%description gui -l zh_CN
Mplayer 的 GUI 支持文件。


%prep

%setup -q -n mplayer-export-%{date} -a 15

%build

./configure \
        --prefix=%{_prefix} \
        --datadir=%{_datadir}/mplayer \
        --confdir=%{_sysconfdir}/mplayer \
        --mandir=%{_mandir} \
        --codecsdir=/usr/lib/codecs \
        --enable-faad            \
        --enable-libmpeg2          \
        --enable-dvdread            \
%if %{with_gui}
        --enable-gui \
%else
        --disable-gui \
%endif
        --enable-radio \
        --enable-radio-capture \
%ifnarch mips64el
        --enable-runtime-cpudetection \
%else
        --extra-cflags="-DARCH_MIPS64=1 -DHAVE_LOONGSON=0" \
%endif
%ifarch %{ix86}
        --enable-qtx \
%endif
        --enable-fbdev \
        --enable-tdfxfb \
        --enable-png \
        --enable-xmga \
        --enable-dga1 \
        --enable-dga2 \
%if %{with_vdpau}
        --enable-vdpau \
%endif
        --language=zh_CN,en \
        --enable-mga  \
        --enable-menu \
        --enable-dynamic-plugins \
        --enable-freetype \
        --enable-vm

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

install -d -m 755 %{buildroot}%{_sysconfdir}/%{name}
install -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/%{name}
install -m 644 etc/input.conf %{buildroot}%{_sysconfdir}/%{name}
install -m 644 etc/codecs.conf %{buildroot}%{_sysconfdir}/%{name}

%if %{with_gui}
# The Skins
install -d -m 755 %{buildroot}/%{_datadir}/mplayer/skins
pushd %{buildroot}/%{_datadir}/mplayer/skins
for FILE in \
Abyss-1.6.tar.bz2 \
AlienMind-1.2.tar.bz2 \
Blue-1.6.tar.bz2 \
handheld-1.0.tar.bz2 \
OSX-Brushed-2.3.tar.bz2 \
phony-1.1.tar.bz2 \
plastic-1.2.tar.bz2 \
PowerPlayer-1.1.tar.bz2 \
QuickSilver-1.0.tar.bz2 \
smoothwebby-1.1.tar.bz2 \
Terminator3-1.1.tar.bz2 \
WMP6-2.2.tar.bz2 \
xmmplayer-1.5.tar.bz2
do
	tar -jxf %{_sourcedir}/$FILE
done
rm -rf default
mv Abyss default
popd

# Fix eventual skin permissions :-( 
find %{buildroot}%{_datadir}/mplayer/skins -type d -exec chmod 755 {} \;
find %{buildroot}%{_datadir}/mplayer/skins -type f -exec chmod 644 {} \;
%endif

make install DESTDIR=%{buildroot}
# We do not need this directory as we have preseted the font information
rm -rf %{buildroot}/%{_datadir}/mplayer/font


# The font for the subtitles
#mkdir -p %{buildroot}/%{_datadir}/mplayer/font
#pushd %{buildroot}/usr/share/mplayer/font
	#tar -xzf  %{SOURCE4}
#popd
	# Fix eventual font permissions :-(
#find %{buildroot}/%{_datadir}/mplayer/font -type d -exec chmod 755 {} \;
#find %{buildroot}/%{_datadir}/mplayer/font -type f -exec chmod 644 {} \;


%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir} 
 

%files
%defattr(-, root, root, 755)
%{_sysconfdir}/mplayer/*.conf
%{_bindir}/mplayer
%{_bindir}/mencoder
%{_mandir}/man1/*.1*
%{_datadir}/man/zh_CN/man1/*.gz

%if %{with_gui}
%files gui
%defattr(-, root, root)
%{_bindir}/gmplayer
%{_datadir}/mplayer/skins/*
%{_datadir}/applications/mplayer.desktop
%{_datadir}/icons/hicolor/*/apps/mplayer.png
%endif

%changelog
* Fri Jul 05 2013 Liu Di <liudidi@gmail.com> - 1.0svn20130702-5
- 为 Magic 3.0 重建

* Tue Jan 15 2013 Liu Di <liudidi@gmail.com> - 1.0svn20120117-4
- 为 Magic 3.0 重建

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 1.0svn20120117-3
- 为 Magic 3.0 重建

* Mon Aug 6 2007 kde <athena_star {at} 163 {dot} com> - 1.0svn20070805-1mgc
- update to 1.0svn20070805
- add many skins
- add some items in mplayer.conf and give some zh_CN translation
- update the realmedia and CJK patch

* Fri Feb 09 2007 Liu Di <liudidi@gmail.com> - 1.0rc1-1mgc
- update to 1.0rc1

* Wed Aug 10 2006 nicholas <abcxyz54321@163.com>
-update to 1.0pre8
* Wed Jun  7 2006 nicholas <abcxyz54321@163.com>
-update to CVS 20060607
* Wed Nov 30 2005 KanKer <kanker@163.com>
- fix sub font bug
* Tue Nov 24 2005 KanKer <kanker@163.com>
- update to mplayer1.0pre7try2
* Mon Apr 18 2005 tingxx<tingxx@21cn.com>
- update to mplayer1.0pre7
* Mon Jan 3 2005 tingxx<tingxx@21cn.com>
- modify the subauto patch and add the rmvb to the file list in Gtk open dialog. 
* Fri Dec 31 2004 tingxx<tingxx@21cn.com>
- modify spec according to yqh.
