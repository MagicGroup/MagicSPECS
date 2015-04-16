Name: pcmciautils
Summary: PCMCIA utilities and initialization programs
Summary(zh_CN.UTF-8): PCMCIA 工具和初始化程序
License: GPLv2
Version: 018
Release: 4%{?dist}
Group: System Environment/Base
Group(zh_CN.UTF-8): 系统环境/基本
ExclusiveArch: i386 i586 i686 x86_64 ia64 ppc ppc64 %{?arm} mips64el
URL: http://www.kernel.org/pub/linux/utils/kernel/pcmcia/pcmcia.html
Source: http://www.kernel.org/pub/linux/utils/kernel/pcmcia/pcmciautils-%{version}.tar.bz2
Obsoletes: pcmcia-cs < 3.2.9
Obsoletes: kernel-pcmcia-cs < 3.1.32
# Do not Provide, because it would conflict
#Provides:  pcmcia-cs = 3.2.9
#Provides:  kernel-pcmcia-cs = 3.1.32
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: libsysfs-devel >= 1.3.0
Requires: udev >= 062, kernel >= 2.6.12-1.1411_FC5
BuildRequires: byacc, flex

%description
The pcmciautils package contains utilities for initializing and
debugging PCMCIA and Cardbus sockets.

%description -l zh_CN.UTF-8
PCMCIA 工具和初始化程序。

%prep
%setup -q

%build
make V=1 OPTIMIZATION="$RPM_OPT_FLAGS" STRIPCMD=: #%{?_smp_mflags}

%install
%{__rm} -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/lib/udev
cp -p src/yacc_config.c y.tab.c # for -debuginfo
magic_rpm_clean.sh

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/pcmcia/*.opts
%dir %{_sysconfdir}/pcmcia
%attr(0644,root,root) /lib/udev/rules.d/*
/sbin/pccardctl
%attr(0755,root,root) /sbin/lspcmcia
%attr(0755,root,root) /lib/udev/pcmcia-check-broken-cis
%attr(0755,root,root) /lib/udev/pcmcia-socket-startup
%{_mandir}/man*/lspcmcia*
%{_mandir}/man*/pccardctl*

%changelog
* Thu Apr 16 2015 Liu Di <liudidi@gmail.com> - 018-4
- 为 Magic 3.0 重建

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 018-3
- 为 Magic 3.0 重建

* Sat Jan 21 2012 Liu Di <liudidi@gmail.com> - 018-2
- 为 Magic 3.0 重建

* Mon May 23 2011 Harald Hoyer <harald@redhat.com> 018-1
- version 018

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 017-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue May 18 2010 Ville Skyttä <ville.skytta@iki.fi> - 017-2
- Build with $RPM_OPT_FLAGS, fix -debuginfo (#566277).

* Mon Feb 15 2010 Harald Hoyer <harald@redhat.com> 017-1
- version 017
- fix build on rawhide (bug #565133)

* Thu Aug 06 2009 Harald Hoyer <harald@redhat.com> 015-4
- add i686 buildarch

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 015-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Mar 12 2009 Harald Hoyer <harald@redhat.com> 015-2
- moved binaries for udev rules to /lib/udev

* Fri Mar 06 2009 Harald Hoyer <harald@redhat.com> 015-1
- version 015
- added buildarch i586

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 014-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 014-12
- Autorebuild for GCC 4.3

* Fri Sep 07 2007 Harald Hoyer <harald@redhat.com> - 014-11
- fixed udev rule

* Wed Aug 22 2007 Harald Hoyer <harald@redhat.com> - 014-10
- changed license tag
- added arm architecture
- removed sh execution in udev rule

* Thu Jun 21 2007 Harald Hoyer <harald@redhat.com> - 014-9
- fixed modprobe udev rule

* Wed Jun  6 2007 Harald Hoyer <harald@redhat.com> - 014-8
- fixed 'pccardctl ident' SEGV
- Resolves: rhbz#242805

* Mon Apr  2 2007 Harald Hoyer <harald@redhat.com> - 014-7
- removed Provides, because it would conflict (#234504)
- Resolves: rhbz#234504

* Fri Mar 23 2007 Harald Hoyer <harald@redhat.com> - 014-6
- specfile cleanup

* Mon Jul 17 2006 Jesse Keating <jkeating@redhat.com> - 014-5
- rebuild
- change br sysfsutils-devel to libsysfs-devel

* Mon Jun 19 2006 Harald Hoyer <harald@redhat.com> - 014-3
- changed MODALIAS to ENV{MODALIAS} in the rules file

* Wed Jun  7 2006 Harald Hoyer <harald@redhat.com> - 014-2
- better buildrequires

* Tue Jun 06 2006 Harald Hoyer <harald@redhat.com> - 014-1
- more build requires (bug #194144)
- version 014

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 011-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 011-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Dec 13 2005  Bill Nottingham <notting@redhat.com> 011-1
- update to 011, now ships with its own udev rules
- remove pcmcia-cs provide

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Sun Jul 24 2005  Bill Nottingham <notting@redhat.com> 007-1
- further udev-related tweaks (#163311)

* Thu Jul 21 2005  Bill Nottingham <notting@redhat.com> 006-2
- udev patch - right idea, awful execution. fix that (#163311)
- add requirement for 2.6.13-rc1, basically

* Wed Jul 20 2005  Bill Nottingham <notting@redhat.com> 006-1
- update to 006
- link libsysfs statically

* Fri Jul 08 2005  Bill Nottingham <notting@redhat.com> 005-1
- initial packaging
