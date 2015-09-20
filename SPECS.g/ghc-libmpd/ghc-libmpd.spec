# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name libmpd

%bcond_with tests

Name:           ghc-%{pkg_name}
Version:        0.9.0.2
Release:        1%{?dist}
Summary:        Haskell MPD client library

License:        MIT
Url:            https://hackage.haskell.org/package/%{pkg_name}
Source0:        https://hackage.haskell.org/package/%{pkg_name}-%{version}/%{pkg_name}-%{version}.tar.gz

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
# Begin cabal-rpm deps:
BuildRequires:  ghc-attoparsec-devel
BuildRequires:  ghc-bytestring-devel
BuildRequires:  ghc-containers-devel
BuildRequires:  ghc-data-default-class-devel
BuildRequires:  ghc-filepath-devel
BuildRequires:  ghc-mtl-devel
BuildRequires:  ghc-network-devel
BuildRequires:  ghc-old-locale-devel
BuildRequires:  ghc-text-devel
BuildRequires:  ghc-time-devel
BuildRequires:  ghc-utf8-string-devel
%if %{with tests}
BuildRequires:  ghc-QuickCheck-devel
BuildRequires:  ghc-hspec-devel
BuildRequires:  ghc-unix-devel
%endif
# End cabal-rpm deps

%description
A client library for MPD, the Music Player Daemon (<http://www.musicpd.org/>).


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
%doc README.md


%changelog
* Sun Jul 19 2015 Ben Boeckel <mathstuf@gmail.com> - 0.9.0.2-1
- Update to 0.9.0.2

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Aug 27 2014 Jens Petersen <petersen@redhat.com> - 0.8.0.5-1
- update to 0.8.0.5

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jun 10 2014 Jens Petersen <petersen@redhat.com> - 0.8.0.2-5
- update to cblrpm-0.8.11

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jun 05 2013 Jens Petersen <petersen@redhat.com> - 0.8.0.2-2
- update to new simplified Haskell Packaging Guidelines

* Tue Mar 12 2013 Jens Petersen <petersen@redhat.com> - 0.8.0.2-1
- update to 0.8.0.2

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Nov 17 2012 Jens Petersen <petersen@redhat.com> - 0.7.2-6
- update with cabal-rpm

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Jens Petersen <petersen@redhat.com> - 0.7.2-4
- change prof BRs to devel

* Sat Jun  9 2012 Jens Petersen <petersen@redhat.com> - 0.7.2-3
- allow building with mtl-2.1

* Thu Mar 22 2012 Jens Petersen <petersen@redhat.com> - 0.7.2-2
- add license to ghc_files

* Tue Feb 28 2012 Ben Boeckel <mathstuf@gmail.com> - 0.7.2-1
- Update to 0.7.2

* Wed Jan  4 2012 Jens Petersen <petersen@redhat.com> - 0.7.0-1
- update to 0.7.0 and cabal2spec-0.25.2

* Mon Oct 24 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.5.0-9.3
- rebuild with new gmp without compat lib

* Fri Oct 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.5.0-9.2
- rebuild with new gmp without compat lib

* Tue Oct 11 2011 Peter Schiffer <pschiffe@redhat.com> - 0.5.0-9.1
- rebuild with new gmp

* Thu Jun 23 2011 Jens Petersen <petersen@redhat.com> - 0.5.0-9
- BR ghc-Cabal-devel instead of ghc-prof and use ghc_arches (cabal2spec-0.23.2)

* Thu Mar 10 2011 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.5.0-8
- Enable build on sparcv9

* Thu Feb 17 2011 Ben Boeckel <mathstuf@gmail.com> - 0.5.0-7
- Rebuild for broken dependencies (ghc-network)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 15 2011 Ben Boeckel <mathstuf@gmail.com> - 0.5.0-5
- Update to cabal2spec-0.22.4
- Rebuild

* Sun Dec  5 2010 Jens Petersen <petersen@redhat.com> - 0.5.0-4
- also bump network dependency

* Mon Nov 29 2010 Jens Petersen <petersen@redhat.com> - 0.5.0-3
- bump some core dependency versions for ghc7

* Sun Nov 28 2010 Ben Boeckel <mathstuf@gmail.com> - 0.5.0-2
- Rebuild for GHC7

* Sun Oct 31 2010 Ben Boeckel <mathstuf@gmail.com> - 0.5.0-1
- Update to 0.5.0

* Wed Sep 01 2010 Ben Boeckel <mathstuf@gmail.com> - 0.4.2-1
- Update to 0.4.2
- Drop QuickCheck BR
- Ship the changelog and readme as well

* Tue Aug 31 2010 Ben Boeckel <mathstuf@gmail.com> - 0.4.1-1
- Initial package

* Tue Aug 31 2010 Fedora Haskell SIG <haskell-devel@lists.fedoraproject.org> - 0.4.1-0
- initial packaging for Fedora automatically generated by cabal2spec-0.22.2
