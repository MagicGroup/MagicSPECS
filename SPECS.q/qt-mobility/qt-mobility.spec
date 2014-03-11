
# options
#define examples 1 

%define snap 20120224git

Name:    qt-mobility
Version: 1.2.2
Release: 0.3.%{snap}%{?dist}
Summary: Qt Mobility Framework
Group:   System Environment/Libraries
License: LGPLv2 with exceptions
URL:     http://qt.nokia.com/products/qt-addons/mobility 
%if 0%{?snap:1}
# git clone git://gitorious.org/qt-mobility/qt-mobility.git
# cd qt-mobility; git archive --prefix=qt-mobility-opensource-src-1.2.0/ master | xz -9 >  qt-mobility-opensources-src-1.2.0-20110922.tar.xz
Source0: qt-mobility-opensource-src-%{version}-%{snap}.tar.xz
%else
Source0: http://get.qt.nokia.com/qt/add-ons/qt-mobility-opensource-src-%{version}.tar.gz
%endif
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Provides: qt4-mobility = %{version}-%{release}
Provides: qt4-mobility%{?_isa} = %{version}-%{release}

## upstreamable patches
Patch50: qt-mobility-opensource-src-1.2.0-translationsdir.patch
# add pkgconfig for linux-* platforms too
Patch51: qt-mobility-opensource-src-1.2.0-pkgconfig.patch
# gcc 4.7, missing unistd.h for getppid
Patch52: qt-mobility-opensource-src-1.2.0-include-unistdh.patch
# dso
Patch53: qt-mobility-opensource-src-1.1.0-pulseaudio-lib.patch
# -fpermissive hack around failed bluez checks
# see also https://bugzilla.redhat.com/show_bug.cgi?id=797266
#Patch54: qt-mobility-opensource-src-1.2.2-bluez_gcc47.patch

## upstream patches

BuildRequires: chrpath
BuildRequires: pkgconfig(alsa)
BuildRequires: pkgconfig(blkid)
BuildRequires: pkgconfig(bluez)
BuildRequires: pkgconfig(gstreamer-plugins-bad-0.10) 
BuildRequires: pkgconfig(gstreamer-app-0.10)
BuildRequires: pkgconfig(libpulse)
BuildRequires: pkgconfig(libudev)
BuildRequires: pkgconfig(NetworkManager)
BuildRequires: pkgconfig(QtCore) pkgconfig(QtGui) pkgconfig(QtOpenGL)
BuildRequires: pkgconfig(xv)

## under review, http://bugzilla.redhat.com/626122
# BuildRequires: libqmf-devel >= 1.0

%{?_qt4_version:Requires: qt4%{?_isa} >= %{_qt4_version}}

%description
Qt Mobility Project delivers a set of new APIs to Qt with features that are well
known from the mobile device world, in particular phones. However, these APIs
allow the developer to use these features with ease from one framework and apply
them to phones, netbooks and non-mobile personal computers. The framework not
only improves many aspects of a mobile experience, because it improves the use
of these technologies, but has applicability beyond the mobile device arena.

%package devel
Summary: Qt Mobility Framework development files
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: qt4-devel
Provides: qt4-mobility-devel = %{version}-%{release}
Provides: qt4-mobility-devel%{?_isa} = %{version}-%{release}
Provides: %{name}-messaging-devel = %{version}-%{release}
Provides: %{name}-bearer-devel = %{version}-%{release}
Provides: %{name}-versit-devel = %{version}-%{release}
Provides: %{name}-contacts-devel = %{version}-%{release}
Provides: %{name}-location-devel = %{version}-%{release}
Provides: %{name}-multimedia-devel = %{version}-%{release}
Provides: %{name}-publishsubscribe-devel = %{version}-%{release}
Provides: %{name}-sensors-devel = %{version}-%{release}
Provides: %{name}-serviceframework-devel = %{version}-%{release}
Provides: %{name}-systeminfo-devel = %{version}-%{release}
%description devel
%{summary}.

