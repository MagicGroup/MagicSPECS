%global soversion_major 1
%global soversion 1.0.41
%global _hardened_build 1

Summary: Library to control and monitor control groups
Summary(zh_CN.UTF-8): 控制和监视 cgroup 的库 
Name: libcgroup
Version: 0.41
Release: 5%{?dist}
License: LGPLv2+
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
URL: http://libcg.sourceforge.net/
Source0: http://downloads.sourceforge.net/libcg/%{name}-%{version}.tar.bz2
Source1: cgconfig.service

Patch0: fedora-config.patch
Patch1: libcgroup-0.37-chmod.patch
Patch2: libcgroup-0.40.rc1-coverity.patch
Patch3: libcgroup-0.40.rc1-fread.patch
Patch4: libcgroup-0.40.rc1-templates-fix.patch
Patch5: libcgroup-0.41-lex.patch

BuildRequires: byacc, coreutils, flex, pam-devel, systemd-units
Requires(pre): shadow-utils
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
Control groups infrastructure. The library helps manipulate, control,
administrate and monitor control groups and the associated controllers.

%package tools
Summary: Command-line utility programs, services and daemons for libcgroup
Group: System Environment/Base
Requires: %{name}%{?_isa} = %{version}-%{release}

%description tools
This package contains command-line programs, services and a daemon for
manipulating control groups using the libcgroup library.

%package pam
Summary: A Pluggable Authentication Module for libcgroup
Group: System Environment/Base
Requires: %{name}%{?_isa} = %{version}-%{release}

%description pam
Linux-PAM module, which allows administrators to classify the user's login
processes to pre-configured control group.

%package devel
Summary: Development libraries to develop applications that utilize control groups
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
It provides API to create/delete and modify cgroup nodes. It will also in the
future allow creation of persistent configuration for control groups and
provide scripts to manage that configuration.

%prep
%setup  -q  -n %{name}-%{version}
%patch0 -p1 -b .config-patch
%patch1 -p1 -b .chmod
%patch2 -p1 -b .coverity
%patch3 -p1 -b .fread
%patch4 -p1 -b .templates-fix
%patch5 -p2 -b .lex

%build
%configure --enable-pam-module-dir=%{_libdir}/security \
           --enable-opaque-hierarchy="name=systemd" \
           --disable-daemon
make %{?_smp_mflags}

%install
make DESTDIR=$RPM_BUILD_ROOT install

# install config files
install -d ${RPM_BUILD_ROOT}%{_sysconfdir}
install -m 644 samples/cgconfig.conf $RPM_BUILD_ROOT/%{_sysconfdir}/cgconfig.conf
install -m 644 samples/cgsnapshot_blacklist.conf $RPM_BUILD_ROOT/%{_sysconfdir}/cgsnapshot_blacklist.conf

# sanitize pam module, we need only pam_cgroup.so
mv -f $RPM_BUILD_ROOT%{_libdir}/security/pam_cgroup.so.*.*.* $RPM_BUILD_ROOT%{_libdir}/security/pam_cgroup.so
rm -f $RPM_BUILD_ROOT%{_libdir}/security/pam_cgroup.la $RPM_BUILD_ROOT/%{_libdir}/security/pam_cgroup.so.*

rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la

rm -f $RPM_BUILD_ROOT/%{_mandir}/man5/cgred.conf.5*
rm -f $RPM_BUILD_ROOT/%{_mandir}/man5/cgrules.conf.5*
rm -f $RPM_BUILD_ROOT/%{_mandir}/man8/cgrulesengd.8*

# install unit and sysconfig files
install -d ${RPM_BUILD_ROOT}%{_unitdir}
install -m 644 %SOURCE1 ${RPM_BUILD_ROOT}%{_unitdir}/
install -d ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig

%pre
getent group cgred >/dev/null || groupadd -r cgred

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post tools
%systemd_post cgconfig.service

%preun tools
%systemd_preun cgconfig.service

%postun tools
%systemd_postun_with_restart cgconfig.service

