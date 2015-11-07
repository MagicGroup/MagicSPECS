Summary:        Library for accessing USB devices
Summary(zh_CN.UTF-8): 访问 USB 设备的库
Name:           libusbx
Version: 1.0.20
Release: 2%{?dist}
Source0:        http://downloads.sourceforge.net/libusb/libusb-%{version}.tar.bz2
License:        LGPLv2+
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL:            http://sourceforge.net/apps/mediawiki/libusbx/
BuildRequires:  doxygen
Provides:       libusb1 = %{version}-%{release}
Obsoletes:      libusb1 <= 1.0.9

%description
This package provides a way for applications to access USB devices.

Libusbx is a fork of the original libusb, which is a fully API and ABI
compatible drop in for the libusb-1.0.9 release. The libusbx fork was
started by most of the libusb-1.0 developers, after the original libusb
project did not produce a new release for over 18 months.

Note that this library is not compatible with the original libusb-0.1 series,
if you need libusb-0.1 compatibility install the libusb package.

%description -l zh_CN.UTF-8
访问 USB 设备的库。

%package        devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-devel-doc = %{version}-%{release}
Provides:       libusb1-devel = %{version}-%{release}
Obsoletes:      libusb1-devel <= 1.0.9

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package devel-doc
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发文档
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name}-devel = %{version}-%{release}
Provides:       libusb1-devel-doc = %{version}-%{release}
Obsoletes:      libusb1-devel-doc <= 1.0.9
BuildArch:      noarch

%description devel-doc
This package contains API documentation for %{name}.

%description devel-doc -l zh_CN.UTF-8
%{name} 的开发文档。

%prep
%setup -q -n libusb-%{version}

%build
%configure --disable-static --enable-examples-build
make %{?_smp_mflags}
pushd doc
make docs
popd


%install
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/*.la
magic_rpm_clean.sh

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%doc AUTHORS COPYING README NEWS
%{_libdir}/*.so.*

%files devel
%{_includedir}/libusb-1.0
%{_libdir}/*.so
%{_libdir}/pkgconfig/libusb-1.0.pc

%files devel-doc
%doc doc/html examples/*.c


%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 1.0.20-2
- 更新到 1.0.20

* Fri Aug 01 2014 Liu Di <liudidi@gmail.com> - 1.0.19-1
- 更新到 1.0.19

* Wed Sep 26 2012 Hans de Goede <hdegoede@redhat.com> - 1.0.14-1
- Upgrade to 1.0.14

* Mon Sep 24 2012 Hans de Goede <hdegoede@redhat.com> - 1.0.13-1
- Upgrade to 1.0.13

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed May 23 2012 Hans de Goede <hdegoede@redhat.com> - 1.0.11-2
- Fix URL to actually point to libusbx
- Improve description to explain the relation between libusbx and libusb
- Build the examples (to test linking, they are not packaged)

* Tue May 22 2012 Hans de Goede <hdegoede@redhat.com> - 1.0.11-1
- New libusbx package, replacing libusb1
- Switching to libusbx upstream as that actually does releases (hurray)
- Drop all patches (all upstream)
- Drop -static subpackage (there are no packages using it)
