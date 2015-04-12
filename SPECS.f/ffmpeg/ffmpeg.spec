# $Id: ffmpeg.spec 1563 2004-07-15 21:11:23Z dude $
# Authority: matthias
%define svn    0
%define date   20100817

#define _without_faac 0

Summary: Hyper fast MPEG1/MPEG4/H263/RV and AC3/MPEG audio encoder and decoder
Summary(zh_CN.UTF-8): 非常快速的 MPEG1/MPEG4/H263/RV 和 AC3/MPEG 声音编码和解码器
Name: ffmpeg
%if %{svn}
Version:	2.5.5
Release: 0.svn%{date}.1%{?dist}.3
%else
Version:	2.5.5
Release: 1%{?dist}
%endif
License: GPL
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL: http://ffmpeg.org/
%if %{svn}
# svn export svn://svn.ffmpeg.org/ffmpeg/trunk ffmpeg-0.6.1-svn20100817
# tar -cjf ffmpeg-0.6.1-svn20100817.tar.bz2 ffmpeg-0.6.1-svn20100817
Source: %{name}-%{version}-svn%{date}.tar.bz2
%else
Source: http://ffmpeg.org/releases/%{name}-%{version}.tar.bz2
%endif
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: imlib, SDL, freetype, zlib
%{!?_without_lame:Requires: lame}
%{!?_without_vorbis:Requires: libogg, libvorbis}
%{!?_without_faac:Requires: faac}
BuildRequires: imlib-devel, SDL-devel, freetype-devel, zlib-devel
%{!?_without_lame:BuildRequires: lame-devel}
%{!?_without_vorbis:BuildRequires: libogg-devel, libvorbis-devel}
%{!?_without_faac:BuildRequires: faac-devel}
%{!?_without_x264:BuildRequires: x264-devel >= 0.118}

BuildRequires: opencore-amr-devel
BuildRequires: openjpeg-devel
BuildRequires: gsm-devel
BuildRequires: libdc1394-devel

Provides: libavcodec.so, libavformat.so

%description
FFmpeg is a very fast video and audio converter. It can also grab from a
live audio/video source.
The command line interface is designed to be intuitive, in the sense that
ffmpeg tries to figure out all the parameters, when possible. You have
usually to give only the target bitrate you want. FFmpeg can also convert
from any sample rate to any other, and resize video on the fly with a high
quality polyphase filter.

Available rpmbuild rebuild options :
--without : lame vorbis faad altivec

%description -l zh_CN.UTF-8
FFmpeg是一个非常快速的视频和音频转换器。它也可以从一个视频/音频直播中抓取流。

命令行界面被设计成直观的，就是说ffmpeg可能时会尝试发现全部参数。你通常只需要
给出目标的速率。FFmpeg也可以转换任何采样率到任意其它大小，并可以直接转换视频
大小。

可用的rpmbuild rebuild 选项：
--without : lame vorbis faad altivec

%package devel
Summary: Header files and static library for the ffmpeg codec library
Summary(zh_CN.UTF-8): ffmpeg编码库的头文件和静态库
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}

%description devel
FFmpeg is a very fast video and audio converter. It can also grab from a
live audio/video source.
The command line interface is designed to be intuitive, in the sense that
ffmpeg tries to figure out all the parameters, when possible. You have
usually to give only the target bitrate you want. FFmpeg can also convert
from any sample rate to any other, and resize video on the fly with a high
quality polyphase filter.

Install this package if you want to compile apps with ffmpeg support.

%description devel -l zh_CN.UTF-8
要编译带有ffmpeg支持的程序你需要安装这个包。

%prep
%if %{svn}
%setup -n %{name}-%{?date:%{version}-svn%{date}}%{!?date:%{version}}
%else
%setup -q 
%endif

# 修正 x264 问题
# sed -i 's/\-lx264\ \-lm/\-lx264\ \-lm\ \-lpthread/g' configure

### 删除无用的 ".svn " 目录
#find . -type d -name ".svn" | xargs rm -rf

%build
./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --shlibdir=%{_libdir} \
    --bindir=%{_bindir} \
    --datadir=%{_datadir}/ffmpeg \
    --mandir=%{_mandir} \
    --enable-gpl \
    --enable-version3 \
    --enable-nonfree \
    --enable-shared \
    --enable-postproc \
    --enable-pthreads \
%ifarch %{ix86}
    --arch=i686 \
    --cpu=i686 \
%endif
%ifarch mips64el
    --arch=mips64el \
    --cpu=mips3 \
    --disable-mips32r2 \
    --disable-mipsdspr1 \
    --disable-mipsdspr2 \
%endif
%ifarch ppc
    %{?_without_altivec: --disable-altivec} \
