#
# spec file for package tdeaccessibility (version R14)
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
%define tde_pkg tdeaccessibility
%define tde_prefix /opt/trinity
%define tde_bindir %{tde_prefix}/bin
%define tde_confdir %{_sysconfdir}/trinity
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


Name:			trinity-tdeaccessibility
Summary:		Trinity Desktop Environment - Accessibility
Version:		%{tde_version}
Release:		%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}%{?_variant}.2
Group:			System/GUI/Other
URL:			http://www.trinitydesktop.org/

License:	GPLv2+

#Vendor:		Trinity Project
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:			%{tde_prefix}
BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:		%{name}-%{version}%{?preversion:~%{preversion}}.tar.gz
Patch1:			trinity-tdeaccessibility-14.0.1-tqt.patch

BuildRequires:	trinity-arts-devel >= %{tde_epoch}:1.5.10
BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	trinity-tdemultimedia-devel >= %{tde_version}

BuildRequires:	autoconf automake libtool m4
BuildRequires:	gcc-c++
BuildRequires:	desktop-file-utils
BuildRequires:	fdupes


# AUDIOFILE support
BuildRequires:	audiofile-devel

# AKODE support
%define with_akode 1
BuildRequires: trinity-akode-devel

%define with_mad 1
%{?with_mad:BuildRequires: libakode_mpeg_decoder}

# ALSA support
BuildRequires:	alsa-lib-devel

# XCB support
BuildRequires:	libxcb-devel

# XAU support
BuildRequires:	libXau-devel

Obsoletes:		trinity-kdeaccessibility < %{version}-%{release}
Provides:		trinity-kdeaccessibility = %{version}-%{release}
Obsoletes:		trinity-kdeaccessibility-libs < %{version}-%{release}
Provides:		trinity-kdeaccessibility-libs = %{version}-%{release}

Requires: trinity-tde-icons-mono = %{version}-%{release}
Requires: trinity-kbstate = %{version}-%{release}
Requires: trinity-kmag = %{version}-%{release}
Requires: trinity-kmousetool = %{version}-%{release}
Requires: trinity-kmouth = %{version}-%{release}
Requires: trinity-ksayit = %{version}-%{release}
Requires: trinity-kttsd = %{version}-%{release}
Requires: trinity-kttsd-contrib-plugins = %{version}-%{release}

%description
Included with this package are:
* kmag, a screen magnifier,
* kmousetool, a program for people whom it hurts to click the mouse,
* kmouth, program that allows people who have lost their voice
  to let their computer speak for them.

%files

##########

%package -n trinity-tde-icons-mono
Summary:	A monochromatic icons theme for TDE
Group:		System/GUI/Other

Obsoletes:	trinity-kde-icons-mono < %{version}-%{release}
Provides:	trinity-kde-icons-mono = %{version}-%{release}

%description -n trinity-tde-icons-mono
A monochromatic icon theme for TDE, designed for accessibility purposes.

This package is part of Trinity, as a component of the TDE accessibility module.

