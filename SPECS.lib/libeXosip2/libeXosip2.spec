Summary: A library that hides the complexity of using the SIP protocol
Summary(zh_CN.UTF-8): 隐藏使用 SIP 协议复杂性的库
Name: libeXosip2
Version: 4.1.0
Release: 3%{?dist}
License: GPLv2+
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL: http://savannah.nongnu.org/projects/eXosip
Source0: http://download.savannah.nongnu.org/releases/exosip/libeXosip2-%{version}.tar.gz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: c-ares-devel
BuildRequires: ortp-devel >= 0.14.2
BuildRequires: libosip2-devel >= 4.0.0
BuildRequires: openssl-devel
BuildRequires: doxygen

%description
A library that hides the complexity of using the SIP protocol for
mutlimedia session establishement. This protocol is mainly to be used
by VoIP telephony applications (endpoints or conference server) but
might be also useful for any application that wish to establish
sessions like multiplayer games.

%description -l zh_CN.UTF-8
隐藏使用 SIP 协议复杂性的库。

%package devel
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Summary: Development files for libeXosip2
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires: %{name} = %{version}-%{release}
Requires: libosip2-devel

%description devel
Development files for libeXosip2.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q


%build
%configure --disable-static
make %{_smp_mflags}
make doxygen

%install
rm -rf %{buildroot}

make install DESTDIR=%{buildroot}
rm %{buildroot}%{_libdir}/%{name}.la

mkdir -p %{buildroot}%{_mandir}/man3
cp help/doxygen/doc/man/man3/*.3* %{buildroot}%{_mandir}/man3
magic_rpm_clean.sh

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README

%{_bindir}/sip_reg
%{_libdir}/libeXosip2.so.*

%files devel
%defattr(-,root,root,-)
%doc help/doxygen/doc/html help/doxygen/doc/latex

%{_includedir}/eXosip2
%{_libdir}/libeXosip2.so
%{_mandir}/man3/*.3*

%changelog
* Mon Nov 09 2015 Liu Di <liudidi@gmail.com> - 4.1.0-3
- 为 Magic 3.0 重建

* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 4.1.0-2
- 为 Magic 3.0 重建

* Wed Jul 16 2014 Liu Di <liudidi@gmail.com> - 4.1.0-1
- 更新到 4.1.0

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 3.6.0-3
- 为 Magic 3.0 重建

* Mon Dec 26 2011 Alexey Kurov <nucleo@fedoraproject.org> - 3.6.0-2
- BR: c-ares-devel

* Mon Dec 26 2011 Alexey Kurov <nucleo@fedoraproject.org> - 3.6.0-1
- libeXosip2-3.6.0

* Fri Sep  2 2011 Alexey Kurov <nucleo@fedoraproject.org> - 3.5.0-1
- libeXosip2-3.5.0
- add BR: openssl-devel
- drop gcc43 patch

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 14 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 3.1.0-1
- Update to 3.1.0

* Tue Feb  5 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 3.0.3-3
- Apply patch from Adam Tkac that fixes compilation with GCC 4.3.

* Mon Feb  4 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 3.0.3-2
- Update to new patchlevel release.

* Tue Aug 28 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 3.0.3-1
- Update to 3.0.3

* Mon Aug 28 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.2.3-3
- Bump release and rebuild.

* Mon Jun  5 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.2.3-2
- Add BR for doxygen.

* Mon May 29 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.2.3-1
- Update to 2.2.3

* Mon Feb 20 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.2.2-4
- Bump release for rebuild.

* Mon Feb 13 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.2.2-3
- Bump release and rebuild for gcc 4.1 and glibc.

* Wed Jan  4 2006 Jeffrey C. Ollie <jeff@max1.ocjtech.us> - 2.2.2
- Update to 2.2.2.
- Bump release because forgot to upload new source.

* Sat Oct 29 2005 Jeffrey C. Ollie <jcollie@lt16585.campus.dmacc.edu> - 1.9.1-0.5.pre17
- Update to next prerelease.

* Mon Oct 24 2005 Jeffrey C. Ollie <jcollie@lt16585.campus.dmacc.edu> - 1.9.1-0.4.pre16
- Remove INSTALL from %doc - not needed in an RPM package

* Sun Oct 23 2005 Jeffrey C. Ollie <jcollie@lt16585.campus.dmacc.edu> - 1.9.1-0.3.pre16
- Added -n to BuildRoot
- BR libosip2-devel for -devel subpackage.

* Sun Oct 16 2005 Jeffrey C. Ollie <jcollie@lt16585.campus.dmacc.edu> - 1.9.1-0.2.pre16
- Changed BuildRoot to match packaging guidelines.
- Remove extraneous %dir in -devel %files
- Replace %makeinstall with proper invocation.

* Fri Oct 14 2005 Jeffrey C. Ollie <jcollie@lt16585.campus.dmacc.edu> - 1.9.1-0.1.pre16
- Initial build.

