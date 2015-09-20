Name:         ipmitool
Summary:      Utility for IPMI control
Version:      1.8.13
Release:      8%{?dist}
License:      BSD
Group:        System Environment/Base
URL:          http://ipmitool.sourceforge.net/
Source0:      http://downloads.sourceforge.net/project/%{name}/%{name}/%{version}/%{name}-%{version}.tar.bz2
Source1:      openipmi-ipmievd.sysconf
Source2:      ipmievd.service
Source3:      exchange-bmc-os-info.service
Source4:      exchange-bmc-os-info.sysconf
Source5:      set-bmc-url.sh
Source6:      exchange-bmc-os-info

BuildRequires: openssl-devel readline-devel ncurses-devel
BuildRequires: systemd-units
# bootstrap
BuildRequires: automake autoconf libtool
Requires:OpenIPMI-modalias
Requires(post): systemd-sysv
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
Obsoletes: OpenIPMI-tools < 2.0.14-3
Provides: OpenIPMI-tools = 2.0.14-3

Patch1: ipmitool-1.8.10-ipmievd-init.patch
Patch2: ipmitool-1.8.10-ipmievd-condrestart.patch
Patch3: ipmitool-1.8.11-remove-umask0.patch
# various threads. still pending.
Patch4: cxoem-jb-cx6.patch
# pending
#Patch5: ipmitool-1.8.12-fips.patch
# pending
#Patch6: ipmitool-1.8.12-fipsman.patch
# pending https://sourceforge.net/p/ipmitool/bugs/280/
Patch7: ipmitool-1.8.13-dualbridgedoc.patch
# TODO
Patch8: ipmitool-1.8.13-envarg.patch

%description
This package contains a utility for interfacing with devices that support
the Intelligent Platform Management Interface specification.  IPMI is
an open standard for machine health, inventory, and remote power control.

This utility can communicate with IPMI-enabled devices through either a
kernel driver such as OpenIPMI or over the RMCP LAN protocol defined in
the IPMI specification.  IPMIv2 adds support for encrypted LAN
communications and remote Serial-over-LAN functionality.

It provides commands for reading the Sensor Data Repository (SDR) and
displaying sensor values, displaying the contents of the System Event
Log (SEL), printing Field Replaceable Unit (FRU) information, reading and
setting LAN configuration, and chassis power control.

%package -n bmc-snmp-proxy
Requires: net-snmp
Requires: exchange-bmc-os-info
Requires:OpenIPMI-modalias
BuildArch: noarch
Summary: Reconfigure SNMP to include host SNMP agent within BMC
%description -n bmc-snmp-proxy
Given a host with BMC, this package would extend system configuration
of net-snmp to include redirections to BMC based SNMP.


%package -n exchange-bmc-os-info
Requires: hostname
Requires: ipmitool OpenIPMI
Requires:OpenIPMI-modalias
BuildArch: noarch
Requires(post): systemd-sysv
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

Summary: Let OS and BMC exchange info

%description -n exchange-bmc-os-info
Given a host with BMC, this package would pass the hostname &
OS information to the BMC and also capture the BMC ip info
for the host OS to use.


%prep

%setup -q
%patch1 -p1 -b .ipmievd-init
%patch2 -p0 -b .condrestart
%patch3 -p1 -b .umask
%patch4 -p1 -b .cxoem
#patch5 -p0 -b .fips
#patch6 -p0 -b .fipsman
%patch7 -p1 -b .dualbridgedoc
%patch8 -p1 -b .argenv

for f in AUTHORS ChangeLog; do
    iconv -f iso-8859-1 -t utf8 < ${f} > ${f}.utf8
    mv ${f}.utf8 ${f}
done

%build
# --disable-dependency-tracking speeds up the build
# --enable-file-security adds some security checks
# --disable-intf-free disables FreeIPMI support - we don't want to depend on
#   FreeIPMI libraries, FreeIPMI has its own ipmitoool-like utility.

# begin: release auto-tools
# Used to be needed by aarch64 support, now only cxoem patch makefiles are left.
aclocal
libtoolize --automake --copy
autoheader
automake --foreign --add-missing --copy
aclocal
autoconf
automake --foreign
# end: release auto-tools

