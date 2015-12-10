# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name haskell-src-exts

%bcond_with tests

# no useful debuginfo for Haskell packages without C sources
%global debug_package %{nil}

Name:           ghc-%{pkg_name}
Version:        1.16.0.1
Release:        5%{?dist}
Summary:        Library for manipulating Haskell source

License:        BSD
URL:            http://hackage.haskell.org/package/%{pkg_name}
Source0:        http://hackage.haskell.org/package/%{pkg_name}-%{version}/%{pkg_name}-%{version}.tar.gz

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
# Begin cabal-rpm deps:
BuildRequires:  ghc-array-devel
BuildRequires:  ghc-cpphs-devel
BuildRequires:  ghc-pretty-devel
BuildRequires:  happy
%if %{with tests}
BuildRequires:  ghc-containers-devel
BuildRequires:  ghc-directory-devel
BuildRequires:  ghc-filepath-devel
BuildRequires:  ghc-mtl-devel
BuildRequires:  ghc-smallcheck-devel
BuildRequires:  ghc-syb-devel
BuildRequires:  ghc-tasty-devel
BuildRequires:  ghc-tasty-golden-devel
BuildRequires:  ghc-tasty-smallcheck-devel
%endif
# End cabal-rpm deps
# FTBFS on s390 which 2GB max process size (#1121620)
ExcludeArch:    s390

%description
Haskell-Source with Extensions is an extension of the standard haskell-src
package, and handles most registered syntactic extensions to Haskell, including:
* Multi-parameter type classes with functional dependencies
* Indexed type families (including associated types)
* Empty data declarations
* GADTs
* Implicit parameters
* Template Haskell
and a few more. All extensions implemented in GHC are supported.
Apart from these standard extensions, it also handles regular patterns
as per the HaRP extension as well as HSX-style embedded XML syntax.


%package devel
Summary:        Haskell %{pkg_name} library development files
Provides:       %{name}-static = %{version}-%{release}
Requires:       ghc-compiler = %{ghc_version}
Requires(post): ghc-compiler = %{ghc_version}
Requires(postun): ghc-compiler = %{ghc_version}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
This package provides the Haskell %{pkg_name} library development
files.


%prep
%setup -q -n %{pkg_name}-%{version}


%build
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
%doc CHANGELOG README.md


%changelog
* Fri Dec 04 2015 Liu Di <liudidi@gmail.com> - 1.16.0.1-5
- 为 Magic 3.0 重建

* Sun Nov 08 2015 Liu Di <liudidi@gmail.com> - 1.16.0.1-4
- 为 Magic 3.0 重建

* Sun Sep 20 2015 Liu Di <liudidi@gmail.com> - 1.16.0.1-3
- 为 Magic 3.0 重建

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.16.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Apr 03 2015 Jens Petersen <petersen@redhat.com> - 1.16.0.1-1
- update to 1.16.0.1

