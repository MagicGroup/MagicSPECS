Summary: Simple kernel loader which boots from a FAT filesystem
Name: syslinux
Version: 6.03
%define tarball_version 6.03
Release: 5%{?dist}
License: GPLv2+
Group: Applications/System
URL: http://syslinux.zytor.com/wiki/index.php/The_Syslinux_Project
Source0: http://www.kernel.org/pub/linux/utils/boot/syslinux/%{name}-%{tarball_version}.tar.xz
Patch0001: 0001-Add-install-all-target-to-top-side-of-HAVE_FIRMWARE.patch
# Backport from upstream git master to fix RHBZ #1234653
Patch0002: 0035-SYSAPPEND-Fix-space-stripping.patch

# this is to keep rpmbuild from thinking the .c32 / .com / .0 / memdisk files
# in noarch packages are a reason to stop the build.
%define _binaries_in_noarch_packages_terminate_build 0

ExclusiveArch: %{ix86} x86_64
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: nasm >= 0.98.38-1, perl, netpbm-progs, git
BuildRequires: /usr/include/gnu/stubs-32.h
BuildRequires: libuuid-devel
Requires: syslinux-nonlinux = %{version}-%{release}
%ifarch %{ix86}
Requires: mtools, libc.so.6
BuildRequires: mingw32-gcc
%endif
%ifarch x86_64
Requires: mtools, libc.so.6()(64bit)
BuildRequires: mingw64-gcc
%endif

# NOTE: extlinux belongs in /sbin, not in /usr/sbin, since it is typically
# a system bootloader, and may be necessary for system recovery.
%define _sbindir /sbin

%description
SYSLINUX is a suite of bootloaders, currently supporting DOS FAT
filesystems, Linux ext2/ext3 filesystems (EXTLINUX), PXE network boots
(PXELINUX), or ISO 9660 CD-ROMs (ISOLINUX).  It also includes a tool,
MEMDISK, which loads legacy operating systems from these media.

%package perl
Summary: Syslinux tools written in perl
Group: Applications/System

%description perl
Syslinux tools written in perl

%package devel
Summary: Headers and libraries for syslinux development.
Group: Development/Libraries
Provides: %{name}-static = %{version}-%{release}

%description devel
Headers and libraries for syslinux development.

%package extlinux
Summary: The EXTLINUX bootloader, for booting the local system.
Group: System/Boot
Requires: syslinux
Requires: syslinux-extlinux-nonlinux = %{version}-%{release}

%description extlinux
The EXTLINUX bootloader, for booting the local system, as well as all
the SYSLINUX/PXELINUX modules in /boot.

%ifarch %{ix86}
%package tftpboot
Summary: SYSLINUX modules in /tftpboot, available for network booting
Group: Applications/Internet
BuildArch: noarch
ExclusiveArch: %{ix86} x86_64
Requires: syslinux

%description tftpboot
All the SYSLINUX/PXELINUX modules directly available for network
booting in the /tftpboot directory.

%package extlinux-nonlinux
Summary: The parts of the EXTLINUX bootloader which aren't run from linux.
Group: System/Boot
Requires: syslinux
BuildArch: noarch
ExclusiveArch: %{ix86} x86_64

%description extlinux-nonlinux
All the EXTLINUX binaries that run from the firmware rather than
from a linux host.

%package nonlinux
Summary: SYSLINUX modules which aren't run from linux.
Group: System/Boot
Requires: syslinux
BuildArch: noarch
ExclusiveArch: %{ix86} x86_64

%description nonlinux
All the SYSLINUX binaries that run from the firmware rather than from a
linux host. It also includes a tool, MEMDISK, which loads legacy operating
systems from media.
%endif

%ifarch %{x86_64}
%package efi64
Summary: SYSLINUX binaries and modules for 64-bit UEFI systems
Group: System/Boot

%description efi64
SYSLINUX binaries and modules for 64-bit UEFI systems
%endif

%prep
%setup -q -n syslinux-%{tarball_version}
git init
git config user.email "%{name}-owner@fedoraproject.org"
git config user.name "Fedora Ninjas"
git add .
git commit -a -q -m "%{version} baseline."
git am %{patches} </dev/null

