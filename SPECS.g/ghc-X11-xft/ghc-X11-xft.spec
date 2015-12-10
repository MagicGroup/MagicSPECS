# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name X11-xft

Name:           ghc-%{pkg_name}
Version:        0.3.1
Release:        17%{?dist}
Summary:        Haskell libXft binding

# no version specified
License:        LGPLv2+
Url:            https://hackage.haskell.org/package/%{pkg_name}
Source0:        https://hackage.haskell.org/package/%{pkg_name}-%{version}/%{pkg_name}-%{version}.tar.gz

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
# Begin cabal-rpm deps:
BuildRequires:  ghc-X11-devel
BuildRequires:  ghc-utf8-string-devel
BuildRequires:  pkgconfig(xft)
# End cabal-rpm deps

%description
Haskell bindings to the X Free Type interface library, and some Xrender parts.


%package devel
Summary:        Haskell %{pkg_name} library development files
Provides:       %{name}-static = %{version}-%{release}
Requires:       ghc-compiler = %{ghc_version}
Requires(post): ghc-compiler = %{ghc_version}
Requires(postun): ghc-compiler = %{ghc_version}
Requires:       %{name}%{?_isa} = %{version}-%{release}
# Begin cabal-rpm deps:
Requires:       pkgconfig(xft)
# End cabal-rpm deps

%description devel
This package provides the Haskell %{pkg_name} library development files.


%prep
%setup -q -n %{pkg_name}-%{version}


%build
%ghc_lib_build


%install
%ghc_lib_install


%post devel
%ghc_pkg_recache


%postun devel
%ghc_pkg_recache


%files -f %{name}.files
%doc LICENSE
%{_docdir}/%{name}-%{version}/LICENSE

%files devel -f %{name}-devel.files
%doc Hello.hs


%changelog
* Sun Nov 08 2015 Liu Di <liudidi@gmail.com> - 0.3.1-17
- 为 Magic 3.0 重建

* Sun Sep 20 2015 Liu Di <liudidi@gmail.com> - 0.3.1-16
- 为 Magic 3.0 重建

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jan 28 2015 Jens Petersen <petersen@redhat.com> - 0.3.1-14
- cblrpm refresh

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 07 2013 Jens Petersen <petersen@redhat.com> - 0.3.1-10
- update to new simplified Haskell Packaging Guidelines

* Fri Mar 22 2013 Jens Petersen <petersen@redhat.com> - 0.3.1-9
- BR pkgconfig(xft)

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Nov 17 2012 Jens Petersen <petersen@redhat.com> - 0.3.1-7
- change license tag to LGPLv2+ since no license version specified
- update with cabal-rpm

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Jens Petersen <petersen@redhat.com> - 0.3.1-5
- change prof BRs to devel

* Fri Jun 15 2012 Jens Petersen <petersen@redhat.com> - 0.3.1-4
- rebuild

* Thu Mar 22 2012 Jens Petersen <petersen@redhat.com> - 0.3.1-3
- add LICENSE to ghc_files

* Fri Jan  6 2012 Jens Petersen <petersen@redhat.com> - 0.3.1-2
- update to cabal2spec-0.25.2

* Fri Dec  2 2011 Jens Petersen <petersen@redhat.com> - 0.3.1-1
- update to 0.3.1 and cabal2spec-0.24.1

* Mon Oct 24 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.3-16.3
- rebuild with new gmp without compat lib

* Fri Oct 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.3-16.2
- rebuild with new gmp without compat lib

* Tue Oct 11 2011 Peter Schiffer <pschiffe@redhat.com> - 0.3-16.1
- rebuild with new gmp

* Wed Jun 22 2011 Jens Petersen <petersen@redhat.com> - 0.3-16
- BR ghc-Cabal-devel instead of ghc-prof and use ghc_arches (cabal2spec-0.23.2)

* Thu Mar 10 2011 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.3-15
- Enable build on sparcv9

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 16 2011 Jens Petersen <petersen@redhat.com> - 0.3-13
- update to cabal2spec-0.22.4

* Sun Dec  5 2010 Jens Petersen <petersen@redhat.com> - 0.3-12
- rebuild

* Fri Nov 26 2010 Jens Petersen <petersen@redhat.com> - 0.3-11
- update url and drop -o obsoletes

* Sat Sep  4 2010 Jens Petersen <petersen@redhat.com> - 0.3-10
- update to latest macros, hscolour and drop doc pkg (cabal2spec-0.22.2)

* Fri Jun 25 2010 Jens Petersen <petersen@redhat.com> - 0.3-9
- strip shared library (cabal2spec-0.21.4)

* Tue Apr 27 2010 Jens Petersen <petersen@redhat.com> - 0.3-8
- rebuild against ghc-6.12.2
- condition ghc_lib_package
- depend on utf8-string again

* Fri Jan 15 2010 Jens Petersen <petersen@redhat.com> - 0.3-7
- drop ghc-utf8-string-devel dependency: utf8-string is part of ghc!

* Mon Jan 11 2010 Jens Petersen <petersen@redhat.com> - 0.3-6
- update to ghc-rpm-macros-0.5.1 and cabal2spec-0.21.1:
- drop doc and prof bcond
- use common summary and common_description
- use ghc_lib_package, ghc_pkg_deps, ghc_pkg_c_deps

* Wed Dec 23 2009 Jens Petersen <petersen@redhat.com> - 0.3-5
- update packaging for ghc-6.12.1
- added shared library support: needs ghc-rpm-macros 0.3.1
- rebuild for ghc-X11-1.5.0.0

* Mon Nov 16 2009 Jens Petersen <petersen@redhat.com> - 0.3-4
- rebuild for ghc-X11-1.4.6.1
- use %%ghc_pkg_ver for lib dep requires

* Wed Aug 26 2009 Jens Petersen <petersen@redhat.com> - 0.3-3
- fix up devel, doc and prof deps

* Fri Aug 14 2009 Zachary Oglesby <zoglesby@fedoraproject.org> - 0.3-2
- Fixed description of -doc to pass rpmlint

* Fri Aug 14 2009 Zachary Oglesby <zoglesby@fedoraproject.org> - 0.3-1
- Updated to version 0.3
- Added ghc-utf8-string-prof as build requirement
- Added ghc-utf8-string-doc as build requirement
- Added ghc-X11-prof as build requirement
- Added ghc-X11-doc as build requirement

* Tue Jul 14 2009 Zachary Oglesby <zoglesby@fedoraproject.org> - 0.2-4
- Added ghc-utf8-string-devel as build requirment
- Added ghc-X11-devel as build requirment

* Thu Jun 18 2009 Zachary Oglesby <zoglesby@fedoraproject.org> - 0.2-3
- Fixed License

* Fri Jun  5 2009 Zachary Oglesby <zoglesby@fedoraproject.org> - 0.2-2
- Updated to new cabal2spec

* Fri May 29 2009 Zachary Oglesby <zoglesby@fedoraproject.org> - 0.2-1
- initial packaging for Fedora created by cabal2spec
