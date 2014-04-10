%define gtk3_version                      3.3.6
%define glib2_version                     2.35.0
%define gtk_doc_version                   1.9
%define gsettings_desktop_schemas_version 3.5.91
%define po_package                        gnome-desktop-3.0

Summary: Shared code among gnome-panel, gnome-session, nautilus, etc
Summary(zh_CN.UTF-8): gnome-panel, gnome-session, nautils 等包共享的代码
Name: gnome-desktop3
Version:	3.12.0
Release: 1%{?dist}
URL: http://www.gnome.org
%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
Source0: http://download.gnome.org/sources/gnome-desktop/%{majorver}/gnome-desktop-%{version}.tar.xz
Patch0: 0001-default-input-sources-Switch-ja_JP-default-to-ibus-k.patch

License: GPLv2+ and LGPLv2+
Group: System Environment/Libraries

# needed for GnomeWallClock
Requires: gsettings-desktop-schemas >= %{gsettings_desktop_schemas_version}

Requires: magic-menus

# Make sure to update libgnome schema when changing this
Requires: system-backgrounds-gnome

# Make sure that gnome-themes-standard gets pulled in for upgrades
Requires: gnome-themes-standard

BuildRequires: gnome-common
BuildRequires: gtk3-devel >= %{gtk3_version}
BuildRequires: gobject-introspection-devel
BuildRequires: gsettings-desktop-schemas-devel >= %{gsettings_desktop_schemas_version}
BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: libxkbfile-devel
BuildRequires: xkeyboard-config-devel
BuildRequires: gettext
BuildRequires: gtk-doc >= %{gtk_doc_version}
BuildRequires: automake autoconf libtool intltool
BuildRequires: itstool
BuildRequires: iso-codes-devel

# GnomeIdleMonitor API change breaks older gnome-shell versions
Conflicts: gnome-shell < 3.7.90

%description

The gnome-desktop package contains an internal library
(libgnomedesktop) used to implement some portions of the GNOME
desktop, and also some data files and other shared components of the
GNOME user environment.

%description -l zh_CN.UTF-8 
GNOME 桌面环境程序的共享代码。

%package devel
Summary: Libraries and headers for libgnome-desktop
Summary(zh_CN.UTF-8): %{name} 的开发包
License: LGPLv2+
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %name = %{version}-%{release}

Requires: gtk3-devel >= %{gtk3_version}
Requires: glib2-devel >= %{glib2_version}
Requires: startup-notification-devel >= %{startup_notification_version}

%description devel
Libraries and header files for the GNOME-internal private library
libgnomedesktop.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n gnome-desktop-%{version}
%patch0 -p1

%build
%configure --with-pnp-ids-path="/usr/share/hwdata/pnp.ids"
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

# stuff we don't want
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a
magic_rpm_clean.sh
%find_lang %{po_package} --all-name --with-gnome

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{po_package}.lang
%doc AUTHORS COPYING COPYING.LIB NEWS README
%{_datadir}/gnome/gnome-version.xml
%{_libexecdir}/gnome-rr-debug
# LGPL
%{_libdir}/lib*.so.*
%{_libdir}/girepository-1.0/GnomeDesktop-3.0.typelib

%files devel
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{_datadir}/gir-1.0/GnomeDesktop-3.0.gir
%dir %{_datadir}/gtk-doc/
%dir %{_datadir}/gtk-doc/html/
%doc %{_datadir}/gtk-doc/html/gnome-desktop3/

%changelog
* Wed Apr 09 2014 Liu Di <liudidi@gmail.com> - 3.12.0-1
- 更新到 3.12.0

* Wed Feb 19 2014 Richard Hughes <rhughes@redhat.com> - 3.11.90-1
- Update to 3.11.90

* Tue Feb 04 2014 Richard Hughes <rhughes@redhat.com> - 3.11.5-1
- Update to 3.11.5

* Thu Jan 16 2014 Richard Hughes <rhughes@redhat.com> - 3.11.4-1
- Update to 3.11.4

* Mon Nov 25 2013 Richard Hughes <rhughes@redhat.com> - 3.11.2-1
- Update to 3.11.2

* Fri Nov 01 2013 Kalev Lember <kalevlember@gmail.com> - 3.11.1-1
- Update to 3.11.1

* Mon Oct 28 2013 Richard Hughes <rhughes@redhat.com> - 3.10.1-1
- Update to 3.10.1

* Tue Sep 24 2013 Kalev Lember <kalevlember@gmail.com> - 3.10.0-1
- Update to 3.10.0

* Wed Sep 18 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.92-1
- Update to 3.9.92

* Mon Sep  9 2013 Rui Matos <rmatos@redhat.com> - 3.9.91-2
- Add patch to default to ibus-kkc for Japanese

* Tue Sep 03 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.91-1
- Update to 3.9.91

* Thu Aug 22 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.90-1
- Update to 3.9.90

