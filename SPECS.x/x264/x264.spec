# $Id: x264.spec 3748 2005-11-29 18:47:34Z thias $
# Authority: matthias

%define sover 135
%define git 1
%define gitdate 20130704
Summary: Library for encoding and decoding H264/AVC video streams
Summary(zh_CN.UTF-8): 编码和解码H264/AVC视频流的库
Name: x264
Version: 0.%{sover}.2012
%if %{git}
Release: 0.svn%{gitdate}.%{?dist}.1
%else
Release: 1%{?dist}
%endif
License: GPL
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL: http://developers.videolan.org/x264.html
# Available through "git clone git://git.videolan.org/x264.git"
# find x264 -name .git | xargs rm -rf
Packager: Liu Di <liudidi@gmail.com>

#Source: %{name}-%{version}.tar.bz2
%if %{git}
Source: http://ftp.videolan.org/pub/videolan/x264/snapshots/%{name}-snapshot-%{gitdate}-2245.tar.bz2
%else
Source: http://download.videolan.org/pub/videolan/x264/%{name}-%{version}.tar.bz2
%endif
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: yasm >= 1.2.0
BuildRequires: libX11-devel
# version.sh requires svnversion
BuildRequires: subversion

%description
x264 is a free library for encoding H264/AVC video streams, written from
scratch.

%description -l zh_CN.UTF-8
x264 是一个自由的用来编码 H264/AVC 视频流的库，从头写的。

%package devel
Summary: Development files for the x264 library
Summary(zh_CN.UTF-8): x264库的开发文件
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
# Only an include file and a static lib, so don't require the main package
#Requires: %{name} = %{version}
Requires: pkgconfig

%description devel
x264 is a free library for encoding H264/AVC video streams, written from
scratch.

%description devel -l zh_CN.UTF-8
x264 是一个自由的用来编码 H264/AVC 视频流的库，从头写的。
这是其开发包。

%prep
#%setup
%setup -q -n %{name}-snapshot-%{gitdate}-2245
# AUTHORS file is in iso-8859-1
iconv -f iso-8859-1 -t utf-8 -o AUTHORS.utf8 AUTHORS
mv -f AUTHORS.utf8 AUTHORS
# configure hardcodes X11 lib path
%{__perl} -pi -e 's|/usr/X11R6/lib |/usr/X11R6/%{_lib} |g' configure


%build
# Force PIC as applications fail to recompile against the lib on x86_64 without
%configure \
    --enable-visualize \
    --enable-shared \
    --enable-static \
    --enable-pic \
    --enable-ffms
%{__make} %{?_smp_mflags}


%install
%{__rm} -rf %{buildroot}
%makeinstall
mkdir -p %{buildroot}%{_includedir}
install -m 0644 x264.h %{buildroot}%{_includedir}
install -m 0644 x264_config.h %{buildroot}%{_includedir}
mkdir -p %{buildroot}%{_libdir}/pkgconfig
install -m 0644 x264.pc %{buildroot}%{_libdir}/pkgconfig
install -m 0755 libx264.a %{buildroot}%{_libdir}
magic_rpm_clean.sh

%clean
%{__rm} -rf %{buildroot}


#post -p /sbin/ldconfig

#postun -p /sbin/ldconfig


%files
%defattr(-, root, root, 0755)
%doc AUTHORS COPYING
%{_bindir}/x264
%{_libdir}/libx264.so.%{sover}

%files devel
%defattr(-, root, root, 0755)
%{_includedir}/x264*.h
%{_libdir}/pkgconfig/x264.pc
%{_libdir}/libx264.a
%{_libdir}/libx264.so

%changelog
* Sun Dec 09 2012 Liu Di <liudidi@gmail.com>
- 为 Magic 3.0 重建

* Wed Aug 27 2008 Liu Di <liudidi@gmail.com> - 0.0.381-20080826
- 更新到 svn 20080826

* Thu Mar 22 2007 Liu Di <liudidi@gmail.com> - 0.0.381-20070321
- update to svn 20070321

* Thu Jan 11 2007 Liu Di <liudidi@gmail.com> - 0.0.381-20070110
- update to svn 20070110

* Tue Nov 29 2005 Matthias Saou <http://freshrpms.net/> 0.0.380-2 - 3748+/thias
- Also force PIC for the yasm bits, thanks to Anssi Hannula.

* Tue Nov 29 2005 Matthias Saou <http://freshrpms.net/> 0.0.380-1
- Update to svn 380.
- Force PIC as apps fail to recompile against the lib on x86_64 without.
- Include new pkgconfig file.

* Tue Oct  4 2005 Matthias Saou <http://freshrpms.net/> 0.0.315-1
- Update to svn 315.
- Disable vizualize since otherwise programs trying to link without -lX11 will
  fail (cinelerra in this particular case).

* Mon Aug 15 2005 Matthias Saou <http://freshrpms.net/> 0.0.285-1
- Update to svn 285.
- Add yasm build requirement (needed on x86_64).
- Replace X11 lib with lib/lib64 to fix x86_64 build.

* Tue Aug  2 2005 Matthias Saou <http://freshrpms.net/> 0.0.281-1
- Update to svn 281.

* Mon Jul 11 2005 Matthias Saou <http://freshrpms.net/> 0.0.273-1
- Initial RPM release.

