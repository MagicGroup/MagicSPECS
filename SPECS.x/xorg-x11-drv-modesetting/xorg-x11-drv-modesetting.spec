%global tarball xf86-video-modesetting
%global moduledir %(pkg-config xorg-server --variable=moduledir )
%global driverdir %{moduledir}/drivers

Summary:   Xorg X11 modesetting video driver
Summary(zh_CN.UTF-8): Xorg X11 modesetting 显卡驱动
Name:      xorg-x11-drv-modesetting
Version:	0.9.0
Release:	2%{?dist}
URL:       http://www.x.org
License:   MIT
Group:     User Interface/X Hardware Support
Group(zh_CN.UTF-8): 用户界面/X 硬件支持

Source0:   http://ftp.nara.wide.ad.jp/pub/X11/x.org/individual/driver/%{tarball}-%{version}.tar.bz2

Patch0: 0001-modesetting-change-output-names-for-secondary-GPUs.patch
Patch1: modesetting-0.8.0-xserver-1.15-compat.patch

Patch2: 0001-modesetting-24bpp-are-too-confusing-shadow-our-way-o.patch
Patch3: 0002-add-mga_g200_a-workaround.patch
# all X hw drivers aren't built on s390 - no need for separate bug
ExcludeArch: s390 s390x

BuildRequires: libudev-devel
BuildRequires: xorg-x11-server-devel >= 1.10.99.902
BuildRequires: libX11-devel
BuildRequires: libdrm-devel
BuildRequires: libXext-devel
BuildRequires: libtool automake autoconf

Requires: Xorg %(xserver-sdk-abi-requires ansic)
Requires: Xorg %(xserver-sdk-abi-requires videodrv)

Obsoletes: xorg-x11-drv-ast < 0.97.0-9

%description 
X.Org X11 modesetting video driver - basic modesetting fallback driver.

%description -l zh_CN.UTF-8
Xorg X11 modesetting 显卡驱动。

%prep
%setup -q -n %{tarball}-%{version}
%patch1 -p1 -b .compat

%build
autoreconf -vif
%configure --disable-static
make

%install
make install DESTDIR=$RPM_BUILD_ROOT

# FIXME: Remove all libtool archives (*.la) from modules directory.  This
# should be fixed in upstream Makefile.am or whatever.
find $RPM_BUILD_ROOT -regex ".*\.la$" | xargs rm -f --

%files
%{driverdir}/modesetting_drv.so
%{_mandir}/man4/modesetting.4*
%doc COPYING README

%changelog
* Mon Oct 26 2015 Liu Di <liudidi@gmail.com> - 0.9.0-2
- 更新到 0.9.0

* Thu Jan 23 2014 Dave Airlie <airlied@redhat.com> 0.8.0-11
- add 32 bpp shadow for 24 bpp hw support - add workaround to use this on early mgag200

* Mon Jan 20 2014 Dave Airlie <airlied@redhat.com> 0.8.0-10
- add missing BR for libudev-devel so hotplug works

* Mon Jan 13 2014 Adam Jackson <ajax@redhat.com> - 0.8.0-9
- 1.15 ABI rebuild

* Tue Dec 17 2013 Adam Jackson <ajax@redhat.com> - 0.8.0-8
- 1.15RC4 ABI rebuild

* Wed Nov 20 2013 Adam Jackson <ajax@redhat.com> - 0.8.0-7
- 1.15RC2 ABI rebuild

* Wed Nov 06 2013 Adam Jackson <ajax@redhat.com> - 0.8.0-6
- 1.15RC1 ABI rebuild

* Fri Oct 25 2013 Adam Jackson <ajax@redhat.com> - 0.8.0-5
- ABI rebuild

* Thu Oct 24 2013 Adam Jackson <ajax@redhat.com> - 0.8.0-4
- ABI rebuild

* Thu Oct 24 2013 Adam Jackson <ajax@redhat.com> 0.8.0-3
- API compat for xserver 1.15

* Wed Jul 31 2013 Dave Airlie <airlied@redhat.com> 0.8.0-2
- fix name collisions across multi-gpu

* Thu Jun 13 2013 Dave Airlie <airlied@redhat.com> 0.8.0-1
- latest upstream release - fix SDL resize

* Fri May 10 2013 Adam Jackson <ajax@redhat.com> 0.6.0-7
- Add Obsoletes: for ast everywhere, and mga and cirrus in RHEL, since we
  have KMS drivers for them now.

* Tue Mar 19 2013 Adam Jackson <ajax@redhat.com> 0.6.0-6
- Less RHEL customization

* Thu Mar 07 2013 Peter Hutterer <peter.hutterer@redhat.com> - 0.6.0-5
- require xorg-x11-server-devel, not -sdk

* Thu Mar 07 2013 Peter Hutterer <peter.hutterer@redhat.com> - 0.6.0-4
- ABI rebuild

* Fri Feb 15 2013 Peter Hutterer <peter.hutterer@redhat.com> - 0.6.0-3
- ABI rebuild

* Fri Feb 15 2013 Peter Hutterer <peter.hutterer@redhat.com> - 0.6.0-2
- ABI rebuild

* Wed Jan 09 2013 Adam Jackson <ajax@redhat.com> 0.6.0-1
- modesetting 0.6.0

* Fri Aug 17 2012 Dave Airlie <airlied@redhat.com> 0.4.0-4
- modesetting add prime slave support.

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 18 2012 Dave Airlie <airlied@redhat.com> - 0.4.0-2
- ABI rebuild

* Fri Jun 22 2012 Dave Airlie <airlied@redhat.com> 0.4.0-1
- bump to upstream release 0.4.0

* Fri May 25 2012 Dave Airlie <airlied@redhat.com> 0.3.0-1
- bump to upstream release 0.3.0

* Mon Apr 09 2012 Adam Jackson <ajax@redhat.com> 0.2.0-2
- RHEL arch exclude updates

* Fri Feb 24 2012 Dave Airlie <airlied@redhat.com> 0.2.0-1
- Update to new upstream - fixes pitch issues

* Mon Feb 20 2012 Dave Airlie <airlied@redhat.com> 0.1.0-3
- add build requires, fix tab/space, fix description line

* Mon Feb 20 2012 Dave Airlie <airlied@redhat.com> 0.1.0-2
- initial review comments 1

* Thu Feb 16 2012 Dave Airlie <airlied@redhat.com> 0.1.0-1
- initial import
