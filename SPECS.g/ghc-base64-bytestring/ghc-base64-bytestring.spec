# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name base64-bytestring

%bcond_with tests

Name:           ghc-%{pkg_name}
Version:        1.0.0.1
Release:        8%{?dist}
Summary:        Fast base64 encoding and decoding for ByteStrings

License:        BSD
Url:            https://hackage.haskell.org/package/%{pkg_name}
Source0:        https://hackage.haskell.org/package/%{pkg_name}-%{version}/%{pkg_name}-%{version}.tar.gz

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
# Begin cabal-rpm deps:
BuildRequires:  ghc-bytestring-devel
%if %{with tests}
BuildRequires:  ghc-HUnit-devel
BuildRequires:  ghc-QuickCheck-devel
BuildRequires:  ghc-containers-devel
BuildRequires:  ghc-test-framework-devel
BuildRequires:  ghc-test-framework-hunit-devel
BuildRequires:  ghc-test-framework-quickcheck2-devel
%endif
# End cabal-rpm deps

%description
Fast base64 encoding and decoding for ByteStrings.


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
%doc README.markdown


%changelog
* Sun Sep 20 2015 Liu Di <liudidi@gmail.com> - 1.0.0.1-8
- 为 Magic 3.0 重建

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jan 28 2015 Jens Petersen <petersen@redhat.com> - 1.0.0.1-6
- cblrpm refresh

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 07 2013 Jens Petersen <petersen@redhat.com> - 1.0.0.1-2
- update to new simplified Haskell Packaging Guidelines

* Mon Mar 11 2013 Jens Petersen <petersen@redhat.com> - 1.0.0.1-1
- update to 1.0.0.1

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 06 2012 Jens Petersen <petersen@redhat.com> - 1.0.0.0-1
- update to 1.0.0.0

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 19 2012 Ben Boeckel <mathstuf@gmail.com> - 0.1.1.3-1
- Update to 0.1.1.3

* Thu Mar 22 2012 Jens Petersen <petersen@redhat.com> - 0.1.1.1-1
- update to 0.1.1.1

* Tue Feb  7 2012 Jens Petersen <petersen@redhat.com> - 0.1.1.0-1
- update to 0.1.1.0

* Wed Jan  4 2012 Jens Petersen <petersen@redhat.com> - 0.1.0.3-1
- update to 0.1.0.3 and cabal2spec-0.25.2
- add README file

* Mon Oct 24 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.1.0.2-7.3
- rebuild with new gmp without compat lib

* Thu Oct 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.1.0.2-7.2
- rebuild with new gmp without compat lib

* Tue Oct 11 2011 Peter Schiffer <pschiffe@redhat.com> - 0.1.0.2-7.1
- rebuild with new gmp

* Sat Jul 09 2011 Ben Boeckel <mathstuf@gmail.com> - 0.1.0.2-7
- Update to cabal2spec-0.24

* Fri Jun 24 2011 Jens Petersen <petersen@redhat.com> - 0.1.0.2-6
- BR ghc-Cabal-devel instead of ghc-prof and use ghc_arches (cabal2spec-0.23.2)

* Wed May 11 2011 Ben Boeckel <mathstuf@gmail.com> - 0.1.0.2-5
- Update to cabal2spec-0.22.7

* Tue May 10 2011 Ben Boeckel <mathstuf@gmail.com> - 0.1.0.2-4
- Update to cabal2spec-0.22.6

* Tue May 10 2011 Ben Boeckel <mathstuf@gmail.com> - 0.1.0.2-3
- Update to cabal2spec-0.22.5

* Thu Mar 10 2011 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.1.0.2-2
- Enable build on sparcv9

* Thu Feb 17 2011 Ben Boeckel <mathstuf@gmail.com> - 0.1.0.2-1
- Update to 0.1.0.2

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 15 2011 Ben Boeckel <mathstuf@gmail.com> - 0.1.0.1-3
- Update to cabal2spec-0.22.4
- Rebuild

* Mon Nov 29 2010 Ben Boeckel <mathstuf@gmail.com> - 0.1.0.1-2
- Fix spelling in summary

* Sat Oct 30 2010 Ben Boeckel <mathstuf@gmail.com> - 0.1.0.1-1
- Initial package

* Sat Oct 30 2010 Fedora Haskell SIG <haskell-devel@lists.fedoraproject.org> - 0.1.0.1-0
- initial packaging for Fedora automatically generated by cabal2spec-0.22.2
