%define device_mapper_version 1.02.86

%define enable_cache 1
%define enable_cluster 1
%define enable_cmirror 1
%define enable_lvmetad 1
%define enable_python 1
%define enable_thin 1

%define systemd_version 189-3
%define dracut_version 002-18
%define util_linux_version 2.24
%define bash_version 4.0
%define corosync_version 1.99.9-1
%define resource_agents_version 3.9.5-12
%define dlm_version 3.99.1-1
%define libselinux_version 1.30.19-4
%define persistent_data_version 0.3.2-1

%if 0%{?rhel}
  %ifnarch i686 x86_64
    %define enable_cluster 0
    %define enable_cmirror 0
  %endif
%endif

%if %{enable_cluster}
  %define configure_cluster --with-cluster=internal --with-clvmd=corosync
  %if %{enable_cmirror}
    %define configure_cmirror --enable-cmirrord
  %endif
%else
    %define configure_cluster --with-cluster=internal --with-clvmd=none
%endif


# Do not reset Release to 1 unless both lvm2 and device-mapper 
# versions are increased together.

Summary: Userland logical volume management tools 
Name: lvm2
Version: 2.02.107
Release: 4%{?dist}
License: GPLv2
Group: System Environment/Base
URL: http://sources.redhat.com/lvm2
Source0: ftp://sources.redhat.com/pub/lvm2/releases/LVM2.%{version}.tgz
Patch0: lvm2-set-default-preferred_names.patch
Patch1: lvm2-enable-lvmetad-by-default.patch
Patch2: lvm2-remove-mpath-device-handling-from-udev-rules.patch

BuildRequires: libblkid-devel >= %{util_linux_version}
BuildRequires: ncurses-devel
BuildRequires: readline-devel
%if %{enable_cluster}
BuildRequires: corosynclib-devel >= %{corosync_version}
BuildRequires: dlm-devel >= %{dlm_version}
%endif
BuildRequires: module-init-tools
BuildRequires: pkgconfig
BuildRequires: systemd-devel
BuildRequires: systemd-units
%if %{enable_python}
BuildRequires: python2-devel
BuildRequires: python-setuptools
%endif
Requires: %{name}-libs = %{version}-%{release}
Requires: bash >= %{bash_version}
Requires(post): systemd-units >= %{systemd_version}, systemd-sysv
Requires(preun): systemd-units >= %{systemd_version}
Requires(postun): systemd-units >= %{systemd_version}
Requires: module-init-tools
%if %{enable_thin}
Requires: device-mapper-persistent-data >= %{persistent_data_version}
%endif

%description
LVM2 includes all of the support for handling read/write operations on
physical volumes (hard disks, RAID-Systems, magneto optical, etc.,
multiple devices (MD), see mdadd(8) or even loop devices, see
losetup(8)), creating volume groups (kind of virtual disks) from one
or more physical volumes and creating one or more logical volumes
(kind of logical partitions) in volume groups.

%prep
%setup -q -n LVM2.%{version}
%patch0 -p1 -b .preferred_names
%patch1 -p1 -b .enable_lvmetad
%patch2 -p1 -b .udev_no_mpath

%build
%define _default_pid_dir /run
%define _default_dm_run_dir /run
%define _default_run_dir /run/lvm
%define _default_locking_dir /run/lock/lvm

%define _udevdir %{_prefix}/lib/udev/rules.d
%define _tmpfilesdir %{_prefix}/lib/tmpfiles.d

%define configure_udev --with-udevdir=%{_udevdir} --enable-udev_sync

%if %{enable_cache}
%define configure_cache --with-cache=internal
%endif

%if %{enable_thin}
%define configure_thin --with-thin=internal --with-thin-check=%{_sbindir}/thin_check --with-thin-dump=%{_sbindir}/thin_dump --with-thin-repair=%{_sbindir}/thin_repair
%endif

%if %{enable_lvmetad}
%define configure_lvmetad --enable-lvmetad
%endif

%if %{enable_python}
%define configure_python --enable-python-bindings
%endif

%configure --with-default-dm-run-dir=%{_default_dm_run_dir} --with-default-run-dir=%{_default_run_dir} --with-default-pid-dir=%{_default_pid_dir} --with-default-locking-dir=%{_default_locking_dir} --with-usrlibdir=%{_libdir} --enable-lvm1_fallback --enable-fsadm --with-pool=internal --enable-write_install --with-user= --with-group= --with-device-uid=0 --with-device-gid=6 --with-device-mode=0660 --enable-pkgconfig --enable-applib --enable-cmdlib --enable-dmeventd --enable-blkid_wiping %{?configure_python} %{?configure_cluster} %{?configure_cmirror} %{?configure_udev} %{?configure_thin} %{?configure_lvmetad} %{?configure_cache}

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
make install_system_dirs DESTDIR=$RPM_BUILD_ROOT
make install_systemd_units DESTDIR=$RPM_BUILD_ROOT
make install_systemd_generators DESTDIR=$RPM_BUILD_ROOT
make install_tmpfiles_configuration DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%systemd_post blk-availability.service lvm2-monitor.service
%if %{enable_lvmetad}
%systemd_post lvm2-lvmetad.socket
%endif

%preun
%systemd_preun blk-availability.service lvm2-monitor.service
%if %{enable_lvmetad}
%systemd_preun lvm2-lvmetad.service lvm2-lvmetad.socket
%endif

%postun
%systemd_postun lvm2-monitor.service
%if %{enable_lvmetad}
%systemd_postun_with_restart lvm2-lvmetad.service
%endif

%triggerun -- %{name} < 2.02.86-2
%{_bindir}/systemd-sysv-convert --save lvm2-monitor >/dev/null 2>&1 || :
/bin/systemctl --no-reload enable lvm2-monitor.service > /dev/null 2>&1 || :
/sbin/chkconfig --del lvm2-monitor > /dev/null 2>&1 || :
/bin/systemctl try-restart lvm2-monitor.service > /dev/null 2>&1 || :

%files
%defattr(-,root,root,-)
%doc COPYING COPYING.LIB README VERSION WHATS_NEW
%doc doc/lvm_fault_handling.txt

# Main binaries
%defattr(555,root,root,-)
%{_sbindir}/blkdeactivate
%{_sbindir}/fsadm
%{_sbindir}/lvm
%{_sbindir}/lvmconf
%{_sbindir}/lvmdump
%if %{enable_lvmetad}
%{_sbindir}/lvmetad
%endif
%{_sbindir}/vgimportclone

# Other files
%defattr(444,root,root,-)
%{_sbindir}/lvchange
%{_sbindir}/lvconvert
%{_sbindir}/lvcreate
%{_sbindir}/lvdisplay
%{_sbindir}/lvextend
%{_sbindir}/lvmchange
%{_sbindir}/lvmdiskscan
%{_sbindir}/lvmsadc
%{_sbindir}/lvmsar
%{_sbindir}/lvreduce
%{_sbindir}/lvremove
%{_sbindir}/lvrename
%{_sbindir}/lvresize
%{_sbindir}/lvs
%{_sbindir}/lvscan
%{_sbindir}/pvchange
%{_sbindir}/pvck
%{_sbindir}/pvcreate
%{_sbindir}/pvdisplay
%{_sbindir}/pvmove
%{_sbindir}/pvremove
%{_sbindir}/pvresize
%{_sbindir}/pvs
%{_sbindir}/pvscan
%{_sbindir}/vgcfgbackup
%{_sbindir}/vgcfgrestore
%{_sbindir}/vgchange
%{_sbindir}/vgck
%{_sbindir}/vgconvert
%{_sbindir}/vgcreate
%{_sbindir}/vgdisplay
%{_sbindir}/vgexport
%{_sbindir}/vgextend
%{_sbindir}/vgimport
%{_sbindir}/vgmerge
%{_sbindir}/vgmknodes
%{_sbindir}/vgreduce
%{_sbindir}/vgremove
%{_sbindir}/vgrename
%{_sbindir}/vgs
%{_sbindir}/vgscan
%{_sbindir}/vgsplit
%{_mandir}/man5/lvm.conf.5.gz
%{_mandir}/man7/lvmcache.7.gz
%{_mandir}/man7/lvmthin.7.gz
%{_mandir}/man8/blkdeactivate.8.gz
%{_mandir}/man8/fsadm.8.gz
%{_mandir}/man8/lvchange.8.gz
%{_mandir}/man8/lvconvert.8.gz
%{_mandir}/man8/lvcreate.8.gz
%{_mandir}/man8/lvdisplay.8.gz
%{_mandir}/man8/lvextend.8.gz
%{_mandir}/man8/lvm.8.gz
%{_mandir}/man8/lvm2-activation-generator.8.gz
%{_mandir}/man8/lvm-dumpconfig.8.gz
%{_mandir}/man8/lvmchange.8.gz
%{_mandir}/man8/lvmconf.8.gz
%{_mandir}/man8/lvmdiskscan.8.gz
%{_mandir}/man8/lvmdump.8.gz
%{_mandir}/man8/lvmsadc.8.gz
%{_mandir}/man8/lvmsar.8.gz
%{_mandir}/man8/lvreduce.8.gz
%{_mandir}/man8/lvremove.8.gz
%{_mandir}/man8/lvrename.8.gz
%{_mandir}/man8/lvresize.8.gz
%{_mandir}/man8/lvs.8.gz
%{_mandir}/man8/lvscan.8.gz
%{_mandir}/man8/pvchange.8.gz
%{_mandir}/man8/pvck.8.gz
%{_mandir}/man8/pvcreate.8.gz
%{_mandir}/man8/pvdisplay.8.gz
%{_mandir}/man8/pvmove.8.gz
%{_mandir}/man8/pvremove.8.gz
%{_mandir}/man8/pvresize.8.gz
%{_mandir}/man8/pvs.8.gz
%{_mandir}/man8/pvscan.8.gz
%{_mandir}/man8/vgcfgbackup.8.gz
%{_mandir}/man8/vgcfgrestore.8.gz
%{_mandir}/man8/vgchange.8.gz
%{_mandir}/man8/vgck.8.gz
%{_mandir}/man8/vgconvert.8.gz
%{_mandir}/man8/vgcreate.8.gz
%{_mandir}/man8/vgdisplay.8.gz
%{_mandir}/man8/vgexport.8.gz
%{_mandir}/man8/vgextend.8.gz
%{_mandir}/man8/vgimport.8.gz
%{_mandir}/man8/vgimportclone.8.gz
%{_mandir}/man8/vgmerge.8.gz
%{_mandir}/man8/vgmknodes.8.gz
%{_mandir}/man8/vgreduce.8.gz
%{_mandir}/man8/vgremove.8.gz
%{_mandir}/man8/vgrename.8.gz
%{_mandir}/man8/vgs.8.gz
%{_mandir}/man8/vgscan.8.gz
%{_mandir}/man8/vgsplit.8.gz
%{_udevdir}/11-dm-lvm.rules
%if %{enable_lvmetad}
%{_mandir}/man8/lvmetad.8.gz
%{_udevdir}/69-dm-lvm-metad.rules
%endif
%dir %{_sysconfdir}/lvm
%ghost %{_sysconfdir}/lvm/cache/.cache
%attr(644, -, -) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lvm/lvm.conf
%dir %{_sysconfdir}/lvm/profile
%{_sysconfdir}/lvm/profile/command_profile_template.profile
%{_sysconfdir}/lvm/profile/metadata_profile_template.profile
%{_sysconfdir}/lvm/profile/thin-generic.profile
%{_sysconfdir}/lvm/profile/thin-performance.profile
%dir %{_sysconfdir}/lvm/backup
%dir %{_sysconfdir}/lvm/cache
%dir %{_sysconfdir}/lvm/archive
%ghost %dir %{_default_locking_dir}
%ghost %dir %{_default_run_dir}
%{_tmpfilesdir}/%{name}.conf
%{_unitdir}/blk-availability.service
%{_unitdir}/lvm2-monitor.service
%attr(555, -, -) %{_prefix}/lib/systemd/system-generators/lvm2-activation-generator
%if %{enable_lvmetad}
%{_unitdir}/lvm2-lvmetad.socket
%{_unitdir}/lvm2-lvmetad.service
%{_unitdir}/lvm2-pvscan@.service
%endif

##############################################################################
# Library and Development subpackages
##############################################################################
%package devel
Summary: Development libraries and headers
Group: Development/Libraries
License: LGPLv2
Requires: %{name} = %{version}-%{release}
Requires: device-mapper-devel = %{device_mapper_version}-%{release}
Requires: device-mapper-event-devel = %{device_mapper_version}-%{release}
Requires: pkgconfig

%description devel
This package contains files needed to develop applications that use
the lvm2 libraries.

%files devel
%defattr(444,root,root,-)
%{_libdir}/liblvm2app.so
%{_libdir}/liblvm2cmd.so
%{_libdir}/libdevmapper-event-lvm2.so
%{_includedir}/lvm2app.h
%{_includedir}/lvm2cmd.h
%{_libdir}/pkgconfig/lvm2app.pc

%package libs
Summary: Shared libraries for lvm2
License: LGPLv2
Group: System Environment/Libraries
Requires: device-mapper-event = %{device_mapper_version}-%{release}

%description libs
This package contains shared lvm2 libraries for applications.

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files libs
%defattr(555,root,root,-)
%{_libdir}/liblvm2app.so.*
%{_libdir}/liblvm2cmd.so.*
%{_libdir}/libdevmapper-event-lvm2.so.*
%dir %{_libdir}/device-mapper
%{_libdir}/device-mapper/libdevmapper-event-lvm2mirror.so
%{_libdir}/device-mapper/libdevmapper-event-lvm2snapshot.so
%{_libdir}/device-mapper/libdevmapper-event-lvm2raid.so
%{_libdir}/libdevmapper-event-lvm2mirror.so
%{_libdir}/libdevmapper-event-lvm2snapshot.so
%{_libdir}/libdevmapper-event-lvm2raid.so

%if %{enable_thin}
%{_libdir}/libdevmapper-event-lvm2thin.so
%{_libdir}/device-mapper/libdevmapper-event-lvm2thin.so
%endif

%if %{enable_python}

%package python-libs
Summary: Python module to access LVM
License: LGPLv2
Group: Development/Libraries
Provides: python-lvm = %{version}-%{release}
Obsoletes: python-lvm < 2.02.98-2
Requires: %{name}-libs = %{version}-%{release}

%description python-libs
Python module to allow the creation and use of LVM
logical volumes, physical volumes, and volume groups.

