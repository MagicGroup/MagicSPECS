%global json_glib_version 0.16.2

Name:           geocode-glib
Version:	3.12.0
Release:        1%{?dist}
Summary:        Geocoding helper library
Summary(zh_CN.UTF-8): 地理编码辅助库

License:        LGPLv2+
URL:            http://www.gnome.org/
%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
Source0:        http://download.gnome.org/sources/geocode-glib/%{majorver}/geocode-glib-%{version}.tar.xz

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

%description -l zh_CN.UTF-8
这是一个方便的库，可以处理地理编码（从地址找到对应的经纬度）和反向地理编码（从
经纬度找地址）。它使用 Nominatim 服务来实现这个目标。它也缓存有关请求以便更快
的取得结果和减轻服务器负载。

%package        devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q


%build
%configure --disable-static
make %{?_smp_mflags} V=1


%install
%make_install
find $RPM_BUILD_ROOT -name '*.la' -delete
magic_rpm_clean.sh

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
* Sun Apr 06 2014 Liu Di <liudidi@gmail.com> - 3.12.0-1
- 更新到 3.12.0

* Sun Apr 06 2014 Liu Di <liudidi@gmail.com> - 3.11.92-1
- 更新到 3.11.92

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
