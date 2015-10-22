# ldplayer can be disabled by --without ldplayer or by changing to %bcond_with
# if it does not build. The debug build is disabled by default, please use
# --with debug to override
%bcond_without ldplayer
%bcond_with debug
%bcond_with simd

%global baseversion 163

# work around low memory on the RPM Fusion builder
%bcond_without lowmem
%if %{with lowmem}
%global _find_debuginfo_dwz_opts %{nil}
%endif

Name:           mame
Version:        0.%{baseversion}
Release:        4%{?dist}
Summary:        Multiple Arcade Machine Emulator

License:        MAME License and BSD and GPLv2+ and LGPLv2+ and Public Domain and zlib
URL:            http://mamedev.org/
Source0:        http://mamedev.org/downloader.php?file=%{name}0%{baseversion}/%{name}0%{baseversion}s.exe
Source100:      whatsnew.zip
Patch0:         %{name}-fortify.patch
Patch1:         %{name}-systempa.patch
Patch2:         %{name}-genie-smpfix.patch
Patch3:         %{name}-armfix.patch

BuildRequires:  expat-devel
BuildRequires:  flac-devel
#BuildRequires:  jsoncpp-devel
BuildRequires:  libjpeg-turbo-devel
%if 0%{?fedora} >= 22
BuildRequires:  lua-devel >= 5.3.0
%endif
#BuildRequires:  mongoose-devel
BuildRequires:  p7zip
BuildRequires:  portaudio-devel
BuildRequires:  portmidi-devel
BuildRequires:  python
BuildRequires:  qt-devel
BuildRequires:  SDL2_ttf-devel
BuildRequires:  sqlite-devel
BuildRequires:  zlib-devel
Requires:       %{name}-data = %{version}-%{release}

Provides:       bundled(bgfx)
Provides:       bundled(bx)
Provides:       bundled(jsoncpp)
%if 0%{?fedora} < 22
Provides:       bundled(lua) = 5.3.0
%endif
Provides:       bundled(lzma-sdk) = 9.22
Provides:       bundled(mongoose)
Provides:       mess = %{version}-%{release}
Obsoletes:      mess < 0.160-2


%description
MAME stands for Multiple Arcade Machine Emulator.  When used in conjunction
with an arcade game's data files (ROMs), MAME will more or less faithfully
reproduce that game on a PC.

The ROM images that MAME utilizes are "dumped" from arcade games' original
circuit-board ROM chips.  MAME becomes the "hardware" for the games, taking
the place of their original CPUs and support chips.  Therefore, these games
are NOT simulations, but the actual, original games that appeared in arcades.

MAME's purpose is to preserve these decades of video-game history.  As gaming
technology continues to rush forward, MAME prevents these important "vintage"
games from being lost and forgotten.  This is achieved by documenting the
hardware and how it functions, thanks to the talent of programmers from the
MAME team and from other contributors.  Being able to play the games is just
a nice side-effect, which doesn't happen all the time.  MAME strives for
emulating the games faithfully.

%package tools
Summary:        Additional tools for MAME
Requires:       %{name} = %{version}-%{release}

Provides:       mess-tools = %{version}-%{release}
Obsoletes:      mess-tools < 0.160-2

%description tools
%{summary}.

%if %{with ldplayer}
%package ldplayer
Summary:        Standalone laserdisc player based on MAME

%description ldplayer
%{summary}.
%endif

%package data
Summary:        Data files used by MAME

Provides:       mess-data = %{version}-%{release}

BuildArch:      noarch

%description data
%{summary}.

%package data-software-lists
Summary:        Software lists used by MAME
Requires:       %{name}-data = %{version}-%{release}

Provides:       mess-data-software-lists = %{version}-%{release}
Obsoletes:      mess-data < 0.146-2

BuildArch:      noarch

%description data-software-lists
%{summary}. These are split from the main -data
subpackage due to relatively large size.


