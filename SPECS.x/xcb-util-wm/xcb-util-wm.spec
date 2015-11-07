Name:		xcb-util-wm
Version:	0.4.1
Release:	5%{?dist}
Summary:	Client and window-manager helper library on top of libxcb
Summary(zh_CN.UTF-8): 基于 libxcb 的客户端和窗口管理器辅助库
Group:		System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:	MIT
URL:		http://xcb.freedesktop.org
Source0:	http://xcb.freedesktop.org/dist/%{name}-%{version}.tar.bz2
BuildRequires:	pkgconfig(xcb-util) >= 0.3.8
BuildRequires:	m4

%description
XCB util-wm module provides the following libraries:

  - ewmh: Both client and window-manager helpers for EWMH.
  - icccm: Both client and window-manager helpers for ICCCM.
%description -l zh_CN.UTF-8
基于 libxcb 的客户端和窗口管理器辅助库，支持 EWMH, ICCCM。

%package 	devel
Summary:	Development and header files for xcb-util-vm
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:		System Environment/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description	devel
Development files for xcb-util-wm.
%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q


%build
%configure --with-pic --disable-static --disable-silent-rules
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
* Fri Nov 06 2015 Liu Di <liudidi@gmail.com> - 0.4.1-5
- 为 Magic 3.0 重建

* Thu Oct 22 2015 Liu Di <liudidi@gmail.com> - 0.4.1-4
- 为 Magic 3.0 重建

* Sun May 04 2014 Liu Di <liudidi@gmail.com> - 0.4.1-3
- 为 Magic 3.0 重建

* Thu Apr 17 2014 Thomas Moschny <thomas.moschny@gmx.de> - 0.4.1-2
- Disable silent build.

* Wed Apr 16 2014 Hans de Goede <hdegoede@redhat.com> - 0.4.1-1
- Update to 0.4.1 (rhbz#1059674)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Aug 20 2012 Thomas Moschny <thomas.moschny@gmx.de> - 0.3.9-1
- Update to 0.3.9.

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Apr  5 2012 Thomas Moschny <thomas.moschny@gmx.de> - 0.3.8-2
- Specfile cleanups as suggested in the review.
- Remove unneeded BR on pkgconfig.
- Remove unneeded chrpath call.

* Mon Dec  5 2011 Thomas Moschny <thomas.moschny@gmx.de> - 0.3.8-1
- New package.

