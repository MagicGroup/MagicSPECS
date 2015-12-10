# asio only ships headers, so no debuginfo package is needed
%define debug_package %{nil}

Summary: A cross-platform C++ library for network programming
Summary(zh_CN.UTF-8): 跨平台的网络程序 C++ 库
Name: asio
Version: 1.10.4
Release: 3%{?dist}
URL: http://sourceforge.net/projects/asio/
Source0: http://downloads.sourceforge.net/asio/asio-%{version}.tar.bz2
License: Boost
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: openssl-devel
BuildRequires: boost-devel

%description
The asio package contains a cross-platform C++ library for network programming
that provides developers with a consistent asynchronous I/O model using a
modern C++ approach.

%description -l zh_CN.UTF-8
跨平台的网络程序 C++ 库。

%package devel
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Summary: Header files for asio
Summary(zh_CN.UTF-8): %name 的开发包。
Requires: openssl-devel
Requires: boost-devel

%description devel
Header files you can use to develop applications with asio.

The asio package contains a cross-platform C++ library for network programming
that provides developers with a consistent asynchronous I/O model using a
modern C++ approach.

%description devel -l zh_CN.UTF-8
%name 的开发包。

%prep
%setup -q

%build
%configure

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT nobase_includeHEADERS_INSTALL='install -D -p -m644'

%check
make %{?_smp_mflags}

%clean
rm -rf $RPM_BUILD_ROOT

%files devel
%defattr(-,root,root,-)
%doc COPYING LICENSE_1_0.txt doc/*
%dir %{_includedir}/asio
%{_includedir}/asio/*
%{_includedir}/asio.hpp

%changelog
* Sat Nov 07 2015 Liu Di <liudidi@gmail.com> - 1.10.4-3
- 为 Magic 3.0 重建

* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 1.10.4-2
- 更新到 1.10.4

* Sat Mar 01 2014 Liu Di <liudidi@gmail.com> - 1.10.1-1
- 更新到 1.10.1

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 1.4.8-3
- 为 Magic 3.0 重建

* Sun Oct 28 2012 Liu Di <liudidi@gmail.com> - 1.4.8-2
- 为 Magic 3.0 重建

* Wed Oct 26 2011 Liu Di <liudidi@gmail.com> - 1.4.8-1
- 升级到 1.4.8
