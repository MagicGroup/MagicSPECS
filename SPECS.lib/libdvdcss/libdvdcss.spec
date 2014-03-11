Name: libdvdcss
Version: 1.2.10
Release: 3%{?dist}

Summary: A portable abstraction library for DVD decryption
Summary(zh_CN.UTF-8): 加密 DVD 的一个可移植抽取库
License: GPL
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Url: http://www.videolan.org/libdvdcss

Packager: Liu Di <liudidi@gmail.com>

Source: %name-%version.tar.bz2

# Put css.h %name.h to %_includedir/dvdcss
Patch0: %name-1.2.6-alt-more_headrs_makefile.patch
Patch1: libdvdcss-1.2.9-alt-tmpdir.patch

# Automatically added by buildreq on Mon May 08 2006
BuildRequires: doxygen

BuildRoot: %{_tmppath}/%{name}-%{version}-root

%description
This is a portable abstraction library for DVD decryption.

libdvdcss is part of the VideoLAN project, a full MPEG2 client/server
solution. The VideoLAN Client can also be used as a standalone program
to play MPEG2 streams from a hard disk or a DVD.

%description -l zh_CN.UTF-8
这是一个抽取加密DVD的一个可移植库。

libdvdcss 是一个 VideoLAN 项目的一部分，一个完整的 MPEG2 客户端/服务器解决方案。
VideoLAN 客户端(VLC)也可以做为单独的程序来播放硬盘或 DVD 上的 MPEG2 流。

%package devel
Summary: Development environment for %name
Summary(zh_CN.UTF-8): %{name} 的开发环境
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %name = %version-%release

%description devel
This package contains development files required for building
%name-based software.

%description devel -l zh_CN.UTF-8
这个包包含了编译基于 %{name} 的软件所需要的开发文件。

%package devel-static
Summary: Static %name library
Summary(zh_CN.UTF-8): %{name}静态库
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %name-devel = %version-%release

%description devel-static
This package contains development files required for building
statically linked %name-based software.

%description devel-static -l zh_CN.UTF-8
这个包包含了静态链接编译基于 %{name} 软件所需要的开发文件。

%prep
%setup -q

#%patch0 -p1
#%patch1 -p1

%build
autoreconf -fisv
%configure \
    --enable-static
make

%install
%makeinstall
rm %{buildroot}%{_libdir}/*.la

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc AUTHORS README
%_libdir/*.so.*

%files devel
%doc doc/html
%_includedir/*
%_libdir/*.so
%_libdir/pkgconfig/*.pc

%files devel-static
%_libdir/*.a

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.2.10-3
- 为 Magic 3.0 重建

* Thu Jan 05 2012 Liu Di <liudidi@gmail.com> - 1.2.10-2
- 为 Magic 3.0 重建

* Mon Oct 09 2006 Liu Di <liudidi@gmail.com> - 1.2.9-1mgc
- rebuild for Magic

