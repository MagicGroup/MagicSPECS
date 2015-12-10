%define realname	partitionmanager

%define jobs		$((`/usr/bin/getconf _NPROCESSORS_ONLN` + 1))

%define git 1
%define vcsdate 20151030
%define kde4_enable_final_bool OFF

Name: 			kde4-%{realname}
Version:		1.0.60
%if 0%{?git}
Release:		0.git%{vcsdate}%{dist}.6
%else
Release:		13%{?dist}
%endif
License:		GPL
Summary:		Easily manage disks, partitions and file systems on your KDE Desktop
Summary(zh_CN.UTF-8):		在 KDE 桌面上易用的管理磁盘、分区和文件系统的程序
Group:			User Interface/Desktops
Group(zh_CN.UTF-8):		用户界面/桌面
URL:			http://www.partitionmanager.org
BuildRoot:	 	%{_tmppath}/%{name}-%{release}-buildroot
%if 0%{?git}
Source0:		%{name}-git%{vcsdate}.tar.xz
%else
Source0:			http://downloads.sourceforge.net/project/partitionman/partitionmanager/%{version}/%{realname}-%{el_maj}.tar.bz2
%endif
Source1:	make_kde4-partitionmanager_git_package.sh
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
%if 0%{?git}
%setup -q -n %{name}-git%{vcsdate}
%else
%setup -q -n %{realname}-%{version}
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
* Mon Nov 09 2015 Liu Di <liudidi@gmail.com> - 1.0.60-0.git20151030.6
- 为 Magic 3.0 重建

* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 1.0.60-0.git20151030.5
- 更新到 20151030 日期的仓库源码

* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 1.0.60-0.git20140604.4
- 为 Magic 3.0 重建

* Wed Jun 04 2014 Liu Di <liudidi@gmail.com> - 1.0.60-0.git20140604.3
- 为 Magic 3.0 重建

* Wed Jun 04 2014 Liu Di <liudidi@gmail.com> - 1.0.60-0.git20140604.2
- 更新到 20140604 日期的仓库源码

* Wed Jun 04 2014 Liu Di <liudidi@gmail.com> - 1.0.60-0.git20140603.2
- 为 Magic 3.0 重建

* Wed Jun 04 2014 Liu Di <liudidi@gmail.com> - 1.0.4-0.git20121228.2
- 为 Magic 3.0 重建

* Wed Jun 04 2014 Liu Di <liudidi@gmail.com> - 1.0.4-0.git20121228.1
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.0.3-2
- 为 Magic 3.0 重建


