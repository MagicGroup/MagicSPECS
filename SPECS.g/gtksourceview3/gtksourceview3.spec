%define gtk_version 3.0.0

%define po_package gtksourceview-3.0

Summary: A library for viewing source files
Summary(zh_CN.UTF-8): 查看源代码的库
Name: gtksourceview3
Version:	3.19.1
Release: 3%{?dist}
License: LGPLv2+ and GPLv2+
# the library itself is LGPL, some .lang files are GPL
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL: http://gtksourceview.sourceforge.net/
#VCS: git:git://git.gnome.org/gtksourceview
%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
Source0: http://download.gnome.org/sources/gtksourceview/%{majorver}/gtksourceview-%{version}.tar.xz
BuildRequires: libxml2-devel
BuildRequires: gtk3-devel >= %{gtk_version}
BuildRequires: intltool >= 0.35
BuildRequires: gettext
BuildRequires: gobject-introspection-devel

%description
GtkSourceView is a text widget that extends the standard GTK+
GtkTextView widget. It improves GtkTextView by implementing
syntax highlighting and other features typical of a source code editor.

This package contains version 3 of GtkSourceView. The older version
2 is contains in the gtksourceview2 package.

%description -l zh_CN.UTF-8
GtkSourceView 是标准 GTK+ 控件 GtkTextView 的一个扩展控件，实现了
语法高亮等特性。

这是 GtkSourceView 的 3 版本，老版本的 2 是 gtksourceview2 包。

%package devel
Summary: Files to compile applications that use gtksourceview3
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}
Requires: gtk3-devel >= %{gtk_version}
Requires: libxml2-devel

%description devel
gtksourceview3-devel contains the files required to compile
applications which use GtkSourceView 3.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n gtksourceview-%{version}

%build
%configure --disable-gtk-doc --disable-static

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

