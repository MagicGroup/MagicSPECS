Name:           libmediaart
Version:        0.2.0
Release:        4%{?dist}
Summary:        Library for managing media art caches

License:        LGPLv2+
URL:            https://github.com/curlybeast/libmediaart
Source0:        https://download.gnome.org/sources/%{name}/0.2/%{name}-%{version}.tar.xz

# upstreamd patches to avoid unncesarry linkage
# https://bugzilla.gnome.org/show_bug.cgi?id=723877
Patch1:         0001-configure-Don-t-link-to-both-Qt-and-gdk-pixbuf-if-bo.patch
Patch2:         0002-build-Remove-leftover-explicit-lm-lz-linkage.patch
Patch3:         0003-build-Force-automake-C-linkage-when-building-C-only.patch

BuildRequires:  pkgconfig(glib-2.0) pkgconfig(gio-2.0) pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(gdk-pixbuf-2.0)
BuildRequires:  vala-tools vala-devel
#for the autoreconf
BuildRequires:  automake autoconf libtool


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
%patch1 -p1
%patch2 -p1
%patch3 -p1
autoreconf -fi


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
* Sat Feb  8 2014 Yanko Kaneti <yaneti@declera.com> - 0.2.0-4
- Add patches to avoid unnecessary linkage

* Sat Feb  8 2014 Yanko Kaneti <yaneti@declera.com> - 0.2.0-3
- Incorporate most changes suggested in the review (#1062686)

* Fri Feb  7 2014 Yanko Kaneti <yaneti@declera.com> - 0.2.0-2
- Qt can be ignored, its only there for systems without gdk-pixbuf

* Fri Feb  7 2014 Yanko Kaneti <yaneti@declera.com> - 0.2.0-1
- Initial attempt
