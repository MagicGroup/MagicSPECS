Summary: A software wavetable MIDI synthesizer
Name: timidity++
Version: 2.13.2
Release: 25%{?dist}
Group: Applications/Multimedia
Source: http://downloads.sourceforge.net/timidity/TiMidity++-%{version}.tar.bz2
Source1: fedora-timidity.desktop
URL: http://timidity.sourceforge.net
Patch3: TiMidity++-2.13.0-detect.patch
Patch5: TiMidity++-2.13.0-64bit.patch
Patch6: TiMidity++-2.13.0-warnings.patch
Patch7: TiMidity++-2.13.2-flac-detect.patch
Patch8: TiMidity++-2.13.2-speex.patch
Patch9: TiMidity++-2.13.2-libao-first.patch
# The following patches are courtesy of Debian
Patch10: TiMidity++-2.13.2-man-pages.patch
Patch11: TiMidity++-2.13.2-misc-fixes.patch
Patch12: TiMidity++-2.13.2-mlutil.patch
Patch13: TiMidity++-2.13.2-flac.patch
# end Debian patches
Patch14: TiMidity++-2.13.2-ipv6.patch
Patch15: TiMidity++-2.13.2-dynlibroot.patch
Patch16: TiMidity++-2.13.2-cfgfile-name.patch
Patch17: TiMidity++-2.13.2-missing-protos.patch
Patch18: TiMidity++-2.13.2-fork-early.patch

License: GPLv2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: alsa-lib-devel ncurses-devel gtk2-devel
BuildRequires: libao-devel libvorbis-devel flac-devel speex-devel
BuildRequires: jack-audio-connection-kit-devel
BuildRequires: desktop-file-utils
Requires: soundfont2-default hicolor-icon-theme

%description
TiMidity++ is a MIDI format to wave table format converter and
player. Install timidity++ if you'd like to play MIDI files and your
sound card does not natively support wave table format.


%prep
%setup -q -n TiMidity++-%{version}
# Autodetect whether we should use aRts, esd, or neither
%patch3 -p1 -b .detect
# fix for x86_64 and s390x
%patch5 -p1 -b .64bit
%patch6 -p1 -b .warnings
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1


%build
export EXTRACFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE"
%configure --enable-dynamic --disable-dependency-tracking \
  --enable-interface=ncurses,vt100,alsaseq,server,network,gtk \
  --enable-audio=oss,alsa,ao,jack,vorbis,speex,flac
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}
echo "soundfont %{_datadir}/soundfonts/default.sf2" > \
  $RPM_BUILD_ROOT/%{_sysconfdir}/timidity++.cfg

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
desktop-file-install --vendor fedora              \
  --dir ${RPM_BUILD_ROOT}%{_datadir}/applications \
  %{SOURCE1}

mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/48x48/apps
install -p -m 644 interface/pixmaps/timidity.xpm \
  $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/48x48/apps/timidity.xpm


%clean
rm -rf $RPM_BUILD_ROOT


%post
# update icon themes
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
   %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%postun
# update icon themes
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
   %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README NEWS ChangeLog
%config(noreplace) %{_sysconfdir}/timidity++.cfg
%{_bindir}/*
%{_mandir}/*/*
%{_datadir}/applications/fedora-timidity.desktop
%{_datadir}/icons/hicolor/48x48/apps/timidity.xpm


%changelog
* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 2.13.2-25
- 为 Magic 3.0 重建

* Wed Feb 15 2012 Liu Di <liudidi@gmail.com> - 2.13.2-24
- 为 Magic 3.0 重建

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.13.2-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Nov  5 2010 Hans de Goede <hdegoede@redhat.com> - 2.13.2-22
- Drop arts and esd as supported outputs, arts is no longer used in kde4
  and esd has been dead for quite some time now. Since timidity++ does not
  have output-plugins, leaving these 2 enabled means that timidity++ often
  is the only thing on a system dragging in esound-libs and arts. If people
  for some reason still want to use esd or arts for sound output they can
  do so through libao
- Drop the don't compile jack for ppc64 hack, the toolchain issue we hit
  should be long fixed by now

* Thu Sep 02 2010 Rakesh Pandit <rakesh@fedoraproject.org> - 2.13.2-21
- Bump for libao

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.13.2-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun  3 2009 Hans de Goede <hdegoede@redhat.com> 2.13.2-19
- Don't crash when started in daemon mode (with -iAD) (#501051)

