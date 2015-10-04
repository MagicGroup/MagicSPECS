Summary: A security tool which acts as a wrapper for TCP daemons
Summary(zh_CN.UTF-8): 工作起来如同 TCP 守护进程的安全工具
Name: tcp_wrappers
Version: 7.6
Release: 63%{?dist}

%define LIB_MAJOR 0
%define LIB_MINOR 7
%define LIB_REL 6

License: BSD
Group: System Environment/Daemons
Group(zh_CN.UTF-8): 系统环境/服务
Source: ftp://ftp.porcupine.org/pub/security/%{name}_%{version}.tar.gz
URL: ftp://ftp.porcupine.org/pub/security/index.html
Patch0: tcpw7.2-config.patch
Patch1: tcpw7.2-setenv.patch
Patch2: tcpw7.6-netgroup.patch
Patch3: tcp_wrappers-7.6-bug11881.patch
Patch4: tcp_wrappers-7.6-bug17795.patch
Patch5: tcp_wrappers-7.6-bug17847.patch
Patch6: tcp_wrappers-7.6-fixgethostbyname.patch
Patch7: tcp_wrappers-7.6-docu.patch
Patch8: tcp_wrappers-7.6-man.patch
Patch9: tcp_wrappers.usagi-ipv6.patch
Patch10: tcp_wrappers.ume-ipv6.patch
Patch11: tcp_wrappers-7.6-shared.patch
Patch12: tcp_wrappers-7.6-sig.patch
Patch13: tcp_wrappers-7.6-strerror.patch
Patch14: tcp_wrappers-7.6-ldflags.patch
Patch15: tcp_wrappers-7.6-fix_sig-bug141110.patch
Patch16: tcp_wrappers-7.6-162412.patch
Patch17: tcp_wrappers-7.6-220015.patch
Patch18: tcp_wrappers-7.6-restore_sigalarm.patch
Patch19: tcp_wrappers-7.6-siglongjmp.patch
Patch20: tcp_wrappers-7.6-sigchld.patch
Patch21: tcp_wrappers-7.6-196326.patch
Patch22: tcp_wrappers_7.6-249430.patch
Patch23: tcp_wrappers-7.6-inetdconf.patch
# required by sin_scope_id in ipv6 patch
BuildRequires: glibc-devel >= 2.2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: tcp_wrappers-libs = %{version}-%{release}

%description
The tcp_wrappers package provides small daemon programs which can
monitor and filter incoming requests for systat, finger, FTP, telnet,
rlogin, rsh, exec, tftp, talk and other network services.

Install the tcp_wrappers program if you need a security tool for
filtering incoming network services requests.

This version also supports IPv6.

%description -l zh_CN.UTF-8
tcp_wrappers 软件包提供了小型的守护进程程序。它们能够为 systat、finger、
FTP、telnet、rlogin、rsh、exec、 tftp、talk、以及其它网络服务监视和过滤
进入的请求。 如果您需要一个用来过滤进入的网络服务请求的安全工具，请安装
tcp_wrappers 程序。

%package libs
Summary: Libraries for tcp_wrappers
Summary(zh_CN.UTF-8): tcp_wrappers 的库
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库

%description libs
tcp_wrappers-libs contains the libraries of the tcp_wrappers package.

%description libs -l zh_CN.UTF-8
tcp_wrappers 的库。

%package devel
Summary: Development libraries and headers for tcp_wrappers
Summary(zh_CN.UTF-8): tcp_wrappers 的开发库和头文件
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: tcp_wrappers-libs = %{version}-%{release}

%description devel
tcp_wrappers-devel contains the libraries and header files needed to
develop applications with tcp_wrappers support.

%description devel -l zh_CN.UTF-8
tcp_wrappers 的开发库和头文件。

