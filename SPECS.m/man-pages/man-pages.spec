%global posix_version 2013
%global posix_release a
%global posix_name man-pages-posix-%{posix_version}-%{posix_release}
%global additional_version 20140218
%global additional_name man-pages-additional-%{additional_version}

Summary: Linux kernel and C library user-space interface documentation
Name: man-pages
Version: 3.70
Release: 1%{?dist}
License: GPL+ and GPLv2+ and BSD and MIT and Copyright only and IEEE
Group: Documentation
URL: http://www.kernel.org/doc/man-pages/
Source: http://www.kernel.org/pub/linux/docs/man-pages/man-pages-%{version}.tar.xz
# POSIX man pages
Source1: http://www.kernel.org/pub/linux/docs/man-pages/man-pages-posix/%{posix_name}.tar.xz
# additional man-pages, the source tarball is fedora/rhel only
Source2: %{additional_name}.tar.xz

Autoreq: false
BuildArch: noarch

## Patches ##

# POSIX man pages
# Currently none

# Regular man pages
# resolves: #698149
# http://thread.gmane.org/gmane.linux.man/3413
Patch20: man-pages-3.32-host.patch
# resolves: #650985
# https://bugzilla.kernel.org/show_bug.cgi?id=53781
Patch21: man-pages-3.42-close.patch

%description
A large collection of manual pages from the Linux Documentation Project (LDP).

%prep
%setup -q -a 1 -a 2

%patch20 -p1
%patch21 -p1

# rename posix README so we don't have conflict
%{__mv} %{posix_name}/README %{posix_name}/%{posix_name}.README

## Remove man pages we are not going to use ##

# deprecated
%{__rm} man2/pciconfig_{write,read,iobase}.2

# problem with db x db4 (#198597) - man pages are obsolete
%{__rm} man3/{db,btree,dbopen,hash,mpool,recno}.3

# we are not using SystemV anymore
%{__rm} man7/boot.7

# we do not have sccs (#203302)
%{__rm} %{posix_name}/man1p/{admin,delta,get,prs,rmdel,sact,sccs,unget,val,what}.1p

%build
# nothing to build

%install
make install DESTDIR=$RPM_BUILD_ROOT
pushd %{posix_name}
make install DESTDIR=$RPM_BUILD_ROOT
popd
pushd %{additional_name}
make install DESTDIR=$RPM_BUILD_ROOT
popd

