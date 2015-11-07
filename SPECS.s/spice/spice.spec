# build_client:
# If you want to build both client and server change value to 1
# If you want to only build the server change value to 0
%define build_client        1

Name:           spice
Version:	0.12.6
Release:	2%{?dist}
Summary:        Implements the SPICE protocol
Summary(zh_CN.UTF-8): SPICE 协议的实现
Group:          User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
License:        LGPLv2+
URL:            http://www.spice-space.org/
Source0:        http://www.spice-space.org/download/releases/%{name}-%{version}.tar.bz2
Source1:        spice-xpi-client-spicec

# https://bugzilla.redhat.com/show_bug.cgi?id=613529
ExclusiveArch:  i686 x86_64 armv6l armv7l armv7hl

BuildRequires:  pkgconfig
BuildRequires:  glib2-devel >= 2.22
BuildRequires:  spice-protocol >= 0.12.3
BuildRequires:  celt051-devel
BuildRequires:  pixman-devel alsa-lib-devel openssl-devel libjpeg-devel
%if %{build_client}
BuildRequires:  libXrandr-devel cegui06-devel
%endif
BuildRequires:  libcacard-devel cyrus-sasl-devel
BuildRequires:  pyparsing

%description
The Simple Protocol for Independent Computing Environments (SPICE) is
a remote display system built for virtual environments which allows
you to view a computing 'desktop' environment not only on the machine
where it is running, but from anywhere on the Internet and from a wide
variety of machine architectures.

%description -l zh_CN.UTF-8
SPICE 协议的实现。

%if %{build_client}
%package client
Summary:          Implements the client side of the SPICE protocol
Summary(zh_CN.UTF-8): SPICE 协议的客户端实现
Group:            User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Requires(post):   %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives

%description client
The Simple Protocol for Independent Computing Environments (SPICE) is
a remote display system built for virtual environments which allows
you to view a computing 'desktop' environment not only on the machine
where it is running, but from anywhere on the Internet and from a wide
variety of machine architectures.

This package contains the SPICE client application.
%description client -l zh_CN.UTF-8
SPICE 协议的客户端实现。
%endif


%package server
Summary:        Implements the server side of the SPICE protocol
Summary(zh_CN.UTF-8): SPICE 协议的服务器端实现
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库

%description server
The Simple Protocol for Independent Computing Environments (SPICE) is
a remote display system built for virtual environments which allows
you to view a computing 'desktop' environment not only on the machine
where it is running, but from anywhere on the Internet and from a wide
variety of machine architectures.

This package contains the run-time libraries for any application that wishes
to be a SPICE server.
%description server -l zh_CN.UTF-8
SPICE 协议的服务器端实现。

%package server-devel
Summary:        Header files, libraries and development documentation for spice-server
Summary(zh_CN.UTF-8): %{name}-server 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name}-server = %{version}-%{release}
Requires:       pkgconfig

%description server-devel
This package contains the header files, static libraries and development
documentation for spice-server. If you like to develop programs
using spice-server, you will need to install spice-server-devel.
%description server-devel -l zh_CN.UTF-8
%{name}-server 的开发包。

%prep
%setup -q


%build
%if %{build_client}
%define configure_client --enable-client --enable-gui
%else
%define configure_client --disable-client
%endif
%configure --enable-smartcard %{configure_client}
make %{?_smp_mflags} WARN_CFLAGS='' V=1


%install
make DESTDIR=%{buildroot} install
rm -f %{buildroot}%{_libdir}/libspice-server.a
rm -f %{buildroot}%{_libdir}/libspice-server.la
mkdir -p %{buildroot}%{_libexecdir}

%if %{build_client}
touch %{buildroot}%{_libexecdir}/spice-xpi-client
install -m 0755 %{_sourcedir}/spice-xpi-client-spicec %{buildroot}%{_libexecdir}/
%endif
magic_rpm_clean.sh

%post server -p /sbin/ldconfig

%postun server -p /sbin/ldconfig

%if %{build_client}
%post client
%{_sbindir}/update-alternatives --install %{_libexecdir}/spice-xpi-client \
  spice-xpi-client %{_libexecdir}/spice-xpi-client-spicec 10

%postun client
if [ $1 -eq 0 ] ; then
  %{_sbindir}/update-alternatives --remove spice-xpi-client %{_libexecdir}/spice-xpi-client-spicec
fi
%endif


%if %{build_client}
%files client
%doc COPYING README NEWS
%{_bindir}/spicec
%ghost %{_libexecdir}/spice-xpi-client
%{_libexecdir}/spice-xpi-client-spicec
%endif

%files server
%doc COPYING README NEWS
%{_libdir}/libspice-server.so.1*

%files server-devel
%{_includedir}/spice-server
%{_libdir}/libspice-server.so
%{_libdir}/pkgconfig/spice-server.pc


%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 0.12.6-2
- 更新到 0.12.6

* Mon Sep 28 2015 Liu Di <liudidi@gmail.com> - 0.12.5-1
- 更新到 0.12.5

* Sun May 04 2014 Liu Di <liudidi@gmail.com> - 0.12.2-3
- 为 Magic 3.0 重建

* Fri Dec 21 2012 Adam Tkac <atkac redhat com> - 0.12.2-2
- rebuild against new libjpeg

* Thu Dec 20 2012 Hans de Goede <hdegoede@redhat.com> - 0.12.2-1
- New upstream release 0.12.2

* Fri Sep 28 2012 Hans de Goede <hdegoede@redhat.com> - 0.12.0-1
- New upstream release 0.12.0
- Some minor spec file cleanups
- Enable building on arm

* Thu Sep 6 2012 Soren Sandmann <ssp@redhat.com> - 0.11.3-1
- BuildRequire pyparsing

* Thu Sep 6 2012 Soren Sandmann <ssp@redhat.com> - 0.11.3-1
- Add capability patches
- Add capability patches to the included copy of spice-protocol

    Please see the comment above Patch6 and Patch7
    regarding this situation.

* Thu Sep 6 2012 Soren Sandmann <ssp@redhat.com> - 0.11.3-1
- Update to 0.11.3 and drop upstreamed patches
- BuildRequire spice-protocol 0.12.1

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon May 14 2012 Alon Levy <alevy@redhat.com>
- Fix mjpeg memory leak and bad behavior.
- Add usbredir to list of channels for security purposes. (#819484)

* Sun May 13 2012 Alon Levy <alevy@redhat.com>
- Add double free fix. (#808936)


