#
# spec file for package tderadio (version R14)
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

%if 0%{?rhel} >= 6 || 0%{?fedora} || 0%{?mdkversion} || 0%{?mgaversion} || 0%{?suse_version}
%define with_lirc 1
%endif

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.0.0
%endif
%define tde_pkg tderadio
%define tde_prefix /opt/trinity
%define tde_bindir %{tde_prefix}/bin
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
Version:	0.1.1.1
Release:	%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}
Summary:	Comfortable Radio Application for TDE
Group:		Applications/Utilities
URL:		http://www.trinitydesktop.org/

%if 0%{?suse_version}
License:	GPL-2.0+
%else
License:	GPLv2+
%endif

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:		%{tde_prefix}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:		%{name}-%{tde_version}%{?preversion:~%{preversion}}.tar.gz

BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	desktop-file-utils
BuildRequires:	gettext

BuildRequires:	autoconf automake libtool m4
BuildRequires:	gcc-c++
BuildRequires:	pkgconfig
BuildRequires:	fdupes

# SUSE desktop files utility
%if 0%{?suse_version}
BuildRequires:	update-desktop-files
%endif

%if 0%{?opensuse_bs} && 0%{?suse_version}
# for xdg-menu script
BuildRequires:	brp-check-trinity
%endif

BuildRequires:	libsndfile-devel
%{?with_lirc:BuildRequires:	lirc-devel}

%if 0%{?mgaversion} || 0%{?mdkversion}
BuildRequires:	%{_lib}twolame-devel
%endif
%if 0%{?suse_version}
BuildRequires:	libtwolame-devel
%endif
%if 0%{?rhel} || 0%{?fedora}
BuildRequires:	lame-devel
%endif

Obsoletes:		trinity-kradio < %{version}-%{release}
Provides:		trinity-kradio = %{version}-%{release}


%description
TDERadio is a comfortable radio application for Trinity with support for 
V4L and V4L2 radio cards drivers.

TDERadio currently provides

 * V4L/V4L2 radio support
%if 0%{?with_lirc}
 * Remote control support (LIRC)
%endif
 * Alarms, sleep Countdown
 * Several GUI Controls (Docking Menu, Station Quickbar, Radio Display)
 * Recording capabilities, including MP3 and Ogg/Vorbis encoding
 * Timeshifter functionality
 * Extendable plugin architecture

This package also includes a growing collection of station preset
files for many cities around the world contributed by TDERadio users.

As TDERadio is based on an extendable plugin architecture, contributions
of new plugins (e.g. Internet Radio Streams, new cool GUIs) are welcome.


##########

%if 0%{?pclinuxos} || 0%{?suse_version} && 0%{?opensuse_bs} == 0
%debug_package
%endif

##########


%prep
%setup -q -n %{name}-%{tde_version}%{?preversion:~%{preversion}}

%__cp "/usr/share/aclocal/libtool.m4" "admin/libtool.m4.in"
%__cp "/usr/share/libtool/config/ltmain.sh" "admin/ltmain.sh" || %__cp "/usr/share/libtool/ltmain.sh" "admin/ltmain.sh"
%__make -f "admin/Makefile.common"



%build
unset QTDIR QTINC QTLIB
export PATH="%{tde_bindir}:${PATH}"

# Warning: --enable-visibility causes applications fails to start !
%configure \
  --prefix=%{tde_prefix} \
  --exec-prefix=%{tde_prefix} \
  --bindir=%{tde_bindir} \
  --datadir=%{tde_datadir} \
  --libdir=%{tde_libdir} \
  --mandir=%{tde_mandir} \
  --includedir=%{tde_tdeincludedir} \
  \
  --disable-dependency-tracking \
  --disable-debug \
  --enable-final \
  --enable-new-ldflags \
  --enable-closure \
  --enable-rpath \
  --disable-gcc-hidden-visibility \
  \
  %{?with_lirc:--enable-lirc} %{?!with_lirc:--disable-lirc} \
  --enable-v4l2 \
  --enable-lame \
  --enable-ogg \
  --enable-alsa \
  --enable-oss

%__make %{?_smp_mflags}


%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf %{buildroot}
%__make install DESTDIR=%{buildroot}

%find_lang %{tde_pkg}

# Updates applications categories for openSUSE
%if 0%{?suse_version}
%suse_update_desktop_file -G "Radio Tuner" %{tde_pkg} AudioVideo Tuner
%endif


%clean
%__rm -rf %{buildroot}


%post
for f in hicolor locolor ; do
  touch --no-create %{tde_datadir}/icons/${f} || :
  gtk-update-icon-cache --quiet %{tde_datadir}/icons/${f} || :
done
update-desktop-database %{tde_tdeappdir} -q &> /dev/null ||:

%postun
for f in hicolor locolor ; do
  touch --no-create %{tde_datadir}/icons/${f} || :
  gtk-update-icon-cache --quiet %{tde_datadir}/icons/${f} || :
done
update-desktop-database %{tde_tdeappdir} -q &> /dev/null ||:


%files -f %{tde_pkg}.lang
%defattr(-,root,root,-)
%{tde_bindir}/convert-presets
%{tde_bindir}/tderadio
%dir %{tde_libdir}/tderadio
%dir %{tde_libdir}/tderadio/plugins
%{tde_libdir}/tderadio/plugins/*.la
%{tde_libdir}/tderadio/plugins/*.so
%{tde_tdeappdir}/tderadio.desktop
%{tde_datadir}/apps/tderadio/
%dir %{tde_datadir}/icons/hicolor/256x256
%dir %{tde_datadir}/icons/hicolor/256x256/actions
%{tde_datadir}/icons/hicolor/*/*/tderadio*.png
%{tde_datadir}/icons/locolor/*/*/tderadio*.png
%lang(de) %{tde_datadir}/locale/de/LC_MESSAGES/*.mo
%lang(ru) %{tde_datadir}/locale/ru/LC_MESSAGES/*.mo
%{tde_tdedocdir}/HTML/en/tderadio/

%changelog
* Fri Jul 05 2013 Francois Andriot <francois.andriot@free.fr> - 2:0.1.1.1-1
- Initial release for TDE 14.0.0
