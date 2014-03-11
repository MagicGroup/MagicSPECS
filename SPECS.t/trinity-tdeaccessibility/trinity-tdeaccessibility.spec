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


Summary:	Trinity Desktop Environment - Accessibility
Name:		trinity-tdeaccessibility
Version:	3.5.13.2
Release:	1%{?dist}%{?_variant}

License:	GPLv2
Group:		User Interface/Desktops

Vendor:		Trinity Project
Packager:	Francois Andriot <francois.andriot@free.fr>
URL:		http://www.trinitydesktop.org/

Source0:	kdeaccessibility-trinity-%{version}.tar.xz

Prefix:		%{tde_prefix}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	autoconf automake libtool m4
BuildRequires:	desktop-file-utils
BuildRequires:	trinity-akode-devel
BuildRequires:	trinity-arts-devel >= %{version}
BuildRequires:	trinity-tdelibs-devel >= %{version}
BuildRequires:	trinity-tdemultimedia-devel >= %{version}

BuildRequires:	alsa-lib-devel

%if 0%{?fedora} > 4 || 0%{?rhel} > 4
BuildRequires: libXtst-devel
%endif

%if 0%{?mgaversion} || 0%{?mdkversion}
BuildRequires:	%{_lib}xi-devel
BuildRequires:	%{_lib}xext%{?mgaversion:6}-devel
BuildRequires:	%{_lib}x11%{?mgaversion:_6}-devel
BuildRequires:	%{_lib}xcb-devel
BuildRequires:	%{_lib}xau%{?mgaversion:6}-devel
%else
BuildRequires:	libXi-devel
BuildRequires:	libXext-devel
BuildRequires:	libX11-devel
%if 0%{?rhel} >= 6 || 0%{?fedora}
BuildRequires:	libxcb-devel
%endif
BuildRequires:	libXau-devel
%endif

# Mageia only: Special packages were built for missing '.la' files on Mageia 2 !!!
%if 0%{?mgaversion}
BuildRequires:	%{_lib}xi-devel-libtool
BuildRequires:	%{_lib}xext6-devel-libtool
BuildRequires:	%{_lib}x11_6-devel-libtool
BuildRequires:	%{_lib}xcb-devel-libtool
BuildRequires:	%{_lib}xau6-devel-libtool
%endif

Obsoletes:		trinity-kdeaccessibility < %{version}-%{release}
Provides:		trinity-kdeaccessibility = %{version}-%{release}
Obsoletes:		trinity-kdeaccessibility-libs < %{version}-%{release}
Provides:		trinity-kdeaccessibility-libs = %{version}-%{release}

Requires: trinity-kde-icons-mono = %{version}-%{release}
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

%package -n trinity-kde-icons-mono
Summary:	A monochromatic icons theme for TDE
Group:		User Interface/Desktops

%description -n trinity-kde-icons-mono
A monochromatic icon theme for TDE, designed for accessibility purposes.

This package is part of Trinity, as a component of the TDE accessibility module.

