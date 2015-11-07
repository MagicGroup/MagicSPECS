Name: chmlib
Summary: Library for dealing with ITSS/CHM format files
Summary(zh_CN.UTF-8): 处理 ITSS/CHM 格式文件的库
Version: 0.40
Release: 4%{?dist}
License: LGPL
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Url: http://www.jedrea.com/chmlib/
Source: 	http://www.jedrea.com/chmlib//%{name}-%{version}.tar.bz2
Patch0: chmlib-chm_lib_c-ppc-patch.diff
Patch1: chmlib-chm_lib_c-mips64-patch.diff
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
CHMLIB is a library for dealing with ITSS/CHM format files. Right now, it is 
a very simple library, but sufficient for dealing with all of the .chm files 
I've come across. Due to the fairly well-designed indexing built into this 
particular file format, even a small library is able to gain reasonably good 
performance indexing into ITSS archives.

%description -l zh_CN.UTF-8
CHMLIB 是一个处理 ITSS/CHM 格式文件的库。

%package tools
Summary:	Some tools with ITSS/CHM format files
Summary(zh_CN.UTF-8): 处理 ITSS/CHM 格式文件的工具集
Group:		Development/Tools
Group(zh_CN.UTF-8): 开发/工具
Requires:	%{name} = %{version}-%{release}

%description tools
Some tools with ITSS/CHM format files.

%description tools -l zh_CN.UTF-8
处理 ITSS/CHM 格式文件的工具集。

%package devel
Summary:	Library for dealing with ITSS/CHM format files - development files
Summary(zh_CN.UTF-8): 处理 ITSS/CHM 格式文件的库 - 开发文件
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:	%{name} = %{version}-%{release}

%description devel
Files needed for developing apps using chmlib.

%description devel -l zh_CN.UTF-8
使用 chmlib 开发程序需要的文件

%prep
%setup -q 
%patch0 -p0
%patch1 -p1

%build
%configure --disable-static --enable-examples
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} DESTDIR=%{buildroot} install
%{__rm} -f %{buildroot}/%{_libdir}/*.la
%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
%{__rm} -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files
%defattr(-,root,root,-)
%{_libdir}/libchm.so.*
%doc README AUTHORS COPYING NEWS

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/libchm.so

%files tools
%defattr(-,root,root,-)
/usr/bin/chm_http
/usr/bin/enum_chmLib
/usr/bin/enumdir_chmLib
/usr/bin/extract_chmLib
/usr/bin/test_chmLib

%changelog
* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 0.40-4
- 为 Magic 3.0 重建

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 0.40-3
- 为 Magic 3.0 重建

* Sun Dec 16 2007 Ni Hui <shuizhuyuanluo@126.com> - 0.39-0.1mgc
- rebuild for MagicLinux-2.1
