%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

# Last updated for version 2.17.0
%define glib2_version		2.8.0
%define pango_version		1.16.0
%define gtk2_version		2.9.0
%define libglade2_version	2.5.0
%define pycairo_version		1.0.2
%define pygobject2_version	2.21.3
%define python2_version		2.3.5

%define buildglade %(pkg-config libglade-2.0 && echo 1 || echo 0)

### Abstract ###

Name: pygtk2
Version: 2.24.0
Release: 5%{?dist}
License: LGPLv2+
Group: Development/Languages
Summary: Python bindings for GTK+
URL: http://www.pygtk.org/
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Source: http://ftp.gnome.org/pub/GNOME/sources/pygtk/2.24/pygtk-%{version}.tar.bz2

### Patches ###

# RH bug #208608
Patch0: pygtk-nodisplay-exception.patch


### Dependencies ###

# Leave these requirements alone!  RPM isn't smart enough
# to derive these from the build requirements below.
Requires: pycairo
Requires: pygobject2

### Build Dependencies ###

BuildRequires: automake
BuildRequires: docbook-style-xsl
BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: gtk2-devel >= %{gtk2_version}
BuildRequires: libglade2-devel >= %{libglade2_version}
BuildRequires: libtool
BuildRequires: libxslt
BuildRequires: numpy
BuildRequires: pango-devel >= %{pango_version}
BuildRequires: pycairo-devel >= %{pycairo_version}
BuildRequires: pygobject2-devel >= %{pygobject2_version}
BuildRequires: python2-devel >= %{python2_version}

%description
PyGTK is an extension module for Python that gives you access to the GTK+
widget set.  Just about anything you can write in C with GTK+ you can write
in Python with PyGTK (within reason), but with all the benefits of using a
high-level scripting language.

%package codegen
Summary: The code generation program for PyGTK
Group: Development/Languages

%description codegen
This package contains the C code generation program for PyGTK.

%package libglade
Summary: A wrapper for the libglade library for use with PyGTK
Group: Development/Languages
Requires: %{name} = %{version}-%{release}

%description libglade
This module contains a wrapper for the libglade library.  Libglade allows
a program to construct its user interface from an XML description, which
allows the programmer to keep the UI and program logic separate.

%package devel
Summary: Development files for building add-on libraries
Group: Development/Languages
Requires: %{name} = %{version}-%{release}
Requires: %{name}-codegen = %{version}-%{release}
Requires: %{name}-doc = %{version}-%{release}
Requires: pkgconfig
Requires: pycairo-devel
Requires: pygobject2-devel

%description devel
This package contains files required to build wrappers for GTK+ add-on
libraries so that they interoperate with pygtk.

%package doc
Summary: Documentation files for %{name}
Group: Development/Languages
BuildArch: noarch

%description doc
This package contains documentation files for %{name}.

%prep
%setup -q -n pygtk-%{version}
%patch0 -p1

%build
%configure --enable-thread --enable-numpy
export tagname=CC
make LIBTOOL=/usr/bin/libtool

%install
rm -rf $RPM_BUILD_ROOT
export tagname=CC
make LIBTOOL=/usr/bin/libtool DESTDIR=$RPM_BUILD_ROOT install
find $RPM_BUILD_ROOT -name '*.la' -or -name '*.a' | xargs rm -f

%clean
rm -fr $RPM_BUILD_ROOT

%files
%defattr(644, root, root, 755)
%doc AUTHORS NEWS README MAPPING COPYING
%doc examples
%dir %{python_sitearch}/gtk-2.0
%dir %{python_sitearch}/gtk-2.0/gtk
%{python_sitearch}/gtk-2.0/gtk/*.py*
%dir %{_libdir}/pygtk
%dir %{_libdir}/pygtk/2.0
%{_libdir}/pygtk/2.0/*

%defattr(755, root, root, 755)
%{_bindir}/pygtk-demo
%{python_sitearch}/gtk-2.0/atk.so
%{python_sitearch}/gtk-2.0/pango.so
%{python_sitearch}/gtk-2.0/gtk/_gtk.so
%{python_sitearch}/gtk-2.0/gtkunixprint.so
%{python_sitearch}/gtk-2.0/pangocairo.so

%if %{buildglade}
%files libglade
%defattr(755, root, root, 755)
%{python_sitearch}/gtk-2.0/gtk/glade.so
%endif

%files codegen
%defattr(755, root, root, 755)
%{_prefix}/bin/pygtk-codegen-2.0

%files devel
%defattr(644, root, root, 755)
%dir %{_prefix}/include/pygtk-2.0
%dir %{_prefix}/include/pygtk-2.0/pygtk
%{_prefix}/include/pygtk-2.0/pygtk/*.h
%{_libdir}/pkgconfig/pygtk-2.0.pc
%dir %{_prefix}/share/pygtk
%dir %{_prefix}/share/pygtk/2.0
%dir %{_prefix}/share/pygtk/2.0/defs
%{_prefix}/share/pygtk/2.0/defs/*.defs
%{_prefix}/share/pygtk/2.0/defs/pangocairo.override

%files doc
%defattr(644, root, root, 755)
%{_datadir}/gtk-doc/html/pygtk

%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 2.24.0-5
- 为 Magic 3.0 重建

* Fri Aug 14 2015 Liu Di <liudidi@gmail.com> - 2.24.0-4
- 为 Magic 3.0 重建

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 2.24.0-3
- 为 Magic 3.0 重建

* Mon Jan 23 2012 Liu Di <liudidi@gmail.com> - 2.24.0-2
- 为 Magic 3.0 重建

