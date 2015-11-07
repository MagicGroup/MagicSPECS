Name:           nss_compat_ossl
Version:        0.9.6
Release:        6%{?dist}
Summary:        Source-level compatibility library for OpenSSL to NSS porting
Summary(zh_CN.UTF-8): OpenSSL 移植到 NSS 的源代码级别兼容库

Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        MIT
URL:            http://rcritten.fedorapeople.org/nss_compat_ossl.html
Source0:        http://rcritten.fedorapeople.org/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# Need > 3.11.7-7 so we have the NSS PKCS#11 flat-file reader available 
BuildRequires:  nss-devel > 3.11.7-7
BuildRequires:  nspr-devel

%description
This library provides a source-level compatibility layer to aid porting
programs that use OpenSSL to use the NSS instead.

%description -l zh_CN.UTF-8
OpenSSL 移植到 NSS 的源代码级别兼容库。

%package devel
Summary:          Development libraries for nss_compat_ossl
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:            Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:         %{name} = %{version}-%{release}
Requires:         nss-devel

%description devel
Header and library files for doing porting work from OpenSSL to NSS.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q

%build

CFLAGS="$RPM_OPT_FLAGS -DPKCS11_PEM_MODULE"
export CFLAGS

%configure --prefix=/usr --disable-static
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# We don't want to ship the .la file
rm $RPM_BUILD_ROOT/%{_libdir}/libnss_compat_ossl.la
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_libdir}/libnss_compat_ossl.so.*
%doc README COPYING

%files devel
%defattr(-,root,root,-)
%dir %{_includedir}/nss_compat_ossl
%{_includedir}/nss_compat_ossl/nss_compat_ossl.h
%{_libdir}/libnss_compat_ossl.so

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 0.9.6-6
- 为 Magic 3.0 重建

* Sat Feb 28 2015 Liu Di <liudidi@gmail.com> - 0.9.6-5
- 为 Magic 3.0 重建

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 0.9.6-4
- 为 Magic 3.0 重建

* Thu Nov 15 2012 Liu Di <liudidi@gmail.com> - 0.9.6-3
- 为 Magic 3.0 重建

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan  5 2010 Rob Crittenden <rcritten@redhat.com> - 0.9.6-1
- Update to 0.9.6

* Mon Jan  4 2010 Rob Crittenden <rcritten@redhat.com> - 0.9.5-5
- Add nss-devel requires to the devel sub-package (BZ #550770)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Apr 29 2009 Rob Crittenden <rcritten@redhat.com> - 0.9.5-3
- Resolve BZ 497788, implement default loading of root CAs

* Mon Apr 20 2009 Rob Crittenden <rcritten@redhat.com> - 0.9.5-2
- Actually change the license in the spec file

* Mon Apr 20 2009 Rob Crittenden <rcritten@redhat.com> - 0.9.5-1
- Update to 0.9.5
- License changed to MIT

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Dec 15 2008 Rob Crittenden <rcritten@redhat.com> - 0.9.4-2
- Patch to fix segfault in parsing ciphers (#476519)

* Wed Oct  1 2008 Rob Crittenden <rcritten@redhat.com> - 0.9.4-1
- update to 0.9.4
- change Source0 to use fedoraproject.org

* Fri Sep 12 2008 Rob Crittenden <rcritten@redhat.com> - 0.9.3-1
- update to 0.9.3

* Thu Aug 28 2008 Michael Schwendt <mschwendt@fedoraproject.org> - 0.9.2-6
- include /usr/include/nss_compat_ossl directory

* Wed Jun  2 2008 Rob Crittenden <rcritten@redhat.com> 0.9.2-5
- Fix BIO NSPR layer (#453651)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.9.2-4
- Autorebuild for GCC 4.3

* Sat Oct 13 2007 Rob Crittenden <rcritten@redhat.com> 0.9.2-3
- Bugzilla #330091, don't explicitly link with libsoftokn3.so

* Wed Sep 26 2007 Rob Crittenden <rcritten@redhat.com> 0.9.2-2
- Bugzilla #306711, need to define CERT_NewTempCertificate

* Wed Sep 20 2007 Rob Crittenden <rcritten@redhat.com> 0.9.2-1
- update to 0.9.2
- Enable loading the NSS PKCS#11 pem module
- Add a URL
- Specify the license as LGPLv2+ instead of just LGPL

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 0.9.1-5
- Rebuild for selinux ppc32 issue.

* Wed Jul 25 2007 Jesse Keating <jkeating@redhat.com> - 0.9.1-4
- Rebuild for RH #249435

* Fri Jul 20 2007 Rob Crittenden <rcritten@redhat.com> 0.9.1-3
- Added missing defattr in the devel package

* Fri Jul 20 2007 Rob Crittenden <rcritten@redhat.com> 0.9.1-2
- rename LICENSE to COPYING
- don't ship the .la in -devel
- fixup devel requirement to be exactly the parent package, not >=

* Tue Jul 17 2007 Rob Crittenden <rcritten@redhat.com> 0.9.1-1
- Initial build.
