%global gname haclient
%global uname hacluster
%global pcmk_docdir %{_docdir}/%{name}

%global specversion 3
%global upstream_version 394e906
%global upstream_prefix ClusterLabs-pacemaker

# Compatibility macros for distros (fedora) that don't provide Python macros by default
# Do this instead of trying to conditionally include {_rpmconfigdir}/macros.python
%{!?py_ver:     %{expand: %%global py_ver      %%(echo `python -c "import sys; print sys.version[:3]"`)}}
%{!?py_prefix:  %{expand: %%global py_prefix   %%(echo `python -c "import sys; print sys.prefix"`)}}
%{!?py_libdir:  %{expand: %%global py_libdir   %%{expand:%%%%{py_prefix}/%%%%{_lib}/python%%%%{py_ver}}}}
%{!?py_sitedir: %{expand: %%global py_sitedir  %%{expand:%%%%{py_libdir}/site-packages}}}

# Compatibility macro wrappers for legacy RPM versions that do not
# support conditional builds
%{!?bcond_without: %{expand: %%global bcond_without() %%{expand:%%%%{!?_without_%%{1}:%%%%global with_%%{1} 1}}}}
%{!?bcond_with:    %{expand: %%global bcond_with()    %%{expand:%%%%{?_with_%%{1}:%%%%global with_%%{1} 1}}}}
%{!?with:          %{expand: %%global with()          %%{expand:%%%%{?with_%%{1}:1}%%%%{!?with_%%{1}:0}}}}
%{!?without:       %{expand: %%global without()       %%{expand:%%%%{?with_%%{1}:0}%%%%{!?with_%%{1}:1}}}}

%global cs_major %(pkg-config corosync --modversion  | awk -F . '{print $1}')
%global cs_minor %(pkg-config corosync --modversion  | awk -F . '{print $2}')
%global rawhide  %(test ! -e /etc/yum.repos.d/fedora-rawhide.repo; echo $?)

# Conditionals
# Invoke "rpmbuild --without <feature>" or "rpmbuild --with <feature>"
# to disable or enable specific features

# Supported cluster stacks, must support at least one
%bcond_without corosync
%bcond_with heartbeat
%bcond_with cman

# Legacy stonithd fencing agents
%bcond_with stonithd

# ESMTP is not available in RHEL, only in EPEL. Allow people to build
# the RPM without ESMTP in case they choose not to use EPEL packages
%bcond_with esmtp
%bcond_with snmp

# Build with/without support for profiling tools
%bcond_with profiling
%bcond_with gcov

# We generate docs using Publican, Asciidoc and Inkscape, but they're not available everywhere
%bcond_with doc

# Use a different versioning scheme
%bcond_with pre_release

%if %{with profiling}
# This disables -debuginfo package creation and also the stripping binaries/libraries
# Useful if you want sane profiling data
%global debug_package %{nil}
%endif

%if %{with pre_release}
%global pcmk_release 0.%{specversion}.%{upstream_version}.git
%else
%global pcmk_release %{specversion}
%endif

Name:          pacemaker
Summary:       Scalable High-Availability cluster resource manager
Version:       1.1.8
Release:       %{pcmk_release}%{?dist}
License:       GPLv2+ and LGPLv2+
Url:           http://www.clusterlabs.org
Group:         System Environment/Daemons

# export VER={upstream_version}
# wget --no-check-certificate -O ClusterLabs-pacemaker-${VER}.tar.gz https://github.com/ClusterLabs/pacemaker/tarball/${VER}
Source0:       %{upstream_prefix}-%{upstream_version}.tar.gz
Patch0:        pacemaker-1.1.8-cast-align.patch
Patch1:	       pacemaker-deprecated-glib.patch
BuildRoot:     %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
AutoReqProv:   on
Requires:      resource-agents
Requires:      %{name}-libs = %{version}-%{release}
Requires:      %{name}-cluster-libs = %{version}-%{release}
Requires:      %{name}-cli = %{version}-%{release}
Requires:      python >= 2.4
Conflicts:     heartbeat < 2.99
Obsoletes:     rgmanager < 3.2.0
Provides:      rgmanager >= 3.2.0
%if !%{with heartbeat}
Obsoletes:     heartbeat < 3.0.4
Provides:      heartbeat >= 3.0.4
%endif

%if %{defined _unitdir}
# Needed for systemd unit
Requires(post):   systemd-sysv
Requires(post):   systemd-units
Requires(preun):  systemd-units
Requires(postun): systemd-units
%endif

%if %{with heartbeat}
Requires(pre): cluster-glue
%endif

%if %{with snmp}
Requires:      perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
%endif

%if 0%{?suse_version}
# net-snmp-devel on SLES10 does not suck in tcpd-devel automatically
BuildRequires: tcpd-devel
# Suse splits this off into a separate package
Requires:      python-curses python-xml
BuildRequires: python-curses python-xml
%endif

# Required for core functionality
BuildRequires: automake autoconf libtool pkgconfig python libtool-ltdl-devel
BuildRequires: glib2-devel libxml2-devel libxslt-devel libuuid-devel
BuildRequires: pkgconfig python-devel gcc-c++ bzip2-devel pam-devel

%if 0%{?suse_version} >= 1100
# Renamed since opensuse-11.0
BuildRequires:  libgnutls-devel
%else
BuildRequires:  gnutls-devel
%endif


# Enables optional functionality
BuildRequires: ncurses-devel openssl-devel docbook-style-xsl libqb-devel
BuildRequires: bison byacc flex help2man

%if %{with cman}

