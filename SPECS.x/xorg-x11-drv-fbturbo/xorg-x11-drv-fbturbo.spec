%define moduledir %(pkg-config xorg-server --variable=moduledir )
%define driverdir %{moduledir}/drivers
%define gitdate 20150221
%define gitrev .%{gitdate}

%undefine _hardened_build

Summary:   Xorg X11 fbturbo driver
Name:      xorg-x11-drv-fbturbo
Version:   0.5.1
Release:   0.6%{?gitrev}%{?dist}
URL:       https://github.com/ssvb/xf86-video-fbturbo
License:   MIT and GPLv2
Group:     User Interface/X Hardware Support

Source0:    xf86-video-fbturbo-%{gitdate}.tar.bz2
Source1:    make-git-snapshot.sh

BuildRequires: kernel-headers
BuildRequires: libdrm-devel
BuildRequires: libudev-devel
BuildRequires: libXext-devel 
BuildRequires: libXrandr-devel 
BuildRequires: libXv-devel
BuildRequires: mesa-libGL-devel
BuildRequires: pixman-devel
BuildRequires: xorg-x11-server-devel
BuildRequires: xorg-x11-util-macros
BuildRequires: autoconf automake libtool
BuildRequires: perl-Carp

Requires: Xorg %(xserver-sdk-abi-requires ansic)
Requires: Xorg %(xserver-sdk-abi-requires videodrv)

ExcludeArch: s390 s390x

%description 
Xorg DDX driver for ARM devices (Allwinner, RPi and others), it's
based on the fbdev driver so will work in all places it does
but has NEON optimised code paths to improve ARM

%if 0%{?gitdate}
%define dirsuffix %{gitdate}
%else
%define dirsuffix %{version}
%endif

%prep
%setup -q -n xf86-video-fbturbo-%{?gitdate:%{gitdate}}%{!?gitdate:%{dirsuffix}} 
touch AUTHORS

%build
%{?gitdate:autoreconf -v --install}

%configure --disable-static  --libdir=%{_libdir} --mandir=%{_mandir}
make %{?_smp_mflags} V=1

%install
make install DESTDIR=%{buildroot}

# Remove libtool archives and static libs
find %{buildroot} -type f -name "*.la" -delete

%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc README
%{driverdir}/fbturbo_drv.so
%{_mandir}/man4/fbturbo.4*

%changelog
* Wed Sep 23 2015 Dave Airlie <airlied@redhat.com> 0.5.1-0.6.20150221
- 1.18 ABI rebuild

* Mon Aug  3 2015 Peter Robinson <pbrobinson@fedoraproject.org> 0.5.1-0.5.20150221
- 1.15 ABI rebuild

* Tue Jun 23 2015 Adam Jackson <ajax@redhat.com> - 0.5.1-0.4.20150221
- Undefine _hardened_build

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-0.3.20150221
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Mar 24 2015 Dan Horák <dan[at]danny.cz> 0.5.1-0.2
- exclude s390(x)

* Sat Feb 21 2015 Peter Robinson <pbrobinson@fedoraproject.org> 0.5.1-0.1
- Initial build
