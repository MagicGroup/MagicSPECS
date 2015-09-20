# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name crypto-cipher-types

Name:           ghc-%{pkg_name}
Version:        0.0.9
Release:        7%{?dist}
Summary:        Generic cryptography cipher types

License:        BSD
Url:            https://hackage.haskell.org/package/%{pkg_name}
Source0:        https://hackage.haskell.org/package/%{pkg_name}-%{version}/%{pkg_name}-%{version}.tar.gz

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
# Begin cabal-rpm deps:
BuildRequires:  ghc-byteable-devel
BuildRequires:  ghc-bytestring-devel
BuildRequires:  ghc-securemem-devel
# End cabal-rpm deps

%description
Generic cryptography cipher types.


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
# README installed in the wrong place
rm $RPM_BUILD_ROOT%{_datadir}/%{pkg_name}-%{version}/README.md


%post devel
%ghc_pkg_recache


%postun devel
%ghc_pkg_recache


%files -f %{name}.files
%doc LICENSE


%files devel -f %{name}-devel.files
%doc README.md


%changelog
* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.9-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Feb 17 2015 Sébastien Willmann <sebastien.willmann@gmail.com> - 0.0.9-6
- Rebuild to fix broken deps

* Tue Jan 27 2015 Jens Petersen <petersen@fedoraproject.org> - 0.0.9-5
- update urls

* Tue Dec 30 2014 Sébastien Willmann <sebastien.willmann@gmail.com> - 0.0.9-4
- Rebuilt to fix broken deps

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Feb 15 2014 Fedora Haskell SIG <haskell@lists.fedoraproject.org> - 0.0.9-1
- spec file generated by cabal-rpm-0.8.7
- Removed README installed in the wrong place
