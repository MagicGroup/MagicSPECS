%define _hardened_build 1
Name:             zfs-fuse
Version:          0.7.0
Release:          18%{?dist}
Summary:          ZFS ported to Linux FUSE
Summary(zh_CN.UTF-8): ZFS 的 FUSE 移植
Group:            System Environment/Base
Group(zh_CN.UTF-8): 系统环境/基本
License:          CDDL
URL:              http://zfs-fuse.net/
Source00:         http://zfs-fuse.net/releases/0.7.0/%{name}-%{version}.tar.bz2
Source01:         zfs-fuse.service
Source02:         zfs-fuse.scrub
Source03:         zfs-fuse.sysconfig
Source04:         zfs-fuse-helper
Patch0:           zfs-fuse-0.7.0-umem.patch
Patch1:           zfs-fuse-0.7.0-stack.patch
Patch2:           zfs-fuse-printf-format.patch
BuildRequires:    fuse-devel libaio-devel scons zlib-devel openssl-devel libattr-devel prelink
BuildRequires:    systemd-units
Requires:         fuse >= 2.7.4-1
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
# (2010 karsten@redhat.com) zfs-fuse doesn't have s390(x) implementations for atomic instructions
ExcludeArch:      s390
ExcludeArch:      s390x
ExcludeArch:      %{arm}
ExcludeArch:      mips64el
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
ZFS is an advanced modern general-purpose filesystem from Sun
Microsystems, originally designed for Solaris/OpenSolaris.

This project is a port of ZFS to the FUSE framework for the Linux
operating system.

%description -l zh_CN.UTF-8
ZFS 的 FUSE 移植。

%prep
%setup -q

%patch0 -p0
%patch1 -p1
%patch2 -p0

f=LICENSE
%{__mv} $f $f.iso88591
iconv -o $f -f iso88591 -t utf8 $f.iso88591
%{__rm} -f $f.iso88591

chmod -x contrib/test-datasets
chmod -x contrib/find-binaries
chmod -x contrib/solaris/fixfiles.py
chmod -x contrib/zfsstress.py

%build
export CCFLAGS="%{optflags}"
pushd src

scons debug=1 optim='%{optflags}'

%install
%{__rm} -rf %{buildroot}
pushd src
scons debug=1 install install_dir=%{buildroot}%{_bindir} man_dir=%{buildroot}%{_mandir}/man8/ cfg_dir=%{buildroot}/%{_sysconfdir}/%{name}
%{__install} -Dp -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
%{__install} -Dp -m 0755 %{SOURCE2} %{buildroot}%{_sysconfdir}/cron.weekly/98-%{name}-scrub
%{__install} -Dp -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
%{__install} -Dp -m 0755 %{SOURCE4} %{buildroot}%{_bindir}/zfs-fuse-helper

#set stack not executable, BZ 911150
for i in zdb zfs zfs-fuse zpool ztest; do
       /usr/bin/execstack -c %{buildroot}%{_bindir}/$i
done

%clean
%{__rm} -rf %{buildroot}

%post
# Move cache if upgrading
oldcache=/etc/zfs/zpool.cache      # this changed per 0.6.9, only needed when upgrading from earlier versions
newcache=/var/lib/zfs/zpool.cache

if [[ -f $oldcache && ! -e $newcache ]]; then
  echo "Moving existing zpool.cache to new location"
  mkdir -p $(dirname $newcache)
  mv $oldcache $newcache
else
  if [ -e $oldcache ]; then
    echo "Note: old zpool.cache present but no longer used ($oldcache)"
  fi
fi

if [ $1 -eq 1 ] ; then 
    # Initial installation 
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%preun
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable zfs-fuse.service > /dev/null 2>&1 || :
    /bin/systemctl stop zfs-fuse.service > /dev/null 2>&1 || :
fi

%postun
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /bin/systemctl try-restart zfs-fuse.service >/dev/null 2>&1 || :
    echo "Removing files since we removed the last package"
    rm -rf /var/run/zfs
    rm -rf /var/lock/zfs
fi

%triggerun -- zfs-fuse < 0.7.0-4
# Save the current service runlevel info
# User must manually run systemd-sysv-convert --apply zfs-fuse
# to migrate them to systemd targets
/usr/bin/systemd-sysv-convert --save zfs-fuse >/dev/null 2>&1 ||:

# Run these because the SysV package being removed won't do them
/sbin/chkconfig --del zfs-fuse >/dev/null 2>&1 || :
/bin/systemctl try-restart zfs-fuse.service >/dev/null 2>&1 || :

