# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name glade

Name:           ghc-%{pkg_name}
Version:        0.12.5.0
Release:        8%{?dist}
Summary:        Binding to the glade library

License:        LGPLv2+
Url:            https://hackage.haskell.org/package/%{pkg_name}
Source0:        https://hackage.haskell.org/package/%{pkg_name}-%{version}/%{pkg_name}-%{version}.tar.gz

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
# Begin cabal-rpm deps:
BuildRequires:  ghc-glib-devel
BuildRequires:  ghc-gtk-devel
BuildRequires:  gtk2hs-buildtools
BuildRequires:  pkgconfig(libglade-2.0)
# End cabal-rpm deps

%description
This library allows to load externally stored user interfaces into programs.
This allows alteration of the interface without recompilation of the program.

Note that this functionality is now provided in gtk directly (as of version
2.12 of the gtk+ C lib) by the Graphics.UI.Gtk.Builder module.


%package devel
Summary:        Haskell %{pkg_name} library development files
Provides:       %{name}-static = %{version}-%{release}
Requires:       ghc-compiler = %{ghc_version}
Requires(post): ghc-compiler = %{ghc_version}
Requires(postun): ghc-compiler = %{ghc_version}
Requires:       %{name}%{?_isa} = %{version}-%{release}
# Begin cabal-rpm deps:
Requires:       pkgconfig(libglade-2.0)
# End cabal-rpm deps

%description devel
This package provides the Haskell %{pkg_name} library development files.


%prep
%setup -q -n %{pkg_name}-%{version}
cabal-tweak-dep-ver glib ' && < 0.13' ''
cabal-tweak-dep-ver gtk ' && < 0.13' ''


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
* Sun Nov 08 2015 Liu Di <liudidi@gmail.com> - 0.12.5.0-8
- 为 Magic 3.0 重建

* Sun Sep 20 2015 Liu Di <liudidi@gmail.com> - 0.12.5.0-7
- 为 Magic 3.0 重建

* Wed Jul 22 2015 Jens Petersen <petersen@redhat.com> - 0.12.5.0-6
- refresh and use license macro

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Sep 17 2014 Jens Petersen <petersen@redhat.com> - 0.12.5.0-4
- allow glib and gtk 0.13
- refresh to cblrpm-0.8.11

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Dec 21 2013 Jens Petersen <petersen@redhat.com> - 0.12.5.0-1
- update to 0.12.5.0

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 07 2013 Jens Petersen <petersen@redhat.com> - 0.12.1-10
- update to new simplified Haskell Packaging Guidelines

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Nov 17 2012 Jens Petersen <petersen@redhat.com> - 0.12.1-8
- update with cabal-rpm

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Jens Petersen <petersen@redhat.com> - 0.12.1-6
- change prof BRs to devel

* Thu Jun 21 2012 Jens Petersen <petersen@redhat.com> - 0.12.1-5
- rebuild

* Fri Jun 15 2012 Jens Petersen <petersen@redhat.com> - 0.12.1-4
- rebuild

* Thu Mar 22 2012 Jens Petersen <petersen@redhat.com> - 0.12.1-3
- add license to ghc_files

* Fri Jan  6 2012 Jens Petersen <petersen@redhat.com> - 0.12.1-2
- update to cabal2spec-0.25.2

* Mon Oct 24 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.12.1-1.3
- rebuild with new gmp without compat lib

* Thu Oct 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.12.1-1.2
- rebuild with new gmp without compat lib

* Tue Oct 11 2011 Peter Schiffer <pschiffe@redhat.com> - 0.12.1-1.1
- rebuild with new gmp

* Tue Sep 20 2011 Jens Petersen <petersen@redhat.com> - 0.12.1-1
- update to 0.12.1
- add _isa suffix to gtk2-devel depends (see #723558)

* Tue Jun 21 2011 Jens Petersen <petersen@redhat.com> - 0.12.0-5
- BR ghc-Cabal-devel instead of ghc-prof (cabal2spec-0.23.2)

* Thu Mar 10 2011 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.12.0-4
- Enable build on sparcv9

* Fri Feb 11 2011 Jens Petersen <petersen@redhat.com> - 0.12.0-3
- rebuild for f15

* Tue Jan 18 2011 Jens Petersen <petersen@redhat.com> - 0.12.0-2
- update to cabal2spec-0.22.4

* Tue Nov 30 2010 Jens Petersen <petersen@redhat.com> - 0.11.1-3
- update to 0.12.0

* Fri Nov 26 2010 Jens Petersen <petersen@redhat.com> - 0.11.1-3
- fix Cabal-1.10 build with ghc7-Gtk2HsSetup-Cabal-1.10.patch

* Thu Oct  7 2010 Jens Petersen <petersen@redhat.com> - 0.11.1-2
- buildrequires gtk2hs-buildtools (#633194)
- correct the license tag

* Mon Sep 13 2010 Jens Petersen <petersen@redhat.com> - 0.11.1-1
- LGPLv2+
- BR ghc-gtk-devel and libglade2-devel
- move demo files to doc

* Mon Sep 13 2010 Fedora Haskell SIG <haskell-devel@lists.fedoraproject.org> - 0.11.1-0
- initial packaging for Fedora automatically generated by cabal2spec-0.22.2
