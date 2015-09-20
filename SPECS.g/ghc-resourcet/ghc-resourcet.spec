# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name resourcet

%bcond_with tests

Name:           ghc-%{pkg_name}
Version:        1.1.4.1
Release:        2%{?dist}
Summary:        Deterministic allocation and freeing of scarce resources

License:        BSD
Url:            https://hackage.haskell.org/package/%{pkg_name}
Source0:        https://hackage.haskell.org/package/%{pkg_name}-%{version}/%{pkg_name}-%{version}.tar.gz

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
# Begin cabal-rpm deps:
BuildRequires:  ghc-containers-devel
BuildRequires:  ghc-exceptions-devel
BuildRequires:  ghc-lifted-base-devel
BuildRequires:  ghc-mmorph-devel
BuildRequires:  ghc-monad-control-devel
BuildRequires:  ghc-mtl-devel
BuildRequires:  ghc-transformers-base-devel
BuildRequires:  ghc-transformers-compat-devel
BuildRequires:  ghc-transformers-devel
%if %{with tests}
BuildRequires:  ghc-hspec-devel
%endif
# End cabal-rpm deps

%description
Allocate resources which are guaranteed to be released.
All register cleanup actions live in the IO monad, not the main monad.
This allows both more efficient code, and for monads to be transformed.


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
* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Mar 03 2015 Jens Petersen <petersen@redhat.com> - 1.1.4.1-1
- update to 1.1.4.1

* Tue Jan 27 2015 Jens Petersen <petersen@fedoraproject.org> - 0.4.10.2-4
- cblrpm refresh

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.10.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.10.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 08 2014 Jens Petersen <petersen@redhat.com> - 0.4.10.2-1
- update to 0.4.10.2
- update packaging to cabal-rpm-0.8.10

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 10 2013 Jens Petersen <petersen@redhat.com> - 0.4.6-1
- update to 0.4.6
- update to new simplified Haskell Packaging Guidelines

* Mon Mar 11 2013 Jens Petersen <petersen@redhat.com> - 0.4.5-1
- update to 0.4.5

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Nov 07 2012 Jens Petersen <petersen@redhat.com> - 0.4.0.2-1
- update to 0.4.0.2

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Jens Petersen <petersen@redhat.com> - 0.3.2.2-1
- update to 0.3.2.2

* Tue May  1 2012 Jens Petersen <petersen@redhat.com> - 0.3.2.1-1
- update to 0.3.2.1

* Tue Apr 10 2012 Jens Petersen <petersen@redhat.com> - 0.3.2-1
- update to 0.3.2

* Sat Mar 24 2012 Jens Petersen <petersen@redhat.com> - 0.3.1-1
- BSD
- depends on lifted-base and containers

* Sat Mar 24 2012 Fedora Haskell SIG <haskell-devel@lists.fedoraproject.org>
- spec file template generated by cabal2spec-0.25.4