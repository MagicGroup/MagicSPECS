Name:		gssproxy
Version:	0.3.1
Release:	5%{?dist}
Summary:	GSSAPI Proxy
Summary(zh_CN.UTF-8): GSSAPI 代理

Group:		System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:	MIT
URL:		http://fedorahosted.org/gss-proxy
Source0:	http://fedorahosted.org/released/gss-proxy/%{name}-%{version}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

Patch0:		gssproxy-0.3.1-flags_handling.patch
Patch1:		gssproxy-0.3.1-nfsd_startup.patch
Patch2:		gssproxy-0.3.1-deadlock_fix.patch
Patch3:		gssproxy-0.3.1-gssi_inquire_context.patch
Patch4:		0001-Fix-error-in-compiling-without-SELinux.patch

%global servicename gssproxy
%global pubconfpath %{_sysconfdir}/gssproxy
%global gpstatedir %{_localstatedir}/lib/gssproxy

### Patches ###

### Dependencies ###

Requires: krb5-libs >= 1.11.3-25
Requires: keyutils-libs
Requires: libverto-tevent
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

### Build Dependencies ###

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool
BuildRequires: m4
BuildRequires: libxslt
BuildRequires: libxml2
BuildRequires: docbook-style-xsl
BuildRequires: doxygen
BuildRequires: gettext-devel
BuildRequires: pkgconfig
BuildRequires: krb5-devel >= 1.11.3-25
BuildRequires: keyutils-libs-devel
BuildRequires: libini_config-devel >= 1.0.0.1
BuildRequires: libverto-devel
BuildRequires: popt-devel
BuildRequires: findutils
BuildRequires: systemd-units


%description
A proxy for GSSAPI credential handling

%description -l zh_CN.UTF-8
GSSAPI 代理。

%prep
%setup -q

%patch0 -p2 -b .flags_handling
%patch1 -p2 -b .nfsd_startup
%patch2 -p2 -b .deadlock_fix
%patch3 -p2 -b .gssi_inquire_context
%patch4 -p2 -b .without_selinux

%build
autoreconf -f -i
%configure \
    --with-pubconf-path=%{pubconfpath} \
    --with-init-dir=%{_initrddir} \
    --disable-static \
    --disable-rpath \
    --without-selinux \
    --with-gpp-default-behavior=REMOTE_FIRST

make %{?_smp_mflags} all
#make test_proxymech

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
rm -f %{buildroot}%{_libdir}/gssproxy/proxymech.la
install -d -m755 %{buildroot}%{_sysconfdir}/gssproxy
install -d -m755 %{buildroot}%{_unitdir}
install -m644 examples/gssproxy.conf %{buildroot}%{_sysconfdir}/gssproxy/gssproxy.conf
install -m644 examples/mech %{buildroot}%{_sysconfdir}/gss/mech
install -m644 systemd/gssproxy.service %{buildroot}%{_unitdir}/gssproxy.service
magic_rpm_clean.sh

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc COPYING
%{_unitdir}/gssproxy.service
%{_sbindir}/gssproxy
%attr(755,root,root) %dir %{pubconfpath}
%attr(755,root,root) %dir %{gpstatedir}
%attr(700,root,root) %dir %{gpstatedir}/clients
%attr(0600,root,root) %config(noreplace) /%{_sysconfdir}/gssproxy/gssproxy.conf
%attr(0644,root,root) %config(noreplace) /%{_sysconfdir}/gss/mech
%{_libdir}/gssproxy/proxymech.so
%{_mandir}/man5/gssproxy.conf.5*
%{_mandir}/man8/gssproxy.8*
%{_mandir}/man8/gssproxy-mech.8*

%post
%systemd_post gssproxy.service

%preun
%systemd_preun gssproxy.service

%postun
%systemd_postun_with_restart gssproxy.service

%changelog
* Fri Feb 13 2015 Liu Di <liudidi@gmail.com> - 0.3.1-5
- 为 Magic 3.0 重建

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 29 2014 Simo Sorce <simo@redhat.com> 0.3.1-2
- Rebuild as new ding-libs brings in soname bump

