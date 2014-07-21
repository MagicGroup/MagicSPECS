Name:          libusbmuxd
Version:       1.0.9
Release:       2%{?dist}
Summary:       Client library USB multiplex daemon for Apple's iOS devices

Group:         System Environment/Libraries
License:       LGPLv2+
URL:           http://www.libimobiledevice.org/
Source0:       http://www.libimobiledevice.org/downloads/%{name}-%{version}.tar.bz2

BuildRequires: libplist-devel >= 1.11

%description
libusbmuxd is the client library used for communicating with Apple's iPod Touch,
iPhone, iPad and Apple TV devices. It allows multiple services on the device 
to be accessed simultaneously.

%package utils
Summary: Utilities for communicating with Apple's iOS devices
Group: Applications/System
License: GPLv2+
Requires: %{name}%{?_isa} = %{version}-%{release}

%description utils
Utilities for Apple's iOS devices

%package devel
Summary: Development package for %{name}
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Files for development with %{name}.

%prep
%setup -q

%build
%configure --disable-static

sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags} V=1

%install
make install DESTDIR=%{buildroot} INSTALL='install -p'

#Remove libtool archives.
find %{buildroot} -name '*.la' -exec rm -f {} ';'

%check
make check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
# License is covered in README, upstream notified about COPYING files
# will be fixed in next release
%doc README AUTHORS
%{_libdir}/libusbmuxd.so.2*

%files utils
%{_bindir}/iproxy

%files devel
%{_includedir}/usbmuxd*
%{_libdir}/pkgconfig/libusbmuxd.pc
%{_libdir}/libusbmuxd.so

%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Mar 22 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.9-1
- Initial package
