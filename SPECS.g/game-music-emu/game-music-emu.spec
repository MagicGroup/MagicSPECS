Name:           game-music-emu
Version:        0.6.0
Release:        3%{?dist}
Provides:       libgme%{?_isa} = %{version}-%{release}
Summary:        Video game music file emulation/playback library
License:        LGPLv2+
URL:            http://code.google.com/p/game-music-emu/
Source0:        http://game-music-emu.googlecode.com/files/%{name}-%{version}.tar.bz2
Patch0:         gme-0.6.0-pc-lib-suffix.patch

BuildRequires:  cmake
# needed to build the player
BuildRequires:  SDL-devel

%package devel
Summary:        Development files for Game_Music_Emu
Provides:       libgme-devel%{?_isa} = %{version}-%{release}
Requires:       %{name}%{?_isa} = %{version}
Requires:       pkgconfig

%package player
Summary:        Demo player utilizing Game_Music_Emu
License:        MIT


%description
Game_Music_Emu is a collection of video game music file emulators that support
the following formats and systems:

 * AY       ZX Spectrum/Amstrad CPC
 * GBS      Nintendo Game Boy
 * GYM      Sega Genesis/Mega Drive
 * HES      NEC TurboGrafx-16/PC Engine
 * KSS      MSX Home Computer/other Z80 systems (doesn't support FM sound)
 * NSF/NSFE Nintendo NES/Famicom (with VRC 6, Namco 106, and FME-7 sound)
 * SAP      Atari systems using POKEY sound chip
 * SPC      Super Nintendo/Super Famicom
 * VGM/VGZ  Sega Master System/Mark III, Sega Genesis/Mega Drive,BBC Micro

%description devel
This package contains files needed to compile code which uses Game_Music_Emu.

%description player
This package contains the demo player for files supported by Game_Music_Emu.


%prep
%setup -q
# fix libgme.pc install path
%patch0
# add install rule for the player
echo -e "\ninstall(TARGETS gme_player RUNTIME DESTINATION %{_bindir})" >> player/CMakeLists.txt


%build
%cmake
make %{?_smp_mflags}
# explicitly build the player as it has EXCLUDE_FROM_ALL set
make %{?_smp_mflags} gme_player


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
# explicitly install the player as it has EXCLUDE_FROM_ALL set
cd player
make install DESTDIR=%{buildroot}
cd ..


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%doc changes.txt license.txt readme.txt
%{_libdir}/libgme.so.*

%files devel
%doc design.txt gme.txt
%{_libdir}/libgme.so
%{_includedir}/gme/
%{_libdir}/pkgconfig/libgme.pc

%files player
%{_bindir}/gme_player


%changelog
* Fri Sep 20 2013 Karel Volný <kvolny@redhat.com> 0.6.0-3
- Adjust virtual provides according to further comments on bug#1006881

* Fri Sep 13 2013 Karel Volný <kvolny@redhat.com> 0.6.0-2
- Add virtual provides libgme (bug #1006881)

* Thu Aug 22 2013 Karel Volný <kvolny@redhat.com> 0.6.0-1
- New release
- See changes.txt for list of upstream changes
- Adds pkgconfig file (+ patch to correct path)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 24 2011 Karel Volny <kvolny@redhat.com> 0.5.5-1
- Initial release for Fedora 15
