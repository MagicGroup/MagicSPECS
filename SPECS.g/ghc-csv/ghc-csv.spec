# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name csv

Name:           ghc-%{pkg_name}
Version:        0.1.2
Release:        25%{?dist}
Summary:        CSV loader and dumper

License:        MIT
Url:            https://hackage.haskell.org/package/%{pkg_name}
Source0:        https://hackage.haskell.org/package/%{pkg_name}-%{version}/%{pkg_name}-%{version}.tar.gz

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
# Begin cabal-rpm deps:
BuildRequires:  ghc-filepath-devel
BuildRequires:  ghc-parsec-devel
# End cabal-rpm deps

%description
This library parses and dumps documents that are formatted
according to RFC 4180, "The common Format and MIME Type for
Comma-Separated Values (CSV) Files". This format is used,
among many other things, as a lingua franca for spreadsheets,
and for certain web services.


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
%doc COPYING
%{_docdir}/%{name}-%{version}/COPYING

%files devel -f %{name}-devel.files


%changelog
* Sun Nov 08 2015 Liu Di <liudidi@gmail.com> - 0.1.2-25
- 为 Magic 3.0 重建

* Sun Sep 20 2015 Liu Di <liudidi@gmail.com> - 0.1.2-24
- 为 Magic 3.0 重建

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jan 27 2015 Jens Petersen <petersen@fedoraproject.org> - 0.1.2-22
- cblrpm refresh

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 07 2013 Jens Petersen <petersen@redhat.com> - 0.1.2-18
- update to new simplified Haskell Packaging Guidelines

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Nov 17 2012 Jens Petersen <petersen@redhat.com> - 0.1.2-16
- update with cabal-rpm

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 15 2012 Jens Petersen <petersen@redhat.com> - 0.1.2-14
- rebuild

* Sun Mar 18 2012 Jens Petersen <petersen@redhat.com> - 0.1.2-13
- correct new license to MIT
- update to cabal2spec-0.25

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2-12.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Oct 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.1.2-11.2
- rebuild with new gmp without compat lib

* Tue Oct 11 2011 Peter Schiffer <pschiffe@redhat.com> - 0.1.2-11.1
- rebuild with new gmp

* Sat Jul 09 2011 Ben Boeckel <mathstuf@gmail.com> - 0.1.2-11
- Update to cabal2spec-0.24

* Fri Jun 24 2011 Jens Petersen <petersen@redhat.com> - 0.1.2-10
- BR ghc-Cabal-devel instead of ghc-prof and use ghc_arches (cabal2spec-0.23.2)

* Wed May 11 2011 Ben Boeckel <mathstuf@gmail.com> - 0.1.2-9
- Update to cabal2spec-0.22.7

* Thu Mar 10 2011 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.1.2-8
- Enable build on sparcv9

* Thu Feb 17 2011 Ben Boeckel <mathstuf@gmail.com> - 0.1.2-7
- Rebuild for broken dependencies

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 15 2011 Ben Boeckel <mathstuf@gmail.com> - 0.1.2-5
- Update to cabal2spec-0.22.4
- Rebuild

* Sun Dec  5 2010 Jens Petersen <petersen@redhat.com> - 0.1.2-4
- rebuild

* Sun Nov 28 2010 Ben Boeckel <mathstuf@gmail.com> - 0.1.2-3
- Rebuild for GHC7

* Wed Nov 10 2010 Ben Boeckel <mathstuf@gmail.com> - 0.1.2-2
- Update to 0.1.2

* Sun Nov 07 2010 Ben Boeckel <mathstuf@gmail.com> - 0.1.1-2
- Rebuild

* Fri Sep 03 2010 Ben Boeckel <mathstuf@gmail.com> - 0.1.1-1
- Initial package

* Fri Sep  3 2010 Fedora Haskell SIG <haskell-devel@lists.fedoraproject.org> - 0.1.1-0
- initial packaging for Fedora automatically generated by cabal2spec-0.22.2
