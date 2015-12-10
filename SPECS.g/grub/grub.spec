Name: grub
Version: 0.97
Release: 20%{?dist}
Summary: GRUB - the Grand Unified Boot Loader.
Summary(zh_CN.UTF-8): GRUB - 多重引导管理系统。
Group: System Environment/Base
Group(zh_CN.UTF-8): 系统环境/基本
License: GPL
URL: http://www.gnu.org/software/%{name}/
Source0: ftp://alpha.gnu.org/gnu/%{name}/%{name}-%{version}.tar.gz
Source1: splash.xpm.gz
Source2: 	grubonce
Source3:	message
Patch0:         %{name}-%{version}-path-patch
Patch1:         use_ferror.diff
Patch2:         grub-R
Patch3:         bad-assert-sideeffect
Patch4:         %{name}-gfxmenu-v8.diff
Patch5:         reiser-unpack
Patch6:         chainloader-devicefix
Patch7:         %{name}-%{version}-devicemap.diff
Patch8:         grub-linux-setup-fix
Patch9:         fix-uninitialized
Patch10:        force-LBA-off.diff
Patch11:        gcc4-diff
Patch12:        %{name}-%{version}-initrdaddr.diff
#Patch13:        grub-A20-sysctlportA
Patch13:        http://www.scl.ameslab.gov/Projects/mini-xen/grub-a20.patch
Patch24:        grub-%{version}-protexec.patch
Patch25:	grub-%{version}-chinese.patch
Patch26:	grub-0.97-patch3-ntfs
Patch27:	grub-gcc4.patch
Patch28:	grub-0.97-newext3.patch
Patch29:	850_all_grub-0.97_ext4.patch
Patch30:	grub-0.97-setup.patch
Patch31:        825_all_grub-0.97-automake-pkglib.patch
Patch32:        http://sources.gentoo.org/cgi-bin/viewvc.cgi/gentoo/src/patchsets/grub/0.97/901_all_grub-0.97-fix-gcc46-reboot-issue.patch

ExclusiveArch: i386 x86_64 i686
BuildRequires: binutils >= 2.9.1.0.23, ncurses-devel, texinfo
BuildRequires: automake
PreReq: /sbin/install-info
Requires: mktemp
Requires: /usr/bin/cmp
BuildRoot: %{_tmppath}/%{name}-%{version}-root

%description
GRUB (Grand Unified Boot Loader) is an experimental boot loader
capable of booting into most free operating systems - Linux, FreeBSD,
NetBSD, GNU Mach, and others as well as most commercial operating
systems.

%description -l zh_CN.UTF-8
GRUB (Grand Unified Boot Loader) 是一个专业的引导装载器，它可以引导大
多数自由操作系统 - Linux, FreeBSD, NetBSD, GNU Mach，也可以引导其它大
多数商业操作系统。

%prep
%setup -q
rm -f acconfig.h || true
%patch31 -p1
#%patch0 -p1 -E
%patch1
%patch2 -p1
%patch3 -p1
%patch4
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
# A20 gate haunts even intel macs. Be extra careful,
# see http://www.win.tue.nl/~aeb/linux/kbd/A20.html
%patch13 -p1
%patch24 -p1
%patch25 -p1
%patch26 -p1
%patch27 -p1
%patch28 -p1
%patch29 -p1
%patch30 -p1
%patch32 -p1
# 修正在 automake 1.10 下编译的问题
sed -i 's/AM_INIT_AUTOMAKE/&\nAM_PROG_AS/' configure.ac

%build
autoreconf --install --force
%ifarch x86_64
  EXTRACFLAGS=' -fno-stack-protector -fno-strict-aliasing -minline-all-stringops -m32 -fno-asynchronous-unwind-tables '
%else
  EXTRACFLAGS=' -fno-stack-protector -fno-strict-aliasing -minline-all-stringops'
%endif  
CFLAGS="$RPM_OPT_FLAGS -Os -DNDEBUG -W -Wall -Wpointer-arith $EXTRACFLAGS" ./configure \
  --prefix=/usr --infodir=%{_infodir} --mandir=%{_mandir} --datadir=/usr/lib \
  --disable-auto-linux-mem-opt --enable-diskless \
  --enable-{3c50{3,7},3c5{0,2}9,3c595,3c90x,cs89x0,davicom,depca,eepro{,100},epic100} \
  --enable-{exos205,lance,ne,ne2100,ni{50,52,65}00,ns8390} \
  --enable-{rtl8139,sk-g16,smc9000,tiara,tulip,via-rhine,w89c840,wd}
