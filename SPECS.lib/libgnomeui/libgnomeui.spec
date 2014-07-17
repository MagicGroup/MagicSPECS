%define po_package libgnomeui-2.0

Summary: GNOME base GUI library
Summary(zh_CN.UTF-8): GNOME 基本图形界面库
Name: libgnomeui
Version: 2.24.5
Release: 5%{?dist}
URL: http://www.gnome.org
Source0: http://download.gnome.org/sources/libgnomeui/2.24/%{name}-%{version}.tar.bz2

# https://bugzilla.gnome.org/show_bug.cgi?id=606437
Patch0: libgnomeui-2.23.4-disable-event-sounds.patch

License: LGPLv2+
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库

BuildRequires: glib2-devel
BuildRequires: gvfs-devel
BuildRequires: pango-devel
BuildRequires: gtk2-devel
BuildRequires: GConf2-devel
BuildRequires: gnome-vfs2-devel
BuildRequires: libgnomecanvas-devel
BuildRequires: libbonoboui-devel
BuildRequires: libxml2-devel
BuildRequires: libgnome-devel
BuildRequires: libart_lgpl-devel
BuildRequires: libglade2-devel
BuildRequires: gnome-keyring-devel
BuildRequires: libSM-devel
BuildRequires: fontconfig-devel
BuildRequires: gettext
BuildRequires: automake, autoconf, libtool
BuildRequires: intltool

#Requires: yelp
#  This creates a chicken/egg problem with updating yelp:
#  https://bugzilla.redhat.com/bugzilla/show_bug.cgi?id=249000

%description
GNOME (GNU Network Object Model Environment) is a user-friendly set of
GUI applications and desktop tools to be used in conjunction with a
window manager for the X Window System. The libgnomeui package
includes GUI-related libraries that are needed to run GNOME. (The
libgnome package includes the library features that don\'t use the X
Window System.)

%description -l zh_CN.UTF-8
GNOME 基本图形界面库。

%package devel
Summary: Libraries and headers for libgnome
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}
Requires: libSM-devel
Requires: libICE-devel

%description devel
You should install the libgnomeui-devel package if you would like to
compile GNOME applications. You do not need to install
libgnomeui-devel if you just want to use the GNOME desktop
environment.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q
%patch0 -p1 -b .disable-sound-events

libtoolize --force --copy
autoreconf -fisv

%build
%configure --disable-gtk-doc --disable-static

sed -i -e 's/ -shared / -Wl,-O1,--as-needed\0 /g' libtool

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

