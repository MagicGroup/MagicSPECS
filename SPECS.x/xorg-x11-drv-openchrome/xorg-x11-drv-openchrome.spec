%define tarball xf86-video-openchrome
%define moduledir %(pkg-config xorg-server --variable=moduledir )
%define driverdir %{moduledir}/drivers
#define gitdate 
%define gitversion 131175a71

%if 0%{?gitdate}
%define gver .%{gitdate}git%{gitversion}
%endif

%define with_xvmc 1
%define with_debug 0

Summary:        Xorg X11 openchrome video driver
Summary(zh_CN.UTF-8): Xorg X11 openchrome 显卡驱动
Name:           xorg-x11-drv-openchrome
Version:        0.3.3
Release:        10%{?gver}%{?dist}
URL:            http://www.openchrome.org
License:        MIT
Group:          User Interface/X Hardware Support
Group(zh_CN.UTF-8): 用户界面/X 硬件支持

%if 0%{?gitdate}
Source0:        %{tarball}-%{gitdate}.tar.bz2
%else
Source0:        http://xorg.freedesktop.org/archive/individual/driver/%{tarball}-%{version}.tar.bz2
%endif

# Upstream patches :

# Fedora specific patches :

# Experimental patches (branch backport, etc...): 
Patch13:        openchrome-0.2.904-fix_tvout_flickering.patch

ExclusiveArch:  %{ix86} x86_64

%if 0%{?gitdate}
BuildRequires:  autoconf automake libtool
%endif
BuildRequires:  xorg-x11-server-devel
BuildRequires:  libX11-devel
BuildRequires:  libXext-devel
BuildRequires:  mesa-libGL-devel
%if %{with_xvmc}
BuildRequires:  libXvMC-devel
%endif
BuildRequires:  libdrm-devel >= 2.0-1
Requires:       Xorg %(xserver-sdk-abi-requires ansic)
Requires:       Xorg %(xserver-sdk-abi-requires videodrv)

Obsoletes:      xorg-x11-drv-via <= 0.2.2-4
Provides:       xorg-x11-drv-via = 0.2.2-5


%description 
X.Org X11 openchrome video driver.

%description -l zh_CN.UTF-8
Xorg X11 openchrome 显卡驱动。

%if %{with_xvmc}
%package devel
Summary:        Xorg X11 openchrome video driver XvMC development package
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/System
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name} = %{version}-%{release}
Obsoletes:      xorg-x11-drv-via-devel <= 0.2.2-4
Provides:       xorg-x11-drv-via-devel = 0.2.2-5

%description devel
X.Org X11 openchrome video driver XvMC development package.
%description devel -l zh_CN.UTF-8
%{name} 的开发包。
%endif


%prep
%setup -q -n %{tarball}-%{?gitdate:%{gitdate}}%{?!gitdate:%{version}}


%build
%{?gitdate:autoreconf -v --install}
%configure --disable-static --enable-viaregtool \
%if %{with_debug}
           --enable-debug --enable-xv-debug
%endif

make


%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_datadir}/hwdata/videoaliases

# FIXME: Remove all libtool archives (*.la) from modules directory.  This
# should be fixed in upstream Makefile.am or whatever.
find $RPM_BUILD_ROOT -regex ".*\.la$" | xargs rm -f --


%clean
rm -rf $RPM_BUILD_ROOT


%post
%if %{with_xvmc}
/sbin/ldconfig
%endif
if [ -e /etc/X11/xorg.conf ]; then
    sed -i "/Driver/s/via/openchrome/" /etc/X11/xorg.conf || :
fi

%if %{with_xvmc}
%postun -p /sbin/ldconfig
%endif


%files
%defattr(-,root,root,-)
%doc COPYING NEWS README
%{driverdir}/openchrome_drv.so
%if %{with_xvmc}
%{_libdir}/libchromeXvMC.so.1
%{_libdir}/libchromeXvMC.so.1.0.0
%{_libdir}/libchromeXvMCPro.so.1
%{_libdir}/libchromeXvMCPro.so.1.0.0
%endif
%{_mandir}/man4/openchrome.4.gz
%{_sbindir}/via_regs_dump

%if %{with_xvmc}
%files devel
%defattr(-,root,root,-)
%{_libdir}/libchromeXvMC.so
%{_libdir}/libchromeXvMCPro.so
%endif


