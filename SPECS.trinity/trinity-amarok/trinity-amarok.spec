#
# spec file for package amarok (version R14)
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

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.0.1
%endif
%define tde_pkg amarok
%define tde_prefix /opt/trinity
%define tde_bindir %{tde_prefix}/bin
%define tde_confdir %{_sysconfdir}/trinity
%define tde_datadir %{tde_prefix}/share
%define tde_docdir %{tde_datadir}/doc
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}
%define tde_mandir %{tde_datadir}/man
%define tde_tdeappdir %{tde_datadir}/applications/tde
%define tde_tdedocdir %{tde_docdir}/tde
%define tde_tdeincludedir %{tde_includedir}/tde
%define tde_tdelibdir %{tde_libdir}/trinity


Name:		trinity-%{tde_pkg}
Epoch:		%{tde_epoch}
Version:	1.4.10
Release:	%{?!preversion:2}%{?preversion:0_%{preversion}}%{?dist}%{?_variant}.1
Summary:	Media player for TDE
Summary(zh_CN.UTF-8): TDE 下的媒体播放器
Group:		Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
URL:		http://www.trinitydesktop.org/
#Url:		http://amarok.kde.org

License:	GPLv2+

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:		%{tde_prefix}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:		%{name}-%{tde_version}%{?preversion:~%{preversion}}.tar.gz

BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	trinity-konqueror-devel >= %{tde_version}

BuildRequires:	trinity-filesystem >= %{tde_version}
Requires:		trinity-filesystem >= %{tde_version}

BuildRequires:	desktop-file-utils
BuildRequires:	cmake >= 2.8
BuildRequires:	gcc-c++
BuildRequires:	pkgconfig
BuildRequires:	gettext

# ACL support
BuildRequires:	libacl-devel

# ALSA support
BuildRequires:	alsa-lib-devel

# ESOUND support
BuildRequires:	esound-devel

# PCRE support
BuildRequires:	pcre-devel

# LIBTOOL
BuildRequires:	libtool
BuildRequires:	libtool-ltdl-devel

BuildRequires:	libusb-devel
BuildRequires:	mysql-devel
BuildRequires:	postgresql-devel
BuildRequires:	SDL-devel
BuildRequires:	taglib-devel
BuildRequires:	sqlite-devel

# not used anymore, in favor of libvisual ? -- Rex
#{?fedora:BuildRequires:  xmms-devel}

# IDN support
BuildRequires:	libidn-devel

# GAMIN support
#  Not on openSUSE.
%define with_gamin 1
BuildRequires:	gamin-devel

# DBUS support
BuildRequires:	dbus-devel

# DBUS-(T)QT support
BuildRequires:	trinity-dbus-tqt-devel >= 1:0.63

# IFP support
#  IFP package is broken under PCLinuxOS.
%define with_ifp 1
BuildRequires:	libifp-devel

# KARMA support

# GPOD (ipod) support
%define with_gpod 1
BuildRequires:	libgpod-devel >= 0.4.2

# MTP players
%define with_mtp 1
BuildRequires:	libmtp-devel
BuildRequires:	libmusicbrainz-devel

# Creative Nomad Jukebox
%define with_njb 1
BuildRequires:	libnjb-devel

# VISUAL support
%define with_libvisual 1
BuildRequires:	libvisual-devel

# TUNEPIMP support
BuildRequires:	libtunepimp-devel

# INOTIFY support
%define with_inotify 1

# XINE support
%define with_xine 1
BuildRequires: xine-lib-devel

# YAUAP support
%define with_yauap 1

# AKODE support
%define with_akode 0
%if 0 && 0%{?with_akode}
BuildRequires:	trinity-akode-devel
%endif

# MP4V2 support
%define with_mp4v2 1
BuildRequires:	mpeg4ip-devel

# ruby
BuildRequires:	ruby
BuildRequires:	ruby-devel
BuildRequires:	rubypick

# To open the selected browser, works with Patch2
Requires:		xdg-utils
Requires(post): xdg-utils
Requires(postun): xdg-utils


