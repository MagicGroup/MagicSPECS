%define git 1
%define vcsdate 20151104

Name:		shadowsocks-libev
Version:	2.3.3
Release:	5%{?dist}
Summary:	Libev port of shadowsocks
Summary(zh_CN.UTF-8): shadowsocks 的 libev 移植版本

Group:		Applications/Internet
Group(zh_CN.UTF-8): 应用程序/互联网
License:	GPLv3+
URL:		https://github.com/madeye/shadowsocks-libev
%if 0%{?git}
Source0:	%{name}-git%{vcsdate}.tar.xz
%else
Source0:	https://github.com/madeye/shadowsocks-libev/archive/v%{version}.tar.gz
%endif
Source1:	make_shadowsocks-libev_git_package.sh
#Source2:	shadowsocks-config.json
Source3:	shadowsocks-server@.service
Source4:	shadowsocks@.service

BuildRequires:	curl-devel zlib-devel openssl-devel perl perl-devel cpio expat-devel gettext-devel
Requires:	curl

%description
Shadowsocks-libev is writen in pure C and only depends on libev and openssl or polarssl.

In normal usage, the memory consumption is about 600KB and the CPU utilization is no more 
than 5% on a low-end router (Buffalo WHR-G300N V2 with a 400MHz MIPS CPU, 32MB memory and 
4MB flash).

%description -l zh_CN.UTF-8
一个 socks 代理工具。

%prep
%if 0%{?git}
%setup -q -n %{name}-git%{vcsdate}
%else
%setup -q
%endif

%build
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
mkdir -p %{buildroot}%{_sysconfdir}/shadowsocks/
mkdir -p %{buildroot}%{_unitdir}
install -m 755 %{SOURCE3} %{buildroot}%{_unitdir}
install -m 755 %{SOURCE4} %{buildroot}%{_unitdir}
rm -f %{buildroot}%{_libdir}/*.la

%files
%doc
%{_bindir}/ss-*
%{_mandir}/man1/ss*1*
%{_mandir}/man8/shadowsocks-libev.8*
%{_sysconfdir}/shadowsocks
%{_unitdir}/*.service

#devel
%{_includedir}/shadowsocks.h
%{_libdir}/libshadowsocks.a
%{_libdir}/pkgconfig/shadowsocks-libev.pc


%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 2.3.3-5
- 更新到 20151104 日期的仓库源码

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 2.3.3-4
- 为 Magic 3.0 重建

* Sun Sep 27 2015 Liu Di <liudidi@gmail.com> - 2.3.3-3
- 更新到 20150927 日期的仓库源码

* Sun Sep 27 2015 Liu Di <liudidi@gmail.com> - 2.3.3-2
- 为 Magic 3.0 重建

* Sun Mar 09 2014 Liu Di <liudidi@gmail.com> - 1.4.3-3
- 更新到 20140309 日期的仓库源码



