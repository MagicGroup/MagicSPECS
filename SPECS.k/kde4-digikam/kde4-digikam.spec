%define real_name digikam
#define pre %{nil}
Name:	 kde4-digikam
Version: 4.1.0
Release: 2%{?dist}
Summary: A digital camera accessing & photo management application
Summary(zh_CN.UTF-8): 一个数码相机访问和照片管理程序

License: GPLv2+
URL:	 http://www.digikam.org/
Source0: http://download.kde.org/stable/digikam/digikam-%{version}%{?pre:-%{pre}}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# digiKam not listed as a media handler for pictures in Nautilus (#516447)
# TODO: upstream me
Source1: digikam-import.desktop

# fix FindCLAPACK.cmake to search %%{_libdir}/atlas
# also patch matrix.cpp for the ATLAS clapack API
# The latter part is probably not upstreamable as is, and the former on its own
# isn't helpful.
Patch0: digikam-2.1.1-clapack-atlas.patch

Patch1:	digikam-3.0.0-beta3-backkipi.patch

## upstreamable patches

## upstream patches
# https://projects.kde.org/projects/extragear/graphics/digikam/repository/revisions/beecc2628e0c4ad3a9a44b28a88360b391048c7d
# fix collision of digiKam icons with Oxygen
Patch100: digikam-2.3.0-hicolor-icons.patch

# for clapack, see also the clapack-atlas patch
BuildRequires: atlas-devel
BuildRequires: desktop-file-utils
BuildRequires: doxygen
BuildRequires: gettext
# marble integration, http://bugzilla.redhat.com/470578
BuildRequires: kde4-marble >= 4.6.80 
BuildRequires: kdelibs4-devel
BuildRequires: kdepimlibs4-devel
BuildRequires: libtiff-devel
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(jasper)
BuildRequires: pkgconfig(lcms)
BuildRequires: pkgconfig(lensfun)
BuildRequires: pkgconfig(libgphoto2_port)
BuildRequires: pkgconfig(lqr-1)
BuildRequires: pkgconfig(libpgf) >= 6.11.42
BuildRequires: pkgconfig(libpng) >= 1.2.7
BuildRequires: pkgconfig(libkdcraw)
BuildRequires: pkgconfig(libkexiv2)
BuildRequires: pkgconfig(libkipi)
BuildRequires: pkgconfig(sqlite3)
BuildRequires: mysql-devel mysql-server
BuildRequires: pkgconfig(exiv2)
## DNG converter
BuildRequires: expat-devel
BuildRequires: pkgconfig(libgpod-1.0)
# until when/if libksane-devel grows a depn on sane-backends-devel
BuildRequires: pkgconfig(libksane) 
BuildRequires: sane-backends-devel
## htmlexport plugin
BuildRequires: pkgconfig(libxslt)
## RemoveRedeye
BuildRequires: pkgconfig(opencv)
## Shwup
BuildRequires: pkgconfig(qca2)
## debianscreenshorts
BuildRequires: pkgconfig(QJson) 

# when lib(-devel) subpkgs were split
Obsoletes: digikam-devel < 2.0.0-2

Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: kdebase4-runtime%{?_kde4_version: >= %{_kde4_version}}

%description
digiKam is an easy to use and powerful digital photo management application,
which makes importing, organizing and manipulating digital photos a "snap".
An easy to use interface is provided to connect to your digital camera,
preview the images and download and/or delete them.

digiKam built-in image editor makes the common photo correction a simple task.
The image editor is extensible via plugins, can also make use of the KIPI image
handling plugins to extend its capabilities even further for photo
manipulations, import and export, etc. Install the kipi-plugins packages
to use them.

%package libs
Summary: Runtime libraries for %{name}
Requires: %{name} = %{version}-%{release}
# grow versioned deps on libkipi (and friends instead?) -- rex
#Requires: kdegraphics-libs%{?_isa}%{?_kde4_version: >= %{_kde4_version}}
%description libs
%{summary}.

%package devel
Summary: Development files for %{name}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: kdelibs4-devel
%description devel
This package contains the libraries, include files and other resources
needed to develop applications using %{name}.

%package -n libkface
Summary: A C++ wrapper around LibFace library to perform face recognition over pictures.  
# when libs were split 
Conflicts: digikam-libs < 2.0.0-2
%description -n libkface 
%{summary}.

%package -n libkface-devel
Summary: Development files for libkface 
%description -n libkface-devel
%{summary}.

%package -n libkgeomap
Summary: A world map library
# when libs were split 
Conflicts: digikam-libs < 2.0.0-2
Requires: kde4-marble%{?_kde4_version: >= %{_kde4_version}}
%description -n libkgeomap
%{summary}.

