# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name ghc-paths

Name:           ghc-%{pkg_name}
Version:        0.1.0.9
Release:        6%{?dist}
Summary:        Interface to GHC's installation directories

License:        BSD
Url:            https://hackage.haskell.org/package/%{pkg_name}
Source0:        https://hackage.haskell.org/package/%{pkg_name}-%{version}/%{pkg_name}-%{version}.tar.gz

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros

%description
Knowledge of GHC's installation directories.


%package devel
Summary:        Haskell %{pkg_name} library development files
Provides:       %{name}-static = %{version}-%{release}
Requires:       ghc-compiler = %{ghc_version}
Requires(post): ghc-compiler = %{ghc_version}
Requires(postun): ghc-compiler = %{ghc_version}
Requires:       %{name}%{?_isa} = %{version}-%{release}

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


%files devel -f %{name}-devel.files


%changelog
* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jan 27 2015 Jens Petersen <petersen@fedoraproject.org> - 0.1.0.9-5
- cblrpm refresh

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 07 2013 Jens Petersen <petersen@redhat.com> - 0.1.0.9-1
- update to 0.1.0.9
- update to new simplified Haskell Packaging Guidelines

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0.8-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Nov 17 2012 Jens Petersen <petersen@redhat.com> - 0.1.0.8-13
- update with cabal-rpm

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0.8-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Jens Petersen <petersen@redhat.com> - 0.1.0.8-11
- change prof BRs to devel

* Thu Mar 22 2012 Jens Petersen <petersen@redhat.com> - 0.1.0.8-10
- add license to ghc_files

* Tue Jan 24 2012 Jens Petersen <petersen@redhat.com> - 0.1.0.8-9
- update to cabal2spec-0.25.4

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0.8-8.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Oct 24 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.1.0.8-7.3
- rebuild with new gmp without compat lib

* Thu Oct 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.1.0.8-7.2
- rebuild with new gmp without compat lib

* Tue Oct 11 2011 Peter Schiffer <pschiffe@redhat.com> - 0.1.0.8-7.1
- rebuild with new gmp

* Tue Jun 21 2011 Jens Petersen <petersen@redhat.com> - 0.1.0.8-7
- BR ghc-Cabal-devel instead of ghc-prof (cabal2spec-0.23.2)

* Thu Mar 10 2011 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.1.0.8-6
- Enable build on sparcv9

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 17 2011 Jens Petersen <petersen@redhat.com>
- update to cabal2spec-0.22.4

* Fri Nov 26 2010 Jens Petersen <petersen@redhat.com> - 0.1.0.8-3
- update url and drop -o obsoletes

* Wed Sep 29 2010 jkeating - 0.1.0.8-2
- Rebuilt for gcc bug 634757

* Tue Sep 21 2010 Jens Petersen <petersen@redhat.com> - 0.1.0.8-1
- update to 0.1.0.8

* Thu Sep 16 2010 Jens Petersen <petersen@redhat.com> - 0.1.0.7-1
- update to 0.1.0.7

* Sat Sep  4 2010 Jens Petersen <petersen@redhat.com> - 0.1.0.6-4
- add hscolour and doc obsolete (cabal2spec-0.22.2)

* Sun Jun 27 2010 Jens Petersen <petersen@redhat.com> - 0.1.0.6-3
- sync cabal2spec-0.22.1

* Tue Apr 27 2010 Jens Petersen <petersen@redhat.com> - 0.1.0.6-2
- rebuild against ghc-6.12.2
- condition ghc_lib_package

* Fri Jan 15 2010 Jens Petersen <petersen@redhat.com> - 0.1.0.6-1
- update to 0.1.0.6
- update to ghc-rpm-macros-0.5.1 and cabal2spec-0.21.1:
- drop doc and prof bcond
- use common_summary and common_description
- use ghc_lib_package
- build shared library
- drop redundant buildroot and its install cleaning


* Tue Sep 22 2009 Jens Petersen <petersen@redhat.com> - 0.1.0.5-9
- rebuild to test versioned ghcdocdir in ghc-rpm-macros

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun May 24 2009 Jens Petersen <petersen@redhat.com> - 0.1.0.5-7
- buildrequires ghc-rpm-macros (cabal2spec-0.16)

* Fri Apr 24 2009 Jens Petersen <petersen@redhat.com> - 0.1.0.5-6
- update to cabal2spec-0.14

* Mon Mar  9 2009 Jens Petersen <petersen@redhat.com> - 0.1.0.5-5
- package renamed from ghc-paths
- update to cabal2spec-0.12

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 13 2009 Jens Petersen <petersen@redhat.com> - 0.1.0.5-3
- update to latest packaging template: use bcond and add doc subpackage

* Tue Dec 23 2008 Jens Petersen <petersen@redhat.com> - 0.1.0.5-2
- improve summary and description (#476483)

* Mon Dec 15 2008 Jens Petersen <petersen@redhat.com> - 0.1.0.5-1
- initial packaging for Fedora
