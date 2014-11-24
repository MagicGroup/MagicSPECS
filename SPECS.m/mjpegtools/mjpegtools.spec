%define name    mjpegtools

%define infoentry "* mjpeg-howto: (mjpeg-howto).        How to use the mjpeg tools"
%define infofile mjpeg-howto.info

%define __os_install_post %{nil}

Name: %name
Version: 2.1.0
Release: 1%{?dist}
Summary: Tools for recording, editing, playing back and mpeg-encoding video under linux
Summary(zh_CN): 在 linux 下录制、编辑、播放以及 mpeg 编码视频的工具
License: GPL
Url: http://mjpeg.sourceforge.net/
Group: Applications/Multimedia
Group(zh_CN): 应用程序/多媒体
Source0: http://prdownloads.sourceforge.net/mjpeg/mjpegtools-%{version}.tar.gz
Patch0:	mjpegtools-2.1.0-fixformat.patch

BuildRoot: %{_tmppath}/%{name}-buildroot-%{version}-%{release}

Requires: libX11 SDL
Requires: libpng libjpeg
Requires: glib2 gtk2
Requires: libquicktime
Requires: libdv

BuildRequires: autoconf automake
BuildRequires: libX11-devel SDL-devel
BuildRequires: libpng-devel libjpeg-devel
BuildRequires: glib2-devel gtk2-devel
BuildRequires: gcc-c++
# BuildRequires:	libquicktime-devel
# BuildRequires:	libdv-devel

Prefix: %{_prefix}

%description
The MJPEG-tools are a basic set of utilities for recording, editing, 
playing back and encoding (to mpeg) video under linux. Recording can
be done with zoran-based MJPEG-boards (LML33, Iomega Buz, Pinnacle
DC10(+), Marvel G200/G400), these can also playback video using the
hardware. With the rest of the tools, this video can be edited and
encoded into mpeg1/2 or divx video.

%description -l zh_CN.UTF-8
在 linux 下录制、编辑、播放以及 mpeg 编码视频的工具。

%package devel
Summary: Development headers and libraries for the mjpegtools
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库

%description devel
This package contains static libraries and C system header files
needed to compile applications that use part of the libraries
of the mjpegtools package.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1

#mkdir usr

%build

#tmp_prefix="`pwd`/usr"
#mkdir -p $tmp_prefix/{include,lib,bin,share}

#CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS
#CXXFLAGS="${CXXFLAGS:-%optflags}" ; export CXXFLAGS

%configure --disable-warnings_as_errors
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} DESTDIR=%{buildroot} install
magic_rpm_clean.sh

%post
#/sbin/install-info \
#	--entry=%{infoentry} \
#	--info-dir=%{_prefix}/share/info \
#	%{_prefix}/share/info/%{infofile}
/sbin/ldconfig

%postun
#/sbin/install-info \
#	--remove \
#	--info-dir=%{_prefix}/share/info \
#	%{_prefix}/share/info/%{infofile}

%clean
%{__rm} -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files
%defattr(-,root,root)
%doc AUTHORS BUGS CHANGES COPYING HINTS PLANS README TODO README.*
%{_bindir}/lav*
%{_bindir}/yuv*
%{_bindir}/jpeg2yuv
#%{_bindir}/testrec
%{_bindir}/y4m*
%{_bindir}/ppm*
%{_bindir}/glav
%{_bindir}/ypipe
%{_bindir}/mp*
%{_bindir}/*toy4m
%{_bindir}/png2yuv
%{_bindir}/anytovcd.sh
%{_bindir}/mjpeg_simd_helper
%{_bindir}/*.flt
%{_libdir}/*.so.*
%{_datadir}/man/man1/*
%{_datadir}/man/man5/*

# 去除 info 文件，以防止文件冲突
%exclude %{_datadir}/info/*
#%{_datadir}/info/

%files devel
%{_includedir}/mjpegtools/*.h
%{_includedir}/mjpegtools/mpeg2enc/*.hh
%{_includedir}/mjpegtools/mpeg2enc/*.h
%{_includedir}/mjpegtools/mplex/*.hpp
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.a
%exclude %{_libdir}/*.la
%{_libdir}/*.so

%changelog
* Wed Oct 15 2014 Liu Di <liudidi@gmail.com> - 2.1.0-1
- 更新到 2.1.0

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 2.0.0-2
- 为 Magic 3.0 重建

* Tue Oct 2 2007 Ni Hui <shuizhuyuanluo@126.com> - 1.9.0rc2-0.1mgc
- modify the spec to port to MagicLinux-2.1

* Fri Jun 02 2006 Steven Schultz <sms@2bsd.com>
  jpeg-mmx is not supported, it crashes on IA32 systems, will not build on
  X86_64 or PPC systems and even when it did work didn't provide  much of
  a speedup (jpeg decoding is a small portion of the overall encoding process).

* Fri Dec 19 2003 Ronald Bultje <rbultje@ronald.bitfreak.net>
- add everything for mpeg2enc/mplex libs (dev headers and so on)

* Sat Aug 23 2003 Ronald Bultje <rbultje@ronald.bitfreak.net>
- Remove quicktime4linux hacks, add libquicktime depdency
- Remove avifile leftovers

* Wed May 20 2002 Thomas Vander Stichele <thomas@apestaart.org>
- Added BuildRequires and Requires

* Tue Feb 12 2002 Geoffrey T. Dairiki <dairiki@dairiki.org>
- Fix spec file to build in one directory, etc...

* Thu Dec 06 2001 Ronald Bultje <rbultje@ronald.bitfreak.net>
- separated mjpegtools and mjpegtools-devel
- added changes by Marcel Pol <mpol@gmx.net> for cleaner RPM build

* Wed Jun 06 2001 Ronald Bultje <rbultje@ronald.bitfreak.net>
- 1.4.0-final release, including precompiled binaries (deb/rpm)