%if 0%{?fedora} > 0
%if 0%{?fedora} < 17
BuildRequires: clusterlib-devel
%endif
%endif

%if 0%{?rhel} > 0
%if 0%{?rhel} < 7
BuildRequires: clusterlib-devel
%endif
%endif

%endif

%if %{with esmtp}
BuildRequires: libesmtp-devel
%endif

%if %{with snmp}
%ifarch alpha %{ix86} x86_64
BuildRequires: lm_sensors-devel
%endif

BuildRequires: net-snmp-devel
%endif

%if %{with corosync}
Requires:      corosync
BuildRequires: corosynclib-devel
%endif

%if %{with heartbeat}
# Do not require heartbeat, the admin should select which stack to use and install it
BuildRequires: cluster-glue-libs-devel heartbeat-devel heartbeat-libs >= 3.0.0
%endif

%if %{with stonithd}
BuildRequires: cluster-glue-libs-devel
%endif

%if !%{rawhide}
# More often than not, inkscape is busted on rawhide, don't even bother

%if %{with doc}
%ifarch %{ix86} x86_64
BuildRequires: publican inkscape asciidoc
%endif
%endif

%endif

%description
Pacemaker is an advanced, scalable High-Availability cluster resource
manager for Linux-HA (Heartbeat) and/or Corosync.

It supports "n-node" clusters with significant capabilities for
managing resources and dependencies.

It will run scripts at initialization, when machines go up or down,
when related resources fail and can be configured to periodically check
resource health.

Available rpmbuild rebuild options:
  --with(out) : heartbeat cman corosync doc publican snmp esmtp pre_release

%package cli
License:      GPLv2+ and LGPLv2+
Summary:      Command line tools for controlling Pacemaker clusters
Group:        System Environment/Daemons
Requires:     %{name}-libs = %{version}-%{release}
Obsoletes:    modcluster < 1.0, cluster-snmp < 1.0, cluster-cim < 1.0
Provides:     modcluster >= 1.0, cluster-snmp >= 1.0, cluster-cim >= 1.0

%description cli
Pacemaker is an advanced, scalable High-Availability cluster resource
manager for Linux-HA (Heartbeat) and/or Corosync.

The %{name}-cli package contains command line tools that can be used
to query and control the cluster from machines that may, or may not,
be part of the cluster.

%package -n %{name}-libs
License:      GPLv2+ and LGPLv2+
Summary:      Core Pacemaker libraries
Group:        System Environment/Daemons

%description -n %{name}-libs
Pacemaker is an advanced, scalable High-Availability cluster resource
manager for Linux-HA (Heartbeat) and/or Corosync.

The %{name}-libs package contains shared libraries needed for cluster
nodes and those just running the CLI tools.

%package -n %{name}-cluster-libs
License:      GPLv2+ and LGPLv2+
Summary:      Cluster Libraries used by Pacemaker
Group:        System Environment/Daemons
Requires:     %{name}-libs = %{version}-%{release}

%description -n %{name}-cluster-libs
Pacemaker is an advanced, scalable High-Availability cluster resource
manager for Linux-HA (Heartbeat) and/or Corosync.

The %{name}-cluster-libs package contains cluster-aware shared
libraries needed for nodes that will form part of the cluster nodes.

%package -n %{name}-libs-devel 
License:      GPLv2+ and LGPLv2+
Summary:      Pacemaker development package
Group:        Development/Libraries
Requires:     %{name}-libs = %{version}-%{release}
Requires:     %{name}-cluster-libs = %{version}-%{release}
Requires:     libtool-ltdl-devel
Requires:     libxml2-devel libxslt-devel bzip2-devel glib2-devel 
%if %{with corosync}
Requires:     corosynclib-devel
%endif
%if %{with heartbeat}
Requires:     cluster-glue-libs-devel heartbeat-devel
%endif

%description -n %{name}-libs-devel
Pacemaker is an advanced, scalable High-Availability cluster resource
manager for Linux-HA (Heartbeat) and/or Corosync.

The %{name}-libs-devel package contains headers and shared libraries
for developing tools for Pacemaker.


%package      cts
License:      GPLv2+ and LGPLv2+
Summary:      Test framework for cluster-related technologies like Pacemaker
Group:        System Environment/Daemons
Requires:     python

%description  cts
Test framework for cluster-related technologies like Pacemaker

%package      doc
License:      GPLv2+ and LGPLv2+
Summary:      Documentation for Pacemaker
Group:        Documentation

%description  doc
Documentation for Pacemaker.

Pacemaker is an advanced, scalable High-Availability cluster resource
manager for Linux-HA (Heartbeat) and/or Corosync.


%prep
%setup -q -n %{upstream_prefix}-%{upstream_version}

%patch0 -p0
%patch1 -p1
# Force the local time
#
# 'hg archive' sets the file date to the date of the last commit.
# This can result in files having been created in the future
# when building on machines in timezones 'behind' the one the 
# commit occurred in - which seriously confuses 'make'
find . -exec touch \{\} \;

%build
./autogen.sh

%if %{with snmp}
eval `objdump --headers --private-headers /usr/bin/perl | grep RPATH | awk '{print "export LD_LIBRARY_PATH="$2}'`
%endif

# RHEL <= 5 does not support --docdir
docdir=%{pcmk_docdir} %{configure}                 \
        %{!?with_heartbeat:  --without-heartbeat}  \
        %{!?with_corosync:   --without-ais}        \
        %{!?with_esmtp:      --without-esmtp}      \
        %{!?with_snmp:       --without-snmp}       \
        %{?with_cman:        --with-cman}          \
        %{?with_profiling:   --with-profiling}     \
        %{?with_gcov:        --with-gcov}          \
        --with-initdir=%{_initrddir}               \
        --localstatedir=%{_var}                    \
        --with-version=%{version}-%{release}

