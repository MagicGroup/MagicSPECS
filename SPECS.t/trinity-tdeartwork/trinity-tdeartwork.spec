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


Name:		trinity-tdeartwork
Summary:	Additional artwork (themes, sound themes, ...) for TDE
Version:	3.5.13.2
Release:	1%{?dist}%{?_variant}

License:	GPLv2
Group:		User Interface/Desktops
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Vendor:		Trinity Project
Packager:	Francois Andriot <francois.andriot@free.fr>
Url:		http://www.trinitydesktop.org/

Source:		kdeartwork-trinity-%{version}.tar.xz

# [kdeartwork] Renames theme 'Locolor' to 'locolor'
Patch1:		kdeartwork-3.5.13.1-fix_locolor_theme_name.patch.gz

BuildRequires:	cmake >= 2.8
BuildRequires:	trinity-tdebase-devel >= %{version}

BuildRequires:	gettext
BuildRequires:	esound-devel

# kdeartwork specific settings

# NAS support
%if 0%{?fedora} || 0%{?mgaversion} || 0%{?mdkversion}
BuildRequires:	nas-devel
%endif

# LIBART support
#  On RHEL, libart is too old !
%if 0%{?fedora} >= 15 || 0%{?mgaversion} || 0%{?mdkversion} || 0%{?suse_version}
%define with_libart 1
BuildRequires:	libart_lgpl-devel
%endif

# XSCREENSAVER support
%if 0%{?fedora} >= 15 || 0%{?mgaversion} || 0%{?mdkversion} || 0%{?rhel} >= 6 || 0%{?suse_version}
%define with_xscreensaver 1
%if 0%{?mgaversion} || 0%{?mdkversion}
BuildRequires:	%{_lib}xscrnsaver%{?mgaversion:1}-devel
BuildRequires:	xscreensaver
BuildRequires:	xscreensaver-base
BuildRequires:	xscreensaver-extrusion
BuildRequires:	xscreensaver-gl
%endif
%if 0%{?fedora} || 0%{?rhel} >= 6 || 0%{?suse_version}
BuildRequires:	libXScrnSaver-devel
%endif

%if 0%{?fedora} || 0%{?rhel} >= 6 
# Provides '/usr/share/xscreensaver/config/deco.xml'
BuildRequires:	xscreensaver-extras
%endif
%if 0%{?suse_version}
BuildRequires:	xscreensaver-data-extra
%endif

# Opensuse does not provide 'webcollage' screensaver
%if 0%{?suse_version} == 0
%define with_webcollage 1
%endif

%endif

# JACK support
%if 0%{?mgaversion} || 0%{?mdkversion}
BuildRequires:	%{_lib}jack-devel
%endif
%if 0%{?fedora} || 0%{?rhel} >= 5
BuildRequires:	jack-audio-connection-kit-devel
%endif


Obsoletes:	trinity-kdeartwork < %{version}-%{release}
Provides:	trinity-kdeartwork = %{version}-%{release}

# Metapackage
Requires: %{name}-emoticons = %{version}-%{release}
Requires: %{name}-misc = %{version}-%{release}
Requires: %{name}-style = %{version}-%{release}
Requires: %{name}-theme-icon = %{version}-%{release}
Requires: %{name}-theme-window = %{version}-%{release}
Requires: trinity-kdewallpapers = %{version}-%{release}
Requires: trinity-kscreensaver = %{version}-%{release}

%if 0%{?with_xscreensaver}
Requires: trinity-kscreensaver-xsavers = %{version}-%{release}
Requires: trinity-kscreensaver-xsavers-extra = %{version}-%{release}
%if 0%{?with_webcollage}
Requires: trinity-kscreensaver-xsavers-webcollage = %{version}-%{release}
%endif
%endif


%description
TDE (the Trinity Desktop Environment) is a powerful Open Source graphical
desktop environment for Unix workstations. It combines ease of use,
contemporary functionality, and outstanding graphical design with the
technological superiority of the Unix operating system.

This metapackage includes a collection of artistic extras (themes, widget
styles, screen savers, wallpaper, icons, emoticons and so on) provided
with the official release of KDE.

Homepage: http://artist.kde.org 

%files

##########

