Name:           libzrtpcpp
Version: 4.2.4
Release: 1%{?dist}
Summary:        ZRTP support library for the GNU ccRTP stack
Summary(zh_CN.UTF-8): GNU ccRTP stack 的 ZRTP 支持库

Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        GPLv3+
URL:            https://github.com/wernerd/ZRTPCPP
Source0:        https://github.com/wernerd/ZRTPCPP/archive/V%{version}.tar.gz
#Source0:	ZRTPCPP-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	ccrtp-devel 
BuildRequires:	libgcrypt-devel
BuildRequires:	doxygen
BuildRequires:  cmake
BuildRequires:  openssl-devel

%description
This package provides a library that adds ZRTP support to the GNU
ccRTP stack. Phil Zimmermann developed ZRTP to allow ad-hoc, easy to
use key negotiation to setup Secure RTP (SRTP) sessions. GNU ZRTP
together with GNU ccRTP (1.5.0 or later) provides a ZRTP
implementation that can be directly embedded into client and server
applications.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:	pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n ZRTPCPP-%{version}


sed -i '/CMAKE_VERBOSE_MAKEFILE/d' CMakeLists.txt
sed -i 's/%{_lib}/lib/g' CMakeLists.txt

%build
%cmake .
make %{?_smp_mflags}

# Make the NEWS file non executable
chmod 644 NEWS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc README.md AUTHORS COPYING NEWS
%{_libdir}/libzrtpcpp.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/libzrtpcpp/
%{_libdir}/libzrtpcpp.so
%{_libdir}/pkgconfig/libzrtpcpp.pc


%changelog
* Fri Aug 08 2014 Liu Di <liudidi@gmail.com> - 4.2.4-1
- 更新到 4.2.4

* Mon Jun 23 2014 Liu Di <liudidi@gmail.com> - 4.2.3-5
- 更新到 4.2.3

* Mon Jun 23 2014 Liu Di <liudidi@gmail.com> - 2.3.4-5
- 更新到 4.2.3

* Mon Jun 23 2014 Liu Di <liudidi@gmail.com> - 2.3.4-5
- 更新到 4.2.3

* Mon Jun 23 2014 Liu Di <liudidi@gmail.com> - 2.3.4-5
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Oct 18 2013 Alexey Kurov <nucleo@fedoraproject.org> - 2.3.4-3
- re-enable ec encryption

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 03 2013 Kevin Fenzi <kevin@scrye.com> 2.3.4-1
- Update to 2.3.4
- Fixes CVE-2013-2221 CVE-2013-2222 CVE-2013-2223

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Nov 21 2012 Kevin Fenzi <kevin@scrye.com> 2.3.2-1
- Update to 2.3.2

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.2-2
- Rebuilt for c++ ABI breakage

* Fri Feb 24 2012 Alexey Kurov <nucleo@fedoraproject.org> - 2.1.2-1
- Update to 2.1.2
- drop upstreamed 64-bit patch
- visibility issue fixed in upstream

* Thu Feb 23 2012 Alexey Kurov <nucleo@fedoraproject.org> - 2.1.1-2
- Workaround for -fvisibility=hidden from commoncpp.pc

* Wed Feb 22 2012 Alexey Kurov <nucleo@fedoraproject.org> - 2.1.1-1
- Update to 2.1.1
- Updated URL

* Tue Feb 21 2012 Dan Horák <dan[at]danny.cz> - 2.0.0-2
- fix build on 64-bit arches

* Sun Jan 22 2012 Kevin Fenzi <kevin@scrye.com> - 2.0.0-1
- Update to 2.0.0

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Apr 07 2009 Kevin Fenzi <kevin@tummy.com> - 1.4.3-1
- Update to 1.4.3 and rebuild against new ccrtp

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jun 30 2008 Kevin Fenzi <kevin@tummy.com> - 1.3.0-2
- Fix unused-direct-shlib-dependency and other minor issues. 

* Wed Jun 25 2008 Kevin Fenzi <kevin@tummy.com> - 1.3.0-1
- Initial version for Fedora

