# $Id: gstreamer-plugins-ugly.spec 5453 2007-05-31 10:59:47Z thias $
# Authority: matthias
# ExclusiveDist: fc5 fc6 el5 fc7

%define majorminor   0.10
%define gstreamer    gstreamer

%define gst_minver   0.10.6
%define gstpb_minver 0.10.3

Summary: GStreamer streaming media framework "ugly" plug-ins
Name: gstreamer-plugins-ugly
Version: 0.10.19
Release: 7%{?dist}
License: LGPLv2+
Group: Applications/Multimedia
URL: http://gstreamer.freedesktop.org/
Source: http://gstreamer.freedesktop.org/src/gst-plugins-ugly/gst-plugins-ugly-%{version}.tar.xz
# Backport from upstream cvs to fix asf seeking, drop on next upstream rebase
Patch0: gstasfdemux.patch
# Backport from upstream cvs to fix playback of certain mp3 streams
Patch1: gst-plugins-ugly-0.10.9-gstmpegaudioparse.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: %{gstreamer} >= %{gst_minver}
BuildRequires: %{gstreamer}-devel >= %{gst_minver}
BuildRequires: %{gstreamer}-plugins-base-devel >= %{gstpb_minver}

BuildRequires: gettext-devel

BuildRequires: libsidplay-devel >= 1.36.0
BuildRequires: a52dec-devel >= 0.7.3
#BuildRequires: libdvdnav-devel >= 0.1.3
BuildRequires: libdvdread-devel >= 0.9.0
BuildRequires: lame-devel >= 3.89
BuildRequires: libid3tag-devel >= 0.15.0
BuildRequires: libmad-devel >= 0.15.0
BuildRequires: libmpeg2-devel >= 0.4.0
BuildRequires: liboil-devel
BuildRequires: libcdio-devel

Provides: gstreamer-sid = %{version}-%{release}
Provides: gstreamer-lame = %{version}-%{release}
Provides: gstreamer-mad = %{version}-%{release}
Provides: gstreamer-a52dec = %{version}-%{release}
#Provides: gstreamer-dvdnav = %{version}-%{release}
Provides: gstreamer-dvdread = %{version}-%{release}
Provides: gstreamer-mpeg2dec = %{version}-%{release}

%description
GStreamer is a streaming media framework, based on graphs of elements which
operate on media data.

This package contains well-written plug-ins that can't be shipped in
gstreamer-plugins-good because:
- the license is not LGPL
- the license of the library is not LGPL
- there are possible licensing issues with the code.


%prep
%setup -q -n gst-plugins-ugly-%{version}
#%patch0 -p1
#%patch1 -p1


%build
%configure \
    --with-package-name="gst-plugins-bad rpmfusion rpm" \
    --with-package-origin="http://rpmfusion.org/" \
    --enable-debug \
    --disable-static \
    --disable-cdio \
    --disable-amrnb \
    --disable-amrwb
%{__make} %{?_smp_mflags}


%install
%{__rm} -rf %{buildroot}
%makeinstall
%find_lang gst-plugins-ugly-%{majorminor}

