%define tarball xf86-video-ati
%define moduledir %(pkg-config xorg-server --variable=moduledir )
%define driverdir	%{moduledir}/drivers
%define gitdate 20150729
%define gitversion 5510cd6

%undefine _hardened_build

%if 0%{?gitdate}
%define gver .%{gitdate}git%{gitversion}
%endif

Summary:   Xorg X11 ati video driver
Name:      xorg-x11-drv-ati
Version:   7.6.0
Release:   0.4%{?gver}%{?dist}
URL:       http://www.x.org
License:   MIT
Group:     User Interface/X Hardware Support

#Source0:    http://www.x.org/pub/individual/driver/%{tarball}-%{version}.tar.bz2
Source0: %{tarball}-%{gitdate}.tar.xz

Patch10:    radeon-6.12.2-lvds-default-modes.patch
Patch13:    fix-default-modes.patch

ExcludeArch: s390 s390x

BuildRequires: python
BuildRequires: xorg-x11-server-devel >= 1.10.99.902
BuildRequires: mesa-libGL-devel >= 6.4-4
BuildRequires: libdrm-devel >= 2.4.33-1
BuildRequires: kernel-headers >= 2.6.27-0.308
BuildRequires: automake autoconf libtool pkgconfig
BuildRequires: xorg-x11-util-macros >= 1.1.5
BuildRequires: libudev-devel
BuildRequires: xorg-x11-glamor-devel

Requires: Xorg %(xserver-sdk-abi-requires ansic)
Requires: Xorg %(xserver-sdk-abi-requires videodrv)
Requires: libdrm >= 2.4.36-1

%description 
X.Org X11 ati video driver.

%prep
%setup -q -n %{tarball}-%{?gitdate:%{gitdate}}%{?!gitdate:%{version}}
%patch10 -p1 -b .lvds
%patch13 -p1 -b .def

%build
autoreconf -iv
%configure --disable-static --enable-glamor
make %{?_smp_mflags}

%install
%make_install
find $RPM_BUILD_ROOT -regex ".*\.la$" | xargs rm -f --

# these only work in UMS, which is not supported
rm -rf $RPM_BUILD_ROOT%{moduledir}/multimedia/

%files
%{driverdir}/ati_drv.so
%{driverdir}/radeon_drv.so
%{_mandir}/man4/ati.4*
%{_mandir}/man4/radeon.4*

%changelog
* Wed Sep 16 2015 Dave Airlie <airlied@redhat.com> - 7.6.0-0.4.20150729git5510cd6
- 1.18 ABI rebuild

* Wed Jul 29 2015 Dave Airlie <airlied@redhat.com> 7.6.0-0.3.20150729git5510cd6
- git snapshot for new ABI

* Wed Jul 29 2015 Dave Airlie <airlied@redhat.com> - 7.6.0-0.2.20150709git95f5d09
- 1.15 ABI rebuild

* Thu Jul 09 2015 Dave Airlie <airlied@redhat.com> 7.6.0-0.1
- git snapshot of the day.

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Mar 02 2015 Dave Airlie <airlied@redhat.com> 7.5.0-4
- kill hardended builds harder

* Mon Mar 02 2015 Dave Airlie <airlied@redhat.com> 7.5.0-3
- kill hardended builds for X.org

* Wed Feb 11 2015 Hans de Goede <hdegoede@redhat.com> - 7.5.0-2
- xserver 1.17 ABI rebuild

* Fri Oct 10 2014 Adam Jackson <ajax@redhat.com> 7.5.0-1
- ati 7.5.0

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jul 28 2014 Hans de Goede <hdegoede@redhat.com> - 7.4.0-2
- Fix FTBFS with xorg-server-1.16.0

* Wed Jul  2 2014 Hans de Goede <hdegoede@redhat.com> - 7.4.0-1
- Update to 7.4.0 (rhbz#907141)

* Mon Jun 16 2014 Hans de Goede <hdegoede@redhat.com> - 7.4.0-0.4.20140419git48d3dbc
- xserver 1.15.99.903 ABI rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.4.0-0.3.20140419git48d3dbc
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Apr 28 2014 Hans de Goede <hdegoede@redhat.com> - 7.4.0-0.2.20140419git48d3dbc
- xserver 1.15.99-20140428 git snapshot ABI rebuild

* Sat Apr 19 2014 Dave Airlie <airlied@redhat.com> 7.4.0-0.1
- latest upstream git snapshot

* Mon Jan 13 2014 Adam Jackson <ajax@redhat.com> - 7.2.0-7.20131101git3b38701
- 1.15 ABI rebuild

* Tue Dec 17 2013 Adam Jackson <ajax@redhat.com> - 7.2.0-6.20131101git3b38701
- 1.15RC4 ABI rebuild

* Wed Nov 20 2013 Adam Jackson <ajax@redhat.com> - 7.2.0-5.20131101git3b38701
- 1.15RC2 ABI rebuild

* Wed Nov 06 2013 Adam Jackson <ajax@redhat.com> - 7.2.0-4.20131101git3b38701
- 1.15RC1 ABI rebuild

* Fri Nov 01 2013 Jerome Glisse <jglisse@redhat.com> - 7.2.0-3
- Update to lastest upstream git snapshot

* Fri Oct 25 2013 Jerome Glisse <jglisse@redhat.com> - 7.2.0-2
- Fix gnome-shell rendering issue with radeonsi

* Fri Oct 25 2013 Adam Jackson <ajax@redhat.com> - 7.2.0-1
- ABI rebuild

* Thu Aug 29 2013 Dave Airlie <airlied@redhat.com> 7.2.0-0
- update to latest upstream release 7.2.0

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.1.0-6.20130408git6e74aacc5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Apr 11 2013 Jerome Glisse <jglisse@redhat.com> 7.1.0-5
- No need to patch for enabling glamor with git snapshot

* Mon Apr 08 2013 Jerome Glisse <jglisse@redhat.com> 7.1.0-4
- Git snapshot
- Enable glamor acceleration for southern island GPU

* Tue Mar 19 2013 Adam Jackson <ajax@redhat.com> 7.1.0-3
- Less RHEL customization

* Thu Mar 07 2013 Peter Hutterer <peter.hutterer@redhat.com> - 7.1.0-2
- ABI rebuild

* Tue Feb 26 2013 Adam Jackson <ajax@redhat.com> 7.1.0-1
- ati 7.1.0

* Fri Feb 15 2013 Peter Hutterer <peter.hutterer@redhat.com> - 7.0.0-0.10.20121015gitbd9e2c064
- ABI rebuild

* Fri Feb 15 2013 Peter Hutterer <peter.hutterer@redhat.com> - 7.0.0-0.9.20121015gitbd9e2c064
- ABI rebuild

* Thu Nov 15 2012 Jerome Glisse <jglisse@redhat.com> 7.0.0-0.8.20121015gitbd9e2c064
- fix dri2 segfault #872536

* Mon Oct 15 2012 Dave Airlie <airlied@redhat.com> 7.0.0-0.7.20121015gitbd9e2c064
- fix issue with damage when using offload or sw cursor

* Mon Sep 10 2012 Dave Airlie <airlied@redhat.com> 7.0.0-0.6.20120910git7c7f27756
- make sure driver loads on outputless GPUs
