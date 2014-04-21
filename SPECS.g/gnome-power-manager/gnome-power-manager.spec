Summary: GNOME power management service
Summary(zh_CN.UTF-8): GNOME 电源管理服务
Name: gnome-power-manager
Version:	3.12.0
Release: 2%{?dist}
License: GPLv2+ and GFDL
Group: Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
Source: http://download.gnome.org/sources/gnome-power-manager/%{majorver}/gnome-power-manager-%{version}.tar.xz
URL: http://projects.gnome.org/gnome-power-manager/

BuildRequires: desktop-file-utils
BuildRequires: gettext
BuildRequires: libtool
BuildRequires: cairo-devel
BuildRequires: upower-devel >= 0.9.0
BuildRequires: intltool
BuildRequires: glib2-devel >= 2.25.9
BuildRequires: gtk3-devel >= 2.91.3
BuildRequires: docbook-utils

Requires: gnome-icon-theme

# obsolete sub-package
Obsoletes: gnome-power-manager-extra <= 2.30.1
Provides: gnome-power-manager-extra

%description
GNOME Power Manager uses the information and facilities provided by UPower
displaying icons and handling user callbacks in an interactive GNOME session.

%description -l zh_CN.UTF-8 
这个包使用 Upower 提供的信息和功能显示和处理电源管理。

%prep
%setup -q

%build
%configure --disable-scrollkeeper

%install
make install DESTDIR=$RPM_BUILD_ROOT
magic_rpm_clean.sh
%find_lang %name --with-gnome

