Name:		xcb-util-renderutil
Version:	0.3.9
Release:	1%{?dist}
Summary:	Convenience functions for the Render extension
Summary(zh_CN.UTF-8): 基于 libxcb 的 Render 扩展
Group:		System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:	MIT
URL:		http://xcb.freedesktop.org
Source0:	http://xcb.freedesktop.org/dist/%{name}-%{version}.tar.bz2
BuildRequires:	pkgconfig(xcb-util) >= 0.3.8
BuildRequires:	m4

%description
XCB util-renderutil module provides the following library:

  - renderutil: Convenience functions for the Render extension.
%description -l zh_CN.UTF-8
基于 libxcb 的 Render 扩展。

%package 	devel
Summary:	Development and header files for xcb-util-renderutil
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:		System Environment/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description	devel
Development files for xcb-util-renderutil.
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
* Thu Oct 22 2015 Liu Di <liudidi@gmail.com> - 0.3.9-1
- 更新到 0.3.9

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu May 17 2012 Thomas Moschny <thomas.moschny@gmx.de> - 0.3.8-1
- New package.
