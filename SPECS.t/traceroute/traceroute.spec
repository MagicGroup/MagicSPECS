Summary: Traces the route taken by packets over an IPv4/IPv6 network
Summary(zh_CN.UTF-8): 在 IPv4/IPv6 网络上跟踪包的路由
Name: traceroute
Epoch: 3
Version:	2.0.21
Release:	2%{?dist}
Group: Applications/Internet
Group(zh_CN.UTF-8): 应用程序/互联网
License: GPLv2+
URL:  http://traceroute.sourceforge.net
Source0: http://downloads.sourceforge.net/project/traceroute/traceroute/traceroute-%{version}/traceroute-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Provides: tcptraceroute = 1.5-1
Obsoletes: tcptraceroute < 1.5-1


%description
The traceroute utility displays the route used by IP packets on their
way to a specified network (or Internet) host.  Traceroute displays
the IP number and host name (if possible) of the machines along the
route taken by the packets.  Traceroute is used as a network debugging
tool.  If you're having network connectivity problems, traceroute will
show you where the trouble is coming from along the route.

Install traceroute if you need a tool for diagnosing network connectivity
problems.

%description -l zh_CN.UTF-8
在 IPv4/IPv6 网络上跟踪包的路由。

%prep
%setup -q


%build
make %{?_smp_mflags} CFLAGS="$RPM_OPT_FLAGS" LDFLAGS=""


%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/bin
install -m755 traceroute/traceroute $RPM_BUILD_ROOT/bin
pushd $RPM_BUILD_ROOT/bin
ln -s traceroute traceroute6
popd

install -d $RPM_BUILD_ROOT%{_bindir}
install -m755 wrappers/tcptraceroute $RPM_BUILD_ROOT%{_bindir}

install -d $RPM_BUILD_ROOT%{_mandir}/man8
install -p -m644 traceroute/traceroute.8 $RPM_BUILD_ROOT%{_mandir}/man8
pushd $RPM_BUILD_ROOT%{_mandir}/man8
ln -s traceroute.8 traceroute6.8
ln -s traceroute.8 tcptraceroute.8
popd


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc COPYING README TODO CREDITS
/bin/*
%{_bindir}/*
%{_mandir}/*/*

%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 3:2.0.21-2
- 为 Magic 3.0 重建

