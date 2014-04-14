%global         majorminor 1.0
%global         _gobject_introspection  1.31.1

# Turn of extras package on RHEL.
%if ! 0%{?rhel}
%bcond_without extras
%else
%bcond_with extras
%endif

Name:           gstreamer1-plugins-bad
Version:        1.2.3
Release:        2%{?dist}
Summary:        GStreamer streaming media framework "bad" plugins

License:        LGPLv2+ and LGPLv2
URL:            http://gstreamer.freedesktop.org/
# The source is:
# http://gstreamer.freedesktop.org/src/gst-plugins-bad/gst-plugins-bad-%{version}.tar.xz
# modified with gst-p-bad-cleanup.sh from SOURCE1
Source0:        http://gstreamer.freedesktop.org/src/gst-plugins-bad/gst-plugins-bad-%{version}.tar.xz
Source1:        gst-p-bad-cleanup.sh

BuildRequires:  gstreamer1-devel >= %{version}
BuildRequires:  gstreamer1-plugins-base-devel >= %{version}

BuildRequires:  check
BuildRequires:  gettext-devel
BuildRequires:  libXt-devel
BuildRequires:  gtk-doc
BuildRequires:  gobject-introspection-devel >= %{_gobject_introspection}

BuildRequires:  bzip2-devel
BuildRequires:  exempi-devel
BuildRequires:  gsm-devel
BuildRequires:  jasper-devel
BuildRequires:  ladspa-devel
BuildRequires:  libdvdnav-devel
BuildRequires:  libexif-devel
BuildRequires:  libiptcdata-devel
BuildRequires:  libmpcdec-devel
BuildRequires:  liboil-devel
BuildRequires:  librsvg2-devel
BuildRequires:  libsndfile-devel
BuildRequires:  mesa-libGLU-devel
BuildRequires:  openssl-devel
BuildRequires:  orc-devel
BuildRequires:  soundtouch-devel
BuildRequires:  wavpack-devel
BuildRequires:  opus-devel
BuildRequires:  libwayland-client-devel
BuildRequires:  gnutls-devel
BuildRequires:  libsrtp-devel

BuildRequires:  chrpath

%if %{with extras}
BuildRequires:  celt-devel
## Plugins not ported
#BuildRequires:  dirac-devel
#BuildRequires:  gmyth-devel >= 0.4
BuildRequires:  fluidsynth-devel
BuildRequires:  libass-devel
## Plugin not ported
#BuildRequires:  libcdaudio-devel
BuildRequires:  libcurl-devel
BuildRequires:  libkate-devel
BuildRequires:  libmodplug-devel
## Plugins not ported
#BuildRequires:  libmusicbrainz-devel
#BuildRequires:  libtimidity-devel
BuildRequires:  libvdpau-devel
# Requires opencv version < 2.3.1, Rawhide currently has 2.4.2
#BuildRequires:  opencv-devel
BuildRequires:  schroedinger-devel
## Plugins not ported
#BuildRequires:  SDL-devel
#BuildRequires:  slv2-devel
BuildRequires:  wildmidi-devel
BuildRequires:  zbar-devel
BuildRequires:  zvbi-devel
%endif


%description
GStreamer is a streaming media framework, based on graphs of elements which
operate on media data.

This package contains plug-ins that aren't tested well enough, or the code
is not of good enough quality.


%if %{with extras}
%package extras
Summary:         Extra GStreamer "bad" plugins (less often used "bad" plugins)
Requires:        %{name} = %{version}-%{release}


%description extras
GStreamer is a streaming media framework, based on graphs of elements which
operate on media data.

gstreamer-plugins-bad contains plug-ins that aren't tested well enough,
or the code is not of good enough quality.

This package (%{name}-extras) contains
extra "bad" plugins for sources (mythtv), sinks (fbdev) and
effects (pitch) which are not used very much and require additional
libraries to be installed.
%endif


%package devel
Summary:        Development files for the GStreamer media framework "bad" plug-ins
Requires:       %{name} = %{version}-%{release}
Requires:       gstreamer1-plugins-base-devel


%description devel
GStreamer is a streaming media framework, based on graphs of elements which
operate on media data.

This package contains the development files for the plug-ins that
aren't tested well enough, or the code is not of good enough quality.


%prep
%setup -q -n gst-plugins-bad-%{version}


