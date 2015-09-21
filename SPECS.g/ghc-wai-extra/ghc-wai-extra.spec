# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name wai-extra

%bcond_with tests

Name:           ghc-%{pkg_name}
Version:        3.0.4.5
Release:        4%{?dist}
Summary:        Basic WAI handlers and middleware

License:        MIT
Url:            https://hackage.haskell.org/package/%{pkg_name}
Source0:        https://hackage.haskell.org/package/%{pkg_name}-%{version}/%{pkg_name}-%{version}.tar.gz

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
# Begin cabal-rpm deps:
BuildRequires:  ghc-ansi-terminal-devel
BuildRequires:  ghc-base64-bytestring-devel
BuildRequires:  ghc-blaze-builder-devel
BuildRequires:  ghc-bytestring-devel
BuildRequires:  ghc-case-insensitive-devel
BuildRequires:  ghc-containers-devel
BuildRequires:  ghc-data-default-class-devel
BuildRequires:  ghc-deepseq-devel
BuildRequires:  ghc-directory-devel
BuildRequires:  ghc-fast-logger-devel
BuildRequires:  ghc-http-types-devel
BuildRequires:  ghc-lifted-base-devel
BuildRequires:  ghc-network-devel
BuildRequires:  ghc-old-locale-devel
BuildRequires:  ghc-resourcet-devel
BuildRequires:  ghc-streaming-commons-devel
BuildRequires:  ghc-stringsearch-devel
BuildRequires:  ghc-text-devel
BuildRequires:  ghc-time-devel
BuildRequires:  ghc-transformers-devel
BuildRequires:  ghc-unix-compat-devel
BuildRequires:  ghc-unix-devel
BuildRequires:  ghc-void-devel
BuildRequires:  ghc-wai-devel
BuildRequires:  ghc-wai-logger-devel
BuildRequires:  ghc-word8-devel
%if %{with tests}
BuildRequires:  ghc-HUnit-devel
BuildRequires:  ghc-hspec-devel
BuildRequires:  ghc-zlib-devel
%endif
# End cabal-rpm deps

%description
Provides basic WAI handler and middleware functionality:

* WAI Testing Framework
Hspec testing facilities and helpers for WAI.

* Event Source/Event Stream
Send server events to the client. Compatible with the JavaScript EventSource
API.

* Accept Override
Override the Accept header in a request. Special handling for the _accept query
parameter (which is used throughout WAI override the Accept header).

* Add Headers
WAI Middleware for adding arbitrary headers to an HTTP request.

* Clean Path
Clean a request path to a canonical form.

* GZip Compression
Negotiate HTTP payload gzip compression.

* HTTP Basic Authentication
WAI Basic Authentication Middleware which uses Authorization header.

* JSONP
"JSON with Padding" middleware. Automatic wrapping of JSON responses to convert
into JSONP.

* Method Override / Post
Allows overriding of the HTTP request method via the _method query string
parameter.

* Request Logging
Request logging middleware for development and production environments

* Request Rewrite
Rewrite request path info based on a custom conversion rules.

* Stream Files
Convert ResponseFile type responses into ResponseStream type.

* Virtual Host
Redirect incoming requests to a new host based on custom rules.

This library provides common Web Application Interface features.
API docs and the README are available at
<http://www.stackage.org/package/wai-extra>.


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
%doc README.md


%changelog
* Sun Sep 20 2015 Liu Di <liudidi@gmail.com> - 3.0.4.5-4
- 为 Magic 3.0 重建

* Mon Aug 24 2015 Ben Boeckel <mathstuf@gmail.com> - 3.0.4.5-3
- rebuild for ghc-stringsearch bump

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.4.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Mar 03 2015 Jens Petersen <petersen@redhat.com> - 3.0.4.5-1
- update to 3.0.4.5

* Fri Jan 23 2015 Jens Petersen <petersen@redhat.com> - 3.0.4.1-1
- update to 3.0.4.1

* Mon Sep 01 2014 Jens Petersen <petersen@redhat.com> - 3.0.2.1-1
- update to 3.0.2.1
- refresh to 0.8.11

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.4.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.4.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 02 2014 Jens Petersen <petersen@redhat.com> - 1.3.4.6-1
- update to 1.3.4.6

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jun 11 2013 Jens Petersen <petersen@redhat.com> - 1.3.3.2-1
- update to 1.3.3.2
- update to new simplified Haskell Packaging Guidelines

* Tue Mar 12 2013 Jens Petersen <petersen@redhat.com> - 1.3.2.4-1
- update to 1.3.2.4

* Thu Feb 14 2013 Jens Petersen <petersen@redhat.com> - 1.3.2-1
- update to 1.3.2

* Fri Nov 09 2012 Jens Petersen <petersen@redhat.com> - 1.3.0.3-1
- update to 1.3.0.3
- new dependencies on date-cache, stringsearch, and wai-logger

* Thu Jul 26 2012 Jens Petersen <petersen@redhat.com> - 1.2.0.4-4
- rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 15 2012 Jens Petersen <petersen@redhat.com> - 1.2.0.4-2
- rebuild

* Wed May 16 2012 Jens Petersen <petersen@redhat.com> - 1.2.0.4-1
- update to 1.2.0.4
- license is now MIT

* Tue May  1 2012 Jens Petersen <petersen@redhat.com> - 0.4.6-4
- allows zlib-bindings 0.1

* Wed Apr 11 2012 Jens Petersen <petersen@redhat.com> - 0.4.6-3
- allow data-default 0.4

* Fri Mar 23 2012 Jens Petersen <petersen@redhat.com> - 0.4.6-2
- add license to ghc_files

* Wed Mar  7 2012 Jens Petersen <petersen@redhat.com> - 0.4.6-1
- update to 0.4.6
- new depends on fast-logger

* Fri Jan  6 2012 Jens Petersen <petersen@redhat.com> - 0.4.5.2-1
- update to 0.4.5.2 and cabal2spec-0.25.2

* Sun Oct 30 2011 Jens Petersen <petersen@redhat.com> - 0.4.3-2
- rebuild against newer enumerator

* Tue Oct 25 2011 Jens Petersen <petersen@redhat.com> - 0.4.3-1
- update to 0.4.3 and cabal2spec-0.24.1
- update dependencies

* Sat Sep 04 2010 Ben Boeckel <mathstuf@gmail.com> - 0.2.2.2-1
- Initial package (#630300)

* Sat Sep  4 2010 Fedora Haskell SIG <haskell-devel@lists.fedoraproject.org> - 0.2.2.2-0
- initial packaging for Fedora automatically generated by cabal2spec-0.22.2
