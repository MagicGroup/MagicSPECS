%global _hardened_build 1

Summary: Clients for remote access commands (rsh, rlogin, rcp).
Summary(zh_CN.UTF-8): 远程访问 (rsh, rlogin, rcp) 的客户端
Name: rsh
Version: 0.17
Release: 56%{?dist}
License: BSD
Group: Applications/Internet
Group(zh_CN.UTF-8): 应用程序/互联网

BuildRoot: %{_tmppath}/%{name}-root
BuildPrereq: perl
BuildPrereq: ncurses-devel

BuildRequires: pam-devel

Source: ftp://ftp.uk.linux.org/pub/linux/Networking/netkit/netkit-rsh-%{version}.tar.gz
Source1: rexec.pam
Source2: rlogin.pam
Source3: rsh.pam
# Source is no longer publicly available.
Source4: rexec-1.5.tar.gz
Source5: rsh@.service
Source6: rsh.socket
Source7: rlogin@.service
Source8: rlogin.socket
Source9: rexec@.service
Source10: rexec.socket
Patch1: netkit-rsh-0.17-sectty.patch
# Make rexec installation process working
Patch2: netkit-rsh-0.17-rexec.patch
Patch3: netkit-rsh-0.10-stdarg.patch
# Improve installation process
Patch4: netkit-rsh-0.16-jbj.patch
# Link rshd against libpam
Patch8: netkit-rsh-0.16-jbj4.patch
Patch9: netkit-rsh-0.16-prompt.patch
Patch10: netkit-rsh-0.16-rlogin=rsh.patch
# Improve documentation
Patch11: netkit-rsh-0.16-nokrb.patch
# Remove spurious double-reporting of errors
Patch12: netkit-rsh-0.17-pre20000412-jbj5.patch
# RH #42880
Patch13: netkit-rsh-0.17-userandhost.patch
# Don't strip binaries during installation
Patch14: netkit-rsh-0.17-strip.patch
# RH #67362
Patch15: netkit-rsh-0.17-lfs.patch
# RH #57392
Patch16: netkit-rsh-0.17-chdir.patch
# RH #63806
Patch17: netkit-rsh-0.17-pam-nologin.patch
# RH #135643
Patch19: netkit-rsh-0.17-rexec-netrc.patch
# RH #68590
Patch20: netkit-rsh-0.17-pam-sess.patch
# RH #67361
Patch21: netkit-rsh-0.17-errno.patch
# RH #118630
Patch22: netkit-rsh-0.17-rexec-sig.patch
# RH #135827
Patch23: netkit-rsh-0.17-nohost.patch
# RH #122315
Patch24: netkit-rsh-0.17-ignchld.patch
# RH #146464
Patch25: netkit-rsh-0.17-checkdir.patch
Patch26: netkit-rsh-0.17-pam-conv.patch
# RH #174045
Patch27: netkit-rsh-0.17-rcp-largefile.patch
# RH #174146
Patch28: netkit-rsh-0.17-pam-rhost.patch
# RH #178916
Patch29: netkit-rsh-0.17-rlogin-linefeed.patch
Patch30: netkit-rsh-0.17-ipv6.patch
Patch31: netkit-rsh-0.17-pam_env.patch
Patch33: netkit-rsh-0.17-dns.patch
Patch34: netkit-rsh-0.17-nohostcheck-compat.patch
# RH #448904
Patch35: netkit-rsh-0.17-audit.patch
Patch36: netkit-rsh-0.17-longname.patch
# RH #440867
Patch37: netkit-rsh-0.17-arg_max.patch
Patch38: netkit-rsh-0.17-rh448904.patch
Patch39: netkit-rsh-0.17-rh461903.patch
Patch40: netkit-rsh-0.17-rh473492.patch
Patch41: netkit-rsh-0.17-rh650119.patch
Patch42: netkit-rsh-0.17-rh710987.patch
Patch43: netkit-rsh-0.17-rh784467.patch
Patch44: netkit-rsh-0.17-rh896583.patch
Patch45: netkit-rsh-0.17-rh947213.patch
Patch46: 0001-rshd-use-sockaddr_in-for-non-native-IPv6-clients.patch
Patch47: 0002-rlogind-use-sockaddr_in-for-non-native-IPv6-client.patch
Patch48: netkit-rsh-0.17-ipv6-rexec.patch
Patch49: 0001-rshd-include-missing-header-file.patch
Patch50: 0001-rshd-use-upper-bound-for-cmdbuflen.patch   
Patch51: 0001-rcp-don-t-advance-pointer-returned-from-rcp_basename.patch

