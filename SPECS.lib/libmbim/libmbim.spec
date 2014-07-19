
%global realversion 1.6.0
%global _hardened_build 1

Name: libmbim
Summary: Support library for the Mobile Broadband Interface Model protocol
Summary(zh_CN.UTF-8): 移动宽带接口模型协议的支持库
Version: %{?realversion}
Release: 1%{?dist}
License: LGPLv2+
URL: http://freedesktop.org/software/libmbim

#
# Source from http://freedesktop.org/software/libmbim/
#
Source: http://freedesktop.org/software/libmbim/%{name}-%{realversion}.tar.xz

BuildRequires: glib2-devel
BuildRequires: pkgconfig
BuildRequires: automake autoconf intltool libtool
BuildRequires: python >= 2.7
BuildRequires: pkgconfig(gudev-1.0) >= 147


%description
This package contains the libraries that make it easier to use MBIM
functionality from applications that use glib.

%description -l zh_CN.UTF-8
移动宽带接口模型协议的支持库。

%package devel
Summary: Header files for adding MBIM support to applications that use glib
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: glib2-devel%{?_isa}

%description devel
This package contains the header and pkg-config files for developing
applications using MBIM functionality from applications that use glib.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package utils
Summary: Utilities to use the MBIM protocol from the command line
Summary(zh_CN.UTF-8): %{name} 的命令行工具
Requires: %{name}%{?_isa} = %{version}-%{release}
License: GPLv2+

%description utils
This package contains the utilities that make it easier to use MBIM
functionality from the command line.

%description utils -l zh_CN.UTF-8
%{name} 的命令行工具。

%prep
# NOTE: the documentation is pre-generated and shipped in the dist tarball;
# it is not build during the RPM build but the pre-generated docs are simply
# installed as-is.
%setup -q -n %{name}-%{realversion}

%build
%configure --disable-static
V=1 make %{?_smp_mflags}

%install
make install INSTALL="install -p" DESTDIR=$RPM_BUILD_ROOT
%{__rm} -f $RPM_BUILD_ROOT%{_libdir}/*.la

%check
make check


%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig


%files
%doc COPYING NEWS AUTHORS README
%{_libdir}/libmbim-glib.so.*
%{_mandir}/man1/*

%files devel
%{_includedir}/libmbim-glib/
%{_libdir}/pkgconfig/mbim-glib.pc
%{_libdir}/libmbim-glib.so
%{_datadir}/gtk-doc/

%files utils
%{_bindir}/mbimcli
%{_bindir}/mbim-network


%changelog
* Sat Feb  1 2014 poma <poma@gmail.com> - 1.6.0-1
- Update to 1.6.0 release

* Thu Aug 15 2013 Dan Williams <dcbw@redhat.com> - 1.5.0-1.20130815git
- Initial Fedora release

