Name:           fuseiso
BuildRequires:  fuse-devel glib2-devel
Summary:        fuseiso is a FUSE module to mount ISO filesystem images
Summary(zh_CN.UTF-8):	fuseiso 是一个 FUSE 的模块可以挂载 ISO 镜像文件
Version:        20070708
Release:        7%{?dist}
License:        GNU General Public License (GPL)
Group:          Applications/System
Group(zh_CN.UTF-8):	应用程序/系统
Source:         %{name}-%{version}.tar.bz2
Patch:		fuseiso-largeiso.patch
URL:            http://fuse.sourceforge.net/wiki/index.php/FuseIso
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
Mount ISO filesystem images as a non-root user. Currently supports
plain ISO9660 Level 1 and 2, Rock Ridge, Joliet, zisofs.

Authors:
--------
    Dmitry Morozhnikov <dmiceman@mail.ru>

%description -l zh_CN.UTF-8
在非 root 用户下挂载 ISO 镜像文件。当前支持 .iso, .bin, .nrg, .mdf, .img

%prep
%setup -q
%patch -p0

%build
%configure
make %{?_smp_flags}

%install
make DESTDIR="$RPM_BUILD_ROOT" install
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc AUTHORS COPYING* ChangeLog NEWS README* TODO
%{_bindir}/*

%changelog -n fuseiso
