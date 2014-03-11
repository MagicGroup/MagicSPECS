%define posix_version 2003
%define posix_release a

Summary: Man (manual) pages from the Linux Documentation Project
Name: man-pages
Version: 3.35
Release: 2%{?dist}
License: GPLv2+ and GPL+ and BSD and MIT and Copyright only and IEEE
Group: Documentation
URL: http://man7.org/linux/man-pages/
Source0: http://man7.org/linux/man-pages/download/man-pages-%{version}.tar.gz
# POSIX man pages
Source1: http://www.kernel.org/pub/linux/docs/man-pages/man-pages-posix/man-pages-posix-%{posix_version}-%{posix_release}.tar.bz2
# additional man-pages, the source tarball is fedora only
# all man-pages have a license info
Source2: man-pages-additional-20101006.tar.bz2
Patch28: man-pages-2.46-nscd.patch
Patch36: man-pages-2.63-unimplemented.patch
Patch45: man-pages-2.48-passwd.patch
Patch46: man-pages-2.51-nscd-conf.patch
Patch53: man-pages-2.78-stream.patch
Patch57: man-pages-3.22-nsswitch.conf.patch
Patch58: man-pages-3.23-proc.patch
Patch59: man-pages-3.23-ld.so.patch
Patch60: man-pages-3.22-sched_setaffinity.patch
Patch63: man-pages-3.24-getnameinfo.patch
Patch67: man-pages-3.24-mmap64.patch
Patch68: man-pages-3.26-rcmd.patch
Patch69: man-pages-3.27-sd.patch
Patch70: man-pages-3.29-uri.patch
Patch71: man-pages-posix-2003-awk.patch
Patch72: man-pages-posix-2003-man.patch
Patch73: man-pages-posix-2003-printf.patch
#Resolves: #647269
Patch75: man-pages-3.30-prctl.patch
#Resolves: #652870
Patch76: man-pages-3.32-strtol.patch
#Resolves: #652869
Patch77: man-pages-3.32-readdir.patch
#Resolves: #679899
Patch78: man-pages-2.39-gai.conf.patch
#Resolves: #675544
Patch79: man-pages-3.32-spellch.patch
#resolves: #681781
Patch80: man-pages-3.35-printf.patch
#resolves: #680214
Patch81: man-pages-3.35-fallocate.patch
#resolves: #698149
Patch82: man-pages-3.32-host.patch
#resolves: #705888 
Patch83: man-pages-3.23-proc_cgroups.patch
#resolves: #723578
Patch84: man-pages-3.35-readlink3p.patch
#Resolves: #655961
Conflicts: quota < 3.17-14
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Autoreq: false
BuildArch: noarch

%description
A large collection of man pages (documentation) from the Linux
Documentation Project (LDP).

%prep
%setup -q -n %{name}-%{version} -a 1 -a 2