%endif
    %{!?_without_lame: --enable-libmp3lame} \
    %{!?_without_vorbis: --enable-libvorbis} \
    %{!?_without_faac: --enable-libfaac} \
			--enable-libfaac \
    %{!?_without_x264: --enable-libx264} \
  --enable-libopencore-amrnb \
  --enable-libopencore-amrwb \
  --enable-libdc1394       \
  --enable-libopenjpeg     \
  --enable-libgsm          \
  --enable-libspeex        \
  --enable-libtheora       \
  --enable-libvorbis

### FIXME: Make Makefile use autotool directory standard. (Please fix upstream)
%{__perl} -pi -e 's|\$\(prefix\)/lib|\$(libdir)|' Makefile */Makefile
%{__perl} -pi -e 's|\$\(prefix\)/include|\$(includedir)|' Makefile */Makefile

%{__make} %{?_smp_mflags} \
#    OPTFLAGS="-fPIC %{optflags}" \
#    SHFLAGS="-shared -Wl,-soname -Wl,\$@"


%install
%{__rm} -rf %{buildroot}
make install DESTDIR=$RPM_BUILD_ROOT

### Make installlib is broken in 0.4.6-8, so we do it by hand
%{__install} -D -m0644 libavcodec/libavcodec.a \
    %{buildroot}%{_libdir}/libavcodec.a
%{__install} -D -m0644 libavformat/libavformat.a \
    %{buildroot}%{_libdir}/libavformat.a

### Create compat symlink
%{__install} -d -m0755 %{buildroot}%{_libdir}/{libavcodec,libavformat}/
%{__ln_s} -f ../libavcodec.a %{buildroot}%{_libdir}/libavcodec/libavcodec.a
%{__ln_s} -f ../libavformat.a %{buildroot}%{_libdir}/libavformat/libavformat.a

### Remove from the included docs
%{__rm} -f doc/Makefile doc/*.1

%{__rm} -rf %{buildroot}/%{_docdir}/ffmpeg

### Move man to right dir

%clean
%{__rm} -rf %{buildroot}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-, root, root, 0755)
%doc %{_mandir}/man1/*
%{_bindir}/*
%{_libdir}/libavcodec.so.*
%{_libdir}/libavdevice.so.*
%{_libdir}/libavfilter.so.*
%{_libdir}/libavformat.so.*
%{_libdir}/libavutil.so.*
%{_libdir}/libpostproc.so.*
%{_libdir}/libswscale.so.*
%{_libdir}/libswresample.so.*
#%{_datadir}/ffmpeg/libx264-*.ffpreset
%{_datadir}/ffmpeg/libvpx-*.ffpreset
%{_datadir}/ffmpeg/ffprobe.xsd

%files devel
%defattr(-, root, root, 0755)
%doc  doc/
%{_includedir}/libavcodec/*.h
%{_includedir}/libswresample/*.h
%{_includedir}/libavdevice/avdevice.h
%{_includedir}/libavfilter/*.h
%{_includedir}/libavformat/*.h
%{_includedir}/libavutil/*.h
%{_includedir}/libpostproc/*.h
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libavcodec/
%{_libdir}/libavformat/
%{_includedir}/libswscale/swscale.h
%{_includedir}/libavdevice/version.h
%{_includedir}/libswscale/version.h
%{_datadir}/ffmpeg/examples/*
%{_mandir}/man1/ff*.1*
%{_mandir}/man3/lib*.3*

%changelog
* Fri Mar 27 2015 Liu Di <liudidi@gmail.com> - 2.5.5-1
- 更新到 2.5.5

* Wed Apr 02 2014 Liu Di <liudidi@gmail.com> - 2.2-1
- 更新到 2.2

* Fri Jul 05 2013 Liu Di <liudidi@gmail.com> - 1.2.2-2
- 为 Magic 3.0 重建

* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 1.0-1
- 为 Magic 3.0 重建

* Mon Dec 03 2012 Liu Di <liudidi@gmail.com> - 1.0-1
- 为 Magic 3.0 重建

* Tue Nov 22 2011 Liu Di <liudidi@gmail.com> - 0.8.7-1
- 更新到 0.8.7
- 注意：我们暂时不使用 libav

* Thu Feb 12 2009 Liu Di <liudidi@gmail.com> - 0.5.0-0.svn20090211.1
- 更新到 svn 20090211
- 注意：可能引起其它包的编译问题

* Fri Aug 29 2008 Ni Hui <shuizhuyuanluo@126.com> - 0.5.0-0.svn20080827.4mgc
- 去除无用的".svn"目录以减小软件包体积
- 戊子  七月廿九


