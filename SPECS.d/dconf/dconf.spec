%define glib2_version 2.27.2
%define vala_version 0.11.7

Name:           dconf
Version:        0.15.0
Release:        4%{?dist}
Summary:        A configuration system

Group:          System Environment/Base
License:        LGPLv2+ and GPLv2+ and GPLv3+
URL:            http://live.gnome.org/dconf
#VCS:           git:git://git.gnome.org/dconf
Source0:        http://download.gnome.org/sources/dconf/0.15/dconf-%{version}.tar.xz

BuildRequires:  glib2-devel >= %{glib2_version}
BuildRequires:  gtk3-devel
BuildRequires:  libxml2-devel
BuildRequires:  dbus-devel
BuildRequires:  vala-devel >= %{vala_version}
BuildRequires:  gtk-doc
BuildRequires:  intltool

Requires:       dbus

%description
dconf is a low-level configuration system. Its main purpose is to provide a
backend to the GSettings API in GLib.

%package devel
Summary: Header files and libraries for dconf development
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: glib2-devel >= %{glib2_version}

%description devel
dconf development package. Contains files needed for doing software
development using dconf.

%package editor
Summary: Configuration editor for dconf
Group:   Applications/System
Requires: %{name} = %{version}-%{release}

%description editor
dconf-editor allows you to browse and modify dconf databases.


%prep
%setup -q

%build
%configure --disable-static
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

%find_lang dconf

%post
/sbin/ldconfig
gio-querymodules-%{__isa_bits} %{_libdir}/gio/modules
touch --no-create %{_datadir}/icons/hicolor >&/dev/null || :

%postun
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
  gio-querymodules-%{__isa_bits} %{_libdir}/gio/modules
  glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
  touch --no-create %{_datadir}/icons/hicolor >&/dev/null || :
  gtk-update-icon-cache %{_datadir}/icons/hicolor >&/dev/null || :
fi

%posttrans
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
gtk-update-icon-cache %{_datadir}/icons/hicolor >&/dev/null || :

%files -f dconf.lang
%doc COPYING
%{_libdir}/gio/modules/libdconfsettings.so
%{_libexecdir}/dconf-service
%{_datadir}/dbus-1/services/ca.desrt.dconf.service
%{_bindir}/dconf
%{_libdir}/libdconf.so.*
%{_libdir}/libdconf-dbus-1.so.*
%{_datadir}/bash-completion/completions/dconf
%{_datadir}/glib-2.0/schemas/ca.desrt.dconf-editor.gschema.xml
%{_mandir}/man1/dconf-service.1.gz
%{_mandir}/man1/dconf.1.gz
%{_mandir}/man7/dconf.7.gz

%files devel
%{_includedir}/dconf
%{_libdir}/libdconf.so
%{_libdir}/pkgconfig/dconf.pc
%{_includedir}/dconf-dbus-1
%{_libdir}/libdconf-dbus-1.so
%{_libdir}/pkgconfig/dconf-dbus-1.pc
%{_datadir}/gtk-doc/html/dconf
%{_datadir}/vala

