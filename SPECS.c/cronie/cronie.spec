%bcond_with selinux
%bcond_without pam
%bcond_with audit
%bcond_without inotify

Summary:   Cron daemon for executing programs at set times
Summary(zh_CN.UTF-8): 在指定的时间执行程序的 cron 服务
Name:      cronie
Version:	1.5.0
Release:   7%{?dist}
Patch1:    unitfile-killprocess.patch
License:   MIT and BSD and ISC and GPLv2+
Group:     System Environment/Base
Group(zh_CN.UTF-8): 系统环境/基本
URL:       https://fedorahosted.org/cronie
Source0:   https://fedorahosted.org/releases/c/r/cronie/%{name}-%{version}.tar.gz

Requires:  dailyjobs

%if %{with selinux}
Requires:      libselinux >= 2.0.64
Buildrequires: libselinux-devel >= 2.0.64
%endif
%if %{with pam}
Requires:      pam >= 1.0.1
Buildrequires: pam-devel >= 1.0.1
%endif
%if %{with audit}
Buildrequires: audit-libs-devel >= 1.4.1
%endif

BuildRequires:    systemd
Obsoletes:        %{name}-sysvinit

Requires(post):   coreutils sed
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd
Requires(post):   systemd

%description
Cronie contains the standard UNIX daemon crond that runs specified programs at
scheduled times and related tools. It is a fork of the original vixie-cron and
has security and configuration enhancements like the ability to use pam and
SELinux.

%description -l zh_CN.UTF-8
这个包是一个标准的 UNIX 服务 crond 的实现，可以在计划的时间执行指定的程序，也包括
相关的芽人。它是原来的 vixie-cron 的一个移植，包含了安全和配置的增加，比如使用 pam。

%package anacron
Summary:   Utility for running regular jobs
Summary(zh_CN.UTF-8): 运行有规律的任务的工具
Requires:  crontabs
Group:     System Environment/Base
Group(zh_CN.UTF-8): 系统环境/基本
Provides:  dailyjobs
Provides:  anacron = 2.4
Obsoletes: anacron <= 2.3
Requires(post): coreutils
Requires:  %{name} = %{version}-%{release}

%description anacron
Anacron is part of cronie that is used for running jobs with regular
periodicity which do not have exact time of day of execution.

The default settings of anacron execute the daily, weekly, and monthly
jobs, but anacron allows setting arbitrary periodicity of jobs.

Using anacron allows running the periodic jobs even if the system is often
powered off and it also allows randomizing the time of the job execution
for better utilization of resources shared among multiple systems.

%description anacron -l zh_CN.UTF-8
这是 cronie 的一部分，它用来运行那些每天运行但无准确时间的周期性程序。

默认设置支持每天、每周和每月运行程序，但可以设置任意的周期。

%package noanacron
Summary:   Utility for running simple regular jobs in old cron style
Summary(zh_CN.UTF-8): 以旧的 cron 风格运行简单的有规律程序
Group:     System Environment/Base
Group(zh_CN.UTF-8): 系统环境/基本
Provides:  dailyjobs
Requires:  crontabs
Requires:  %{name} = %{version}-%{release}

%description noanacron
Old style of running {hourly,daily,weekly,monthly}.jobs without anacron. No
extra features.

%description noanacron -l zh_CN.UTF-8
以旧的 cron 风格运行简单的有规律程序。


%prep
%setup -q
%patch1 -p1

%build
%configure \
%if %{with pam}
--with-pam \
%endif
%if %{with selinux}
--with-selinux \
%endif
%if %{with audit}
--with-audit \
%endif
%if %{with inotify}
--with-inotify \
%endif
--enable-anacron \
--enable-pie \
--enable-relro

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT DESTMAN=$RPM_BUILD_ROOT%{_mandir}
mkdir -pm700 $RPM_BUILD_ROOT%{_localstatedir}/spool/cron
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/
mkdir -pm755 $RPM_BUILD_ROOT%{_sysconfdir}/cron.d/
%if ! %{with pam}
    rm -f $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/crond
%endif
install -m 644 crond.sysconfig $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/crond
touch $RPM_BUILD_ROOT%{_sysconfdir}/cron.deny
install -m 644 contrib/anacrontab $RPM_BUILD_ROOT%{_sysconfdir}/anacrontab
install -c -m755 contrib/0hourly $RPM_BUILD_ROOT%{_sysconfdir}/cron.d/0hourly
mkdir -pm 755 $RPM_BUILD_ROOT%{_sysconfdir}/cron.hourly
install -c -m755 contrib/0anacron $RPM_BUILD_ROOT%{_sysconfdir}/cron.hourly/0anacron
mkdir -p $RPM_BUILD_ROOT/var/spool/anacron
touch $RPM_BUILD_ROOT/var/spool/anacron/cron.daily
touch $RPM_BUILD_ROOT/var/spool/anacron/cron.weekly
touch $RPM_BUILD_ROOT/var/spool/anacron/cron.monthly

