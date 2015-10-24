Summary: A secure replacement for inetd
Name: xinetd
Version: 2.3.15
Release: 16%{?dist}
License: xinetd
Group: System Environment/Daemons
Epoch: 2
URL: https://github.com/xinetd-org/xinetd
# source can be downloaded at
# https://github.com/xinetd-org/xinetd/archive/xinetd-2-3-15.tar.gz
Source: xinetd-%{version}.tar.gz
Source1: xinetd.service
Patch0: xinetd-2.3.15-pie.patch
Patch4: xinetd-2.3.14-bind-ipv6.patch
Patch6: xinetd-2.3.14-man-section.patch
Patch7: xinetd-2.3.15-PIE.patch
Patch8: xinetd-2.3.14-ident-bind.patch
Patch9: xinetd-2.3.14-readable-debuginfo.patch
# Patch for clean reconfiguration using newer versions of autotools
Patch10: xinetd-2.3.14-autoconf.patch
# Completely rewritten socket handling code (it uses poll() instead
# of select() function)
Patch11: xinetd-2.3.14-poll.patch
# New configuration option (limit for files opened by child process)
Patch12: xinetd-2.3.14-file-limit.patch
# When using tcpmux, xinetd ended up with sigsegv
# (detection of NULL pointer in pollfd structure was missing)
Patch13: xinetd-2.3.14-tcpmux.patch
# When service is destroyed, destroy also its
# file descriptor in array given to poll function
Patch14: xinetd-2.3.14-clean-pfd.patch
# xinetd confuses ipv6 and ipv4 port parsing
# - furtunately, they have the same format, so everything
#   works even without this patch
Patch15: xinetd-2.3.14-ipv6confusion.patch
# This fixes bug #593904 - online reconfiguration caused log message
# flood when turning off UDP service
Patch16: xinetd-2.3.14-udp-reconfig.patch
Patch18: xinetd-2.3.14-rpc-specific-port.patch
Patch19: xinetd-2.3.14-signal-log-hang.patch
Patch20: xinetd-2.3.14-fix-type-punned-ptr.patch
# Fix leaking file descriptors and pfd_array wasting
# This fixes #702670
Patch21: xinetd-2.3.14-leaking-fds.patch
# Fix memory corruption when loading a large number of services
# This fixes #720390
Patch22: xinetd-2.3.14-many-services.patch
# Remove realloc of fds that was causing memory corruption
Patch23: xinetd-2.3.14-realloc-remove.patch
# Fix leaking descriptor when starting a service fails
Patch24: xinetd-2.3.14-leaking-fds-2a.patch
# Fix #770858 - Instances limit in xinetd can be easily bypassed
Patch25: xinetd-2.3.14-instances.patch
# Fix #809272 - Service disabled due to bind failure
Patch26: xinetd-2.3.14-retry-svc-activate-in-cps-restart.patch
Patch27: xinetd-2.3.15-bad-port-check.patch
# Fix #977873 - Use full path to server when checking selinux context
Patch28: xinetd-2.3.15-context-exepath.patch
Patch29: xinetd-2.3.15-creds.patch
# Fix #1033528 - xinetd segfaults when connecting to tcpmux service
Patch30: xinetd-2.3.15-tcpmux-nameinargs-disable-service.patch

BuildRequires: autoconf, automake
BuildRequires: libselinux-devel >= 1.30
BuildRequires: systemd-units
Requires(post): systemd-sysv
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
%{!?tcp_wrappers:BuildRequires: tcp_wrappers-devel}
Requires: filesystem >= 2.0.1, setup, fileutils
Provides: inetd


%description
Xinetd is a secure replacement for inetd, the Internet services
daemon. Xinetd provides access control for all services based on the
address of the remote host and/or on time of access and can prevent
denial-of-access attacks. Xinetd provides extensive logging, has no
limit on the number of server arguments, and lets you bind specific
services to specific IP addresses on your host machine. Each service
has its own specific configuration file for Xinetd; the files are
located in the /etc/xinetd.d directory.

%prep
%setup -q

