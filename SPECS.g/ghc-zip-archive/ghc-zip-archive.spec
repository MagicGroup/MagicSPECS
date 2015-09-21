# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name zip-archive

%ifnarch armv7hl
%bcond_without tests
%endif

Name:           ghc-%{pkg_name}
Version:        0.2.3.5
Release:        3%{?dist}
Summary:        Library for creating and modifying zip archives

License:        BSD
Url:            https://hackage.haskell.org/package/%{pkg_name}
Source0:        https://hackage.haskell.org/package/%{pkg_name}-%{version}/%{pkg_name}-%{version}.tar.gz

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
# Begin cabal-rpm deps:
BuildRequires:  ghc-array-devel
BuildRequires:  ghc-binary-devel
BuildRequires:  ghc-bytestring-devel
BuildRequires:  ghc-containers-devel
BuildRequires:  ghc-digest-devel
BuildRequires:  ghc-directory-devel
BuildRequires:  ghc-filepath-devel
BuildRequires:  ghc-mtl-devel
BuildRequires:  ghc-old-time-devel
BuildRequires:  ghc-pretty-devel
BuildRequires:  ghc-text-devel
BuildRequires:  ghc-time-devel
BuildRequires:  ghc-unix-devel
BuildRequires:  ghc-zlib-devel
%if %{with tests}
BuildRequires:  ghc-HUnit-devel
BuildRequires:  ghc-process-devel
%endif
# End cabal-rpm deps

%description
The zip-archive library provides functions for creating, modifying, and
extracting files from zip archives.


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
%doc README.markdown


%changelog
* Sun Sep 20 2015 Liu Di <liudidi@gmail.com> - 0.2.3.5-3
- 为 Magic 3.0 重建

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jan 23 2015 Jens Petersen <petersen@redhat.com> - 0.2.3.5-1
- update to 0.2.3.5

* Thu Oct 30 2014 Jens Petersen <petersen@redhat.com> - 0.2.3.4-1
- update to 0.2.3.4
- refresh to cblrpm-0.8.11

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.3.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.3.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.3.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 07 2013 Jens Petersen <petersen@redhat.com> - 0.1.3.4-2
- update to new simplified Haskell Packaging Guidelines

* Sun Mar 10 2013 Jens Petersen <petersen@redhat.com> - 0.1.3.4-1
- update to 0.1.3.4

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 08 2012 Jens Petersen <petersen@redhat.com> - 0.1.2.1-1
- update to 0.1.2.1
- license is now BSD

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Jens Petersen <petersen@redhat.com> - 0.1.1.8-2
- change prof BRs to devel

* Wed Jun 13 2012 Jens Petersen <petersen@redhat.com> - 0.1.1.8-1
- update to 0.1.1.8

* Fri Jan  6 2012 Jens Petersen <petersen@redhat.com> - 0.1.1.7-6
- update to cabal2spec-0.25.2

* Fri Oct 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.1.1.7-5.2
- rebuild with new gmp without compat lib

* Tue Oct 11 2011 Peter Schiffer <pschiffe@redhat.com> - 0.1.1.7-5.1
- rebuild with new gmp

* Fri Sep 30 2011 Jens Petersen <petersen@redhat.com> - 0.1.1.7-5
- rebuild against latest digest library

* Wed Jun 22 2011 Jens Petersen <petersen@redhat.com> - 0.1.1.7-4
- BR ghc-Cabal-devel instead of ghc-prof and use ghc_arches (cabal2spec-0.23.2)

* Sat May 28 2011 Jens Petersen <petersen@redhat.com> - 0.1.1.7-3
- update to cabal2spec-0.23: add ppc64

* Thu Mar 10 2011 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.1.1.7-2
- Enable build on sparcv9

* Tue Feb 15 2011 Jens Petersen <petersen@redhat.com> - 0.1.1.7-1
- update to 0.1.1.7

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 19 2011 Jens Petersen <petersen@redhat.com> - 0.1.1.6-5
- update to cabal2spec-0.22.4

* Tue Dec 21 2010 Jens Petersen <petersen@redhat.com> - 0.1.1.6-4
- install COPYING instead

* Fri Dec 10 2010 Jens Petersen <petersen@redhat.com> - 0.1.1.6-3
- include the COPYING file (#652573)

* Thu Dec  2 2010 Jens Petersen <petersen@redhat.com> - 0.1.1.6-2
- also depends on binary (#652573)

* Thu Dec  2 2010 Jens Petersen <petersen@redhat.com> - 0.1.1.6-1
- GPLv2+
- depends on digest, mtl, utf8-string, zlib

* Fri Nov 12 2010 Fedora Haskell SIG <haskell-devel@lists.fedoraproject.org> - 0.1.1.6-0
- initial packaging for Fedora automatically generated by cabal2spec-0.22.2
