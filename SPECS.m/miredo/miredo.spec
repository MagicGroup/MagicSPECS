# vim: expandtab

%define withjudy 1

Name:           miredo
Version:        1.1.7
Release:        5%{?dist}
Summary:        Tunneling of IPv6 over UDP through NATs
Summary(zh_CN):	通过基于 UDP 协议的 IPv6 隧道

Group:          Applications/Internet
Group(zh_CN):	应用程序/互联网
License:        GPLv2+
URL:            http://www.simphalempin.com/dev/miredo/
Source0:        http://www.remlab.net/files/miredo/miredo-%{version}.tar.bz2
Source1:        miredo-client.init
Source2:        miredo-server.init
Patch0:         miredo-config-not-exec
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:    libcap-devel 
%if %{withjudy}
BuildRequires:     Judy-devel
%endif


Requires(pre):    shadow-utils
Requires(post):   chkconfig, /sbin/ldconfig
# This is for /sbin/service
Requires(preun):  chkconfig, initscripts
Requires(postun): initscripts, /sbin/ldconfig

%description
Miredo is an implementation of the "Teredo: Tunneling IPv6 over UDP
through NATs" proposed Internet standard (RFC4380). It can serve
either as a Teredo client, a stand-alone Teredo relay, or a Teredo
server, please install the miredo-server or miredo-client aproprietly.
It is meant to provide IPv6 connectivity to hosts behind NAT
devices, most of which do not support IPv6, and not even
IPv6-over-IPv4 (including 6to4).

%description -l zh_CN
通过基于 UDP 协议的 IPv6 隧道

%package libs
Summary:        Tunneling of IPv6 over UDP through NATs
Summary(zh_CN): %name 的库文件
Group:          Applications/Internet 
Group(zh_CN):   应用程序/互联网

%description libs
Miredo is an implementation of the "Teredo: Tunneling IPv6 over UDP
through NATs" proposed Internet standard (RFC4380). It can serve
either as a Teredo client, a stand-alone Teredo relay, or a Teredo
server, please install the miredo-server or miredo-client aproprietly.
It is meant to provide IPv6 connectivity to hosts behind NAT
devices, most of which do not support IPv6, and not even
IPv6-over-IPv4 (including 6to4).
This libs package provides the files necessary for both server and client.

%description libs -l zh_CN
%name 的库文件

%package devel
Summary:        Header files, libraries and development documentation for %{name}
Summary(zh_CN):	%name 开发包
Group:          Development/Libraries
Group(zh_CN):	开发/库
Requires:       %{name}-libs = %{version}-%{release}

%description devel
This package contains the header files, development libraries and development
documentation for %{name}. If you would like to develop programs using %{name},
you will need to install %{name}-devel.

%description devel -l zh_CN
%name 的开发包

%package server
Summary:        Tunneling server for IPv6 over UDP through NATs
Summary(zh_CN):	通过路由的基于 UDP 协议的 IPv6 隧道
Group:          Applications/Internet
Group(zh_CN):   应用程序/互联网
Requires:       %{name}-libs = %{version}-%{release}
%description server
Miredo is an implementation of the "Teredo: Tunneling IPv6 over UDP
through NATs" proposed Internet standard (RFC4380). This offers the server 
part of miredo. Most people will need only the client part.

%description server -l zh_CN
通过路由的基于 UDP 协议的 IPv6 隧道，这是服务器端，一般情况下只需要客户端。

%package client
Summary:        Tunneling client for IPv6 over UDP through NATs
Summary(zh_CN):	%name 的客户端
Group:          Applications/Internet
Group(zh_CN):   应用程序/互联网
Requires:       %{name}-libs = %{version}-%{release}
Provides:       %{name} = %{version}-%{release}
Obsoletes:      %{name} <= 1.1.6


%description client
Miredo is an implementation of the "Teredo: Tunneling IPv6 over UDP
through NATs" proposed Internet standard (RFC4380). This offers the client
part of miredo. Most people only need the client part.

%description client -l zh_CN
%name 的客户端