%package doc
Summary: API documentation for %{name}
Group: Documentation
Requires: qt4
BuildArch: noarch
%description doc
%{summary}.

%package examples
Summary: Qt Mobility Framework examples
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
%description examples
%{summary}.


%prep
%setup -q -n %{name}-opensource-src-%{version}

%patch50 -p1 -b .translationsdir
%patch51 -p1 -b .pkgconfig
%patch52 -p1 -b .include-unistdh
%patch53 -p1 -b .pulseaudio_lib
#patch54 -p1 -b .bluez_gcc47


%build
PATH=%{_qt4_bindir}:$PATH; export PATH

./configure \
  -prefix %{_qt4_prefix} \
  -bindir %{_bindir} \
  -headerdir %{_qt4_headerdir} \
  -libdir %{_qt4_libdir} \
  -plugindir %{_qt4_plugindir} \
  -qmake-exec %{_qt4_qmake} \
  -release \
  %{?examples:-examples} 

make %{?_smp_mflags} 

make %{?_smp_mflags} qch_docs


%install
rm -rf %{buildroot}

make install INSTALL_ROOT=%{buildroot} 

# manually install docs
install -p -m644 -D doc/qch/qtmobility.qch %{buildroot}%{_qt4_docdir}/qch/qtmobility.qch
mkdir -p %{buildroot}%{_qt4_docdir}/html/qtmobility
cp -a doc/html/* %{buildroot}%{_qt4_docdir}/html/qtmobility/

## WTF, translations went awol in 1.1.0 ?  -- Rex
#find_lang %{name} --all-name --with-qt --without-mo

# die rpath, die
chrpath --delete %{buildroot}%{_bindir}/* ||:
chrpath --delete %{buildroot}%{_qt4_libdir}/libQt*.so ||:
chrpath --delete %{buildroot}%{_qt4_plugindir}/*/*.so ||:
chrpath --delete %{buildroot}%{_qt4_importdir}/*/*.so ||:
chrpath --delete %{buildroot}%{_qt4_importdir}/*/*/*.so ||:
magic_rpm_clean.sh

%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files 
%defattr(-,root,root,-)
%doc LICENSE.LGPL LGPL_EXCEPTION.txt
%{_qt4_libdir}/libQtBearer.so.1*
%{_qt4_libdir}/libQtContacts.so.1*
%{_qt4_libdir}/libQtConnectivity.so.1*
%{_qt4_libdir}/libQtFeedback.so.1*
%{_qt4_libdir}/libQtGallery.so.1*
%{_qt4_libdir}/libQtLocation.so.1*
%{_qt4_libdir}/libQtMultimediaKit.so.1*
%{_qt4_libdir}/libQtOrganizer.so.1*
%{_qt4_libdir}/libQtPublishSubscribe.so.1*
%{_qt4_libdir}/libQtSensors.so.1*
%{_qt4_libdir}/libQtServiceFramework.so.1*
%{_qt4_libdir}/libQtSystemInfo.so.1*
%{_qt4_libdir}/libQtVersit.so.1*
%{_qt4_libdir}/libQtVersitOrganizer.so.1*
%{_qt4_importdir}/QtMobility/
%{_qt4_importdir}/QtMultimediaKit/
%{_qt4_plugindir}/*

%files devel
%defattr(-,root,root,-)
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
%defattr(-,root,root,-)
%{_qt4_docdir}/qch/qtmobility.qch
%{_qt4_docdir}/html/qtmobility/

%if 0%{?examples}
%files examples
%defattr(-,root,root,-)
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
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 1.2.2-0.3.20120224git
- 为 Magic 3.0 重建

* Fri Jul 06 2012 Liu Di <liudidi@gmail.com> - 1.2.2-0.2.20120224git
- 为 Magic 3.0 重建

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

