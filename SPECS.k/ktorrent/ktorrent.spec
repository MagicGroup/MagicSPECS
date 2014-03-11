%define name		ktorrent
%define version		2.2.8
%define release		1%{?dist}
%define testver		%{nil}
%define isrel		1
%define needpo		0

Summary:	A Bittorent program for KDE.
Summary(zh_CN.UTF-8):	KDE 下的 BT 下载程序。
Name:		%{name}
Version:		%{version}
%if %isrel
Release:	%{release}
%else
Release:	0.%{testver}.%{release}
%endif
License:		GPL
Group:		Applications/Internet
Group(zh_CN.UTF-8):	应用程序/互联网
Url:		http://ktorrent.org/index.php?page=downloads
%if %isrel
Source0:	%{name}-%{version}.tar.bz2
%else
Source0:	%{name}-%{version}%{testver}.tar.gz
%endif
%if %needpo
Source1:	%{name}-%{version}.po
%endif
#修正中文 torrents 显示问题
Patch1:		%{name}-2.2.7-cjk.patch
#将标识改为Xunlei的:D，不知道有没有用
Patch2:		%{name}-2.2.7-agent.patch
#TDE的补丁
Patch3:		ktorrent-2.2.8-admin.patch
Packager:	Liu Di <sejishikong{at}263{dot}net>
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)
Prefix:		%{_prefix}

%description
KTorrent is a BitTorrent program for KDE. It's main features are : 

Downloads torrent files 
Upload speed capping, seeing that most people can't upload infinite amounts of data. 
Internet searching using The Bittorrent website's search engine 
UDP Trackers more info 

%description -l zh_CN.UTF-8
KTorrent 是一个 KDE 下的 BT 下载程序。它的主要特性有：
下载 torrent 文件；
上传速度控制；
使用 BT 网页搜索引擎进行互联网搜索；
支持 UDP Tracker 等。

%prep
%if %isrel
%setup -q
%else
%setup -q -n %{name}-%{version}%{testver}
%endif
%patch1 -p1
%patch3 -p1
chmod 777 admin/*

%build
make -f admin/Makefile.common
%configure
#临时措施
sed -i 's/\/include\/tqt/\/include\/tqt \-lqt\-mt \-ltdecore \-ltdeui \-lDCOP \-lkio/g' plugins/*/Makefile
sed -i 's/\/include\/tqt/\/include\/tqt \-lqt\-mt \-ltdecore \-ltdeui \-lDCOP \-lkio/g' apps/*/Makefile
make #%{?_smp_mflags}

%install
rm -rf %{buildroot}
%makeinstall
/usr/bin/magic_rpm_clean.sh
%if %needpo
mkdir -p %{buildroot}%{_datadir}/locale/zh_CN/LC_MESSAGES/
msgfmt %{SOURCE1} -o %{buildroot}%{_datadir}/locale/zh_CN/LC_MESSAGES/%{name}.mo
%endif
%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*
%{_datadir}/*
%exclude %{_libdir}/debug

%changelog
* Fri Jul 25 2008 Liu Di <liudidi@gmail.com> - 2.2.7-4mgc
- 添加一个修改标识的补丁，也许对加速有用

* Thu Jul 24 2008 Liu Di <liudidi@gmail.com> - 2.2.7-2mgc
- 添加中文编码修正补丁

* Fri Jun 13 2008 Liu Di <Liudidi@gmail.com> - 2.2.7-1mgc
- 更新到 2.2.7

* Sun Feb 03 2008 Liu Di <liudidi@gmail.com> - 2.2.5-1mgc
- update to 2.2.5

* Fri Nov 16 2007 Liu Di <liudidi@gmail.coM> - 2.2.3-1mgc
- update to 2.2.3

* Fri Nov 09 2007 Liu Di <liudidi@gmail.com> - 2.2.2-1mgc
- updaet to 2.2.2

* Sat Jun 23 2007 kde <athena_star {at} 163 {dot} com>  - 2.2-0.rc1.1mgc
- update to 2.2rc1

* Fri Jun 08 2007 Liu Di <liudidi@gmail.com> - 2.2-0.beta1.1mgc
- update to 2.2beta1

* Tue May 08 2007 kde <athena_star {at} 163 {dot} com> - 2.1.4-1mgc
- update to 2.1.4

* Sat Jul 16 2005 - 1.0
- Fix a bug about Chinese lang file

* Thu Jul 14 2005 - 1.0
- First Build ML 1.2 final
