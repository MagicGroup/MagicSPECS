%define moduledir %(pkg-config xorg-server --variable=moduledir )
%define sysconfigdir %(pkg-config xorg-server --variable=sysconfigdir )
%define driverdir       %{moduledir}/drivers
#define gitdate 20140503
#define gitrev .%{gitdate}

%undefine _hardened_build

Summary:   Xorg X11 freedreno driver
Summary(zh_CN.UTF-8): Xorg X11 freedreno 显卡驱动
Name:      xorg-x11-drv-freedreno
Version:   1.3.0
Release:   6%{?gitrev}%{?dist}
URL:       http://www.x.org
License:   MIT
Group:     User Interface/X Hardware Support
Group(zh_CN.UTF-8): 用户界面/X 硬件支持

%if 0%{?gitdate}
Source0:    xf86-video-freedreno-%{gitdate}.tar.bz2
%else
Source0:    http://xorg.freedesktop.org/archive/individual/driver/xf86-video-freedreno-%{version}.tar.bz2
%endif
Source2:    make-git-snapshot.sh

ExclusiveArch: %{arm} aarch64

BuildRequires: kernel-headers >= 2.6.32.3
BuildRequires: pkgconfig(libdrm_freedreno)
BuildRequires: pkgconfig(xatracker)
BuildRequires: libudev-devel
BuildRequires: libXext-devel 
BuildRequires: libXrandr-devel 
BuildRequires: libXv-devel
BuildRequires: mesa-libGL-devel >= 6.5-9
BuildRequires: xorg-x11-server-devel >= 1.4.99.1-0.15
BuildRequires: autoconf automake libtool

Requires: Xorg %(xserver-sdk-abi-requires ansic)
Requires: Xorg %(xserver-sdk-abi-requires videodrv)

%description 
X.Org X11 freedreno driver for qualcomm based ARM devices.

%description -l zh_CN.UTF-8
org X11 freedreno 显卡驱动。

%if 0%{?gitdate}
%define dirsuffix %{gitdate}
%else
%define dirsuffix %{version}
%endif

%prep
%setup -q -n xf86-video-freedreno-%{?gitdate:%{gitdate}}%{!?gitdate:%{dirsuffix}}

%build
%{?gitdate:autoreconf -v --install}

%configure --disable-static  --libdir=%{_libdir} --mandir=%{_mandir}
make %{?_smp_mflags} V=1

%install
make install DESTDIR=$RPM_BUILD_ROOT

# FIXME: Remove all libtool archives (*.la) from modules directory.  This
# should be fixed in upstream Makefile.am or whatever.
find $RPM_BUILD_ROOT -regex ".*\.la$" | xargs rm -f --

%files
%doc NEWS
%{driverdir}/freedreno_drv.so
%if 0%{?fedora} >= 20
%{sysconfigdir}/42-freedreno.conf
%endif
%{_mandir}/man4/freedreno.4*

%changelog
* Fri Nov 06 2015 Liu Di <liudidi@gmail.com> - 1.3.0-6
- 为 Magic 3.0 重建

* Wed Jul 29 2015 Dave Airlie <airlied@redhat.com> - 1.3.0-5
- 1.15 ABI rebuild

* Tue Jun 23 2015 Adam Jackson <ajax@redhat.com> - 1.3.0-4
- Undefine _hardened_build

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Feb 11 2015 Hans de Goede <hdegoede@redhat.com> - 1.3.0-2
- xserver 1.17 ABI rebuild

* Wed Oct 22 2014 Rob Clark <robdclark@gmail.com> - 1.3.0-1
- update to 1.3.0

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jul 23 2014 Dennis Gilmore <dennis@ausil.us> - 1.2.0-1
- update to 1.2.0

* Wed Jul  9 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.1.0-5
- Build on aarch64

* Mon Jun 16 2014 Hans de Goede <hdegoede@redhat.com> - 1.1.0-4
- xserver 1.15.99.903 ABI rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat May 17 2014 Dennis Gilmore <dennis@ausil.us> - 1.1.0-2
- enable XA support

* Sat May 17 2014 Dennis Gilmore <dennis@ausil.us> - 1.1.0-1
- update to 1.1.0 release

* Thu May 01 2014 Dennis Gilmore <dennis@ausil.us> - 1.0.0-1.20140503
- initial packaging

