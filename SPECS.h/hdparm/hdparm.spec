Summary: A utility for displaying and/or setting hard disk parameters
Summary(zh_CN.UTF-8): 显示或设置硬盘参数的工具
Name: hdparm
Version: 9.39
Release: 2%{?dist}
License: BSD
Group: Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
URL:    http://sourceforge.net/projects/hdparm/
Source: http://download.sourceforge.net/hdparm/hdparm-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
ExcludeArch: s390 s390x

%description
Hdparm is a useful system utility for setting (E)IDE hard drive
parameters.  For example, hdparm can be used to tweak hard drive
performance and to spin down hard drives for power conservation.

%description -l zh_CN.UTF-8
显示或设置硬盘参数的工具，支持 (E)IDE 硬盘。

%prep
%setup -q

%build
CFLAGS="$RPM_OPT_FLAGS" make %{?_smp_mflags} STRIP=/bin/true LDFLAGS=

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_sbindir}
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man8
install -c -m 755 hdparm $RPM_BUILD_ROOT%{_sbindir}/hdparm
install -c -m 644 hdparm.8 $RPM_BUILD_ROOT/%{_mandir}/man8

magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc hdparm.lsm Changelog LICENSE.TXT README.acoustic TODO
%{_sbindir}/hdparm
%{_mandir}/man8/hdparm.8*

%changelog
* Tue Apr 15 2014 Liu Di <liudidi@gmail.com> - 9.39-2
- 更新到 9.43

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 9.39-2
- 为 Magic 3.0 重建

