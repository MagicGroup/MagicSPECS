Summary:			A minimal libc subset for use with initramfs.
Summary(zh_CN.UTF-8):		一个迷你化的用于 initramfs 里面的 libc
Name:				klibc
Version:			2.0.2
Release:			1%{?dist}
License:			BSD/GPL

Group:				Development/Libraries
Group(zh_CN.UTF-8):		开发/库

URL:				http://www.zytor.com/mailman/listinfo/klibc
Source0:			http://www.kernel.org/pub/linux/libs/klibc-%{version}.tar.xz
Source1:			linux-2.6.39.tar.bz2

BuildRoot:			%{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires:			kernel >= 2.6.0, kernel-headers

Packager:			H. Peter Anvin <hpa@zytor.com>, Jiang Tao <jiangtao9999@163.com>
Prefix:				/usr
Vendor:				Starving Linux Artists

%define klibcdir  %{_libdir}/klibc
%define libdocdir %{_docdir}/%{name}-%{version}-%{release}
%define bindocdir %{_docdir}/%{name}-utils-%{version}-%{release}

%description
%{name} is intended to be a minimalistic libc subset for use with
initramfs.  It is deliberately written for small size, minimal
entanglement, and portability, not speed.

%description -l zh_CN.UTF-8
%{name} 是一个在 initramfs 中使用的最低要求化为目的的 C 库。
它被特意编写为最小的体积、最小化环境、以及可移植性，而不是为了速度。

%package devel
Summary:			Libraries and tools needed to compile applications against klibc.
Summary(zh_CN.UTF-8):		依赖 klibc 而编译程序所需要的库和工具
Group:				开发/库
Requires:			klibc = %{version}-%{release}

%description devel
This package contains the link libraries, header files, and gcc
wrapper scripts needed to compile applications against klibc.

%description devel -l zh_CN.UTF-8
这个包提供依赖 klibc 而编译程序所需要的 link 库、头文件、
以及 gcc 包装器脚本。

%package utils
Summary:			Small utilities built with klibc.
Summary(zh_CN.UTF-8):		klibc 的小程序
Group:				应用程序/系统
Requires: klibc = %{version}-%{release}

%description utils
This package contains a collection of programs that are linked against
klibc.  These duplicate some of the functionality of a regular Linux
toolset, but are typically much smaller than their full-function
counterparts.  They are intended for inclusion in initramfs images and
embedded systems.

%description utils -l zh_CN.UTF-8
这个包包含 klibc 所提供的程序集合。这些副本是部分功能化的一个常
规 linux 工具集，但他们的特点是相对于他们全功能状态体积小。他们
被设计用来放在 initramfs 镜像或者嵌入式系统中。

%prep
%setup -q -a 1
mv linux-2.6.39 linux
#cp -dRs /lib/modules/`uname -r`/build/ ./linux
# Shouldn't need this when getting the build tree from /lib/modules
# make -C linux defconfig ARCH=i386
# make -C linux prepare ARCH=i386
# Deal with braindamage in RedHat's kernel-source RPM
rm -f linux/include/linux/config.h
cat <<EOF > linux/include/linux/config.h
#ifndef _LINUX_CONFIG_H
#define _LINUX_CONFIG_H

#include <linux/autoconf.h>

#endif
EOF
mkdir -p %{buildroot}

%build
make %{_smp_mflags} \
	prefix=%{_prefix} bindir=%{_bindir} \
	INSTALLDIR=%{klibcdir} mandir=%{_mandir} INSTALLROOT=%{buildroot}

%install
rm -rf %{buildroot}
make prefix=%{_prefix} bindir=%{_bindir} \
	INSTALLDIR=%{klibcdir} mandir=%{_mandir} INSTALLROOT=%{buildroot} \
	install

find $RPM_BUILD_ROOT -type f | xargs sed -i "s|$RPM_BUILD_ROOT||g"

# Make the .so file in /lib a hardlink (they will be expanded as two
# files automatically if it crosses filesystems when extracted.)
# ln -f %{buildroot}%{klibcdir}/lib/klibc-*.so %{buildroot}/lib

# Install the docs
mkdir -p %{buildroot}%{bindocdir} %{buildroot}%{libdocdir}
install -m 444 README %{buildroot}%{libdocdir}
#install -m 444 usr/klibc/README %{buildroot}%{libdocdir}/README.klibc
#install -m 444 usr/klibc/arch/README %{buildroot}%{libdocdir}/README.klibc.arch

#install -m 444 usr/gzip/COPYING %{buildroot}%{bindocdir}/COPYING.gzip
#install -m 444 usr/gzip/README %{buildroot}%{bindocdir}/README.gzip
#install -m 444 usr/kinit/ipconfig/README %{buildroot}%{bindocdir}/README.ipconfig
#install -m 444 usr/kinit/README %{buildroot}%{bindocdir}/README.kinit

mv %{buildroot}/lib/* %{buildroot}%{_libdir}

rm -rf %{buildroot}/lib

rm -f %{buildroot}%{klibcdir}/include/asm/asm-i386

mkdir -p %{buildroot}%{klibcdir}/include/asm/asm-i386

magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

#
# Note: libc.so and interp.o are technically -devel files, but
# put them in this package until we can make really, really sure
# the dependency system can avoid confusion.  (In fact, it would be
# good to eventually get them out of here, so that multiple runtimes
# can be installed should it be necessary.)
#
%files
%defattr(-,root,root,-)
%{_libdir}/*.so
%{klibcdir}/lib/*.so
%{klibcdir}/lib/interp.o

%files devel
%defattr(-,root,root,-)
%{klibcdir}/include
%{klibcdir}/lib/*.a
%{klibcdir}/lib/crt0.o
%{_bindir}/klcc
%doc %{_mandir}/man1/*
%doc %{libdocdir}/*

%files utils
%defattr(-,root,root,-)
%{klibcdir}/bin
#%doc %{bindocdir}/*

%changelog
* Tue Jun 12 2012 Jiang Tao <jiangtao9999@163.com> - 2.0-1
- Update to 2.0

* Mon Apr 23 2012 Liu Di <liudidi@gmail.com> - 1.5.15-6
- 为 Magic 3.0 重建

* Mon Apr 23 2012 Liu Di <liudidi@gmail.com> - 1.5.15-5
- 为 Magic 3.0 重建

* Wed Apr 18 2012 Liu Di <liudidi@gmail.com> - 1.5.15-4
- 为 Magic 3.0 重建

* Wed Apr 18 2012 Liu Di <liudidi@gmail.com> - 1.5.15-3
- 为 Magic 3.0 重建

* Fri Dec 30 2011 Liu Di <liudidi@gmail.com> - 1.5.15-2
- 为 Magic 3.0 重建

* Sat Aug 2 2008 Jiang Tao <jiangtao9999@163.com> - 1.5.12-1mgc
- Modify & build for Magic Linux 2.1 rc1

* Tue Mar 1 2005 H. Peter Anvin <hpa@zytor.com>
- New "make install" scheme, klcc

* Tue Jul 6 2004 H. Peter Anvin <hpa@zytor.com>
- Update to use kernel-source RPM for the kernel symlink.

* Sat Nov 29 2003 Bryan O'Sullivan <bos@serpentine.com> -
- Initial build.