%changelog
* Fri Nov 06 2015 Liu Di <liudidi@gmail.com> - 0.3.3-10
- 为 Magic 3.0 重建

* Mon Oct 26 2015 Liu Di <liudidi@gmail.com> - 0.3.3-9
- 为 Magic 3.0 重建

* Mon Jan 13 2014 Adam Jackson <ajax@redhat.com> - 0.3.3-8
- 1.15 ABI rebuild

* Sat Dec 21 2013 Ville Skyttä <ville.skytta@iki.fi> - 0.3.3-7
- Call ldconfig in %%post* scriptlets.
- Fix bogus dates in %%changelog.

* Tue Dec 17 2013 Adam Jackson <ajax@redhat.com> - 0.3.3-6
- 1.15RC4 ABI rebuild

* Wed Nov 20 2013 Adam Jackson <ajax@redhat.com> - 0.3.3-5
- 1.15RC2 ABI rebuild

* Wed Nov 06 2013 Adam Jackson <ajax@redhat.com> - 0.3.3-4
- 1.15RC1 ABI rebuild

* Fri Oct 25 2013 Adam Jackson <ajax@redhat.com> - 0.3.3-3
- ABI rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu May 23 2013 Xavier Bachelot <xavier@bachelot.org> - 0.3.3-1
- Update to 0.3.3 (CVE-2013-1994).

* Wed Mar 27 2013 Xavier Bachelot <xavier@bachelot.org> - 0.3.2-1
- Update to 0.3.2.
- Remove old --enable-dri configure switch.
- Change Source0 URL to fd.o.

* Thu Mar 07 2013 Peter Hutterer <peter.hutterer@redhat.com> - 0.3.1-5
- ABI rebuild

* Fri Feb 15 2013 Peter Hutterer <peter.hutterer@redhat.com> - 0.3.1-4
- ABI rebuild

* Fri Feb 15 2013 Peter Hutterer <peter.hutterer@redhat.com> - 0.3.1-3
- ABI rebuild

* Thu Jan 10 2013 Adam Jackson <ajax@redhat.com> - 0.3.1-2
- ABI rebuild

* Tue Sep 04 2012 Xavier Bachelot <xavier@bachelot.org> - 0.3.1-1
- Update to 0.3.1.

* Sun Aug 05 2012 Xavier Bachelot <xavier@bachelot.org> - 0.3.0-2
- Update to latest snapshot to fix a crash in I2C code with Xserver 1.13.

* Fri Jul 20 2012 Xavier Bachelot <xavier@bachelot.org> - 0.3.0-1
- Update to 0.3.0.
- Install registers dumper tool.

* Fri Jul 20 2012 Dave Airlie <airlied@redhat.com> 0.2.906-2
- temporary git snapshot, to fix deps after X server rebuild

* Wed May 16 2012 Xavier Bachelot <xavier@bachelot.org> - 0.2.906-1
- Update to 0.2.906.

* Thu May 03 2012 Xavier Bachelot <xavier@bachelot.org> - 0.2.905-6
- Fix I420 Xv surface.

* Mon Mar 26 2012 Xavier Bachelot <xavier@bachelot.org> - 0.2.905-5
- Make EXA work out of the box.

