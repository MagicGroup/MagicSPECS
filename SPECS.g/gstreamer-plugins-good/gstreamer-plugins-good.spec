%define         gstreamer       gstreamer
%define         majorminor      0.10

%define         _gst            0.10.36
%define         _gstpb          %{_gst}

Name:           %{gstreamer}-plugins-good
Version:        0.10.31
Release:        7%{?dist}
Summary:        GStreamer plug-ins with good code and licensing

Group:          Applications/Multimedia
License:        LGPLv2+
URL:            http://gstreamer.freedesktop.org/
#Source:         http://gstreamer.freedesktop.org/src/gst-plugins-good/pre/gst-plugins-good-%{version}.tar.xz
Source:         http://gstreamer.freedesktop.org/src/gst-plugins-good/gst-plugins-good-%{version}.tar.xz

# Cherry picks from upstream git which hopefully fix rhbz#815581
Patch1:         0001-fix-v4l2_munmap.patch
Patch2:         0002-clear_DISCONT_flag.patch
# https://bugzilla.gnome.org/show_bug.cgi?id=677516
Patch3:         0003-v4l2src-fix.patch
# https://bugzilla.gnome.org/show_bug.cgi?id=677722
Patch4:         0004-v4l2object-Don-t-probe-UVC-devices-for-being-interla.patch
Patch5:         0001-sys-v4l2-Some-blind-compilation-fixes.patch
# https://bugzilla.gnome.org/show_bug.cgi?id=724085
Patch6:         gnome-724085.patch

Requires:       %{gstreamer} >= %{_gst}
Requires(pre): GConf2 
Requires(preun): GConf2
Requires(post): GConf2
Requires:       gstreamer-plugins-base
# superceded by the package above and ourselves
Obsoletes:      gstreamer-plugins

BuildRequires:  %{gstreamer}-devel >= %{_gst}
BuildRequires:  %{gstreamer}-plugins-base-devel >= %{_gstpb}

BuildRequires:  liboil-devel >= 0.3.6
BuildRequires:  gettext
BuildRequires:  gcc-c++

BuildRequires:  cairo-devel
BuildRequires:  flac-devel >= 1.1.3
BuildRequires:  GConf2-devel
BuildRequires:  glibc-devel
BuildRequires:  gtk2-devel
BuildRequires:  kernel-headers
BuildRequires:  libjpeg-devel
BuildRequires:  libpng-devel >= 1.2.0
BuildRequires:  libshout-devel
BuildRequires:  libsoup-devel
BuildRequires:  libX11-devel
BuildRequires:  mikmod
BuildRequires:  orc-devel
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  speex-devel
BuildRequires:  taglib-devel
BuildRequires:  wavpack-devel
BuildRequires:  libv4l-devel

%ifnarch s390 s390x
BuildRequires:  libavc1394-devel
BuildRequires:  libdv-devel
BuildRequires:  libiec61883-devel
BuildRequires:  libraw1394-devel
%endif

# documentation
BuildRequires:  gtk-doc
BuildRequires:  python-devel

Provides: gstreamer-plugins-pulse = 0.9.8-1
Obsoletes: gstreamer-plugins-pulse < 0.9.8

%description
GStreamer is a streaming media framework, based on graphs of filters which
operate on media data. Applications using this library can do anything
from real-time sound processing to playing videos, and just about anything
else media-related.  Its plugin-based architecture means that new data
types or processing capabilities can be added simply by installing new
plug-ins.

GStreamer Good Plug-ins is a collection of well-supported plug-ins of
good quality and under the LGPL license.

%package devel-docs
Summary:        Documentation for gstreamer-plugins-good
Group:          Development/Libraries

Requires:       %{name} = %{version}-%{release}
# for /usr/share/gtk-doc/html
Requires:       gtk-doc
BuildArch:      noarch
# Providing the devel package here as its the docs package's old name.
# Remove this line once we get a real -devel package again.
Provides:       %{name}-devel = %{version}-%{release}
Obsoletes:       %{name}-devel < %{version}-%{release}

