# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name HUnit

%bcond_without tests

Name:           ghc-%{pkg_name}
# part of haskell-platform
Version:        1.2.5.2
Release:        37%{?dist}
Summary:        Unit testing framework for Haskell

License:        BSD
Url:            https://hackage.haskell.org/package/%{pkg_name}
Source0:        https://hackage.haskell.org/package/%{pkg_name}-%{version}/%{pkg_name}-%{version}.tar.gz

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
# Begin cabal-rpm deps:
BuildRequires:  ghc-deepseq-devel
%if %{with tests}
BuildRequires:  ghc-filepath-devel
%endif
# End cabal-rpm deps

%description
HUnit is a unit testing framework for Haskell, inspired by JUnit for Java.


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

# remove unwanted files
rm %{buildroot}%{_datadir}/%{pkg_name}-%{version}/{README,doc/Guide.html,examples/Example.hs,prologue.txt}


%check
%if %{with tests}
mv HUnit.cabal HUnit.cabal.orig
mv HUnit.cabal.tests HUnit.cabal
%cabal configure --enable-tests
%cabal build
%cabal test
mv HUnit.cabal HUnit.cabal.tests
mv HUnit.cabal.orig HUnit.cabal
%endif


%post devel
%ghc_pkg_recache


%postun devel
%ghc_pkg_recache


%files -f %{name}.files
%doc LICENSE
%{_docdir}/%{name}-%{version}/LICENSE


%files devel -f %{name}-devel.files
%doc README doc/Guide.html examples/Example.hs


%changelog
* Sun Nov 08 2015 Liu Di <liudidi@gmail.com> - 1.2.5.2-37
- 为 Magic 3.0 重建

* Sun Sep 20 2015 Liu Di <liudidi@gmail.com> - 1.2.5.2-36
- 为 Magic 3.0 重建

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.5.2-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jan 27 2015 Jens Petersen <petersen@redhat.com> - 1.2.5.2-34
- cblrpm refresh

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.5.2-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jun  4 2014 Jens Petersen <petersen@redhat.com> - 1.2.5.2-32
- enable tests

* Mon Feb 24 2014 Jens Petersen <petersen@redhat.com> - 1.2.5.2-31
- split out of haskell-platform

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec 30 2011 Jens Petersen <petersen@redhat.com> - 1.2.4.2-2
- fix accidently deleted post script
- cabal2spec-0.25.1

* Tue Dec 27 2011 Jens Petersen <petersen@redhat.com> - 1.2.4.2-1
- update to 1.2.4.2 for haskell-platform-2011.4.0.0
- update to cabal2spec-0.25

* Mon Oct 24 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.2.2.3-7.3
- rebuild with new gmp without compat lib

* Fri Oct 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.2.2.3-7.2
- rebuild with new gmp without compat lib

* Tue Oct 11 2011 Peter Schiffer <pschiffe@redhat.com> - 1.2.2.3-7.1
- rebuild with new gmp

* Tue Jun 21 2011 Jens Petersen <petersen@redhat.com> - 1.2.2.3-7
- ghc_arches replaces ghc_excluded_archs

* Mon Jun 20 2011 Jens Petersen <petersen@redhat.com> - 1.2.2.3-6
- BR ghc-Cabal-devel and use ghc_excluded_archs

* Fri May 27 2011 Jens Petersen <petersen@redhat.com> - 1.2.2.3-5
- update to cabal2spec-0.23: add ppc64

* Thu Mar 10 2011 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.2.2.3-4
- Enable build on sparcv9

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 17 2011 Jens Petersen <petersen@redhat.com> - 1.2.2.3-2
- update to cabal2spec-0.22.4

* Sun Dec  5 2010 Jens Petersen <petersen@redhat.com> - 1.2.2.3-1
- update to 1.2.2.3

* Thu Nov 25 2010 Jens Petersen <petersen@redhat.com> - 1.2.2.1-5
- drop -o obsolete
- don't list license file twice

* Sat Jul 31 2010 Jens Petersen <petersen@redhat.com> - 1.2.2.1-4
- ghc-rpm-macros-0.8.1 for doc obsoletes
- part of haskell-platform-2010.2.0.0
- add hscolour
- datadir filelist cleanup

* Sun Jun 27 2010 Jens Petersen <petersen@redhat.com> - 1.2.2.1-3
- sync cabal2spec-0.22.1

* Tue Apr 27 2010 Jens Petersen <petersen@redhat.com> - 1.2.2.1-2
- part of haskell-platform-2010.1.0.0
- rebuild against ghc-6.12.2
- condition ghc_lib_package

* Mon Jan 11 2010 Jens Petersen <petersen@redhat.com> - 1.2.2.1-1
- update 1.2.2.1 (current haskell-platform-2009.3.1)
- remove test programs and move doc files to docdir
- add check section for test programs
- update to ghc-rpm-macros-0.5.1 and cabal2spec-0.21.1:
- drop doc and prof bcond
- use common summary and common_description
- use ghc_lib_package
- drop redundant buildroot and its install cleaning

* Wed Dec 23 2009 Jens Petersen <petersen@redhat.com> - 1.2.0.3-2
- update packaging for ghc-6.12.1
- added shared library support: needs ghc-rpm-macros 0.3.1

* Wed Aug 12 2009 Bryan O'Sullivan <bos@serpentine.com> - 1.2.0.3-1
- initial packaging for Fedora created by cabal2spec
