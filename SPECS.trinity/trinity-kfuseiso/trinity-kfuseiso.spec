Name:           kfuseiso
BuildRequires:  fuseiso
Requires:	fuseiso
Summary:        KDE integration to mount CD-ROM filesystem images
Summary(zh_CN.UTF-8):	KDE 集成的挂载光驱镜像文件
Version:        20061108
Release:        4%{?dist}
License:        GNU General Public License (GPL)
Group:          Applications/System
Group(zh_CN.UTF-8):	应用程序/系统
Source:         %{name}-%{version}.tar.bz2
Patch0:		kfuseiso-20061108.patch
Patch1:		kfuseiso-20061108-admin.patch
URL:            http://fuse.sourceforge.net/wiki/index.php/FuseIso
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
KFuseIso provides KDE integration to mount CD-ROM filesystem images, such as .iso, .nrg, 
.bin, .mdf, and .img files. It uses fuseiso to do the actual job.

%description -l zh_CN.UTF-8
KFuseISo 提供了一个 KDE 集成挂载 ISO 镜像文件的功能，比如 .iso, .bin, .nrg, .mdf和.img文件。
它使用 fuseiso 来做实际的工作。

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
make -f admin/Makefile.common
%configure
#临时措施
sed -i 's/\/include\/tqt/\/include\/tqt \-lqt\-mt \-ltdecore \-ltdeui \-lDCOP \-lkio/g' src/Makefile
make

%install
make DESTDIR="$RPM_BUILD_ROOT" install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc AUTHORS COPYING* ChangeLog NEWS README* TODO
%{_bindir}/*
%{_libdir}/trinity/*
%{_datadir}/*

%changelog -n fuseiso
* Sun Oct 19 2008 Liu Di <liudidi@gmail.com> - 20061108-3mgc
- 添加补丁1，修正中文文件名 iso 挂载问题

* Mon Feb 06 2007 Liu Di <liudidi@gmail.com> - 20061108-1mgc
- initial package (version 20061108)