%description devel-docs
GStreamer is a streaming media framework, based on graphs of filters which
operate on media data. Applications using this library can do anything
from real-time sound processing to playing videos, and just about anything
else media-related.  Its plugin-based architecture means that new data
types or processing capabilities can be added simply by installing new
plug-ins.

GStreamer Good Plug-ins is a collection of well-supported plug-ins of
good quality and under the LGPL license.

This package contains documentation for the provided plugins.

%prep
%setup -q -n gst-plugins-good-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%build

%configure \
  --with-package-name='Magic gstreamer-plugins-good package' \
  --with-package-origin='http://apt.linuxfans.org/magic' \
  --enable-experimental \
  --enable-gtk-doc \
  --enable-orc \
  --disable-monoscope \
  --disable-aalib \
  --disable-esd \
  --disable-libcaca \
  --disable-hal \
  --with-default-visualizer=autoaudiosink

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
%makeinstall
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL

# Clean out files that should not be part of the rpm.
rm -f $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
magic_rpm_clean.sh
%find_lang gst-plugins-good-%{majorminor}

%files -f gst-plugins-good-%{majorminor}.lang
%defattr(-, root, root)
%doc AUTHORS COPYING README REQUIREMENTS

# Equaliser presets
%{_datadir}/gstreamer-%{majorminor}/

# non-core plugins without external dependencies
%{_libdir}/gstreamer-%{majorminor}/libgstalaw.so
%{_libdir}/gstreamer-%{majorminor}/libgstalphacolor.so
%{_libdir}/gstreamer-%{majorminor}/libgstalpha.so
%{_libdir}/gstreamer-%{majorminor}/libgstannodex.so
%{_libdir}/gstreamer-%{majorminor}/libgstapetag.so
%{_libdir}/gstreamer-%{majorminor}/libgstaudiofx.so
%{_libdir}/gstreamer-%{majorminor}/libgstaudioparsers.so
%{_libdir}/gstreamer-%{majorminor}/libgstauparse.so
%{_libdir}/gstreamer-%{majorminor}/libgstautodetect.so
%{_libdir}/gstreamer-%{majorminor}/libgstavi.so
%{_libdir}/gstreamer-%{majorminor}/libgstcutter.so
%{_libdir}/gstreamer-%{majorminor}/libgstdebug.so
%{_libdir}/gstreamer-%{majorminor}/libgstdeinterlace.so
%{_libdir}/gstreamer-%{majorminor}/libgstefence.so
%{_libdir}/gstreamer-%{majorminor}/libgsteffectv.so
%{_libdir}/gstreamer-%{majorminor}/libgstequalizer.so
%{_libdir}/gstreamer-%{majorminor}/libgstflv.so
%{_libdir}/gstreamer-%{majorminor}/libgstflxdec.so
%{_libdir}/gstreamer-%{majorminor}/libgstgoom2k1.so
%{_libdir}/gstreamer-%{majorminor}/libgstgoom.so
%{_libdir}/gstreamer-%{majorminor}/libgsticydemux.so
%{_libdir}/gstreamer-%{majorminor}/libgstid3demux.so
%{_libdir}/gstreamer-%{majorminor}/libgstimagefreeze.so
%{_libdir}/gstreamer-%{majorminor}/libgstinterleave.so
%{_libdir}/gstreamer-%{majorminor}/libgstisomp4.so
%{_libdir}/gstreamer-%{majorminor}/libgstlevel.so
%{_libdir}/gstreamer-%{majorminor}/libgstmatroska.so
%{_libdir}/gstreamer-%{majorminor}/libgstmulaw.so
%{_libdir}/gstreamer-%{majorminor}/libgstmultifile.so
%{_libdir}/gstreamer-%{majorminor}/libgstmultipart.so
%{_libdir}/gstreamer-%{majorminor}/libgstnavigationtest.so
%{_libdir}/gstreamer-%{majorminor}/libgstoss4audio.so
%{_libdir}/gstreamer-%{majorminor}/libgstreplaygain.so
%{_libdir}/gstreamer-%{majorminor}/libgstrtp.so
%{_libdir}/gstreamer-%{majorminor}/libgstrtsp.so
%{_libdir}/gstreamer-%{majorminor}/libgstshapewipe.so
%{_libdir}/gstreamer-%{majorminor}/libgstsmpte.so
%{_libdir}/gstreamer-%{majorminor}/libgstspectrum.so
%{_libdir}/gstreamer-%{majorminor}/libgstudp.so
%{_libdir}/gstreamer-%{majorminor}/libgstvideobox.so
%{_libdir}/gstreamer-%{majorminor}/libgstvideocrop.so
%{_libdir}/gstreamer-%{majorminor}/libgstvideofilter.so
%{_libdir}/gstreamer-%{majorminor}/libgstvideomixer.so
%{_libdir}/gstreamer-%{majorminor}/libgstwavenc.so
%{_libdir}/gstreamer-%{majorminor}/libgstwavparse.so
%{_libdir}/gstreamer-%{majorminor}/libgstximagesrc.so
%{_libdir}/gstreamer-%{majorminor}/libgsty4menc.so

