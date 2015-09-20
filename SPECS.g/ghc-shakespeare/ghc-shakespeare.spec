# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name shakespeare

%bcond_with tests

# no useful debuginfo for Haskell packages without C sources
%global debug_package %{nil}

Name:           ghc-%{pkg_name}
Version:        2.0.1.1
Release:        4%{?dist}
Summary:        Toolkit for compile-time interpolated templates

License:        MIT
URL:            http://hackage.haskell.org/package/%{pkg_name}
Source0:        http://hackage.haskell.org/package/%{pkg_name}-%{version}/%{pkg_name}-%{version}.tar.gz

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
# Begin cabal-rpm deps:
BuildRequires:  ghc-aeson-devel
BuildRequires:  ghc-blaze-html-devel
BuildRequires:  ghc-blaze-markup-devel
BuildRequires:  ghc-bytestring-devel
BuildRequires:  ghc-containers-devel
BuildRequires:  ghc-directory-devel
BuildRequires:  ghc-exceptions-devel
BuildRequires:  ghc-parsec-devel
BuildRequires:  ghc-process-devel
BuildRequires:  ghc-system-fileio-devel
BuildRequires:  ghc-system-filepath-devel
BuildRequires:  ghc-template-haskell-devel
BuildRequires:  ghc-text-devel
BuildRequires:  ghc-time-devel
BuildRequires:  ghc-transformers-devel
ExclusiveArch:  %{ghc_arches_with_ghci}
%if %{with tests}
BuildRequires:  ghc-HUnit-devel
BuildRequires:  ghc-hspec-devel
%endif
# End cabal-rpm deps
Obsoletes:      ghc-hamlet < 1.3
Obsoletes:      ghc-shakespeare-css < 1.2
Obsoletes:      ghc-shakespeare-i18n < 1.2
Obsoletes:      ghc-shakespeare-js < 1.4
Obsoletes:      ghc-shakespeare-text < 1.2

%description
Shakespeare is a family of type-safe, efficient template languages.
Shakespeare templates are expanded at compile-time, ensuring that all
interpolated variables are in scope. Variables are interpolated according to
their type through a typeclass.

Shakespeare templates can be used inline with a quasi-quoter
or in an external file.

See the documentation at <http://www.yesodweb.com/book/shakespearean-templates>
for more details.


%package devel
Summary:        Haskell %{pkg_name} library development files
Provides:       %{name}-static = %{version}-%{release}
Requires:       ghc-compiler = %{ghc_version}
Requires(post): ghc-compiler = %{ghc_version}
Requires(postun): ghc-compiler = %{ghc_version}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Obsoletes:      ghc-hamlet-devel < 1.3
Obsoletes:      ghc-shakespeare-css-devel < 1.2
Obsoletes:      ghc-shakespeare-i18n-devel < 1.2
Obsoletes:      ghc-shakespeare-js-devel < 1.4
Obsoletes:      ghc-shakespeare-text-devel < 1.2

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


%files devel -f %{name}-devel.files


%changelog
* Tue Sep  8 2015 Peter Robinson <pbrobinson@fedoraproject.org> 2.0.1.1-4
- Rebuild (aarch64 hashes)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Mar  5 2015 Jens Petersen <petersen@redhat.com> - 2.0.1.1-2
- obsolete hamlet, shakespeare-css, shakespeare-i18n, shakespeare-js,
  shakespeare-text

* Wed Sep 17 2014 Jens Petersen <petersen@redhat.com> - 2.0.1.1-1
- update to 2.0.1.1

* Thu Aug 28 2014 Jens Petersen <petersen@redhat.com> - 1.2.1.1-1
- update to 1.2.1.1
- refresh to cblrpm-0.8.11

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Aug 30 2013 Jens Petersen <petersen@redhat.com> - 1.0.5.1-1
- update to 1.0.5.1

* Wed Aug 28 2013 Jens Petersen <petersen@redhat.com> - 1.0.5-1
- update to 1.0.5

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jun 04 2013 Jens Petersen <petersen@redhat.com> - 1.0.4-1
- update to 1.0.4
- update to new simplified Haskell Packaging Guidelines

* Tue Mar 12 2013 Jens Petersen <petersen@redhat.com> - 1.0.3.1-1
- update to 1.0.3.1

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Nov  7 2012 Jens Petersen <petersen@redhat.com> - 1.0.1.4-1
- update to 1.0.1.4
- license is now MIT

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Jens Petersen <petersen@redhat.com> - 1.0.0.2-2
- change prof BRs to devel

* Wed Jun 13 2012 Jens Petersen <petersen@redhat.com> - 1.0.0.2-1
- update to 1.0.0.2

* Thu Apr 26 2012 Jens Petersen <petersen@redhat.com> - 1.0.0.1-1
- update to 1.0.0.1

* Fri Mar 23 2012 Jens Petersen <petersen@redhat.com> - 0.11-1
- update to 0.11
- depends on text not blaze-html and failure

* Wed Mar  7 2012 Jens Petersen <petersen@redhat.com> - 0.10.3.1-1
- update to 0.10.3.1
- only build on ghc_arches_with_ghci

* Thu Jan  5 2012 Jens Petersen <petersen@redhat.com> - 0.10.2-2
- update to cabal2spec-0.25.2

* Tue Nov  1 2011 Jens Petersen <petersen@redhat.com> - 0.10.2-1
- update to 0.10.2

* Mon Oct 24 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.10.1.1-1.1
- rebuild with new gmp without compat lib

* Sat Oct  8 2011 Jens Petersen <petersen@redhat.com> - 0.10.1.1-1
- update to 0.10.1.1

* Thu Sep  8 2011 Jens Petersen <petersen@redhat.com> - 0.10.0-2
- BR ghc-*-prof

* Wed Sep  7 2011 Jens Petersen <petersen@redhat.com> - 0.10.0-1
- BSD license; deps

* Wed Sep  7 2011 Fedora Haskell SIG <haskell-devel@lists.fedoraproject.org> - 0.10.0-0
- initial packaging for Fedora automatically generated by cabal2spec-0.23.2
