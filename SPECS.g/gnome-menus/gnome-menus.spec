%global enable_debugging 0

Summary:  A menu system for the GNOME project
Summary(zh_CN.UTF-8): GNOME 项目的菜单系统
Name: gnome-menus
Version:	3.13.3
Release: 4%{?dist}
License: LGPLv2+
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL: http://www.gnome.org/

%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
#VCS: git:git://git.gnome.org/gnome-menus
Source0: http://download.gnome.org/sources/gnome-menus/%{majorver}/%{name}-%{version}.tar.xz
Requires:  magic-menus
BuildRequires: gamin-devel
BuildRequires: gawk
BuildRequires: gettext
BuildRequires: glib2-devel
BuildRequires: pkgconfig
BuildRequires: python2-devel
BuildRequires: intltool
BuildRequires: gobject-introspection-devel

%description
gnome-menus is an implementation of the draft "Desktop
Menu Specification" from freedesktop.org. This package
also contains the GNOME menu layout configuration files,
.directory files and assorted menu related utility programs,
Python bindings, and a simple menu editor.

%description -l zh_CN.UTF-8 
GNOME 桌面的菜单系统，实现了 freedesktop.org 的桌面菜单标准的支持。

%package devel
Summary: Libraries and include files for the GNOME menu system
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}

%description devel
This package provides the necessary development libraries for
writing applications that use the GNOME menu system.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q

%build
%configure --disable-static \
   --enable-introspection \
%if %{enable_debugging}
   --enable-debug=yes
%else
   --enable-debug=no
%endif

