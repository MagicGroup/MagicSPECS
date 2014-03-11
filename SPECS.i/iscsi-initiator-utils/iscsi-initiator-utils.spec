%global _hardened_build 1
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%define open_iscsi_version	2.0
%define open_iscsi_build	873
%define iscsiuio_version	0.7.2.1

Summary: iSCSI daemon and utility programs
Name: iscsi-initiator-utils
Version: 6.%{open_iscsi_version}.%{open_iscsi_build}
Release: 7%{?dist}
Source0: http://www.open-iscsi.org/bits/open-iscsi-%{open_iscsi_version}-%{open_iscsi_build}.tar.gz
Source1: iscsiuio-%{iscsiuio_version}.tar.gz
Source4: 04-iscsi
Source5: iscsi-tmpfiles.conf

# upstream patches, post last tagged version
Patch1: 0001-iscsid-fix-iscsid-segfault-during-qla4xxx-login.patch
Patch2: 0002-ISCSISTART-Bring-up-the-corresponding-network-interf.patch
Patch3: 0003-iscsi-tools-fix-compile-error-when-OFFLOAD_BOOT_SUPP.patch
Patch4: 0004-ISCSID-Passing-more-net-params-from-ibft-to-iface.patch
Patch5: 0005-iscsi-tools-Convert-r-argument-to-an-integer-before-.patch
Patch6: 0006-Update-README-for-removal-of-DBM-requirement.patch
Patch7: 0007-iscsid-iscsiadm-fix-abstract-socket-length-in-bind-c.patch
Patch8: 0008-iscsid-implement-systemd-compatible-socket-activatio.patch
Patch9: 0009-iscsid-add-example-unit-files-for-systemd.patch
Patch10: 0010-iscsi-tools-fix-get_random_bytes-error-handling.patch
# pending upstream merge
Patch31: 0031-iscsid-add-initrd-option-to-set-run-from-initrd-hint.patch
Patch32: 0032-iscsiadm-iscsid-newroot-command-to-survive-switch_ro.patch
Patch33: 0033-iscsiadm-param-parsing-for-advanced-node-creation.patch
Patch34: 0034-update-systemd-service-files-add-iscsi.service-for-s.patch
# distro specific modifications
Patch51: 0051-update-initscripts-and-docs.patch
Patch52: 0052-use-var-for-config.patch
Patch53: 0053-use-red-hat-for-name.patch
Patch54: 0054-add-libiscsi.patch
Patch55: 0055-dont-use-static.patch
Patch56: 0056-remove-the-offload-boot-supported-ifdef.patch
Patch57: 0057-iscsid-iscsiuio-ipc-interface.patch
Patch58: 0058-iscsiuio-IPC-newroot-command.patch
Patch59: 0059-iscsiuio-systemd-unit-files.patch
Patch60: 0060-use-systemctl-to-start-iscsid.patch
Patch61: 0061-resolve-565245-multilib-issues-caused-by-doxygen.patch
Patch62: 0062-Don-t-check-for-autostart-sessions-if-iscsi-is-not-u.patch
Patch63: 0063-fix-order-of-setting-uid-gid-and-drop-supplementary-.patch
# iscsiuio patches
Patch71: 0071-iscsiuio-0.7.4.3.patch
Patch72: 0072-iscsiuio-0.7.6.1.patch
Patch73: 0073-iscsiuio-fix-long-options.patch
Patch74: 0074-iscsiuio-add-initrd-option-to-set-run-from-initrd-hi.patch
Patch75: 0075-iscsiuio-systemd-socket-activation-support.patch
Patch76: 0076-iscsiuio-iscsid-IPC-newroot-command.patch
Patch77: 0077-iscsiuio-document-pidfile-option.patch
# version string, needs to be updated with each build
Patch99: 0099-use-Red-Hat-version-string-to-match-RPM-package-vers.patch


