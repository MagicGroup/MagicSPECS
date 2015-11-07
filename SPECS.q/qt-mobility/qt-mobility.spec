
# options
#define examples 1

%define git_long  169da60c8f657b3b61309c0a570d296107181411
%define git_short 169da60c
%define snap 20140317

Name:    qt-mobility
Summary: Qt Mobility Framework
Version: 1.2.2
Release: 0.22.%{snap}git%{git_short}%{?dist}

License: LGPLv2 with exceptions
URL:     http://qt.digia.com/Product/Qt-Add-Ons/
%if 0%{?snap:1}
# git clone git://gitorious.org/qt-mobility/qt-mobility.git
# cd qt-mobility; git archive --prefix=qt-mobility-opensource-src-%{version}/ %{git_long} | xz -9 >  qt-mobility-opensources-src-%{version}-%{git_short}.tar.xz
Source0: qt-mobility-opensource-src-%{version}-%{git_short}.tar.xz
%else
Source0: http://get.qt.nokia.com/qt/add-ons/qt-mobility-opensource-src-%{version}.tar.gz
%endif

Provides: qt4-mobility = %{version}-%{release}
Provides: qt4-mobility%{?_isa} = %{version}-%{release}

## local patches
# kill rpath
Patch1: qt-mobility-opensource-src-1.2.2-no_rpath.patch

## upstreamable patches
Patch50: qt-mobility-opensource-src-1.2.0-translationsdir.patch
# add pkgconfig for linux-* platforms too, Requires.private: QtCore
Patch51: qt-mobility-opensource-src-1.2.2-pkgconfig.patch
# fix ftbfs in sensors doc
Patch52: qt-mobility-opensource-src-1.2.2-sensors_ftbfs.patch
# dso
Patch53: qt-mobility-opensource-src-1.1.0-pulseaudio-lib.patch

## upstream patches

BuildRequires: pkgconfig(alsa)
BuildRequires: pkgconfig(blkid)
BuildRequires: pkgconfig(bluez)
BuildRequires: pkgconfig(gstreamer-plugins-bad-0.10) 
BuildRequires: pkgconfig(gstreamer-app-0.10)
BuildRequires: pkgconfig(libpulse)
%if 0%{?fedora} || 0%{?rhel} > 6
BuildRequires: pkgconfig(libudev)
%endif
BuildRequires: pkgconfig(NetworkManager)
BuildRequires: pkgconfig(QtCore)
BuildRequires: pkgconfig(QtDeclarative)
BuildRequires: pkgconfig(QtGui) pkgconfig(QtOpenGL)
BuildRequires: pkgconfig(QtNetwork) >= 4.7
BuildRequires: pkgconfig(xv)
BuildRequires: proj-devel

Provides: qt4-mobility = %{version}-%{release}
Provides: qt4-mobility%{?_isa} = %{version}-%{release}

# base metapackage pulls in split stuff for upgrade path
Requires: %{name}-bearer%{?_isa} = %{version}-%{release}
Requires: %{name}-connectivity%{?_isa} = %{version}-%{release}
Requires: %{name}-feedback%{?_isa} = %{version}-%{release}
Requires: %{name}-gallery%{?_isa} = %{version}-%{release}
Requires: %{name}-location%{?_isa} = %{version}-%{release}
Requires: %{name}-multimediakit%{?_isa} = %{version}-%{release}
Requires: %{name}-pim%{?_isa} = %{version}-%{release}
#Requires: %{name}-contacts%{?_isa} = %{version}-%{release}
#Requires: %{name}-organizer%{?_isa} = %{version}-%{release}
#Requires: %{name}-versit%{?_isa} = %{version}-%{release}
Requires: %{name}-publishsubscribe%{?_isa} = %{version}-%{release}
Requires: %{name}-sensors%{?_isa} = %{version}-%{release}
Requires: %{name}-serviceframework%{?_isa} = %{version}-%{release}
Requires: %{name}-systeminfo%{?_isa} = %{version}-%{release}

%description
Qt Mobility Project delivers a set of new APIs to Qt with features that are well
known from the mobile device world, in particular phones. However, these APIs
allow the developer to use these features with ease from one framework and apply
them to phones, netbooks and non-mobile personal computers. The framework not
only improves many aspects of a mobile experience, because it improves the use
of these technologies, but has applicability beyond the mobile device arena.

%package common
Summary: Common files for %{name}
%{?_qt4_version:Requires: qt4%{?_isa} >= %{_qt4_version}}
%description common
%{summary}.

