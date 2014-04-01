Summary:        Tool to analyse BIOS DMI data
Summary(zh_CN.UTF-8): 分析 BIOS DMI 数据的工具
Name:           dmidecode
Version:        2.12
Release:        4%{?dist}
Epoch:          1
Group:          System Environment/Base
Group(zh_CN.UTF-8): 系统环境/基本
License:        GPLv2+
Source0:        %{name}-%{version}.tar.bz2
URL:            http://www.nongnu.org/dmidecode/
Patch0:         dmidecode-2.12-smbios_fix.patch
Buildroot:      %{_tmppath}/%{name}-%{version}-root
BuildRequires:  automake autoconf
ExclusiveArch:  %{ix86} x86_64 ia64 mips64el

%description
dmidecode reports information about x86 & ia64 hardware as described in the
system BIOS according to the SMBIOS/DMI standard. This information
typically includes system manufacturer, model name, serial number,
BIOS version, asset tag as well as a lot of other details of varying
level of interest and reliability depending on the manufacturer.

This will often include usage status for the CPU sockets, expansion
slots (e.g. AGP, PCI, ISA) and memory module slots, and the list of
I/O ports (e.g. serial, parallel, USB).

%description -l zh_CN.UTF-8
分析 BIOS DMI 数据的工具。

%prep
%setup -q
%patch0 -p1 -b .smbios_fix

%build
make %{?_smp_mflags} CFLAGS="$RPM_OPT_FLAGS"

%install
rm -rf ${buildroot}
make %{?_smp_mflags} DESTDIR=%{buildroot} prefix=%{_prefix} install-bin install-man

%clean
rm -rf ${buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS CHANGELOG LICENSE README
%{_sbindir}/dmidecode
%ifnarch ia64 mips64el
%{_sbindir}/vpddecode
%{_sbindir}/ownership
%{_sbindir}/biosdecode
%endif
%{_mandir}/man8/*

%changelog
* Thu May 09 2013 Anton Arapov <anton@redhat.com> - 1:2.12-3
- Accomodate few more necesary, to enable SMBIOS v2.8, changes from upstream.

* Fri Apr 26 2013 Anton Arapov <anton@redhat.com> - 1:2.12-2
- Fixup, so that it actually read SMBIOS 2.8.0 table.

* Wed Apr 17 2013 Anton Arapov <anton@redhat.com> - 1:2.12-1
- Update to upstream 2.12 release.

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.11-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.11-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Mar 26 2012 Anton Arapov <anton@redhat.com> - 1:2.11-8
- Update dmidecode.8 manpage

* Mon Mar 12 2012 Anton Arapov <anton@redhat.com> - 1:2.11-7
- Add "PXE" to HP OEM Type 209 record output
- Properly print the hexadecimal value of invalid string characters

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 14 2011 Anton Arapov <anton@redhat.com> - 1:2.11-5
- Fix the wrong call of the dmi_chassis_type function call. Thus fix
  an issue on the systems with the chassis lock available, application
  doesn't fall out with the out of spec error anymore.

* Tue May 03 2011 Anton Arapov <anton@redhat.com> - 1:2.11-4
- Update to SMBIOS 2.7.1
- Fix the boundaries check in type16

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 19 2011 Anton Arapov <anton@redhat.com> - 1:2.11-2
- Update to upstream 2.11 release. (#623047)

* Wed Jan 19 2011 Anton Arapov <anton@redhat.com> - 1:2.11-1
- Fix the changelog's NVR.

* Mon Nov 08 2010 Prarit Bhargava <prarit@redhat.com> - 1:2.10-3
- updated kernel.spec for review [BZ 225698]

* Fri Oct 15 2010 Anton Arapov <aarapov@redhat.com> - 1:2.10-2
- Does not build with gnu make v3.82+ (#631407)

* Fri Dec 18 2009 Prarit Bhargava <prarit@redhat.com> - 1:2.10-1.40
- Fix rpmlint errors in specfile

* Fri Aug 28 2009 Jarod Wilson <jarod@redhat.com> - 1:2.10-1.39
- Fix cache associativity mapping (was missing some commas)

* Mon Aug 24 2009 Jarod Wilson <jarod@redhat.com> - 1:2.10-1.38
- Add support for newer sockets, processors and pcie slot types

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.10-1.36.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Feb 27 2009 Matthias Clasen <mclasen@redhat.com>
- Build for i586

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.10-1.34.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 09 2009 Prarit Bhargava <prarit@redhat.com> 1:2.10
- rebuild with version 2.10

* Wed Jan 28 2009 Prarit Bhargava <prarit@redhat.com> 1:2.9-1.32
- fix Summary field (BZ 225698)

* Wed Jul 16 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1:2.9-1.30
- fix license tag

* Fri Mar 14 2008 Doug Chapman <doug.chapman@hp.com> 1:2.9-1.29.1
- Do not package vpddecode, ownership and biosdecode on ia64 since those are x86 only

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1:2.9-1.27.1
- Autorebuild for GCC 4.3

* Mon Oct 22 2007 Prarit Bhargava <prarit@redhat.com> - 1:2.9
- rebuild with version 2.9
* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1:2.7-1.25.1
- rebuild

* Thu Feb 09 2006 Dave Jones <davej@redhat.com>
- rebuild.

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Nov 28 2005 Dave Jones <davej@redhat.com>
- Integrate several specfile cleanups from Robert Scheck. (#172543)

* Sat Sep 24 2005 Dave Jones <davej@redhat.com>
- Revert yesterdays patch, its unneeded in 2.7

* Fri Sep 23 2005 Dave Jones <davej@redhat.com>
- Don't try to modify areas mmap'd read-only.
- Don't build on ia64 any more.
  (It breaks on some boxes very badly, and works on very few).

* Mon Sep 12 2005 Dave Jones <davej@redhat.com>
- Update to upstream 2.7

* Fri Apr 15 2005 Florian La Roche <laroche@redhat.com>
- remove empty scripts

* Wed Mar  2 2005 Dave Jones <davej@redhat.com>
- Update to upstream 2.6

* Tue Mar  1 2005 Dave Jones <davej@redhat.com>
- Rebuild for gcc4

* Tue Feb  8 2005 Dave Jones <davej@redhat.com>
- Rebuild with -D_FORTIFY_SOURCE=2

* Tue Jan 11 2005 Dave Jones <davej@redhat.com>
- Add missing Obsoletes: kernel-utils

* Mon Jan 10 2005 Dave Jones <davej@redhat.com>
- Update to upstream 2.5 release.

* Sat Dec 18 2004 Dave Jones <davej@redhat.com>
- Initial packaging, based upon kernel-utils package.

