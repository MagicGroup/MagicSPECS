%define beta 3

Name:       qca-ossl
Version:    2.0.0
Release:    0.17.beta%{beta}%{?dist}

Summary:    OpenSSL plugin for the Qt Cryptographic Architecture v2
License:    LGPLv2+
Group:      System Environment/Libraries
URL:        http://delta.affinix.com/qca/
Source0:    http://delta.affinix.com/download/qca/2.0/plugins/qca-ossl-%{version}-beta%{beta}.tar.bz2
Patch1:     qca-ossl-2.0.0-no-whirlpool.patch
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: qt4-devel, qca2-devel >= 2.0.0-1
BuildRequires: openssl-devel >= 0.9.8

Provides:   qca2-ossl = %{version}-%{release}

%{?_qt4_version:Requires: qt4%{?_isa} >= %{_qt4_version}}

%description
This is a plugin to provide SSL/TLS capability to programs that use the Qt
Cryptographic Architecture (QCA).  QCA is a library providing an easy API
for several cryptographic algorithms to Qt programs.  This package only
contains the TLS plugin.

%prep
%setup -q -n %{name}-%{version}-beta%{beta}
%patch1 -p1 -b .no-whirlpool

%build
unset QTDIR
./configure \
  --no-separate-debug-info \
  --verbose
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT

export INSTALL_ROOT=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_qt4_plugindir}/crypto
make install
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc README COPYING
%{_qt4_plugindir}/crypto/libqca-ossl.so


%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 2.0.0-0.17.beta3
- 为 Magic 3.0 重建

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-0.16.beta3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Mar 14  2012 Alexey Kurov <nucleo@fedoraproject.org> - 2.0.0-0.15.beta3
- yet one rebuilt for openssl-1.0.1 (f18), openssl-1.0.0 (f17)

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-0.14.beta3
- Rebuilt for c++ ABI breakage

* Wed Feb 15  2012 Alexey Kurov <nucleo@fedoraproject.org> - 2.0.0-0.13.beta3
- Rebuilt for openssl-1.0.1

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-0.12.beta3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-0.11.beta3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Apr 29 2010 Rex Dieter <rdieter@fedoraproject.org> - 2.0.0-0.10.beta3
- add minimal qt4 dep
- don't own %%{_qt4_plugindir}/crypto/

* Fri Jan 29 2010 Alexey Kurov <nucleo@fedoraproject.org> - 2.0.0-0.9.beta3
- Provides: qca2-ossl (fixes bug #512000)

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 2.0.0-0.8.beta3
- rebuilt with new openssl

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-0.7.beta3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-0.6.beta3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jan 26 2009 Tomas Mraz <tmraz@redhat.com> - 2.0.0-0.5.beta3
- rebuild with new openssl
- fix the test for whirlpool support

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.0.0-0.4.beta3
- Autorebuild for GCC 4.3

* Thu Dec 13 2007 Aurelien Bompard <abompard@fedoraproject.org> 2.0.0-0.3.beta3
- version 2.0.0 beta 3

* Fri Dec 07 2007 Release Engineering <rel-eng at fedoraproject dot org> - 2.0.0-0.2.beta1
- Rebuild for deps

* Tue Nov 06 2007 Aurelien Bompard <abompard@fedoraproject.org> 2.0.0-0.1.beta1
- version 2.0.0 beta 1

* Sat Oct 27 2007 Aurelien Bompard <abompard@fedoraproject.org> 0.1-4.20070904
- update Source1 URL

* Thu Oct 25 2007 Aurelien Bompard <abompard@fedoraproject.org> 0.1-3.20070904
- update to 20070904

* Thu Sep 13 2007 Aurelien Bompard <abompard@fedoraproject.org> 0.1-2.20070706
- fixes from review in bug 289701 (thanks Rex)

* Thu Sep 13 2007 Aurelien Bompard <abompard@fedoraproject.org> 0.1-1.20070706
- initial package
