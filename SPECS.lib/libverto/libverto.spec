Name:           libverto
Version: 0.2.6
Release: 1%{?dist}
Summary:        Main loop abstraction library
Summary(zh_CN.UTF-8): 主循环抽象库

License:        MIT
URL:            https://fedorahosted.org/libverto/
Source0:        http://fedorahosted.org/releases/l/i/%{name}/%{name}-%{version}.tar.gz

BuildRequires:  glib2-devel
BuildRequires:  libev-devel
BuildRequires:  libevent-devel
BuildRequires:  libtevent-devel

%description
libverto provides a way for libraries to expose asynchronous interfaces
without having to choose a particular event loop, offloading this
decision to the end application which consumes the library.

If you are packaging an application, not library, based on libverto,
you should depend either on a specific implementation module or you
can depend on the virtual provides 'libverto-module-base'. This will
ensure that you have at least one module installed that provides io,
timeout and signal functionality. Currently glib is the only module
that does not provide these three because it lacks signal. However,
glib will support signal in the future.

%description -l zh_CN.UTF-8
主循环抽象库。

%package        devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package        glib
Summary:        glib module for %{name}
Summary(zh_CN.UTF-8): %{name} 的 glib 模块
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    glib
Module for %{name} which provides integration with glib.

This package does NOT yet provide %{name}-module-base.

%description glib -l zh_CN.UTF-8
%{name} 的 glib 模块。

%package        glib-devel
Summary:        Development files for %{name}-glib
Requires:       %{name}-glib%{?_isa} = %{version}-%{release}
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}

%description    glib-devel
The %{name}-glib-devel package contains libraries and header files for
developing applications that use %{name}-glib.

%package        libev
Summary:        libev module for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:       %{name}-module-base = %{version}-%{release}

%description    libev
Module for %{name} which provides integration with libev.

This package provides %{name}-module-base since it supports io, timeout
and signal.

%package        libev-devel
Summary:        Development files for %{name}-libev
Requires:       %{name}-libev%{?_isa} = %{version}-%{release}
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}

%description    libev-devel
The %{name}-libev-devel package contains libraries and header files for
developing applications that use %{name}-libev.

This package provides %{name}-module-base since it supports io, timeout
and signal.

%package        libevent
Summary:        libevent module for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:       %{name}-module-base = %{version}-%{release}

%description    libevent
Module for %{name} which provides integration with libevent.

%package        libevent-devel
Summary:        Development files for %{name}-libevent
Requires:       %{name}-libevent%{?_isa} = %{version}-%{release}
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}

%description    libevent-devel
The %{name}-libevent-devel package contains libraries and header files for
developing applications that use %{name}-libevent.

%package        tevent
Summary:        tevent module for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:       %{name}-module-base = %{version}-%{release}

%description    tevent
Module for %{name} which provides integration with tevent.

This package provides %{name}-module-base since it supports io, timeout
and signal.

%package        tevent-devel
Summary:        Development files for %{name}-tevent
Requires:       %{name}-tevent%{?_isa} = %{version}-%{release}
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}

%description    tevent-devel
The %{name}-tevent-devel package contains libraries and header files for
developing applications that use %{name}-tevent.

%prep
%setup -q

%build
%configure --disable-static --with-libev
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

magic_rpm_clean.sh

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post -n %{name}-glib -p /sbin/ldconfig
%postun -n %{name}-glib -p /sbin/ldconfig

%post -n %{name}-libev -p /sbin/ldconfig
%postun -n %{name}-libev -p /sbin/ldconfig

%post -n %{name}-libevent -p /sbin/ldconfig
%postun -n %{name}-libevent -p /sbin/ldconfig

%post -n %{name}-tevent -p /sbin/ldconfig
%postun -n %{name}-tevent -p /sbin/ldconfig


%files
%doc AUTHORS ChangeLog COPYING NEWS README
%{_libdir}/%{name}.so.*

%files devel
%{_includedir}/verto.h
%{_includedir}/verto-module.h
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

%files glib
%{_libdir}/%{name}-glib.so.*

%files glib-devel
%{_includedir}/verto-glib.h
%{_libdir}/%{name}-glib.so
%{_libdir}/pkgconfig/%{name}-glib.pc

%files libev
%{_libdir}/%{name}-libev.so.*

%files libev-devel
%{_includedir}/verto-libev.h
%{_libdir}/%{name}-libev.so
%{_libdir}/pkgconfig/%{name}-libev.pc

%files libevent
%{_libdir}/%{name}-libevent.so.*

%files libevent-devel
%{_includedir}/verto-libevent.h
%{_libdir}/%{name}-libevent.so
%{_libdir}/pkgconfig/%{name}-libevent.pc

%files tevent
%{_libdir}/%{name}-tevent.so.*

%files tevent-devel
%{_includedir}/verto-tevent.h
%{_libdir}/%{name}-tevent.so
%{_libdir}/pkgconfig/%{name}-tevent.pc

%changelog
* Wed Aug 06 2014 Liu Di <liudidi@gmail.com> - 0.2.6-1
- 更新到 0.2.6

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.2.4-3
- 为 Magic 3.0 重建

* Mon Feb 13 2012 Nathaniel McCallum <npmccallum@redhat.com> - 0.2.4-2
- Added libverto-0.2.4-fix-libev.patch

* Thu Feb 09 2012 Nathaniel McCallum <npmccallum@redhat.com> - 0.2.4-1
- Update to 0.2.4 release

* Wed Feb 08 2012 Nathaniel McCallum <npmccallum@redhat.com> - 0.2.3-1
- Update to 0.2.3 release

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 11 2011 Nathaniel McCallum <npmccallum@redhat.com> - 0.2.2-1
- Update to 0.2.2 release
- Add ChangeLog documentation

* Fri Nov 11 2011 Nathaniel McCallum <npmccallum@redhat.com> - 0.2.1-2
- Fix Requires to have proper ISA dependencies

* Thu Nov 10 2011 Nathaniel McCallum <npmccallum@redhat.com> - 0.2.1-1
- Update to 0.2.1

* Mon Aug 15 2011 Nathaniel McCallum <npmccallum@redhat.com> - 0.1-1
- Initial release

