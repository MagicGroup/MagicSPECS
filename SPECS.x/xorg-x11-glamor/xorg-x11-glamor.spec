%global checkout 20130401git81aadb8

Summary: X.org glamor library
Name: xorg-x11-glamor
Version: 0.5.0
Release: 5.%{checkout}%{?dist}
License: MIT
Group: System Environment/Libraries
URL: http://www.freedesktop.org/wiki/Software/Glamor


# source tarball has to be created from git using make-git-snapshot.sh
# if checkout value is 20130401git81aadb8 then create the tar with :
# ./make-git-snapshot.sh 81aadb8
# http://cgit.freedesktop.org/xorg/driver/glamor/
Source0: %{name}-%{checkout}.tar.xz
Source1: make-git-snapshot.sh

Requires: xorg-x11-server-Xorg
BuildRequires: pkgconfig autoconf automake libtool
BuildRequires: xorg-x11-server-devel
BuildRequires: mesa-libgbm-devel mesa-libEGL-devel

%description
glamor provides xorg-x11 acceleration using the OpenGL driver.

%package devel
Summary: X.org glamor renderer development package
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
X.org glamor development package

%prep
%setup -q -n %{name}-%{checkout}

%build
autoreconf --install
%configure --disable-static
make %{?_smp_mflags}

%install
# core libs and headers, but not drivers.
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name '*.la' -delete

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc README
%doc COPYING
%{_libdir}/libglamor.so.0
%{_libdir}/libglamor.so.0.0.0
%{_libdir}/xorg/modules/libglamoregl.so
%{_datadir}/X11/xorg.conf.d/glamor.conf

%files devel
%dir %{_includedir}/xorg
%{_includedir}/xorg/glamor.h
%{_libdir}/pkgconfig/glamor.pc
%{_libdir}/pkgconfig/glamor-egl.pc
%{_libdir}/libglamor.so


%changelog
* Thu Apr 11 2013 Dave Airlie <airlied@redhat.com> 0.5.0-5.20130401git81aadb8
- enable TLS, mesa builds with TLS enabled are also processing.

* Fri Apr 05 2013 Jerome Glisse <jglisse@redhat.com> 0.5.0-4.20130401git81aadb8
- Fix directory ownership.

* Thu Apr 04 2013 Jerome Glisse <jglisse@redhat.com> 0.5.0-3.20130401git81aadb8
- Remove comment rather than investigating Xorg mess as running ldconfig can't be harmfull.
- Fix devel package dependency.

* Wed Apr 03 2013 Jerome Glisse <jglisse@redhat.com> 0.5.0-2.20130401git81aadb8
- Silence rpmlint warning about ldconfig
- Only install libglamor.so in devel package.
- Adding COPYING and README as doc

* Thu Mar 28 2013 Jerome Glisse <jglisse@redhat.com> 0.5.0-1.20130401git81aadb8
- Initial package
