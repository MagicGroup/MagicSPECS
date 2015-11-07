%global _default_patch_fuzz 2

# https://fedoraproject.org/wiki/Packaging:Guidelines#Compiler_flags
%global _hardened_build 1

%global checkout 986eb2e

Name:               lldpad
Version:            1.0.1
Release:            3.git%{checkout}%{?dist}
Summary:            Intel LLDP Agent
Summary(zh_CN.UTF-8): Intel LLDP 代理
Group:              System Environment/Daemons
Group(zh_CN.UTF-8): 系统环境/服务
License:            GPLv2
URL:                http://open-lldp.org/
Source0:            %{name}-%{version}.tar.gz
Patch1:		open-lldp-v1.0.1-1-VDP-vdp22_cmds-retrieve-vsi-paramenter-data.patch
Patch2:		open-lldp-v1.0.1-2-VDP-vdptool-first-version.patch
Patch3:		open-lldp-v1.0.1-3-VDP-vdptool-test-cases-Some-test-cases-to-test-the-n.patch
Patch4:		open-lldp-v1.0.1-4-VDP-Changes-to-make-the-interface-to-VDP22-in-lldpad.patch
Patch5:		open-lldp-v1.0.1-5-VDP-Support-for-get-tlv-in-vdptool-and-VDP22.patch
Patch6:		open-lldp-v1.0.1-6-VDP-Support-in-VDP22-for-correct-error-code-status-t.patch
Patch7:		open-lldp-v1.0.1-7-VDP-Support-for-OUI-infrastructure-in-VDP22.patch
Patch8:		open-lldp-v1.0.1-8-VDP-Support-for-OUI-infrastructure-in-vdptool.patch
Patch9:		open-lldp-v1.0.1-9-VDP-Support-for-OUI-infrastructure-in-vdp22.patch
Patch10:	open-lldp-v1.0.1-10-VDP-Support-for-OUI-infrastructure-in-vdp22.patch
Patch11:	open-lldp-v1.0.1-11-VDP-Support-for-Cisco-specific-OUI-extensions-to-VDP.patch
Patch12:	open-lldp-v1.0.1-12-VDP22-Fix-the-ack-timeout-handler-to-set-the-right-t.patch
Patch13:	open-lldp-v1.0.1-13-VDP-Changes-in-OUI-infra-for-get-tlv.patch
Patch14:	open-lldp-v1.0.1-14-VDP-Changes-in-Cisco-OUI-handlers-to-support-get-tlv.patch
Patch15:	open-lldp-v1.0.1-15-VDP-Add-vdptool-man-page-to-Makefile.patch
Patch16:	open-lldp-v1.0.1-16-VDP-Fixed-DBG-print-compile-errors-in-32-bit-systems.patch
Patch17:	open-lldp-v1.0.1-17-lldp-automake-fixes-for-dist-distcheck.patch
Patch18:	open-lldp-v1.0.1-18-enabled-test-tool-building-for-distcheck.patch
Patch19:	open-lldp-v1.0.1-19-nltest-build-error.patch
Patch20:	open-lldp-v1.0.1-20-lldp-automake-fix-drop-prefix-on-vdptool_LDADD.patch
Patch21:	open-lldp-v1.0.1-21-lldpad-Fix-DCBX-event-generation-from-lldpad.patch
Patch22:	open-lldp-v1.0.1-22-vdp-Fixed-the-memory-leak-for-modify-VSI-support-for.patch
Patch23:	open-lldp-v1.0.1-23-lldp-make-TTL-TLV-configurable.patch
Patch24:	open-lldp-v1.0.1-24-fix-build-warnings.patch

BuildRequires:      automake autoconf libtool
BuildRequires:      flex >= 2.5.33
BuildRequires:      kernel-headers >= 2.6.32
BuildRequires:      libconfig-devel >= 1.3.2
BuildRequires:      libnl3-devel
BuildRequires:      readline-devel
BuildRequires:      systemd
Requires:           readline

Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd

%description
This package contains the Linux user space daemon and configuration tool for
Intel LLDP Agent with Enhanced Ethernet support for the Data Center.

%description -l zh_CN.UTF-8
Intel LLDP 代理。

%package            devel
Summary:            Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:              Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:           %{name}%{?_isa} = %{version}-%{release}
Provides:           dcbd-devel = %{version}-%{release}
Obsoletes:          dcbd-devel < 0.9.26

%description devel
The %{name}-devel package contains header files for developing applications
that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%autosetup -p1

