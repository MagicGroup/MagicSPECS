%define testrelease 0
%define releasecandidate 0
%if 0%{testrelease}
  %define extrapath test-releases/
  %define extraversion test30
%endif
%if 0%{releasecandidate}
  %define extrapath release-candidates/
  %define extraversion rc1
%endif

Name:           dnsmasq
Version:	2.68
Release:        6%{?extraversion}%{?dist}
Summary:        A lightweight DHCP/caching DNS server
Summary(zh_CN.UTF-8): 一个轻量级的 DHCP/DNS缓存 服务

Group:          System Environment/Daemons
Group(zh_CN.UTF-8): 系统环境/服务
License:        GPLv2
URL:            http://www.thekelleys.org.uk/dnsmasq/
Source0:        http://www.thekelleys.org.uk/dnsmasq/%{?extrapath}%{name}-%{version}%{?extraversion}.tar.xz
Source1:        %{name}.service
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  dbus-devel
BuildRequires:  pkgconfig

BuildRequires:  systemd-units
Requires(post): systemd-units systemd-sysv chkconfig
Requires(preun): systemd-units
Requires(postun): systemd-units


%description
Dnsmasq is lightweight, easy to configure DNS forwarder and DHCP server.
It is designed to provide DNS and, optionally, DHCP, to a small network.
It can serve the names of local machines which are not in the global
DNS. The DHCP server integrates with the DNS server and allows machines
with DHCP-allocated addresses to appear in the DNS with names configured
either in each host or in a central configuration file. Dnsmasq supports
static and dynamic DHCP leases and BOOTP for network booting of diskless
machines.

%description -l zh_CN.UTF-8
一个轻量级的 DHCP 和 DNS 服务程序。

%package        utils
Summary:        Utilities for manipulating DHCP server leases
Summary(zh_CN.UTF-8): 处理 DHCP 服务的工具
Group:          System Environment/Daemons
Group(zh_CN.UTF-8): 系统环境/服务

%description    utils
Utilities that use the standard DHCP protocol to
query/remove a DHCP server's leases.

%description utils -l zh_CN.UTF-8
处理 DHCP 服务的工具。

%prep
%setup -q -n %{name}-%{version}%{?extraversion}

# use /var/lib/dnsmasq instead of /var/lib/misc
for file in dnsmasq.conf.example man/dnsmasq.8 man/es/dnsmasq.8 src/config.h; do
    sed -i 's|/var/lib/misc/dnsmasq.leases|/var/lib/dnsmasq/dnsmasq.leases|g' "$file"
done

#enable dbus
sed -i 's|/\* #define HAVE_DBUS \*/|#define HAVE_DBUS|g' src/config.h

#enable /etc/dnsmasq.d fix bz 526703
sed -i 's|#conf-dir=/etc/dnsmasq.d|conf-dir=/etc/dnsmasq.d|g' dnsmasq.conf.example


%build
# Note the main Makefile handles RPM_OPT_FLAGS internally,
# while we need to explicitly set it for the contrib Makefile
make %{?_smp_mflags}
CFLAGS="$RPM_OPT_FLAGS" make -C contrib/wrt %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
# normally i'd do 'make install'...it's a bit messy, though
mkdir -p $RPM_BUILD_ROOT%{_sbindir} \
        $RPM_BUILD_ROOT%{_mandir}/man8 \
        $RPM_BUILD_ROOT%{_var}/lib/dnsmasq \
        $RPM_BUILD_ROOT%{_sysconfdir}/dnsmasq.d \
        $RPM_BUILD_ROOT%{_sysconfdir}/dbus-1/system.d
install src/dnsmasq $RPM_BUILD_ROOT%{_sbindir}/dnsmasq
install dnsmasq.conf.example $RPM_BUILD_ROOT%{_sysconfdir}/dnsmasq.conf
install dbus/dnsmasq.conf $RPM_BUILD_ROOT%{_sysconfdir}/dbus-1/system.d/
install -m 644 man/dnsmasq.8 $RPM_BUILD_ROOT%{_mandir}/man8/

# utils sub package
mkdir -p $RPM_BUILD_ROOT%{_bindir} \
         $RPM_BUILD_ROOT%{_mandir}/man1
install -m 755 contrib/wrt/dhcp_release $RPM_BUILD_ROOT%{_bindir}/dhcp_release
install -m 644 contrib/wrt/dhcp_release.1 $RPM_BUILD_ROOT%{_mandir}/man1/dhcp_release.1
install -m 755 contrib/wrt/dhcp_lease_time $RPM_BUILD_ROOT%{_bindir}/dhcp_lease_time
install -m 644 contrib/wrt/dhcp_lease_time.1 $RPM_BUILD_ROOT%{_mandir}/man1/dhcp_lease_time.1

