# Conditionals
# Invoke "rpmbuild --without <feature>" or "rpmbuild --with <feature>"
# to disable or enable specific features
%bcond_with testagents
%bcond_with watchdog
%bcond_with monitoring
%bcond_without snmp
%bcond_without dbus
# no InfiniBand stack on s390(x)
%ifnarch s390 s390x
%bcond_without rdma
%endif
%bcond_without systemd
%bcond_with upstart
%bcond_without xmlconf
%bcond_without runautogen

%global gitver %{?numcomm:.%{numcomm}}%{?alphatag:.%{alphatag}}%{?dirty:.%{dirty}}
%global gittarver %{?numcomm:.%{numcomm}}%{?alphatag:-%{alphatag}}%{?dirty:-%{dirty}}

Name: corosync
Summary: The Corosync Cluster Engine and Application Programming Interfaces
Version: 2.3.5
Release: 3%{?gitver}%{?dist}
License: BSD
Group: System Environment/Base
URL: http://www.corosync.org/
Source0: http://corosync.org/download/%{name}-%{version}%{?gittarver}.tar.gz

%if 0%{?rhel}
ExclusiveArch: i686 x86_64
%endif

# Runtime bits
Requires: corosynclib = %{version}-%{release}
Requires(pre): /usr/sbin/useradd
Requires(post): /sbin/chkconfig
Requires(preun): /sbin/chkconfig
Obsoletes: openais, openais-devel, openaislib, openaislib-devel
Obsoletes: cman, clusterlib, clusterlib-devel

# Build bits

BuildRequires: groff
BuildRequires: libqb-devel >= 0.14.2
BuildRequires: nss-devel
%if %{with runautogen}
BuildRequires: autoconf automake libtool
%endif
%if %{with monitoring}
BuildRequires: libstatgrab-devel
%endif
%if %{with rdma}
BuildRequires: libibverbs-devel librdmacm-devel
%endif
%if %{with snmp}
BuildRequires: net-snmp-devel
%endif
%if %{with dbus}
BuildRequires: dbus-devel
%endif
%if %{with systemd}
BuildRequires: systemd-units
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
%endif
%if %{with xmlconf}
Requires: libxslt
%endif

BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%prep
%setup -q -n %{name}-%{version}%{?gittarver}

%build
%if %{with runautogen}
./autogen.sh
%endif

%if %{with rdma}
export ibverbs_CFLAGS=-I/usr/include/infiniband \
export ibverbs_LIBS=-libverbs \
export rdmacm_CFLAGS=-I/usr/include/rdma \
export rdmacm_LIBS=-lrdmacm \
%endif
%{configure} \
%if %{with testagents}
	--enable-testagents \
%endif
%if %{with watchdog}
	--enable-watchdog \
%endif
%if %{with monitoring}
	--enable-monitoring \
%endif
%if %{with snmp}
	--enable-snmp \
%endif
%if %{with dbus}
	--enable-dbus \
%endif
%if %{with rdma}
	--enable-rdma \
%endif
%if %{with systemd}
	--enable-systemd \
%endif
%if %{with upstart}
	--enable-upstart \
%endif
%if %{with xmlconf}
	--enable-xmlconf \
%endif
	--with-initddir=%{_initrddir} \
	--with-systemddir=%{_unitdir} \
	--with-upstartdir=%{_sysconfdir}/init

make %{_smp_mflags}

%install
rm -rf %{buildroot}

make install DESTDIR=%{buildroot}

%if %{with dbus}
mkdir -p -m 0700 %{buildroot}/%{_sysconfdir}/dbus-1/system.d
install -m 644 %{_builddir}/%{name}-%{version}%{?gittarver}/conf/corosync-signals.conf %{buildroot}/%{_sysconfdir}/dbus-1/system.d/corosync-signals.conf
%endif