%files python-libs
%{python_sitearch}/*

%endif

##############################################################################
# Cluster subpackage
# The 'clvm' OCF script to manage clvmd instance is part of resource-agents.
##############################################################################
%if %{enable_cluster}

%package cluster
Summary: Cluster extensions for userland logical volume management tools
License: GPLv2
Group: System Environment/Base
Requires: lvm2 = %{version}-%{release}
Requires(preun): device-mapper >= %{device_mapper_version}
Requires(preun): lvm2 >= 2.02
Requires: corosync >= %{corosync_version}
Requires: dlm >= %{dlm_version}
Requires: resource-agents >= %{resource_agents_version}

%description cluster

Extensions to LVM2 to support clusters.

%post cluster
if [ -e %{_default_pid_dir}/clvmd.pid ]; then
	/usr/sbin/clvmd -S || echo "Failed to restart clvmd daemon. Please, try manual restart."
fi

%preun cluster
if [ "$1" = "0" ]; then
	/sbin/lvmconf --disable-cluster
fi

%files cluster
%defattr(555,root,root,-)
%{_sbindir}/clvmd
%attr(444, -, -) %{_mandir}/man8/clvmd.8.gz

##############################################################################
# Cluster-standalone subpackage
##############################################################################
%package cluster-standalone
Summary: Additional files to support clustered LVM2 in standalone mode
License: GPLv2
Group: System Environment/Base
Requires: lvm2-cluster = %{version}-%{release}

%description cluster-standalone

Additional files needed to run clustered LVM2 daemon and clustered volume
activation in standalone mode as services without cluster resource manager
involvement (e.g. pacemaker).

%post cluster-standalone
%systemd_post lvm2-clvmd.service lvm2-cluster-activation.service

%preun cluster-standalone
%systemd_preun lvm2-clvmd.service lvm2-cluster-activation.service

%postun cluster-standalone
%systemd_postun lvm2-clvmd.service lvm2-cluster-activation.service

%files cluster-standalone
%defattr(555,root,root,-)
%{_prefix}/lib/systemd/lvm2-cluster-activation
%defattr(444,root,root,-)
%{_unitdir}/lvm2-clvmd.service
%{_unitdir}/lvm2-cluster-activation.service

%endif

###############################################################################
# Cluster mirror subpackage
# The 'clvm' OCF script to manage cmirrord instance is part of resource-agents.
###############################################################################
%if %{enable_cluster}
%if %{enable_cmirror}

%package -n cmirror
Summary: Daemon for device-mapper-based clustered mirrors
Group: System Environment/Base
Requires: corosync >= %{corosync_version}
Requires: device-mapper = %{device_mapper_version}-%{release}
Requires: resource-agents >= %{resource_agents_version}

%description -n cmirror
Daemon providing device-mapper-based mirrors in a shared-storage cluster.

%files -n cmirror
%defattr(555,root,root,-)
%{_sbindir}/cmirrord
%attr(444, -, -) %{_mandir}/man8/cmirrord.8.gz

##############################################################################
# Cmirror-standalone subpackage
##############################################################################
%package -n cmirror-standalone
Summary: Additional files to support device-mapper-based clustered mirrors in standalone mode
License: GPLv2
Group: System Environment/Base
Requires: cmirror >= %{epoch}:%{version}-%{release}

%description -n cmirror-standalone

Additional files needed to run daemon for device-mapper-based clustered
mirrors in standalone mode as a service without cluster resource manager
involvement (e.g. pacemaker).

%post -n cmirror-standalone
%systemd_post lvm2-cmirrord.service

%preun -n cmirror-standalone
%systemd_preun lvm2-cmirrord.service

%postun -n cmirror-standalone
%systemd_postun lvm2-cmirrord.service

%files -n cmirror-standalone
%defattr(444,root,root,-)
%{_unitdir}/lvm2-cmirrord.service

%endif
%endif

##############################################################################
# Device-mapper subpackages
##############################################################################
%package -n device-mapper
Summary: Device mapper utility
Version: %{device_mapper_version}
License: GPLv2
Group: System Environment/Base
URL: http://sources.redhat.com/dm
Requires: device-mapper-libs = %{device_mapper_version}-%{release}
Requires: util-linux >= %{util_linux_version}
Requires: systemd >= %{systemd_version}
# We need dracut to install required udev rules if udev_sync
# feature is turned on so we don't lose required notifications.
Conflicts: dracut < %{dracut_version}

%description -n device-mapper
This package contains the supporting userspace utility, dmsetup,
for the kernel device-mapper.

%files -n device-mapper
%defattr(-,root,root,-)
%doc COPYING COPYING.LIB WHATS_NEW_DM VERSION_DM README
%doc udev/12-dm-permissions.rules
%defattr(444,root,root,-)
%attr(555, -, -) %{_sbindir}/dmsetup
%{_mandir}/man8/dmsetup.8.gz
%{_udevdir}/10-dm.rules
%{_udevdir}/13-dm-disk.rules
%{_udevdir}/95-dm-notify.rules

%package -n device-mapper-devel
Summary: Development libraries and headers for device-mapper
Version: %{device_mapper_version}
License: LGPLv2
Group: Development/Libraries
Requires: device-mapper = %{device_mapper_version}-%{release}
Requires: pkgconfig

%description -n device-mapper-devel
This package contains files needed to develop applications that use
the device-mapper libraries.

%files -n device-mapper-devel
%defattr(444,root,root,-)
%{_libdir}/libdevmapper.so
%{_includedir}/libdevmapper.h
%{_libdir}/pkgconfig/devmapper.pc

%package -n device-mapper-libs
Summary: Device-mapper shared library
Version: %{device_mapper_version}
License: LGPLv2
Group: System Environment/Libraries
Requires: device-mapper = %{device_mapper_version}-%{release}

%description -n device-mapper-libs
This package contains the device-mapper shared library, libdevmapper.

%post -n device-mapper-libs -p /sbin/ldconfig

%postun -n device-mapper-libs -p /sbin/ldconfig

%files -n device-mapper-libs
%defattr(555,root,root,-)
%{_libdir}/libdevmapper.so.*

%package -n device-mapper-event
Summary: Device-mapper event daemon
Group: System Environment/Base
Version: %{device_mapper_version}
Requires: device-mapper = %{device_mapper_version}-%{release}
Requires: device-mapper-event-libs = %{device_mapper_version}-%{release}
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

%description -n device-mapper-event
This package contains the dmeventd daemon for monitoring the state
of device-mapper devices.

%post -n device-mapper-event
%systemd_post dm-event.socket
if [ -e %{_default_pid_dir}/dmeventd.pid ]; then
	%{_sbindir}/dmeventd -R || echo "Failed to restart dmeventd daemon. Please, try manual restart."
fi

%preun -n device-mapper-event
%systemd_preun dm-event.service dm-event.socket

%files -n device-mapper-event
%defattr(444,root,root,-)
%attr(555, -, -) %{_sbindir}/dmeventd
%{_mandir}/man8/dmeventd.8.gz
%{_unitdir}/dm-event.socket
%{_unitdir}/dm-event.service

%package -n device-mapper-event-libs
Summary: Device-mapper event daemon shared library
Version: %{device_mapper_version}
License: LGPLv2
Group: System Environment/Libraries

%description -n device-mapper-event-libs
This package contains the device-mapper event daemon shared library,
libdevmapper-event.

%post -n device-mapper-event-libs -p /sbin/ldconfig

%postun -n device-mapper-event-libs -p /sbin/ldconfig

%files -n device-mapper-event-libs
%defattr(555,root,root,-)
%{_libdir}/libdevmapper-event.so.*

%package -n device-mapper-event-devel
Summary: Development libraries and headers for the device-mapper event daemon
Version: %{device_mapper_version}
License: LGPLv2
Group: Development/Libraries
Requires: device-mapper-event = %{device_mapper_version}-%{release}
Requires: pkgconfig

%description -n device-mapper-event-devel
This package contains files needed to develop applications that use
the device-mapper event library.

%files -n device-mapper-event-devel
%defattr(444,root,root,-)
%{_libdir}/libdevmapper-event.so
%{_includedir}/libdevmapper-event.h
%{_libdir}/pkgconfig/devmapper-event.pc

%changelog
* Tue Nov 10 2015 Liu Di <liudidi@gmail.com> - 2.02.107-4
- 为 Magic 3.0 重建

* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 2.02.107-3
- 为 Magic 3.0 重建

* Fri Jul 04 2014 Liu Di <liudidi@gmail.com> - 2.02.107-2
- 为 Magic 3.0 重建

* Tue Jun 24 2014 Peter Rajnoha <prajnoha@redhat.com> - 2.02.107-1
- Add cmirror-standalone subpackage containing new lvm2-cmirrord.service
  systemd unit for standalone cmirrord daemon management without cluster
  resource manager involvement.
- Add lvm2-cluster-standalone subpackage containing new lvm2-clvmd.service
  and lvm2-cluster-activation.service systemd unit for standalone clvmd
  daemon management without cluster resource manager involvement.
- Add Requires: resource-agents for lvm2-cluster and cmirror subpackages.
  The resource-agents package provides "clvm" cluster resource to manage
  clvmd and cmirrord instances. This replaces obsolete clvmd and cmirrord
  initscripts.
- Introduce LCK_ACTIVATION to avoid concurrent activation of basic LV types.
- Fix open_count test for lvchange --refresh or mirrors and raids.
- Update pvs,vgs,lvs and lvm man page for selection support.
- Add -S/--select to lvm devtypes for report selection.
- Add -S/--select to pvs,vgs,lvs and {pv,vg,lv}display -C for report selection.
- Use dm_report_init_with_selection now, implicit "selected" field appears.
- Make use of libdm's DM_REPORT_FIELD_TYPE{SIZE,PERCENT,STRING_LIST} for fields.
- Support all-or-nothing pvmove --atomic.
- Automatically add snapshot metadata size for -l %ORIGIN calculation.
- When converting RAID origin to cache LV, properly rename sub-LVs.
- Use RemoveOnStop for lvm2-lvmetad.socket systemd unit.
- Add thin-generic configuration profile for generic thin settings.
- Fix crash when reporting empty labels on pvs.
- Use retry_deactivation also when cleaning orphan devices.
- Wait for client threads when shutting down lvmetad.
- Remove PV from cache on pvremove.
- Avoid repeatedly reporting of failure to connect to lvmetad.
- Introduce MDA_FAILED to permit metadata updates even if some mdas are missing.
- Prompt when setting the VG cluster attr if the cluster is not setup.
- Allow --yes to skip prompt in vgextend (worked only with -f).
- Don't use name mangling for LVM - it never uses dm names with wrong char set.
- Remove default.profile and add {command,metadata}_profile_template.profile.
- Use proper umask for systemd units generated by lvm2-activation-generator.
- Check for failing mirror_remove_missing() function.
- Prompt before converting volumes to thin pool and thin pool metadata.
- Add dumpconfig --type profilable-{metadata,command} to select profile type.
- Exit immediately with error if command profile is found invalid.
- Separate --profile cmd line arg into --commandprofile and --metadataprofile.
- Strictly separate command profiles and per-VG/LV profiles referenced in mda.
- Fix dumpconfig --type diff when run as second and later cmd in lvm shell.
- Fix wrong profile reuse from previous run if another cmd is run in lvm shell.
- Move cache description from lvm(8) to new lvmcache(7) man page.
- Display skipped prompt in silent mode.
- Make reporting commands show help about possible sort keys on '-O help'.
- Add metadata_percent to lvs_cols.
- Take account of parity areas with alloc anywhere in _calc_required_extents.
- Use proper uint64 casting for calculation of cache metadata size.
- Better support for nesting of blocking signals.
- Use only sigaction handler and drop duplicate signal handler.
- Separate signal handling and flock code out into lib/misc.
- Don't start dmeventd checking seg_monitor and monitoring is disabled.
- Catch CTRL-c during pvremove prompts.
- Show correct availability status for snapshot origin in lvscan.
- Move segment thin pool/volume info into segment display 'lvdisplay --maps'.
- Display thin pool usage even when just thin volume is available.
- Display monitoring status for monitorable segments in 'lvdisplay --maps'.
- Display virtual extents for virtual LVs in 'lvdisplay --maps'.
- Make vgsplit fail cleanly when not all PVs are specified for RAID 4/5/6.
- Make vgsplit work on mirrors with logs that share PVs with images.
- Use devices/ignore_suspended_devices=0 by default if not defined in lvm.conf.
- Use proper libmem mempool for allocation of unknown segment name.
- Add --readonly to reporting and display tools for lock-free metadata access.
- Add locking_type 5 for dummy locking for tools that do not need any locks.
- Fix _recover_vg() error path when lock conversion fails.
- Use X for LV attributes that are unknown when activation disabled.
- Only output lvdisplay 'LV Status' field when activation is enabled.
- Use lvmetad_used() in pvscan instead of config_tree.
- Configure --enable-udev-systemd-background-jobs if not disabled explicitly.
- Add lvmdump -s to collect system info and context (currently systemd only).
- Refactor allocation code to make A_POSITIONAL_FILL explicit.
- Use thread-safe ctime_r() for clvmd debug logging.
- Skip adding replies to already finished reply thread.
- Use mutex to check number of replies in request_timed_out() in clvmd.
- Drop usage of extra reply_mutex for localsock in clvmd.
- Protect manipulation with finished flag with mutex in clvmd.
- Shift mutex creation and destroy for localsock in clvmd to correct place.
- Fix usage of --test option in clvmd.
- Skip more libraries to be mlocked in memory.
- Remove LOCKED flag for pvmove replaced with error target.
- Return invalid command when specifying negative polling interval.
- Make "help" and "?" reporting fields implicit.
- Recognize implicit "selected" field if using dm_report_init_with_selection.
- Add support for implicit reporting fields which are predefined in libdm.
- Add DM_REPORT_FIELD_TYPE_PERCENT: separate number and percent fields.
- Add dm_percent_range_t,dm_percent_to_float,dm_make_percent to libdm for reuse.
- Add dm_report_reserved_value to libdevmapper for reserved value definition.
- Also display field types when listing all fields in selection help.
- Recognize "help" keyword in selection string to show brief help for selection.
- Always order items reported as string list field lexicographically.
- Add dm_report_field_string_list to libdevmapper for direct string list report.
- Add DM_REPORT_FIELD_TYPE_STRING_LIST: separate string and string list fields.
- Add dm_str_list to libdevmapper for string list type definition and its reuse.
- Add dmsetup -S/--select to define selection criteria for dmsetup reports.
- Add dm_report_init_with_selection to intialize report with selection criteria.
- Add DM_REPORT_FIELD_TYPE_SIZE: separate number and size reporting fields.
- Use RemoveOnStop for dm-event.socket systemd unit.
- Document env var 'DM_DEFAULT_NAME_MANGLING_MODE' in dmsetup man page.
- Warn user about incorrect use of cookie with 'dmsetup remove --force'.
- Also recognize 'help'/'?' as reserved sort key name to show help.
- Add dm_units_to_factor for size unit parsing.
- Increase bitset size for minors for thin dmeventd plugin.

* Mon Jun 09 2014 Alasdair Kergon <agk@redhat.com> - 2.02.106-5
- Remove separate sub-package release tags to fix last commit.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.02.106-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 29 2014 Peter Rajnoha <prajnoha@redhat.com> - 2.02.106-3
- Remove obsolete lvm2-sysvinit subpackage.

* Thu Apr 24 2014 Peter Rajnoha <prajnoha@redhat.com> - 2.02.106-2
- Require exact lvm2/device-mapper version among LVM2 subpackages
  so all of them are always updated synchronously within one update.

* Fri Apr 11 2014 Peter Rajnoha <prajnoha@redhat.com> - 2.02.106-1
- Require latest device-mapper-persistent-data 0.3.2-1.
- Fix ignored --dataalignment/dataalignmentoffset for pvcreate --restorefile.
- Fix lost information about bootloader area when using lvmetad.
- Don't require --major to be specified when using -My option on kernels > 2.4.
- Add configure --disable-thin_check_needs_check to support old thin_check.
- Use thin_check --clear-needs-check-flag by default.
- Add lvmthin man page to section 7.
- Ensure mapped device names are not too long in vg_validate and lvrename.
- Ensure resume failure in lvrename results in command failure.
- Add explicit error message when using lvdisplay -c -m.
- Report error if superfluous argument (e.g. PV name) supplied to pvscan.
- Fix error message for pvdisplay -c -m and add one for pvdisplay -c -s.
- Use EINVALID_CMD_LINE correctly instead of ECMD_FAILED in vgimport/export.
- Obtain list of known VGs from lvmetad for pvchange --all.
- Add man page for lvm-dumpconfig to section 8.
- Validate name for renamed sub LVs.
- When lvrename fails on argument parsing return EINVALID_CMD_LINE.
- Fix exit code regression in failing pvchange command (2.02.66).
- Include 'lvm dumpconfig --type missing' and '--type diff' output to lvmdump.
- Return failure when specifying negative size for pvresize.
- Fix memory corruption in cmd context refresh if clvmd leaks opened device.
- Reinitialise lvmcache properly on fork to fix premature polldaemon exit.
- Add 'lvm dumpconfig --type diff' to show differences from defaults.
- Fix swap signature detection for devices smaller then 2MB.
- Resolve memory release order for clvmd shutdown.
- Report error when lvm2 activation is released in critical_section.
- Fix memory corruption when pvscan reports long pv names.
- Do not report internal orphan VG names when reporting pvdisplay/pvscan.
- Fix pvdisplay -c man page referencing KB instead of sectors.
- Skip redundant synchronization calls on local clvmd.
- Use correct PATH_MAX for locking dir path.
- Do not check for backups when when its creation is disabled.
- Don't allow --mergedconfig without --type current in dumpconfig. Fix memleak.
- Make global/lvdisplay_shows_full_device_path lvm.conf setting profilable.
- Make global/{units|si_unit_consistency|suffix} lvm.conf setting profilable.
- Validate minimal chunk size for snapshot COW volume in lvconvert.
- Disallow lvconvert of origin to snapshot COW volume.
- Make report lvm.conf settings profilable.
- Add existing report settings to lvm.conf.
- Use VG read lock during 'pvscan --cache -aay' autoactivation.
- Issue a VG refresh before autoactivation only if the PV has changed/is new.
- Add flag to lvmetad protocol to indicate the PV scanned has changed/is new.
- Also add vgname to lvmetad protocol when referencing VGs for PVs scanned.
- Add man page for lvm2-activation-generator.
- Don't print an error and accept empty value for global/thin_disabled_features.
- Do not try to check empty pool with scheduled messages.
- Fix return value in pool_has_message() when quering for any message.
- Cleanup all client resources on clvmd exit.
- Use BLKID_CFLAGS when compiling with blkid support.
- Make lvm 'dumpconfig --type default' complete for it to be consumed by lvm.
- Run pvscan --cache via systemd-run in udev if the PV label is detected lost.
- Fix memleak when lvmetad discovers PV to appear on another device.
- Fix calculation of maximum size of COW device for snapshot (2.02.99).
- Do not allow stripe size to be bigger then extent size for lvresize.
- Zero snapshot COW header when creating read-only snapshot.
- Comment out config lines in dumpconfig output without default values defined.
- Improve detection of clustered mirror support.
- Enhance raid code with feature flags, for now checks for raid10.
- Move parsing of VG metadata from vg_commit() back to vg_write() (2.02.99)
- Avoid a PV label scan while in a critical section.
- Create /dev/disk/by-id/lvm-pv-uuid-<PV_UUID> symlink for each PV via udev.
- lvcreate computes RAID4/5/6 stripes if not given from # of allocatable PVs.
- Fix merging of old snapshot into thin volume origin.
- Use --ignoreskippedcluster in lvm2-monitor initscript/systemd unit.
- Do not use VG read/write state for LV read/write state.
- Use --ignoreskippedcluster in activation systemd units if use_lvmetad=0.
- Allow approximate allocation when specifying size in percentage terms.
- Add basic LVM support for cache[pool] segment types.
- Use local exclusive activation for creation of raid in cluster.
- Use correctly signed 64b constant when selecting raid volumes.
- Remove ExecReload from lvmetad systemd unit: lvmetad -R undefined. (2.02.98)
- Do not fork lvmetad if running under systemd.
- Wipe DM_snapshot_cow signature without prompt in new LVs with blkid wiping.
- Avoid exposing temporary devices when initializing raid metadata volumes.
- Add internal tags command to display any tags defined on the host.
- Prohibit use of external origin with size incompatible with thin pool.
- Avoid trying to convert single to thin pool and volume at the same time.
- Add support for partitions on ZFS zvol.
- Fix unwanted drop of hold flocks on forked children.
- Respect LVM_LVMETAD_PIDFILE env var for lvm command.
- Fix test when checking target version for available thin features.
- Detect thin feature external_origin_extend and limit extend when missing.
- Issue error if libbblkid detects signature and fails to return offset/length.
- Update autoconf config.guess/sub to 2014-01-01.
- Online thin pool metadata resize requires 1.10 kernel thin pool target.
- Check for sprintf error when building internal device path.
- Check for sprintf error when creating path for dm control node.
- When buffer for dm_get_library_version() is too small, return error code.
- Always reinitialize _name_mangling_mode in dm_lib_init().
- Stop timeout thread immediately when the last worker thread is finished.
- Fix dmeventd logging with parallel wait event processing.
- Reuse _node_send_messages() for validation of transaction_id in preload.
- Transaction_id could be lower by one only when messages are prepared.
- Wrap is_selinux_enabled() to be called just once.
- Use correctly signed 64b constant when working with raid volumes.
- Exit dmeventd with pidfile cleanup instead of raising SIGKILL on DIE request.
- Add new DM_EVENT_GET_PARAMETERS request to dmeventd protocol.
- Do not use systemd's reload for dmeventd restart, use dmeventd -R instead.

* Mon Jan 27 2014 Peter Rajnoha <prajnoha@redhat.com> - 2.02.105-2
- Avoid exposing temporary devices when initializing thin pool volume.
- Remove udev rule for multipath's PATH_FAILED event processing,
  multipath handles that properly in its own udev rules now.
- Remove duplicate udev rule for cryptsetup temporary devices,
  cryptsetup handles that properly directly in its code.

* Tue Jan 21 2014 Peter Rajnoha <prajnoha@redhat.com> - 2.02.105-1
- Fix thin LV flagging for udev to skip scanning only if the LV is wiped.
- Replace use of xfs_check with xfs_repair in fsadm.
- Mark lvm1 format metadata as FMT_OBSOLETE. Do not use it with lvmetad.
- Invalidate cached VG struct after a PV in it gets orphaned. (2.02.87)
- Mark pool format metadata as FMT_OBSOLETE.
- Use major:minor in lvm2-pvscan@.service for proper global_filter application.
- Syntax and spelling fixes in some man pages.
- Dependency scan counts with snapshots and external origins.
- Make sure VG extent size is always greater or equal to PV phys. block size.
- Optimize double call of stat() for cached devices.
- Enable support for thin provisioning for default configuration.
- Disable online thin pool metadata resize for 1.9 kernel thin target.
- Shortened code for initialization of raid segment types.
- Test for remote exclusive activation after activation fails.
- Support lvconvert --merge for thin snapshots.
- Add support to read thin device id from table line entry.
- Drop extra test for origin when testing merging origin in lv_refresh().
- Extend lv_remove_single() to not print info about removed LV.
- Replace open_count check with lv_check_not_in_use() for snapshot open test.
- Add error messages with LV names for failing lv refresh.
- Compile/link executables with new RELRO and PIE options (non-static builds).
- Support per-object compilation cflags via CFLAGS_object.o.
- Automatically detect support for compiler/linker options to use RELRO and PIE.
- Add --splitsnapshot to lvconvert to separate out cow LV.
- Reinstate origin reload to complete lvconvert -s with active LVs. (2.02.98)
- Select only active volume groups if vgdisplay -A is used.
- Add -p and LVM_LVMETAD_PID env var to lvmetad to change pid file.
- Allow lvmetad to reuse stale socket.
- Only unlink lvmetad socket on error if created by the same process.
- Append missing newline to lvmetad missing socket path error message.
- Add allocation/use_blkid_wiping to lvm.conf to enable blkid wiping.
- Enable blkid_wiping by default if the blkid library is present.
- Add configure --disable-blkid_wiping to disable libblkid signature detection.
- Add -W/--wipesignatures lvcreate option to support wiping on new LVs.
- Add allocation/wipe_signatures_when_zeroing_new_lvs to lvm.conf.
- Do not fail the whole autoactivation if the VG refresh done before fails.
- Do not connect to lvmetad on vg/lvchange --sysinit -aay and socket absent.
- Use lv_check_not_in_use() when testing device in use before merging.
- Check for failure of lvmcache_add_mda() when writing pv.
- Check for failure of dev_get_size() when reporting device size.
- Drop extra unneeded '/' when scanning sysfs directory.
- Fix undef value if skipped clustered VG ignored for toollib PV seg. (2.02.103)
- Support validation of VG/LV names in liblvm/python.
- Allow creation of PVs with arguments to liblvm/python.
- Ensure sufficient metadata copies retained in liblvm/python vgreduce.
- Fix installation of profiles from conf subdir when not building in srcdir.
- Show UUIDs for missing PVs in reports.
- Add reporting of thin_id device id for thin volumes.
- Fix reporting of empty numerical values for recently-added fields.
- Revert activation of activated nodes if a node preload callback fails.
- Avoid busy looping on CPU when dmeventd reads event DM_WAIT_RETRY.
- Ensure global mutex is held when working with dmeventd thread.
- Drop taking timeout mutex for un/registering dmeventd monitor.
- Allow section names in config file data to be quoted strings.
- Close fifos before exiting in dmeventd restart() error path.
- Catch invalid use of string sort values when reporting numerical fields.
- Require util-linux >= 2.24 for blkid wiping support (via device-mapper pkg).
- Add BuildRequires: libblkid-devel to build with blkid wiping functionality.
- Do not install /run and /run/lvm directory but only own them by lvm2 package.
  These dirs are controlled by systemd's tmpfiles.d/lvm2.conf configuration.
- Consolidate file permissions for all packaged files.

* Thu Jan 16 2014 Ville Skyttä <ville.skytta@iki.fi> - 2.02.104-4
- Drop INSTALL from docs, escape percents in %%changelog.

* Fri Dec 13 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.104-3
- Change lvm2-python-libs to require lvm2, not just lvm2-libs.

* Wed Dec 11 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.104-2
- Fix SYSTEMD_READY assignment for foreign devs in lvmetad rules.

* Thu Nov 14 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.104-1
- Workaround VG refresh race during autoactivation by retrying the refresh.
- Handle failures in temporary mirror used when adding images to mirrors.
- Fix and improve logic for implicitely exclusive activations.
- Return success when LV cannot be activated because of volume_list filter.
- Return proper error state for remote exclusive activation.
- Fix clvmd message verification to not reject REMOTE flag. (2.02.100)
- Compare equality of double values with DBL_EPSILON predefined constant.
- Use additional gcc warning flags by default.
- Add ignore_lvm_mirrors to config file to read/ignore labels on mirrors.
- Use #ifdef __linux__ instead of linux throughout.
- Consistently report on stderr when device is not found for dmsetup info.
- Skip race errors when non-udev dmsetup build runs on udev-enabled system.
- Skip error message when holders are not present in sysfs.

* Wed Oct 30 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.103-3
- Fix missing lvmetad scan for PVs found on MD partitions.
- Respect DM_UDEV_DISABLE_OTHER_RULES_FLAG in lvmetad udev rules.

* Fri Oct 25 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.103-2
- Add internal flag for temporary LVs to properly direct udev to not interfere.
- Fix endless loop in blkdeactivate <device>... if unable to umount/deactivate.
- Add dev-block-<major>:<minor>.device systemd alias for complete PV tracking.
- Use major:minor as short form of --major and --minor arg for pvscan --cache.
- Remove 2>/dev/null from three lvm commands executed by vgimportclone.
- Add configure --enable-udev-systemd-background-jobs.
- Add lvm2-pvscan@.service to run pvscan as a service for lvmetad/autoactivation.
- Fix lvconvert swap of poolmetadata volume for active thin pool.
- Check for open count with a timeout before removal/deactivation of an LV.
- Report RAID images split with tracking as out-of-sync ("I").
- Improve parsing of snapshot lv segment.
- Add workaround for deactivation problem of opened virtual snapshot.
- Disable unsupported merge for virtual snapshot.
- Move code to remove virtual snapshot from tools to lib for lvm2app.
- Fix possible race during daemon worker thread creation (lvmetad).
- Fix possible deadlock while clearing lvmetad cache for full rescan.
- Fix possible race while creating/destroying memory pools.
- Recognise NVM Express devices in filter.
- Fix failing metadata repair when lvmetad is used.
- Fix incorrect memory handling when reading messages from lvmetad.
- Fix locking in lvmetad when handling the PV which is gone.
- Recognize new flag to skip udev scanning in udev rules and act appropriately.
- Add support for flagging an LV to skip udev scanning during activation.
- Improve message when unable to change discards setting on active thin pool.
- Run full scan before vgrename operation to avoid any cache name collision.
- Fix lvconvert when converting to a thin pool and thin LV at once.
- Skip race errors when non-udev dmsetup build runs on udev-enabled system.
- Skip error message when holders are not present in sysfs.
- Use __linux__ instead of linux define to make libdevmapper.h C compliant.

* Fri Oct 04 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.103-1
- Ensure vgid matches before removing vgname entry from lvmetad cache.
- Add --ignoreskippedcluster for exit status success when clustered VGs skipped.
- Fix 3 minute udev timeout so that it is applied for all LVM volumes.
- Fix thin/raid & activation config defaults with configure --disable-devmapper.
- Fix RAID calculation for sufficient allocatable space.
- lvconvert from linear to mirror or RAID1 now honors mirror_segtype_default.
- Add thin-performance configuration profile.
- Add lvm.conf allocation/thin_pool_chunk_size_policy option.
- Fix contiguous & cling allocation policies for parity RAID.  (2.02.100)
- Have lvmconf --enable/disable-cluster reset/set use_lvmetad.
- Add seg_size_pe field to reports.
- Support start+length notation with command line PE ranges.
- Exit cleanly with message when pvmove cannot restart because LV is inactive.
- Define symbolic names for subsystem udev flags in libdevmapper for easier use.
- Make subsystem udev rules responsible for importing DM_SUBSYSTEM_UDEV_FLAG*.

* Tue Sep 24 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.102-1
- Fix missing build dependency for scripts subdir in Makefile.
- Fix node up/down handling in clvmd corosync module.
- Fix 3-thread clvmd deadlock triggered by cleanup on EOF from client.
- Remove VG from lvmetad before restoring it with vgcfgrestore.
- Add devtypes report command to display built-in recognised block device types.
- Fix CC Makefile override which had reverted to using built-in value. (2.02.75)
- Recognise bcache block devices in filter (experimental).
- Run lvm2-activation-net after lvm2-activation service to prevent parallel run.
- Add man page entries for lvmdump's -u and -l options.
- Fix lvm2app segfault while using lvm_list_pvs_free fn if there are no PVs.
- Improve of clvmd singlenode locking simulation.
- lvconvert no longer converts LVs of "mirror" segment type to thinpool.
- lvconvert no longer converts thinpool sub-LVs to "mirror" segment type.
- Direct udev to use 3min timeout for LVM devices. Recent udev has default 30s.
- Do not scan multipath or RAID components and avoid incorrect autoactivation.
- Fix MD/loop udev handling to fire autoactivation after setup or coldplug only.
- Make RAID capable of single-machine exclusive operations in a cluster.
- Drop calculation of read ahead for deactivated volume.
- Check for exactly one lv segment in validation of thin pools and volumes.
- Fix dmeventd unmonitoring of thin pools.
- Fix lvresize for stacked thin pool volumes (i.e. mirrors).
- Write Completed debug message before reinstating log defaults after command.
- Refresh existing VG before autoactivation (event retrigger/device reappeared).
- Use pvscan -b in udev rules to avoid a deadlock on udev process count limit.
- Add pvscan -b/--background for the command to be processed in the background.
- Don't assume stdin file descriptor is readable.
- Avoid unlimited recursion when creating dtree containing inactive pvmove LV.
- Require exactly 3 arguments for lvm2-activation-generator. Remove defaults.
- Inform lvmetad about any lost PV label to make it in sync with system state.
- Support most of lvchange operations on stacked thin pool meta/data LVs.
- Enable non-clustered pvmove of snapshots and snapshot origins.
- Add ability to pvmove non-clustered RAID, mirror, and thin volumes.
- Make lvm2-activation-generator silent unless it's in error state.
- Remove "mpath major is not dm major" msg for mpath component scan (2.02.94).
- Prevent cluster mirror logs from being corrupted by redundant checkpoints.
- Fix ignored lvmetad update on loop device configuration (2.02.99).
- Use LVM_PATH instead of hardcoded value in lvm2 activation systemd generator.
- Fix vgck to notice on-disk corruption even if lvmetad is used.
- Move mpath device filter before partitioned filter (which opens devices).
- Require confirmation for vgchange -c when no VGs listed explicitly.
- Also skip /var and /var/log by default in blkdeactivate when unmounting.
- Add support for bind mounts in blkdeactivate.
- Add blkdeactivate -v/--verbose for debug output from external tools used.
- Add blkdeactivate -e/--errors for error messages from external tools used.
- Suppress messages from external tools called in blkdeactivate by default.
- Fix inability to remove a VG's cluster flag if it contains a mirror.
- Fix bug making lvchange unable to change recovery rate for RAID.
- Prohibit conversion of thin pool to external origin.
- Workaround gcc v4.8 -O2 bug causing failures if config/checks=1 (32bit arch).
- Verify clvmd message validity before processing and log error if incorrect.
- When creating PV on existing LV don't forbid reserved LV names on LVs below.
- When converting mirrors, default segtype should be the same unless specified.
- Make "raid1" the default mirror segment type.
- Fix clogd descriptor leak when daemonizing.
- Fix clvmd descriptor leak on restart.
- Add pipe_open/close() to use instead of less efficient/secure popen().
- Inherit and apply any profile attached to a VG if creating new thin pool.
- Add initial support thin pool lvconvert --repair.
- Add --with-thin-repair and --with-thin-dump configure options.
- Add lvm.conf thin_repair/dump_executable and thin_repair_options.
- Require 1.9 thin pool target version for online thin pool metadata resize.
- Ignore previous LV seg with alloc contiguous & cling when num stripes varies.
- Fix segfault if devices/global_filter is not specified correctly.
- Tidy dmeventd fifo initialisation.
- Detect invalid sector supplied to 'dmsetup message'.
- Free any previously-set string if a dm_task_set_* function is called again.
- Do not allow passing empty new name for dmsetup rename.
- Display any output returned by 'dmsetup message'.
- Add dm_task_get_message_response to libdevmapper.
- Create dmeventd timeout threads as "detached" so exit status is freed.
- Add DM_ABORT_ON_INTERNAL_ERRORS env var support to abort on internal errors.

* Tue Aug 06 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.99-2
- Fix metadata area offset/size overflow if it's >= 4g and while using lvmetad.
- Require the newest device-mapper-persistent-data-0.2.3-1.
- Fix spec file's util-linux version definition for proper expansion when used.

* Thu Jul 25 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.99-1
-  o Features/Extensions/Additions:
- Add support for poolmetadataspare LV, that will be used for pool recovery.
- Improve activation order when creating thin pools in non-clustered VG.
- Add lvm2-activation-net systemd unit to activate LVs on net-attached storage.
- Automatically flag thin snapshots to be skipped during activation.
- Add support for persistent flagging of LVs to be skipped during activation.
- Make selected thinp settings customizable by a profile.
- Support storing profile name in metadata for both VGs and LVs.
- Add support for configuration profiles.
- Add support for thin volumes in vgsplit.
- Add lvresize support for online thin pool metadata volume resize.
- Add detection for thin pool metadata resize kernel support.
- Add vg->vg_ondisk / lv_ondisk() holding committed metadata.
- Add detection of mounted fs also for vgchange deactivation.
- Detect maximum usable size for snapshot for lvresize.
- Improve RAID kernel status retrieval to include sync_action/mismatch_cnt.
- Add external origin support for lvcreate.
- Support automatic config validation.
- Add PV header extension: extension version, flags and bootloader areas.
- Initial support for lvconvert of thin external origin.
- Improve activation code for better support of stacked devices.
- vgimport '--force' now allows import of VGs with missing PVs.
- Allow removal or replacement of RAID LV components that are error segments.
- Make 'vgreduce --removemissing' able to handle RAID LVs with missing PVs.
- Give precedence to EMC power2 devices with duplicate PVIDs.
- Recognise Storage Class Memory (IBM S/390) devices in filter.
- Recognise STEC skd devices in filter.
- Recognise Violin Memory vtms devices in filter.
- Automatically restore MISSING PVs with no MDAs.
- Detect mounted fs also via reading /proc/self/mountinfo.
-  o Command Interface/Options:
- Support ARG_GROUPABLE with merge_synonym (for --raidwritemostly).
- Add --ignoreactivationskip to lvcreate/vgchange/lvchange to ignore skip flag.
- Add --setactivationskip to lvcreate/lvchange to set activation skip flag.
- Add --type profilable to lvm dumpconfig to show profilable config settings.
- Add --mergedconfig to lvm dumpconfig for merged --config/--profile/lvm.conf.
- Support changing VG/LV profiles: vgchange/lvchange --profile/--detachprofile.
- Add new --profile command line arg to select a configuration profile for use.
- For creation of snapshot require size for at least 3 chunks.
- Do not accept size parameters bigger then 16EiB.
- Accept --yes in all commands so test scripts can be simpler.
- Add lvcreate/lvchange --[raid]{min|max}recoveryrate for raid LVs.
- Add lvchange --[raid]writemostly/writebehind support for RAID1
- Add lvchange --[raid]syncaction for scrubbing of RAID LVs.
- Add --validate option to lvm dumpconfig to validate current config on demand.
- Add --ignoreadvanced and --ignoreunsupported switch to lvm dumpconfig.
- Add --withcomments and --withversions switch to lvm dumpconfig.
- Add --type {current|default|missing|new} and --atversion to lvm dumpconfig.
- Add --bootloaderareasize to pvcreate and vgconvert to create bootloader area.
- Do not take a free lv name argument for lvconvert --thinpool option.
- Allow lvconvert --stripes/stripesize only with --mirrors/--repair/--thinpool.
- Do not ignore -f in lvconvert --repair -y -f for mirror and raid volumes.
- Support use of option --yes for lvchange --persistent.
- Fix clvmd support for option -d and properly use its argument.
-  o Reporting:
- Issue an error msg if lvconvert --type used incorrectly with other options.
- Use LOG_DEBUG/ERR msg severity instead default for lvm2-activation-generator.
- Add LV report fields: raid_mismatch_count/raid_sync_action/raid_write_behind.
- Add LV reporting fields raid_min_recovery_rate, raid_max_recovery_rate.
- Add sync_percent as alias for copy_percent LV reporting field.
- Add lv_ prefix to modules reporting field.
- Use units B or b (never E) with no decimal places when displaying sizes < 1k.
- List thin-pool and thin modules for thin volumes.
- Add 's(k)ip activation' bit to lvs -o lv_attr to indicate skip flag attached.
- Improve error loging when user tries to interrupt commands.
- Add vgs/lvs -o vg_profile/lv_profile to report profiles attached to VG/LV.
- Report lvs volume type 'e' with higher priority.
- Report lvs volume type 'o' also for external origin volumes.
- Report lvs target type 't' only for thin pools and thin volumes.
- Add "active" LV reporting field to show activation state.
- Add "monitor" segment reporting field to show dmevent monitoring status.
- Add explicit message about unsupported pvmove for thin/thinpool volumes.
- Add pvs -o pv_ba_start,pv_ba_size to report bootloader area start and size.
- Fix pvs -o pv_free reporting for PVs with zero PE count.
- Report blank origin_size field if the LV doesn't have an origin instead of 0.
- Report partial and in-sync RAID attribute based on kernel status
- Log output also to syslog when abort_on_internal_error is set.
- Change lvs heading Copy%% to Cpy%%Sync and print RAID4/5/6 sync%% there too.
- Report error for nonexisting devices in dmeventd communication.
- Reduce some log_error messages to log_warn where we don't fail.
-  o Configuration:
- Add activation/auto_set_activation_skip to control activation skip flagging.
- Add default.profile configuration profile and install it on make install.
- Add config/profile_dir to set working directory to load profiles from.
- Use mirror_segtype_default if type not specified for linear->mirror upconvert.
- Refine lvm.conf and man page documentation for autoactivation feature.
- Override system's global_filter settings for vgimportclone.
- Find newest timestamp of merged config files.
- Add 'config' section to lvm.conf to set the way the LVM configuration is handled.
- Add global/raid10_segtype_default to lvm.conf.
- Accept activation/raid_region_size in preference to mirror_region_size config.
- Add log/debug_classes to lvm.conf to control debug log messages.
- Allow empty activation/{auto_activation|read_only|}_volume_list config option.
- Relax ignore_suspended_devices to read from mirrors that don't have a device marked failed.
-  o Documentation:
- Add man page entries for profile configuration and related options.
- Document lvextend --use-policies option in man.
- Improve lvcreate, lvconvert and lvm man pages.
-  o API/interfaces:
- liblvm/python API: Additions: PV create/removal/resize/listing
- liblvm/python API: Additions: LV attr/origin/Thin pool/Thin LV creation
- Fix exported symbols regex for non-GNU busybox sed.
- Add LV snapshot support to liblvm and python-lvm.
- Remove python liblvm object. systemdir can only be changed using env var now.
- Add dm_get_status_snapshot() for parsing snapshot status.
- Append discards and read-only fields to exported struct dm_status_thin_pool.
- Validate passed params to dm_get_status_raid/thin/thin_pool().
- Add dm_mountinfo_read() for parsing /proc/self/mountinfo.
- Add dm_config_write_{node_out/one_node_out} for enhanced config output.
- Add dm_config_value_is_bool to check for boolean value in supported formats.
- Add DM_ARRAY_SIZE public macro.
- Add DM_TO_STRING public macro.
- Implement ref-counting for parents in python lib.
-  o Fixes (general):
- Do not zero init 4KB of thin snapshot for non-zeroing thin pool (2.02.94).
- Correct thin creation error paths.
- Add whole log_lv and metadata_lv sub volumes when creating partial tree.
- Properly use snapshot layer for origin which is also thin volume.
- Avoid generating metadata backup when calling update_pool_lv().
- Send thin messages also for active thin pool and inactive thin volume.
- Avoid creation of multiple archives for one command.
- Avoid flushing thin pool when just requesting transaction_id.
- Fix use of too big chunks of memory when communication with lvmetad.
- Also filter partitions on mpath components if multipath_component_detection=1.
- Do not use persistent filter with lvmetad.
- Move syslog code out of signal handle in dmeventd.
- Fix lvresize --use-policies of VALID but 100%% full snapshot.
- Skip monitoring of snapshots that are already bigger then origin.
- Refuse to init a snapshot merge in lvconvert if there's no kernel support.
- Fix alignment of PV data area if detected alignment less than 1 MB (2.02.74).
- Fix creation and removal of clustered snapshot.
- Fix clvmd caching of metadata when suspending inactive volumes.
- Fix lvmetad error path in lvmetad_vg_lookup() for null vgname.
- Fix clvmd _cluster_request() return code in memory fail path.
- Fix vgextend to not allow a PV with 0 MDAs to be used while already in a VG.
- Fix PV alignment to incorporate alignment offset if the PV has zero MDAs.
- Fix missing cleanup of flags when the LV is detached from pool.
- Fix check for some forbidden discards conversion of thin pools.
- Limit RAID device replacement to repair only if LV is not in-sync.
- Disallow RAID device replacement or repair on inactive LVs.
- Unlock vg mutex in error path when lvmetad tries to lock_vg.
- Detect key string duplication failure in config_make_nodes_v in libdaemon.
- Disallow pvmove on RAID LVs until they are addressed properly
- Recognize DM_DISABLE_UDEV environment variable for a complete fallback.
- When no --stripes argument is given when creating a RAID10 volume, default to 2 stripes.
- Do not allow lvconvert --splitmirrors on RAID10 logical volumes.
- Repair a mirrored log before the mirror itself when both fail.
- Avoid trying to read a mirror that has a failed device in its mirrored log.
- Fix segfault for truncated string token in config file after the first '"'.
- Fix config node lookup inside empty sections to not return the section itself.
- Fix parsing of 64bit snapshot status in dmeventd snapshot plugin.
- Always return success on dmeventd -V command call.
-  o Fixes (segfaults/crashes/deadlocks/races):
- Fix segfault when reporting raid_syncaction for older kernels.
- Fix vgcfgrestore crash when specified incorrect vg name.
- Check for memory failure of dm_config_write_node() in lvmetad.
- Prevent double free error after dmeventd call of _fill_device_data().
-  o Fixes (resource leaks/memleaks):
- Release memory allocated with _cached_info().
- Release memory and unblock signals in lock_vol error path.
- Fix memory resource leak in memlocking error path.
- Fix memleak in dmeventd thin plugin in device list obtaining err path.
- Fix socket leak on error path in lvmetad's handle_connect.
- Fix memleak on error path for lvmetad's pv_found.
- Fix memleak in device_is_usable mirror testing function.
- Fix memory leak on error path for pvcreate with invalid uuid.
- Fix resource leak in error path of dmeventd's umount of thin volume.
-  o Testing:
- Fix test for active snapshot in cluster before resizing it.
- Add python-lvm unit test case
-  o Other:
- Use local activation for clearing snapshot COW device.
- Add configure --with-default-profile-subdir to select dir to keep profiles in.
- Creation of snapshot takes at most 100%% origin coverage.
- Use LC_ALL to set locale in daemons and fsadm instead of lower priority LANG.
- Optimize out setting the same value of read_ahead.
- Automatically deactivate failed preloaded dm tree node.
- Process thin messages once to active thin pool target for dm_tree.
-  o Packaging:
- Add /etc/lvm/profile dir and /etc/lvm/profile/default.profile to lvm2 package.
- Do not include /lib/udev and /lib/udev/rules.d in device-mapper package.
- Fix some incorrect changelog dates.

* Tue May 14 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.98-9
- Fix 'dmsetup splitname -o' to not fail if used without '-c' switch (1.02.68).
- Close open dmeventd FIFO file descriptors on exec (FD_CLOEXEC).
- Fix premature DM version checking which caused useless mapper/control access.
- Recognize DM_DISABLE_UDEV environment variable for a complete fallback.
- Do not verify udev operations if --noudevsync command option is used.
- Fix blkdeactivate to handle nested mountpoints and mangled mount paths.
- Fix a crash-inducing race condition in lvmetad while updating metadata.
- Fix possible race while removing metadata from lvmetad.
- Fix possible deadlock when querying and updating lvmetad at the same time.
- Avoid a global lock in pvs when lvmetad is in use.
- Fix crash in pvscan --cache -aay triggered by non-mda PV.
- Fix lvm2app to return all property sizes in bytes.
- Add lvm.conf option global/thin_disabled_features.
- Add lvconvert support to swap thin pool metadata volume.
- Implement internal function detach_pool_metadata_lv().
- Fix lvm2app and return lvseg discards property as string.
- Allow forced vgcfgrestore of lvm2 metadata with thin volumes.
- Add lvm.conf thin pool defs thin_pool_{chunk_size|discards|zero}.
- Support discards for non-power-of-2 thin pool chunks.
- Support allocation of pool metadata with lvconvert command.
- Move common functionality for thin lvcreate and lvconvert to toollib.
- Use lv_is_active() instead of lv_info() call.

* Fri May 03 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.98-8
- Fix non-functional autoactivation of LVM volumes on top of MD devices.

* Fri Apr 19 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.98-7
- Autoactivate VG/LV on coldplug of DM-based PVs at boot.

* Tue Apr 09 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.98-6
- Synchronize with udev in pvscan --cache and fix dangling udev_sync cookies.
- Fix autoactivation to not autoactivate VG/LV on each change of the PVs used.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.02.98-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Dec 06 2012 Peter Rajnoha <prajnoha@redhat.com> - 2.02.98-4
- Skip mlocking [vectors] on arm architecture.

* Sat Nov 17 2012 Peter Rajnoha <prajnoha@redhat.com> - 2.02.98-3
- Add lvm2-activation-generator systemd generator to automatically generate
  systemd units to activate LVM2 volumes even if lvmetad is not used.
  This replaces lvm activation part of the former fedora-storage-init
  script that was included in the initscripts package before.
- Enable lvmetad - the LVM metadata daemon by default.
- Exit pvscan --cache immediately if cluster locking used or lvmetad not used.
- Don't use lvmetad in lvm2-monitor.service ExecStop to avoid a systemd issue.
- Remove dependency on fedora-storage-init.service in lvm2 systemd units.
- Depend on lvm2-lvmetad.socket in lvm2-monitor.service systemd unit.
- Init lvmetad lazily to avoid early socket access on config overrides.
- Hardcode use_lvmetad=0 if cluster locking used and issue a warning msg.
- Fix dm_task_set_cookie to properly process udev flags if udev_sync disabled.

* Sat Oct 20 2012 Peter Rajnoha <prajnoha@redhat.com> - 2.02.98-2
- Incorporate former python-lvm package in lvm2 as lvm2-python-libs subpackage.

* Tue Oct 16 2012 Peter Rajnoha <prajnoha@redhat.com> - 2.02.98-1
- Don't try to issue discards to a missing PV to avoid segfault.
- Fix vgchange -aay not to activate non-matching LVs that follow a matching LV.
- Fix lvchange --resync for RAID LVs which had no effect.
- Add RAID10 support (--type raid10).
- Introduce blkdeactivate script to deactivate block devs with dependencies.
- Apply 'dmsetup mangle' for dm UUIDs besides dm names.
- Use -q as short form of --quiet.
- Suppress non-essential stdout with -qq.
- Add log/silent to lvm.conf equivalent to -qq.
- Add (p)artial attribute to lvs.
- Implement devices/global_filter to hide devices from lvmetad.
- Add lvmdump -l, to collect a state dump from lvmetad.
- Add --discards to lvconvert.
- Add support for lvcreate --discards.
- Add --poolmetadata to lvconvert and support thin meta/data dev stacking.
- Support creation of read-only thin volumes (lvcreate -p r).
- Support changes of permissions for thin snapshot volumes.
- Make lvremove ask before discarding data areas.
- Prohibit not yet supported change of thin-pool to read-only.
- Using autoextend percent 0 for thin pool fails 'lvextend --use-policies'.
- Make vgscan --cache an alias for pvscan --cache.
- Clear lvmetad metadata/PV cache before a rescan.
- Fix a segmentation fault upon receiving a corrupt lvmetad response.
- Give inconsistent metadata warnings in pvscan --cache.
- Avoid overlapping locks that could cause a deadlock in lvmetad.
- Fix memory leaks in libdaemon and lvmetad.
- Optimize libdaemon logging for a fast no-output path.
- Only create lvmetad pidfile when running as a daemon (no -f).
- Warn if lvmetad is running but disabled.
- Warn about running lvmetad with use_lvmetad = 0 in example.conf.
- Update lvmetad help output (flags and their meaning).
- Make pvscan --cache read metadata from LVM1 PVs.
- Make libdaemon buffer handling asymptotically more efficient.
- Make --sysinit suppress lvmetad connection failure warnings.
- Prohibit usage of lvcreate --thinpool with --mirrors.
- Fix lvm2api origin reporting for thin snapshot volume.
- Add implementation of lvm2api function lvm_percent_to_float.
- Allow non power of 2 thin chunk sizes if thin pool driver supports that.
- Allow limited metadata changes when PVs are missing via [vg|lv]change.
- Do not start dmeventd for lvchange --resync when monitoring is off.
- Remove pvscan --cache from lvm2-lvmetad init script.
- Remove ExecStartPost with pvscan --cache from lvm2-lvmetad.service.
- Report invalid percentage for property snap_percent of non-snaphot LVs.
- Disallow conversion of thin LVs to mirrors.
- Fix lvm2api data_percent reporting for thin volumes.
- Do not allow RAID LVs in a clustered volume group.
- Enhance insert_layer_for_lv() with recursive rename for _tdata LVs.
- Skip building dm tree for thin pool when called with origin_only flag.
- Ensure descriptors 0,1,2 are always available, using /dev/null if necessary.
- Use /proc/self/fd when available for closing opened descriptors efficiently.
- Fix inability to create, extend or convert to a large (> 1TiB) RAID LV.
- Update lvmetad communications to cope with clients using different filters.
- Clear LV_NOSYNCED flag when a RAID1 LV is converted to a linear LV.
- Disallow RAID1 upconvert if the LV was created with --nosync.
- Depend on systemd-udev-settle in units generated by activation generator.
- Disallow addition of RAID images until the array is in-sync.
- Fix RAID LV creation with '--test' so valid commands do not fail.
- Add lvm_lv_rename() to lvm2api.
- Fix setvbuf code by closing and reopening stream before changing buffer.
- Disable private buffering when using liblvm.
- When private stdin/stdout buffering is not used always use silent mode.
- Fix 32-bit device size arithmetic needing 64-bit casting throughout tree.
- Fix dereference of NULL in lvmetad error path logging.
- Fix buffer memory leak in lvmetad logging.
- Correct the discards field in the lvs manpage (2.02.97).
- Use proper condition to check for discards settings unsupported by kernel.
- Reinstate correct default to ignore discards for thin metadata from old tools.
- Issue error message when -i and -m args do not match specified RAID type.
- Change lvmetad logging syntax from -ddd to -l {all|wire|debug}.
- Add new libdaemon logging infrastructure.
- Support unmount of thin volumes from pool above thin pool threshold.
- Update man page to reflect that dm UUIDs are being mangled as well.
- Add 'mangled_uuid' and 'unmangled_uuid' fields to dmsetup info -c -o.
- Mangle device UUID on dm_task_set_uuid/newuuid call if necessary.
- Add dm_task_get_uuid_mangled/unmangled to libdevmapper.
- Always reset delay_resume_if_new flag when stacking thin pool over anything.
- Don't create value for dm_config_node and require dm_config_create_value call.
- Check for existing new_name for dmsetup rename.
- Fix memory leak in dmsetup _get_split_name() error path.
- Clean up spec file and keep support only for Fedora 18 upwards.
- Use systemd macros in rpm scriptlets to set up systemd units.
- Add Requires: bash >= 4.0 for blkdeactivate script.

* Tue Aug 07 2012 Alasdair Kergon <agk@redhat.com> - 2.02.97-1
- Improve documention of allocation policies in lvm.8.
- Increase limit for major:minor to 4095:1048575 when using -My option.
- Add generator for lvm2 activation systemd units.
- Add lvm_config_find_bool lvm2app fn to retrieve bool value from config tree.
- Respect --test when using lvmetad.
- No longer capitalise first LV attribute char for invalid snapshots.
- Allow vgextend to add PVs to a VG that is missing PVs.
- Recognise Micron PCIe SSDs in filter and move array out to device-types.h.
- Fix dumpconfig <node> to print only <node> without its siblings. (2.02.89)
- Do not issue "Failed to handle a client connection" error if lvmetad killed.
- Support lvchange --discards and -Z with thin pools.
- Add discard LV segment field to reports.
- Add --discards to lvcreate --thin.
- Set discard and external snapshot features if thin pool target is vsn 1.1+.
- Count percentage of completeness upwards not downwards when merging snapshot.
- Skip activation when using vg/lvchange --sysinit -a ay and lvmetad is active.
- Fix extending RAID 4/5/6 logical volumes
- Fix test for PV with unknown VG in process_each_pv to ignore ignored mdas.
- Fix _alloc_parallel_area to avoid picking already-full areas for raid devices.
- Never issue discards when LV extents are being reconfigured, not deleted.
- Allow release_lv_segment_area to fail as functions it calls can fail.
- Fix missing sync of filesystem when creating thin volume snapshot.
- Allow --noflush with dmsetup status and wait (for thin target).
- Add dm_config_write_one_node to libdevmapper.
- Add dm_vasprintf to libdevmapper.
- Support thin pool message release/reserve_metadata_snap in libdevmapper.
- Support thin pool discards and external origin features in libdevmapper.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.02.96-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 04 2012 Peter Rajnoha <prajnoha@redhat.com> - 2.02.96-3
- Use configure --with-default-pid-dir=/run.
- Use globally set prefix for udev rules path.

* Mon Jul 02 2012 Peter Rajnoha <prajnoha@redhat.com> - 2.02.96-2
- Compile with lvmetad support enabled.
- Add support for volume autoactivation using lvmetad.
- Update man pages with --activate ay option and auto_activation_volume_list.
- Use vgchange -aay instead of vgchange -ay in clmvd init script.
- Add activation/auto_activation_volume_list to lvm.conf.
- Add --activate ay to lvcreate, lvchange, pvscan and vgchange.
- Add --activate synonym for --available arg and prefer --activate.
- Open device read-only to obtain readahead value.
- Add configure --enable-udev-rule-exec-detection to detect exec path in rules.
- Use sbindir in udev rules by default and remove executable path detection.
- Remove hard-coded paths for dmeventd fifos and use default-dm-run-dir.
- Add configure --with-lvmetad-pidfile to remove hard-coded value.
- Add configure --with-default-pid-dir for common directory with pid files.
- Add configure --with-default-dm-run-dir to set run directory for dm tools.
- Add documentation references in systemd units.
- Clean up spec file and keep support only for Fedora 17 upwards.

* Mon Jun 18 2012 Alasdair Kergon <agk@redhat.com> - 2.02.96-1
- Require device-mapper-persistent-data package for thin provisioning.
- Set delay_resume_if_new on deptree snapshot origin.
- Log value chosen in _find_config_bool like other variable types do.
- Wait for dmeventd to exit after sending it DM_EVENT_CMD_DIE when restarting.
- Append 'Used' to {Blk}DevNames/DevNos dmsetup report headers for clarity.
- Remove dmeventd fifos on exit if they are not managed by systemd.
- Use SD_ACTIVATION environment variable in systemd units to detect systemd.
- Only start a new dmeventd instance on restart if one was already running.
- Extend the time waited for input from dmeventd fifo to 5 secs. (1.02.73)
- Fix error paths for regex filter initialization.
- Re-enable partial activation of non-thin LVs until it can be fixed. (2.02.90)
- Fix alloc cling to cling to PVs already found with contiguous policy.
- Fix cling policy not to behave like normal policy if no previous LV seg.
- Fix allocation loop not to use later policies when --alloc cling without tags.
- Fix division by zero if PV with zero PE count is used during vgcfgrestore.
- Add initial support for thin pool lvconvert.
- Fix lvrename for thin volumes (regression in for_each_sub_lv). (2.02.89)
- Fix up-convert when mirror activation is controlled by volume_list and tags.
- Warn of deadlock risk when using snapshots of mirror segment type.
- Fix bug in cmirror that caused incorrect status info to print on some nodes.
- Remove statement that snapshots cannot be tagged from lvm man page.
- Disallow changing cluster attribute of VG while RAID LVs are active.
- Fix lvconvert error message for non-mergeable volumes.
- Allow subset of failed devices to be replaced in RAID LVs.
- Prevent resume from creating error devices that already exist from suspend.
- Update and correct lvs man page with supported column names.
- Handle replacement of an active device that goes missing with an error device.
- Change change raid1 segtype always to request a flush when suspending.
- Add udev info and context to lvmdump.
- Add lvmetad man page.
- Fix RAID device replacement code so that it works under snapshot.
- Fix inability to split RAID1 image while specifying a particular PV.
- Update man pages to give them all the same look&feel.
- Fix lvresize of thin pool for striped devices.
- For lvresize round upward when specifying number of extents.
- For lvcreate with %%FREE support rounding downward stripe alignment.
- Change message severity to log_very_verbose for missing dev info in udev db.
- Fix lvconvert when specifying removal of a RAID device other than last one.
- Fix ability to handle failures in mirrored log in dmeventd plugin. (2.02.89)
- Fix unlocking volume group in vgreduce in error path.
- Cope when VG name is part of the supplied name in lvconvert --splitmirrors -n.
- Fix exclusive lvchange running from other node. (2.02.89)
- Add 'vgscan --cache' functionality for consistency with 'pvscan --cache'.
- Keep exclusive activation in pvmove if LV is already active.
- Disallow exclusive pvmove if some affected LVs are not exclusively activated.
- Remove unused and wrongly set cluster VG flag from clvmd lock query command.
- Fix pvmove for exclusively activated LV pvmove in clustered VG. (2.02.86)
- Update and fix monitoring of thin pool devices.
- Check hash insert success in lock_vg in clvmd.
- Check for buffer overwrite in get_cluster_type() in clvmd.
- Fix global/detect_internal_vg_cache_corruption config check.
- Fix initializiation of thin monitoring. (2.02.92)
- Cope with improperly formatted device numbers in /proc/devices. (2.02.91)
- Exit if LISTEN_PID environment variable incorrect in lvmetad systemd handover.
- Fix fsadm propagation of -e option.
- Fix fsadm parsing of /proc/mounts files (don't check for substrings).
- Fix fsadm usage of arguments with space.
- Fix arg_int_value alongside ARG_GROUPABLE --major/--minor for lvcreate/change.
- Fix name conflicts that prevent down-converting RAID1 when specifying a device
- Improve thin_check option passing and use configured path.
- Add --with-thin-check configure option for path to thin_check.
- Fix error message when pvmove LV activation fails with name already in use.
- Better structure layout for device_info in dev_subsystem_name().
- Change message severity for creation of VG over uninitialised devices.
- Fix error path for failed toolcontext creation.
- Don't unlink socket on lvmetad shutdown if instantiated from systemd.
- Restart lvmetad automatically from systemd if it exits from uncaught signal.
- Fix warn msg for thin pool chunk size and update man for chunksize. (2.02.89)

* Thu Jun 07 2012 Kay Sievers - 2.02.95-8
- Remove explicit Requires: libudev, rpm takes care of that:
    $ rpm -q --requires device-mapper | grep udev
    libudev.so...

* Tue Jun 05 2012 Peter Rajnoha <prajnoha@redhat.com> - 2.02.95-7
- Use BuildRequires: systemd-devel instead of BuildRequires: libudev-devel.
- Remove unsupported udev_get_dev_path libudev call used for checking udev dir.

* Thu Mar 29 2012 Fabio M. Di Nitto <fdinitto@redhat.com> - 2.02.95-6
- BuildRequires and Requires on newer version of corosync and dlm.
- Restart clvmd on upgrades.

* Mon Mar 19 2012 Peter Rajnoha <prajnoha@redhat.com> - 2.02.95-5
- Do not strictly require openais for cmirror subpackage.

* Mon Mar 19 2012 Peter Rajnoha <prajnoha@redhat.com> - 2.02.95-4
- Reinstate cmirror support.
- Detect lvm binary path in lvmetad udev rules.
- Use pvscan --cache instead of vgscan in systemd units/init scripts.

* Fri Mar 16 2012 Fabio M. Di Nitto <fdinitto@redhat.com> - 2.02.95-3
- Rebuild against new corosync (soname change).
- BuildRequires and Requires on newer version of corosync.

* Thu Mar 08 2012 Peter Rajnoha <prajnoha@redhat.com> - 2.02.95-2
- Reload dm-event systemd service on upgrade.

* Tue Mar 06 2012 Alasdair Kergon <agk@redhat.com> - 2.02.95-1
- If unspecified, adjust thin pool metadata and chunk size to fit into 128MB.
- Deactivation of failed thin check on thin pool returns success.
- Check for multiply-mangled names in auto mangling mode.
- Fix dm_task_get_name_unmangled to not unmangle already unmangled name.
- Check whether device names are properly mangled on ioctl return.

* Sat Mar 03 2012 Alasdair Kergon <agk@redhat.com> - 2.02.94-1
- Add support to execute thin_check with each de/active of thin pool.
- Fix automatic estimation of metadata device size for thin pool.
- Wipe initial 4KiB of non zeroed thin volumes.
- Update code-base to incorporate new metadata daemon. (Not used in Fedora yet.)
- Numerous minor cleanups across the code-base.
- Fix dmsetup / dm_task_set_name to properly resolve path to dm name. (2.02.93)

* Thu Feb 23 2012 Alasdair Kergon <agk@redhat.com> - 2.02.93-1
- Moved systemd tmpfiles installation upstream for lvm2 lock and run dirs.
- Require number of stripes to be greater than parity devices in higher RAID.
- Fix allocation code to allow replacement of single RAID 4/5/6 device.
- Check all tags and LV names are in a valid form before writing any metadata.
- Allow 'lvconvert --repair' to operate on RAID 4/5/6.
- Fix build_parallel_areas_from_lv to account correctly for raid parity devices.
- Print message when faulty raid devices have been replaced.

* Mon Feb 20 2012 Alasdair Kergon <agk@redhat.com> - 2.02.92-1
- Read dmeventd monitoring config settings for every lvm command.
- For thin devices, initialize monitoring only for thin pools not thin volumes.
- Make conversion from a synced 'mirror' to 'raid1' not cause a full resync.
- Add clvmd init dependency on dlm service when running with new corosync.
- Switch to using built-in blkid in 13-dm-disk.rules.
- Add "watch" rule to 13-dm-disk.rules.
- Detect failing fifo and skip 20s retry communication period.
- Replace any '\' char with '\\' in dm table specification on input.
- New 'mangle' options in dmsetup/libdevmapper for transparent reversible 
  encoding of characters that udev forbids in device names.
- Add --manglename option to dmsetup to select the name mangling mode.
- Add mangle command to dmsetup to provide renaming to correct mangled form.
- Add 'mangled_name' and 'unmangled_name' fields to dmsetup info -c -o.
- Mangle device name on dm_task_set_name/newname call if necessary.
- Add dm_task_get_name_mangled/unmangled to libdevmapper.
- Add dm_set/get_name_mangling_mode to set/get name mangling in libdevmapper.

* Mon Feb 13 2012 Peter Rajnoha <prajnoha@redhat.com> - 2.02.91-2
- Add configure --with-systemdsystemunitdir.

* Sun Feb 12 2012 Alasdair Kergon <agk@redhat.com> - 2.02.91-1
- New upstream with trivial fixes and refactoring of some lvmcache and orphan code.

* Wed Feb 1 2012 Alasdair Kergon <agk@redhat.com> - 2.02.90-1
- Drop support for cman, openais and cmirror for f17. Require dlm not cluster.
- Automatically detect whether corosync clvmd needs to use confdb or cmap.
- Disable partial activation for thin LVs and LVs with all missing segments.
- sync_local_dev_names before (re)activating mirror log for initialisation.
- Do not print warning for pv_min_size between 512KB and 2MB.
- Clean up systemd unit ordering and requirements.
- Allow ALLOC_NORMAL to track reserved extents for log and data on same PV.
- Fix data%% report for thin volume used as origin for non-thin snapshot.

* Thu Jan 26 2012 Alasdair Kergon <agk@redhat.com> - 2.02.89-2
- New upstream release with experimental support for thinly-provisioned devices.
- The changelog for this release is quite long and contained in 
  WHATS_NEW and WHATS_NEW_DM in the documentation directory.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.02.88-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec 30 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 2.02.88-2
- update util-linux-ng -> util-linux dependency as it changed long ago.

* Mon Aug 22 2011 Alasdair Kergon <agk@redhat.com> - 2.02.88-1
- Remove incorrect 'Breaking' error message from allocation code. (2.02.87)
- Add lvconvert --merge support for raid1 devices split with --trackchanges.
- Add --trackchanges support to lvconvert --splitmirrors option for raid1.
- Add dm_tree_node_add_null_area for temporarily-missing raid devs tracked.
- Support lvconvert of -m1 raid1 devices to a higher number.
- Support splitting off a single raid1 rimage in lvconvert --splitmirrors.
- Add -V as short form of --virtualsize in lvcreate.

* Fri Aug 12 2011 Peter Rajnoha <prajnoha@redhat.com> - 2.02.87-1
- Cache and share generated VG structs to improve performance.
- Suppress locking error messages in monitoring init scripts.
- Add global/detect_internal_vg_cache_corruption to lvm.conf.
- If pipe in clvmd fails return busy instead of using uninitialised descriptors.
- Initialise clvmd locks before lvm context to avoid open descriptor leaks.
- Suppress low-level locking errors and warnings while using --sysinit.
- Add test for fcntl error in singlenode client code.
- Compare file size (as well as timestamp) to detect changed config file.
- Change DEFAULT_UDEV_SYNC to 1 so udev_sync is used if there is no config file.
- Update udev rules to skip DM flags decoding for removed devices.
- Remove device name prefix from dmsetup line output if -j & -m or -u supplied.
- Add new segtype 'raid' for MD RAID 1/4/5/6 support with dmeventd plugin.
- Add ability to reduce the number of mirrors in raid1 arrays to lvconvert.
- Add support for systemd file descriptor handover in dmeventd.
- Add systemd unit file to provide lvm2 monitoring.
- Add systemd unit files for dmeventd.
- Use new oom killer adjustment interface (oom_score_adj) when available.
- Fix read-only identical table reload supression.
- Remove --force option from lvrename manpage.

* Wed Aug 03 2011 Peter Rajnoha <prajnoha@redhat.com> - 2.02.86-5
- Change DEFAULT_UDEV_SYNC to 1 so udev_sync is used even without any config.

* Thu Jul 28 2011 Peter Rajnoha <prajnoha@redhat.com> - 2.02.86-4
- Add support for systemd file descriptor handover to dmeventd.
- Add support for new oom killer adjustment interface (oom_score_adj).

* Wed Jul 20 2011 Peter Rajnoha <prajnoha@redhat.com> - 2.02.86-3
- Fix broken lvm2-sysinit Requires: lvm2 dependency.

* Mon Jul 18 2011 Peter Rajnoha <prajnoha@redhat.com> - 2.02.86-2
- Add dm-event and lvm2-monitor unit files for use with systemd.
- Add sysvinit subpackage for legacy SysV init script support.

* Fri Jul 8 2011 Alasdair Kergon <agk@redhat.com> - 2.02.86-1
- Fix activation sequences to avoid trapped I/O with multiple LVs.
- Fix activation sequences to avoid allocating tables while devs suspended.
- Remove unnecessary warning in pvcreate for MD linear devices.
- Add activation/checks to lvm.conf to perform additional ioctl validation.
- Append 'm' attribute to pv_attr for missing PVs.
- Fix to preserve exclusive activation of mirror while up-converting.
- Reject allocation if number of extents is not divisible by area count.
- Fix cluster mirror creation to work with new mirror allocation algorithm.
- Ignore activation/verify_udev_operations if dm kernel driver vsn < 4.18.
- Add activation/verify_udev_operations to lvm.conf, disabled by default.
- Ignore inconsistent pre-commit metadata on MISSING_PV devs while activating.
- Add proper udev library context initialization and finalization to liblvm.
- Downgrade critical_section errors to debug level until it is moved to libdm.
- Fix ignored background polling default in vgchange -ay.
- Fix reduction of mirrors with striped segments to always align to stripe size.
- Validate mirror segments size.
- Fix extent rounding for striped volumes never to reduce more than requested.
- Fix create_temp_name to replace any '/' found in the hostname with '?'.
- Always use append to file in lvmdump. selinux policy may ban file truncation.
- Propagate test mode to clvmd to skip activation and changes to held locks.
- Permit --available with lvcreate so non-snapshot LVs need not be activated.
- Clarify error message when unable to convert an LV into a snapshot of an LV.
- Do not issue an error message when unable to remove .cache on read-only fs.
- Avoid memlock size mismatch by preallocating stdio line buffers.
- Report internal error if suspending a device using an already-suspended dev.
- Report internal error if any table is loaded while any dev is known suspended.
- Report error if a table load requiring target parameters has none supplied.
- Add dmsetup --checks and dm_task_enable_checks framework to validate ioctls.
- Add age_in_minutes parameter to dmsetup udevcomplete_all.
- Disable udev fallback by default and add --verifyudev option to dmsetup.
- Add dm_get_suspended_counter() for number of devs in suspended state by lib.
- Fix "all" report field prefix matching to include label fields with pv_all.
- Delay resuming new preloaded mirror devices with core logs in deptree code.

* Wed Jun 22 2011 Zdenek Kabelac <zkabelac@redhat.com> - 2.02.84-3
- Updated uname string test.

* Sat Jun 4 2011 Milan Broz <mbroz@redhat.com> - 2.02.84-2
- Accept kernel 3.0 uname string in libdevmapper initialization.
- Make systemd initscripts configurable.

* Wed Feb 9 2011 Alasdair Kergon <agk@redhat.com> - 2.02.84-1
- Fix big-endian CRC32 checksumming broken since 2.02.75.  If affected,
  ensure metadata backups in /etc/lvm/backup are up-to-date (vgcfgbackup)
  then after updating to 2.02.84 restore metadata from them (using pvcreate
  with -Zn --restorefile and -u if PVs can no longer be seen, then
  vgcfgrestore -f).
- Reinstate libdevmapper DEBUG_MEM support. (Removed in 1.02.62.)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.02.83-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb 4 2011 Alasdair Kergon <agk@redhat.com> - 2.02.83-1
- Allow exclusive activation of snapshots in a cluster.
- Don't lose LV exclusive lock state when suspending clustered devices.
- Fix fs operation stack handling when multiple operations on same device.
- Increase hash table sizes to 1024 LV names and 64 PV uuids.
- When setting up mda wipe first 4k of it as was intended.
- Remove unneeded checks for open_count in lv_info().
- Synchronize with udev before checking open_count in lv_info().
- Add "dmsetup ls --tree" output to lvmdump.
- Fix udev synchronization with no-locking --sysinit (2.02.80).
- Improve man page style consistency for pvcreate, pvremove, pvresize, pvscan.
- Avoid rebuilding of uuid validation table.
- Improve lvcreate error text from insufficient "extents" to "free space".
- Always use O_DIRECT when opening block devices to check for partitioning.
- Move creation of device nodes from 'create' to 'resume'.
- Add --addnodeonresume and --addnodeoncreate options to dmsetup.
- Add dm_task_set_add_node to libdevmapper to control dev node creation time.
- Add dm_task_secure_data to libdevmapper to wipe ioctl buffers in kernel.
- Log debug message when expected uevent is not generated.
- Set DM_UDEV_DISABLE_OTHER_RULES_FLAG for suspended DM devices in udev rules.
- Begin a new pool object for each row in _output_as_rows() correctly.

* Mon Jan 24 2011 Alasdair Kergon <agk@redhat.com> - 2.02.82-2
- Bring lvscan man page up-to-date.
- Fix lvchange --test to exit cleanly.
- Add change_tag to toollib.
- Allow multiple pvchange command line options to be specified together.
- Do not fail pvmove polling if another process cleaned up first.
- Avoid clvmd incrementing dlm lockspace reference count more than once.
- Add -f (don't fork) option to clvmd and fix clvmd -d<num> description.

* Mon Jan 17 2011 Alasdair Kergon <agk@redhat.com> - 2.02.81-1
- Add disk to allowed mirrored log type conversions.
- Accept fusion fio in device type filter.
- Speed up command processing by caching resolved config tree.
- Use same dm cookie for consecutive dm ops in same VG to reduce udev waits.
- Do not scan devices in dev_reset_error_count() when forking.
- Skip unnecessary LOCK_NULL unlock call during volume deactivation.
- Skip fs_unlock when calling exec_cmd within activation code (for modprobe).
- Replace fs_unlock by sync_local_dev_names to notify local clvmd. (2.02.80)
- Fix wrongly paired unlocking of VG_GLOBAL in pvchange. (2.02.66)
- Return 0 from cmirrord initscript 'start' if daemon is already running.
- Add DM_COOKIE_AUTO_CREATE to libdevmapper.h.
- Improve general lvconvert man page description.
- Detect NULL handle in get_property().
- Fix memory leak in persistent filter creation error path.
- Check for errors setting up dm_task struct in _setup_task().
- Fail polldaemon creation when lvmcache_init() fails.
- Return PERCENT_INVALID for errors in _copy_percent() and _snap_percent().
- Detect errors from dm_task_set calls in _get_device_info (dmeventd).
- Fix memory leak in debug mode of restart_clvmd() error path.
- Log error message for pthread_join() failure in clvmd.
- Use tmpfiles.d/lvm2.conf to create /var/lock/lvm and /var/run/lvm at boot.
- Require initscripts for tmpfiles.d/lvm2.conf.

* Tue Dec 21 2010 Alasdair Kergon <agk@redhat.com> - 2.02.79-1
- Create /var/run/lvm directory during clvmd initialisation if missing.
- Avoid revalidating the label cache immediately after scanning.
- Support scanning for a single VG in independent mdas.
- Don't skip full scan when independent mdas are present even if memlock is set.
- Add copy_percent and snap_percent to liblvm.
- Add new dm_prepare_selinux_context fn to libdevmapper and use it throughout.
- Enhance vg_validate to ensure integrity of LV and PV structs referenced.
- Enhance vg_validate to check composition of pvmove LVs.
- Avoid writing to freed memory in vg_release.  (2.02.78)
- Add missing test for reallocation error in _find_parallel_space().
- Add checks for allocation errors in config node cloning.
- Fix error path if regex engine cannot be created in _build_matcher().
- Check read() and close() results in _get_cmdline().
- Fix NULL pointer check in error path in clvmd do_command(). (2.02.78)
- Check for unlink failure in remove_lockfile() in dmeventd.
- Use dm_free for dm_malloc-ed areas in _clog_ctr/_clog_dtr in cmirrord.
- Change dm_regex_create() API to accept const char * const *patterns.

* Mon Dec 6 2010 Alasdair Kergon <agk@redhat.com> - 2.02.78-1
- Miscellaneous error path corrections and minor leaks fixed.
- Avoid misleading PV missing warnings in vgextend --restoremissing.
- Ignore unrecognised allocation policy found in metadata instead of aborting.
- Disallow lvconvert ops that both allocate & free supplied PEs in a single cmd.
- Fix liblvm seg_size to give bytes not sectors.
- Add functions to look up LV/PV by name/uuid to liblvm.
- Suppress 'No PV label' message when removing several PVs without mdas.
- Fix default /etc/lvm permissions to be 0755. (2.02.66)

* Mon Nov 22 2010 Alasdair Kergon <agk@redhat.com> - 2.02.77-1
- Add PV and LV segment types and functions to liblvm.
- Add set_property functions to liblvm.
- Remove tag length restriction and allow / = ! : # & characters.
- Support repetition of --addtag and --deltag arguments.
- Add infrastructure for specific cmdline arguments to be repeated in groups.
- Fix fsadm no longer to require '-f' to resize an unmounted filesystem.
- Fix fsadm to detect mounted filesystems on older systems. (2.0.75)
- Extend cling allocation policy to recognise PV tags (cling_by_tags).
- Add allocation/cling_tag_list to lvm.conf.

* Tue Nov 9 2010 Alasdair Kergon <agk@redhat.com> - 2.02.76-1
- Clarify error messages when activation fails due to activation filter use.
- Fix handling of online filesystem resize (using new fsadm return code).
- Modify fsadm to return different status code for check of mounted filesystem.
- Add DIAGNOSTICS section to fsadm man page.
- Update VG metadata only once in vgchange when making multiple changes.
- Allow independent vgchange arguments to be used together.
- Fix vgchange to process -a, --refresh, --monitor and --poll like lvchange.
- Add dmeventd -R to restart dmeventd without losing monitoring state. (1.02.56)
- Automatically unmount invalidated snapshots in dmeventd.
- Add lvm2app functions to query any pv, vg, or lv property / report field.
- Fix a deadlock caused by double close in clvmd.
- Fix NULL pointer dereference on too-large MDA error path in _vg_read_raw_area.
- Fix regex optimiser not to ignore RHS of OR nodes in _find_leftmost_common.
- Fix memory leak of field_id in _output_field function.
- Allocate buffer for reporting functions dynamically to support long outputs.

* Mon Oct 25 2010 Alasdair Kergon <agk@redhat.com> - 2.02.75-1
- Fix pthread mutex usage deadlock in clvmd.
- Avoid segfault by limiting partial mode for lvm1 metadata. (2.02.74)
- Skip dm devices in scan if they contain only error targets or are empty.
- Don't take write lock in vgchange --refresh, --poll or --monitor.
- Fix hang when repairing a mirrored-log that had both devs fail.
- Speed up unquoting of quoted double quotes and backslashes.
- Speed up CRC32 calculations by using a larger lookup table.
- Implement dmeventd -R to restart without state loss.
- Add --setuuid to dmsetup rename.
- Add global/metadata_read_only to use unrepaired metadata in read-only cmds.
- Automatically extend snapshots with dmeventd according to policy in lvm.conf.
- Add activation/snapshot_autoextend_threshold/percent to lvm.conf.
- Add devices/disable_after_error_count config to limit access to failing devs.
- Implement vgextend --restoremissing to reinstate missing devs that return.
- Read whole /proc/self/maps file before working with maps entries.
- Convey need for snapshot-merge target in lvconvert error message and man page.
- Give correct error message when creating a too-small snapshot.
- Make lvconvert respect --yes and --force when converting an inactive log.
- Better support of noninteractive shell execution of fsadm.
- Fix usage of --yes flag for ReiserFS resize in fsadm.
- Fix detection of mounted filesystems for fsadm when udev is used.
- Fix assignment of default value to LVM variable in fsadm.
- Fix support for --yes flag for fsadm.
- Do not execute lvresize from fsadm --dry-run.
- Fix fsadm return error code from user's break action.
- Return const pointer from dm_basename() in libdevmapper.
- Add dm_zalloc and use it and dm_pool_zalloc throughout.
- Add dm_task_set_newuuid to set uuid of mapped device post-creation.
- Fix missing variable initialization in cluster_send() function from cmirrord.
- Fix pointer for VG name in _pv_resize_single error code path.
- Fix vg_read memory leak with directory-based metadata.
- Fix memory leak of config_tree in reinitialization code path.
- Fix pool destruction order in dmeventd_lvm2_exit() to avoid leak debug mesg.
- Remove dependency on libm by replacing floor() by an integer-based algorithm.
- Refactor and add 'get' functions for pv, vg and lv properties/fields.
- Add pv_get_property and create generic internal _get_property function.
- Make generic GET_*_PROPERTY_FN macros with secondary macro for vg, pv & lv.

* Fri Oct 15 2010 Alasdair Kergon <agk@redhat.com> - 2.02.73-3
- Add --setuuid to dmsetup rename.
- Add dm_task_set_newuuid to set uuid of mapped device post-creation.

* Wed Sep 29 2010 jkeating - 2.02.74-2
- Rebuilt for gcc bug 634757

* Fri Sep 24 2010 Alasdair Kergon <agk@redhat.com> - 2.02.74-1
- Fix the way regions are marked complete to avoid slow --nosync cmirror I/O.
- Add DM_REPORT_FIELD_TYPE_ID_LEN to libdevmapper.h.
- Allow : and @ to be escaped with \ in device names of PVs.
- Avoid stack corruption when reading in large metadata.
- Fix partial mode operations for lvm1 metadata format.
- Track recursive filter iteration to avoid refreshing while in use. (2.02.56)
- Allocate buffer for metadata tags dynamically to remove 4k limit.
- Add random suffix to archive file names to prevent races when being created.
- Reinitialize archive and backup handling on toolcontext refresh.
- Make poll_mirror_progress report PROGRESS_CHECK_FAILED if LV is not a mirror.
- Like mirrors, don't scan origins if ignore_suspended_devices() is set.
- Automatically generate tailored LSB Requires-Start for clvmd init script.
- Fix return code of pvmove --abort PV.
- Fix pvmove --abort to remove even for empty pvmove LV.
- Add implementation for simple numeric 'get' property functions.
- Simplify MD/swap signature detection in pvcreate and allow aborting.
- Allow --yes to be used without --force mode.
- Fix file descriptor leak in swap signature detection error path.
- Detect and allow abort in pvcreate if LUKS signature is detected.

* Wed Aug 25 2010 Peter Rajnoha <prajnoha@redhat.com> - 2.02.73-2
- Add configure --with-default-data-alignment.
- Update heuristic used for default and detected data alignment.
- Add "devices/default_data_alignment" to lvm.conf.

* Wed Aug 18 2010 Alasdair Kergon <agk@redhat.com> - 2.02.73-1
- Change default alignment of data extents to 1MB.
- Add --norestorefile option to pvcreate.
- Require --restorefile when using pvcreate --uuid.
- Fix potential for corruption during cluster mirror device failure.
- Ignore snapshots when performing mirror recovery beneath an origin.
- Monitor origin -real device below snapshot instead of overlay device.
- Don't really change monitoring status when in test mode.
- Fix some exit statuses when starting/stopping monitoring fails.
- Enable snapshot monitoring by default when dmeventd is enabled.
- Fix 'lvconvert --splitmirrors' in cluster operation.
- Fix clvmd init script exit code to return 4 when executed as non-root user.
- Recognise and give preference to md device partitions (blkext major).
- Never scan internal LVM devices.
- Don't ignore user-specified PVs in split-mirror operations. (2.02.71)
- Fix data corruption bug in cluster mirrors.
- Require logical volume(s) to be explicitly named for lvconvert --merge.
- Avoid changing aligned pe_start as a side-effect of a log message.
- Use built-in rule for device aliases: block/ < dm- < disk/ < mapper/ < other.
- Handle failure of all mirrored log devices and all but one mirror leg. 
- Disallow 'mirrored' log type for cluster mirrors.
- Fix configure to supply DEFAULT_RUN_DIR to Makefiles.
- Fix allocation of wrong number of mirror logs with 'remove' fault policy.
- Add dmeventd/executable to lvm.conf to test alternative dmeventd.
- Fix udev rules to support udev database content generated by older rules.
- Reinstate detection of inappropriate uevent with DISK_RO set and suppress it.
- Fix regex ttree off-by-one error.
- Fix segfault in regex matcher with characters of ordinal value > 127.
- Wait for node creation before displaying debug info in dmsetup.
- Fix return status 0 for "dmsetup info -c -o help".

* Mon Aug 2 2010 Alasdair Kergon <agk@redhat.com> - 2.02.72-5
- Make udev configurable and merge with f12.

* Mon Aug 2 2010 Alasdair Kergon <agk@redhat.com> - 2.02.72-4
- Merge f13, f14 and rawhide spec files.

* Sat Jul 31 2010 Alasdair Kergon <agk@redhat.com> - 2.02.72-3
- Address lvm2-cluster security flaw CVE-2010-2526.
    https://bugzilla.redhat.com/CVE-2010-2526
- Change clvmd to communicate with lvm2 via a socket in /var/run/lvm.
- Return controlled error if clvmd is run by non-root user.
- Never use clvmd singlenode unless explicitly requested with -Isinglenode.
- Fix exported_symbols generation to use standard compiler arguments.
- Use #include <> not "" in lvm2app.h which gets installed on the system.
- Make liblvm.device-mapper wait for include file generation.
- Fix configure to supply DEFAULT_RUN_DIR to Makefiles.
- Fix wrong number of mirror log at allocate policy

* Wed Jul 28 2010 Alasdair Kergon <agk@redhat.com> - 2.02.71-1
- Make vgck warn about missing PVs.
- Revert failed table load preparation after "create, load and resume".
- Check if cluster log daemon is running before allowing cmirror create.
- Add dm_create_lockfile to libdm and use for pidfiles for all daemons.
- Correct LV list order used by lvconvert when splitting a mirror.
- Check if LV with specified name already exists when splitting a mirror.
- Fix suspend/resume logic for LVs resulting from splitting a mirror.
- Fix possible hang when all mirror images of a mirrored log fail.
- Adjust auto-metadata repair and caching logic to try to cope with empty mdas.
- Update pvcreate, {pv|vg}change, and lvm.conf man pages about metadataignore.
- Prompt if metadataignore with vgextend or pvchange would adjust vg_mda_copies.
- Adjust vg_mda_copies if metadataignore given with vgextend or pvchange.
- Speed up the regex matcher.
- Use "nowatch" udev rule for inappropriate devices.
- Document LVM fault handling in lvm_fault_handling.txt.
- Clarify help text for vg_mda_count.
- Add more verbose messages while checking volume_list and hosttags settings.
- Add log_error when strdup fails in {vg|lv}_change_tag().
- Do not log backtrace in valid _lv_resume() code path.

* Wed Jul 7 2010 Alasdair Kergon <agk@redhat.com> - 2.02.70-1
- Remove log directly if all mirror images of a mirrored log fail.
- Randomly select which mdas to use or ignore.
- Add printf format attributes to yes_no_prompt and fix a caller.
- Always pass unsuspended dm devices through persistent filter to other filters.
- Move test for suspended dm devices ahead of other filters.
- Fix another segfault in clvmd -R if no response from daemon received. (2.02.68)
- Remove superfluous suspended device counter from clvmd.
- Fix lvm shell crash when input is entirely whitespace.
- Update partial mode warning message.
- Preserve memlock balance in clvmd when activation triggers a resume.
- Restore the removemissing behaviour of lvconvert --repair --use-policies.

* Wed Jun 30 2010 Alasdair Kergon <agk@redhat.com> - 2.02.69-1
- Fix vgremove to allow removal of VG with missing PVs. (2.02.52)
- Add metadata/vgmetadatacopies to lvm.conf.
- Add --metadataignore to pvcreate and vgextend.
- Add vg_mda_copies, pv_mda_used_count and vg_mda_used_count to reports.
- Describe --vgmetadatacopies in lvm.conf and other man pages.
- Add --[vg]metadatacopies to select number of mdas to use in a VG.
- Make the metadata ignore bit control read/write metadata areas in a PV.
- Add pvchange --metadataignore to set or clear a metadata ignore bit.
- Refactor metadata code to prepare for --metadataignore / --vgmetadatacopies.
- Ensure region_size of mirrored log does not exceed its full size.
- Preload libc locale messages to prevent reading it in memory locked state.
- Fix handling of simultaneous mirror image and mirrored log image failure.

* Thu Jun 24 2010 Peter Rajnoha <prajnoha@redhat.com> - 2.02.68-2
- Fix udev rules to handle spurious events properly.
- Add Requires: udev >= 158-1 (needed for the change in udev rules).

* Wed Jun 23 2010 Alasdair Kergon <agk@redhat.com> - 2.02.68-1
- Have device-mapper-libs require device-mapper (circular) for udev rules.
- Clear exec_prefix.
- Use early udev synchronisation and update of dev nodes for clustered mirrors.
- Add lv_path to reports to offer full /dev pathname.
- Avoid abort when generating cmirror status.
- Fix clvmd initscript status to print only active clustered LVs.
- Fix segfault in clvmd -R if no response from daemon received.
- Honour log argument when down-converting stacked mirror.
- Sleep to workaround clvmd -S race: socket closed early and server drops cmd.
- Exit successfully when using -o help (but not -o +help) with LVM reports.
- Add man pages for lvmconf, dmeventd and non-existent lvmsadc and lvmsar tools.
- Add --force, --nofsck and --resizefs to lvresize/extend/reduce man pages.
- Fix lvm2cmd example in documentation.
- Fix typo in warning message about missing device with allocated data areas.
- Add device name and offset to raw_read_mda_header error messages.
- Allow use of lvm2app and lvm2cmd headers in C++ code.

* Fri Jun 4 2010 Alasdair Kergon <agk@redhat.com> - 2.02.67-1
- Require partial option in lvchange --refresh for partial LVs.
- Don't merge unchanged persistent cache file before dumping if tool scanned.
- Avoid selecting names under /dev/block if there is an alternative.
- Fix semctl parameter (union) to avoid misaligned parameter on some arches.
- Fix clvmd initscript restart command to start clvmd if not yet running.
- Handle failed restart of clvmd using -S switch properly.
- Use built-in absolute paths in clvmd (clvmd restart and PV and LV queries).
- Consistently return ECMD_FAILED if interrupted processing multiple LVs.
- Add --type parameter description to the lvcreate man page.
- Document 'clear' in dmsetup man page.
- Replace strncmp kernel version number checks with proper ones.
- Update clustered log kernel module name to log-userspace for 2.6.31 onwards.
- Support autoloading of dm-mod module for kernels from 2.6.35.
- Add dm_tree_node_set_presuspend_node() to presuspend child when deactivating.
- Do not fail lvm_init() if init_logging() or _init_rand() generates an errno.
- Fix incorrect memory pool deallocation while using vg_read for files.

* Thu May 20 2010 Alasdair Kergon <agk@redhat.com> - 2.02.66-2
- Simplify and fix Requires package headers.
- If unable to obtain snapshot percentage leave value blank on reports.
- Use new install_system_dirs and install_initscripts makefile targets.
- Add lvm2app functions to lookup a vgname from a pvid and pvname.
- Change internal processing of PVs in pvchange.
- Validate internal lock ordering of orphan and VG_GLOBAL locks.

* Mon May 17 2010 Alasdair Kergon <agk@redhat.com> - 2.02.65-1
- Disallow vgchange --clustered if there are active mirrors or snapshots.
- Fix truncated total size displayed by pvscan.
- Skip internal lvm devices in scan if ignore_suspended_devices is set.
- Do not merge old device cache after we run full scan. (2.02.56)
- Add new --sysinit compound option to vgchange and lvchange.
- Fix clvmd init script never to deactivate non-clustered volume groups.
- Drop duplicate errors for read failures and missing devices to verbose level.
- Do not print encryption key in message debug output (cryptsetup luksResume).
- Use -d to control level of messages sent to syslog by dmeventd.
- Change -d to -f to run dmeventd in foreground.
- Fix udev flags on remove in create_and_load error path.
- Add dm_list_splice() function to join two lists together.
- Use /bin/bash for scripts with bashisms.
- Switch Libs.private to Requires.private in devmapper.pc and lvm2app.pc.
- Use pkgconfig Requires.private for devmapper-event.pc.

* Fri Apr 30 2010 Alasdair Kergon <agk@redhat.com> - 2.02.64-1
- Avoid pointless initialisation when the 'version' command is run directly.
- Fix memory leak for invalid regex pattern input.
- Display invalid regex pattern for filter configuration in case of error.
- Fix -M and --type to use strings, not pointers that change on config refresh.
- Fix lvconvert error message when existing mirrored LV is not found.
- Set appropriate udev flags for reserved LVs.
- Disallow the direct removal of a merging snapshot.
- Don't preload the origin when removing a snapshot whose merge is pending.
- Disallow the addition of mirror images while a conversion is happening.
- Disallow primary mirror image removal when mirror is not in-sync.
- Remove obsolete --name parameter from vgcfgrestore.
- Add -S command to clvmd to restart the daemon preserving exclusive locks.
- Increment lvm2app version from 1 to 2 (memory allocation changes).
- Change lvm2app memory alloc/free for pv/vg/lv properties.
- Change daemon lock filename from lvm2_monitor to lvm2-monitor for consistency.
- Add support for new IMPORT{db} udev rule.
- Add DM_UDEV_PRIMARY_SOURCE_FLAG udev flag to recognize proper DM events.
- Also include udev libs in libdevmapper.pc.
- Cache bitset locations to speed up _calc_states.
- Add a regex optimisation pass for shared prefixes and suffixes.
- Add dm_bit_and and dm_bitset_equal to libdevmapper.
- Speed up dm_bit_get_next with ffs().

* Thu Apr 15 2010 Alasdair Kergon <agk@redhat.com> - 2.02.63-2
- Remove 'lvmconf --lockinglibdir' from cluster post: locking is now built-in.
- Move libdevmapper-event-lvm2.so to devel package.
- Explicitly specify libdevmapper-event.so* attributes.
- Drop support for upgrades from very old versions that used lvm not lvm2.
- Move libdevmapper-event plug-in libraries into new device-mapper subdirectory.
- Don't verify lvm.conf contents when using rpm --verify.

* Wed Apr 14 2010 Alasdair Kergon <agk@redhat.com> - 2.02.63-1
- Move development links to shared objects to /usr (hard-coded temporarily).
- Change libdevmapper deactivation to fail if device is open.
- Wipe memory buffers for libdevmapper dm-ioctl parameters before releasing.
- Strictly require libudev if udev_sync is used.
- Add support for ioctl's DM_UEVENT_GENERATED_FLAG.
- Allow incomplete mirror restore in lvconvert --repair upon insufficient space.
- Do not reset position in metadata ring buffer on vgrename and vgcfgrestore.
- Allow VGs with active LVs to be renamed.
- Only pass visible LVs to tools in cmdline VG name/tag expansions without -a.
- Use C locale and mlockall in clvmd and dmeventd.
- Mask LCK_HOLD in cluster VG locks for upgrade compatibility with older clvmd.
- Add activation/polling_interval to lvm.conf as --interval default.
- Don't ignore error if resuming any LV fails when resuming groups of LVs.
- Skip closing persistent filter cache file if open failed.
- Permit mimage LVs to be striped in lvcreate, lvresize and lvconvert.
- Fix pvmove allocation to take existing parallel stripes into account.
- Fix incorrect removal of symlinks after LV deactivation fails.
- Fix is_partitioned_dev not to attempt to reopen device.
- Fix another thread race in clvmd.
- Improve vg_validate to detect some loops in lists.
- Change most remaining log_error WARNING messages to log_warn.
- Always use blocking lock for VGs and orphan locks.
- Allocate all memory for segments from private VG mempool.
- Optimise searching PV segments for seeking the most recently-added.
- Remove duplicated vg_validate checks when parsing cached metadata.
- Use hash table of LVs to speed up parsing of text metadata with many LVs.
- Fix two vg_validate messages, adding whitespace and parentheses.
- When dmeventd is not forking because of -d flag, don't kill parent process.
- Fix dso resource leak in error path of dmeventd.
- Fix --alloc contiguous policy only to allocate one set of parallel areas.
- Do not allow {vg|lv}change --ignoremonitoring if on clustered VG.
- Add ability to create mirrored logs for mirror LVs.
- Fix clvmd cluster propagation of dmeventd monitoring mode.
- Allow ALLOC_ANYWHERE to split contiguous areas.
- Add some assertions to allocation code.
- Introduce pv_area_used into allocation algorithm and add debug messages.
- Add activation/monitoring to lvm.conf.
- Add --monitor and --ignoremonitoring to lvcreate.
- Don't allow resizing of internal logical volumes.
- Fix libdevmapper-event pkgconfig version string to match libdevmapper.
- Avoid scanning all pvs in the system if operating on a device with mdas.
- Disable long living process flag in lvm2app library.
- Fix pvcreate device md filter check.
- Suppress repeated errors about the same missing PV uuids.
- Bypass full device scans when using internally-cached VG metadata.
- Only do one full device scan during each read of text format metadata.
- Look up missing PVs by uuid not dev_name in pvs to avoid invalid stat.

* Tue Mar 09 2010 Alasdair Kergon <agk@redhat.com> - 2.02.62-1
- Rewrite clvmd init script.
- Add default alternative to mlockall using mlock to reduce pinned memory size.
- Add use_mlockall and mlock_filter to activation section of lvm.conf.
- Handle misaligned devices that report alignment_offset of -1.
- Extend core allocation code in preparation for mirrored log areas.
- No longer fall back to looking up active devices by name if uuid not found.
- Don't touch /dev in vgmknodes if activation is disabled.
- Add --showkeys parameter description to dmsetup man page.
- Add --help option as synonym for help command.
- Add lvm2app functions lvm_{vg|lv}_{get|add|remove}_tag() functions.
- Refactor snapshot-merge deptree and device removal to support info-by-uuid.

* Fri Mar 05 2010 Peter Rajnoha <prajnoha@redhat.com> - 2.02.61-2
- Change spec file to support excluding cluster components from the build.

* Tue Feb 16 2010 Alasdair Kergon <agk@redhat.com> - 2.02.61-1
- Add %%ORIGIN support to lv{create,extend,reduce,resize} --extents.
- Accept a list of LVs with 'lvconvert --merge @tag' using process_each_lv.
- Remove false "failed to find tree node" error when activating merging origin.
- Exit with success when lvconvert --repair --use-policies performs no action.
- Avoid unnecessary second resync when adding mimage to core-logged mirror.
- Make clvmd -V return status zero.
- Fix cmirrord segfault in clog_cpg list processing when converting mirror log.
- Deactivate temporary pvmove mirror cluster-wide when activating it fails.
- Add missing metadata vg_reverts in pvmove error paths.
- Unlock shared lock in clvmd if activation calls fail.
- Add lvm_pv_get_size, lvm_pv_get_free and lvm_pv_get_dev_size to lvm2app.
- Change lvm2app to return all sizes in bytes as documented (not sectors).
- Exclude internal VG names and uuids from lists returned through lvm2app.
- Add LVM_SUPPRESS_LOCKING_FAILURE_MESSAGES environment variable.
- Add DM_UDEV_DISABLE_LIBRARY_FALLBACK udev flag to rely on udev only.
- Remove hard-coding that skipped _mimage devices from 11-dm-lvm.rules.
- Export dm_udev_create_cookie function to create new cookies on demand.
- Add --udevcookie, udevcreatecookie and udevreleasecookie to dmsetup.
- Set udev state automatically instead of using DM_UDEV_DISABLE_CHECKING.
- Set udev state automatically instead of using LVM_UDEV_DISABLE_CHECKING.
- Remove pointless versioned symlinks to dmeventd plugin libraries.

* Fri Jan 29 2010 Alasdair Kergon <agk@redhat.com> - 2.02.60-5
- Replace spaces with tabs in a couple of places in spec file.

* Sat Jan 23 2010 Alasdair Kergon <agk@redhat.com> - 2.02.60-4
- Extend cmirrord man page.
- Sleep before first progress check iff pvmove/lvconvert interval has prefix '+'.
- Fix cmirror initscript syntax problems.
- Fix first syslog message prefix for dmeventd plugins.
- Make failed locking initialisation messages more descriptive.

* Fri Jan 22 2010 Alasdair Kergon <agk@redhat.com> - 2.02.59-3
- Fix dmeventd lvm2 wrapper (plug-ins unusable in last build).
- Make failed locking initialisation messages more descriptive.

* Fri Jan 22 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 2.02.59-2
- Drop duplicated BuildRequires on openaislib-devel.
- Drop Requires on clusterlib for cmirror subpackage.
- clvmd subpackage should Requires cman (#506592).

* Fri Jan 22 2010 Alasdair Kergon <agk@redhat.com> - 2.02.59-1
- Add cmirror subpackage for clustered mirrors.
- Set 'preferred_names' in default lvm.conf.
- Add libdevmapper-event-lvm2.so to serialise dmeventd plugin liblvm2cmd use.
- Stop dmeventd trying to access already-removed snapshots.
- Fix clvmd to never scan suspended devices.
- Fix detection of completed snapshot merge.
- Improve snapshot merge metadata import validation.

* Thu Jan 14 2010 Alasdair Kergon <agk@redhat.com> - 2.02.58-1
- Fix clvmd automatic target module loading crash.
- Fix allocation code not to stop at the first area of a PV that fits.
- Add support for the "snapshot-merge" kernel target (2.6.33-rc1).
- Add --merge to lvconvert to merge a snapshot into its origin.

* Tue Jan 12 2010 Alasdair Kergon <agk@redhat.com> - 2.02.57-1
- Add --splitmirrors to lvconvert to split off part of a mirror.
- Allow vgremove to remove a VG with PVs missing after a prompt.
- Add activation/udev_rules config option in lvm.conf.
- Add --poll flag to vgchange and lvchange to control background daemon launch.
- Impose limit of 8 mirror images to match the in-kernel kcopyd restriction.
- Log failure type and recognise type 'F' (flush) in dmeventd mirror plugin.
- Add --noudevrules option for dmsetup to disable /dev node management by udev.
- Fix 'dmsetup info -c -o all' to show all fields.
- Fix coredump and memory leak for 'dmsetup help -c'.
- Rename mirror_device_fault_policy to mirror_image_fault policy.
- Use extended status of new kernel snapshot target 1.8.0 to detect when empty.
- Allow use of precommitted metadata when a PV is missing.
- Add global/abort_on_internal_errors to lvm.conf to assist testing.
- If aborting due to internal error, always send that message to stderr.
- Keep log type consistent when changing mirror image count.
- Exit with success in lvconvert --repair --use-policies on failed allocation.
- Ensure any background daemon exits without duplicating parent's functionality.
- Change background daemon process names to "(lvm2)".
- Fix internal lock state after forking.
- Remove empty PV devices if lvconvert --repair is using defined policies.
- Use fixed buffer to prevent stack overflow in persistent filter dump.
- Propagate metadata commit and revert notifications to other cluster nodes.
- Fix metadata caching and lock state propagation to remote nodes in clvmd.
- Properly decode all flags in clvmd messages including VG locks.
- Drop cached metadata after device was auto-repaired and removed from VG.
- Clear MISSING_PV flag if PV reappeared and is empty.
- Fix removal of multiple devices from a mirror.
- Also clean up PVs flagged as missing in vgreduce --removemissing --force.
- Fix some pvresize and toollib error paths with missing VG releases/unlocks.
- Explicitly call suspend for temporary mirror layer.
- Add memlock information to do_lock_lv debug output.
- Always bypass calls to remote cluster nodes for non-clustered VGs.
- Permit implicit cluster lock conversion in pre/post callbacks on local node.
- Permit implicit cluster lock conversion to the lock mode already held.
- Fix lock flag masking in clvmd so intended code paths get invoked.
- Remove newly-created mirror log from metadata if initial deactivation fails.
- Improve pvmove error message when all source LVs are skipped.
- Fix memlock imbalance in lv_suspend if already suspended.
- Fix pvmove test mode not to poll (and fail).
- Fix vgcreate error message if VG already exists.
- Fix tools to use log_error when aborted due to user response to prompt.
- Fix ignored readahead setting in lvcreate --readahead.
- Fix clvmd memory leak in lv_info_by_lvid by calling release_vg.
- If LVM_UDEV_DISABLE_CHECKING is set in environment, disable udev warnings.
- If DM_UDEV_DISABLE_CHECKING is set in environment, disable udev warnings.
- Always set environment variables for an LVM2 device in 11-dm-lvm.rules.
- Disable udev rules for change events with DISK_RO set.
- Add dm_tree_add_dev_with_udev_flags to provide wider support for udev flags.
- Correct activated or deactivated text in vgchange summary message.
- Fix fsadm man page typo (fsdam).

* Tue Nov 24 2009 Alasdair Kergon <agk@redhat.com> - 2.02.56-2
- Revert vg_read_internal change as clvmd was not ready for vg_read. (2.02.55)
- Fix unbalanced memory locking when deactivating LVs.
- Add missing vg_release to pvs and pvdisplay to fix memory leak.
- Do not try to unlock VG which is not locked when processing a VG.
- Update .cache file after every full device rescan in clvmd.
- Refresh all device filters (including sysfs) before each full device rescan.
- Return error status if vgchange fails to activate any volume.

* Thu Nov 19 2009 Alasdair Kergon <agk@redhat.com> - 2.02.55-1
- Fix deadlock when changing mirrors due to unpaired memlock refcount changes.
- Fix pvmove region_size overflow for very large PVs.
- Fix lvcreate and lvresize %%PVS argument always to use sensible total size.
- Directly restrict vgchange to activating visible LVs.
- Fix hash lookup segfault when keys compared are different lengths.
- Flush stdout after yes/no prompt.
- Recognise DRBD devices and handle them like md devices.
- Add dmsetup --inactive support (requires kernel support targetted for 2.6.33).

* Fri Nov 13 2009 Peter Rajnoha <prajnoha@redhat.com> - 2.02.54-3
- Support udev flags even when udev_sync is disabled.
- Remove last_rule from udev_rules.
- Udev rules cleanup.

* Tue Nov 3 2009 Peter Rajnoha <prajnoha@redhat.com> - 2.02.54-2
- Enable udev synchronisation code.
- Install default udev rules for device-mapper and LVM2.
- Add BuildRequires: libudev-devel.
- Add Requires: libudev (to check udev is running).
- Add Requires: util-linux-ng (blkid used in udev rules).
- Add Conflicts: dracut < 002-18 (for dracut to install required udev rules)

* Tue Oct 27 2009 Alasdair Kergon <agk@redhat.com> - 2.02.54-1
- Add implict pvcreate support to vgcreate and vgextend.
- Add --pvmetadatacopies for pvcreate, vgcreate, vgextend, vgconvert.
- Distinguish between powers of 1000 and powers of 1024 in unit suffixes.
- Restart lvconverts in vgchange.
- Don't attempt to deactivate an LV if any of its snapshots are in use.
- Return error if lv_deactivate fails to remove device from kernel.
- Treat input units of both 's' and 'S' as 512-byte sectors.  (2.02.49)
- Use standard output units for 'PE Size' and 'Stripe size' in pv/lvdisplay.
- Add global/si_unit_consistency to enable cleaned-up use of units in output.
- Only do lock conversions in clvmd if we are explicitly asked for one.
- Fix clvmd segfault when refresh_toolcontext fails.
- Cleanup mimagetmp LV if allocation fails for new lvconvert mimage.
- Handle metadata with unknown segment types more gracefully.
- Make clvmd return 0 on success rather than 1.
- Correct example.conf to indicate that lvm2 not lvm1 is the default format.
- Delay announcing mirror monitoring to syslog until initialisation succeeded.
- Update lvcreate/lvconvert man pages to explain PhysicalVolume parameter.
- Document --all option in man pages and cleanup {pv|vg|lv}{s|display} pages.

* Mon Oct 19 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 2.02.53-3
- Enable openais support in clvmd.

* Fri Sep 25 2009 Alasdair Kergon <agk@redhat.com> - 2.02.53-2
- Reissued tarball to fix compilation warning from lvm2_log_fn prototype.

* Fri Sep 25 2009 Alasdair Kergon <agk@redhat.com> - 2.02.53-1
- Create any directories in /dev with umask 022. (#507397)
- Handle paths supplied to dm_task_set_name by getting name from /dev/mapper.
- Add splitname and --yes to dmsetup man page.

* Thu Sep 24 2009 Peter Rajnoha <prajnoha@redhat.com> - 2.02.52-4
- Disable udev synchronisation code (revert previous build).

* Mon Sep 21 2009 Peter Rajnoha <prajnoha@redhat.com> - 2.02.52-3
- Enable udev synchronisation code.
- Install default udev rules for device-mapper and LVM2.
- Add BuildRequires: libudev-devel.
- Add Requires: libudev (to check udev is running).
- Add Requires: util-linux-ng (blkid used in udev rules).

* Wed Sep 16 2009 Alasdair Kergon <agk@redhat.com> - 2.02.52-2
- Build dmeventd and place into a separate set of subpackages.
- Remove no-longer-needed BuildRoot tag and buildroot emptying at install.

* Tue Sep 15 2009 Alasdair Kergon <agk@redhat.com> - 2.02.52-1
- Prioritise write locks over read locks by default for file locking.
- Add local lock files with suffix ':aux' to serialise locking requests.
- Fix readonly locking to permit writeable global locks (for vgscan). (2.02.49)
- Make readonly locking available as locking type 4.
- Fix global locking in PV reporting commands (2.02.49).
- Make lvchange --refresh only take a read lock on volume group.
- Fix race where non-blocking file locks could be granted in error.
- Fix pvcreate string termination in duplicate uuid warning message.
- Don't loop reading sysfs with pvcreate on a non-blkext partition (2.02.51).
- Fix vgcfgrestore error paths when locking fails (2.02.49).
- Make clvmd check corosync to see what cluster interface it should use.
- Fix vgextend error path - if ORPHAN lock fails, unlock / release vg (2.02.49).
- Clarify use of PE ranges in lv{convert|create|extend|resize} man pages.
- Restore umask when device node creation fails.
- Check kernel vsn to use 'block_on_error' or 'handle_errors' in mirror table.

* Mon Aug 24 2009 Milan Broz <mbroz@redhat.com> - 2.02.51-3
- Fix global locking in PV reporting commands (2.02.49).
- Fix pvcreate on a partition (2.02.51).
- Build clvmd with both cman and corosync support.

* Thu Aug 6 2009 Alasdair Kergon <agk@redhat.com> - 2.02.51-2
- Fix clvmd locking broken in 2.02.50-1.
- Only change LV /dev symlinks on ACTIVATE not PRELOAD (so not done twice).
- Make lvconvert honour log mirror options combined with downconversion.
- Add devices/data_alignment_detection to lvm.conf.
- Add devices/data_alignment_offset_detection to lvm.conf.
- Add --dataalignmentoffset to pvcreate to shift start of aligned data area.
- Update synopsis in lvconvert manpage to mention --repair.
- Document -I option of clvmd in the man page.

* Thu Jul 30 2009 Alasdair Kergon <agk@redhat.com> - 2.02.50-2
- lvm2-devel requires device-mapper-devel.
- Fix lvm2app.pc filename.

* Tue Jul 28 2009 Alasdair Kergon <agk@redhat.com> - 2.02.50-1
- Add libs and devel subpackages to include shared libraries for applications.
  N.B. The liblvm2app API is not frozen yet and may still be changed
  Send any feedback to the mailing list lvm-devel@redhat.com.
- Remove obsolete --with-dmdir from configure.
- Add global/wait_for_locks to lvm.conf so blocking for locks can be disabled.
- Fix race condition with vgcreate and vgextend on same device since 2.02.49.
- Add an API version number, LVM_LIBAPI, to the VERSION string.
- Return EINVALID_CMD_LINE not success when invalid VG name format is used.
- Remove unnecessary messages after vgcreate/vgsplit code change in 2.02.49.
- Store any errno and error messages issued while processing each command.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.02.49-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 15 2009 Alasdair Kergon <agk@redhat.com> - 2.02.49-1
- Exclude VG_GLOBAL from vg_write_lock_held so scans open devs read-only again.
- Fix dev name mismatch in vgcreate man page example.
- Check md devices for a partition table during device scan.
- Add extended device (blkext) and md partition (mdp) types to filters.
- Make text metadata read errors for segment areas more precise.
- Fix text segment metadata read errors to mention correct segment name.
- Include segment and LV names in text segment import error messages.
- Fix memory leak in vgsplit when re-reading the vg.
- Permit several segment types to be registered by a single shared object.
- Update the man pages to document size units uniformly.
- Allow commandline sizes to be specified in terms of bytes and sectors.
- Update 'md_chunk_alignment' to use stripe-width to align PV data area.
- Fix segfault in vg_release when vg->cmd is NULL.
- Add dm_log_with_errno and dm_log_with_errno_init, deprecating the old fns.
- Fix whitespace in linear target line to fix identical table line detection.
- Add device number to more log messages during activation.

* Fri Jul 10 2009 Fabio M. Di Nitto <fdinitto@redhat.com> 2.02.48-2
- BuildRequires and Requires on stable versions of both corosync-lib (1.0.0-1)
  and cluster-lib (3.0.0-20).

* Tue Jun 30 2009 Alasdair Kergon <agk@redhat.com> - 2.02.48-1
- Abort if automatic metadata correction fails when reading VG to update it.
- Don't fallback to default major number in libdm: use dm_task_set_major_minor.
- Explicitly request fallback to default major number in device mapper.
- Ignore suspended devices during repair.
- Suggest using lvchange --resync when adding leg to not-yet-synced mirror.
- Destroy toolcontext on clvmd exit to avoid memory pool leaks.
- Fix lvconvert not to poll mirror if no conversion in progress.
- Fix memory leaks in toolcontext error path.
- Reinstate partial activation support in clustered mode.
- Allow metadata correction even when PVs are missing.
- Use 'lvm lvresize' instead of 'lvresize' in fsadm.
- Do not use '-n' realine option in fsadm for rescue disk compatiblity.
- Round up requested readahead to at least one page and print warning.
- Try to repair vg before actual vgremove when force flag provided.
- Unify error messages when processing inconsistent volume group.
- Introduce lvconvert --use_policies (repair policy according to lvm.conf).
- Fix rename of active snapshot with virtual origin.
- Fix convert polling to ignore LV with different UUID.
- Cache underlying device readahead only before activation calls.
- Fix segfault when calculating readahead on missing device in vgreduce.
- Remove verbose 'visited' messages.
- Handle multi-extent mirror log allocation when smallest PV has only 1 extent.
- Add LSB standard headers and functions (incl. reload) to clvmd initscript.
- When creating new LV, double-check that name is not already in use.
- Remove /dev/vgname/lvname symlink automatically if LV is no longer visible.
- Rename internal vorigin LV to match visible LV.
- Suppress 'removed' messages displayed when internal LVs are removed.
- Fix lvchange -a and -p for sparse LVs.
- Fix lvcreate --virtualsize to activate the new device immediately.
- Make --snapshot optional with lvcreate --virtualsize.
- Generalise --virtualoriginsize to --virtualsize.
- Skip virtual origins in process_each_lv_in_vg() without --all.
- Fix counting of virtual origin LVs in vg_validate.
- Attempt to load dm-zero module if zero target needed but not present.
- Add crypt target handling to libdevmapper tree nodes.
- Add splitname command to dmsetup.
- Add subsystem, vg_name, lv_name, lv_layer fields to dmsetup reports.
- Make mempool optional in dm_split_lvm_name() in libdevmapper.

* Wed Jun 10 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 2.02.47-2
- BuildRequire newer version of corosynclib (0.97-1) to link against
  latest libraries version (soname 4.0.0).
- Add lvm2-2_02_48-cluster-cpg-new-api.patch to port clvmd-corosync
  to new corosync cpg API.

* Fri May 22 2009 Alasdair Kergon <agk@redhat.com> - 2.02.47-1
- Inherit readahead setting from underlying devices during activation.
- Detect LVs active on remote nodes by querying locks if supported.
- Enable online resizing of mirrors.
- Use suspend with flush when device size was changed during table preload.
- Implement query_resource_fn for cluster_locking.
- Support query_resource_fn in locking modules.
- Fix pvmove to revert operation if temporary mirror creation fails.
- Fix metadata export for VG with missing PVs.
- Add vgimportclone and install it and the man page by default.
- Force max_lv restriction only for newly created LV.
- Do not query nonexistent devices for readahead.
- Reject missing PVs from allocation in toollib.
- Fix PV datalignment for values starting prior to MDA area. (2.02.45)
- Add sparse devices: lvcreate -s --virtualoriginsize (hidden zero origin).
- Fix minimum width of devices column in reports.
- Add lvs origin_size field.
- Implement lvconvert --repair for repairing partially-failed mirrors.
- Fix vgreduce --removemissing failure exit code.
- Fix remote metadata backup for clvmd.
- Fix metadata backup to run after vg_commit always.
- Fix pvs report for orphan PVs when segment attributes are requested.
- Fix pvs -a output to not read volume groups from non-PV devices.
- Introduce memory pools per volume group (to reduce memory for large VGs).
- Always return exit error status when locking of volume group fails.
- Fix mirror log convert validation question.
- Enable use of cached metadata for pvs and pvdisplay commands.
- Fix memory leak in mirror allocation code.
- Save and restore the previous logging level when log level is changed.
- Fix error message when archive initialization fails.
- Make sure clvmd-corosync releases the lockspace when it exits.
- Fix segfault for vgcfgrestore on VG with missing PVs.
- Block SIGTERM & SIGINT in clvmd subthreads.
- Detect and conditionally wipe swapspace signatures in pvcreate.
- Fix maximal volume count check for snapshots if max_lv set for volume group.
- Fix lvcreate to remove unused cow volume if the snapshot creation fails.
- Fix error messages when PV uuid or pe_start reading fails.
- Flush memory pool and fix locking in clvmd refresh and backup command.
- Fix unlocks in clvmd-corosync. (2.02.45)
- Fix error message when adding metadata directory to internal list fails.
- Fix size and error message of memory allocation at backup initialization.
- Remove old metadata backup file after renaming VG.
- Restore log_suppress state when metadata backup file is up-to-date.
- Export dm_tree_node_size_changed() from libdevmapper.
- Fix segfault when getopt processes dmsetup -U, -G and -M options.
- Add _smp_mflags to compilation and remove DESTDIR.

* Fri Apr 17 2009 Milan Broz <mbroz@redhat.com> - 2.02.45-4
- Add MMC (mmcblk) device type to filters. (483686)

* Mon Mar 30 2009 Jussi Lehtola <jussi.lehtola@iki.fi> 2.02.45-3
- Add FTP server location to Source0.

* Mon Mar 30 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 2.02.45-2
- BuildRequires a newer version of corosync (0.95-2) to fix linking.

* Tue Mar 3 2009 Alasdair Kergon <agk@redhat.com> - 2.02.45-1
- Update clusterlib and corosync dependencies.
- Attempt proper clean up in child before executing fsadm or modprobe.
- Do not scan devices if reporting only attributes from PV label.
- Use pkgconfig to obtain corosync library details during configuration.
- Fix error returns in clvmd-corosync interface to DLM.
- Add --refresh to vgchange and vgmknodes man pages.
- Pass --test from lvresize to fsadm as --dry-run.
- Prevent fsadm from checking mounted filesystems.
- No longer treats any other key as 'no' when prompting in fsadm.
- Add --dataalignment to pvcreate to specify alignment of data area.
- Fix unblocking of interrupts after several commands.
- Provide da and mda locations in debug message when writing text format label.
- Mention the restriction on file descriptors at invocation on the lvm man page.
- Index cached vgmetadata by vgid not vgname to cope with duplicate vgnames.
- No longer require kernel and metadata major numbers to match.
- If kernel supports only one dm major number, use in place of any supplied.
- Add option to /etc/sysconfig/cluster to select cluster type for clvmd.
- Allow clvmd to start up if its lockspace already exists.
- Separate PV label attributes which do not need parse metadata when reporting.
- Remove external dependency on the 'cut' command from fsadm.
- Fix pvs segfault when pv mda attributes requested for unavailable PV.
- Add fsadm support for reszing ext4 filesysystems.
- Change lvm2-cluster to corosync instead of cman.
- Fix some old changelog typos in email addresses.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.02.44-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan 27 2009 Alasdair Kergon <agk@redhat.com> - 2.02.44-1
- Add --nameprefixes, --unquoted, --rows to pvs, vgs, lvs man pages.
- Fix lvresize size conversion for fsadm when block size is not 1K.
- Fix pvs segfault when run with orphan PV and some VG fields.
- Display a 'dev_size' of zero for missing devices in reports.
- Add pv_mda_size to pvs and vg_mda_size to vgs.
- Fix lvmdump /sys listing to include virtual devices directory.
- Add "--refresh" functionality to vgchange and vgmknodes.
- Avoid exceeding LV size when wiping device.
- Calculate mirror log size instead of using 1 extent.
- Ensure requested device number is available before activating with it.
- Fix incorrect exit status from 'help <command>'.
- Fix vgrename using UUID if there are VGs with identical names.
- Fix segfault when invalid field given in reporting commands.
- Use better random seed value in temp file creation.
- Add read_urandom to read /dev/urandom. Use in uuid calculation.
- Fix race in vgcreate that would result in second caller overwriting first.
- Fix uninitialised lv_count in vgdisplay -c.
- Don't skip updating pvid hash when lvmcache_info struct got swapped.
- Fix startup race in clvmd.
- Cope with snapshot dependencies when removing a whole VG with lvremove.
- Make man pages and tool help text consistent using | for alternative options.
- Add "all" field to reports expanding to all fields of report type.
- Enforce device name length and character limitations in libdm.

* Mon Nov 10 2008 Alasdair Kergon <agk@redhat.com> - 2.02.43-1
- Upstream merge of device-mapper and lvm2 source.
- Correct prototype for --permission on lvchange and lvcreate man pages.
- Exit with non-zero status from vgdisplay if couldn't show any requested VG.
- libdevmapper.pc: Use simplified x.y.z version number.
- Accept locking fallback_to_* options in the global section as documented.
- Several fixes to lvconvert involving mirrors.
- Avoid overwriting in-use on-disk text metadata when metadataarea fills up.
- Generate man pages from templates and include version.
- Fix misleading error message when there are no allocatable extents in VG.
- Fix handling of PVs which reappeared with old metadata version.
- Fix validation of --minor and --major in lvcreate to require -My always.
- Allow lvremove to remove LVs from VGs with missing PVs.
- In VG with PVs missing, by default allow activation of LVs that are complete.
- Require --force with --removemissing in vgreduce to remove partial LVs.
- No longer write out PARTIAL flag into metadata backups.
- Treat new default activation/missing_stripe_filler "error" as an error target.
- Add devices/md_chunk_alignment to lvm.conf.
- Pass struct physical_volume to pe_align and adjust for md chunk size.
- Avoid shuffling remaining mirror images when removing one, retaining primary.
- Prevent resizing an LV while lvconvert is using it.
- Avoid repeatedly wiping cache while VG_GLOBAL is held in vgscan & pvscan.
- Fix pvresize to not allow resize if PV has two metadata areas.
- Fix setting of volume limit count if converting to lvm1 format.
- Fix vgconvert logical volume id metadata validation.
- Fix lvmdump metadata gather option (-m) to work correctly.
- Fix allocation bug in text metadata format write error path.
- Fix vgcfgbackup to properly check filename if template is used.
- vgremove tries to remove lv snapshot first.
- Improve file descriptor leak detection to display likely culprit and filename.
- Avoid looping forever in _pv_analyze_mda_raw used by pvck.
- Change lvchange exit status to indicate if any part of the operation failed.
- Fix pvchange and pvremove to handle PVs without mdas.
- Fix pvchange -M1 -u to preserve existing extent locations when there's a VG.
- Cease recognising snapshot-in-use percentages returned by early devt kernels.
- Add backward-compatible flags field to on-disk format_text metadata.
- libdevmapper: Only resume devices in dm_tree_preload_children if size changes.
- libdevmapper: Extend deptree buffers so the largest possible device numbers fit.
- libdevmapper: Underline longer report help text headings.

* Tue Oct 7 2008 Alasdair Kergon <agk@redhat.com> - 2.02.39-6
- Only set exec_prefix once and configure explicit directories to work with
  new version of rpm.

* Fri Sep 26 2008 Fabio M. Di Nitto <fdinitto@redhat.cm> - 2.02.39-5
- Add BuildRequires on cmanlib-devel. This is required after libcman split
  from cman and cman-devel into cmanlib and cmanlib-devel.
- Make versioned BuildRequires on cman-devel and cmanlib-devel more strict
  to guarantee to get the right version.

* Thu Sep 25 2008 Fabio M. Di Nitto <fdinitto@redhat.cm> - 2.02.39-5
- Add versioned BuildRequires on new cman-devel.

* Sun Sep 21 2008 Ville Skyttä <ville.skytta at iki.fi> - 2.02.39-5
- Change %%patch to %%patch0 to match Patch0 as required by RPM package update.

* Thu Aug  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.02.39-4
- Fix license tag.

* Fri Jun 27 2008 Alasdair Kergon <agk@redhat.com> - 2.02.39-3
- Fix up cache for PVs without mdas after consistent VG metadata is processed.
- Update validation of safe mirror log type conversions in lvconvert.
- Fix lvconvert to disallow snapshot and mirror combinations.
- Fix reporting of LV fields alongside unallocated PV segments.
- Add --unquoted and --rows to reporting tools.
- Avoid undefined status code after _memlock commands in lvm shell.
- Fix and improve readahead 'auto' calculation for stripe_size.
- Fix lvchange output for -r auto setting if auto is already set.
- Fix add_mirror_images not to dereference uninitialized log_lv upon failure.
- Add --force to lvextend and lvresize.
- Fix vgchange to not activate component mirror volumes directly.

* Wed Jun 25 2008 Alasdair Kergon <agk@redhat.com> - 2.02.38-2
- dmsetup: Add --unquoted and --rows to 'info -c' command.
- libdevmapper: Fix inverted no_flush debug message.

* Fri Jun 13 2008 Alasdair Kergon <agk@redhat.com> - 2.02.38-1
- libdevmapper: Make dm_hash_iter safe against deletion.
- libdevmapper: Accept a NULL pointer to dm_free silently.
- libdevmapper: Calculate string size within dm_pool_grow_object.
- libdevmapper: Send reporting field help text to stderr not stdout.

- dmsetup: Add tables_loaded, readonly and suspended columns to reports.
- dmsetup: Add --nameprefixes for new report output format FIELD=VALUE.

- Add --nameprefixes to reporting tools for field name prefix output format.
- Fix return values for reporting commands when run with no PVs, LVs, or VGs.
- Add omitted unlock_vg() call when sigint_caught() during vg processing.
- Fix free_count when reading pool metadata.
- Fix segfault when using pvcreate on a device containing pool metadata.
- In script-processing mode, stop if any command fails.
- Warn if command exits with non-zero status code without a prior log_error.
- Correct config file line numbers in messages when parsing comments.
- Add missing deactivation after activation failure in lvcreate -Zy.
- When removing LV symlinks, skip any where the VG name is not determined.
- Fix vgsplit internal counting of snapshot LVs.
- Update vgsplit to only restrict split with active LVs involved in split.
- Fix vgsplit to only move hidden 'snapshotN' LVs when necessary.
- Update vgsplit man page to reflect lvnames on the cmdline.
- Update vgsplit to take "-n LogicalVolumeName" on the cmdline.
- Fix vgsplit error paths to release vg_to lock.
- Avoid spurious duplicate VG messages referring to VGs that are gone.
- Drop dev_name_confirmed error message to debug level.
- Fix setpriority error message to signed int.
- Add assertions to trap deprecated P_ and V_ lock usage.
- Avoid using DLM locks with LCK_CACHE type P_ lock requests.
- Don't touch /dev in vgrename if activation is disabled.
- Exclude VG_GLOBAL from internal concurrent VG lock counter.
- Fix vgmerge snapshot_count when source VG contains snapshots.
- Fix internal LV counter when a snapshot is removed.
- Fix metadata corruption writing lvm1-formatted metadata with snapshots.
- Fix lvconvert -m0 allocatable space check.
- Don't attempt remote metadata backups of non-clustered VGs.
- Improve preferred_names lvm.conf example.
- Fix vgdisplay 'Cur LV' field to match lvdisplay output.
- Fix lv_count report field to exclude hidden LVs.
- Fix some pvmove error status codes.
- Indicate whether or not VG is clustered in vgcreate log message.
- Mention default --clustered setting in vgcreate man page.
- Fix vgreduce to use vg_split_mdas to check sufficient mdas remain.
- Update lvmcache VG lock state for all locking types now.
- Fix output if overriding command_names on cmdline.
- Add check to vg_commit() ensuring VG lock held before writing new VG metadata.
- Add validation of LV name to pvmove -n.
- Add some basic internal VG lock validation.
- Fix vgsplit internal counting of snapshot LVs.
- Update vgsplit to only restrict split with active LVs involved in split.
- Fix vgsplit to only move hidden 'snapshotN' LVs when necessary.
- Update vgsplit man page to reflect lvnames on the cmdline.
- Update vgsplit to take "-n LogicalVolumeName" on the cmdline.
- Fix vgsplit error paths to release vg_to lock.
- Fix vgsplit locking of new VG.
- Avoid erroneous vgsplit error message for new VG.
- Suppress duplicate message when lvresize fails because of invalid vgname.
- Cache VG metadata internally while VG lock is held.
- Fix redundant lvresize message if vg doesn't exist.
- Make clvmd-cman use a hash rather than an array for node updown info.
- Decode numbers in clvmd debugging output.
- Fix uninitialised mutex in clvmd if all daemons are not running at startup.
- Add config file overrides to clvmd when it reads the active LVs list.
- Make clvmd refresh the context correctly when lvm.conf is updated.
- Fix another allocation bug with clvmd and large node IDs.
- Fix uninitialised variable in clvmd that could cause odd hangs.
- Correct command name in lvmdiskscan man page.
- clvmd no longer crashes if it sees nodeids over 50.
- Fix potential deadlock in clvmd thread handling.
- Update usage message for clvmd.
- Fix clvmd man page not to print <br> and clarified debug options.
- Escape double quotes and backslashes in external metadata and config data.
- Correct a function name typo in _line_append error message.
- Fix resetting of MIRROR_IMAGE and VISIBLE_LV after removal of LV.
- Fix remove_layer_from_lv to empty the LV before removing it.
- Add missing no-longer-used segs_using_this_lv test to check_lv_segments.
- Fix lvconvert detection of mirror conversion in progress.
- Avoid automatic lvconvert polldaemon invocation when -R specified.
- Fix 'pvs -a' to detect VGs of PVs without metadata areas.
- Divide up internal orphan volume group by format type.
- Fix lvresize to support /dev/mapper prefix in the LV name.
- Fix lvresize to pass new size to fsadm when extending device.
- Fix unfilled parameter passed to fsadm from lvresize.
- Update fsadm to call lvresize if the partition size differs (with option -l).
- Fix fsadm to support VG/LV names.

* Wed Apr  2 2008 Jeremy Katz <katzj@redhat.com> - 2.02.33-11
- Adjust for new name for vio disks (from danpb)
- And fix the build (also from danpb)

* Wed Mar  5 2008 Jeremy Katz <katzj@redhat.com> - 2.02.33-10
- recognize vio disks

* Thu Jan 31 2008 Alasdair Kergon <agk@redhat.com> - 2.02.33-9
- Improve internal label caching performance while locks are held.
- Fix mirror log name construction during lvconvert.

* Tue Jan 29 2008 Alasdair Kergon <agk@redhat.com> - 2.02.32-8
- Fix pvs, vgs, lvs error exit status on some error paths.
- Fix new parameter validation in vgsplit and test mode.
- Fix internal metadata corruption in lvchange --resync.

* Sat Jan 19 2008 Alasdair Kergon <agk@redhat.com> - 2.02.31-7
- Avoid readahead error message when using default setting of lvcreate -M1.
- Fix lvcreate --nosync not to wait for non-happening sync.
- Add very_verbose lvconvert messages.

* Thu Jan 17 2008 Alasdair Kergon <agk@redhat.com> - 2.02.30-6
- Remove static libraries and binaries and move most binaries out of /usr.
- Fix a segfault if using pvs with --all argument.
- Fix vgreduce PV list processing not to process every PV in the VG.
- Reinstate VG extent size and stripe size defaults (halved).
- Set default readahead to twice maximium stripe size.
- Detect non-orphans without MDAs correctly.
- Prevent pvcreate from overwriting MDA-less PVs belonging to active VGs.
- Don't use block_on_error with mirror targets version 1.12 and above.
- Change vgsplit -l (for unimplemented --list) into --maxlogicalvolumes.
- Update vgsplit to accept vgcreate options when new VG is destination.
- Update vgsplit to accept existing VG as destination.
- Major restructuring of pvmove and lvconvert code, adding stacking support.
- Add new convert_lv field to lvs output.
- Permit LV segment fields with PV segment reports.
- Extend lvconvert to use polldaemon and wait for completion of initial sync.
- Add seg_start_pe and seg_pe_ranges to reports.
- Add fsadm interface to filesystem resizing tools.
- Update --uuid argument description in man pages.
- Print warning when lvm tools are running as non-root.

* Thu Dec 20 2007 Alasdair Kergon <agk@redhat.com> - 2.02.29-5
- Fix libdevmapper readahead processing with snapshots (for example).

* Thu Dec 13 2007 Alasdair Kergon <agk@redhat.com> - 2.02.29-4
- Add missing lvm2 build & runtime dependencies on module-init-tools (modprobe).

* Thu Dec  6 2007 Jeremy Katz <katzj@redhat.com> - 2.02.29-3
- fix requirements

* Thu Dec 06 2007 Alasdair Kergon <agk@redhat.com> - 2.02.29-2
- Fold device-mapper build into this lvm2 spec file.

* Wed Dec 05 2007 Alasdair Kergon <agk@redhat.com> - 2.02.29-1
- Make clvmd backup vg metadata on remote nodes.
- Decode cluster locking state in log message.
- Change file locking state messages from debug to very verbose.
- Fix --addtag to drop @ prefix from name.
- Stop clvmd going haywire if a pre_function fails.
- Avoid nested vg_reads when processing PVs in VGs and fix associated locking.
- Attempt to remove incomplete LVs with lvcreate zeroing/activation problems.
- Add full read_ahead support.
- Add lv_read_ahead and lv_kernel_read_ahead fields to reports and lvdisplay.
- Prevent lvconvert -s from using same LV as origin and snapshot.
- Fix human-readable output of odd numbers of sectors.
- Add pv_mda_free and vg_mda_free fields to reports for raw text format.
- Add LVM2 version to 'Generated by' comment in metadata.
- Show 'not usable' space when PV is too large for device in pvdisplay.
- Ignore and fix up any excessive device size found in metadata.
- Fix error message when fixing up PV size in lvm2 metadata (2.02.11).
- Fix orphan-related locking in pvdisplay and pvs.
- Fix missing VG unlocks in some pvchange error paths.
- Add some missing validation of VG names.
- Detect md superblocks version 1.0, 1.1 and 1.2.
- Add some pv-related error paths.
- Handle future sysfs subsystem/block/devices directory structure.
- Fix a bug in lvm_dump.sh checks for lvm/dmsetup binaries.
- Fix underquotations in lvm_dump.sh.
- Print --help output to stdout, not stderr.
- After a cmdline processing error, don't print help text but suggest --help.
- Add %%PVS extents option to lvresize, lvextend, and lvcreate.
- Remove no-longer-correct restrictions on PV arg count with stripes/mirrors.
- Fix strdup memory leak in str_list_dup().
- Link with -lpthread when static SELinux libraries require that.
- Detect command line PE values that exceed their 32-bit range.
- Include strerror string in dev_open_flags' stat failure message.
- Avoid error when --corelog is provided without --mirrorlog. (2.02.28)
- Correct --mirrorlog argument name in man pages (not --log).
- Clear MIRROR_NOTSYNCED LV flag when converting from mirror to linear.
- Modify lvremove to prompt for removal if LV active on other cluster nodes.
- Add '-f' to vgremove to force removal of VG even if LVs exist.

* Fri Aug 24 2007 Alasdair Kergon <agk@redhat.com> - 2.02.28-1
- vgscan and pvscan now trigger clvmd -R, which should now work.
- Fix clvmd logging so you can get lvm-level debugging out of it.
- Allow clvmd debug to be turned on in a running daemon using clvmd -d [-C].
- Add more cluster info to lvmdump.
- Fix lvdisplay man page to say LV size is reported in sectors, not KB.
- Fix loading of persistent cache if cache_dir is used.
- Only permit --force, --verbose and --debug arguments to be repeated.
- Add support for renaming mirrored LVs.
- Add --mirrorlog argument to specify log type for mirrors.
- Don't leak a file descriptor if flock or fcntl fails.
- Detect stream write failure reliably.
- Reduce severity of lstat error messages to very_verbose.
- Update to use autoconf 2.61, while still supporting 2.57.

* Thu Aug 09 2007 Alasdair Kergon <agk@redhat.com> - 2.02.27-3
- Clarify GPL licence as being version 2.

* Wed Aug 01 2007 Milan Broz <mbroz@redhat.com> - 2.02.27-2
- Add SUN's LDOM virtual block device (vdisk) and ps3disk to filters.

* Wed Jul 18 2007 Alasdair Kergon <agk@redhat.com> - 2.02.27-1
- Add -f to vgcfgrestore to list metadata backup files.
- Add pvdisplay --maps implementation.
- Add devices/preferred_names config regex list for displayed device names.
- Add vg_mda_count and pv_mda_count columns to reports.
- Change cling alloc policy attribute character from 'C' to l'.
- Print warnings to stderr instead of stdout.
- Fix snapshot cow area deactivation if origin is not active.
- Reinitialise internal lvmdiskscan variables when called repeatedly.
- Allow keyboard interrupt during user prompts when appropriate.
- Fix deactivation code to follow dependencies and remove symlinks.
- Fix a segfault in device_is_usable() if a device has no table.
- Fix creation and conversion of mirrors with tags.
- Add command stub for pvck.
- Handle vgsplit of an entire VG as a vgrename.
- Fix vgsplit for lvm1 format (set and validate VG name in PVs metadata).
- Split metadata areas in vgsplit properly.
- Fix and clarify vgsplit error messages.
- Update lists of attribute characters in man pages.
- Remove unsupported LVM1 options from vgcfgrestore man page.
- Update vgcfgrestore man page to show mandatory VG name.
- Update vgrename man page to include UUID and be consistent with lvrename.
- Add some more debug messages to clvmd startup.
- Fix thread race in clvmd.
- Make clvmd cope with quorum devices.
- Add extra internal error checking to clvmd.
- Fix missing lvm_shell symbol in lvm2cmd library.
- Move regex functions into libdevmapper.
- Add kernel and device-mapper targets versions to lvmdump.
- Add /sys/block listings to lvmdump.
- Make lvmdump list /dev recursively.
- Mark /etc/lvm subdirectories as directories in spec file.

* Mon Mar 19 2007 Alasdair Kergon <agk@redhat.com> - 2.02.24-1
- Add BuildRequires readline-static until makefiles get fixed.
- Fix processing of exit status in init scripts
- Fix vgremove to require at least one vg argument.
- Fix reading of striped LVs in LVM1 format.
- Flag nolocking as clustered so clvmd startup sees clustered LVs.
- Add a few missing pieces of vgname command line validation.
- Support the /dev/mapper prefix on most command lines.

* Thu Mar 08 2007 Alasdair Kergon <agk@redhat.com> - 2.02.23-1
- Fix vgrename active LV check to ignore differing vgids.
- Fix two more segfaults if an empty config file section encountered.
- Fix a leak in a reporting error path.
- Add devices/cache_dir & devices/cache_file_prefix, deprecating devices/cache.

* Tue Feb 27 2007 Alasdair Kergon <agk@redhat.com> - 2.02.22-3
- Move .cache file to /etc/lvm/cache.

* Wed Feb 14 2007 Alasdair Kergon <agk@redhat.com> - 2.02.22-2
- Rebuild after device-mapper package split.

* Wed Feb 14 2007 Alasdair Kergon <agk@redhat.com> - 2.02.22-1
- Add ncurses-static BuildRequires after package split.
- Fix loading of segment_libraries.
- If a PV reappears after it was removed from its VG, make it an orphan.
- Don't update metadata automatically if VGIDs don't match.
- Fix some vgreduce --removemissing command line validation.
- Trivial man page corrections (-b and -P).
- Add global/units to example.conf.
- Remove readline support from lvm.static.

* Mon Feb 05 2007 Alasdair Kergon <agk@redhat.com> - 2.02.21-4
- Remove file wildcards and unintentional lvmconf installation.

* Mon Feb 05 2007 Alasdair Kergon <agk@redhat.com> - 2.02.21-3
- Add build dependency on new device-mapper-devel package.

* Wed Jan 31 2007 Alasdair Kergon <agk@redhat.com> - 2.02.21-2
- Remove superfluous execute perm from .cache data file.

* Tue Jan 30 2007 Alasdair Kergon <agk@redhat.com> - 2.02.21-1
- Fix vgsplit to handle mirrors.
- Reorder fields in reporting field definitions.
- Fix vgs to treat args as VGs even when PV fields are displayed.
- Fix md signature check to handle both endiannesses.

* Fri Jan 26 2007 Alasdair Kergon <agk@redhat.com> - 2.02.20-1
- Fix exit statuses of reporting tools.
- Add some missing close() and fclose() return code checks.
- Add devices/ignore_suspended_devices to ignore suspended dm devices.
- Fix refresh_toolcontext() always to wipe persistent device filter cache.
- Long-lived processes write out persistent dev cache in refresh_toolcontext().
- Streamline dm_report_field_* interface.
- Update reporting man pages.
- Add --clustered to man pages.
- Add field definitions to report help text.

* Mon Jan 22 2007 Milan Broz <mbroz@redhat.com> - 2.02.19-2
- Remove BuildRequires libtermcap-devel
  Resolves: #223766

* Wed Jan 17 2007 Alasdair Kergon <agk@redhat.com> - 2.02.19-1
- Fix a segfault if an empty config file section encountered.
- Fix partition table processing after sparc changes.
- Fix cmdline PE range processing segfault.
- Move basic reporting functions into libdevmapper.

* Fri Jan 12 2007 Alasdair Kergon <agk@redhat.com> - 2.02.18-2
- Rebuild.

* Thu Jan 11 2007 Alasdair Kergon <agk@redhat.com> - 2.02.18-1
- Use CFLAGS when linking so mixed sparc builds can supply -m64.
- Prevent permission changes on active mirrors.
- Print warning instead of error message if lvconvert cannot zero volume.
- Add snapshot options to lvconvert man page.
- dumpconfig accepts a list of configuration variables to display.
- Change dumpconfig to use --file to redirect output to a file.
- Avoid vgreduce error when mirror code removes the log LV.
- Fix ambiguous vgsplit error message for split LV.
- Fix lvextend man page typo.
- Use no flush suspending for mirrors.
- Fix create mirror with name longer than 22 chars.

* Thu Dec 14 2006 Alasdair Kergon <agk@redhat.com> - 2.02.17-1
- Add missing pvremove error message when device doesn't exist.
- When lvconvert allocates a mirror log, respect parallel area constraints.
- Check for failure to allocate just the mirror log.
- Support mirror log allocation when there is only one PV: area_count now 0.
- Fix detection of smallest area in _alloc_parallel_area() for cling policy.
- Add manpage entry for clvmd -T
- Fix hang in clvmd if a pre-command failed.

* Fri Dec 01 2006 Alasdair Kergon <agk@redhat.com> - 2.02.16-1
- Fix VG clustered read locks to use PR not CR.
- Adjust some alignments for ia64/sparc.
- Fix mirror segment removal to use temporary error segment.
- Always compile debug logging into clvmd.
- Add startup timeout to clvmd startup script.
- Add -T (startup timeout) switch to clvmd.
- Improve lvm_dump.sh robustness.

* Tue Nov 21 2006 Alasdair Kergon <agk@redhat.com> - 2.02.15-3
- Fix clvmd init script line truncation.

* Tue Nov 21 2006 Alasdair Kergon <agk@redhat.com> - 2.02.15-2
- Fix lvm.conf segfault.

* Mon Nov 20 2006 Alasdair Kergon <agk@redhat.com> - 2.02.15-1
- New upstream - see WHATS_NEW.

* Sat Nov 11 2006 Alasdair Kergon <agk@redhat.com> - 2.02.14-1
- New upstream - see WHATS_NEW.

* Mon Oct 30 2006 Alasdair Kergon <agk@redhat.com> - 2.02.13-2
- Fix high-level free-space check on partial allocation.
  Resolves: #212774

* Fri Oct 27 2006 Alasdair Kergon <agk@redhat.com> - 2.02.13-1
- New upstream - see WHATS_NEW.
  Resolves: #205818

* Fri Oct 20 2006 Alasdair Kergon <agk@redhat.com> - 2.02.12-2
- Remove no-longer-used ldconfig from lvm2-cluster and fix lvmconf
  to cope without the shared library.

* Mon Oct 16 2006 Alasdair Kergon <agk@redhat.com> - 2.02.12-1
- New upstream.

* Sat Oct 14 2006 Alasdair Kergon <agk@redhat.com> - 2.02.11-6
- Incorporate lvm2-cluster as a subpackage.

* Sat Oct 14 2006 Alasdair Kergon <agk@redhat.com> - 2.02.11-5
- Install lvmdump script.

* Sat Oct 14 2006 Alasdair Kergon <agk@redhat.com> - 2.02.11-4
- Build in cluster locking with fallback if external locking fails to load.

* Sat Oct 14 2006 Alasdair Kergon <agk@redhat.com> - 2.02.11-3
- Drop .0 suffix from release.

* Sat Oct 14 2006 Alasdair Kergon <agk@redhat.com> - 2.02.11-2.0
- Append distribution to release.

* Fri Oct 13 2006 Alasdair Kergon <agk@redhat.com> - 2.02.11-1.0
- New upstream with numerous fixes and small enhancements.
  (See the WHATS_NEW documentation file for complete upstream changelog.)

* Thu Sep 28 2006 Peter Jones <pjones@redhat.com> - 2.02.06-4
- Fix metadata and map alignment problems on ppc64 (#206202)

* Tue Aug  1 2006 Jeremy Katz <katzj@redhat.com> - 2.02.06-3
- require new libselinux to avoid segfaults on xen (#200783)

* Thu Jul 27 2006 Jeremy Katz <katzj@redhat.com> - 2.02.06-2
- free trip through the buildsystem

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.02.06-1.2.1
- rebuild

* Tue Jun  6 2006 Stephen C. Tweedie <sct@redhat.com> - 2.02.06-1.2
- Rebuild to pick up new nosegneg libc.a for lvm.static

* Mon May 22 2006 Alasdair Kergon <agk@redhat.com> - 2.02.06-1.1
- Reinstate archs now build system is back.
- BuildRequires libsepol-devel.

* Fri May 12 2006 Alasdair Kergon <agk@redhat.com> - 2.02.06-1.0
- New upstream release.

* Sat Apr 22 2006 Alasdair Kergon <agk@redhat.com> - 2.02.05-1.1
- Exclude archs that aren't building.

* Fri Apr 21 2006 Alasdair Kergon <agk@redhat.com> - 2.02.05-1.0
- Fix VG uuid comparisons.

* Wed Apr 19 2006 Alasdair Kergon <agk@redhat.com> - 2.02.04-1.0
- New release upstream, including better handling of duplicated VG names.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.02.01-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.02.01-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Dec  2 2005 Peter Jones <pjones@redhat.com> - 2.02.01-1
- update to 2.02.01

* Tue Nov  8 2005 Jeremy Katz <katzj@redhat.com> - 2.01.14-4
- add patch for xen block devices

* Sat Oct 15 2005 Florian La Roche <laroche@redhat.com>
- add -lselinux -lsepol to the static linking -ldevice-mapper requires it

* Wed Sep 14 2005 Jeremy Katz <katzj@redhat.com> - 2.01.14-2
- the distro doesn't really work without a 2.6 kernel, so no need to require it

* Thu Aug 4 2005 Alasdair Kergon <agk@redhat.com> - 2.01.14-1.0
- And a few more bugs fixes.

* Wed Jul 13 2005 Alasdair Kergon <agk@redhat.com> - 2.01.13-1.0
- Fix several bugs discovered in the last release.

* Tue Jun 14 2005 Alasdair Kergon <agk@redhat.com> - 2.01.12-1.0
- New version upstream with a lot of fixes and enhancements.

* Wed Apr 27 2005 Alasdair Kergon <agk@redhat.com> - 2.01.08-2.1
- Add /etc/lvm

* Wed Apr 27 2005 Alasdair Kergon <agk@redhat.com> - 2.01.08-2.0
- No longer abort read operations if archive/backup directories aren't there.
- Add runtime directories and file to the package.

* Tue Mar 22 2005 Alasdair Kergon <agk@redhat.com> - 2.01.08-1.0
- Improve detection of external changes affecting internal cache.
- Add clustered VG attribute.
- Suppress rmdir opendir error message.

* Tue Mar 08 2005 Alasdair Kergon <agk@redhat.com> - 2.01.07-1.3
* Tue Mar 08 2005 Alasdair Kergon <agk@redhat.com> - 2.01.07-1.2
* Tue Mar 08 2005 Alasdair Kergon <agk@redhat.com> - 2.01.07-1.1
- Suppress some new compiler messages.

* Tue Mar 08 2005 Alasdair Kergon <agk@redhat.com> - 2.01.07-1.0
- Remove build directory from built-in path.
- Extra /dev scanning required for clustered operation.

* Thu Mar 03 2005 Alasdair Kergon <agk@redhat.com> - 2.01.06-1.0
- Allow anaconda to suppress warning messages.

* Fri Feb 18 2005 Alasdair Kergon <agk@redhat.com> - 2.01.05-1.0
- Upstream changes not affecting Fedora.

* Wed Feb 09 2005 Alasdair Kergon <agk@redhat.com> - 2.01.04-1.0
- Offset pool minors; lvm2cmd.so skips open fd check; pvmove -f gone.

* Tue Feb 01 2005 Alasdair Kergon <agk@redhat.com> - 2.01.03-1.0
- Fix snapshot device size & 64-bit display output.

* Fri Jan 21 2005 Alasdair Kergon <agk@redhat.com> - 2.01.02-1.0
- Minor fixes.

* Mon Jan 17 2005 Alasdair Kergon <agk@redhat.com> - 2.01.01-1.0
- Update vgcreate man page.  Preparation for snapshot origin extension fix.

* Mon Jan 17 2005 Alasdair Kergon <agk@redhat.com> - 2.01.00-1.0
- Fix metadata auto-correction. Only request open_count when needed.

* Wed Jan 12 2005 Tim Waugh <twaugh@redhat.com> - 2.00.33-2.0
- Rebuilt for new readline.

* Fri Jan 7 2005 Alasdair Kergon <agk@redhat.com> - 2.00.33-1.0
- pvcreate wipes ext label
- several clvm fixes

* Thu Jan 6 2005 Alasdair Kergon <agk@redhat.com> - 2.00.32-2.0
- Remove temporary /sbin symlinks no longer needed.
- Include read-only pool support in the build.

* Wed Dec 22 2004 Alasdair Kergon <agk@redhat.com> - 2.00.32-1.0
- More fixes (143501).

* Sun Dec 12 2004 Alasdair Kergon <agk@redhat.com> - 2.00.31-1.0
- Fix pvcreate install issues.

* Fri Dec 10 2004 Alasdair Kergon <agk@redhat.com> - 2.00.30-1.0
- Additional debugging code.
- Some trivial man page corrections.

* Tue Nov 30 2004 Alasdair Kergon <agk@redhat.com> - 2.00.29-1.3
- Reinstate all archs.

* Sun Nov 28 2004 Alasdair Kergon <agk@redhat.com> - 2.00.29-1.2
- Try excluding more archs.

* Sat Nov 27 2004 Alasdair Kergon <agk@redhat.com> - 2.00.29-1.1
- Exclude s390x which fails.

* Sat Nov 27 2004 Alasdair Kergon <agk@redhat.com> - 2.00.29-1
- Fix last fix.

* Sat Nov 27 2004 Alasdair Kergon <agk@redhat.com> - 2.00.28-1
- Endian fix to partition/md signature detection.

* Wed Nov 24 2004 Alasdair Kergon <agk@redhat.com> - 2.00.27-1
- Fix partition table detection & an out of memory segfault.

* Tue Nov 23 2004 Alasdair Kergon <agk@redhat.com> - 2.00.26-1
- Several installation-related fixes & man page updates.

* Mon Oct 25 2004 Elliot Lee <sopwith@redhat.com> - 2.00.25-1.01
- Fix 2.6 kernel requirement

* Wed Sep 29 2004 Alasdair Kergon <agk@redhat.com> - 2.00.25-1
- Fix vgmknodes return code & vgremove locking.

* Fri Sep 17 2004 Alasdair Kergon <agk@redhat.com> - 2.00.24-2
- Obsolete old lvm1 packages; refuse install if running kernel 2.4. [bz 128185]

* Thu Sep 16 2004 Alasdair Kergon <agk@redhat.com> - 2.00.24-1
- More upstream fixes.  (Always check WHATS_NEW file for details.)
- Add requested BuildRequires. [bz 124916, 132408]

* Wed Sep 15 2004 Alasdair Kergon <agk@redhat.com> - 2.00.23-1
- Various minor upstream fixes.

* Fri Sep  3 2004 Alasdair Kergon <agk@redhat.com> - 2.00.22-1
- Permission fix included upstream; use different endian conversion macros.

* Thu Sep  2 2004 Jeremy Katz <katzj@redhat.com> - 2.00.21-2
- fix permissions on vg dirs

* Thu Aug 19 2004 Alasdair Kergon <agk@redhat.com> - 2.00.21-1
- New upstream release incorporating fixes plus minor enhancements.

* Tue Aug 17 2004 Jeremy Katz <katzj@redhat.com> - 2.00.20-2
- add patch for iSeries viodasd support
- add patch to check file type using stat(2) if d_type == DT_UNKNOWN (#129674)

* Sat Jul 3 2004 Alasdair Kergon <agk@redhat.com> - 2.00.20-1
- New upstream release fixes 2.6 kernel device numbers.

* Tue Jun 29 2004 Alasdair Kergon <agk@redhat.com> - 2.00.19-1
- Latest upstream release.  Lots of changes (see WHATS_NEW).

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com> - 2.00.15-5
- rebuilt

* Wed May 26 2004 Alasdair Kergon <agk@redhat.com> - 2.00.15-4
- clone %%description from LVM rpm

* Wed May 26 2004 Alasdair Kergon <agk@redhat.com> - 2.00.15-3
- vgscan shouldn't return error status when no VGs present

* Thu May 06 2004 Warren Togami <wtogami@redhat.com> - 2.00.15-2
- i2o patch from Markus Lidel

* Tue Apr 20 2004 Bill Nottingham <notting@redhat.com> - 2.00.15-1.1
- handle disabled SELinux correctly, so that LVMs can be detected in a
  non-SELinux context
  
* Mon Apr 19 2004 Alasdair Kergon <agk@redhat.com> - 2.00.15-1
- Fix non-root build with current version of 'install'.

* Fri Apr 16 2004 Alasdair Kergon <agk@redhat.com> - 2.00.14-1
- Use 64-bit file offsets.

* Fri Apr 16 2004 Alasdair Kergon <agk@redhat.com> - 2.00.13-1
- Avoid scanning devices containing md superblocks.
- Integrate ENOTSUP patch.

* Thu Apr 15 2004 Jeremy Katz <katzj@redhat.com> - 2.00.12-4
- don't die if we get ENOTSUP setting selinux contexts

* Thu Apr 15 2004 Alasdair Kergon <agk@redhat.com> 2.00.12-3
- Add temporary pvscan symlink for LVM1 until mkinitrd gets updated.

* Wed Apr 14 2004 Alasdair Kergon <agk@redhat.com> 2.00.12-2
- Mark config file noreplace.

* Wed Apr 14 2004 Alasdair Kergon <agk@redhat.com> 2.00.12-1
- Install default /etc/lvm/lvm.conf.
- Move non-static binaries to /usr/sbin.
- Add temporary links in /sbin to lvm.static until rc.sysinit gets updated.

* Thu Apr 08 2004 Alasdair Kergon <agk@redhat.com> 2.00.11-1
- Fallback to using LVM1 tools when using a 2.4 kernel without device-mapper.

* Wed Apr 07 2004 Alasdair Kergon <agk@redhat.com> 2.00.10-2
- Install the full toolset, not just 'lvm'.

* Wed Apr 07 2004 Alasdair Kergon <agk@redhat.com> 2.00.10-1
- Update to version 2.00.10, which incorporates the RH-specific patches
  and includes various fixes and enhancements detailed in WHATS_NEW.

* Wed Mar 17 2004 Jeremy Katz <katzj@redhat.com> 2.00.08-5
- Fix sysfs patch to find sysfs
- Take patch from dwalsh and tweak a little for setting SELinux contexts on
  device node creation and also do it on the symlink creation.  
  Part of this should probably be pushed down to device-mapper instead

* Thu Feb 19 2004 Stephen C. Tweedie <sct@redhat.com> 2.00.08-4
- Add sysfs filter patch
- Allow non-root users to build RPM

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Dec  5 2003 Jeremy Katz <katzj@redhat.com> 2.00.08-2
- add static lvm binary

* Tue Dec  2 2003 Jeremy Katz <katzj@redhat.com> 
- Initial build.