* Fri Aug 09 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.5-1
- Update to 3.9.5

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.9.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jun 02 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.1.1-1
- Update to 3.9.1.1
- Remove unused startup-notification dependency

* Tue May 14 2013 Richard Hughes <rhughes@redhat.com> - 3.8.2-1
- Update to 3.8.2

* Mon Apr 15 2013 Kalev Lember <kalevlember@gmail.com> - 3.8.1-1
- Update to 3.8.1

* Wed Mar 27 2013 Kalev Lember <kalevlember@gmail.com> - 3.8.0.1-1
- Update to 3.8.0.1

* Tue Mar 26 2013 Kalev Lember <kalevlember@gmail.com> - 3.8.0-1
- Update to 3.8.0

* Tue Mar 19 2013 Matthias Clasen <mclasen@redhat.com> - 3.7.92-1
- Update to 3.7.92

* Wed Mar  6 2013 Matthias Clasen <mclasen@redhat.com> - 3.7.91.1-1
- Update to 3.7.91.1

* Thu Feb 21 2013 Kalev Lember <kalevlember@gmail.com> - 3.7.90-2
- Conflict with older gnome-shell versions

* Wed Feb 20 2013 Richard Hughes <rhughes@redhat.com> - 3.7.90-1
- Update to 3.7.90

* Tue Feb 05 2013 Richard Hughes <rhughes@redhat.com> - 3.7.5-1
- Update to 3.7.5

* Tue Jan 15 2013 Matthias Clasen <mclasen@redhat.com> - 3.7.4-1
- Update to 3.7.4

* Thu Dec 20 2012 Kalev Lember <kalevlember@gmail.com> - 3.7.3-1
- Update to 3.7.3

* Tue Nov 20 2012 Richard Hughes <hughsient@gmail.com> - 3.7.2-1
- Update to 3.7.2

* Fri Nov 09 2012 Kalev Lember <kalevlember@gmail.com> - 3.7.1-1
- Update to 3.7.1

* Wed Oct 17 2012 Kalev Lember <kalevlember@gmail.com> - 3.6.1-1
- Update to 3.6.1

* Wed Sep 26 2012 Richard Hughes <hughsient@gmail.com> - 3.6.0.1-1
- Update to 3.6.0.1

* Tue Sep 25 2012 Richard Hughes <hughsient@gmail.com> - 3.6.0-1
- Update to 3.6.0

* Thu Sep 06 2012 Richard Hughes <hughsient@gmail.com> - 3.5.91-1
- Update to 3.5.91

* Wed Aug 22 2012 Richard Hughes <hughsient@gmail.com> - 3.5.90-1
- Update to 3.5.90

* Tue Aug 07 2012 Richard Hughes <hughsient@gmail.com> - 3.5.5-1
- Update to 3.5.5

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 17 2012 Richard Hughes <hughsient@gmail.com> - 3.5.4-1
- Update to 3.5.4

* Tue Jun 26 2012 Richard Hughes <hughsient@gmail.com> - 3.5.3-1
- Update to 3.5.3

* Thu Jun 07 2012 Richard Hughes <hughsient@gmail.com> - 3.5.2-3
- Add missing files

* Thu Jun 07 2012 Richard Hughes <hughsient@gmail.com> - 3.5.2-2
- Add missing BRs

* Wed Jun 06 2012 Richard Hughes <hughsient@gmail.com> - 3.5.2-1
- Update to 3.5.2

* Mon May 14 2012 Richard Hughes <hughsient@gmail.com> - 3.4.2-1
- Update to 3.4.2

* Mon Apr 16 2012 Daniel Drake <dsd@laptop.org> - 3.4.1-2
- Add upstream patch to fix crash when the system clock is wrong
- Fixes GNOME#673551, OLPC#11714

* Mon Apr 16 2012 Richard Hughes <hughsient@gmail.com> - 3.4.1-1
- Update to 3.4.1

* Mon Mar 26 2012 Richard Hughes <rhughes@redhat.com> - 3.4.0-1
- New upstream version.

* Mon Mar 19 2012 Richard Hughes <rhughes@redhat.com> 3.3.92-1
- Update to 3.3.92

* Tue Feb  6 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.5-1
- Update to 3.3.5

* Tue Jan 17 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.4-1
- Update to 3.3.4

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 20 2011 Matthias Clasen <mclasen@redhat.com> - 3.3.3-1
- Update to 3.3.3

* Mon Nov 21 2011 Matthias Clasen <mclasen@redhat.com> - 3.3.2-1
- Update to 3.3.2

* Wed Nov  2 2011 Matthias Clasen <mclasen@redhat.com> - 3.3.1-1
- Update to 3.3.1

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-2
- Rebuilt for glibc bug#747377

* Tue Oct 18 2011 Matthias Clasen <mclasen@redhat.com> - 3.2.1-1
- Update to 3.2.1

* Tue Sep 27 2011 Ray <rstrode@redhat.com> - 3.2.0-1
- Update to 3.2.0