Group: System Environment/Daemons
License: GPLv2+
URL: http://www.open-iscsi.org
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: openssl-devel flex bison python-devel doxygen glibc-static kmod-devel
# For dir ownership
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
The iscsi package provides the server daemon for the iSCSI protocol,
as well as the utility programs used to manage it. iSCSI is a protocol
for distributed disk access using SCSI commands sent over Internet
Protocol networks.

%package devel
Summary: Development files for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n open-iscsi-%{open_iscsi_version}-%{open_iscsi_build} -a 1
mv iscsiuio-%{iscsiuio_version} iscsiuio
# upstream patches
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
# pending upstream merge
%patch31 -p1
%patch32 -p1
%patch33 -p1
%patch34 -p1
# distro specific modifications
%patch51 -p1
%patch52 -p1
%patch53 -p1
%patch54 -p1
%patch55 -p1
%patch56 -p1
%patch57 -p1
%patch58 -p1
%patch59 -p1
%patch60 -p1
%patch61 -p1
%patch62 -p1
%patch63 -p1
# iscsiuio patches
cd iscsiuio
%patch71 -p1
%patch72 -p1
%patch73 -p1
%patch74 -p1
%patch75 -p1
%patch76 -p1
%patch77 -p1
cd ..
# version string
%patch99 -p1


%build
make OPTFLAGS="%{optflags} %{?__global_ldflags} -DUSE_KMOD -lkmod"

cd iscsiuio
chmod u+x configure
./configure --enable-debug
make OPTFLAGS="%{optflags}" LDFLAGS="%{?__global_ldflags}" CFLAGS="$RPM_OPT_FLAGS" CXXFLAGS="$RPM_OPT_FLAGS"

cd ..

pushd libiscsi
python setup.py build
touch -r libiscsi.doxy html/*
popd


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/sbin
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man8
mkdir -p $RPM_BUILD_ROOT/etc/iscsi
mkdir -p $RPM_BUILD_ROOT/etc/logrotate.d
mkdir -p $RPM_BUILD_ROOT/etc/NetworkManager/dispatcher.d
mkdir -p $RPM_BUILD_ROOT/var/lib/iscsi
mkdir -p $RPM_BUILD_ROOT/var/lib/iscsi/nodes
mkdir -p $RPM_BUILD_ROOT/var/lib/iscsi/send_targets
mkdir -p $RPM_BUILD_ROOT/var/lib/iscsi/static
mkdir -p $RPM_BUILD_ROOT/var/lib/iscsi/isns
mkdir -p $RPM_BUILD_ROOT/var/lib/iscsi/slp
mkdir -p $RPM_BUILD_ROOT/var/lib/iscsi/ifaces
mkdir -p $RPM_BUILD_ROOT/var/lock/iscsi
mkdir -p $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_includedir}
mkdir -p $RPM_BUILD_ROOT%{python_sitearch}



install -p -m 755 usr/iscsid usr/iscsiadm utils/iscsi-iname usr/iscsistart $RPM_BUILD_ROOT/sbin
install -p -m 644 doc/iscsiadm.8 $RPM_BUILD_ROOT/%{_mandir}/man8
install -p -m 644 doc/iscsid.8 $RPM_BUILD_ROOT/%{_mandir}/man8
install -p -m 644 etc/iscsid.conf $RPM_BUILD_ROOT%{_sysconfdir}/iscsi
install -p -m 644 doc/iscsistart.8 $RPM_BUILD_ROOT/%{_mandir}/man8
install -p -m 644 doc/iscsi-iname.8 $RPM_BUILD_ROOT/%{_mandir}/man8
install -p -m 644 iscsiuio/docs/iscsiuio.8 $RPM_BUILD_ROOT/%{_mandir}/man8
install -p -m 644 iscsiuio/iscsiuiolog $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
install -p -m 755 iscsiuio/src/unix/iscsiuio $RPM_BUILD_ROOT/sbin

install -p -D -m 644 etc/systemd/iscsi.service $RPM_BUILD_ROOT%{_unitdir}/iscsi.service
install -p -D -m 644 etc/systemd/iscsid.service $RPM_BUILD_ROOT%{_unitdir}/iscsid.service
install -p -D -m 644 etc/systemd/iscsid.socket $RPM_BUILD_ROOT%{_unitdir}/iscsid.socket
install -p -D -m 644 etc/systemd/iscsiuio.service $RPM_BUILD_ROOT%{_unitdir}/iscsiuio.service
install -p -D -m 644 etc/systemd/iscsiuio.socket $RPM_BUILD_ROOT%{_unitdir}/iscsiuio.socket
install -p -D -m 755 etc/systemd/iscsi_mark_root_nodes $RPM_BUILD_ROOT/usr/libexec/iscsi_mark_root_nodes
install -p -m 755 %{SOURCE4} $RPM_BUILD_ROOT/etc/NetworkManager/dispatcher.d
install -p -D -m 644 %{SOURCE5} $RPM_BUILD_ROOT/usr/lib/tmpfiles.d/iscsi.conf

install -p -m 755 libiscsi/libiscsi.so.0 $RPM_BUILD_ROOT%{_libdir}
ln -s libiscsi.so.0 $RPM_BUILD_ROOT%{_libdir}/libiscsi.so
install -p -m 644 libiscsi/libiscsi.h $RPM_BUILD_ROOT%{_includedir}

install -p -m 755 libiscsi/build/lib.linux-*/libiscsimodule.so \
	$RPM_BUILD_ROOT%{python_sitearch}

