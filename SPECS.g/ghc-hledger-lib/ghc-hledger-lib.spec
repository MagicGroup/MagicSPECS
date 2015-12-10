# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name hledger-lib

%bcond_with tests

Name:           ghc-%{pkg_name}
Version:        0.24
Release:        5%{?dist}
Summary:        Core data types, parsers and utilities for the hledger accounting tool

License:        GPLv3
URL:            http://hackage.haskell.org/package/%{pkg_name}
Source0:        http://hackage.haskell.org/package/%{pkg_name}-%{version}/%{pkg_name}-%{version}.tar.gz
# rhbz(974725)
Patch0:         hledger-lib-0.24-no-pretty-show.patch

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
# Begin cabal-rpm deps:
BuildRequires:  ghc-Decimal-devel
BuildRequires:  ghc-HUnit-devel
BuildRequires:  ghc-array-devel
BuildRequires:  ghc-blaze-markup-devel
BuildRequires:  ghc-bytestring-devel
BuildRequires:  ghc-cmdargs-devel
BuildRequires:  ghc-containers-devel
BuildRequires:  ghc-csv-devel
BuildRequires:  ghc-directory-devel
BuildRequires:  ghc-filepath-devel
BuildRequires:  ghc-mtl-devel
BuildRequires:  ghc-old-locale-devel
BuildRequires:  ghc-old-time-devel
BuildRequires:  ghc-parsec-devel
#BuildRequires:  ghc-pretty-show-devel
BuildRequires:  ghc-regex-tdfa-devel
BuildRequires:  ghc-regexpr-devel
BuildRequires:  ghc-safe-devel
BuildRequires:  ghc-split-devel
BuildRequires:  ghc-time-devel
BuildRequires:  ghc-transformers-devel
BuildRequires:  ghc-utf8-string-devel
%if %{with tests}
BuildRequires:  ghc-test-framework-devel
BuildRequires:  ghc-test-framework-hunit-devel
%endif
# End cabal-rpm deps

%description
Hledger is a library and set of user tools for working with financial data (or
anything that can be tracked in a double-entry accounting ledger.) It is a
haskell port and friendly fork of John Wiegley's Ledger. hledger provides
command-line, curses and web interfaces, and aims to be a reliable, practical
tool for daily use.


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
%patch0 -p1 -b .no-pretty-show


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


%changelog
* Fri Dec 04 2015 Liu Di <liudidi@gmail.com> - 0.24-5
- 为 Magic 3.0 重建

* Sun Sep 20 2015 Liu Di <liudidi@gmail.com> - 0.24-4
- 为 Magic 3.0 重建

* Sat Aug 08 2015 Ben Boeckel <mathstuf@gmail.com> - 0.24-3
- rebuild for ghc-safe bump

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Mar 01 2015 Ben Boeckel <mathstuf@gmail.com> - 0.24-1
- update to 0.24
- cblrpm refresh

* Fri Aug 29 2014 Jens Petersen <petersen@redhat.com> - 0.23.2-1
- update to 0.23.2
- patch out pretty-show until available in Fedora

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jun 12 2013 Jens Petersen <petersen@redhat.com> - 0.19.3-1
- update to 0.19.3
- update to new simplified Haskell Packaging Guidelines

* Fri Mar 22 2013 Jens Petersen <petersen@redhat.com> - 0.17-9
- rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov  9 2012 Jens Petersen <petersen@redhat.com> - 0.17-7
- allow building with cmdargs 0.10 and split 0.2

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Jens Petersen <petersen@redhat.com> - 0.17-5
- change prof BRs to devel

* Fri Jun 22 2012 Jens Petersen <petersen@redhat.com> - 0.17-4
- rebuild

* Sat Jun 16 2012 Jens Petersen <petersen@redhat.com> - 0.17-3
- rebuild

* Thu Mar 22 2012 Jens Petersen <petersen@redhat.com> - 0.17-2
- add license to ghc_files

* Tue Feb 28 2012 Ben Boeckel <mathstuf@gmail.com> - 0.17-1
- Update to 0.17

* Wed Jan  4 2012 Jens Petersen <petersen@redhat.com> - 0.16.1-1
- update to 0.16.1 and cabal2spec-0.25.2

* Mon Oct 24 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.16-1.1
- rebuild with new gmp without compat lib

* Mon Oct  3 2011 Jens Petersen <petersen@redhat.com> - 0.16-1
- update to 0.16
- new dependency on ghc-cmdargs

* Mon Oct  3 2011 Jens Petersen <petersen@redhat.com> - 0.14-2
- BR ghc-*-prof not devel

* Sat Jul 09 2011 Ben Boeckel <mathstuf@gmail.com> - 0.14-1
- Update to 0.14 and cabal2spec-0.24

* Fri Dec 10 2010 Ben Boeckel <mathstuf@gmail.com> - 0.13-1
- Update to 0.13

* Fri Dec 03 2010 Ben Boeckel <mathstuf@gmail.com> - 0.12.98-1
- Update to snapshot (0.12.98)

* Sat Oct 30 2010 Ben Boeckel <mathstuf@gmail.com> - 0.12.1-1
- Update to 0.12.1

* Sun Sep 05 2010 Ben Boeckel <mathstuf@gmail.com> - 0.12-1
- Update to 0.12

* Fri Sep 03 2010 Ben Boeckel <mathstuf@gmail.com> - 0.11.1-1
- Initial package

* Fri Sep  3 2010 Fedora Haskell SIG <haskell-devel@lists.fedoraproject.org> - 0.11.1-0
- initial packaging for Fedora automatically generated by cabal2spec-0.22.2
