%define pkgname xinit

Summary:   X.Org X11 X Window System xinit startup scripts
Name:      xorg-x11-%{pkgname}
Version:   1.3.2
Release:   7%{?dist}
License:   MIT
Group:     User Interface/X
URL:       http://www.x.org

Source0:  http://ftp.nara.wide.ad.jp/pub/X11/x.org/individual/app/%{pkgname}-%{version}.tar.bz2
Source10: xinitrc-common
Source11: xinitrc
Source12: Xclients
Source13: Xmodmap
Source14: Xresources
# NOTE: Xsession is used by xdm/kdm/gdm and possibly others, so we keep it
#       here instead of the xdm package.
Source16: Xsession
Source17: localuser.sh
Source18: xinit-compat.desktop
Source19: xinit-compat

# Fedora specific patches

Patch1: xinit-1.0.2-client-session.patch
# Fix startx to run on the same tty as user to avoid new session. 
# https://bugzilla.redhat.com/show_bug.cgi?id=806491
Patch2: xorg-x11-xinit-1.3.2-systemd-logind.patch
Patch3: xinit-1.0.9-unset.patch

BuildRequires: pkgconfig
BuildRequires: libX11-devel
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: dbus-devel
BuildRequires: libtool
BuildRequires: xorg-x11-util-macros
# NOTE: startx needs xauth in order to run, but that is not picked up
#       automatically by rpm.  (Bug #173684)
Requires: xorg-x11-xauth
# next two are for localuser.sh
Requires: coreutils
Requires: xorg-x11-server-utils

%package session
Summary: Display manager support for ~/.xsession and ~/.Xclients
Group: User Interface/X

%description
X.Org X11 X Window System xinit startup scripts

%description session
Allows legacy ~/.xsession and ~/.Xclients files to be used from display managers

%prep
%setup -q -n %{pkgname}-%{version}
%patch1 -p1 -b .client-session
%patch2 -p1 -b .systemd-logind
%patch3 -p1 -b .unset

%build
autoreconf
%configure
# FIXME: Upstream should default to XINITDIR being this.  Make a patch to
# Makefile.am and submit it in a bug report or check into CVS.
make XINITDIR=%{_sysconfdir}/X11/xinit

%install
# FIXME: Upstream should default to XINITDIR being this.  Make a patch to
# Makefile.am and submit it in a bug report or check into CVS.
make install DESTDIR=$RPM_BUILD_ROOT XINITDIR=%{_sysconfdir}/X11/xinit
install -p -m644 -D %{SOURCE18} $RPM_BUILD_ROOT%{_datadir}/xsessions/xinit-compat.desktop

