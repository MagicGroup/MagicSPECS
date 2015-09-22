# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name split

%bcond_without tests

Name:           ghc-%{pkg_name}
# part of haskell-platform-2012.4+
Version:        0.2.2
Release:        6%{?dist}
Summary:        Combinator library for splitting lists

License:        BSD
Url:            https://hackage.haskell.org/package/%{pkg_name}
Source0:        https://hackage.haskell.org/package/%{pkg_name}-%{version}/%{pkg_name}-%{version}.tar.gz

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
# Begin cabal-rpm deps:
%if %{with tests}
BuildRequires:  ghc-QuickCheck-devel
%endif
# End cabal-rpm deps

%description
A collection of various methods for splitting
lists into parts, akin to the \"split\" function
found in several mainstream languages. Here is
its tale:

Once upon a time the standard "Data.List" module
held no function for splitting a list into parts
according to a delimiter.  Many a brave
lambda-knight strove to add such a function, but
their striving was in vain, for Lo, the Supreme
Council fell to bickering amongst themselves what
was to be the essential nature of the One True
Function which could cleave a list in twain (or
thrain, or any required number of parts).

And thus came to pass the split package,
comprising divers functions for splitting a list
asunder, each according to its nature.  And the
Supreme Council had no longer any grounds for
argument, for the favored method of each was
contained therein.

To get started, see the "Data.List.Split" module.


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
%cabal_test


%post devel
%ghc_pkg_recache


%postun devel
%ghc_pkg_recache


%files -f %{name}.files
%doc LICENSE
%{_docdir}/%{name}-%{version}/LICENSE


%files devel -f %{name}-devel.files
%doc CHANGES README


%changelog
* Sun Sep 20 2015 Liu Di <liudidi@gmail.com> - 0.2.2-6
- 为 Magic 3.0 重建

* Mon Jan 26 2015 Jens Petersen <petersen@fedoraproject.org> - 0.2.2-5
- cblrpm refresh
- use cabal_test

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jun 04 2013 Jens Petersen <petersen@redhat.com> - 0.2.2-1
- update to 0.2.2
- update to new simplified Haskell Packaging Guidelines

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 27 2012 Jens Petersen <petersen@redhat.com> - 0.2.1.1-1
- update to 0.2.1.1, part of haskell-platform-2012.4

* Sat Nov 17 2012 Jens Petersen <petersen@redhat.com>
- update with cabal-rpm

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.4.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Jens Petersen <petersen@redhat.com> - 0.1.4.3-2
- change prof BRs to devel

* Wed Jun 13 2012 Jens Petersen <petersen@redhat.com> - 0.1.4.3-1
- update to 0.1.4.3

* Fri Mar 23 2012 Jens Petersen <petersen@redhat.com> - 0.1.4.2-2
- add license to ghc_files

* Fri Jan  6 2012 Jens Petersen <petersen@redhat.com> - 0.1.4.2-1
- update to 0.1.4.2 and cabal2spec-0.25.2

* Fri Oct 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.1.4-1.2
- rebuild with new gmp without compat lib

* Tue Oct 11 2011 Peter Schiffer <pschiffe@redhat.com> - 0.1.4-1.1
- rebuild with new gmp

* Sat Jul 09 2011 Ben Boeckel <mathstuf@gmail.com> - 0.1.4-1
- Update to 0.1.4
- Update to cabal2spec-0.24

* Fri Jun 24 2011 Jens Petersen <petersen@redhat.com> - 0.1.3-5
- BR ghc-Cabal-devel instead of ghc-prof and use ghc_arches (cabal2spec-0.23.2)

* Thu Mar 10 2011 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.1.3-4
- Enable build on sparcv9

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 15 2011 Ben Boeckel <mathstuf@gmail.com> - 0.1.3-2
- Update to cabal2spec-0.22.4
- Rebuild

* Fri Dec 17 2010 Ben Boeckel <mathstuf@gmail.com> - 0.1.3-1
- Update to 0.1.3

* Sun Nov 28 2010 Ben Boeckel <mathstuf@gmail.com> - 0.1.2.3-1
- Update to 0.1.2.3

* Fri Nov 12 2010 Ben Boeckel <mathstuf@gmail.com> - 0.1.2.2-1
- Update to 0.1.2.2

* Sun Nov 07 2010 Ben Boeckel <mathstuf@gmail.com> - 0.1.2.1-2
- Rebuild

* Tue Sep 14 2010 Ben Boeckel <mathstuf@gmail.com> - 0.1.2.1-1
- Update to 0.1.2.1

* Sun Sep 05 2010 Ben Boeckel <mathstuf@gmail.com> - 0.1.2-1
- Initial package

* Sun Sep  5 2010 Fedora Haskell SIG <haskell-devel@lists.fedoraproject.org> - 0.1.2-0
- initial packaging for Fedora automatically generated by cabal2spec-0.22.2
