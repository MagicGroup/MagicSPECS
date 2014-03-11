%define rversion 20090816
%define betatag %{nil}
%define real_name kfuseiso

Name: kde4-kfuseiso
Summary: KDE integration to mount CD-ROM filesystem images
Summary(zh_CN.UTF-8): KDE 集成的挂载光驱镜像文件
Version: %{rversion}
Release: 0.3%{?dist}
License: GPL v2 or Later
Group: Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
URL: http://fuse.sourceforge.net/wiki/index.php/FuseIso
Source0: 110509-%{real_name}-%{version}.tar.gz
Patch1:	 kfuseiso-20090816-gcc4.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: cmake >= 2.6.2
BuildRequires: gettext
BuildRequires: libkdelibs4-devel

%description
KFuseIso provides KDE integration to mount CD-ROM filesystem images, such as .iso, .nrg,
.bin, .mdf, and .img files. It uses fuseiso to do the actual job.

%description -l zh_CN.UTF-8
KFuseISo 提供了一个 KDE 集成挂载 ISO 镜像文件的功能，比如 .iso, .bin, .nrg, .mdf和.img文件。
它使用 fuseiso 来做实际的工作。

%prep
%setup -q -n %{real_name}-%{rversion}%{betatag}
%patch1 -p1

%build
mkdir build
cd build
%cmake_kde4 ..

make %{?_smp_mflags}

%install
cd build
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

magic_rpm_clean.sh

%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root,-)
%{kde4_bindir}/*
%{kde4_appsdir}/kfuseiso
%{kde4_libdir}/kde4/*.so
%{kde4_xdgappsdir}/kfuseisomount.desktop
%{kde4_servicesdir}/*
%{kde4_datadir}/mimelnk/application/x-iso-image.desktop
%{kde4_datadir}/mimelnk/inode/x-iso-image-mounted.desktop


%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 20090816-0.3
- 为 Magic 3.0 重建

* Tue Dec 20 2011 Liu Di <liudidi@gmail.com> - 20090816-0.2
- 为 Magic 3.0 重建


