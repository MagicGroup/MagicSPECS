%global         majorminor 1.0
%global         _gobject_introspection  1.31.1

# Turn of extras package on RHEL.
%if ! 0%{?rhel}
%bcond_without extras
%else
%bcond_with extras
%endif

Name:           gstreamer1-plugins-ugly
Version:	1.3.90
Release:        2%{?dist}
Summary:        GStreamer streaming media framework "ugly" plugins

License:        LGPLv2+ and LGPLv2
URL:            http://gstreamer.freedesktop.org/
# The source is:
# http://gstreamer.freedesktop.org/src/gst-plugins-ugly/gst-plugins-ugly-%{version}.tar.xz
# modified with gst-p-ugly-cleanup.sh from SOURCE1
Source0:        http://gstreamer.freedesktop.org/src/gst-plugins-ugly/gst-plugins-ugly-%{version}.tar.xz

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


%prep
%setup -q -n gst-plugins-ugly-%{version}


%build
%configure \
    --with-package-name="Fedora GStreamer-plugins-ugly package" \
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
magic_rpm_clean.sh
%find_lang gst-plugins-ugly-%{majorminor}
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files -f gst-plugins-ugly-%{majorminor}.lang
%{_libdir}/gstreamer-%{majorminor}/libgsta52dec.so
%{_libdir}/gstreamer-%{majorminor}/libgstamrnb.so
%{_libdir}/gstreamer-%{majorminor}/libgstamrwbdec.so
%{_libdir}/gstreamer-%{majorminor}/libgstasf.so
%{_libdir}/gstreamer-%{majorminor}/libgstcdio.so
%{_libdir}/gstreamer-%{majorminor}/libgstdvdlpcmdec.so
%{_libdir}/gstreamer-%{majorminor}/libgstdvdread.so
%{_libdir}/gstreamer-%{majorminor}/libgstdvdsub.so
%{_libdir}/gstreamer-%{majorminor}/libgstlame.so
%{_libdir}/gstreamer-%{majorminor}/libgstmad.so
%{_libdir}/gstreamer-%{majorminor}/libgstmpeg2dec.so
%{_libdir}/gstreamer-%{majorminor}/libgstrmdemux.so
%{_libdir}/gstreamer-%{majorminor}/libgstx264.so
%{_libdir}/gstreamer-%{majorminor}/libgstxingmux.so
%{_libdir}/gstreamer-%{majorminor}/libgsttwolame.so
%{_datadir}/gtk-doc/html/gst-plugins-ugly-plugins-%{majorminor}/*
%{_datadir}/gstreamer-%{majorminor}/presets/GstAmrnbEnc.prs
%{_datadir}/gstreamer-%{majorminor}/presets/GstX264Enc.prs

%changelog
* Thu Jul 10 2014 Liu Di <liudidi@gmail.com> - 1.3.90-2
- 更新到 1.3.90

* Wed Jun 25 2014 Liu Di <liudidi@gmail.com> - 1.3.3-2
- 更新到 1.3.3

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