# Systemd
mkdir -p %{buildroot}%{_unitdir}
install -m644 %{SOURCE1} %{buildroot}%{_unitdir}
rm -rf %{buildroot}%{_initrddir}

magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ $1 -eq 1 ] ; then
    /usr/bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%preun
if [ $1 -eq 0 ]; then
  /usr/bin/systemctl --no-reload dnsmasq.service > /dev/null 2>&1 || :
  /usr/bin/systemctl stop dnsmasq.service > /dev/null 2>&1 || :
fi


%postun
/usr/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    /usr/bin/systemctl try-restart dnsmasq.service >/dev/null 2>&1 || :
fi

%triggerun -- dnsmasq < 2.52-3
%{_bindir}/systemd-sysv-convert --save dnsmasq >/dev/null 2>&1 ||:
/usr/sbin/chkconfig --del dnsmasq >/dev/null 2>&1 || :
/usr/bin/systemctl try-restart dnsmasq.service >/dev/null 2>&1 || :

%files
%defattr(-,root,root,-)
%doc CHANGELOG COPYING FAQ doc.html setup.html dbus/DBus-interface
%config(noreplace) %attr(644,root,root) %{_sysconfdir}/dnsmasq.conf
%dir /etc/dnsmasq.d
%dir %{_var}/lib/dnsmasq
%config(noreplace) %attr(644,root,root) %{_sysconfdir}/dbus-1/system.d/dnsmasq.conf
%{_unitdir}/%{name}.service
%{_sbindir}/dnsmasq
%{_mandir}/man8/dnsmasq*

%files utils
%{_bindir}/dhcp_*
%{_mandir}/man1/dhcp_*

%changelog
* Fri Mar 21 2014 Liu Di <liudidi@gmail.com> - 2.68-6
- 更新到 2.68

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 2.59-6
- 为 Magic 3.0 重建

* Sat Feb 11 2012 Pádraig Brady <P@draigBrady.com> - 2.59-5
- Compile DHCP lease management utils with RPM_OPT_FLAGS

* Thu Feb  9 2012 Pádraig Brady <P@draigBrady.com> - 2.59-4
- Include DHCP lease management utils in a subpackage

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.59-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Aug 26 2011 Douglas Schilling Landgraf <dougsland@redhat.com> - 2.59-2
- do not enable service by default

* Fri Aug 26 2011 Douglas Schilling Landgraf <dougsland@redhat.com> - 2.59-1
- New version 2.59
- Fix regression in 2.58 (IPv6 issue) - bz 744814

* Fri Aug 26 2011 Douglas Schilling Landgraf <dougsland@redhat.com> - 2.58-1
- Fixed License
- New version 2.58

* Mon Aug 08 2011 Patrick "Jima" Laughton <jima@fedoraproject.org> - 2.52-5
- Include systemd unit file

* Mon Aug 08 2011 Patrick "Jima" Laughton <jima@fedoraproject.org> - 2.52-3
- Applied Jóhann's patch, minor cleanup

* Thu Jul 26 2011 Jóhann B. Guðmundsson <johannbg@gmail.com> - 2.52-3
- Introduce systemd unit file, drop SysV support

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.52-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 26 2010 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 2.52-1
- New Version 2.52
- fix condrestart() in initscript bz 547605
- fix sed to enable DBUS(the '*' need some escaping) bz 553161

* Sun Nov 22 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 2.51-2
- fix bz 512664

* Sat Oct 17 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 2.51-1
- move initscript from patch to a plain text file
- drop (dnsmasq-configuration.patch) and use sed instead
- enable /etc/dnsmasq.d fix bz 526703
- change requires to package name instead of file
- new version 2.51

* Mon Oct  5 2009 Mark McLoughlin <markmc@redhat.com> - 2.48-4
- Fix multiple TFTP server vulnerabilities (CVE-2009-2957, CVE-2009-2958)

* Wed Aug 12 2009 Ville Skyttä <ville.skytta@iki.fi> - 2.48-3
- Use lzma compressed upstream tarball.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.48-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 10 2009 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.48-1
- Bugfix/feature enhancement update
- Fixing BZ#494094

* Fri May 29 2009 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.47-1
- Bugfix/feature enhancement update

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.46-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 29 2008 Matěj Cepl <mcepl@redhat.com> - 2.45-2
- rebuilt

* Mon Jul 21 2008 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.45-1
- Upstream release (bugfixes)

