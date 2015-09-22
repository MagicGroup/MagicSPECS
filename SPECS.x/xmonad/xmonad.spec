# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name xmonad

Name:           %{pkg_name}
Version:        0.11.1
Release:        2%{?dist}
Summary:        A tiling window manager

License:        BSD
Url:            https://hackage.haskell.org/package/%{name}
Source0:        https://hackage.haskell.org/package/%{name}-%{version}/%{name}-%{version}.tar.gz
Source1:        xmonad-session.desktop
Source2:        xmonad-start
Source3:        xmonad.desktop
Source4:        README.fedora
Source5:        xmonad-mate-session.desktop
Source7:        xmonad.hs

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
# Begin cabal-rpm deps:
BuildRequires:  ghc-X11-devel
BuildRequires:  ghc-containers-devel
BuildRequires:  ghc-directory-devel
BuildRequires:  ghc-extensible-exceptions-devel
BuildRequires:  ghc-filepath-devel
BuildRequires:  ghc-mtl-devel
BuildRequires:  ghc-process-devel
BuildRequires:  ghc-unix-devel
BuildRequires:  ghc-utf8-string-devel
# End cabal-rpm deps
BuildRequires:  desktop-file-utils
Requires:       xmonad-basic = %{version}-%{release}
Requires:       xmonad-config = %{version}-%{release}

%description
xmonad is a tiling window manager for X. Windows are arranged
automatically to tile the screen without gaps or overlap, maximising
screen use. All features of the window manager are accessible from
the keyboard: a mouse is strictly optional. xmonad is written and
extensible in Haskell. Custom layout algorithms, and other
extensions, may be written by the user in config files. Layouts are
applied dynamically, and different layouts may be used on each
workspace. Xinerama is fully supported, allowing windows to be tiled
on several screens.

This is a meta-package that installs xmonad-basic and ghc-xmonad-contrib-devel,
allowing xmonad to be customized with "~/.xmonad/xmonad.hs".

To use xmonad with GNOME/MATE, please install xmonad-mate.


%package -n ghc-%{name}
Summary:        Haskell %{name} library

%description -n ghc-%{name}
This package provides the Haskell %{name} shared library.


%package -n ghc-%{name}-devel
Summary:        Haskell %{name} library development files
Requires:       ghc-compiler = %{ghc_version}
Requires(post): ghc-compiler = %{ghc_version}
Requires(postun): ghc-compiler = %{ghc_version}
Requires:       ghc-%{name} = %{version}-%{release}

%description -n ghc-%{name}-devel
This package provides the Haskell %{name} library development files.


%package basic
Summary:        A tiling window manager
Requires:       xmonad-core = %{version}-%{release}
# required until there is a command to open a system-default xterminal
Requires:       xterm
Requires:       dmenu
Obsoletes:      xmonad-core < 0.10-5
Requires:       zenity

%description basic
xmonad is a tiling window manager for X. Windows are arranged
automatically to tile the screen without gaps or overlap, maximising
screen use. All features of the window manager are accessible from
the keyboard: a mouse is strictly optional. xmonad is written and
extensible in Haskell. Custom layout algorithms, and other
extensions, may be written by the user in config files. Layouts are
applied dynamically, and different layouts may be used on each
workspace. Xinerama is fully supported, allowing windows to be tiled
on several screens.

This meta-package allows running the default basic upstream xmonad
configuration with xterm and dmenu.

If you want to customize xmonad, please install xmonad or xmonad-mate.


%package config
Summary:        xmonad config
Requires:       xmonad-core = %{version}-%{release}
Requires:       ghc-xmonad-devel = %{version}-%{release}
Requires:       ghc-xmonad-contrib-devel

%description config
This package provides a basic desktop configuration for xmonad.


%package core
Summary:        A tiling window manager
# for xmessage
Requires:       xorg-x11-apps

%description core
This package just provides the core xmonad window manager program.

To run the default xmonad configuration you should install xmonad-basic.
If you want to customize xmonad please install either xmonad or xmonad-mate.


%package mate
Summary:        xmonad MATE session
Requires:       xmonad-config = %{version}-%{release}
Requires:       mate-session-manager, mate-terminal
Requires:       mate-panel, mate-settings-daemon
Obsoletes:      xmonad-gnome < 0.11-3