# gstreamer-plugins with external dependencies but in the main package
%{_libdir}/gstreamer-%{majorminor}/libgstcairo.so
%{_libdir}/gstreamer-%{majorminor}/libgstflac.so
%{_libdir}/gstreamer-%{majorminor}/libgstgconfelements.so
%{_libdir}/gstreamer-%{majorminor}/libgstgdkpixbuf.so
%{_libdir}/gstreamer-%{majorminor}/libgstjpeg.so
%{_libdir}/gstreamer-%{majorminor}/libgstossaudio.so
%{_libdir}/gstreamer-%{majorminor}/libgstpng.so
%{_libdir}/gstreamer-%{majorminor}/libgstpulse.so
%{_libdir}/gstreamer-%{majorminor}/libgstrtpmanager.so
%{_libdir}/gstreamer-%{majorminor}/libgstshout2.so
%{_libdir}/gstreamer-%{majorminor}/libgstsouphttpsrc.so
%{_libdir}/gstreamer-%{majorminor}/libgstspeex.so
%{_libdir}/gstreamer-%{majorminor}/libgsttaglib.so
%{_libdir}/gstreamer-%{majorminor}/libgstvideo4linux2.so
%{_libdir}/gstreamer-%{majorminor}/libgstwavpack.so
#%{_libdir}/gstreamer-%{majorminor}/libgsthalelements.so
%{_libdir}/gstreamer-%{majorminor}/libgstjack.so

%ifnarch s390 s390x
%{_libdir}/gstreamer-%{majorminor}/libgstdv.so
%{_libdir}/gstreamer-%{majorminor}/libgst1394.so
%endif

## Libraries

# schema files
%{_sysconfdir}/gconf/schemas/gstreamer-%{majorminor}.schemas

%files devel-docs
%defattr(-, root, root)

# gtk-doc documentation
%doc %{_datadir}/gtk-doc/html/gst-plugins-good-plugins-%{majorminor}

%pre
if [ "$1" -gt 1 ]; then
  export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
  gconftool-2 --makefile-uninstall-rule %{_sysconfdir}/gconf/schemas/gstreamer-%{majorminor}.schemas > /dev/null || :
fi

%preun
if [ "$1" -eq 0 ]; then
  export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
  gconftool-2 --makefile-uninstall-rule %{_sysconfdir}/gconf/schemas/gstreamer-%{majorminor}.schemas > /dev/null || :
fi

%post
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/gstreamer-%{majorminor}.schemas > /dev/null || :

%changelog
* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 0.10.31-7
- 为 Magic 3.0 重建

* Thu Apr 17 2014 Liu Di <liudidi@gmail.com> - 0.10.31-6
- 为 Magic 3.0 重建

* Thu Apr 17 2014 Liu Di <liudidi@gmail.com> - 0.10.31-5
- 为 Magic 3.0 重建

* Fri Apr 11 2014 Liu Di <liudidi@gmail.com> - 0.10.31-4
- 为 Magic 3.0 重建

* Tue Jun 18 2013 Liu Di <liudidi@gmail.com> - 0.10.31-3
- 移除 hal 支持。

* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 0.10.31-2
- 为 Magic 3.0 重建


