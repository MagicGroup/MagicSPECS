%global WITH_LDAP 1
%global WITH_DIRSRV 1
# These next two *will* change.
%global WITH_OPENSSL 1
%global WITH_NSS 0
%global WITH_SYSVERTO 1
%global gettext_domain mit-krb5

Summary: The Kerberos network authentication system
Name: krb5
Version: 1.10.1
Release: 3%{?dist}
# Maybe we should explode from the now-available-to-everybody tarball instead?
# http://web.mit.edu/kerberos/dist/krb5/1.10/krb5-1.10.1-signed.tar
Source0: krb5-%{version}.tar.gz
Source1: krb5-%{version}.tar.gz.asc
Source2: kprop.service
Source4: kadmin.service
Source5: krb5kdc.service
Source6: krb5.conf
Source10: kdc.conf
Source11: kadm5.acl
Source19: krb5kdc.sysconfig
Source20: kadmin.sysconfig
# The same source files we "check", generated with "krb5-tex-pdf.sh create"
# and tarred up.
Source23: krb5-%{version}-pdf.tar.xz
Source24: krb5-tex-pdf.sh
Source25: krb5-1.10-manpaths.txt
Source29: ksu.pamd
Source30: kerberos-iv.portreserve
Source31: kerberos-adm.portreserve
Source32: krb5_prop.portreserve
Source33: krb5kdc.logrotate
Source34: kadmind.logrotate
Source35: kdb_check_weak.c

Patch5: krb5-1.10-ksu-access.patch
Patch6: krb5-1.10-ksu-path.patch
Patch12: krb5-1.7-ktany.patch
Patch16: krb5-1.10-buildconf.patch
Patch23: krb5-1.3.1-dns.patch
Patch29: krb5-1.10-kprop-mktemp.patch
Patch30: krb5-1.3.4-send-pr-tempfile.patch
Patch39: krb5-1.8-api.patch
Patch56: krb5-1.10-doublelog.patch
Patch59: krb5-1.10-kpasswd_tcp.patch
Patch60: krb5-1.10-pam.patch
Patch61: krb5-1.10-manpaths.patch
Patch63: krb5-1.10-selinux-label.patch
Patch71: krb5-1.9-dirsrv-accountlock.patch
Patch75: krb5-pkinit-debug.patch
Patch86: krb5-1.9-debuginfo.patch
Patch100: krb5-trunk-7046.patch
Patch101: krb5-trunk-7047.patch
Patch102: krb5-trunk-7048.patch
Patch103: krb5-1.10-gcc47.patch
Patch105: krb5-kvno-230379.patch

License: MIT
URL: http://web.mit.edu/kerberos/www/
Group: System Environment/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: autoconf, bison, flex, gawk, gettext
%if 0%{?fedora} >= 12 || 0%{?rhel} >= 6
BuildRequires: libcom_err-devel, libss-devel
%endif
BuildRequires: gzip, ncurses-devel, texinfo, texinfo-tex, tar
BuildRequires: texlive-latex
BuildRequires: keyutils-libs-devel
BuildRequires: pam-devel
BuildRequires: systemd-units
# For the test framework.
BuildRequires: perl, dejagnu, tcl-devel

%if %{WITH_LDAP}
BuildRequires: openldap-devel
%endif
%if %{WITH_OPENSSL} || %{WITH_NSS}
BuildRequires: openssl-devel >= 0.9.8
%endif
%if %{WITH_NSS}
BuildRequires: nss-devel >= 3.13
%endif
%if %{WITH_SYSVERTO}
BuildRequires: libverto-devel
%endif

%description
Kerberos V5 is a trusted-third-party network authentication system,
which can improve your network's security by eliminating the insecure
practice of sending passwords over the network in unencrypted form.

%package devel
Summary: Development files needed to compile Kerberos 5 programs
Group: Development/Libraries
Requires: %{name}-libs = %{version}-%{release}
%if 0%{?fedora} >= 12 || 0%{?rhel} >= 6
Requires: libcom_err-devel
%endif
Requires: keyutils-libs-devel

%description devel
Kerberos is a network authentication system. The krb5-devel package
contains the header files and libraries needed for compiling Kerberos
5 programs. If you want to develop Kerberos-aware programs, you need
to install this package.

%package libs
Summary: The shared libraries used by Kerberos 5
Group: System Environment/Libraries

%description libs
Kerberos is a network authentication system. The krb5-libs package
contains the shared libraries needed by Kerberos 5. If you are using
Kerberos, you need to install this package.

%package server
Group: System Environment/Daemons
Summary: The KDC and related programs for Kerberos 5
Requires: %{name}-libs = %{version}-%{release}
Requires(post): /usr/sbin/install-info
Requires(post): systemd-sysv
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
# we need 'status -l' to work, and that option was added in 8.99
Requires: initscripts >= 8.99-1
# we drop files in its directory, but we don't want to own that directory
Requires: logrotate
Requires(preun): /usr/sbin/install-info
# mktemp is used by krb5-send-pr
Requires: coreutils
# portreserve is used by init scripts for kadmind, kpropd, and krb5kdc
Requires: portreserve
%if %{WITH_SYSVERTO}
# for run-time, and for parts of the test suite
BuildRequires: libverto-module-base
Requires: libverto-module-base
%endif

%description server
Kerberos is a network authentication system. The krb5-server package
contains the programs that must be installed on a Kerberos 5 key
distribution center (KDC).  If you are installing a Kerberos 5 KDC,
you need to install this package (in other words, most people should
NOT install this package).

%package server-ldap
Group: System Environment/Daemons
Summary: The LDAP storage plugin for the Kerberos 5 KDC
Requires: %{name}-server = %{version}-%{release}
Requires: %{name}-libs = %{version}-%{release}

%description server-ldap
Kerberos is a network authentication system. The krb5-server package
contains the programs that must be installed on a Kerberos 5 key
distribution center (KDC).  If you are installing a Kerberos 5 KDC,
and you wish to use a directory server to store the data for your
realm, you need to install this package.

%package workstation
Summary: Kerberos 5 programs for use on workstations
Group: System Environment/Base
Requires: %{name}-libs = %{version}-%{release}
Requires(post): /usr/sbin/install-info
Requires(preun): /usr/sbin/install-info
# mktemp is used by krb5-send-pr
Requires: coreutils

%description workstation
Kerberos is a network authentication system. The krb5-workstation
package contains the basic Kerberos programs (kinit, klist, kdestroy,
kpasswd). If your network uses Kerberos, this package should be
installed on every workstation.

%if 0%{?fedora} >= 17 || 0%{?rhel} >= 6
%package pkinit
%else
%package pkinit-openssl
%endif
Summary: The PKINIT module for Kerberos 5
Group: System Environment/Libraries
Requires: %{name}-libs = %{version}-%{release}
%if 0%{?fedora} >= 17 || 0%{?rhel} >= 6
Obsoletes: krb5-pkinit-openssl
Provides: krb5-pkinit-openssl = %{version}-%{release}
%endif

%if 0%{?fedora} >= 17 || 0%{?rhel} >= 6
%description pkinit
%else
%description pkinit-openssl
%endif
Kerberos is a network authentication system. The krb5-pkinit
package contains the PKINIT plugin, which allows clients
to obtain initial credentials from a KDC using a private key and a
certificate.

%prep
%setup -q -a 23 -n krb5-%{version}
ln -s NOTICE LICENSE

%patch60 -p1 -b .pam

%patch61 -p1 -b .manpaths

%patch63 -p1 -b .selinux-label

%patch5  -p1 -b .ksu-access
%patch6  -p1 -b .ksu-path
%patch12 -p1 -b .ktany
%patch16 -p1 -b .buildconf
%patch23 -p1 -b .dns
%patch29 -p1 -b .kprop-mktemp
%patch30 -p1 -b .send-pr-tempfile
%patch39 -p1 -b .api
%patch56 -p1 -b .doublelog
%patch59 -p1 -b .kpasswd_tcp
%patch71 -p1 -b .dirsrv-accountlock
#%patch75 -p1 -b .pkinit-debug
%patch86 -p0 -b .debuginfo
%patch100 -p1 -b .7046
%patch101 -p1 -b .7047
%patch102 -p1 -b .7048
%patch103 -p0 -b .gcc47
%patch105 -p1 -b .kvno
rm src/lib/krb5/krb/deltat.c

gzip doc/*.ps

sed -i -e '1s!\[twoside\]!!;s!%\(\\usepackage{hyperref}\)!\1!' doc/api/library.tex
sed -i -e '1c\
\\documentclass{article}\
\\usepackage{fixunder}\
\\usepackage{functions}\
\\usepackage{fancyheadings}\
\\usepackage{hyperref}' doc/implement/implement.tex

# Take the execute bit off of documentation.
chmod -x doc/krb5-protocol/*.txt doc/*.html doc/*/*.html

# Rename the man pages so that they'll get generated correctly.  Uses the
# "krb5-1.8-manpaths.txt" source file.
pushd src
cat %{SOURCE25} | while read manpage ; do
	mv "$manpage" "$manpage".in
done
popd

# Check that the PDFs we built earlier match this source tree, using the
# "krb5-tex-pdf.sh" source file.
sh %{SOURCE24} check << EOF
doc/api       library krb5
doc/implement implement
doc/kadm5     adb-unit-test
doc/kadm5     api-unit-test
doc/kadm5     api-funcspec
doc/kadm5     api-server-design
EOF

# Generate an FDS-compatible LDIF file.
inldif=src/plugins/kdb/ldap/libkdb_ldap/kerberos.ldif
cat > 60kerberos.ldif << EOF
# This is a variation on kerberos.ldif which 389 Directory Server will like.
dn: cn=schema
EOF
egrep -iv '(^$|^dn:|^changetype:|^add:)' $inldif | \
sed -r 's,^		,                ,g' | \
sed -r 's,^	,        ,g' >> 60kerberos.ldif
touch -r $inldif 60kerberos.ldif

# Rebuild the configure scripts.
pushd src
autoheader
autoconf
popd

%build
# Go ahead and supply tcl info, because configure doesn't know how to find it.
. %{_libdir}/tclConfig.sh
pushd src
# Work out the CFLAGS and CPPFLAGS which we intend to use.
INCLUDES=-I%{_includedir}/et
CFLAGS="`echo $RPM_OPT_FLAGS $DEFINES $INCLUDES -fPIC -fno-strict-aliasing -fstack-protector-all`"
CPPFLAGS="`echo $DEFINES $INCLUDES`"
%configure \
	CC="%{__cc}" \
	CFLAGS="$CFLAGS" \
	CPPFLAGS="$CPPFLAGS" \
%if 0%{?fedora} >= 7 || 0%{?rhel} >= 6
	SS_LIB="-lss" \
%else
	SS_LIB="-lss -lncurses" \
%endif
	--enable-shared \
	--localstatedir=%{_var}/kerberos \
	--disable-rpath \
	--with-system-et \
	--with-system-ss \
	--with-netlib=-lresolv \
	--with-tcl \
	--enable-dns-for-realm \
%if %{WITH_LDAP}
%if %{WITH_DIRSRV}
	--with-dirsrv \
%else
	--with-ldap \
%endif
%endif
%if %{WITH_OPENSSL} || %{WITH_NSS}
	--enable-pkinit \
%else
	--disable-pkinit \
%endif
%if %{WITH_OPENSSL}
	--with-pkinit-crypto-impl=openssl \
%endif
%if %{WITH_NSS}
	--with-crypto-impl=nss \
%endif
%if %{WITH_SYSVERTO}
	--with-system-verto \
%else
	--without-system-verto \
%endif
	--with-pam \
	--without-selinux
# Now build it.
make
popd

# A sanity checker for upgrades.
env LD_LIBRARY_PATH=`pwd`/src/lib \
%{__cc} -o kdb_check_weak \
	-I src/include `./src/krb5-config --cflags kdb` \
	%{SOURCE35} \
	-L src/lib `./src/krb5-config --libs kdb`

%if 0%{?with_check}
%check
# Run the test suite. We can't actually run the whole thing in the build system.
make -C src fake-install
: make -C src check TMPDIR=%{_tmppath}
make -C src/lib check TMPDIR=%{_tmppath}
make -C src/kdc check TMPDIR=%{_tmppath}
%endif

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

