%global USE_FIPSCHECK true
%global USE_LIBCAP_NG true
%global USE_LABELED_IPSEC false
%global USE_CRL_FETCHING true
%global USE_DNSSEC true
%global USE_NM true
%global USE_LINUX_AUDIT 0

%global _hardened_build 1

%global fipscheck_version 1.3.0
%global buildefence 0
%global development 0

#global prever rc1

Name: libreswan
Summary: IPsec implementation with IKEv1 and IKEv2 keying protocols
Summary(zh_CN.UTF-8): 带有 IKEv1 和 IKEv2 协议的 IPsec 实现
Version: 3.9
Release: 1%{?dist}
License: GPLv2
Url: https://www.libreswan.org/
Source: https://download.libreswan.org/%{name}-%{version}%{?prever}.tar.gz
Group: System Environment/Daemons
Group(zh_CN.UTF-8): 系统环境/服务
BuildRequires: gmp-devel bison flex pkgconfig
BuildRequires: systemd
Requires(post): coreutils bash systemd
Requires(preun): systemd
Requires(postun): systemd

Conflicts: openswan < %{version}-%{release}
Obsoletes: openswan < %{version}-%{release}
Provides: openswan = %{version}-%{release}
Provides: openswan-doc = %{version}-%{release}

BuildRequires: pkgconfig hostname
BuildRequires: nss-devel >= 3.14.3, nspr-devel
BuildRequires: pam-devel
%if %{USE_DNSSEC}
BuildRequires: unbound-devel
%endif
%if %{USE_FIPSCHECK}
BuildRequires: fipscheck-devel >= %{fipscheck_version}
Requires: fipscheck%{_isa} >= %{fipscheck_version}
%endif
%if %{USE_LINUX_AUDIT}
Buildrequires: audit-libs-devel
%endif

%if %{USE_LIBCAP_NG}
BuildRequires: libcap-ng-devel
%endif
%if %{USE_CRL_FETCHING}
BuildRequires: openldap-devel curl-devel
%endif
%if %{buildefence}
BuildRequires: ElectricFence
%endif
# Only needed if xml man pages are modified and need regeneration
# BuildRequires: xmlto

Requires: nss-tools, nss-softokn
Requires: iproute >= 2.6.8

%description
Libreswan is a free implementation of IPsec & IKE for Linux.  IPsec is
the Internet Protocol Security and uses strong cryptography to provide
both authentication and encryption services.  These services allow you
to build secure tunnels through untrusted networks.  Everything passing
through the untrusted net is encrypted by the ipsec gateway machine and
decrypted by the gateway at the other end of the tunnel.  The resulting
tunnel is a virtual private network or VPN.

This package contains the daemons and userland tools for setting up
Libreswan. To build KLIPS, see the kmod-libreswan.spec file.

Libreswan also supports IKEv2 (RFC4309) and Secure Labeling

Libreswan is based on Openswan-2.6.38 which in turn is based on FreeS/WAN-2.04

%description -l zh_CN.UTF-8
带有 IKEv1 和 IKEv2 协议的 IPsec 实现。

%prep
%setup -q -n libreswan-%{version}%{?prever}

%build
%if %{buildefence}
 %define efence "-lefence"
%endif

#796683: -fno-strict-aliasing
%{__make} \
%if %{development}
   USERCOMPILE="-g -DGCC_LINT %(echo %{optflags} | sed -e s/-O[0-9]*/ /) %{?efence} -fPIE -pie -fno-strict-aliasing -Wformat-nonliteral -Wformat-security" \
%else
  USERCOMPILE="-g -DGCC_LINT %{optflags} %{?efence} -fPIE -pie -fno-strict-aliasing -Wformat-nonliteral -Wformat-security" \
%endif
  USERLINK="-g -pie -Wl,-z,relro,-z,now %{?efence}" \
  INITSYSTEM=systemd \
  USE_NM=%{USE_NM} \
  USE_XAUTHPAM=true \
%if %{USE_FIPSCHECK}
  USE_FIPSCHECK="%{USE_FIPSCHECK}" \
  FIPSPRODUCTCHECK=%{_sysconfdir}/system-fips \
%endif
  USE_LIBCAP_NG="%{USE_LIBCAP_NG}" \
  USE_LABELED_IPSEC="%{USE_LABELED_IPSEC}" \
%if %{USE_CRL_FETCHING}
  USE_LDAP=true \
  USE_LIBCURL=true \
%endif
  USE_LINUX_AUDIT=false \
  USE_DNSSEC="%{USE_DNSSEC}" \
  INC_USRLOCAL=%{_prefix} \
  FINALLIBDIR=%{_libexecdir}/ipsec \
  FINALLIBEXECDIR=%{_libexecdir}/ipsec \
  MANTREE=%{_mandir} \
  INC_RCDEFAULT=%{_initrddir} \
  programs
FS=$(pwd)