# SPARC/SPARC64 needs -fPIE/-PIE
# This really should be detected by configure.
%ifarch sparcv9 sparc64
%patch7 -p1 -b .PIE
%else
%patch0 -p1 -b .pie
%endif
%patch4 -p1 -b .bind
%patch6 -p1 -b .man-section
%patch8 -p1 -b .ident-bind
%patch9 -p1 -b .readable-debuginfo
%patch10 -p1 -b .autoconf
%patch11 -p1 -b .poll
%patch12 -p1 -b .file-limit
%patch13 -p1 -b .tcpmux
%patch14 -p1 -b .clean-pfd
%patch15 -p1 -b .ipv6confusion
%patch16 -p1 -b .udp-reconfig
%patch18 -p1 -b .rpc-specific-port
%patch19 -p1 -b .signal-log-hang
%patch20 -p1 -b .fix-type-punned-ptr
%patch21 -p1 -b .leaking-fds
%patch22 -p1 -b .many-services
%patch23 -p1 -b .realloc-remove
%patch24 -p1 -b .leaking-fds-2a
%patch25 -p1 -b .instances
%patch26 -p1 -b .retry-svc-activate
%patch27 -p1 -b .bad-port-check
%patch28 -p1 -b .context-exepath
%patch29 -p1 -b .creds
%patch30 -p1

aclocal
autoconf

%build
# -pie -PIE flags added by separate patches
export LDFLAGS="$LDFLAGS -Wl,-z,relro,-z,now"
%configure --with-loadavg --with-inet6 %{!?tcp_wrappers:--with-libwrap} --with-labeled-networking
make

%install
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
mkdir -m 700 -p $RPM_BUILD_ROOT/etc/xinetd.d/
# Remove unneeded service
rm -f contrib/xinetd.d/ftp-sensor
%make_install DAEMONDIR=$RPM_BUILD_ROOT/usr/sbin MANDIR=$RPM_BUILD_ROOT/%{_mandir}
install -m 600 contrib/xinetd.conf $RPM_BUILD_ROOT/etc
install -m 600 contrib/xinetd.d/* $RPM_BUILD_ROOT/etc/xinetd.d
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_unitdir}

rm -f $RPM_BUILD_ROOT/%{_mandir}/man8/itox*
rm -f $RPM_BUILD_ROOT/usr/sbin/itox
rm -f $RPM_BUILD_ROOT/%{_mandir}/man8/xconv.pl*
rm -f $RPM_BUILD_ROOT/usr/sbin/xconv.pl

%post
%systemd_post xinetd.service

%preun
%systemd_preun xinetd.service

%postun
%systemd_postun_with_restart xinetd.service

%files
%doc CHANGELOG COPYRIGHT README xinetd/sample.conf contrib/empty.conf
%config(noreplace) /etc/xinetd.conf
%{_unitdir}/xinetd.service
%config(noreplace) /etc/xinetd.d/*
/usr/sbin/xinetd
%{_mandir}/*/*

%changelog
* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:2.3.15-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:2.3.15-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:2.3.15-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Feb 24 2014 Jan Synáček <jsynacek@redhat.com> - 2:2.3.15-13
- drop sysconfig-related stuff
- add documentation reference to the service file

* Tue Jan 14 2014 Jan Synáček <jsynacek@redhat.com> - 2:2.3.15-12
- fix bad URL

* Fri Dec 13 2013 Jan Synáček <jsynacek@redhat.com> - 2:2.3.15-11
- fixup of the previous patch
- Resolves: #1042652
- Related: #1033528

* Tue Dec  3 2013 Jan Synáček <jsynacek@redhat.com> - 2:2.3.15-10
- xinetd segfaults when connecting to tcpmux service
- Resolves: #1033528

* Fri Oct  4 2013 Jan Synáček <jsynacek@redhat.com> - 2:2.3.15-9
- xinetd should not depend on NetworkManager-wait-online
- Resolves: #1002294

* Thu Oct  3 2013 Jan Synáček <jsynacek@redhat.com> - 2:2.3.15-8
- Honor user and group directives
- Resolves: CVE-2013-4342

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:2.3.15-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jun 26 2013 Jan Synáček <jsynacek@redhat.com> - 2:2.3.15-6
- Use full path to server when checking selinux context
- Resolves: #977873

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:2.3.15-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Sep 03 2012 Jan Synáček <jsynacek@redhat.com> - 2:2.3.15-4
- Change config files' permissions
- Resolves: #853144

* Wed Aug 22 2012 Jan Synáček <jsynacek@redhat.com> - 2:2.3.15-3
- Replace the makeinstall macro
- Add systemd-rpm macros
- Resolves: #850370

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:2.3.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon May 14 2012 Jan Synáček <jsynacek@redhat.com> - 2:2.3.15-1
- Update to 2.3.15
- Drop patches merged by upstream
  (-log-crash, -tcp_rpc, -label, -contextconf, -ssize_t)
