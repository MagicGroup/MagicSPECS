%global _hardened_build 1
%global backends %{nil}

Name: pdns
Version:	3.4.6
Release:	2%{?dist}
Summary: A modern, advanced and high performance authoritative-only nameserver
Summary(zh_CN.UTF-8): 一个现代化，先进的高性能的域名服务
Group: System Environment/Daemons
Group(zh_CN.UTF-8): 系统环境/服务
License: GPLv2
URL: http://powerdns.com
Source0: http://downloads.powerdns.com/releases/%{name}-%{version}.tar.bz2
Patch0: pdns-default-config.patch
Patch1: pdns-systemd.patch
Patch2: pdns-disable-secpoll.patch

Requires(pre): shadow-utils
Requires(post): systemd-sysv
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

BuildRequires: systemd-units
BuildRequires: boost-devel
BuildRequires: lua-devel
BuildRequires: cryptopp-devel
BuildRequires: bison
BuildRequires: polarssl-devel
BuildRequires: zeromq-devel
Provides: powerdns = %{version}-%{release}
%global backends %{backends} bind

%description
The PowerDNS Nameserver is a modern, advanced and high performance
authoritative-only nameserver. It is written from scratch and conforms
to all relevant DNS standards documents.
Furthermore, PowerDNS interfaces with almost any database.

%description -l zh_CN.UTF-8
一个现代化，先进的高性能的域名服务。

%package tools
Summary: Extra tools for %{name}
Summary(zh_CN.UTF-8): %{name} 的额外工具
Group: System Environment/Daemons
Group(zh_CN.UTF-8): 系统环境/服务

%description tools
This package contains the extra tools for %{name}

%description tools -l zh_CN.UTF-8
%{name} 的额外工具。

%package backend-mysql
Summary: MySQL backend for %{name}
Group: System Environment/Daemons
Requires: %{name}%{?_isa} = %{version}-%{release}
BuildRequires: mysql-devel
%global backends %{backends} gmysql

%description backend-mysql
This package contains the gmysql backend for %{name}

%package backend-postgresql
Summary: PostgreSQL backend for %{name}
Group: System Environment/Daemons
Requires: %{name}%{?_isa} = %{version}-%{release}
BuildRequires: postgresql-devel
%global backends %{backends} gpgsql

%description backend-postgresql
This package contains the gpgsql backend for %{name}

%package backend-pipe
Summary: Pipe backend for %{name}
Group: System Environment/Daemons
Requires: %{name}%{?_isa} = %{version}-%{release}
%global backends %{backends} pipe

%description backend-pipe
This package contains the pipe backend for %{name}

%package backend-remote
Summary: Remote backend for %{name}
Group: System Environment/Daemons
Requires: %{name}%{?_isa} = %{version}-%{release}
%global backends %{backends} remote

%description backend-remote
This package contains the remote backend for %{name}

%package backend-geo
Summary: Geo backend for %{name}
Group: System Environment/Daemons
Requires: %{name}%{?_isa} = %{version}-%{release}
%global backends %{backends} geo

%description backend-geo
This package contains the geo backend for %{name}
It allows different answers to DNS queries coming from different
IP address ranges or based on the geographic location

%package backend-ldap
Summary: LDAP backend for %{name}
Group: System Environment/Daemons
Requires: %{name}%{?_isa} = %{version}-%{release}
BuildRequires: openldap-devel
%global backends %{backends} ldap

%description backend-ldap
This package contains the ldap backend for %{name}

%package backend-lua
Summary: LUA backend for %{name}
Group: System Environment/Daemons
Requires: %{name}%{?_isa} = %{version}-%{release}
%global backends %{backends} lua

%description backend-lua
This package contains the lua backend for %{name}

%package backend-sqlite
Summary: SQLite backend for %{name}
Group: System Environment/Daemons
Requires: %{name}%{?_isa} = %{version}-%{release}
BuildRequires: sqlite-devel
%global backends %{backends} gsqlite3

