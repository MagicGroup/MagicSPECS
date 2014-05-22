# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

%define _soname_glib 4
%define _soname_gtk2 4
%define _soname_gtk3 4
%define _soname_jsonloader 4

Name:		libdbusmenu
Version:	12.10.2
Release:	1.1
License:	GPL-3.0 and LGPL-2.0 and LGPL-3.0
Summary:	Small library that passes a menu structure across DBus
Url:		https://launchpad.net/dbusmenu
Group:		System/Libraries
Source:		https://launchpad.net/dbusmenu/12.10/%{version}/+download/libdbusmenu-%{version}.tar.gz

Patch0:		0001_Fix_sgml.patch
Patch1:		libdbusmenu-12.10.2-glib.patch

BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	vala

BuildRequires:	pkgconfig(atk)
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(gdk-pixbuf-2.0)
BuildRequires:	pkgconfig(gnome-doc-utils)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(json-glib-1.0)
%ifnarch mips64el
BuildRequires:	pkgconfig(valgrind)
%endif
BuildRequires:	pkgconfig(x11)

%description
A small little library that was created by pulling out some comon code out of
indicator-applet. It passes a menu structure across DBus so that a program can
create a menu simply without worrying about how it is displayed on the other
side of the bus.


%package tools
Summary:	Development tools for the dbusmenu libraries
Group:		Development/Tools/Other

Requires:	%{name}-glib%{_soname_glib} = %{version}-%{release}

%description tools
This packages contains the development tools for the dbusmenu libraries.


%package glib%{_soname_glib}
Summary:	Small library that passes a menu structure across DBus
Group:		System/Libraries

%description glib%{_soname_glib}
This package contains the shared libraries for the dbusmenu-glib library.


%package -n typelib-1_0-Dbusmenu-0_4
Summary:	Small library that passes a menu structure across DBus - Introspection bindings
Group:		System/Libraries

%description -n typelib-1_0-Dbusmenu-0_4
This package contains the GObject Introspection bindings for the dbusmenu
library.


%package glib-devel
Summary:	Development files for libdbusmenu-glib
Group:		Development/Libraries/C and C++

Requires:	%{name}-glib%{_soname_glib} = %{version}-%{release}
Requires:	pkgconfig(dbus-glib-1)

%description glib-devel
This package contains the development files for the dbusmenu-glib library.


%package glib-doc
Summary:	Documentation for libdbusmenu-glib%{_soname_glib}
Group:		Documentation/HTML

BuildArch:	noarch

%description glib-doc
This package includes the documentation for the dbusmenu-glib library.


%package gtk%{_soname_gtk2}
Summary:	Small library that passes a menu structure across DBus - GTK2 version
Group:		System/Libraries

%description gtk%{_soname_gtk2}
This package contains the shared libraries for the dbusmenu-gtk2 library.


%package -n typelib-1_0-DbusmenuGtk-0_4
Summary:	Small library that passes a menu structure across DBus - Introspection bindings
Group:		System/Libraries

%description -n typelib-1_0-DbusmenuGtk-0_4
This package contains the GObject Introspection bindings for the GTK 2 version
of the dbusmenu-gtk library.


%package gtk-devel
Summary:	Development files for libdbusmenu-gtk%{_soname_gtk2}
Group:		Development/Libraries/C and C++

Requires:	%{name}-gtk%{_soname_gtk2} = %{version}-%{release}
Requires:	%{name}-glib-devel = %{version}-%{release}

Requires:	pkgconfig(dbus-glib-1)

%description gtk-devel
This package contains the development files for the dbusmenu-gtk2 library.


%package gtk3-%{_soname_gtk3}
Summary:	Small library that passes a menu structure across DBus - GTK3 version
Group:		System/Libraries


%description gtk3-%{_soname_gtk3}
This package contains the shared libraries for the dbusmenu-gtk3 library.


%package -n typelib-1_0-DbusmenuGtk3-0_4
Summary:	Small library that passes a menu structure across DBus - Introspection bindings
Group:		System/Libraries

%description -n typelib-1_0-DbusmenuGtk3-0_4
This package contains the GObject Introspection bindings for the GTK 3 version
of the dbusmenu-gtk library.


%package gtk3-devel
Summary:	Development files for libdbusmenu-gtk3-%{_soname_gtk3}
Group:		Development/Libraries/C and C++

Requires:	%{name}-gtk3-%{_soname_gtk3} = %{version}-%{release}
Requires:	%{name}-glib-devel = %{version}-%{release}

# GTK 3 with Ubuntu's patches is needed
Requires:	pkgconfig(dbus-glib-1)


%description gtk3-devel
This package contains the development files for the dbusmenu-gtk3 library.


%package gtk-doc
Summary:	Documentation for libdbusmenu-gtk%{_soname_gtk2} and libdbusmenu-gtk3-%{_soname_gtk3}
Group:		Documentation/HTML

BuildArch:	noarch

%description gtk-doc
This package contains the documentation for the dbusmenu-gtk2 and dbusmenu-gtk3
libraries.


