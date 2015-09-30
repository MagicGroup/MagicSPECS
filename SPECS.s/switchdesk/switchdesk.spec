Name: switchdesk
Summary: A desktop environment switcher
Summary(zh_CN.UTF-8): 桌面环境切换工具
Version: 4.0.10
Release: 4%{?dist}
Url: http://than.fedorapeople.org/
Source: http://than.fedorapeople.org/%{name}-%{version}.tar.bz2
License: GPLv2+
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
BuildRequires: intltool
BuildRequires: gettext
BuildRequires: python-devel
BuildRequires: desktop-file-utils

%description
The Desktop Switcher is a tool which enables users to easily switch
between various desktop environments that they have installed.

Support for different environments on different computers is available, as
well as support for setting a global default environment.

Install switchdesk if you need a tool for switching between desktop
environments.
%description -l zh_CN.UTF-8
桌面环境切换工具。

%package gui
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Summary: A graphical interface for the Desktop Switcher
Summary(zh_CN.UTF-8): 图形界面的桌面切换工具
Requires: %{name} = %{version}-%{release}
Requires: python
Requires: pygtk2

%description gui
The switchdesk-gui package provides the graphical user interface for
the Desktop Switcher.
%description gui -l zh_CN.UTF-8
图形界面的桌面切换工具。

%prep

%setup -q

%build
make %{?_smp_mflags}

%install
rm -rf %{buildroot}

make install DESTDIR=%{buildroot}

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop
install -p -m 644 %{name}.desktop %{buildroot}%{_datadir}/applications/
magic_rpm_clean.sh
%find_lang %{name}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS COPYING
%dir %{_datadir}/%{name}
%{_bindir}/%{name}*
%{_datadir}/%{name}/Xclients*
%{_mandir}/man1/%{name}*

