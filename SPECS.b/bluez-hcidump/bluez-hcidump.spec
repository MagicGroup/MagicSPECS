Summary: Bluetooth HCI protocol analyser
Summary(zh_CN.UTF-8): 蓝牙 HCI 协议分析器
Name: bluez-hcidump
Version: 2.5
Release: 4%{?dist}
License: GPLv2+
Group: Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
Source: http://www.kernel.org/pub/linux/bluetooth/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
URL: http://www.bluez.org/
Requires: glibc >= 2.2.4
Requires: bluez-libs >= 3.14
BuildRequires: glibc-devel >= 2.2.4
BuildRequires: bluez-libs-devel >= 3.14
BuildRequires: pkgconfig
ExcludeArch: s390 s390x

%description
Protocol analyser for Bluetooth traffic.

The BLUETOOTH trademarks are owned by Bluetooth SIG, Inc., U.S.A.

%description -l zh_CN.UTF-8
蓝牙 HCI 协议分析器。

%prep

%setup -q

%build
%configure
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%doc AUTHORS COPYING INSTALL ChangeLog NEWS README
%{_sbindir}/hcidump
%{_mandir}/man8/hcidump.8.gz

%changelog
* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 2.5-4
- 为 Magic 3.0 重建

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Dec 04 2012 Bastien Nocera <bnocera@redhat.com> 2.5-1
- Update to 2.5

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Apr 27 2012 Bastien Nocera <bnocera@redhat.com> 2.4-1
- Update to 2.4

* Fri Mar 02 2012 Bastien Nocera <bnocera@redhat.com> 2.3-1
- Update to 2.3

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec 30 2011 Bastien Nocera <bnocera@redhat.com> 2.2-1
- Update to 2.2

* Mon Jun 20 2011 Bastien Nocera <bnocera@redhat.com> 2.1-1
- Update to 2.1

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 27 2011 Bastien Nocera <bnocera@redhat.com> 2.0-1
- Update to 2.0

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.42-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.42-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Sep 22 2008 - David Woodhouse <David.Woodhouse@intel.com> - 1.42-2
- Rebuild for libbluetooth.so.3

* Tue Jun 17 2008 - Bastien Nocera <bnocera@redhat.com> - 1.42-1
- Update to 1.42

* Tue Mar 04 2008 David Woodhouse <dwmw2@infradead.org> - 1.41-1
- update to bluez-hcidump 1.41

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.40-2
- Autorebuild for GCC 4.3

* Wed Aug 22 2007 David Woodhouse <dwmw2@infradead.org> - 1.40-1
- update to bluez-hcidump 1.40
- update licence

* Sat Jul 21 2007 David Woodhouse <dwmw2@infradead.org> - 1.37-1
- update to bluez-hcidump 1.37

* Tue Jan 30 2007 David Woodhouse <dwmw2@redhat.com> - 1.33-1
- update to bluez-hcidump 1.33

* Sat Sep 30 2006 David Woodhouse <dwmw2@redhat.com> - 1.32-1
- update to bluez-hcidump 1.32
- Fix BNEP IPv6 parsing (#196879)
- Support IPv6 in -n and -s options (#196878)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.31-5.1
- rebuild

* Sun Jun 11 2006 David Woodhouse <dwmw2@redhat.com> 1.31-5
- Upload 1.31 tarball now that the lookaside works again

* Sun Jun 11 2006 David Woodhouse <dwmw2@redhat.com> 1.31-4
- BuildRequire pkgconfig so that the autocrap stuff doesn't break

* Sun Jun 11 2006 David Woodhouse <dwmw2@redhat.com> 1.31-3
- Rebuild now that new bluez-libs is actually in the repo

* Sun Jun 11 2006 David Woodhouse <dwmw2@redhat.com> 1.31-2
- use 1.30 tarball and patch, since lookaside cache seems broken

* Sun Jun 11 2006 David Woodhouse <dwmw2@redhat.com> 1.31-1
- update to bluez-hcidump 1.31

* Thu Feb 23 2006 David Woodhouse <dwmw2@redhat.com> 1.30-1
- Ipdate to bluez-hcidump 1.30

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.27-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.27-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Sun Nov 6 2005 David Woodhouse <dwmw2@redhat.com> 1.27-1
- update to bluez-hcidump 1.27

* Mon Aug 8 2005 David Woodhouse <dwmw2@redhat.com> 1.24-1
- update to bluez-hcidump 1.24
- require bluez-libs 1.18

* Tue Mar 2 2005 David Woodhouse <dwmw2@redhat.com> 1.18-1
- update to bluez-hcidump 1.18

* Tue Jan 12 2005 David Woodhouse <dwmw2@redhat.com> 1.16-1
- update to bluez-hcidump 1.16

* Tue Sep 22 2004 David Woodhouse <dwmw2@redhat.com> 1.11-1
- update to bluez-hcidump 1.11

* Tue Aug 02 2004 David Woodhouse <dwmw2@redhat.com> 1.10-1
- update to bluez-hcidump 1.10

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed May 12 2004 David Woodhouse <dwmw2@redhat.com>
- update to bluez-hcidump 1.8

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Apr 25 2003 David Woodhosue <dwmw2@redhat.com> 1.5-2
- Fix get_unaligned() -- don't abuse kernel headers.

* Thu Apr 24 2003 David Woodhouse <dwmw2@redhat.com>
- Initial build
