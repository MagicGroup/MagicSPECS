Summary:    A Router Advertisement daemon
Name:       radvd
Version:    1.12
Release: 1%{?dist}
# The code includes the advertising clause, so it's GPL-incompatible
License:    BSD with advertising
Group:      System Environment/Daemons
URL:        http://www.litech.org/radvd/
Source0:    %{url}dist/%{name}-%{version}.tar.gz
Source1:    radvd-tmpfs.conf
Source2:    radvd.service
BuildRequires:      byacc
BuildRequires:      flex
BuildRequires:      flex-static
BuildRequires:      libdaemon-devel
BuildRequires:      pkgconfig
BuildRequires:      systemd-units
Requires(postun):   systemd-units
Requires(preun):    systemd-units
Requires(post):     systemd-units
Requires(pre):      shadow-utils

%description
radvd is the router advertisement daemon for IPv6.  It listens to router
solicitations and sends router advertisements as described in "Neighbor
Discovery for IP Version 6 (IPv6)" (RFC 2461).  With these advertisements
hosts can automatically configure their addresses and some other
parameters.  They also can choose a default router based on these
advertisements.

Install radvd if you are setting up IPv6 network and/or Mobile IPv6
services.

%prep
%setup -q
for F in CHANGES; do
    iconv -f iso-8859-1 -t utf-8 < "$F" > "${F}.new"
    touch -r "$F" "${F}.new"
    mv "${F}.new" "$F"
done

%build
export CFLAGS="$RPM_OPT_FLAGS -fPIE" 
export LDFLAGS='-pie -Wl,-z,relro,-z,now,-z,noexecstack,-z,nodlopen'
%configure --with-pidfile=%{_localstatedir}/run/radvd/radvd.pid
make %{?_smp_mflags} 

%install
make DESTDIR=$RPM_BUILD_ROOT install

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/run/radvd
mkdir -p $RPM_BUILD_ROOT%{_unitdir}

install -m 644 redhat/radvd.conf.empty $RPM_BUILD_ROOT%{_sysconfdir}/radvd.conf
install -m 644 redhat/radvd.sysconfig $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/radvd

install -d -m 755 $RPM_BUILD_ROOT%{_tmpfilesdir}
install -p -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_tmpfilesdir}/radvd.conf
install -m 644 %{SOURCE2} ${RPM_BUILD_ROOT}%{_unitdir}

%postun
%systemd_postun_with_restart radvd.service

%post
%systemd_post radvd.service

%preun
%systemd_preun radvd.service

# Static UID and GID defined by /usr/share/doc/setup-*/uidgid
%pre
getent group radvd >/dev/null || groupadd -r -g 75 radvd
getent passwd radvd >/dev/null || \
  useradd -r -u 75 -g radvd -d / -s /sbin/nologin -c "radvd user" radvd
exit 0

