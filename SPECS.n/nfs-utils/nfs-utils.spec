Summary: NFS utilities and supporting clients and daemons for the kernel NFS server
Name: nfs-utils
URL: http://sourceforge.net/projects/nfs
Version: 1.2.5
Release: 15%{?dist}
Epoch: 1

# group all 32bit related archs
%define all_32bit_archs i386 i486 i586 i686 athlon ppc sparcv9

Source0: http://www.kernel.org/pub/linux/utils/nfs/%{name}-%{version}.tar.bz2

Source9: id_resolver.conf
Source10: nfs.sysconfig
Source11: nfs-lock.service
Source12: nfs-secure.service
Source13: nfs-secure-server.service
Source14: nfs-server.service
Source15: nfs-blkmap.service
%define nfs_services %{SOURCE11} %{SOURCE12} %{SOURCE13} %{SOURCE14} %{SOURCE15}

Source20: var-lib-nfs-rpc_pipefs.mount
Source21: proc-fs-nfsd.mount
%define nfs_automounts %{SOURCE20} %{SOURCE21}

Source50: nfs-lock.preconfig
Source51: nfs-server.preconfig
Source52: nfs-server.postconfig
%define nfs_configs %{SOURCE50} %{SOURCE51} %{SOURCE52} 

Patch001: nfs-utils-1.2.6-rc6.patch
Patch002: nfs-utils-1.2.4-mountshortcut.patch
Patch003: nfs-utils-1.2.5-libidmap-hide-syms.patch
Patch004: nfs-utils-1.2.5-nfsd-new-default.patch
Patch005: nfs-utils-1.2.5-gssd-usercreds.patch
Patch006: nfs-utils-1.2.5-gssd-nolibgssapi-krb5.patch

Patch100: nfs-utils-1.2.1-statdpath-man.patch
Patch101: nfs-utils-1.2.1-exp-subtree-warn-off.patch
Patch102: nfs-utils-1.2.3-sm-notify-res_init.patch
Patch103: nfs-utils-1.2.5-idmap-errmsg.patch

Group: System Environment/Daemons
Provides: exportfs    = %{epoch}:%{version}-%{release}
Provides: nfsstat     = %{epoch}:%{version}-%{release}
Provides: showmount   = %{epoch}:%{version}-%{release}
Provides: rpcdebug    = %{epoch}:%{version}-%{release}
Provides: rpc.idmapd  = %{epoch}:%{version}-%{release}
Provides: rpc.mountd  = %{epoch}:%{version}-%{release}
Provides: rpc.nfsd    = %{epoch}:%{version}-%{release}
Provides: rpc.statd   = %{epoch}:%{version}-%{release}
Provides: rpc.gssd    = %{epoch}:%{version}-%{release}
Provides: rpc.svcgssd = %{epoch}:%{version}-%{release}
Provides: mount.nfs   = %{epoch}:%{version}-%{release}
Provides: mount.nfs4  = %{epoch}:%{version}-%{release}
Provides: umount.nfs  = %{epoch}:%{version}-%{release}
Provides: umount.nfs4 = %{epoch}:%{version}-%{release}
Provides: sm-notify   = %{epoch}:%{version}-%{release}
Provides: start-statd = %{epoch}:%{version}-%{release}

License: MIT and GPLv2 and GPLv2+ and BSD
Buildroot: %{_tmppath}/%{name}-%{version}-root
Requires: rpcbind, sed, gawk, sh-utils, fileutils, textutils, grep
Requires: kmod, keyutils
BuildRequires: libgssglue-devel libevent-devel libcap-devel
BuildRequires: libnfsidmap-devel libtirpc-devel libblkid-devel
BuildRequires: krb5-libs >= 1.4 autoconf >= 2.57 openldap-devel >= 2.2
BuildRequires: automake, libtool, glibc-headers, device-mapper-devel
BuildRequires: krb5-devel, tcp_wrappers-devel, libmount-devel
Requires(pre): shadow-utils >= 4.0.3-25
Requires(pre): /usr/sbin/chkconfig /sbin/nologin
Requires: libnfsidmap libgssglue libevent
Requires: libtirpc libblkid libcap libmount
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

%description
The nfs-utils package provides a daemon for the kernel NFS server and
related tools, which provides a much higher level of performance than the
traditional Linux NFS server used by most users.

This package also contains the showmount program.  Showmount queries the
mount daemon on a remote host for information about the NFS (Network File
System) server on the remote host.  For example, showmount can display the
clients which are mounted on that host.

This package also contains the mount.nfs and umount.nfs program.

%prep
%setup -q

%patch001 -p1
%patch002 -p1
%patch003 -p1
%patch004 -p1
%patch005 -p1
%patch006 -p1

%patch100 -p1
%patch101 -p1
%patch102 -p1
%patch103 -p1

# Remove .orig files
find . -name "*.orig" | xargs rm -f

%build

%ifarch s390 s390x sparcv9 sparc64
PIE="-fPIE"
%else
PIE="-fpie"
%endif
export PIE

sh -x autogen.sh

CFLAGS="`echo $RPM_OPT_FLAGS $ARCH_OPT_FLAGS $PIE -D_FILE_OFFSET_BITS=64`"
%configure \
    CFLAGS="$CFLAGS" \
    CPPFLAGS="$DEFINES" \
    LDFLAGS="-pie" \
    --enable-mountconfig \
    --enable-ipv6 \
	--with-statdpath=/var/lib/nfs/statd \
	--enable-libmount-mount

make %{?_smp_mflags} all

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT{sbin,/usr/sbin,%{_prefix}/lib/systemd/system}
mkdir -p $RPM_BUILD_ROOT/usr/lib/%{name}/scripts
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man8
mkdir -p $RPM_BUILD_ROOT/etc/sysconfig
mkdir -p $RPM_BUILD_ROOT/etc/request-key.d
make DESTDIR=$RPM_BUILD_ROOT install
install -s -m 755 tools/rpcdebug/rpcdebug $RPM_BUILD_ROOT/usr/sbin
install -m 644 utils/mount/nfsmount.conf  $RPM_BUILD_ROOT/etc
install -m 644 %{SOURCE9} $RPM_BUILD_ROOT/etc/request-key.d
install -m 644 %{SOURCE10} $RPM_BUILD_ROOT/etc/sysconfig/nfs

for service in %{nfs_services} ; do
	install -m 644 $service $RPM_BUILD_ROOT%{_prefix}/lib/systemd/system
done
for service in %{nfs_automounts} ; do
	install -m 644 $service $RPM_BUILD_ROOT%{_prefix}/lib/systemd/system
done
for config in %{nfs_configs} ; do
	install -m 755 $config $RPM_BUILD_ROOT/usr/lib/%{name}/scripts
done

mkdir -p $RPM_BUILD_ROOT/var/lib/nfs/rpc_pipefs

touch $RPM_BUILD_ROOT/var/lib/nfs/rmtab
mv $RPM_BUILD_ROOT/usr/sbin/rpc.statd $RPM_BUILD_ROOT/sbin

mkdir -p $RPM_BUILD_ROOT/var/lib/nfs/statd/sm
mkdir -p $RPM_BUILD_ROOT/var/lib/nfs/statd/sm.bak
mkdir -p $RPM_BUILD_ROOT/var/lib/nfs/v4recovery
mkdir -p $RPM_BUILD_ROOT/etc/exports.d

