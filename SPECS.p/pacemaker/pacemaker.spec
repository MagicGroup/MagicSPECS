%global gname haclient
%global uname hacluster
%global pcmk_docdir %{_docdir}/%{name}

%global specversion 2
%global commit a9c81774b89f21f990be255f9862446d1a38afee
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global github_owner ClusterLabs

%global py_site %(python -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")

# Turn off the auto compilation of python files not in the site-packages directory
# Needed so that the -devel package is multilib compliant
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')

%global cs_major %(pkg-config corosync --modversion  | awk -F . '{print $1}')
%global cs_minor %(pkg-config corosync --modversion  | awk -F . '{print $2}')
%global rawhide  %(test ! -e /etc/yum.repos.d/fedora-rawhide.repo; echo $?)

# Conditionals
# Invoke "rpmbuild --without <feature>" or "rpmbuild --with <feature>"
# to disable or enable specific features

# Legacy stonithd fencing agents
%bcond_with stonithd

# Build with/without support for profiling tools
%bcond_with profiling

# We generate docs using Publican, Asciidoc and Inkscape, but they're not available everywhere
%bcond_with doc

# Use a different versioning scheme
%bcond_with pre_release

# Ship an Upstart job file
%bcond_with upstart_job

%if %{with profiling}
# This disables -debuginfo package creation and also the stripping binaries/libraries
# Useful if you want sane profiling data
%global debug_package %{nil}
%endif

%if %{with pre_release}
%global pcmk_release 0.%{specversion}.%{shortcommit}.git
%else
%global pcmk_release %{specversion}
%endif

Name:          pacemaker
Summary:       Scalable High-Availability cluster resource manager
Version:       1.1.12
Release:       %{pcmk_release}%{?dist}.2
License:       GPLv2+ and LGPLv2+
Url:           http://www.clusterlabs.org
Group:         System Environment/Daemons

Source0:       https://github.com/%{github_owner}/%{name}/archive/%{commit}/%{name}-%{commit}.tar.gz
Patch1:        pacemaker-systemd.patch

BuildRoot:     %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
AutoReqProv:   on
Requires:      resource-agents
Requires:      %{name}-libs = %{version}-%{release}
Requires:      %{name}-cluster-libs = %{version}-%{release}
Requires:      %{name}-cli = %{version}-%{release}
Requires:      python >= 2.4

%if %{defined systemd_requires}
%systemd_requires
%endif

%if 0%{?rhel} > 0
ExclusiveArch: i686 x86_64
%endif

%if 0%{?suse_version}
# Suse splits this off into a separate package
Requires:      python-curses python-xml
BuildRequires: python-curses python-xml
%endif

# Required for core functionality
BuildRequires: automake autoconf libtool pkgconfig python libtool-ltdl-devel
BuildRequires: glib2-devel libxml2-devel libxslt-devel libuuid-devel
BuildRequires: pkgconfig python-devel gcc-c++ bzip2-devel pam-devel

# Required for agent_config.h which specifies the correct scratch directory
BuildRequires: resource-agents

# We need reasonably recent versions of libqb
BuildRequires: libqb-devel > 0.11.0
Requires:      libqb > 0.11.0

# Enables optional functionality
BuildRequires: ncurses-devel openssl-devel docbook-style-xsl
BuildRequires: bison byacc flex help2man dbus-devel

%if %{defined _unitdir}
BuildRequires: systemd-devel
%endif

%if 0%{?suse_version} >= 1100
# Renamed since opensuse-11.0
BuildRequires:  libgnutls-devel
%else
BuildRequires:  gnutls-devel
%endif

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

Requires:      corosync
BuildRequires: corosynclib-devel

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
manager for Corosync, CMAN and/or Linux-HA.

It supports more than 16 node clusters with significant capabilities
for managing resources and dependencies.

It will run scripts at initialization, when machines go up or down,
when related resources fail and can be configured to periodically check
resource health.

Available rpmbuild rebuild options:
  --with(out) : stonithd doc profiling pre_release upstart_job

%package cli
License:      GPLv2+ and LGPLv2+
Summary:      Command line tools for controlling Pacemaker clusters
Group:        System Environment/Daemons
Requires:     %{name}-libs = %{version}-%{release}
Requires:     perl-TimeDate

%description cli
Pacemaker is an advanced, scalable High-Availability cluster resource
manager for Corosync, CMAN and/or Linux-HA.

The %{name}-cli package contains command line tools that can be used
to query and control the cluster from machines that may, or may not,
be part of the cluster.

%package -n %{name}-libs
License:      GPLv2+ and LGPLv2+
Summary:      Core Pacemaker libraries
Group:        System Environment/Daemons

%description -n %{name}-libs
Pacemaker is an advanced, scalable High-Availability cluster resource
manager for Corosync, CMAN and/or Linux-HA.

The %{name}-libs package contains shared libraries needed for cluster
nodes and those just running the CLI tools.

%package -n %{name}-cluster-libs
License:      GPLv2+ and LGPLv2+
Summary:      Cluster Libraries used by Pacemaker
Group:        System Environment/Daemons
Requires:     %{name}-libs = %{version}-%{release}

%description -n %{name}-cluster-libs
Pacemaker is an advanced, scalable High-Availability cluster resource
manager for Corosync, CMAN and/or Linux-HA.

The %{name}-cluster-libs package contains cluster-aware shared
libraries needed for nodes that will form part of the cluster nodes.

%package remote
License:      GPLv2+ and LGPLv2+
Summary:      Pacemaker remote daemon for non-cluster nodes
Group:        System Environment/Daemons
Requires:     %{name}-libs = %{version}-%{release}
Requires:      %{name}-cli = %{version}-%{release}
Requires:      resource-agents
%if %{defined systemd_requires}
%systemd_requires
%endif

%description remote
Pacemaker is an advanced, scalable High-Availability cluster resource
manager for Corosync, CMAN and/or Linux-HA.

The %{name}-remote package contains the Pacemaker Remote daemon
which is capable of extending pacemaker functionality to remote
nodes not running the full corosync/cluster stack.

%package -n %{name}-libs-devel
License:      GPLv2+ and LGPLv2+
Summary:      Pacemaker development package
Group:        Development/Libraries
Requires:     %{name}-cts = %{version}-%{release}
Requires:     %{name}-libs = %{version}-%{release}
Requires:     %{name}-cluster-libs = %{version}-%{release}
Requires:     libtool-ltdl-devel libqb-devel libuuid-devel
Requires:     libxml2-devel libxslt-devel bzip2-devel glib2-devel
Requires:     corosynclib-devel

%description -n %{name}-libs-devel
Pacemaker is an advanced, scalable High-Availability cluster resource
manager for Corosync, CMAN and/or Linux-HA.

The %{name}-libs-devel package contains headers and shared libraries
for developing tools for Pacemaker.


%package      cts
License:      GPLv2+ and LGPLv2+
Summary:      Test framework for cluster-related technologies like Pacemaker
Group:        System Environment/Daemons
Requires:     python
Requires:     %{name}-libs = %{version}-%{release}

%description  cts
Test framework for cluster-related technologies like Pacemaker

%package      doc
License:      GPLv2+ and LGPLv2+
Summary:      Documentation for Pacemaker
Group:        Documentation

%description  doc
Documentation for Pacemaker.

Pacemaker is an advanced, scalable High-Availability cluster resource
manager for Corosync, CMAN and/or Linux-HA.


%prep
%autosetup -n %{name}-%{commit} -p1

# Force the local time
#
# 'git' sets the file date to the date of the last commit.
# This can result in files having been created in the future
# when building on machines in timezones 'behind' the one the
# commit occurred in - which seriously confuses 'make'
find . -exec touch \{\} \;

%build
./autogen.sh

# RHEL <= 5 does not support --docdir
docdir=%{pcmk_docdir} %{configure}                 \
        %{?with_profiling:   --with-profiling}     \
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

%if %{with upstart_job}
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/init
install -m 644 mcp/pacemaker.upstart ${RPM_BUILD_ROOT}%{_sysconfdir}/init/pacemaker.conf
install -m 644 mcp/pacemaker.combined.upstart ${RPM_BUILD_ROOT}%{_sysconfdir}/init/pacemaker.combined.conf
%endif

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

# Don't ship init scripts for systemd based platforms
%if %{defined _unitdir}
rm -f %{buildroot}/%{_initrddir}/pacemaker
rm -f %{buildroot}/%{_initrddir}/pacemaker_remote
%endif

%if %{with profiling}
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
%systemd_post pacemaker.service

%preun
%systemd_preun pacemaker.service

%postun
%systemd_postun_with_restart pacemaker.service 

%post remote
%systemd_post pacemaker_remote.service

%preun remote
%systemd_preun pacemaker_remote.service

%postun remote
%systemd_postun_with_restart pacemaker_remote.service 

%pre -n %{name}-libs

getent group %{gname} >/dev/null || groupadd -r %{gname} -g 189
getent passwd %{uname} >/dev/null || useradd -r -g %{gname} -u 189 -s /sbin/nologin -c "cluster user" %{uname}
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
%{_sbindir}/pacemakerd

%if %{defined _unitdir}
%{_unitdir}/pacemaker.service
%else
%{_initrddir}/pacemaker
%endif

%{_datadir}/pacemaker
%{_datadir}/snmp/mibs/PCMK-MIB.txt
%exclude %{_libexecdir}/pacemaker/lrmd_test
%exclude %{_sbindir}/pacemaker_remoted
%{_libexecdir}/pacemaker/*

%{_sbindir}/crm_attribute
%{_sbindir}/crm_master
%{_sbindir}/crm_node
%{_sbindir}/attrd_updater
%{_sbindir}/fence_legacy
%{_sbindir}/fence_pcmk
%{_sbindir}/stonith_admin

%doc %{_mandir}/man7/*
%doc %{_mandir}/man8/attrd_updater.*
%doc %{_mandir}/man8/crm_attribute.*
%doc %{_mandir}/man8/crm_node.*
%doc %{_mandir}/man8/crm_master.*
%doc %{_mandir}/man8/fence_pcmk.*
%doc %{_mandir}/man8/pacemakerd.*
%doc %{_mandir}/man8/stonith_admin.*

%doc COPYING
%doc AUTHORS
%doc ChangeLog

%dir %attr (750, %{uname}, %{gname}) %{_var}/lib/pacemaker
%dir %attr (750, %{uname}, %{gname}) %{_var}/lib/pacemaker/cib
%dir %attr (750, %{uname}, %{gname}) %{_var}/lib/pacemaker/cores
%dir %attr (750, %{uname}, %{gname}) %{_var}/lib/pacemaker/pengine
%dir %attr (750, %{uname}, %{gname}) %{_var}/lib/pacemaker/blackbox
%ghost %dir %attr (750, %{uname}, %{gname}) %{_var}/run/crm
%dir /usr/lib/ocf
%dir /usr/lib/ocf/resource.d
/usr/lib/ocf/resource.d/pacemaker

%if 0%{?cs_major} < 2
%if 0%{?cs_minor} < 8
%{_libexecdir}/lcrso/pacemaker.lcrso
%endif
%endif

%if %{with upstart_job}
%config(noreplace) %{_sysconfdir}/init/pacemaker.conf
%config(noreplace) %{_sysconfdir}/init/pacemaker.combined.conf
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
%exclude %{_mandir}/man8/pacemakerd.*
%exclude %{_mandir}/man8/pacemaker_remoted.*
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
%{_libdir}/libstonithd.so.*
%{_libdir}/libtransitioner.so.*
%doc COPYING.LIB
%doc AUTHORS

%files -n %{name}-cluster-libs
%defattr(-,root,root)
%{_libdir}/libcrmcluster.so.*
%doc COPYING.LIB
%doc AUTHORS

%files remote
%defattr(-,root,root)

%config(noreplace) %{_sysconfdir}/logrotate.d/pacemaker
%config(noreplace) %{_sysconfdir}/sysconfig/pacemaker
%if %{defined _unitdir}
%{_unitdir}/pacemaker_remote.service
%else
%{_initrddir}/pacemaker_remote
%endif

%{_sbindir}/pacemaker_remoted
%{_mandir}/man8/pacemaker_remoted.*
%doc COPYING.LIB
%doc AUTHORS

%files doc
%defattr(-,root,root)
%doc %{pcmk_docdir}

%files cts
%defattr(-,root,root)
%{py_site}/cts
%{_datadir}/pacemaker/tests/cts
%{_libexecdir}/pacemaker/lrmd_test
%doc COPYING.LIB
%doc AUTHORS

%files -n %{name}-libs-devel
%defattr(-,root,root)
%exclude %{_datadir}/pacemaker/tests/cts
%{_datadir}/pacemaker/tests
%{_includedir}/pacemaker
%{_libdir}/*.so
%if %{with profiling}
%{_var}/lib/pacemaker
%endif
%{_libdir}/pkgconfig/*.pc
%doc COPYING.LIB
%doc AUTHORS

%changelog
* Fri Jul 31 2015 Liu Di <liudidi@gmail.com> - 1.1.12-2.2
- 为 Magic 3.0 重建

* Tue Apr 14 2015 Liu Di <liudidi@gmail.com> - 1.1.12-2.1
- 为 Magic 3.0 重建

* Tue Nov 05 2014 Andrew Beekhof <abeekhof@redhat.com> - 1.1.12-2
- Address incorrect use of the dbus API for interacting with systemd

* Tue Oct 28 2014 Andrew Beekhof <abeekhof@redhat.com> - 1.1.12-1
- Update for new upstream tarball: Pacemaker-1.1.12+ (a9c8177)
- See included ChangeLog file or https://raw.github.com/ClusterLabs/pacemaker/master/ChangeLog for full details

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.11-1.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.11-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Feb 18 2014 Andrew Beekhof <abeekhof@redhat.com> - 1.1.11-1
- Update for new upstream tarball: Pacemaker-1.1.11 (9d39a6b)
- See included ChangeLog file or https://raw.github.com/ClusterLabs/pacemaker/master/ChangeLog for full details

* Thu Jun 20 2013 Andrew Beekhof <abeekhof@redhat.com> - 1.1.9-3
- Update to upstream 7d8acec
- See included ChangeLog file or https://raw.github.com/ClusterLabs/pacemaker/master/ChangeLog for full details

  + Feature: Turn off auto-respawning of systemd services when the cluster starts them
  + Fix: crmd: Ensure operations for cleaned up resources don't block recovery
  + Fix: logging: If SIGTRAP is sent before tracing is turned on, turn it on instead of crashing

* Mon Jun 17 2013 Andrew Beekhof <abeekhof@redhat.com> - 1.1.9-2
- Update for new upstream tarball: 781a388
- See included ChangeLog file or https://raw.github.com/ClusterLabs/pacemaker/master/ChangeLog for full details

* Wed May 12 2010 Andrew Beekhof <andrew@beekhof.net> - 1.1.2-1
- Update the tarball from the upstream 1.1.2 release
- See included ChangeLog file or https://raw.github.com/ClusterLabs/pacemaker/master/ChangeLog for full details

* Tue Jul 14 2009 Andrew Beekhof <andrew@beekhof.net> - 1.0.4-1
- Initial checkin
