Name:           engine_pkcs11
Version:        0.1.8
Release:        5%{?dist}
Summary:        A PKCS#11 engine for use with OpenSSL
Summary(zh_CN.UTF-8): 使用 OpenSSL 的 PKCS#11 引擎

Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
License:        BSD
URL:            http://www.opensc-project.org/engine_pkcs11/
Source0:        http://www.opensc-project.org/files/%{name}/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  openssl-devel pkgconfig
BuildRequires:  libp11-devel >= 0.2.5
Requires:       openssl > 0.9.6

%description
Engine_pkcs11 is an implementation of an engine for OpenSSL. It can be loaded
using code, config file or command line and will pass any function call by
openssl to a PKCS#11 module. Engine_pkcs11 is meant to be used with smart
cards and software for using smart cards in PKCS#11 format, such as OpenSC.

%description -l zh_CN.UTF-8
使用 OpenSSL 的 PKCS#11 引擎。


%prep
%setup -q


%build
%configure --disable-static --libdir %{_libdir}/openssl
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/%{name}
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc NEWS doc/README
%doc doc/nonpersistent/wiki.out/*.html doc/nonpersistent/wiki.out/*.css
%{_libdir}/openssl/engines/engine_pkcs11.so


%changelog
* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 0.1.8-5
- 为 Magic 3.0 重建

* Thu Nov 17 2011 Liu Di <liudidi@gmail.com> - 0.1.8-4
- 为 Magic 3.0 重建

* Fri Apr 15 2011 Kalev Lember <kalev@smartlink.ee> - 0.1.8-3
- Rebuilt for lib11 0.2.8 soname bump

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 14 2010 Tomas Mraz <tmraz@redhat.com> - 0.1.8-1
- Update to the current upstream release

* Sat Aug 22 2009 Kalev Lember <kalev@smartlink.ee> - 0.1.4-7
- Rebuilt with new libp11

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 0.1.4-6
- rebuilt with new openssl

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 16 2009 Tomas Mraz <tmraz@redhat.com> - 0.1.4-3
- rebuild with new openssl

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.1.4-2
- Autorebuild for GCC 4.3

* Thu Dec 06 2007 Matt Anderson <mra@hp.com> - 0.1.4-1
- Update to latest upstream sources

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 0.1.3-5
- Rebuild for selinux ppc32 issue.


* Thu Jun 28 2007 Matt Anderson <mra@hp.com> - 0.1.3-4
- tibbs@math.uh.edu pointed out that OpenSSL engines go in /usr/lib/openssl

* Thu Jun 28 2007 Matt Anderson <mra@hp.com> - 0.1.3-3
- Feedback from tibbs@math.uh.edu, Source0 URL and directory ownership

* Wed Jun 27 2007 Matt Anderson <mra@hp.com> - 0.1.3-2
- Applied changes based on feedback from michael@gmx.net

* Thu Jun 21 2007 Matt Anderson <mra@hp.com> - 0.1.3-1
- Initial RPM packaging

