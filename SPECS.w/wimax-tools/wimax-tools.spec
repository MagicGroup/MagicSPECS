Name: wimax-tools
Version: 1.4.5
Release: 3%{?dist}
License: BSD
Group: System Environment/Base
Summary: Low level user space tools for the Linux WiMAX stack
URL: http://linuxwimax.org/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n) 
# Source: git://people.freedesktop.org/~dcbw/wimax-tools
Source: wimax-tools-%{version}.tar.gz
BuildRequires: libnl3-devel glib2-devel
ExcludeArch: s390 s390x

%description
Tools for diagnosing and testing WiMAX connectivity.

%package libs
Group: System Environment/Libraries
Summary: Runtime libraries for WiMAX support
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description libs
Runtime libraries for the WiMAX low level tools.
Other applications use these libraries to gain access to the WiMAX kernel stack.

%package devel
Group: Development/Libraries
Summary: Development files for libwimax
Requires: wimax-tools-libs = %{version}-%{release}
Requires: pkgconfig

%description devel
This package provides the header files and libraries needed to compile
programs that will use the runtime libraries provided by the WiMAX low
level tools.

%prep
%setup -q

%build
%configure --disable-doxygen-doc
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
find $RPM_BUILD_ROOT -name "*.la" -exec rm {} \;
find $RPM_BUILD_ROOT -name "*.a" -exec rm {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README ChangeLog INSTALL LICENSE
%{_bindir}/*
%{_libdir}/wimax-tools

%files libs
%defattr(-,root,root,-)
%{_libdir}/lib*.so.0*

%files devel
%defattr(-,root,root,-)
%{_includedir}/wimaxll/*
%{_includedir}/wimaxll.h
%{_includedir}/wimaxll-version.h
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 1.4.5-3
- 为 Magic 3.0 重建

* Fri Mar  2 2012 Dan Williams <dcbw@redhat.com> - 1.4.5-2
- Rebuild against libnl3

* Tue Jan 10 2012 Dan Williams <dcbw@redhat.com> - 1.4.5-1
- Update to 1.4.5
- Allow building against libnl3 (not enabled yet)

* Tue Mar 22 2011 Bill Nottingham <notting@redhat.com> 1.4.4-1
- Initial packaging, based on upstream spec