%description backend-sqlite
This package contains the SQLite backend for %{name}

%package backend-opendbx
Summary: OpenDBX backend for %{name}
Group: System Environment/Daemons
Requires: %{name}%{?_isa} = %{version}-%{release}
BuildRequires: opendbx-devel
%global backends %{backends} opendbx

%description backend-opendbx
This package contains the opendbx backend for %{name}

%package backend-geoip
Summary: GeoIP backend for %{name}
Group: System Environment/Daemons
Requires: %{name}%{?_isa} = %{version}-%{release}
BuildRequires: geoip-devel
BuildRequires: yaml-cpp-devel
%global backends %{backends} geoip

%description backend-geoip
This package contains the GeoIP backend for %{name}

%package backend-mydns
Summary: MyDNS backend for %{name}
Group: System Environment/Daemons
Requires: %{name}%{?_isa} = %{version}-%{release}
%global backends %{backends} mydns

%description backend-mydns
This package contains the MyDNS backend for %{name}

%package backend-tinydns
Summary: TinyDNS backend for %{name}
Group: System Environment/Daemons
Requires: %{name}%{?_isa} = %{version}-%{release}
BuildRequires: tinycdb-devel
%global backends %{backends} tinydns

%description backend-tinydns
This package contains the TinyDNS backend for %{name}

%package backend-lmdb
Summary: LMDB backend for %{name}
Group: System Environment/Daemons
Requires: %{name}%{?_isa} = %{version}-%{release}
BuildRequires: lmdb-devel
%global backends %{backends} lmdb

%description backend-lmdb
This package contains the LMDB backend for %{name}

%prep
%setup -q
%patch0 -p1 -b .default-config-patch
%patch1 -p1 -b .systemd-patch
%patch2 -p1 -b .disable-secpoll

%build
export CPPFLAGS="-DLDAP_DEPRECATED"

%configure \
	--sysconfdir=%{_sysconfdir}/%{name} \
	--disable-static \
	--disable-dependency-tracking \
	--disable-silent-rules \
	--with-modules='' \
	--with-system-polarssl \
	--with-lua \
	--with-dynmodules='%{backends}' \
	--enable-cryptopp \
	--enable-tools \
	--enable-remotebackend-zeromq \
	--enable-unit-tests

make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

