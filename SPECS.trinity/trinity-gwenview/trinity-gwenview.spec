#
# spec file for package gwenview (version R14)
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
%define tde_pkg gwenview
%define tde_prefix /opt/trinity
%define tde_appdir %{tde_datadir}/applications
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


Name:			trinity-%{tde_pkg}
Epoch:			%{tde_epoch}
Version:		1.4.2
Release:		%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}%{?_variant}.1
Summary:		Gwenview is an image viewer for TDE.
Summary(zh_CN.UTF-8): TDE 下的图像查看器
Group:			Applications/Utilities
Group(zh_CN.UTF-8): 应用程序/工具
URL:			http://www.trinitydesktop.org/

License:	GPLv2+

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:			%{_prefix}
BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:		%{name}-%{tde_version}%{?preversion:~%{preversion}}.tar.gz

Patch1:			trinity-gwenview-14.0.1-tqt.patch

BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	desktop-file-utils
BuildRequires:	gettext

BuildRequires:	autoconf automake libtool m4
BuildRequires:	gcc-c++
BuildRequires:	pkgconfig

BuildRequires:	exiv2-devel

%if "%{?tde_prefix}" == "/usr"
Conflicts: kdegraphics
%endif


%description
Gwenview is a fast and easy to use image viewer/browser for TDE.
All common image formats are supported, such as PNG(including transparency),
JPEG(including EXIF tags and lossless transformations), GIF, XCF (Gimp
image format), BMP, XPM and others. Standard features include slideshow,
fullscreen view, image thumbnails, drag'n'drop, image zoom, full network
transparency using the KIO framework, including basic file operations and
browsing in compressed archives, non-blocking GUI with adjustable views.
Gwenview also provides image and directory KParts components for use e.g. in
Konqueror. Additional features, such as image renaming, comparing,
converting, and batch processing, HTML gallery and others are provided by the
KIPI image framework.

%description -l zh_CN.UTF-8
TDE 下的快速图像查看器。

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
  --docdir=%{tde_tdedocdir} \
  --includedir=%{tde_tdeincludedir} \
  --libdir=%{tde_libdir} \
  --mandir=%{tde_mandir} \
  \
  --disable-dependency-tracking \
  --disable-debug \
  --enable-new-ldflags \
  --enable-final \
  --enable-closure \
  --enable-rpath \
  --disable-gcc-hidden-visibility

%__make %{?_smp_mflags}


%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf %{buildroot}
%__make install DESTDIR=%{buildroot}

# Removes useless files (-devel ?)
%__rm -f %{?buildroot}%{tde_libdir}/libgwenviewcore.so

magic_rpm_clean.sh

%clean
%__rm -rf %{buildroot}


%post
for f in crystalsvg hicolor ; do
  touch --no-create %{tde_datadir}/icons/${f} || :
  gtk-update-icon-cache --quiet %{tde_datadir}/icons/${f} || :
done
/sbin/ldconfig


%postun
for f in crystalsvg hicolor ; do
  touch --no-create %{tde_datadir}/icons/${f} || :
  gtk-update-icon-cache --quiet %{tde_datadir}/icons/${f} || :
done
/sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING
%{tde_bindir}/gwenview
%{tde_libdir}/libgwenviewcore.la
%{tde_libdir}/libgwenviewcore.so.1
%{tde_libdir}/libgwenviewcore.so.1.0.0
%{tde_libdir}/libtdeinit_gwenview.la
%{tde_libdir}/libtdeinit_gwenview.so
%{tde_tdelibdir}/gwenview.la
%{tde_tdelibdir}/gwenview.so
%{tde_tdelibdir}/libgvdirpart.la
%{tde_tdelibdir}/libgvdirpart.so
%{tde_tdelibdir}/libgvimagepart.la
%{tde_tdelibdir}/libgvimagepart.so
%{tde_tdeappdir}/gwenview.desktop
%{tde_datadir}/apps/gwenview/
%dir %{tde_datadir}/apps/gvdirpart
%{tde_datadir}/apps/gvdirpart/gvdirpart.rc
%dir %{tde_datadir}/apps/gvimagepart
%{tde_datadir}/apps/gvimagepart/gvimagepart.rc
%{tde_datadir}/apps/gvimagepart/gvimagepartpopup.rc
%{tde_datadir}/apps/tdeconf_update/gwenview_1.4_osdformat.sh
%{tde_datadir}/apps/tdeconf_update/gwenview_1.4_osdformat.upd
%{tde_datadir}/apps/tdeconf_update/gwenview_thumbnail_size.sh
%{tde_datadir}/apps/tdeconf_update/gwenview_thumbnail_size.upd
%{tde_datadir}/apps/konqueror/servicemenus/konqgwenview.desktop
%{tde_datadir}/config.kcfg/fileoperationconfig.kcfg
%{tde_datadir}/config.kcfg/fileviewconfig.kcfg
%{tde_datadir}/config.kcfg/fullscreenconfig.kcfg
%{tde_datadir}/config.kcfg/gvdirpartconfig.kcfg
%{tde_datadir}/config.kcfg/imageviewconfig.kcfg
%{tde_datadir}/config.kcfg/miscconfig.kcfg
%{tde_datadir}/config.kcfg/slideshowconfig.kcfg
%{tde_datadir}/icons/crystalsvg/*/apps/gvdirpart.png
%{tde_datadir}/icons/crystalsvg/scalable/apps/gvdirpart.svg
%{tde_datadir}/icons/hicolor/*/apps/gwenview.png
%{tde_datadir}/icons/hicolor/*/apps/gvdirpart.png
%{tde_datadir}/icons/hicolor/scalable/apps/gvdirpart.svg
%{tde_datadir}/icons/hicolor/scalable/apps/gwenview.svgz
%{tde_datadir}/man/man1/gwenview.1*
%{tde_datadir}/services/gvdirpart.desktop
%{tde_datadir}/services/gvimagepart.desktop
%lang(en) %{tde_tdedocdir}/HTML/en/gwenview/

%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 2:1.4.2-1.1
- 为 Magic 3.0 重建

* Fri Jul 05 2013 Francois Andriot <francois.andriot@free.fr> - 2:1.4.2-1
- Initial release for TDE 14.0.0
