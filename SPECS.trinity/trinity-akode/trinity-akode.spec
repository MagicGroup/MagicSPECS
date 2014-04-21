# If TDE is built in a specific prefix (e.g. /opt/trinity), the release will be suffixed with ".opt".
%if "%{?tde_prefix}" != "/usr"
%define _variant .opt
%endif

# TDE 3.5.13 specific building variables
%define tde_bindir %{tde_prefix}/bin
%define tde_datadir %{tde_prefix}/share
%define tde_docdir %{tde_datadir}/doc
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}
%define tde_mandir %{tde_datadir}/man

%define tde_tdeappdir %{tde_datadir}/applications/kde
%define tde_tdedocdir %{tde_docdir}/tde
%define tde_tdeincludedir %{tde_includedir}/tde
%define tde_tdelibdir %{tde_libdir}/trinity

%define _docdir %{tde_docdir}

Summary: Audio-decoding framework 
Name:	 trinity-akode 
Version: 2.0.2
Release:	4%{?dist}%{?_variant}

License: LGPLv2+
Group: 	 System Environment/Libraries
#URL:	 http://carewolf.com/akode/  
URL:	 http://www.kde-apps.org/content/show.php?content=30375
Source0: http://www.kde-apps.org/CONTENT/content-files/akode-%{version}.tar.bz2

Prefix:		%{tde_prefix}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)


# Legacy Fedora 9 patches
Patch1: akode-pulseaudio.patch
Patch2: akode-2.0.2-multilib.patch
Patch3: akode-2.0.2-flac113-portable.patch
Patch4: akode-2.0.2-gcc43.patch

# New patch for Fedora 16 / TDE 3.5.13
Patch10: akode-autotools.patch
Patch11: akode-2.0.2-fix_ffmpeg_include.patch

# Optional features that are always enabled :-)
%define _with_flac --with-flac
%define _with_jack --with-jack
%define _with_libsamplerate --with-libsamplerate

# Pulseaudio is not available on RHEL 5 and earlier
%if 0%{?fedora} >= 15 || 0%{?rhel} >= 6 || 0%{?mgaversion} || 0%{?mdkversion}
%define _with_pulseaudio --with-pulseaudio
%endif

BuildRequires: automake libtool
BuildRequires: alsa-lib-devel
%{?_with_libsamplerate:BuildRequires: libsamplerate-devel}
BuildRequires: libvorbis-devel
BuildRequires: speex-devel

%if 0%{?mgaversion} || 0%{?mdkversion}
%{?_with_jack:BuildRequires: %{_lib}jack-devel}
%{?_with_flac:BuildRequires: %{_lib}flac-devel}
%{?_with_pulseaudio:BuildRequires: %{_lib}pulseaudio-devel}
%else
%{?_with_flac:BuildRequires: flac-devel}
%{?_with_jack:BuildRequires: jack-audio-connection-kit-devel}
%{?_with_pulseaudio:BuildRequires: pulseaudio-libs-devel}
%endif

%description
aKode is a simple audio-decoding frame-work that provides a uniform
interface to decode the most common audio-formats. It also has a direct
playback option for a number of audio-outputs.

aKode currently has the following decoder plugins:
* mpc: Decodes musepack aka mpc audio.
* xiph: Decodes FLAC, Ogg/FLAC, Speex and Ogg Vorbis audio. 

aKode also has the following audio outputs:
* alsa: Outputs to ALSA (dmix is recommended).

%package devel
Summary: Headers for developing programs that will use %{name} 
Group:   Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig
%description devel
%{summary}.

%package jack 
Summary: Jack audio output backend for %{name}
Group:   Development/Libraries
Requires: %{name} = %{version}-%{release}
%description jack 
%{summary}.

%package pulseaudio
Summary: Pulseaudio output backend for %{name}
Group:   Development/Libraries
Requires: %{name} = %{version}-%{release}
%description pulseaudio
%{summary}.
Recommended for network transparent audio.

# Packaged separately to keep main/core %{akode} package LGPL-clean.
%package libsamplerate 
Summary: Resampler based on libsamplerate for %{name}
Group:   Development/Libraries
License: GPLv2+
Requires: %{name} = %{version}-%{release}
%description libsamplerate 
%{summary}.


%if 0%{?suse_version}
%debug_package
%endif


%prep
%setup -q -n akode-%{version}

%patch1 -p1 -b .pulseaudio
%patch2 -p1 -b .multilib
%patch3 -p4 -b .flac113_portable
%patch4 -p1 -b .gcc43

%patch10 -p1
%patch11 -p1 -b .ffmpeg

