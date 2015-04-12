Name:           ortp
Version:	0.24.0
Release:        1%{?dist}
Summary:        A C library implementing the RTP protocol (RFC3550)
Summary(zh_CN.UTF-8): RTP 协议的 C 库实现
Epoch:          1

Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        LGPLv2+ and VSL
URL:            http://www.linphone.org/eng/documentation/dev/ortp.html
Source:         http://download.savannah.gnu.org/releases/linphone/ortp/sources/%{name}-%{version}.tar.gz

Patch1:		ortp-0.23.0-libzrtpcpp.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  doxygen
BuildRequires:  graphviz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  libsrtp-devel
BuildRequires:  openssl-devel
BuildRequires:  libzrtpcpp-devel >= 2.1.0

%description
oRTP is a C library that implements RTP (RFC3550).

%description -l zh_CN.UTF-8
RTP 协议的 C 库实现。

%package        devel
Summary:        Development libraries for ortp
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:       pkgconfig
Requires:       libsrtp-devel
Requires:       libzrtpcpp-devel

%description    devel
Libraries and headers required to develop software with ortp.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup0 -q
#%patch1 -p1

autoreconf -i -f

%{__perl} -pi.dot  -e 's/^(HAVE_DOT\s+=)\s+NO$/\1 YES/;s/^(CALL_GRAPH\s+=)\s+NO$/\1 YES/;s/^(CALLER_GRAPH\s+=)\s+NO$/\1 YES/' ortp.doxygen.in

%build
%configure --disable-static \
%if 0%{?fedora} > 16
           --enable-zrtp=yes \
%endif
           --enable-ipv6 \
           --enable-ssl-hmac CFLAGS="-Wno-error=cpp"


make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name \*.la -exec rm {} \;
rm doc/html/html.tar
rm -rf %{buildroot}%{_datadir}/doc/ortp
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog TODO
%{_libdir}/libortp.so.*

%files devel
%defattr(-,root,root,-)
%doc doc/html
%{_includedir}/%{name}
%{_libdir}/libortp.so
%{_libdir}/pkgconfig/ortp.pc
%{_docdir}/*

%changelog
* Tue Mar 31 2015 Liu Di <liudidi@gmail.com> - 1:0.24.0-1
- 更新到 0.24.0

* Mon Jun 23 2014 Liu Di <liudidi@gmail.com> - 1:0.23.0-1
- 更新到 0.23.0

* Mon Jun 23 2014 Liu Di <liudidi@gmail.com> - 1:0.22.0-4
- 为 Magic 3.0 重建

* Mon Jun 09 2014 Liu Di <liudidi@gmail.com> - 1:0.22.0-3
- 更新到 0.22.0

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 1:0.20.0-3
- 为 Magic 3.0 重建

* Thu Feb 23 2012 Alexey Kurov <nucleo@fedoraproject.org> - 1:0.20.0-2
- ortp-0.20.0
- BR: libzrtpcpp-devel for F17+

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.18.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec 26 2011 Alexey Kurov <nucleo@fedoraproject.org> - 0.18.0-1
- ortp-0.18.0
- drop patches for issues fixed in upstream (retval and unused vars)

* Tue Sep 27 2011 Dan Horák <dan[at]danny.cz> - 1:0.16.5-2
- fix another gcc warning and move all fixes to one patch

* Fri Sep  2 2011 Alexey Kurov <nucleo@fedoraproject.org> - 0.16.5-1
- ortp-0.16.5
- add BR: libsrtp-devel openssl-devel

* Tue Mar 15 2011 Karsten Hopp <karsten@redhat.com> 0.16.1-3.1
- fix build error (unused variable)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.16.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Sep  2 2010 Dan Horák <dan[at]danny.cz> - 1:0.16.1-2
- fix "ignoring return value" warning

* Mon Nov 30 2009 Rakesh Pandit <rakesh@fedoraproject.org> - 1:0.16.1-1
- Updated to 0.16.1, removed old patch
- removed autotool calls, and using install -p

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.14.2-0.5.20080211
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.14.2-0.4.20080211
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Aug 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1:0.14.2-0.3.20080211
- fix license tag
- epoch bump to fix pre-release versioning

* Thu Feb 14 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.14.2-0.20080211.2%{?dist}
- Update to 0.14.2 snapshot

* Tue Feb  5 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.14.1-0.20080123.2
- Apply patch to remove -Werror from the build (for PPC).

* Fri Feb  1 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.14.1-0.20080123.1
- Update to 0.14.1 (using CVS snapshot until official release is available).

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 0.13.1-4
- Rebuild for selinux ppc32 issue.

* Fri Jun 22 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.13.1-2
- Fix URL

* Mon Apr 23 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.13.1-1
- Update to 0.13.1
- BR doxygen and graphviz for building documentation

* Mon Jan 29 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.13.0-1
- Update to 0.13.0
- ortp-devel BR pkgconfig
- Add ldconfig scriptlets

* Tue Nov 21 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.12.0-1
- Update to 0.12.0

* Mon Oct  9 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.11.0-2
- Bring back -Werror patch (needed for building on PPC)

* Mon Oct  9 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.11.0-1
- Update to 0.11.0
- Remove ortp-0.8.1-Werror.patch

* Wed Aug 30 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.8.1-3
- Bump release and rebuild

* Mon Feb 13 2006 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.8.1-2
- Rebuild for Fedora Extras 5

* Tue Jan  3 2006 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.8.1-1
- Upstream update

* Thu Dec 22 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.7.1-2
- Added ortp.pc to -devel

* Sat Dec  3 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.7.1-1
- Upstream update

* Wed Nov 30 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.7.0-6
- Fix a typo in Requires on -devel

* Wed Nov 30 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.7.0-5
- Add missing Requires on -devel

* Sun Nov 13 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.7.0-4
- Split from linphone
