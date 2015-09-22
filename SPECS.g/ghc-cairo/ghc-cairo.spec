# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name cairo

Name:           ghc-%{pkg_name}
Version:        0.13.0.6
Release:        3%{?dist}
Summary:        Binding to the Cairo library

License:        BSD
Url:            https://hackage.haskell.org/package/%{pkg_name}
Source0:        https://hackage.haskell.org/package/%{pkg_name}-%{version}/%{pkg_name}-%{version}.tar.gz

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
# Begin cabal-rpm deps:
BuildRequires:  ghc-array-devel
BuildRequires:  ghc-bytestring-devel
BuildRequires:  ghc-mtl-devel
BuildRequires:  ghc-text-devel
BuildRequires:  ghc-utf8-string-devel
BuildRequires:  gtk2hs-buildtools
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(cairo-pdf)
BuildRequires:  pkgconfig(cairo-ps)
BuildRequires:  pkgconfig(cairo-svg)
# End cabal-rpm deps

%description
Cairo is a library to render high quality vector graphics. There exist various
backends that allows rendering to Gtk windows, PDF, PS, PNG and SVG documents,
amongst others.


%package devel
Summary:        Haskell %{pkg_name} library development files
Provides:       %{name}-static = %{version}-%{release}
Requires:       ghc-compiler = %{ghc_version}
Requires(post): ghc-compiler = %{ghc_version}
Requires(postun): ghc-compiler = %{ghc_version}
Requires:       %{name}%{?_isa} = %{version}-%{release}
# Begin cabal-rpm deps:
Requires:       pkgconfig(cairo)
Requires:       pkgconfig(cairo-pdf)
Requires:       pkgconfig(cairo-ps)
Requires:       pkgconfig(cairo-svg)
# End cabal-rpm deps

%description devel
This package provides the Haskell %{pkg_name} library development files.


%prep
%setup -q -n %{pkg_name}-%{version}


%build
%ghc_lib_build


%install
%ghc_lib_install

rm -r %{buildroot}%{_datadir}/%{pkg_name}-%{version}


%post devel
%ghc_pkg_recache


%postun devel
%ghc_pkg_recache


%files -f %{name}.files
%doc COPYRIGHT
%{_docdir}/%{name}-%{version}/COPYRIGHT

%files devel -f %{name}-devel.files
%doc demo


%changelog
* Sun Sep 20 2015 Liu Di <liudidi@gmail.com> - 0.13.0.6-3
- 为 Magic 3.0 重建

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jan 19 2015 Jens Petersen <petersen@redhat.com> - 0.13.0.6-1
- update to 0.13.0.6

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
- use upstream summary and description

* Sat Nov 17 2012 Jens Petersen <petersen@redhat.com> - 0.12.4-1
- update to 0.12.4

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Jens Petersen <petersen@redhat.com> - 0.12.3.1-2
- change prof BRs to devel

* Wed Jun 13 2012 Jens Petersen <petersen@redhat.com> - 0.12.3.1-1
- update to 0.12.3.1

* Tue Mar 20 2012 Jens Petersen <petersen@redhat.com> - 0.12.3-1
- update to 0.12.3

* Wed Jan  4 2012 Jens Petersen <petersen@redhat.com> - 0.12.2-1
- update to 0.12.2 and cabal2spec-0.25.2

* Thu Oct 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.12.1-1.2
- rebuild with new gmp without compat lib

* Tue Oct 11 2011 Peter Schiffer <pschiffe@redhat.com> - 0.12.1-1.1
- rebuild with new gmp

* Tue Sep 20 2011 Jens Petersen <petersen@redhat.com> - 0.12.1-1
- update to 0.12.1

* Tue Jun 21 2011 Jens Petersen <petersen@redhat.com> - 0.12.0-5
- use BR ghc-Cabal-devel instead of ghc-prof (cabal2spec-0.23.1)

* Thu Mar 10 2011 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.12.0-4
- Enable build on sparcv9

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 18 2011 Jens Petersen <petersen@redhat.com> - 0.12.0-2
- update to cabal2spec-0.22.4

* Tue Nov 30 2010 Jens Petersen <petersen@redhat.com> - 0.12.0-1
- update to 0.12.0
- Gtk2HsSetup patch no longer needed

* Thu Nov 25 2010 Jens Petersen <petersen@redhat.com> - 0.11.1-2
- add ghc-cairo-Gtk2HsSetup-Cabal-1.10.patch to fix build

* Thu Aug 19 2010 Jens Petersen <petersen@redhat.com> - 0.11.1-1
- update to 0.11.1

* Fri Jul 16 2010 Jens Petersen <petersen@redhat.com> - 0.11.0-2
- use ghc-rpm-macros-0.8.1 so devel provides doc

* Wed Jun 30 2010 Jens Petersen <petersen@redhat.com> - 0.11.0-1
- description and license
- buildrequires gtk2hs-buildtools
- support hscolour
- buildrequires ghc-mtl-devel and cairo-devel

* Wed Jun 30 2010 Fedora Haskell SIG <haskell-devel@lists.fedoraproject.org> - 0.11.0-0
- initial packaging for Fedora automatically generated by cabal2spec-0.22.1