%description mate
xmonad is a tiling window manager for X. Windows are arranged
automatically to tile the screen without gaps or overlap, maximising
screen use. All features of the window manager are accessible from
the keyboard: a mouse is strictly optional. xmonad is written and
extensible in Haskell. Custom layout algorithms, and other
extensions, may be written by the user in config files. Layouts are
applied dynamically, and different layouts may be used on each
workspace. Xinerama is fully supported, allowing windows to be tiled
on several screens.

This package adds a "xmonad-mate" X session configuration
so that xmonad can be started easily from GDM to run
in a MATE session.


%prep
%setup -q
cp -p %SOURCE4 .


%build
%ghc_lib_build


%install
%ghc_lib_install

install -p -m 0644 -D man/%{name}.1 %{buildroot}%{_mandir}/man1/%{name}.1
install -p -m 0644 -D %SOURCE1 %{buildroot}%{_datadir}/xsessions/%{name}.desktop
install -p -m 0755 -D %SOURCE2 %{buildroot}%{_bindir}/%{name}-start
desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{SOURCE3}
install -p -m 0644 -D %SOURCE5 %{buildroot}%{_datadir}/xsessions/%{name}-mate.desktop
install -p -m 0644 -D %SOURCE7 %{buildroot}%{_datadir}/xmonad/xmonad.hs

rm %{buildroot}%{_datadir}/%{name}-%{version}/man/xmonad.{hs,1,1.html}
# ship LICENSE in xmonad-core
rm %{buildroot}%{_docdir}/%{name}*/LICENSE


%post -n ghc-%{name}-devel
%ghc_pkg_recache


%postun -n ghc-%{name}-devel
%ghc_pkg_recache


%files


%files basic
%{_datadir}/xsessions/%{name}.desktop


%files config
%{_datadir}/xmonad/xmonad.hs


%files core
%license LICENSE
%doc CONFIG README README.fedora
%doc man/xmonad.{hs,1{.html,.markdown}}
%attr(755,root,root) %{_bindir}/%{name}
%attr(755,root,root) %{_bindir}/%{name}-start
%{_mandir}/man1/%{name}.1*
%{_datadir}/applications/%{name}.desktop


%files mate
%{_datadir}/xsessions/%{name}-mate.desktop


%files -n ghc-%{name} -f ghc-%{name}.files
%license LICENSE


%files -n ghc-%{name}-devel -f ghc-%{name}-devel.files
%doc STYLE


