%define plugindir %(pkg-config bmp --variable=input_plugin_dir)

Name:           bmp-flac
Version:        2
Release:        4%{?dist}
Summary:        FLAC playback plugin for the Beep Media Player
Summary(zh_CN):	bmp 的 FLAC 插件

Group:          Applications/Multimedia
Group(zh_CN):	应用程序/多媒体
License:        GPL
URL:            http://www.skytale.net/projects/bmp-flac/
Source0:        bmp-flac-%{version}.tar.gz
Patch1:		bmp-flac-2-new.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  beep-media-player, flac-devel >= 1.1.0

%description
This package contains a FLAC (Free Lossless Audio Codec) playback plugin
for BMP (Beep Media Player).

%description -l zh_CN
bmp 的 FLAC 插件。

%prep
%setup -q
%patch1 -p1

%build
make %{?_smp_mflags} CFLAGS="$RPM_OPT_FLAGS -fPIC"


%install
rm -rf $RPM_BUILD_ROOT
make install \
    DESTDIR=$RPM_BUILD_ROOT \
    plugindir=%{plugindir}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc COPYING.GPL README
%{plugindir}/*



%changelog
* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 2-4
- 为 Magic 3.0 重建

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 2-3
- 为 Magic 3.0 重建

