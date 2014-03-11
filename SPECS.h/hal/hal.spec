%define expat_version           1.95.5
%define glib2_version           2.6.0
%define dbus_version            0.70
%define pygtk2			2.0.0
%define gnome_python2		2.0.0
%define udev_version            057-3
%define util_linux_version      2.12a-16
%define doxygen_version         1.3.9.1-1
%define initscripts_version     8.04-1
%define kernel_version          2.6.11
%define gettext_version	        0.14.1-14
%define libusb_version          0.1.10a-1
%define cryptsetup_luks_version 1.0.1-2

%define hal_user_uid           68
%define use_pmount		1
%define relver	0.5.9
%define rcver rc1
%define gitdate 20121225
%define git 1

Summary: Hardware Abstraction Layer
Summary(zh_CN.UTF-8): 硬件抽象层
Name: hal
Version: 0.5.15
%if 0%{git}
Release: 0.git%{gitdate}1%{?dist}
%else
Release: 5%{?dist}
%endif
URL: http://www.freedesktop.org/Software/hal
%if 0%{git}
Source0: %{name}-git%{gitdate}.tar.xz
%else
Source0: %{name}-%{version}.tar.bz2
%endif
Source1: make_hal_git_package.sh
Patch1: hal-policy-magic.patch
Patch2:	hal-0.5.13-label.patch
Patch5: hal-0.5.8.1-mount_point.patch
Patch6: hal-normaluser.patch
Patch7:	hal-dontzap.patch
Patch8:	hal-volume.patch
Patch9: hal-newglib.patch
License: AFL/GPL
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
BuildRoot: %{_tmppath}/%{name}-root
PreReq: chkconfig
BuildRequires: expat-devel >= %{expat_version}
BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: dbus-devel  >= %{dbus_version}
BuildRequires: python-devel
BuildRequires: hwdata
BuildRequires: doxygen >= %{doxygen_version}
BuildRequires: gettext >= %{gettext_version}
%ifnarch s390 s390x
BuildRequires: libusb-devel >= %{libusb_version}
%endif
Requires: dbus >= %{dbus_version}
Requires: dbus-glib >= %{dbus_version}
Requires: glib2 >= %{glib2_version}
Requires: udev >= %{udev_version} 
Requires: util-linux >= %{util_linux_version} 
Requires: initscripts >= %{initscripts_version}
#Requires: cryptsetup-luks >= %{cryptsetup_luks_version}
Conflicts: kernel < %{kernel_version}
%ifnarch s390 s390x
Requires: libusb >= %{libusb_version}
%endif

%description

HAL is daemon for collection and maintaining information from several
sources about the hardware on the system. It provdes a live device
list through D-BUS.

%description -l zh_CN.UTF-8
HAL是一个从几个来源收集和维护系统上的硬件信息的服务。它通过D-BUS提供了
实时设备列表。

%package devel
Summary: Libraries and headers for HAL
Summary(zh_CN.UTF-8): HAL的库和头文件
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %name = %{version}-%{release}
Requires: dbus-devel >= %{dbus_version}

%description devel
Headers, static libraries and API docs for HAL.

%description devel -l zh_CN.UTF-8
HAL的头文件，静态库和API文档。

%prep
%if 0%{git}
%setup -q -n %{name}-git%{gitdate}
%else
%setup
%endif
%patch1 -p1 -b .magic
#%patch2 -p1
%patch5 -p1 -b .mount_point
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1

%build
%if 0%{git}
./autogen.sh --prefix=%{_prefix} --sysconfdir=%{_sysconfdir} --libdir=%{_libdir} --disable-docbook-docs  --with-os-type=redhat  --disable-policy-kit --with-backend=linux
%else
%configure --disable-docbook-docs  --with-os-type=redhat  --disable-policy-kit --with-backend=linux
%endif
make

%install
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/var/cache/hald
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
mkdir -p  $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d
install -m 0644 tools/linux/90-hal.rules $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/90-hal.rules
[ -x /usr/bin/magic_rpm_clean.sh ] && /usr/bin/magic_rpm_clean.sh


%clean
rm -rf %{buildroot}

%pre
# Add the "haldaemon" user
/usr/sbin/useradd -c 'HAL daemon' -u %{hal_user_uid} \
	-s /sbin/nologin -r -d '/' haldaemon 2> /dev/null || :

