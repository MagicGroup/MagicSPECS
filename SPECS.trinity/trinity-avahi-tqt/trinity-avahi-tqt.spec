#
# spec file for package avahi-tqt (version R14)
#
# Copyright (c) 2014 Trinity Desktop Environment
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.
#
# Please submit bugfixes or comments via http://www.trinitydesktop.org/
#

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.0.1
%endif

%define libavahi libavahi


Name:		trinity-avahi-tqt
Epoch:		%{tde_epoch}
Version:	0.6.30
Release:	%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}%{?_variant}.1
Summary:	Avahi TQt integration library
Summary(zh_CN.UTF-8): Avahi TQt 集成库
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL:		http://www.trinitydesktop.org/

License:	LGPLv2+

#Vendor:		Trinity Project
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:		/usr
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:	%{name}-%{tde_version}%{?preversion:~%{preversion}}.tar.gz

BuildRequires:	libtqt4-devel >= %{tde_epoch}:4.2.0

BuildRequires:	gcc-c++
BuildRequires:	pkgconfig
BuildRequires:	libtool

# GLIB2 support
BuildRequires:	glib2-devel

# GETTEXT support
BuildRequires:	gettext-devel

BuildRequires:	libXi-devel

# DBUS support
BuildRequires:	dbus-devel

# PCAP support
BuildRequires:	libcap-devel

# AVAHI support
%define avahi_devel avahi-devel
%{?avahi_devel:BuildRequires: %{avahi_devel}}

# EXPAT support
BuildRequires:	expat-devel

# NAS support
%define with_nas 1
BuildRequires: nas-devel

# XT support
BuildRequires: libXt-devel

%description
Avahi is a fully LGPL framework for Multicast DNS Service Discovery.
It allows programs to publish and discover services and hosts
running on a local network with no specific configuration. For
example you can plug into a network and instantly find printers to
print to, files to look at and people to talk to.
 .
This library contains the interface to integrate the Avahi libraries
into a TQt main loop application.
%description -l zh_CN.UTF-8
Avahi Tqt 集成库。

##########

%package -n %{libavahi}-tqt1
Summary:	Avahi TQt integration library
Summary(zh_CN.UTF-8): Avahi TQT 集成库
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Provides:	libavahi-tqt1 = %{?epoch:%{epoch}:}%{version}-%{release}

Obsoletes:		trinity-avahi-tqt < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:		trinity-avahi-tqt = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n %{libavahi}-tqt1
Avahi is a fully LGPL framework for Multicast DNS Service Discovery.
It allows programs to publish and discover services and hosts
running on a local network with no specific configuration. For
example you can plug into a network and instantly find printers to
print to, files to look at and people to talk to.
 .
This library contains the interface to integrate the Avahi libraries
into a TQt main loop application.

%description -n %{libavahi}-tqt1 -l zh_CN.UTF-8
Avahi TQT 集成库。

%post -n %{libavahi}-tqt1
/sbin/ldconfig || :

%postun -n %{libavahi}-tqt1
/sbin/ldconfig || :

%files -n %{libavahi}-tqt1
%defattr(-,root,root,-)
%{_libdir}/libavahi-tqt.so.1
%{_libdir}/libavahi-tqt.so.1.0.0

##########

%package -n %{libavahi}-tqt-devel
Summary:	Avahi TQt integration library (Development Files)
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Provides:	libavahi-tqt-devel = %{?epoch:%{epoch}:}%{version}-%{release}

Requires:	%{libavahi}-tqt1 = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:	libtqt4-devel >= %{tde_epoch}:4.2.0
%{?avahi_devel:Requires: %{avahi_devel}}

Obsoletes:		trinity-avahi-tqt-devel < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:		trinity-avahi-tqt-devel = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n %{libavahi}-tqt-devel
Avahi is a fully LGPL framework for Multicast DNS Service Discovery.
It allows programs to publish and discover services and hosts
running on a local network with no specific configuration. For
example you can plug into a network and instantly find printers to
print to, files to look at and people to talk to.
 .
This library contains the interface to integrate the Avahi libraries
into a TQt main loop application.

%description -n %{libavahi}-tqt-devel -l zh_CN.UTF-8
%{name} 的开发包。

%post -n %{libavahi}-tqt-devel
/sbin/ldconfig || :

%postun -n %{libavahi}-tqt-devel
/sbin/ldconfig || :

%files -n %{libavahi}-tqt-devel
%defattr(-,root,root,-)
%{_includedir}/avahi-tqt/
%{_libdir}/libavahi-tqt.so
%{_libdir}/libavahi-tqt.la
%{_libdir}/pkgconfig/avahi-tqt.pc

##########

%prep
%setup -q -n %{name}-%{tde_version}%{?preversion:~%{preversion}}
export NOCONFIGURE=1
./autogen.sh


%build
unset QTDIR QTINC QTLIB
export PATH="%{tde_bindir}:${PATH}"

%configure \
  --exec-prefix=%{_prefix} \
  --includedir=%{_includedir} \
  --libdir=%{_libdir} \
  \
  --disable-static \
  --disable-dependency-tracking \
  \
  --enable-compat-libdns_sd \
  --with-systemdsystemunitdir=/lib/systemd/system \
%if 0%{?suse_version}
  --with-distro=suse \
%endif
%if 0%{?fedora} || 0%{?rhel}
  --with-distro=fedora \
%endif
%if 0%{?mdkversion} || 0%{?mgaversion}
  --with-distro=mandriva \
%endif

%__make %{?_smp_mflags} || %__make


%install
%__rm -rf %{?buildroot}
%__make install DESTDIR=%{?buildroot}


%clean
%__rm -rf %{?buildroot}


%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 2:0.6.30-1.1
- 为 Magic 3.0 重建

* Fri Jul 05 2013 Francois Andriot <francois.andriot@free.fr> - 2:0.6.30-1
- Initial release for TDE 14.0.0
