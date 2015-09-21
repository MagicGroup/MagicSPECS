# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name xmonad-contrib

Name:           ghc-%{pkg_name}
Version:        0.11.4
Release:        2%{?dist}
Summary:        Third party extensions for xmonad

License:        BSD
Url:            https://hackage.haskell.org/package/%{pkg_name}
Source0:        https://hackage.haskell.org/package/%{pkg_name}-%{version}/%{pkg_name}-%{version}.tar.gz
Patch0:         xmonad-contrib-use_xft-flag.patch
Patch1:         xmonad-contrib-0.10-xft-fonts.patch
Patch2:         xmonad-contrib-0.10-ewmh-set-NET_WM_STATE.patch
Patch4:         xmonad-contrib-0.10-PositionStore-dont-rescale-with-screen.patch
Patch5:         xmonad-contrib-0.11.2-xfce4-terminal.patch
Patch6:         xmonad-contrib-0.11.4-applicative-imports.patch

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
# Begin cabal-rpm deps:
BuildRequires:  ghc-X11-devel
BuildRequires:  ghc-X11-xft-devel
BuildRequires:  ghc-containers-devel
BuildRequires:  ghc-directory-devel
BuildRequires:  ghc-extensible-exceptions-devel
BuildRequires:  ghc-mtl-devel
BuildRequires:  ghc-old-locale-devel
BuildRequires:  ghc-old-time-devel
BuildRequires:  ghc-process-devel
BuildRequires:  ghc-random-devel
BuildRequires:  ghc-unix-devel
BuildRequires:  ghc-utf8-string-devel
BuildRequires:  ghc-xmonad-devel
# End cabal-rpm deps

%description
Third party tiling algorithms, configurations and scripts to xmonad,
a tiling window manager for X.

For an introduction to building, configuring and using xmonad
extensions, see "XMonad.Doc". In particular:

"XMonad.Doc.Configuring", a guide to configuring xmonad
"XMonad.Doc.Extending", using the contributed extensions library
"XMonad.Doc.Developing", introduction to xmonad internals and writing
your own extensions.


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
%patch0 -p1 -b .orig-xft
%patch1 -p1 -b .orig-misc-fixed
%patch2 -p1 -b .orig-NET_WM_STATE
%patch4 -p1 -b .orig-rescale
%patch5 -p1 -b .orig-Terminal
%patch6 -p1 -b .applicative-imports


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
%doc README


%changelog
* Sun Sep 20 2015 Liu Di <liudidi@gmail.com> - 0.11.4-2
- 为 Magic 3.0 重建

