Summary: A MathML rendering library
Name: gtkmathview
Version: 0.8.0
Release: 10%{?dist}
Group: System Environment/Libraries
License: LGPLv3+
Source: http://helm.cs.unibo.it/mml-widget/sources/gtkmathview-%{version}.tar.gz
URL: http://helm.cs.unibo.it/mml-widget/
BuildRequires: glib2-devel >= 2.2
BuildRequires: gtk2-devel >= 2.2
BuildRequires: libxml2-devel >= 2.6.7
BuildRequires: libxslt >= 1.0.32
BuildRequires: popt >= 1.7 
BuildRequires: popt-devel >= 1.7 
BuildRequires: t1lib-devel
BuildRequires: libtool
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Patch0: gtkmathview-0.8.0-gcc43.patch
Patch1: gtkmathview-0.8.0-includes.patch

# Fixes from git
Patch09: gtkmathview-marshalling-functions-git7d938a.patch
Patch10: gtkmathview-gcc-fixes-git3918e8.patch
Patch11: gtkmathview-fix-ComputerModernShaper-git210206.patch
Patch12: gtkmathview-lowercasegreek-gitb03152.patch

Patch20: gtkmathview-0.8.0-gcc47.patch

# these are currently f12+ only, but will propogate back to earlier
# branches soonish -- Rex
%if 0%{?fedora} > 11
Requires: lyx-fonts
%else
Requires: mathml-fonts
%endif

%description
GtkMathView is a C++ rendering engine for MathML documents. 
It provides an interactive view that can be used for browsing 
and editing MathML markup.

%package devel
Summary: Support files necessary to compile applications using gtkmathview
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: glib2-devel >= 2.2.1
Requires: gtk2-devel >= 2.2.1
Requires: libxml2-devel >= 2.6.7
Requires: popt >= 1.7.0 
Requires: pkgconfig

%description devel
Libraries, headers, and support files needed for using gtkmathview.

%prep
%setup -q
%patch0 -p1 -b .gcc43
%patch1 -p1 -b .includes

%patch10 -p1 -b .git3918e8
%patch11 -p1 -b .git210206
%patch12 -p1 -b .gitb03152

%patch20 -p1 -b .gcc47

# AM_BINRELOC missing, just ignore
echo 'AC_DEFUN([AM_BINRELOC], [])' > acinclude.m4
autoreconf -if

%build
%configure --disable-static
make %{?_smp_mflags} LIBTOOL=/usr/bin/libtool

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a

rm -f $RPM_BUILD_ROOT/%{_mandir}/man1/mathml2ps.1
rm -f $RPM_BUILD_ROOT/%{_mandir}/man1/mathmlviewer.1

%files
%defattr(-,root,root)
%doc COPYING README AUTHORS CONTRIBUTORS BUGS LICENSE
%{_bindir}/*
%{_libdir}/lib*.so.*
%{_sysconfdir}/gtkmathview/
%{_datadir}/gtkmathview/

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/pkgconfig/mathview-core.pc
%{_libdir}/pkgconfig/mathview-frontend-libxml2.pc
%{_libdir}/pkgconfig/gtkmathview-custom-reader.pc
%{_libdir}/pkgconfig/gtkmathview-libxml2-reader.pc
%{_libdir}/pkgconfig/gtkmathview-libxml2.pc
%{_libdir}/pkgconfig/mathview-frontend-libxml2-reader.pc
%{_libdir}/pkgconfig/mathview-frontend-custom-reader.pc
%{_libdir}/pkgconfig/mathview-backend-svg.pc
%{_libdir}/pkgconfig/mathview-backend-gtk.pc
%{_libdir}/pkgconfig/mathview-backend-ps.pc
%{_includedir}/gtkmathview

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Feb 27 2012 Tom Callaway <spot@fedoraproject.org> - 0.8.0-9
- apply fixes from git
- fix build with gcc 4.7

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 16 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.8.0-6
- Requires: lyx-fonts

* Tue Aug 04 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.8.0-5
- add lyx-fonts/mathml-fonts dep

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 28 2009 Caolán McNamara <caolanm@redhat.com> - 0.8.0-3
- add stdio.h for snprintf

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jul 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.8.0-1
- update to 0.8.0
- fix rpath
- fix gcc43 patch for 0.8.0

* Fri Mar 14 2008 Doug chapman <doug.chapman@hp.com> - 0.7.6-7
- fix GCC 4.3 build errors (BZ 434485)
- require popt-devel for build (BZ 426136)

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.7.6-6
- Autorebuild for GCC 4.3

* Thu Oct 12 2006 Marc Maurer <uwog@abisource.com> 0.7.6-5.fc6
- Add pkgconfig to the -devel requires (bug 206451)

* Mon Sep 16 2006 Marc Maurer <uwog@abisource.com> 0.7.6-4.fc6
- Rebuild for FC 6

* Thu Feb 16 2006 Marc Maurer <uwog@abisource.com> 0.7.6-3.fc5
- Rebuild for Fedora Extras 5

* Sun Feb 05 2006 Marc Maurer <uwog@abisource.com> - 0.7.6-2.fc5
- Use %%{?dist} in the release name
- Omit static libs (part of bug 171971)
- s/gtkmathview/%%{name} (part of bug 171971)

* Sun Dec 11 2005 Marc Maurer <uwog@abisource.com> - 0.7.6-1
- Update to 0.7.6

* Sun Sep 25 2005 Marc Maurer <uwog@abisource.com> - 0.7.5-1
- Update to 0.7.5

* Mon Sep 12 2005 Marc Maurer <uwog@abisource.com> - 0.7.4-1
- Update to 0.7.4

* Tue Aug 30 2005 Marc Maurer <uwog@abisource.com> - 0.7.3-5
- Drop more unneeded Requires

* Tue Aug 30 2005 Marc Maurer <uwog@abisource.com> - 0.7.3-4
- Drop the explicit Requires

* Mon Aug 29 2005 Marc Maurer <uwog@abisource.com> - 0.7.3-3
- Use smaller lines in the Description field
- Remove the --disable-gmetadom and --without-t1lib flags
- Add a '/' to directories in the files section
- Remove the mathmlviewer man page

* Tue Aug 23 2005 Marc Maurer <uwog@abisource.com> - 0.7.3-2
- Add the proper Requires and Buildrequires
- Make the description field more descriptive
- Add CONTRIBUTORS BUGS LICENSE to the doc section
- Disable gmetadom and t1lib
- Remove the mathml2ps man page

* Sun Aug 14 2005 Marc Maurer <uwog@abisource.com> - 0.7.3-1
- Initial version