%files
%doc README man-pages-%{version}.Announce Changes
%doc %{posix_name}/POSIX-COPYRIGHT %{posix_name}/%{posix_name}.{README,Announce}
%{_mandir}/man*/*

%changelog
* Fri Jul 11 2014 jchaloup <jchaloup@redhat.com> - 3.70-1
- resolves: #1118632
  updated to 3.70

* Mon Jun 16 2014 jchaloup <jchaloup@redhat.com> - 3.69-1
- resolves: #1111836
  updated to 3.69

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.68-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jun 02 2014 jchaloup <jchaloup@redhat.com> - 3.68-1
- resolves: #1103158
  updated to 3.68

* Tue May 27 2014 jchaloup <jchaloup@redhat.com> - 3.67-1
- resolves: #1100444
  updated to 3.67

* Fri May 09 2014 Peter Schiffer <pschiffe@redhat.com> - 3.66-1
- resolves: #1095840
  updated to 3.66

* Wed Apr 23 2014 Peter Schiffer <pschiffe@redhat.com> - 3.65-1
- resolves: #1071305
  updated to 3.65
- resolves: #1082566
  install *xattr.2 man pages

* Tue Feb 18 2014 Peter Schiffer <pschiffe@redhat.com> - 3.60-1
- updated to 3.60

* Tue Feb 18 2014 Peter Schiffer <pschiffe@redhat.com> - 3.59-1
- resolves: #1066332
  updated to 3.59
- cleaned .spec file

* Tue Feb 11 2014 Peter Schiffer <pschiffe@redhat.com> - 3.58-1
- resolves: #1063754
  updated to 3.58

* Wed Feb  5 2014 Peter Schiffer <pschiffe@redhat.com> - 3.57-2
- removed invalid patch for man(1p) man page

* Wed Jan 29 2014 Peter Schiffer <pschiffe@redhat.com> - 3.57-1
- resolves: #1058001
  updated to 3.57
- resolves: #1056781
  updated to POSIX.1 2013

* Wed Jan 15 2014 Peter Schiffer <pschiffe@redhat.com> - 3.56-1
- resolves: #1051765
  updated to 3.56

* Mon Dec 16 2013 Peter Schiffer <pschiffe@redhat.com> - 3.55-1
- resolves: #1043074
  updated to 3.55

* Wed Dec  4 2013 Peter Schiffer <pschiffe@redhat.com> - 3.54-2
- resolves: #1031703
  removed pt_chown(5) man page

* Wed Oct  9 2013 Peter Schiffer <pschiffe@redhat.com> - 3.54-1
- resolves: #1009535
  updated to 3.54

* Wed Jul 31 2013 Peter Schiffer <pschiffe@redhat.com> - 3.53-1
- resolves: #990459
  updated to 3.53

* Mon Jul 22 2013 Peter Schiffer <pschiffe@redhat.com> - 3.52-1
- resolves: #981385
  updated to 3.52
- fixed broken sentence on the futex(7) man page
- resolves: #885740
  documented O_PATH flag on the open(2) man page

* Tue Apr 23 2013 Peter Schiffer <pschiffe@redhat.com> - 3.51-1
- resolves: #921911
  updated to 3.51

* Thu Mar  7 2013 Peter Schiffer <pschiffe@redhat.com> - 3.48-1
- resolves: #918417
  updated to 3.48

* Tue Feb 12 2013 Peter Schiffer <pschiffe@redhat.com> - 3.47-1
- resolves: #910268
  updated to 3.47

* Fri Feb  1 2013 Peter Schiffer <pschiffe@redhat.com> - 3.46-2
- related: #858703
  moved killpgrp(8) man page to the amanda-client package

* Mon Jan 28 2013 Peter Schiffer <pschiffe@redhat.com> - 3.46-1
- resolves: #904950
  updated to 3.46

* Wed Jan 16 2013 Peter Schiffer <pschiffe@redhat.com> - 3.45-2
- dropped some outdated patches, few patches updated

* Fri Dec 21 2012 Peter Schiffer <pschiffe@redhat.com> - 3.45-1
- resolves: #889446
  updated to 3.45

* Wed Nov 21 2012 Peter Schiffer <pschiffe@redhat.com> - 3.44-1
- resolves: #874650
  updated to 3.44

* Thu Oct 25 2012 Peter Schiffer <pschiffe@redhat.com> - 3.43-1
- resolves: #866874
  updated to 3.43
- added description of the TCP_CONGESTION on the tcp(7) man page
- added description of the IP_MULTICAST_ALL on the ip(7) man page
- updated additional man pages

* Wed Sep 19 2012 Peter Schiffer <pschiffe@redhat.com> - 3.42-1
- resolves: #847941
  update to 3.42
- updated additional man pages
- cleaned patches
- cleaned .spec file, fixed minor encoding issue
- resolves: #837090
  updated example on inet(3) man page - use fprintf(stderr,..) instead of perror
- resolves: #751429
  included initgroups database in the nsswitch.conf(5) man page
- removed the sccs-related man pages (#203302)
- added description of single-request-reopen to the resolv.conf(5) man page (#717770)
- added missing EIDRM error code description to the shmop(2) man page (#800256)
- added documentation of several source-specific multicast socket options to the ip(7) man page (#804003)
- improved explanation about calling listen or connect on the ip(7) man page (#787567)
- added information about incorrect use of getdents(2) call to the man page (#809490)
- removed man-pages-3.22-sched_setaffinity.patch because the problem it describes was fixed in the kernel. see #533811 for more info
- documented why to use shutdown() before close() when dealing with sockets on close(2) man page (#650985)
- updated description of /proc/sys/fs/file-nr file in proc(5) man page (#497197)
- updated zdump(8) man page to match current zdump usage (#517309)
- fixed one incorrect error code on connect(2) man page (#392431)
- fixed typo in sysconf(3) man page (#202092)
- removed additional uuname(1) man page - was moved to the uucp package (#858642)
- removed obsolete additional userisdnctl(8) man page

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.41-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu May 17 2012 Peter Schiffer <pschiffe@redhat.com> - 3.41-1
- resolves: #820901
  update to 3.41

* Fri Apr 27 2012 Peter Schiffer <pschiffe@redhat.com> - 3.40-2
- related: #797857
  fixed broken source file

* Fri Apr 27 2012 Peter Schiffer <pschiffe@redhat.com> - 3.40-1
- resolves: #797857
  update to 3.40

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.35-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 11 2011 Peter Schiffer <pschiffe@redhat.com> - 3.35-1
- resolves: #751620
  update to 3.35
- resolves: #723578
  typo in readlink(3p)

* Fri May 27 2011 Ivana Hutarova Varekova <varekova@redhat.com> - 3.32-14
- resolves: #705888
  the man page for proc is missing an explanation for /proc/[pid]/cgroup

* Fri Apr 22 2011 Ivana Hutarova Varekova <varekova@redhat.com> - 3.32-13
- resolves: #698149
  Remove documentation for "order" keyword in /etc/host.conf manpage

* Fri Apr 22 2011 Ivana Hutarova Varekova <varekova@redhat.com> - 3.32-12
- resolves: #680214
  manpage for fallocate(2) is wrong

* Fri Mar 25 2011 Ivana Hutarova Varekova <varekova@redhat.com> - 3.32-11
- resolves: #681781
  snprintf man page is wrong

* Wed Mar  9 2011 Ivana Hutarova Varekova <varekova@redhat.com> - 3.32-10
- resolves: #675544
  perfmonctl(2) typo manpage fix

* Thu Feb 24 2011 Ivana Hutarova Varekova <varekova@redhat.com> - 3.32-9
- resolves: #679899
  add scopev4 to gai.conf man page 

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.32-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 31 2011 Ivana Hutarova Varekova <varekova@redhat.com> - 3.31-7
- resolves: #673586
  fix the sed pages parsing

* Thu Jan 27 2011 Ivana Hutarova Varekova <varekova@redhat.com> - 3.31-6
- resolves: #652869
  fix the necessary buffer limit in the man page for readdir_r

* Thu Jan 27 2011 Ivana Hutarova Varekova <varekova@redhat.com> - 3.31-5
- resolves: #672348
  problems with the encoding of characters set man-pages
  thanks Denis Barbier for a patch

* Tue Jan 25 2011 Ivana Hutarova Varekova <varekova@redhat.com> - 3.31-4
- resolves: #672377
  fix man-pages-2.48-passwd.patch remove trailing dots

* Tue Jan 25 2011 Ivana Hutarova Varekova <varekova@redhat.com> - 3.31-3
- resolves: #652870
  fix strtol man-page

* Mon Jan  3 2011 Ivana Hutarova Varekova <varekova@redhat.com> - 3.31-2
- update to 3.32

* Wed Nov 24 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 3.31-2
- resolves: #655961
  add the conflict tag

* Fri Nov 19 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 3.31-1
- update to 3.31

* Thu Nov 18 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 3.30-3
- resolves: #647269
  PR_SET_SECCOMP and _exit, documentation bug

* Thu Nov 11 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 3.30-2
- Resolves: #650257
  fix open.2 O_EXCL description

* Fri Nov  5 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 3.30-1
- update to 3.30

* Mon Oct 25 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 3.29-1
- update 3.29
  several bug fixes

* Wed Oct  6 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 3.28-3
- don't remove numa_maps, now the man page is not in numactl
- don't remove getipnodeby{name,addr}.3 and freehostent.3
  they are not more part of glibc-devel
- fix typo in gai_{error,suspend,cancel} pages

* Wed Oct  6 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 3.28-2
- add quotactl.2 to man-pages (the package was removed from quota - #640590)

* Wed Oct  6 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 3.28-1
- update to 3.28
- move all additional man-pages to one source
    (man-pages-additional-20101006.tar.bz2)
- remove additional man-pages without the info about license

* Thu Sep 23 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 3.27-3
- Resolves: #634626
  remove link to non-existing man page

* Thu Sep 23 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 3.27-2
- Resolves: #635869 
  remove the link to removed man page

* Thu Sep 23 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 3.27-1
- Update to 3.27
- remove obsolete patch

* Wed Sep  8 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 3.26-1
- Update to 3.26
- Resolves: 624399 (rresvport man entry misleading)

* Thu Jul  1 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 3.25-1
- Update to 3.25

* Thu Jun 24 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 3.24-7
- resolves: #606038
  filesystems.5 makes no mention of ext4

* Fri Jun  4 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 3.24-6
- Resolves: #596666
  Man page for mmap64 is confusing

* Mon May 31 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 3.24-5
- Resolves: #597429
  remove the duplicate info about error output (recv(2) man page)

* Mon May 10 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 3.24-4
- Resolves: #588620
  Typo in sysconf(3) Manual page

* Mon May  3 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 3.24-3
- fix atanh man-page bug in glibc was fixed so removed the info about it

* Fri Mar 19 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 3.24-2
- Resolves: #570703
  fix getnameinfo prototype

* Tue Mar  2 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 3.24-1
- update to 3.24
  Resolves: #569451

* Mon Feb 22 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 3.23-7
- Resolves: #564528
  Man page and "info" information on snprintf incomplete

* Wed Jan 27 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 3.23-6
- Resolves: #556199
  update iconv.1 man page

* Tue Jan 26 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 3.23-5
- Resolves: #557971
  remove unnecessary man-pages from man-pages_syscalls and man-pages_add

* Thu Dec  3 2009 Ivana Hutarova Varekova <varekova@redhat.com> - 3.23-4
- fix typo in sched_setaffinity(2) patch

* Wed Dec  2 2009 Ivana Hutarova Varekova <varekova@redhat.com> - 3.23-3
- fix sched_setaffinity(2) page - add an EXAMPLE and new NOTES

* Wed Nov 18 2009 Ivana Varekova <varekova@redhat.com> - 3.23-2
- fix ld.so man-page (#532629)

* Mon Oct  5 2009 Ivana Varekova <varekova@redhat.com> - 3.23-1
- update to 3.23
- fix proc description

* Wed Sep 16 2009 Ivana Varekova <varekova@redhat.com> - 3.22-6
- fix nsswitch.conf(5) man page

* Mon Sep 14 2009 Ivana Varekova <varekova@redhat.com> - 3.22-5
- fix strcpy.3 man page
- remove statfc64 man page from syscalls tarball

* Tue Aug 11 2009 Ivana Varekova <varekova@redhat.com> - 3.22-4
- fix gai.conf an page (#515347)

* Mon Jul 27 2009 Ivana Varekova <varekova@redhat.com> - 3.22-3
- update to 3.22

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 17 2009 Ivana Varekova <varekova@redhat.com> - 3.21-2
- fix major.3 man page

* Tue Apr 21 2009 Ivana Varekova <varekova@redhat.com> - 3.21-1
- update to 3.21

* Tue Mar 31 2009 Ivana Varekova <varekova@redhat.com> - 3.20-1
- update to 3.20

* Tue Mar 10 2009 Ivana Varekova <varekova@redhat.com> - 3.19-1
- update to 3.19

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 16 2009 Ivana Varekova <varekova@redhat.com> - 3.16-1
- update to 3.16

* Mon Dec  8 2008 Ivana Varekova <varekova@redhat.com> - 3.15-1
- update to 3.15

* Thu Nov 13 2008 Ivana Varekova <varekova@redhat.com> - 3.13-2
- fix relative path in proc.5
- not build yet

* Thu Nov 13 2008 Ivana Varekova <varekova@redhat.com> - 3.13-1
- update to 3.13

* Mon Sep 15 2008 Ivana Varekova <varekova@redhat.com> - 3.09-2
- remove numa_maps.5 man page (part of numactl)

* Fri Sep 12 2008 Ivana Varekova <varekova@redhat.com> - 3.09-1
- update to 3.09

* Thu Aug 14 2008 Ivana Varekova <varekova@redhat.com> - 3.07-1
- update to 3.07
- remove ncsa_auth.8 (#458498)

* Thu Aug  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 3.04-2
- fix license tag

* Tue Jul 22 2008 Ivana Varekova <varekova@redhat.com> - 3.04-1
- update to 3.04
- remove mmap, sched_setaffinity, crypt and prctl patches
- remove -f from rm commands
- remove unnecessary/bogus rm commands

* Wed Jun 18 2008 Ivana Varekova <varekova@redhat.com> - 3.00-1
- update to 3.00
- source files changes
