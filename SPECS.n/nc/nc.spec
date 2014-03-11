Summary:    Reads and writes data across network connections using TCP or UDP
Name:       nc
Version:    1.107
Release:    2%{?dist}
URL:        http://www.openbsd.org/cgi-bin/cvsweb/src/usr.bin/%{name}/
License:    BSD and ISC
Group:      Applications/Internet
# source is CVS checkout, e.g.:
# CVSROOT=anoncvs@anoncvs.openbsd.org.ar:/cvs/src/usr.bin cvs checkout nc
Source0:    %{name}-%{version}.tar.bz2
Source1:    b64_ntop.c
Patch0:     nc-1.107-linux-ify.patch
Patch1:     nc-1.107-pollhup.patch
Patch2:     nc-1.107-udp-stop.patch
Patch3:     nc-1.107-udp-portscan.patch
Patch4:     nc-1.107-crlf.patch
Patch5:     nc-1.107-comma.patch
Patch6:     nc-1.100-libbsd.patch
Patch7:     nc-1.107-initialize-range.patch
Patch8:     nc-1.107-iptos-class.patch

BuildRequires: libbsd-devel

%description
The nc package contains Netcat (the program is actually nc), a simple
utility for reading and writing data across network connections, using
the TCP or UDP protocols. Netcat is intended to be a reliable back-end
tool which can be used directly or easily driven by other programs and
scripts.  Netcat is also a feature-rich network debugging and
exploration tool, since it can create many different connections and
has many built-in capabilities.

You may want to install the netcat package if you are administering a
network and you'd like to use its debugging and network exploration
capabilities.

%prep
%setup -q -n nc
%patch0 -p1 -b .linux-ify
%patch1 -p1 -b .pollhup
%patch2 -p1 -b .udp-stop
%patch3 -p1 -b .udp-portscan
%patch4 -p1 -b .crlf
%patch5 -p1 -b .comma
%patch6 -p1 -b .libbsd
%patch7 -p1 -b .initialize-range
%patch8 -p1 -b .iptos-class
cp -p %{SOURCE1} .

%build
gcc %{optflags} `pkg-config --cflags --libs libbsd` -o nc netcat.c atomicio.c socks.c b64_ntop.c

%install
install -d %{buildroot}%{_bindir}
install -m755 -p nc %{buildroot}%{_bindir}
install -d %{buildroot}%{_mandir}/man1
install -m644 -p nc.1 %{buildroot}%{_mandir}/man1

magic_rpm_clean.sh

%files
%{_bindir}/nc
%{_mandir}/man1/nc.1*

%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 1.107-2
- 为 Magic 3.0 重建

* Tue Apr 03 2012 Petr Šabata <contyk@redhat.com> - 1.107-1
- 1.107 bump
- Warn if accept fails implemented upstream, removing the patch

* Fri Mar 23 2012 Petr Šabata <contyk@redhat.com> - 1.106-1
- 1.106 bump
- BSD jumbo support removed upstream
- size_t format patch included upstream

* Thu Feb 09 2012 Petr Šabata <contyk@redhat.com> - 1.105-1
- 1.105 bump

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.103-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.103-2
- Rebuilt for glibc bug#747377

* Wed Oct 05 2011 Petr Sabata <contyk@redhat.com> - 1.103-1
- 1.103 bump

* Thu Jul 07 2011 Petr Sabata <contyk@redhat.com> - 1.101-2
- Do not send CRLF line endings in an extra packet
  Thanks to Jaroslav Franek, rhbz#719386

* Wed Jun 22 2011 Petr Sabata <contyk@redhat.com> - 1.101-1
- 1.101 bump (no changes for us...)

