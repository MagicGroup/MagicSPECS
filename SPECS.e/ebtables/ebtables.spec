%global ebminor 4

Name:			ebtables
Version:		2.0.10
Release:		17%{?dist}
Summary:		Ethernet Bridge frame table administration tool
Summary(zh_CN.UTF-8): 	以太网桥接帧表管理工具
License:		GPLv2+
Group:			System Environment/Base
Group(zh_CN.UTF-8): 	系统环境/基本
URL:			http://ebtables.sourceforge.net/
Source0:		http://downloads.sourceforge.net/ebtables/ebtables-v%{version}-%{ebminor}.tar.gz
Source1:		ebtables-save
Source2:		ebtables.systemd
Source3:		ebtables.service
Patch0:			ebtables-2.0.10-norootinst.patch
Patch3:			ebtables-2.0.9-lsb.patch
Patch4:			ebtables-2.0.10-linkfix.patch
Patch5:			ebtables-2.0.0-audit.patch
# Upstream commit 5e126db0f
Patch6:			0001-add-RARP-and-update-iana-url.patch
BuildRequires:		systemd-units
Requires(post):		systemd
Requires(preun):	systemd
Requires(postun):	systemd

%description
Ethernet bridge tables is a firewalling tool to transparently filter network
traffic passing a bridge. The filtering possibilities are limited to link
layer filtering and some basic filtering on higher network layers.

This tool is the userspace control for the bridge and ebtables kernel
components (built by default in Fedora kernels).

The ebtables tool can be used together with the other Linux filtering tools,
like iptables. There are no known incompatibility issues.

%description -l zh_CN.UTF-8
以太网桥接帧表管理工具。

%prep
%setup -q -n ebtables-v%{version}-%{ebminor}
%patch0 -p1 -b .norootinst
%patch3 -p1 -b .lsb
# extension modules need to link to libebtc.so for ebt_errormsg
%patch4 -p1 -b .linkfix
%patch5 -p1 -b .AUDIT
%patch6 -p1 -b .RARP

# Convert to UTF-8
f=THANKS; iconv -f iso-8859-1 -t utf-8 $f -o $f.utf8 ; mv $f.utf8 $f

%build
make %{?_smp_mflags} CFLAGS="${RPM_OPT_FLAGS}" LIBDIR="/%{_lib}/ebtables" BINDIR="/sbin" MANDIR="%{_mandir}" LDFLAGS="${RPM_LD_FLAGS} -Wl,-z,now"

