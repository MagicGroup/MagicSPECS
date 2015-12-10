Name:		svgalib
Version:	1.9.25
Release:	12%{?dist}
Summary:	Low-level fullscreen SVGA graphics library
Summary(zh_CN.UTF-8): 低级全屏 SVGA 图形库
Group:		System Environment/Libraries
Group(zh_CN.UTF-8):	系统环境/库
License:	Public Domain
URL:		http://www.svgalib.org/
Source0:	http://www.arava.co.il/matan/svgalib/svgalib-%{version}.tar.gz
Source1:	svgalib-todo
Patch0:		svgalib-1.9.21-makefiles.patch
Patch1:		svgalib-1.4.3-fhs.patch
Patch2:		svgalib-1.9.21-demos.patch
Patch3:		svgalib-1.9.21-cfg.patch
Patch4:		svgalib-1.9.25-kernel-2.6.26.patch
Patch5:		svgalib-1.9.25-round.patch 
Patch6:		svgalib-1.9.25-vga_getmodenumber.patch
Patch7:		svgalib-1.9.25-quickmath-h-redefinitions.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Exclusivearch:	%{ix86} x86_64

%description
The svgalib package provides the SVGAlib low-level graphics library
for Linux.  SVGAlib is a library which allows applications to use full
screen graphics on a variety of hardware platforms. Some games and
utilities use SVGAlib for their graphics. For details on
supported chipsets, see man 7 svgalib (when svgalib is installed).

%description -l zh_CN.UTF-8
低级全屏 SVGA 图形库。

%package devel
Summary:	Development tools for the SVGAlib graphics library
Summary(zh_CN.UTF-8): %name 的开发包
Group:		Development/Libraries
Group(zh_CN.UTF-8):	开发/库
Requires:	%{name} = %{version}-%{release}
Provides:	libvga-devel = %{version}-%{release}

%description devel
The svgalib-devel package contains the libraries and header files
needed to build programs which will use the SVGAlib low-level graphics
library.

%description devel -l zh_CN.UTF-8
%name 的开发包。

%prep
%setup -q 
%patch0 -p1 -b .makefiles
%patch1 -p1 -b .fhs
%patch2 -p1
%patch3 -p1 -b .defaultcfg
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

#the testlinear demo needs svgalib's internal libvga header, so copy it to the
#demo dir
cp src/libvga.h demos


%build
#%{?_smp_mflags} doesn't work on x86_64 chances are it will fail on
#some i386 machines too.
make OPTIMIZE="$RPM_OPT_FLAGS -Wno-pointer-sign" LDFLAGS= \
  prefix=%{_prefix} \
  NO_HELPER=y \
  INCLUDE_ET4000_DRIVER=y \
  INCLUDE_OAK_DRIVER=y \
  INCLUDE_MACH32_DRIVER=y \
  INCLUDE_ET3000_DRIVER=y \
  INCLUDE_GVGA6400_DRIVER=y \
  INCLUDE_ATI_DRIVER=y \
  INCLUDE_G450C2_DRIVER=y \
  INCLUDE_ET4000_DRIVER_TEST=y \
  INCLUDE_FBDEV_DRIVER_TEST=y \
  INCLUDE_VESA_DRIVER_TEST=y \
  shared
cd utils
make OPTIMIZE="$RPM_OPT_FLAGS -Wno-pointer-sign" LDFLAGS= \
  prefix=%{_prefix}
cd ..
cd threeDKit
make OPTIMIZE="$RPM_OPT_FLAGS -Wno-pointer-sign -I../gl" LDFLAGS= \
  prefix=%{_prefix} lib3dkit.so.%{version}
cd ..


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/etc/vga
mkdir -p $RPM_BUILD_ROOT/%{_libdir}
make \
  TOPDIR=$RPM_BUILD_ROOT \
  prefix=$RPM_BUILD_ROOT/%{_prefix} \
  mandir=$RPM_BUILD_ROOT/%{_mandir} \
  sharedlibdir=$RPM_BUILD_ROOT/%{_libdir} \
  NO_HELPER=y \
  MANFORMAT=compressed \
  "INSTALL_PROGRAM=install -p -m 755" \
  "INSTALL_SCRIPT=install -p -m 755" \
  "INSTALL_SHLIB=install -p -m 755" \
  "INSTALL_DATA=install -p -m 644" \
  install
ln -s libvga.so.%{version} $RPM_BUILD_ROOT/%{_libdir}/libvga.so.1
ln -s libvgagl.so.%{version} $RPM_BUILD_ROOT/%{_libdir}/libvgagl.so.1
ln -s lib3dkit.so.%{version} $RPM_BUILD_ROOT/%{_libdir}/lib3dkit.so.1
#for %ghost
touch $RPM_BUILD_ROOT/etc/vga/fontdata
touch $RPM_BUILD_ROOT/etc/vga/textregs


%clean
rm -fr $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc doc/CHANGES doc/README.joystick doc/README.keymap lrmi-0.6m/README
%doc doc/README.multi-monitor doc/README.vesa doc/TODO doc/dual-head-howto
%dir %{_sysconfdir}/vga/
%config(noreplace) %{_sysconfdir}/vga/dvorak-us.keymap
%config(noreplace) %{_sysconfdir}/vga/libvga.config
%config(noreplace) %{_sysconfdir}/vga/libvga.et4000
%config(noreplace) %{_sysconfdir}/vga/null.keymap
%ghost %{_sysconfdir}/vga/fontdata
%ghost %{_sysconfdir}/vga/textregs
%{_bindir}/*
%{_libdir}/*.so.*
%{_mandir}/man[^3]/*

%files devel
%defattr(-,root,root,-)
%doc demos doc/DESIGN doc/Driver-programming-HOWTO doc/README.patching
%{_includedir}/*
%{_libdir}/*.so
%{_mandir}/man3/*


%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 1.9.25-12
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 1.9.25-11
- 为 Magic 3.0 重建

* Tue Sep 29 2015 Liu Di <liudidi@gmail.com> - 1.9.25-10
- 为 Magic 3.0 重建

* Tue Sep 29 2015 Liu Di <liudidi@gmail.com> - 1.9.25-9
- 为 Magic 3.0 重建

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 1.9.25-8
- 为 Magic 3.0 重建

* Fri Feb 10 2012 Liu Di <liudidi@gmail.com> - 1.9.25-7
- 为 Magic 3.0 重建