%package devel
Summary: Qt Mobility Framework development files
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: qt4-devel
Provides: qt4-mobility-devel = %{version}-%{release}
Provides: qt4-mobility-devel%{?_isa} = %{version}-%{release}
Provides: %{name}-bearer-devel = %{version}-%{release}
Provides: %{name}-connectivity-devel = %{version}-%{release}
Provides: %{name}-contacts-devel = %{version}-%{release}
Provides: %{name}-feedback-devel = %{version}-%{release}
Provides: %{name}-gallery-devel = %{version}-%{release}
Provides: %{name}-location-devel = %{version}-%{release}
Provides: %{name}-multimediakit-devel = %{version}-%{release}
Provides: %{name}-organizer-devel = %{version}-%{release}
Provides: %{name}-publishsubscribe-devel = %{version}-%{release}
Provides: %{name}-sensors-devel = %{version}-%{release}
Provides: %{name}-serviceframework-devel = %{version}-%{release}
Provides: %{name}-systeminfo-devel = %{version}-%{release}
Provides: %{name}-versit-devel = %{version}-%{release}
%description devel
%{summary}.

%package doc
Summary: API documentation for %{name}
Requires: qt4
BuildArch: noarch
%description doc
%{summary}.

%package examples
Summary: Qt Mobility Framework examples
Requires: %{name}%{?_isa} = %{version}-%{release}
%description examples
%{summary}.

%package bearer
Summary: QtBearer support
Requires: %{name}-common%{?_isa} = %{version}-%{release}
%description bearer
%{summary}.

%package connectivity
Summary: QtConnectivity support
Requires: %{name}-common%{?_isa} = %{version}-%{release}
%description connectivity
%{summary}.

%package contacts
Summary: QtContacts support
Requires: %{name}-common%{?_isa} = %{version}-%{release}
Requires: %{name}-serviceframework%{?_isa} = %{version}-%{release}
Requires: %{name}-versit%{?_isa} = %{version}-%{release}
%description contacts
%{summary}.

%package feedback
Summary: QtFeedback support
Requires: %{name}-common%{?_isa} = %{version}-%{release}
Requires: %{name}-multimediakit%{?_isa} = %{version}-%{release}
%description feedback
%{summary}.

%package gallery
Summary: QtGallery support
Requires: %{name}-common%{?_isa} = %{version}-%{release}
%description gallery
%{summary}.

%package location
Summary: QtLocation support
Requires: %{name}-common%{?_isa} = %{version}-%{release}
%description location
%{summary}.

%package multimediakit
Summary: QtMultiMediaKit support
Requires: %{name}-common%{?_isa} = %{version}-%{release}
%description multimediakit
%{summary}.

%package organizer
Summary: QtOrganizer support
Requires: %{name}-common%{?_isa} = %{version}-%{release}
Requires: %{name}-contacts%{?_isa} = %{version}-%{release}
Requires: %{name}-versit%{?_isa} = %{version}-%{release}
%description organizer
%{summary}.

# Combine these items since they are (currently) interdependant anyway
%package pim
Summary: Qt Mobility Personal Information Management support
Requires: %{name}-common%{?_isa} = %{version}-%{release}
## contacts
Provides: %{name}-contacts%{?_isa} = %{version}-%{release}
Requires: %{name}-serviceframework%{?_isa} = %{version}-%{release}
#Requires: %{name}-versit%{?_isa} = %{version}-%{release}
## organizer
Provides: %{name}-organizer%{?_isa} = %{version}-%{release}
#Requires: %{name}-contacts%{?_isa} = %{version}-%{release}
#Requires: %{name}-versit%{?_isa} = %{version}-%{release}
## versit
Provides: %{name}-versit%{?_isa} = %{version}-%{release}
#Requires: %{name}-contacts%{?_isa} = %{version}-%{release}
#Requires: %{name}-organizer%{?_isa} = %{version}-%{release}
%description pim
%{summary}, including:
QtContacts, QtOrganzier, QtVersit, QtVersitOrganizer.

%package publishsubscribe
Summary: QtPublishSubscribe support
Requires: %{name}-common%{?_isa} = %{version}-%{release}
%description publishsubscribe
%{summary}.

%package sensors
Summary: QtSensors support
Requires: %{name}-common%{?_isa} = %{version}-%{release}
%description sensors
%{summary}.

%package serviceframework
Summary: QtServiceFramework support
Requires: %{name}-common%{?_isa} = %{version}-%{release}
%description serviceframework
%{summary}.