%configure --disable-dependency-tracking --enable-file-security --disable-intf-free
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

install -Dpm 644 %{SOURCE2} %{buildroot}%{_unitdir}/ipmievd.service
install -Dpm 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/sysconfig/ipmievd
install -Dm 644 %{SOURCE3} %{buildroot}%{_unitdir}/exchange-bmc-os-info.service
install -Dm 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/sysconfig/exchange-bmc-os-info
install -Dm 644 %{SOURCE5} %{buildroot}%{_sysconfdir}/profile.d/set-bmc-url.sh
install -Dm 755 %{SOURCE6} %{buildroot}%{_libexecdir}/exchange-bmc-os-info


install -Dm 644 contrib/bmc-snmp-proxy.sysconf %{buildroot}%{_sysconfdir}/sysconfig/bmc-snmp-proxy
install -Dm 644 contrib/bmc-snmp-proxy.service %{buildroot}%{_unitdir}/bmc-snmp-proxy.service
install -Dm 755 contrib/bmc-snmp-proxy         %{buildroot}%{_libexecdir}/bmc-snmp-proxy

%post
%systemd_post ipmievd.service

%preun
%systemd_preun ipmievd.service

%postun
%systemd_postun_with_restart ipmievd.service

%post -n exchange-bmc-os-info
%systemd_post exchange-bmc-os-info.service

%preun -n exchange-bmc-os-info
%systemd_preun exchange-bmc-os-info.service

%postun -n exchange-bmc-os-info
%systemd_postun_with_restart exchange-bmc-os-info.service


%triggerun -- ipmievd < 1.8.11-7
# Save the current service runlevel info
# User must manually run systemd-sysv-convert --apply ipmievd
# to migrate them to systemd targets
/usr/bin/systemd-sysv-convert --save ipmievd >/dev/null 2>&1 ||:

# Run these because the SysV package being removed won't do them
/sbin/chkconfig --del ipmievd >/dev/null 2>&1 || :
/bin/systemctl try-restart ipmievd.service >/dev/null 2>&1 || :

%files
%config(noreplace) %{_sysconfdir}/sysconfig/ipmievd
%{_unitdir}/ipmievd.service
%{_bindir}/*
%{_sbindir}/*
%{_mandir}/man*/*
%doc %{_datadir}/doc/ipmitool
%{_datadir}/ipmitool

%files -n exchange-bmc-os-info
%config(noreplace) %{_sysconfdir}/sysconfig/exchange-bmc-os-info
%{_sysconfdir}/profile.d/set-bmc-url.sh
%{_unitdir}/exchange-bmc-os-info.service
%{_libexecdir}/exchange-bmc-os-info

%files -n bmc-snmp-proxy
%config(noreplace) %{_sysconfdir}/sysconfig/bmc-snmp-proxy
%{_unitdir}/bmc-snmp-proxy.service
%{_libexecdir}/bmc-snmp-proxy

%changelog
* Sat Sep 19 2015 Liu Di <liudidi@gmail.com> - 1.8.13-8
- 为 Magic 3.0 重建

* Mon Sep 15 2014 Liu Di <liudidi@gmail.com> - 1.8.13-7
- 为 Magic 3.0 重建

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.13-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.13-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr  8 2014 Ales Ledvinka <aledvink@redhat.com> 1.8.13-4
- Support for environment variable short options.

* Tue Nov  5 2013 Ales Ledvinka <aledvink@redhat.com> 1.8.13-3
- Cleanup of dual bridge option.

* Tue Oct 15 2013 Ales Ledvinka <aledvink@redhat.com> 1.8.13-2
- BMC SNMP agent redirection

* Mon Oct 14 2013 Ales Ledvinka <aledvink@redhat.com> 1.8.13-1
- Upstream release 1.8.13

* Fri Aug 09 2013 Ales Ledvinka <aledvink@redhat.com> 1.8.12-13073103
- Avoid FIPS mode crashes if possible.
- Document FIPS limitations.

* Wed Jul  31 2013 Ales Ledvinka <aledvink@redhat.com> 1.8.12-13073101
- Include current upstream bugfixes.

