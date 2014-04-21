# Default version for this component
%define kdecomp digikam
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

%define tde_tdeappdir %{tde_datadir}/applications/kde
%define tde_tdedocdir %{tde_docdir}/tde
%define tde_tdeincludedir %{tde_includedir}/tde
%define tde_tdelibdir %{tde_libdir}/trinity

%define _docdir %{tde_docdir}


Name:		trinity-%{kdecomp}
Summary:	digital photo management application for KDE [Trinity]
Version:	0.9.6
Release:	5%{?dist}%{?_variant}

License:	GPLv2+
Group:		Applications/Utilities

Vendor:		Trinity Project
Packager:	Francois Andriot <francois.andriot@free.fr>
URL:		http://www.trinitydesktop.org/

Prefix:    %{_prefix}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:	%{kdecomp}-trinity-%{tdeversion}.tar.xz

# [digikam] Fix FTBFS on png >= 0.15 [Commit #18ecd512]
Patch9:		digikam-3.5.13-fix_ftbfs_png_015.patch


BuildRequires:	trinity-tqtinterface-devel >= 3.5.13.1
BuildRequires:	trinity-arts-devel >= 3.5.13.1
BuildRequires:	trinity-tdelibs-devel >= 3.5.13.1
BuildRequires:	trinity-tdebase-devel >= 3.5.13.1
BuildRequires:	trinity-libkexiv2-devel >= 3.5.13.1
BuildRequires:	trinity-libkdcraw-devel >= 3.5.13.1
BuildRequires:	trinity-libkipi-devel >= 3.5.13.1
%if 0%{?rhel} == 5 || 0%{?mgaversion} || 0%{?mdkversion}
BuildRequires:	gphoto2-devel
%else
BuildRequires:	libgphoto2-devel
%endif
BuildRequires:	libtiff-devel
BuildRequires:	desktop-file-utils
BuildRequires:	gettext

# JASPER support
%if 0%{?suse_version}
BuildRequires:	libjasper-devel
%else
BuildRequires:	jasper-devel
%endif

# EXIV2 support
%if 0%{?mgaversion} || 0%{?mdkversion}
BuildRequires:	%{_lib}exiv2-devel
%endif
%if 0%{?suse_version}
BuildRequires:	libexiv2-devel
%endif
%if 0%{?rhel} || 0%{?fedora}
BuildRequires:	exiv2-devel
%endif

Requires:	trinity-libkexiv2 >= 3.5.13.1
Requires:	trinity-libkdcraw >= 3.5.13.1
Requires:	trinity-libkipi >= 3.5.13.1

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


%package devel
Group:		Development/Libraries
Summary:	Development files for %{name}
Requires:	%{name} = %{version}

%description devel
%{summary}


%if 0%{?suse_version}
%debug_package
%endif


%prep
%setup -q -n %{kdecomp}-trinity-%{tdeversion}
#%patch9 -p1 -b .png015


# Ugly hack to modify TQT include directory inside autoconf files.
# If TQT detection fails, it fallbacks to TQT4 instead of TQT3 !
%__sed -i admin/acinclude.m4.in \
  -e "s|/usr/include/tqt|%{tde_includedir}/tqt|g" \
  -e "s|kde_htmldir='.*'|kde_htmldir='%{tde_tdedocdir}/HTML'|g"

%__cp -f "/usr/share/aclocal/libtool.m4" "admin/libtool.m4.in"
%__cp -f "/usr/share/libtool/config/ltmain.sh" "admin/ltmain.sh" || %__cp -f "/usr/share/libtool/ltmain.sh" "admin/ltmain.sh"
%__make -f "admin/Makefile.common"


%build
unset QTDIR || : ; source /etc/profile.d/qt3.sh
export PATH="%{tde_bindir}:${PATH}"
export LDFLAGS="-L%{tde_libdir} -I%{tde_tdeincludedir}"

