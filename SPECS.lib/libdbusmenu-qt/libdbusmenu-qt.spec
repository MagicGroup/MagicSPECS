Summary: A Qt implementation of the DBusMenu protocol
Summary(zh_CN.UTF-8): DBusMenu 协议的 Qt 实现
Name: libdbusmenu-qt
Version: 0.8.3
Release: 4%{?dist}
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License: LGPLv2+
URL: http://people.canonical.com/~agateau/dbusmenu/
Source0: http://people.canonical.com/~agateau/dbusmenu/%{name}-%{version}.tar.bz2    
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

## upstream patches
# honor LIB_SUFFIX (ie, use /usr/lib64 on 64bit)
Patch100: dbusmenu-qt-0.3.2-pkgconfig.patch

BuildRequires: cmake
BuildRequires: pkgconfig
BuildRequires: qjson-devel
BuildRequires: qt4-devel

Provides: dbusmenu-qt = %{version}-%{release}

%description
This library provides a Qt implementation of the DBusMenu protocol.
The DBusMenu protocol makes it possible for applications to export and import
their menus over DBus.

%description -l zh_CN.UTF-8
DBusMenu 协议的 Qt 实现。DBusMenu 协议可让应用程序通过 DBus 导出和导入菜单。

%package devel
Summary: Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发文件
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Provides: dbusmenu-qt-devel = %{version}-%{release}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
%{summary}.

%description devel -l zh_CN.UTF-8
%{name} 的开发文件。

%prep
%setup -q

%patch100 -p1 -b .pkgconfig

%build
mkdir build
cd build
%cmake .. 

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
cd build
make install/fast DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot} 

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING README
%{_libdir}/libdbusmenu-qt.so.2*

%files devel
%defattr(-,root,root,-)
%{_includedir}/dbusmenu-qt/
%{_libdir}/libdbusmenu-qt.so
%{_libdir}/pkgconfig/dbusmenu-qt.pc
%{_docdir}/*

%changelog
* Mon Jul 14 2014 Liu Di <liudidi@gmail.com> - 0.8.3-4
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.8.3-3
- 为 Magic 3.0 重建

* Thu Jan 05 2012 Liu Di <liudidi@gmail.com> - 0.8.3-2
- 为 Magic 3.0 重建

* Fri May 21 2010 Rex Dieter <rdieter@fedoraproject.org> 0.3.3-1
- dbusmenu-qt-0.3.3

* Sun Apr 25 2010 Rex Dieter <rdieter@fedoraproject.org> 0.3.2-2
- pkg rename s/libdbusmenu-qt/dbusmenu-qt/
- Provides: libdbusmenu-qt(-devel)

* Sun Apr 25 2010 Rex Dieter <rdieter@fedoraproject.org> 0.3.2-1
- dbusmenu-qt-0.3.2