# Info docs.
mkdir -p $RPM_BUILD_ROOT%{_infodir}
install -m 644 doc/*.info* $RPM_BUILD_ROOT%{_infodir}/

# Unconditionally compress the info pages so that we know the right file name
# to pass to install-info in %%post.
gzip $RPM_BUILD_ROOT%{_infodir}/*.info*

# Sample KDC config files (bundled kdc.conf and kadm5.acl).
mkdir -p $RPM_BUILD_ROOT%{_var}/kerberos/krb5kdc
install -pm 600 %{SOURCE10} $RPM_BUILD_ROOT%{_var}/kerberos/krb5kdc/
install -pm 600 %{SOURCE11} $RPM_BUILD_ROOT%{_var}/kerberos/krb5kdc/

# Default configuration file for everything.
mkdir -p $RPM_BUILD_ROOT/etc
install -pm 644 %{SOURCE6} $RPM_BUILD_ROOT/etc/krb5.conf

# Server init scripts (krb5kdc,kadmind,kpropd) and their sysconfig files.
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
for init in \
	%{SOURCE5}\
	%{SOURCE4} \
	%{SOURCE2} ; do
	# In the past, the init script was supposed to be named after the
	# service that the started daemon provided.  Changing their names
	# is an upgrade-time problem I'm in no hurry to deal with.
	install -pm 644 ${init} $RPM_BUILD_ROOT%{_unitdir}
done
mkdir -p $RPM_BUILD_ROOT/etc/sysconfig
for sysconfig in \
	%{SOURCE19}\
	%{SOURCE20} ; do
	install -pm 644 ${sysconfig} \
	$RPM_BUILD_ROOT/etc/sysconfig/`basename ${sysconfig} .sysconfig`
done

# portreserve configuration files.
mkdir -p $RPM_BUILD_ROOT/etc/portreserve
for portreserve in \
	%{SOURCE30} \
	%{SOURCE31} \
	%{SOURCE32} ; do
	install -pm 644 ${portreserve} \
	$RPM_BUILD_ROOT/etc/portreserve/`basename ${portreserve} .portreserve`
done

# logrotate configuration files
mkdir -p $RPM_BUILD_ROOT/etc/logrotate.d/
for logrotate in \
	%{SOURCE33} \
	%{SOURCE34} ; do
	install -pm 644 ${logrotate} \
	$RPM_BUILD_ROOT/etc/logrotate.d/`basename ${logrotate} .logrotate`
done

# PAM configuration files.
mkdir -p $RPM_BUILD_ROOT/etc/pam.d/
for pam in \
	%{SOURCE29} ; do
	install -pm 644 ${pam} \
	$RPM_BUILD_ROOT/etc/pam.d/`basename ${pam} .pamd`
done

# Plug-in directories.
install -pdm 755 $RPM_BUILD_ROOT/%{_libdir}/krb5/plugins/preauth
install -pdm 755 $RPM_BUILD_ROOT/%{_libdir}/krb5/plugins/kdb
install -pdm 755 $RPM_BUILD_ROOT/%{_libdir}/krb5/plugins/authdata

# The rest of the binaries, headers, libraries, and docs.
make -C src DESTDIR=$RPM_BUILD_ROOT EXAMPLEDIR=%{_docdir}/krb5-libs-%{version}/examples install

# Munge krb5-config yet again.  This is totally wrong for 64-bit, but chunks
# of the buildconf patch already conspire to strip out /usr/<anything> from the
# list of link flags, and it helps prevent file conflicts on multilib systems.
sed -r -i -e 's|^libdir=/usr/lib(64)?$|libdir=/usr/lib|g' $RPM_BUILD_ROOT%{_bindir}/krb5-config

# Move specific libraries from %{_libdir} to /%{_lib}, and fixup the symlinks.
touch $RPM_BUILD_ROOT/rootfile
rellibdir=..
while ! test -r $RPM_BUILD_ROOT/%{_libdir}/${rellibdir}/rootfile ; do
	rellibdir=../${rellibdir}
done
rm -f $RPM_BUILD_ROOT/rootfile
#mkdir -p $RPM_BUILD_ROOT/%{_lib}
for library in libgssapi_krb5 libgssrpc libk5crypto libkrb5 libkrb5support ; do
#	mv $RPM_BUILD_ROOT/%{_libdir}/${library}.so.* $RPM_BUILD_ROOT/%{_lib}/
	pushd $RPM_BUILD_ROOT/%{_libdir}
	ln -fs ${library}.so.*.* ${library}.so
	popd
done

# A sanity checker for upgrades.
install -m 755 kdb_check_weak $RPM_BUILD_ROOT/%{_libdir}/krb5/

magic_rpm_clean.sh

%find_lang %{gettext_domain} || touch %{gettext_domain}.lang

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%post server-ldap -p /sbin/ldconfig

%postun server-ldap -p /sbin/ldconfig

%post server
if [ $1 -eq 1 ] ; then 
    # Initial installation 
    /usr/bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi
# Remove the init script for older servers.
[ -x /etc/rc.d/init.d/krb5server ] && /usr/sbin/chkconfig --del krb5server
# Install info pages.
/usr/sbin/install-info %{_infodir}/krb5-admin.info.gz %{_infodir}/dir
/usr/sbin/install-info %{_infodir}/krb5-install.info.gz %{_infodir}/dir
exit 0

%preun server
if [ "$1" -eq "0" ] ; then
	/usr/bin/systemctl --no-reload disable krb5kdc.service > /dev/null 2>&1 || :
	/usr/bin/systemctl --no-reload disable kadmin.service > /dev/null 2>&1 || :
	/usr/bin/systemctl --no-reload disable kprop.service > /dev/null 2>&1 || :
	/usr/bin/systemctl stop krb5kdc.service > /dev/null 2>&1 || :
	/usr/bin/systemctl stop kadmin.service > /dev/null 2>&1 || :
	/usr/bin/systemctl stop kprop.service > /dev/null 2>&1 || :
	/usr/sbin/install-info --delete %{_infodir}/krb5-admin.info.gz %{_infodir}/dir
	/usr/sbin/install-info --delete %{_infodir}/krb5-install.info.gz %{_infodir}/dir
fi
exit 0

%postun server
/usr/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
	/usr/bin/systemctl try-restart krb5kdc.service >/dev/null 2>&1 || :
	/usr/bin/systemctl try-restart kadmin.service >/dev/null 2>&1 || :
	/usr/bin/systemctl try-restart kprop.service >/dev/null 2>&1 || :
fi

%triggerun server -- krb5-server < 1.9.1-13
# Save the current service runlevel info
# User must manually run 
#  systemd-sysv-convert --apply krb5kdc
#  systemd-sysv-convert --apply kadmin
#  systemd-sysv-convert --apply kprop
# to migrate them to systemd targets
/usr/bin/systemd-sysv-convert --save krb5kdc >/dev/null 2>&1 ||:
/usr/bin/systemd-sysv-convert --save kadmin >/dev/null 2>&1 ||:
/usr/bin/systemd-sysv-convert --save kprop >/dev/null 2>&1 ||:

# Run these because the SysV package being removed won't do them
/usr/sbin/chkconfig --del krb5kdc >/dev/null 2>&1 || :
/usr/sbin/chkconfig --del kadmin >/dev/null 2>&1 || :
/usr/sbin/chkconfig --del kprop >/dev/null 2>&1 || :
/usr/bin/systemctl try-restart krb5kdc.service >/dev/null 2>&1 || :
/usr/bin/systemctl try-restart kadmin.service >/dev/null 2>&1 || :
/usr/bin/systemctl try-restart kprop.service >/dev/null 2>&1 || :

%triggerun server -- krb5-server < 1.6.3-100
if [ "$2" -eq "0" ] ; then
	/usr/sbin/install-info --delete %{_infodir}/krb425.info.gz %{_infodir}/dir
	/sbin/service krb524 stop > /dev/null 2>&1 || :
	/usr/sbin/chkconfig --del krb524 > /dev/null 2>&1 || :
fi
exit 0

%post workstation
/usr/sbin/install-info %{_infodir}/krb5-user.info.gz %{_infodir}/dir
exit 0

%preun workstation
if [ "$1" -eq "0" ] ; then
	/usr/sbin/install-info --delete %{_infodir}/krb5-user.info.gz %{_infodir}/dir
fi
exit 0

%files workstation
%defattr(-,root,root,-)
%doc doc/user*.ps.gz src/config-files/services.append
%doc doc/{kdestroy,kinit,klist,kpasswd,ksu}.html
%doc doc/krb5-user.html
%attr(0755,root,root) %doc src/config-files/convert-config-files
%{_infodir}/krb5-user.info*

# Clients of the KDC, including tools you're likely to need if you're running
# app servers other than those built from this source package.
%{_bindir}/kdestroy
%{_mandir}/man1/kdestroy.1*
%{_bindir}/kinit
%{_mandir}/man1/kinit.1*
%{_bindir}/klist
%{_mandir}/man1/klist.1*
%{_bindir}/kpasswd
%{_mandir}/man1/kpasswd.1*
%{_bindir}/kswitch
%{_mandir}/man1/kswitch.1*

%{_bindir}/kvno
%{_mandir}/man1/kvno.1*
%{_bindir}/kadmin
%{_mandir}/man1/kadmin.1*
%{_bindir}/k5srvutil
%{_mandir}/man1/k5srvutil.1*
%{_bindir}/ktutil
%{_mandir}/man1/ktutil.1*

# Doesn't really fit anywhere else.
%attr(4755,root,root) %{_bindir}/ksu
%{_mandir}/man1/ksu.1*
%config(noreplace) /etc/pam.d/ksu

# Problem-reporting tool.
%{_sbindir}/krb5-send-pr
%dir %{_datadir}/gnats
%{_datadir}/gnats/mit
%{_mandir}/man1/krb5-send-pr.1*

%files server
%defattr(-,root,root,-)
%docdir %{_mandir}

%{_unitdir}/krb5kdc.service
%{_unitdir}/kadmin.service
%{_unitdir}/kprop.service
%config(noreplace) /etc/sysconfig/krb5kdc
%config(noreplace) /etc/sysconfig/kadmin
%config(noreplace) /etc/portreserve/kerberos-iv
%config(noreplace) /etc/portreserve/kerberos-adm
%config(noreplace) /etc/portreserve/krb5_prop
%config(noreplace) /etc/logrotate.d/krb5kdc
%config(noreplace) /etc/logrotate.d/kadmind

%doc doc/admin*.ps.gz
%doc doc/install*.ps.gz
%doc doc/krb5-admin.html
%doc doc/krb5-install.html

%{_infodir}/krb5-admin.info*
%{_infodir}/krb5-install.info*

%dir %{_var}/kerberos
%dir %{_var}/kerberos/krb5kdc
%config(noreplace) %{_var}/kerberos/krb5kdc/kdc.conf
%config(noreplace) %{_var}/kerberos/krb5kdc/kadm5.acl

%dir %{_libdir}/krb5
%if ! %{WITH_SYSVERTO}
%{_libdir}/libverto-k5ev.so
%{_libdir}/libverto-k5ev.so.*
%endif
%{_libdir}/krb5/kdb_check_weak
%dir %{_libdir}/krb5/plugins
%dir %{_libdir}/krb5/plugins/kdb
%dir %{_libdir}/krb5/plugins/preauth
%dir %{_libdir}/krb5/plugins/authdata

# Problem-reporting tool.
%{_sbindir}/krb5-send-pr
%dir %{_datadir}/gnats
%{_datadir}/gnats/mit
%{_mandir}/man1/krb5-send-pr.1*

# KDC binaries and configuration.
%{_mandir}/man5/kdc.conf.5*
%{_sbindir}/kadmin.local
%{_mandir}/man8/kadmin.local.8*
%{_sbindir}/kadmind
%{_mandir}/man8/kadmind.8*
%{_sbindir}/kdb5_util
%{_mandir}/man8/kdb5_util.8*
%{_sbindir}/kprop
%{_mandir}/man8/kprop.8*
%{_sbindir}/kpropd
%{_mandir}/man8/kpropd.8*
%{_sbindir}/kproplog
%{_mandir}/man8/kproplog.8*
%{_sbindir}/krb5kdc
%{_mandir}/man8/krb5kdc.8*

# This is here for people who want to test their server, and also 
# included in devel package for similar reasons.
%{_bindir}/sclient
%{_mandir}/man1/sclient.1*
%{_sbindir}/sserver
%{_mandir}/man8/sserver.8*

%if %{WITH_LDAP}
%files server-ldap
%defattr(-,root,root,-)
%docdir %{_mandir}
%doc src/plugins/kdb/ldap/libkdb_ldap/kerberos.ldif
%doc src/plugins/kdb/ldap/libkdb_ldap/kerberos.schema
%doc 60kerberos.ldif
%dir %{_libdir}/krb5
%dir %{_libdir}/krb5/plugins
%dir %{_libdir}/krb5/plugins/kdb
%{_libdir}/krb5/plugins/kdb/kldap.so
%{_libdir}/libkdb_ldap.so
%{_libdir}/libkdb_ldap.so.*
%{_mandir}/man8/kdb5_ldap_util.8.gz
%{_sbindir}/kdb5_ldap_util
%endif

%files libs -f %{gettext_domain}.lang
%defattr(-,root,root,-)
%doc README NOTICE LICENSE
%docdir %{_mandir}
%verify(not md5 size mtime) %config(noreplace) /etc/krb5.conf
/%{_mandir}/man1/kerberos.1*
/%{_mandir}/man5/.k5identity.5*
/%{_mandir}/man5/.k5login.5*
/%{_mandir}/man5/k5identity.5*
/%{_mandir}/man5/k5login.5*
/%{_mandir}/man5/krb5.conf.5*
/%{_libdir}/libgssapi_krb5.so.*
/%{_libdir}/libgssrpc.so.*
/%{_libdir}/libk5crypto.so.*
%{_libdir}/libkadm5clnt_mit.so.*
%{_libdir}/libkadm5srv_mit.so.*
%{_libdir}/libkdb5.so.*
/%{_libdir}/libkrb5.so.*
/%{_libdir}/libkrb5support.so.*
%dir %{_libdir}/krb5
%dir %{_libdir}/krb5/plugins
%dir %{_libdir}/krb5/plugins/*
%{_libdir}/krb5/plugins/kdb/db2.so
%if ! %{WITH_SYSVERTO}
# These really shouldn't be here, but until we have a system copy of libverto,
# don't force people who are using libverto to install the KDC just to get the
# shared library.  Not that there are any development headers, but anyway.
%{_libdir}/libverto.so
%{_libdir}/libverto.so.*
%endif

%if 0%{?fedora} >= 17 || 0%{?rhel} >= 6
%files pkinit
%else
%files pkinit-openssl
%endif
%defattr(-,root,root,-)
%dir %{_libdir}/krb5
%dir %{_libdir}/krb5/plugins
%dir %{_libdir}/krb5/plugins/preauth
%{_libdir}/krb5/plugins/preauth/pkinit.so

%files devel
%defattr(-,root,root,-)
%docdir %{_mandir}
%doc doc/api/*.pdf
%doc doc/ccapi
%doc doc/implement/*.pdf
%doc doc/kadm5/*.pdf
%doc doc/kadmin
%doc doc/kim
%doc doc/krb5-protocol
%doc doc/rpc
%doc doc/threads.txt

%{_includedir}/*
%{_libdir}/libgssapi_krb5.so
%{_libdir}/libgssrpc.so
%{_libdir}/libk5crypto.so
%{_libdir}/libkadm5clnt.so
%{_libdir}/libkadm5clnt_mit.so
%{_libdir}/libkadm5srv.so
%{_libdir}/libkadm5srv_mit.so
%{_libdir}/libkdb5.so
%{_libdir}/libkrb5.so
%{_libdir}/libkrb5support.so

%{_bindir}/krb5-config
%{_bindir}/sclient
%{_mandir}/man1/krb5-config.1*
%{_mandir}/man1/sclient.1*
%{_mandir}/man8/sserver.8*
%{_sbindir}/sserver

# Protocol test clients.
%{_bindir}/sim_client
%{_bindir}/gss-client
%{_bindir}/uuclient

# Protocol test servers.
%{_sbindir}/sim_server
%{_sbindir}/gss-server
%{_sbindir}/uuserver

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.10.1-3
- 为 Magic 3.0 重建

* Tue Mar 20 2012 Nalin Dahyabhai <nalin@redhat.com> 1.10.1-2
- change back dns_lookup_kdc to the default setting (Stef Walter, #805318)
- comment out example.com examples in default krb5.conf (Stef Walter, #805320)

* Fri Mar  9 2012 Nalin Dahyabhai <nalin@redhat.com> 1.10.1-1
- update to 1.10.1
  - drop the KDC crash fix
  - drop the KDC lookaside cache fix
  - drop the fix for kadmind RPC ACLs (CVE-2012-1012)

* Wed Mar  7 2012 Nalin Dahyabhai <nalin@redhat.com> 1.10-5
- when removing -workstation, remove our files from the info index while
  the file is still there, in %%preun, rather than %%postun, and use the
  compressed file's name (#801035)

* Tue Feb 21 2012 Nathaniel McCallum <nathaniel@natemccallum.com> - 1.10-4
- Fix string RPC ACLs (RT#7093); CVE-2012-1012

* Tue Jan 31 2012 Nathaniel McCallum <nathaniel@natemccallum.com> - 1.10-3
- Add upstream lookaside cache behavior fix (RT#7082)

* Mon Jan 30 2012 Nalin Dahyabhai <nalin@redhat.com> 1.10-2
- add patch to accept keytab entries with vno==0 as matches when we're
  searching for an entry with a specific name/kvno (#230382/#782211,RT#3349)

* Mon Jan 30 2012 Nalin Dahyabhai <nalin@redhat.com> 1.10-1
- update to 1.10 final

* Thu Jan 26 2012 Nathaniel McCallum <nathaniel@natemccallum.com> - 1.10-0.beta1.2
- Add upstream crashfix patch (RT#7081)

* Thu Jan 12 2012 Nalin Dahyabhai <nalin@redhat.com> 1.10-0.beta1.1
- update to beta 1

* Wed Jan 11 2012 Peter Robinson <pbrobinson@gmail.com>
- mktemp was long obsoleted by coreutils

* Wed Jan  4 2012 Nalin Dahyabhai <nalin@redhat.com> 1.10-0.alpha2.2
- modify the deltat grammar to also tell gcc (4.7) to suppress
  "maybe-uninitialized" warnings in addition to the "uninitialized" warnings
  it's already being told to suppress (RT#7080)

* Tue Dec 20 2011 Nalin Dahyabhai <nalin@redhat.com> 1.10-0.alpha2.1
- update to alpha 2
- drop a couple of patches which were integrated for alpha 2

* Tue Dec 13 2011 Nalin Dahyabhai <nalin@redhat.com> 1.10-0.alpha1.3
- pull in patch for RT#7046: tag a ccache containing credentials obtained via
  S4U2Proxy with the principal name of the proxying principal (part of #761317)
  so that the default principal name can be set to that of the client for which
  it is proxying, which results in the ccache looking more normal to consumers
  of the ccache that don't care that there's proxying going on
- pull in patch for RT#7047: allow tickets obtained via S4U2Proxy to be cached
  (more of #761317)
- pull in patch for RT#7048: allow PAC verification to only bother trying to
  verify the signature with keys that it's given (still more of #761317)

* Tue Dec  6 2011 Nalin Dahyabhai <nalin@redhat.com> 1.10-0.alpha1.2
- apply upstream patch to fix a null pointer dereference when processing
  TGS requests (CVE-2011-1530, #753748)

* Wed Nov 30 2011 Nalin Dahyabhai <nalin@redhat.com> 1.10-0.alpha1.1
- correct a bug in the fix for #754001 so that the file creation context is
  consistently reset

* Tue Nov 15 2011 Nalin Dahyabhai <nalin@redhat.com> 1.10-0.alpha1.0
- update to 1.10 alpha 1
- on newer releases where we can assume NSS >= 3.13, configure PKINIT to build
  using NSS
- on newer releases where we build PKINIT using NSS, configure libk5crypto to
  build using NSS
- rename krb5-pkinit-openssl to krb5-pkinit on newer releases where we're
  expecting to build PKINIT using NSS instead
- during %%check, run check in the library and kdc subdirectories, which
  should be able to run inside of the build system without issue

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.1-19
- Rebuilt for glibc bug#747377

* Tue Oct 18 2011 Nalin Dahyabhai <nalin@redhat.com> 1.9.1-18
- apply upstream patch to fix a null pointer dereference with the LDAP kdb
  backend (CVE-2011-1527, #744125), an assertion failure with multiple kdb
  backends (CVE-2011-1528), and a null pointer dereference with multiple kdb
  backends (CVE-2011-1529) (#737711)

* Thu Oct 13 2011 Nalin Dahyabhai <nalin@redhat.com> 1.9.1-17
- pull in patch from trunk to rename krb5int_pac_sign() to krb5_pac_sign() and
  make it public (#745533)

* Fri Oct  7 2011 Nalin Dahyabhai <nalin@redhat.com> 1.9.1-16
- kadmin.service: fix #723723 again
- kadmin.service,krb5kdc.service: remove optional use of $KRB5REALM in command
  lines, because systemd parsing doesn't handle alternate value shell variable
  syntax
- kprop.service: add missing Type=forking so that systemd doesn't assume simple
- kprop.service: expect the ACL configuration to be there, not absent
- handle a harder-to-trigger assertion failure that starts cropping up when we
  exit the transmit loop on time (#739853)

* Sun Oct  2 2011 Tom Callaway <spot@fedoraproject.org> 1.9.1-15
- hardcode pid file as option in krb5kdc.service

* Fri Sep 30 2011 Tom Callaway <spot@fedoraproject.org> 1.9.1-14
- fix pid path in krb5kdc.service

* Mon Sep 19 2011 Tom Callaway <spot@fedoraproject.org> 1.9.1-13
- convert to systemd

* Tue Sep  6 2011 Nalin Dahyabhai <nalin@redhat.com> 1.9.1-12
- pull in upstream patch for RT#6952, confusion following referrals for
  cross-realm auth (#734341)
- pull in build-time deps for the tests

* Thu Sep  1 2011 Nalin Dahyabhai <nalin@redhat.com> 1.9.1-11
- switch to the upstream patch for #727829

* Wed Aug 31 2011 Nalin Dahyabhai <nalin@redhat.com> 1.9.1-10
- handle an assertion failure that starts cropping up when the patch for
  using poll (#701446) meets servers that aren't running KDCs or against
  which the connection fails for other reasons (#727829, #734172)

* Mon Aug  8 2011 Nalin Dahyabhai <nalin@redhat.com> 1.9.1-9
- override the default build rules to not delete temporary y.tab.c files,
  so that they can be packaged, allowing debuginfo files which point to them
  do so usefully (#729044)

* Fri Jul 22 2011 Nalin Dahyabhai <nalin@redhat.com> 1.9.1-8
- build shared libraries with partial RELRO support (#723995)
- filter out potentially multiple instances of -Wl,-z,relro from krb5-config
  output, now that it's in the buildroot's default LDFLAGS
- pull in a patch to fix losing track of the replay cache FD, from SVN by
  way of Kevin Coffman

* Wed Jul 20 2011 Nalin Dahyabhai <nalin@redhat.com> 1.9.1-7
- kadmind.init: drop the attempt to detect no-database-present errors (#723723),
  which is too fragile in cases where the database has been manually moved or
  is accessed through another kdb plugin

* Tue Jul 19 2011 Nalin Dahyabhai <nalin@redhat.com> 1.9.1-6
- backport fixes to teach libkrb5 to use descriptors higher than FD_SETSIZE
  to talk to a KDC by using poll() if it's detected at compile-time (#701446,
  RT#6905)

* Thu Jun 23 2011 Nalin Dahyabhai <nalin@redhat.com> 1.9.1-5
- pull a fix from SVN to try to avoid triggering a PTR lookup in getaddrinfo()
  during krb5_sname_to_principal(), and to let getaddrinfo() decide whether or
  not to ask for an IPv6 address based on the set of configured interfaces
  (#717378, RT#6922)
- pull a fix from SVN to use AI_ADDRCONFIG more often (RT#6923)

* Mon Jun 20 2011 Nalin Dahyabhai <nalin@redhat.com> 1.9.1-4
- apply upstream patch by way of Burt Holzman to fall back to a non-referral
  method in cases where we might be derailed by a KDC that rejects the
  canonicalize option (for example, those from the RHEL 2.1 or 3 era) (#715074)

* Tue Jun 14 2011 Nalin Dahyabhai <nalin@redhat.com> 1.9.1-3
- pull a fix from SVN to get libgssrpc clients (e.g. kadmin) authenticating
  using the old protocol over IPv4 again (RT#6920)

* Tue Jun 14 2011 Nalin Dahyabhai <nalin@redhat.com>
- incorporate a fix to teach the file labeling bits about when replay caches
  are expunged (#576093)

* Thu May 26 2011 Nalin Dahyabhai <nalin@redhat.com>
- switch to the upstream patch for #707145

* Wed May 25 2011 Nalin Dahyabhai <nalin@redhat.com> 1.9.1-2
- klist: don't trip over referral entries when invoked with -s (#707145,
  RT#6915)

* Fri May  6 2011 Nalin Dahyabhai <nalin@redhat.com>
- fixup URL in a comment
- when built with NSS, require 3.12.10 rather than 3.12.9

* Thu May  5 2011 Nalin Dahyabhai <nalin@redhat.com> 1.9.1-1
- update to 1.9.1:
  - drop no-longer-needed patches for CVE-2010-4022, CVE-2011-0281,
    CVE-2011-0282, CVE-2011-0283, CVE-2011-0284, CVE-2011-0285

* Wed Apr 13 2011 Nalin Dahyabhai <nalin@redhat.com> 1.9-9
- kadmind: add upstream patch to fix free() on an invalid pointer (#696343,
  MITKRB5-SA-2011-004, CVE-2011-0285)

* Mon Apr  4 2011 Nalin Dahyabhai <nalin@redhat.com>
- don't discard the error code from an error message received in response
  to a change-password request (#658871, RT#6893)

* Fri Apr  1 2011 Nalin Dahyabhai <nalin@redhat.com>
- override INSTALL_SETUID at build-time so that ksu is installed into
  the buildroot with the right permissions (part of #225974)

* Fri Mar 18 2011 Nalin Dahyabhai <nalin@redhat.com> 1.9-8
- backport change from SVN to fix a computed-value-not-used warning in
  kpropd (#684065)

* Tue Mar 15 2011 Nalin Dahyabhai <nalin@redhat.com> 1.9-7
- turn off NSS as the backend for libk5crypto for now to work around its
  DES string2key not working (#679012)
- add revised upstream patch to fix double-free in KDC while returning
  typed-data with errors (MITKRB5-SA-2011-003, CVE-2011-0284, #674325)

* Thu Feb 17 2011 Nalin Dahyabhai <nalin@redhat.com>
- throw in a not-applied-by-default patch to try to make pkinit debugging
  into a run-time boolean option named "pkinit_debug"

* Wed Feb 16 2011 Nalin Dahyabhai <nalin@redhat.com> 1.9-6
- turn on NSS as the backend for libk5crypto, adding nss-devel as a build
  dependency when that switch is flipped

* Wed Feb  9 2011 Nalin Dahyabhai <nalin@redhat.com> 1.9-5
- krb5kdc init script: prototype some changes to do a quick spot-check
  of the TGS and kadmind keys and warn if there aren't any non-weak keys
  on file for them (to flush out parts of #651466)

* Tue Feb  8 2011 Nalin Dahyabhai <nalin@redhat.com> 1.9-4
- add upstream patches to fix standalone kpropd exiting if the per-client
  child process exits with an error (MITKRB5-SA-2011-001), a hang or crash
  in the KDC when using the LDAP kdb backend, and an uninitialized pointer
  use in the KDC (MITKRB5-SA-2011-002) (CVE-2010-4022, #664009,
  CVE-2011-0281, #668719, CVE-2011-0282, #668726, CVE-2011-0283, #676126)

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Feb  7 2011 Nalin Dahyabhai <nalin@redhat.com>
- fix a compile error in the SELinux labeling patch when -DDEBUG is used (Sumit
  Bose)

* Tue Feb  1 2011 Nalin Dahyabhai <nalin@redhat.com>
- properly advertise that the kpropd init script now supports force-reload
  (Zbysek Mraz, #630587)

* Wed Jan 26 2011 Nalin Dahyabhai <nalin@redhat.com> 1.9-2
- pkinit: when verifying signed data, use the CMS APIs for better
  interoperability (#636985, RT#6851)

* Wed Dec 22 2010 Nalin Dahyabhai <nalin@redhat.com> 1.9-1
- update to 1.9 final

* Mon Dec 20 2010 Nalin Dahyabhai <nalin@redhat.com> 1.9-0.beta3.1
- fix link flags and permissions on shared libraries (ausil)

* Thu Dec 16 2010 Nalin Dahyabhai <nalin@redhat.com> 1.9-0.beta3.0
- update to 1.9 beta 3

* Mon Dec  6 2010 Nalin Dahyabhai <nalin@redhat.com> 1.9-0.beta2.0
- update to 1.9 beta 2

* Tue Nov  9 2010 Nalin Dahyabhai <nalin@redhat.com> 1.9-0.beta1.1
- drop not-needed-since-1.8 build dependency on rsh (ssorce)

* Fri Nov  5 2010 Nalin Dahyabhai <nalin@redhat.com> 1.9-0.beta1.0
- start moving to 1.9 with beta 1
  - drop patches for RT#5755, RT#6762, RT#6774, RT#6775
  - drop no-longer-needed backport patch for #539423
  - drop no-longer-needed patch for CVE-2010-1322
- if WITH_NSS is set, built with --with-crypto-impl=nss (requires NSS 3.12.9)

* Tue Oct  5 2010 Nalin Dahyabhai <nalin@redhat.com> 1.8.3-8
- incorporate upstream patch to fix uninitialized pointer crash in the KDC's
  authorization data handling (CVE-2010-1322, #636335)

* Mon Oct  4 2010 Nalin Dahyabhai <nalin@redhat.com> 1.8.3-7
- rebuild

* Mon Oct  4 2010 Nalin Dahyabhai <nalin@redhat.com> 1.8.3-6
- pull down patches from trunk to implement k5login_authoritative and
  k5login_directory settings for krb5.conf (#539423)

* Wed Sep 29 2010 jkeating - 1.8.3-5
- Rebuilt for gcc bug 634757

* Wed Sep 15 2010 Nalin Dahyabhai <nalin@redhat.com> 1.8.3-4
- fix reading of keyUsage extensions when attempting to select pkinit client
  certs (part of #629022, RT#6775)
- fix selection of pkinit client certs when one or more don't include a
  subjectAltName extension (part of #629022, RT#6774)

* Fri Sep  3 2010 Nalin Dahyabhai <nalin@redhat.com> 1.8.3-3
- build with -fstack-protector-all instead of the default -fstack-protector,
  so that we add checking to more functions (i.e., all of them) (#629950)
- also link binaries with -Wl,-z,relro,-z,now (part of #629950)

* Tue Aug 24 2010 Nalin Dahyabhai <nalin@redhat.com> 1.8.3-2
- fix a logic bug in computing key expiration times (RT#6762, #627022)

* Wed Aug  4 2010 Nalin Dahyabhai <nalin@redhat.com> 1.8.3-1
- update to 1.8.3
  - drop backports of fixes for gss context expiration and error table
    registration/deregistration mismatch
  - drop patch for upstream #6750

* Wed Jul  7 2010 Nalin Dahyabhai <nalin@redhat.com> 1.8.2-3
- tell krb5kdc and kadmind to create pid files, since they can
- add logrotate configuration files for krb5kdc and kadmind (#462658)
- fix parsing of the pidfile option in the KDC (upstream #6750)

* Mon Jun 21 2010 Nalin Dahyabhai <nalin@redhat.com> 1.8.2-2
- libgssapi: pull in patch from svn to stop returning context-expired errors
  when the ticket which was used to set up the context expires (#605366,
  upstream #6739)

* Mon Jun 21 2010 Nalin Dahyabhai <nalin@redhat.com>
- pull up fix for upstream #6745, in which the gssapi library would add the
  wrong error table but subsequently attempt to unload the right one

* Thu Jun 10 2010 Nalin Dahyabhai <nalin@redhat.com> 1.8.2-1
- update to 1.8.2
  - drop patches for CVE-2010-1320, CVE-2010-1321

* Tue Jun  1 2010 Nalin Dahyabhai <nalin@redhat.com> 1.8.1-7
- rebuild

* Thu May 27 2010 Nalin Dahyabhai <nalin@redhat.com>
- ksu: move session management calls to before we drop privileges, like
  su does (#596887), and don't skip the PAM account check for root or the
  same user (more of #540769)

* Mon May 24 2010 Nalin Dahyabhai <nalin@redhat.com> 1.8.1-6
- make krb5-server-ldap also depend on the same version-release of krb5-libs,
  as the other subpackages do, if only to make it clearer than it is when we
  just do it through krb5-server
- drop explicit linking with libtinfo for applications that use libss, now
  that readline itself links with libtinfo (as of readline-5.2-3, since
  fedora 7 or so)
- go back to building without strict aliasing (compiler warnings in gssrpc)

* Tue May 18 2010 Nalin Dahyabhai <nalin@redhat.com> 1.8.1-5
- add patch to correct GSSAPI library null pointer dereference which could be
  triggered by malformed client requests (CVE-2010-1321, #582466)

* Tue May  4 2010 Nalin Dahyabhai <nalin@redhat.com> 1.8.1-4
- fix output of kprop's init script's "status" and "reload" commands (#588222)

* Tue Apr 20 2010 Nalin Dahyabhai <nalin@redhat.com> 1.8.1-3
- incorporate patch to fix double-free in the KDC (CVE-2010-1320, #581922)

* Wed Apr 14 2010 Nalin Dahyabhai <nalin@redhat.com> 1.8.1-2
- fix a typo in kerberos.ldif

* Fri Apr  9 2010 Nalin Dahyabhai <nalin@redhat.com> 1.8.1-1
- update to 1.8.1
  - no longer need patches for #555875, #561174, #563431, RT#6661, CVE-2010-0628
- replace buildrequires on tetex-latex with one on texlive-latex, which is
  the package that provides it now

* Thu Apr  8 2010 Nalin Dahyabhai <nalin@redhat.com>
- kdc.conf: no more need to suggest a v4 mode, or listening on the v4 port

* Thu Apr  8 2010 Nalin Dahyabhai <nalin@redhat.com>
- drop patch to suppress key expiration warnings sent from the KDC in
  the last-req field, as the KDC is expected to just be configured to either
  send them or not as a particular key approaches expiration (#556495)

* Tue Mar 23 2010 Nalin Dahyabhai <nalin@redhat.com> - 1.8-5
- add upstream fix for denial-of-service in SPNEGO (CVE-2010-0628, #576325)
- kdc.conf: no more need to suggest keeping keys with v4-compatible salting

* Fri Mar 19 2010 Nalin Dahyabhai <nalin@redhat.com> - 1.8-4
- remove the krb5-appl bits (the -workstation-clients and -workstation-servers
  subpackages) now that krb5-appl is its own package
- replace our patch for #563431 (kpasswd doesn't fall back to guessing your
  principal name using your user name if you don't have a ccache) with the
  one upstream uses

* Fri Mar 12 2010 Nalin Dahyabhai <nalin@redhat.com> - 1.8-3
- add documentation for the ticket_lifetime option (#561174)

* Mon Mar  8 2010 Nalin Dahyabhai <nalin@redhat.com> - 1.8-2
- pull up patch to get the client libraries to correctly perform password
  changes over IPv6 (Sumit Bose, RT#6661)

* Fri Mar  5 2010 Nalin Dahyabhai <nalin@redhat.com> - 1.8-1
- update to 1.8
  - temporarily bundling the krb5-appl package (split upstream as of 1.8)
    until its package review is complete
  - profile.d scriptlets are now only needed by -workstation-clients
  - adjust paths in init scripts
  - drop upstreamed fix for KDC denial of service (CVE-2010-0283)
  - drop patch to check the user's password correctly using crypt(), which
    isn't a code path we hit when we're using PAM

* Wed Mar  3 2010 Nalin Dahyabhai <nalin@redhat.com> - 1.7.1-6
- fix a null pointer dereference and crash introduced in our PAM patch that
  would happen if ftpd was given the name of a user who wasn't known to the
  local system, limited to being triggerable by gssapi-authenticated clients by
  the default xinetd config (Olivier Fourdan, #569472)

* Tue Mar  2 2010 Nalin Dahyabhai <nalin@redhat.com> - 1.7.1-5
- fix a regression (not labeling a kdb database lock file correctly, #569902)

* Thu Feb 25 2010 Nalin Dahyabhai <nalin@redhat.com> - 1.7.1-4
- move the package changelog to the end to match the usual style (jdennis)
- scrub out references to $RPM_SOURCE_DIR (jdennis)
- include a symlink to the readme with the name LICENSE so that people can
  find it more easily (jdennis)

* Wed Feb 17 2010 Nalin Dahyabhai <nalin@redhat.com> - 1.7.1-3
- pull up the change to make kpasswd's behavior better match the docs
  when there's no ccache (#563431)

* Tue Feb 16 2010 Nalin Dahyabhai <nalin@redhat.com> - 1.7.1-2
- apply patch from upstream to fix KDC denial of service (CVE-2010-0283,
  #566002)

* Wed Feb  3 2010 Nalin Dahyabhai <nalin@redhat.com> - 1.7.1-1
- update to 1.7.1
  - don't trip AD lockout on wrong password (#542687, #554351)
  - incorporates fixes for CVE-2009-4212 and CVE-2009-3295
  - fixes gss_krb5_copy_ccache() when SPNEGO is used
- move sim_client/sim_server, gss-client/gss-server, uuclient/uuserver to
  the devel subpackage, better lining up with the expected krb5/krb5-appl
  split in 1.8
- drop kvno,kadmin,k5srvutil,ktutil from -workstation-servers, as it already
  depends on -workstation which also includes them

* Mon Jan 25 2010 Nalin Dahyabhai <nalin@redhat.com> - 1.7-23
- tighten up default permissions on kdc.conf and kadm5.acl (#558343)

* Fri Jan 22 2010 Nalin Dahyabhai <nalin@redhat.com> - 1.7-22
- use portreserve correctly -- portrelease takes the basename of the file
  whose entries should be released, so we need three files, not one

* Mon Jan 18 2010 Nalin Dahyabhai <nalin@redhat.com> - 1.7-21
- suppress warnings of impending password expiration if expiration is more than
  seven days away when the KDC reports it via the last-req field, just as we
  already do when it reports expiration via the key-expiration field (#556495)
- link with libtinfo rather than libncurses, when we can, in future RHEL

* Fri Jan 15 2010 Nalin Dahyabhai <nalin@redhat.com> - 1.7-20
- krb5_get_init_creds_password: check opte->flags instead of options->flags
  when checking whether or not we get to use the prompter callback (#555875)

* Thu Jan 14 2010 Nalin Dahyabhai <nalin@redhat.com> - 1.7-19
- use portreserve to make sure the KDC can always bind to the kerberos-iv
  port, kpropd can always bind to the krb5_prop port, and that kadmind can
  always bind to the kerberos-adm port (#555279)
- correct inadvertent use of macros in the changelog (rpmlint)

* Tue Jan 12 2010 Nalin Dahyabhai <nalin@redhat.com> - 1.7-18
- add upstream patch for integer underflow during AES and RC4 decryption
  (CVE-2009-4212), via Tom Yu (#545015)

* Wed Jan  6 2010 Nalin Dahyabhai <nalin@redhat.com> - 1.7-17
- put the conditional back for the -devel subpackage
- back down to the earlier version of the patch for #551764; the backported
  alternate version was incomplete

* Tue Jan  5 2010 Nalin Dahyabhai <nalin@redhat.com> - 1.7-16
- use %%global instead of %%define
- pull up proposed patch for creating previously-not-there lock files for
  kdb databases when 'kdb5_util' is called to 'load' (#551764)

* Mon Jan  4 2010 Dennis Gregorovic <dgregor@redhat.com>
- fix conditional for future RHEL

* Mon Jan  4 2010 Nalin Dahyabhai <nalin@redhat.com> - 1.7-15
- add upstream patch for KDC crash during referral processing (CVE-2009-3295),
  via Tom Yu (#545002)

* Mon Dec 21 2009 Nalin Dahyabhai <nalin@redhat.com> - 1.7-14
- refresh patch for #542868 from trunk

* Thu Dec 10 2009 Nalin Dahyabhai <nalin@redhat.com>
- move man pages that live in the -libs subpackage into the regular
  %%{_mandir} tree where they'll still be found if that package is the
  only one installed (#529319)

* Wed Dec  9 2009 Nalin Dahyabhai <nalin@redhat.com> - 1.7-13
- and put it back in

* Tue Dec  8 2009 Nalin Dahyabhai <nalin@redhat.com>
- back that last change out

* Tue Dec  8 2009 Nalin Dahyabhai <nalin@redhat.com> - 1.7-12
- try to make gss_krb5_copy_ccache() work correctly for spnego (#542868)

* Fri Dec  4 2009 Nalin Dahyabhai <nalin@redhat.com>
- make krb5-config suppress CFLAGS output when called with --libs (#544391)

* Thu Dec  3 2009 Nalin Dahyabhai <nalin@redhat.com> - 1.7-11
- ksu: move account management checks to before we drop privileges, like
  su does (#540769)
- selinux: set the user part of file creation contexts to match the current
  context instead of what we looked up
- configure with --enable-dns-for-realm instead of --enable-dns, which isn't
  recognized any more

* Fri Nov 20 2009 Nalin Dahyabhai <nalin@redhat.com> - 1.7-10
- move /etc/pam.d/ksu from krb5-workstation-servers to krb5-workstation,
  where it's actually needed (#538703)

* Fri Oct 23 2009 Nalin Dahyabhai <nalin@redhat.com> - 1.7-9
- add some conditional logic to simplify building on older Fedora releases

* Tue Oct 13 2009 Nalin Dahyabhai <nalin@redhat.com>
- don't forget the README

* Mon Sep 14 2009 Nalin Dahyabhai <nalin@redhat.com> - 1.7-8
- specify the location of the subsystem lock when using the status() function
  in the kadmind and kpropd init scripts, so that we get the right error when
  we're dead but have a lock file - requires initscripts 8.99 (#521772)

* Tue Sep  8 2009 Nalin Dahyabhai <nalin@redhat.com>
- if the init script fails to start krb5kdc/kadmind/kpropd because it's already
  running (according to status()), return 0 (part of #521772)

* Mon Aug 24 2009 Nalin Dahyabhai <nalin@redhat.com> - 1.7-7
- work around a compile problem with new openssl

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 1.7-6
- rebuilt with new openssl

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul  7 2009 Nalin Dahyabhai <nalin@redhat.com> 1.7-5
- rebuild to pick up the current forms of various patches

* Mon Jul  6 2009 Nalin Dahyabhai <nalin@redhat.com>
- simplify the man pages patch by only preprocessing the files we care about
  and moving shared configure.in logic into a shared function
- catch the case of ftpd printing file sizes using %%i, when they might be
  bigger than an int now

* Tue Jun 30 2009 Nalin Dahyabhai <nalin@redhat.com> 1.7-4
- try to merge and clean up all the large file support for ftp and rcp
  - ftpd no longer prints a negative length when sending a large file
    from a 32-bit host

* Tue Jun 30 2009 Nalin Dahyabhai <nalin@redhat.com>
- pam_rhosts_auth.so's been gone, use pam_rhosts.so instead

* Mon Jun 29 2009 Nalin Dahyabhai <nalin@redhat.com> 1.7-3
- switch buildrequires: and requires: on e2fsprogs-devel into
  buildrequires: and requires: on libss-devel, libcom_err-devel, per
  sandeen on fedora-devel-list

* Fri Jun 26 2009 Nalin Dahyabhai <nalin@redhat.com>
- fix a type mismatch in krb5_copy_error_message()
- ftp: fix some odd use of strlen()
- selinux labeling: use selabel_open() family of functions rather than
  matchpathcon(), bail on it if attempting to get the mutex lock fails

* Tue Jun 16 2009 Nalin Dahyabhai <nalin@redhat.com>
- compile with %%{?_smp_mflags} (Steve Grubb)
- drop the bit where we munge part of the error table header, as it's not
  needed any more

* Fri Jun  5 2009 Nalin Dahyabhai <nalin@redhat.com> 1.7-2
- add and own %%{_libdir}/krb5/plugins/authdata

* Thu Jun  4 2009 Nalin Dahyabhai <nalin@redhat.com> 1.7-1
- update to 1.7
  - no need to work around build issues with ASN1BUF_OMIT_INLINE_FUNCS
  - configure recognizes --enable/--disable-pkinit now
  - configure can take --disable-rpath now
  - no more libdes425, krb524d, krb425.info
  - kadmin/k5srvutil/ktutil are user commands now
  - new kproplog
  - FAST encrypted-challenge plugin is new
- drop static build logic
- drop pam_krb5-specific configuration from the default krb5.conf
- drop only-use-v5 flags being passed to various things started by xinetd
- put %%{krb5prefix}/sbin in everyone's path, too (#504525)

* Tue May 19 2009 Nalin Dahyabhai <nalin@redhat.com> 1.6.3-106
- add an auth stack to ksu's PAM configuration so that pam_setcred() calls
  won't just fail

* Mon May 11 2009 Nalin Dahyabhai <nalin@redhat.com> 1.6.3-105
- make PAM support for ksu also set PAM_RUSER

* Thu Apr 23 2009 Nalin Dahyabhai <nalin@redhat.com> 1.6.3-104
- extend PAM support to ksu: perform account and session management for the
  target user
- pull up and merge James Leddy's changes to also set PAM_RHOST in PAM-aware
  network-facing services

* Tue Apr 21 2009 Nalin Dahyabhai <nalin@redhat.com> 1.6.3-103
- fix a typo in a ksu error message (Marek Mahut)
- "rev" works the way the test suite expects now, so don't disable tests
  that use it

* Mon Apr 20 2009 Nalin Dahyabhai <nalin@redhat.com> 1.6.3-102
- add LSB-style init script info

* Fri Apr 17 2009 Nalin Dahyabhai <nalin@redhat.com>
- explicitly run the pdf generation script using sh (part of #225974)

* Tue Apr  7 2009 Nalin Dahyabhai <nalin@redhat.com> 1.6.3-101
- add patches for read overflow and null pointer dereference in the
  implementation of the SPNEGO mechanism (CVE-2009-0844, CVE-2009-0845)
- add patch for attempt to free uninitialized pointer in libkrb5
  (CVE-2009-0846)
- add patch to fix length validation bug in libkrb5 (CVE-2009-0847)
- put the krb5-user .info file into just -workstation and not also
  -workstation-clients

* Mon Apr  6 2009 Nalin Dahyabhai <nalin@redhat.com> 1.6.3-100
- turn off krb4 support (it won't be part of the 1.7 release, but do it now)
- use triggeruns to properly shut down and disable krb524d when -server and
  -workstation-servers gets upgraded, because it's gone now
- move the libraries to /%%{_lib}, but leave --libdir alone so that plugins
  get installed and are searched for in the same locations (#473333)
- clean up buildprereq/prereqs, explicit mktemp requires, and add the
  ldconfig for the -server-ldap subpackage (part of #225974)
- escape possible macros in the changelog (part of #225974)
- fixup summary texts (part of #225974)
- take the execute bit off of the protocol docs (part of #225974)
- unflag init scripts as configuration files (part of #225974)
- make the kpropd init script treat 'reload' as 'restart' (part of #225974)

* Tue Mar 17 2009 Nalin Dahyabhai <nalin@redhat.com> 1.6.3-19
- libgssapi_krb5: backport fix for some errors which can occur when
  we fail to set up the server half of a context (CVE-2009-0845)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.3-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 16 2009 Nalin Dahyabhai <nalin@redhat.com> 1.6.3-17
- rebuild

* Thu Sep  4 2008 Nalin Dahyabhai <nalin@redhat.com>
- if we successfully change the user's password during an attempt to get
  initial credentials, but then fail to get initial creds from a non-master
  using the new password, retry against the master (#432334)

* Tue Aug  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.6.3-16
- fix license tag

* Wed Jul 16 2008 Nalin Dahyabhai <nalin@redhat.com>
- clear fuzz out of patches, dropping a man page patch which is no longer
  necessary
- quote %%{__cc} where needed because it includes whitespace now
- define ASN1BUF_OMIT_INLINE_FUNCS at compile-time (for now) to keep building

* Fri Jul 11 2008 Nalin Dahyabhai <nalin@redhat.com> 1.6.3-15
- build with -fno-strict-aliasing, which is needed because the library
  triggers these warnings
- don't forget to label principal database lock files
- fix the labeling patch so that it doesn't break bootstrapping

* Sat Jun 14 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.6.3-14
- generate src/include/krb5/krb5.h before building
- fix conditional for sparcv9

* Wed Apr 16 2008 Nalin Dahyabhai <nalin@redhat.com> 1.6.3-13
- ftp: use the correct local filename during mget when the 'case' option is
  enabled (#442713)

* Fri Apr  4 2008 Nalin Dahyabhai <nalin@redhat.com> 1.6.3-12
- stop exporting kadmin keys to a keytab file when kadmind starts -- the
  daemon's been able to use the database directly for a long long time now
- belatedly add aes128,aes256 to the default set of supported key types

* Tue Apr  1 2008 Nalin Dahyabhai <nalin@redhat.com> 1.6.3-11
- libgssapi_krb5: properly export the acceptor subkey when creating a lucid
  context (Kevin Coffman, via the nfs4 mailing list)

* Tue Mar 18 2008 Nalin Dahyabhai <nalin@redhat.com> 1.6.3-10
- add fixes from MITKRB5-SA-2008-001 for use of null or dangling pointer
  when v4 compatibility is enabled on the KDC (CVE-2008-0062, CVE-2008-0063,
  #432620, #432621)
- add fixes from MITKRB5-SA-2008-002 for array out-of-bounds accesses when
  high-numbered descriptors are used (CVE-2008-0947, #433596)
- add backport bug fix for an attempt to free non-heap memory in
  libgssapi_krb5 (CVE-2007-5901, #415321)
- add backport bug fix for a double-free in out-of-memory situations in
  libgssapi_krb5 (CVE-2007-5971, #415351)

* Tue Mar 18 2008 Nalin Dahyabhai <nalin@redhat.com> 1.6.3-9
- rework file labeling patch to not depend on fragile preprocessor trickery,
  in another attempt at fixing #428355 and friends

* Tue Feb 26 2008 Nalin Dahyabhai <nalin@redhat.com> 1.6.3-8
- ftp: add patch to fix "runique on" case when globbing fixes applied
- stop adding a redundant but harmless call to initialize the gssapi internals

* Mon Feb 25 2008 Nalin Dahyabhai <nalin@redhat.com>
- add patch to suppress double-processing of /etc/krb5.conf when we build
  with --sysconfdir=/etc, thereby suppressing double-logging (#231147)

* Mon Feb 25 2008 Nalin Dahyabhai <nalin@redhat.com>
- remove a patch, to fix problems with interfaces which are "up" but which
  have no address assigned, which conflicted with a different fix for the same
  problem in 1.5 (#200979)

* Mon Feb 25 2008 Nalin Dahyabhai <nalin@redhat.com>
- ftp: don't lose track of a descriptor on passive get when the server fails to
  open a file

* Mon Feb 25 2008 Nalin Dahyabhai <nalin@redhat.com>
- in login, allow PAM to interact with the user when they've been strongly
  authenticated
- in login, signal PAM when we're changing an expired password that it's an
  expired password, so that when cracklib flags a password as being weak it's
  treated as an error even if we're running as root

* Mon Feb 18 2008 Nalin Dahyabhai <nalin@redhat.com> 1.6.3-7
- drop netdb patch
- kdb_ldap: add patch to treat 'nsAccountLock: true' as an indication that
  the DISALLOW_ALL_TIX flag is set on an entry, for better interop with Fedora,
  Netscape, Red Hat Directory Server (Simo Sorce)

* Wed Feb 13 2008 Nalin Dahyabhai <nalin@redhat.com> 1.6.3-6
- patch to avoid depending on <netdb.h> to define NI_MAXHOST and NI_MAXSERV

* Tue Feb 12 2008 Nalin Dahyabhai <nalin@redhat.com> 1.6.3-5
- enable patch for key-expiration reporting
- enable patch to make kpasswd fall back to TCP if UDP fails (#251206)
- enable patch to make kpasswd use the right sequence number on retransmit
- enable patch to allow mech-specific creds delegated under spnego to be found
  when searching for creds

* Wed Jan  2 2008 Nalin Dahyabhai <nalin@redhat.com> 1.6.3-4
- some init script cleanups
  - drop unquoted check and silent exit for "$NETWORKING" (#426852, #242502)
  - krb524: don't barf on missing database if it looks like we're using kldap,
    same as for kadmin
  - return non-zero status for missing files which cause startup to
    fail (#242502)

* Tue Dec 18 2007 Nalin Dahyabhai <nalin@redhat.com> 1.6.3-3
- allocate space for the nul-terminator in the local pathname when looking up
  a file context, and properly free a previous context (Jose Plans, #426085)

* Wed Dec  5 2007 Nalin Dahyabhai <nalin@redhat.com> 1.6.3-2
- rebuild

* Tue Oct 23 2007 Nalin Dahyabhai <nalin@redhat.com> 1.6.3-1
- update to 1.6.3, dropping now-integrated patches for CVE-2007-3999
  and CVE-2007-4000 (the new pkinit module is built conditionally and goes
  into the -pkinit-openssl package, at least for now, to make a buildreq
  loop with openssl avoidable)

* Wed Oct 17 2007 Nalin Dahyabhai <nalin@redhat.com> 1.6.2-10
- make proper use of pam_loginuid and pam_selinux in rshd and ftpd

* Fri Oct 12 2007 Nalin Dahyabhai <nalin@redhat.com>
- make krb5.conf %%verify(not md5 size mtime) in addition to
  %%config(noreplace), like /etc/nsswitch.conf (#329811)

* Mon Oct  1 2007 Nalin Dahyabhai <nalin@redhat.com> 1.6.2-9
- apply the fix for CVE-2007-4000 instead of the experimental patch for
  setting ok-as-delegate flags

* Tue Sep 11 2007 Nalin Dahyabhai <nalin@redhat.com> 1.6.2-8
- move the db2 kdb plugin from -server to -libs, because a multilib libkdb
  might need it

* Tue Sep 11 2007 Nalin Dahyabhai <nalin@redhat.com> 1.6.2-7
- also perform PAM session and credential management when ftpd accepts a
  client using strong authentication, missed earlier
- also label kadmind log files and files created by the db2 plugin

* Thu Sep  6 2007 Nalin Dahyabhai <nalin@redhat.com> 1.6.2-6
- incorporate updated fix for CVE-2007-3999 (CVE-2007-4743)
- fix incorrect call to "test" in the kadmin init script (#252322,#287291)

* Tue Sep  4 2007 Nalin Dahyabhai <nalin@redhat.com> 1.6.2-5
- incorporate fixes for MITKRB5-SA-2007-006 (CVE-2007-3999, CVE-2007-4000)

* Sat Aug 25 2007 Nalin Dahyabhai <nalin@redhat.com> 1.6.2-4
- cover more cases in labeling files on creation
- add missing gawk build dependency

* Thu Aug 23 2007 Nalin Dahyabhai <nalin@redhat.com> 1.6.2-3
- rebuild

* Thu Jul 26 2007 Nalin Dahyabhai <nalin@redhat.com> 1.6.2-2
- kdc.conf: default to listening for TCP clients, too (#248415)

* Thu Jul 19 2007 Nalin Dahyabhai <nalin@redhat.com> 1.6.2-1
- update to 1.6.2
- add "buildrequires: texinfo-tex" to get texi2pdf

* Wed Jun 27 2007 Nalin Dahyabhai <nalin@redhat.com> 1.6.1-8
- incorporate fixes for MITKRB5-SA-2007-004 (CVE-2007-2442,CVE-2007-2443)
  and MITKRB5-SA-2007-005 (CVE-2007-2798)

* Mon Jun 25 2007 Nalin Dahyabhai <nalin@redhat.com> 1.6.1-7
- reintroduce missing %%postun for the non-split_workstation case

* Mon Jun 25 2007 Nalin Dahyabhai <nalin@redhat.com> 1.6.1-6
- rebuild

* Mon Jun 25 2007 Nalin Dahyabhai <nalin@redhat.com> 1.6.1-5.1
- rebuild

* Sun Jun 24 2007 Nalin Dahyabhai <nalin@redhat.com> 1.6.1-5
- add missing pam-devel build requirement, force selinux-or-fail build

* Sun Jun 24 2007 Nalin Dahyabhai <nalin@redhat.com> 1.6.1-4
- rebuild

* Sun Jun 24 2007 Nalin Dahyabhai <nalin@redhat.com> 1.6.1-3
- label all files at creation-time according to the SELinux policy (#228157)

* Fri Jun 22 2007 Nalin Dahyabhai <nalin@redhat.com>
- perform PAM account / session management in krshd (#182195,#195922)
- perform PAM authentication and account / session management in ftpd
- perform PAM authentication, account / session management, and password-
  changing in login.krb5 (#182195,#195922)

* Fri Jun 22 2007 Nalin Dahyabhai <nalin@redhat.com>
- preprocess kerberos.ldif into a format FDS will like better, and include
  that as a doc file as well

* Fri Jun 22 2007 Nalin Dahyabhai <nalin@redhat.com>
- switch man pages to being generated with the right paths in them
- drop old, incomplete SELinux patch
- add patch from Greg Hudson to make srvtab routines report missing-file errors
  at same point that keytab routines do (#241805)

* Thu May 24 2007 Nalin Dahyabhai <nalin@redhat.com> 1.6.1-2
- pull patch from svn to undo unintentional chattiness in ftp
- pull patch from svn to handle NULL krb5_get_init_creds_opt structures
  better in a couple of places where they're expected

* Wed May 23 2007 Nalin Dahyabhai <nalin@redhat.com> 1.6.1-1
- update to 1.6.1
  - drop no-longer-needed patches for CVE-2007-0956,CVE-2007-0957,CVE-2007-1216
  - drop patch for sendto bug in 1.6, fixed in 1.6.1

* Fri May 18 2007 Nalin Dahyabhai <nalin@redhat.com>
- kadmind.init: don't fail outright if the default principal database
  isn't there if it looks like we might be using the kldap plugin
- kadmind.init: attempt to extract the key for the host-specific kadmin
  service when we try to create the keytab

* Wed May 16 2007 Nalin Dahyabhai <nalin@redhat.com> 1.6-6
- omit dependent libraries from the krb5-config --libs output, as using
  shared libraries (no more static libraries) makes them unnecessary and
  they're not part of the libkrb5 interface (patch by Rex Dieter, #240220)
  (strips out libkeyutils, libresolv, libdl)

* Fri May  4 2007 Nalin Dahyabhai <nalin@redhat.com> 1.6-5
- pull in keyutils as a build requirement to get the "KEYRING:" ccache type,
  because we've merged

* Fri May  4 2007 Nalin Dahyabhai <nalin@redhat.com> 1.6-4
- fix an uninitialized length value which could cause a crash when parsing
  key data coming from a directory server
- correct a typo in the krb5.conf man page ("ldap_server"->"ldap_servers")

* Fri Apr 13 2007 Nalin Dahyabhai <nalin@redhat.com>
- move the default acl_file, dict_file, and admin_keytab settings to
  the part of the default/example kdc.conf where they'll actually have
  an effect (#236417)

* Thu Apr  5 2007 Nalin Dahyabhai <nalin@redhat.com> 1.5-24
- merge security fixes from RHSA-2007:0095

* Tue Apr  3 2007 Nalin Dahyabhai <nalin@redhat.com> 1.6-3
- add patch to correct unauthorized access via krb5-aware telnet
  daemon (#229782, CVE-2007-0956)
- add patch to fix buffer overflow in krb5kdc and kadmind
  (#231528, CVE-2007-0957)
- add patch to fix double-free in kadmind (#231537, CVE-2007-1216)

* Thu Mar 22 2007 Nalin Dahyabhai <nalin@redhat.com>
- back out buildrequires: keyutils-libs-devel for now

* Thu Mar 22 2007 Nalin Dahyabhai <nalin@redhat.com> 1.6-2
- add buildrequires: on keyutils-libs-devel to enable use of keyring ccaches,
  dragging keyutils-libs in as a dependency

* Mon Mar 19 2007 Nalin Dahyabhai <nalin@redhat.com> 1.5-23
- fix bug ID in changelog

* Thu Mar 15 2007 Nalin Dahyabhai <nalin@redhat.com> 1.5-22

* Thu Mar 15 2007 Nalin Dahyabhai <nalin@redhat.com> 1.5-21
- add preliminary patch to fix buffer overflow in krb5kdc and kadmind
  (#231528, CVE-2007-0957)
- add preliminary patch to fix double-free in kadmind (#231537, CVE-2007-1216)

* Wed Feb 28 2007 Nalin Dahyabhai <nalin@redhat.com>
- add patch to build semi-useful static libraries, but don't apply it unless
  we need them

* Tue Feb 27 2007 Nalin Dahyabhai <nalin@redhat.com> - 1.5-20
- temporarily back out %%post changes, fix for #143289 for security update
- add preliminary patch to correct unauthorized access via krb5-aware telnet

* Mon Feb 19 2007 Nalin Dahyabhai <nalin@redhat.com>
- make profile.d scriptlets mode 644 instead of 755 (part of #225974)

* Tue Jan 30 2007 Nalin Dahyabhai <nalin@redhat.com> 1.6-1
- clean up quoting of command-line arguments passed to the krsh/krlogin
  wrapper scripts

* Mon Jan 22 2007 Nalin Dahyabhai <nalin@redhat.com>
- initial update to 1.6, pre-package-reorg
- move workstation daemons to a new subpackage (#81836, #216356, #217301), and
  make the new subpackage require xinetd (#211885)

* Mon Jan 22 2007 Nalin Dahyabhai <nalin@redhat.com> - 1.5-18
- make use of install-info more failsafe (Ville Skyttä, #223704)
- preserve timestamps on shell scriptlets at %%install-time

* Tue Jan 16 2007 Nalin Dahyabhai <nalin@redhat.com> - 1.5-17
- move to using pregenerated PDF docs to cure multilib conflicts (#222721)

* Fri Jan 12 2007 Nalin Dahyabhai <nalin@redhat.com> - 1.5-16
- update backport of the preauth module interface (part of #194654)

* Tue Jan  9 2007 Nalin Dahyabhai <nalin@redhat.com> - 1.5-14
- apply fixes from Tom Yu for MITKRB5-SA-2006-002 (CVE-2006-6143) (#218456)
- apply fixes from Tom Yu for MITKRB5-SA-2006-003 (CVE-2006-6144) (#218456)

* Wed Dec 20 2006 Nalin Dahyabhai <nalin@redhat.com> - 1.5-12
- update backport of the preauth module interface

* Mon Oct 30 2006 Nalin Dahyabhai <nalin@redhat.com>
- update backport of the preauth module interface
- add proposed patches 4566, 4567
- add proposed edata reporting interface for KDC
- add temporary placeholder for module global context fixes

* Mon Oct 23 2006 Nalin Dahyabhai <nalin@redhat.com> - 1.5-11
- don't bail from the KDC init script if there's no database, it may be in
  a different location than the default (fenlason)
- remove the [kdc] section from the default krb5.conf -- doesn't seem to have
  been applicable for a while

* Wed Oct 18 2006 Nalin Dahyabhai <nalin@redhat.com> - 1.5-10
- rename krb5.sh and krb5.csh so that they don't overlap (#210623)
- way-late application of added error info in kadmind.init (#65853)
 
* Wed Oct 18 2006 Nalin Dahyabhai <nalin@redhat.com> - 1.5-9.pal_18695
- add backport of in-development preauth module interface (#208643)

* Mon Oct  9 2006 Nalin Dahyabhai <nalin@redhat.com> - 1.5-9
- provide docs in PDF format instead of as tex source (Enrico Scholz, #209943)

* Wed Oct  4 2006 Nalin Dahyabhai <nalin@redhat.com> - 1.5-8
- add missing shebang headers to krsh and krlogin wrapper scripts (#209238)

* Wed Sep  6 2006 Nalin Dahyabhai <nalin@redhat.com> - 1.5-7
- set SS_LIB at configure-time so that libss-using apps get working readline
  support (#197044)

* Fri Aug 18 2006 Nalin Dahyabhai <nalin@redhat.com> - 1.5-6
- switch to the updated patch for MITKRB-SA-2006-001

* Tue Aug  8 2006 Nalin Dahyabhai <nalin@redhat.com> - 1.5-5
- apply patch to address MITKRB-SA-2006-001 (CVE-2006-3084)

* Mon Aug  7 2006 Nalin Dahyabhai <nalin@redhat.com> - 1.5-4
- ensure that the gssapi library's been initialized before walking the
  internal mechanism list in gss_release_oid(), needed if called from
  gss_release_name() right after a gss_import_name() (#198092)

* Tue Jul 25 2006 Nalin Dahyabhai <nalin@redhat.com> - 1.5-3
- rebuild

* Tue Jul 25 2006 Nalin Dahyabhai <nalin@redhat.com> - 1.5-2
- pull up latest revision of patch to reduce lockups in rsh/rshd

* Mon Jul 17 2006 Nalin Dahyabhai <nalin@redhat.com> - 1.5-1.2
- rebuild

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.5-1.1
- rebuild

* Thu Jul  6 2006 Nalin Dahyabhai <nalin@redhat.com> 1.5-1
- build

* Wed Jul  5 2006 Nalin Dahyabhai <nalin@redhat.com> 1.5-0
- update to 1.5

* Fri Jun 23 2006 Nalin Dahyabhai <nalin@redhat.com> 1.4.3-9
- mark profile.d config files noreplace (Laurent Rineau, #196447)

* Thu Jun  8 2006 Nalin Dahyabhai <nalin@redhat.com> 1.4.3-8
- add buildprereq for autoconf

* Mon May 22 2006 Nalin Dahyabhai <nalin@redhat.com> 1.4.3-7
- further munge krb5-config so that 'libdir=/usr/lib' is given even on 64-bit
  architectures, to avoid multilib conflicts; other changes will conspire to
  strip out the -L flag which uses this, so it should be harmless (#192692)

* Fri Apr 28 2006 Nalin Dahyabhai <nalin@redhat.com> 1.4.3-6
- adjust the patch which removes the use of rpath to also produce a
  krb5-config which is okay in multilib environments (#190118)
- make the name-of-the-tempfile comment which compile_et adds to error code
  headers always list the same file to avoid conflicts on multilib installations
- strip SIZEOF_LONG out of krb5.h so that it doesn't conflict on multilib boxes
- strip GSS_SIZEOF_LONG out of gssapi.h so that it doesn't conflict on mulitlib
  boxes

* Fri Apr 14 2006 Stepan Kasal <skasal@redhat.com> 1.4.3-5
- Fix formatting typo in kinit.1 (krb5-kinit-man-typo.patch)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> 1.4.3-4.1
- bump again for double-long bug on ppc(64)

* Mon Feb  6 2006 Nalin Dahyabhai <nalin@redhat.com> 1.4.3-4
- give a little bit more information to the user when kinit gets the catch-all
  I/O error (#180175)

* Thu Jan 19 2006 Nalin Dahyabhai <nalin@redhat.com> 1.4.3-3
- rebuild properly when pthread_mutexattr_setrobust_np() is defined but not
  declared, such as with recent glibc when _GNU_SOURCE isn't being used

* Thu Jan 19 2006 Matthias Clasen <mclasen@redhat.com> 1.4.3-2
- Use full paths in krb5.sh to avoid path lookups

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Dec  1 2005 Nalin Dahyabhai <nalin@redhat.com>
- login: don't truncate passwords before passing them into crypt(), in
  case they're significant (#149476)

* Thu Nov 17 2005 Nalin Dahyabhai <nalin@redhat.com> 1.4.3-1
- update to 1.4.3
- make ksu setuid again (#137934, others)

* Tue Sep 13 2005 Nalin Dahyabhai <nalin@redhat.com> 1.4.2-4
- mark %%{krb5prefix}/man so that files which are packaged within it are
  flagged as %%doc (#168163)

* Tue Sep  6 2005 Nalin Dahyabhai <nalin@redhat.com> 1.4.2-3
- add an xinetd configuration file for encryption-only telnetd, parallelling
  the kshell/ekshell pair (#167535)

* Wed Aug 31 2005 Nalin Dahyabhai <nalin@redhat.com> 1.4.2-2
- change the default configured encryption type for KDC databases to the
  compiled-in default of des3-hmac-sha1 (#57847)

* Thu Aug 11 2005 Nalin Dahyabhai <nalin@redhat.com> 1.4.2-1
- update to 1.4.2, incorporating the fixes for MIT-KRB5-SA-2005-002 and
  MIT-KRB5-SA-2005-003

* Wed Jun 29 2005 Nalin Dahyabhai <nalin@redhat.com> 1.4.1-6
- rebuild

* Wed Jun 29 2005 Nalin Dahyabhai <nalin@redhat.com> 1.4.1-5
- fix telnet client environment variable disclosure the same way NetKit's
  telnet client did (CAN-2005-0488) (#159305)
- keep apps which call krb5_principal_compare() or krb5_realm_compare() with
  malformed or NULL principal structures from crashing outright (Thomas Biege)
  (#161475)

* Tue Jun 28 2005 Nalin Dahyabhai <nalin@redhat.com>
- apply fixes from draft of MIT-KRB5-SA-2005-002 (CAN-2005-1174,CAN-2005-1175)
  (#157104)
- apply fixes from draft of MIT-KRB5-SA-2005-003 (CAN-2005-1689) (#159755)

* Fri Jun 24 2005 Nalin Dahyabhai <nalin@redhat.com> 1.4.1-4
- fix double-close in keytab handling
- add port of fixes for CAN-2004-0175 to krb5-aware rcp (#151612)

* Fri May 13 2005 Nalin Dahyabhai <nalin@redhat.com> 1.4.1-3
- prevent spurious EBADF in krshd when stdin is closed by the client while
  the command is running (#151111)

* Fri May 13 2005 Martin Stransky <stransky@redhat.com> 1.4.1-2
- add deadlock patch, removed old patch

* Fri May  6 2005 Nalin Dahyabhai <nalin@redhat.com> 1.4.1-1
- update to 1.4.1, incorporating fixes for CAN-2005-0468 and CAN-2005-0469
- when starting the KDC or kadmind, if KRB5REALM is set via the /etc/sysconfig
  file for the service, pass it as an argument for the -r flag

* Wed Mar 23 2005 Nalin Dahyabhai <nalin@redhat.com> 1.4-3
- drop krshd patch for now

* Thu Mar 17 2005 Nalin Dahyabhai <nalin@redhat.com>
- add draft fix from Tom Yu for slc_add_reply() buffer overflow (CAN-2005-0469)
- add draft fix from Tom Yu for env_opt_add() buffer overflow (CAN-2005-0468)

* Wed Mar 16 2005 Nalin Dahyabhai <nalin@redhat.com> 1.4-2
- don't include <term.h> into the telnet client when we're not using curses

* Thu Feb 24 2005 Nalin Dahyabhai <nalin@redhat.com> 1.4-1
- update to 1.4
  - v1.4 kadmin client requires a v1.4 kadmind on the server, or use the "-O"
    flag to specify that it should communicate with the server using the older
    protocol
  - new libkrb5support library
  - v5passwdd and kadmind4 are gone
  - versioned symbols
- pick up $KRB5KDC_ARGS from /etc/sysconfig/krb5kdc, if it exists, and pass
  it on to krb5kdc
- pick up $KADMIND_ARGS from /etc/sysconfig/kadmin, if it exists, and pass
  it on to kadmind
- pick up $KRB524D_ARGS from /etc/sysconfig/krb524, if it exists, and pass
  it on to krb524d *instead of* "-m"
- set "forwardable" in [libdefaults] in the default krb5.conf to match the
  default setting which we supply for pam_krb5
- set a default of 24h for "ticket_lifetime" in [libdefaults], reflecting the
  compiled-in default

* Mon Dec 20 2004 Nalin Dahyabhai <nalin@redhat.com> 1.3.6-3
- rebuild

* Mon Dec 20 2004 Nalin Dahyabhai <nalin@redhat.com> 1.3.6-2
- rebuild

* Mon Dec 20 2004 Nalin Dahyabhai <nalin@redhat.com> 1.3.6-1
- update to 1.3.6, which includes the previous fix

* Mon Dec 20 2004 Nalin Dahyabhai <nalin@redhat.com> 1.3.5-8
- apply fix from Tom Yu for MITKRB5-SA-2004-004 (CAN-2004-1189)

* Fri Dec 17 2004 Martin Stransky <stransky@redhat.com> 1.3.5-7
- fix deadlock during file transfer via rsync/krsh
- thanks goes to James Antill for hint

* Fri Nov 26 2004 Nalin Dahyabhai <nalin@redhat.com> 1.3.5-6
- rebuild

* Mon Nov 22 2004 Nalin Dahyabhai <nalin@redhat.com> 1.3.5-3
- fix predictable-tempfile-name bug in krb5-send-pr (CAN-2004-0971, #140036)

* Tue Nov 16 2004 Nalin Dahyabhai <nalin@redhat.com>
- silence compiler warning in kprop by using an in-memory ccache with a fixed
  name instead of an on-disk ccache with a name generated by tmpnam()

* Tue Nov 16 2004 Nalin Dahyabhai <nalin@redhat.com> 1.3.5-2
- fix globbing patch port mode (#139075)

* Mon Nov  1 2004 Nalin Dahyabhai <nalin@redhat.com> 1.3.5-1
- fix segfault in telnet due to incorrect checking of gethostbyname_r result
  codes (#129059)

* Fri Oct 15 2004 Nalin Dahyabhai <nalin@redhat.com>
- remove rc4-hmac:norealm and rc4-hmac:onlyrealm from the default list of
  supported keytypes in kdc.conf -- they produce exactly the same keys as
  rc4-hmac:normal because rc4 string-to-key ignores salts
- nuke kdcrotate -- there are better ways to balance the load on KDCs, and
  the SELinux policy for it would have been scary-looking
- update to 1.3.5, mainly to include MITKRB5SA 2004-002 and 2004-003

* Tue Aug 31 2004 Nalin Dahyabhai <nalin@redhat.com> 1.3.4-7
- rebuild

* Tue Aug 24 2004 Nalin Dahyabhai <nalin@redhat.com> 1.3.4-6
- rebuild

* Tue Aug 24 2004 Nalin Dahyabhai <nalin@redhat.com> 1.3.4-5
- incorporate revised fixes from Tom Yu for CAN-2004-0642, CAN-2004-0644,
  CAN-2004-0772

* Mon Aug 23 2004 Nalin Dahyabhai <nalin@redhat.com> 1.3.4-4
- rebuild

* Mon Aug 23 2004 Nalin Dahyabhai <nalin@redhat.com> 1.3.4-3
- incorporate fixes from Tom Yu for CAN-2004-0642, CAN-2004-0772
  (MITKRB5-SA-2004-002, #130732)
- incorporate fixes from Tom Yu for CAN-2004-0644 (MITKRB5-SA-2004-003, #130732)

* Tue Jul 27 2004 Nalin Dahyabhai <nalin@redhat.com> 1.3.4-2
- fix indexing error in server sorting patch (#127336)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Jun 14 2004 Nalin Dahyabhai <nalin@redhat.com> 1.3.4-0.1
- update to 1.3.4 final

* Mon Jun  7 2004 Nalin Dahyabhai <nalin@redhat.com> 1.3.4-0
- update to 1.3.4 beta1
- remove MITKRB5-SA-2004-001, included in 1.3.4

* Mon Jun  7 2004 Nalin Dahyabhai <nalin@redhat.com> 1.3.3-8
- rebuild

* Fri Jun  4 2004 Nalin Dahyabhai <nalin@redhat.com> 1.3.3-7
- rebuild

* Fri Jun  4 2004 Nalin Dahyabhai <nalin@redhat.com> 1.3.3-6
- apply updated patch from MITKRB5-SA-2004-001 (revision 2004-06-02)

* Tue Jun  1 2004 Nalin Dahyabhai <nalin@redhat.com> 1.3.3-5
- rebuild

* Tue Jun  1 2004 Nalin Dahyabhai <nalin@redhat.com> 1.3.3-4
- apply patch from MITKRB5-SA-2004-001 (#125001)

* Wed May 12 2004 Thomas Woerner <twoerner@redhat.com> 1.3.3-3
- removed rpath

* Thu Apr 15 2004 Nalin Dahyabhai <nalin@redhat.com> 1.3.3-2
- re-enable large file support, fell out in 1.3-1
- patch rcp to use long long and %%lld format specifiers when reporting file
  sizes on large files

* Tue Apr 13 2004 Nalin Dahyabhai <nalin@redhat.com> 1.3.3-1
- update to 1.3.3

* Wed Mar 10 2004 Nalin Dahyabhai <nalin@redhat.com> 1.3.2-1
- update to 1.3.2

* Mon Mar  8 2004 Nalin Dahyabhai <nalin@redhat.com> 1.3.1-12
- rebuild

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com> 1.3.1-11.1
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com> 1.3.1-11
- rebuilt

* Mon Feb  9 2004 Nalin Dahyabhai <nalin@redhat.com> 1.3.1-10
- catch krb4 send_to_kdc cases in kdc preference patch

* Mon Feb  2 2004 Nalin Dahyabhai <nalin@redhat.com> 1.3.1-9
- remove patch to set TERM in klogind which, combined with the upstream fix in
  1.3.1, actually produces the bug now (#114762)

* Mon Jan 19 2004 Nalin Dahyabhai <nalin@redhat.com> 1.3.1-8
- when iterating over lists of interfaces which are "up" from getifaddrs(),
  skip over those which have no address (#113347)

* Mon Jan 12 2004 Nalin Dahyabhai <nalin@redhat.com>
- prefer the kdc which last replied to a request when sending requests to kdcs

* Mon Nov 24 2003 Nalin Dahyabhai <nalin@redhat.com> 1.3.1-7
- fix combination of --with-netlib and --enable-dns (#82176)

* Tue Nov 18 2003 Nalin Dahyabhai <nalin@redhat.com>
- remove libdefault ticket_lifetime option from the default krb5.conf, it is
  ignored by libkrb5

* Thu Sep 25 2003 Nalin Dahyabhai <nalin@redhat.com> 1.3.1-6
- fix bug in patch to make rlogind start login with a clean environment a la
  netkit rlogin, spotted and fixed by Scott McClung

* Tue Sep 23 2003 Nalin Dahyabhai <nalin@redhat.com> 1.3.1-5
- include profile.d scriptlets in krb5-devel so that krb5-config will be in
  the path if krb5-workstation isn't installed, reported by Kir Kolyshkin

* Mon Sep  8 2003 Nalin Dahyabhai <nalin@redhat.com>
- add more etypes (arcfour) to the default enctype list in kdc.conf
- don't apply previous patch, refused upstream

* Fri Sep  5 2003 Nalin Dahyabhai <nalin@redhat.com> 1.3.1-4
- fix 32/64-bit bug storing and retrieving the issue_date in v4 credentials

* Wed Sep 3 2003 Dan Walsh <dwalsh@redhat.com> 1.3.1-3
- Don't check for write access on /etc/krb5.conf if SELinux

* Tue Aug 26 2003 Nalin Dahyabhai <nalin@redhat.com> 1.3.1-2
- fixup some int/pointer varargs wackiness

* Tue Aug  5 2003 Nalin Dahyabhai <nalin@redhat.com> 1.3.1-1
- rebuild

* Mon Aug  4 2003 Nalin Dahyabhai <nalin@redhat.com> 1.3.1-0
- update to 1.3.1

* Thu Jul 24 2003 Nalin Dahyabhai <nalin@redhat.com> 1.3-2
- pull fix for non-compliant encoding of salt field in etype-info2 preauth
  data from 1.3.1 beta 1, until 1.3.1 is released.

* Mon Jul 21 2003 Nalin Dahyabhai <nalin@redhat.com> 1.3-1
- update to 1.3

* Mon Jul  7 2003 Nalin Dahyabhai <nalin@redhat.com> 1.2.8-4
- correctly use stdargs

* Wed Jun 18 2003 Nalin Dahyabhai <nalin@redhat.com> 1.3-0.beta.4
- test update to 1.3 beta 4
- ditch statglue build option
- krb5-devel requires e2fsprogs-devel, which now provides libss and libcom_err

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed May 21 2003 Jeremy Katz <katzj@redhat.com> 1.2.8-2
- gcc 3.3 doesn't implement varargs.h, include stdarg.h instead

* Wed Apr  9 2003 Nalin Dahyabhai <nalin@redhat.com> 1.2.8-1
- update to 1.2.8

* Mon Mar 31 2003 Nalin Dahyabhai <nalin@redhat.com> 1.2.7-14
- fix double-free of enc_part2 in krb524d

* Fri Mar 21 2003 Nalin Dahyabhai <nalin@redhat.com> 1.2.7-13
- update to latest patch kit for MITKRB5-SA-2003-004

* Wed Mar 19 2003 Nalin Dahyabhai <nalin@redhat.com> 1.2.7-12
- add patch included in MITKRB5-SA-2003-003 (CAN-2003-0028)

* Mon Mar 17 2003 Nalin Dahyabhai <nalin@redhat.com> 1.2.7-11
- add patches from patchkit from MITKRB5-SA-2003-004 (CAN-2003-0138 and
  CAN-2003-0139)

* Thu Mar  6 2003 Nalin Dahyabhai <nalin@redhat.com> 1.2.7-10
- rebuild

* Thu Mar  6 2003 Nalin Dahyabhai <nalin@redhat.com> 1.2.7-9
- fix buffer underrun in unparsing certain principals (CAN-2003-0082)

* Tue Feb  4 2003 Nalin Dahyabhai <nalin@redhat.com> 1.2.7-8
- add patch to document the reject-bad-transited option in kdc.conf

* Mon Feb  3 2003 Nalin Dahyabhai <nalin@redhat.com>
- add patch to fix server-side crashes when principals have no
  components (CAN-2003-0072)

* Thu Jan 23 2003 Nalin Dahyabhai <nalin@redhat.com> 1.2.7-7
- add patch from Mark Cox for exploitable bugs in ftp client

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Jan 15 2003 Nalin Dahyabhai <nalin@redhat.com> 1.2.7-5
- use PICFLAGS when building code from the ktany patch

* Thu Jan  9 2003 Bill Nottingham <notting@redhat.com> 1.2.7-4
- debloat

* Tue Jan  7 2003 Jeremy Katz <katzj@redhat.com> 1.2.7-3
- include .so.* symlinks as well as .so.*.*

* Mon Dec  9 2002 Jakub Jelinek <jakub@redhat.com> 1.2.7-2
- always #include <errno.h> to access errno, never do it directly
- enable LFS on a bunch of other 32-bit arches

* Wed Dec  4 2002 Nalin Dahyabhai <nalin@redhat.com>
- increase the maximum name length allowed by kuserok() to the higher value
  used in development versions

* Mon Dec  2 2002 Nalin Dahyabhai <nalin@redhat.com>
- install src/krb524/README as README.krb524 in the -servers package,
  includes information about converting for AFS principals

* Fri Nov 15 2002 Nalin Dahyabhai <nalin@redhat.com> 1.2.7-1
- update to 1.2.7
- disable use of tcl

* Mon Nov 11 2002 Nalin Dahyabhai <nalin@redhat.com>
- update to 1.2.7-beta2 (internal only, not for release), dropping dnsparse
  and kadmind4 fixes

* Wed Oct 23 2002 Nalin Dahyabhai <nalin@redhat.com> 1.2.6-5
- add patch for buffer overflow in kadmind4 (not used by default)

* Fri Oct 11 2002 Nalin Dahyabhai <nalin@redhat.com> 1.2.6-4
- drop a hunk from the dnsparse patch which is actually redundant (thanks to
  Tom Yu)

* Wed Oct  9 2002 Nalin Dahyabhai <nalin@redhat.com> 1.2.6-3
- patch to handle truncated dns responses

* Mon Oct  7 2002 Nalin Dahyabhai <nalin@redhat.com> 1.2.6-2
- remove hashless key types from the default kdc.conf, they're not supposed to
  be there, noted by Sam Hartman on krbdev

* Fri Sep 27 2002 Nalin Dahyabhai <nalin@redhat.com> 1.2.6-1
- update to 1.2.6

* Fri Sep 13 2002 Nalin Dahyabhai <nalin@redhat.com> 1.2.5-7
- use %%{_lib} for the sake of multilib systems

* Fri Aug  2 2002 Nalin Dahyabhai <nalin@redhat.com> 1.2.5-6
- add patch from Tom Yu for exploitable bugs in rpc code used in kadmind

* Tue Jul 23 2002 Nalin Dahyabhai <nalin@redhat.com> 1.2.5-5
- fix bug in krb5.csh which would cause the path check to always succeed

* Fri Jul 19 2002 Jakub Jelinek <jakub@redhat.com> 1.2.5-4
- build even libdb.a with -fPIC and $RPM_OPT_FLAGS.

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed May  1 2002 Nalin Dahyabhai <nalin@redhat.com> 1.2.5-1
- update to 1.2.5
- disable statglue

* Fri Mar  1 2002 Nalin Dahyabhai <nalin@redhat.com> 1.2.4-1
- update to 1.2.4

* Wed Feb 20 2002 Nalin Dahyabhai <nalin@redhat.com> 1.2.3-5
- rebuild in new environment
- reenable statglue

* Sat Jan 26 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- prereq chkconfig for the server subpackage

* Wed Jan 16 2002 Nalin Dahyabhai <nalin@redhat.com> 1.2.3-3
- build without -g3, which gives us large static libraries in -devel

* Tue Jan 15 2002 Nalin Dahyabhai <nalin@redhat.com> 1.2.3-2
- reintroduce ld.so.conf munging in the -libs %%post

* Thu Jan 10 2002 Nalin Dahyabhai <nalin@redhat.com> 1.2.3-1
- rename the krb5 package back to krb5-libs; the previous rename caused
  something of an uproar
- update to 1.2.3, which includes the FTP and telnetd fixes
- configure without --enable-dns-for-kdc --enable-dns-for-realm, which now set
  the default behavior instead of enabling the feature (the feature is enabled
  by --enable-dns, which we still use)
- reenable optimizations on Alpha
- support more encryption types in the default kdc.conf (heads-up from post
  to comp.protocols.kerberos by Jason Heiss)

* Fri Aug  3 2001 Nalin Dahyabhai <nalin@redhat.com> 1.2.2-14
- rename the krb5-libs package to krb5 (naming a subpackage -libs when there
  is no main package is silly)
- move defaults for PAM to the appdefaults section of krb5.conf -- this is
  the area where the krb5_appdefault_* functions look for settings)
- disable statglue (warning: breaks binary compatibility with previous
  packages, but has to be broken at some point to work correctly with
  unpatched versions built with newer versions of glibc)

* Fri Aug  3 2001 Nalin Dahyabhai <nalin@redhat.com> 1.2.2-13
- bump release number and rebuild

* Wed Aug  1 2001 Nalin Dahyabhai <nalin@redhat.com>
- add patch to fix telnetd vulnerability

* Fri Jul 20 2001 Nalin Dahyabhai <nalin@redhat.com>
- tweak statglue.c to fix stat/stat64 aliasing problems
- be cleaner in use of gcc to build shlibs

* Wed Jul 11 2001 Nalin Dahyabhai <nalin@redhat.com>
- use gcc to build shared libraries

* Wed Jun 27 2001 Nalin Dahyabhai <nalin@redhat.com>
- add patch to support "ANY" keytab type (i.e.,
  "default_keytab_name = ANY:FILE:/etc/krb5.keytab,SRVTAB:/etc/srvtab"
  patch from Gerald Britton, #42551)
- build with -D_FILE_OFFSET_BITS=64 to get large file I/O in ftpd (#30697)
- patch ftpd to use long long and %%lld format specifiers to support the SIZE
  command on large files (also #30697)
- don't use LOG_AUTH as an option value when calling openlog() in ksu (#45965)
- implement reload in krb5kdc and kadmind init scripts (#41911)
- lose the krb5server init script (not using it any more)

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Tue May 29 2001 Nalin Dahyabhai <nalin@redhat.com>
- pass some structures by address instead of on the stack in krb5kdc

* Tue May 22 2001 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in new environment

* Thu Apr 26 2001 Nalin Dahyabhai <nalin@redhat.com>
- add patch from Tom Yu to fix ftpd overflows (#37731)

* Wed Apr 18 2001 Than Ngo <than@redhat.com>
- disable optimizations on the alpha again

* Fri Mar 30 2001 Nalin Dahyabhai <nalin@redhat.com>
- add in glue code to make sure that libkrb5 continues to provide a
  weak copy of stat()

* Thu Mar 15 2001 Nalin Dahyabhai <nalin@redhat.com>
- build alpha with -O0 for now

* Thu Mar  8 2001 Nalin Dahyabhai <nalin@redhat.com>
- fix the kpropd init script

* Mon Mar  5 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to 1.2.2, which fixes some bugs relating to empty ETYPE-INFO
- re-enable optimization on Alpha

* Thu Feb  8 2001 Nalin Dahyabhai <nalin@redhat.com>
- build alpha with -O0 for now
- own %%{_var}/kerberos

* Tue Feb  6 2001 Nalin Dahyabhai <nalin@redhat.com>
- own the directories which are created for each package (#26342)

* Tue Jan 23 2001 Nalin Dahyabhai <nalin@redhat.com>
- gettextize init scripts

* Fri Jan 19 2001 Nalin Dahyabhai <nalin@redhat.com>
- add some comments to the ksu patches for the curious
- re-enable optimization on alphas

* Mon Jan 15 2001 Nalin Dahyabhai <nalin@redhat.com>
- fix krb5-send-pr (#18932) and move it from -server to -workstation
- buildprereq libtermcap-devel
- temporariliy disable optimization on alphas
- gettextize init scripts

* Tue Dec  5 2000 Nalin Dahyabhai <nalin@redhat.com>
- force -fPIC

* Fri Dec  1 2000 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in new environment

* Tue Oct 31 2000 Nalin Dahyabhai <nalin@redhat.com>
- add bison as a BuildPrereq (#20091)

* Mon Oct 30 2000 Nalin Dahyabhai <nalin@redhat.com>
- change /usr/dict/words to /usr/share/dict/words in default kdc.conf (#20000)

* Thu Oct  5 2000 Nalin Dahyabhai <nalin@redhat.com>
- apply kpasswd bug fixes from David Wragg

* Wed Oct  4 2000 Nalin Dahyabhai <nalin@redhat.com>
- make krb5-libs obsolete the old krb5-configs package (#18351)
- don't quit from the kpropd init script if there's no principal database so
  that you can propagate the first time without running kpropd manually
- don't complain if /etc/ld.so.conf doesn't exist in the -libs %%post

* Tue Sep 12 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix credential forwarding problem in klogind (goof in KRB5CCNAME handling)
  (#11588)
- fix heap corruption bug in FTP client (#14301)

* Wed Aug 16 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix summaries and descriptions
- switched the default transfer protocol from PORT to PASV as proposed on
  bugzilla (#16134), and to match the regular ftp package's behavior

* Wed Jul 19 2000 Jeff Johnson <jbj@redhat.com>
- rebuild to compress man pages.

* Sat Jul 15 2000 Bill Nottingham <notting@redhat.com>
- move initscript back

* Fri Jul 14 2000 Nalin Dahyabhai <nalin@redhat.com>
- disable servers by default to keep linuxconf from thinking they need to be
  started when they don't

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jul 10 2000 Nalin Dahyabhai <nalin@redhat.com>
- change cleanup code in post to not tickle chkconfig
- add grep as a Prereq: for -libs

* Thu Jul  6 2000 Nalin Dahyabhai <nalin@redhat.com>
- move condrestarts to postun
- make xinetd configs noreplace
- add descriptions to xinetd configs
- add /etc/init.d as a prereq for the -server package
- patch to properly truncate $TERM in krlogind

* Fri Jun 30 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 1.2.1
- back out Tom Yu's patch, which is a big chunk of the 1.2 -> 1.2.1 update
- start using the official source tarball instead of its contents

* Thu Jun 29 2000 Nalin Dahyabhai <nalin@redhat.com>
- Tom Yu's patch to fix compatibility between 1.2 kadmin and 1.1.1 kadmind
- pull out 6.2 options in the spec file (sonames changing in 1.2 means it's not
  compatible with other stuff in 6.2, so no need)

* Wed Jun 28 2000 Nalin Dahyabhai <nalin@redhat.com>
- tweak graceful start/stop logic in post and preun

* Mon Jun 26 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to the 1.2 release
- ditch a lot of our patches which went upstream
- enable use of DNS to look up things at build-time
- disable use of DNS to look up things at run-time in default krb5.conf
- change ownership of the convert-config-files script to root.root
- compress PS docs
- fix some typos in the kinit man page
- run condrestart in server post, and shut down in preun

* Mon Jun 19 2000 Nalin Dahyabhai <nalin@redhat.com>
- only remove old krb5server init script links if the init script is there

* Sat Jun 17 2000 Nalin Dahyabhai <nalin@redhat.com>
- disable kshell and eklogin by default

* Thu Jun 15 2000 Nalin Dahyabhai <nalin@redhat.com>
- patch mkdir/rmdir problem in ftpcmd.y
- add condrestart option to init script
- split the server init script into three pieces and add one for kpropd

* Wed Jun 14 2000 Nalin Dahyabhai <nalin@redhat.com>
- make sure workstation servers are all disabled by default
- clean up krb5server init script

* Fri Jun  9 2000 Nalin Dahyabhai <nalin@redhat.com>
- apply second set of buffer overflow fixes from Tom Yu
- fix from Dirk Husung for a bug in buffer cleanups in the test suite
- work around possibly broken rev binary in running test suite
- move default realm configs from /var/kerberos to %%{_var}/kerberos

* Tue Jun  6 2000 Nalin Dahyabhai <nalin@redhat.com>
- make ksu and v4rcp owned by root

* Sat Jun  3 2000 Nalin Dahyabhai <nalin@redhat.com>
- use %%{_infodir} to better comply with FHS
- move .so files to -devel subpackage
- tweak xinetd config files (bugs #11833, #11835, #11836, #11840)
- fix package descriptions again

* Wed May 24 2000 Nalin Dahyabhai <nalin@redhat.com>
- change a LINE_MAX to 1024, fix from Ken Raeburn
- add fix for login vulnerability in case anyone rebuilds without krb4 compat
- add tweaks for byte-swapping macros in krb.h, also from Ken
- add xinetd config files
- make rsh and rlogin quieter
- build with debug to fix credential forwarding
- add rsh as a build-time req because the configure scripts look for it to
  determine paths

* Wed May 17 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix config_subpackage logic

* Tue May 16 2000 Nalin Dahyabhai <nalin@redhat.com>
- remove setuid bit on v4rcp and ksu in case the checks previously added
  don't close all of the problems in ksu
- apply patches from Jeffrey Schiller to fix overruns Chris Evans found
- reintroduce configs subpackage for use in the errata
- add PreReq: sh-utils

* Mon May 15 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix double-free in the kdc (patch merged into MIT tree)
- include convert-config-files script as a documentation file

* Wed May 03 2000 Nalin Dahyabhai <nalin@redhat.com>
- patch ksu man page because the -C option never works
- add access() checks and disable debug mode in ksu
- modify default ksu build arguments to specify more directories in CMD_PATH
  and to use getusershell()

* Wed May 03 2000 Bill Nottingham <notting@redhat.com>
- fix configure stuff for ia64

* Mon Apr 10 2000 Nalin Dahyabhai <nalin@redhat.com>
- add LDCOMBINE=-lc to configure invocation to use libc versioning (bug #10653)
- change Requires: for/in subpackages to include %%{version}

* Wed Apr 05 2000 Nalin Dahyabhai <nalin@redhat.com>
- add man pages for kerberos(1), kvno(1), .k5login(5)
- add kvno to -workstation

* Mon Apr 03 2000 Nalin Dahyabhai <nalin@redhat.com>
- Merge krb5-configs back into krb5-libs.  The krb5.conf file is marked as
  a %%config file anyway.
- Make krb5.conf a noreplace config file.

* Thu Mar 30 2000 Nalin Dahyabhai <nalin@redhat.com>
- Make klogind pass a clean environment to children, like NetKit's rlogind does.

* Wed Mar 08 2000 Nalin Dahyabhai <nalin@redhat.com>
- Don't enable the server by default.
- Compress info pages.
- Add defaults for the PAM module to krb5.conf

* Mon Mar 06 2000 Nalin Dahyabhai <nalin@redhat.com>
- Correct copyright: it's exportable now, provided the proper paperwork is
  filed with the government.

* Fri Mar 03 2000 Nalin Dahyabhai <nalin@redhat.com>
- apply Mike Friedman's patch to fix format string problems
- don't strip off argv[0] when invoking regular rsh/rlogin

* Thu Mar 02 2000 Nalin Dahyabhai <nalin@redhat.com>
- run kadmin.local correctly at startup

* Mon Feb 28 2000 Nalin Dahyabhai <nalin@redhat.com>
- pass absolute path to kadm5.keytab if/when extracting keys at startup

* Sat Feb 19 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix info page insertions

* Wed Feb  9 2000 Nalin Dahyabhai <nalin@redhat.com>
- tweak server init script to automatically extract kadm5 keys if
  /var/kerberos/krb5kdc/kadm5.keytab doesn't exist yet
- adjust package descriptions

* Thu Feb  3 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix for potentially gzipped man pages

* Fri Jan 21 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix comments in krb5-configs

* Fri Jan  7 2000 Nalin Dahyabhai <nalin@redhat.com>
- move /usr/kerberos/bin to end of PATH

* Tue Dec 28 1999 Nalin Dahyabhai <nalin@redhat.com>
- install kadmin header files

* Tue Dec 21 1999 Nalin Dahyabhai <nalin@redhat.com>
- patch around TIOCGTLC defined on alpha and remove warnings from libpty.h
- add installation of info docs
- remove krb4 compat patch because it doesn't fix workstation-side servers

* Mon Dec 20 1999 Nalin Dahyabhai <nalin@redhat.com>
- remove hesiod dependency at build-time

* Sun Dec 19 1999 Nalin Dahyabhai <nsdahya1@eos.ncsu.edu>
- rebuild on 1.1.1

* Thu Oct  7 1999 Nalin Dahyabhai <nsdahya1@eos.ncsu.edu>
- clean up init script for server, verify that it works [jlkatz]
- clean up rotation script so that rc likes it better
- add clean stanza

* Mon Oct  4 1999 Nalin Dahyabhai <nsdahya1@eos.ncsu.edu>
- backed out ncurses and makeshlib patches
- update for krb5-1.1
- add KDC rotation to rc.boot, based on ideas from Michael's C version

* Mon Sep 26 1999 Nalin Dahyabhai <nsdahya1@eos.ncsu.edu>
- added -lncurses to telnet and telnetd makefiles

* Mon Jul  5 1999 Nalin Dahyabhai <nsdahya1@eos.ncsu.edu>
- added krb5.csh and krb5.sh to /etc/profile.d

* Mon Jun 22 1999 Nalin Dahyabhai <nsdahya1@eos.ncsu.edu>
- broke out configuration files

* Mon Jun 14 1999 Nalin Dahyabhai <nsdahya1@eos.ncsu.edu>
- fixed server package so that it works now

* Sat May 15 1999 Nalin Dahyabhai <nsdahya1@eos.ncsu.edu>
- started changelog (previous package from zedz.net)
- updated existing 1.0.5 RPM from Eos Linux to krb5 1.0.6
- added --force to makeinfo commands to skip errors during build
