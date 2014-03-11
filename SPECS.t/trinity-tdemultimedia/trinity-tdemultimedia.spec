# If TDE is built in a specific prefix (e.g. /opt/trinity), the release will be suffixed with ".opt".
%if "%{?tde_prefix}" != "/usr"
%define _variant .opt
%endif

# TDE 3.5.13 specific building variables
%define tde_bindir %{tde_prefix}/bin
%define tde_datadir %{tde_prefix}/share
%define tde_docdir %{tde_datadir}/doc
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}

%define tde_tdeappdir %{tde_datadir}/applications/kde
%define tde_tdedocdir %{tde_docdir}/tde
%define tde_tdeincludedir %{tde_includedir}/tde
%define tde_tdelibdir %{tde_libdir}/trinity

%define _docdir %{tde_docdir}

# former extras bits
%define _with_akode --with-akode
## not currently compatible with libtunepimp-0.5 (only libtunepimp-0.4)
#define _with_musicbrainz --with-musicbrainz
%define _with_taglib --with-taglib

Name:		trinity-tdemultimedia
Summary:	Multimedia applications for the Trinity Desktop Environment (TDE)
Version:	3.5.13.2
Release:	1%{?dist}%{?_variant}

License:	GPLv2
Group:		Applications/Multimedia

Vendor:		Trinity Project
Packager:	Francois Andriot <francois.andriot@free.fr>
URL:		http://www.trinitydesktop.org/

Prefix:		%{tde_prefix}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:	kdemultimedia-trinity-%{version}.tar.xz


# RedHat Legacy patches (from Fedora 8)
Patch3:		kdemultimedia-3.4.0-xdg.patch
Patch5:		kdemultimedia-3.5.7-pthread.patch


Obsoletes:	trinity-kdemultimedia < %{version}-%{release}
Provides:	trinity-kdemultimedia = %{version}-%{release}
Obsoletes:	trinity-kdemultimedia-libs < %{version}-%{release}
Provides:	trinity-kdemultimedia-libs = %{version}-%{release}
Obsoletes:	trinity-kdemultimedia-extras < %{version}-%{release}
Provides:	trinity-kdemultimedia-extras = %{version}-%{release}
Obsoletes:	trinity-kdemultimedia-extras-libs < %{version}-%{release}
Provides:	trinity-kdemultimedia-extras-libs = %{version}-%{release}


BuildRequires: autoconf automake libtool m4
BuildRequires: trinity-tqtinterface-devel >= %{version}
BuildRequires: trinity-arts-devel >= %{version}
BuildRequires: trinity-tdelibs-devel >= %{version}
BuildRequires: qt-devel

BuildRequires: zlib-devel
BuildRequires: libvorbis-devel
BuildRequires: audiofile-devel
BuildRequires: desktop-file-utils
BuildRequires: libtheora-devel
BuildRequires: alsa-lib-devel 
BuildRequires: automake libtool
%{?_with_akode:BuildRequires: trinity-akode-devel}
%{?_with_musicbrainz:BuildRequires: libmusicbrainz-devel libtunepimp-devel}
%{?_with_taglib:BuildRequires: taglib-devel}
BuildRequires:	cdparanoia
BuildRequires:	trinity-akode-devel

%if 0%{?mgaversion} || 0%{?mdkversion}
BuildRequires:	%{_lib}gstreamer0.10-devel
BuildRequires:	%{_lib}flac-devel
BuildRequires:	libcdda-devel
BuildRequires:	%{_lib}xxf86dga-devel
BuildRequires:	%{_lib}xxf86vm-devel
BuildRequires:	%{_lib}xtst-devel
%else
BuildRequires:	gstreamer-devel
BuildRequires:	flac-devel
BuildRequires:	cdparanoia-devel
BuildRequires:	libXxf86dga-devel
BuildRequires:	libXxf86vm-devel
BuildRequires:	libXt-devel
%endif

# XINE support
%if 0%{?fedora} || 0%{?rhel} >= 5 || 0%{?suse_version} || 0%{?mgaversion} || 0%{?mdkversion}
%define with_xine 1
%if 0%{?mgaversion} || 0%{?mdkversion}
BuildRequires: %{_lib}xine-devel
%endif
%if 0%{?fedora} || 0%{?rhel}
BuildRequires: xine-lib-devel
%endif
%if 0%{?suse_version} >= 1220
BuildRequires: libxine-devel
%endif
%endif

Requires: trinity-artsbuilder = %{version}-%{release}
Requires: trinity-juk = %{version}-%{release}
%{?with_xine:Requires: trinity-kaboodle = %{version}-%{release}}
Requires: trinity-kaudiocreator = %{version}-%{release}
Requires: %{name}-kfile-plugins = %{version}-%{release}
Requires: %{name}-kappfinder-data = %{version}-%{release}
Requires: %{name}-kio-plugins = %{version}-%{release}
Requires: trinity-kmid = %{version}-%{release}
Requires: trinity-kmix = %{version}-%{release}
Requires: trinity-krec = %{version}-%{release}
Requires: trinity-kscd = %{version}-%{release}
Requires: trinity-libarts-akode = %{version}-%{release}
Requires: trinity-libarts-audiofile = %{version}-%{release}
Requires: trinity-libarts-mpeglib = %{version}-%{release}
%{?with_xine:Requires: trinity-libarts-xine = %{version}-%{release}}
Requires: trinity-libkcddb = %{version}-%{release}
Requires: trinity-mpeglib = %{version}-%{release}
Requires: trinity-noatun = %{version}-%{release}


%description
The Trinity Desktop Environment (TDE) is a GUI desktop for the X Window
System. The %{name} package contains multimedia applications for
TDE, including:
  artsbuilder, Synthesizer designer for aRts
  juk, a media player
  kmid, a midi player
  kmix, an audio mixer
  arts, additional functionality for the aRts sound system
  krec, a recording tool
  kscd, an Audio-CD player
  kaudiocreator, a graphical frontend for audio file creation 
  kaboodle, a media player
  noatun, a media player

%files

##########

%package -n trinity-artsbuilder
Summary:	Synthesizer designer for aRts
Group:		Applications/Multimedia

%description -n trinity-artsbuilder
This is the analog Realtime synthesizer's graphical design tool.