%build
%configure \
    --with-package-name="Fedora GStreamer-plugins-bad package" \
    --with-package-origin="http://download.fedoraproject.org" \
    %{!?with_extras:--disable-fbdev --disable-decklink --disable-linsys} \
    --enable-debug --disable-static --enable-experimental \
    --disable-dts --disable-faac --disable-faad --disable-nas \
    --disable-mimic --disable-libmms --disable-mpeg2enc --disable-mplex \
    --disable-neon --disable-openal --disable-rtmp --disable-xvid
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%find_lang gst-plugins-bad-%{majorminor}
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
# Kill rpath
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstvideoparsersbad.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstcamerabin2.so


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files -f gst-plugins-bad-%{majorminor}.lang
%doc AUTHORS COPYING COPYING.LIB README REQUIREMENTS

%{_libdir}/libgstbasecamerabinsrc-%{majorminor}.so.*
%{_libdir}/libgstcodecparsers-%{majorminor}.so.*
%{_libdir}/libgstegl-%{majorminor}.so.*
%{_libdir}/libgstinsertbin-%{majorminor}.so.*
%{_libdir}/libgstmpegts-%{majorminor}.so.*
%{_libdir}/libgstphotography-%{majorminor}.so.*
%{_libdir}/libgsturidownloader-%{majorminor}.so.*

%{_libdir}/girepository-1.0/GstEGL-1.0.typelib
%{_libdir}/girepository-1.0/GstInsertBin-1.0.typelib
%{_libdir}/girepository-1.0/GstMpegts-1.0.typelib

# Plugins without external dependencies
%{_libdir}/gstreamer-%{majorminor}/libgstaccurip.so
%{_libdir}/gstreamer-%{majorminor}/libgstadpcmdec.so
%{_libdir}/gstreamer-%{majorminor}/libgstadpcmenc.so
%{_libdir}/gstreamer-%{majorminor}/libgstaiff.so
%{_libdir}/gstreamer-%{majorminor}/libgstasfmux.so
%{_libdir}/gstreamer-%{majorminor}/libgstaudiofxbad.so
%{_libdir}/gstreamer-%{majorminor}/libgstaudiovisualizers.so
%{_libdir}/gstreamer-%{majorminor}/libgstautoconvert.so
%{_libdir}/gstreamer-%{majorminor}/libgstbayer.so
%{_libdir}/gstreamer-%{majorminor}/libgstcamerabin2.so
%{_libdir}/gstreamer-%{majorminor}/libgstcoloreffects.so
%{_libdir}/gstreamer-%{majorminor}/libgstdashdemux.so
%{_libdir}/gstreamer-%{majorminor}/libgstdataurisrc.so
%{_libdir}/gstreamer-%{majorminor}/libgstfbdevsink.so
%{_libdir}/gstreamer-%{majorminor}/libgstfestival.so
%{_libdir}/gstreamer-%{majorminor}/libgstfieldanalysis.so
%{_libdir}/gstreamer-%{majorminor}/libgstfreeverb.so
%{_libdir}/gstreamer-%{majorminor}/libgstfrei0r.so
%{_libdir}/gstreamer-%{majorminor}/libgstgaudieffects.so
%{_libdir}/gstreamer-%{majorminor}/libgstgdp.so
%{_libdir}/gstreamer-%{majorminor}/libgstgeometrictransform.so
%{_libdir}/gstreamer-%{majorminor}/libgstid3tag.so
%{_libdir}/gstreamer-%{majorminor}/libgstinter.so
%{_libdir}/gstreamer-%{majorminor}/libgstinterlace.so
%{_libdir}/gstreamer-%{majorminor}/libgstivtc.so
%{_libdir}/gstreamer-%{majorminor}/libgstjpegformat.so
%{_libdir}/gstreamer-%{majorminor}/libgstliveadder.so
%{_libdir}/gstreamer-%{majorminor}/libgstmfc.so
%{_libdir}/gstreamer-%{majorminor}/libgstmidi.so
%{_libdir}/gstreamer-%{majorminor}/libgstmpegpsdemux.so
%{_libdir}/gstreamer-%{majorminor}/libgstmpegtsdemux.so
%{_libdir}/gstreamer-%{majorminor}/libgstmpegpsmux.so
%{_libdir}/gstreamer-%{majorminor}/libgstmpegtsmux.so
%{_libdir}/gstreamer-%{majorminor}/libgstmxf.so
%{_libdir}/gstreamer-%{majorminor}/libgstpcapparse.so
%{_libdir}/gstreamer-%{majorminor}/libgstpnm.so
%{_libdir}/gstreamer-%{majorminor}/libgstrawparse.so
%{_libdir}/gstreamer-%{majorminor}/libgstremovesilence.so
%{_libdir}/gstreamer-%{majorminor}/libgstresindvd.so
%{_libdir}/gstreamer-%{majorminor}/libgstrfbsrc.so
%{_libdir}/gstreamer-%{majorminor}/libgstrsvg.so
%{_libdir}/gstreamer-%{majorminor}/libgstsdpelem.so
%{_libdir}/gstreamer-%{majorminor}/libgstsegmentclip.so
%{_libdir}/gstreamer-%{majorminor}/libgstshm.so
%{_libdir}/gstreamer-%{majorminor}/libgstsmooth.so
%{_libdir}/gstreamer-%{majorminor}/libgstsmoothstreaming.so
%{_libdir}/gstreamer-%{majorminor}/libgstspeed.so
%{_libdir}/gstreamer-%{majorminor}/libgstsubenc.so
%{_libdir}/gstreamer-%{majorminor}/libgstvdpau.so
%{_libdir}/gstreamer-%{majorminor}/libgstvideofiltersbad.so
%{_libdir}/gstreamer-%{majorminor}/libgstvideoparsersbad.so
%{_libdir}/gstreamer-%{majorminor}/libgstyadif.so
%{_libdir}/gstreamer-%{majorminor}/libgsty4mdec.so

