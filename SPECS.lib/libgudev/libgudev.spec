Name:           libgudev
Version:        230
Release:        4%{?dist}
Summary:        GObject-based wrapper library for libudev

License:        LGPLv2+
URL:            https://wiki.gnome.org/Projects/libgudev
Source0:        https://download.gnome.org/sources/libgudev/%{version}/libgudev-%{version}.tar.xz

BuildRequires:  glib2-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  pkgconfig
BuildRequires:  libudev-devel
BuildRequires:  gtk-doc

# Upstream promises to remove libgudev from systemd before this version
Provides:       libgudev1 = %{version}-%{release}
Obsoletes:      libgudev1 < 230

%description
This library makes it much simpler to use libudev from programs
already using GObject. It also makes it possible to easily use libudev
from other programming languages, such as Javascript, because of
GObject introspection support.

%package devel
Summary:   Header files for %{name}
Requires:  %{name}%{?_isa} = %{version}-%{release}

Provides:       libgudev1-devel = %{version}-%{release}
Obsoletes:      libgudev1-devel < 230

%description devel
This package is necessary to build programs using %{name}.

%prep
%setup -q

%build
%configure --enable-gtk-doc
make %{?_smp_mflags}

%install
%makeinstall
rm %{buildroot}%{_libdir}/*.la

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license COPYING
%doc NEWS
%{_libdir}/libgudev-1.0.so.*
%{_libdir}/girepository-1.0/GUdev-1.0.typelib

%files devel
%{_libdir}/libgudev-1.0.so
%dir %{_includedir}/gudev-1.0
%dir %{_includedir}/gudev-1.0/gudev
%{_includedir}/gudev-1.0/gudev/*.h
%{_datadir}/gir-1.0/GUdev-1.0.gir
%dir %{_datadir}/gtk-doc/html/gudev
%{_datadir}/gtk-doc/html/gudev/*
%{_libdir}/pkgconfig/gudev-1.0*


%changelog
* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 230-4
- 为 Magic 3.0 重建

* Wed Sep 30 2015 Liu Di <liudidi@gmail.com> - 230-3
- 为 Magic 3.0 重建

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 230-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun May 31 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 230-1
- Initial packaging
