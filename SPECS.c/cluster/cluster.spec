###############################################################################
###############################################################################
##
##  Copyright (C) 2004-2011 Red Hat, Inc.  All rights reserved.
##
##  This copyrighted material is made available to anyone wishing to use,
##  modify, copy, or redistribute it subject to the terms and conditions
##  of the GNU General Public License v.2.
##
###############################################################################
###############################################################################

# main (empty) package
# http://www.rpm.org/max-rpm/s1-rpm-subpack-spec-file-changes.html

# keep around ready for later user
## global alphatag rc4

Name: cluster
Summary: Red Hat Cluster
Version: 3.1.7
Release: 1%{?alphatag:.%{alphatag}}%{?dist}
License: GPLv2+ and LGPLv2+
Group: System Environment/Base
URL: http://sourceware.org/cluster/wiki/
Source0: https://fedorahosted.org/releases/c/l/cluster/%{name}-%{version}.tar.xz

## Setup/build bits

BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

# Build dependencies
BuildRequires: perl python
BuildRequires: glibc-kernheaders glibc-devel
BuildRequires: libxml2-devel ncurses-devel
BuildRequires: corosynclib-devel >= 1.4.1
BuildRequires: openaislib-devel >= 1.1.4-1
BuildRequires: openldap-devel perl(ExtUtils::MakeMaker)
BuildRequires: dbus-devel zlib-devel

%prep
%setup -q -n %{name}-%{version}

%build
./configure \
  --sbindir=%{_sbindir} \
  --initddir=%{_sysconfdir}/rc.d/init.d \
  --libdir=%{_libdir} \
  --without_rgmanager \
  --disable_kernel_check

##CFLAGS="$(echo '%{optflags}')" make %{_smp_mflags}
CFLAGS="$(echo '%{optflags}')" make

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

## tree fix up
# /etc/sysconfig/cman
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
cp cman/init.d/cman.init.defaults \
   %{buildroot}%{_sysconfdir}/sysconfig/cman
# logrotate name
mv %{buildroot}%{_sysconfdir}/logrotate.d/cluster \
	%{buildroot}%{_sysconfdir}/logrotate.d/cman
# remove static libraries
find %{buildroot} -name "*.a" -exec rm {} \;
# fix library permissions or fedora strip helpers won't work.
find %{buildroot} -name "lib*.so.*" -exec chmod 0755 {} \;
# fix lcrso permissions or fedora strip helpers won't work.
find %{buildroot} -name "*.lcrso" -exec chmod 0755 {} \;
# remove docs
rm -rf %{buildroot}/usr/share/doc/cluster
# cleanup perl bindings bits
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -type f -name perllocal.pod -exec rm -f {} \;
find %{buildroot} -type f -name '*.bs' -a -empty -exec rm -f {} \;
find %{buildroot} -type f -name CCS.so -exec chmod 755 {} \;

%clean
rm -rf %{buildroot}

## Runtime and subpackages section

# main empty package
%description
Red Hat Cluster

## subpackages

%package -n cman
Group: System Environment/Base
Summary: Red Hat Cluster Manager
Requires(post): chkconfig
Requires(preun): initscripts
Requires(preun): chkconfig
Requires: corosync >= 1.4.1-2
Requires: openais >= 1.1.4-1
Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires: ricci >= 0.18.1-1 modcluster >= 0.18.1-1
Requires: fence-agents >= 3.1.5-1
Requires: fence-virt >= 0.2.3-1
Obsoletes: dlm-pcmk < 3.1.0
Provides: dlm-pcmk = %{version}
Obsoletes: resource-agents < 3.9.2-1
Requires: /usr/bin/xsltproc

%description -n cman
Red Hat Cluster Manager

%post -n cman
/sbin/chkconfig --add cman
ccs_update_schema > /dev/null 2>&1 ||:

# make sure to stop cman always as last
%preun -n cman
if [ "$1" = 0 ]; then
	/sbin/service cman stop >/dev/null 2>&1
	/sbin/chkconfig --del cman
fi