mv man-pages-posix-%{posix_version}-%{posix_release}/Changes{,.posix}
mv man-pages-posix-%{posix_version}-%{posix_release}/* ./
rmdir man-pages-posix-%{posix_version}-%{posix_release}
%patch28 -p1
%patch36 -p1
%patch45 -p1
%patch46 -p1
%patch53 -p1
%patch57 -p1
%patch58 -p1
%patch59 -p1
%patch60 -p1
%patch63 -p1
%patch67 -p1
%patch68 -p1
%patch69 -p1
%patch70 -p1
%patch71 -p1
%patch72 -p1
%patch73 -p1
%patch75 -p1
%patch76 -p1
%patch77 -p1
%patch78 -p1
%patch79 -p1
%patch80 -p1
%patch81 -p1
%patch82 -p1
%patch83 -p1
%patch84 -p1

### And now remove those we are not going to use:

# Part of libattr-devel
rm -v man2/{,f,l}{get,list,remove,set}xattr.2

# Problem with db x db4 (#198597) - man pages are obsolete
rm -v man3/{db,btree,dbopen,hash,mpool,recno}.3

# Deprecated
rm -v man2/pciconfig_{write,read,iobase}.2

%build
: Nothing to build.


%install
rm -rf $RPM_BUILD_ROOT

instdir=$RPM_BUILD_ROOT%{_mandir}
for sec in 0p 1 1p 2 3 3p 4 5 6 7 8 9; do
  mkdir -p $instdir{,/en}/man$sec
  for f in man$sec/*.$sec; do
    case $f in
      man$sec/'*'.$sec)
	# this dir is empty
	continue ;;
      man7/iso_8859-*.7)
	enc=${f#man7/}
	enc=${enc%.7}
	enc=ISO-${enc#iso_}
	LANG=en iconv -f $enc -t utf-8 $f | sed -e '1s/coding: *[^ ]* /coding: UTF-8 /' > $instdir/$f ;;
      man7/koi8-*.7 | man7/armscii-8.7 | man7/cp1251.7)
	enc=${f#man7/}
	enc=${enc%.7}
	LANG=en iconv -f $enc -t utf-8 $f | sed -e '1s/coding: *[^ ]* /coding: UTF-8 /' > $instdir/$f ;;
      *)
	LANG=en iconv -f latin1 -t utf-8 -o $instdir/en/$f $f
	LANG=en iconv -f utf-8 -t ascii//translit -o $instdir/$f $instdir/en/$f
	cmp -s $instdir/$f $instdir/en/$f &&
	  rm $instdir/en/$f ;;
    esac
  done
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0644,root,root,0755)
%doc README man-pages-%{version}.Announce POSIX-COPYRIGHT
%{_mandir}/man*/*
%lang(en) %{_mandir}/en/man*/*

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 3.35-2
- 为 Magic 3.0 重建

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

* Wed Jun 11 2008 Ivana Varekova <varekova@redhat.com> - 2.80-2
- reformulate the malloc_hook patch

* Tue Jun 10 2008 Ivana Varekova <varekova@redhat.com> - 2.80-1
- update to 2.80
- Resolves: #450187
  deprecate malloc_hook(3) man page

* Fri Mar  7 2008 Ivana Varekova <varekova@redhat.com> - 2.78-2
- fix 436398:
  add information about unimplemented syscalls

* Fri Feb 22 2008 Ivana Varekova <varekova@redhat.com> - 2.78-1
- update to 2.78

* Tue Jan 29 2008 Ivana Varekova <varekova@redhat.com> - 2.76-1
- update to 2.76
- add new option to prctl man page

* Fri Jan 11 2008 Ivana Varekova <varekova@redhat.com> - 2.75-2
- update crypt.3 man page

* Fri Jan 11 2008 Ivana Varekova <varekova@redhat.com> - 2.75-1
- update to 2.75
- remove fs page patch

* Mon Dec 17 2007 Ivana Varekova <varekova@redhat.com> - 2.73-1
- update to 2.73

* Tue Dec  4 2007 Ivana Varekova <varekova@redhat.com> - 2.69-1
- update to 2.69

* Thu Nov 22 2007 Ivana Varekova <varekova@redhat.com> - 2.68-1
- update to 2.68

* Mon Oct 22 2007 Ivana Varekova <varekova@redhat.com> - 2.67-1
- update to 2.67

* Tue Oct  9 2007 Ivana Varekova <varekova@redhat.com> - 2.66-1
- update to 2.66
- add proc man-page patch

* Tue Sep 18 2007 Ivana Varekova <varekova@redhat.com> - 2.65-1
- update to 2.65

* Tue Aug 14 2007 Ivana Varekova <varekova@redhat.com> - 2.64-1
- update to 2.64
- remove obsolete patch

* Tue Aug  7 2007 Ivana Varekova <varekova@redhat.com> - 2.63-3
- add iconv patch (245040)
  thanks to Josef Kubin

* Wed Jul 20 2007 Ivana Varekova <varekova@redhat.com> - 2.63-2
- Resolves: #248655 
  add getent patch (thanks Ville Skyttä)

* Wed Jul 20 2007 Ivana Varekova <varekova@redhat.com> - 2.63-1
- update to 2.63

* Tue Jun 26 2007 Ivana Varekova <varekova@redhat.com> - 2.55-3
- remove ncsa_auth.8

* Mon Jun 11 2007 Stepan Kasal <skasal@redhat.com> - 2.55-2
- Add man-suid-bins.tar.bz2 and uuname.1 to document suid binaries
  (submitted through bug #196352).
- Add man-pages-2.51-sched_setaffinity.patch, fixing the prototypes.
- Remove sccs-related man pages.
- Add man-pages-2.55-syscalls-2.6.9.patch, updating syscalls.2 to kernel
  version 2.6.9.
- Add man-pages-2.55-clone2.patch; s/clone2/__&/, clone2 is not exported.
- Add man-pages-2.55-signal.patch; SIGRTMIN is not constant.

* Mon Jun 11 2007 Ivana Varekova <varekova@redhat.com> - 2.55-1
- update to 2.55

* Mon Jun  4 2007 Stepan Kasal <skasal@redhat.com> - 2.51-4
- Simplify the build and install phases; pages are now recoded during the
  install.
- Move the "rm" commands from build to prep.
- Add man-pages-2.51-epoll_pwait.patch to fix a circular link.

* Mon Jun  4 2007 Stepan Kasal <skasal@redhat.com> - 2.51-3
- Add man-pages-2.51-nscd-conf.patch, fixes #204596
- Fix typos, man-pages-2.51-typos.patch

* Thu May 31 2007 Ivana Varekova <varekova@redhat.com> 2.51-2
- remove mount page patch
- fix mmap patch

* Wed May 30 2007 Ivana Varekova <varekova@redhat.com> 2.51-1
- update to 2.51

* Mon May 21 2007 Ivana Varekova <varekova@redhat.com> 2.49-1
- update to 2.49

* Fri May 11 2007 Ivana Varekova <varekova@redhat.com> 2.48-1
- update to 2.48

* Mon Apr 30 2007 Ivana Varekova <varekova@redhat.com> 2.46-1
- update to 2.46

* Wed Apr 11 2007 Ivana Varekova <varekova@redhat.com> 2.44-1
- update to 2.44

* Mon Apr  2 2007 Steve Dickson <steved@redhat.com> 2.43-12
- Remove the rpcinfo man page (#228894).

* Fri Mar 16 2007 Ivana Varekova <varekova@redhat.com> 2.43-11
- Resolves: 230899
  Error in the man-pages.spec file: incorrect encoding convertation

* Mon Mar 12 2007 Ivana Varekova <varekova@redhat.com> 2.43-10
- change the default buildroot

* Mon Mar 12 2007 Ivana Varekova <varekova@redhat.com> 2.43-9
- add lang macro

* Tue Feb 27 2007 Ivana Varekova <varekova@redhat.com> 2.43-8
- fix 229870 - bug in fadvise(2)
- fix 229204 - bug in passwd(5)

* Thu Feb 15 2007 Ivana Varekova <varekova@redhat.com> 2.43-7
- fix rand.3 man page (#228662)
  thanks Mark Summerfield

* Tue Feb 13 2007 Ivana Varekova <varekova@redhat.com> 2.43-6
- Resolves: 227260
  fix iso-8859 (koi8-r) man pages

* Mon Jan 29 2007 Ivana Varekova <varekova@redhat.com> 2.43-4
- fix rt_sigprocmask.2 (#219074)
- remove pciconfig_{read,write,iobase}.2 (#219827)
- fix swapon.2 (#222493)

* Fri Jan 12 2007 Ivana Varekova <varekova@redhat.com> 2.43-3
- fix mmap2 man page
- spec file cleanup

* Fri Dec  8 2006 Ivana Varekova <varekova@redhat.com> 2.43-2
- remove old/wrong patches
- fix tgkill/tkill man pages inconsistency 

* Fri Dec  1 2006 Ivana Varekova <varekova@redhat.com> 2.43-1
- update to 2.43
- fix mount.2 man page (#211608)

* Fri Oct 20 2006 Ivana Varekova <varekova@redhat.com> 2.41-2
- fix mmap(2) man page

* Fri Oct 20 2006 Ivana Varekova <varekova@redhat.com> 2.41-1
- update to 2.41

* Mon Oct  2 2006 Ivana Varekova <varekova@redhat.com> 2.39-6
- add getunwind.2, kexec_load.2, move_pages.2, perfmonctl.2, 
  spu_create.2, spufs.2, spu_run.2 and  vserver.2 man pages

* Mon Aug 28 2006 Ivana Varekova <varekova@redhat.com> 2.39-5
- add the description clone2 syscall to clone.2 man page
- add multiplexer.2 man page 

* Wed Aug 23 2006 Ivana Varekova <varekova@redhat.com> 2.39-4
- add (get/set)_robust_list.2 man pages
- add add_key.2, keyctl.2, request_key.2 man pages 
    (removed from keyutils-libs-devel package)
- add tux.2 man page
    (removed from tux package)

* Mon Aug 14 2006 Marcela Maslanova <mmaslano@redhat.com> 2.39-3
- fix same bug better

* Wed Aug 09 2006 Marcela Maslanova <mmaslano@redhat.com> 2.39-2
- fix(#200681) typo

* Wed Aug 09 2006 Marcela Maslanova <mmaslano@redhat.com> 2.39-1
- new version 2.39

* Thu Jul 20 2006 Marcela Maslanova <mmaslano@redhat.com> 2.36-2
- fix (#198903)

* Fri Jul 14 2006 Ivana Varekova <varekova@redhat.com> 2.36-1
- add nscd_conf options (nscd_conf.patch)
- added {create,query}_module.2, get_kernel_syms.2 man-pages 
- added nscd, getrlimit, libaio and write patch
- remove sigprocmask patch
- update to 2.36

* Thu Jul 13 2006 Marcela Maslanova <mmaslano@redhat.com> 2.34-3
- fix small typo (#198663)

* Wed Jul 12 2006 Ivana Varekova <varekova@redhat.com> 2.34-2
- remove btree, dbopen, hash, mpool and recno man-pages
  (#198597)

* Thu Jun 29 2006 Ivana Varekova <varekova@redhat.com> 2.34-1
- update to 2.34
- add inet patch (#189147)

* Fri May 26 2006 Ivana Varekova <varekova@redhat.com> 2.32-2
- add nss.5 man page (#192142)
- add the man-pages directories (#192998)

* Mon May 15 2006 Ivana Varekova <varekova@redhat.com> 2.32-1
- update to 2.32
- add gai.conf.5 man page (#191656)

* Mon Apr 18 2006 Ivana Varekova <varekova@redhat.com> 2.29-1
- update to 2.29
- fix sigprocmask(2) man page (#189121)

* Thu Mar 16 2006 Ivana Varekova <varekova@redhat.com> 2.25-2
- fix MALLOC_CHECK_ description (#185502)

* Tue Mar 14 2006 Ivana Varekova <varekova@redhat.com> 2.25-1
- update to 2.25
- remove mbind and set_mempolicy files
- fix dbopen man page (#185310)

* Mon Jan 16 2006 Ivana Varekova <varekova@redhat.com> 2.21-1
- update to 2.21
- add the description of reload-count option (nscd.conf 
  man page - bug 177368)

* Fri Jan  6 2006 Ivana Varekova <varekova@redhat.com> 2.20-1
- update to 2.20

* Tue Dec 13 2005 Ivana Varekova <varekova@redhat.com> 2.16-2
- fix bug 174628 - mmap(2) CAN return mappings at location 0

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Dec  8 2005 Ivana Varekova <varekova@redhat.com> 2.16-1
- update to 2.16

* Thu Nov 10 2005 Ivana Varekova <varekova@redhat.com> 2.13-1
- update to 2.13

* Mon Oct 10 2005 Ivana Varekova <varekova@redhat.com> 2.08-1
- update to 2.08

* Thu Sep 29 2005 Ivana Varekova <varekova@redhat.com> 2.07-7
- fix typo in nsswitch.conf man page (bug 169309)

* Thu Sep 29 2005 Ivana Varekova <varekova@redhat.com> 2.07-6
- man pages updated for new audit system (added missing man-pages 
of some syscalls) (see bug 159225)

* Tue Sep 13 2005 Ivana Varekova <varekova@redhat.com> 2.07-5
- change termcap SEE ALSO part - bug 168131

* Mon Sep 12 2005 Ivana Varekova <varekova@redhat.com> 2.07-3
- fix socket.7 man page - fix information about SO_RCVLOWAT option
  (bug 163120)

* Tue Aug 23 2005 Ivana Varekova <varekova@redhat.com> 2.07-2
- add sln.8 man page (bug 10601)

* Mon Aug  8 2005 Ivana Varekova <varekova@redhat.com> 2.07-1
- update to 2.07

* Mon Jul 04 2005 Jiri Ryska <jryska@redhat.com> 2.05-1
- update to 2.05
- atanh(3) fix
- issue(5) fix
- ldd(1) fix
- removed man1p/{compress,uncompress,renice}.1p

* Mon Apr  4 2005 Jiri Ryska <jryska@redhat.com> 1.67-7
- io_setup() and io_destroy() pages now refers to header file
- fixed types for struct shmid_ds in shmget(2) and shmctl(2)
- fixed pages for readv(2) and writev(2)

* Mon Mar  7 2005 Jindrich Novy <jnovy@redhat.com> 1.67-6
- unify fs.5 patches together to get rid of the bogus
  fs.5.orig.gz shipped among man5 pages
- bump release to 6 to avoid conflicts with RHEL4/FC3 man-pages

* Wed Aug 25 2004 Adrian Havill <havill@redhat.com> 1.67-3
- make resolver clearer and less bind-focused (#126696)

* Fri Aug 20 2004 Adrian Havill <havill@redhat.com> 1.67-2
- updated to latest
- getrpcent/setrpcent typo (#73836)
- add new resolver.5 page (#126557)
- add SHM_HUGETLB option to shmget (#128837)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Apr 16 2004 Adrian Havill <havill@redhat.com> 1.66-3
- fixed minor typo (#118169)

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Feb 11 2004 Adrian Havill <havill@redhat.com> 1.66-1
- update to 1.66
- add posix section processing for sections 0p, 1p, 3p (#114584)

* Mon Dec 15 2003 Adrian Havill <havill@redhat.com> 1.64-2
- update to 1.64
- convert iso-8859-1 en locale pages to UTF-8 for fc2 (#108991)

* Wed Sep 24 2003 Adrian Havill <havill@redhat.com> 1.60-4.1
- bump n-v-r

* Wed Sep 24 2003 Adrian Havill <havill@redhat.com> 1.60-4
- transliterated ALL pages with latin-1 characters that would be
  displayed as either a fallback from a ascii-superset locale or
  from the POSIX locale into ascii (according to glibc transliteration
  data for locale "en"). pages with non-ascii are moved into the "en"
  locale. (#103214)

* Thu Aug 28 2003 Adrian Havill <havill@redhat.com> 1.60-2
- transliterated Lichtmaier's first name for the sake of iconv (#103214)

* Thu Aug 28 2003 Adrian Havill <havill@redhat.com> 1.60-1.1
- bumped n-v-r

* Thu Aug 28 2003 Adrian Havill <havill@redhat.com> 1.60-1
- bumped version, removed no longer needed patches
- added #define for re_comp() and re_exec() (#79703)
- fixed typo in Era format specifier (#80025)
- fixed ftell info for fopen with mode "a+" (#81359)
- fixed prototype for shmget() (#86258)
- fixed spelling in wait.2 (#86450)
- obsoleted _init and _fini in dlopen() (#88408)
- fixed and merged double ext3 descriptions (#103198)
- issue to refer to mingetty (#86248)
- synced man page with actual ld params (#97176)

* Fri Aug 01 2003 Elliot Lee <sopwith@redhat.com> 1.58-2
- Remove libattr conflicts

* Wed Jul 30 2003 Adrian Havill <havill@redhat.com> 1.58-1
- Bumped version (which also solves n-v-r conflict with RHEL)

* Fri Jul 11 2003 Ernie Petrides <petrides@redhat.com>
- Modify mlock.2, mlockall.2, and shmctl.2 for change to locking
  permission semantics made in kernel's linux-2.4.21-mlock.patch.

* Tue Apr 29 2003 Ernie Petrides <petrides@redhat.com>
- Modify semop.2 for new semtimedop(2) and add semtimedop.2 link.

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Dec 11 2002 Tim Powers <timp@redhat.com> 1.53-2
- rebuild

* Tue Aug 27 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.53-1
- 1.53
- Fix #71750, #72754

* Thu Jul 25 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.52-2
- Fix reference in rpcgen(1) - #69740

* Wed Jul 24 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.52-1
- 1.52

* Thu Jul 18 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.51-5
- Fix #63547

* Tue Jul  9 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.51-4
- Mentium mem=nopentium in bootparam(7) - #60487

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jun 12 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.51-2
- Fix to iconv(1) - #66441

* Tue Jun 11 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.51-1
- 1.51

* Thu Jun  6 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.50-1
- 1.50

* Wed May 29 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.48-4
- Bump

* Thu May 23 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.48-3
- Ret value of iconv(3) was wrong (#65375)

* Thu Apr  4 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.48-2
- Remove getipnodebyname, getipnodebyname, freehostent - they were
  only briefly part of a glibc devel version (#62646)

* Wed Mar 13 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.48-1
- 1.48

* Thu Feb 21 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.47-2
- Rebuild

* Tue Jan 15 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.47-1
- 1.47

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Dec  6 2001 Trond Eivind Glomsrød <teg@redhat.com> 1.44-2
- Add entry on ext3 in fs.5 (#55945)

* Tue Dec  4 2001 Trond Eivind Glomsrød <teg@redhat.com> 1.44-1
- 1.44
- No patches required anymore - get rid of them.

* Thu Nov 15 2001 Trond Eivind Glomsrød <teg@redhat.com> 1.43-2
- Fix docs for setresuid/setresgid (#56038)

* Thu Nov  8 2001 Trond Eivind Glomsrød <teg@redhat.com> 1.43-1
- 1.43

* Tue Oct 23 2001 Trond Eivind Glomsrød <teg@redhat.com> 1.42-1
- 1.42

* Mon Oct 15 2001 Trond Eivind Glomsrød <teg@redhat.com> 1.41-1
- 1.41
- Remove bug section in llseek.2, which claimed ext2 don't support
  files bigger than 2 GB (#54569)

* Tue Sep 25 2001 Trond Eivind Glomsrød <teg@redhat.com> 1.40-1
- 1.40. Remove now included patches.

* Tue Sep  4 2001 Trond Eivind Glomsrød <teg@redhat.com> 1.39-2
- New strptime.3, from the ftp site. Matches glibc better.
- Fix missing .br in netdevices.7 (#53091)

* Tue Aug  7 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 1.39
- Drop obsolete patches

* Tue Jul 24 2001 Trond Eivind Glomsrød <teg@redhat.com>
- s/NSF/NFS/ in initrd.4 - (#48322)

* Mon Jul  2 2001 Trond Eivind Glomsrød <teg@redhat.com>
- regcomp and friends support collating elements now (#46939)

* Thu Jun 21 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 1.38

* Fri Jun  8 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 1.37

* Thu Jun  7 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Remove capset(2) - part of libcap (#43828)

* Fri Jun  1 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Remove diff.1 - let diffutils include it instead
- Remove capget.2 - it's included in libcap
- Keep resolv.conf.5 - it's useful on systems without bind packages
- Fix bootparam.7 (patch from Tim Waugh (twaugh@redhat.com)

* Tue May 22 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 1.36
- drop some old patches, redo others

* Thu May 17 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Work around bug in groff for latin1.7 (#41118)

* Wed Apr  4 2001 Trond Eivind Glomsrød <teg@redhat.com>
- use MS_SYNCHRONOUS instead of MS_SYNC in mount(2) (#34665)

* Tue Apr  3 2001 Trond Eivind Glomsrød <teg@redhat.com>
- roff fixes to multiple man pages

* Mon Apr  2 2001 Trond Eivind Glomsrød <teg@redhat.com>
- correct the URL for unicode in the charset manpage (#34291)
- roff fixes
- redo iconv patch, so we don't get a .orig from patch because of
  a two line offset

* Fri Mar 30 2001 Trond Eivind Glomsrød <teg@redhat.com>
- remove resolv.conf (bind-utils) and infnan (obsolete - #34171)

* Wed Mar 28 2001 Trond Eivind Glomsrød <teg@redhat.com>
- resurrect getnetent(3)

* Sun Mar 25 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 1.35, obsoletes patch for strsep
- move rpcinfo to section 8 (#33114)

* Fri Mar  9 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Include man-pages on locales (#29713)

* Tue Feb 13 2001 Trond Eivind Glomsrød <teg@redhat.com>
- fix return value of strsep(3) call (#24789)

* Mon Jan 15 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 1.34

* Fri Dec 15 2000 Trond Eivind Glomsrød <teg@redhat.com>
- 1.33
- obsolete some old, now included patches
- remove netman-cvs, it's now older than the mainstream

* Tue Nov 21 2000 Trond Eivind Glomsrød <teg@redhat.com>
- Identify two of the macros in stat(2) as GNU, not POSIX. (#21169)

* Wed Nov 08 2000 Trond Eivind Glomsrød <teg@redhat.com>
- don't delete the man pages for dlopen() and friends, 
  they are no longer part of another package
- include man pages for ld*

* Thu Oct 24 2000 Trond Eivind Glomsrød <teg@redhat.com>
- remove const from iconv function prototype (#19486)

* Tue Aug 29 2000 Trond Eivind Glomsrød <teg@redhat.com>
- reference wctype(3) instead of non-existing ctype(3)
  from regex(7) (#17037)
- 1.31

* Sun Aug 27 2000 Trond Eivind Glomsrød <teg@redhat.com>
- remove lilo man pages (now included in package)
  (#16984)

* Fri Aug 04 2000 Trond Eivind Glomsrød <teg@redhat.com>
- fixed bad header specification (#15364)
- removed obsolete patches from package
- updated the rest

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jun 19 2000 Matt Wilson <msw@redhat.com>
- defattr before docs in filelist

* Sun Jun 17 2000 Trond Eivind Glomsrød <teg@redhat.com>
- updated to 1.30

* Tue Jun 06 2000 Trond Eivind Glomsrød <teg@redhat.com>
- use %%{_tmppath}

* Wed May 31 2000 Trond Eivind Glomsrød <teg@redhat.com>
- remove resolv.conf(5) - part of bind-utils

* Tue May 30 2000 Trond Eivind Glomsrød <teg@redhat.com>
- Remove resolver, dlclose, dlerror, dlopen, dlsym as these
  are included in other packages.

* Tue May 30 2000 Trond Eivind Glomsrød <teg@redhat.com>
- use %%{_mandir) instead of /usr/man
- verify and fix bug in mmap man page (#7382)
- verify and fix missing data in recvfrom man page (#1736)
- verify and fix missing data in putw man page (#10104)
- fixed sendfile(2) man page (#5599)
- fixed tzset man page (#11623)

* Mon May 15 2000 Trond Eivind Glomsrød <teg@redhat.com>
- updated to 1.29
- split off other languages into separate RPMS 

* Thu Mar 16 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- do not use group "man"

* Fri Mar 03 2000 Cristian Gafton <gafton@redhat.com>
- don't apply the netman-cvs man pages anymore, as they seem to be really
  out of date

* Sat Feb 05 2000 Cristian Gafton <gafton@redhat.com>
- put back man3/resolver.3

* Fri Feb 04 2000 Cristian Gafton <gafton@redhat.com>
- remove non-man pages (#7814)

* Fri Feb  4 2000 Matt Wilson <msw@redhat.com>
- exclude dir.1 and vdir.1 (these are in the fileutils package)

* Thu Feb 03 2000 Cristian Gafton <gafton@redhat.com>
- version 1.28

* Fri Nov 05 1999 Michael K. Johnson <johnsonm@redhat.com>
- Fixed SIGILL, SIGQUIT in signals.7

* Wed Oct 06 1999 Cristian Gafton <gafton@redhat.com>
- fix man page for getcwd

* Wed Sep 22 1999 Cristian Gafton <gafton@redhat.com>
- added man pages for set/getcontext

* Tue Sep 14 1999 Bill Nottingham <notting@redhat.com>
- remove some bad man pages

* Mon Sep 13 1999 Preston Brown <pbrown@redhat.com>
- czech, german, spanish, russian man pages

* Thu Sep 09 1999 Cristian Gafton <gafton@redhat.com>
- version 1.26
- add french man pages
- add italian man pages

* Fri Jul 23 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.25.

* Fri Apr 16 1999 Cristian Gafton <gafton@redhat.com>
- fiox man page fro ftw

* Mon Apr 05 1999 Cristian Gafton <gafton@redhat.com>
- spellnig fixse

* Tue Mar 30 1999 Bill Nottingham <notting@redhat.com>
- updated to 1.23

* Thu Mar 25 1999 Cristian Gafton <gafton@redhat.com>
- added kernel net manpages

* Mon Mar 22 1999 Erik Troan <ewt@redhat.com>
- updated printf man page
- added rpcgen man page

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 6)

* Thu Mar 18 1999 Cristian Gafton <gafton@redhat.com>
- leave the lilo man pages alone (oops)

* Fri Feb 12 1999 Michael Maher <mike@redhat.com>
- fixed bug #413

* Mon Jan 18 1999 Cristian Gafton <gafton@redhat.com>
- remove lilo man pages too
- got rebuilt for 6.0

* Tue Sep 08 1998 Cristian Gafton <gafton@redhat.com>
- version 1.21

* Sat Jun 20 1998 Jeff Johnson <jbj@redhat.com>
- updated to 1.20

* Wed May 06 1998 Cristian Gafton <gafton@redhat.com>
- get rid of the modutils man pages
- updated to 1.19

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed Apr 08 1998 Erik Troan <ewt@redhat.com>
- updated to 1.18

* Sun Oct 19 1997 Erik Troan <ewt@redhat.com>
- updated to 1.17
- moved build root to /var

* Thu Jul 31 1997 Erik Troan <ewt@redhat.com>
- made a noarch package