%files -n trinity-kde-icons-mono
%defattr(-,root,root,-)
%{tde_datadir}/icons/mono/index.theme
%{tde_datadir}/icons/mono/scalable/*/*.svgz

##########

%package -n trinity-kbstate
Summary:	a keyboard status applet for TDE
Group:		User Interface/Desktops

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
Group:		User Interface/Desktops

%description -n trinity-kmag
KDE's screen magnifier tool.

You can use KMagnifier to magnify a part of the screen just as you would use 
a lens to magnify a newspaper fine-print or a photograph.  This application is
useful for a variety of people: from researchers to artists to web-designers to
people with low vision.

This package is part of Trinity, as a component of the TDE accessibility module.

%files -n trinity-kmag
%defattr(-,root,root,-)
%{tde_bindir}/kmag
%{tde_datadir}/applnk/Applications/kmag.desktop
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
Group:		User Interface/Desktops

%description -n trinity-kmousetool
KMouseTool clicks the mouse whenever the mouse cursor pauses briefly. It was
designed to help those with repetitive strain injuries, for whom pressing
buttons hurts.

This package is part of Trinity, as a component of the TDE accessibility module.

%files -n trinity-kmousetool
%defattr(-,root,root,-)
%{tde_bindir}/kmousetool
%{tde_datadir}/applnk/Applications/kmousetool.desktop
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
Group:		User Interface/Desktops

%description -n trinity-kmouth
KDE's type-and-say frontend for speech synthesizers.

It includes a history of spoken sentences from which the user can select
sentences to be re-spoken.

This package is part of Trinity, as a component of the TDE accessibility module.

%files -n trinity-kmouth
%defattr(-,root,root,-)
%{tde_datadir}/config/kmouthrc
%{tde_bindir}/kmouth
%{tde_datadir}/applnk/Applications/kmouth.desktop
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
Group:		User Interface/Desktops

%description -n trinity-ksayit
Text-to-speech front-end to kttsd.

This package is part of Trinity, as a component of the TDE accessibility module.

%files -n trinity-ksayit
%defattr(-,root,root,-)
%{tde_bindir}/ksayit
%{tde_tdeincludedir}/ksayit_fxplugin.h
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
Group:		User Interface/Desktops

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
%{tde_tdelibdir}/ktexteditor_kttsd.la
%{tde_tdelibdir}/ktexteditor_kttsd.so
%{tde_tdelibdir}/libkttsd_akodeplugin.la
%{tde_tdelibdir}/libkttsd_akodeplugin.so
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
%{tde_datadir}/apps/ktexteditor_kttsd/ktexteditor_kttsdui.rc
%exclude %{tde_datadir}/apps/kttsd/hadifix/xslt/SSMLtoTxt2pho.xsl
%{tde_datadir}/apps/kttsd/
%{tde_datadir}/icons/hicolor/16x16/actions/female.png
%{tde_datadir}/icons/hicolor/16x16/actions/male.png
%{tde_datadir}/services/ktexteditor_kttsd.desktop
%{tde_datadir}/services/kttsd.desktop
%{tde_datadir}/services/kttsd_akodeplugin.desktop
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
%{tde_datadir}/icons/crystalsvg/*/apps/kttsd.png
%{tde_datadir}/icons/crystalsvg/*/apps/kttsd.svgz
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
Summary:	the TDE Text-to-Speech system
Group:		User Interface/Desktops
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
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	trinity-tdelibs-devel >= %{version}

Obsoletes:		trinity-kdeaccessibility-devel < %{version}-%{release}
Provides:		trinity-kdeaccessibility-devel = %{version}-%{release}

%description devel
%{summary}.

%files devel
%defattr(-,root,root,-)
%{tde_libdir}/libkttsd.la
%{tde_libdir}/libkttsd.so
%{tde_libdir}/libKTTSD_Lib.la
%{tde_libdir}/libKTTSD_Lib.so

%post devel
/sbin/ldconfig ||:

%postun devel
/sbin/ldconfig ||:

##########

%if 0%{?suse_version}
%debug_package
%endif

##########

%prep
%setup -q -n kdeaccessibility-trinity-%{version}

# Ugly hack to modify TQT include directory inside autoconf files.
# If TQT detection fails, it fallbacks to TQT4 instead of TQT3 !
%__sed -i admin/acinclude.m4.in \
  -e "s|/usr/include/tqt|%{tde_includedir}/tqt|g" \
  -e "s|kde_htmldir='.*'|kde_htmldir='%{tde_tdedocdir}/HTML'|g"

%__cp -f "/usr/share/aclocal/libtool.m4" "admin/libtool.m4.in"
%__cp -f "/usr/share/libtool/config/ltmain.sh" "admin/ltmain.sh" || %__cp -f "/usr/share/libtool/ltmain.sh" "admin/ltmain.sh"
%__make -f "admin/Makefile.common"


%build
unset QTDIR || : ; . /etc/profile.d/qt3.sh
export PATH="%{tde_bindir}:${PATH}"
export LDFLAGS="-L%{tde_libdir} -I%{tde_includedir}"

# Avoir conflict with KDE4, if installed
# see file: '/etc/profile.d/kde.sh' from package 'kde-settings'
export KDEDIRS=%{tde_prefix}
export KDEDIR=%{tde_prefix}

%configure \
  --prefix=%{tde_prefix} \
  --exec-prefix=%{tde_prefix} \
  --bindir=%{tde_bindir} \
  --libdir=%{tde_libdir} \
  --datadir=%{tde_datadir} \
  --includedir=%{tde_tdeincludedir} \
  --disable-rpath \
  --enable-new-ldflags \
  --enable-closure \
  --disable-debug --disable-warnings \
  --enable-final \
  --enable-ksayit-audio-plugins \
  --with-akode \
  --with-extra-includes=%{tde_includedir}:%{tde_includedir}/tqt

%__make %{?_smp_mflags}


%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf %{buildroot}
%__make install DESTDIR=%{buildroot}

# file lists for locale
HTML_DIR=$(kde-config --expandvars --install html)
if [ -d %{buildroot}/$HTML_DIR ]; then
  for lang_dir in %{buildroot}/$HTML_DIR/* ; do
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


%clean
%__rm -rf %{buildroot}



%changelog
* Sun Sep 30 2012 Francois Andriot <francois.andriot@free.fr> - 3.5.13.1-1
- Initial build for TDE 3.5.13.1
