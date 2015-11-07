# $Id: bmp-wma.spec 3414 2005-07-20 22:51:05Z thias $
# Authority: matthias

%define bmp_inputdir %(pkg-config --variable=input_plugin_dir bmp 2>/dev/null || echo %{_libdir}/bmp/Input)

Summary: Windows Media Audio (WMA) playback plugin for the Beep Media Player
Name: bmp-wma
Version: 0.1.1
Release: 3%{?dist}
License: GPL
Group: Applications/Multimedia
URL: http://bmp-plugins.berlios.de/
Source: http://download.berlios.de/bmp-plugins/bmp-wma-%{version}.tar.gz 
Patch: bmp-wma-0.1.1-gcc4.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: beep-media-player


%description
This package contains a Windows Media Audio (WMA) playback plugin for BMP
(Beep Media Player), a media player that uses a skinned user interface based
on Winamp 2.x skins, and is based on ("forked off") XMMS.


%prep
%setup
%patch -p1 -b .gcc4

%build
%configure
sed -i 's/\/\* #undef HAVE_LRINTF \*\//#define HAVE_LRINTF 1/g' config.h
%{__make} %{?_smp_mflags} CFLAGS="$RPM_OPT_FLAGS -fPIC"


%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR=%{buildroot}


%clean
%{__rm} -rf %{buildroot}


%files
%defattr(-, root, root, 0755)
%exclude %{bmp_inputdir}/libwma.a
%exclude %{bmp_inputdir}/libwma.la
%{bmp_inputdir}/libwma.so


%changelog
* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 0.1.1-3
- 为 Magic 3.0 重建

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 0.1.1-2
- 为 Magic 3.0 重建

* Thu Jul 21 2005 Matthias Saou <http://freshrpms.net/> 0.1.1-2
- Include bmp-wma-0.1.1-gcc4.patch with the "usual" ffmpeg common.h change.

* Thu May 26 2005 Matthias Saou <http://freshrpms.net/> 0.1.1-1
- Initial rpm package.

