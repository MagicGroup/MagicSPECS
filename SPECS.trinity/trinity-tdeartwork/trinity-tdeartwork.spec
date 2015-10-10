#
# spec file for package tdeartwork (version R14)
#
# Copyright (c) 2014 Trinity Desktop Environment
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.
#
# Please submit bugfixes or comments via http://www.trinitydesktop.org/
#

# BUILD WARNING:
#  Remove qt-devel and qt3-devel and any kde*-devel on your system !
#  Having KDE libraries may cause FTBFS here !

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.0.1
%endif
%define tde_pkg tdeartwork
%define tde_prefix /opt/trinity
%define tde_bindir %{tde_prefix}/bin
%define tde_datadir %{tde_prefix}/share
%define tde_docdir %{tde_datadir}/doc
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}
%define tde_sbindir %{tde_prefix}/sbin
%define tde_tdeappdir %{tde_datadir}/applications/tde
%define tde_tdedocdir %{tde_docdir}/tde
%define tde_tdeincludedir %{tde_includedir}/tde
%define tde_tdelibdir %{tde_libdir}/trinity

# If TDE is built in a specific prefix (e.g. /opt/trinity), the release will be suffixed with ".opt".
%if "%{?tde_prefix}" != "/usr"
%define _variant .opt
%endif


Name:		trinity-%{tde_pkg}
Summary:	Additional artwork (themes, sound themes, ...) for TDE
Version:	%{tde_version}
Release:	%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}%{?_variant}
Group:		System/GUI/Other
URL:		http://www.trinitydesktop.org/

License:	GPLv2+

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:		%{tde_prefix}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:		%{name}-%{version}%{?preversion:~%{preversion}}.tar.gz

Obsoletes:	trinity-kdeartwork < %{version}-%{release}
Provides:	trinity-kdeartwork = %{version}-%{release}

BuildRequires:	trinity-arts-devel >= %{tde_epoch}:1.5.10
BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}

BuildRequires:	cmake >= 2.8
BuildRequires:	gcc-c++
BuildRequires:	fdupes

BuildRequires:	gettext
BuildRequires:	libidn-devel

# ESOUND support
BuildRequires:	esound-devel

# ACL support
BuildRequires:	libacl-devel

# MESA support
BuildRequires: mesa-libGL-devel
BuildRequires: mesa-libGLU-devel

# LIBART support
%define with_libart 1
BuildRequires:	libart_lgpl-devel

# XSCREENSAVER support
#  RHEL 4: disabled
#  RHEL 6: available in EPEL
#  RHEL 7: available in NUX
%define with_xscreensaver 1

BuildRequires:	libXScrnSaver-devel
BuildRequires:	xscreensaver
BuildRequires:	xscreensaver-base
BuildRequires:	xscreensaver-extras
BuildRequires:	xscreensaver-extras-base

%define with_webcollage 1

# JACK support
%define with_jack 1
%define jack_devel jack-audio-connection-kit-devel
BuildRequires:	%{jack_devel}

# GAMIN support
#  Not on openSUSE.
%define with_gamin 1
BuildRequires:	gamin-devel


# Metapackage
Requires: %{name}-emoticons = %{version}-%{release}
Requires: %{name}-misc = %{version}-%{release}
Requires: %{name}-style = %{version}-%{release}
Requires: %{name}-theme-icon = %{version}-%{release}
Requires: %{name}-theme-window = %{version}-%{release}
Requires: trinity-tdewallpapers = %{version}-%{release}
Requires: trinity-tdescreensaver = %{version}-%{release}

%if 0%{?with_xscreensaver}
Requires: trinity-tdescreensaver-xsavers = %{version}-%{release}
Requires: trinity-tdescreensaver-xsavers-extra = %{version}-%{release}
%if 0%{?with_webcollage}
Requires: trinity-tdescreensaver-xsavers-webcollage = %{version}-%{release}
%endif
%endif


%description
TDE (the Trinity Desktop Environment) is a powerful Open Source graphical
desktop environment for Unix workstations. It combines ease of use,
contemporary functionality, and outstanding graphical design with the
technological superiority of the Unix operating system.

