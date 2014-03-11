%define _name       BitStormLite
%define version      0.2q
%define release      2%{?dist}
%define testver     %{nil}

%define prefix     /usr
%define sysconfdir /etc

%define real_name BitStormLite

Summary:	A Bittorent program
Summary(zh_CN.UTF-8): 一个 Bittroent 程序
Name:		bitstormlite
Version:		%{version}
Release:	%{release}
License:		GPL
Group:		Applications/Internet
Group(zh_CN.UTF-8):   应用程序/互联网
Url:		http://www.linuxfans.org/nuke/modules.php?name=Forums&file=viewforum&f=68
Source0:	http://downloads.sourceforge.net/project/bbom/BitStormLite/%{real_name}-%{version}.tar.gz
Source1:	bitstormlite.desktop
Patch0:		BitStormLite-0.2a-autoencoding.patch
Patch1: 	BitStormLite-util.h.patch
Patch2: 	BitStormLite-Storage.patch
Patch3:		BitStormLite-gcc44.patch

#for 5qzone patch
#Patch:		%{name}-5q.patch
Packager:	sejishikong <sejishikong@263.net>
BuildRoot: %{_tmppath}/%{name}-%{version}%{testver}-%{release}-buildroot-%(%{__id_u} -n)
BuildRequires: boost-devel, curl-devel, gtk2-devel
Obsoletes: BitStormLite

%description
BitStormLite is a BitTorrent program use GTK2. 

%description -l zh_CN.UTF-8
BitStorm 0.2 Lite 主要特性如下：
1)基于 C++ 和 GTK2，占用系统资源少
2)可调整大小的磁盘缓存，极大地减轻磁盘负担
3)支持多个示踪服务器(Tracker)，支持 UDP Tracker，支持 compact 模式 HTTP Tracker
4)UPnP NAT 功能，自动进行端口映射(默认监听端口为 7681~7689)
5)支持多文件选择性下载，可单独下载某些文件
6)支持 UTF-8 编码的 Torrent 文件，文件名不会出现乱码
7)可设置上传/下载速度

%prep
%setup -q -n %{real_name}-%{version}
%patch0 -p1 -b .autoencoding
%patch1 -p1 -b .fix
#%patch2 -p1 -b .cjk
#%patch3 -p1 -b .gcc44

%build
%configure
%{__make} %{?_smp_mflags} 


%install
rm -rf %{buildroot}
%makeinstall

#Install application link for X-Windows
mkdir -p %{buildroot}%{_datadir}/applications
install -D -m 644 %{SOURCE1} %{buildroot}%{_datadir}/applications/bitstormlite.desktop

%clean
%{__rm} -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files
%defattr(-,root,root)
%{_bindir}/*
%{_datadir}/*
%exclude /usr/*/debug*

%changelog
* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 0.2q-2
- 为 Magic 3.0 重建

* Wed Nov 02 2011 Liu Di <Liudidi@gmail.com> - 0.2q-1
- 升级到 0.2q　

* Sun May 6 2007 kde <athena_star {at} 163 {dot} com> - 0.2i-1mgc
- update to 0.2i
- modify the spec file

* Tue Feb 13 2007 Liu Di <liudidi@gmail.com> - 0.2g-1mgc
- update to 0.2g

* Tue Oct 12 2006 KanKer <kanker@163.com> -0.2c-1mgc
- update 0.2c
* Sun Mar 19 2006 KanKer <kanker@163.com>
- update 20060319cvs
* Mon Jan 16 2006 KanKer <kanker@163.com>
- update 0.2b
- remove patch
* Fri Dec 9 2005 KanKer <kanker@163.com>
- update 0.2a
* Tue Dec 8 2005 KanKer <kanker@163.com>
- update 0.2
* Fri Oct 28 2005 KanKer <kanker@163.com>
- update 0.1b
* Tue Oct 25 2005 sejishikong <sejishikong@263.net>
- First Build ML 2.0b3 
