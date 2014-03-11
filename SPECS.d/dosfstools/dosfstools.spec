Name: dosfstools
Summary: Utilities for making and checking MS-DOS FAT filesystems on Linux
Version: 3.0.12
Release: 3%{?dist}
License: GPLv3+
Group: Applications/System
Source0: http://www.daniel-baumann.ch/software/dosfstools/%{name}-%{version}.tar.bz2
URL: http://www.daniel-baumann.ch/software/dosfstools/
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# Fix buffer overflow in alloc_rootdir_entry (#674095)
Patch0: dosfstools-3.0.12-fix-alloc-rootdir-entry.patch
# Fix dosfslabel on FAT32 (#693662)
Patch1: dosfstools-3.0.12-dosfslabel-fat32.patch
# Fix device partitions detection (#710480)
Patch2: dosfstools-3.0.12-dev-detect-fix.patch

%description
The dosfstools package includes the mkdosfs and dosfsck utilities,
which respectively make and check MS-DOS FAT filesystems on hard
drives or on floppies.

%prep
%setup -q
%patch0 -p1 -b .fix-alloc-rootdir-entry
%patch1 -p1 -b .dosfslabel-fat32
%patch2 -p1 -b .dev-detect-fix

%build
make %{?_smp_mflags} CFLAGS="$RPM_OPT_FLAGS -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64 -fno-strict-aliasing"

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install-bin install-man PREFIX=%{_prefix} SBINDIR=%{_sbindir}