# for %%ghost
touch $RPM_BUILD_ROOT/var/lock/iscsi/lock


%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig

%systemd_post iscsi.service iscsid.service iscsiuio.service iscsid.socket iscsiuio.socket

if [ $1 -eq 1 ]; then
	if [ ! -f %{_sysconfdir}/iscsi/initiatorname.iscsi ]; then
		echo "InitiatorName=`/sbin/iscsi-iname`" > %{_sysconfdir}/iscsi/initiatorname.iscsi
	fi
	# enable socket activation and persistant session startup by default
	/bin/systemctl enable iscsi.service >/dev/null 2>&1 || :
	/bin/systemctl enable iscsid.socket >/dev/null 2>&1 || :
	/bin/systemctl enable iscsiuio.socket >/dev/null 2>&1 || :
fi

%preun
%systemd_preun iscsi.service iscsid.service iscsiuio.service iscsid.socket iscsiuio.socket

%postun
/sbin/ldconfig
%systemd_postun

%triggerun -- iscsi-initiator-utils < 6.2.0.873-1
# Save the current service runlevel info
# User must manually run systemd-sysv-convert --apply iscsid
# and systemd-sysv-convert --apply iscsi
# to migrate them to systemd targets
/usr/bin/systemd-sysv-convert --save iscsi >/dev/null 2>&1 ||:
/usr/bin/systemd-sysv-convert --save iscsid >/dev/null 2>&1 ||:

# enable socket activation
/bin/systemctl enable iscsid.socket >/dev/null 2>&1 || :
/bin/systemctl enable iscsiuio.socket >/dev/null 2>&1 || :

# Run these because the SysV package being removed won't do them
/sbin/chkconfig --del iscsid >/dev/null 2>&1 || :
/sbin/chkconfig --del iscsi >/dev/null 2>&1 || :
/bin/systemctl try-restart iscsid.service >/dev/null 2>&1 || :
/bin/systemctl try-restart iscsi.service >/dev/null 1>&1 || :