This metapackage includes a collection of artistic extras (themes, widget
styles, screen savers, wallpaper, icons, emoticons and so on) provided
with the official release of TDE.


%files

##########

%package emoticons
Summary:	Emoticon collections for tDE chat clients
Group:		System/GUI/Other

%description emoticons
This package contains several collections of emoticons used by official
and unofficial TDE chat clients, such as Kopete and Konversation.

This package is part of TDE, and a component of the TDE artwork module.

%files emoticons
%defattr(-,root,root,-)
%{tde_datadir}/emoticons/

##########

%package misc
Summary:	Various multimedia goodies released with TDE
Group:		System/GUI/Other

%description misc
This package contains miscellaneous multimedia goodies for TDE.
Included are additional TDE sounds and kworldclock themes.

This package is part of Trinity, and a component of the TDE artwork module.

%files misc
%defattr(-,root,root,-)
%{tde_datadir}/apps/kworldclock/
%{tde_datadir}/sounds/KDE_Logout_new.wav
%{tde_datadir}/sounds/KDE_Startup_new.wav

##########

%package style
Summary:	Widget styles released with Trinity
Group:		System/GUI/Other

%description style
This package contains additional widget styles for Trinity. Widget styles
can be used to customise the look and feel of interface components such
as buttons, scrollbars and so on.  They can be applied using the style
manager in the Trinity Control Center.

This package is part of Trinity, and a component of the TDE artwork module.

%files style
%defattr(-,root,root,-)
%{tde_tdelibdir}/plugins/styles/
%{tde_tdelibdir}/tdestyle_phase_config.la
%{tde_tdelibdir}/tdestyle_phase_config.so
%{tde_datadir}/apps/tdestyle/

##########

%package theme-icon
Summary:	Icon themes released with Trinity
Group:		System/GUI/Other

Obsoletes:	trinity-kdeartwork-icons < %{version}-%{release}
Provides:	trinity-kdeartwork-icons = %{version}-%{release}

%description theme-icon
This package contains additional icon themes for Trinity. Icon themes can be
used to customise the appearance of standard icons throughout TDE. They
can be applied using the icon manager in the Trinity Control Centre.

This package is part of Trinity, and a component of the TDE artwork module.

%files theme-icon
%defattr(-,root,root,-)
%{tde_datadir}/icons/ikons/
%{tde_datadir}/icons/kdeclassic/
%{tde_datadir}/icons/kids/
%{tde_datadir}/icons/slick/
%{tde_datadir}/icons/locolor/index.theme
%{tde_datadir}/icons/locolor/*/*/*.png

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
Summary:	Window decoration themes released with Trinity
Group:		System/GUI/Other

%description theme-window
This package contains additional window decoration themes for Trinity. Window
decoration themes can be used to customise the look of window borders and
buttons, and can be applied using the window decoration manager in the Trinity
Control Center.

This package is part of Trinity, and a component of the TDE artwork module.

%files theme-window
%defattr(-,root,root,-)
%{tde_tdelibdir}/twin*
%{tde_datadir}/apps/twin/

##########

%package -n trinity-tdewallpapers
Summary:	Wallpapers released with Trinity
Group:		System/GUI/Other
Obsoletes:	trinity-kdewallpapers < %{version}-%{release}
Provides:	trinity-kdewallpapers = %{version}-%{release}

%description -n trinity-tdewallpapers
This package contains additional wallpapers for Trinity. Wallpapers can be
applied using the background manager in the Trinity Control Center.

This package is part of Trinity, and a component of the TDE artwork module.