* Thu Mar 13 2014 Guenther Deschner <gdeschner@redhat.com> 0.3.1-1
- Fix flags handling in gss_init_sec_context()
- resolves: https://fedorahosted.org/gss-proxy/ticket/112
- Fix nfsd startup
- resolves: https://fedorahosted.org/gss-proxy/ticket/114
- Fix potential mutex deadlock
- resolves: https://fedorahosted.org/gss-proxy/ticket/120
- Fix segfault in gssi_inquire_context
- resolves: https://fedorahosted.org/gss-proxy/ticket/117
- resolves: #1061133

* Tue Nov 26 2013 Guenther Deschner <gdeschner@redhat.com> 0.3.1-0
- New upstream release 0.3.1:
  * Fix use of gssproxy for client initiation
  * Add new enforcing and filtering options for context initialization
  * Fix potential thread safety issues
- resolves: https://fedorahosted.org/gss-proxy/ticket/110
- resolves: https://fedorahosted.org/gss-proxy/ticket/111

* Tue Nov 19 2013 Guenther Deschner <gdeschner@redhat.com> 0.3.0-3
- Fix flags handling in gss_init_sec_context()
- resolves: https://fedorahosted.org/gss-proxy/ticket/106
- Fix OID handling in gss_inquire_cred_by_mech()
- resolves: https://fedorahosted.org/gss-proxy/ticket/107
- Fix continuation processing for not yet fully established contexts.
- resolves: https://fedorahosted.org/gss-proxy/ticket/108
- Add flags filtering and flags enforcing.
- resolves: https://fedorahosted.org/gss-proxy/ticket/109

* Wed Oct 23 2013 Guenther Deschner <gdeschner@redhat.com> 0.3.0-0
- New upstream release 0.3.0:
  * Add support for impersonation (depends on s4u2self/s4u2proxy on the KDC)
  * Add support for new rpc.gssd mode of operation that forks and changes uid
  * Add 2 new options allow_any_uid and cred_usage

* Fri Oct 18 2013 Guenther Deschner <gdeschner@redhat.com> 0.2.3-8
- Fix default proxymech documentation and fix LOCAL_FIRST implementation
- resolves: https://fedorahosted.org/gss-proxy/ticket/105

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 24 2013 Guenther Deschner <gdeschner@redhat.com> 0.2.3-6
- Add better default gssproxy.conf file for nfs client and server usage

* Thu Jun 06 2013 Guenther Deschner <gdeschner@redhat.com> 0.2.3-5
- New upstream release

* Fri May 31 2013 Guenther Deschner <gdeschner@redhat.com> 0.2.2-5
- Require libverto-tevent to make sure libverto initialization succeeds

* Wed May 29 2013 Guenther Deschner <gdeschner@redhat.com> 0.2.2-4
- Modify systemd unit files for nfs-secure services

* Wed May 22 2013 Guenther Deschner <gdeschner@redhat.com> 0.2.2-3
- Fix cred_store handling w/o client keytab

* Thu May 16 2013 Guenther Deschner <gdeschner@redhat.com> 0.2.2-2
- New upstream release

* Tue May 07 2013 Guenther Deschner <gdeschner@redhat.com> 0.2.1-2
- New upstream release

* Wed Apr 24 2013 Guenther Deschner <gdeschner@redhat.com> 0.2.0-1
- New upstream release

* Mon Apr 01 2013 Simo Sorce <simo@redhat.com> - 0.1.0-0
- New upstream release

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 06 2012 Guenther Deschner <gdeschner@redhat.com> 0.0.3-7
- Update to 0.0.3

* Wed Aug 22 2012 Guenther Deschner <gdeschner@redhat.com> 0.0.2-6
- Use new systemd-rpm macros
- resolves: #850139

* Wed Jul 18 2012 Guenther Deschner <gdeschner@redhat.com> 0.0.2-5
- More spec file fixes

* Mon Jul 16 2012 Guenther Deschner <gdeschner@redhat.com> 0.0.2-4
- Fix systemd service file

* Fri Jul 13 2012 Guenther Deschner <gdeschner@redhat.com> 0.0.2-3
- Fix various packaging issues

* Mon Jul 02 2012 Guenther Deschner <gdeschner@redhat.com> 0.0.1-2
- Add systemd packaging

* Wed Mar 28 2012 Guenther Deschner <gdeschner@redhat.com> 0.0.1-1
- Various fixes

* Mon Dec 12 2011 Simo Sorce <simo@redhat.com> - 0.0.2-0
- Automated build of the gssproxy daemon