%description
Amarok is a multimedia player with:
 - fresh playlist concept, very fast to use, with drag and drop
 - plays all formats supported by the various engines
 - audio effects, like reverb and compressor
 - compatible with the .m3u and .pls formats for playlists
 - nice GUI, integrates into the TDE look, but with a unique touch

%description -l zh_CN.UTF-8
这是一个媒体播放器。

%files -f %{tde_pkg}.lang
%defattr(-,root,root,-)
%doc COPYING AUTHORS ChangeLog README
%{tde_bindir}/amarok
%{tde_bindir}/amarokapp
%{tde_bindir}/amarokcollectionscanner
%{tde_bindir}/amarok_proxy.rb
%{tde_datadir}/apps/amarok/
%{tde_datadir}/icons/crystalsvg/*/actions/covermanager.png
%{tde_datadir}/icons/crystalsvg/*/actions/dynamic.png
%{tde_datadir}/icons/crystalsvg/*/actions/equalizer.png
%{tde_datadir}/icons/crystalsvg/*/actions/mini_dock.png
%{tde_datadir}/icons/crystalsvg/*/actions/player_playlist_2.png
%{tde_datadir}/icons/crystalsvg/*/actions/podcast.png
%{tde_datadir}/icons/crystalsvg/*/actions/podcast_new.png
%{tde_datadir}/icons/crystalsvg/*/actions/random.png
%{tde_datadir}/icons/crystalsvg/*/actions/repeat_playlist.png
%{tde_datadir}/icons/crystalsvg/*/actions/repeat_track.png
%{tde_datadir}/icons/crystalsvg/*/actions/visualizations.png
%{tde_datadir}/icons/crystalsvg/*/actions/wiki.png
%{tde_datadir}/icons/crystalsvg/*/actions/amarok_podcast.png
%{tde_datadir}/icons/crystalsvg/*/actions/amarok_podcast_new.png
%{tde_datadir}/icons/crystalsvg/*/actions/amazon_locale.png
%{tde_datadir}/icons/hicolor/*/*/*
%{tde_tdeappdir}/*.desktop
%{tde_datadir}/servicetypes/*.desktop
%{tde_datadir}/apps/profiles/amarok.profile.xml
%{tde_confdir}/amarokrc
%{tde_datadir}/config.kcfg/*.kcfg
%{tde_datadir}/services/amarokitpc.protocol
%{tde_datadir}/services/amaroklastfm.protocol
%{tde_datadir}/services/amarokpcast.protocol
# -libs ?  -- Rex
%{tde_libdir}/libamarok.so.0
%{tde_libdir}/libamarok.so.0.0.0
# DAAP
%{tde_bindir}/amarok_daapserver.rb
%{tde_tdelibdir}/libamarok_daap-mediadevice.*
%{tde_datadir}/services/amarok_daap-mediadevice.desktop
# Mass-storage
%{tde_datadir}/services/amarok_massstorage-device.desktop
%{tde_tdelibdir}/libamarok_massstorage-device.*
# NFS
%{tde_datadir}/services/amarok_nfs-device.desktop
%{tde_tdelibdir}/libamarok_nfs-device.*
# SMB
%{tde_datadir}/services/amarok_smb-device.desktop
%{tde_tdelibdir}/libamarok_smb-device.*
# IPod
%if 0%{?with_gpod}
%{tde_datadir}/services/amarok_ipod-mediadevice.desktop
%{tde_tdelibdir}/libamarok_ipod-mediadevice.*
%endif
# VFAT
%{tde_datadir}/services/amarok_generic-mediadevice.desktop
%{tde_tdelibdir}/libamarok_generic-mediadevice.*
# iRiver
%if 0%{?with_ifp}
%{tde_datadir}/services/amarok_ifp-mediadevice.desktop
%{tde_tdelibdir}/libamarok_ifp-mediadevice.*
%endif
# Creative Zen
%if 0%{?with_njb}
%{tde_datadir}/services/amarok_njb-mediadevice.desktop
%{tde_tdelibdir}/libamarok_njb-mediadevice.*
%endif
# MTP players
%if 0%{?with_mtp}
%{tde_datadir}/services/amarok_mtp-mediadevice.desktop
%{tde_tdelibdir}/libamarok_mtp-mediadevice.*
%endif
# Rio Karma
%if 0%{?with_karma}
%{tde_datadir}/services/amarok_riokarma-mediadevice.desktop
%{tde_tdelibdir}/libamarok_riokarma-mediadevice.*
%endif
# Void engine (noop)
%{tde_datadir}/services/amarok_void-engine_plugin.desktop
%{tde_tdelibdir}/libamarok_void-engine_plugin.*
# Xine engine
%if 0%{?with_xine}
%{tde_datadir}/services/amarok_xine-engine.desktop
%{tde_tdelibdir}/libamarok_xine-engine.*
%endif
## Gstreamer engine
#%{tde_datadir}/services/amarok_gst10engine_plugin.desktop
#%{tde_tdelibdir}/libamarok_gst10engine_plugin.*
# YAUAP
%if 0%{?with_yauap}
%{tde_datadir}/services/amarok_yauap-engine_plugin.desktop
%{tde_tdelibdir}/libamarok_yauap-engine_plugin.*
%endif
# AKODE
%if 0 && 0%{?with_akode}
%{tde_datadir}/services/amarok_aKode-engine.desktop
%{tde_tdelibdir}/libamarok_aKode-engine.*
%endif

%post
/sbin/ldconfig
xdg-icon-resource forceupdate --theme hicolor 2> /dev/null || :
xdg-desktop-menu forceupdate 2> /dev/null || :

%postun
/sbin/ldconfig
xdg-icon-resource forceupdate --theme hicolor 2> /dev/null || :
xdg-desktop-menu forceupdate 2> /dev/null || :


##########

%package ruby
Summary:		%{name} Ruby support
Group:			Applications/Multimedia
Requires:		%{name} = %{?epoch:%{epoch}:}%{version}-%{release}
# For dir ownership and some default plugins (lyrics)
Requires:		ruby

%description ruby
%{summary}.

%files ruby
%defattr(-,root,root,-)
%{tde_libdir}/ruby_lib/

##########

%package konqueror
Summary:		Amarok konqueror (service menus, sidebar) support
Group:			Applications/Multimedia

Requires:		%{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:		trinity-konqueror

%description konqueror
%{summary}.

%files konqueror
%defattr(-,root,root,-)
%{tde_datadir}/apps/konqueror/servicemenus/*.desktop
%{tde_tdelibdir}/konqsidebar_universalamarok.*
%{tde_datadir}/apps/konqsidebartng/*/amarok.desktop


