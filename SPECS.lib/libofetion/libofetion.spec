Name: libofetion
Version: 2.2.2
Release: 4%{?dist}
Summary: Fetion GTK+ fronted, based on Fetion v4 protocal
Summary(zh_CN.UTF-8): 飞信 GTK+ 前端，基于飞信 v4 协议
Group: Appications/Internet
Group(zh_CN.UTF-8): 应用程序/互联网
License: GPLv2
URL: http://ofetion.googlecode.com
Source0: http://ofetion.googlecode.com/files/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)

BuildRequires: libxml2-devel
BuildRequires: openssl-devel
BuildRequires: gtk2-devel
BuildRequires: gstreamer-devel
BuildRequires: libnotify-devel

%description
Fetion GTK+ frontend app, based on Fetion v4 protocal.

%description -l zh_CN.UTF-8
飞信 GTK+ 前端，基于飞信 v4 协议。

%package devel
Summary: Development files for openfetion
Summary(zh_CN.UTF-8): openfetion 的开发文件
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
This package contains libraries, header files and developer documentation 
needed for developing software which uses the openfetion app.

%description devel -l zh_CN.UTF-8
本软件包包含了使用 openfetion 开发应用程序所需的库、头文件和开发文档。

%prep
%setup -q

%build

%cmake .
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING LICENSE README
%{_datadir}/*
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 2.2.2-4
- 为 Magic 3.0 重建

* Wed Jul 23 2014 Liu Di <liudidi@gmail.com> - 2.2.2-3
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 2.2.2-2
- 为 Magic 3.0 重建

* Thu Aug 19 2010 Ni Hui <shuizhuyuanluo@126.com> - 1.8-1mgc
- 首次生成 rpm 包
- 庚寅  七月初十
