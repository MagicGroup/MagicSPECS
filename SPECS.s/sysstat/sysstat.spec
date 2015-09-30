Summary: Collection of performance monitoring tools for Linux
Summary(zh_CN.UTF-8): Linux 下的性能监视工具集合
Name: sysstat
Version:	11.1.7
Release:	1%{?dist}
License: GPLv2+
Group: Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
URL: http://sebastien.godard.pagesperso-orange.fr/
Source: http://pagesperso-orange.fr/sebastien.godard/%{name}-%{version}.tar.bz2

Requires: /etc/cron.d, fileutils, grep, sh-utils, textutils
Requires(post): systemd, systemd-sysv
Requires(preun): systemd
Requires(postun): systemd

BuildRequires: %{_includedir}/linux/if.h, gettext, lm_sensors-devel, perl

%description
The sysstat package contains sar, sadf, mpstat, iostat, pidstat, nfsiostat,
cifsiostat and sa tools for Linux.
The sar command collects and reports system activity information. This
information can be saved in a file in a binary format for future inspection. The
statistics reported by sar concern I/O transfer rates, paging activity,
process-related activities, interrupts, network activity, memory and swap space
utilization, CPU utilization, kernel activities and TTY statistics, among
others. Both UP and SMP machines are fully supported.
The sadf command may be used to display data collected by sar in various formats
(CSV, XML, etc.).
The iostat command reports CPU utilization and I/O statistics for disks.
The mpstat command reports global and per-processor statistics.
The pidstat command reports statistics for Linux tasks (processes).
The nfsiostat command reports I/O statistics for network file systems.
The cifsiostat command reports I/O statistics for CIFS file systems.

%description -l zh_CN.UTF-8
Linux 下的性能监视工具集合。

%prep
%setup -q

%build
%configure --enable-install-cron --enable-copy-only --disable-file-attr \
    --disable-stripping --docdir=%{_pkgdocdir} sadc_options='-S DISK' \
    history=28 compressafter=31
make %{?_smp_mflags}

%install
%make_install
magic_rpm_clean.sh
%find_lang %{name}

%post
%systemd_post sysstat.service sysstat-collect.timer sysstat-summary.timer