# Install Red Hat custom xinitrc, etc.
{
    mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit

    install -p -m 644 %{SOURCE10} $RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit/xinitrc-common

    for script in %{SOURCE11} %{SOURCE12} %{SOURCE16} ; do
        install -p -m 755 $script $RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit/${script##*/}
    done

    install -p -m 644 %{SOURCE13} $RPM_BUILD_ROOT%{_sysconfdir}/X11/Xmodmap
    install -p -m 644 %{SOURCE14} $RPM_BUILD_ROOT%{_sysconfdir}/X11/Xresources

    mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit/xinitrc.d
    install -p -m 755 %{SOURCE17} $RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit/xinitrc.d/localuser.sh

    mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit/Xclients.d

    mkdir -p $RPM_BUILD_ROOT%{_libexecdir}
    install -p -m 755 %{SOURCE19} $RPM_BUILD_ROOT%{_libexecdir}
}

%files
%defattr(-,root,root,-)
%doc COPYING README ChangeLog
%{_bindir}/startx
%{_bindir}/xinit
%dir %{_sysconfdir}/X11/xinit
%{_sysconfdir}/X11/xinit/xinitrc
%{_sysconfdir}/X11/xinit/xinitrc-common
%config(noreplace) %{_sysconfdir}/X11/Xmodmap
%config(noreplace) %{_sysconfdir}/X11/Xresources
%dir %{_sysconfdir}/X11/xinit/Xclients.d
%{_sysconfdir}/X11/xinit/Xclients
%{_sysconfdir}/X11/xinit/Xsession
%dir %{_sysconfdir}/X11/xinit/xinitrc.d
%{_sysconfdir}/X11/xinit/xinitrc.d/*
%{_mandir}/man1/startx.1*
%{_mandir}/man1/xinit.1*

%files session
%defattr(-, root, root,-)
%{_libexecdir}/xinit-compat
%{_datadir}/xsessions/xinit-compat.desktop

%changelog
* Mon Oct 01 2012 Kevin Fenzi <kevin@scrye.com> 1.3.2-7
- Add patch to not switch tty's, so systemd-logind works right with startx. 
- Partially Fixes bug #806491 

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Apr 26 2012 Adam Jackson <ajax@redhat.com> 1.3.2-5
- xinit 1.3.2

* Thu Mar 08 2012 Adam Jackson <ajax@redhat.com> 1.3.1-5
- Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 16 2011 Adam Jackson <ajax@redhat.com> 1.3.1-2
- Drop ConsoleKit integration, being removed in F17

* Mon Jul 25 2011 Matěj Cepl <mcepl@redhat.com> - 1.3.1-1
- New upstream version. Patches updated.

* Sat May 28 2011 Matěj Cepl <mcepl@redhat.com> - 1.0.9-21
- xinitrc-common sources ~/.profile (Bug 551508)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.9-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Sep 25 2010 Parag Nemade <paragn AT fedoraproject.org> - 1.0.9-19
- Merge-review cleanup (#226653)

* Fri Aug 27 2010 Matěj Cepl <mcepl@redhat.com> - 1.0.9-18
- Fix ownership of files.

* Tue Aug 24 2010 Adam Tkac <atkac redhat com> - 1.0.9-17
- rebuild to ensure F14 has higher NVR than F13

* Wed Mar 24 2010 Matěj Cepl <mcepl@redhat.com> - 1.0.9-16
- Remove explicit %%attr from _bindir

* Thu Feb 04 2010 Matěj Cepl <mcepl@redhat.com> - 1.0.9-15
- Add xinit-compat script
  Patch from Rex Dieter, bug 540546
  Move xinit-compat script to -session subpackage.

* Fri Jan 29 2010 Ville Skyttä <ville.skytta@iki.fi> - 1.0.9-14
- Eliminate dependency on which.
- Change Xclients, Xsession and xinitrc-common to make fewer stat calls.
- Install xinitrc-common non-executable.

* Tue Nov 10 2009 Matěj Cepl <mcepl@redhat.com> - 1.0.9-13
- Fix SELinux labels on $errfile (fixes bug# 530419)

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.9-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 17 2009 Nalin Dahyabhai <nalin@redhat.com> - 1.0.9-11
- pull up ck-xinit-session changes for #502258 from from F11 branch

* Sun Jun 14 2009 Matthias Clasen <mclasen@redhat.com> - 1.0.9-10
- Don't own /etc/X11, since its already owned by filesystem

* Mon Jun 08 2009 Matěj Cepl <mcepl@redhat.com> - 1.0.9-9
- consider scripts in /etc/X11/xinit/Xclients.d/ as well
- add back scripts in Release -7 and -8 from F11 branch.

* Fri May 22 2009 Nalin Dahyabhai <nalin@redhat.com> 1.0.9-8
- have ck-xinit-session tell the session bus to set
  XDG_SESSION_COOKIE for services which it autostarts (#502258)
- add direct build dependency on dbus-devel, since we call it
  directly now

* Fri May 08 2009 Adam Jackson <ajax@redhat.com> 1.0.9-7
- xinit-1.0.9-unset.patch: Also unset XDG_SESSION_COOKIE in
  startx. (#489999)

* Wed Mar 11 2009 Adam Jackson <ajax@redhat.com> 1.0.9-6
- xinitrc-common: Load /etc/X11/Xresources with -nocpp

* Wed Feb 25 2009 Adam Tkac <atkac redhat com> 1.0.9-5
- run ck-xinit-session for all sessions where the xdg cookie isn't already
  set (#452156, patch from Patrice Dumas)
- add which Requires (#413041, patch from Patrice Dumas)

* Mon Aug 25 2008 Matthias Clasen <mclasen@redhat.com> 1.0.9-4
- Make the gnome session actually take the gnome case in the switch (#458694)
- Update patches
- Drop upstreamed patch

* Mon Aug 11 2008 Jason L Tibbitts III <tibbs@math.uh.edu> - 1.0.9-3
- Really fix license tag.

* Tue Jul 15 2008 Adam Jackson <ajax@redhat.com> 1.0.9-2
- Fix license tag.

* Wed Jun 11 2008 Adam Jackson <ajax@redhat.com> 1.0.9-1
- xinit 1.0.9

* Tue Apr 08 2008 Adam Jackson <ajax@redhat.com> 1.0.7-7
- Xsession: Don't start ssh-agent for gnome sessions anymore, gnome-keyring
  acts as an agent now. (#441123)

* Wed Mar 12 2008 Ray Strode <rstrode@redhat.com> 1.0.7-6
- Add a new subpackage to add ~/.xsessions and ~/.Xclients
  to session list

* Mon Feb 11 2008 Adam Jackson <ajax@redhat.com> 1.0.7-5
- Xresources: s/don't/do not/, cpp is dumb. (#431704)

* Mon Feb 11 2008 Adam Jackson <ajax@redhat.com> 1.0.7-4
- xinit-1.0.7-unset.patch: Unset various session-related environment
  variables at the top of startx. (#431899)

* Mon Feb  4 2008 Ray Strode <rstrode@redhat.com> 1.0.7-3
- don't special case dbus-launch. dbus-x11 now installs
  a script into /etc/X11/xinit/xinitrc.d.
- Drop the weird grep rule for extensions ending in .sh
  when sourcing /etc/X11/xinit/xinitrc.d

* Fri Oct 12 2007 Nalin Dahyabhai <nalin@redhat.com> 1.0.7-2
- Try opening the console-kit session after the user's UID has already
  been granted access to the server by localuser.sh, so that console-kit-daemon
  can connect and ask the server for information just by having switch to the
  user's UID (#287941).

* Mon Sep 24 2007 Adam Jackson <ajax@redhat.com> 1.0.7-1
- xinit 1.0.7

* Tue Aug 21 2007 Adam Jackson <ajax@redhat.com> - 1.0.2-27
- Rebuild for build id

* Mon Aug 6 2007 Soren Sandmann <sandmann@redhat.com> 1.0.2-26
- Bump release

* Mon Aug 6 2007 Soren Sandmann <sandmann@redhat.com> 1.0.2-25
- Fix typo: s/unask/umask/ - Bug 250882, Jan ONDREJ (ondrejj@salstar.sk)

* Thu Aug 2 2007 Soren Sandmann <sandmann@redhat.com> 1.0.2-24
- Fix bug 212167, CVE-2006-5214

* Sun Jul 29 2007 Soren Sandmann <sandmann@redhat.com> 1.0.2-23
- Fix Xsession to run the login shell inside the setgid ssh-agent, rather
  than the other way around. This preserves LD_LIBRARY_PRELOAD.
  Patch from Stefan Becker, bug 164869.

* Fri Jul 27 2007 Soren Sandmann <sandmann@redhat.com> 1.0.2-22
- Remove xinput.sh. Bug 244963.

* Mon May 21 2007 Adam Jackson <ajax@redhat.com> 1.0.2-21
- localuser.sh: Run silently.

* Sat Apr 22 2007 Matthias Clasen <mclasen@redhat.com> 1.0.2-20
- Don't install INSTALL

* Thu Apr 19 2007 Warren Togami <wtogami@redhat.com> 1.0.2-19
- disable SCIM by default in non-Asian languages #237054
  If you want to use SCIM, use im-chooser to enable it.

* Mon Apr 02 2007 David Zeuthen <davidz@redhat.com> 1.0.2-18
- Man pages are now in section 1, not in section 1x

* Mon Apr 02 2007 David Zeuthen <davidz@redhat.com> 1.0.2-17
- Also BR xorg-x11-util-macros since we autoreconf

* Mon Apr 02 2007 David Zeuthen <davidz@redhat.com> 1.0.2-16
- Add ConsoleKit support (#233183)

* Mon Nov 27 2006 Adam Jackson <ajax@redhat.com> 1.0.2-15
- Bump EVR to fix 6 to 7 updates.

* Fri Nov 10 2006 Ray Strode <rstrode@redhat.com> - 1.0.2-14
- start client in its own session with no controlling tty
  (bug 214649)

* Mon Oct 23 2006 Kristian Høgsberg <krh@redhat.com> - 1.0.2-13
- Update Xsession to not use switchdesk for the hard coded kde and twm
  cases.

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 1.0.2-12
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Mon Sep 25 2006 Kristian Høgsberg <krh@redhat.com> - 1.0.2-11.fc6
- Bump and rebuild.

* Mon Sep 25 2006 Kristian Høgsberg <krh@redhat.com> - 1.0.2-10.fc6
- Move hardcoded xsetroot background color to fallback cases (#205901).

* Thu Aug 17 2006 Kristian Høgsberg <krh@redhat.com> - 1.0.2-9.fc6
- Start ssh-agent for startx also (#169259).

* Sat Jul 22 2006 Adam Jackson <ajackson@redhat.com> 1.0.2-8.fc6
- Fix SourceN line for localuser.sh to not collide.

* Fri Jul 21 2006 Adam Jackson <ajackson@redhat.com> 1.0.2-7.fc6
- Added localuser.sh.

* Wed Jul 19 2006 Mike A. Harris <mharris@redhat.com> 1.0.2-6.fc6
- Added fix to Xclients script, based on patch from bug (#190799)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> 1.0.2-5.1.fc6
- rebuild

* Wed Jul 05 2006 Mike A. Harris <mharris@redhat.com> 1.0.2-5.fc6
- Implemented changes to xinput.sh based on suggestions from (#194458)

* Wed Jun 21 2006 Mike A. Harris <mharris@redhat.com> 1.0.2-4
- Added documentation to doc macro.

* Tue Jun 20 2006 Mike A. Harris <mharris@redhat.com> 1.0.2-3
- Added xinit-1.0.2-setuid.diff to fix potential security issue (#196094)

* Tue Jun 06 2006 Mike A. Harris <mharris@redhat.com> 1.0.2-2
- Added "BuildRequires: pkgconfig" for bug (#194187)

* Thu Apr 27 2006 Adam Jackson <ajackson@redhat.com> 1.0.2-1
- Update xinit to 1.0.2

* Thu Feb 16 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-2
- Change Conflicts to Obsoletes for xorg-x11 and XFree86 (#181414)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> 1.0.1-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> 1.0.1-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan 18 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-1
- Updated to xinit 1.0.1 from X11R7.0

* Fri Dec 16 2005 Mike A. Harris <mharris@redhat.com> 1.0.0-1
- Updated to xinit 1.0.0 from X11R7 RC4.
- Changed manpage dir from man1x to man1 to match upstream default.

* Tue Nov 22 2005 Mike A. Harris <mharris@redhat.com> 0.99.3-6
- Add "Requires: xauth" for startx, to fix bug (#173684)

* Mon Nov 14 2005 Jeremy Katz <katzj@redhat.com> 0.99.3-5
- Do not provide xinit anymore, gdm has been fixed and that breaks things
  with the obsoletes

* Sat Nov 12 2005 Mike A. Harris <mharris@redhat.com> 0.99.3-4
- Added Xsession script from xinitrc, as it is very similar codebase, which
  shares "xinitrc-common" anyway, and all of the display managers use it.

* Fri Nov 11 2005 Mike A. Harris <mharris@redhat.com> 0.99.3-3
- Updated to xinit 0.99.3 from X11R7 RC2.

* Mon Nov 07 2005 Mike A. Harris <mharris@redhat.com> 0.99.2-3
- Added "Provides: xinitrc = 5.0.0-1" for temporary compatibility between
  monolithic and modular X.  This will be removed however for FC5.

* Mon Oct 31 2005 Mike A. Harris <mharris@redhat.com> 0.99.2-2
- Import custom Red Hat xinit scripts from xinitrc package.
- Obsolete xinitrc package, as we include the scripts/configs here now.
- Fix all scripts/configs to avoid the now obsolete /usr/X11R6 prefix.

* Mon Oct 31 2005 Mike A. Harris <mharris@redhat.com> 0.99.2-1
- Updated to xinit 0.99.2 from X11R7 RC1.
- Change manpage location to 'man1x' in file manifest.

* Wed Oct 05 2005 Mike A. Harris <mharris@redhat.com> 0.99.0-2
- Use Fedora-Extras style BuildRoot tag.
- Update BuildRequires to use new library package names.
- Tidy up spec file a bit.

* Wed Aug 24 2005 Mike A. Harris <mharris@redhat.com> 0.99.0-1
- Initial build.
