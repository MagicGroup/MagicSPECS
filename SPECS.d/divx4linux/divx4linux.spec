# $Id: divx4linux.spec 3053 2005-03-24 17:16:13Z dag $
# Authority: dag

%define	date 20060201
%define real_version 611

Summary: DivX for Linux codec binaries
Summary(zh_CN.UTF-8): Linux下的DivX解码器的二进制代码
Name: divx4linux
Version: 6.1.1
Release: 4%{?dist}
License: Distributable
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL: http://www.divx.com/divx/linux/

Autoreq: no
Epoch: 1
Packager: Liu Di <liudidi@gmail.com>
Vendor: Magic Group

#Source: http://download.divx.com/divx/divx4linux-std-%{date}.tar.gz
Source: http://download.divx.com/labs/divx611-20060201-gcc4.0.1.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

Requires: gcc > 4.0.1
ExclusiveArch: i386 i686

%description
This archive includes the binary release of DivX Codec 6.1.1 for x86 Linux.

%description -l zh_CN.UTF-8
这个档案包括了x86 Linux下的DivX Codec 6.1.1 的二进制代码。

%package devel
Summary: Header files, libraries and development documentation for %{name}
Summary(zh_CN.UTF-8): %{name}的头文件，库和开发文档
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Autoreq: no
Requires: %{name} = %{epoch}:%{version}-%{release}

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%description devel -l zh_CN.UTF-8
这个包包含了%{name}头文件，静态库和开发文档。如果你要使用%{name}开发程序，
你需要安装 %{name}-devel。

%prep
%setup -n divx611-%{date}-gcc4.0.1

%build
%install
%{__rm} -rf %{buildroot}
unzip -P h08pzt4 contents.dat
%{__install} -Dp -m0755 lib/libdivx.so %{buildroot}%{_libdir}/libdivx.so.0
%{__ln_s} -f %{_libdir}/libdivx.so.0 %{buildroot}%{_libdir}/libdivx.so

%{__install} -d -m0755 %{buildroot}%{_includedir}/divx
%{__cp} -rf  include/* %{buildroot}%{_includedir}/divx
magic_rpm_clean.sh

%post
/usr/sbin/ldconfig 2>/dev/null

%postun
/usr/sbin/ldconfig 2>/dev/nullx

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%{_libdir}/*.so.*

%files devel
%defattr(-, root, root, 0755)
%{_libdir}/*.so
%{_includedir}/*

%changelog
* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 1:6.1.1-4
- 为 Magic 3.0 重建

* Thu Nov 15 2012 Liu Di <liudidi@gmail.com> - 1:6.1.1-3
- 为 Magic 3.0 重建

* Wed Nov 26 2008 Liu Di <liudid@gmail.com> - 6.1.1-0.1%{?dist}
- 更新到 6.1.1

* Thu Aug 14 2003 Dag Wieers <dag@wieers.com> - 3053/dag
- Updated to release 5.0.5.
- Split into a seperate devel package.

* Sun Jan 19 2003 Dag Wieers <dag@wieers.com>
- Initial package. (using DAR)