##########

%if 0%{?with_libvisual}

%package visualisation
Summary:		Visualisation plugins for Amarok
Group:			Applications/Multimedia
Requires:		%{name} = %{?epoch:%{epoch}:}%{version}-%{release}
# No plugins by default, we need libvisual-plugins
#Requires:   libvisual-plugins

%description visualisation
Amarok can use visualisation plugins from different origins.
Right now, only xmms is supported, which means that you can
use any of xmms' visualisation plugins with Amarok.

%files visualisation
%defattr(-,root,root,-)
%{tde_bindir}/amarok_libvisual

%endif

##########

%if 0%{?pclinuxos} || 0%{?suse_version} && 0%{?opensuse_bs} == 0
%debug_package
%endif

##########

%prep
%setup -q -n %{name}-%{tde_version}%{?preversion:~%{preversion}}

# Fix some Ruby stuff
if ! ruby -rrbconfig -e "puts Config.expand( Config::MAKEFILE_CONFIG['MAJOR'] )" &>/dev/null; then
  %__sed -i "amarok/src/mediadevice/daap/ConfigureChecks.cmake" \
         -e "s|Config::|RbConfig::|g" \
         -e "s|Config\.|RbConfig\.|g"
fi


%build
unset QTDIR QTINC QTLIB
export PATH="%{tde_bindir}:${PATH}"
export PKG_CONFIG_PATH="%{tde_libdir}/pkgconfig"

