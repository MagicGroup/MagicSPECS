%define moduledir %(pkg-config xorg-server --variable=moduledir )
%define driverdir	%{moduledir}/drivers
%define gputoolsdate 20130611
%define gputoolsver 1.9
#define gitdate 20120907
#define gitrev .%{gitdate}

%define prime 1

%ifnarch %{ix86}
%define kmsonly 1
%endif

Summary:   Xorg X11 Intel video driver
Summary(zh_CN.UTF-8): Xorg X11 Intel 显卡驱动
Name:      xorg-x11-drv-intel
Version:	2.99.917
Release:	2%{?dist}
URL:       http://www.x.org
License:   MIT
Group:     User Interface/X Hardware Support
Group(zh_CN.UTF-8): 用户界面/X 硬件支持

%if 0%{?gitdate}
Source0:    xf86-video-intel-%{gitdate}.tar.bz2
%else
Source0:    http://ftp.nara.wide.ad.jp/pub/X11/x.org/individual/driver/xf86-video-intel-%{version}.tar.bz2 
%endif
Source1:    make-intel-gpu-tools-snapshot.sh
Source3:    http://xorg.freedesktop.org/archive/individual/app/intel-gpu-tools-%{gputoolsver}.tar.bz2
#Source3:    intel-gpu-tools-%{gputoolsdate}.tar.bz2
Source4:    make-git-snapshot.sh

Patch1:		fix-sna-fstat-include.patch  
Patch2:		fix-uxa-fstat-include.patch  
Patch3:		fix-yuv-to-rgb-shared-on-intel-gen8.patch

Patch4:		igt-stat.patch

ExclusiveArch: %{ix86} x86_64 ia64

BuildRequires: autoconf automake libtool
BuildRequires: xorg-x11-server-devel >= 1.10.99.902
BuildRequires: libXvMC-devel
BuildRequires: mesa-libGL-devel >= 6.5-9
BuildRequires: libdrm-devel >= 2.4.25
BuildRequires: kernel-headers >= 2.6.32.3
BuildRequires: libudev-devel
BuildRequires: libxcb-devel >= 1.5 
BuildRequires: xcb-util-devel
BuildRequires: cairo-devel

Requires: Xorg %(xserver-sdk-abi-requires ansic)
Requires: Xorg %(xserver-sdk-abi-requires videodrv)

%description 
X.Org X11 Intel video driver.

%description -l zh_CN.UTF-8
Xorg X11 Intel 显卡驱动。

%package devel
Summary:   Xorg X11 Intel video driver XvMC development package
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:     Development/System
Group(zh_CN.UTF-8): 开发/库
Requires:  %{name} = %{version}-%{release}
Provides:  xorg-x11-drv-intel-devel = %{version}-%{release}

%description devel
X.Org X11 Intel video driver XvMC development package.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package -n intel-gpu-tools
Summary:    Debugging tools for Intel graphics chips
Summary(zh_CN.UTF-8): Intel 显卡用的调试工具
Group:	    Development/Tools
Group(zh_CN.UTF-8): 开发/工具

%description -n intel-gpu-tools
Debugging tools for Intel graphics chips

%description -n intel-gpu-tools -l zh_CN.UTF-8
Intel 显卡用的调试工具。

%if 0%{?gitdate}
%define dirsuffix %{gitdate}
%else
%define dirsuffix %{version}
%endif

%prep
%setup -q -n xf86-video-intel-%{?gitdate:%{gitdate}}%{!?gitdate:%{dirsuffix}} -b3
%patch1 -p1
%patch2 -p1
%patch3 -p1

pushd ../intel-gpu-tools-%{gputoolsver}
%patch4 -p1 -b .stat
popd

%build
autoreconf -fisv 
%configure %{?kmsonly:--enable-kms-only} --enable-tools
make %{?_smp_mflags} V=1

