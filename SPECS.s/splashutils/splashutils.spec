%global  _hardened_build        0
%define _hardened_cflags       %{nil}
%define _hardened_ldflags      %{nil}

Summary:			Splashutils - fbsplash utils and miscellaneous framebuffer utilities
Summary(zh_CN.UTF-8):			Splashutils - fbsplash 的相关程序以及一些帧缓冲工具
Name:				splashutils
Version:			1.5.4.4
Release:			3%{?dist}

Source:				http://dev.gentoo.org/~spock/projects/gensplash/archive/splashutils-lite-%{version}.tar.bz2
Source1:			http://dev.gentoo.org/~spock/projects/gensplash/current/miscsplashutils-0.1.8.tar.bz2
Source2:			luxisri.ttf
Source3:			splash.conf
Source4:			splashrcfunction.sh
Source5:			splashutils-gentoo-1.0.17.tar.bz2

Source10:			libpng-1.4.3.tar.bz2
Source11:			jpegsrc.v8a.tar.gz
Source12:			freetype-2.3.12.tar.bz2
Source13:			zlib-1.2.3.tar.bz2


Patch0:				splashutils-progress.patch
Patch1:				splashutils-bootmsg.diff
Patch2:				splashutils-1.5.4.4-bzip2.patch
Patch3:				splashutils-1.5.4.4-freetype-bz2.patch
Patch4:				splashutils-1.5.4.4-format-security.patch
Patch5:				splashutils-1.5.4.4-freetype2.patch 
Patch6:				miscsplashutils-0.1.8-freetype2.patch

URL:				http://dev.gentoo.org/~spock/projects/gensplash/

Group:				Applications/System
Group(zh_CN.UTF-8):			应用程序/系统
Packager:			Jiang Tao < jiangtao9999@163.com >
Distribution:			Magic Linux 2.1
License:				GPL
BuildRoot:			%{_tmppath}/%{name}-%{version}-%{release}-buildroot

Requires:			libjpeg, libpng, freetype
BuildRequires:			gcc
BuildRequires:			libjpeg-turbo-devel, libjpeg-turbo-static
BuildRequires:			libpng-devel, libpng-static
BuildRequires:			freetype-devel
BuildRequires:			klibc-devel
BuildRequires:			libmng-static, libmng-devel, freetype-static, gpm-devel, gpm-static, lcms-devel, bzip2-static

%description
fbsplash (formerly gensplash) is a userspace implementation of a splash 
screen for Linux systems. It provides a graphical environment during 
system boot using the Linux framebuffer layer.
Currently, all core programs, libraries and scripts developed as parts of 
the fbsplash project are available in a single package called splashutils. 

%description -l zh_CN.UTF-8
fbsplash (formerly gensplash) 是一个 Linux 系统飞溅屏幕的用户空间
实现。它提供一个使用帧缓冲层图形环境下的 Linux 启动界面。
通常的，作为 fbsplash 项目下面开发的所有核心程序，函数库和脚本都
在一个名叫 splashutils 包中提供。

%prep

tar xfj %{SOURCE0}
tar xfj %{SOURCE1}
tar xfj %{SOURCE5}

cd %{name}-%{version}

ln -s ./ core

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch4 -p1
%patch5 -p1

cd libs
tar xf %{SOURCE10}
tar xf %{SOURCE11}
tar xf %{SOURCE12}
tar xf %{SOURCE13}
cd ..

rm libs/zlib-1.2.3/Makefile
echo > libs/klibc_compat.h

%build
cd %{name}-%{version}
autoreconf -fisv
%configure --with-mng --with-jpeg-src=libs/jpeg-8a --with-lpng-src=libs/libpng-1.4.3 --with-zlib-src=libs/zlib-1.2.3 --with-freetype2-src=libs/freetype-2.3.12
make -j1

cd ../miscsplashutils-0.1.8
patch -p0 -i %{PATCH3}
patch -p1 -i %{PATCH6}
make %{?_smp_mflags}

%install
%{__rm} -rf "%{buildroot}"

cd %{name}-%{version}
make DESTDIR=$RPM_BUILD_ROOT install 
cd ../miscsplashutils-0.1.8
make DESTDIR=$RPM_BUILD_ROOT install 
cd ..

mkdir -p $RPM_BUILD_ROOT/lib/splash/tmp
mkdir -p $RPM_BUILD_ROOT/lib/splash/sys
mkdir -p $RPM_BUILD_ROOT/lib/splash/cache

mkdir -p $RPM_BUILD_ROOT/etc/splash

cp %{SOURCE2} $RPM_BUILD_ROOT/etc/splash/
cp %{SOURCE3} $RPM_BUILD_ROOT/etc/splash/splash

mkdir -p $RPM_BUILD_ROOT/etc/init.d/
cp %{SOURCE4} $RPM_BUILD_ROOT/etc/init.d/

mkdir -p $RPM_BUILD_ROOT/usr/share/splashutils/
cp splashutils-gentoo-1.0.17/initrd.splash $RPM_BUILD_ROOT/usr/share/splashutils/

magic_rpm_clean.sh

%clean
%{__rm} -rf %{name}-%{version}
%{__rm} -rf miscsplashutils-0.1.8
%{__rm} -rf splashutils-gentoo-1.0.17

%files
%defattr(-,root,root)
%{_sysconfdir}/init.d/splashrcfunction.sh
%{_sysconfdir}/splash/*
/sbin/*
%{_bindir}/*
%{_includedir}/fbsplash.h
%{_libdir}/libfbsplash.*
%{_libdir}/libfbsplashrender.*
%{_libdir}/pkgconfig/*
/lib/splash/*
%{_sbindir}/*
%{_docdir}/splashutils/*
%{_datadir}/splashutils/initrd.splash

%changelog
* Thu Jun 14 2012 JiangTao <jiangtao9999@163.com> - 1.5.4.4-2
- Update to 1.5.4.4 for Magic Linux 3.0
- Add initrd.splash which is needed by dracut

* Thu Aug 21 2008 Jiang Tao < jiangtao9999@163.com> - 1.5.4.2-3mgc
- Split the fbsplash-control-code from initscript to splashrcfunction.sh which is included in this package.

* Mon Aug 4 2008 Jiang Tao < jiangtao9999@163.com> - 1.5.4.2-2mgc
- Add BOOT_MSG patch. It let fbsplash kernel helper display a Chinese String.
- Set Chinese String in splash.conf (Install to /etc/splash/splash ).
- luxisri.ttf now is a MODUFIED font. It is a Part of wqy-zhenhei.
- Enabled mng support.

* Sat Aug 2 2008 Jiang Tao < jiangtao9999@163.com> - 1.5.4.2-1mgc
- Build rpm for Magic Linux 2.1 rc1
