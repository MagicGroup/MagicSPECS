# $Revision: 1.62 $, $Date: 2008/11/09 17:09:57 $
#
# Conditional build:
%bcond_without	alsa	# build without ALSA support in SDLAudio
#
%undefine _hardened_build
Summary:	MPEG4IP - system for encoding, streaming and playing MPEG-4 audio/video
Summary(zh_CN.UTF-8):	MPEG4IP - 编码，发布和播放 MPEG-4 音频/视频的系统
Name:		mpeg4ip
Version:	1.6.1
Release:	16%{?dist}
Epoch:		1
License:	MPL v1.1 (original code) and other licenses (included libraries)
Group:		Applications/Multimedia
Group(zh_CN.UTF-8):	应用程序/多媒体
# official tarball corrupted
# Source0:	http://dl.sourceforge.net/mpeg4ip/%{name}-%{version}.tar.gz
Source0:	ftp://ftp.freebsd.org/pub/FreeBSD/ports/local-distfiles/ahze/%{name}-%{version}.tar.gz
# Source0-md5:	59e9d9cb7aad0a9605fb6015e7f0b197
Patch0:		mpeg4ip-link.patch
Patch1:		mpeg4ip-ac.patch
Patch2:		mpeg4ip-gcc4.patch
Patch3:		mpeg4ip-configure.patch
Patch4:		mpeg4ip-audio_l16.cpp-typo.patch
Patch5:		mpeg4ip-ffmpeg.patch
Patch6:		mpeg4ip-gcc44.patch
Patch7:		mpeg4ip-srtp.patch
Patch8:		mpeg4ip-1.6.1-ffmpeg1.patch
Patch9:		mpeg4ip-ffmpeg55.patch
URL:		http://www.mpeg4ip.net/
BuildRequires:	SDL-devel
BuildRequires:	a52dec-devel
%{?with_alsa:BuildRequires:	alsa-lib-devel >= 0.9.0}
BuildRequires:	autoconf
BuildRequires:	automake >= 1.4
BuildRequires:	esound-devel >= 0.2.8
BuildRequires:	faac-devel >= 1.20.1
BuildRequires:	ffmpeg-devel >= 0.4.9-3.20061204
BuildRequires:	gtk2-devel >= 2.0.0
BuildRequires:	lame-devel >= 3.92
BuildRequires:	libid3tag-devel
BuildRequires:	libmad-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 1.4d
BuildRequires:	libvorbis-devel >= 1.0
BuildRequires:	x264-devel
BuildRequires:	libmpeg2
%ifarch %{ix86} %{x8664}
BuildRequires:	nasm >= 0.98.19
%endif
BuildRequires:	pkgconfig
#BuildRequires:	srtp-devel >= 1.4.2
#BuildRequires:	srtp-devel >= 1.5
#BuildRequires:	xvid-devel >= 1:1.0.0
BuildConflicts:	faad2 < 2.0-3
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags	-fno-strict-aliasing -Wno-error

%description
The MPEG4IP project provides a standards-based system for encoding,
streaming, and playing MPEG-4 encoded audio and video. To achieve this
the developers integrated a number of existing open source packages,
and also created some original code to fill in the gaps.

%description -l zh_CN.UTF-8
编码，发布和播放 MPEG-4 音频/视频的系统。

%package libs
Summary:	Base shared MPEG4IP libraries
Summary(zh_CN.UTF-8):	%name 的基本运行库
Group:		System/Libraries
Group(zh_CN.UTF-8):	系统环境/库

%description libs
Base shared MPEG4IP libraries.

%description libs -l zh_CN.UTF-8
%name 的基本运行库

%package devel
Summary:	Header files for base MPEG4IP libraries
Summary(zh_CN.UTF-8):	%name 的开发包
Group:		Development/Libraries
Group(zh_CN.UTF-8):	开发/库
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
Requires:	libstdc++-devel

%description devel
Header files for base MPEG4IP libraries.

%description devel -l zh_CN.UTF-8
%name 的开发包

%package static
Summary:	Static versions of base MPEG4IP libraries
Summary(zh_CN.UTF-8):	%name 的静态库
Group:		Development/Libraries
Group(zh_CN.UTF-8):	开发/库
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
Static versions of base MPEG4IP libraries.

%description static -l zh_CN.UTF-8
%name 的静态库。

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1

%build
cd lib/SDLAudio
touch NEWS AUTHORS ChangeLog
autoreconf -fisv
cd ../..
touch NEWS AUTHORS ChangeLog
pushd common/video/iso-mpeg4
touch NEWS AUTHORS ChangeLog
popd
autoreconf -fisv
install -d config
touch bootstrapped
%configure \
	%{!?with_alsa:--disable-alsa} \
	--enable-ffmpeg=%{_includedir} \
	--enable-ipv6 CFLAGS="-I/usr/include/SDL" CPPFLAGS="-I/usr/include/SDL"

for i in `find . -name Makefile`;do sed -i 's/\-Werror.* //g' $i;done
sed -i 's/\-Werror//g' lib/rtp/Makefile

%{__make} \
	CCAS="%{__cc}"

%install
rm -rf $RPM_BUILD_ROOT

# workaround for:
# libtool: install: warning: relinking `libmp4av.la'
#   ...  /usr/bin/ld: cannot find -lmp4v2
%{__make} -C lib/mp4v2 install \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install server/util/mp4encode/mp4encode $RPM_BUILD_ROOT%{_bindir}

