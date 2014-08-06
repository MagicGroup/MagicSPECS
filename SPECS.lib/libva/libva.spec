%bcond_without libudev
#需要细分包

Name:      libva
Version:   1.0.15
Release:   3%{?dist}
Summary:   Video Acceleration (VA) API for Linux
Summary(zh_CN.UTF-8): Linux 下的视频加速 (VA) API
Group:     System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:   MIT
URL:       http://freedesktop.org/wiki/Software/vaapi
Source0:   http://www.freedesktop.org/software/vaapi/releases/libva//%{name}-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: libtool
%{?with_libudev:BuildRequires: libudev-devel}
BuildRequires: libXext-devel
BuildRequires: libXfixes-devel
BuildRequires: libdrm-devel
BuildRequires: mesa-libGL-devel

Provides:  libva-freeworld = %{version}-%{release}
Obsoletes: libva-freeworld < %{version}-%{release}
Provides:  libva-utils = %{version}-%{release}
Obsoletes: libva-utils < %{version}-%{release}

%description
Libva is a library providing the VA API video acceleration API.

%description -l zh_CN.UTF-8
Linux 下的视频加速 (VA) API。

%package libs
Summary: Shared libs for %{name}
Summary(zh_CN.UTF-8): %{name} 的共享库
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}

%description libs
Shared libraries for %{name}.

%description libs -l zh_CN.UTF-8
%{name} 的动态共享库。

%package static
Summary: Static libs for %{name}
Summary(zh_CN.UTF-8): %{name} 的静态库
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}

%description static
Static libraries for %{name}.

%description static -l zh_CN.UTF-8
%{name} 的静态库。

%package devel
Summary: Devel files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发文件
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}

%description devel
Devel files for %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发文件。

%prep
%setup -q

%build
autoreconf -vif
%configure --enable-static \
           --enable-glx 
make

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} INSTALL="install -p"

find %{buildroot} -regex ".*\.la$" | xargs rm -f --

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc COPYING
%{_bindir}/vainfo
%{_bindir}/h264encode
%{_bindir}/mpeg2vldemo
%{_bindir}/putsurface
%{_bindir}/avcenc
%{_libdir}/dri/dummy_drv_video.so

%files libs 
%defattr(-,root,root,-)
%{_libdir}/lib*.so.*