* Sun Jul 19 2015 Ben Boeckel <mathstuf@gmail.com> - 0.11.4-1
- Update to 0.11.4

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Aug 29 2014 Jens Petersen <petersen@redhat.com> - 0.11.3-1
- update to 0.11.3
- refresh to cblrpm-0.8.11

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Nov 26 2013 Jens Petersen <petersen@redhat.com> - 0.11.2-3
- XFCE Terminal is now called xfce4-terminal (#1034353)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 21 2013 Jens Petersen <petersen@redhat.com> - 0.11.2-1
- update to 0.11.2

* Fri Jun 07 2013 Jens Petersen <petersen@redhat.com> - 0.11.1-2
- update to new simplified Haskell Packaging Guidelines

* Thu Mar 21 2013 Jens Petersen <petersen@redhat.com> - 0.11.1-1
- update to 0.11.1

* Tue Mar 19 2013 Jens Petersen <petersen@redhat.com> - 0.11-3
- fix build with X11-1.6.1

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 18 2013 Jens Petersen <petersen@redhat.com> - 0.11-1
- update to 0.11
- BorderResize, X11-1.6, and takeFocus patches no longer needed

* Tue Nov 20 2012 Jens Petersen <petersen@redhat.com> - 0.10-8
- rebuild

* Sat Nov 17 2012 Jens Petersen <petersen@redhat.com> - 0.10-7
- add ICCCMFocus patch from upstream for WM_TAKE_FOCUS move to core (#874855)
- use a patch for use_xft flag
- condition X11-1.6 patch to fedora >= 18
- update packaging with cabal-rpm

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun May 13 2012 Jens Petersen <petersen@redhat.com> - 0.10-5
- patch XMonad.Util.PositionStore to not scale the size of windows
  when changing screen unless the window is now larger than the monitor
- allow building with X11-1.6

* Fri Mar 23 2012 Jens Petersen <petersen@redhat.com> - 0.10-4
- add license to ghc_files

* Tue Mar 13 2012 Jens Petersen <petersen@redhat.com> - 0.10-3
- use xft fonts by default
- make ewmh set _NET_WM_STATE property on windows so that gtk3 apps do
  not render unfocused
- place BorderResize rectangles within window decor with narrower width

* Fri Jan  6 2012 Jens Petersen <petersen@redhat.com> - 0.10-2
- update to cabal2spec-0.25.2

* Sat Dec  3 2011 Jens Petersen <petersen@redhat.com> - 0.10-1
- update to 0.10

* Mon Oct 24 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.9.2-6.3
- rebuild with new gmp without compat lib

* Fri Oct 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.9.2-6.2
- rebuild with new gmp without compat lib

* Tue Oct 11 2011 Peter Schiffer <pschiffe@redhat.com> - 0.9.2-6.1
- rebuild with new gmp

* Mon Aug 29 2011 Jens Petersen <petersen@redhat.com> - 0.9.2-6
- make sure we build with X11-xft

* Sat Jul 09 2011 Ben Boeckel <mathstuf@gmail.com> - 0.9.2-5
- Update to cabal2spec-0.24

* Wed Jun 22 2011 Jens Petersen <petersen@redhat.com> - 0.9.2-4
- BR ghc-Cabal-devel instead of ghc-prof and use ghc_arches (cabal2spec-0.23.2)

* Thu Mar 10 2011 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.9.2-3
- Enable build on sparcv9

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 15 2011 Ben Boeckel <mathstuf@gmail.com> - 0.9.2-1
- Update to 0.9.2

* Sat Jan 15 2011 Ben Boeckel <mathstuf@gmail.com> - 0.9.1-11
- Update to cabal2spec-0.22.4
- Rebuild

* Sun Dec  5 2010 Jens Petersen <petersen@redhat.com> - 0.9.1-10
- rebuild for syb-0.3

* Sat Nov 27 2010 Jens Petersen <petersen@redhat.com> - 0.9.1-9
- backport base4 changes from upstream darcs for ghc7
- update url and drop -o obsoletes

* Wed Sep 29 2010 jkeating - 0.9.1-8
- Rebuilt for gcc bug 634757

* Tue Sep 14 2010 Jens Petersen <petersen@redhat.com> - 0.9.1-7
- rebuild against patched xmonad

* Sat Sep  4 2010 Jens Petersen <petersen@redhat.com> - 0.9.1-6
- add hscolour and doc obsolete (cabal2spec-0.22.2)

* Sat Jun 26 2010 Jens Petersen <petersen@redhat.com> - 0.9.1-5
- sync cabal2spec-0.22

* Thu Apr 29 2010 Jens Petersen <petersen@redhat.com> - 0.9.1-4
- rebuild against ghc-6.12.2
- condition ghc_lib_package
- depend on utf8-string again

* Fri Jan 15 2010 Jens Petersen <petersen@redhat.com> - 0.9.1-3
- utf8-string is part of ghc so drop ghc-utf8-string-devel dependency

* Wed Jan 13 2010 Jens Petersen <petersen@redhat.com> - 0.9.1-2
- rebuild against ghc-mtl package

* Mon Jan 11 2010 Jens Petersen <petersen@redhat.com> - 0.9.1-1
- update to 0.9.1
- update to ghc-rpm-macros-0.5.1 and cabal2spec-0.21.1:
- drop doc and prof bcond
- use common_summary and common_description
- use ghc_lib_package and ghc_pkg_deps
- build shared library
- drop redundant buildroot and its install cleaning

* Tue Nov 17 2009 Jens Petersen <petersen@redhat.com> - 0.9-1
- update to 0.9
- use %%ghc_pkg_ver for dep requires versions

* Fri Aug 28 2009 Yaakov M. Nemoy <ynemoy@fedoraproject.org> - 0.8.1-8
- added a few more docs

* Thu Aug 27 2009 Yaakov M. Nemoy <ynemoy@fedoraproject.org> - 0.8.1-7
- removed bcond since xft will be in fedora soon

* Wed Aug 26 2009 Jens Petersen <petersen@redhat.com> - 0.8.1-6
- drop ghc-X11 deps since already in xmonad
- drop X lib deps since already in ghc-X11
- add ghc-utf8-string deps
- add bcond for X11-xft
- drop base package requires

* Wed Jun 17 2009 Yaakov M. Nemoy <ynemoy@fedoraproject.org> - 0.8.1-5
- added -devel to some BRs

* Wed Jun 17 2009 Yaakov M. Nemoy <ynemoy@fedoraproject.org> - 0.8.1-4
- updated to latest cabal2spec 0.16

* Mon Mar  2 2009 Yaakov M. Nemoy <ynemoy@fedoraproject.org> - 0.8.1-3
- updated to new guidelines ala cabal2spec 0.12

* Tue Feb 24 2009 Yaakov M. Nemoy <ynemoy@fedoraproject.org> - 0.8.1-2
- updated package to new guidelines ala cabal2spec 0.7

* Wed Jan 21 2009 ynemoy <ynemoy@fedoraproject.org> - 0.8.1-1
- initial packaging for Fedora created by cabal2spec
