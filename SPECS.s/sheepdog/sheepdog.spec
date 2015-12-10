Name: sheepdog
Summary: The Sheepdog Distributed Storage System for KVM/QEMU
Summary(zh_CN.UTF-8): KVM/QEMU 使用的 sheepdog 分布式存储系统
Version: 0.3.0
Release: 11%{?dist}
License: GPLv2 and GPLv2+
Group: System Environment/Base
Group(zh_CN.UTF-8): 系统环境/基本
URL: http://www.osrg.net/sheepdog
Source0: collie-sheepdog-v0.3.0-0-gbb41896.tar.gz
#get source from github here https://github.com/collie/sheepdog/tarball/v0.3.0
Source1: sheepdog.service
Patch0: update_cpg_to_cs_defines.patch

# Runtime bits
Requires: corosync 
Requires(post): chkconfig
Requires(preun): chkconfig
Requires(preun): initscripts
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
Requires(post): systemd-sysv

# Build bits
BuildRequires: autoconf automake systemd-units
BuildRequires: corosync corosynclib corosynclib-devel

BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%description
This package contains the Sheepdog server, and command line tool which offer
a distributed object storage system for KVM.

%description -l zh_CN.UTF-8
KVM/QEMU 使用的 sheepdog 分布式存储系统。

%prep
%setup -qn collie-sheepdog-bb41896
%patch0 -p1

%build
./autogen.sh
%{configure} --with-initddir=%{_initrddir}

make %{_smp_mflags}
%install
rm -rf %{buildroot}

make install DESTDIR=%{buildroot}
mkdir -p %{buildroot}/%{_unitdir}
cp -a %{SOURCE1} %{buildroot}/%{_unitdir}/
## tree fixup
# drop static libs
rm -f %{buildroot}%{_libdir}/*.a
rm -f %{buildroot}%{_initddir}/sheepdog
magic_rpm_clean.sh

%clean
rm -rf %{buildroot}

%post
if [ $1 -eq 1 ] ; then 
    # Initial installation 
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%preun
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable sheepdog.service > /dev/null 2>&1 || :
    /bin/systemctl stop sheepdog.service > /dev/null 2>&1 || :
fi

%triggerun -- sheepdog < 0.2.4-2
/usr/bin/systemd-sysv-convert --save httpd >/dev/null 2>&1 ||:
/sbin/chkconfig --del httpd >/dev/null 2>&1 || :
/bin/systemctl try-restart sheepdog.service >/dev/null 2>&1 || :
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /bin/systemctl try-restart sheepdog.service >/dev/null 2>&1 || :
fi

%files
%defattr(-,root,root,-)
%doc COPYING README
%{_sbindir}/sheep
%{_sbindir}/collie
#%attr(755,-,-)%config %{_initddir}/sheepdog
%{_unitdir}/sheepdog.service
%dir %{_localstatedir}/lib/sheepdog
%{_mandir}/man8/sheep.8*

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 0.3.0-11
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 0.3.0-10
- 为 Magic 3.0 重建

* Sun Sep 27 2015 Liu Di <liudidi@gmail.com> - 0.3.0-9
- 为 Magic 3.0 重建

* Thu Aug 07 2014 Liu Di <liudidi@gmail.com> - 0.3.0-8
- 为 Magic 3.0 重建

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Dec 21 2013 Ville Skyttä <ville.skytta@iki.fi> - 0.3.0-6
- Drop empty %%postun script.
- Drop INSTALL from docs.
- Fix bogus date in %%changelog.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Mar 16 2012 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.3.0-2
- Rebuild against new corosync (soname change).
- Add patch to fix build against new corosync headers.

* Thu Jan 12 2012 David Nalley <david@gnsa.us> - 0.3.0-1
- updating to 0.3.0

* Thu Nov 24 2011 David Nalley <david@gnsa.us> - 0.2.4-2
- adding systemd support

* Thu Nov 24 2011 David Nalley <david@gnsa.us> - 0.2.4-1
- updating to 0.2.4

* Sat Jun 04 2011 David Nalley <david@gnsa.us> - 0.2.3-2
- excluding ppc and ppc64 arch for el6

* Sat May 21 2011 David Nalley <david@gnsa.us> - 0.2.3-1
- updating to 0.2.3 to track upstream.

* Fri May 20 2011 David Nalley <david@gnsa.us> - 0.2.2-2
- removed -n from setup
- hardcoded version number. 
- changed lic from gpl to gplv2
- added INSTALL to doc
- added proper handling of initscripts

* Fri May 20 2011 Autotools generated version <nobody@nowhere.org> - 0.2.2-1
- Autotools generated version

