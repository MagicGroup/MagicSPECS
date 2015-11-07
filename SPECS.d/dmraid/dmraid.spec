#
# Copyright (C)  Heinz Mauelshagen, 2004-2010 Red Hat GmbH. All rights reserved.
#
# See file LICENSE at the top of this source tree for license information.
#

Summary: dmraid (Device-mapper RAID tool and library)
Name: dmraid
Version: 1.0.0.rc16
Release: 20%{?dist}
License: GPLv2+
Group: System Environment/Base
URL: http://people.redhat.com/heinzm/sw/dmraid
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: device-mapper-devel >= 1.02.02-2
BuildRequires: device-mapper-event-devel
Requires: device-mapper >= 1.02.02-2
Requires: dmraid-events
Requires: kpartx
Requires: systemd
Requires(post): systemd >= 195-4
Obsoletes: dmraid-libs < %{version}-%{release}
Provides: dmraid-libs = %{version}-%{release}
Source0: ftp://people.redhat.com/heinzm/sw/dmraid/src/%{name}-%{version}.tar.bz2
Source1: fedora-dmraid-activation
Source2: dmraid-activation.service

Patch0: dmraid-1.0.0.rc16-test_devices.patch
Patch1: ddf1_lsi_persistent_name.patch
Patch2: pdc_raid10_failure.patch
Patch3: return_error_wo_disks.patch
Patch4: fix_sil_jbod.patch
Patch5: avoid_register.patch
Patch6: move_pattern_file_to_var.patch
Patch7: libversion.patch
Patch8: libversion-display.patch

Patch9: bz635995-data_corruption_during_activation_volume_marked_for_rebuild.patch
# Patch10: bz626417_8-faulty_message_after_unsuccessful_vol_registration.patch
Patch11: bz626417_19-enabling_registration_degraded_volume.patch
Patch12: bz626417_20-cleanup_some_compilation_warning.patch
Patch13: bz626417_21-add_option_that_postpones_any_metadata_updates.patch

%description
DMRAID supports RAID device discovery, RAID set activation, creation,
removal, rebuild and display of properties for ATARAID/DDF1 metadata on
Linux >= 2.4 using device-mapper.

%package -n dmraid-devel
Summary: Development libraries and headers for dmraid.
Group: Development/Libraries
Requires: dmraid = %{version}-%{release}, sgpio

%description -n dmraid-devel
dmraid-devel provides a library interface for RAID device discovery,
RAID set activation and display of properties for ATARAID volumes.

%package -n dmraid-events
Summary: dmevent_tool (Device-mapper event tool) and DSO
Group: System Environment/Base
Requires: dmraid = %{version}-%{release}, sgpio
Requires: device-mapper-event

%description -n dmraid-events
Provides a dmeventd DSO and the dmevent_tool to register devices with it
for device monitoring.  All active RAID sets should be manually registered
with dmevent_tool.

%package -n dmraid-events-logwatch
Summary: dmraid logwatch-based email reporting
Group: System Environment/Base
Requires: dmraid-events = %{version}-%{release}, logwatch, /etc/cron.d

%description -n dmraid-events-logwatch
Provides device failure reporting via logwatch-based email reporting.
Device failure reporting has to be activated manually by activating the 
/etc/cron.d/dmeventd-logwatch entry and by calling the dmevent_tool
(see manual page for examples) for any active RAID sets.

%prep
%setup -q -n dmraid/%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1

%patch9 -p1
# %patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1

%build
%define _libdir /%{_lib}

%configure --prefix=${RPM_BUILD_ROOT}/usr --sbindir=${RPM_BUILD_ROOT}/sbin --libdir=${RPM_BUILD_ROOT}/%{_libdir} --mandir=${RPM_BUILD_ROOT}/%{_mandir} --includedir=${RPM_BUILD_ROOT}/%{_includedir} --enable-debug --disable-libselinux --disable-libsepol --disable-static_link --enable-led --enable-intel_led
make DESTDIR=$RPM_BUILD_ROOT

%install
rm -rf $RPM_BUILD_ROOT
install -m 755 -d $RPM_BUILD_ROOT{%{_libdir},/sbin,%{_sbindir},%{_bindir},%{_libdir},%{_includedir}/dmraid/,/var/lock/dmraid,/etc/cron.d/,/etc/logwatch/conf/services/,/etc/logwatch/scripts/services/,/var/cache/logwatch/dmeventd}
make DESTDIR=$RPM_BUILD_ROOT install
ln -s dmraid $RPM_BUILD_ROOT/sbin/dmraid.static