%files -n trinity-tdewallpapers
%defattr(-,root,root,-)
%{tde_datadir}/wallpapers/*

##########

%package -n trinity-tdescreensaver
Summary:	Additional screen savers released with Trinity
Group:		System/GUI/Other

Obsoletes:	trinity-kscreensaver < %{version}-%{release}
Provides:	trinity-kscreensaver = %{version}-%{release}

%description -n trinity-tdescreensaver
This package contains the screen savers for Trinity. They can be tested and
selected within the Appearance and Themes section of the Trinity Control
Center.

The hooks for the standard xscreensavers are no longer part of this
package. To select and/or configure the standard xscreensavers through
the Trinity Control Center, install the separate package tdescreensaver-xsavers.

This package is part of Trinity, and a component of the TDE artwork module.

%files -n trinity-tdescreensaver
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
%{tde_bindir}/tdepartsaver.kss
%{tde_bindir}/kpendulum.kss
%{tde_bindir}/kblob.kss
%{tde_bindir}/klines.kss
%{tde_bindir}/kwave.kss
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
%{tde_datadir}/applnk/System/ScreenSavers/tdepartsaver.desktop
%{tde_datadir}/apps/kfiresaver/
%{tde_datadir}/apps/tdescreensaver/

%if 0%{?with_xscreensaver}
%{tde_bindir}/kspace.kss
%{tde_bindir}/kswarm.kss
%{tde_datadir}/applnk/System/ScreenSavers/KSpace.desktop
%{tde_datadir}/applnk/System/ScreenSavers/KSwarm.desktop
%endif

##########

%if 0%{?with_xscreensaver}

%package -n trinity-tdescreensaver-xsavers
Summary:	Trinity hooks for standard xscreensavers
Group:		System/GUI/Other
Requires:	trinity-tdebase-bin >= %{tde_version}
Requires:	xscreensaver

Obsoletes:	trinity-kscreensaver-xsavers < %{version}-%{release}
Provides:	trinity-kscreensaver-xsavers = %{version}-%{release}

%description -n trinity-tdescreensaver-xsavers
This package allows a smooth integration of the standard xscreensavers
into Trinity. With this package installed you can select and/or configure
the standard xscreensavers through the Appearances and Themes section of
the Trinity Control Centre.

Note that this package does not actually contain any screensavers itself.
For the additional screensavers shipped with Trinity, see the separate package
tdescreensaver-trinity. This package does depend on the xscreensaver package, and
recommend the xscreensaver-gl package, as well as contain the necessary
files to integrate these packages into Trinity.

This package is part of Trinity, and a component of the TDE artwork module.

%files -n trinity-tdescreensaver-xsavers
%defattr(-,root,root,-)
%{tde_bindir}/xscreensaver-getimage-file
%{tde_bindir}/xscreensaver-getimage
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
%if 0%{?rhel} == 5
%{tde_datadir}/applnk/System/ScreenSavers/bubbles.desktop
%{tde_datadir}/applnk/System/ScreenSavers/critical.desktop
%{tde_datadir}/applnk/System/ScreenSavers/flag.desktop
%{tde_datadir}/applnk/System/ScreenSavers/forest.desktop
%{tde_datadir}/applnk/System/ScreenSavers/glforestfire.desktop
%{tde_datadir}/applnk/System/ScreenSavers/hyperball.desktop
%{tde_datadir}/applnk/System/ScreenSavers/hypercube.desktop
%{tde_datadir}/applnk/System/ScreenSavers/juggle.desktop
%{tde_datadir}/applnk/System/ScreenSavers/laser.desktop
%{tde_datadir}/applnk/System/ScreenSavers/lightning.desktop
%{tde_datadir}/applnk/System/ScreenSavers/lisa.desktop
%{tde_datadir}/applnk/System/ScreenSavers/lissie.desktop
%{tde_datadir}/applnk/System/ScreenSavers/lmorph.desktop
%{tde_datadir}/applnk/System/ScreenSavers/mismunch.desktop
%{tde_datadir}/applnk/System/ScreenSavers/rotor.desktop
%{tde_datadir}/applnk/System/ScreenSavers/sphere.desktop
%{tde_datadir}/applnk/System/ScreenSavers/spiral.desktop
%{tde_datadir}/applnk/System/ScreenSavers/t3d.desktop
%{tde_datadir}/applnk/System/ScreenSavers/vines.desktop
%{tde_datadir}/applnk/System/ScreenSavers/whirlygig.desktop
%{tde_datadir}/applnk/System/ScreenSavers/worm.desktop
%endif

##########

%if 0%{?with_webcollage}

%package -n trinity-tdescreensaver-xsavers-webcollage
Summary:	Webcollage screensaver Trinity hook
Group:		System/GUI/Other
Requires:	trinity-tdescreensaver-xsavers-extra = %{version}-%{release}
Requires:	netpbm

Obsoletes:	trinity-kscreensaver-xsavers-webcollage < %{version}-%{release}
Provides:	trinity-kscreensaver-xsavers-webcollage = %{version}-%{release}

%description -n trinity-tdescreensaver-xsavers-webcollage
This package give access to the webcollage screensaver through the Trinity
screensaver configuration.

This screensaver downloads random pictures from the internet and creates
a collage as screensaver.

IMPORTANT NOTICE: The internet contains all kinds of pictures, some of which
you might find inappropriate and offensive.
You are specially discouraged to install this package if you are using 
your computer in a working environment or in an environment with children.

This package is part of Trinity, and a component of the TDE artwork module.

%files -n trinity-tdescreensaver-xsavers-webcollage
%defattr(-,root,root,-)
%{tde_datadir}/applnk/System/ScreenSavers/webcollage.desktop

%endif

##########

%package -n trinity-tdescreensaver-xsavers-extra
Summary:	Trinity hooks for standard xscreensavers
Group:		System/GUI/Other
Requires:	trinity-tdescreensaver-xsavers = %{version}-%{release}

Obsoletes:	trinity-kscreensaver-xsavers-extra < %{version}-%{release}
Provides:	trinity-kscreensaver-xsavers-extra = %{version}-%{release}

%description -n trinity-tdescreensaver-xsavers-extra
This package allows a smooth integration of the universe xscreensavers
into Trinity. With this package installed you can select and/or configure
the universe xscreensavers through the Appearances and Themes section of
the Trinity Control Centre.

Note that this package does not actually contain any screensavers itself.
For the additional screensavers shipped with TDE, see the separate package
tdescreensaver.

This package is part of Trinity, and a component of the TDE artwork module.

%files -n trinity-tdescreensaver-xsavers-extra
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
%if 0%{?rhel} != 7
%{tde_datadir}/applnk/System/ScreenSavers/extrusion.desktop
%endif
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

# These screensavers do not exist on OpenSuse
%{tde_datadir}/applnk/System/ScreenSavers/vidwhacker.desktop

# These screensavers do not exist on Mageia / Mandriva
%{tde_datadir}/applnk/System/ScreenSavers/glmatrix.desktop
%{tde_datadir}/applnk/System/ScreenSavers/xjack.desktop
%{tde_datadir}/applnk/System/ScreenSavers/xmatrix.desktop

%{tde_datadir}/applnk/System/ScreenSavers/rubikblocks.desktop
%{tde_datadir}/applnk/System/ScreenSavers/surfaces.desktop

%{tde_datadir}/applnk/System/ScreenSavers/companioncube.desktop
%{tde_datadir}/applnk/System/ScreenSavers/hilbert.desktop
%{tde_datadir}/applnk/System/ScreenSavers/tronbit.desktop

%if 0
%{tde_datadir}/applnk/System/ScreenSavers/hexadrop.desktop
%{tde_datadir}/applnk/System/ScreenSavers/kaleidocycle.desktop
%{tde_datadir}/applnk/System/ScreenSavers/quasicrystal.desktop
%{tde_datadir}/applnk/System/ScreenSavers/unknownpleasures.desktop

%{tde_datadir}/applnk/System/ScreenSavers/geodesic.desktop
%endif

%{tde_datadir}/applnk/System/ScreenSavers/projectiveplane.desktop
%{tde_datadir}/applnk/System/ScreenSavers/tessellimage.desktop

%{tde_datadir}/applnk/System/ScreenSavers/winduprobot.desktop
%{tde_datadir}/applnk/System/ScreenSavers/binaryring.desktop
%{tde_datadir}/applnk/System/ScreenSavers/cityflow.desktop
%{tde_datadir}/applnk/System/ScreenSavers/geodesicgears.desktop

%endif

##########

%prep
%setup -q -n %{name}-%{version}%{?preversion:~%{preversion}}

# http://www.trinitydesktop.org/wiki/bin/view/Developers/HowToBuild
# NOTE: Before building tdeartwork, install any and all xhack screensavers that might be uses, then:
cd tdescreensaver/kxsconfig/
./update_hacks.sh


%build
unset QTDIR QTINC QTLIB
export PATH="%{tde_bindir}:${PATH}"
export PKG_CONFIG_PATH="%{tde_libdir}/pkgconfig"

if ! rpm -E %%cmake|grep -q "cd build"; then
  %__mkdir_p build
  cd build
fi

%cmake \
  -DCMAKE_BUILD_TYPE="RelWithDebInfo" \
  -DCMAKE_C_FLAGS="${RPM_OPT_FLAGS} -DNDEBUG" \
  -DCMAKE_CXX_FLAGS="${RPM_OPT_FLAGS} -DNDEBUG" \
  -DCMAKE_SKIP_RPATH=OFF \
  -DCMAKE_INSTALL_RPATH="%{tde_libdir}" \
  -DCMAKE_VERBOSE_MAKEFILE=ON \
  -DWITH_GCC_VISIBILITY=OFF \
  \
  -DBIN_INSTALL_DIR=%{tde_bindir} \
  -DINCLUDE_INSTALL_DIR=%{tde_tdeincludedir} \
  -DLIB_INSTALL_DIR=%{tde_libdir} \
  -DSHARE_INSTALL_PREFIX=%{tde_datadir} \
  -DSHARE_INSTALL_PREFIX=%{tde_datadir} \
  \
  %{!?with_xscreensaver:-DWITH_XSCREENSAVER=OFF} \
  %{!?with_libart}:-DWITH_LIBART=OFF} \
  -DWITH_OPENGL=ON \
  -DWITH_ARTS=ON \
  -DBUILD_ALL=ON \
  ..

%__make %{?_smp_mflags} || %__make


%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf "%{buildroot}"
%__make install -C build DESTDIR="%{buildroot}"

# Should not be here if xscreensaver is disabled
%if 0%{?with_xscreensaver} == 0
%__rm -f "%{?buildroot}%{tde_bindir}/xscreensaver-getimage"
%__rm -f "%{?buildroot}%{tde_bindir}/xscreensaver-getimage-file"
%endif

# Duplicate with trinity-kbabel (from tdesdk)
%__rm -f "%{?buildroot}%{tde_datadir}/icons/locolor/16x16/apps/kbabel.png"
%__rm -f "%{?buildroot}%{tde_datadir}/icons/locolor/32x32/apps/kbabel.png"

# Links duplicate files
%fdupes "%{?buildroot}%{tde_datadir}"

# Fix invalid permissions
%if 0%{?with_xscreensaver}
chmod +x "%{?buildroot}%{tde_bindir}/xscreensaver-getimage"
chmod +x "%{?buildroot}%{tde_bindir}/xscreensaver-getimage-file"
%endif

# Fix missing screensavers on Fedora 20
%if 0%{?with_xscreensaver} &&  0%{?fedora} >= 20
touch "%{?buildroot}%{tde_datadir}/applnk/System/ScreenSavers/binaryring.desktop"
touch "%{?buildroot}%{tde_datadir}/applnk/System/ScreenSavers/cityflow.desktop"
touch "%{?buildroot}%{tde_datadir}/applnk/System/ScreenSavers/geodesicgears.desktop"
touch "%{?buildroot}%{tde_datadir}/applnk/System/ScreenSavers/projectiveplane.desktop"
touch "%{?buildroot}%{tde_datadir}/applnk/System/ScreenSavers/tessellimage.desktop"
touch "%{?buildroot}%{tde_datadir}/applnk/System/ScreenSavers/winduprobot.desktop"
%endif


%clean
%__rm -rf %{buildroot}


%changelog
* Fri Jul 05 2013 Francois Andriot <francois.andriot@free.fr> - 14.0.0-1
- Initial release for TDE R14.0.0
