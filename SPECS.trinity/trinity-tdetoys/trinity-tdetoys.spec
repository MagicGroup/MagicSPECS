#
# spec file for package tdetoys (version R14)
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
%if "%{?tde_version}" == ""
%define tde_version 14.0.1
%endif
%define tde_pkg tdetoys
%define tde_prefix /opt/trinity
%define tde_bindir %{tde_prefix}/bin
%define tde_datadir %{tde_prefix}/share
%define tde_docdir %{tde_datadir}/doc
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}
%define tde_tdeappdir %{tde_datadir}/applications/tde
%define tde_tdedocdir %{tde_docdir}/tde
%define tde_tdeincludedir %{tde_includedir}/tde
%define tde_tdelibdir %{tde_libdir}/trinity

# If TDE is built in a specific prefix (e.g. /opt/trinity), the release will be suffixed with ".opt".
%if "%{?tde_prefix}" != "/usr"
%define _variant .opt
%endif


Name:		trinity-%{tde_pkg}
Summary:	Trinity Desktop Environment - Toys and Amusements
Version:	%{tde_version}
Release:	%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}%{?_variant}.2
Group:		Amusements/Graphics
URL:		http://www.trinitydesktop.org/

License:	GPLv2+

#Vendor:		Trinity Project
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:		%{tde_prefix}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:	%{name}-%{version}%{?preversion:~%{preversion}}.tar.gz

# Trinity dependencies
BuildRequires: trinity-tdelibs-devel >= %{tde_version}
BuildRequires: trinity-kdesktop >= %{tde_version}
BuildRequires: trinity-kicker >= %{tde_version}

BuildRequires:	cmake >= 2.8
BuildRequires:	gcc-c++
BuildRequires:	pkgconfig
BuildRequires:	fdupes


BuildRequires: desktop-file-utils
BuildRequires: gettext

# IDN support
BuildRequires:	libidn-devel

# GAMIN support
#  Not on openSUSE.
%define with_gamin 1
BuildRequires:	gamin-devel

# ACL support
BuildRequires:	libacl-devel

# PCRE support
BuildRequires:	pcre-devel

Obsoletes:		trinity-kdetoys < %{version}-%{release}
Provides:		trinity-kdetoys = %{version}-%{release}

# Metapackage
Requires: trinity-amor = %{version}-%{release}
Requires: trinity-eyesapplet = %{version}-%{release}
Requires: trinity-fifteenapplet = %{version}-%{release}
Requires: trinity-kmoon = %{version}-%{release}
Requires: trinity-kodo = %{version}-%{release}
Requires: trinity-kteatime = %{version}-%{release}
Requires: trinity-ktux = %{version}-%{release}
Requires: trinity-kweather = %{version}-%{release}
Requires: trinity-kworldclock = %{version}-%{release}


%description
Includes: 
* amor: Amusing Misuse Of Resources put's comic figures above your windows
* eyesapplet: a kicker applet similar to XEyes
* fifteenapplet: kicker applet, order 15 pieces in a 4x4 square by moving them
* kmoon: system tray applet showing the moon phase
* kodo: mouse movement meter
* kteatime: system tray applet that makes sure your tea doesn't get too strong
* ktux: Tux-in-a-Spaceship screen saver
* kweather: kicker applet that will display the current weather outside
* kworldwatch: application and kicker applet showing daylight area on the world
               globe

NOTE: kicker applets and screen savers require tdebase to be installed, 
and user to be logged-in to TDE.

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README

##########

%package -n trinity-amor
Summary:	a Trinity creature for your desktop
Group:		Amusements/Graphics

%description -n trinity-amor
AMOR stands for Amusing Misuse Of Resources. It provides several different
characters who prance around your X screen doing tricks and giving you tips.

Note that AMOR will only work with some window managers. Both TWin (the
TDE window manager) and Metacity (a GTK2 window manager) are supported.

This package is part of Trinity, and a component of the TDE toys module.

