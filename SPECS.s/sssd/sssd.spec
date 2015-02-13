%global rhel7_minor %(%{__grep} -o "7.[0-9]*" /etc/redhat-release |%{__sed} -s 's/7.//')

# we don't want to provide private python extension libs
%define __provides_exclude_from %{python_sitearch}/.*\.so$|%{_libdir}/%{name}/modules/libwbclient.so.*$
%define _hardened_build 1


# Determine the location of the LDB modules directory
%global ldb_modulesdir %(pkg-config --variable=modulesdir ldb)
%global ldb_version 1.1.20

%if (0%{?fedora} || 0%{?rhel} >= 7)
    %global with_cifs_utils_plugin 1
%else
    %global with_cifs_utils_plugin_option --disable-cifs-idmap-plugin
%endif

%if (0%{?fedora} >= 21 || (0%{?rhel} == 7 &&  0%{?rhel7_minor} >= 1))
    %global with_krb5_localauth_plugin 1
%endif


%global libwbc_alternatives_suffix %nil
%if 0%{?__isa_bits} == 64
%global libwbc_alternatives_suffix -64
%endif

Name: sssd
Version: 1.12.3
Release: 5%{?dist}
Group: Applications/System
Summary: System Security Services Daemon
License: GPLv3+
URL: http://fedorahosted.org/sssd/
Source0: https://fedorahosted.org/released/sssd/%{name}-%{version}.tar.gz
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

### Patches ###
Patch0001: 0001-logrotate-Fix-warning-file-size-changed-while-zippin.patch
Patch0002: 0002-MAN-dyndns_iface-supports-only-one-interface.patch
Patch0003: 0003-krb5-fix-entry-order-in-MEMORY-keytab.patch

### Dependencies ###
Requires: sssd-common = %{version}-%{release}
Requires: sssd-ldap = %{version}-%{release}
Requires: sssd-krb5 = %{version}-%{release}
Requires: sssd-ipa = %{version}-%{release}
Requires: sssd-common-pac = %{version}-%{release}
Requires: sssd-ad = %{version}-%{release}
Requires: sssd-proxy = %{version}-%{release}
Requires: python-sssdconfig = %{version}-%{release}

%global servicename sssd
%global sssdstatedir %{_localstatedir}/lib/sss
%global dbpath %{sssdstatedir}/db
%global pipepath %{sssdstatedir}/pipes
%global mcpath %{sssdstatedir}/mc
%global pubconfpath %{sssdstatedir}/pubconf
%global gpocachepath %{sssdstatedir}/gpo_cache

### Build Dependencies ###

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool
BuildRequires: m4
BuildRequires: popt-devel
BuildRequires: libtalloc-devel
BuildRequires: libtevent-devel
BuildRequires: libtdb-devel

# LDB needs a strict version match to build
BuildRequires: libldb-devel = %{ldb_version}
BuildRequires: libdhash-devel >= 0.4.2
BuildRequires: libcollection-devel
BuildRequires: libini_config-devel >= 1.1
BuildRequires: dbus-devel
BuildRequires: dbus-libs
BuildRequires: openldap-devel
BuildRequires: pam-devel
BuildRequires: nss-devel
BuildRequires: nspr-devel
BuildRequires: pcre-devel
BuildRequires: libxslt
BuildRequires: libxml2
BuildRequires: docbook-style-xsl
%if (0%{?with_krb5_localauth_plugin} == 1)
BuildRequires: krb5-devel >= 1.12
%else
BuildRequires: krb5-devel
%endif
BuildRequires: c-ares-devel
BuildRequires: python-devel
BuildRequires: check-devel
BuildRequires: doxygen
BuildRequires: libselinux-devel
BuildRequires: libsemanage-devel
BuildRequires: bind-utils
BuildRequires: keyutils-libs-devel
BuildRequires: gettext-devel
BuildRequires: pkgconfig
BuildRequires: diffstat
BuildRequires: findutils
BuildRequires: glib2-devel
BuildRequires: selinux-policy-targeted
%ifarch %{ix86} x86_64 %{arm}
BuildRequires: libcmocka-devel
%endif
%if (0%{?fedora} >= 20)
BuildRequires: uid_wrapper
BuildRequires: nss_wrapper
%endif
BuildRequires: libnl3-devel
BuildRequires: systemd-devel
%if (0%{?with_cifs_utils_plugin} == 1)
BuildRequires: cifs-utils-devel
%endif
BuildRequires: libnfsidmap-devel

BuildRequires: samba4-devel >= 4.0.0-59beta2
BuildRequires: libsmbclient-devel

%description
Provides a set of daemons to manage access to remote directories and
authentication mechanisms. It provides an NSS and PAM interface toward
the system and a plug-gable back-end system to connect to multiple different
account sources. It is also the basis to provide client auditing and policy
services for projects like FreeIPA.

The sssd sub-package is a meta-package that contains the daemon as well as all
the existing back ends.

%package common
Summary: Common files for the SSSD
Group: Applications/System
License: GPLv3+
# Conflicts
Conflicts: selinux-policy < 3.10.0-46
Conflicts: sssd < 1.10.0-8%{?dist}.beta2
# Requires

# LDB needs a strict version match to run
# This protects against
# "sssd[XXX]: ldb: module version mismatch in src/ldb_modules/memberof.c"
Requires: libldb%{?_isa} = %{ldb_version}

Requires: libtdb%{?_isa} >= 1.1.3
Requires: sssd-client%{?_isa} = %{version}-%{release}
Requires: libsss_idmap%{?_isa} = %{version}-%{release}
Requires: libini_config >= 1.0.0.1
Requires(post): systemd-units chkconfig
Requires(preun): systemd-units chkconfig
Requires(postun): systemd-units chkconfig


### Provides ###
Provides: libsss_sudo = %{version}-%{release}
Obsoletes: libsss_sudo <= 1.10.0-7%{?dist}.beta1
Provides: libsss_sudo-devel = %{version}-%{release}
Obsoletes: libsss_sudo-devel <= 1.10.0-7%{?dist}.beta1
Provides: libsss_autofs = %{version}-%{release}
Obsoletes: libsss_autofs <= 1.10.0-7%{?dist}.beta1

%description common
Common files for the SSSD. The common package includes all the files needed
to run a particular back end, however, the back ends are packaged in separate
sub-packages such as sssd-ldap.

%package client
Summary: SSSD Client libraries for NSS and PAM
Group: Applications/System
License: LGPLv3+
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Requires(post):  /usr/sbin/alternatives
Requires(preun): /usr/sbin/alternatives

%description client
Provides the libraries needed by the PAM and NSS stacks to connect to the SSSD
service.

%package tools
Summary: Userspace tools for use with the SSSD
Group: Applications/System
License: GPLv3+
Requires: sssd-common = %{version}-%{release}

%description tools
Provides userspace tools for manipulating users, groups, and nested groups in
SSSD when using id_provider = local in /etc/sssd/sssd.conf.

Also provides several other administrative tools:
    * sss_debuglevel to change the debug level on the fly
    * sss_seed which pre-creates a user entry for use in kickstarts
    * sss_obfuscate for generating an obfuscated LDAP password

%package -n python-sssdconfig
Summary: SSSD and IPA configuration file manipulation classes and functions
Group: Applications/System
License: GPLv3+
BuildArch: noarch

%description -n python-sssdconfig
Provides python files for manipulation SSSD and IPA configuration files.

%package ldap
Summary: The LDAP back end of the SSSD
Group: Applications/System
License: GPLv3+
Conflicts: sssd < 1.10.0-8.beta2
Requires: sssd-common = %{version}-%{release}
Requires: sssd-krb5-common = %{version}-%{release}

%description ldap
Provides the LDAP back end that the SSSD can utilize to fetch identity data
from and authenticate against an LDAP server.

%package krb5-common
Summary: SSSD helpers needed for Kerberos and GSSAPI authentication
Group: Applications/System
License: GPLv3+
Conflicts: sssd < 1.10.0-8.beta2
Requires: cyrus-sasl-gssapi%{?_isa}
Requires: sssd-common = %{version}-%{release}

%description krb5-common
Provides helper processes that the LDAP and Kerberos back ends can use for
Kerberos user or host authentication.

%package krb5
Summary: The Kerberos authentication back end for the SSSD
Group: Applications/System
License: GPLv3+
Conflicts: sssd < 1.10.0-8.beta2
Requires: sssd-common = %{version}-%{release}
Requires: sssd-krb5-common = %{version}-%{release}

%description krb5
Provides the Kerberos back end that the SSSD can utilize authenticate
against a Kerberos server.

%package common-pac
Summary: Common files needed for supporting PAC processing
Group: Applications/System
License: GPLv3+
Requires: sssd-common = %{version}-%{release}

%description common-pac
Provides common files needed by SSSD providers such as IPA and Active Directory
for handling Kerberos PACs.

%package ipa
Summary: The IPA back end of the SSSD
Group: Applications/System
License: GPLv3+
Conflicts: sssd < 1.10.0-8.beta2
Requires: sssd-common = %{version}-%{release}
Requires: sssd-krb5-common = %{version}-%{release}
Requires: libipa_hbac%{?_isa} = %{version}-%{release}
Requires: bind-utils
Requires: sssd-common-pac = %{version}-%{release}

%description ipa
Provides the IPA back end that the SSSD can utilize to fetch identity data
from and authenticate against an IPA server.

%package ad
Summary: The AD back end of the SSSD
Group: Applications/System
License: GPLv3+
Conflicts: sssd < 1.10.0-8.beta2
Requires: sssd-common = %{version}-%{release}
Requires: sssd-krb5-common = %{version}-%{release}
Requires: bind-utils
Requires: sssd-common-pac = %{version}-%{release}

%description ad
Provides the Active Directory back end that the SSSD can utilize to fetch
identity data from and authenticate against an Active Directory server.