%package systeminfo
Summary: QtSystemInfo support
Requires: %{name}-common%{?_isa} = %{version}-%{release}
%description systeminfo
%{summary}.

%package versit
Summary: QtVersit and QtVersitOrganzier support
Requires: %{name}-common%{?_isa} = %{version}-%{release}
Requires: %{name}-contacts%{?_isa} = %{version}-%{release}
Requires: %{name}-organizer%{?_isa} = %{version}-%{release}
%description versit
%{summary}.


%prep
%setup -q -n %{name}-opensource-src-%{version}
rm -r src/3rdparty/proj

%patch1 -p1 -b .no_rpath
%patch50 -p1 -b .translationsdir
%patch51 -p1 -b .pkgconfig
%patch52 -p1 -b .sensors_ftbfs
%patch53 -p1 -b .pulseaudio_lib


%build
PATH=%{_qt4_bindir}:$PATH; export PATH

./configure \
  -prefix %{_qt4_prefix} \
  -bindir %{_bindir} \
  -headerdir %{_qt4_headerdir} \
  -languages "ar cs da de es fr he hu ja ko pl pt ru sk sl sv uk zh_CN zh_TW" \
  -libdir %{_qt4_libdir} \
  -plugindir %{_qt4_plugindir} \
  -qmake-exec %{_qt4_qmake} \
  -release \
  %{?examples:-examples} 

make %{?_smp_mflags} 

make %{?_smp_mflags} qch_docs


%install
make install INSTALL_ROOT=%{buildroot} 

# manually install docs
install -p -m644 -D doc/qch/qtmobility.qch %{buildroot}%{_qt4_docdir}/qch/qtmobility.qch
mkdir -p %{buildroot}%{_qt4_docdir}/html/qtmobility
cp -a doc/html/* %{buildroot}%{_qt4_docdir}/html/qtmobility/

%find_lang %{name} --all-name --with-qt --without-mo


%files
# empty metapackage

%files common -f %{name}.lang
%doc LICENSE.LGPL LGPL_EXCEPTION.txt
%dir %{_qt4_importdir}/QtMobility/

%post bearer -p /sbin/ldconfig
%postun bearer -p /sbin/ldconfig

%files bearer
%{_qt4_libdir}/libQtBearer.so.1*

%post connectivity -p /sbin/ldconfig
%postun connectivity -p /sbin/ldconfig

%files connectivity
%{_qt4_libdir}/libQtConnectivity.so.1*
%{_qt4_importdir}/QtMobility/connectivity/

%post feedback -p /sbin/ldconfig
%postun feedback -p /sbin/ldconfig

%files feedback
%{_qt4_libdir}/libQtFeedback.so.1*
%{_qt4_importdir}/QtMobility/feedback/
%{_qt4_plugindir}/feedback/

%post gallery -p /sbin/ldconfig
%postun gallery -p /sbin/ldconfig

%files gallery
%{_qt4_libdir}/libQtGallery.so.1*
%{_qt4_importdir}/QtMobility/gallery/

%post location -p /sbin/ldconfig
%postun location -p /sbin/ldconfig

%files location
%{_qt4_libdir}/libQtLocation.so.1*
%{_qt4_importdir}/QtMobility/location/
%{_qt4_plugindir}/geoservices/
%{_qt4_plugindir}/landmarks/

%post multimediakit -p /sbin/ldconfig
%postun multimediakit -p /sbin/ldconfig

%files multimediakit
%{_qt4_libdir}/libQtMultimediaKit.so.1*
%{_qt4_importdir}/QtMultimediaKit/
%{_qt4_plugindir}/audio/
%{_qt4_plugindir}/mediaservice/
%{_qt4_plugindir}/playlistformats/

%post pim -p /sbin/ldconfig
%postun pim -p /sbin/ldconfig

%files pim
#files contacts
%{_qt4_libdir}/libQtContacts.so.1*
%{_qt4_importdir}/QtMobility/contacts/
%{_qt4_plugindir}/contacts/
#files organizer
%{_qt4_libdir}/libQtOrganizer.so.1*
%{_qt4_importdir}/QtMobility/organizer/
#files versit
%{_qt4_libdir}/libQtVersit.so.1*
%{_qt4_libdir}/libQtVersitOrganizer.so.1*
%{_qt4_plugindir}/versit/

%post publishsubscribe -p /sbin/ldconfig
%postun publishsubscribe -p /sbin/ldconfig

%files publishsubscribe
%{_qt4_libdir}/libQtPublishSubscribe.so.1*
%{_qt4_importdir}/QtMobility/publishsubscribe/

%post sensors -p /sbin/ldconfig
%postun sensors -p /sbin/ldconfig

%files sensors
%{_qt4_libdir}/libQtSensors.so.1*
%{_qt4_importdir}/QtMobility/sensors/
%{_qt4_plugindir}/sensorgestures/
%{_qt4_plugindir}/sensors/

%post serviceframework -p /sbin/ldconfig
%postun serviceframework -p /sbin/ldconfig

%files serviceframework
%{_qt4_libdir}/libQtServiceFramework.so.1*
%{_qt4_importdir}/QtMobility/serviceframework/

%post systeminfo -p /sbin/ldconfig
%postun systeminfo -p /sbin/ldconfig

%files systeminfo
%{_qt4_libdir}/libQtSystemInfo.so.1*
%{_qt4_importdir}/QtMobility/systeminfo/

%files devel
%{_bindir}/icheck
%{_bindir}/ndefhandlergen
%{_bindir}/qcrmlgen
%{_bindir}/servicedbgen
%{_bindir}/servicefw
%{_bindir}/servicexmlgen
%{_bindir}/vsexplorer
%{_qt4_prefix}/mkspecs/features/mobility.prf
%{_qt4_prefix}/mkspecs/features/mobilityconfig.prf 
%{_qt4_headerdir}/Qt*/
%{_qt4_libdir}/libQt*.prl
%{_qt4_libdir}/libQt*.so
%{_qt4_libdir}/pkgconfig/Qt*.pc

