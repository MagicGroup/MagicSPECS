#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.
#

# Below is the script used to generate a new source file
# from the resource-agent upstream git repo.
#
# TAG=$(git log --pretty="format:%h" -n 1)
# distdir="ClusterLabs-resource-agents-${TAG}"
# TARFILE="${distdir}.tar.gz"
# rm -rf $TARFILE $distdir
# git archive --prefix=$distdir/ HEAD | gzip > $TARFILE
#

%global upstream_prefix ClusterLabs-resource-agents
%global upstream_version 39c1f6e

# SSLeay (required by ldirectord)
%if 0%{?suse_version}
%global SSLeay perl-Net_SSLeay
%else
%global SSLeay perl-Net-SSLeay
%endif

# determine the ras-set to process based on configure invokation
%bcond_with rgmanager
%bcond_without linuxha

Name:		resource-agents
Summary:	Open Source HA Reusable Cluster Resource Scripts
Version:	3.9.5
Release:	12%{?rcver:%{rcver}}%{?numcomm:.%{numcomm}}%{?alphatag:.%{alphatag}}%{?dirty:.%{dirty}}%{?dist}.1
License:	GPLv2+ and LGPLv2+
URL:		https://github.com/ClusterLabs/resource-agents
%if 0%{?fedora} || 0%{?centos_version} || 0%{?rhel}
Group:		System Environment/Base
%else
Group:		Productivity/Clustering/HA
%endif
Source0:	%{upstream_prefix}-%{upstream_version}.tar.gz
Obsoletes:	heartbeat-resources <= %{version}
Provides:	heartbeat-resources = %{version}

## Setup/build bits
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

# Build dependencies
BuildRequires: automake autoconf pkgconfig
BuildRequires: perl python-devel
BuildRequires: libxslt glib2-devel
BuildRequires: which

%if 0%{?fedora} || 0%{?centos_version} || 0%{?rhel}
#BuildRequires: cluster-glue-libs-devel
BuildRequires: docbook-style-xsl docbook-dtds
%if 0%{?rhel} == 0
BuildRequires: libnet-devel
%endif
%endif

%if 0%{?suse_version}  
%if 0%{?suse_version} >= 1140
BuildRequires:  libnet1
%else
BuildRequires:  libnet
%endif
BuildRequires:  libglue-devel
BuildRequires:  libxslt docbook_4 docbook-xsl-stylesheets
%endif

## Runtime deps
## These apply to rgmanager agents only to guarantee agents
## are functional
%if %{with rgmanager}
# system tools shared by several agents
Requires: /bin/bash /bin/grep /bin/sed /bin/gawk
Requires: /bin/ps /usr/bin/pkill /bin/hostname
Requires: /sbin/fuser
Requires: /sbin/findfs /bin/mount

# fs.sh
Requires: /sbin/quotaon /sbin/quotacheck
Requires: /sbin/fsck
Requires: /usr/sbin/fsck.ext2 /usr/sbin/fsck.ext3 /usr/sbin/fsck.ext4
Requires: /usr/sbin/fsck.xfs

# ip.sh
Requires: /sbin/ip /usr/sbin/ethtool
Requires: /sbin/rdisc /usr/sbin/arping /bin/ping /bin/ping6

# lvm.sh
Requires: /usr/sbin/lvm

# netfs.sh
Requires: /sbin/mount.nfs /sbin/mount.nfs4 /usr/sbin/mount.cifs
Requires: /usr/sbin/rpc.nfsd /sbin/rpc.statd /usr/sbin/rpc.mountd
%endif

%description
A set of scripts to interface with several services to operate in a
High Availability environment for both Pacemaker and rgmanager
service managers.

%if %{with linuxha}
%package -n ldirectord
License:	GPLv2+
Summary:	A Monitoring Daemon for Maintaining High Availability Resources
%if 0%{?fedora} || 0%{?centos_version} || 0%{?rhel}
Group:		System Environment/Daemons
%else
Group:		Productivity/Clustering/HA
%endif
Obsoletes:	heartbeat-ldirectord <= %{version}
Provides:	heartbeat-ldirectord = %{version}
%if 0%{?fedora} > 18 || 0%{?centos_version} > 6 || 0%{?rhel} > 6
BuildRequires: perl-podlators
%endif
Requires:       %{SSLeay} perl-libwww-perl perl-MailTools
Requires:       ipvsadm logrotate
%if 0%{?fedora_version}
Requires:	perl-Net-IMAP-Simple-SSL
Requires(post):	/sbin/chkconfig
Requires(preun):/sbin/chkconfig
%endif