%files
%doc CHANGES COPYRIGHT INTRO.html README TODO
%{_unitdir}/radvd.service
%config(noreplace) %{_sysconfdir}/radvd.conf
%config(noreplace) %{_sysconfdir}/sysconfig/radvd
%{_tmpfilesdir}/radvd.conf
%dir %attr(-,radvd,radvd) %{_localstatedir}/run/radvd/
%doc radvd.conf.example
%{_mandir}/*/*
%{_sbindir}/radvd
%{_sbindir}/radvdump

%changelog
* Thu Jun 12 2014 Pavel Šimerda <psimerda@redhat.com> - 1.12-1
- new version 1.12

* Fri Jun 06 2014 Pavel Šimerda <psimerda@redhat.com> - 1.11-1
- new version 1.11

* Mon Mar 24 2014 Pavel Šimerda <psimerda@redhat.com> - 1.10.0-2
- #1079758 - Add support for systemctl-reload action

* Thu Mar 20 2014 Pavel Šimerda <psimerda@redhat.com> - 1.10.0-1
- new package version 1.10.0

* Wed Mar 05 2014 Pavel Šimerda <psimerda@redhat.com> - 1.9.9-1
- bump to 1.9.9

* Wed Mar 05 2014 b'Pavel \xc5\xa0imerda <psimerda@redhat.com>' - b'1.9.9-1\n'
- rebuilt

* Mon Jan 13 2014 Pavel Šimerda <psimerda@redhat.com> - 1.9.8-1
- 1.9.8 bump

* Mon Jan 06 2014 Pavel Šimerda <psimerda@redhat.com> - 1.9.7-2
- #984330 - use _tmpfilesdir macro instead of the old location

* Mon Jan 06 2014 Pavel Šimerda <psimerda@redhat.com> - 1.9.7-1
- 1.9.7 bump

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Dec 05 2012 Petr Pisar <ppisar@redhat.com> - 1.9.2-2
- Create radvd user and and group with ID 75

* Wed Nov 21 2012 Petr Pisar <ppisar@redhat.com> - 1.9.2-1
- 1.9.2 bump

* Wed Aug 22 2012 Petr Pisar <ppisar@redhat.com> - 1.9.1-4
- Modernize systemd scriptlets (bug #850292)

* Tue Aug 07 2012 Petr Pisar <ppisar@redhat.com> - 1.9.1-3
- Remove useless chkconfig invocation (bug #845562)
- Do not reload unit file while unistalling

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 20 2012 Petr Pisar <ppisar@redhat.com> - 1.9.1-1
- 1.9.1 bump

* Fri Jun 15 2012 Petr Pisar <ppisar@redhat.com> - 1.9-2
- Drop already defined _GNU_SOURCE symbol

* Fri Jun 15 2012 Petr Pisar <ppisar@redhat.com> - 1.9-1
- 1.9 bump

* Wed May 23 2012 Petr Pisar <ppisar@redhat.com> - 1.8.5-4
- Start service independently on network state (bug #824205)
- Do not force systemd logging to syslog (bug #824205)

* Thu Apr 12 2012 Petr Pisar <ppisar@redhat.com> - 1.8.5-3
- Store PID before daemonizing (bug #811997)

* Tue Apr 03 2012 Petr Pisar <ppisar@redhat.com> - 1.8.5-2
- Clean up spec file
- Remove System V init support
- Fix radvd account creation

* Wed Feb 01 2012 Jiri Skala <jskala@redhat.com> - 1.8.5-1
- update to latest upstream version 1.8.5

* Mon Jan 23 2012 Jiri Skala <jskala@redhat.com> - 1.8.4-1
- update to latest upstream version 1.8.4

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Oct 17 2011 Jiri Skala <jskala@redhat.com> - 1.8.3-1
- update to latest upstream version 1.8.3

* Mon Oct 10 2011 Jiri Skala <jskala@redhat.com> - 1.8.2-2
- fixes CVE-2011-3602

* Fri Oct 07 2011 Jiri Skala <jskala@redhat.com> - 1.8.2-1
- update to latest upstream version 1.8.2
- this update fixes CVE-2011-360{1..5}

* Wed Aug 24 2011 Jiri Skala <jskala@redhat.com> - 1.8.1-1
- update to latest upstream version 1.8.1

* Fri Aug 12 2011 Jiri Skala <jskala@redhat.com> - 1.8-2
- fixes #729367 - supress unadvisable messages - applied upstream changes

* Tue May 17 2011 Jiri Skala <jskala@redhat.com> - 1.8-1
- update to latest upstream version 1.8

* Mon Feb 28 2011 Jiri Skala <jskala@redhat.com> - 1.7-3
- fixes #679830 - radvd dies when reloading, initscript reports "OK"

* Wed Feb 23 2011 Jiri Skala <jskala@redhat.com> - 1.7-2
- fixes #679821 - provides native systemd service file

* Wed Feb 09 2011 Jiri Skala <jskala@redhat.com> - 1.7-1
- update to latest upstream version 1.7

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 01 2010 Jiri Skala <jskala@redhat.com> - 1.6-4
- #656682 - using tmpfiles.d

* Wed Dec 01 2010 Jiri Skala <jskala@redhat.com> - 1.6-3
- fixes #656682 - using %%ghost on files in /var/run
- added necessary buildrequres flex-static 

* Fri May 21 2010 Jiri Skala <jskala@redhat.com> - 1.6-2
- ensure fax group id == fax user id

* Mon Mar 29 2010 Jiri Skala <jskala@redhat.com> - 1.6-1
- update to latest upstream version

* Mon Jan 25 2010 Jiri Skala <jskala@redhat.com> - 1.5-3
- spec file uses Source1 for radvd.init no more init from tarball
- radvd.init modified to make rmplint more silent
- removed userdel usage from postun

* Wed Jan 13 2010 Jan Gorig <jgorig@redhat.com> - 1.5-2
- mistake in last build

* Wed Jan 13 2010 Jan Gorig <jgorig@redhat.com> - 1.5-1
- updated do latest upstream version
- fixed #554125 - added error message

* Sun Oct 18 2009 Jiri Skala <jskala@redhat.com> - 1.3-4
- fixed #528178 - added force-reload

* Sun Oct 18 2009 Jiri Skala <jskala@redhat.com> - 1.3-3
- fixed #528178 - retval in init script to be posix compliant

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 10 2009 Jiri Skala <jskala@redhat.com> - 1.3-1
- updated to latest upstream version

* Wed Jun 03 2009 Jiri Skala <jskala@redhat.com> - 1.2-3
- changed echos to be able to accept localization

* Tue Apr 28 2009 Jiri Skala <jskala@redhat.com> - 1.2-2
- fixed ambiguous condition in init script (exit 4)

* Mon Apr 27 2009 Jiri Skala <jskala@redhat.com> - 1.2-1
- updated to latest upstream version

* Fri Feb 27 2009 Jiri Skala <jskala@redhat.com> - 1.1-8
- regenerated posix patch

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 02 2009 Jiri Skala <jskala@redhat.com> - 1.1-6
- init script modified to be POSIX compliant

* Wed Sep  3 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.1-5
- fix license tag

* Mon Jun 23 2008 Jiri Skala <jskala@redhat.com> - 1.1-4
- radvd.init LSB compliant

* Fri Apr 11 2008 Martin Nagy <mnagy@redhat.com> - 1.1-3
- remove stale pid file on start

* Mon Feb 25 2008 Martin Nagy <mnagy@redhat.com> - 1.1-2
- fix up string comparison in init script (#427047)

* Mon Feb 25 2008 Martin Nagy <mnagy@redhat.com> - 1.1-1
- update to new upstream version
- remove patch fixed in upstream: initscript

* Mon Feb 11 2008 Martin Nagy <mnagy@redhat.com> - 1.0-6
- rebuild for gcc-4.3

* Tue Nov 13 2007 Martin Bacovsky <mbacovsk@redhat.com> - 1.0-5
- resolves #376081: The radvd init script exits without doing anything if /usr/sbin/radvd exists

* Thu Aug 23 2007 Martin Bacovsky <mbacovsk@redhat.com> - 1.0-4.1
- Rebuild

* Fri Aug  3 2007 Martin Bacovsky <mbacovsk@redhat.com> - 1.0-4
- resolves: #247041: Initscript Review

* Wed Feb 14 2007 Martin Bacovsky <mbacovsk@redhat.com> - 1.0-3
- specfile cleanup for review

* Thu Feb  1 2007 Martin Bacovsky <mbacovsk@redhat.com> - 1.0-2
- linking with -pie flag turned on again

* Wed Jan 31 2007 Martin Bacovsky <mbacovsk@redhat.com> - 1.0-1
- rebase to upstream 1.0
- Resolves: #225542: radvd 1.0 released

* Fri Aug 18 2006 Jesse Keating <jkeating@redhat.com> - 0.9.1-4
- rebuilt with latest binutils to pick up 64K -z commonpagesize on ppc*
  (#203001)

* Mon Jul 17 2006 Jason Vas Dias <jvdias@redhat.com> - 0.9.1-3
- rebuild for new FC-6 build environment

* Mon Jun 05 2006 Jason Vas Dias <jvdias@redhat.com> - 0.9.1-2
- fix BuildRequires for Mock

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.9.1-1.1.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jason Vas Dias <jvdias@redhat.com> - 0.9.1-1.1
- rebuild for new gcc, glibc, glibc-kernheaders

* Mon Jan 16 2006 Jason Vas Dias<jvdias@redhat.com> - 0.9.1-1
- Upgrade to upstream version 0.9.1

* Sun Dec 18 2005 Jason Vas Dias<jvdias@redhat.com>
- Upgrade to upstream version 0.9

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Jul 19 2005 Jason Vas Dias <jvdias@redhat.com> 0.8.2.FC5
- fix bug 163593: must use '%%configure' to get correct conf file location

* Mon Jul 18 2005 Jason Vas Dias <jvdias@redhat.com> 0.8-1.FC5
- Upgrade to upstream version 0.8

* Fri Jul  8 2005 Pekka Savola <pekkas@netcore.fi> 0.8-1
- 0.8.
- Ship the example config file as %%doc (Red Hat's #159005)

* Fri Feb 25 2005 Jason Vas Dias <jvdias@redhat.com> 0.7.3-1_FC4
- make version compare > that of FC3

* Mon Feb 21 2005 Jason Vas Dias <jvdias@redhat.com> 0.7.3-1
- Upgrade to radvd-0.7.3
- add execshield -fPIE / -pie compile / link options

* Mon Feb 21 2005 Pekka Savola <pekkas@netcore.fi> 0.7.3-1
- 0.7.3.

* Mon Oct 28 2002 Pekka Savola <pekkas@netcore.fi>
- 0.7.2.

* Tue May  7 2002 Pekka Savola <pekkas@netcore.fi>
- remove '-g %%{RADVD_GID}' when creating the user, which may be problematic
  if the user didn't exist before.

* Fri Apr 12 2002 Bernhard Rosenkraenzer <bero@redhat.com> 0.7.1-1
- 0.7.1 (bugfix release, #61023), fixes:
  - Check that forwarding is enabled when starting radvd
    (helps avoid odd problems) 
  - Check configuration file permissions (note: in setuid operation, must not
    be writable by the user.group) 
  - Cleanups and enhancements for radvdump
  - Ensure NULL-termination with strncpy even with overlong strings
    (non-criticals, but better safe than sorry) 
  - Update config.{guess,sub} to cope with some newer architectures 
  - Minor fixes and cleanups 

* Mon Jan 14 2002 Pekka Savola <pekkas@netcore.fi>
- 0.7.1.

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Jan  8 2002 Pekka Savola <pekkas@netcore.fi>
- Change 'reload' to signal HUP to radvd instead or restarting.

* Fri Dec 28 2001 Pekka Savola <pekkas@netcore.fi>
- License unfortunately is BSD *with* advertising clause, so to be pedantic,
  change License: to 'BSD-style'.

* Thu Nov 22 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- 0.7.0

* Wed Nov 14 2001 Pekka Savola <pekkas@netcore.fi>
- spec file cleanups
- update to 0.7.0.

* Mon Jul  9 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- initial Red Hat Linux build

* Sun Jun 24 2001 Pekka Savola <pekkas@netcore.fi>
- add a patch from USAGI for overflow, Copyright -> License.

* Wed Jun 20 2001 Pekka Savola <pekkas@netcore.fi>
- use /sbin/service.
- update to 0.6.2pl4.

* Sat Apr 28 2001 Pekka Savola <pekkas@netcore.fi>
- update to 0.6.2pl3.

* Wed Apr 11 2001 Pekka Savola <pekkas@netcore.fi>
- update to 0.6.2pl2.

* Wed Apr  4 2001 Pekka Savola <pekkas@netcore.fi>
- update to 0.62pl1.  Bye bye patches!
- Require: initscripts (should really be with a version providing IPv6)
- clean up the init script, make condrestart work properly
- Use a static /etc/rc.d/init.d; init.d/radvd required it anyway.

* Sun Apr  1 2001 Pekka Savola <pekkas@netcore.fi>
- add patch to chroot (doesn't work well yet, as /proc is used directly)
- clean up droproot patch, drop the rights earlier; require user-writable
pidfile directory
- set up the pidfile directory at compile time.

* Sat Mar 31 2001 Pekka Savola <pekkas@netcore.fi>
- add select/kill signals patch from Nathan Lutchansky <lutchann@litech.org>.
- add address syntax checked fix from Marko Myllynen <myllynen@lut.fi>.
- add patch to check the pid file before fork.
- add support for OPTIONS sourced from /etc/sysconfig/radvd, provide a nice
default one.
- add/delete radvd user, change the pidfile to /var/run/radvd/radvd.pid.
- fix initscript NETWORKING_IPV6 check.

* Sun Mar 18 2001 Pekka Savola <pekkas@netcore.fi>
- add droproot patch, change to nobody by default (should use radvd:radvd or
the like, really).

* Mon Mar  5 2001 Tim Powers <timp@redhat.com>
- applied patch supplied by Pekka Savola in #30508
- made changes to initscript as per Pekka's suggestions

* Thu Feb 15 2001 Tim Powers <timp@redhat.com>
- needed -D_GNU_SOURCE to build properly

* Tue Feb  6 2001 Tim Powers <timp@redhat.com>
- use %%configure and %%makeinstall, just glob the manpages, cleans
  things up
- fixed initscript so that it can be internationalized in the future

* Fri Feb 2 2001 Pekka Savola <pekkas@netcore.fi>
- Create a single package(source) for glibc21 and glibc22 (automatic
Requires can handle this just fine).
- use %%{_mandir} and friends
- add more flesh to %%doc
- streamline %%config file %%attrs
- streamline init.d file a bit:
   * add a default chkconfig: (default to disable for security etc. reasons; 
     also, the default config isn't generic enough..)
   * add reload/condrestart
   * minor tweaks
   * missing: localization support (initscripts-5.60)
- use %%initdir macro

* Thu Feb 1 2001 Lars Fenneberg <lf@elemental.net>
- updated to new release 0.6.2

* Thu Feb 1 2001 Marko Myllynen <myllynen@lut.fi>
- initial version, radvd version 0.6.1
