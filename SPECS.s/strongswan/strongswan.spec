%global hardened_build 1

%if 0%{?fedora} >= 15 || 0%{?rhel} >= 7
%global enable_nm 1
%global _enable_nm '--enable-nm'
%else
%global enable_nm 0
%endif

Name:           strongswan
Version:        5.1.1
Release:        4%{?dist}
Summary:        An OpenSource IPsec-based VPN Solution
Group:          System Environment/Daemons
License:        GPLv2+
URL:            http://www.strongswan.org/
Source0:        http://download.strongswan.org/%{name}-%{version}.tar.bz2
Patch0:         strongswan-init.patch
Patch1:         strongswan-pts-ecp-disable.patch
Patch2:         libstrongswan-plugin.patch
Patch3:         libstrongswan-settings-debug.patch
Patch4:         libstrongswan-973315.patch
Patch5:         strongswan-1036844.patch

BuildRequires:  gmp-devel autoconf automake
BuildRequires:  libcurl-devel
BuildRequires:  openldap-devel
BuildRequires:  openssl-devel
BuildRequires:  sqlite-devel
BuildRequires:  gettext-devel
BuildRequires:  trousers-devel
BuildRequires:  libxml2-devel
%if 0%{?enable_nm}
BuildRequires:  NetworkManager-devel
BuildRequires:  NetworkManager-glib-devel
Obsoletes:      %{name}-NetworkManager < 0:5.0.4-5
Provides:       %{name}-charon-nm = 0:%{version}-%{release}
%else
Obsoletes:      %{name}-NetworkManager < 0:5.0.0-3.git20120619
%endif

%if 0%{?fedora} >= 15 || 0%{?rhel} >= 7
BuildRequires:  systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
%else
Requires(post): chkconfig
Requires(preun): chkconfig
Requires(preun): initscripts
%endif
%description
The strongSwan IPsec implementation supports both the IKEv1 and IKEv2 key
exchange protocols in conjunction with the native NETKEY IPsec stack of the
Linux kernel.

%if 0%{?enable_nm}
%package charon-nm
Summary:        NetworkManager plugin for Strongswan
Group:          System Environment/Daemons
%description charon-nm
NetworkManager plugin integrates a subset of Strongswan capabilities
to NetworkManager.
%endif

%package tnc-imcvs
Summary: Trusted network connect (TNC)'s IMC/IMV functionality
Group: Applications/System
Requires: %{name} = %{version}
%description tnc-imcvs
This package provides Trusted Network Connect's (TNC) IMC and IMV
functionality. Specifically it includes PTS based IMC/IMV for TPM based
remote attestation and scanner and test IMCs and IMVs. The Strongswan's
IMC/IMV dynamic libraries can be used by any third party TNC Client/Server
implementation possessing a standard IF-IMC/IMV interface.


%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

echo "For migration from 4.6 to 5.0 see http://wiki.strongswan.org/projects/strongswan/wiki/CharonPlutoIKEv1" > README.Fedora

%build
# for initscript patch to work
autoreconf
%configure --disable-static \
    --with-ipsec-script=%{name} \
    --sysconfdir=%{_sysconfdir}/%{name} \
    --with-ipsecdir=%{_libexecdir}/%{name} \
    --with-ipseclibdir=%{_libdir}/%{name} \
    --with-fips-mode=2 \
    --with-tss=trousers \
    --enable-openssl \
    --enable-md4 \
    --enable-xauth-eap \
    --enable-eap-md5 \
    --enable-eap-gtc \
    --enable-eap-tls \
    --enable-eap-ttls \
    --enable-eap-peap \
    --enable-eap-mschapv2 \
    --enable-farp \
    --enable-dhcp \
    --enable-sqlite \
    --enable-tnc-ifmap \
    --enable-tnc-pdp \
    --enable-imc-test \
    --enable-imv-test \
    --enable-imc-scanner \
    --enable-imv-scanner  \
    --enable-imc-attestation \
    --enable-imv-attestation \
    --enable-imv-os \
    --enable-imc-os \
    --enable-imc-swid \
    --enable-imv-swid \
    --enable-eap-tnc \
    --enable-tnccs-20 \
    --enable-tnccs-11 \
    --enable-tnccs-dynamic \
    --enable-tnc-imc \
    --enable-tnc-imv \
    --enable-eap-radius \
    --enable-curl \
    --enable-eap-identity \
    --enable-cmd \
    %{?_enable_nm}