%files gui -f %{name}.lang
%defattr(-,root,root)
%{_datadir}/%{name}/pixmaps
%{_datadir}/%{name}/*.glade
%{_datadir}/%{name}/*.py*
%{_datadir}/applications/*

%changelog
* Tue Sep 29 2015 Liu Di <liudidi@gmail.com> - 4.0.10-4
- 为 Magic 3.0 重建

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 4.0.10-3
- 为 Magic 3.0 重建

* Sat Feb 11 2012 Liu Di <liudidi@gmail.com> - 4.0.10-2
- 为 Magic 3.0 重建

* Thu Mar 17 2011 Than Ngo <than@redhat.com> - 4.0.10-1
- 4.0.10 release

* Wed Jul 07 2010 Than Ngo <than@redhat.com> - 4.0.9-8
- fixed 226443 - Merge Review

* Wed Jul 07 2010 Than Ngo <than@redhat.com> - 4.0.9-7
- fixed 226443 - Merge Review

* Wed Jul 07 2010 Than Ngo <than@redhat.com> - 4.0.9-6
- fixed 226443 - Merge Review

* Tue Sep 29 2009 Than Ngo <than@redhat.com> - 4.0.9-5
- update po files 

* Mon Aug 10 2009 Ville Skyttä <ville.skytta@iki.fi> - 4.0.9-4.3
- Convert specfile to UTF-8.

* Sat Dec 13 2008 Than Ngo <than@redhat.com> - 4.0.9-4
- fix bz447749, broken desktop file

* Mon Dec 01 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 4.0.9-3.1
- Rebuild for Python 2.6

* Wed Nov 26 2008 Than Ngo <than@redhat.com> -  4.0.9-3
- add better advice for kde install (#440670)

* Mon Mar 10 2008 Than Ngo <than@redhat.com> 4.0.9-2
- update po files

* Fri Mar 07 2008 Than Ngo <than@redhat.com> 4.0.9-1
- 4.0.9
   - remove obsolete translation (#335231)
   - fix permission of po files (#435031)
   - start fluxbox correctly (#415181)
   - start icewm correctly (#288891)
   - own /usr/share/switchdesk (#233917)

* Mon Jan 22 2007 Than Ngo <than@redhat.com> - 4.0.8-7
- fix #174513, it supports any window manager

* Thu Jun 08 2006 Than Ngo <than@redhat.com> 4.0.8-6
- fix build problem in mock #194170

* Fri May 19 2006 Than Ngo <than@redhat.com> 4.0.8-5
- add French translation, thanks to Alain PORTAL

* Thu Mar 09 2006 Than Ngo <than@redhat.com> 4.0.8-4
- fix deprecated functions in gtk

* Wed Jan 25 2006 Than Ngo <than@redhat.com> 4.0.8-3
- fix modular X problem #178840
- update po files

* Sat Dec 17 2005 Than Ngo <than@redhat.com> 4.0.8-2
- rebuilt

* Tue Nov 29 2005 Than Ngo <than@redhat.com> 4.0.8-1
- 4.0.8

* Tue Jul 19 2005 Than Ngo <than@redhat.com> 4.0.7-1
- show more infos when it fails #162751
- add correct path for fluxbox #160433

* Fri Oct 01 2004 Than Ngo <than@redhat.com> 4.0.6-3
- update translations

* Thu Sep 16 2004 Than Ngo <than@redhat.com> 4.0.6-2
- add intltool in BuildRequires #132620
- get rid of unneeded automake16 #132631

* Sun Jul 04 2004 Than Ngo <than@redhat.com> 4.0.6-1
- add new GNOME logo, bug #127182

* Mon Jun 28 2004 Than Ngo <than@redhat.com> 4.0.5-1 
- fixed wrong output when fvwm is selected #126801

* Wed May 26 2004 Than Ngo <than@redhat.com> 4.0.4-1
- fix wrong RB id of enlightenment which causes switchdesk crashed #124408
- fix bug in setting default wm, bug #124292, #122260
- fix bug in creating .Xclients, bug #123545
- add selection button for System Default #110312

* Fri Apr 30 2004 Than Ngo <than@redhat.com> 4.0.3-1
- fix a invalid syntax bug in python script #121840, #121813
- update translations

* Tue Apr 06 2004 Than Ngo <than@redhat.com> 4.0.2-1
- 4.0.2 release
- translation update
- fix #120143

* Tue Feb 03 2004 Than Ngo <than@redhat.com> 4.0.1-1
- 4.0.1 release

* Sun Feb  1 2004 Than Ngo <than@redhat.com> 4.0.0-1 
- 4.0.0 release
- fixed #40226, #71711, #71990, #72744, #75751, #78603, #81801, #84043, #85077, #89347, #105880, #108582, #109683, #110312, #114190

- Thu Jun 26 2003 Than Ngo <than@redhat.com> 3.9.8-18
- build with gcc-3.3-12
- fix desktop file issue
- cleanup specfile
- disable debuginfo

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Mike A. Harris <mharris@redhat.com> 3.9.8-15
- Remove multiple .desktop files (#72872)

* Wed Jan 22 2003 Tim Powers <timp@redhat.com> 3.9.8-14
- rebuilt

* Tue Jan 21 2003 Paul Gampe <pgampe@redhat.com> 3.9.8-13
- Ensure .po file encoding is in UTF-8 (#77813) and update translations

* Tue Jan 21 2003 Paul Gampe <pgampe@redhat.com> 3.9.8-13
- Ensure .po file encoding is in UTF-8 (#77813)

* Wed Nov 13 2002 Mike A. Harris <mharris@redhat.com> 3.9.8-12
- Removed extraneous desktop file (#81801)

* Wed Nov 13 2002 Mike A. Harris <mharris@redhat.com> 3.9.8-11
- Changed ./configure to rpm %%configure macro so libdir is set right on x86_64
- More prefix/share -> %%{_datadir} fixes, removal of {prefix}, and usage of
  {_prefix} instead
- Changed make install to %%makeinstall macro

* Wed Nov 13 2002 Mike A. Harris <mharris@redhat.com> 3.9.8-10
- Changed all occurances of {prefix}/foo to proper RPM macros and other spec
  file cleanups
- Fix for unpackaged files in buildroot detected by new rpm policy

* Sat Aug 10 2002 Elliot Lee <sopwith@redhat.com>
- rebuilt with gcc-3.2 (we hope)

* Mon Aug 05 2002 Karsten Hopp <karsten@redhat.de>
- desktop-file (#69506)
- fix wmaker (#65303)
- sync with cvs
- remove acconfig.h from CVS, it creates a config.h 
  with invalid deklarations
- fix comments in switchdesk-gnome.c
- fix CXXFLAGS in src/Makefile.am

* Tue Jul 23 2002 Tim Powers <timp@redhat.com> 3.9.8-7
- rebuild using gcc-3.2-0.1

* Fri Jul 05 2002 Karsten Hopp <karsten@redhat.de> 3.9.8-6
- fix #67326

* Wed Jun 26 2002 Karsten Hopp <karsten@redhat.de> 3.9.8-5
- fix #66791 (switchdesk doesn't list GNOME)
- use updated message catalogs fom CVS

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Apr 16 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.9.8-2
- Rebuild

* Mon Apr 15 2002 Trond Eivind Glomsrød <teg@redhat.com> 3.9.8-1
- Update translations

* Tue Aug 28 2001 Bernhard Rosenkraenzer <bero@redhat.com> 3.9.7-1
- Fix i18n (Patch from kmaraas@online.no, #52717)

* Tue Aug 28 2001 Trond Eivind Glomsrød <teg@redhat.com> 3.9.6-1
- Translation update

* Mon Mar 19 2001 Tim Powers <timp@redhat.com>
- fixed switchdesk-helper script, and cleaned up manpage so we don't
  refer to AnotherLevel etc (#31142)

* Mon Mar 12 2001 Preston Brown <pbrown@redhat.com>
- Xclients.fvwm was still missing (#31142)

* Thu Mar  8 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Remove dependency on kdesupport, we don't actually use it

* Wed Feb 28 2001 Trond Eivind Glomsrød <teg@redhat.com>
- rebuild
- add buildprereqs

* Fri Feb 16 2001 Yukihiro Nakai <ynakai@redhat.com>
- Add ja.po to Makefile.am
- enable NLS
- Change tar archive to handle bzip2 archive correctly.

* Wed Feb 14 2001 Preston Brown <pbrown@redhat.com>
- last translation update.

* Thu Jan 25 2001 Yukihiro Nakai <ynakai@redhat.com>
- Fix between selection and icon.
- Comment out the part that uses Makefile.cvs
- Version update.

* Wed Jan 24 2001 Preston Brown <pbrown@redhat.com>
- i18n for europe included.

* Fri Dec 22 2000 Yukihiro Nakai <ynakai@redhat.com>
- Gettextized
- Add Japanese resources

* Mon Dec 11 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix typo in switchdesk-helper
- Don't exclude ia64 anymore, Qt compiles by now.

* Thu Nov 16 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Handle KDE 2.0 (Bug #20371)
- Make the desktop names for the textmode frontend case insensitive
- Add Swedish translation to Desktop file (RFE #15362)
- Add German translation to Desktop file
- Fix up help text when neither switchdesk-kde nor switchdesk-gnome is
  installed
- Fix up %%description - we support WindowMaker, fvwm and twm.
- Add the missing Xclients.fvwm file

* Thu Aug 24 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Check whether the selected UI actually exists in textmode (Bug #16603)

* Wed Aug 23 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Add docs for the KDE2 switch on command line (Bug #16743)
- Fix crash in switchdesk-gnome (Bug #16743)
- fix some minor oddities

* Tue Aug 22 2000 Than Ngo <than@redhat.com>
- fix /usr/share/apps/switchdesk/Xclients.kde2 for starting KDE2 correct
 
* Sat Aug 19 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- minor fix in spec file                                                        

* Wed Aug  9 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Don't use KDE2 calls in switchdesk-kde; we're Qt only for now.

* Fri Jul 14 2000 Bill Nottingham <notting@redhat.com>
- defattr

* Thu Jul 13 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- fix up the Xclients.* scripts

* Wed Jul 12 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- add enlightenment, twm, windowmaker to gnome version, remove AnotherLevel
- fix build with current KDE 2.0
- stop using egcs++
- fix a number of bugs
- ExcludeArch ia64 for now (kdelibs doesn't compile there)

* Fri Jul  7 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- use egcs++ for now

* Wed Jun 21 2000 Preston Brown <pbrown@redhat.com>
- add enlightenment, twm, windowmaker to kde version, remove AnotherLevel

* Sun Jun 18 2000 Matt Wilson <msw@redhat.com>
- rebuild for next release
- use %%{_mandir}

* Mon May 22 2000 Bill Nottingham <notting@redhat.com>
- update autoconf stuff (ia64)

* Sun Apr  9 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Port to KDE 2.0
- some spec file tweaks

* Mon Feb 28 2000 Preston Brown <pbrown@redhat.com>
- ignore unknown desktop names

* Mon Feb 14 2000 Preston Brown <pbrown@redhat.com>
- switchdesk works from the console
- minor bugfixes and cleanups
- man page added

* Mon Oct 04 1999 Preston Brown <pbrown@redhat.com>
- make the startup script a bit more probing/robust.

* Tue Sep 14 1999 Preston Brown <pbrown@redhat.com>
- convert .kdelnk file to a system-wide .desktop file.

* Mon Apr 19 1999 Preston Brown <pbrown@redhat.com>
- added back in switchdesk.kdelnk file (kde still doesn't handle
  .desktop files)

* Tue Apr 13 1999 Preston Brown <pbrown@redhat.com>
- fix up X display string handling

* Wed Mar 24 1999 Preston Brown <pbrown@redhat.com>
- Xclients scripts installed with execute permission.

* Wed Mar 17 1999 Preston Brown <pbrown@redhat.com>
- hardcode path to pidof (/sbin) because it isn't in default path.

* Tue Mar 16 1999 Preston Brown <pbrown@redhat.com>
- converted kdelnk file to desktop file, moved location, removed KDEDIR

* Mon Mar 08 1999 Preston Brown <pbrown@redhat.com>
- broke out separate kde, gnome packages.

* Wed Feb 24 1999 Preston Brown <pbrown@redhat.com>
- new group.

* Wed Feb 03 1999 Preston Brown <pbrown@redhat.com>
- initial revision of spec file.
