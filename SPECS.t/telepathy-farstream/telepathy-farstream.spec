Name:           telepathy-farstream
Version:        0.6.0
Release:        4%{?dist}
Summary:        Telepathy client library to handle Call channels

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://telepathy.freedesktop.org/wiki/Telepathy-Farsight
Source0:        http://telepathy.freedesktop.org/releases/%{name}/%{name}-%{version}.tar.gz

BuildRequires:  telepathy-glib-devel >= 0.19.0
BuildRequires:  farstream02-devel >= 0.2.0
BuildRequires:  dbus-devel
BuildRequires:  dbus-glib-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  python-devel

## Obsolete telepathy-farsight(-python) with Fedora 17.
Provides:       telepathy-farsight = %{version}
Obsoletes:      telepathy-farsight < 0.0.20
Provides:       telepathy-farsight-python = %{version}
Obsoletes:      telepathy-farsight-python < 0.0.20
# Obsolete telepathy-farstream-python with Fedora 18 since gobject-introspection is
# provided now
Provides:       %{name}-python = %{version}
Obsoletes:      %{name}-python < 0.6.0


%description
%{name} is a Telepathy client library that uses Farstream to handle
Call channels.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       telepathy-glib-devel >= 0.19.0
Requires:       farstream02-devel >= 0.2.0
Requires:       dbus-devel
Requires:       dbus-glib-devel
Requires:       pkgconfig

## Obsolete telepathy-farsight with Fedora 17
Provides:       telepathy-farsight-devel = %{version}
Obsoletes:      telepathy-farsight-devel < 0.0.20


%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q


%build
%configure --enable-static=no
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%check
make check


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%doc NEWS README COPYING
%{_libdir}/libtelepathy-farstream*.so.*
%{_libdir}/girepository-1.0/TelepathyFarstream-0.6.typelib


%files devel
%doc %{_datadir}/gtk-doc/html/%{name}/
%{_libdir}/libtelepathy-farstream.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/telepathy-1.0/%{name}/
%{_datadir}/gir-1.0/TelepathyFarstream-0.6.gir


%changelog
* Fri Feb 14 2014 Debarshi Ray <rishi@fedoraproject.org> - 0.6.0-4
- Add %%check to run the upstream test suite on each build

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Oct  3 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.6.0-1
- Update to 0.6.0
- Drop python subpackage. gobject-introspection is used now.
- Drop unnecessary buildroot cleaning in install section.
- Update BR for farstream02-devel.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Apr 05 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.4.0-2
- Rebuild against farstream

* Thu Apr  5 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.4.0-1
- Update to 0.4.0.

* Tue Apr 03 2012 Brian Pepple <bpepple@fedoraproject.org. - 0.2.3-2
- Rebuild against new tp-glib.

* Tue Mar 20 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.2.3-1
- Update to 0.2.3.

* Tue Mar 13 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.2.2-2
- Add obsolete/provides on python subpackage.

* Fri Mar  9 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.2.2-1
- Update 0.2.2.

* Wed Mar  7 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.2.1-3
- Enable python bindings.

* Mon Mar  5 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.2.1-2
- Use macro for version in provides.
- Change reference Farsight in description to Farstream.

* Sun Mar  4 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.2.1-1
- Update to 0.2.1.
- Add BR on farstream-devel.
- Bump minimum version of tp-glib.
- Add obsolete/provide on telepathy-farsight.

* Mon Nov 21 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.1.2-1
- Initial Fedora spec file.
- Disable the python bindings for now.

