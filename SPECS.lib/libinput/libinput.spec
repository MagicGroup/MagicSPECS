Name:           libinput
Version: 1.0.1
Release:        2%{?dist}
Summary:        Input device library
Summary(zh_CN.UTF-8): 输入设备库

License:        MIT
URL:            http://www.freedesktop.org/wiki/Software/libinput/
Source0:        http://www.freedesktop.org/software/libinput/libinput-%{version}.tar.xz

BuildRequires:  libevdev-devel
BuildRequires:  libudev-devel
BuildRequires:  mtdev-devel

%description
libinput is a library that handles input devices for display servers and other
applications that need to directly deal with input devices.

It provides device detection, device handling, input device event processing
and abstraction so minimize the amount of custom input code the user of
libinput need to provide the common set of functionality that users expect.

%description -l zh_CN.UTF-8
输入设备库。

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
%configure --disable-static
make %{?_smp_mflags}
magic_rpm_clean.sh

%install
%make_install
find $RPM_BUILD_ROOT -name '*.la' -delete


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc COPYING
%{_libdir}/libinput.so.*
%{_bindir}/libinput-debug-events
%{_bindir}/libinput-list-devices
%{_libdir}/udev/*
%{_mandir}/man1/libinput-*.1*

%files devel
%{_includedir}/libinput.h
%{_libdir}/libinput.so
%{_libdir}/pkgconfig/libinput.pc


%changelog
* Sun Sep 06 2015 Liu Di <liudidi@gmail.com> - 1.0.1-2
- 更新到 1.0.1

* Fri Jul 18 2014 Liu Di <liudidi@gmail.com> - 0.4.0-2
- 为 Magic 3.0 重建

* Thu Jul 17 2014 Liu Di <liudidi@gmail.com> - 0.4.0-1
- 更新到 0.4.0

* Fri Feb 28 2014 Kalev Lember <kalevlember@gmail.com> - 0.1.0-1
- Initial Fedora packaging