magic_rpm_clean.sh

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc ChangeLog COPYING doc/*-2.x
%{_sbindir}/*
%{_mandir}/man8/*

%changelog
* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 3.0.12-3
- 为 Magic 3.0 重建

* Mon Apr 16 2012 Liu Di <liudidi@gmail.com> - 3.0.12-2
- 为 Magic 3.0 重建

* Sat Oct 29 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 3.0.12-1
- New version, all patches were rebased
  Resolves: rhbz#749969

* Fri Jun 03 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 3.0.11-5
- Fixed device partitions detection
  Resolves: rhbz#710480

* Tue Apr 05 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 3.0.11-4
- Fixed dosfslabel on FAT32 (#693662)

* Mon Feb 14 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 3.0.11-3
- Fixed buffer overflow in alloc_rootdir_entry (#674095)
- Dropped fix-reclaim-file patch, obsoleted by fix-alloc-rootdir-entry patch

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 06 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 3.0.11-1
- New version
- Fixed buffer overflow in reclaim file (#660154)

* Fri Oct 08 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 3.0.10-2
- Fixed dosfsck and dosfslabel on s390x (#624596)

* Wed Oct 06 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 3.0.10-1
- Bump to newer release

* Mon May 31 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 3.0.9-3
- Rebuilt with -fno-strict-aliasing

* Fri Feb 26 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 3.0.9-2
- Used bz2 compresed sources

* Fri Feb 26 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 3.0.9-1
- Bump to newer release
- Removed mkdosfs-ygg from Obsoletes/Provides tag as it looks really deprecated
- Drop bounds patch - fixed upstream

* Sun Dec 06 2009 Lubomir Rintel <lkundrak@v3.sk> - 3.0.6-1
- Bump to newer release
- Fix numerous out-of-bound writes

* Mon Aug 10 2009 Ville Skyttä <ville.skytta@iki.fi> - 3.0.1-6
- Use bzipped upstream tarball.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 30 2009 Stepan Kasal <skasal@redhat.com> - 3.0.1-3
- fix the previous commit
- omit the most obsolete documents
- after writing the label, exit with exit code 0 (#468050)

* Fri Jan 30 2009 Stepan Kasal <skasal@redhat.com> - 3.0.1-2
- install all the documentation to the usual docdir (#225707)

* Mon Jan 19 2009 Peter Vrabec <pvrabec@redhat.com> - 3.0.1-1
- upgrade
- include ChangeLog and COPYING (#225707)

* Mon Nov 17 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 3.0.0-2
- apply vfat timing fix (bz 448247)

* Tue Sep 30 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 3.0.0-1
- update to 3.0.0

* Wed Jul 16 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.11-10
- fix license tag
- fix patch to apply with fuzz=0

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.11-9
- Autorebuild for GCC 4.3

* Tue Apr  3 2007 Jeremy Katz <katzj@redhat.com> - 2.11-8
- add dosfslabel (originally by Peter Jones)

* Wed Feb 21 2007 Peter Vrabec <pvrabec@redhat.com> 2.11-7
- fix debuginfo package (#225707)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.11-6.1
- rebuild

* Fri Jun 30 2006 Peter Vrabec <pvrabec@redhat.com> 2.11-6
- fix upgrade path (#197231)

* Thu May 11 2006 Peter Vrabec <pvrabec@redhat.com> 2.11-5
- fix work with disk image files > 4GB (#191198)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.11-4.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.11-4.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Sun Dec 16 2005 Jakub Jelinek <jakub@redhat.com> 2.11-4
- rebuilt with GCC 4.1
- make it build with -D_FORTIFY_SOURCE=2

* Sun Nov 06 2005 Peter Vrabec <pvrabec@redhat.com> 2.11-3
- fix LFS (#172369)

* Fri Nov 04 2005 Peter Vrabec <pvrabec@redhat.com> 2.11-2
- fix LFS

* Wed Oct 12 2005 Peter Vrabec <pvrabec@redhat.com> 2.11-1
- upgrade

* Thu Apr 28 2005 Peter Vrabec <pvrabec@redhat.com> 2.10-3
- if HDIO_GETGEO fails, print a warning and default to H=255,S=63 (#155950)

* Thu Mar 17 2005 Peter Vrabec <pvrabec@redhat.com> 2.10-2
- rebuild

* Thu Dec 09 2004 Peter Vrabec <pvrabec@redhat.com>  2.10-1
- updated to 2.10

* Wed Nov 10 2004 Martin Stransky <stransky@redhat.com> 2.8-16
- add check for minimum count of clusters in FAT16 and FAT32

* Wed Oct 13 2004 Peter Vrabec <pvrabec@redhat.com> 2.8-15
- fix fat_length type in boot.c. (same problem like in RHEL bug #135293)

* Wed Oct  6 2004 Jeremy Katz <katzj@redhat.com> - 2.8-14
- fix rebuilding (#134834)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Sep  3 2003 Bill Nottingham <notting@redhat.com> 2.8-11
- rebuild

* Wed Sep  3 2003 Bill Nottingham <notting@redhat.com> 2.8-10
- don't rely on <linux/msdos_fs.h> including <asm/byteorder.h>

* Tue Jun 24 2003 Jeremy Katz <katzj@redhat.com> 2.8-9
- rebuild

* Tue Jun 24 2003 Jeremy Katz <katzj@redhat.com> 2.8-8
- add patch from Vince Busam (http://www.sixpak.org/dosfstools/) to do auto 
  creation of FAT32 on large devices (#97308)

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Feb 19 2003 Jeremy Katz <katzj@redhat.com> 2.8-6
- handle getting the size of loop devices properly (part of #84351)

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Dec 12 2002 Elliot Lee <sopwith@redhat.com> 2.8-4
- Patch2 for errno

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Mar 07 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- update to version 2.8

* Fri Jul  6 2001 Preston Brown <pbrown@redhat.com>
- major upgrade to v2.7.
- forward port old ia64 patch (now incorporated) s390 additions

* Tue Mar 20 2001 Oliver Paukstadt <oliver.paukstadt@millenux.com>
- ported to zSeries (64 bit)

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Fri Jun 17 2000 Bill Nottingham <notting@redhat.com>
- hard link mkdosfs

* Thu Jun 15 2000 Matt Wilson <msw@redhat.com>
- FHS
- patch to build against 2.4 kernel headers (patch3)

* Fri Apr 28 2000 Bill Nottingham <notting@redhat.com>
- fix for ia64

* Thu Feb  3 2000 Matt Wilson <msw@redhat.com>
- remove mkdosfs.8 symlink, symlink mkdosfs.8.gz to mkfs.msdos.8.gz

* Wed Feb 02 2000 Cristian Gafton <gafton@redhat.com>
- fix descriptions and summary
- man pages are compressed

* Thu Dec 16 1999 Cristian Gafton <gafton@redhat.com>
- fix the 2.88MB drives (patch from hjl)

* Mon Aug 16 1999 Matt Wilson <msw@redhat.com>
- updated to 2.2

* Sun Jun 27 1999 Matt Wilson <msw@redhat.com>
- changed to new maintainer, renamed to dosfstools

* Sat Apr 17 1999 Jeff Johnson <jbj@redhat.com>
- fix mkdosfs on sparc (#1746)

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 10)

* Thu Jan 21 1999 Bill Nottingham <notting@redhat.com>
- build for RH 6.0

* Tue Oct 13 1998 Cristian Gafton <gafton@redhat.com>
- avoid using unsinged long on alphas 

* Sun Aug 16 1998 Jeff Johnson <jbj@redhat.com>
- build root

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Jul 10 1997 Erik Troan <ewt@redhat.com>
- built against glibc