%prep
%setup -qcT
for sourcefile in %{sources}; do
    7za x $sourcefile
done

find \( -regex '.*\.\(c\|fsh\|fx\|h\|lua\|map\|md\|txt\|vsh\|xml\)$' \
    -o -wholename ./makefile \) -exec sed -i 's@\r@@' {} \;

%patch0 -p1 -b .fortify
%patch1 -p1 -b .systempa
%patch2 -p1 -b .smpfix
%patch3 -p1 -b .armfix

# Fix encoding
#for whatsnew in whatsnew_0162.txt; do
#    iconv -f iso8859-1 -t utf-8 $whatsnew > $whatsnew.conv
#    mv -f $whatsnew.conv $whatsnew
#done

# Create ini files
cat > %{name}.ini << EOF
# Define multi-user paths
artpath            %{_datadir}/%{name}/artwork;%{_datadir}/%{name}/effects
cheatpath          %{_datadir}/%{name}/cheat
crosshairpath      %{_datadir}/%{name}/crosshair
ctrlrpath          %{_datadir}/%{name}/ctrlr
fontpath           %{_datadir}/%{name}/fonts
hashpath           %{_datadir}/%{name}/hash
rompath            %{_datadir}/%{name}/roms;%{_datadir}/%{name}/chds
samplepath         %{_datadir}/%{name}/samples

# Allow user to override ini settings
inipath            \$HOME/.%{name}/ini;%{_sysconfdir}/%{name}

# Set paths for local storage
cfg_directory      \$HOME/.%{name}/cfg
comment_directory  \$HOME/.%{name}/comments
diff_directory     \$HOME/.%{name}/diff
input_directory    \$HOME/.%{name}/inp
nvram_directory    \$HOME/.%{name}/nvram
snapshot_directory \$HOME/.%{name}/snap
state_directory    \$HOME/.%{name}/sta

# Fedora custom defaults
video              opengl
autosave           1
EOF

%if %{with simd}
sed -i 's@USE_SIMD        (0)@USE_SIMD        (1)@' src/emu/cpu/rsp/rsp.h
%endif

%build
#these flags are already included in the genie.lua
RPM_OPT_FLAGS=$(echo $RPM_OPT_FLAGS | sed -e 's@-O2 -g -pipe -Wall @@')

%if %{with simd}
RPM_OPT_FLAGS=$(echo $RPM_OPT_FLAGS | sed -e 's@-mtune=generic@-march=corei7-avx@')
%endif

#save some space
#jsoncpp and mongoose in Fedora are too old, lua is only new enough on F22+
%if 0%{?fedora} >= 22
MAME_FLAGS="NOWERROR=1 SYMBOLS=1 OPTIMIZE=2 VERBOSE=1 USE_SYSTEM_LIB_EXPAT=1 \
    USE_SYSTEM_LIB_ZLIB=1 USE_SYSTEM_LIB_JPEG=1 USE_SYSTEM_LIB_FLAC=1 \
    USE_SYSTEM_LIB_LUA=1 USE_SYSTEM_LIB_SQLITE3=1 USE_SYSTEM_LIB_PORTMIDI=1 \
    USE_SYSTEM_LIB_PORTAUDIO=1 SDL_INI_PATH=%{_sysconfdir}/%{name};"
%else
MAME_FLAGS="NOWERROR=1 SYMBOLS=1 OPTIMIZE=2 VERBOSE=1 USE_SYSTEM_LIB_EXPAT=1 \
    USE_SYSTEM_LIB_ZLIB=1 USE_SYSTEM_LIB_JPEG=1 USE_SYSTEM_LIB_FLAC=1 \
    USE_SYSTEM_LIB_SQLITE3=1 USE_SYSTEM_LIB_PORTMIDI=1 \
    USE_SYSTEM_LIB_PORTAUDIO=1 SDL_INI_PATH=%{_sysconfdir}/%{name};"
%endif

