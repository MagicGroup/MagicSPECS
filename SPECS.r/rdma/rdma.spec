#  Copyright (c) 2008 Red Hat, Inc.

#  There is no URL or upstream source entry as this package constitutes
#  upstream for itself.

Summary: Infiniband/iWARP Kernel Module Initializer
Name: rdma
Version: 2.0
Release: 16%{?dist}
License: GPLv2+
Group: System Environment/Base
Source0: rdma.conf
Source1: rdma.udev-ipoib-naming.rules
Source2: rdma.fixup-mtrr.awk
Source4: rdma.ifup-ib
Source5: rdma.ifdown-ib
Source6: rdma.service
Source7: rdma.kernel-init
Source8: rdma.udev-rules
Source9: rdma.modules-setup.sh
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
BuildRequires: systemd-units
Requires: udev >= 095
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
%global dracutlibdir %{_prefix}/lib/dracut

%description 
User space initialization scripts for the kernel InfiniBand/iWARP drivers

%prep

%build

%install
rm -rf %{buildroot}
install -d %{buildroot}%{_sysconfdir}/%{name}
install -d %{buildroot}%{_sysconfdir}/udev/rules.d
install -d %{buildroot}%{_sysconfdir}/sysconfig/network-scripts
install -d %{buildroot}%{_libexecdir}
install -d %{buildroot}%{_unitdir}
install -d %{buildroot}%{_udevrulesdir}
install -d %{buildroot}%{dracutlibdir}/modules.d/05rdma

# Stuff to go into the base package
install -m 0644 %{SOURCE0} %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf
install -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/udev/rules.d/70-persistent-ipoib.rules
install -m 0644 %{SOURCE6} %{buildroot}%{_unitdir}/rdma.service
install -m 0755 %{SOURCE7} %{buildroot}%{_libexecdir}/rdma-init-kernel
install -m 0644 %{SOURCE2} %{buildroot}%{_libexecdir}/rdma-fixup-mtrr.awk
install -m 0755 %{SOURCE4} %{buildroot}%{_sysconfdir}/sysconfig/network-scripts/ifup-ib
install -m 0755 %{SOURCE5} %{buildroot}%{_sysconfdir}/sysconfig/network-scripts/ifdown-ib
install -m 0644 %{SOURCE8} %{buildroot}%{_udevrulesdir}/98-rdma.rules
install -m 0755 %{SOURCE9} %{buildroot}%{dracutlibdir}/modules.d/05rdma/module-setup.sh

%clean
rm -rf %{buildroot}

%post
%systemd_post rdma.service

%preun
%systemd_preun rdma.service

%postun
%systemd_postun

