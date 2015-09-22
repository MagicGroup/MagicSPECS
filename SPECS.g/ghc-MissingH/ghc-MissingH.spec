# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name MissingH

%bcond_with tests

Name:           ghc-%{pkg_name}
Version:        1.3.0.1
Release:        3%{?dist}
Summary:        Large utility library

# src/Data/Hash/MD5.lhs is BSD or GPL+
# src/Data/Hash/CRC32/Posix.hs is GPL+
# src/System/Time/ParseDate.hs is GPLv2 (newer parsedate is now BSD)
# all other src/ (and testsrc/) files are BSD
License:        GPLv2+
Url:            https://hackage.haskell.org/package/%{pkg_name}
Source0:        https://hackage.haskell.org/package/%{pkg_name}-%{version}/%{pkg_name}-%{version}.tar.gz

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
# Begin cabal-rpm deps:
BuildRequires:  ghc-HUnit-devel
BuildRequires:  ghc-array-devel
BuildRequires:  ghc-containers-devel
BuildRequires:  ghc-directory-devel
BuildRequires:  ghc-filepath-devel
BuildRequires:  ghc-hslogger-devel
BuildRequires:  ghc-mtl-devel
BuildRequires:  ghc-network-devel
BuildRequires:  ghc-old-locale-devel
BuildRequires:  ghc-old-time-devel
BuildRequires:  ghc-parsec-devel
BuildRequires:  ghc-process-devel
BuildRequires:  ghc-random-devel
BuildRequires:  ghc-regex-compat-devel
BuildRequires:  ghc-time-devel
BuildRequires:  ghc-unix-devel
%if %{with tests}
BuildRequires:  ghc-QuickCheck-devel
BuildRequires:  ghc-errorcall-eq-instance-devel
BuildRequires:  ghc-testpack-devel
%endif
# End cabal-rpm deps

%description
MissingH is a library of all sorts of utility functions for Haskell
programmers. It is written in pure Haskell and thus should be extremely
portable and easy to use.


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
%doc LICENSE 3rd-party-licenses
%{_docdir}/%{name}-%{version}/LICENSE

%files devel -f %{name}-devel.files
%doc announcements TODO


%changelog
* Sun Sep 20 2015 Liu Di <liudidi@gmail.com> - 1.3.0.1-3
- 为 Magic 3.0 重建

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jan 20 2015 Jens Petersen <petersen@redhat.com> - 1.3.0.1-1
- update to 1.3.0.1

* Fri Aug 29 2014 Jens Petersen <petersen@redhat.com> - 1.2.1.0-1
- update to 1.2.1.0
- refresh to cblrpm-0.8.11

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jun 11 2013 Jens Petersen <petersen@redhat.com> - 1.2.0.0-3
- update to new simplified Haskell Packaging Guidelines

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Nov 07 2012 Jens Petersen <petersen@redhat.com> - 1.2.0.0-1
- update to 1.2.0.0

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Jens Petersen <petersen@redhat.com> - 1.1.1.0-4
- change prof BRs to devel

* Fri Jun 15 2012 Jens Petersen <petersen@redhat.com> - 1.1.1.0-3
- rebuild

* Wed Jan  4 2012 Jens Petersen <petersen@redhat.com> - 1.1.1.0-2
- update to cabal2spec-0.25.2

* Mon Oct 24 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.1.1.0-1.3
- rebuild with new gmp without compat lib

* Fri Oct 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.1.1.0-1.2
- rebuild with new gmp without compat lib

* Tue Oct 11 2011 Peter Schiffer <pschiffe@redhat.com> - 1.1.1.0-1.1
- rebuild with new gmp

* Mon Sep 26 2011 Jens Petersen <petersen@redhat.com> - 1.1.1.0-1
- update to 1.1.1.0
- most of the library modules now BSD

* Mon Aug 29 2011 Jens Petersen <petersen@redhat.com> - 1.1.0.3-9
- rebuild for hslogger-1.1.5

* Wed Jun 22 2011 Jens Petersen <petersen@redhat.com> - 1.1.0.3-8
- BR ghc-Cabal-devel instead of ghc-prof and use ghc_arches (cabal2spec-0.23.2)

* Thu Mar 10 2011 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.1.0.3-7
- Enable build on sparcv9

* Thu Feb 17 2011 Ben Boeckel <mathstuf@gmail.com> - 1.1.0.3-6
- Update for broken dependencies

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Jens Petersen <petersen@redhat.com> - 1.1.0.3-4
- rebuild (for hslogger-1.1.3)

* Sat Jan 15 2011 Ben Boeckel <mathstuf@gmail.com> - 1.1.0.3-3
- Update to cabal2spec-0.22.4
- Rebuild

* Wed Sep 22 2010 Jens Petersen <petersen@redhat.com> - 1.1.0.3-2
- use iconv to fix COPYRIGHT file encoding
- add license comments

* Sun Sep 05 2010 Ben Boeckel <mathstuf@gmail.com> - 1.1.0.3-1
- Initial package

* Sun Sep  5 2010 Fedora Haskell SIG <haskell-devel@lists.fedoraproject.org> - 1.1.0.3-0
- initial packaging for Fedora automatically generated by cabal2spec-0.22.2
