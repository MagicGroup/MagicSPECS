%global	dbus_ver	0.95
%global	dbus_glib_ver	0.90
%global	glib_ver	2.36.0
%global gobj_ver	1.30
%global vala_ver	0.16.0

Name:           telepathy-glib
Version:        0.24.0
Release:        1%{?dist}
Summary:        GLib bindings for Telepathy

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://telepathy.freedesktop.org/wiki/FrontPage
Source0:        http://telepathy.freedesktop.org/releases/%{name}/%{name}-%{version}.tar.gz

BuildRequires:  gtk-doc >= 1.17
BuildRequires:  dbus-devel >= %{dbus_ver}
BuildRequires:	dbus-glib-devel >= %{dbus_glib_ver}
BuildRequires:	glib2-devel >= %{glib_ver}
BuildRequires:	gobject-introspection-devel >= %{gobj_ver}
BuildRequires:	vala-devel >= %{vala_ver}
BuildRequires:	vala-tools
BuildRequires:	libxslt
BuildRequires:	python

%description
Telepathy-glib is the glib bindings for the telepathy unified framework
for all forms of real time conversations, including instant messaging, IRC, 
voice calls and video calls.


%package vala
Summary:	Vala bindings for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	vala


%description vala
Vala bindings for %{name}.


%package 	devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-vala = %{version}-%{release}
Requires:	telepathy-filesystem
Requires:	dbus-devel >= %{dbus_ver}
Requires:	dbus-glib-devel >= %{dbus_glib_ver}
Requires:	glib2-devel >= %{glib_ver}
Requires:	pkgconfig


%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q


%check
make check


%build
%configure --enable-static=no --enable-introspection=yes --enable-vala-bindings=yes
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%doc AUTHORS COPYING README NEWS
%{_libdir}/libtelepathy-glib*.so.*
%{_libdir}/girepository-1.0/TelepathyGLib-0.12.typelib


%files vala
%{_datadir}/vala/vapi/telepathy-glib.deps
%{_datadir}/vala/vapi/telepathy-glib.vapi


%files devel
%doc %{_datadir}/gtk-doc/html/%{name}/
%{_libdir}/libtelepathy-glib.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/telepathy-1.0/%{name}/
%{_datadir}/gir-1.0/TelepathyGLib-0.12.gir


%changelog
* Thu Mar 27 2014 Brian Pepple <bpepple@fedoraproject.org> - 0.24.0-1
- Update to 0.24.0.

* Tue Mar 18 2014 Brian Pepple <bpepple@fedoraproject.org> - 0.23.3-1
- Update to 0.23.3.

* Wed Mar 05 2014 Richard Hughes <rhughes@redhat.com> - 0.23.2-1
- Update to 0.23.2.

* Thu Feb 20 2014 Adam Williamson <awilliam@redhat.com> - 0.23.1-1
- update to 0.23.1.

* Thu Jan 30 2014 Brian Pepple <bpepple@fedoraproject.org> - 0.22.1-1
- Update to 0.22.1.

* Wed Oct  2 2013 Brian Pepple <bpepple@fedoraproject.org> - 0.22.0-1
- Update to 0.22.0.

* Tue Sep 24 2013 Brian Pepple <bpepple@fedoraproject.org> - 0.21.2-1
- Update to 0.21.2.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.21.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jun 20 2013 Brian Pepple <bpepple@fedoraproject.org> - 0.21.1-1
- Update to 0.21.1.

* Wed Apr  3 2013 Brian Pepple <bpepple@fedoraproject.org> - 0.21.0-1
- Update to 0.21.0.

* Wed Apr  3 2013 Brian Pepple <bpepple@fedoraproject.org> - 0.20.2-1
- Update to 0.20.2.
- Enable tests again.

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov  9 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.20.1-1
- Update to 0.20.1
- Drop call channel patches. Fixed upstream.

* Tue Oct 16 2012 Debarshi Ray <rishi@fedoraproject.org> - 0.20.0-2
- Fix FD #56044

* Wed Oct  3 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.20.0-1
- Update to 0.20.0