mv $RPM_BUILD_ROOT/sbin/* $RPM_BUILD_ROOT%{_sbindir}
rm -rf $RPM_BUILD_ROOT/sbin

magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%pre

# move files so the running service will have this applied as well
for x in gssd svcgssd idmapd ; do
    if [ -f /var/lock/subsys/rpc.$x ]; then
        mv /var/lock/subsys/rpc.$x /var/lock/subsys/rpc$x
    fi
done

/usr/sbin/useradd -l -c "RPC Service User" -r \
        -s /sbin/nologin -u 29 -d /var/lib/nfs rpcuser 2>/dev/null || :
/usr/sbin/groupadd -g 29 rpcuser 2>/dev/null || :

# Using the 16-bit value of -2 for the nfsnobody uid and gid
%define nfsnobody_uid   65534

# Create nfsnobody gid as long as it does not already exist
cat /etc/group | cut -d':' -f 3 | grep --quiet %{nfsnobody_uid} 2>/dev/null
if [ "$?" -eq 1 ]; then
    /usr/sbin/groupadd -g %{nfsnobody_uid} nfsnobody 2>/dev/null || :
else
    /usr/sbin/groupmod -g %{nfsnobody_uid} nfsnobody 2>/dev/null || :
fi

# Create nfsnobody uid as long as it does not already exist.
cat /etc/passwd | cut -d':' -f 3 | grep --quiet %{nfsnobody_uid} 2>/dev/null
if [ "$?" -eq 1 ]; then
    /usr/sbin/useradd -l -c "Anonymous NFS User" -r -g %{nfsnobody_uid} \
        -s /sbin/nologin -u %{nfsnobody_uid} -d /var/lib/nfs nfsnobody 2>/dev/null || :
else

   /usr/sbin/usermod -u %{nfsnobody_uid} nfsnobody 2>/dev/null || :
fi

%post
/usr/bin/systemctl enable nfs-lock.service >/dev/null 2>&1 || :
# Make sure statd used the correct uid/gid.
chown -R rpcuser:rpcuser /var/lib/nfs/statd

%preun
if [ $1 -eq 0 ]; then
	# Package removal, not upgrade
	for service in %(sed 's!\S*/!!g' <<< '%{nfs_services}') ; do
    	/usr/bin/systemctl disable $service >/dev/null 2>&1 || :
    	/usr/bin/systemctl stop $service >/dev/null 2>&1 || :
	done
    /usr/sbin/userdel rpcuser 2>/dev/null || :
    /usr/sbin/groupdel rpcuser 2>/dev/null || :
    /usr/sbin/userdel nfsnobody 2>/dev/null || :
    /usr/sbin/groupdel nfsnobody 2>/dev/null || :
    rm -rf /var/lib/nfs/statd
    rm -rf /var/lib/nfs/v4recovery
fi

%postun
if [ $1 -ge 1 ]; then
	# Package upgrade, not uninstall
	for service in %(sed 's!\S*/!!g' <<< '%{nfs_services}') ; do
    	/usr/bin/systemctl try-restart $service >/dev/null 2>&1 || :
	done
fi
/usr/bin/systemctl --system daemon-reload >/dev/null 2>&1 || :

%triggerun -- nfs-utils < 1:1.2.4-2
/usr/bin/systemctl enable nfs-lock.service >/dev/null 2>&1 || :
if /usr/sbin/chkconfig --level 3 nfs ; then
	/usr/bin/systemctl enable nfs-server.service >/dev/null 2>&1 || :
fi
if /usr/sbin/chkconfig --level 3 rpcgssd ; then
	/usr/bin/systemctl enable nfs-secure.service >/dev/null 2>&1 || :
fi
if /usr/sbin/chkconfig --level 3 rpcsvcgssd ; then
	/usr/bin/systemctl enable nfs-secure-server.service >/dev/null 2>&1 || :
fi