%package proxy
Summary: The proxy back end of the SSSD
Group: Applications/System
License: GPLv3+
Conflicts: sssd < 1.10.0-8.beta2
Requires: sssd-common = %{version}-%{release}

%description proxy
Provides the proxy back end which can be used to wrap an existing NSS and/or
PAM modules to leverage SSSD caching.

%package -n libsss_idmap
Summary: FreeIPA Idmap library
Group: Development/Libraries
License: LGPLv3+
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description -n libsss_idmap
Utility library to convert SIDs to Unix uids and gids

%package -n libsss_idmap-devel
Summary: FreeIPA Idmap library
Group: Development/Libraries
License: LGPLv3+
Requires: libsss_idmap = %{version}-%{release}

%description -n libsss_idmap-devel
Utility library to SIDs to Unix uids and gids

%package -n libipa_hbac
Summary: FreeIPA HBAC Evaluator library
Group: Development/Libraries
License: LGPLv3+
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description -n libipa_hbac
Utility library to validate FreeIPA HBAC rules for authorization requests

%package -n libipa_hbac-devel
Summary: FreeIPA HBAC Evaluator library
Group: Development/Libraries
License: LGPLv3+
Requires: libipa_hbac = %{version}-%{release}

%description -n libipa_hbac-devel
Utility library to validate FreeIPA HBAC rules for authorization requests

%package -n libipa_hbac-python
Summary: Python bindings for the FreeIPA HBAC Evaluator library
Group: Development/Libraries
License: LGPLv3+
Requires: libipa_hbac = %{version}-%{release}

%description -n libipa_hbac-python
The libipa_hbac-python contains the bindings so that libipa_hbac can be
used by Python applications.

%package -n libsss_nss_idmap
Summary: Library for SID based lookups
Group: Development/Libraries
License: LGPLv3+
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description -n libsss_nss_idmap
Utility library for SID based lookups

%package -n libsss_nss_idmap-devel
Summary: Library for SID based lookups
Group: Development/Libraries
License: LGPLv3+
Requires: libsss_nss_idmap = %{version}-%{release}

%description -n libsss_nss_idmap-devel
Utility library for SID based lookups

%package -n libsss_nss_idmap-python
Summary: Python bindings for libsss_nss_idmap
Group: Development/Libraries
License: LGPLv3+
Requires: libsss_nss_idmap = %{version}-%{release}

%description -n libsss_nss_idmap-python
The libsss_nss_idmap-python contains the bindings so that libsss_nss_idmap can
be used by Python applications.

%package dbus
Summary: The D-Bus responder of the SSSD
Group: Applications/System
License: GPLv3+
BuildRequires: augeas-devel
Requires: sssd-common = %{version}-%{release}

%description dbus
Provides the D-Bus responder of the SSSD, called the InfoPipe, that allows
the information from the SSSD to be transmitted over the system bus.

%package -n libsss_simpleifp
Summary: The SSSD D-Bus responder helper library
Group: Development/Libraries
License: GPLv3+
Requires: dbus-libs
Requires: sssd-dbus = %{version}-%{release}
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description -n libsss_simpleifp
Provides library that simplifies D-Bus API for the SSSD InfoPipe responder.

%package -n libsss_simpleifp-devel
Summary: The SSSD D-Bus responder helper library
Group: Development/Libraries
License: GPLv3+
Requires: dbus-devel
Requires: libsss_simpleifp = %{version}-%{release}

%description -n libsss_simpleifp-devel
Provides library that simplifies D-Bus API for the SSSD InfoPipe responder.

%package libwbclient
Summary: The SSSD libwbclient implementation
Group: Applications/System
License: GPLv3+ and LGPLv3+
Conflicts: libwbclient < 4.2.0-0.2.rc2

%description libwbclient
The SSSD libwbclient implementation.

%package libwbclient-devel
Summary: Development libraries for the SSSD libwbclient implementation
Group:  Development/Libraries
License: GPLv3+ and LGPLv3+
Conflicts: libwbclient-devel < 4.2.0-0.2.rc2

%description libwbclient-devel
Development libraries for the SSSD libwbclient implementation.

%prep
# Update timestamps on the files touched by a patch, to avoid non-equal
# .pyc/.pyo files across the multilib peers within a build, where "Level"
# is the patch prefix option (e.g. -p1)
# Taken from specfile for python-simplejson
UpdateTimestamps() {
  Level=$1
  PatchFile=$2

  # Locate the affected files:
  for f in $(diffstat $Level -l $PatchFile); do
    # Set the files to have the same timestamp as that of the patch:
    touch -r $PatchFile $f
  done
}

%setup -q

for p in %patches ; do
    %__patch -p1 -i $p
    UpdateTimestamps -p1 $p
done

%build
autoreconf -ivf

%configure \
    --with-test-dir=/dev/shm \
    --with-db-path=%{dbpath} \
    --with-mcache-path=%{mcpath} \
    --with-pipe-path=%{pipepath} \
    --with-pubconf-path=%{pubconfpath} \
    --with-gpo-cache-path=%{gpocachepath} \
    --with-init-dir=%{_initrddir} \
    --with-krb5-rcache-dir=%{_localstatedir}/cache/krb5rcache \
    --enable-nsslibdir=%{_libdir} \
    --enable-pammoddir=%{_libdir}/security \
    --enable-nfsidmaplibdir=%{_libdir}/libnfsidmap \
    --disable-static \
    --disable-rpath \
    --with-initscript=systemd \
    --with-syslog=journald \
    %{?with_cifs_utils_plugin_option} \
    --enable-ldb-version-check \
    --enable-sss-default-nss-plugin

make %{?_smp_mflags} all docs

%check
export CK_TIMEOUT_MULTIPLIER=10
make %{?_smp_mflags} check VERBOSE=yes
unset CK_TIMEOUT_MULTIPLIER

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# Prepare language files
/usr/lib/rpm/find-lang.sh $RPM_BUILD_ROOT sssd

# Prepare empty config file
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/sssd
touch $RPM_BUILD_ROOT/%{_sysconfdir}/sssd/sssd.conf

# Copy default logrotate file
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/logrotate.d
install -m644 src/examples/logrotate $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/sssd

# Make sure SSSD is able to run on read-only root
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/rwtab.d
install -m644 src/examples/rwtab $RPM_BUILD_ROOT%{_sysconfdir}/rwtab.d/sssd

# Replace sysv init script with systemd unit file
rm -f $RPM_BUILD_ROOT/%{_initrddir}/%{name}
mkdir -p $RPM_BUILD_ROOT/%{_unitdir}/
cp src/sysv/systemd/sssd.service $RPM_BUILD_ROOT/%{_unitdir}/

# Remove .la files created by libtool
find $RPM_BUILD_ROOT -name "*.la" -exec rm -f {} \;

# Suppress developer-only documentation
rm -Rf ${RPM_BUILD_ROOT}/%{_docdir}/%{name}

# Older versions of rpmbuild can only handle one -f option
# So we need to append to the sssd*.lang file
for file in `ls $RPM_BUILD_ROOT/%{python_sitelib}/*.egg-info 2> /dev/null`
do
    echo %{python_sitelib}/`basename $file` >> python_sssdconfig.lang
done

touch sssd_tools.lang
touch sssd_client.lang
for provider in ldap krb5 ipa ad proxy
do
    touch sssd_$provider.lang
done

for man in `find $RPM_BUILD_ROOT/%{_mandir}/??/man?/ -type f | sed -e "s#$RPM_BUILD_ROOT/%{_mandir}/##"`
do
    lang=`echo $man | cut -c 1-2`
    case `basename $man` in
        sss_cache*)
            echo \%lang\(${lang}\) \%{_mandir}/${man}\* >> sssd.lang
            ;;
        sss_*)
            echo \%lang\(${lang}\) \%{_mandir}/${man}\* >> sssd_tools.lang
            ;;
        sssd_krb5_*)
            echo \%lang\(${lang}\) \%{_mandir}/${man}\* >> sssd_client.lang
            ;;
        pam_sss*)
            echo \%lang\(${lang}\) \%{_mandir}/${man}\* >> sssd_client.lang
            ;;
        sssd-ldap*)
            echo \%lang\(${lang}\) \%{_mandir}/${man}\* >> sssd_ldap.lang
            ;;
        sssd-krb5*)
            echo \%lang\(${lang}\) \%{_mandir}/${man}\* >> sssd_krb5.lang
            ;;
        sssd-ipa*)
            echo \%lang\(${lang}\) \%{_mandir}/${man}\* >> sssd_ipa.lang
            ;;
        sssd-ad*)
            echo \%lang\(${lang}\) \%{_mandir}/${man}\* >> sssd_ad.lang
            ;;
        sssd-proxy*)
            echo \%lang\(${lang}\) \%{_mandir}/${man}\* >> sssd_proxy.lang
            ;;
        *)
            echo \%lang\(${lang}\) \%{_mandir}/${man}\* >> sssd.lang
            ;;
    esac
done

# Print these to the rpmbuild log
echo "sssd.lang:"
cat sssd.lang

echo "sssd_client.lang:"
cat sssd_client.lang

echo "sssd_tools.lang:"
cat sssd_tools.lang

for provider in ldap krb5 ipa ad proxy
do
    echo "sssd_$provider.lang:"
    cat sssd_$provider.lang
done


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc COPYING

%files common -f sssd.lang
%defattr(-,root,root,-)
%doc COPYING
%doc src/examples/sssd-example.conf
%{_sbindir}/sssd
%{_unitdir}/sssd.service

%dir %{_libexecdir}/%{servicename}
%{_libexecdir}/%{servicename}/sssd_be
%{_libexecdir}/%{servicename}/sssd_nss
%{_libexecdir}/%{servicename}/sssd_pam
%{_libexecdir}/%{servicename}/sssd_autofs
%{_libexecdir}/%{servicename}/sssd_ssh
%{_libexecdir}/%{servicename}/sssd_sudo

%dir %{_libdir}/%{name}
%{_libdir}/%{name}/libsss_simple.so

