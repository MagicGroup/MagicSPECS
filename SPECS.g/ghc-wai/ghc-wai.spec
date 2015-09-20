# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name wai

%bcond_with tests

# no useful debuginfo for Haskell packages without C sources
%global debug_package %{nil}

Name:           ghc-%{pkg_name}
Version:        3.0.1.1
Release:        2%{?dist}
Summary:        Haskell Web Application Interface library

License:        MIT
URL:            http://hackage.haskell.org/package/%{pkg_name}
Source0:        http://hackage.haskell.org/package/%{pkg_name}-%{version}/%{pkg_name}-%{version}.tar.gz

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
# Begin cabal-rpm deps:
BuildRequires:  ghc-blaze-builder-devel
BuildRequires:  ghc-bytestring-devel
BuildRequires:  ghc-http-types-devel
BuildRequires:  ghc-network-devel
BuildRequires:  ghc-text-devel
BuildRequires:  ghc-vault-devel
%if %{with tests}
BuildRequires:  ghc-hspec-devel
%endif
# End cabal-rpm deps

%description
Provides a common protocol for communication between web applications
and web servers.


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


%changelog
* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Sep 01 2014 Jens Petersen <petersen@redhat.com> - 3.0.1.1-1
- update to 3.0.1.1

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jun 10 2014 Jens Petersen <petersen@redhat.com> - 1.4.1-3
- disable debuginfo explicitly (cblrpm-0.8.11)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 02 2014 Jens Petersen <petersen@redhat.com> - 1.4.1-1
- update to 1.4.1

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 10 2013 Jens Petersen <petersen@redhat.com> - 1.4.0.1-1
- update to 1.4.0.1
- update to new simplified Haskell Packaging Guidelines

* Tue Mar 12 2013 Jens Petersen <petersen@redhat.com> - 1.4.0-1
- update to 1.4.0

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 08 2012 Jens Petersen <petersen@redhat.com> - 1.3.0.1-1
- update to 1.3.0.1

* Thu Jul 26 2012 Jens Petersen <petersen@redhat.com> - 1.2.0.3-1
- update to 1.2.0.3

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 15 2012 Jens Petersen <petersen@redhat.com> - 1.2.0.2-2
- rebuild

* Wed May 16 2012 Jens Petersen <petersen@redhat.com> - 1.2.0.2-1
- update to 1.2.0.2
- license is now MIT

* Fri Mar 23 2012 Jens Petersen <petersen@redhat.com> - 0.4.3-4
- add license to ghc_files

* Thu Mar  8 2012 Jens Petersen <petersen@redhat.com> - 0.4.3-3
- rebuild

* Sat Mar  3 2012 Jens Petersen <petersen@redhat.com> - 0.4.3-2
- rebuild

* Fri Jan  6 2012 Jens Petersen <petersen@redhat.com> - 0.4.3-1
- update to 0.4.3 and cabal2spec-0.25.2

* Sun Oct 30 2011 Jens Petersen <petersen@redhat.com> - 0.4.2-3
- rebuild against newer enumerator

* Mon Oct 24 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.4.2-2.1
- rebuild with new gmp without compat lib

* Fri Oct 14 2011 Jens Petersen <petersen@redhat.com> - 0.4.2-2
- rebuild for newer deps

* Tue Sep 27 2011 Jens Petersen <petersen@redhat.com> - 0.4.2-1
- update to 0.4.2

* Thu Sep  8 2011 Jens Petersen <petersen@redhat.com> - 0.4.1-1
- update to 0.4.1 and cabal2spec-0.24.1
- add dependencies

* Sat Jun 25 2011 Ben Boeckel <mathstuf@gmail.com> - 0.4.0-1
- Update to 0.4.0
- Update to cabal2spec-0.23.2

* Tue Mar 08 2011 Ben Boeckel <mathstuf@gmail.com> - 0.3.2-1
- Update to 0.3.2

* Tue Nov 23 2010 Ben Boeckel <mathstuf@gmail.com> - 0.2.2.1-1
- Update to 0.2.2.1

* Sat Oct 30 2010 Ben Boeckel <mathstuf@gmail.com> - 0.2.2-1
- Update to 0.2.2

* Tue Sep 14 2010 Ben Boeckel <mathstuf@gmail.com> - 0.2.1-1
- Update to 0.2.1

* Sat Sep 04 2010 Ben Boeckel <mathstuf@gmail.com> - 0.2.0-1
- Initial package

* Sat Sep  4 2010 Fedora Haskell SIG <haskell-devel@lists.fedoraproject.org> - 0.2.0-0
- initial packaging for Fedora automatically generated by cabal2spec-0.22.2