# remove unwanted files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_datadir}/gtksourceview-3.0/language-specs/check.sh
rm -f $RPM_BUILD_ROOT%{_datadir}/gtksourceview-3.0/language-specs/convert.py
magic_rpm_clean.sh
%find_lang %{po_package}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{po_package}.lang
%defattr(-,root,root,-)
%doc README AUTHORS COPYING NEWS MAINTAINERS
%{_datadir}/gtksourceview-3.0
%{_libdir}/*.so.*
%{_libdir}/girepository-1.0/GtkSource-3.0.typelib

%files devel
%defattr(-,root,root,-)
%{_includedir}/gtksourceview-3.0
%{_datadir}/gtk-doc/html/*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so
%{_datadir}/gir-1.0/GtkSource-3.0.gir

%changelog
* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 3.19.1-3
- 更新到 3.19.1

* Mon Apr 14 2014 Liu Di <liudidi@gmail.com> - 3.12.0-2
- 为 Magic 3.0 重建

* Sun Apr 06 2014 Liu Di <liudidi@gmail.com> - 3.12.0-1
- 更新到 3.12.0

* Mon Apr 15 2013 Ignacio Casal Quinteiro <icq@gnome.org> - 3.8.1-1
- Update to 3.8.1

* Mon Mar 25 2013 Ignacio Casal Quinteiro <icq@gnome.org> - 3.8.0-1
- Update to 3.8.0

* Tue Mar 19 2013 Richard Hughes <rhughes@redhat.com> - 3.7.92-1
- Update to 3.7.92

* Thu Mar 07 2013 Ignacio Casal Quinteiro <icq@gnome.org> - 3.7.91-1
- Update to 3.7.91

* Tue Feb 19 2013 Richard Hughes <rhughes@redhat.com> - 3.7.90-1
- Update to 3.7.90

* Mon Feb 04 2013 Ignacio Casal Quinteiro <icq@gnome.org> - 3.7.3-1
- Update to 3.7.3

* Wed Jan 16 2013 Ignacio Casal Quinteiro <icq@gnome.org> - 3.7.2-1
- Update to 3.7.2

* Mon Jan 07 2013 Ignacio Casal Quinteiro <icq@gnome.org> - 3.7.1-1
- Update to 3.7.1

* Mon Nov 05 2012 Ray Strode <rstrode@redhat.com> 3.6.1-1
- Update to 3.6.1

* Mon Sep 24 2012 Ignacio Casal Quinteiro <icq@gnome.org> - 3.6.0-1
- Update to 3.6.0

* Wed Sep 19 2012 Richard Hughes <hughsient@gmail.com> - 3.5.4-1
- Update to 3.5.4

* Tue Aug 21 2012 Richard Hughes <hughsient@gmail.com> - 3.5.3-1
- Update to 3.5.3

* Tue Jul 31 2012 Richard Hughes <hughsient@gmail.com> - 3.5.2-1
- Update to 3.5.2

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu May 17 2012 Kalev Lember <kalevlember@gmail.com> - 3.4.2-1
- Update to 3.4.2

* Mon Apr 16 2012 Ignacio Casal Quinteiro <icq@gnome.org> - 3.4.1-1
- Update to 3.4.1

* Mon Mar 26 2012 Ignacio Casal Quinteiro <icq@gnome.org> - 3.4.0-1
- Update to 3.4.0

* Wed Mar 21 2012 Kalev Lember <kalevlember@gmail.com> - 3.3.5-1
- Update to 3.3.5

* Fri Feb 24 2012 Ignacio Casal Quinteiro <icq@gnome.org> - 3.3.4-1
- Update to 3.3.4

* Mon Feb  6 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.3-1
- Update to 3.3.3

* Sun Jan 08 2012 Ignacio Casal Quinteiro <icq@gnome.org> - 3.3.2-1
- Update to 3.3.2

* Sat Dec 17 2011 Ignacio Casal Quinteiro <icq@gnome.org> - 3.3.1-1
- Update to 3.3.1

* Tue Nov 01 2011 Ignacio Casal Quinteiro <icq@gnome.org> - 3.2.3-1
- Update to 3.2.3

* Sun Oct 16 2011 Ignacio Casal Quinteiro <icq@gnome.org> - 3.2.2-1
- Update to 3.2.2

* Sun Oct 09 2011 Ignacio Casal Quinteiro <icq@gnome.org> - 3.2.1-1
- Update to 3.2.1

* Mon Sep 26 2011 Ignacio Casal Quinteiro <icq@gnome.org> - 3.2.0-1
- Update to 3.2.0

* Tue Sep 20 2011 Ignacio Casal Quinteiro <icq@gnome.org> - 3.1.6-1
- Update to 3.1.6

* Tue Sep 06 2011 Ignacio Casal Quinteiro <icq@gnome.org> - 3.1.5-1
- Update to 3.1.5

* Mon Aug 08 2011 Ignacio Casal Quinteiro <icq@gnome.org> - 3.1.4-1
- Update to 3.1.4

* Mon Jul 04 2011 Ignacio Casal Quinteiro <icq@gnome.org> - 3.1.3-1
- Update to 3.1.3

* Thu Jun 16 2011 Tomas Bzatek <tbzatek@redhat.com> - 3.1.2-1
- Update to 3.1.2

* Tue Apr 26 2011 Matthias Clasen <mclasen@redhat.com> 3.0.1-1
- Update to 3.0.1

* Mon Apr  4 2011 Matthias Clasen <mclasen@redhat.com> 3.0.0-1
- Update to 3.0.0

* Tue Mar 22 2011 Matthias Clasen <mclasen@redhat.com> 2.91.9-1
- Update to 2.91.9

* Mon Mar  7 2011 Matthias Clasen <mclasen@redhat.com> 2.91.8-1
- Update to 2.91.8

* Tue Feb 22 2011 Matthias Clasen <mclasen@redhat.com> 2.91.6-1
- Update to 2.91.6

* Thu Feb 10 2011 Matthias Clasen <mclasen@redhat.com> 2.91.5-3
- Rebuild against newer gtk

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.91.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Matthias Clasen <mclasen@redhat.com> 2.91.5-1
- Update to 2.91.5

* Mon Jan 10 2011 Matthias Clasen <mclasen@redhat.com> 2.91.4-1
- Update to 2.91.4

* Sat Jan  8 2011 Matthias Clasen <mclasen@redhat.com> 2.91.3-1
- Update to 2.91.3

* Fri Dec  3 2010 Tomas Bzatek <tbzatek@redhat.com> 2.91.2-1
- Update to 2.91.2

* Tue Nov  2 2010 Matthias Clasen <mclasen@redhat.com> 2.91.1-1
- Update to 2.91.1

* Wed Oct  6 2010 Matthias Clasen <mclasen@redhat.com> 2.91.0-1
- Update to 2.91.0

* Wed Sep 29 2010 jkeating - 2.90.4-5.git7701e36
- Rebuilt for gcc bug 634757

* Tue Sep 21 2010 Matthias Clasen <mclasen@redhat.com> - 2.90.4-4.git7701e36
- git snapshot
- Rebuild with newer gobject-introspection

* Thu Jul 15 2010 Colin Walters <walters@verbum.org> - 2.90.4-2
- Rebuild with new gobject-introspection

* Tue Jul 13 2010 Matthias Clasen <mclasen@redhat.com> - 2.90.4-1
- Update to 2.90.4

* Tue Jun 29 2010 Matthias Clasen <mclasen@redhat.com> - 2.90.3-2
- Incorporate some review feedback

* Tue Jun 29 2010 Matthias Clasen <mclasen@redhat.com> - 2.90.3-1
- Initial packaging of GtkSourceview 3