%install
mkdir -p %{buildroot}%{_initrddir}
mkdir -p %{buildroot}%{_unitdir}
install -p %{SOURCE3} %{buildroot}%{_unitdir}/
chmod -x %{buildroot}%{_unitdir}/*.service
mkdir -p %{buildroot}%{_libexecdir}
install -m0755 %{SOURCE2} %{buildroot}%{_libexecdir}/ebtables
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
make DESTDIR="%{buildroot}" LIBDIR="/%{_lib}/ebtables" BINDIR="/sbin" MANDIR="%{_mandir}" install
touch %{buildroot}%{_sysconfdir}/sysconfig/ebtables.filter
touch %{buildroot}%{_sysconfdir}/sysconfig/ebtables.nat
touch %{buildroot}%{_sysconfdir}/sysconfig/ebtables.broute

# Do not need the sysvinit
rm -rf %{buildroot}%{_initrddir}

# install ebtables-save bash script
rm -f %{buildroot}/sbin/ebtables-save
install %{SOURCE1} %{buildroot}/sbin/ebtables-save

# move libebtc.so into the ldpath
mv %{buildroot}/%{_lib}/ebtables/libebtc.so %{buildroot}/%{_lib}/

%post
%systemd_post ebtables.service
/sbin/ldconfig

%preun
%systemd_preun ebtables.service

%postun
%systemd_postun_with_restart ebtables.service
/sbin/ldconfig

%files
%defattr(-, root, root, 0755)
%doc ChangeLog COPYING THANKS
%doc %{_mandir}/man8/ebtables.8*
%config(noreplace) %{_sysconfdir}/ethertypes
%config(noreplace) %{_sysconfdir}/sysconfig/ebtables-config
%{_unitdir}/ebtables.service
%{_libexecdir}/ebtables
/%{_lib}/libebtc.so
/%{_lib}/ebtables/
/sbin/ebtables*
%ghost %{_sysconfdir}/sysconfig/ebtables.filter
%ghost %{_sysconfdir}/sysconfig/ebtables.nat
%ghost %{_sysconfdir}/sysconfig/ebtables.broute

%changelog
* Sat Nov 07 2015 Liu Di <liudidi@gmail.com> - 2.0.10-17
- 为 Magic 3.0 重建

* Thu Oct 29 2015 Liu Di <liudidi@gmail.com> - 2.0.10-16
- 为 Magic 3.0 重建

* Fri Jun 20 2014 Liu Di <liudidi@gmail.com> - 2.0.10-15
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.10-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Mar 31 2014 Tom Callaway <spot@fedoraproject.org> - 2.0.10-13
- use standard optflags and ldflags (bz 1071993)

* Wed Feb 19 2014 Tom Callaway <spot@fedoraproject.org> - 2.0.10-12
- remove executable bit from systemd service file
- add RARP type to ethertypes (bz 1060537)

* Wed Aug 21 2013 Tom Callaway <spot@fedoraproject.org> - 2.0.10-11
- convert to systemd

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.10-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 21 2013 Tom Callaway <spot@fedoraproject.org> - 2.0.10-8
- add audit module

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.10-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Apr  5 2012 Tom Callaway <spot@fedoraproject.org> - 2.0.10-5
- update to 2.0.10-4 (upstream numbering is goofy)
- fix missing symbol issue with extension modules (bz810006)

* Thu Feb 16 2012 Thomas Woerner <twoerner@redhat.com> - 2.0.10-4
- replaced ebtables-save perl script by bash script to get rid of the perl 
  requirement

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Aug 11 2011 Tom Callaway <spot@fedoraproject.org> - 2.0.10-2
- update to 2.0.10-2

* Mon Jul 11 2011 Tom Callaway <spot@fedoraproject.org> - 2.0.10-1
- update to 2.0.10-1

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Feb 15 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 2.0.9-5
- update to 2.0.9-2

* Fri Jan 29 2010 Thomas Woerner <twoerner@redhat.com> - 2.0.9-4
- moved ebtables modules to /lib[64]/ebtables (rhbz#558886)

* Fri Jan 15 2010 Thomas Woerner <twoerner@redhat.com> - 2.0.9-3
- fixed init script to be lsb conform (rhbz#536828)
- fixed download link according to package review

* Wed Aug 19 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2.0.9-2
- fix source0 url

* Mon Jul 27 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2.0.9-1
- update to 2.0.9

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.0.8-5
- Autorebuild for GCC 4.3

* Sun Oct 28 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.8-4
- bump to 2.0.8-2 from upstream
- keep _libdir/ebtables, even though upstream just moved away from it.

* Thu Aug 23 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.8-3
- use _libdir/ebtables to match upstream RPATH (bugzilla 248865)
- correct license tag
- use upstream init script
- enable build-id
- use cflags for all compiles
- be sane with DESTDIR

* Mon Jul  9 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.8-2
- remove "Fedora Core" reference in spec

* Mon Jul  2 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.8-1
- final 2.0.8 release

* Wed Jan 17 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.8-0.8.rc3
- fix release order

* Wed Jan 17 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.8-0.1.rc3
- bump to rc3

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 2.0.8-0.7.rc2
 - rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Mon Sep 18 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.8-0.6.rc2
- fix versioning

* Thu Sep 14 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.8-0.3.rc2
- fix bugzilla 206257

* Tue Sep 12 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.8-0.2.rc2
- fix for FC-6

* Mon Apr 24 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.8-0.1.rc2
- bump to rc2

* Sun Apr  2 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.8-0.5.rc1
- learn to use "install" correctly. :/

* Sun Apr  2 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.8-0.4.rc1
- package up the shared libs too

* Wed Mar 29 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.8-0.3.rc1
- use -fPIC

* Wed Mar 29 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.8-0.2.rc1
- broken tagging

* Tue Jan 10 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.8-0.1.rc1
- bump to 2.0.8-rc1

* Mon Jul  4 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.6-7
- buildsystem error requires artificial release bump

* Mon Jul  4 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.6-6
- actually touch ghosted files

* Fri Jul  1 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.6-5
- fix sysv file

* Fri Jul  1 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.6-4
- remove INSTALL file
- add some text to description, correct typos
- fix %%postun
- add PreReqs
- add %%ghost config files

* Tue May 31 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.6-3
- reworked for Fedora Extras
- add gcc4 fix
- move init file into SOURCE1

* Thu Dec 02 2004 Dag Wieers <dag@wieers.com> - 2.0.6-2
- Added patch for gcc 3.4. (Nigel Smith)

* Tue Apr 27 2004 Dag Wieers <dag@wieers.com> - 2.0.6-2
- Cosmetic changes.

* Tue Apr 27 2004 Dag Wieers <dag@wieers.com> - 2.0.6-1
- Initial package. (using DAR)