%postun
update-desktop-database %{_datadir}/applications &> /dev/null || :
if [ $1 -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor
  gtk-update-icon-cache -q %{_datadir}/icons/hicolor &> /dev/null || :
  glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans
touch --no-create %{_datadir}/icons/hicolor
gtk-update-icon-cache -q %{_datadir}/icons/hicolor &> /dev/null || :
update-desktop-database %{_datadir}/applications &> /dev/null || :
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :

%files -f %{name}.lang
%doc AUTHORS COPYING README
%{_bindir}/*
%{_datadir}/applications/*.desktop
%{_datadir}/glib-2.0/schemas/*.gschema.xml
#%{_datadir}/gnome-power-manager/*.ui
%{_datadir}/appdata/gnome-power-statistics.appdata.xml
%{_datadir}/icons/HighContrast/*/*/*.*
%{_datadir}/icons/hicolor/*/apps/gnome-power-statistics.*
#%dir %{_datadir}/gnome-power-manager
%{_datadir}/glib-2.0/schemas/*.gschema.xml
%{_mandir}/man1/*.1.gz

%changelog
* Wed Apr 09 2014 Liu Di <liudidi@gmail.com> - 3.12.0-2
- 更新到 3.12.0

* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 3.2.1-2
- 为 Magic 3.0 重建

* Mon Oct 17 2011 Richard Hughes <rhughes@redhat.com> - 3.2.1-1
- New upstream version.

* Mon Sep 26 2011 Richard Hughes <rhughes@redhat.com> - 3.2.0-1
- New upstream version.

* Mon Sep 19 2011 Richard Hughes <rhughes@redhat.com> - 3.1.92-1
- New upstream version.

* Wed Sep 14 2011 Richard Hughes <rhughes@redhat.com> - 3.1.90-2
- Fix an error in the postun scriptlet
- Require gnome-settings-daemon as we use its schema.

* Tue Aug 30 2011 Richard Hughes <rhughes@redhat.com> - 3.1.90-1
- New upstream version.

* Mon Jul 25 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.3-1
- Update to 3.1.3

* Mon Jun 13 2011 Richard Hughes <rhughes@redhat.com> - 3.1.2-2
- Add BR gnome-keyring-devel

* Mon Jun 13 2011 Richard Hughes <rhughes@redhat.com> - 3.1.2-1
- New upstream version.

* Mon Apr 04 2011 Richard Hughes <rhughes@redhat.com> - 3.0.0-1
- New upstream version.

* Mon Mar 29 2011 Richard Hughes  <rhughes@redhat.com> - 2.91.93-1
- New upstream release.

* Mon Mar 21 2011 Richard Hughes  <rhughes@redhat.com> - 2.91.92-2
- Add BR docbook-utils for the manpages.

* Mon Mar 21 2011 Richard Hughes  <rhughes@redhat.com> - 2.91.92-1
- New upstream release.

* Fri Feb 11 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.5-4
- Rebuild against newer gtk

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.91.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.5-2
- Rebuild

* Tue Jan 11 2011 Richard Hughes  <rhughes@redhat.com> - 2.91.5-1
- New upstream release.

* Fri Jan  7 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.4-1
- Update to 2.91.4

* Wed Dec 15 2010 Dan Williams <dcbw@redhat.com> - 2.91.3-3
- Fix crash due to bad reference counting (rh #662279)

* Fri Dec  3 2010 Matthias Clasen <mclasen@redhat.com> - 2.91.3-2
- Rebuild against new gtk

* Wed Dec 01 2010 Richard Hughes  <rhughes@redhat.com> - 2.91.3-1
- New upstream release.

* Mon Nov 08 2010 Richard Hughes  <rhughes@redhat.com> - 2.91.2-2
- Fix up the tarball location.

* Mon Nov 08 2010 Richard Hughes  <rhughes@redhat.com> - 2.91.2-1
- New upstream release.

* Wed Nov 03 2010 Richard Hughes <richard@hughsie.com> 2.91.2-0.2.20101102
- Rebuild now libnotify 0.7.0 is in rawhide.

* Tue Nov 02 2010 Richard Hughes <richard@hughsie.com> 2.91.2-0.1.20101102
- Update to a git snapshot to fix rawhide.

* Mon Oct 04 2010 Richard Hughes  <rhughes@redhat.com> - 2.91.1-1
- New upstream release.

* Tue Sep 28 2010 Matthias Clasen <mclasen@redhat.com> - 2.32.0-1
- Update to 2.32.0

* Mon Aug 23 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.90-1
- Update to 2.31.90
- Include some fixes for backlight handling

* Thu Jul 01 2010 Richard Hughes  <rhughes@redhat.com> - 2.31.4-1
- New upstream release.

* Mon Jun 28 2010 Matthias Clasen <mclasen@redhat.com> - 2.21.3-2
- Rebuild

* Wed Jun 21 2010 Richard Hughes  <rhughes@redhat.com> - 2.31.3-1
- New upstream release.
- This release requires new versions of glib2, gtk3 and others.

* Fri Jun 18 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.1-3
- Drop more unneded direct deps

* Wed Jun 16 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.1-2
- Drop scrollkeeper dep

* Wed Jun 02 2010 Richard Hughes  <rhughes@redhat.com> - 2.31.1-1
- New upstream release.
- This release no longer requires HAL. It may also eat your cat.

* Mon Apr 26 2010 Richard Hughes  <rhughes@redhat.com> - 2.30.1-1
- New upstream release.
- Fix up a critical warning from the GpmScreensaver code.
- Only dim the screen on idle when on the active console.
- Many translation updates.

* Mon Mar 29 2010 Richard Hughes  <rhughes@redhat.com> - 2.30.0-1
- New upstream release.

* Mon Mar 15 2010 Richard Hughes  <rhughes@redhat.com> - 2.29.91-4
- Update to the latest version of the Fedora Packaging Guidelines
- Do not run scrollkeeper-update
- Remove the custom BuildRoot
- Do not clean the buildroot before install
- Use the gconf_schema defines for the GConf schemas

* Mon Mar 15 2010 Bastien Nocera <bnocera@redhat.com> 2.29.91-3
- Really enable HAL build and fix compilation (#572896)

* Thu Mar 11 2010 Bastien Nocera <bnocera@redhat.com> 2.29.91-2
- Update to 2.29.91
- Revert HAL removal, or some machines wouldn't have brightness
  handling any more

* Mon Feb 02 2010 Richard Hughes  <rhughes@redhat.com> - 2.29.2-1
- Update to 2.29.2

* Fri Dec 18 2009 Matthias Clasen <mclasen@redhat.com> - 2.29.1-2
- Avoid warning messages at startup

* Tue Dec 08 2009 Richard Hughes  <rhughes@redhat.com> - 2.29.1-1
- Update to 2.29.1
- Remove upstreamed patches

* Mon Dec 07 2009 Bastien Nocera <bnocera@redhat.com> 2.28.1-5
- Remove HAL dependency

* Wed Oct 28 2009 Bastien Nocera <bnocera@redhat.com> 2.28.1-4
- Match gnome-settings-daemon's positioning for the OSD

* Tue Oct 27 2009 Bastien Nocera <bnocera@redhat.com> 2.28.1-3
- Update OSD to match gnome-settings-daemon's

* Thu Oct 22 2009 Richard Hughes  <rhughes@redhat.com> - 2.28.1-2
- Backport two patches from git master to polish the UI for F12.

* Mon Oct 19 2009 Richard Hughes  <rhughes@redhat.com> - 2.28.1-1
- Update to 2.28.1
- Translation updates
- Remove upstreamed patch
- Help the kernel through its sleep key confusion
- Correctly set the focus on the last used device in gnome-power-statistics
- Do not hide some radio buttons depending on the current machine state
- Throttle screensaver before suspend/hibernate

* Tue Oct 13 2009 Matthias Clasen <mclasen@redhat.com> - 2.28.0-2
- Fix possible segfault

* Mon Sep 21 2009 Richard Hughes  <rhughes@redhat.com> - 2.28.0-1
- Update to 2.28.0

* Mon Sep 07 2009 Richard Hughes  <rhughes@redhat.com> - 2.27.92-1
- Update to 2.27.92

* Mon Aug 24 2009 Richard Hughes  <rhughes@redhat.com> - 2.27.91-1
- Update to 2.27.91

* Tue Aug 11 2009 Ville Skyttä <ville.skytta@iki.fi> - 2.27.5-2
- Use bzipped upstream tarball.

* Mon Aug 03 2009 Richard Hughes  <rhughes@redhat.com> - 2.27.5-1
- Update to 2.27.5

* Thu Jul 30 2009 Richard Hughes  <rhughes@redhat.com> - 2.27.3-0.5.20090730git
- Update to todays git snapshot.
- Split the inhibit applet and gnome-power-statistics into an
  gnome-power-manager-extra subpackage.
- Remove upstreamed patches.
- Fixes #514249

* Mon Jul 27 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.3-0.4.20090727git
- Drop an unneeded include that broke the build

* Mon Jul 27 2009 Richard Hughes  <rhughes@redhat.com> - 2.27.3-0.2.20090727git
- Update to todays git snapshot.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.27.3-0.3.20090721git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 21 2009 Richard Hughes  <rhughes@redhat.com> - 2.27.3-0.2.20090721git
- Update to todays git snapshot to fix some issues found during the test day.

* Tue Jul 21 2009 Richard Hughes  <rhughes@redhat.com> - 2.27.3-0.1.20090721git
- Update to todays git snapshot to fix many issues with multiple composite
  laptop batteries and notifications.

* Tue Jul 07 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2.27.2-2
- Fix file ownership so that only this packages manpages are owned, 
  resolves duplicate directory ownership with "filesystem" package

* Mon Jul 06 2009 Richard Hughes  <rhughes@redhat.com> - 2.27.2-1
- Update to 2.27.1

* Tue Jun 16 2009 Richard Hughes  <rhughes@redhat.com> - 2.27.2-0.2.20090616git
- Apply a patch to convert to the PolKit1 API.
- Do autoreconf as the polkit patch is pretty invasive

* Tue Jun 16 2009 Richard Hughes  <rhughes@redhat.com> - 2.27.2-0.1.20090616git
- Update to todays git snapshot to fix many issues with multiple composite
  laptop batteries.

* Mon Jun 01 2009 Richard Hughes  <rhughes@redhat.com> - 2.27.1-1
- Update to 2.27.1

* Mon May 11 2009 Richard Hughes  <rhughes@redhat.com> - 2.27.1-0.4.20090507git
- Make build harder, this time with patience.

* Thu May 07 2009 Richard Hughes  <rhughes@redhat.com> - 2.27.1-0.3.20090507git
- Make build harder.

* Thu May 07 2009 Richard Hughes  <rhughes@redhat.com> - 2.27.1-0.2.20090507git
- Make build.

* Thu May 07 2009 Richard Hughes  <rhughes@redhat.com> - 2.27.1-0.1.20090507git
- Update to todays git snapshot
- Drop upstreamed patches

* Mon Apr 27 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.0-3
- Don't drop schemas translations from po files

* Sat Apr 18 2009 Lubomir Rintel <lkundrak@v3.sk> - 2.26.0-2
- Fix broken battery capacity percentage reporting

* Mon Mar 16 2009 Richard Hughes  <rhughes@redhat.com> - 2.26.0-1
- Update to 2.26.0

* Mon Mar 09 2009 Richard Hughes  <rhughes@redhat.com> - 2.25.92-1
- Update to 2.25.92

* Fri Feb 27 2009 Richard Hughes  <rhughes@redhat.com> - 2.25.91-7
- We actually neeed BuildRequires PolicyKit-gnome-devel too

* Fri Feb 27 2009 Richard Hughes  <rhughes@redhat.com> - 2.25.91-6
- We actually neeed BuildRequires PolicyKit-devel

* Fri Feb 27 2009 Richard Hughes  <rhughes@redhat.com> - 2.25.91-5
- Backport patch from svn to not block logout

* Fri Feb 27 2009 Matthias Clasen <mclasen@redhat.com> - 2.25.91-4
- Require PolicyKit-authentication-agent

* Wed Feb 25 2009 Richard Hughes  <rhughes@redhat.com> - 2.25.91-3
- Enable legacy buttons so we get lid events. Eurgh.

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.25.91-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 11 2009 Richard Hughes  <rhughes@redhat.com> - 2.25.91-1
- Update to 2.25.91

* Thu Feb 05 2009 Richard Hughes  <rhughes@redhat.com> - 2.25.3-3
- Rebuild as desktop-files-utils should now be fixed and allow the build.

* Wed Feb 04 2009 Adam Jackson <ajax@redhat.com> 2.25.3-2
- gpm-2.25.3-idletime-hilarity.patch: Ask for edge triggers on system idle
  time, not level triggers. The latter lead to wakeup storms and sadness.

* Mon Feb 02 2009 Richard Hughes  <rhughes@redhat.com> - 2.25.3-1
- Update to 2.25.3
- New processor wakeup functionality in gnome-power-statistics

* Wed Jan  7 2009 Matthias Clasen <mclasen@redhat.com> - 2.25.2-1
- Update to 2.25.2

* Fri Dec 19 2008 Matthias Clasen <mclasen@redhat.com> - 2.25.1-2
- Fix the spec file 

* Thu Dec 18 2008 Richard Hughes  <rhughes@redhat.com> - 2.25.1-1
- Update to 2.25.1
- Depend on DeviceKit-power
- Build with PolicyKit support enabled
- Drop gstreamer and pick up libcanberra deps

* Fri Nov 21 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.2-3
- Better URL

* Tue Nov 18 2008 Richard Hughes  <rhughes@redhat.com> - 2.24.2-2
- Update to 2.24.2
- Duplicate button presses should now be detected
- Drop upstreamed patches

* Fri Oct 31 2008 Matthias Clasen  <mclasen@redhat.com> - 2.24.1-3
- Make "Make default" button work

* Fri Oct 24 2008 Richard Hughes  <rhughes@redhat.com> - 2.24.1-2
- Backport some patches from trunk to fix:
 - Duplicate buttons from X and HAL
 - Use the Sessionmanager rather than the old gnome_client_request_save
 - Ignore policy actions when the session is not active

* Wed Oct 22 2008 Richard Hughes  <rhughes@redhat.com> - 2.24.1-1
- Update to 2.24.1

* Thu Oct 09 2008 Ray Strode <rstrode@redhat.com> - 2.24.0-6
- Enable policy kit support

* Wed Oct 08 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.0-5
- Save some more space

* Thu Sep 25 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.0-4
- Save some space

* Mon Sep 22 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.0-2
- Update to 2.24.0

* Mon Sep 01 2008 Richard Hughes  <rhughes@redhat.com> - 2.23.91-1
- Update to 2.23.91, which should some translation issues.

* Mon Aug 25 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.6-4
- Drop the login session .desktop file, since gdm provides it now

* Thu Aug 14 2008 David Zeuthen <davidz@redhat.com> - 2.23.6-3
- Actually make the patch apply and rebuild

* Thu Aug 14 2008 Richard Hughes  <rhughes@redhat.com> - 2.23.6-2
- Apply a fix from upstream to fix crashing on percentage change.

* Wed Aug 06 2008 Richard Hughes  <rhughes@redhat.com> - 2.23.6-1
- Update to 2.23.6, which should the Eee and some Policykit stuff.

* Tue Jul 31 2008 Richard Hughes  <rhughes@redhat.com> - 2.23.3-4
- Rebuild for libunique ABI break.

* Wed Jul 23 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.23.3-3
- fix license tag

* Tue Jul 01 2008 Richard Hughes  <rhughes@redhat.com> - 2.23.3-1
- Update to 2.23.3, which should fix backlight brightness.

* Fri May 20 2008 Richard Hughes  <rhughes@redhat.com> - 2.23.1-2
- Add a BR on Policykit-gnome

* Fri May 20 2008 Richard Hughes  <rhughes@redhat.com> - 2.23.1-1
- Update to 2.23.1

* Fri May 16 2008 Richard Hughes  <rhughes@redhat.com> - 2.22.1-3
- Add a BR on unique to make the client tools single instance

* Sun Apr 13 2008 Richard Hughes  <rhughes@redhat.com> - 2.22.1-2
- Fix the homepage URL to http://www.gnome.org/projects/gnome-power-manager/

* Fri Mar 28 2008 Bill Nottingham <notting@redhat.com> - 2.22.1-1
- update to 2.22.1

* Mon Mar 10 2008 Jon McCann <jmccann@redhat.com> - 2.22.0-1
- Update to 2.22.0

* Mon Feb 18 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.92-2
- Plug an X resource leak in the brightness applet

* Thu Feb 14 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.92-1
- Update to 2.21.92

* Sat Jan 26 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.1-2
- Save some space

* Mon Dec 17 2007 Matthias Clasen <mclasen@redhat.com> - 2.21.1-1
- Update to 2.21.1

* Fri Dec 14 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.2-1
- Update to 2.20.2

* Tue Nov 13 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.1-1
- Update to 2.20.1
- Drop upstreamed patches

* Tue Oct 23 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.0-7
- Rebuild against new dbus-glib

* Tue Oct 16 2007 David Zeuthen <davidz@redhat.com> - 2.20.0-6
- When hibernate is triggered by system idle, avoid suspending
  right after resuming from hibernate (#329541)

* Sat Oct  6 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.0-5
- Fix a thinko in the previous patch (#321671)

* Fri Oct  5 2007 David Zeuthen <davidz@redhat.com> - 2.20.0-4
- Rebuild

* Fri Oct  5 2007 David Zeuthen <davidz@redhat.com> - 2.20.0-3
- Fix the "Sleep problem" popup (#312761)

* Fri Oct  5 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.0-2
- Make the inhibit applet work with all background settings 
  of the panel.

* Mon Sep 17 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.0-1
- Update to 2.20.0

* Tue Sep  4 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.92-1
- Update to 2.19.92

* Tue Aug 28 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 2.19.6-3
- Rebuild for selinux ppc32 issue.

* Tue Aug  7 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.6-2
- Update license field
- Use %%find_lang for help files

* Sun Jul 29 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.6-1
- Update to 2.19.6

* Fri Jul  6 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.5-1
- Update to 2.19.5

* Tue Jun  5 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.2-3
- Rebuild again

* Mon Jun  4 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.2-2
- Rebuild against new libwnck

* Sun May 20 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.2-1
- Update to 2.19.2

* Wed May 16 2007 Matthias Clasen <mclasen@redhat.com> - 2.18.2-4
- Don't put markup in notification summaries (#240258)

* Sun May  6 2007 Matthias Clasen <mclasen@redhat.com> - 2.18.2-3
- Avoid a crash in gnome-power-statistics if the daemon
  is not running (#239228)

* Fri Apr 27 2007 David Zeuthen <davidz@redhat.com> - 2.18.2-2
- Remove broken nodefaultbeep patch as it was wrongly applied to disable
  battery recall warnings - gotta love patch(1) (#238087)

* Fri Apr 13 2007 Ray Strode <rstrode@redhat.com> - 2.18.2-1
- Update to 2.18.2

* Sat Mar 31 2007 Matthias Clasen <mclasen@redhat.com> - 2.18.1-2
- Add bug-buddy support to the applets 

* Fri Mar 23 2007 Ray Strode <rstrode@redhat.com> - 2.18.1-1
- Update to 2.18.1

* Tue Mar 13 2007 Matthias Clasen <mclasen@redhat.com> - 2.18.0-1
- Update to 2.18.0

* Thu Mar 08 2007 Adam Jackson <ajax@redhat.com> 2.17.92-2
- gnome-power-manager-2.17.92-dpms-query-less.patch: DPMSCapable() can never
  change for a given display, so cache the result and cut our wakeups in half.

* Wed Feb 28 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.92-1
- Update to 2.17.92

* Tue Feb 13 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.91-1
- Update to 2.17.91

* Tue Jan 23 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.90-1
- Update to 2.17.90

* Wed Dec 19 2006 Matthias Clasen <mclasen@redhat.com> - 2.17.4-1
- Update to 2.17.4

* Tue Dec  5 2006 Matthias Clasen <mclasen@redhat.com> - 2.17.3-1
- Update to 2.17.3
- Remove obsolete patch

* Mon Nov 27 2006 Ray Strode <rstrode@redhat.com> - 2.17.2.1-2.fc7
- fix screensaver from going blank even when configured to show
  a screensaver (bug 216045)

* Sat Oct 21 2006 Matthias Clasen <mclasen@redhat.com> - 2.17.2.1-1
- Update to 2.17.2.1

* Wed Oct  4 2006 Matthias Clasen <mclasen@redhat.com> - 2.16.0-3
- Don't install a broken symlink (#208399)

* Fri Sep 15 2006 Matthias Clasen <mclasen@redhat.com> - 2.16.0-2.fc6
- Make the tray icon re-embed into the tray after a panel crash

* Sun Sep  3 2006 Matthias Clasen <mclasen@redhat.com> - 2.16.0-1.fc6
- Update to 2.16.0

* Sun Aug 27 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.92-2.fc6
- Wire up preferences in gnome-power-preferences (#203949)
- Add BR for perl-XML-Parser

* Sun Aug 20 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.92-1.fc6
- Update to 2.15.92

* Tue Aug 15 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.91-2.fc6
- Fix a double free in the smartcart code

* Sun Aug 13 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.91-1.fc6
- Update to 2.15.91

* Tue Aug  8 2006 Peter Jones <pjones@redhat.com> - 2.15.4-3
- Don't beep by default, since there's no UI to turn it off.

* Tue Jul 18 2006 Ray Strode <rstrode@redhat.com> - 2.15.3-2
- explicitly disable policykit since we don't ship it

* Tue Jun 13 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.3-1
- Update to 2.15.3

* Fri Jun  9 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.2-3
- Drop unfounded gnome-mime-data dependency
- Add missing BuildRequires

* Mon May 22 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.2-2
- Rebuild

* Mon May 15 2006 John (J5) Palmieri <johnp@redhat.com> - 2.15.2-1
- Update to upstream version 2.15.2

* Mon May 15 2006 John (J5) Palmieri <johnp@redhat.com> - 2.15.1-3
- Add BR for desktop-file-utils

* Mon May 15 2006 John (J5) Palmieri <johnp@redhat.com> - 2.15.1-1.1
- bump and rebuild

* Tue Apr 25 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.1-1
- Update to 2.15.1

* Fri Apr  7 2006 Ray Strode <rstrode@redhat.com> - 2.15.0-1
- update to 2.15.0 to get the cool new runtime analysis
  graphs.

* Mon Mar 27 2006 Ray Strode <rstrode@redhat.com> - 2.14.0-2
- use blank screensaver when lid is closed instead of
  of turning off screensaver completly (bug 186849).

* Tue Mar 14 2006 Ray Strode <rstrode@redhat.com> - 2.14.0-1
- Update to 2.14.0

* Mon Mar  6 2006 Ray Strode <rstrode@redhat.com> - 2.13.93-4
- fix the fix in -2 and -3

* Mon Mar  6 2006 Ray Strode <rstrode@redhat.com> - 2.13.93-3
- fix the fix in -2

* Mon Mar  6 2006 Ray Strode <rstrode@redhat.com> - 2.13.93-2
- fix icon in bubbles (bug 184192). 

* Fri Mar  3 2006 Ray Strode <rstrode@redhat.com> - 2.13.93-1
- Update to 2.13.93
- ignore d-bus timeout errors

* Thu Mar  2 2006 Ray Strode <rstrode@redhat.com> - 2.13.92-3
- Add patch from Richard Hughes to potentially fix a
  crasher bug (bug 183127)

* Tue Feb 28 2006 Karsten Hopp <karsten@redhat.de> 2.13.92-2
- Buildrequires: gnome-doc-utils

* Sun Feb 26 2006 Ray Strode <rstrode@redhat.com> - 2.13.92-1
- Update to 2.13.92

* Tue Feb 21 2006 Matthias Clasen <mclasen@redhat.com> - 2.13.91-1
- Update to 2.13.91
- Drop upstreamed patch

* Wed Feb 15 2006 Matthias Clasen <mclasen@redhat.com> - 2.13.90-1
- Update to 2.13.90
- Require dbus-x11 (#176656)

* Sun Feb 13 2006 Ray Strode <rstrode@redhat.com> - 2.13.5.0.20060207-2
- remove Hibernate and Suspend from menus as part of
  panel/g-p-m integration effort

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.13.5.0.20060207-1.1
- bump again for double-long bug on ppc(64)

* Tue Feb  7 2006 Ray Strode <rstrode@redhat.com> - 2.13.5.0.20060207-1
- pull cvs snapshot from HEAD and drop the patches caillon
  just added

* Tue Feb  7 2006 Christopher Aillon <caillon@redhat.com> - 2.13.5-3
- Install into the autostart directory
- Don't suspend on lid close while on AC power

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.13.5-2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan 31 2006 Matthias Clasen <mclasen@redhat.com> - 2.13.5-2
- rebuild 

* Thu Jan 26 2006 Ray Strode <rstrode@redhat.com> - 2.13.5-1
- packaging tweaks

* Thu Jan 26 2006 Christopher Aillon <caillon@redhat.com> 2.13.5-1
- Update to 2.13.5

* Tue Jan 24 2006 Christopher Aillon <caillon@redhat.com> - 0.3.4-2
- Left clicking on the applet should bring up the menu

* Tue Jan 17 2006 Ray Strode <rstrode@redhat.com> - 0.3.4-1
- update to 0.3.4
- disable updating scrollkeeper database in buildroot
  (move to %%post)

* Fri Jan  6 2006 Jeremy Katz <katzj@redhat.com> - 0.3.3-0.cvs.20060106
- update to a cvs snap so that it works with hal cvs snap
- make sure we use libnotify

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com> - 0.3.1-2.1
- rebuilt

* Thu Dec 01 2005 John (J5) Palmieri <johnp@redhat.com> - 0.3.1-2
- rebuild for new dbus

* Mon Nov 28 2005 Christopher Aillon <caillon@redhat.com> 0.3.1-1
- Update to 0.3.1

* Fri Nov 25 2005 Christopher Aillon <caillon@redhat.com> 0.3.0-1
- Update to 0.3.0

* Wed Oct 19 2005 Ray Strode <rstrode@redhat.com> 0.2.8-1
- update to 0.2.8

* Wed Oct  3 2005 Ray Strode <rstrode@redhat.com> 0.2.6-1
- update to 0.2.6

* Wed Sep 28 2005 Ray Strode <rstrode@redhat.com> 0.2.4-1
- update to 0.2.4

* Fri Sep 02 2005 David Zeuthen <davidz@redhat.com> 0.2.3.1-1
- Initial import based on an SRPM from Richard Hughes