%build
./bootstrap.sh
%configure --disable-static
# fix the hardened build flags
sed -i -e 's! \\\$compiler_flags !&\\\$CFLAGS \\\$LDFLAGS !' libtool
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
mkdir -p %{buildroot}%{_sharedstatedir}/%{name}
rm -f %{buildroot}%{_libdir}/liblldp_clif.la
magic_rpm_clean.sh

%post
/sbin/ldconfig
%systemd_post %{name}.service %{name}.socket

%preun
%systemd_preun %{name}.service %{name}.socket

%postun
/sbin/ldconfig
%systemd_postun_with_restart %{name}.service %{name}.socket

%files
%doc COPYING README ChangeLog
%{_sbindir}/*
%{_libdir}/liblldp_clif.so.*
%dir %{_sharedstatedir}/%{name}
%{_unitdir}/%{name}.service
%{_unitdir}/%{name}.socket
%dir %{_sysconfdir}/bash_completion.d/
%{_sysconfdir}/bash_completion.d/*
%{_mandir}/man3/*
%{_mandir}/man8/*

%files devel
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/liblldp_clif.so

%changelog
* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 1.0.1-3.git986eb2e
- 为 Magic 3.0 重建

* Thu Sep 03 2015 Liu Di <liudidi@gmail.com> - 1.0.1-2.git986eb2e
- 为 Magic 3.0 重建

* Wed Jun 17 2015 Chris Leech <cleech@redhat.com> - 1.0.1-1.git986eb2e
- rebased to upstream v1.0.1-23-g986eb2e

* Thu Oct 23 2014 Chris Leech <cleech@redhat.com> - 0.9.46-8.git48a5f38
- sync to upstream v0.9.46-123-g48a5f38

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.46-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Peter Robinson <pbrobinson@fedoraproject.org> 0.9.46-6
- Add upstream patch to build against libnl3
- Drop legacy dcbd packaging support, we've not shipped it since F-13

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.46-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 11 2014 Petr Šabata <contyk@redhat.com> - 0.9.46-4
- Drop the explicit kernel runtime dependency
- Patch configure.ac to build in rawhide

* Wed Jul 31 2013 Petr Šabata <contyk@redhat.com> - 0.9.46-3
- Require 'systemd' instead of 'systemd-units'

* Tue Jul 02 2013 Petr Šabata <contyk@redhat.com> - 0.9.46-2
- Fix the hardened build flags

* Tue Jun 04 2013 Petr Šabata <contyk@redhat.com> - 0.9.46-1
- 0.9.46 bump
- 802.1Qaz fixes to enable support on not CEE DCBX-enabled hardware
- 802.1Qbg EVB module support
- lldpad now supports bonded interfaces

* Tue Mar 05 2013 Petr Šabata <contyk@redhat.com> - 0.9.45-5
- Fix build by patching the sizeof() call in lldp_8021qaz_cmds.c

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.45-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Aug 28 2012 Petr Šabata <contyk@redhat.com> - 0.9.45-3
- Migrate to systemd scriptlets (#850192)

* Thu Aug 23 2012 Petr Šabata <contyk@redhat.com> - 0.9.45-2
- Fix displaying of the Management Address TLV (327ef662)

* Wed Aug 15 2012 Petr Šabata <contyk@redhat.com> - 0.9.45-1
- 0.9.45 bump
- Provide bash-completion and the new clif library

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.44-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 27 2012 Petr Šabata <contyk@redhat.com> - 0.9.44-1
- 0.9.44 bump, patches cleanup
- Correct dependencies a bit
- Require dlopen()'d readline

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.43-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Oct 06 2011 Petr Sabata <contyk@redhat.com> - 0.9.43-5
- Do not enable lldpad by default (#701999)

* Fri Sep 23 2011 Petr Sabata <contyk@redhat.com> - 0.9.43-4
- Enable hardened build

* Tue Sep 13 2011 Petr Sabata <contyk@redhat.com> - 0.9.43-3
- Mute systemd output (#737897)

* Tue Aug 30 2011 Petr Sabata <contyk@redhat.com> - 0.9.43-2
- Apply various upstream 0.9.43 bugfixes
- Include not yet accepted Jens Osterkamp's patch to fix bug #720080
- Whitespace cleanup, phew

* Thu Jul 07 2011 Petr Sabata <contyk@redhat.com> - 0.9.43-1
- 0.9.43 bump
- Drop the the clean exit patch and our unit file, both are now included upstream

* Tue Jun 21 2011 Petr Sabata <contyk@redhat.com> - 0.9.42-2
- Introduce systemd unit file, drop SysV support
- Call systemctl instead of service and chkconfig
- Enable the service only on new installation (post)
- Clean exit patch

* Mon Jun 13 2011 Petr Sabata <contyk@redhat.com> - 0.9.42-1
- 0.9.42 bump (massive patches cleanup)
- Remove obsolete defattr
- Remove COPYING and README from devel subpackage

* Wed May  4 2011 Petr Sabata <psabata@redhat.com> - 0.9.41-3
- Fix the frequent, power consuming lldpad wake-ups (rhbz#701943)

* Thu Apr 21 2011 Petr Sabata <psabata@redhat.com> - 0.9.41-2
- Bring in upstream 802.1Qbg bugfixes

* Thu Feb 10 2011 Petr Sabata <psabata@redhat.com> - 0.9.41-1
- 0.9.41 bump
- New BR: autotools, flex
- Buildroot garbage removed
- Devel post and preun scriptlets sanitized

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.38-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jun 28 2010 Jan Zeleny <jzeleny@redhat.com> - 0.9.38-1
- rebased to 0.9.38 (various enhancements and bugfixes, see 
  lldpad-0.9.38-relnotes.txt on http://e1000.sf.net for complete list)

* Mon May 10 2010 Jan Zeleny <jzeleny@redhat.com> - 0.9.32-2
- rebuild to match new libconfig

* Mon Apr 12 2010 Jan Zeleny <jzeleny@redhat.com> - 0.9.32-1
- rebased to 0.9.32 (various enhancements and bugfixes, see 
  lldpad-0.9.32-relnotes.txt on http://e1000.sf.net for complete list)

* Thu Mar 25 2010 Jan Zeleny <jzeleny@redhat.com> - 0.9.29-2
- added Provides and Obsoletes tags to devel subpackage

* Mon Mar 15 2010 Jan Zeleny <jzeleny@redhat.com> - 0.9.29-1
- updated package to 0.9.29, improved compatibility with fcoe-utils

* Fri Feb 26 2010 Jan Zeleny <jzeleny@redhat.com> - 0.9.26-2
- updated spec file and LSB init script patch for re-review
  (#568641)

* Thu Feb 25 2010 Jan Zeleny <jzeleny@redhat.com> - 0.9.26-1
- rebased to 0.9.26
- package renamed to lldpad
- enahanced functionality (LLDP supported as well as DCBX)

* Fri Nov 13 2009 Jan Zeleny <jzeleny@redhat.com> - 0.9.19-2
- init script patch adding LSB compliance

* Thu Oct 08 2009 Jan Zeleny <jzeleny@redhat.com> - 0.9.19-1
- update to new upstream version

* Mon Oct 05 2009 Jan Zeleny <jzeleny@redhat.com> - 0.9.15-5
- replaced the last patch, which was not fully functional, with
  the new one

* Wed Sep 09 2009 Karsten Hopp <karsten@redhat.com> 0.9.15-4
- buildrequire libconfig-devel >= 1.3.2, it doesn't build with 1.3.1 due to
  the different config_lookup_string api

* Thu Aug 20 2009 Jan Zeleny <jzeleny@redhat.com> - 0.9.15-3
- update of config_lookup_string() function calls

* Thu Aug 20 2009 Jan Zeleny <jzeleny@redhat.com> - 0.9.15-2
- rebuild in order to match new libconfig

* Mon Aug 17 2009 Jan Zeleny <jzeleny@redhat.com> - 0.9.15-1
- rebase to 0.9.15

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Mar 20 2009 Jan Zeleny <jzeleny@redhat.com> - 0.9.7-4
- updated scriptlets in spec file to follow the rules

* Wed Mar 11 2009 Jan Zeleny <jzeleny@redhat.com> - 0.9.7-3
- added devel files again to support fcoe-utils package
- added kernel >= 2.6.29 to Requires, deleted dcbnl.h, since it is
  aviable in kernel 2.6.29-rc7
- changed config dir from /etc/sysconfig/dcbd to /etc/dcbd
- updated init script: added mandatory Short description tag,
  deleted default runlevels, which should start the script

* Tue Mar 10 2009 Jan Zeleny <jzeleny@redhat.com> - 0.9.7-2
- added patch to enable usage of libconfig shared in system
- removed devel part of package

* Mon Mar 2 2009 Chris Leech <christopher.leech@intel.com> - 0.9.7-1
- Updated to 0.9.7
- Added a private copy of dcbnl.h until kernel-headers includes it.
  Export patch is making it's way to the upstream kernel via net-2.6,
  expected in 2.6.29-rc7

* Thu Feb 26 2009 Chris Leech <christopher.leech@intel.com> - 0.9.5-1
- initial RPM packaging
