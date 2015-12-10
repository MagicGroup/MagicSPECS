Name: libndp
Version: 1.5
Release: 3%{?dist}
Summary: Library for Neighbor Discovery Protocol
Summary(zh_CN.UTF-8): 邻居发现协议的库
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License: LGPLv2+
URL: http://www.libndp.org/
Source: http://www.libndp.org/files/libndp-%{version}.tar.gz

%description
This package contains a library which provides a wrapper
for IPv6 Neighbor Discovery Protocol.  It also provides a tool
named ndptool for sending and receiving NDP messages.

%description -l zh_CN.UTF-8
IPv6 邻居发现协议的库。

%package devel
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Summary: Libraries and header files for libndp development
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires: libndp = %{version}-%{release}

%description devel
The libndp-devel package contains the header files and libraries
necessary for developing programs using libndp.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q

%build
%configure --disable-static
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name \*.la -delete
magic_rpm_clean.sh

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc COPYING
%{_libdir}/*so.*
%{_bindir}/ndptool
%{_mandir}/man8/ndptool.8*

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Mon Nov 09 2015 Liu Di <liudidi@gmail.com> - 1.5-3
- 为 Magic 3.0 重建

* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 1.5-2
- 更新到 1.5

* Tue Jul 22 2014 Liu Di <liudidi@gmail.com> - 1.3-1
- 更新到 1.3

* Tue Oct 15 2013 Jiri Pirko <jpirko@redhat.com> - 1.2-1
- Update to 1.2
- libndp: silently ignore packets with optlen 0
- libndp: fix processing for larger options
- libndp: do not fail on receiving non-ndp packets

* Fri Oct 04 2013 Jiri Pirko <jpirko@redhat.com> - 1.1-1
- Update to 1.1

* Fri Sep 13 2013 Dan Williams <dcbw@redhat.com> - 1.0-2
- Fix .pc file includes path
- Fix ndptool -v argument

* Thu Aug 08 2013 Jiri Pirko <jpirko@redhat.com> - 1.0-1
- Update to 1.0

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-4.20130723git873037a
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 24 2013 Dan Williams <dcbw@redhat.com> - 0.1-3.20130723git873037a
- Update to git 873037a

* Fri Jun 07 2013 Jiri Pirko <jpirko@redhat.com> - 0.1-2.20130607git39e1f53
- Update to git 39e1f53

* Sat May 04 2013 Jiri Pirko <jpirko@redhat.com> - 0.1-1.20130504gitca3c399
- Initial build.
