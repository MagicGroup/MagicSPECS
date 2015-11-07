#
# spec file for package digikam (version R14)
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
%define tde_pkg digikam
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


Name:			trinity-%{tde_pkg}
Epoch:			%{tde_epoch}
Version:		0.9.6
Release:		%{?!preversion:6}%{?preversion:0_%{preversion}}%{?dist}%{?_variant}.3
Summary:		Digital photo management application for TDE
Summary(zh_CN.UTF-8): TDE 下的数码照片管理程序
Group:			Applications/Utilities
Group(zh_CN.UTF-8): 应用程序/工具
URL:			http://www.trinitydesktop.org/

License:	GPLv2+

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:			%{_prefix}
BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:		%{name}-%{tde_version}%{?preversion:~%{preversion}}.tar.gz
Source1:		digikam-open_in_digikam.desktop

Patch1:			trinity-digikam-14.0.1-tqt.patch

BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	desktop-file-utils

BuildRequires:	trinity-libkexiv2-devel
BuildRequires:	trinity-libkdcraw-devel
BuildRequires:	trinity-libkipi-devel

BuildRequires:	autoconf automake libtool m4
BuildRequires:	gcc-c++
BuildRequires:	pkgconfig
BuildRequires:	libtool

BuildRequires:	libtiff-devel
BuildRequires:	gettext

BuildRequires: lcms-devel

# GPHOTO2 support
BuildRequires:	gphoto2-devel

# JASPER support
BuildRequires:	jasper-devel

# EXIV2 support
BuildRequires:	exiv2-devel

Requires:		trinity-libkexiv2
Requires:		trinity-libkdcraw
Requires:		trinity-libkipi

%description
An easy to use and powerful digital photo management
application, which makes importing, organizing and manipulating
digital photos a "snap".  An interface is provided to connect to
your digital camera, preview the images and download and/or
delete them.

The digiKam built-in image editor makes the common photo correction
a simple task. The image editor is extensible via plugins and,
the digikamimageplugins project has been merged to digiKam core
since release 0.9.2, all useful image editor plugins are available
in the base installation.

digiKam can also make use of the KIPI image handling plugins to
extend its capabilities even further for photo manipulations,
import and export, etc. The kipi-plugins package contains many
very useful extentions.

digiKam is based in part on the work of the Independent JPEG Group.

%description -l zh_CN.UTF-8
数码照片管理程序。

