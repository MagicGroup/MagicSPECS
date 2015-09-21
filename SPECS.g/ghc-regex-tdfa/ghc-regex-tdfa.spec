# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name regex-tdfa

# no useful debuginfo for Haskell packages without C sources
%global debug_package %{nil}

Name:           ghc-%{pkg_name}
Version:        1.2.0
Release:        3%{?dist}
Summary:        Haskell tagged DFA regular expression library

License:        BSD
URL:            http://hackage.haskell.org/package/%{pkg_name}
Source0:        http://hackage.haskell.org/package/%{pkg_name}-%{version}/%{pkg_name}-%{version}.tar.gz

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
# Begin cabal-rpm deps:
BuildRequires:  ghc-array-devel
BuildRequires:  ghc-bytestring-devel
BuildRequires:  ghc-containers-devel
BuildRequires:  ghc-mtl-devel
BuildRequires:  ghc-parsec-devel
BuildRequires:  ghc-regex-base-devel
# End cabal-rpm deps

%description
A new all Haskell "tagged" DFA regex engine, inspired by libtre.


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
%doc LICENSE


%files devel -f %{name}-devel.files


%changelog
* Sun Sep 20 2015 Liu Di <liudidi@gmail.com> - 1.2.0-3
- 为 Magic 3.0 重建

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Aug 27 2014 Jens Petersen <petersen@redhat.com> - 1.2.0-1
- update to 1.2.0
- refresh to cblrpm-0.8.11

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.8-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.8-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.8-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jun 05 2013 Jens Petersen <petersen@redhat.com> - 1.1.8-10
- update to new simplified Haskell Packaging Guidelines

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.8-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Nov 17 2012 Jens Petersen <petersen@redhat.com> - 1.1.8-8
- update with cabal-rpm

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Jens Petersen <petersen@redhat.com> - 1.1.8-6
- change prof BRs to devel

* Fri Jun 15 2012 Jens Petersen <petersen@redhat.com> - 1.1.8-5
- rebuild

* Sun Mar 18 2012 Jens Petersen <petersen@redhat.com> - 1.1.8-4
- update to cabal2spec-0.25

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.8-3.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Oct 24 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.1.8-2.3
- rebuild with new gmp without compat lib

* Fri Oct 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.1.8-2.2
- rebuild with new gmp without compat lib

* Tue Oct 11 2011 Peter Schiffer <pschiffe@redhat.com> - 1.1.8-2.1
- rebuild with new gmp

* Tue Jun 21 2011 Lakshmi Narasimhan T V <lakshminaras2002@gmail.com> - 1.1.8-2
- Update to cabal2spec-0.23.2

* Mon Apr 18 2011 Lakshmi Narasimhan T V <lakshminaras2002@gmail.com> - 1.1.8-1
- Package update to 1.1.8. Update to cabal2spec 0.22.5

* Fri Mar 11 2011 Lakshmi Narasimhan T V <lakshminaras2002@gmail.com> - 1.1.7-6
Rebuild for ghc-7.0.2

* Thu Mar 10 2011 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.1.7-5
- Enable build on sparcv9

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 15 2011 Lakshmi Narasimhan T V <lakshminaras2002@gmail.com> - 1.1.7-3
- rebuild for ghc7
- update to cabal2spec 0.22.4

* Sun Dec  5 2010 Jens Petersen <petersen@redhat.com> - 1.1.7-2
- rebuild

* Sun Nov 28 2010 Lakshmi Narasimhan T V <lakshminaras2002@gmail.com> - 1.1.7-1
- updated to 1.1.7

* Sun Nov 28 2010 Lakshmi Narasimhan T V <lakshminaras2002@gmail.com> - 1.1.6-2
- Rebuilding for ghc7

* Sun Oct 31 2010 Lakshmi Narasimhan T V <lakshminaras2002@gmail.com> - 1.1.6-1
- package updated to 1.1.6

* Sat Sep 18 2010 Lakshmi Narasimhan T V <lakshminaras2002@gmail.com> - 1.1.4-1
- using ghc-rpm-macros 0.8.1
- package updated to 1.1.4

* Sat Jul  3 2010 Lakshmi Narasimhan T V <lakshminaras2002@gmail.com> - 1.1.3-1
- initial packaging for Fedora automatically generated by cabal2spec-0.22.1
- Updated to use ghc_lib_package, ghc_lib_build, ghc_lib_install macros instead of cabal macros

* Tue May 25 2010 Fedora Haskell SIG <haskell-devel@lists.fedoraproject.org> - 1.1.2-1
- initial packaging for Fedora automatically generated by cabal2spec-0.21.3
