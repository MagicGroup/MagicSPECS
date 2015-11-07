# TODO, sometime, maybe:
# - libstk:  http://www.libstk.net/ - probably not, see 1.1.5 ChangeLog
# - drop the opengl video out plugin?

%define         plugin_abi  2.5
%define         codecdir    %{_libdir}/codecs

%ifarch %{ix86}
    %define     have_vidix  1
%else
    %define     have_vidix  0
%endif # ix86

%ifarch %{arm}
%define _without_directfb 1
%endif

%define _disable_v4l1 0

%define _without_esound 1

Summary:        A multimedia engine
Summary(zh_CN.UTF-8): 多媒体引擎
Name:           xine-lib
Version:	1.2.6
Release:        3%{?dist}
License:        GPLv2+
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL:            http://www.xine-project.org/
# The tarball is generated from the upstream tarball using
# the script in SOURCE1. It prunes potentially patented code
#Source0:        http://downloads.sourceforge.net/xine/xine-lib-%{version}.tar.xz
Source0:        http://sourceforge.net/projects/xine/files/xine-lib/%{version}/xine-lib-%{version}.tar.xz
Source1:        xine-lib-cleanup-sources.sh
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Patch0:         xine-lib-1.1.19-no_autopoint.patch
Patch1:         xine-lib-1.1.4-optflags.patch
# http://bugzilla.redhat.com/470568
Patch8:         xine-lib-1.1.17-avsync_hack.patch
# http://bugzilla.redhat.com/477226
Patch9:         xine-lib-1.1.16.2-multilib.patch

Patch10:	xine-lib-1.2.1-v4l.patch
Patch11:        xine-lib-1.2.2-fix-non-x86-build.diff

Provides:         xine-lib(plugin-abi) = %{plugin_abi}
%{?_isa:Provides: xine-lib(plugin-abi)%{?_isa} = %{plugin_abi}}

BuildRequires:  autoconf automake libtool
# X11
BuildRequires:  libX11-devel
BuildRequires:  libXv-devel
BuildRequires:  libXinerama-devel
BuildRequires:  libXvMC-devel
BuildRequires:  libGLU-devel
BuildRequires:  libv4l-devel
BuildRequires:  libxcb-devel
# Video
BuildRequires:  SDL-devel
BuildRequires:  libtheora-devel
BuildRequires:  libmng-devel
BuildRequires:  aalib-devel >= 1.4
BuildRequires:  libcaca-devel >= 0.99-0.5.beta14
BuildRequires:	ffmpeg-devel
%if 0%{!?_without_directfb:1}
BuildRequires:  directfb-devel
%endif # directfb
BuildRequires:  ImageMagick-devel >= 6.2.4.6-1
%if 0%{?_with_freetype:1}
BuildRequires:  fontconfig-devel
%endif # freetype
# Audio
BuildRequires:  alsa-lib-devel >= 0.9.0
%if 0%{!?_without_esound:1}
BuildRequires:  esound-devel
%endif # esound
BuildRequires:  flac-devel
BuildRequires:  jack-audio-connection-kit-devel
BuildRequires:  libmodplug-devel
BuildRequires:  libmpcdec-devel
BuildRequires:  libvorbis-devel
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  speex-devel
BuildRequires:  wavpack-devel
# CDs
BuildRequires:  libcdio-devel
# Other
BuildRequires:  pkgconfig
BuildRequires:  gtk2-devel
BuildRequires:  libsmbclient-devel
BuildRequires:  libdvdnav-devel
BuildRequires:  libdvdread-devel

# Dropped in Fedora 9
Obsoletes:      xine-lib-arts < %{version}-%{release}

# Included in main package since Fedora 12
Obsoletes: xine-lib-pulseaudio < 1.1.16.3-5
Provides:  xine-lib-pulseaudio = %{version}-%{release}

%description
This package contains the Xine library.  It can be used to play back
various media, decode multimedia files from local disk drives, and display
multimedia streamed over the Internet. It interprets many of the most
common multimedia formats available - and some uncommon formats, too. 

%description -l zh_CN.UTF-8
这可以回放多种媒体，解码多媒体文件，播放互联网上的流媒体等。

%package        devel
Summary:        Xine library development files
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig
Requires:       zlib-devel
%description    devel
This package contains development files for %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package        extras
Summary:        Additional plugins for %{name} 
Summary(zh_CN.UTF-8): %{name} 的附加插件
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Requires:       %{name}%{?_isa} = %{version}-%{release}
#Requires:      xine-lib(plugin-abi) = %{plugin_abi}
%description    extras
This package contains extra plugins for %{name}:
%if 0%{!?_without_esound:1}
  - EsounD
%endif # esound
  - JACK
  - GDK-Pixbuf
  - SMB
  - SDL
  - AA-lib
  - Libcaca
  - Image decoding
%if 0%{!?_without_directfb:1}
  - DirectFB output
%endif # directfb

%description extras -l zh_CN.UTF-8
%{name} 的附加插件。