%if %{with lowmem}
MAME_FLAGS="$MAME_FLAGS LDOPTS=-Wl,--no-keep-memory,--reduce-memory-overheads \
    SYMLEVEL=1"
%endif

#only use assembly on supported architectures
%ifnarch %{ix86} x86_64 ppc ppc64
MAME_FLAGS="$MAME_FLAGS NOASM=1"
%endif

%if %{with ldplayer}
make %{?_smp_mflags} $MAME_FLAGS TARGET=ldplayer OPT_FLAGS="$RPM_OPT_FLAGS"
%endif
%if %{with debug}
make %{?_smp_mflags} $MAME_FLAGS DEBUG=1 TOOLS=1 OPT_FLAGS="$RPM_OPT_FLAGS"
%else
make %{?_smp_mflags} $MAME_FLAGS TOOLS=1 OPT_FLAGS="$RPM_OPT_FLAGS"
%endif


%install
rm -rf $RPM_BUILD_ROOT

# create directories
install -d $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
for folder in cfg comments diff ini inp memcard nvram snap sta
do
    install -d $RPM_BUILD_ROOT%{_sysconfdir}/skel/.%{name}/$folder
done
install -d $RPM_BUILD_ROOT%{_bindir}
for folder in artwork chds cheats ctrlr effects fonts hash hlsl keymaps roms \
    samples shader
do
    install -d $RPM_BUILD_ROOT%{_datadir}/%{name}/$folder
done
install -d $RPM_BUILD_ROOT%{_mandir}/man1
install -d $RPM_BUILD_ROOT%{_mandir}/man6

# install files
install -pm 644 %{name}.ini $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
%if %{with ldplayer}
install -pm 755 ldplayer $RPM_BUILD_ROOT%{_bindir}/ldplayer || \
install -pm 755 ldplayer64 $RPM_BUILD_ROOT%{_bindir}/ldplayer
%endif
%if %{with debug}
install -pm 755 %{name}d $RPM_BUILD_ROOT%{_bindir}/%{name}d || \
install -pm 755 %{name}64d $RPM_BUILD_ROOT%{_bindir}/%{name}d
%else
install -pm 755 %{name} $RPM_BUILD_ROOT%{_bindir}/%{name} || \
install -pm 755 %{name}64 $RPM_BUILD_ROOT%{_bindir}/%{name}
%endif
install -pm 755 castool chdman floptool imgtool jedutil ldresample ldverify \
    nltool pngcmp romcmp testkeys unidasm $RPM_BUILD_ROOT%{_bindir}
for tool in regrep split src2html srcclean
do
    install -pm 755 $tool $RPM_BUILD_ROOT%{_bindir}/%{name}-$tool
