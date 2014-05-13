%define snapshot .svn457

Name:		vpnc
Version:	0.5.3
Release:	21%{snapshot}%{?dist}

Summary:	IPSec VPN client compatible with Cisco equipment

Group:		Applications/Internet
License:	GPLv2+
URL:		http://www.unix-ag.uni-kl.de/~massar/vpnc/
Source0:	http://www.unix-ag.uni-kl.de/~massar/vpnc/%{name}-%{version}%{snapshot}.tar.gz
Source1:	generic-vpnc.conf
Source2:	vpnc.consolehelper
Source3:	vpnc-disconnect.consolehelper
Source4:	vpnc.pam
Source5:	vpnc-helper
# vpnc-script based on http://git.infradead.org/users/dwmw2/vpnc-scripts.git
# local changes sent upstream
Source7:	vpnc-script
Source8:	%{name}-tmpfiles.conf

Patch1:		vpnc-0.5.1-dpd.patch
Patch2:		vpnc-0.5.3-use-autodie.patch

BuildRequires:	libgcrypt-devel > 1.1.90
BuildRequires:	gnutls-devel
BuildRequires:	perl(autodie)
Requires:	iproute vpnc-script
Requires:	initscripts

%description
A VPN client compatible with Cisco's EasyVPN equipment.

Supports IPSec (ESP) with Mode Configuration and Xauth.  Supports only
shared-secret IPSec authentication, 3DES, MD5, and IP tunneling.

%package consoleuser
Summary:	Allows console user to run the VPN client directly
Group:		Applications/Internet
Requires:	vpnc = %{version}-%{release}
Requires:	usermode

%description consoleuser
Allows the console user to run the IPSec VPN client directly without
switching to the root account.

%package script
Summary:	Routing setup script for vpnc and openconnect
Group:		Applications/Internet
BuildArch:	noarch

%description script
This script sets up routing for VPN connectivity, when invoked by vpnc
or openconnect.


%prep
%setup -q
%patch1 -p1 -b .dpd
%patch2 -p1 -b .autodie

%build
CFLAGS="$RPM_OPT_FLAGS -fPIE" LDFLAGS="$RPM_OPT_FLAGS -pie" make PREFIX=/usr 

%install
make install DESTDIR="$RPM_BUILD_ROOT" PREFIX=/usr
rm -f $RPM_BUILD_ROOT%{_bindir}/pcf2vpnc
chmod 0644 pcf2vpnc
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/pcf2vpnc.1
chmod 0644 $RPM_BUILD_ROOT%{_mandir}/man8/vpnc.8
install -m 0600 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/vpnc/default.conf
install -Dp -m 0644 %{SOURCE2} \
    $RPM_BUILD_ROOT%{_sysconfdir}/security/console.apps/vpnc
install -Dp -m 0644 %{SOURCE3} \
    $RPM_BUILD_ROOT%{_sysconfdir}/security/console.apps/vpnc-disconnect
install -Dp -m 0644 %{SOURCE4} \
    $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/vpnc
install -Dp -m 0644 %{SOURCE4} \
    $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/vpnc-disconnect
install -m 0755 %{SOURCE5} \
    $RPM_BUILD_ROOT%{_sbindir}/vpnc-helper
install -m 0755 %{SOURCE7} \
    $RPM_BUILD_ROOT%{_sysconfdir}/vpnc/vpnc-script
mkdir -p $RPM_BUILD_ROOT%{_bindir}
ln -sf consolehelper $RPM_BUILD_ROOT%{_bindir}/vpnc
ln -sf consolehelper $RPM_BUILD_ROOT%{_bindir}/vpnc-disconnect
rm -f $RPM_BUILD_ROOT%{_datadir}/doc/vpnc/COPYING

mkdir -p %{buildroot}%{_sysconfdir}/tmpfiles.d
install -m 0644 %{SOURCE8} %{buildroot}%{_sysconfdir}/tmpfiles.d/%{name}.conf

