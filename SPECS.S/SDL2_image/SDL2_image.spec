Name:           SDL2_image
Version:        2.0.0
Release:        8%{?dist}
Summary:        Image loading library for SDL

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://www.libsdl.org/projects/SDL_image/
Source0:        http://www.libsdl.org/projects/SDL_image/release/%{name}-%{version}.tar.gz
# http://hg.libsdl.org/SDL_image/rev/f0b623bb5570
Patch0:         SDL2_image-2.0.0-big-endian.patch

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

%package devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       SDL2-devel
Requires:       pkgconfig

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q
%patch0 -p1 -b big-endian
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