%prep
%setup -q -n %{name}_%{version}
%patch0 -p1 -b .config
%patch1 -p1 -b .setenv
%patch2 -p1 -b .netgroup
%patch3 -p1 -b .bug11881
%patch4 -p1 -b .bug17795
%patch5 -p1 -b .bug17847
%patch6 -p1 -b .fixgethostbyname
%patch7 -p1 -b .docu
%patch8 -p1 -b .man
%patch9 -p1 -b .usagi-ipv6
%patch10 -p1 -b .ume-ipv6
%patch11 -p1 -b .shared
%patch12 -p1 -b .sig
%patch13 -p1 -b .strerror
%patch14 -p1 -b .cflags
%patch15 -p1 -b .fix_sig
%patch16 -p1 -b .162412
%patch17 -p1 -b .220015
%patch18 -p1 -b .restore_sigalarm
%patch19 -p1 -b .siglongjmp
%patch20 -p1 -b .sigchld
%patch21 -p1 -b .196326
%patch22 -p1 -b .249430
%patch23 -p1 -b .inetdconf

%build
make RPM_OPT_FLAGS="$RPM_OPT_FLAGS -fPIC -DPIC -D_REENTRANT -DHAVE_STRERROR" LDFLAGS="-pie" MAJOR=%{LIB_MAJOR} MINOR=%{LIB_MINOR} REL=%{LIB_REL} linux


%install
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{_includedir}
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man{3,5,8}
mkdir -p ${RPM_BUILD_ROOT}%{_sbindir}

install -p -m644 hosts_access.3 ${RPM_BUILD_ROOT}%{_mandir}/man3
install -p -m644 hosts_access.5 hosts_options.5 ${RPM_BUILD_ROOT}%{_mandir}/man5
install -p -m644 tcpd.8 tcpdchk.8 tcpdmatch.8 safe_finger.8 try-from.8 ${RPM_BUILD_ROOT}%{_mandir}/man8
ln -sf hosts_access.5 ${RPM_BUILD_ROOT}%{_mandir}/man5/hosts.allow.5
ln -sf hosts_access.5 ${RPM_BUILD_ROOT}%{_mandir}/man5/hosts.deny.5
#cp -a libwrap.a ${RPM_BUILD_ROOT}%{_libdir}
cp -a libwrap.so* ${RPM_BUILD_ROOT}%{_libdir}
#install -p -m644 libwrap.so.0.7.6 ${RPM_BUILD_ROOT}/%{_lib}
install -p -m644 tcpd.h ${RPM_BUILD_ROOT}%{_includedir}
install -m755 safe_finger ${RPM_BUILD_ROOT}%{_sbindir}
install -m755 tcpd ${RPM_BUILD_ROOT}%{_sbindir}
install -m755 try-from ${RPM_BUILD_ROOT}%{_sbindir}
install -m755 tcpdmatch ${RPM_BUILD_ROOT}%{_sbindir}

# XXX remove utilities that expect /etc/inetd.conf (#16059).
#install -m755 tcpdchk ${RPM_BUILD_ROOT}%{_sbindir}
rm -f ${RPM_BUILD_ROOT}%{_mandir}/man8/tcpdchk.*

magic_rpm_clean.sh

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root,-)
%doc BLURB README* DISCLAIMER Banners.Makefile
%{_sbindir}/*
%{_mandir}/man8/*

%files libs
%defattr(-,root,root,-)
%doc BLURB README* DISCLAIMER Banners.Makefile
%{_libdir}/*.so.*
%{_mandir}/man5/*

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
#%{_libdir}/*.a
%{_libdir}/*.so
%{_mandir}/man3/*

%changelog
* Wed Sep 30 2015 Liu Di <liudidi@gmail.com> - 7.6-63
- 为 Magic 3.0 重建

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 7.6-62
- 为 Magic 3.0 重建

* Sun Apr 22 2012 Liu Di <liudidi@gmail.com> - 7.6-61
- 为 Magic 3.0 重建

* Mon Feb 13 2012 Liu Di <liudidi@gmail.com> - 7.6-60
- 为 Magic 3.0 重建

* Wed Oct 11 2006 Liu Di <liudidi@gmail.com> - 7.6-40mgc
- rebuild for Magic
