%global major_ver 1.5
%global minor_ver .3

Summary: Graphics abstraction library for the Linux Framebuffer Device
Name: directfb
Version: %{major_ver}%{minor_ver}
Release: 6%{?dist}
Group: System Environment/Libraries
License: LGPLv2+
URL: http://www.directfb.org/
Source0: http://www.directfb.org/downloads/Core/DirectFB-%{major_ver}/DirectFB-%{version}.tar.gz
Patch0: http://sources.gentoo.org/cgi-bin/viewvc.cgi/gentoo-x86/dev-libs/DirectFB/files/DirectFB-1.4.9-libpng-1.5.patch
Patch1: DirectFB-1.2.8-tweak.patch
Patch2: DirectFB-1.5.3-fix_v4l1.patch
Patch3: DirectFB-1.5.3-lm.patch
Patch4: DirectFB-1.5.3-mips-arm-fix.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

#BuildRequires: libtool

BuildRequires: libpng-devel
BuildRequires: zlib-devel
BuildRequires: libjpeg-devel
BuildRequires: libmng-devel
BuildRequires: freetype-devel
%{?_with_sdl:BuildRequires: SDL-devel}
BuildRequires: libdrm-devel
BuildRequires: libGL-devel
BuildRequires: libGLU-devel
BuildRequires: libsysfs-devel
BuildRequires: libv4l-devel
BuildRequires: libvdpau-devel
BuildRequires: libvncserver-devel
%{?_with_fusion:BuildRequires: linux-fusion-devel}
%{?_with_fusion:Requires: linux-fusion}
BuildRequires: mesa-libEGL-devel
BuildRequires: mesa-libGLES-devel
BuildRequires: tslib-devel


%description
DirectFB is a thin library that provides hardware graphics acceleration,
input device handling and abstraction, integrated windowing system with
support for translucent windows and multiple display layers on top of the
Linux Framebuffer Device.

It is a complete hardware abstraction layer with software fallbacks for
every graphics operation that is not supported by the underlying hardware.
DirectFB adds graphical power to embedded systems and sets a new standard
for graphics under Linux.

Non-default rpmbuild options:
--with fusion:   Enable linux-fusion support
--with sdl:      Enable SDL experimental support


%package devel
Summary: Development files for DirectFB
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig
Requires: zlib-devel
Requires: libsysfs-devel
%{?_with_fusion:Requires: linux-fusion-devel}

%description devel
Development files for DirectFB.


%prep
%setup -q -n DirectFB-%{version}
%patch0 -p1 -b .libpng15
%patch1 -p1 -b .tweak
%patch2 -p1 -b .fix_v4l1
%patch3 -p1 -b .lm
%patch4 -p1 -b .mips-arm-fix

#Disable ppc asm since compilation fails (and it seems better to use glibc)
sed -i.noppcasm -e 's/want_ppcasm=yes/want_ppcasm=no/'g configure.in configure

# Fix file-not-utf8
for i in ChangeLog README NEWS AUTHORS ; do
cp -pr $i $i.not-utf8
iconv -f ISO_8859-1 -t UTF8 $i.not-utf8 > $i
touch -r $i.not-utf8 $i
rm $i.not-utf8
done

#Remove old headers
rm interfaces/IDirectFBVideoProvider/{videodev.h,videodev2.h}



%build
%configure \
%ifarch %{ix86}
    --disable-mmx --disable-sse \
%endif
    --enable-sdl  \
    --enable-zlib \
%{?_with_fusion:--enable-multi} \
    --enable-unique \
    --enable-video4linux2 \
    --disable-vnc \
    --disable-osx \
    --disable-voodoo \
    --enable-mesa \
    --enable-drmkms \
    --without-tests

# Remove rpath for 64bit
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%{__make} %{?_smp_mflags}


%install
%{__rm} -rf %{buildroot}
%{__make} DESTDIR=%{buildroot} install INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

#Fix some relative fonts for dfbinspector.c
ln -s ../fonts/dejavu/DejaVuSans.ttf %{buildroot}%{_datadir}/%{name}-%{version}/decker.ttf


%check
make check

%clean
%{__rm} -rf %{buildroot}