## tree fixup
# drop static libs
rm -f %{buildroot}%{_libdir}/*.a
rm -f %{buildroot}%{_libdir}/*.la
# drop docs and html docs for now
rm -rf %{buildroot}%{_docdir}/*
# /etc/sysconfig/corosync-notifyd
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
install -m 644 tools/corosync-notifyd.sysconfig.example \
   %{buildroot}%{_sysconfdir}/sysconfig/corosync-notifyd

%clean
rm -rf %{buildroot}

%description
This package contains the Corosync Cluster Engine Executive, several default
APIs and libraries, default configuration files, and an init script.

%post
%if %{with systemd} && 0%{?systemd_post:1}
%systemd_post corosync.service
%else
if [ $1 -eq 1 ]; then
	/sbin/chkconfig --add corosync || :
fi
%endif

%preun
%if %{with systemd} && 0%{?systemd_preun:1}
%systemd_preun corosync.service
%else
if [ $1 -eq 0 ]; then
	/sbin/service corosync stop &>/dev/null || :
	/sbin/chkconfig --del corosync || :
fi
%endif

%postun
%if %{with systemd} && 0%{?systemd_postun:1}
%systemd_postun
%endif

%files
%defattr(-,root,root,-)
%doc LICENSE SECURITY
%{_sbindir}/corosync
%{_sbindir}/corosync-keygen
%{_sbindir}/corosync-cmapctl
%{_sbindir}/corosync-cfgtool
%{_sbindir}/corosync-cpgtool
%{_sbindir}/corosync-quorumtool
%{_sbindir}/corosync-notifyd
%{_bindir}/corosync-blackbox
%if %{with xmlconf}
%{_bindir}/corosync-xmlproc
%config(noreplace) %{_sysconfdir}/corosync/corosync.xml.example
%dir %{_datadir}/corosync
%{_datadir}/corosync/xml2conf.xsl
%{_mandir}/man8/corosync-xmlproc.8*
%{_mandir}/man5/corosync.xml.5*
%endif
%dir %{_sysconfdir}/corosync
%dir %{_sysconfdir}/corosync/uidgid.d
%config(noreplace) %{_sysconfdir}/corosync/corosync.conf.example
%config(noreplace) %{_sysconfdir}/corosync/corosync.conf.example.udpu
%config(noreplace) %{_sysconfdir}/sysconfig/corosync-notifyd
%{_sysconfdir}/logrotate.d/corosync
%if %{with dbus}
%{_sysconfdir}/dbus-1/system.d/corosync-signals.conf
%endif
%if %{with snmp}
%{_datadir}/snmp/mibs/COROSYNC-MIB.txt
%endif
%if %{with systemd}
%{_unitdir}/corosync.service
%{_unitdir}/corosync-notifyd.service
%dir %{_datadir}/corosync
%{_datadir}/corosync/corosync
%{_datadir}/corosync/corosync-notifyd
%else
%{_initrddir}/corosync
%{_initrddir}/corosync-notifyd
%endif
%if %{with upstart}
%{_sysconfdir}/init/corosync.conf
%{_sysconfdir}/init/corosync-notifyd.conf
%endif
%dir %{_localstatedir}/lib/corosync
%dir %{_localstatedir}/log/cluster
%{_mandir}/man8/corosync_overview.8*
%{_mandir}/man8/corosync.8*
%{_mandir}/man8/corosync-blackbox.8*
%{_mandir}/man8/corosync-cmapctl.8*
%{_mandir}/man8/corosync-keygen.8*
%{_mandir}/man8/corosync-cfgtool.8*
%{_mandir}/man8/corosync-cpgtool.8*
%{_mandir}/man8/corosync-notifyd.8*
%{_mandir}/man8/corosync-quorumtool.8*
%{_mandir}/man5/corosync.conf.5*
%{_mandir}/man5/votequorum.5*
%{_mandir}/man8/cmap_keys.8*

# optional testagent rpm
#
%if %{with testagents}

%package -n corosync-testagents
Summary: The Corosync Cluster Engine Test Agents
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: libqb >= 0.14.2

%description -n corosync-testagents
This package contains corosync test agents.

%files -n corosync-testagents
%defattr(755,root,root,-)
%{_datadir}/corosync/tests/mem_leak_test.sh
%{_datadir}/corosync/tests/net_breaker.sh
%{_datadir}/corosync/tests/cmap-dispatch-deadlock.sh
%{_datadir}/corosync/tests/shm_leak_audit.sh
%{_bindir}/cpg_test_agent
%{_bindir}/sam_test_agent
%{_bindir}/votequorum_test_agent

%endif

# library
#
%package -n corosynclib
Summary: The Corosync Cluster Engine Libraries
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}

%description -n corosynclib
This package contains corosync libraries.

%files -n corosynclib
%defattr(-,root,root,-)
%doc LICENSE
%{_libdir}/libcfg.so.*
%{_libdir}/libcpg.so.*
%{_libdir}/libcmap.so.*
%{_libdir}/libtotem_pg.so.*
%{_libdir}/libquorum.so.*
%{_libdir}/libvotequorum.so.*
%{_libdir}/libsam.so.*
%{_libdir}/libcorosync_common.so.*

%post -n corosynclib -p /sbin/ldconfig

%postun -n corosynclib -p /sbin/ldconfig

%package -n corosynclib-devel
Summary: The Corosync Cluster Engine Development Kit
Group: Development/Libraries
Requires: corosynclib = %{version}-%{release}
Requires: pkgconfig
Provides: corosync-devel = %{version}
Obsoletes: corosync-devel < 0.92-7

%description -n corosynclib-devel
This package contains include files and man pages used to develop using
The Corosync Cluster Engine APIs.

%files -n corosynclib-devel
%defattr(-,root,root,-)
%doc LICENSE
%dir %{_includedir}/corosync/
%{_includedir}/corosync/corodefs.h
%{_includedir}/corosync/cfg.h
%{_includedir}/corosync/cmap.h
%{_includedir}/corosync/corotypes.h
%{_includedir}/corosync/cpg.h
%{_includedir}/corosync/hdb.h
%{_includedir}/corosync/sam.h
%{_includedir}/corosync/quorum.h
%{_includedir}/corosync/votequorum.h
%dir %{_includedir}/corosync/totem/
%{_includedir}/corosync/totem/totem.h
%{_includedir}/corosync/totem/totemip.h
%{_includedir}/corosync/totem/totempg.h
%{_libdir}/libcfg.so
%{_libdir}/libcpg.so
%{_libdir}/libcmap.so
%{_libdir}/libtotem_pg.so
%{_libdir}/libquorum.so
%{_libdir}/libvotequorum.so
%{_libdir}/libsam.so
%{_libdir}/libcorosync_common.so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/cpg_*3*
%{_mandir}/man3/quorum_*3*
%{_mandir}/man3/votequorum_*3*
%{_mandir}/man3/sam_*3*
%{_mandir}/man8/cpg_overview.8*
%{_mandir}/man8/votequorum_overview.8*
%{_mandir}/man8/sam_overview.8*
%{_mandir}/man3/cmap_*3*
%{_mandir}/man8/cmap_overview.8*
%{_mandir}/man8/quorum_overview.8*

%changelog
* Sat Nov 07 2015 Liu Di <liudidi@gmail.com> - 2.3.5-3
- 为 Magic 3.0 重建

* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 2.3.5-2
- 更新到 2.3.5

* Tue Jan 14 2014 Jan Friesse <jfriesse@redhat.com> - 2.3.3-1
- New upstream release

* Mon Sep 16 2013 Jan Friesse <jfriesse@redhat.com> - 2.3.2-1
- New upstream release

* Mon Aug 19 2013 Jan Friesse <jfriesse@redhat.com> 2.3.1-3
- Resolves: rhbz#998362

- Fix scheduler pause-detection timeout (rhbz#998362)
- merge upstream commit 2740cfd1eac60714601c74df2137fe588b607866 (rhbz#998362)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 10 2013 Jan Friesse <jfriesse@redhat.com> - 2.3.1-1
- New upstream release
- Fix incorrect dates in specfile changelog section

* Mon Mar 25 2013 Jan Friesse <jfriesse@redhat.com> - 2.3.0-3
- Resolves: rhbz#925185

- Run autogen by default

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 18 2013 Jan Friesse <jfriesse@redhat.com> - 2.3.0-1
- New upstream release

* Wed Dec 12 2012 Jan Friesse <jfriesse@redhat.com> - 2.2.0-1
- New upstream release

* Thu Oct 11 2012 Jan Friesse <jfriesse@redhat.com> - 2.1.0-1
- New upstream release

* Fri Aug 3 2012 Steven Dake <sdake@redhat.com> - 2.0.1-3
- add groff as a BuildRequires as it is no longer installed in the buildroot

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 22 2012 Jan Friesse <jfriesse@redhat.com> - 2.0.1-1
- New upstream release

* Tue Apr 17 2012 Fabio M. Di Nitto <fdinitto@redhat.com> - 2.0.0-2
- Backport IPCS fix from master (ack by Steven)

* Tue Apr 10 2012 Jan Friesse <jfriesse@redhat.com> - 2.0.0-1
- New upstream release

* Thu Apr 05 2012 Karsten Hopp <karsten@redhat.com> 1.99.9-1.1
- bump release and rebuild on PPC

* Tue Mar 27 2012 Jan Friesse <jfriesse@redhat.com> - 1.99.9-1
- New upstream release

* Fri Mar 16 2012 Jan Friesse <jfriesse@redhat.com> - 1.99.8-1
- New upstream release

* Tue Mar  6 2012 Jan Friesse <jfriesse@redhat.com> - 1.99.7-1
- New upstream release

* Tue Feb 28 2012 Jan Friesse <jfriesse@redhat.com> - 1.99.6-1
- New upstream release

* Wed Feb 22 2012 Jan Friesse <jfriesse@redhat.com> - 1.99.5-1
- New upstream release

* Tue Feb 14 2012 Jan Friesse <jfriesse@redhat.com> - 1.99.4-1
- New upstream release

* Tue Feb 14 2012 Jan Friesse <jfriesse@redhat.com> - 1.99.3-1
- New upstream release

* Tue Feb  7 2012 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.99.2-1
- New upstream release
- Re-enable xmlconfig bits
- Ship cmap man pages
- Add workaround to usrmove breakage!!

* Thu Feb  2 2012 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.99.1-2
- Add proper Obsoltes on openais/cman/clusterlib

* Wed Feb  1 2012 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.99.1-1
- New upstream release
- Temporary disable xml config (broken upstream tarball)

* Tue Jan 24 2012 Jan Friesse <jfriesse@redhat.com> - 1.99.0-1
- New upstream release

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Oct 06 2011 Jan Friesse <jfriesse@redhat.com> - 1.4.2-1
- New upstream release

* Thu Sep 08 2011 Jan Friesse <jfriesse@redhat.com> - 1.4.1-2
- Add upstream fixes

* Tue Jul 26 2011 Jan Friesse <jfriesse@redhat.com> - 1.4.1-1
- New upstream release

* Wed Jul 20 2011 Jan Friesse <jfriesse@redhat.com> - 1.4.0-2
- Change attributes of cluster log directory

* Tue Jul 19 2011 Jan Friesse <jfriesse@redhat.com> - 1.4.0-1
- New upstream release
- Resync spec file with upstream changes

* Fri Jul 08 2011 Jan Friesse <jfriesse@redhat.com> - 1.3.2-1
- New upstream release

* Tue May 10 2011 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.3.1-1
- New upstream release

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec  2 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.3.0-1
- New upstream release
- drop upstream patch revision-2770.patch now included in release
- update spec file to ship corosync-blackbox

* Thu Sep  2 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.2.8-1
- New upstream release

* Thu Jul 29 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.2.7-1
- New upstream release

* Fri Jul  9 2010 Dan Horák <dan[at]danny.cz> - 1.2.6-2
- no InfiniBand stack on s390(x)

* Mon Jul  5 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.2.6-1
- New upstream release
- Resync spec file with upstream changes

* Tue May 25 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.2.3-1
- New upstream release
- Rediff revision 2770 patch

* Mon May 17 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.2.2-1
- New upstream release
- Add upstream trunk revision 2770 to add cpg_model_initialize api.
- Fix URL and Source0 entries.
- Add workaround to broken 1.2.2 Makefile with make -j.

* Wed Mar 24 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.2.1-1
- New upstream release

* Tue Dec  8 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.2.0-1
- New upstream release
- Use global instead of define
- Update Source0 url
- Use more name macro around
- Cleanup install section. Init script is now installed by upstream
- Cleanup whitespace
- Don't deadlock between package upgrade and corosync condrestart
- Ship service.d config directory
- Fix Conflicts vs Requires
- Ship new sam library and man pages

* Fri Oct 23 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.1.2-1
- New upstream release fixes major regression on specific loads

* Wed Oct 21 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.1.1-1
- New upstream release

* Fri Sep 25 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.1.0-1
- New upstream release
- spec file updates:
  * enable IB support
  * explicitly define built-in features at configure time

* Tue Sep 22 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.0.1-1
- New upstream release
- spec file updates:
  * use proper configure macro

* Tue Jul 28 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.0.0-3
- spec file updates:
  * more consistent use of macros across the board
  * fix directory ownership

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul  8 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.0.0-1
- New upstream release

* Thu Jul  2 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.100-1
- New upstream release

* Sat Jun 20 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.98-1
- New upstream release
- spec file updates:
  * Drop corosync-trunk patch and alpha tag.
  * Fix alphatag vs buildtrunk handling.
  * Drop requirement on ais user/group and stop creating them.
  * New config file locations from upstream: /etc/corosync/corosync.conf.

* Wed Jun 10 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.97-1.svn2233
- spec file updates:
  * Update to svn version 2233 to include library linking fixes

* Wed Jun 10 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.97-1.svn2232
- New upstream release
- spec file updates:
  * Drop pkgconfig fix that's now upstream
  * Update to svn version 2232
  * Define buildtrunk if we are using svn snapshots
  * BuildRequires: nss-devel to enable nss crypto for network communication
  * Force autogen invokation if buildtrunk is defined
  * Whitespace cleanup
  * Stop shipping corosync.conf in favour of a generic example
  * Update file list

* Mon Mar 30 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.95-2
- Backport svn commit 1913 to fix pkgconfig files generation
  and unbreak lvm2 build.

* Tue Mar 24 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.95-1
- New upstream release
- spec file updates:
  * Drop alpha tag
  * Drop local patches (no longer required)
  * Allow to build from svn trunk by supporting rpmbuild --with buildtrunk 
  * BuildRequires autoconf automake if building from trunk
  * Execute autogen.sh if building from trunk and if no configure is available
  * Switch to use rpm configure macro and set standard install paths
  * Build invokation now supports _smp_mflags
  * Remove install section for docs and use proper doc macro instead
  * Add tree fixup bits to drop static libs and html docs (only for now)
  * Add LICENSE file to all subpackages
  * libraries have moved to libdir. Drop ld.so.conf.d corosync file
  * Update BuildRoot usage to preferred versions/names

* Tue Mar 10 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.94-5.svn1797
- Update the corosync-trunk patch for real this time.

* Tue Mar 10 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.94-4.svn1797
- Import fixes from upstream:
  * Cleanup logsys format init around to use default settings (1795)
  * logsys_format_set should use its own internal copy of format_buffer (1796)
  * Add logsys_format_get to logsys API (1797)
- Cherry pick svn1807 to unbreak CPG.

* Mon Mar  9 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.94-3.svn1794
- Import fixes from upstream:
  * Add reserve/release feature to totem message queue space (1793)
  * Fix CG shutdown (1794)

* Fri Mar  6 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.94-2.svn1792
- Import fixes from upstream:
  * Fix uninitialized memory. Spotted by valgrind (1788)
  * Fix logsys_set_format by updating the right bits (1789)
  * logsys: re-add support for timestamp  (1790)
  * Fix cpg crash (1791)
  * Allow logsys_format_set to reset to default (1792)

* Tue Mar  3 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.94-1
- New upstream release.
- Drop obsolete patches.
- Add soname bump patch that was missing from upstream.

* Wed Feb 25 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.93-4
- Add Makefile fix to install all corosync tools (commit r1780)

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.93-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 23 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.93-2
- Rename gcc-4.4 patch to match svn commit (r1767).
- Backport patch from trunk (commit r1774) to fix quorum engine.

* Thu Feb 19 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.93-1
- New upstream release.
- Drop alphatag from spec file.
- Drop trunk patch.
- Update Provides for corosynclib-devel.
- Backport gcc-4.4 build fix from trunk.

* Mon Feb  2 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.92-7.svn1756
- Update to svn trunk at revision 1756 from upstream.
- Add support pkgconfig to devel package.
- Tidy up spec files by re-organazing sections according to packages.
- Split libraries from corosync to corosynclib.
- Rename corosync-devel to corosynclib-devel.
- Comply with multiarch requirements (libraries).

* Tue Jan 27 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.92-6.svn1750
- Update to svn trunk at revision 1750 from upstream.
- Include new quorum service in the packaging.

* Mon Dec 15 2008 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.92-5.svn1709
- Update to svn trunk at revision 1709 from upstream.
- Update spec file to include new include files.

* Wed Dec 10 2008 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.92-4.svn1707
- Update to svn trunk at revision 1707 from upstream.
- Update spec file to include new lcrso services and include file.

* Mon Oct 13 2008 Dennis Gilmore <dennis@ausil.us> - 0.92-3
- remove ExclusiveArch line

* Wed Sep 24 2008 Steven Dake <sdake@redhat.com> - 0.92-2
- Add conflicts for openais and openais-devel packages older then 0.90.

* Wed Sep 24 2008 Steven Dake <sdake@redhat.com> - 0.92-1
- New upstream release corosync-0.92.

* Sun Aug 24 2008 Steven Dake <sdake@redhat.com> - 0.91-3
- move logsys_overview.8.* to devel package.
- move shared libs to main package.

* Wed Aug 20 2008 Steven Dake <sdake@redhat.com> - 0.91-2
- use /sbin/service instead of calling init script directly.
- put corosync-objctl man page in the main package.
- change all initrddir to initddir for fedora 10 guidelines.

* Thu Aug 14 2008 Steven Dake <sdake@redhat.com> - 0.91-1
- First upstream packaged version of corosync for rawhide review.
