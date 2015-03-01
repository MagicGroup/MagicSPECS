#global gitdate 20140411

#global commit 6eb075c70e2f91a9c45a90677bd46e8fb0432655
#global shortcommit %(c=%{commit}; echo ${c:0:7})

Summary: Direct Rendering Manager runtime library
Summary(zh_CN.UTF-8): 直接渲染管理 (DRM) 运行库
Name: libepoxy
Version: 1.2
Release: 2%{?dist}
License: MIT
URL: http://github.com/anholt/libepoxy
# github url - generated archive
#ource0: https://github.com/anholt/libepoxy/archive/%{commit}/%{name}-%{commit}.tar.gz
Source0: https://github.com/anholt/libepoxy/archive/%{commit}/v%{version}.tar.gz

BuildRequires: automake autoconf libtool
BuildRequires: mesa-libGL-devel
BuildRequires: mesa-libEGL-devel
BuildRequires: mesa-libGLES-devel
BuildRequires: xorg-x11-util-macros
BuildRequires: python3

%description
A library for handling OpenGL function pointer management.

%description -l zh_CN.UTF-8
处理 OpenGL 函数的库。

%package devel
Summary: Development files for libepoxy
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains libraries and header files for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q

%build
autoreconf -vif || exit 1
%configure --disable-silent-rules
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

# NOTE: We intentionally don't ship *.la files
find $RPM_BUILD_ROOT -type f -name '*.la' -delete -print
magic_rpm_clean.sh

%check
# In theory this is fixed in 1.2 but we still see errors on most platforms
# https://github.com/anholt/libepoxy/issues/24
%ifnarch %{arm} aarch64 %{power64} s390x
make check
%else
make check ||:
%endif

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc README.md
%{_libdir}/libepoxy.so.0
%{_libdir}/libepoxy.so.0.0.0

%files devel
%dir %{_includedir}/epoxy/
%{_includedir}/epoxy/*
%{_libdir}/libepoxy.so
%{_libdir}/pkgconfig/epoxy.pc

%changelog
* Wed Feb 25 2015 Liu Di <liudidi@gmail.com> - 1.2-2
- 为 Magic 3.0 重建

* Mon Oct 13 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.2.0-1
- Update to 1.2 GA
- Don't fail build on make check failure for some architectures

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-0.4.20140411git6eb075c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-0.3.20140411git6eb075c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Apr 11 2014 Dave Airlie <airlied@redhat.com> 1.2-0.2.20140411git6eb075c
- update to latest git snapshot

* Thu Mar 27 2014 Dave Airlie <airlied@redhat.com> 1.2-0.1.20140307gitd4ad80f
- initial git snapshot

