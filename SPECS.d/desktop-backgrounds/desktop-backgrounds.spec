%global rh_backgrounds_version 15
%global waves_version 0.1.2
%global fedora_release_name beefy-miracle
%global Fedora_Release_Name Beefy_Miracle
#此包是fedora特有包，需要改成Magic的。
Name:           desktop-backgrounds
Version:        17.0.0
Release:        2%{?dist}
Summary:        Desktop backgrounds

Group:          User Interface/Desktops
License:        LGPLv2
Source0:        redhat-backgrounds-%{rh_backgrounds_version}.tar.bz2
Source2:        Propaganda-1.0.0.tar.gz
Source3:        README.Propaganda
Source5:        waves-%{waves_version}.tar.bz2
Source6:        FedoraWaves-metadata.desktop
Source7:        desktop-backgrounds-fedora.xml
Source8:        fedora-metadata.desktop
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

%description
The desktop-backgrounds package contains artwork intended to be used as
desktop background image.


%package        basic
Summary:        Desktop backgrounds
Group:          User Interface/Desktops
Provides:       desktop-backgrounds = %{version}-%{release}
Obsoletes:      desktop-backgrounds < %{version}-%{release}

%description    basic
The desktop-backgrounds-basic package contains artwork intended to be used as
desktop background image.

%package        gnome
Summary:        The default Fedora wallpaper from GNOME desktop
Group:          User Interface/Desktops
%if 0%{?fedora} == 15
Requires:       lovelock-backgrounds-stripes-gnome
%else
#Requires:       %{fedora_release_name}-backgrounds-gnome
%endif
# starting with this release, gnome uses picture-uri instead of picture-filename
# see gnome bz #633983
Requires:       gsettings-desktop-schemas >= 2.91.92
Provides:       system-backgrounds-gnome = %{version}-%{release}
License:        CC-BY-SA

%description    gnome
The desktop-backgrounds-gnome package sets default background in gnome.

%package        xfce
Summary:        The default Fedora wallpaper from XFCE desktop
Group:          User Interface/Desktops
#Requires:       %{fedora_release_name}-backgrounds-xfce
Provides:       system-backgrounds-xfce = %{version}-%{release}
License:        CC-BY-SA

%description    xfce
The desktop-backgrounds-xfce package contains file-names used by XFCE desktop
environment to set up the default backdrop.

%package        compat
Summary:        The default Fedora wallpaper for less common DEs
Group:          User Interface/Desktops
#Requires:       %{fedora_release_name}-backgrounds-single
Provides:       system-backgrounds-compat = %{version}-%{release}
License:        CC-BY-SA

%description    compat
The desktop-backgrounds-compat package contains file-names used
by less common Desktop Environments such as LXDE to set up the
default wallpaper.

%package        waves
Summary:        Desktop backgrounds for the Waves theme
Group:          User Interface/Desktops

%description    waves
The desktop-backgrounds-waves package contains the "Waves" desktop backgrounds
which were used in Fedora 9.

%prep
%setup -qn redhat-backgrounds-%{rh_backgrounds_version}

