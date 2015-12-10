Name:    kde4-kmplayer
%define realname kmplayer
Summary: A simple front-end for MPlayer/FFMpeg/Phonon
Summary(zh_CN): 一个 Mplayer/FFMpeg/Phonon 的简单前端
Version: 0.11.3d
Release: 3%{?dist}
Group:   Applications/Multimedia
Group(zh_CN):	应用程序/多媒体
# The documentation is GFDL.
# The files under src/moz-sdk are MPLv1.1 or GPLv2+ or LGPLv2+
# except src/moz-sdk/npruntime.h is BSD.
# The other source files carry GPL and LGPL licenses
# For instance:
# src/kmplayer.h is GPLv2+
# src/kmplayer_asx.cpp is LGPLv2
# src/kmplayer_atom.h is LGPLv2+
# and each of the other source files carry one of the above 3 licenses. So
#License: GFDL and (MPLv1.1 or GPLv2+ or LGPLv2+) and BSD and GPLv2+ and LGPLv2 and LGPLv2+
License: GFDL and GPLv2+
URL:     http://kmplayer.kde.org/
Source0: http://kmplayer.kde.org/pkgs/kmplayer-%{version}%{?beta}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# default to using phonon (instead of mplayer)
Patch4: kmplayer-0.11.0a-kmplayerrc_phonon_default.patch
Patch5: kmplayer-0.11.3a-newglib.patch

BuildRequires: cairo-devel
BuildRequires: dbus-devel 
BuildRequires: dbus-glib-devel
BuildRequires: desktop-file-utils
BuildRequires: expat-devel
BuildRequires: gettext
BuildRequires: glib2-devel
BuildRequires: gtk2-devel
BuildRequires: kdelibs4-devel
BuildRequires: pango-devel
BuildRequires: phonon-devel

%description
KMPlayer, a simple front-end for MPlayer/FFMpeg/Phonon.
It can play DVD/VCD movies, from file or URL and from a video device.
KMPlayer can embed inside Konqueror. Which means if you click
on a movie file, the movie is played inside Konqueror.

%description -l zh_CN
一个 Mplayer/FFMpeg/Phonon 的简单前端。
它可以播放 DVD/VCD 影片。

%prep
%setup -q -n %{realname}-%{version}%{?beta}
%patch4 -p1 -b .kmplayerrc_phonon_default
#%patch5 -p1

%build

mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} \
 -DWITH_EXPAT:BOOL=ON \
  ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
rm -rf %{buildroot}

make install DESTDIR=%{buildroot} -C %{_target_platform}

## File lists
# locale's
magic_rpm_clean.sh
%find_lang %{name} 
# HTML (1.0)
HTML_DIR=$(kde4-config --expandvars --install html)
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

## unpackaged files
# oxygen conflicts
rm -f %{buildroot}%{_kde4_iconsdir}/oxygen/*/apps/kmplayer.*

# Desktop file
desktop-file-install \
   --dir=%{buildroot}/%{_kde4_datadir}/applications/kde4 \
   --add-category="Player" \
   %{buildroot}/%{_kde4_datadir}/applications/kde4/kmplayer.desktop

# Permission fix
chmod +x %{buildroot}/%{_kde4_datadir}/apps/kmplayer/find-media.sh

%clean
rm -rf %{buildroot}


%post
touch --no-create %{_kde4_iconsdir}hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_kde4_iconsdir}/hicolor &>/dev/null
    gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &>/dev/null
    update-desktop-database -q &> /dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &>/dev/null || :
update-desktop-database -q &> /dev/null || :

%files
#%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING* README TODO
%{_kde4_bindir}/kmplayer
%{_kde4_bindir}/knpplayer
%{_kde4_bindir}/kphononplayer
%{_kde4_appsdir}/kmplayer/
%{_kde4_configdir}/kmplayerrc
%{_kde4_datadir}/applications/kde4/kmplayer.desktop
%{_kde4_datadir}/kde4/services/*.desktop
%{_kde4_iconsdir}/hicolor/*/*/*
%{_kde4_libdir}/kde4/*.so
%{_kde4_libdir}/libkdeinit4_kmplayer.so
%{_kde4_libdir}/libkmplayercommon.so
%{kde4_localedir}/*
%{kde4_datadir}/doc/*

%changelog
* Sun Nov 08 2015 Liu Di <liudidi@gmail.com> - 0.11.3d-3
- 为 Magic 3.0 重建

* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 0.11.3d-2
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.11.3a-2
- 为 Magic 3.0 重建