%files -n trinity-tde-icons-mono
%defattr(-,root,root,-)
%dir %{tde_datadir}/icons/mono
%dir %{tde_datadir}/icons/mono/scalable
%dir %{tde_datadir}/icons/mono/scalable/actions
%dir %{tde_datadir}/icons/mono/scalable/apps
%dir %{tde_datadir}/icons/mono/scalable/devices
%dir %{tde_datadir}/icons/mono/scalable/mimetypes
%dir %{tde_datadir}/icons/mono/scalable/places
%{tde_datadir}/icons/mono/index.theme
%{tde_datadir}/icons/mono/scalable/*/*.svgz

##########

%package -n trinity-kbstate
Summary:	A keyboard status applet for TDE
Group:		System/GUI/Other

%description -n trinity-kbstate
A panel applet that displays the keyboard status.

This package is part of Trinity, as a component of the TDE accessibility module.

%files -n trinity-kbstate
%defattr(-,root,root,-)
%{tde_tdelibdir}/kbstate_panelapplet.la
%{tde_tdelibdir}/kbstate_panelapplet.so
%{tde_datadir}/apps/kbstateapplet/
%{tde_datadir}/apps/kicker/applets/kbstateapplet.desktop

##########

%package -n trinity-kmag
Summary:	A screen magnifier for TDE
Group:		System/GUI/Other

%description -n trinity-kmag
TDE's screen magnifier tool.

You can use KMagnifier to magnify a part of the screen just as you would use 
a lens to magnify a newspaper fine-print or a photograph.  This application is
useful for a variety of people: from researchers to artists to web-designers to
people with low vision.

This package is part of Trinity, as a component of the TDE accessibility module.

%files -n trinity-kmag
%defattr(-,root,root,-)
%{tde_bindir}/kmag
%{tde_tdeappdir}/kmag.desktop
%{tde_datadir}/apps/kmag/
%{tde_datadir}/icons/hicolor/*/apps/kmag.png
%{tde_datadir}/icons/locolor/*/apps/kmag.png
%{tde_tdedocdir}/HTML/en/kmag/

%post -n trinity-kmag
/sbin/ldconfig ||:
for icon_theme in hicolor locolor ; do
  touch --no-create %{tde_datadir}/icons/${icon_theme} 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/${icon_theme} 2> /dev/null ||:
done

%postun -n trinity-kmag
/sbin/ldconfig ||:
for icon_theme in hicolor locolor ; do
  touch --no-create %{tde_datadir}/icons/${icon_theme} 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/${icon_theme} 2> /dev/null ||:
done

##########

%package -n trinity-kmousetool
Summary:	TDE mouse manipulation tool for the disabled
Group:		System/GUI/Other

%description -n trinity-kmousetool
KMouseTool clicks the mouse whenever the mouse cursor pauses briefly. It was
designed to help those with repetitive strain injuries, for whom pressing
buttons hurts.

This package is part of Trinity, as a component of the TDE accessibility module.

%files -n trinity-kmousetool
%defattr(-,root,root,-)
%{tde_bindir}/kmousetool
%{tde_tdeappdir}/kmousetool.desktop
%{tde_datadir}/apps/kmousetool/
%{tde_datadir}/icons/hicolor/*/apps/kmousetool.png
%{tde_tdedocdir}/HTML/en/kmousetool/

%post -n trinity-kmousetool
for icon_theme in hicolor ; do
  touch --no-create %{tde_datadir}/icons/${icon_theme} 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/${icon_theme} 2> /dev/null ||:
done

%postun -n trinity-kmousetool
for icon_theme in hicolor ; do
  touch --no-create %{tde_datadir}/icons/${icon_theme} 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/${icon_theme} 2> /dev/null ||:
done

##########

%package -n trinity-kmouth
Summary:	A type-and-say KDE frontend for speech synthesizers
Group:		System/GUI/Other

%description -n trinity-kmouth
KDE's type-and-say frontend for speech synthesizers.

It includes a history of spoken sentences from which the user can select
sentences to be re-spoken.

This package is part of Trinity, as a component of the TDE accessibility module.

%files -n trinity-kmouth
%defattr(-,root,root,-)
%{tde_confdir}/kmouthrc
%{tde_bindir}/kmouth
%{tde_tdeappdir}/kmouth.desktop
%{tde_datadir}/apps/kmouth/
%{tde_datadir}/icons/hicolor/*/actions/speak.png
%{tde_datadir}/icons/hicolor/*/actions/nospeak.png
%{tde_datadir}/icons/hicolor/*/apps/kmouth.png
%{tde_datadir}/icons/locolor/*/actions/speak.png
%{tde_datadir}/icons/locolor/*/apps/kmouth.png
%{tde_tdedocdir}/HTML/en/kmouth/

%post -n trinity-kmouth
for icon_theme in hicolor ; do
  touch --no-create %{tde_datadir}/icons/${icon_theme} 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/${icon_theme} 2> /dev/null ||:
done

%postun -n trinity-kmouth
for icon_theme in hicolor ; do
  touch --no-create %{tde_datadir}/icons/${icon_theme} 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/${icon_theme} 2> /dev/null ||:
done

##########

%package -n trinity-ksayit
Summary:	A frontend for the TDE Text-to-Speech system
Group:		System/GUI/Other

%description -n trinity-ksayit
Text-to-speech front-end to kttsd.

This package is part of Trinity, as a component of the TDE accessibility module.

%files -n trinity-ksayit
%defattr(-,root,root,-)
%{tde_bindir}/ksayit
%{tde_tdelibdir}/libFreeverb_plugin.la
%{tde_tdelibdir}/libFreeverb_plugin.so
%{tde_libdir}/libKTTSD_Lib.so.*
%{tde_tdeappdir}/ksayit.desktop
%{tde_datadir}/apps/ksayit/
%{tde_datadir}/icons/hicolor/*/apps/ksayit.png
%{tde_datadir}/icons/hicolor/32x32/apps/ksayit_clipempty.png
%{tde_datadir}/icons/hicolor/32x32/apps/ksayit_talking.png
%{tde_datadir}/services/ksayit_libFreeverb.desktop
%{tde_datadir}/servicetypes/ksayit_libFreeverb_service.desktop
%{tde_tdedocdir}/HTML/en/ksayit/

