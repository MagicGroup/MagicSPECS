# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name parsec

Name:           ghc-%{pkg_name}
# part of haskell-platform
Version:        3.1.5
Release:        4%{?dist}
Summary:        Monadic parser combinators

License:        BSD
Url:            https://hackage.haskell.org/package/%{pkg_name}
Source0:        https://hackage.haskell.org/package/%{pkg_name}-%{version}/%{pkg_name}-%{version}.tar.gz

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
# Begin cabal-rpm deps:
BuildRequires:  ghc-bytestring-devel
BuildRequires:  ghc-mtl-devel
BuildRequires:  ghc-text-devel
# End cabal-rpm deps

%description
Parsec is designed from scratch as an industrial-strength parser library.
It is simple, safe, well documented (on the package homepage), has extensive
libraries and good error messages, and is also fast. It is defined as a monad
transformer that can be stacked on arbitrary monads, and it is also parametric
in the input stream type.


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
* Sun Nov 08 2015 Liu Di <liudidi@gmail.com> - 3.1.5-4
- 为 Magic 3.0 重建

* Sun Sep 20 2015 Liu Di <liudidi@gmail.com> - 3.1.5-3
- 为 Magic 3.0 重建

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Aug  8 2014 Jens Petersen <petersen@redhat.com> - 3.1.5-1
- update to 3.1.5

* Tue Jul  8 2014 Jens Petersen <petersen@redhat.com> - 3.1.3-31
- update to cblrpm-0.8.11

* Fri Jan 31 2014 Jens Petersen <petersen@redhat.com> - 3.1.3-30
- bump over haskell-platform

* Wed Dec  4 2013 Jens Petersen <petersen@redhat.com> - 3.1.3-28
- revived with cabal-rpm-0.8.6

* Wed Mar 21 2012 Jens Petersen <petersen@redhat.com> - 3.1.2-1
- update to 3.1.2
- depends on text

* Mon Jan 16 2012 Jens Petersen <petersen@redhat.com> - 3.1.1-8
- no longer depends on syb

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jan  2 2012 Jens Petersen <petersen@redhat.com> - 3.1.1-6
- update to cabal2spec-0.25.2

* Mon Oct 24 2011 Marcela Mašláňová <mmaslano@redhat.com> - 3.1.1-5.3
- rebuild with new gmp without compat lib

* Fri Oct 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 3.1.1-5.2
- rebuild with new gmp without compat lib

* Tue Oct 11 2011 Peter Schiffer <pschiffe@redhat.com> - 3.1.1-5.1
- rebuild with new gmp

* Tue Jun 21 2011 Jens Petersen <petersen@redhat.com> - 3.1.1-5
- ghc_arches replaces ghc_excluded_archs

* Mon Jun 20 2011 Jens Petersen <petersen@redhat.com> - 3.1.1-4
- BR ghc-Cabal-devel and use ghc_excluded_archs

* Fri May 27 2011 Jens Petersen <petersen@redhat.com> - 3.1.1-3
- update to cabal2spec-0.23: add ppc64

* Thu Mar 10 2011 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.1.1-2
- Enable build on sparcv9

* Tue Feb 15 2011 Jens Petersen <petersen@redhat.com> - 3.1.1-1
- update to 3.1.1 for haskell-platform-2011.1

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 15 2011 Jens Petersen <petersen@redhat.com> - 3.1.0-2
- update to cabal2spec-0.22.4

* Sun Dec  5 2010 Jens Petersen <petersen@redhat.com> - 3.1.0-1
- update to 3.1.0
- depends on mtl and syb

* Wed Nov 24 2010 Jens Petersen <petersen@redhat.com> - 2.1.0.1-6
- rebuild with ghc-7.0.1

* Sat Sep  4 2010 Jens Petersen <petersen@redhat.com> - 2.1.0.1-5
- update to ghc-rpm-macros-0.8.1, hscolour and drop doc pkg (cabal2spec-0.22.2)
- part of haskell-platform-2010.2.0.0

* Wed Jun 23 2010 Jens Petersen <petersen@redhat.com> - 2.1.0.1-4
- use ghc_strip_dynlinked (ghc-rpm-macros-0.6.0)

* Sat Apr 24 2010 Jens Petersen <petersen@redhat.com> - 2.1.0.1-3
- part of haskell-platform-2010.1.0.0
- rebuild against ghc-6.12.2
- condition ghc_lib_package

* Mon Jan 11 2010 Jens Petersen <petersen@redhat.com> - 2.1.0.1-2
- update to ghc-rpm-macros-0.5.1: use ghc_lib_package
- drop bcond for doc and prof
- add comment about haskell-platform

* Thu Dec 24 2009 Jens Petersen <petersen@redhat.com> - 2.1.0.1-1
- update packaging for ghc-6.12.1
- added shared library support
- use new ghc*_requires macros: needs ghc-rpm-macros 0.4.0

* Wed Dec 23 2009 Fedora Haskell SIG <fedora-haskell-list@redhat.com> - 2.1.0.1-0
- initial packaging for Fedora automatically generated by cabal2spec-0.19
