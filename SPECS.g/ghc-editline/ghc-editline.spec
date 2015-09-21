# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name editline

Name:           ghc-%{pkg_name}
Version:        0.2.1.1
Release:        12%{?dist}
Summary:        Bindings to the libedit library

License:        BSD
Url:            https://hackage.haskell.org/package/%{pkg_name}
Source0:        https://hackage.haskell.org/package/%{pkg_name}-%{version}/%{pkg_name}-%{version}.tar.gz
Patch1:         editline-0.2.1.1-ghc78-Handle.patch

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
BuildRequires:  libedit-devel%{?_isa}

%description
This package contains bindings to the BSD editline library
(<http://www.thrysoee.dk/editline/>). It provides a basic interface to the
editline API for reading lines of input from the user.

Additionally, a readline compatibility module is included which provides a
subset of the functions from the readline package.


%package devel
Summary:        Haskell %{pkg_name} library development files
Provides:       %{name}-static = %{version}-%{release}
Requires:       ghc-compiler = %{ghc_version}
Requires(post): ghc-compiler = %{ghc_version}
Requires(postun): ghc-compiler = %{ghc_version}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       libedit-devel%{?_isa}

%description devel
This package provides the Haskell %{pkg_name} library development files.


%prep
%setup -q -n %{pkg_name}-%{version}
%patch1 -p1 -b .orig

cabal-tweak-dep-ver base '< 4.7' '< 4.8'


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


%Changelog
* Sun Sep 20 2015 Liu Di <liudidi@gmail.com> - 0.2.1.1-12
- 为 Magic 3.0 重建

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Feb 15 2015 Jochen Schmitt <Jochen herr-schmitt de> - 0.2.1.1-10
- Rebuilt to fix an dependency issues agains ghc(base)

* Wed Feb 11 2015 Jochen Schmitt <Jochen herr-schmitt de> - 0.2.1.1-9
- for new ghc release

* Tue Feb  3 2015 Jens Petersen <petersen@redhat.com> - 0.2.1.1-8
- cblrpm refresh

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed May 14 2014 Jens Petersen <petersen@redhat.com> - 0.2.1.1-6
- fix build on ghc-7.8

* Sat Aug  3 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun  7 2013 Jens Petersen <petersen@redhat.com> - 0.2.1.1-4
- update to new simplified Haskell Packaging Guidelines

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jan 12 2013 Jochen Schmitt <Jochen herr-schmitt de> - 0.2.1.1-2
- Bump to fix EVR-issue

* Mon Nov 26 2012 Jochen Schmitt <Jochen herr-schmitt de> - 0.2.1.1-1
- New upstream release
- Add BR to libedit-devel

* Sat Nov 17 2012 Jens Petersen <petersen@redhat.com>
- update with cabal-rpm

* Sun Mar 18 2012 Jens Petersen <petersen@redhat.com> - 0.2.1.0-26
- update to cabal2spec-0.25

* Wed Oct 26 2011 Jens Petersen <petersen@redhat.com> - 0.2.1.0-25
- update to cabal2spec-0.24.1
- use _isa for libedit dependency

* Sun Jun 19 2011 Jochen Schmitt <Jochen herr-schmitt de> 0.2.1.0-24
- Rebuild for new ghc release

* Thu Mar 10 2011 Fabio M. Di Nitto <fdinitto@redhat.com> 0.2.1.0-23
- Enable build on sparcv9

* Fri Jan  7 2011 Jochen Schmitt <Jochen herr-schmitt de> 0.2.1.0-20
- Rebuild to bix broken dependencies on rawhide

* Fri Nov 26 2010 Jens Petersen <petersen@redhat.com> 0.2.1.0-19
- rebuild for ghc-7.0.1
- no longer need BR for libffi-devel
- drop deprecated -o obsoletes

* Sun Nov  7 2010 Jochen Schmitt <Jochen herr-schmitt de> 0.2.1.0-18
- Add libffi-devel as a new BR

* Sat Sep  4 2010 Jens Petersen <petersen@redhat.com> - 0.2.1.0-17
- add hscolour and doc obsolete (cabal2spec-0.22.2)

* Sun Jun 27 2010 Jens Petersen <petersen@redhat.com> - 0.2.1.0-16
- sync cabal2spec-0.22.1

* Tue Apr 27 2010 Jens Petersen <petersen@redhat.com> - 0.2.1.0-15
- rebuild against ghc-6.12.2
- condition ghc_lib_package

* Wed Jan 20 2010 Jochen Schmitt <Jochen herr-schmitt de> 0.2.1.0-14
- Fix missing package-conf issue

* Mon Jan 11 2010 Jens Petersen <petersen@redhat.com> 0.2.1.0-13
- update to ghc-rpm-macros-0.5.1 and cabal2spec-0.21.1:
- drop doc and prof bcond
- use common summary and common_description
- use ghc_lib_package
- drop redundant buildroot and its install cleaning

* Tue Dec 22 2009 Jens Petersen <petersen@redhat.com> 0.2.1.0-12
- build for ghc-6.12.1
- added shared library support: needs ghc-rpm-macros 0.3.1

* Wed Sep 16 2009 Jens Petersen <petersen@redhat.com> 0.2.1.0-11
- sync with current cabal2spec template to minimise cabal2spec-diff
  - fixes uninstall error

* Mon Jul 27 2009 Jochen Schmitt <Jochen herr-schmitt de> 0.2.1.0-10
- Rebuild

* Thu Jul 23 2009 Jochen Schmitt <Jochen herr-schmitt de> 0.2.1.0-8
- Fix typo in Requires(post)

* Thu Jul 23 2009 Jens Petersen <petersen@redhat.com> - 0.2.1.0-7
- pkg_libdir is redundant
- devel requires libedit-devel

* Wed Jul 22 2009 Jochen Schmitt <Jochen herr-schmitt de> 0.2.1.0-6
- Rebuild for new ghc release on rawhide

* Tue Jul 21 2009 Jochen Schmitt <Jochen herr-schmitt de> 0.2.1.0-5
- Fix typo in %%{pkg_name} macro

* Mon Jul 20 2009 Jochen Schmitt <Jochen herr-schmitt de> 0.2.1.0-4
- Fix typo in definition of %%{pkg_libdir}

* Sun Jul 19 2009 Jochen Schmitt <Jochen herr-schmitt de> 0.2.1.0-3
- Fix monor grammer issue

* Thu Jul 16 2009 Jochen Schmitt <Jochen herr-schmitt de> 0.2.1.0-2
- Fix typos reported in review reqest

* Thu Jul  9 2009 Jochen Schmitt <Jochen herr-schmitt de> 0.2.1.0-1
- Initial package


