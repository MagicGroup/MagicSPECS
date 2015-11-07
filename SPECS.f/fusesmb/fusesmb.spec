Name:           fusesmb
Version:        0.8.7
Release:        7%{?dist}
Summary:        Mount "network neighbourhood"
Summary(zh_CN.UTF-8): 挂载“网上邻居”
Group:          Applications/Internet
Group(zh_CN.UTF-8):   应用程序/互联网
License:        GPL
URL:            http://hannibal.lr-s.tudelft.nl/fusesmb/
Source0:        http://hannibal.lr-s.tudelft.nl/fusesmb/download/%{name}-%{version}.tar.gz
Source1:        fusesmb.conf
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:  fuse-devel >= 2.3
BuildRequires:  samba-common >= 3.0
Packager:      kde <jack@linux.net.cn>

%description
With SMB for Fuse you can seamlessly browse your network neighbourhood
as were it on your own filesystem.
It's basically smbmount with a twist. Instead of mounting one Samba share at
a time, you mount all workgroups, hosts and shares at once. Only when you're
accessing a share a connection is made to the remote computer.

%description -l zh_CN.UTF-8
使用Fuse的SMB你可以无缝的浏览你的网上邻居，就像你自己的文件系统一样。
它基于smbmount的绑定。和挂载一个Samba不同，你可以一次挂载所有的工作组、主机和
共享。只有当你访问共享时才会建立到远程计算机的连接。

%prep
%setup -q


%build
CFLAGS="%{optflags} -I/usr/include/samba-4.0" %configure 
%{__make} %{?_smp_mflags} OPTIMIZE="%{optflags}" 


%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__make} install DESTDIR=$RPM_BUILD_ROOT
%{__strip} $RPM_BUILD_ROOT%{_bindir}/*

mkdir -p $RPM_BUILD_ROOT/etc/skel/.smb
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT/etc/skel/.smb/fusesmb.conf
magic_rpm_clean.sh
#mkdir -p $RPM_BUILD_ROOT/root/.smb
#install -m 600 %{SOURCE1} $RPM_BUILD_ROOT/root/.smb/fusesmb.conf

%post
for D in `cat /etc/passwd | grep ':/home/' | cut -f 6 -d:`; do
if [ -d $D ];then
cp -af /etc/skel/.smb $D/
USRHOME=`ls -la $D | grep "[^\.\.]\.$"`
OWNER=`echo $USRHOME | cut -f 3 -d\ `
GROUP=`echo $USRHOME | cut -f 4 -d\ `
chown -hR ${OWNER}:${GROUP} $D/.smb/
chmod 600 $D/.smb/fusesmb.conf
fi
done

%clean
%{__rm} -rf $RPM_BUILD_ROOT
%{__rm} -rf $RPM_BUILD_DIR/%{name}-%{version}

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README
%{_bindir}/*
%{_mandir}/man*/*
%{_sysconfdir}/*

%changelog
* Thu Oct 29 2015 Liu Di <liudidi@gmail.com> - 0.8.7-7
- 为 Magic 3.0 重建

