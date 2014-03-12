Name:           libevdev
Version:        1.0
Release:        1%{?dist}
Summary:        Kernel Evdev Device Wrapper Library

Group:          System Environment/Libraries
License:        MIT
URL:            http://www.freedesktop.org/wiki/Software/libevdev
Source0:        http://www.freedesktop.org/software/%{name}/%{name}-%{version}.tar.xz

BuildRequires:  automake libtool
BuildRequires:  python

%description
%{name} is a library to wrap kernel evdev devices and provide a proper API
to interact with those devices.

%package devel
Summary:        Kernel Evdev Device Wrapper Library Development Package
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Kernel Evdev Device Wrapper Library Development Package.

%prep
%setup -q -n %{name}-%{version}

%build
autoreconf --force -v --install || exit 1
%configure --disable-static --disable-silent-rules --disable-gcov
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

# We intentionally don't ship *.la files
rm -f %{buildroot}%{_libdir}/*.la

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc COPYING 
%{_libdir}/libevdev.so.*

%files devel
%dir %{_includedir}/libevdev-1.0/
%dir %{_includedir}/libevdev-1.0/libevdev
%{_includedir}/libevdev-1.0/libevdev/libevdev.h
%{_includedir}/libevdev-1.0/libevdev/libevdev-uinput.h
%{_libdir}/libevdev.so
%{_libdir}/pkgconfig/libevdev.pc
%{_mandir}/man3/libevdev.3*

%changelog
* Tue Feb 18 2014 Peter Hutterer <peter.hutterer@redhat.com> 1.0-1
- libevdev 1.0

* Wed Feb 05 2014 Peter Hutterer <peter.hutterer@redhat.com> 0.9.1-1
- libevdev 1.0RC1

* Fri Jan 03 2014 Peter Hutterer <peter.hutterer@redhat.com> 0.6-3
- Restore deprecated constants LIBEVDEV_READ_* dropped from 0.6 (#1046426)

* Thu Dec 26 2013 Adam Williamson <awilliam@redhat.com> 0.6-2
- revert catastrophic upstream dropping of 'deprecated' functions - #1046426

* Mon Dec 23 2013 Peter Hutterer <peter.hutterer@redhat.com> 0.6-1
- libevdev 0.6

* Fri Nov 22 2013 Peter Hutterer <peter.hutterer@redhat.com> 0.5-1
- libevdev 0.5

* Fri Nov 01 2013 Peter Hutterer <peter.hutterer@redhat.com> 0.4.1-1
- libevdev 0.4.1

* Wed Oct 02 2013 Peter Hutterer <peter.hutterer@redhat.com> 0.4-2
- disable gcov (#1012180)
- disable unittests, we don't run them anyway

* Wed Sep 18 2013 Peter Hutterer <peter.hutterer@redhat.com> 0.4-1
- libevdev 0.4

* Tue Aug 13 2013 Peter Hutterer <peter.hutterer@redhat.com> 0.3-1
- libevdev 0.3

* Thu Jul 25 2013 Peter Hutterer <peter.hutterer@redhat.com> 0.2.1-1
- Initial package (#987204)