# move things where %%doc can find them
cp %{SOURCE3} .
mv images/space/*.ps .
mv images/space/README* .

# add propaganda
(cd tiles && tar zxf %{SOURCE2})

# add waves
tar xjf %{SOURCE5}

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_prefix}/share/backgrounds
cd $RPM_BUILD_ROOT%{_prefix}/share/backgrounds

cp -a $RPM_BUILD_DIR/redhat-backgrounds-%{rh_backgrounds_version}/images .
cp -a $RPM_BUILD_DIR/redhat-backgrounds-%{rh_backgrounds_version}/tiles .

mkdir waves
# copy actual image files
cp -a $RPM_BUILD_DIR/redhat-backgrounds-%{rh_backgrounds_version}/waves-%{waves_version}/*.png waves
# copy animation xml file
cp -a $RPM_BUILD_DIR/redhat-backgrounds-%{rh_backgrounds_version}/waves-%{waves_version}/waves.xml waves

mkdir -p $RPM_BUILD_ROOT%{_datadir}/gnome-background-properties
cp -a $RPM_BUILD_DIR/redhat-backgrounds-%{rh_backgrounds_version}/desktop-backgrounds-basic.xml $RPM_BUILD_ROOT%{_prefix}/share/gnome-background-properties
cp -a $RPM_BUILD_DIR/redhat-backgrounds-%{rh_backgrounds_version}/waves-%{waves_version}/desktop-backgrounds-waves.xml $RPM_BUILD_ROOT%{_prefix}/share/gnome-background-properties

bgdir=$RPM_BUILD_ROOT%{_datadir}/backgrounds
for I in tiles/Propaganda images/dewdop_leaf.jpg images/dragonfly.jpg images/frosty_pipes.jpg images/in_flight.jpg images/leaf_veins.jpg \
        images/leafdrops.jpg images/lightrays-transparent.png images/lightrays.png images/lightrays2.png images/raingutter.jpg images/riverstreet_rail.jpg \
        images/sneaking_branch.jpg images/space images/yellow_flower.jpg; do
        rm -rf ${bgdir}/${I}
done

# FedoraWaves theme for KDE4
mkdir -p $RPM_BUILD_ROOT%{_datadir}/wallpapers/Fedora_Waves/contents/images
install -m 644 -p %{SOURCE6} $RPM_BUILD_ROOT%{_datadir}/wallpapers/Fedora_Waves/metadata.desktop
(cd $RPM_BUILD_ROOT%{_datadir}/wallpapers/Fedora_Waves/contents/;
ln -s ../../../backgrounds/waves/waves-eeepc-3-night.png screenshot.png
cd $RPM_BUILD_ROOT%{_datadir}/wallpapers/Fedora_Waves/contents/images
ln -s ../../../../backgrounds/waves/waves-normal-3-night.png 1024x768.png
ln -s ../../../../backgrounds/waves/waves-wide-3-night.png 1280x800.png
# FIXME: there doesn't seem to be a 5:4 image in the latest iteration
ln -s ../../../../backgrounds/waves/waves-wide-3-night.png 1280x1024.png
ln -s ../../../../backgrounds/waves/waves-wide-3-night.png 1440x900.png
ln -s ../../../../backgrounds/waves/waves-normal-3-night.png 1600x1200.png
ln -s ../../../../backgrounds/waves/waves-wide-3-night.png 1920x1200.png
)

# Defalts for various desktops:
#   for GNOME
mkdir -p $RPM_BUILD_ROOT%{_datadir}/glib-2.0/schemas
/usr/bin/echo '[org.gnome.desktop.background]' > \
    $RPM_BUILD_ROOT%{_datadir}/glib-2.0/schemas/org.gnome.desktop.background.fedora.gschema.override
%if 0%{?fedora} == 15
/usr/bin/echo "picture-uri='file://%{_datadir}/backgrounds/lovelock/default-stripes/lovelock.xml'" >> \
    $RPM_BUILD_ROOT%{_datadir}/glib-2.0/schemas/org.gnome.desktop.background.fedora.gschema.override
%else
/usr/bin/echo "picture-uri='file://%{_datadir}/backgrounds/%{fedora_release_name}/default/%{fedora_release_name}.xml'" >> \
    $RPM_BUILD_ROOT%{_datadir}/glib-2.0/schemas/org.gnome.desktop.background.fedora.gschema.override
%endif
#   for KDE, this is handled in kde-settings
#   for XFCE
mkdir -p $RPM_BUILD_ROOT%{_datadir}/xfce4/backdrops
/usr/bin/ln -s %{fedora_release_name}.png \
           $RPM_BUILD_ROOT%{_datadir}/xfce4/backdrops/default.png
#   and for the rest (e.g. LXDE)
(cd $RPM_BUILD_ROOT%{_datadir}/backgrounds/images;
ln -s ../%{fedora_release_name}/default/standard/%{fedora_release_name}.png \
      default.png
ln -s ../%{fedora_release_name}/default/normalish/%{fedora_release_name}.png \
      default-5_4.png
ln -s ../%{fedora_release_name}/default/wide/%{fedora_release_name}.png \
      default-16_10.png
cd ..
ln -s ./%{fedora_release_name}/default/standard/%{fedora_release_name}.png \
      default.png
)
magic_rpm_clean.sh
%clean
rm -rf $RPM_BUILD_ROOT

%posttrans gnome
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :

%postun gnome
if [ $1 -eq 0 ]; then
  glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%files basic
%defattr(-, root, root)
%dir %{_datadir}/backgrounds
%dir %{_datadir}/backgrounds/tiles
%dir %{_datadir}/backgrounds/images
%{_datadir}/backgrounds/tiles/*.png
%{_datadir}/backgrounds/tiles/*jpg
%{_datadir}/backgrounds/images/earth_from_space.jpg
%{_datadir}/backgrounds/images/flowers_and_leaves.jpg
%{_datadir}/backgrounds/images/ladybugs.jpg
%{_datadir}/backgrounds/images/stone_bird.jpg
%{_datadir}/backgrounds/images/tiny_blast_of_red.jpg
%dir %{_datadir}/gnome-background-properties
%{_datadir}/gnome-background-properties/desktop-backgrounds-basic.xml
%dir %{_datadir}/wallpapers

%files waves
%defattr(-, root, root)
%dir %{_datadir}/backgrounds/waves
%{_datadir}/backgrounds/waves/*.png
%{_datadir}/backgrounds/waves/waves.xml
%{_datadir}/gnome-background-properties/desktop-backgrounds-waves.xml
%{_datadir}/wallpapers/Fedora_Waves

%files gnome
%defattr(-, root, root)
%{_datadir}/glib-2.0/schemas/org.gnome.desktop.background.fedora.gschema.override

%files xfce
%defattr(-, root, root)
%{_datadir}/xfce4/backdrops/default.png

%files compat
%defattr(-, root, root)
%{_datadir}/backgrounds/images/default*
%{_datadir}/backgrounds/default.png

%changelog
* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 17.0.0-2
- 为 Magic 3.0 重建

* Tue Feb 07 2012 Martin Sourada <mso@fedoraproject.org> - 17.0.0-1
- Switch to Beefy Miracle

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 16.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jul 29 2011 Martin Sourada <mso@fedoraproject.org> - 16.0.0-1
- Switch to Verne

* Sat Apr 02 2011 Martin Sourada <mso@fedoraproject.org> - 15.0.0-8
- Use stripes version of the wallpaper on F15 in Gnome
- We should require the schema we override, not the component that uses
  it
- Fix the scriplets
- Minor spec clean-up

* Tue Mar 22 2011 Tom Callaway <spot@fedoraproject.org> - 15.0.0-7
- picture-uri needs to be an actual uri

* Tue Mar 22 2011 Martin Sourada <mso@fedoraproject.org> - 15.0.0-6
- Update for upcoming changes in gnome-desktop-2.91.92
  * picture-uri is used instead of picture-filename to select background
    gnome bz #633983

* Tue Mar 22 2011 Martin Sourada <mso@fedoraproject.org> - 15.0.0-5
- Set default wallpaper for gnome

* Mon Mar 07 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> - 15.0.0-4
- Drop unused -kde subpackage, we set the default through kde-settings & pull it
  in through system-plasma-desktoptheme, which is Provided by lovelock-kde-theme

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 15.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Feb 07 2011 Martin Sourada <mso@fedoraproject.org> - 15.0.0-2
- The file-names should not contain the word fedora for the system-backgrounds*
  virtual provides to be more effective

* Mon Feb 07 2011 Martin Sourada <mso@fedoraproject.org> - 15.0.0-1
- Provide file-names for default wallpapers
  * new subpackages -gnome, -kde, xfce for the various DEs
  * -compat subpackage is really for setting the default wallpaper for the
    other desktops like LXDE, adjust the description and summary
  * use correct suffix in file-names in -compat subpackage
- Sync version with Fedora release

* Thu Aug 12 2010 Martin Sourada <mso@fedoraproject.org> - 9.0.0-15
- Rebuild, add dist tag.
- Properly versioned provides/obsoletes for the -basic subpackage

* Thu Aug 05 2010 Christoph Wickert <cwickert@fedoraproject.org> - 9.0.0-14
- Update for F14 Laughlin artwork

* Fri Apr 16 2010 Christoph Wickert <cwickert@fedoraproject.org> - 9.0.0-14
- Adjustments for recent Goddard artwork changes

* Thu Mar 18 2010 Christoph Wickert <cwickert@fedoraproject.org> - 9.0.0-13
- Update for F13 Goddard artwork

* Mon Mar  1 2010 Matthias Clasen <mclasen@redhat.com> - 9.0.0-12
- Fix a directory ownership issue

* Tue Nov 03 2009 Christoph Wickert <cwickert@fedoraproject.org> - 9.0.0-11
- Bump release for RC

* Sun Nov 01 2009 Christoph Wickert <cwickert@fedoraproject.org> - 9.0.0-10
- Update for F12 constantine artwork

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.0.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Apr 22 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 9.0.0-8
- fix compat subpackage

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Nov 21 2008 Matthias Clasen <mclasen@redhat.com> - 9.0.0-6
- Tweak descriptions

* Tue Nov  4 2008 Ray Strode <rstrode@redhat.com> 9.0.0-5
- Fix compat links after solar-backgrounds restructuring
  (bug 469789)

* Mon Oct 27 2008 Ray Strode <rstrode@redhat.com> 9.0.0-4
- Make compat subpackage depend on solar backgrounds
  (bug 468749)

* Tue Oct 21 2008 Ray Strode <rstrode@redhat.com> 9.0.0-3
- Move waves wallpapers to a subpackage

* Wed Oct 08 2008 Than Ngo <than@redhat.com> 9.0.0-2
- own /usr/share/wallpapers

* Fri Apr 11 2008 Ray Strode <rstrode@redhat.com> 9.0.0-1
- Update wallpapers to latest iteration from art team
- Add compat subpackage to provide compat-links for all the cruft
  that's accumulated over the years

* Fri Apr 11 2008 Than Ngo <than@redhat.com> 8.92-5
- Add FedoraWaves theme for KDE4

* Mon Apr  7 2008 Matthias Clasen <mclasen@redhat.com> - 8.92-4
- Rename FC5-era backgrounds

* Sun Apr  6 2008 Matthias Clasen <mclasen@redhat.com> - 8.92-3
- Drop infinity backgrounds, they will be moved to a separate package

* Sat Mar 29 2008 Matthias Clasen <mclasen@redhat.com> - 8.92-2
- Move the "waves" animation start time back to the past

* Sat Mar 29 2008 Matthias Clasen <mclasen@redhat.com> - 8.92-1
- Add "Waves" backgrounds. Leave infinity for now

* Thu Oct 11 2007 Ray Strode <rstrode@redhat.com> - 7.92-8
- Scale images

* Tue Oct 9 2007 Ray Strode <rstrode@redhat.com> - 7.92-7
- Upgrade desktop backgrounds to higher fidelity versions,
  given by Máirín Duffy

* Wed Sep 26 2007 Máirín Duffy <duffy@redhat.com> - 7.92-6
- wallpapers redone so there is no more banding
- wallpapers renamed
- infinity animated file bugs fixed (hopefully)

* Thu Sep 20 2007 Ray Strode <rstrode@redhat.com> - 7.92-5
- fix symlinks again

* Thu Sep  6 2007 Bill Nottingham <notting@redhat.com> - 7.92-4
- fix symlinks

* Wed Sep  5 2007 Ray Strode <rstrode@redhat.com> - 7.92-3
- create links for default.png etc until more artwork shows up
- start animated backgrounds at midnight

* Thu Aug 30 2007 Jeremy Katz <katzj@redhat.com> - 7.92-2
- need to include less infinity backgrounds for now; the space usage
  kill livecds

* Wed Aug 28 2007 Máirín Duffy <duffy@redhat.com> - 7.92-1
- Add Infinity background

* Wed Aug  8 2007 Matthias Clasen <mclasen@redhat.com> - 2.0-38
- Update the licence field

* Wed Sep 06 2006 John (J5) Palmieri <johnp@redhat.com> - 2.0-37
- Backgrounds are now changed to jpgs and 4:3 has been replaced
  by a 5:4 aspect image

* Fri Jul 28 2006 John (J5) Palmieri <johnp@redhat.com> - 2.0-35
- Add 4:3 aspect ration version of background

* Thu Jul 27 2006 John (J5) Palmieri <johnp@redhat.com> - 2.0-35
- Add dual screen background

* Wed Jul 26 2006 Alexander Larsson <alexl@redhat.com> - 2.0-34
- Add wide desktop background

* Mon Jun  5 2006 Matthias Clasen <mclasen@redaht.com> 2.0-33
- Really remove the default background

* Mon Jun  5 2006 Matthias Clasen <mclasen@redaht.com> 2.0-32
- Move the default background to fedora-logos

* Mon Dec 19 2005 Ray Strode <rstrode@redhat.com> 2.0-31
- replace default fedora background with new one
  from Diana Fong

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com> 2.0-30.1
- rebuilt

* Thu Oct  6 2005 Matthias Clasen <mclasen@redhat.com> 2.0-30
- Replace earth_from_space.jpg with a non-mirrored version (#163345)

* Wed Apr 27 2005 John (J5) Palmieri <johnp@redhat.com> 2.0-29
- Add translations
- redhat-backgrounds-9

* Tue Feb 22 2005 Elliot Lee <sopwith@redhat.com> 2.0-28
- Remove extra backgrounds for now to save space.

* Wed Feb  2 2005 Matthias Clasen <mclasen@redhat.com> - 2.0-27
- Move .xml files to where the background capplet in
  Gnome 2.10 will find them

* Mon Oct 18 2004 Alexander Larsson <alexl@redhat.com> - 2.0-26.2.1E
- RHEL build

* Mon Oct 18 2004 Alexander Larsson <alexl@redhat.com> - 2.0-26.2
- New background

* Thu Sep 30 2004 Alexander Larsson <alexl@redhat.com> - 2.0-26.1E
- RHEL build

* Thu Sep 30 2004 Alexander Larsson <alexl@redhat.com> - 2.0-26
- New default background infrastructure.

* Mon Sep 27 2004 Matthias Clasen <mclasen@@redhat.com> 2.0.25
- avoid duplicate images

* Mon Sep 27 2004 Matthias Clasen <mclasen@@redhat.com> 2.0.24
- Prepopulate the list of backgrounds in the background
  changes with a small set of good backgrounds (#133382)
- redhat-backgrounds-7

* Thu Sep 09 2004 Elliot Lee <sopwith@redhat.com> 2.0-23
- Really update the default background.

* Wed Jul 07 2004 Elliot Lee <sopwith@redhat.com> 2.0-21
- Change background for FC3test1

* Thu May  6 2004 Jeremy Katz <katzj@redhat.com> - 2.0-20
- background from Garrett for FC2

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sun Nov  2 2003 Elliot Lee <sopwith@redhat.com> 2.0-18
- redhat-backgrounds-6

* Wed Oct 29 2003 Havoc Pennington <hp@redhat.com> 2.0-17
- redhat-backgrounds-5

* Tue Sep 23 2003 Michael Fulbright <msf@redhat.com> 2.0-16
- new fedora background
- (this change was never committed to cvs -hp)

* Thu Jul 17 2003 Havoc Pennington <hp@redhat.com> 2.0-15
- background for the beta

* Fri Feb 21 2003 Havoc Pennington <hp@redhat.com> 2.0-14
- some background tweaks from Garrett

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Fri Dec  6 2002 Havoc Pennington <hp@redhat.com>
- rebuild
- update redhat-backgrounds version

* Tue Sep  3 2002 Havoc Pennington <hp@redhat.com>
- new redhat-backgrounds from CVS with new default

* Tue Aug 27 2002 Than Ngo <than@redhat.com> 2.0-9
- add missing kdebase desktop backgrounds (bug #72508)

* Wed Aug 21 2002 Havoc Pennington <hp@redhat.com>
- drop the beta placeholder in favor of final background

* Tue Aug 13 2002 Havoc Pennington <hp@redhat.com>
- new redhat-backgrounds with wallpapers moved to tiles
- overwrite default.png with a placeholder

* Fri Aug  9 2002 Havoc Pennington <hp@redhat.com>
- new redhat-backgrounds with default.png

* Mon Jul 22 2002 Havoc Pennington <hp@redhat.com>
- new redhat-backgrounds from CVS with default.jpg

* Tue Jul 16 2002 Havoc Pennington <hp@redhat.com>
- new images from Garrett added to -extra

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun Jun 16 2002 Havoc Pennington <hp@redhat.com>
- redo it, now it includes the tile/image collection
  redhat-backgrounds from CVS, plus propaganda
- move things to datadir/share/backgrounds/images
  and datadir/share/backgrounds/wallpapers
- split into a small basic package and an extra package,
  so we can have packages require the basic package
  without sucking in huge images
- move space images into devserv CVS
- move nautilus and kdebase tiles into devserv CVS

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Thu Jun 29 2000 Dave Mason <dcm@redhat.com>
- updated spec file to RPM guidelines

* Thu Jun 29 2000 Than Ngo <than@redhat.de>
- FHS fixes

* Tue Feb 01 2000 Preston Brown <pbrown@redhat.com>
- new space backgrounds

* Fri Apr  2 1999 Jonathan Blandford <jrb@redhat.com>
- added propaganda tiles.  Spruced it up a bit
- moved README files out of tarball, and into docs dir.

* Fri Mar 19 1999 Michael Fulbright <drmike@redhat.com>
- First attempt
