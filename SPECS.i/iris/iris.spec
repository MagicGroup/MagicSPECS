
%define snap 20131107

Name:    iris
Summary: A library for working with the XMPP/Jabber protocol
Version: 1.0.0
Release: 0.16.%{snap}git%{?dist}
License: LGPLv2+
URL:     https://github.com/psi-im/iris
Source0: iris-1.0.0-%{snap}git.tar.gz

BuildRequires: pkgconfig(libidn)
BuildRequires: pkgconfig(qca2)
BuildRequires: pkgconfig(QtNetwork)
BuildRequires: zlib-devel

Requires: qjdns%{?_isa} = %{version}-%{release}
# some default qca plugin(s)
Requires: qca-ossl%{?_isa}

## upstreamable patches
# add pkgconfig support
# add 'make install' target
Patch0: iris-1.0.0-install.patch
# Build shared library, bump VERSION to 2.0.0 for ABI changes from Kopete
Patch1: iris-1.0.0-sharedlib.patch
# install jdns
Patch3: iris-1.0.0-jdns_install.patch
# omit source files with undefined references
Patch4: iris-1.0.0-no_undefined.patch

%description
%{summary}.

%package devel
Summary:  Development file for %{name} 
Requires: %{name}%{?_isa} = %{version}-%{release}
%description devel
%{summary}.

%package -n qjdns
Summary: a simple DNS implementation that can perform normal as well as Multicast DNS queries
License: MIT
%description -n qjdns
JDNS is a simple DNS implementation that can perform normal DNS queries
of any record type (notably SRV), as well as Multicast DNS queries and
advertising.  Multicast support is based on Jeremie Miller's "mdnsd"
implementation.

For Qt users there is a wrapper available called QJDns.

%package -n qjdns-devel
Summary: Development files for qjdns
License: MIT
Requires: qjdns%{?_isa} = %{version}-%{release}
%description -n qjdns-devel
%{summary}.



%prep
%setup -q

%patch0 -p1 -b .install
%patch1 -p1 -b .shared
%patch3 -p1 -b .jdns_install
%patch4 -p1 -b .no_undefined



%build
./configure \
  --verbose \
  --release \
  --no-separate-debug-info \
  --disable-tests
  
make %{?_smp_mflags}


%install
make install INSTALL_ROOT=%{buildroot}

# post processing to fix iris-related headers
mv %{buildroot}%{_qt4_headerdir}/iris/jid.h \
   %{buildroot}%{_qt4_headerdir}/iris/xmpp_jid.h
sed -i -e 's|#include "xmpp/jid/jid.h"|#include "xmpp_jid.h"|g' \
  %{buildroot}%{_qt4_headerdir}/iris/*.h


%check
export PKG_CONFIG_PATH=%{buildroot}%{_qt4_libdir}/pkgconfig:
# The pkg-config versions should match the soversions.
test "$(pkg-config --modversion iris)" = "2.0.0"
test "$(pkg-config --modversion irisnet)" = "2.0.0"
test "$(pkg-config --modversion qjdns)" = "1.0.0"


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc COPYING README TODO
%{_qt4_libdir}/libiris.so.2*
%{_qt4_libdir}/libirisnet.so.2*

%files devel
%{_qt4_headerdir}/iris/
%{_qt4_libdir}/libiris.so
%{_qt4_libdir}/libirisnet.so
%{_qt4_libdir}/pkgconfig/iris.pc
%{_qt4_libdir}/pkgconfig/irisnet.pc

%post -n qjdns -p /sbin/ldconfig
%postun -n qjdns -p /sbin/ldconfig

%files -n qjdns
%doc src/jdns/README src/jdns/TODO
%{_qt4_libdir}/libqjdns.so.1*

%files -n qjdns-devel
%{_qt4_headerdir}/jdns/
%{_qt4_libdir}/libqjdns.so
%{_qt4_libdir}/pkgconfig/qjdns.pc


%changelog
* Sat Nov 23 2013 Rex Dieter <rdieter@fedoraproject.org> 1.0.0-0.16.20131107git
- 20131107 snapshot

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-0.15.20110904svn812
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 07 2013 Kevin Kofler <Kevin@tigcc.ticalc.org> 1.0.0-0.14.20110904svn812
- bump soname version to 2.0.0 for ABI changes from Kopete (#958793)

* Thu Feb 14 2013 Rex Dieter <rdieter@fedoraproject.org> 1.0.0-0.13.20110904svn812
- port/rebase kopete patches (kudos to kkofler)

* Mon Feb 11 2013 Rex Dieter <rdieter@fedoraproject.org> - 1.0.0-0.12.20110904svn812
- iris.pc: +Requires: qca2
- system_libidn.patch: link against system libidn too
- -devel: install missing headers

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-0.11.20110904svn812
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 07 2012 Rex Dieter <rdieter@fedoraproject.org> 1.0.0-0.10.20110904svn812
- fix iris headers (#772410)

* Fri Jan 06 2012 Rex Dieter <rdieter@fedoraproject.org> 1.0.0-0.9.20110904svn812
- use include/jdns instead of include/qjdns, that's what most consumers expect

* Wed Nov 16 2011 Rex Dieter <rdieter@fedoraproject.org> 1.0.0-0.8.20110904svn812
- fix Release

* Tue Nov 15 2011 Rex Dieter <rdieter@fedoraproject.org> 1.0.0-0.7.r812
- use svn revision instead of snapshot date

* Tue Nov 15 2011 Rex Dieter <rdieter@fedoraproject.org> 1.0.0-0.6.20110904
- qjdns-devel: Requires: qjdns

* Tue Nov 08 2011 Rex Dieter <rdieter@fedoraproject.org> 1.0.0-0.5.20110904
- install/package qjdns

* Mon Nov 07 2011 Rex Dieter <rdieter@fedoraproject.org> 1.0.0-0.4.20110904
- unbundle libidn

* Fri Oct 28 2011 Rex Dieter <rdieter@fedoraproject.org> 1.0.0-0.3.20110904
- pkgconfig-style deps
- Requires: qca-ossl

* Wed Oct 26 2011 Tom Callaway <spot@fedoraproject.org> 1.0.0-0.2.20110904
- finish install patch
- generate sharedlibs

* Sun Sep 04 2011 Rex Dieter <rdieter@fedoraproject.org> 1.0.0-0.1.20110904
- first try
