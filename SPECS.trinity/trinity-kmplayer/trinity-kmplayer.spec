# Default version for this component
%define kdecomp kmplayer
%define tdeversion 3.5.13.2

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
%define tde_mandir %{tde_datadir}/man
%define tde_appdir %{tde_datadir}/applications

%define tde_tdeappdir %{tde_appdir}/kde
%define tde_tdedocdir %{tde_docdir}/tde
%define tde_tdeincludedir %{tde_includedir}/tde
%define tde_tdelibdir %{tde_libdir}/trinity

%define _docdir %{tde_docdir}


Name:		trinity-%{kdecomp}
Summary:	media player for Trinity
Version:	0.10.0c
Release:	5%{?dist}%{?_variant}

License:	GPLv2+
Group:		Applications/Multimedia

Vendor:		Trinity Project
Packager:	Francois Andriot <francois.andriot@free.fr>
URL:		http://kmplayer.kde.org

Prefix:		%{tde_prefix}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:	%{kdecomp}-trinity-%{tdeversion}.tar.xz

# [kmplayer] Fix xine 1.2 support
Patch1:		kmplayer-3.5.13.1-fix_xine12_support.patch


BuildRequires:	trinity-tqtinterface-devel >= 3.5.13.1
BuildRequires:	trinity-dbus-tqt-devel >= 3.5.13.1
BuildRequires:	trinity-tdelibs-devel >= 3.5.13.1
BuildRequires:	trinity-tdebase-devel >= 3.5.13.1
BuildRequires:	desktop-file-utils


%if 0%{?mgaversion} || 0%{?mdkversion}
BuildRequires:	%{_lib}gstreamer0.10-devel
BuildRequires:	%{_lib}gstreamer-plugins-base0.10-devel
BuildRequires:	libxv-devel
%endif
%if 0%{?rhel} || 0%{?fedora}
BuildRequires:	gstreamer-devel
BuildRequires:	gstreamer-plugins-base-devel
BuildRequires:	libXv-devel
%endif
%if 0%{?suse_version}
BuildRequires:	gstreamer-devel
BuildRequires:	gstreamer-0_10-plugins-base-devel
BuildRequires:	libXv-devel
%endif

Requires:	%{name}-base

%description
A basic audio/video viewer application for Trinity.

KMPlayer can:
* play DVD (DVDNav only with the Xine player)
* play VCD
* let the backend players play from a pipe (read from stdin)
* play from a TV device (experimental)
* show backend player's console output
* launch ffserver (only 0.4.8 works) when viewing from a v4l device
* DCOP KMediaPlayer interface support
* VDR viewer frontend (with *kxvplayer), configure VDR keys with standard KDE
  shortcut configure window
* Lots of configurable shortcuts. Highly recommended for the VDR keys
  (if you have VDR) and volume increase/decrease


%package base
Group:			Applications/Multimedia
Summary:		Base files for KMPlayer [Trinity]

%description base
Core files needed for KMPlayer.


%package konq-plugins
Group:			Applications/Multimedia
Requires:		trinity-kmplayer-base, trinity-kdebase
Summary:		KMPlayer plugin for KHTML/Konqueror [Trinity]

%description konq-plugins
This plugin enables audio/video playback inside konqueror, using Xine (with
*kxineplayer) or GStreamer (with *kgstplayer), such as movie trailers, web
tv or radio. It mimics QuickTime, MS Media Player and RealPlayer plugin
browser plugins.


%package doc
Group:			Applications/Multimedia
Requires:		%{name} = %{version}-%{release}
Summary:		Handbook for KMPlayer [Trinity]

%description doc
Documention for KMPlayer, a basic audio/video viewer application for KDE.


%if 0%{?suse_version}
%debug_package
%endif


%prep
%setup -q -n %{kdecomp}-trinity-%{tdeversion}
#%patch1 -p1

# Ugly hack to modify TQT include directory inside autoconf files.
# If TQT detection fails, it fallbacks to TQT4 instead of TQT3 !
%__sed -i admin/acinclude.m4.in \
  -e "s|/usr/include/tqt|%{tde_includedir}/tqt|g" \
  -e "s|kde_htmldir='.*'|kde_htmldir='%{tde_tdedocdir}/HTML'|g"

%__cp "/usr/share/aclocal/libtool.m4" "admin/libtool.m4.in"
%__cp "/usr/share/libtool/config/ltmain.sh" "admin/ltmain.sh" || %__cp "/usr/share/libtool/ltmain.sh" "admin/ltmain.sh"
%__make -f "admin/Makefile.common"



