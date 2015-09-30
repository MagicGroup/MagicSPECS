Name:           sofia-sip
Version:        1.12.11
Release:        6%{?dist}
Summary:        Sofia SIP User-Agent library
Summary(zh_CN.UTF-8): Sofia SIP 用户代理库

Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        LGPLv2+
URL:            http://sofia-sip.sourceforge.net/
Source0:        http://dl.sourceforge.net/sofia-sip/%{name}-%{version}.tar.gz

#BuildRequires:  doxygen >= 1.3
#BuildRequires:  graphviz
BuildRequires:  openssl-devel >= 0.9.7
BuildRequires:  glib2-devel >=  2.4
BuildRequires:  lksctp-tools-devel

%description
Sofia SIP is a RFC-3261-compliant library for SIP user agents and
other network elements.  The Session Initiation Protocol (SIP) is an
application-layer control (signaling) protocol for creating,
modifying, and terminating sessions with one or more
participants. These sessions include Internet telephone calls,
multimedia distribution, and multimedia conferences.

%description -l zh_CN.UTF-8
Sofia SIP 用户代理库。

%package devel
Summary:        Sofia-SIP Development Package
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       sofia-sip = %{version}-%{release}
Requires:       pkgconfig

%description devel
Development package for Sofia SIP UA library.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package glib
Summary:        Glib bindings for Sofia-SIP 
Summary(zh_CN.UTF-8): %{name} 的 glibc 绑定
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Requires:       sofia-sip = %{version}-%{release}

%description glib
GLib interface to Sofia SIP User Agent library.

%description glib -l zh_CN.UTF-8
%{name} 的 glib 绑定。

%package glib-devel
Summary:        Glib bindings for Sofia SIP development files
Summary(zh_CN.UTF-8): %{name}-glib 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       sofia-sip-glib = %{version}-%{release}
Requires:       sofia-sip-devel = %{version}-%{release}
Requires:       pkgconfig

%description  glib-devel
Development package for Sofia SIP UA Glib library. This package
includes libraries and include files for developing glib programs
using Sofia SIP.
%description glib-devel -l zh_CN.UTF-8
%{name}-glib 的开发包。

%package utils
Summary:        Sofia-SIP Command Line Utilities
Summary(zh_CN.UTF-8): Sofia-SIP 命令行工具
Group:          Applications/Internet
Group(zh_CN.UTF-8): 应用程序/互联网
Requires:       sofia-sip = %{version}-%{release}

%description utils
Command line utilities for the Sofia SIP UA library.

%description utils -l zh_CN.UTF-8
Sofia-SIP 命令行工具。

%prep
%setup0 -q -n sofia-sip-%{version}%{?work:work%{work}}

%build
%configure --disable-rpath --disable-static
make %{?_smp_mflags}
#make doxygen

%check
#TPORT_DEBUG=9 TPORT_TEST_HOST=0.0.0.0 make check

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
find %{buildroot} -name \*.la -delete
find %{buildroot} -name \*.h.in -delete
find . -name installdox -delete
magic_rpm_clean.sh

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post glib -p /sbin/ldconfig
%postun glib -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog ChangeLog.ext-trees COPYING COPYRIGHTS
%doc README README.developers RELEASE TODO 
%{_libdir}/libsofia-sip-ua.so.*

%files devel
%defattr(-,root,root,-)
#%doc libsofia-sip-ua/docs/html
%dir %{_includedir}/sofia-sip-1.12
%dir %{_includedir}/sofia-sip-1.12/sofia-sip
%{_includedir}/sofia-sip-1.12/sofia-sip/*.h
%exclude %{_includedir}/sofia-sip-1.12/sofia-sip/su_source.h
%dir %{_includedir}/sofia-sip-1.12/sofia-resolv
%{_includedir}/sofia-sip-1.12/sofia-resolv/*.h
%{_libdir}/libsofia-sip-ua.so
%{_libdir}/pkgconfig/sofia-sip-ua.pc
%{_datadir}/sofia-sip

%files glib
%defattr(-,root,root,-)
%{_libdir}/libsofia-sip-ua-glib.so.*

%files glib-devel
%defattr(-,root,root,-)
#%doc libsofia-sip-ua-glib/docs/html
%{_includedir}/sofia-sip-1.12/sofia-sip/su_source.h
%{_libdir}/libsofia-sip-ua-glib.so
%{_libdir}/pkgconfig/sofia-sip-ua-glib.pc

%files utils
%defattr(-,root,root,-)
%{_bindir}/*
%{_mandir}/man1/*.1*

%changelog
* Mon Sep 28 2015 Liu Di <liudidi@gmail.com> - 1.12.11-6
- 为 Magic 3.0 重建

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 1.12.11-5
- 为 Magic 3.0 重建

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu May 24 2012 Brian Pepple <bpepple@fedoraproject.org> - 1.12.11-3
- Do not use enable-sctp option. (#817579)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Sep 27 2011 Brian Pepple <bpepple@fedoraproject.org> - 1.12.11-1
- Update to 1.12.11.
- Drop non-weak symbol patch. Fixed upstream.
- Drop buildroot and clean section. No longer necessary.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 1.12.10-5
- rebuilt with new openssl

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> - 1.12.10-2
- rebuild with new openssl

* Tue Dec  9 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.12.10-1
- Update to 1.12.10

* Sat Jun 14 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.12.9-1
- Update to 1.12.9
- Disable building API documentation because it won't build on PPC/PPC64 (at least in a reasonable amount of time).

* Mon Feb 11 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.12.8-1
- Update to 1.12.8

* Thu Dec 06 2007 Release Engineering <rel-eng at fedoraproject dot org> - 1.12.6-12
- Rebuild for deps

* Tue Aug 28 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.12.6-11
- Update license tag.

* Tue Jul 31 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.12.6-10
- Clean up

* Tue Jul 31 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.12.6-9
- Enable building on PPC64

* Tue Jul  3 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.12.6-8
- Disable checks for now, they all pass in local mock builds but fail when built with plague.

* Tue Jul  3 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.12.6-7
- Enable more debugging output from "make check"

* Tue Jul  3 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.12.6-6
- Block building on ppc64

* Mon Jul  2 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.12.6-5
- Update description.

* Fri Jun 29 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.12.6-4
- Get rid of .h.in files.

* Fri Jun 29 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.12.6-3
- Link glib library with main library.

* Tue Jun 26 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.12.6-2
- Re-run libtoolize and auto* to fix rpath issues.
- Add --disable-rpath to the configure line.
- The devel packages need to BR pkgconfig.

* Wed Apr 25 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.12.6-1
- Update to 1.12.6

* Fri Apr 13 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.12.5-4.work6
- Update to 1.12.5work6
- Add workaround to get tests working.

* Mon Mar  5 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.12.5-2
- Update to 1.12.5work1

* Thu Jan 11 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.12.4-1
- First version for Fedora Extras