* Wed Aug 27 2014 Jens Petersen <petersen@redhat.com> - 1.14.0.1-1
- update to 1.14.0.1
- refresh with cblrpm-0.8.11
- exclude s390 since build exhausts VM (#1121620)

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 07 2013 Jens Petersen <petersen@redhat.com> - 1.13.5-4
- update to new simplified Haskell Packaging Guidelines

* Sat Mar 23 2013 Jens Petersen <petersen@redhat.com> - 1.13.5-3
- rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Nov 07 2012 Jens Petersen <petersen@redhat.com> - 1.13.5-1
- update to 1.13.5

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Jens Petersen <petersen@redhat.com> - 1.13.3-2
- change prof BRs to devel

* Sat Jun  9 2012 Jens Petersen <petersen@redhat.com> - 1.13.3-1
- update to 1.13.3

* Thu Mar 22 2012 Jens Petersen <petersen@redhat.com> - 1.11.1-6
- add license to ghc_files

* Tue Feb  7 2012 Jens Petersen <petersen@redhat.com> - 1.11.1-5
- update to cabal2spec-0.25

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11.1-4.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Oct 24 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.11.1-3.2
- rebuild with new gmp without compat lib

* Fri Oct 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.11.1-3.1
- rebuild with new gmp without compat lib

* Sat Oct 15 2011 Jens Petersen <petersen@redhat.com> - 1.11.1-3
- rebuild for newer cpphs

* Tue Oct 11 2011 Peter Schiffer <pschiffe@redhat.com> - 1.11.1-2.1
- rebuild with new gmp

* Fri Jul 22 2011 Jens Petersen <petersen@redhat.com> - 1.11.1-2
- rebuild for cpphs-1.12

* Wed Jun 22 2011 Jens Petersen <petersen@redhat.com> - 1.11.1-1
- update to 1.11.1
- BR ghc-Cabal-devel instead of ghc-prof and use ghc_arches (cabal2spec-0.23.2)

* Fri Mar 11 2011 Jens Petersen <petersen@redhat.com> - 1.10.2-1
- update to 1.10.2

* Thu Mar 10 2011 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.9.6-4
- Enable build on sparcv9

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 18 2011 Jens Petersen <petersen@redhat.com> - 1.9.6-2
- update to cabal2spec-0.22.4

* Mon Nov 29 2010 Jens Petersen <petersen@redhat.com> - 1.9.6-1
- update to 1.9.6
- update url

* Sat Sep  4 2010 Jens Petersen <petersen@redhat.com> - 1.9.0-2
- add hscolour and doc obsolete (cabal2spec-0.22.2)

* Sat Jun 26 2010 Jens Petersen <petersen@redhat.com> - 1.9.0-1
- 1.9.0 release
- sync cabal2spec-0.22

* Mon Feb 15 2010 Conrad Meyer <konrad@tylerc.org> - 1.8.2-2
- Bump to rebuild against cpphs 1.11

* Mon Feb 15 2010 Conrad Meyer <konrad@tylerc.org> - 1.8.2-1
- Bump to 1.8.2

* Fri Jan 22 2010 Jens Petersen <petersen@redhat.com> - 1.6.1-1
- update to 1.6.1

* Mon Jan 11 2010 Jens Petersen <petersen@redhat.com> - 1.5.3-1
- update to 1.5.3
- update to ghc-rpm-macros-0.5.1 and cabal2spec-0.21.1:
- drop doc and prof bcond
- use ghc_lib_package and ghc_pkg_deps
- drop redundant buildroot and its install cleaning

* Mon Nov 16 2009 Jens Petersen <petersen@redhat.com> - 1.3.0-2
- use %%ghc_pkg_ver for requires

* Sun Nov 15 2009 Jens Petersen <petersen@redhat.com> - 1.3.0-1
- update to 1.3.0
- requires ghc-cpphs-devel

* Fri Sep 18 2009 Jens Petersen <petersen@redhat.com> - 1.1.4-1
- update to 1.1.4

* Tue Aug  4 2009 Yaakov M. Nemoy <ynemoy@fedoraproject.org> - 1.0.1-3
- rebuild against new ghc

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 1 2009 Conrad Meyer <konrad@tylerc.org> - 1.0.1-1
- Version bump.

* Tue Jun  2 2009 Jens Petersen <petersen@redhat.com> - 0.4.8-7
- drop superfluous cpphs and happy requires

* Sun May 24 2009 Jens Petersen <petersen@redhat.com> - 0.4.8-6
- buildrequires ghc-rpm-macros (cabal2spec-0.16)

* Fri Apr 24 2009 Jens Petersen <petersen@redhat.com> - 0.4.8-5
- sync with cabal2spec-0.15
- buildrequires >= 6.10.2-3 for latest macros

* Thu Mar 19 2009 Conrad Meyer <konrad@tylerc.org> - 0.4.8-4
- Update to new cabal2spec template.

* Mon Feb 16 2009 Conrad Meyer <konrad@tylerc.org> - 0.4.8-3
- Update to new cabal2spec template.
- Replace %%defines by %%globals.

* Wed Jan 21 2009 Conrad Meyer <konrad@tylerc.org> - 0.4.8-2
- update to new haskell packaging template

* Mon Jan 12 2009 Conrad Meyer <konrad@tylerc.org> - 0.4.8-1
- initial packaging for Fedora created by cabal2spec
