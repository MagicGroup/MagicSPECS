%define gtk3_version 3.3.8
%define glib2_version 2.31.0
%define gnome_desktop_version 2.91.2
%define gnome_icon_theme_version 2.19.1
%define desktop_file_utils_version 0.9
%define libexif_version 0.6.14

Summary: Eye of GNOME image viewer
Name:    eog
Version: 3.8.0
Release: 1%{?dist}
URL: http://projects.gnome.org/eog/
#VCS: git:git://git.gnome.org/eog
Source: http://download.gnome.org/sources/eog/3.8/%{name}-%{version}.tar.xz

# The GFDL has an "or later version" clause embedded inside the license.
# There is no need to add the + here.
License: GPLv2+ and GFDL
Group: User Interface/Desktops
BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: gtk3-devel >= %{gtk3_version}
BuildRequires: libexif-devel >= %{libexif_version}
BuildRequires: exempi-devel
BuildRequires: lcms2-devel
BuildRequires: intltool >= 0.50.0-1
BuildRequires: libjpeg-devel
BuildRequires: gettext
BuildRequires: desktop-file-utils >= %{desktop_file_utils_version}
BuildRequires: gnome-desktop3-devel >= %{gnome_desktop_version}
BuildRequires: gnome-icon-theme >= %{gnome_icon_theme_version}
BuildRequires: libXt-devel
BuildRequires: libxml2-devel
BuildRequires: librsvg2-devel
BuildRequires: libpeas-devel >= 0.7.4
BuildRequires: gdk-pixbuf2-devel
BuildRequires: shared-mime-info
BuildRequires: gsettings-desktop-schemas-devel
BuildRequires: dbus-glib-devel
BuildRequires: gobject-introspection-devel
BuildRequires: zlib-devel
BuildRequires: itstool
Requires:      gsettings-desktop-schemas

Requires(post):   desktop-file-utils >= %{desktop_file_utils_version}
Requires(postun): desktop-file-utils >= %{desktop_file_utils_version}

%description
The Eye of GNOME image viewer (eog) is the official image viewer for the
GNOME desktop. It can view single image files in a variety of formats, as
well as large image collections.

eog is extensible through a plugin system.

%package devel
Summary: Support for developing plugins for the eog image viewer
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: gtk3-devel

%description devel
The Eye of GNOME image viewer (eog) is the official image viewer for the
GNOME desktop. This package allows you to develop plugins that add new
functionality to eog.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name} --with-gnome