#Internal shared libraries
%{_libdir}/%{name}/libsss_child.so
%{_libdir}/%{name}/libsss_crypt.so
%{_libdir}/%{name}/libsss_debug.so
%{_libdir}/%{name}/libsss_ldap_common.so
%{_libdir}/%{name}/libsss_util.so
%{_libdir}/%{name}/libsss_semanage.so

# 3rd party application libraries
%{_libdir}/sssd/modules/libsss_autofs.so
%{_libdir}/libsss_sudo.so
%{_libdir}/libnfsidmap/sss.so

%{ldb_modulesdir}/memberof.so
%{_bindir}/sss_ssh_authorizedkeys
%{_bindir}/sss_ssh_knownhostsproxy
%{_sbindir}/sss_cache
%{_libexecdir}/%{servicename}/sss_signal

%dir %{sssdstatedir}
%dir %{_localstatedir}/cache/krb5rcache
%attr(700,root,root) %dir %{dbpath}
%attr(755,root,root) %dir %{mcpath}
%ghost %attr(0644,root,root) %verify(not md5 size mtime) %{mcpath}/passwd
%ghost %attr(0644,root,root) %verify(not md5 size mtime) %{mcpath}/group
%attr(755,root,root) %dir %{pipepath}
%attr(755,root,root) %dir %{pubconfpath}
%attr(755,root,root) %dir %{gpocachepath}
%attr(700,root,root) %dir %{pipepath}/private
%attr(750,root,root) %dir %{_var}/log/%{name}
%attr(700,root,root) %dir %{_sysconfdir}/sssd
%ghost %attr(0600,root,root) %config(noreplace) %{_sysconfdir}/sssd/sssd.conf
%attr(755,root,root) %dir %{_sysconfdir}/systemd/system/sssd.service.d
%config(noreplace) %{_sysconfdir}/systemd/system/sssd.service.d/journal.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/sssd
%config(noreplace) %{_sysconfdir}/rwtab.d/sssd
%dir %{_datadir}/sssd
%{_datadir}/sssd/sssd.api.conf
%{_datadir}/sssd/sssd.api.d
%{_mandir}/man1/sss_ssh_authorizedkeys.1*
%{_mandir}/man1/sss_ssh_knownhostsproxy.1*
%{_mandir}/man5/sssd.conf.5*
%{_mandir}/man5/sssd-simple.5*
%{_mandir}/man5/sssd-sudo.5*
%{_mandir}/man5/sss_rpcidmapd.5*
%{_mandir}/man8/sssd.8*
%{_mandir}/man8/sss_cache.8*
%{python_sitearch}/pysss.so
%{python_sitearch}/pysss_murmur.so

%files ldap -f sssd_ldap.lang
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/%{name}/libsss_ldap.so
%{_mandir}/man5/sssd-ldap.5*

%files krb5-common
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/%{name}/libsss_krb5_common.so
%{_libexecdir}/%{servicename}/ldap_child
%{_libexecdir}/%{servicename}/krb5_child

%files krb5 -f sssd_krb5.lang
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/%{name}/libsss_krb5.so
%{_mandir}/man5/sssd-krb5.5*

%files common-pac
%defattr(-,root,root,-)
%doc COPYING
%{_libexecdir}/%{servicename}/sssd_pac

%files ipa -f sssd_ipa.lang
%defattr(-,root,root,-)
%doc COPYING
%attr(755,root,root) %dir %{pubconfpath}/krb5.include.d
%{_libdir}/%{name}/libsss_ipa.so
%{_libexecdir}/%{servicename}/selinux_child
%{_mandir}/man5/sssd-ipa.5*

%files ad -f sssd_ad.lang
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/%{name}/libsss_ad.so
%{_libdir}/%{name}/libsss_ad_common.so
%{_libexecdir}/%{servicename}/gpo_child
%{_mandir}/man5/sssd-ad.5*

%files proxy
%defattr(-,root,root,-)
%doc COPYING
%{_libexecdir}/%{servicename}/proxy_child
%{_libdir}/%{name}/libsss_proxy.so

%files dbus
%defattr(-,root,root,-)
%doc COPYING
%{_libexecdir}/%{servicename}/sssd_ifp
%{_mandir}/man5/sssd-ifp.5*
# InfoPipe DBus plumbing
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.sssd.infopipe.conf
%{_datadir}/dbus-1/system-services/org.freedesktop.sssd.infopipe.service
%{_libdir}/%{name}/libsss_config.so

%files -n libsss_simpleifp
%defattr(-,root,root,-)
%{_libdir}/libsss_simpleifp.so.*

%files -n libsss_simpleifp-devel
%defattr(-,root,root,-)
%doc sss_simpleifp_doc/html
%{_includedir}/sss_sifp.h
%{_includedir}/sss_sifp_dbus.h
%{_libdir}/libsss_simpleifp.so
%{_libdir}/pkgconfig/sss_simpleifp.pc

%files client -f sssd_client.lang
%defattr(-,root,root,-)
%doc src/sss_client/COPYING src/sss_client/COPYING.LESSER
%{_libdir}/libnss_sss.so.2
%{_libdir}/security/pam_sss.so
%{_libdir}/krb5/plugins/libkrb5/sssd_krb5_locator_plugin.so
%{_libdir}/krb5/plugins/authdata/sssd_pac_plugin.so
%if (0%{?with_cifs_utils_plugin} == 1)
%{_libdir}/cifs-utils/cifs_idmap_sss.so
%ghost %{_sysconfdir}/cifs-utils/idmap-plugin
%endif
%if (0%{?with_krb5_localauth_plugin} == 1)
%{_libdir}/%{name}/modules/sssd_krb5_localauth_plugin.so
%endif
%{_mandir}/man8/pam_sss.8*
%{_mandir}/man8/sssd_krb5_locator_plugin.8*

%files tools -f sssd_tools.lang
%defattr(-,root,root,-)
%doc COPYING
%{_sbindir}/sss_useradd
%{_sbindir}/sss_userdel
%{_sbindir}/sss_usermod
%{_sbindir}/sss_groupadd
%{_sbindir}/sss_groupdel
%{_sbindir}/sss_groupmod
%{_sbindir}/sss_groupshow
%{_sbindir}/sss_obfuscate
%{_sbindir}/sss_debuglevel
%{_sbindir}/sss_seed
%{_mandir}/man8/sss_groupadd.8*
%{_mandir}/man8/sss_groupdel.8*
%{_mandir}/man8/sss_groupmod.8*
%{_mandir}/man8/sss_groupshow.8*
%{_mandir}/man8/sss_useradd.8*
%{_mandir}/man8/sss_userdel.8*
%{_mandir}/man8/sss_usermod.8*
%{_mandir}/man8/sss_obfuscate.8*
%{_mandir}/man8/sss_debuglevel.8*
%{_mandir}/man8/sss_seed.8*