mkdir -p %{buildroot}%{_localstatedir}/run/
install -d -m 0755 %{buildroot}%{_localstatedir}/run/%{name}/

%files
%defattr(-,root,root)
%doc README COPYING pcf2vpnc pcf2vpnc.1

%config(noreplace) %{_sysconfdir}/tmpfiles.d/%{name}.conf
%config(noreplace) %{_sysconfdir}/vpnc/default.conf
%{_sbindir}/vpnc
%{_bindir}/cisco-decrypt
%{_sbindir}/vpnc-disconnect
%{_mandir}/man8/vpnc.*
%{_mandir}/man1/cisco-decrypt.*
%dir %{_localstatedir}/run/%{name}/

%files consoleuser
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/security/console.apps/vpnc*
%config(noreplace) %{_sysconfdir}/pam.d/vpnc*
%{_bindir}/vpnc*
%{_sbindir}/vpnc-helper

%files script
%defattr(-,root,root)
%dir %{_sysconfdir}/vpnc
%config(noreplace) %{_sysconfdir}/vpnc/vpnc-script

%changelog
* Tue May 06 2014 Liu Di <liudidi@gmail.com> - 0.5.3-21.svn457
- 为 Magic 3.0 重建

* Fri Nov 15 2013 Paul Wouters <pwouters@redhat.com> - 0.5.3-20.svn457
- Actually patch the vpnc-script we ship with the unbound patch