%files -n trinity-artsbuilder
%defattr(-,root,root,-)
%{tde_bindir}/artsbuilder
%{tde_bindir}/artscontrol
%{tde_bindir}/midisend
%{tde_libdir}/libartsbuilder.la
%{tde_libdir}/libartsbuilder.so.*
%{tde_libdir}/libartscontrolapplet.la
%{tde_libdir}/libartscontrolapplet.so.*
%{tde_libdir}/libartscontrolsupport.la
%{tde_libdir}/libartscontrolsupport.so.*
%{tde_libdir}/libartsgui_idl.la
%{tde_libdir}/libartsgui_idl.so.*
%{tde_libdir}/libartsgui_kde.la
%{tde_libdir}/libartsgui_kde.so.*
%{tde_libdir}/libartsgui.la
%{tde_libdir}/libartsgui.so.*
%{tde_libdir}/libartsmidi_idl.la
%{tde_libdir}/libartsmidi_idl.so.*
%{tde_libdir}/libartsmidi.la
%{tde_libdir}/libartsmidi.so.*
%{tde_libdir}/libartsmodulescommon.la
%{tde_libdir}/libartsmodulescommon.so.*
%{tde_libdir}/libartsmoduleseffects.la
%{tde_libdir}/libartsmoduleseffects.so.*
%{tde_libdir}/libartsmodulesmixers.la
%{tde_libdir}/libartsmodulesmixers.so.*
%{tde_libdir}/libartsmodules.la
%{tde_libdir}/libartsmodules.so.*
%{tde_libdir}/libartsmodulessynth.la
%{tde_libdir}/libartsmodulessynth.so.*
%{tde_libdir}/mcop/Arts/ArtsBuilderLoader.mcopclass
%{tde_libdir}/mcop/artsbuilder.mcopclass
%{tde_libdir}/mcop/artsbuilder.mcoptype
%{tde_libdir}/mcop/Arts/Button.mcopclass
%{tde_libdir}/mcop/Arts/EffectRackGuiFactory.mcopclass
%{tde_libdir}/mcop/Arts/Effect_WAVECAPTURE.mcopclass
%{tde_libdir}/mcop/Arts/Environment/Container.mcopclass
%{tde_libdir}/mcop/Arts/Environment/EffectRackItem.mcopclass
%{tde_libdir}/mcop/Arts/Environment/InstrumentItemGuiFactory.mcopclass
%{tde_libdir}/mcop/Arts/Environment/InstrumentItem.mcopclass
%{tde_libdir}/mcop/Arts/Environment/MixerItem.mcopclass
%{tde_libdir}/mcop/Arts/Fader.mcopclass
%{tde_libdir}/mcop/Arts/FiveBandMonoComplexEQGuiFactory.mcopclass
%{tde_libdir}/mcop/Arts/FiveBandMonoComplexEQ.mcopclass
%{tde_libdir}/mcop/Arts/FreeverbGuiFactory.mcopclass
%{tde_libdir}/mcop/Arts/GenericGuiFactory.mcopclass
%{tde_libdir}/mcop/Arts/GraphLine.mcopclass
%{tde_libdir}/mcop/artsgui.mcopclass
%{tde_libdir}/mcop/artsgui.mcoptype
%{tde_libdir}/mcop/Arts/HBox.mcopclass
%{tde_libdir}/mcop/Arts/Label.mcopclass
%{tde_libdir}/mcop/Arts/LayoutBox.mcopclass
%{tde_libdir}/mcop/Arts/LevelMeter.mcopclass
%{tde_libdir}/mcop/Arts/LineEdit.mcopclass
%{tde_libdir}/mcop/Arts/LittleStereoMixerChannelGuiFactory.mcopclass
%{tde_libdir}/mcop/Arts/LittleStereoMixerChannel.mcopclass
%{tde_libdir}/mcop/Arts/LocalFactory.mcopclass
%{tde_libdir}/mcop/Arts/MidiManager.mcopclass
%{tde_libdir}/mcop/artsmidi.mcopclass
%{tde_libdir}/mcop/artsmidi.mcoptype
%{tde_libdir}/mcop/Arts/MixerGuiFactory.mcopclass
%{tde_libdir}/mcop/artsmodulescommon.mcopclass
%{tde_libdir}/mcop/artsmodulescommon.mcoptype
%{tde_libdir}/mcop/artsmoduleseffects.mcopclass
%{tde_libdir}/mcop/artsmoduleseffects.mcoptype
%{tde_libdir}/mcop/artsmodules.mcopclass
%{tde_libdir}/mcop/artsmodules.mcoptype
%{tde_libdir}/mcop/artsmodulesmixers.mcopclass
%{tde_libdir}/mcop/artsmodulesmixers.mcoptype
%{tde_libdir}/mcop/artsmodulessynth.mcopclass
%{tde_libdir}/mcop/artsmodulessynth.mcoptype
%{tde_libdir}/mcop/Arts/MonoSimpleMixerChannelGuiFactory.mcopclass
%{tde_libdir}/mcop/Arts/MonoSimpleMixerChannel.mcopclass
%{tde_libdir}/mcop/Arts/MonoToStereo.mcopclass
%{tde_libdir}/mcop/Arts/PopupBox.mcopclass
%{tde_libdir}/mcop/Arts/Poti.mcopclass
%{tde_libdir}/mcop/Arts/SimpleMixerChannelGuiFactory.mcopclass
%{tde_libdir}/mcop/Arts/SimpleMixerChannel.mcopclass
%{tde_libdir}/mcop/Arts/SpinBox.mcopclass
%{tde_libdir}/mcop/Arts/StereoBalanceGuiFactory.mcopclass
%{tde_libdir}/mcop/Arts/StereoBalance.mcopclass
%{tde_libdir}/mcop/Arts/StereoCompressorGuiFactory.mcopclass
%{tde_libdir}/mcop/Arts/StereoFirEqualizerGuiFactory.mcopclass
%{tde_libdir}/mcop/Arts/StereoToMono.mcopclass
%{tde_libdir}/mcop/Arts/StereoVolumeControlGuiFactory.mcopclass
%{tde_libdir}/mcop/Arts/StereoVolumeControlGui.mcopclass
%{tde_libdir}/mcop/Arts/StructureBuilder.mcopclass
%{tde_libdir}/mcop/Arts/StructureDesc.mcopclass
%{tde_libdir}/mcop/Arts/Synth_ATAN_SATURATE.mcopclass
%{tde_libdir}/mcop/Arts/Synth_AUTOPANNER.mcopclass
%{tde_libdir}/mcop/Arts/Synth_BRICKWALL_LIMITER.mcopclass
%{tde_libdir}/mcop/Arts/Synth_CAPTURE_WAV.mcopclass
%{tde_libdir}/mcop/Arts/Synth_CDELAY.mcopclass
%{tde_libdir}/mcop/Arts/Synth_COMPRESSOR.mcopclass
%{tde_libdir}/mcop/Arts/Synth_DATA.mcopclass
%{tde_libdir}/mcop/Arts/Synth_DEBUG.mcopclass
%{tde_libdir}/mcop/Arts/Synth_DELAY.mcopclass
%{tde_libdir}/mcop/Arts/Synth_DIV.mcopclass
%{tde_libdir}/mcop/Arts/Synth_ENVELOPE_ADSR.mcopclass
%{tde_libdir}/mcop/Arts/Synth_FM_SOURCE.mcopclass
%{tde_libdir}/mcop/Arts/Synth_FREEVERB.mcopclass
%{tde_libdir}/mcop/Arts/Synth_FX_CFLANGER.mcopclass
%{tde_libdir}/mcop/Arts/Synth_MIDI_DEBUG.mcopclass
%{tde_libdir}/mcop/Arts/Synth_MIDI_TEST.mcopclass
%{tde_libdir}/mcop/Arts/Synth_MOOG_VCF.mcopclass
%{tde_libdir}/mcop/Arts/Synth_NIL.mcopclass
%{tde_libdir}/mcop/Arts/Synth_NOISE.mcopclass
%{tde_libdir}/mcop/Arts/Synth_OSC.mcopclass
%{tde_libdir}/mcop/Arts/Synth_PITCH_SHIFT_FFT.mcopclass
%{tde_libdir}/mcop/Arts/Synth_PITCH_SHIFT.mcopclass
%{tde_libdir}/mcop/Arts/Synth_PLAY_PAT.mcopclass
%{tde_libdir}/mcop/Arts/Synth_PSCALE.mcopclass
%{tde_libdir}/mcop/Arts/Synth_RC.mcopclass
%{tde_libdir}/mcop/Arts/Synth_SEQUENCE_FREQ.mcopclass
%{tde_libdir}/mcop/Arts/Synth_SEQUENCE.mcopclass
%{tde_libdir}/mcop/Arts/Synth_SHELVE_CUTOFF.mcopclass
%{tde_libdir}/mcop/Arts/Synth_STD_EQUALIZER.mcopclass
%{tde_libdir}/mcop/Arts/Synth_STEREO_COMPRESSOR.mcopclass
%{tde_libdir}/mcop/Arts/Synth_STEREO_FIR_EQUALIZER.mcopclass
%{tde_libdir}/mcop/Arts/Synth_STEREO_PITCH_SHIFT_FFT.mcopclass
%{tde_libdir}/mcop/Arts/Synth_STEREO_PITCH_SHIFT.mcopclass
%{tde_libdir}/mcop/Arts/Synth_TREMOLO.mcopclass
%{tde_libdir}/mcop/Arts/Synth_VOICE_REMOVAL.mcopclass
%{tde_libdir}/mcop/Arts/Synth_WAVE_PULSE.mcopclass
%{tde_libdir}/mcop/Arts/Synth_WAVE_SOFTSAW.mcopclass
%{tde_libdir}/mcop/Arts/Synth_WAVE_SQUARE.mcopclass
%{tde_libdir}/mcop/Arts/Synth_WAVE_TRI.mcopclass
%{tde_libdir}/mcop/Arts/Synth_XFADE.mcopclass
%{tde_libdir}/mcop/Arts/VBox.mcopclass
%{tde_libdir}/mcop/Arts/VoiceRemovalGuiFactory.mcopclass
%{tde_libdir}/mcop/Arts/Widget.mcopclass
%{tde_tdeappdir}/artsbuilder.desktop
%{tde_tdeappdir}/artscontrol.desktop
%{tde_datadir}/apps/artsbuilder/
%{tde_datadir}/apps/artscontrol/
%{tde_datadir}/apps/kicker/applets/artscontrolapplet.desktop
%{tde_datadir}/icons/crystalsvg/*/actions/artsaudiomanager.png
%{tde_datadir}/icons/crystalsvg/*/actions/artsbuilderexecute.png
%{tde_datadir}/icons/crystalsvg/*/actions/artsenvironment.png
%{tde_datadir}/icons/crystalsvg/*/actions/artsfftscope.png
%{tde_datadir}/icons/crystalsvg/*/actions/artsmediatypes.png
%{tde_datadir}/icons/crystalsvg/*/actions/artsmidimanager.png
%{tde_datadir}/icons/crystalsvg/scalable/actions/artsaudiomanager.svgz
%{tde_datadir}/icons/crystalsvg/scalable/actions/artsenvironment.svgz
%{tde_datadir}/icons/crystalsvg/scalable/actions/artsfftscope.svgz
%{tde_datadir}/icons/crystalsvg/scalable/actions/artsmediatypes.svgz
%{tde_datadir}/icons/crystalsvg/scalable/actions/artsmidimanager.svgz
%{tde_datadir}/icons/hicolor/*/apps/artsbuilder.png
%{tde_datadir}/icons/hicolor/*/apps/artscontrol.png
%{tde_datadir}/icons/hicolor/scalable/apps/artsbuilder.svgz
%{tde_datadir}/icons/hicolor/scalable/apps/artscontrol.svgz
%{tde_datadir}/mimelnk/application/x-artsbuilder.desktop
%{tde_tdedocdir}/HTML/en/artsbuilder/