magic_rpm_clean.sh
%find_lang %{po_package}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{po_package}.lang
%defattr(-,root,root,-)
%doc COPYING.LIB NEWS ChangeLog
%{_libdir}/lib*.so.*
## FIXME questionable that libgnomeui still contains these
%{_datadir}/pixmaps/*
%{_libdir}/libglade/2.0/*.so

%files devel
%defattr(-,root,root,-)
%doc %{_datadir}/gtk-doc/html/libgnomeui
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*
%{_includedir}/*

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 2.24.5-5
- 为 Magic 3.0 重建

* Tue Oct 30 2012 Liu Di <liudidi@gmail.com> - 2.24.5-4
- 为 Magic 3.0 重建

* Sat Jan 07 2012 Liu Di <liudidi@gmail.com> - 2.24.5-3
- 为 Magic 3.0 重建

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.24.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Christopher Aillon <caillon@redhat.com> 2.24.5-1
- Update to 2.24.5

* Wed Oct 06 2010 Parag Nemade <paragn AT fedoraproject.org> 2.24.4-2
- Resolves:rh#638938 - missing dependencies in libgnomeui-devel

* Wed Sep 29 2010 Matthias Clasen <mclasen@redhat.com> 2.24.4-1
- Update to 2.24.4

* Thu Sep 16 2010 Parag Nemade <paragn AT fedoraproject.org> 2.24.3-2
- spec cleanup

* Wed Mar 31 2010 Matthias Clasen <mclasen@redhat.com> - 2.24.3-1
- Update to 2.24.3

* Sun Jul 26 2009 Matthias Clasen <mclasen@redhat.com> - 2.24.1-3
- Save some space

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.24.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Mar 16 2009 Matthias Clasen <mclasen@redhat.com> - 2.24.1-1
- Update to 2.24.1

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.24.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Nov 25 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.0-3
- Reduce unneeded direct library deps

* Mon Sep 22 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.0-2
- Update to 2.24.0

* Sat Sep 20 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.90-3
- Plug a memory leak

* Fri Sep 19 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.90-2
- Plug a memory leak

* Fri Aug 22 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.90-1
- Update to 2.23.90

* Thu Aug 14 2008 Lennart Poettering <lpoetter@redhat.com> - 2.23.4-2
- Disable event sounds because we do them now with libcanberra

* Tue Jun 17 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.4-1
- Update to 2.23.4

* Wed Jun  4 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.3-1
- Update to 2.23.3

* Mon May 19 2008 - Bastien Nocera <bnocera@redhat.com> - 2.22.1-3
- Add patch to fix ObexFTP crasher

* Mon Apr 14 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.1-2
- Bump rev to make sure the NVR is newer than the previous one

* Wed Apr  9 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.1-1
- Update to 2.22.1 (filechooser crash fixes)
- Implement authentication support for the file chooser (Tomas Bzatek)

* Mon Mar 10 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.01-1
- Update to 2.22.01

* Mon Mar 10 2008 - Bastien Nocera <bnocera@redhat.com> - 2.21.93-2
- Add patch to avoid hang on error in the filechooser under EOG

* Fri Mar 07 2008 - Bastien Nocera <bnocera@redhat.com> - 2.21.93-1
- Update to 2.21.93

* Mon Feb 25 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.92-1
- Update to 2.21.92

* Tue Feb 19 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.91-2
- Use gio for thumbnails

* Tue Feb 12 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.91-1
- Update to 2.21.91

* Tue Jan 29 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.90-1
- Update to 2.21.90

* Mon Jan 14 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.5-1
- Update to 2.21.5

* Sat Dec 22 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.1.1-2
- Add the gvfs filechooser backend

* Wed Oct 17 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.1.1-1
- Update to 2.20.1.1 (fixes a crash in thumbnailing code) 

* Mon Oct 15 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.1-1
- Update to 2.20.1 (translation updates, file chooser improvements)

* Wed Sep 19 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.0-1
- Update to 2.20.0

* Thu Aug 23 2007 Adam Jackson <ajax@redhat.com> - 2.19.1-3
- Rebuild for ppc toolchain bug

* Tue Aug  7 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.1-2
- Update the license field

* Mon Jul 30 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.1-1
- Update to 2.19.1

* Fri Jul 20 2007 Jesse Keating <jkeating@redhat.com> 0 2.19.0-2
- Don't require yelp (RH #249000)

* Mon Jun 18 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.0-1
- Update to 2.19.0

* Tue Jun 12 2007 Ray Strode <rstrode@redhat.com> - 2.18.1-3
- Require yelp

* Tue Apr 10 2007 Matthias Clasen <mclasen@redhat.com> - 2.18.1-2
- Add user-dirs support to the gnome-vfs filechooser backend

* Tue Mar 13 2007 Matthias Clasen <mclasen@redhat.com> - 2.18.1-1
- Update to 2.18.1

* Tue Mar 13 2007 Matthias Clasen <mclasen@redhat.com> - 2.18.0-1
- Update to 2.18.0

* Tue Feb 27 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.92-1
- Update to 2.17.92

* Tue Feb 13 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.91-1
- Update to 2.17.91

* Mon Jan 22 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.90-1
- Update to 2.17.90

* Sat Jan 20 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.1-2
- Drop explicit esound requirement in preparation for pulseaudio 
- Clean up requires

* Wed Jan 10 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.1-1
- Update to 2.17.1

* Tue Dec  5 2006 Matthias Clasen <mclasen@redhat.com> - 2.17.0-1
- Update to 2.17.0

* Sat Oct 21 2006 Matthias Clasen <mclasen@redhat.com> - 2.16.1-1
- Update to 2.16.1
- Drop upstreamed patches

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 2.16.0-4
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Tue Sep 26 2006 Matthew Barnes <mbarnes@redhat.com> - 2.16.0-3.fc6
- Make the API documentation easier to navigate.

* Mon Sep 11 2006 Matthias Clasen <mclasen@redhat.com> - 2.16.0-2
- Fix a deadlock when destroying file choosers (#206058)

* Mon Sep  4 2006 Matthias Clasen <mclasen@redhat.com> - 2.16.0-1.fc6
- Update to 2.16.0
- Require pkgconfig in the -devel package

* Fri Sep  1 2006 Matthew Barnes <mbarnes@redhat.com> - 2.15.91-2.fc6
- Don't spawn bug-buddy when bug-buddy itself aborts (RH bug #204943).

* Sat Aug 12 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.91-1.fc6
- Update to 2.15.91

* Thu Aug  3 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.90-1.fc6
- Update to 2.15.90

* Wed Jul 26 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.2-2
- Make GnomeIconList work again

* Wed Jul 12 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.2-1
- Update to 2.15.2

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.15.1-6.1
- rebuild

* Sat Jun 10 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.1-6
- More BuildRequires fixes

* Mon Jun  5 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.1-5
- Fix BuildRequires

* Mon May  8 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.1-4
- Update to 2.15.1

* Fri May  5 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.1.cvs20060505-2
- Update to a cvs snapshot that supports the new GTK+ filechooser
  backend API
- Require GTK+ 2.9.0

* Tue Apr 11 2006 Matthias Clasen <mclasen@redhat.com> - 2.14.1-2
- Update to 2.14.1

* Mon Mar 13 2006 Matthias Clasen <mclasen@redhat.com> - 2.14.0-1
- Update to 2.14.0

* Mon Feb 27 2006 Matthias Clasen <mclasen@redhat.com> - 2.13.90-1
- Update to 2.13.90

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.13.3-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.13.3-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Thu Jan 26 2006 Matthias Clasen <mclasen@redhat.com>
- Update to 2.13.3

* Mon Jan 16 2006 Matthias Clasen <mclasen@redhat.com>
- Update to 2.13.2

* Wed Dec 14 2005 Matthias Clasen <mclasen@redhat.com>
- Update to 2.13.0

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Nov 28 2005 Ray Strode <rstrode@redhat.com> - 2.12.0-6
- Add libSM-devel/libICE-devel requires for libgnomeui-devel 
  (bug 173610)

* Tue Nov  8 2005 Matthias Clasen <mclasen@redhat.com> - 2.12.0-5
- Remove static libs

* Sun Nov  6 2005 Matthias Clasen <mclasen@redhat.com> - 2.12.0-4
- Switch requires to modular X

* Mon Sep 12 2005 Jeremy Katz <katzj@redhat.com> - 2.12.0-2
- devel subpackage requires gnome-keyring-devel (noticed by Marc Maurer)

* Thu Sep  8 2005 Matthias Clasen <mclasen@redhat.com> - 2.12.0-1
- Update to 2.12.0

* Tue Aug 16 2005 Warren Togami <wtogami@redhat.com> - 2.11.2-2
- rebuild for new cairo

* Tue Aug 9 2005 Ray Strode <rstrode@redhat.com> - 2.11.2-1
- Newer upstream version

* Mon Jul 11 2005 Matthias Clasen <mclasen@redhat.com> - 2.11.1-1
- Newer upstream version

* Fri Apr 8 2005 Ray Strode <rstrode@redhat.com> - 2.10.0-1
- Update to 2.10.0

-* Thu Jan 27 2005 Matthias Clasen <mclasen@redhat.com> - 2.9.1-1
- Update to 2.9.1
- Drop upstreamed patches

* Wed Sep 22 2004 Alexander Larsson <alexl@redhat.com> - 2.8.0-1
- update to 2.8.0

* Fri Sep 17 2004 Matthias Clasen <mclasen@redhat.com> 2.7.92-2
- make the gnome-vfs file chooser backend work better with ftp:

* Tue Aug 31 2004 Alex Larsson <alexl@redhat.com> 2.7.92-1
- update to 2.7.92

* Wed Aug  4 2004 Mark McLoughlin <markmc@redhat.com> 2.7.2-1
- Update to 2.7.2
- Remove patches - all upstream now.

* Tue Jul 27 2004 Colin Walters <walters@redhat.com> 2.6.0-6
- Revert unneeded dep on newer gtk

* Thu Jul 22 2004 Colin Walters <walters@redhat.com> 2.6.0-5
- Backport fileselector crash fix from HEAD
- Remove unneeded calls to autotools
- Remove BR on autotools

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Apr 16 2004 Alexander Larsson <alexl@redhat.com> 2.6.0-3
- Backport fixes from cvs
-  fix fileselector crashes
-  fix auth callback threadsafeness
-  fix auth callback modal dialog bug

* Fri Apr  2 2004 Mark McLoughlin <markmc@redhat.com> 2.6.0-2
- Require libjpeg and BuildRequire libjpeg-devel for the thumbnailer (#111111)

* Thu Apr  1 2004 Alex Larsson <alexl@redhat.com> 2.6.0-1
- update to 2.6.0

* Wed Mar 17 2004 Alex Larsson <alexl@redhat.com> 2.5.92-1
- update to 2.5.92

* Thu Mar 11 2004 Alex Larsson <alexl@redhat.com> 2.5.91-2
- enable gtk-doc

* Wed Mar 10 2004 Mark McLoughlin <markmc@redhat.com> 2.5.91-1
- Update to 2.5.91

* Thu Mar 04 2004 Mark McLoughlin <markmc@redhat.com> 2.5.90.1-1
- Update to 2.5.90.1
- Package the gnome-vfs GtkFilesystem impl.

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Feb 24 2004 Alexander Larsson <alexl@redhat.com> 2.5.90-1
- update to 2.5.90

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Jan 26 2004 Alexander Larsson <alexl@redhat.com> 2.5.3-2
- require later gnome-vfs2

* Fri Jan 23 2004 Jonathan Blandford <jrb@redhat.com> 2.5.3-1
- update to new version

* Fri Oct  3 2003 Alexander Larsson <alexl@redhat.com> 2.4.0.1-1
- 2.4.0.1

* Wed Sep  3 2003 Alexander Larsson <alexl@redhat.com> 2.4.0-1
- update to 2.4.0

* Wed Aug 13 2003 Alexander Larsson <alexl@redhat.com> 2.3.6-2
- Remove bonobo-activation dependencies

* Tue Aug 12 2003 Jonathan Blandford <jrb@redhat.com>
- new release for GNOME 2.4

* Mon Jul 28 2003 Havoc Pennington <hp@redhat.com> 2.2.1-3
- rebuild, and libtoolize

* Wed Jul 23 2003 Nalin Dahyabhai <nalin@redhat.com> 2.2.1-2
- remove apparently-unused source file for rebuild

* Mon Jul  7 2003 Havoc Pennington <hp@redhat.com> 2.2.1-1
- 2.2.1

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun  3 2003 Jeff Johnson <jbj@redhat.com>
- add explicit epoch's where needed, hide epoch in esound_version.

* Thu Feb 13 2003 Tim Powers <timp@redhat.com> 2.2.0.1-5
- fixed requires so that we no longer require Xft and Xft-devel, but
  instead XFree86 and XFree86-devel >= 4.2.99

* Tue Feb 11 2003 Alexander Larsson <alexl@redhat.com> 2.2.0.1-4
- Passs LIBTOOL=/usr/bin/libtool to make, should fix lib64 issue

* Tue Feb 11 2003 Bill Nottingham <notting@redhat.com> 2.2.0.1-3
- fix esound req (#74566)

* Fri Jan 31 2003 Alexander Larsson <alexl@redhat.com> 2.2.0.1-2
- Add patch to enable top-left text

* Thu Jan 23 2003 Alexander Larsson <alexl@redhat.com> 2.2.0.1-1
- Update to 2.2.0.1
- removed icon scale patch. Other patch is in upstream.

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Mon Jan 13 2003 Havoc Pennington <hp@redhat.com>
- copy kdelibs by not scaling icons up more than 6 pixels. needs
  syncing with icon theme spec

* Sun Jan 12 2003 Havoc Pennington <hp@redhat.com>
- rebuild with newer requirements

* Thu Jan  9 2003 Alexander Larsson <alexl@redhat.com> 2.1.90-1
- Update to 2.1.90

* Mon Nov 11 2002 Havoc Pennington <hp@redhat.com>
- 2.1.2
- comment out change-esound-startup patch, not sure about it, doesn't
  apply anymore

* Tue Nov  5 2002 Bill Nottingham <notting@redhat.com> 2.0.3-4
- rebuild for fixed pkgconfig paths

* Thu Aug 29 2002 Havoc Pennington <hp@redhat.com>
- require new libtool and libtoolize to fix rpath bugs

* Wed Aug 21 2002 Elliot Lee <sopwith@redhat.com> 2.0.3-2
- Don't always ensure an esd connection is available just because we
  can do so.

* Mon Aug 12 2002 Havoc Pennington <hp@redhat.com>
- 2.0.3
- fixups to file list and not-packaged files warnings

* Wed Jun 26 2002 Owen Taylor <otaylor@redhat.com>
- Fix find_lang

* Sun Jun 16 2002 Havoc Pennington <hp@redhat.com>
- 2.0.1

* Fri Jun 07 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment

* Wed Jun  5 2002 Havoc Pennington <hp@redhat.com>
- 1.117.2
- remove zero-length AUTHORS/README
- add post/postun ldconfig

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon May 20 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment

* Mon May 20 2002 Havoc Pennington <hp@redhat.com>
- 1.117.1

* Fri May 03 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment

* Fri May  3 2002 Havoc Pennington <hp@redhat.com>
- 1.116.1

* Thu Apr  4 2002 Jeremy Katz <katzj@redhat.com>
- 1.114.0

* Thu Feb 14 2002 Havoc Pennington <hp@redhat.com>
- 1.111.1

* Wed Jan 30 2002 Owen Taylor <otaylor@redhat.com>
- Version 1.110.0

* Mon Jan 28 2002 Havoc Pennington <hp@redhat.com>
- rebuild in rawhide
- --disable-gtk-doc

* Mon Jan  7 2002 Havoc Pennington <hp@redhat.com>
- 1.108.0.90 snap, remove gconf stuff moved to libgnome

* Tue Nov 27 2001 Havoc Pennington <hp@redhat.com>
- 1.106.0.90 snap, glib 1.3.11
- add explicit-versioned requires on dependency libs
- do gconftool stuff, put schemas in file list
- use makeinstall instead of destdir to avoid broken makefiles

* Mon Oct 29 2001 Havoc Pennington <hp@redhat.com>
- grumble, we require libglade 2 not libglade 1

* Mon Oct 29 2001 Havoc Pennington <hp@redhat.com>
- add libglade module to file list
- add libglade dependency

* Sun Oct 28 2001 Havoc Pennington <hp@redhat.com>
- new snap, rebuild for glib 1.3.10

* Fri Oct  5 2001 Havoc Pennington <hp@redhat.com>
- new tarball, rebuild for new glib, remove db1 dependency

* Mon Sep 24 2001 Havoc Pennington <hp@redhat.com>
- new cvs snap

* Tue Sep 18 2001 Havoc Pennington <hp@redhat.com>
- Initial build.


