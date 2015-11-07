# NOTE: packages that can use jasper:
# ImageMagick
# kdelibs
# netpbm

Name: jasper
Summary: Implementation of the JPEG-2000 standard, Part 1
Summary(zh_CN.UTF-8): JPEG-2000 标准，第 1 部分的实现
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Version: 1.900.1
Release: 7%{?dist}
License: JasPer License Version 2.0
URL: http://www.ece.uvic.ca/~mdadams/jasper/
Source0: http://www.ece.uvic.ca/~mdadams/jasper/software/%{name}-%{version}.zip

Patch1: jasper-1.701.0-GL.patch
# autoconf/automake bits of patch1
Patch2: jasper-1.701.0-GL-ac.patch
# CVE-2007-2721 (bug #240397)
# borrowed from http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=413041;msg=88
Patch3: patch-libjasper-stepsizes-overflow.diff
# borrowed from http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=469786 
Patch4: jpc_dec.c.patch
# OpenBSD hardening patches addressing couple of possible integer overflows
# during the memory allocations
# https://bugzilla.redhat.com/show_bug.cgi?id=CVE-2008-3520
Patch5: jasper-1.900.1-CVE-2008-3520.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=CVE-2008-3522
Patch6: jasper-1.900.1-CVE-2008-3522.patch
# add pkg-config support
Patch7: jasper-pkgconfig.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: automake
BuildRequires: libjpeg-devel
# "freeglut-devel: Requires: libGL-devel libGLU-devel" (#179464)
BuildRequires: freeglut-devel libGL-devel libGLU-devel

%description
This package contains an implementation of the image compression
standard JPEG-2000, Part 1. It consists of tools for conversion to and
from the JP2 and JPC formats.

%description -l zh_CN.UTF-8
本软件包包含了 JPEG-2000 图像压缩标准，第 1 部分的实现。它包含了双向转换 JP2 和 JPC 格式的工具。

%package devel
Summary: JPEG-2000 library developer files
Summary(zh_CN.UTF-8): JPEG-2000 库开发文件
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}
Requires: libjpeg-devel

%description devel
JPEG-2000 library developer files.

%description devel -l zh_CN.UTF-8
JPEG-2000 库开发文件。

%prep
%setup -q -n %{name}-%{version}

%patch1 -p1 -b .GL
%patch2 -p1 -b .GL-ac
%patch3 -p1 -b .CVE-2007-2721
%patch4 -p1 -b .jpc_dec_assertion
%patch5 -p1 -b .CVE-2008-3520
%patch6 -p1 -b .CVE-2008-3522
%patch7 -p1 -b .pkgconfig


%build
autoreconf -i
%configure \
  --enable-shared \
  --enable-static

%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} DESTDIR=%{buildroot} install

# Unpackaged files
%{__rm} -f doc/README
%{__rm} -f %{buildroot}%{_libdir}/lib*.la

%check
%{__make} check

%clean
%{__rm} -rf %{buildroot} %{_builddir}/%{buildsubdir}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYRIGHT LICENSE NEWS README
%{_bindir}/imgcmp
%{_bindir}/jiv
%{_bindir}/imginfo
%{_bindir}/*jasper*
%{_bindir}/tmrdemo
%{_libdir}/lib*.so.*
%{_mandir}/man1/*

%files devel
%defattr(-,root,root,-)
%doc doc/*
%{_includedir}/jasper/
%{_libdir}/lib*.so
%{_libdir}/*.a
%{_libdir}/pkgconfig/*.pc

%changelog
* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 1.900.1-7
- 为 Magic 3.0 重建

* Mon Apr 21 2014 Liu Di <liudidi@gmail.com> - 1.900.1-6
- 为 Magic 3.0 重建

* Mon Apr 21 2014 Liu Di <liudidi@gmail.com> - 1.900.1-5
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.900.1-4
- 为 Magic 3.0 重建

* Tue Dec 13 2011 Liu Di <liudidi@gmail.com> - 1.900.1-3
- 为 Magic 3.0 重建

* Fri Nov 23 2007 Ni Hui <shuizhuyuanluo@126.com> - 1.900.1-0.3mgc
- rebuilt
- 恢复 /usr/bin/jiv

* Sat Oct 20 2007 Ni Hui <shuizhuyuanluo@126.com> - 1.900.1-0.2mgc
- rebuilt
- 丢失文件 jiv （无用）

* Wed Oct 3 2007 Ni Hui <shuizhuyuanluo@126.com> - 1.900.1-0.1mgc
- first spec file for MagicLinux-2.1
- 去除 GEO jasper 部分以及过时的相关 GL 补丁