make %{?_smp_mflags}
sed -i 's/\t/    /' src/strongswan.conf src/starter/ipsec.conf

%install
make install DESTDIR=%{buildroot}
# prefix man pages
for i in %{buildroot}%{_mandir}/*/*; do
    if echo "$i" | grep -vq '/%{name}[^\/]*$'; then
        mv "$i" "`echo "$i" | sed -re 's|/([^/]+)$|/%{name}_\1|'`"
    fi
done
# delete unwanted library files
rm %{buildroot}%{_libdir}/%{name}/*.so
find %{buildroot} -type f -name '*.la' -delete
# fix config permissions
chmod 644 %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf
# protect configuration from ordinary user's eyes
chmod 700 %{buildroot}%{_sysconfdir}/%{name}
# setup systemd unit or initscript
%if 0%{?fedora} >= 15 || 0%{?rhel} >= 7
%else
install -D -m 755 init/sysvinit/%{name} %{buildroot}/%{_initddir}/%{name}
%endif
#rename /usr/bin/pki to avoid conflict with pki-core/pki-tools
mv %{buildroot}%{_bindir}/pki %{buildroot}%{_bindir}/%{name}-pki

# Create ipsec.d directory tree.
install -d -m 700 %{buildroot}%{_sysconfdir}/%{name}/ipsec.d
for i in aacerts acerts certs cacerts crls ocspcerts private reqs; do
    install -d -m 700 %{buildroot}%{_sysconfdir}/%{name}/ipsec.d/${i}
done


%post
/sbin/ldconfig
%if 0%{?fedora} >= 15 || 0%{?rhel} >= 7
%systemd_post %{name}.service
%else
/sbin/chkconfig --add %{name}
%endif

%preun
%if 0%{?fedora} >= 15 || 0%{?rhel} >= 7
%systemd_preun %{name}.service
%else
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /sbin/service %{name} stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}
fi
%endif

%postun
/sbin/ldconfig
%if 0%{?fedora} >= 15 || 0%{?rhel} >= 7
%systemd_postun_with_restart %{name}.service
%else
%endif


%files
%doc README README.Fedora COPYING NEWS TODO
%dir %{_sysconfdir}/%{name}
%{_sysconfdir}/%{name}/ipsec.d/
%config(noreplace) %{_sysconfdir}/%{name}/ipsec.conf
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%if 0%{?fedora} >= 15 || 0%{?rhel} >= 7
%{_unitdir}/%{name}.service
%else
%{_initddir}/%{name}
%endif
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/libcharon.so.0
%{_libdir}/%{name}/libcharon.so.0.0.0
%{_libdir}/%{name}/libhydra.so.0
%{_libdir}/%{name}/libhydra.so.0.0.0
%{_libdir}/%{name}/libtls.so.0
%{_libdir}/%{name}/libtls.so.0.0.0
%{_libdir}/%{name}/libpttls.so.0
%{_libdir}/%{name}/libpttls.so.0.0.0
%{_libdir}/%{name}/lib%{name}.so.0
%{_libdir}/%{name}/lib%{name}.so.0.0.0
%dir %{_libdir}/%{name}/plugins
%{_libdir}/%{name}/plugins/lib%{name}-aes.so
%{_libdir}/%{name}/plugins/lib%{name}-attr.so
%{_libdir}/%{name}/plugins/lib%{name}-cmac.so
%{_libdir}/%{name}/plugins/lib%{name}-constraints.so
%{_libdir}/%{name}/plugins/lib%{name}-des.so
%{_libdir}/%{name}/plugins/lib%{name}-dnskey.so
%{_libdir}/%{name}/plugins/lib%{name}-fips-prf.so
%{_libdir}/%{name}/plugins/lib%{name}-gmp.so
%{_libdir}/%{name}/plugins/lib%{name}-hmac.so
%{_libdir}/%{name}/plugins/lib%{name}-kernel-netlink.so
%{_libdir}/%{name}/plugins/lib%{name}-md5.so
%{_libdir}/%{name}/plugins/lib%{name}-nonce.so
%{_libdir}/%{name}/plugins/lib%{name}-openssl.so
%{_libdir}/%{name}/plugins/lib%{name}-pem.so
%{_libdir}/%{name}/plugins/lib%{name}-pgp.so
%{_libdir}/%{name}/plugins/lib%{name}-pkcs1.so
%{_libdir}/%{name}/plugins/lib%{name}-pkcs8.so
%{_libdir}/%{name}/plugins/lib%{name}-pkcs12.so
%{_libdir}/%{name}/plugins/lib%{name}-rc2.so
%{_libdir}/%{name}/plugins/lib%{name}-sshkey.so
%{_libdir}/%{name}/plugins/lib%{name}-pubkey.so
%{_libdir}/%{name}/plugins/lib%{name}-random.so
%{_libdir}/%{name}/plugins/lib%{name}-resolve.so
%{_libdir}/%{name}/plugins/lib%{name}-revocation.so
%{_libdir}/%{name}/plugins/lib%{name}-sha1.so
%{_libdir}/%{name}/plugins/lib%{name}-sha2.so
%{_libdir}/%{name}/plugins/lib%{name}-socket-default.so
%{_libdir}/%{name}/plugins/lib%{name}-stroke.so
%{_libdir}/%{name}/plugins/lib%{name}-updown.so
%{_libdir}/%{name}/plugins/lib%{name}-x509.so
%{_libdir}/%{name}/plugins/lib%{name}-xauth-generic.so
%{_libdir}/%{name}/plugins/lib%{name}-xauth-eap.so
%{_libdir}/%{name}/plugins/lib%{name}-xcbc.so
%{_libdir}/%{name}/plugins/lib%{name}-md4.so
%{_libdir}/%{name}/plugins/lib%{name}-eap-md5.so
%{_libdir}/%{name}/plugins/lib%{name}-eap-gtc.so
%{_libdir}/%{name}/plugins/lib%{name}-eap-tls.so
%{_libdir}/%{name}/plugins/lib%{name}-eap-ttls.so
%{_libdir}/%{name}/plugins/lib%{name}-eap-peap.so
%{_libdir}/%{name}/plugins/lib%{name}-eap-mschapv2.so
%{_libdir}/%{name}/plugins/lib%{name}-farp.so
%{_libdir}/%{name}/plugins/lib%{name}-dhcp.so
%{_libdir}/%{name}/plugins/lib%{name}-curl.so
%{_libdir}/%{name}/plugins/lib%{name}-eap-identity.so
%dir %{_libexecdir}/%{name}
%{_libexecdir}/%{name}/_copyright
%{_libexecdir}/%{name}/_updown
%{_libexecdir}/%{name}/_updown_espmark
%{_libexecdir}/%{name}/charon
%{_libexecdir}/%{name}/openac
%{_libexecdir}/%{name}/scepclient
%{_libexecdir}/%{name}/starter
%{_libexecdir}/%{name}/stroke
%{_libexecdir}/%{name}/_imv_policy
%{_libexecdir}/%{name}/imv_policy_manager
%{_bindir}/%{name}-pki
%{_sbindir}/charon-cmd
%{_sbindir}/%{name}
%{_mandir}/man1/%{name}_pki*.1.gz
%{_mandir}/man5/%{name}.conf.5.gz
%{_mandir}/man5/%{name}_ipsec.conf.5.gz
%{_mandir}/man5/%{name}_ipsec.secrets.5.gz
%{_mandir}/man8/%{name}.8.gz
%{_mandir}/man8/%{name}__updown.8.gz
%{_mandir}/man8/%{name}__updown_espmark.8.gz
%{_mandir}/man8/%{name}_openac.8.gz
%{_mandir}/man8/%{name}_scepclient.8.gz
%{_mandir}/man8/%{name}_charon-cmd.8.gz

%files tnc-imcvs
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/libimcv.so.0
%{_libdir}/%{name}/libimcv.so.0.0.0
%{_libdir}/%{name}/libpts.so.0
%{_libdir}/%{name}/libpts.so.0.0.0
%{_libdir}/%{name}/libtnccs.so.0
%{_libdir}/%{name}/libtnccs.so.0.0.0
%{_libdir}/%{name}/libradius.so.0
%{_libdir}/%{name}/libradius.so.0.0.0
%dir %{_libdir}/%{name}/imcvs
%{_libdir}/%{name}/imcvs/imc-attestation.so
%{_libdir}/%{name}/imcvs/imc-scanner.so
%{_libdir}/%{name}/imcvs/imc-test.so
%{_libdir}/%{name}/imcvs/imc-os.so
%{_libdir}/%{name}/imcvs/imc-swid.so
%{_libdir}/%{name}/imcvs/imv-attestation.so
%{_libdir}/%{name}/imcvs/imv-scanner.so
%{_libdir}/%{name}/imcvs/imv-test.so
%{_libdir}/%{name}/imcvs/imv-os.so
%{_libdir}/%{name}/imcvs/imv-swid.so
%dir %{_libdir}/%{name}/plugins
%{_libdir}/%{name}/plugins/lib%{name}-pkcs7.so
%{_libdir}/%{name}/plugins/lib%{name}-sqlite.so
%{_libdir}/%{name}/plugins/lib%{name}-eap-tnc.so
%{_libdir}/%{name}/plugins/lib%{name}-tnc-imc.so
%{_libdir}/%{name}/plugins/lib%{name}-tnc-imv.so
%{_libdir}/%{name}/plugins/lib%{name}-tnc-tnccs.so
%{_libdir}/%{name}/plugins/lib%{name}-tnccs-20.so
%{_libdir}/%{name}/plugins/lib%{name}-tnccs-11.so
%{_libdir}/%{name}/plugins/lib%{name}-tnccs-dynamic.so
%{_libdir}/%{name}/plugins/lib%{name}-eap-radius.so
%{_libdir}/%{name}/plugins/lib%{name}-tnc-ifmap.so
%{_libdir}/%{name}/plugins/lib%{name}-tnc-pdp.so
%dir %{_libexecdir}/%{name}
%{_libexecdir}/%{name}/attest
%{_libexecdir}/%{name}/pacman
%{_libexecdir}/%{name}/pt-tls-client
#swid files
%{_libexecdir}/%{name}/*.swidtag
%dir %{_datadir}/regid.2004-03.org.%{name}
%{_datadir}/regid.2004-03.org.%{name}/*.swidtag

%if 0%{?enable_nm}
%files charon-nm
%doc COPYING
%{_libexecdir}/%{name}/charon-nm
%endif


%changelog
* Thu Jan 09 2014 Pavel Šimerda <psimerda@redhat.com> - 5.1.1-4
- Removed redundant patches and *.spec commands caused by branch merging

* Wed Jan 08 2014 Pavel Šimerda <psimerda@redhat.com> - 5.1.1-3
- rebuilt

* Mon Dec 2 2013 Avesh Agarwal <avagarwa@redhat.com> - 5.1.1-2
- Resolves: 973315
- Resolves: 1036844

* Fri Nov 1 2013 Avesh Agarwal <avagarwa@redhat.com> - 5.1.1-1
- Support for PT-TLS  (RFC 6876)
- Support for SWID IMC/IMV
- Support for command line IKE client charon-cmd
- Changed location of pki to /usr/bin
- Added swid tags files
- Added man pages for pki and charon-cmd
- Renamed pki to strongswan-pki to avoid conflict with
  pki-core/pki-tools package.
- Update local patches
- Fixes CVE-2013-6075
- Fixes CVE-2013-6076
- Fixed autoconf/automake issue as configure.ac got changed
  and it required running autoreconf during the build process.
- added strongswan signature file to the sources.

* Thu Sep 12 2013 Avesh Agarwal <avagarwa@redhat.com> - 5.1.0-3
- Fixed initialization crash of IMV and IMC particularly
  attestation imv/imc as libstrongswas was not getting
  initialized.

* Fri Aug 30 2013 Avesh Agarwal <avagarwa@redhat.com> - 5.1.0-2
- Enabled fips support
- Enabled TNC's ifmap support
- Enabled TNC's pdp support
- Fixed hardocded package name in this spec file

* Wed Aug 7 2013 Avesh Agarwal <avagarwa@redhat.com> - 5.1.0-1
- rhbz#981429: New upstream release
- Fixes CVE-2013-5018: rhbz#991216, rhbz#991215
- Fixes rhbz#991859 failed to build in rawhide
- Updated local patches and removed which are not needed
- Fixed errors around charon-nm
- Added plugins libstrongswan-pkcs12.so, libstrongswan-rc2.so,
  libstrongswan-sshkey.so
- Added utility imv_policy_manager

* Thu Jul 25 2013 Jamie Nguyen <jamielinux@fedoraproject.org> - 5.0.4-5
- rename strongswan-NetworkManager to strongswan-charon-nm
- fix enable_nm macro

* Mon Jul 15 2013 Jamie Nguyen <jamielinux@fedoraproject.org> - 5.0.4-4
- %%files tries to package some of the shared objects as directories (#984437)
- fix broken systemd unit file (#984300)
- fix rpmlint error: description-line-too-long
- fix rpmlint error: macro-in-comment
- fix rpmlint error: spelling-error Summary(en_US) fuctionality
- depend on 'systemd' instead of 'systemd-units'
- use new systemd scriptlet macros
- NetworkManager subpackage should have a copy of the license (#984490)
- enable hardened_build as this package meets the PIE criteria (#984429)
- invocation of "ipsec _updown iptables" is broken as ipsec is renamed
  to strongswan in this package (#948306)
- invocation of "ipsec scepclient" is broken as ipsec is renamed
  to strongswan in this package
- add /etc/strongswan/ipsec.d and missing subdirectories
- conditionalize building of strongswan-NetworkManager subpackage as the
  version of NetworkManager in EL6 is too old (#984497)

* Fri Jun 28 2013 Avesh Agarwal <avagarwa@redhat.com> - 5.0.4-3
- Patch to fix a major crash issue when Freeradius loads
  attestatiom-imv and does not initialize libstrongswan which
  causes crash due to calls to PTS algorithms probing APIs.
  So this patch fixes the order of initialization. This issues
  does not occur with charon because libstrongswan gets
  initialized earlier.
- Patch that allows to outputs errors when there are permission
  issues when accessing strongswan.conf.
- Patch to make loading of modules configurable when libimcv
  is used in stand alone mode without charon with freeradius
  and wpa_supplicant.

* Tue Jun 11 2013 Avesh Agarwal <avagarwa@redhat.com> - 5.0.4-2
- Enabled TNCCS 1.1 protocol
- Fixed libxm2-devel build dependency
- Patch to fix the issue with loading of plugins

* Wed May 1 2013 Avesh Agarwal <avagarwa@redhat.com> - 5.0.4-1
- New upstream release
- Fixes for CVE-2013-2944
- Enabled support for OS IMV/IMC
- Created and applied a patch to disable ECP in fedora, because
  Openssl in Fedora does not allow ECP_256 and ECP_384. It makes
  it non-compliant to TCG's PTS standard, but there is no choice
  right now. see redhat bz # 319901.
- Enabled Trousers support for TPM based operations.

* Sat Apr 20 2013 Pavel Šimerda <psimerda@redhat.com> - 5.0.3-2
- Rebuilt for a single specfile for rawhide/f19/f18/el6

* Fri Apr 19 2013 Avesh Agarwal <avagarwa@redhat.com> - 5.0.3-1
- New upstream release
- Enabled curl and eap-identity plugins
- Enabled support for eap-radius plugin.

* Thu Apr 18 2013 Pavel Šimerda <psimerda@redhat.com> - 5.0.2-3
- Add gettext-devel to BuildRequires because of epel6
- Remove unnecessary comments

* Tue Mar 19 2013 Avesh Agarwal <avagarwa@redhat.com> - 5.0.2-2
- Enabled support for eap-radius plugin.

* Mon Mar 11 2013 Avesh Agarwal <avagarwa@redhat.com> - 5.0.2-1
- Update to upstream release 5.0.2
- Created sub package strongswan-tnc-imcvs that provides trusted network
  connect's IMC and IMV funtionality. Specifically it includes PTS 
  based IMC/IMV for TPM based remote attestation and scanner and test 
  IMCs and IMVs. The Strongswan's IMC/IMV dynamic libraries can be used 
  by any third party TNC Client/Server implementation possessing a 
  standard IF-IMC/IMV interface.

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Oct 04 2012 Pavel Šimerda <psimerda@redhat.com> - 5.0.1-1
- Update to release 5.0.1

* Thu Oct 04 2012 Pavel Šimerda <psimerda@redhat.com> - 5.0.0-4.git20120619
- Add plugins to interoperate with Windows 7 and Android (#862472)
  (contributed by Haim Gelfenbeyn)

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0.0-3.git20120619
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jul 08 2012 Pavel Šimerda <pavlix@pavlix.net> - 5.0.0-2.git20120619
- Fix configure substitutions in initscripts

* Wed Jul 04 2012 Pavel Šimerda <psimerda@redhat.com> - 5.0.0-1.git20120619
- Update to current upstream release
- Comment out all stuff that is only needed for git builds
- Remove renaming patch from git
- Improve init patch used for EPEL

* Thu Jun 21 2012 Pavel Šimerda <psimerda@redhat.com> - 5.0.0-0.3.git20120619
- Build with openssl plugin enabled

* Wed Jun 20 2012 Pavel Šimerda <psimerda@redhat.com> - 5.0.0-0.2.git20120619
- Add README.Fedora with link to 4.6 to 5.0 migration information

* Tue Jun 19 2012 Pavel Šimerda - 5.0.0-0.1.git20120619
- Snapshot of upcoming major release
- Move patches and renaming upstream
  http://wiki.strongswan.org/issues/194
  http://wiki.strongswan.org/issues/195
- Notified upstream about manpage issues

* Tue Jun 19 2012 Pavel Šimerda - 4.6.4-2
- Make initscript patch more distro-neutral
- Add links to bugreports for patches

* Fri Jun 01 2012 Pavel Šimerda <pavlix@pavlix.net> - 4.6.4-1
- New upstream version (CVE-2012-2388)

* Sat May 26 2012 Pavel Šimerda <pavlix@pavlix.net> - 4.6.3-2
- Add --enable-nm to configure
- Add NetworkManager-devel to BuildRequires
- Add NetworkManager-glib-devel to BuildRequires
- Add strongswan-NetworkManager package

* Sat May 26 2012 Pavel Šimerda <pavlix@pavlix.net> - 4.6.3-1
- New version of Strongswan
- Support for RFC 3110 DNSKEY (see upstream changelog)
- Fix corrupt scriptlets

* Fri Mar 30 2012 Pavel Šimerda <pavlix@pavlix.net> - 4.6.2-2
- #808612 - strongswan binary renaming side-effect

* Sun Feb 26 2012 Pavel Šimerda <pavlix@pavlix.net> - 4.6.2-1
- New upstream version
- Changed from .tar.gz to .tar.bz2
- Added libstrongswan-pkcs8.so

* Wed Feb 15 2012 Pavel Šimerda <pavlix@pavlix.net> - 4.6.1-8
- Fix initscript's status function

* Wed Feb 15 2012 Pavel Šimerda <pavlix@pavlix.net> - 4.6.1-7
- Expand tabs in config files for better readability
- Add sysvinit script for epel6

* Wed Feb 15 2012 Pavel Šimerda <pavlix@pavlix.net> - 4.6.1-6
- Fix program name in systemd unit file

* Tue Feb 14 2012 Pavel Šimerda <pavlix@pavlix.net> - 4.6.1-5
- Improve fedora/epel conditionals

* Sat Jan 21 2012 Pavel Šimerda <pavlix@pavlix.net> - 4.6.1-4
- Protect configuration directory from ordinary users
- Add still missing directory /etc/strongswan

* Fri Jan 20 2012 Pavel Šimerda <pavlix@pavlix.net> - 4.6.1-3
- Change directory structure to avoid clashes with Openswan
- Prefixed all manpages with 'strongswan_'
- Every file now includes 'strongswan' somewhere in its path
- Removed conflict with Openswan
- Finally fix permissions on strongswan.conf

* Fri Jan 20 2012 Pavel Šimerda <pavlix@pavlix.net> - 4.6.1-2
- Change license tag from GPL to GPLv2+
- Change permissions on /etc/strongswan.conf to 644
- Rename ipsec.8 manpage to strongswan.8
- Fix empty scriptlets for non-fedora builds
- Add ldconfig scriptlet
- Add missing directories and files

* Sun Jan 01 2012 Pavel Šimerda <pavlix@pavlix.net - 4.6.1-1
- Bump to version 4.6.1

* Sun Jan 01 2012 Pavel Šimerda <pavlix@pavlix.net - 4.6.0-3
- Add systemd scriptlets
- Add conditions to also support EPEL6

* Sat Dec 10 2011 Pavel Šimerda <pavlix@pavlix.net> - 4.6.0-2
- Experimental build for development
