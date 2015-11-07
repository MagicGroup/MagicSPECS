# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name cpphs

Name:           %{pkg_name}
Version:        1.18.9
Release:        4%{?dist}
Summary:        A liberalised C pre-processor for Haskell

License:        GPL+ and LGPLv2+ or BSD
URL:            http://hackage.haskell.org/package/%{name}
Source0:        http://hackage.haskell.org/package/%{name}-%{version}/%{name}-%{version}.tar.gz

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
# Begin cabal-rpm deps:
BuildRequires:  ghc-directory-devel
BuildRequires:  ghc-old-locale-devel
BuildRequires:  ghc-old-time-devel
BuildRequires:  ghc-polyparse-devel
# End cabal-rpm deps

%description
Cpphs is a re-implementation of the C pre-processor that is both
more compatible with Haskell, and itself written in Haskell so
that it can be distributed with compilers.

This version of the C pre-processor is pretty-much
feature-complete and compatible with traditional (K&R)
pre-processors.  Additional features include: a plain-text mode;
an option to unlit literate code files; and an option to turn
off macro-expansion.


%package -n ghc-%{name}
Summary:        Haskell %{name} library
License:        LGPLv2+ or BSD

%description -n ghc-%{name}
This package provides the Haskell %{name} shared library.


%package -n ghc-%{name}-devel
Summary:        Haskell %{name} library development files
License:        LGPLv2+ or BSD
Provides:       ghc-%{name}-static = %{version}-%{release}
Requires:       ghc-compiler = %{ghc_version}
Requires(post): ghc-compiler = %{ghc_version}
Requires(postun): ghc-compiler = %{ghc_version}
Requires:       ghc-%{name}%{?_isa} = %{version}-%{release}

%description -n ghc-%{name}-devel
This package provides the Haskell %{name} library development files.


%prep
%setup -q


%build
%ghc_lib_build


%install
%ghc_lib_install
rm %{buildroot}%{_docdir}/%{name}*/LICENCE-LGPL

install -D -p -m 0644 docs/cpphs.1 %{buildroot}%{_mandir}/man1/%{name}.1


%post -n ghc-%{name}-devel
%ghc_pkg_recache


%postun -n ghc-%{name}-devel
%ghc_pkg_recache


%files
%doc LICENCE-GPL README docs/index.html
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*


%files -n ghc-%{name} -f ghc-%{name}.files
%doc LICENCE-LGPL LICENCE-GPL


%files -n ghc-%{name}-devel -f ghc-%{name}-devel.files
%doc README


%changelog
* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 1.18.9-4
- 为 Magic 3.0 重建

* Mon Sep 21 2015 Liu Di <liudidi@gmail.com> - 1.18.9-3
- 为 Magic 3.0 重建

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.18.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Apr  2 2015 Jens Petersen <petersen@redhat.com> - 1.18.9-1
- update to 1.18.9

* Fri Aug 29 2014 Jens Petersen <petersen@redhat.com> - 1.18.2-1
- update to 1.18.2
- refresh to cblrpm-0.8.11
- add alternative BSD license tag: cpphs has been dual licensed for a while

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.16-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.16-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Oct 25 2013 Jens Petersen <petersen@redhat.com> - 1.16-5
- replace ghc_docdir by _pkgdocdir

* Fri Jul 26 2013 Jens Petersen <petersen@redhat.com> - 1.16-4
- use ghc_docdir to handle F20 unversioned docdir

* Tue Jun 11 2013 Jens Petersen <petersen@redhat.com>
- update to new approved simplified Haskell Packaging Guidelines

* Wed Apr 24 2013 Jens Petersen <petersen@redhat.com> - 1.16-2
- update to revised simplified Haskell Packaging Guidelines (cabal-rpm-0.8)

* Mon Mar 11 2013 Jens Petersen <petersen@redhat.com> - 1.16-1
- update to 1.16

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Nov 17 2012 Jens Petersen <petersen@redhat.com> - 1.14-3
- add LICENCE-GPL and manpage
- update with cabal-rpm

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Jens Petersen <petersen@redhat.com> - 1.14-1
- update to 1.14
- drop haskell98 BR

* Tue Feb  7 2012 Jens Petersen <petersen@redhat.com> - 1.13.3-1
- update to 1.13.3

