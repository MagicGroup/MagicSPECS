
%global glib2_version 2.32.0

%global realversion 1.12.6

Name: libqmi
Summary: Support library to use the Qualcomm MSM Interface (QMI) protocol
Summary(zh_CN.UTF-8): 使用 Qualcomm MSM Interface (QMI) 协议的支持库
Version: %{?realversion}
Release: 2%{?dist}
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
License: LGPLv2+
URL: http://freedesktop.org/software/libqmi

#
# Source from http://freedesktop.org/software/libqmi/
#
Source: http://freedesktop.org/software/libqmi/%{name}-%{realversion}.tar.xz

BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: pkgconfig
BuildRequires: automake autoconf intltool libtool
BuildRequires: python >= 2.7

Requires: glib2 >= %{glib2_version}

%description
This package contains the libraries that make it easier to use QMI functionality
from applications that use glib.

%description -l zh_CN.UTF-8
使用 Qualcomm MSM Interface (QMI) 协议的支持库。

%package devel
Summary: Header files for adding QMI support to applications that use glib
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: glib2-devel
Requires: pkgconfig

%description devel
This package contains the header and pkg-config files for development
applications using QMI functionality from applications that use glib.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package utils
Summary: Utilities to use the QMI protocol from the command line
Summary(zh_CN.UTF-8): 使用 QMI 协议的命令行工具
Requires: %{name}%{?_isa} = %{version}-%{release}
License: GPLv2+

%description utils
This package contains the utilities that make it easier to use QMI functionality
from the command line.

%description utils -l zh_CN.UTF-8
使用 QMI 协议的命令行工具。

%prep
%setup -q -n %{name}-%{realversion}

%build
%configure --disable-static
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
%{__rm} -f $RPM_BUILD_ROOT%{_libdir}/*.la
magic_rpm_clean.sh

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post   devel -p /sbin/ldconfig
%postun	devel -p /sbin/ldconfig


%files
%doc COPYING NEWS AUTHORS README
%{_libdir}/libqmi-glib.so.*

%files devel
%dir %{_includedir}/libqmi-glib
%{_includedir}/libqmi-glib/*.h
%{_libdir}/pkgconfig/qmi-glib.pc
%{_libdir}/libqmi-glib.so
%dir %{_datadir}/gtk-doc/html/libqmi-glib
%{_datadir}/gtk-doc/html/libqmi-glib/*

%files utils
%{_bindir}/qmicli
%{_bindir}/qmi-network
%{_mandir}/man1/*
%{_libexecdir}/qmi-proxy


%changelog
* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 1.12.6-2
- 更新到 1.12.6

* Mon Jul 28 2014 Liu Di <liudidi@gmail.com> - 1.10.0-1
- 更新到 1.10.0

* Sat Feb  1 2014 poma <poma@gmail.com> - 1.8.0-1
- Update to 1.8.0 release

* Fri Sep  6 2013 Dan Williams <dcbw@redhat.com> - 1.6.0-1
- Update to 1.6.0 release

* Fri Jun  7 2013 Dan Williams <dcbw@redhat.com> - 1.4.0-1
- Update to 1.4.0 release

* Fri May 10 2013 Dan Williams <dcbw@redhat.com> - 1.3.0-1.git20130510
- Initial Fedora release

