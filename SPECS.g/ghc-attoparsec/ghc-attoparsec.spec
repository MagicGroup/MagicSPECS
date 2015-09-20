# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name attoparsec

%bcond_with tests

Name:           ghc-%{pkg_name}
# part of haskell-platform-2013.2+
Version:        0.11.3.4
Release:        2%{?dist}
Summary:        Fast combinator parsing for bytestrings and text

License:        BSD
Url:            https://hackage.haskell.org/package/%{pkg_name}
Source0:        https://hackage.haskell.org/package/%{pkg_name}-%{version}/%{pkg_name}-%{version}.tar.gz

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
# Begin cabal-rpm deps:
BuildRequires:  ghc-array-devel
BuildRequires:  ghc-bytestring-devel
BuildRequires:  ghc-containers-devel
BuildRequires:  ghc-deepseq-devel
BuildRequires:  ghc-scientific-devel
BuildRequires:  ghc-text-devel
%if %{with tests}
BuildRequires:  ghc-QuickCheck-devel
BuildRequires:  ghc-test-framework-devel
BuildRequires:  ghc-test-framework-quickcheck2-devel
%endif
# End cabal-rpm deps

%description
A fast parser combinator library, aimed particularly at dealing efficiently
with network protocols and complicated text/binary file formats.


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
%doc README.markdown examples


%changelog
* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jan 26 2015 Jens Petersen <petersen@redhat.com> - 0.11.3.4-1
- update to 0.11.3.4

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat May 04 2013 Jens Petersen <petersen@redhat.com> - 0.10.4.0-1
- update to 0.10.4.0 (now part of Haskell Platform 2013.2)
- update spec file to cabal-rpm-0.8.0

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Nov 17 2012 Jens Petersen <petersen@redhat.com> - 0.10.2.0-4
- update with cabal-rpm

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Jens Petersen <petersen@redhat.com> - 0.10.2.0-2
- change prof BRs to devel

* Tue Jun 19 2012 Ben Boeckel <mathstuf@gmail.com> - 0.10.2.0-1
- Update to 0.10.2.0

* Fri Jun 15 2012 Jens Petersen <petersen@redhat.com> - 0.10.1.1-3
- rebuild

* Fri Mar 23 2012 Jens Petersen <petersen@redhat.com> - 0.10.1.1-2
- add license to ghc_files

* Tue Feb 28 2012 Ben Boeckel <mathstuf@gmail.com> - 0.10.1.1-1
- Update to 0.10.1.1

* Thu Jan  5 2012 Jens Petersen <petersen@redhat.com> - 0.10.1.0-1
- update to 0.10.1.0 and cabal2spec-0.25.2
- now depends on text library

* Thu Oct 27 2011 Jens Petersen <petersen@redhat.com> - 0.9.1.2-1
- update to 0.9.1.2
- BR ghc-*-prof not devel

* Thu Oct 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.9.1.1-2.2
- rebuild with new gmp without compat lib

* Tue Oct 11 2011 Peter Schiffer <pschiffe@redhat.com> - 0.9.1.1-2.1
- rebuild with new gmp

* Mon Jul 25 2011 Ben Boeckel <mathstuf@gmail.com> - 0.9.1.1-2
- Update to cabal2spec-0.24

* Fri Jul 22 2011 Jens Petersen <petersen@redhat.com> - 0.9.1.1-1
- update to 0.9.1.1

* Fri Jun 24 2011 Jens Petersen <petersen@redhat.com> - 0.8.6.1-2
- BR ghc-Cabal-devel instead of ghc-prof and use ghc_arches (cabal2spec-0.23.2)

* Wed May 11 2011 Ben Boeckel <mathstuf@gmail.com> - 0.8.6.1-1
- Update to 0.8.6.1
- Update to cabal2spec-0.22.7

* Tue May 10 2011 Ben Boeckel <mathstuf@gmail.com> - 0.8.5.3-2
- Update to cabal2spec-0.22.6

* Tue May 10 2011 Ben Boeckel <mathstuf@gmail.com> - 0.8.5.3-1
- Update to cabal2spec-0.22.5
- Update to 0.8.5.3
- Add new deepseq dependency

* Thu Mar 10 2011 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.8.5.0-3
- Enable build on sparcv9

* Sat Mar 05 2011 Ben Boeckel <mathstuf@gmail.com> - 0.8.5.0-2
- Update to 0.8.5.0

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 15 2011 Ben Boeckel <mathstuf@gmail.com> - 0.8.3.0-1
- Update to 0.8.3.0

* Sat Jan 15 2011 Ben Boeckel <mathstuf@gmail.com> - 0.8.2.0-2
- Update to cabal2spec-0.22.4
- Rebuild

* Mon Nov 29 2010 Ben Boeckel <mathstuf@gmail.com> - 0.8.2.0-1
- Update to 0.8.2.0

* Mon Oct 18 2010 Ben Boeckel <mathstuf@gmail.com> - 0.8.1.1-1
- Update to 0.8.1.1

* Sat Sep 04 2010 Ben Boeckel <mathstuf@gmail.com> - 0.8.1.0-1
- Initial package

* Sat Sep  4 2010 Fedora Haskell SIG <haskell-devel@lists.fedoraproject.org> - 0.8.1.0-0
- initial packaging for Fedora automatically generated by cabal2spec-0.22.2
