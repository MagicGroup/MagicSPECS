Summary: Distributed SSL session cache
Summary(zh_CN.UTF-8): 分布式 SSL 会话缓存
Name: distcache
Version: 1.4.5
Release: 4%{?dist}
License: LGPLv2
Group: System Environment/Daemons
Group(zh_CN.UTF-8): 系统环境/服务
URL: http://www.distcache.org/
Source0: http://downloads.sourceforge.net/distcache/%{name}-%{version}.tar.bz2
Patch0: distcache-1.4.5-setuid.patch
Patch1: distcache-1.4.5-libdeps.patch
Patch2: distcache-1.4.5-limits.patch
Source1: dc_server.init
Source2: dc_client.init
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: automake >= 1.7, autoconf >= 2.50, libtool, openssl-devel
Requires(post): /sbin/chkconfig, /sbin/ldconfig, shadow-utils
Requires(preun): /sbin/service, /sbin/chkconfig

%description
The distcache package provides a variety of functionality for
enabling a network-based session caching system, primarily for
(though not restricted to) SSL/TLS session caching.

%description -l zh_CN.UTF-8
distcache 包提供了一个多样化的方法来启用基于网络的会话缓存系统，
主要是 SSL/TLS 会话缓存。

%package devel
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Summary: Development tools for distcache distributed session cache
Summary(zh_CN.UTF-8): distcache 的开发工具
Requires: %{name} = %{version}-%{release}

%description devel
This package includes the libraries that implement the necessary
network functionality, the session caching protocol, and APIs for
applications wishing to use a distributed session cache, or indeed
even to implement a storage mechanism for a session cache server.

%description devel -l zh_CN.UTF-8
distcache 的开发工具

%prep
%setup -q
%patch0 -p1 -b .setuid
%patch1 -p1 -b .libdeps
%patch2 -p1 -b .limits

%build
libtoolize --force --copy && aclocal && autoconf
automake -aic --gnu || : automake ate my hamster
%configure --enable-shared --disable-static
make %{?_smp_mflags} LIBTOOL=/usr/bin/libtool

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT LIBTOOL=/usr/bin/libtool
make -C ssl install DESTDIR=$RPM_BUILD_ROOT LIBTOOL=/usr/bin/libtool

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d
install -p -m 755 $RPM_SOURCE_DIR/dc_server.init \
        $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/dc_server
install -p -m 755 $RPM_SOURCE_DIR/dc_client.init \
        $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/dc_client

mkdir -p $RPM_BUILD_ROOT%{_sbindir}

# Unpackaged files
rm -f $RPM_BUILD_ROOT%{_bindir}/{nal_test,piper} \
      $RPM_BUILD_ROOT%{_libdir}/lib*.la \
      $RPM_BUILD_ROOT%{_libdir}/lib*.a

%post
/sbin/chkconfig --add dc_server
/sbin/chkconfig --add dc_client
/sbin/ldconfig
# Add the "distcache" user
/usr/sbin/useradd -c "Distcache" -u 94 \
        -s /sbin/nologin -r -d / distcache 2> /dev/null || :

%preun
if [ $1 = 0 ]; then
    /sbin/service dc_server stop > /dev/null 2>&1
    /sbin/service dc_client stop > /dev/null 2>&1
    /sbin/chkconfig --del dc_server
    /sbin/chkconfig --del dc_client
fi

%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_bindir}/sslswamp
%{_bindir}/dc_*
%{_sysconfdir}/rc.d/init.d/dc_*
%doc ANNOUNCE CHANGES README LICENSE FAQ
%{_libdir}/*.so.*
%{_mandir}/man1/*
%{_mandir}/man8/*
%{_datadir}/swamp

%files devel
%defattr(-,root,root,-)
%{_includedir}/distcache
%{_includedir}/libnal
%{_libdir}/*.so
%{_mandir}/man2/*

%changelog
* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 1.4.5-4
- 为 Magic 3.0 重建

* Thu Jul 17 2008 Liu Di <liudidi@gmail.com> - 1.4.5-1mgc
- 为 Magic 打包