# System (Linux) specific plugins
%{_libdir}/gstreamer-%{majorminor}/libgstdvb.so

# Plugins with external dependencies
%{_libdir}/gstreamer-%{majorminor}/libgstbz2.so
%{_libdir}/gstreamer-%{majorminor}/libgstfragmented.so
%{_libdir}/gstreamer-%{majorminor}/libgstgsm.so
%{_libdir}/gstreamer-%{majorminor}/libgstladspa.so
%{_libdir}/gstreamer-%{majorminor}/libgstopus.so
%{_libdir}/gstreamer-%{majorminor}/libgstsoundtouch.so
%{_libdir}/gstreamer-%{majorminor}/libgstsrtp.so
%{_libdir}/gstreamer-%{majorminor}/libgstwaylandsink.so

#debugging plugin
%{_libdir}/gstreamer-%{majorminor}/libgstdebugutilsbad.so


%if %{with extras}
%files extras
# Plugins with external dependencies
%{_libdir}/gstreamer-%{majorminor}/libgstassrender.so
%{_libdir}/gstreamer-%{majorminor}/libgstcurl.so
%{_libdir}/gstreamer-%{majorminor}/libgstdecklink.so
%{_libdir}/gstreamer-%{majorminor}/libgstfluidsynthmidi.so
%{_libdir}/gstreamer-%{majorminor}/libgstkate.so
%{_libdir}/gstreamer-%{majorminor}/libgstmodplug.so
%{_libdir}/gstreamer-%{majorminor}/libgstschro.so
%{_libdir}/gstreamer-%{majorminor}/libgstzbar.so
%{_libdir}/gstreamer-%{majorminor}/libgstwildmidi.so

%{_libdir}/gstreamer-%{majorminor}/libgsteglglessink.so
%{_libdir}/gstreamer-%{majorminor}/libgstflite.so
%{_libdir}/gstreamer-%{majorminor}/libgstuvch264.so
%{_libdir}/gstreamer-%{majorminor}/libgstwebp.so
%endif


%files devel
#%doc %{_datadir}/gtk-doc/html/gst-plugins-bad-plugins-%{majorminor}
%doc %{_datadir}/gtk-doc/html/gst-plugins-bad-libs-%{majorminor}

%{_datadir}/gir-1.0/GstEGL-%{majorminor}.gir
%{_datadir}/gir-1.0/GstInsertBin-%{majorminor}.gir
%{_datadir}/gir-1.0/GstMpegts-%{majorminor}.gir

%{_libdir}/libgstbasecamerabinsrc-%{majorminor}.so
%{_libdir}/libgstcodecparsers-%{majorminor}.so
%{_libdir}/libgstegl-%{majorminor}.so
%{_libdir}/libgstinsertbin-%{majorminor}.so
%{_libdir}/libgstmpegts-%{majorminor}.so
%{_libdir}/libgstphotography-%{majorminor}.so
%{_libdir}/libgsturidownloader-%{majorminor}.so