* Wed Jul 16 2008 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.43-2
- New upstream release, contains fixes for CVE-2008-1447/CERT VU#800113
- Dropped patch for newer glibc (merged upstream)

* Wed Feb 13 2008 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.41-0.8
- Added upstream-authored patch for newer glibc (thanks Simon!)

* Wed Feb 13 2008 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.41-0.7
- New upstream release

* Wed Jan 30 2008 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.41-0.6.rc1
- Release candidate
- Happy Birthday Isaac!

* Wed Jan 23 2008 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.41-0.5.test30
- Bugfix update

* Mon Dec 31 2007 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.41-0.4.test26
- Bugfix/feature enhancement update

* Thu Dec 13 2007 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.41-0.3.test24
- Upstream fix for fairly serious regression

* Tue Dec 04 2007 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.41-0.2.test20
- New upstream test release
- Moving dnsmasq.leases to /var/lib/dnsmasq/ as per BZ#407901
- Ignoring dangerous-command-in-%%post rpmlint warning (as per above fix)
- Patch consolidation/cleanup
- Removed conditionals for Fedora <= 3 and Aurora 2.0

* Tue Sep 18 2007 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.40-1
- Finalized upstream release
- Removing URLs from patch lines (CVS is the authoritative source)
- Added more magic to make spinning rc/test packages more seamless

* Sun Aug 26 2007 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.40-0.1.rc2
- New upstream release candidate (feature-frozen), thanks Simon!
- License clarification

* Tue May 29 2007 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.39-1
- New upstream version (bugfixes, enhancements)

* Mon Feb 12 2007 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.38-1
- New upstream version with bugfix for potential hang

* Tue Feb 06 2007 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.37-1
- New upstream version

* Wed Jan 24 2007 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.36-1
- New upstream version

* Mon Nov 06 2006 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.35-2
- Stop creating /etc/sysconfig on %%install
- Create /etc/dnsmasq.d on %%install

* Mon Nov 06 2006 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.35-1
- Update to 2.35
- Removed UPGRADING_to_2.0 from %%doc as per upstream change
- Enabled conf-dir in default config as per RFE BZ#214220 (thanks Chris!)
- Added %%dir /etc/dnsmasq.d to %%files as per above RFE

* Tue Oct 24 2006 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.34-2
- Fixed BZ#212005
- Moved %%postun scriptlet to %%post, where it made more sense
- Render scriptlets safer
- Minor cleanup for consistency

* Thu Oct 19 2006 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.34-1
- Hardcoded version in patches, as I'm getting tired of updating them
- Update to 2.34

* Mon Aug 28 2006 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.33-2
- Rebuild for FC6

* Tue Aug 15 2006 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.33-1
- Update

* Sat Jul 22 2006 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.32-3
- Added pkgconfig BuildReq due to reduced buildroot

* Thu Jul 20 2006 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.32-2
- Forced update due to dbus version bump

* Mon Jun 12 2006 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.32-1
- Update from upstream
- Patch from Dennis Gilmore fixed the conditionals to detect Aurora Linux

* Mon May  8 2006 Patrick "Jima" Laughton <jima@auroralinux.org> 2.31-1
- Removed dbus config patch (now provided upstream)
- Patched in init script (no longer provided upstream)
- Added DBus-interface to docs

* Tue May  2 2006 Patrick "Jima" Laughton <jima@auroralinux.org> 2.30-4.2
- More upstream-recommended cleanups :)
- Killed sysconfig file (provides unneeded functionality)
- Tweaked init script a little more

* Tue May  2 2006 Patrick "Jima" Laughton <jima@auroralinux.org> 2.30-4
- Moved options out of init script and into /etc/sysconfig/dnsmasq
- Disabled DHCP_LEASE in sysconfig file, fixing bug #190379
- Simon Kelley provided dbus/dnsmasq.conf, soon to be part of the tarball

* Thu Apr 27 2006 Patrick "Jima" Laughton <jima@auroralinux.org> 2.30-3
- Un-enabled HAVE_ISC_READER, a hack to enable a deprecated feature (request)
- Split initscript & enable-dbus patches, conditionalized dbus for FC3
- Tweaked name field in changelog entries (trying to be consistent)

* Mon Apr 24 2006 Patrick "Jima" Laughton <jima@auroralinux.org> 2.30-2
- Disabled stripping of binary while installing (oops)
- Enabled HAVE_ISC_READER/HAVE_DBUS via patch
- Added BuildReq for dbus-devel

* Mon Apr 24 2006 Patrick "Jima" Laughton <jima@auroralinux.org> 2.30-1
- Initial Fedora Extras RPM
