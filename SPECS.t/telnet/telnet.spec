Summary: The client program for the telnet remote login protocol.
Summary(zh_CN.UTF-8): 远程登录协议 - telnet - 的客户端
Name: telnet
Version: 0.17
Release: 47%{?dist}
Epoch: 1
License: BSD
Group: Applications/Internet
Group(zh_CN.UTF-8): 应用程序/互联网
Source0: ftp://ftp.uk.linux.org/pub/linux/Networking/netkit/netkit-telnet-%{version}.tar.gz
Source2: telnet-client.tar.gz
Source4: telnet.wmconfig
Source5: telnet@.service
Source6: telnet.socket
Patch1: telnet-client-cvs.patch
Patch5: telnetd-0.17.diff
Patch6: telnet-0.17-env.patch
Patch7: telnet-0.17-issue.patch
Patch8: telnet-0.17-sa-01-49.patch
Patch10: telnet-0.17-pek.patch
Patch11: telnet-0.17-8bit.patch
Patch12: telnet-0.17-argv.patch
Patch13: telnet-0.17-conf.patch
Patch14: telnet-0.17-cleanup_race.patch
Patch15: telnetd-0.17-pty_read.patch
Patch16: telnet-0.17-CAN-2005-468_469.patch
Patch18: telnet-gethostbyname.patch
Patch19: netkit-telnet-0.17-ipv6.diff
Patch20: netkit-telnet-0.17-nodns.patch
Patch21: telnet-0.17-errno_test_sys_bsd.patch
Patch22: netkit-telnet-0.17-reallynodns.patch
Patch23: telnet-rh678324.patch
Patch24: telnet-rh674942.patch
Patch25: telnet-rh704604.patch
Patch26: telnet-rh825946.patch
Patch27: telnet-0.17-ipv6-support.patch

BuildPreReq: ncurses-devel
Buildroot: %{_tmppath}/%{name}-root

%description
Telnet is a popular protocol for logging into remote systems over the
Internet. The telnet package provides a command line telnet client.

%description -l zh_CN.UTF-8
Telnet 是一个通过互联网登录远程系统的流行协议。
这个包提供了一个命令行工具 telnet。

%package server
Requires: xinetd
Group: System Environment/Daemons
Group(zh_CN.UTF-8): 系统环境/服务
Summary: The server program for the telnet remote login protocol.
Summary(zh_CN.UTF-8): telnet 的服务器端


%description server
Telnet is a popular protocol for logging into remote systems over the
Internet. The telnet-server package includes a telnet daemon that
supports remote logins into the host machine. The telnet daemon is
disabled by default. You may enable the telnet daemon by editing
/etc/xinetd.d/telnet.

%description server -l zh_CN.UTF-8
Telnet 是一个通过互联网登录远程系统的流行协议。这个包提供了一个 telnet 
的服务器端。它默认没有开启，编辑 /etc/xinet.d/telnet 可以开启它。

%prep
%setup -q -n netkit-telnet-%{version}

mv telnet telnet-NETKIT
%setup -T -D -q -a 2 -n netkit-telnet-%{version}

%patch1 -p0 -b .cvs
%patch5 -p0 -b .fix
%patch6 -p1 -b .env
%patch10 -p0 -b .pek
%patch7 -p1 -b .issue
%patch8 -p1 -b .sa-01-49
%patch11 -p1 -b .8bit
%patch12 -p1 -b .argv
%patch13 -p1 -b .confverb
%patch14 -p1 -b .cleanup_race 
%patch15 -p0 -b .pty_read
%patch16 -p1 -b .CAN-2005-468_469
#%patch17 -p1 -b .linemode
%patch18 -p1 -b .gethost
%patch19 -p1 -b .gethost2
%patch20 -p1 -b .nodns
%patch21 -p1 -b .errnosysbsd
%patch22 -p1 -b .reallynodns
%patch23 -p1 -b .rh678324
%patch24 -p1 -b .rh674942
%patch25 -p1 -b .rh704604
%patch26 -p1 -b .rh825946
%patch27 -p1 -b .ipv6-support

%build
%ifarch s390 s390x
    export CC_FLAGS="$RPM_OPT_FLAGS -fPIE"
%else
    export CC_FLAGS="$RPM_OPT_FLAGS -fpie"
%endif

export LD_FLAGS="$LD_FLAGS -z now -pie"

sh configure --with-c-compiler=gcc 
perl -pi -e '
    s,-O2,\$(CC_FLAGS),;
    s,LDFLAGS=.*,LDFLAGS=\$(LD_FLAGS),;
    s,^BINDIR=.*$,BINDIR=%{_bindir},;
    s,^MANDIR=.*$,MANDIR=%{_mandir},;
    s,^SBINDIR=.*$,SBINDIR=%{_sbindir},;
    ' MCONFIG

# remove stripping
perl -pi -e 's|install[ ]+-s|install|g' \
    ./telnet/GNUmakefile \
    ./telnetd/Makefile \
    ./telnetlogin/Makefile \
    ./telnet-NETKIT/Makefile

make %{?_smp_mflags}

%install
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
mkdir -p ${RPM_BUILD_ROOT}%{_sbindir}
mkdir -p ${RPM_BUILD_ROOT}%{_unitdir}
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man1
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man5
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man8

make INSTALLROOT=${RPM_BUILD_ROOT} install

install -p -m644 %SOURCE5 ${RPM_BUILD_ROOT}%{_unitdir}/telnet@.service
install -p -m644 %SOURCE6 ${RPM_BUILD_ROOT}%{_unitdir}/telnet.socket

%post server
%systemd_post telnet.socket

%preun server
%systemd_preun telnet.socket

%postun server
%systemd_postun_with_restart telnet.socket

%files
%doc README
%defattr(-,root,root,-)
%{_bindir}/telnet
%{_mandir}/man1/telnet.1*

%files server
%defattr(-,root,root,-)
%{_unitdir}/*
%{_sbindir}/in.telnetd
%{_mandir}/man5/issue.net.5*
%{_mandir}/man8/in.telnetd.8*
%{_mandir}/man8/telnetd.8*


%changelog
* Wed Sep 30 2015 Liu Di <liudidi@gmail.com> - 1:0.17-47
- 为 Magic 3.0 重建

* Sat Sep 19 2015 Liu Di <liudidi@gmail.com> - 1:0.17-46
- 为 Magic 3.0 重建

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 1:0.17-45
- 为 Magic 3.0 重建

* Tue Feb 14 2012 Liu Di <liudidi@gmail.com> - 1:0.17-44
- 为 Magic 3.0 重建