* Sun Oct 04 2015 Liu Di <liudidi@gmail.com> - 3:2.0.21-1
- 更新到 2.0.21

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 3:2.0.18-4
- 为 Magic 3.0 重建

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3:2.0.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov  2 2011 Dmitry Butskoy <Dmitry@Butskoy.name>  - 3:2.0.18-2
- add wrapper for tcptraceroute (which is obsoleted now, #733030)

* Wed Aug 24 2011 Dmitry Butskoy <Dmitry@Butskoy.name>  - 3:2.0.18-1
- update to 2.0.18 (make possible to use unprivileged icmp echo sockets)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3:2.0.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 14 2010 Dmitry Butskoy <Dmitry@Butskoy.name>  - 3:2.0.17-1
- update to 2.0.17 (makes possible to use Linux capabilities)

* Wed Sep 29 2010 Jesse Keating <jkeating@redhat.com> - 3:2.0.16-2
- Rebuilt for gcc bug 634757

* Tue Sep 14 2010 Dmitry Butskoy <Dmitry@Butskoy.name>  - 3:2.0.16-1
- update to 2.0.16 (fix #631033)

* Wed Jul 14 2010 Dmitry Butskoy <Dmitry@Butskoy.name>  - 3:2.0.15-1
- update to 2.0.15

* Tue Apr 27 2010 Dmitry Butskoy <Dmitry@Butskoy.name>  - 3:2.0.14-1
- update to 2.0.14 (fixes #583985)

* Thu Jan 07 2010 Jiri Skala <jskala@redhat.com> - 3:2.0.13-2
- fixed Source0 link

* Tue Nov  3 2009 Dmitry Butskoy <Dmitry@Butskoy.name>  - 3:2.0.13-1
- update to 2.0.13 (fixes #532346)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3:2.0.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3:2.0.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Sep 17 2008 Dmitry Butskoy <Dmitry@Butskoy.name>  - 3:2.0.12-1
- update to 2.0.12 (fixes #461278 and #461626)
- this release adds support for icmp extensions (including MPLS),
  which was expected for a long time (#176588)
- drop "tracert" symlink (#461109)

* Mon May 19 2008 Dmitry Butskoy <Dmitry@Butskoy.name>  - 3:2.0.11-1
- update to 2.0.11

* Thu Apr 17 2008 Dmitry Butskoy <Dmitry@Butskoy.name>  - 3:2.0.10-1
- upgrade to 2.0.10 (fixes #245438 and ipv6 tracerouting for new kernels)

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3:2.0.9-2
- Autorebuild for GCC 4.3

* Wed Oct 10 2007 Martin Bacovsky <mbacovsk@redhat.com> - 3:2.0.9-1
- upgrade to new upstream traceroute-2.0.9

* Tue Sep 18 2007 Martin Bacovsky <mbacovsk@redhat.com> - 3:2.0.8-1
- upgrade to new upstream traceroute-2.0.8
- fixed traceroute.8 install source path and traceroute6.8 link source
- fixed typo in Source0 URL

* Tue Aug 28 2007 Dmitry Butskoy <Dmitry@Butskoy.name>
- Change URL and Source0 (upstream is at SourceForge now)

* Thu Aug 23 2007 Martin Bacovsky <mbacovsk@redhat.com> - 3:2.0.7-1
- upgrade to new upstream traceroute-2.0.7
- resolves: #249958: traceroute: useless debuginfo package

* Mon Jan 29 2007 Martin Bacovsky <mbacovsk@redhat.com> - 3:2.0.3-1.1.fc7
- Resolves: #225063: Re-add Epoch to traceroute

* Mon Jan 22 2007 Martin Bacovsky <mbacovsk@redhat.com> - 2.0.3-1.fc7
- Resolves: #222577 - man page with execute bit
- Resolves: #223784 - new traceroute breaks scripts
- Resolves: #223795 - /bin/tcptraceroute symlink occludes alternate tcptraceroute package

* Tue Nov 21 2006 Martin Bacovsky <mbacovsk@redhat.com> - 3:2.0.2-1.fc7
- new source
- more accurate check_expired() routine.
- some minor fixes.

* Mon Oct 30 2006 Martin Bacovsky <mbacovsk@redhat.com> - 3:2.0.1-2
- posted up lost epoch number

* Mon Oct 23 2006 Martin Bacovsky <mbacovsk@redhat.com> - 2.0.1-1
- upgarde to 2.0.1
- changed bindir to /bin
- improoved time obtaining

* Thu Oct 19 2006 Martin Bacovsky <mbacovsk@redhat.com> - 2.0.0-2
- fixed release numbering in spec file

* Tue Oct 17 2006 Martin Bacovsky <mbacovsk@redhat.com> - 2.0.0-1.fc7
- new source
- new features including ICMP support above all (#176587)
- Thanks to Dmitry Butskoy

* Wed Jul 19 2006 Radek Vokal <rvokal@redhat.com> - 2:1.0.4-2
- traceroute can not continue past destination host (#199342)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2:1.0.4-1.2.1
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2:1.0.4-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2:1.0.4-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Jan 09 2006 Radek Vokal <rvokal@redhat.com> 1.0.4-1
- upgrade to 1.0.4
- proper fix for bug #173762

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Nov 21 2005 Radek Vokal <rvokal@redhat.com> 1.0.3-5
- removed ICMP6_DST_UNREACH_NOTNEIGHBOR (#173762)

* Tue Nov 08 2005 Radek Vokal <rvokal@redhat.com> 1.0.3-4
- comaptibility patch, use -s and -i options

* Thu Nov 03 2005 Robert Scheck <redhat@linuxnetz.de> 1.0.3-3
- enable working IPv6 support in traceroute
- removed old compatibility links, nothing has SUID/SGID
- added some documentation files
- don't expand rpm macros in %%changelog

* Wed Nov 02 2005 Xose Vazquez Perez <xose.vazquez@gmail.com> 1.0.3-2
- license is GPL
- remove S_ISUID from /bin/traceroute
- description of this implementation
- s/$RPM_BUILD_ROOT/%%{buildroot}
- man page needs 0644
- link it agains relative paths, it works over NFS

* Wed Nov 02 2005 Radek Vokal <rvokal@redhat.com> 1.0.3-1
- new source 

* Thu Aug 11 2005 Radek Vokal <rvokal@redhat.com> 1.4a12-27
- fixed packet size for icmp checksum (#164466)
- small buffer-overflow fixies

* Fri Mar 04 2005 Radek Vokal <rvokal@redhat.com> 1.4a12-26
- gcc4 rebuilt

* Wed Feb 09 2005 Radek Vokal <rvokal@redhat.com> 1.4a12-25
- rebuilt
- verify icmp checksum only when -I used (#106013)

* Mon Oct 11 2004 Radek Vokal <rvokal@redhat.com> 1.4a12-24
- spec file updated (#135187)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed May 12 2004 Phil Knirsch <pknirsch@redhat.com> 1.4a12-22
- Enabled PIE for traceroute.

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Sep 01 2003 Phil Knirsch <pknirsch@redhat.com> 1.4a12-20.1
- rebuilt

* Mon Sep 01 2003 Phil Knirsch <pknirsch@redhat.com> 1.4a12-20
- Added patch from Jesper Skriver supplied by Kaj J. Niemi to support
  draft-ietf-mpls-icmp-02.txt.

* Thu Aug 28 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- move debuginfo stuff into proper rpms

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue May 13 2003 Phil Knirsch <pknirsch@redhat.com> 1.4a12-17
- Bumped release and rebuilt

* Tue May 13 2003 Phil Knirsch <pknirsch@redhat.com> 1.4a12-16
- Moved binary to /bin and symlink to old /usr/sbin place for compatibility.

* Mon May 12 2003 Phil Knirsch <pknirsch@redhat.com> 1.4a12-15
- Bumped release and rebuilt

* Mon May 12 2003 Phil Knirsch <pknirsch@redhat.com> 1.4a12-14
- Added -t option (#71790).

* Mon May 12 2003 Phil Knirsch <pknirsch@redhat.com> 1.4a12-13
- Bumped release and rebuilt

* Mon May 12 2003 Phil Knirsch <pknirsch@redhat.com> 1.4a12-12
- Switch to bz2 tarball to save space
- Added URL tag.

* Mon May 12 2003 Phil Knirsch <pknirsch@redhat.com> 1.4a12-11
- Bumped release and rebuilt

* Mon May 12 2003 Phil Knirsch <pknirsch@redhat.com> 1.4a12-10
- Added symlink to /usr/bin (#18313).

* Wed Jan 22 2003 Tim Powers <timp@redhat.com> 1.4a12-9
- rebuilt

* Wed Jan 08 2003 Phil Knirsch <pknirsch@redhat.com> 1.4a12-8
- Yet another fix for that bug.

* Tue Nov 26 2002 Phil Knirsch <pknirsch@redhat.com> 1.4a12-7
- Added fix for -i option (#78424).

* Fri Jun 21 2002 Tim Powers <timp@redhat.com> 1.4a12-6
- automated rebuild

* Wed Jun 19 2002 Phil Knirsch <pknirsch@redhat.com> 1.4a12-5
- Don't forcibly strip binaries

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jan 30 2002 Phil Knirsch <pknirsch@redhat.com>
- Bumped version number for rebuild

* Mon Jun 25 2001 Philipp Knirsch <pknirsch@redhat.de>
- Updated to 1.4a12

* Fri Dec  1 2000 Jeff Johnson <jbj@redhat.com>
- use RPM_OPT_FLAGS (#21279).

* Wed Oct  4 2000 Jeff Johnson <jbj@redhat.com>
- check max. packet length correctly (#15917).
- support LSRR correctly (#16281).

* Tue Jul 18 2000 Jeff Johnson <jbj@redhat.com>
- drop root privileges even earlier (#13466).

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jul 10 2000 Preston Brown <pbrown@redhat.com>
- bugfix for segfault with source routing (#13466)
- fix bug tracerouting thru aliased ethernet addresses (#9351)

* Sun Jun 18 2000 Jeff Johnson <jbj@redhat.com>
- FHS packaging.

* Fri Apr 28 2000 Bill Nottingham <notting@redhat.com>
- fix build with new stricter patch

* Mon Feb  7 2000 Jeff Johnson <jbj@redhat.com>
- compress man pages.

* Fri Jan 14 2000 Bill Nottingham <notting@redhat.com>
- add patch for tracing to really long hostnames

* Thu May 27 1999 Richard Henderson <rth@twiddle.net>
- avoid unaligned traps writing into the output data area.

* Fri May 14 1999 Jeff Johnson <jbj@redhat.com>
- fix segfault when host cannot be reached through if (#2819)

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 14)

* Fri Mar 19 1999 Jeff Johnson <jbj@redhat.com>
- strip binaries.

* Sun Feb 07 1999 Preston Brown <pbrown@redhat.com>
- patch added to automatically determine interface to route through

* Fri Jan 22 1999 Jeff Johnson <jbj@redhat.com>
- use %%configure
- fix 64 bit problem on alpha (#919)

* Wed Jan 13 1999 Bill Nottingham <notting@redhat.com>
- configure fix for arm

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Tue Dec 16 1997 Cristian Gafton <gafton@redhat.com>
- updated the security patch (ouch!). Without the glibc fix, it could be
  worthless anyway

* Sat Dec 13 1997 Cristian Gafton <gafton@redhat.com>
- added a security patch fix

* Wed Oct 22 1997 Erik Troan <ewt@redhat.com>
- added fix from Christopher Seawood

* Mon Sep 22 1997 Erik Troan <ewt@redhat.com>
- updated to 1.4a5 for security fixes; release 1 is for RH 4.2, release 2
  is against glibc

* Fri Jul 18 1997 Erik Troan <ewt@redhat.com>
- built against glibc
