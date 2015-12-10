Summary: Unobtrusive window manager
Summary(zh_CN.UTF-8): 窗口管理器
Name: metacity
Version:	3.18.1
Release: 5%{?dist}
URL: http://download.gnome.org/sources/metacity/
Source0: http://download.gnome.org/sources/metacity/3.12/metacity-%{version}.tar.xz
# http://bugzilla.gnome.org/show_bug.cgi?id=558723
Patch4: stop-spamming-xsession-errors.patch

# https://bugzilla.gnome.org/show_bug.cgi?id=598995
Patch16: Dont-focus-ancestor-window-on-a-different-workspac.patch
# https://bugzilla.gnome.org/show_bug.cgi?id=559816
Patch24: metacity-2.28-empty-keybindings.patch

License: GPLv2+
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
BuildRequires: gtk2-devel 
BuildRequires: pango-devel 
BuildRequires: fontconfig-devel
BuildRequires: gsettings-desktop-schemas-devel
BuildRequires: desktop-file-utils
BuildRequires: libglade2-devel 
BuildRequires: autoconf, automake, libtool, gnome-common
BuildRequires: intltool
BuildRequires: startup-notification-devel 
BuildRequires: libtool automake autoconf gettext
BuildRequires: xorg-x11-proto-devel 
BuildRequires: libSM-devel, libICE-devel, libX11-devel
BuildRequires: libXext-devel, libXinerama-devel, libXrandr-devel, libXrender-devel
BuildRequires: libXcursor-devel
BuildRequires: libXcomposite-devel, libXdamage-devel
# for gnome-keybindings.pc
BuildRequires: control-center 
BuildRequires: yelp-tools
BuildRequires: zenity
BuildRequires: dbus-devel
BuildRequires: libcanberra-devel
BuildRequires: itstool

Requires: startup-notification 
Requires: gsettings-desktop-schemas
# for /usr/share/control-center/keybindings, /usr/share/gnome/wm-properties
Requires: control-center-filesystem
Requires: zenity

# http://bugzilla.redhat.com/605675
Provides: firstboot(windowmanager) = metacity

%description
Metacity is a window manager that integrates nicely with the GNOME desktop.
It strives to be quiet, small, stable, get on with its job, and stay out of
your attention.

%description -l zh_CN.UTF-8
GNOME3 的窗口管理器。

%package devel
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Summary: Development files for metacity
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the files needed for compiling programs using
the metacity-private library. Note that you are not supposed to write
programs using the metacity-private library, since it is a private
API. This package exists purely for technical reasons.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q
%patch4 -p1 -b .stop-spamming-xsession-errors

%patch16 -p1 -b .focus-different-workspace
%patch24 -p1 -b .empty-keybindings

# force regeneration
rm -f src/org.gnome.metacity.gschema.valid

%build
CPPFLAGS="$CPPFLAGS -I$RPM_BUILD_ROOT%{_includedir}"
export CPPFLAGS

# Always rerun configure for now
rm -f configure
(if ! test -x configure; then autoreconf -i -f; fi;
 %configure --disable-static --disable-schemas-compile)

SHOULD_HAVE_DEFINED="HAVE_SM HAVE_XINERAMA HAVE_XFREE_XINERAMA HAVE_SHAPE HAVE_RANDR HAVE_STARTUP_NOTIFICATION"

for I in $SHOULD_HAVE_DEFINED; do
  if ! grep -q "define $I" config.h; then
    echo "$I was not defined in config.h"
    grep "$I" config.h
    exit 1
  else
    echo "$I was defined as it should have been"
    grep "$I" config.h
  fi
done

make CPPFLAGS="$CPPFLAGS" LIBS="$LIBS" %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

# the desktop file is not valid, I've complained on metacity-devel-list
#desktop-file-install --vendor "" --delete-original \
#	--dir $RPM_BUILD_ROOT%{_datadir}/applications \
#	$RPM_BUILD_ROOT%{_datadir}/applications/metacity.desktop
magic_rpm_clean.sh
%find_lang %{name} --all-name --with-gnome

%post -p /sbin/ldconfig

%posttrans
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :

%postun
/sbin/ldconfig
if [ $1 -eq 0 ]; then
  glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%files -f %{name}.lang
