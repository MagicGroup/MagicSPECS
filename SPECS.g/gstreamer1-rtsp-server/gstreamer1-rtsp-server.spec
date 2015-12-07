%global         majorminor      1.0

Name:           gstreamer1-rtsp-server
Version:        1.6.1
Release:        1%{?dist}
Summary:        GStreamer RTSP server library

Group:          Applications/Multimedia
License:        LGPLv2+
URL:            http://gstreamer.freedesktop.org/
Source0:        http://gstreamer.freedesktop.org/src/gst-rtsp/gst-rtsp-server-%{version}.tar.xz

BuildRequires:  gstreamer1-devel >= %{version}
BuildRequires:  gstreamer1-plugins-base-devel >= %{version}
BuildRequires:  gobject-introspection-devel
BuildRequires:  chrpath

BuildRequires:  automake autoconf libtool

# documentation
BuildRequires:  gtk-doc >= 1.3

Requires:       gstreamer1%{?_isa} >= %{version}
Requires:       gstreamer1-plugins-base%{?_isa} >= %{version}

%description
A GStreamer-based RTSP server library.

%package devel
Summary:        Development files for %{name}
Group:          Development/Libraries
License:        LGPLv2+
Requires:       gstreamer1-devel%{?_isa} >= %{version}
Requires:       gstreamer1-plugins-base-devel%{?_isa} >= %{version}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for %{name}, the GStreamer RTSP server library.

%package devel-docs
Summary:         Developer documentation for GStreamer-based RTSP server library
Requires:        %{name} = %{version}-%{release}
BuildArch:       noarch

%description devel-docs
This %{name}-devel-docs contains developer documentation for the
GStreamer-based RTSP server library.

%prep
%setup -q -n gst-rtsp-server-%{version}

autoreconf -fiv

%build
%configure  --enable-gtk-doc --disable-static --disable-tests

make %{?_smp_mflags} V=1

%check
make check

%install
%make_install

#Remove libtool archives
find %{buildroot} -name '*.la' -exec rm -f {} ';'

# Remove rpath as per https://fedoraproject.org/wiki/Packaging/Guidelines#Beware_of_Rpath
# can't tweak libtool, see:
# https://bugzilla.gnome.org/show_bug.cgi?id=634376#c1
chrpath --delete %{buildroot}%{_libdir}/libgstrtspserver-%{majorminor}.so*

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license COPYING.LIB
%doc README TODO NEWS
%dir %{_libdir}/girepository-1.0/
%{_libdir}/libgstrtspserver-%{majorminor}.so.*
%{_libdir}/girepository-1.0/GstRtspServer-%{majorminor}.typelib

%files devel
%dir %{_datadir}/gir-1.0/
%{_includedir}/gstreamer-%{majorminor}/gst/rtsp-server
%{_libdir}/libgstrtspserver-%{majorminor}.so
%{_libdir}/pkgconfig/gstreamer-rtsp-server-%{majorminor}.pc
%{_datadir}/gir-1.0/GstRtspServer-%{majorminor}.gir

%files devel-docs
%dir %{_datadir}/gtk-doc/
%dir %{_datadir}/gtk-doc/html/
%doc %{_datadir}/gtk-doc/html/gst-rtsp-server-%{majorminor}

%changelog
* Mon Nov 2 2015 Wim Taymans <wtaymans@redhat.com> - 1.6.1-1
- update to 1.6.1

* Sat Sep 26 2015 Kalev Lember <klember@redhat.com> - 1.6.0-1
- Update to 1.6.0

* Tue Sep 22 2015 Wim Taymans <wtaymans@redhat.com> - 1.5.91-1
- update to 1.5.91

* Thu Aug 20 2015 Wim Taymans <wtaymans@redhat.com> - 1.5.90-1
- update to 1.5.90
- remove obsolete patch

* Thu Aug 20 2015 Wim Taymans <wtaymans@redhat.com> - 1.4.5-1
- update to 1.4.5
- add double unlock patch
- fix devel-docs requires

* Thu Aug 20 2015 Wim Taymans <wtaymans@redhat.com> - 1.4.0-5
- disable checks

* Fri Jul 24 2015 Wim Taymans <wtaymans@redhat.com> - 1.4.0-4
- Fix Changelog entry
- Fix wrong comment about introspection
- disable-static instead of building and then removing .a files
- mark COPYING.LIB as license
- don't use thr rtsp-server majorminor for gobject instrospection versions
- add devel-docs directories

* Tue Mar 3 2015 Wim Taymans <wtaymans@redhat.com> - 1.4.0-3
- Add docs
- style updates: autoreconf -fiv and make_install

* Tue Aug 19 2014 Stefan Ringel <linuxtv@stefanringel.de> - 1.4.0-2
- Fix depedencies
- Fix file permission

* Thu Aug 14 2014 Wim Taymans <wtaymans@redhat.com> - 1.4.0-1
- Use majorminor, like the other GStreamer packages
- Fix project URL and description
- Include all .so file versions

* Wed Aug 13 2014 Stefan Ringel <linuxtv@stefanringel.de> - 1.4.0-0
- First version
