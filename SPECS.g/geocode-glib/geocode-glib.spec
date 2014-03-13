%global json_glib_version 0.16.2

Name:           geocode-glib
Version:        3.11.5
Release:        1%{?dist}
Summary:        Geocoding helper library

License:        LGPLv2+
URL:            http://www.gnome.org/
Source0:        http://download.gnome.org/sources/geocode-glib/3.11/geocode-glib-%{version}.tar.xz

BuildRequires:  glib2-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  intltool
BuildRequires:  json-glib-devel >= %{json_glib_version}
BuildRequires:  libsoup-devel

Requires:       json-glib%{?_isa} >= %{json_glib_version}

%description
geocode-glib is a convenience library for the geocoding (finding longitude,
and latitude from an address) and reverse geocoding (finding an address from
coordinates). It uses Nominatim service to achieve that. It also caches
(reverse-)geocoding requests for faster results and to avoid unnecessary server
load.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q


%build
%configure --disable-static
make %{?_smp_mflags} V=1


%install
%make_install
find $RPM_BUILD_ROOT -name '*.la' -delete


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc AUTHORS COPYING.LIB NEWS README
%{_libdir}/libgeocode-glib.so.*
%{_libdir}/girepository-1.0/GeocodeGlib-1.0.typelib

%files devel
%{_includedir}/geocode-glib-1.0/
%{_libdir}/libgeocode-glib.so
%{_libdir}/pkgconfig/geocode-glib-1.0.pc
%{_datadir}/gir-1.0/GeocodeGlib-1.0.gir
%{_datadir}/icons/gnome/scalable/places/*.svg
%doc %{_datadir}/gtk-doc/

%changelog
* Wed Feb 05 2014 Richard Hughes <rhughes@redhat.com> - 3.11.5-1
- Update to 3.11.5

* Wed Jan 15 2014 Richard Hughes <rhughes@redhat.com> - 3.11.4.1-1
- Update to 3.11.4.1

* Tue Sep 24 2013 Kalev Lember <kalevlember@gmail.com> - 3.10.0-1
- Update to 3.10.0
- Specify minimum json-glib version

* Wed Sep 18 2013 Kalev Lember <kalevlember@gmail.com> - 0.99.4-1
- Update to 0.99.4

* Tue Sep 03 2013 Kalev Lember <kalevlember@gmail.com> - 0.99.3-1
- Update to 0.99.3

* Sat Aug 31 2013 Kalev Lember <kalevlember@gmail.com> - 0.99.2-2
- Move the pkgconfig file to -devel

* Fri Aug 23 2013 Kalev Lember <kalevlember@gmail.com> - 0.99.2-1
- Initial Fedora packaging
