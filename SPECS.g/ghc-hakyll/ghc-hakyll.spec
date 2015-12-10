# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name hakyll

%bcond_with tests

Name:           ghc-%{pkg_name}
Version:        4.5.4.0
Release:        6%{?dist}
Summary:        Static website compiler library

License:        BSD
Url:            https://hackage.haskell.org/package/%{pkg_name}
Source0:        https://hackage.haskell.org/package/%{pkg_name}-%{version}/%{pkg_name}-%{version}.tar.gz

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
# Begin cabal-rpm deps:
BuildRequires:  ghc-binary-devel
BuildRequires:  ghc-blaze-html-devel
BuildRequires:  ghc-blaze-markup-devel
BuildRequires:  ghc-bytestring-devel
BuildRequires:  ghc-cmdargs-devel
BuildRequires:  ghc-containers-devel
BuildRequires:  ghc-cryptohash-devel
BuildRequires:  ghc-data-default-devel
BuildRequires:  ghc-deepseq-devel
BuildRequires:  ghc-directory-devel
BuildRequires:  ghc-filepath-devel
BuildRequires:  ghc-fsnotify-devel
BuildRequires:  ghc-lrucache-devel
BuildRequires:  ghc-mtl-devel
BuildRequires:  ghc-network-devel
BuildRequires:  ghc-old-locale-devel
BuildRequires:  ghc-old-time-devel
BuildRequires:  ghc-pandoc-citeproc-devel
BuildRequires:  ghc-pandoc-devel
BuildRequires:  ghc-parsec-devel
BuildRequires:  ghc-process-devel
BuildRequires:  ghc-random-devel
BuildRequires:  ghc-regex-base-devel
BuildRequires:  ghc-regex-tdfa-devel
BuildRequires:  ghc-snap-core-devel
BuildRequires:  ghc-snap-server-devel
BuildRequires:  ghc-system-filepath-devel
BuildRequires:  ghc-tagsoup-devel
BuildRequires:  ghc-text-devel
BuildRequires:  ghc-time-devel
%if %{with tests}
BuildRequires:  ghc-HUnit-devel
BuildRequires:  ghc-QuickCheck-devel
BuildRequires:  ghc-test-framework-devel
BuildRequires:  ghc-test-framework-hunit-devel
BuildRequires:  ghc-test-framework-quickcheck2-devel
%endif
# End cabal-rpm deps

%description
Hakyll is a static website compiler library.
It provides you with the tools to create a simple or advanced static website
using a Haskell DSL and formats such as markdown or RST.


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
cabal-tweak-dep-ver pandoc-citeproc '< 0.5' '< 0.6'
cabal-tweak-flag checkExternal False


%build
%ghc_lib_build


%install
%ghc_lib_install

# put in devel doc
rm -r %{buildroot}%{_datadir}/%{pkg_name}-%{version}/example


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
%{_datadir}/%{pkg_name}-%{version}
%{_docdir}/%{name}-%{version}/LICENSE


%files devel -f %{name}-devel.files
%doc data/example
%{_bindir}/hakyll-init


%changelog
* Sun Nov 08 2015 Liu Di <liudidi@gmail.com> - 4.5.4.0-6
- 为 Magic 3.0 重建

* Sun Sep 20 2015 Liu Di <liudidi@gmail.com> - 4.5.4.0-5
- 为 Magic 3.0 重建

* Mon Sep  7 2015 Jens Petersen <petersen@redhat.com> - 4.5.4.0-4
- rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.5.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Mar  4 2015 Jens Petersen <petersen@fedoraproject.org> - 4.5.4.0-2
- rebuild

* Mon Jan 26 2015 Jens Petersen <petersen@redhat.com> - 4.5.4.0-1
- update to 4.5.4.0

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.5.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jul 16 2014 Jens Petersen <petersen@redhat.com> - 4.5.2.0-1
- update to 4.5.2.0 and cblrpm-0.8.11
- build with pandoc-citeproc instead of citeproc-hs hack

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.5.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Jens Petersen <petersen@redhat.com> - 4.5.1.0-3
- rebuild

