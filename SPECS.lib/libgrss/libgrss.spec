Name:          libgrss
Version:       0.7.0
Release:       1%{?dist}
Summary:       Library for easy management of RSS/Atom/Pie feeds

License:       LGPLv3+
URL:           https://wiki.gnome.org/Projects/Libgrss
Source0:       https://download.gnome.org/sources/%{name}/0.7/%{name}-%{version}.tar.xz

BuildRequires: gcc
BuildRequires: intltool
BuildRequires: gtk-doc
BuildRequires: pkgconfig(gobject-introspection-1.0)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(libsoup-2.4)
BuildRequires: pkgconfig(libxml-2.0)

%description
libgrss is a Glib abstaction to handle feeds in RSS, Atom and other formats.

%package       devel
Summary:       Development files for %{name}
Requires:      %{name}%{?_isa} = %{version}-%{release}

%description   devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup

%build
%configure --disable-static --disable-silent-rules --enable-gtk-doc
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/%{name}.la

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license COPYING
%{_libdir}/%{name}.so.*
%{_libdir}/girepository-1.0/Grss-0.7.typelib

%files devel
%{_libdir}/%{name}.so
%{_includedir}/%{name}/
%{_libdir}/pkgconfig/%{name}.pc
%{_datadir}/gir-1.0/Grss-0.7.gir
%{_datadir}/gtk-doc/html/%{name}/

%changelog
* Sun Jul 19 2015 Igor Gnatenko <ignatenko@src.gnome.org> - 0.7.0-1
- 0.7.0

* Tue Jul 14 2015 Igor Gnatenko <ignatenko@src.gnome.org> - 0.6-2
- Add patch for fix gobject-introspection

* Tue Jul 07 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.6-1
- Initial package
