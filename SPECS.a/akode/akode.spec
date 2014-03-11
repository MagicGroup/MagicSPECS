Summary: Audio-decoding framework 
Summary(zh_CN.UTF-8): 音频解码框架
Name:	 akode 
Version: 2.0.2
Release: 4%{?dist}
License: LGPL
Group: 	 System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL:	 http://carewolf.com/akode/  
#URL:	 http://www.kde-apps.org/content/show.php?content=30375
Source:	 http://www.kde-apps.org/content/files/30375-akode-%{version}.tar.bz2
Patch0:  akode-2.0.2-ffmpeg.patch
patch1:  akode-2.0.2-gcc44.patch
Patch2:	 akode-2.0.2-flac113-portable.patch
Patch3:  akode-2.0.2-multilib.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: automake
BuildRequires: alsa-lib-devel
BuildRequires: flac-devel
BuildRequires: libsamplerate-devel
BuildRequires: speex-devel
BuildRequires: libvorbis-devel
BuildRequires: libtool

%description
aKode is a simple audio-decoding frame-work that provides a uniform
interface to decode the most common audio-formats. It also has a direct
playback option for a number of audio-outputs.

aKode currently has the following decoder plugins:
* mpc: Decodes musepack aka mpc audio.
* xiph: Decodes FLAC, Ogg/FLAC, Speex and Ogg Vorbis audio. 

aKode also has the following audio outputs:
* oss: Outputs to the OSS (Open Sound System)
* alsa: Outputs to ALSA (dmix is recommended).

%description -l zh_CN.UTF-8
aKode 是一个简单的音频解码框架，提供了统一接口来解码大多数音频格式。

当前支持下面的解码插件：
* mpc: 解码 musepack，就是 mpc 音频。
* xiph: 解码 FLAC, Ogg/FLAC, Speex 和 Ogg Vorbis 音频
* mpeg: 解码 mp2/mp3 等音频
* ffmpeg: 解码 wma/rm 等音频

当前支持的输入：
oss/alsa/jack/sun/polyp

%package devel
Summary: Headers for developing programs that will use %{name} 
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:   Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}
%description devel
%{summary}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package static
Summary: Static libraries for %{name}
Summary(zh_CN.UTF-8): %{name} 的静态库
Group:   Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name}-devel = %{version}-%{release}

%description static
%{summary}.

%description static -l zh_CN.UTF-8
%{name} 的静态库。

%prep
%setup -q -n %{name}-%{version}%{?beta}
%patch0 -p1
%patch1 -p1
%patch2 -p4
%patch3 -p1

make -f Makefile.cvs


%build
%configure \
  --disable-static \
  --disable-debug --disable-warnings --disable-dependency-tracking \
  --without-libltdl \
  --with-alsa \
  --with-flac \
  --with-libsamplerate \
  --with-speex \
  --with-vorbis \
  --without-jack \
  --without-polypaudio \
  --with-ffmpeg \
  --with-libmad 

make LIBTOOL=/usr/bin/libtool


%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# unpackaged files
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.la
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README
# NEWS omitted, currently empty
#doc NEWS
%{_bindir}/akodeplay
%{_libdir}/libakode.so.*
%{_libdir}/libakode_*_*.so

%files devel
%defattr(-,root,root,-)
%{_bindir}/akode-config
%{_includedir}/*
%{_libdir}/libakode.so
%{_libdir}/pkgconfig/akode.pc

%files static
%defattr(-,root,root,-)
%{_libdir}/*.a

%changelog
* Thu Oct 27 2011 Liu Di <liudidi@gmail.com> - 2.0.2-4
- 为 Magic 3.0 重建
- 分出 static 包
- 注意：这个包是过时的，只有 KDE3 需要
