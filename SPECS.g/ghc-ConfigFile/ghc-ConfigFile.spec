# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name ConfigFile

# no useful debuginfo for Haskell packages without C sources
%global debug_package %{nil}

Name:           ghc-%{pkg_name}
Version:        1.1.4
Release:        4%{?dist}
Summary:        Configuration file reading and writing

License:        BSD or LGPLv2+
Url:            https://hackage.haskell.org/package/%{pkg_name}
Source0:        https://hackage.haskell.org/package/%{pkg_name}-%{version}/%{pkg_name}-%{version}.tar.gz

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
# Begin cabal-rpm deps:
BuildRequires:  ghc-MissingH-devel
BuildRequires:  ghc-containers-devel
BuildRequires:  ghc-mtl-devel
BuildRequires:  ghc-parsec-devel
# End cabal-rpm deps

%description
Parser and writer for handling sectioned config files in Haskell.

The ConfigFile module works with configuration files in a standard format that
is easy for the user to edit, easy for the programmer to work with, yet remains
powerful and flexible. It is inspired by, and compatible with, Python's
ConfigParser module. It uses files that resemble Windows .INI-style files, but
with numerous improvements.

ConfigFile provides simple calls to both read and write config files.
It's possible to make a config file parsable by this module, the Unix shell,
and make.


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
%doc COPYRIGHT LGPL-2.1
%{_docdir}/%{name}-%{version}/COPYRIGHT

%files devel -f %{name}-devel.files
%doc README


%changelog
* Sun Nov 08 2015 Liu Di <liudidi@gmail.com> - 1.1.4-4
- 为 Magic 3.0 重建

* Sun Sep 20 2015 Liu Di <liudidi@gmail.com> - 1.1.4-3
- 为 Magic 3.0 重建

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jan 19 2015 Jens Petersen <petersen@redhat.com> - 1.1.4-1
- update to 1.1.4
- now dual licensed BSD or LGPL

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 07 2013 Jens Petersen <petersen@redhat.com> - 1.1.1-8
- update to new simplified Haskell Packaging Guidelines

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Nov 17 2012 Jens Petersen <petersen@redhat.com> - 1.1.1-6
- update with cabal-rpm

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Jens Petersen <petersen@redhat.com> - 1.1.1-4
- change prof BRs to devel

* Fri Jun 15 2012 Jens Petersen <petersen@redhat.com> - 1.1.1-3
- rebuild

* Wed Jan  4 2012 Jens Petersen <petersen@redhat.com> - 1.1.1-2
- update to cabal2spec-0.25.2

* Sat Dec  3 2011 Jens Petersen <petersen@redhat.com> - 1.1.1-1
- update to 1.1.1

* Mon Oct 24 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.0.6-7.3
- rebuild with new gmp without compat lib

* Thu Oct 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.0.6-7.2
- rebuild with new gmp without compat lib

* Tue Oct 11 2011 Peter Schiffer <pschiffe@redhat.com> - 1.0.6-7.1
- rebuild with new gmp

* Mon Sep 26 2011 Jens Petersen <petersen@redhat.com> - 1.0.6-7
- rebuild against MissingH-1.1.1.0 and BR haskell98

* Mon Aug 29 2011 Jens Petersen <petersen@redhat.com> - 1.0.6-6
- rebuild for hslogger-1.1.5

* Wed Jun 22 2011 Jens Petersen <petersen@redhat.com> - 1.0.6-5
- BR ghc-Cabal-devel instead of ghc-prof and use ghc_arches (cabal2spec-0.23.2)

* Wed Mar 16 2011 Jens Petersen <petersen@redhat.com> - 1.0.6-4
- update to cabal2spec-0.22.5

* Sat Jan 29 2011 Jens Petersen <petersen@redhat.com> - 1.0.6-3
- update to cabal2spec-0.22.4

* Wed Sep 15 2010 Jens Petersen <petersen@redhat.com> - 1.0.6-2
- include the COPYRIGHT file too

* Sun Sep 05 2010 Ben Boeckel <mathstuf@gmail.com> - 1.0.6-1
- Initial package

* Sun Sep  5 2010 Fedora Haskell SIG <haskell-devel@lists.fedoraproject.org> - 1.0.6-0
- initial packaging for Fedora automatically generated by cabal2spec-0.22.2
