%define         soname 5
%define         gtksoname 3

Name:		libindicate
Version:	12.10.1
Release:	2.1
License:	LGPL-2.1 and LGPL-3.0
Summary:	Library to raise flags on dbus
Url:		http://launchpad.net/libindicate
Group:		System/Libraries
Source:		https://launchpad.net/libindicate/12.10/%{version}/+download/libindicate-%{version}.tar.gz

# PATCH_FIX_UPSTREAM 0002_missing_documentation.patch -- Add's some missing documentation
Patch0:		0002_missing_documentation.patch
# PATCH-FIX-UPSTREAM 0003_libpyglib-linking.patch [lp#690555] -- Fixes Python static version (patch by nmarques@opensuse.org) - Accepted upstream, but is still distributed as a patch in Ubuntu's packaging
Patch1:		0003_libpyglib-linking.patch

BuildRequires:	fdupes
BuildRequires:	gnome-doc-utils
BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	vala

BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(dbusmenu-glib-0.4)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(gtk+-3.0)
%ifnarch mips64el
BuildRequires:	pkgconfig(gtk-sharp-2.0)
BuildRequires:	pkgconfig(mono)
%endif
BuildRequires:	pkgconfig(pygobject-2.0)
BuildRequires:	pkgconfig(pygtk-2.0)
BuildRequires:	pkgconfig(python2)

%description
A small library for applications to raise "flags" on DBus for other components
of the desktop to pick up and visualize. Currently used by the messaging
indicator.


%package -n python-indicate
Summary:	Python 2 bindings for libindicate
Group:		Development/Libraries/Python

Requires:	%{name}%{soname} = %{version}-%{release}

%description -n python-indicate
This package provides the Python 2 bindings for libindicate.


%package -n %{name}%{soname}
Summary:	Library to raise flags on DBus
Group:		System/Libraries

%description -n %{name}%{soname}
A small library for applications to raise "flags" on DBus for other components
of the desktop to pick up and visualize. Currently used by the messaging
indicator.


%package -n typelib-1_0-Indicate-0_7
Summary:	Library to raise flags on DBus - Introspection bindings
Group:		System/Libraries

%description -n typelib-1_0-Indicate-0_7
This package contains the GObject Introspection bindings for the indicate
library.


%package devel
Summary:	Development files for libindicate
Group:		Development/Libraries/C and C++

Requires:	%{name}%{soname} = %{version}-%{release}
Requires:	pkgconfig(dbus-glib-1)
Requires:	pkgconfig(dbusmenu-glib-0.4)

%description devel
This package contains the development files for the indicate library.


%package gtk3-%{gtksoname}
Summary:	Library to raise flags on DBus - GTK 3 version
Group:		System/Libraries

%description gtk3-%{gtksoname}
A small library for applications to raise "flags" on DBus for other components
of the desktop to pick up and visualize. Currently used by the messaging
indicator.

This package contains the GTK3 bindings for this library.


%package -n typelib-1_0-IndicateGtk3-0_7
Summary:	Library to raise flags on DBus - Introspection bindings
Group:		System/Libraries

%description -n typelib-1_0-IndicateGtk3-0_7
This package contains the GObject Introspection bindings for the indicate-gtk3
library.


%package gtk3-devel
Summary:	Development files for libindicate-gtk3
Group:		Development/Libraries/C and C++

Requires:	%{name}-gtk3-%{gtksoname} = %{version}-%{release}
Requires:	%{name}-devel = %{version}-%{release}
Requires:	pkgconfig(dbus-glib-1)
Requires:	pkgconfig(gtk+-3.0)

%description gtk3-devel
This package contains the development files for the indicate-gtk3 library.


%package gtk%{gtksoname}
Summary:	Library to raise flags on DBus - GTK 2 version
Group:		System/Libraries

%description gtk%{gtksoname}
A small library for applications to raise "flags" on DBus for other components
of the desktop to pick up and visualize. Currently used by the messaging
indicator.

This package contains the GTK2 bindings for this library.


%package -n typelib-1_0-IndicateGtk-0_7
Summary:	Library to raise flags on DBus - Introspection bindings
Group:		System/Libraries

%description -n typelib-1_0-IndicateGtk-0_7
This package contains the GObject Introspection bindings for the indicate-gtk
library.


%package gtk-devel
Summary:	Development files for libindicate-gtk
Group:		Development/Libraries/C and C++

Requires:	%{name}-gtk%{gtksoname} = %{version}-%{release}
Requires:	%{name}-devel = %{version}-%{release}
Requires:	%{name}-gtk3-devel = %{version}-%{release}
Requires:	pkgconfig(dbus-glib-1)
Requires:	pkgconfig(gtk+-2.0)

