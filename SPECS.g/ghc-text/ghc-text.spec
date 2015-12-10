# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name text

%bcond_with tests

Name:           ghc-%{pkg_name}
# part of haskell-platform
Version:        1.1.1.3
Release:        5%{?dist}
Summary:        An efficient packed Unicode text type

License:        BSD
Url:            https://hackage.haskell.org/package/%{pkg_name}
Source0:        https://hackage.haskell.org/package/%{pkg_name}-%{version}/%{pkg_name}-%{version}.tar.gz

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
# Begin cabal-rpm deps:
BuildRequires:  ghc-array-devel
BuildRequires:  ghc-bytestring-devel
BuildRequires:  ghc-deepseq-devel
%if %{with tests}
BuildRequires:  ghc-HUnit-devel
BuildRequires:  ghc-QuickCheck-devel
BuildRequires:  ghc-directory-devel
BuildRequires:  ghc-random-devel
BuildRequires:  ghc-test-framework-devel
BuildRequires:  ghc-test-framework-hunit-devel
BuildRequires:  ghc-test-framework-quickcheck2-devel
%endif
# End cabal-rpm deps

%description
An efficient packed, immutable Unicode text type (both strict and lazy), with a
powerful loop fusion optimization framework.

The 'Text' type represents Unicode character strings, in a time and
space-efficient manner. This package provides text processing capabilities that
are optimized for performance critical use, both in terms of large data
quantities and high speed.

The 'Text' type provides character-encoding, type-safe case conversion via
whole-string case conversion functions. It also provides a range of functions
for converting 'Text' values to and from 'ByteStrings', using several standard
encodings.

Efficient locale-sensitive support for text IO is also supported.


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
%{_docdir}/%{name}-%{version}/LICENSE


%files devel -f %{name}-devel.files
%doc README.markdown


%changelog
* Fri Dec 04 2015 Liu Di <liudidi@gmail.com> - 1.1.1.3-5
- 为 Magic 3.0 重建

* Sun Nov 08 2015 Liu Di <liudidi@gmail.com> - 1.1.1.3-4
- 为 Magic 3.0 重建

* Sun Sep 20 2015 Liu Di <liudidi@gmail.com> - 1.1.1.3-3
- 为 Magic 3.0 重建

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jan 19 2015 Jens Petersen <petersen@redhat.com> - 1.1.1.3-1
- update to 1.1.1.3

* Fri Aug  8 2014 Jens Petersen <petersen@redhat.com> - 1.1.0.0-1
- update to 1.1.0.0

* Mon Jun  9 2014 Jens Petersen <petersen@redhat.com> - 0.11.3.1-3
- rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri May 17 2013 Jens Petersen <petersen@redhat.com> - 0.11.3.1-1
- package revived for updating to HP-2013.2
- spec file updated with cabal-rpm-0.8.0

* Tue Mar 20 2012 Jens Petersen <petersen@redhat.com> - 0.11.1.13-1
- update to 0.11.1.13

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 28 2011 Jens Petersen <petersen@redhat.com> - 0.11.1.5-1
- update to 0.11.1.5 for haskell-platform-2011.4.0.0
- update to cabal2spec-0.25.1

* Mon Oct 24 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.11.0.6-2.3
- rebuild with new gmp without compat lib

* Fri Oct 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.11.0.6-2.2
- rebuild with new gmp without compat lib

* Tue Oct 11 2011 Peter Schiffer <pschiffe@redhat.com> - 0.11.0.6-2.1
- rebuild with new gmp

* Tue Jun 21 2011 Jens Petersen <petersen@redhat.com> - 0.11.0.6-2
- ghc_arches replaces ghc_excluded_archs

* Mon Jun 20 2011 Jens Petersen <petersen@redhat.com> - 0.11.0.6-1
- update to 0.11.0.6 (haskell-platform-2011.1.0.1)
- BR ghc-Cabal-devel and depends

* Fri May 27 2011 Jens Petersen <petersen@redhat.com> - 0.11.0.5-3
- update to cabal2spec-0.23: add ppc64

* Thu Mar 10 2011 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.11.0.5-2
- Enable build on sparcv9

* Tue Feb 15 2011 Jens Petersen <petersen@redhat.com> - 0.11.0.5-1
- update to 0.11.0.5 for haskell-platform-2011.1

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 17 2011 Jens Petersen <petersen@redhat.com> - 0.11.0.0-2
- update to cabal2spec-0.22.4

* Sun Dec  5 2010 Jens Petersen <petersen@redhat.com> - 0.11.0.0-1
- update to 0.11.0.0

* Thu Nov 25 2010 Jens Petersen <petersen@redhat.com> - 0.10.0.0-2
- rebuild

* Mon Nov  1 2010 Jens Petersen <petersen@redhat.com> - 0.10.0.0-1
- update to 0.10.0.0
- README renamed to README.markdown

* Wed Sep 29 2010 jkeating - 0.8.1.0-2
- Rebuilt for gcc bug 634757

* Wed Sep  1 2010 Jens Petersen <petersen@redhat.com> - 0.8.0.0-1
- update to 0.8.0.0
- include README in devel

* Sat Jul 31 2010 Jens Petersen <petersen@redhat.com> - 0.7.2.1-1
- BSD license
- requires deepseq

* Sat Jul 31 2010 Fedora Haskell SIG <haskell-devel@lists.fedoraproject.org> - 0.7.2.1-0
- initial packaging for Fedora automatically generated by cabal2spec-0.22.2