# Provide convenience link from dmevent_tool
(cd $RPM_BUILD_ROOT/sbin ; ln -f dmevent_tool dm_dso_reg_tool)
(cd $RPM_BUILD_ROOT/%{_mandir}/man8 ; ln -f dmevent_tool.8 dm_dso_reg_tool.8 ; ln -f dmraid.8 dmraid.static.8)

install -m 644 include/dmraid/*.h $RPM_BUILD_ROOT%{_includedir}/dmraid/

# Install the libdmraid and libdmraid-events (for dmeventd) DSO
# Create version symlink to libdmraid.so.1 we link against
install -m 755 lib/libdmraid.so \
	$RPM_BUILD_ROOT%{_libdir}/libdmraid.so.%{version}
(cd $RPM_BUILD_ROOT/%{_libdir} ; ln -sf libdmraid.so.%{version} libdmraid.so ; ln -sf libdmraid.so.%{version} libdmraid.so.1)
install -m 755 lib/libdmraid-events-isw.so \
	$RPM_BUILD_ROOT%{_libdir}/libdmraid-events-isw.so.%{version}
(cd $RPM_BUILD_ROOT/%{_libdir} ; ln -sf libdmraid-events-isw.so.%{version} libdmraid-events-isw.so ; ln -sf libdmraid-events-isw.so.%{version} libdmraid-events-isw.so.1)

# Install logwatch config file and script for dmeventd
install -m 644 logwatch/dmeventd.conf $RPM_BUILD_ROOT/etc/logwatch/conf/services/dmeventd.conf
install -m 755 logwatch/dmeventd $RPM_BUILD_ROOT/etc/logwatch/scripts/services/dmeventd
install -m 644 logwatch/dmeventd_cronjob.txt $RPM_BUILD_ROOT/etc/cron.d/dmeventd-logwatch
install -m 0700 /dev/null $RPM_BUILD_ROOT/var/cache/logwatch/dmeventd/syslogpattern.txt

# Install systemd unit
install -d ${RPM_BUILD_ROOT}/%{_prefix}/lib/systemd
install -d ${RPM_BUILD_ROOT}/%{_unitdir}
install -m 755 %{SOURCE1} $RPM_BUILD_ROOT/%{_prefix}/lib/systemd/fedora-dmraid-activation
install -m 444 %{SOURCE2} $RPM_BUILD_ROOT/%{_unitdir}/dmraid-activation.service

rm -f $RPM_BUILD_ROOT/%{_libdir}/libdmraid.a

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%systemd_post dmraid-activation.service

%postun
/sbin/ldconfig

# 1. Main package
%files
%defattr(-,root,root)
%doc CHANGELOG CREDITS KNOWN_BUGS LICENSE LICENSE_GPL LICENSE_LGPL README TODO doc/dmraid_design.txt
/%{_mandir}/man8/dmraid*
/sbin/dmraid
/sbin/dmraid.static
%{_libdir}/libdmraid.so*
%{_libdir}/libdmraid-events-isw.so*
%{_prefix}/lib/systemd/fedora-dmraid-activation
%{_unitdir}/dmraid-activation.service
%ghost /var/lock/dmraid

# 2. Development package
%files -n dmraid-devel
%defattr(-,root,root)
%dir %{_includedir}/dmraid
%{_includedir}/dmraid/*

# 3. Event (device montoring) package
%files -n dmraid-events
%defattr(-,root,root)
/%{_mandir}/man8/dmevent_tool*
/%{_mandir}/man8/dm_dso_reg_tool*
/sbin/dmevent_tool
/sbin/dm_dso_reg_tool

# 4. Event package to support logwatch monitoring
%files -n dmraid-events-logwatch
%defattr(-,root,root)
%config(noreplace) /etc/logwatch/*
%config(noreplace) /etc/cron.d/dmeventd-logwatch
%dir /var/cache/logwatch/dmeventd
%ghost /var/cache/logwatch/dmeventd/syslogpattern.txt

%changelog
* Thu Oct 29 2015 Liu Di <liudidi@gmail.com> - 1.0.0.rc16-20
- 为 Magic 3.0 重建

* Wed Nov 28 2012 Peter Rajnoha <prajnoha@redhat.com> - 1.0.0.rc16-19
- Fix postun scriptlet to run ldconfig properly.

* Thu Nov 01 2012 Peter Rajnoha <prajnoha@redhat.com> - 1.0.0.rc16-18
- Add fedora-dmraid-activation script and dmraid-activation.service systemd unit.
  This replaces dmraid activation part of the former fedora-storage-init
  script that was included in the initscripts package before.
- Add 'Requires: systemd' to dmraid package.

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0.rc16-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0.rc16-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0.rc16-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Nov 24 2010  Heinz Mauelshagen <heinzm@redhat.com> - 1.0.0.rc16-14
- Updated specfile to use %ghost on /var/lock/dmraid
- Resolves: bz#656576

* Thu Nov 08 2010  Heinz Mauelshagen <heinzm@redhat.com> - 1.0.0.rc16-13
- Fix kernel panic when rebuilding and reboot occurs on IMSM RAID5 volume
- Resolves: bz#649788

* Thu Jan 21 2010  Heinz Mauelshagen <heinzm@redhat.com> - 1.0.0.rc16-12
- Create symlink from full versioned libdmraid dso file to libdmraid.so.1
  (ie. soname we use for linking)
- Resolves: bz#557276

* Wed Jan 20 2010  Heinz Mauelshagen <heinzm@redhat.com> - 1.0.0.rc16-11
- return full internal library name as a combination of library
  major, minor, subminor and suffix numbers on calls to libdmraid_version()
- Related: bz#556863

* Tue Jan 19 2010  Heinz Mauelshagen <heinzm@redhat.com> - 1.0.0.rc16-10
- change libdmraid version to 1
- Resolves: bz#556863

* Tue Jan 12 2010  Heinz Mauelshagen <heinzm@redhat.com> - 1.0.0.rc16-9
- bz554754: switch to using /var/cache/logwatch/dmeventd/syslogpattern.txt;
  explicitly claim logwatch files in dmraid-events-logwatch

* Thu Jan 7 2010  Heinz Mauelshagen <heinzm@redhat.com> - 1.0.0.rc16-8
- scratch build

* Fri Dec 1 2009  Heinz Mauelshagen <heinzm@redhat.com> - 1.0.0.rc16-7
- bz542898: fix Silicon Image JBOD support

* Fri Oct 16 2009  Heinz Mauelshagen <heinzm@redhat.com> - 1.0.0.rc16-6
- Fix manual path in specfile

* Fri Oct 16 2009  Heinz Mauelshagen <heinzm@redhat.com> - 1.0.0.rc16-5
- bz526157: fix manual pages for dmraid.static and dm_dso_reg_tool

* Thu Oct 15 2009  Heinz Mauelshagen <heinzm@redhat.com> - 1.0.0.rc16-4
- bz505562: ddf1 metadata format handler LSI persistent name fix
- bz524168: fix pdc metadata format handler to report the correct number
  of devices in a RAID10 subset
- bz528097: move libraries to /lib* in order to avoid catch22
  with unmountable u/usr

* Mon Sep 21 2009 Hans de Goede <hdegoede@redhat.com> - 1.0.0.rc16-3
- Add Obsoletes for dmraid-libs packages (merged into the main pkg, #524261)
- Make -devel Require the main package now the dmraid-libs package is gone

* Wed Sep 16 2009 Heinz Mauelshagen <heinzm@redhat.com> - 1.0.0.rc16
- Update to version 1.0.0.rc16

* Fri Apr 17 2009 Hans de Goede <hdegoede@redhat.com> - 1.0.0.rc15-7
- Fix activation of isw raid sets when the disks have serialnumber longer
  then 16 characters (#490121)

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0.rc15-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 13 2009 Hans de Goede <hdegoede@redhat.com> - 1.0.0.rc15-5
- Make --rm_partitions work with older kernels which return EINVAL when trying
  to remove a partition with a number > 16
- Document --rm_partitions in the man page

* Thu Feb 12 2009 Hans de Goede <hdegoede@redhat.com> - 1.0.0.rc15-4
- Add patch adding --rm_partitions cmdline option and functionality (#484845)

* Thu Feb  5 2009 Hans de Goede <hdegoede@redhat.com> - 1.0.0.rc15-3
- Fix mismatch between BIOS and dmraid's view of ISW raid 10 sets

* Tue Nov 18 2008 Bill Nottingham <notting@redhat.com> - 1.0.0.rc15-2
- Re-add upstream whitespace removal patch (#468649, #470634)

* Thu Sep 25 2008 Heinz Mauelshagen <heinzm@redhat.com> - 1.0.0.rc15-1
- Update to version 1.0.0.rc15

* Thu Jul 03 2008 Alasdair Kergon <agk@redhat.com> - 1.0.0.rc14-8
- Move library into libs subpackage.
- Fix summary and licence tags.
- Replace static build with symlink.

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.0.rc14-7
- Autorebuild for GCC 4.3

* Wed Nov 21 2007 Ian Kent <ikent@redhat.com> - 1.0.0.rc14-6
- Bug 379911: dmraid needs to generate UUIDs for lib device-mapper
  - add "DMRAID-" prefix to dmraid UUID string.

* Wed Nov 14 2007 Ian Kent <ikent@redhat.com> - 1.0.0.rc14-5
- Bug 379911: dmraid needs to generate UUIDs for lib device-mapper
- Bug 379951: dmraid needs to activate device-mapper mirror resynchronization error handling

* Mon Oct 22 2007 Ian Kent <ikent@redhat.com> - 1.0.0.rc14-4
- Fix SEGV on "dmraid -r -E" (bz 236891).

* Wed Apr 18 2007 Peter Jones <pjones@redhat.com> - 1.0.0.rc14-3
- Fix jmicron name parsing (#219058)

* Mon Feb 05 2007 Alasdair Kergon <agk@redhat.com> - 1.0.0.rc14-2
- Add build dependency on new device-mapper-devel package.
- Add dependency on device-mapper.
- Add post and postun ldconfig.
- Update BuildRoot and Summary.

* Wed Nov 08 2006 Heinz Mauelshagen <heinzm@redhat.com> - 1.0.0.rc14-1
- asr.c: fixed Adaptec HostRAID DDF1 metadata discovery (bz#211016)
- ddf1_crc.c: added crc() routine to avoid linking to zlib alltogether,
              because Ubuntu had problems with this
- dropped zlib build requirement

* Thu Oct 26 2006 Heinz Mauelshagen <heinzm@redhat.com> - 1.0.0.rc14-bz211016-1
- ddf1.c: get_size() fixed (bz#211016)
- ddf1_lib.c: ddf1_cr_off_maxpds_helper() fixed (bz#211016)

* Wed Oct 11 2006 Heinz Mauelshagen <heinzm@redhat.com> - 1.0.0.rc13-1
- metadata.c: fixed bug returning wrang unified RAID type (bz#210085)
- pdc.c: fixed magic number check

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 1.0.0.rc12-7
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Fri Sep 22 2006 Heinz Mauelshagen <heinzm@redhat.com> - 1.0.0.rc12-1
- sil.c: quorate() OBO fix
- activate.c: handler() OBO fix
- added SNIA DDF1 support
- added reload functionality to devmapper.c
- added log_zero_sectors() to various metadata format handlers
- sil.[ch]: added JBOD support

* Fri Sep  1 2006 Peter Jones <pjones@redhat.com> - 1.0.0.rc11-4
- Require kpartx, so initscripts doesn't have to if you're not using dmraid

* Thu Aug 17 2006 Jesse Keating <jkeating@redhat.com> - 1.0.0.rc11-3
- Change Release to follow guidelines, and add dist tag.

* Thu Aug 17 2006 Peter Jones <pjones@redhat.com> - 1.0.0.rc11-FC6.3
- No more excludearch for s390/s390x

* Fri Jul 28 2006 Peter Jones <pjones@redhat.com> - 1.0.0.rc11-FC6.2
- Fix bounds checking on hpt37x error log
- Only build the .so, not the .a
- Fix asc.c duplication in makefile rule

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.0.0.rc11-FC6.1.1
- rebuild

* Fri Jul  7 2006 Heinz Mauelshagen <heinzm@redhat.com> - 1.0.0.rc11-FC6.1
- rebuilt for FC6 with dos partition discovery fix (#197573)

* Tue May 16 2006 Heinz Mauelshagen <heinzm@redhat.com> - 1.0.0.rc11-FC6
- rebuilt for FC6 with better tag

* Tue May 16 2006 Heinz Mauelshagen <heinzm@redhat.com> - 1.0.0.rc11-FC5_7.2
- rebuilt for FC5

* Tue May 16 2006 Heinz Mauelshagen <heinzm@redhat.com> - 1.0.0.rc11-FC5_7.1
- jm.c: checksum() calculation
- misc.c: support "%d" in p_fmt and fix segfault with wrong format identifier
- nv.c: size fix in setup_rd()
- activate.c:
        o striped devices could end on non-chunk boundaries
        o calc_region_size() calculated too small sizes causing large
          dirty logs in memory
- isw.c: set raid5 type to left asymmetric
- toollib.c: fixed 'No RAID...' message
- support selection of RAID5 allocation algorithm in metadata format handlers
- build

* Mon Mar 27 2006 Milan Broz <mbroz@redhat.com> - 1.0.0.rc10-FC5_6.2
- fixed /var/lock/dmraid in specfile (#168195)

* Fri Feb 17 2006 Heinz Mauelshagen <heinzm@redhat.com> - 1.0.0.rc10-FC5_6
- add doc/dmraid_design.txt to %doc (#181885)
- add --enable-libselinux --enable-libsepol to configure
- rebuilt

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.0.0.rc9-FC5_5.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.0.0.rc9-FC5_5.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Sun Jan 22 2006 Peter Jones <pjones@redhat.com> 1.0.0.rc9-FC5_5
- Add selinux build deps
- Don't set owner during make install

* Fri Dec  9 2005 Jesse Keating <jkeating@redhat.com> 1.0.0.rc9-FC5_4.1
- rebuilt

* Sun Dec  3 2005 Peter Jones <pjones@redhat.com> 1.0.0.rc9-FC5_4
- rebuild for device-mapper-1.02.02-2

* Fri Dec  2 2005 Peter Jones <pjones@redhat.com> 1.0.0.rc9-FC5_3
- rebuild for device-mapper-1.02.02-1

* Thu Nov 10 2005 Peter Jones <pjones@redhat.com> 1.0.0.rc9-FC5_2
- update to 1.0.0.rc9
- make "make install" do the right thing with the DSO
- eliminate duplicate definitions in the headers
- export more symbols in the DSO
- add api calls to retrieve dm tables
- fix DESTDIR for 'make install' 
- add api calls to identify degraded devices
- remove several arch excludes

* Sat Oct 15 2005 Florian La Roche <laroche@redhat.com>
- add -lselinux -lsepol for new device-mapper deps

* Fri May 20 2005 Heinz Mauelshagen <heinzm@redhat.com> 1.0.0.rc8-FC4_2
- specfile change to build static and dynamic binray into one package
- rebuilt

* Thu May 19 2005 Heinz Mauelshagen <heinzm@redhat.com> 1.0.0.rc8-FC4_1
- nv.c: fixed stripe size
- sil.c: avoid incarnation_no in name creation, because the Windows
         driver changes it every time
- added --ignorelocking option to avoid taking out locks in early boot
  where no read/write access to /var is given

* Wed Mar 16 2005 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 15 2005 Heinz Mauelshagen <heinzm@redhat.com> 1.0.0.rc6.1-4_FC4
- VIA metadata format handler
- added RAID10 to lsi metadata format handler
- "dmraid -rD": file device size into {devicename}_{formatname}.size
- "dmraid -tay": pretty print multi-line tables ala "dmsetup table"
- "dmraid -l": display supported RAID levels + manual update
- _sil_read() used LOG_NOTICE rather than LOG_INFO in order to
  avoid messages about valid metadata areas being displayed
  during "dmraid -vay".
- isw, sil filed metadata offset on "-r -D" in sectors rather than in bytes.
- isw needed dev_sort() to sort RAID devices in sets correctly.
- pdc metadata format handler name creation. Lead to
  wrong RAID set grouping logic in some configurations.
- pdc RAID1 size calculation fixed (rc6.1)
- dos.c: partition table code fixes by Paul Moore
- _free_dev_pointers(): fixed potential OOB error
- hpt37x_check: deal with raid_disks = 1 in mirror sets
- pdc_check: status & 0x80 doesn't always show a failed device;
  removed that check for now. Status definitions needed.
- sil addition of RAID sets to global list of sets
- sil spare device memory leak
- group_set(): removal of RAID set in case of error
- hpt37x: handle total_secs > device size
- allow -p with -f
- enhanced error message by checking target type against list of
  registered target types

* Fri Jan 21 2005 Alasdair Kergon <agk@redhat.com> 1.0.0.rc5f-2
- Rebuild to pick up new libdevmapper.

* Fri Nov 26 2004 Heinz Mauelshagen <heinzm@redhat.com> 1.0.0.rc5f
- specfile cleanup

* Tue Aug 20 2004 Heinz Mauelshagen <heinzm@redhat.com> 1.0.0-rc4-pre1
- Removed make flag after fixing make.tmpl.in

* Tue Aug 18 2004 Heinz Mauelshagen <heinzm@redhat.com> 1.0.0-rc3
- Added make flag to prevent make 3.80 from looping infinitely

* Thu Jun 17 2004 Heinz Mauelshagen <heinzm@redhat.com> 1.0.0-pre1
- Created
