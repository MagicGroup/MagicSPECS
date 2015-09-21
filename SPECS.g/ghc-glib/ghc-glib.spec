# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name glib

Name:           ghc-%{pkg_name}
Version:        0.13.1.1
Release:        2%{?dist}
Summary:        Binding to the GLIB library for Gtk2Hs

License:        LGPLv2+
Url:            https://hackage.haskell.org/package/%{pkg_name}
Source0:        https://hackage.haskell.org/package/%{pkg_name}-%{version}/%{pkg_name}-%{version}.tar.gz

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
# Begin cabal-rpm deps:
BuildRequires:  ghc-bytestring-devel
BuildRequires:  ghc-containers-devel
BuildRequires:  ghc-text-devel
BuildRequires:  ghc-utf8-string-devel
BuildRequires:  gtk2hs-buildtools
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gobject-2.0)
# End cabal-rpm deps

%description
GLib is a collection of C data structures and utility functions for the GObject
system, main loop implementation, for strings and common data structures
dealing with Unicode. This package only binds as much functionality as required
to support the packages that wrap libraries that are themselves based on GLib.


%package devel
Summary:        Haskell %{pkg_name} library development files
Provides:       %{name}-static = %{version}-%{release}
Requires:       ghc-compiler = %{ghc_version}
Requires(post): ghc-compiler = %{ghc_version}
Requires(postun): ghc-compiler = %{ghc_version}
Requires:       %{name}%{?_isa} = %{version}-%{release}
# Begin cabal-rpm deps:
Requires:       pkgconfig(glib-2.0)
Requires:       pkgconfig(gobject-2.0)
# End cabal-rpm deps
# obsolete old gtk2hs packages
Obsoletes:      ghc-gconf-devel < 0.11, ghc-gstreamer-devel < 0.11, ghc-svgcairo-devel < 0.11, ghc-gtk2hs-doc < 0.11

%description devel
This package provides the Haskell %{pkg_name} library development files.


%prep
%setup -q -n %{pkg_name}-%{version}


%build
%ghc_lib_build


%install
%ghc_lib_install

rm %{buildroot}%{ghc_pkgdocdir}/COPYING


%post devel
%ghc_pkg_recache


%postun devel
%ghc_pkg_recache


%files -f %{name}.files
%license COPYING


%files devel -f %{name}-devel.files


%changelog
* Sun Sep 20 2015 Liu Di <liudidi@gmail.com> - 0.13.1.1-2
- 为 Magic 3.0 重建

* Wed Jul 22 2015 Jens Petersen <petersen@redhat.com> - 0.13.1.1-1
- update to 0.13.1.1

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jan 19 2015 Jens Petersen <petersen@redhat.com> - 0.13.0.7-1
- update to 0.13.0.7

* Wed Oct 29 2014 Jens Petersen <petersen@redhat.com> - 0.13.0.5-1
- update to 0.13.0.5
- refresh to cblrpm-0.8.11

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Dec 21 2013 Jens Petersen <petersen@redhat.com> - 0.12.5.0-1
- update to 0.12.5.0

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 07 2013 Jens Petersen <petersen@redhat.com> - 0.12.4-3
- update to new simplified Haskell Packaging Guidelines

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 19 2012 Jens Petersen <petersen@redhat.com> - 0.12.4-1
- update to 0.12.4

* Sat Nov 17 2012 Jens Petersen <petersen@redhat.com> - 0.12.3.1-4
- update with cabal-rpm
- move old obsoletes to devel subpackage

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Jens Petersen <petersen@redhat.com> - 0.12.3.1-2
- change prof BRs to devel

* Wed Jun 13 2012 Jens Petersen <petersen@redhat.com> - 0.12.3.1-1
- update to 0.12.3.1

* Tue Mar 20 2012 Jens Petersen <petersen@redhat.com> - 0.12.3-1
- update to 0.12.3

* Fri Jan  6 2012 Jens Petersen <petersen@redhat.com> - 0.12.2-2
- update to cabal2spec-0.25.2

* Tue Dec 27 2011 Jens Petersen <petersen@redhat.com> - 0.12.2-1
- update to 0.12.2 and cabal2spec-0.25

* Thu Oct 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.12.1-1.2
- rebuild with new gmp without compat lib

* Tue Oct 11 2011 Peter Schiffer <pschiffe@redhat.com> - 0.12.1-1.1
- rebuild with new gmp

* Tue Sep 20 2011 Jens Petersen <petersen@redhat.com> - 0.12.1-1
- update to 0.12.1
- add _isa suffix to gtk2-devel depends (see #723558)

* Tue Jun 21 2011 Jens Petersen <petersen@redhat.com> - 0.12.0-5
- BR ghc-Cabal-devel instead of ghc-prof (cabal2spec-0.23.1)

* Thu Mar 10 2011 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.12.0-4
- Enable build on sparcv9

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 18 2011 Jens Petersen <petersen@redhat.com> - 0.12.0-2
- update to cabal2spec-0.22.4

* Tue Nov 30 2010 Jens Petersen <petersen@redhat.com> - 0.12.0-1
- update to 0.12.0 and drop the Gtk2HsSetup patch

* Thu Nov 25 2010 Jens Petersen <petersen@redhat.com> - 0.11.2-4
- obsolete ghc-gtk2hs-doc
- fix build with Cabal-1.10 with ghc-glib-Gtk2HsSetup-Cabal-1.10.patch

* Sat Sep 25 2010 Jens Petersen <petersen@redhat.com> - 0.11.2-3
- obsolete ghc-gtk2hs gconf, gstreamer, and svgcairo
- using ghc_pkg_obsoletes from ghc-rpm-macros-0.8.2

* Tue Sep  7 2010 Jens Petersen <petersen@redhat.com> - 0.11.2-2
- fix the build macro

* Mon Sep  6 2010 Jens Petersen <petersen@redhat.com> - 0.11.2-1
- update to 0.11.2

* Thu Aug 19 2010 Jens Petersen <petersen@redhat.com> - 0.11.1-1
- update to 0.11.1

* Fri Jul 16 2010 Jens Petersen <petersen@redhat.com> - 0.11.0-2
- use ghc-rpm-macros-0.8.1 so devel provides doc

* Wed Jun 30 2010 Jens Petersen <petersen@redhat.com> - 0.11.0-1
- description and license
- buildrequires gtk2hs-buildtools
- support hscolour
- buildrequires glib2-devel

* Wed Jun 30 2010 Fedora Haskell SIG <haskell-devel@lists.fedoraproject.org> - 0.11.0-0
- initial packaging for Fedora automatically generated by cabal2spec-0.22.1
