%define gtk3_version           2.99.3
%define dbus_version           0.90
%define dbus_glib_version      0.74
%define redhat_menus_version   5.0.1
%define gnome_desktop3_version 3.1.91
%define libgnomekbd_version    2.91.1

Summary: GNOME Screensaver
Summary(zh_CN.UTF-8): GNOME 屏幕保护
Name: gnome-screensaver
Version: 3.6.1
Release: 7%{?dist}
License: GPLv2+
Group: Amusements/Graphics
Group(zh_CN.UTF-8): 娱乐/图像
#VCS: git:git://git.gnome.org/gnome-screensaver
%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
Source0: http://download.gnome.org/sources/gnome-screensaver/3.6/%{name}-%{version}.tar.xz
Source1: gnome-screensaver-hide-xscreensaver.menu

URL: http://www.gnome.org
BuildRequires: gtk3-devel => %{gtk3_version}
BuildRequires: dbus-devel >= %{dbus_version}
BuildRequires: dbus-glib-devel >= %{dbus_glib_version}
BuildRequires: gnome-desktop3-devel >= %{gnome_desktop3_version}
BuildRequires: pam-devel
BuildRequires: nss-devel
BuildRequires: libX11-devel, libXScrnSaver-devel, libXext-devel
BuildRequires: libXinerama-devel libXmu-devel
BuildRequires: libgnomekbd-devel >= %{libgnomekbd_version}
# this is here because the configure tests look for protocol headers
BuildRequires: xorg-x11-proto-devel
BuildRequires: gettext
BuildRequires: automake, autoconf, libtool, intltool, gnome-common
BuildRequires: libXxf86misc-devel
BuildRequires: libXxf86vm-devel
BuildRequires: libXtst-devel
BuildRequires: desktop-file-utils
BuildRequires: gsettings-desktop-schemas >= 0.1.7
BuildRequires: systemd-devel

Requires: gsettings-desktop-schemas >= 0.1.7
Requires: magic-menus >= %{redhat_menus_version}
# since we use it, and pam spams the log if a module is missing
Requires: gnome-keyring-pam
Conflicts: xscreensaver < 1:5.00-19

# I have no idea why this is required, but for now, just get things to build
BuildRequires:  libxklavier-devel

%description
gnome-screensaver is a screen saver and locker that aims to have
simple, sane, secure defaults and be well integrated with the desktop.

%description -l zh_CN.UTF-8
GNOME 的屏幕保护程序。

%prep
%setup -q

autoreconf -f -i

%build
%configure --with-mit-ext=no --enable-systemd
make

%install
make install DESTDIR=$RPM_BUILD_ROOT
magic_rpm_clean.sh
%find_lang %{name}

