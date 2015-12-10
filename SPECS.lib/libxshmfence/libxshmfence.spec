Name:           libxshmfence
Version:        1.2
Release:        5%{?dist}
Summary:        X11 shared memory fences
Summary(zh_CN.UTF-8): X11 共享内存库

License:        MIT
URL:            http://www.x.org/
Source0:        http://xorg.freedesktop.org/archive/individual/lib/%{name}-%{version}.tar.bz2

# upstream tarball has broken libtool because libtool is never not broken
BuildRequires:  autoconf automake libtool xorg-x11-util-macros
BuildRequires:  pkgconfig(xproto)
#Requires:       

%description
Shared memory fences for X11, as used in DRI3.

%description -l zh_CN.UTF-8
X11 共享内存库。

%package        devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q

%build
autoreconf -v -i -f
%configure --disable-static
make %{?_smp_mflags}

%install
%make_install
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
magic_rpm_clean.sh

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc
%{_libdir}/libxshmfence.so.1*

%files devel
%doc
%{_includedir}/*
%{_libdir}/pkgconfig/xshmfence.pc
%{_libdir}/*.so

%changelog
* Tue Nov 10 2015 Liu Di <liudidi@gmail.com> - 1.2-5
- 为 Magic 3.0 重建

* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 1.2-4
- 为 Magic 3.0 重建

* Mon Sep 07 2015 Liu Di <liudidi@gmail.com> - 1.2-3
- 为 Magic 3.0 重建

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jan 02 2015 Adel Gadllah <adel.gadllah@gmail.com> - 1.2-1
- Update to 1.2

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Dec 12 2013 Adam Jackson <ajax@redhat.com> 1.1-1
- xshmfence 1.1

* Wed Nov 06 2013 Adam Jackson <ajax@redhat.com> 1.0-1
- Initial packaging

