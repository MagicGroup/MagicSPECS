# vim: expandtab

%if 0%{?rhel}
%define withjudy 0
%else
%define withjudy 1
%endif

%global _hardened_build 1

Name:           miredo
Version:        1.2.6
Release:        3%{?dist}
Summary:        Tunneling of IPv6 over UDP through NATs
Summary(zh_CN.UTF-8): 在 UDP 协议上通过地址转换使用 IPv6 隧道

Group:          Applications/Internet
Group(zh_CN.UTF-8): 应用程序/互联网
License:        GPLv2+
URL:            http://www.remlab.net/miredo/
Source0:        http://www.remlab.net/files/miredo/miredo-%{version}.tar.xz
Source1:        miredo-client.service
Source2:        miredo-server.service
Patch0:         miredo-config-not-exec
Patch1:         reread-resolv-before-resolv-ipv4.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:    libcap-devel 
BuildRequires:    systemd-units
BuildRequires:    autoconf
%if %{withjudy}
BuildRequires:     Judy-devel
%endif

%description
Miredo is an implementation of the "Teredo: Tunneling IPv6 over UDP
through NATs" proposed Internet standard (RFC4380). It can serve
either as a Teredo client, a stand-alone Teredo relay, or a Teredo
server, please install the miredo-server or miredo-client appropriately.
It is meant to provide IPv6 connectivity to hosts behind NAT
devices, most of which do not support IPv6, and not even
IPv6-over-IPv4 (including 6to4).

%description -l zh_CN.UTF-8
在 UDP 协议上通过地址转换使用 IPv6 隧道。

%package libs
Summary:        Tunneling of IPv6 over UDP through NATs
Summary(zh_CN.UTF-8): 在 UDP 协议上通过地址转换使用 IPv6 隧道
Group:          Applications/Internet 
Group(zh_CN.UTF-8): 应用程序/互联网
Requires(post):   /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Requires(pre):    shadow-utils


%description libs
Miredo is an implementation of the "Teredo: Tunneling IPv6 over UDP
through NATs" proposed Internet standard (RFC4380). It can serve
either as a Teredo client, a stand-alone Teredo relay, or a Teredo
server, please install the miredo-server or miredo-client appropriately.
It is meant to provide IPv6 connectivity to hosts behind NAT
devices, most of which do not support IPv6, and not even
IPv6-over-IPv4 (including 6to4).
This libs package provides the files necessary for both server and client.

%description libs -l zh_CN.UTF-8
在 UDP 协议上通过地址转换使用 IPv6 隧道。
这是服务器和客户端都需要的库。


%package devel
Summary:        Header files, libraries and development documentation for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name}-libs = %{version}-%{release}

%description devel
This package contains the header files, development libraries and development
documentation for %{name}. If you would like to develop programs using %{name},
you will need to install %{name}-devel.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package server
Summary:        Tunneling server for IPv6 over UDP through NATs
Summary(zh_CN.UTF-8): %{name} 的服务器端
Group:          Applications/Internet
Group(zh_CN.UTF-8): 应用程序/互联网
Requires:       %{name}-libs = %{version}-%{release}
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
# For triggerun
Requires(post): systemd-sysv
%description server
Miredo is an implementation of the "Teredo: Tunneling IPv6 over UDP
through NATs" proposed Internet standard (RFC4380). This offers the server 
part of miredo. Most people will need only the client part.

%description server -l zh_CN.UTF-8
%{name} 的服务器端。

%package client
Summary:        Tunneling client for IPv6 over UDP through NATs
Summary(zh_CN.UTF-8): %{name} 的客户端
Group:          Applications/Internet
Group(zh_CN.UTF-8): 应用程序/互联网
Requires:       %{name}-libs = %{version}-%{release}
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
# For triggerun
Requires(post): systemd-sysv
Provides:       %{name} = %{version}-%{release}
Obsoletes:      %{name} <= 1.1.6

%description client
Miredo is an implementation of the "Teredo: Tunneling IPv6 over UDP
through NATs" proposed Internet standard (RFC4380). This offers the client
part of miredo. Most people only need the client part.

%description client -l zh_CN.UTF-8
%{name} 的客户端。

%prep
%setup -q
%patch0 -p1 
%patch1 -p1
autoconf

%build
%configure \
               --disable-static \
               --disable-rpath \
               --enable-miredo-user \
%if %{withjudy} == 0
               --without-Judy \
%endif


# rpath does not really work
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} INSTALL='install -p'
magic_rpm_clean.sh
%find_lang %{name}
mkdir rpmdocs
mv %{buildroot}%{_docdir}/miredo/examples rpmdocs/
mkdir -p %{buildroot}%{_unitdir}
install -p -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/miredo-client.service
install -p -m 644 %{SOURCE2} %{buildroot}%{_unitdir}/miredo-server.service
rm -f %{buildroot}%{_libdir}/lib*.la
# We use our own service file
rm -f %{buildroot}/usr/lib*/systemd/system/miredo.service
touch %{buildroot}%{_sysconfdir}/miredo/miredo-server.conf


%pre libs
getent group miredo >/dev/null || groupadd -r miredo
getent passwd miredo >/dev/null || useradd -r -g miredo -d /etc/miredo \
         -s /sbin/nologin -c "Miredo Daemon" miredo
exit 0


%post libs -p /sbin/ldconfig
 
%post client 
if [ $1 -eq 1 ] ; then 
    # Initial installation 
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi


%post server
if [ $1 -eq 1 ] ; then 
    # Initial installation 
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi


%preun client
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable miredo-client.service > /dev/null 2>&1 || :
    /bin/systemctl stop miredo-client.service > /dev/null 2>&1 || :
