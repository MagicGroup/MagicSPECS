Name: setuptool
Version: 1.19.11
Release: 8%{?dist}
Summary: A text mode system configuration tool
Summary(zh_CN.UTF-8): 文本模式的系统配置工具
License: GPLv2+
Group: Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
Url: http://git.fedorahosted.org/git/?p=setuptool.git
Source: setuptool-%{version}.tar.gz
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires: newt-devel, gettext, perl-XML-Parser, glib2-devel, intltool
Requires: usermode

%description
Setuptool is a user-friendly text mode menu utility which allows you
to access all of the text mode configuration programs included in the
operating system distribution.

%description -l zh_CN.UTF-8
文本模式的系统配置工具。

%prep
%setup -q 

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
magic_rpm_clean.sh
%find_lang setup

%clean
rm -rf $RPM_BUILD_ROOT

%files -f setup.lang
%defattr(-,root,root,-)
%doc README COPYING
%{_bindir}/setup
%config(noreplace) %{_sysconfdir}/pam.d/setup
%config(noreplace) %{_sysconfdir}/security/console.apps/setup
%{_sbindir}/setup
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/setuptool.d
%dir %{_sysconfdir}/setuptool.d
%config(noreplace) %{_sysconfdir}/setuptool.d/*
%{_mandir}/man1/setup.1.gz

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 1.19.11-8
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 1.19.11-7
- 为 Magic 3.0 重建

* Sat Sep 26 2015 Liu Di <liudidi@gmail.com> - 1.19.11-6
- 为 Magic 3.0 重建

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 1.19.11-5
- 为 Magic 3.0 重建

* Mon Feb 06 2012 Liu Di <liudidi@gmail.com> - 1.19.11-4
- 为 Magic 3.0 重建

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.19.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 29 2010 jkeating - 1.19.11-2
- Rebuilt for gcc bug 634757

* Wed Sep 22 2010 Michal Hlavinka <mhlavink@redhat.com> 1.19.11-1
- update translations

* Wed May 19 2010 Michal Hlavinka <mhlavink@redhat.com> 1.19.10-2
- install man page

* Wed Apr 07 2010 Michal Hlavinka <mhlavink@redhat.com> 1.19.10-1
- update translations

* Mon Nov 02 2009 Michal Hlavinka <mhlavink@redhat.com> 1.19.9-2
- spec cleanup

* Tue Oct 21 2009 Michal Hlavinka <mhlavink@redhat.com> 1.19.9-1
- update path of firewall configuration tool (#529794)
- update translations

* Mon Oct 12 2009 Michal Hlavinka <mhlavink@redhat.com> 1.19.8-1
- add setup.1 man page
- update translations

* Mon Sep 14 2009 Michal Hlavinka <mhlavink@redhat.com> - 1.19.7-1
- relase with updated translations

* Tue Aug 04 2009 Michal Hlavinka <mhlavink@redhat.com> - 1.19.6-1
- updated to 1.19.6
- don't display *_IN locale in /dev/tty/X it does not work (#511193)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.19.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Mar 09 2009 Michal Hlavinka <mhlavink@redhat.com> - 1.19.5-2
- fix buildrequires

* Mon Mar 09 2009 Michal Hlavinka <mhlavink@redhat.com> - 1.19.5-1
- new version (only translations updated)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.19.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.19.4-2
- Autorebuild for GCC 4.3

* Wed Jan 23 2008 Nalin Dahyabhai <nalin@redhat.com> 1.19.4-1
- drop system-config-printer-tui from the list of things we search for as
  an option for printer configuration (#377401)

* Mon Jan  7 2008 Nalin Dahyabhai <nalin@redhat.com> 1.19.3-2
- own $(pkgdatadir) (#427813)

* Thu Aug 16 2007 Nalin Dahyabhai <nalin@redhat.com> 1.19.3-1
- packaging cleanups
- add the ability to scan for pointers in $(pkgdatadir)/setuptool.d

* Fri Dec  1 2006 Nalin Dahyabhai <nalin@redhat.com> 1.19.2-2
- rebuild

* Thu Nov 30 2006 Nalin Dahyabhai <nalin@redhat.com> 1.19.2-1
- update more translations (#216494)

* Thu Nov 30 2006 Nalin Dahyabhai <nalin@redhat.com> 1.19.1-2
- rebuild

* Thu Nov 30 2006 Nalin Dahyabhai <nalin@redhat.com> 1.19.1-1
- update translations (#216494)

* Wed Oct 18 2006 Nalin Dahyabhai <nalin@redhat.com> 1.19-2
- rebuild

* Tue Oct 17 2006 Nalin Dahyabhai <nalin@redhat.com> 1.19-1
- fix crashers in cases when we find no configuration files (or malformed or
  useless ones) under %%{_sysconfdir}/setuptool.d (#211084)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.18.1-1.2.1
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.18.1-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.18.1-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Sun Jan 29 2006 Nalin Dahyabhai <nalin@redhat.com> 1.18.1-1
- add missing dependency on usermode (#179230)

* Wed Jan 18 2006 Nalin Dahyabhai <nalin@redhat.com> 1.18-1
- fix sorting of multiple options so that precedence is determined
  correctly (#178022)
- prefer authconfig-tui to authconfig, because if we have both, then
  authconfig is just a command-line app  (#178022)
- actually include the README

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Oct 10 2005 Nalin Dahyabhai <nalin@redhat.com> 1.17.3-1
- update PAM configuration to use "include" directive (#170265)
- conflict with versions of the pam package (< 0.78) which don't
  support the "include" directive

* Mon Oct  3 2005 Nalin Dahyabhai <nalin@redhat.com> 1.17.2-1
- clean up a compiler warning
- add a new config file so that the system-config-authentication-tui
  shows up in the menu now that it's been moved

* Wed Mar 16 2005 Nalin Dahyabhai <nalin@redhat.com> 1.17.1-1
- add a short README detailing the setuptool config file format

* Fri Oct  1 2004 Nalin Dahyabhai <nalin@redhat.com> 1.17-2
- specify %%{_bindir}/setup by name now instead of with a pattern

* Fri Oct  1 2004 Nalin Dahyabhai <nalin@redhat.com> 1.17-1
- refresh translations

* Wed Sep 29 2004 Miloslav Trmac <mitr@redhat.com> - 1.16-1
- Fix crash with LANG=ko_KR.UTF-8 (#128112)
- Add missing BuildRequires (#124175, #126595)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed May  5 2004 Nalin Dahyabhai <nalin@redhat.com> 1.15-1
- prefer system-config-keyboard to kbdconfig (#122575)
- handle tools which require command-line arguments correctly

* Tue Apr 13 2004 Nalin Dahyabhai <nalin@redhat.com> 1.14-1
- use control files to find things so that the source needn't be
  revised so often
- determine available translations at build-time (#102082)

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com> 1.13-2.1
- rebuilt
  
* Sat Jul 12 2003 Nalin Dahyabhai <nalin@redhat.com> 1.13-2
- rebuild

* Sat Jul 12 2003 Nalin Dahyabhai <nalin@redhat.com> 1.13-1
- call bindtextdomain and textdomain with the right values (#74059)

* Wed Feb 19 2003 Nalin Dahyabhai <nalin@redhat.com> 1.12-1
- setup complains if we're not root, set FALLBACK=false in the userhelper config

* Mon Jan 27 2003 Nalin Dahyabhai <nalin@redhat.com> 1.11-2
- rebuild

* Mon Nov 11 2002 Bill Nottingham <notting@redhat.com> 1.11-1
- kill hardcoded paths from pam config file

* Tue Sep  3 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.10-1
- Update translations

* Thu Aug 15 2002 Bill Nottingham <notting@redhat.com> 1.9-2
- build against new slang

* Wed Jul 24 2002 Nalin Dahyabhai <nalin@redhat.com> 1.9-1
- nuke the .desktop file
- add usermode bits

* Wed Jul 24 2002 Nalin Dahyabhai <nalin@redhat.com> 1.9-1
- intltoolize, use desktop-file-install, autotools full pull

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 16 2002 Nalin Dahyabhai <nalin@redhat.com> 1.8-3
- rebuild in new environment

* Mon Aug  6 2001 Nalin Dahyabhai <nalin@redhat.com>
- add buildrequires on newt-devel (#49696)

* Sun Aug  5 2001 Nalin Dahyabhai <nalin@redhat.com>
- add printconf-tui for printer configuration

* Fri Feb 23 2001 Trond Eivind Glomsrød <teg@redhat.com>
- langify

* Wed Jan 24 2001 Nalin Dahyabhai <nalin@redhat.com>
- add lokkit for firewall configuration (#24854)

* Tue Jan 16 2001 Nalin Dahyabhai <nalin@redhat.com>
- add netconfig (no, not netconf, and not netcfg, netconfig) (#23444)

* Wed Dec 20 2000 Bill Nottingham <notting@redhat.com>
- ship the translations (oops)

* Thu Aug 24 2000 Erik Troan <ewt@redhat.com>
- updated it/es translations

* Sat Aug 19 2000 Nalin Dahyabhai <nalin@redhat.com>
- make the .desktop file root-only-readable, because only root can run
  setuptool anyway (#16575)

* Sun Aug  6 2000 Bill Nottingham <notting@redhat.com>
- don't bother running if they're not root (#15560)

* Fri Aug  4 2000 Nalin Dahyabhai <nalin@redhat.com>
- add sv translations for .desktop file (#15361)

* Wed Jul 26 2000 Matt Wilson <msw@redhat.com>
- new translations for de fr it es

* Wed Jun 28 2000 Nalin Dahyabhai <nalin@redhat.com>
- add "archive" make target
- size list box based on length of list

* Sun Jun 18 2000 Matt Wilson <msw@redhat.com>
- rebuild for next release

* Wed Feb 09 2000 Preston Brown <pbrown@redhat.com>
- wmconfig -> desktop

* Thu Feb  3 2000 Nalin Dahyabhai <nalin@redhat.com>
- rebuilt in new environment

* Mon Aug  2 1999 Matt Wilson <msw@redhat.com>
- rebuilt against newt 0.50

* Mon Apr  5 1999 Bill Nottingham <notting@redhat.com>
- strip binary

* Fri Mar 26 1999 Bill Nottingham <notting@redhat.com>
- port to C, so we can get python out of base component

* Tue Mar 16 1999 Bill Nottingham <notting@redhat.com>
- add support for authconfig, remove cabaret

* Wed Nov 05 1997 Michael K. Johnson <johnsonm@redhat.com>
- initial version