pushd ../intel-gpu-tools-%{gputoolsver}
# this is missing from the tarbal, having it empty is ok
touch lib/check-ndebug.h
mkdir -p m4
autoreconf -f -i -v
# --disable-dumper: quick_dump is both not recommended for packaging yet,
# and requires python3 to build; i'd like to keep this spec valid for rhel6
# for at least a bit longer
%configure %{!?prime:--disable-nouveau} --disable-dumper
# some of the sources are in utf-8 and pre-preprocessed by python
export LANG=en_US.UTF-8
make %{?_smp_mflags}
popd

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

pushd ../intel-gpu-tools-%{gputoolsver}
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_bindir}/eudb
popd

find $RPM_BUILD_ROOT -regex ".*\.la$" | xargs rm -f --

# libXvMC opens the versioned file name, these are useless
rm -f $RPM_BUILD_ROOT%{_libdir}/libI*XvMC.so

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc COPYING
%{driverdir}/intel_drv.so
%if !%{?kmsonly}
%{_libdir}/libI810XvMC.so.1*
%endif
%{_libdir}/libIntelXvMC.so.1*
%{_libexecdir}/xf86-video-intel-backlight-helper
%{_datadir}/polkit-1/actions/org.x.xf86-video-intel.backlight-helper.policy
%{_mandir}/man4/i*

%files devel
%{_bindir}/intel-gen4asm
%{_bindir}/intel-gen4disasm
%{_libdir}/pkgconfig/intel-gen4asm.pc

%files -n intel-gpu-tools
%doc COPYING
%{_bindir}/gem_userptr_benchmark
%{_bindir}/intel*
%{_datadir}/gtk-doc
%{_mandir}/man1/intel_*.1*

%changelog
* Mon Oct 26 2015 Liu Di <liudidi@gmail.com> - 2.99.917-2
- 更新到 2.99.917

* Tue May 28 2013 Adam Jackson <ajax@redhat.com> 2.21.8-1
- intel 2.21.8

* Fri Apr 12 2013 Dave Airlie <airlied@redhat.com> 2.21.6-1
- intel 2.21.6

* Thu Mar 21 2013 Adam Jackson <ajax@redhat.com> 2.21.5-1
- intel 2.21.5

* Mon Mar 11 2013 Adam Jackson <ajax@redhat.com> 2.21.4-1
- intel 2.21.4

* Thu Mar 07 2013 Adam Jackson <ajax@redhat.com> 2.21.3-1
- intel 2.21.3

* Thu Mar 07 2013 Peter Hutterer <peter.hutterer@redhat.com> - 2.21.2-4
- ABI rebuild

* Fri Feb 15 2013 Peter Hutterer <peter.hutterer@redhat.com> - 2.21.2-3
- ABI rebuild

* Fri Feb 15 2013 Peter Hutterer <peter.hutterer@redhat.com> - 2.21.2-2
- ABI rebuild

* Tue Feb 12 2013 Adam Jackson <ajax@redhat.com> 2.21.2-1
- intel 2.21.2
- New i-g-t snapshot
- Pre-F16 changelog trim

* Wed Jan 16 2013 Adam Jackson <ajax@redhat.com> 2.20.18-2
- Compensate for rawhide's aclocal breaking in a newly stupid way

* Wed Jan 16 2013 Adam Jackson <ajax@redhat.com> 2.20.18-1
- intel 2.20.18

* Tue Jan 08 2013 Dave Airlie <airlied@redhat.com> 2.20.17-2
- Fix damage issue for reverse prime work

* Fri Jan 04 2013 Adam Jackson <ajax@redhat.com> 2.20.17-1
- intel 2.20.17

* Wed Jan 02 2013 Dave Airlie <airlied@redhat.com> 2.20.16-2
- Fix uxa bug that trips up ilk on 3.7 kernels

* Mon Dec 17 2012 Adam Jackson <ajax@redhat.com> 2.20.16-1
- intel 2.20.16

* Wed Nov 28 2012 Adam Jackson <ajax@redhat.com> 2.20.14-1
- intel 2.20.14

