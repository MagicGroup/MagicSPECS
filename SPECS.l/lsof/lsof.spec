Summary: A utility which lists open files on a Linux/UNIX system
Name: lsof
Version: 4.87
Release: 6%{?dist}
# Sendmail .. lib/snpf.c
# LGPLv2+  .. lib/regex.c, regex.h
License: zlib and Sendmail and LGPLv2+
Group: Development/Debuggers

# lsof contains licensed code that we cannot ship.  Therefore we use
# upstream2downstream.sh script to remove the code before shipping it.
#
# The script you can found in SCM or download from:
# http://pkgs.fedoraproject.org/gitweb/?p=lsof.git;a=blob_plain;f=upstream2downstream.sh

%global lsofrh lsof_%{version}-rh
URL: http://people.freebsd.org/~abe/
Source0: %{lsofrh}.tar.xz
Source1: upstream2downstream.sh

%description
Lsof stands for LiSt Open Files, and it does just that: it lists
information about files that are open by the processes running on a
UNIX system.

%prep
%setup -q -n %{lsofrh}

%build
./Configure -n linux
make DEBUG="$RPM_OPT_FLAGS" %{?_smp_mflags}

%install
mkdir -p ${RPM_BUILD_ROOT}%{_sbindir}
install -p -m 0755 lsof ${RPM_BUILD_ROOT}%{_sbindir}
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man8
install -p -m 0644 lsof.8 ${RPM_BUILD_ROOT}%{_mandir}/man8

