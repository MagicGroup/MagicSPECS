Summary: The Point-to-Point Protocol daemon
Name: ppp
Version: 2.4.5
Release: 19%{?dist}
License: BSD and LGPLv2+ and GPLv2+ and Public Domain
Group: System Environment/Daemons
URL: http://www.samba.org/ppp
Source0: ftp://ftp.samba.org/pub/ppp/ppp-%{version}.tar.gz
Source1: ppp-2.3.5-pamd.conf
Source2: ppp.logrotate
Source3: ppp-tmpfs.conf
Patch0: ppp-2.4.3-make.patch
Patch1: ppp-2.3.6-sample.patch
Patch2: ppp-2.4.2-libutil.patch
Patch3: ppp-2.4.1-varargs.patch
Patch4: ppp-2.4.4-lib64.patch
Patch7: ppp-2.4.2-pie.patch
Patch8: ppp-2.4.3-fix.patch
Patch9: ppp-2.4.3-fix64.patch
Patch11: ppp-2.4.2-change_resolv_conf.patch
Patch13: ppp-2.4.4-no_strip.patch
Patch17: ppp-2.4.2-pppoatm-make.patch
Patch19: ppp-2.4.3-local.patch
Patch20: ppp-2.4.3-ipv6-accept-remote.patch
Patch22: ppp-2.4.4-cbcp.patch
Patch23: ppp-2.4.2-dontwriteetc.patch
Patch24: ppp-2.4.4-fd_leak.patch
Patch25: ppp-2.4.5-var_run_ppp.patch
Patch26: ppp-2.4.5-manpg.patch
Patch27: ppp-2.4.5-eaptls-mppe-0.99.patch
Patch28: ppp-2.4.5-ppp_resolv.patch
Patch29: ppp-2.4.5-man.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: pam-devel, libpcap-devel, openssl-devel
Requires: glibc >= 2.0.6, /etc/pam.d/system-auth, logrotate, libpcap >= 14:0.8.3-6
Requires: systemd-units

%description
The ppp package contains the PPP (Point-to-Point Protocol) daemon and
documentation for PPP support. The PPP protocol provides a method for
transmitting datagrams over serial point-to-point links. PPP is
usually used to dial in to an ISP (Internet Service Provider) or other
organization over a modem and phone line.

%package devel
Summary: Headers for ppp plugin development
Group: Development/Libraries

%description devel
This package contains the header files for building plugins for ppp.

%prep
%setup  -q
%patch0 -p1 -b .make
%patch1 -p1 -b .sample
# patch 2 depends on the -lutil in patch 0
%patch2 -p1 -b .libutil
%patch3 -p1 -b .varargs
# patch 4 depends on the -lutil in patch 0
%patch4 -p1 -b .lib64
%patch7 -p1 -b .pie
%patch8 -p1 -b .fix
%patch9 -p1 -b .fix64
%patch11 -p1 -b .change_resolv_conf
%patch13 -p1 -b .no_strip
%patch17 -p1 -b .atm-make
%patch19 -p1 -b .local
%patch20 -p1 -b .ipv6cp
%patch22 -p1 -b .cbcp
%patch23 -p1 -b .dontwriteetc
%patch24 -p1 -b .fd_leak
%patch25 -p1 -b .var_run_ppp
%patch26 -p1 -b .manpg
%patch27 -p1 -b .eaptls
%patch28 -p1 -b .ppp_resolv
%patch29 -p1 -b .man

