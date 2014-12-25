Name:           libmediaart
Version:        0.7.0
Release:        1%{?dist}
Summary:        Library for managing media art caches

License:        LGPLv2+
URL:            https://github.com/curlybeast/libmediaart
Source0:        https://download.gnome.org/sources/%{name}/0.7/%{name}-%{version}.tar.xz

BuildRequires:  pkgconfig(glib-2.0) pkgconfig(gio-2.0) pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(gdk-pixbuf-2.0)
BuildRequires:  vala-tools vala-devel


%description
Library tasked with managing, extracting and handling media art caches.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q


%build
%configure --disable-static \
  --enable-gdkpixbuf \
  --disable-qt
make %{?_smp_mflags}


%install
%make_install
find $RPM_BUILD_ROOT -name '*.la' -delete -print

#check
# requires X
#make check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc AUTHORS COPYING.LESSER NEWS
%{_libdir}/libmediaart-1.0.so.*
%{_libdir}/girepository-1.0/MediaArt-1.0.typelib

%files devel
%{_includedir}/libmediaart-1.0
%{_libdir}/libmediaart-1.0.so
%{_libdir}/pkgconfig/libmediaart-1.0.pc
%{_datadir}/gir-1.0/MediaArt-1.0.gir
%{_datadir}/gtk-doc/html/libmediaart
%{_datadir}/vala/vapi/libmediaart-1.0.vapi


%changelog
* Mon Sep 22 2014 Yanko Kaneti <yaneti@declera.com> - 0.7.0-1
- Update to 0.7.0

* Tue Aug 19 2014 Kalev Lember <kalevlember@gmail.com> - 0.6.0-1
- Update to 0.6.0

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 0.4.0-3
- Rebuilt for gobject-introspection 1.41.4

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr  1 2014 Yanko Kaneti <yaneti@declera.com> - 0.4.0-1
- Update to 0.4.0

* Fri Mar  7 2014 Yanko Kaneti <yaneti@declera.com> - 0.3.0-1
- Update to 0.3.0. Drop upstreamed patches.

* Sat Feb  8 2014 Yanko Kaneti <yaneti@declera.com> - 0.2.0-4
- Add patches to avoid unnecessary linkage

* Sat Feb  8 2014 Yanko Kaneti <yaneti@declera.com> - 0.2.0-3
- Incorporate most changes suggested in the review (#1062686)

* Fri Feb  7 2014 Yanko Kaneti <yaneti@declera.com> - 0.2.0-2
- Qt can be ignored, its only there for systems without gdk-pixbuf

* Fri Feb  7 2014 Yanko Kaneti <yaneti@declera.com> - 0.2.0-1
- Initial attempt