rm -rf $RPM_BUILD_ROOT%{_libdir}/eog/plugins/*.la

desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/eog.desktop


%post
update-desktop-database >&/dev/null || :
touch %{_datadir}/icons/hicolor >&/dev/null || :

%postun
update-desktop-database >&/dev/null || :
if [ $1 -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor >&/dev/null || :
  gtk-update-icon-cache %{_datadir}/icons/hicolor >&/dev/null || :
  glib-compile-schemas %{_datadir}/glib-2.0/schemas >&/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor >&/dev/null || :
glib-compile-schemas %{_datadir}/glib-2.0/schemas >&/dev/null || :

%files -f %{name}.lang
%doc AUTHORS COPYING NEWS README
%{_datadir}/eog
%{_datadir}/applications/eog.desktop
%{_datadir}/icons/hicolor/*/apps/*
%{_bindir}/*
%{_libdir}/eog
%{_datadir}/GConf/gsettings/eog.convert
%{_datadir}/glib-2.0/schemas/org.gnome.eog.enums.xml
%{_datadir}/glib-2.0/schemas/org.gnome.eog.gschema.xml

%files devel
%{_includedir}/eog-3.0
%{_libdir}/pkgconfig/eog.pc
%{_datadir}/gtk-doc/

%changelog
* Tue Mar 26 2013 Kalev Lember <kalevlember@gmail.com> - 3.8.0-1
- Update to 3.8.0

* Wed Mar 20 2013 Richard Hughes <rhughes@redhat.com> - 3.7.92-1
- Update to 3.7.92

* Fri Mar  8 2013 Matthias Clasen <mclasen@redhat.com> - 3.7.91-1
- Update to 3.7.91

* Thu Feb 21 2013 Kalev Lember <kalevlember@gmail.com> - 3.7.4-5
- Drop the desktop file vendor prefix

* Wed Feb 20 2013 Kalev Lember <kalevlember@gmail.com> - 3.7.4-4
- Rebuilt for libgnome-desktop soname bump

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 3.7.4-2
- rebuild due to "jpeg8-ABI" feature drop

* Wed Jan 16 2013 Richard Hughes <hughsient@gmail.com> - 3.7.4-1
- Update to 3.7.4

* Fri Dec 21 2012 Kalev Lember <kalevlember@gmail.com> - 3.7.2-2
- Rebuilt for libgnome-desktop-3 3.7.3 soname bump

* Wed Nov 21 2012 Richard Hughes <hughsient@gmail.com> - 3.7.2-1
- Update to 3.7.2

* Fri Nov 09 2012 Kalev Lember <kalevlember@gmail.com> - 3.7.1-1
- Update to 3.7.1

* Tue Oct 16 2012 Kalev Lember <kalevlember@gmail.com> - 3.6.1-1
- Update to 3.6.1

* Tue Sep 25 2012 Kalev Lember <kalevlember@gmail.com> - 3.6.0-1
- Update to 3.6.0
- Drop upstreamed eog-link-with-libm.patch

* Wed Sep 19 2012 Matthias Clasen <mclasen@redhat.com> - 3.5.92-1
- Update to 3.5.92

* Tue Sep 04 2012 Richard Hughes <hughsient@gmail.com> - 3.5.91-1
- Update to 3.5.91

* Tue Aug 21 2012 Richard Hughes <hughsient@gmail.com> - 3.5.90-1
- Update to 3.5.90

* Tue Aug 07 2012 Richard Hughes <hughsient@gmail.com> - 3.5.4-1
- Update to 3.5.4

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 18 2012 Kalev Lember <kalevlember@gmail.com> - 3.5.3-1
- Update to 3.5.3

* Tue Jun 26 2012 Richard Hughes <hughsient@gmail.com> - 3.5.2-1
- Update to 3.5.2

* Fri Jun  8 2012 Matthias Clasen <mclasen@redhat.com> - 3.5.1-2
- Rebuild against new gnome-desktop

* Sat May 05 2012 Kalev Lember <kalevlember@gmail.com> - 3.5.1-1
- Update to 3.5.1

* Fri Apr 27 2012 Kalev Lember <kalevlember@gmail.com> - 3.4.1-3
- Removed last traces of gconf handling (#704230)

* Tue Apr 24 2012 Kalev Lember <kalevlember@gmail.com> - 3.4.1-2
- Silence rpm scriptlet output

* Tue Apr 17 2012 Kalev Lember <kalevlember@gmail.com> - 3.4.1-1
- Update to 3.4.1

* Tue Mar 27 2012 Richard Hughes <hughsient@gmail.com> - 3.4.0-1
- Update to 3.4.0

* Wed Mar 21 2012 Kalev Lember <kalevlember@gmail.com> - 3.3.92-1
- Update to 3.3.92

* Tue Mar  6 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.91-1
- Update to 3.3.91

* Sun Feb 26 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.90-1
- Update to 3.3.90

* Tue Feb  6 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.5-1
- Update to 3.3.5

* Tue Jan 17 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.4-1
- Update to 3.3.4

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 20 2011 Alon Levy <alevy@redhat.com> - 3.3.3-1
- Update to 3.3.3
- requires newer intltool for --no-translations

* Tue Nov 22 2011 Tomas Bzatek <tbzatek@redhat.com> - 3.3.2-1
- Update to 3.3.2

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-2
- Rebuilt for glibc bug#747377

* Tue Oct 18 2011 Matthias Clasen <mclasen@redhat.com> - 3.2.1-1
- Update to 3.2.1

* Tue Sep 27 2011 Ray <rstrode@redhat.com> - 3.2.0-1
- Update to 3.2.0

* Tue Sep 20 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.92-1
- Update to 3.1.92

* Wed Sep 07 2011 Kalev Lember <kalevlember@gmail.com> - 3.1.91-1
- Update to 3.1.91

* Wed Aug 31 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.90-1
- Update to 3.1.90

* Thu Aug 18 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.5-1
- Update to 3.1.5

* Mon Jul 25 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.4-1
- Update to 3.1.4

* Fri Jun 17 2011 Tomas Bzatek <tbzatek@redhat.com> - 3.1.2-2
- Rebuilt in order to fix pre scriptlet

* Thu Jun 16 2011 Tomas Bzatek <tbzatek@redhat.com> - 3.1.2-1
- Update to 3.1.2

* Wed May 11 2011 Tomas Bzatek <tbzatek@redhat.com> 3.1.1-1
- Update to 3.1.1

* Tue Apr 26 2011 Matthias Clasen <mclasen@redhat.com> 3.0.1-1
- Update to 3.0.1

* Mon Apr  4 2011 Matthias Clasen <mclasen@redhat.com> 3.0.0-1
- Update to 3.0.0

* Tue Mar 22 2011 Matthias Clasen <mclasen@redhat.com> 2.91.92-1
- Update to 2.91.92

* Tue Mar  8 2011 Matthias Clasen <mclasen@redhat.com> 2.91.91-1
- Update to 2.91.91

* Tue Feb 22 2011 Matthias Clasen <mclasen@redhat.com> 2.91.90-1
- Update to 2.91.90

* Thu Feb 10 2011 Matthias Clasen <mclasen@redhat.com> 2.91.7-3
- Rebuild against newer gtk

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.91.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Christopher Aillon <caillon@redhat.com> 2.91.7-1
- Update to 2.91.7

* Fri Jan 14 2011 Matthias Clasen <mclasen@redhat.com> 2.91.6-1
- Update to 2.91.6

* Sun Jan  9 2011 Matthias Clasen <mclasen@redhat.com> 2.91.5-1
- Update to 2.91.5

* Fri Dec  3 2010 Matthias Clasen <mclasen@redhat.com> 2.91.3-1
- Update to 2.91.3

* Tue Nov  9 2010 Tomas Bzatek <tbzatek@redhat.com> 2.91.2-1
- Update to 2.91.2

* Tue Nov  2 2010 Matthias Clasen <mclasen@redhat.com> 2.91.1-1
- Update to 2.91.1

* Sat Oct 16 2010 Siddhesh Poyarekar <spoyarek@redhat.com> 2.91.0-2
- Add librsvg to BuildRequires to build native svg support

* Wed Oct  6 2010 Matthias Clasen <mclasen@redhat.com> 2.91.0-1
- Update to 2.91.0

* Tue Sep 28 2010 Matthias Clasen <mclasen@redhat.com> 2.32.0-1
- Update to 2.32.0

* Tue Aug 31 2010 Matthias Clasen <mclasen@redhat.com> 2.31.91-1
- Update to 2.31.91

* Mon Aug 23 2010 Matthias Clasen <mclasen@redhat.com> 2.31.90-2
- Co-own /usr/share/gtk-doc

* Tue Aug 17 2010 Matthias Clasen <mclasen@redhat.com> 2.31.90-1
- Update to 2.31.90

* Wed Jun 23 2010 Matthias Clasen <mclasen@redhat.com> 2.31.4-0.1.20100623git
- git snapshot that works with glib 2.25.9

* Wed Jun 16 2010 Matthias Clasen <mclasen@redhat.com> 2.31.3-2
- Make installed gsettings schema compile

* Tue Jun  8 2010 Matthias Clasen <mclasen@redhat.com> 2.31.3-1
- Update to 2.31.3

* Thu May 27 2010 Matthias Clasen <mclasen@redhat.com> 2.31.2-1
- Update to 2.31.2

* Sat May 15 2010 Matthias Clasen <mclasen@redhat.com> 2.31.1-1
- Update to 2.31.1

* Tue Apr 27 2010 Matthias Clasen <mclasen@redhat.com> 2.30.1-1
- Update to 2.30.1

* Mon Mar 29 2010 Matthias Clasen <mclasen@redhat.com> 2.30.0-1
- Update to 2.30.0

* Mon Feb 22 2010 Matthias Clasen <mclasen@redhat.com> 2.29.91-1
- Update to 2.29.91

* Wed Feb 10 2010 Bastien Nocera <bnocera@redhat.com> 2.29.90-1
- Update to 2.29.90

* Sun Jan 17 2010 Matthias Clasen <mclasen@redhat.com> 2.29.5-2
 - Rebuild

* Tue Jan 12 2010 Matthias Clasen <mclasen@redhat.com> 2.29.5-1
- Update to 2.29.5

* Thu Dec  3 2009 Matthias Clasen <mclasen@redhat.com> 2.29.3-2
- Don't ship .la files

* Tue Dec 01 2009 Bastien Nocera <bnocera@redhat.com> 2.29.3-1
- Update to 2.29.3

* Mon Sep 21 2009 Matthias Clasen <mclasen@redhat.com> 2.28.0-1
- Update to 2.28.0

* Tue Sep  8 2009 Matthias Clasen <mclasen@redhat.com> 2.27.92-1
- Update to 2.27.92

* Mon Aug 24 2009 Matthias Clasen <mclasen@redhat.com> 2.27.91-1
- Update to 2.27.91

* Fri Aug 14 2009 Matthias Clasen <mclasen@redhat.com> 2.27.90-1
- 2.27.90

* Tue Jul 28 2009 Matthias Clasen <mclasen@redhat.com> 2.27.5-1
- Update to 2.27.5

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.27.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 14 2009 Matthias Clasen <mclasen@redhat.com> 2.27.4-1
- Update to 2.27.4

* Tue Jun 16 2009 Matthias Clasen <mclasen@redhat.com> 2.27.3-1
- Update to 2.27.3

* Wed May 27 2009 Bastien Nocera <bnocera@redhat.com> 2.27.2-1
- Update to 2.27.2

* Sat May 16 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.1-1
- Update to 2.27.1

* Mon Apr 13 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.1-1
- Update to 2.26.1
- See http://download.gnome.org/sources/eog/2.26/eog-2.26.1.news

* Mon Mar 16 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.0-1
- Update to 2.26.0

* Tue Mar  3 2009 Matthias Clasen <mclasen@redhat.com> - 2.25.92-1
- Update to 2.25.92

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.25.91-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 18 2009 Matthias Clasen <mclasen@redhat.com> - 2.25.91-1
- Update to 2.25.91

* Tue Feb  3 2009 Matthias Clasen <mclasen@redhat.com> - 2.25.90-1
- Update to 2.25.90

* Tue Jan 20 2009 Matthias Clasen <mclasen@redhat.com> - 2.25.5-1
- Update to 2.25.5

* Tue Jan  6 2009 Matthias Clasen <mclasen@redhat.com> - 2.25.4-1
- Update to 2.25.4

* Wed Dec 17 2008 Matthias Clasen <mclasen@redhat.com> - 2.25.3-2
- Update to 2.25.3

* Wed Dec  3 2008 Matthias Clasen <mclasen@redhat.com> - 2.25.2-1
- Update to 2.25.2

* Fri Nov 21 2008 Matthias Clasen <mclasen@redhat.com> - 2.25.1-5
- Better URL

* Fri Nov 21 2008 Matthias Clasen <mclasen@redhat.com> - 2.25.1-4
- Tweak %%summary and %%description

* Wed Nov 12 2008 Matthias Clasen <mclasen@redhat.com> - 2.25.1-3
- Update to 2.25.1

* Mon Oct 20 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.1-1
- Update to 2.24.1

* Thu Oct  9 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.0-2
- Save some space

* Mon Sep 22 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.0-1
- Update to 2.24.0

* Mon Sep  8 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.92-1
- Update to 2.23.92

* Tue Sep  2 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.91-1
- Update to 2.23.91

* Fri Aug 22 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.90-1
- Update to 2.23.90

* Tue Aug 12 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.6-2
- Add a possible fix for a deadlock

* Tue Aug  5 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.6-1
- Update to 2.23.6

* Fri Aug  1 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.5-2
- Use standard icon names

* Tue Jul 22 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.5-1
- Update to 2.23.5

* Wed Jun 18 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.4.1-1
- Update to 2.23.4.1

* Wed Jun  4 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.3-1
- Update to 2.23.3

* Wed May 21 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.23.2-2
- fix license tag

* Tue May 13 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.2-1
- Update to 2.23.2

* Fri Apr 25 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.1-1
- Update to 2.23.1
 
* Mon Apr  7 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.1-1
- Update to 2.22.1

* Mon Mar 10 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.0-1
- Update to 2.22.0

* Mon Feb 25 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.92-1
- Update to 2.21.92

* Wed Feb 13 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.90-1
- Update to 2.21.90

* Mon Jan 14 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.4-1
- Update to 2.21.4

* Tue Dec 18 2007 Matthias Clasen <mclasen@redhat.com> - 2.21.3-1
- Update to 2.21.3

* Tue Dec  4 2007 Matthias Clasen <mclasen@redhat.com> - 2.21.2-1
- Update to 2.21.2

* Tue Nov 13 2007 Matthias Clasen <mclasen@redhat.com> - 2.21.1-1
- Update to 2.21.1

* Tue Oct 23 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.1-2
- Rebuild against new dbus-glib

* Mon Oct 15 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.1-1
- Update to 2.20.1 (bug fixes and translation updates)

* Mon Sep 17 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.0-1
- Update to 2.20.0

* Mon Sep  3 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.92-1
- Update to 2.19.92

* Thu Aug 16 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.5-3
- Hide it from the menus _again_

* Tue Aug 14 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.5-2
- Build with XMP support

* Mon Aug 13 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.5-1
- Update to 2.19.5

* Thu Aug  9 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.4-4
- Hide it from the menus again

* Mon Aug  6 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.4-3
- Update license field
- Use %%find_lang for help files, too

* Tue Jul 24 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.4-2
- Fix a undefined macro use (#248689)

* Tue Jul 10 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.4-1
- Update to 2.19.4

* Fri Jul  6 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.3-2
- Fix a directory ownership issue

* Mon Jun  4 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.3-1
- Update to 2.19.3

* Sat May 19 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.2-1
- Update to 2.19.2
- Split off a -devel package
- Small spec fixes

* Sun Apr  1 2007 Matthias Clasen <mclasen@redhat.com> - 2.18.0.1-27
- Fix a problem with the svgz patch

* Tue Mar 13 2007 Matthias Clasen <mclasen@redhat.com> - 2.18.0.1-1
- Update to 2.18.0.1

* Tue Feb 27 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.92-1
- Update to 2.17.92

* Tue Feb 13 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.91-1
- Update to 2.17.91

* Mon Jan 22 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.90-1
- Update to 2.17.90

* Wed Jan 10 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.4-1
- Update to 2.17.4

* Tue Jan 09 2007 Behdad Esfahbod <besfahbo@redhat.com> - 2.17.3-2
- Handle svgz images
- Resolves: #219782

* Tue Dec 19 2006 Matthias Clasen <mclasen@redhat.com> - 2.17.3-1
- Update to 2.17.3

* Tue Dec  5 2006 Matthias Clasen <mclasen@redhat.com> - 2.17.2-1
- Update to 2.17.2

* Fri Oct 20 2006 Matthias Clasen <mclasen@redhat.com> - 2.17.1-1
- Update to 2.17.1

* Wed Oct 18 2006 Matthias Clasen <mclasen@redhat.com> - 2.16.0.1-3
- Fix scripts according to the packaging guidelines

* Thu Sep  7 2006 Matthias Clasen <mclasen@redhat.com> - 2.16.0.1-2.fc6
- Fix some directory ownership issues

* Mon Sep  4 2006 Matthias Clasen <mclasen@redhat.com> - 2.16.0.1-1.fc6
- Update to 2.16.0.1

* Mon Aug 21 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.92-1.fc6
- Update to 2.15.92

* Sat Aug 12 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.91-1.fc6
- Update to 2.15.91

* Wed Aug  2 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.90-1.fc6
- Update to 2.15.90

* Wed Jul 12 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.4-1
- Update to 2.15.4

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.15.3-1.1
- rebuild

* Tue Jun 13 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.3-1
- Update to 2.15.3

* Mon May 22 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.2-1
- Update to 2.15.2

* Sat May 20 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.1-2
- Add missing BuildRequires (#129025)

* Tue May  9 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.1-1
- Update to 2.15.1
- Remove workaround for a long-fixed bug

* Mon Apr 10 2006 Matthias Clasen <mclasen@redhat.com> - 2.14.1-2
- Update to 2.14.1

* Mon Mar 13 2006 Matthias Clasen <mclasen@redhat.com> - 2.14.0-1
- Update to 2.14.0

* Sat Mar  4 2006 Matthias Clasen <mclasen@redhat.com> - 2.13.92-1
- Update to 2.13.92
- Drop upstreamed patch

* Wed Feb 15 2006 Matthias Clasen <mclasen@redhat.com> - 2.13.91-2
- silence excessive debug output

* Wed Feb 15 2006 Matthias Clasen <mclasen@redhat.com> - 2.13.91-1
- Update to 2.13.91

* Mon Feb 13 2006 Matthias Clasen <mclasen@redhat.com> - 2.13.90-2
- Append NoDisplay=true to the right file

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.13.90-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.13.90-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Jan 30 2006 Matthias Clasen <mclasen@redhat.com> 2.13.90-1
- Update to 2.13.90

* Mon Jan 16 2006 Matthias Clasen <mclasen@redhat.com> 2.13.5-1
- Update to 2.13.5

* Fri Jan 13 2006 Matthias Clasen <mclasen@redhat.com> 2.13.4-1
- Update to 2.13.4

* Wed Dec 14 2005 Matthias Clasen <mclasen@redhat.com> 2.13.3-1
- Update to 2.13.3

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Nov 30 2005 Matthias Clasen <mclasen@redhat.com> 2.13.2-1
- Update to 2.13.2

* Thu Oct  6 2005 Matthias Clasen <mclasen@redhat.com> 2.12.1-1
- Update to 2.12.1

* Wed Sep  7 2005 Matthias Clasen <mclasen@redhat.com> 2.12.0-1
- Update to 2.12.0

* Tue Aug 16 2005 Matthias Clasen <mclasen@redhat.com> 
- Rebuilt

* Thu Aug  4 2005 Matthias Clasen <mclasen@redhat.com> 2.11.90-1
- Newer upstream version

* Fri Jul  8 2005 Matthias Clasen <mclasen@redhat.com> 2.11.0-1
- Update to 2.11.0

* Mon Mar 28 2005 Matthias Clasen <mclasen@redhat.com> 2.10.0-1
- Update to 2.10.0

* Thu Mar  3 2005 Marco Pesenti Gritti <mpg@redhat.com> 2.9.0-2
- Rebuild

* Mon Jan 31 2005 Matthias Clasen <mclasen@redhat.com> 2.9.0-1
- Update to 2.9.0

* Sat Nov  6 2004 Marco Pesenti Gritti <mpg@redhat.com> 2.8.1-1
- Update to 2.8.1

* Thu Sep 30 2004 Christopher Aillon <caillon@redhat.com> 2.8.0-3
- Prereq desktop-file-utils >= 0.9
- update-desktop-database on uninstall

* Sun Sep 26 2004 Christopher Aillon <caillon@redhat.com> 2.8.0-2
- Remove the graphics menu entry (#131724)

* Wed Sep 22 2004 Christopher Aillon <caillon@redhat.com> 2.8.0-1
- Update to 2.8.0

* Wed Aug 19 2004 Christopher Aillon <caillon@redhat.com> 2.7.1-1
- Update to 2.7.1

* Mon Aug 16 2004 Christopher Aillon <caillon@redhat.com> 2.7.0-3
- Use update-desktop-database instead of rebuild-mime-info-cache

* Sun Aug 15 2004 Christopher Aillon <caillon@redhat.com> 2.7.0-2
- Rebuild MIME info cache

* Sun Aug 15 2004 Christopher Aillon <caillon@redhat.com> 2.7.0-1
- Update to 2.7.0

* Tue Jun 29 2004 Christopher Aillon <caillon@redhat.com> 2.6.1-1
- Update to 2.6.1

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sat Apr 10 2004 Warren Togami <wtogami@redhat.com> 2.6.0-2
- BR intltool libjpeg-devel scrollkeeper gettext

* Fri Apr  2 2004 Alex Larsson <alexl@redhat.com> 2.6.0-1
- update to 2.6.0

* Wed Mar 10 2004 Alex Larsson <alexl@redhat.com> 2.5.90-1
- update to 2.5.90

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Feb 26 2004 Alexander Larsson <alexl@redhat.com> 2.5.6-1
- update to 2.5.6

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Jan 30 2004 Alexander Larsson <alexl@redhat.com> 2.5.3-1
- update to 2.5.3

* Fri Oct  3 2003 Alexander Larsson <alexl@redhat.com> 2.4.0-1
- 2.4.0

* Fri Aug 29 2003 Alexander Larsson <alexl@redhat.com> 2.3.5-2
- prereq gconf2 (#90698)

* Tue Aug 19 2003 Alexander Larsson <alexl@redhat.com> 2.3.5-1
- update for gnome 2.3

* Tue Jul 29 2003 Havoc Pennington <hp@redhat.com> 2.2.2-2
- rebuild

* Mon Jul  7 2003 Havoc Pennington <hp@redhat.com> 2.2.2-1
- 2.2.2
- remove arg-escaping patch now upstream

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Apr  1 2003 Havoc Pennington <hp@redhat.com> 2.2.0-2
- add patch to better escape filenames passed in as arguments
- add eel2-devel buildreq

* Thu Feb  6 2003 Havoc Pennington <hp@redhat.com> 2.2.0-1
- 2.2.0
- fix dependency versions

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Fri Dec 13 2002 Tim Powers <timp@redhat.com> 1.1.3-1
- update to 1.1.3
- include glade file

* Sun Dec  1 2002 Havoc Pennington <hp@redhat.com>
- 1.1.2

* Tue Aug  6 2002 Havoc Pennington <hp@redhat.com>
- 1.0.2
- remove --copy-generic-name-to-name because there's no GenericName
  anymore
- include libexecdir stuff

* Mon Jul 29 2002 Havoc Pennington <hp@redhat.com>
- copy generic name to name and move to -Extra

* Mon Jul 29 2002 Havoc Pennington <hp@redhat.com>
- 1.0.1, rebuild with new gail

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun Jun 16 2002 Havoc Pennington <hp@redhat.com>
- 1.0.0
- use desktop-file-install

* Fri Jun 07 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment

* Wed Jun 05 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue May 21 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment
- build requires libgnomeprint

* Tue May 21 2002 Havoc Pennington <hp@redhat.com>
- 0.118.0

* Fri May  3 2002 Havoc Pennington <hp@redhat.com>
- 0.117.0

* Thu Apr 25 2002 Havoc Pennington <hp@redhat.com>
- initial build



