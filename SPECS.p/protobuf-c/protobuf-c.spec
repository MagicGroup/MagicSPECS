Name:           protobuf-c
Version:        0.15
Release:        8%{?dist}
Summary:        C bindings for Google's Protocol Buffers

Group:          System Environment/Libraries
License:        ASL 2.0
URL:            http://code.google.com/p/protobuf-c/
Source0:        http://protobuf-c.googlecode.com/files/protobuf-c-%{version}.tar.gz
Source1:        http://protobuf-c.googlecode.com/svn/tags/%{version}/LICENSE

BuildRequires:  protobuf-devel

%description
Protocol Buffers are a way of encoding structured data in an efficient yet 
extensible format. This package provides a code generator and run-time
libraries to use Protocol Buffers from pure C (not C++).

It uses a modified version of protoc called protoc-c. 

%package devel
Summary:        Protocol Buffers C headers and libraries
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description devel
This package contains protobuf-c headers and libraries.

%prep
%setup -q
cp %{SOURCE1} .

%build
%configure --disable-static
# Causes build to fail
#make %{?_smp_mflags}
make

%check
make check

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT/%{_libdir}/libprotobuf-c.la

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_bindir}/protoc-c
%{_libdir}/libprotobuf-c.so.*
%doc TODO LICENSE ChangeLog

%files devel
%defattr(-,root,root,-)
%dir %{_includedir}/google
%{_includedir}/google/protobuf-c
%{_libdir}/libprotobuf-c.so
%{_libdir}/pkgconfig/libprotobuf-c.pc

%changelog
* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 11 2013 David Robinson <zxvdr.au@gmail.com> - 0.15-7
- rebuilt for protobuf-2.5.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jun 12 2011 David Robinson <zxvdr.au@gmail.com> - 0.15-3
- rebuilt for protobuf-2.4.1

* Sun Apr 24 2011 David Robinson <zxvdr.au@gmail.com> - 0.15-2
- Spec file cleanup

* Wed Apr 20 2011 David Robinson <zxvdr.au@gmail.com> - 0.15-1
- New upstream release
- Spec file cleanup

* Mon Jan 17 2011 Bobby Powers <bobby@laptop.org> - 0.14-1
- New upstream release
- Removed -devel dependency on protobuf-devel
- Small specfile cleanups

* Wed May 19 2010 David Robinson <zxvdr.au@gmail.com> - 0.13-2
- Spec file cleanup

* Wed May 19 2010 David Robinson <zxvdr.au@gmail.com> - 0.13-1
- Initial packaging
