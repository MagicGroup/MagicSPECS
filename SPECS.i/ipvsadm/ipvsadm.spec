Summary: Utility to administer the Linux Virtual Server
Summary(zh_CN.UTF-8): 管理 Linux 虚拟服务器的工具
Name: ipvsadm
Version: 1.26
Release: 5%{?dist}
License: GPLv2+
Group: Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
URL: http://www.linuxvirtualserver.org/software/ipvs.html
Source0: http://www.linuxvirtualserver.org/software/kernel-2.6/ipvsadm-%{version}.tar.gz
Source1: ipvsadm.service
Source2: ipvsadm-config
Patch0: ipvsadm-1.26-popt.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Buildrequires: libnl-devel
Buildrequires: popt-devel
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
# For triggerun
Requires(post): systemd-sysv

%description
ipvsadm is a utility to administer the IP Virtual Server services
offered by the Linux kernel.

%description -l zh_CN.UTF-8
这是一个管理 Linux 内核提供的 IP 虚拟服务系统的工具。

%prep
%setup -q
%patch0 -p1


%build
# Don't use _smp_mflags as it makes the build fail (1.2.4)
CFLAGS="%{optflags}" make


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/etc/rc.d/init.d
make install BUILD_ROOT=%{buildroot} MANDIR=%{_mandir}
# Remove the provided init script
rm -f %{buildroot}/etc/rc.d/init.d/ipvsadm
install -D -p -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/ipvsadm.service
# Install config file which controls the service behavior
install -D -p -m 0600 %{SOURCE2} %{buildroot}/etc/sysconfig/ipvsadm-config