fi

%preun server
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable miredo-server.service > /dev/null 2>&1 || :
    /bin/systemctl stop miredo-server.service > /dev/null 2>&1 || :
fi


%postun libs -p /sbin/ldconfig

%postun client
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /bin/systemctl try-restart miredo-client.service >/dev/null 2>&1 || :
fi


%postun server
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /bin/systemctl try-restart miredo-server.service >/dev/null 2>&1 || :
fi

%triggerun -- miredo-client < 1.1.7-8
# Save the current service runlevel info
# User must manually run systemd-sysv-convert --apply miredo-client
# to migrate them to systemd targets
/usr/bin/systemd-sysv-convert --save miredo-client >/dev/null 2>&1 ||:

# Run these because the SysV package being removed won't do them
/sbin/chkconfig --del miredo-client >/dev/null 2>&1 || :
/bin/systemctl try-restart miredo-client.service >/dev/null 2>&1 || :

%triggerun -- miredo-server < 1.1.7-8
# Save the current service runlevel info
# User must manually run systemd-sysv-convert --apply miredo-server
# to migrate them to systemd targets
/usr/bin/systemd-sysv-convert --save miredo-server >/dev/null 2>&1 ||:

# Run these because the SysV package being removed won't do them
/sbin/chkconfig --del miredo-server >/dev/null 2>&1 || :
/bin/systemctl try-restart miredo-server.service >/dev/null 2>&1 || :

%clean
rm -rf %{buildroot}


%files libs -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README THANKS TODO rpmdocs/*
%{_libdir}/libteredo.so.*
%{_libdir}/libtun6.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/libteredo/
%{_includedir}/libtun6/
%{_libdir}/libteredo.so
%{_libdir}/libtun6.so

%files server
%defattr(-,root,root,-)
%ghost %config(noreplace,missingok) %{_sysconfdir}/miredo/miredo-server.conf
%{_bindir}/teredo-mire
%{_sbindir}/miredo-server
%{_sbindir}/miredo-checkconf
%{_unitdir}/miredo-server.service
%doc %{_mandir}/man1/teredo-mire*
%doc %{_mandir}/man?/miredo-server*
%doc %{_mandir}/man?/miredo-checkconf*


%files client
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/miredo/miredo.conf
%config(noreplace) %{_sysconfdir}/miredo/client-hook
%{_unitdir}/miredo-client.service
%{_sbindir}/miredo
%{_libexecdir}/miredo/miredo-privproc
%doc %{_mandir}/man?/miredo.*


%changelog
* Wed Oct 15 2014 Liu Di <liudidi@gmail.com> - 1.2.6-3
- 为 Magic 3.0 重建

* Mon Apr 14 2014 Liu Di <liudidi@gmail.com> - 1.2.6-2
- 为 Magic 3.0 重建

* Mon Aug 05 2013 Jens <bugzilla-redhat@jens.kuehnel.org> - 1.2.6-1
- upgrade to 1.2.6
- fix missing buildreq systemd-units

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Apr 23 2013 Jens <bugzilla-redhat@jens.kuehnel.org> - 1.2.5-4
- Add PIE Compilier Flag

* Mon Mar 25 2013 Jens <bugzilla-redhat@jens.kuehnel.org> - 1.2.5-3
- add autoconf for aarch64 support

* Fri Mar 22 2013 Jens <bugzilla-redhat@jens.kuehnel.org> - 1.2.5-2
- Fix deletion of mirdeo.service file for 32bit

* Thu Mar 21 2013 Jens Kuehnel <bugzilla-redhat@jens.kuehnel.org> - 1.2.5-1
- Update to 1.2.5

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.7-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.7-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Apr 24 2012 Jon Ciesla <limburgher@gmail.com> - 1.1.7-8
- Migrate to systemd, BZ 789782.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Aug 04 2010 "Jens Kuehnel <fedora-package@jens.kuehnel.org>" - 1.1.7-5
- Fixed BZ#606106 - miredo-client fails to notice resolv.conf changes

* Thu Jul 30 2009 Jens Kuehnel <fedora-package@jens.kuehnel.org> - 1.1.7-4
- Fix Obsoletes for smooth upgrade

* Tue Jul 28 2009 Jens Kuehnel <fedora-package@jens.kuehnel.org> - 1.1.7-3
- without July as optional, hopefully the last EL fix

* Sun Jul 19 2009 Jens Kuehnel <fedora-package@jens.kuehnel.org> - 1.1.7-2
- rename miredo to miredo-libs
- fixes EL

* Tue Jul 14 2009 Jens Kuehnel <fedora-package@jens.kuehnel.org> - 1.1.7-1
- split into server and client package
- update to upstream 1.1.7

* Sun Jun 28 2009 Jens Kuehnel <fedora-package@jens.kuehnel.org> - 1.1.6-2
- renamed miredo startscript to miredo-client
- preliminary preperation for EL
- miredo-server.conf ghosted
- removed .la files instead excluding of them
- fixed ldconfig requires

* Sat Jun 27 2009 Jens Kuehnel <fedora-package@jens.kuehnel.org> - 1.1.6-1
- ReInitiate Fedora package review
- update to 1.1.6
- removed isatap stuff
- don't start it by default

* Sun Oct 05 2008 Charles R. Anderson <cra@wpi.edu> - 1.1.5-1
- Initial Fedora package based on Dries miredo.spec 5059
- Updated to 1.1.5
- disable-static libs
- remove hardcoded rpaths
- create initscripts for client, server, and isatap daemon
- create system user miredo for daemon to setid to