%files
%defattr(-,root,root)
%config(noreplace) /etc/sysconfig/nfs
%config(noreplace) /etc/nfsmount.conf
%dir /etc/exports.d
%dir /var/lib/nfs/v4recovery
%dir /var/lib/nfs/rpc_pipefs
%dir /var/lib/nfs
%dir %attr(700,rpcuser,rpcuser) /var/lib/nfs/statd
%dir %attr(700,rpcuser,rpcuser) /var/lib/nfs/statd/sm
%dir %attr(700,rpcuser,rpcuser) /var/lib/nfs/statd/sm.bak
%config(noreplace) %attr(644,rpcuser,rpcuser) /var/lib/nfs/state
%config(noreplace) /var/lib/nfs/xtab
%config(noreplace) /var/lib/nfs/etab
%config(noreplace) /var/lib/nfs/rmtab
%config(noreplace) %{_sysconfdir}/request-key.d/id_resolver.conf
%doc linux-nfs/ChangeLog linux-nfs/KNOWNBUGS linux-nfs/NEW linux-nfs/README
%doc linux-nfs/THANKS linux-nfs/TODO
/usr/sbin/rpc.statd
/usr/sbin/exportfs
/usr/sbin/nfsstat
/usr/sbin/rpcdebug
/usr/sbin/rpc.mountd
/usr/sbin/rpc.nfsd
/usr/sbin/showmount
/usr/sbin/rpc.idmapd
/usr/sbin/rpc.gssd
/usr/sbin/rpc.svcgssd
/usr/sbin/gss_clnt_send_err
/usr/sbin/gss_destroy_creds
/usr/sbin/sm-notify
/usr/sbin/start-statd
/usr/sbin/mountstats
/usr/sbin/nfsiostat
/usr/sbin/nfsidmap
/usr/sbin/blkmapd
%{_mandir}/*/*
%{_prefix}/lib/systemd/system/*
/usr/lib/%{name}/scripts/*

%attr(4755,root,root)   /usr/sbin/mount.nfs
%attr(4755,root,root)   /usr/sbin/mount.nfs4
%attr(4755,root,root)   /usr/sbin/umount.nfs
%attr(4755,root,root)   /usr/sbin/umount.nfs4

%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 1:1.2.5-15
- 为 Magic 3.0 重建

* Thu Mar 22 2012 Steve Dickson <steved@redhat.com> 1.2.5-14
- gssd: Look for user creds in user defined directory (bz 786993)
- gssd: Don't link with libgssapi_krb5 (bz 784908)

* Fri Mar 16 2012 Steve Dickson <steved@redhat.com> 1.2.5-13
- Make sure statd is start before NFS mounts (bz 786050)
- rpc.idmap: Hide global symbols from libidmap plugins (bz 797332)
- nfsd: Bump up the default to 8 nprocs (bz 757452)

* Wed Feb 08 2012 Harald Hoyer <harald@redhat.com> 1.2.5-12
- require kmod instead of modutils (bz 788571)

* Mon Jan 16 2012 Steve Dickson <steved@redhat.com> 1.2.5-11
- Update to upstream RC release: nfs-utils-1.2.6-rc6
- Reworked how the nfsd service requires the rpcbind service (bz 768550)

* Mon Jan  9 2012 Steve Dickson <steved@redhat.com> 1.2.5-10
- Added back the SUID bits on mount commands (bz 772396)
- Added a decency on keyutils (bz 769724)

* Thu Jan  5 2012 Steve Dickson <steved@redhat.com> 1.2.5-9
- Update to upstream RC release: nfs-utils-1.2.6-rc5

* Thu Dec 15 2011 Steve Dickson <steved@redhat.com> 1.2.5-8
- Removed the nfs-idmap service. rpc.idmap is now part of
  the nfs-server service

* Tue Dec 13 2011 Steve Dickson <steved@redhat.com> 1.2.5-7
- Enabled new idmaping by installing the id_resolver.conf file.
- Update to upstream RC release: nfs-utils-1.2.6-rc4

* Fri Nov 18 2011 Steve Dickson <steved@redhat.com> 1.2.5-6
- Remove RQUOTAD_PORT and RQUOTAD from /etc/sysconfig/nfs (bz 754496)
- Ensured nfs-idmap service is started after the named is up (bz 748275)

* Mon Nov 14 2011 Steve Dickson <steved@redhat.com> 1.2.5-5
- Ensured nfs-idmap service is started after the network up (bz 748275)
- Update to upstream RC release: nfs-utils-1.2.6-rc3 (bz 746497)

* Thu Oct 20 2011 Steve Dickson <steved@redhat.com> 1.2.5-4
- Added pNFS debugging to rpcdebug.

* Tue Oct 18 2011 Steve Dickson <steved@redhat.com> 1.2.5-3
- Update to upstream RC release: nfs-utils-1.2.6-rc2

* Tue Oct  4 2011 Steve Dickson <steved@redhat.com> 1.2.5-2
- Removed SUID bits on mount commands (bz 528498)
- Fixed a few typos in a couple man pages (bz 668124, 673818, 664330)
- Fixed a I/0 problem in rpc.idmapd (bz 684308)

* Mon Oct  3 2011 Steve Dickson <steved@redhat.com> 1.2.5-1
- Update to upstream RC release: nfs-utils-1.2.6-rc1
- Added named.service to After list in nfs-server.service (bz 742746)

* Tue Sep 27 2011 Steve Dickson <steved@redhat.com> 1.2.5-0
- Update to upstream release: nfs-utils-1.2.5 (bz 717931)

* Wed Sep 21 2011 Steve Dickson <steved@redhat.com> 1.2.4-11
- Update to upstream RC release: nfs-utils-1.2.5-rc3

* Wed Sep 14 2011 Steve Dickson <steved@redhat.com> 1.2.4-10
- Created /etc/exports.d to stop a warning (bz 697006)

* Tue Aug 30 2011 Steve Dickson <steved@redhat.com> 1.2.4-9
- Both the nfs.lock and nfs.idmap services should always
  enabled on both installs and upgrades (bz 699040)
- Fixed the paths to the server scriptlets (bz 733531)

* Mon Aug 29 2011 Steve Dickson <steved@redhat.com> 1.2.4-8
- Update to upstream RC release: nfs-utils-1.2.5-rc2

* Wed Aug 24 2011 Steve Dickson <steved@redhat.com> 1.2.4-7
- Added StandardError=syslog+console to all the service files
  so startup errors will be logged. 
- Changed exportfs to only log errors on existing /etc/export.d 
  directory, which eliminates a needless syslog entry.
- Automount /proc/fs/nfsd for rpc.nfsd 

* Wed Aug 10 2011 Steve Dickson <steved@redhat.com> 1.2.4-6
- Fixed some bugs in the triggerun script as well in
  the nfs-server scripts (bz 699040).

* Wed Aug  3 2011 Steve Dickson <steved@redhat.com> 1.2.4-5
- Cleaned up the .preconfig and .postconfig files per
  code review request.

* Wed Aug  3 2011 Steve Dickson <steved@redhat.com> 1.2.4-4
- Converted init scrips to systemd services. (bz 699040)
- Made nfsnobody's uid/gid to always be a 16-bit value of -2
- mount: fix for libmount from util-linux >= 2.20

* Thu Jul 21 2011 Steve Dickson <steved@redhat.com> 1.2.4-3
- Updated to latest upstream release: nfs-utils-1-2-5-rc1

* Thu Jul  7 2011 Ville Skyttä <ville.skytta@iki.fi> - 1:1.2.4-2
- Don't ship Makefiles or INSTALL in docs (#633934).

* Mon Jul  4 2011 J. Bruce Fields <bfields@redhat.com> 1.2.4-1
- Rely on crypto module autoloading in init scripts
- initscripts: just try to mount rpc_pipefs always

* Wed Jun 29 2011 Steve Dickson <steved@redhat.com> 1.2.4-0
- Updated to latest upstream release: nfs-utils-1-2-4

* Wed Apr 20 2011 Steve Dickson <steved@redhat.com> 1.2.3-13
- Updated to latest upstream release: nfs-utils-1-2-4-rc8

* Wed Apr  6 2011 Steve Dickson <steved@redhat.com> 1.2.3-12
- Updated to latest upstream release: nfs-utils-1-2-4-rc7
- Enabled the libmount code.

* Mon Mar  7 2011 Steve Dickson <steved@redhat.com> 1.2.3-11
- Updated to latest upstream release: nfs-utils-1-2-4-rc6

* Wed Feb 09 2011 Christopher Aillon <caillon@redhat.com> - 1.2.3-10
- Rebuild against newer libevent

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.2.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 26 2011 Steve Dickson <steved@redhat.com> 1.2.3-8
- Fixed segfault in rpc.mountd (bz 669065)

* Fri Jan 14 2011 Steve Dickson <steved@redhat.com> 1.2.3-7
- Updated to latest upstream release: nfs-utils-1-2-4-rc5
- Add initscripts changes needed for rpcbind to be running when nfs is started
- Initscripts changes needed to support NFS over RDMA
- Allow the setting of the NFSv4 grace period (bz 665387)

* Mon Dec 13 2010 Steve Dickson <steved@redhat.com> 1.2.3-6
- Updated to latest upstream release: nfs-utils-1-2-4-rc4

* Wed Dec  8  2010 Steve Dickson <steved@redhat.com> 1.2.3-5
- Replace the nfs-utils-lib dependency with a libnfsidmap 
  dependency

* Wed Dec  1  2010 Steve Dickson <steved@redhat.com> 1.2.3-4
- The nfs service is not stopped on reboot or halt (bz 652786)
- Removed obsolete configuration values (bz 653765)

* Mon Nov 29 2010 Steve Dickson <steved@redhat.com> 1.2.3-3
- Updated to latest upstream release: nfs-utils-1-2-4-rc3

* Fri Oct 15 2010 Steve Dickson <steved@redhat.com> 1.2.3-2
- Initscripts do not conform to LSB specification (bz 621562)
- sm-notify needs to call res_init() before each try (bz 625531)
- exports(5) man page duplicated paragraphs (bz 590921)

* Thu Oct 14 2010 Steve Dickson <steved@redhat.com> 1.2.3-1
- Updated to latest upstream release: nfs-utils-1-2-4-rc1

* Mon Oct  4 2010 Steve Dickson <steved@redhat.com> 1.2.3-0.1
- Fixed a regession with -p arguemnt to rpc.mountd 

* Thu Sep 30 2010 Steve Dickson <steved@redhat.com> 1.2.3-0
- Updated to latest upstream release: nfs-utils-1-2-3

* Thu Sep 16 2010 Steve Dickson <steved@redhat.com> 1.2.2-8
- Update to upstream RC release: nfs-utils-1-2-3-rc6

* Thu Sep  9 2010 Steve Dickson <steved@redhat.com> 1.2.2-7
- Update to upstream RC release: nfs-utils-1-2-3-rc5

* Tue Jun 22 2010 Steve Dickson <steved@redhat.com> 1.2.2-6
- Update to upstream RC release: nfs-utils-1-2-3-rc4

* Thu May  6 2010 Steve Dickson <steved@redhat.com> 1.2.2-4
- Update to upstream RC release: nfs-utils-1-2-3-rc3

* Fri Apr 16 2010 Steve Dickson <steved@redhat.com> 1.2.2-3
- Update to upstream RC release: nfs-utils-1-2-3-rc2

* Mon Mar 22 2010 Steve Dickson <steved@redhat.com> 1.2.2-2
- Update to upstream RC release: nfs-utils-1-2-3-rc1

* Thu Feb 18 2010 Steve Dickson <steved@redhat.com> 1.2.2-1
- Updated to latest upstream version: 1.2.2

* Thu Jan 28 2010 Steve Dickson <steved@redhat.com> 1.2.1-17
- Backed out the  "Don't fail mounts when /etc/netconfig is 
  nonexistent" patch

* Wed Jan 27 2010 Steve Dickson <steved@redhat.com> 1.2.1-16
- mount.nfs: Don't fail mounts when /etc/netconfig is nonexistent

* Mon Jan 25 2010 Steve Dickson <steved@redhat.com> 1.2.1-15
- statd: Teach nfs_compare_sockaddr() to handle NULL 
  arguments

* Fri Jan 22 2010 Steve Dickson <steved@redhat.com> 1.2.1-14
- Update to upstream RC release: nfs-utils-1-2-2-rc9

* Thu Jan 21 2010 Steve Dickson <steved@redhat.com> 1.2.1-13
- mount.nfs: Configuration file parser ignoring options
- mount.nfs: Set the default family for lookups based on 
    defaultproto= setting
- Enabled ipv6 

* Sun Jan 17 2010 Steve Dickson <steved@redhat.com> 1.2.1-12
- Updated to latest upstream RC release: nfs-utils-1-2-2-rc7
  which includes Ipv6 support for tcpwrapper (disabled by default).

* Sat Jan 16 2010 Steve Dickson <steved@redhat.com> 1.2.1-11
- Updated to latest upstream RC release: nfs-utils-1-2-2-rc7
  which includes Ipv6 support for statd (disabled by default).

* Thu Jan 14 2010 Steve Dickson <steved@redhat.com> 1.2.1-10
- Updated to the latest pseudo root release (rel10) which
  containts the upstream pseudo root release

* Mon Jan 12 2010 Steve Dickson <steved@redhat.com> 1.2.1-9
- Updated to latest upstream RC release: nfs-utils-1-2-2-rc5

* Mon Jan  4 2010 Steve Dickson <steved@redhat.com> 1.2.1-8
- mount.nfs: don't use IPv6 unless IPV6_SUPPORTED is set

* Mon Dec 14 2009 Steve Dickson <steved@redhat.com> 1.2.1-7
- Updated to latest upstream RC release: nfs-utils-1-2-2-rc3

* Thu Dec 10 2009 Steve Dickson <steved@redhat.com> 1.2.1-6
- Update the  pseudo root to handle security flavors better.

* Mon Dec  7 2009 Steve Dickson <steved@redhat.com> 1.2.1-5
- mount.nfs: Retry v4 mounts with v3 on ENOENT errors

* Mon Dec  7 2009 Steve Dickson <steved@redhat.com> 1.2.1-4
- Updated to the latest pseudo root release (rel9) (bz 538609).

* Thu Nov 12 2009 Steve Dickson <steved@redhat.com> 1.2.1-3
- Stop rpc.nfsd from failing to startup when the network
  is down (bz 532270)

* Wed Nov 11 2009 Steve Dickson <steved@redhat.com> 1.2.1-2
- Updated to the latest pseudo root release (rel8).

* Wed Nov 4 2009 Steve Dickson <steved@redhat.com> 1.2.1-1
- Updated to latest upstream release: 1.2.0

* Tue Nov 3 2009 Steve Dickson <steved@redhat.com> 1.2.0-18
- Reworked and remove some of the Default-Start/Stop stanzas
  in the init scripts (bz 531425)

* Mon Nov 2 2009 Steve Dickson <steved@redhat.com> 1.2.0-17
- Updated to the latest pseudo root release (rel7).
- Added upstream 1.2.1-rc7 patch which fixes:
  - Stop ignoring the -o v4 option (bz 529407)
  - Allow network protocol roll backs when proto is set
    in the config file (bz 529864)
- v4 mounts will roll back to v3 mounts when the mount
  fails with ENOENT. 

* Mon Oct  5 2009 Steve Dickson <steved@redhat.com> 1.2.0-16
- Fixed a whole where '-o v4' was not overriding the
  version in the conf file.

* Wed Sep 30 2009 Steve Dickson <steved@redhat.com> 1.2.0-15
- Change the nfsmount.conf file to define v3 as the default 
  protocol version.
- Make sure versions set on the command line override version
  set in nfsmount.conf
- Make version rollbacks still work when versions are set in
  nfsmount.conf

* Tue Sep 29 2009 Steve Dickson <steved@redhat.com> 1.2.0-13
- Added upstream 1.2.1-rc5 patch
  - mount.nfs: Support negotiation between v4, v3, and v2
  - mount.nfs: Keep server's address in nfsmount_info
  - mount.nfs: Sandbox each mount attempt
  - mount.nfs: Support negotiation between v4, v3, and v2

* Wed Sep 23 2009 Steve Dickson <steved@redhat.com> 1.2.0-12
- Updated to the latest pseudo root release (rel6).

* Tue Sep 15 2009 Steve Dickson <steved@redhat.com> 1.2.0-11
- Added upstream 1.2.1-rc5 patch
  - Added --sort --list functionality to nfs-iostat.py
  - Fixed event handler in idmapd
  - Added -o v4 support
  - Disabled IPv6 support in nfsd
  - Don't give client an empty flavor list
  - Fixed gssed so it does not blindly caches machine credentials

* Mon Aug 17 2009 Steve Dickson <steved@redhat.com> 1.2.0-10
- Added upstream 1.2.1-rc4 patch
  - Fix bug when both crossmnt
  - nfs(5): Add description of lookupcache mount option
  - nfs(5): Remove trailing blanks
  - Added nfs41 support to nfssat
  - Added support for mount to us a configuration file.

* Fri Aug 14 2009 Steve Dickson <steved@redhat.com> 1.2.0-9
- Added upstream 1.2.1-rc3 patch
  - Add IPv6 support to nfsd
  - Allow nfssvc_setfds to properly deal with AF_INET6
  - Convert nfssvc_setfds to use getaddrinfo
  - Move check for active knfsd to helper function
  - Declare a static common buffer for nfssvc.c routine
  - Convert rpc.nfsd to use xlog() and add --debug and --syslog options

* Tue Jul 28 2009 Steve Dickson <steved@redhat.com> 1.2.0-8
- Fixed 4.1 versioning problem (bz 512377)

* Wed Jul 15 2009 Steve Dickson <steved@redhat.com> 1.2.0-7
- Added upstream 1.2.1-rc2 patch
  - A large number of mount command changes.

* Mon Jul 13 2009 Steve Dickson <steved@redhat.com> 1.2.0-6
- Added NFSD v4 dynamic pseudo root patch which allows
  NFS v3 exports to be mounted by v4 clients.

* Mon Jun 29 2009 Steve Dickson <steved@redhat.com> 1.2.0-5
- Stopped rpc.idmapd from spinning (bz 508221)

* Mon Jun 22 2009 Steve Dickson <steved@redhat.com> 1.2.0-4
- Added upstream 1.2.1-rc1 patch 
  - Fix to check in closeall()
  - Make --enable-tirpc the default
  - Set all verbose types in gssd daemons
  - Retry exports if getfh() fails

* Wed Jun 10 2009 Steve Dickson <steved@redhat.com> 1.2.0-3
- Updated init scripts to add dependencies
  on other system facilities (bz 475133)

* Wed Jun 10 2009 Steve Dickson <steved@redhat.com> 1.2.0-2
- nfsnobody gid is wrong (bz 485379)

* Tue Jun  2 2009 Steve Dickson <steved@redhat.com> 1.2.0-1
- Updated to latest upstream release: 1.2.0

* Tue May 19 2009 Tom "spot" Callaway <tcallawa@redhat.com> 1.1.6-4
- Replace the Sun RPC license with the BSD license, with the explicit permission of Sun Microsystems

* Mon May 18 2009 Steve Dickson <steved@redhat.com> 1.1.6-3
- Added upstream 1.1.7-rc1 patch 
  - utils/nfsd: add support for minorvers4
  - sm-notify: Don't orphan addrinfo structs
  - sm-notify: Failed DNS lookups should be retried
  - mount: remove legacy version of nfs_name_to_address()
  - compiling error in rpcgen
  - nfs-utils: Fix IPv6 support in support/nfs/rpc_socket.c
  - umount.nfs: Harden umount.nfs error reportin

* Mon Apr 27 2009 Steve Dickson <steved@redhat.com> 1.1.6-2
- nfslock.init: options not correctly parsed (bz 459591)

* Mon Apr 20 2009 Steve Dickson <steved@redhat.com> 1.1.6-1
- Updated to latest upstream release: 1.1.6

* Mon Mar 23 2009 Steve Dickson <steved@redhat.com> 1.1.5-4
- Added upstream rc3 patch
  - gssd: initialize fakeseed in prepare_krb5_rfc1964_buffer
  - gssd: NULL-terminate buffer after read in read_service_info (try #2)
  - gssd: free buffer allocated by gssd_k5_err_msg
  - gssd: fix potential double-frees in gssd
  - Removed a number of warn_unused_result warnings

* Mon Mar 16 2009 Steve Dickson <steved@redhat.com> 1.1.5-3
- Added upstream rc2 patch

* Fri Mar  6 2009 Steve Dickson <steved@redhat.com> 1.1.5-2
- Fixed lockd not using settings in sysconfig/nfs (bz 461043)
- Fixed some lost externs in the tcpwrapper code

* Thu Mar  5 2009 Steve Dickson <steved@redhat.com> 1.1.5-1
- Updated to latest upstream version: 1.1.5

* Wed Mar  4 2009 Steve Dickson <steved@redhat.com> 1.1.4-21
- configure: fix AC_CACHE_VAL warnings

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.1.4-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 18 2009 Steve Dickson <steved@redhat.com> 1.1.4-19
- Exportfs and rpc.mountd optimalization (bz 76643)

* Tue Feb 17 2009 Steve Dickson <steved@redhat.com> 1.1.4-18
- umount.nfs command: Add an AF_INET6-capable version of nfs_call_unmount()
- umount.nfs command: Support AF_INET6 server addresses
- umount command: remove do_nfs_umount23 function

* Tue Feb 17 2009 Steve Dickson <steved@redhat.com> 1.1.4-17
- Integrated the upstream fix for bz 483375
- mount: segmentation faults on UDP mounts (bz 485448)

* Sat Jan 31 2009 Steve Dickson <steved@redhat.com> 1.1.4-16
- Fixed typo in -mount-textbased.patch (bz 483375)

* Sat Jan 31 2009 Steve Dickson <steved@redhat.com> 1.1.4-15
- Reworked tcp wrapper code to correctly use API (bz 480223)
- General clean up of tcp wrapper code.

* Tue Jan 27 2009 Steve Dickson <steved@redhat.com> 1.1.4-14
- text-based mount command: make po_rightmost() work for N options
- text-based mount command: Function to stuff "struct pmap" from mount options
- text-based mount options: Use new pmap stuffer when	rewriting mount options
- text-based mount command: fix mount option rewriting logic
- text-based mount command: support AF_INET6 in rewrite_mount_options()

* Tue Jan 20 2009 Steve Dickson <steved@redhat.com> 1.1.4-13
- mountd: Don't do tcp wrapper check when there are no rules (bz 448898)

* Wed Jan  7 2009 Steve Dickson <steved@redhat.com> 1.1.4-12
- configure: Remove inet_ntop(3) check from configure.ac
- configure: Add new build option "--enable-tirpc"
- showmount command: Quiesce warning when TI-RPC is disabled

* Sat Jan  3 2009 Steve Dickson <steved@redhat.com> 1.1.4-11
- Added warnings to tcp wrapper code when mounts are 
  denied due to misconfigured DNS configurations.
- gssd: By default, don't spam syslog when users' credentials expire
- mount: revert recent fix for build problems on old systems
- mount: use gethostbyname(3) when building on old systems
- mount: getport: don't use getaddrinfo(3) on old systems
- mount: Random clean up
- configure: use "--disable-uuid" instead of	"--without-uuid"

* Fri Dec 19 2008 Steve Dickson <steved@redhat.com> 1.1.4-10
- Re-enabled and fixed/enhanced tcp wrappers.

* Wed Dec 17 2008 Steve Dickson <steved@redhat.com> 1.1.4-9
- text-based mount command: add function to parse numeric mount options
- text-based mount command: use po_get_numeric() for handling retry
- sm-notify command: fix a use-after-free bug
- statd: not unlinking host files

* Thu Dec 11 2008 Steve Dickson <steved@redhat.com> 1.1.4-8
- mount command: AF_INET6 support for probe_bothports()
- mount command: support AF_INET6 in probe_nfsport() and probe_mntport()
- mount command: full support for AF_INET6 addresses in probe_port()
- gssd/svcgssd: add support to retrieve actual context expiration
- svcgssd: use the actual context expiration for cache

* Sat Dec  6 2008 Steve Dickson <steved@redhat.com> 1.1.4-7
- sm-notify: always exiting without any notification.

* Tue Dec  2 2008 Steve Dickson <steved@redhat.com> 1.1.4-6
- mount command: remove local getport() implementation
- mount command: Replace clnt_ping() and getport() calls in probe_port()
- mount command: Use nfs_error() instead of perror()
- mount command: Use nfs_pmap_getport() in probe_statd()

* Mon Dec  1 2008 Steve Dickson <steved@redhat.com> 1.1.4-5
- Make sure /proc/fs/nfsd exists when the nfs init script
  does the exports (bz 473396)
- Fixed typo in nfs init script that caused rpc.rquotad daemons
  to be started but not stoppped (bz 473929)

* Wed Nov 26 2008 Steve Dickson <steved@redhat.com> 1.1.4-4
- gssd: unblock DNOTIFY_SIGNAL in case it was blocked
- Ensure statd gets started if required when non-root
  user mounts an NFS filesystem

* Tue Nov 25 2008 Steve Dickson <steved@redhat.com> 1.1.4-3
- Give showmount support for querying via rpcbindv3/v4 

* Tue Nov 18 2008 Steve Dickson <steved@redhat.com> 1.1.4-2
- Add AF_INET6-capable API to acquire an RPC CLIENT
- Introduce rpcbind client utility functions

* Sat Oct 18 2008 Steve Dickson <steved@redhat.com> 1.1.4-1
- Updated to latest upstream version: 1.1.4

* Tue Oct 14 2008 Steve Dickson <steved@redhat.com> 1.1.3-6
- sm-notify exists when there are no hosts to notify

* Thu Sep 18 2008 Steve Dickson <steved@redhat.com> 1.1.3-5
- Reworked init scripts so service will be able to
  stop when some of the checks fail. (bz 462508)
- Pre-load nfsd when args to rpc.nfsd are given (bz 441983)

* Thu Aug 28 2008 Steve Dickson <steved@redhat.com> 1.1.3-4
- Added in a number of up upstream patches (101 thru 110).

* Mon Aug 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.1.3-3
- fix license tag

* Thu Jul 31 2008 Steve Dickson <steved@redhat.com> 1.1.3-2
- Mount command did not compile against older glibc versions.

* Mon Jul 28 2008 Steve Dickson <steved@redhat.com> 1.1.3-1
- Updated to latest upstream version: 1.1.3

* Wed Jul  2 2008 Steve Dickson <steved@redhat.com> 1.1.2-12
- Changed the default directories for sm-notify (bz 435480)
- Added 'condstop' to init scripts so service are not
  started when nfs-utils is removed.

* Mon Jun 30 2008 Dennis Gilmore <dennis@ausil.us> 1.1.2-11
- add sparc arch handling 

* Mon Jun 30 2008 Steve Dickson <steved@redhat.com>  1.1.2-10
- Rebuild for the updated libevent lib.

* Fri Jun 27 2008 Steve Dickson <steved@redhat.com>  1.1.2-9
- Removed the nfslock service start/stop from %%post section 
  (bz 453046)

* Wed Jun 25 2008 Steve Dickson <steved@redhat.com>  1.1.2-8
- FQDNs in the rmtab causes exportfs to seg fault (bz 444275)

* Mon Jun 23 2008 Steve Dickson <steved@redhat.com>  1.1.2-7
- Added -D_FILE_OFFSET_BITS=64 to CFLAGS
- make nfsstat read and print stats as unsigned integers
- Added (but not installed) the mountstats and nfs-iostat
  python scripts.

* Fri Jun  6 2008 Steve Dickson <steved@redhat.com>  1.1.2-6
- Added 5 (111 thru 115) upstream patches that fixed
  things mostly in the text mounting code.

* Thu May  8 2008 Steve Dickson <steved@redhat.com>  1.1.2-5
- Added 10 (101 thru 110) upstream patches that fixed
  things mostly in the mount and gssd code.

* Wed May  7 2008 Steve Dickson <steved@redhat.com>  1.1.2-4
- Added ppc arch to the all_32bit_archs list (bz 442847)

* Wed Apr 23 2008 Steve Dickson <steved@redhat.com>  1.1.2-3
- Documented how to turn off/on protocol support for
  rpc.nfsd in /etc/sysconfig/nfs (bz443625)
- Corrected the nfslock initscript 'status' return code (bz 441605)
- Removed obsolete code from the nfslock initscript (bz 441604)

* Mon Apr 14 2008 Steve Dickson <steved@redhat.com>  1.1.2-2
- Make EACCES a non fatal error (bz 439807)

* Tue Mar 25 2008 Steve Dickson <steved@redhat.com>  1.1.2-1
- Upgrade to nfs-utils-1.1.2

* Mon Mar  3 2008 Steve Dickson <steved@redhat.com>  1.1.1-5
- Stopped mountd from incorrectly logging an error
  (commit 9dd9b68c4c44f0d9102eb85ee2fa36a8b7f638e3)
- Stop gssd from ignoring the machine credential caches
  (commit 46d439b17f22216ce8f9257a982c6ade5d1c5931)
- Fixed typo in the nfsstat command line arugments.
  (commit acf95d32a44fd8357c24e8a04ec53fc6900bfc58)
- Added test to stop buffer overflow in idmapd
  (commit bcd0fcaf0966c546da5043be700587f73174ae25)

* Sat Feb  9 2008 Steve Dickson <steved@redhat.com>  1.1.1-4
- Cleaned up some typos that were found in the various
  places in the mountd code

* Thu Jan 24 2008 Steve Dickson <steved@redhat.com>  1.1.1-3
- Added in relatime mount option so mount.nfs stays
  compatible with the mount command in util-linux-ng (bz 274301)

* Tue Jan 22 2008 Steve Dickson <steved@redhat.com>  1.1.1-2
- Added -S/--since to the nfsstat(1) manpage
- The wording in the exportfs man page can be a bit confusing, implying
  that "exportfs -u :/foo" will unexport /foo from all hosts, which it won't
- Removed nfsprog option since the kernel no longer supports it.
- Removed mountprog option since the kernel no longer supports it.
- Stop segfaults on amd64 during warnings messages.
- Fix bug when both crossmnt and fsid are set.

* Sat Jan  5 2008 Steve Dickson <steved@redhat.com>  1.1.1-1
- Updated to latest upstream release, nfs-utils-1.1.1
- Added the removal of sm-notify.pid to nfslock init script.
- Changed spec file to use condrestart instead of condstop
  when calling init scripts.
- Fixed typo in rpc.mountd man page 
- Turn on 'nohide' automatically for all refer exports (bz 313561)

* Tue Dec 04 2007 Release Engineering <rel-eng at fedoraproject dot org> - 1.1.0-7
 - Rebuild for openldap bump

* Wed Oct 17 2007 Steve Dickson <steved@redhat.com>  1.1.0-6
- Switch the libgssapi dependency to libgssglue

* Fri Sep 14 2007 Steve Dickson <steved@redhat.com>  1.1.0-5
- Changed the default paths in sm-notify to 
  /var/lib/nfs/statd (bz 258461)
- Updated exportfs manpage (bz 262861)

* Wed Aug 15 2007 Steve Dickson <steved@redhat.com>  1.1.0-4
- Make sure the open() system calling in exportfs uses
  mode bits when creating the etab file (bz 252440).

* Mon Aug 13 2007 Steve Dickson <steved@redhat.com>  1.1.0-3
- Added nosharecache mount option which re-enables
  rw/ro mounts to the same server (bz 243913).

* Thu Aug  2 2007 Steve Dickson <steved@redhat.com>  1.1.0-2
- Make sure the gss and idmap daemons remove thier lock
  files when they are stopped.

* Sat Jul 28 2007 Steve Dickson <steved@redhat.com>  1.1.0-1
- Upgraded to the latest upstream version (nfs-utils-1.1.0)

* Thu May 24 2007 Steve Dickson <steved@redhat.com> 1.0.10-7
- Fixed typo in mount.nfs4 that causes a segfault during
  error processing (bz 241190)

* Tue May 22 2007 Steve Dickson <steved@redhat.com> 1.0.10-6
- Make sure the condrestarts exit with a zero value (bz 240225)
- Stopped /etc/sysconfig/nfs from being overwritten on updates (bz 234543)
- Added -o nordirplus mount option to disable READDIRPLUS (bz 240357)
- Disabled the FSCache patch, for now... 

* Wed May 10 2007 Steve Dickson <steved@redhat.com> 1.0.12-5
- Fix mount.nfs4 to display correct error message (bz 227212)
- Updated mountd and showmount reverse lookup flags (bz 220772)
- Eliminate timeout on nfsd shutdowns (bz 222001)
- Eliminate memory leak in mountd (bz 239536)
- Make sure statd uses correct uid/gid by chowning
  the /var/lib/nfs/statd with the rpcuser id. (bz 235216)
- Correct some sanity checking in rpc.nfsd. (bz 220887) 
- Added missing unlock_mtab() call in moutnd
- Have mountd hold open etab file to force inode number to change (bz 236823)
- Create a /etc/sysconfig/nfs with all the possible init script
  variables (bz 234543)
- Changed nfs initscript to exit with correct value (bz 221874)

* Tue Apr  3 2007 Steve Dickson <steved@redhat.com> 1.0.12-4
- Replace portmap dependency with an rpcbind dependency (bz 228894)

* Mon Mar 12 2007 Steve Dickson <steved@redhat.com> 1.0.12-3
- Incorporated Merge Review comments (bz 226198)

* Fri Mar  9 2007 Steve Dickson <steved@redhat.com> 1.0.12-2
- Added condstop to all the initscripts (bz 196934)
- Made no_subtree_check a default export option (bz 212218)

* Tue Mar  6 2007 Steve Dickson <steved@redhat.com> 1.0.12-1
- Upgraded to 1.0.12 
- Fixed typo in Summary.

* Thu Mar  1 2007 Karel Zak <kzak@redhat.com>  1.0.11-2
- Fixed mount.nfs -f (fake) option (bz 227988)

* Thu Feb 22 2007 Steve Dickson <steved@redhat.com> 1.0.11-1
- Upgraded to 1.0.11 

* Wed Feb 21 2007 Steve Dickson <steved@redhat.com> 1.0.10-7
- Added FS_Location support

* Mon Dec 18 2006 Karel Zak <kzak@redhat.com> 1.0.10-6
- add support for mount options that contain commas (bz 219645)

* Wed Dec 13 2006 Steve Dickson <steved@redhat.com> 1.0.10-5
- Stopped v4 umounts from ping rpc.mountd (bz 215553)

* Wed Nov 28 2006 Steve Dickson <steved@redhat.com> 1.0.10-4
- Doing a connect on UDP sockets causes the linux network
  stack to reject UDP patches from multi-home server with
  nic on the same subnet. (bz 212471)

* Wed Nov 15 2006 Steve Dickson <steved@redhat.com> 1.0.10-3
- Removed some old mounting versioning code that was
  stopping tcp mount from working (bz 212471)

* Tue Oct 31 2006 Steve Dickson <steved@redhat.com> 1.0.10-2
- Fixed -o remount (bz 210346)
- fix memory leak in rpc.idmapd (bz 212547)
- fix use after free bug in dirscancb (bz 212547)
- Made no_subtree_check a default export option (bz 212218)

* Wed Oct 25 2006 Steve Dickson <steved@redhat.com> 1.0.10-1
- Upgraded to 1.0.10 

* Mon Oct 16 2006 Steve Dickson <steved@redhat.com> 1.0.9-10
- Fixed typo in nfs man page (bz 210864).

* Fri Oct 13 2006 Steve Dickson <steved@redhat.com> 1.0.9-9
- Unable to mount NFS V3 share where sec=none is specified (bz 210644)

* Tue Sep 26 2006 Steve Dickson <steved@redhat.com> 1.0.9-8
- mount.nfs was not returning a non-zero exit value 
  on failed mounts (bz 206705)

* Wed Sep 20 2006 Karel Zak <kzak@redhat.com> 1.0.9-7
- Added support for the mount -s (sloppy) option (#205038)
- Added nfs.5 man page from util-linux
- Added info about [u]mount.nfs to the package description

* Mon Sep 11 2006  <SteveD@RedHat.com> 1.0.9-6
- Removed the compiling of getiversion and getkversion since
  UTS_RELEASE is no longer defined and these binary are
  not installed.

* Fri Aug 18 2006 <SteveD@RedHat.com> 1.0.9-5
- Changed gssd daemons to cache things in memory
  instead of /tmp which makes selinux much happier.
  (bz 203078)

* Wed Aug 16 2006 <SteveD@RedHat.com> 1.0.9-4
- Allow variable for HA callout program in /etc/init.d/nfslock
  (bz 202790)

* Wed Aug 02 2006 <wtogami@redhatcom> 1.0.9-3
- add epoch (#196359)

* Fri Jul 28 2006 <SteveD@RedHat.com> 1.0.9-2
- Enabled the creating of mount.nfs and umount.nfs binaries
- Added mount option fixes suggested by upstream.
- Fix lazy umounts (bz 169299)
- Added -o fsc mount option.

* Mon Jul 24 2006 <SteveD@RedHat.com> 1.0.9-1
- Updated to 1.0.9 release

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1:1.0.8-5.1
- rebuild

* Sun Jul  2 2006 <jkeating@redhat.com> 1:1.0.8-5
- Introduce epoch to fix upgrade path

* Sat Jul  1 2006 <SteveD@RedHat.com> 1.0.8-3
- Fixed typos in /etc/rc.d/init.d/nfs file (bz 184486)

* Fri Jun 30 2006 <SteveD@RedHat.com> 1.0.8-3
- Split the controlling of nfs version, ports, and protocol 
  into two different patches
- Fixed and added debugging statements to rpc.mountd.
- Fixed -p arg to work with priviledged ports (bz 156655)
- Changed nfslock initscript to set LOCKD_TCPPORT and
  LOCKD_UDPPORT (bz 162133)
- Added MOUNTD_NFS_V1 variable to version 1 of the
  mount protocol can be turned off. (bz 175729)
- Fixed gssd to handel mixed case characters in
  the domainname. (bz 186069)

* Wed Jun 21 2006 <SteveD@RedHat.com> 1.0.8-2
- Updated to nfs-utils-1.0.8

* Thu Jun  8 2006 <SteveD@RedHat.com> 1.0.8.rc4-1
- Upgraded to the upstream 1.0.8.rc4 version

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.0.8.rc2-4.FC5.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.0.8.rc2-4.FC5.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Jan 20 2006 Steve Dickson <SteveD@RedHat.com> 1.0.8.rc2-4.FC5
- Added new libnfsidmap call, nfs4_set_debug(), to rpc.idmapd
  which turns on debugging in the libarary.

* Mon Jan 16 2006 Steve Dickson <SteveD@RedHat.com> 1.0.8.rc2-3.FC5
- Added innetgr patch that changes configure scripts to 
  check for the innetgr function. (bz 177899)

* Wed Jan 11 2006 Peter Jones <pjones@redhat.com> 1.0.8.rc2-2.FC5
- Fix lockfile naming in the initscripts so they're stopped correctly.

* Mon Jan  9 2006 Steve Dickson <SteveD@RedHat.com> 1.0.8.rc2-1.FC5
- Updated to 1.0.8-rc2 release
- Broke out libgssapi into its own rpm
- Move librpcsecgss and libnfsidmap in the new nfs-utils-lib rpm
- Removed libevent code; Required to be installed.

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Sun Oct 23 2005 Steve Dickson <SteveD@RedHat.com> 1.0.7-19
- Updated to latest code in SourceForge CVS
- Updated to latest CITI patches (1.0.7-4)
- Fix bug in nfsdreopen by compiling in server defaults

* Thu Sep 22 2005 Steve Dickson <SteveD@RedHat.com> 1.0.7-18
- Updated libnfsidmap to 0.11
- Updated libgssapi to 0.5
- Made sure the gss daemons and new libs are
  all using the same include files.
- Removed code from the tree that is no longer used.
- Add ctlbits patch that introduced the -N -T and -U
  command line flags to rpc.nfsd.

* Sun Sep 18 2005 Steve Dickson <SteveD@RedHat.com> 1.0.7-17
- Updated to latest nfs-utils code in upstream CVS tree
- Updated libevent from 1.0b to 1.1a
- Added libgssapi-0.4 and librpcsecgss-0.6 libs from CITI

* Tue Sep  8 2005 Steve Dickson <SteveD@RedHat.com> 1.0.7-16
- Reworked the nfslock init script so if lockd is running
  it will be killed which is what the HA community needs. (bz 162446)
- Stopped rpcidmapd.init from doing extra echoing when
  condstart-ed.

* Wed Aug 24 2005 Peter Jones <pjones@redhat.com> - 1.0.7-15
- don't strip during "make install", so debuginfo packages are generated right

* Thu Aug 18 2005 Florian La Roche <laroche@redhat.com>
- no need to still keep a requirement for kernel-2.2 or newer

* Tue Aug 16 2005 Steve Dickson <SteveD@RedHat.com> 1.0.7-13
- Changed mountd to use stat64() (bz 165062)

* Tue Aug  2 2005 Steve Dickson <SteveD@RedHat.com> 1.0.7-12
- Changed useradd to use new -l flag (bz149407)
- 64bit fix in gssd code (bz 163139)
- updated broken dependencies
- updated rquotad to compile with latest
  quota version.

* Thu May 26 2005 Steve Dickson <SteveD@RedHat.com> 1.0.7-8
- Fixed subscripting problem in idmapd (bz 158188)

* Thu May 19 2005 Steve Dickson <SteveD@RedHat.com> 1.0.7-7
- Fixed buffer overflow in rpc.svcgssd (bz 114288)

* Wed Apr 13 2005 Steve Dickson <SteveD@RedHat.com> 1.0.7-6
- Fixed misformated output from nfslock script (bz 154648)

* Mon Mar 29 2005 Steve Dickson <SteveD@RedHat.com> 1.0.7-4
- Fixed a compile error on x86_64 machines in the gss code.
- Updated the statd-notify-hostname.patch to eliminate 
  a segmentation fault in rpc.statd when an network 
  interface was down. (bz 151828)

* Sat Mar 19 2005 Steve Dickson <SteveD@RedHat.com> 1.0.7-3
- Changed xlog to use LOG_INFO instead of LOG_DEBUG
  so debug messages will appear w/out any config
  changes to syslog.conf.
- Reworked how /etc/exports is setup (bz 151389)

* Wed Mar  2 2005 Steve Dickson <SteveD@RedHat.com> 1.0.7-2
- Tied the rpcsecgss debugging in with gssd and
  svcgssd debugging

* Mon Feb 14 2005 Steve Dickson <SteveD@RedHat.com>
- Added support to rpcgssd.init and rpcsvcgssd.init scripts
  to insmod security modules.
- Changed the nfs.init script to bring rpc.svcgssd up and down,
  since rpc.svcgssd is only needed with the NFS server is running.

* Tue Dec 14 2004 Steve Dickson <SteveD@RedHat.com>
- Fix problem in idmapd that was causing "xdr error 10008"
  errors (bz 142813)
- make sure the correct hostname is used in the SM_NOTIFY
  message that is sent from a rebooted server which has 
  multiple network interfaces. (bz 139101)

- Changed nfslock to send lockd a -KILL signal
  when coming down. (bz 125257)

* Thu Nov 11 2004 Steve Dickson <SteveD@RedHat.com>
- Replaced a memcopy with explicit assignments
  in getquotainfo() of rquotad to fix potential overflow
  that can occur on 64bit machines. (bz 138068)

* Mon Nov  8 2004 Steve Dickson <SteveD@RedHat.com>
- Updated to latest sourceforge code
- Updated to latest CITIT nfs4 patches

* Sun Oct 17 2004 Steve Dickson <SteveD@RedHat.com>
- Changed nfs.init to bring down rquotad correctly
  (bz# 136041)

* Thu Oct 14 2004 Steve Dickson <SteveD@RedHat.com>
- Added "$RQUOTAD_PORT" variable to nfs.init which
  allows the rpc.rquotad to use a predefined port
  (bz# 124676)

* Fri Oct  1 2004 <SteveD@RedHat.com
- Incorporate some clean up code from Ulrich Drepper (bz# 134025)
- Fixed the chkconfig number in the rpcgssd, rpcidmapd, and 
  rpcsvcgssd initscrpts (bz# 132284)

* Fri Sep 24 2004 <SteveD@RedHat.com>
- Make sure the uid/gid of nfsnobody is the
  correct value for all archs (bz# 123900)
- Fixed some security issues found by SGI (bz# 133556)

* Mon Aug 30 2004 Steve Dickson <SteveD@RedHat.com>
- Major clean up. 
- Removed all unused/old patches
- Rename and condensed a number of patches
- Updated to CITI's nfs-utils-1.0.6-13 patches

* Tue Aug 10 2004 Bill Nottingham <notting@redhat.com>
- move if..fi condrestart stanza to %%postun (#127914, #128601)

* Wed Jun 16 2004 <SteveD@RedHat.com>
- nfslock stop is now done on package removals
- Eliminate 3 syslog messages that are logged for
  successful events.

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Jun 14 2004 <SteveD@RedHat.com>
- Fixed syntax error in nfs initscripts when
  NETWORKING is not defined
- Removed sync warning on readonly exports.
- Changed run levels in rpc initscripts.
- Replaced modinfo with lsmod when checking
  for loaded modules.

* Tue Jun  1 2004 <SteveD@RedHat.com>
- Changed the rpcgssd init script to ensure the 
  rpcsec_gss_krb5 module is loaded

* Tue May 18 2004 <SteveD@RedHat.com>
- Removed the auto option from MOUNTD_NFS_V2 and
  MOUNTD_NFS_V3 variables. Since v2 and v3 are on
  by default, there only needs to be away of 
  turning them off.

* Thu May 10 2004 <SteveD@RedHat.com>
- Rebuilt

* Thu Apr 15 2004 <SteveD@RedHat.com>
- Changed the permission on idmapd.conf to 644
- Added mydaemon code to svcgssd
- Updated the add_gssd.patch from upstream

* Wed Apr 14 2004 <SteveD@RedHat.com>
- Created a pipe between the parent and child so 
  the parent process can report the correct exit
  status to the init scripts
- Added SIGHUP processing to rpc.idmapd and the 
  rpcidmapd init script.

* Mon Mar 22 2004 <SteveD@RedHat.com>
- Make sure check_new_cache() is looking in the right place 

* Wed Mar 17 2004 <SteveD@RedHat.com>
- Changed the v4 initscripts to use $prog for the
  arugment to daemon

* Tue Mar 16 2004 <SteveD@RedHat.com>
- Made the nfs4 daemons initscripts work better when 
  sunrpc is not a module
- added more checks to see if modules are being used.

* Mon Mar 15 2004 <SteveD@RedHat.com>
- Add patch that sets up gssapi_mech.conf correctly

* Fri Mar 12 2004 <SteveD@RedHat.com>
- Added the shutting down of the rpc v4 daemons.
- Updated the Red Hat only patch with some init script changes.

* Thu Mar 11 2004 Bill Nottingham <notting@redhat.com>
- rpc_pipefs mounting and aliases are now in modutils; require that

* Thu Mar 11 2004 <SteveD@RedHat.com>
- Updated the gssd patch.

* Sun Mar  7 2004 <SteveD@RedHat.com>
- Added the addition and deletion of rpc_pipefs to /etc/fstab
- Added the addition and deletion of module aliases to /etc/modules.conf

* Mon Mar  1 2004 <SteveD@RedHat.com>
- Removed gssd tarball and old nfsv4 patch.
- Added new nfsv4 patches that include both the
   gssd and idmapd daemons
- Added redhat-only v4 patch that reduces the
   static librpc.a to only contain gss rpc related
   routines (I would rather have gssd use the glibc 
   rpc routines)
-Changed the gssd svcgssd init scripts to only
   start up if SECURE_NFS is set to 'yes' in
   /etc/sysconfig/nfs

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Feb 12 2004 Thomas Woerner <twoerner@redhat.com>
- make rpc.lockd, rpc.statd, rpc.mountd and rpc.nfsd pie

* Wed Jan 28 2004 Steve Dickson <SteveD@RedHat.com>
- Added the NFSv4 bits

* Mon Dec 29 2003 Steve Dickson <SteveD@RedHat.com>
- Added the -z flag to nfsstat

* Wed Dec 24 2003  Steve Dickson <SteveD@RedHat.com>
- Fixed lockd port setting in nfs.int script

* Wed Oct 22 2003 Steve Dickson <SteveD@RedHat.com>
- Upgrated to 1.0.6
- Commented out the acl path for fedora

* Thu Aug  27 2003 Steve Dickson <SteveD@RedHat.com>
- Added the setting of lockd ports via sysclt interface
- Removed queue setting code since its no longer needed

* Thu Aug  7 2003 Steve Dickson <SteveD@RedHat.com>
- Added back the acl patch Taroon b2

* Wed Jul 23 2003 Steve Dickson <SteveD@RedHat.com>
- Commented out the acl patch (for now)

* Wed Jul 21 2003 Steve Dickson <SteveD@RedHat.com>
- Upgrated to 1.0.5

* Wed Jun 18 2003 Steve Dickson <SteveD@RedHat.com>
- Added security update
- Fixed the drop-privs.patch which means the chroot
patch could be removed.

* Mon Jun  9 2003 Steve Dickson <SteveD@RedHat.com>
- Defined the differ kinds of debugging avaliable for mountd in
the mountd man page. 

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun  3 2003 Steve Dickson <SteveD@RedHat.com>
- Upgraded to 1.0.3 
- Fixed numerous bugs in init scrips
- Added nfsstat overflow patch

* Thu Jan 23 2003 Tim Powers <timp@redhat.com> 1.0.1-2.9
- rebuild

* Fri Dec 13 2002 Daniel J Walsh <dwalsh@redhat.com>
- change init script to not start rpc.lock if already running

* Wed Dec 11 2002 Daniel J Walsh <dwalsh@redhat.com>
- Moved access code to be after dropping privs

* Mon Nov 18 2002 Stephen C. Tweedie <sct@redhat.com>
- Build with %%configure
- Add nhfsgraph, nhfsnums and nhfsrun to the files list

* Mon Nov 11 2002 Stephen C. Tweedie <sct@redhat.com>
- Don't drop privs until we've bound the notification socket

* Thu Nov  7 2002 Stephen C. Tweedie <sct@redhat.com>
- Ignore SIGPIPE in rpc.mountd

* Thu Aug  1 2002 Bob Matthews <bmatthews@redhat.com>
- Add Sean O'Connell's <sean@ee.duke.edu> nfs control tweaks
- to nfs init script.

* Mon Jul 22 2002 Bob Matthews <bmatthews@redhat.com>
- Move to nfs-utils-1.0.1

* Mon Feb 18 2002 Bob Matthews <bmatthews@redhat.com>
- "service nfs restart" should start services even if currently 
-   not running (#59469)
- bump version to 0.3.3-4

* Wed Oct  3 2001 Bob Matthews <bmatthews@redhat.com>
- Move to nfs-utils-0.3.3
- Make nfsnobody a system account (#54221)

* Tue Aug 21 2001 Bob Matthews <bmatthews@redhat.com>
- if UID 65534 is unassigned, add user nfsnobody (#22685)

* Mon Aug 20 2001 Bob Matthews <bmatthews@redhat.com>
- fix typo in nfs init script which prevented MOUNTD_PORT from working (#52113)

* Tue Aug  7 2001 Bob Matthews <bmatthews@redhat.com>
- nfs init script shouldn't fail if /etc/exports doesn't exist (#46432)

* Fri Jul 13 2001 Bob Matthews <bmatthews@redhat.com>
- Make %%pre useradd consistent with other Red Hat packages.

* Tue Jul 03 2001 Michael K. Johnson <johnsonm@redhat.com>
- Added sh-utils dependency for uname -r in nfs init script

* Tue Jun 12 2001 Bob Matthews <bmatthews@redhat.com>
- make non RH kernel release strings scan correctly in 
-   nfslock init script (#44186)

* Mon Jun 11 2001 Bob Matthews <bmatthews@redhat.com>
- don't install any rquota pages in _mandir: (#39707, #44119)
- don't try to manipulate rpc.rquotad in init scripts 
-   unless said program actually exists: (#43340)

* Tue Apr 10 2001 Preston Brown <pbrown@redhat.com>
- don't translate initscripts for 6.x

* Tue Apr 10 2001 Michael K. Johnson <johnsonm@redhat.com>
- do not start lockd on kernel 2.2.18 or higher (done automatically)

* Fri Mar 30 2001 Preston Brown <pbrown@redhat.com>
- don't use rquotad from here now; quota package contains a version that 
  works with 2.4 (#33738)

* Tue Mar 12 2001 Bob Matthews <bmatthews@redhat.com>
- Statd logs at LOG_DAEMON rather than LOG_LOCAL5
- s/nfs/\$0/ where appropriate in init scripts

* Tue Mar  6 2001 Jeff Johnson <jbj@redhat.com>
- Move to nfs-utils-0.3.1

* Wed Feb 14 2001 Bob Matthews <bmatthews@redhat.com>
- #include <time.h> patch

* Mon Feb 12 2001 Bob Matthews <bmatthews@redhat.com>
- Really enable netgroups

* Mon Feb  5 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- i18nize initscripts

* Fri Jan 19 2001 Bob Matthews <bmatthews@redhat.com>
- Increased {s,r}blen in rpcmisc.c:makesock to accommodate eepro100

* Tue Jan 16 2001 Bob Matthews <bmatthews@redhat.com>
- Hackish fix in build section to enable netgroups

* Wed Jan  3 2001 Bob Matthews <bmatthews@redhat.com>
- Fix incorrect file specifications in statd manpage.
- Require gawk 'cause it's used in nfslock init script.

* Thu Dec 13 2000 Bob Matthews <bmatthews@redhat.com>
- Require sed because it's used in nfs init script

* Tue Dec 12 2000 Bob Matthews <bmatthews@redhat.com>
- Don't do a chroot(2) after dropping privs, in statd.

* Mon Dec 11 2000 Bob Matthews <bmatthews@redhat.com>
- NFSv3 if kernel >= 2.2.18, detected in init script

* Thu Nov 23 2000 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 0.2.1

* Tue Nov 14 2000 Bill Nottingham <notting@redhat.com>
- don't start lockd on 2.4 kernels; it's unnecessary

* Tue Sep  5 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- more portable fix for mandir

* Sun Sep  3 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- update to 0.2-release

* Fri Sep  1 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- fix reload script

* Thu Aug 31 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- update to 0.2 from CVS
- adjust statd-drop-privs patch
- disable tcp_wrapper support

* Wed Aug  2 2000 Bill Nottingham <notting@redhat.com>
- fix stop priority of nfslock

* Tue Aug  1 2000 Bill Nottingham <notting@redhat.com>
- um, actually *include and apply* the statd-drop-privs patch

* Mon Jul 24 2000 Bill Nottingham <notting@redhat.com>
- fix init script ordering (#14502)

* Sat Jul 22 2000 Bill Nottingham <notting@redhat.com>
- run statd chrooted and as non-root
- add prereqs

* Tue Jul 18 2000 Trond Eivind Glomsrød <teg@redhat.com>
- use "License", not "Copyright"
- use %%{_tmppath} and %%{_mandir}

* Mon Jul 17 2000 Matt Wilson <msw@redhat.com>
- built for next release

* Mon Jul 17 2000 Matt Wilson <msw@redhat.com>
- 0.1.9.1
- remove patch0, has been integrated upstream

* Wed Feb  9 2000 Bill Nottingham <notting@redhat.com>
- the wonderful thing about triggers, is triggers are wonderful things...

* Thu Feb 03 2000 Cristian Gafton <gafton@redhat.com>
- switch to nfs-utils as the base tree
- fix the statfs patch for the new code base
- single package that obsoletes everything we had before (if I am to keep
  some traces of my sanity with me...)

* Mon Jan 17 2000 Preston Brown <pbrown@redhat.com>
- use statfs syscall instead of stat to determinal optimal blksize