%files -n trinity-amor
%defattr(-,root,root,-)
%{tde_bindir}/amor
%{tde_datadir}/apps/amor/
%{tde_tdeappdir}/amor.desktop
%{tde_datadir}/icons/hicolor/*/apps/amor.png
%{tde_tdedocdir}/HTML/en/amor/
%doc AUTHORS COPYING README

%post -n trinity-amor
touch --no-create %{tde_datadir}/icons/hicolor ||:
gtk-update-icon-cache -q %{tde_datadir}/icons/hicolor 2> /dev/null ||:
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-amor
touch --no-create %{tde_datadir}/icons/hicolor ||:
gtk-update-icon-cache -q %{tde_datadir}/icons/hicolor 2> /dev/null ||:
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-eyesapplet
Summary:	eyes applet for Trinity
Group:		Amusements/Graphics

Requires:	trinity-kicker >= %{tde_version}

%description -n trinity-eyesapplet
An applet for the TDE panel containing a pair of eyes that follow your mouse
around the screen.

This package is part of Trinity, and a component of the TDE toys module.

%files -n trinity-eyesapplet
%defattr(-,root,root,-)
%{tde_tdelibdir}/eyes_panelapplet.la
%{tde_tdelibdir}/eyes_panelapplet.so
%{tde_datadir}/apps/kicker/applets/eyesapplet.desktop
%doc AUTHORS COPYING README

##########

%package -n trinity-fifteenapplet
Summary:	fifteen pieces puzzle for Trinity
Group:		Amusements/Graphics

%description -n trinity-fifteenapplet
An applet for the TDE panel that lets you play the Fifteen Pieces
sliding block puzzle. You have to order 15 pieces in a 4x4 square by
moving them around.

This package is part of Trinity, and a component of the TDE toys module.

%files -n trinity-fifteenapplet
%defattr(-,root,root,-)
%{tde_tdelibdir}/fifteen_panelapplet.la
%{tde_tdelibdir}/fifteen_panelapplet.so
%{tde_datadir}/apps/kicker/applets/kfifteenapplet.desktop
%doc AUTHORS COPYING README

##########

%package -n trinity-kmoon
Summary:	moon phase indicator for Trinity
Group:		Amusements/Graphics

Requires:	trinity-kicker >= %{tde_version}

%description -n trinity-kmoon
An applet for the TDE panel that displays the current phase of the moon.

This package is part of Trinity, and a component of the TDE toys module.

%files -n trinity-kmoon
%defattr(-,root,root,-)
%{tde_tdelibdir}/kmoon_panelapplet.la
%{tde_tdelibdir}/kmoon_panelapplet.so
%{tde_datadir}/apps/kicker/applets/kmoonapplet.desktop
%{tde_datadir}/apps/kmoon/
%{tde_datadir}/icons/hicolor/*/apps/kmoon.png
%{tde_tdedocdir}/HTML/en/kmoon/
%doc AUTHORS COPYING README

%post -n trinity-kmoon
touch --no-create %{tde_datadir}/icons/hicolor ||:
gtk-update-icon-cache -q %{tde_datadir}/icons/hicolor 2> /dev/null ||:

%postun
touch --no-create %{tde_datadir}/icons/hicolor ||:
gtk-update-icon-cache -q %{tde_datadir}/icons/hicolor 2> /dev/null ||:

##########

%package -n trinity-kodo
Summary:	mouse odometer for Trinity
Group:		Amusements/Graphics

%description -n trinity-kodo
KOdometer measures your desktop mileage. It tracks the movement of your mouse
pointer across your desktop and renders it in inches/feet/miles! It can
do cm/metres/km too. Its most exciting feature is the tripometer.

This package is part of Trinity, and a component of the TDE toys module.

