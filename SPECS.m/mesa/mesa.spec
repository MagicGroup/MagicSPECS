%{!?_licensedir:%global license %%doc}

%define with_private_llvm 0
%define with_wayland 1

# S390 doesn't have video cards, but we need swrast for xserver's GLX
# llvm (and thus llvmpipe) doesn't actually work on ppc32
%ifnarch s390 ppc
%define with_llvm 1
%endif

%define min_wayland_version 1.0
%if 0%{?with_llvm}
%define with_radeonsi 1
%endif

%ifarch s390 s390x ppc
%define with_hardware 0
%define base_drivers swrast
%else
%define with_hardware 1
%define with_vdpau 1
%define with_vaapi 1
%define with_nine 1
%define base_drivers swrast,nouveau,radeon,r200
%endif
%ifarch %{ix86} x86_64
%define platform_drivers ,i915,i965
%define with_ilo    1
%define with_vmware 1
%define with_xa     1
%define with_opencl 1
%define with_omx    1
%endif
%ifarch %{arm} aarch64
%define with_vc4       1
%define with_freedreno 1
%define with_xa        1
%define with_omx       1
%endif

%define dri_drivers --with-dri-drivers=%{?base_drivers}%{?platform_drivers}

%define _default_patch_fuzz 2

%define gitdate 20151122
#% define githash 21ccdbd
%define git %{?githash:%{githash}}%{!?githash:%{gitdate}}

Summary: Mesa graphics libraries
Name: mesa
Version: 11.0.6
Release: 1.%{git}%{?dist}
License: MIT
Group: System Environment/Libraries
URL: http://www.mesa3d.org

Source0: %{name}-%{git}.tar.xz
Source1: Makefile
Source2: vl_decoder.c
Source3: vl_mpeg12_decoder.c

# src/gallium/auxiliary/postprocess/pp_mlaa* have an ... interestingly worded license.
# Source4 contains email correspondence clarifying the license terms.
# Fedora opts to ignore the optional part of clause 2 and treat that code as 2 clause BSD.
Source4: Mesa-MLAA-License-Clarification-Email.txt

Patch15: mesa-9.2-hardware-float.patch
Patch20: mesa-10.2-evergreen-big-endian.patch
Patch30: mesa-10.3-bigendian-assert.patch

# To have sha info in glxinfo
BuildRequires: git

BuildRequires: pkgconfig autoconf automake libtool
%if %{with_hardware}
BuildRequires: kernel-headers
BuildRequires: xorg-x11-server-devel
%endif
BuildRequires: libdrm-devel >= 2.4.42
BuildRequires: libXxf86vm-devel
BuildRequires: expat-devel
BuildRequires: xorg-x11-proto-devel
BuildRequires: makedepend
BuildRequires: libXext-devel
BuildRequires: libXfixes-devel
BuildRequires: libXdamage-devel
BuildRequires: libXi-devel
BuildRequires: libXmu-devel
BuildRequires: libxshmfence-devel
BuildRequires: elfutils
BuildRequires: python
BuildRequires: gettext
%if 0%{?with_llvm}
%if 0%{?with_private_llvm}
BuildRequires: mesa-private-llvm-devel
%else
BuildRequires: llvm-devel >= 3.7
%if 0%{?with_opencl}
BuildRequires: clang-devel >= 3.0
%endif
%endif
%endif
BuildRequires: elfutils-libelf-devel
BuildRequires: libxml2-python
BuildRequires: libudev-devel
BuildRequires: bison flex
%if 0%{?with_wayland}
BuildRequires: pkgconfig(wayland-client) >= %{min_wayland_version}
BuildRequires: pkgconfig(wayland-server) >= %{min_wayland_version}
%endif
BuildRequires: mesa-libGL-devel
%if 0%{?with_vdpau}
BuildRequires: libvdpau-devel
%endif
%if 0%{?with_vaapi}
BuildRequires: libva-devel
%endif
BuildRequires: zlib-devel
%if 0%{?with_omx}
BuildRequires: libomxil-bellagio-devel
%endif
%if 0%{?with_opencl}
BuildRequires: libclc-devel llvm-static opencl-filesystem
%endif
BuildRequires: python-mako

%description
Mesa

%package libGL
Summary: Mesa libGL runtime libraries and DRI drivers
Group: System Environment/Libraries
Provides: libGL

%description libGL
Mesa libGL runtime library.

%package libEGL
Summary: Mesa libEGL runtime libraries
Group: System Environment/Libraries

%description libEGL
Mesa libEGL runtime libraries

%package libGLES
Summary: Mesa libGLES runtime libraries
Group: System Environment/Libraries

%description libGLES
Mesa GLES runtime libraries

%package filesystem
Summary: Mesa driver filesystem
Group: User Interface/X Hardware Support
Provides: mesa-dri-filesystem = %{version}-%{release}
Obsoletes: mesa-dri-filesystem < %{version}-%{release}
%description filesystem
Mesa driver filesystem

%package dri-drivers
Summary: Mesa-based DRI drivers
Group: User Interface/X Hardware Support
Requires: mesa-filesystem%{?_isa}
Obsoletes: mesa-dri-drivers-dri1 < 7.12
Obsoletes: mesa-dri-llvmcore <= 7.12
%description dri-drivers
Mesa-based DRI drivers.

%if 0%{?with_omx}
%package omx-drivers
Summary: Mesa-based OMX drivers
Group: User Interface/X Hardware Support
Requires: mesa-filesystem%{?_isa}
Requires: libomxil-bellagio%{?_isa}
%description omx-drivers
Mesa-based OMX drivers.
%endif

