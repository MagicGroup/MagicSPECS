# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name polyparse

Name:           ghc-%{pkg_name}
Version:        1.11
Release:        2%{?dist}
Summary:        A variety of alternative parser combinator libraries

License:        LGPLv2+
Url:            https://hackage.haskell.org/package/%{pkg_name}
Source0:        https://hackage.haskell.org/package/%{pkg_name}-%{version}/%{pkg_name}-%{version}.tar.gz

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
# Begin cabal-rpm deps:
BuildRequires:  ghc-bytestring-devel
BuildRequires:  ghc-text-devel
# End cabal-rpm deps

%description
A variety of alternative parser combinator libraries, including the original
HuttonMeijer set. The Poly sets have features like good error reporting,
arbitrary token type, running state, lazy parsing, and so on. Finally,
Text.Parse is a proposed replacement for the standard Read class, for better
deserialisation of Haskell values from Strings.


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


%post devel
%ghc_pkg_recache


%postun devel
%ghc_pkg_recache


%files -f %{name}.files
%doc COPYRIGHT


%files devel -f %{name}-devel.files


%changelog
* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Feb 27 2015 Fedora Haskell SIG <haskell@lists.fedoraproject.org> - 1.11-1
- spec file generated by cabal-rpm-0.9.4
