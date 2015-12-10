# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name citeproc-hs

Name:           ghc-%{pkg_name}
Version:        0.3.9
Release:        9%{?dist}
Summary:        Citation Style Language library

License:        BSD
Url:            https://hackage.haskell.org/package/%{pkg_name}
Source0:        https://hackage.haskell.org/package/%{pkg_name}-%{version}/%{pkg_name}-%{version}.tar.gz

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
# Begin cabal-rpm deps:
BuildRequires:  ghc-HTTP-devel
BuildRequires:  ghc-bytestring-devel
BuildRequires:  ghc-containers-devel
BuildRequires:  ghc-directory-devel
BuildRequires:  ghc-filepath-devel
BuildRequires:  ghc-hs-bibutils-devel
BuildRequires:  ghc-json-devel
BuildRequires:  ghc-mtl-devel
BuildRequires:  ghc-network-devel
BuildRequires:  ghc-old-locale-devel
BuildRequires:  ghc-pandoc-types-devel
BuildRequires:  ghc-parsec-devel
BuildRequires:  ghc-syb-devel
BuildRequires:  ghc-time-devel
BuildRequires:  ghc-utf8-string-devel
BuildRequires:  ghc-xml-devel
# End cabal-rpm deps

%description
citeproc-hs is a library for rendering bibliographic reference citations
into a variety of styles using a macro language called
Citation Style Language (CSL): http://citationstyles.org/.


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

cabal-tweak-flag hexpat False


%build
%ghc_lib_build


%install
%ghc_lib_install

rm %{buildroot}%{ghc_pkgdocdir}/LICENSE


%post devel
%ghc_pkg_recache


%postun devel
%ghc_pkg_recache


%files -f %{name}.files
%license LICENSE
%{_datadir}/%{pkg_name}-%{version}


%files devel -f %{name}-devel.files
%doc README


%changelog
* Sun Nov 08 2015 Liu Di <liudidi@gmail.com> - 0.3.9-9
- 为 Magic 3.0 重建

* Sun Sep 20 2015 Liu Di <liudidi@gmail.com> - 0.3.9-8
- 为 Magic 3.0 重建

* Tue Sep  1 2015 Jens Petersen <petersen@redhat.com> - 0.3.9-7
- use license macro

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jan 28 2015 Jens Petersen <petersen@redhat.com> - 0.3.9-5
- update urls

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May  8 2014 Jens Petersen <petersen@redhat.com> - 0.3.9-2
- update packaging to cabal-rpm-0.8.10

* Wed Jan 22 2014 Jens Petersen <petersen@redhat.com> - 0.3.9-1
- update to 0.3.9

* Tue Aug 06 2013 Adam Williamson <awilliam@redhat.com> - 0.3.8-4
- rebuild for new libbibutils

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 07 2013 Jens Petersen <petersen@redhat.com> - 0.3.8-2
- update to new simplified Haskell Packaging Guidelines

* Sun Mar 10 2013 Jens Petersen <petersen@redhat.com> - 0.3.8-1
- update to 0.3.8

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Dec  3 2012 Jens Petersen <petersen@redhat.com> - 0.3.6-3
- data files needed at runtime

* Wed Nov 21 2012 Jens Petersen <petersen@redhat.com> - 0.3.6-2
- enable bibutils (#861782)

* Tue Nov 06 2012 Jens Petersen <petersen@redhat.com> - 0.3.6-1
- update to 0.3.6 with cabal-rpm
- override hexpat and bibutils flags

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Jens Petersen <petersen@redhat.com> - 0.3.4-6
- change prof BRs to devel

* Fri Jun 15 2012 Jens Petersen <petersen@redhat.com> - 0.3.4-5
- rebuild

* Thu Mar 22 2012 Jens Petersen <petersen@redhat.com> - 0.3.4-4
- add license to ghc_files

* Wed Mar  7 2012 Jens Petersen <petersen@redhat.com> - 0.3.4-3
- rebuild

* Mon Feb 13 2012 Jens Petersen <petersen@redhat.com> - 0.3.4-2
- rebuild

* Tue Feb  7 2012 Jens Petersen <petersen@redhat.com> - 0.3.4-1
- update to 0.3.4

* Fri Jan  6 2012 Jens Petersen <petersen@redhat.com> - 0.3.3-1
- update to 0.3.3 and cabal2spec-0.25.2

* Thu Oct 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.3.2-6.2
- rebuild with new gmp without compat lib

* Tue Oct 11 2011 Peter Schiffer <pschiffe@redhat.com> - 0.3.2-6.1
- rebuild with new gmp

* Thu Aug  4 2011 Jens Petersen <petersen@redhat.com> - 0.3.2-6
- rebuild for pandoc-types-1.8.2

* Wed Jul 27 2011 Jens Petersen <petersen@redhat.com> - 0.3.2-5
- rebuild for xml-1.3.9

* Wed Jun 22 2011 Jens Petersen <petersen@redhat.com> - 0.3.2-4
- BR ghc-Cabal-devel instead of ghc-prof and use ghc_arches (cabal2spec-0.23.2)

* Sat May 28 2011 Jens Petersen <petersen@redhat.com> - 0.3.2-3
- rebuild for newer ghc-xml

* Tue May 24 2011 Jens Petersen <petersen@redhat.com> - 0.3.2-2
- include locale files
- drop ghc_pkg_deps
- fix macro in comment for rpmlint

* Tue May  3 2011 Jens Petersen <petersen@redhat.com> - 0.3.2-1
- BSD license
- long list of deps

* Tue May  3 2011 Fedora Haskell SIG <haskell-devel@lists.fedoraproject.org> - 0.3.2-0
- initial packaging for Fedora automatically generated by cabal2spec-0.22.6
