# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name pango

Name:           ghc-%{pkg_name}
Version:        0.13.1.0
Release:        4%{?dist}
Summary:        Binding to the Pango text rendering engine

License:        LGPLv2+
Url:            https://hackage.haskell.org/package/%{pkg_name}
Source0:        https://hackage.haskell.org/package/%{pkg_name}-%{version}/%{pkg_name}-%{version}.tar.gz

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
# Begin cabal-rpm deps:
BuildRequires:  ghc-array-devel
BuildRequires:  ghc-cairo-devel
BuildRequires:  ghc-containers-devel
BuildRequires:  ghc-directory-devel
BuildRequires:  ghc-glib-devel
BuildRequires:  ghc-mtl-devel
BuildRequires:  ghc-pretty-devel
BuildRequires:  ghc-process-devel
BuildRequires:  ghc-text-devel
BuildRequires:  gtk2hs-buildtools
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(pangocairo)
# End cabal-rpm deps

%description
This package provides a wrapper around the Pango C library that allows
high-quality rendering of Unicode text. It can be used either with Cairo to
output text in PDF, PS or other documents or with Gtk+ to display text
on-screen.


%package devel
Summary:        Haskell %{pkg_name} library development files
Provides:       %{name}-static = %{version}-%{release}
Requires:       ghc-compiler = %{ghc_version}
Requires(post): ghc-compiler = %{ghc_version}
Requires(postun): ghc-compiler = %{ghc_version}
Requires:       %{name}%{?_isa} = %{version}-%{release}
# Begin cabal-rpm deps:
Requires:       pkgconfig(cairo)
Requires:       pkgconfig(pango)
Requires:       pkgconfig(pangocairo)
# End cabal-rpm deps

%description devel
This package provides the Haskell %{pkg_name} library development files.


%prep
%setup -q -n %{pkg_name}-%{version}


%build
%ghc_lib_build


%install
%ghc_lib_install

rm %{buildroot}%{ghc_pkgdocdir}/COPYING

# demo files
rm -r %{buildroot}%{_datadir}/%{pkg_name}-%{version}


%post devel
%ghc_pkg_recache


%postun devel
%ghc_pkg_recache


%files -f %{name}.files
%license COPYING


%files devel -f %{name}-devel.files
%doc demo


%changelog
* Fri Dec 04 2015 Liu Di <liudidi@gmail.com> - 0.13.1.0-4
- 为 Magic 3.0 重建

* Sun Nov 08 2015 Liu Di <liudidi@gmail.com> - 0.13.1.0-3
- 为 Magic 3.0 重建

* Sun Sep 20 2015 Liu Di <liudidi@gmail.com> - 0.13.1.0-2
- 为 Magic 3.0 重建

* Wed Jul 22 2015 Jens Petersen <petersen@redhat.com> - 0.13.1.0-1
- update to 0.13.1.0

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jan 20 2015 Jens Petersen <petersen@redhat.com> - 0.13.0.5-1
- update to 0.13.0.5

* Tue Sep 16 2014 Jens Petersen <petersen@redhat.com> - 0.13.0.0-1
- update to 0.13.0.0
- refresh to cblrpm-0.8.11

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Dec 21 2013 Jens Petersen <petersen@redhat.com> - 0.12.5.0-1
- update to 0.12.5.0

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 07 2013 Jens Petersen <petersen@redhat.com> - 0.12.4-4
- update to new simplified Haskell Packaging Guidelines

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 19 2012 Jens Petersen <petersen@redhat.com> - 0.12.4-2
- rebuild

* Sat Nov 17 2012 Jens Petersen <petersen@redhat.com> - 0.12.4-1
- update to 0.12.4

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Jens Petersen <petersen@redhat.com> - 0.12.3-3
- change prof BRs to devel

* Fri Jun 15 2012 Jens Petersen <petersen@redhat.com> - 0.12.3-2
- rebuild

* Tue Mar 20 2012 Jens Petersen <petersen@redhat.com> - 0.12.3-1
- update to 0.12.3

* Fri Jan  6 2012 Jens Petersen <petersen@redhat.com> - 0.12.2-1
- update to 0.12.2 and cabal2spec-0.25.2

* Mon Oct 24 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.12.1-1.3
- rebuild with new gmp without compat lib

* Fri Oct 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.12.1-1.2
- rebuild with new gmp without compat lib

* Tue Oct 11 2011 Peter Schiffer <pschiffe@redhat.com> - 0.12.1-1.1
- rebuild with new gmp

* Tue Sep 20 2011 Jens Petersen <petersen@redhat.com> - 0.12.1-1
- update to 0.12.1
- add _isa suffix to gtk2-devel depends (see #723558)

* Tue Jun 21 2011 Jens Petersen <petersen@redhat.com> - 0.12.0-5
- BR ghc-Cabal-devel instead of ghc-prof and use ghc_arches (cabal2spec-0.23.2)

* Thu Mar 10 2011 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.12.0-4
- Enable build on sparcv9

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 18 2011 Jens Petersen <petersen@redhat.com> - 0.12.0-2
- update to cabal2spec-0.22.4

* Tue Nov 30 2010 Jens Petersen <petersen@redhat.com> - 0.12.0-1
- update to 0.12.0

* Thu Nov 25 2010 Jens Petersen <petersen@redhat.com> - 0.11.2-3
- fix build with Cabal-1.10: add ghc7-Gtk2HsSetup-Cabal-1.10.patch

* Tue Sep  7 2010 Jens Petersen <petersen@redhat.com> - 0.11.2-2
- rebuild against ghc-glib-0.11.2

* Wed Sep  1 2010 Jens Petersen <petersen@redhat.com> - 0.11.2-1
- update to 0.11.2
- move demo into devel doc

* Fri Jul 16 2010 Jens Petersen <petersen@redhat.com> - 0.11.0-2
- use ghc-rpm-macros-0.8.1 so devel provides doc

* Tue Jul 13 2010 Jens Petersen <petersen@redhat.com> - 0.11.0-1
- license is LGPLv2+
- description
- depends on ghc-glib-devel, ghc-cairo-devel, and pango-devel
- BR gtk2hs-buildtools
- support hscolour

* Tue Jul 13 2010 Fedora Haskell SIG <haskell-devel@lists.fedoraproject.org> - 0.11.0-0
- initial packaging for Fedora automatically generated by cabal2spec-0.22.1