%preun
%systemd_preun sysstat.service sysstat-collect.timer sysstat-summary.timer
if [[ $1 -eq 0 ]]; then
    # Remove sa logs if removing sysstat completely
    rm -rf %{_localstatedir}/log/sa/*
fi

%postun
%systemd_postun sysstat.service sysstat-collect.timer sysstat-summary.timer

%files -f %{name}.lang
%config(noreplace) %{_sysconfdir}/sysconfig/sysstat
%config(noreplace) %{_sysconfdir}/sysconfig/sysstat.ioconf
%{_bindir}/*
%{_libdir}/sa
%{_unitdir}/sysstat*
%{_mandir}/man*/*
%{_localstatedir}/log/sa
%{_docdir}/%{name}-%{version}/*

%changelog
* Tue Sep 29 2015 Liu Di <liudidi@gmail.com> - 11.1.7-1
- 更新到 11.1.7

* Wed Jan  2 2013 Peter Schiffer <pschiffe@redhat.com> - 10.1.3-1
- resolves: #890425
  updated to 10.1.3

* Mon Dec  3 2012 Peter Schiffer <pschiffe@redhat.com> - 10.1.2-2
- added new -y option to iostat command to skip first since boot report if
  displaying multiple reports

* Tue Nov 13 2012 Peter Schiffer <pschiffe@redhat.com> - 10.1.2-1
- resolves: #863791
  updated to 10.1.2
- resolves: #850333
  migrated to the new systemd-rpm macros
- cleaned .spec file

* Wed Aug 01 2012 Peter Schiffer <pschiffe@redhat.com> - 10.1.1-1
- resolves: #844387
  update to 10.1.1
- keep log files for 28 days instead of 7
- collect all aditional statistics

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 19 2012 Peter Schiffer <pschiffe@redhat.com> - 10.0.5-1
- resolves: #822867
  update to 10.0.5

* Wed May 16 2012 Peter Schiffer <pschiffe@redhat.com> - 10.0.4-1
- resolves: #803032
  update to 10.0.4
- resolves: #820725
  enable sysstat service by default

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 30 2011 Peter Schiffer <pschiffe@redhat.com> - 10.0.3-1
- resolves: #757687
  update to 10.0.3

* Tue Sep 13 2011 Tom Callaway <spot@fedoraproject.org> - 10.0.2-2
- fix libdir pathing in systemd service file

* Mon Sep 12 2011 Tom Callaway <spot@fedoraproject.org> - 10.0.2-1
- update to 10.0.2
- convert to systemd

* Tue Jun  7 2011 Ivana Hutarova Varekova <varekova@redhat.com> - 10.0.1-1
- update to 10.0.1
- remove useles patches

* Wed May  4 2011 Ivana Hutarova Varekova <varekova@redhat.com> - 10.0.0-4
- close the file descriptor in a special situation in read_uoptime function
- fix the number on open files in cifsiostat output

* Mon May  2 2011 Ivana Hutarova Varekova <varekova@redhat.com> - 10.0.0-3
- add -h optioon to iostat tool
  (-h   Make the disk stats report easier to read by a human.)

* Mon Apr  4 2011 Ivana Hutarova Varekova <varekova@redhat.com> - 10.0.0-2
- remove unnecessary patch

* Mon Apr  4 2011 Ivana Hutarova Varekova <varekova@redhat.com> - 10.0.0-1
- update to 10.0.0
  remove obsolete patches
  remove autoreconfiguration

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.0.6.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 22 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 9.0.6.1-13
- Resolves: #642280
  sar -u overflow problem - thanks Michal Srb

* Thu Oct  7 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 9.0.6.1-12
- improve sar thickless kernel support 
  (fix the output per separate cpu "-P ALL" option )

* Mon Oct  4 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 9.0.6.1-11
- resolves: #635646
  test the output of localtime properly

* Wed Sep 29 2010 jkeating - 9.0.6.1-10
- Rebuilt for gcc bug 634757

* Thu Sep 23 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 9.0.6.1-9
- add the mandir patch
- add the possibility to sed sadc cron options

* Tue Sep 21 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 9.0.6.1-8
- add necessary dependency (autoconf), necessary because of patch7

* Tue Sep 21 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 9.0.6.1-7
- remove needless DOCDIR setting
- remove needless INIT_DIR setting
- fix the problem with --disable-man-group option

* Wed Sep  8 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 9.0.6.1-6
- fix the sar output on tickless kernel

* Fri Aug 13 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 9.0.6.1-5
- remove bogus links description

* Mon Jul 19 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 9.0.6.1-4
- fix sar problem - sysstat can not monitor system status every second

* Mon Apr 19 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 9.0.6.1-3
- fix mpstat tool (when the cpu is switched off)

* Fri Apr 16 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 9.0.6.1-2
- fix the mpstat output on tickless kernel

* Tue Mar  2 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 9.0.6.1-1
- update to 9.0.6.1

* Tue Feb 16 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 9.0.6-3
- fix init script format

* Fri Dec 11 2009 Ivana Hutarova Varekova <varekova@redhat.com> - 9.0.6-2
- fix the problem in get_nfs_mount_nr function
  ( iostat -n causes stack smashing)

* Wed Dec  2 2009 Ivana Hutarva Varekova <varekova@redhat.com> - 9.0.6-1
- update to 9.0.6

* Tue Sep 15 2009 Ivana Varekova <varekova@redhat.com> - 9.0.4-4
- fix init script

* Mon Sep 14 2009 Ivana Varekova <varekova@redhat.com> - 9.0.4-3
- fix init script - add INIT INFO flags (#522740)
  and add condrestart, try-restart and force-reload (#522743)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 20 2009 Ivana Varekova <varekova@redhat.com> - 9.0.4-1
- update to 9.0.4

* Thu May 28 2009 Ivana Varekova <varekova@redhat.com> - 9.0.3-1
- update to 9.0.3
- remove obsolete patches

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.0.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Dec  5 2008 Ivana Varekova <varekova@redhat.com> - 8.0.4-6
- add /proc/diskstats reading patch

* Mon Sep 22 2008 Ivana Varekova <varekova@redhat.com> - 8.0.4-5
- Resolves: #463066 - Fix Patch0:/%%patch mismatch

* Wed Apr 23 2008 Ivana Varekova <varekova@redhat.com> - 8.0.4-4 
- Resolves: #442801 mpstat shows one extra cpu
  thanks Chris Wright

* Thu Mar  6 2008 Ivana Varekova <varekova@redhat.com> - 8.0.4-3
- add nfs extended statistic to iostat command

* Thu Feb 28 2008 Ivana Varekova <varekova@redhat.com> - 8.0.4-2
- retry write functuon in sadc command - thanks Tomas Mraz

* Fri Feb  8 2008 Ivana Varekova <varekova@redhat.com> - 8.0.4-1
- updated to 8.0.4

* Mon Dec  3 2007 Ivana Varekova <varekova@redhat.com> - 8.0.3-1
- updated to 8.0.3

* Fri Nov  9 2007 Ivana Varekova <varekova@redhat.com> - 8.0.2-3
- used macros instead of var, etc 

* Thu Nov  8 2007 Ivana Varekova <varekova@redhat.com> - 8.0.2-2
- change license tag
- remove sysstat.crond source (add -d)
- remove obsolete sysconfig file
- spec file cleanup

* Mon Nov  5 2007 Ivana Varekova <varekova@redhat.com> - 8.0.2-1
- update 8.0.2
- spec file cleanup

* Wed Oct 24 2007 Ivana Varekova <varekova@redhat.com> - 8.0.1-2
- remove useless patches

* Mon Oct 22 2007 Ivana Varekova <varekova@redhat.com> - 8.0.1-1
- update to 8.0.1
- remove useless patches
- spec file cleanup
- remove smp build flag (ar problem)
- add libdir flags 

* Wed Aug 15 2007 Ivana Varekova <varekova@redhat.com> - 7.0.4-3
- fix cve-2007-3852 -
  sysstat insecure temporary file usage

* Fri Mar 23 2007 Ivana Varekova <varekova@redhat.com> - 7.0.4-2
- fix sa2 problem (sa2 works wrong when the /var/log/sa file is 
  a link to another directory)

* Mon Feb 12 2007 Ivana Varekova <varekova@redhat.com> - 7.0.4-1
- update to 7.0.4
- spec file cleanup

* Tue Jan 30 2007 Ivana Varekova <varekova@redhat.com> - 7.0.3-3
- remove -s flag

* Mon Dec 18 2006 Ivana Varekova <varekova@redhat.com> - 7.0.3-1
- update to 7.0.3

* Tue Nov 21 2006 Ivana Varekova <varekova@redhat.com> - 7.0.2-3
- update NFS mount statistic patch 

* Wed Nov  8 2006 Ivana Varekova <varekova@redhat.com> - 7.0.2-1
- update to 7.0.2

* Thu Oct 26 2006 Ivana Varekova <varekova@redhat.com> - 7.0.0-3
- move tmp file (#208433)

* Mon Oct  9 2006 Ivana Varekova <varekova@redhat.com> - 7.0.0-2
- add NFS mount statistic (#184321)

* Fri Jul 14 2006 Marcela Maslanova <mmaslano@redhat.com> - 7.0.0-1
- new version 7.0.0

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 6.0.2-2.1
- rebuild

* Mon Jun  5 2006 Jesse Keating <jkeating@redhat.com> 6.0.2-2
- Add missing BR of gettext

* Fri May  5 2006 Ivana Varekova <varekova@redhat.com> 6.0.2-1
- update to 6.0.2
- remove asm/page.h used sysconf command to get PAGE_SIZE

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 6.0.1-3.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 6.0.1-3.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Oct 11 2005 Ivana Varekova <varekova@redhat.com> 6.0.1-3
- add FAQ to documentation (bug 170158)

* Mon Oct 10 2005 Ivana Varekova <varekova@redhat.com> 6.0.1-2
- fix chkconfig problem

* Fri Oct  7 2005 Ivana Varekova <varekova@redhat.com> 6.0.1-1
- version 6.0.1

* Thu Aug 18 2005 Florian La Roche <laroche@redhat.com>
- no need to kernel kernel 2.2 or newer anymore

* Tue May 10 2005 Ivana Varekova <varekova@redhat.com> 5.0.5-10.fc
- add debug files to debug_package

* Mon Mar  7 2005 Ivana Varekova <varekova@redhat.com> 5.0.5-9.fc
- rebuilt (add gcc4fix, update lib64ini)

* Fri Mar  4 2005 Ivana Varekova <varekova@redhat.ccm> 5.0.5-7.fc
- rebuilt

* Thu Sep 30 2004 Charles Bennett <ccb@redhat.com> 5.0.5-5.fc
- bring in filename and append-msg patch
- append-msg adds verbose text for when saNN data file cpu count
-  does not match cpu count on the currently running system

* Wed Jun 30 2004 Nils Philippsen <nphilipp@redhat.com>
- version 5.0.5
- remove some obsolete patches
- update statreset, overrun, lib64init patches
- renumber patches

* Wed Jun 16 2004 Alan Cox <alan@redhat.com>
- Fix spew of crap to console at startup
- Fix order of startup (#124035)
- Fix array overrun (#117182)
- Fix interrupt buffer sizing (caused bogus irq info)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Mar 24 2004 Justin Forbes <64bit_fedora@comcast.net> 5.0.1-2
- fix lib64 init

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Feb 18 2004 Nils Philippsen <nphilipp@redhat.com> 5.0.1-1
- version 5.0.1
- update statreset patch

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Jan 22 2004 Nils Philippsen <nphilipp@redhat.com> 5.0.0-0.6
- let user configure how long to keep logs through /etc/sysconfig/sysstat
  (#81294)
- reset stats at system boot (#102445)

* Wed Jan 21 2004 Nils Philippsen <nphilipp@redhat.com> 5.0.0-0.5
- fix ifnamsiz patch for s390x (hopefully)

* Tue Jan 20 2004 Nils Philippsen <nphilipp@redhat.com> 5.0.0-0.4
- fix insecure tmp files in scripts (#78212)
- require tools needed in scripts
- use IFNAMSIZ from {_includedir}/linux/if.h for maximum interface length

* Mon Jan 12 2004 Nils Philippsen <nphilipp@redhat.com> 5.0.0-0.3
- Buildrequires: perl
- check for %%_lib == lib64 instead of specific arches

* Mon Jan 12 2004 Nils Philippsen <nphilipp@redhat.com> 5.0.0-0.2
- fix dealing with lib64 case of cron.d file

* Mon Jan 12 2004 Nils Philippsen <nphilipp@redhat.com> 5.0.0-0.1
- version 5.0.0

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Mar  3 2003 Joe Orton <jorton@redhat.com> 4.0.7-4
- really fix paths for multilib (#82913)

* Wed Feb 19 2003 Bill Nottingham <notting@redhat.com> 4.0.7-3
- fix paths on multilib arches (#82913)

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Sat Nov 23 2002 Mike A. Harris <mharris@redhat.com> 4.0.7-1
- Updated to new upstream version 4.0.7

* Tue Nov 19 2002 Mike A. Harris <mharris@redhat.com> 4.0.5-7
- Fixed files installed in /usr/doc to be put in correct place

* Tue Oct  8 2002 Mike A. Harris <mharris@redhat.com> 4.0.5-6
- All-arch rebuild

* Tue Jul 23 2002 Trond Eivind Glomsrød <teg@redhat.com> 4.0.5-3
- Rebuild

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Jun 17 2002 Trond Eivind Glomsrød <teg@redhat.com> 4.0.5-1
- 4.0.5-1
- isag is no longer installed by default upstream, removing
  requirement on gnuplot

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Apr 22 2002 Trond Eivind Glomsrød <teg@redhat.com> 4.0.4-1
- 4.0.4
- Add an explicit requires on gnuplot (#63474)

* Fri Apr 12 2002 Trond Eivind Glomsrød <teg@redhat.com> 4.0.3-2
- Do the daily sa2 run just before midnight, not at 4AM... you'd 
  only get 4 hours worth of data that way (#63132)

* Thu Feb 28 2002 Trond Eivind Glomsrød <teg@redhat.com> 4.0.3-1
- 4.0.3

* Wed Feb 27 2002 Trond Eivind Glomsrød <teg@redhat.com> 4.0.2-3
- Rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Dec 12 2001 Trond Eivind Glomsrød <teg@redhat.com> 4.0.2-1
- 4.0.2
- the kernel patch for extended statistics is in, don't say it needs
  applying in the man page

* Mon Aug 13 2001 Preston Brown <pbrown@redhat.com>
- be more verbose about which files are corrupt (#47122)

* Mon Jul  2 2001 Preston Brown <pbrown@redhat.com>
- run sa1 from cron.d to fix run-parts interaction problem (#37733)

* Fri Jun 29 2001 Preston Brown <pbrown@redhat.com>
- upgrade to 4.0.1 stable release

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Sun Apr  8 2001 Preston Brown <pbrown@redhat.com>
- explicitly set safe umask (#35142)

* Fri Mar  9 2001 Preston Brown <pbrown@redhat.com>
- iostat disk utilization was off by a factor of 10.

* Wed Feb 14 2001 Preston Brown <pbrown@redhat.com>
- 3.3.5 brings us full support for kernel IO stats

* Tue Jan 30 2001 Preston Brown <pbrown@redhat.com>
- Summarize previous day's activity with sa2, not current day (which is only 4 hours of data when it gets run) (#24820)
- upgrade to 3.3.4 for full 2.4 compatibility and improved iostat

* Tue Jan 17 2001 Preston Brown <pbrown@redhat.com>
- iostat man page fixes

* Fri Jan 05 2001 Preston Brown <pbrown@redhat.com>
- 3.3.3, crontab fixes

* Fri Dec 29 2000 Bill Nottingham <notting@redhat.com>
- fix prereqs

* Fri Oct 13 2000 Preston Brown <pbrown@redhat.com>
- crontab entry was still incorrect.  Fixed.

* Mon Oct 09 2000 Preston Brown <pbrown@redhat.com>
- make sure disk accounting is enabled to fix iostat -l, -p (#16268)
- crontab entries were missing the user (root) to run as (#18212)

* Tue Aug 22 2000 Preston Brown <pbrown@redhat.com>
- enable IO accounting now that kernel supports it

* Wed Aug 16 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix buildrooting (#16271)

* Tue Aug 08 2000 Preston Brown <pbrown@redhat.com>
- bugfixes in 3.2.4 cause our inclusion. :)

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Thu Jun 29 2000 Preston Brown <pbrown@redhat.com>
- 3.2.3 fixes SMP race condition

* Tue Jun 20 2000 Preston Brown <pbrown@redhat.com>
- FHS macros
- 3.2.2

* Fri May 26 2000 Preston Brown <pbrown@redhat.com>
- packaged for Winston
- change va patch to indicate kernel is not patched for iostat accounting.
  re-enable if our stock kernel gets this patch.
- upgrade to 3.2.
- install crontab entry.

* Sun Dec 12 1999  Ian Macdonald <ian@caliban.org>
- upgraded to 2.2

* Fri Oct 29 1999  Ian Macdonald <ian@caliban.org>
- first RPM release (2.1)
