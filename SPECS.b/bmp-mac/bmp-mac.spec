%define bmp_inputdir %(pkg-config --variable=input_plugin_dir bmp 2>/dev/null || echo %{_libdir}/bmp/Input)

Summary: Monkey's Audio Codec (MAC/APE) playback plugin for the Beep Media Player
Summary(zh_CN): bmp 播放器的 MAC/APE 播放插件
Name: bmp-mac
Version: 0.1.1
Release: 4%{?dist}
License: GPL
Group: Applications/Multimedia
Group(zh_CN): 应用程序/多媒体
URL: http://supermmx.org/linux/mac/
Source: http://dl.sf.net/mac-port/bmp-mac-%{version}.tar.gz
Patch1: bmp-mac-0.1.1-gtk2.patch
Patch2: bmp-mac-0.1.1-gtkdeprecated.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: beep-media-player, mac-devel, gcc-c++


%description
This package contains a Monkey's Audio Codec (MAC/APE) playback plugin for BMP
(Beep Media Player), a media player that uses a skinned user interface based
on Winamp 2.x skins, and is based on ("forked off") XMMS.

%description -l zh_CN
bmp 播放器的 MAC/APE 播放插件

%prep
%setup
%patch1 -p1
%patch2 -p1

%build
%configure
%{__make} %{?_smp_mflags}


%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR=%{buildroot}


%clean
%{__rm} -rf %{buildroot}


%files
%defattr(-, root, root, 0755)
%doc AUTHORS BUGS ChangeLog COPYING NEWS README TODO
%exclude %{bmp_inputdir}/libbmp-mac.a
%exclude %{bmp_inputdir}/libbmp-mac.la
%{bmp_inputdir}/libbmp-mac.so


%changelog
* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 0.1.1-4
- 为 Magic 3.0 重建


