Name:           clutter-gst3
Version:        3.0.12
Release:        3%{?dist}
Summary:        GStreamer integration library for Clutter
Summary(zh_CN.UTF-8): Clutter 的 GStreamer 集成库

Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
License:        LGPLv2+
URL:            https://developer.gnome.org/clutter-gst/stable/
Source0:        https://download.gnome.org/sources/clutter-gst/3.0/clutter-gst-%{version}.tar.xz

BuildRequires: /usr/bin/chrpath
BuildRequires: pkgconfig(clutter-1.0)
BuildRequires: pkgconfig(cogl-2.0-experimental)
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: pkgconfig(gobject-introspection-1.0)
BuildRequires: pkgconfig(gstreamer-1.0)
BuildRequires: pkgconfig(gstreamer-audio-1.0)
BuildRequires: pkgconfig(gstreamer-base-1.0)
BuildRequires: pkgconfig(gstreamer-pbutils-1.0)
BuildRequires: pkgconfig(gstreamer-plugins-base-1.0)
BuildRequires: pkgconfig(gstreamer-tag-1.0)
BuildRequires: pkgconfig(gstreamer-video-1.0)
BuildRequires: pkgconfig(gudev-1.0)


%description
Clutter is an open source software library for creating fast, visually
rich and animated graphical user interfaces.

Clutter GStreamer enables the use of GStreamer with Clutter.

%description -l zh_CN.UTF-8
Clutter 的 GStreamer 集成库。

%package        devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Clutter is an open source software library for creating fast, visually
rich and animated graphical user interfaces.

Clutter GStreamer enables the use of GStreamer with Clutter.

The %{name}-devel package contains libraries and header files for
developing applications that use clutter-gst API version 3.0.
%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n clutter-gst-%{version}


%build
%configure
make %{?_smp_mflags} V=1


%install
make install DESTDIR=%{buildroot} INSTALL="install -p"

find %{buildroot} -name '*.la' -delete

rm -rf %{buildroot}%{_libdir}/gstreamer-1.0/
magic_rpm_clean.sh

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc AUTHORS NEWS README
%license COPYING
%{_libdir}/girepository-1.0/ClutterGst-3.0.typelib
%{_libdir}/libclutter-gst-3.0.so.*

%files devel
%{_includedir}/clutter-gst-3.0/
%{_libdir}/libclutter-gst-3.0.so
%{_libdir}/pkgconfig/clutter-gst-3.0.pc
%{_datadir}/gir-1.0/ClutterGst-3.0.gir
%doc %{_datadir}/gtk-doc/



%changelog
* Sun Oct 04 2015 Liu Di <liudidi@gmail.com> - 3.0.12-3
- 为 Magic 3.0 重建

* Sun Oct 04 2015 Liu Di <liudidi@gmail.com> - 3.0.12-2
- 为 Magic 3.0 重建

* Wed Sep 30 2015 David King <amigadave@amigadave.com> - 3.0.12-1
- Update to 3.0.12

* Fri Sep 04 2015 David King <amigadave@amigadave.com> - 3.0.10-1
- Update to 3.0.10

* Sun Jul 19 2015 David King <amigadave@amigadave.com> - 3.0.8-1
- Update to 3.0.8

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 25 2015 David King <amigadave@amigadave.com> - 3.0.6-1
- Update to 3.0.6

* Fri Mar 27 2015 Bastien Nocera <bnocera@redhat.com> - 3.0.4-2
- Remove the GStreamer plugin, as it can cause the one in the
  clutter-gst2 package to become unavailable, breaking Cheese
  https://bugzilla.gnome.org/show_bug.cgi?id=746883

* Sun Feb 22 2015 David King <amigadave@amigadave.com> - 3.0.4-1
- Initial packaging (#1190361)
