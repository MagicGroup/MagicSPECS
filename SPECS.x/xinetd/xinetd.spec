Summary: A secure replacement for inetd
Name: xinetd
Version: 2.3.14
Release: 42%{?dist}
License: xinetd 
Group: System Environment/Daemons
Epoch: 2
URL: http://www.xinetd.org
Source: http://www.xinetd.org/xinetd-%{version}.tar.gz
Source1: xinetd.service
Source3: xinetd.sysconf
Patch0: xinetd-2.3.11-pie.patch
Patch1: xinetd-2.3.12-tcp_rpc.patch
Patch2: xinetd-2.3.14-label.patch
Patch3: xinetd-2.3.14-contextconf.patch
Patch4: xinetd-2.3.14-bind-ipv6.patch
Patch5: xinetd-2.3.14-ssize_t.patch
Patch6: xinetd-2.3.14-man-section.patch
Patch7: xinetd-2.3.11-PIE.patch
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
Patch17: xinetd-2.3.13-log-crash.patch
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

BuildRequires: autoconf, automake
BuildRequires: systemd-units
Requires(post): systemd-sysv
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
%{!?tcp_wrappers:BuildRequires: tcp_wrappers-devel}
Requires: filesystem >= 2.0.1, initscripts, setup, fileutils
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
%patch7 -p0 -b .PIE
%else
%patch0 -p0 -b .pie
%endif
%patch1 -p1 -b .tcp_rpc
%patch2 -p1 -b .lspp
%patch3 -p1 -b .confcntx
%patch4 -p1 -b .bind
%patch5 -p1 -b .ssize_t
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
%patch17 -p1 -b .log-crash
%patch18 -p1 -b .rpc-specific-port
%patch19 -p1 -b .signal-log-hang
%patch20 -p1 -b .fix-type-punned-ptr
%patch21 -p1 -b .leaking-fds
%patch22 -p1 -b .many-services
%patch23 -p1 -b .realloc-remove

aclocal
autoconf

%build
# -pie -PIE flags added by separate patches
export LDFLAGS="$LDFLAGS -Wl,-z,relro,-z,now"
%configure --with-loadavg --with-inet6 %{!?tcp_wrappers:--with-libwrap} --with-labeled-networking
make

%install
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
mkdir -p $RPM_BUILD_ROOT/etc/xinetd.d/
# Remove unneeded service
rm -f contrib/xinetd.d/ftp-sensor
%makeinstall DAEMONDIR=$RPM_BUILD_ROOT/usr/sbin MANDIR=$RPM_BUILD_ROOT/%{_mandir}
install -m 644 contrib/xinetd.conf $RPM_BUILD_ROOT/etc
install -m 644 contrib/xinetd.d/* $RPM_BUILD_ROOT/etc/xinetd.d
install -m 755 %{SOURCE1} $RPM_BUILD_ROOT%{_unitdir}

rm -f $RPM_BUILD_ROOT/%{_mandir}/man8/itox*
rm -f $RPM_BUILD_ROOT/usr/sbin/itox
rm -f $RPM_BUILD_ROOT/%{_mandir}/man8/xconv.pl*
rm -f $RPM_BUILD_ROOT/usr/sbin/xconv.pl

mkdir -p $RPM_BUILD_ROOT/etc/sysconfig
install -m 644 %SOURCE3 $RPM_BUILD_ROOT/etc/sysconfig/xinetd

%post
if [ $1 -eq 1 ] ; then 
    # Initial installation
    /bin/systemctl enable xinetd.service >/dev/null 2>&1 || :
fi

%preun
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable xinetd.service > /dev/null 2>&1 || :
    /bin/systemctl stop xinetd.service > /dev/null 2>&1 || :
fi

%postun
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /bin/systemctl try-restart xinetd.service >/dev/null 2>&1 || :
fi

%triggerun -- xinetd < 2:2.3.14-37
# Save the current service runlevel info
# User must manually run systemd-sysv-convert --apply xinetd
# to migrate them to systemd targets
/usr/bin/systemd-sysv-convert --save xinetd >/dev/null 2>&1 ||:
/bin/systemctl --no-reload enable xinetd.service >/dev/null 2>&1 ||:

# Run these because the SysV package being removed won't do them
/sbin/chkconfig --del xinetd >/dev/null 2>&1 || :
/bin/systemctl try-restart xinetd.service >/dev/null 2>&1 || :

%files
%doc INSTALL CHANGELOG COPYRIGHT README xinetd/sample.conf contrib/empty.conf 
%config(noreplace) /etc/xinetd.conf
%config(noreplace) /etc/sysconfig/xinetd
%{_unitdir}/xinetd.service
%config(noreplace) /etc/xinetd.d/*
/usr/sbin/xinetd
%{_mandir}/*/*

%changelog
* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 2:2.3.14-42
- 为 Magic 3.0 重建

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

