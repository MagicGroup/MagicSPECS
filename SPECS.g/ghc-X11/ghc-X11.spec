# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name X11

Name:           ghc-%{pkg_name}
Version:        1.6.1.2
Release:        3%{?dist}
Summary:        Haskell binding to the X11 graphics library

License:        BSD
Url:            https://hackage.haskell.org/package/%{pkg_name}
Source0:        https://hackage.haskell.org/package/%{pkg_name}-%{version}/%{pkg_name}-%{version}.tar.gz

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
# Begin cabal-rpm deps:
BuildRequires:  ghc-data-default-devel
BuildRequires:  libX11-devel%{?_isa}
BuildRequires:  libXext-devel%{?_isa}
BuildRequires:  libXrandr-devel%{?_isa}
# End cabal-rpm deps
BuildRequires:  libXinerama-devel%{?_isa}

%description
A Haskell binding to the X11 graphics library. The binding is a direct
translation of the C binding; for documentation of these calls, refer to "The
Xlib Programming Manual", available online at <http://tronche.com/gui/x/xlib/>.


%package devel
Summary:        Haskell %{pkg_name} library development files
Provides:       %{name}-static = %{version}-%{release}
Requires:       ghc-compiler = %{ghc_version}
Requires(post): ghc-compiler = %{ghc_version}
Requires(postun): ghc-compiler = %{ghc_version}
Requires:       %{name}%{?_isa} = %{version}-%{release}
# Begin cabal-rpm deps:
Requires:       libX11-devel%{?_isa}
Requires:       libXext-devel%{?_isa}
Requires:       libXrandr-devel%{?_isa}
# End cabal-rpm deps
Requires:       libXinerama-devel%{?_isa}

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
* Sun Sep 20 2015 Liu Di <liudidi@gmail.com> - 1.6.1.2-3
- 为 Magic 3.0 重建

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jan 23 2015 Jens Petersen <petersen@redhat.com> - 1.6.1.2-1
- update to 1.6.1.2

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Apr 24 2013 Jens Petersen <petersen@redhat.com> - 1.6.1.1-2
- update to revised simplified Haskell Packaging Guidelines (cabal-rpm-0.8)

* Tue Mar 12 2013 Jens Petersen <petersen@redhat.com> - 1.6.1.1-1
- update to 1.6.1.1

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 08 2012 Jens Petersen <petersen@redhat.com> - 1.6.0.2-1
- update to 1.6.0.2

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Jens Petersen <petersen@redhat.com> - 1.6.0-3
- change prof BRs to devel

* Fri Jun 15 2012 Jens Petersen <petersen@redhat.com> - 1.6.0-2
- requires libXrandr too

* Sat Jun  9 2012 Jens Petersen <petersen@redhat.com> - 1.6.0-1
- update to 1.6.0
- new libXrandr binding

* Thu Mar 22 2012 Jens Petersen <petersen@redhat.com> - 1.5.0.1-3
- rebuild

* Fri Jan  6 2012 Jens Petersen <petersen@redhat.com> - 1.5.0.1-2
- restore X devel requires

* Thu Jan  5 2012 Jens Petersen <petersen@redhat.com> - 1.5.0.1-1
- update to 1.5.0.1 and cabal2spec-0.25.2

* Fri Dec  2 2011 Jens Petersen <petersen@redhat.com> - 1.5.0.0-13
- use _isa and update to cabal2spec-0.24.1

* Mon Oct 24 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.5.0.0-12.3
- rebuild with new gmp without compat lib

* Fri Oct 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.5.0.0-12.2
- rebuild with new gmp without compat lib

* Tue Oct 11 2011 Peter Schiffer <pschiffe@redhat.com> - 1.5.0.0-12.1
- rebuild with new gmp

* Wed Jun 22 2011 Jens Petersen <petersen@redhat.com> - 1.5.0.0-12
- BR ghc-Cabal-devel instead of ghc-prof and use ghc_arches (cabal2spec-0.23.2)