mkdir -p %{buildroot}%{_sbindir}
mv %{buildroot}/sbin/* %{buildroot}%{_sbindir}

magic_rpm_clean.sh

%clean
rm -rf %{buildroot}


%post
if [ $1 -eq 1 ] ; then 
    # Initial installation 
    /usr/bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%preun
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /usr/bin/systemctl --no-reload disable ipvsadm.service > /dev/null 2>&1 || :
    /usr/bin/systemctl stop ipvsadm.service > /dev/null 2>&1 || :
fi

%postun
/usr/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /usr/bin/systemctl try-restart ipvsadm.service >/dev/null 2>&1 || :
fi

%triggerun -- ipvsadm < 1.26-4
# Save the current service runlevel info
# User must manually run systemd-sysv-convert --apply ipvsadm
# to migrate them to systemd targets
/usr/bin/systemd-sysv-convert --save ipvsadm >/dev/null 2>&1 ||:

# Run these because the SysV package being removed won't do them
/usr/sbin/chkconfig --del ipvsadm >/dev/null 2>&1 || :
/usr/bin/systemctl try-restart ipvsadm.service >/dev/null 2>&1 || :

%files
%defattr(-,root,root)
%doc README
%{_unitdir}/ipvsadm.service
%config(noreplace) /etc/sysconfig/ipvsadm-config
%{_sbindir}/ipvsadm
%{_sbindir}/ipvsadm-restore
%{_sbindir}/ipvsadm-save
%{_mandir}/man8/ipvsadm.8*
%{_mandir}/man8/ipvsadm-restore.8*
%{_mandir}/man8/ipvsadm-save.8*


%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.26-5
- 为 Magic 3.0 重建

* Thu Apr 19 2012 Jon Ciesla <limburgher@gmail.com> - 1.26-4
- Migrate to systemd, BZ 720175.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.26-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jul 11 2011 Matthias Saou <http://freshrpms.net/> 1.26-2
- Backport the init script from RHEL6, which contains lots of changes to make
  it behave simlarly to the iptables init script (#593276).

* Sat Jul  9 2011 Matthias Saou <http://freshrpms.net/> 1.26-1
- Update to 1.26 (#676167).
- Remove upstreamed Makefile and activeconns patchs, rebase popt patch.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.25-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Apr 29 2010 Matthias Saou <http://freshrpms.net/> 1.25-5
- Include patch to fix activeconns when using the netlink interface (#573921).

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.25-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.25-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Dec 24 2008 Matthias Saou <http://freshrpms.net/> 1.25-2
- Fork the included init script to be (mostly) LSB compliant (#246955).

* Mon Dec 22 2008 Matthias Saou <http://freshrpms.net/> 1.25-1
- Prepare update to 1.25 for when devel will update to kernel 2.6.28.
- Build require libnl-devel and popt-devel (+ patch to fix popt detection).

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org>
- Autorebuild for GCC 4.3

* Mon Oct 22 2007 Matthias Saou <http://freshrpms.net/> 1.24-10
- Update to latest upstream sources. Same filename, but updated content!
- Update kernhdr patch for it to still apply, update ip_vs.h from 1.2.0 to
  1.2.1 from kernel 2.6.23.1.

* Fri Aug 24 2007 Matthias Saou <http://freshrpms.net/> 1.24-9
- Spec file cleanup.
- Update License field.
- Don't "chkconfig --del" upon update.
- Add missing kernel-headers build requirement.
- Update URL and Source locations.
- Remove outdated piranha obsoletes, it has never been part of any Fedora.
- No longer mark init script as config.
- Include Makefile patch to prevent stripping and install init script.
- The init script could use a rewrite... leave that one for later.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.24-8.1
- rebuild

* Mon May 15 2006 Phil Knirsch <pknirsch@redhat.com> - 1.24-8
- Added missing prereq to chkconfig

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.24-7.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.24-7.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Mar 14 2005 Lon Hohberger <lhh@redhat.com> 1.24-7
- rebuilt

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 16 2004 Mike McLean <mikem@redhat.com> 1.24-4.2.ipvs120
- bump release

* Tue Mar 02 2004 Mike McLean <mikem@redhat.com> 1.24-4.1.ipvs120
- update to new version for 2.6 kernel

* Thu Jan 08 2004 Mike McLean <mikem@redhat.com> 1.21-10.ipvs108
- fixing a minor bug/typo in output format processing

* Wed Aug 06 2003 Mike McLean <mikem@redhat.com> 1.21-9.ipvs108
- Dropping kernel-source BuildRequires and including a local copy of 
  net/ip_vs.h to compensate.
- Incorporating some upstream changes, most notably the --sort option.

* Fri Jun 13 2003 Mike McLean <mikem@redhat.com> 1.21-8
- dropping ppc from excluded arches

* Thu Apr 4 2003 Mike McLean <mikem@redhat.com> 1.21-7
- changing %%ExcludeArch

* Thu Apr 4 2003 Mike McLean <mikem@redhat.com> 1.21-6
- added BuildRequires: kernel-source
- escaped all %% characters in %%changelog

* Mon Dec 2 2002 Mike McLean <mikem@redhat.com> 1.21-5
- Improved the description in the ipvsadm initscript.
- fixed Buildroot to use _tmppath

* Wed Aug 21 2002 Philip Copeland <bryce@redhat.com> 1.21-4
- Argh,.. %%docdir was defined which overrode what I'd
  intended to happen

* Tue Aug 1 2002 Philip Copeland <bryce@redhat.com>
- Ah... the manuals were being pushed into /usr/man
  instead of /usr/share/man. Fixed.

* Tue Jul 16 2002 Philip Copeland <bryce@redhat.com>
- Minor Makefile tweak so that we do a minimal hunt for to find
  the ip_vs.h file location

* Thu Dec 16 2001 Wensong Zhang <wensong@linuxvirtualserver.org>
- Changed to install ipvsadm man pages according to the %%{_mandir}

* Thu Dec 30 2000 Wensong Zhang <wensong@linuxvirtualserver.org>
- update the %%file section

* Thu Dec 17 2000 Wensong Zhang <wensong@linuxvirtualserver.org>
- Added a if-condition to keep both new or old rpm utility building
  the package happily.

* Tue Dec 12 2000 P.opeland <bryce@redhat.com>
- Small modifications to make the compiler happy in RH7 and the Alpha
- Fixed the documentation file that got missed off in building
  the rpm
- Made a number of -pedantic mods though popt will not compile with
  -pedantic

* Wed Aug 9 2000 Horms <horms@vergenet.net>
- Removed Obseletes tag as ipvsadm is back in /sbin where it belongs 
  as it is more or less analogous to both route and ipchains both of
  which reside in /sbin.
- Create directory to install init script into. Init scripts won't install
  into build directory unless this is done

* Thu Jul  6 2000 Wensong Zhang <wensong@linuxvirtualserver.org>
- Changed to build rpms on the ipvsadm tar ball directly

* Wed Jun 21 2000 P.Copeland <copeland@redhat.com>
- fixed silly install permission settings

* Mon Jun 19 2000 P.Copeland <copeland@redhat.com>
- Added 'dist' and 'rpms' to the Makefile
- Added Obsoletes tag since there were early versions
  of ipvsadm-*.rpm that installed in /sbin
- Obsolete tag was a bit vicious re: piranha

* Mon Apr 10 2000 Horms <horms@vergenet.net>
- created for version 1.9