%package jsonloader%{_soname_jsonloader}
Summary:	Small library that passes a menu structure across DBus - Test library
Group:		System/Libraries

%description jsonloader%{_soname_jsonloader}
This package contains the shared libraries for dbusmenu-jsonloader, a library
meant for test suites.


%package jsonloader-devel
Summary:	Development files for libdbusmenu-jsonloader%{_soname_jsonloader}
Group:		Development/Libraries/C and C++

Requires:	%{name}-jsonloader%{_soname_jsonloader} = %{version}-%{release}
Requires:	%{name}-glib-devel = %{version}-%{release}
Requires:	pkgconfig(dbus-glib-1)
Requires:	pkgconfig(json-glib-1.0)

%description jsonloader-devel
This package contains the development files for the dbusmenu-jsonloader library.


%prep
%setup -q

# Allow build with older gnome-doc-utils
sed -i 's/\(gdu_cv_version_required=\)0\.3\.2/\10.20.10/g' m4/gnome-doc-utils.m4

%patch0 -p1 -b .fix-sgml
%patch1 -p1

autoreconf -vfi

# Disable rpath (from Debian wiki)
sed -i -r 's/(hardcode_into_libs)=.*$/\1=no/' configure


%build
%global _configure ../configure
mkdir build-gtk2 build-gtk3

pushd build-gtk2
%configure --disable-scrollkeeper --enable-gtk-doc --enable-introspection \
           --with-gtk=2 --disable-static
make %{?_smp_mflags}
popd

pushd build-gtk3
%configure --disable-scrollkeeper --enable-gtk-doc --enable-introspection \
           --with-gtk=3 --disable-static
make %{?_smp_mflags}
popd


%install
pushd build-gtk2
%make_install
popd

pushd build-gtk3
%make_install
popd

# Remove libtool files
find $RPM_BUILD_ROOT -type f -name '*.la' -delete

# Put documentation in correct directory
install -dm755 $RPM_BUILD_ROOT%{_docdir}/%{name}-tools/
mv $RPM_BUILD_ROOT%{_datadir}/doc/%{name}/README.dbusmenu-bench \
               $RPM_BUILD_ROOT%{_docdir}/%{name}-tools/

# Put examples in correct documentation directory
install -dm755 $RPM_BUILD_ROOT%{_docdir}/%{name}-glib-devel/examples/
mv $RPM_BUILD_ROOT%{_datadir}/doc/%{name}/examples/glib-server-nomenu.c \
               $RPM_BUILD_ROOT%{_docdir}/%{name}-glib-devel/examples/

# Remove empty directories
#find $RPM_BUILD_ROOT -type d -empty -delete


%post glib%{_soname_glib} -p /sbin/ldconfig

%postun glib%{_soname_glib} -p /sbin/ldconfig


%post gtk%{_soname_gtk2} -p /sbin/ldconfig

%postun gtk%{_soname_gtk2} -p /sbin/ldconfig


%post gtk3-%{_soname_gtk3} -p /sbin/ldconfig

%postun gtk3-%{_soname_gtk3} -p /sbin/ldconfig


%post jsonloader%{_soname_jsonloader} -p /sbin/ldconfig

%postun jsonloader%{_soname_jsonloader} -p /sbin/ldconfig


%files tools
%defattr(-,root,root)
%doc AUTHORS README
%{_libexecdir}/dbusmenu-bench
%{_libexecdir}/dbusmenu-dumper
%{_libexecdir}/dbusmenu-testapp
%dir %{_datadir}/%{name}/
%dir %{_datadir}/%{name}/json/
%{_datadir}/%{name}/json/test-gtk-label.json
%doc %dir %{_docdir}/%{name}-tools/
%doc %{_docdir}/%{name}-tools/README.dbusmenu-bench


%files glib%{_soname_glib}
%defattr(-,root,root)
%doc AUTHORS README
%{_libdir}/libdbusmenu-glib.so.%{_soname_glib}*


%files -n typelib-1_0-Dbusmenu-0_4
%defattr(-,root,root)
%{_libdir}/girepository-1.0/Dbusmenu-0.4.typelib


%files glib-devel
%defattr(-,root,root)
%doc AUTHORS README
%dir %{_includedir}/libdbusmenu-glib-0.4/
%dir %{_includedir}/libdbusmenu-glib-0.4/libdbusmenu-glib/
%{_includedir}/libdbusmenu-glib-0.4/libdbusmenu-glib/client.h
%{_includedir}/libdbusmenu-glib-0.4/libdbusmenu-glib/dbusmenu-glib.h
%{_includedir}/libdbusmenu-glib-0.4/libdbusmenu-glib/enum-types.h
%{_includedir}/libdbusmenu-glib-0.4/libdbusmenu-glib/menuitem-proxy.h
%{_includedir}/libdbusmenu-glib-0.4/libdbusmenu-glib/menuitem.h
%{_includedir}/libdbusmenu-glib-0.4/libdbusmenu-glib/server.h
%{_includedir}/libdbusmenu-glib-0.4/libdbusmenu-glib/types.h
%{_libdir}/pkgconfig/dbusmenu-glib-0.4.pc
%{_libdir}/libdbusmenu-glib.so
%{_datadir}/gir-1.0/Dbusmenu-0.4.gir
%dir %{_datadir}/vala/vapi/
%{_datadir}/vala/vapi/Dbusmenu-0.4.vapi
%doc %dir %{_docdir}/%{name}-glib-devel/
%doc %dir %{_docdir}/%{name}-glib-devel/examples/
%doc %{_docdir}/%{name}-glib-devel/examples/glib-server-nomenu.c