%{_includedir}/gstreamer-%{majorminor}/gst/basecamerabinsrc
%{_includedir}/gstreamer-%{majorminor}/gst/codecparsers
%{_includedir}/gstreamer-%{majorminor}/gst/egl
%{_includedir}/gstreamer-%{majorminor}/gst/insertbin
%{_includedir}/gstreamer-%{majorminor}/gst/interfaces/photography*
%{_includedir}/gstreamer-%{majorminor}/gst/mpegts
%{_includedir}/gstreamer-%{majorminor}/gst/uridownloader

# pkg-config files
%{_libdir}/pkgconfig/gstreamer-codecparsers-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-egl-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-insertbin-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-mpegts-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-plugins-bad-%{majorminor}.pc

%changelog
* Fri Apr 11 2014 Liu Di <liudidi@gmail.com> - 1.2.3-2
- 为 Magic 3.0 重建

* Mon Feb 10 2014 Brian Pepple <bpepple@fedoraproject.org> - 1.2.3-1
- Update to 1.2.3.

* Thu Feb  6 2014 Brian Pepple <bpepple@fedoraproject.org> - 1.2.2-2
- Build the srtp plugin. (#1055669)

* Fri Dec 27 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.2.2-1
- Update to 1.2.2.

* Fri Nov 15 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.2.1-4
- Build fluidsynth plugin. (#1024906)

* Thu Nov 14 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.2.1-3
- Add BR on gnutls-devel for HLS support. (#1030491)

* Mon Nov 11 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.2.1-2
- Build ladspa, libkate, and wildmidi plugins.

* Mon Nov 11 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.2.1-1
- Update to 1.2.1.

* Fri Nov  8 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.2.0-3
- Build gobject-introspection support. (#1028156)

* Fri Oct 04 2013 Bastien Nocera <bnocera@redhat.com> 1.2.0-2
- Build the wayland video output plugin

* Tue Sep 24 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.2.0-1
- Update to 1.2.0.

* Thu Sep 19 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.1.90-1
- Update to 1.1.90.

* Wed Aug 28 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.1.4-1
- Update to 1.1.4.

* Mon Jul 29 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.1.3-1
- Update to 1.1.3.

* Fri Jul 12 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.1.2-1
- Update to 1.1.2.

* Tue May 07 2013 Colin Walters <walters@verbum.org> - 1.0.7-2
- Move libgstdecklink to its correct place in extras; needed for RHEL

* Fri Apr 26 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.0.7-1
- Update to 1.0.7.

* Sun Mar 24 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.0.6-1
- Update to 1.0.6.
- Drop BR on PyXML.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan  8 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.0.5-1
- Update to 1.0.5

* Wed Dec 19 2012 Brian Pepple <bpepple@fedoraproject.org> - 1.0.4-1
- Update to 1.0.4

* Wed Nov 21 2012 Brian Pepple <bpepple@fedoraproject.org> - 1.0.3-1
- Update to 1.0.3

* Thu Oct 25 2012 Brian Pepple <bpepple@fedoraproject.org> - 1.0.2-1
- Update to 1.0.2

* Sun Oct  7 2012 Brian Pepple <bpepple@fedoraproject.org> - 1.0.1-1
- Update to 1.0.1
- Add frei0r plugin to file list.

* Mon Oct  1 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.0.0-3
- Enable verbose build

* Wed Sep 26 2012 Brian Pepple <bpepple@fedoraproject.org> - 1.0.0-2
- Build opus plugin.

* Mon Sep 24 2012 Brian Pepple <bpepple@fedoraproject.org> - 1.0.0-1
- Update to 1.0.0.

* Thu Sep 20 2012 Bastien Nocera <bnocera@redhat.com> 0.11.99-2
- The soundtouch-devel BR should be on, even with extras disabled

* Wed Sep 19 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.11.99-1
- Update to 0.11.99

* Fri Sep 14 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.11.94-1
- Update to 0.11.94.

* Sat Aug 18 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.11.93-2
- Fix permission on tarball clean-up script.
- Re-enable soundtouch-devel.
- Add COPYING.LIB to package.
- Use %%global instead of %%define.

* Wed Aug 15 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.11.93-1
- Update to 0.11.93.

* Fri Jul 20 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.11.92-1
- Initial Fedora spec file.