* Wed Sep 26 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.19.10-1
- Update to 0.19.10

* Tue Sep 11 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.19.9-1
- Update to 0.19.9.

* Fri Aug 31 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.19.8-1
- Update to 0.19.8.

* Tue Aug 28 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.19.7-1
- Update to 0.19.7.

* Mon Aug  6 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.19.6-1
- Update to 0.19.6.
- Use global macro instead of define macro.

* Tue Jul 24 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.19.5-1
- Update to 0.19.5.

* Thu Jul 19 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.19.4-1
- Update to 0.19.4.

* Thu Jul  5 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.19.3-1
- Update to 0.19.3.

* Thu Jun 28 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.19.2-1
- Update to 0.19.2.

* Wed Jun  6 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.19.1-1
- Update to 0.19.1.
- Bump minimum version of vala.

* Thu May 10 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.19.0-1
- Update to 0.19.0.
- Bump minimum version of glib2.

* Sat Apr 21 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.18.1-1
- Update to 0.18.1.

* Mon Apr  2 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.18.0-1
- Update to 0.18.0.

* Thu Mar 22 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.17.7-1
- Update to 0.17.7.

* Mon Mar 19 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.17.6-1
- Update to 0.17.6.
- Bump minimum version of glib2 and dbus-glib.

* Tue Feb 21 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.17.5-1
- Update to 0.17.5.

* Sun Jan 08 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.17.4-2
- Rebuild for new gcc.

* Mon Dec 19 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.17.4-1
- Update to 0.17.4.

* Mon Nov 28 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.17.3-1
- Update to 0.17.3.

* Wed Nov 23 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.17.2-1
- Update to 0.17.2.
- Bump min version of gtk-doc needed.

* Wed Nov 16 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.17.1-1
- Update to 0.17.1.

* Tue Oct 25 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.16.1-1
- Update to 0.16.1.

* Fri Oct 14 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.16.0-1
- Update to 0.16.0.

* Wed Oct 12 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.15.9-1
- Update to 0.15.9.

* Wed Oct  5 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.15.7-1
- Update to 0.15.7.

* Fri Sep 30 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.15.6-1
- Update to 0.15.6.

* Wed Aug 17 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.15.5-1
- Update to 0.15.5.

* Tue Jul 12 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.15.4-1
- Update to 0.15.4.

* Fri Jul  8 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.15.3-1
- Update to 0.15.3.

* Tue Jun 21 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.15.2-1
- Update to 0.15.2.

* Fri Jun 10 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.15.1-1
- Update to 0.15.1.

* Mon May 30 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.14.7-1
- Update to 0.14.7.

* Tue May 17 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.14.6-1
- Update to 0.14.6.

* Thu Apr 21 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.14.5-1
- Update to 0.14.5.

* Fri Apr 15 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.14.4-1
- Update to 0.14.4.

* Thu Mar 31 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.14.3-1
- Update to 0.14.3.

* Tue Mar 22 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.14.1-1
- Update to 0.14.1.

* Mon Mar 21 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.14.0-1
- Update to 0.14.0.

* Tue Mar 15 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.13.18-1
- Update to 0.13.18.

* Wed Mar  9 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.13.17-1
- Update to 0.13.17.

* Mon Mar  7 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.13.16-1
- Update to 0.13.16.

* Thu Feb 24 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.13.15-1
- Update to 0.13.15.

* Wed Feb 23 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.13.14-1
- Update to 0.13.14.

* Thu Feb 10 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.13.13-1
- Update to 0.13.13.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb  1 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.13.12-1
- Update to 0.13.12.
- Drop test string patch. Fixed upstream.

* Tue Feb  1 2011 Dan Horák <dan[at]danny.cz> - 0.13.11-2
- add upstream fix for failing test

* Thu Jan 27 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.13.11-1
- Update to 0.13.11.

* Thu Jan 13 2011 Matthias Clasen <mclasen@redhat.com> - 0.13.10-2
- Move girs to -devel

* Mon Dec 20 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.13.10-1
- Update to 0.13.10.