%files -n trinity-kodo
%defattr(-,root,root,-)
%{tde_bindir}/kodo
%{tde_tdeappdir}/kodo.desktop
%{tde_datadir}/apps/kodo/
%{tde_datadir}/icons/hicolor/*/apps/kodo.png
%{tde_tdedocdir}/HTML/en/kodo/
%doc AUTHORS COPYING README

%post -n trinity-kodo
touch --no-create %{tde_datadir}/icons/hicolor ||:
gtk-update-icon-cache -q %{tde_datadir}/icons/hicolor 2> /dev/null ||:
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-kodo
touch --no-create %{tde_datadir}/icons/hicolor ||:
gtk-update-icon-cache -q %{tde_datadir}/icons/hicolor 2> /dev/null ||:
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-kteatime
Summary:	Trinity utility for making a fine cup of tea
Group:		Amusements/Graphics

%description -n trinity-kteatime
KTeaTime is a handy timer for steeping tea. No longer will you have to
guess at how long it takes for your tea to be ready. Simply select the
type of tea you have, and it will alert you when the tea is ready to
drink.

KTeaTime sits in the Trinity system tray.

Please note that KTeaTime is written explicitly for Trinity. If you are
using a non-TDE window manager or desktop environment then it is quite
possible that KTeaTime will not work on your system.

This package is part of Trinity, and a component of the TDE toys module.

%files -n trinity-kteatime
%defattr(-,root,root,-)
%{tde_bindir}/kteatime
%{tde_tdeappdir}/kteatime.desktop
%{tde_datadir}/apps/kteatime/
%{tde_datadir}/icons/hicolor/*/apps/kteatime.png
%{tde_tdedocdir}/HTML/en/kteatime/
%doc AUTHORS COPYING README

%post -n trinity-kteatime
touch --no-create %{tde_datadir}/icons/hicolor ||:
gtk-update-icon-cache -q %{tde_datadir}/icons/hicolor 2> /dev/null ||:
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-kteatime
touch --no-create %{tde_datadir}/icons/hicolor ||:
gtk-update-icon-cache -q %{tde_datadir}/icons/hicolor 2> /dev/null ||:
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-ktux
Summary:	Tux screensaver for Trinity
Group:		Amusements/Graphics

%description -n trinity-ktux
A neat Tux-in-a-spaceship screensaver for the Trinity Desktop Environment (TDE).

This package is part of Trinity, and a component of the TDE toys module.

%files -n trinity-ktux
%defattr(-,root,root,-)
%{tde_bindir}/ktux
%{tde_datadir}/apps/ktux/
%{tde_datadir}/applnk/System/ScreenSavers/ktux.desktop
%{tde_datadir}/icons/hicolor/*/apps/ktux.png
%doc AUTHORS COPYING README

%post -n trinity-ktux
touch --no-create %{tde_datadir}/icons/hicolor ||:
gtk-update-icon-cache -q %{tde_datadir}/icons/hicolor 2> /dev/null ||:

%postun -n trinity-ktux
touch --no-create %{tde_datadir}/icons/hicolor ||:
gtk-update-icon-cache -q %{tde_datadir}/icons/hicolor 2> /dev/null ||:

##########

%package -n trinity-kweather
Summary:	weather display applet for Trinity
Group:		Amusements/Graphics

Requires:	trinity-kicker >= %{tde_version}

%description -n trinity-kweather
An applet for the TDE panel that displays your area's current weather.
Information shown includes the temperature, wind speed, air pressure
and more. By pressing a button a full weather report can be obtained.

KWeather also provides a weather service that can track multiple weather
stations and provide this information to other applications, including
Konqueror's sidebar and Kontact's summary page.

This package is part of Trinity, and a component of the TDE toys module.

%files -n trinity-kweather
%defattr(-,root,root,-)
%{tde_bindir}/kweatherservice
%{tde_bindir}/kweatherreport
%{tde_libdir}/libtdeinit_kweatherreport.so
%{tde_libdir}/libtdeinit_kweatherreport.la
%{tde_tdelibdir}/kcm_weather.so
%{tde_tdelibdir}/kcm_weather.la
%{tde_tdelibdir}/kcm_weatherservice.so
%{tde_tdelibdir}/kcm_weatherservice.la
%{tde_tdelibdir}/kweatherreport.so
%{tde_tdelibdir}/kweatherreport.la
%{tde_tdelibdir}/weather_panelapplet.la
%{tde_tdelibdir}/weather_panelapplet.so
%{tde_datadir}/apps/kicker/applets/kweather.desktop
%{tde_datadir}/apps/kweather/
%{tde_datadir}/apps/kweatherservice/
%{tde_datadir}/icons/hicolor/*/apps/kweather.png
%{tde_datadir}/services/kweatherservice.desktop
%{tde_datadir}/services/kcmweather.desktop
%{tde_datadir}/services/kcmweatherservice.desktop
%{tde_tdedocdir}/HTML/en/kweather/
%doc AUTHORS COPYING README