%build
make bios clean all
%ifarch %{x86_64}
make efi64 clean all
%endif

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_prefix}/lib/syslinux
mkdir -p %{buildroot}%{_includedir}
make bios install-all \
	INSTALLROOT=%{buildroot} BINDIR=%{_bindir} SBINDIR=%{_sbindir} \
	LIBDIR=%{_prefix}/lib DATADIR=%{_datadir} \
	MANDIR=%{_mandir} INCDIR=%{_includedir} \
	TFTPBOOT=/tftpboot EXTLINUXDIR=/boot/extlinux \
	LDLINUX=ldlinux.c32
%ifarch %{x86_64}
make efi64 install netinstall \
	INSTALLROOT=%{buildroot} BINDIR=%{_bindir} SBINDIR=%{_sbindir} \
	LIBDIR=%{_prefix}/lib DATADIR=%{_datadir} \
	MANDIR=%{_mandir} INCDIR=%{_includedir} \
	TFTPBOOT=/tftpboot EXTLINUXDIR=/boot/extlinux \
	LDLINUX=ldlinux.c32
%endif

mkdir -p %{buildroot}/%{_docdir}/%{name}/sample
install -m 644 sample/sample.* %{buildroot}/%{_docdir}/%{name}/sample/
mkdir -p %{buildroot}/etc
( cd %{buildroot}/etc && ln -s ../boot/extlinux/extlinux.conf . )

