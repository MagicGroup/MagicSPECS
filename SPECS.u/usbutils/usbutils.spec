Name:    usbutils
Summary: Linux USB utilities
Summary(zh_CN.UTF-8): Linux 下的 USB 工具
Version: 008
Release: 7%{?dist}
URL:     http://www.linux-usb.org/
License: GPLv2+
Group:   Applications/System
Group(zh_CN.UTF-8): 应用程序/系统

Source0: https://www.kernel.org/pub/linux/utils/usb/usbutils/%{name}-%{version}.tar.xz

#Path to usb.ids in lsusb.py should be with /hwdata/
Patch0: usbutils-006-hwdata.patch

BuildRequires: libusbx-devel
BuildRequires: systemd-devel
Requires: hwdata

%description
This package contains utilities for inspecting devices connected to a
USB bus.

%description -l zh_CN.UTF-8
Linux 下的 USB 工具，用来发现连接到 USB 总线的设备。

%prep
%setup -q
%patch0 -p1

%build
%configure --sbindir=%{_sbindir} --datadir=%{_datadir}/hwdata --disable-usbids
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
magic_rpm_clean.sh

%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc AUTHORS NEWS README
%{_mandir}/*/*
%{_bindir}/*
%{_datadir}/pkgconfig/usbutils.pc

%changelog
* Sat Nov 14 2015 Liu Di <liudidi@gmail.com> - 008-7
- 为 Magic 3.0 重建

* Thu Nov 05 2015 Liu Di <liudidi@gmail.com> - 008-6
- 为 Magic 3.0 重建

* Sat Oct 17 2015 Liu Di <liudidi@gmail.com> - 008-5
- 为 Magic 3.0 重建

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 005-2
- 为 Magic 3.0 重建

* Thu Apr 19 2012 Lukas Nykryn <lnykryn@redhat.com> 005-1
- new upstream release

* Thu Apr 19 2012 Lukas Nykryn <lnykryn@redhat.com> 004-4
- Ignore missing driver symlink (#808934)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 004-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Aug 20 2011 Lukas Nykryn <lnykryn@redhat.com> 004-2
- fixed paths to usb.ids 

* Sat Aug 13 2011 Jiri Moskovcak <jmoskovc@redhat.com> 004-1
- new upstream release
- dropepd config descriptor patch, it's included in upstream version

* Thu Aug 11 2011 Jiri Moskovcak <jmoskovc@redhat.com> 003-3
- fixed path to usb.ids in lsusb.py rhbz#729903

* Mon Jun 27 2011 Nils Philippsen <nils@redhat.com> 003-2
- don't use invalid config descriptors (#707853)

* Thu Jun 16 2011 Jiri Moskovcak <jmoskovc@redhat.com> 003-1
- new upstream release

* Tue Apr 26 2011 Jiri Moskovcak <jmoskovc@redhat.com> 002-1
- new upstream release
- udpated hwdata patch

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 001-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 27 2011 Jiri Moskovcak <jmoskovc@redhat.com> 001-2
- rebuild against new libusb

* Thu Jan 06 2011 Jiri Moskovcak <jmoskovc@redhat.com> 001-1
- new upstream release
- updated usbhid-dump subproject
- usbutils: Support UVC frame-based descriptors
- usbutils: Support UVC MPEG2-TS format descriptor
- lsusb: Fix getting BOS and DEVQUAL descriptors
- lsusb: Dump the Pipe Usage desciptor
- lsusb: Fix bMaxBurst reporting
- lsusb: install into /usr/bin
- usbmisc: pull in unistd.h for readlink()
- lsusb: pull in stdlib.h for exit()
- lsusb: constify!
- usbutils: convert to libusb-1.0
- Update usbhid-dump to release 1.2
- usbutils: Fix compile error on Ubuntu 9.04
- usbutils: Make lsusb -t show USB 3.0 devices

* Wed Oct 27 2010 Jiri Moskovcak <jmoskovc@redhat.com> 0.91-2
- bump release

* Wed Oct 27 2010 Jiri Moskovcak <jmoskovc@redhat.com> 0.91-1
- new upstream release
  - ads usbhid-dump

* Thu Aug 26 2010 Jiri Moskovcak <jmoskovc@redhat.com> 0.90-1
- new upstream release

* Tue Sep 22 2009  Jiri Moskovcak <jmoskovc@redhat.com> 0.86-2
- spec file fixes - package should not own /usr/{bin,sbin} (rhbz#524005)

* Wed Sep 16 2009  Jiri Moskovcak <jmoskovc@redhat.com> 0.86-1
- new version
- spec file fixes as suggested in rhbz#466041 (info@owlriver.com)

* Mon Aug 24 2009 Karsten Hopp <karsten@redhat.com> 0.82-5
- drop ExcludeArch: s390 s390x as we need this package on s390x to be able to build
  p.e. udev without any hacks

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.82-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul  1 2009  Jiri Moskovcak <jmoskovc@rdhat.com> 0.82-3
- added autoconf to fix build in koji

* Wed Jul  1 2009  Jiri Moskovcak <jmoskovc@redhat.com> 0.82-2
- minor fix in Makefile.am to properly find usb.ids from hwdata
- Resolves: #506974

* Fri May 22 2009 David Zeuthen <davidz@redhat.com> 0.82-1
- Update to 0.82

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.73-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 12 2008 Jiri Moskovcak <jmoskovc@redhat.com> 0.73-2
- spec file cleanup

* Thu Jan 17 2008 Jiri Moskovcak <jmoskovc@redhat.com> 0.73-1
- new version 0.73

* Mon Sep 18 2006 Thomas Woerner <twoerner@redhat.com> 0.72-1
- new version 0.72
- videoterminal (vt) patch is now upstream, dropped

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.71-2.1
- rebuild

* Wed Mar 01 2006 Karsten Hopp <karsten@redhat.de> 1.71-2
- add usbutils-0.71-VT.patch to fix warnings about unknown lines
  (#176903)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.71-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.71-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Dec 13 2005 Thomas Woerner <twoerner@redhat.com> 0.71-1
- new version 0.71

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Apr 15 2005 Thomas Woerner <twoerner@redhat.com> 0.70-1.1
- added fix from Robert Scheck to fix missing BuildRequires for libusb-devel
 (#155006)

* Thu Apr 14 2005 Thomas Woerner <twoerner@redhat.com> 0.70-1
- new version 0.70

* Thu Jan 20 2005 David Woodhouse <dwmw2@redhat.com> 0.11-6.2
- Don't byteswap parts of device descriptor which kernel already swapped

* Mon Sep 13 2004 Thomas Woerner <twoerner@redhat.com> 0.11-6.1
- added missing BuildRequires for libtool (#132406)

* Wed Sep  1 2004 Thomas Woerner <twoerner@redhat.com> 0.11-6
- added patch from Aurelien Jarno for unknown HID Country Code entries in
  usb.ids (#127415)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue May  4 2004 Bill Nottingham <notting@redhat.com> 0.11-4
- add patch from USB maintainer to fix various brokenness (#115694, <david-b@pacbell.net>)

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun  3 2003 Jeff Johnson <jbj@redhat.com>
- add explicit epoch's where needed.

* Mon May 19 2003 Bill Nottingham <notting@redhat.com> 0.11-1
- update to 0.11, fixes #90640
- add patch to fix some warnings (#78462, <d.binderman@virgin.net>)

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Fri Nov 29 2002 Tim Powers <timp@redhat.com> 0.9-9
- remove unpackaged files from the buildroot

* Wed Nov 20 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- exclude mainframe

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Mar 21 2002 Trond Eivind Glomsrød <teg@redhat.com> 0.9-5
- Fix conflict check

* Mon Mar 18 2002 Trond Eivind Glomsrød <teg@redhat.com> 0.9-4
- Conflict with older versions of hotplug which contained
  parts of this package (#60615)

* Fri Feb 22 2002 Trond Eivind Glomsrød <teg@redhat.com> 0.9-3
- Rebuild

* Wed Jan 30 2002 Bill Nottingham <notting@redhat.com> 0.9-2
- require hwdata

* Wed Jan 16 2002 Trond Eivind Glomsrød <teg@redhat.com> 0.9-1
- Initial RPM
- make it build on ia64

