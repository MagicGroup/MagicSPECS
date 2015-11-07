%define glib2_version 2.13.6
%define gtk2_version 2.12.0

%define po_package gtksourceview-2.0

Summary: A library for viewing source files
Name: gtksourceview2
Version: 2.11.2
Release: 9%{?dist}
License: LGPLv2+ and GPLv2+
# the library itself is LGPL, some .lang files are GPL
Group: System Environment/Libraries
URL: http://gtksourceview.sourceforge.net/
#VCS: git:git://git.gnome.org/gtksourceview
Source0: http://download.gnome.org/sources/gtksourceview/2.11/gtksourceview-%{version}.tar.bz2
# https://bugzilla.redhat.com/show_bug.cgi?id=661068
Patch0: gtksourceview-2.11.2-cflags.patch
Patch1:	gtksourceview-2.11.2-forcegtk2.patch
BuildRequires: libxml2-devel
BuildRequires: GConf2-devel
BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: gtk2-devel >= %{gtk2_version}
BuildRequires: intltool >= 0.35
BuildRequires: gettext
BuildRequires: gobject-introspection-devel

%description
GtkSourceView is a text widget that extends the standard GTK+
GtkTextView widget. It improves GtkTextView by implementing
syntax highlighting and other features typical of a source code editor.

This package contains version 2 of GtkSourceView. The older version
1 is contains in the gtksourceview package.

%package devel
Summary: Files to compile applications that use gtksourceview2
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: gtk2-devel >= %{gtk2_version}
Requires: libxml2-devel

%description devel
gtksourceview2-devel contains the files required to compile
applications which use GtkSourceView 2.x.

%prep
%setup -q -n gtksourceview-%{version}
%patch0 -p1 -b .cflags
%patch1 -p1

%build
%configure --enable-deprecations --disable-gtk-doc --disable-static

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

# remove unwanted files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_datadir}/gtksourceview-2.0/language-specs/check.sh
rm -f $RPM_BUILD_ROOT%{_datadir}/gtksourceview-2.0/language-specs/convert.py

