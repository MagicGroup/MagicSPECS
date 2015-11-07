Summary:   GTK support library for colord
Summary(zh_CN.UTF-8): colord 的 GTK 支持库
Name:      colord-gtk
Version:	0.1.26
Release:   2%{?dist}
License:   LGPLv2+
URL:       http://www.freedesktop.org/software/colord/
Source0:   http://www.freedesktop.org/software/colord/releases/%{name}-%{version}.tar.xz

BuildRequires: docbook-utils
BuildRequires: gettext
BuildRequires: glib2-devel
BuildRequires: colord-devel >= 0.1.23
BuildRequires: intltool
BuildRequires: lcms2-devel >= 2.2
BuildRequires: gobject-introspection-devel
BuildRequires: vala-tools
BuildRequires: gtk3-devel
BuildRequires: gtk-doc

%description
colord-gtk is a support library for colord and provides additional
functionality that requires GTK+.

%description -l zh_CN.UTF-8
colord 的 GTK 支持库，提供了需要 GTK+ 支持的额外函数。

%package devel
Summary: Development package for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Files for development with %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q

%build
%configure \
        --disable-gtk-doc \
        --enable-vala \
        --disable-static \
        --disable-rpath \
        --disable-dependency-tracking

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

# Remove static libs and libtool archives.
find %{buildroot} -name '*.la' -exec rm -f {} ';'
find %{buildroot} -name '*.a' -exec rm -f {} ';'

%find_lang %{name}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{name}.lang
%doc README AUTHORS NEWS COPYING
%{_libdir}/libcolord-gtk.so.*
%{_libdir}/girepository-1.0/ColordGtk-1.0.typelib

%files devel
%{_libdir}/libcolord-gtk.so
%{_libdir}/pkgconfig/colord-gtk.pc
%dir %{_includedir}/colord-1
%{_includedir}/colord-1/colord-gtk.h
%dir %{_includedir}/colord-1/colord-gtk
%{_includedir}/colord-1/colord-gtk/*.h
%dir %{_datadir}/gir-1.0
%{_datadir}/gir-1.0/ColordGtk-1.0.gir
#%doc %{_datadir}/gtk-doc/html/colord-gtk
%{_datadir}/vala/vapi/colord-gtk.vapi
#%dir %{_datadir}/gtk-doc
#%dir %{_datadir}/gtk-doc/html

%changelog
* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 0.1.26-2
- 更新到 0.1.26

* Tue Mar 19 2013 Richard Hughes <richard@hughsie.com> 0.1.25-1
- New upstream version.
- Give the sample widget slightly curved corners and a gray outline
- Do not use deprecated functions from libcolord
- Fix warnings when building ColordGtk-1.0.gir
- Fix up the licence boilerplate for CdSampleWidget

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Dec 17 2012 Richard Hughes <richard@hughsie.com> 0.1.24-1
- New upstream version.

* Wed Aug 29 2012 Richard Hughes <richard@hughsie.com> 0.1.23-1
- New upstream version.
- Remove upstreamed patch
- Add include guards to cd-sample-window.h

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 27 2012 Richard Hughes <richard@hughsie.com> 0.1.22-2
- Backport a patch from git master that fixes an include issue with
  projects that want to use colord-gtk.h and colord.h at the same time.

* Tue Jun 26 2012 Richard Hughes <richard@hughsie.com> 0.1.22-1
- New version after Fedora package review.

* Mon Jun 18 2012 Richard Hughes <richard@hughsie.com> 0.1.1-1
- Initial version for Fedora package review.
