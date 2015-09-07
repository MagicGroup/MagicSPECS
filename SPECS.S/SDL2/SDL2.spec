Name:           SDL2
Version:        2.0.3
Release:        7%{?dist}
Summary:        A cross-platform multimedia library
Group:          System Environment/Libraries
URL:            http://www.libsdl.org/
License:        zlib and MIT
Source0:        http://www.libsdl.org/release/%{name}-%{version}.tar.gz
Source1:        SDL_config.h
Patch0:         multilib.patch
# https://hg.libsdl.org/SDL/rev/7e843b8b8301
Patch1:		SDL2-2.0.3-oldgcc.patch

BuildRequires:  alsa-lib-devel
BuildRequires:  audiofile-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  mesa-libGLU-devel
BuildRequires:  mesa-libEGL-devel
BuildRequires:  mesa-libGLES-devel
BuildRequires:  libXext-devel
BuildRequires:  libX11-devel
BuildRequires:  libXi-devel
BuildRequires:  libXrandr-devel
BuildRequires:  libXrender-devel
BuildRequires:  dbus-devel
BuildRequires:  libXScrnSaver-devel
BuildRequires:  libusb-devel
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  libXinerama-devel
BuildRequires:  libXcursor-devel
BuildRequires:  systemd-devel
# Wayland
BuildRequires:  libwayland-client-devel
BuildRequires:  libwayland-egl-devel
BuildRequires:  libwayland-cursor-devel
BuildRequires:  libxkbcommon-devel

%description
Simple DirectMedia Layer (SDL) is a cross-platform multimedia library designed
to provide fast access to the graphics frame buffer and audio device.

%package devel
Summary:    Files needed to develop Simple DirectMedia Layer applications
Group:      Development/Libraries
Requires:   %{name}%{?_isa} = %{version}-%{release}
Requires:   alsa-lib-devel
Requires:   mesa-libGL-devel
Requires:   mesa-libGLU-devel
Requires:   mesa-libEGL-devel
Requires:   mesa-libGLES-devel
Requires:   libX11-devel
Requires:   libXi-devel
Requires:   libXext-devel
Requires:   libXrandr-devel
Requires:   libXrender-devel
Requires:   libXScrnSaver-devel
Requires:   libXinerama-devel
Requires:   libXcursor-devel
Requires:   systemd-devel
# Wayland
Requires:   libwayland-client-devel
Requires:   libwayland-egl-devel
Requires:   libwayland-cursor-devel
Requires:   libxkbcommon-devel

%description devel
Simple DirectMedia Layer (SDL) is a cross-platform multimedia library designed
to provide fast access to the graphics frame buffer and audio device. This
package provides the libraries, include files, and other resources needed for
developing SDL applications.

%prep
%setup -q
%patch0 -p1 -b .multilib
%patch1 -p1 -b .oldgcc
# Compilation without ESD
sed -i -e 's/.*AM_PATH_ESD.*//' configure.in
sed -i -e 's/\r//g' TODO.txt README.txt WhatsNew.txt BUGS.txt COPYING.txt CREDITS.txt README-SDL.txt

%build
%configure \
    --enable-sdl-dlopen \
    --disable-arts \
    --disable-esd \
    --disable-nas \
    --enable-pulseaudio-shared \
    --enable-alsa \
    --enable-video-wayland \
    --disable-rpath
make %{?_smp_mflags}

%install
%make_install

# Rename SDL_config.h to SDL_config-<arch>.h to avoid file conflicts on
# multilib systems and install SDL_config.h wrapper
mv %{buildroot}%{_includedir}/SDL2/SDL_config.h %{buildroot}%{_includedir}/SDL2/SDL_config-%{_arch}.h
install -p -m 644 %{SOURCE1} %{buildroot}%{_includedir}/SDL2/SDL_config.h

# remove libtool .la file
rm -f %{buildroot}%{_libdir}/*.la
# remove static .a file
rm -f %{buildroot}%{_libdir}/*.a

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc BUGS.txt CREDITS.txt COPYING.txt README-SDL.txt
%{_libdir}/lib*.so.*

%files devel
%doc README.txt TODO.txt WhatsNew.txt
%{_bindir}/*-config
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/sdl2.pc
%{_includedir}/SDL2
%{_datadir}/aclocal/*

%changelog
* Sun Sep 06 2015 Liu Di <liudidi@gmail.com> - 2.0.3-7
- 为 Magic 3.0 重建

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun  2 2015 Tom Callaway <spot@fedoraproject.org> - 2.0.3-5
- remove code preventing builds with ancient gcc

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jun 11 2014 Karsten Hopp <karsten@redhat.com> 2.0.3-3
- fix filename of SDL_config.h for ppc64le

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Mar 19 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.3-1
- 2.0.3 upstream release

* Sat Mar 08 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.2-1
- 2.0.2 upstream release
- Enable wayland backend

* Tue Dec 10 2013 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.1-2
- Add libXinerama, libudev, libXcursor support (RHBZ #1039702)

* Thu Oct 24 2013 Tom Callaway <spot@fedoraproject.org> - 2.0.1-1
- update to 2.0.1

* Sat Aug 24 2013 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.0-3
- Fix multilib issues

* Tue Aug 13 2013 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.0-2
- SDL2 is released. Announce:
- http://lists.libsdl.org/pipermail/sdl-libsdl.org/2013-August/089854.html

* Sat Aug 10 2013 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.0-1.rc4
- Update to latest SDL2 (08.08.2013)

* Tue Jul 30 2013 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.0-1.rc3
- Fix Licenses
- some cleanups in spec

* Tue Jul 30 2013 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.0-1.rc2
- Delete -static package
- Fix License tag
- Fix end-of-line in documents
- Remove all spike-nails EL-specify (if someone will want to do - 'patches are welcome')
- Change Release tag to .rcX%%{?dist} (maintainer has changed released tarballs)

* Mon Jul 29 2013 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.0-1.rc1
- Some fixes in spec and cleanup

* Mon Jul 29 2013 Jon Ciesla <limburgher@gmail.com> - 2.0.0-1
- Ported from SDL 1.2.15-10
