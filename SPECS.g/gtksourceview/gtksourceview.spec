%define gtk2_version 2.8.0
%define gnome_print_version 2.8.0

%define po_package gtksourceview-1.0

Summary: A library for viewing source files
Name: gtksourceview
Version: 1.8.5
Release: 10%{?dist} 
Epoch: 1
License: GPLv2+
Group: System Environment/Libraries
URL: http://gtksourceview.sourceforge.net/ 
Source0: http://ftp.gnome.org/pub/gnome/sources/gtksourceview/1.8/%{name}-%{version}.tar.bz2
Patch0: use-gnu.patch
Patch1: gtksourceview-1.8.5-glibh.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n) 
BuildRequires: gnome-vfs2-devel
BuildRequires: libxml2-devel
BuildRequires: gtk2-devel >= %{gtk2_version}
BuildRequires: libgnomeprint22-devel >= %{gnome_print_version}
BuildRequires: libgnomeprintui22-devel >= %{gnome_print_version}
BuildRequires: intltool >= 0.35
BuildRequires: gettext 

%description
GtkSourceView is a text widget that extends the standard gtk+ 2.x
text widget GtkTextView. It improves GtkTextView by implementing 
syntax highlighting and other features typical of a source code editor.

%package devel
Summary: Files to compile applications that use gtksourceview
Group: Development/Libraries
Requires: %{name} = %{epoch}:%{version}-%{release}
Requires: gtk2-devel >= %{gtk2_version} 
Requires: libgnomeprint22-devel >= %{gnome_print_version}
Requires: libxml2-devel
Requires: pkgconfig

%description devel
gtksourceview-devel contains the files required to compile 
applications which use GtkSourceView.

%prep
%setup -q
%patch0 -p1 -b .use-gnu
%patch1 -p1

%build

%configure --disable-gtk-doc --disable-static

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# remove unwanted files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%find_lang %{po_package}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{po_package}.lang
%defattr(-,root,root,-)
%doc README AUTHORS COPYING NEWS MAINTAINERS ChangeLog
%{_datadir}/gtksourceview-1.0
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/gtksourceview-1.0
%{_datadir}/gtk-doc/html/gtksourceview
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1:1.8.5-10
- 为 Magic 3.0 重建

* Tue Nov 27 2012 Liu Di <liudidi@gmail.com> - 1:1.8.5-9
- 为 Magic 3.0 重建

* Tue Dec 06 2011 Liu Di <liudidi@gmail.com> - 1:1.8.5-8
- 为 Magic 3.0 重建

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.8.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.8.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jul 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1:1.8.5-5
- fix license tag

* Thu Feb 14 2008 Matthias Clasen <mclasen@redhat.com> - 1:1.8.5-4
- Rebuild

* Thu Aug 23 2007 Adam Jackson <ajax@redhat.com> - 1:1.8.5-3
- Rebuild for ppc toolchain bug

* Tue Jul 10 2007 Matthias Clasen <mclasen@redhat.com> - 1:1.8.5-2
- Add an epoch and downgrade to 1.8.5; gtksourceview 2.x 
  will live in the gtksourceview2 package2

* Wed Jun 27 2007 Matthias Clasen <mclasen@redhat.com> - 1.90.1-2
- Avoid a conflict with compat-gtksourceview

* Mon Jun 18 2007 Matthias Clasen <mclasen@redhat.com> - 1.90.1-1
- Update to 1.90.1
- Update dependencies

* Tue Mar 13 2007 Matthias Clasen <mclasen@redhat.com> - 1.8.5-1
- Update to 1.8.5

* Tue Feb 13 2007 Matthias Clasen <mclasen@redhat.com> - 1.8.4-1
- Update to 1.8.4

* Mon Feb  5 2007 Matthias Clasen <mclasen@redhat.com> - 1.8.3-3
- Correct the license tag to say GPL
- Rework -devel description

* Sun Feb  4 2007 Matthias Clasen <mclasen@redhat.com> - 1.8.3-2
- Incorporate package review feedback

* Wed Jan 10 2007 Matthias Clasen <mclasen@redhat.com> - 1.8.3-1
- Update to 1.8.3

* Mon Dec 18 2006 Matthias Clasen <mclasen@redhat.com> - 1.8.2-1
- Update to 1.8.2

* Sat Oct 21 2006 Matthias Clasen <mclasen@redhat.com> - 1.8.1-1
- Update to 1.8.1

* Mon Sep  4 2006 Matthias Clasen <mclasen@redhat.com> - 1.8.0-1.fc6
- Update to 1.8.0

* Sat Aug 12 2006 Matthias Clasen <mclasen@redhat.com> - 1.7.2-1.fc6
- Update to 1.7.2