%changelog
* Wed Aug  5 2015 Jens Petersen <petersen@redhat.com> - 0.11.1-2
- use _JAVA_AWT_WM_NONREPARENTING=1 to handle Java apps correctly
  (#1061568, thanks to Erik Streb del Toro)

* Sun Jul 19 2015 Ben Boeckel <mathstuf@gmail.com> - 0.11.1-1
- Update to 0.11.1

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 22 2014 Jens Petersen <petersen@redhat.com> - 0.11-11
- no _pkgdocdir in EL7

* Sun Dec 22 2013 Jens Petersen <petersen@redhat.com> - 0.11-10
- add message about installing xmonad.hs to xmonad-start dialog

* Fri Sep 13 2013 Jens Petersen <petersen@redhat.com> - 0.11-9
- drop the mate-file-manager-schemas requires since mate-panel has it now
  (#1007219)

* Thu Sep 12 2013 Jens Petersen <petersen@redhat.com> - 0.11-8
- update README.fedora

* Thu Sep 12 2013 Jens Petersen <petersen@redhat.com> - 0.11-7
- mate-panel requires mate-file-manager-schemas to run (see #1007219)
- popup a zenity dialog for first-time users rather than manpage in terminal

* Mon Aug 19 2013 Jens Petersen <petersen@redhat.com> - 0.11-6
- use new _pkgdocdir to handled unversioned docdir

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 07 2013 Jens Petersen <petersen@redhat.com> - 0.11-5
- update to new simplified Haskell Packaging Guidelines

* Fri Mar 22 2013 Jens Petersen <petersen@redhat.com> - 0.11-4
- rebuild

* Mon Feb 25 2013 Jens Petersen <petersen@redhat.com> - 0.11-3
- xmonad-gnome subpackage renamed to xmonad-mate
  since gnome-panel in f19 is gone
- corresponding renamings from gnome to mate
- forward-port xmonad-start arg from f16

* Wed Jan 30 2013 Jens Petersen <petersen@redhat.com> - 0.11-2
- try to start gnome-screensaver for gnome sessions (#902850)

* Fri Jan 18 2013 Jens Petersen <petersen@redhat.com> - 0.11-1
- update to 0.11
- X11-1.6 and WM_TAKE_FOCUS patches no longer needed

* Thu Dec 13 2012 Jens Petersen <petersen@redhat.com> - 0.10-17
- xmonad-gnome now requires gnome-panel and gnome-settings-daemon to start

* Tue Nov 20 2012 Jens Petersen <petersen@redhat.com> - 0.10-16
- rebuild

* Fri Nov 16 2012 Jens Petersen <petersen@redhat.com> - 0.10-15
- add upstream patches for ICCCM WM_TAKE_FOCUS protocol and
  tracking currently processing event to fix focus for Java apps:
  see http://code.google.com/p/xmonad/issues/detail?id=177 (#874855)
- update to cabal-rpm packaging

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Jens Petersen <petersen@redhat.com> - 0.10-13
- change prof BRs to devel

* Mon Jun 11 2012 Jens Petersen <petersen@redhat.com> - 0.10-12
- allow building with X11-1.6

* Thu May 31 2012 Jens Petersen <petersen@redhat.com> - 0.10-11
- really fix xmonad-start to use hardware-platform correctly

* Tue May 29 2012 Jens Petersen <petersen@redhat.com> - 0.10-10
- fix user binary ldd check on i686/i386 using "uname -i" not "arch",
  and then recompile directly instead of just touching xmonad.hs first

* Fri May 25 2012 Jens Petersen <petersen@redhat.com> - 0.10-9
- basic subpackage should only obsolete core from before the split

* Thu May 24 2012 Jens Petersen <petersen@redhat.com> - 0.10-8
- move xmonad.desktop from core to basic subpackage

* Thu May 24 2012 Jens Petersen <petersen@redhat.com> - 0.10-7
- xmonad-start: if user binary has missing shared lib dependencies
  touch xmonad.hs so it gets recompiled (#806624 reported by Erik Streb)

* Fri Mar 23 2012 Jens Petersen <petersen@redhat.com> - 0.10-6
- try delaying manpage terminal startup 5s to avoid window resize
- add license to ghc_files

* Mon Feb 20 2012 Jens Petersen <petersen@redhat.com> - 0.10-5
- use gnome-terminal to display initial manpage from xmonad-gnome
- change the xmonad-gnome session name to xmonad-gnome

* Tue Feb  7 2012 Jens Petersen <petersen@redhat.com> - 0.10-4
- new "basic" meta-subpackage for pulling in xterm and dmenu for the default
  basic upstream config, also used by the base package

* Tue Feb  7 2012 Jens Petersen <petersen@redhat.com> - 0.10-3
- xmonad-gnome sessions now use gnomeConfig in xmonad.hs
- add note about gnome-panel menu activation in README.fedora

* Fri Jan  6 2012 Jens Petersen <petersen@redhat.com> - 0.10-2
- update to cabal2spec-0.25.2

* Fri Dec  2 2011 Jens Petersen <petersen@redhat.com> - 0.10-1
- update to 0.10 and cabal2spec-0.24.1
- depends on utf8-string
- re-enable haddock
- replace gnomeConfig in xmonad-start with xmonad.hs in new config subpackage
- drop the dynamic linking patch: dyn libs need to be default first (#744274)
- require dmenu

* Wed Oct 26 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.9.2-11.2
- rebuild with new gmp without compat lib

* Wed Oct 12 2011 Peter Schiffer <pschiffe@redhat.com> - 0.9.2-11.1
- rebuild with new gmp

* Thu Jul 28 2011 Jens Petersen <petersen@redhat.com> - 0.9.2-11
- remove _isa again since it doesn't fix the libX11-devel multilib problem

* Thu Jul 28 2011 Jens Petersen <petersen@redhat.com> - 0.9.2-10
- add _isa to the ghc-xmonad-contrib-devel requires to avoid missing libX11.so
  when custom linking (reported by Evan Dale Aromin, #723558)

* Thu Jun 16 2011 Jens Petersen <petersen@redhat.com> - 0.9.2-9
- ignore user configured packages when recompiling user xmonad.hs
  to avoid linking errors (#713035)
- don't display README.fedora initially on startup anymore
- drop the ghc-xmonad requires from xmonad-core
- update to cabal2spec-0.23.2

* Fri May 13 2011 Jens Petersen <petersen@redhat.com> - 0.9.2-8
- add a core subpackage and let the base package can pull in ghc-xmonad*-devel
- add a gnome subpackage for the gnome session
- more README.fedora improvements
- xmonad-start: quote the xterm commands and support ~/.xmonad/session
- fix doc files conflicts by having xmonad-core require ghc-xmonad

* Wed May 11 2011 Jens Petersen <petersen@redhat.com> - 0.9.2-7
- xmonad-start no longer execs xmonad not to confuse gnome-session
- xmonad-start now tries to setup a new xmonad.hs for GNOME desktop
  if running a xmonad-gnome session with xmonad-contrib installed
- improvements to README.fedora

* Fri Apr 22 2011 Jens Petersen <petersen@redhat.com> - 0.9.2-6
- drop explicit requires on ghc-xmonad-devel for lighter installs
- update readme to mention gsettings for gnome3
- enable ppc64 build
- buildrequires desktop-file-utils
- add an xsession file for a gnome-session too
- add a gnome-session-3 .session file

* Fri Apr  1 2011 Jens Petersen <petersen@redhat.com> - 0.9.2-5
- use desktop-file-install to install xmonad.desktop correctly
- update the desktop files for desktop-file-validate

* Fri Mar 11 2011 Jens Petersen <petersen@redhat.com> - 0.9.2-4
- disable haddock for now to build

* Thu Mar 10 2011 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.9.2-3
- Enable build on sparcv9

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 15 2011 Ben Boeckel <mathstuf@gmail.com> - 0.9.2-1
- Update to 0.9.2

* Sat Jan 15 2011 Ben Boeckel <mathstuf@gmail.com> - 0.9.1-12
- Update to cabal2spec-0.22.4
- Rebuild
- Use %%{buildroot}

* Sun Dec  5 2010 Jens Petersen <petersen@redhat.com> - 0.9.1-11
- rebuild

* Fri Nov 26 2010 Jens Petersen <petersen@redhat.com> - 0.9.1-10
- backport exceptions changes from upstream darcs for ghc7 base4
- update url and drop -o obsoletes

* Sun Nov 07 2010 Ben Boeckel <mathstuf@gmail.com> - 0.9.1-9
- Rebuild

* Wed Sep 29 2010 jkeating - 0.9.1-8
- Rebuilt for gcc bug 634757

* Thu Sep 23 2010 Jens Petersen <petersen@redhat.com> - 0.9.1-7
- xmonad-start should run xterm in background
- improve README.fedora more

* Sun Sep 12 2010 Jens Petersen <petersen@redhat.com> - 0.9.1-6
- add application desktop file for gnome-session to find xmonad
  so setting /desktop/gnome/session/required_components/windowmanager now works
- add xmonad-dynamic-link.patch to dynamically link customized xmonad
- move display of manpage for new users from xmonad.hs to xmonad-start
  and only display it when no ~/.xmonad/
- drop skel file and dont create ~/.xmonad by default

* Sat Sep  4 2010 Jens Petersen <petersen@redhat.com> - 0.9.1-5
- update to ghc-rpm-macros-0.8.1, hscolour and drop doc pkg (cabal2spec-0.22.2)

* Fri Jun 25 2010 Jens Petersen <petersen@redhat.com> - 0.9.1-4
- strip dynamic files (cabal2spec-0.21.4)

* Tue Apr 27 2010 Jens Petersen <petersen@redhat.com> - 0.9.1-3
- rebuild against ghc-6.12.2

* Wed Jan 13 2010 Jens Petersen <petersen@redhat.com> - 0.9.1-2
- rebuild against ghc-mtl package

* Mon Jan 11 2010 Jens Petersen <petersen@redhat.com> - 0.9.1-1
- update to 0.9.1
- update to ghc-rpm-macros-0.5.1 and cabal2spec-0.21.1:
- drop doc and prof bcond
- use common_summary and common_description
- use ghc_name, ghc_binlib_package and ghc_pkg_deps
- build shared library
- drop X11_minver for now: it breaks macros
- drop redundant buildroot and its install cleaning

* Tue Dec  8 2009 Jens Petersen <petersen@redhat.com> - 0.9-4
- drop the ppc build cabal workaround

* Tue Nov 17 2009 Jens Petersen <petersen@redhat.com> - 0.9-3
- use %%ghc_pkg_ver for requires

* Sun Nov 15 2009 Jens Petersen <petersen@redhat.com> - 0.9-2
- also buildrequires and requires ghc-X11-doc

* Sun Nov 15 2009 Jens Petersen <petersen@redhat.com> - 0.9-1
- update to 0.9 (requires ghc-X11 >= 1.4.6.1)
- drop superfluous X11_version from ghc-X11 requires
- rename X11_version to X11_minver
- remove extra xmonad.hs under datadir

* Thu Jul 30 2009 Yaakov M. Nemoy <ynemoy@fedoraproject.org> - 0.8.1-15
- rebuild against newer packages from the mass rebuild

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 16 2009 Jens Petersen <petersen@redhat.com> - 0.8.1-13
- buildrequires ghc-rpm-macros (cabal2spec-0.16)
- rebuild for ghc-6.10.3

* Wed May  6 2009 Yaakov M. Nemoy <ynemoy@fedoraproject.org> - 0.8.1-12
- applies changes from jens' patch
- renames xmonad.desktop entry
- adds .orig of the xmonad default config
- modifies manpage patch to use 'better' filenames
- renames manpage patch

* Mon Apr 27 2009 Yaakov M. Nemoy <yankee@localhost.localdomain> - 0.8.1-11
- adds runghc hack taken from haddock

* Mon Apr 27 2009 Yaakov M. Nemoy <ynemoy@fedoraproject.org> - 0.8.1-10
- converts the sample config into a patch on the upstream source
- renumbers down the source lines

* Mon Apr 20 2009 Jens Petersen <petersen@redhat.com> - 0.8.1-9
- update to latest macros.ghc without ghc_version (cabal2spec-0.15)
- require xorg-x11-apps for xmessage

* Mon Apr  6 2009 Jens Petersen <petersen@redhat.com>
- merge xmonad-session into xmonad-start
- fix with_prof configure test

* Thu Apr 02 2009 Till Maas <opensource@till.name> - 0.8.1-8
- remove tabs in spec
- rename start-xmonad to xmonad-start for consistency with xmonad-session
- add directory creation and exec of xmonad to start-xmonad
- install xmonad.hs that only displays manpage in /etc/skel/.xmonad/xmonad.hs
- add xterm dependency

* Tue Mar 31 2009 Yaakov M. Nemoy <yankee@localhost.localdomain> - 0.8.1-7
- added session and start scripts

* Mon Mar 30 2009 Till Maas <opensource@till.name> - 0.8.1-6
- add desktop file
- install man page
- include sample config file (xmonad.hs)
- include other documentation files

* Tue Mar 17 2009 Yaakov M. Nemoy <ynemoy@fedoraproject.org> - 0.8.1-5
- refixes permissions after doing it wrong the first time

* Fri Mar 13 2009 Yaakov M. Nemoy <ynemoy@fedoraproject.org> - 0.8.1-4
- fixed license to BSD
- fixed version of X11 to be a tad more flexible
- fixes permissions of /usr/bin/xmonad

* Mon Mar  2 2009 Yaakov M. Nemoy <ynemoy@fedoraproject.org> - 0.8.1-3
- updated to newest cabal2spec 0.12
- this includes the shiny new devel package

* Tue Feb 24 2009 Yaakov M. Nemoy <ynemoy@fedoraproject.org> - 0.8.1-2
- updated spec to meet new guidelines ala cabal2spec 0.7

* Wed Jan 21 2009 ynemoy <ynemoy@fedoraproject.org> - 0.8.1-1
- initial packaging for Fedora created by cabal2spec
