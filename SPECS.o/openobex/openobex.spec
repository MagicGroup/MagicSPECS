Summary: Library for using OBEX
Summary(zh_CN.UTF-8): 使用OBEX的库
Name: openobex
Version: 1.5
Release: 3%{?dist}
License: LGPL
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL: http://openobex.sourceforge.net
Source: ftp://download.sourceforge.net/pub/sourceforge/openobex/openobex-%{version}.tar.gz
Patch: openobex-apps-flush.patch

BuildRoot: %{_tmppath}/%{name}-root
BuildRequires: autoconf >= 0:2.57, docbook-utils >= 0:0.6.13, bluez-libs-devel sed, libusb-devel
BuildRequires: automake autoconf libtool
ExcludeArch: s390 s390x

%description
Open OBEX shared c-library

%description -l zh_CN.UTF-8
Open OBEX 共享库

%package devel
Summary: Files for development of applications which will use OBEX
Summary(zh_CN.UTF-8): 使用OBEX开发应用程序需要的文件
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = 0:%{version}-%{release} bluez-libs-devel libusb-devel pkgconfig

%description devel
Open OBEX shared c-library

%description devel -l zh_CN.UTF-8
Open OBEX 开发包

%package apps
Summary: Applications for using OBEX
Summary(zh_CN.UTF-8): 使用OBEX的应用程序
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
BuildRequires: bluez-libs-devel
BuildRequires: autoconf >= 0:2.57
Excludearch: s390x s390

%description apps
Open OBEX Applications

%description apps -l zh_CN.UTF-8
Open OBEX 应用程序

%prep
rm -rf $RPM_BUILD_ROOT

%setup -q
%patch -p1

%build
autoreconf --install --force
%configure --disable-static --enable-apps --enable-usb
make
make -C doc 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
# we do not want .la files
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-, root, root)
%{_libdir}/libopenobex*.so.*

%files devel
%defattr(-, root, root)
%doc AUTHORS COPYING ChangeLog NEWS README 
%{_libdir}/libopenobex*.so
%dir %{_includedir}/openobex
%{_includedir}/openobex/*.h
%{_libdir}/pkgconfig/openobex.pc

%files apps
%defattr(-, root, root)
%doc AUTHORS COPYING ChangeLog NEWS README
%{_bindir}/irobex_palm3
%{_bindir}/irxfer
%{_bindir}/ircp
%{_bindir}/obex_tcp
%{_bindir}/obex_test


%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 1.5-3
- 为 Magic 3.0 重建

* Fri Jan 20 2012 Liu Di <liudidi@gmail.com> - 1.5-2
- 为 Magic 3.0 重建

* Mon Oct 09 2006 Liu Di <liudidi@gmail.com> - 1.3-1mgc
- rebuild