done
install -pm 644 artwork/* $RPM_BUILD_ROOT%{_datadir}/%{name}/artwork
install -pm 644 hash/* $RPM_BUILD_ROOT%{_datadir}/%{name}/hash
install -pm 644 hlsl/* $RPM_BUILD_ROOT%{_datadir}/%{name}/hlsl
install -pm 644 keymaps/* $RPM_BUILD_ROOT%{_datadir}/%{name}/keymaps
pushd src/osd/modules/opengl
install -pm 644 shader/*.?sh $RPM_BUILD_ROOT%{_datadir}/%{name}/shader
popd
pushd src/osd/sdl/man
%if %{with ldplayer}
install -pm 644 ldplayer.1 $RPM_BUILD_ROOT%{_mandir}/man1
%endif
install -pm 644 castool.1 chdman.1 imgtool.1 floptool.1 jedutil.1 ldresample.1 \
    ldverify.1 romcmp.1 testkeys.1 $RPM_BUILD_ROOT%{_mandir}/man1
install -pm 644 mame.6 mess.6 $RPM_BUILD_ROOT%{_mandir}/man6
popd


%files
%doc docs/config.txt docs/floppy.txt docs/hlsl.txt docs/luaengine.md
%doc docs/m6502.txt docs/mame.txt docs/mamelicense.txt docs/newvideo.txt
%doc docs/nscsi.txt docs/SDL.txt README.md whatsnew*.txt 
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.ini
%dir %{_sysconfdir}/%{name}
%{_sysconfdir}/skel/.%{name}
%if %{with debug}
%{_bindir}/%{name}d
%else
%{_bindir}/%{name}
%endif
%{_mandir}/man6/mame.6*
%{_mandir}/man6/mess.6*

%files tools
%doc docs/imgtool.txt
%{_bindir}/castool
%{_bindir}/chdman
%{_bindir}/jedutil
%{_bindir}/floptool
%{_bindir}/imgtool
%{_bindir}/ldresample
%{_bindir}/ldverify
%{_bindir}/%{name}-regrep
%{_bindir}/nltool
%{_bindir}/pngcmp
%{_bindir}/romcmp
%{_bindir}/%{name}-split
%{_bindir}/%{name}-src2html
%{_bindir}/%{name}-srcclean
%{_bindir}/testkeys
%{_bindir}/unidasm
%{_mandir}/man1/castool.1*
%{_mandir}/man1/chdman.1*
%{_mandir}/man1/floptool.1*
%{_mandir}/man1/imgtool.1*
%{_mandir}/man1/jedutil.1*
%{_mandir}/man1/ldresample.1*
%{_mandir}/man1/ldverify.1*
%{_mandir}/man1/romcmp.1*
%{_mandir}/man1/testkeys.1*

%if %{with ldplayer}
%files ldplayer
%{_bindir}/ldplayer
%{_mandir}/man1/ldplayer.1*
%endif

%files data
%{_datadir}/%{name}
%exclude %{_datadir}/%{name}/hash/*

%files data-software-lists
%{_datadir}/%{name}/hash/*


%changelog
* Sat Jul 18 2015 Julian Sikorski <belegdol@fedoraproject.org> - 0.163-4
- Fixed debug conditional build (rfbz #3715)

* Tue Jul 14 2015 Julian Sikorski <belegdol@fedoraproject.org> - 0.163-3
- Fixed arm build
- Added crosshairpath to default .ini, removed memcard_directory
- Further spec cleanups

* Mon Jul 13 2015 Julian Sikorski <belegdol@fedoraproject.org> - 0.163-2
- Added ExcludeArch: %%{arm}

* Sun Jul 05 2015 Julian Sikorski <belegdol@fedoraproject.org> - 0.163-1
- Updated to 0.163
- Cleaned up the spec file further
- Dropped upstreamed patches
- Patched to use system PortAudio
- Added more workarouds for low memory on the builder
- Replaced wildcards with || approach
- Fixed parallel building

* Sun Jun 07 2015 Julian Sikorski <belegdol@fedoraproject.org> - 0.162-1
- Updated to 0.162
- Adapted to the new build system
- Cleaned up the .spec file considerably 

* Sun Mar 29 2015 Julian Sikorski <belegdol@fedoraproject.org> - 0.160-1
- Updated to 0.160

* Thu Feb 26 2015 Julian Sikorski <belegdol@fedoraproject.org> - 0.159-1
- Updated to 0.159
- Updated the verbosebuild patch

* Wed Jan 28 2015 Julian Sikorski <belegdol@fedoraproject.org> - 0.158-1
- Updated to 0.158
- Updated the verbosebuild patch
- Patched to make build using system zlib and flac work

* Sat Jan 03 2015 Julian Sikorski <belegdol@fedoraproject.org> - 0.157-1
- Updated to 0.157
- Updated the verbosebuild patch

* Thu Nov 27 2014 Julian Sikorski <belegdol@fedoraproject.org> - 0.156-1
- Updated to 0.156
- Switched to SDL2

* Tue Nov 04 2014 Julian Sikorski <belegdol@fedoraproject.org> - 0.155-2
- Fixed the ini path correctly

* Wed Oct 15 2014 Julian Sikorski <belegdol@fedoraproject.org> - 0.155-1
- Updated to 0.155
- Fixed the knock-on effect of changed build order on ini file names
- Use system sqlite3

* Thu Jul 24 2014 Julian Sikorski <belegdol@fedoraproject.org> - 0.154-1
- Updated to 0.154
- Changed to build mess before mame

* Mon Apr 14 2014 Julian Sikorski <belegdol@fedoraproject.org> - 0.153-1
- Updated to 0.153

* Wed Jan 01 2014 Julian Sikorski <belegdol@fedoraproject.org> - 0.152-1
- Updated to 0.152

* Sun Nov 10 2013 Julian Sikorski <belegdol@fedoraproject.org> - 0.151-1
- Updated to 0.151
- Updated the verbosebuild patch
- Use system-wide portmidi
- Fedora 17 is long EOL, always use system-wide libjpeg
- Added a conditional N64 SIMD
- Added new man pages
- Only use assembly on supported architectures

* Mon Sep 30 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.150-2
- Rebuilt

* Thu Sep 19 2013 Julian Sikorski <belegdol@fedoraproject.org> - 0.150-1
- Updated to 0.150
- Fixed the cheatpath

* Wed Jul 24 2013 Julian Sikorski <belegdol@fedoraproject.org> - 0.149u1-1
- Updated to 0.149u1

* Tue Jun 11 2013 Julian Sikorski <belegdol@fedoraproject.org> - 0.149-1
- Updated to 0.149

* Mon May 20 2013 Julian Sikorski <belegdol@fedoraproject.org> - 0.148u5-1
- Updated to 0.148u5

* Tue Apr 30 2013 Julian Sikorski <belegdol@fedoraproject.org> - 0.148u4-1
- Updated to 0.148u4

* Tue Apr 09 2013 Julian Sikorski <belegdol@fedoraproject.org> - 0.148u3-1
- Updated to 0.148u3

* Tue Mar 19 2013 Julian Sikorski <belegdol@fedoraproject.org> - 0.148u2-1
- Updated to 0.148u2
- Switched to the qt debugger and adjusted BR accordingly
- Made it easy to build an svn snapshot

* Mon Feb 11 2013 Julian Sikorski <belegdol@fedoraproject.org> - 0.148u1-1
- Updated to 0.148u1
- Use system libjpeg on Fedora 18 too (RH bug #854695)

* Sat Jan 12 2013 Julian Sikorski <belegdol@fedoraproject.org> - 0.148-1
- Updated to 0.148

* Mon Dec 17 2012 Julian Sikorski <belegdol@fedoraproject.org> - 0.147u4-1
- Updated to 0.147u4
- Updated the lowmem workaround - the linker is not the culprit, dwz is
- BR: libjpeg-devel → libjpeg-turbo-devel
- Updated the verbosebuild patch

* Mon Nov 19 2012 Julian Sikorski <belegdol@fedoraproject.org> - 0.147u3-1
- Updated to 0.147u3

* Tue Oct 30 2012 Julian Sikorski <belegdol@fedoraproject.org> - 0.147u2-1
- Updated to 0.147u2
- Conditionalised the low memory workaround
- Use system libjpeg-turbo on Fedora 19 and above
- Do not delete the entire obj/, leave the bits needed by the -debuginfo package

* Sat Oct 27 2012 Julian Sikorski <belegdol@fedoraproject.org> - 0.147u1-2
- Work around low memory on the RPM Fusion builder

* Mon Oct 08 2012 Julian Sikorski <belegdol@fedoraproject.org> - 0.147u1-1
- Updated to 0.147u1
- Dropped missing whatsnew.txt workaround
- Fixed incorrect paths in mess.ini
- Remove the object tree between mame and mess builds to prevent mess using /etc/mame

* Fri Sep 21 2012 Julian Sikorski <belegdol@fedoraproject.org> - 0.147-1
- Updated to 0.147
- Merged with mess
- Streamlined the directories installation
- Worked around missing whatsnew.txt
- Fixed mame.6 installation location
- Re-enabled ldplayer
- Cleaned-up ancient Obsoletes/Provides

* Mon Aug 20 2012 Julian Sikorski <belegdol@fedoraproject.org> - 0.146u5-1
- Updated to 0.146u5

* Mon Jul 30 2012 Julian Sikorski <belegdol@fedoraproject.org> - 0.146u4-1
- Updated to 0.146u4

* Sun Jul 15 2012 Julian Sikorski <belegdol@fedoraproject.org> - 0.146u3-1
- Updated to 0.146u3

* Mon Jul 02 2012 Julian Sikorski <belegdol@fedoraproject.org> - 0.146u2-1
- Updated to 0.146u2

* Mon Jun 11 2012 Julian Sikorski <belegdol@fedoraproject.org> - 0.146u1-1
- Updated to 0.146u1

* Tue May 22 2012 Julian Sikorski <belegdol@fedoraproject.org> - 0.146-1
- Updated to 0.146
- Added GLSL shaders to the installed files

* Mon May 07 2012 Julian Sikorski <belegdol@fedoraproject.org> - 0.145u8-1
- Updated to 0.145u8

* Sun Apr 22 2012 Julian Sikorski <belegdol@fedoraproject.org> - 0.145u7-1
- Updated to 0.145u7

* Sun Apr 08 2012 Julian Sikorski <belegdol@fedoraproject.org> - 0.145u6-1
- Updated to 0.154u6
- Dropped the systemlibs patch (no longer necessary)

* Sun Mar 25 2012 Julian Sikorski <belegdol@fedoraproject.org> - 0.145u5-1
- Updated to 0.145u5
- mame.1 → mame.6

* Sun Mar 11 2012 Julian Sikorski <belegdol@fedoraproject.org> - 0.145u4-1
- Updated to 0.145u4
- Updated the systemlibs patch (FLAC++ was removed)

* Mon Feb 27 2012 Julian Sikorski <belegdol@fedoraproject.org> - 0.145u3-1
- Updated to 0.145u3

* Sun Feb 26 2012 Julian Sikorski <belegdol@fedoraproject.org> - 0.145u2-1
- Updated to 0.145u2
- Re-enabled ldresample and ldverify

* Sun Feb 19 2012 Julian Sikorski <belegdol@fedoraproject.org> - 0.145u1-1
- Updated to 0.145u1
- Added artwork/* and hlsl/* to the installed files
- Fixed the line ending fix to spare all the *.png files
- Added bundled(libjpeg) and bundled(lzma-sdk) Provides
- Temporarily disabled ldresample and ldverify

* Mon Feb 06 2012 Julian Sikorski <belegdol@fedoraproject.org> - 0.145-1
- Updated to 0.145
- Updated the systemlibs patch

* Mon Jan 30 2012 Julian Sikorski <belegdol@fedoraproject.org> - 0.144u7-1
- Updated to 0.144u7
- Dropped upstreamed gcc-4.7 patch
- Patched to use system libflac, libjpeg needs more work

* Mon Jan 16 2012 Julian Sikorski <belegdol@fedoraproject.org> - 0.144u6-1
- Updated to 0.144u6

* Tue Jan 10 2012 Julian Sikorski <belegdol@fedoraproject.org> - 0.144u5-1
- Updated to 0.144u5
- Fixed building with gcc-4.7

* Sun Dec 25 2011 Julian Sikorski <belegdol@fedoraproject.org> - 0.144u4-1
- Updated to 0.144u4

* Wed Dec 14 2011 Julian Sikorski <belegdol@fedoraproject.org> - 0.144u3-1
- Updated to 0.144u3
- Dropped obsolete Group, Buildroot, %%clean and %%defattr

* Sun Dec 04 2011 Julian Sikorski <belegdol@fedoraproject.org> - 0.144u2-1
- Updated to 0.144u2

* Sun Nov 27 2011 Julian Sikorski <belegdol@fedoraproject.org> - 0.144u1-1
- Updated to 0.144u1

* Tue Nov 15 2011 Julian Sikorski <belegdol@fedoraproject.org> - 0.144-1
- Updated to 0.144
- Fixed whatsnew.txt encoding (cp1252 → utf-8)
- Updated Source0 URL

* Thu Oct 27 2011 Julian Sikorski <belegdol@fedoraproject.org> - 0.143u9-1
- Updated to 0.143u9

* Sun Oct 23 2011 Julian Sikorski <belegdol@fedoraproject.org> - 0.143u8-1
- Updated to 0.143u8

* Tue Oct 11 2011 Julian Sikorski <belegdol@fedoraproject.org> - 0.143u7-1
- Updated to 0.143u7

* Thu Sep 22 2011 Julian Sikorski <belegdol@fedoraproject.org> - 0.143u6-1
- Updated to 0.143u6
- Dropped upstreamed stacksmash patch

* Tue Sep 06 2011 Julian Sikorski <belegdol@fedoraproject.org> - 0.143u5-1
- Updated to 0.143u5
- Fixed stack smash in m68kmake.c

* Thu Aug 25 2011 Julian Sikorski <belegdol@fedoraproject.org> - 0.143u4-1
- Updated to 0.143u4

* Mon Aug 15 2011 Julian Sikorski <belegdol@fedoraproject.org> - 0.143u3-1
- Updated to 0.143u3

* Wed Jul 27 2011 Julian Sikorski <belegdol@fedoraproject.org> - 0.143u2-1
- Updated to 0.143u2

* Fri Jul 15 2011 Julian Sikorski <belegdol@fedoraproject.org> - 0.143u1-1
- Updated to 0.143u1

* Wed Jun 29 2011 Julian Sikorski <belegdol@fedoraproject.org> - 0.143-1
- Updated to 0.143

* Sun Jun 19 2011 Julian Sikorski <belegdol@fedoraproject.org> - 0.142u6-1
- Updated to 0.142u6

* Mon Jun 06 2011 Julian Sikorski <belegdol@fedoraproject.org> - 0.142u5-1
- Updated to 0.142u5

* Tue May 24 2011 Julian Sikorski <belegdol@fedoraproject.org> - 0.142u4-1
- Updated to 0.142u4

* Sun May 08 2011 Julian Sikorski <belegdol@fedoraproject.org> - 0.142u3-1
- Updated to 0.142u3
- Disabled ldplayer

* Mon Apr 25 2011 Julian Sikorski <belegdol@fedoraproject.org> - 0.142u2-1
- Updated to 0.142u2

* Tue Apr 19 2011 Julian Sikorski <belegdol@fedoraproject.org> - 0.142u1-1
- Updated to 0.142u1
- Updated the verbosebuild patch

* Sun Apr 03 2011 Julian Sikorski <belegdol@fedoraproject.org> - 0.142-1
- Updated to 0.142

* Fri Mar 25 2011 Julian Sikorski <belegdol@fedoraproject.org> - 0.141u4-1
- Updated to 0.141u4
- Re-enabled ldplayer
- Added support for hash files
- Sorted the %%install section alphabetically

* Mon Feb 28 2011 Julian Sikorski <belegdol@fedoraproject.org> - 0.141u3-1
- Updated to 0.141u3
- Filtered out redundant $RPM_OPT_FLAGS
- No longer enable joystick by default
- Provided an easy way to disable ldplayer
- Dropped upstreamed gcc-4.6 patch

* Wed Feb 09 2011 Julian Sikorski <belegdol@fedoraproject.org> - 0.141u2-1
- Updated to 0.141u2

* Mon Jan 24 2011 Julian Sikorski <belegdol@fedoraproject.org> - 0.141u1-1
- Updated to 0.141u1
- Re-enabled the fortify patch
- Fixed building with gcc-4.6

* Thu Jan 13 2011 Julian Sikorski <belegdol@fedoraproject.org> - 0.141-1
- Updated to 0.141
- Temporarily dropped the fortify patch

* Thu Dec 09 2010 Julian Sikorski <belegdol@fedoraproject.org> - 0.140u2-1
- Updated to 0.140u2
- Added SDL_ttf-devel to BuildRequires, removed explicit SDL-devel

* Mon Nov 08 2010 Julian Sikorski <belegdol@fedoraproject.org> - 0.140u1-1
- Updated to 0.140u1

* Thu Oct 21 2010 Julian Sikorski <belegdol@fedoraproject.org> - 0.140-1
- Updated to 0.140
- Re-enabled ldplayer

* Sat Oct 16 2010 Julian Sikorski <belegdol@fedoraproject.org> - 0.139u4-1
- Updated to 0.139u4

* Thu Oct 14 2010 Nicolas Chauvet <kwizart@gmail.com> - 0.139u3-2
- Rebuilt for gcc bug

* Sun Sep 19 2010 Julian Sikorski <belegdol@fedoraproject.org> - 0.139u3-1
- Updated to 0.139u3
- Updated the verbosebuild patch

* Tue Aug 31 2010 Julian Sikorski <belegdol@fedoraproject.org> - 0.139u2-1
- Updated to 0.139u2

* Fri Aug 13 2010 Julian Sikorski <belegdol@fedoraproject.org> - 0.139u1-1
- Updated to 0.139u1

* Thu Jul 29 2010 Julian Sikorski <belegdol@fedoraproject.org> - 0.139
- Updated to 0.139

* Thu Jul 22 2010 Julian Sikorski <belegdol@fedoraproject.org> - 0.138u4-1
- Updated to 0.138u4
- Install the new manpages

* Thu Jul 08 2010 Julian Sikorski <belegdol@fedoraproject.org> - 0.138u3-1
- Updated to 0.138u3
- Updated the verbosebuild patch
- Disabled ldplayer since it does not build ATM (mametesters #3930)

* Thu Jun 17 2010 Julian Sikorski <belegdol@fedoraproject.org> - 0.138u2-1
- Updated to 0.138u2
- Adjusted the license tag - it concerns the binary, not the source

* Fri May 28 2010 Julian Sikorski <belegdol@fedoraproject.org> - 0.138u1-1
- Updated to 0.138u1

* Sun May 16 2010 Julian Sikorski <belegdol@fedoraproject.org> - 0.138-1
- Updated to 0.138

* Wed May 05 2010 Julian Sikorski <belegdol@fedoraproject.org> - 0.137u4-1
- Updated to 0137u4

* Thu Apr 22 2010 Julian Sikorski <belegdol@fedoraproject.org> - 0.137u3-1
- Updated to 0137u3
- Dropped upstreamed ppc64 patch
- Moved rpm patches application after upstream ones

* Fri Apr 09 2010 Julian Sikorski <belegdol@fedoraproject.org> - 0.137u2-1
- Updated to 0137u2

* Sun Mar 21 2010 Julian Sikorski <belegdol@fedoraproject.org> - 0.137-4
- Stripped @ from the commands to make the build more verbose

* Sun Mar 21 2010 Julian Sikorski <belegdol@fedoraproject.org> - 0.137-3
- Dropped suffix64
- Added ppc64 autodetection support
- Re-diffed the fortify patch

* Sat Mar 20 2010 Julian Sikorski <belegdol@fedoraproject.org> - 0.137-2
- Changed the versioning scheme to include the dot
- Changed the source URL to point to aarongiles.com mirror directly
- Added missing application of the fortify patch
- Added sparc64 and s390 to architectures getting suffix64
- Removed duplicate license.txt

* Thu Mar 11 2010 Julian Sikorski <belegdol@fedoraproject.org> - 0137-1
- Initial package based on sdlmame