%post -n trinity-artsbuilder
/sbin/ldconfig
for f in crystalsvg hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-artsbuilder
/sbin/ldconfig
for f in crystalsvg hicolor locolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-juk
Summary:	Music organizer and player for Trinity
Group:		Applications/Multimedia

%description -n trinity-juk
JuK (pronounced "jook") is a jukebox and music manager for the TDE
desktop similar to jukebox software on other platforms such as
iTunes or RealOne.

Some of JuK's features include:
* Support for Ogg Vorbis and MP3 formats
* Tag editing support for both formats, including ID3v2 for MP3 files.
  Multitagging or editing a selection of multiple files at once is also
  supported
* Output to either the aRts, default KDE sound system, or GStreamer
* Management of your "collection" and multiple playlists
* Import and export to m3u playlists
* Binary caching of audio meta-data and playlist information for faster
  load times (starting with the second time you run JuK)
* Integration into TDE that allows drag-and-drop and clipboard usage
  with other TDE and X apps

%files -n trinity-juk
%defattr(-,root,root,-)
%{tde_bindir}/juk
%{tde_tdeappdir}/juk.desktop
%{tde_datadir}/apps/juk/
%{tde_datadir}/apps/konqueror/servicemenus/jukservicemenu.desktop
%{tde_datadir}/icons/crystalsvg/*/actions/juk_dock.png
%{tde_datadir}/icons/hicolor/*/apps/juk.png
%{tde_tdedocdir}/HTML/en/juk/

