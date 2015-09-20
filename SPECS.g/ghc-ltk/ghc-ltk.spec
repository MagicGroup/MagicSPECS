# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name ltk

Name:           ghc-%{pkg_name}
Version:        0.14.3.0
Release:        3%{?dist}
Summary:        Leksah IDE's UI toolkit library

#The cabal file states license as GPLv2 while sources specify license
#as GPL. Hence GPL+.
License:        GPL+
Url:            https://hackage.haskell.org/package/%{pkg_name}
Source0:        https://hackage.haskell.org/package/%{pkg_name}-%{version}/%{pkg_name}-%{version}.tar.gz
Patch0:         ltk-0.14.3.0-ViewFrame-gtk2.patch

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
# Begin cabal-rpm deps:
BuildRequires:  ghc-containers-devel
BuildRequires:  ghc-filepath-devel
BuildRequires:  ghc-ghc-devel
BuildRequires:  ghc-glib-devel
BuildRequires:  ghc-gtk-devel
BuildRequires:  ghc-mtl-devel
BuildRequires:  ghc-parsec-devel
BuildRequires:  ghc-pretty-devel
BuildRequires:  ghc-text-devel
BuildRequires:  ghc-transformers-devel
# End cabal-rpm deps

%description
This package provides UI toolkit library for Leksah IDE.


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
%patch0 -p1 -b .orig
cabal-tweak-flag gtk3 False


%build
%ghc_lib_build


%install
%ghc_lib_install

rm %{buildroot}%{ghc_pkgdocdir}/LICENSE


%post devel
%ghc_pkg_recache


%postun devel
%ghc_pkg_recache


%files -f %{name}.files
%license LICENSE


%files devel -f %{name}-devel.files


%changelog
* Thu Jul 23 2015 Jens Petersen <petersen@redhat.com> - 0.14.3.0-3
- use license macro

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Feb 06 2015 Jens Petersen <petersen@redhat.com> - 0.14.3.0-1
- update to 0.14.3.0

* Tue Sep 16 2014 Jens Petersen <petersen@redhat.com> - 0.14.0.0-1
- update to 0.14.0.0

* Thu Aug 28 2014 Jens Petersen <petersen@redhat.com> - 0.13.2.0-1
- update to 0.13.2.0
- build with Haskell gtk until gtk3 in Fedora
- refresh to cblrpm-0.8.11

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.1.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.1.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Dec 21 2013 Jens Petersen <petersen@redhat.com> - 0.12.1.0-11
- rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.1.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jun 13 2013 Jens Petersen <petersen@redhat.com> - 0.12.1.0-9
- update to new simplified Haskell Packaging Guidelines
- patch from upstream git to build on ghc-7.6

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Nov 17 2012 Jens Petersen <petersen@redhat.com> - 0.12.1.0-7
- update with cabal-rpm
- does not depend on haddock

* Tue Oct 02 2012 Lakshmi Narasimhan T V <lakshminaras2002@gmail.com> - 0.12.1.0-6
- Rebuilt for haddock

* Tue Oct 02 2012 Lakshmi Narasimhan T V <lakshminaras2002@gmail.com> - 0.12.1.0-5
- Rebuilt for ghc-7.4.1

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Jens Petersen <petersen@redhat.com> - 0.12.1.0-3
- change prof BRs to devel

* Fri Jun 22 2012 Lakshmi Narasimhan T V <lakshminaras2002@gmail.com> - 0.12.1.0-2
- rebuild

* Sun Jun 10 2012 Jens Petersen <petersen@redhat.com> - 0.12.1.0-1
- update to 0.12.1.0

* Sun Mar 18 2012 Jens Petersen <petersen@redhat.com> - 0.12.0.0-2
- update to cabal2spec-0.25

* Mon Mar 12 2012 Lakshmi Narasimhan T V <lakshminaras2002@gmail.com> - 0.12.0.0-1
- package update to 0.12.0.0

* Mon Jan 2 2012 Lakshmi Narasimhan T V <lakshminaras2002@gmail.com> - 0.10.0.4-5
- rebuild for haddock

* Mon Oct 24 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.10.0.4-4.3
- rebuild with new gmp without compat lib

* Fri Oct 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.10.0.4-4.2
- rebuild with new gmp without compat lib

* Tue Oct 11 2011 Peter Schiffer <pschiffe@redhat.com> - 0.10.0.4-4.1
- rebuild with new gmp

* Sun Sep 25 2011 Lakshmi Narasimhan T V <lakshminaras2002@gmail.com> - 0.10.0.4-4
- Rebuild for gtk2hs related updates
- Update to cabal2spec-0.24.1

* Tue Jun 21 2011 Lakshmi Narasimhan T V <lakshminaras2002@gmail.com> - 0.10.0.4-3
- Update to cabal2spec-0.23.2

* Sat May 21 2011 Lakshmi Narasimhan T V <lakshminaras2002@gmail.com> - 0.10.0.4-2
- Updated spec file to cabal2spec 0.22.7
- License is GPL+. The cabal file states license as GPLv2 while sources specify license
- as GPL. Hence GPL+.
- Removed patch as it is not needed.

* Sun May 1 2011 Lakshmi Narasimhan T V <lakshminaras2002@gmail.com> - 0.10.0.4-1
- Package updated to 0.10.0.4

* Tue Apr 12 2011 Lakshmi Narasimhan T V <lakshminaras2002@gmail.com> - 0.10.0-1
- Package update.cabal file patch to fix build issue on F15 and greater.

* Thu Mar 24 2011 Lakshmi Narasimhan T V <lakshminaras2002@gmail.com> - 0.8.0.8-2
- Upgrade to cabal2spec 0.22.5

* Sun Oct 10 2010 Lakshmi Narasimhan T V <lakshminaras2002@gmail.com> - 0.8.0.8-1
- Modify license details, summary, description and added dependencies.

* Sun Oct 10 2010 Fedora Haskell SIG <haskell-devel@lists.fedoraproject.org> - 0.8.0.8-0
- initial packaging for Fedora automatically generated by cabal2spec-0.22.2