%files
%defattr(-, root, root, -)
%doc BUGS CHANGES contrib HACKING LICENSE README 
%doc README.NFS STATUS TESTING TODO
%{_bindir}/zdb
%{_bindir}/zfs
%{_bindir}/zfs-fuse
%{_bindir}/zfs-fuse-helper
%{_bindir}/zpool
%{_bindir}/zstreamdump
%{_bindir}/ztest
%{_unitdir}/%{name}.service
%{_sysconfdir}/cron.weekly/98-%{name}-scrub
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_sysconfdir}/%{name}/
%{_mandir}/man8/zfs-fuse.8.gz
%{_mandir}/man8/zdb.8.gz
%{_mandir}/man8/zfs.8.gz
%{_mandir}/man8/zpool.8.gz
%{_mandir}/man8/zstreamdump.8.gz

%changelog
* Fri Nov 06 2015 Liu Di <liudidi@gmail.com> - 0.7.0-18
- 为 Magic 3.0 重建

* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 0.7.0-17
- 为 Magic 3.0 重建

* Mon Feb 10 2014 Jon Ciesla <limburgher@gmail.com> - 0.7.0-16
- Fix format-security FTBFS, BZ 1037411.

* Tue Aug 13 2013 Jon Ciesla <limburgher@gmail.com> - 0.7.0-15
- ExcludeArch ARM, BZ 993168.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Jon Ciesla <limburgher@gmail.com> - 0.7.0-13
- Fixed date, systemd-units BR.

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 0.7.0-12
- Perl 5.18 rebuild

* Fri May 24 2013 Jon Ciesla <limburgher@gmail.com> - 0.7.0-11
- Fix unit file typo, BZ 966850.

* Fri Feb 15 2013 Jon Ciesla <limburgher@gmail.com> - 0.7.0-10
- Patch to add stack-protector and FORTIFY_SOURCE, BZ 911150.

* Thu Feb 14 2013 Jon Ciesla <limburgher@gmail.com> - 0.7.0-9
- Set stack not executable on some binaries, BZ 911150.

* Tue Jan 29 2013 Jon Ciesla <limburgher@gmail.com> - 0.7.0-8
- Correct OOM immunization.
- Drop PrivateTmp to fix mount issue, BZ 904643.

* Tue Jan 15 2013 Jon Ciesla <limburgher@gmail.com> - 0.7.0-7
- Fix directory ownership, BZ 894517.

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Apr 12 2012 Jon Ciesla <limburgher@gmail.com> - 0.7.0-5
- Add hardened build.

* Wed Mar 14 2012 Jon Ciesla <limburgher@gmail.com> - 0.7.0-4
- Migrate to systemd.

* Tue Feb 28 2012 Jon Ciesla <limburgher@gmail.com> - 0.7.0-3
- Partially decrufted spec.

* Tue Feb 28 2012 Jon Ciesla <limburgher@gmail.com> - 0.7.0-2
- Fixed sysconfig permissions, BZ 757488.

* Mon Feb 27 2012 Jon Ciesla <limburgher@gmail.com> - 0.7.0-1
- New upstream, fix FTBFS BZ 716087.
- Patch out bad umem declaration.
- Stop starting automatically in post. BZ 755464.
- Marked sysconfig file noreplace, BZ 772403.
- Setting weekly scrub to off by default in sysconfig to silence crob job if service disabled, BZ 757488 et. al.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.9-9.20100709git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.9-8.20100709git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Aug 01 2010 Uwe Kubosch <uwe@kubosch.no> - 0.6.9-7.20100709git
- Moved to fedpkg and git
- Fixed missing dependency to libaio

* Fri Jul 09 2010 Uwe Kubosch <uwe@kubosch.no> - 0.6.9-6.20100709git
- Updated to upstream maintenance snapshot.
- Fixes build problems on EL5
- Added zfs-fuse man page
- Removed package patching of linked libraries

* Mon Jul 05 2010 Uwe Kubosch <uwe@kubosch.no> - 0.6.9-5
- Cleanup of RPM spec and init script

* Sun Jul 04 2010 Uwe Kubosch <uwe@kubosch.no> - 0.6.9-4
- Patched SConstruct to define NDEBUG instead of DEBUG to avoid debug code while still generating debug symbols
- Added moving of zfs.cache when updating from pre 0.6.9 version

* Sat Jul 03 2010 Uwe Kubosch <uwe@kubosch.no> - 0.6.9-2
- Updated to upstream stable release 0.6.9
- Patched default debug level from 0 to 1
- Fixed missing compiler flags and debug flag in build: BUG 595442

