Summary:        GNOME User Documentation
Name:           gnome-user-docs
Version:        3.8.0
Release:        1%{?dist}
License:        GFDL
#VCS: git:git://git.gnome.org/gnome-user-docs
Source:         http://download.gnome.org/sources/gnome-user-docs/3.6/gnome-user-docs-%{version}.tar.xz
Group:          Documentation
BuildArch:      noarch

BuildRequires: pkgconfig
BuildRequires: gettext
BuildRequires: itstool
BuildRequires: yelp-tools

%description
This package contains end user documentation for the GNOME desktop
environment.

%prep
%setup -q -n gnome-user-docs-%{version}

%build
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

%find_lang %{name} --all-name --with-gnome

%files -f %{name}.lang
%doc COPYING AUTHORS NEWS README

%changelog
* Tue Mar 26 2013 Kalev Lember <kalevlember@gmail.com> - 3.8.0-1
- Update to 3.8.0

* Tue Feb 19 2013 Richard Hughes <rhughes@redhat.com> - 3.7.90-1
- Update to 3.7.90

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 12 2012 Kalev Lember <kalevlember@gmail.com> - 3.6.2-1
- Update to 3.6.2

* Tue Oct 16 2012 Kalev Lember <kalevlember@gmail.com> - 3.6.1-1
- Update to 3.6.1
- Use find_lang macro instead of manually listing all the translated docs

* Tue Sep 25 2012 Matthias Clasen <mclasen@redhat.com> - 3.6.0-1
- Update to 3.6.0

* Wed Sep 19 2012 Tomas Bzatek <tbzatek@redhat.com> - 3.5.92-1
- Update to 3.5.92

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 07 2012 Richard Hughes <hughsient@gmail.com> - 3.4.2-1
- Update to 3.4.2

* Tue Apr 17 2012 Kalev Lember <kalevlember@gmail.com> - 3.4.1-1
- Update to 3.4.1

* Wed Mar 27 2012 Richard Hughes <hughsient@gmail.com> - 3.4.0-2
- Fix the spec file to include all the languages

* Tue Mar 27 2012 Richard Hughes <hughsient@gmail.com> - 3.4.0-1
- Update to 3.4.0

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Nov 24 2011 Tomas Bzatek <tbzatek@redhat.com> - 3.2.2-1
- Update to 3.2.2

* Tue Oct 18 2011 Matthias Clasen <mclasen@redhat.com> - 3.2.1-1
- Update to 3.2.1

* Wed Sep 28 2011 Ray <rstrode@redhat.com> - 3.2.0.1-1
- Update to 3.2.0.1

* Tue Sep 27 2011 Ray <rstrode@redhat.com> - 3.2.0-1
- Update to 3.2.0

* Tue Sep  6 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.1-1
- Update to 3.1.1

* Tue May 24 2011 Christopher Aillon <caillon@redhat.com> - 3.0.4-1
- Update to 3.0.4

* Mon Apr 25 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.3-1
- Update to 3.0.3

* Mon Apr 18 2011 Christopher Aillon <caillon@redhat.com> - 3.0.2-1
- Update to 3.0.2

* Sun Apr 10 2011 Christopher Aillon <caillon@redhat.com> - 3.0.1-1
- Update to 3.0.1

* Tue Apr  5 2011 Christopher Aillon <caillon@redhat.com> - 3.0.0-1
- Update to 3.0.0

* Tue Mar 22 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.92-1
- Update to 2.91.92

* Mon Mar  7 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.91-1
- Update to 2.91.91

* Tue Feb 22 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.90-1
- Update to 2.91.90

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.32.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Sep 28 2010 Matthias Clasen <mclasen@redhat.com> - 2.32.0-1
- Update to 2.32.0

