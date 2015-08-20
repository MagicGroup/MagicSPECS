Name:           protobuf-c
Version:        1.1.1
Release:        3%{?dist}
Summary:        C bindings for Google's Protocol Buffers
Summary(zh_CN.UTF-8): 谷歌 Protocol Buffers 的 C 绑定

Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        BSD
URL:            https://github.com/protobuf-c/protobuf-c
Source0:	https://github.com/protobuf-c/protobuf-c/releases/download/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  autoconf automake libtool protobuf-devel

%description
Protocol Buffers are a way of encoding structured data in an efficient yet 
extensible format. This package provides a code generator and run-time
libraries to use Protocol Buffers from pure C (not C++).

It uses a modified version of protoc called protoc-c. 

%description -l zh_CN.UTF-8
谷歌 Protocol Buffers 的 C 绑定。

%package devel
Summary:        Protocol Buffers C headers and libraries
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name} = %{version}-%{release}

%description devel
This package contains protobuf-c headers and libraries.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q

%build
autoreconf -ifv
%configure --disable-static
make %{?_smp_mflags}

%check
make check

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT/%{_libdir}/libprotobuf-c.la
magic_rpm_clean.sh

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
%{_includedir}/protobuf-c
%{_includedir}/google/protobuf-c
%{_libdir}/libprotobuf-c.so
%{_libdir}/pkgconfig/libprotobuf-c.pc

%changelog
* Fri Aug 07 2015 Liu Di <liudidi@gmail.com> - 1.1.1-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Apr 23 2015 Nikos Mavrogiannopoulos <nmav@redhat.com> - 1.1.1-1
- new upstream release (#1142988)

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 1.0.1-3
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Aug 06 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 1.0.1-1
- new upstream release

* Mon Aug 04 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 1.0.0-1
- new upstream release (#1126116)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

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
