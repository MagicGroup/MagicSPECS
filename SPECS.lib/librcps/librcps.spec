Name: librcps
Version: 0.3
Release: 5%{?dist}
Summary: Library for resource constrained project scheduling
Summary(zh_CN.UTF-8): 资源驱动的项目计划库
License: GPLv2
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL: http://www.librcps.org/
Source0: http://www.librcps.org/%{name}-%{version}.tar.gz
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%description
Librcps is a library for resource constrained project scheduling.

%description -l zh_CN.UTF-8
Librcps 是资源驱动的项目计划库。

%package devel
Summary: Libraries and header files for %{name}
Summary(zh_CN.UTF-8): %{name} 的库和头文件
Group: Development/Languages
Group(zh_CN.UTF-8): 开发/语言
Requires: pkgconfig

%description devel
This package contains library and header files needed to develop new
native programs that use the %{name} libraries.

%description devel -l zh_CN.UTF-8
本软件包包含了使用 %{name} 库开发程序所需的库和头文件。

%prep
%setup -q

%build
%configure --enable-shared --disable-static
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

rm -f %{buildroot}%{_libdir}/*.la

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/*.so

%changelog
* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 0.3-5
- 为 Magic 3.0 重建

* Wed Jul 30 2014 Liu Di <liudidi@gmail.com> - 0.3-4
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.3-3
- 为 Magic 3.0 重建

* Wed Jan 11 2012 Liu Di <liudidi@gmail.com> - 0.3-2
- 为 Magic 3.0 重建