%post -n trinity-ksayit
/sbin/ldconfig ||:
for icon_theme in mono hicolor locolor ; do
  touch --no-create %{tde_datadir}/icons/${icon_theme} 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/${icon_theme} 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-ksayit
/sbin/ldconfig ||:
for icon_theme in mono hicolor locolor ; do
  touch --no-create %{tde_datadir}/icons/${icon_theme} 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/${icon_theme} 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-kttsd
Summary:	A Text-to-Speech system for TDE
Group:		System/GUI/Other

%description -n trinity-kttsd
The KDE Text-to-Speech system is a plugin based service that allows any KDE
(or non-KDE) application to speak using the DCOP interface.

ksayit and kmouth are useful front-ends for this capability, while one of
festival, flite, and epos are essential back-ends.

This package is part of Trinity, as a component of the TDE accessibility module.

Homepage: http://accessibility.kde.org/developer/kttsd

%files -n trinity-kttsd
%defattr(-,root,root,-)
%{tde_bindir}/kttsd
%{tde_bindir}/kttsmgr
%{tde_tdelibdir}/kcm_kttsd.la
%{tde_tdelibdir}/kcm_kttsd.so
%{tde_tdelibdir}/tdetexteditor_kttsd.la
%{tde_tdelibdir}/tdetexteditor_kttsd.so
%if 0%{?with_akode}
%{tde_tdelibdir}/libkttsd_akodeplugin.la
%{tde_tdelibdir}/libkttsd_akodeplugin.so
%endif
%{tde_tdelibdir}/libkttsd_alsaplugin.la
%{tde_tdelibdir}/libkttsd_alsaplugin.so
%{tde_tdelibdir}/libkttsd_artsplugin.la
%{tde_tdelibdir}/libkttsd_artsplugin.so
%{tde_tdelibdir}/libkttsd_commandplugin.la
%{tde_tdelibdir}/libkttsd_commandplugin.so
%{tde_tdelibdir}/libkttsd_eposplugin.la
%{tde_tdelibdir}/libkttsd_eposplugin.so
%{tde_tdelibdir}/libkttsd_festivalintplugin.la
%{tde_tdelibdir}/libkttsd_festivalintplugin.so
%{tde_tdelibdir}/libkttsd_fliteplugin.la
%{tde_tdelibdir}/libkttsd_fliteplugin.so
%{tde_tdelibdir}/libkttsd_sbdplugin.la
%{tde_tdelibdir}/libkttsd_sbdplugin.so
%{tde_tdelibdir}/libkttsd_stringreplacerplugin.la
%{tde_tdelibdir}/libkttsd_stringreplacerplugin.so
%{tde_tdelibdir}/libkttsd_talkerchooserplugin.la
%{tde_tdelibdir}/libkttsd_talkerchooserplugin.so
%{tde_tdelibdir}/libkttsd_xmltransformerplugin.la
%{tde_tdelibdir}/libkttsd_xmltransformerplugin.so
%{tde_tdelibdir}/libkttsjobmgrpart.la
%{tde_tdelibdir}/libkttsjobmgrpart.so
%{tde_libdir}/libkttsd.so.*
%{tde_tdeappdir}/kcmkttsd.desktop
%{tde_tdeappdir}/kttsmgr.desktop
%{tde_datadir}/apps/tdetexteditor_kttsd/
%exclude %{tde_datadir}/apps/kttsd/hadifix/xslt/SSMLtoTxt2pho.xsl
%{tde_datadir}/apps/kttsd/
%{tde_datadir}/icons/hicolor/16x16/actions/female.png
%{tde_datadir}/icons/hicolor/16x16/actions/male.png
%{tde_datadir}/icons/hicolor/*/apps/kttsd.png
%{tde_datadir}/icons/hicolor/*/apps/kcmkttsd.png
%{tde_datadir}/services/tdetexteditor_kttsd.desktop
%{tde_datadir}/services/kttsd.desktop
%if 0%{?with_akode}
%{tde_datadir}/services/kttsd_akodeplugin.desktop
%endif
%{tde_datadir}/services/kttsd_alsaplugin.desktop
%{tde_datadir}/services/kttsd_artsplugin.desktop
%{tde_datadir}/services/kttsd_commandplugin.desktop
%{tde_datadir}/services/kttsd_eposplugin.desktop
%{tde_datadir}/services/kttsd_festivalintplugin.desktop
%{tde_datadir}/services/kttsd_fliteplugin.desktop
%{tde_datadir}/services/kttsd_sbdplugin.desktop
%{tde_datadir}/services/kttsd_stringreplacerplugin.desktop
%{tde_datadir}/services/kttsd_talkerchooserplugin.desktop
%{tde_datadir}/services/kttsd_xmltransformerplugin.desktop
%{tde_datadir}/services/kttsjobmgr.desktop
%{tde_datadir}/servicetypes/kttsd_audioplugin.desktop
%{tde_datadir}/servicetypes/kttsd_filterplugin.desktop
%{tde_datadir}/servicetypes/kttsd_synthplugin.desktop
%{tde_tdedocdir}/HTML/en/kttsd/

