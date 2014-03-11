%global gname haclient
%global uname hacluster
%global nogroup nobody

# When downloading directly from Mercurial, it will automatically add this prefix
# Invoking 'hg archive' wont but you can add one with: hg archive -t tgz -p "Reusable-Cluster-Components-" -r $upstreamversion $upstreamversion.tar.gz
%global specversion 9
%global upstreamprefix Reusable-Cluster-Components-
%global upstreamversion 8286b46c91e3

# Keep around for when/if required
#global alphatag %{upstreamversion}.hg

Name:		cluster-glue
Summary:	Reusable cluster components
Version:	1.0.6
Release:	%{?alphatag:0.}%{specversion}%{?alphatag:.%{alphatag}}%{?dist}.2
License:	GPLv2+ and LGPLv2+
Url:		http://linux-ha.org/wiki/Cluster_Glue
Group:		System Environment/Base
Source0:	http://hg.linux-ha.org/glue/archive/%{upstreamversion}.tar.bz2
Source1:	logd.service
Patch1:		glib-everything-or-bust.patch
Requires:	%{name}-libs = %{version}-%{release}

# Directives to allow upgrade from combined heartbeat packages in Fedora11
Provides:	heartbeat-stonith = 3.0.0-1
Provides:	heartbeat-pils = 3.0.0-1
Obsoletes:	heartbeat-stonith < 3.0.0-1
Obsoletes:	heartbeat-pils < 3.0.0-1

## Setup/build bits

BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

# Needed for systemd unit
Requires(post): systemd-sysv
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

# Build dependencies
Requires: perl-TimeDate
BuildRequires: automake autoconf libtool pkgconfig chrpath libtool-ltdl-devel
BuildRequires: bzip2-devel glib2-devel python-devel libxml2-devel
BuildRequires: systemd-units

# For documentation
BuildRequires: libxslt docbook-style-xsl

# For additional Stonith plugins
BuildRequires: net-snmp-devel OpenIPMI-devel libcurl-devel
# openhpi-devel

%if 0%{?fedora} > 11 || 0%{?rhel} > 5
BuildRequires: libuuid-devel
%else
BuildRequires: e2fsprogs-devel
%endif

%prep
%setup -q -n %{upstreamprefix}%{upstreamversion}
%patch1 -p0

./autogen.sh

%{configure}	CFLAGS="${CFLAGS} $(echo '%{optflags}')" \
		--enable-fatal-warnings=no   \
		--localstatedir=%{_var}      \
		--with-daemon-group=%{gname} \
		--with-daemon-user=%{uname}