%package emoticons
Summary:	emoticon collections for tDE chat clients
Group:		User Interface/Desktops

%description emoticons
This package contains several collections of emoticons used by official
and unofficial KDE chat clients, such as Kopete and Konversation.

This package is part of KDE, and a component of the KDE artwork module.

%files emoticons
%defattr(-,root,root,-)
%{tde_datadir}/emoticons/

##########

%package misc
Summary:	various multimedia goodies released with TDE
Group:		User Interface/Desktops

%description misc
This package contains miscellaneous multimedia goodies for KDE.
Included are additional TDE sounds and kworldclock themes.

This package is part of Trinity, and a component of the TDE artwork module.

%files misc
%defattr(-,root,root,-)
%{tde_datadir}/apps/kworldclock/
%{tde_datadir}/sounds/KDE_Logout_new.wav
%{tde_datadir}/sounds/KDE_Startup_new.wav

##########

%package style
Summary:	widget styles released with Trinity
Group:		User Interface/Desktops

%description style
This package contains additional widget styles for Trinity. Widget styles
can be used to customise the look and feel of interface components such
as buttons, scrollbars and so on.  They can be applied using the style
manager in the TDE Control Centre.

This package is part of Trinity, and a component of the TDE artwork module.

%files style
%defattr(-,root,root,-)
%{tde_tdelibdir}/plugins/styles/
%{tde_tdelibdir}/kstyle_phase_config.la
%{tde_tdelibdir}/kstyle_phase_config.so
%{tde_datadir}/apps/kstyle/

##########

%package theme-icon
Summary:	icon themes released with Trinity
Group:		User Interface/Desktops

Obsoletes:	trinity-kdeartwork-icons < %{version}-%{release}
Provides:	trinity-kdeartwork-icons = %{version}-%{release}

%description theme-icon
This package contains additional icon themes for Trinity. Icon themes can be
used to customise the appearance of standard icons throughout KDE. They
can be applied using the icon manager in the Trinity Control Centre.

This package is part of Trinity, and a component of the TDE artwork module.