%files doc
%{_qt4_docdir}/qch/qtmobility.qch
%{_qt4_docdir}/html/qtmobility/

%if 0%{?examples}
%files examples
%{_qt4_bindir}/arrowkeys
%{_qt4_bindir}/audiodevices
%{_qt4_bindir}/audioinput
%{_qt4_bindir}/audiooutput
%{_qt4_bindir}/audiorecorder
%{_qt4_bindir}/battery-publisher
%{_qt4_bindir}/battery-subscriber
%{_qt4_bindir}/bearercloud
%{_qt4_bindir}/bearermonitor
%{_qt4_bindir}/cubehouse
%{_qt4_bindir}/flickrdemo
%{_qt4_bindir}/grueapp
%{_qt4_bindir}/logfilepositionsource
%{_qt4_bindir}/metadata
%{_qt4_bindir}/nmealog.txt
%{_qt4_bindir}/orientation
%{_qt4_bindir}/publish-subscribe
%{_qt4_bindir}/radio
%{_qt4_bindir}/samplephonebook
%{_qt4_bindir}/satellitedialog
%{_qt4_bindir}/sensor_explorer
%{_qt4_bindir}/servicebrowser
%{_qt4_bindir}/sfw-notes
%{_qt4_bindir}/show_acceleration
%{_qt4_bindir}/show_als
%{_qt4_bindir}/show_compass
%{_qt4_bindir}/show_magneticflux
%{_qt4_bindir}/show_orientation
%{_qt4_bindir}/show_proximity
%{_qt4_bindir}/show_rotation
%{_qt4_bindir}/show_tap
%{_qt4_bindir}/simplelog.txt
%{_qt4_bindir}/slideshow
%{_qt4_bindir}/videographicsitem
%{_qt4_bindir}/videowidget
%{_qt4_bindir}/xmldata
%{_qt4_plugindir}/serviceframework/libserviceframework_voipdialerservice.so
%{_qt4_plugindir}/serviceframework/libserviceframework_landlinedialerservice.so
%{_qt4_plugindir}/serviceframework/libserviceframework_filemanagerplugin.so
%{_qt4_plugindir}/serviceframework/libserviceframework_bluetoothtransferplugin.so
%{_qt4_plugindir}/serviceframework/libserviceframework_notesmanagerplugin.so
%{_qt4_plugindir}/sensors/libqtsensors_grueplugin.so
%endif


%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 1.2.2-0.22.20140317git169da60c
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-0.21.20140317git169da60c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.2.2-0.20.20140317git169da60c
- Rebuilt for GCC 5 C++11 ABI change

* Wed Mar 11 2015 Rex Dieter <rdieter@fedoraproject.org> 1.2.2-0.19.20140317git169da60c
- rebuild (proj)

