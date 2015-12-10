Summary: Hardware graphics acceleration for the framebuffer device
Summary(zh_CN.UTF-8): 帧缓存设备的硬件图形加速
Name: directfb
Version: 1.7.4
Release: 19%{?dist}
License: GPL
Group: System/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL: http://www.directfb.org/
Source0: http://www.directfb.org/downloads/Core/DirectFB-1.4/DirectFB-%{version}.tar.gz
#Source1: i2c-dev.h
#Patch0: directfb-0.9.25.1-asmtypes.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: gcc-c++
#BuildRequires: /usr/bin/man2html
BuildRequires: SDL-devel, freetype-devel >= 2.0.1
BuildRequires: libjpeg-devel >= 6b, libpng-devel >= 1.0, zlib-devel
BuildRequires: %{_includedir}/sysfs/libsysfs.h
BuildRequires: libX11-devel
BuildRequires: libvncserver-devel
BuildRequires: tslib-devel
BuildRequires: mesa-libGLES-devel, mesa-libEGL-devel

%description
DirectFB is a thin library that provides hardware graphics
acceleration, input device handling and abstraction, integrated
windowing system with support for translucent windows and multiple
display layers on top of the Linux Framebuffer Device.

It is a complete hardware abstraction layer with software fallbacks
for every graphics operation that is not supported by the underlying
hardware.

%package devel
Summary: Development files for building applications with the directfb library
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release} SDL-devel freetype-devel
Requires: libjpeg-devel >= 6b, libpng-devel >= 1.0 zlib-devel

%description devel
Dialog is a utility that allows you to show dialog boxes (containing
questions or messages) in TTY (text mode) interfaces. This package
contains the files needed for developing applications, which use the
dialog library.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n DirectFB-%{version}
%ifarch ppc
grep -rl '#include <linux/config.h>' . | xargs perl -pi -e's,#include <linux/config.h>,/* #include <linux/config.h> */,'
%endif
perl -pi -e's,/usr/X11R6/lib ,/usr/X11R6/%{_lib} ,' configure directfb-config.in

%build
%configure \
	--docdir=%{_defaultdocdir}/%{name}-%{version} \
        --enable-static \
        --enable-shared \
	--enable-x11 \
	--disable-multi \
%ifarch %{ix86}
	--enable-mmx \
%endif
	--enable-sse \
	--enable-fbdev \
	--enable-sdl \
	--enable-jpeg \
	--enable-zlib \
	--enable-png \
  	--enable-gif \
  	--enable-freetype \
  	--enable-video4linux \
  	--enable-video4linux2 \
	--with-gfxdrivers=all \
	--with-inputdrivers=all \
	--with-tests

echo '#undef HAVE_ASM_PAGE_H' >> config.h

make

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

rm -f %{buildroot}%{_libdir}/*.la

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc COPYING AUTHORS INSTALL README NEWS TODO
%{_libdir}/%{name}-*
%{_libdir}/lib*.so.*
%{_datadir}/%{name}-*
%{_bindir}/dfb*
%{_bindir}/mkdfiff
%{_bindir}/mkdgiff
%{_bindir}/coretest_blit2
%{_bindir}/direct_*
%{_bindir}/fusion_*
%{_bindir}/mkdgifft
%{_bindir}/pxa3xx_dump
%{_mandir}/man1/dfbg.1*
%{_mandir}/man5/directfbrc.5*

%files devel 
%defattr(-,root,root,-)
%{_bindir}/directfb-config
%{_bindir}/directfb-csource
%{_bindir}/coretest_task
%{_bindir}/coretest_task_fillrect
%{_mandir}/man1/directfb-csource.1*
%{_includedir}/*
%{_libdir}/lib*.so
%{_libdir}/lib*.a
%{_libdir}/pkgconfig/*.pc

%changelog
* Sat Nov 07 2015 Liu Di <liudidi@gmail.com> - 1.7.4-19
- 为 Magic 3.0 重建

* Thu Oct 29 2015 Liu Di <liudidi@gmail.com> - 1.7.4-18
- 为 Magic 3.0 重建

* Sun May  4 2014 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.7.4-17
- Update to 1.7.4.

* Thu Mar 24 2011 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.4.11-16
- Update to 1.4.11.

* Sat Jan 12 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.0.1-15
- Update to 1.0.1.

* Sat Mar 17 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.0.0-13
- Update to 1.0.0.

* Mon Jun 26 2006 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 0.9.25.1.

* Wed Oct 26 2005 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 0.9.24.

* Sun Oct  9 2005 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 0.9.22.
- Dropped sis315 build.

* Mon May 17 2004 Axel Thimm <Axel.Thimm@ATrpms.net>
- Apply patch for building against 2.6.x kernel headers.

* Sat Nov 22 2003 Axel Thimm <Axel.Thimm@ATrpms.net> 
- Initial build.
