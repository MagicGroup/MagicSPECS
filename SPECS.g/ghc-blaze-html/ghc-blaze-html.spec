# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name blaze-html

%bcond_with tests

# no useful debuginfo for Haskell packages without C sources
%global debug_package %{nil}

Name:           ghc-%{pkg_name}
Version:        0.7.0.3
Release:        4%{?dist}
Summary:        A blazingly fast HTML combinator library for Haskell

License:        BSD
URL:            http://hackage.haskell.org/package/%{pkg_name}
Source0:        http://hackage.haskell.org/package/%{pkg_name}-%{version}/%{pkg_name}-%{version}.tar.gz

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
# Begin cabal-rpm deps:
BuildRequires:  ghc-blaze-builder-devel
BuildRequires:  ghc-blaze-markup-devel
BuildRequires:  ghc-bytestring-devel
BuildRequires:  ghc-text-devel
%if %{with tests}
BuildRequires:  ghc-HUnit-devel
BuildRequires:  ghc-QuickCheck-devel
BuildRequires:  ghc-containers-devel
BuildRequires:  ghc-test-framework-devel
BuildRequires:  ghc-test-framework-hunit-devel
BuildRequires:  ghc-test-framework-quickcheck2-devel
%endif
# End cabal-rpm deps

%description
A blazingly fast HTML combinator library for the Haskell programming language.
It embeds HTML templates in Haskell code for optimal efficiency and
composability.  The project is aimed at those who seek to write
web applications in Haskell — it integrates well with Haskell web frameworks.


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
%if %{with tests}
%cabal test
%endif


%post devel
%ghc_pkg_recache


%postun devel
%ghc_pkg_recache


%files -f %{name}.files
%doc LICENSE
%{_docdir}/%{name}-%{version}/LICENSE

%files devel -f %{name}-devel.files


%changelog
* Sun Nov 08 2015 Liu Di <liudidi@gmail.com> - 0.7.0.3-4
- 为 Magic 3.0 重建

* Sun Sep 20 2015 Liu Di <liudidi@gmail.com> - 0.7.0.3-3
- 为 Magic 3.0 重建

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Sep 25 2014 Jens Petersen <petersen@redhat.com> - 0.7.0.3-1
- update to 0.7.0.3
- refresh to cblrpm-0.8.11

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 10 2013 Jens Petersen <petersen@redhat.com> - 0.6.1.1-1
- update to 0.6.1.1
- update to new simplified Haskell Packaging Guidelines

* Mon Mar 11 2013 Jens Petersen <petersen@redhat.com> - 0.6.0.0-1
- update to 0.6.0.0

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 19 2012 Jens Petersen <petersen@redhat.com> - 0.5.1.0-1
- update to 0.5.1.0 with cabal-rpm

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.3.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Jens Petersen <petersen@redhat.com> - 0.4.3.4-2
- change prof BRs to devel

* Wed Jun 13 2012 Jens Petersen <petersen@redhat.com> - 0.4.3.4-1
- update to 0.4.3.4

* Thu Mar 22 2012 Jens Petersen <petersen@redhat.com> - 0.4.3.1-3
- rebuild

* Thu Mar  1 2012 Jens Petersen <petersen@redhat.com> - 0.4.3.1-2
- rebuild

* Thu Jan  5 2012 Jens Petersen <petersen@redhat.com> - 0.4.3.1-1
- update to 0.4.3.1 and cabal2spec-0.25.2

* Thu Oct 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.4.2.0-1.2
- rebuild with new gmp without compat lib

* Tue Oct 11 2011 Peter Schiffer <pschiffe@redhat.com> - 0.4.2.0-1.1
- rebuild with new gmp

* Mon Oct  3 2011 Jens Petersen <petersen@redhat.com> - 0.4.2.0-1
- update to 0.4.2.0

* Wed Sep 28 2011 Jens Petersen <petersen@redhat.com> - 0.4.1.7-1
- update to 0.4.1.7

* Thu Aug  4 2011 Jens Petersen <petersen@redhat.com> - 0.4.1.6-1
- update to 0.4.1.6

* Sat Jun 18 2011 Jens Petersen <petersen@redhat.com> - 0.4.1.4-1
- update to 0.4.1.4

* Wed Jun 15 2011 Jens Petersen <petersen@redhat.com> - 0.4.1.3-1
- update to 0.4.1.3
- cabal2spec-0.23

* Tue May  3 2011 Jens Petersen <petersen@redhat.com> - 0.4.1.1-1
- update to 0.4.1.1
- cabal2spec-0.22.6

* Sat Mar 26 2011 Jens Petersen <petersen@redhat.com> - 0.4.1.0-1
- BSD license
- depends on ghc-text and ghc-blaze-builder

* Sat Mar 26 2011 Fedora Haskell SIG <haskell-devel@lists.fedoraproject.org> - 0.4.1.0-0
- initial packaging for Fedora automatically generated by cabal2spec-0.22.5
