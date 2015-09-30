%global debug_package %{nil}
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           system-config-keyboard
Version:        1.4.0
Release:        2%{?dist}
Summary:        A graphical interface for modifying the keyboard
Summary(zh_CN.UTF-8): 修改键盘布局的图形界面

Group:          System Environment/Base
Group(zh_CN.UTF-8): 系统环境/基本
License:        GPLv2+
URL:            https://fedorahosted.org/system-config-keyboard/
Source0:        https://fedorahosted.org/releases/s/y/system-config-keyboard/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  desktop-file-utils
BuildRequires:  gettext
BuildRequires:  intltool

Requires:       system-config-keyboard-base = %{version}-%{release}
Requires:       usermode >= 1.36

Obsoletes:      kbdconfig
Obsoletes:      redhat-config-keyboard


%description
system-config-keyboard is a graphical user interface that allows 
the user to change the default keyboard of the system.

%description -l zh_CN.UTF-8
修改键盘布局的图形界面。

%package base
Summary:        system-config-keyboard base components
Summary(zh_CN.UTF-8): %{name} 的基本组件
Group:          System Environment/Base
Group(zh_CN.UTF-8): 系统环境/基本
License:        GPLv2+
Requires:       python
Requires:       dbus-python

%description base
Base components of system-config-keyboard.
%description base -l zh_CN.UTF-8
%{name} 的基本组件。

%prep
%setup -q

# rhbz (#1185860)
sed -i -e 's,Terminal=false,Terminal=true,g' system-config-keyboard.desktop.in

%build
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
%{make_install} PYTHON=python2
desktop-file-install --vendor system --delete-original      \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications             \
   $RPM_BUILD_ROOT%{_datadir}/applications/system-config-keyboard.desktop
magic_rpm_clean.sh
%find_lang %{name}


%clean
rm -rf $RPM_BUILD_ROOT


%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi


%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files
%{_sbindir}/system-config-keyboard
%{_bindir}/system-config-keyboard
%{_datadir}/system-config-keyboard
%attr(0755,root,root) %dir %{_datadir}/firstboot/modules
%{_datadir}/firstboot/modules/*
%attr(0644,root,root) %{_datadir}/applications/system-config-keyboard.desktop
%attr(0644,root,root) %{_datadir}/polkit-1/actions/org.fedoraproject.config.keyboard.policy
%attr(0644,root,root) %{_datadir}/icons/hicolor/48x48/apps/system-config-keyboard.png
%{_datadir}/man/man*/system-config-keyboard.*


%files base -f %{name}.lang
%doc COPYING
%{python2_sitelib}/system_config_keyboard

%changelog
* Tue Sep 29 2015 Liu Di <liudidi@gmail.com> - 1.4.0-2
- 为 Magic 3.0 重建

* Tue Sep 29 2015 Liu Di <liudidi@gmail.com> - 1.4.0-1
- 更新到 1.4.0

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 1.3.1-9
- 为 Magic 3.0 重建

