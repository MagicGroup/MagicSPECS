# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name primes

Name:           ghc-%{pkg_name}
Version:        0.2.1.0
Release:        11%{?dist}
Summary:        Efficient, purely functional generation of prime numbers

License:        BSD
Url:            https://hackage.haskell.org/package/%{pkg_name}
Source0:        https://hackage.haskell.org/package/%{pkg_name}-%{version}/%{pkg_name}-%{version}.tar.gz

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros

%description
This Haskell library provides an efficient lazy wheel sieve for
prime generation inspired by "Lazy wheel sieves and spirals of primes"
by Colin Runciman and "The Genuine Sieve of Eratosthenes" by Melissa O'Neil.

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
# Remove LICENSE file until clarification
%if 0%{?fedora} > 19
rm -f ${RPM_BUILD_ROOT}%{_docdir}/%{name}/LICENSE
%else
rm -f ${RPM_BUILD_ROOT}%{_docdir}/%{name}-%{version}/LICENSE
%endif

%post devel
%ghc_pkg_recache

%postun devel
%ghc_pkg_recache

%files -f %{name}.files
# %doc LICENSE
%{_docdir}/%{name}-%{version}/LICENSE


%files devel -f %{name}-devel.files

%changelog
* Sun Nov 08 2015 Liu Di <liudidi@gmail.com> - 0.2.1.0-11
- 为 Magic 3.0 重建

* Sun Sep 20 2015 Liu Di <liudidi@gmail.com> - 0.2.1.0-10
- 为 Magic 3.0 重建

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Feb 15 2015 Jochen Schmitt <Jochen herr-schmitt de> - 0.2.1.0-8
- Rebult to fix an dependency issues agains ghc(base)

* Wed Feb 11 2015 Jochen Schmitt <Jochen herr-schmitt de> - 0.2.1.0-7
- Rebuilt for new ghc release

* Tue Feb  3 2015 Jens Petersen <petersen@redhat.com> - 0.2.1.0-6
- update urls for rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Oct 18 2013 Jochen Schmitt <Jochen herr-schmitt de> - 0.2.1.0-3
- Fix license tag
- Add Provides %%{name}-static in the devel subpackage
- Remove LICENSE file until clarification

* Wed Oct 16 2013 Jochen Schmitt <Jochen herr-schmitt de> - 0.2.1.0-2
- Cleanup description
- Add %%{?_isa} macro in Req. 

* Tue Oct  8 2013 Jochen Schmitt <Jochen herr-schmitt de> - 0.2.1.0-1
- Initial package

