Name:           gstreamer1-libav
Version:	1.3.90
Release:        1%{?dist}
Summary:        GStreamer FFmpeg-based plug-ins
Summary(zh_CN.UTF-8): GStreamer FFmpeg 插件
Group:          Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
# the ffmpeg plugin is LGPL, the postproc plugin is GPL
License:        GPLv2+ and LGPLv2+
URL:            http://gstreamer.freedesktop.org/
Source:         http://gstreamer.freedesktop.org/src/gst-libav/gst-libav-%{version}.tar.xz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  gstreamer-devel >= 0.10.0
BuildRequires:  gstreamer-plugins-base-devel >= 0.10.0
BuildRequires:  ffmpeg-devel liboil-devel bzip2-devel

%description
GStreamer is a streaming media framework, based on graphs of filters which
operate on media data. Applications using this library can do anything
from real-time sound processing to playing videos, and just about anything
else media-related.  Its plugin-based architecture means that new data
types or processing capabilities can be added simply by installing new 
plugins.

This package provides FFmpeg-based GStreamer plug-ins.

%description -l zh_CN.UTF-8
GStreamer FFmpeg 插件。

%prep
%setup -q -n gst-libav-%{version}


%build
%configure --disable-dependency-tracking --disable-static \
  --with-package-name="gst-plugins-libav" \
  --with-package-origin="http://www.magiclinux.org/" \
  --with-system-ffmpeg
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/gstreamer-1.0/libgst*.la


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog NEWS README TODO
%{_libdir}/gstreamer-1.0/libgstlibav.so
#%{_libdir}/gstreamer-1.0/libgstavscale.so
%{_datadir}/gtk-doc/html/gst-libav-plugins-1.0/*

%changelog
* Thu Jul 10 2014 Liu Di <liudidi@gmail.com> - 1.3.90-1
- 更新到 1.3.90

* Wed Jun 25 2014 Liu Di <liudidi@gmail.com> - 1.3.3-1
- 更新到 1.3.3

* Fri Apr 11 2014 Liu Di <liudidi@gmail.com> - 1.2.3-1
- 更新到 1.2.3

* Fri Jan 11 2013 Liu Di <liudidi@gmail.com> - 0.10.13-2
- 为 Magic 3.0 重建

