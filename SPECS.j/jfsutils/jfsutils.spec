Summary: Utilities for managing the JFS filesystem.
Summary(zh_CN.UTF-8): 管理 JFS 文件系统的工具
Name: jfsutils
Version: 1.1.13
Release: 3%{?dist}
Source0: jfsutils-%{version}.tar.gz
URL: http://jfs.sourceforge.net/
Group: System Environment/Base
Group(zh_CN.UTF-8): 系统环境/基本
License: GPLv2+
Buildroot: %{_tmppath}/%{name}-root
Buildrequires: e2fsprogs-devel

%description
The jfsutils package contains a number of utilities for creating,
checking, modifying, and correcting any inconsistencies in JFS
filesystems.  The following utilities are available: fsck.jfs - initiate
replay of the JFS transaction log, and check and repair a JFS formatted
device; logdump - dump a JFS formatted device's journal log; logredo -
"replay" a JFS formatted device's journal log;  mkfs.jfs - create a JFS
formatted partition; xchkdmp - dump the contents of a JFS fsck log file
created with xchklog; xchklog - extract a log from the JFS fsck workspace
into a file;  xpeek - shell-type JFS file system editor.

%description -l zh_CN.UTF-8
jfsutils 软件包包括许多用来创建、检查、修改、和改正任何 JFS 文件系统中不
一致的地方的工具。其中包括下列工具： fsck.jfs―发动 JFS 事务日志的重播，
并检查及修理 JFS 格式化的设备；logdump―转储一个 JFS 格式化的设备的日志文
件； logredo－重播一个 JFS 格式化的设备的日志文件； mkfs.jfs―创建一个 JFS
格式化的分区； xchkdmp―转储用 xchklog 创建的 JFS fsck 日志文件的内容；
xchklog―从 JFS fsck 工作区中把日志抽取到一个文件中； xpeek―shell 类型的
JFS 文件系统编辑器。

%prep
%setup -q

%build
CFLAGS="${RPM_OPT_FLAGS}" ./configure --mandir=%{_mandir}
make

%install
[ "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
# let brp-compress handle this policy
rm -f $RPM_BUILD_ROOT/%{_mandir}/*/*.gz

%clean
[ "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/sbin/*
%{_mandir}/*/*
%doc AUTHORS COPYING INSTALL NEWS README ChangeLog

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.1.13-3
- 为 Magic 3.0 重建

* Tue Dec 13 2011 Liu Di <liudidi@gmail.com> - 1.1.13-2
- 为 Magic 3.0 重建


