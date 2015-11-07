# $Revision: 1.9 $, $Date: 2007-12-27 00:24:45 $
Summary:	Liblazy - D-Bus methods provided for convenience
Summary(zh_CN.UTF-8): Liblazy - 方便提供的 D-Bus 模式
Name:		liblazy
Version:	0.2
Release:	7%{?dist}
License:	LGPL v2.1+
Group:        System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Source0:	http://people.freedesktop.org/~homac/liblazy/%{name}-%{version}.tar.bz2
# Source0-md5:	d1a91efd155dcd1467c2768447d01e42
URL:		http://freedesktop.org/wiki/Software_2fliblazy
BuildRequires:	dbus-devel >= 1.0
BuildRequires:	pkgconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Liblazy is a simple and easy to use library that provides convenient
functions for sending messages over the D-Bus daemon, querying
information from HAL or asking PolicyKit for a privilege. Its features
may grow as needed, though.

%description -l zh_CN.UTF-8
Liblazy 是一个简单并且容易使用的库，它提供了方便的函数来在 D-Bus 服务
上发送信息，从 HAL 查询信息或询问 PolicyKit 的权限。

%package devel
Summary:	Header files for liblazy
Summary(zh_CN.UTF-8):	liblazy 的头文件和库
Group:		Development/Libraries
Group(zh_CN.UTF-8):	开发/库
Requires:	%{name} = %{version}-%{release}
Requires:	dbus-devel >= 1.0

%description devel
Header files for liblazy.

%description devel -l zh_CN.UTF-8
liblazy 的头文件和库。

%prep
%setup -q

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS README
%attr(755,root,root) %{_libdir}/lib*.so.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/*.la
%{_includedir}/liblazy.h
%{_libdir}/pkgconfig/lazy.pc
%{_libdir}/liblazy.a

%changelog
* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 0.2-7
- 为 Magic 3.0 重建

* Fri Jul 18 2014 Liu Di <liudidi@gmail.com> - 0.2-6
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.2-5
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Liu Di <liudidi@gmail.com> - 0.2-4
- 为 Magic 3.0 重建

* Tue Jul 22 2008 Liu Di <liudidi@gmail.com> - 0.2-2mgc
- 修正组别的问题

* Fri Jun 13 2008 Liu Di <liudidi@gmail.com> - 0.2-1mgc
- 首次为 Magic 打包
- powersave 包需要此包