rm -f scripts/*.local
rm -f scripts/*.change_resolv_conf
rm -f scripts/*.usepeerdns-var_run_ppp_resolv
rm -f scripts/*.ppp_resolv
find . -type f -name "*.sample" | xargs rm -f 

rm -f include/linux/if_pppol2tp.h

%build
#find . -name 'Makefile*' -print0 | xargs -0 perl -pi.no_strip -e "s: -s : :g"
RPM_OPT_FLAGS="$RPM_OPT_FLAGS -fPIC -Wall"
%configure
make

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
export INSTROOT=$RPM_BUILD_ROOT
make install install-etcppp

chmod -R a+rX scripts
find scripts -type f | xargs chmod a-x
chmod 0755 $RPM_BUILD_ROOT/%{_libdir}/pppd/%{version}/*.so
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/pam.d
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/ppp

# Provide pointers for people who expect stuff in old places
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/log/ppp
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/run/ppp

install -d -m 755 $RPM_BUILD_ROOT%{_sysconfdir}/tmpfiles.d
install -p -m 644 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/tmpfiles.d/ppp.conf

# Logrotate script
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/ppp

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_sbindir}/chat
%{_sbindir}/pppd
%{_sbindir}/pppdump
%{_sbindir}/pppoe-discovery
%{_sbindir}/pppstats
%{_mandir}/man8/chat.8*
%{_mandir}/man8/pppd.8*
%{_mandir}/man8/pppdump.8*
%{_mandir}/man8/pppd-radattr.8*
%{_mandir}/man8/pppd-radius.8*
%{_mandir}/man8/pppstats.8*
%{_mandir}/man8/pppoe-discovery.8*
%{_libdir}/pppd
%dir %{_sysconfdir}/ppp
%dir %{_localstatedir}/run/ppp
%attr(700, root, root) %dir %{_localstatedir}/log/ppp
%config %{_sysconfdir}/tmpfiles.d/ppp.conf
%config(noreplace) %{_sysconfdir}/ppp/eaptls-client
%config(noreplace) %{_sysconfdir}/ppp/eaptls-server
%config(noreplace) %{_sysconfdir}/ppp/chap-secrets
%config(noreplace) %{_sysconfdir}/ppp/options
%config(noreplace) %{_sysconfdir}/ppp/pap-secrets
%config(noreplace) %{_sysconfdir}/pam.d/ppp
%config(noreplace) %{_sysconfdir}/logrotate.d/ppp
%doc FAQ README README.cbcp README.linux README.MPPE README.MSCHAP80 README.MSCHAP81 README.pwfd README.pppoe scripts sample README.eap-tls

%files devel
%defattr(-,root,root)
%{_includedir}/pppd
%doc PLUGINS

%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 2.4.5-19
- 为 Magic 3.0 重建

* Thu Jan 26 2012 Liu Di <liudidi@gmail.com> - 2.4.5-18
- 为 Magic 3.0 重建

* Mon Apr 04 2011 Jiri Skala <jskala@redhat.com> - 2.4.5-17
- fixes #664282 and #664868 - man page fixes

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.5-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 02 2010 Jiri Skala <jskala@redhat.com> - 2.4.5-15
- corrected tmpfiles.d conf
- replaced remaining /etc by macros

* Tue Nov 30 2010 Jiri Skala <jskala@redhat.com> - 2.4.5-14
- fixes #656671 - /var/run and /var/lock on tmpfs
- replaced paths /var /etc by macros

* Tue Nov 16 2010 Jiri Skala <jskala@redhat.com> - 2.4.5-13
- fixes #565294 - SELinux is preventing /sbin/consoletype access to a leaked packet_socket fd

* Wed Sep 29 2010 Jiri Skala <jskala@redhat.com> - 2.4.5-12
- fixes #637513 - Missing: README.eap-tls
- updated to latest eaptls upstream
- fixes #637886 - EAP-TLS not working with enabled PPP Multilink Framing option

* Thu Aug 05 2010 Jiri Skala <jskala@redhat.com> - 2.4.5-11
- fixes #617625 - FTBFS in ppp due to change in kernel-headers
- fixes pppol2tp Makefile

* Tue Jul 13 2010 Jiri Skala <jskala@redhat.com> - 2.4.5-10
- fixes #613717 - Missing line in example script ip-up.local.add
- removed /usr/kerberos/include from eaptls patch

* Wed Jun 16 2010 Jiri Skala <jskala@redhat.com> - 2.4.5-9
- included eap-tls patch

* Wed Apr 07 2010 Jiri Skala <jskala@redhat.com> - 2.4.5-8
- added pppoe-discovery(8)

* Fri Mar 05 2010 Jiri Skala <jskala@redhat.com> - 2.4.5-7
- removed duplicities from patches (ip-*.local.add)

* Fri Feb 12 2010 Jiri Skala <jskala@redhat.com> - 2.4.5-6
- fixes #560014 - SELinux is preventing /usr/sbin/pppd "read write" access on pppd2.tdb

* Thu Feb 04 2010 Jiri Skala <jskala@redhat.com> - 2.4.5-5
- one line correction in fd_leak patch

* Wed Feb 03 2010 Jiri Skala <jskala@redhat.com> - 2.4.5-4
- applied patch fd_leak

* Fri Jan 22 2010 Jiri Skala <jskala@redhat.com> - 2.4.5-3
- fixed some rpmlint complains

* Sun Nov 22 2009 Jiri Skala <jskala@redhat.com>  - 2.4.5-2
- updated patches (make local succeeded, koji failed)

* Fri Nov 20 2009 Jiri Skala <jskala@redhat.com>  - 2.4.5-1
- updated to latest upstream sources (#538058)

* Thu Oct 08 2009 Jiri Skala <jskala@redhat.com>  - 2.4.4-14
- fixed #519042 - ppp package is missing URL in spec
- fixed #524575 - ppp: no_strip patch modifies backup files created by previous patches

* Wed Sep 16 2009 Tomas Mraz <tmraz@redhat.com> 2.4.4-13
- use password-auth common PAM configuration instead of system-auth

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Mar 06 2009 - Jiri Skala <jskala@redhat.com> 2.4.4-11
- fixed #488764 - package upgrade should not replace configuration files

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Dec 11 2008 Jiri Skala <jskala@redhat.com> 2.4.4.-9
- fixed #467004 PPP sometimes gets incorrect DNS servers for mobile broadband connections

* Thu Aug 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.4.4-8
- fix license tag

* Tue May 13 2008 Martin Nagy <mnagy@redhat.com> 2.4.4-7
- add new speeds, patch by Jason Vas Dias (#446132)

* Thu Mar 06 2008 Martin Nagy <mnagy@redhat.com> 2.4.4-6
- call closelog earlier (#222295)
- fix ChapMS2 (#217076)
- moving header files to new -devel package (#203542)

* Mon Mar 03 2008 Martin Nagy <mnagy@redhat.com> 2.4.4-5
- put logs into /var/log/ppp (#118837)

* Mon Feb 11 2008 Martin Nagy <mnagy@redhat.com> 2.4.4-4
- rebuild for gcc-4.3

* Fri Nov 09 2007 Martin Nagy <mnagy@redhat.com> 2.4.4-3
- removed undesired files from the package (#241753)

* Fri Dec  1 2006 Thomas Woerner <twoerner@redhat.com> 2.4.4-2
- fixed build requirement for libpcap (#217661)

* Wed Jul 19 2006 Thomas Woerner <twoerner@redhat.com> 2.4.4-1
- new version 2.4.4 with lots of fixes
- fixed reesolv.conf docs (#165072)
  Thanks to Matt Domsch for the initial patch 
- enabled CBCP (#199278)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.4.3-6.2.2
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.4.3-6.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.4.3-6.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Sat Nov 12 2005 Florian La Roche <laroche@redhat.com>
- rebuild

* Fri Nov  4 2005 David Woodhouse <dwmw2@redhat.com> 2.4.3-5
- Implement ipv6cp-accept-remote option

* Fri Oct  7 2005 Tomas Mraz <tmraz@redhat.com> 2.4.3-4
- use include instead of pam_stack in pam config

* Sun Jul 31 2005 Florian La Roche <laroche@redhat.com>
- rebuild for libpcap of the day

* Tue Jul 19 2005 Thomas Woerner <twoerner@redhat.com> 2.4.3-2.1
- additional patch for the scripts, thanks to Sammy (#163621)

* Tue Jul 19 2005 Thomas Woerner <twoerner@redhat.com> 2.4.3-2
- dropped all executable bits in scripts directory to prevent rpm requiring
  programs used in there

* Mon Jul 18 2005 Thomas Woerner <twoerner@redhat.com> 2.4.3-1
- new version 2.4.3
  - updated patches: make, lib64, dontwriteetc, fix, fix64, no_strip,
    radiusplugin
  - dropped patches: bpf, signal, pcap, pppoatm, pkgcheck

* Tue Nov  2 2004 Thomas Woerner <twoerner@redhat.com> 2.4.2-7
- fixed out of bounds memory access, possible DOS

* Thu Oct  7 2004 David Woodhouse <dwmw2@redhat.com> 2.4.2-6.3
- Fix use of 'demand' without explicit MTU/MRU with pppoatm

* Tue Oct  5 2004 David Woodhouse <dwmw2@redhat.com> 2.4.2-6.2
- Link pppoatm plugin against libresolv.
- Revert to linux-atm headers without the workaround for #127098

* Mon Oct  4 2004 David Woodhouse <dwmw2@redhat.com> 2.4.2-6.1
- Include atmsap.h for pppoatm plugin.

* Mon Oct  4 2004 David Woodhouse <dwmw2@redhat.com> 2.4.2-6
- Add pppoatm plugin (#131555)

* Thu Sep 16 2004 Thomas Woerner <twoerner@redhat.com> 2.4.2-5.1
- fixed subscript out of range (#132677)

* Wed Sep 15 2004 Thomas Woerner <twoerner@redhat.com> 2.4.2-5
- example scripts are using change_resolv_conf to modify /etc/resolv.conf
  (#132482)
- require new libpcap library (>= 0.8.3-6) with a fix for inbound/outbound
  filter processing
- not using internal libpcap structures anymore, fixes inbound/outbound
  filter processing (#128053) 

* Fri Aug  6 2004 Thomas Woerner <twoerner@redhat.com> 2.4.2-4
- fixed signal handling (#29171)

* Mon Jun 21 2004 Thomas Woerner <twoerner@redhat.com> 2.4.2-3.1
- fixed compiler warnings
- fixed 64bit problem with ms-chap (#125501)
- enabled pie again

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed May 24 2004 David Woodhouse <dwmw2@redhat.com> 2.4.2-2.3
- Enable IPv6 support. Disable PIE to avoid bogus Provides:

* Fri May 14 2004 Thomas Woerner <twoerner@redhat.com> 2.4.2-2.2
- compiled pppd and chat PIE

* Thu May 13 2004 Thomas Woerner <twoerner@redhat.com> 2.4.2-2.1
- added 'missingok' to ppp.logrotate (#122911)

* Fri May 07 2004 Nils Philippsen <nphilipp@redhat.com> 2.4.2-2
- don't write to /etc (#118837)

* Wed Mar 10 2004 Nalin Dahyabhai <nalin@redhat.com> 2.4.2-1
- update to 2.4.2

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Sep  5 2003 Nalin Dahyabhai <nalin@redhat.com> 2.4.1-15
- rebuild

* Fri Sep  5 2003 Nalin Dahyabhai <nalin@redhat.com> 2.4.1-14
- apply the patch from -11

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun  3 2003 Nalin Dahyabhai <nalin@redhat.com> 2.4.1-12
- rebuild

* Tue Jun  3 2003 Nalin Dahyabhai <nalin@redhat.com> 2.4.1-11
- check for libcrypt in the right directory at compile-time

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Dec 12 2002 Elliot Lee <sopwith@redhat.com> 2.4.1-9
- Fix build failure by rebuilding

* Tue Nov 19 2002 Nalin Dahyabhai <nalin@redhat.com> 2.4.1-8
- rebuild
- set x86_64 to use varargs the way s390 does

* Mon Jul 22 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- add patch:
	* Thu Jun 06 2002 Phil Knirsch <pknirsch@redhat.com>
	- Fixed varargs problem for s390/s390x.

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri May 17 2002 Nalin Dahyabhai <nalin@redhat.com> 2.4.1-4
- rebuild in new environment

* Wed Feb 27 2002 Nalin Dahyabhai <nalin@redhat.com> 2.4.1-3
- revert cbcp patch, it's wrong (#55367)

* Thu Aug  9 2001 Nalin Dahyabhai <nalin@redhat.com> 2.4.1-2
- add buildprereq on pam-devel (#49559)
- add patch to respond to CBCP LCP requests (#15738)
- enable cbcp support at build-time
- change the Copyright: tag to a License: tag

* Wed May 23 2001 Nalin Dahyabhai <nalin@redhat.com> 2.4.1-1
- update to 2.4.1

* Fri Dec  1 2000 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in new environment

* Thu Nov  9 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.4.0

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jun  5 2000 Nalin Dahyabhai <nalin@redhat.com>
- move man pages to %{_mandir}

* Thu Jun  1 2000 Nalin Dahyabhai <nalin@redhat.com>
- change perms using defattr
- modify PAM setup to use system-auth

* Sun Mar 26 2000 Florian La Roche <Florian.La Roche@redhat.com>
- change to root:root perms

* Mon Mar 06 2000 Nalin Dahyabhai <nalin@redhat.com>
- reaper bugs verified as fixed
- check pam_open_session result code (bug #9966)

* Mon Feb 07 2000 Nalin Dahyabhai <nalin@redhat.com>
- take a shot at the wrong reaper bugs (#8153, #5290)

* Thu Feb 03 2000 Nalin Dahyabhai <nalin@redhat.com>
- free ride through the build system (release 2)

* Tue Jan 18 2000 Nalin Dahyabhai <nalin@redhat.com>
- Update to 2.3.11

* Sat Nov 06 1999 Michael K. Johnson <johnsonm@redhat.com>
- Better fix for both problems

* Fri Nov 05 1999 Michael K. Johnson <johnsonm@redhat.com>
- fix for double-dial problem
- fix for requiring a controlling terminal problem

* Sun Sep 19 1999 Preston Brown <pbrown@redhat.com>
- 2.3.10 bugfix release

* Fri Aug 13 1999 Michael K. Johnson <johnsonm@redhat.com>
- New version 2.3.9 required for kernel 2.3.13 and will be required
  for new initscripts.  auth patch removed; 2.3.9 does the same thing
  more readably than the previous patch.

* Thu Jun 24 1999 Cristian Gafton <gafton@redhat.com>
- add pppdump

* Fri Apr 09 1999 Cristian Gafton <gafton@redhat.com>
- force pppd use the glibc's logwtmp instead of implementing its own

* Wed Apr 01 1999 Preston Brown <pbrown@redhat.com>
- version 2.3.7 bugfix release

* Tue Mar 23 1999 Cristian Gafton <gafton@redhat.com>
- version 2.3.6

* Mon Mar 22 1999 Michael Johnson <johnsonm@redhat.com>
- auth patch

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 3)

* Thu Jan 07 1999 Cristian Gafton <gafton@redhat.com>
- build for glibc 2.1

* Fri Jun  5 1998 Jeff Johnson <jbj@redhat.com>
- updated to 2.3.5.

* Tue May 19 1998 Prospector System <bugs@redhat.com>
- translations modified for de

* Fri May  8 1998 Jakub Jelinek <jj@ultra.linux.cz>
- make it run with kernels 2.1.100 and above.

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed Mar 18 1998 Cristian Gafton <gafton@redhat.com>
- requires glibc 2.0.6 or later

* Wed Mar 18 1998 Michael K. Johnson <johnsonm@redhat.com>
- updated PAM patch to not turn off wtmp/utmp/syslog logging.

* Wed Jan  7 1998 Cristian Gafton <gafton@redhat.com>
- added the /etc/pam.d config file
- updated PAM patch to include session support

* Tue Jan  6 1998 Cristian Gafton <gafton@redhat.com>
- updated to ppp-2.3.3, build against glibc-2.0.6 - previous patches not
  required any more.
- added buildroot
- fixed the PAM support, which was really, completely broken and against any
  standards (session support is still not here... :-( )
- we build against running kernel and pray that it will work
- added a samples patch; updated glibc patch

* Thu Dec 18 1997 Erik Troan <ewt@redhat.com>
- added a patch to use our own route.h, rather then glibc's (which has 
  alignment problems on Alpha's) -- I only applied this patch on the Alpha,
  though it should be safe everywhere

* Fri Oct 10 1997 Erik Troan <ewt@redhat.com>
- turned off the execute bit for scripts in /usr/doc

* Fri Jul 18 1997 Erik Troan <ewt@redhat.com>
- built against glibc

* Tue Mar 25 1997 Erik Troan <ewt@redhat.com>
- Integrated new patch from David Mosberger
- Improved description