%post -n trinity-juk
for f in crystalsvg hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-juk
for f in crystalsvg hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%if 0%{?with_xine}
%package -n trinity-kaboodle
Summary:	light, embedded media player for Trinity
Group:		Applications/Multimedia

Requires:	trinity-libarts-xine = %{version}-%{release}

%description -n trinity-kaboodle
Kaboodle is a light, embedded media player, supporting both video and audio,
for TDE. It uses the aRts framework for playing media files.

%files -n trinity-kaboodle
%defattr(-,root,root,-)
%{tde_bindir}/kaboodle
%{tde_tdelibdir}/libkaboodlepart.la
%{tde_tdelibdir}/libkaboodlepart.so
%{tde_tdeappdir}/kaboodle.desktop
%{tde_datadir}/apps/kaboodle/
%{tde_datadir}/icons/hicolor/*/apps/kaboodle.png
%{tde_datadir}/services/kaboodle_component.desktop
%{tde_datadir}/services/kaboodleengine.desktop
%{tde_tdedocdir}/HTML/en/kaboodle/

%post -n trinity-kaboodle
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-kaboodle
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :
%endif

##########

%package -n trinity-kaudiocreator
Summary:	CD ripper and audio encoder frontend for Trinity
Group:		Applications/Multimedia

Requires:	%{name}-kio-plugins = %{version}-%{release}
Requires:	vorbis-tools
Requires:	flac

%description -n trinity-kaudiocreator
KAudioCreator is a tool for audio extraction (ripping) and encoding. It can
keep your WAV files, or convert them to Ogg/Vorbis, MP3, or FLAC. It also
searches CDDB to retrieve the information of the disk.

%files -n trinity-kaudiocreator
%defattr(-,root,root,-)
%{tde_bindir}/kaudiocreator
%{tde_tdeappdir}/kaudiocreator.desktop
%{tde_datadir}/apps/kaudiocreator/
%{tde_datadir}/apps/kconf_update/kaudiocreator-libkcddb.upd
%{tde_datadir}/apps/kconf_update/kaudiocreator-meta.upd
%{tde_datadir}/apps/kconf_update/upgrade-kaudiocreator-metadata.sh
%{tde_datadir}/apps/konqueror/servicemenus/audiocd_extract.desktop
%{tde_datadir}/config.kcfg/kaudiocreator.kcfg
%{tde_datadir}/config.kcfg/kaudiocreator_encoders.kcfg
%{tde_datadir}/icons/hicolor/*/apps/kaudiocreator.png
%{tde_datadir}/icons/locolor/*/apps/kaudiocreator.png
%{tde_tdedocdir}/HTML/en/kaudiocreator/

%post -n trinity-kaudiocreator
for f in hicolor locolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-kaudiocreator
for f in hicolor locolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package kfile-plugins
Summary:	au/avi/m3u/mp3/ogg/wav plugins for kfile
Group:		Applications/Multimedia

%description kfile-plugins
au/avi/m3u/mp3/ogg/wav file metainformation plugins for Trinity.

%files kfile-plugins
%defattr(-,root,root,-)
%{tde_tdelibdir}/kfile_au.la
%{tde_tdelibdir}/kfile_au.so
%{tde_tdelibdir}/kfile_avi.la
%{tde_tdelibdir}/kfile_avi.so
%{tde_tdelibdir}/kfile_flac.la
%{tde_tdelibdir}/kfile_flac.so
%{tde_tdelibdir}/kfile_m3u.la
%{tde_tdelibdir}/kfile_m3u.so
%{tde_tdelibdir}/kfile_mp3.la
%{tde_tdelibdir}/kfile_mp3.so
%{tde_tdelibdir}/kfile_mpc.la
%{tde_tdelibdir}/kfile_mpc.so
%{tde_tdelibdir}/kfile_mpeg.la
%{tde_tdelibdir}/kfile_mpeg.so
%{tde_tdelibdir}/kfile_ogg.la
%{tde_tdelibdir}/kfile_ogg.so
%{tde_tdelibdir}/kfile_sid.la
%{tde_tdelibdir}/kfile_sid.so
%{tde_tdelibdir}/kfile_theora.la
%{tde_tdelibdir}/kfile_theora.so
%{tde_tdelibdir}/kfile_wav.la
%{tde_tdelibdir}/kfile_wav.so
%{tde_datadir}/services/kfile_au.desktop
%{tde_datadir}/services/kfile_avi.desktop
%{tde_datadir}/services/kfile_flac.desktop
%{tde_datadir}/services/kfile_m3u.desktop
%{tde_datadir}/services/kfile_mp3.desktop
%{tde_datadir}/services/kfile_mpc.desktop
%{tde_datadir}/services/kfile_mpeg.desktop
%{tde_datadir}/services/kfile_ogg.desktop
%{tde_datadir}/services/kfile_sid.desktop
%{tde_datadir}/services/kfile_theora.desktop
%{tde_datadir}/services/kfile_wav.desktop

##########

%package kappfinder-data
Summary:	multimedia data for kappfinder-trinity
Group:		Applications/Multimedia

Requires: 	trinity-kappfinder

%description kappfinder-data
This package provides data on multimedia applications for kappfinder.

%files kappfinder-data
%defattr(-,root,root,-)
%{tde_datadir}/apps/kappfinder/*
%{tde_datadir}/desktop-directories/[kt]de-multimedia-music.directory
%{tde_prefix}/etc/xdg/menus/applications-merged/trinity-multimedia-music.menu

##########

%package kio-plugins
Summary:	Enables the browsing of audio CDs under Konqueror
Group:		Applications/Multimedia

%description kio-plugins
This package allow audio CDs to be browsed like a file system using
Konqueror and the audiocd:/ URL.

%files kio-plugins
%defattr(-,root,root,-)
%{tde_tdelibdir}/kcm_audiocd.la
%{tde_tdelibdir}/kcm_audiocd.so
%{tde_tdelibdir}/kio_audiocd.la
%{tde_tdelibdir}/kio_audiocd.so
%{tde_tdelibdir}/libaudiocd_encoder_flac.la
%{tde_tdelibdir}/libaudiocd_encoder_flac.so
%{tde_tdelibdir}/libaudiocd_encoder_lame.la
%{tde_tdelibdir}/libaudiocd_encoder_lame.so
%{tde_tdelibdir}/libaudiocd_encoder_vorbis.la
%{tde_tdelibdir}/libaudiocd_encoder_vorbis.so
%{tde_tdelibdir}/libaudiocd_encoder_wav.la
%{tde_tdelibdir}/libaudiocd_encoder_wav.so
%{tde_libdir}/libaudiocdplugins.so.*
%{tde_tdeappdir}/audiocd.desktop
%{tde_datadir}/apps/kconf_update/audiocd.upd
%{tde_datadir}/apps/kconf_update/upgrade-metadata.sh
%{tde_datadir}/config.kcfg/audiocd_lame_encoder.kcfg
%{tde_datadir}/config.kcfg/audiocd_vorbis_encoder.kcfg
%{tde_datadir}/services/audiocd.protocol
%{tde_tdedocdir}/HTML/en/kioslave/audiocd.docbook

%post kio-plugins
/sbin/ldconfig
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun kio-plugins
/sbin/ldconfig
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-kmid
Summary:	MIDI/karaoke player for Trinity
Group:		Applications/Multimedia

%description -n trinity-kmid
This package provides a MIDI and karaoke player for TDE.

%files -n trinity-kmid
%defattr(-,root,root,-)
%{tde_bindir}/kmid
%{tde_tdelibdir}/libkmidpart.la
%{tde_tdelibdir}/libkmidpart.so
%{tde_libdir}/libkmidlib.so.*
%{tde_tdeappdir}/kmid.desktop
%{tde_datadir}/apps/kmid/
%{tde_datadir}/icons/hicolor/*/apps/kmid.png
%{tde_datadir}/mimelnk/audio/x-karaoke.desktop
%{tde_datadir}/servicetypes/audiomidi.desktop
%{tde_tdedocdir}/HTML/en/kmid/