* Fri Jun 03 2011 Petr Sabata <contyk@redhat.com> - 1.100-4
- Check return value of accept() (#710482)

* Fri Jun 03 2011 Petr Sabata <contyk@redhat.com> - 1.100-3
- Initialize range (#710464)
- Remove defattr macro

* Mon Apr 11 2011 Petr Sabata <psabata@redhat.com> - 1.100-2
- Include libbsd stdlib, rhbz#694407
- Use %zd format for size_t

* Tue Mar 08 2011 Petr Sabata <psabata@redhat.com> - 1.100-1
- Update to current upstream
- Moving from glib to libbsd
- Including __b64_ntop() implementation taken from nsd
- Patches cleanup (most included upstream now)

* Tue Mar 01 2011 Petr Sabata <psabata@redhat.com> - 1.84-26
- Spec cleanup, removed buildroot garbage

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.84-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Oct 20 2010 Ville Skytta <ville.skytta@iki.fi> - 1.84-24
- Own the %%{_datadir}/nc dir.

* Fri Oct 08 2010 Petr Sabata <psabata@redhat.com> - 1.84-23
- accept ports separated by commas, patch by Jonathan Kamens
- rhbz#622204

* Wed Jan 06 2010 Jan Zeleny <jzeleny@redhat.com> - 1.84-22
- some updates in spec file in order to complete merge review
- changed location of testing scripts to /usr/share/nc/scripts

* Mon Jul 27 2009 Jan Zeleny <jzeleny@redhat.com> - 1.84-21
- fixed segfault when listening to socket and -v enabled (#513925)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.84-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Apr 03 2009 Jan Zeleny <jzeleny@redhat.com> - 1.84-19
- updated network reading to be more efficient (#493129)

* Fri Feb 27 2009 Jan Safranek <jsafrane@redhat.com> - 1.84-18
- fixed compilation with GCC 4.4

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.84-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.84-16
- Autorebuild for GCC 4.3

* Mon Jan  7 2008 Jan Safranek <jsafrane@redhat.com> - 1.84-15
- fixed compilation with gcc 4.3

* Wed Dec  5 2007 Radek Vokál <rvokal@redhat.com> - 1.84-14
- rebuilt

* Thu Aug 23 2007 Radek Vokál <rvokal@redhat.com> - 1.84-13
- rebuilt

* Wed Mar 14 2007 Radek Vokál <rvokal@redhat.com> - 1.84-12
- fix manpage for -C option (#203931)

* Tue Feb 13 2007 Radek Vokál <rvokal@redhat.com> - 1.84-11
- few spec file changes

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 1.84-10
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Tue Sep 26 2006 Radek Vokal <rvokal@redhat.com> - 1.84-9
- fix in crlf patch, -z option now works again (#207733)

* Tue Aug 29 2006 Radek Vokal <rvokal@redhat.com> - 1.84-8
- fix verbose option (#202321) <varmojfekoj@gmail.com>

* Mon Aug 28 2006 Radek Vokal <rvokal@redhat.com> - 1.84-7
- add dist tag
- add '-C' option and behaviour for sending CRLFs as line-ending (#203931) <koszorus@reidea.hu>

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.84-6.1
- rebuild

* Mon Jul 10 2006 Radek Vokal <rvokal@redhat.com> - 1.84-6
- improve UDP port scanning (#159119) <varmojfekoj@gmail.com>

* Mon Jul 10 2006 Radek Vokal <rvokal@redhat.com> - 1.84-5
- stop hanging when used as a UDP client (#188976) <varmojfekoj@gmail.com>

* Mon Mar 06 2006 Radek Vokál <rvokal@redhat.com> - 1.84-4
- timeout works also for connect (#182736)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.84-3.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.84-3.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan 25 2006 Radek Vokal <rvokal@redhat.com> 1.84-3
- warnings cleaned-up, compile with -Werror

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Dec 07 2005 Radek Vokal <rvokal@redhat.com> 1.84-2
- fix build requires

* Fri Nov 18 2005 Radek Vokal <rvokal@redhat.com> 1.84-1
- follow upstream

* Fri Oct 21 2005 Radek Vokal <rvokal@redhat.com> 1.82-2
- use SO_REUSEADDR (#171315)

* Tue Sep 27 2005 Tomas Mraz <tmraz@redhat.com> 1.82-1
- update from OpenBSD upstream CVS
- fix pollhup patch so it reads everything before shutdown

* Wed May 11 2005 David Woodhouse <dwmw2@redhat.com> 1.78-2
- Don't ignore POLLHUP and go into an endless loop (#156835)

* Mon Apr 11 2005 Radek Vokal <rvokal@redhat.com> 1.78-1
- update from CVS, using glib functions

* Thu Mar 31 2005 Radek Vokal <rvokal@redhat.com> 1.77-1
- switching to new OpenBSD version of netcat

* Fri Mar 04 2005 Radek Vokal <rvokal@redhat.com> 1.10-25
- gcc4 rebuilt

* Wed Dec 22 2004 Radek Vokal <rvokal@redhat.com> 1.10-24
- enabling telnet support (#143498)
- removed static linking
- array range fixed

* Mon Nov 01 2004 Radek Vokal <rvokal@redhat.com> 1.10-23
- return value of help function fixed (#137785)

* Tue Sep 21 2004 Radek Vokal <rvokal@redhat.com> 1.10-22
- timeout option patch when SIGALRM blocked (#132973)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Dec 11 2002 Tim Powers <timp@redhat.com> 1.10-17
- rebuild on all arches

* Tue Jul 23 2002 Bill Nottingham <notting@redhat.com> 1.10-16
- fix for the parsing patch (<eedmoba@eede.ericsson.se>)

* Thu Jul 18 2002 Bill Nottingham <notting@redhat.com> 1.10-15
- don't strip binaries
- fix parsing of some services (#52874) (<eedmoba@eede.ericsson.se>)
- fix man page (#63544)