%post -n trinity-kweather
touch --no-create %{tde_datadir}/icons/hicolor ||:
gtk-update-icon-cache -q %{tde_datadir}/icons/hicolor 2> /dev/null ||:
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-kweather
touch --no-create %{tde_datadir}/icons/hicolor ||:
gtk-update-icon-cache -q %{tde_datadir}/icons/hicolor 2> /dev/null ||:
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-kworldclock
Summary:	earth watcher for Trinity
Group:		Amusements/Graphics

Requires:	trinity-kdesktop >= %{tde_version}
Requires:	trinity-kicker >= %{tde_version}

%description -n trinity-kworldclock
Displays where in the world it is light and dark depending on time, as
well as offering the time in all of the major cities of the world.
This can be run standalone, as an applet in the TDE panel or as a
desktop background.

Additional kworldclock themes are available in the tdeartwork-misc package.

This package is part of Trinity, and a component of the TDE toys module.

%files -n trinity-kworldclock
%defattr(-,root,root,-)
%{tde_bindir}/kworldclock
%{tde_tdelibdir}/ww_panelapplet.la
%{tde_tdelibdir}/ww_panelapplet.so
%{tde_tdeappdir}/kworldclock.desktop
%{tde_datadir}/apps/kdesktop/programs/kdeworld.desktop
%{tde_datadir}/apps/kicker/applets/kwwapplet.desktop
%{tde_datadir}/apps/kworldclock/
%{tde_datadir}/icons/hicolor/*/apps/kworldclock.png
%{tde_tdedocdir}/HTML/en/kworldclock/
%doc AUTHORS COPYING README

%post -n trinity-kworldclock
touch --no-create %{tde_datadir}/icons/hicolor ||:
gtk-update-icon-cache -q %{tde_datadir}/icons/hicolor 2> /dev/null ||:
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-kworldclock
touch --no-create %{tde_datadir}/icons/hicolor ||:
gtk-update-icon-cache -q %{tde_datadir}/icons/hicolor 2> /dev/null ||:
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%prep
%setup -q -n %{name}-%{version}%{?preversion:~%{preversion}}


%build
unset QTDIR QTINC QTLIB
export PATH="%{tde_bindir}:${PATH}"

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
  -DCMAKE_INSTALL_PREFIX="%{tde_prefix}" \
  -DBIN_INSTALL_DIR="%{tde_bindir}" \
  -DDOC_INSTALL_DIR="%{tde_docdir}" \
  -DINCLUDE_INSTALL_DIR="%{tde_tdeincludedir}" \
  -DLIB_INSTALL_DIR="%{tde_libdir}" \
  -DPKGCONFIG_INSTALL_DIR="%{tde_libdir}/pkgconfig" \
  -DSHARE_INSTALL_PREFIX="%{tde_datadir}" \
  \
  -DBUILD_ALL=ON \
  ..

%__make %{?_smp_mflags}


%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf "%{buildroot}"
%__make install DESTDIR=%{buildroot} -C build

# Useless include file from Amor
%__rm -f %{buildroot}%{tde_tdeincludedir}/AmorIface.h

# Updates applications categories for openSUSE
%if 0%{?suse_version}
%suse_update_desktop_file -r kworldclock Utility Clock
%suse_update_desktop_file -r kteatime    Applet
%suse_update_desktop_file -r amor        Amusement
%suse_update_desktop_file -r kodo        Amusement 
%suse_update_desktop_file ktux        Screensaver
%endif


%clean
%__rm -rf %{buildroot}


%changelog
* Sat Nov 14 2015 Liu Di <liudidi@gmail.com> - 14.0.1-1.opt.2
- 为 Magic 3.0 重建

* Thu Nov 05 2015 Liu Di <liudidi@gmail.com> - 14.0.1-1.opt.1
- 为 Magic 3.0 重建

* Fri Jul 05 2013 Francois Andriot <francois.andriot@free.fr> - 14.0.0-1
- Initial release for TDE 14.0.0