%configure \
  --prefix=%{tde_prefix} \
  --exec-prefix=%{tde_prefix} \
  --bindir=%{tde_bindir} \
  --libdir=%{tde_libdir} \
  --datadir=%{tde_datadir} \
  --mandir=%{tde_mandir} \
  --includedir=%{tde_tdeincludedir} \
  --disable-rpath \
  --with-extra-includes=%{tde_tdeincludedir}/tqt \
  --enable-closure

%__make %{?_smp_mflags}


%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf %{buildroot}
%__make install DESTDIR=%{buildroot}


%find_lang %{kdecomp}


%clean
%__rm -rf %{buildroot}


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

%post devel
/sbin/ldconfig || :

%postun devel
/sbin/ldconfig || :


%files -f %{kdecomp}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING
%{tde_bindir}/digikam
%{tde_bindir}/digikamthemedesigner
%{tde_bindir}/digitaglinktree
%{tde_bindir}/showfoto
%{tde_libdir}/libdigikam.so.0
%{tde_libdir}/libdigikam.so.0.0.0
%{tde_tdelibdir}/kio_digikamalbums.la
%{tde_tdelibdir}/kio_digikamalbums.so
%{tde_tdelibdir}/kio_digikamdates.la
%{tde_tdelibdir}/kio_digikamdates.so
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
%{tde_tdelibdir}/kio_digikamsearch.la
%{tde_tdelibdir}/kio_digikamsearch.so
%{tde_tdelibdir}/kio_digikamtags.la
%{tde_tdelibdir}/kio_digikamtags.so
%{tde_tdelibdir}/kio_digikamthumbnail.la
%{tde_tdelibdir}/kio_digikamthumbnail.so
%{tde_tdeappdir}/digikam.desktop
%{tde_tdeappdir}/showfoto.desktop
%{tde_datadir}/apps/digikam/
%{tde_datadir}/apps/konqueror/servicemenus/digikam-download.desktop
%{tde_datadir}/apps/konqueror/servicemenus/digikam-gphoto2-camera.desktop
%{tde_datadir}/apps/konqueror/servicemenus/digikam-mount-and-download.desktop
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
#%{tde_tdedocdir}/HTML/en/digikam-apidocs/


%files devel
%{tde_tdeincludedir}/digikam_export.h
%{tde_tdeincludedir}/digikam/
%{tde_libdir}/libdigikam.so
%{tde_libdir}/libdigikam.la


%changelog
* Wed Oct 03 2012 Francois Andriot <francois.andriot@free.fr> - 0.9.6-4
- Initial build for TDE 3.5.13.1

* Fri Aug 03 2012 Francois Andriot <francois.andriot@free.fr> - 0.9.6-3
- Add support for Mageia 2 and Mandriva 2011
- Removes old patches, adds GIT patches.
- Fix digikam FTBFS due to jpeg code [Commit #b9419cd5]
- Fix FTBFS due to png code [Bug #595] [Commit #3e27b07f]
- Remove version.h. Cruft from an older version prior to 0.9.6.
- Fix usage of obsolete libpng jmpbuf member [Commit #7d0d82b7]
- GCC 4.7 fix. [Bug #958] [Commit #a9489034]
- GCC 4.7 fix. [Bug #958] [Commit #a209c81b]
- Fix 'format not a string literal' error [Commit #029218cd]
- Update patch in GIT hash a9489034 to use reinterpret_cast. [Commit #5a043853]
- Fix FTBFS on png >= 0.15 [Commit #18ecd512]

* Sun Jul 08 2012 Francois Andriot <francois.andriot@free.fr> - 0.9.6-3
- Fix man directory location
- Fix postinstall
- Fix description
- Add "BuildRequires: exiv2-devel"

* Tue May 01 2012 Francois Andriot <francois.andriot@free.fr> - 0.9.6-2
- gcc 4.7 + libpng 1.5 patch for digikam (consolidated) [Bug #958]

* Sun Nov 06 2011 Francois Andriot <francois.andriot@free.fr> - 0.9.6-1
- Initial release for RHEL 6, RHEL 5 and Fedora 15