%files editor
%{_bindir}/dconf-editor
%{_datadir}/applications/dconf-editor.desktop
%dir %{_datadir}/dconf-editor
%{_datadir}/dconf-editor/dconf-editor.ui
%{_datadir}/dconf-editor/dconf-editor-menu.ui
%{_datadir}/icons/hicolor/*/apps/dconf-editor.png
%{_mandir}/man1/dconf-editor.1.gz

%changelog
* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 0.15.0-4
- 为 Magic 3.0 重建

* Fri Nov 09 2012 Kalev Lember <kalevlember@gmail.com> - 0.15.0-3
- Move some of the rpm scriptlets back to %%posttrans
  (glib-compile-schemas, icon cache)

* Thu Nov  8 2012 Marek Kasik <mkasik@redhat.com> - 0.15.0-2
- Move dconf-editor's man page to the dconf-editor sub-package

* Wed Nov  7 2012 Marek Kasik <mkasik@redhat.com> - 0.15.0-1
- Update to 0.15.0
- Remove upstreamed patch

* Wed Nov  7 2012 Marek Kasik <mkasik@redhat.com> - 0.14.0-4
- Move %%posttrans commands to %%post (rpmlint related)

* Wed Nov  7 2012 Marek Kasik <mkasik@redhat.com> - 0.14.0-3
- Update License field
- Update Source URL
- Add link of corresponding bug for the memory leak patch

* Wed Nov  7 2012 Marek Kasik <mkasik@redhat.com> - 0.14.0-2.1
- Merge spec-file fixes from f18 branch

* Sun Oct 21 2012 Matthias Clasen <mclasen@redhat.com> - 0.14.0-2
- Fix a memory leak
- Update to 0.14.0

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 17 2012 Richard Hughes <hughsient@gmail.com> - 0.13.4-1
- Update to 0.13.4

* Thu Jun 07 2012 Richard Hughes <hughsient@gmail.com> - 0.13.0-2
- Add missing file to file list.

* Thu Jun 07 2012 Richard Hughes <hughsient@gmail.com> - 0.13.0-1
- Update to 0.13.0

* Sat May 05 2012 Kalev Lember <kalevlember@gmail.com> - 0.12.1-1
- Update to 0.12.1

* Tue Mar 27 2012 Kalev Lember <kalevlember@gmail.com> - 0.12.0-1
- Update to 0.12.0

* Tue Mar 20 2012 Kalev Lember <kalevlember@gmail.com> - 0.11.7-1
- Update to 0.11.7

* Fri Mar  9 2012 Matthias Clasen <mclasen@redhat.com> - 0.11.6-1
- Update to 0.11.6

* Mon Feb  6 2012 Matthias Clasen <mclasen@redhat.com> - 0.11.5-1
- Update to 0.11.5

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 21 2011 Matthias Clasen <mclasen@redhat.com> - 0.11.2-1
- Update to 0.11.2

* Fri Nov  4 2011 Matthias Clasen <mclasen@redhat.com> - 0.11.0-2
- Fix a typo (#710700)

* Wed Nov  2 2011 Matthias Clasen <mclasen@redhat.com> - 0.11.0-1
- Update to 0.11.0

* Mon Sep 26 2011 Ray <rstrode@redhat.com> - 0.10.0-1
- Update to 0.10.0

* Mon Sep 19 2011 Matthias Clasen <mclasen@redhat.com> - 0.9.1-1
- Update to 0.9.1

* Tue Jul 26 2011 Matthias Clasen <mclasen@redhat.com> - 0.9.0-1
- Update to 0.9.0

* Wed May 11 2011 Tomas Bzatek <tbzatek@redhat.com> - 0.7.5-1
- Update to 0.7.5

* Fri May  6 2011 Matthias Clasen <mclasen@redhat.com> - 0.7.4-1
- Update to 0.7.4

* Wed Apr  6 2011 Matthias Clasen <mclasen@redhat.com> - 0.7.3-2
- Fix a crash in dconf-editor

* Tue Mar 22 2011 Tomas Bzatek <tbzatek@redhat.com> - 0.7.3-1
- Update to 0.7.3

* Thu Feb 10 2011 Matthias Clasen <mclasen@redhat.com> - 0.7.2-3
- Rebuild for newer gtk

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Feb  5 2011 Matthias Clasen <mclasen@redhat.com> - 0.7.2-1
- Update to 0.7.2

* Wed Feb  2 2011 Matthias Clasen <mclasen@redhat.com> - 0.7.1-1
- Update to 0.7.1

* Mon Jan 17 2011 Matthias Clasen <mclasen@redhat.com> - 0.7-1
- Update to 0.7

* Wed Sep 29 2010 jkeating - 0.5.1-2
- Rebuilt for gcc bug 634757

* Tue Sep 21 2010 Matthias Clasen <mclasen@redhat.com> - 0.5.1-1
- Update to 0.5.1

* Thu Aug  5 2010 Matthias Clasen <mclasen@redhat.com> - 0.5-2
- Fix up shared library symlinks (#621733)

* Tue Aug  3 2010 Matthias Clasen <mclasen@redhat.com> - 0.5-1
- Update to 0.5

* Mon Jul 12 2010 Matthias Clasen <mclasen@redhat.com> - 0.4.2-1
- Update to 0.4.2

* Wed Jun 30 2010 Colin Walters <walters@verbum.org> - 0.4.1-2
- Changes to support snapshot builds

* Sat Jun 26 2010 Matthias Clasen <mclasen@redhat.com> 0.4.1-1
- Update to 0.4.1
- Include dconf-editor (in a subpackage)

* Wed Jun 23 2010 Matthias Clasen <mclasen@redhat.com> 0.4-2
- Rebuild against glib 2.25.9

* Sat Jun 12 2010 Matthias Clasen <mclasen@redhat.com> 0.4-1
- Update to 0.4

* Tue Jun 08 2010 Richard Hughes <rhughes@redhat.com> 0.3.2-0.1.20100608
- Update to a git snapshot so that users do not get a segfault in every
  application using GSettings.

* Wed Jun 02 2010 Bastien Nocera <bnocera@redhat.com> 0.3.1-2
- Rebuild against latest glib2

* Tue May 24 2010 Matthias Clasen <mclasen@redhat.com> 0.3.1-1
- Update to 0.3.1
- Add a -devel subpackage

* Fri May 21 2010 Matthias Clasen <mclasen@redhat.com> 0.3-3
- Make batched writes (e.g. with delayed settings) work

* Thu May 20 2010 Matthias Clasen <mclasen@redhat.com> 0.3-2
- Make the registration of the backend work

* Wed May 19 2010 Matthias Clasen <mclasen@redhat.com> 0.3-1
- Initial packaging
