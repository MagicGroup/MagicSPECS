%define libxml2_version 2.5
%define orbit2_version 2.5.1
%define libbonobo_version 2.13.0
%define libgnomecanvas_version 2.0.1
%define libgnome_version 2.13.7
%define libart_lgpl_version 2.3.8
%define gtk2_version 2.6.0
%define libglade2_version 2.0.0
%define glib2_version 2.6.0

%define po_package libbonoboui-2.0

Summary: Bonobo user interface components
Name: libbonoboui
Version: 2.24.5
Release: 7%{?dist}
URL: http://www.gnome.org
#VCS: git:git://git.gnome.org/libbonoboui
Source0: http://download.gnome.org/sources/libbonoboui/2.24/%{name}-%{version}.tar.bz2
License: LGPLv2+
Group: System Environment/Libraries

Requires: ORBit2 >= %{orbit2_version}

BuildRequires: libxml2-devel >= %{libxml2_version}
BuildRequires: ORBit2-devel >= %{orbit2_version}
BuildRequires: libbonobo-devel >= %{libbonobo_version}
BuildRequires: libgnomecanvas-devel >= %{libgnomecanvas_version}
BuildRequires: libgnome-devel >= %{libgnome_version}
BuildRequires: libart_lgpl-devel >= %{libart_lgpl_version}
BuildRequires: gtk2-devel >= %{gtk2_version}
BuildRequires: libglade2-devel >= %{libglade2_version}
BuildRequires: intltool >= 0.14-1
BuildRequires: libtool >= 1.4.2-12
BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: gettext

%description

Bonobo is a component system based on CORBA, used by the GNOME
desktop. libbonoboui contains the user interface related components
that come with Bonobo.

%package devel
Summary: Libraries and headers for libbonoboui
Group: Development/Libraries
License: GPLv2+ and LGPLv2+
# bonobo-browser is GPL, libbonoboui is LGPL
Requires: %name = %{version}-%{release}
Requires: libxml2-devel >= %{libxml2_version}
Requires: ORBit2-devel >= %{orbit2_version}
Requires: libbonobo-devel >= %{libbonobo_version}
Requires: libgnomecanvas-devel >= %{libgnomecanvas_version}
Requires: libgnome-devel >= %{libgnome_version}
Requires: libart_lgpl-devel >= %{libart_lgpl_version}
Requires: gtk2-devel >= %{gtk2_version}
Requires: libglade2-devel >= %{libglade2_version}
Requires: glib2-devel >= %{glib2_version}
Requires: pkgconfig
Conflicts: bonobo-devel < 1.0.8

%description devel

Bonobo is a component system based on CORBA, used by the GNOME desktop.
libbonoboui contains GUI components that come with Bonobo.

This package contains header files used to compile programs that
use libbonoboui.

%prep
%setup -q -n %{name}-%{version}

%build

%configure --disable-gtk-doc --disable-static
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/libglade/2.0/*.la
rm -f $RPM_BUILD_ROOT%{_datadir}/applications/bonobo-browser.desktop

for serverfile in $RPM_BUILD_ROOT%{_libdir}/bonobo/servers/*.server; do
    sed -i -e 's|location *= *"/usr/lib\(64\)*/|location="/usr/$LIB/|' $serverfile
done


