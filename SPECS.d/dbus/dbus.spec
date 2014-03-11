%global _hardened_build 1

%define gettext_package dbus

%define expat_version           1.95.5
%define libselinux_version      1.15.2

%define dbus_user_uid           81

%define dbus_common_config_opts --disable-libaudit --enable-selinux=no --with-init-scripts=redhat --with-system-pid-file=%{_localstatedir}/run/messagebus.pid --with-dbus-user=dbus --libdir=/%{_lib} --bindir=/bin --sysconfdir=/etc --exec-prefix=/ --libexecdir=/%{_lib}/dbus-1 --with-systemdsystemunitdir=/lib/systemd/system/ --enable-doxygen-docs --enable-xml-docs --disable-silent-rules

Summary: D-BUS message bus
Name: dbus
Epoch: 1
Version: 1.6.8
Release: 5%{?dist}
URL: http://www.freedesktop.org/software/dbus/
#VCS: git:git://git.freedesktop.org/git/dbus/dbus
Source0: http://dbus.freedesktop.org/releases/dbus/%{name}-%{version}.tar.gz
Source2: 00-start-message-bus.sh
License: GPLv2+ or AFL
Group: System Environment/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: libtool
BuildRequires: expat-devel >= %{expat_version}
BuildRequires: libX11-devel
BuildRequires: libcap-ng-devel
BuildRequires: gettext
BuildRequires: doxygen
BuildRequires: xmlto
BuildRequires: libxslt
BuildRequires:  systemd-units
Requires(post): systemd-units chkconfig
Requires(preun): systemd-units
Requires(postun): systemd-units
Requires: dbus-libs%{?_isa} = %{epoch}:%{version}-%{release}
Requires(pre): /usr/sbin/useradd

# FIXME this should be upstreamed; need --daemon-bindir=/bin and --bindir=/usr/bin or something?
Patch0: bindir.patch

%description
D-BUS is a system for sending messages between applications. It is
used both for the system-wide message bus service, and as a
per-user-login-session messaging facility.

%package libs
Summary: Libraries for accessing D-BUS
Group: Development/Libraries

%description libs
This package contains lowlevel libraries for accessing D-BUS.

%package doc
Summary: Developer documentation for D-BUS
Group: Documentation
Requires: %{name} = %{epoch}:%{version}-%{release}
BuildArch: noarch

%description doc
This package contains developer documentation for D-Bus along with
other supporting documentation such as the introspect dtd file.

%package devel
Summary: Development files for D-BUS
Group: Development/Libraries
Requires: %{name} = %{epoch}:%{version}-%{release}

%description devel
This package contains libraries and header files needed for
developing software that uses D-BUS.

%package x11
Summary: X11-requiring add-ons for D-BUS
Group: Development/Libraries
Requires: %{name} = %{epoch}:%{version}-%{release}

%description x11
D-BUS contains some tools that require Xlib to be installed, those are
in this separate package so server systems need not install X.

%prep
%setup -q -n %{name}-%{version}

# For some reason upstream ships these files as executable
# Make sure they are not
/bin/chmod 0644 COPYING ChangeLog NEWS

%patch0 -p1 -b .bindir

%build
if test -f autogen.sh; then env NOCONFIGURE=1 ./autogen.sh; else autoreconf -v -f -i; fi
%configure %{dbus_common_config_opts} --disable-tests --disable-asserts
make

%install
rm -rf %{buildroot}

make install DESTDIR=%{buildroot}

mkdir -p %{buildroot}/%{_libdir}/pkgconfig

#change the arch-deps.h include directory to /usr/lib[64] instead of /lib[64]
sed -e 's@-I${libdir}@-I${prefix}/%{_lib}@' %{buildroot}/%{_lib}/pkgconfig/dbus-1.pc > %{buildroot}/%{_libdir}/pkgconfig/dbus-1.pc
rm -f %{buildroot}/%{_lib}/pkgconfig/dbus-1.pc