make OBJCOPY="objcopy -R .note.gnu.build-id"
(cd stage2; mv nbgrub pxegrub ..)
mv stage2/stage2{,.netboot}
make clean
CFLAGS="$RPM_OPT_FLAGS -Os -DNDEBUG -W -Wall -Wpointer-arith $EXTRACFLAGS" ./configure \
  --prefix=/usr --infodir=%{_infodir} --mandir=%{_mandir} --datadir=/usr/lib \
  --disable-auto-linux-mem-opt
make OBJCOPY="objcopy -R .note.gnu.build-id"

%install
[ "$RPM_BUILD_ROOT" != "" -a -d $RPM_BUILD_ROOT ] && rm -rf $RPM_BUILD_ROOT;
make -k DESTDIR=$RPM_BUILD_ROOT install
mkdir -p $RPM_BUILD_ROOT/boot/grub
(cd $RPM_BUILD_ROOT/usr/lib/grub && mv *-suse/* . && rmdir *-suse) >/dev/null 2>&1 || true
cp -p {nb,pxe}grub stage2/stage2{,.netboot} $RPM_BUILD_ROOT/usr/lib/grub
cp -p %{SOURCE2} $RPM_BUILD_ROOT/usr/sbin/. 
cp -p %{SOURCE3} $RPM_BUILD_ROOT/boot/grub/.
rm %{buildroot}%{_infodir}/dir -rf
magic_rpm_clean.sh

%clean
rm -fr $RPM_BUILD_ROOT

%post
# should anything go wrong the system will remain bootable :
[ -e /boot/grub/stage2 ] && mv /boot/grub/stage2{,.old}
# copy especially stage2 over, because it will be modified in-place !
cp -p /usr/lib/grub/*stage1*   /boot/grub 2>/dev/null || true
cp -p /usr/lib/grub/*/*stage1* /boot/grub 2>/dev/null || true
#special hack for #46843
dd if=/usr/lib/grub/stage2 of=/boot/grub/stage2 bs=256k
sync
# command sequence to update-install stage1/stage2.
# leave everything else alone !
[ -e /etc/grub.conf ] && /usr/sbin/grub --batch < /etc/grub.conf >/dev/null 2>&1
/sbin/install-info --info-dir=%{_infodir} %{_infodir}/%{name}.info.gz
/sbin/install-info --info-dir=%{_infodir} %{_infodir}/multiboot.info.gz
exit 0

%preun
if [ "$1" = 0 ] ;then
  /sbin/install-info --delete --info-dir=%{_infodir} %{_infodir}/grub.info.gz
  /sbin/install-info --delete --info-dir=%{_infodir} %{_infodir}/multiboot.info.gz
fi

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog NEWS README COPYING TODO docs/menu.lst
/boot/grub
/usr/sbin/grub
/usr/sbin/grub-install
/usr/sbin/grub-terminfo
/usr/sbin/grub-md5-crypt
/usr/sbin/grub-set-default
/usr/sbin/grubonce
%{_bindir}/mbchk
%{_infodir}/grub*
%{_infodir}/multiboot*
%{_mandir}/man*/*
%{_libdir}/grub/*

%changelog
* Sun Nov 08 2015 Liu Di <liudidi@gmail.com> - 0.97-20
- 为 Magic 3.0 重建

* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 0.97-19
- 为 Magic 3.0 重建

* Fri Apr 11 2014 Liu Di <liudidi@gmail.com> - 0.97-18
- 为 Magic 3.0 重建

* Fri Feb 23 2007 Liu Di <liudidi@gmail.com> - 0.97-11mgc
- readd ntfs support

* Sun Oct 08 2006 Liu Di <liudidi@gmail.com> - 0.97-2mgc
- rebuild, add mactel kbd patch

* Thu May 2 2006 KanKer <kanker@163.com>
- rebuild

* Mon Mar 13 2006 Peter Jones <pjones@redhat.com> - 0.97-5
- Fix merge error for "bootonce" patch (broken in 0.95->0.97 update)
- Get rid of the 0.97 "default" stuff, since it conflicts with our working
  method.

* Mon Mar  9 2006 Peter Jones <pjones@redhat.com> - 0.97-4
- Fix running "install" multiple times on the same fs in the same invocation
  of grub.  (bz #158426 , patch from lxo@redhat.com)

* Mon Feb 13 2006 Peter Jones <pjones@redhat.com> - 0.97-3
- fix partition names on dmraid

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.97-2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Jan 13 2006 Peter Jones <pjones@redhat.com> - 0.97-2
- add dmraid support

* Wed Dec 14 2005 Peter Jones <pjones@redhat.com> - 0.97-1
- update to grub 0.97

* Mon Dec  5 2005 Peter Jones <pjones@redhat.com> - 0.95-17
- fix configure conftest.c bugs
- add -Wno-unused to defeat gcc41 "unused" checking when there are aliases.

* Mon Aug  1 2005 Peter Jones <pjones@redhat.com> - 0.95-16
- minor fix to the --recheck fix.

* Mon Jul 25 2005 Peter Jones <pjones@redhat.com> 0.95-15
- Make "grub-install --recheck" warn the user about how bad it is,
  and keep a backup file, which it reverts to upon detecting some errors.

* Wed Jul  6 2005 Peter Jones <pjones@redhat.com> 0.95-14
- Fix changelog to be UTF-8

* Thu May 19 2005 Peter Jones <pjones@redhat.com> 0.95-13
- Make the spec work with gcc3 and gcc4, so people can test on existing
  installations.
- don't treat i2o like a cciss device, since its partition names aren't done
  that way. (#158158)

* Wed Mar 16 2005 Peter Jones <pjones@redhat.com> 0.95-12
- Make installing on a partition work again when not using raid

* Thu Mar  3 2005 Peter Jones <pjones@redhat.com> 0.95-11
- Make it build with gcc4

* Sun Feb 20 2005 Peter Jones <pjones@redhat.com> 0.95-10
- Always install in MBR for raid1 /boot/

* Sun Feb 20 2005 Peter Jones <pjones@redhat.com> 0.95-9
- Always use full path for mdadm in grub-install

* Tue Feb  8 2005 Peter Jones <pjones@redhat.com> 0.95-8
- Mark the simulation stack executable
- Eliminate the use of inline functions in stage2/builtins.c

* Wed Jan 11 2005 Peter Jones <pjones@redhat.com> 0.95-7
- Make grub ignore everything before the XPM header in the splash image,
  fixing #143879
- If the boot splash image is missing, use console mode instead 
  of graphics mode.
- Don't print out errors using the graphics terminal code if we're not
  actually in graphics mode.

* Mon Jan  3 2005 Peter Jones <pjones@redhat.com> 0.95-6
- reworked much of how the RAID1 support in grub-install works.  This version
  does not require all the devices in the raid to be listed in device.map,
  as long as you specify a physical device or partition rather than an md
  device.  It should also work with a windows dual-boot on the first partition.

* Fri Dec 17 2004 Peter Jones <pjones@redhat.com> 0.95-5
- added support for RAID1 devices to grub-install, partly based on a
  patch from David Knierim. (#114690)

* Tue Nov 30 2004 Jeremy Katz <katzj@redhat.com> 0.95-4
- add patch from upstream CVS to handle sparse files on ext[23]
- make geometry detection a little bit more robust/correct
- use O_DIRECT when reading/writing from devices.  use aligned buffers as 
  needed for read/write (#125808)
- actually apply the i2o patch
- detect cciss/cpqarray devices better (#123249)

* Thu Sep 30 2004 Jeremy Katz <katzj@redhat.com> - 0.95-3
- don't act on the keypress for the menu (#134029)

* Mon Jun 28 2004 Jeremy Katz <katzj@redhat.com> - 0.95-2
- add patch from Nicholas Miell to make hiddenmenu work more 
  nicely with splashimage mode (#126764)

* Fri Jun 18 2004 Jeremy Katz <katzj@redhat.com> - 0.95-1
- update to 0.95
- drop emd patch, E-MD isn't making forward progress upstream
- fix static build for x86_64 (#121095)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun  9 2004 Jeremy Katz <katzj@redhat.com>
- require system-logos (#120837)

* Fri Jun  4 2004 Jeremy Katz <katzj@redhat.com>
- buildrequire automake (#125326)

* Thu May 06 2004 Warren Togami <wtogami@redhat.com> - 0.94-5
- i2o patch from Markus Lidel

* Wed Apr 14 2004 Jeremy Katz <katzj@redhat.com> - 0.94-4
- read geometry off of the disk since HDIO_GETGEO doesn't actually 
  return correct data with a 2.6 kernel

* Fri Mar 12 2004 Jeremy Katz <katzj@redhat.com>
- add texinfo buildrequires (#118146)

* Wed Feb 25 2004 Jeremy Katz <katzj@redhat.com> 0.94-3
- don't use initrd_max_address

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com> 0.94-2
- rebuilt

* Thu Feb 12 2004 Jeremy Katz <katzj@redhat.com> 0.94-1
- update to 0.94, patch merging and updating as necessary

* Sat Jan  3 2004 Jeremy Katz <katzj@redhat.com> 0.93-8
- new bootonce patch from Padraig Brady so that you don't lose 
  the old default (#112775)

* Mon Nov 24 2003 Jeremy Katz <katzj@redhat.com>
- add ncurses-devel as a buildrequires (#110732)

* Tue Oct 14 2003 Jeremy Katz <katzj@redhat.com> 0.93-7
- rebuild

* Wed Jul  2 2003 Jeremy Katz <katzj@redhat.com> 
- Requires: /usr/bin/cmp (#98325)

* Thu May 22 2003 Jeremy Katz <katzj@redhat.com> 0.93-6
- add patch from upstream to fix build with gcc 3.3

* Wed Apr  2 2003 Jeremy Katz <katzj@redhat.com> 0.93-5
- add patch to fix support for serial terminfo (#85595)

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Fri Jan 17 2003 Jeremy Katz <katzj@redhat.com> 0.93-3
- add patch from HJ Lu to support large disks (#80980, #63848)
- add patch to make message when ending edit clearer (#53846)

* Sun Dec 29 2002 Jeremy Katz <katzj@redhat.com> 0.93-2
- add a patch to reset the terminal type to console before doing 'boot' from
  the command line (#61069)

* Sat Dec 28 2002 Jeremy Katz <katzj@redhat.com> 0.93-1
- update to 0.93
- update configfile patch
- graphics patch rework to fit in as a terminal type as present in 0.93
- use CFLAGS="-Os -g"
- patch configure.in to allow building if host_cpu=x86_64, include -m32 in
  CFLAGS if building on x86_64
- link glibc static on x86_64 to not require glibc32
- include multiboot info pages
- drop obsolete patches, reorder remaining patches into some semblance of order

* Thu Sep  5 2002 Jeremy Katz <katzj@redhat.com> 0.92-7
- splashscreen is in redhat-logos now

* Tue Sep  3 2002 Jeremy Katz <katzj@redhat.com> 0.92-6
- update splashscreen again

* Mon Sep  2 2002 Jeremy Katz <katzj@redhat.com> 0.92-5
- update splashscreen

* Fri Jun 21 2002 Tim Powers <timp@redhat.com> 0.92-4
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com> 0.92-3
- automated rebuild

* Fri May  3 2002 Jeremy Katz <katzj@redhat.com> 0.92-2
- add patch from Grant Edwards to make vga16 + serial happier (#63491)

* Wed May  1 2002 Jeremy Katz <katzj@redhat.com> 0.92-1
- update to 0.92
- back to autoreconf
- make it work with automake 1.6/autoconf 2.53
- use "-falign-jumps=1 -falign-loops=1 -falign-functions=1" instead of
  "-malign-jumps=1 -malign-loops=1 -malign-functions=1"	to not use 
  deprecated gcc options

* Tue Apr  9 2002 Jeremy Katz <katzj@redhat.com> 0.91-4
- new splash screen

* Fri Mar  8 2002 Jeremy Katz <katzj@redhat.com> 0.91-3
- include patch from Denis Kitzmen to fix typo causing several options to 
  never be defined (in upstream CVS)
- include patch from upstream CVS to make displaymem always use hex for 
  consistency
- add patch from GRUB mailing list from Keir Fraser to add a --once flag to
  savedefault function so that you can have the equivalent of lilo -R 
  functionality (use 'savedefault --default=N --once' from the grub shell)
- back to autoconf

* Sun Jan 27 2002 Jeremy Katz <katzj@redhat.com> 
- change to use $grubdir instead of /boot/grub in the symlink patch (#58771)

* Fri Jan 25 2002 Jeremy Katz <katzj@redhat.com> 0.91-2
- don't ifdef out the auto memory passing, use the configure flag instead
- add a patch so that grub respects mem= from the kernel command line when 
  deciding where to place the initrd (#52558)

* Mon Jan 21 2002 Jeremy Katz <katzj@redhat.com> 0.91-1
- update to 0.91 final
- add documentation on splashimage param (#51609)

* Wed Jan  2 2002 Jeremy Katz <katzj@redhat.com> 0.91-0.20020102cvs
- update to current CVS snapshot to fix some of the hangs on boot related
  to LBA probing (#57503, #55868, and others)

* Fri Dec 21 2001 Erik Troan <ewt@redhat.com> 0.90-14
- fixed append patch to not require arguments to begin with
- changed to autoreconf from autoconf

* Wed Oct 31 2001 Jeremy Katz <katzj@redhat.com> 0.90-13
- include additional patch from Erich to add sync calls in grub-install to 
  work around updated images not being synced to disk
- fix segfault in grub shell if 'password --md5' is used without specifying
  a password (#55008)

* Fri Oct 26 2001 Jeremy Katz <katzj@redhat.com> 0.90-12
- Include Erich Boleyn <erich@uruk.org>'s patch to disconnect from the 
  BIOS after APM operations.  Should fix #54375

* Wed Sep 12 2001 Erik Troan <ewt@redhat.com>
- added patch for 'a' option in grub boot menu

* Wed Sep  5 2001 Jeremy Katz <katzj@redhat.com> 0.90-11
- grub-install: if /boot/grub/grub.conf doesn't exist but /boot/grub/menu.lst 
  does, create a symlink

* Fri Aug 24 2001 Jeremy Katz <katzj@redhat.com>
- pull in patch from upstream CVS to fix md5crypt in grub shell (#52220)
- use mktemp in grub-install to avoid tmp races

* Fri Aug  3 2001 Jeremy Katz <katzj@redhat.com>
- link curses statically (#49519)

* Thu Aug  2 2001 Jeremy Katz <katzj@redhat.com>
- fix segfault with using the serial device before initialization (#50219)

* Thu Jul 19 2001 Jeremy Katz <katzj@redhat.com>
- add --copy-only flag to grub-install

* Thu Jul 19 2001 Jeremy Katz <katzj@redhat.com>
- copy files in grub-install prior to device probe

* Thu Jul 19 2001 Jeremy Katz <katzj@redhat.com>
- original images don't go in /boot and then grub-install does the right
  thing

* Thu Jul 19 2001 Jeremy Katz <katzj@redhat.com>
- fix the previous patch
- put the password prompt in the proper location

* Thu Jul 19 2001 Jeremy Katz <katzj@redhat.com>
- reset the screen when the countdown is cancelled so text will disappear 
  in vga16 mode

* Mon Jul 16 2001 Jeremy Katz <katzj@redhat.com>
- change configfile defaults to grub.conf

* Sun Jul 15 2001 Jeremy Katz <katzj@redhat.com>
- updated to grub 0.90 final

* Fri Jul  6 2001 Matt Wilson <msw@redhat.com>
- modifed splash screen to a nice shade of blue

* Tue Jul  3 2001 Matt Wilson <msw@redhat.com>
- added a first cut at a splash screen

* Sun Jul  1 2001 Nalin Dahyabhai <nalin@redhat.com>
- fix datadir mismatch between build and install phases

* Mon Jun 25 2001 Jeremy Katz <katzj@redhat.com>
- update to current CVS 
- forward port VGA16 patch from Paulo C茅sar Pereira de 
  Andrade <pcpa@conectiva.com.br>
- add patch for cciss, ida, and rd raid controllers
- don't pass mem= to the kernel

* Wed May 23 2001 Erik Troan <ewt@redhat.com>
- initial build for Red Hat