%files
%defattr(-,root,root)
%doc README
%dir %{_var}/lib/iscsi
%dir %{_var}/lib/iscsi/nodes
%dir %{_var}/lib/iscsi/isns
%dir %{_var}/lib/iscsi/static
%dir %{_var}/lib/iscsi/slp
%dir %{_var}/lib/iscsi/ifaces
%dir %{_var}/lib/iscsi/send_targets
%ghost %{_var}/lock/iscsi
%ghost %{_var}/lock/iscsi/lock
%{_unitdir}/iscsi.service
%{_unitdir}/iscsid.service
%{_unitdir}/iscsid.socket
%{_unitdir}/iscsiuio.service
%{_unitdir}/iscsiuio.socket
/usr/libexec/iscsi_mark_root_nodes
%{_sysconfdir}/NetworkManager/dispatcher.d/04-iscsi
/usr/lib/tmpfiles.d/iscsi.conf
%dir %{_sysconfdir}/iscsi
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/iscsi/iscsid.conf
/sbin/*
%{_libdir}/libiscsi.so.0
%{python_sitearch}/libiscsimodule.so
%{_mandir}/man8/*
%{_sysconfdir}/logrotate.d/iscsiuiolog

%files devel
%defattr(-,root,root,-)
%doc libiscsi/html
%{_libdir}/libiscsi.so
%{_includedir}/libiscsi.h

%changelog
* Tue Jun 11 2013 Chris Leech <cleech@redhat.com> - 6.2.0.873-7
- Use the systemd tmpfiles service to recreate lockfiles in /var/lock
- 955167 build as a position independent executable
- 894576 fix order of setuid/setgid and drop additional groups

* Tue May 28 2013 Chris Leech <cleech@redhat.com> - 6.2.0.873-6
- Don't have iscsiadm scan for autostart record if node db is empty (bug #951951)

* Tue Apr 30 2013 Orion Poplawski <orion@cora.nwra.com> - 6.2.0.873-5
- Fix typo in NM dispatcher script (bug #917058)

* Thu Feb 21 2013 Chris Leech <cleech@redhat.com> - 6.2.0.873-4
- build with libkmod support, instead of calling out to modprobe
- enable socket activation by default

* Thu Jan 24 2013 Kalev Lember <kalevlember@gmail.com> - 6.2.0.873-3
- Fix the postun script to not use ldconfig as the interpreter

* Wed Jan 23 2013 Chris Leech <cleech@redhat.com> - 6.2.0.873-2
- package iscsi_mark_root_nodes script, it's being referenced by the unit files

* Tue Jan 22 2013 Chris Leech <cleech@redhat.com> - 6.2.0.873-1
- rebase to new upstream code
- systemd conversion
- 565245 Fix multilib issues caused by timestamp in doxygen footers

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.2.0.872-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Feb 14 2012 Mike Christie <mchristi@redhat.com> 6.2.0.872.18
- 789683 Fix boot slow down when the iscsi service is started
  (regression added in 6.2.0.872.16 when the nm wait was added).

* Mon Feb 5 2012 Mike Christie <mchristi@redhat.com> 6.2.0.872.17
- 786174 Change iscsid/iscsi service startup, so it always starts
  when called.

* Sat Feb 4 2012 Mike Christie <mchristi@redhat.com> 6.2.0.872.16
- 747479 Fix iscsidevs handling of network requirement

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.2.0.872-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 30 2011 Mike Christie <mcrhsit@redhat.com> 6.2.0.872.14
- Fix version string to reflect fedora and not rhel.

* Tue Oct 18 2011 Mike Christie <mcrhsit@redhat.com> 6.2.0.872.13
- Update iscsi tools.

* Sat Apr 30 2011 Hans de Goede <hdegoede@redhat.com> - 6.2.0.872-12
- Change iscsi init scripts to check for networking being actually up, rather
  then for NetworkManager being started (#692230)

* Tue Apr 26 2011 Hans de Goede <hdegoede@redhat.com> - 6.2.0.872-11
- Fix iscsid autostarting when upgrading from an older version
  (add iscsid.startup key to iscsid.conf on upgrade)
- Fix printing of [ OK ] when successfully stopping iscsid
- systemd related fixes:
 - Add Should-Start/Stop tgtd to iscsi init script to fix (re)boot from
   hanging when using locally hosted targets
 - %%ghost /var/lock/iscsi and contents (#656605)

* Mon Apr 25 2011 Mike Christie <mchristi@redhat.com> 6.2.0.872-10
- Fix iscsi init scripts check for networking being up (#692230)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.2.0.872-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 6.2.0.872-8
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Jul 12 2010 Mike Christie <mchristi@redhat.com> 6.2.0.872.7
- Sync to upstream open-iscsi-2.0-872-rc4 which fixes:
  iscsiadm discovery port handling, add discoveryd init script
  support, move from iscsid.conf to discovery db discoveryd settings,
  and add discoverydb mode support.

* Thu Jun 10 2010 Mike Christie <mchristi@redhat.com> 6.2.0.872.6
- Fix last patch.

* Wed Jun 9 2010 Mike Christie <mchristi@redhat.com> 6.2.0.872.5
- Fix iscsiadm handling of port argument when it is not the default 3260.

* Thu May 6 2010 Mike Christie <mchristi@redhat.com> 6.2.0.872.4
- Fix iscsi script operations to check for offload drivers in rh_status
- Fix iscsiadm logging to not trigger iscsi script error detection

* Wed May 5 2010 Mike Christie <mchristi@redhat.com> 6.2.0.872.3
- 578455 Fix initial R2T=0 handling for be2iscsi

* Wed Mar 31 2010 Mike Christie <mchristi@redhat.com> 6.2.0.872.2
- 578455 Fix handling of MaxXmitDataSegmentLength=0 for be2iscsi

* Wed Mar 31 2010 Mike Christie <mchristi@redhat.com> 6.2.0.872.1
- 578455 Fix handling of MaxXmitDataSegmentLength=0

* Wed Mar 24 2010 Mike Christie <mchristi@redhat.com> 6.2.0.872.0
- 516444 Add iSNS SCN handling (rebased to open-iscsi-2.0-872-rc1-)
- Update brcm to 0.5.7

* Sun Feb 14 2010 Hans de Goede <hdegoede@redhat.com> 6.2.0.870-13
- Preserve timestamps on doxygen generated files
- Fix FTBFS (#565038)

* Mon Feb 8 2010 Mike Christie <mchristi@redhat.com> 6.2.0.871.1.1-3
- Add spec patch comments.

* Thu Jan 21 2010 Mike Christie <mchristi@redhat.com> 6.2.0.871.1.1-2
- 556985 Fix up init.d iscsid script to remove offload modules and
  load be2iscsi.
- Enable s390/s390x

* Fri Jan 15 2010 Mike Christie <mchristi@redhat.com> 6.2.0.871.1.1-1
- Sync to upstream
- 529324 Add iscsi-iname and iscsistart man page
- 463582 OF/iBFT support

* Thu Jan  7 2010 Hans de Goede <hdegoede@redhat.com> 6.2.0.870-12
- Change python_sitelib macro to use %%global as the new rpm will break
  using %%define here, see:
  https://www.redhat.com/archives/fedora-devel-list/2010-January/msg00093.html

* Tue Dec  1 2009 Hans de Goede <hdegoede@redhat.com> 6.2.0.870-11
- Own /etc/iscsi (#542849)
- Do not own /etc/NetworkManager/dispatcher.d (#533700)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.2.0.870-10.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri May 22 2009 Dan Horak <dan[at]danny.cz> 6.2.0.870-9.1
- drop the s390/s390x ExcludeArch

* Mon Apr 27 2009 Hans de Goede <hdegoede@redhat.com> 6.2.0.870-9
- Don't crash when asked to parse the ppc firmware table more then
  once (which can be done from libiscsi) (#491363)

* Fri Apr  3 2009 Hans de Goede <hdegoede@redhat.com> 6.2.0.870-8
- Stop the NM script from exiting with an error status when it
  didn't do anything (#493411)

* Fri Mar 20 2009 Hans de Goede <hdegoede@redhat.com> 6.2.0.870-7
- libiscsi: use fwparam_ibft_sysfs() instead of fw_get_entry(), as
  the latter causes stack corruption (workaround #490515)

* Sat Mar 14 2009 Terje Rosten <terje.rosten@ntnu.no> - 6.2.0.870-6
- Add glibc-static to buildreq to build in F11

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.2.0.870-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 12 2009 Hans de Goede <hdegoede@redhat.com> 6.2.0.870-4
- Fix libiscsi.discover_sendtargets python method to accept None as valid
  authinfo argument (#485217)

* Wed Jan 28 2009 Hans de Goede <hdegoede@redhat.com> 6.2.0.870-3
- Fix reading of iBFT firmware with newer kernels

* Wed Jan 28 2009 Hans de Goede <hdegoede@redhat.com> 6.2.0.870-2
- Add libiscsi iscsi administration library and -devel subpackage

* Tue Nov  25 2008 Mike Christie <mchristie@redhat.com> 6.2.0.870-1.0
- Rebase to upstream

* Thu Nov  6 2008 Hans de Goede <hdegoede@redhat.com> 6.2.0.870-0.2.rc1
- Add force-start iscsid initscript option and use that in "patch to make
  iscsiadm start iscsid when needed" so that iscsid will actual be started
  even if there are no iscsi disks configured yet (rh 470437)
- Do not start iscsid when not running when iscsiadm -k 0 gets executed
  (rh 470438)

* Tue Sep 30 2008 Hans de Goede <hdegoede@redhat.com> 6.2.0.870-0.1.rc1
- Rewrite SysV initscripts, fixes rh 441290, 246960, 282001, 436175, 430791
- Add patch to make iscsiadm complain and exit when run as user instead
  of hang spinning for the database lock
- Add patch to make iscsiadm start iscsid when needed (rh 436175 related)
- Don't start iscsi service when network not yet up (in case of using NM)
  add NM dispatcher script to start iscsi service once network is up

* Mon Jun 30 2008 Mike Christie <mchristie@redhat.com> - 6.2.0.870
- Rebase to open-iscsi-2-870
- 453282 Handle sysfs changes.

* Fri Apr 25 2008 Mike Christie <mchristie@redhat.com> - 6.2.0.868-0.7
- 437522 log out sessions that are not used for root during "iscsi stop".

* Fri Apr 4 2008 Mike Christie <mchristie@redhat.com> - 6.2.0.868-0.6
- Rebase to RHEL5 to bring in bug fixes.
- 437522 iscsi startup does not need to modify with network startup.
- 436175 Check for running sessions when stopping service.

* Wed Feb 5 2008 Mike Christie <mchristie@redhat.com> - 6.2.0.868-0.3
- Rebase to upstream and RHEL5.
- 246960 LSB init script changes.

* Fri Oct 5 2007 Mike Christie <mchristie@redhat.com> - 6.2.0.865-0.2
- Rebase to upstream's bug fix release.
- Revert init script startup changes from 225915 which reviewers did
 not like.

* Mon Jun 20 2007 Mike Christie <mchristie@redhat.com> - 6.2.0.754-0.1
- 225915 From Adrian Reber - Fix up spec and init files for rpmlint.

* Tue Feb 6 2007 Mike Christie <mchristie@redhat.com> - 6.2.0.754-0.0
- Rebase to upstream.
- Add back --map functionality but in session mode to match RHEL5 fixes
- Break up iscsi init script into two, so iscsid can be started early for root

* Tue Nov 28 2006 Mike Christie <mchristie@redhat.com> - 6.2.0.747-0.0
- Fix several bugs in actor.c (iscsi scheduling). This should result
- in better dm-multipath intergation and fix bugs where time outs
- or requests were missed or dropped.
- Set default noop timeout correctly.

* Sat Nov 25 2006 Mike Christie <mchristie@redhat.com> - 6.2.0.742-0.0
- Don't flood targets with nop-outs.

* Fri Nov 24 2006 Mike Christie <mchristie@redhat.com> - 6.2.0.737-0.0
- Add commands missing from RHEL4/RHEL3 and document iscsid.conf.
- Fixup README.

* Mon Nov 7 2006 Mike Christie <mchristie@redhat.com> - 6.2.0.695-0.8
- Rebase to upstream open-iscsi-2.0-730.

* Tue Oct 17 2006 Mike Christie <mchristie@redhat.com> - 6.2.0.695-0.7
- Change period to colon in default name

* Thu Oct 5 2006 Mike Christie <mchristie@redhat.com> - 6.2.0.695-0.6
- BZ 209523 make sure the network is not going to get shutdown so
iscsi devices (include iscsi root and dm/md over iscsi) get syncd.
- BZ 209415 have package create iscsi var dirs

* Tue Oct 3 2006 Mike Christie <mchristie@redhat.com> - 6.2.0.695-0.5
- BZ 208864 move /etc/iscsi/nodes and send_targets to /var/lib/iscsi

* Mon Oct 1 2006 Mike Christie <mchristie@redhat.com> - 6.2.0.695-0.4
- BZ 208548 move /etc/iscsi/lock to /var/lock/iscsi/lock

* Wed Sep 27 2006 Jeremy Katz <katzj@redhat.com> - 6.2.0.695-0.3
- Add fix for initscript with pid file moved

* Tue Sep 26 2006 Mike Christie <mchristie@redhat.com> - 6.2.0.695-0.2
- BZ 208050 - change default initiator name to reflect redhat
- Move pid from /etc/iscsi to /var/run/iscsid.pid

* Fri Sep 15 2006 Mike Christie <mchristie@redhat.com> - 6.2.0.695-0.1
- Add compat with FC kernel so iscsid will pass startup checks and run.
- Fix bug when using hw iscsi and software iscsi and iscsid is restarted.
- Fix session matching bug when hw and software iscsi is both running

* Tue Sep  5 2006 Jeremy Katz <katzj@redhat.com> - 6.1.1.685-0.1
- Fix service startup
- Fix another case where cflags weren't being used

* Mon Aug 28 2006 Mike Christie <mchristie@redhat.com> - 6.1.1.685
- Rebase to upstream to bring in many bug fixes and rm db.
- iscsi uses /etc/iscsi instead of just etc now

* Fri Jul 21 2006 Jeremy Katz <katzj@redhat.com> - 6.1.1.645-1
- fix shutdown with root on iscsi

* Thu Jul 13 2006 Mike Christie <mchristie@redhat.com> - 6.1.1.645
- update to upstream 1.1.645
- Note DB and interface changed so you must update kernel, tools and DB

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 6.0.5.595-2.1.1
- rebuild

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 6.0.5.595-2.1
- rebuild

* Wed Jun 21 2006 Mike Christie <mchristi@redhat.com> - 6.0.5.595-2
- add PatM's statics.c file. This is needed for boot since 
  there is no getpwuid static available at that time.
* Tue Jun 20 2006 Jeremy Katz <katzj@redhat.com> - 6.0.5.595-1
- ensure that we respect %%{optflags}
- cleaned up initscript to make use of standard functions, return right 
  values and start by default
- build iscsistart as a static binary for use in initrds

* Tue May 30 2006 Mike Christie <mchristi@redhat.com>
- rebase package to svn rev 595 to fix several bugs
  NOTE!!!!!!!! This is not compatible with the older open-iscsi modules
  and tools. You must upgrade.

* Thu May 18 2006 Mike Christie <mchristi@redhat.com>
- update package to open-iscsi svn rev 571
  NOTE!!!!!!!! This is not compatible with the older open-iscsi modules
  and tools. You must upgrade.

* Fri Apr 7 2006 Mike Christie <mchristi@redhat.com>
- From Andy Henson <andy@zexia.co.uk>:
  Autogenerate /etc/initiatorname.iscsi during install if not already present
- Remove code to autogenerate /etc/initiatorname.iscsi from initscript
- From dan.y.roche@gmail.com:
  add touch and rm lock code
- update README
- update default iscsid.conf. "cnx" was not supported. The correct
  id was "conn".

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 5.0.5.476-0.1
- bump again for double-long bug on ppc(64)

* Mon Jan 23 2006 Mike Christie <mchristi@redhat.com>
- rebase package to bring in ppc64 unsigned long vs unsigned
  long long fix and iscsadm return value fix. Also drop rdma patch
  becuase it is now upstream.
* Wed Dec 14 2005 Mike Christie <mchristi@redhat.com>
- initial packaging

