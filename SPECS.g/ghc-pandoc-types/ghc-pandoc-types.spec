# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name pandoc-types

Name:           ghc-%{pkg_name}
Version:        1.12.4.1
Release:        4%{?dist}
Summary:        Types for representing a structured document

License:        GPLv2+
Url:            https://hackage.haskell.org/package/%{pkg_name}
Source0:        https://hackage.haskell.org/package/%{pkg_name}-%{version}/%{pkg_name}-%{version}.tar.gz

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
# Begin cabal-rpm deps:
BuildRequires:  ghc-aeson-devel
BuildRequires:  ghc-bytestring-devel
BuildRequires:  ghc-containers-devel
BuildRequires:  ghc-deepseq-generics-devel
BuildRequires:  ghc-syb-devel
# End cabal-rpm deps

%description
This package contains definitions for the Pandoc data structure, which
is used by pandoc to represent structured documents. These definitions
used to live in the pandoc package, but they have been split off, so
that other packages can use them without drawing in all of pandoc's
dependencies, and pandoc itself can depend on packages (like
citeproc-hs) that use them.


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
%doc COPYING


%files devel -f %{name}-devel.files


%changelog
* Sun Sep 20 2015 Liu Di <liudidi@gmail.com> - 1.12.4.1-4
- 为 Magic 3.0 重建

* Mon Aug 31 2015 Peter Robinson <pbrobinson@fedoraproject.org> 1.12.4.1-3
- Rebuild (aarch64 vector hashes)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jan 26 2015 Jens Petersen <petersen@redhat.com> - 1.12.4.1-1
- update to 1.12.4.1

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.3.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 08 2014 Jens Petersen <petersen@redhat.com> - 1.12.3.3-1
- update to 1.12.3.3

* Sun Apr 20 2014 Jens Petersen <petersen@redhat.com> - 1.12.3.1-3
- revert requiring ghci: aeson now patched to build when no ghci

* Sun Apr 20 2014 Jens Petersen <petersen@redhat.com> - 1.12.3.1-2
- aeson needs TemplateHaskell
- update packaging to latest cblrpm

* Wed Jan 22 2014 Jens Petersen <petersen@redhat.com> - 1.12.3.1-1
- update to 1.12.3.1

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jun 05 2013 Jens Petersen <petersen@redhat.com> - 1.10-2
- update to new simplified Haskell Packaging Guidelines

* Sun Mar 10 2013 Jens Petersen <petersen@redhat.com> - 1.10-1
- update to 1.10

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Nov 17 2012 Jens Petersen <petersen@redhat.com> - 1.9.1-6
- update with cabal-rpm

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Jens Petersen <petersen@redhat.com> - 1.9.1-4
- change prof BRs to devel

* Fri Jun 15 2012 Jens Petersen <petersen@redhat.com> - 1.9.1-3
- rebuild

* Thu Mar 22 2012 Jens Petersen <petersen@redhat.com> - 1.9.1-2
- add license to ghc_files

* Wed Mar  7 2012 Jens Petersen <petersen@redhat.com> - 1.9.1-1
- update to 1.9.1

* Sun Feb 12 2012 Jens Petersen <petersen@redhat.com> - 1.9.0.2-1
- update to 1.9.0.2

* Thu Jan  5 2012 Jens Petersen <petersen@redhat.com> - 1.8.2-2
- update to cabal2spec-0.25.2

* Mon Oct 24 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.8.2-1.3
- rebuild with new gmp without compat lib

* Fri Oct 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.8.2-1.2
- rebuild with new gmp without compat lib

* Tue Oct 11 2011 Peter Schiffer <pschiffe@redhat.com> - 1.8.2-1.1
- rebuild with new gmp

* Thu Aug  4 2011 Jens Petersen <petersen@redhat.com> - 1.8.2-1
- update to 1.8.2

* Wed Jun 22 2011 Jens Petersen <petersen@redhat.com> - 1.8.0.2-2
- use ghc_arches (cabal2spec-0.23.2)

* Fri May 13 2011 Jens Petersen <petersen@redhat.com> - 1.8.0.2-1
- update to 1.8.0.2

* Wed May 11 2011 Jens Petersen <petersen@redhat.com> - 1.8-2
- drop ghc_package_deps
- add BR on ghc-Cabal-devel and ghc-containers-prof

* Tue May  3 2011 Jens Petersen <petersen@redhat.com> - 1.8-1
- GPLv2+ and depends on syb

* Tue May  3 2011 Fedora Haskell SIG <haskell-devel@lists.fedoraproject.org> - 1.8-0
- initial packaging for Fedora automatically generated by cabal2spec-0.22.6