make %{_smp_mflags} V=1 docdir=%{pcmk_docdir} all

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} docdir=%{pcmk_docdir} V=1 install

mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig
mkdir -p ${RPM_BUILD_ROOT}%{_var}/lib/pacemaker/cores
install -m 644 mcp/pacemaker.sysconfig ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig/pacemaker

# Scripts that should be executable
chmod a+x %{buildroot}/%{_datadir}/pacemaker/tests/cts/CTSlab.py

# These are not actually scripts
find %{buildroot} -name '*.xml' -type f -print0 | xargs -0 chmod a-x
find %{buildroot} -name '*.xsl' -type f -print0 | xargs -0 chmod a-x
find %{buildroot} -name '*.rng' -type f -print0 | xargs -0 chmod a-x
find %{buildroot} -name '*.dtd' -type f -print0 | xargs -0 chmod a-x
 
# Dont package static libs
find %{buildroot} -name '*.a' -type f -print0 | xargs -0 rm -f
find %{buildroot} -name '*.la' -type f -print0 | xargs -0 rm -f

# Do not package these either
rm -f %{buildroot}/%{_libdir}/service_crm.so

%if %{with gcov}
GCOV_BASE=%{buildroot}/%{_var}/lib/pacemaker/gcov
mkdir -p $GCOV_BASE
find . -name '*.gcno' -type f | while read F ; do
        D=`dirname $F`
        mkdir -p ${GCOV_BASE}/$D
        cp $F ${GCOV_BASE}/$D
done
%endif

%clean
rm -rf %{buildroot}

%post
%if %{defined _unitdir}
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
%endif
/sbin/chkconfig --add pacemaker || :

%preun
if [ $1 -eq 0 ]; then
        # Package removal, not upgrade
        /sbin/service pacemaker stop &>/dev/null || :
        /sbin/chkconfig --del pacemaker || :
fi

%pre -n %{name}-libs
getent group %{gname} >/dev/null || groupadd -r %{gname}
getent passwd %{uname} >/dev/null || useradd -r -g %{gname} -s /sbin/nologin -c "heartbeat user" %{uname}
exit 0

%post -n %{name}-libs -p /sbin/ldconfig

%postun -n %{name}-libs -p /sbin/ldconfig

%post -n %{name}-cluster-libs -p /sbin/ldconfig

%postun -n %{name}-cluster-libs -p /sbin/ldconfig

%files
###########################################################
%defattr(-,root,root)

%exclude %{_datadir}/pacemaker/tests

%config(noreplace) %{_sysconfdir}/sysconfig/pacemaker
%if %{with corosync}
%{_sbindir}/pacemakerd
%{_initrddir}/pacemaker
%endif

%if %{defined _unitdir}
%{_unitdir}/pacemaker.service
%endif