%prep
%setup -q
%patch0 -p1 

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
%find_lang %{name}
mkdir rpmdocs
mv %{buildroot}%{_docdir}/miredo/examples rpmdocs/
mkdir -p %{buildroot}%{_initrddir}
install -p -m 755 %{SOURCE1} %{buildroot}%{_initrddir}/miredo-client
install -p -m 755 %{SOURCE2} %{buildroot}%{_initrddir}/miredo-server
rm -f %{buildroot}%{_libdir}/lib*.la
touch %{buildroot}%{_sysconfdir}/miredo/miredo-server.conf


%pre libs
getent group miredo >/dev/null || groupadd -r miredo
getent passwd miredo >/dev/null || useradd -r -g miredo -d /etc/miredo \
         -s /sbin/nologin -c "Miredo Daemon" miredo
exit 0


%post libs -p /sbin/ldconfig
 
%post client 
/sbin/chkconfig --add miredo-client

%post server
/sbin/chkconfig --add miredo-server


%preun client
if [ $1 = 0 ] ; then
    /sbin/service miredo-client stop >/dev/null 2>&1
    /sbin/chkconfig --del miredo-client
fi

%preun server
if [ $1 = 0 ] ; then
    /sbin/service miredo-server stop >/dev/null 2>&1
    /sbin/chkconfig --del miredo-server
fi


%postun libs -p /sbin/ldconfig

%postun client
if [ "$1" -ge "1" ] ; then
    /sbin/service miredo-client condrestart >/dev/null 2>&1 || :
fi


%postun server
if [ "$1" -ge "1" ] ; then
    /sbin/service miredo-server condrestart >/dev/null 2>&1 || :
fi

%clean
rm -rf %{buildroot}


%files libs -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README THANKS TODO rpmdocs/*
#%doc %{_mandir}/man?/miredo*
%dir %{_sysconfdir}/miredo
%{_libdir}/libteredo.so.*
%{_libdir}/libtun6.so.*
%{_libdir}/miredo/

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
%{_initrddir}/miredo-server
%doc %{_mandir}/man1/teredo-mire*
%doc %{_mandir}/man?/miredo-server*
%doc %{_mandir}/man?/miredo-checkconf*


%files client
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/miredo/miredo.conf
%config(noreplace) %{_sysconfdir}/miredo/client-hook
%{_initrddir}/miredo-client
%{_sbindir}/miredo
%doc %{_mandir}/man?/miredo.*


%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.1.7-5
- 为 Magic 3.0 重建

* Thu Jul 30 2009 Jens Kuehnel <fedora-package@jens.kuehnel.org> 1.1.7-4
- Fix Obsoletes for smooth upgrade

* Tue Jul 28 2009 Jens Kuehnel <fedora-package@jens.kuehnel.org> 1.1.7-3
- without July as optional, hopefully the last EL fix

* Sun Jul 19 2009 Jens Kuehnel <fedora-package@jens.kuehnel.org> 1.1.7-2
- rename miredo to miredo-libs
- fixes EL

* Thu Jul 14 2009 Jens Kuehnel <fedora-package@jens.kuehnel.org> 1.1.7-1
- split into server and client package
- update to upstream 1.1.7

* Sat Jun 28 2009 Jens Kuehnel <fedora-package@jens.kuehnel.org> 1.1.6-2
- renamed miredo startscript to miredo-client
- preliminary preperation for EL
- miredo-server.conf ghosted
- removed .la files instead excluding of them
- fixed ldconfig requires

* Sat Jun 27 2009 Jens Kuehnel <fedora-package@jens.kuehnel.org> 1.1.6-1
- ReInitiate Fedora package review
- update to 1.1.6
- removed isatap stuff
- don't start it by default

* Sun Oct 05 2008 Charles R. Anderson <cra@wpi.edu> 1.1.5-1
- Initial Fedora package based on Dries miredo.spec 5059
- Updated to 1.1.5
- disable-static libs
- remove hardcoded rpaths
- create initscripts for client, server, and isatap daemon
- create system user miredo for daemon to setid to