* Thu Mar 15 2012 Xavier Bachelot <xavier@bachelot.org> - 0.2.905-4
- Make EXA the default (but disable compositing) (RHBZ#804194).
- Xv support for VX900.

* Sat Feb 11 2012 Peter Hutterer <peter.hutterer@redhat.com> - 0.2.905-3
- ABI rebuild

* Fri Feb 10 2012 Peter Hutterer <peter.hutterer@redhat.com> - 0.2.905-2
- ABI rebuild

* Fri Feb 10 2012 Xavier Bachelot <xavier@bachelot.org> - 0.2.905-1
- Update to 0.2.905.

* Tue Jan 24 2012 Peter Hutterer <peter.hutterer@redhat.com> - 0.2.904-21
- ABI rebuild

* Wed Jan 04 2012 Peter Hutterer <peter.hutterer@redhat.com> 0.2.904-20
- Really drop .xinf

* Wed Jan 04 2012 Peter Hutterer <peter.hutterer@redhat.com> - 0.2.904-19
- Rebuild for server 1.12

* Wed Nov 16 2011 Adam Jackson <ajax@redhat.com> 0.2.904-18
- ABI rebuild
- openchrome-0.2.904-vga.patch: Adapt to videoabi 12

* Sun Sep 11 2011 Xavier Bachelot <xavier@bachelot.org> - 0.2.904-16
- Update to svn933 for bugfixes.

* Thu Aug 18 2011 Adam Jackson <ajax@redhat.com> - 0.2.904-15
- Rebuild for xserver 1.11 ABI

* Sat May 07 2011 Xavier Bachelot <xavier@bachelot.org> - 0.2.904-14
- Bump release.

* Sat May 07 2011 Xavier Bachelot <xavier@bachelot.org> - 0.2.904-13
- Update to svn921 for XO 1.5 regression and Xv crash fix (RHBZ #697901).
- Update I420 patch (RHBZ #674551).

* Thu Mar 03 2011 Xavier Bachelot <xavier@bachelot.org> - 0.2.904-12
- Update to svn916 for VX900 support and bug fixes.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.904-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 02 2010 Adam Jackson <ajax@redhat.com> 0.2.904-10
- Rebuild for new ABI

* Wed Oct 27 2010 Adam Jackson <ajax@redhat.com> 0.2.904-9
- Add ABI requires magic (#542742)

* Mon Jul 05 2010 Peter Hutterer <peter.hutterer@redhat.com> - 0.2.904-8
- rebuild for X Server 1.9

* Thu Jun 10 2010 Xavier Bachelot <xavier@bachelot.org> - 0.2.904-7
- Add upstream fix for a regression with DRI on 64 bits.
- Clean up spec indentation.

* Sat May 08 2010 Xavier Bachelot <xavier@bachelot.org> - 0.2.904-6
- Sync with trunk (r853) and drop patches accordingly.
- Add Xv acceleration for I420 on CME engine.

* Sat Apr 03 2010 Xavier Bachelot <xavier@bachelot.org> - 0.2.904-5.1
- Workaround broken libdrm 2.4.19 Cflags.

* Wed Mar 31 2010 Xavier Bachelot <xavier@bachelot.org> - 0.2.904-5
- Sanitize SaveVideoRegister function.
- Fix an Xv regression on CME chipsets introduced by the VX855 Xv patch.

* Mon Mar 22 2010 Xavier Bachelot <xavier@bachelot.org> - 0.2.904-4
- Fix an Xv regression on VX800 introduced by the VX855 Xv patch.

* Thu Mar 18 2010 Xavier Bachelot <xavier@bachelot.org> - 0.2.904-3
- Sync with trunk (r841) for assorted tweaks and fixes.
- Add VX855 Xv support.
- Fix colorkey on VX8xx.
- Disable DMA and AGP by default on VX8xx.
- Fix TV out flickering regression.
- Add I2CDevices option (needed for XO-1.5).
- Improve PCI 2D performances path.
- Add a guard against HQV engine hang.

* Thu Jan 21 2010 Peter Hutterer <peter.hutterer@redhat.com> - 0.2.904-2
- Rebuild for server 1.8

* Tue Oct 13 2009 Adam Jackson <ajax@redhat.com> 0.2.904-1
- openchrome 0.2.904

* Fri Sep 18 2009 Xavier Bachelot <xavier@bachelot.org> - 0.2.903-16
- Update to latest snapshot (svn 789).
- Drop upstreamed patches.

* Tue Aug 25 2009 Xavier Bachelot <xavier@bachelot.org> - 0.2.903-15
- Add patch for resources/RAC API removal in xserver (RHBZ#516765).

* Thu Jul 30 2009 Xavier Bachelot <xavier@bachelot.org> - 0.2.903-14
- Update to latest snapshot (svn 766) for bugfixes.
- Drop upstreamed patches.
 
* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.903-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jul 18 2009 Xavier Bachelot <xavier@bachelot.org> - 0.2.903-12
- Update to latest snapshot (svn 758) :
  - Basic VX855 support.
  - Fix pci space corruption on P4M900 (RHBZ#506622).
  - Fix null pointer dereference in viaExaCheckComposite (RHBZ#449034).
- Add patch to allow 1200x900 panel (X0-1.5).
- Add patch to remove loader symbol lists, needed for xserver 1.7 (RHBZ#510206).
- Add experimental patch for better VT1625 support.
- Drop upstreamed patches.
 
* Wed Jul 15 2009 Adam Jackson <ajax@redhat.com> - 0.2.903-11.1
- ABI bump

* Thu Jun 18 2009 Xavier Bachelot <xavier@bachelot.org> - 0.2.903-11
- Update to latest snapshot (svn 751) :
  - Add support for VX800 integrated TMDS encoder.
  - Make sure Chrome9 chipsets use software rasterizer for 3D.
  - Various small fixes.
- Add patch for VX855 support.
- Add patch to fix cursor on secondary display.
- Add patch to disable TMDS by default.

* Sat Mar 21 2009 Xavier Bachelot <xavier@bachelot.org> - 0.2.903-10
- Update to latest snapshot (svn 740) :
  - Fix panel resolution detection fallback (RHBZ#491417).
  - Fix 2D engine initialization.
  - Add support for CX700 integrated TMDS encoder.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.903-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 19 2009 Xavier Bachelot <xavier@bachelot.org> - 0.2.903-8
- Update to latest snapshot (svn 735) :
  - Fix green bars after VT switch (RHBZ#469504).
  - Set P4M890 primary FIFO.

* Tue Feb 17 2009 Xavier Bachelot <xavier@bachelot.org> - 0.2.903-7
- Update to latest snapshot (svn 726) :
  - Bug fixes for XAA and EXA.
  - Fix 2d initialization for P4M900.

* Wed Jan 07 2009 Xavier Bachelot <xavier@bachelot.org> - 0.2.903-6
- Fix crash with xserver 1.6 (changeset 712) (RHBZ#479141).

* Mon Jan 05 2009 Xavier Bachelot <xavier@bachelot.org> - 0.2.903-5
- Update to latest snapshot (svn 711) :
  - Fix hardware cursor (RHBZ#465596).
  - Add VX800 Xv.

* Tue Dec 30 2008 Xavier Bachelot <xavier@bachelot.org> - 0.2.903-4
- Fix autoreconf call.

* Mon Dec 29 2008 Xavier Bachelot <xavier@bachelot.org> - 0.2.903-3
- Update to latest snapshot (svn 696), fix RHBZ#446489.
- Make debug build optional and disable it.

* Fri Nov 07 2008 Xavier Bachelot <xavier@bachelot.org> - 0.2.903-2
- Update to latest snapshot (svn 685), most notably add basic VX800 support.
- Turn on full debugging.

* Wed Aug 20 2008 Xavier Bachelot <xavier@bachelot.org> - 0.2.903-1
- Update to 0.2.903.

* Wed Aug 06 2008 Xavier Bachelot <xavier@bachelot.org> - 0.2.902-10
- Disable argb cursor for K8M800.

* Sun Aug 03 2008 Xavier Bachelot <xavier@bachelot.org> - 0.2.902-9
- New version of the panel and hw cursor patch.
- Rawhide is now using patch --fuzz=0, fixes for induced issues.

* Mon Jun 23 2008 Xavier Bachelot <xavier@bachelot.org> - 0.2.902-8
- New version of the panel and hw cursor patch.

* Sat May 31 2008 Xavier Bachelot <xavier@bachelot.org> - 0.2.902-7
- New panel and hardware cursor code from randr branch.

* Sat May 31 2008 Xavier Bachelot <xavier@bachelot.org> - 0.2.902-6
- Disable XvDMA for K8M890 and P4M890 (RHBZ #391621).

* Mon May 26 2008 Xavier Bachelot <xavier@bachelot.org> - 0.2.902-5
- Add patch to fix Xv on LCD for CX700.

* Sun May 25 2008 Xavier Bachelot <xavier@bachelot.org> - 0.2.902-4
- Unbreak ActiveDevice option.

* Thu Apr 17 2008 Xavier Bachelot <xavier@bachelot.org> - 0.2.902-3
- Strip leading /trunk/ from patch #2 and #3.

* Sun Apr 13 2008 Xavier Bachelot <xavier@bachelot.org> - 0.2.902-2
- Add patch to properly report driver version in the libpciaccess code path.
- Add patch to properly report chipset revision in the libpciaccess code path.

* Wed Apr 09 2008 Xavier Bachelot <xavier@bachelot.org> - 0.2.902-1
- New upstream release.
- Re-enable AGPDMA for K8M800 and VM800, as the drm bug is fixed in kernel
  >= 2.6.25rc7 (Patch #1).

* Mon Mar 17 2008 Jesse Keating <jkeating@redhat.com> - 0.2.901-16
- Remove dangerous unversioned obsoletes/provides.

* Sun Mar 16 2008 Xavier Bachelot <xavier@bachelot.org> - 0.2.901-15
- Update to latest svn snapshot (Rev. 553).

* Sun Mar 09 2008 Xavier Bachelot <xavier@bachelot.org> - 0.2.901-14
- Revert to last good version of the libpciaccess patch.

* Sun Mar 09 2008 Xavier Bachelot <xavier@bachelot.org> - 0.2.901-13
- Temporarily revert to old memory detection method. We need something that
  works out of the box for F9 Beta.

* Sat Mar 08 2008 Xavier Bachelot <xavier@bachelot.org> - 0.2.901-12
- Yet another revision of the libpciaccess patch.

* Fri Mar 07 2008 Xavier Bachelot <xavier@bachelot.org> - 0.2.901-11
- Fix a typo in libpciaccess patch.

* Fri Mar 07 2008 Adam Jackson <ajax@redhat.com> 0.2.901-10
- Fix -devel subpackage to obsolete via-devel properly.

* Thu Mar 06 2008 Xavier Bachelot <xavier@bachelot.org> - 0.2.901-9
- Fix libpciaccess patch.

* Thu Mar 06 2008 Xavier Bachelot <xavier@bachelot.org> - 0.2.901-8
- Add patch to fix XV on LCD for VM800.
- Improved libpciaccess patch.

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.2.901-7
- Autorebuild for GCC 4.3

* Wed Jan 23 2008 Xavier Bachelot <xavier@bachelot.org> - 0.2.901-6
- Add patch to properly set fifo on P4M900.

* Sat Jan 19 2008 Xavier Bachelot <xavier@bachelot.org> - 0.2.901-5
- Add patch to replace xf86memcpy by plain memcpy.

* Thu Jan 10 2008 Xavier Bachelot <xavier@bachelot.org> - 0.2.901-4
- Another try at fixing the libpciaccess patch.

* Mon Jan 07 2008 Xavier Bachelot <xavier@bachelot.org> - 0.2.901-3
- And now fix patch filename...

* Mon Jan 07 2008 Xavier Bachelot <xavier@bachelot.org> - 0.2.901-2
- Fix broken libpciaccess patch.

* Wed Jan 02 2008 Xavier Bachelot <xavier@bachelot.org> - 0.2.901-1
- Update to 0.2.901.
- Remove obsoleted patches.
- Update libpciaccess patch.

* Sat Dec 08 2007 Xavier Bachelot <xavier@bachelot.org> - 0.2.900-9
- Add patch for preliminary libpciaccess support.

* Wed Nov 28 2007 Adam Jackson <ajax@redhat.com> 0.2.900-8
- Obsolete xorg-x11-drv-via.  The king is dead, long live the king.
- Munge xorg.conf in %%post to change from via to openchrome.
- Drive-by spec cleanups.

* Fri Nov 02 2007 Xavier Bachelot <xavier@bachelot.org> - 0.2.900-7
- Replace broken VT1625 NTSC patch.
- Add patch to announce as release not as development build.
- First official Fedora build.

* Thu Oct 18 2007 Xavier Bachelot <xavier@bachelot.org> - 0.2.900-6
- Update to official 0.2.900

* Wed Oct 10 2007 Xavier Bachelot <xavier@bachelot.org> - 0.2.900-5
- Update to release_0_3_0 branch rev. 410
- Add VT1625 patch for 720x576 PAL

* Mon Sep 10 2007 Xavier Bachelot <xavier@bachelot.org> - 0.2.900-4
- Update to release_0_3_0 branch rev. 384 plus all changes from experimental
  merged back
- Remove upstream patch #2

* Wed Aug 01 2007 Xavier Bachelot <xavier@bachelot.org> - 0.2.900-3
- Update to release_0_3_0 branch rev. 380 (fix a bug with XvMC acceleration)
- Add a patch to allow proper detection of DDR667 (patch #2)

* Mon Jul 16 2007 Xavier Bachelot <xavier@bachelot.org> - 0.2.900-2
- Update to release_0_3_0 branch rev. 373
- Add release notes to %%doc

* Thu Jul 05 2007 Xavier Bachelot <xavier@bachelot.org> - 0.2.900-1
- Initial build (release_0_3_0 branch rev. 365)
- Add some NTSC modes for the VT1625 (patch #1)