%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog NEWS README TODO
%{_bindir}/dfbfx
%{_bindir}/dfbg
%{_bindir}/dfbdump
%{_bindir}/dfbinfo
%{_bindir}/dfbinput
%{_bindir}/dfblayer
%{_bindir}/dfbpenmount
%{_bindir}/dfbscreen
## new with 1.2.0
%{_bindir}/dfbinspector
## new with 1.2.6
%{_bindir}/dfbmaster
#{_bindir}/dfbsummon
%{_bindir}/mkdfiff
%{_bindir}/mkdgiff
# uwmdump Unique WM
%{_bindir}/uwmdump
## New with 1.4.3
%{_bindir}/coretest_blit2
%{_bindir}/dfbtest_blit2
%{_bindir}/dfbtest_mirror
%{_bindir}/dfbtest_window_flip_once
## New with 1.4.1
%{_bindir}/dfbtest_blit
%{_bindir}/dfbtest_reinit
%{_bindir}/dfbtest_scale
%{_bindir}/dfbtest_sync
%{_bindir}/dfbtest_window
%{_bindir}/direct_stream
%{_bindir}/direct_test
%{_bindir}/fusion_fork
%{_bindir}/fusion_reactor
%{_bindir}/fusion_skirmish
%{_bindir}/fusion_stream
%{_bindir}/pxa3xx_dump
## New with 1.4.11
%{_bindir}/dfbtest_fillrect
%{_bindir}/dfbtest_font
%{_bindir}/fusion_call
%{_bindir}/mkdgifft
#New with 1.5.0
%{_bindir}/dfbtest_init
%{_bindir}/dfbtest_water
%{_bindir}/dfbtest_windows_watcher
%{_bindir}/fluxcomp
%{_bindir}/fusion_call_bench
#New with 1.5.3
%{_bindir}/dfbtest_stereo_window
%{_bindir}/dfbtest_gl1
%{_bindir}/dfbtest_gl2
%{_bindir}/dfbtest_gl3
%{_libdir}/libdirectfb-*.so.*
%{_libdir}/libdirect-*.so.*
%{_libdir}/libfusion-*.so.*
%{_libdir}/libuniquewm*.so.*
%{_libdir}/directfb-%{major_ver}-0/
%{_datadir}/directfb-%{version}/
%{_mandir}/man1/dfbg.1*
%{_mandir}/man5/directfbrc.5*