* Tue Mar 24 2009 Hans de Goede <hdegoede@redhat.com> 2.13.2-18
- Require soundfont2-default virtual provides instead of hardcoding
  PersonalCopy-Lite-soundfont (#491421)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.13.2-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat May  3 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 2.13.2-16
- Some small fixes to ipv6 support from upstream

* Thu Apr  3 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 2.13.2-15
- Fix missing prototype compiler warnings

* Sun Mar  9 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 2.13.2-14
- Fix local ipv6 clients being rejected when running in server mode

* Mon Mar  3 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 2.13.2-13
- Merge review fixes (bz 226492)
  - merge patch0 into patch16, drop patch0
  - Make License tag just GPLv2
  - Unify macros usage

* Thu Feb 28 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 2.13.2-12
- Stop shipping a timidity++-patches package, investigation into the license
  of the included patches has turned up doubts about the rights of the author
  of the midas SGI midi player to release these into the Public Domain
- Instead require PersonalCopy-Lite-soundfont, and point to PCLite.sf2 in
  timidity++.cfg
- Note PersonalCopy-Lite-soundfont also has a PersonalCopy-Lite-patches
  sub-package with the .sf2 file converted to GUS patch format for other
  applications who require timidity++-patches to get GUS format patches, this
  package contains an /etc/timidity.cfg file pointing to the gus patches,
  therefor the timidity++ package now ships a timidty++.cfg instead of a
  timidity.cfg
- Check for /etc/timidity++.cfg before trying /etc/timidity.cfg, see above for
  rationale

* Thu Feb 21 2008 Jindrich Novy <jnovy@redhat.com> 2.13.2-11
- rebuild

* Thu Feb 21 2008 Jindrich Novy <jnovy@redhat.com> 2.13.2-10
- don't free a constant string if -d is specified (#433756),
  thanks to Andrew Bartlett

* Wed Feb 20 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 2.13.2-9
- Add IPv6 support, patch by Milan Zazrivec (bz 198467)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.13.2-8
- Autorebuild for GCC 4.3

* Thu Jan 24 2008 Jindrich Novy <jnovy@redhat.com> 2.13.2-7
- merge review fixes, thanks to Mamoru Tasaka: (#226492)
  - update License tag (still unclear what to do with GUS patches)
  - remove useless unversioned obsolete timidity++-X11
  - substitute /etc with %%{_sysconfdir}
  - enable parallel build
  - preserve timestamps, tar unpacking is no more verbose
  - add docs

* Tue Dec 11 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 2.13.2-6
- Disable building of the jack output on powerpc64, as that mysteriously fails
  to build there.

* Mon Dec 10 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 2.13.2-5
- Add patches to fix detect and compile of speex and flac outputs
- Add various bugfixes from Debian
- Enable ogg, flac, speex, libao and jack output formats (bz 412431)
- Make libao the default output as libao support pulseaudio directly

* Sat Oct 13 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 2.13.2-4
- Split the patches of into a seperate sub package so that they can be used
  by other wavetable midi synthesizers, without dragging in a bunch of unwanted
  dependencies (bz 250735)
- There is no reason to install the icon in /usr/share/pixmaps if it also gets
  installed under /usr/share/icons
- Rewrite autodetection of wether to use esd, aRts or alsa as output patch,
  so that it actually works (bz 200688)

* Thu Oct 11 2007 Jindrich Novy <jnovy@redhat.com> 2.13.2-3
- fix typo in package description (#185328) 
- use RPM_OPT_FLAGS, make debuginfo package usable (#249968),
  thanks to Ville Skitta
- compile with GTK interface (#231745), thanks to Brian Jedsen
  
* Mon Sep 24 2007 Jindrich Novy <jnovy@redhat.com> 2.13.2-2
- spec/license fixes
  
* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.13.2-1.2.2
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.13.2-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.13.2-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Aug 26 2004 Thomas Woerner <twoerner@redhat.com> 2.13.0-3
- fixed esd output plugin to not output to stderr on fault (#130633)

* Mon Jul  5 2004 Thomas Woerner <twoerner@redhat.com> 2.13.0-2
- fixed configure options (#127190)

* Thu Jul  1 2004 Thomas Woerner <twoerner@redhat.com> 2.13.0-1
- new version 2.13.0
  - with alsa support (#117024, #123327)
  - working default output (#124774)
  - working ogg output (#124776)
- spec file fixes
- fixed some configure options
- added BuildRequires for ncurses-devel (#125028)

* Sat Jun 19 2004 Alan Cox <alan@redhat.com>
- fixed compiler reported bugs 

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Oct 21 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- add %%clean specfile target

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 11 2003 Thomas Woerner <twoerner@redhat.com> 2.11.3-7
- fix for x86_64 and s390x

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Mon Dec  9 2002 Thomas Woerner <twoerner@redhat.com> 2.11.3-5
- fixed dependency for autoconf

* Mon Jul 22 2002 Than Ngo <than@redhat.com> 2.11.3-4
- build against current libvorbis

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Jan 24 2002 Bernhard Rosenkraenzer <bero@redhat.com> 2.11.3-1
- Update to 2.11.3
- Extend the aRts output plugin to support KDE 3.x features
- Fix the dependency mess

* Wed Aug 22 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.10.4-2
- Finally managed to locate free versions of britepno.pat and pistol.pat
  (#50982)

* Sat Apr 14 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- 2.10.4

* Fri Feb 23 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Change timidity.cfg to work perfectly with both the real
  TiMidity++ and the timidity version used in kmidi
- Fix a typo in the GUS drumset #0

* Mon Jan  8 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Autodetect whether the aRts, esd or dsp backend should
  be used

* Thu Dec  7 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Add aRts (KDE 2.x) backend (Patches #1 and #2)

* Mon Nov 27 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 2.10.3a2
- Move the config file to the FHSly correct place, /etc/timidity.cfg
- Enable ogg/vorbis support, now that we're shipping it

* Thu Aug 3 2000 Tim Powers <timp@redhat.com>
- rebuilt against libpng-1.0.8

* Wed Aug  2 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Move instrument files to /usr/share/timidity, where it's actually looking
  for them (Bug #13932)
- 2.9.5 (bugfix release)

* Mon Jul 24 2000 Prospector <prospector@redhat.com>
- rebuilt

* Mon Jul 17 2000 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Jun 28 2000 Than Ngo <than@redhat.de>
- FHS fixes
- clean up specfile
- use RPM macros

* Sat Jun 17 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 2.9.4

* Wed Jan 19 2000 Tim Powoers <timp@redhat.com>
- bzipped source to conserve space

* Sat Aug 14 1999 Bill Nottingham <notting@redhat.com>
- add a changelog
- strip binaries
