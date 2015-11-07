# https://fedoraproject.org/wiki/Packaging:Haskell

Name:           gtk2hs-buildtools
Version:        0.13.0.4
Release:        3%{?dist}
Summary:        Tools to build the Gtk2Hs suite of User Interface libraries

License:        GPLv2+
Url:            https://hackage.haskell.org/package/%{name}
Source0:        https://hackage.haskell.org/package/%{name}-%{version}/%{name}-%{version}.tar.gz

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
# Begin cabal-rpm deps:
BuildRequires:  alex
BuildRequires:  ghc-array-devel
BuildRequires:  ghc-containers-devel
BuildRequires:  ghc-directory-devel
BuildRequires:  ghc-filepath-devel
BuildRequires:  ghc-hashtables-devel
BuildRequires:  ghc-pretty-devel
BuildRequires:  ghc-process-devel
BuildRequires:  ghc-random-devel
BuildRequires:  happy
# End cabal-rpm deps

%description
This package provides a set of helper programs necessary to build the Gtk2Hs
suite of libraries. These tools include a modified c2hs binding tool that is
used to generate FFI declarations, a tool to build a type hierarchy that
mirrors the C type hierarchy of GObjects found in glib, and a generator for
signal declarations that are used to call back from C to Haskell.
These tools are not needed to actually run Gtk2Hs programs.


%prep
%setup -q


%build
%ghc_bin_build


%install
%ghc_bin_install

rm %buildroot%{ghc_pkgdocdir}/COPYING


%files
%license COPYING
%{_bindir}/gtk2hsC2hs
%{_bindir}/gtk2hsHookGenerator
%{_bindir}/gtk2hsTypeGen
%{_datadir}/%{name}-%{version}


%changelog
* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 0.13.0.4-3
- 为 Magic 3.0 重建

* Mon Sep 21 2015 Liu Di <liudidi@gmail.com> - 0.13.0.4-2
- 为 Magic 3.0 重建

* Mon Jun 29 2015 Jens Petersen <petersen@redhat.com> - 0.13.0.4-1
- update to 0.13.0.4
- remove aarch64 build-tools hacks
- use %%license

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Apr 10 2015 Jens Petersen <petersen@redhat.com> - 0.13.0.3-2
- workaround build-tools version check failures on aarch64 (#1210323)

* Fri Jan 23 2015 Jens Petersen <petersen@redhat.com> - 0.13.0.3-1
- update to 0.13.0.3

* Wed Aug 27 2014 Jens Petersen <petersen@redhat.com> - 0.13.0.1-1
- update to 0.13.0.1
- refresh to cblrpm-0.9
- disable debuginfo since no files generated for c2hs_config.c

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Dec 21 2013 Jens Petersen <petersen@redhat.com> - 0.12.5.1-1
- update to 0.12.5.1

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jun 19 2013 Jens Petersen <petersen@redhat.com> - 0.12.4-3
- update to cabal-rpm-0.8

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Nov 17 2012 Jens Petersen <petersen@redhat.com> - 0.12.4-1
- update to 0.12.4

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun  9 2012 Jens Petersen <petersen@redhat.com> - 0.12.3.1-1
- update to 0.12.3.1

* Fri Mar 23 2012 Jens Petersen <petersen@redhat.com> - 0.12.1-3
- depends on random
- update to cabal2spec-0.25

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.1-2.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Oct 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.12.1-1.2
- rebuild with new gmp without compat lib

* Tue Oct 11 2011 Peter Schiffer <pschiffe@redhat.com> - 0.12.1-1.1
- rebuild with new gmp

* Tue Sep 20 2011 Jens Petersen <petersen@redhat.com> - 0.12.1-1
- update to 0.12.1

* Tue Jun 21 2011 Jens Petersen <petersen@redhat.com> - 0.12.0-6
- ghc_arches replaces ghc_excluded_archs

* Tue Jun 21 2011 Jens Petersen <petersen@redhat.com> - 0.12.0-5
- BR ghc-Cabal-devel and use ghc_excluded_archs

* Thu Mar 10 2011 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.12.0-4
- Enable build on sparcv9

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 15 2011 Jens Petersen <petersen@redhat.com> - 0.12.0-2
- update to cabal2spec-0.22.4
- BR ghc-devel

* Mon Nov 29 2010 Jens Petersen <petersen@redhat.com> - 0.12.0-1
- update to 0.12.0

* Thu Nov 25 2010 Jens Petersen <petersen@redhat.com> - 0.11.2-2
- rebuild

* Mon Sep  6 2010 Jens Petersen <petersen@redhat.com> - 0.11.2-1
- update to 0.11.2

* Thu Aug 19 2010 Jens Petersen <petersen@redhat.com> - 0.11.1-1
- update to 0.11.1

* Wed Jun 30 2010 Jens Petersen <petersen@redhat.com> - 0.9-2
- buildrequires alex and happy

* Wed Jun 30 2010 Jens Petersen <petersen@redhat.com> - 0.9-1
- summary, description, license, group, and filelist

* Wed Jun 30 2010 Fedora Haskell SIG <haskell-devel@lists.fedoraproject.org> - 0.9-0
- initial packaging for Fedora automatically generated by cabal2spec-0.22.1