%if 0%{?with_vdpau}
%package vdpau-drivers
Summary: Mesa-based DRI drivers
Group: User Interface/X Hardware Support
Requires: mesa-filesystem%{?_isa}
%description vdpau-drivers
Mesa-based VDPAU drivers.
%endif

%package libGL-devel
Summary: Mesa libGL development package
Group: Development/Libraries
Requires: mesa-libGL = %{version}-%{release}
Requires: gl-manpages
Provides: libGL-devel

%description libGL-devel
Mesa libGL development package

%package libEGL-devel
Summary: Mesa libEGL development package
Group: Development/Libraries
Requires: mesa-libEGL = %{version}-%{release}
Provides: khrplatform-devel = %{version}-%{release}
Obsoletes: khrplatform-devel < %{version}-%{release}

%description libEGL-devel
Mesa libEGL development package

%package libGLES-devel
Summary: Mesa libGLES development package
Group: Development/Libraries
Requires: mesa-libGLES = %{version}-%{release}

%description libGLES-devel
Mesa libGLES development package


%package libOSMesa
Summary: Mesa offscreen rendering libraries
Group: System Environment/Libraries
Provides: libOSMesa

%description libOSMesa
Mesa offscreen rendering libraries


%package libOSMesa-devel
Summary: Mesa offscreen rendering development package
Group: Development/Libraries
Requires: mesa-libOSMesa = %{version}-%{release}

%description libOSMesa-devel
Mesa offscreen rendering development package


%package libgbm
Summary: Mesa gbm library
Group: System Environment/Libraries
Provides: libgbm

%description libgbm
Mesa gbm runtime library.


%package libgbm-devel
Summary: Mesa libgbm development package
Group: Development/Libraries
Requires: mesa-libgbm%{?_isa} = %{version}-%{release}
Provides: libgbm-devel

%description libgbm-devel
Mesa libgbm development package


%if 0%{?with_wayland}
%package libwayland-egl
Summary: Mesa libwayland-egl library
Group: System Environment/Libraries
Provides: libwayland-egl

%description libwayland-egl
Mesa libwayland-egl runtime library.


%package libwayland-egl-devel
Summary: Mesa libwayland-egl development package
Group: Development/Libraries
Requires: mesa-libwayland-egl%{?_isa} = %{version}-%{release}
Provides: libwayland-egl-devel

%description libwayland-egl-devel
Mesa libwayland-egl development package
%endif


%if 0%{?with_xa}
%package libxatracker
Summary: Mesa XA state tracker
Group: System Environment/Libraries
Provides: libxatracker

%description libxatracker
Mesa XA state tracker

%package libxatracker-devel
Summary: Mesa XA state tracker development package
Group: Development/Libraries
Requires: mesa-libxatracker%{?_isa} = %{version}-%{release}
Provides: libxatracker-devel

%description libxatracker-devel
Mesa XA state tracker development package
%endif

%package libglapi
Summary: Mesa shared glapi
Group: System Environment/Libraries

%description libglapi
Mesa shared glapi


%if 0%{?with_opencl}
%package libOpenCL
Summary: Mesa OpenCL runtime library
Requires: ocl-icd
Requires: libclc
Requires: mesa-libgbm = %{version}-%{release}

%description libOpenCL
Mesa OpenCL runtime library.

%package libOpenCL-devel
Summary: Mesa OpenCL development package
Requires: mesa-libOpenCL%{?_isa} = %{version}-%{release}

%description libOpenCL-devel
Mesa OpenCL development package.
%endif

%if 0%{?with_nine}
%package libd3d
Summary: Mesa Direct3D9 state tracker

%description libd3d
Mesa Direct3D9 state tracker

%package libd3d-devel
Summary: Mesa Direct3D9 state tracker development package
Requires: mesa-libd3d%{?_isa} = %{version}-%{release}

%description libd3d-devel
Mesa Direct3D9 state tracker development package
%endif

%prep
#setup -q -n Mesa-%{version}%{?snapshot}
%setup -q -n mesa-%{git}
grep -q ^/ src/gallium/auxiliary/vl/vl_decoder.c && exit 1

%patch15 -p1 -b .hwfloat
%patch20 -p1 -b .egbe
%patch30 -p1 -b .beassert

%if 0%{with_private_llvm}
sed -i 's/llvm-config/mesa-private-llvm-config-%{__isa_bits}/g' configure.ac
sed -i 's/`$LLVM_CONFIG --version`/&-mesa/' configure.ac
%endif

cp %{SOURCE4} docs/

%build

autoreconf --install

export CFLAGS="$RPM_OPT_FLAGS"
# C++ note: we never say "catch" in the source.  we do say "typeid" once,
# in an assert, which is patched out above.  LLVM doesn't use RTTI or throw.
#
# We do say 'catch' in the clover and d3d1x state trackers, but we're not
# building those yet.
export CXXFLAGS="$RPM_OPT_FLAGS %{?with_opencl:-frtti -fexceptions} %{!?with_opencl:-fno-rtti -fno-exceptions}"
%ifarch %{ix86}
# i do not have words for how much the assembly dispatch code infuriates me
%define asm_flags --disable-asm
%endif

%configure \
    %{?asm_flags} \
    --disable-selinux \
    --enable-osmesa \
    --with-dri-driverdir=%{_libdir}/dri \
    --enable-egl \
    --disable-gles1 \
    --enable-gles2 \
    --disable-xvmc \
    %{?with_vdpau:--enable-vdpau} \
    %{?with_vaapi:--enable-va} \
    --with-egl-platforms=x11,drm%{?with_wayland:,wayland} \
    --enable-shared-glapi \
    --enable-gbm \
    %{?with_omx:--enable-omx} \
    %{?with_opencl:--enable-opencl --enable-opencl-icd --with-clang-libdir=%{_prefix}/lib} %{!?with_opencl:--disable-opencl} \
    --enable-glx-tls \
    --enable-texture-float=yes \
    %{?with_llvm:--enable-gallium-llvm} \
    %{?with_llvm:--enable-llvm-shared-libs} \
    --enable-dri \
