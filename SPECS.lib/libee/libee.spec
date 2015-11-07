Summary: Event expression library inspired by CEE
Summary(zh_CN.UTF-8): 来自于 CEE 的事件表达库
Name: libee
Version: 0.4.1
Release: 5%{?dist}

License: LGPLv2+ and MIT and GPL+ 
Group: System Environment/Libraries 
Group(zh_CN.UTF-8): 系统环境/库
URL: http://www.libee.org
Source0: http://www.libee.org/files/download/%{name}-%{version}.tar.gz

BuildRequires: libestr-devel
BuildRequires: chrpath

%description
The core idea of libee is to provide a small but hopefully convenient API layer
above the CEE standard. CEE is under heavy development and even some of its 
core data structures have not been fully specified.

CEE is an upcoming standard used to describe network events in a number of
normalized formats. It's goal is to unify many different
representations that exist in the industry.

%description -l zh_CN.UTF-8
来自于 CEE 的事件表达库。

%package devel
Summary: Development files for libee
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:   %{name}%{?_isa} = %{version}-%{release}
Requires: libestr-devel%{?_isa}

%package utils
Summary:   Optional utilities like libee-convert 
Summary(zh_CN.UTF-8): 类似 libee-convert 的可选工具
Requires:   %{name}%{?_isa} = %{version}-%{release}

%description devel
This package provides files required for development with libee,
the event expression library used by the rsyslog daemon.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%description utils
The libee-convert utility provided by event expression library.

%description utils -l zh_CN.UTF-8
类似 libee-convert 的可选工具。

%prep
%setup -q  -n %{name}-%{version}

%build
%configure 
V=1 make

%install
make install INSTALL="install -p" DESTDIR=%{buildroot}
rm -f %{buildroot}/%{_libdir}/*.{a,la}
chrpath --delete %{buildroot}%{_libdir}/libee.so.*
chrpath --delete %{buildroot}%{_sbindir}/libee-convert
magic_rpm_clean.sh

%check
make check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc README COPYING AUTHORS ChangeLog
%{_libdir}/libee.so.0
%{_libdir}/libee.so.0.0.0

%files devel
%{_libdir}/pkgconfig/libee.pc
%dir %{_includedir}/libee
%{_includedir}/libee/*.h
%{_libdir}/*.so

%files utils
%{_sbindir}/*

%changelog
* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 0.4.1-5
- 为 Magic 3.0 重建

* Tue Jul 15 2014 Liu Di <liudidi@gmail.com> - 0.4.1-4
- 为 Magic 3.0 重建

* Thu Sep 20 2012 Mahaveer Darade <mdarade@redhat.com> - 0.4.1-3
- Added check to enable testsuite in tests dir

* Mon Aug 27 2012 mdarade <mdarade@redhat.com> - 0.4.1-2
- Added separate util package to have libee-convert utility


* Tue Aug 7 2012 Mahaveer Darade <mdarade@redhat.com> 0.4.1-1
- Initial port
