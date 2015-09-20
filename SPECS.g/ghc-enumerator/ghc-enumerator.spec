# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name enumerator

# no useful debuginfo for Haskell packages without C sources
%global debug_package %{nil}

Name:           ghc-%{pkg_name}
Version:        0.4.20
Release:        2%{?dist}
Summary:        Reliable, high-performance processing with left-fold enumerators

License:        MIT
URL:            http://hackage.haskell.org/package/%{pkg_name}
Source0:        http://hackage.haskell.org/package/%{pkg_name}-%{version}/%{pkg_name}-%{version}.tar.gz

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
# Begin cabal-rpm deps:
BuildRequires:  ghc-bytestring-devel
BuildRequires:  ghc-containers-devel
BuildRequires:  ghc-text-devel
BuildRequires:  ghc-transformers-devel
# End cabal-rpm deps

%description
Enumerators are an efficient, predictable, and safe alternative to lazy I/O.
Discovered by Oleg Kiselyov, they allow large datasets to be processed
in near-constant space by pure code. Although somewhat more complex to write,
using enumerators instead of lazy I/O produces more correct programs.

This library contains an enumerator implementation for Haskell, designed to
be both simple and efficient. Three core types are defined, along with
numerous helper functions:

* /Iteratee/: Data sinks, analogous to left folds. Iteratees consume
a sequence of /input/ values, and generate a single /output/ value.
Many iteratees are designed to perform side effects (such as printing to
stdout), so they can also be used as monad transformers.

* /Enumerator/: Data sources, which generate input sequences. Typical
enumerators read from a file handle, socket, random number generator, or
other external stream. To operate, enumerators are passed an iteratee, and
provide that iteratee with input until either the iteratee has completed its
computation, or EOF.

* /Enumeratee/: Data transformers, which operate as both enumerators and
iteratees. Enumeratees read from an /outer/ enumerator, and provide the
transformed data to an /inner/ iteratee.


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
%doc license.txt


%files devel -f %{name}-devel.files
%doc examples


%changelog
* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Aug 28 2014 Jens Petersen <petersen@redhat.com> - 0.4.20-1
- update to 0.4.20

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.19-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul  8 2014 Jens Petersen <petersen@redhat.com> - 0.4.19-8
- update to cblrpm-0.8.11

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.19-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 07 2013 Jens Petersen <petersen@redhat.com> - 0.4.19-6
- update to new simplified Haskell Packaging Guidelines

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.19-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Nov 17 2012 Jens Petersen <petersen@redhat.com> - 0.4.19-4
- update with cabal-rpm

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Jens Petersen <petersen@redhat.com> - 0.4.19-2
- change prof BRs to devel

* Sat Jun  9 2012 Jens Petersen <petersen@redhat.com> - 0.4.19-1
- update to 0.4.19

* Thu Mar 22 2012 Jens Petersen <petersen@redhat.com> - 0.4.18-2
- add license to ghc_files

* Tue Feb 28 2012 Ben Boeckel <mathstuf@gmail.com> - 0.4.18-1
- Update to 0.4.18

* Thu Jan  5 2012 Jens Petersen <petersen@redhat.com> - 0.4.17-1
- update to 0.4.17 and cabal2spec-0.25.2

* Sat Oct 29 2011 Jens Petersen <petersen@redhat.com> - 0.4.15-1
- update to 0.4.15

* Thu Oct 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.4.13.1-2.2
- rebuild with new gmp without compat lib

* Tue Oct 11 2011 Peter Schiffer <pschiffe@redhat.com> - 0.4.13.1-2.1
- rebuild with new gmp

* Mon Jul 25 2011 Ben Boeckel <mathstuf@gmail.com> - 0.4.13.1-2
- Update to cabal2spec-0.24

* Fri Jul 22 2011 Jens Petersen <petersen@redhat.com> - 0.4.13.1-1
- update to 0.4.13.1

* Thu Jun 23 2011 Jens Petersen <petersen@redhat.com> - 0.4.10-3
- BR ghc-Cabal-devel instead of ghc-prof and use ghc_arches (cabal2spec-0.23.2)

* Wed May 11 2011 Ben Boeckel <mathstuf@gmail.com> - 0.4.10-2
- Add missing ppc64 ExclusiveArch

* Wed May 11 2011 Ben Boeckel <mathstuf@gmail.com> - 0.4.10-1
- Update to cabal2spec-0.22.7
- Update to 0.4.10

* Thu Mar 10 2011 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.4.7-2
- Enable build on sparcv9

* Thu Feb 17 2011 Ben Boeckel <mathstuf@gmail.com> - 0.4.7-1
- Update to 0.4.7

* Thu Feb 17 2011 Ben Boeckel <mathstuf@gmail.com> - 0.4.5-3
- Rebuild for broken dependencies

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 15 2011 Ben Boeckel <mathstuf@gmail.com> - 0.4.5-1
- Update to 0.4.5

* Sat Jan 15 2011 Ben Boeckel <mathstuf@gmail.com> - 0.4.4-2
- Update to cabal2spec-0.22.4
- Rebuild

* Fri Dec 17 2010 Ben Boeckel <mathstuf@gmail.com> - 0.4.4-1
- Update to 0.4.4

* Fri Dec 10 2010 Ben Boeckel <mathstuf@gmail.com> - 0.4.3.1-1
- Update to 0.4.3.1

* Sat Oct 30 2010 Ben Boeckel <mathstuf@gmail.com> - 0.4.2-1
- Update to 0.4.2

* Sat Sep 04 2010 Ben Boeckel <mathstuf@gmail.com> - 0.4.0.1-1
- Initial package

* Sat Sep  4 2010 Fedora Haskell SIG <haskell-devel@lists.fedoraproject.org> - 0.4.0.1-0
- initial packaging for Fedora automatically generated by cabal2spec-0.22.2