* Wed Feb 18 2015 Rex Dieter <rdieter@fedoraproject.org> 1.2.2-0.18.20140317git169da60c
- rebuild (gcc5)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-0.17.20140317git169da60c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-0.16.20140317git169da60c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Jun 07 2014 Rex Dieter <rdieter@fedoraproject.org> 1.2.2-0.15.20140317git169da60c
- revert proj workaround, postinstaller's google-earth packaging is fixed

* Wed Jun 04 2014 Rex Dieter <rdieter@fedoraproject.org> 1.2.2-0.14.20140317git169da60c
- update no_rpath patch for -examples too (which isn't enabled by default yet)

* Wed Jun 04 2014 Rex Dieter <rdieter@fedoraproject.org> 1.2.2-0.13.20140317git169da60c
- -location: add explicit 'Requires: proj' to workaround google-earth packaging bug (kde#335751)

* Fri May 02 2014 Rex Dieter <rdieter@fedoraproject.org> 1.2.2-0.12.20140317git169da60c
- update URL

* Mon Apr 28 2014 Rex Dieter <rdieter@fedoraproject.org> - 1.2.2-0.11.20140317git169da60c
- split packaging
- (re)enable translations
- better rpath handling

* Mon Apr 28 2014 Rex Dieter <rdieter@fedoraproject.org> 1.2.2-0.10.20140317git169da60c
- fresh snapshot

* Mon Apr 28 2014 Rex Dieter <rdieter@fedoraproject.org> 1.2.2-0.9.20120224git
- .spec cleanup, pkgconfig: +Requires.private: QtCore

* Wed Mar 19 2014 Ville Skyttä <ville.skytta@iki.fi> - 1.2.2-0.8.20120224git
- Use system proj instead of bundled one

* Sat Mar 08 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> 1.2.2-0.7.20120224git
- rebuild against fixed qt to fix -debuginfo (#1074041)

* Fri Oct 25 2013 Rex Dieter <rdieter@fedoraproject.org> 1.2.2-0.6.20120224git
- BR: pkgconfig(QtNetwork) >= 4.7
- omit udev support on el6 (ftbfs)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-0.5.20120224git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-0.4.20120224git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-0.3.20120224git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 14 2012 Rex Dieter <rdieter@fedoraproject.org> 1.2.2-0.2.20120224git
- rebuild for newer libudev/systemd (#831991) 

* Fri Feb 24 2012 Rex Dieter <rdieter@fedoraproject.org> 1.2.2-0.1.20120224git
- 1.2.2 20120224git snapshot

* Fri Feb 24 2012 Rex Dieter <rdieter@fedoraproject.org> 1.2.0-9.20110922
- build in release mode

* Fri Feb 24 2012 Jaroslav Reznik <jreznik@redhat.com> - 1.2.0-8.20110922
- fix FTBFS because of missing unistd.h include

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-7.20110922
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Oct 29 2011 Rex Dieter <rdieter@fedoraproject.org> 1.2.0-6.20110922
- add pkgconfig support

* Thu Sep 22 2011 Rex Dieter <rdieter@fedoraproject.org> 1.2.0-5.20110922
- 20110922 snapshot
- use pkgconfig-style deps

* Wed Jul 20 2011 Rex Dieter <rdieter@fedoraproject.org> 1.2.0-4
- rebuild (qt48)

* Mon May 23 2011 Rex Dieter <rdieter@fedoraproject.org> 1.2.0-3
- drop BR: qt4-webkit-devel
- BR: libXv-devel

* Tue May 17 2011 Rex Dieter <rdieter@fedoraproject.org> 1.2.0-2
- BR: libudev-devel
- BR: gstreamer-plugins-bad-free-devel gstreamer-plugins-base-devel

* Fri May 13 2011 Jaroslav Reznik <jreznik@redhat.com> 1.2.0-1
- 1.2.0

* Mon May 09 2011 Jaroslav Reznik <jreznik@redhat.com> 1.1.3-1
- 1.1.3

* Tue Apr 19 2011 Rex Dieter <rdieter@fedoraproject.org> 1.1.1-1
- 1.1.1

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 09 2010 Rex Dieter <rdieter@fedoraproject.org> 1.1.0-1
- 1.1.0

* Wed Jul 14 2010 Rex Dieter <rdieter@fedoraproject.org> 1.0.1-3
- License: LGPLv2 ...
- -doc subpkg

* Wed Jul 14 2010 Rex Dieter <rdieter@fedoraproject.org> 1.0.1-2
- 1.0.1 (first try, based on work by heliocastro)