%package -n libkgeomap-devel
Summary: Development files for libkgeomap
%description -n libkgeomap-devel
%{summary}.

%package -n libmediawiki
Summary: a MediaWiki C++ interface
# when libs were split 
Conflicts: digikam-libs < 2.0.0-2
%description -n libmediawiki
%{summary}.

%package -n libmediawiki-devel
Summary: Development files for libmediawiki
%description -n libmediawiki-devel
%{summary}.

%package -n libkvkontakte
Summary: Library implementing VKontakte.ru API
%description -n libkvkontakte
KDE C++ library for asynchronous interaction with
vkontakte.ru social network via its open API.

%package -n libkvkontakte-devel
Summary: Development files for libkvkontakte
%description -n libkvkontakte-devel
%{summary}.

%package -n kipi-plugins
Summary: Plugins to use with Kipi
License: GPLv2+ and Adobe
Requires: kipi-plugins-libs%{?_isa} = %{version}-%{release}
## jpeglossless plugin
Requires: ImageMagick
## expoblending
Requires: hugin-base
%description -n kipi-plugins
This package contains plugins to use with Kipi, the KDE Image Plugin
Interface.  Currently implemented plugins are:
AcquireImages      : acquire images using flat scanner
AdvancedSlideshow  : slide images with 2D and 3D effects using OpenGL
Calendar           : create calendars
DngConverter       : convert Raw Image to Digital NeGative
ExpoBlending       : blend bracketed images
FbExport           : export images to a remote Facebook web service
FlickrExport       : export images to a remote Flickr web service
GalleryExport      : export images to a remote Gallery server
GPSSync            : geolocalize pictures
HTMLExport         : export images collections into a static XHTML page
ImageViewer        : preview images using OpenGL
IpodExport         : export pictures to an Ipod device
JpegLossLess       : rotate/flip images without losing quality
KioExportImport    : export/imports pictures to/from accessible via KIO
MetadataEdit       : edit EXIF, IPTC and XMP metadata
PicasaWebExport    : export images to a remote Picasa web service
PrintWizard        : print images in various format
RemoveRedEyes      : remove red eyes on image automatically
RawConverter       : convert Raw Image to JPEG/PNG/TIFF
SendImages         : send images by e-mail
SimpleViewerExport : export images to Flash using SimpleViewer
ShwupExport        : export images to a remote Shwup web service
SmugExport         : export images to a remote SmugMug web service
TimeAdjust         : adjust date and time

%package -n kipi-plugins-libs
Summary: Runtime libraries for kipi-plugins
License: GPLv2+ and Adobe
Requires: kipi-plugins = %{version}-%{release}
%{?_kde4_version:Requires: kdelibs4%{?_isa} >= %{_kde4_version}}
%{?_qt4_version:Requires: qt4%{?_isa} >= %{_qt4_version}}
%description -n kipi-plugins-libs
%{summary}.


%prep
%setup -q -n %{real_name}-%{version}%{?pre:-%{pre}}

#%patch1 -p1
#%patch0 -p1 -b .clapack-atlas

#pushd core
#for i in data/icons/apps/ox*; do mv $i $(echo $i | sed -e 's/ox/hi/g'); done
#%patch100 -p1 -b .hicolor-icons
#popd

%build

mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} -DDIGIKAMSC_USE_PRIVATE_KDEGRAPHICS:BOOL=0 ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
rm -rf %{buildroot}

make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

desktop-file-install --vendor="" \
  --dir=%{buildroot}%{_datadir}/applications/kde4 \
  %{SOURCE1}

magic_rpm_clean.sh

## unpackaged files
rm -f %{buildroot}%{_kde4_libdir}/libdigikamcore.so
rm -f %{buildroot}%{_kde4_libdir}/libdigikamdatabase.so
rm -f %{buildroot}%{_kde4_libdir}/libkipiplugins.so
rm -f %{buildroot}%{_kde4_libdir}/libPropertyBrowser.a

