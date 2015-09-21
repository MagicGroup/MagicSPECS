# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name hashed-storage

Name:           ghc-%{pkg_name}
Version:        0.5.11
Release:        3%{?dist}
Summary:        Hashed file storage support code

License:        BSD
URL:            http://hackage.haskell.org/package/%{pkg_name}
Source0:        http://hackage.haskell.org/package/%{pkg_name}-%{version}/%{pkg_name}-%{version}.tar.gz
# Bigendian Bits a needs Num a
Patch1:         hashed-storage-Bigendian-Num-Bits.patch

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
# Begin cabal-rpm deps:
BuildRequires:  ghc-binary-devel
BuildRequires:  ghc-bytestring-devel
BuildRequires:  ghc-containers-devel
BuildRequires:  ghc-dataenc-devel
BuildRequires:  ghc-directory-devel
BuildRequires:  ghc-extensible-exceptions-devel
BuildRequires:  ghc-filepath-devel
BuildRequires:  ghc-mmap-devel
BuildRequires:  ghc-mtl-devel
BuildRequires:  ghc-zlib-devel
# End cabal-rpm deps

%description
Support code for reading and manipulating hashed file storage (where each file
and directory is associated with a cryptographic hash, for corruption-resistant
storage and fast comparisons).

The supported storage formats include darcs hashed pristine, a plain filesystem
tree and an indexed plain tree (where the index maintains hashes of the plain
files and directories).


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
%patch1 -p1 -b .orig


%build
%ghc_lib_build


%check
# tests require test-framework


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
* Sun Sep 20 2015 Liu Di <liudidi@gmail.com> - 0.5.11-3
- 为 Magic 3.0 重建

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Aug 29 2014 Jens Petersen <petersen@redhat.com> - 0.5.11-1
- update to 0.5.11

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.10-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul  8 2014 Jens Petersen <petersen@redhat.com> - 0.5.10-7
- update to cblrpm-0.8.11

* Fri Apr 25 2014 Jens Petersen <petersen@redhat.com> - 0.5.10-6
- fix build on bigendian archs

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 07 2013 Jens Petersen <petersen@redhat.com> - 0.5.10-4
- update to new simplified Haskell Packaging Guidelines

* Fri Mar 22 2013 Jens Petersen <petersen@redhat.com> - 0.5.10-3
- rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Nov 07 2012 Jens Petersen <petersen@redhat.com> - 0.5.10-1
- update to 0.5.10

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Jens Petersen <petersen@redhat.com> - 0.5.9-5
- change prof BRs to devel

* Fri Jun 15 2012 Jens Petersen <petersen@redhat.com> - 0.5.9-4
- rebuild

* Thu Mar 22 2012 Jens Petersen <petersen@redhat.com> - 0.5.9-3
- add license to ghc_files

* Wed Jan  4 2012 Jens Petersen <petersen@redhat.com> - 0.5.9-2
- update to cabal2spec-0.25.2

* Mon Oct 24 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.5.9-1.2
- rebuild with new gmp without compat lib

* Fri Oct 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.5.9-1.1
- rebuild with new gmp without compat lib

* Thu Oct 13 2011 Jens Petersen <petersen@redhat.com> - 0.5.9-1
- update to 0.5.9

* Tue Oct 11 2011 Peter Schiffer <pschiffe@redhat.com> - 0.5.8-1.1
- rebuild with new gmp

* Wed Aug 17 2011 Jens Petersen <petersen@redhat.com> - 0.5.8-1
- update to 0.5.8

* Thu Jun 23 2011 Jens Petersen <petersen@redhat.com> - 0.5.7-2
- BR ghc-Cabal-devel instead of ghc-prof and use ghc_arches (cabal2spec-0.23.2)

* Sat May 28 2011 Jens Petersen <petersen@redhat.com> - 0.5.7-1
- update to 0.5.7
- update to cabal2spec-0.23: add ppc64

* Fri May  6 2011 Jens Petersen <petersen@redhat.com> - 0.5.6-1
- update to 0.5.6
- update to cabal2spec-0.22.6

* Thu Mar 10 2011 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.5.5-2
- Enable build on sparcv9

* Tue Feb 15 2011 Jens Petersen <petersen@redhat.com> - 0.5.5-1
- update to 0.5.5

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 19 2011 Jens Petersen <petersen@redhat.com> - 0.5.4-2
- update to cabal2spec-0.22.4

* Thu Nov 25 2010 Jens Petersen <petersen@redhat.com> - 0.5.4-1
- update to 0.5.4

* Mon Nov  1 2010 Jens Petersen <petersen@redhat.com> - 0.5.3-3
- rebuild for new versions of dataenc and mmap

* Wed Sep 29 2010 jkeating - 0.5.3-2
- Rebuilt for gcc bug 634757

* Fri Sep 17 2010 Jens Petersen <petersen@redhat.com> - 0.5.3-1
- update to 0.5.3

* Thu Aug 19 2010 Jens Petersen <petersen@redhat.com> - 0.4.13-3
- update to ghc-rpm-macros-0.8.1 (cabal2spec-0.22.2)

* Sun Jun 27 2010 Jens Petersen <petersen@redhat.com> - 0.4.13-2
- sync cabal2spec-0.22.1

* Mon May 17 2010 Jens Petersen <petersen@redhat.com> - 0.4.13-1
- update to 0.4.13 for darcs-2.4.3

* Mon Apr 26 2010 Jens Petersen <petersen@redhat.com> - 0.4.11-2
- rebuild against ghc-6.12.2
- condition ghc_lib_package

* Thu Apr 15 2010 Jens Petersen <petersen@redhat.com> - 0.4.11-1
- update to 0.4.11 for darcs-2.4.1

* Mon Mar  1 2010 Jens Petersen <petersen@redhat.com> - 0.4.7-1
- update to 0.4.7

* Sat Jan 23 2010 Jens Petersen <petersen@redhat.com> - 0.4.5-1
- update to 0.4.5 for darcs-beta
- code is now pure BSD: upstream rewrote SHA256.hs
- now depends also on ghc-binary and ghc-dataenc

* Tue Jan 12 2010 Jens Petersen <petersen@redhat.com> - 0.3.9-2
- update to ghc-rpm-macros-0.5.1 and cabal2spec-0.21.1:
- drop doc and prof bcond
- use common summary and common_description
- use ghc_lib_package
- drop redundant buildroot and its install cleaning

* Tue Nov 17 2009 Jens Petersen <petersen@redhat.com> - 0.3.9-1
- initial packaging for Fedora created by cabal2spec