%prep
%setup -q
%patch0 -p1 -b .no_autopoint
# extra work for to omit old libtool-related crud
rm -f configure ltmain.sh libtool m4/libtool.m4 m4/ltoptions.m4 m4/ltversion.m4
#%patch1 -p1 -b .optflags
#%patch8 -p1 -b .avsync_hack
%patch9 -p1 -b .multilib
%patch10 -p1 -b .v4l
%ifarch mips64el
%patch11 -p0 -b .non-x86
%endif

./autogen.sh noconfig


%build
export SDL_CFLAGS="$(sdl-config --cflags)" SDL_LIBS="$(sdl-config --libs)"
# Keep list of options in mostly the same order as ./configure --help.
%configure \
    --disable-dependency-tracking \
    --enable-ipv6 \
%if 0%{!?_without_directfb:1}
    --enable-directfb \
%endif # directfb
    --enable-v4l \
    --enable-libv4l \
    --enable-xvmc \
    --disable-gnomevfs \
    --disable-a52dec \
    --disable-mad \
    --disable-vcd \
    --disable-asf \
    --disable-faad \
%if 0%{?_with_freetype:1}
%if 0%{?_with_antialiasing:1}
    --enable-antialiasing \
%endif # antialiasing
    --with-freetype \
    --with-fontconfig \
%endif # freetype
    --with-caca \
    --with-external-ffmpeg \
    --with-external-dvdnav \
    --with-xv-path=%{_libdir} \
    --with-libflac \
    --with-external-libmpcdec \
    --without-arts \
%if 0%{?_without_esound:1}
    --without-esound \
%endif
    --with-wavpack \
    --with-real-codecs-path=%{codecdir} \
    --with-w32-path=%{codecdir}

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT __docs
make install DESTDIR=$RPM_BUILD_ROOT
magic_rpm_clean.sh
#%find_lang libxine2
cp -pR $RPM_BUILD_ROOT%{_docdir}/xine-lib __docs
rm -rf $RPM_BUILD_ROOT%{_docdir}/xine-lib
rm -f  $RPM_BUILD_ROOT%{_libdir}/libxine-interface.la
 
# Removing useless files
rm -Rf $RPM_BUILD_ROOT%{_libdir}/libxine.la __docs/README \
       __docs/README.{freebsd,irix,solaris,MINGWCROSS,WIN32} \
       __docs/README.{dxr3,network_dvd}

# Directory for binary codecs
mkdir -p $RPM_BUILD_ROOT%{codecdir}

