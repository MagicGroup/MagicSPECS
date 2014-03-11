Name:           libgnomekbd
Version:        3.6.0
Release:        2%{?dist}
Summary:        A keyboard configuration library

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://gswitchit.sourceforge.net
# VCS: git:git://git.gnome.org/libgnomekbd
Source0:        http://download.gnome.org/sources/libgnomekbd/3.6/libgnomekbd-%{version}.tar.xz

BuildRequires:  gtk3-devel >= 3.0.0
BuildRequires:  cairo-devel
BuildRequires:  libxklavier-devel
BuildRequires:  desktop-file-utils
BuildRequires:  gettext
BuildRequires:  intltool
BuildRequires:  chrpath
BuildRequires:  GConf2-devel
BuildRequires:  gobject-introspection-devel

Requires(post): GConf2
Obsoletes:      libgnomekbd-capplet < 3.3.90-2

%description
The libgnomekbd package contains a GNOME library which manages
keyboard configuration and offers various widgets related to
keyboard configuration.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}


%description    devel
The libgnomekbd-devel package contains libraries and header files for
developing applications that use libgnomekbd.


%prep
%setup -q

%build
%configure --disable-static \
           --disable-compile-warnings \
           --enable-introspection
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

chrpath --delete $RPM_BUILD_ROOT%{_libdir}/libgnomekbdui.so.8.0.0

desktop-file-install --delete-original       \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications             \
  $RPM_BUILD_ROOT%{_datadir}/applications/gkbd-keyboard-display.desktop

%find_lang %{name}

%preun
%gconf_schema_remove desktop_gnome_peripherals_keyboard_xkb

%post
/sbin/ldconfig
touch --no-create %{_datadir}/icons/hicolor >&/dev/null || :