%post -n trinity-kmid
/sbin/ldconfig
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-kmid
/sbin/ldconfig
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-kmix
Summary:	Sound mixer applet for Trinity
Group:		Applications/Multimedia

%description -n trinity-kmix
This package includes TDE's dockable sound mixer applet.

%files -n trinity-kmix
%defattr(-,root,root,-)
%{tde_bindir}/kmix
%{tde_bindir}/kmixctrl
%{tde_tdelibdir}/kmix.la
%{tde_tdelibdir}/kmix.so
%{tde_tdelibdir}/kmix_panelapplet.la
%{tde_tdelibdir}/kmix_panelapplet.so
%{tde_tdelibdir}/kmixctrl.la
%{tde_tdelibdir}/kmixctrl.so
%{tde_libdir}/lib[kt]deinit_kmix.so
%{tde_libdir}/lib[kt]deinit_kmixctrl.so
%{tde_tdeappdir}/kmix.desktop
%{tde_datadir}/apps/kicker/applets/kmixapplet.desktop
%{tde_datadir}/apps/kmix/
%{tde_datadir}/autostart/kmix.desktop
%{tde_datadir}/autostart/restore_kmix_volumes.desktop
%{tde_datadir}/icons/hicolor/*/apps/kmix.png
%{tde_datadir}/services/kmixctrl_restore.desktop
%{tde_tdedocdir}/HTML/en/kmix/

%post -n trinity-kmix
/sbin/ldconfig
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-kmix
/sbin/ldconfig
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-krec
Summary:	Sound recorder utility for Trinity
Group:		Applications/Multimedia

%description -n trinity-krec
This is a sound recording utility for Trinity.

%files -n trinity-krec
%defattr(-,root,root,-)
%{tde_bindir}/krec
%{tde_tdelibdir}/kcm_krec.la
%{tde_tdelibdir}/kcm_krec.so
%{tde_tdelibdir}/kcm_krec_files.la
%{tde_tdelibdir}/kcm_krec_files.so
%{tde_tdelibdir}/krec.la
%{tde_tdelibdir}/krec.so
%{tde_tdelibdir}/libkrecexport_ogg.la
%{tde_tdelibdir}/libkrecexport_ogg.so
%{tde_tdelibdir}/libkrecexport_wave.la
%{tde_tdelibdir}/libkrecexport_wave.so
%{tde_libdir}/lib[kt]deinit_krec.so
%{tde_tdeappdir}/krec.desktop
%{tde_datadir}/apps/krec/
%{tde_datadir}/icons/hicolor/*/apps/krec.png
%{tde_datadir}/services/kcm_krec.desktop
%{tde_datadir}/services/kcm_krec_files.desktop
%{tde_datadir}/services/krec_exportogg.desktop
%{tde_datadir}/services/krec_exportwave.desktop
%{tde_datadir}/servicetypes/krec_exportitem.desktop
%{tde_tdedocdir}/HTML/en/krec/

%post -n trinity-krec
/sbin/ldconfig
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-krec
/sbin/ldconfig
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-kscd
Summary:	Audio CD player for Trinity
Group:		Applications/Multimedia

%description -n trinity-kscd
This is Trinity's audio CD player.

