# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name uniplate

Name:           ghc-%{pkg_name}
Version:        1.6.12
Release:        2%{?dist}
Summary:        Uniform type generic traversals library

License:        BSD
Url:            https://hackage.haskell.org/package/%{pkg_name}
Source0:        https://hackage.haskell.org/package/%{pkg_name}-%{version}/%{pkg_name}-%{version}.tar.gz
Patch0:         uniplate-1.6.10-annotation-ghci.patch

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
# Begin cabal-rpm deps:
BuildRequires:  ghc-containers-devel
BuildRequires:  ghc-hashable-devel
BuildRequires:  ghc-syb-devel
BuildRequires:  ghc-unordered-containers-devel
# End cabal-rpm deps

%description
Uniplate is library for writing simple and concise generic operations.
Uniplate has similar goals to the original Scrap Your Boilerplate work,
but is substantially simpler and faster. The Uniplate manual is available at
<http://community.haskell.org/~ndm/darcs/uniplate/uniplate.htm>.


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
%ifnarch %{ghc_arches_with_ghci}
%patch0 -p1 -b .orig
%endif


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


%files devel -f %{name}-devel.files
%doc uniplate.htm


%changelog
* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jan 23 2015 Jens Petersen <petersen@redhat.com> - 1.6.12-1
- update to 1.6.12

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Nov  7 2013 Jens Petersen <petersen@redhat.com> - 1.6.10-4
- disable SPEC annotation on secondary arch's (#1027172)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 07 2013 Jens Petersen <petersen@redhat.com> - 1.6.10-2
- update to new simplified Haskell Packaging Guidelines

* Tue Mar 12 2013 Jens Petersen <petersen@redhat.com> - 1.6.10-1
- update to 1.6.10

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Nov 17 2012 Jens Petersen <petersen@redhat.com> - 1.6.7-5
- update with cabal-rpm

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Jens Petersen <petersen@redhat.com> - 1.6.7-3
- change prof BRs to devel

* Fri Jun 15 2012 Jens Petersen <petersen@redhat.com> - 1.6.7-2
- rebuild

* Tue Mar 20 2012 Jens Petersen <petersen@redhat.com> - 1.6.7-1
- update to 1.6.7
- depends on unordered-containers

* Thu Jan  5 2012 Jens Petersen <petersen@redhat.com> - 1.6.5-1
- update to 1.6.5 and cabal2spec-0.25.2

* Mon Oct 24 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.6.3-1.2
- rebuild with new gmp without compat lib

* Fri Oct 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.6.3-1.1
- rebuild with new gmp without compat lib

* Fri Oct 14 2011 Jens Petersen <petersen@redhat.com> - 1.6.3-1
- update to 1.6.3

* Tue Oct 11 2011 Peter Schiffer <pschiffe@redhat.com> - 1.6-6.1
- rebuild with new gmp

* Wed Jun 22 2011 Jens Petersen <petersen@redhat.com> - 1.6-6
- BR ghc-Cabal-devel instead of ghc-prof and use ghc_arches (cabal2spec-0.23.2)
- no longer requires mtl

* Thu Mar 10 2011 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.6-5
- Enable build on sparcv9

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 18 2011 Jens Petersen <petersen@redhat.com> - 1.6-3
- update to cabal2spec-0.22.4

* Sun Dec  5 2010 Jens Petersen <petersen@redhat.com> - 1.6-2
- rebuild

* Mon Nov 29 2010 Jens Petersen <petersen@redhat.com> - 1.6-1
- update to 1.6
- depends on syb

* Sat Sep  4 2010 Jens Petersen <petersen@redhat.com> - 1.5.1-4
- update to latest macros, hscolour and drop doc pkg (cabal2spec-0.22.2)

* Sat Jun 26 2010 Jens Petersen <petersen@redhat.com> - 1.5.1-3
- strip shared library (cabal2spec-0.21.4)

* Mon Feb 15 2010 Conrad Meyer <konrad@tylerc.org> - 1.5.1-1
- Update to 1.5.1

* Fri Jan 22 2010 Jens Petersen <petersen@redhat.com> - 1.4-1
- update to 1.4

* Tue Jan 12 2010 Jens Petersen <petersen@redhat.com> - 1.2.0.3-8
- rebuild against ghc-mtl package

* Mon Jan 11 2010 Jens Petersen <petersen@redhat.com> - 1.2.0.3-7
- update to ghc-rpm-macros-0.5.1 and cabal2spec-0.21.1:
- drop doc and prof bcond
- use common_summary and common_description
- use ghc_lib_package and ghc_pkg_deps
- build shared library
- drop redundant buildroot and its install cleaning

* Tue Aug  4 2009 Yaakov M. Nemoy <ynemoy@fedoraproject.org> - 1.2.0.3-6
- rebuild against new ghc

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu May 28 2009 Jens Petersen <petersen@redhat.com> - 1.2.0.3-4
- update to cabal2spec-0.16
- uncomment LICENSE in devel filelist!

* Fri Mar 20 2009 Conrad Meyer <konrad@tylerc.org> - 1.2.0.3-3
- Fix URL.

* Thu Mar 19 2009 Conrad Meyer <konrad@tylerc.org> - 1.2.0.3-2
- Update to new cabal2spec template.

* Mon Jan 12 2009 Conrad Meyer <konrad@tylerc.org> - 1.2.0.3-1
- initial packaging for Fedora created by cabal2spec