%files -f %{name}.lang
%doc AUTHORS NEWS README COPYING
%{_bindir}/*
%{_libexecdir}/*
%{_sysconfdir}/pam.d/*
%{_sysconfdir}/xdg/autostart/gnome-screensaver.desktop
%doc %{_mandir}/man1/*.1.gz

%changelog
* Sun Nov 08 2015 Liu Di <liudidi@gmail.com> - 3.6.1-7
- 为 Magic 3.0 重建

* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 3.6.1-6
- 为 Magic 3.0 重建

* Sun Apr 28 2013 Liu Di <liudidi@gmail.com> - 3.6.1-5
- 为 Magic 3.0 重建

* Wed Feb 20 2013 Kalev Lember <kalevlember@gmail.com> - 3.6.1-4
- Rebuilt for libgnome-desktop soname bump

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Dec 21 2012 Kalev Lember <kalevlember@gmail.com> - 3.6.1-2
- Rebuilt for libgnome-desktop-3 3.7.3 soname bump

* Tue Oct 16 2012 Kalev Lember <kalevlember@gmail.com> - 3.6.1-1
- Update to 3.6.1

* Tue Sep 25 2012 Matthias Clasen <mclasen@redhat.com> - 3.6.0-1
- Update to 3.6.0

* Tue Aug 07 2012 Richard Hughes <hughsient@gmail.com> - 3.5.5-1
- Update to 3.5.5

* Fri Jul 20 2012 Richard Hughes <hughsient@gmail.com> - 3.5.4-1
- Update to 3.5.4

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 17 2012 Richard Hughes <hughsient@gmail.com> - 3.4.3-1
- Update to 3.4.3

* Tue Jun 26 2012 Richard Hughes <hughsient@gmail.com> - 3.4.2-1
- Update to 3.4.2

* Fri Jun 8 2012 Matthias Clasen <mclasen@redhat.com> - 3.4.1-2
- Rebuild against new gnome-desktop

* Sat Apr 14 2012 Matthias Clasen <mclasen@redhat.com> - 3.4.1-1
- Update to 3.4.1

* Tue Mar 27 2012 Richard Hughes <hughsient@gmail.com> - 3.4.0-1
- Update to 3.4.0

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Sep 27 2011 Ray <rstrode@redhat.com> - 3.2.0-1
- Update to 3.2.0

* Tue Sep 20 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.92-1
- Update to 3.1.92

* Tue Aug 30 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.90-1
- Update to 3.1.90

* Wed Aug 17 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.5-1
- Update to 3.1.5

* Wed Aug 17 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.0-3
- Rebuild

* Fri Jun 17 2011 Tomas Bzatek <tbzatek@redhat.com> - 3.0.0-2
- Rebuilt for new gtk3 and gnome-desktop3

* Mon Apr  4 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.0-1
- Update to 3.0.0

* Mon Mar 21 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.92-1
- Update to 2.91.92
- Spec file cleanups

* Tue Mar  8 2011 Christopher Aillon <caillon@redhat.com> - 2.91.91-1
- Update to 2.91.91

* Tue Feb 22 2011 Matthias Clasen <mclasen@redhat.com>
- Update to 2.91.90

* Sun Feb 13 2011 Christopher Aillon <caillon@redhat.com> - 2.91.4-4
- Rebuild for new libxklavier

* Fri Feb 11 2011 Matthias Clasen <mclasen@redhat.com>
- Rebuild against newer gtk

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.91.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Christopher Aillon <caillon@redhat.com> 2.91.4-1
- Update to 2.91.4

* Thu Jan 13 2011 Matthias Clasen <mclasen@redhat.com> 2.91.3-2
- Drop dependency on fedora theme, we don't use it

* Sat Jan  8 2011 Matthias Clasen <mclasen@redhat.com> 2.91.3-1
- Update to 2.91.3

* Fri Dec  3 2010 Matthias Clasen <mclasen@redhat.com> 2.91.2-2
- Rebuild against new gtk

* Tue Nov 30 2010 Dan Williams <dcbw@redhat.com> 2.91.2-1
- Update to 2.91.2

* Wed Nov  3 2010 Matthias Clasen <mclasen@redhat.com>  2.91.0-2
- Rebuild against libnotify 0.7.0

* Tue Oct 19 2010 Ray Strode <rstrode@redhat.com> 2.91.0-1
- Update to latest release
- Reenable keyboard layout selector

* Tue Oct 19 2010 Ray Strode <rstrode@redhat.com> 2.30.2-5
- Temporarily build without libgnomekbd until we have a gtk3
  ready release of gnome-screensaver.

* Wed Oct 13 2010 Bastien Nocera <bnocera@redhat.com> 2.30.2-4
- Really hide xscreensaver properties from the menus when
  gnome-screensaver is installed (#530318)

* Wed Oct 06 2010 Richard Hughes <rhughes@redhat.com> 2.30.2-3
- Add BR libxklavier-devel as a workaround.

* Wed Oct 06 2010 Richard Hughes <rhughes@redhat.com> 2.30.2-2
- Rebuild against the new libgnomekbd library

* Wed Sep 29 2010 Matthias Clasen <mclasen@redhat.com> - 2.30.2-1
- Update to 2.30.2

* Wed Jun 16 2010 Matthias Clasen <mclasen@redhat.com> - 2.30.0-2
- Kill explicit library deps
- Nuke %%clean

* Tue Mar 30 2010 Matthias Clasen <mclasen@redhat.com> - 2.30.0-1
- Update to 2.30.0

* Fri Feb 12 2010 Ray Strode <rstrode@redhat.com> 2.29.91-1
- Don't lost grab when monitor is hotplugged repeatedly
  (CVE-2010-0422, #564464)
- Fix screen dirt in floaters screensavers

* Tue Feb 09 2010 Ray Strode <rstrode@redhat.com> 2.29.90-1
- Update to 2.29.90 (fixes CVE-2010-0414)

* Fri Jan 29 2010 Jon McCann <jmccann@redhat.com> 2.29.1-2
- Try again

* Fri Jan 29 2010 Jon McCann <jmccann@redhat.com> 2.29.1-1
- Update to 2.29.1

* Sun Jan 17 2010 Matthias Clasen <mclasen@redhat.com> 2.28.0-10
- Rebuild

* Fri Dec 11 2009 Matthias Clasen <mclasen@redhat.com> 2.28.0-9
- Properly handle cmdline parsing errors in popsquares (#546656)

* Thu Dec  3 2009 Matthias Clasen <mclasen@redhat.com> 2.28.0-8
- Drop an unwanted dependency

* Fri Nov  6 2009 Matthias Clasen <mclasen@redhat.com> 2.28.0-7
- Clean up session inhibitors if the owner falls off the bus
- Add an api to show messages

* Fri Oct 23 2009 Matthias Clasen <mclasen@redhat.com> 2.28.0-5
- Make the dialog ask to be killed after 5 attempts

* Fri Oct 23 2009 Matthias Clasen <mclasen@redhat.com> 2.28.0-4
- Fix crashes and malfunctions in dynamic multihead situations

* Thu Oct 22 2009 Matthias Clasen <mclasen@redhat.com> 2.28.0-3
- Fix an oversight in the previous patch

* Thu Oct 22 2009 Matthias Clasen <mclasen@redhat.com> 2.28.0-2
- Use xrandr for gamma fading, if available, to fix fading in
  multihead setups

* Wed Sep 23 2009 Matthias Clasen <mclasen@redhat.com> 2.28.0-1
- Update to 2.28.0

* Mon Aug 24 2009 Matthias Clasen <mclasen@redhat.com> 2.27.0-10
- Fix GtkBuilder conversion

* Tue Aug 18 2009 Adam Jackson <ajax@redhat.com> 2.27.0-9
- gnome-screensaver-2.27.0-gamma.patch: Backport patch to fix gamma fadeout
  (#508513)

* Sat Aug 15 2009 Matthias Clasen <mclasen@redhat.com> 2.27.0-8
- Manual XML editing considered harmful...

* Fri Aug 14 2009 Matthias Clasen <mclasen@redhat.com> 2.27.0-7
- Make the slideshow cyclic

* Fri Aug 14 2009 Matthias Clasen <mclasen@redhat.com> 2.27.0-6
- Make cosmos images available as background slideshow

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.27.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 16 2009 Matthias Clasen <mclasen@redhat.com> 2.27.0-4
- Use GtkBulider
- Respect button-images setting

* Wed Jul 15 2009 Matthias Clasen <mclasen@redhat.com> 2.27.0-3
- Rebuild against new libgnomekbd

* Wed Jul  1 2009 Matthias Clasen <mclasen@redhat.com> 2.27.0-2
- Rebuild against new libxklavier

* Fri Jun 26 2009 Bastien Nocera <bnocera@redhat.com> 2.27.0-1
- Update to 2.27.0
- Disable the text entry when using a fingerprint for auth

* Mon Apr 13 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.1-1
- Update to 2.26.1
- See http://download.gnome.org/sources/gnome-screensaver/2.26/gnome-screensaver-2.26.1.news

* Tue Apr  7 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.0-2
- Make the idle time slider work again

* Thu Mar 19 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.0-1
- Update to 2.26.0

* Thu Feb 26 2009 Adam Jackson <ajax@redhat.com> 2.25.2-6
- gnome-screensaver-2.25.2-xf86misc.patch: Don't carp about missing
  XFree86-Misc extension. (#486841)

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.25.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb 21 2009 Matthias Clasen <mclasen@redhat.com> - 2.25.2-4
- Make all hacks work again

* Fri Feb 20 2009 Matthias Clasen <mclasen@redhat.com> - 2.25.2-3
- Show menuitem in Xfce

* Thu Jan  8 2009 Matthias Clasen <mclasen@redhat.com> - 2.25.2-2
- Use better invisible char

* Wed Dec 17 2008 Matthias Clasen <mclasen@redhat.com> - 2.25.2-1
- Update to 2.25.2

* Thu Dec  4 2008 Matthias Clasen <mclasen@redhat.com> - 2.25.1-2
- Update to 2.25.1

* Mon Nov 24 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.1-2
- Update to 2.24.1

* Thu Nov 13 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.0-4
- Rebuild

* Fri Oct 10 2008 Ray Strode <rstrode@redhat.com> - 2.24.0-2
- Don't leak background pixmaps (gnome bug 555701)

* Wed Sep 24 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.0-1
- Update to 2.24.0

* Thu Aug 28 2008 Jon McCann <jmccann@redhat.com> - 2.23.90-2
- Fix patch

* Thu Aug 28 2008 Jon McCann <jmccann@redhat.com> - 2.23.90-1
- Update to 2.23.90

* Sun Jul 27 2008 Matthias Clasen  <mclasen@redhat.com> - 2.23.3-0.2008.05.29.3
- Use standard icon names

* Wed Jun  4 2008 Matthias Clasen  <mclasen@redhat.com> - 2.23.3-0.2008.05.29.2
- Rebuild

* Thu May 29 2008 Jon McCann  <jmccann@redhat.com> - 2.23.3-0.2008.05.29.1
- Update to snapshot

* Thu May 22 2008 Matthias Clasen  <mclasen@redhat.com> - 2.23.3-0.2008.05.14.2
- Fix directory ownership (#447498)

* Fri May 16 2008 Jon McCann <jmccann@redhat.com> - 2.23.3-0.2008.05.14.1
- Add frame to face image

* Wed May 14 2008 Jon McCann <jmccann@redhat.com> - 2.23.3-0.2008.05.14.0
- Update to snapshot

* Tue May 13 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.1-2
- Rebuild

* Wed Apr  2 2008 Jon McCann <jmccann@redhat.com> - 2.22.1-1
- Update to 2.22.1

* Mon Mar 31 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.0-2
- Drop gnome-vfs requires

* Mon Mar 10 2008 Jon McCann <jmccann@redhat.com> - 2.22.0-1
- Update to 2.22.0

* Wed Jan 30 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.6-1
- Update to 2.21.6

* Tue Nov 13 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.0-11
- Rebuild against newer libgnomekbd

* Mon Nov 12 2007 Dan Walsh <dwalsh@redhat.com> - 2.20.0-10
- Add pam_selinux_permit to pam config so that xguest will work properly

* Wed Oct 29 2007 Warren Togami <wtogami@redhat.com> - 2.20.0-9
- Blank screen by default in order to save power

* Wed Oct 10 2007 Ray Strode <rstrode@redhat.com> - 2.20.0-8
- Require the appropriate artwork (bug 327161)

* Fri Oct 5 2007 Ray Strode <rstrode@redhat.com> - 2.20.0-7
- fix up gamma handling, patch by John Bryant (should fix 290611)

* Fri Sep 28 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.0-6
- Use small bullets in the password entry

* Mon Sep 24 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.0-5
- Fix up GConf requires (#220547)

* Fri Sep 21 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.0-4
- Add %%pre scriptlet

* Fri Sep 21 2007 Ray Strode <rstrode@redhat.com> - 2.20.0-3
- hide xscreensaver menu if gnome-screensaver is installed
  (bug 300401)

* Thu Sep 20 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.0-2
- Make the default theme setting work 

* Mon Sep 17 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.0-1
- Update to 2.20.0

* Tue Sep  4 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.7-1
- Update to 2.19.7

* Thu Aug 23 2007 Adam Jackson <ajax@redhat.com> - 2.19.6-5
- Rebuild for build ID

* Mon Aug  6 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.6-4
- Require gnome-keyring-pam

* Fri Aug  3 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.6-3
- Update the license field

* Tue Jul 31 2007 Ray Strode <rstrode@redhat.com> - 2.19.6-2
- add the _right_ missing build requires to get fade animation back 
  (bug 247485)

* Mon Jul 30 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.6-1
- Update to 2.19.6

* Mon Jul 30 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.1.1-3
- Add optional gnome-keyring support to the gnome-screensaver pam stack

* Mon Jul  9 2007 Ray Strode <rstrode@redhat.com> - 2.19.1.1-2
- add missing build requires to get fade animation back 
  (bug 247485)

* Sun May 20 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.1.1-1
- Update to 2.19.1.1

* Fri May 18 2007 Ray Strode <rstrode@redhat.com> - 2.18.0-12
- rebuild

* Fri May 18 2007 Ray Strode <rstrode@redhat.com> - 2.18.0-11
- Yet another crack at bug 238961.

* Wed May 16 2007 Ray Strode <rstrode@redhat.com> - 2.18.0-10
- Another crack at bug 238961.

* Wed May 16 2007 Ray Strode <rstrode@redhat.com> - 2.18.0-9
- Try to workaround xrandr bug (bug 238961)

* Thu May 10 2007 Matthias Clasen <mclasen@redhat.com> - 2.18.0-8
- Drop the explicit file requires on the themed lock 
  dialog, as it is provided by system-logos anyway
  and gnome-screensaver handles its absence just fine.

* Tue Apr 10 2007 Matthias Clasen <mclasen@redhat.com> - 2.18.0-7
- Make fast-user-switching work with gdm configurations
  involving multiple X servers

* Mon Apr  2 2007 Matthias Clasen <mclasen@redhat.com> - 2.18.0-6
- Hide Power Preferences button if gnome-power-manager 
  is not installed

* Mon Apr  2 2007 Ray Strode <rstrode@redhat.com> - 2.18.0-5
- require mouse grab to lock screensaver (bug 197452)

* Mon Apr  2 2007 Matthias Clasen <mclasen@redhat.com> - 2.18.0-4
- Remove the hardwired /etc/skel/Pictures, since we are
  now using xdg-user-dirs

* Sun Apr  1 2007 Matthias Clasen <mclasen@redhat.com> - 2.18.0-3
- Fall back to HOME/Pictures if PICTURES is not set

* Fri Mar 30 2007 Matthias Clasen <mclasen@redhat.com> - 2.18.0-2
- Use the PICTURES user dir in the Pictures screensaver

* Wed Mar 14 2007 Ray Strode <rstrode@redhat.com> - 2.18.0-1
- Update to 2.18.0 (Matthias)
- rework smart card patch

* Wed Feb 28 2007 Ray Strode <rstrode@redhat.com> - 2.17.8-1
- Update to 2.17.8 (Matthias)
- Drop obsolete patches (Matthias)
- rework smart card patch

* Wed Feb 14 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.7-3
- Create ~/Pictures folder for new users, so the slideshow screensaver
  has a dropspot for screensavers

* Wed Feb 14 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.7-2
- Make the switch user button go directly to gdm

* Tue Feb 13 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.7-1
- Update to 2.17.7
- Drop upstreamed patch

* Tue Feb  6 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.6-3
- Apply a patch to improve the fast user switching experience

* Tue Feb  6 2007 David Zeuthen <davidz@redhat.com> - 2.17.6-2%{?dist} 
- Enable the "Switch User" button by default

* Tue Jan 22 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.6-1
- Update to 2.17.6

* Thu Jan 11 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.5-1
- Update to 2.17.5

* Wed Dec 20 2006 Matthias Clasen <mclasen@redhat.com> - 2.17.4-1
- Update to 2.17.4

* Tue Dec  5 2006 Matthias Clasen <mclasen@redhat.com> - 2.17.3-1
- Update to 2.17.3
- Drop upstreamed patch

* Sun Nov 12 2006 Ray Strode <rstrode@redhat.com> - 2.17.2-3
- desensitize entry instead of hiding it to prevent
  a lot of widget movement (gnome bug 272556)

* Sun Nov 12 2006 Ray Strode <rstrode@redhat.com> - 2.17.2-2
- re-enable smart card patches

* Tue Nov  7 2006 Matthias Clasen <mclasen@redhat.com> - 2.17.2-1
- Update to 2.17.2

* Thu Nov  2 2006 Ray Strode <rstrode@redhat.com> - 2.17.1-2
- temporarily revert smart card patches since they got
  broke in the switch to 2.17.1 and people can't login (bug
  212194)

* Sat Oct 21 2006 Matthias Clasen <mclasen@redhat.com> - 2.17.1-1
- Update to 2.17.1

* Mon Oct 16 2006 Ray Strode <rstrode@redhat.com> - 2.16.1-1.fc7
- Update to 2.16.1 

* Sun Oct 15 2006 Ray Strode <rstrode@redhat.com> - 2.16.0-13.fc7
- prefer smart card drivers found in system secmod db over the
  hardcoded /usr/lib/pkcs11/libcoolkeypk11.so

* Sun Oct 15 2006 Ray Strode <rstrode@redhat.com> - 2.16.0-12.fc7
- lock screen immediately if login security token was removed
  before startup (bug 210411)

* Sat Oct 14 2006 Ray Strode <rstrode@redhat.com> - 2.16.0-11.fc7
- have security token monitor helper process kill itself when 
  the communication pipe to the main process goes away (bug
  210677).

* Thu Oct 05 2006 Ray Strode <rstrode@redhat.com> - 2.16.0-10.fc6
- report token events from helper process using token name instead
  of slot id and slot series number, since slot id and slot series
  number are relative to each process (bug 208018)

* Wed Oct 04 2006 Ray Strode <rstrode@redhat.com> - 2.16.0-9.fc6
- Add more debugging messages to help diagnose bug 208018

* Sun Oct 01 2006 Ray Strode <rstrode@redhat.com> - 2.16.0-8.fc6
- handle PAM messages in a separate thread so that when a pam
  module blocks, the cancel button still works (bug 206322)
- set cursor to busy while waiting on pam module (bug 202276)
- hide prompt label/entry/unlock button until pam asks the user for input (bug 202276)
- don't assume first pam message will be "Password:" (bug 201858, 202278)

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 2.16.0-7.fc6
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Thu Sep 28 2006 Ray Strode <rstrode@redhat.com> - 2.16.0-6.fc6
- don't busy loop if the smart card even message pipe isn't ready
  (bug 208018)

* Mon Sep 18 2006 Ray Strode <rstrode@redhat.com> - 2.16.0-5.fc6
- fix problem in smart card forking code

* Mon Sep 18 2006 Ray Strode <rstrode@redhat.com> - 2.16.0-4.fc6
- fix problem in driver loading code

* Thu Sep 14 2006 Ray Strode <rstrode@redhat.com> - 2.16.0-3.fc6
- update security token patch to not poll

* Tue Sep 05 2006 Nils Philippsen <nphilipp@redhat.com> - 2.16.0-2.fc6
- remove xscreensaver migration cruft (preun script and triggers, #204944)

* Tue Sep  5 2006 Matthias Clasen <mclasen@redhat.com> - 2.16.0-1.fc6
- Update to 2.16.0
- Drop obsolete patch

* Mon Aug 21 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.7-1.fc6
- Update to 2.15.7
- Add a %%preun script

* Sun Aug 13 2006 Ray Strode <rstrode@redhat.com> - 2.15.6-1.fc6
- Update to 2.15.6
- fix up rpm group (bug 202372)

* Fri Aug  4 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.5-1.fc6
- Update to 2.15.5

* Sun Jul 23 2006 Ray Strode <rstrode@redhat.com> - 2.15.4-6
- don't listen for smart card events unless session was
  initiated after smart card authentication.
- update lock dialog UI in between individual pam messages

* Thu Jul 20 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.4-5
- Fix Requires for dbus-glib

* Wed Jul 19 2006 John (J5) Palmieri <johnp@redhat.com> - 2.15.4-4
- Add BR on dbus-glib-devel
- Add patch to fix deprecated dbus functions

* Sun Jul 16 2006 Ray Strode <rstrode@redhat.com> - 2.15.4-3
- only lock screen if screen locking is enabled and the token
  pulled out is a login token (requires uncommited changes to 
  pam_pkcs11).

* Sat Jul 15 2006 Ray Strode <rstrode@redhat.com> - 2.15.4-2
- add initial security token support (still needs work) 

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.15.4-1.1
- rebuild

* Tue Jul 11 2006 Matthias Clasen <mclasen@redhat.com> 2.15.4-1
- Update to 2.15.4
- Rename the branded screensaver to "system" and move
  it to fedora-logos

* Mon Jun 19 2006 Ray Strode <rstrode@redhat.com> 2.15.3-2
- rename widget in glade file to allow unlocking to work
  again (bug 195317)

* Tue Jun 13 2006 Matthias Clasen <mclasen@redhat.com> 2.15.3-1
- Update to 2.15.3

* Fri Jun  9 2006 Matthias Clasen <mclasen@redhat.com> 2.15.2-5
- Add missing BuildRequires

* Mon Jun  5 2006 Matthias Clasen <mclasen@redhat.com> 2.15.2-4
- Move the branded lock dialog background to fedora-logos
- Require system-logos, not fedora-logos

* Wed May 17 2006 Matthias Clasen <mclasen@redhat.com> 2.15.2-1
- Update to 2.15.2

* Fri May 12 2006 Matthias Clasen <mclasen@redhat.com> 2.15.1-2
- Fix invisible char

* Wed May 10 2006 Matthias Clasen <mclasen@redhat.com> 2.15.1-1
- Update to 2.15.1

* Tue May 2 2006 Ray Strode <rstrode@redhat.com> 2.14.1-3
- apply patch from upstream CVS to allow scrolls to unlock
  the screen (bug 189335)

* Mon Apr 10 2006 Matthias Clasen <mclasen@redhat.com> 2.14.1-2
- Update to 2.14.1
- Drop upstreamed patch

* Tue Apr  4 2006 Ray Strode <rstrode@redhat.com> 2.14.0-4
- don't ignore idle timers after long suspend
  (bug 183668)

* Thu Mar 30 2006 Ray Strode <rstrode@redhat.com> 2.14.0-3
- refresh kerberos credentials when unlocking screen 
  (bug 187341)

* Sat Mar 25 2006 Ray Strode <rstrode@redhat.com> 2.14.0-2
- Add missing "c" to the word "Screensaver" in summary
  (bug 186711).

* Mon Mar 13 2006 Matthias Clasen  <mclasen@redhat.com> 2.14.0-1
- Update to 2.14.0

* Wed Mar 01 2006 Karsten Hopp <karsten@redhat.de> 2.13.92-2
- BuildRequires: libXmu-devel

* Mon Feb 27 2006 Matthias Clasen <mclasen@redhat.com> - 2.13.92-1
- Update to 2.13.92

* Wed Feb 15 2006 Matthias Clasen <mclasen@redhat.com> - 2.13.91-1
- Update to 2.13.91

* Mon Feb 13 2006 Ray Strode <rstrode@redhat.com> - 2.13.90-4
- migrate xscreensaver screensavers in %%post as well as the
  triggers already there (bug 180984)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.13.90-3.1
- bump again for double-long bug on ppc(64)

* Fri Feb 10 2006 Ray Strode <rstrode@redhat.com> - 2.13.90-3
- take some more measures to cut cpu usage down

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.13.90-2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan 31 2006 Ray Strode <rstrode@redhat.com> - 2.13.90-2
- try to migrate xscreensaver screensavers (bug 172715)

* Mon Jan 30 2006 Matthias Clasen <mclasen@redhat.com> - 2.13.90-1
- Update to 2.13.90

* Sun Jan 22 2006 Ray Strode <rstrode@redhat.com> - 2.13.5-4
- throttle cpu usage in floaters screensaver to allow things
  like background compiles to be faster (bug 178496).

* Thu Jan 19 2006 Matthias Clasen <mclasen@redhat.com> - 2.13.5-3
- Slight improvements to the Fedora lock dialog

* Tue Jan 17 2006 Matthias Clasen <mclasen@redhat.com> - 2.13.5-1
- Update to 2.13.5

* Fri Jan 13 2006 Matthias Clasen <mclasen@redhat.com> - 0.0.24-1
- Update to 0.0.24

* Mon Jan 9 2006 Ray Strode <rstrode@redhat.com> - 0.0.23-4
- don't include .desktop part of theme name in gconf schema

* Tue Dec 20 2005 Ray Strode <rstrode@redhat.com> - 0.0.23-3
- use fedora floater screensaver by default (bug 176229)

* Tue Dec 20 2005 Ray Strode <rstrode@redhat.com> - 0.0.23-2
- install the right theme file instead of a tarball

* Tue Dec 20 2005 Ray Strode <rstrode@redhat.com> - 0.0.23-1
- Update to 0.0.23
- remove floaters screensaver engine patch (it's upstreamed)
- keep fedora branded parts

* Mon Dec 19 2005 Matthias Clasen <mclasen@redhat.com> - 0.0.22-3
- add floaters lock dialog

* Sun Dec 18 2005 Ray Strode <rstrode@redhat.com> - 0.0.22-2
- add floaters screensaver

* Thu Dec 15 2005 Matthias Clasen <mclasen@redhat.com> - 0.0.22-1
- Update to 0.0.22

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com> - 0.0.20-2.1
- rebuilt

* Thu Dec 01 2005 John (J5) Palmieri <johnp@redhat.com> - 0.0.20-2
- rebuild for new dbus

* Mon Nov 21 2005 Ray Strode <rstrode@redhat.com> 0.0.20-1
- upgrade to 0.0.20

* Thu Nov 10 2005 Ray Strode <rstrode@redhat.com> 0.0.18-2
- make screensaver background window override redirect (bug 172889). 

* Thu Nov  3 2005 Ray Strode <rstrode@redhat.com> 0.0.18-1
- Update to 0.0.18

* Tue Nov  1 2005 Matthias Clasen <mclasen@redhat.com> 0.0.17-4
- Use /proc/interrupts

* Tue Nov  1 2005 Matthias Clasen <mclasen@redhat.com> 0.0.17-2
- Switch requires to modular X

* Tue Oct 25 2005 Matthias Clasen <mclasen@redhat.com> 0.0.17-1
- Update to 0.0.17

* Sun Oct 16 2005 Matthias Clasen <mclasen@redhat.com> 0.0.16-1
- Update to 0.0.16

* Fri Oct 14 2005 Matthias Clasen <mclasen@redhat.com> 0.0.15-2
- Don't use pam_stack (#170703)

* Thu Oct  6 2005 Matthias Clasen <mclasen@redhat.com> 0.0.15-1
- Update to 0.0.15

* Thu Sep 29 2005 Matthias Clasen <mclasen@redhat.com> 0.0.14-1
- Update to 0.0.14
- Drop upstreamed patches

* Tue Sep 27 2005 Ray Strode <rstrode@redhat.com> 0.0.13-5
- Location to copy .menu file changed to preferences-post-merged.

* Mon Sep 26 2005 Ray Strode <rstrode@redhat.com> 0.0.13-4
- Copy .menu file to hide xscreensaver from menus (bug 169108).

* Fri Sep 23 2005 Ray Strode <rstrode@redhat.com> 0.0.13-3
- We don't want the xscreensaver virtual provides
- Don't use /proc/interrupts

* Thu Sep 22 2005 Matthias Clasen <mclasen@redhat.com> 0.0.13-2
- Explicitly specify xscreensaver directories
- Turn off fast user switching for now

* Wed Sep 21 2005 Ray Strode  <rstrode@redhat.com> 0.0.13-1
- Update to 0.0.13

* Fri Sep 13 2005 David Zeuthen <davidz@redhat.com> 0.0.8-1
- Initial package 