%doc README AUTHORS COPYING NEWS HACKING doc/theme-format.txt doc/metacity-theme.dtd rationales.txt
%{_bindir}/metacity
%{_bindir}/metacity-message
%{_datadir}/glib-2.0/schemas/*
%{_datadir}/GConf/gsettings/metacity-schemas.convert
%{_datadir}/metacity
%{_datadir}/themes/*
%{_datadir}/gnome-control-center/keybindings/*
%{_libdir}/lib*.so.*
%{_mandir}/man1/metacity.1.gz
%{_mandir}/man1/metacity-message.1.gz
%{_datadir}/applications/metacity.desktop
%{_datadir}/gnome/wm-properties/metacity-wm.desktop

%files devel
%defattr(-,root,root,-)
%{_bindir}/metacity-theme-viewer
%{_bindir}/metacity-window-demo
%{_includedir}/*
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*
%{_mandir}/man1/metacity-theme-viewer.1.gz
%{_mandir}/man1/metacity-window-demo.1.gz

%changelog
* Tue Nov 10 2015 Liu Di <liudidi@gmail.com> - 3.18.1-5
- 为 Magic 3.0 重建

* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 3.18.1-4
- 更新到 3.18.1

* Tue Aug 26 2014 Liu Di <liudidi@gmail.com> - 3.12.0-3
- 为 Magic 3.0 重建

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jun 18 2014 Richard Hughes <rhughes@redhat.com> - 3.12.0-1
- Update to 3.12.0

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.34.13-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.34.13-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu May 16 2013 Florian Müllner <fmuellner@redhat.com> - 2.34.13-5
- Include documentation update from upstream

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.34.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 22 2012 Florian Müllner <fmuellner@redhat.com> - 2.34.13-3
- Clean up leftovers from upstream patch removed in commit 24481514

* Tue Nov 20 2012 Matthias Clasen <mclasen@redhat.com> - 2.34.13-2
- Don't use a patch fuzz of 999

* Mon Oct 15 2012 Florian Müllner <fmuellner@redhat.com> - 2.34.13-1
- Update to 2.34.13

* Tue Sep 04 2012 Richard Hughes <hughsient@gmail.com> - 2.34.8-1
- Update to 2.34.8
- Add yelp-tools BR

* Mon Aug 06 2012 Florian Müllner <fmuellner@redhat.com> - 2.34.5-1
- Update to new upstream version, drop upstreamed patch

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.34.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 11 2012 Ville Skyttä <ville.skytta@iki.fi> - 2.34.3-3
- Fix %%post scriptlet dependencies.

* Thu Jun 14 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 2.34.3-2
- Add options to disable mouse button modifers

* Tue Mar 20 2012 Florian Müllner <fmuellner@redhat.com> - 2.34.3-1
- Update to new upstream version

* Sat Feb 18 2012 Michael Schwendt <mschwendt@fedoraproject.org> - 2.34.2-3
- Execute %%postun via /bin/sh not /sbin/ldconfig.

* Wed Feb 15 2012 Florian Müllner <fmuellner@redhat.com> 2.34.2-2
- Explicitly require gsettings-desktop-schemas

* Thu Feb 09 2012 Florian Müllner <fmuellner@redhat.com> 2.34.2-1
- Update to 2.34.2
- Remove patches:
  - screenshot-forkbomb.patch: screenshot keybindings have been moved
    to gnome-settings-daemon
  - workspace.patch: default preference values now defined in
    gsettings-desktop-schemas
  - default-window-icon.patch: included upstream
- Rebase remaining patches
- Adjust spec file to dropped GConf dependency

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.34.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Nov 10 2011 Adam Jackson <ajax@redhat.com> 2.34.1-2
- Rebuild to break bogus libpng dep

* Wed Jul  6 2011 Matthias Clasen <mclasen@redhat.com> - 2.34.1-1
- Update to 2.34.1

* Sun May 22 2011 Daniel Drake <dsd@laptop.org> - 2.34.0-2
- Add upstream patch to allow keybindings ungrab, needed for Sugar

* Mon Apr  4 2011 Matthias Clasen <mclasen@redhat.com> - 2.34.0-1
- Update to 2.34.0

* Mon Feb 28 2011 Colin Walters <walters@verbum.org> - 2.32.0-1.git20110228
- Upstream git snapshot
  Includes Alt-` binding which we really want for gnome-shell
- Drop upstreamed patches
- Switch to my auto-autogen snippet which automatically invokes configure,
  so we can build from a pure git archive
- Instead of using autoreconf, just rm -f configure and let autogen do
  the work
- BR gnome-common so autogen works

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.30.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 13 2011 Matthias Clasen <mclasen@redhat.com> - 2.30.3-4
- Drop gnome-themes dependency

* Tue Oct 26 2010 Parag Nemade <paragn AT fedoraproject.org> - 2.30.3-3
- Gconf2 scriptlet accepts schema file names without file extension.

* Mon Oct 18 2010 Parag Nemade <paragn AT fedoraproject.org> - 2.30.3-2
- Merge-review cleanup (#226138)

* Thu Sep 30 2010 Matthias Clasen <mclasen@redhat.com> - 2.30.3-1
- Update to 2.30.3

* Wed Sep 29 2010 Matthias Clasen <mclasen@redhat.com> - 2.30.2-1
- Update to 2.30.2

* Wed Sep 15 2010 Rex Dieter <rdieter@fedoraproject.org> - 2.30.0-8
- firstboot -> metacity dep (#605675)

* Tue Jul 20 2010 Dan Horák <dan[at]danny.cz> - 2.30.0-7
- updated the nofocuswindows_prefs patch for gcc 4.5

* Wed Jun 23 2010 Owen Taylor <otaylor@redhat.com> - 2.30.0-6
- Add patch to allow breaking out from maximization during mouse resize
  (gnome bz 622517)

* Wed Jun  9 2010 Owen Taylor <otaylor@redhat.com> - 2.30.0-5
- Add a patch to fix confusion between windows (rhbz #533066)
- Add additional tweeks no_focus_windows and new_windows_always_on_top
  preferences (gnome bz 599248, gnome bz 599261)

* Tue Apr 20 2010 Matthias Clasen <mclasen@redhat.com> - 2.30.0-3
- Include the default window icon

* Mon Apr  5 2010 Matthias Clasen <mclasen@redhat.com> - 2.30.0-2
- Don't crash on titlebar right-click

* Wed Mar 31 2010 Matthias Clasen <mclasen@redhat.com> - 2.30.0-1
- Update to 2.30.0

* Fri Feb 26 2010 Matthias Clasen <mclasen@redhat.com> - 2.28.1-3
- Fix linking with pedantic linkers

* Wed Jan 27 2010 Owen Taylor <otaylor@redhat.com> - 2.28.1-2
- Update to 2.28.1, remove 7 patches now applied upstream

* Sun Jan  3 2010 Owen Taylor <otaylor@redhat.com> - 2.28.0-15
- Fix crash in _IceTransClose (rhbz 551994)
  The previous patch for rhbz 539905 didn't actually fix the
  problem; the ICE connection was still being closed twice.

* Thu Dec 17 2009 Owen Taylor <otaylor@redhat.com> - 2.28.0-14
- Fix crash in in tooltip on_style_set() (rhbz 546509)
- Fix Crash in SmcSetProperties() on exit (rhbz 539905, gnome 604867)

* Thu Dec 10 2009 Owen Taylor <otaylor@redhat.com> - 2.28.0-13
- Require gnome-themes rather than nodoka-metacity-theme (rhbz 532455, Stijn Hoop)
- Add patches for GNOME bugs
   445447 - Application-induced window raise fails when raise_on_click off (rhbz 526045)
   530702 - compiz doesn't start if metacity compositor is enabled (rhbz 537791)
   559816 - Doesn't update keybindings being disabled/cleared (rhbz 473224)
   567528 - Cannot raise windows from applications in Tcl/Tk and Java (rhbz 503522)
   577576 - Failed to read saved session file warning on new sessions (rhbz 493245)
   598231 - When Chromium rings the bell, metacity quits (rhbz 532282)
   598995 - Don't focus ancestor window on a different workspace (rhbz 237158)
   599097 - For mouse and sloppy focus, return to "mouse mode" on motion (rhbz 530261)
   599248 - Add no_focus_windows preference to list windows that shouldn't be focused (rhbz 530262)
   599261 - Add a new_windows_always_on_top preference (rhbz 530263)
   599262 - Add XFCE Terminal as a terminal
   604319 - Handle XError and XIOError for unknown displays (rhbz 537845)

* Thu Nov 26 2009 Matthias Clasen <mclasen@redhat.com> - 2.28.0-11
- Fix a problem with the previous change

* Tue Nov 24 2009 Matthias Clasen <mclasen@redhat.com> - 2.28.0-10
- Disable key repeat for screenshot keybinding (#506369)

* Thu Nov 05 2009 Ray Strode <rstrode@redhat.com> 2.28.0-9
- One stab at the metacity patch

* Thu Nov 05 2009 Ray Strode <rstrode@redhat.com> 2.28.0-8
- Minor clean ups to last patch based on feedback from
  Owen

* Thu Nov 05 2009 Ray Strode <rstrode@redhat.com> 2.28.0-7
- Don't do bad things on sigterm

* Wed Oct 28 2009 Matthias Clasen <mclasen@redhat.cm> - 2.28.0-6
- Make tooltips look sharper

* Wed Oct 21 2009 Matthias Clasen <mclasen@redhat.cm> - 2.28.0-4
- Make tooltips look match GTK+

* Thu Oct 15 2009 Matthias Clasen <mclasen@redhat.cm> - 2.28.0-3
- Tweak the default number of workspaces

* Tue Sep 22 2009 Matthias Clasen <mclasen@redhat.cm> - 2.28.0-1
- Update to 2.28.0

* Tue Sep  8 2009 Matthias Clasen <mclasen@redhat.cm> - 2.27.1-1
- Update to 2.27.1

* Wed Sep  2 2009 Peter Robinson <pbrobinson@gmail.com> - 2.27.0-9
- Add upstreamed patch for option to force fullscreen for sugar
- https://bugzilla.redhat.com/show_bug.cgi?id=516225

* Fri Aug 28 2009 Lennart Poettering <lpoetter@redhat.com> - 2.27.0-8
- Actually apply the patch from -7

* Fri Aug 28 2009 Lennart Poettering <lpoetter@redhat.com> - 2.27.0-7
- Apply another trivial patch related to sound events
- http://bugzilla.gnome.org/show_bug.cgi?id=593358

* Fri Aug 28 2009 Lennart Poettering <lpoetter@redhat.com> - 2.27.0-6
- Apply two trivial patches for bell/sound
- http://bugzilla.gnome.org/show_bug.cgi?id=593356
- http://bugzilla.gnome.org/show_bug.cgi?id=593355

* Sat Aug 22 2009 Owen Taylor <otaylor@redhat.com> - 2.27.0-5
- Add a fix for http://bugzilla.gnome.org/show_bug.cgi?id=588119,
  remove no-longer-needed no-lame-dialog patch

* Wed Aug  5 2009 Matthias Clasen  <mclasen@redhat.com> - 2.27.0-4
- Change the default theme to Clearlooks

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.27.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jun  7 2009 Matthias Clasen  <mclasen@redhat.com> - 2.27.0-2
- Make DND work better
- Don't show a lame dialog

* Sun May 31 2009 Matthias Clasen  <mclasen@redhat.com> - 2.27.0-1
- Update to 2.27.0

* Mon Apr 27 2009 Matthias Clasen  <mclasen@redhat.com> - 2.26.0-2
- Don't drop schemas translations from po files

* Mon Mar 16 2009 Matthias Clasen  <mclasen@redhat.com> - 2.26.0-1
- Update to 2.26.0

* Wed Mar 11 2009 Matthias Clasen  <mclasen@redhat.com> - 2.25.144-6
- Fix interaction with autohide panels

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.25.144-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb 21 2009 Matthias Clasen  <mclasen@redhat.com> - 2.25.144-4
- Don't force the bell (#486137)

* Wed Feb 18 2009 Matthias Clasen  <mclasen@redhat.com> - 2.25.144-3
- Update the theme patch to apply to the right file

* Tue Feb 10 2009 Matthias Clasen  <mclasen@redhat.com> - 2.25.144-2
- Use libcanberra to play the alert sound from the sound theme
  for the audible system bell

* Tue Feb  3 2009 Matthias Clasen  <mclasen@redhat.com> - 2.25.144-1
- Update to 2.25.144

* Mon Jan  5 2009 Matthias Clasen  <mclasen@redhat.com> - 2.25.89-1
- Update to 2.25.89

* Tue Dec 16 2008 Matthias Clasen  <mclasen@redhat.com> - 2.25.55-1
- Update to 2.25.55

* Mon Dec 15 2008 Matthias Clasen  <mclasen@redhat.com> - 2.25.34-3
- Clean _NET_SUPPORTING_WM_CHECK on shutdown
- Fix BuildRequires

* Wed Dec  3 2008 Matthias Clasen  <mclasen@redhat.com> - 2.25.34-1
- Update to 2.25.34

* Mon Nov 24 2008 Matthias Clasen  <mclasen@redhat.com> - 2.25.8-4
- Update to 2.25.8

* Sat Nov 22 2008 Matthias Clasen  <mclasen@redhat.com> - 2.25.5-4
- Tweak %%summary and %%description
- Fix BuildRequires

* Wed Nov 12 2008 Matthias Clasen  <mclasen@redhat.com> - 2.25.5-1
- Update to 2.25.5

* Fri Oct 31 2008 Soren Sandmann <sandmann@redhat.com> - 2.24.0-3
- Don't spam .xsession-errors so hard (bug 467802)

* Thu Sep 25 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.0-2
- Save some space

* Mon Sep 22 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.0-1
- Update to 2.24.0

* Fri Sep 19 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.610-2
- Fix some memory leaks

* Tue Sep  9 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.610-1
- Update to 2.23.610

* Tue Sep  2 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.233-1
- Update to 2.23.233

* Fri Aug 22 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.144-1
- Update to 2.23.144

* Tue Jul 15 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.55-1
- Update to 2.23.55

* Tue Jun 17 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.34-1
- Update to 2.23.34

* Tue May 27 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.21-1
- Update to 2.23.21

* Mon May  5 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.13-1
- Update to 2.23.13

* Thu Apr 24 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.8-1
- Update to 2.23.8
- Drop obsolete patches

* Thu Apr 24 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.0-3
- Fix a possible crash in the appearance capplet with
  invalid metacity themes (launchpad #199402)

* Wed Mar 12 2008 Marco Pesenti Gritti <mpg@redhat.com> - 2.22.0-2
- Add patch to fix focus of keep-above windows
  http://bugzilla.gnome.org/show_bug.cgi?id=519188

* Mon Mar 10 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.0-1
- Update to 2.22.0

* Wed Feb 27 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.21-1
- Update to 2.21.21

* Tue Feb 12 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.13-1
- Update to 2.21.13

* Wed Feb  6 2008 Colin Walters <walters@redhat.com> - 2.21.8.svn3554-1
- Drop random macros at top of file; spec files should be as amenable
  to static analysis as possible, easing our way into the bright future
  where our software build process isn't a horrible mismash of a
  preprocessor on shell script, with manual editing required, 
  but something scriptable.
- Update to SVN 3554, to which our patches were designed to apply
- Readd patch metacity-2.21.13-dont-move-windows.patch, which makes
  Firefox behave as those multiple-workspace users desire.

* Wed Feb  6 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.8-1
- Update to 2.21.8

* Sun Feb  3 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.5-3
- Make skip-taskbar windows appear in the ctrl-alt-tab list

* Thu Dec 20 2007 Colin Walters <walters@redhat.com> - 2.21.5-2
- Add patch for avoiding moving windows across workspaces
  This makes clicking on links in firefox do what you want.
  http://bugzilla.gnome.org/show_bug.cgi?id=482354

* Wed Dec 19 2007 Matthias Clasen <mclasen@redhat.com> - 2.21.5-1
- Update to 2.21.5, including the new compositor

* Sun Dec 16 2007 Matthias Clasen <mclasen@redhat.com> - 2.21.3-1
- Update to 2.21.3

* Sun Nov 18 2007 Matthias Clasen <mclasen@redhat.com> - 2.21.2-1
- Update to 2.21.2

* Tue Nov 13 2007 Matthias Clasen <mclasen@redhat.com> - 2.21.1-1
- Update to 2.21.1

* Sun Nov 11 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.0-4
- Fix a crash when the number of workspaces is 1

* Thu Oct 18 2007 Colin Walters <walters@redhat.com> - 2.20.0-3
- Add patch to fix workspace behavior when presenting normal windows

* Thu Sep 27 2007 Ray Strode <rstrode@redhat.com> - 2.20.0-2
- Drop dep on redhat-artwork, add one on nodoka

* Sun Sep 16 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.0-1
- Update to 2.20.0

* Tue Sep 11 2007 Ray Strode <rstrode@redhat.com> - 2.19.55-4
- fix crash on logout (and on the subsequent login, bug 243761)

* Tue Aug 21 2007 Adam Jackson <ajax@redhat.com> - 2.19.55-3
- Rebuild for build id

* Sun Aug 12 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.55-2
- Switch default theme to Nodoka

* Tue Aug  7 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.55-1
- Update to 2.19.55

* Tue Aug  7 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.34-3
- Update license field

* Wed Jul 25 2007 Jesse Keating <jkeating@redhat.com> - 2.19.34-2
- Rebuild for RH #249435

* Mon Jul 23 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.34-1
- Update to 2.19.34

* Fri Jul  6 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.21-3
- Require control-center-filesystem

* Thu Jul  5 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.21-2
- Fix keybindings

* Mon Jun 18 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.21-1
- Update to 2.19.21

* Sun Jun 17 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.13-2
- Clean up directory ownership

* Fri Jun 15 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.13-1
- Update to 2.19.13

* Mon Jun 11 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.8-2
- Don't ship .so.0 in the -devel package (#243689)

* Mon Jun  4 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.8-1
- Update to 2.19.8

* Sat May 19 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.5-1
- Update to 2.19.5

* Tue Apr  3 2007 Matthias Clasen <mclasen@redhat.com> - 2.18.0-2
- Split off a devel package (#203547)
- Some spec file cleanups (#21573)

* Tue Mar 13 2007 Matthias Clasen <mclasen@redhat.com> - 2.18.0-1
- Update to 2.18.0

* Wed Feb 28 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.8-1
- Update to 2.17.8

* Thu Feb 22 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.5-2
- Fix a spec file typo
- Don't ship static libraries

* Wed Jan 17 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.5-1
- Update to 2.17.5

* Mon Nov  6 2006 Matthias Clasen <mclasen@redhat.com> - 2.17.2-1
- Update to 2.17.2

* Fri Oct 20 2006 Matthias Clasen <mclasen@redhat.com> - 2.17.1-1
- Update to 2.17.1

* Wed Oct 18 2006 Matthias Clasen <mclasen@redhat.com> - 2.16.0-7
- Fix scripts according to packaging guidelines

* Tue Oct 17 2006 Matthias Clasen <mclasen@redhat.com> - 2.16.0-6
- Add missing Requires (#203813)

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 2.16.0-5
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Mon Sep 25 2006 Soren Sandmann <sandmann@redhat.com> - 2.16.0-4.fc6
- Build

* Fri Sep 21 2006 Soren Sandmann <sandmann@redhat.com>
- Remove GL dependencies.
- Remove static-cm patch
- add patch to fix more CurrentTime race conditions (bug 206263)

* Thu Sep 14 2006 Ray Strode <rstrode@redhat.com> - 2.16.0-3.fc6
- remove stale ctrl-alt-delete patch

* Sat Sep  9 2006 Soren Sandmann <sandmann@redhat.com> - 2.16.0-2.fc6
- Add patch from Elijah that may fix bug 204519

* Mon Sep  4 2006 Matthias Clasen <mclasen@redhat.com> - 2.16.0-1.fc6
- Update to 2.16.0

* Mon Aug 21 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.34-1.fc6
- Update to 2.15.34
- Require pkgconfig, since we installing a .pc file

* Sun Aug 13 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.21-1.fc6
- Update to 2.15.21
- Uninstall gconf schemas in %%preun

* Mon Aug 7 2006 Soren Sandmann <sandmann@redhat.com> - 2.15.13-2
- Remove leftover snapshot string.

* Mon Aug 7 2006 Soren Sandmann <sandmann@redhat.com> - 2.15.13-1
- Update to 2.15.13. Disable compositing manager.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.15.5-6.1
- rebuild

* Tue Jun 13 2006 Michael J. Knox <michael[AT]knox.net.nz> - 2.15.5-6
- remove BR on automake14, use current automake instead

* Tue Jun 6 2006 Soren Sandmann <sandmann@redhat.com> 2.15.5-5
- Update to new tarball with different intltool magic in it.

* Tue Jun 6 2006 Soren Sandmann <sandmann@redhat.com> 2.15.5-4
- Update intltool BuildRequires to 0.35

* Fri Jun 2 2006 Soren Sandmann <sandmann@redhat.com> 2.15.5-2
- Update intltool BuildRequires to 0.34.90

* Thu Jun 1 2006 Soren Sandmann <sandmann@redhat.com> 2.15.5-1
- Update metacity to a cvs snapshot, and libcm 0.0.22. (The standalone
  libcm package is being put through the package review process). 

* Tue May 30 2006 Kristian Høgsberg <krh@redhat.com> 2.15.3-4
- Bump for rawhide build.

* Mon May 29 2006 Kristian Høgsberg <krh@redhat.com> - 2.15.3-3
- Bump libGL build requires so libcm picks up the right tfp tokens.

* Thu May 18 2006 Soren Sandmann <sandmann@redhat.com> 2.15.3-2
- Update libcm to 0.0.21

* Wed May 17 2006 Matthias Clasen <mclasen@redhat.com> 2.15.3-1
- Update to 2.15.3

* Fri May 12 2006 Adam Jackson <ajackson@redhat.com> 2.15.2-2
- Update protocol dep to 7.0-13 for final EXT_tfp enums, and rebuild.

* Thu May 11 2006 Soren Sandmann <sandmann@redhat.com> 2.15.2-1
- Update to metacity 2.15.2

* Tue Apr 18 2006 Kristian Høgsberg <krh@redhat.com> 2.15.0-6
- Bump for fc5-bling build.

* Thu Apr 13 2006 Soren Sandmann <sandmann@redhat.com> 2.15.0-5
- Update to libcm 0.0.19

* Wed Apr 12 2006 Kristian Høgsberg <krh@redhat.com> 2.15.0-4
- Bump for fc5-bling rebuild.

* Thu Apr 6 2006 Soren Sandmann <sandmann@redhat.com> - 2.16.0-3
- Bump libcm to 0.0.18.

* Mon Apr  3 2006 Soren Sandmann <sandmann@redhat.com> - 2.15.0-2
- Fix leftover libcm-snapshot-date, buildrequire libXcomposite-devel >= 0.3

* Fri Mar 31 2006 Soren Sandmann <sandmann@redhat.com> - 2.15.0
- Update to 2.15.0

* Mon Mar 13 2006 Ray Strode <rstrode@redhat.com> - 2.14.0-1
- update to 2.14.0

* Mon Mar  6 2006 Ray Strode <rstrode@redhat.com> - 2.13.144-1
- update to 2.13.144
- add bling patch from HEAD

* Sun Feb 19 2006 Ray Strode <rstrode@redhat.com> - 2.13.89.0.2006.02.17-2
- disable compositor on s390 s390x and ppc64

* Fri Feb 17 2006 Ray Strode <rstrode@redhat.com> - 2.13.89.0.2006.02.17-1
- Update to latest cvs snapshot to give meaningful failure error
  messages
- Don't remove build root in install, because it triggers a
  rebuild of metacity

* Thu Feb 16 2006 Ray Strode <rstrode@redhat.com> - 2.13.89.0.2006.02.16-1
- Update to cvs snapshot to add the ability to 
  runtime enable compositor
- change %%makeinstall to make install DESTDIR=..

* Mon Feb 13 2006 Matthias Clasen <mclasen@redhat.com> - 2.13.89-1
- Update to 2.13.89

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.13.55-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.13.55-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Jan 30 2006 Matthias Clasen <mclasen@redhat.com> 2.13.55-1
- Update to 2.13.55

* Thu Jan 26 2006 Matthias Clasen <mclasen@redhat.com> 2.13.34-1
- Update to 2.13.34

* Mon Jan 16 2006 Ray Strode <rstrode@redhat.com> 2.13.21-1
- Update to 2.13.21

* Fri Jan 13 2006 Matthias Clasen <mclasen@redhat.com> 2.13.13-1
- Update to 2.13.13

* Tue Jan 03 2006 Matthias Clasen <mclasen@redhat.com> 2.13.8-1
- Update to 2.13.8

* Thu Dec 15 2005 Matthias Clasen <mclasen@redhat.com> 2.13.5-1
- Update to 2.13.5

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Dec  1 2005 Matthias Clasen <mclasen@redhat.com> 2.13.3-1
- Update to 2.13.3

* Mon Nov 21 2005 Ray Strode <rstrode@redhat.com> 2.13.2-1
- Update to 2.13.2

* Fri Nov 18 2005 Bill Nottingham <notting@redhat.com>
- remove references to obsolete X11R6 paths

* Thu Oct  6 2005 Matthias Clasen <mclasen@redhat.com> 2.12.1-1
- Update to 2.12.1

* Thu Sep  8 2005 Matthias Clasen <mclasen@redhat.com> 2.12.0-1
- Update to 2.12.0

* Thu Sep  1 2005 Ray Strode <rstrode@redhat.com> 2.11.2-3
- truncate long window titles to 512 characters (bug 164071)

* Tue Aug 16 2005 Warren Togami <wtogami@redhat.com> 2.11.2-2
- rebuild for new cairo

* Tue Aug  9 2005 Ray Strode <rstrode@redhat.com> 2.11.2-1
- Update to 2.11.2 (fixes bug 163745)

* Fri Aug  5 2005 Matthias Clasen <mclasen@redhat.com> 2.11.1-1
- New upstream version

* Mon Jul 18 2005 Matthias Clasen <mclasen@redhat.com> 2.11.0-3
- fix xcursor detection

* Wed Jul 13 2005 Matthias Clasen <mclasen@redhat.com> 2.11.0-1
- newer upstream version

* Mon May 30 2005 Warren Togami <wtogami@redhat.com> 2.10.0-2
- raise demands attention (#157271 newren)

* Sun Apr  3 2005 Ray Strode <rstrode@redhat.com> 2.10.0-1
- Update to 2.10.0

* Thu Mar 17 2005 Matthias Clasen <mclasen@redhat.com> 2.9.21-2
- Switch to Clearlooks as default theme

* Mon Feb 28 2005 Matthias Clasen <mclasen@redhat.com> 2.9.21-1
- Update to 2.9.21

* Wed Feb  9 2005 Matthias Clasen <mclasen@redhat.com> 2.9.13-1
- Update to 2.9.13

* Fri Jan 28 2005 Matthias Clasen <mclasen@redhat.com> 2.9.8-1
- Update to 2.9.8

* Sat Oct 16 2004 Havoc Pennington <hp@redhat.com> 2.8.6-2
- remove all the rerunning of autotools, intltool, etc. cruft; seemed to be breaking build

* Fri Oct 15 2004 Havoc Pennington <hp@redhat.com> 2.8.6-1
- upgrade to 2.8.6, fixes a lot of focus bugs primarily.

* Fri Oct 15 2004 Soren Sandmann <sandmann@redhat.com> - 2.8.5-3
- Kludge around right alt problem (#132379)

* Mon Oct 11 2004 Alexander Larsson <alexl@redhat.com> - 2.8.5-2
- Require startup-notification 0.7 (without this we'll crash)

* Thu Sep 23 2004 Alexander Larsson <alexl@redhat.com> - 2.8.5-1
- update to 2.8.5

* Tue Aug 31 2004 Alex Larsson <alexl@redhat.com> 2.8.4-1
- update to 2.8.4

* Tue Aug 24 2004 Warren Togami <wtogami@redhat.com> 2.8.3-1
- update to 2.8.3

* Thu Aug  5 2004 Mark McLoughlin <markmc@redhat.com> 2.8.2-1
- Update to 2.8.2
- Remove systemfont patch - upstream now

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu May  6 2004 Havoc Pennington <hp@redhat.com> 2.8.1-2
- fix mangled Summary

* Thu May  6 2004 Havoc Pennington <hp@redhat.com> 2.8.1-1
- 2.8.1

* Thu Apr  1 2004 Alex Larsson <alexl@redhat.com> 2.8.0-1
- update to 2.8.0

* Wed Mar 10 2004 Mark McLoughlin <markmc@redhat.com> 2.7.1-1
- Update to 2.7.1

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Feb 25 2004 Alexander Larsson <alexl@redhat.com> 2.7.0-1
- update to 2.7.0
- removed reduced resouces patch (its now upstream)

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Oct 27 2003 Havoc Pennington <hp@redhat.com> 2.6.3-1
- 2.6.3

* Wed Oct  1 2003 Havoc Pennington <hp@redhat.com> 2.6.2-1
- 2.6.2

* Thu Sep  4 2003 Havoc Pennington <hp@redhat.com> 2.5.3-3
- put reduced resources patch back in

* Fri Aug 22 2003 Elliot Lee <sopwith@redhat.com> 2.5.3-2
- Work around libXrandr need for extra $LIBS

* Fri Aug 15 2003 Alexander Larsson <alexl@redhat.com> 2.5.3-1
- update for gnome 2.3

* Mon Jul 28 2003 Havoc Pennington <hp@redhat.com> 2.4.55-7
- rebuild

* Mon Jul 28 2003 Havoc Pennington <hp@redhat.com> 2.4.55-6
- backport the "reduced_resources" patch with wireframe

* Mon Jul 07 2003 Christopher Blizzard <blizzard@redhat.com> 2.4.55-4
- add patch to fix mouse down problems in mozilla

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu May 29 2003 Havoc Pennington <hp@redhat.com> 2.4.55-2
- rebuild

* Thu May 29 2003 Havoc Pennington <hp@redhat.com> 2.4.55-1
- 2.4.55

* Wed May 14 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- add proper ldconfig calls for shared libs

* Mon Feb 24 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 21 2003 Havoc Pennington <hp@redhat.com> 2.4.34-2
- fix a crash in multihead situations, #84412

* Wed Feb  5 2003 Havoc Pennington <hp@redhat.com> 2.4.34-1
- 2.4.34
- try disabling smp_mflags and see if it fixes build

* Wed Jan 22 2003 Havoc Pennington <hp@redhat.com>
- 2.4.21.90 with a bunch o' fixes

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Jan 16 2003 Havoc Pennington <hp@redhat.com>
- bind Ctrl+Alt+Del to logout, #72973

* Wed Jan 15 2003 Havoc Pennington <hp@redhat.com>
- 2.4.13.90 cvs snap with event queue lag fix

* Fri Jan 10 2003 Havoc Pennington <hp@redhat.com>
- 2.4.13

* Thu Dec 12 2002 Havoc Pennington <hp@redhat.com>
- 2.4.8

* Mon Dec  2 2002 Havoc Pennington <hp@redhat.com>
- 2.4.5.90
- add little script after configure that checks what config.h
  contains, to be sure we detected all the right features.

* Tue Oct 29 2002 Havoc Pennington <hp@redhat.com>
- 2.4.3
- remove patches that have gone upstream

* Tue Aug 27 2002 Havoc Pennington <hp@redhat.com>
- fix shaded window decorations in Bluecurve theme

* Sat Aug 24 2002 Havoc Pennington <hp@redhat.com>
- fix the mplayer-disappears-on-de-fullscreen bug

* Sat Aug 24 2002 Havoc Pennington <hp@redhat.com>
- add some fixes from CVS for #71163 #72379 #72478 #72513

* Thu Aug 22 2002 Havoc Pennington <hp@redhat.com>
- patch .schemas.in instead of .schemas so we get right default theme/fonts

* Tue Aug 20 2002 Havoc Pennington <hp@redhat.com>
- grow size of top resize, and display proper cursor on enter notify
- require latest intltool to try and fix metacity.schemas by
  regenerating it in non-UTF-8 locale

* Thu Aug 15 2002 Havoc Pennington <hp@redhat.com>
- default to Sans Bold font, fixes #70920 and matches graphic design spec

* Thu Aug 15 2002 Havoc Pennington <hp@redhat.com>
- 2.4.0.91 with raise/lower keybindings for msf, fixes to fullscreen
- more apps that probably intend to be, fix for changing number of
  workspaces, fix for moving windows in multihead

* Tue Aug 13 2002 Havoc Pennington <hp@redhat.com>
- update build requires

* Mon Aug 12 2002 Havoc Pennington <hp@redhat.com>
- upgrade to cvs snap 2.4.0.90 with pile of bugfixes from 
  this weekend
- change default theme to bluecurve and require new redhat-artwork

* Tue Aug  6 2002 Havoc Pennington <hp@redhat.com>
- 2.4.0
- themes are moved, require appropriate redhat-artwork

* Thu Aug  1 2002 Havoc Pennington <hp@redhat.com>
- munge the desktop file to be in toplevel menus and 
  not show in KDE

* Tue Jul 23 2002 Havoc Pennington <hp@redhat.com>
- don't use system font by default as metacity's 
  font is now in the system font dialog

* Tue Jul 23 2002 Havoc Pennington <hp@redhat.com>
- 2.3.987.92 cvs snap

* Fri Jul 12 2002 Havoc Pennington <hp@redhat.com>
- 2.3.987.91 cvs snap

* Mon Jun 24 2002 Havoc Pennington <hp@redhat.com>
- 2.3.987.90 cvs snap

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun Jun 16 2002 Havoc Pennington <hp@redhat.com>
- rebuild for new libraries

* Mon Jun 10 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment

* Mon Jun 10 2002 Havoc Pennington <hp@redhat.com>
- 2.3.987
- default to redhat theme

* Fri Jun 07 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment

* Tue Jun  4 2002 Havoc Pennington <hp@redhat.com>
- 2.3.610.90 cvs snap

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon May 20 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment

* Fri May 17 2002 Havoc Pennington <hp@redhat.com>
- 2.3.377

* Thu May  2 2002 Havoc Pennington <hp@redhat.com>
- 2.3.233

* Thu Apr 25 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment
- add gconf schemas boilerplate

* Mon Apr 15 2002 Havoc Pennington <hp@pobox.com>
- 2.3.89

* Tue Oct 30 2001 Havoc Pennington <hp@redhat.com>
- 2.3.34

* Fri Oct 13 2001 Havoc Pennington <hp@redhat.com>
- 2.3.21 

* Mon Sep 17 2001 Havoc Pennington <hp@redhat.com>
- 2.3.8
- 2.3.13

* Wed Sep  5 2001 Havoc Pennington <hp@redhat.com>
- Initial build.


