Summary: Lightweight, fast and secure FTP server
Summary(zh_CN.UTF-8): 轻量、快速和安全的 FTP 服务器
Name: pure-ftpd
Version:	1.0.42
Release:	1%{?dist}
License: GPL
Group: System Environment/Daemons
URL: http://www.pureftpd.org/

Packager: sejishikong <sejishikong@263.net>

Source: ftp://ftp.pureftpd.org/pub/pure-ftpd/releases/%{name}-%{version}.tar.bz2
BuildRoot: %{_tmppath}/root-%{name}-%{version}
Prefix: %{_prefix}

BuildRequires: pam-devel, openldap-devel, zlib-devel
BuildRequires: scrollkeeper

Requires(post): scrollkeeper

Provides: ftp-server
Provides: pureftpd
Conflicts: wu-ftpd proftpd ftpd in.ftpd anonftp publicfile wuftpd ftpd-BSD

%description
Pure-FTPd is a fast, production-quality, standard-comformant FTP server,
based upon Troll-FTPd. Unlike other popular FTP servers, it has no known
security flaw, it is really trivial to set up and it is especially designed
for modern Linux and FreeBSD kernels (setfsuid, sendfile, capabilities) .
Features include chroot()ed and/or virtual chroot()ed home directories,
virtual domains, built-in 'ls', anti-warez system, bounded ports for passive
downloads, FXP protocol, bandwidth throttling, ratios, LDAP / MySQL /
PostgreSQL-based authentication, fortune files, Apache-like log files, fast
standalone mode, text / HTML / XML real-time status report, virtual users,
virtual quotas, privilege separation and more.

%description -l zh_CN.UTF-8
轻量、快速和安全的 FTP 服务器。

%prep
%setup -n %{name}-%{version}

%build
%configure \
	--with-language=simplified-chinese \
        --with-pam --with-pgsql --with-mysql --with-ldap --with-extauth --with-capabilities --with-ascii --with-sendfile \
        --with-puredb --with-quotas --with-uploadscript --with-virtualhosts --with-virtualchroot --with-altlog --with-cookie \
        --with-throttling --with-ratios --with-ftpwho --with-diraliases --with-peruserlimits --with-largefile --with-boring \
        --with-privsep --with-sysquotas --with-paranoidmsg --with-rfc2640
make

%install
rm -rf %{buildroot}
install -d -m0755 %{buildroot}%{_sysconfdir}/pure-ftpd/ \
			%{buildroot}%{_sysconfdir}/pam.d/ \
			%{buildroot}%{_sbindir} \
			%{buildroot}%{_initrddir}
%makeinstall
install -m0755 configuration-file/pure-config.pl %{buildroot}%{_sbindir}
install -m0644 configuration-file/pure-ftpd.conf %{buildroot}%{_sysconfdir}

sed -e "s|/usr/local|%{_prefix}|g; s|/etc/sysconfig|%{_sysconfdir}/sysconfig|g" contrib/redhat.init >redhat.init_replaced
install -m0755 redhat.init_replaced %{buildroot}%{_initrddir}/pure-ftpd

sed -e "s|\(\$prefix *= *['\"]\)/usr/local|\1%{_prefix}|g" configuration-file/pure-config.pl >pure-config.pl_replaced
install -m0755 pure-config.pl_replaced %{buildroot}%{_sbindir}/pure-config.pl

install -m0644 pam/pure-ftpd %{buildroot}%{_sysconfdir}/pam.d/

%post
/sbin/chkconfig --add pure-ftpd

%preun
usermod -u 101 ftp
groupmod -g 101 ftp
if [ $1 -eq 0 ]; then
	/sbin/service pure-ftpd stop >/dev/null 2>&1 || :
	/sbin/chkconfig --del pure-ftpd
fi

%postun
/sbin/service pure-ftpd condrestart >/dev/null 2>&1 || :

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc AUTHORS CONTACT FAQ HISTORY NEWS pureftpd.schema pureftpd-*.conf README* THANKS
%doc %{_mandir}/man8/*
%config %{_sysconfdir}/pure-ftpd.conf
%config %{_sysconfdir}/pure-ftpd/
%config(noreplace) %{_initrddir}/pure-ftpd
%config(noreplace) %{_sysconfdir}/pam.d/*
%{_sbindir}/*
%{_bindir}/*

%changelog
* Mon Aug 10 2015 Liu Di <liudidi@gmail.com> - 1.0.42-1
- 更新到 1.0.42

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 1.0.35-3
- 为 Magic 3.0 重建

* Wed Apr 26 2006 liudi <liudidi@gmail.com>
- Update to 1.0.21
* Tue Aug 16 2005 sejishikong<sejishikong@263.net>
- Initial package. For magiclinux 2.0 beta 3