# unpackaged files
%if 0%{?_disable_v4l1:1}
rm -fv $RPM_BUILD_ROOT%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_inp_pvr.so
rm -fv $RPM_BUILD_ROOT%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_inp_v4l.so
%endif


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files 
%defattr(-,root,root,-)
%doc AUTHORS COPYING COPYING.LIB CREDITS ChangeLog* README TODO
%doc __docs/README.* __docs/faq.*
%dir %{codecdir}/
%{_datadir}/xine-lib/
%{_libdir}/libxine.so.*
%{_mandir}/man5/xine.5*
%dir %{_libdir}/xine/
%dir %{_libdir}/xine/plugins/
%dir %{_libdir}/xine/plugins/%{plugin_abi}/
%{_libdir}/xine/plugins/%{plugin_abi}/mime.types
# Listing every plugin separately for better control over binary packages
# containing exactly the plugins we want, nothing accidentally snuck in
# nor dropped.
%dir %{_libdir}/xine/plugins/%{plugin_abi}/post/
%{_libdir}/xine/plugins/%{plugin_abi}/post/xineplug_post_audio_filters.so
%{_libdir}/xine/plugins/%{plugin_abi}/post/xineplug_post_goom.so
%{_libdir}/xine/plugins/%{plugin_abi}/post/xineplug_post_mosaico.so
%{_libdir}/xine/plugins/%{plugin_abi}/post/xineplug_post_switch.so
%{_libdir}/xine/plugins/%{plugin_abi}/post/xineplug_post_visualizations.so
%{_libdir}/xine/plugins/%{plugin_abi}/post/xineplug_post_planar.so
%ifnarch mips64el
%{_libdir}/xine/plugins/%{plugin_abi}/post/xineplug_post_tvtime.so
%endif
%if %{have_vidix}
%dir %{_libdir}/xine/plugins/%{plugin_abi}/vidix/
%{_libdir}/xine/plugins/%{plugin_abi}/vidix/cyberblade_vid.so
%{_libdir}/xine/plugins/%{plugin_abi}/vidix/mach64_vid.so
%{_libdir}/xine/plugins/%{plugin_abi}/vidix/mga_crtc2_vid.so
%{_libdir}/xine/plugins/%{plugin_abi}/vidix/mga_vid.so
%{_libdir}/xine/plugins/%{plugin_abi}/vidix/nvidia_vid.so
%{_libdir}/xine/plugins/%{plugin_abi}/vidix/pm2_vid.so
%{_libdir}/xine/plugins/%{plugin_abi}/vidix/pm3_vid.so
%{_libdir}/xine/plugins/%{plugin_abi}/vidix/radeon_vid.so
%{_libdir}/xine/plugins/%{plugin_abi}/vidix/rage128_vid.so
%{_libdir}/xine/plugins/%{plugin_abi}/vidix/savage_vid.so
%{_libdir}/xine/plugins/%{plugin_abi}/vidix/sis_vid.so
%{_libdir}/xine/plugins/%{plugin_abi}/vidix/unichrome_vid.so
%endif # vidix
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_ao_out_alsa.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_ao_out_file.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_ao_out_none.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_ao_out_oss.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_ao_out_pulseaudio.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_decode_bitplane.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_decode_gsm610.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_decode_lpcm.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_decode_mpc.so
%ifarch %{ix86}
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_decode_qt.so
%endif # ix86
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_decode_real.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_decode_rgb.so
#%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_decode_speex.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_decode_spu.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_decode_spucc.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_decode_spucmml.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_decode_spudvb.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_decode_spuhdmv.so
#%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_decode_sputext.so
#%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_decode_theora.so
#%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_decode_vorbis.so
%ifarch %{ix86}
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_decode_w32dll.so
%endif # ix86
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_decode_yuv.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_dmx_audio.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_dmx_avi.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_dmx_fli.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_dmx_flv.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_dmx_games.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_dmx_iff.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_dmx_image.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_dmx_matroska.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_dmx_mng.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_dmx_mpeg.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_dmx_mpeg_block.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_dmx_mpeg_elem.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_dmx_mpeg_pes.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_dmx_mpeg_ts.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_dmx_nsv.so
#%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_dmx_ogg.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_dmx_pva.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_dmx_qt.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_dmx_rawdv.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_dmx_real.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_dmx_slave.so
#%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_dmx_sputext.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_dmx_yuv_frames.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_dmx_yuv4mpeg2.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_flac.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_inp_cdda.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_inp_dvb.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_inp_file.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_inp_http.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_inp_net.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_inp_pnm.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_inp_rtp.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_inp_rtsp.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_inp_stdin_fifo.so
%if ! 0%{?_disable_v4l1:1}
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_inp_pvr.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_inp_v4l.so
%endif
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_inp_v4l2.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_vo_out_fb.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_vo_out_none.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_vo_out_opengl.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_vo_out_raw.so
#%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_vo_out_syncfb.so
%if %{have_vidix}
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_vo_out_vidix.so
%endif # vidix
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_vo_out_xcbshm.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_vo_out_xcbxv.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_vo_out_xshm.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_vo_out_xv.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_vo_out_xvmc.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_vo_out_xxmc.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_wavpack.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_decode_dts.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_decode_dvaudio.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_decode_dxr3_spu.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_decode_dxr3_video.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_decode_ff.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_decode_mpeg2.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_decode_vdpau_h264.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_decode_vdpau_h264_alter.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_decode_vdpau_mpeg12.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_decode_vdpau_mpeg4.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_decode_vdpau_vc1.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_dmx_modplug.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_dmx_playlist.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_dmx_vc1_es.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_inp_bluray.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_inp_dvd.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_inp_mms.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_nsf.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_sputext.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_vdr.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_vo_out_dxr3.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_vo_out_vdpau.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_xiph.so

%files extras
%defattr(-,root,root,-)
%if 0%{!?_without_esound:1}
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_ao_out_esd.so
%endif # esound
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_ao_out_jack.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_decode_gdk_pixbuf.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_decode_image.so
#%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_inp_smb.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_vo_out_aa.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_vo_out_caca.so
%if 0%{!?_without_directfb:1}
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_vo_out_directfb.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_vo_out_xdirectfb.so
%endif # directfb
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_vo_out_sdl.so

%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_decode_libjpeg.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_inp_smb.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_inp_test.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_vo_out_opengl2.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_vo_out_vaapi.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_decode_libvpx.so

%files devel
%defattr(-,root,root,-)
%doc __docs/hackersguide/*
%{_bindir}/xine-config
%{_bindir}/xine-list*
%{_datadir}/aclocal/xine.m4
%{_includedir}/xine.h
%{_includedir}/xine/
%{_libdir}/libxine.so
%{_libdir}/pkgconfig/libxine.pc
%{_mandir}/man1/xine-config.1*
%{_mandir}/man1/xine-list*.1*


%changelog
* Fri Nov 06 2015 Liu Di <liudidi@gmail.com> - 1.2.6-3
- 为 Magic 3.0 重建

* Sat Oct 24 2015 Liu Di <liudidi@gmail.com> - 1.2.6-2
- 为 Magic 3.0 重建

* Tue Sep 22 2015 Liu Di <liudidi@gmail.com> - 1.2.6-1
- 更新到 1.2.6

* Mon Jun 09 2014 Liu Di <liudidi@gmail.com> - 1.2.5-1
- 更新到 1.2.5

* Mon Jan 14 2013 Liu Di <liudidi@gmail.com> - 1.2.2-5
- 为 Magic 3.0 重建

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 1.2.2-4
- 为 Magic 3.0 重建

* Mon Dec 03 2012 Liu Di <liudidi@gmail.com> - 1.2.1-3
- 为 Magic 3.0 重建

* Mon Oct 22 2012 Liu Di <liudidi@gmail.com> - 1.2.1-2
- 为 Magic 3.0 重建


