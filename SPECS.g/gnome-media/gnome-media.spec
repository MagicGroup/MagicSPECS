%define glib2_version 2.4.0
%define pango_version 1.4.0
%define gtk3_version 2.99.0
%define libgnome_version 2.13.7
%define libgnomeui_version 2.13.2
%define gail_version 1.2
%define desktop_file_utils_version 0.2.90
%define gstreamer_version 0.10.3

%define gettext_package gnome-media-2.0

Summary:        GNOME media programs
Name:           gnome-media
Version:        3.4.0
Release:        4%{?dist}
License:        GPLv2+ and GFDL
Group:          Applications/Multimedia
#VCS: git:git://git.gnome.org/gnome-media
Source:         http://download.gnome.org/sources/%{name}/%{version}/%{name}-%{version}.tar.xz

URL:            http://www.gnome.org
ExcludeArch:    s390 s390x

Requires(post):  GConf2 >= 2.14
Requires(pre):   GConf2 >= 2.14
Requires(preun): GConf2 >= 2.14

Requires: gnome-icon-theme-symbolic

BuildRequires:  gtk3-devel >= %{gtk3_version}
BuildRequires:  GConf2-devel
BuildRequires:  desktop-file-utils >= %{desktop_file_utils_version}
BuildRequires:  gstreamer-devel >= %{gstreamer_version}
BuildRequires:  gstreamer-plugins-base-devel >= %{gstreamer_version}
BuildRequires:  libgnome-media-profiles-devel
BuildRequires:  gnome-doc-utils
BuildRequires:  intltool
BuildRequires:  control-center-devel
BuildRequires:  rarian-devel
BuildRequires:  rarian-compat

%description
This package contains a few media utilities for the GNOME desktop,
including a volume control and a configuration utility for audio profiles.

%package apps
Summary: Some media-related applications for the GNOME desktop
Group: Applications/Multimedia
Requires: %{name} = %{version}-%{release}

%description apps
This package contains an application to record and play sound files
in various formats and a configuration utility for the gstreamer media
framework.

%prep
%setup -q

%build
%configure \
        --disable-schemas-install \
        --enable-gnomecd=no \
        --enable-cddbslave=no \
        --enable-gstprops \
        --with-gnu-ld \
        --disable-scrollkeeper 
  
make %{?_smp_mflags} V=1

%install
make install DESTDIR=$RPM_BUILD_ROOT

# show in all
desktop-file-install --vendor gnome --delete-original       \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications             \
  $RPM_BUILD_ROOT%{_datadir}/applications/gnome-sound-recorder.desktop

desktop-file-install --vendor "" --delete-original          \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications             \
  $RPM_BUILD_ROOT%{_datadir}/applications/gstreamer-properties.desktop

rm -f $RPM_BUILD_ROOT%{_datadir}/applications/vumeter.desktop
rm -f $RPM_BUILD_ROOT%{_datadir}/applications/reclevel.desktop
rm -f $RPM_BUILD_ROOT%{_bindir}/vumeter

rm -rf $RPM_BUILD_ROOT%{_datadir}/gnome-media/sounds/
rm -rf $RPM_BUILD_ROOT%{_datadir}/sounds/

rm -rf $RPM_BUILD_ROOT/var/scrollkeeper

%find_lang %{gettext_package}
%find_lang gnome-sound-recorder --with-gnome
%find_lang gstreamer-properties --with-gnome
cat gnome-sound-recorder.lang >> apps.lang
cat gstreamer-properties.lang >> apps.lang

%post
touch --no-create %{_datadir}/icons/hicolor >&/dev/null || :

%post apps
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
gconftool-2 --makefile-install-rule \
    %{_sysconfdir}/gconf/schemas/gnome-sound-recorder.schemas \
    > /dev/null || :
touch --no-create %{_datadir}/icons/hicolor >&/dev/null || :

