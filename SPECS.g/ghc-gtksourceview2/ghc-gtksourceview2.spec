# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name gtksourceview2

Name:           ghc-%{pkg_name}
Version:        0.13.1.3
Release:        2%{?dist}
Summary:        Binding to the GtkSourceView library

License:        LGPLv2+
Url:            https://hackage.haskell.org/package/%{pkg_name}
Source0:        https://hackage.haskell.org/package/%{pkg_name}-%{version}/%{pkg_name}-%{version}.tar.gz

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
# Begin cabal-rpm deps:
BuildRequires:  ghc-array-devel
BuildRequires:  ghc-containers-devel
BuildRequires:  ghc-glib-devel
BuildRequires:  ghc-gtk-devel
BuildRequires:  ghc-mtl-devel
BuildRequires:  ghc-text-devel
BuildRequires:  gtk2hs-buildtools
BuildRequires:  pkgconfig(gtksourceview-2.0)
# End cabal-rpm deps

%description
GtkSourceView is a text widget that extends the standard GTK+ 2.x text widget
GtkTextView. It improves GtkTextView by implementing syntax highlighting and
other features typical of a source editor.


%package devel
Summary:        Haskell %{pkg_name} library development files
Provides:       %{name}-static = %{version}-%{release}
Requires:       ghc-compiler = %{ghc_version}
Requires(post): ghc-compiler = %{ghc_version}
Requires(postun): ghc-compiler = %{ghc_version}
Requires:       %{name}%{?_isa} = %{version}-%{release}
# Begin cabal-rpm deps:
Requires:       pkgconfig(gtksourceview-2.0)
# End cabal-rpm deps

%description devel
This package provides the Haskell %{pkg_name} library development files.


%prep
%setup -q -n %{pkg_name}-%{version}


%build
%ghc_lib_build


%install
%ghc_lib_install

rm %{buildroot}%{ghc_pkgdocdir}/COPYING

# move demos
rm -r %{buildroot}%{_datadir}/%{pkg_name}-%{version}


%post devel
%ghc_pkg_recache


%postun devel
%ghc_pkg_recache


%files -f %{name}.files
%license COPYING


%files devel -f %{name}-devel.files
%doc demo

%changelog
* Sun Sep 20 2015 Liu Di <liudidi@gmail.com> - 0.13.1.3-2
- 为 Magic 3.0 重建

* Wed Jul 22 2015 Jens Petersen <petersen@redhat.com> - 0.13.1.3-1
- update to 0.13.1.3

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jan 19 2015 Jens Petersen <petersen@redhat.com> - 0.13.1.2-1
- update to 0.13.1.2

* Tue Oct 28 2014 Jens Petersen <petersen@redhat.com> - 0.13.1.1-1
- update to 0.13.1.1
- refresh to cblrpm-0.8.11

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Dec 21 2013 Jens Petersen <petersen@redhat.com> - 0.12.5.0-1
- update to 0.12.5.0

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.3.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 07 2013 Jens Petersen <petersen@redhat.com> - 0.12.3.1-7
- update to new simplified Haskell Packaging Guidelines

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.3.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Nov 17 2012 Jens Petersen <petersen@redhat.com> - 0.12.3.1-5
- update with cabal-rpm

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Jens Petersen <petersen@redhat.com> - 0.12.3.1-3
- change prof BRs to devel

* Thu Jun 21 2012 Jens Petersen <petersen@redhat.com> - 0.12.3.1-2
- rebuild

* Wed Jun 13 2012 Jens Petersen <petersen@redhat.com> - 0.12.3.1-1
- update to 0.12.3.1

* Thu Mar 22 2012 Jens Petersen <petersen@redhat.com> - 0.12.3-3
- add license to ghc_files

* Fri Jan  6 2012 Jens Petersen <petersen@redhat.com> - 0.12.3-2
- update to cabal2spec-0.25.2

* Fri Oct 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.12.3-1.2
- rebuild with new gmp without compat lib

* Tue Oct 11 2011 Peter Schiffer <pschiffe@redhat.com> - 0.12.3-1.1
- rebuild with new gmp

* Tue Sep 20 2011 Jens Petersen <petersen@redhat.com> - 0.12.3-1
- update to 0.12.3
- add _isa suffix to gtk2-devel depends (see #723558)

* Tue Jun 21 2011 Jens Petersen <petersen@redhat.com> - 0.12.2-5
- BR ghc-Cabal-devel instead of ghc-prof (cabal2spec-0.23.2)

* Thu Mar 10 2011 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.12.2-4
- Enable build on sparcv9

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 18 2011 Jens Petersen <petersen@redhat.com> - 0.12.2-2
- update to cabal2spec-0.22.4

* Tue Nov 30 2010 Jens Petersen <petersen@redhat.com> - 0.12.2-1
- update to 0.12.2

* Fri Nov 26 2010 Jens Petersen <petersen@redhat.com> - 0.12.1-2
- fix Cabal-1.10 build with ghc7-Gtk2HsSetup-Cabal-1.10.patch
- drop devhelp

* Thu Oct  7 2010 Jens Petersen <petersen@redhat.com> - 0.12.1-1
- update to 0.12.1
- put demo files in docdir

* Wed Sep  1 2010 Jens Petersen <petersen@redhat.com> - 0.11.1-1
- update to 0.11.1

* Sun Jul 18 2010 Jens Petersen <petersen@redhat.com> - 0.11.0-1
- BR ghc-glib, ghc-gtk, ghc-mtl
- ghc-rpm-macros-0.8.1
- support hscolour and devhelp

* Sun Jul 18 2010 Fedora Haskell SIG <haskell-devel@lists.fedoraproject.org> - 0.11.0-0
- initial packaging for Fedora automatically generated by cabal2spec-0.22.1
