# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name yesod-routes

%bcond_with tests

# no useful debuginfo for Haskell packages without C sources
%global debug_package %{nil}

Name:           ghc-%{pkg_name}
Version:        1.2.0.7
Release:        4%{?dist}
Summary:        Efficient routing for Yesod

License:        MIT
URL:            http://hackage.haskell.org/package/%{pkg_name}
Source0:        http://hackage.haskell.org/package/%{pkg_name}-%{version}/%{pkg_name}-%{version}.tar.gz

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
# Begin cabal-rpm deps:
BuildRequires:  ghc-containers-devel
BuildRequires:  ghc-path-pieces-devel
BuildRequires:  ghc-template-haskell-devel
BuildRequires:  ghc-text-devel
BuildRequires:  ghc-vector-devel
ExclusiveArch:  %{ghc_arches_with_ghci}
%if %{with tests}
BuildRequires:  ghc-HUnit-devel
BuildRequires:  ghc-bytestring-devel
BuildRequires:  ghc-hspec-devel
%endif
# End cabal-rpm deps

%description
Provides an efficient routing system, a parser and TH code generation.


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


%changelog
* Sun Nov 08 2015 Liu Di <liudidi@gmail.com> - 1.2.0.7-4
- 为 Magic 3.0 重建

* Sun Sep 20 2015 Liu Di <liudidi@gmail.com> - 1.2.0.7-3
- 为 Magic 3.0 重建

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Aug 28 2014 Jens Petersen <petersen@redhat.com> - 1.2.0.7-1
- update to 1.2.0.7
- refresh to cblrpm-0.8.11

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 16 2013 Fedora Haskell SIG <haskell@lists.fedoraproject.org> - 1.2.0.1-1
- spec file generated by cabal-rpm-0.8.3
