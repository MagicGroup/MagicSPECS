Summary:        Utilities for configuring the linux ethernet bridge
Summary(zh_CN.UTF-8): 配置 Linux 以太网网桥的工具
Name:           bridge-utils
Version:        1.5
Release:        4%{?dist}
License:        GPLv2+
URL:            http://www.linuxfoundation.org/collaborate/workgroups/networking/bridge
Group:          System Environment/Base
Group(zh_CN.UTF-8): 系统环境/基本
Source:         http://dl.sf.net/bridge/%{name}-%{version}.tar.gz
Patch0:         bridge-utils-1.5-fix-incorrect-command-in-manual.patch
Patch1:         bridge-utils-1.5-fix-error-message-for-incorrect-command.patch
Patch2:         bridge-utils-1.5-check-error-returns-from-write-to-sysfs.patch
Patch3:		bridge-utils-1.5-linux_3.8.x.patch
Patch10:        bridge-utils-1.0.4-inc.patch
BuildRequires:  libsysfs-devel autoconf
BuildRequires:  kernel-headers >= 2.6.16

%description
This package contains utilities for configuring the linux ethernet
bridge. The linux ethernet bridge can be used for connecting multiple
ethernet devices together. The connecting is fully transparent: hosts
connected to one ethernet device see hosts connected to the other
ethernet devices directly.

Install bridge-utils if you want to use the linux ethernet bridge.

%description -l zh_CN.UTF-8
配置 Linux 以太网网桥的工具，网桥可以用来透明的连接多个设备。

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch10 -p1

%build
autoconf
%configure
make

%install
make DESTDIR=%{buildroot} SUBDIRS="brctl doc" install

%files
%doc AUTHORS COPYING doc/FAQ doc/HOWTO
%{_sbindir}/brctl
%{_mandir}/man8/brctl.8*

%changelog
* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 1.5-4
- 为 Magic 3.0 重建

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 1.5-3
- 为 Magic 3.0 重建

* Mon May 30 2011 Petr Sabata <contyk@redhat.com> - 1.5-2
- Add three latest bugfixes from upstream git on top of 1.5
- Dropping params patch (included upstream variant)

* Mon May 30 2011 Petr Sabata <contyk@redhat.com> - 1.5-1
- 1.5 bump
- BuildRoot and defattr cleanup
- Use macros in Sources
- Drop show-ports and foreach patches -- those have been included upstream

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 20 2010 Bill Nottingham <notting@redhat.com> - 1.2-9
- Fix URL (#248086)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jul 03 2008 David Woodhouse <david.woodhouse@intel.com> 1.2-6
- Fix location of bridge parameters in sysfs

* Wed Mar 05 2008 David Woodhouse <dwmw2@redhat.com> 1.2-5
- Fix handling of bridge named 'bridge' (#436120)

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.2-4
- Autorebuild for GCC 4.3

* Mon Dec 10 2007 Patrick "Jima" Laughton <jima@beer.tclug.org> 1.2-3
- Minor tweaks as recommended in merge review (BZ#225625)

* Wed Aug 22 2007 David Woodhouse <dwmw2@redhat.com> 1.2-2
- Update licence

* Wed Aug 22 2007 David Woodhouse <dwmw2@redhat.com> 1.2-1
- Update to 1.2

* Sat Sep 09 2006 David Woodhouse <dwmw2@redhat.com> 1.1-2
- Fix setportprio command (#205810)
- Other updates from bridge-utils git tree

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.1-1.1
- rebuild

* Wed Jun 07 2006 David Woodhouse <dwmw2@redhat.com> 1.1-1
- Update to 1.1
- BR libsysfs-devel instead of sysfsutils-devel

* Wed Jun 07 2006 David Woodhouse <dwmw2@redhat.com> 1.0.6-2
- Use sane kernel headers, drop -devel package

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.0.6-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.0.6-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Dec 21 2005 David Woodhouse <dwmw2@redhat.com> 1.0.6-1
- Update to 1.0.6
- Cleanups from Matthias Saou (#172774)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Mar 2 2005 David Woodhouse <dwmw2@redhat.com> 1.0.4-6
- Rebuild with gcc 4

* Tue Feb 15 2005 David Woodhouse <dwmw2@redhat.com> 1.0.4-5
- Rebuild

* Thu Aug 26 2004 David Woodhouse <dwmw2@redhat.com> 1.0.4-4
- BuildRequires: sysfsutils-devel to make the horrid autoconf script magically
  change the entire package's behaviour just because it happens to find 
  slightly different header files lying around.
- Include our own kernel-derived headers

* Thu Jul 1 2004 David Woodhouse <dwmw2@redhat.com>
- Update to 1.0.4

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sat Oct 25 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- support change to call sysconf() to get HZ

* Tue Sep 16 2003 David Woodhouse <dwmw2@redhat.com> 0.9.6-1
- Update to 0.9.6
- Detect lack of kernel bridge support or EPERM and exit with appropriate code.

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Fri Dec 13 2002 Elliot Lee <sopwith@redhat.com> 0.9.3-7
- Rebuild

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Mar 04 2002 Benjamin LaHaise <bcrl@redhat.com>
- manual rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Nov 07 2001 Matthew Galgoci <mgalgoci@redhat.com>
- initial cleanup of spec file from net release

