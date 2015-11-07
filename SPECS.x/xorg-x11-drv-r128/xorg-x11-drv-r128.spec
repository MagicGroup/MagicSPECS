%define tarball xf86-video-r128
%define moduledir %(pkg-config xorg-server --variable=moduledir )
%define driverdir	%{moduledir}/drivers

#global gitdate 20120104
#global gitversion b4892e340

Summary:   Xorg X11 r128 video driver
Summary(zh_CN.UTF-8): Xorg X11 r128 显卡驱动
Name:      xorg-x11-drv-r128
Version:	6.10.0
Release:	3%{?dist}
URL:       http://www.x.org
License:   MIT
Group:     User Interface/X Hardware Support
Group(zh_CN.UTF-8): 用户界面/X 硬件支持

%if 0%{?gitdate}
Source0:    %{tarball}-%{gitdate}.tar.bz2
Source1:    make-git-snapshot.sh
Source2:    commitid
%else
Source0:   http://www.x.org/pub/individual/driver/%{tarball}-%{version}.tar.bz2
%endif

ExcludeArch: s390 s390x %{?rhel:ppc ppc64}

BuildRequires: autoconf automake libtool
BuildRequires: xorg-x11-server-devel >= 1.10.99.902
BuildRequires: mesa-libGL-devel >= 6.4-4
BuildRequires: libdrm-devel >= 2.0-1
BuildRequires: automake autoconf libtool pkgconfig
BuildRequires: xorg-x11-util-macros >= 1.1.5

Requires: Xorg %(xserver-sdk-abi-requires ansic)
Requires: Xorg %(xserver-sdk-abi-requires videodrv)

%description 
X.Org X11 r128 video driver.

%description -l zh_CN.UTF-8
Xorg X11 r128 显卡驱动。

%prep
%setup -q -n %{tarball}-%{?gitdate:%{gitdate}}%{!?gitdate:%{version}}

%build
autoreconf -fisv
%configure --disable-static --disable-dri
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -regex ".*\.la$" | xargs rm -f --

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc README
%{driverdir}/r128_drv.so
%{_mandir}/man4/r128.4*

%changelog
* Fri Nov 06 2015 Liu Di <liudidi@gmail.com> - 6.10.0-3
- 为 Magic 3.0 重建

* Mon Oct 26 2015 Liu Di <liudidi@gmail.com> - 6.10.0-2
- 更新到 6.10.0

* Mon Jan 13 2014 Adam Jackson <ajax@redhat.com> - 6.9.1-11
- 1.15 ABI rebuild

* Tue Dec 17 2013 Adam Jackson <ajax@redhat.com> - 6.9.1-10
- 1.15RC4 ABI rebuild

* Wed Nov 20 2013 Adam Jackson <ajax@redhat.com> - 6.9.1-9
- 1.15RC2 ABI rebuild

* Wed Nov 06 2013 Adam Jackson <ajax@redhat.com> - 6.9.1-8
- 1.15RC1 ABI rebuild

* Fri Oct 25 2013 Adam Jackson <ajax@redhat.com> - 6.9.1-7
- ABI rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.9.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 07 2013 Peter Hutterer <peter.hutterer@redhat.com> - 6.9.1-5
- require xorg-x11-server-devel, not -sdk

* Thu Mar 07 2013 Peter Hutterer <peter.hutterer@redhat.com> - 6.9.1-4
- ABI rebuild

* Fri Feb 15 2013 Peter Hutterer <peter.hutterer@redhat.com> - 6.9.1-3
- ABI rebuild

* Fri Feb 15 2013 Peter Hutterer <peter.hutterer@redhat.com> - 6.9.1-2
- ABI rebuild

* Fri Sep 28 2012 Dave Airlie <airlied@redhat.com> 6.9.1-1
- bump to latest upstream release: add EXA support

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.8.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 18 2012 Dave Airlie <airlied@redhat.com> 6.8.4-1git}
- r128 6.8.4

* Fri Apr 27 2012 Adam Jackson <ajax@redhat.com> 6.8.2-1
- r128 6.8.2

* Thu Apr 05 2012 Adam Jackson <ajax@redhat.com> - 6.8.1-21.20120104gitb4892e340
- RHEL arch exclude updates

* Sat Feb 11 2012 Peter Hutterer <peter.hutterer@redhat.com> - 6.8.1-20.20120104gitb4892e340
- ABI rebuild

* Fri Feb 10 2012 Peter Hutterer <peter.hutterer@redhat.com> - 6.8.1-19.20120104gitb4892e340
- ABI rebuild

* Tue Jan 24 2012 Peter Hutterer <peter.hutterer@redhat.com> - 6.8.1-18.20120104gitb4892e340
- ABI rebuild

* Wed Jan 04 2012 Peter Hutterer <peter.hutterer@redhat.com> 6.8.1-17.20120104.gitb4892e340
- Update to git snapshot
- Add hack to allow building with --disable-dri

* Wed Jan 04 2012 Peter Hutterer <peter.hutterer@redhat.com> - 6.8.1-16
- Rebuild for server 1.12

* Fri Dec 16 2011 Adam Jackson <ajax@redhat.com> - 6.8.1-15
- Drop xinf file

* Thu Nov 17 2011 Adam Jackson <ajax@redhat.com> 6.8.1-14
- Disable DRI1

* Mon Nov 14 2011 Adam Jackson <ajax@redhat.com> - 6.8.1-13
- ABI rebuild

* Wed Nov 09 2011 ajax <ajax@redhat.com> - 6.8.1-12
- ABI rebuild

* Thu Aug 18 2011 Adam Jackson <ajax@redhat.com> - 6.8.1-11
- Rebuild for xserver 1.11 ABI

* Wed May 11 2011 Peter Hutterer <peter.hutterer@redhat.com> - 6.8.1-10
- Rebuild for server 1.11

* Mon Feb 28 2011 Peter Hutterer <peter.hutterer@redhat.com> - 6.8.1-9
- Rebuild for server 1.10

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.8.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 02 2010 Peter Hutterer <peter.hutterer@redhat.com> - 6.8.1-7
- Rebuild for server 1.10

* Wed Oct 27 2010 Adam Jackson <ajax@redhat.com> 6.8.1-6
- Add ABI requires magic (#542742)

* Thu Oct 14 2010 Adam Jackson <ajax@redhat.com> 6.8.1-5
- r128-6.8.1-panel-hack.patch: Use standard CVT instead of CVT-R.

* Mon Jul 05 2010 Peter Hutterer <peter.hutterer@redhat.com> - 6.8.1-4
- rebuild for X Server 1.9

* Thu Jan 21 2010 Peter Hutterer <peter.hutterer@redhat.com> - 6.8.1-3
- Rebuild for server 1.8

* Fri Sep 18 2009 Adam Jackson <ajax@redhat.com> 6.8.1-2
- r128-6.8.1-panel-hack.patch: Set sync ranges based on panel size.

* Tue Aug 04 2009 Dave Airlie <airlied@redhat.com> 6.8.1-1
- r128 6.8.1

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.8.0-4.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 15 2009 Adam Jackson <ajax@redhat.com> - 6.8.0-3.1
- ABI bump

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 22 2008 Dave Airlie <airlied@redhat.com> 6.8.0-2
- rebuild for new server API

* Mon Aug 04 2008 Adam Jackson <ajax@redhat.com> 6.8.0-1
- Initial build of separate r128 driver.