%files -n trinity-kscd
%defattr(-,root,root,-)
%{tde_bindir}/kscd
%{tde_bindir}/workman2cddb.pl
%{tde_tdeappdir}/kscd.desktop
%{tde_datadir}/apps/konqueror/servicemenus/audiocd_play.desktop
%{tde_datadir}/apps/kscd/
%{tde_datadir}/apps/profiles/kscd.profile.xml
%{tde_datadir}/config.kcfg/kscd.kcfg
%{tde_datadir}/icons/hicolor/*/apps/kscd.png
%{tde_datadir}/mimelnk/text/xmcd.desktop
%{tde_tdedocdir}/HTML/en/kscd/

%post -n trinity-kscd
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-kscd
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-libarts-akode
Summary:	Akode plugin for aRts
Group:		Environment/Libraries

%description -n trinity-libarts-akode
This package contains akode plugins for aRts.

%files -n trinity-libarts-akode
%defattr(-,root,root,-)
%{tde_libdir}/libarts_akode.so.*
%{tde_libdir}/libarts_akode.la
%{tde_libdir}/mcop/akodearts.mcoptype
%{tde_libdir}/mcop/akodearts.mcopclass
%{tde_libdir}/mcop/akodeMPCPlayObject.mcopclass
%{tde_libdir}/mcop/akodePlayObject.mcopclass
%{tde_libdir}/mcop/akodeSpeexStreamPlayObject.mcopclass
%{tde_libdir}/mcop/akodeVorbisStreamPlayObject.mcopclass
%{tde_libdir}/mcop/akodeXiphPlayObject.mcopclass

# -devel

%post -n trinity-libarts-akode
/sbin/ldconfig

%postun -n trinity-libarts-akode
/sbin/ldconfig

##########

%package -n trinity-libarts-audiofile
Summary:	Audiofile plugin for aRts
Group:		Environment/Libraries

%description -n trinity-libarts-audiofile
This package contains audiofile plugins for aRts.

%files -n trinity-libarts-audiofile
%defattr(-,root,root,-)
%{tde_libdir}/libarts_audiofile.so.*
%{tde_libdir}/libarts_audiofile.la
%{tde_libdir}/mcop/Arts/audiofilePlayObject.mcopclass
%{tde_libdir}/mcop/audiofilearts.mcopclass
%{tde_libdir}/mcop/audiofilearts.mcoptype

%post -n trinity-libarts-audiofile
/sbin/ldconfig

%postun -n trinity-libarts-audiofile
/sbin/ldconfig

##########

%package -n trinity-libarts-mpeglib
Summary:	Mpeglib plugin for aRts, supporting mp3 and mpeg audio/video
Group:		Environment/Libraries

%description -n trinity-libarts-mpeglib
This package contains the mpeglib aRts plugin, supporting mp3 and mpeg
audio and video.

This is the arts (TDE Sound daemon) plugin.

%files -n trinity-libarts-mpeglib
%defattr(-,root,root,-)
%{tde_bindir}/mpeglibartsplay
%{tde_libdir}/libarts_mpeglib-0.3.0.so.*
%{tde_libdir}/libarts_mpeglib.la
%{tde_libdir}/libarts_splay.so.*
%{tde_libdir}/libarts_splay.la
%{tde_libdir}/mcop/CDDAPlayObject.mcopclass
%{tde_libdir}/mcop/MP3PlayObject.mcopclass
%{tde_libdir}/mcop/NULLPlayObject.mcopclass
%{tde_libdir}/mcop/OGGPlayObject.mcopclass
%{tde_libdir}/mcop/SplayPlayObject.mcopclass
%{tde_libdir}/mcop/WAVPlayObject.mcopclass

%post -n trinity-libarts-mpeglib
/sbin/ldconfig

%postun -n trinity-libarts-mpeglib
/sbin/ldconfig

##########

%if 0%{?with_xine}
%package -n trinity-libarts-xine
Summary:	aRts plugin enabling xine support
Group:		Environment/Libraries

%description -n trinity-libarts-xine
This package contains aRts' xine plugin, allowing the use of the xine
multimedia engine though aRts.

%files -n trinity-libarts-xine
%defattr(-,root,root,-)
%{tde_tdelibdir}/videothumbnail.la
%{tde_tdelibdir}/videothumbnail.so
%{tde_libdir}/libarts_xine.so.*
%{tde_libdir}/libarts_xine.la
%{tde_libdir}/mcop/xineAudioPlayObject.mcopclass
%{tde_libdir}/mcop/xineVideoPlayObject.mcopclass
%{tde_datadir}/apps/videothumbnail/sprocket-large.png
%{tde_datadir}/apps/videothumbnail/sprocket-medium.png
%{tde_datadir}/apps/videothumbnail/sprocket-small.png
%{tde_datadir}/services/videothumbnail.desktop

%post -n trinity-libarts-xine
/sbin/ldconfig

%postun -n trinity-libarts-xine
/sbin/ldconfig
%endif

##########

%package -n trinity-libkcddb
Summary:	CDDB library for Trinity
Group:		Environment/Libraries

%description -n trinity-libkcddb
The Trinity native CDDB (CD Data Base) library, providing easy access to Audio
CD meta-information (track titles, artist information, etc.) from on-line
databases, for TDE applications.

%files -n trinity-libkcddb
%defattr(-,root,root,-)
%{tde_tdelibdir}/kcm_cddb.la
%{tde_tdelibdir}/kcm_cddb.so
%{tde_libdir}/libkcddb.so.*
%{tde_tdeappdir}/libkcddb.desktop
%{tde_datadir}/apps/kconf_update/kcmcddb-emailsettings.upd
%{tde_datadir}/config.kcfg/libkcddb.kcfg

%post -n trinity-libkcddb
/sbin/ldconfig
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-libkcddb
/sbin/ldconfig
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-mpeglib
Summary:	MP3 and MPEG-1 audio and video library
Group:		Environment/Libraries
Requires:	trinity-libarts-mpeglib = %{version}-%{release}

%description -n trinity-mpeglib
mpeglib is a MPEG-1 and MP3 audio and video library. It supports
MPEG-1 audio (layers 1, 2, 3), MPEG-1 video, MPEG-1 system layer,
and WAV playback

%files -n trinity-mpeglib
%defattr(-,root,root,-)
%{tde_bindir}/yaf-cdda
%{tde_bindir}/yaf-mpgplay
%{tde_bindir}/yaf-splay
%{tde_bindir}/yaf-tplay
%{tde_bindir}/yaf-vorbis
%{tde_bindir}/yaf-yuv
%{tde_libdir}/libmpeg-0.3.0.so
%{tde_libdir}/libyafcore.so
%{tde_libdir}/libyafxplayer.so

%post -n trinity-mpeglib
/sbin/ldconfig

%postun -n trinity-mpeglib
/sbin/ldconfig

##########

%package -n trinity-noatun
Summary:	Media player for Trinity
Group:		Applications/Multimedia

# 20120802: Hack to avoir dependency issue on MGA2 and MDV2011
%if 0%{?mgaversion} || 0%{?mdkversion}
Provides:	devel(libnoatunarts)
Provides:	devel(libnoatunarts(64bit))
%endif

%description -n trinity-noatun
Noatun is an aRts-based audio and video player for Trinity. It supports all
formats supported by your installation of aRts (including aRts plugins).

%files -n trinity-noatun
%defattr(-,root,root,-)
%{tde_bindir}/noatun
%{tde_libdir}/kconf_update_bin/noatun20update
%{tde_tdelibdir}/noatun.la
%{tde_tdelibdir}/noatun.so
%{tde_tdelibdir}/noatun_dcopiface.la
%{tde_tdelibdir}/noatun_dcopiface.so
%{tde_tdelibdir}/noatun_excellent.la
%{tde_tdelibdir}/noatun_excellent.so
%{tde_tdelibdir}/noatun_htmlexport.la
%{tde_tdelibdir}/noatun_htmlexport.so
%{tde_tdelibdir}/noatun_infrared.la
%{tde_tdelibdir}/noatun_infrared.so
%{tde_tdelibdir}/noatun_kaiman.la
%{tde_tdelibdir}/noatun_kaiman.so
%{tde_tdelibdir}/noatun_keyz.la
%{tde_tdelibdir}/noatun_keyz.so
%{tde_tdelibdir}/noatun_kjofol.la
%{tde_tdelibdir}/noatun_kjofol.so
%{tde_tdelibdir}/noatun_marquis.la
%{tde_tdelibdir}/noatun_marquis.so
%{tde_tdelibdir}/noatun_metatag.la
%{tde_tdelibdir}/noatun_metatag.so
%{tde_tdelibdir}/noatun_monoscope.la
%{tde_tdelibdir}/noatun_monoscope.so
%{tde_tdelibdir}/noatun_net.la
%{tde_tdelibdir}/noatun_net.so
%{tde_tdelibdir}/noatun_splitplaylist.la
%{tde_tdelibdir}/noatun_splitplaylist.so
%{tde_tdelibdir}/noatun_systray.la
%{tde_tdelibdir}/noatun_systray.so
%{tde_tdelibdir}/noatun_ui.la
%{tde_tdelibdir}/noatun_ui.so
%{tde_tdelibdir}/noatun_voiceprint.la
%{tde_tdelibdir}/noatun_voiceprint.so
%{tde_tdelibdir}/noatun_winskin.la
%{tde_tdelibdir}/noatun_winskin.so
%{tde_tdelibdir}/noatunsimple.la
%{tde_tdelibdir}/noatunsimple.so
%{tde_libdir}/libartseffects.la
%{tde_libdir}/libartseffects.so
%{tde_libdir}/lib[kt]deinit_noatun.so
%{tde_libdir}/libnoatun.so.*
%{tde_libdir}/libnoatunarts.la
%{tde_libdir}/libnoatunarts.so
%{tde_libdir}/libnoatuncontrols.so.*
%{tde_libdir}/libnoatuntags.so.*
%{tde_libdir}/libwinskinvis.la
%{tde_libdir}/libwinskinvis.so
%{tde_libdir}/mcop/ExtraStereo.mcopclass
%{tde_libdir}/mcop/ExtraStereoGuiFactory.mcopclass
%{tde_libdir}/mcop/Noatun/
%{tde_libdir}/mcop/RawWriter.mcopclass
%{tde_libdir}/mcop/VoiceRemoval.mcopclass
%{tde_libdir}/mcop/artseffects.mcopclass
%{tde_libdir}/mcop/artseffects.mcoptype
%{tde_libdir}/mcop/noatunarts.mcopclass
%{tde_libdir}/mcop/noatunarts.mcoptype
%{tde_libdir}/mcop/winskinvis.mcopclass
%{tde_libdir}/mcop/winskinvis.mcoptype
%{tde_tdeappdir}/noatun.desktop
%{tde_datadir}/apps/kconf_update/noatun.upd
%{tde_datadir}/apps/noatun/
%{tde_datadir}/icons/hicolor/*/apps/noatun.png
%{tde_datadir}/mimelnk/interface/x-winamp-skin.desktop
%{tde_tdedocdir}/HTML/en/noatun/

