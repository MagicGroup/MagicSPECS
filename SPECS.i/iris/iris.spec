%define git 1
%define vcsdate 20151030

Name:    iris
Summary: A library for working with the XMPP/Jabber protocol
Version: 1.0.0
Release: 0.18.git%{vcsdate}%{?dist}
License: LGPLv2+
URL:     https://github.com/psi-im/iris
Source0: iris-git%{vcsdate}git.tar.xz

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
%setup -q -n %{name}-git%{vcsdate}

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
* Sun Nov 08 2015 Liu Di <liudidi@gmail.com> - 1.0.0-0.18.git20151030
- 为 Magic 3.0 重建

* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 1.0.0-0.17.git20151030
- 更新到 20151030 日期的仓库源码

* Fri Apr 18 2014 Liu Di <liudidi@gmail.com> - 1.0.0-0.16.git20140418
- 更新到 20140418 日期的仓库源码


