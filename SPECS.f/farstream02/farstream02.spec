%global gst_ver 1.0.0
%global gst_plugins_base_ver 1.0.0
%global far farstream

Name:           %{far}02
Version:	0.2.3
Release:        3%{?dist}
Summary:        Libraries for videoconferencing
Summary(zh_CN.UTF-8): 视频会议库

# Package is LGPLv2 except for a few files in /common/coverage/
License:        LGPLv2+ and GPLv2+
URL:            http://www.freedesktop.org/wiki/Software/Farstream
Source0:        http://freedesktop.org/software/%{far}/releases/%{far}/%{far}-%{version}.tar.gz
Patch0:         0001-Update-and-fix-the-default-properties-for-vp8enc.patch

BuildRequires:  libnice-devel >= 0.1.3
BuildRequires:  gstreamer1-devel >= %{gst_ver}
BuildRequires:  gstreamer1-plugins-base-devel >= %{gst_plugins_base_ver}
BuildRequires:  gupnp-igd-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  python-devel

Requires:       gstreamer1-plugins-good >= 1.0.0
Requires:       gstreamer1-plugins-bad-free >= 1.0.0


%description
%{name} is a collection of GStreamer modules and libraries for
videoconferencing.

%description -l zh_CN.UTF-8
用于视频会议的 GStreamer 模块和库。

%package        devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       gstreamer1-devel  >= %{gst_ver}
Requires:       gstreamer1-plugins-base-devel >= %{gst_plugins_base_ver}
Requires:       pkgconfig


%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n %{far}-%{version}

%build
%configure                                                              \
  --with-package-name='Fedora Farstream-0.2 package'                       \
  --with-package-origin='http://download.fedoraproject.org'             \
  --disable-static
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
magic_rpm_clean.sh

%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%doc COPYING NEWS AUTHORS
%{_libdir}/*.so.*
%dir %{_libdir}/%{far}-0.2
%{_libdir}/%{far}-0.2/libmulticast-transmitter.so
%{_libdir}/%{far}-0.2/libnice-transmitter.so
%{_libdir}/%{far}-0.2/librawudp-transmitter.so
%{_libdir}/%{far}-0.2/libshm-transmitter.so
%{_libdir}/gstreamer-1.0/libfsmsnconference.so
%{_libdir}/gstreamer-1.0/libfsrawconference.so
%{_libdir}/gstreamer-1.0/libfsrtcpfilter.so
%{_libdir}/gstreamer-1.0/libfsrtpconference.so
%{_libdir}/gstreamer-1.0/libfsvideoanyrate.so
%{_libdir}/girepository-1.0/Farstream-0.2.typelib
%dir %{_datadir}/%{far}
%dir %{_datadir}/%{far}/0.2
%dir %{_datadir}/%{far}/0.2/fsrtpconference
%dir %{_datadir}/%{far}/0.2/fsrawconference
%{_datadir}/%{far}/0.2/fsrawconference/default-element-properties
%{_datadir}/%{far}/0.2/fsrtpconference/default-codec-preferences
%{_datadir}/%{far}/0.2/fsrtpconference/default-element-properties

%files devel
%{_libdir}/libfarstream-0.2.so
%{_libdir}/pkgconfig/%{far}-0.2.pc
%{_includedir}/%{far}-0.2/%{far}/
%{_datadir}/gir-1.0/Farstream-0.2.gir
%{_datadir}/gtk-doc/html/%{far}-libs-1.0/
%{_datadir}/gtk-doc/html/%{far}-plugins-0.2/


%changelog
* Wed Apr 02 2014 Liu Di <liudidi@gmail.com> - 0.2.3-3
- 更新到 0.2.3

* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 0.2.1-3
- 为 Magic 3.0 重建

* Wed Oct 24 2012 Debarshi Ray <rishi@fedoraproject.org> - 0.2.1-2
- Update and fix the default properties for vp8enc

* Thu Oct  4 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.2.1-1
- Update to 0.2.1

* Wed Oct  3 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.2.0-2
- Drop unnecessary removal of buildroot in the install section.
- Update License info.

* Wed Sep 26 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.2.0-1
- Update to 0.2.0

* Tue Sep 25 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.1.91-1
- Initial Fedora spec.