# noanacron package
install -m 644 contrib/dailyjobs $RPM_BUILD_ROOT/%{_sysconfdir}/cron.d/dailyjobs

# install systemd initscript
mkdir -p $RPM_BUILD_ROOT/lib/systemd/system/
install -m 644 contrib/cronie.systemd $RPM_BUILD_ROOT/lib/systemd/system/crond.service

%post
# run after an installation
%systemd_post crond.service

%post anacron
[ -e /var/spool/anacron/cron.daily ] || touch /var/spool/anacron/cron.daily
[ -e /var/spool/anacron/cron.weekly ] || touch /var/spool/anacron/cron.weekly
[ -e /var/spool/anacron/cron.monthly ] || touch /var/spool/anacron/cron.monthly

%preun
# run before a package is removed
%systemd_preun crond.service

%postun
# run after a package is removed
%systemd_postun_with_restart crond.service

%triggerun -- cronie-anacron < 1.4.1
# empty /etc/crontab in case there are only old regular jobs
cp -a /etc/crontab /etc/crontab.rpmsave
sed -e '/^01 \* \* \* \* root run-parts \/etc\/cron\.hourly/d'\
  -e '/^02 4 \* \* \* root run-parts \/etc\/cron\.daily/d'\
  -e '/^22 4 \* \* 0 root run-parts \/etc\/cron\.weekly/d'\
  -e '/^42 4 1 \* \* root run-parts \/etc\/cron\.monthly/d' /etc/crontab.rpmsave > /etc/crontab
exit 0

%triggerun -- cronie < 1.4.7-2
# Save the current service runlevel info
# User must manually run systemd-sysv-convert --apply crond
# to migrate them to systemd targets
/usr/bin/systemd-sysv-convert --save crond

# The package is allowed to autostart:
/bin/systemctl enable crond.service >/dev/null 2>&1

/sbin/chkconfig --del crond >/dev/null 2>&1 || :
/bin/systemctl try-restart crond.service >/dev/null 2>&1 || :
/bin/systemctl daemon-reload >/dev/null 2>&1 || :

%triggerin -- pam, glibc, libselinux
# changes in pam, glibc or libselinux can make crond crash
# when it calls pam
/bin/systemctl try-restart crond.service >/dev/null 2>&1 || :

%files
%doc AUTHORS COPYING README ChangeLog
%attr(755,root,root) %{_sbindir}/crond
%attr(4755,root,root) %{_bindir}/crontab
%{_mandir}/man8/crond.*
%{_mandir}/man8/cron.*
%{_mandir}/man5/crontab.*
%{_mandir}/man1/crontab.*
%dir %{_localstatedir}/spool/cron
%dir %{_sysconfdir}/cron.d
%if %{with pam}
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/pam.d/crond
%endif
%config(noreplace) %{_sysconfdir}/sysconfig/crond
%config(noreplace) %{_sysconfdir}/cron.deny
%attr(0644,root,root) %{_sysconfdir}/cron.d/0hourly
%attr(0644,root,root) /lib/systemd/system/crond.service

%files anacron
%{_sbindir}/anacron
%attr(0755,root,root) %{_sysconfdir}/cron.hourly/0anacron
%config(noreplace) %{_sysconfdir}/anacrontab
%dir /var/spool/anacron
%ghost %verify(not md5 size mtime) /var/spool/anacron/cron.daily
%ghost %verify(not md5 size mtime) /var/spool/anacron/cron.weekly
%ghost %verify(not md5 size mtime) /var/spool/anacron/cron.monthly
%{_mandir}/man5/anacrontab.*
%{_mandir}/man8/anacron.*

%files noanacron
%attr(0644,root,root) %{_sysconfdir}/cron.d/dailyjobs

%changelog
* Sat Nov 07 2015 Liu Di <liudidi@gmail.com> - 1.5.0-7
- 为 Magic 3.0 重建

* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 1.5.0-6
- 更新到 1.5.0

* Thu Jan 16 2014 Ville Skyttä <ville.skytta@iki.fi> - 1.4.11-5
- Drop INSTALL from docs, fix rpmlint tabs vs spaces warning.

