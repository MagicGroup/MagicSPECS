Summary: A Tubing and Extrusion Library for OpenGL
Name: libgle
Version: 3.1.0
Release: 7%{?dist}
License: GPLv2 or (Artistic clarified and MIT)
Group: System Environment/Libraries
URL: http://www.linas.org/gle/
Source: http://www.linas.org/gle/pub/gle-%{version}.tar.gz
# Make the examples makefile multilib-compliant
Patch0: libgle-examples-makefile.patch

BuildRequires: mesa-libGL-devel 
BuildRequires: freeglut-devel
BuildRequires: libXmu-devel
BuildRequires: libXi-devel 

Requires(post):   /sbin/ldconfig
Requires(postun): /sbin/ldconfig

BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%description
The GLE Tubing and Extrusion Library consists of a number of "C"
language subroutines for drawing tubing and extrusions. It is a very
fast implementation of these shapes, outperforming all other
implementations, most by orders of magnitude. It uses the
OpenGL programming API to perform the actual drawing of the tubing
and extrusions.

%package devel
Requires: glut-devel
Requires: libGL-devel
Requires: libGLU-devel
Requires: libX11-devel
Requires: libXext-devel
Requires: libXi-devel
Requires: libXmu-devel
Requires: libXmu-devel
Requires: libXt-devel
Summary: GLE includes and development libraries
Group: Development/Libraries

%description devel
Includes, man pages, and development libraries for the GLE Tubing and
Extrusion Library.

%prep
%setup -q -n gle-%{version}
%patch0 -p5

%build
%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# Clean up a bit
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
mv $RPM_BUILD_ROOT%{_docdir}/gle docs
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/*.so.*
%doc docs/AUTHORS docs/COPYING docs/README

%files devel
%defattr(-,root,root,-)
%{_libdir}/*.so
%{_includedir}/*
%{_mandir}/man?/*
%doc docs/examples docs/html


%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 3.1.0-7
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 18 2010 Mary Ellen Foster <mefoster at gmail.com> - 3.1.0-4
- Add the full set of requirements for the -devel package

* Mon Nov 30 2009 Mary Ellen Foster <mefoster at gmail.com> - 3.1.0-3
- Incorporate some more suggestions from Thomas Fitzsimmons

* Wed Sep 30 2009 Mary Ellen Foster <mefoster at gmail.com> - 3.1.0-2
- Incorporating some clean-ups from Ralf Corsépius's spec file

* Tue Sep 29 2009 Mary Ellen Foster <mefoster at gmail.com> - 3.1.0-1
- Initial version, based on upstream .spec file
