# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name readline

Name:           ghc-%{pkg_name}
Version:        1.0.3.0
Release:        9%{?dist}
Summary:        An interface to the GNU readline library

License:        GPL+
Url:            https://hackage.haskell.org/package/%{pkg_name}
Source0:        https://hackage.haskell.org/package/%{pkg_name}-%{version}/%{pkg_name}-%{version}.tar.gz

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
# Begin cabal-rpm deps:
BuildRequires:  ghc-process-devel
# End cabal-rpm deps
BuildRequires:  readline-devel%{_isa}

%description
The GNU Readline library provides a set of functions for use by applications
that allow users to edit command lines as they are typed in. The Readline
library includes additional functions to maintain a list of previously-entered
command lines, to recall and perhaps reedit those lines, and perform csh-like
history expansion on previous commands.


%package devel
Summary:        Haskell %{pkg_name} library development files
Provides:       %{name}-static = %{version}-%{release}
Requires:       ghc-compiler = %{ghc_version}
Requires(post): ghc-compiler = %{ghc_version}
Requires(postun): ghc-compiler = %{ghc_version}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       readline-devel%{_isa}

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
%{_docdir}/%{name}-%{version}/LICENSE


%files devel -f %{name}-devel.files


%changelog
* Sun Nov 08 2015 Liu Di <liudidi@gmail.com> - 1.0.3.0-9
- 为 Magic 3.0 重建

* Sun Sep 20 2015 Liu Di <liudidi@gmail.com> - 1.0.3.0-8
- 为 Magic 3.0 重建

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Feb  3 2015 Jens Petersen <petersen@redhat.com> - 1.0.3.0-6
- cblrpm refresh

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 07 2013 Jens Petersen <petersen@redhat.com> - 1.0.3.0-2
- update to new simplified Haskell Packaging Guidelines

* Mon Mar 18 2013 Shakthi Kannan <shakthimaan [AT] fedoraproject dot org> - 1.0.3.0-1
- new upstream version 1.0.3.0

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov  9 2012 Jens Petersen <petersen@redhat.com> - 1.0.1.0-2
- fix missing readline-devel requires
- change license tag to GPL+ since no source version indications
- update with cabal-rpm

* Tue Jun 12 2012 Shakthi Kannan <shakthimaan [AT] fedoraproject dot org> - 1.0.1.0-1
- Added BuildRequires.
- Spec file template generated by cabal2spec-0.25.5
