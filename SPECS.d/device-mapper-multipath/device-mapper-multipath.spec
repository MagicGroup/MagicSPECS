Summary: Tools to manage multipath devices using device-mapper
Summary(zh_CN.UTF-8): 使用 device-mapper 管理多路径设备的工具
Name: device-mapper-multipath
Version: 0.4.9
Release: 63%{?dist}
License: GPL+
Group: System Environment/Base
Group(zh_CN.UTF-8): 系统环境/基本
URL: http://christophe.varoqui.free.fr/

Source0: multipath-tools-130222.tgz
Source1: multipath.conf
Patch0001: 0001-RH-dont_start_with_no_config.patch
Patch0002: 0002-RH-multipath.rules.patch
Patch0003: 0003-RH-Make-build-system-RH-Fedora-friendly.patch
Patch0004: 0004-RH-multipathd-blacklist-all-by-default.patch
Patch0005: 0005-RH-add-mpathconf.patch
Patch0006: 0006-RH-add-find-multipaths.patch
Patch0007: 0007-RH-add-hp_tur-checker.patch
Patch0008: 0008-RH-revert-partition-changes.patch
Patch0009: 0009-RH-RHEL5-style-partitions.patch
Patch0010: 0010-RH-dont-remove-map-on-enomem.patch
Patch0011: 0011-RH-deprecate-uid-gid-mode.patch
Patch0012: 0012-RH-kpartx-msg.patch
Patch0013: 0013-RHBZ-883981-cleanup-rpmdiff-issues.patch
Patch0014: 0014-RH-handle-other-sector-sizes.patch
Patch0015: 0015-RH-fix-output-buffer.patch
Patch0016: 0016-RH-dont-print-ghost-messages.patch
#Patch0017: 0017-RH-fix-sigusr1.patch
Patch0018: 0018-RH-fix-factorize.patch
Patch0019: 0019-RH-fix-sockets.patch
Patch0020: 0020-RHBZ-907360-static-pthread-init.patch
Patch0021: 0021-RHBZ-919119-respect-kernel-cmdline.patch
Patch0022: 0022-RH-multipathd-check-wwids.patch
Patch0023: 0023-RH-multipath-wipe-wwid.patch
Patch0024: 0024-RH-multipath-wipe-wwids.patch
Patch0025: 0025-UPBZ-916668_add_maj_min.patch
Patch0026: 0026-fix-checker-time.patch
Patch0027: 0027-RH-get-wwid.patch
Patch0028: 0028-RHBZ-929078-refresh-udev-dev.patch
Patch0029: 0029-RH-no-prio-put-msg.patch
Patch0030: 0030-RHBZ-916528-override-queue-no-daemon.patch
Patch0031: 0031-RHBZ-957188-kpartx-use-dm-name.patch
Patch0032: 0032-RHBZ-956464-mpathconf-defaults.patch
Patch0033: 0033-RHBZ-829963-e-series-conf.patch
Patch0034: 0034-RHBZ-851416-mpathconf-display.patch
Patch0035: 0035-RHBZ-891921-list-mpp.patch
Patch0036: 0036-RHBZ-949239-load-multipath-module.patch
Patch0037: 0037-RHBZ-768873-fix-rename.patch
Patch0038: 0038-RHBZ-799860-netapp-config.patch
Patch0039: 0039-RH-detect-prio-fix.patch
Patch0040: 0040-RH-bindings-fix.patch
Patch0041: 0041-RH-check-for-erofs.patch
Patch0042: 0042-UP-fix-signal-handling.patch
Patch0043: 0043-RH-signal-waiter.patch
Patch0044: 0044-RHBZ-976688-fix-wipe-wwids.patch
Patch0045: 0045-RHBZ-977297-man-page-fix.patch
Patch0046: 0046-RHBZ-883981-move-udev-rules.patch
Patch0047: 0047-RHBZ-980777-kpartx-read-only-loop-devs.patch
Patch0048: 0048-RH-print-defaults.patch
Patch0049: 0049-RH-remove-ID_FS_TYPE.patch
#Patch0050: 0050-RH-listing-speedup.patch
Patch0051: 0051-UP-fix-cli-resize.patch
Patch0052: 0052-RH-fix-bad-derefs.patch
Patch0053: 0053-UP-fix-failback.patch
Patch0054: 0054-UP-keep-udev-ref.patch
Patch0055: 0055-UP-handle-quiesced-paths.patch
Patch0056: 0056-UP-alua-prio-fix.patch
Patch0057: 0057-UP-fix-tmo.patch
Patch0058: 0058-UP-fix-failback.patch
Patch0059: 0059-UP-flush-failure-queueing.patch
Patch0060: 0060-UP-uevent-loop-udev.patch
Patch0061: 0061-RH-display-find-mpaths.patch
Patch0062: 0062-RH-dont-free-vecs.patch
Patch0063: 0063-RH-fix-warning.patch
Patch0064: 0064-fix-ID_FS-attrs.patch
Patch0065: 0065-UPBZ-995538-fail-rdac-on-unavailable.patch
Patch0066: 0066-UP-dos-4k-partition-fix.patch
Patch0067: 0067-RHBZ-1022899-fix-udev-partition-handling.patch
Patch0068: 0068-RHBZ-1034578-label-partition-devices.patch
Patch0069: 0069-UPBZ-1033791-improve-rdac-checker.patch
Patch0070: 0070-RHBZ-1036503-blacklist-td-devs.patch
Patch0071: 0071-RHBZ-1031546-strip-dev.patch
Patch0072: 0072-RHBZ-1039199-check-loop-control.patch
Patch0073: 0073-RH-update-build-flags.patch
Patch0074: 0074-RHBZ-1056976-dm-mpath-rules.patch
Patch0075: 0075-RHBZ-1056976-reload-flag.patch
Patch0076: 0076-RHBZ-1056686-add-hw_str_match.patch

