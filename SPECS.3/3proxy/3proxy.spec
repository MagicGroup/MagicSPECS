# To build on Fedora 14 due to https://bugzilla.redhat.com/show_bug.cgi?id=715580
#% global _unitdir /lib/systemd/system

Name:		3proxy
Version:		0.6.1
Release:		16%{?dist}

Summary:		Tiny but very powerful proxy
Summary(zh_CN.UTF-8):	一个小而功能强大的代理服务软件

License:		BSD or ASL 2.0 or GPLv2+ or LGPLv2+
Group:		System Environment/Daemons
Group(zh_CN.UTF-8):	系统环境/服务
Url:			http://3proxy.ru/?l=EN

Source0:		http://3proxy.ru/%{version}/%{name}-%{version}.tgz
Source1:		3proxy.init
Source2:		3proxy.cfg
Source3:		3proxy.service
# EPEL still require it
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	dos2unix
Requires:		initscripts systemd

# I correct config path in man only. It is fully Fedora related.
Patch0:		3proxy-0.6.1-config-path.patch

# Systemd compliant: https://fedoraproject.org/wiki/Systemd_Packaging_Draft
# https://fedoraproject.org/wiki/Packaging:Systemd
# https://fedoraproject.org/wiki/Packaging:ScriptletSnippets#Systemd
BuildRequires:			systemd-devel


%description
%{name} -- light proxy server.
Universal proxy server with HTTP, HTTPS, SOCKS v4, SOCKS v4a, SOCKS v5, FTP,
POP3, UDP and TCP portmapping, access control, bandwith control, traffic
limitation and accounting based on username, client IP, target IP, day time,
day of week, etc.

%description -l zh_CN.UTF-8
%{name} -- 轻量级的代理服务器。
支持 HTTP, HTTPS, SOCKS v4, SOCKS v4, SOCKS v4a, SOCKS v5, FTP, POP3,UDP 
和 TCP 端口映射，访问控制，带宽控制，流量限制及基于用户名，客户端 IP, 目
标 IP，日期的账号控制的通用代理服务器。

%prep
%setup -q

%patch0 -p0 -b .man-cfg

# To use "magic" CFLAGS (exported)
sed -i -e "s/CFLAGS =/CFLAGS +=/" Makefile.Linux

dos2unix Changelog

%build
%{__make} -f Makefile.Linux

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_sysconfdir}
mkdir -p %{buildroot}%{_sysconfdir}/NetworkManager/dispatcher.d/
mkdir -p %{buildroot}%{_mandir}/man{3,8}
mkdir -p %{buildroot}%{_localstatedir}/log/%{name}
install -m755 -D src/%{name} %{buildroot}%{_bindir}/%{name}
install -m755 -D src/dighosts %{buildroot}%{_bindir}/dighosts
install -m755 -D src/ftppr %{buildroot}%{_bindir}/ftppr
install -m755 -D src/mycrypt %{buildroot}%{_bindir}/mycrypt
install -m755 -D src/pop3p %{buildroot}%{_bindir}/pop3p
install -m755 -D src/%{name} %{buildroot}%{_bindir}/%{name}
install -m755 -D src/proxy %{buildroot}%{_bindir}/htproxy
install -m755 -D src/socks %{buildroot}%{_bindir}/socks
install -m755 -D src/tcppm %{buildroot}%{_bindir}/tcppm
install -m755 -D src/udppm %{buildroot}%{_bindir}/udppm

install -pD -m644 %{SOURCE2} %{buildroot}/%{_sysconfdir}/%{name}.cfg
install -pD -m755 %{SOURCE3} %{buildroot}/%{_unitdir}/%{name}.service

	for man in man/*.{3,8} ; do
	install "$man" "%{buildroot}%{_mandir}/man${man:(-1)}/"
	done

cat > %{buildroot}%{_sysconfdir}/NetworkManager/dispatcher.d/40-%{name} <<EOF
#!/bin/sh

	if [ "\$2" = "up" ]; then
	/sbin/service %{name} condrestart || : # reload doesn't work
	fi
EOF

%clean
rm -rf %{buildroot}

%post
	if [ $1 -eq 1 ]; then
	# Initial installation
	/bin/systemctl daemon-reload >/dev/null 2>&1 || :
	fi

%preun
	if [ $1 -eq 0 ] ; then
	# Package removal, not upgrade
	/bin/systemctl --no-reload disable %{name}.service > /dev/null 2>&1 || :
	/bin/systemctl stop %{name}.service > /dev/null 2>&1 || :
	fi

%postun
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
	if [ $1 -ge 1 ] ; then
	# Package upgrade, not uninstall
	/bin/systemctl try-restart %{name}.service >/dev/null 2>&1 || :
	fi

%triggerun -- %{name} < 0.6.1-10
# Save the current service runlevel info
# User must manually run systemd-sysv-convert --apply httpd
# to migrate them to systemd targets
%{_bindir}/systemd-sysv-convert --save %{name} >/dev/null 2>&1 ||:

# Run these because the SysV package being removed won't do them
/sbin/chkconfig --del %{name} >/dev/null 2>&1 || :
/bin/systemctl try-restart %{name}.service >/dev/null 2>&1 || :

%files
%defattr(-,root,root,-)
%{_bindir}/*
%config(noreplace) %{_sysconfdir}/%{name}.cfg
%attr(0755,root,root) %config %{_sysconfdir}/NetworkManager/dispatcher.d/40-%{name}
%{_localstatedir}/log/%{name}
%doc Readme Changelog authors copying news
%{_mandir}/man8/*.8.gz
%{_mandir}/man3/*.3.gz
%{_unitdir}/%{name}.service

%changelog
* Sat May 11 2013 Liu Di <liudidi@gmail.com> - 0.6.1-14
- 重新编译

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 0.6.1-13
- 为 Magic 3.0 重建

* Wed Oct 19 2011 Liu Di <liudidi@gmail.com> - 0.6.1-12
- 从 fc 移植 spec
- 添加中文描述