# Clean out files that should not be part of the rpm.
%{__rm} -f %{buildroot}%{_libdir}/gstreamer-%{majorminor}/*.la
%{__rm} -f %{buildroot}%{_libdir}/*.la


%clean
%{__rm} -rf %{buildroot}


%files -f gst-plugins-ugly-%{majorminor}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING README REQUIREMENTS
# Plugins without external dependencies
%{_libdir}/gstreamer-%{majorminor}/libgstasf.so
%{_libdir}/gstreamer-%{majorminor}/libgstdvdlpcmdec.so
%{_libdir}/gstreamer-%{majorminor}/libgstdvdsub.so
%{_libdir}/gstreamer-%{majorminor}/libgstiec958.so
%{_libdir}/gstreamer-%{majorminor}/libgstmpegaudioparse.so
%{_libdir}/gstreamer-%{majorminor}/libgstmpegstream.so
%{_libdir}/gstreamer-%{majorminor}/libgstrmdemux.so
# Plugins with external dependencies
%{_libdir}/gstreamer-%{majorminor}/libgsta52dec.so
#%{_libdir}/gstreamer-%{majorminor}/libgstcdio.so
#%{_libdir}/gstreamer-%{majorminor}/libgstdvdnav.so
%{_libdir}/gstreamer-%{majorminor}/libgstdvdread.so
%{_libdir}/gstreamer-%{majorminor}/libgstlame.so
%{_libdir}/gstreamer-%{majorminor}/libgstmad.so
%{_libdir}/gstreamer-%{majorminor}/libgstmpeg2dec.so
#%{_libdir}/gstreamer-%{majorminor}/libgstsid.so
%{_libdir}/gstreamer-%{majorminor}/libgsttwolame.so
%{_libdir}/gstreamer-%{majorminor}/libgstx264.so
%{_datadir}/gstreamer-%{majorminor}/presets/GstX264Enc.prs*

%changelog
* Wed Oct 21 2015 Liu Di <liudidi@gmail.com> - 0.10.19-7
- 为 Magic 3.0 重建

* Thu Apr 17 2014 Liu Di <liudidi@gmail.com> - 0.10.19-6
- 为 Magic 3.0 重建

* Thu Apr 17 2014 Liu Di <liudidi@gmail.com> - 0.10.19-5
- 为 Magic 3.0 重建

* Fri Apr 11 2014 Liu Di <liudidi@gmail.com> - 0.10.19-4
- 为 Magic 3.0 重建

* Sat Jul 06 2013 Liu Di <liudidi@gmail.com> - 0.10.19-3
- 为 Magic 3.0 重建

* Tue Nov  4 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.9-2
- Fix decoding of certain mp3 files (rpmfusion bug 108)

* Sat Sep 14 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.9-1
- New upstream release 0.10.9

* Fri Aug 15 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.8-3
- Fix building of dvdread plugin with libdvdread includes rename

* Wed Jul 23 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.8-2
- Release bump for rpmfusion

* Thu May 22 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.8-1
- New upstream release 0.10.8
- Drop upstreamed patches

* Sun Feb 24 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.7-1
- New upstream release 0.10.7
- Drop upstreamed patches

* Tue Dec 18 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.6-5
- Fix a crash when reading certain DVD's (livna #1770, gnome #358891)

* Sun Dec  9 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.6-4
- Add patch which makes asf ask its source if it can convert a timestamp
  to a byte offset before doing byte based seeking, this makes mms/mmsh
  seeking (supported in gstreamer-plugins-bad-0.10.5-12) much smoother,
  as gstmmssrc can actually do that

* Mon Nov 26 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.6-3
- Rebuild for new libdvdread (bz 1738)

* Mon Oct  8 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.6-2
- Merge livna spec bugfixes into freshrpms spec for rpmfusion:
- Set release to 2 to be higher as both livna and freshrpms latest release
- Set package name and origin to rpmfusion
- Remove amrnb plugin because of licensing issues
- Update license tag in accordance with new license tag guidelines
- Add a patch to fix "streaming task paused, reason error (-5)" with certain
  mp3's (livna bug 1625)
- Build in livna development for testing and for new ffmpeg in livna

* Tue Aug 21 2007 Matthias Saou <http://freshrpms.net/> 0.10.6-1
- Update to 0.10.6.

* Wed Mar 30 2007 Matthias Saou <http://freshrpms.net/> 0.10.5-2
- Remove gtk-doc entirely, do devel package too.

* Fri Dec 15 2006 Matthias Saou <http://freshrpms.net/> 0.10.5-1
- Update to 0.10.5.
- Remove no longer needed AC3 sound patch.

* Sun Nov 26 2006 Paulo Roma <roma@lcg.ufrj.br> 0.10.4-3
- Patched to fix AC3 sound.

* Tue Oct 17 2006 Matthias Saou <http://freshrpms.net/> 0.10.4-2
- Include translations which are now built.

* Sun Sep 17 2006 Matthias Saou <http://freshrpms.net/> 0.10.4-1
- Update to 0.10.4.

* Wed Apr 19 2006 Matthias Saou <http://freshrpms.net/> 0.10.3-1
- Update to 0.10.3.
- Remove no longer needed asfdemux fixes patch.
- Include new dvdsub plugin.
- Still don't add and include dvdnav plugin, "not stable yet".

* Tue Mar 28 2006 Matthias Saou <http://freshrpms.net/> 0.10.2-2
- Include backported asfdemux fixes patch from Daniel S. Rogers.

* Wed Feb 22 2006 Matthias Saou <http://freshrpms.net/> 0.10.2-1
- Update to 0.10.2.
- Add libgstasf.so.
- Enable re-added libgstdvdread.so.

* Thu Jan 19 2006 Matthias Saou <http://freshrpms.net/> 0.10.1-1
- Update to 0.10.1.

* Fri Dec 16 2005 Matthias Saou <http://freshrpms.net/> 0.10.0.1-1
- Update to CVS snapshot.
- Enable amrnb support.

* Mon Dec 05 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.10.0-0.gst.1
- new release

* Thu Dec 01 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.7-0.gst.1
- new release with 0.10 major/minor
- added mpegstream

* Sat Nov 12 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- new release

* Tue Oct 25 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.4-0.gst.1
- added a52dec plugin
- new release

* Mon Oct 03 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.3-0.gst.1
- new release
- add -devel and -docs

* Fri Sep 02 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- clean out for split into ugly

* Mon Feb 14 2005 Christian Schaller <christian at fluendo dot com>
- Add vnc plugin

* Wed Jan 19 2005 Christian Schaller <christian at fluendo dot com>
- add dv1394 plugin

* Wed Dec 22 2004 Christian Schaller <christian at fluendo dot com>
- Add -plugins- to plugin names

* Thu Dec  9 2004 Christian Schaller <christian a fluendo dot com>
- Add the mms plugin

* Wed Oct 06 2004 Christian Schaller <christian at fluendo dot com>
- Add Wim's new mng decoder plugin
- add shout2 plugin for Zaheer, hope it is correctly done :)

* Wed Sep 29 2004 Christian Schaller <uraeus at gnome dot org>
- Fix USE statement for V4L2

* Thu Sep 28 2004 Christian Schaller <uraeus at gnome dot org>
- Remove kio plugin (as it was broken)

* Wed Sep 21 2004 Christian Schaller <uraeus at gnome dot org>
- Reorganize SPEC to fit better with fedora.us and freshrpms.net packages
- Make sure gstinterfaces.so is in the package
- Add all new plugins

* Mon Mar 15 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- put back media-info
- add ffmpegcolorspace plugin

* Sun Mar 07 2004 Christian Schaller <Uraeus@gnome.org>
- Remove rm commands for media-info stuff
- Add libdir/*

* Thu Mar 04 2004 Christian Schaller <Uraeus@gnome.org>
- Add missing gconf schema install in %%post

* Tue Mar 02 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- Libraries/Multimedia doesn't exist, remove it

* Tue Mar 02 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- added speex plugin.

* Mon Mar 01 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- Cleaned up the mess.  Could we PLEASE keep this sort of organized and
- alphabetic for easy lookup ?

* Fri Feb 13 2004 Christian Schaller <Uraeus@gnome.org>
- Added latest new headers

* Wed Jan 21 2004 Christian Schaller <Uraeus@gnome.org>
- added NAS plugin
- added i18n locale dir

* Fri Jan 16 2004 Christian Schaller <uraeus@gnome.org>
- added libcaca plugin
- added libgstcolorspace - fixed name of libgsthermescolorspace

* Wed Jan 14 2004 Christian Schaller <uraeus@gnome.org>
- Add gamma plugin
- Have the pixbuf plugin deleted for now

* Wed Dec 18 2003 Christian Schaller <Uraeus@gnome.org>
- remove gsttagediting.h as it is gone
- replace it with gst/tag/tag.h

* Sun Nov 23 2003 Christian Schaller <Uraeus@gnome.org>
- Update spec file for latest changes
- add faad plugin

* Thu Oct 16 2003 Christian Schaller <Uraeus@gnome.org>
- Add new colorbalance and tuner and xoverlay stuff
- Change name of kde-audio-devel to arts-devel

* Sat Sep 27 2003 Christian Schaller <Uraeus@gnome.org>
- Add majorminor to man page names
- add navigation lib to package

* Tue Sep 11 2003 Christian Schaller <Uraeus@gnome.org>
- Add -%%{majorminor} to each instance of gst-register

* Tue Aug 19 2003 Christian Schaller <Uraeus@Gnome.org>
- Add new plugins

* Sat Jul 12 2003 Thomas Vander Stichele <thomas at apestaart dot org>
- move gst/ mpeg plugins to base package
- remove hermes conditional from snapshot
- remove one instance of resample plugin
- fix up silly versioned plugins efence and rmdemux

* Sat Jul 05 2003 Christian Schaller <Uraeus@gnome.org>
- Major overhaul of SPEC file to make it compatible with what Red Hat ships
  as default
- Probably a little less sexy, but cross-distro SPEC files are a myth anyway
  so making it convenient for RH users wins out
- Keeping conditionals even with new re-org so that developers building the
  RPMS don't need everything installed
- Add bunch of obsoletes to ease migration from earlier official GStreamer RPMS
- Remove plugins that doesn't exist anymore

* Sun Mar 02 2003 Christian Schaller <Uraeus@gnome.org>
- Remove USE_RTP statement from RTP plugin
- Move RTP plugin to no-deps section

* Sat Mar 01 2003 Christian Schaller <Uraeus@gnome.org>
- Remove videosink from SPEC
* Thu Jan 23 2003 Thomas Vander Stichele <thomas at apestaart dot org>
- various fixes
- make video output packages provide gstreamer-videosink

* Thu Jan 23 2003 Thomas Vander Stichele <thomas at apestaart dot org>
- split out ffmpeg stuff to separate plugin

* Fri Dec 27 2002 Thomas Vander Stichele <thomas at apestaart dot org>
- add virtual provides for audio sources and sinks

* Sun Dec 15 2002 Christian Schaller <Uraeus@linuxrising.org>
- Update mpeg2dec REQ to be 0.3.1

* Tue Dec 10 2002 Thomas Vander Stichele <thomas at apestaart dot org>
- only install schema once
- move out devel lib stuff to -devel package

* Sun Dec 08 2002 Thomas Vander Stichele <thomas at apestaart dot org>
- fix location of libgstpng
- changes for parallel installability

* Thu Nov 28 2002 Christian Schaller <Uraeus@linuxrising.org>
- Put in libgstpng plugin
- rm the libgstmedia-info stuff until thomas think they are ready

* Fri Nov 01 2002 Thomas Vander Stichele <thomas at apestaart dot org>
- don't use compprep until ABI issues can be fixed

* Wed Oct 30 2002 Thomas Vander Stichele <thomas at apestaart dot org>
- added smpte plugin
- split out dvdnavread package
- fixed snapshot deps and added hermes conditionals

* Tue Oct 29 2002 Thomas Vander Stichele <thomas at apestaart dot org>
- added -play package, libs, and .pc files

* Thu Oct 24 2002 Christian Schaller <Uraeus@linuxrising.org>
- Added wavenc to audio formats package

* Sat Oct 20 2002 Christian Scchaller <Uraeus@linuxrising.org>
- Removed all .la files
- added separate non-openquicktime demuxer plugin
- added snapshot plugin
- added videotest plugin
- Split avi plugin out to avi and windec plugins since aviplugin do not depend on avifile
- Added cdplayer plugin

* Fri Sep 20 2002 Thomas Vander Stichele <thomas@apestaart.org>
- added gst-compprep calls

* Wed Sep 18 2002 Thomas Vander Stichele <thomas@apestaart.org>
- add gst-register-%%{majorminor} calls everywhere again since auto-reregister doesn't work
- added gstreamer-audio-formats to mad's requires since it needs the typefind
  to work properly

* Mon Sep 9 2002 Christian Schaller <Uraeus@linuxrising.org>
- Added v4l2 plugin
* Thu Aug 27 2002 Christian Schaller <Uraeus@linuxrising.org>
- Fixed USE_DV_TRUE to USE_LIBDV_TRUE
- Added Gconf and floatcast headers to gstreamer-plugins-devel package
- Added mixmatrix plugin to audio-effects package

* Thu Jul 11 2002 Thomas Vander Stichele <thomas@apestaart.org>
- fixed oss package to buildrequire instead of require glibc headers

* Mon Jul 08 2002 Thomas Vander Stichele <thomas@apestaart.org>
- fixed -devel package group

* Fri Jul 05 2002 Thomas Vander Stichele <thomas@apestaart.org>
- release 0.4.0 !
- added gstreamer-libs.pc
- removed all gst-register-%%{majorminor} calls since this should be done automatically now

* Thu Jul 04 2002 Thomas Vander Stichele <thomas@apestaart.org>
- fix issue with SDL package
- make all packages STRICTLY require the right version to avoid
  ABI issues
- make gst-plugins obsolete gst-plugin-libs
- also send output of gst-register-%%{majorminor} to /dev/null to lower the noise

* Wed Jul 03 2002 Thomas Vander Stichele <thomas@apestaart.org>
- require glibc-devel instead of glibc-kernheaders since the latter is only
  since 7.3 and glibc-devel pulls in the right package anyway

* Sun Jun 23 2002 Thomas Vander Stichele <thomas@apestaart.org>
- changed header location of plug-in libs

* Mon Jun 17 2002 Thomas Vander Stichele <thomas@apestaart.org>
- major cleanups
- adding gst-register-%%{majorminor} on postun everywhere
- remove ldconfig since we don't actually install libs in system dirs
- removed misc package
- added video-effects
- dot every Summary
- uniformify all descriptions a little

* Thu Jun 06 2002 Thomas Vander Stichele <thomas@apestaart.org>
- various BuildRequires: additions

* Tue Jun 04 2002 Thomas Vander Stichele <thomas@apestaart.org>
- added USE_LIBADSPA_TRUE bits to ladspa package

* Mon Jun 03 2002 Thomas Vander Stichele <thomas@apestaart.org>
- Added libfame package

* Mon May 12 2002 Christian Fredrik Kalager Schaller <Uraeus@linuxrising.org>
- Added jack, dxr3, http packages
- Added visualisation plug-ins, effecttv and synaesthesia
- Created devel package
- Removed gstreamer-plugins-libs package (moved it into gstreamer-plugins)
- Replaced prefix/dirname with _macros

* Mon May 06 2002 Thomas Vander Stichele <thomas@apestaart.org>
- added gstreamer-GConf package

* Wed Mar 13 2002 Thomas Vander Stichele <thomas@apestaart.org>
- added more BuildRequires and Requires
- rearranged some plug-ins
- added changelog ;)