* Mon Sep 23 2013 Paul Wouters <pwouters@redhat.com> - 0.5.3-19.svn457
- Add support for dynamically reconfiguring unbound DNS (rhbz#865092)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-18.svn457
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar  7 2013 Tomáš Mráz <tmraz@redhat.com> - 0.5.3-17.svn457
- Make it build
- Remove vpnc-cleanup upstart configuration file

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-16.svn457
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-15.svn457
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-14.svn457
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Sep 11 2011 Christian Krause <chkr@fedoraproject.org> - 0.5.3-13.svn457
- Use tmpfiles.d service to correctly handle /var/run/vpnc (#656719)
- Update vpnc-script:
  - fix negative MTU (#693235)
  - use restorecon to relabel /dev/net and /var/run/vpnc (#731382)
- Various minor spec file cleanup

* Thu Jul 21 2011 Dan Williams <dcbw@redhat.com> - 0.5.3-12.svn457
- Update to svn snapshot r457
- Enable support for Hybrid XAUTH (see rh #677419)

* Sat May 28 2011 David Woodhouse <David.Woodhouse@intel.com> - 0.5.3-11
- Update vpnc-script to cope with 'ipid' in route list.

* Sun Feb 27 2011 Ville Skyttä <ville.skytta@iki.fi> - 0.5.3-10
- Move /etc/vpnc dir ownership to vpnc-script (#680783).

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 17 2010 Dan Williams <dcbw@redhat.com> - 0.5.3-8
- Remove dependency on upstart since we use systemd now

* Wed Dec  9 2009 Bill Nottingham <notting@redhat.com> - 0.5.3-7
- Adjust for upstart 0.6

* Tue Nov 17 2009 David Woodhouse <David.Woodhouse@intel.com> - 0.5.3-6
- Update vpnc-script to support IPv6 properly

* Tue Nov  3 2009 David Woodhouse <David.Woodhouse@intel.com> - 0.5.3-5
- Split vpnc-script out into separate package

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Nov 20 2008 Tomas Mraz <tmraz@redhat.com> - 0.5.3-2
- upgrade to new version
- fix race in vpnc-cleanup (#465315)

* Thu Jul 24 2008 Tomas Mraz <tmraz@redhat.com> - 0.5.1-6
- do not modify domain in resolv.conf (#446404)
- clean up modified resolv.conf on startup (#455899)

* Sat Apr  5 2008 Michal Schmidt <mschmidt@redhat.com> - 0.5.1-5
- vpnc-script: fix 'ip link ...' syntax.

* Thu Apr  3 2008 Tomas Mraz <tmraz@redhat.com> - 0.5.1-4
- drop autogenerated perl requires (#440304)
- compute MTU based on default route device (#433846)

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.5.1-3
- Autorebuild for GCC 4.3

* Tue Nov 13 2007 Tomas Mraz <tmraz@redhat.com> - 0.5.1-2
- try to make DPD less sensitive (#345281)

* Thu Sep 20 2007 Tomas Mraz <tmraz@redhat.com> - 0.5.1-1
- upgrade to latest upstream

* Mon Sep  3 2007 Tomas Mraz <tmraz@redhat.com> - 0.4.0-4
- fix long standing bug causing problems on x86_64 (#232565) now for real

* Wed Aug 22 2007 Tomas Mraz <tmraz@redhat.com> - 0.4.0-3
- license tag fix

* Tue Mar 20 2007 Tomas Mraz <tmraz@redhat.com> - 0.4.0-2
- -fstack-protector miscompilation on x86_64 is back (#232565)

* Mon Feb 26 2007 Tomas Mraz <tmraz@redhat.com> - 0.4.0-1
- upgrade to new upstream version

* Wed Jan 17 2007 Tomas Mraz <tmraz@redhat.com> - 0.3.3-15
- do not overwrite personalized vpnc scripts (#195842)
- we must not allow commandline options to vpnc when run through consolehelper

* Wed Jan 17 2007 Tomas Mraz <tmraz@redhat.com> - 0.3.3-14
- add consoleuser subpackage (#160571)
- fix permissions on manpage (#222578)

* Tue Nov  7 2006 Tomas Mraz <tmraz@redhat.com> - 0.3.3-13
- don't leak socket fds

* Tue Sep 12 2006 Tomas Mraz <tmraz@redhat.com> - 0.3.3-12
- drop hoplimit from ip route output (#205923)
- let's try enabling -fstack-protector again, seems to work now

* Thu Sep  7 2006 Tomas Mraz <tmraz@redhat.com> - 0.3.3-11
- rebuilt for FC6

* Wed Jun  7 2006 Tomas Mraz <tmraz@redhat.com> 0.3.3-9
- drop the -fstack-protector not -f-stack-protector

* Tue May 30 2006 Tomas Mraz <tmraz@redhat.com> 0.3.3-8
- drop -fstack-protector from x86_64 build (workaround for #172145)
- make rekeying a little bit better

* Thu Mar  9 2006 Tomas Mraz <tmraz@redhat.com> 0.3.3-7
- add basic rekeying support (the patch includes NAT keepalive support
  by Brian Downing)
- dropped disconnect patch (solved differently)

* Wed Feb 15 2006 Tomas Mraz <tmraz@redhat.com> 0.3.3-6
- rebuild with new gcc

* Tue Jan 24 2006 Tomas Mraz <tmraz@redhat.com> 0.3.3-5
- send the disconnect packet properly (patch by Laurence Moindrot)

* Thu Sep 22 2005 Tomas Mraz <tmraz@redhat.com> 0.3.3-4
- improve compatibility with some Ciscos

* Wed Jun 15 2005 Tomas Mraz <tmraz@redhat.com> 0.3.3-3
- improve fix_ip_get_output in vpnc-script (#160364)

* Mon May 30 2005 Tomas Mraz <tmraz@redhat.com> 0.3.3-2
- package /var/run/vpnc and ghost files it can contain (#159015)
- add /sbin /usr/sbin to the path in vpnc-script (#159099)

* Mon May 16 2005 Tomas Mraz <tmraz@redhat.com> 0.3.3-1
- new upstream version

* Thu Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Wed Jan 05 2005 Warren Togami <wtogami@redhat.com> 0.3.2-3
- Fix 64bit

* Thu Dec 23 2004 Warren Togami <wtogami@redhat.com> 0.3.2-2
- make PIE (davej)

* Mon Dec 20 2004 Warren Togami <wtogami@redhat.com> 0.3.2-1
- 0.3.2
