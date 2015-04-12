Name: openfetion
Version: 2.2.1
Release: 3%{?dist}
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
BuildRequires: libofetion-devel

Requires: libofetion

%description
Fetion GTK+ frontend app, based on Fetion v4 protocal.

%description -l zh_CN.UTF-8
飞信 GTK+ 前端，基于飞信 v4 协议。

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

%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_datadir}/*

%changelog
* Fri Mar 27 2015 Liu Di <liudidi@gmail.com> - 2.2.1-3
- 为 Magic 3.0 重建

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 2.2.1-2
- 为 Magic 3.0 重建

* Thu Aug 19 2010 Ni Hui <shuizhuyuanluo@126.com> - 1.8-1mgc
- 首次生成 rpm 包
- 庚寅  七月初十
