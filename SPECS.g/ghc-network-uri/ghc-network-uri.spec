# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name network-uri

%bcond_with tests

Name:           ghc-%{pkg_name}
Version:        2.6.0.3
Release:        3%{?dist}
Summary:        URI manipulation

License:        BSD
Url:            https://hackage.haskell.org/package/%{pkg_name}
Source0:        https://hackage.haskell.org/package/%{pkg_name}-%{version}/%{pkg_name}-%{version}.tar.gz

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
# Begin cabal-rpm deps:
BuildRequires:  ghc-deepseq-devel
BuildRequires:  ghc-parsec-devel
%if %{with tests}
BuildRequires:  ghc-HUnit-devel
BuildRequires:  ghc-test-framework-devel
BuildRequires:  ghc-test-framework-hunit-devel
BuildRequires:  ghc-test-framework-quickcheck2-devel
%endif
# End cabal-rpm deps

%description
This package provides an URI manipulation interface.


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
rm -vf %{buildroot}%{_docdir}/%{name}/LICENSE
rmdir -v %{buildroot}%{_docdir}/%{name}


%check
%if %{with tests}
%cabal test
%endif


%post devel
%ghc_pkg_recache


%postun devel
%ghc_pkg_recache


%files -f %{name}.files
%license LICENSE


%files devel -f %{name}-devel.files


%changelog
* Sun Sep 20 2015 Liu Di <liudidi@gmail.com> - 2.6.0.3-3
- 为 Magic 3.0 重建

* Wed Sep 09 2015 Ben Boeckel <mathstuf@gmail.com> - 2.6.0.3-2
- fedora import

* Sun Aug 23 2015 Ben Boeckel <mathstuf@gmail.com> - 2.6.0.3-1
- initial package