%files -n cman
%defattr(-,root,root,-)
%doc doc/COPYING.* doc/COPYRIGHT doc/README.licence doc/*.txt config/plugins/ldap/*.ldif
%doc doc/cman_notify_template.sh doc/cluster_conf.html
%dir %{_sysconfdir}/cluster
%{_sysconfdir}/rc.d/init.d/cman
%dir %{_sysconfdir}/cluster/cman-notify.d
%config(noreplace) %{_sysconfdir}/logrotate.d/cman
%config(noreplace) %{_sysconfdir}/sysconfig/cman
%{_sbindir}/ccs*
%{_sbindir}/cman*
%{_sbindir}/confdb2ldif
%{_sbindir}/dlm_controld
%{_sbindir}/dlm_tool
%{_sbindir}/fence*
%{_sbindir}/group*
%{_sbindir}/*qdisk*
/usr/libexec/*
%dir %{_datadir}/cluster
%{_datadir}/cluster/cluster.rng
%{_datadir}/cluster/checkquorum
%dir %{_datadir}/cluster/relaxng
%{_datadir}/cluster/relaxng/cluster.rng.in.head
%{_datadir}/cluster/relaxng/cluster.rng.in.tail
%{perl_vendorarch}/*
%dir /var/log/cluster
%dir /var/lib/cluster
%{_mandir}/man5/*
%{_mandir}/man8/ccs*
%{_mandir}/man8/checkquorum.8.gz
%{_mandir}/man8/cman*
%{_mandir}/man8/confdb2ldif*
%{_mandir}/man8/dlm*
%{_mandir}/man8/fence*
%{_mandir}/man8/group*
%{_mandir}/man8/*qdisk*
%{_mandir}/man3/*.3pm.gz

%package -n clusterlib
Group: System Environment/Libraries
Summary: The Red Hat Cluster libraries
Requires: udev
Conflicts: cman < 3.0.3-1
Provides: cmanlib = %{version}
Obsoletes: cmanlib < 3.0.0-5.alpha4

%description -n clusterlib
The Red Hat Cluster libraries package

%files -n clusterlib
%defattr(-,root,root,-)
%doc doc/COPYING.* doc/COPYRIGHT doc/README.licence
/lib/udev/rules.d/*-dlm.rules
%{_libdir}/libcman.so.*
%{_libdir}/libccs*.so.*
%{_libdir}/libdlm*.so.*
%{_libdir}/libfence*.so.*
%{_libdir}/liblogthread*.so.*

%post -n clusterlib -p /sbin/ldconfig

%postun -n clusterlib -p /sbin/ldconfig

%package -n clusterlib-devel
Group: Development/Libraries
Summary: The Red Hat Cluster libraries development package
Requires: clusterlib = %{version}-%{release}
Requires: pkgconfig
Provides: cman-devel = %{version}
Obsoletes: cman-devel < 3.0.0-5.alpha4
Provides: cmanlib-devel = %{version}
Obsoletes: cmanlib-devel < 3.0.0-5.alpha4

%description -n clusterlib-devel
The Red Hat Cluster libraries development package

%files -n clusterlib-devel
%defattr(-,root,root,-)
%doc doc/COPYING.* doc/COPYRIGHT doc/README.licence
%{_libdir}/libcman.so
%{_libdir}/libccs*.so
%{_libdir}/libdlm*.so
%{_libdir}/libfence*.so
%{_libdir}/liblogthread*.so
%{_includedir}/ccs.h
%{_includedir}/libcman.h
%{_includedir}/libdlm*.h
%{_includedir}/libfence.h
%{_includedir}/libfenced.h
%{_includedir}/liblogthread.h
%{_mandir}/man3/*3.gz
%{_libdir}/pkgconfig/*.pc

%changelog
* Tue Sep 27 2011 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.1.7-1
- new upstream release
- spec file update:
  Update BuildRequires and Requires to match current requirements

* Wed Aug 24 2011 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.1.6-1
- new upstream release

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 3.1.5-3
- Perl mass rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 3.1.5-2
- Perl mass rebuild

* Wed Jul 13 2011 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.1.5-1
- new upstream release
- spec file update:
  * Add Requires: /usr/bin/xsltproc
  * Bump Requires: for fence-agents and fence-virt
  * Obsolets resource-agents that do not provide xsl/relaxng infrastructure
  * ship %{_datadir}/cluster/relaxng

* Mon Jun 20 2011 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.1.3-1
- new upstream release
- spec file update:
  BuildRequires: zlib-devel

* Thu Jun 16 2011 Marcela Mašláňová <mmaslano@redhat.com> - 3.1.1-2
- Perl mass rebuild

* Tue Mar  8 2011 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.1.1-1
- New upstream release
- spec file update:
  BuildRequires: dbus-devel
  clusterlib now Requires: udev and rules are in /lib/udev
  Drop systemd workaround, now upstream

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec  8 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.1.0-6
- Drop circular dependency on gfs2-cluster

* Fri Dec  3 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.1.0-5
- Obsoletes/Provides dlm-pcmk from cman

* Fri Dec  3 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.1.0-4
- Add patch to workaround systemd limitations (patch stolen from upstream)

* Fri Dec  3 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.1.0-3
- Use less restrictive Requires on corosync for Fedora

* Thu Dec  2 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.1.0-2
- Switch to .xz tarballs

* Thu Dec  2 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.1.0-1
- new upstream release
  Resolves: rhbz#584140, rhbz#624844, rhbz#619874, rhbz#645830
  Resolves: rhbz#639103
- spec file update:
  Update upstream URL
  Remove ringid.patch, now fully merged upstream
  Update BuildRequires and Requires to match current requirements
  Drop pacemaker bits build and -pcmk package variants
  (pacemaker now built with cman support)
  Update ./configure invokation
  Stop shipping /var/run/cluster (Resolves: rhbz#656559)
  Stop shipping gfs2-utils (now standalone package/upstream)
  Requires gfs2-cluster for rolling upgrade compatibility vs gfs2-utils split

* Thu Oct  6 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.17-1
- new upstream release
  Resolves: rhbz#632595, rhbz#633856, rhbz#632385, rhbz#628013
  Resolves: rhbz#621313, rhbz#595383, rhbz#580492, rhbz#605733
  Resolves: rhbz#636243, rhbz#591003, rhbz#637913, rhbz#634718
  Resolves: rhbz#617247, rhbz#617247, rhbz#617234, rhbz#631943
  Resolves: rhbz#639018

* Thu Sep  2 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.16-1
- new upstream release
  Resolves: rhbz#619096, rhbz#614046, rhbz#620679, rhbz#619680
  Resolves: rhbz#621562, rhbz#621694, rhbz#608887, rhbz#622844
  Resolves: rhbz#623810, rhbz#617306, rhbz#623816, rhbz#624691
  Resolves: rhbz#622576
- spec file update:
  Ship cluster_conf.html documentation.

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
- spec file update:
  * Requires corosync with totem timer check disabled.
  * Ship /etc/sysconfig/cman.
  * Temporary add BR to workaround cluster-glue-libs-devel

* Mon Jun  7 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.13-1
- new upstream release
  Resolves: rhbz#592103, rhbz#593108, rhbz#578617, rhbz#594626
  Resolves: rhbz#594511, rhbz#596046, rhbz#594111, rhbz#597002
  Resolves: rhbz#599643

* Tue Jun 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 3.0.12-3
- Mass rebuild with perl-5.12.0

* Mon May 17 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.12-2
- Use cpg ringid (ringid.patch)
- spec file update:
  * Requires/BuildRequires corosync + cpg ringid patch.
- all cpg ringid patches are upstream but not part of a tarball release
  Resolves: rhbz#584140

* Mon May 10 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.12-1
- new upstream release
  Resolves: rhbz#585217, rhbz#586100, rhbz#581533, rhbz#582753
  Resolves: rhbz#582754, rhbz#585083, rhbz#587079, rhbz#588890
  Resolves: rhbz#588925, rhbz#583789, rhbz#589131, rhbz#588010
  Resolves: rhbz#576871, rhbz#576871, rhbz#590000, rhbz#589823
- spec file update:
  * Fix bug reference in 3.0.11 changelog entry
  * Ship cman_notify_template.sh documentation

* Wed Apr 21 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.11-1
- new upstream release
  Drop gfs2_fix_build_with_new_kernels.patch
  Resolves: rhbz#583945, rhbz#581047, rhbz#576330, rhbz#583017
  Resolves: rhbz#583019, rhbz#583948, rhbz#584003, rhbz#582017
  Resolves: rhbz#555901, rhbz#582754, rhbz#582753, rhbz#581533

* Fri Apr  9 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.10-1
- new upstream release
  Resolves: rhbz#519491, rhbz#570525, rhbz#571806, rhbz#574027
  Resolves: rhbz#574215, rhbz#574886, rhbz#576322, rhbz#576335
  Resolves: rhbz#575103, rhbz#577856, rhbz#577874, rhbz#578249
  Resolves: rhbz#578625, rhbz#578626, rhbz#578628, rhbz#578626
  Resolves: rhbz#579621, rhbz#579623, rhbz#579625, rhbz#579626
  Resolves: rhbz#579059
- Add gfs2_fix_build_with_new_kernels.patch to build with
  more recent kernels > 2.6.33 (patch is already upstream).
  Resolves: rhbz#581038

* Mon Mar  1 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.9-1
- new upstream release
  Resolves: rhbz#455300, rhbz#568446, rhbz#561862, rhbz#536902
  Resolves: rhbz#512171, rhbz#519491
- spec file update:
  cman should Requires fence-virt directly

* Mon Feb 22 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.8-1
- new upstream release
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
  * bump minimum requirements for corosync/openais

* Tue Jan 12 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.7-1
- New upstream release
  Resolves: rhbz#536902, rhbz#545801, rhbz#528786

* Tue Jan  6 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.6-2
- Drop gfs-utils commodity package

* Mon Dec  7 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.6-1
- New upstream release
- spec file update:
  * use global instead of define
  * use new Source0 url
  * use %name macro more aggressively
  * bump Requires on fence-agents
  * ship var/run/cluster and var/lib/cluster

* Fri Nov 20 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.5-1
- New upstream release
- spec file update:
  * drop BuildRequires on slang-devel.

* Wed Oct 21 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.4-1
- New upstream release
- spec file update:
  * explicitly Requires newer version of fence-agents

* Fri Oct  2 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.3-2
- spec file update:
  * gfs-pcmk now Requires dlm-pcmk

* Fri Sep 25 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.3-1
- New upstream release
- spec file updates:
  * drop cp_workaround patch
  * stop shipping rgmanager from cluster
  * move dlm udev rules in clusterlib where they belong
  * enable pacemaker components build
  * ship 2 new rpms: dlm-pcmk and gfs-pcmk for pacemaker integration

* Mon Aug 24 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.2-2
- Add temporary workaround to install symlinks

* Mon Aug 24 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.2-1
- New upstream release

* Thu Aug 20 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.1-1
- New upstream release

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.0-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul  8 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-20
- New upstream release
- spec file updates:
  * Update copyright header
  * final release.. undefine alphatag
  * BuildRequires and Requires corosync/openais 1.0.0-1 final.

* Thu Jul  2 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-19.rc4
- New upstream release
- spec file updates:
  * cman subpackage: avoid unnecessary calls to ldconfig
  * rgmanager subpackage: drop unrequired Requires: that belong to ras
  * BuildRequires and Requires corosync/openais 1.0.0.rc1

* Sat Jun 20 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-18.rc3
- New upstream release
- spec file updates:
  * Drop local patches.
  * Update BuildRequires and Requires: on newer corosync/openais.

* Thu Jun 11 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-17.rc2
- Update from git up to 779dd3c23ca6c56f5b3f7a8a7831bae775c85201
- spec file updates:
  * Drop BuildRequires on libvolume_id-devel that's now obsoleted
  * gfs*-utils now Requires: file
  * Add temporary patch to get rid of volume_id references in the code

* Wed Jun 10 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-16.rc2
- New upstream release + git94df30ca63e49afb1e8aeede65df8a3e5bcd0970
- spec file updates:
  * BuildRequires / Requires: latest corosync and openais
  * Update configure invokation
  * Cleanup tree fix up bits that are now upstream
  * Ship cluster.rng
  * Move fsck/mkfs gfs/gfs2 binaries in /sbin to be FHS compliant

* Tue Mar 24 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-15.rc1
- New upstream release.
- Update corosync/openais BuildRequires and Requires.
- Drop --corosynclibdir from configure. Libs are now in standard path.
- Update BuildRoot usage to preferred versions/names
- Drop qdisk init script. Now merged in cman init from upstream.

* Mon Mar  9 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-14.alpha7
- New upstream release.
- Update corosync/openais BuildRequires and Requires.
- Fix gfs-utils and cman man page overlapping files.

* Fri Mar  6 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-13.alpha7
- New upstream release.
- Drop local build fix patch.

* Tue Mar  3 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-12.alpha6
- New upstream release.
- Add missing LICENCE and COPYRIGHT files from clusterlib-devel.
- Add patch to fix build failure (already upstream).

* Tue Feb 24 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-11.alpha5
- Stop building fence and resource agents.
- cman now Requires: fence-agents.
- rgmanager now Requires: resource-agents.

* Tue Feb 24 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-10.alpha5
- Fix typo in gfs-utils preun scriptlet.
- Fix gfs-utils file list.

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.0-9.alpha5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 23 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-8.alpha5
- New upstream release.

* Thu Feb 19 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-7.alpha4
- Update to latest stable3 code from git (e3a9ac674fa0ff025e833dcfbc8575cada369843)
- Fix Provides: version.
- Update corosync/openais BuildRequires and Requires

* Fri Feb  6 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-6.alpha4
- Fix datadir/fence directory ownership.

* Sat Jan 31 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-5.alpha4
- New upstream release.
- Fix directory ownership #483330.
- Add support pkgconfig to devel package.
- Total libraries cleanup:
  - split libraries out of cman into clusterlib.
  - merge cmanlib into clusterlib.
  - rename cman-devel into clusterlib-devel.
  - merge cmanlib-devel into clusterlib-devel.
- Comply with multiarch requirements (libraries).
- Relax BuildRequires and Requires around corosync and openais.

* Tue Jan 27 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-4.alpha3
- New upstream release

* Wed Jan 21 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-3.alpha2
- Move all binaries where they belong. All the legacy stuff is now dead.

* Mon Jan 12 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-2.alpha2
- New upstream release (retag cvs package)

* Mon Jan 12 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-1.alpha2
- New upstream release

* Wed Dec 17 2008 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-1.alpha1
- New upstream release.
- Fix legacy code build.
- Fix wrong conffile attribute.

* Mon Dec 15 2008 Fabio M. Di Nitto <fdinitto@redhat.com> - 2.99.13-1
- New upstream release.
- Drop gnbd* packages that are now a separate project.
- Tight dependencies with corosync/openais.

* Mon Dec 01 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.99.12-2
- Rebuild for Python 2.6

* Mon Nov  3 2008 Fabio M. Di Nitto <fdinitto@redhat.com> - 2.99.12-1
- new upstream release.
  Fix several security related issues.

* Mon Oct 20 2008 Fabio M. Di Nitto <fdinitto@redhat.com> - 2.99.11-1
- new upstream release.
- drop obsoleted patches.
- include very important gfs1 bug fix.
- include fix for fence_egenera (CVE-2008-4192).

* Wed Oct  8 2008 Fabio M. Di Nitto <fdinitto@redhat.com> - 2.99.10-6
- cman init: add fix from upstream for cman_tool wrong path.

* Fri Sep 26 2008 Fabio M. Di Nitto <fdinitto@redhat.com> - 2.99.10-5
- cman now Requires: ricci and modcluster.

* Fri Sep 26 2008 Fabio M. Di Nitto <fdinitto@redhat.com> - 2.99.10-4
- Split libcman.so* from cman and cman-devel into  cmanlib and cmanlib-devel
  to break a very annoying circular dependency.

* Thu Sep 25 2008 Fabio M. Di Nitto <fdinitto@redhat.com> - 2.99.10-3
- The "CVS HATES ME" release.
- New upstream release.
- Build against new corosync and openais.
- specfile cleanup: rename buildxen to buildvirt.

* Thu Sep 25 2008 Fabio M. Di Nitto <fdinitto@redhat.com> - 2.99.10-2
- Retag release.
- New upstream release.
- Build against new corosync and openais.
- specfile cleanup: rename buildxen to buildvirt.

* Thu Sep 25 2008 Fabio M. Di Nitto <fdinitto@redhat.com> - 2.99.10-1
- New upstream release.
- Build against new corosync and openais.
- specfile cleanup: rename buildxen to buildvirt.

* Wed Sep 03 2008 Jesse Keating <jkeating@redhat.com> - 2.99.08-3
- Rebuild for broken deps.
- Pull in upstream patches for libvolume_id changes

* Wed Sep 03 2008 Jesse Keating <jkeating@redhat.com> - 2.99.08-2
- Rebuild for broken deps.

* Tue Aug 12 2008 Fabio M. Di Nitto <fdinitto@redhat.com> - 2.99.08-1
- New upstream release.
- Drop local patch that's part of upstream.
- Tight BR and Requires for openais to a very specific version.
- cman Requires ricci as new default config distribution system.
  (ricci changes will land soon but in the meantime this is done our side)

* Fri Aug  1 2008 Fabio M. Di Nitto <fdinitto@redhat.com> - 2.99.07-1
- New upstream release.
- Add patch to build against new headers (already part of upstream next release)
- BR on perl(ExtUtils::MakeMaker) to build perl bindings
- Fix logrotate install from upstream
- Add "clean up after perl bindings" snippet
- Update Requires for perl bindings
- Properly split man3 man pages

* Tue Jul 15 2008 Fabio M. Di Nitto <fdinitto@redhat.com> - 2.99.06-1
- New upstream release.
- BR on new openais for logging features.
- drop local logrotate snippet in favour of upstream one.
- cman Requires: PyOpenSSL for telnet_ssl wrapper.
- cman Requires: pexpect and net-snmp-utils for fence agents.
  Thanks to sendro on IRC for spotting the issue.
- Another cleanup round for docs

* Tue Jun 24 2008 Fabio M. Di Nitto <fdinitto@redhat.com> - 2.99.05-1
- New upstream release
- Update licence tags again after upstream relicensing to kill OSL 2.1.
- Add 2 commodity packages (gfs-utils and gnbd-utils). They both
  require external kernel modules but at least userland will stay
  automatically in sync for our users.
- BR openais 0.84 for new logsys symbols (and requires for runtime).
- Update build section to enable gfs-utils and gnbd-utils.

* Mon Jun  9 2008 Fabio M. Di Nitto <fdinitto@redhat.com> - 2.99.04-1
- New upstream release
- Update license tags after major upstream cleanup (note: rgmanager
  includes a shell script that is shipped under OSL 2.1 license).
- Update inclusion of documents to reflect updated COPYRIGHT file
  from upstream.
- Add documentation to different packages.

* Mon Jun  2 2008 Fabio M. Di Nitto <fdinitto@redhat.com> - 2.99.03-1
- New upstream release
- cman Requires telnet and ssh client
- drops some tree fix up bits that are now upstream

* Fri May 23 2008 Fabio M. Di Nitto <fdinitto@redhat.com> - 2.99.02-4
- Add missing OpenIPMI requires to cman for fence_ipmilan

* Thu May 22 2008 Fabio M. Di Nitto <fdinitto@redhat.com> - 2.99.02-3
- New kernel-headers has what we need release.
- Drop BR on kernel-devel.
- Drop cluster-dlmheaders.patch.
- Drop --kernel_* from configure invokation.
- Cleanup a few comments in the spec file.

* Tue May 20 2008 Fabio M. Di Nitto <fdinitto@redhat.com> - 2.99.02-2
- disable parallel build (broken upstream)
- build requires higher openais (fix ppc64 build failure)

* Mon May 19 2008 Fabio M. Di Nitto <fdinitto@redhat.com> - 2.99.02-1
- New upstream release
- Shut up the last few rpmlint warnings

* Wed May 15 2008 Fabio M. Di Nitto <fdinitto@redhat.com> - 2.99.01-4
- Fix typo in rgmanager Summary

* Wed May 14 2008 Fabio M. Di Nitto <fdinitto@redhat.com> - 2.99.01-3
- Fix rgmanager License: tag.

* Wed May 14 2008 Fabio M. Di Nitto <fdinitto@redhat.com> - 2.99.01-2
- Drop BR on openais as it is pulled by openais-devel.
- Change postun section to use -p /sbin/ldconfig.
- Fix rgmanager Requires.

* Wed May 14 2008 Fabio M. Di Nitto <fdinitto@redhat.com> - 2.99.01-1
- Initial packaging.
