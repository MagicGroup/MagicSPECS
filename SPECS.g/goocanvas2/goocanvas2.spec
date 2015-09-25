%global tarname goocanvas
%global apiver  2.0

Name:           goocanvas2
Version:        2.0.2
Release:        5%{?dist}
Summary:        A new canvas widget for GTK+ that uses cairo for drawing

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://live.gnome.org/GooCanvas
Source0:        https://download.gnome.org/sources/goocanvas/2.0/goocanvas-%{version}.tar.xz

BuildRequires:  gettext, pkgconfig
BuildRequires:  gtk3-devel >= 2.91.3
BuildRequires:  cairo-devel >= 1.4.0
BuildRequires:  gobject-introspection-devel
# For the girepository-1.0 directory
Requires:       gobject-introspection

%description
GooCanvas is a new canvas widget for GTK+ that uses the cairo 2D library for
drawing. It has a model/view split, and uses interfaces for canvas items and
views, so you can easily turn any application object into canvas items.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?isa} = %{version}-%{release}
Requires:       gobject-introspection-devel

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n goocanvas-%{version}


%build
# python GI wrapper is not enabled yet until i figure a proper way to package it
%configure --disable-static \
           --enable-python=no
make %{?_smp_mflags}


%install
make install DESTDIR=%buildroot
find %buildroot -name '*.la' -exec rm -f {} ';'
%find_lang %{name}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files  -f %{name}.lang
%doc COPYING README ChangeLog AUTHORS NEWS TODO
%{_libdir}/*.so.*
%{_libdir}/girepository-1.0/GooCanvas-2.0.typelib

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{tarname}-%{apiver}.pc
%{_datadir}/gtk-doc/html/%{name}
%{_datadir}/gir-1.0/GooCanvas-2.0.gir

%changelog
* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 2.0.2-3
- Rebuilt for gobject-introspection 1.41.4

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat May 17 2014 Kalev Lember <kalevlember@gmail.com> - 2.0.2-1
- Update to 2.0.2

* Wed Aug 07 2013 Haïkel Guémar <hguemar@fedoraproject.org> - 2.0.1-6.8f2c63git
- backport gobject introspection fixes from GNOME git
- fix FTBFS (RHBZ #992421)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Oct 10 2011 Haïkel Guémar <hguemar@fedoraproject.org> - 2.0.1-1
- upstream 2.0.1
- remove upstreamed patch and enable GIR

* Fri Feb 11 2011 Haïkel Guémar <hguemar@fedoraproject.org> - 1.90.2-1
- initial package
