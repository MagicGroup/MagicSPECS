Name:		keybinder3
Version:	0.3.0
Release:	5%{?dist}
Summary:	A library for registering global keyboard shortcuts
Summary(zh_CN.UTF-8): 注册全局键盘快捷方式的库
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
License:	MIT
URL:		https://github.com/engla/keybinder/tree/keybinder-3.0
Source0:	https://github.com/engla/keybinder/archive/keybinder-3.0-v%{version}.tar.gz

BuildRequires:	gtk3-devel, gnome-common, gtk-doc, gobject-introspection-devel

%description
Keybinder is a library for registering global keyboard shortcuts. 
Keybinder works with GTK-based applications using the X Window System.

The library contains:
- A C library, libkeybinder
- Gobject-Introspection bindings

%description -l zh_CN.UTF-8
注册全局键盘快捷方式的库。

%package devel
Summary: Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name}%{?_isa} = %{version}-%{release}
%description devel
This package contains the development files for %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package doc
Summary: Documentation for %{name}
Summary(zh_CN.UTF-8): %{name} 的文档
Group: Documentation
Group(zh_CN.UTF-8): 文档
BuildArch: noarch
Requires: %{name} = %{version}-%{release}
Requires: devhelp
%description doc
This package contains documentation for %{name}.

%description doc -l zh_CN.UTF-8
%{name} 的文档。

%prep
%setup -qn keybinder-keybinder-3.0-v%{version}

%build
./autogen.sh
%configure --prefix=/usr --libdir=%{_libdir} --enable-shared --enable-gtk-doc
make %{?_smp_mflags} V=1

%install
make install DESTDIR=%{buildroot}

rm -rf %{buildroot}/%{_libdir}/libkeybinder-3.0.la
magic_rpm_clean.sh

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc NEWS AUTHORS README COPYING
%{_libdir}/libkeybinder-3.0.so.*
%{_libdir}/girepository-1.0/Keybinder-3.0.typelib

%files devel
%dir %{_includedir}/keybinder-3.0/
%{_includedir}/keybinder-3.0/keybinder.h
%{_libdir}/pkgconfig/keybinder-3.0.pc
%{_libdir}/libkeybinder-3.0.so
%{_datadir}/gir-1.0/Keybinder-3.0.gir

%files doc
%dir %{_datadir}/gtk-doc/html/keybinder-3.0/
%{_datadir}/gtk-doc/html/keybinder-3.0/*

%changelog
* Sun Feb 15 2015 Liu Di <liudidi@gmail.com> - 0.3.0-5
- 为 Magic 3.0 重建

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 0.3.0-3
- Rebuilt for gobject-introspection 1.41.4

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Aug 1 2013 TingPing <tingping@tingping.se> - 0.3.0-1
- Initial Package