%pre
if [ "$1" -gt 1 ]; then
  export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
  if [ -f %{_sysconfdir}/gconf/schemas/gnome-cd.schemas ] ; then
    gconftool-2 --makefile-uninstall-rule \
      %{_sysconfdir}/gconf/schemas/gnome-cd.schemas \
      %{_sysconfdir}/gconf/schemas/CDDB-Slave2.schemas \
      > /dev/null || :
  fi
  if [ -f %{_sysconfdir}/gconf/schemas/gnome-sound-recorder.schemas ] ; then
    gconftool-2 --makefile-uninstall-rule \
      %{_sysconfdir}/gconf/schemas/gnome-sound-recorder.schemas \
      > /dev/null || :
  fi
  if [ -f %{_sysconfdir}/gconf/schemas/gnome-volume-control.schemas ] ; then
    gconftool-2 --makefile-uninstall-rule \
      %{_sysconfdir}/gconf/schemas/gnome-volume-control.schemas \
      > /dev/null || :
  fi
fi

%pre apps
if [ "$1" -gt 1 ]; then
  export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
  if [ -f %{_sysconfdir}/gconf/schemas/gnome-sound-recorder.schemas ] ; then
    gconftool-2 --makefile-uninstall-rule \
      %{_sysconfdir}/gconf/schemas/gnome-sound-recorder.schemas \
      > /dev/null || :
  fi
fi

%preun
if [ "$1" -eq 0 ]; then
  export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
  if [ -f %{_sysconfdir}/gconf/schemas/gnome-cd.schemas ] ; then
    gconftool-2 --makefile-uninstall-rule \
      %{_sysconfdir}/gconf/schemas/gnome-cd.schemas \
      %{_sysconfdir}/gconf/schemas/CDDB-Slave2.schemas \
      > /dev/null || :
  fi
  if [ -f %{_sysconfdir}/gconf/schemas/gnome-sound-recorder.schemas ] ; then
    gconftool-2 --makefile-uninstall-rule \
      %{_sysconfdir}/gconf/schemas/gnome-sound-recorder.schemas \
      > /dev/null || :
  fi
  if [ -f %{_sysconfdir}/gconf/schemas/gnome-volume-control.schemas ] ; then
    gconftool-2 --makefile-uninstall-rule \
      %{_sysconfdir}/gconf/schemas/gnome-volume-control.schemas \
      > /dev/null || :
  fi
fi

%preun apps
if [ "$1" -gt 1 ]; then
  export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
  if [ -f %{_sysconfdir}/gconf/schemas/gnome-sound-recorder.schemas ] ; then
    gconftool-2 --makefile-uninstall-rule \
      %{_sysconfdir}/gconf/schemas/gnome-sound-recorder.schemas \
      > /dev/null || :
  fi
fi

