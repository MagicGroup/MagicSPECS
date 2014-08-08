Name:		proxychains
Version:	3.1
Release:	15%{?dist}
Summary:	Provides proxy support to any application
Group:		Applications/Internet
License:	GPLv2+
URL:		http://proxychains.sourceforge.net
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Patch0:		proxychains-3.1-ld_preload.patch
Patch1:         proxychains-3.1-glibc215.patch
Requires:	bind-utils

%description
Proxychains forces any tcp connection made by any given tcp client to 
follow through a proxy. Proxychains intercepts TCP calls and forces 
them through a user defined proxy

You must configure /etc/proxychains.conf before use

%prep
%setup -q
%patch0 -p1 -b .ld_preload
%patch1 -p1 -b .glibc215

%build
%configure --disable-static
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="%{__install} -p"
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.so

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc AUTHORS ChangeLog COPYING README
%config(noreplace) %{_sysconfdir}/proxychains.conf
%{_bindir}/proxychains
%{_bindir}/proxyresolv
%{_libdir}/libproxychains.so.3
%{_libdir}/libproxychains.so.3.0.0

%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Mar  8 2012 Tom Callaway <spot@fedoraproject.org> - 3.1-11
- fix build against modern glibc (getnameinfo struct types change)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Aug 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 3.1-6
- fix license tag

* Sat Feb 09 2008 Tyler Owen <tyler.l.owen at gmail dot com> - 3.1-5
- Rebuild for GCC 4.3

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 3.1-4
- Rebuild for selinux ppc32 issue.

* Sat Jul 07 2007 Tyler Owen <tyler.l.owen@gmail.com> - 3.1-3
- Added -p option to install to preserve timestamps
- Added Requires for bind-utils

* Wed Jun 20 2007 Tyler Owen <tyler.l.owen@gmail.com> 3.1-2
- Removed proxychains-devel package as it is not needed
- Removed .la file

* Sun Jun 10 2007 Tyler Owen <tyler.l.owen@gmail.com> 3.1-1
- Initial RPM build