mkdir -p %{buildroot}/%{_bindir}
mv -f %{buildroot}/bin/dbus-launch %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/%{_libdir}/dbus-1.0/include/
mv -f %{buildroot}/%{_lib}/dbus-1.0/include/* %{buildroot}/%{_libdir}/dbus-1.0/include/
rm -rf %{buildroot}/%{_lib}/dbus-1.0

rm -f %{buildroot}/%{_lib}/*.a
rm -f %{buildroot}/%{_lib}/*.la

install -D -m755 %{SOURCE2} %{buildroot}%{_sysconfdir}/X11/xinit/xinitrc.d/00-start-message-bus.sh

mkdir -p %{buildroot}%{_datadir}/dbus-1/interfaces

# Make sure that when somebody asks for D-Bus under the name of the
# old SysV script, that he ends up with the standard dbus.service name
# now.
ln -s dbus.service %{buildroot}/lib/systemd/system/messagebus.service

## %find_lang %{gettext_package}
# Delete the old legacy sysv init script
rm -rf %{buildroot}%{_initrddir}

mkdir -p %{buildroot}/var/lib/dbus

%check
if test -f autogen.sh; then env NOCONFIGURE=1 ./autogen.sh; else autoreconf -v -f -i; fi
%configure %{dbus_common_config_opts} --enable-asserts --enable-verbose-mode

make clean
DBUS_TEST_SLOW=1 make check

%clean
rm -rf %{buildroot}

%pre
# Add the "dbus" user and group
/usr/sbin/groupadd -r -g %{dbus_user_uid} dbus 2>/dev/null || :
/usr/sbin/useradd -c 'System message bus' -u %{dbus_user_uid} -g %{dbus_user_uid} \
	-s /sbin/nologin -r -d '/' dbus 2> /dev/null || :

%post libs -p /sbin/ldconfig

%preun
if [ $1 = 0 ]; then
  /bin/systemctl stop dbus.service dbus.socket > /dev/null 2>&1 || :
fi

%postun libs -p /sbin/ldconfig

%postun
/bin/systemctl daemon-reload >/dev/null 2>&1 || :

%triggerun -- dbus < 1.4.10-2
/sbin/chkconfig --del messagebus >/dev/null 2>&1 || :

%files
%defattr(-,root,root)

%doc COPYING

%dir %{_sysconfdir}/dbus-1
%config %{_sysconfdir}/dbus-1/*.conf
%dir %{_sysconfdir}/dbus-1/system.d
%dir %{_sysconfdir}/dbus-1/session.d
%ghost %dir %{_localstatedir}/run/dbus
%dir %{_localstatedir}/lib/dbus/
/bin/dbus-daemon
/bin/dbus-send
/bin/dbus-cleanup-sockets
/bin/dbus-monitor
/bin/dbus-uuidgen
%{_mandir}/man*/dbus-cleanup-sockets.1.gz
%{_mandir}/man*/dbus-daemon.1.gz
%{_mandir}/man*/dbus-monitor.1.gz
%{_mandir}/man*/dbus-send.1.gz
%{_mandir}/man*/dbus-uuidgen.1.gz
%dir %{_datadir}/dbus-1
%{_datadir}/dbus-1/services
%{_datadir}/dbus-1/system-services
%{_datadir}/dbus-1/interfaces
%dir /%{_lib}/dbus-1
# See doc/system-activation.txt in source tarball for the rationale
# behind these permissions
%attr(4750,root,dbus) /%{_lib}/dbus-1/dbus-daemon-launch-helper
/lib/systemd/system/dbus.service
/lib/systemd/system/dbus.socket
/lib/systemd/system/dbus.target.wants/dbus.socket
/lib/systemd/system/messagebus.service
/lib/systemd/system/multi-user.target.wants/dbus.service
/lib/systemd/system/sockets.target.wants/dbus.socket

%files libs
%defattr(-,root,root,-)
/%{_lib}/*dbus-1*.so.*

%files x11
%defattr(-,root,root)

%{_bindir}/dbus-launch
%{_datadir}/man/man*/dbus-launch.1.gz
%{_sysconfdir}/X11/xinit/xinitrc.d/00-start-message-bus.sh

%files doc
%defattr(-,root,root)
%doc doc/introspect.dtd doc/introspect.xsl doc/system-activation.txt
%doc %{_datadir}/doc/dbus

%files devel
%defattr(-,root,root)

/%{_lib}/lib*.so
%dir %{_libdir}/dbus-1.0
%{_libdir}/dbus-1.0/include/
%{_libdir}/pkgconfig/dbus-1.pc
%{_includedir}/*

%changelog