%description gtk-devel
This packages contains the development files for the indicate-gtk library.


%package doc
Summary:	Documentation for libindicate
Group:		Documentation/HTML

BuildArch:	noarch

%description doc
This package contains the documentation for the indicate library.


%ifnarch mips64el
%package -n indicate-sharp
Summary:	Library to raise flags on DBus - C# bindings
Group:		System/Libraries

%description -n indicate-sharp
A small library for applications to raise "flags" on DBus for other components
of the desktop to pick up and visualize. Currently used by the messaging
indicator.

This package contains the Mono C# bindings for this library.


%package -n indicate-sharp-devel
Summary:	Development files for libindicate-sharp
Group:		Development/Libraries/Other

Requires:	indicate-sharp = %{version}-%{release}

%description -n indicate-sharp-devel
This package contains the development files for the indicator-sharp library.


%package -n indicate-gtk-sharp
Summary:	Library to raise flags on DBus - GTK# bindings
Group:		System/Libraries

Requires:	indicate-sharp = %{version}-%{release}

%description -n indicate-gtk-sharp
A small library for applications to raise "flags" on DBus for other components
of the desktop to pick up and visualize. Currently used by the messaging
indicator.

This package contains the GTK# bindings for this library.


%package -n indicate-gtk-sharp-devel
Summary:	Development files for libindicate-gtk-sharp
Group:		Development/Libraries/Other

Requires:	indicate-gtk-sharp = %{version}-%{release}

%description -n indicate-gtk-sharp-devel
This packages contains the development files for the indicate-gtk-sharp
library.
%endif


%prep
%setup -q
%patch0 -p1 -b .documentation
%patch1 -p1 -b .libpygliblink

# Build fix (thanks to Damian!)
sed -i '/#include "glib\/gmessages.h"/d' libindicate/indicator.c

autoreconf -vfi


%build
%global _configure ../configure
mkdir build-gtk2 build-gtk3

pushd build-gtk2
%configure --with-gtk=2 --disable-scrollkeeper --disable-gtk-doc \
           --enable-introspection=yes --disable-static
make -j1
popd

pushd build-gtk3
%configure --with-gtk=3 --disable-scrollkeeper --disable-gtk-doc \
           --enable-introspection=yes --disable-static
make -j1
popd


%install
pushd build-gtk2
%make_install
popd

pushd build-gtk3
%make_install
popd

# Remove libtool archives
find $RPM_BUILD_ROOT -name '*.la' -type f -delete -print

