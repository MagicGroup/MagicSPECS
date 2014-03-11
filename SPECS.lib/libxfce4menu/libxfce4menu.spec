Summary: 	freedesktop.org compliant menu implementation for Xfce
Summary(zh_CN):	和 freedesktop.org 兼容的 Xfce 菜单
Name: 		libxfce4menu
Version: 	4.6.2
Release: 	2%{?dist}
License:	LGPL
URL: 		http://www.xfce.org/
Source0: 	http://archive.xfce.org/src/xfce/libxfce4menu/4.6/%{name}-%{version}.tar.bz2
Group: 		Development/Libraries
Group(zh_CN):	开发/库
BuildRoot: 	%{_tmppath}/%{name}-root
Requires:	libxfce4util >= 4.5.90
BuildRequires: 	libxfce4util-devel >= 4.5.90
BuildRequires: 	gtk-doc

%description
multi-channel settings management support for xfce.

%description -l zh_CN
xfce的多通道设置管理支持.

%package devel
Summary:	developpment tools for libxfce4mcs library
Summary(zh_CN):	libxfce4mcs库的开发工具
Group:		Development/Libraries
Group(zh_CN):   开发/库
Requires:	%{name} = %{version}-%{release}

%description devel
Static libraries and header files for the libxfce4mcs library.

%description devel -l zh_CN
libxfce4mcs库的静态库和头文件。

%prep
%setup -q

%build
%configure --disable-gtk-doc
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT mandir=%{_mandir}
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/lib*.so.*

%files devel
%defattr(-, root, root)
%{_libdir}/lib*.so
%{_libdir}/*a
%{_libdir}/pkgconfig/*.pc
%{_includedir}/xfce4/libxfce4menu-0.1
%{_datadir}/gtk-doc
%{_datadir}/locale/*

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 4.6.2-2
- 为 Magic 3.0 重建

* Wed Oct 08 2008 Liu Di <liudidi@gmail.com> - 4.5.90-1mgc
- 首次打包
