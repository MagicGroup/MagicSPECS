# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name warp

%bcond_with tests

Name:           ghc-%{pkg_name}
Version:        3.0.0.5
Release:        6%{?dist}
Summary:        A fast, light-weight web server for WAI applications

License:        MIT
Url:            https://hackage.haskell.org/package/%{pkg_name}
Source0:        https://hackage.haskell.org/package/%{pkg_name}-%{version}/%{pkg_name}-%{version}.tar.gz

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
# Begin cabal-rpm deps:
BuildRequires:  ghc-array-devel
BuildRequires:  ghc-blaze-builder-devel
BuildRequires:  ghc-bytestring-devel
BuildRequires:  ghc-case-insensitive-devel
BuildRequires:  ghc-hashable-devel
BuildRequires:  ghc-http-date-devel
BuildRequires:  ghc-http-types-devel
BuildRequires:  ghc-network-devel
BuildRequires:  ghc-simple-sendfile-devel
BuildRequires:  ghc-streaming-commons-devel
BuildRequires:  ghc-text-devel
BuildRequires:  ghc-unix-compat-devel
BuildRequires:  ghc-unix-devel
BuildRequires:  ghc-void-devel
BuildRequires:  ghc-wai-devel
%if %{with tests}
BuildRequires:  ghc-HTTP-devel
BuildRequires:  ghc-HUnit-devel
BuildRequires:  ghc-QuickCheck-devel
BuildRequires:  ghc-async-devel
BuildRequires:  ghc-doctest-devel
BuildRequires:  ghc-hspec-devel
BuildRequires:  ghc-lifted-base-devel
BuildRequires:  ghc-old-locale-devel
BuildRequires:  ghc-time-devel
BuildRequires:  ghc-transformers-devel
%endif
# End cabal-rpm deps

%description
A fast, light-weight web server for WAI applications.
Warp is the premier WAI handler.
See http://steve.vinoski.net/blog/2011/05/01/warp-a-haskell-web-server/.


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
* Fri Dec 04 2015 Liu Di <liudidi@gmail.com> - 3.0.0.5-6
- 为 Magic 3.0 重建

* Sun Nov 08 2015 Liu Di <liudidi@gmail.com> - 3.0.0.5-5
- 为 Magic 3.0 重建

* Sun Sep 20 2015 Liu Di <liudidi@gmail.com> - 3.0.0.5-4
- 为 Magic 3.0 重建

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Mar  3 2015 Jens Petersen <petersen@fedoraproject.org> - 3.0.0.5-2
- cblrpm refresh

* Mon Sep 01 2014 Jens Petersen <petersen@redhat.com> - 3.0.0.5-1
- update to 3.0.0.5
- refresh to cblrpm-0.8.11

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.8.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.8.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 02 2014 Jens Petersen <petersen@redhat.com> - 1.3.8.4-1
- update to 1.3.8.4

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 10 2013 Jens Petersen <petersen@redhat.com> - 1.3.8.2-1
- update to 1.3.8.2

* Fri Jun 07 2013 Jens Petersen <petersen@redhat.com> - 1.3.7.4-2
- update to new simplified Haskell Packaging Guidelines

* Tue Mar 12 2013 Jens Petersen <petersen@redhat.com> - 1.3.7.4-1
- update to 1.3.7.4

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 08 2012 Jens Petersen <petersen@redhat.com> - 1.3.4.1-1
- update to 1.3.4.1

* Thu Jul 26 2012 Jens Petersen <petersen@redhat.com> - 1.2.2-1
- update to 1.2.2

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 15 2012 Jens Petersen <petersen@redhat.com> - 1.2.1.1-2
- rebuild

* Sat Jun  2 2012 Jens Petersen <petersen@redhat.com> - 1.2.1.1-1
- update to 1.2.1.1
- license is now MIT
- depends on network-conduit

* Fri Mar 23 2012 Jens Petersen <petersen@redhat.com> - 0.4.6.3-3
- add license to ghc_files

* Thu Mar  8 2012 Jens Petersen <petersen@redhat.com> - 0.4.6.3-2
- rebuild

* Mon Jan 16 2012 Jens Petersen <petersen@redhat.com> - 0.4.6.3-1
- update to 0.4.6.3 and cabal2spec-0.25.2

* Fri Dec 16 2011 Jens Petersen <petersen@redhat.com> - 0.4.6.2-1
- update to 0.4.6.2

* Thu Dec  1 2011 Jens Petersen <petersen@redhat.com> - 0.4.6.1-1
- BSD; add deps

* Thu Dec  1 2011 Fedora Haskell SIG <haskell-devel@lists.fedoraproject.org>
- initial packaging for Fedora automatically generated by cabal2spec-0.24.1