%if %{USE_FIPSCHECK}
# Add generation of HMAC checksums of the final stripped binaries
%define __spec_install_post \
    %{?__debug_package:%{__debug_install_post}} \
    %{__arch_install_post} \
    %{__os_install_post} \
  fipshmac -d %{buildroot}%{_libdir}/fipscheck %{buildroot}%{_libexecdir}/ipsec/* \
  fipshmac -d %{buildroot}%{_libdir}/fipscheck %{buildroot}%{_sbindir}/ipsec \
%{nil}
%endif

%install
rm -rf %{buildroot}
%{__make} \
  DESTDIR=%{buildroot} \
  INC_USRLOCAL=%{_prefix} \
  FINALLIBDIR=%{_libexecdir}/ipsec \
  FINALLIBEXECDIR=%{_libexecdir}/ipsec \
  MANTREE=%{buildroot}%{_mandir} \
  INC_RCDEFAULT=%{_initrddir} \
  INSTMANFLAGS="-m 644" \
  INITSYSTEM=systemd \
  install
FS=$(pwd)
rm -rf %{buildroot}/usr/share/doc/libreswan

install -d -m 0755 %{buildroot}%{_localstatedir}/run/pluto
# used when setting --perpeerlog without --perpeerlogbase 
install -d -m 0700 %{buildroot}%{_localstatedir}/log/pluto/peer
install -d %{buildroot}%{_sbindir}

%if %{USE_FIPSCHECK}
mkdir -p %{buildroot}%{_libdir}/fipscheck
install -d %{buildroot}%{_sysconfdir}/prelink.conf.d/
install -m644 packaging/fedora/libreswan-prelink.conf %{buildroot}%{_sysconfdir}/prelink.conf.d/libreswan-fips.conf
%endif

echo "include %{_sysconfdir}/ipsec.d/*.secrets" > %{buildroot}%{_sysconfdir}/ipsec.secrets
rm -fr %{buildroot}%{_sysconfdir}/rc.d/rc*

%files
%doc CHANGES COPYING CREDITS README LICENSE
%doc docs/*.*
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/ipsec.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/pluto
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/ipsec.secrets
%attr(0700,root,root) %dir %{_sysconfdir}/ipsec.d
%attr(0700,root,root) %dir %{_sysconfdir}/ipsec.d/cacerts
%attr(0700,root,root) %dir %{_sysconfdir}/ipsec.d/crls
%attr(0700,root,root) %dir %{_sysconfdir}/ipsec.d/policies
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/ipsec.d/policies/*
%attr(0700,root,root) %dir %{_localstatedir}/log/pluto/peer
%attr(0755,root,root) %dir %{_localstatedir}/run/pluto
%attr(0644,root,root) %{_unitdir}/ipsec.service
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/pam.d/pluto
%{_sbindir}/ipsec
%{_libexecdir}/ipsec
%attr(0644,root,root) %doc %{_mandir}/*/*

%if %{USE_FIPSCHECK}
%{_libdir}/fipscheck/*.hmac
# We own the directory so we don't have to require prelink
%attr(0755,root,root) %dir %{_sysconfdir}/prelink.conf.d/
%{_sysconfdir}/prelink.conf.d/libreswan-fips.conf
%endif

%preun
%systemd_preun ipsec.service

%postun
%systemd_postun_with_restart ipsec.service

%post
%systemd_post ipsec.service
if [ ! -f %{_sysconfdir}/ipsec.d/cert8.db ] ; then
    TEMPFILE=$(/bin/mktemp %{_sysconfdir}/ipsec.d/nsspw.XXXXXXX)
    [ $? -gt 0 ] && TEMPFILE=%{_sysconfdir}/ipsec.d/nsspw.$$
    echo > ${TEMPFILE}
    certutil -N -f ${TEMPFILE} -d %{_sysconfdir}/ipsec.d
    restorecon %{_sysconfdir}/ipsec.d/*db 2>/dev/null || :
    rm -f ${TEMPFILE}
fi

%changelog
* Wed Jul 30 2014 Liu Di <liudidi@gmail.com> - 3.9-1
- 更新到 3.9

* Sat Jan 18 2014 Paul Wouters <pwouters@redhat.com> - 3.8-1
- Updated to 3.8, fixes rhbz#CVE-2013-6467 (rhbz#1054102)

* Wed Dec 11 2013 Paul Wouters <pwouters@redhat.com> - 3.7-1
- Updated to 3.7, fixes CVE-2013-4564
- Fixes creating a bogus NSS db on startup (rhbz#1005410)

* Thu Oct 31 2013 Paul Wouters <pwouters@redhat.com> - 3.6-1
- Updated to 3.6 (IKEv2, MODECFG, Cisco interop fixes)
- Generate empty NSS db if none exists

* Mon Aug 19 2013 Paul Wouters <pwouters@redhat.com> - 3.5-3
- Add a Provides: for openswan-doc

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 15 2013 Paul Wouters <pwouters@redhat.com> - 3.5-2
- Added interop patch for (some?) Cisco VPN clients sending 16 zero
  bytes of extraneous IKE data
- Removed fipscheck_version

* Sat Jul 13 2013 Paul Wouters <pwouters@redhat.com> - 3.5-1
- Updated to 3.5

* Thu Jun 06 2013 Paul Wouters <pwouters@redhat.com> - 3.4-1
- Updated to 3.4, which only contains style changes to kernel coding style
- IN MEMORIAM: June 3rd, 2013 Hugh Daniel

* Mon May 13 2013 Paul Wouters <pwouters@redhat.com> - 3.3-1
- Updated to 3.3, which resolves CVE-2013-2052

* Sat Apr 13 2013 Paul Wouters <pwouters@redhat.com> - 3.2-1
- Initial package for Fedora
