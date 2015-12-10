# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name cmdargs

Name:           ghc-%{pkg_name}
Version:        0.10.12
Release:        4%{?dist}
Summary:        Command line argument processing

License:        BSD
Url:            https://hackage.haskell.org/package/%{pkg_name}
Source0:        https://hackage.haskell.org/package/%{pkg_name}-%{version}/%{pkg_name}-%{version}.tar.gz

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
# Begin cabal-rpm deps:
BuildRequires:  ghc-filepath-devel
BuildRequires:  ghc-process-devel
BuildRequires:  ghc-template-haskell-devel
BuildRequires:  ghc-transformers-devel
# End cabal-rpm deps

%description
This library provides an easy way to define command line parsers.


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
cabal-tweak-flag quotation False
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
%{_docdir}/%{name}-%{version}/LICENSE


%files devel -f %{name}-devel.files
%doc README.md


%changelog
* Sun Nov 08 2015 Liu Di <liudidi@gmail.com> - 0.10.12-4
- 为 Magic 3.0 重建

* Sun Sep 20 2015 Liu Di <liudidi@gmail.com> - 0.10.12-3
- 为 Magic 3.0 重建

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jan 19 2015 Jens Petersen <petersen@redhat.com> - 0.10.12-1
- update to 0.10.12

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Apr 24 2014 Jens Petersen <petersen@redhat.com> - 0.10.3-3
- disable quotation on archs without ghci

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 07 2013 Jens Petersen <petersen@redhat.com> - 0.10.3-1
- update to 0.10.3
- update to new simplified Haskell Packaging Guidelines

* Tue Mar 12 2013 Jens Petersen <petersen@redhat.com> - 0.10.2-1
- update to 0.10.2

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct 29 2012 Jens Petersen <petersen@redhat.com> - 0.10-1
- update to 0.10 with cabal-rpm
- disable building testprog in .cabal

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Jens Petersen <petersen@redhat.com> - 0.9.5-2
- change prof BRs to devel

* Sun Jun 10 2012 Jens Petersen <petersen@redhat.com> - 0.9.5-1
- update to 0.9.5
- disable dynamic linking of test program

* Sun Mar 18 2012 Jens Petersen <petersen@redhat.com> - 0.9.3-2
- update to cabal2spec-0.25

* Tue Feb 28 2012 Ben Boeckel <mathstuf@gmail.com> - 0.9.3-1
- Update to 0.9.3

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-2.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Oct 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.8-1.2
- rebuild with new gmp without compat lib

* Tue Oct 11 2011 Peter Schiffer <pschiffe@redhat.com> - 0.8-1.1
- rebuild with new gmp

* Mon Oct  3 2011 Jens Petersen <petersen@redhat.com> - 0.8-1
- update to 0.8 and cabal2spec-0.24.1

* Sat Jul 09 2011 Ben Boeckel <mathstuf@gmail.com> - 0.7-4
- Update to cabal2spec-0.24

* Fri Jun 24 2011 Jens Petersen <petersen@redhat.com> - 0.7-3
- BR ghc-Cabal-devel instead of ghc-prof and use ghc_arches (cabal2spec-0.23.2)

* Wed May 11 2011 Ben Boeckel <mathstuf@gmail.com> - 0.7-2
- Update to cabal2spec-0.22.7

* Tue May 10 2011 Ben Boeckel <mathstuf@gmail.com> - 0.7-1
- Update to cabal2spec-0.22.6

* Thu Mar 10 2011 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.6.8-2
- Enable build on sparcv9

* Thu Feb 17 2011 Ben Boeckel <mathstuf@gmail.com> - 0.6.8-1
- Update to 0.6.8

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 15 2011 Ben Boeckel <mathstuf@gmail.com> - 0.6.7-1
- Update to 0.6.7

* Sat Jan 15 2011 Ben Boeckel <mathstuf@gmail.com> - 0.6.5-2
- Update to cabal2spec-0.22.4
- Rebuild

* Fri Dec 17 2010 Ben Boeckel <mathstuf@gmail.com> - 0.6.5-1
- Update to 0.6.5

* Fri Dec 03 2010 Ben Boeckel <mathstuf@gmail.com> - 0.6.4-1
- Update to 0.6.4

* Mon Nov 29 2010 Jens Petersen <petersen@redhat.com> - 0.6.3-2
- BR transformers

* Fri Nov 12 2010 Ben Boeckel <mathstuf@gmail.com> - 0.6.3-1
- Update to 0.6.3

* Mon Oct 18 2010 Ben Boeckel <mathstuf@gmail.com> - 0.6.1-1
- Update to 0.6.1

* Sat Sep 18 2010 Ben Boeckel <mathstuf@gmail.com> - 0.6-1
- Update to 0.6

* Thu Sep 16 2010 Ben Boeckel <mathstuf@gmail.com> - 0.5-1
- Update to 0.5

* Sun Sep 05 2010 Ben Boeckel <mathstuf@gmail.com> - 0.4-1
- Update to 0.4

* Wed Sep 01 2010 Ben Boeckel <mathstuf@gmail.com> - 0.2-2
- Don't ship the demo program

* Wed Sep 01 2010 Ben Boeckel <mathstuf@gmail.com> - 0.2-1
- Initial package

* Wed Sep  1 2010 Fedora Haskell SIG <haskell-devel@lists.fedoraproject.org> - 0.2-0
- initial packaging for Fedora automatically generated by cabal2spec-0.22.2