%post -n trinity-kttsd
/sbin/ldconfig ||:
for icon_theme in crystalsvg hicolor locolor ; do
  touch --no-create %{tde_datadir}/icons/${icon_theme} 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/${icon_theme} 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-kttsd
/sbin/ldconfig ||:
for icon_theme in crystalsvg hicolor locolor ; do
  touch --no-create %{tde_datadir}/icons/${icon_theme} 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/${icon_theme} 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-kttsd-contrib-plugins
Summary:	The TDE Text-to-Speech system
Group:		System/GUI/Other
Requires:	trinity-kttsd = %{version}-%{release}

%description -n trinity-kttsd-contrib-plugins
kttsd synthetizer plugins that depends on non-free software :
* FreeTTS plugin.
* Hadifix (mbrola/txt2pho) plugin.
Those plugins will require manual installation of third party,
non free software to work.

This package is part of Trinity, as a component of the TDE accessibility module.

%files -n trinity-kttsd-contrib-plugins
%defattr(-,root,root,-)
%{tde_tdelibdir}/libkttsd_freettsplugin.la
%{tde_tdelibdir}/libkttsd_freettsplugin.so
%{tde_tdelibdir}/libkttsd_hadifixplugin.la
%{tde_tdelibdir}/libkttsd_hadifixplugin.so
%{tde_datadir}/apps/kttsd/hadifix/xslt/SSMLtoTxt2pho.xsl
%{tde_datadir}/services/kttsd_freettsplugin.desktop
%{tde_datadir}/services/kttsd_hadifixplugin.desktop

##########

%package devel
Summary:	Development files for tdeaccessibility
Group:		Development/Libraries/X11
Requires:	%{name} = %{version}-%{release}
Requires:	trinity-tdelibs-devel >= %{version}
Requires:	libjpeg-devel
Requires:	libpng-devel

Obsoletes:		trinity-kdeaccessibility-devel < %{version}-%{release}
Provides:		trinity-kdeaccessibility-devel = %{version}-%{release}

%description devel
This package contains the development file for TDE accessibility 
programs.

