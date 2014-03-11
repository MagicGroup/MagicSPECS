Name:           libestr
Version:        0.1.3 
Release:        3%{?dist}
Summary:        String handling essentials library

License:        LGPLv2+
URL:            http://libestr.adiscon.com/
Source0:        http://libestr.adiscon.com/files/download/libestr-%{version}.tar.gz
Patch0:        libestr-0.1.3-broken-configure-script.patch

%description
This package compiles the string handling essentials library
used by the Rsyslog daemon.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The package contains libraries and header files for
developing applications that use libestr.

%prep
%setup -q
%patch0 -p1 -b broken-configure-script.patch

%build
%configure --disable-static --with-pic
V=1 make %{?_smp_mflags}

%install
make install INSTALL="install -p" DESTDIR=%{buildroot}
rm -f %{buildroot}/%{_libdir}/*.{a,la}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc README COPYING AUTHORS ChangeLog
%{_libdir}/lib*.so.*

%files devel
%{_includedir}/libestr.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/libestr.pc

%changelog
* Thu Sep 20 2012 mdarade <mdarade@redhat.com> - 0.1.3-3
- Fixed broken configure script

* Mon Aug 27 2012 mdarade <mdarade@redhat.com> - 0.1.3-2
- Removed unnecessary macros in spec file.


* Wed Aug 7 2012 Mahaveer Darade <mdarade@redhat.com> - 0.1.3-1
- Initial port libestr-0.1.3