* Thu Jul 25 2013 Ales Ledvinka <aledvink@redhat.com> 1.8.12-16
- Calxeda OEM extensions.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.12-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Dec 17 2012 Praveen K Paladugu <praveen_paladugu@dell.com> - 1.8.12-14
- Updated the exchange-bmc-os-info's service file with Requires stmt

* Fri Dec 14 2012 Ales Ledvinka <aledvink@redhat.com> 1.8.12-13
- fixed argument parsing leaks
- ask user for password only once and do so only when interactive password
  is the chosen password method.

* Thu Dec 13 2012 Praveen K Paladugu <praveen_paladugu@dell.com> - 1.8.12-12
- Removed the extra symbols in the patch, as the build is failing.

* Thu Dec 13 2012 Praveen K Paladugu <praveen_paladugu@dell.com> - 1.8.12-11
- Subpackage for exchange-bmc-os-info as it requires OPenIPMI

* Wed Dec 12 2012 Ales Ledvinka <aledvink@redhat.com> 1.8.12-10
- documented fixed and conditional defaults. adjusted synopsis

* Tue Dec 4 2012 Ales Ledvinka <aledvink@redhat.com> 1.8.12-9
- fixed ipmitool documentation

* Fri Nov 30 2012 Praveen K Paladugu <praveen_paladugu@dell.com> 1.8.12-8
- service & scripts to allow OS to capture BMC's IP & URL info
- Also pass the OS information to BMC
- patches submitted by Charles Rose (charles_rose[at]dell.com)

* Fri Nov 16 2012 Ales Ledvinka <aledvink@redhat.com> 1.8.12-7
- failed sol session activation crashes while logging exit

* Fri Nov 16 2012 Ales Ledvinka <aledvink@redhat.com> 1.8.12-6
- revert default cipersuite back to 3 which includes integrity and confidentiality

* Thu Oct 18 2012 Dan Horák <dan[at]danny.cz> - 1.8.12-5
- fix build on big endian arches

* Wed Oct 17 2012 Ales Ledvinka <aledvink@redhat.cz> 1.8.12-4
- support setting OS name and Hostname on BMC

* Tue Sep 04 2012 Dan Horák <dan[at]danny.cz> - 1.8.12-3
- fix build on big endian arches

* Mon Aug 27 2012 Jan Safranek <jsafrane@redhat.com> - 1.8.12-2
- Fixed starting ipmievd under systemd (#819234).
- Updated RPM scriplets with latest systemd-rpm macros (#850161)

* Fri Aug 10 2012 Jan Safranek <jsafrane@redhat.com> - 1.8.12-1
- update to ipmitool-1.8.12

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.11-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 22 2012 Jan Safranek <jsafrane@redhat.com> - 1.8.11-11
- start ipmievd.service after ipmi (#819234)

* Thu Apr 26 2012 Jan Safranek <jsafrane@redhat.com> - 1.8.11-10
- fixed ipmievd.service systemd unit (#807757)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.11-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 13 2011 Jan Safranek <jsafrane@redhat.com> - 1.8.11-8
- fixed CVE-2011-4339

* Mon Sep 12 2011 Tom Callaway <spot@fedoraproject.org> - 1.8.11-7
- convert to systemd

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Mar  3 2010 Jan Safranek <jsafrane@redhat.com> - 1.8.11-5
- Fixed exit code of ipmievd initscript with wrong arguments

* Mon Nov  2 2009 Jan Safranek  <jsafrane@redhat.com> 1.8.11-4
- fix ipmievd initscript 'condrestart' action (#532188)

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 1.8.11-3
- rebuilt with new openssl

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Jan Safranek <jsafrane@redhat.com> 1.8.11-1
- updated to new version

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> 1.8.10-3
- rebuild with new openssl

* Tue Oct 14 2008 Jan Safranek <jsafrane@redhat.com> 1.8.10-2
- fix issues found during package review:
  - clear Default-Start: line in the init script, the service should be 
    disabled by default
  - added Obsoletes: OpenIPMI-tools
  - compile with --disable-dependency-tracking to speed things up
  - compile with --enable-file-security
  - compile with --disable-intf-free, don't depend on FreeIPMI libraries
    (FreeIPMI has its own ipmitool-like utility)

* Mon Oct 13 2008 Jan Safranek <jsafrane@redhat.com> 1.8.10-1
- package created, based on upstream .spec file