* Sat May 22 2010 Uwe Kubosch <uwe@kubosch.no> - 0.6.9_beta3-6
- Updated to upstream version 0.6.9_beta3
- Add more build requires to build on F13 BUG 565076
- Add patches for missing libraries and includes to build on F13 BUG 565076
- Added packages for ppc and ppc64
- Build on F13 BUG 565076
- Fixes BUG 558172
- Added man files
- Added zfs_pool_alert
- Added zstreamdump
- Fixed bug in automatic scrub script BUG 559518

* Mon Jan 04 2010 Uwe Kubosch <uwe@kubosch.no> - 0.6.0-6
- Added option for automatic weekly scrubbing.
  Set ZFS_WEEKLY_SCRUB=yes in /etc/sysconfig/zfs-fuse to enable
- Changed ZFS_AUTOMOUNT option value from "1" to "yes" for better readability.
  ZFS_AUTOMOUNT=1 deprecated and will be removed in version 0.7.0.
- Added option for killing processes with unknown working directory at zfs-fuse startup.
  This would be the case if zfs-fuse crashed.  Use with care.  It may kill unrelated processes.
  Set ZFS_KILL_ORPHANS=yes_really in /etc/sysconfig/zfs-fuse to enable.
- Relaxed dependency on fuse from 2.8.0 to 2.7.4 to allow installation on RHEL/Centos 5

* Sat Dec 26 2009 Uwe Kubosch <uwe@kubosch.no> - 0.6.0-5
- Removed chckconfig on and service start commands from install script
  See https://fedoraproject.org/wiki/Packaging:SysVInitScript#Why_don.27t_we

* Sat Dec 26 2009 Uwe Kubosch <uwe@kubosch.no> - 0.6.0-4
- Updated to upstream version 0.6.0 STABLE

* Mon Nov 30 2009 Uwe Kubosch <uwe@kubosch.no> - 0.6.0-3
- Updated the home page URL to http://zfs-fuse.net/

* Sat Nov 28 2009 Uwe Kubosch <uwe@kubosch.no> - 0.6.0-2
- Corrected some KOJI build errors.

* Fri Nov 27 2009 Uwe Kubosch <uwe@kubosch.no> - 0.6.0-1
- Updated to upstream version 0.6.0 BETA
- Updated dependency to Fuse 2.8.0
- Minor change in spec: Source0 to Source00 for consistency

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-9.20081221.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 10 2009 Karsten Hopp <karsten@redhat.com> 0.5.0-8.20081221.1
- excludearch s390, s390x as there is no implementation for atomic instructions

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-8.20081221
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 24 2009 Uwe Kubosch <uwe@kubosch.no> - 0.5.0-7.20081221
- Updated etc/init.d/zfs-fuse init script after feedback from Rudd-O
  Removed limits for the fuse process which could lead to a hung system
  or use lots of memory.

* Sun Dec 28 2008 Uwe Kubosch <uwe@kubosch.no> - 0.5.0-6.20081221
- Updated etc/init.d/zfs-fuse init script after feedback from Rudd-O at
  http://groups.google.com/group/zfs-fuse/browse_thread/thread/da94aa803bceef52
- Adds better wait at startup before mounting filesystems.
- Add OOM kill protection.
- Adds syncing of disks at shutdown.
- Adds pool status when asking for service status.
- Changed to start zfs-fuse at boot as default.
- Changed to start zfs-fuse right after installation.
- Cleanup of /var/run/zfs and /var/lock/zfs after uninstall.

* Wed Dec 24 2008 Uwe Kubosch <uwe@kubosch.no> - 0.5.0-5.20081221
- Development tag.

* Sun Dec 21 2008 Uwe Kubosch <uwe@kubosch.no> - 0.5.0-4.20081221
- Updated to upstream trunk of 2008-12-21
- Added config file in /etc/sysconfig/zfs
- Added config option ZFS_AUTOMOUNT=0|1 to mount filesystems at boot

* Tue Nov 11 2008 Uwe Kubosch <uwe@kubosch.no> - 0.5.0-3.20081009
- Rebuild after import into Fedora build system.

* Thu Oct 09 2008 Uwe Kubosch <uwe@kubosch.no> - 0.5.0-2.20081009
- Updated to upstream trunk of 2008-10-09
- Adds changes to make zfs-fuse build out-of-the-box on Fedora 9,
  and removes the need for patches.

* Sat Oct  4 2008 Terje Rosten <terje.rosten@ntnu.no> - 0.5.0-1 
- initial build
