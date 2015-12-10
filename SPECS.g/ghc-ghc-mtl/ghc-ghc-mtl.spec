# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name ghc-mtl

Name:           ghc-%{pkg_name}
Version:        1.2.1.0
Release:        9%{?dist}
Summary:        A mtl compatible with GHC-API monads and monad-transformers

License:        BSD
Url:            https://hackage.haskell.org/package/%{pkg_name}
Source0:        https://hackage.haskell.org/package/%{pkg_name}-%{version}/%{pkg_name}-%{version}.tar.gz

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
# Begin cabal-rpm deps:
BuildRequires:  ghc-exceptions-devel
BuildRequires:  ghc-extensible-exceptions-devel
BuildRequires:  ghc-ghc-devel
BuildRequires:  ghc-mtl-devel
# End cabal-rpm deps

%description
Provides an 'mtl' compatible version of the 'GhcT' monad-transformer defined in
the 'GHC-API' since version 6.10.1.


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
%{_docdir}/%{name}-%{version}/LICENSE


%files devel -f %{name}-devel.files


%changelog
* Fri Dec 04 2015 Liu Di <liudidi@gmail.com> - 1.2.1.0-9
- 为 Magic 3.0 重建

* Sun Nov 08 2015 Liu Di <liudidi@gmail.com> - 1.2.1.0-8
- 为 Magic 3.0 重建

* Sun Sep 20 2015 Liu Di <liudidi@gmail.com> - 1.2.1.0-7
- 为 Magic 3.0 重建

* Tue Sep  1 2015 Peter Robinson <pbrobinson@fedoraproject.org> 1.2.1.0-6
- Rebuild (aarch64 vector hashes)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jan 27 2015 Jens Petersen <petersen@fedoraproject.org> - 1.2.1.0-4
- cblrpm refresh

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 16 2014 Jens Petersen <petersen@redhat.com> - 1.2.1.0-1
- update to 1.2.1.0

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 07 2013 Jens Petersen <petersen@redhat.com> - 1.0.1.2-2
- update to new simplified Haskell Packaging Guidelines

* Tue Mar 12 2013 Jens Petersen <petersen@redhat.com> - 1.0.1.2-1
- update to 1.0.1.2

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Nov 17 2012 Jens Petersen <petersen@redhat.com> - 1.0.1.1-3
- update with cabal-rpm

* Mon Oct 01 2012 Lakshmi Narasimhan T V <lakshminaras2002@gmail.com> - 1.0.1.1-2
- rebuild for ghc-7.4.1

* Sun Jul 15 2012 Lakshmi Narasimhan T V <lakshminaras2002@gmail.com> - 1.0.1.1-1
- spec file template generated by cabal2spec-0.25.5

* Fri Jun 10 2011 Lakshmi Narasimhan T V <lakshminaras2002@gmail.com> - 1.0.1.0-1
- License is BSD 3 clause. Added dependencies.