* Thu Sep 09 2010 Parag Nemade <paragn AT fedoraproject.org> 2.30.1-2
- Merge-review cleanup (#225841)

* Mon Apr 26 2010 Matthias Clasen <mclasen@redhat.com> - 2.30.1-1
- Update to 2.30.1

* Mon Mar 29 2010 Matthias Clasen <mclasen@redhat.com> - 2.30.0-1
- Update to 2.30.0

* Wed Feb 10 2010 Bastien Nocera <bnocera@redhat.com> 2.29.2-1
- Update to 2.29.2

* Tue Jan 26 2010 Matthias Clasen <mclasen@redhat.com> - 2.29.1-1
- Update to 2.29.1

* Mon Sep 21 2009 Matthias Clasen <mclasen@redhat.com> - 2.28.0-1
- Update to 2.28.0

* Mon Sep  7 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.2-1
- Update to 2.27.2

* Mon Aug 24 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.1-1
- Update to 2.27.1

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.26.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Apr 14 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.1-1
- Update to 2.26.1

* Mon Mar 16 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.0-1
- Update to 2.26.0

* Mon Mar  2 2009 Matthias Clasen <mclasen@redhat.com> - 2.25.1-1
- Update to 2.25.1

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.24.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Dec 17 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.1-1
- Update to 2.24.1

* Mon Sep 22 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.0-1
- Update to 2.24.0

* Wed Jul 23 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.22.0-2
- fix license tag

* Mon Mar 10 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.0-1
- Update to 2.22.0

* Fri Oct 12 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.1-1
- Update to 2.20.1 (Accessibility guide updates and updated translations)

* Mon Sep 17 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.0-1
- Update to 2.20.0

* Tue Aug  7 2007 Matthias Clasen <mclasen@redhat.com> - 2.18.2-2
- Update the license field
- Use %%find_lang

* Mon Jul  2 2007 Matthias Clasen <mclasen@redhat.com> - 2.18.2-1
- Update to 2.18.2

* Tue Mar 13 2007 Matthias Clasen <mclasen@redhat.com> - 2.18.0-1
- Update to 2.18.0

* Sat Oct 21 2006 Matthias Clasen <mclasen@redhat.com> - 2.16.1-1
- Update to 2.16.1

* Fri Sep  8 2006 Matthias Clasen <mclasen@redhat.com> - 2.16.0-2
- Fix directory ownership issues

* Tue Sep  5 2006 Matthias Clasen <mclasen@redhat.com> - 2.16.0-1.fc6
- Update to 2.16.0

* Sun Aug 13 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.1-1.fc6
- Update to 2.15.1

* Fri Jun  9 2006 Matthias Clasen <mclasen@redhat.com> 2.14.2-4
- Add more BuildRequires

* Mon Jun  5 2006 Matthias Clasen <mclasen@redhat.com> 2.14.2-3
- Fix BuildRequires

* Tue Apr 11 2006 Matthias Clasen <mclasen@redhat.com> 2.14.2-2
- Update to 2.14.2

* Mon Apr 10 2006 Matthias Clasen <mclasen@redhat.com> 2.14.1-2
- Update to 2.14.1

* Mon Mar 13 2006 Matthias Clasen <mclasen@redhat.com> 2.14.0-1
- Update to 2.14.0

* Wed Mar 8 2006 Ray Strode <rstrode@redhat.com> 2.13.1.1-2
- PreReq instead of Requires scrollkeeper.  Reported by
  Bill Nottingham

* Tue Feb 21 2006 Matthias Clasen <mclasen@redhat.com> 2.13.1.1-1
- Update to 2.13.1.1

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Sat Nov  6 2004 Marco Pesenti Gritti <mpg@redhat.com> 2.8.1-2
- Remove the section about menu editing. Fix 134119

* Mon Oct 25 2004 Christopher Aillon <caillon@redhat.com> 2.8.1-1
- Update to 2.8.1

* Wed Sep 22 2004 Christopher Aillon <caillon@redhat.com> 2.8.0.1-1
- Update to 2.8.0-1

* Tue Apr 13 2004 Warren Togami <wtogami@redhat.com> 2.6.0.1-2
- BR scrollkeeper

* Fri Apr  2 2004 Mark McLoughlin <markmc@redhat.com> 2.6.0.1-1
- Update to 2.6.0.1

* Mon Mar 15 2004 Alex Larsson <alexl@redhat.com> 2.5.90-1
- update to 2.5.90

* Thu Feb 26 2004 Alexander Larsson <alexl@redhat.com> 2.5.0-1
- update to 2.5.0

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Jan 30 2004 Alexander Larsson <alexl@redhat.com> 2.4.1-1
- update to 2.4.1

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Mon Dec 16 2002 Havoc Pennington <hp@redhat.com>
- add introduction-to-gnome.xml from CVS so the XML won't be broken

* Fri Dec 13 2002 Tim Powers <timp@redhat.com> 2.0.1-1
- update to 2.0.1

* Thu Aug  8 2002 Havoc Pennington <hp@redhat.com>
- 2.0.0 stable release
- clean up uninstalled file warnings
- blow build root at start of install

* Mon Jun 24 2002 Owen Taylor <otaylor@redhat.com>
- Version 1.93, should fix #67207

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Jun 20 2002 Havoc Pennington <hp@redhat.com>
- prereq scrollkeeper

* Mon Jun 17 2002 Havoc Pennington <hp@redhat.com>
- upgrade to gnome 2 docs
- clean up the spec file a bit

* Thu Jun 13 2002 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in different environment

* Thu Jun 13 2002 Nalin Dahyabhai <nalin@redhat.com>
- fix a scrollkeeper validation bug

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild


* Tue Apr 17 2001 Jonathan Blandford <jrb@redhat.com>
- Moved to red hat build system

* Thu Feb 22 2001 Gregory Leblanc <gleblanc@cu-portland.edu>
- de-uglification, and fixed the macros.

* Mon Nov 27 2000 Kenny Graunke <kwg@teleport.com>
- Initial cut