* Thu Mar 10 2011 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.5.0.0-11
- Enable build on sparcv9

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 15 2011 Ben Boeckel <mathstuf@gmail.com> - 1.5.0.0-9
- Update to cabal2spec-0.22.4
- Rebuild

* Sun Dec  5 2010 Jens Petersen <petersen@redhat.com> - 1.5.0.0-8
- rebuild

* Thu Nov 25 2010 Jens Petersen <petersen@redhat.com> - 1.5.0.0-7
- new syb dependency needed for ghc7
- drop -o obsoletes

* Sun Nov 07 2010 Ben Boeckel <mathstuf@gmail.com> - 1.5.0.0-6
- Rebuild

* Sat Sep  4 2010 Jens Petersen <petersen@redhat.com> - 1.5.0.0-5
- update to ghc-rpm-macros-0.8.1, hscolour and drop doc pkg (cabal2spec-0.22.2)

* Wed Jun 23 2010 Jens Petersen <petersen@redhat.com> - 1.5.0.0-4
- use ghc_strip_dynlinked (ghc-rpm-macros-0.6.0)

* Tue Apr 27 2010 Jens Petersen <petersen@redhat.com> - 1.5.0.0-3
- rebuild against ghc-6.12.2
- condition ghc_lib_package

* Mon Jan 11 2010 Jens Petersen <petersen@redhat.com> - 1.5.0.0-2
- update to ghc-rpm-macros-0.5.1 and cabal2spec-0.21.1:
- drop doc and prof bcond
- use common summary and common_description
- use ghc_lib_package and ghc_pkg_c_deps

* Wed Dec 23 2009 Jens Petersen <petersen@redhat.com>
- update base Group and devel Summary

* Mon Dec 21 2009 Yaakov M. Nemoy <ynemoy@fedoraproject.org> - 1.5.0.0-1
- updated to latest upstream
- updates spec to use shared libraries and new ghc

* Thu Oct 29 2009 Yaakov M. Nemoy <ynemoy@fedoraproject.org> - 1.4.6.1-1
- update to latest upstream

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.5-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 16 2009 Jens Petersen <petersen@redhat.com> - 1.4.5-11
- buildrequires ghc-rpm-macros (cabal2spec-0.16)

* Fri Apr 24 2009 Jens Petersen <petersen@redhat.com> - 1.4.5-10
- ghc_version is now in macros.ghc

* Fri Apr 24 2009 Jens Petersen <petersen@redhat.com> - 1.4.5-9
- try defining ghc_version with global

* Fri Apr 24 2009 Jens Petersen <petersen@redhat.com> - 1.4.5-8
- define ghc_version correctly

* Mon Apr 20 2009 Jens Petersen <petersen@redhat.com> - 1.4.5-7
- rebuild with ghc-6.10.2
- update to latest cabal2spec template and macros.ghc
  - pkg_libdir and pkg_docdir moved to macros.ghc
  - drop ghc_version from buildrequires
  - fix prof configure
  - add doc filelist
  - get ghc_version from ghc

* Sat Apr  4 2009 Yaakov M. Nemoy <yankee@localhost.localdomain> - 1.4.5-6
- rebuild bump to raise EVR manually, to match with F-10 branch

* Sun Mar  8 2009 Yaakov M. Nemoy <yankee@localhost.localdomain> - 1.4.5-5
- corrected a faulty tag

* Sun Mar  8 2009 Yaakov M. Nemoy <yankee@localhost.localdomain> - 1.4.5-4
- forgot to include the right arch tags

* Sat Feb 28 2009 Jens Petersen <petersen@redhat.com> - 1.4.5-3
- sync with cabal2spec-0.12:
- improve requires

* Mon Feb 23 2009 Yaakov M. Nemoy <loupgaroublond@gmail.com> - 1.4.5-2
- updated template to new guidelines

* Mon Jan  5 2009 Yaakov M. Nemoy <loupgaroublond@gmail.com> - 1.4.5-1
- initial packaging for Fedora created by cabal2spec
- added description and build requires
- altered license from template
