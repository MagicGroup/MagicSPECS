# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name setlocale

Name:           ghc-%{pkg_name}
Version:        1.0.0.3
Release:        1%{?dist}
Summary:        A Haskell interface to setlocale

License:        BSD
Url:            https://hackage.haskell.org/package/%{pkg_name}
Source0:        https://hackage.haskell.org/package/%{pkg_name}-%{version}/%{pkg_name}-%{version}.tar.gz

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros

%description
A Haskell interface to 'setlocale()'.


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
%doc LICENSE


%files devel -f %{name}-devel.files


%changelog
* Thu Jun 25 2015 Philip Withnall <philip@tecnocode.co.uk> - 1.0.0.3-1
- Update to 1.0.0.3

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jan 27 2015 Jens Petersen <petersen@redhat.com> - 1.0.0.1-3
- cblrpm refresh

* Fri Dec 12 2014 Philip Withnall <philip@tecnocode.co.uk> - 1.0.0.1-2
- Rebuilt for libHSbase changes

* Thu Sep 11 2014 Philip Withnall <philip@tecnocode.co.uk> - 1.0.0.1-1
- Update to 1.0.0.1

* Thu Aug 28 2014 Philip Withnall <philip@tecnocode.co.uk> - 1.0.0-1
- Update to 1.0.0 (rewrite due to licencing issues)

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 28 2014 Philip Withnall <philip@tecnocode.co.uk> - 0.0.3-1
- spec file generated by cabal-rpm-0.8.11
