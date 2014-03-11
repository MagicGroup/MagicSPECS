%define realname	partitionmanager
%define _rel_maj	1.0.4

%define jobs		$((`/usr/bin/getconf _NPROCESSORS_ONLN` + 1))

%define svn 		1
%define svndate		20121228
%define kde4_enable_final_bool OFF

Name: 			kde4-%{realname}
Version:		%{_rel_maj}
%if 0%{?svn}
Release:		0.svn%{svndate}%{dist}
%else
Release:		1%{?dist}
%endif
License:		GPL
Summary:		Easily manage disks, partitions and file systems on your KDE Desktop
Summary(zh_CN.UTF-8):		在 KDE 桌面上易用的管理磁盘、分区和文件系统的程序
Group:			Productivity/File utilities
Group(zh_CN.UTF-8):		用户界面/桌面
URL:			http://www.partitionmanager.org
BuildRoot:	 	%{_tmppath}/%{name}-%{release}-buildroot
%if 0%{?svn}
Source0:		%{realname}-svn%{svndate}.tar.xz
%else
Source0:			http://downloads.sourceforge.net/project/partitionman/partitionmanager/%{version}/%{realname}-%{_rel_maj}.tar.bz2
%endif
Source1:	make_partitionmanager_svn_package.sh
BuildRequires:	gcc-c++
BuildRequires:	cmake
BuildRequires:	parted-devel
BuildRequires:  desktop-file-utils
BuildRequires:  kdelibs4-devel
BuildRequires:  e2fsprogs-devel
BuildRequires:	qt4-devel

%description
Partition Manager is a utility program to help you manage the disk devices,
partitions and file systems on your computer. It allows you to easily create,
copy, move, delete, resize without losing data, backup and restore partitions.

%description -l zh_CN.UTF-8
在 KDE 桌面上易用的管理磁盘、分区和文件系统的程序。

%prep
%if 0%{?svn}
%setup -q -n %{realname}-svn%{svndate}
%else
%setup -q -n %{realname}-%{_rel_maj}
%endif

%build
mkdir build
cd build
%cmake_kde4 ..

%__make %{?jobs:-j%{jobs}}

%install
cd build
%__make install DESTDIR=%{buildroot} 

#desktop-file-validate %{buildroot}/%{kde4_xdgappsdir}/{realname}.desktop
magic_rpm_clean.sh

%clean_kde4_desktop_files

%clean
[ -d "%{buildroot}" -a "%{buildroot}" != "" ] && %__rm -rf "%{buildroot}"

%files
%defattr(-, root, root)
%doc COPYING README
%{kde4_bindir}/%{realname}
#%{kde4_bindir}/%{realname}-bin
%{kde4_libdir}/lib*.so
%{kde4_plugindir}/*.so
%dir %{kde4_appsdir}/%{realname}
%{kde4_appsdir}/%{realname}/%{realname}ui.rc
%{kde4_xdgappsdir}/%{realname}.desktop
%{kde4_servicesdir}/*.desktop
%{kde4_servicetypesdir}/*
%{kde4_iconsdir}/hicolor/*/apps/%{realname}.*
#%{kde4_localedir}/*


%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.0.3-2
- 为 Magic 3.0 重建