* Wed Sep 25 2013 Marcela Mašláňová <mmaslano@redhat.com> - 1.4.11-4
- some jobs are not executed because not all environment variables are set 995590
- cronie's systemd script use "KillMode=process" 919290

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 22 2013 Marcela Mašláňová <mmaslano@redhat.com> - 1.4.11-2
- scriptlets are not created correctly if systemd is not in BR 986698
- remove sub-package sysvinit, which is not needed anymore
- update license, anacron is under GPLv2+

* Thu Jul 18 2013 Marcela Mašláňová <mmaslano@redhat.com> - 1.4.11-1
- new release 1.4.11 (contains previous bug fixes from 1.4.10-5)

* Tue Jun 11 2013 Tomáš Mráz <tmraz@redhat.com> - 1.4.10-5
- add support for RANDOM_DELAY - delaying job startups
- pass some environment variables to processes (LANG, etc.) (#969761)
- do not use putenv() with string literals (#971516)

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan  2 2013 Marcela Mašláňová <mmaslano@redhat.com> - 1.4.10-3
- change configuration files to 644
- change 6755 to 4755 for crontab binary

* Tue Nov 27 2012 Marcela Mašláňová <mmaslano@redhat.com> - 1.4.10-1
- New release 1.4.10

* Thu Nov 22 2012 Marcela Mašláňová <mmaslano@redhat.com> - 1.4.9-1
- New release 1.4.9

* Wed Sep 05 2012 Václav Pavlín <vpavlin@redhat.com> - 1.4.8-13
- Scriptlets replaced with new systemd macros (#850070)

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.8-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.8-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.8-10
- Rebuilt for glibc bug#747377

* Tue Oct 25 2011 Tomáš Mráz <tmraz@redhat.com> - 1.4.8-9
- make crond run a little bit later in the boot process (#747759)

* Mon Oct 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.4.8-8
- change triggerun to fix 735802 during upgrade

* Wed Jul 27 2011 Karsten Hopp <karsten@redhat.com> 1.4.8-7
- rebuild again, ppc still had the broken rpm in the buildroots

* Thu Jul 21 2011 Rex Dieter <rdieter@fedoraproject.org> 1.4.8-6
- rebuild (broken rpm in buildroot)

* Thu Jul 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.4.8-5
- fix permission of init.d/crond

* Thu Jun 30 2011 Tomáš Mráz <tmraz@redhat.com> - 1.4.8-4
- drop the without systemd build condition
- add the chkconfig readding trigger to the sysvinit subpackage

* Wed Jun 29 2011 Tomáš Mráz <tmraz@redhat.com> - 1.4.8-3
- start crond after auditd

* Wed Jun 29 2011 Tomáš Mráz <tmraz@redhat.com> - 1.4.8-2
- fix inotify support to not leak fds (#717505)

* Tue Jun 28 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.4.8-1
- update to 1.4.8
- create sub-package sysvinit for initscript

* Mon May  9 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.4.7-3
- missing requirement on systemd-sysv for scriptlets

* Thu May 05 2011 Tomáš Mráz <tmraz@redhat.com> - 1.4.7-2
- use only systemd units with systemd
- add trigger for restart on glibc, libselinux or pam upgrades (#699189)

* Tue Mar 15 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.4.7-1
- new release 1.4.7

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.4.6-8
- enable crond even with systemctl

* Thu Dec 16 2010 Marcela Mašláňová <mmaslano@redhat.com> - 1.4.6-7
- 663193 rewritten selinux support

* Wed Dec 15 2010 Marcela Mašláňová <mmaslano@redhat.com> - 1.4.6-6
- apply selinux patch from dwalsh

* Fri Dec 10 2010 Tomas Mraz <tmraz@redhat.com> - 1.4.6-5
- do not lock jobs that fall out of allowed range - 661966

* Thu Dec 02 2010 Marcela Mašláňová <mmaslano@redhat.com> - 1.4.6-4
- fix post (thanks plautrba for review)

* Tue Nov 30 2010 Marcela Mašláňová <mmaslano@redhat.com> - 1.4.6-3
- systemd init script 617320

* Tue Nov 30 2010 Marcela Mašláňová <mmaslano@redhat.com> - 1.4.6-2
- fix typos in man pages

* Fri Oct 22 2010 Marcela Mašláňová <mmaslano@redhat.com> - 1.4.6-1
- update to 1.4.6

* Fri Aug 13 2010 Marcela Mašláňová <mmaslano@redhat.com> - 1.4.5-4
- 623908 fix fd leak in anacron, which caused denail of prelink 
  and others

* Mon Aug  9 2010 Marcela Mašláňová <mmaslano@redhat.com> - 1.4.5-2
- remove sendmail from requirements. If it's not installed, it will
 log into (r)syslog.

* Mon Aug  2 2010 Marcela Mašláňová <mmaslano@redhat.com> - 1.4.5-1
- update to new release

* Fri Feb 19 2010 Marcela Mašláňová <mmaslano@redhat.com> - 1.4.4-1
- update to new release

* Mon Feb 15 2010 Marcela Mašláňová <mmaslano@redhat.com> - 1.4.3-3
- 564894 FTBFS DSOLinking

* Thu Nov  5 2009 Marcela Mašláňová <mmaslano@redhat.com> - 1.4.3-2
- 533189 pam needs add a line and selinux needs defined one function

* Fri Oct 30 2009 Marcela Mašláňová <mmaslano@redhat.com> - 1.4.3-1
- 531963 and 532482 creating noanacron package

* Mon Oct 19 2009 Marcela Mašláňová <mmaslano@redhat.com> - 1.4.2-2
- 529632 service crond stop returns appropriate value

* Mon Oct 12 2009 Marcela Mašláňová <mmaslano@redhat.com> - 1.4.2-1
- new release

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 1.4.1-3
- rebuilt with new audit

* Fri Aug 14 2009 Tomas Mraz <tmraz@redhat.com> - 1.4.1-2
- create the anacron timestamps in correct post script

* Fri Aug 14 2009 Marcela Mašláňová <mmaslano@redhat.com> - 1.4.1-1
- update to 1.4.1
- create and own /var/spool/anacron/cron.{daily,weekly,monthly} to
 remove false warning about non existent files
- Resolves: 517398

* Wed Aug  5 2009 Tomas Mraz <tmraz@redhat.com> - 1.4-4
- 515762 move anacron provides and obsoletes to the anacron subpackage

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 20 2009 Marcela Mašláňová <mmaslano@redhat.com> - 1.4-2
- merge cronie and anacron in new release of cronie
- obsolete/provide anacron in spec

* Thu Jun 18 2009 Marcela Mašláňová <mmaslano@redhat.com> - 1.3-2
- 506560 check return value of access

* Mon Apr 27 2009 Marcela Mašláňová <mmaslano@redhat.com> - 1.3-1
- new release

* Fri Apr 24 2009 Marcela Mašláňová <mmaslano@redhat.com> - 1.2-8
- 496973 close file descriptors after exec

* Mon Mar  9 2009 Tomas Mraz <tmraz@redhat.com> - 1.2-7
- rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Dec 23 2008 Marcela Mašláňová <mmaslano@redhat.com> - 1.2-5
- 477100 NO_FOLLOW was removed, reload after change in symlinked
  crontab is needed, man updated.

* Fri Oct 24 2008 Marcela Mašláňová <mmaslano@redhat.com> - 1.2-4
- update init script

* Thu Sep 25 2008 Marcela Maslanova <mmaslano@redhat.com> - 1.2-3
- add sendmail file into requirement, cause it's needed some MTA

* Thu Sep 18 2008 Marcela Maslanova <mmaslano@redhat.com> - 1.2-2
- 462252  /etc/sysconfig/crond does not need to be executable 

* Thu Jun 26 2008 Marcela Maslanova <mmaslano@redhat.com> - 1.2-1
- update to 1.2

* Tue Jun 17 2008 Tomas Mraz <tmraz@redhat.com> - 1.1-3
- fix setting keycreate context
- unify logging a bit
- cleanup some warnings and fix a typo in TZ code
- 450993 improve and fix inotify support

* Wed Jun  4 2008 Marcela Maslanova <mmaslano@redhat.com> - 1.1-2
- 49864 upgrade/update problem. Syntax error in spec.

* Wed May 28 2008 Marcela Maslanova <mmaslano@redhat.com> - 1.1-1
- release 1.1

* Tue May 20 2008 Marcela Maslanova <mmaslano@redhat.com> - 1.0-6
- 446360 check for lock didn't call chkconfig

* Tue Feb 12 2008 Marcela Maslanova <mmaslano@redhat.com> - 1.0-5
- upgrade from less than cronie-1.0-4 didn't add chkconfig

* Wed Feb  6 2008 Marcela Maslanova <mmaslano@redhat.com> - 1.0-4
- 431366 after reboot wasn't cron in chkconfig

* Tue Feb  5 2008 Marcela Maslanova <mmaslano@redhat.com> - 1.0-3
- 431366 trigger part => after update from vixie-cron on cronie will 
  be daemon running.

* Wed Jan 30 2008 Marcela Maslanova <mmaslano@redhat.com> - 1.0-2
- change the provides on higher version than obsoletes

* Tue Jan  8 2008 Marcela Maslanova <mmaslano@redhat.com> - 1.0-1
- packaging cronie
- thank's for help with packaging to my reviewers
