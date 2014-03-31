%global __python %{__python3}

Name:           eog-plugins
Version:        3.11.4
Release:        4%{?dist}
Summary:        A collection of plugins for the eog image viewer

Group:          User Interface/Desktops
License:        GPLv2+
URL:            http://live.gnome.org/EyeOfGnome/Plugins
#VCS: git:git://git.gnome.org/eog-plugins
Source0:        http://download.gnome.org/sources/eog-plugins/3.11/%{name}-%{version}.tar.xz

BuildRequires:  eog-devel
BuildRequires:  clutter-gtk-devel
BuildRequires:  gsettings-desktop-schemas-devel
BuildRequires:  libchamplain-gtk-devel
BuildRequires:  libexif-devel
BuildRequires:  intltool
BuildRequires:  libgdata-devel >= 0.6.0
BuildRequires:  libpeas-devel
BuildRequires:  python3-devel

Requires:       eog

%description
It's a collection of plugins for use with the Eye of GNOME Image Viewer.
The included plugins provide a map view for where the picture was taken,
display of Exif information, Zoom to fit, etc.

%prep
%setup -q

%build
%configure --disable-silent-rules
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT%{_libdir}/eog/plugins/*.la

%find_lang %{name}

%postun
if [ $1 -eq 0 ]; then
  glib-compile-schemas %{_datadir}/glib-2.0/schemas || :
fi

%posttrans
glib-compile-schemas %{_datadir}/glib-2.0/schemas || :

%files -f %{name}.lang
%doc COPYING NEWS
%{_libdir}/eog/plugins/*.so
%{_libdir}/eog/plugins/*.py
%{_libdir}/eog/plugins/*.plugin
%{_libdir}/eog/plugins/__pycache__
%{_libdir}/eog/plugins/pythonconsole/
%{_datadir}/eog/plugins
%{_datadir}/glib-2.0/schemas/org.gnome.eog.plugins.exif-display.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.eog.plugins.fullscreenbg.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.eog.plugins.pythonconsole.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.eog.plugins.export-to-folder.gschema.xml

%changelog
* Thu Feb 20 2014 Kalev Lember <kalevlember@gmail.com> - 3.11.4-4
- Rebuilt for cogl soname bump

* Mon Feb 10 2014 Peter Hutterer <peter.hutterer@redhat.com> - 3.11.4-3
- Rebuild for libevdev soname bump

* Wed Feb 05 2014 Kalev Lember <kalevlember@gmail.com> - 3.11.4-2
- Build with Python 3

* Tue Jan 14 2014 Richard Hughes <rhughes@redhat.com> - 3.11.4-1
- Update to 3.11.4

* Mon Oct 28 2013 Richard Hughes <rhughes@redhat.com> - 3.10.1-1
- Update to 3.10.1

* Wed Sep 25 2013 Kalev Lember <kalevlember@gmail.com> - 3.10.0-1
- Update to 3.10.0

* Sat Aug 10 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.5-1
- Update to 3.9.5

* Fri Aug 09 2013 Kalev Lember <kalevlember@gmail.com> - 3.8.1-3
- Rebuilt for cogl 1.15.4 soname bump

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed May 22 2013 Kalev Lember <kalevlember@gmail.com> - 3.8.1-1
- Update to 3.8.1

* Tue Mar 26 2013 Kalev Lember <kalevlember@gmail.com> - 3.8.0-1
- Update to 3.8.0

* Wed Mar 20 2013 Richard Hughes <rhughes@redhat.com> - 3.7.92-1
- Update to 3.7.92

* Mon Mar 18 2013 Richard Hughes <rhughes@redhat.com> - 3.7.91-1
- Update to 3.7.91

* Thu Feb 21 2013 Kalev Lember <kalevlember@gmail.com> - 3.6.1-3
- Rebuilt for cogl soname bump

* Fri Jan 25 2013 Peter Robinson <pbrobinson@fedoraproject.org> 3.6.1-2
- Rebuild for new cogl

* Tue Oct 16 2012 Kalev Lember <kalevlember@gmail.com> - 3.6.1-1
- Update to 3.6.1

* Tue Sep 25 2012 Richard Hughes <hughsient@gmail.com> - 3.6.0-1
- Update to 3.6.0

* Wed Sep 19 2012 Kalev Lember <kalevlember@gmail.com> - 3.5.92-1
- Update to 3.5.92

* Tue Sep 04 2012 Richard Hughes <hughsient@gmail.com> - 3.5.91-1
- Update to 3.5.91

* Tue Aug 28 2012 Matthias Clasen <mclasen@redhat.com> - 3.5.5-2
- Rebuild against new cogl/clutter

* Tue Aug 21 2012 Richard Hughes <hughsient@gmail.com> - 3.5.5-1
- Update to 3.5.5

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 07 2012 Richard Hughes <hughsient@gmail.com> - 3.4.1-1
- Update to 3.4.1

* Tue Mar 27 2012 Richard Hughes <hughsient@gmail.com> - 3.4.0-1
- Update to 3.4.0

* Wed Mar 21 2012 Kalev Lember <kalevlember@gmail.com> - 3.3.92-1
- Update to 3.3.92
- Package the python console plugin

* Sat Mar 11 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.91-2
- Rebuild for new cogl

* Tue Mar  6 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.91-1
- Update to 3.3.91

* Sun Feb 26 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.90-1
- Update to 3.3.90

* Tue Jan 24 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 3.2.2-4
- Rebuild for cogl soname bump

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Nov 27 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 3.2.2-2
- Rebuild for new clutter

* Tue Nov 22 2011 Tomas Bzatek <tbzatek@redhat.com> - 3.2.2-1
- Update to 3.2.2

* Tue Jul 26 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.2-1
- Update to 3.1.2

* Fri Apr 22 2011 Christopher Aillon <caillon@redhat.com> - 3.0.0-1
- Update to 3.0.0

* Tue Mar 22 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.90-1
- Update to 2.91.90

* Tue Feb 22 2011 Matthias Clasen <mclasen@redhat.com> - 2.30.2-1
- Update to 2.30.2

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.30.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 22 2011 Matthias Clasen <mclasen@redhat.com> - 2.30.1-1
- Update to 2.30.1

* Wed Jul  7 2010 Matthias Clasen <mclasen@redhat.com> - 2.30.0-2
- Rebuild against new libchamplain

* Mon Mar 29 2010 Matthias Clasen <mclasen@redhat.com> - 2.30.0-1
- Update to 2.30.0

* Mon Feb 22 2010 Matthias Clasen <mclasen@redhat.com> - 2.29.91-1
- Update to 2.29.91

* Mon Feb 15 2010 Matthias Clasen <mclasen@redhat.com> - 2.29.90-1
- Update to 2.29.90

* Wed Jan 13 2010 Matthias Clasen <mclasen@redhat.com> - 2.29.5-1
- Update to 2.29.5

* Tue Sep 22 2009 Matthias Clasen <mclasen@redhat.com> - 2.28.0-1
- Update to 2.28.0

* Tue Sep  8 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.92-1
- Update to 2.27.92

* Fri Aug 28 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.91-2
- Build verbosely

* Tue Aug 25 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.91-1
- Initial packaging