%postun
if [ $1 -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor >&/dev/null || :
  gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor >&/dev/null || :
fi

%postun apps
if [ $1 -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor >&/dev/null || :
  gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor >&/dev/null || :
fi

%posttrans
gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor >&/dev/null || :

%posttrans apps
gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor >&/dev/null || :

%files -f %{gettext_package}.lang
%defattr(-, root, root)
%doc AUTHORS COPYING NEWS README

%files apps -f apps.lang
%defattr(-, root, root)
%{_bindir}/gnome-sound-recorder
%{_datadir}/gnome-sound-recorder
%config %{_sysconfdir}/gconf/schemas/gnome-sound-recorder.schemas
%{_datadir}/applications/gnome-sound-recorder.desktop
%{_datadir}/icons/hicolor/*/apps/gnome-sound-recorder*

%{_bindir}/gstreamer-properties
%{_datadir}/gstreamer-properties
%{_datadir}/applications/gstreamer-properties.desktop
%{_datadir}/icons/hicolor/*/apps/gstreamer-properties*


%changelog
* Sun Mar 03 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 3.4.0-4
- Update source URL to correct version
- Disable scrollkeeper
- Remove unneeded BRs

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Mar 28 2012 Richard Hughes <hughsient@gmail.com> - 3.4.0-1
- Update to 3.4.0

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.91.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 2.91.2-8
- Rebuild for new libpng

* Wed Jul 20 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.2-7
- Rebuild

* Tue Feb 22 2011 Rakesh Pandit <rakesh@fedoraproject.org> 2.91.2-6
- Rebuild for new glade

* Fri Feb 11 2011 Matthias Clasen <mclasne@redhat.com> 2.91.2-5
- Rebuild against newr gtk

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.91.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan  7 2011 Matthias Clasen <mclasen@redhat.com> 2.91.2-3
- Rebuild against newer gtk

* Fri Dec  3 2010 Matthias Clasen <mclasen@redhat.com> 2.91.2-2
- Rebuild against new gtk

* Wed Nov 10 2010 Bastien Nocera <bnocera@redhat.com> 2.91.2-1
- Update to 2.91.2

* Mon Oct 18 2010 Bastien Nocera <bnocera@redhat.com> 2.91.0-1.
- Update to 2.91.0

* Tue Sep 28 2010 Matthias Clasen <mclasen@redhat.com> 2.31.5-6.git146c994
- git snapshot to fix the build with newer gtk

* Fri Aug 20 2010 Bastien Nocera <bnocera@redhat.com> 2.31.5-5
- Add a Requires for gnome-icon-theme-symbolic so that the
  applet icon shows up (#619376)

* Thu Jul 22 2010 Bastien Nocera <bnocera@redhat.com> 2.31.5-4
- Fix GConf handling in sound theme editor (#617025)
- Some minor bugs

* Tue Jul 13 2010 Matthias Clasen <mclasen@redhat.com>  2.31.5-1
- Update to 2.31.5

* Mon May 10 2010 Rakesh Pandit <rakesh@fedoraproject.org> 2.30.0-2
- Rebuild for new glade version

* Mon Mar 29 2010 Matthias Clasen <mclasen@redhat.com>  2.30.0-1
- Update to 2.30.0

* Fri Mar 12 2010 Bastien Nocera <bnocera@redhat.com> 2.29.91-2
- Add a speaker testing UI

* Tue Feb 23 2010 Matthias Clasen <mclasen@redhat.com>  2.19.91-1
- Update to 2.29.91

* Sun Feb 14 2010 Matthias Clasen <mclasen@redhat.com>  2.18.5-2
- Add missing libs

* Sat Jan 16 2010 Matthias Clasen <mclasen@redhat.com>  2.18.5-1
- Update to 2.18.5
- Drop an obsolete Obsoletes
- Various spec file cleanups

* Wed Oct 07 2009 Bastien Nocera <bnocera@redhat.com> 2.28.1-1
- Update to 2.28.1

* Tue Sep 22 2009 Bastien Nocera <bnocera@redhat.com> 2.28.0-2
- Fix problems with mute status handling in the applet and dialogue

* Mon Sep 21 2009 Bastien Nocera <bnocera@redhat.com> 2.28.0-1
- Update to 2.28.0

* Wed Sep 16 2009 Bastien Nocera <bnocera@redhat.com> 2.27.91-3
- Fix -libs description (#520271)

* Wed Sep 16 2009 Bastien Nocera <bnocera@redhat.com> 2.27.91-2
- Fix crashing when profile changes happen quickly (#523669)

* Mon Sep 07 2009 Bastien Nocera <bnocera@redhat.com> 2.27.91-1
- Update to 2.27.91

* Thu Aug 13 2009 Bastien Nocera <bnocera@redhat.com> 2.27.90.fix-1
- Update to 2.27.90.fix

* Fri Jul 31 2009 Matthias Clasen <mclasen@redhat.com> 2.27.5-3
- Adjust the package split to not break rhythmbox

* Fri Jul 31 2009 Matthias Clasen <mclasen@redhat.com> 2.27.5-2
- Split off an apps subpackage

* Mon Jul 27 2009 Bastien Nocera <bnocera@redhat.com> 2.27.5-1
- Update to 2.27.5

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.27.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 14 2009 Matthias Clasen <mclasen@redhat.com> 2.27.4-1
- Update to 2.27.4

* Thu Jul  2 2009 Matthias Clasen <mclasen@redhat.com> 2.27.3.1-2
- Shrink GConf schemas

* Wed Jul 01 2009 Bastien Nocera <bnocera@redhat.com> 2.27.3.1-1
- Update to 2.27.3.1

* Tue Jun 16 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.3-1
- Update to 2.27.3

* Fri May 15 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.1-1
- Update to 2.27.1

* Mon Apr 27 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.0-2
- Don't drop schemas translations from po files
- Fix alignment of sliders

* Mon Mar 16 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.0-1
- Update to 2.26.0

* Thu Mar 12 2009 - Bastien Nocera <bnocera@redhat.com> - 2.25-92-5
- Add a 100% mark for amplified sources

* Thu Mar 12 2009 - Bastien Nocera <bnocera@redhat.com> - 2.25.92-4
- Fix dB tooltip always being wrong (#489297)

* Wed Mar 11 2009 - Bastien Nocera <bnocera@redhat.com> - 2.25.92-3
- Fix unwanted random muting (#485979)

* Fri Mar  6 2009 Matthias Clasen  <mclasen@redhat.com> 2.25.92-2
- Turn off debug spew

* Tue Mar  3 2009 Matthias Clasen  <mclasen@redhat.com> 2.25.92-1
- Update to 2.25.92

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.25.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan 20 2009 - Bastien Nocera <bnocera@redhat.com> - 2.25.5-1
- Update to 2.25.5
- Add work-around for fontconfig crasher

* Tue Jan 13 2009 - Bastien Nocera <bnocera@redhat.com> - 2.25.1-6
- I get paid by the commit, more fixing the scriptlets

* Tue Jan 13 2009 - Bastien Nocera <bnocera@redhat.com> - 2.25.1-5
- Another try at fixing the scriplets

* Sun Jan 11 2009 Matthias Clasen <mclasen@redhat.com>  2.25.1-4
- Silence %%pre and %%preun

* Wed Jan 07 2009 - Rex Dieter <rdieter@fedoraproject.org> - 2.25.1-3
- gnome-media should not depend on -devel packages (#479181)

* Mon Jan 05 2009 - Bastien Nocera <bnocera@redhat.com> - 2.25.1-2
- Split applications and the media profiles library
- Remove some unneeded BuildRequires

* Wed Dec 17 2008 Matthias Clasen <mclasen@redhat.com>  2.25.1-1
- Update to 2.25.1

* Sun Nov 23 2008 Matthias Clasen <mclasen@redhat.com>  2.24.0.1-3
- Tweak description

* Fri Oct 10 2008 Matthias Clasen <mclasen@redhat.com>  2.24.0.1-2
- Save some space

* Wed Sep 24 2008 Matthias Clasen <mclasen@redhat.com>  2.24.0.1-1
- Update to 2.24.0

* Tue Sep 23 2008 Matthias Clasen <mclasen@redhat.com>  2.24.0-1
- Update to 2.24.0

* Mon Sep  8 2008 Matthias Clasen <mclasen@redhat.com>  2.23.92-1
- Update to 2.23.92

* Thu Sep  4 2008 Matthias Clasen <mclasen@redhat.com>  2.23.91-2
- Fix a non-standard icon name

* Tue Sep  2 2008 Matthias Clasen <mclasen@redhat.com>  2.23.91-1
- Update to 2.23.91

* Mon Sep 01 2008 - Bastien Nocera <bnocera@redhat.com> 2.23.3-4
- Update description (#448399)

* Sat Aug 23 2008 - Bastien Nocera <bnocera@redhat.com> - 2.23.3-3
- Rebuild to fix directory ownership (#447837)

* Wed Jul 23 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.23.3-2
- fix license tag

* Tue Jun  3 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.3-1
- Update to 2.23.3

* Fri Apr 25 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.1.1-1
- Update to 2.23.1.1

* Wed Mar 12 2008 - Bastien Nocera <bnocera@redhat.com> - 2.22.0-2
- Remove ExcludeArch for ppc/ppc64

* Mon Mar 10 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.0-1
- Update to 2.22.0

* Thu Mar  6 2008 Matthias Clasen <mclasen@redhat.com> - 2.20.1-9
- Use desktop-file-install for all desktop files

* Thu Feb 14 2008 Matthias Clasen <mclasen@redhat.com> - 2.20.1-8
- Rebuild

* Mon Oct 22 2007 - Bastien Nocera <bnocera@redhat.com> - 2.20.1-7
- Fix spurious '%' in the scriplets, spotted by Yanko Kaneti
  <yaneti@declera.com>

* Wed Oct 17 2007 - Bastien Nocera <bnocera@redhat.com> - 2.20.1-6
- Show the "Front" track by default (#335121)

* Wed Oct 10 2007 - Bastien Nocera <bnocera@redhat.com> - 2.20.1-5
- Install the mixer's schema file (#186791)

* Wed Oct 10 2007 - Bastien Nocera <bnocera@redhat.com> - 2.20.1-4
- Sanitise the default width/height values from GConf before we
  use them (#186791)

* Fri Oct 05 2007 - Bastien Nocera <bnocera@redhat.com> - 2.20.1-3
- Add gnome-sound-recorder (#161112)
- Fix CDDBSlave schemas handling

* Fri Oct 05 2007 - Bastien Nocera <bnocera@redhat.com> - 2.20.1-2
- Remove gnome-cd (#278321)

* Wed Sep 19 2007 - Bastien Nocera <bnocera@redhat.com> - 2.20.1-1
- Update to 2.20.1
- Remove obsolete icons patch

* Wed Sep 19 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.0-2
- Don't add extra categories to volume control, since
  upstream has moved it to Hardware  (#295251)
- Make icons show up again  (#295171)

* Mon Sep 17 2007 - Bastien Nocera <bnocera@redhat.com> - 2.20.0-1
- Update to 2.20.0

* Fri Sep 07 2007 - Bastien Nocera <bnocera@redhat.com> - 2.19.92-1
- Update to 2.19.92
- Remove upstreamed/obsolete patches

* Sat Aug 25 2007 - Bastien Nocera <bnocera@redhat.com> - 2.18.0-6
- Run intltoolize before autoreconf, to avoid intltool version
  mismatches

* Fri Aug 24 2007 Adam Jackson <ajax@redhat.com> - 2.18.0-5
- Rebuild for build ID

* Tue Aug  7 2007 Matthias Clasen <mclasen@redhat.com> - 2.18.0-4
- Update license field
- Use %%find_lang for help files

* Thu Apr 19 2007 - Bastien Nocera <bnocera@redhat.com> - 2.18.0-3
- Fix playback of last track in track mode (#142722)

* Thu Apr 19 2007 - Bastien Nocera <bnocera@redhat.com> - 2.18.0-2
- Fix modality so that you can actually edit profiles in sound-juicer
  and Rhythmbox (#230872)

* Tue Mar 13 2007 Matthias Clasen <mclasen@redhat.com> - 2.18.0-1
- Update to 2.18.0
- Drop obsolete patch

* Mon Feb 12 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.91-1
- Update to 2.17.91

* Thu Feb 08 2007 - Bastien Nocera <bnocera@redhat.com> - 2.17.90-6
- Fix rpath issue by using a newer libtool, disable scrollkeeper-update
  during package installation by patching omf.make

* Thu Feb 08 2007 - Bastien Nocera <bnocera@redhat.com> - 2.17.90-5
- Really fix rpath issue

* Thu Feb 08 2007 - Bastien Nocera <bnocera@redhat.com> - 2.17.90-4
- Fix rpath being defined in binaries and libraries

* Thu Feb 08 2007 - Bastien Nocera <bnocera@redhat.com> - 2.17.90-3
- Fix a few specfile issues, as per Deji Akingunola
  <dakingun@gmail.com>'s review

* Wed Feb  7 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.90-2
- Add X-GNOME-PersonalSettings to gnome-volume-control.desktop

* Mon Jan 22 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.90-1
- Update to 2.17.90

* Wed Jan 10 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.2-1
- Update to 2.17.2

* Wed Dec 20 2006 Matthias Clasen <mclasen@redhat.com> - 2.17.1-1
- Update to 2.17.1

* Wed Oct 18 2006 Matthias Clasen <mclasen@redhat.com> - 2.16.1-3
- Fix scripts according to packaging guidelines

* Fri Sep  8 2006 Matthias Clasen <mclasen@redhat.com> - 2.16.1-2
- Fix directory ownership issues
- Don't ship grecord help

* Mon Sep  4 2006 Matthias Clasen <mclasen@redhat.com> - 2.16.1-1
- Update to 2.16.1

* Mon Sep  4 2006 Matthias Clasen <mclasen@redhat.com> - 2.16.0-1
- Update to 2.16.0
- Require pkgconfig in the -devel package
- Update the settings patch

* Wed Jul 19 2006 Matthias Clasen <mclasen@redhat.com> - 2.14.2-6
- Rebuild against dbus

* Wed Jul 12 2006 Matthias Clasen <mclasen@redhat.com> - 2.14.2-5
- Rebuild

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.14.2-4.1
- rebuild

* Tue Jun 13 2006 Matthias Clasen <mclasen@redhat.com> - 2.14.2-4
- Rebuild against new nautilus-cd-burner
- Work around a gstreamer problem

* Fri Jun  9 2006 Matthias Clasen <mclasen@redhat.com> - 2.14.2-3
- Fix missing BuildRequires

* Mon May 29 2006 Matthias Clasen <mclasen@redhat.com> - 2.14.2-2
- Update to 2.14.2

* Mon May 22 2006 Matthias Clasen <mclasen@redhat.com> - 2.14.0-3
- disable scrollkeeper

* Tue Mar 14 2006 Ray Strode <rstrode@redhat.com> - 2.14.0-2
- rebuild

* Sun Mar 12 2006 Matthias Clasen <mclasen@redhat.com> - 2.14.0-1
- Update to 2.14.0 

* Mon Feb 27 2006 Matthias Clasen <mclasen@redhat.com> - 2.13.93-1
- Update to 2.13.93

* Wed Feb 15 2006 Matthias Clasen <mclasen@redhat.com> - 2.13.92-1
- Update to 2.13.92

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.13.91-2.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.13.91-2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Sat Feb  4 2006 Christopher Aillon <caillon@redhat.com> - 2.13.91-2
- Use gstreamer (0.10)

* Mon Jan 30 2006 Matthias Clasen <mclasen@redhat.com> - 2.13.91-1
- Update to 2.13.91

* Sat Jan 28 2006 Matthias Clasen <mclasen@redhat.com> - 2.13.7-1
-Update to 2.13.7

* Sun Jan 22 2006 Christopher Aillon <caillon@redhat.com> - 2.13.5-2
- Disable the help button in gnome-audio-profiles-properties since
  it isn't yet hooked up to anything.

* Wed Jan 18 2006 John (J5) Palmieri <johnp@redhat.com> - 2.13.5-1
- Upgrade to 2.13.5
- Pull in gstreamer08 not gstreamer

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Dec  2 2005 John (J5) Palmieri <johnp@redhat.com> - 2.12.0-3
- Rebuild with new nautilus-cd-burner

* Tue Nov 22 2005 Matthias Clasen <mclasen@redhat.com> - 2.12.0-2
- Classify volume control as setting, for better menus

* Thu Sep  8 2005 Matthias Clasen <mclasen@redhat.com> - 2.12.0-1
- Update to 2.12.0

* Tue Aug 16 2005 Warren Togami <wtogami@redhat.com> - 2.11.91-1
- rebuild for new cairo and 2.11.91

* Mon Jul 18 2005 John (J5) Palmieri <johnp@redhat.com> 2.11.5-1
- Update to 2.11.5

* Tue Jul 12 2005 Matthias Clasen <mclasen@redhat.com> 2.11.4-1
- Newer upstream version

* Fri May 20 2005 John (J5) Palmieri <johnp@redhat.com> 2.10.2-4
- patch that avoids a deadlock when the last track on the cd is done
  (bug #151093)

* Tue May 17 2005 John (J5) Palmieri <johnp@redhat.com> 2.10.2-2
- remove gnome-sound-recorder because it hasn't worked for some time

* Mon May 02 2005 John (J5) Palmieri <johnp@redhat.com> 2.10.2-1
- Update to 2.10.2

* Tue Mar 29 2005 John (J5) Palmieri <johnp@redhat.com> 2.10.0-2
- Added a devel package

* Wed Mar 16 2005 Colin Walters <walters@redhat.com> 2.10.0-1
- Update to 2.10.0

* Sat Jan 01 2005 Matthias Clasen <mclasen@redhat.com> 2.9.90-1
- Update to 2.9.90

* Mon Oct 25 2004 Colin Walters <walters@redhat.com> 2.8.0-4
- Add fix from Ronald to gnome-media-2.8.0-gst-mixer-nomodem.patch
  to make two-soundcard case work again (136930)

* Tue Oct 19 2004 Colin Walters <walters@redhat.com> 2.8.0-3
- Add patch to not show empty mixers for modems,
  etc.  Tested and confirmed to work on two machines.

* Mon Oct 18 2004 Colin Walters <walters@redhat.com> 2.8.0-2
- Add patch to not show oss mixers

* Mon Sep 13 2004 Colin Walters <walters@redhat.com> 2.8.0-1
- Remove upstreamed cd-sink-fix.patch

* Fri Sep 03 2004 Matthias Clasen <mclasen@redhat.com> 2.7.92-7
- Make help button of gstreamer-properties work

* Tue Aug 31 2004 Colin Walters <walters@redhat.com> 2.7.92-2
- Add patch to use correct sink for gnome-cd

* Tue Aug 31 2004 Colin Walters <walters@redhat.com> 2.7.92-1
- Update to 2.7.92

* Wed Aug 04 2004 Colin Walters <walters@redhat.com> 2.7.1-1
- Update to 2.7.1
- Delete tons of cruft from makeinstall code

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue May 18 2004 Colin Walters <walters@redhat.com> 2.6.2-1
- New upstream version
- Bump required versions of various build dependencies
- Update Source URL
- Remove BuildRequires and calls to autofoo, since we don't
  patch any autofoo files anymore.

* Thu Apr 15 2004 Warren Togami <wtogami@redhat.com> 2.6.0-2
- #111141 BR automake libtool gstreamer-plugins-devel gettext
  still something missing...

* Fri Apr  2 2004 Alex Larsson <alexl@redhat.com> 2.6.0-1
- update to 2.6.0

* Tue Mar 16 2004 Jeremy Katz <katzj@redhat.com> 2.5.5-2
- rebuild for new gstreamer

* Thu Mar 11 2004 Alex Larsson <alexl@redhat.com> 2.5.5-1
- update to 2.5.5

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar  2 2004 Alexander Larsson <alexl@redhat.com> 2.5.4-2
- fixed schemas list

* Thu Feb 26 2004 Alexander Larsson <alexl@redhat.com> 2.5.4-1
- update to 2.5.4

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Jan 29 2004 Bill Nottingham <notting@redhat.com> 2.5.2-1
- update to 2.5.2

* Mon Oct 27 2003 Than Ngo <than@redhat.com> 2.4.0-2
- don't show Volume Control in KDE

* Tue Oct  7 2003 Havoc Pennington <hp@redhat.com> 2.4.0-1
- 2.4.0

* Thu Aug 21 2003 Alexander Larsson <alexl@redhat.com> 2.3.7-1
- update for gnome 2.3

* Wed Jul 30 2003 Havoc Pennington <hp@redhat.com> 2.2.1.1-6
- rebuild

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 14 2003 Havoc Pennington <hp@redhat.com> 2.2.1.1-4
- don't buildreq Xft

* Wed Feb  5 2003 Jonathan Blandford <jrb@redhat.com> 2.2.1.1-1
- new version
- add back $(_datadir)/gnome-media-2.0 as it turned out the files missing last release were just temporarily gone

* Tue Feb  4 2003 Jonathan Blandford <jrb@redhat.com>
- bump version

* Tue Feb  4 2003 Tim Powers <timp@redhat.com> 2.1.3-6
- rebuild against new gstreamer

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Dec 18 2002 Elliot Lee <sopwith@redhat.com>
- Include ia64
- _smp_mflags

* Thu Dec 12 2002 Jonathan Blandford <jrb@redhat.com>
- 2.1.3
- update requirements
- Try and build all but ia64 until we get gstreamer working.

* Tue Dec  3 2002 Havoc Pennington <hp@redhat.com>
- excludearch the no-gstreamer arches, and require gstreamer
- fixups to file list

* Mon Dec  2 2002 Tim Powers <timp@redhat.com> 2.1.1-1
- update to 2.1.1
- don't apply the patches, they should be upstream now

* Tue Aug 27 2002 Owen Taylor <otaylor@redhat.com>
- Fix bug with changing device in preferences (#72465)
- Make the operation of --unique per-device

* Fri Aug 23 2002 Owen Taylor <otaylor@redhat.com>
- Add --unique option to allow starting only one CD player
  per display. (#39208)

* Wed Aug 21 2002 Havoc Pennington <hp@redhat.com>
- remove gnome-reclevel.desktop that was another alias for vumeter #71916

* Wed Aug 14 2002 Havoc Pennington <hp@redhat.com>
- remove vumeter, #67140

* Mon Jul 29 2002 Havoc Pennington <hp@redhat.com>
- rebuild with new gail

* Thu Jul 25 2002 Havoc Pennington <hp@redhat.com>
- put translations in, makes it rebuild #69404

* Sun Jun 16 2002 Havoc Pennington <hp@redhat.com>
- 2.0.0
- install capplet control center file, though I may 
  take it out again since it sucks
- use desktop-file-install
- add omf to file list

* Fri Jun 07 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment

* Wed Jun  5 2002 Havoc Pennington <hp@redhat.com>
- add post/postun ldconfig
- rebuild with latest libs

* Tue May 21 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment

* Tue May 21 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment
- buildrequire gail

* Tue May 21 2002 Havoc Pennington <hp@redhat.com>
- 1.547.0

* Fri May 03 2002 Havoc Pennington <hp@redhat.com>
- rebuild with new libs

* Thu Apr 25 2002 Havoc Pennington <hp@redhat.com>
- GNOME 2 version 1.520.2

* Wed Aug 22 2001 Owen Taylor <otaylor@redhat.com>
- Force regeneration of .po files (#52326)

* Thu Jul 19 2001 Havoc Pennington <hp@redhat.com>
- build requires gnome-libs-devel
- fix rpmlint's utterly crack-smoking request that we not 
  run /bin/sh in post/postun

* Tue Jul 03 2001 Owen Taylor <otaylor@redhat.com>
- Update to 1.2.3

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Wed May  9 2001 Owen Taylor <otaylor@redhat.com>
- Version 1.2.2
- Fix bogus scrollkeeper version in dependency

* Fri Feb 23 2001 Trond Eivind Glomsrød <teg@redhat.com>
- langify
- move changelog to end of file
- don't use and define "ver" at the top of the spec file

* Wed Feb 07 2001 Than Ngo <than@redhat.com>
- fixed non-standard dir perm (Bug #26264)

* Wed Jan 31 2001 Elliot Lee <sopwith@redhat.com> 1.2.0-10
- Fix bug #17713, grecord internals (Patch10)

* Tue Jan 30 2001 Elliot Lee <sopwith@redhat.com> 1.2.0-9
- Fix bug #21488, include cddb-submit-methods in file list

* Thu Jan 18 2001 Akira TAGOH <tagoh@redhat.com>
- Added Japanese patch.

* Fri Aug 11 2000 Jonathan Blandford <jrb@redhat.com>
- Update Epoch

* Sat Aug 05 2000 Havoc Pennington <hp@redhat.com>
- Find "sox", bug 15472, patch from Alan

* Fri Aug 04 2000 Havoc Pennington <hp@redhat.com>
- Add docs for gtcd, bug 14558

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sat Jul 8 2000 Havoc Pennington <hp@redhat.com>
- Remove docdir

* Thu Jun 15 2000 Havoc Pennington <hp@redhat.com>
- 1.2.0
- use %%makeinstall

* Tue Sep 21 1999 Havoc Pennington <hp@redhat.com>
- Fixed gtcd so it works without corba-gtcd
- add DrMike's no-g_error() patch 

* Mon Sep 20 1999 Elliot Lee <sopwith@redhat.com>
- Update to 1.0.40

* Fri Sep 17 1999 Owen Taylor <otaylor@redhat.com>
- Don't keep device open in gtcd

* Thu Sep 9 1999 Owen Taylor <otaylor@redhat.com>
- Fixed warnings with previous

* Wed Sep 8 1999 Owen Taylor <otaylor@redhat.com>
- added --play option to gtcd

* Mon Aug 16 1999 Michael Fulbright <drmike@redhat.com>
- version 1.0.9.1

* Fri Mar 19 1999 Michael Fulbright <drmike@redhat.com>
- strip binaries

* Mon Feb 15 1999 Michael Fulbright <drmike@redhat.com>
- version 0.99.8

* Tue Jan 19 1999 Michael Fulbright <drmike@redhat.com>
- fixed building on sparc and RH 5.2 - seems to get confused into thinking
  we have cd changer support when we don't

* Wed Jan 06 1999 Michael Fulbright <drmike@redhat.com>
- updated to 0.99.1

* Wed Dec 16 1998 Michael Fulbright <drmike@redhat.com>
- updated for GNOME freeze

* Sat Nov 21 1998 Pablo Saratxaga <srtxg@chanae.alphanet.ch>
- added spanish and french translations for rpm

* Wed Sep 23 1998 Michael Fulbright <msf@redhat.com>
- Updated to 0.30 release

* Mon Mar 16 1998 Marc Ewing <marc@redhat.com>
- Integrate into gnome-media CVS source tree