%files static
%defattr(-,root,root,-)
%{_libdir}/lib*.a
%{_libdir}/dri/*

%files devel
%defattr(-,root,root,-)
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/va/*.h

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.0.15-3
- 为 Magic 3.0 重建

* Sun Apr 10 2011 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.0.10-5
- Allow building/running against older libdrm.

* Sun Mar 07 2011 Paulo Roma <roma@lcg.ufrj.br> - 1.0.10-4
- Switch to upstream.

* Sun Jan 30 2011 Paulo Roma <roma@lcg.ufrj.br> - 0.32.0-3.sds1
- Update to 0.32.0-1.sds1

* Sun Jan 30 2011 Paulo Roma <roma@lcg.ufrj.br> - 0.31.1-2.sds5
- Update to 0.31.1-1.sds5

* Sun Jul 18 2010 Paulo Roma <roma@lcg.ufrj.br> - 0.31.1-1.sds4
- Rebuilt as libva for ATrpms.

* Fri Jul 16 2010 Nicolas Chauvet <kwizart@gmail.com> - 0.31.1-1.sds4
- Update to 0.31.1-1+sds4
- Add BR libudev-devel
- Obsoletes libva-utils 
 (tests files aren't installed anymore).

* Fri Jul 16 2010 Nicolas Chauvet <kwizart@gmail.com> - 0.31.0.1.sds13-3
- Revert to the previous version scheme
- Fix mix use of spaces and tabs

* Wed Jul 14 2010 Nicolas Chauvet <kwizart@gmail.com> - 0.31.0-1.sds13
- Move to libva-freeworld
- Virtual provides libva bumped with epoch
- Remove duplicate licence file.

* Mon Jul 05 2010 Nicolas Chauvet <kwizart@gmail.com> - 0.31.0.1.sds130-1
- Update to 0.31.0-1+sds13

* Fri Mar 12 2010 Adam Williamson <awilliam@redhat.com> - 0.31.0.1.sds10-1
- new SDS patch version (sds10):
 + Add detection of Broadcom Crystal HD chip.
 + Require vaDriverInit() function to include SDS API version. 
 + OpenGL extensions updates:
 - Drop the 'bind' API. Only keep vaCopySurfaceGLX().
 - Fix FBO check for the generic implementation with TFP.
 + Compat: strip vaPutSurface() flags to match older API.
 - This fixes deinterlacing support with GMA500 "psb" driver.
 + Upgrade to GIT snapshot 2009/12/17:
 - Add a "magic" number to VADisplayContext.
 - Add more test programs, including h264 encoding.
- add -utils package for the various new binaries in this build

* Thu Dec 3 2009 Adam Williamson <awilliam@redhat.com> - 0.31.0.1.sds9-1
- new SDS patch version (sds9):
 + Add extra picture info for VDPAU/MPEG-4

* Mon Nov 23 2009 Adam Williamson <awilliam@redhat.com> - 0.31.0.1.sds8-1
- new SDS patch version (sds8) - note sds7 package actually contained
 sds5 due to an error on my part:
 + Fix detection of ATI chipsets with fglrx >= 8.69-Beta1.
 + Upgrade to GIT snapshot 2009/11/20:
  + Merge in some G45 fixes and additions.
  + Add VA_STATUS_ERROR_SURFACE_IN_DISPLAYING.

* Tue Nov 17 2009 Adam Williamson <awilliam@redhat.com> - 0.31.0.1.sds7-1
- new SDS patch version:
 + Fix compatibility with older programs linked against libva.so.0
 + G45 updates:
  + Fix vaCreateImage() and vaDestroyImage()
  + Fix subpictures association to parent surfaces
  + Fix rendering of subpictures (extra level of scaling)
  + Fix subpicture palette upload (IA44 and AI44 formats for now)
  + Add RGBA subpicture formats
  + Add YV12 vaGetImage() and vaPutImage()
  + Fix subpicture rendering (flickering)
  + Fix return value for unimplemented functions
  + Fix vaPutSurface() to handle cliprects (up to 80)


* Thu Oct 8 2009 Adam Williamson <awilliam@redhat.com> - 0.31.0.1.sds5-2
- enable the i965 driver build

* Tue Oct 6 2009 Adam Williamson <awilliam@redhat.com> - 0.31.0.1.sds5-1
- new SDS patch version:
 + G45 updates:
 + Fix VA driver version
 + Fix vaAssociateSubpicture() arguments
 + Add vaQueryDisplayAttributes() as a no-op
 + Fix vaQueryImageFormats() to return 0 formats at this time

* Tue Sep 22 2009 Adam Williamson <awilliam@redhat.com> - 0.31.0.1.sds4-1
- new SDS patch version:
 + Fix chek for GLX extensions
 + Fix libva pkgconfig dependencies
 + Fix vainfo dependencies (Konstantin Pavlov)
 + Add C++ guards to <va/va_glx.h>
 + Don't search LIBGL_DRIVERS_PATH, stick to extra LIBVA_DRIVERS_PATH
 + Upgrade to GIT snapshot 2009/09/22:
 - Merge in SDS patches 001, 201, 202
 - i965_drv_driver: use the horizontal position of a slice

* Thu Sep 10 2009 Adam Williamson <awilliam@redhat.com> - 0.31.0.1.sds3-1
- new upstream + SDS patch version:
 + Add OpenGL extensions (v3)
 + Upgrade to VA API version 0.31 (2009/09/07 snapshot)
 + Add drmOpenOnce() / drmCloseOnce() replacements for libdrm < 2.3
 + Add generic VA/GLX implementation with TFP and FBO
 + Fix detection of ATI chipsets with fglrx >= 8.66-RC1
 + Add VASliceParameterBufferMPEG2.slice_horizontal_position for i965 
   driver

* Thu Sep 3 2009 Adam Williamson <awilliam@redhat.com> - 0.30.4.1.sds5-3
- don't declare the stack as executable when creating libva.so.0

* Mon Aug 31 2009 Adam Williamson <awilliam@redhat.com> - 0.30.4.1.sds5-2
- enable glx support

* Mon Aug 31 2009 Adam Williamson <awilliam@redhat.com> - 0.30.4.1.sds5-1
- new SDS patch version:
 + Add VA_STATUS_ERROR_UNIMPLEMENTED
 + Add vaBindSurfaceToTextureGLX() and vaReleaseSurfaceFromTextureGLX()

* Wed Aug 26 2009 Adam Williamson <awilliam@redhat.com> - 0.30.4.1.sds4-1
- new SDS patch version:
 + Add OpenGL extensions
 + Fix NVIDIA driver version check
 + Fix libva-x11-VERSION.so.* build dependencies

* Wed Aug 12 2009 Adam Williamson <awilliam@redhat.com> - 0.30.4.1.sds3-1
- initial package