* Fri Dec 10 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.13.9-1
- Update to 0.13.9.
- Enable tests.

* Wed Dec  1 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.13.8-1
- Update to 0.13.8.

* Thu Nov 25 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.13.7-1
- Update to 0.13.7.

* Wed Nov 17 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.13.6-1
- Update to 0.13.6.

* Fri Nov  5 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.13.5-1
- Update to 0.13.5.
- Drop provides/obsoletes on libtelepathy.
- Drop buildroot & clean section. No longer needed.

* Wed Nov  3 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.13.4-1
- Update to 0.13.4.

* Tue Oct 26 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.13.3-1
- Update to 0.13.3.

* Fri Oct 15 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.13.2-1
- Update to 0.13.2.
- Drop provide/obsolete on libtelepathy.

* Wed Sep 29 2010 jkeating - 0.12.0-2
- Rebuilt for gcc bug 634757

* Sat Sep 25 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.12.0-1
- Update to 0.12.0.

* Thu Sep 23 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.11.16-1
- Update to 0.11.16.

* Tue Sep 21 2010 Matthias Clasen <mclasen@redhat.com> - 0.11.15-2
- Rebuild against newer gobject-introspection

* Mon Sep 13 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.11.15-1
- Update to 0.11.15.

* Wed Aug 25 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.11.14-1
- Update to 0.11.14.

