# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name tar

%bcond_with tests

Name:           ghc-%{pkg_name}
Version:        0.4.2.1
Release:        1%{?dist}
Summary:        Reading, writing and manipulating ".tar" archive files

License:        BSD
Url:            https://hackage.haskell.org/package/%{pkg_name}
Source0:        https://hackage.haskell.org/package/%{pkg_name}-%{version}/%{pkg_name}-%{version}.tar.gz

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
# Begin cabal-rpm deps:
BuildRequires:  ghc-array-devel
BuildRequires:  ghc-bytestring-devel
BuildRequires:  ghc-directory-devel
BuildRequires:  ghc-filepath-devel
BuildRequires:  ghc-old-time-devel
%if %{with tests}
BuildRequires:  ghc-QuickCheck-devel
BuildRequires:  ghc-tasty-devel
BuildRequires:  ghc-tasty-quickcheck-devel
BuildRequires:  ghc-time-devel
%endif
# End cabal-rpm deps

%description
This library is for working with "'.tar'" archive files. It can read and write
a range of common variations of archive format including V7, USTAR, POSIX and
GNU formats. It provides support for packing and unpacking portable archives.
This makes it suitable for distribution but not backup because details like
file ownership and exact permissions are not preserved.


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


%files devel -f %{name}-devel.files


%changelog
* Sat Aug 08 2015 Ben Boeckel <mathstuf@gmail.com> - 0.4.2.1-1
- update to 0.4.2.1

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jan 27 2015 Jens Petersen <petersen@fedoraproject.org> - 0.4.0.1-7
- cblrpm refresh

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jun 04 2013 Jens Petersen <petersen@redhat.com> - 0.4.0.1-3
- update to new simplified Haskell Packaging Guidelines

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 08 2012 Jens Petersen <petersen@redhat.com> - 0.4.0.1-1
- update to 0.4.0.1

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Mar 20 2012 Jens Petersen <petersen@redhat.com> - 0.3.2.0-1
- update to 0.3.2.0

* Sun Mar 18 2012 Jens Petersen <petersen@redhat.com> - 0.3.1.0-15
- update to cabal2spec-0.25

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1.0-14.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Oct 24 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.3.1.0-13.3
- rebuild with new gmp without compat lib

* Fri Oct 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.3.1.0-13.2
- rebuild with new gmp without compat lib

* Tue Oct 11 2011 Peter Schiffer <pschiffe@redhat.com> - 0.3.1.0-13.1
- rebuild with new gmp

* Sat Jul 09 2011 Ben Boeckel <mathstuf@gmail.com> - 0.3.1.0-13
- Update to cabal2spec-0.24

* Thu Jun 23 2011 Jens Petersen <petersen@redhat.com> - 0.3.1.0-12
- BR ghc-Cabal-devel instead of ghc-prof and use ghc_arches (cabal2spec-0.23.2)

* Thu Mar 10 2011 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.3.1.0-11
- Enable build on sparcv9

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 15 2011 Ben Boeckel <mathstuf@gmail.com> - 0.3.1.0-9
- Update to cabal2spec-0.22.4
- Rebuild

* Thu Nov 25 2010 Jens Petersen <petersen@redhat.com> - 0.3.1.0-8
- update url

* Sun Nov 07 2010 Ben Boeckel <mathstuf@gmail.com> - 0.3.1.0-7
- Rebuild
- Update summary and description

* Sat Sep  4 2010 Jens Petersen <petersen@redhat.com> - 0.3.1.0-6
- add hscolour and doc obsolete (cabal2spec-0.22.2)

* Sun Jun 27 2010 Jens Petersen <petersen@redhat.com> - 0.3.1.0-5
- sync cabal2spec-0.22.1

* Tue Apr 27 2010 Jens Petersen <petersen@redhat.com> - 0.3.1.0-4
- rebuild against ghc-6.12.2
- condition ghc_lib_package

* Mon Jan 11 2010 Jens Petersen <petersen@redhat.com> - 0.3.1.0-3
- update to ghc-rpm-macros-0.5.1 and cabal2spec-0.21.1:
- drop doc and prof bcond
- use ghc_lib_package

* Sat Dec 26 2009 Jens Petersen <petersen@redhat.com> - 0.3.1.0-2
- update for ghc-6.12.1: add shared library support
- use new ghc*_requires macros: needs ghc-rpm-macros 0.4.0
- add common_summary and common_description

* Fri Aug 28 2009 Yaakov M. Nemoy <ynemoy@fedoraproject.org> - 0.3.1.0-1
- updated to latest upstream

* Sun Aug 23 2009 Yaakov M. Nemoy <loupgaroublond@gmail.com> - 0.3.0.0-2
- updated to latest cabal2spec output

* Tue Mar  3 2009 Yaakov M. Nemoy <loupgaroublond@gmail.com> - 0.3.0.0-1
- initial packaging for Fedora created by cabal2spec
