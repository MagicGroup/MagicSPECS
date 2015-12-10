# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name mmap

Name:           ghc-%{pkg_name}
Version:        0.5.9
Release:        4%{?dist}
Summary:        Memory mapped files library

License:        BSD
Url:            https://hackage.haskell.org/package/%{pkg_name}
Source0:        https://hackage.haskell.org/package/%{pkg_name}-%{version}/%{pkg_name}-%{version}.tar.gz

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
# Begin cabal-rpm deps:
BuildRequires:  ghc-bytestring-devel
# End cabal-rpm deps

%description
This library provides a wrapper to mmap(2) or MapViewOfFile, allowing files or
devices to be lazily loaded into memory as strict or lazy ByteStrings,
ForeignPtrs or plain Ptrs, using the virtual memory subsystem to do on-demand
loading. Modifications are also supported.


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
* Sun Nov 08 2015 Liu Di <liudidi@gmail.com> - 0.5.9-4
- 为 Magic 3.0 重建

* Sun Sep 20 2015 Liu Di <liudidi@gmail.com> - 0.5.9-3
- 为 Magic 3.0 重建

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jan 20 2015 Jens Petersen <petersen@redhat.com> - 0.5.9-1
- update to 0.5.9

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jun 05 2013 Jens Petersen <petersen@redhat.com> - 0.5.8-3
- update to new simplified Haskell Packaging Guidelines

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Nov 07 2012 Jens Petersen <petersen@redhat.com> - 0.5.8-1
- update to 0.5.8

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.7-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Jens Petersen <petersen@redhat.com> - 0.5.7-9
- change prof BRs to devel

* Sun Mar 18 2012 Jens Petersen <petersen@redhat.com> - 0.5.7-8
- update to cabal2spec-0.25

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.7-7.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Oct 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.5.7-6.2
- rebuild with new gmp without compat lib

* Tue Oct 11 2011 Peter Schiffer <pschiffe@redhat.com> - 0.5.7-6.1
- rebuild with new gmp

* Thu Jun 23 2011 Jens Petersen <petersen@redhat.com> - 0.5.7-6
- BR ghc-Cabal-devel instead of ghc-prof and use ghc_arches (cabal2spec-0.23.2)

* Thu Mar 10 2011 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.5.7-5
- Enable build on sparcv9

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 19 2011 Jens Petersen <petersen@redhat.com> - 0.5.7-3
- update to cabal2spec-0.22.4

* Thu Nov 25 2010 Jens Petersen <petersen@redhat.com> - 0.5.7-2
- update to 0.5.4 and drop -o obsoletes

* Mon Nov  1 2010 Jens Petersen <petersen@redhat.com> - 0.5.7-1
- update to 0.5.7
- mmap-no-HUnit.patch is now upstream

* Wed Sep 29 2010 jkeating - 0.5.6-2
- Rebuilt for gcc bug 634757

* Fri Sep 17 2010 Jens Petersen <petersen@redhat.com> - 0.5.6-1
- update to 0.5.6 for darcs-2.5
- patch out superfluous test dependency on HUnit

* Sat Sep  4 2010 Jens Petersen <petersen@redhat.com> - 0.4.1-5
- add hscolour and doc obsolete (cabal2spec-0.22.2)

* Sat Jun 26 2010 Jens Petersen <petersen@redhat.com> - 0.4.1-4
- sync cabal2spec-0.22

* Sat Apr 24 2010 Jens Petersen <petersen@redhat.com> - 0.4.1-3
- rebuild against ghc-6.12.2
- condition ghc_lib_package

* Mon Jan 11 2010 Jens Petersen <petersen@redhat.com> - 0.4.1-2
- update to ghc-rpm-macros-0.5.1 and cabal2spec-0.21.1:
- drop doc and prof bcond
- use common summary and common_description
- use ghc_lib_package
- drop redundant buildroot and its install cleaning

* Tue Nov 17 2009 Jens Petersen <petersen@redhat.com> - 0.4.1-1
- initial packaging for Fedora created by cabal2spec