%build
make %{_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

## tree fix up
# Dont package static libs
find %{buildroot} -name '*.a' -exec rm {} \;
find %{buildroot} -name '*.la' -exec rm {} \;

# Don't package things we wont support
rm -f %{buildroot}/%{_libdir}/stonith/plugins/stonith2/rhcs.*
rm -f %{buildroot}/%{_sbindir}/hb_report

# Nuke sysvinit bits
rm -rf %{buildroot}%{_sysconfdir}/init.d/

# Install systemd bits
mkdir -p %{buildroot}%{_unitdir}
install -m0644 %{SOURCE1} %{buildroot}%{_unitdir}/

magic_rpm_clean.sh

%clean
rm -rf %{buildroot}

# cluster-glue

%description
A collection of common tools that are useful for writing cluster managers 
such as Pacemaker.
Provides a local resource manager that understands the OCF and LSB
standards, and an interface to common STONITH devices.

%post
if [ $1 -eq 1 ] ; then 
    # Initial installation 
    /usr/bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%preun
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /usr/bin/systemctl --no-reload disable logd.service > /dev/null 2>&1 || :
    /usr/bin/systemctl stop logd.service > /dev/null 2>&1 || :
fi

%postun
/usr/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /usr/bin/systemctl try-restart logd.service >/dev/null 2>&1 || :
fi

%triggerun -- cluster-glue < 1.0.6-7
# Save the current service runlevel info
# User must manually run systemd-sysv-convert --apply httpd
# to migrate them to systemd targets
/usr/bin/systemd-sysv-convert --save logd >/dev/null 2>&1 ||:

# Run these because the SysV package being removed won't do them
/usr/sbin/chkconfig --del logd >/dev/null 2>&1 || :
/usr/bin/systemctl try-restart logd.service >/dev/null 2>&1 || :

%files
%defattr(-,root,root)
%{_sbindir}/ha_logger
%{_sbindir}/lrmadmin
%{_sbindir}/meatclient
%{_sbindir}/sbd
%{_sbindir}/stonith
%{_unitdir}/logd.service

%dir %{_libdir}/heartbeat
%dir %{_libdir}/heartbeat/plugins
%dir %{_libdir}/heartbeat/plugins/RAExec
%dir %{_libdir}/heartbeat/plugins/InterfaceMgr
%{_libdir}/heartbeat/lrmd
%{_libdir}/heartbeat/ha_logd
%{_libdir}/heartbeat/plugins/RAExec/*.so
%{_libdir}/heartbeat/plugins/InterfaceMgr/*.so

%dir %{_libdir}/stonith
%dir %{_libdir}/stonith/plugins
%dir %{_libdir}/stonith/plugins/stonith2
%{_datadir}/cluster-glue/ha_log.sh
%{_libdir}/stonith/plugins/external
%{_libdir}/stonith/plugins/stonith2/*.so
%{_libdir}/stonith/plugins/stonith2/*.py*
%{_libdir}/stonith/plugins/xen0-ha-dom0-stonith-helper

%dir %{_datadir}/cluster-glue
%{_datadir}/cluster-glue/ha_cf_support.sh
%{_datadir}/cluster-glue/openais_conf_support.sh
%{_datadir}/cluster-glue/utillib.sh
%{_datadir}/cluster-glue/combine-logs.pl

%dir %{_var}/lib/heartbeat
%dir %{_var}/lib/heartbeat/cores
%dir %attr (0700, root, root)		%{_var}/lib/heartbeat/cores/root
%dir %attr (0700, nobody, %{nogroup})	%{_var}/lib/heartbeat/cores/nobody
%dir %attr (0700, %{uname}, %{gname})	%{_var}/lib/heartbeat/cores/%{uname}

%doc %{_datadir}/doc/cluster-glue/stonith
%doc %{_mandir}/man1/*
%doc %{_mandir}/man8/*
%doc AUTHORS
%doc COPYING

# cluster-glue-libs

%package libs
Summary:	Reusable cluster libraries
Group:		Development/Libraries

%description libs
A collection of libraries that are useful for writing cluster managers 
such as Pacemaker.

%pre
getent group %{gname} >/dev/null || groupadd -r %{gname}
getent passwd %{uname} >/dev/null || \
useradd -r -g %{gname} -d %{_var}/lib/heartbeat/cores/hacluster -s /sbin/nologin \
-c "heartbeat user" %{uname}
exit 0

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files libs
%defattr(-,root,root)
%{_libdir}/lib*.so.*
%doc AUTHORS
%doc COPYING.LIB

# cluster-glue-libs-devel

%package libs-devel
Summary:	Headers and libraries for writing cluster managers
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description libs-devel
Headers and shared libraries for a useful for writing cluster managers 
such as Pacemaker.

%files libs-devel
%defattr(-,root,root)
%dir %{_libdir}/heartbeat
%dir %{_libdir}/heartbeat/plugins
%dir %{_libdir}/heartbeat/plugins/test
%dir %{_datadir}/cluster-glue
%{_libdir}/lib*.so
%{_libdir}/heartbeat/ipctest
%{_libdir}/heartbeat/ipctransientclient
%{_libdir}/heartbeat/ipctransientserver
%{_libdir}/heartbeat/transient-test.sh
%{_libdir}/heartbeat/base64_md5_test
%{_libdir}/heartbeat/logtest
%{_includedir}/clplumbing
%{_includedir}/heartbeat
%{_includedir}/stonith
%{_includedir}/pils
%{_datadir}/cluster-glue/lrmtest
%{_libdir}/heartbeat/plugins/test/test.so

%doc AUTHORS
%doc COPYING
%doc COPYING.LIB

%changelog
* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 1.0.6-9.2
- 为 Magic 3.0 重建

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-9.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec 12 2011 Andrew Beekhof <andrew@beekhof.net> - 1.0.6-9
- Fix compilation now that it is compulsory to include the whole of glib

* Mon Sep 26 2011 Andrew Beekhof <andrew@beekhof.net> - 1.0.6-8
- Allow cluster-glue-libs to be installed independently of cluster-glue

* Thu Sep 15 2011 Tom Callaway <spot@fedoraproject.org> - 1.0.6-7
- convert to systemd

* Thu Aug 04 2011 Andrew Beekhof <andrew@beekhof.net> - 1.0.6-6
- Remove hb_report, people should use crm_report instead

* Thu Aug 04 2011 Andrew Beekhof <andrew@beekhof.net> - 1.0.6-5
- Rebuild for new bzip version

* Mon Jul 11 2011 Andrew Beekhof <andrew@beekhof.net> - 1.0.6-4
- Remove support for openhpi so that we can build

* Mon Jul 11 2011 Andrew Beekhof <andrew@beekhof.net> - 1.0.6-3
- Rebuild for new snmp .so version

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jul 26 2010 Andrew Beekhof <andrew@beekhof.net> - 1.0.6-2
- Rebuild for new snmp .so version

* Mon Jul 26 2010 Andrew Beekhof <andrew@beekhof.net> - 1.0.6-1
  + High: LRM: lrmd,clientlib: asynchronous resource delete notification (lf#2439)
  + High: LRM: lrmd: don't allow cancelled operations to get back to the repeating op list (lf#2417)
  + Medium: stonith: add -E option to get the configuration from the environment

* Wed May 12 2010 Andrew Beekhof <andrew@beekhof.net> - 1.0.5-1
  + High: clplumbing: Add farside_uid and farside_gid info of the user on the other side of socket
  + High: hb_report: do not filter CIB/PE files by default
  + High: LRM: lrmd: don't add the cancel option in flush to the running operations (bnc#578644)
  + High: LRM: lrmd: don't flush operations which don't belong to the requesting client (lf#2161)
  + High: LRM: lrmd: on shutdown exit once all operations finished (lf#2340)
  + High: stonith: external/ibmrsa-telnet: fix expect regex
  + High: stonith: external/ipmi: fix reset
  + High: stonith: external/sbd: fix status operation (thanks to Lars Ellenberg)
  + High: stonith: external/sbd: support heartbeat
  + High: stonith: new external/ippower9258 plugin

* Wed Mar 24 2010 Andrew Beekhof <andrew@beekhof.net> - 1.0.2-3
- Version bump to ensure we're >= fc13

* Mon Jan 11 2010 Andrew Beekhof <andrew@beekhof.net> - 1.0.2-1
- Suppress unsupported stonith plugins
- Update to latest upstream release: aa1f9dee2793
  + High: stonith: add ha_log.sh for external plugins (LF 1971)
  + High: stonith: external plugins log using ha_log.sh (LF 2294)
  + High: stonith: external/dracmc-telnet: new stonith plugin for Dell Drac/MC Blade Enclosure and Cyclades terminal server
  + High: stonith: external/riloe: workaround for the iLO double close of RIBCL element (bnc#553340)
  + High: stonith: external: log messages immediately on manage and status calls
  + High: stonith: external: log output of plugins (bnc#548699,553340)
  + Medium: LRM: lrmd: log outcome of monitor once an hour
  + Medium: LRM: lrmd: remove operation history on client unregister and flushing all operations (LF 2161)
  + Medium: LRM: lrmd: restore reset scheduler for children (bnc#551971, lf#2296)
  + Medium: LRM: raexec: close the logd fd too when executing agents (LF 2267)
  + Medium: Tools: hb_report: add -V (version) option and add support for corosync
  + Medium: external STONITH plugins: remove dependency on .ocf-shellfuncs (LF2249)
  + Medium: stonith: cyclades: fix for support for newer PM10 firmware (LF 1938)
  + Medium: stonith: external/ipmi: add explanation on reset and power off (LF 2071)
  + Medium: stonith: external/riloe: make sure that host is turned on after power off/on reset (LF 2282)
  + Medium: stonith: meatclient: add -w option to wait until it can connect
  + Medium: stonith: print complete metadata for -m (LF 2279)
  + Medium: stonith: stonith: add -m option to display metadata

* Mon Nov 23 2009 Andrew Beekhof <andrew@beekhof.net> - 1.0-0.12.b79635605337.hg
- Correctly select libuuid for building on rhel >=6 

* Mon Oct 12 2009 Andrew Beekhof <andrew@beekhof.net> - 1.0-0.11.b79635605337.hg
- Add install dependancy on perl-TimeDate for hb_report
- Update to upstream version b79635605337
  + Build: fix defines for pacemaker-pygui compatibility.
  + High: Tools: hb_report: log/events combining
  + High: doc: new README for wti_mpc
  + High: hb_report: add man page hb_report.8
  + High: hb_report: extract important events from the logs
  + High: stonith: external/ibmrsa-telnet: add support for later RSA cards
  + High: stonith: wti_mpc: support for MIB versions 1 and 3
  + Logd: Start/stop priorities are not created by configure
  + Med: sbd: Fix definition of size_t.
  + Med: sbd: Nodename comparison should be case insensitive (bnc#534445)
  + Med: wti_nps: add support for internet power switch model (bnc#539912)
  + Medium (LF 2194): LRM: fix return code on RA exec failure
  + Medium: Tools: hb_report: add -v option (debugging)
  + Medium: Tools: hb_report: options -C and -D are obsoleted
  + ha_logd: Fix a compile error/warning.
  + hb_report: report corosync packages too.
  + sbd: Accept -h (bnc#529574)
  + sbd: really fix the sector_size type.

* Fri Oct  9 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.0-0.10.d97b9dea436e.hg.1
- rebuild with new net-snmp

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 1.0-0.9.d97b9dea436e.hg.1
- rebuilt with new openssl

* Mon Aug 17 2009 Andrew Beekhof <andrew@beekhof.net> - 1.0-0.9.d97b9dea436e.hg
- Include relevant provides: and obsoletes: directives for heartbeat
- Update the tarball from upstream to version d97b9dea436e
  + Include license files
  + Fix error messages in autogen.sh
  + High (bnc#501723): Tools: hb_report: collect archived logs too
  + Medium: clplumbing: check input when creating IPC channels
  + Medium (bnc#510299): stonith: set G_SLICE to always-malloc to avoid bad interaction with the threaded openhpi
  + Med: hb_report: report on more packages and with more state.
  + The -E option to lrmadmin does not take an argument
  + Provide a default value for docdir and ensure it is expanded
  + Low: clplumbing: fix a potential resource leak in cl_random (bnc#525393).
  + Med: hb_report: Include dlm_tool debugging information if available.
  + hb_report: Include more possible error output.
  + Medium: logd: add init script and example configuration file.
  + High: logd: Fix init script. Remove apphbd references.
  + logd: configuration file is optional.
  + logd: print status on finished operations.
  + High: sbd: actually install the binary.
  + Medium: stonith: remove references to heartbeat artifacts.
  + High: hb_report: define HA_NOARCHBIN
  + hb_report: correct syntax error.
  + hb_report: Include details about more packages even.
  + hb_report: report corosync packages too.

* Mon Aug 10 2009 Ville Skyttä <ville.skytta@iki.fi> - 1.0-0.8.75cab275433e.hg
- Use bzipped upstream tarball.

* Tue Jul  28 2009 Andrew Beekhof <andrew@beekhof.net> - 1.0-0.7.75cab275433e.hg
- Add a leading zero to the revision when alphatag is used

* Tue Jul  28 2009 Andrew Beekhof <andrew@beekhof.net> - 1.0-0.6.75cab275433e.hg
- Incorporate results of Fedora review
  - Use global instead of define
  - Remove unused rpm variable
  - Remove redundant configure options
  - Change version to 1.0.0 pre-release and include Mercurial tag in version

* Mon Jul  27 2009 Andrew Beekhof <andrew@beekhof.net> - 0.9-5
- Use linux-ha.org for Source0
- Remove Requires: $name from -devel as its implied
- Instead of 'daemon', use the user and group from Heartbeat and create it 
  if necessary

* Fri Jul  24 2009 Andrew Beekhof <andrew@beekhof.net> - 0.9-4
- Update the tarball from upstream to version 75cab275433e
- Include an AUTHORS and license file in each package
- Change the library package name to cluster-glue-libs to be more 
  Fedora compliant

* Mon Jul  20 2009 Andrew Beekhof <andrew@beekhof.net> - 0.9-3
- Package the project AUTHORS file
- Have Source0 reference the upstream Mercurial repo

* Tue Jul  14 2009 Andrew Beekhof <andrew@beekhof.net> - 0.9-2
- More cleanups

* Fri Jul  3 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.9-1
- Fedora-ize the spec file

* Fri Jun  5 2009 Andrew Beekhof <andrew@beekhof.net> - 0.9-0
- Initial checkin
