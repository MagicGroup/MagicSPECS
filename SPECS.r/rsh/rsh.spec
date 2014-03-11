Summary: Clients for remote access commands (rsh, rlogin, rcp).
Summary(zh_CN.UTF-8): 远程访问 (rsh, rlogin, rcp) 的客户端
Name: rsh
Version: 0.17
Release: 54%{?dist}
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
Source4: http://www.tc.cornell.edu/~sadd/rexec-1.5.tar.gz
Source5: rsh-xinetd
Source6: rlogin-xinetd
Source7: rexec-xinetd

Patch1: netkit-rsh-0.17-sectty.patch
Patch2: netkit-rsh-0.17-rexec.patch
Patch3: netkit-rsh-0.10-stdarg.patch
Patch4: netkit-rsh-0.16-jbj.patch
Patch5: netkit-rsh-0.16-pamfix.patch
Patch6: netkit-rsh-0.16-jbj2.patch
Patch7: netkit-rsh-0.16-jbj3.patch
Patch8: netkit-rsh-0.16-jbj4.patch
Patch9: netkit-rsh-0.16-prompt.patch
Patch10: netkit-rsh-0.16-rlogin=rsh.patch
Patch11: netkit-rsh-0.16-nokrb.patch
Patch12: netkit-rsh-0.17-pre20000412-jbj5.patch
Patch13: netkit-rsh-0.17-userandhost.patch
Patch14: netkit-rsh-0.17-strip.patch
Patch15: netkit-rsh-0.17-lfs.patch
Patch16: netkit-rsh-0.17-chdir.patch
Patch17: netkit-rsh-0.17-pam-nologin.patch
Patch19: netkit-rsh-0.17-rexec-netrc.patch
Patch20: netkit-rsh-0.17-pam-sess.patch
Patch21: netkit-rsh-0.17-errno.patch
Patch22: netkit-rsh-0.17-rexec-sig.patch
Patch23: netkit-rsh-0.17-nohost.patch
Patch24: netkit-rsh-0.17-ignchld.patch
Patch25: netkit-rsh-0.17-checkdir.patch
Patch26: netkit-rsh-0.17-pam-conv.patch
Patch27: netkit-rsh-0.17-rcp-largefile.patch
Patch28: netkit-rsh-0.17-pam-rhost.patch
Patch29: netkit-rsh-0.17-rlogin-linefeed.patch
Patch30: netkit-rsh-0.17-ipv6.patch
Patch31: netkit-rsh-0.17-pam_env.patch
Patch33: netkit-rsh-0.17-dns.patch
Patch34: netkit-rsh-0.17-nohostcheck-compat.patch
Patch36: netkit-rsh-0.17-longname.patch
Patch37: netkit-rsh-0.17-arg_max.patch
Patch38: netkit-rsh-0.17-rh448904.patch

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
# XXX patches {6,7,8} not applied
#%patch5 -p1 -b .pamfix
#%patch6 -p1 -b .jbj2
#%patch7 -p1 -b .jbj3
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
%patch36 -p1 -b .longname
%patch37 -p1 -b .arg_max

# No, I don't know what this is doing in the tarball.
rm -f rexec/rexec

%build
sh configure --with-c-compiler=gcc
%ifarch s390 s390x
%{__perl} -pi -e '
    s,^CC=.*$,CC=cc,;
    s,-O2,\$(RPM_OPT_FLAGS) -fPIC -D_LARGEFILE_SOURCE -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64 -D_GNU_SOURCE,;
    s,^LDFLAGS=,LDFLAGS=-pie,;
    s,^BINDIR=.*$,BINDIR=%{_bindir},;
    s,^MANDIR=.*$,MANDIR=%{_mandir},;
    s,^SBINDIR=.*$,SBINDIR=%{_sbindir},;
    ' MCONFIG
%else
%{__perl} -pi -e '
    s,^CC=.*$,CC=cc,;
    s,-O2,\$(RPM_OPT_FLAGS) -fpic -D_LARGEFILE_SOURCE -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64 -D_GNU_SOURCE,;
    s,^LDFLAGS=,LDFLAGS=-pie,;
    s,^BINDIR=.*$,BINDIR=%{_bindir},;
    s,^MANDIR=.*$,MANDIR=%{_mandir},;
    s,^SBINDIR=.*$,SBINDIR=%{_sbindir},;
    ' MCONFIG
%endif
make %{?_smp_mflags}

%install
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
mkdir -p ${RPM_BUILD_ROOT}%{_sbindir}
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man{1,5,8}
mkdir -p ${RPM_BUILD_ROOT}/etc/pam.d

make INSTALLROOT=${RPM_BUILD_ROOT} BINDIR=%{_bindir} MANDIR=%{_mandir} install

install -m 644 $RPM_SOURCE_DIR/rexec.pam ${RPM_BUILD_ROOT}/etc/pam.d/rexec
install -m 644 $RPM_SOURCE_DIR/rlogin.pam ${RPM_BUILD_ROOT}/etc/pam.d/rlogin
install -m 644 $RPM_SOURCE_DIR/rsh.pam ${RPM_BUILD_ROOT}/etc/pam.d/rsh

mkdir -p ${RPM_BUILD_ROOT}/etc/xinetd.d/
install -m644 %SOURCE5 ${RPM_BUILD_ROOT}/etc/xinetd.d/rsh
install -m644 %SOURCE6 ${RPM_BUILD_ROOT}/etc/xinetd.d/rlogin
install -m644 %SOURCE7 ${RPM_BUILD_ROOT}/etc/xinetd.d/rexec

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root)
%attr(4755,root,root)	%{_bindir}/rcp
%{_bindir}/rexec
%attr(4755,root,root)	%{_bindir}/rlogin
%attr(4755,root,root)	%{_bindir}/rsh
%{_mandir}/man1/*.1*

%files server
%defattr(-,root,root)
%config	/etc/pam.d/rsh
%config	/etc/pam.d/rlogin
%config	/etc/pam.d/rexec
%{_sbindir}/in.rexecd
%{_sbindir}/in.rlogind
%{_sbindir}/in.rshd
%config(noreplace) /etc/xinetd.d/*
%{_mandir}/man8/*.8*

%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 0.17-54
- 为 Magic 3.0 重建

* Sat Feb 04 2012 Liu Di <liudidi@gmail.com> - 0.17-53
- 为 Magic 3.0 重建