%description -n ldirectord
The Linux Director Daemon (ldirectord) was written by Jacob Rief.
<jacob.rief@tiscover.com>

ldirectord is a stand alone daemon for monitoring the services on real
servers. Currently, HTTP, HTTPS, and FTP services are supported.
lditrecord is simple to install and works with the heartbeat code
(http://www.linux-ha.org/).

See 'ldirectord -h' and linux-ha/doc/ldirectord for more information.
%endif

%prep
%if 0%{?suse_version} == 0 && 0%{?fedora} == 0 && 0%{?centos_version} == 0 && 0%{?rhel} == 0
%{error:Unable to determine the distribution/version. This is generally caused by missing /etc/rpm/macros.dist. Please install the correct build packages or define the required macros manually.}
exit 1
%endif
%setup -q -n %{upstream_prefix}-%{upstream_version}

%build
if [ ! -f configure ]; then
	./autogen.sh
fi

%if 0%{?fedora} >= 11 || 0%{?centos_version} > 5 || 0%{?rhel} > 5
CFLAGS="$(echo '%{optflags}')"
%global conf_opt_fatal "--enable-fatal-warnings=no"
%else
CFLAGS="${CFLAGS} ${RPM_OPT_FLAGS}"
%global conf_opt_fatal "--enable-fatal-warnings=yes"
%endif

%if %{with rgmanager}
%global rasset rgmanager
%endif
%if %{with linuxha}
%global rasset linux-ha
%endif
%if %{with rgmanager} && %{with linuxha}
%global rasset all
%endif

export CFLAGS

%configure \
	%{conf_opt_fatal} \
	--with-pkg-name=%{name} \
	--with-ras-set=%{rasset}

%if %{defined jobs}
JFLAGS="$(echo '-j%{jobs}')"
%else
JFLAGS="$(echo '%{_smp_mflags}')"
%endif

make $JFLAGS

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

## tree fixup
# remove docs (there is only one and they should come from doc sections in files)
rm -rf %{buildroot}/usr/share/doc/resource-agents

%if %{with linuxha}
%if 0%{?suse_version}
test -d %{buildroot}/sbin || mkdir %{buildroot}/sbin
(
  cd %{buildroot}/sbin
  ln -sf /%{_sysconfdir}/init.d/ldirectord rcldirectord 
) || true
%endif
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS COPYING COPYING.GPLv3 ChangeLog
%if %{with linuxha}
%doc doc/README.webapps
%doc %{_datadir}/%{name}/ra-api-1.dtd
%endif

%if %{with rgmanager}
%{_datadir}/cluster
%{_sbindir}/rhev-check.sh
%endif

%if %{with linuxha}
%dir /usr/lib/ocf
%dir /usr/lib/ocf/resource.d
%dir /usr/lib/ocf/lib

/usr/lib/ocf/lib/heartbeat

/usr/lib/ocf/resource.d/heartbeat
%if %{with rgmanager}
/usr/lib/ocf/resource.d/redhat
%endif

%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/ocft
%{_datadir}/%{name}/ocft/configs
%{_datadir}/%{name}/ocft/caselib
%{_datadir}/%{name}/ocft/README
%{_datadir}/%{name}/ocft/README.zh_CN

%{_sbindir}/ocf-tester
%{_sbindir}/ocft
#%{_sbindir}/sfex_init
#%{_sbindir}/sfex_stat

%{_includedir}/heartbeat

%dir %attr (1755, root, root)	%{_var}/run/resource-agents

%{_mandir}/man7/*.7*
%{_mandir}/man8/ocf-tester.8*
#%{_mandir}/man8/sfex_init.8*

# For compatability with pre-existing agents
%dir %{_sysconfdir}/ha.d
%{_sysconfdir}/ha.d/shellfuncs

%{_libexecdir}/heartbeat

%if %{with rgmanager}
%post -n resource-agents
ccs_update_schema > /dev/null 2>&1 ||:
%endif

%if 0%{?suse_version}
%preun -n ldirectord
%stop_on_removal ldirectord
%postun -n ldirectord
%insserv_cleanup
%endif

%if 0%{?fedora}
%preun -n ldirectord
/sbin/chkconfig --del ldirectord
%postun -n ldirectord -p /sbin/ldconfig
%post -n ldirectord
/sbin/chkconfig --add ldirectord
%endif
%endif

%if %{with linuxha}
%files -n ldirectord
%defattr(-,root,root)
%{_sbindir}/ldirectord
%doc ldirectord/ldirectord.cf COPYING
%{_mandir}/man8/ldirectord.8*
%config(noreplace) %{_sysconfdir}/logrotate.d/ldirectord
%dir %{_sysconfdir}/ha.d
%dir %{_sysconfdir}/ha.d/resource.d
%{_sysconfdir}/ha.d/resource.d/ldirectord
%{_sysconfdir}/init.d/ldirectord
%if 0%{?suse_version}
/sbin/rcldirectord
%endif
%if 0%{?fedora}
/usr/lib/ocf/resource.d/heartbeat/ldirectord
%endif
%endif

%changelog
* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.9.5-12.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr 30 2014 David Vossel <dvossel@redhat.com> - 3.9.5-12
- Sync with latest upstream.

* Thu Jan 2 2014 David Vossel <dvossel@redhat.com> - 3.9.5-11
- Sync with latest upstream.

* Wed Oct 20 2013 David Vossel <dvossel@redhat.com> - 3.9.5-10
- Fix build system for rawhide.

* Wed Oct 16 2013 David Vossel <dvossel@redhat.com> - 3.9.5-9
- Remove rgmanager agents from build. 

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.9.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 3.9.5-7
- Perl 5.18 rebuild

* Tue Jun 18 2013 David Vossel <dvossel@redhat.com> - 3.9.5-6
- Restores rsctmp directory to upstream default.

* Tue Jun 18 2013 David Vossel <dvossel@redhat.com> - 3.9.5-5
- Merges redhat provider into heartbeat provider. Remove
  rgmanager's redhat provider.

  Resolves: rhbz#917681
  Resolves: rhbz#928890
  Resolves: rhbz#952716
  Resolves: rhbz#960555

* Tue Mar 12 2013 David Vossel <dvossel@redhat.com> - 3.9.5-3
- Fixes build system error with conditional logic involving
  IPv6addr and updates spec file to build against rhel 7 as
  well as fedora 19.

* Mon Mar 11 2013 David Vossel <dvossel@redhat.com> - 3.9.5-2
- Resolves rhbz#915050

* Mon Mar 11 2013 David Vossel <dvossel@redhat.com> - 3.9.5-1
- New upstream release.

* Fri Jan 25 2013 Kevin Fenzi <kevin@scrye.com> - 3.9.2-5
- Fix cifs mount requires

* Mon Nov 12 2012 Chris Feist <cfeist@redhat.com> - 3.9.2-4
- Removed version number after dist

* Mon Oct 29 2012 Chris Feist <cfeist@redhat.com> - 3.9.2-3.8
- Remove cluster-glue-libs-devel
- Disable IPv6addr & sfex to fix deps on libplumgpl & libplum (due to
  disappearance of cluster-glue in F18)

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.9.2-3.5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jul 05 2012 Chris Feist <cfeist@redhat.com> - 3.9.2-3.4
- Fix location of lvm (change from /sbin to /usr/sbin)

* Tue Apr 04 2012 Jon Ciesla <limburgher@gmail.com> - 3.9.2-3.3
- Rebuilt to fix rawhide dependency issues (caused by move of fsck from
  /sbin to /usr/sbin).

* Fri Mar 30 2012 Jon Ciesla <limburgher@gmail.com> - 3.9.2-3.1
- libnet rebuild.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.9.2-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jul  8 2011 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.9.2-2
- add post call to resource-agents to integrate with cluster 3.1.4

* Thu Jun 30 2011 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.9.2-1
- new upstream release
- fix 2 regressions from 3.9.1

* Mon Jun 20 2011 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.9.1-1
- new upstream release
- import spec file from upstream

* Tue Mar  1 2011 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.1.1-1
- new upstream release 3.1.1 and 1.0.4

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec  2 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.1.0-1
- new upstream release
- spec file update:
  Update upstream URL
  Update source URL
  use standard configure macro
  use standard make invokation

* Thu Oct  7 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.17-1
- new upstream release
  Resolves: rhbz#632595, rhbz#633856, rhbz#632385, rhbz#628013
  Resolves: rhbz#621313, rhbz#595383, rhbz#580492, rhbz#605733
  Resolves: rhbz#636243, rhbz#591003, rhbz#637913, rhbz#634718
  Resolves: rhbz#617247, rhbz#617247, rhbz#617234, rhbz#631943
  Resolves: rhbz#639018

* Thu Oct  7 2010 Andrew Beekhof <andrew@beekhof.net> - 3.0.16-2
- new upstream release of the Pacemaker agents: 71b1377f907c

* Thu Sep  2 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.16-1
- new upstream release
  Resolves: rhbz#619096, rhbz#614046, rhbz#620679, rhbz#619680
  Resolves: rhbz#621562, rhbz#621694, rhbz#608887, rhbz#622844
  Resolves: rhbz#623810, rhbz#617306, rhbz#623816, rhbz#624691
  Resolves: rhbz#622576

* Thu Jul 29 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.14-1
- new upstream release
  Resolves: rhbz#553383, rhbz#557563, rhbz#578625, rhbz#591003
  Resolves: rhbz#593721, rhbz#593726, rhbz#595455, rhbz#595547
  Resolves: rhbz#596918, rhbz#601315, rhbz#604298, rhbz#606368
  Resolves: rhbz#606470, rhbz#606480, rhbz#606754, rhbz#606989
  Resolves: rhbz#607321, rhbz#608154, rhbz#608887, rhbz#609181
  Resolves: rhbz#609866, rhbz#609978, rhbz#612097, rhbz#612110
  Resolves: rhbz#612165, rhbz#612941, rhbz#614127, rhbz#614356
  Resolves: rhbz#614421, rhbz#614457, rhbz#614961, rhbz#615202
  Resolves: rhbz#615203, rhbz#615255, rhbz#617163, rhbz#617566
  Resolves: rhbz#618534, rhbz#618703, rhbz#618806, rhbz#618814

* Mon Jun  7 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.13-1
- new upstream release
  Resolves: rhbz#592103, rhbz#593108, rhbz#578617, rhbz#594626
  Resolves: rhbz#594511, rhbz#596046, rhbz#594111, rhbz#597002
  Resolves: rhbz#599643

* Tue May 18 2010 Andrew Beekhof <andrew@beekhof.net> - 3.0.12-2
- libnet is not available on RHEL
- Do not package ldirectord on RHEL
  Resolves: rhbz#577264

* Mon May 10 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.12-1
- new upstream release
  Resolves: rhbz#585217, rhbz#586100, rhbz#581533, rhbz#582753
  Resolves: rhbz#582754, rhbz#585083, rhbz#587079, rhbz#588890
  Resolves: rhbz#588925, rhbz#583789, rhbz#589131, rhbz#588010
  Resolves: rhbz#576871, rhbz#576871, rhbz#590000, rhbz#589823

* Mon May 10 2010 Andrew Beekhof <andrew@beekhof.net> - 3.0.12-1
- New pacemaker agents upstream release: a7c0f35916bf
  + High: pgsql: properly implement pghost parameter
  + High: RA: mysql: fix syntax error
  + High: SAPInstance RA: do not rely on op target rc when monitoring clones (lf#2371)
  + High: set the HA_RSCTMP directory to /var/run/resource-agents (lf#2378)
  + Medium: IPaddr/IPaddr2: add a description of the assumption in meta-data
  + Medium: IPaddr: return the correct code if interface delete failed
  + Medium: nfsserver: rpc.statd as the notify cmd does not work with -v (thanks to Carl Lewis)
  + Medium: oracle: reduce output from sqlplus to the last line for queries (bnc#567815)
  + Medium: pgsql: implement "config" parameter
  + Medium: RA: iSCSITarget: follow changed IET access policy

* Wed Apr 21 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.11-1
- new upstream release
  Resolves: rhbz#583945, rhbz#581047, rhbz#576330, rhbz#583017
  Resolves: rhbz#583019, rhbz#583948, rhbz#584003, rhbz#582017
  Resolves: rhbz#555901, rhbz#582754, rhbz#582573, rhbz#581533
- Switch to file based Requires.
  Also address several other problems related to missing runtime
  components in different agents.
  With the current Requires: set, we guarantee all basic functionalities
  out of the box for lvm/fs/clusterfs/netfs/networking.
  Resolves: rhbz#570008

* Sat Apr 17 2010 Andrew Beekhof <andrew@beekhof.net> - 3.0.10-2
- New pacemaker agents upstream release
  + High: RA: vmware: fix set_environment() invocation (LF 2342)
  + High: RA: vmware: update to version 0.2
  + Medium: Filesystem: prefer /proc/mounts to /etc/mtab for non-bind mounts (lf#2388)
  + Medium: IPaddr2: don't bring the interface down on stop (thanks to Lars Ellenberg)
  + Medium: IPsrcaddr: modify the interface route (lf#2367)
  + Medium: ldirectord: Allow multiple email addresses (LF 2168)
  + Medium: ldirectord: fix setting defaults for configfile and ldirectord (lf#2328)
  + Medium: meta-data: improve timeouts in most resource agents
  + Medium: nfsserver: use default values (lf#2321)
  + Medium: ocf-shellfuncs: don't log but print to stderr if connected to a terminal
  + Medium: ocf-shellfuncs: don't output to stderr if using syslog
  + Medium: oracle/oralsnr: improve exit codes if the environment isn't valid
  + Medium: RA: iSCSILogicalUnit: fix monitor for STGT
  + Medium: RA: make sure that OCF_RESKEY_CRM_meta_interval is always defined (LF 2284)
  + Medium: RA: ManageRAID: require bash
  + Medium: RA: ManageRAID: require bash
  + Medium: RA: VirtualDomain: bail out early if config file can't be read during probe (Novell 593988)
  + Medium: RA: VirtualDomain: fix incorrect use of __OCF_ACTION
  + Medium: RA: VirtualDomain: improve error messages
  + Medium: RA: VirtualDomain: spin on define until we definitely have a domain name
  + Medium: Route: add route table parameter (lf#2335)
  + Medium: sfex: don't use pid file (lf#2363,bnc#585416)
  + Medium: sfex: exit with success on stop if sfex has never been started (bnc#585416)

* Fri Apr  9 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.10-1
- New rgmanager resource agents upstream release
  Resolves: rhbz#519491, rhbz#570525, rhbz#571806, rhbz#574027
  Resolves: rhbz#574215, rhbz#574886, rhbz#576322, rhbz#576335
  Resolves: rhbz#575103, rhbz#577856, rhbz#577874, rhbz#578249
  Resolves: rhbz#578625, rhbz#578626, rhbz#578628, rhbz#578626
  Resolves: rhbz#579621, rhbz#579623, rhbz#579625, rhbz#579626
  Resolves: rhbz#579059

* Wed Mar 24 2010 Andrew Beekhof <andrew@beekhof.net> - 3.0.9-2
- Resolves: rhbz#572993 - Patched build process to correctly generate ldirectord man page
- Resolves: rhbz#574732 - Add libnet-devel as a dependancy to ensure IPaddrv6 is built

* Mon Mar  1 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.9-1
- New rgmanager resource agents upstream release
  Resolves: rhbz#455300, rhbz#568446, rhbz#561862, rhbz#536902
  Resolves: rhbz#512171, rhbz#519491

* Mon Feb 22 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.8-1
- New rgmanager resource agents upstream release
  Resolves: rhbz#548133, rhbz#565907, rhbz#545602, rhbz#555901
  Resolves: rhbz#564471, rhbz#515717, rhbz#557128, rhbz#536157
  Resolves: rhbz#455300, rhbz#561416, rhbz#562237, rhbz#537201
  Resolves: rhbz#536962, rhbz#553383, rhbz#556961, rhbz#555363
  Resolves: rhbz#557128, rhbz#455300, rhbz#557167, rhbz#459630
  Resolves: rhbz#532808, rhbz#556603, rhbz#554968, rhbz#555047
  Resolves: rhbz#554968, rhbz#555047
- spec file update:
  * update spec file copyright date
  * use bz2 tarball

* Fri Jan 15 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.7-2
- Add python as BuildRequires

* Mon Jan 11 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.7-1
- New rgmanager resource agents upstream release
  Resolves: rhbz#526286, rhbz#533461

* Mon Jan 11 2010 Andrew Beekhof <andrew@beekhof.net> - 3.0.6-2
- Update Pacameker agents to upstream version: c76b4a6eb576
  + High: RA: VirtualDomain: fix forceful stop (LF 2283)
  + High: apache: monitor operation of depth 10 for web applications (LF 2234)
  + Medium: IPaddr2: CLUSTERIP/iptables rule not always inserted on failed monitor (LF 2281)
  + Medium: RA: Route: improve validate (LF 2232)
  + Medium: mark obsolete RAs as deprecated (LF 2244)
  + Medium: mysql: escalate stop to KILL if regular shutdown doesn't work

* Mon Dec 7 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.6-1
- New rgmanager resource agents upstream release
- spec file update:
  * use global instead of define
  * use new Source0 url
  * use %name macro more aggressively

* Mon Dec 7 2009 Andrew Beekhof <andrew@beekhof.net> - 3.0.5-2
- Update Pacameker agents to upstream version: bc00c0b065d9
  + High: RA: introduce OCF_FUNCTIONS_DIR, allow it to be overridden (LF2239)
  + High: doc: add man pages for all RAs (LF2237)
  + High: syslog-ng: new RA
  + High: vmware: make meta-data work and several cleanups (LF 2212)
  + Medium: .ocf-shellfuncs: add ocf_is_probe function
  + Medium: Dev: make RAs executable (LF2239)
  + Medium: IPv6addr: ifdef out the ip offset hack for libnet v1.1.4 (LF 2034)
  + Medium: add mercurial repository version information to .ocf-shellfuncs
  + Medium: build: add perl-MailTools runtime dependency to ldirectord package (LF 1469)
  + Medium: iSCSITarget, iSCSILogicalUnit: support LIO
  + Medium: nfsserver: use check_binary properly in validate (LF 2211)
  + Medium: nfsserver: validate should not check if nfs_shared_infodir exists (thanks to eelco@procolix.com) (LF 2219)
  + Medium: oracle/oralsnr: export variables properly
  + Medium: pgsql: remove the previous backup_label if it exists
  + Medium: postfix: fix double stop (thanks to Dinh N. Quoc)
  + RA: LVM: Make monitor operation quiet in logs (bnc#546353)
  + RA: Xen: Remove instance_attribute "allow_migrate" (bnc#539968)
  + ldirectord: OCF agent: overhaul

* Fri Nov 20 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.5-1
- New rgmanager resource agents upstream release
- Allow pacemaker to use rgmanager resource agents

* Wed Oct 28 2009 Andrew Beekhof <andrew@beekhof.net> - 3.0.4-2
- Update Pacameker agents to upstream version: e2338892f59f
  + High: send_arp - turn on unsolicited mode for compatibilty with the libnet version's exit codes
  + High: Trap sigterm for compatibility with the libnet version of send_arp
  + Medium: Bug - lf#2147: IPaddr2: behave if the interface is down
  + Medium: IPv6addr: recognize network masks properly
  + Medium: RA: VirtualDomain: avoid needlessly invoking "virsh define"

* Wed Oct 21 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.4-1
- New rgmanager resource agents upstream release

* Mon Oct 12 2009 Andrew Beekhof <andrew@beekhof.net> - 3.0.3-3
- Update Pacameker agents to upstream version: 099c0e5d80db
  + Add the ha_parameter function back into .ocf-shellfuncs.
  + Bug bnc#534803 - Provide a default for MAILCMD
  + Fix use of undefined macro @HA_NOARCHDATAHBDIR@
  + High (LF 2138): IPsrcaddr: replace 0/0 with proper ip prefix (thanks to Michael Ricordeau and Michael Schwartzkopff)
  + Import shellfuncs from heartbeat as badly written RAs use it
  + Medium (LF 2173): nfsserver: exit properly in nfsserver_validate
  + Medium: RA: Filesystem: implement monitor operation
  + Medium: RA: VirtualDomain: loop on status if libvirtd is unreachable
  + Medium: RA: VirtualDomain: loop on status if libvirtd is unreachable (addendum)
  + Medium: RA: iSCSILogicalUnit: use a 16-byte default SCSI ID
  + Medium: RA: iSCSITarget: be more persistent deleting targets on stop
  + Medium: RA: portblock: add per-IP filtering capability
  + Medium: mysql-proxy: log_level and keepalive parameters
  + Medium: oracle: drop spurious output from sqlplus
  + RA: Filesystem: allow configuring smbfs mounts as clones

* Wed Sep 23 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.3-1
- New rgmanager resource agents upstream release

* Thu Aug 20 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.1-1
- New rgmanager resource agents upstream release

* Tue Aug 18 2009 Andrew Beekhof <andrew@beekhof.net> - 3.0.0-16
- Create an ldirectord package
- Update Pacameker agents to upstream version: 2198dc90bec4
  + Build: Import ldirectord.
  + Ensure HA_VARRUNDIR has a value to substitute
  + High: Add findif tool (mandatory for IPaddr/IPaddr2)
  + High: IPv6addr: new nic and cidr_netmask parameters
  + High: postfix: new resource agent
  + Include license information
  + Low (LF 2159): Squid: make the regexp match more precisely output of netstat
  + Low: configure: Fix package name.
  + Low: ldirectord: add dependency on $remote_fs.
  + Low: ldirectord: add mandatory required header to init script.
  + Medium (LF 2165): IPaddr2: remove all colons from the mac address before passing it to send_arp
  + Medium: VirtualDomain: destroy domain shortly before timeout expiry
  + Medium: shellfuncs: Make the mktemp wrappers work.
  + Remove references to Echo function
  + Remove references to heartbeat shellfuncs.
  + Remove useless path lookups
  + findif: actually include the right header. Simplify configure.
  + ldirectord: Remove superfluous configure artifact.
  + ocf-tester: Fix package reference and path to DTD.

* Tue Aug 11 2009 Ville Skyttä <ville.skytta@iki.fi> - 3.0.0-15
- Use bzipped upstream hg tarball.

* Wed Jul 29 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-14
- Merge Pacemaker cluster resource agents:
  * Add Source1.
  * Drop noarch. We have real binaries now.
  * Update BuildRequires.
  * Update all relevant prep/build/install/files/description sections.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul  8 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-12
- spec file updates:
  * Update copyright header
  * final release.. undefine alphatag

* Thu Jul  2 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-11.rc4
- New upstream release.

* Sat Jun 20 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-10.rc3
- New upstream release.

* Wed Jun 10 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-9.rc2
- New upstream release + git94df30ca63e49afb1e8aeede65df8a3e5bcd0970

* Tue Mar 24 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-8.rc1
- New upstream release.
- Update BuildRoot usage to preferred versions/names

* Mon Mar  9 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-7.beta1
- New upstream release.

* Fri Mar  6 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-6.alpha7
- New upstream release.

* Tue Mar  3 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-5.alpha6
- New upstream release.

* Tue Feb 24 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-4.alpha5
- Drop Conflicts with rgmanager.

* Mon Feb 23 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-3.alpha5
- New upstream release.

* Thu Feb 19 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-2.alpha4
- Add comments on how to build this package.

* Thu Feb  5 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-1.alpha4
- New upstream release.
- Fix datadir/cluster directory ownership.

* Tue Jan 27 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-1.alpha3
  - Initial packaging