%find_lang %{po_package}

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{po_package}.lang
%defattr(-,root,root)
%doc COPYING.LIB NEWS README
%{_libdir}/lib*.so.*
%{_libdir}/libglade/2.0/*.so
%{_libdir}/bonobo/servers/*
%{_datadir}/gnome-2.0

%files devel
%defattr(-,root,root)
%doc COPYING COPYING.LIB
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{_bindir}/*
%{_libdir}/bonobo-2.0
%{_datadir}/gtk-doc/html/libbonoboui

%changelog
* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 2.24.5-7
- 为 Magic 3.0 重建

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.24.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.24.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.24.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.24.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 2.24.5-2
- Rebuild for new libpng

* Mon Apr  4 2011 Tomas Bzatek <tbzatek@redhat.com> - 2.24.5-1
- Update to 2.24.5

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.24.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 29 2010 Matthias Clasen <mclasen@redhat.com> - 2.24.4-1
- Update to 2.24.4

* Tue Mar 30 2010 Matthias Clasen <mclasen@redhat.com> - 2.24.3-1
- Update to 2.24.3

* Wed Sep 23 2009 Matthias Clasen <mclasen@redhat.com> - 2.24.2-1
- Update to 2.24.2

* Thu Jul 30 2009 Matthias Clasen <mclasen@redhat.com> - 2.24.1-2
-  Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.24.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Mar 16 2009 Matthias Clasen <mclasen@redhat.com> - 2.24.1-1
- Update to 2.24.1

* Fri Feb 27 2009 Ray Strode <rstrode@redhat.com> - 2.24.0-2
- Remove some libtool fu

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.24.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Sep 22 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.0-1
- Update to 2.24.0

* Tue Aug  5 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.5-1
- Update to 2.23.5

* Tue Jun 17 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.4-1
- Update to 2.23.4

* Mon Mar 10 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.0-1
- Update to 2.22.0-1

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.21.90-2
- Autorebuild for GCC 4.3

* Tue Jan 29 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.90-1
- Update to 2.21.90

* Mon Sep 17 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.0-1
- Update to 2.20.0

* Sat Sep  8 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.6-4
- Display a dialog if help cannot be found

* Thu Aug 23 2007 Adam Jackson <ajax@redhat.com> - 2.19.6-3
- Rebuild for ppc toolchain bug

* Tue Aug  7 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.6-2
- Update license field

* Mon Jul 30 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.6-1
- Update to 2.19.6

* Sat Jul  7 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.4-2
- Fix directory ownership

* Tue Jun 19 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.4-1
- Update to 2.19.4

* Tue Mar 13 2007 Matthias Clasen <mclasen@redhat.com> - 2.18.0-1
- Update to 2.18.0

* Tue Feb 27 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.94-1
- Update to 2.17.94

* Tue Feb 27 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.92-1
- Update to 2.17.92

* Tue Feb 13 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.91-1
- Update to 2.17.91

* Wed Jan 22 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.90-1
- Update to 2.17.90

* Wed Jan 10 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.0-1
- Update to 2.17.0

* Mon Sep  4 2006 Matthias Clasen <mclasen@redhat.com> - 2.16.0-1.fc6
- Update to 2.16.0

* Fri Sep  1 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.1-1.fc6
- Update to 2.15.1
- Require pkgconfig in the -devel package

* Sat Aug 12 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.0-1.fc6
- Update to 2.15.0
- Don't ship static libraries and .la files

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.14.0-3.1
- rebuild

* Sat Jun 10 2006 Matthias Clasen <mclasen@redhat.com> 2.14.0-3
- More missing BuildRequires

* Sat May 21 2006 Matthias Clasen <mclasen@redhat.com> 2.14.0-2
- Add missing BuildRequires (#129104)

* Tue Mar 14 2006 Ray Strode <rstrode@redhat.com> 2.14.0-1
- Update to 2.14.0

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.13.1-4.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.13.1-4.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Thu Jan 19 2006 Ray Strode <rstrode@redhat.com> 2.13.1-4
- change sed -ie to sed -i -e

* Thu Jan 19 2006 Ray Strode <rstrode@redhat.com>
- s/$(LIB)/$LIB/g

* Thu Jan 19 2006 Ray Strode <rstrode@redhat.com>
- fix shlib multilib bonobo issue (bug 156982)

* Mon Jan 16 2006 Matthias Clasen <mclasen@redhat.com>
- Update to 2.13.1

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Dec  1 2005 Matthias Clasen <mclasen@redhat.com> - 2.13.0-1
- Update to 2.13.0

* Thu Sep  8 2005 Matthias Clasen <mclasen@redhat.com> - 2.10.1-1
- Update to 2.10.1

* Tue Aug 16 2005 Warren Togami <wtogami@redhat.com> - 2.10.0-2
- rebuild for new cairo

* Fri Aug  5 2005 Matthias Clasen <mclasen@redhat.com> 2.10.0-1
- New upstream version

* Wed Apr 27 2005 Ray Strode <rstrode@redhat.com> 2.8.1-4
- Add fixed tamil translation (bug 135354).

* Fri Apr 15 2005 Ray Strode <rstrode@redhat.com> 2.8.1-3
- Remove bonobo-browser from menus (bug 154827).

* Wed Mar 09 2005 Than Ngo <than@redhat.com> 2.8.1-2
- add OnlyShowIn=GNOME;

* Wed Feb  9 2005 Matthias Clasen <mclasen@redhat.com> - 2.8.1-1
- Update to 2.8.1

* Wed Sep 29 2004 Matthias Clasen <mclasen@redhat.com> - 2.8.0.99cvs20040929-2
- add libtoolize to make it build

* Wed Sep 29 2004 Matthias Clasen <mclasen@redhat.com> - 2.8.0.99cvs20040929-1
- fix a few issues after the merge from Monday. 

* Mon Sep 27 2004 Matthias Clasen <mclasen@redhat.com> - 2.8.0.99cvs20040927-1
- incorporate the fix for #132988

* Wed Sep 22 2004 Alexander Larsson <alexl@redhat.com> - 2.8.0-1
- update to 2.8.0

* Wed Aug  4 2004 Mark McLoughlin <markmc@redhat.com> 2.6.1-1
- Update to 2.6.1

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Apr  1 2004 Alex Larsson <alexl@redhat.com> 2.6.0-1
- update to 2.6.0

* Thu Mar 11 2004 Alex Larsson <alexl@redhat.com> 2.5.4-2
- enable gtk-doc

* Wed Mar 10 2004 Mark McLoughlin <markmc@redhat.com> 2.5.4-1
- Update to 2.5.4

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Feb 24 2004 Mark McLoughlin <markmc@redhat.com> 2.5.3-1
- Update to 2.5.3
- Remove unused bonoboui-fixed-ltmain.sh

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jan 20 2004 Alexander Larsson <alexl@redhat.com> 2.5.2-1
- update to 2.5.2

* Wed Jan 14 2004 Jeremy Katz <katzj@redhat.com> 2.4.3-1
- update to 2.4.3

* Wed Sep  3 2003 Alexander Larsson <alexl@redhat.com> 2.4.0-1
- Update to 2.4.0

* Tue Aug 12 2003 Alexander Larsson <alexl@redhat.com> 2.3.6-2
- update for gnome 2.3

* Wed Jul 23 2003 Havoc Pennington <hp@redhat.com> 2.2.2-2
- remove LIBTOOL=/usr/bin/libtool
- automated rebuild

* Wed Jul  9 2003 Havoc Pennington <hp@redhat.com> 2.2.2-1
- 2.2.2

* Thu Jun 26 2003 Havoc Pennington <hp@redhat.com> 2.2.0-3
- rebuild

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Feb  5 2003 Alexander Larsson <alexl@redhat.com> 2.2.0-1
- 2.2.0

* Tue Jan 28 2003 Matt Wilson <msw@redhat.com> 2.1.2-3
- use LIBTOOL=/usr/bin/libtool

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Sun Jan 12 2003 Havoc Pennington <hp@redhat.com>
- 2.1.2

* Mon Dec  2 2002 Havoc Pennington <hp@redhat.com>
- 2.1.1
- remove lib64 hackaround, upstream looks fixed

* Mon Nov 11 2002 Havoc Pennington <hp@redhat.com>
- 2.1.0
- force-move some stuff from prefix/lib to libdir

* Thu Aug 29 2002 Havoc Pennington <hp@redhat.com>
- libtoolize with our latest libtool to try fixing rpaths

* Mon Aug 12 2002 Havoc Pennington <hp@redhat.com>
- 2.0.1

* Wed Jun 26 2002 Owen Taylor <otaylor@redhat.com>
- Fix find_lang

* Sun Jun 16 2002 Havoc Pennington <hp@redhat.com>
- 2.0.0
- include sample server in libdir
- remove .a files from glade module dir

* Fri Jun 07 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment

* Wed Jun  5 2002 Havoc Pennington <hp@redhat.com>
- 1.118.0
- remove empty AUTHORS file

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon May 20 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment

* Mon May 20 2002 Havoc Pennington <hp@redhat.com>
- 1.117.0

* Fri May  3 2002 Havoc Pennington <hp@redhat.com>
- 1.116.0

* Thu Apr  4 2002 Jeremy Katz <katzj@redhat.com>
- 1.113.0

* Thu Feb 14 2002 Havoc Pennington <hp@redhat.com>
- 1.111.0

* Wed Jan 30 2002 Owen Taylor <otaylor@redhat.com>
- Version 1.110.0
- Reintoolize to fix DBM problems

* Mon Jan 28 2002 Havoc Pennington <hp@redhat.com>
- rebuild in rawhide

* Mon Jan  7 2002 Havoc Pennington <hp@redhat.com>
- 1.108.1.90 cvs snap

* Tue Nov 27 2001 Havoc Pennington <hp@redhat.com>
- 1.107.0.90 snap, explicit requires lines for dependencies
- add libtool hack to avoid relinking

* Mon Oct 29 2001 Havoc Pennington <hp@redhat.com>
- add glade dependency, add glade module to file list

* Sun Oct 28 2001 Havoc Pennington <hp@redhat.com>
- rebuild with glib 1.3.10, new cvs snap

* Mon Oct 15 2001 Havoc Pennington <hp@redhat.com>
- rebuild, hoping build root is fixed

* Mon Oct 15 2001 Havoc Pennington <hp@redhat.com>
- grumble, build require newer gtk
- require libart_lgpl-devel not the non-devel package

* Mon Oct 15 2001 Havoc Pennington <hp@redhat.com>
- cvs snap with menu stuff fixed so gnome-terminal works

* Fri Oct  5 2001 Havoc Pennington <hp@redhat.com>
- new tarball, rebuild for new glib

* Mon Sep 24 2001 Havoc Pennington <hp@redhat.com>
- new cvs snap, fix up prereqs/requires a bit

* Tue Sep 18 2001 Havoc Pennington <hp@redhat.com>
- Initial build.