%description
The rsh package contains a set of programs which allow users to run
commands on remote machines, login to other machines and copy files
between machines (rsh, rlogin and rcp).  All three of these commands
use rhosts style authentication.  This package contains the clients
needed for all of these services.
The rsh package should be installed to enable remote access to other
machines.

%description -l zh_CN.UTF-8
rsh 软件包包括一组允许用户在远程机器上运行命令(rsh)，登录到其它机器
(rlogin)，以及在机器间复制文件(rcp)的程序。这三个程序都使用 rhosts
样式的验证。

%package server
Summary: Servers for remote access commands (rsh, rlogin, rcp).
Summary(zh_CN.UTF-8): 远程访问 (rsh, rlogin, rcp) 的服务端
Group: System Environment/Daemons
Group(zh_CN.UTF-8): 系统环境/服务
Requires: pam >= 0.59, /etc/pam.d/system-auth, xinetd

%description server
The rsh-server package contains a set of programs which allow users
to run commands on remote machines, login to other machines and copy
files between machines (rsh, rlogin and rcp).  All three of these
commands use rhosts style authentication.  This package contains the
servers needed for all of these services.  It also contains a server
for rexec, an alternate method of executing remote commands.
All of these servers are run by inetd and configured using
/etc/xinet.d/ and PAM.

The rsh-server package should be installed to enable remote access
from other machines.

%description server -l zh_CN.UTF-8
rsh 软件包包括一组允许用户在远程机器上运行命令(rsh)，登录到其它机器
(rlogin)，以及在机器间复制文件(rcp)的程序。这三个程序都使用 rhosts
样式的验证。

这个包是 rsh 的服务器端。

%prep
%setup -q -n netkit-rsh-%{version} -a 4
%patch1 -p1 -b .sectty
%patch2 -p1 -b .rexec
%patch3 -p1 -b .stdarg
%patch4 -p1 -b .jbj
%patch8 -p1 -b .jbj4
%patch9 -p1 -b .prompt
%patch10 -p1 -b .rsh
%patch11 -p1 -b .rsh.nokrb
%patch12 -p1 -b .jbj5
%patch13 -p1 -b .userandhost
%patch14 -p1 -b .strip
%patch15 -p1 -b .lfs
%patch16 -p1 -b .chdir
%patch17 -p1 -b .pam-nologin
%patch19 -p1 -b .rexec-netrc
%patch20 -p1 -b .pam-sess
%patch21 -p1 -b .errno
%patch22 -p1 -b .rexec-sig
%patch23 -p1 -b .nohost
%patch24 -p1 -b .ignchld
%patch25 -p1 -b .checkdir
%patch26 -p1 -b .pam-conv
%patch27 -p1 -b .largefile
%patch28 -p1 -b .pam-rhost
%patch29 -p1 -b .linefeed
%patch30 -p1 -b .ipv6
%patch31 -p1 -b .pam_env
%patch33 -p1 -b .dns
%patch34 -p1 -b .compat
%patch35 -p1 -b .audit
%patch36 -p1 -b .longname
%patch37 -p1 -b .arg_max
%patch38 -p1 -b .rh448904
%patch39 -p1 -b .rh461903
%patch40 -p1 -b .rh473492
%patch41 -p1 -b .rh650119
%patch42 -p1 -b .rh710987
%patch43 -p1 -b .rh784467
%patch44 -b .rh896583
%patch45 -p1 -b .rh947213
%patch46 -p1
%patch47 -p1
%patch48 -p1 -b .ipv6-rexec
%patch49 -p1 -b .waitpid
%patch50 -p1
%patch51 -p1