%files devel
%defattr(-,root,root,-)
%{tde_libdir}/libkttsd.la
%{tde_libdir}/libkttsd.so
%{tde_libdir}/libKTTSD_Lib.la
%{tde_libdir}/libKTTSD_Lib.so
%{tde_tdeincludedir}/ksayit_fxplugin.h

%post devel
/sbin/ldconfig ||:

%postun devel
/sbin/ldconfig ||:

##########

%prep
%setup -q -n %{name}-%{version}%{?preversion:~%{preversion}}
%patch1 -p1

# Update icons for some control center modules
%__sed -i "kttsd/kcmkttsmgr/kcmkttsd.desktop" -e "s|^Icon=.*|Icon=kcmkttsd|"

%__cp -f "/usr/share/aclocal/libtool.m4" "admin/libtool.m4.in"
%__cp -f "/usr/share/libtool/config/ltmain.sh" "admin/ltmain.sh" || %__cp -f "/usr/share/libtool/ltmain.sh" "admin/ltmain.sh"
%__make -f "admin/Makefile.common"


%build
unset QTDIR QTINC QTLIB
export PATH="%{tde_bindir}:${PATH}"
export PKG_CONFIG_PATH="%{tde_libdir}/pkgconfig"
export kde_confdir="%{tde_confdir}"

%configure \
  --prefix=%{tde_prefix} \
  --exec-prefix=%{tde_prefix} \
  --bindir=%{tde_bindir} \
  --libdir=%{tde_libdir} \
  --datadir=%{tde_datadir} \
  --includedir=%{tde_tdeincludedir} \
  \
  --disable-dependency-tracking \
  --disable-debug \
  --enable-new-ldflags \
  --enable-final \
  --enable-closure \
  --enable-rpath \
  --disable-gcc-hidden-visibility \
  \
  --enable-ksayit-audio-plugins \
  %{?with_akode:--with-akode} %{?!with_akode:--without-akode}
  
%__make %{?_smp_mflags}


%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf %{buildroot}
%__make install DESTDIR=%{buildroot}

# Move desktop files to correct XDG location
%__mv -f "%{?buildroot}%{tde_datadir}/applnk/Applications/kmag.desktop" "%{?buildroot}%{tde_tdeappdir}"
%__mv -f "%{?buildroot}%{tde_datadir}/applnk/Applications/kmousetool.desktop" "%{?buildroot}%{tde_tdeappdir}"
%__mv -f "%{?buildroot}%{tde_datadir}/applnk/Applications/kmouth.desktop" "%{?buildroot}%{tde_tdeappdir}"

# Adds missing icons in 'hicolor' theme
# These icons are copied from 'crystalsvg' theme, provided by 'tdelibs'.
%__mkdir_p "%{?buildroot}%{tde_datadir}/icons/hicolor/"{16x16,22x22,32x32,48x48,64x64,128x128}"/apps/"
pushd "%{?buildroot}%{tde_datadir}/icons"
for i in {16,22,32,48,64,128}; do %__cp %{tde_datadir}/icons/crystalsvg/"$i"x"$i"/apps/kttsd.png  hicolor/"$i"x"$i"/apps/kttsd.png    ;done
for i in {16,22,32,48,64,128}; do %__cp %{tde_datadir}/icons/crystalsvg/"$i"x"$i"/apps/kttsd.png  hicolor/"$i"x"$i"/apps/kcmkttsd.png ;done
popd

# Avoid conflict with tdelibs
%__rm -f %{?buildroot}%{tde_datadir}/icons/crystalsvg/*/apps/kttsd.png
%__rm -f %{?buildroot}%{tde_datadir}/icons/crystalsvg/scalable/apps/kttsd.svgz


# Links duplicate files
%fdupes "%{?buildroot}%{tde_datadir}"


%clean
%__rm -rf %{buildroot}


%changelog
* Sat Nov 14 2015 Liu Di <liudidi@gmail.com> - 14.0.1-1.opt.2
- 为 Magic 3.0 重建

* Thu Nov 05 2015 Liu Di <liudidi@gmail.com> - 14.0.1-1.opt.1
- 为 Magic 3.0 重建

* Fri Jul 05 2013 Francois Andriot <francois.andriot@free.fr> - 14.0.0-1
- Initial release for TDE R14.0.0