%build
unset QTDIR; . /etc/profile.d/qt3.sh
export PATH="%{tde_bindir}:${PATH}"
export LDFLAGS="-L%{tde_libdir} -I%{tde_includedir}"

export CXXFLAGS="${CXXFLAGS} -fpermissive"

%configure \
  --prefix=%{tde_prefix} \
  --exec-prefix=%{tde_prefix} \
  --bindir=%{tde_bindir} \
  --datadir=%{tde_datadir} \
  --includedir=%{tde_tdeincludedir} \
  --libdir=%{tde_libdir} \
  --mandir=%{tde_mandir} \
  --disable-rpath \
  --with-extra-includes=%{tde_includedir}/tqt:%{tde_includedir}/dbus-1.0 \
  --enable-closure


%__make %{?_smp_mflags}


%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf %{buildroot}
%__make install DESTDIR=%{buildroot}

%find_lang %{kdecomp}

# Removes unwanted files
%__rm -f %{?buildroot}%{tde_datadir}/mimelnk/application/x-mplayer2.desktop


%clean
%__rm -rf %{buildroot}


%post
/sbin/ldconfig || :

%postun
/sbin/ldconfig || :

%post base
touch --no-create %{tde_datadir}/icons/hicolor || :
gtk-update-icon-cache --quiet %{tde_datadir}/icons/hicolor || :
/sbin/ldconfig || :

%postun base
touch --no-create %{tde_datadir}/icons/hicolor || :
gtk-update-icon-cache --quiet %{tde_datadir}/icons/hicolor || :
/sbin/ldconfig || :


%files -f %{kdecomp}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog INSTALL README TODO kmplayer.lsm
%{tde_bindir}/kmplayer
#%{tde_bindir}/knpplayer
%{tde_bindir}/kxvplayer
%{tde_libdir}/libkdeinit_kmplayer.la
%{tde_libdir}/libkdeinit_kmplayer.so
%{tde_tdelibdir}/kmplayer.la
%{tde_tdelibdir}/kmplayer.so
%{tde_tdeappdir}/kmplayer.desktop
%{tde_datadir}/apps/kmplayer
%{tde_datadir}/services/kmplayer_part.desktop

%files base
%defattr(-,root,root,-)
%{tde_libdir}/libkmplayercommon.la
%{tde_libdir}/libkmplayercommon.so
%{tde_bindir}/kgstplayer
%{tde_bindir}/kxineplayer
%{tde_datadir}/config/kmplayerrc
%{tde_datadir}/apps/kmplayer/bookmarks.xml
%{tde_datadir}/apps/kmplayer/noise.gif
%{tde_datadir}/apps/kmplayer/pluginsinfo
%{tde_datadir}/icons/hicolor/*/apps/kmplayer.png
%{tde_datadir}/icons/hicolor/*/apps/kmplayer.svgz
%{tde_datadir}/mimelnk/application/x-kmplayer.desktop
%{tde_datadir}/mimelnk/video/x-ms-wmp.desktop


%files doc
%defattr(-,root,root,-)
%{tde_tdedocdir}/HTML/*/kmplayer

%files konq-plugins
%defattr(-,root,root,-)
%{tde_tdelibdir}/libkmplayerpart.la
%{tde_tdelibdir}/libkmplayerpart.so
%{tde_datadir}/apps/kmplayer/kmplayerpartui.rc
%{tde_datadir}/apps/kmplayer/pluginsinfo
%{tde_datadir}/services/kmplayer_part.desktop


%changelog
* Fri Aug 02 2013 Liu Di <liudidi@gmail.com> - 0.10.0c-5.opt
- 为 Magic 3.0 重建

* Fri Aug 02 2013 Liu Di <liudidi@gmail.com> - 0.10.0c-4.opt
- 为 Magic 3.0 重建

* Wed Oct 03 2012 Francois Andriot <francois.andriot@free.fr> - 0.10.0c-3
- Initial build for TDE 3.5.13.1

* Wed May 02 2012 Francois Andriot <francois.andriot@free.fr> - 0.10.0c-2
- Fix compilation with GCC 4.7 [Commit #5106117b]

* Sat Dec 03 2011 Francois Andriot <francois.andriot@free.fr> - 0.10.0c-1
- Initial build for RHEL 5, RHEL 6, Fedora 15, Fedora 16