%{__rm} -f %{buildroot}%{_libdir}/%{name}/*.la
%{__mv} %{buildroot}%{_sysconfdir}/%{name}/pdns.conf{-dist,}

chmod 600 %{buildroot}%{_sysconfdir}/%{name}/pdns.conf

# rename zone2ldap to pdns-zone2ldap (#1193116)
%{__mv} %{buildroot}/%{_bindir}/zone2ldap %{buildroot}/%{_bindir}/pdns-zone2ldap
%{__mv} %{buildroot}/%{_mandir}/man1/zone2ldap.1 %{buildroot}/%{_mandir}/man1/pdns-zone2ldap.1

# install systemd unit file
%{__install} -D -p -m 644 contrib/systemd-pdns.service %{buildroot}%{_unitdir}/%{name}.service

%check
make %{?_smp_mflags} -C pdns check

%pre
getent group pdns >/dev/null || groupadd -r pdns
getent passwd pdns >/dev/null || \
	useradd -r -g pdns -d / -s /sbin/nologin \
	-c "PowerDNS user" pdns
exit 0

%post
%systemd_post pdns.service

%preun
%systemd_preun pdns.service

%postun
%systemd_postun_with_restart pdns.service

%triggerun -- pdns < 3.0-rc3
# Save the current service runlevel info
# User must manually run systemd-sysv-convert --apply pdns
# to migrate them to systemd targets
%{_bindir}/systemd-sysv-convert --save pdns &>/dev/null ||:

# Run these because the SysV package being removed won't do them
/sbin/chkconfig --del pdns &>/dev/null || :
/bin/systemctl try-restart pdns.service &>/dev/null || :

%files
%doc COPYING README
%{_bindir}/pdns_control
%{_bindir}/pdnssec
%{_bindir}/pdns-zone2ldap
%{_bindir}/zone2sql
%{_bindir}/zone2json
%{_bindir}/zone2lmdb
%{_sbindir}/pdns_server
%{_libdir}/%{name}/libbindbackend.so
%{_mandir}/man1/pdns_control.1.gz
%{_mandir}/man1/pdns_server.1.gz
%{_mandir}/man1/zone2sql.1.gz
%{_mandir}/man1/pdns-zone2ldap.1.gz
%{_mandir}/man1/pdnssec.1.gz
%{_unitdir}/pdns.service
%dir %{_libdir}/%{name}/
%dir %{_sysconfdir}/%{name}/
%config(noreplace) %{_sysconfdir}/%{name}/pdns.conf

%files tools
%{_bindir}/dnsbulktest
%{_bindir}/dnsreplay
%{_bindir}/dnsscan
%{_bindir}/dnsscope
%{_bindir}/dnsdist
%{_bindir}/dnstcpbench
%{_bindir}/dnswasher
%{_bindir}/nproxy
%{_bindir}/nsec3dig
%{_bindir}/saxfr
%{_mandir}/man1/dnsreplay.1.gz
%{_mandir}/man1/dnsscope.1.gz
%{_mandir}/man1/dnswasher.1.gz
%{_mandir}/man1/dnstcpbench.1.gz
%{_mandir}/man1/dnsdist.1.gz

%files backend-mysql
%doc modules/gmysqlbackend/schema.mysql.sql
%doc modules/gmysqlbackend/dnssec-3.x_to_3.4.0_schema.mysql.sql
%doc modules/gmysqlbackend/nodnssec-3.x_to_3.4.0_schema.mysql.sql
%{_libdir}/%{name}/libgmysqlbackend.so

%files backend-postgresql
%doc modules/gpgsqlbackend/schema.pgsql.sql
%doc modules/gpgsqlbackend/dnssec-3.x_to_3.4.0_schema.pgsql.sql
%doc modules/gpgsqlbackend/nodnssec-3.x_to_3.4.0_schema.pgsql.sql
%{_libdir}/%{name}/libgpgsqlbackend.so

%files backend-pipe
%{_libdir}/%{name}/libpipebackend.so

%files backend-remote
%{_libdir}/%{name}/libremotebackend.so

%files backend-geo
%doc modules/geobackend/README
%{_libdir}/%{name}/libgeobackend.so

%files backend-ldap
%{_libdir}/%{name}/libldapbackend.so

%files backend-lua
%{_libdir}/%{name}/libluabackend.so

%files backend-sqlite
%doc modules/gsqlite3backend/schema.sqlite3.sql
%doc modules/gsqlite3backend/dnssec-3.x_to_3.4.0_schema.sqlite3.sql
%doc modules/gsqlite3backend/nodnssec-3.x_to_3.4.0_schema.sqlite3.sql
%{_libdir}/%{name}/libgsqlite3backend.so

%files backend-opendbx
%{_libdir}/%{name}/libopendbxbackend.so

%files backend-geoip
%{_libdir}/%{name}/libgeoipbackend.so

%files backend-mydns
%{_libdir}/%{name}/libmydnsbackend.so

%files backend-tinydns
%{_libdir}/%{name}/libtinydnsbackend.so

%files backend-lmdb
%{_libdir}/%{name}/liblmdbbackend.so

%changelog
* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 3.4.6-2
- 更新到 3.4.6

* Sat Jul 25 2015 Liu Di <liudidi@gmail.com> - 3.4.5-1
- 更新到 3.4.5

* Thu Apr 16 2015 Liu Di <liudidi@gmail.com> - 3.4.3-2
- 为 Magic 3.0 重建

* Mon Mar 02 2015 Morten Stevens <mstevens@imt-systems.com> - 3.4.3-1
- Update to 3.4.3

* Tue Feb 17 2015 Morten Stevens <mstevens@imt-systems.com> - 3.4.2-2
- Rename zone2ldap to pdns-zone2ldap (#1193116)
- Remove rpath workaround

* Sat Feb 07 2015 Morten Stevens <mstevens@imt-systems.com> - 3.4.2-1
- Update to 3.4.2
- Disable security status polling by default

* Tue Jan 27 2015 Petr Machata <pmachata@redhat.com> - 3.4.1-2
- Rebuild for boost 1.57.0

* Mon Nov 03 2014 Morten Stevens <mstevens@imt-systems.com> - 3.4.1-1
- Update to 3.4.1
- Enable security status polling

* Fri Oct 10 2014 Ruben Kerkhof <ruben@rubenkerkhof.com> - 3.4.0-5
- Run the unit tests during check

* Mon Oct 06 2014 Morten Stevens <mstevens@imt-systems.com> - 3.4.0-4
- Enable backend LMDB

* Mon Oct 06 2014 Morten Stevens <mstevens@imt-systems.com> - 3.4.0-3
- Remove unused build dependency

* Thu Oct 02 2014 Morten Stevens <mstevens@imt-systems.com> - 3.4.0-2
- Enable backend: GeoIP, MyDNS, TinyDNS

* Tue Sep 30 2014 Morten Stevens <mstevens@imt-systems.com> - 3.4.0-1
- Update to 3.4.0

* Tue Sep 23 2014 Morten Stevens <mstevens@imt-systems.com> - 3.4.0-0.3.rc2
- Update to 3.4.0-rc2

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.0-0.2.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Aug 01 2014 Morten Stevens <mstevens@imt-systems.com> - 3.4.0-0.1.rc1
- Update to 3.4.0-rc1
- Enable zeromq remote backend

* Mon Jul 14 2014 Morten Stevens <mstevens@imt-systems.com> - 3.3.1-6
- Rebuild for PolarSSL 1.3.8

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 23 2014 Petr Machata <pmachata@redhat.com> - 3.3.1-4
- Rebuild for boost 1.55.0

* Fri May 02 2014 Morten Stevens <mstevens@imt-systems.com> - 3.3.1-3
- Rebuild for PolarSSL 1.3.6

* Mon Mar 17 2014 Morten Stevens <mstevens@imt-systems.com> - 3.3.1-2
- Enable OpenDBX backend, thanks to Jean-Eudes Onfray (rhbz#1075490)

* Tue Dec 17 2013 Morten Stevens <mstevens@imt-systems.com> - 3.3.1-1
- Update to latest upstream release 3.3.1
- Add LUA backend
- Add polarssl-devel as build dependency

* Sun Oct 13 2013 Morten Stevens <mstevens@imt-systems.com> - 3.3-6
- Enable remotebackend-http

* Sat Aug 31 2013 Morten Stevens <mstevens@imt-systems.com> - 3.3-5
- Add patch to fix Remote backend

* Wed Aug 21 2013 Morten Stevens <mstevens@imt-systems.com> - 3.3-4
- Add Remote backend

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 27 2013 pmachata@redhat.com - 3.3-2
- Rebuild for boost 1.54.0

* Fri Jul 05 2013 Morten Stevens <mstevens@imt-systems.com> - 3.3-1
- Update to 3.3

* Fri Jun 28 2013 Morten Stevens <mstevens@imt-systems.com> - 3.3-0.3.rc2
- Update to 3.3-rc2
- Add extra tools package for pdns

* Tue Jun 04 2013 Morten Stevens <mstevens@imt-systems.com> - 3.3-0.2.rc1
- Update systemd unit file
- Spec cleanup

* Tue May 28 2013 Morten Stevens <mstevens@imt-systems.com> - 3.3-0.1.rc1
- Update to 3.3-rc1

* Mon Apr 22 2013 Morten Stevens <mstevens@imt-systems.com> - 3.2-7
- Disarm dead code that causes gcc crashes on ARM (rhbz#954191)

* Tue Apr 09 2013 Morten Stevens <mstevens@imt-systems.com> - 3.2-6
- Add support for aarch64 (rhbz#926316)

* Tue Mar 05 2013 Ruben Kerkhof <ruben@rubenkerkhof.com> - 3.2-5
- Enable hardened build as per http://fedoraproject.org/wiki/Packaging:Guidelines#PIE

* Mon Feb 11 2013 Ruben Kerkhof <ruben@rubenkerkhof.com> - 3.2-4
- Enable PrivateTmp as per http://fedoraproject.org/wiki/Features/ServicesPrivateTmp
- Fix bogus date in changelog

* Sun Feb 10 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 3.2-3
- Rebuild for Boost-1.53.0

* Sat Feb 09 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 3.2-2
- Rebuild for Boost-1.53.0

* Thu Jan 17 2013 Morten Stevens <mstevens@imt-systems.com> - 3.2-1
- Update to 3.2

* Mon Jan 07 2013 Morten Stevens <mstevens@imt-systems.com> - 3.1-7
- Disable pdns guardian by default (rhbz#883852)
- Drop backend MongoDB as it does not work (upstream commit 3017)

* Thu Nov 22 2012 Ruben Kerkhof <ruben@rubenkerkhof.com> - 3.1-6
- Add example schemas to documentation

* Fri Oct 19 2012 Morten Stevens <mstevens@imt-systems.com> - 3.1-5
- Fixed permissions of pdns.conf file (rhbz#646510)
- Set bind as default backend

* Mon Sep 24 2012 Morten Stevens <mstevens@imt-systems.com> - 3.1-4
- use new systemd rpm macros (rhbz#850266)

* Mon Sep 24 2012 Morten Stevens <mstevens@imt-systems.com> - 3.1-3
- Fix pdns daemon exit code (rhbz#859898)
- Update systemd unit file

* Tue Sep 18 2012 Morten Stevens <mstevens@imt-systems.com> - 3.1-2
- Fix MongoDB backend

* Mon Sep 17 2012 Morten Stevens <mstevens@imt-systems.com> - 3.1-1
- Update to 3.1
- Remove MongoDB backend due build problems

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.1-2
- Rebuilt for c++ ABI breakage

* Mon Jan 09 2012 Ruben Kerkhof <ruben@rubenkerkhof.com> 3.0.1-1
- CVE-2012-0206

* Sun Aug 07 2011 Dan Horák <dan@danny.cz> - 3.0-7
- mongodb supports only x86

* Mon Jul 25 2011 Ruben Kerkhof <ruben@rubenkerkhof.com> 3.0-6
- Upstream released new version

* Wed Jul 20 2011 Ruben Kerkhof <ruben@rubenkerkhof.com> 3.0-5.rc3
- New release candidate
- Add MongoDB backend
- Enable LUA support
- Convert to systemd

* Sat Apr 09 2011 Ruben Kerkhof <ruben@rubenkerkhof.com> 3.0-4.pre.20110327.2103.fc16
- Rebuilt for new boost

* Mon Mar 28 2011 Ruben Kerkhof <ruben@rubenkerkhof.com> 3.0-3.pre.20110327.2103
- License file moved a directory up
- Add pdnssec and dnsreplay commands

* Mon Mar 28 2011 Ruben Kerkhof <ruben@rubenkerkhof.com> 3.0-2.pre.20110327.2103
- Add lua BuildRequires

* Mon Mar 28 2011 Ruben Kerkhof <ruben@rubenkerkhof.com> 3.0-1.pre.20110327.2103
- Upstream released new pre-release version
- Now with DNSSEC support
- Drop merged patches

* Wed Mar 23 2011 Dan Horák <dan@danny.cz> - 2.9.22-13
- rebuilt for mysql 5.5.10 (soname bump in libmysqlclient)

* Wed Mar 23 2011 Ruben Kerkhof <ruben@rubenkerkhof.com> 2.9.22-12
- Rebuilt for new mysqlclient

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.22-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 14 2010 Ruben Kerkhof <ruben@rubenkerkhof.com> 2.9.22-10
- Fix crash on SIGSTOP and SIGCONT, thanks to Anders Kaseorg (#652841)

* Thu Jan 14 2010 Ruben Kerkhof <ruben@rubenkerkhof.com> 2.9.22-9
- Fix changelog entry

* Thu Jan 14 2010 Ruben Kerkhof <ruben@rubenkerkhof.com> 2.9.22-8
- Fix postgres lib detection (#555462)

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 2.9.22-7
- rebuilt with new openssl

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.22-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Ruben Kerkhof <ruben@rubenkerkhof.com> - 2.9.22-5
- Fix build with gcc4.4

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.22-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jan 26 2009 Ruben Kerkhof <ruben@rubenkerkhof.com> 2.9.22-3
- Upstream released new version

* Fri Jan 23 2009 Ruben Kerkhof <ruben@rubenkerkhof.com> 2.9.22-2.rc3
- Rebuild for new libmysqlclient

* Mon Jan 19 2009 Ruben Kerkhof <ruben@rubenkerkhof.com> 2.9.22-1.rc3
- New release candidate

* Wed Dec 03 2008 Ruben Kerkhof <ruben@rubenkerkhof.com> 2.9.22-1.rc2
- Upstream released new release candidate
- Drop patches which are upstreamed

* Mon Nov 17 2008 Ruben Kerkhof <ruben@rubenkerkhof.com> 2.9.21.2-1
- Upstream released new version

* Fri Sep 12 2008 Ruben Kerkhof <ruben@rubenkerkhof.com> 2.9.21.1-2
- Fix handling of AAAA records (bz #461768)

* Wed Aug 06 2008 Ruben Kerkhof <ruben@rubenkerkhof.com> 2.9.21.1-1
- CVE-2008-3337

* Sat Feb 09 2008 Ruben Kerkhof <ruben@rubenkerkhof.com> 2.9.21-4
- GCC 4.3 fixes

* Wed Dec 05 2007 Ruben Kerkhof <ruben@rubenkerkhof.com> 2.9.21-3
- Rebuild to pick up new openldap

* Tue Sep 11 2007 Ruben Kerkhof <ruben@rubenkerkhof.com> 2.9.21-2
- Fix license tag
- Add README for geo backend to docs

* Tue Apr 24 2007 Ruben Kerkhof <ruben@rubenkerkhof.com> 2.9.21-1
- Upstream released 2.9.21
- Enabled new SQLite backend

* Tue Apr 10 2007 <ruben@rubenkerkhof.com> 2.9.20-9
- Add Requires for chkconfig, service and useradd (#235582)

* Mon Jan 1 2007 <ruben@rubenkerkhof.com> 2.9.20-8
- Add the pdns user and group to the config file
- Don't restart pdns on an upgrade
- Minor cleanups in scriptlets

* Mon Jan 1 2007 <ruben@rubenkerkhof.com> 2.9.20-7
- Fixed typo in scriptlet

* Mon Jan 1 2007 <ruben@rubenkerkhof.com> 2.9.20-6
- Check if user pdns exists before adding it

* Sat Dec 30 2006 <ruben@rubenkerkhof.com> 2.9.20-5
- Strip rpath from the backends as well

* Fri Dec 29 2006 <ruben@rubenkerkhof.com> 2.9.20-4
- Disable rpath

* Thu Dec 28 2006 <ruben@rubenkerkhof.com> 2.9.20-3
- More fixes as per review #219973

* Wed Dec 27 2006 <ruben@rubenkerkhof.com> 2.9.20-2
- A few changes for FE review (bz #219973):
- Renamed package to pdns, since that's how upstream calls it
- Removed calls to ldconfig
- Subpackages now require %%{version}-%%{release}

* Sat Dec 16 2006 <ruben@rubenkerkhof.com> 2.9.20-1
- Initial import