%if %{with_hardware}
    %{?with_xa:--enable-xa} \
    %{?with_nine:--enable-nine} \
    --with-gallium-drivers=%{?with_vmware:svga,}%{?with_radeonsi:radeonsi,}%{?with_llvm:swrast,r600,}%{?with_freedreno:freedreno,}%{?with_vc4:vc4,}%{?with_ilo:ilo,}r300,nouveau \
%else
    --with-gallium-drivers=%{?with_llvm:swrast} \
%endif
    %{?dri_drivers}

make %{?_smp_mflags} MKDEP=/bin/true

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

%if !%{with_hardware}
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/drirc
%endif

# libvdpau opens the versioned name, don't bother including the unversioned
rm -f $RPM_BUILD_ROOT%{_libdir}/vdpau/*.so

# strip out useless headers
rm -f $RPM_BUILD_ROOT%{_includedir}/GL/w*.h

# remove .la files
find $RPM_BUILD_ROOT -name '*.la' -delete

# this keeps breaking, check it early.  note that the exit from eu-ftr is odd.
pushd $RPM_BUILD_ROOT%{_libdir}
for i in libOSMesa*.so libGL.so ; do
    eu-findtextrel $i && exit 1
done
popd

%clean
rm -rf $RPM_BUILD_ROOT

%check

%post libGL -p /sbin/ldconfig
%postun libGL -p /sbin/ldconfig
%post libOSMesa -p /sbin/ldconfig
%postun libOSMesa -p /sbin/ldconfig
%post libEGL -p /sbin/ldconfig
%postun libEGL -p /sbin/ldconfig
%post libGLES -p /sbin/ldconfig
%postun libGLES -p /sbin/ldconfig
%post libglapi -p /sbin/ldconfig
%postun libglapi -p /sbin/ldconfig
%post libgbm -p /sbin/ldconfig
%postun libgbm -p /sbin/ldconfig
%if 0%{?with_wayland}
%post libwayland-egl -p /sbin/ldconfig
%postun libwayland-egl -p /sbin/ldconfig
%endif
%if 0%{?with_xa}
%post libxatracker -p /sbin/ldconfig
%postun libxatracker -p /sbin/ldconfig
%endif
%if 0%{?with_opencl}
%post libOpenCL -p /sbin/ldconfig
%postun libOpenCL -p /sbin/ldconfig
%endif
%if 0%{?with_nine}
%post libd3d -p /sbin/ldconfig
%postun libd3d -p /sbin/ldconfig
%endif

%files libGL
%defattr(-,root,root,-)
%doc docs/COPYING
%{_libdir}/libGL.so.1
%{_libdir}/libGL.so.1.*

%files libEGL
%defattr(-,root,root,-)
%doc docs/COPYING
%{_libdir}/libEGL.so.1
%{_libdir}/libEGL.so.1.*

%files libGLES
%defattr(-,root,root,-)
%doc docs/COPYING
%{_libdir}/libGLESv2.so.2
%{_libdir}/libGLESv2.so.2.*

%files filesystem
%defattr(-,root,root,-)
%doc docs/COPYING docs/Mesa-MLAA-License-Clarification-Email.txt
%dir %{_libdir}/dri
%if %{with_hardware}
%if 0%{?with_vdpau}
%dir %{_libdir}/vdpau
%endif
%endif

%files libglapi
%{_libdir}/libglapi.so.0
%{_libdir}/libglapi.so.0.*

%files dri-drivers
%defattr(-,root,root,-)
%if %{with_hardware}
%config(noreplace) %{_sysconfdir}/drirc
%if !0%{?rhel}
%{_libdir}/dri/radeon_dri.so
%{_libdir}/dri/r200_dri.so
%{_libdir}/dri/nouveau_vieux_dri.so
%endif
%{_libdir}/dri/r300_dri.so
%if 0%{?with_llvm}
%{_libdir}/dri/r600_dri.so
%if 0%{?with_radeonsi}
%{_libdir}/dri/radeonsi_dri.so
%endif
%endif
%ifarch %{ix86} x86_64
%{_libdir}/dri/i915_dri.so
%{_libdir}/dri/i965_dri.so
%if 0%{?with_ilo}
%{_libdir}/dri/ilo_dri.so
%endif
%endif
%if 0%{?with_vc4}
%{_libdir}/dri/vc4_dri.so
%endif
%if 0%{?with_freedreno}
%{_libdir}/dri/kgsl_dri.so
%{_libdir}/dri/msm_dri.so
%endif
%{_libdir}/dri/nouveau_dri.so
%if 0%{?with_vmware}
%{_libdir}/dri/vmwgfx_dri.so
%endif
%endif
%if 0%{?with_llvm}
%ifarch %{ix86} x86_64
%dir %{_libdir}/gallium-pipe
%{_libdir}/gallium-pipe/*.so
%endif
%{_libdir}/dri/kms_swrast_dri.so
%endif
%{_libdir}/dri/swrast_dri.so
%if 0%{?with_vaapi}
%{_libdir}/dri/gallium_drv_video.so
%endif

%if %{with_hardware}
%if 0%{?with_omx}
%files omx-drivers
%defattr(-,root,root,-)
%{_libdir}/bellagio/libomx_mesa.so
%endif
%if 0%{?with_vdpau}
%files vdpau-drivers
%defattr(-,root,root,-)
%{_libdir}/vdpau/libvdpau_nouveau.so.1*
%{_libdir}/vdpau/libvdpau_r300.so.1*
%if 0%{?with_llvm}
%{_libdir}/vdpau/libvdpau_r600.so.1*
%if 0%{?with_radeonsi}
%{_libdir}/vdpau/libvdpau_radeonsi.so.1*
%endif
%endif
%endif
%endif

%files libGL-devel
%defattr(-,root,root,-)
%{_includedir}/GL/gl.h
%{_includedir}/GL/gl_mangle.h
%{_includedir}/GL/glext.h
%{_includedir}/GL/glx.h
%{_includedir}/GL/glx_mangle.h
%{_includedir}/GL/glxext.h
%{_includedir}/GL/glcorearb.h
%dir %{_includedir}/GL/internal
%{_includedir}/GL/internal/dri_interface.h
%{_libdir}/pkgconfig/dri.pc
%{_libdir}/libGL.so
%{_libdir}/libglapi.so
%{_libdir}/pkgconfig/gl.pc

%files libEGL-devel
%defattr(-,root,root,-)
%dir %{_includedir}/EGL
%{_includedir}/EGL/eglext.h
%{_includedir}/EGL/egl.h
%{_includedir}/EGL/eglmesaext.h
%{_includedir}/EGL/eglplatform.h
%{_includedir}/EGL/eglextchromium.h
%dir %{_includedir}/KHR
%{_includedir}/KHR/khrplatform.h
%{_libdir}/pkgconfig/egl.pc
%{_libdir}/libEGL.so

%files libGLES-devel
%defattr(-,root,root,-)
%dir %{_includedir}/GLES2
%{_includedir}/GLES2/gl2platform.h
%{_includedir}/GLES2/gl2.h
%{_includedir}/GLES2/gl2ext.h
%{_includedir}/GLES3/gl3platform.h
%{_includedir}/GLES3/gl3.h
%{_includedir}/GLES3/gl3ext.h
%{_includedir}/GLES3/gl31.h
%{_libdir}/pkgconfig/glesv2.pc
%{_libdir}/libGLESv2.so

%files libOSMesa
%defattr(-,root,root,-)
%doc docs/COPYING
%{_libdir}/libOSMesa.so.8*

%files libOSMesa-devel
%defattr(-,root,root,-)
%dir %{_includedir}/GL
%{_includedir}/GL/osmesa.h
%{_libdir}/libOSMesa.so
%{_libdir}/pkgconfig/osmesa.pc

%files libgbm
%defattr(-,root,root,-)
%doc docs/COPYING
%{_libdir}/libgbm.so.1
%{_libdir}/libgbm.so.1.*

%files libgbm-devel
%defattr(-,root,root,-)
%{_libdir}/libgbm.so
%{_includedir}/gbm.h
%{_libdir}/pkgconfig/gbm.pc

%if 0%{?with_wayland}
%files libwayland-egl
%defattr(-,root,root,-)
%doc docs/COPYING
%{_libdir}/libwayland-egl.so.1
%{_libdir}/libwayland-egl.so.1.*

%files libwayland-egl-devel
%defattr(-,root,root,-)
%{_libdir}/libwayland-egl.so
%{_libdir}/pkgconfig/wayland-egl.pc
%endif

%if 0%{?with_xa}
%files libxatracker
%defattr(-,root,root,-)
%doc docs/COPYING
%if %{with_hardware}
%{_libdir}/libxatracker.so.2
%{_libdir}/libxatracker.so.2.*
%endif

%files libxatracker-devel
%defattr(-,root,root,-)
%if %{with_hardware}
%{_libdir}/libxatracker.so
%{_includedir}/xa_tracker.h
%{_includedir}/xa_composite.h
%{_includedir}/xa_context.h
%{_libdir}/pkgconfig/xatracker.pc
%endif
%endif

%if 0%{?with_opencl}
%files libOpenCL
%{_libdir}/libMesaOpenCL.so.*
%{_sysconfdir}/OpenCL/vendors/mesa.icd

%files libOpenCL-devel
%{_libdir}/libMesaOpenCL.so
%endif

%if 0%{?with_nine}
%files libd3d
%dir %{_libdir}/d3d/
%{_libdir}/d3d/*.so.*

%files libd3d-devel
%{_libdir}/pkgconfig/d3d.pc
%{_includedir}/d3dadapter/
%{_libdir}/d3d/*.so
%endif

%changelog
* Thu Nov 26 2015 Liu Di <liudidi@gmail.com> - 10.6.3-5.20150729
- 为 Magic 3.0 重建

* Tue Nov 10 2015 Liu Di <liudidi@gmail.com> - 10.6.3-4.20150729
- 为 Magic 3.0 重建

* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 10.6.3-3.20150729
- 为 Magic 3.0 重建

* Mon Sep 07 2015 Liu Di <liudidi@gmail.com> - 10.6.3-2.20150729
- 为 Magic 3.0 重建

* Wed Jul 29 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.6.3-1.20150729
- 10.6.3

* Sat Jul 11 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.6.2-1.20150711
- 10.6.2

* Mon Jun 29 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.6.1-1.20150629
- 10.6.1

* Thu Jun 18 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.6.0-1
- 10.6.0

* Mon Jun 08 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.5.7-1.20150608
- 10.5.7

* Tue May 05 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.5.4-1.20150505
- 10.5.4

* Mon Apr 20 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.5.3-1.20150420
- 10.5.3

* Sat Mar 14 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.5.1-1.20150314
- 10.5.1

* Sun Mar 08 2015 Kalev Lember <kalevlember@gmail.com> - 10.5.0-2.20150218
- Backport a patch fixing partially transparent screenshots (fdo#89292)

* Wed Feb 18 2015 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 10.5.0-1.20150218
- 10.5.0

* Fri Jan 02 2015 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 10.5.0-0.devel.32.6171131
- 6171131

* Fri Jan 02 2015 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 10.5.0-0.devel.31.c3260f8
- c3260f8

* Fri Jan 02 2015 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 10.5.0-0.devel.30.290553b
- 290553b

* Thu Jan 01 2015 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 10.5.0-0.devel.28.b77eaaf
- b77eaaf

* Thu Jan 01 2015 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 10.5.0-0.devel.26.c633528
- c633528

* Thu Jan 01 2015 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 10.5.0-0.devel.25.a6f6d61
- a6f6d61

* Wed Dec 31 2014 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 10.5.0-0.devel.23.be0311c
- be0311c

* Wed Dec 31 2014 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 10.5.0-0.devel.21.609c3e5
- 609c3e5

* Wed Dec 31 2014 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 10.5.0-0.devel.19.3ba57ba
- 3ba57ba

* Tue Dec 30 2014 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 10.5.0-0.devel.17.64dcb2b
- 64dcb2b

* Mon Dec 29 2014 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 10.5.0-0.devel.15.6c18279
- 6c18279

* Sat Dec 27 2014 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 10.5.0-0.devel.13.0c7f895
- 0c7f895

* Fri Dec 26 2014 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 10.5.0-0.devel.11.cb5a372
- cb5a372

* Sun Dec 21 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.5.0-0.devel.10.git0d7f4c8
- enable ilo gallium driver

* Fri Dec 19 2014 Dan Horák <dan[at]danny.cz> 10.5.0-0.devel.9
- Sync with_{vaapi,vdpau,nine} settings with F21

* Thu Dec 18 2014 Adam Jackson <ajax@redhat.com> 10.5.0-0.devel.8
- Sync ppc build config with F21

* Wed Dec 17 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.5.0-0.devel.7.git0d7f4c8
- fix requirements for d3d

* Sun Dec 14 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.5.0-0.devel.6.git0d7f4c8
- 0d7f4c8

* Sun Dec 14 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.5.0-0.devel.5.git29c7cf2
- Enable VA state-tracker
- Enable Nine state-tracker (Direct3D9 API)

* Thu Dec 11 2014 Adam Jackson <ajax@redhat.com> 10.5.0-0.devel.4
- Restore hardware drivers on ppc64{,le}

* Tue Dec 02 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.5.0-0.devel.3.git29c7cf2
- 29c7cf2

* Sat Nov 22 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.5.0-0.devel.2.git3d9c1a9
- 3d9c1a9

* Wed Nov 19 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.5.0-0.devel.1.git9460cd3
- 9460cd3

* Mon Nov 10 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.4-0.devel.8.gitf3b709c
- f3b709c

* Tue Oct 28 2014  10.4-0.devel.7.git1a17098
- rebuild for llvm

* Mon Oct 27 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.4-0.devel.6.git1a17098
- 1a17098

* Sat Sep 27 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.4-0.devel.5.gitc3f17bb
- c3f17bb18f597d7f606805ae94363dae7fd51582

* Sat Sep 06 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.4-0.devel.4.git1f184bc
- apply patch for bigendian from karsten
- fix ppc filelist from karsten

* Sat Sep 06 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.4-0.devel.3.git1f184bc
- 1f184bc114143acbcea373184260da777b6c6be1 commit

* Thu Aug 28 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.4-0.devel.2.1.80771e47b6c1e47ab55f17311e1d4e227a9eb3d8
- add swrast to dri driver list

* Wed Aug 27 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.4-0.devel.2.80771e47b6c1e47ab55f17311e1d4e227a9eb3d8
- 80771e47b6c1e47ab55f17311e1d4e227a9eb3d8 commit

* Sat Aug 23 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.4-0.devel.1.c2867f5b3626157379ef0d4d5bcaf5180ca0ec1f
- 10.4 c2867f5b3626157379ef0d4d5bcaf5180ca0ec1f

* Fri Aug 22 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.3-0.rc1.1.e7f2f2dea5acdbd1a12ed88914e64a38a97432f0
- e7f2f2dea5acdbd1a12ed88914e64a38a97432f0 commit

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10.3-0.devel.2.c40d7d6d948912a4d51cbf8f0854cf2ebe916636.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Aug 06 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.3-0.devel.2.c40d7d6d948912a4d51cbf8f0854cf2ebe916636
- c40d7d6d948912a4d51cbf8f0854cf2ebe916636 commit

* Fri Jul 11 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.3-0.devel.1.f381c27c548aa28b003c8e188f5d627ab4105f76
- Rebase to 'master' branch (f381c27c548aa28b003c8e188f5d627ab4105f76 commit)

* Fri Jul 11 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.2.3-1.20140711
- 10.2.3 upstream release

* Mon Jul  7 2014 Peter Robinson <pbrobinson@fedoraproject.org> 10.2.2-4.20140625
- Build aarch64 options the same as ARMv7
- Fix PPC conditionals

* Fri Jul 04 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.2.2-3.20140625
- Fix up intelInitScreen2 for DRI3 (RHBZ #1115323) (patch from drago01)

* Fri Jun 27 2014 Dave Airlie <airlied@redhat.com> 10.2.2-2.20140625
- add dri3 gnome-shell startup fix from Jasper.

* Wed Jun 25 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.2.2-1.20140625
- 10.2.2 upstream release

* Wed Jun 11 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.2.1-2.20140608
- drop radeonsi llvm hack

* Sun Jun 08 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.2.1-1.20140608
- 10.2.1 upstream release

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10.2-0.11.rc5.20140531
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Jun 04 2014 Dan Horák <dan[at]danny.cz> - 10.2-0.10.rc5.20140531
- fix build without hardware drivers

* Sat May 31 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.2-0.9.rc5.20140531
- 10.2-rc5 upstream release

* Wed May 28 2014 Brent Baude <baude@us.ibm.com> - 10.2-0.8.rc4.20140524
- Removing ppc64le arch from with_llvm

* Wed May 28 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.2-0.7.rc4.20140524
- i915: add a missing NULL pointer check (RHBZ #1100967)

* Sat May 24 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.2-0.6.rc4.20140524
- 10.2-rc4 upstream release
- add back updated radeonsi hack for LLVM

* Sat May 17 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.2-0.5.rc3.20140517
- 10.2-rc3 upstream release

* Sat May 10 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.2-0.4.rc2.20140510
- 10.2-rc2 upstream release
- drop radeonsi hack for LLVM

* Tue May 06 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.2-0.3.rc1.20140505
- Move gallium-pipe to the correct sub-package (RHBZ #1094588) (kwizart)
- Move egl_gallium.so to the correct location (RHBZ #1094588) (kwizart)
- Switch from with to enable for llvm shared libs (kwizart)

* Mon May 05 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.2-0.2.rc1.20140505
- Enable gallium-egl (needed by freedreeno) (RHBZ #1094199) (kwizart)

* Mon May 05 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.2-0.1.rc1.20140505
- Enable omx on x86 and arm (RHBZ #1094199) (kwizart)
- Split _with_xa from _with_vmware (RHBZ #1094199) (kwizart)
- Add _with_xa when arch is arm and _with_freedreeno (RHBZ #1094199) (kwizart)

* Mon May 05 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.2-0.rc1.20140505
- 10.2-rc1 upstream release

* Wed Apr 30 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.1.1-3.20140430
- Update to today snapshot
- apply as downstream patches for reporting GPU max frequency on r600 (FD.o #73511)

* Sat Apr 19 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.1.1-2.20140419
- fix buildrequires llvm 3.4-5 to 3.4-6, because 3.4-5 is not available for F20

* Sat Apr 19 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.1.1-1.20140419
- 10.1.1 upstream release

* Tue Apr 15 2014 Adam Jackson <ajax@redhat.com> 10.1-6.20140305
- Disable DRI3 in F20, it requires libxcb bits we haven't backported.

* Wed Mar 26 2014 Adam Jackson <ajax@redhat.com> 10.1-5.20140305
- Initial ppc64le enablement (no hardware drivers or vdpau yet)

* Fri Mar 21 2014 Adam Jackson <ajax@redhat.com> 10.1-4.20140305
- mesa: Don't optimize out glClear if drawbuffer size is 0x0 (fdo #75797)

* Wed Mar 19 2014 Dave Airlie <airlied@redhat.com> 10.1-3.20140305
- rebuild against backported llvm 3.4-5 for radeonsi GL 3.3 support.

* Wed Mar 12 2014 Dave Airlie <airlied@redhat.com> 10.1-2.20140305
- disable r600 llvm compiler (upstream advice)

* Wed Mar 05 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.1-1.20140305
- mesa: Bump version to 10.1 (final) (Ian Romanick)
- glx/dri2: fix build failure on HURD (Julien Cristau)
- i965: Validate (and resolve) all the bound textures. (Chris Forbes)
- i965: Widen sampler key bitfields for 32 samplers (Chris Forbes)

* Sat Mar 01 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.1-0.rc3.20140301
- 10.1-rc3

* Tue Feb 25 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.1-0.rc2.20140225
- really 10.1-rc2

* Sat Feb 22 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.1-0.rc2.20140222
- 10.1-rc2

* Sat Feb 08 2014 Adel Gadllah <adel.gadllah@gmail.com> - 10.1-0.rc1.20140208
- 10.1rc1
- Drop upstreamed patches

* Thu Feb 06 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.0.3-1.20140206
- 10.0.3 upstream release

* Tue Feb 04 2014 Kyle McMartin <kyle@redhat.com> - 10.0.2-6.20140118
- Fix accidentally inverted logic that meant radeonsi_dri.so went missing
  on all architectures instead of just ppc and s390. Sorry!

* Sun Feb 02 2014 Kyle McMartin <kyle@redhat.com> - 10.0.2-5.20140118
- Fix a thinko in previous commit wrt libdrm_nouveau2.

* Sun Feb 02 2014 Kyle McMartin <kyle@redhat.com> - 10.0.2-4.20140118
- Fix up building drivers on AArch64, enable LLVM there.
- Eliminate some F17 cruft from the spec, since we don't support it anymore.
- Conditionalize with_radeonsi on with_llvm instead of ppc,s390 && >F-17.
- Conditionalize libvdpau_radeonsi.so.1* on with_radeonsi instead of simply
  with_llvm to fix a build failure on AArch64.

* Sun Jan 19 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.0.2-3.20140118
- Enable OpenCL (RHBZ #887628)
- Enable r600 llvm compiler (RHBZ #1055098)

* Fri Dec 20 2013 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 9.2.5-1.20131220
- 9.2.5 upstream release

* Fri Dec 13 2013 Dave Airlie <airlied@redhat.com> 9.2.4-2.20131128
- backport the GLX_MESA_copy_sub_buffer from upstream for cogl

* Thu Nov 28 2013 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 9.2.4-1.20131128
- 9.2.4 upstream release

* Thu Nov 14 2013 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 9.2.3-1.20131114
- 9.2.3 upstream release

* Wed Nov 13 2013 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 9.2.2-1.20131113
- 9.2.2 upstream release + fixes from git 9.2 branch

* Thu Sep 19 2013 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 9.2-1.20130919
- Today's git snap of 9.2 branch
- [NVE4] Fix crashing games when set AA to x2 on GTX760
- (freedesktop 68665 rhbz 1001714 1001698 1001740 1004674)

* Mon Sep 02 2013 Dave Airlie <airlied@redhat.com> 9.2-1.20130902
- 9.2 upstream release + fixes from git branch

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.2-0.15.20130723
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 23 2013 Adam Jackson <ajax@redhat.com> 9.2-0.14.20130723
- Today's git snap of 9.2 branch

* Sun Jul 14 2013 Kyle McMartin <kyle@redhat.com> 9.2-0.13.20130610
- Use LLVM::MCJIT on ARM and AArch64.

* Mon Jun 17 2013 Adam Jackson <ajax@redhat.com> 9.2-0.12.20130610
- Re-enable hardware float support (#975204)

* Mon Jun 17 2013 Adam Jackson <ajax@redhat.com> 9.2-0.11.20130610
- Fix evergreen on big-endian

* Wed Jun 12 2013 Adam Jackson <ajax@redhat.com> 9.2-0.10.20130610
- Fix s390x build
- Fold khrplatform-devel in to libEGL-devel

* Tue Jun 11 2013 Adam Jackson <ajax@redhat.com> 9.2-0.9.20130610
- 0001-Revert-i965-Disable-unused-pipeline-stages-once-at-s.patch: Fix some
  hangs on ivb+

* Mon Jun 10 2013 Adam Jackson <ajax@redhat.com> 9.2-0.8.20130610
- Today's git snap

* Tue May 28 2013 Adam Jackson <ajax@redhat.com> 9.2-0.7.20130528
- Today's git snap

* Sun May 19 2013 Peter Robinson <pbrobinson@fedoraproject.org> 9.2-0.6.20130514
- Update the name of the freedreno driver

* Fri May 17 2013 Adam Jackson <ajax@redhat.com> 9.2-0.5.20130514
- Fix build issues on ppc32

* Thu May 16 2013 Adam Jackson <ajax@redhat.com> 9.2-0.4.20130514
- Fix yet more build issues on s390{,x}

* Wed May 15 2013 Adam Jackson <ajax@redhat.com> 9.2-0.3.20130514
- Fix build ordering issue on s390x

* Wed May 15 2013 Adam Jackson <ajax@redhat.com> 9.2-0.2.20130514
- Fix filesystem for with_hardware == 0

* Tue May 14 2013 Adam Jackson <ajax@redhat.com> 9.2-0.1.20130514
- Today's git snap
- Revert to swrast on ppc32 and s390 since llvm doesn't actually work
- Build freedreno on arm
- Drop snb hang workaround (upstream 1dfea559)
- Rename filesystem package

* Wed May 08 2013 Adam Jackson <ajax@redhat.com> 9.2-0.1.20130508
- Switch to Mesa master (pre 9.2)
- Fix llvmpipe on big-endian and enable llvmpipe everywhere
- Build vdpau drivers for r600/radeonsi/nouveau
- Enable hardware floating-point texture support
- Drop GLESv1, nothing's using it, let's not start

* Sat Apr 27 2013 Dave Airlie <airlied@redhat.com> 9.1.1-1
- rebase to Mesa 9.1.1 + fixes from git

* Thu Apr 11 2013 Dave Airlie <airlied@redhat.com> 9.1-6
- enable glx tls for glamor to work properly

* Thu Apr 04 2013 Adam Jackson <ajax@redhat.com> 9.1-5
- Enable llvmpipe even on non-SSE2 machines (#909473)

* Tue Mar 26 2013 Adam Jackson <ajax@redhat.com> 9.1-4
- Fix build with private LLVM

* Tue Mar 19 2013 Adam Jackson <ajax@redhat.com> 9.1-3
- mesa-9.1-53-gd0ccb5b.patch: Sync with today's git

* Tue Mar 19 2013 Dave Airlie <airlied@redhat.com> 9.1-2
- add SNB hang workaround from chromium

* Fri Mar 08 2013 Adam Jackson <ajax@redhat.com> 9.1-1
- Mesa 9.1

* Wed Feb 27 2013 Dan Horák <dan[at]danny.cz> - 9.1-0.4
- /etc/drirc is always created, so exclude it on platforms without hw drivers

* Tue Feb 26 2013 Adam Jackson <ajax@redhat.com> 9.1-0.3
- Fix s390*'s swrast to be classic not softpipe

* Tue Feb 19 2013 Jens Petersen <petersen@redhat.com> - 9.1-0.2
- build against llvm-3.2
- turn on radeonsi

* Wed Feb 13 2013 Dave Airlie <airlied@redhat.com> 9.1-0.1
- snapshot mesa 9.1 branch

* Tue Jan 15 2013 Tom Callaway <spot@fedoraproject.org> 9.0.1-4
- clarify license on pp_mlaa* files

* Thu Dec 20 2012 Adam Jackson <ajax@redhat.com> 9.0.1-3
- mesa-9.0.1-22-gd0a9ab2.patch: Sync with git
- Build with -fno-rtti -fno-exceptions, modest size and speed win
- mesa-9.0.1-less-cxx-please.patch: Remove the only use of typeid() so the
  above works.

* Wed Dec 05 2012 Adam Jackson <ajax@redhat.com> 9.0.1-2
- Allow linking against a private version of LLVM libs for RHEL7
- Build with -j again

* Mon Dec 03 2012 Adam Jackson <ajax@redhat.com> 9.0.1-1
- Mesa 9.0.1

* Wed Nov 07 2012 Dave Airlie <airlied@redhat.com> 9.0-5
- mesa-9.0-19-g895a587.patch: sync with 9.0 branch with git
- drop wayland patch its in git now.

* Thu Nov 01 2012 Adam Jackson <ajax@redhat.com> 9.0-4
- mesa-9.0-18-g5fe5aa8: sync with 9.0 branch in git
- Portability fixes for F17: old wayland, old llvm.

* Sat Oct 27 2012 Dan Horák <dan[at]danny.cz> 9.0-3
- gallium drivers must be set explicitely for s390(x) otherwise also r300, r600 and vmwgfx are built

* Fri Oct 19 2012 Adam Jackson <ajax@redhat.com> 9.0-2
- Rebuild for wayland 0.99

* Wed Oct 10 2012 Adam Jackson <ajax@redhat.com> 9.0-1
- Mesa 9.0
- mesa-9.0-12-gd56ee24.patch: sync with 9.0 branch in git

* Wed Oct 10 2012 Adam Jackson <ajax@redhat.com> 9.0-0.4
- Switch to external gl-manpages and libGLU
- Drop ShmGetImage fastpath for a bit

* Mon Oct 01 2012 Dan Horák <dan[at]danny.cz> 9.0-0.3
- explicit BR: libGL-devel is required on s390(x), it's probbaly brought in indirectly on x86
- gallium drivers must be set explicitely for s390(x) otherwise also r300, r600 and vmwgfx are built

* Mon Sep 24 2012 Adam Jackson <ajax@redhat.com> 9.0-0.2
- Switch to swrast classic instead of softpipe for non-llvm arches
- Re-disable llvm on ppc until it can draw pixels

* Mon Sep 24 2012 Dave Airlie <airlied@redhat.com> 9.0-0.1
- rebase to latest upstream 9.0 pre-release branch
- add back glu from new upstream (split for f18 later)

* Fri Sep 14 2012 Dave Airlie <airlied@redhat.com> 8.1-0.21
- why fix one yylex when you can fix two

* Fri Sep 14 2012 Dave Airlie <airlied@redhat.com> 8.1-0.20
- fix yylex collision reported on irc by hughsie

* Mon Aug 27 2012 Adam Jackson <ajax@redhat.com> 8.1-0.19
- Today's git snap
- Revert dependency on libkms
- Patch from Mageia to fix some undefined symbols

* Fri Aug 17 2012 Dave Airlie <airlied@redhat.com> 8.1-0.18
- parallel make seems broken - on 16 way machine internally.

* Thu Aug 16 2012 Dave Airlie <airlied@redhat.com> 8.1-0.17
- upstream snapshot

* Wed Jul 25 2012 Peter Robinson <pbrobinson@fedoraproject.org> 8.1-0.16
- Enable LLVM on ARM

* Wed Jul 25 2012 Peter Robinson <pbrobinson@fedoraproject.org> 8.1-0.15
- Fix building on platforms with HW and without LLVM

* Tue Jul 24 2012 Adam Jackson <ajax@redhat.com> 8.1-0.14
- Re-enable llvm on ppc, being worked on
- Don't BuildReq on wayland things in RHEL

* Mon Jul 23 2012 Adam Jackson <ajax@redhat.com> 8.1-0.13
- Build radeonsi (#842194)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.1-0.12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 17 2012 Dave Airlie <airlied@redhat.com> 8.1-0.11
- upstream snapshot: fixes build issues

* Tue Jul 17 2012 Dave Airlie <airlied@redhat.com> 8.1-0.10
- snapshot mesa: add some build hackarounds 

* Sat Jul 14 2012 Ville Skyttä <ville.skytta@iki.fi> - 8.1-0.9
- Call ldconfig at -libglapi and -libxatracker post(un)install time.
- Drop redundant ldconfig dependencies, let rpm auto-add them.

* Wed Jun 13 2012 Dave Airlie <airlied@redhat.com> 8.1-0.8
- enable shared llvm usage.

* Thu Jun 07 2012 Adam Jackson <ajax@redhat.com> 8.1-0.7
- Disable llvm on non-x86 (#829020)

* Sun Jun 03 2012 Dave Airlie <airlied@redhat.com> 8.1-0.6
- rebase to git master + build on top of llvm 3.1

* Thu May 17 2012 Adam Jackson <ajax@redhat.com> 8.1-0.5
- mesa-8.0-llvmpipe-shmget.patch: Rediff for 8.1.

* Thu May 10 2012 Karsten Hopp <karsten@redhat.com> 8.1-0.4
- revert disabling of hardware drivers, disable only llvm on PPC*
  (#819060)

* Tue May 01 2012 Adam Jackson <ajax@redhat.com> 8.1-0.3
- More RHEL tweaking: no pre-DX7 drivers, no wayland.

* Thu Apr 26 2012 Karsten Hopp <karsten@redhat.com> 8.1-0.2
- move drirc into with_hardware section (Dave Airlie)
- libdricore.so and libglsl.so get built and installed on
  non-hardware archs, include them in the file list

* Thu Apr 26 2012 Adam Jackson <ajax@redhat.com> 8.1-0.2
- Don't build vmware stuff on non-x86 (#815444)

* Tue Apr 24 2012 Richard Hughes <rhughes@redhat.com> 8.0.3-0.1
- Rebuild with new git snapshot
- Remove upstreamed patches