%post -n trinity-noatun
/sbin/ldconfig
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-noatun
/sbin/ldconfig
for f in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package devel
Summary:	Development files for %{name}, aRts and noatun plugins
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	trinity-tdelibs-devel >= 3.5.13

Obsoletes:	trinity-kdemultimedia-devel < %{version}-%{release}
Provides:	trinity-kdemultimedia-devel = %{version}-%{release}

%description devel
{summary}.

Install %{name}-devel if you wish to develop or compile any
applications using aRtsbuilder, aRtsmidi, aRtskde, aRts modules or
noatun plugins.

%files devel
%defattr(-,root,root,-)
%{tde_includedir}/*
%{tde_libdir}/libarts_akode.so
%{tde_libdir}/libarts_audiofile.so
%{tde_libdir}/libarts_mpeglib.so
%{tde_libdir}/libarts_splay.so
%{?with_xine:%{tde_libdir}/libarts_xine.so}
%{tde_libdir}/libartsbuilder.so
%{tde_libdir}/libartscontrolapplet.so
%{tde_libdir}/libartscontrolsupport.so
%{tde_libdir}/libartsgui.so
%{tde_libdir}/libartsgui_idl.so
%{tde_libdir}/libartsgui_kde.so
%{tde_libdir}/libartsmidi.so
%{tde_libdir}/libartsmidi_idl.so
%{tde_libdir}/libartsmodules.so
%{tde_libdir}/libartsmodulescommon.so
%{tde_libdir}/libartsmoduleseffects.so
%{tde_libdir}/libartsmodulesmixers.so
%{tde_libdir}/libartsmodulessynth.so
%{tde_libdir}/libaudiocdplugins.la
%{tde_libdir}/libaudiocdplugins.so
%{tde_libdir}/libkcddb.la
%{tde_libdir}/libkcddb.so
%{tde_libdir}/lib[kt]deinit_kmix.la
%{tde_libdir}/lib[kt]deinit_kmixctrl.la
%{tde_libdir}/lib[kt]deinit_krec.la
%{tde_libdir}/lib[kt]deinit_noatun.la
%{tde_libdir}/libkmidlib.la
%{tde_libdir}/libkmidlib.so
%{tde_libdir}/libmpeg.la
%{tde_libdir}/libmpeg.so
%{tde_libdir}/libnoatun.la
%{tde_libdir}/libnoatun.so
%{tde_libdir}/libnoatuncontrols.la
%{tde_libdir}/libnoatuncontrols.so
%{tde_libdir}/libnoatuntags.la
%{tde_libdir}/libnoatuntags.so
%{tde_libdir}/libyafcore.la
%{tde_libdir}/libyafxplayer.la

%post devel
/sbin/ldconfig

%postun devel
/sbin/ldconfig

##########

%if 0%{?suse_version}
%debug_package
%endif

##########


%prep
%setup -q -n kdemultimedia-trinity-%{version}
#%patch3 -p1 -b .xdg
#%patch5 -p1 -b .pthread

# Ugly hack to modify TQT include directory inside autoconf files.
# If TQT detection fails, it fallbacks to TQT4 instead of TQT3 !
%__sed -i "admin/acinclude.m4.in" \
  -e "s|/usr/include/tqt|%{tde_includedir}/tqt|g" \
  -e "s|kde_htmldir='.*'|kde_htmldir='%{tde_tdedocdir}/HTML'|g"

%__cp "/usr/share/aclocal/libtool.m4" "admin/libtool.m4.in"
%__cp "/usr/share/libtool/config/ltmain.sh" "admin/ltmain.sh" || %__cp "/usr/share/libtool/ltmain.sh" "admin/ltmain.sh"
%__make -f "admin/Makefile.common"

%__sed -i 's/TQT_PREFIX/TDE_PREFIX/g' cmake/modules/FindTQt.cmake

%build
unset QTDIR || : ; . /etc/profile.d/qt3.sh
export PATH="%{tde_bindir}:${PATH}"
export LDFLAGS="-L%{tde_libdir} -I%{tde_includedir}"
export PKG_CONFIG_PATH="%{tde_libdir}/pkgconfig:${PKG_CONFIG_PATH}"

# Required for some distro
export KDEDIRS=%{tde_prefix}

%configure  \
   --prefix=%{tde_prefix} \
   --exec-prefix=%{tde_prefix} \
   --bindir=%{tde_bindir} \
   --libdir=%{tde_libdir} \
   --includedir=%{tde_tdeincludedir} \
   --datadir=%{tde_datadir} \
   --enable-new-ldflags \
   --disable-dependency-tracking \
   --with-cdparanoia \
   --with-flac \
   --with-theora \
   --with-vorbis \
   --with-alsa \
   --with-gstreamer \
   --without-lame \
   --disable-debug \
   --disable-warnings \
   --enable-final \
   --disable-rpath \
  %{?_with_akode} %{!?_with_akode:--without-akode} \
  %{?_with_musicbrainz} %{!?_with_musicbrainz:--without-musicbrainz} \
  %{?_with_taglib} %{!?_with_taglib:--without-taglib} \
  %{?with_xine:--with-xine} %{!?with_xine:--without-xine} \
   --with-extra-includes="%{_includedir}/cdda:%{_includedir}/cddb:%{tde_includedir}/tqt:%{tde_tdeincludedir}/arts:%{tde_includedir}/artsc" \
   --enable-closure

%if 0
# Shitty hack for RHEL4 ...
if [ -d /usr/X11R6 ]; then
  export CMAKE_INCLUDE_PATH="${CMAKE_INCLUDE_PATH=}:/usr/X11R6/include:/usr/X11R6/%{_lib}"
  export CFLAGS="${CFLAGS} -I/usr/X11R6/include -L/usr/X11R6/%{_lib}"
  export CXXFLAGS="${CXXFLAGS} -I/usr/X11R6/include -L/usr/X11R6/%{_lib}"
fi

%if 0%{?rhel} || 0%{?fedora} || 0%{?suse_version}
%__mkdir_p build
cd build
%endif

%cmake \
  -DCMAKE_PREFIX_PATH=%{tde_prefix} \
  -DTDE_PREFIX=%{tde_prefix} \
  -DBIN_INSTALL_DIR=%{tde_bindir} \
  -DINCLUDE_INSTALL_DIR=%{tde_tdeincludedir} \
  -DLIB_INSTALL_DIR=%{tde_libdir} \
  -DSHARE_INSTALL_PREFIX=%{tde_datadir} \
  -DCMAKE_SKIP_RPATH="OFF" \
  -DBUILD_ALL=ON \
    ..
%endif

%__make %{?_smp_mflags} || %__make


%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf %{?buildroot} 
%__make install DESTDIR=%{buildroot}

# don't make these world-writeable
chmod go-w %{buildroot}%{tde_datadir}/apps/kscd/*

# locale's
HTML_DIR=$(kde-config --expandvars --install html)
if [ -d %{buildroot}$HTML_DIR ]; then
for lang_dir in %{buildroot}$HTML_DIR/* ; do
  if [ -d $lang_dir ]; then
    lang=$(basename $lang_dir)
    echo "%lang($lang) $HTML_DIR/$lang/*" >> %{name}.lang
    # replace absolute symlinks with relative ones
    pushd $lang_dir
      for i in *; do
        [ -d $i -a -L $i/common ] && ln -nsf ../common $i/common
      done
    popd
  fi
done
fi

# Moves the XDG configuration files to TDE directory
%__install -p -D -m644 \
	"%{?buildroot}%{_sysconfdir}/xdg/menus/applications-merged/kde-multimedia-music.menu" \
	"%{?buildroot}%{tde_prefix}/etc/xdg/menus/applications-merged/trinity-multimedia-music.menu"
%__rm -rf "%{?buildroot}%{_sysconfdir}/xdg"


%clean
%__rm -rf %{buildroot}


%changelog
* Sat Sep 29 2012 Francois Andriot <francois.andriot@free.fr> - 3.5.13.1-1
- Initial build for TDE 3.5.13.1