%files -f %{tde_pkg}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING
%{tde_bindir}/digikam
%{tde_bindir}/digikamthemedesigner
%{tde_bindir}/digitaglinktree
%{tde_bindir}/showfoto
%{tde_libdir}/libdigikam.so.0
%{tde_libdir}/libdigikam.so.0.0.0
%{tde_tdelibdir}/tdeio_digikamalbums.la
%{tde_tdelibdir}/tdeio_digikamalbums.so
%{tde_tdelibdir}/tdeio_digikamdates.la
%{tde_tdelibdir}/tdeio_digikamdates.so
%{tde_tdelibdir}/digikamimageplugin_adjustcurves.la
%{tde_tdelibdir}/digikamimageplugin_adjustcurves.so
%{tde_tdelibdir}/digikamimageplugin_adjustlevels.la
%{tde_tdelibdir}/digikamimageplugin_adjustlevels.so
%{tde_tdelibdir}/digikamimageplugin_antivignetting.la
%{tde_tdelibdir}/digikamimageplugin_antivignetting.so
%{tde_tdelibdir}/digikamimageplugin_blurfx.la
%{tde_tdelibdir}/digikamimageplugin_blurfx.so
%{tde_tdelibdir}/digikamimageplugin_border.la
%{tde_tdelibdir}/digikamimageplugin_border.so
%{tde_tdelibdir}/digikamimageplugin_channelmixer.la
%{tde_tdelibdir}/digikamimageplugin_channelmixer.so
%{tde_tdelibdir}/digikamimageplugin_charcoal.la
%{tde_tdelibdir}/digikamimageplugin_charcoal.so
%{tde_tdelibdir}/digikamimageplugin_colorfx.la
%{tde_tdelibdir}/digikamimageplugin_colorfx.so
%{tde_tdelibdir}/digikamimageplugin_core.la
%{tde_tdelibdir}/digikamimageplugin_core.so
%{tde_tdelibdir}/digikamimageplugin_distortionfx.la
%{tde_tdelibdir}/digikamimageplugin_distortionfx.so
%{tde_tdelibdir}/digikamimageplugin_emboss.la
%{tde_tdelibdir}/digikamimageplugin_emboss.so
%{tde_tdelibdir}/digikamimageplugin_filmgrain.la
%{tde_tdelibdir}/digikamimageplugin_filmgrain.so
%{tde_tdelibdir}/digikamimageplugin_freerotation.la
%{tde_tdelibdir}/digikamimageplugin_freerotation.so
%{tde_tdelibdir}/digikamimageplugin_hotpixels.la
%{tde_tdelibdir}/digikamimageplugin_hotpixels.so
%{tde_tdelibdir}/digikamimageplugin_infrared.la
%{tde_tdelibdir}/digikamimageplugin_infrared.so
%{tde_tdelibdir}/digikamimageplugin_inpainting.la
%{tde_tdelibdir}/digikamimageplugin_inpainting.so
%{tde_tdelibdir}/digikamimageplugin_inserttext.la
%{tde_tdelibdir}/digikamimageplugin_inserttext.so
%{tde_tdelibdir}/digikamimageplugin_lensdistortion.la
%{tde_tdelibdir}/digikamimageplugin_lensdistortion.so
%{tde_tdelibdir}/digikamimageplugin_noisereduction.la
%{tde_tdelibdir}/digikamimageplugin_noisereduction.so
%{tde_tdelibdir}/digikamimageplugin_oilpaint.la
%{tde_tdelibdir}/digikamimageplugin_oilpaint.so
%{tde_tdelibdir}/digikamimageplugin_perspective.la
%{tde_tdelibdir}/digikamimageplugin_perspective.so
%{tde_tdelibdir}/digikamimageplugin_raindrop.la
%{tde_tdelibdir}/digikamimageplugin_raindrop.so
%{tde_tdelibdir}/digikamimageplugin_restoration.la
%{tde_tdelibdir}/digikamimageplugin_restoration.so
%{tde_tdelibdir}/digikamimageplugin_sheartool.la
%{tde_tdelibdir}/digikamimageplugin_sheartool.so
%{tde_tdelibdir}/digikamimageplugin_superimpose.la
%{tde_tdelibdir}/digikamimageplugin_superimpose.so
%{tde_tdelibdir}/digikamimageplugin_texture.la
%{tde_tdelibdir}/digikamimageplugin_texture.so
%{tde_tdelibdir}/digikamimageplugin_whitebalance.la
%{tde_tdelibdir}/digikamimageplugin_whitebalance.so
%{tde_tdelibdir}/tdeio_digikamsearch.la
%{tde_tdelibdir}/tdeio_digikamsearch.so
%{tde_tdelibdir}/tdeio_digikamtags.la
%{tde_tdelibdir}/tdeio_digikamtags.so
%{tde_tdelibdir}/tdeio_digikamthumbnail.la
%{tde_tdelibdir}/tdeio_digikamthumbnail.so
%{tde_tdeappdir}/digikam.desktop
%{tde_tdeappdir}/showfoto.desktop
%{tde_datadir}/apps/digikam/
%{tde_datadir}/apps/konqueror/servicemenus/digikam-download.desktop
%{tde_datadir}/apps/konqueror/servicemenus/digikam-gphoto2-camera.desktop
%{tde_datadir}/apps/konqueror/servicemenus/digikam-mount-and-download.desktop
%{tde_datadir}/apps/konqueror/servicemenus/digikam-open_in_digikam.desktop
%{tde_datadir}/apps/showfoto/
%{tde_datadir}/icons/hicolor/*/apps/digikam.png
%{tde_datadir}/icons/hicolor/*/apps/showfoto.png
%{tde_datadir}/services/digikamalbums.protocol
%{tde_datadir}/services/digikamdates.protocol
%{tde_datadir}/services/digikamimageplugin_adjustcurves.desktop
%{tde_datadir}/services/digikamimageplugin_adjustlevels.desktop
%{tde_datadir}/services/digikamimageplugin_antivignetting.desktop
%{tde_datadir}/services/digikamimageplugin_blurfx.desktop
%{tde_datadir}/services/digikamimageplugin_border.desktop
%{tde_datadir}/services/digikamimageplugin_channelmixer.desktop
%{tde_datadir}/services/digikamimageplugin_charcoal.desktop
%{tde_datadir}/services/digikamimageplugin_colorfx.desktop
%{tde_datadir}/services/digikamimageplugin_core.desktop
%{tde_datadir}/services/digikamimageplugin_distortionfx.desktop
%{tde_datadir}/services/digikamimageplugin_emboss.desktop
%{tde_datadir}/services/digikamimageplugin_filmgrain.desktop
%{tde_datadir}/services/digikamimageplugin_freerotation.desktop
%{tde_datadir}/services/digikamimageplugin_hotpixels.desktop
%{tde_datadir}/services/digikamimageplugin_infrared.desktop
%{tde_datadir}/services/digikamimageplugin_inpainting.desktop
%{tde_datadir}/services/digikamimageplugin_inserttext.desktop
%{tde_datadir}/services/digikamimageplugin_lensdistortion.desktop
%{tde_datadir}/services/digikamimageplugin_noisereduction.desktop
%{tde_datadir}/services/digikamimageplugin_oilpaint.desktop
%{tde_datadir}/services/digikamimageplugin_perspective.desktop
%{tde_datadir}/services/digikamimageplugin_raindrop.desktop
%{tde_datadir}/services/digikamimageplugin_restoration.desktop
%{tde_datadir}/services/digikamimageplugin_sheartool.desktop
%{tde_datadir}/services/digikamimageplugin_superimpose.desktop
%{tde_datadir}/services/digikamimageplugin_texture.desktop
%{tde_datadir}/services/digikamimageplugin_whitebalance.desktop
%{tde_datadir}/services/digikamsearch.protocol
%{tde_datadir}/services/digikamtags.protocol
%{tde_datadir}/services/digikamthumbnail.protocol
%{tde_datadir}/servicetypes/digikamimageplugin.desktop
%{tde_mandir}/man*/*
%{tde_tdedocdir}/HTML/en/digikam/
%{tde_tdedocdir}/HTML/en/showfoto/

%post
touch --no-create %{tde_datadir}/icons/hicolor || :
gtk-update-icon-cache --quiet %{tde_datadir}/icons/hicolor || :
/sbin/ldconfig
update-desktop-database %{tde_appdir} 2> /dev/null || : 

%postun
touch --no-create %{tde_datadir}/icons/hicolor || :
gtk-update-icon-cache --quiet %{tde_datadir}/icons/hicolor || :
/sbin/ldconfig
update-desktop-database %{tde_appdir} 2> /dev/null || : 

##########

%package devel
Group:			Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Summary:		Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires:		%{name} = %{epoch}:%{version}-%{release}

%description devel
%{summary}

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%files devel
%defattr(-,root,root,-)
%{tde_tdeincludedir}/digikam_export.h
%{tde_tdeincludedir}/digikam/
%{tde_libdir}/libdigikam.so
%{tde_libdir}/libdigikam.la

%post devel
/sbin/ldconfig || :

%postun devel
/sbin/ldconfig || :

##########

%package i18n
Summary:		Translation files for %{tde_pkg}
Group:			Applications/Utilities
Requires:		%{name} = %{epoch}:%{version}-%{release}

%description i18n
%{summary}

%files i18n
%defattr(-,root,root,-)
%lang(da) %{tde_tdedocdir}/HTML/da/digikam/
%lang(da) %{tde_tdedocdir}/HTML/da/showfoto/
%lang(de) %{tde_tdedocdir}/HTML/de/digikam/
%lang(de) %{tde_tdedocdir}/HTML/de/showfoto/
%lang(es) %{tde_tdedocdir}/HTML/es/digikam/
%lang(es) %{tde_tdedocdir}/HTML/es/showfoto/
%lang(et) %{tde_tdedocdir}/HTML/et/digikam/
%lang(et) %{tde_tdedocdir}/HTML/et/showfoto/
%lang(it) %{tde_tdedocdir}/HTML/it/digikam/
%lang(it) %{tde_tdedocdir}/HTML/it/showfoto/
%lang(nl) %{tde_tdedocdir}/HTML/nl/digikam/
%lang(nl) %{tde_tdedocdir}/HTML/nl/showfoto/
%lang(pt_BR) %{tde_tdedocdir}/HTML/pt_BR/digikam/
#%lang(pt_BR) %{tde_tdedocdir}/HTML/pt_BR/showfoto/
%lang(ru) %{tde_tdedocdir}/HTML/ru/digikam/
#%lang(ru) %{tde_tdedocdir}/HTML/ru/showfoto/
%lang(sv) %{tde_tdedocdir}/HTML/sv/digikam/
%lang(sv) %{tde_tdedocdir}/HTML/sv/showfoto/

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
  --libdir=%{tde_libdir} \
  --datadir=%{tde_datadir} \
  --mandir=%{tde_mandir} \
  --includedir=%{tde_tdeincludedir} \
  \
  --disable-dependency-tracking \
  --disable-debug \
  --enable-new-ldflags \
  --enable-final \
  --enable-closure \
  --enable-rpath \
  --disable-gcc-hidden-visibility

%__make %{?_smp_mflags} || %__make


%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf %{buildroot}
%__make install DESTDIR=%{buildroot}
magic_rpm_clean.sh
%find_lang %{tde_pkg}

# Hide 'showfoto'.
echo "NoDisplay=true" >> "$RPM_BUILD_ROOT%{tde_tdeappdir}/showfoto.desktop"

# Install the 'open in digikam' action for konqueror.
install -D -m 644 "%{SOURCE1}" "$RPM_BUILD_ROOT%{tde_datadir}/apps/konqueror/servicemenus/digikam-open_in_digikam.desktop"

%clean
%__rm -rf %{buildroot}


%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 2:0.9.6-6.3
- 为 Magic 3.0 重建

* Thu Oct 08 2015 Liu Di <liudidi@gmail.com> - 2:0.9.6-6.2
- 为 Magic 3.0 重建

* Thu Oct 08 2015 Liu Di <liudidi@gmail.com> - 2:0.9.6-6.1
- 为 Magic 3.0 重建

* Mon Feb 02 2015 Francois Andriot <francois.andriot@free.fr> - 2:0.9.6-2
- Rebuild on Fedora 21 for updated libgphoto2

* Mon Jul 29 2013 Francois Andriot <francois.andriot@free.fr> - 2:0.9.6-1
- Initial release for TDE 14.0.0