- Update -pie, -PIE, -poll patch
- Resolves: #820927
- Add -bad-port-check patch

* Fri Apr 13 2012 Jan Synáček <jsynacek@redhat.com> - 2:2.3.14-46
- Fix: service file: avoid problems when name resolution is not ready
- Resolves: #748931

* Fri Apr 13 2012 Jan Synáček <jsynacek@redhat.com> - 2:2.3.14-45
- Fix: Service disabled due to bind failure
- Update patch: xinetd-2.3.14-leaking-fds-2.patch
- Resolves: #809272

* Mon Mar 05 2012 Jan Synáček <jsynacek@redhat.com> - 2:2.3.14-44
- Fix: Instances limit in xinetd can be easily bypassed
- Resolves: #770858

* Mon Mar 05 2012 Jan Synáček <jsynacek@redhat.com> - 2:2.3.14-43
- Fix xinetd.service permissions
- Remove useless INSTALL from package documentation
- Implement reload in xinetd.service

* Fri Mar 02 2012 Jan Synáček <jsynacek@redhat.com> - 2:2.3.14-42
- Fix leaking descriptor when starting a service fails (#795188)

* Wed Jan 18 2012 Jan Synáček <jsynacek@redhat.com> - 2:2.3.14-41
- Remove realloc inside svc_activate that was causing memory corruption
- Number of alloc'd file descriptors is now determined by system limits (ulimit -n)
- Add patch -realloc-remove

* Tue Jan 17 2012 Jan Synáček <jsynacek@redhat.com> - 2:2.3.14-40
- Fix memory corruption when loading a large number of services
- Resolves #720390

* Mon Jan 16 2012 Jan Synáček <jsynacek@redhat.com> - 2:2.3.14-39
- Fix leaking file descriptors
- Resolves: #702670

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:2.3.14-38
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Sep 12 2011 Tom Callaway <spot@fedoraproject.org> - 2:2.3.14-37
- covert to systemd

* Thu Apr 21 2011 Vojtech Vitek (V-Teq) <vvitek@redhat.com> - 2:2.3.14-36
- Fix build warning about "dereferencing type-punned pointer"
  Related: #695674
- Avoid possible hang while logging an unexpected signal
  Related: #501604
- Let RPC services bind to a specific port
  Related: #624800

* Fri Feb 18 2011 Vojtech Vitek (V-Teq) <vvitek@redhat.com> - 2:2.3.14-35
- fix crash when application's logfile hit size limit
  Related: #244063

* Mon Feb 14 2011 Vojtech Vitek (V-Teq) <vvitek@redhat.com> - 2:2.3.14-34
- Add -Wl,-z,relro,-z,now to LDFLAGS

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:2.3.14-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jun 02 2010 Jan Zeleny <jzeleny@redhat.com> - 2:2.3.14-32
- fixed log message flooding when turning off UDP service during online
  reconfiguration (#593904)

* Fri Mar 19 2010 Jan Zeleny <jzeleny@redhat.com> - 2:2.3.14-31
- corrected port parsing code (IPv4 and IPv6 were switched)
- commented patches I'm familiar with in spec file

* Fri Mar 19 2010 Jan Zeleny <jzeleny@redhat.com> - 2:2.3.14-30
- fixed flooding log with error messages when disabled service at runtime
- updated release number to 30 to prevent rpm from detecting this as downgrade

* Thu Jan 21 2010 Jan Zeleny <jzeleny@redhat.com> - 2:2.3.14-28
- fixed issue with tcpmux service (#543968)

* Tue Oct 20 2009 Jan Zeleny <jzeleny@redhat.com> - 2:2.3.14-27
- last update of init script modified to work with SELinux correctly
- added support for new configuration option - file limit for service

* Mon Oct 12 2009 Jan Zeleny <jzeleny@redhat.com> - 2:2.3.14-26
- updated init script (LSB compliance - #528154)

* Thu Sep 17 2009 Jan Zeleny <jzeleny@redhat.com> - 2:2.3.14-25
- correction of last patch replacing select() with poll()

* Mon Sep 14 2009 Jan Zeleny <jzeleny@redhat.com> - 2:2.3.14-24
- select() function and it's supporting macros replaced by poll() and it's supporting macros
- added patch of configure.in for clean compilation

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:2.3.14-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:2.3.14-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Sep 18 2008 Jan Safranek <jsafranek@redhat.com> - 2:2.3.14-21
- fix glitches found during package review (#226560)
- make all files in .debuginfo package readable by everyone

* Wed Jul 16 2008 Jan Safranek <jsafranek@redhat.com> - 2:2.3.14-20
- fix wrong bind() call (#448069)

* Thu May 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2:2.3.14-19
- fix sparc fPIE issues

* Thu Jan 31 2008 Jan Safranek <jsafranek@redhat.com> - 2:2.3.14-18
- fixed LABEL flag (#430929)

* Wed Jan 30 2008 Jan Safranek <jsafranek@redhat.com> - 2:2.3.14-17
- fixing init scripts (#430816)

* Mon Jan 28 2008 Jan Safranek <jsafranek@redhat.com> - 2:2.3.14-16
- xinetd.log man page is in the right section now (#428812)

* Thu Sep  6 2007 Jan Safranek <jsafranek@redhat.com> - 2:2.3.14-15
- initscript made LSB compliant (#247099)

* Thu Sep  6 2007 Jan Safranek <jsafranek@redhat.com> - 2:2.3.14-14
- removed inetdconvert script, nobody is using inetd

* Wed Aug 22 2007 Jan Safranek <jsafranek@redhat.com> - 2:2.3.14-13
- updated license field

* Wed May 16 2007 Jan Safranek <jsafranek@redhat.com> - 2:2.3.14-12
- bind IPv6 socket by default and switch to IPv4 on error
  (bz#195265)
- service xinetd status returns actual status (bz#232887)
- use ssize_t instead of int (bz#211776)

* Mon Dec  4 2006 Thomas Woerner <twoerner@redhat.com> - 2:2.3.14-11
- tcp_wrappers has a new devel and libs sub package, therefore changing build
  requirement for tcp_wrappers to tcp_wrappers-devel

* Fri Dec 01 2006 James Antill <james.antill@redhat.com> - 2:2.3.14-9
- Fix getpeercon() for LABELED networking MLS environments
- Resolves: rhbz#209379

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 2:2.3.14-8
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Wed Sep 20 2006 Steve Grubb <sgrubb@redhat.com> 2:2.3.14-7
- Revised labeled networking patch to not allow redirection

* Tue Aug 29 2006 Steve Grubb <sgrubb@redhat.com> 2:2.3.14-6
- Revised labeled networking patch again

* Thu Aug 24 2006 Steve Grubb <sgrubb@redhat.com> 2:2.3.14-5
- Revised labeled networking patch

* Wed Aug 23 2006 Steve Grubb <sgrubb@redhat.com> 2:2.3.14-4
- Added labeled networking patch

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2:2.3.14-3.1
- rebuild

* Fri Jun 16 2006 Steve Grubb <sgrubb@redhat.com> 2:2.3.14-3
- Rework spec file & use xinetd's sevice config files

* Fri Mar 24 2006 Jay Fenlason <fenlason@redhat.com> 2:2.3.14-2
- Upgrade to new upstream version.  This obsoletes the -libwrap,
  -rpc, -banner, -bug140084 and -gcc4 patches.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2:2.3.13-6.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2:2.3.13-6.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Feb 17 2005 Jay Fenlason <fenlason@redhat.com> 2:2.3.13-6
- include new patch to allow gcc4 to compile xinetd.

* Sat Jan 8 2005 Jay Fenlason <fenlason@redhat.com> 2:2.3.13-4
- Added patch committed to upstream CVS to fix bz#140084
  (error logging accidentally using one of [012] as the syslog
  descriptor)

* Fri Jun 18 2004 Jay Fenlason <fenlason@redhat.com> 2:2.3.13-3
- Add patch to fix #126242: banner's don't work

* Thu Jun 17 2004 Jay Fenlason <fenlason@redhat.com>
- Remove the configuration for the no-longer-present "services" service.
  Closes #126169

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri May 14 2004 Jay Fenlason <fenlason@redhat.com>
- Add patch to allow multiple rpc services to cooexist as long as they're
  different program numbers or different versions.

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Jan 29 2004 Jay Fenlason <fenlason@redhat.com> 2.3.13-1
- Upgrade to new upstream version, which obsoletes most patches.
- Add new tcp_rpc patch, to turn on the nolibwrap flag on tcp rpc services,
  since libwrap cannot be used on them.

* Sun Dec 28 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- use new technology to filter python dep for inetdconvert instead
  of changing the -x bit on file permissions

