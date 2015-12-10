Name:		xcb-util-keysyms
Version:	0.4.0
Release:	3%{?dist}
Summary:	Standard X key constants and keycodes conversion on top of libxcb
Summary(zh_CN.UTF-8): 基于 libxcb 的标准 X 键盘常量和键盘码转换
Group:		System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:	MIT
URL:		http://xcb.freedesktop.org
Source0:	http://xcb.freedesktop.org/dist/%{name}-%{version}.tar.bz2
BuildRequires:	pkgconfig(xcb-util) >= 0.3.8
BuildRequires:	m4

%description
XCB util-keysyms module provides the following library:

  - keysyms: Standard X key constants and conversion to/from keycodes.

%description -l zh_CN.UTF-8
基于 libxcb 的标准 X 键盘常量和键盘码转换。

%package 	devel
Summary:	Development and header files for xcb-util-keysyms
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:		System Environment/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description	devel
Development files for xcb-util-keysyms.
%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q


%build
%configure --with-pic --disable-static
make %{?_smp_mflags}


%check
make check


%install
make install DESTDIR=%{buildroot} INSTALL="install -p"
rm %{buildroot}%{_libdir}/*.la
magic_rpm_clean.sh

%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%doc README
%{_libdir}/*.so.*


%files devel
%doc NEWS
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so
%{_includedir}/xcb/*.h


%changelog
* Sat Nov 14 2015 Liu Di <liudidi@gmail.com> - 0.4.0-3
- 为 Magic 3.0 重建

* Fri Nov 06 2015 Liu Di <liudidi@gmail.com> - 0.4.0-2
- 为 Magic 3.0 重建

* Thu Oct 22 2015 Liu Di <liudidi@gmail.com> - 0.4.0-1
- 更新到 0.4.0

* Mon Aug 20 2012 Thomas Moschny <thomas.moschny@gmx.de> - 0.3.9-1
- Update to 0.3.9.

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Apr  6 2012 Thomas Moschny <thomas.moschny@gmx.de> - 0.3.8-3
- Fix explicit requires.

* Tue Mar 13 2012 Thomas Moschny <thomas.moschny@gmx.de> - 0.3.8-2
- Specfile cleanups suggested in the review.

* Mon Dec  5 2011 Thomas Moschny <thomas.moschny@gmx.de> - 0.3.8-1
- New package.