%files -n python-sssdconfig -f python_sssdconfig.lang
%defattr(-,root,root,-)
%dir %{python_sitelib}/SSSDConfig
%{python_sitelib}/SSSDConfig/*.py*

%files -n libsss_idmap
%defattr(-,root,root,-)
%doc src/sss_client/COPYING src/sss_client/COPYING.LESSER
%{_libdir}/libsss_idmap.so.*

%files -n libsss_idmap-devel
%defattr(-,root,root,-)
%doc idmap_doc/html
%{_includedir}/sss_idmap.h
%{_libdir}/libsss_idmap.so
%{_libdir}/pkgconfig/sss_idmap.pc

%files -n libipa_hbac
%defattr(-,root,root,-)
%doc src/sss_client/COPYING src/sss_client/COPYING.LESSER
%{_libdir}/libipa_hbac.so.*

%files -n libipa_hbac-devel
%defattr(-,root,root,-)
%doc hbac_doc/html
%{_includedir}/ipa_hbac.h
%{_libdir}/libipa_hbac.so
%{_libdir}/pkgconfig/ipa_hbac.pc

%files -n libsss_nss_idmap
%defattr(-,root,root,-)
%doc src/sss_client/COPYING src/sss_client/COPYING.LESSER
%{_libdir}/libsss_nss_idmap.so.*

%files -n libsss_nss_idmap-devel
%defattr(-,root,root,-)
%doc nss_idmap_doc/html
%{_includedir}/sss_nss_idmap.h
%{_libdir}/libsss_nss_idmap.so
%{_libdir}/pkgconfig/sss_nss_idmap.pc

%files -n libsss_nss_idmap-python
%defattr(-,root,root,-)
%{python_sitearch}/pysss_nss_idmap.so

%files -n libipa_hbac-python
%defattr(-,root,root,-)
%{python_sitearch}/pyhbac.so

%files libwbclient
%defattr(-,root,root,-)
%{_libdir}/%{name}/modules/libwbclient.so.*

%files libwbclient-devel
%defattr(-,root,root,-)
%{_includedir}/wbclient_sssd.h
%{_libdir}/%{name}/modules/libwbclient.so
%{_libdir}/pkgconfig/wbclient_sssd.pc

%post common
if [ $1 -ge 1 ] ; then
    # Initial installation
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%preun common
if [ $1 -eq 0 ]; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable sssd.service > /dev/null 2>&1 || :
    /bin/systemctl stop sssd.service > /dev/null 2>&1 || :
fi

%postun common
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /bin/systemctl try-restart sssd.service >/dev/null 2>&1 || :
fi

%if (0%{?with_cifs_utils_plugin} == 1)
%post client
/sbin/ldconfig
/usr/sbin/alternatives --install /etc/cifs-utils/idmap-plugin cifs-idmap-plugin %{_libdir}/cifs-utils/cifs_idmap_sss.so 20

%preun client
if [ $1 -eq 0 ]; then
        /usr/sbin/alternatives --remove cifs-idmap-plugin %{_libdir}/cifs-utils/cifs_idmap_sss.so
fi
%else
%post client -p /sbin/ldconfig
%endif

%postun client -p /sbin/ldconfig

%post -n libipa_hbac -p /sbin/ldconfig

%postun -n libipa_hbac -p /sbin/ldconfig

%post -n libsss_idmap -p /sbin/ldconfig

%postun -n libsss_idmap -p /sbin/ldconfig

%post -n libsss_nss_idmap -p /sbin/ldconfig

%postun -n libsss_nss_idmap -p /sbin/ldconfig

%post libwbclient
%{_sbindir}/update-alternatives --install %{_libdir}/libwbclient.so.0.11 \
                                libwbclient.so.0.11%{libwbc_alternatives_suffix} \
                                %{_libdir}/%{name}/modules/libwbclient.so.0.11.0 5
/sbin/ldconfig

%preun libwbclient
if [ $1 -eq 0 ]; then
        %{_sbindir}/update-alternatives --remove \
                                libwbclient.so.0.11%{libwbc_alternatives_suffix} \
                                %{_libdir}/%{name}/modules/libwbclient.so.0.11.0
fi
/sbin/ldconfig

%post libwbclient-devel
%{_sbindir}/update-alternatives --install %{_libdir}/libwbclient.so \
                                libwbclient.so%{libwbc_alternatives_suffix} \
                                %{_libdir}/%{name}/modules/libwbclient.so 5

%preun libwbclient-devel
if [ $1 -eq 0 ]; then
        %{_sbindir}/update-alternatives --remove \
                                libwbclient.so%{libwbc_alternatives_suffix} \
                                %{_libdir}/%{name}/modules/libwbclient.so
fi

%changelog
* Wed Jan 28 2015 Jakub Hrozek <jhrozek@redhat.com> - 1.12.3-5
- Rebuild for new libldb

* Thu Jan 22 2015 Lukas Slebodnik <lslebodn@redhat.com> - 1.12.3-4
- Decrease priority of sssd-libwbclient 20 -> 5
- It should be lower than priority of samba veriosn of libwbclient.
- https://bugzilla.redhat.com/show_bug.cgi?id=1175511#c18

* Mon Jan 19 2015 Lukas Slebodnik <lslebodn@redhat.com> - 1.12.3-3
- Apply a number of patches from upstream to fix issues found 1.12.3
- Resolves: rhbz#1176373 - dyndns_iface does not accept multiple
                           interfaces, or isn't documented to be able to
- Resolves: rhbz#988068 - getpwnam_r fails for non-existing users when sssd is
                          not running
- Resolves: upstream #2557  authentication failure with user from AD

* Fri Jan 09 2015 Lukas Slebodnik <lslebodn@redhat.com> - 1.12.3-2
- Resolves: rhbz#1164156 - libsss_simpleifp should pull sssd-dbus
- Resolves: rhbz#1179379 - gzip: stdin: file size changed while
                           zipping when rotating logfile

* Thu Jan 08 2015 Lukas Slebodnik <lslebodn@redhat.com> - 1.12.3-1
- New upstream release 1.12.3
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.12.3
- Fix spelling errors in description (fedpkg lint)

* Tue Jan  6 2015 Lukas Slebodnik <lslebodn@redhat.com> - 1.12.2-8
- Rebuild for libldb 1.1.19

* Fri Dec 19 2014 Sumit Bose <sbose@redhat.com> - 1.12.2-7
- Resolves: rhbz#1175511 - sssd-libwbclient conflicts with Samba's and causes
                           crash in wbinfo
                           - in addition to the patch libwbclient.so is
                             filtered out of the Provides list of the package

* Wed Dec 17 2014 Lukas Slebodnik <lslebodn@redhat.com> - 1.12.2-6
- Fix regressions and bugs in sssd upstream 1.12.2
- https://fedorahosted.org/sssd/ticket/{id}
- Regressions: #2471, #2475, #2483, #2487, #2529, #2535
- Bugs: #2287, #2445

* Sun Dec  7 2014 Jakub Hrozek <jhrozek@redhat.com> - 1.12.2-5
- Rebuild for libldb 1.1.18

* Wed Nov 26 2014 Jakub Hrozek <jhrozek@redhat.com> - 1.12.2-4
- Fix typo in libwbclient-devel %preun

* Tue Nov 25 2014 Jakub Hrozek <jhrozek@redhat.com> - 1.12.2-3
- Use alternatives for libwbclient

* Wed Oct 22 2014 Jakub Hrozek <jhrozek@redhat.com> - 1.12.2-2
- Backport several patches from upstream.
- Fix a potential crash against old (pre-4.0) IPA servers

* Mon Oct 20 2014 Jakub Hrozek <jhrozek@redhat.com> - 1.12.2-1
- New upstream release 1.12.2
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.12.2

* Mon Sep 15 2014 Jakub Hrozek <jhrozek@redhat.com> - 1.12.1-2
- Resolves: rhbz#1139962 - Fedora 21, FreeIPA 4.0.2: sssd does not find user
                           private group from server

* Mon Sep  8 2014 Jakub Hrozek <jhrozek@redhat.com> - 1.12.1-1
- New upstream release 1.12.1
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.12.1

* Fri Aug 22 2014 Jakub Hrozek <jhrozek@redhat.com> - 1.12.0-7
- Do not crash on resolving a group SID in IPA server mode

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 10 2014 Stephen Gallagher <sgallagh@redhat.com> 1.12.0-5
- Fix release version for upgrades

* Wed Jul 09 2014 Jakub Hrozek <jhrozek@redhat.com> - 1.12.0-1
- New upstream release 1.12.0
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.12.0

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.0-4.beta2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Jun 04 2014 Jakub Hrozek <jhrozek@redhat.com> - 1.12.0-1.beta2
- New upstream release 1.12 beta2
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.12.0beta2

* Mon Jun 02 2014 Jakub Hrozek <jhrozek@redhat.com> - 1.12.0-2.beta1
- Fix tests on big-endian
- Fix previous changelog entry

* Fri May 30 2014 Jakub Hrozek <jhrozek@redhat.com> - 1.12.0-1.beta1
- New upstream release 1.12 beta1
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.12.0beta1

* Thu May 29 2014 Jakub Hrozek <jhrozek@redhat.com> - 1.11.5.1-4
- Rebuild against new ding-libs

* Thu May 08 2014 Stephen Gallagher <sgallagh@redhat.com> - 1.11.5.1-3
- Make LDB dependency a strict equivalency

* Thu May 08 2014 Stephen Gallagher <sgallagh@redhat.com> - 1.11.5.1-2
- Rebuild against new libldb

* Fri Apr 11 2014 Jakub Hrozek <jhrozek@redhat.com> - 1.11.5.1-1
- New upstream release 1.11.5.1
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.11.5.1

* Thu Apr 10 2014 Stephen Gallagher <sgallagh@redhat.com> 1.11.5-2
- Fix bug in generation of systemd unit file

* Tue Apr 08 2014 Jakub Hrozek <jhrozek@redhat.com> - 1.11.5-1
- New upstream release 1.11.5
- Remove upstreamed patch
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.11.5

* Thu Mar 13 2014 Sumit Bose <sbose@redhat.com> - 1.11.4-3
- Handle new error code for IPA password migration

* Tue Mar 11 2014 Jakub Hrozek <jhrozek@redhat.com> - 1.11.4-2
- Include couple of patches from upstream 1.11 branch

* Mon Feb 17 2014 Jakub Hrozek <jhrozek@redhat.com> - 1.11.4-1
- New upstream release 1.11.4
- Remove upstreamed patch
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.11.4

* Tue Feb 11 2014 Jakub Hrozek <jhrozek@redhat.com> - 1.11.3-2
- Handle OTP response from FreeIPA server gracefully

* Wed Oct 30 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.11.3-1
- New upstream release 1.11.3
- Remove upstreamed patches
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.11.3

* Wed Oct 30 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.11.2-1
- New upstream release 1.11.2
- Remove upstreamed patches
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.11.2

* Wed Oct 16 2013 Sumit Bose <sbose@redhat.com> - 1.11.1-5
- Fix potential crash with external groups in trusted IPA-AD setup

* Mon Oct 14 2013 Sumit Bose <sbose@redhat.com> - 1.11.1-4
- Add plugin for cifs-utils
- Resolves: rhbz#998544

* Tue Oct 08 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.11.1-3
- Fix failover from Global Catalog to LDAP in case GC is not available

* Fri Oct 04 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.11.1-2
- Remove the ability to create public ccachedir (#1015089)

* Fri Sep 27 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.11.1-1
- New upstream release 1.11.1
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.11.1

* Thu Sep 26 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.11.0-3
- Fix multicast checks in the SSSD
- Resolves: rhbz#1007475 - The multicast check is wrong in the sudo source
                           code getting the host info

* Wed Aug 28 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.11.0-2
- Backport simplification of ccache management from 1.11.1
- Resolves: rhbz#1010553 - sssd setting KRB5CCNAME=(null) on login

* Wed Aug 28 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.11.0-1
- New upstream release 1.11.0
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.11.0

* Fri Aug 23 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.11.0-0.4.beta2
- Resolves: #967012 - [abrt] sssd-1.9.5-1.fc18: sss_mmap_cache_gr_invalidate_gid:
                      Process /usr/libexec/sssd/sssd_nss was killed by
                      signal 11 (SIGSEGV)
- Resolves: #996214 - sssd proxy_child segfault

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11.0-0.3.beta2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 31 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.11.0.2beta2
- Resolves: #906427 - Do not use %{_lib} in specfile for the nss and
                      pam libraries

* Wed Jul 24 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.11.0.1beta2
- New upstream release 1.11 beta 2
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.11.0beta2

* Thu Jul 18 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.10.1-1
- New upstream release 1.10.1
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.10.1

* Mon Jul 08 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.10.0-17
- sssd-tools should require sssd-common, not sssd

* Tue Jul 02 2013 Stephen Gallagher <sgallagh@redhat.com> - 1.10.0-16
- Move sssd_pac to the sssd-ipa and sssd-ad subpackages
- Trim out RHEL5-specific macros since we don't build on RHEL 5
- Trim out macros for Fedora older than F18
- Update libldb requirement to 1.1.16
- Trim RPM changelog down to the last year

* Tue Jul 02 2013 Stephen Gallagher <sgallagh@redhat.com> - 1.10.0-15
- Move sssd_pac to the sssd-krb5 subpackage

* Mon Jul 01 2013 Stephen Gallagher <sgallagh@redhat.com> - 1.10.0-14
- Fix Obsoletes: to account for dist tag
- Convert post and pre scripts to run on the sssd-common subpackage
- Remove old conversion from SYSV

* Thu Jun 27 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.10.0-13
- New upstream release 1.10
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.10.0

* Mon Jun 17 2013 Dan Horák <dan[at]danny.cz> - 1.10.0-12.beta2
- the cmocka toolkit exists only on selected arches

* Sun Jun 16 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.10.0-11.beta2
- Apply a number of patches from upstream to fix issues found post-beta,
  in particular:
  -- segfault with a high DEBUG level
  -- Fix IPA password migration (upstream #1873)
  -- Fix fail over when retrying SRV resolution (upstream #1886)

* Thu Jun 13 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.10.0-10.beta2
- Only BuildRequire libcmocka on Fedora

* Thu Jun 13 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.10.0-9.beta2
- Fix typo in Requires that prevented an upgrade (#973916)
- Use a hardcoded version in Conflicts, not less-than-current

* Wed Jun 12 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.10.0-8.beta1
- Enable hardened build for RHEL7

* Wed Jun 12 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.10.0-8.beta2
- New upstream release 1.10 beta2
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.10.0beta2
- BuildRequire libcmocka-devel in order to run all upstream tests during build
- BuildRequire libnl3 instead of libnl1
- No longer BuildRequire initscripts, we no longer use /sbin/service
- Remove explicit krb5-libs >= 1.10 requires; this platform doensn't carry any
  older krb5-libs version

* Fri May 24 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.10.0-7.beta1
- Apply a couple of patches from upstream git that resolve crashes when
  ID mapping object was not initialized properly but needed later

* Tue May 14 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.10.0-6.beta1
- Resolves: rhbz#961357 - Missing dyndns_update entry in sssd.conf during
                          realm join
- Resolves: rhbz#961278 - Login failure: Enterprise Principal enabled by
                          default for AD Provider
- Resolves: rhbz#961251 - sssd does not create user's krb5 ccache dir/file
                          parent directory when logging in

* Tue May  7 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.10.0-5.beta1
- BuildRequire recent libini_config to ensure consistent behaviour

* Tue May  7 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.10.0-4.beta1
- Explicitly Require libini_config >= 1.0.0.1 to work around a SONAME bug
  in ding-libs
- Fix SSH integration with fully-qualified domains
- Add the ability to dynamically discover the NetBIOS name

* Fri May  3 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.10.0-3.beta1
- New upstream release 1.10 beta1
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.10.0beta1

* Wed Apr 17 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.10.0-2.alpha1
- Add a patch to fix krb5 ccache creation issue with krb5 1.11

* Tue Apr  2 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.10.0-1.alpha1
- New upstream release 1.10 alpha1
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.10.0alpha1

* Fri Mar 29 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.9.5-10
- Add a patch to fix krb5 unit tests

* Fri Mar 01 2013 Stephen Gallagher <sgallagh@redhat.com> - 1.9.4-9
- Split internal helper libraries into a shared object
- Significantly reduce disk-space usage

* Thu Feb 14 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.9.4-8
- Fix the Kerberos password expiration warning (#912223)

* Thu Feb 14 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.9.4-7
- Do not write out dots in the domain-realm mapping file (#905650)

* Mon Feb 11 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.9.4-6
- Include upstream patch to build with krb5-1.11

* Thu Feb 07 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.9.4-5
- Rebuild against new libldb

* Mon Feb 04 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.9.4-4
- Fix build with new automake versions

* Wed Jan 30 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.9.4-3
- Recreate Kerberos ccache directory if it's missing
- Resolves: rhbz#853558 - [sssd[krb5_child[PID]]]: Credential cache
                          directory /run/user/UID/ccdir does not exist

* Tue Jan 29 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.9.4-2
- Fix changelog dates to make F19 rpmbuild happy

* Mon Jan 28 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.9.4-1
- New upstream release 1.9.4

* Thu Dec 06 2012 Jakub Hrozek <jhrozek@redhat.com> - 1.9.3-1
- New upstream release 1.9.3

* Tue Oct 30 2012 Jakub Hrozek <jhrozek@redhat.com> - 1.9.2-5
- Resolve groups from AD correctly

* Tue Oct 30 2012 Jakub Hrozek <jhrozek@redhat.com> - 1.9.2-4
- Check the validity of naming context

* Thu Oct 18 2012 Jakub Hrozek <jhrozek@redhat.com> - 1.9.2-3
- Move the sss_cache tool to the main package

* Sun Oct 14 2012 Jakub Hrozek <jhrozek@redhat.com> - 1.9.2-2
- Include the 1.9.2 tarball

* Sun Oct 14 2012 Jakub Hrozek <jhrozek@redhat.com> - 1.9.2-1
- New upstream release 1.9.2

* Sun Oct 07 2012 Jakub Hrozek <jhrozek@redhat.com> - 1.9.1-1
- New upstream release 1.9.1

* Wed Oct 03 2012 Jakub Hrozek <jhrozek@redhat.com> - 1.9.0-24
- require the latest libldb

* Tue Sep 25 2012 Jakub Hrozek <jhrozek@redhat.com> - 1.9.0-24
- Use mcpath insted of mcachepath macro to be consistent with
  upsteam spec file

* Tue Sep 25 2012 Jakub Hrozek <jhrozek@redhat.com> - 1.9.0-23
- New upstream release 1.9.0

* Fri Sep 14 2012 Jakub Hrozek <jhrozek@redhat.com> - 1.9.0-22.rc1
- New upstream release 1.9.0 rc1

* Thu Sep 06 2012 Jakub Hrozek <jhrozek@redhat.com> - 1.9.0-21.beta7
- New upstream release 1.9.0 beta7
- obsoletes patches #1-#3

* Mon Sep 03 2012 Jakub Hrozek <jhrozek@redhat.com> - 1.9.0-20.beta6
- Rebuild against libldb 1.12

* Tue Aug 28 2012 Jakub Hrozek <jhrozek@redhat.com> - 1.9.0-19.beta6
- Rebuild against libldb 1.11

* Fri Aug 24 2012 Jakub Hrozek <jhrozek@redhat.com> - 1.9.0-18.beta6
- Change the default ccache location to DIR:/run/user/${UID}/krb5cc
  and patch man page accordingly
- Resolves: rhbz#851304

* Mon Aug 20 2012 Jakub Hrozek <jhrozek@redhat.com> - 1.9.0-17.beta6
- Rebuild against libldb 1.10

* Fri Aug 17 2012 Jakub Hrozek <jhrozek@redhat.com> - 1.9.0-16.beta6
- Only create the SELinux login file if there are SELinux mappings on
  the IPA server

* Fri Aug 10 2012 Jakub Hrozek <jhrozek@redhat.com> - 1.9.0-14.beta6
- Don't discard HBAC rule processing result if SELinux is on
  Resolves: rhbz#846792 (CVE-2012-3462)

* Thu Aug 02 2012 Jakub Hrozek <jhrozek@redhat.com> - 1.9.0-13.beta6
- New upstream release 1.9.0 beta 6
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.9.0beta6
- A new option, override_shell was added. If this option is set, all users
  managed by SSSD will have their shell set to its value.
- Fixes for the support for setting default SELinux user context from FreeIPA.
- Fixed a regression introduced in beta 5 that broke LDAP SASL binds
- The SSSD supports the concept of a Primary Server and a Back Up Server in
  failover
- A new command-line tool sss_seed is available to help prime the cache with
  a user record when deploying a new machine
- SSSD is now able to discover and save the domain-realm mappings
  between an IPA server and a trusted Active Directory server.
- Packaging changes to fix ldconfig usage in subpackages (#843995)
- Rebuild against libldb 1.1.9

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.0-13.beta5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jul 19 2012 Jakub Hrozek <jhrozek@redhat.com> - 1.9.0-12.beta5
- New upstream release 1.9.0 beta 5
- Obsoletes the patch for missing DP_OPTION_TERMINATOR in AD provider options
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.9.0beta5
- Many fixes for the support for setting default SELinux user context from
  FreeIPA, most notably fixed the specificity evaluation
- Fixed an incorrect default in the krb5_canonicalize option of the AD
  provider which was preventing password change operation
- The shadowLastChange attribute value is now correctly updated with the
  number of days since the Epoch, not seconds

* Mon Jul 16 2012 Stephen Gallagher <sgallagh@redhat.com> - 1.9.0-11.beta4
- Fix broken ARM build
- Add missing DP_OPTION_TERMINATOR in AD provider options

* Wed Jul 11 2012 Jakub Hrozek <jhrozek@redhat.com> - 1.9.0-10.beta4
- Own several directories create during make install (#839782)

* Wed Jul 11 2012 Jakub Hrozek <jhrozek@redhat.com> - 1.9.0-9.beta4
- New upstream release 1.9.0 beta 4
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.9.0beta4
- Add a new AD provider to improve integration with Active Directory 2008 R2
  or later servers
- SUDO integration was completely rewritten. The new implementation works
  with multiple domains and uses an improved refresh mechanism to download
  only the necessary rules
- The IPA authentication provider now supports subdomains
- Fixed regression for setups that were setting default_tkt_enctypes
  manually by reverting a previous workaround.

* Mon Jun 25 2012 Stephen Gallagher <sgallagh@redhat.com> - 1.9.0-8.beta3
- New upstream release 1.9.0 beta 3
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.9.0beta3
- Add a new PAC responder for dealing with cross-realm Kerberos trusts
- Terminate idle connections to the NSS and PAM responders

* Wed Jun 20 2012 Stephen Gallagher <sgallagh@redhat.com> - 1.9.0-7.beta2
- Switch unicode library from libunistring to Glib
- Drop unnecessary explicit Requires on keyutils
- Guarantee that versioned Requires include the correct architecture

* Mon Jun 18 2012 Stephen Gallagher <sgallagh@redhat.com> - 1.9.0-6.beta2
- Fix accidental disabling of the DIR cache support

* Fri Jun 15 2012 Stephen Gallagher <sgallagh@redhat.com> - 1.9.0-5.beta2
- New upstream release 1.9.0 beta 2
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.9.0beta2
- Add support for the Kerberos DIR cache for storing multiple TGTs
  automatically
- Major performance enhancement when storing large groups in the cache
- Major performance enhancement when performing initgroups() against Active
  Directory
- SSSDConfig data file default locations can now be set during configure for
  easier packaging

* Tue May 29 2012 Stephen Gallagher <sgallagh@redhat.com> - 1.9.0-4.beta1
- Fix regression in endianness patch

* Tue May 29 2012 Stephen Gallagher <sgallagh@redhat.com> - 1.9.0-3.beta1
- Rebuild SSSD against ding-libs 0.3.0beta1
- Fix endianness bug in service map protocol

* Thu May 24 2012 Stephen Gallagher <sgallagh@redhat.com> - 1.9.0-2.beta1
- Fix several regressions since 1.5.x
- Ensure that the RPM creates the /var/lib/sss/mc directory
- Add support for Netscape password warning expiration control
- Rebuild against libldb 1.1.6

* Fri May 11 2012 Stephen Gallagher <sgallagh@redhat.com> - 1.9.0-1.beta1
- New upstream release 1.9.0 beta 1
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.9.0beta1
- Add native support for autofs to the IPA provider
- Support for ID-mapping when connecting to Active Directory
- Support for handling very large (> 1500 users) groups in Active Directory
- Support for sub-domains (will be used for dealing with trust relationships)
- Add a new fast in-memory cache to speed up lookups of cached data on
  repeated requests

* Thu May 03 2012 Stephen Gallagher <sgallagh@redhat.com> - 1.8.3-11
- New upstream release 1.8.3
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.8.3
- Numerous manpage and translation updates
- LDAP: Handle situations where the RootDSE isn't available anonymously
- LDAP: Fix regression for users using non-standard LDAP attributes for user
  information

* Mon Apr 09 2012 Stephen Gallagher <sgallagh@redhat.com> - 1.8.2-10
- New upstream release 1.8.2
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.8.2
- Several fixes to case-insensitive domain functions
- Fix for GSSAPI binds when the keytab contains unrelated principals
- Fixed several segfaults
- Workarounds added for LDAP servers with unreadable RootDSE
- SSH knownhostproxy will no longer enter an infinite loop preventing login
- The provided SYSV init script now starts SSSD earlier at startup and stops
  it later during shutdown
- Assorted minor fixes for issues discovered by static analysis tools

* Mon Mar 26 2012 Stephen Gallagher <sgallagh@redhat.com> - 1.8.1-9
- Don't duplicate libsss_autofs.so in two packages
- Set explicit package contents instead of globbing

* Wed Mar 21 2012 Stephen Gallagher <sgallagh@redhat.com> - 1.8.1-8
- Fix uninitialized value bug causing crashes throughout the code
- Resolves: rhbz#804783 - [abrt] Segfault during LDAP 'services' lookup

* Mon Mar 12 2012 Stephen Gallagher <sgallagh@redhat.com> - 1.8.1-7
- New upstream release 1.8.1
- Resolve issue where we could enter an infinite loop trying to connect to an
  auth server
- Fix serious issue with complex (3+ levels) nested groups
- Fix netgroup support for case-insensitivity and aliases
- Fix serious issue with lookup bundling resulting in requests never
  completing
- IPA provider will now check the value of nsAccountLock during pam_acct_mgmt
  in addition to pam_authenticate
- Fix several regressions in the proxy provider
- Resolves: rhbz#743133 - Performance regression with Kerberos authentication
                          against AD
- Resolves: rhbz#799031 - --debug option for sss_debuglevel doesn't work

* Tue Feb 28 2012 Stephen Gallagher <sgallagh@redhat.com> - 1.8.0-6
- New upstream release 1.8.0
- Support for the service map in NSS
- Support for setting default SELinux user context from FreeIPA
- Support for retrieving SSH user and host keys from LDAP (Experimental)
- Support for caching autofs LDAP requests (Experimental)
- Support for caching SUDO rules (Experimental)
- Include the IPA AutoFS provider
- Fixed several memory-corruption bugs
- Fixed a regression in group enumeration since 1.7.0
- Fixed a regression in the proxy provider
- Resolves: rhbz#741981 - Separate Cache Timeouts for SSSD
- Resolves: rhbz#797968 - sssd_be: The requested tar get is not configured is
                          logged at each login
- Resolves: rhbz#754114 - [abrt] sssd-1.6.3-1.fc16: ping_check: Process
                          /usr/sbin/sssd was killed by signal 11 (SIGSEGV)
- Resolves: rhbz#743133 - Performance regression with Kerberos authentication
                          against AD
- Resolves: rhbz#773706 - SSSD fails during autodetection of search bases for
                          new LDAP features
- Resolves: rhbz#786957 - sssd and kerberos should change the default location for create the Credential Cashes to /run/usr/USERNAME/krb5cc

* Wed Feb 22 2012 Stephen Gallagher <sgallagh@redhat.com> - 1.8.0-5.beta3
- Change default kerberos credential cache location to /run/user/<username>

* Wed Feb 15 2012 Stephen Gallagher <sgallagh@redhat.com> - 1.8.0-4.beta3
- New upstream release 1.8.0 beta 3
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.8.0beta3
- Fixed a regression in group enumeration since 1.7.0
- Fixed several memory-corruption bugs
- Finalized the ABI for the autofs support
- Fixed a regression in the proxy provider

* Fri Feb 10 2012 Petr Pisar <ppisar@redhat.com> - 1.8.0-3.beta2
- Rebuild against PCRE 8.30

* Mon Feb 06 2012 Stephen Gallagher <sgallagh@redhat.com> - 1.8.0-1.beta2
- New upstream release
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.8.0beta2
- Fix two minor manpage bugs
- Include the IPA AutoFS provider

* Mon Feb 06 2012 Stephen Gallagher <sgallagh@redhat.com> - 1.8.0-1.beta1
- New upstream release
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.8.0beta1
- Support for the service map in NSS
- Support for setting default SELinux user context from FreeIPA
- Support for retrieving SSH user and host keys from LDAP (Experimental)
- Support for caching autofs LDAP requests (Experimental)
- Support for caching SUDO rules (Experimental)

* Wed Feb 01 2012 Stephen Gallagher <sgallagh@redhat.com> - 1.7.0-5
- Resolves: rhbz#773706 - SSSD fails during autodetection of search bases for
                          new LDAP features - fix netgroups and sudo as well

* Wed Feb 01 2012 Stephen Gallagher <sgallagh@redhat.com> - 1.7.0-4
- Fixes a serious memory hierarchy bug causing unpredictable behavior in the
  LDAP provider.

* Wed Feb 01 2012 Stephen Gallagher <sgallagh@redhat.com> - 1.7.0-3
- Resolves: rhbz#773706 - SSSD fails during autodetection of search bases for
                          new LDAP features

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 22 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.7.0-1
- New upstream release 1.7.0
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.7.0
- Support for case-insensitive domains
- Support for multiple search bases in the LDAP provider
- Support for the native FreeIPA netgroup implementation
- Reliability improvements to the process monitor
- New DEBUG facility with more consistent log levels
- New tool to change debug log levels without restarting SSSD
- SSSD will now disconnect from LDAP server when idle
- FreeIPA HBAC rules can choose to ignore srchost options for significant
  performance gains
- Assorted performance improvements in the LDAP provider

* Mon Dec 19 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.6.4-1
- New upstream release 1.6.4
- Rolls up previous patches applied to the 1.6.3 tarball
- Fixes a rare issue causing crashes in the failover logic
- Fixes an issue where SSSD would return the wrong PAM error code for users
  that it does not recognize.

* Wed Dec 07 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.6.3-5
- Rebuild against libldb 1.1.4

* Tue Nov 29 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.6.3-4
- Resolves: rhbz#753639 - sssd_nss crashes when passed invalid UTF-8 for the
                          username in getpwnam()
- Resolves: rhbz#758425 - LDAP failover not working if server refuses
                          connections

* Thu Nov 24 2011 Jakub Hrozek <jhrozek@redhat.com> - 1.6.3-3
- Rebuild for libldb 1.1.3

* Thu Nov 10 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.6.3-2
- Resolves: rhbz#752495 - Crash when apply settings

* Fri Nov 04 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.6.3-1
- New upstream release 1.6.3
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.6.3
- Fixes a major cache performance issue introduced in 1.6.2
- Fixes a potential infinite-loop with certain LDAP layouts

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-5
- Rebuilt for glibc bug#747377

* Sun Oct 23 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.6.2-4
- Change selinux policy requirement to Conflicts: with the old version,
  rather than Requires: the supported version.

* Fri Oct 21 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.6.2-3
- Add explicit requirement on selinux-policy version to address new SBUS
  symlinks.

* Wed Oct 19 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.6.2-2
- Remove %%files reference to sss_debuglevel copied from wrong upstreeam
  spec file.

* Tue Oct 18 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.6.2-1
- Improved handling of users and groups with multi-valued name attributes
  (aliases)
- Performance enhancements
    Initgroups on RFC2307bis/FreeIPA
    HBAC rule processing
- Improved process-hang detection and restarting
- Enabled the midpoint cache refresh by default (fewer cache misses on
  commonly-used entries)
- Cleaned up the example configuration
- New tool to change debug level on the fly

* Mon Aug 29 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.6.1-1
- New upstream release 1.6.1
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.6.1
- Fixes a serious issue with LDAP connections when the communication is
  dropped (e.g. VPN disconnection, waking from sleep)
- SSSD is now less strict when dealing with users/groups with multiple names
  when a definitive primary name cannot be determined
- The LDAP provider will no longer attempt to canonicalize by default when
  using SASL. An option to re-enable this has been provided.
- Fixes for non-standard LDAP attribute names (e.g. those used by Active
  Directory)
- Three HBAC regressions have been fixed.
- Fix for an infinite loop in the deref code

* Wed Aug 03 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.6.0-2
- Build with _hardened_build macro

* Wed Aug 03 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.6.0-1
- New upstream release 1.6.0
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.6.0
- Add host access control support for LDAP (similar to pam_host_attr)
- Finer-grained control on principals used with Kerberos (such as for FAST or
- validation)
- Added a new tool sss_cache to allow selective expiring of cached entries
- Added support for LDAP DEREF and ASQ controls
- Added access control features for Novell Directory Server
- FreeIPA dynamic DNS update now checks first to see if an update is needed
- Complete rewrite of the HBAC library
- New libraries: libipa_hbac and libipa_hbac-python

* Tue Jul 05 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.5.11-2
- New upstream release 1.5.11
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.5.11
- Fix a serious regression that prevented SSSD from working with ldaps:// URIs
- IPA Provider: Fix a bug with dynamic DNS that resulted in the wrong IPv6
- address being saved to the AAAA record

* Fri Jul 01 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.5.10-1
- New upstream release 1.5.10
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.5.10
- Fixed a regression introduced in 1.5.9 that could result in blocking calls
- to LDAP

* Thu Jun 30 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.5.9-1
- New upstream release 1.5.9
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.5.9
- Support for overriding home directory, shell and primary GID locally
- Properly honor TTL values from SRV record lookups
- Support non-POSIX groups in nested group chains (for RFC2307bis LDAP
- servers)
- Properly escape IPv6 addresses in the failover code
- Do not crash if inotify fails (e.g. resource exhaustion)
- Don't add multiple TGT renewal callbacks (too many log messages)

* Fri May 27 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.5.8-1
- New upstream release 1.5.8
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.5.8
- Support for the LDAP paging control
- Support for multiple DNS servers for name resolution
- Fixes for several group membership bugs
- Fixes for rare crash bugs

* Mon May 23 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.5.7-3
- Resolves: rhbz#706740 - Orphaned links on rc0.d-rc6.d
- Make sure to properly convert to systemd if upgrading from newer
- updates for Fedora 14

* Mon May 02 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.5.7-2
- Fix segfault in TGT renewal

* Fri Apr 29 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.5.7-1
- Resolves: rhbz#700891 - CVE-2011-1758 sssd: automatic TGT renewal overwrites
-                         cached password with predicatable filename

* Wed Apr 20 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.5.6.1-1
- Re-add manpage translations

* Wed Apr 20 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.5.6-1
- New upstream release 1.5.6
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.5.6
- Fixed a serious memory leak in the memberOf plugin
- Fixed a regression with the negative cache that caused it to be essentially
- nonfunctional
- Fixed an issue where the user's full name would sometimes be removed from
- the cache
- Fixed an issue with password changes in the kerberos provider not working
- with kpasswd

* Wed Apr 20 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.5.5-5
- Resolves: rhbz#697057 - kpasswd fails when using sssd and
-                         kadmin server != kdc server
- Upgrades from SysV should now maintain enabled/disabled status

* Mon Apr 18 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.5.5-4
- Fix %%postun

* Thu Apr 14 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.5.5-3
- Fix systemd conversion. Upgrades from SysV to systemd weren't properly
- enabling the systemd service.
- Fix a serious memory leak in the memberOf plugin
- Fix an issue where the user's full name would sometimes be removed
- from the cache

* Tue Apr 12 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.5.5-2
- Install systemd unit file instead of sysv init script

* Tue Apr 12 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.5.5-1
- New upstream release 1.5.5
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.5.5
- Fixes for several crash bugs
- LDAP group lookups will no longer abort if there is a zero-length member
- attribute
- Add automatic fallback to 'cn' if the 'gecos' attribute does not exist

* Thu Mar 24 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.5.4-1
- New upstream release 1.5.4
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.5.4
- Fixes for Active Directory when not all users and groups have POSIX attributes
- Fixes for handling users and groups that have name aliases (aliases are ignored)
- Fix group memberships after initgroups in the IPA provider

* Thu Mar 17 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.5.3-2
- Resolves: rhbz#683267 - sssd 1.5.1-9 breaks AD authentication

* Fri Mar 11 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.5.3-1
- New upstream release 1.5.3
- Support for libldb >= 1.0.0

* Thu Mar 10 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.5.2-1
- New upstream release 1.5.2
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.5.2
- Fixes for support of FreeIPA v2
- Fixes for failover if DNS entries change
- Improved sss_obfuscate tool with better interactive mode
- Fix several crash bugs
- Don't attempt to use START_TLS over SSL. Some LDAP servers can't handle this
- Delete users from the local cache if initgroups calls return 'no such user'
- (previously only worked for getpwnam/getpwuid)
- Use new Transifex.net translations
- Better support for automatic TGT renewal (now survives restart)
- Netgroup fixes

* Sun Feb 27 2011 Simo Sorce <ssorce@redhat.com> - 1.5.1-9
- Rebuild sssd against libldb 1.0.2 so the memberof module loads again.
- Related: rhbz#677425

* Mon Feb 21 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.5.1-8
- Resolves: rhbz#677768 - name service caches names, so id command shows
-                         recently deleted users

* Fri Feb 11 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.5.1-7
- Ensure that SSSD builds against libldb-1.0.0 on F15 and later
- Remove .la for memberOf

* Fri Feb 11 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.5.1-6
- Fix memberOf install path

* Fri Feb 11 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.5.1-5
- Add support for libldb 1.0.0

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb 01 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.5.1-3
- Fix nested group member filter sanitization for RFC2307bis
- Put translated tool manpages into the sssd-tools subpackage

* Thu Jan 27 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.5.1-2
- Restore Requires: cyrus-sasl-gssapi as it is not auto-detected during
- rpmbuild

* Thu Jan 27 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.5.1-1
- New upstream release 1.5.1
- Addresses CVE-2010-4341 - DoS in sssd PAM responder can prevent logins
- Vast performance improvements when enumerate = true
- All PAM actions will now perform a forced initgroups lookup instead of just
- a user information lookup
-   This guarantees that all group information is available to other
-   providers, such as the simple provider.
- For backwards-compatibility, DNS lookups will also fall back to trying the
- SSSD domain name as a DNS discovery domain.
- Support for more password expiration policies in LDAP
-    389 Directory Server
-    FreeIPA
-    ActiveDirectory
- Support for ldap_tls_{cert,key,cipher_suite} config options
-Assorted bugfixes

* Tue Jan 11 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.5.0-2
- CVE-2010-4341 - DoS in sssd PAM responder can prevent logins

* Wed Dec 22 2010 Stephen Gallagher <sgallagh@redhat.com> - 1.5.0-1
- New upstream release 1.5.0
- Fixed issues with LDAP search filters that needed to be escaped
- Add Kerberos FAST support on platforms that support it
- Reduced verbosity of PAM_TEXT_INFO messages for cached credentials
- Added a Kerberos access provider to honor .k5login
- Addressed several thread-safety issues in the sss_client code
- Improved support for delayed online Kerberos auth
- Significantly reduced time between connecting to the network/VPN and
- acquiring a TGT
- Added feature for automatic Kerberos ticket renewal
- Provides the kerberos ticket for long-lived processes or cron jobs
- even when the user logs out
- Added several new features to the LDAP access provider
- Support for 'shadow' access control
- Support for authorizedService access control
- Ability to mix-and-match LDAP access control features
- Added an option for a separate password-change LDAP server for those
- platforms where LDAP referrals are not supported
- Added support for manpage translations


* Thu Nov 18 2010 Stephen Gallagher <sgallagh@redhat.com> - 1.4.1-3
- Solve a shutdown race-condition that sometimes left processes running
- Resolves: rhbz#606887 - SSSD stops on upgrade

* Tue Nov 16 2010 Stephen Gallagher <sgallagh@redhat.com> - 1.4.1-2
- Log startup errors to the syslog
- Allow cache cleanup to be disabled in sssd.conf

* Mon Nov 01 2010 Stephen Gallagher <sgallagh@redhat.com> - 1.4.1-1
- New upstream release 1.4.1
- Add support for netgroups to the proxy provider
- Fixes a minor bug with UIDs/GIDs >= 2^31
- Fixes a segfault in the kerberos provider
- Fixes a segfault in the NSS responder if a data provider crashes
- Correctly use sdap_netgroup_search_base

* Mon Oct 18 2010 Stephen Gallagher <sgallagh@redhat.com> - 1.4.0-2
- Fix incorrect tarball URL

* Mon Oct 18 2010 Stephen Gallagher <sgallagh@redhat.com> - 1.4.0-1
- New upstream release 1.4.0
- Added support for netgroups to the LDAP provider
- Performance improvements made to group processing of RFC2307 LDAP servers
- Fixed nested group issues with RFC2307bis LDAP servers without a memberOf plugin
- Build-system improvements to support Gentoo
- Split out several libraries into the ding-libs tarball
- Manpage reviewed and updated

* Mon Oct 04 2010 Stephen Gallagher <sgallagh@redhat.com> - 1.3.0-35
- Fix pre and post script requirements

* Mon Oct 04 2010 Stephen Gallagher <sgallagh@redhat.com> - 1.3.0-34
- Resolves: rhbz#606887 - sssd stops on upgrade

* Fri Oct 01 2010 Stephen Gallagher <sgallagh@redhat.com> - 1.3.0-33
- Resolves: rhbz#626205 - Unable to unlock screen

* Tue Sep 28 2010 Stephen Gallagher <sgallagh@redhat.com> - 1.3.0-32
- Resolves: rhbz#637955 - libini_config-devel needs libcollection-devel but
-                         doesn't require it

* Thu Sep 16 2010 Stephen Gallagher <sgallagh@redhat.com> - 1.3.0-31
- Resolves: rhbz#632615 - the krb5 locator plugin isn't packaged for multilib

* Tue Aug 24 2010 Stephen Gallagher <sgallagh@redhat.com> - 1.3.0-30
- Resolves: CVE-2010-2940 - sssd allows null password entry to authenticate
-                           against LDAP

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 1.2.91-21
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Jul 09 2010 Stephen Gallagher <sgallagh@redhat.com> - 1.2.91-20
- New upstream version 1.2.91 (1.3.0rc1)
- Improved LDAP failover
- Synchronous sysdb API (provides performance enhancements)
- Better online reconnection detection

* Mon Jun 21 2010 Stephen Gallagher <sgallagh@redhat.com> - 1.2.1-15
- New stable upstream version 1.2.1
- Resolves: rhbz#595529 - spec file should eschew %%define in favor of
-                         %%global
- Resolves: rhbz#593644 - Empty list of simple_allow_users causes sssd service
-                         to fail while restart.
- Resolves: rhbz#599026 - Makefile typo causes SSSD not to use the kernel
-                         keyring
- Resolves: rhbz#599724 - sssd is broken on Rawhide

* Mon May 24 2010 Stephen Gallagher <sgallagh@redhat.com> - 1.2.0-12
- New stable upstream version 1.2.0
- Support ServiceGroups for FreeIPA v2 HBAC rules
- Fix long-standing issue with auth_provider = proxy
- Better logging for TLS issues in LDAP

* Tue May 18 2010 Stephen Gallagher <sgallagh@redhat.com> - 1.1.92-11
- New LDAP access provider allows for filtering user access by LDAP attribute
- Reduced default timeout for detecting offline status with LDAP
- GSSAPI ticket lifetime made configurable
- Better offline->online transition support in Kerberos

* Fri May 07 2010 Stephen Gallagher <sgallagh@redhat.com> - 1.1.91-10
- Release new upstream version 1.1.91
- Enhancements when using SSSD with FreeIPA v2
- Support for deferred kinit
- Support for DNS SRV records for failover

* Fri Apr 02 2010 Simo Sorce <ssorce@redhat.com> - 1.1.1-3
- Bump up release number to avoid library sub-packages version issues with
  previous releases.

* Thu Apr 01 2010 Stephen Gallagher <sgallagh@redhat.com> - 1.1.1-1
- New upstream release 1.1.1
- Fixed the IPA provider (which was segfaulting at start)
- Fixed a bug in the SSSDConfig API causing some options to revert to
- their defaults
- This impacted the Authconfig UI
- Ensure that SASL binds to LDAP auto-retry when interrupted by a signal

* Tue Mar 23 2010 Stephen Gallagher <sgallagh@redhat.com> - 1.1.0-2
- Release SSSD 1.1.0 final
- Fix two potential segfaults
- Fix memory leak in monitor
- Better error message for unusable confdb

* Wed Mar 17 2010 Stephen Gallagher <sgallagh@redhat.com> - 1.1.0-1.pre20100317git0ea7f19
- Release candidate for SSSD 1.1
- Add simple access provider
- Create subpackages for libcollection, libini_config, libdhash and librefarray
- Support IPv6
- Support LDAP referrals
- Fix cache issues
- Better feedback from PAM when offline

* Wed Feb 24 2010 Stephen Gallagehr <sgallagh@redhat.com> - 1.0.5-2
- Rebuild against new libtevent

* Fri Feb 19 2010 Stephen Gallagher <sgallagh@redhat.com> - 1.0.5-1
- Fix licenses in sources and on RPMs

* Mon Jan 25 2010 Stephen Gallagher <sgallagh@redhat.com> - 1.0.4-1
- Fix regression on 64-bit platforms

* Fri Jan 22 2010 Stephen Gallagher <sgallagh@redhat.com> - 1.0.3-1
- Fixes link error on platforms that do not do implicit linking
- Fixes double-free segfault in PAM
- Fixes double-free error in async resolver
- Fixes support for TCP-based DNS lookups in async resolver
- Fixes memory alignment issues on ARM processors
- Manpage fixes

* Thu Jan 14 2010 Stephen Gallagher <sgallagh@redhat.com> - 1.0.2-1
- Fixes a bug in the failover code that prevented the SSSD from detecting when it went back online
- Fixes a bug causing long (sometimes multiple-minute) waits for NSS requests
- Several segfault bugfixes

* Mon Jan 11 2010 Stephen Gallagher <sgallagh@redhat.com> - 1.0.1-1
- Fix CVE-2010-0014

* Mon Dec 21 2009 Stephen Gallagher <sgallagh@redhat.com> - 1.0.0-2
- Patch SSSDConfig API to address
- https://bugzilla.redhat.com/show_bug.cgi?id=549482

* Fri Dec 18 2009 Stephen Gallagher <sgallagh@redhat.com> - 1.0.0-1
- New upstream stable release 1.0.0

* Fri Dec 11 2009 Stephen Gallagher <sgallagh@redhat.com> - 0.99.1-1
- New upstream bugfix release 0.99.1

* Mon Nov 30 2009 Stephen Gallagher <sgallagh@redhat.com> - 0.99.0-1
- New upstream release 0.99.0

* Tue Oct 27 2009 Stephen Gallagher <sgallagh@redhat.com> - 0.7.1-1
- Fix segfault in sssd_pam when cache_credentials was enabled
- Update the sample configuration
- Fix upgrade issues caused by data provider service removal

* Mon Oct 26 2009 Stephen Gallagher <sgallagh@redhat.com> - 0.7.0-2
- Fix upgrade issues from old (pre-0.5.0) releases of SSSD

* Fri Oct 23 2009 Stephen Gallagher <sgallagh@redhat.com> - 0.7.0-1
- New upstream release 0.7.0

* Thu Oct 15 2009 Stephen Gallagher <sgallagh@redhat.com> - 0.6.1-2
- Fix missing file permissions for sssd-clients

* Tue Oct 13 2009 Stephen Gallagher <sgallagh@redhat.com> - 0.6.1-1
- Add SSSDConfig API
- Update polish translation for 0.6.0
- Fix long timeout on ldap operation
- Make dp requests more robust

* Tue Sep 29 2009 Stephen Gallagher <sgallagh@redhat.com> - 0.6.0-1
- Ensure that the configuration upgrade script always writes the config
  file with 0600 permissions
- Eliminate an infinite loop in group enumerations

* Mon Sep 28 2009 Sumit Bose <sbose@redhat.com> - 0.6.0-0
- New upstream release 0.6.0

* Mon Aug 24 2009 Simo Sorce <ssorce@redhat.com> - 0.5.0-0
- New upstream release 0.5.0

* Wed Jul 29 2009 Jakub Hrozek <jhrozek@redhat.com> - 0.4.1-4
- Fix for CVE-2009-2410 - Native SSSD users with no password set could log in
  without a password. (Patch by Stephen Gallagher)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 22 2009 Simo Sorce <ssorce@redhat.com> - 0.4.1-2
- Fix a couple of segfaults that may happen on reload

* Thu Jun 11 2009 Simo Sorce <ssorce@redhat.com> - 0.4.1-1
- add missing configure check that broke stopping the daemon
- also fix default config to add a missing required option

* Mon Jun  8 2009 Simo Sorce <ssorce@redhat.com> - 0.4.1-0
- latest upstream release.
- also add a patch that fixes debugging output (potential segfault)

* Mon Apr 20 2009 Simo Sorce <ssorce@redhat.com> - 0.3.2-2
- release out of the official 0.3.2 tarball

* Mon Apr 20 2009 Jakub Hrozek <jhrozek@redhat.com> - 0.3.2-1
- bugfix release 0.3.2
- includes previous release patches
- change permissions of the /etc/sssd/sssd.conf to 0600

* Tue Apr 14 2009 Simo Sorce <ssorce@redhat.com> - 0.3.1-2
- Add last minute bug fixes, found in testing the package

* Mon Apr 13 2009 Simo Sorce <ssorce@redhat.com> - 0.3.1-1
- Version 0.3.1
- includes previous release patches

* Mon Apr 13 2009 Simo Sorce <ssorce@redhat.com> - 0.3.0-2
- Try to fix build adding automake as an explicit BuildRequire
- Add also a couple of last minute patches from upstream

* Mon Apr 13 2009 Simo Sorce <ssorce@redhat.com> - 0.3.0-1
- Version 0.3.0
- Provides file based configuration and lots of improvements

* Tue Mar 10 2009 Simo Sorce <ssorce@redhat.com> - 0.2.1-1
- Version 0.2.1

* Tue Mar 10 2009 Simo Sorce <ssorce@redhat.com> - 0.2.0-1
- Version 0.2.0

* Sun Mar 08 2009 Jakub Hrozek <jhrozek@redhat.com> - 0.1.0-5.20090309git691c9b3
- package git snapshot

* Fri Mar 06 2009 Jakub Hrozek <jhrozek@redhat.com> - 0.1.0-4
- fixed items found during review
- added initscript

* Thu Mar 05 2009 Sumit Bose <sbose@redhat.com> - 0.1.0-3
- added sss_client

* Mon Feb 23 2009 Jakub Hrozek <jhrozek@redhat.com> - 0.1.0-2
- Small cleanup and fixes in the spec file

* Thu Feb 12 2009 Stephen Gallagher <sgallagh@redhat.com> - 0.1.0-1
- Initial release (based on version 0.1.0 upstream code)