%check
for i in %{buildroot}%{_kde4_datadir}/applications/kde4/*.desktop ; do
desktop-file-validate $i
done


%post
touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
  touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null
  gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null || :
  update-desktop-database -q &> /dev/null
fi

%posttrans
gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null || :
update-desktop-database -q &> /dev/null

%files
%doc core/AUTHORS core/ChangeLog core/COPYING
%doc core/NEWS core/README core/TODO
%doc core/TODO.FACE core/TODO.MYSQLPORT
%{_kde4_bindir}/digikam
%{_kde4_bindir}/digitaglinktree
%{_kde4_bindir}/cleanup_digikamdb
%{_kde4_bindir}/showfoto
%{_kde4_libdir}/kde4/digikam*.so
%{_kde4_libdir}/kde4/kio_digikam*.so
%{_kde4_appsdir}/digikam/
%{_kde4_appsdir}/showfoto/
%{_kde4_appsdir}/solid/actions/digikam*.desktop
%{_datadir}/applications/kde4/digikam-import.desktop
%{_kde4_datadir}/applications/kde4/digikam.desktop
%{_kde4_datadir}/applications/kde4/showfoto.desktop
%{_kde4_datadir}/kde4/services/digikam*.desktop
%{_kde4_datadir}/kde4/services/digikam*.protocol
%{_kde4_datadir}/kde4/servicetypes/digikam*.desktop
%{kde4_mandir}/man1/digitaglinktree.1*
%{kde4_mandir}/man1/cleanup_digikamdb.1*
%{_kde4_iconsdir}/hicolor/*/apps/digikam*
%{_kde4_iconsdir}/hicolor/*/apps/showfoto*
#%{_kde4_libexecdir}/digikamdatabaseserver
%{kde4_htmldir}/en/digikam/*
%{kde4_htmldir}/en/showfoto/*
%{kde4_datadir}/locale/zh_*/LC_MESSAGES/digikam.mo
%{kde4_appsdir}/kconf_update/adjustlevelstool.upd
%{kde4_appsdir}/kipi/tips

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files libs
%{_kde4_libdir}/libdigikamcore.so.*
%{_kde4_libdir}/libdigikamdatabase.so.*

%post -n libkface -p /sbin/ldconfig
%postun -n libkface -p /sbin/ldconfig

%files -n libkface
%{_kde4_appsdir}/libkface/
%{_kde4_libdir}/libkface.so.*

%files -n libkface-devel
%{_kde4_includedir}/libkface/
%{_kde4_libdir}/libkface.so
%{_kde4_appsdir}/cmake/modules/FindKface.cmake
%{_libdir}/pkgconfig/libkface.pc

%post -n libkgeomap -p /sbin/ldconfig
%postun -n libkgeomap -p /sbin/ldconfig

%files -n libkgeomap 
#%{_kde4_bindir}/libkgeomap_demo
%{_kde4_appsdir}/libkgeomap/
%{_kde4_libdir}/libkgeomap.so.*
%{kde4_localedir}/zh_*/LC_MESSAGES/libkgeomap.mo

%files -n libkgeomap-devel
%{_kde4_includedir}/libkgeomap/
%{_kde4_libdir}/libkgeomap.so
%{_kde4_appsdir}/cmake/modules/FindKGeoMap.cmake
%{_libdir}/pkgconfig/libkgeomap.pc

%post -n libmediawiki -p /sbin/ldconfig
%postun -n libmediawiki -p /sbin/ldconfig

%files -n libmediawiki
%{_kde4_libdir}/libmediawiki.so.*

%files -n libmediawiki-devel
%{_kde4_includedir}/libmediawiki/
%{_kde4_libdir}/libmediawiki.so
%{_kde4_appsdir}/cmake/modules/FindMediawiki.cmake
%{_libdir}/pkgconfig/libmediawiki.pc

%post -n libkvkontakte -p /sbin/ldconfig
%postun -n libkvkontakte -p /sbin/ldconfig

%files -n libkvkontakte
%{kde4_libdir}/libkvkontakte.so.*

%files -n libkvkontakte-devel
%{kde4_includedir}/libkvkontakte/
%{kde4_libdir}/libkvkontakte.so
%{kde4_libdir}/cmake/LibKVkontakte/

%post -n kipi-plugins
touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null  ||:
touch --no-create %{_kde4_iconsdir}/oxygen &> /dev/null ||:

%postun -n kipi-plugins
if [ $1 -eq 0 ] ; then
  touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null ||:
  touch --no-create %{_kde4_iconsdir}/oxygen  &> /dev/null ||:
  gtk-update-icon-cache %{_kde4_iconsdir}/hicolor >& /dev/null ||:
  gtk-update-icon-cache %{_kde4_iconsdir}/oxygen >& /dev/null ||:
  update-desktop-database -q &> /dev/null
fi

%posttrans -n kipi-plugins
gtk-update-icon-cache %{_kde4_iconsdir}/hicolor >& /dev/null ||:
gtk-update-icon-cache %{_kde4_iconsdir}/oxygen >& /dev/null ||:
update-desktop-database -q &> /dev/null