* Thu Aug  3 2006 Matthias Clasen <mclasen@redhat.com> - 1.7.1-1.fc6
- Update to 1.7.1

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.6.1-2.1
- rebuild

* Mon Apr 10 2006 Matthias Clasen <mclasen@redhat.com> - 1.6.1-2
- Update to 1.6.1

* Sun Mar 12 2006 Ray Strode <rstrode@redhat.com> - 1.6.0-1
- update to 1.6.0

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.5.7-2.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.5.7-2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Sat Feb  4 2006 Matthias Clasen <mclasen@redhat.com>
- Update URL

* Mon Jan 30 2006 Matthias Clasen <mclasen@redhat.com>
- Update to 1.5.7

* Mon Jan 16 2006 Matthias Clasen <mclasen@redhat.com>
- Update to 1.5.6

* Tue Jan 05 2006 Matthias Clasen <mclasen@redhat.com>
- Update to 1.5.4

* Tue Jan 03 2006 Matthias Clasen <mclasen@redhat.com>
- Update to 1.5.3

* Wed Dec 14 2005 Matthias Clsaen <mclasen@redhat.com>
- Update to 1.5.2
- Remove upstreamed patch
 
* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Dec  6 2005 Dan Williams <dcbw@redhat.com> - 1.5.1-2
- Fix off-by-one when searching for language specification files
    which breaks syntax hilighting.  Already fixed upstream.

* Thu Dec  1 2005 Matthias Clasen <mclasen@redhat.com> - 1.5.1-1
- Update to 1.5.1

* Thu Oct  6 2005 Matthias Clasen <mclasen@redhat.com> - 1.4.2-1
- Update to 1.4.2

* Thu Sep  8 2005 Matthias Clasen <mclasen@redhat.com> - 1.4.1-1
- Update to 1.4.1

* Tue Aug 16 2005 Warren Togami <wtogami@redhat.com> - 1.3.91-2
- rebuild for new cairo

* Tue Aug 08 2005 Ray Strode <rstrode@redhat.com> - 1.3.91-1
- Update to upstream version 1.3.91

* Wed Aug 03 2005 Ray Strode <rstrode@redhat.com> - 1.2.1-1
- Update to upstream version 1.2.1

* Thu Mar 17 2005 Ray Strode <rstrode@redhat.com> - 1.2.0-1
- Update to upstream version 1.2.0

* Wed Feb  9 2005 Matthias Clasen <mclasen@redhat.com> - 1.1.92-1
- Update to 1.1.92

* Sun Jan 30 2005 Matthias Clasen <mclasen@redhat.com> - 1.1.91-1
- Update to 1.1.91

* Mon Sep 20 2004 Matthias Clasen <mclasen@redhat.com> - 1.1.0-3
- Fix problem with backspace to delete partial characters

* Mon Aug 16 2004 Owen Taylor <otaylor@redhat.com> - 1.1.0-2
- Fix problem with extra blank lines when printing

* Tue Aug  3 2004 Owen Taylor <otaylor@redhat.com> - 1.1.0-1
- Update to 1.1.0
- Remove re-auto-ification which should no longer be necessary

* Sat Jul 31 2004 Dan Williams <dcbw@redhat.com>
- Update to 1.0.1

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sat Apr 10 2004 Warren Togami <wtogami@redhat.com> 1.0.0-2
- BR gnome-vfs2-devel libxml2-devel intltool gtk-doc gtk2-devel libgnomeprint22-devel 
  libgnomeprintui22-devel gettext

* Fri Apr  2 2004 Alex Larsson <alexl@redhat.com> 1.0.0-1
- update to 1.0.0

* Wed Mar 24 2004 Jens Petersen <petersen@redhat.com> - 0.9.2-2
- make -devel require libxml2-devel and libgnomeprint22-devel

* Wed Mar 10 2004 Alex Larsson <alexl@redhat.com> 0.9.2-1
- update to 0.9.2

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Feb 26 2004 Alexander Larsson <alexl@redhat.com> 0.9.1-1
- update to 0.9.1

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 28 2004 Alexander Larsson <alexl@redhat.com> 0.8.0-1
- update to 0.8.0

* Tue Aug 26 2003 Jonathan Blandford <jrb@redhat.com>
- new version

* Mon Aug 25 2003 Jonathan Blandford <jrb@redhat.com>
- try removing the libtool line

* Fri Aug 22 2003 Jonathan Blandford <jrb@redhat.com>
- Libtool fix

* Fri Aug 15 2003 Jonathan Blandford <jrb@redhat.com> 
- Initial build.