%files
%doc 00* README.lsof_*
%{_sbindir}/lsof
%{_mandir}/man*/*

%changelog
* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 4.87-6
- 为 Magic 3.0 重建

* Thu Jul 03 2014 Liu Di <liudidi@gmail.com> - 4.87-5
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.87-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.87-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.87-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jan  3 2013 Peter Schiffer <pschiffe@redhat.com> - 4.87-1
- resolves: #891508
  updated to 4.87

* Tue Aug 28 2012 Peter Schiffer <pschiffe@redhat.com> - 4.86-4
- .spec file cleanup

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.86-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 04 2012 Peter Schiffer <pschiffe@redhat.com> - 4.86-2
- added support for files on anon_inodefs

* Fri Apr 20 2012 Peter Schiffer <pschiffe@redhat.com> - 4.86-1
- resolves: #811520
  update to 4.86

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.85-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Sep 30 2011 Peter Schiffer <pschiffe@redhat.com> - 4.85-1
- resolves: #741882
  update to 4.85

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.84-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 13 2011 Ville SkyttÃ¤ <ville.skytta@iki.fi> - 4.84-3
- Fix man page permissions.

* Wed Sep 29 2010 jkeating - 4.84-2
- Rebuilt for gcc bug 634757

* Wed Sep 15 2010 Karel Zak <kzak@redhat.com> 4.84-1
- upgrade to 4.84
- remove lsof_4.81-threads.patch, "lsof -K" provides basic support for tasks now

* Fri Feb 19 2010 Karel Zak <kzak@redhat.com> 4.83-2
- minor changes in spec file (#226108 - Merge Review)

* Thu Feb 11 2010 Karel Zak <kzak@redhat.com> 4.83-1
- upgrade to 4.83 (see the 00DIST file for list of changes)
- remove lsof_4.83A-selinux-typo.patch (fixed upstream)

* Mon Jul 27 2009 Karel Zak <kzak@redhat.com> 4.82-1
- upgrade to 4.82 (see the 00DIST file for list of changes)
- backport an upstream patch from 4.83A-linux
- remove lsof_4.81-man.patch (fixed upstream)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.81-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.81-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 30 2009 Karel Zak <kzak@redhat.com> 4.81-2
- fix #480694 - lsof manpage mismarked and formats badly

* Tue Dec  2 2008 Karel Zak <kzak@redhat.com> 4.81-1
- upgrade to 4.81
  - lsof_4.80-threads.patch - rebased

* Thu Aug  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> 4.80-2
- fix license tag

* Tue May 20 2008 Karel Zak <kzak@redhat.com> 4.80-1
- upgrade to 4.80
  - lsof_4.78C-inode.patch - merged upstream
  - lsof_4.78C-selinux.patch - merged upstream
  - lsof_4.78C-threads.patch - rebased

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 4.78-8
- Autorebuild for GCC 4.3

* Wed Oct  3 2007 Karel Zak <kzak@redhat.com> 4.78-7
- update selinux and inode patches (new versions are based on upstream)

* Tue Oct  2 2007 Karel Zak <kzak@redhat.com> 4.78-6
- fix #280651 - lsof prints entries in multiple lines when SElinux is disabled
- fix #243976 - mmap'd files with large inode numbers confuse lsof

* Thu Mar  1 2007 Karel Zak <kzak@redhat.com> 4.78-5
- fix License

* Thu Mar  1 2007 Karel Zak <kzak@redhat.com> 4.78-4
- fix #226108 - Merge Review: lsof

* Thu Aug 10 2006 Karel Zak <kzak@redhat.com> 4.78-3
- minor changes to thread patch

* Wed Aug  9 2006 Karel Zak <kzak@redhat.com> 4.78-2
- fix #184338 - allow lsof access nptl threads

* Wed Jul 19 2006 Karel Zak <kzak@redhat.com> 4.78-1
- rebuild

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 4.78-06122006devel.1.1
- rebuild

* Mon Jun 12 2006 Karel Zak <kzak@redhat.com> 4.78-06122006devel.1
- upgrade to 4.78C (last bugfix accepted by upstream)

* Mon Jun 12 2006 Karel Zak <kzak@redhat.com> 4.78-06052006devel.2
- added BuildRequires libselinux-devel
- fix #194864 - lsof segfaults on starting

* Wed May 24 2006 Karel Zak <kzak@redhat.com> 4.78-06052006devel.1
- upgrade to 4.78B (upstream devel version with selinux patch)

* Wed Feb 15 2006 Karel Zak <kzak@redhat.com> 4.76-2
- fix #175568 - lsof prints 'unknown inode type' for epoll

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 4.76-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 4.76-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Sep 19 2005 Karel Zak <kzak@redhat.com> 4.76-1
- new upstream version

* Tue May 10 2005 Karel Zak <kzak@redhat.com> 4.74-7
- fix debuginfo

* Wed Mar 23 2005 Karel Zak <kzak@redhat.com> 4.74-6
- fix "lsof -b" hangs if a process is stuck in disk-wait/NFS (#131712)

* Mon Mar 14 2005 Karel Zak <kzak@redhat.com> 4.74-5
- src.rpm cleanup

* Sat Mar  5 2005 Karel Zak <kzak@redhat.com> 4.74-3
- rebuilt

* Tue Feb  8 2005 Karel Zak <kzak@redhat.com> 4.74-2
- replace 'Copyright' with 'License' in .spec

* Tue Feb  8 2005 Karel Zak <kzak@redhat.com> 4.74-1
- sync with upstream 4.74

* Mon Dec 13 2004 Karel Zak <kzak@redhat.com> 4.73-1
- update to 4.73
- remove lsof_4.72-sock.patch, already in the upstream code

* Fri Jul 30 2004 Jakub Jelinek <jakub@redhat.com> 4.72-1
- update to 4.72
- use st_dev/st_ino comparison for sockets by name if possible
  (#126419)

* Fri Jul 18 2003 Jakub Jelinek <jakub@redhat.com> 4.68-1
- update to 4.68 (#99064)

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Dec 12 2002 Tim Powers <timp@redhat.com> 4.63-3
- rebuild on all arches

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Jun 21 2002 Jakub Jelinek <jakub@redhat.com> 4.63-1
- update to 4.63 (#66333).

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Thu Sep  7 2000 Jeff Johnson <jbj@redhat.com>
- update to 4.51.

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Wed Jun 14 2000 Jeff Johnson <jbj@redhat.com>
- FHS packaging.

* Sun Mar 26 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- change to root:root perms

* Wed Feb 02 2000 Cristian Gafton <gafton@redhat.com>
- fix description
- man pages are compressed

* Wed Dec 22 1999 Jeff Johnson <jbj@redhat.com>
- update to 4.47.

* Tue Aug  3 1999 Jeff Johnson <jbj@redhat.com>
- update to 4.45.

* Fri Jun 25 1999 Jeff Johnson <jbj@redhat.com>
- update to 4.44.

* Fri May 14 1999 Jeff Johnson <jbj@redhat.com>
- upgrade to 4.43 with sparc64 tweak (#2803)

* Thu Apr 08 1999 Preston Brown <pbrown@redhat.com>
- upgrade to 4.42 (security fix)

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 5)

* Fri Mar 19 1999 Jeff Johnson <jbj@redhat.com>
- turn off setgid kmem "just in case".

* Thu Feb 18 1999 Jeff Johnson <jbj@redhat.com>
- buffer overflow patch.
- upgrade to 4.40.

* Wed Dec 30 1998 Jeff Johnson <jbj@redhat.com>
- update to "official" 4.39 release.

* Wed Dec 16 1998 Jeff Johnson <jbj@redhat.com>
- update to 4.39B (linux) with internal kernel src.

* Tue Dec 15 1998 Jeff Johnson <jbj@redhat.com>
- update to 4.39A (linux)

* Sat Sep 19 1998 Jeff Johnson <jbj@redhat.com>
- update to 4.37

* Thu Sep 10 1998 Jeff Johnson <jbj@redhat.com>
- update to 4.36

* Thu Jul 23 1998 Jeff Johnson <jbj@redhat.com>
- upgrade to 4.35.
- rewrap for RH 5.2.

* Mon Jun 29 1998 Maciej Lesniewski <nimir@kis.p.lodz.pl>
  [4.34-1]
- New version
- Spec rewriten to use %%{name} and %%{version} macros
- Removed old log enteries

* Tue Apr 28 1998 Maciej Lesniewski <nimir@kis.p.lodz.pl>
- Built under RH5
- install macro was changed
