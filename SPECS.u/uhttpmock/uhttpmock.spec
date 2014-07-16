%global glib2_version 2.31.0
%global libsoup_version 2.37.91

# Packagers: This is the API version of libuhttpmock, as it allows
# for parallel installation of different major API versions (e.g. like
# GTK+ 2 and 3).
%global uhm_api_version 0.0

Name:           uhttpmock
Version:        0.3.0
Release:        1%{?dist}
Summary:        HTTP web service mocking library
License:        LGPLv2
URL:            http://gitorious.org/uhttpmock/
Source0:        http://tecnocode.co.uk/downloads/%{name}-%{version}.tar.xz

BuildRequires:  glib2-devel >= %{glib2_version}
BuildRequires:  libsoup-devel >= %{libsoup_version}
BuildRequires:  intltool
BuildRequires:  gobject-introspection-devel
BuildRequires:  gtk-doc
BuildRequires:  vala-tools
BuildRequires:  vala-devel

Requires:       glib2 >= %{glib2_version}
Requires:       libsoup >= %{libsoup_version}

%description
uhttpmock is a project for mocking web service APIs which use HTTP or HTTPS.
It provides a library, libuhttpmock, which implements recording and
playback of HTTP request–response traces.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains libraries, header files and documentation for
developing applications that use %{name}.

%prep
%setup -q

%build
%configure \
    --enable-gtk-doc \
    --enable-introspection \
    --enable-vala=yes \
    --disable-static
make %{?_smp_mflags}

%check
make check

%install
make DESTDIR=$RPM_BUILD_ROOT install

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc README COPYING NEWS AUTHORS
%{_libdir}/libuhttpmock-%{uhm_api_version}.so.0*
%{_libdir}/girepository-1.0/Uhm-%{uhm_api_version}.typelib

%files devel
%{_libdir}/libuhttpmock-%{uhm_api_version}.so
%{_includedir}/libuhttpmock-%{uhm_api_version}/
%{_libdir}/pkgconfig/libuhttpmock-%{uhm_api_version}.pc
%{_datadir}/gir-1.0/Uhm-%{uhm_api_version}.gir
%{_datadir}/vala/vapi/libuhttpmock-%{uhm_api_version}.deps
%{_datadir}/vala/vapi/libuhttpmock-%{uhm_api_version}.vapi
%doc %{_datadir}/gtk-doc/html/libuhttpmock-%{uhm_api_version}/

%changelog
* Sun Jun 22 2014 Philip Withnall <philip@tecnocode.co.uk> - 0.3.0-1
- Update to 0.3.0

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Nov 05 2013 Philip Withnall <philip.withnall@collabora.co.uk> - 0.2.0-1
- Initial spec file for version 0.2.0.
