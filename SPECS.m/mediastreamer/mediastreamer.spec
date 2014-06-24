#
# Conditional build:
%bcond_without	opengl		# X11+OpenGL rendering support
%bcond_with	pcap		# audio playing from PCAP files
%bcond_without	pulseaudio	# PulseAudio support
#
Summary:	Audio/Video real-time streaming
Summary(pl.UTF-8):	Przesyłanie strumieni audio/video w czasie rzeczywistym 
Name:		mediastreamer
Version:	2.10.0
Release:	1
License:	GPL v2+
Group:		Libraries
Source0:	http://download-mirror.savannah.gnu.org/releases/linphone/mediastreamer/%{name}-%{version}.tar.gz
# Source0-md5:	5a4e7545e212068534b56fdf41c961e9
Patch0:		%{name}-imagedir.patch
URL:		http://www.linphone.org/eng/documentation/dev/mediastreamer2.html
%{?with_opengl:BuildRequires:	OpenGL-GLX-devel}
BuildRequires:	SDL-devel >= 1.2.0
BuildRequires:	alsa-lib-devel
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake >= 1:1.9
BuildRequires:	doxygen
# libavcodec >= 51.0.0, libswscale >= 0.7.0
BuildRequires:	ffmpeg-devel
BuildRequires:	gettext-devel
%{?with_opengl:BuildRequires:	glew-devel >= 1.5}
BuildRequires:	jack-audio-connection-kit-devel
BuildRequires:	intltool >= 0.40
BuildRequires:	libgsm-devel
%{?with_pcap:BuildRequires:	libpcap-devel}
BuildRequires:	libtheora-devel >= 1.0-0.alpha7
BuildRequires:	libtool >= 2:2
BuildRequires:	libupnp-devel >= 1.6
BuildRequires:	libupnp-devel < 1.7
BuildRequires:	libv4l-devel
BuildRequires:	libvpx-devel >= 0.9.6
BuildRequires:	opus-devel >= 0.9.0
BuildRequires:	ortp-devel >= 0.23.0
BuildRequires:	pkgconfig
%{?with_pulseaudio:BuildRequires:	pulseaudio-devel >= 0.9.21}
BuildRequires:	sed >= 4.0
BuildRequires:	spandsp-devel >= 0.0.6
BuildRequires:	speex-devel >= 1.2-beta3
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXv-devel
BuildRequires:	xxd
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

%description -l pl.UTF-8
Mediastreamer2 to udostępniona na licencji GPL biblioteka do
przesyłania i przetwarzania strumieni audio/video w czasie
rzeczywistym. Jest napisana w czystym C, oparta na bibliotece oRTP.

%package devel
Summary:	Header files and development documentation for mediastreamer library
Summary(pl.UTF-8):	Pliki nagłówkowe i dokumentacja do biblioteki mediastreamer
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%{?with_opengl:Requires:	OpenGL-devel}
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
%{?with_pulseaudio:Requires:	pulseaudio-devel >= 0.9.21}
Requires:	spandsp-devel >= 0.0.6
Requires:	speex-devel >= 1.2-beta3
Requires:	xorg-lib-libX11-devel
Requires:	xorg-lib-libXv-devel

%description devel
Header files and development documentation for mediastreamer library.

%description devel -l pl.UTF-8
Pliki nagłówkowe i dokumentacja do biblioteki mediastreamer.

%package static
Summary:	Static mediastreamer library
Summary(pl.UTF-8):	Statyczna biblioteka mediastreamer
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static mediastreamer library.

%description static -l pl.UTF-8
Statyczna biblioteka mediastreamer.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
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

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/mediastream
%{?with_pcap:%attr(755,root,root) %{_bindir}/pcap_playback}
%attr(755,root,root) %{_libdir}/libmediastreamer_base.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libmediastreamer_base.so.3
%attr(755,root,root) %{_libdir}/libmediastreamer_voip.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libmediastreamer_voip.so.3
%dir %{_libdir}/mediastreamer
%dir %{_libdir}/mediastreamer/plugins
%{_pixmapsdir}/%{name}

%files devel
%defattr(644,root,root,755)
%doc help/doc/html
%attr(755,root,root) %{_libdir}/libmediastreamer_base.so
%attr(755,root,root) %{_libdir}/libmediastreamer_voip.so
%{_libdir}/libmediastreamer_base.la
%{_libdir}/libmediastreamer_voip.la
%{_includedir}/mediastreamer2
%{_pkgconfigdir}/mediastreamer.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libmediastreamer_base.a
%{_libdir}/libmediastreamer_voip.a
