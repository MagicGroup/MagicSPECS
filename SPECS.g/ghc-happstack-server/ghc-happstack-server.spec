# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name happstack-server

%bcond_without tests

Name:           ghc-%{pkg_name}
Version:        7.3.9
Release:        3%{?dist}
Summary:        Happstack web server

License:        BSD
Url:            https://hackage.haskell.org/package/%{pkg_name}
Source0:        https://hackage.haskell.org/package/%{pkg_name}-%{version}/%{pkg_name}-%{version}.tar.gz
Patch1:         happstack-server-time-compat.patch

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
# Begin cabal-rpm deps:
BuildRequires:  ghc-base64-bytestring-devel
BuildRequires:  ghc-blaze-html-devel
BuildRequires:  ghc-bytestring-devel
BuildRequires:  ghc-containers-devel
BuildRequires:  ghc-directory-devel
BuildRequires:  ghc-extensible-exceptions-devel
BuildRequires:  ghc-filepath-devel
BuildRequires:  ghc-hslogger-devel
BuildRequires:  ghc-html-devel
BuildRequires:  ghc-monad-control-devel
BuildRequires:  ghc-mtl-devel
BuildRequires:  ghc-network-devel
BuildRequires:  ghc-old-locale-devel
BuildRequires:  ghc-parsec-devel
BuildRequires:  ghc-process-devel
BuildRequires:  ghc-sendfile-devel
BuildRequires:  ghc-syb-devel
BuildRequires:  ghc-system-filepath-devel
BuildRequires:  ghc-template-haskell-devel
BuildRequires:  ghc-text-devel
BuildRequires:  ghc-threads-devel
BuildRequires:  ghc-time-devel
BuildRequires:  ghc-transformers-base-devel
BuildRequires:  ghc-transformers-devel
BuildRequires:  ghc-unix-devel
BuildRequires:  ghc-utf8-string-devel
BuildRequires:  ghc-xhtml-devel
BuildRequires:  ghc-zlib-devel
ExclusiveArch:  %{ghc_arches_with_ghci}
%if %{with tests}
BuildRequires:  ghc-HUnit-devel
%endif
# End cabal-rpm deps

%description
Happstack Server provides an HTTP server and a rich set of functions for
routing requests, handling query parameters, generating responses, working with
cookies, serving files, and more. For in-depth documentation see the Happstack
Crash Course <http://happstack.com/docs/crashcourse/index.html>.


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
%patch1 -p1 -b .orig


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
%doc COPYING
%{_docdir}/%{name}-%{version}/COPYING

%files devel -f %{name}-devel.files


%changelog
* Sun Sep 20 2015 Liu Di <liudidi@gmail.com> - 7.3.9-3
- 为 Magic 3.0 重建

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.3.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Mar  4 2015 Jens Petersen <petersen@fedoraproject.org> - 7.3.9-1
- update to 7.3.9

* Mon Sep 01 2014 Jens Petersen <petersen@redhat.com> - 7.3.8-1
- update to 7.3.8
- refresh to cblrpm-0.8.11

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.1.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.1.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jan 21 2014 Jens Petersen <petersen@redhat.com> - 7.1.0-3
- rebuild

* Fri Nov 29 2013 Jens Petersen <petersen@redhat.com> - 7.1.0-2
- rebuild

* Wed Sep 04 2013 Jens Petersen <petersen@redhat.com> - 7.1.0-1
- update to 7.1.0

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.0.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 07 2013 Jens Petersen <petersen@redhat.com> - 7.0.0-9
- update to new simplified Haskell Packaging Guidelines
- patch for newer time lib in ghc-7.6

* Tue Mar 19 2013 Jens Petersen <petersen@redhat.com> - 7.0.0-8
- allow blaze-html-0.6

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov  9 2012 Jens Petersen <petersen@redhat.com> - 7.0.0-6
- build with base64-bytestring-1.0 and blaze-html-0.5

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 21 2012 Jens Petersen <petersen@redhat.com> - 7.0.0-4
- rebuild

* Mon Jun 11 2012 Jens Petersen <petersen@redhat.com> - 7.0.0-3
- allow building with mtl-2.1 and transformers-0.3

* Mon May  7 2012 Jens Petersen <petersen@redhat.com> - 7.0.0-2
- turn on base4 flag
- add syb depends

* Fri Apr 13 2012 Jens Petersen <petersen@redhat.com> - 7.0.0-1
- BSD license
- dependencies

* Fri Apr 13 2012 Fedora Haskell SIG <haskell-devel@lists.fedoraproject.org>
- spec file template generated by cabal2spec-0.25.5
