Summary: PPP Over Ethernet (xDSL support)
Summary(zh_CN.UTF-8): 以太网客户机上的 PPP(用于 xDSL 支持)
Name: rp-pppoe
Version: 3.10
Release: 10%{?dist}
License: GPL
Group: System Environment/Daemons
Group(zh_CN.UTF-8): 系统环境/服务
Source: http://www.roaringpenguin.com/penguin/pppoe/rp-pppoe-3.10.tar.gz
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
cd src
./configure --mandir=%{_mandir}

%build
cd src
make
cd ../gui
make

%install
umask 022
cd src
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/etc/init.d
test -f $RPM_BUILD_ROOT/etc/init.d/pppoe || cp ../scripts/pppoe-init $RPM_BUILD_ROOT/etc/init.d/pppoe
chmod 755 $RPM_BUILD_ROOT/etc/init.d/pppoe
cd ../gui
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT/etc/ppp/pppoe.conf-3.10
rm -f $RPM_BUILD_ROOT/etc/ppp/firewall-masq-3.10
rm -f $RPM_BUILD_ROOT/etc/ppp/firewall-standalone-3.10
rm -f $RPM_BUILD_ROOT/etc/ppp/pppoe-server-options-example

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc doc/CHANGES doc/HOW-TO-CONNECT doc/LICENSE doc/KERNEL-MODE-PPPOE README SERVPOET
%config(noreplace) /etc/ppp/pppoe.conf
%config(noreplace) /etc/ppp/pppoe-server-options
%config(noreplace) /etc/ppp/firewall-masq
%config(noreplace) /etc/ppp/firewall-standalone
/etc/rc.d/init.d/pppoe
/etc/ppp/plugins/*
/usr/sbin/pppoe
/usr/sbin/pppoe-server
/usr/sbin/pppoe-sniff
/usr/sbin/pppoe-relay
/usr/sbin/pppoe-connect
/usr/sbin/pppoe-start
/usr/sbin/pppoe-stop
/usr/sbin/pppoe-setup
/usr/sbin/pppoe-status
%{_mandir}/man5/pppoe.conf.5*
%{_mandir}/man8/pppoe.8*
%{_mandir}/man8/pppoe-server.8*
%{_mandir}/man8/pppoe-relay.8*
%{_mandir}/man8/pppoe-sniff.8*
%{_mandir}/man8/pppoe-connect.8*
%{_mandir}/man8/pppoe-start.8*
%{_mandir}/man8/pppoe-stop.8*
%{_mandir}/man8/pppoe-status.8*
%{_mandir}/man8/pppoe-setup.8*
/etc/init.d/pppoe
%dir /etc/ppp/rp-pppoe-gui
/usr/sbin/pppoe-wrapper
/usr/bin/tkpppoe
%{_mandir}/man1/tkpppoe.1*
%{_mandir}/man1/pppoe-wrapper.1*
/usr/share/tkpppoe/tkpppoe.html
/usr/share/tkpppoe/mainwin-busy.png
/usr/share/tkpppoe/mainwin-nonroot.png
/usr/share/tkpppoe/mainwin.png
/usr/share/tkpppoe/props-advanced.png
/usr/share/tkpppoe/props-basic.png
/usr/share/tkpppoe/props-nic.png
/usr/share/tkpppoe/props-options.png
/usr/share/tkpppoe/en.msg
/usr/share/tkpppoe/ja.msg
%post
%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 3.10-10
- 为 Magic 3.0 重建

