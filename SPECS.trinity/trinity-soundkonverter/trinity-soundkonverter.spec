#
# spec file for package soundkonverter (version R14)
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
%define tde_pkg soundkonverter
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
Version:	0.3.8
Release:	%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}.1
Summary:	Audio converter frontend for Trinity
Summary(zh_CN.UTF-8): TDE 下的音频转换程序
Group:		Application/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
URL:		http://potracegui.sourceforge.net

License:	GPLv2+

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:		%{tde_prefix}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:		%{name}-%{tde_version}%{?preversion:~%{preversion}}.tar.gz

Patch1:		%{name}-14.0.1-tqt.patch

BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	desktop-file-utils

BuildRequires:	autoconf automake libtool m4
BuildRequires:	gcc-c++
BuildRequires:	pkgconfig
BuildRequires:	fdupes

# TAGLIB support
BuildRequires:	taglib-devel

BuildRequires:	cdparanoia-devel

%description
soundKonverter is a frontend to various audio converters.

The key features are:
 - Audio conversion
 - Replay Gain calculation
 - CD ripping

soundKonverter supports reading and writing tags for many formats, so the tags
are preserved when converting files.

It comes with an Amarok script.

See 'soundkonverter-amarok' package for more informations.

See README.Debian for more informations on supported formats.

%description -l zh_CN.UTF-8
TDE 下的音频转换程序。

%package amarok
Summary:		audio converter frontend for Trinity (Amarok script)
Summary(zh_CN.UTF-8): TDE 下的音频转换程序
Group:			Application/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
Requires:		%{name} = %{epoch}:%{version}-%{release}
Requires:		trinity-amarok

%description amarok
Amarok script for soundKonverter. It allows you to easily transcode files when
transferring them to your media device.

See the 'soundkonverter-trinity' package for more information.

%description amarok -l zh_CN.UTF-8
%{name} 的 Amarok 脚本。

##########

%prep
%setup -q -n %{name}-%{tde_version}%{?preversion:~%{preversion}}
%patch1 -p1

%__cp -f "/usr/share/aclocal/libtool.m4" "admin/libtool.m4.in"
%__cp -f "/usr/share/libtool/config/ltmain.sh" "admin/ltmain.sh" || %__cp -f "/usr/share/libtool/ltmain.sh" "admin/ltmain.sh"
%__make -f "admin/Makefile.common"


%build
unset QTDIR QTINC QTLIB
export PATH="%{tde_bindir}:${PATH}"

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
  --disable-gcc-hidden-visibility
   
%__make %{?_smp_mflags}


%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf %{buildroot}
%__make install DESTDIR=%{buildroot}
magic_rpm_clean.sh
%find_lang %{tde_pkg} || :

%clean
%__rm -rf %{buildroot}


%post
update-desktop-database %{tde_tdeappdir} > /dev/null
touch --no-create %{tde_datadir}/icons/hicolor || :
gtk-update-icon-cache --quiet %{tde_datadir}/icons/hicolor || :

%postun
update-desktop-database %{tde_tdeappdir} > /dev/null
touch --no-create %{tde_datadir}/icons/hicolor || :
gtk-update-icon-cache --quiet %{tde_datadir}/icons/hicolor || :


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README TODO
%{tde_bindir}/soundkonverter
%{tde_bindir}/userscript.sh
%{tde_tdeappdir}/soundkonverter.desktop
%{tde_datadir}/apps/konqueror/servicemenus/audiocd_extract_with_soundkonverter.desktop
%{tde_datadir}/apps/soundkonverter
%exclude %{tde_datadir}/apps/soundkonverter/amarokscript/
%{tde_tdedocdir}/HTML/en/soundkonverter/
%{tde_datadir}/icons/hicolor/*/apps/soundkonverter*.png
%{tde_datadir}/mimelnk/application/x-la.soundkonverter.desktop
%{tde_datadir}/mimelnk/application/x-ofc.soundkonverter.desktop
%{tde_datadir}/mimelnk/application/x-ofr.soundkonverter.desktop
%{tde_datadir}/mimelnk/application/x-ofs.soundkonverter.desktop
%{tde_datadir}/mimelnk/application/x-shorten.soundkonverter.desktop
%{tde_datadir}/mimelnk/audio/amr.soundkonverter.desktop
%{tde_datadir}/mimelnk/audio/x-ape.soundkonverter.desktop
%{tde_datadir}/mimelnk/audio/x-bonk.soundkonverter.desktop
%{tde_datadir}/mimelnk/audio/x-pac.soundkonverter.desktop
%{tde_datadir}/mimelnk/audio/x-tta.soundkonverter.desktop
%{tde_datadir}/mimelnk/audio/x-wavpack-correction.soundkonverter.desktop
%{tde_datadir}/mimelnk/audio/x-wavpack.soundkonverter.desktop
%{tde_datadir}/mimelnk/video/x-flv.soundkonverter.desktop

%files amarok
%defattr(-,root,root,-)
%{tde_datadir}/apps/soundkonverter/amarokscript/


%changelog
* Thu Nov 05 2015 Liu Di <liudidi@gmail.com> - 2:0.3.8-1.1
- 为 Magic 3.0 重建

* Fri Jul 05 2013 Francois Andriot <francois.andriot@free.fr> - 2:0.3.8-1
- Initial release for TDE 14.0.0