# Put documentation in correct directory
install -dm755 $RPM_BUILD_ROOT%{_docdir}/%{name}-doc/examples/
mv $RPM_BUILD_ROOT%{_datadir}/doc/libindicate/examples/* \
               $RPM_BUILD_ROOT%{_docdir}/%{name}-doc/examples/

fdupes -s $RPM_BUILD_ROOT
magic_rpm_clean.sh

%post -n %{name}%{soname} -p /sbin/ldconfig

%postun -n %{name}%{soname} -p /sbin/ldconfig


%post gtk3-%{gtksoname} -p /sbin/ldconfig

%postun gtk3-%{gtksoname} -p /sbin/ldconfig


%post gtk%{gtksoname} -p /sbin/ldconfig

%postun gtk%{gtksoname} -p /sbin/ldconfig


%files -n python-indicate
%defattr(-,root,root)
%dir %{python_sitearch}/indicate/
%{python_sitearch}/indicate/__init__.py*
%{python_sitearch}/indicate/_indicate.so
%dir %{_datadir}/pygtk/
%dir %{_datadir}/pygtk/2.0/
%dir %{_datadir}/pygtk/2.0/defs/
%{_datadir}/pygtk/2.0/defs/indicate.defs


%files -n %{name}%{soname}
%defattr(-,root,root)
%doc AUTHORS
%{_libdir}/libindicate.so.%{soname}*


%files -n typelib-1_0-Indicate-0_7
%defattr(-,root,root)
%{_libdir}/girepository-1.0/Indicate-0.7.typelib


%files devel
%defattr(-,root,root)
%dir %{_includedir}/libindicate-0.7/
%dir %{_includedir}/libindicate-0.7/libindicate/
%{_includedir}/libindicate-0.7/libindicate/*.h
%{_libdir}/pkgconfig/indicate-0.7.pc
%{_libdir}/libindicate.so
%{_datadir}/gir-1.0/Indicate-0.7.gir
%{_datadir}/vala/vapi/Indicate-0.7.vapi


%files gtk3-%{gtksoname}
%defattr(-,root,root)
%{_libdir}/libindicate-gtk3.so.%{gtksoname}*


%files -n typelib-1_0-IndicateGtk3-0_7
%defattr(-,root,root)
%{_libdir}/girepository-1.0/IndicateGtk3-0.7.typelib


%files gtk3-devel
%defattr(-,root,root)
%dir %{_includedir}/libindicate-gtk3-0.7/
%dir %{_includedir}/libindicate-gtk3-0.7/libindicate-gtk/
%{_includedir}/libindicate-gtk3-0.7/libindicate-gtk/*.h
%{_libdir}/pkgconfig/indicate-gtk3-0.7.pc
%{_libdir}/libindicate-gtk3.so
%{_datadir}/gir-1.0/IndicateGtk3-0.7.gir
%{_datadir}/vala/vapi/IndicateGtk3-0.7.vapi


%files gtk%{gtksoname}
%defattr(-,root,root)
%{_libdir}/libindicate-gtk.so.%{gtksoname}*


%files -n typelib-1_0-IndicateGtk-0_7
%defattr(-,root,root)
%{_libdir}/girepository-1.0/IndicateGtk-0.7.typelib


%files gtk-devel
%defattr(-,root,root)
%dir %{_includedir}/libindicate-gtk-0.7/
%dir %{_includedir}/libindicate-gtk-0.7/libindicate-gtk/
%{_includedir}/libindicate-gtk-0.7/libindicate-gtk/*.h
%{_libdir}/pkgconfig/indicate-gtk-0.7.pc
%{_libdir}/libindicate-gtk.so
%{_datadir}/gir-1.0/IndicateGtk-0.7.gir
%{_datadir}/vala/vapi/IndicateGtk-0.7.vapi


%files doc
%defattr(-,root,root)
%doc %{_datadir}/gtk-doc/html/libindicate/
%dir %{_docdir}/%{name}-doc/
%dir %{_docdir}/%{name}-doc/examples/
%{_docdir}/%{name}-doc/examples/im-client.c
%{_docdir}/%{name}-doc/examples/im-client.py*
%{_docdir}/%{name}-doc/examples/indicate-alot.c
%{_docdir}/%{name}-doc/examples/indicate-and-crash.c
%{_docdir}/%{name}-doc/examples/listen-and-print.c
%{_docdir}/%{name}-doc/examples/listen-and-print.py*


%ifnarch mips64el
%files -n indicate-sharp
%defattr(-,root,root)
%dir %{_libdir}/indicate-sharp-0.1/
%{_libdir}/indicate-sharp-0.1/indicate-sharp.dll
%{_libdir}/indicate-sharp-0.1/indicate-sharp.dll.config
%dir %{_prefix}/lib/mono/gac/indicate-sharp/
%dir %{_prefix}/lib/mono/gac/indicate-sharp/*/
%{_prefix}/lib/mono/gac/indicate-sharp/*/*.dll*
%dir %{_prefix}/lib/mono/indicate/
%{_prefix}/lib/mono/indicate/indicate-sharp.dll


%files -n indicate-sharp-devel
%defattr(-,root,root)
%{_libdir}/pkgconfig/indicate-sharp-0.1.pc


%files -n indicate-gtk-sharp
%defattr(-,root,root)
%dir %{_libdir}/indicate-gtk-sharp-0.1/
%{_libdir}/indicate-gtk-sharp-0.1/indicate-gtk-sharp.dll
%{_libdir}/indicate-gtk-sharp-0.1/indicate-gtk-sharp.dll.config
%dir %{_prefix}/lib/mono/gac/indicate-gtk-sharp/
%dir %{_prefix}/lib/mono/gac/indicate-gtk-sharp/*/
%{_prefix}/lib/mono/gac/indicate-gtk-sharp/*/*.dll*
%dir %{_prefix}/lib/mono/indicate-gtk/
%{_prefix}/lib/mono/indicate-gtk/indicate-gtk-sharp.dll


%files -n indicate-gtk-sharp-devel
%defattr(-,root,root)
%{_libdir}/pkgconfig/indicate-gtk-sharp-0.1.pc
%endif


%changelog
* Fri Jul 18 2014 Liu Di <liudidi@gmail.com> - 12.10.1-2.1
- 为 Magic 3.0 重建

* Mon Aug 27 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 12.10.1-1
- Version 12.10.1

* Sat Aug 18 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 12.10.0-1
- Update to 12.10.0
- Add missing subpackages
- Fix incorrect summaries and descriptions
- Fix incorrect files lists (ie. gtk3 subpackage only contains mono files)