%triggerun -- libcgroup < 0.38
# Save the current service runlevel info
# User must manually run systemd-sysv-convert --apply cgconfig
# to migrate them to systemd targets
/usr/bin/systemd-sysv-convert --save cgconfig >/dev/null 2>&1 ||:

# Run these because the SysV package being removed won't do them
/sbin/chkconfig --del cgconfig >/dev/null 2>&1 || :
/bin/systemctl try-restart cgconfig.service >/dev/null 2>&1 || :

%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc README
%{_libdir}/libcgroup.so.*

%files tools
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc README README_systemd
%config(noreplace) %{_sysconfdir}/cgconfig.conf
%config(noreplace) %{_sysconfdir}/cgsnapshot_blacklist.conf
/usr/bin/cgcreate
/usr/bin/cgget
/usr/bin/cgset
/usr/bin/cgdelete
/usr/bin/lscgroup
/usr/bin/lssubsys
/usr/sbin/cgconfigparser
/usr/sbin/cgclear
/usr/bin/cgsnapshot
%attr(2755, root, cgred) /usr/bin/cgexec
%attr(2755, root, cgred) /usr/bin/cgclassify
%attr(0644, root, root) %{_mandir}/man1/*
%attr(0644, root, root) %{_mandir}/man5/*
%attr(0644, root, root) %{_mandir}/man8/*
%{_unitdir}/cgconfig.service

%files pam
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc README
%attr(0755,root,root) %{_libdir}/security/pam_cgroup.so

%files devel
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc README
%{_includedir}/libcgroup.h
%{_includedir}/libcgroup/*.h
%{_libdir}/libcgroup.so
%{_libdir}/pkgconfig/libcgroup.pc

%changelog
* Thu Aug 07 2014 Liu Di <liudidi@gmail.com> - 0.41-5
- 为 Magic 3.0 重建

* Thu Jul 17 2014 Tom Callaway <spot@fedoraproject.org> - 0.41-4
- fix license handling

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.41-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Mar 03 2014 jchaloup <jchaloup@redhat.com> - 0.41-2
- lex.l update: add \ character into regexp for ID token

* Tue Jan 14 2014 Peter Schiffer <pschiffe@redhat.com> 0.41-1
- resolves: #966008
  updated to 0.41
- removed deprecated cgred service
  please use Control Group Interface in Systemd instead

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.38-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Karsten Hopp <karsten@redhat.com> 0.38-6
- add BR: systemd-units

* Tue Jul 09 2013 Karsten Hopp <karsten@redhat.com> 0.38-5
- bump release and rebuild to fix some dependencies on PPC

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.38-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov 23 2012 Peter Schiffer <pschiffe@redhat.com> - 0.38-3
- resolves: #850183
  scriptlets replaced with new systemd macros (thanks to vpavlin)
- cleaned .spec file

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.38-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Feb 20 2012 Jan Safranek <jsafrane@redhat.com> 0.38-1
- updated to 0.38

* Fri Feb  3 2012 Jan Safranek <jsafrane@redhat.com> 0.38-0.rc1
- updated to 0.38.rc1

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.37.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon May 30 2011 Jan Safranek <jsafrane@redhat.com> 0.37.1-4
- fixed cgconfig service not to unmount stuff it did not mount
- added better sample cgconfig.conf file to reflect systemd
  mounting all controllers during boot (#702111)

* Wed May 25 2011 Ivana Hutarova Varekova <varekova@redhat.com> 0.37.1-3
- split tools part from libcgroup package

* Fri Apr  8 2011 Jan Safranek <jsafrane@redhat.com> 0.37.1-2
- Remove /cgroup directory, groups are created in /sys/fs/cgroup
  (#694687)

* Thu Mar  3 2011 Jan Safranek <jsafrane@redhat.com> 0.37.1-1
- Update to 0.37.1

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.37-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 17 2011 Jan Safranek <jsafrane@redhat.com> 0.37-2
- Create the 'cgred' group as system group, not as user
- Fix cgclassify exit code

* Mon Dec 13 2010 Jan Safranek <jsafrane@redhat.com> 0.37-1
- Update to 0.37
- use /sys/fs/cgroup as default directory to mount control groups (and rely on
  systemd mounting tmpfs there)

* Fri Nov 12 2010 Jan Safranek <jsafrane@redhat.com> 0.36.2-3
- Ignore systemd hierarchy - it's now invisible to libcgroup (#627378)

* Mon Aug  2 2010 Jan Safranek <jsafrane@redhat.com> 0.36.2-2
- Fix initscripts to report stopped cgconfig service as not running
  (#619091)

* Tue Jun 22 2010 Jan Safranek <jsafrane@redhat.com> 0.36.2-1
- Update to 0.36.2, fixing packaging the libraries (#605434)
- Remove the dependency on redhat-lsb (#603578)

* Fri May 21 2010 Jan Safranek <jsafrane@redhat.com> 0.36-1
- Update to 0.36.1

* Tue Mar  9 2010 Jan Safranek <jsafrane@redhat.com> 0.35-1
- Update to 0.35.1
- Separate pam module to its own subpackage

* Mon Jan 18 2010 Jan Safranek <jsafrane@redhat.com> 0.34-4
- Added README.Fedora to describe initscript integration

* Mon Oct 19 2009 Jan Safranek <jsafrane@redhat.com> 0.34-3
- Change the default configuration to mount everything to /cgroup

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.34-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul  7 2009 Jan Safranek <jsafrane@redhat.com> 0.34-1
- Update to 0.34
* Mon Mar 09 2009 Dhaval Giani <dhaval@linux.vnet.ibm.com> 0.33-3
- Add a workaround for rt cgroup controller.
* Mon Mar 09 2009 Dhaval Giani <dhaval@linux.vnet.ibm.com> 0.33-2
- Change the cgconfig script to start earlier
- Move the binaries to /bin and /sbin
* Mon Mar 02 2009 Dhaval Giani <dhaval@linux.vnet.ibm.com> 0.33-1
- Update to latest upstream
* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 0.32.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jan 05 2009 Dhaval Giani <dhaval@linux.vnet.ibm.com> 0.32.2-3
- Fix redhat-lsb dependency
* Mon Dec 29 2008 Dhaval Giani <dhaval@linux.vnet.ibm.com> 0.32.2-2
- Fix build dependencies
* Mon Dec 29 2008 Dhaval Giani <dhaval@linux.vnet.ibm.com> 0.32.2-1
- Update to latest upstream
* Thu Oct 23 2008 Dhaval Giani <dhaval@linux.vnet.ibm.com> 0.32.1-1
* Tue Feb 24 2009 Balbir Singh <balbir@linux.vnet.ibm.com> 0.33-1
- Update to 0.33, spec file changes to add Makefiles and pam_cgroup module
* Fri Oct 10 2008 Dhaval Giani <dhaval@linux.vnet.ibm.com> 0.32-1
- Update to latest upstream
* Thu Sep 11 2008 Dhaval Giani <dhaval@linux-vnet.ibm.com> 0.31-1
- Update to latest upstream
* Sat Aug 2 2008 Dhaval Giani <dhaval@linux.vnet.ibm.com> 0.1c-3
- Change release to fix broken upgrade path
* Wed Jun 11 2008 Dhaval Giani <dhaval@linux.vnet.ibm.com> 0.1c-1
- Update to latest upstream version
* Tue Jun 3 2008 Balbir Singh <balbir@linux.vnet.ibm.com> 0.1b-3
- Add post and postun. Also fix Requires for devel to depend on base n-v-r
* Sat May 31 2008 Balbir Singh <balbir@linux.vnet.ibm.com> 0.1b-2
- Fix makeinstall, Source0 and URL (review comments from Tom)
* Mon May 26 2008 Balbir Singh <balbir@linux.vnet.ibm.com> 0.1b-1
- Add a generatable spec file
* Tue May 20 2008 Balbir Singh <balbir@linux.vnet.ibm.com> 0.1-1
- Get the spec file to work
* Tue May 20 2008 Dhaval Giani <dhaval@linux.vnet.ibm.com> 0.01-1
- The first version of libcg
