Summary: PPP Over Ethernet (xDSL support)
Summary(zh_CN.UTF-8): 以太网客户机上的 PPP(用于 xDSL 支持)
Name: rp-pppoe
Version:	3.11
Release:	2%{?dist}
License: GPL
Group: System Environment/Daemons
Group(zh_CN.UTF-8): 系统环境/服务
Source0: http://www.roaringpenguin.com/files/download/rp-pppoe-%{version}.tar.gz
Source1: pppoe-connect
Source2: pppoe-setup
Source3: pppoe-start
Source4: pppoe-status
Source5: pppoe-stop
Source6: pppoe-server.service

Patch0: rp-pppoe-3.8-redhat.patch
Patch1: rp-pppoe-3.11-ip-allocation.patch
Url: http://www.roaringpenguin.com/pppoe/
Packager: David F. Skoll <dfs@roaringpenguin.com>
BuildRoot: /tmp/pppoe-build
Vendor: Roaring Penguin Software Inc.
Requires: ppp >= 2.3.7

# LIC: GPL
%description
PPPoE (Point-to-Point Protocol over Ethernet) is a protocol used by
many DSL Internet Service Providers. Roaring Penguin has a free
client for Linux systems to connect to PPPoE service providers.

The client is a user-mode program and does not require any kernel
modifications. It is fully compliant with RFC 2516, the official PPPoE
specification.
%description -l zh_CN.UTF-8
PPPoE(以太网上的点对点协议)是一个被许多 ADSL 互联网服务提供者使用的协议。
该软件包包括 Roaring Penguin PPPoE 客户，一个不需要内核修改的用户模式程
序。它完全符合正式的 PPPoE 明细表 RFC 2516 的标准。

%prep
%setup
%patch0 -p1 -b .config
%patch1 -p1 -b .ip-allocation

# configure honors docdir, but Makefile.in doesn't
sed -i -e 's,^docdir=.*$,docdir=@docdir@,' src/Makefile.in

%build
cd src
autoconf
export CFLAGS="%{optflags} -D_GNU_SOURCE -fno-strict-aliasing"
%configure --docdir=%{_pkgdocdir}
make

%install
mkdir -p %{buildroot}%{_sbindir} %{buildroot}%{_unitdir}

make -C src install DESTDIR=%{buildroot}

install -m 0755 %{SOURCE1} %{buildroot}%{_sbindir}
install -m 0755 %{SOURCE2} %{buildroot}%{_sbindir}
install -m 0755 %{SOURCE3} %{buildroot}%{_sbindir}
install -m 0755 %{SOURCE4} %{buildroot}%{_sbindir}
install -m 0755 %{SOURCE5} %{buildroot}%{_sbindir}
install -m 0644 %{SOURCE6} %{buildroot}%{_unitdir}/pppoe-server.service

ln -sf pppoe-stop %{buildroot}%{_sbindir}/adsl-stop
ln -sf pppoe-start %{buildroot}%{_sbindir}/adsl-start

rm -rf %{buildroot}/etc/ppp/pppoe.conf \
       %{buildroot}/etc/rc.d/init.d/pppoe \
       %{buildroot}%{_sysconfdir}/ppp/plugins

%post
%systemd_post pppoe-server.service

%preun
%systemd_preun pppoe-server.service

%postun
%systemd_postun_with_restart pppoe-server.service

%files
%doc scripts/pppoe-connect scripts/pppoe-setup scripts/pppoe-init
%doc scripts/pppoe-start scripts/pppoe-status scripts/pppoe-stop
%doc configs
%config(noreplace) %{_sysconfdir}/ppp/pppoe-server-options
%config(noreplace) %{_sysconfdir}/ppp/firewall*
%{_unitdir}/pppoe-server.service
%{_sbindir}/*
%{_mandir}/man?/*
%{_docdir}/*

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 3.11-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 3.11-1
- 更新到 3.11

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 3.10-10
- 为 Magic 3.0 重建