# runtime
Requires: %{name}-libs = %{version}-%{release}
Requires: kpartx = %{version}-%{release}
Requires: device-mapper >= 1.02.82-2
Requires: initscripts
Requires(post): systemd-units systemd-sysv chkconfig
Requires(preun): systemd-units
Requires(postun): systemd-units

# build/setup
BuildRequires: libaio-devel, device-mapper-devel >= 1.02.82-2
BuildRequires: readline-devel, ncurses-devel
BuildRequires: systemd-units, systemd-devel

BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%description
%{name} provides tools to manage multipath devices by
instructing the device-mapper multipath kernel module what to do. 
The tools are :
* multipath - Scan the system for multipath devices and assemble them.
* multipathd - Detects when paths fail and execs multipath to update things.

%description -l zh_CN.UTF-8
使用 device-mapper 多路么内核模块管理多路径设备的工具。

%package libs
Summary: The %{name} modules and shared library
Summary(zh_CN.UTF-8): %{name} 的运行库
License: GPL+
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库

%description libs
The %{name}-libs provides the path checker
and prioritizer modules. It also contains the multipath shared library,
libmultipath.

%description libs -l zh_CN.UTF-8
%{name} 的运行库

%package -n kpartx
Summary: Partition device manager for device-mapper devices
Summary(zh_CN.UTF-8): device-mapper 设备的分区管理
Group: System Environment/Base
Group(zh_CN.UTF-8): 系统环境/基本

%description -n kpartx
kpartx manages partition creation and removal for device-mapper devices.

%description -n kpartx -l zh_CN.UTF-8
device-mapper 设备的分区管理程序，可以建立或删除 device-mapper 设备。

