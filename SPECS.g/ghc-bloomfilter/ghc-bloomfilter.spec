# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name bloomfilter

%bcond_with tests

Name:           ghc-%{pkg_name}
Version:        2.0.1.0
Release:        4%{?dist}
Summary:        Pure and impure Bloom Filter implementations

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
BuildRequires:  ghc-QuickCheck-devel
BuildRequires:  ghc-random-devel
BuildRequires:  ghc-test-framework-devel
BuildRequires:  ghc-test-framework-quickcheck2-devel
%endif
# End cabal-rpm deps

%description
Pure and impure Bloom Filter implementations.


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
%doc examples README.markdown


%changelog
* Fri Dec 04 2015 Liu Di <liudidi@gmail.com> - 2.0.1.0-4
- 为 Magic 3.0 重建

* Sun Nov 08 2015 Liu Di <liudidi@gmail.com> - 2.0.1.0-3
- 为 Magic 3.0 重建

* Sun Sep 20 2015 Liu Di <liudidi@gmail.com> - 2.0.1.0-2
- 为 Magic 3.0 重建

* Sat Aug 08 2015 Ben Boeckel <mathstuf@gmail.com> - 2.0.1.0-1
- update to 2.0.1.0

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Aug 28 2014 Jens Petersen <petersen@redhat.com> - 2.0.0.0-1
- update to 2.0.0.0
- refresh to cblrpm-0.8.11

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.6.10-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.6.10-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.6.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 07 2013 Jens Petersen <petersen@redhat.com> - 1.2.6.10-5
- update to new simplified Haskell Packaging Guidelines

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.6.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Nov 17 2012 Jens Petersen <petersen@redhat.com> - 1.2.6.10-3
- update with cabal-rpm

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.6.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 22 2012 Lakshmi Narasimhan T V <lakshminaras2002@gmail.com> - 1.2.6.10-1
- update to 1.2.6.10

* Sat Apr 14 2012 Lakshmi Narasimhan T V <lakshminaras2002@gmail.com> - 1.2.6.8-1
- spec file template generated by cabal2spec-0.25.5
- Package updated to 1.2.6.8

* Sun Jan 16 2011 Lakshmi Narasimhan T V <lakshminaras2002@gmail.com> - 1.2.6.7-1
- Initial package. License is BSD. Added summary and description

* Sun Jan 16 2011 Fedora Haskell SIG <haskell-devel@lists.fedoraproject.org> - 1.2.6.7-0
- initial packaging for Fedora automatically generated by cabal2spec-0.22.4
