%undefine _hardened_build

Summary:   Xorg X11 opentegra driver
Name:      xorg-x11-drv-opentegra
Version:   0.7.0
Release:   6%{?dist}
URL:       http://cgit.freedesktop.org/xorg/driver/xf86-video-opentegra/
License:   MIT
Group:     User Interface/X Hardware Support

Source0:   http://xorg.freedesktop.org/releases/individual/driver/xf86-video-opentegra-%{version}.tar.xz

ExclusiveArch: %{arm}

BuildRequires: kernel-headers
BuildRequires: pkgconfig(libdrm)
BuildRequires: libudev-devel
BuildRequires: libXrandr-devel
BuildRequires: xorg-x11-server-devel
BuildRequires: xorg-x11-util-macros
BuildRequires: autoconf automake libtool
Requires: Xorg %(xserver-sdk-abi-requires ansic)
Requires: Xorg %(xserver-sdk-abi-requires videodrv)

%description
X.Org X11 opentegra driver for Nvidia Tegra GPUs.

%prep
%setup -q -n xf86-video-opentegra-%{version}

%build
%configure --disable-static
make V=1 %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -regex ".*\.la$" -exec rm -f {} ';'


%files
%doc README COPYING
%{_libdir}/xorg/modules/drivers/opentegra_drv.so
%{_mandir}/man4/*
%if 0%{?fedora} > 20
%{_datadir}/X11/xorg.conf.d/opentegra.conf
%endif

%changelog
* Wed Jul 29 2015 Dave Airlie <airlied@redhat.com> - 0.7.0-6
- 1.15 ABI rebuild

* Tue Jun 23 2015 Adam Jackson <ajax@redhat.com> - 0.7.0-5
- Undefine _hardened_build

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Feb 13 2015 Nicolas Chauvet <kwizart@gmail.com> - 0.7.0-3
- xserver 1.17 ABI rebuild

* Fri Oct 10 2014 Peter Robinson <pbrobinson@fedoraproject.org> 0.7.0-2
- Don't build on aarch64 (all 64 chips are Nouveau based)

* Wed Jul 09 2014 Nicolas Chauvet <kwizart@gmail.com> - 0.7.0-1
- Update to 0.7.0

* Thu Apr 10 2014 Nicolas Chauvet <kwizart@gmail.com> - 0.6.0-1.3
- Updated snapshot

* Wed Apr 24 2013 Jiri Kastner <jkastner@fedoraproject.org> 0.6.0-1
- Initial package