rm -f $RPM_BUILD_ROOT%{_libdir}/mp4player_plugin/*.{a,la}
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
# bogus manual
rm -rf $RPM_BUILD_ROOT%{_mandir}/manm

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog encoding60.dsw FEATURES.html index.html README* NEWS TODO
%doc doc/{*.pdf,*.txt,*.html,*.jpg} doc/ietf/rfc*.txt doc/mcast/{mcast.txt,*_example}
%attr(755,root,root) %{_bindir}/avi2raw
%attr(755,root,root) %{_bindir}/avidump
%attr(755,root,root) %{_bindir}/gmp4player
%attr(755,root,root) %{_bindir}/h264_parse
%attr(755,root,root) %{_bindir}/lboxcrop
%attr(755,root,root) %{_bindir}/mp4art
%attr(755,root,root) %{_bindir}/mp4creator
%attr(755,root,root) %{_bindir}/mp4dump
%attr(755,root,root) %{_bindir}/mp4encode
%attr(755,root,root) %{_bindir}/mp4extract
%attr(755,root,root) %{_bindir}/mp4info
#%attr(755,root,root) %{_bindir}/mp4live
%attr(755,root,root) %{_bindir}/mp4player
%attr(755,root,root) %{_bindir}/mp4tags
%attr(755,root,root) %{_bindir}/mp4trackdump
%attr(755,root,root) %{_bindir}/mp4videoinfo
%attr(755,root,root) %{_bindir}/mpeg2t_dump
%attr(755,root,root) %{_bindir}/mpeg2video_parse
%attr(755,root,root) %{_bindir}/mpeg4vol
%attr(755,root,root) %{_bindir}/mpeg_ps_extract
%attr(755,root,root) %{_bindir}/mpeg_ps_info
%attr(755,root,root) %{_bindir}/rgb2yuv
%attr(755,root,root) %{_bindir}/sdl_pcm_play
%attr(755,root,root) %{_bindir}/yuvdump
%dir %{_libdir}/mp4player_plugin
%attr(755,root,root) %{_libdir}/mp4player_plugin/*.so*
%{_mandir}/man1/gmp4player.1*
%{_mandir}/man1/mp4creator.1*
%{_mandir}/man1/mp4encode.1*
%{_mandir}/man1/mp4live.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libhttp.so.*.*.*
%attr(755,root,root) %{_libdir}/libismacryp.so.*.*.*
%attr(755,root,root) %{_libdir}/libmp4*.so.*.*.*
%attr(755,root,root) %{_libdir}/libmpeg4ip*.so.*.*.*
%attr(755,root,root) %{_libdir}/libmsg_queue.so.*.*.*
%attr(755,root,root) %{_libdir}/libsdp.so.*.*.*
%attr(755,root,root) %{_libdir}/libsrtpif.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libhttp.so.0
%attr(755,root,root) %ghost %{_libdir}/libismacryp.so.0
%attr(755,root,root) %ghost %{_libdir}/libmp4*.so.0
%attr(755,root,root) %ghost %{_libdir}/libmpeg4ip*.so.0
%attr(755,root,root) %ghost %{_libdir}/libmsg_queue.so.0
%attr(755,root,root) %ghost %{_libdir}/libsdp.so.0
%attr(755,root,root) %ghost %{_libdir}/libsrtpif.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mpeg4ip-config
%attr(755,root,root) %{_libdir}/libhttp.so
%attr(755,root,root) %{_libdir}/libismacryp.so
%attr(755,root,root) %{_libdir}/libmp4*.so
%attr(755,root,root) %{_libdir}/libmpeg4ip*.so
%attr(755,root,root) %{_libdir}/libmsg_queue.so
%attr(755,root,root) %{_libdir}/libsdp.so
%attr(755,root,root) %{_libdir}/libsrtpif.so
%{_includedir}/codec_plugin.h
%{_includedir}/h264_sdp.h
%{_includedir}/mp4.h
%{_includedir}/mp4av*.h
%{_includedir}/mpeg4_*.h
%{_includedir}/mpeg4ip*.h
%{_includedir}/rtp_plugin.h
%{_includedir}/sdp*.h
%{_includedir}/text_plugin.h
%{_mandir}/man3/MP4*.3*

%files static
%defattr(644,root,root,755)
%{_libdir}/libhttp.a
%{_libdir}/libismacryp.a
%{_libdir}/libmp4*.a
%{_libdir}/libmpeg4ip*.a
%{_libdir}/libmsg_queue.a
%{_libdir}/libsdp.a
%{_libdir}/libsrtpif.a

%changelog
* Tue Nov 10 2015 Liu Di <liudidi@gmail.com> - 1:1.6.1-16
- 为 Magic 3.0 重建

* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 1:1.6.1-15
- 为 Magic 3.0 重建

* Tue Mar 31 2015 Liu Di <liudidi@gmail.com> - 1:1.6.1-14
- 为 Magic 3.0 重建

* Thu Dec 04 2014 Liu Di <liudidi@gmail.com> - 1:1.6.1-13
- 为 Magic 3.0 重建

* Tue Jun 24 2014 Liu Di <liudidi@gmail.com> - 1:1.6.1-12
- 为 Magic 3.0 重建

* Thu Jul 04 2013 Liu Di <liudidi@gmail.com> - 1:1.6.1-11
- 为 Magic 3.0 重建

* Thu Jul 04 2013 Liu Di <liudidi@gmail.com> - 1:1.6.1-10
- 为 Magic 3.0 重建

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 1:1.6.1-9
- 为 Magic 3.0 重建