* Tue Sep 27 2011 Ray <rstrode@redhat.com> - 3.2.0-1
- Update to 3.2.0

* Mon Sep 19 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.92-1
- Update to 3.1.92

* Mon Sep 12 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.91-3
- Fix a gnome-screensaver crash

* Fri Sep  9 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.91-2
- Require gsettings-desktop-schemas

* Tue Sep  5 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.91-1
- Update to 3.1.91

* Tue Aug 30 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.90.1-1
- Update to 3.1.90.1

* Tue Aug 16 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.5-1
- Update to 3.1.5

* Mon Jul 25 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.4-1
- Update to 3.1.4

* Mon Jul 04 2011 Bastien Nocera <bnocera@redhat.com> 3.1.3-1
- Update to 3.1.3

* Tue Jun 14 2011 Tomas Bzatek <tbzatek@redhat.com> - 3.1.2-1
- Update to 3.1.2

* Wed May 11 2011 Tomas Bzatek <tbzatek@redhat.com> - 3.1.1-1
- Update to 3.1.1

* Mon May  2 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.1-2
- Prevent segfaults in gnome-rr users on randr-less displays

* Tue Apr 26 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.1-1
- Update to 3.0.1

* Fri Apr 15 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.0-2
- Require gnome-themes-standard (#674799)

* Mon Apr  4 2011 Christopher Aillon <caillon@redhat.com> - 3.0.0-1
- Update to 3.0.0

* Thu Mar 24 2011 Christopher Aillon <caillon@redhat.com> - 2.91.93-1
- Update to 2.91.93

* Tue Mar 22 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.92-1
- Update to 2.91.92

* Mon Mar  7 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.91-1
- Update to 2.91.91

* Mon Feb 21 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.90-1
- 2.91.90
- Drop obsolete GConf dep

* Thu Feb 10 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.6.1-4
- Rebuild against newer gtk

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.91.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb 04 2011 Bastien Nocera <bnocera@redhat.com> 2.91.6.1-2
- Fix refcount issue in GnomeRRLabeler

* Wed Feb  2 2011 Matthias Clasen <mclasen@redhat.com> 2.91.6.1-1
- Update to 2.91.6.1

* Wed Feb  2 2011 Matthias Clasen <mclasen@redhat.com> 2.91.6-3
- Rebuild against newer gtk

* Fri Jan 28 2011 Matthias Clasen <mclasen@redhat.com> 2.91.6-2
- Build with introspection support

* Tue Jan 11 2011 Matthias Clasen <mclasen@redhat.com> 2.91.6-1
- Update to 2.91.6

* Mon Jan 10 2011 Matthias Clasen <mclasen@redhat.com> 2.91.5-1
- Update to 2.91.5

* Fri Jan  7 2011 Matthias Clasen <mclasen@redhat.com> 2.91.4-1
- Update to 2.91.4

* Fri Dec  3 2010 Matthias Clasen <mclasen@redhat.com> 2.91.3-2
- Rebuild against new gtk

* Thu Nov 25 2010 Bastien Nocera <bnocera@redhat.com> 2.91.3-1
- Update to 2.91.3

* Wed Nov 17 2010 Bastien Nocera <bnocera@redhat.com> 2.91.2-1
- Update to 2.91.2

* Thu Nov 11 2010 Bill Nottingham <notting@redhat.com> 2.91.1-3
- remove some extraneous deps

* Thu Nov 11 2010 Bastien Nocera <bnocera@redhat.com> 2.91.1-2
- Fix a possible double-free crasher

* Wed Nov 10 2010 Bastien Nocera <bnocera@redhat.com> 2.91.1-1
- Update to 2.91.1

* Tue Nov  2 2010 Matthias Clasen <mclasen@redhat.com> 2.91.0-3
- Rebuild against newer gtk3

* Thu Oct 28 2010 Bill Nottingham <notting@redhat.com> 2.91.0-2
- flip background to match F-14

* Mon Oct  4 2010 Matthias Clasen <mclasen@redhat.com> 2.91.0-1
- Update to 2.91.0

* Wed Sep 29 2010 jkeating - 2.90.4-4
- Rebuilt for gcc bug 634757

* Wed Sep 22 2010 Matthias Clasen <mclasen@redhat.com> 2.90.4-3
- Rebuild against newer gobject-introspection
- Rebuild against newer gtk

* Thu Aug 19 2010 Matthias Clasen <mclasen@redhat.com> 2.90.4-2
- Prevent file conflict with gnome-desktop

* Tue Jun 29 2010 Matthias Clasen <mclasen@redhat.com> 2.90.4-1
- Update to 2.90.4

* Mon Jun 28 2010 Matthias Clasen <mclasen@redhat.com> 2.90.2-1
- 2.90.2

* Thu Jun 17 2010 Richard Hughes <richard@hughsie.com> 2.90.1-1
- Initial build for review.

