# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name snap-core

Name:           ghc-%{pkg_name}
Version:        0.9.6.4
Release:        3%{?dist}
Summary:        Snap web framework core library

License:        BSD
Url:            https://hackage.haskell.org/package/%{pkg_name}
Source0:        https://hackage.haskell.org/package/%{pkg_name}-%{version}/%{pkg_name}-%{version}.tar.gz

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
# Begin cabal-rpm deps:
BuildRequires:  ghc-HUnit-devel
BuildRequires:  ghc-MonadCatchIO-transformers-devel
BuildRequires:  ghc-attoparsec-devel
BuildRequires:  ghc-attoparsec-enumerator-devel
BuildRequires:  ghc-blaze-builder-devel
BuildRequires:  ghc-blaze-builder-enumerator-devel
BuildRequires:  ghc-bytestring-devel
BuildRequires:  ghc-case-insensitive-devel
BuildRequires:  ghc-containers-devel
BuildRequires:  ghc-deepseq-devel
BuildRequires:  ghc-directory-devel
BuildRequires:  ghc-enumerator-devel
BuildRequires:  ghc-filepath-devel
BuildRequires:  ghc-hashable-devel
BuildRequires:  ghc-mtl-devel
BuildRequires:  ghc-old-locale-devel
BuildRequires:  ghc-random-devel
BuildRequires:  ghc-regex-posix-devel
BuildRequires:  ghc-text-devel
BuildRequires:  ghc-time-devel
BuildRequires:  ghc-unix-compat-devel
BuildRequires:  ghc-unordered-containers-devel
BuildRequires:  ghc-vector-devel
BuildRequires:  ghc-zlib-enum-devel
# End cabal-rpm deps
Patch1:         snap-core-0.9.2.2-portable-flag.patch

%description
Snap is a simple and fast web development framework and server written
in Haskell.  This library contains the core definitions and types for
the Snap framework.


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
%patch1 -p1 -b .orig


%build
%ghc_lib_build


# requires pureMD5 and test-framework*
#%%check
#cd test
#../Setup configure
#../Setup build
#./runTestsAndCoverage.sh


%install
%ghc_lib_install


%post devel
%ghc_pkg_recache


%postun devel
%ghc_pkg_recache


%files -f %{name}.files
%doc LICENSE
%{_docdir}/%{name}-%{version}/LICENSE

%files devel -f %{name}-devel.files
%doc CONTRIBUTORS README*.md


%changelog
* Sun Sep 20 2015 Liu Di <liudidi@gmail.com> - 0.9.6.4-3
- 为 Magic 3.0 重建

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.6.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jan 20 2015 Jens Petersen <petersen@redhat.com> - 0.9.6.4-1
- update to 0.9.6.4

* Mon Sep 01 2014 Jens Petersen <petersen@redhat.com> - 0.9.6.3-1
- update to 0.9.6.3
- refresh to clrpm-0.8.11

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jun 11 2013 Jens Petersen <petersen@redhat.com> - 0.9.4.0-1
- update to 0.9.4.0
- update to new simplified Haskell Packaging Guidelines

* Tue Mar 12 2013 Jens Petersen <petersen@redhat.com> - 0.9.3.1-1
- update to 0.9.3.1

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct 29 2012 Jens Petersen <petersen@redhat.com> - 0.9.2.2-1
- update to 0.9.2.2
- compile in portable cross-platform mode until bytestring-mmap packaged

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Jens Petersen <petersen@redhat.com> - 0.9.0-3
- change prof BRs to devel

* Fri Jun 22 2012 Jens Petersen <petersen@redhat.com> - 0.9.0-2
- rebuild

* Thu Jun 21 2012 Jens Petersen <petersen@redhat.com> - 0.9.0-1
- update to 0.9.0

* Fri Jun 15 2012 Jens Petersen <petersen@redhat.com> - 0.8.1-2
- rebuild

* Tue May  1 2012 Jens Petersen <petersen@redhat.com> - 0.8.1-1
- update to 0.8.1

* Fri Mar 23 2012 Jens Petersen <petersen@redhat.com> - 0.8.0.1-1
- update to 0.8.0.1
- mwc-random version patch no longer needed

* Thu Mar  8 2012 Jens Petersen <petersen@redhat.com> - 0.7.0.1-2
- rebuild

* Mon Jan 16 2012 Jens Petersen <petersen@redhat.com> - 0.7.0.1-1
- update to 0.7.0.1 and cabal2spec-0.25.2
- add some doc files
- allow building with mwc-random-0.11

* Fri Dec 16 2011 Jens Petersen <petersen@redhat.com> - 0.6.0.1-1
- update to 0.6.0.1
- new deps base16-bytestring, mwc-random, unordered-containers,
  regex-posix, and HUnit

* Tue Nov 22 2011 Jens Petersen <petersen@redhat.com> - 0.5.5-1
- update to 0.5.5
- depends on zlib-enum and blaze-builder-enumerator

* Tue Nov  8 2011 Jens Petersen <petersen@redhat.com> - 0.5.4-2
- add missed mtl dep

* Sat Oct 15 2011 Jens Petersen <petersen@redhat.com> - 0.5.4-1
- update to 0.5.4

* Thu Sep  8 2011 Jens Petersen <petersen@redhat.com> - 0.5.3.1-1
- BSD license and deps

* Thu Sep  8 2011 Fedora Haskell SIG <haskell-devel@lists.fedoraproject.org> - 0.5.3.1-0
- initial packaging for Fedora automatically generated by cabal2spec-0.24.1
