Summary: A library that performs asynchronous DNS operations
Summary(zh_CN): 操作同步 DNS 的库
Name: c-ares
Version:	1.10.0
Release: 3%{?dist}
License: MIT
Group: System Environment/Libraries
Group(zh_CN): 系统环境/库
URL: http://c-ares.haxx.se/
Source0: http://c-ares.haxx.se/download/c-ares-%{version}.tar.gz
Source1: LICENSE
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
c-ares is a C library that performs DNS requests and name resolves 
asynchronously. c-ares is a fork of the library named 'ares', written 
by Greg Hudson at MIT.

%description -l zh_CN
操作同步 DNS 的库。

%package devel
Summary: Development files for c-ares
Summary(zh_CN): %name 的开发包
Group: Development/Libraries
Group(zh_CN): 开发/库
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
This package contains the header files and static libraries needed to
compile applications or shared objects that use c-ares.

%description devel -l zh_CN
%name 的开发包。

%prep
%setup -q
cp %{SOURCE1} .

%build
%configure --enable-shared
%{__make} %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
rm -rf $RPM_BUILD_ROOT/%{_libdir}/libcares.la
rm -rf $RPM_BUILD_ROOT/%{_libdir}/libcares.a

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-, root, root)
%doc README README.cares CHANGES NEWS LICENSE
%{_libdir}/*.so.*

%files devel
%defattr(-, root, root, 0755)
%{_includedir}/ares.h
%{_includedir}/ares_*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/libcares.pc
%{_mandir}/man3/ares_*

%changelog
* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 1.10.0-3
- 更新到 1.10.0

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 1.7.5-2
- 为 Magic 3.0 重建

* Sun Oct 30 2011 Liu Di <liudidi@gmail.com> - 1.7.5-1
- 升级到 1.7.5