%postun
/sbin/ldconfig
if [ $1 -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor >&/dev/null || :
  gtk-update-icon-cache %{_datadir}/icons/hicolor >&/dev/null || :
  glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor >&/dev/null || :
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :

%files -f %{name}.lang
%doc AUTHORS COPYING.LIB
%{_libdir}/*.so.*
%{_datadir}/libgnomekbd
%{_datadir}/glib-2.0/schemas/org.gnome.libgnomekbd*.gschema.xml
%{_libdir}/girepository-1.0/Gkbd-3.0.typelib
%{_bindir}/gkbd-keyboard-display
%{_datadir}/applications/gkbd-keyboard-display.desktop
%{_datadir}/GConf/gsettings/libgnomekbd.convert


%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_datadir}/gir-1.0/Gkbd-3.0.gir


%changelog
* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Sep 25 2012 Kalev Lember <kalevlember@gmail.com> - 3.6.0-1
- Update to 3.6.0

* Tue Aug 28 2012 Richard Hughes <hughsient@gmail.com> - 3.5.90-1
- Update to 3.5.90

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 07 2012 Richard Hughes <hughsient@gmail.com> - 3.5.2-2
- Fix the call to chrpath

* Thu Jun 07 2012 Richard Hughes <hughsient@gmail.com> - 3.5.2-1
- Update to 3.5.2

* Tue Mar 27 2012 Richard Hughes <hughsient@gmail.com> - 3.4.0.2-1
- Update to 3.4.0.2

* Tue Mar 27 2012 Kalev Lember <kalevlember@gmail.com> - 3.4.0.1-1
- Update to 3.4.0.1
- Obsolete the -capplet subpackage; the whole plugins architecture is
  removed from libgnomekbd

* Fri Feb 25 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.90-1
- Update to 3.3.90

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Sep 27 2011 Ray <rstrode@redhat.com> - 3.2.0-1
- Update to 3.2.0

* Tue Sep 27 2011 Ray <rstrode@redhat.com> - 3.1.92-1
- Update to 3.1.92

* Sat May 07 2011 Christopher Aillon <caillon@redhat.com> - 3.0.0-3
- Update gsettings scriptlet

* Tue Apr  5 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.0-2
- Fix size of keyboard indicator in fallback mode

* Mon Apr  4 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.0-1
- Update to 3.0.0

* Mon Mar  7 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.91-1
- Update to 2.91.91

* Tue Feb 22 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.90-1
- Update to 2.91.90

* Sun Feb 13 2011 Christopher Aillon <caillon@redhat.com> - 2.91.5-10
- Rebuild against newer libxklavier

* Thu Feb 10 2011 Matthias Clasen <mclasen@redhat.com> 2.91.5-9
- Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.91.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Feb 03 2011 Bastien Nocera <bnocera@redhat.com> 2.91.5-7
- Disable separate layouts per window

* Wed Feb 02 2011 Ray Strode <rstrode@redhat.com> 2.91.5-6
- Fix error at login screen

* Wed Feb  2 2011 Matthias Clasen <mclasen@redhat.com> 2.91.5-5
- Build with introspection

* Wed Feb  2 2011 Matthias Clasen <mclasen@redhat.com> 2.91.5-3
- Rebuild against newer gtk

* Tue Jan 25 2011 Matthias Clasen <mclasen@redhat.com> 2.91.5-2
- Fix scriptlet problems (#650378)

* Mon Jan 10 2011 Matthias Clasen <mclasen@redhat.com> 2.91.5-1
- Update to 2.91.5

* Fri Jan  7 2011 Matthias Clasen <mclasen@redhat.com> 2.91.4-1
- Update to 2.91.4

* Fri Dec  3 2010 Matthias Clasen <mclasen@redhat.com> 2.91.3.1-1
- Update to 2.91.3.1

* Thu Nov 11 2010 Matthias Clasen <mclasen@redhat.com> 2.91.2-1
- Update to 2.91.2

* Tue Nov  2 2010 Matthias Clasen <mclasen@redhat.com> 2.91.1-4
- Fix pc file deps

* Mon Nov  1 2010 Matthias Clasen <mclasen@redhat.com> 2.91.1-3
- Add missing BR (#641122)

* Fri Oct 29 2010 Bill Nottingham <notting@redhat.com> 2.91.1-2
- fix crashing gnome-settings-daemon (#642454)

* Wed Oct 06 2010 Richard Hughes <rhughes@redhat.com> 2.91.1-1
- Update to 2.91.1
- Remove obsolete patches
- Remove RPATH

* Wed Sep 29 2010 Matthias Clasen <mclasen@redhat.com> 2.32.0-1
- Update to 2.32.0

* Thu Sep 16 2010 Parag Nemade <paragn AT fedoraproject.org> 2.31.5-2
- spec cleanup

* Tue Jul 13 2010 Matthias Clasen <mclasen@redhat.com> 2.31.5-1
- Update to 2.31.5

* Tue Jun  8 2010 Matthias Clasen <mclasen@redhat.com> 2.31.2-0.1.git06082010
- Snapshot needed for other builds

* Thu May 27 2010 Matthias Clasen <mclasen@redhat.com> 2.31.1-1
- Update to 2.31.1

* Mon Apr 26 2010 Matthias Clasen <mclasen@redhat.com> 2.30.1-1
- Update to 2.30.1
- Spec file cleanups

* Wed Apr  7 2010 Matthias Clasen <mclasen@redhat.com> 2.30.0-2
- Fix an invalid schema default

* Mon Mar 29 2010 Matthias Clasen <mclasen@redhat.com> 2.30.0-1
- Update to 2.30.0

* Wed Mar 24 2010 Matthias Clasen <mclasen@redhat.com> 2.29.92-2
- Fix a crash in the keyboard indicator

* Tue Mar 09 2010 Bastien Nocera <bnocera@redhat.com> 2.29.92-1
- Update to 2.29.92

* Sat Jan 16 2010 Matthias Clasen <mclasen@redhat.com> - 2.29.5-1
- Update 2.29.5

* Thu Dec 03 2009 Bastien Nocera <bnocera@redhat.com> 2.28.0-4
- Remove debug in patch

* Thu Dec  3 2009 Matthias Clasen <mclasen@redhat.com> - 2.28.0-3
- Small spec fixes

* Thu Oct  8 2009 Matthias Clasen <mclasen@redhat.com> - 2.28.0-2
- Incorporate visual fixes from upstream

* Wed Sep 23 2009 Matthias Clasen <mclasen@redhat.com> - 2.28.0-1
- Update to 2.28.0

* Tue Aug 25 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.91-1
- Update to 2.27.91

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.27.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 15 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.4-1
- Update to 2.27.4

* Tue Jun 30 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.2-3
- Rebuild against new libxklavier
- Adapt to api changes

* Sun May 31 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.2-1
- Update to 2.27.2

* Mon Mar 16 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.0-1
- Update to 2.26.0

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.25.91-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 23 2009 Matthias Clasen <mclasen@redhat.com> - 2.25.91-1
- Update to 2.25.91

* Mon Sep 22 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.0-1
- Update to 2.24.0

* Thu Sep  4 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.91-1
- Update to 2.23.91

* Fri Aug 29 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.2-2
- Plug a small memory leak

* Sun May 11 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.2-1
- Update to 2.23.2

* Sun Apr  6 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.0-2
- Split the plugins capplet off into a subpackage, since we don't
  have any plugins and don't want the capplet by default

* Thu Mar 20 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.0-1
- Update to 2.22.0

* Thu Jan 31 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.4.1-2
- Rebuild against new libxklavier

* Tue Dec 18 2007 Matthias Clasen <mclasen@redhat.com> - 2.21.4.1-1
- Update to 2.21.4.1

* Thu Dec 13 2007 Matthias Clasen <mclasen@redhat.com> - 2.21.4-1
- Update to 2.21.4

* Tue Nov 13 2007 Matthias Clasen <mclasen@redhat.com> - 2.21.1-1
- Update to 2.21.1

* Tue Oct 23 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.0-2
- Rebuild against new dbus-glib

* Mon Sep 17 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.0-1
- Update to 2.20.0

* Mon Sep  3 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.91-1
- Update to 2.19.91

* Mon Aug 13 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.90-2
- Fix a bad free

* Sun Aug 12 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.90-1
- Update to 2.19.90 

* Tue Aug  7 2007 Matthias Clasen <mclasen@redhat.com> - 2.18.2-2
- Update the license field

* Sun May 20 2007 Matthias Clasen <mclasen@redhat.com> - 2.18.2-1
- Update to 2.18.2

* Sun May 20 2007 Matthias Clasen <mclasen@redhat.com> - 2.18.1-1
- Update to 2.18.1

* Wed Apr  4 2007 Matthias Clasen <mclasen@redhat.com> - 2.18.0-2
- Fix a typo in URL

* Tue Mar 13 2007 Matthias Clasen <mclasen@redhat.com> - 2.18.0-1
- Update to 2.18.0

* Wed Jan 24 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.2-2
- Port former control-center patches to improve keyboard drawing

* Tue Nov  7 2006 Matthias Clasen <mclasen@redhat.com> - 2.17.2-1
- Update to 2.17.2

* Tue Nov  7 2006 Matthias Clasen <mclasen@redhat.com> - 0.1-4
- Fix up Requires

* Thu Nov  2 2006 Matthias Clasen <mclasen@redhat.com> - 0.1-3
- Don't use --Werror

* Sat Oct 28 2006 Matthias Clasen <mclasen@redhat.com> - 0.1-2
- Fix a memory allocation error

* Sat Oct 28 2006 Matthias Clasen <mclasen@redhat.com> - 0.1-1
- Initial release
