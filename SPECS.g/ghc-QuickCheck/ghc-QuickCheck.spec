# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name QuickCheck

%bcond_with tests

Name:           ghc-%{pkg_name}
# part of haskell-platform
Version:        2.7.6
Release:        4%{?dist}
Summary:        Automatic testing of Haskell programs

License:        BSD
Url:            https://hackage.haskell.org/package/%{pkg_name}
Source0:        https://hackage.haskell.org/package/%{pkg_name}-%{version}/%{pkg_name}-%{version}.tar.gz

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
# Begin cabal-rpm deps:
BuildRequires:  ghc-random-devel
%ifarch %{ghc_arches_with_ghci}
BuildRequires:  ghc-template-haskell-devel
%endif
BuildRequires:  ghc-tf-random-devel
BuildRequires:  ghc-transformers-devel
ExclusiveArch:  %{ghc_arches_with_ghci}
%if %{with tests}
BuildRequires:  ghc-test-framework-devel
%endif
# End cabal-rpm deps

%description
QuickCheck is a library for random testing of program properties.

The programmer provides a specification of the program, in the form of
properties which functions should satisfy, and QuickCheck then tests that the
properties hold in a large number of randomly generated cases.

Specifications are expressed in Haskell, using combinators defined in the
QuickCheck library. QuickCheck provides combinators to define properties,
observe the distribution of test data, and define test data generators.


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
%ifnarch %{ghc_arches_with_ghci}
%define cabal_configure_options -f "-templateHaskell"
%endif
%ghc_lib_build


%install
%ghc_lib_install


%check
%if %{with tests}
%cabal test
%endif


%post devel
%ghc_pkg_recache


%postun devel
%ghc_pkg_recache


%files -f %{name}.files
%doc LICENSE
%{_docdir}/%{name}-%{version}/LICENSE

%files devel -f %{name}-devel.files
%doc examples README


%changelog
* Sun Nov 08 2015 Liu Di <liudidi@gmail.com> - 2.7.6-4
- 为 Magic 3.0 重建

* Sun Sep 20 2015 Liu Di <liudidi@gmail.com> - 2.7.6-3
- 为 Magic 3.0 重建

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Apr  2 2015 Jens Petersen <petersen@redhat.com> - 2.7.6-1
- update to 2.7.6

* Wed Jan 28 2015 Jens Petersen <petersen@redhat.com> - 2.6-35
- update urls

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Mar 26 2014 Jens Petersen <petersen@redhat.com> - 2.6-32
- bump over haskell-platform

* Mon Feb 24 2014 Jens Petersen <petersen@redhat.com> - 2.6-31
- separate out of haskell-platform (#1069070)

* Tue Mar 20 2012 Jens Petersen <petersen@redhat.com> - 2.4.2-1
- update to 2.4.2

* Sun Mar 18 2012 Jens Petersen <petersen@redhat.com> - 2.4.1.1-3
- update to cabal2spec-0.25

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 27 2011 Jens Petersen <petersen@redhat.com> - 2.4.1.1-1
- update to 2.4.1.1 for haskell-platform-2011.4.0.0
- no longer depends on mtl nor ghci
- update to cabal2spec-0.24.1
- build on archs without ghci without template-haskell

* Mon Oct 24 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.4.0.1-7.3
- rebuild with new gmp without compat lib

* Fri Oct 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.4.0.1-7.2
- rebuild with new gmp without compat lib

* Tue Oct 11 2011 Peter Schiffer <pschiffe@redhat.com> - 2.4.0.1-7.1
- rebuild with new gmp

* Mon Jun 20 2011 Jens Petersen <petersen@redhat.com> - 2.4.0.1-7
- BR ghc-Cabal-devel and use ghc_excluded_archs

* Fri May 27 2011 Jens Petersen <petersen@redhat.com> - 2.4.0.1-6
- update to cabal2spec-0.23: add ppc64

* Thu Mar 10 2011 Fabio M. Di Nitto <fdinitto@redhat.com> - 2.4.0.1-5
- Enable build on sparcv9

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 23 2011 Jens Petersen <petersen@redhat.com> - 2.4.0.1-3
- rebuild

* Tue Jan 18 2011 Jens Petersen <petersen@redhat.com> - 2.4.0.1-2
- update to cabal2spec-0.22.4

* Thu Nov 25 2010 Jens Petersen <petersen@redhat.com> - 2.4.0.1-1
- update to 2.4.0.1
- add hscolour
- update url and drop -o obsoletes

* Fri Jul 16 2010 Jens Petersen <petersen@redhat.com> - 2.1.1.1-1
- update to 2.1.1.1 for haskell-platform-2010.2.0.0
- obsolete doc subpackage (ghc-rpm-macros-0.8.0)

* Sun Jun 27 2010 Jens Petersen <petersen@redhat.com> - 2.1.0.3-3
- sync cabal2spec-0.22.1

* Tue Apr 27 2010 Jens Petersen <petersen@redhat.com> - 2.1.0.3-2
- rebuild against ghc-6.12.2

* Tue Mar 23 2010 Jens Petersen <petersen@redhat.com> - 2.1.0.3-1
- update to 2.1.0.3 for haskell-platform-2010.1.0.0
- BR ghc-ghc

* Thu Jan 21 2010 Jens Petersen <petersen@redhat.com> - 2.1.0.2-2
- BSD license
- summary and description
- comment part of haskell-platform-2009.3.1

* Thu Jan 21 2010 Fedora Haskell SIG <haskell-devel@lists.fedoraproject.org> - 2.1.0.2-1
- initial packaging for Fedora automatically generated by cabal2spec-0.21.1
