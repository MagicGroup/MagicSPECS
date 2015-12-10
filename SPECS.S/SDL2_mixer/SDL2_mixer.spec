Name:           SDL2_mixer
Version:        2.0.0
Release:        13%{?dist}
Summary:        Simple DirectMedia Layer - Sample Mixer Library
Summary(zh_CN.UTF-8): SDL 的混音库

Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        zlib
URL:            http://www.libsdl.org/projects/SDL_mixer/
Source0:        http://www.libsdl.org/projects/SDL_mixer/release/%{name}-%{version}.tar.gz
Patch0:         properly_include_modplug.patch

BuildRequires:  SDL2-devel
BuildRequires:  libvorbis-devel
BuildRequires:  flac-devel
BuildRequires:  chrpath
BuildRequires:  libmodplug-devel
BuildRequires:  fluidsynth-devel
BuildRequires:  libmikmod-devel

%description
SDL_mixer is a sample multi-channel audio mixer library.
It supports any number of simultaneously playing channels of 16 bit stereo
audio, plus a single channel of music, mixed by the popular FLAC,
MikMod MOD, Timidity MIDI, Ogg Vorbis, and SMPEG MP3 libraries. 

%description -l zh_CN.UTF-8
SDL 的混音库。

%package devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       SDL2-devel
Requires:       libvorbis-devel

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.
%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q
sed -i -e 's/\r//g' README.txt CHANGES.txt COPYING.txt
# https://bugzilla.redhat.com/show_bug.cgi?id=1093378
%patch0 -p1 -b .include_modplug
rm -rf external/

%build
%configure --disable-dependency-tracking \
           --disable-static
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool
make %{?_smp_mflags}

%install
%make_install install-bin
for i in playmus playwave
do
  chrpath -d %{buildroot}%{_bindir}/${i}
  mv %{buildroot}%{_bindir}/${i} %{buildroot}%{_bindir}/${i}2
done

find %{buildroot} -name '*.la' -exec rm -f {} ';'
magic_rpm_clean.sh

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc CHANGES.txt COPYING.txt
%{_bindir}/playmus2
%{_bindir}/playwave2
%{_libdir}/lib*.so.*

%files devel
%doc README.txt
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/SDL2/*

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 2.0.0-13
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 2.0.0-12
- 为 Magic 3.0 重建

* Wed Sep 30 2015 Liu Di <liudidi@gmail.com> - 2.0.0-11
- 为 Magic 3.0 重建

* Mon Sep 07 2015 Liu Di <liudidi@gmail.com> - 2.0.0-10
- 为 Magic 3.0 重建

* Mon Sep 07 2015 Liu Di <liudidi@gmail.com> - 2.0.0-9
- 为 Magic 3.0 重建

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 01 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.0-5
- Fix FTBFS with autoreconf

* Thu May 01 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.0-4
- Add patch for properly include modplug (RHBZ #1093378)

* Wed Nov 20 2013 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.0-3
- Add some BuildRequires (cicku)
- Delete pkgconfig from -devel subpackage (cicku)
- Removing external folder in prep section (ignatenkobrain)
- Fix license to correct zlib (cicku & ignatenkobrain)

* Mon Nov 18 2013 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.0-2
- Update for review

* Sat Sep  7 2013 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.0-1
- Based on SDL_mixer