%files
%defattr(-,root,root,-)
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%config(noreplace) %{_sysconfdir}/udev/rules.d/*
%{_unitdir}/%{name}.service
%{_libexecdir}/rdma-init-kernel
%{_libexecdir}/rdma-fixup-mtrr.awk
%{_sysconfdir}/sysconfig/network-scripts/*
%{_udevrulesdir}/*
%dir %{dracutlibdir}/modules.d/05rdma
%{dracutlibdir}/modules.d/05rdma/module-setup.sh

%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jul 22 2014 Doug Ledford <dledford@redhat.com> - 2.0-15
- Fold in improvements made in the rhel7 tree back to Fedora

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Nov 26 2013 Doug Ledford <dledford@redhat.com> - 2.0-13
- Fix bug in ifdown-ib script handling of P_Key devs
- Move setting of node_desc to udev rules and make it more reliable
- Only load RDS if rds kernel module exists as we've disabled it
  in some places

* Tue Jul 30 2013 Doug Ledford <dledford@redhat.com> - 2.0-12
- Change VLAN/PKEY in ifup/ifdown scripts.  Overloading VLAN was
  causing problems

* Thu May 23 2013 Doug Ledford <dledford@redhat.com> - 2.0-11
- Oops, didn't update ifdown-ib to match latest ifup-ib

* Thu May 23 2013 Doug Ledford <dledford@redhat.com> - 2.0-10
- More fixups for ifup-ib and P_Key support
- Move persistent-ipoib.rules to 70 instead of 60 to match prior
  persistent-net.rules file numbering

* Wed May 22 2013 Doug Ledford <dledford@redhat.com> - 2.0-9
- Add support for P_Key interfaces (IPoIB version of VLANs)
- Add sample 60-persistent-ipoib.rules file

* Mon Mar 25 2013 Doug Ledford <dledford@redhat.com> - 2.0-8
- Drop the sysv package
- Add the SRPT module to the conf file and startup script
- Add support for the new ocrdma driver from Emulex

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Dec 05 2012 Doug Ledford <dledford@redhat.com> - 2.0-6
- Add some proper systemd scriptlets
- Resolves: bz820154, bz816073, bz816389

* Tue Nov 27 2012 Doug Ledford <dledford@redhat.com> - 2.0-5
- Oops, we really do need that install section in our service file, so
  put it back

* Tue Nov 27 2012 Doug Ledford <dledford@redhat.com> - 2.0-4
- Don't add an Install section to our service file, that way we aren't
  started unless our hardware is detected

* Mon Nov 26 2012 Doug Ledford <dledford@redhat.com> - 2.0-3
- Minor corrections to systemd service file

* Mon Nov 26 2012 Doug Ledford <dledford@redhat.com> - 2.0-2
- Minor whitespace cleanups
- Correct the usage of MTRR_SCRIPT in rdma-init-kernel
- Remove no longer relevant sections of config related to NFSoRDMA
  (now handled by nfs-utils-rdma)

* Mon Nov 26 2012 Doug Ledford <dledford@redhat.com> - 2.0-1
- Update version to reflect addition of systemd support

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 28 2012 Doug Ledford <dledford@redhat.com> - 1.0-11
- Remove udev rules file, recent kernels create the proper devices without
  need of the file
- Remove the nfs-rdma init script so it can be taken over by the nfs-utils
  package
- Fix up some LSB header bogons in the init script (will convert to
  systemd after this is tested and working and move sysv init script
  to a sub-package)
- Add ifdown-ib and update ifup-ib so we have more of the same capabilities
  on IPoIB interfaces that RHEL has

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Aug 02 2010 Doug Ledford <dledford@redhat.com> - 1.0-8
- Update udev rules syntax to eliminate warnings emitted via syslog (bz603264)
- Add new init script for starting/stopping nfs over rdma support
- Require that the nfs-rdma service be down before stopping the rdma
  service (bz613437)
- Change ifup-ib to properly account for the fact that the [ test program
  does not process tests in order and fail immediately on first failing
  test, resulting in error messages due to unquoted environment variables
  that don't need quoting in the second test due to the fact that the
  first test guarantees they exist.  Or that's how things should be, but
  they aren't, so rewrite tests to accommodate this fact. (bz612284)
- Use ip instead of ifconfig as ifconfig knows it doesn't handle infinband
  hardware addresses properly (even though we don't care, we aren't using
  it for that) and prints out copious warning messages (bz613086)
  
* Thu Feb 25 2010 Doug Ledford <dledford@redhat.com> - 1.0-7
- Minor tweak to rdma.init to silence udev warnings (bz567981)

* Tue Dec 01 2009 Doug Ledford <dledford@redhat.com> - 1.0-6
- Tweak init script for LSB compliance
- Tweak ifup-ib script to work properly with bonded slaves that need their
  MTU set
- Tweak ifup-ib script to properly change connected mode either on or off
  instead of only setting it on but not turning it off if the setting changes

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Oct 09 2008 Doug Ledford <dledford@redhat.com> - 1.0-3
- Add the ifup-ib script so we support connected mode on ib interfaces

* Mon Jun 09 2008 Doug Ledford <dledford@redhat.com> - 1.0-2
- Attempt to use --subsystem-match=infiniband in the rdma init script use
  of udevtrigger so we don't trigger the whole system
- Add a requirement to stop opensm to the init script

* Sun Jun 08 2008 Doug Ledford <dledford@redhat.com> - 1.0-1
- Create an initial package for Fedora review