* Tue Aug 17 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.11.13-1
- Update to 0.11.13.
- Enable vala bindings. (#619137)

* Wed Aug 11 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.11.12-1
- Update to 0.11.12.

* Mon Jul 26 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.11.11-1
- Update to 0.11.11.

* Mon Jul 12 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.11.10-1
- Update to 0.11.10.

* Tue Jun 22 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.11.8-1
- Update to 0.11.8.
- Enable gobject introspection.
- Bump min version of glib required.

* Mon Jun 14 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.11.7-1
- Update to 0.11.7.

* Mon Jun  7 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.11.6-1
- Update to 0.11.6.

* Mon May 31 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.11.5-2
- Enable checks.

* Mon May 10 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.11.5-1
- Update to 0.11.5.

* Wed Apr 28 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.10.5-1
- Update to 0.10.5.

* Tue Apr 20 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.10.4-1
- Update to 0.10.4.

* Mon Apr 19 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.10.3-3
- Obsolete the devel subpackage as well.

* Thu Apr 15 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.10.3-2
- Add missing Obsoletes on libtelepathy.

* Tue Apr  6 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.10.3-1
- Update to 0.10.3.

* Wed Mar 31 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.10.2-1
- Update to 0.10.2.

* Wed Mar 24 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.10.1-1
- Update to 0.10.1.

* Thu Jan 21 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.10.0-1
- Update to 0.10.0.

* Thu Dec  3 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.9.2-1
- Update to 0.9.2.

* Thu Oct 15 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.9.1-1
- Update to 0.9.1.

* Mon Sep 28 2009 Bastien Nocera <bnocera@redhat.com> 0.9.0-1
- Update to 0.9.0

* Thu Sep 24 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.8.0-1
- Update to 0.8.0.

* Mon Sep 14 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.7.37-1
- Update to 0.7.37.

* Thu Sep  3 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.7.36-1
- Update to 0.7.36.

* Tue Aug 18 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.7.35-1
- Update to 0.7.35.

* Mon Aug 17 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.7.34-1
- Update to 0.7.34.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.33-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jun 27 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.7.33-1
- Update to 0.7.33.

* Sat Jun 13 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.7.32-1
- Update to 0.7.32.

* Wed Jun 10 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.7.31-1
- Update to 0.7.31.

* Fri Apr  3 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.7.29-1
- Update to 0.7.29.

* Tue Mar 24 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.7.28-1
- Update to 0.7.28.

* Tue Mar 17 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.7.27-1
- Update to 0.7.27.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 16 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.7.26-1
- Update to 0.7.26.

* Fri Jan 30 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.7.25-1
- Update to 0.7.25.

* Wed Jan 28 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.7.24-1
- Update to 0.7.24.

* Tue Jan 20 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.7.23-1
- Update to 0.7.23.

* Tue Jan 13 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.7.22-1
- Update to 0.7.22.

* Mon Jan 12 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.7.21-1
- Update to 0.7.21.

* Mon Dec 15 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.7.20-1
- Update to 0.7.20.

* Mon Dec  1 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.7.19-1
- Update to 0.7.19.

* Fri Nov  7 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.7.18-1
- Update to 0.7.18.

* Wed Oct 15 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.7.17-1
- Update to 0.7.17.

* Fri Sep 26 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.7.16-1
- Update to 0.7.16.

* Fri Sep 19 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.7.15-1
- Update to 0.7.15.
- Bump min version of glib needed.
- Update broken-pkgconfig patch.

* Sat Aug 23 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.7.14-1
- Update to 0.7.14.
- Add README & NEWS to docs.

* Tue Jul 29 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.7.13-1
- Update to 0.7.13.

* Mon Jul 28 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.7.12-2
- Update broken-pkgconfig patch. (#456621)

* Mon Jul 21 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.7.12-1
- Update to 0.7.12.
- Update pkgconfig patch.

* Thu Jul  3 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.7.11-1
- Update to 0.7.11.

* Fri Jun  6 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.7.10-1
- Update 0.7.10.

* Fri May 30 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.7.9-1
- Update to 0.7.9.
- Enable tests.

* Fri May  9 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.7.8-1
- Update to 0.7.8.

* Tue Apr 22 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.7.6-1
- Update to 0.7.6.

* Mon Mar 24 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.7.5-4
- Bump.

* Fri Mar 21 2008 - Bastien Nocera <bnocera@redhat.com> - 0.7.5-3
- Really fix #436773

* Mon Mar 10 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.7.5-2
- Add requires for glib2-devel to devel package. (#436773)

* Fri Mar  7 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.7.5-1
- Update to 0.7.5.
- Remove hack to fix ppc64 build.  fixed upstream.

* Thu Mar  6 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.7.4-1
- Update to 0.7.4.
- Disable test for now.
- Add hack to fix build on ppc64.

* Fri Feb  8 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.7.0-2
- Rebuild for gcc-4.3.

* Fri Nov 23 2007 Brian Pepple <bpepple@fedoraproject.org> - 0.7.0-1
- Update to 0.7.0.
- Drop unstable-static subpackage.
- Bump min. versions of dbus-devel & dbus-glib-devel.

* Mon Nov 12 2007 Brian Pepple <bpepple@fedoraproject.org> - 0.6.1-1
- Update to 0.6.1.

* Wed Aug 29 2007 Brian Pepple <bpepple@fedoraproject.org> - 0.5.14-1
- Update to 0.5.14.

* Tue Aug 28 2007 Brian Pepple <bpepple@fedoraproject.org> - 0.5.13-6
- Add BR on python.

* Tue Aug 21 2007 Brian Pepple <bpepple@fedoraproject.org> - 0.5.13-5
- Rebuild.

* Sun Aug  5 2007 Brian Pepple <bpepple@fedoraproject.org> - 0.5.13-4
- Update license tag.

* Mon Jun 18 2007 Brian Pepple <bpepple@fedoraproject.org> - 0.5.13-3
- Add check section to run test suite.
- Mark gtk-docs as docs.

* Sat Jun 16 2007 Brian Pepple <bpepple@fedoraproject.org> - 0.5.13-2
- Change Group to more accurate categoryn.
- Require pkgconfig on the devel package.
- Move headers for unstable libs to unstable-static sub-pacakge.

* Tue Jun  5 2007 Brian Pepple <bpepple@fedoraproject.org> - 0.5.13-1
- Update to 0.5.13.

* Wed May 16 2007 Brian Pepple <bpepple@fedoraproject.org> - 0.5.11-1
- Update to 0.5.11.

* Sat Apr 21 2007 Brian Pepple <bpepple@fedoraproject.org> - 0.5.10-1
- Intial spec.
