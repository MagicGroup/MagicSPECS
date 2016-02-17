Name:           SDL2_image
Version:	2.0.1
Release:	1%{?dist}
Summary:        Image loading library for SDL
Summary(zh_CN.UTF-8): SDL 的图像载入库

Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        LGPLv2+
URL:            http://www.libsdl.org/projects/SDL_image/
Source0:        http://www.libsdl.org/projects/SDL_image/release/%{name}-%{version}.tar.gz

BuildRequires:  SDL2-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libpng-devel
BuildRequires:  libtiff-devel
BuildRequires:  libwebp-devel
BuildRequires:  chrpath

%description
Simple DirectMedia Layer (SDL) is a cross-platform multimedia library
designed to provide fast access to the graphics frame buffer and audio
device.  This package contains a simple library for loading images of
various formats (BMP, PPM, PCX, GIF, JPEG, PNG) as SDL surfaces.

%description -l zh_CN.UTF-8
SDL 的图像载入库，支持多种图像格式（BMP, PPM, PCX, GIF, JPEG, PNG）。

%package devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       SDL2-devel
Requires:       pkgconfig

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.
%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q
rm -rf external/
sed -i -e 's/\r//g' README.txt CHANGES.txt COPYING.txt

%build
%configure --disable-dependency-tracking \
           --disable-jpg-shared \
           --disable-png-shared \
           --disable-tif-shared \
           --disable-webp-shared \
           --disable-static
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool
make %{?_smp_mflags}

%install
%make_install
mkdir -p %{buildroot}%{_bindir}
./libtool --mode=install /usr/bin/install showimage %{buildroot}%{_bindir}/showimage2
chrpath -d %{buildroot}%{_bindir}/showimage2

rm -f %{buildroot}%{_libdir}/*.la
magic_rpm_clean.sh

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc CHANGES.txt COPYING.txt
%{_bindir}/showimage2
%{_libdir}/lib*.so.*

%files devel
%doc README.txt
%{_libdir}/lib*.so
%{_includedir}/SDL2/*
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Wed Sep 30 2015 Liu Di <liudidi@gmail.com> - 2.0.0-10
- 为 Magic 3.0 重建

* Mon Sep 07 2015 Liu Di <liudidi@gmail.com> - 2.0.0-9
- 为 Magic 3.0 重建

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 15 2014 Dan Horák <dan[at]danny.cz> - 2.0.0-5
- fix FTBFS on big endian arches

* Fri Jan 03 2014 Kalev Lember <kalevlember@gmail.com> - 2.0.0-4
- Rebuilt for libwebp soname bump

* Fri Sep  6 2013 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.0-3
- showimage -> showimage2 (rhbz 1005324)

* Fri Sep  6 2013 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.0-2
- Move README.txt to -devel subpackage

* Fri Sep  6 2013 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.0-1
- Based on SDL_image