* Mon Oct 22 2012 Adam Jackson <ajax@redhat.com> 2.20.12-1
- intel 2.20.12

* Fri Oct 19 2012 Adam Jackson <ajax@redhat.com> 2.20.10-2
- Today's i-g-t
- Don't bother building the nouveau bits of i-g-t on OSes without an X
  server with prime support.

* Mon Oct 15 2012 Dave Airlie <airlied@redhat.com> 2.20.10-1
- intel 2.20.10

* Fri Oct 05 2012 Adam Jackson <ajax@redhat.com> 2.20.9-1
- intel 2.20.9
- Today's intel-gpu-tools snapshot

* Fri Sep 21 2012 Adam Jackson <ajax@redhat.com> 2.20.8-1
- intel 2.20.8

* Mon Sep 10 2012 Adam Jackson <ajax@redhat.com> 2.20.7-1
- intel 2.20.7

* Fri Sep 07 2012 Dave Airlie <airlied@redhat.com> 2.20.6-2
- latest upstream git snapshot with prime + fixes

* Tue Sep 04 2012 Adam Jackson <ajax@redhat.com> 2.20.6-2
- Only bother to build UMS (read: i810) support on 32-bit.  If you've
  managed to build a machine with an i810 GPU but a 64-bit CPU, please
  don't have done that.

* Tue Sep 04 2012 Adam Jackson <ajax@redhat.com> 2.20.6-1
- intel 2.20.6 (#853783)

* Thu Aug 30 2012 Adam Jackson <ajax@redhat.com> 2.20.5-2
- Don't package I810XvMC when not building legacy i810

* Mon Aug 27 2012 Adam Jackson <ajax@redhat.com> 2.20.5-1
- intel 2.20.5

* Mon Aug 20 2012 Adam Jackson <ajax@redhat.com> 2.20.4-3
- Rebuild for new xcb-util soname

* Mon Aug 20 2012 Adam Jackson <ajax@redhat.com> 2.20.4-2
- Backport some patches to avoid binding to non-i915.ko-driven Intel GPUs,
  like Cedarview and friends (#849475)

* Mon Aug 20 2012 Adam Jackson <ajax@redhat.com> 2.20.4-1
- intel 2.20.4

* Thu Aug 16 2012 Dave Airlie <airlied@redhat.com> 2.20.3-3
- fix vmap flush to correct upstream version in prime patch

* Thu Aug 16 2012 Dave Airlie <airlied@redhat.com> 2.20.3-2
- snapshot upstream + add prime support for now

* Wed Aug 15 2012 Adam Jackson <ajax@redhat.com> 2.20.3-1
- intel 2.20.3

* Wed Aug 01 2012 Adam Jackson <ajax@redhat.com> 2.20.2-1
- intel 2.20.2
- Only disable UMS in RHEL7, since i810 exists in RHEL6

* Mon Jul 23 2012 Adam Jackson <ajax@redhat.com> 2.20.1-1
- intel 2.20.1

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.20.0-2.20120718
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 18 2012 Dave Airlie <airlied@redhat.com> 2.20.0-1.20120718
- todays git snapshot

* Tue Jun 12 2012 Dave Airlie <airlied@redhat.com> 2.19.0-5.20120612
- today's git snapshot
- resurrect copy-fb

* Tue May 29 2012 Adam Jackson <ajax@redhat.com> 2.19.0-4.20120529
- Today's git snapshot
- Enable SNA (default is still UXA, use Option "AccelMethod" to switch)
- build-fix.patch: Fix build with Fedora's default cflags

* Tue May 29 2012 Adam Jackson <ajax@redhat.com> 2.19.0-3
- Don't autoreconf the driver, fixes build on F16.

* Mon May 21 2012 Adam Jackson <ajax@redhat.com> 2.19.0-2
- Disable UMS support in RHEL.
- Trim some Requires that haven't been needed since F15.

* Thu May 03 2012 Adam Jackson <ajax@redhat.com> 2.19.0-1
- intel 2.19.0
