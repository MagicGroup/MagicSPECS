Summary:TLS Plugin for Qt Cryptographic Architecture
Summary(zh_CN.UTF-8): Qt密码体系的TLS插件
Name: qca-tls
Version: 1.0
Release: 7%{?dist}
License: LGPL 2.1
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Source: http://delta.affinix.com/qca/qca-tls-1.0.tar.bz2
Patch0: qca-tls-1.0-ossl098.patch
Patch1:	qca-tls-1.0-gcc4.patch
BuildRoot: /var/tmp/%{name}-buildroot
	    
%description
QCA-TLS is a plugin for QCA supporting SSL/TLS, X509, RSA, SHA1, Md5, Blowfish, 3DES and AES.

%description -l zh_CN.UTF-8
QCA-TLS是一个QCA的插件，它支持SSL/TLS, X509, RSA, SHA1, Md5, Blowfish, 3DES和AES。
		    
%prep
%setup
%patch0 -p1
%patch1 -p1
					    
%build
./configure
make
					  
%install
echo $RPM_BUILD_ROOT
install -D -s -m 755 libqca-tls.so $RPM_BUILD_ROOT%{_libdir}/qt-3.3/plugins/crypto/libqca-tls.so
install -D -m 644 qca.h         $RPM_BUILD_ROOT%{_libdir}/qt-3.3/include/qca.h
install -D -m 644 qcaprovider.h         $RPM_BUILD_ROOT%{_libdir}/qt-3.3/include/qcaprovider.h
install -D -m 644 qca-tls.h         $RPM_BUILD_ROOT%{_libdir}/qt-3.3/include/qca-tls.h

%clean
rm -rf $RPM_BUILD_ROOT

%post
ldconfig

%postun
ldconfig

%files
%defattr(-,root,root)
%doc README COPYING   
%{_libdir}/qt-3.3/plugins/crypto/libqca-tls.so
%{_libdir}/qt-3.3/include/qca*.h
  
%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 1.0-7
- 为 Magic 3.0 重建

* Sat Aug 27 2005 sejishikong <sejishikong@263.net>
- First Build of qca-tls