* Fri Feb 03 2012 Karsten Hopp <karsten@redhat.com> 9.39-1
- hdparm-9.39

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.36-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.36-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 24 2011 Karsten Hopp <karsten@redhat.com> 9.36-1
- update to hdparm-9.36 (#645048)

* Thu Oct 07 2010 Karsten Hopp <karsten@redhat.com> 9.33-1
- update to hdparm-9.33 (#592896)

* Fri Dec 11 2009 Karsten Hopp <karsten@redhat.com> 9.27-1
- update to 9.27
- enhance security-erase timeout to 12h (#536731)

* Thu Aug 20 2009 Ville Skyttä <ville.skytta@iki.fi> - 9.16-3
- Let rpmbuild strip the executable (#513025).

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 17 2009 Karsten Hopp <karsten@redhat.com> 9.16-1
- update to 9.16, fixes disk spindowns

* Wed Mar 04 2009 Karsten Hopp <karsten@redhat.com> 9.12-1
- update to 9.12 to fix #488560

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jan 14 2009 Karsten Hopp <karsten@redhat.com> 9.8-1
- update

* Wed Mar 05 2008 Karsten Hopp <karsten@redhat.com> 8.6-1
- update to 8.6
- fix source URL

* Mon Feb 25 2008 Karsten Hopp <karsten@redhat.com> 8.5-1
- version 8.5, fixes u8->u16 bug in security commands

* Mon Feb 25 2008 Karsten Hopp <karsten@redhat.com> 8.4-2
- fix debuginfo package (#434644)

* Wed Feb 20 2008 Karsten Hopp <karsten@redhat.com> 8.4-1
- version 8.4

* Tue Feb 19 2008 Karsten Hopp <karsten@redhat.com> 8.1-3
- upload 8.1 sources and rebuild

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 8.1-2
- Autorebuild for GCC 4.3

* Mon Feb 18 2008 Karsten Hopp <karsten@redhat.com> 8.1-1
- update to 8.1

* Fri Aug 24 2007 Karsten Hopp <karsten@redhat.com> 7.7-1
- update to 7.7

* Tue Jul 10 2007 Karsten Hopp <karsten@redhat.com> 7.6-1
- update to version 7.6

* Fri Feb 09 2007 Karsten Hopp <karsten@redhat.com> 6.9-3
- more review cleanups (#225882)

* Mon Feb 05 2007 Karsten Hopp <karsten@redhat.com> 6.9-2
- clean up spec file for merge review (#225882)

* Thu Jan 18 2007 Karsten Hopp <karsten@redhat.com> 6.9-1
- update to 6.9

* Mon Jul 17 2006 Karsten Hopp <karsten@redhat.de> 6.6-2
- test builds on ia64, ppc, ppc64

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 6.6-1.1
- rebuild

* Mon May 22 2006 Karsten Hopp <karsten@redhat.de> 6.3-3
- remove obsolute include patch
- disable idestruct patch, rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 6.3-2.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 6.3-2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Dec 20 2005 Karsten Hopp <karsten@redhat.de> 6.3-2
- use ExcludeArch, this allows building on archs we don't
  ship such as Alpha (#175919)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Nov 30 2005 Karsten Hopp <karsten@redhat.de> 6.3-1
- fix package URL

* Tue Oct 25 2005 Karsten Hopp <karsten@redhat.de> 6.3-1
- update to hdparm-6.3

* Wed Jun 08 2005 Karsten Hopp <karsten@redhat.de> 6.1-1
- update to 6.1 (BLKGETSIZE fixes)
- work around hdparm's usage of kernel headers, assume
  that we run it on little-endian machines only

* Wed May 18 2005 Karsten Hopp <karsten@redhat.de> 5.9-3
- remove /etc/sysconfig/harddisks (#157673)

* Tue May 10 2005 Karsten Hopp <karsten@redhat.de> 5.9-2
- enable debuginfo

* Wed Mar 02 2005 Karsten Hopp <karsten@redhat.de> 5.9-1
- update to 5.9
- build with gcc-4

* Mon Jan 03 2005 Karsten Hopp <karsten@redhat.de> 5.8-2 
- add --help option (#143916)

* Fri Nov 26 2004 Karsten Hopp <karsten@redhat.de> 5.8-1 
- update

* Tue Sep 21 2004 Than Ngo <than@redhat.com> 5.7-2
- rebuilt

* Mon Sep 06 2004 Karsten Hopp <karsten@redhat.de> 5.7-1 
- update to latest stable version

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Feb 19 2004 Karsten Hopp <karsten@redhat.de> 5.5-1 
- update to latest stable version
- rename variable to avoid name clash with readahead function

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 04 2003 Karsten Hopp <karsten@redhat.de> 5.4-2
- rebuild

* Wed Jun 04 2003 Karsten Hopp <karsten@redhat.de> 5.4-1
- update
- #92057

* Wed Apr 23 2003 Karsten Hopp <karsten@redhat.de> 5.3-2
- rebuild

* Wed Apr 23 2003 Karsten Hopp <karsten@redhat.de> 5.3-1
- update to 5.3
- add comment to /etc/sysconfig/harddisks

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Dec 12 2002 Tim Powers <timp@redhat.com> 5.2-3
- rebuild on all arches

* Tue Nov 19 2002 Tim Powers <timp@redhat.com>
- rebuild on all arches

* Wed Jun 26 2002 Karsten Hopp <karsten@redhat.de>
- update to 5.2 with the following fixes:
 - v5.2 compile fixes for 2.5.xx
 - v5.1 fixed segfault in "-i" on older drives
 - v5.0 lots of updates and new features
 - v4.9 fixed compile error with 2.5.xx kernels
 - v4.8 changed -Q to allow specifying queue depth
 - v4.7 added -z, -Q, -M flags; expanded parm range for -p

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Feb 22 2002 Karsten Hopp <karsten@redhat.de>
- bump version for 8.0

* Fri Feb 22 2002 Karsten Hopp <karsten@redhat.de>
- rebuild in new environment

* Wed Jan 23 2002 Karsten Hopp <karsten@redhat.de> (4.6-1)
- Update to 4.6

* Mon Oct 01 2001 Karsten Hopp <karsten@redhat.de>
- fix name of doc file  (#54137)

* Fri Jul 20 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- exclude s390,s390x

* Mon Jun 25 2001 Karsten Hopp <karsten@redhat.de>
- update to version 4.1
- update URL

* Wed Jul 19 2000 Bernhard Rosenkränzer <bero@redhat.com>
- disable readahead (#14268)
- add comment in /etc/sysconfig/harddisks about possible extra parameters

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Wed Jul 12 2000 Trond Eivind Glomsrød <teg@redhat.com>
- disable 32 bit interfacing (#13730)

* Tue Jun 27 2000 Trond Eivind Glomsrød <teg@redhat.com>
- use %%{_tmppath}
- add /etc/sysconfig/harddisks, a new file for hardisk 
  optimization parameters

* Mon Jun 18 2000 Bernhard Rosenkränzer <bero@redhat.com>
- FHSify

* Sun Apr  9 2000 Bernhard Rosenkränzer <bero@redhat.com>
- Fix compilation with kernel 2.3.*

* Thu Feb 17 2000 Bernhard Rosenkränzer <bero@redhat.com>
- 3.9
- handle RPM_OPT_FLAGS

* Thu Feb 17 2000 Bernhard Rosenkränzer <bero@redhat.com>
- Use O_NONBLOCK when opening devices so we can manipulate CD-ROM drives
  with no media inserted, even when running a current kernel (Bug #6457)

* Sat Feb  5 2000 Bill Nottingham <notting@redhat.com>
- build as non-root user (#6458)

* Fri Feb  4 2000 Bernhard Rosenkränzer <bero@redhat.com>
- deal with RPM compressing man pages

* Fri Nov 19 1999 Bernhard Rosenkraenzer <bero@redhat.com>
- 3.6

* Thu Aug 12 1999 Cristian Gafton <gafton@redhat.com>
- version 3.5

* Wed Mar 24 1999 Cristian Gafton <gafton@redhat.com>
- added patches from UP

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 4)

* Tue Dec 29 1998 Cristian Gafton <gafton@redhat.com>
- build for 6.0

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed Apr 08 1998 Erik Troan <ewt@redhat.com>
- updated to 3.3
- build rooted

* Fri Oct 31 1997 Donnie Barnes <djb@redhat.com>
- fixed spelling error in summary

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc

