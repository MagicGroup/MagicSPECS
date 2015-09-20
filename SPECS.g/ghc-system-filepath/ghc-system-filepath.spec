# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name system-filepath

%bcond_with tests

Name:           ghc-%{pkg_name}
Version:        0.4.13.1
Release:        2%{?dist}
Summary:        File and directory path manipulations

License:        MIT
Url:            https://hackage.haskell.org/package/%{pkg_name}
Source0:        https://hackage.haskell.org/package/%{pkg_name}-%{version}/%{pkg_name}-%{version}.tar.gz

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
# Begin cabal-rpm deps:
BuildRequires:  ghc-bytestring-devel
BuildRequires:  ghc-deepseq-devel
BuildRequires:  ghc-text-devel
%if %{with tests}
BuildRequires:  ghc-QuickCheck-devel
BuildRequires:  ghc-chell-devel
BuildRequires:  ghc-chell-quickcheck-devel
%endif
# End cabal-rpm deps

%description
High-level, byte-based file and directory path manipulations.


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
%doc license.txt


%files devel -f %{name}-devel.files
%doc README.md


%changelog
* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.13.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jan 20 2015 Jens Petersen <petersen@redhat.com> - 0.4.13.1-1
- update to 0.4.13.1

* Wed Aug 27 2014 Jens Petersen <petersen@redhat.com> - 0.4.12-1
- update to 0.4.12
- refresh to cblrpm-0.8.11

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jun 27 2013 Jens Petersen <petersen@redhat.com> - 0.4.7-1
- simpler summary

* Thu Jun 27 2013 Fedora Haskell SIG <haskell@lists.fedoraproject.org> - 0.4.7-0
- spec file generated by cabal-rpm-0.8.2
