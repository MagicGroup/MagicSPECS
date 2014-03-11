%define date 20041215
%define bmp_inputdir %(pkg-config --variable=input_plugin_dir bmp 2>/dev/null || echo %{_libdir}/bmp/Input)

Summary: AAC/MP4 playback plugin for the Beep Media Player
Summary(zh_CN): bmp 播放器的 AAC/MP4 插件
Name: bmp-aac
Version: 0
Release: 4.%{date}.%{?dist}
License: GPL
Group: Applications/Multimedia
Group(zh_CN): 应用程序/多媒体
URL: http://fondriest.frederic.free.fr/realisations/
Source: http://fondriest.frederic.free.fr/fichiers/bmp-mp4_%{date}.tar.bz2
Patch1: bmp-mp4_20041215-gcc4.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: beep-media-player
# No configure included
BuildRequires: autoconf, automake, libtool, gcc-c++


%description
This package contains an AAC/MP4 playback plugin for BMP (Beep Media Player),
a media player that uses a skinned user interface based on Winamp 2.x skins,
and is based on ("forked off") XMMS.

%description -l zh_CN
bmp 播放器的 AAC/MP4 插件

%prep
%setup -n bmp-mp4_%{date}
%patch1 -p1
autoreconf -vifs


%build
%configure
%{__make} %{?_smp_mflags}


%install
%{__rm} -rf %{buildroot}
mkdir -p %{buildroot}%{_libdir}/bmp/Input
%{__make} install DESTDIR=%{buildroot}

%clean
%{__rm} -rf %{buildroot}


%files
%defattr(-, root, root, 0755)
%doc AUTHORS ChangeLog COPYING
%exclude %{bmp_inputdir}/libmp4.la
%{bmp_inputdir}/libmp4.so


%changelog
* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 0-4.20041215.
- 为 Magic 3.0 重建