%prep
%setup -q -n multipath-tools-130222
%patch0001 -p1
%patch0002 -p1
%patch0003 -p1
%patch0004 -p1
%patch0005 -p1
%patch0006 -p1
%patch0007 -p1
%patch0008 -p1
%patch0009 -p1
%patch0010 -p1
%patch0011 -p1
%patch0012 -p1
%patch0013 -p1
%patch0014 -p1
%patch0015 -p1
%patch0016 -p1
# %%patch0017 -p1
%patch0018 -p1
%patch0019 -p1
%patch0020 -p1
%patch0021 -p1
%patch0022 -p1
%patch0023 -p1
%patch0024 -p1
%patch0025 -p1
%patch0026 -p1
%patch0027 -p1
%patch0028 -p1
%patch0029 -p1
%patch0030 -p1
%patch0031 -p1
%patch0032 -p1
%patch0033 -p1
%patch0034 -p1
%patch0035 -p1
%patch0036 -p1
%patch0037 -p1
%patch0038 -p1
%patch0039 -p1
%patch0040 -p1
%patch0041 -p1
%patch0042 -p1
%patch0043 -p1
%patch0044 -p1
%patch0045 -p1
%patch0046 -p1
%patch0047 -p1
%patch0048 -p1
%patch0049 -p1
# %%patch0050 -p1
%patch0051 -p1
%patch0052 -p1
%patch0053 -p1
%patch0054 -p1
%patch0055 -p1
%patch0056 -p1
%patch0057 -p1
%patch0058 -p1
%patch0059 -p1
%patch0060 -p1
%patch0061 -p1
%patch0062 -p1
%patch0063 -p1
%patch0064 -p1
%patch0065 -p1
%patch0066 -p1
%patch0067 -p1
%patch0068 -p1
%patch0069 -p1
%patch0070 -p1
%patch0071 -p1
%patch0072 -p1
%patch0073 -p1
%patch0074 -p1
%patch0075 -p1
%patch0076 -p1
cp %{SOURCE1} .

%build
%define _sbindir /usr/sbin
%define _libdir /usr/%{_lib}
%define _libmpathdir %{_libdir}/multipath
make %{?_smp_mflags} LIB=%{_lib}

%install
rm -rf %{buildroot}

make install \
	DESTDIR=%{buildroot} \
	bindir=%{_sbindir} \
	syslibdir=%{_libdir} \
	libdir=%{_libmpathdir} \
	rcdir=%{_initrddir} \
	unitdir=%{_unitdir}

# tree fix up
install -d %{buildroot}/etc/multipath
rm -f %{buildroot}%{_initrddir}/multipathd
magic_rpm_clean.sh

%clean
rm -rf %{buildroot}

%post
%systemd_post multipathd.service

%preun
%systemd_preun multipathd.service

%postun
if [ $1 -ge 1 ] ; then
	/sbin/multipathd forcequeueing daemon > /dev/null 2>&1 || :
fi
%systemd_postun_with_restart multipathd.service

%triggerun -- %{name} < 0.4.9-37
# make sure old systemd symlinks are removed after changing the [Install]
# section in multipathd.service from multi-user.target to sysinit.target
/bin/systemctl --quiet is-enabled multipathd.service >/dev/null 2>&1 && /bin/systemctl reenable multipathd.service ||:

%triggerun --  %{name} < 0.4.9-16
%{_bindir}/systemd-sysv-convert --save multipathd >/dev/null 2>&1 ||: 
bin/systemctl --no-reload enable multipathd.service >/dev/null 2>&1 ||:
/sbin/chkconfig --del multipathd >/dev/null 2>&1 || :
/bin/systemctl try-restart multipathd.service >/dev/null 2>&1 || :

%files
%defattr(-,root,root,-)
%{_sbindir}/multipath
%{_sbindir}/multipathd
%{_sbindir}/mpathconf
%{_sbindir}/mpathpersist
%{_unitdir}/multipathd.service
%{_mandir}/man3/mpath_persistent_reserve_in.3.gz
%{_mandir}/man3/mpath_persistent_reserve_out.3.gz
%{_mandir}/man5/multipath.conf.5.gz
%{_mandir}/man8/multipath.8.gz
%{_mandir}/man8/multipathd.8.gz
%{_mandir}/man8/mpathconf.8.gz
%{_mandir}/man8/mpathpersist.8.gz
%config /usr/lib/udev/rules.d/62-multipath.rules
%config /usr/lib/udev/rules.d/11-dm-mpath.rules
%doc AUTHOR COPYING FAQ
%doc multipath.conf
%dir /etc/multipath

%files libs
%defattr(-,root,root,-)
%doc AUTHOR COPYING
%{_libdir}/libmultipath.so
%{_libdir}/libmultipath.so.*
%{_libdir}/libmpathpersist.so
%{_libdir}/libmpathpersist.so.*
%dir %{_libmpathdir}
%{_libmpathdir}/*

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files -n kpartx
%defattr(-,root,root,-)
%{_sbindir}/kpartx
%{_mandir}/man8/kpartx.8.gz

%changelog