make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
magic_rpm_clean.sh
%find_lang gnome-menus-3.0

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f gnome-menus-3.0.lang
%doc AUTHORS NEWS COPYING.LIB
%{_sysconfdir}/xdg/menus/gnome-applications.menu
%{_libdir}/lib*.so.*
%{_datadir}/desktop-directories/*
%{_libdir}/girepository-1.0/GMenu-3.0.typelib

%files devel
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*
%{_includedir}/gnome-menus-3.0
%{_datadir}/gir-1.0/GMenu-3.0.gir

%changelog
* Sun Nov 08 2015 Liu Di <liudidi@gmail.com> - 3.13.3-4
- 为 Magic 3.0 重建

* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 3.13.3-3
- 更新到 3.13.3

* Wed Apr 09 2014 Liu Di <liudidi@gmail.com> - 3.10.1-2
- 更新到 3.10.1

* Sat Mar 30 2013 Kalev Lember <kalevlember@gmail.com> - 3.8.0-2
- Fix gnome-calculator to show up in the menus again

* Tue Mar 26 2013 Kalev Lember <kalevlember@gmail.com> - 3.8.0-1
- Update to 3.8.0

* Fri Feb 22 2013 Kalev Lember <kalevlember@gmail.com> - 3.7.90-1
- Update to 3.7.90
- Drop the downstream patch for changing the release notes categories

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan 15 2013 Matthias Clasen <mclasen@redhat.com> - 3.6.2-1
- Update to 3.6.2

* Wed Nov 14 2012 Kalev Lember <kalevlember@gmail.com> - 3.6.1-1
- Update to 3.6.1

* Thu Oct 18 2012 Florian Müllner <fmuellner@redhat.com> - 3.6.0-2
- Use gnome-applications.menu instead of applications-gnome.menu,
  in order to be able to use XDG_MENU_PREFIX instead of a downstream
  patch to gnome-shell

* Tue Sep 25 2012 Matthias Clasen <mclasen@redhat.com> - 3.6.0-1
- Update to 3.6.0

* Wed Sep 19 2012 Richard Hughes <hughsient@gmail.com> - 3.5.92-1
- Update to 3.5.92

* Tue Aug 07 2012 Richard Hughes <hughsient@gmail.com> - 3.5.5-1
- Update to 3.5.5

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 17 2012 Richard Hughes <hughsient@gmail.com> - 3.5.4-1
- Update to 3.5.4

* Tue Jun 26 2012 Matthias Clasen <mclasen@redhat.com> - 3.5.3-1
- Update to 3.5.3

* Thu Jun 07 2012 Richard Hughes <hughsient@gmail.com> - 3.5.2-1
- Update to 3.5.2

* Fri May 18 2012 Richard Hughes <hughsient@gmail.com> - 3.4.2-1
- Update to 3.4.2

* Tue Mar 27 2012 Kalev Lember <kalevlember@gmail.com> - 3.4.0-1
- Update to 3.4.0

* Tue Feb 21 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 3.3.5-2
- Drop the rpath change as it's fixed upstream and the associated circular dep hack

* Tue Feb  7 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.5-1
- Update to 3.3.5

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov  2 2011 Matthias Clasen <mclasen@redhat.com> - 3.3.1-1
- Update to 3.3.1

* Wed Sep 28 2011 Ray <rstrode@redhat.com> - 3.2.0.1-1
- Update to 3.2.0.1

* Tue Sep 27 2011 Ray <rstrode@redhat.com> - 3.2.0-1
- Update to 3.2.0

* Mon Sep 19 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.92-1
- Update to 3.1.92

* Tue Aug 30 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.90-1
- Update to 3.1.90

* Fri Aug 24 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.5-3
- Sync with F16

* Tue Apr 26 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.1-1
- Update to 3.0.1

* Mon Apr 11 2011 Colin Walters <walters@verbum.org> - 3.0.0-2
- Ship applications-gnome.desktop; we don't want GNOME 3 to use redhat-menus.
- Disable introspection, we're not using it right now

* Mon Apr  4 2011 Matthias Clasen <mclasen@redhat.com> 3.0.0-1
- Update to 3.0.0

* Mon Mar  7 2011 Matthias Clasen <mclasen@redhat.com> 2.91.91-1
- Update to 2.91.91

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.30.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 29 2010 Matthias Clasen <mclasen@redhat.com> 2.30.4-1
- Update to 2.30.4

* Wed Sep 29 2010 jkeating - 2.30.0-5
- Rebuilt for gcc bug 634757

* Fri Sep 10 2010 Parag Nemade <paragn AT fedoraproject.org> 2.30.0-4
- Merge-review cleanup (#225823)

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 2.30.0-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Apr  7 2010 Matthias Clasen <mclasen@redhat.com> 2.30.0-2
- Keep release notes out of Applications>Other

* Mon Mar 29 2010 Matthias Clasen <mclasen@redhat.com> 2.30.0-1
- Update to 2.30.0

* Tue Mar 09 2010 Bastien Nocera <bnocera@redhat.com> 2.29.92-1
- Update to 2.29.92

* Mon Feb 22 2010 Matthias Clasen <mclasen@redhat.com> 2.29.91-1
- Update to 2.29.91

* Thu Feb 11 2010 Matthias Clasen <mclasen@redhat.com> 2.29.6-1
- Update to 2.29.6

* Thu Sep 24 2009 Matthias Clasen <mclasen@redhat.com> 2.28.0-2
- Remove obsolete configure option

* Mon Sep 21 2009 Matthias Clasen <mclasen@redhat.com> 2.28.0-1
- Update to 2.28.0

* Wed Sep  9 2009 Matthias Clasen <mclasen@redhat.com> 2.27.92-1
- Update to 2.27.92

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.27.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 15 2009 Matthias Clasen <mclasen@redhat.com> 2.27.4-1
- Update to 2.27.4

* Tue Jun 30 2009 Matthias Clasen <mclasen@redhat.com> 2.26.2-1
- Update to 2.26.2
- See http://download.gnome.org/sources/gnome-menus/2.26/gnome-menus-2.26.2.news

* Sun Jun 14 2009 Matthias Clasen <mclasen@redhat.com> 2.26.1-2
- Minor directory ownership cleanup

* Mon Apr 13 2009 Matthias Clasen <mclasen@redhat.com> 2.26.1-1
- Update to 2.26.1
- See http://download.gnome.org/sources/gnome-menus/2.26/gnome-menus-2.26.1.news

* Mon Mar 16 2009 Matthias Clasen <mclasen@redhat.com> 2.26.0-1
- Update to 2.26.0

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.25.91-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 17 2009 Matthias Clasen <mclasen@redhat.com> 2.25.91-1
- Update to 2.25.91

* Tue Jan 20 2009 Matthias Clasen <mclasen@redhat.com> 2.25.5-1
- Update to 2.25.5

* Thu Dec  4 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.25.2-3
- Rebuild for Python 2.6

* Wed Dec  3 2008 Matthias Clasen <mclasen@redhat.com> 2.25.2-2
- Update to 2.25.2

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.24.1-2
- Rebuild for Python 2.6

* Wed Oct 22 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.1-1
- Update to 2.24.1

* Mon Oct 20 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.0-2
- Fix a translation error in Marathi

* Mon Sep 22 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.0-1
- Update to 2.24.0

* Mon Sep  8 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.92-1
- Update to 2.23.92

* Tue Sep  2 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.91-1
- Update to 2.23.91

* Tue Aug  5 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.6-1
- Update to 2.23.6

* Fri Aug  1 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.5-2
- Use standard icon names

* Tue Jul 22 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.5-1
- Update to 2.23.5

* Wed Jun 18 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.4-1
- Update to 2.23.4

* Wed Jun  4 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.3-1
- Update to 2.23.3

* Fri Apr 25 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.1-1
- Update to 2.23.1

* Mon Apr  7 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.1-1
- Update to 2.22.1

* Mon Mar 10 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.0-1
- Update to 2.22.0

* Tue Feb 26 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.92-1
- Update to 2.21.92

* Tue Feb 12 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.91-1
- Update to 2.21.91

* Tue Jan 29 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.90-1
- Update to 2.21.90

* Mon Jan 14 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.4-1
- Update to 2.21.4

* Wed Jan 09 2008 - Bastien Nocera <bnocera@redhat.com> - 2.21.3-2
- Add upstream patch to allow building with the new GIO file
  monitoring API

* Sat Dec 22 2007 Matthias Clasen <mclasen@redhat.com> - 2.21.3-1
- Update to 2.21.3
- Use gio for file monitoring

* Mon Nov 12 2007 Matthias Clasen <mclasen@redhat.com> - 2.21.2-1
- Update to 2.21.2

* Mon Oct 15 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.1-1
- Update to 2.20.1 (translation updates)

* Mon Sep 17 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.0-1
- Update to 2.20.0

* Tue Sep  4 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.92-1
- Update to 2.19.92

* Thu Aug 23 2007 Adam Jackson <ajax@redhat.com> - 2.19.90-2
- Rebuild for build ID
- BuildRequires: gawk

* Mon Aug 13 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.90-1
- Update to 2.19.90

* Thu Aug  2 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.6-2 
- Update license field

* Mon Jul 30 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.6-1 
- Update to 2.19.6

* Sun Jul  8 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.5-1 
- Update to 2.19.5

* Sun Jun 17 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.4-1 
- Update to 2.19.4
- Drop upstreamed patch

* Thu Jun 14 2007 Colin Walters <walters@redhat.com> - 2.19.3-2
- Add patch gnome-menus-pythread-bgo442747.patch

* Mon Jun  4 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.3-1
- Update to 2.19.3

* Sat May 19 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.2-1
- Update to 2.19.2

* Tue Mar 13 2007 Matthias Clasen <mclasen@redhat.com> - 2.18.0-1
- Update to 2.18.0

* Tue Feb 27 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.92-1
- Update to 2.17.92
- Drop obsolete patch

* Thu Feb 15 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.91-2
- Show the Preferences menu

* Tue Feb 13 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.91-1
- Update to 2.17.91

* Mon Jan 29 2007 Adam Jackson <ajax@redhat.com> - 2.17.5-2
- Fix the redhat-menus Requires: to a version where there's no
  System.directory conflict.

* Wed Jan 10 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.5-1
- Update to 2.17.5 
- Remove traces of gmenu-simple-editor

* Thu Dec  7 2006 Jeremy Katz <katzj@redhat.com> - 2.17.2-2
- rebuild for python 2.5

* Mon Nov  6 2006 Matthias Clasen <mclasen@redhat.com> - 2.17.2-1
- Update to 2.17.2
- Don't ship static libraries
- Fix python packaging

* Sat Oct 21 2006 Matthias Clasen <mclasen@redhat.com> - 2.16.1-1
- Update to 2.16.1

* Tue Sep  5 2006 Ray Strode <rstrode@redhat.com> - 2.16.0-2.fc6
- Remove menu editor (bug 205210)

* Mon Sep  4 2006 Matthias Clasen <mclasen@redhat.com> - 2.16.0-1.fc6
- Update to 2.16.0

* Mon Aug 21 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.91-2.fc6
- Add Requires to the -devel package

* Sat Aug 12 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.91-1.fc6
- Update to 2.15.91

* Thu Aug  2 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.90-1.fc6
- Update to 2.15.90

* Wed Jul 12 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.4.1-1
- Update to 2.15.4.1

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.14.0-4.1
- rebuild

* Fri Jun  9 2006 Matthias Clasen <mclasen@redhat.com> - 2.14.0-4
- More missing BuildRequires

* Tue Jun  6 2006 Matthias Clasen <mclasen@redhat.com> - 2.14.0-3
- Add a BuildRequires for perl-XML-Parser

* Mon Apr 13 2006 Matthias Clasen <mclasen@redhat.com> - 2.14.0-2
- Update to 2.14.0
- Drop upstreamed patch

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.13.5-5.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.13.5-5.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Feb  6 2006 Ray Strode <rstrode@redhat.com> 2.13.5-5
- break infinite loop 

* Wed Feb  1 2006 Ray Strode <rstrode@redhat.com> 2.13.5-4
- don't ship upstream Desktop.directory files

* Fri Jan 27 2006 Ray Strode <rstrode@redhat.com> 2.13.5-3
- ship upstream .directory files

* Thu Jan 19 2006 Matthias Clasen <mclasen@redhat.com> 2.13.5-2
- Add a BuildRequires for gamin

* Tue Jan 17 2006 Matthias Clasen <mclasen@redhat.com> 2.13.5-1
- Update to 2.13.5

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Sep  6 2005 Mark McLoughlin <markmc@redhat.com> 2.12.0-1
- Update to 2.12.0

* Mon Aug 22 2005 Mark McLoughlin <markmc@redhat.com> 2.11.92-1
- Update to 2.11.92

* Thu Aug 18 2005 Mark McLoughlin <markmc@redhat.com> 2.11.91-3
- Fix infinite loop in patch for gnome #313624

* Thu Aug 18 2005 Mark McLoughlin <markmc@redhat.com> 2.11.91-2
- Add patch to fix "duplicate entries after upgrade" issue (gnome #313624)

* Tue Aug 16 2005 Mark McLoughlin <markmc@redhat.com> 2.11.91-1
- Update to 2.11.91
- Backport patch from HEAD to hopefully fix crasher (rh #165977)

* Wed Aug 03 2005 Ray Strode <rstrode@redhat.com> - 2.11.90-1
- Update to upstream version 2.11.90

* Mon Jul 11 2005 Matthias Clasen <mclasen@redhat.com> 2.11.1.1-2
- Undo the split into tiny subpackages, instead move
  the Python bindings and the editor into the main package.
- Fix dependencies

* Fri Jul  8 2005 Matthias Clasen <mclasen@redhat.com> 2.11.1.1-1
- Update to 2.11.1.1
- Split off subpackages for python bindings and editor

* Fri Apr 22 2005 Matthias Clasen <mclasen@redhat.com> 2.10.1-3
- Call ldconfig in %%post (#155734)
- Add some BuildRequires

* Wed Apr  6 2005 Mark McLoughlin <markmc@redhat.com> 2.10.1-2
- Backport patch from CVS to fix large memory leak on re-loading
  the menus (gnome #172472)

* Wed Mar 23 2005 Mark McLoughlin <markmc@redhat.com> 2.10.1-1
- Update to 2.10.1

* Thu Mar 17 2005 Ray Strode <rstrode@redhat.com> - 2.10.0-1
- Update to upstream version 2.10.0

* Fri Mar  4 2005 Jeremy Katz <katzj@redhat.com> - 2.9.90-4
- fix 64bit pointer problem that caused the panel to crash

* Wed Mar  2 2005 Mark McLoughlin <markmc@redhat.com> 2.9.90-3
- Turn off debugging by default
- Rebuild with gcc4

* Tue Feb  1 2005 Matthias Clasen <mclasen@redhat.com> - 2.9.90-2
- Don't include .directory and .menu files,
  we want those from redhat-menus

* Mon Jan 31 2005 Matthias Clasen <mclasen@redhat.com> - 2.9.90-1
- Initial build.

