Name:           clutter-gst2
Version:	2.0.16
Release:        2%{?dist}
Summary:        GStreamer integration for Clutter

License:        LGPLv2+
URL:            http://www.clutter-project.org
%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
Source0:        http://ftp.gnome.org/pub/GNOME/sources/clutter-gst/%{majorver}/clutter-gst-%{version}.tar.xz

BuildRequires:  clutter-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  gstreamer1-devel
BuildRequires:  gstreamer1-plugins-base-devel

%description
Clutter is an open source software library for creating fast, visually
rich and animated graphical user interfaces.

Clutter GStreamer enables the use of GStreamer with Clutter.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Clutter is an open source software library for creating fast, visually
rich and animated graphical user interfaces.

Clutter GStreamer enables the use of GStreamer with Clutter.

The %{name}-devel package contains libraries and header files for
developing applications that use clutter-gst API version 2.0.

%prep
%setup -q -n clutter-gst-%{version}

%build
%configure
make %{?_smp_mflags} V=1

%install
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

# Remove the documentation for now as it conflicts with the files in
# clutter-gst-devel. I'll work with upstream to fix this properly.
rm -rf $RPM_BUILD_ROOT%{_datadir}/gtk-doc/

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc AUTHORS COPYING README
%{_libdir}/girepository-1.0/ClutterGst-2.0.typelib
%{_libdir}/gstreamer-1.0/libgstclutter.so
%{_libdir}/libclutter-gst-2.0.so.*

%files devel
%{_includedir}/clutter-gst-2.0/
%{_libdir}/libclutter-gst-2.0.so
%{_libdir}/pkgconfig/clutter-gst-2.0.pc
%{_datadir}/gir-1.0/ClutterGst-2.0.gir
#doc #{_datadir}/gtk-doc/

%changelog
* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 2.0.16-2
- 为 Magic 3.0 重建

* Sun Oct 04 2015 Liu Di <liudidi@gmail.com> - 2.0.16-1
- 更新到 2.0.16

* Thu Feb 20 2014 Kalev Lember <kalevlember@gmail.com> - 2.0.10-3
- Rebuilt for cogl soname bump

* Mon Feb 10 2014 Peter Hutterer <peter.hutterer@redhat.com> - 2.0.10-2
- Rebuild for libevdev soname bump

* Mon Jan 20 2014 Richard Hughes <rhughes@redhat.com> - 2.0.10-1
- Update to 2.0.10

* Wed Sep 18 2013 Kalev Lember <kalevlember@gmail.com> - 2.0.8-1
- Update to 2.0.8

* Fri Aug 09 2013 Kalev Lember <kalevlember@gmail.com> - 2.0.6-3
- Rebuilt for cogl 1.15.4 soname bump

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 23 2013 Kalev Lember <kalevlember@gmail.com> - 2.0.6-1
- Update to 2.0.6

* Sat May 25 2013 Kalev Lember <kalevlember@gmail.com> - 2.0.4-1
- Update to 2.0.4

* Tue Feb 26 2013 Kalev Lember <kalevlember@gmail.com> - 2.0.2-1
- Update to 2.0.2

* Thu Feb 21 2013 Kalev Lember <kalevlember@gmail.com> - 2.0.0-3
- Rebuilt for cogl soname bump

* Fri Jan 25 2013 Peter Robinson <pbrobinson@fedoraproject.org> 2.0.0-2
- Rebuild for new cogl

* Thu Jan 24 2013 Peter Robinson <pbrobinson@fedoraproject.org> 2.0.0-1
- Update to 2.0.0

* Tue Sep 25 2012 Matthias Clasen <mclasen@redhat.com> - 1.9.92-1
- Update to 1.9.92

* Wed Sep 19 2012 Kalev Lember <kalevlember@gmail.com> - 1.9.90-2
- Rebuilt with gstreamer1 0.11.99

* Wed Aug 29 2012 Kalev Lember <kalevlember@gmail.com> - 1.9.90-1
- Initial clutter-gst2 packaging, based on Fedora clutter-gst (#852778)