# Specific path for RHEL4
if [ -d /usr/X11R6 ]; then
  export RPM_OPT_FLAGS="${RPM_OPT_FLAGS} -I/usr/X11R6/include -L/usr/X11R6/%{_lib}"
fi

if ! rpm -E %%cmake|grep -q "cd build"; then
  %__mkdir_p build
  cd build
fi

# Warning: GCC visibility causes FTBFS [Bug #1285]
%cmake \
  -DCMAKE_BUILD_TYPE="RelWithDebInfo" \
  -DCMAKE_C_FLAGS="${RPM_OPT_FLAGS} -DNDEBUG" \
  -DCMAKE_CXX_FLAGS="${RPM_OPT_FLAGS} -DNDEBUG" \
  -DCMAKE_SKIP_RPATH=OFF \
  -DCMAKE_INSTALL_RPATH="%{tde_libdir}" \
  -DCMAKE_NO_BUILTIN_CHRPATH=ON \
  -DCMAKE_VERBOSE_MAKEFILE=ON \
  -DWITH_GCC_VISIBILITY=OFF \
  \
  -DBIN_INSTALL_DIR=%{tde_bindir} \
  -DCONFIG_INSTALL_DIR="%{tde_confdir}" \
  -DINCLUDE_INSTALL_DIR=%{tde_tdeincludedir} \
  -DLIB_INSTALL_DIR=%{tde_libdir} \
  -DSHARE_INSTALL_PREFIX=%{tde_datadir} \
  \
  %{?with_libvisual:-DWITH_LIBVISUAL=ON} \
  -DWITH_KONQSIDEBAR=ON \
  %{?with_xine:-DWITH_XINE=ON} \
  %{?with_yauap:-DWITH_YAUAP=ON} \
  -DWITH_AKODE=OFF \
  %{?with_gpod:-DWITH_IPOD=ON} \
  %{?with_ifp:-DWITH_IFP=ON} \
  %{?with_njb:-DWITH_NJB=ON} \
  %{?with_mtp:-DWITH_MTP=ON} \
  %{?with_karma:-DWITH_RIOKARMA=ON} \
  -DWITH_DAAP=ON \
  %{?with_mp4v2:-DWITH_MP4V2=ON} \
  %{?with_inotify:-DWITH_INOTIFY=ON} \
  -DBUILD_ALL=ON \
  ..

%__make %{?_smp_mflags} || %__make


%install
%__rm -fr $RPM_BUILD_ROOT
%__make install DESTDIR=$RPM_BUILD_ROOT -C build


# unpackaged files
%__rm -f $RPM_BUILD_ROOT%{tde_libdir}/lib*.la
# Removes '.so' to avoid automatic -devel dependency
%__rm -f $RPM_BUILD_ROOT%{tde_libdir}/libamarok.so

magic_rpm_clean.sh
# Locales
%find_lang %{tde_pkg} || :

# HTML
for lang_dir in $RPM_BUILD_ROOT%{tde_tdedocdir}/HTML/* ; do
  if [ -d $lang_dir ]; then
    lang=$(basename $lang_dir)
    [ "$lang" == "en" ] && d=en/amarok || d=$lang
    echo "%lang($lang) %doc %{tde_tdedocdir}/HTML/$d" >> amarok.lang
  fi
done



%clean
%__rm -fr $RPM_BUILD_ROOT


%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 2:1.4.10-2.1
- 为 Magic 3.0 重建

* Mon Feb 02 2015 Francois Andriot <francois.andriot@free.fr> - 2:1.4.10-2
- Rebuild on CentOS 7 for updated mp4v2

* Mon Jul 29 2013 Francois Andriot <francois.andriot@free.fr> - 2:1.4.10-1
- Initial release for TDE 14.0.0