%files -n kipi-plugins
#%doc extra/kipi-plugins/AUTHORS extra/kipi-plugins/COPYING
#%doc extra/kipi-plugins/COPYING-ADOBE extra/kipi-plugins/ChangeLog
#%doc extra/kipi-plugins/README extra/kipi-plugins/TODO extra/kipi-plugins/NEWS
%{_kde4_bindir}/dngconverter
%{_kde4_bindir}/dnginfo
%{_kde4_bindir}/expoblending
%{_kde4_bindir}/panoramagui
%{_kde4_bindir}/photolayoutseditor
%{_kde4_bindir}/scangui
%{_kde4_libdir}/kde4/kipiplugin_acquireimages.so
%{_kde4_libdir}/kde4/kipiplugin_advancedslideshow.so
%{_kde4_libdir}/kde4/kipiplugin_batchprocessimages.so
%{_kde4_libdir}/kde4/kipiplugin_calendar.so
%{_kde4_libdir}/kde4/kipiplugin_debianscreenshots.so
%{_kde4_libdir}/kde4/kipiplugin_dngconverter.so
%{_kde4_libdir}/kde4/kipiplugin_facebook.so
%{_kde4_libdir}/kde4/kipiplugin_flickrexport.so
%{_kde4_libdir}/kde4/kipiplugin_flashexport.so
%{_kde4_libdir}/kde4/kipiplugin_galleryexport.so
%{_kde4_libdir}/kde4/kipiplugin_gpssync.so
#%{_kde4_libdir}/kde4/kipiplugin_htmlexport.so
%{_kde4_libdir}/kde4/kipiplugin_imageviewer.so
%{_kde4_libdir}/kde4/kipiplugin_ipodexport.so
%{_kde4_libdir}/kde4/kipiplugin_jpeglossless.so
%{_kde4_libdir}/kde4/kipiplugin_kioexportimport.so
%{_kde4_libdir}/kde4/kipiplugin_kmlexport.so
%{_kde4_libdir}/kde4/kipiplugin_kopete.so
%{_kde4_libdir}/kde4/kipiplugin_metadataedit.so
%{_kde4_libdir}/kde4/kipiplugin_panorama.so
%{_kde4_libdir}/kde4/kipiplugin_picasawebexport.so
%{_kde4_libdir}/kde4/kipiplugin_piwigoexport.so
%{_kde4_libdir}/kde4/kipiplugin_printimages.so
%{_kde4_libdir}/kde4/kipiplugin_rajceexport.so
%{_kde4_libdir}/kde4/kipiplugin_rawconverter.so
%{_kde4_libdir}/kde4/kipiplugin_sendimages.so
%{_kde4_libdir}/kde4/kipiplugin_shwup.so
%{_kde4_libdir}/kde4/kipiplugin_smug.so
%{_kde4_libdir}/kde4/kipiplugin_timeadjust.so
%{_kde4_libdir}/kde4/kipiplugin_vkontakte.so
%{_kde4_libdir}/kde4/kipiplugin_yandexfotki.so
%{_kde4_libdir}/kde4/kipiplugin_dropbox.so
%{_kde4_libdir}/kde4/kipiplugin_googledrive.so
%{_kde4_libdir}/kde4/kipiplugin_htmlexport.so
%{_kde4_libdir}/kde4/kipiplugin_jalbumexport.so
%{_kde4_libdir}/kde4/kipiplugin_videoslideshow.so
%{_kde4_appsdir}/kipiplugin_htmlexport/THEME_HOWTO
%{_kde4_appsdir}/kipiplugin_htmlexport/themes/*
%{kde4_kcfgdir}/photolayoutseditor.kcfg
%{_kde4_iconsdir}/hicolor/*/apps/kipi-*.png
%{_kde4_appsdir}/gpssync/
%{_kde4_appsdir}/kipiplugin_flashexport/
%{_kde4_appsdir}/kipiplugin_galleryexport/
#%{_kde4_appsdir}/kipiplugin_htmlexport/
%{_kde4_appsdir}/kipiplugin_imageviewer/
%{_kde4_appsdir}/kipiplugin_panorama/
%{_kde4_appsdir}/kipiplugin_piwigoexport/
%{_kde4_appsdir}/kipiplugin_printimages/
%{_kde4_datadir}/applications/kde4/dngconverter.desktop
%{_kde4_datadir}/applications/kde4/kipiplugins.desktop
%{_kde4_datadir}/applications/kde4/expoblending.desktop
%{_kde4_datadir}/applications/kde4/panoramagui.desktop
%{_kde4_datadir}/applications/kde4/photolayoutseditor.desktop
%{_kde4_datadir}/applications/kde4/scangui.desktop
%{_kde4_datadir}/kde4/services/kipiplugin*.desktop
%{_kde4_iconsdir}/hicolor/*/actions/*
%{_kde4_iconsdir}/hicolor/*/apps/photolayoutseditor*
%{_kde4_iconsdir}/hicolor/*/apps/kipi-*
%{_kde4_iconsdir}/oxygen/*/apps/rawconverter*
%{_kde4_libdir}/kde4/kipiplugin_expoblending.so
%{_kde4_appsdir}/kipiplugin_expoblending/
%{_kde4_libdir}/kde4/kipiplugin_removeredeyes.so
%{_kde4_appsdir}/kipiplugin_removeredeyes/
%{_kde4_libdir}/kde4/kipiplugin_photolayoutseditor.so
%{_kde4_appsdir}/photolayoutseditor/
#%{_kde4_datadir}/config.kcfg/PLEConfigSkeleton.kcfgc
%{_kde4_datadir}/kde4/servicetypes/photolayoutseditor*.desktop
%{kde4_htmldir}/en/kipi-plugins/*
%{kde4_datadir}/locale/zh_*/LC_MESSAGES/kipiplugin_*.mo
%{kde4_plugindir}/kipiplugin_imageshackexport.so
%{kde4_plugindir}/kipiplugin_imgurexport.so
%{kde4_plugindir}/kipiplugin_wikimedia.so
%{kde4_datadir}/locale/zh_*/LC_MESSAGES/kipiplugins.mo
%{kde4_datadir}/templates/kipiplugins_photolayoutseditor/data/templates/a4/h/*.ple
%{kde4_plugindir}/kipiplugin_dlnaexport.so
%{kde4_plugindir}/libexec/digikamdatabaseserver
%{kde4_appsdir}/kipi/kipiplugin_*.rc
%{kde4_appsdir}/kipiplugin_dlnaexport/xml/*.xml
%exclude %{kde4_datadir}/locale/zh_CN/LC_MESSAGES/libkipi.mo
%exclude %{kde4_datadir}/locale/zh_TW/LC_MESSAGES/libkipi.mo

%post -n kipi-plugins-libs -p /sbin/ldconfig
%postun -n kipi-plugins-libs -p /sbin/ldconfig

%files -n kipi-plugins-libs
%{_kde4_libdir}/libkipiplugins.so.*


%changelog
* Fri Jul 18 2014 Liu Di <liudidi@gmail.com> - 4.1.0-2
- 为 Magic 3.0 重建

* Fri Jul 18 2014 Liu Di <liudidi@gmail.com> - 4.1.0-1
- 更新到 4.1.0

* Fri May 23 2014 Liu Di <liudidi@gmail.com> - 4.0.0-1
- 更新到 4.0.0

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 2.3.0-3
- 为 Magic 3.0 重建

* Tue Nov  8 2011 Alexey Kurov <nucleo@fedoraproject.org> - 2.3.0-2
- fix collision of digiKam icons with Oxygen

* Mon Nov  7 2011 Alexey Kurov <nucleo@fedoraproject.org> - 2.3.0-1
- digikam-2.3.0
- drop libpgf-api patch

* Sat Oct 29 2011 Alexey Kurov <nucleo@fedoraproject.org> - 2.2.0-2
- rebuild for libpgf-6.11.42
- bacport fix for changed libpgf API

* Tue Oct  4 2011 Alexey Kurov <nucleo@fedoraproject.org> - 2.2.0-1
- digikam-2.2.0
- drop libkvkontakte-libdir patch
- added photolayoutseditor in kipi-plugins

* Wed Sep 28 2011 Rex Dieter <rdieter@fedoraproject.org> 2.1.1-5
- include marble epoch in deps

* Mon Sep 26 2011 Alexey Kurov <nucleo@fedoraproject.org> - 2.1.1-4
- BR: pkgconfig(libpgf)

* Mon Sep 26 2011 Rex Dieter <rdieter@fedoraproject.org> 2.1.1-3
- pkgconfig-style deps

* Fri Sep 23 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> - 2.1.1-2
- BuildRequires: atlas-devel (for clapack, instead of the bundled version)
- fix FindCLAPACK.cmake to search %%{_libdir}/atlas
- patch matrix.cpp for the ATLAS clapack API

* Wed Sep 14 2011 Alexey Kurov <nucleo@fedoraproject.org> - 2.1.1-1
- digikam-2.1.1

* Fri Sep  9 2011 Alexey Kurov <nucleo@fedoraproject.org> - 2.1.0-1
- digikam-2.1.0
- drop qt_rasterengine patch
- add libkvkontakte subpkg

* Sun Aug 21 2011 Rex Dieter <rdieter@fedoraproject.org> 2.0.0-4
- rebuild (opencv)

* Thu Aug 18 2011 Rex Dieter <rdieter@fedoraproject.org> 2.0.0-3
- digikam crashes with "-graphicssystem raster" (#726971)

* Tue Aug 02 2011 Rex Dieter <rdieter@fedoraproject.org> 2.0.0-2
- new libkface, libkgeomap, libmediawiki subpkgs (#727570)
- remove rpm cruft (%%clean, %%defattr, Group:, BuildRoot:)

* Fri Jul 29 2011 Alexey Kurov <nucleo@fedoraproject.org> - 2.0.0-1
- digikam-2.0.0
- drop s390 patch included upstream
- bundled code not used by default (DIGIKAMSC_USE_PRIVATE_KDEGRAPHICS not defined)

* Thu Jul 07 2011 Rex Dieter <rdieter@fedoraproject.org> 2.0.0-0.2.rc
- use pkgconfig()-style deps for libkdcraw, libkexiv2, libkipi, libksane
- -libs: drop (versioned) dep on kdegraphics-libs

* Thu Jun 30 2011 Alexey Kurov <nucleo@fedoraproject.org> - 2.0.0-0.1.rc
- digikam-2.0.0-rc
- merge with kipi-plugins.spec

* Wed Jun 15 2011 Rex Dieter <rdieter@fedoraproject.org> 1.9.0-2
- rebuild (marble)

* Thu Mar 17 2011 Rex Dieter <rdieter@fedoraproject.org> 1.9.0-1
- 1.9.0

* Thu Mar 03 2011 Rex Dieter <rdieter@fedoraproject.org> 1.8.0-3
- use safer check for libjpeg version, using cmake_try_compile (kde#265431)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Feb 03 2011 Rex Dieter <rdieter@fedoraproject.org> 1.8.0-1
- 1.8.0

* Wed Dec 22 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.7.0-1
- digikam-1.7.0

* Tue Nov 23 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.6.0-1
- digikam-1.6.0 (#628156)

* Tue Nov 02 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.5.0-1.1
- -libs: add minimal kdegraphics-libs dep (#648741)

* Mon Oct 11 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.5.0-1
- digikam-1.5.0

* Wed Aug 25 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.4.0-1
- digikam-1.4.0

* Tue Jun 08 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.3.0-1
- digikam-1.3.0

* Tue Mar 30 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.2.0-2
- crash on startup in RatingWidget (kde#232628)

* Mon Mar 29 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.2.0-1
- digikam-1.2.0

* Mon Mar 22 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.1.0-3
- -libs: drop extraneous deps
- -devel: Req: kdelibs4-devel

* Wed Feb 10 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.1.0-2
- touch up marble-related deps

* Mon Feb 01 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.1.0-1
- digikam-1.1.0

* Thu Jan 28 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.0.0-2
- use %%{_kde4_version}

* Mon Dec 21 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.0.0-1
- digikam-1.0.0

* Mon Nov 30 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.0.0-0.11.rc
- digikam-1.0.0-rc

* Wed Nov 25 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.0.0-0.10.beta6
- rebuild (kdegraphics)

* Sat Nov 14 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.0.0-0.9.beta6
- digiKam not listed as a media handler for pictures in Nautilus (#516447)

* Mon Nov 08 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.0.0-0.8.beta6
- digikam-1.0.0-beta6

* Tue Oct 06 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.0.0-0.7.beta5
- digikam-1.0.0-beta5
- tweak marble deps (again)

* Tue Sep 29 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.0.0-0.6.beta4
- fix marble dep(s)

* Mon Aug 31 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.0.0-0.5.beta4
- digikam-1.0.0-beta4
- BR: liblqr-1-devel

* Wed Aug 05 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.0.0-0.4.beta3
- drop xdg-utils references 
- tighten -libs related deps via %%{?_isa}

* Fri Jul 24 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.0.0-0.3.beta3
- digikam-1.0.0-beta3

* Mon Jul 06 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.0.0-0.2.beta2
- digikam-1.0.0-beta2

* Fri Jun 12 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.0.0-0.1.beta1
- digikam-1.0.0-beta1

* Tue Mar 17 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.10.0-1
- digikam-0.10.0 (final)

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.0-0.18.rc2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb 14 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.10.0-0.17.rc2
- digikam-0.10.0-rc2

* Mon Feb 09 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.10.0-0.16.rc1
- Req: kdebase-runtime

* Wed Feb 04 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.10.0-0.15.rc1
- BR: kdeedu-devel >= 4.2.0, Req: kdeedu-marble >= 4.2.0
- add min Req: kdelibs4 dep too 

* Thu Jan 22 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.10-0-0.14.rc1
- digikam-0.10.0-rc1

* Mon Jan 12 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.10-0.13.beta8
- re-enable marble integration, kde42+ (bug #470578)

* Mon Jan 05 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.10.0-0.12.beta8
- digikam-0.10.0-beta8

* Mon Dec 22 2008 Rex Dieter <rdieter@fedoraproject.org> - 0.10.0-0.11.beta7
- BR: libkipi-devel >= 0.3.0

* Thu Dec 18 2008 Rex Dieter <rdieter@fedoraproject.org> - 0.10.0-0.9.beta7
- digikam-0.10.0-beta7

* Mon Dec 01 2008 Rex Dieter <rdieter@fedoraproject.org> - 0.10.0-0.8.beta6
- omit kde42 (icon) conflicts

* Tue Nov 25 2008 Rex Dieter <rdieter@fedoraproject.org> - 0.10.0-0.7.beta6
- digikam-0.10.0-beta6
- lensfun support

* Mon Oct 27 2008 Rex Dieter <rdieter@fedoraproject.org> - 0.10.0-0.6.beta5
- digikam-0.10.0-beta5

* Mon Oct 06 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0.10.0-0.5.beta4
- update to 0.10.0 beta 4
- build against latest kdegraphics

* Fri Sep 26 2008 Rex Dieter <rdieter@fedoraproject.org> - 0.10.0-0.4.beta3
- digikam-0.10.0-beta3

* Mon Aug 04 2008 Rex Dieter <rdieter@fedoraproject.org> - 0.10.0-0.3.beta2
- disable marble integration

* Sat Aug 02 2008 Rex Dieter <rdieter@fedoraproject.org> - 0.10.0-0.2.beta2
- omit conflicts with oxygen-icon-theme

* Thu Jul 31 2008 Rex Dieter <rdieter@fedoraproject.org> - 0.10.0-0.1.beta2
- digikam-0.10.0-beta2

* Fri Jul 18 2008 Rex Dieter <rdieter@fedoraproject.org> - 0.9.4-2
- --without-included-sqlite3, BR: sqlite-devel

* Thu Jul 17 2008 Rex Dieter <rdieter@fedoraproject.org> - 0.9.4-1
- digikam-0.9.4

* Mon Jul 07 2008 Marcin Garski <mgarski[AT]post.pl> 0.9.3-5
- Don't lose some photos during import (#448235)

* Fri Mar 14 2008 Rex Dieter <rdieter@fedoraproject.org> - 0.9.3-3
- respin (for libkdcraw)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.9.3-2
- Autorebuild for GCC 4.3

* Sat Dec 22 2007 Marcin Garski <mgarski[AT]post.pl> 0.9.3-1
- Update to 0.9.3
- BR: libkexiv2-devel >= 0.1.6 libkdcraw-devel >= 0.1.2

* Sat Dec 08 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.9.3-0.5.rc1
- digikam-0.9.3-rc1
- BR: kdelibs3-devel

* Thu Nov 20 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.9.3-0.2.beta3
- digikam-0.9.3-beta3

* Tue Nov 13 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.9.3-0.1.beta2
- digikam-0.9.3-beta2

* Tue Sep 18 2007 Marcin Garski <mgarski[AT]post.pl> 0.9.2-5
- Rebuild

* Wed Aug 29 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.9.3-4
- License: GPLv2+
- lcms patch (kde bug #148930)

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 0.9.2-3
- Rebuild for selinux ppc32 issue.

* Fri Jun 22 2007 Marcin Garski <mgarski[AT]post.pl> 0.9.2-2
- Create symlinks in pixmaps directory (#242978)

* Tue Jun 19 2007 Marcin Garski <mgarski[AT]post.pl> 0.9.2-1
- Update to version 0.9.2-final
- Remove digikam-0.9.2-beta3-fix-exiv2-dep.patch, merged upstream

* Wed Jun 06 2007 Marcin Garski <mgarski[AT]post.pl> 0.9.2-0.3.beta3
- Fix .desktop category

* Wed Jun 06 2007 Marcin Garski <mgarski[AT]post.pl> 0.9.2-0.2.beta3
- Fix broken compilation caused by Exiv2 dependency

* Tue Jun 05 2007 Marcin Garski <mgarski[AT]post.pl> 0.9.2-0.1.beta3
- Update to version 0.9.2-beta3 (merge with digikamimageplugins)
- Update description

* Mon May 14 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.9.1-3
- respin against libkexiv2-0.1.5
- preserve upstream .desktop vendor (f7 branch at least)

* Mon Apr 02 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.9.1-2
- exiv2-0.14 patch
- cleanup/simplify BR's,Requires,d-f-i usage

* Fri Mar 09 2007 Marcin Garski <mgarski[AT]post.pl> 0.9.1-1
- Update to version 0.9.1
- Update BuildRequires

* Mon Dec 18 2006 Marcin Garski <mgarski[AT]post.pl> 0.9.0-1
- Update to version 0.9.0

* Tue Nov 28 2006 Marcin Garski <mgarski[AT]post.pl> 0.9.0-0.2.rc1
- Rebuild

* Tue Nov 28 2006 Marcin Garski <mgarski[AT]post.pl> 0.9.0-0.1.rc1
- Update to version 0.9.0-rc1

* Fri Sep 01 2006 Marcin Garski <mgarski[AT]post.pl> 0.8.2-3
- Rebuild for Fedora Core 6

* Wed Aug 16 2006 Marcin Garski <mgarski[AT]post.pl> 0.8.2-2
- Release bump (#201756)

* Tue Aug 01 2006 Marcin Garski <mgarski[AT]post.pl> 0.8.2-1
- Update to version 0.8.2 (#200932)

* Tue Feb 14 2006 Marcin Garski <mgarski[AT]post.pl> 0.8.1-3
- Rebuild

* Wed Feb 08 2006 Marcin Garski <mgarski[AT]post.pl> 0.8.1-2
- Exclude x-raw.desktop (bug #179754)
- Don't own icons directory

* Mon Jan 23 2006 Marcin Garski <mgarski[AT]post.pl> 0.8.1-1
- Add --enable-final
- Remove GCC 4.1 patch, applied upstream
- Update to version 0.8.1

* Mon Jan 23 2006 Marcin Garski <mgarski[AT]post.pl> 0.8.0-16
- Add some stuff to BuildRequires (finally fix bug #178031)

* Tue Jan 17 2006 Marcin Garski <mgarski[AT]post.pl> 0.8.0-15
- Remove redundant BuildRequires (bug #178031)

* Mon Jan 16 2006 Marcin Garski <mgarski[AT]post.pl> 0.8.0-14
- Remove --disable-dependency-tracking

* Mon Jan 16 2006 Marcin Garski <mgarski[AT]post.pl> 0.8.0-13
- Remove --enable-final (caused compilation errors)

* Sun Jan 15 2006 Marcin Garski <mgarski[AT]post.pl> 0.8.0-12
- Change "/etc/profile.d/qt.sh" to "%%{_sysconfdir}/profile.d/qt.sh"
- Add --disable-dependency-tracking & --enable-final

* Wed Dec 14 2005 Marcin Garski <mgarski[AT]post.pl> 0.8.0-11
- Add libart_lgpl-devel and gamin-devel to BR

* Wed Dec 14 2005 Marcin Garski <mgarski[AT]post.pl> 0.8.0-10
- Add libacl-devel to BR

* Wed Dec 14 2005 Marcin Garski <mgarski[AT]post.pl> 0.8.0-9
- Add libidn-devel to BR

* Wed Dec 14 2005 Marcin Garski <mgarski[AT]post.pl> 0.8.0-8
- Fix compile on GCC 4.1

* Tue Dec 13 2005 Marcin Garski <mgarski[AT]post.pl> 0.8.0-7
- Remove autoreconf

* Tue Dec 13 2005 Marcin Garski <mgarski[AT]post.pl> 0.8.0-6
- Remove patch

* Tue Dec 13 2005 Marcin Garski <mgarski[AT]post.pl> 0.8.0-5
- Last chance to make it right (modular X.Org)

* Tue Dec 13 2005 Marcin Garski <mgarski[AT]post.pl> 0.8.0-4
- Try to build for modular X.Org

* Tue Dec 13 2005 Marcin Garski <mgarski[AT]post.pl> 0.8.0-3
- Add new paths for modular X.Org

* Fri Dec 09 2005 Marcin Garski <mgarski[AT]post.pl> 0.8.0-2
- Work around for modular X.Org paths

* Thu Dec 01 2005 Marcin Garski <mgarski[AT]post.pl> 0.8.0-1
- Add description about digikamimageplugins and kipi-plugins
- Remove 64 bit patch, applied upstream
- Update to version 0.8.0

* Sat Oct 22 2005 Marcin Garski <mgarski[AT]post.pl> 0.7.4-4
- Exclude libdigikam.la (bug #171503)

* Sat Sep 17 2005 Marcin Garski <mgarski[AT]post.pl> 0.7.4-3
- Change confusing warning about Big Endian Platform

* Tue Sep 13 2005 Marcin Garski <mgarski[AT]post.pl> 0.7.4-2
- Spec improvements

* Mon Sep 12 2005 Marcin Garski <mgarski[AT]post.pl> 0.7.4-1
- Updated to version 0.7.4 & clean up for Fedora Extras

* Sat Jun 26 2004 Marcin Garski <mgarski[AT]post.pl> 0.6.2-1.fc2
- Updated to version 0.6.2

* Wed Jun 09 2004 Marcin Garski <mgarski[AT]post.pl> 0.6.2RC-1.fc2
- Initial specfile