# Ugly hack to modify TQT include directory inside autoconf files.
# If TQT detection fails, it fallbacks to TQT4 instead of TQT3 !
%__sed -i "admin/acinclude.m4.in" \
  -e "s|/usr/include/tqt|%{tde_includedir}/tqt|g" \
  -e "s|kde_htmldir='.*'|kde_htmldir='%{tde_tdedocdir}/HTML'|g"

%__cp -f "/usr/share/aclocal/libtool.m4" "admin/libtool.m4.in"
%__cp -f "/usr/share/libtool/config/ltmain.sh" "admin/ltmain.sh" || %__cp -f "/usr/share/libtool/ltmain.sh" "admin/ltmain.sh"
%__make -f admin/Makefile.common cvs

%build
%configure \
  --bindir=%{tde_bindir} \
  --libdir=%{tde_libdir} \
  --includedir=%{tde_includedir} \
  --datadir=%{tde_datadir} \
  --disable-static \
  --enable-shared \
  --disable-debug --disable-warnings --disable-dependency-tracking \
  --without-libltdl \
  --with-alsa \
  --with-oss \
  %{?_with_flac} %{!?_with_flac:--without-flac} \
  %{?_with_jack} %{!?_with_jack:--without-jack} \
  %{?_with_libsamplerate} %{!?_with_libsamplerate:--without-libsamplerate} \
  %{?_with_pulseaudio} %{!?_with_pulseaudio:--without-pulseaudio} \
  --with-speex \
  --with-vorbis \
  --without-ffmpeg \
  --without-libmad \
  --enable-closure \
  --enable-new-ldflags \
  --enable-final

%__make %{?_smp_mflags} LIBTOOL=$(which libtool)


%install
%__rm -rf %{buildroot} 
%__make install DESTDIR=%{buildroot}

# unpackaged files
%__rm -f %{buildroot}%{tde_libdir}/*.a

# rpmdocs
for file in AUTHORS COPYING NEWS README TODO ; do
  test -s  "$file" && install -p -m644 -D "$file" "rpmdocs/$file"
done


%clean
%__rm -rf %{buildroot} 


%post
/sbin/ldconfig

%postun 
/sbin/ldconfig

%post devel
/sbin/ldconfig

%postun devel
/sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc rpmdocs/* 
%{tde_bindir}/akodeplay
%{tde_libdir}/libakode.so.*
%{tde_libdir}/libakode_alsa_sink.la
%{tde_libdir}/libakode_alsa_sink.so
%{tde_libdir}/libakode_mpc_decoder.la
%{tde_libdir}/libakode_mpc_decoder.so
%{tde_libdir}/libakode_oss_sink.la
%{tde_libdir}/libakode_oss_sink.so
%{tde_libdir}/libakode_xiph_decoder.la
%{tde_libdir}/libakode_xiph_decoder.so

#files -libmad
#   /opt/trinity/lib64/libakode_mpeg_decoder.la
#   /opt/trinity/lib64/libakode_mpeg_decoder.so


%files devel
%defattr(-,root,root,-)
%{tde_bindir}/akode-config
%{tde_includedir}/*
%{tde_libdir}/libakode.la
%{tde_libdir}/libakode.so
%{tde_libdir}/pkgconfig/*.pc

%if "%{?_with_jack}" != ""
%files jack 
%defattr(-,root,root,-)
%{tde_libdir}/libakode_jack_sink.la
%{tde_libdir}/libakode_jack_sink.so
%endif

# License: GPLv2+
%if "%{?_with_libsamplerate:1}" == "1"
%files libsamplerate
%defattr(-,root,root,-)
%{tde_libdir}/libakode_src_resampler.la
%{tde_libdir}/libakode_src_resampler.so
%endif

%if "%{?_with_pulseaudio:1}" == "1"
%files pulseaudio
%defattr(-,root,root,-)
%{tde_libdir}/libakode_polyp_sink.la
%{tde_libdir}/libakode_polyp_sink.so
%endif


%changelog
* Tue Jul 23 2013 Liu Di <liudidi@gmail.com> - 2.0.2-4.opt
- 为 Magic 3.0 重建

* Wed Oct 03 2012 Francois Andriot <francois.andriot@free.fr> - 2.0.2-3
- Initial build for TDE 3.5.13.1

* Tue Jul 30 2012 Francois Andriot <francois.andriot@free.fr> 2.0.2-2
- Re-adds '.la' files

* Tue May 01 2012 Francois Andriot <francois.andriot@free.fr> 2.0.2-1
- Port to TDE 3.5.13
- Based on spec file from Fedora 9 'akode-2.0.2-5'
