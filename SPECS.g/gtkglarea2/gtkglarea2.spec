Summary:        OpenGL GTK widget
Name:           gtkglarea2
Version:        2.0.1
Release:        5%{?dist}

License:        LGPLv2+
Group:          System Environment/Libraries
URL:            http://ftp.gnome.org/pub/gnome/sources/gtkglarea/2.0/
Source0:        http://ftp.gnome.org/pub/gnome/sources/gtkglarea/2.0/gtkglarea-%{version}.tar.bz2

Patch0:         gtkglarea-2.0.1-link-examples-with-libm.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  pkgconfig
BuildRequires:  gtk2-devel
BuildRequires:  libGL-devel
BuildRequires:  libGLU-devel

%package devel
Summary:        Development package for gtkglarea2
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       gtk2-devel
Requires:       libGL-devel
Requires:       libGLU-devel

%description
GtkGLArea is a GTK widget that makes it easy to use OpenGL or Mesa
from your GTK programs.

%description devel
GtkGLArea is a GTK widget that makes it easy to use OpenGL or Mesa
from your GTK programs.
This package contains header files and libraries for GtkGLArea
software development.

%prep
%setup -q -n gtkglarea-%{version}
%patch0 -p1

%build
%configure --disable-static --disable-dependency-tracking
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/libgtkgl-2.0.so.*

%files devel
%defattr(-,root,root,-)
%doc COPYING README AUTHORS TODO
%exclude %{_libdir}/libgtkgl-2.0.la
# %{_libdir}/libgtkgl-2.0.a
%{_libdir}/libgtkgl-2.0.so
%{_includedir}/gtkgl-2.0
%{_libdir}/pkgconfig/gtkgl-2.0.pc

%changelog
* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov  7 2011 Richard W.M. Jones <rjones@redhat.com> - 2.0.1-3
- Rebuild for libpng 1.5.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul  7 2010 Richard W.M. Jones <rjones@redhat.com> - 2.0.1-1
- New(-ish) upstream version 2.0.1 (RHBZ#611999).
- Fix examples to link directly with -lm.
- Make sure COPYING is included with each RPM as required by LGPL section 1.
- Make sure each RPM has documentation (from rpmlint).
- Use spaces instead of tabs (from rpmlint).

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.99.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.99.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jul 25 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.99.0-9
- fix license tag

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.99.0-8
- Autorebuild for GCC 4.3

* Mon Aug 28 2006 Gerard Milmeister <gemi@bluewin.ch> - 1.99.0-7
- Rebuild for FE6

* Sat Mar 04 2006 Ralf Corsépius <rc040203@freenet.de> - 1.99.0-6
- Re-enable building.
- disable static libs.
- disable dep-tracking.
- BR|R: libGL-devel, libGLU-devel.

* Fri Feb 17 2006 Gerard Milmeister <gemi@bluewin.ch> - 1.99.0-5
- Rebuild for Fedora Extras 5

* Sun Jan  1 2006 Gerard Milmeister <gemi@bluewin.ch> - 1.99.0-3
- adapted for modular xorg

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sun Feb 13 2005 Gerard Milmeister <gemi@bluewin.ch> - 0:1.99.0-1
- Adapted for Extras

* Sun Jul  6 2003 Dams <anvil[AT]livna.org> 0:1.99.0-0.fdr.4
- Renamed specfile to gtkglarea2.spec to make rpmlint happy.
- Added missing dependencies for devel package
- Fixed typo in devel Summary:

* Wed Jun 25 2003 Dams <anvil[AT]livna.org> 0:1.99.0-0.fdr.3
- BuildRequires for XFree86-Mesa-libGL/libGLU
- Removed URL in Source0

* Tue May  6 2003 Dams <anvil[AT]livna.org> 0:1.99.0-0.fdr.2
- buildroot -> RPM_BUILD_ROOT

* Wed Apr 23 2003 Dams <anvil[AT]livna.org>
- Initial build.