# No, I don't know what this is doing in the tarball.
rm -f rexec/rexec

%build
sh configure --with-c-compiler=gcc
export RPM_OPT_FLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
%ifarch s390 s390x
%{__perl} -pi -e '
    s,^CC=.*$,CC=cc,;
    s,-O2,\$(RPM_OPT_FLAGS) -fPIC -D_LARGEFILE_SOURCE -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64 -D_GNU_SOURCE,;
    s,^LDFLAGS=,LDFLAGS=-z now -pie,;
    s,^BINDIR=.*$,BINDIR=%{_bindir},;
    s,^MANDIR=.*$,MANDIR=%{_mandir},;
    s,^SBINDIR=.*$,SBINDIR=%{_sbindir},;
    ' MCONFIG
%else
%{__perl} -pi -e '
    s,^CC=.*$,CC=cc,;
    s,-O2,\$(RPM_OPT_FLAGS) -fpic -D_LARGEFILE_SOURCE -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64 -D_GNU_SOURCE,;
    s,^LDFLAGS=,LDFLAGS=-z now -pie,;
    s,^BINDIR=.*$,BINDIR=%{_bindir},;
    s,^MANDIR=.*$,MANDIR=%{_mandir},;
    s,^SBINDIR=.*$,SBINDIR=%{_sbindir},;
    ' MCONFIG
%endif
make %{?_smp_mflags}

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_mandir}/man{1,5,8}
mkdir -p %{buildroot}%{_sysconfdir}/pam.d

make INSTALLROOT=%{buildroot} BINDIR=%{_bindir} MANDIR=%{_mandir} install

install -m 644 %SOURCE1 %{buildroot}%{_sysconfdir}/pam.d/rexec
install -m 644 %SOURCE2 %{buildroot}%{_sysconfdir}/pam.d/rlogin
install -m 644 %SOURCE3 %{buildroot}%{_sysconfdir}/pam.d/rsh

mkdir -p %{buildroot}%{_unitdir}
install -m644 %SOURCE5 %{buildroot}%{_unitdir}/rsh@.service
install -m644 %SOURCE6 %{buildroot}%{_unitdir}/rsh.socket
install -m644 %SOURCE7 %{buildroot}%{_unitdir}/rlogin@.service
install -m644 %SOURCE8 %{buildroot}%{_unitdir}/rlogin.socket
install -m644 %SOURCE9 %{buildroot}%{_unitdir}/rexec@.service
install -m644 %SOURCE10 %{buildroot}%{_unitdir}/rexec.socket

%post server
%systemd_post rsh.socket
%systemd_post rlogin.socket
%systemd_post rexec.socket

%preun server
%systemd_preun rsh.socket
%systemd_preun rlogin.socket
%systemd_preun rexec.socket

%postun server
%systemd_postun_with_restart rsh.socket
%systemd_postun_with_restart rlogin.socket
%systemd_postun_with_restart rexec.socket

%files
%defattr(-,root,root,-)
%doc README BUGS
%attr(0755,root,root) %caps(cap_net_bind_service=pe) %{_bindir}/rcp
%{_bindir}/rexec
%attr(0755,root,root) %caps(cap_net_bind_service=pe) %{_bindir}/rlogin
%attr(0755,root,root) %caps(cap_net_bind_service=pe) %{_bindir}/rsh
%{_mandir}/man1/*.1*

%files server
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/pam.d/rsh
%config(noreplace) %{_sysconfdir}/pam.d/rlogin
%config(noreplace) %{_sysconfdir}/pam.d/rexec
%{_sbindir}/in.rexecd
%{_sbindir}/in.rlogind
%{_sbindir}/in.rshd
%{_unitdir}/*
%{_mandir}/man8/*.8*

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.17-56
- 为 Magic 3.0 重建

* Fri Sep 18 2015 Liu Di <liudidi@gmail.com> - 0.17-55
- 为 Magic 3.0 重建

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 0.17-54
- 为 Magic 3.0 重建

* Sat Feb 04 2012 Liu Di <liudidi@gmail.com> - 0.17-53
- 为 Magic 3.0 重建


