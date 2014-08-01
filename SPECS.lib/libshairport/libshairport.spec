%define	gitdate	20121216

Summary:	Apple RAOP server library
Summary(zh_CN.UTF-8): 苹果 RAOP 服务库
Name:		libshairport
Version:	1.2.1
Release:	3%{?dist}
License:	MIT
Group:		System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL:		https://github.com/amejia1/libshairport
# git archive --prefix libshairport-20120111/ master | xz > libshairport-20120111.tar.xz
Source:		%{name}-%{gitdate}.tar.xz
BuildRequires:	openssl-devel
BuildRequires:	libao-devel

%description
This library emulates an AirPort Express for the purpose of streaming
music from iTunes and compatible iPods. It implements a server for the
Apple RAOP protocol.

ShairPort does not support AirPlay v2 (video and photo streaming).

%description -l zh_CN.UTF-8
苹果 RAOP 服务库.

它不支持 AirPlay v2。

%package devel
Summary:	Headers for libshairport development
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:	%{name} = %{version}
# we are not actually linking against it (just using the headers), so this
# doesn't get added automatically:
Requires:	libao-devel
Provides:	shairport-devel = %{version}

%description devel
libshairport is an Apple RAOP server library.

This package contains the headers that are needed to compile
applications that use libshairport.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n %{name}-%{gitdate}

%build
autoreconf -fi
%configure --disable-static
make

%install
rm -rf %{buildroot}
%makeinstall
rm -f %{buildroot}%{_libdir}/*.la
magic_rpm_clean.sh

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%doc README
%{_libdir}/*.so
%dir %{_includedir}/shairport
%{_includedir}/shairport/*.h
%{_libdir}/pkgconfig/%{name}.pc



%changelog
* Thu Jul 31 2014 Liu Di <liudidi@gmail.com> - 1.2.1-3
- 为 Magic 3.0 重建

* Thu Jul 31 2014 Liu Di <liudidi@gmail.com> - 1.2.1-2
- 更新到 20140731 日期的仓库源码

* Thu Jul 31 2014 Liu Di <liudidi@gmail.com> - 1.2.1-2
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.2.1-0.git20120409.1.1
- 为 Magic 3.0 重建