%files glib-doc
%defattr(-,root,root)
%doc %{_datadir}/gtk-doc/html/libdbusmenu-glib/


%files gtk%{_soname_gtk2}
%defattr(-,root,root)
%doc AUTHORS README
%{_libdir}/libdbusmenu-gtk.so.%{_soname_gtk2}*


%files -n typelib-1_0-DbusmenuGtk-0_4
%defattr(-,root,root)
%{_libdir}/girepository-1.0/DbusmenuGtk-0.4.typelib


%files gtk-devel
%defattr(-,root,root)
%doc AUTHORS README
%dir %{_includedir}/libdbusmenu-gtk-0.4/
%dir %{_includedir}/libdbusmenu-gtk-0.4/libdbusmenu-gtk/
%{_includedir}/libdbusmenu-gtk-0.4/libdbusmenu-gtk/client.h
%{_includedir}/libdbusmenu-gtk-0.4/libdbusmenu-gtk/dbusmenu-gtk.h
%{_includedir}/libdbusmenu-gtk-0.4/libdbusmenu-gtk/menu.h
%{_includedir}/libdbusmenu-gtk-0.4/libdbusmenu-gtk/menuitem.h
%{_includedir}/libdbusmenu-gtk-0.4/libdbusmenu-gtk/parser.h
%{_libdir}/pkgconfig/dbusmenu-gtk-0.4.pc
%{_libdir}/libdbusmenu-gtk.so
%{_datadir}/gir-1.0/DbusmenuGtk-0.4.gir
%dir %{_datadir}/vala/vapi/
%{_datadir}/vala/vapi/DbusmenuGtk-0.4.vapi


%files gtk3-%{_soname_gtk3}
%defattr(-,root,root)
%doc AUTHORS README
%{_libdir}/libdbusmenu-gtk3.so.%{_soname_gtk3}*


%files -n typelib-1_0-DbusmenuGtk3-0_4
%defattr(-,root,root)
%{_libdir}/girepository-1.0/DbusmenuGtk3-0.4.typelib


%files gtk3-devel
%defattr(-,root,root)
%doc AUTHORS README
%dir %{_includedir}/libdbusmenu-gtk3-0.4/
%dir %{_includedir}/libdbusmenu-gtk3-0.4/libdbusmenu-gtk/
%{_includedir}/libdbusmenu-gtk3-0.4/libdbusmenu-gtk/client.h
%{_includedir}/libdbusmenu-gtk3-0.4/libdbusmenu-gtk/dbusmenu-gtk.h
%{_includedir}/libdbusmenu-gtk3-0.4/libdbusmenu-gtk/menu.h
%{_includedir}/libdbusmenu-gtk3-0.4/libdbusmenu-gtk/menuitem.h
%{_includedir}/libdbusmenu-gtk3-0.4/libdbusmenu-gtk/parser.h
%{_libdir}/pkgconfig/dbusmenu-gtk3-0.4.pc
%{_libdir}/libdbusmenu-gtk3.so
%{_datadir}/gir-1.0/DbusmenuGtk3-0.4.gir
%dir %{_datadir}/vala/vapi/
%{_datadir}/vala/vapi/DbusmenuGtk3-0.4.vapi


%files gtk-doc
%defattr(-,root,root)
%doc %{_datadir}/gtk-doc/html/libdbusmenu-gtk/


%files jsonloader%{_soname_jsonloader}
%defattr(-,root,root)
%doc AUTHORS README
%{_libdir}/libdbusmenu-jsonloader.so.%{_soname_jsonloader}*


%files jsonloader-devel
%defattr(-,root,root)
%doc AUTHORS README
%dir %{_includedir}/libdbusmenu-glib-0.4/
%dir %{_includedir}/libdbusmenu-glib-0.4/libdbusmenu-jsonloader/
%{_includedir}/libdbusmenu-glib-0.4/libdbusmenu-jsonloader/json-loader.h
%{_libdir}/pkgconfig/dbusmenu-jsonloader-0.4.pc
%{_libdir}/libdbusmenu-jsonloader.so


%changelog
* Sat Oct 06 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 12.10.2-1
- Version 12.10.2

* Thu Sep 20 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 12.10.1-1
- Version 12.10.1

* Fri Aug 17 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.6.2-1
- Initial release
- Based on GNOME:Ayatana's Fedora 17 spec file
- Version 0.6.2