%files theme-icon
%defattr(-,root,root,-)
%{tde_datadir}/icons/*/*

%post theme-icon
for i in locolor ikons kdeclassic kids slick ; do
 touch --no-create %{tde_datadir}/icons/$i 2>/dev/null || :
 gtk-update-icon-cache --quiet %{tde_datadir}/icons/$i 2>/dev/null || :
done

%postun theme-icon
for i in locolor ikons kdeclassic kids slick ; do
 touch --no-create %{tde_datadir}/icons/$i 2>/dev/null || :
 gtk-update-icon-cache --quiet %{tde_datadir}/icons/$i 2>/dev/null || :
done

##########

%package theme-window
Summary:	window decoration themes released with Trinity
Group:		User Interface/Desktops

%description theme-window
This package contains additional window decoration themes for Trinity. Window
decoration themes can be used to customise the look of window borders and
buttons, and can be applied using the window decoration manager in the Trinity
Control Center.

This package is part of Trinity, and a component of the TDE artwork module.

%files theme-window
%defattr(-,root,root,-)
%{tde_tdelibdir}/[kt]win*
%{tde_datadir}/apps/[kt]win/

##########

%package -n trinity-kdewallpapers
Summary:	wallpapers released with Trinity
Group:		User Interface/Desktops

%description -n trinity-kdewallpapers
This package contains additional wallpapers for Trinity. Wallpapers can be
applied using the background manager in the TDE Control Centre.

This package is part of Trinity, and a component of the TDE artwork module.

%files -n trinity-kdewallpapers
%defattr(-,root,root,-)
%{tde_datadir}/wallpapers/

##########

%package -n trinity-kscreensaver
Summary:	additional screen savers released with Trinity
Group:		User Interface/Desktops

%description -n trinity-kscreensaver
This package contains the screen savers for Trinity. They can be tested and
selected within the Appearance and Themes section of the Trinity Control
Center.

The hooks for the standard xscreensavers are no longer part of this
package. To select and/or configure the standard xscreensavers through
the TDE Control Center, install the separate package kscreensaver-xsavers.

This package is part of Trinity, and a component of the TDE artwork module.

%files -n trinity-kscreensaver
%defattr(-,root,root,-)
%{tde_bindir}/kslideshow.kss
%{tde_bindir}/kpolygon.kss
%{tde_bindir}/krotation.kss
%{tde_bindir}/ksolarwinds.kss
%{tde_bindir}/klorenz.kss
%{tde_bindir}/kvm.kss
%{tde_bindir}/kflux.kss
%{tde_bindir}/kscience.kss
%{tde_bindir}/kbanner.kss
%{tde_bindir}/kclock.kss
%{tde_bindir}/kfiresaver.kss
%{tde_bindir}/keuphoria.kss
%{tde_bindir}/kfountain.kss
%{tde_bindir}/kgravity.kss
%{tde_bindir}/kpartsaver.kss
%{tde_bindir}/kpendulum.kss
%{tde_bindir}/kblob.kss
%{tde_bindir}/klines.kss
%{tde_bindir}/kwave.kss
%{tde_bindir}/xscreensaver-getimage
%{tde_bindir}/xscreensaver-getimage-file
%{tde_datadir}/applnk/System/ScreenSavers/KBanner.desktop
%{tde_datadir}/applnk/System/ScreenSavers/KBlob.desktop
%{tde_datadir}/applnk/System/ScreenSavers/KClock.desktop
%{tde_datadir}/applnk/System/ScreenSavers/KEuphoria.desktop
%{tde_datadir}/applnk/System/ScreenSavers/KFiresaver.desktop
%{tde_datadir}/applnk/System/ScreenSavers/KFlux.desktop
%{tde_datadir}/applnk/System/ScreenSavers/KFountain.desktop
%{tde_datadir}/applnk/System/ScreenSavers/KGravity.desktop
%{tde_datadir}/applnk/System/ScreenSavers/KLines-saver.desktop
%{tde_datadir}/applnk/System/ScreenSavers/KLorenz.desktop
%{tde_datadir}/applnk/System/ScreenSavers/KPendulum.desktop
%{tde_datadir}/applnk/System/ScreenSavers/KPolygon.desktop
%{tde_datadir}/applnk/System/ScreenSavers/KRotation.desktop
%{tde_datadir}/applnk/System/ScreenSavers/KScience.desktop
%{tde_datadir}/applnk/System/ScreenSavers/KSlideshow.desktop
%{tde_datadir}/applnk/System/ScreenSavers/KSolarWinds.desktop
%{tde_datadir}/applnk/System/ScreenSavers/KVm.desktop
%{tde_datadir}/applnk/System/ScreenSavers/KWave.desktop
%{tde_datadir}/applnk/System/ScreenSavers/kpartsaver.desktop
%{tde_datadir}/apps/kfiresaver/
%{tde_datadir}/apps/kscreensaver/

%if 0%{?with_xscreensaver}
%{tde_bindir}/kspace.kss
%{tde_bindir}/kswarm.kss
%{tde_datadir}/applnk/System/ScreenSavers/KSpace.desktop
%{tde_datadir}/applnk/System/ScreenSavers/KSwarm.desktop
%endif

##########

%if 0%{?with_xscreensaver}

%package -n trinity-kscreensaver-xsavers
Summary:	Trinity hooks for standard xscreensavers
Group:		User Interface/Desktops
Requires:	trinity-tdebase-bin >= 3.5.13
Requires:	xscreensaver

%description -n trinity-kscreensaver-xsavers
This package allows a smooth integration of the standard xscreensavers
into Trinity. With this package installed you can select and/or configure
the standard xscreensavers through the Appearances and Themes section of
the Trinity Control Centre.

Note that this package does not actually contain any screensavers itself.
For the additional screensavers shipped with Trinity, see the separate package
kscreensaver-trinity. This package does depend on the xscreensaver package, and
recommend the xscreensaver-gl package, as well as contain the necessary
files to integrate these packages into Trinity.

This package is part of Trinity, and a component of the TDE artwork module.

%files -n trinity-kscreensaver-xsavers
%defattr(-,root,root,-)
#%{tde_bindir}/xscreensaver-getimage-file
#%{tde_bindir}/xscreensaver-getimage
%{tde_bindir}/kxsconfig
%{tde_bindir}/kxsrun
%{tde_datadir}/applnk/System/ScreenSavers/antinspect.desktop
%{tde_datadir}/applnk/System/ScreenSavers/antspotlight.desktop
%{tde_datadir}/applnk/System/ScreenSavers/atunnel.desktop
%{tde_datadir}/applnk/System/ScreenSavers/blinkbox.desktop
%{tde_datadir}/applnk/System/ScreenSavers/braid.desktop
%{tde_datadir}/applnk/System/ScreenSavers/bubble3d.desktop
%{tde_datadir}/applnk/System/ScreenSavers/circuit.desktop
%{tde_datadir}/applnk/System/ScreenSavers/cubestorm.desktop
%{tde_datadir}/applnk/System/ScreenSavers/deco.desktop
%{tde_datadir}/applnk/System/ScreenSavers/distort.desktop
%{tde_datadir}/applnk/System/ScreenSavers/endgame.desktop
%{tde_datadir}/applnk/System/ScreenSavers/engine.desktop
%{tde_datadir}/applnk/System/ScreenSavers/fiberlamp.desktop
%{tde_datadir}/applnk/System/ScreenSavers/flipflop.desktop
%{tde_datadir}/applnk/System/ScreenSavers/flipscreen3d.desktop
%{tde_datadir}/applnk/System/ScreenSavers/flyingtoasters.desktop
%{tde_datadir}/applnk/System/ScreenSavers/fuzzyflakes.desktop
%{tde_datadir}/applnk/System/ScreenSavers/galaxy.desktop
%{tde_datadir}/applnk/System/ScreenSavers/gears.desktop
%{tde_datadir}/applnk/System/ScreenSavers/gflux.desktop
%{tde_datadir}/applnk/System/ScreenSavers/glblur.desktop
%{tde_datadir}/applnk/System/ScreenSavers/gleidescope.desktop
%{tde_datadir}/applnk/System/ScreenSavers/glknots.desktop
%{tde_datadir}/applnk/System/ScreenSavers/glslideshow.desktop
%{tde_datadir}/applnk/System/ScreenSavers/glsnake.desktop
%{tde_datadir}/applnk/System/ScreenSavers/gltext.desktop
%{tde_datadir}/applnk/System/ScreenSavers/hypertorus.desktop
%{tde_datadir}/applnk/System/ScreenSavers/jigglypuff.desktop
%{tde_datadir}/applnk/System/ScreenSavers/lavalite.desktop
%{tde_datadir}/applnk/System/ScreenSavers/metaballs.desktop
%{tde_datadir}/applnk/System/ScreenSavers/mirrorblob.desktop
%{tde_datadir}/applnk/System/ScreenSavers/moebius.desktop
%{tde_datadir}/applnk/System/ScreenSavers/molecule.desktop
%{tde_datadir}/applnk/System/ScreenSavers/morph3d.desktop
%{tde_datadir}/applnk/System/ScreenSavers/penrose.desktop
%{tde_datadir}/applnk/System/ScreenSavers/pipes.desktop
%{tde_datadir}/applnk/System/ScreenSavers/polyhedra.desktop
%{tde_datadir}/applnk/System/ScreenSavers/polytopes.desktop
%{tde_datadir}/applnk/System/ScreenSavers/popsquares.desktop
%{tde_datadir}/applnk/System/ScreenSavers/pulsar.desktop
%{tde_datadir}/applnk/System/ScreenSavers/queens.desktop
%{tde_datadir}/applnk/System/ScreenSavers/ripples.desktop
%{tde_datadir}/applnk/System/ScreenSavers/shadebobs.desktop
%{tde_datadir}/applnk/System/ScreenSavers/sierpinski3d.desktop
%{tde_datadir}/applnk/System/ScreenSavers/slidescreen.desktop
%{tde_datadir}/applnk/System/ScreenSavers/sonar.desktop
%{tde_datadir}/applnk/System/ScreenSavers/spheremonics.desktop
%{tde_datadir}/applnk/System/ScreenSavers/stonerview.desktop
%{tde_datadir}/applnk/System/ScreenSavers/superquadrics.desktop
%{tde_datadir}/applnk/System/ScreenSavers/swirl.desktop
%{tde_datadir}/applnk/System/ScreenSavers/xlyap.desktop
%{tde_datadir}/applnk/System/ScreenSavers/m6502.desktop
%{tde_datadir}/applnk/System/ScreenSavers/glschool.desktop
%{tde_datadir}/applnk/System/ScreenSavers/moebiusgears.desktop
%{tde_datadir}/applnk/System/ScreenSavers/glcells.desktop
%{tde_datadir}/applnk/System/ScreenSavers/abstractile.desktop
%{tde_datadir}/applnk/System/ScreenSavers/lockward.desktop
%{tde_datadir}/applnk/System/ScreenSavers/cwaves.desktop
%{tde_datadir}/applnk/System/ScreenSavers/topblock.desktop
%{tde_datadir}/applnk/System/ScreenSavers/voronoi.desktop
%{tde_datadir}/applnk/System/ScreenSavers/cubicgrid.desktop
%{tde_datadir}/applnk/System/ScreenSavers/hypnowheel.desktop
%{tde_datadir}/applnk/System/ScreenSavers/lcdscrub.desktop
%{tde_datadir}/applnk/System/ScreenSavers/photopile.desktop
%{tde_datadir}/applnk/System/ScreenSavers/skytentacles.desktop

# These screensavers do not exist on Mageia 2
%if 0%{?mgaversion} == 0 && 0%{?mdkversion} == 0
%{tde_datadir}/applnk/System/ScreenSavers/glmatrix.desktop
%endif

##########

%if 0%{?with_webcollage}

%package -n trinity-kscreensaver-xsavers-webcollage
Summary:	webcollage screensaver Trinity hook
Group:		User Interface/Desktops
Requires:	trinity-kscreensaver-xsavers-extra = %{version}-%{release}
Requires:	netpbm

%description -n trinity-kscreensaver-xsavers-webcollage
This package give access to the webcollage screensaver through the Trinity
screensaver configuration.

This screensaver downloads random pictures from the internet and creates
a collage as screensaver.

IMPORTANT NOTICE: The internet contains all kinds of pictures, some of which
you might find inappropriate and offensive.
You are specially discouraged to install this package if you are using 
your computer in a working environment or in an environment with children.

If you still want to install this package, please read the file
/usr/share/doc/kscreensaver-xsavers-webcollage/README.Debian after the 
installation.

This package is part of Trinity, and a component of the TDE artwork module.

%files -n trinity-kscreensaver-xsavers-webcollage
%defattr(-,root,root,-)
%{tde_datadir}/applnk/System/ScreenSavers/webcollage.desktop

%endif

##########

%package -n trinity-kscreensaver-xsavers-extra
Summary:	Trinity hooks for standard xscreensavers
Group:		User Interface/Desktops
Requires:	trinity-kscreensaver-xsavers = %{version}-%{release}

%description -n trinity-kscreensaver-xsavers-extra
This package allows a smooth integration of the universe xscreensavers
into Trinity. With this package installed you can select and/or configure
the universe xscreensavers through the Appearances and Themes section of
the Trinity Control Centre.

Note that this package does not actually contain any screensavers itself.
For the additional screensavers shipped with TDE, see the separate package
kscreensaver.

This package is part of Trinity, and a component of the TDE artwork module.

%files -n trinity-kscreensaver-xsavers-extra
%defattr(-,root,root,-)
%{tde_datadir}/applnk/System/ScreenSavers/anemone.desktop
%{tde_datadir}/applnk/System/ScreenSavers/anemotaxis.desktop
%{tde_datadir}/applnk/System/ScreenSavers/antmaze.desktop
%{tde_datadir}/applnk/System/ScreenSavers/apollonian.desktop
%{tde_datadir}/applnk/System/ScreenSavers/apple2.desktop
%{tde_datadir}/applnk/System/ScreenSavers/atlantis.desktop
%{tde_datadir}/applnk/System/ScreenSavers/attraction.desktop
%{tde_datadir}/applnk/System/ScreenSavers/barcode.desktop
%{tde_datadir}/applnk/System/ScreenSavers/blaster.desktop
%{tde_datadir}/applnk/System/ScreenSavers/blitspin.desktop
%{tde_datadir}/applnk/System/ScreenSavers/blocktube.desktop
%{tde_datadir}/applnk/System/ScreenSavers/boing.desktop
%{tde_datadir}/applnk/System/ScreenSavers/bouboule.desktop
%{tde_datadir}/applnk/System/ScreenSavers/bouncingcow.desktop
%{tde_datadir}/applnk/System/ScreenSavers/boxed.desktop
%{tde_datadir}/applnk/System/ScreenSavers/boxfit.desktop
%{tde_datadir}/applnk/System/ScreenSavers/bsod.desktop
%{tde_datadir}/applnk/System/ScreenSavers/bumps.desktop
%{tde_datadir}/applnk/System/ScreenSavers/cage.desktop
%{tde_datadir}/applnk/System/ScreenSavers/carousel.desktop
%{tde_datadir}/applnk/System/ScreenSavers/ccurve.desktop
%{tde_datadir}/applnk/System/ScreenSavers/celtic.desktop
%{tde_datadir}/applnk/System/ScreenSavers/cloudlife.desktop
%{tde_datadir}/applnk/System/ScreenSavers/compass.desktop
%{tde_datadir}/applnk/System/ScreenSavers/coral.desktop
%{tde_datadir}/applnk/System/ScreenSavers/crackberg.desktop
%{tde_datadir}/applnk/System/ScreenSavers/crystal.desktop
%{tde_datadir}/applnk/System/ScreenSavers/cube21.desktop
%{tde_datadir}/applnk/System/ScreenSavers/cubenetic.desktop
%{tde_datadir}/applnk/System/ScreenSavers/cynosure.desktop
%{tde_datadir}/applnk/System/ScreenSavers/dangerball.desktop
%{tde_datadir}/applnk/System/ScreenSavers/decayscreen.desktop
%{tde_datadir}/applnk/System/ScreenSavers/deluxe.desktop
%{tde_datadir}/applnk/System/ScreenSavers/demon.desktop
%{tde_datadir}/applnk/System/ScreenSavers/discrete.desktop
%{tde_datadir}/applnk/System/ScreenSavers/drift.desktop
%{tde_datadir}/applnk/System/ScreenSavers/epicycle.desktop
%{tde_datadir}/applnk/System/ScreenSavers/eruption.desktop
%{tde_datadir}/applnk/System/ScreenSavers/euler2d.desktop
%{tde_datadir}/applnk/System/ScreenSavers/extrusion.desktop
%{tde_datadir}/applnk/System/ScreenSavers/fadeplot.desktop
%{tde_datadir}/applnk/System/ScreenSavers/fireworkx.desktop
%{tde_datadir}/applnk/System/ScreenSavers/flame.desktop
%{tde_datadir}/applnk/System/ScreenSavers/fliptext.desktop
%{tde_datadir}/applnk/System/ScreenSavers/flow.desktop
%{tde_datadir}/applnk/System/ScreenSavers/fluidballs.desktop
%{tde_datadir}/applnk/System/ScreenSavers/flurry.desktop
%{tde_datadir}/applnk/System/ScreenSavers/fontglide.desktop
%{tde_datadir}/applnk/System/ScreenSavers/glhanoi.desktop
%{tde_datadir}/applnk/System/ScreenSavers/glplanet.desktop
%{tde_datadir}/applnk/System/ScreenSavers/goop.desktop
%{tde_datadir}/applnk/System/ScreenSavers/grav.desktop
%{tde_datadir}/applnk/System/ScreenSavers/greynetic.desktop
%{tde_datadir}/applnk/System/ScreenSavers/halftone.desktop
%{tde_datadir}/applnk/System/ScreenSavers/halo.desktop
%{tde_datadir}/applnk/System/ScreenSavers/helix.desktop
%{tde_datadir}/applnk/System/ScreenSavers/hopalong.desktop
%{tde_datadir}/applnk/System/ScreenSavers/ifs.desktop
%{tde_datadir}/applnk/System/ScreenSavers/imsmap.desktop
%{tde_datadir}/applnk/System/ScreenSavers/interaggregate.desktop
%{tde_datadir}/applnk/System/ScreenSavers/interference.desktop
%{tde_datadir}/applnk/System/ScreenSavers/intermomentary.desktop
%{tde_datadir}/applnk/System/ScreenSavers/jigsaw.desktop
%{tde_datadir}/applnk/System/ScreenSavers/juggler3d.desktop
%{tde_datadir}/applnk/System/ScreenSavers/julia.desktop
%{tde_datadir}/applnk/System/ScreenSavers/kaleidescope.desktop
%{tde_datadir}/applnk/System/ScreenSavers/klein.desktop
%{tde_datadir}/applnk/System/ScreenSavers/kumppa.desktop
%{tde_datadir}/applnk/System/ScreenSavers/lament.desktop
%{tde_datadir}/applnk/System/ScreenSavers/loop.desktop
%{tde_datadir}/applnk/System/ScreenSavers/maze.desktop
%{tde_datadir}/applnk/System/ScreenSavers/memscroller.desktop
%{tde_datadir}/applnk/System/ScreenSavers/menger.desktop
%{tde_datadir}/applnk/System/ScreenSavers/moire.desktop
%{tde_datadir}/applnk/System/ScreenSavers/moire2.desktop
%{tde_datadir}/applnk/System/ScreenSavers/mountain.desktop
%{tde_datadir}/applnk/System/ScreenSavers/munch.desktop
%{tde_datadir}/applnk/System/ScreenSavers/nerverot.desktop
%{tde_datadir}/applnk/System/ScreenSavers/noof.desktop
%{tde_datadir}/applnk/System/ScreenSavers/noseguy.desktop
%{tde_datadir}/applnk/System/ScreenSavers/pacman.desktop
%{tde_datadir}/applnk/System/ScreenSavers/pedal.desktop
%{tde_datadir}/applnk/System/ScreenSavers/penetrate.desktop
%{tde_datadir}/applnk/System/ScreenSavers/petri.desktop
%{tde_datadir}/applnk/System/ScreenSavers/phosphor.desktop
%{tde_datadir}/applnk/System/ScreenSavers/piecewise.desktop
%{tde_datadir}/applnk/System/ScreenSavers/pinion.desktop
%{tde_datadir}/applnk/System/ScreenSavers/polyominoes.desktop
%{tde_datadir}/applnk/System/ScreenSavers/pong.desktop
%{tde_datadir}/applnk/System/ScreenSavers/providence.desktop
%{tde_datadir}/applnk/System/ScreenSavers/pyro.desktop
%{tde_datadir}/applnk/System/ScreenSavers/qix.desktop
%{tde_datadir}/applnk/System/ScreenSavers/rd-bomb.desktop
%{tde_datadir}/applnk/System/ScreenSavers/rocks.desktop
%{tde_datadir}/applnk/System/ScreenSavers/rorschach.desktop
%{tde_datadir}/applnk/System/ScreenSavers/rotzoomer.desktop
%{tde_datadir}/applnk/System/ScreenSavers/rubik.desktop
%{tde_datadir}/applnk/System/ScreenSavers/sballs.desktop
%{tde_datadir}/applnk/System/ScreenSavers/sierpinski.desktop
%{tde_datadir}/applnk/System/ScreenSavers/slip.desktop
%{tde_datadir}/applnk/System/ScreenSavers/speedmine.desktop
%{tde_datadir}/applnk/System/ScreenSavers/spotlight.desktop
%{tde_datadir}/applnk/System/ScreenSavers/sproingies.desktop
%{tde_datadir}/applnk/System/ScreenSavers/squiral.desktop
%{tde_datadir}/applnk/System/ScreenSavers/stairs.desktop
%{tde_datadir}/applnk/System/ScreenSavers/starfish.desktop
%{tde_datadir}/applnk/System/ScreenSavers/starwars.desktop
%{tde_datadir}/applnk/System/ScreenSavers/strange.desktop
%{tde_datadir}/applnk/System/ScreenSavers/substrate.desktop
%{tde_datadir}/applnk/System/ScreenSavers/tangram.desktop
%{tde_datadir}/applnk/System/ScreenSavers/thornbird.desktop
%{tde_datadir}/applnk/System/ScreenSavers/timetunnel.desktop
%{tde_datadir}/applnk/System/ScreenSavers/triangle.desktop
%{tde_datadir}/applnk/System/ScreenSavers/truchet.desktop
%{tde_datadir}/applnk/System/ScreenSavers/twang.desktop
%{tde_datadir}/applnk/System/ScreenSavers/vermiculate.desktop
%{tde_datadir}/applnk/System/ScreenSavers/wander.desktop
%{tde_datadir}/applnk/System/ScreenSavers/whirlwindwarp.desktop
%{tde_datadir}/applnk/System/ScreenSavers/wormhole.desktop
%{tde_datadir}/applnk/System/ScreenSavers/xanalogtv.desktop
%{tde_datadir}/applnk/System/ScreenSavers/xflame.desktop
%{tde_datadir}/applnk/System/ScreenSavers/xrayswarm.desktop
%{tde_datadir}/applnk/System/ScreenSavers/xspirograph.desktop
%{tde_datadir}/applnk/System/ScreenSavers/zoom.desktop

# These screensavers do not exist on OpenSuse 12.2
%if 0%{?suse_version} == 0
%{tde_datadir}/applnk/System/ScreenSavers/vidwhacker.desktop
%endif

# These screensavers do not exist on Mageia 2 and Mandriva 2011
%if 0%{?mgaversion} == 0 && 0%{?mdkversion} == 0
%{tde_datadir}/applnk/System/ScreenSavers/xjack.desktop
%{tde_datadir}/applnk/System/ScreenSavers/xmatrix.desktop
%endif

%endif

##########

%if 0%{?suse_version}
%debug_package
%endif

##########

%prep
%setup -q -n kdeartwork-trinity-%{version}

%__sed -i 's/TQT_PREFIX/TDE_PREFIX/g' cmake/modules/FindTQt.cmake

%build
unset QTDIR || : ; . /etc/profile.d/qt3.sh
export PATH="%{tde_bindir}:${PATH}"
export PKG_CONFIG_PATH="%{tde_libdir}/pkgconfig"
export CMAKE_INCLUDE_PATH="%{tde_includedir}:%{tde_includedir}/tqt"
export LD_LIBRARY_PATH="%{tde_libdir}"

%if 0%{?rhel} || 0%{?fedora} || 0%{?suse_version}
%__mkdir_p build
cd build
%endif

%cmake \
  -DTDE_PREFIX=%{tde_prefix} \
  -DBIN_INSTALL_DIR=%{tde_bindir} \
  -DINCLUDE_INSTALL_DIR=%{tde_tdeincludedir} \
  -DLIB_INSTALL_DIR=%{tde_libdir} \
  -DSHARE_INSTALL_PREFIX=%{tde_datadir} \
  -DCMAKE_SKIP_RPATH="OFF" \
  -DSHARE_INSTALL_PREFIX=%{tde_datadir} \
  %{!?with_xscreensaver:-DWITH_XSCREENSAVER=OFF} \
  %{!?with_libart}:-DWITH_LIBART=OFF} \
  -DWITH_OPENGL=ON \
  -DWITH_ARTS=ON \
  -DBUILD_ALL=ON \
  ..

%__make %{?_smp_mflags}


%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf %{buildroot}
%__make install -C build DESTDIR=%{buildroot}

# webcollage -root -directory /usr/share/backgrounds/images #227683

# File lists
HTML_DIR=$(kde-config --expandvars --install html)
if [ -d %{buildroot}$HTML_DIR ]; then
for lang_dir in %{buildroot}$HTML_DIR/* ; do
  if [ -d $lang_dir ]; then
    lang=$(basename $lang_dir)
    echo "%lang($lang) $HTML_DIR/$lang/*" >> %{name}.lang
    # replace absolute symlinks with relative ones
    pushd $lang_dir
      for i in *; do
        [ -d $i -a -L $i/common ] && rm -f $i/common && ln -sf ../common $i/common
      done
    popd
  fi
done
fi

# Duplicate with trinity-kbabel (from tdesdk)
%__rm -f %{?buildroot}%{tde_datadir}/icons/locolor/16x16/apps/kbabel.png
%__rm -f %{?buildroot}%{tde_datadir}/icons/locolor/32x32/apps/kbabel.png

%clean
%__rm -rf %{buildroot}


%changelog
* Sun Sep 30 2012 Francois Andriot <francois.andriot@free.fr> - 3.5.13.1-1
- Initial build for TDE 3.5.13.1