%post
/sbin/ldconfig
/sbin/chkconfig --add haldaemon
if [ `cat /etc/group | awk -F: '{print $1}' |grep plugdev` != "plugdev" ]
then
/usr/sbin/groupadd plugdev
fi

%preun
if [ $1 = 0 ]; then
    service haldaemon stop > /dev/null 2>&1
    /sbin/chkconfig --del haldaemon
fi

%postun
/sbin/ldconfig
if [ "$1" -ge "1" ]; then
  service haldaemon condrestart > /dev/null 2>&1
fi

%files
%defattr(-,root,root)

%dir %{_sysconfdir}/dbus-1/system.d
%{_sysconfdir}/dbus-1/system.d/*

%config %{_sysconfdir}/rc.d/init.d/haldaemon

#%dir %{_sysconfdir}/hal
#%{_sysconfdir}/hal/*

%dir /var/cache/hald

%{_sbindir}/*
%{_bindir}/*

%{_libexecdir}/*

%{_libdir}/*hal*.so.*

%dir %{_datadir}/hal
%dir %{_datadir}/hal/fdi

#%dir %{_libdir}/hal/scripts
#%dir %{_libdir}/hal/scripts/linux

%{_datadir}/hal/fdi/*
%{_mandir}/*

#%{_datadir}/PolicyKit/policy/*

#%{_libdir}/hal/scripts/*
#%{_libdir}/hal/scripts/linux/*

%{_prefix}/lib/udev/rules.d/90-hal.rules
%{_sysconfdir}/udev/rules.d/90-hal.rules

%files devel
%defattr(-,root,root)

%{_libdir}/lib*.a
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{_datadir}/gtk-doc/*
# TODO: include hal-spec

%changelog
* Thu Oct 30 2008 Liu Di <liudidi@gmail.com> - 0.5.11-0.2mgc
- 更新到 0.5.11

* Wed Apr 16 2008 Liu Di <liudidi@gmail.com> - 0.5.9-git200706071
- 修复普通用户自动挂载的问题

* Fri Mar 16 2007 Liu Di <liudidi@gmail.com> - 0.5.9-git20070316
- update to git20070316

* Tue Oct 19 2006 KanKer <kanker@163.com> -0.5.8-3mgc
- rebuild hal-0.5.8.1
- fix some encode bug
- change default mount_point from label to device

* Wed Nov 30 2005 KanKer <kanker@163.com>
- update to latest upstream version

* Fri Oct 7 2005 KanKer <kanker@163.com>
- update 20051007 cvs

* Fri Sep 30 2005 KanKer <kanker@163.com>
- remove pmount-hal.sh and pmount-hal.fdi

* Wed Sep 14 2005 KanKer <kanker@163.com>
- use pmount

* Thu Sep 13 2005 KanKer <kanker@163.com>
- rebuild

* Tue Aug 30 2005 David Zeuthen <davidz@redhat.com> - 0.5.4-3
- Rebuild

* Tue Aug 30 2005 David Zeuthen <davidz@redhat.com> - 0.5.4-2
- Pull in cryptsetup-luks and fix some unpackaged files

* Tue Aug 30 2005 David Zeuthen <davidz@redhat.com> - 0.5.4-1
- Update to upstream release 0.5.4 and drop patches already upstream

* Thu Aug 11 2005 David Zeuthen <davidz@redhat.com> - 0.5.3-4
- Add patch to make libhal-storage report the right fs usage (#165707)

* Tue Aug  9 2005 Jeremy Katz <katzj@redhat.com> - 0.5.3-3
- make kernel version requirement a conflicts instead

* Tue Jul 12 2005 David Zeuthen <davidz@redhat.com> 0.5.3-2
- Fix a minor packaging bug

* Tue Jul 12 2005 David Zeuthen <davidz@redhat.com> 0.5.3-1
- Update to upstream release 0.5.3
- Drop patches as they are upstream

* Mon May 23 2005 David Zeuthen <davidz@redhat.com> 0.5.2-2
- Fix doublefree when locking (#158474)
- Never use the 'sync' mount option (#157674)
- Update the fstab-sync man page (#158483)

* Thu May 12 2005 David Zeuthen <davidz@redhat.com> 0.5.2-1
- Update to upstream release 0.5.2

* Wed Apr 27 2005 David Zeuthen <davidz@redhat.com> 0.5.1-1
- Update to upstream release 0.5.1

* Tue Apr 19 2005 Florian La Roche <laroche@redhat.com>
- exclude usb reqs for mainframe (#154616)

* Mon Apr  4 2005 David Zeuthen <davidz@redhat.com> 0.5.0.cvs20050404b-2
- Rebuild

* Mon Apr  4 2005 David Zeuthen <davidz@redhat.com> 0.5.0.cvs20050404b-1
- Use new upstream tarball rather than patching configure

* Mon Apr  4 2005 David Zeuthen <davidz@redhat.com> 0.5.0.cvs20050404-3
- Add libusb checks to configure.in

* Mon Apr  4 2005 David Zeuthen <davidz@redhat.com> 0.5.0.cvs20050404-2
- Add BuildRequires and Requires for libusb

* Mon Apr  4 2005 David Zeuthen <davidz@redhat.com> 0.5.0.cvs20050404-1
- New snapshot from upstream CVS

* Tue Mar 22 2005 David Zeuthen <davidz@redhat.com> 0.5.0.cvs20050322b-1
- Another new snapshot from upstream CVS

* Tue Mar 22 2005 David Zeuthen <davidz@redhat.com> 0.5.0.cvs20050322-1
- New snapshot from upstream CVS

* Fri Mar 18 2005 David Zeuthen <davidz@redhat.com> 0.5.0.cvs20050318-1
- Snapshot from upstream CVS; should fix selinux labeling problems
  for /etc/fstab entries

* Thu Mar 10 2005 David Zeuthen <davidz@redhat.com> 0.5.0.cvs20050310-1
- Snapshot from CVS; should fix ACPI issues reported on f-d-l

* Tue Mar  8 2005 David Zeuthen <davidz@redhat.com> 0.5.0-3
- Rebuild

* Mon Mar  7 2005 David Zeuthen <davidz@redhat.com> 0.5.0-2
- Update to upstream release 0.5.0

* Thu Jan 27 2005 David Zeuthen <davidz@redhat.com> 0.4.7-2
- Add patch that should close #146316

* Mon Jan 24 2005 David Zeuthen <davidz@redhat.com> 0.4.7-1
- New upstream release.
- Should close #145921, #145750, #145293, #145256

* Mon Jan 24 2005 John (J5) Palmieri <johnp@redhat.com> 0.4.6-3
- Update required dbus version to 0.23 

* Thu Jan 20 2005 David Zeuthen <davidz@redhat.com> 0.4.6-2
- Fix parameters to configure

* Thu Jan 20 2005 David Zeuthen <davidz@redhat.com> 0.4.6-1
- New upstream release
- Should close #145099, #144600, #140150, #145223, #137672

* Wed Jan 12 2005 David Zeuthen <davidz@redhat.com> 0.4.5-1
- New upstream release.
- Should close #142834, #141771, #142183

* Fri Dec 12 2004 David Zeuthen <davidz@redhat.com> 0.4.2.cvs20041210-1
- Snapshot from stable branch of upstream CVS

* Tue Oct 26 2004 David Zeuthen <davidz@redhat.com> 0.4.0-8
- Forgot to add some diffs in hal-0.4.0-pcmcia-net-support.patch

* Tue Oct 26 2004 David Zeuthen <davidz@redhat.com> 0.4.0-7
- Change default policy such that non-hotpluggable fixed disks are not
  added to the /etc/fstab file because a) ATARAID detection in hal is
  incomplete (e.g. RAID members from ATARAID controllers might be added
  to /etc/fstab); and b) default install wont corrupt multiboot 
  systems on fixed drives (#137072)

* Tue Oct 26 2004 David Zeuthen <davidz@redhat.com> 0.4.0-6
- Fix hotplug timeout handling (#136626)
- Detect ATARAID devices and do not add /etc/fstab entry for them
- Probe for ext3 before ntfs (#136966)
- Use fstype 'auto' for optical drives instead of 'iso9660,udf'
- Properly detect wireless ethernet devices  (#136591)
- Support 16-bit PCMCIA networking devices (by Dan Williams) (#136658)

* Tue Oct 19 2004 David Zeuthen <davidz@redhat.com> 0.4.0-5
- Make hal work with PCMCIA IDE hotpluggable devices (#133943)
- Fixup URL listed from rpm -qi (#136396)
- Add Portuguese translations for hal
- Fix addition of Russian and Hungarian translations

* Mon Oct 18 2004 David Zeuthen <davidz@redhat.com> 0.4.0-4
- Make hald cope with missing hotplug events from buggy drivers (#135202)
- Fix the order of mount options in fstab-sync (#136191)
- Allow x86 legacy floppy drives in default policy (#133777)
- Fix fstab-sync crashing without any options and not run from hald (#136214)
- man page for fstab-sync references non-existing files (#136026)
- Add Russian translations for hal (#135853)
- Add Hungarian translations for hal

* Fri Oct 15 2004 David Zeuthen <davidz@redhat.com> 0.4.0-3
- Fix bad use of O_NONBLOCK as the 2.6.8-1.624 kernel exposes this (#135886)
- Never use the UUID as mount point candidate in the default policy 
  as it is unfriendly (#135907)
- Fix a trivial bug in fstab-sync so the syslog messages actually expose
  the device name instead of just the word foo

* Thu Oct 14 2004 David Zeuthen <davidz@redhat.com> 0.4.0-2
- Fix issue with fstab-sync not cleaning /etc/fstab on startup

* Thu Oct 14 2004 David Zeuthen <davidz@redhat.com> 0.4.0-1
- Update to upstream stable version 0.4.0
- Remove patch for libhal shutdown since that is now upstream
- fstab-sync: man page, adds comment in /etc/fstab pointing to man page

* Fri Oct 01 2004 David Zeuthen <davidz@redhat.com> 0.2.98.cvs20040929-3
- Fix a bug so libhal actually invoke callback functions when needed

* Fri Oct 01 2004 John (J5) Palmieri <johnp@redhat.com> 0.2.98.cvs20040929-2
- Use "user" mount flag for now until "pamconsole" flag gets into mount

* Wed Sep 29 2004 David Zeuthen <davidz@redhat.com> 0.2.98.cvs20040929-1
- Update to upstream CVS version
- Enable libselinux again

* Mon Sep 27 2004 David Zeuthen <davidz@redhat.com> 0.2.98.cvs20040927-1
- Update to upstream CVS version

* Fri Sep 24 2004 David Zeuthen <davidz@redhat.com> 0.2.98.cvs20040923-1
- Update to upstream CVS release
- Include libhal-storage library
- Should close bug #132876

* Mon Sep 20 2004 David Zeuthen <davidz@redhat.com> 0.2.98-4
- Rebuilt

* Mon Sep 20 2004 David Zeuthen <davidz@redhat.com> 0.2.98-3
- Rebuilt

* Mon Sep 20 2004 David Zeuthen <davidz@redhat.com> 0.2.98-2
- Temporarily disable explicit requirement for libselinux

* Mon Sep 20 2004 David Zeuthen <davidz@redhat.com> 0.2.98-1
- Update to upstream release 0.2.98. 
- Use --with-pid-file so we don't depend on /etc/redhat-release

* Wed Sep 01 2004 David Zeuthen <davidz@redhat.com> 0.2.97.cvs20040901-1
- Update to upstream CVS HEAD

* Tue Aug 31 2004 David Zeuthen <davidz@redhat.com> 0.2.97.cvs20040831-3
- Add UID for haldaemon user

* Tue Aug 31 2004 David Zeuthen <davidz@redhat.com> 0.2.97.cvs20040831-2
- Rebuilt with a newer snapshot.

* Fri Aug 27 2004 David Zeuthen <davidz@redhat.com> 0.2.97.cvs20040827-3
- Rebuilt

* Fri Aug 27 2004 David Zeuthen <davidz@redhat.com> 0.2.97.cvs20040827-2
- Rebuilt
- Closes RH Bug #130971

* Fri Aug 27 2004 David Zeuthen <davidz@redhat.com> 0.2.97.cvs20040827-1
- Update to upstream CVS HEAD. 
- Should close RH Bug #130588

* Wed Aug 25 2004 David Zeuthen <davidz@redhat.com> 0.2.97.cvs20040823-3
- Rebuilt

* Wed Aug 25 2004 David Zeuthen <davidz@redhat.com> 0.2.97.cvs20040823-2
- Apply a patch so hald doesn't hang on startup.

* Mon Aug 23 2004 David Zeuthen <davidz@redhat.com> 0.2.97.cvs20040823-1
- Update to upstream CVS HEAD
- Remove symlinking of fstab-sync from specfile since this is now being
  done in the package

* Mon Aug 23 2004 Florian La Roche <Florian.LaRoche@redhat.de>
- change the %%define names to not use "-"

* Thu Aug 19 2004 David Zeuthen <davidz@redhat.com> 0.2.97.cvs20040819-1
- Update to upstream CVS HEAD
- Remove suid patch as it is fixed upstream
- Fix some dependency issues (RH Bug #130202)

* Wed Aug 18 2004 John (J5) Palmieri <johnp@redhat.com> 0.2.97-2
- Add stopgap patch to remove suid from mount flags (RH Bug #130290)

* Mon Aug 16 2004 David Zeuthen <davidz@redhat.com> 0.2.97-1
- update to upstream release 0.2.97
- use kudzu option in fstab-sync since updfstab is now disabled

* Thu Aug 12 2004 John (J5) Palmieri <johnp@redhat.com> 0.2.96-2
- fixed Requires lines to use %{} instead of ${}
- made dbus related requires lines use the = condition instead of =<
  because the dbus API is still in flux

* Thu Aug 12 2004 David Zeuthen <davidz@redhat.com> 0.2.96
- Update to upstream release 0.2.96
- Symlink fstab-sync into /etc/hal/device.d on install

* Fri Aug 06 2004 John (J5) Palmieri <johnp@redhat.com> 0.2.95.cvs20040802-2
- Base hal package no longer requires python

* Mon Aug 02 2004 John (J5) Palmieri <johnp@redhat.com> 0.2.95.cvs20040802-1
- Update to CVS head
- Remove Dan's patches as they were commited to CVS

* Fri Jul 30 2004 Dan Williams <dcbw@redhat.com> 0.2.93.cvs.20040712-2
- Fix netlink sockets pointer arithmetic bug

* Mon Jul 12 2004 John (J5) Palmieri <johnp@redhat.com> 0.2.93.cvs.20040712-1
- Update to new CVS version as of 7-12-2004

* Fri Jun 25 2004 John (J5) Palmieri <johnp@redhat.com> 0.2.92.cvs.20040611-2
- take out fstab-update.sh from install
- add to rawhide
 
* Fri Jun 11 2004 John (J5) Palmieri <johnp@redhat.com> 0.2.92.cvs.20040611-1 
- update to CVS head as of 6-11-2004 which contains dcbw's 
  network link status fix 

* Wed Jun 9 2004 Ray Strode <rstrode@redhat.com> 0.2.91.cvs20040527-2
- added dependency on udev

* Wed May 12 2004 John (J5) Palmieri <johnp@redhat.com> 0.2.91.cvs20040527-1
- update to CVS head as of 5-27-2004 which contains fixes for PCMCIA
  and wireless network devices.

* Wed May 12 2004 John (J5) Palmieri <johnp@redhat.com> 0.2.90.cvs20040511-3
- added hal-0.2.90.cvs20040511.callbackscripts.patch which installs 
  the file system mounting script in /etc/hal/device.d

* Wed May 12 2004 John (J5) Palmieri <johnp@redhat.com> 0.2.90.cvs20040511-2
- added the %{_sysconfigdir}/hal directory tree to %files 

* Tue May 11 2004 John (J5) Palmieri <johnp@redhat.com> 0.2.90.cvs20040511-1
- update to CVS head as of 5-11-2004

* Wed May 5 2004 Christopher Blizzard <blizzard@redhat.com> 0.2.90-2
- Install hal.dev from /etc/dev.d/default/

* Mon Apr 19 2004 John (J5) Palmieri <johnp@redhat.com> 0.2.90-1
- upstream update

* Mon Apr 19 2004 John (J5) Palmieri <johnp@redhat.com> 0.2-1 
- initial checkin to package repository
- added dependency to the dbus-python package
- added %{_libexecdir}/hal.dev to teh %files section