%files devel
%defattr(-,root,root,-)
%doc docs/html/*.html docs/html/*.png
%exclude %{_bindir}/directfb-config
%{_bindir}/directfb-csource
%{_includedir}/directfb/
%{_includedir}/directfb-internal/
%{_libdir}/pkgconfig/direct.pc
%{_libdir}/pkgconfig/directfb.pc
%{_libdir}/pkgconfig/directfb-internal.pc
%{_libdir}/pkgconfig/fusion.pc
%{_libdir}/libdirectfb.so
%{_libdir}/libdirect.so
%{_libdir}/libfusion.so
%{_libdir}/libuniquewm.so
%{_mandir}/man1/directfb-csource.1*


%changelog
* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 1.5.3-5
- 为 Magic 3.0 重建

* Sat Jan 14 2012 Ville Skyttä <ville.skytta@iki.fi> - 1.5.3-4
- Fix build with libpng 1.5 (patch from Gentoo).

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 1.5.3-2
- Rebuild for new libpng

* Fri Aug 19 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.5.3-1
- Update to 1.5.3
- Add BR libvdpau-devel
- Add BR mesa-{EGL,GLU,GLES}-devel libdrm-devel
- Fix asm on %%{ix86}
- Remove v4l internal headers
- Remove autoreconf call

* Sun Aug 07 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.5.2-1
- Update to 1.5.2

* Sun Jul 17 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.5.1-1
- Update to 1.5.1

* Thu Jul 14 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.5.0-1
- Update to 1.5.0
- Drop not upstreamed libv4l patches

* Wed Nov 24 2010 Nicolas Chauvet <kwizart@gmail.com> - 1.4.11-1
- Update to 1.4.11

* Mon Apr 19 2010 Nicolas Chauvet <kwizart@fedoraproject.org> - 1.4.3-1
- Update to 1.4.3

* Mon Aug 31 2009 kwizart < kwizart at gmail.com > - 1.4.2-3
- Update to 1.4.2
- Add dfbtest_sync and pxa3xx_dump

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 16 2009 kwizart < kwizart at gmail.com > - 1.4.1-1
- Update to 1.4.1

* Mon Jun 30 2009 kwizart < kwizart at gmail.com > - 1.4.0-1
- Update to 1.4.0
- Add BR libGL-devel

* Mon Jun 30 2009 kwizart < kwizart at gmail.com > - 1.2.8-4
- Built with tslib

* Mon May 11 2009 kwizart < kwizart at gmail.com > - 1.2.8-3
- Improve tty patch
- Conditionalize SDL experimental support.

* Thu May  7 2009 kwizart < kwizart at gmail.com > - 1.2.8-2
- Change default tty to tty1

* Tue Apr 21 2009 kwizart < kwizart at gmail.com > - 1.2.8-1
- Update to 1.2.8
- Disable mmx/sse on x86

* Thu Feb 12 2009 kwizart < kwizart at gmail.com > - 1.2.7-3
- Force autoreconf + re tag

* Tue Jan 20 2009 kwizart < kwizart at gmail.com > - 1.2.7-1
- Update to 1.2.7
- Fix decker.ttf path
- Add libv4l2 support
- Fix doc encoding

* Wed Oct 22 2008 kwizart < kwizart at gmail.com > - 1.2.6-3
- Disable the sorelease downgrade
- Exclude directfb-config - Fix multiarch conflicts #341011.

* Mon Oct 20 2008 kwizart < kwizart at gmail.com > - 1.2.6-2
- Disable ppc asm
- Drop the asm/type.h patch (fixed upstream)

* Mon Sep 29 2008 kwizart < kwizart at gmail.com > - 1.2.6-1
- Update to 1.2.6

* Wed Jul 16 2008 kwizart < kwizart at gmail.com > - 1.2.0-1
- Update to 1.2.0 (final)
- Add BR libvncserver-devel
- Enable Unique WM
- Enabled multi (Requires linux-fusion kernel module)

* Sat Jun 21 2008 kwizart < kwizart at gmail.com > - 1.2.0-0.1.rc1
- Update to 1.2.0-rc1

* Sat Jun 21 2008 kwizart < kwizart at gmail.com > - 1.1.1-1
- Update to 1.1.1
- Add --enable-multi 

* Wed Aug 22 2007 Matthias Saou <http://freshrpms.net/> 1.0.0-3
- Rebuild for new BuildID feature.

* Mon Aug  6 2007 Matthias Saou <http://freshrpms.net/> 1.0.0-2
- Update License field.

* Mon Apr  9 2007 Matthias Saou <http://freshrpms.net/> 1.0.0-1
- Update to 1.0.0 final.
- No longer disable MMX on x86_64, it builds again.
- Disable /usr/lib64 rpath on 64bit.

* Fri Feb  2 2007 Matthias Saou <http://freshrpms.net/> 1.0.0-0.1.rc3
- Update to 1.0.0-rc3.

* Wed Jan 17 2007 Matthias Saou <http://freshrpms.net/> 1.0.0-0.1.rc2
- Update to 1.0.0-rc2.
- Include sysfs patch from Eric Moret (#204568).
- Require sysfs devel package in the devel sub-package.
- Spec file cleanup.
- Update asmtypes patch, required to get this rc2 to build.
- Disable MMX on x86_64 since some asm code fails to build otherwise.
- No longer pass an explicit list of drivers to configure since default is all.

* Thu Oct 19 2006 Matthias Saou <http://freshrpms.net/> 1.0.0-0.1.rc1
- Update to 1.0.0-rc1.
- Include the new mkdfiff program (DirectFB Fast Image File Format).

* Thu Sep 14 2006 Matthias Saou <http://freshrpms.net/> 0.9.25.1-3
- FC6 rebuild.
- Remove gcc-c++ build requirement, it's a default now.
- End directory lines in %%files with slashes to identify them more easily.
- Add types patch to fix 64bit build on FC6.
- Add linux-compiler patch to remove obsolete kernel header include.
- Add ppc patch to remove other obsolete kernel header include.

* Sun Jun 09 2006 Warren Togami <wtogami@redhat.com> 0.9.25.1-2
- buildreq sysfsutils-devel became libsysfs-devel

* Sat May 13 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.25.1-1
- new upstream version

* Sun Mar 05 2006 Thomas Vander Stichele <thomas at apestaart dot org> 0.9.24-5
- rebuild for fedora extras 5

* Fri Nov 25 2005 Hans de Goede <j.w.r.degoede@hhs.nl> 0.9.24-4
- Merge FC-4 and devel specfiles for easier maintainance and consistence.
- Incorperate improvements suggested by Ville Skyttä in bug 162358.

* Thu Nov 24 2005 Hans de Goede <j.w.r.degoede@hhs.nl> 0.9.24-3
- Remove "remove custom CFLAGS" patch, this only adds -ffast-math,
  which IMHO is unlikely to be the cause of the build problems, especially
  since a local x86_64 mockbuild works fine. Try to build it hoping that the
  real cause is gone now, since Dan's build did succeed.

* Tue Nov 15 2005 Dan Williams <dcbw@redhat.com> 0.9.24-2
- Try removing custom CFLAGS to see if build makes it through x86_64

* Sun Nov 13 2005 Hans de Goede <j.w.r.degoede@hhs.nl> 0.9.24-1
- 0.9.22 Has build troubles on PPC, upgrade to 0.9.24 which will most
  likely fix this (Only a build will tell for sure).
- Re-enable sis315 since this is fixed in 0.9.24, add r200.

* Mon Oct 17 2005 Hans de Goede <j.w.r.degoede@hhs.nl> 0.9.22-2.fc5
- increase release field to be equal to FC4 release field, to avoid upgrade
  problems.
- force rebuild since directfb is missing from extra-devel repository.

* Thu Jun 30 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.22-2.fc4
- increment release because of new source upload

* Tue Jun 19 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.22-1.fc5
- incorporate changes from Ville
- update to new upstream release

* Wed Jun 15 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.22-1.fc4
- new upstream release
- add libdirect and libfusion shared libraries

* Fri Dec 31 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.21-0.fdr.1
- new upstream release
- added new binaries and libraries
- remove epochs

* Fri Jan 02 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- 0:0.9.20-0.fdr.1: new version

* Sat Sep 13 2003 Thomas Vander Stichele <thomas at apestaart dot org>
- 0:0.9.18-0.fdr.3:
  - readd epochs
  - disable sse, make mmx optional

* Tue Aug 19 2003 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.18-0.fdr.2:
  - incorporated Anvil's suggestions

* Sun Jul 06 2003 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.18-0.fdr.1: initial rpm release