* Wed Feb 22 2012 Thomas Woerner <twoerner@redhat.com> 1.3.1-8
- split out base components into base sub package (rhbz#791332)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 01 2011 Adam Jackson <ajax@redhat.com> 1.3.1-6
- Drop keyboard_backend.py and un-Require pyxf86config (#758709)

* Thu Jun 16 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 1.3.1-5
- Apply patches from itamarjp, landgraf, mschwendt to fix:
  - Needs pyhon-dbus: https://bugzilla.redhat.com/show_bug.cgi?id=708631
  - Missing OK button: https://bugzilla.redhat.com/show_bug.cgi?id=646041

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Oct 22 2010 Bill Nottingham <notting@redhat.com> - 1.3.1-3
- Drop firstboot requirement (#629456)

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 1.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon Sep 14 2009 Lubomir Rintel <lkundrak@v3.sk> 1.3.1-1
- New upstream release
- Drop upstreamed patches

* Tue Aug 18 2009 Lubomir Rintel <lkundrak@v3.sk> 1.3.0-4
- Wrong keyboard layout after install fix (#517542), Chris Lumens

* Wed Aug 05 2009 Lubomir Rintel <lkundrak@v3.sk> 1.3.0-3
- Include dracutSetupString() patch by Hans

* Mon Jul 27 2009 Lubomir Rintel <lkundrak@v3.sk> 1.3.0-2
- Disable debuginfo subpackage

* Mon Jul 27 2009 Lubomir Rintel <lkundrak@v3.sk> 1.3.0-1
- New upstream release
- Drop upstreamed patches
- Make arch-dependent
- Drop rphl dependency

* Mon Jun 22 2009 Karsten Hopp <karsten@redhat.com> 1.2.15-8.2
- ifnarch doesn't work in noarch packages, undo last change

* Thu Jun 18 2009 Karsten Hopp <karsten@redhat.com> 1.2.15-8.1
- don't require pyxf86config on s390x

* Wed Mar 04 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.2.15-8
- system-config-keyboard-1.2.15-nolayout.patch: insert a default ServerLayout
  section if none is found.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.15-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 01 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.2.15-6
- Rebuild for Python 2.6

* Wed Nov 12 2008 Lubomir Rintel <lkundrak@v3.sk> - 1.2.15-5
- Include icon in anaconda keyboard selection screen (#469165)
- Remove extension from desktop entry icon

* Thu Oct 23 2008 Chris Lumens <clumens@redhat.com> 1.2.15-4
- Fix a traceback when running under firstboot reconfig mode.

* Thu May 22 2008 Lubomir Rintel <lkundrak@v3.sk> 1.2.15-3
- Fix traceback from firstboot (#305465)

* Sat Apr 12 2008 Lubomir Kundrak <lkundrak@redhat.com> 1.2.15-2
- Fix the comment line ending

* Sat Apr 12 2008 Lubomir Kundrak <lkundrak@redhat.com> 1.2.15-1
- New upstream release
- Fix possibility to cancel in TUI (#216132)
- Use system icon set (#291261)
- Fix install places and permissions

* Sat Apr 12 2008 Lubomir Kundrak <lkundrak@redhat.com> 1.2.14-3
- Handle situations where CoreKeyboard is not present
- Fix License tag

* Sat Apr 05 2008 Lubomir Kundrak <lkundrak@redhat.com> 1.2.14-2
- Do not show in KDE and Gnome menus
- Rework specfile

* Wed Mar 26 2008 Bill Nottingham <notting@redhat.com> 1.2.14-1
- this doesn't actually require kudzu

* Fri Feb 29 2008 Chris Lumens <clumens@redhat.com> 1.2.13-1
- Fix a traceback in the firstboot module (#435416).

* Tue Feb 19 2008 Chris Lumens <clumens@redhat.com> 1.2.12-1
- Fix setting the default keyboard in anaconda (#432158).

* Tue Feb 12 2008 Lubomir Kundrak <lkundrak@redhat.com> - 1.2.11-6
- Fix a typo

* Tue Jan 22 2008 Jesse Keating <jkeating@redhat.com> - 1.2.11-4
- Patch to work with new firstboot (#424811)
- Add requires for kudzu/newt (#177301)
- Update url (#235072)
- Remove obsolete no translation (#332301)

* Thu Aug 23 2007 Pete Graner <pgraner@redhat.com> - 1.2.11-3
- Rebulid

* Tue Aug 21 2007 Pete Graner <pgraner@redhat.com> - 1.2.11-2
- Updated License tag per Fedora Licenseing Guidlines.
- Removed  --add-category X-Red-Hat-Base to fix build errors

* Tue Nov 21 2006 Paul Nasrat <pnasrat@redhat.com> - 1.2.11-1
- Update translations

* Fri Oct 13 2006 Bill Nottingham <notting@redhat.com> - 1.2.10-1
- use valid charset for translations (#210720)

* Wed Oct 04 2006 Chris Lumens <clumens@redhat.com> - 1.2.9-1
- Fix type ahead order to use displayed names (#209218).

* Mon Oct  2 2006 Jeremy Katz <katzj@redhat.com> - 1.2.8-1
- update translations

* Mon Jul 17 2006 Paul Nasrat <pnasrat@redhat.com> - 1.2.7-2
- Don't nuke *.pyc in preun (#198952)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.2.7-1.1.1
- rebuild

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Oct 20 2005 Paul Nasrat <pnasrat@redhat.com> - 1.2.7-1
- Update pam file (#170630)
- New firstboot module
- Compiled python

* Thu Sep 15 2005 Jeremy Katz <katzj@redhat.com> - 1.2.6-3
- exclude ppc64 since we don't have X stuff there

* Wed Apr 27 2005 Jeremy Katz <katzj@redhat.com> - 1.2.6-2
- silence %%post

* Fri Apr 01 2005 Paul Nasrat <pnasrat@redhat.com> - 1.2.6-1
- Translations
- Gtk deprecations

* Mon Mar 28 2005 Christopher Aillon <caillon@redhat.com>
- rebuilt

* Fri Mar 25 2005 Christopher Aillon <caillon@redhat.com> 1.2.5-2
- Update the GTK+ theme icon cache on (un)install

* Fri Oct 08 2004 Paul Nasrat <pnasrat@redhat.com> - 1.2.5-1
- Firstboot fix for xorg.conf

* Fri Oct 01 2004 Paul Nasrat <pnasrat@redhat.com> - 1.2.4-1
- Translations 

* Wed Sep 22 2004 Jeremy Katz <katzj@redhat.com> - 1.2.3-1
- fix traceback when using treeview typeahead (#133178)

* Tue Sep 07 2004 Paul Nasrat <pnasrat@redhat.com> 1.2.2-1
- i18n desktop

* Thu Apr  8 2004 Brent Fox <bfox@redhat.com> 1.2.1-2
- fix icon path (bug #120175)

* Wed Nov 12 2003 Brent Fox <bfox@redhat.com> 1.2.1-1
- renamed from redhat-config-keyboard
- add Obsoletes for redhat-config-keyboard
- make changes for Python2.3

* Mon Oct 13 2003 Brent Fox <bfox@redhat.com> 1.1.5-2
- pull in Croatian translation (bug #106617)

* Thu Aug 14 2003 Brent Fox <bfox@redhat.com> 1.1.5-1
- tag on every build

* Wed Jul  2 2003 Brent Fox <bfox@redhat.com> 1.1.3-2
- bump release and rebuild

* Wed Jul  2 2003 Brent Fox <bfox@redhat.com> 1.1.3-1
- mark string for translation

* Tue Jul  1 2003 Brent Fox <bfox@redhat.com> 1.1.2-2
- bump version and rebuild

* Tue Jul  1 2003 Brent Fox <bfox@redhat.com> 1.1.2-1
- fix formatting problem (bug #97873)
- create an XkbOption if it doesn't exist (bug #97877)

* Wed May 21 2003 Brent Fox <bfox@redhat.com> 1.1.1-2
- made a typo in redhat-config-keyboard.py

* Wed May 21 2003 Brent Fox <bfox@redhat.com> 1.1.1-1
- Created a command line interface
- updated all copyright dates

* Wed Apr  2 2003 Brent Fox <bfox@redhat.com> 1.0.5-1
- pass window size into rhpl

* Wed Mar  5 2003 Brent Fox <bfox@redhat.com> 1.0.4-1
- add functions in keyboard_gui.py for anaconda popup mode

* Wed Feb 12 2003 Jeremy Katz <katzj@redhat.com> 1.0.3-4
- fixes for tui cjk (#83518)

* Tue Feb  4 2003 Brent Fox <bfox@redhat.com> 1.0.3-3
- change packing order a little for firstboot reconfig mode

* Thu Jan 30 2003 Brent Fox <bfox@redhat.com> 1.0.3-2
- bump and build

* Wed Jan 22 2003 Brent Fox <bfox@redhat.com> 1.0.3-1
- add a us keymap to keymaps with non-latin chars (bug #82440)
- write out the XkbVariant line if it is present
- handle XkbOptions to allow toggling between keymaps

* Mon Dec 23 2002 Brent Fox <bfox@redhat.com> 1.0.2-1
- add a textdomain for rhpl so we pull in translations (bug #78831)

* Thu Dec 12 2002 Brent Fox <bfox@redhat.com> 1.0.1-9
- remove requires for pygtk2 since we have a text mode now

* Wed Dec 11 2002 Brent Fox <bfox@redhat.com> 1.0.1-8
- fall back to text mode if gui mode fails

* Tue Nov 12 2002 Brent Fox <bfox@redhat.com> 1.0.1-7
- pam path changes

* Thu Nov 07 2002 Brent Fox <bfox@redhat.com> 1.0.1-6
- Add keyboard_backend.py to cvs

* Thu Oct 31 2002 Brent Fox <bfox@redhat.com> 1.0.1-5
- Obsolete kbdconfig

* Wed Oct 09 2002 Brent Fox <bfox@redhat.com> 1.0.1-4
- Added a tui mode - keyboard_tui.py
- Moved some non-UI code to keyboard_backend.py

* Fri Oct 04 2002 Brent Fox <bfox@redhat.com> 1.0.1-3
- Add a window icon
- set selection mode to browse

* Wed Aug 28 2002 Brent Fox <bfox@redhat.com> 1.0.1-1
- Make no arch

* Wed Aug 14 2002 Brent Fox <bfox@redhat.com> 0.9.9-6
- rebuild for translations

* Tue Aug 13 2002 Brent Fox <bfox@redhat.com> 0.9.9-5
- fix textdomain so translations show up correctly

* Tue Aug 13 2002 Brent Fox <bfox@redhat.com> 0.9.9-4
- pull translations into desktop file

* Mon Aug 12 2002 Tammy Fox <tfox@redhat.com> 0.9.9-3
- Replace System with SystemSetup in desktop file categories

* Sun Aug 11 2002 Brent Fox <bfox@redhat.com> 0.9.9-2
- Fix ordering of layout and model.  Fixes bug 71067

* Thu Aug 08 2002 Brent Fox <bfox@redhat.com> 0.9.9-1
- Added Requires for pyxf86config

* Fri Aug 02 2002 Brent Fox <bfox@redhat.com> 0.9.8-1
- Make changes for new pam timestamp policy

* Thu Aug 01 2002 Brent Fox <bfox@redhat.com> 0.9.7-2
- sort the list by the full keyboard name, not the keymap

* Thu Aug 01 2002 Brent Fox <bfox@redhat.com> 0.9.7-1
- make calls to pyxf86config to update XF86Config file

* Wed Jul 24 2002 Brent Fox <bfox@redhat.com> 0.9.6-3
- fix Makefiles and spec files so that translations get installed

* Wed Jul 24 2002 Brent Fox <bfox@redhat.com> 0.9.6-2
- update spec file for public beta 2

* Tue Jul 23 2002 Brent Fox <bfox@redhat.com> 0.9.6-1
- put desktop file in correct location

* Mon Jul 22 2002 Jeremy Katz <katzj@redhat.com> 0.9.5-2
- add scrollto hack back

* Fri Jul 19 2002 Brent Fox <bfox@redhat.com> 0.9.5-1
- add version dependency for pygtk2 API change

* Thu Jul 18 2002 Jeremy Katz <katzj@redhat.com> 0.9.4-3
- add fix for list store changes in new pygtk2

* Tue Jul 16 2002 Brent Fox <bfox@redhat.com> 0.9.4-2
- bump rev num and rebuild

* Thu Jul 11 2002 Brent Fox <bfox@redhat.com> 0.9.3-2
- Update changelogs and rebuild

* Mon Jul  1 2002 Jeremy Katz <katzj@redhat.com> 0.9.3-1
- add wacky scrollto hack so that the screen in the installer scrolls properly

* Mon Jul 01 2002 Brent Fox <bfox@redhat.com> 0.9.2-1
- Bump rev number

* Mon Jul 1 2002 Brent Fox <bfox@redhat.com> 0.9.2-1
- Wrap the destroy call in a try/except because there is no self.mainWindow in firstboot reconfig mode

* Wed Jun 26 2002 Brent Fox <bfox@redhat.com> 0.9.1-1
- Fixed description

* Tue Jun 25 2002 Brent Fox <bfox@redhat.com> 0.9.0-5
- Create pot file

* Mon Jun 24 2002 Brent Fox <bfox@redhat.com> 0.9.0-4
- Fix spec file

* Fri Jun 21 2002 Brent Fox <bfox@redhat.com> 0.9.0-3
- Print init message on debug mode

* Thu Jun 20 2002 Brent Fox <bfox@redhat.com> 0.9.0-2
- Pass doDebug into launch instead of setupScreen
- Add snapsrc to Makefile

* Tue Jun 18 2002 Brent Fox <bfox@redhat.com> 0.9.0-1
- Create a way to pass keymap name back to firstboot

* Wed May 29 2002 Brent Fox <bfox@redhat.com> 0.2.0-3
- Make symbolic link in /usr/share/firstboot/modules point to keyboard_gui.py

* Tue May 28 2002 Jeremy Katz <katzj@redhat.com>
- changes to be usable within an anaconda context 

* Tue Dec 05 2001 Brent Fox <bfox@redhat.com>
- initial coding and packaging