%{_datadir}/pacemaker
%{_datadir}/snmp/mibs/PCMK-MIB.txt
%{_libexecdir}/pacemaker/*

%if %{with heartbeat}
%{_libdir}/heartbeat/*
%endif

%{_sbindir}/crm_attribute
%{_sbindir}/crm_master
%{_sbindir}/crm_node
%{_sbindir}/attrd_updater
%{_sbindir}/fence_legacy
%{_sbindir}/fence_pcmk
%{_bindir}/ccs2cib
%{_bindir}/ccs_flatten
%{_bindir}/disable_rgmanager
%{_sbindir}/stonith_admin

%if %{with heartbeat}
%{_sbindir}/crm_uuid
%endif

%doc %{_mandir}/man7/*
%doc %{_mandir}/man8/attrd_updater.*
%doc %{_mandir}/man8/crm_attribute.*
%doc %{_mandir}/man8/crm_node.*
%doc %{_mandir}/man8/crm_master.*
%doc %{_mandir}/man8/fence_pcmk.*
%if %{with corosync}
%doc %{_mandir}/man8/pacemakerd.*
%endif
%doc %{_mandir}/man8/stonith_admin.*

%doc COPYING
%doc AUTHORS
%doc ChangeLog

%dir %attr (750, %{uname}, %{gname}) %{_var}/lib/pacemaker
%dir %attr (750, %{uname}, %{gname}) %{_var}/lib/pacemaker/cib
%dir %attr (750, %{uname}, %{gname}) %{_var}/lib/pacemaker/cores
%dir %attr (750, %{uname}, %{gname}) %{_var}/lib/pacemaker/pengine
%ghost %dir %attr (750, %{uname}, %{gname}) %{_var}/run/crm
%dir /usr/lib/ocf
%dir /usr/lib/ocf/resource.d
/usr/lib/ocf/resource.d/pacemaker

%if %{with corosync}
%if 0%{?cs_major} < 2
%if 0%{?cs_minor} < 8
%{_libexecdir}/lcrso/pacemaker.lcrso
%endif
%endif
%endif

%files cli
%defattr(-,root,root)
%{_sbindir}/cibadmin
%{_sbindir}/crm_diff
%{_sbindir}/crm_error
%{_sbindir}/crm_failcount
%{_sbindir}/crm_mon
%{_sbindir}/crm_resource
%{_sbindir}/crm_standby
%{_sbindir}/crm_verify
%{_sbindir}/crmadmin
%{_sbindir}/iso8601
%{_sbindir}/crm_shadow
%{_sbindir}/crm_simulate
%{_sbindir}/crm_report
%{_sbindir}/crm_ticket
%doc %{_mandir}/man8/*
%exclude %{_mandir}/man8/attrd_updater.*
%exclude %{_mandir}/man8/crm_attribute.*
%exclude %{_mandir}/man8/crm_node.*
%exclude %{_mandir}/man8/crm_master.*
%exclude %{_mandir}/man8/fence_pcmk.*
%if %{with corosync}
%exclude %{_mandir}/man8/pacemakerd.*
%endif
%exclude %{_mandir}/man8/stonith_admin.*

%doc COPYING
%doc AUTHORS
%doc ChangeLog

%files -n %{name}-libs
%defattr(-,root,root)

%{_libdir}/libcib.so.*
%{_libdir}/liblrmd.so.*
%{_libdir}/libcrmservice.so.*
%{_libdir}/libcrmcommon.so.*
%{_libdir}/libpe_status.so.*
%{_libdir}/libpe_rules.so.*
%{_libdir}/libpengine.so.*
%{_libdir}/libtransitioner.so.*
%doc COPYING.LIB
%doc AUTHORS

%files -n %{name}-cluster-libs
%defattr(-,root,root)
%{_libdir}/libcrmcluster.so.*
%{_libdir}/libstonithd.so.*
%doc COPYING.LIB
%doc AUTHORS

%files doc
%defattr(-,root,root)
%doc %{pcmk_docdir}

%files cts
%defattr(-,root,root)
%{py_sitedir}/cts
%{_datadir}/pacemaker/tests/cts
%doc COPYING.LIB
%doc AUTHORS

%files -n %{name}-libs-devel
%defattr(-,root,root)
%exclude %{_datadir}/pacemaker/tests/cts
%{_datadir}/pacemaker/tests
%{_includedir}/pacemaker
%{_libdir}/*.so
%if %{with gcov}
%{_var}/lib/pacemaker
%endif
%{_libdir}/pkgconfig/*.pc
%doc COPYING.LIB
%doc AUTHORS

%changelog
* Wed Oct 17 2012 Jon Ciesla <limburgher@gmail.com> 1.1.8-3
- EVR fix.

* Wed Oct 17 2012 Jon Ciesla <limburgher@gmail.com> 1.1.8-2
- Fix FTBFS on ARM by removing cast-align.

* Fri Sep 21 2012 Andrew Beekhof <andrew@beekhof.net> 1.1.8-1
- Rebuild for upstream 1.1.8 release

- New upstream tarball: 394e906
  Changesets: 269
  Diff:       218 files changed, 16188 insertions(+), 5106 deletions(-)

- See included ChangeLog file or https://raw.github.com/ClusterLabs/pacemaker/master/ChangeLog for full details

  + High: Core: Bug cl#5032 - Rewrite the iso8601 date handling code 
  + High: corosync: Use unsigned nodeid's in the cib 
  + High: crmd: Correctly handle scheduled node down events 
  + High: fencing: Bug cl#5092 - Always timeout stonith operations if timeout period expires. 
  + High: fencing: Bug cl#5093 - Stonith per device timeout option 
  + High: fencing: Bug rhbz#801355 - Abort transition on DC when external fencing operation is detected 
  + High: fencing: Bug rhbz#801355 - Merge fence requests for identical operations already in progress. 
  + High: fencing: Bug rhbz#801355 - Report fencing operations external of pacemaker to cib 
  + High: Fencing: fence_legacy - Fix passing of parameters containing '=' 
  + High: fencing: Guarantee non-blocking when fetching stonith metadata 
  + High: fencing: Return cached dynamic target list for busy devices. 
  + High: lrmd: Cancel of recurring ops is now implied by rsc stop action. 
  + High: lrmd: Bug cl#5090 - Do not block stonith monitor actions 
  + High: lrmd: Bug cl#5092 - Fixes timeout value used when monitoring stonith resources 
  + High: lrmd: Bug cl#5094 - Immediately report monitor errors for all stonith devices when lrmd's stonith connection fails. 
  + High: PE: Bug cl#5044 - migrate_to no longer requires load_stopped due to transition loops 
  + High: PE: Correctly find action definitions for anonymous clones 
  + High: PE: Correctly find failcounts for /stopped/ anonymous clones 
  + High: PE: Fix memory leaks found by valgrind 
  + High: PE: Fix failcount expiration 


* Wed Aug 8 2012 Andrew Beekhof <andrew@beekhof.net> 1.1.8-0.1-c72d970.git
- Pre-release 1.1.8 build
  + New IPC implementation from libqb
  + New logging implementation from libqb
  + Quieter - info, debug and trace logs are no longer sent to syslog
  + Dropped dependancy on cluster-glue
  + Config and core directories no longer located in heartbeat directories
  + Support for managing systemd services
  + Rewritten local resource management daemon
  + Version bumps for every shared library due to API cleanups
  + Removes crm shell, install/use pcs shell and GUI instead
- New upstream tarball: c72d970
  Changesets: 764
  Diff:       2073 files changed, 102539 insertions(+), 69977 deletions(-)
- See included ChangeLog file or https://raw.github.com/ClusterLabs/pacemaker/master/ChangeLog for details

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.7-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Mar 28 2012 Andrew Beekhof <andrew@beekhof.net> Pacemaker-1.1.7-2
- Reinstate the ghost directive for /var/run/crm

* Wed Mar 28 2012 Andrew Beekhof <andrew@beekhof.net> Pacemaker-1.1.7-1
- Update source tarball to upstream release: Pacemaker-1.1.7
- See included ChangeLog file or https://raw.github.com/ClusterLabs/pacemaker/master/ChangeLog for details

* Thu Feb 16 2012 Andrew Beekhof <andrew@beekhof.net> 1.1.7-0.3-7742926.git
- New upstream tarball: 7742926
- Additional Provides and Obsoletes directives to enable upgrading from heartbeat
- Rebuild now that the Corosync CFG API has been removed 

* Thu Feb 02 2012 Andrew Beekhof <andrew@beekhof.net> 1.1.7-0.2-bc7c125.git
- Additional Provides and Obsoletes directives to enable upgrading from rgmanager

* Thu Feb 02 2012 Andrew Beekhof <andrew@beekhof.net> 1.1.7-0.1-bc7c125.git
- New upstream tarball: bc7c125
- Pre-release 1.1.7 build to deal with the removal of cman and support for corosync plugins
- Add libqb as a dependancy

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.6-3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Sep 26 2011 Andrew Beekhof <andrew@beekhof.net> 1.1.6-3
- New upstream tarball: 89678d4
- Move man pages to the correct subpackages

* Mon Sep 26 2011 Andrew Beekhof <andrew@beekhof.net> 1.1.6-2
- Do not build in support for heartbeat, snmp, esmtp by default
- Create a package for cluster unaware libraries to minimze our
  footprint on non-cluster nodes
- Better package descriptions

* Thu Sep 07 2011 Andrew Beekhof <andrew@beekhof.net> 1.1.6-1
- Upstream release of 1.1.6
- See included ChangeLog file or http://hg.clusterlabs.org/pacemaker/1.1/file/tip/ChangeLog for details

- Disabled eSMTP and SNMP support.  Painful to configure and rarely used. 
- Created cli sub-package for non-cluster usage

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 1.1.5-3.2
- Perl mass rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 1.1.5-3.1
- Perl mass rebuild

* Mon Jul 11 2011 Andrew Beekhof <andrew@beekhof.net> 1.1.5-3
- Rebuild for new snmp .so

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.1.5-2.2
- Perl mass rebuild

* Fri Jun 10 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.1.5-2.1
- Perl 5.14 mass rebuild

* Wed Apr 27 2011 Andrew Beekhof <andrew@beekhof.net> 1.1.5-2
- Mark /var/run directories with ghost directive
  Resolves: rhbz#656654

* Wed Apr 27 2011 Andrew Beekhof <andrew@beekhof.net> 1.1.5-1
- New upstream release plus patches for CMAN integration
 
* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.4-5.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 11 2011 Andrew Beekhof <andrew@beekhof.net> 1.1.4-5
- Re-enable corosync and heartbeat support with correct bcond variable
  usage

* Wed Dec  8 2010 Fabio M. Di Nitto <fdinitto@redhat.com> 1.1.4-4
- Temporary drop publican doc build

* Wed Dec  8 2010 Fabio M. Di Nitto <fdinitto@redhat.com> 1.1.4-3
- Fix publican build on x86

* Wed Dec  8 2010 Fabio M. Di Nitto <fdinitto@redhat.com> 1.1.4-2
- Drop double source entry and 22Mb from the srpm

* Mon Nov 15 2010 Andrew Beekhof <andrew@beekhof.net> 1.1.4-1
- Upstream release of 1.1.4
- See included ChangeLog file or http://hg.clusterlabs.org/pacemaker/1.1/file/tip/ChangeLog for details

* Wed Sep 29 2010 jkeating - 1.1.3-1.1
- Rebuilt for gcc bug 634757

* Thu Sep 21 2010 Andrew Beekhof <andrew@beekhof.net> - 1.1.3-1
- Upstream release of 1.1.3
  + High: crmd: Use the correct define/size for lrm resource IDs
  + High: crmd: Bug lf#2458 - Ensure stop actions always have the relevant resource attributes
  + High: crmd: Ensure we activate the DC timer if we detect an alternate DC
  + High: mcp: Correctly initialize the string containing the list of active daemons
  + High: mcp: Fix the expansion of the pid file in the init script
  + High: mcp: Tell chkconfig we need to shut down early on
  + High: PE: Bug lf#2476 - Repair on-fail=block for groups and primitive resources
  + High: PE: Do not demote resources because something that requires it can't run
  + High: PE: Rewrite the ordering constraint logic to be simplicity, clarity and maintainability
  + High: PE: Wait until stonith is available, don't fall back to shutdown for nodes requesting termination
  + High: PE: Prevent segfault by ensuring the arguments to do_calculations() are initialized
  + High: stonith: Bug lf#2461 - Prevent segfault by not looking up operations if the hashtable hasn't been initialized yet
  + High: Stonith: Bug lf#2473 - Ensure stonith operations complete within the timeout and are terminated if they run too long
  + High: stonith: Bug lf#2473 - Gracefully handle remote operations that arrive late (after we've done notifications)
  + High: stonith: Bug lf#2473 - Add the timeout at the top level where the daemon is looking for it
  + High: stonith: Bug lf#2473 - Ensure timeouts are included for fencing operations
  + High: Stonith: Use the timeout specified by the user
  + High: Tools: Bug lf#2456 - Fix assertion failure in crm_resource

* Mon Jul 26 2010 Andrew Beekhof <andrew@beekhof.net> - 1.1.3-0.1-b3cb4f4a30ae.hg
- Pre-release version of 1.1.3
  + High: ais: Bug lf2401 - Improved processing when the peer crmd processes join/leave
  + High: ais: fix list of active processes sent to clients (bnc#603685)
  + High: ais: Move the code for finding uid before the fork so that the child does no logging
  + High: ais: Resolve coverity CONSTANT_EXPRESSION_RESULT defects
  + High: cib: Also free query result for xpath operations that return more than one hit
  + High: cib: Attempt to resolve memory corruption when forking a child to write the cib to disk
  + High: cib: Correctly free memory when writing out the cib to disk
  + High: cib: Fix the application of unversioned diffs
  + High: cib: Remove old developmental error logging
  + High: cib: Restructure the 'valid peer' check for deciding which instructions to ignore
  + High: Core: Bug lf#2401 - Backed out changeset 6e6980376f01
  + High: Core: Correctly unpack HA_Messages containing multiple entries with the same name
  + High: Core: crm_count_member() should only track nodes that have the full stack up
  + High: Core: New developmental logging system inspired by the kernel and a PoC from Lars Ellenberg
  + High: crmd: All nodes should see status updates, not just he DC
  + High: crmd: Allow non-DC nodes to clear failcounts too
  + High: crmd: Base DC election on process relative uptime
  + High: crmd: Bug lf#2439 - cancel_op() can also return HA_RSCBUSY
  + High: crmd: Bug lf#2439 - Handle asynchronous notification of resource deletion events
  + High: crmd: Fix assertion failure when performing async resource failures
  + High: crmd: Fix handling of async resource deletion results
  + High: crmd: Include the action for crm graph operations
  + High: crmd: Make sure the membership cache is accurate after a sucessful fencing operation
  + High: crmd: Make sure we always poke the FSA after a transition to clear any TE_HALT actions
  + High: crmd: Offer crm-level membership once the peer starts the crmd process
  + High: crmd: Only need to request quorum update for plugin based clusters
  + High: crmd: Prevent everyone from loosing DC elections by correctly initializing all relevant variables
  + High: crmd: Prevent segmentation fault
  + High: crmd: several fixes for async resource delete
  + High: mcp: Add missing headers when built without heartbeat support
  + High: mcp: New master control process for (re)spawning pacemaker daemons
  + High: PE: Avoid creating invalid ordering constraints for probes that are not needed
  + High: PE: Bug lf#1959 - Fail unmanaged resources should not prevent other services from shutting down
  + High: PE: Bug lf#2422 - Ordering dependencies on partially active groups not observed properly
  + High: PE: Bug lf#2424 - Use notify oepration definition if it exists in the configuration
  + High: PE: Bug lf#2433 - No services should be stopped until probes finish
  + High: PE: Bug lf#2453 - Enforce clone ordering in the absense of colocation constraints
  + High: PE: Correctly detect when there is a real failcount that expired and needs to be cleared
  + High: PE: Correctly handle pseudo action creation
  + High: PE: Correctly order clone startup after group/clone start
  + High: PE: Fix colocation for interleaved clones
  + High: PE: Fix colocation with partially active groups
  + High: PE: Fix potential use-after-free defect from coverity
  + High: PE: Fix previous merge
  + High: PE: Fix use-after-free in order_actions() reported by valgrind
  + High: PE: Prevent endless loop when looking for operation definitions in the configuration
  + High: Resolve coverity RESOURCE_LEAK defects
  + High: Shell: Complete the transition to using crm_attribute instead of crm_failcount and crm_standby
  + High: stonith: Advertise stonith-ng options in the metadata
  + High: stonith: Correctly parse pcmk_host_list parameters that appear on a single line
  + High: stonith: Map poweron/poweroff back to on/off expected by the stonith tool from cluster-glue
  + High: stonith: pass the configuration to the stonith program via environment variables (bnc#620781)
  + High: Support starting plugin-based Pacemaker clusters with the MCP as well
  + High: tools: crm_report - corosync.conf wont necessarily contain the text 'pacemaker' anymore
  + High: tools: crm_simulate - Resolve coverity USE_AFTER_FREE defect
  + High: Tools: Drop the 'pingd' daemon and resource agent in favor of ocf:pacemaker:ping
  + High: Tools: Fix recently introduced use-of-NULL
  + High: Tools: Fix use-after-free defect from coverity

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 1.1.2-5.1
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Jul  9 2010 Dan Horák <dan[at]danny.cz> - 1.1.2-5
- re-enable AIS cluster on s390(x)

* Fri Jul  9 2010 Dan Horák <dan[at]danny.cz> - 1.1.2-4
- AIS cluster not available on s390(x)

* Mon Jun 21 2010 Andrew Beekhof <andrew@beekhof.net> - 1.1.2-3
- publican is only available as a dependancy on i386/x86_64 machines

* Fri Jun 11 2010 Andrew Beekhof <andrew@beekhof.net> - 1.1.2-2
- Resolves rhbz#602239 - Added patch to documentation so that it passes validation
- High: Core: Bug lf#2401 - Backed out changeset 6e6980376f01

* Tue Jun 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.1.2-1.1
- Mass rebuild with perl-5.12.0

* Wed May 12 2010 Andrew Beekhof <andrew@beekhof.net> - 1.1.2-1
- Update the tarball from the upstream 1.1.2 release 
  + High: ais: Bug lf#2340 - Force rogue child processes to terminate after waiting 2.5 minutes
  + High: ais: Bug lf#2359 - Default expected votes to 2 inside Corosync/OpenAIS plugin
  + High: ais: Bug lf#2359 - expected-quorum-votes not correctly updated after membership change
  + High: ais: Bug rhbz#525552 - Move non-threadsafe calls to setenv() to after the fork()
  + High: ais: Do not count votes from offline nodes and calculate current votes before sending quorum data
  + High: ais: Ensure the list of active processes sent to clients is always up-to-date
  + High: ais: Fix previous commit, actually return a result in get_process_list()
  + High: ais: Fix two more uses of getpwnam() in non-thread-safe locations
  + High: ais: Look for the correct conf variable for turning on file logging
  + High: ais: Need to find a better and thread-safe way to set core_uses_pid. Disable for now.
  + High: ais: Use the threadsafe version of getpwnam
  + High: Core: Bug lf#2414 - Prevent use-after-free reported by valgrind when doing xpath based deletions
  + High: Core: Bump the feature set due to the new failcount expiry feature
  + High: Core: Fix memory leak in replace_xml_child() reported by valgrind
  + High: Core: fix memory leaks exposed by valgrind
  + High: crmd: Bug 2401 - Improved detection of partially active peers
  + High: crmd: Bug bnc#578644 - Improve handling of cancelled operations caused by resource cleanup
  + High: crmd: Bug lf#2379 - Ensure the cluster terminates when the PE is not available
  + High: crmd: Bug lf#2414 - Prevent use-after-free of the PE connection after it dies
  + High: crmd: Bug lf#2414 - Prevent use-after-free of the stonith-ng connection
  + High: crmd: Do not allow the target_rc to be misused by resource agents
  + High: crmd: Do not ignore action timeouts based on FSA state
  + High: crmd: Ensure we dont get stuck in S_PENDING if we loose an election to someone that never talks to us again
  + High: crmd: Fix memory leaks exposed by valgrind
  + High: crmd: Remove race condition that could lead to multiple instances of a clone being active on a machine
  + High: crmd: Send erase_status_tag() calls to the local CIB when the DC is fenced, since there is no DC to accept them
  + High: crmd: Use global fencing notifications to prevent secondary fencing operations of the DC
  + High: fencing: Account for stonith_get_info() always returning a pointer to the same static buffer
  + High: PE: Allow startup probes to be disabled - their calculation is a major bottleneck for very large clusters
  + High: PE: Bug lf#2317 - Avoid needless restart of primitive depending on a clone
  + High: PE: Bug lf#2358 - Fix master-master anti-colocation
  + High: PE: Bug lf#2361 - Ensure clones observe mandatory ordering constraints if the LHS is unrunnable
  + High: PE: Bug lf#2383 - Combine failcounts for all instances of an anonymous clone on a host
  + High: PE: Bug lf#2384 - Fix intra-set colocation and ordering
  + High: PE: Bug lf#2403 - Enforce mandatory promotion (colocation) constraints
  + High: PE: Bug lf#2412 - Correctly locate clone instances by their prefix
  + High: PE: Correctly implement optional colocation between primitives and clone resources
  + High: PE: Do not be so quick to pull the trigger on nodes that are coming up
  + High: PE: Fix memory leaks exposed by valgrind
  + High: PE: Fix memory leaks reported by valgrind
  + High: PE: Repair handling of unordered groups in RHS ordering constraints
  + High: PE: Rewrite native_merge_weights() to avoid Fix use-after-free
  + High: PE: Suppress duplicate ordering constraints to achieve orders of magnitude speed increases for large clusters
  + High: Shell: add support for xml in cli
  + High: Shell: always reload status if working with the cluster (bnc#590035)
  + High: Shell: check timeouts also against the default-action-timeout property
  + High: Shell: Default to using the status section from the live CIB (bnc#592762)
  + High: Shell: edit multiple meta_attributes sets in resource management (lf#2315)
  + High: Shell: enable comments (lf#2221)
  + High: Shell: implement new cibstatus interface and commands (bnc#580492)
  + High: Shell: improve configure commit (lf#2336)
  + High: Shell: new cibstatus import command (bnc#585471)
  + High: Shell: new configure filter command
  + High: Shell: restore error reporting in options
  + High: Shell: split shell into modules
  + High: Shell: support for the utilization element (old patch for the new structure)
  + High: Shell: update previous node lookup procedure to include the id where necessary
  + High: Tools: crm_mon - fix memory leaks exposed by valgrind

* Thu Feb 11 2010 Andrew Beekhof <andrew@beekhof.net> - 1.1.1-0.1-60b7753f7310.hg
- Update the tarball from upstream to version 60b7753f7310
  + First public release of the 1.1 series

* Wed Dec 9 2009 Andrew Beekhof <andrew@beekhof.net> - 1.0.5-5
- Include patch of changeset 66b7bfd467f3:
  Some clients such as gfs_controld want a cluster name, allow one to be specified in corosync.conf

* Thu Oct 29 2009 Andrew Beekhof <andrew@beekhof.net> - 1.0.5-4
- Include the fixes from CoroSync integration testing
- Move the resource templates - they are not documentation
- Ensure documentation is placed in a standard location
- Exclude documentation that is included elsewhere in the package

- Update the tarball from upstream to version ee19d8e83c2a
  + High: cib: Correctly clean up when both plaintext and tls remote ports are requested
  + High: PE: Bug bnc#515172 - Provide better defaults for lt(e) and gt(e) comparisions
  + High: PE: Bug lf#2197 - Allow master instances placemaker to be influenced by colocation constraints
  + High: PE: Make sure promote/demote pseudo actions are created correctly
  + High: PE: Prevent target-role from promoting more than master-max instances
  + High: ais: Bug lf#2199 - Prevent expected-quorum-votes from being populated with garbage
  + High: ais: Prevent deadlock - dont try to release IPC message if the connection failed
  + High: cib: For validation errors, send back the full CIB so the client can display the errors
  + High: cib: Prevent use-after-free for remote plaintext connections
  + High: crmd: Bug lf#2201 - Prevent use-of-NULL when running heartbeat
  + High: Core: Bug lf#2169 - Allow dtd/schema validation to be disabled
  + High: PE: Bug lf#2106 - Not all anonymous clone children are restarted after configuration change
  + High: PE: Bug lf#2170 - stop-all-resources option had no effect
  + High: PE: Bug lf#2171 - Prevent groups from starting if they depend on a complex resource which cannot
  + High: PE: Disable resource management if stonith-enabled=true and no stonith resources are defined
  + High: PE: Do not include master score if it would prevent allocation
  + High: ais: Avoid excessive load by checking for dead children every 1s (instead of 100ms)
  + High: ais: Bug rh#525589 - Prevent shutdown deadlocks when running on CoroSync
  + High: ais: Gracefully handle changes to the AIS nodeid
  + High: crmd: Bug bnc#527530 - Wait for the transition to complete before leaving S_TRANSITION_ENGINE
  + High: crmd: Prevent use-after-free with LOG_DEBUG_3
  + Medium: xml: Mask the "symmetrical" attribute on rsc_colocation constraints (bnc#540672)
  + Medium (bnc#520707): Tools: crm: new templates ocfs2 and clvm
  + Medium: Build: Invert the disable ais/heartbeat logic so that --without (ais|heartbeat) is available to rpmbuild
  + Medium: PE: Bug lf#2178 - Indicate unmanaged clones
  + Medium: PE: Bug lf#2180 - Include node information for all failed ops
  + Medium: PE: Bug lf#2189 - Incorrect error message when unpacking simple ordering constraint
  + Medium: PE: Correctly log resources that would like to start but cannot
  + Medium: PE: Stop ptest from logging to syslog
  + Medium: ais: Include version details in plugin name
  + Medium: crmd: Requery the resource metadata after every start operation

* Fri Oct  9 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.0.5-3
- rebuilt with new net-snmp

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 1.0.5-2.1
- rebuilt with new openssl

* Wed Aug 19 2009 Andrew Beekhof <andrew@beekhof.net> - 1.0.5-2
- Add versioned perl dependancy as specified by
    https://fedoraproject.org/wiki/Packaging/Perl#Packages_that_link_to_libperl
- No longer remove RPATH data, it prevents us finding libperl.so and no other
  libraries were being hardcoded
- Compile in support for heartbeat
- Conditionally add heartbeat-devel and corosynclib-devel to the -devel requirements 
  depending on which stacks are supported

* Mon Aug 17 2009 Andrew Beekhof <andrew@beekhof.net> - 1.0.5-1
- Add dependancy on resource-agents
- Use the version of the configure macro that supplies --prefix, --libdir, etc
- Update the tarball from upstream to version 462f1569a437 (Pacemaker 1.0.5 final)
  + High: Tools: crm_resource - Advertise --move instead of --migrate
  + Medium: Extra: New node connectivity RA that uses system ping and attrd_updater
  + Medium: crmd: Note that dc-deadtime can be used to mask the brokeness of some switches

* Tue Aug 11 2009 Ville Skyttä <ville.skytta@iki.fi> - 1.0.5-0.7.c9120a53a6ae.hg
- Use bzipped upstream tarball.

* Wed Jul  29 2009 Andrew Beekhof <andrew@beekhof.net> - 1.0.5-0.6.c9120a53a6ae.hg
- Add back missing build auto* dependancies
- Minor cleanups to the install directive

* Tue Jul  28 2009 Andrew Beekhof <andrew@beekhof.net> - 1.0.5-0.5.c9120a53a6ae.hg
- Add a leading zero to the revision when alphatag is used

* Tue Jul  28 2009 Andrew Beekhof <andrew@beekhof.net> - 1.0.5-0.4.c9120a53a6ae.hg
- Incorporate the feedback from the cluster-glue review
- Realistically, the version is a 1.0.5 pre-release
- Use the global directive instead of define for variables
- Use the haclient/hacluster group/user instead of daemon
- Use the _configure macro
- Fix install dependancies

* Fri Jul  24 2009 Andrew Beekhof <andrew@beekhof.net> - 1.0.4-3
- Include an AUTHORS and license file in each package
- Change the library package name to pacemaker-libs to be more 
  Fedora compliant
- Remove execute permissions from xml related files
- Reference the new cluster-glue devel package name
- Update the tarball from upstream to version c9120a53a6ae
  + High: PE: Only prevent migration if the clone dependancy is stopping/starting on the target node
  + High: PE: Bug 2160 - Dont shuffle clones due to colocation
  + High: PE: New implementation of the resource migration (not stop/start) logic
  + Medium: Tools: crm_resource - Prevent use-of-NULL by requiring a resource name for the -A and -a options
  + Medium: PE: Prevent use-of-NULL in find_first_action()
  + Low: Build: Include licensing files

* Tue Jul 14 2009 Andrew Beekhof <andrew@beekhof.net> - 1.0.4-2
- Reference authors from the project AUTHORS file instead of listing in description
- Change Source0 to reference the project's Mercurial repo
- Cleaned up the summaries and descriptions
- Incorporate the results of Fedora package self-review

* Tue Jul 14 2009 Andrew Beekhof <andrew@beekhof.net> - 1.0.4-1
- Initial checkin
