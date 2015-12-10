Name:           fuse-sshfs
Version:	2.5
Release:        3%{?dist}
Summary:        FUSE-Filesystem to access remote filesystems via SSH
Summary(zh_CN.UTF-8): 通过 SSH 访问远程文件系统的 FUSE 文件系统

Group:          System Environment/Base
Group(zh_CN.UTF-8):	系统环境/基本
License:        GPLv2
URL:            http://fuse.sourceforge.net/sshfs.html
Source0:        http://downloads.sourceforge.net/fuse/sshfs-fuse-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Provides:       sshfs = %{version}
Requires:       fuse >= 2.2
Requires:	openssh-clients >= 4.4
BuildRequires:  fuse-devel >= 2.2
BuildRequires:  glib2-devel >= 2.0
BuildRequires:	openssh-clients >= 4.4

%description
This is a FUSE-filesystem client based on the SSH File Transfer Protocol.
Since most SSH servers already support this protocol it is very easy to set
up: i.e. on the server side there's nothing to do.  On the client side
mounting the filesystem is as easy as logging into the server with ssh.

%description -l zh_CN.UTF-8
这是一个基于 SSH 文件传输协议的 FUSE 文件系统客户端。因为大多数 SSH 服务器
已经支持这个协议，所以可以非常简单的设置，也就是说服务器那边不用做任何事情。
在客户端这边挂载文件系统就像使用 ssh 登录服务器一样简单。

%prep
%setup -q -n sshfs-fuse-%{version}

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING FAQ.txt NEWS README
%{_bindir}/sshfs
%{_mandir}/man1/sshfs.1.gz

%changelog
* Sun Nov 08 2015 Liu Di <liudidi@gmail.com> - 2.5-3
- 为 Magic 3.0 重建

* Thu Oct 29 2015 Liu Di <liudidi@gmail.com> - 2.5-2
- 为 Magic 3.0 重建

* Fri Apr 04 2014 Liu Di <liudidi@gmail.com> - 2.5-1
- 更新到 2.5

* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 2.3-2
- 为 Magic 3.0 重建