* Tue May 13 2014 Jens Petersen <petersen@redhat.com> - 4.5.1.0-2
- reenable ARM now that pandoc is available (#992364)

* Fri May 02 2014 Jens Petersen <petersen@redhat.com> - 4.5.1.0-1
- update to 4.5.1.0
- enable previewServer and watchServer
- move example dir to devel doc

* Wed Jan 22 2014 Jens Petersen <petersen@redhat.com> - 4.4.3.1-1
- update to 4.4.3.1
- disable watchServer (needs fsnotify)
- patch to use citeproc-hs until pandoc-citeproc packaged:
  this may cause biblio regressions

* Wed Aug 28 2013 Jens Petersen <petersen@redhat.com> - 4.3.1.0-4
- temporarily exclude armv7hl since pandoc not building there (#992364)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 21 2013 Jens Petersen <petersen@redhat.com> - 4.3.1.0-2
- rebuild

* Thu Jun 20 2013 Jens Petersen <petersen@redhat.com> - 4.3.1.0-1
- update to 4.3.1.0

* Fri Jun 14 2013 Jens Petersen <petersen@redhat.com> - 4.3.0.0-1
- update to 4.3.0.0
- update to new simplified Haskell Packaging Guidelines

* Sun Mar 10 2013 Jens Petersen <petersen@redhat.com> - 4.2.1.2-1
- update to 4.2.1.2
- no longer depends on hamlet
- disable checkExternal since it requires http-conduit
- add hakyll-init to devel subpackage

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Nov 21 2012 Jens Petersen <petersen@redhat.com> - 3.4.0.0-2
- rebuild

* Mon Oct 29 2012 Jens Petersen <petersen@redhat.com> - 3.4.0.0-1
- update to 3.4.0.0 with cabal-rpm
- disable previewServer explicitly until snap-server packaged
- allow hamlet-1.1

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.7.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Jens Petersen <petersen@redhat.com> - 3.2.7.2-5
- change prof BRs to devel

* Thu Jun 21 2012 Jens Petersen <petersen@redhat.com> - 3.2.7.2-4
- rebuild

* Fri Jun 15 2012 Jens Petersen <petersen@redhat.com> - 3.2.7.2-3
- rebuild

* Fri May 11 2012 Karsten Hopp <karsten@redhat.com> 3.2.7.2-2
- change exclusivearches from ghc_arches to ghc_arches_with_ghci as
  the BR ghc-hamlet is only available on those archs

* Thu Apr 26 2012 Jens Petersen <petersen@redhat.com> - 3.2.7.2-1
- update to 3.2.7.2

* Thu Mar 22 2012 Jens Petersen <petersen@redhat.com> - 3.2.6.2-1
- update to 3.2.6.2

* Wed Mar  7 2012 Jens Petersen <petersen@redhat.com> - 3.2.6.1-1
- update to 3.2.6.1
- regex-pcre depends replaced by regex-tdfa

* Mon Feb 13 2012 Jens Petersen <petersen@redhat.com> - 3.2.6.0-1
- update to 3.2.6.0

* Fri Feb 10 2012 Petr Pisar <ppisar@redhat.com> - 3.2.5.1-2
- Rebuild against PCRE 8.30

* Tue Feb  7 2012 Jens Petersen <petersen@redhat.com> - 3.2.5.1-1
- update to 3.2.5.1

* Thu Jan 26 2012 Jens Petersen <petersen@redhat.com> - 3.2.5.0-1
- update to 3.2.5.0

* Fri Jan  6 2012 Jens Petersen <petersen@redhat.com> - 3.2.3.2-1
- update to 3.2.3.2 and cabal2spec-0.25.2
- use ghc_add_basepkg_file

* Mon Nov  7 2011 Jens Petersen <petersen@redhat.com> - 3.2.0.10-1
- BSD license, deps, and description

* Mon Oct 31 2011 Fedora Haskell SIG <haskell-devel@lists.fedoraproject.org> - 3.2.0.10-0
- initial packaging for Fedora automatically generated by cabal2spec-0.24.1
