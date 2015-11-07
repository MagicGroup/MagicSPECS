#
# Conditional build:
%bcond_without	opengl		# X11+OpenGL rendering support
%bcond_with	pcap		# audio playing from PCAP files
%bcond_without	pulseaudio	# PulseAudio support
#
Summary:	Audio/Video real-time streaming
Summary(zh_CN.UTF-8): 音频/视频实时流
Name:		mediastreamer
Version: 2.11.2
Release: 2%{?dist}
License:	GPL v2+
Group:		Libraries
Source0:	http://download-mirror.savannah.gnu.org/releases/linphone/mediastreamer/%{name}-%{version}.tar.gz
# Source0-md5:	5a4e7545e212068534b56fdf41c961e9
URL:		http://www.linphone.org/eng/documentation/dev/mediastreamer2.html
%{?with_opengl:BuildRequires:	mesa-libGL-devel}
Patch1:		mediastreamer-2.11.2-mbedtls.patch
BuildRequires:	SDL-devel >= 1.2.0
BuildRequires:	alsa-lib-devel
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake >= 1.9
BuildRequires:	doxygen
# libavcodec >= 51.0.0, libswscale >= 0.7.0
BuildRequires:	ffmpeg-devel
BuildRequires:	gettext-devel
%{?with_opengl:BuildRequires:	glew-devel >= 1.5}
BuildRequires:	jack-audio-connection-kit-devel
BuildRequires:	intltool >= 0.40
BuildRequires:	gsm-devel
%{?with_pcap:BuildRequires:	libpcap-devel}
BuildRequires:	libtheora-devel >= 1.0-0.alpha7
BuildRequires:	libtool >= 2
BuildRequires:	libupnp-devel >= 1.6
BuildRequires:	libupnp-devel < 1.7
BuildRequires:	libv4l-devel
BuildRequires:	libvpx-devel >= 0.9.6
BuildRequires:	opus-devel >= 0.9.0
BuildRequires:	ortp-devel >= 0.23.0
BuildRequires:	pkgconfig
%{?with_pulseaudio:BuildRequires:	pulseaudio-libs-devel >= 0.9.21}
BuildRequires:	sed >= 4.0
BuildRequires:	spandsp-devel >= 0.0.6
BuildRequires:	speex-devel >= 1.2-beta3
BuildRequires:	libX11-devel
BuildRequires:	libXv-devel
#BuildRequires:	xxd
%{?with_opengl:Requires:	glew >= 1.5}
Requires:	libtheora >= 1.0-0.alpha7
Requires:	libupnp >= 1.6
Requires:	libvpx >= 0.9.6
Requires:	opus >= 0.9.0
Requires:	ortp >= 0.23.0
%{?with_pulseaudio:Requires:	pulseaudio-libs >= 0.9.21}
Requires:	spandsp >= 0.0.6
Requires:	speex >= 1.2-beta3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Mediastreamer2 is a GPL licensed library to make audio and video
real-time streaming and processing. Written in pure C, it is based
upon the oRTP library.

%description -l zh_CN.UTF-8
支持音频和视频的实时流。

%package devel
Summary:	Header files and development documentation for mediastreamer library
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:	%{name} = %{version}-%{release}
%{?with_opengl:Requires:	mesa-libGL-devel}
Requires:	alsa-lib-devel
Requires:	ffmpeg-devel
%{?with_opengl:Requires:	glew-devel >= 1.5}
Requires:	libtheora-devel >= 1.0-0.alpha7
Requires:	libupnp-devel >= 1.6
Requires:	libupnp-devel < 1.7
Requires:	libv4l-devel
Requires:	libvpx-devel >= 0.9.6
Requires:	opus-devel >= 0.9.0
Requires:	ortp-devel >= 0.23.0
%{?with_pulseaudio:Requires:	pulseaudio-libs-devel >= 0.9.21}
Requires:	spandsp-devel >= 0.0.6
Requires:	speex-devel >= 1.2-beta3
Requires:	libX11-devel
Requires:	libXv-devel

%description devel
Header files and development documentation for mediastreamer library.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package static
Summary:	Static mediastreamer library
Summary(zh_CN.UTF-8): %{name} 的静态库
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static mediastreamer library.

%description static -l zh_CN.UTF-8
%{name} 的静态库。

%prep
%setup -q
%patch1 -p1

%build
autoreconf -fisv
%configure \
	--enable-external-ortp \
	%{!?with_opengl:--disable-glx} \
	%{?with_pcap:--enable-pcap} \
	%{?with_pulseaudio:--enable-pulseaudio} \
	--disable-silent-rules \
	--enable-static

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# for external plugins
install -d $RPM_BUILD_ROOT%{_libdir}/mediastreamer/plugins

# Remove duplicated documentation
%{__rm} -r $RPM_BUILD_ROOT/usr/share/doc/%{name}-%{version}/html
magic_rpm_clean.sh
%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/mediastream
%attr(755,root,root) %{_bindir}/msaudiocmp
%{?with_pcap:%attr(755,root,root) %{_bindir}/pcap_playback}
%attr(755,root,root) %{_libdir}/libmediastreamer_base.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libmediastreamer_base.so.4
%attr(755,root,root) %{_libdir}/libmediastreamer_voip.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libmediastreamer_voip.so.4
%dir %{_libdir}/mediastreamer
%dir %{_libdir}/mediastreamer/plugins
%{_datadir}/images/*

%files devel
%defattr(644,root,root,755)
%doc help/doc/html
%attr(755,root,root) %{_libdir}/libmediastreamer_base.so
%attr(755,root,root) %{_libdir}/libmediastreamer_voip.so
%{_libdir}/libmediastreamer_base.la
%{_libdir}/libmediastreamer_voip.la
%{_includedir}/mediastreamer2
%{_libdir}/pkgconfig/mediastreamer.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libmediastreamer_base.a
%{_libdir}/libmediastreamer_voip.a