* Thu Jan 19 2012 Jens Petersen <petersen@redhat.com> - 1.13.2-3
- update to cabal2spec-0.25.2, fixing anomalous ghc-cpphs requires ghc-compiler

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13.2-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Oct 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.13.2-1.1
- rebuild with new gmp without compat lib

* Sat Oct 15 2011 Jens Petersen <petersen@redhat.com> - 1.13.2-1
- update to 1.13.2
- update to cabal2spec-0.24.1
- use ghc_exclude_docdir from ghc-rpm-macros-0.13.12

* Fri Oct 14 2011 Jens Petersen <petersen@redhat.com> - 1.13.1-1
- update to 1.13.1

* Mon Oct 10 2011 Peter Schiffer <pschiffe@redhat.com> - 1.12-1.1
- rebuild with new gmp

* Fri Jul 22 2011 Jens Petersen <petersen@redhat.com> - 1.12-1
- update to 1.12
- missing LICENCE-GPL reported upstream

* Tue Jun 21 2011 Jens Petersen <petersen@redhat.com> - 1.11-10
- BR ghc-Cabal-devel instead of ghc-prof (cabal2spec-0.23.2)

* Thu Mar 10 2011 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.11-9
- Enable build on sparcv9

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 23 2011 Jens Petersen <petersen@redhat.com> - 1.11-7
- rebuild

* Sat Jan 15 2011 Jens Petersen <petersen@redhat.com> - 1.11-6
- update to cabal2spec-0.22.4

* Mon Nov 29 2010 Jens Petersen <petersen@redhat.com> - 1.11-5
- update url and drop -o obsoletes

* Sat Sep  4 2010 Jens Petersen <petersen@redhat.com> - 1.11-4
- update to ghc-rpm-macros-0.8.1, hscolour and drop doc pkg (cabal2spec-0.22.2)

* Sat Jun 26 2010 Jens Petersen <petersen@redhat.com> - 1.11-3
- strip dynlinked files (cabal2spec-0.21.4)

* Sat Apr 24 2010 Jens Petersen <petersen@redhat.com> - 1.11-2
- rebuild for ghc-6.12.2

* Mon Feb 15 2010 Conrad Meyer <konrad@tylerc.org> - 1.11-1
- Bump to 1.11

* Mon Jan 11 2010 Jens Petersen <petersen@redhat.com> - 1.9-4
- update to ghc-rpm-macros-0.5.1 and cabal2spec-0.21.1:
- drop doc and prof bcond
- common summary and common_description
- use ghc_binlib_package with license arg

* Wed Dec 23 2009 Jens Petersen <petersen@redhat.com> - 1.9-3
- devel package requires shared library not base

* Tue Dec 22 2009 Jens Petersen <petersen@redhat.com> - 1.9-2
- update spec for ghc-6.12.1
- added shared library support: needs ghc-rpm-macros 0.3.1
- drop -dynamic for now since Cabal chokes with prof looking for p_dyn
- use ghc-cpphs for ghc_gen_filelists

* Fri Sep 18 2009 Jens Petersen <petersen@redhat.com> - 1.9-1
- update to 1.9

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun May 17 2009 Jens Petersen <petersen@redhat.com> - 1.6-8
- buildrequires ghc-rpm-macros (cabal2spec-0.16)

* Fri Apr 24 2009 Jens Petersen <petersen@redhat.com> - 1.6-7
- update to cabal2spec-0.14

* Mon Mar  2 2009 Jens Petersen <petersen@redhat.com> - 1.6-6
- update to cabal2spec-0.12:
  - add devel subpackage
  - use global
  - update archs

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jan 19 2009 Conrad Meyer <konrad@tylerc.org> - 1.6-4
- update to new template (haskell-packaging 0.4-1)

* Wed Jan 14 2009 Jens Petersen <petersen@redhat.com> - 1.6-3
- simplify summaries
- move lgpl license file to ghc-cpphs
- add html doc

* Tue Jan 13 2009 Jens Petersen <petersen@redhat.com> - 1.6-2
- make this a proper binlib package
- use bcond

* Mon Jan 12 2009 Conrad Meyer <konrad@tylerc.org> - 1.6-1
- initial packaging for Fedora created by cabal2spec