# don't ship libsyslinux, at least, not for now
rm -f %{buildroot}%{_prefix}/lib/libsyslinux*
rm -f %{buildroot}%{_includedir}/syslinux.h

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc NEWS README*
%doc doc/* 
%doc sample
%{_mandir}/man1/gethostip*
%{_mandir}/man1/syslinux*
%{_mandir}/man1/extlinux*
%{_mandir}/man1/isohybrid*
%{_mandir}/man1/memdiskfind*
%{_bindir}/gethostip
%{_bindir}/isohybrid
%{_bindir}/memdiskfind
%{_bindir}/syslinux
%dir %{_datadir}/syslinux
%dir %{_datadir}/syslinux/dosutil
%{_datadir}/syslinux/dosutil/*
%{_datadir}/syslinux/diag/*
%ifarch %{ix86}
%{_datadir}/syslinux/syslinux.exe
%else
%{_datadir}/syslinux/syslinux64.exe
%endif

%files perl
%defattr(-,root,root)
%{!?_licensedir:%global license %%doc}
%license COPYING
%{_mandir}/man1/lss16toppm*
%{_mandir}/man1/ppmtolss16*
%{_mandir}/man1/syslinux2ansi*
%{_bindir}/keytab-lilo
%{_bindir}/lss16toppm
%{_bindir}/md5pass
%{_bindir}/mkdiskimage
%{_bindir}/ppmtolss16
%{_bindir}/pxelinux-options
%{_bindir}/sha1pass
%{_bindir}/syslinux2ansi
%{_bindir}/isohybrid.pl

%files devel
%defattr(-,root,root)
%{!?_licensedir:%global license %%doc}
%license COPYING
%dir %{_datadir}/syslinux/com32
%{_datadir}/syslinux/com32

%files extlinux
%{_sbindir}/extlinux
%config /etc/extlinux.conf

%ifarch %{ix86}
%files tftpboot
/tftpboot

%files nonlinux
%{_datadir}/syslinux/*.com
%{_datadir}/syslinux/*.exe
%{_datadir}/syslinux/*.c32
%{_datadir}/syslinux/*.bin
%{_datadir}/syslinux/*.0
%{_datadir}/syslinux/memdisk

%files extlinux-nonlinux
/boot/extlinux

%else
%exclude %{_datadir}/syslinux/memdisk
%exclude %{_datadir}/syslinux/*.com
%exclude %{_datadir}/syslinux/*.exe
%exclude %{_datadir}/syslinux/*.c32
%exclude %{_datadir}/syslinux/*.bin
%exclude %{_datadir}/syslinux/*.0
%exclude /boot/extlinux
%exclude /tftpboot
%endif

%ifarch %{x86_64}
%files efi64
%{!?_licensedir:%global license %%doc}
%license COPYING
%dir %{_datadir}/syslinux/efi64
%{_datadir}/syslinux/efi64
%endif

%post extlinux
# If we have a /boot/extlinux.conf file, assume extlinux is our bootloader
# and update it.
if [ -f /boot/extlinux/extlinux.conf ]; then \
	extlinux --update /boot/extlinux ; \
elif [ -f /boot/extlinux.conf ]; then \
	mkdir -p /boot/extlinux && \
	mv /boot/extlinux.conf /boot/extlinux/extlinux.conf && \
	extlinux --update /boot/extlinux ; \
fi

%changelog
* Fri Jul 03 2015 Adam Williamson <awilliam@redhat.com> - 6.03-5
- backport a commit from git master which appears to fix RHBZ #1234653

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.03-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 6.03-3
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Sat Jan 10 2015 Michael Schwendt <mschwendt@fedoraproject.org> - 6.03-2
- Add -static Provides to -devel package to meet Fedora's
  Packaging Static Libraries guidelines (rhbz #609617)

* Wed Oct 08 2014 Peter Jones <pjones@redhat.com> - 6.03-1
- Update to 6.03

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.02-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Aug  5 2014 Tom Callaway <spot@fedoraproject.org> - 6.02-6
- fix license handling

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.02-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 15 2014 Peter Jones <pjones@redhat.com> - 6.02-4
- Do our firmware/nonlinux packages as .noarch + ExclusiveArch
  Related: rhbz#1086446

* Tue Apr 15 2014 Peter Jones <pjones@redhat.com> - 6.02-3
- -2 was entirely the wrong thing to do.

* Tue Apr 15 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> - 6.02-2
- Undo packaging changes that break live image composes (#1086446)

* Tue Apr 08 2014 Peter Jones <pjones@redhat.com> - 6.02-1
- Update this to 6.02

* Mon Aug 05 2013 Peter Jones <pjones@redhat.com> - 4.05-7
- Fixing %%doc path.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.05-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 4.05-6
- Perl 5.18 rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.05-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Aug 06 2012 Peter Jones <pjones@redhat.com> - 4.05-4
- Fix build problem from kernel-headers' removeal of ext2_fs.h
  (fix backported from as-yet-unreleased upstream version.)

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.05-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Apr 18 2012 Michael Schwendt <mschwendt@fedoraproject.org> - 4.05-2
- Remove old Obsoletes/Provides for syslinux-devel as such a subpkg
  was introduced with 3.83-2 (#756733).

* Wed Feb 15 2012 Matthew Garrett <mjg@redhat.com> - 4.05-1
- New upstream release
- syslinux-isohybrid-fix-mbr.patch: generate a full MBR for UEFI images

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.02-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Aug 24 2011 Matthew Garrett <mjg@redhat.com> - 4.02-5
- Add support for building Mac and GPT bootable hybrid images

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.02-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Aug 20 2010 Matt Domsch <mdomsch@fedoraproject.org> - 4.02-2
- add perl subpackage, move perl apps there

* Fri Aug 06 2010 Peter Jones <pjones@redhat.com> - 4.02-2
- Split out extlinux and tftpboot.
- remove duplicate syslinux/com32/ left in base package after 3.83-2

* Thu Aug 05 2010 Peter Jones <pjones@redhat.com> - 4.02-1
- Update to 4.02

* Mon Jan 11 2010 Peter Jones <pjones@redhat.com> - 3.84-1
- Update to 3.84

* Thu Dec 17 2009 Peter Jones <pjones@redhat.com> - 3.83-2
- Split out -devel

* Thu Oct 29 2009 Peter Jones <pjones@redhat.com> - 3.83-1
- update to 3.83

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.75-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Apr 28 2009 Jeremy Katz <katzj@redhat.com> - 3.75-3
- Stop suppressing requirements of the package (#465299)

* Tue Apr 28 2009 Jeremy Katz <katzj@redhat.com> - 3.75-2
- Don't strip binaries to fix debuginfo (#249970)

* Thu Apr 16 2009 Jeremy Katz <katzj@redhat.com> - 3.75-1
- update to 3.75

* Fri Apr 10 2009 Jeremy Katz <katzj@redhat.com> - 3.74-1
- update to 3.74

* Fri Feb 27 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 3.73-2
- fix arch issues 

* Fri Feb 27 2009 Jeremy Katz <katzj@redhat.com> - 3.73-1
- Update to 3.73

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.61-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Sep  6 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 3.61-3
- fix license tag

* Mon Feb 25 2008 Peter Jones <pjones@redhat.com> - 3.61-2
- Remove 16bpp patch, hpa says that's there to cover a bug that's fixed.
- Remove x86_64 patch; building without it works now.

* Thu Feb 21 2008 Peter Jones <pjones@redhat.com> - 3.61-1
- Update to 3.61 .

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.36-9
- Autorebuild for GCC 4.3

* Wed Jan 09 2008 Florian La Roche <laroche@redhat.com> - 3.36-8
- spec in utf-8
- add URL tag
- own /usr/share/syslinux (rhbz#427816)

* Wed Oct 17 2007 Peter Jones <pjones@redhat.com> - 3.36-7
- Add necessary files for makebootfat to make usb images (patch from
  Joel Granados <jgranado@redhat.com>)

* Wed Oct  3 2007 Jeremy Katz <katzj@redhat.com> - 3.36-6
- fix menu system memory corruption (#239585)

* Tue Aug 14 2007 Jeremy Katz <katzj@redhat.com> - 3.36-5
- backport "menu hidden" support from upstream git

* Fri May  4 2007 Jeremy Katz <katzj@redhat.com> - 3.36-4
- switch to preferring 16bpp for graphical menu; this fixes the display for 
  qemu, kvm, etc

* Tue May  1 2007 Jeremy Katz <katzj@redhat.com> - 3.36-3
- fix countdown on boot images (#229491)

* Tue Apr 03 2007 Florian La Roche <laroche@redhat.com> - 3.36-2
- add upstream patch from 3.3x branch

* Mon Feb 12 2007 Florian La Roche <laroche@redhat.com> - 3.36-1
- update to 3.36

* Thu Feb 08 2007 Florian La Roche <laroche@redhat.com> - 3.35-1
- update to 3.35

* Thu Jan 18 2007 Jesse Keating <jkeating@redhat.com> - 3.31-2
- Make syslinux own /usr/lib/syslinux.

* Wed Jan 17 2007 Jeremy Katz <katzj@redhat.com> - 3.31-1
- update to 3.31

* Tue Aug 22 2006 Jesse Keating <jkeating@redhat.com> - 3.11-4
- Obsolete syslinux-devel.
- Couple cleanups for packaging guidelines

* Fri Jul 14 2006 David Cantrell <dcantrell@redhat.com> - 3.11-3
- Remove com32/include/time.h and com32/include/sys/times.h
- Replace CLK_TCK macros with CLOCKS_PER_SEC

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 3.11-2.1
- rebuild

* Mon Jun 12 2006 Peter Jones <pjones@redhat.com> - 3.11-2
- Fold -devel subpackage into "syslinux"

* Mon Jun 05 2006 Jesse Keating <jkeating@redhat.com> - 3.10-5
- Use the actual file as a BuildRequire

* Mon Jun 05 2006 Jesse Keating <jkeating@redhat.com> - 3.10-4
- Changed glibc-devel to glibc32 to get the 32bit package in

* Mon Jun 05 2006 Jesse Keating <jkeating@redhat.com> - 3.10-3
- Added missing glibc-devel BuildRequires

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 3.10-2.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Aug 22 2005 Peter Jones <pjones@redhat.com> - 3.10-2
- Update to 3.10
- Don't do "make clean", so we actually ship the bins hpa gives us

* Sat Jul  9 2005 Peter Jones <pjones@redhat.com> - 3.09-2
- Update to 3.09

* Thu Jun 16 2005 Peter Jones <pjones@redhat.com> - 3.08.92-1
- Update to 3.09-pre2, to fix the i915 .bss overflow bug

* Thu May 19 2005 Peter Jones <pjones@redhat.com> - 3.08-3
- Fix filespec for samples in -devel

* Thu May 19 2005 Peter Jones <pjones@redhat.com> - 3.08-2
- update to 3.08

* Wed Mar 16 2005 Peter Jones <pjones@redhat.com> - 3.07-2
- gcc4 update

* Thu Jan 13 2005 Peter Jones <pjones@redhat.com> - 3.07-1
- update to 3.07

* Tue Jan 11 2005 Peter Jones <pjones@redhat.com> - 3.06-1
- update to 3.06 , which should fix the directory parsing bug that wedges it
  with diskboot.img
- change README to README* in doc, to include README.menu and README.usbkey

* Tue Jan  4 2005 Peter Jones <pjones@redhat.com> - 3.02-2
- Beehive doesn't let you build in scratch and then build someplace else,
  arrrrgh.

* Tue Jan  4 2005 Peter Jones <pjones@redhat.com> - 3.02-1
- 3.02
- Make the spec a little closer to hpa's.

* Mon Jan  3 2005 Peter Jones <pjones@redhat.com> - 3.00-2
- make tag says the tag is there, make build says it's not.
  Bump release, try again.

* Mon Jan  3 2005 Peter Jones <pjones@redhat.com> - 3.00-1
- 3.00

* Mon Aug 16 2004 Jeremy Katz <katzj@redhat.com> - 2.11-1
- 2.11

* Fri Jul 30 2004 Jeremy Katz <katzj@redhat.com> - 2.10-1
- update to 2.10

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sat Apr 17 2004 Jeremy Katz <katzj@redhat.com> 2.0.8-3
- add syslinux-nomtools binary to be used for creating some installer images

* Tue Feb 17 2004 Jeremy Katz <katzj@redhat.com> 
- add netpbm-progs BuildRequires (#110255)

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sun Dec 14 2003 Jeremy Katz <katzj@redhat.com> 2.08-1
- 2.08

* Fri Aug 22 2003 Jeremy Katz <katzj@redhat.com> 2.06-1
- 2.06

* Thu Aug 14 2003 Jeremy Katz <katzj@redhat.com> 2.05-1
- update to 2.05

* Mon Apr 21 2003 Jeremy Katz <katzj@redhat.com> 2.04-2
- add patch for samples to build on x86_64
- integrate some changes from upstream specfile (#88593)

* Fri Apr 18 2003 Jeremy Katz <katzj@redhat.com> 2.04-1
- update to 2.04

* Mon Feb  3 2003 Jeremy Katz <katzj@redhat.com> 2.01-1
- update to 2.01

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Jan 14 2003 Jeremy Katz <katzj@redhat.com> 2.00-3
- fix deps for x86_64

* Wed Nov 27 2002 Tim Powers <timp@redhat.com> 2.00-2
- build on both x86_64 and i386

* Fri Nov  1 2002 Jeremy Katz <katzj@redhat.com>
- update to 2.00
- add additional files as requested by hpa (#68073)

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Jun 18 2002 Jeremy Katz <katzj@redhat.com>
- lss16toppm and ppmtolss16 are both perl scripts... turn off find-requires
  so we don't suck in perl as a dependency for syslinux

* Mon Jun 17 2002 Jeremy Katz <katzj@redhat.com>
- update to 1.75
- include tools to create graphical image format needed by syslinux
- include isolinux 
- include pxelinux (#64942)

* Fri Jun 14 2002 Preston Brown <pbrown@redhat.com>
- upgrade to latest version w/graphical screen support

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Sat Feb 10 2001 Matt Wilson <msw@redhat.com>
- 1.52

* Wed Jan 24 2001 Matt Wilson <msw@redhat.com>
- 1.51pre7

* Mon Jan 22 2001 Matt Wilson <msw@redhat.com>
- 1.51pre5

* Fri Jan 19 2001 Matt Wilson <msw@redhat.com>
- 1.51pre3, with e820 detection

* Tue Dec 12 2000 Than Ngo <than@redhat.com>
- rebuilt with fixed fileutils

* Thu Nov 9 2000 Than Ngo <than@redhat.com>
- update to 1.49
- update ftp site
- clean up specfile
- add some useful documents

* Tue Jul 18 2000 Nalin Dahyabhai <nalin@redhat.com>
- add %%defattr (release 4)

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Thu Jul 06 2000 Trond Eivind Glomsrød <teg@redhat.com>
- use %%{_tmppath}
- change application group (Applications/Internet doesn't seem
  right to me)
- added BuildRequires

* Tue Apr 04 2000 Erik Troan <ewt@redhat.com>
- initial packaging
