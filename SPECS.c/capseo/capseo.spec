%define svn_version 20081031

Summary: realtime encoder/decoder library
Summary(zh_CN.UTF-8): 实时编码/解码库
Name: capseo
Version: 0.3.0
Release: 0.%{svn_version}.0.2%{?dist}.1
URL: http://rm-rf.in/captury
Source: %{name}_%{version}+svn%{svn_version}.orig.tar.bz2
License: GPL
Group: System/Libraries
Group(zh_CN.UTF-8): 系统/库
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
The capseo codec is meant to encode fast, not to generate 
the smallest files on your file system.

Proposed Filename Extension for raw Encoded Streams:
    .cps
    .captury

%description -l zh_CN.UTF-8
实时编码/解码库。

%package devel
Summary: Library and include files for capseo
Summary(zh_CN.UTF-8): capseo 的库和头文件
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}

%description devel
Library and include files for applications that want to use capseo.

%description devel -l zh_CN.UTF-8
capseo 的库和头文件。

%prep
%setup -q -n %{name}_%{version}+svn%{svn_version}

%build
./autogen.sh
%configure --enable-shared \
	--enable-static \
	--enable-theora

make CFLAGS="$RPM_OPT_FLAGS"

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install
rm %{buildroot}%{_libdir}/*.la

%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog README NEWS TODO COPYING
%{_bindir}/*
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/pkgconfig/capseo.pc

%changelog
* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 0.3.0-0.20081031.0.2.1
- 为 Magic 3.0 重建

* Wed Feb 6 2008 Ni Hui <shuizhuyuanluo@126.com> - 0.3.0-0.svn20070725.0.2mgc
- 重建

* Sat Dec 15 2007 Ni Hui <shuizhuyuanluo@126.com> - 0.3.0-0.svn20070725.0.1mgc
- 首次制作 rpm 包 for MagicLinux-2.1