%find_lang %{po_package}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{po_package}.lang
%defattr(-,root,root,-)
%doc README AUTHORS COPYING NEWS MAINTAINERS
%{_datadir}/gtksourceview-2.0
%{_libdir}/*.so.*
%{_libdir}/girepository-1.0/GtkSource-2.0.typelib

%files devel
%defattr(-,root,root,-)
%{_includedir}/gtksourceview-2.0
%{_datadir}/gtk-doc/html/*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so
%{_datadir}/gir-1.0/GtkSource-2.0.gir

%changelog
* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 2.11.2-9
- 为 Magic 3.0 重建

* Mon Apr 14 2014 Liu Di <liudidi@gmail.com> - 2.11.2-8
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 2.11.2-7
- 为 Magic 3.0 重建

* Tue Dec 21 2010 Dan Horák <dan[at]danny.cz> - 2.11.2-6
- fix FTBFS #661068

* Wed Sep 29 2010 jkeating - 2.11.2-5
- Rebuilt for gcc bug 634757

* Tue Sep 21 2010 Matthias Clasen <mclasen@redhat.com> - 2.11.2-3
- Rebuild with newer gobject-introspection

* Thu Jul 15 2010 Colin Walters <walters@verbum.org> - 2.11.2-2
- Rebuild with new gobject-introspection
- Drop gir-repository-devel

* Tue Jun  8 2010 Matthias Clasen <mclasen@redhat.com> - 2.11.2-1
- Update to 2.11.2

* Wed Jun  2 2010 Matthias Clasen <mclasen@redhat.com> - 2.11.1-1
- Update to 2.11.1

* Thu May 27 2010 Matthias Clasen <mclasen@redhat.com> - 2.10.2-1
- Update to 2.10.2

* Tue Apr 27 2010 Matthias Clasen <mclasen@redhat.com> - 2.10.1-1
- Update to 2.10.1

* Sun Mar 28 2010 Matthias Clasen <mclasen@redhat.com> - 2.10.0-1
- Update to 2.10.0

* Sun Mar 28 2010 Matthias Clasen <mclasen@redhat.com> - 2.9.9-1
- Update to 2.9.9

* Tue Mar  2 2010 Matthias Clasen <mclasen@redhat.com> - 2.9.8-1
- Update to 2.9.8

* Mon Feb 22 2010 Matthias Clasen <mclasen@redhat.com> - 2.9.7-1
- Update to 2.9.7

* Tue Jan 26 2010 Matthias Clasen <mclasen@redhat.com> - 2.9.5-1
- Update to 2.9.5

* Sat Jan 16 2010 Matthias Clasen <mclasen@redhat.com> - 2.9.4-1
- Update to 2.9.4

* Tue Dec 01 2009 Bastien Nocera <bnocera@redhat.com> 2.9.3-1
- Update to 2.9.3

* Wed Sep 23 2009 Matthias Clasen <mclasen@redhat.com> - 2.8.0-1
- Update to 2.8.0

* Mon Sep 14 2009 Matthias Clasen <mclasen@redhat.com> - 2.7.5-1
- Update to 2.7.5

* Mon Aug 24 2009 Matthias Clasen <mclasen@redhat.com> - 2.7.4-1
- Update to 2.7.4

* Tue Jul 28 2009 Matthias Clasen <mclasen@redhat.com> - 2.7.3-1
- Update to 2.7.3

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jun 14 2009 Matthias Clasen <mclasen@redhat.com> - 2.7.1-2
- Minor directory ownership cleanup

* Sun May 31 2009 Matthias Clasen <mclasen@redhat.com> - 2.7.1-1
- Update to 2.7.1

* Sun Apr 12 2009 Matthias Clasen <mclasen@redhat.com> - 2.6.1-1
- Update to 2.6.1
- See http://download.gnome.org/sources/gtksourceview/2.6/gtksourceview-2.6.1.news

* Mon Mar 16 2009 Matthias Clasen <mclasen@redhat.com> - 2.6.0-1
- Update to 2.6.0

* Mon Mar  2 2009 Matthias Clasen <mclasen@redhat.com> - 2.5.6-1
- Update to 2.5.6

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 18 2009 Matthias Clasen <mclasen@redhat.com> - 2.5.5-1
- Update to 2.5.5

* Tue Feb  3 2009 Matthias Clasen <mclasen@redhat.com> - 2.5.4-1
- Update to 2.5.4

* Fri Jan 30 2009 Matthias Clasen <mclasen@redhat.com> - 2.5.3-2
- Recognize %else in spec files (#480587)

* Tue Jan 20 2009 Matthias Clasen <mclasen@redhat.com> - 2.5.3-1
- Update to 2.5.3

* Tue Jan  6 2009 Matthias Clasen <mclasen@redhat.com> - 2.5.2-1
- Update to 2.5.2

* Wed Nov 12 2008 Matthias Clasen <mclasen@redhat.com> - 2.4.1-1
- Update to 2.4.1

* Sun Sep 21 2008 Matthias Clasen <mclasen@redhat.com> - 2.4.0-1
- Update to 2.4.0

* Mon Sep  8 2008 Matthias Clasen <mclasen@redhat.com> - 2.3.3-1
- Update to 2.3.3

* Tue Sep  2 2008 Matthias Clasen <mclasen@redhat.com> - 2.3.2-1
- Update to 2.3.2

* Wed Aug 13 2008 Matthias Clasen <mclasen@redhat.com> - 2.3.1-1
- Update to 2.3.1

* Mon Apr  7 2008 Matthias Clasen <mclasen@redhat.com> - 2.2.1-1
- Update to 2.2.1

* Mon Mar 10 2008 Matthias Clasen <mclasen@redhat.com> - 2.2.0-1
- Update to 2.2.0

* Mon Feb 25 2008 Matthias Clasen <mclasen@redhat.com> - 2.1.3-1
- Update to 2.1.3

* Wed Feb  6 2008 Matthias Clasen <mclasen@redhat.com> - 2.1.2-1
- Update to 2.1.2

* Tue Jan 29 2008 Matthias Clasen <mclasen@redhat.com> - 2.1.1-1
- Update to 2.1.1

* Mon Jan 14 2008 Matthias Clasen <mclasen@redhat.com> - 2.1.0-1
- Update to 2.1.0

* Mon Nov 26 2007 Matthias Clasen <mclasen@redhat.com> - 2.0.2-1
- Update to 2.0.2

* Mon Nov 12 2007 Matthias Clasen <mclasen@redhat.com> - 2.0.1-1
- Update to 2.0.1

* Mon Sep 17 2007 Matthias Clasen <mclasen@redhat.com> - 2.0.0-1
- Update to 2.0.0

* Tue Sep 11 2007 Matthew Barnes <mbarnes@redhat.com> - 1.90.5-1
- Update to 1.90.5

* Tue Sep  4 2007 Matthias Clasen <mclasen@redhat.com> - 1.90.4-1
- Update to 1.90.4

* Tue Aug  7 2007 Matthias Clasen <mclasen@redhat.com> - 1.90.3-2
- Update license field

* Wed Aug  1 2007 Matthias Clasen <mclasen@redhat.com> - 1.90.3-1
- Update to 1.90.3

* Tue Jul 10 2007 Matthias Clasen <mclasen@redhat.com> - 1.90.2-1
- Update to 1.90.2

* Mon Jul  2 2007 Matthias Clasen <mclasen@redhat.com> - 1.90.1-4
- More package review feedback:
  + don't ship check.sh and convert.py scripts
  + use GRegex from glib

* Fri Jun 29 2007 Matthias Clasen <mclasen@redhat.com> - 1.90.1-3
- Package review feedback

* Wed Jun 27 2007 Matthias Clasen <mclasen@redhat.com> - 1.90.1-2
- New package for GtkSourceView 2.x, based on gtksourceview
