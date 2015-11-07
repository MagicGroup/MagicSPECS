%define _missing_build_ids_terminate_build %{nil}
Name: codec
Version: 20110131
Release: 3%{?dist}
Summary: package of win32 codec and linux codec for mplayer and xine
Summary(zh_CN.UTF-8): mplayer 和 xine 的 win32 和 linux 编解码器
Group: Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
License: GPL
Vendor: Magic Group
Packager: KDE <jack@linux.net.cn>
URL: http://www.mplayerhq.hu
Source0: http://www.mplayerhq.hu/MPlayer/releases/codecs/all-%{version}.tar.bz2
Provides: win32codec, mplayer-win32codec
Obsoletes: mplayer-win32codec
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)
Autoreq: no

BuildArch: %{ix86} x86_64

%description
These are Video and Audio codecs binary packages add support for codecs that are not yet
implemented natively, like newer RealVideo variants and a lot of uncommon formats. Note that
they are not necessary to play most common formats like DVDs, MPEG-1/2/4, etc. 

%description -l zh_CN.UTF-8
这些是还没本地化实现的一些视频和音频编解码器的二进制包，比如
新的 Real 视频变种和其它很多不常见的格式。注意这些对播放大多数
常见格式，比如 DVD，MPEG-1/2/4 等，都不是必需的。

%prep
%setup -q -n all-%{version}

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_libdir}/codecs
cp *  %{buildroot}%{_libdir}/codecs
pushd %{buildroot}%{_libdir}
ln -s codecs win32
popd
magic_rpm_clean.sh

%clean
rm -rf ${RPM_BUILD_ROOT}
rm -rf ${RPM_BUILD_DIR}/all-%{version}


%files
%defattr (-,root,root)
%{_libdir}/win32
%{_libdir}/codecs/*

%changelog
* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 20110131-3
- 为 Magic 3.0 重建

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 20110131-2
- 为 Magic 3.0 重建

* Mon Nov 07 2011 Liu Di <liudidi@gmail.com> - 20111107-1
- 更新到 20110131

* Fri Nov 09 2007 Liu Di <liudidi@gmail.com> - 20071007-1mgc
- update to 20071007

* Mon Mar 19 2007 kde <athena_star {at} 163 {dot} com> - 20061022-3mgc
- add a symbolic link for xine-lib: codecs---->win32

* Fri Mar 9 2007 kde <athena_star {at} 163 {dot} com> - 20061022-2mgc
- modify the spec file

* Fri Feb 09 2007 Liu Di <liudidi@gmail.com> - 20061022-1mgc
- update to 20061022

* Tue Oct 10 2006 kde <jack@linux.net.cn>  - 20060611-3mgc
- add Provides: mplayer-win32codec

* Sat Oct 7 2006 kde <jack@linux.net.cn>  - 20060611-2mgc
- build with all win32codec

* Mon Oct 2 2006 kde <jack@linux.net.cn>  - 20060611-1mgc
- initial the first spec file.
 
