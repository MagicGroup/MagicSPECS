
%global qt_module qtmultimedia

# define to build docs, need to undef this for bootstrapping
# where qt5-qttools builds are not yet available
%define docs 1

Summary: Qt5 - Multimedia support
Name:    qt5-%{qt_module}
Version: 5.2.1
Release: 1%{?dist}

# See LGPL_EXCEPTIONS.txt, LICENSE.GPL3, respectively, for exception details
License: LGPLv2 with exceptions or GPLv3 with exceptions
Url: http://qt-project.org/
%if 0%{?pre:1}
Source0: http://download.qt-project.org/development_releases/qt/5.2/%{version}-%{pre}/submodules/%{qt_module}-opensource-src-%{version}-%{pre}.tar.xz
%else
Source0: http://download.qt-project.org/official_releases/qt/5.2/%{version}/submodules/%{qt_module}-opensource-src-%{version}.tar.xz
%endif

BuildRequires: qt5-qtbase-devel >= %{version}
BuildRequires: qt5-qtdeclarative-devel >= %{version}
BuildRequires: pkgconfig(alsa)
BuildRequires: pkgconfig(gstreamer-0.10)
BuildRequires: pkgconfig(gstreamer-app-0.10)
BuildRequires: pkgconfig(gstreamer-audio-0.10)
BuildRequires: pkgconfig(gstreamer-base-0.10)
BuildRequires: pkgconfig(gstreamer-interfaces-0.10)
BuildRequires: pkgconfig(gstreamer-pbutils-0.10)
BuildRequires: pkgconfig(gstreamer-plugins-bad-0.10)
BuildRequires: pkgconfig(gstreamer-video-0.10)
BuildRequires: pkgconfig(libpulse) pkgconfig(libpulse-mainloop-glib)
BuildRequires: pkgconfig(openal)
BuildRequires: pkgconfig(xv)

%{?_qt5_version:Requires: qt5-qtbase%{?_isa} >= %{_qt5_version}}

%description
The Qt Multimedia module provides a rich feature set that enables you to
easily take advantage of a platforms multimedia capabilites and hardware.
This ranges from the playback and recording of audio and video content to
the use of available devices like cameras and radios.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: qt5-qtbase-devel%{?_isa}
Requires: qt5-qtdeclarative-devel%{?_isa}
%description devel
%{summary}.

%if 0%{?docs}
%package doc
Summary: API documentation for %{name}
Requires: %{name} = %{version}-%{release}
# for qhelpgenerator
BuildRequires: qt5-qttools-devel
BuildArch: noarch
%description doc
%{summary}.
%endif

%package examples
Summary: Programming examples for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
%description examples
%{summary}.


%prep
%setup -q -n %{qt_module}-opensource-src-%{version}%{?pre:-%{pre}}


%build
%{_qt5_qmake}

make %{?_smp_mflags}
%if 0%{?docs}
make %{?_smp_mflags} docs
%endif


%install
make install INSTALL_ROOT=%{buildroot}

%if 0%{?docs}
make install_docs INSTALL_ROOT=%{buildroot}
%endif

## .prl file love (maybe consider just deleting these -- rex
# nuke dangling reference(s) to %%buildroot, excessive (.la-like) libs
sed -i \
  -e "/^QMAKE_PRL_BUILD_DIR/d" \
  -e "/^QMAKE_PRL_LIBS/d" \
  %{buildroot}%{_qt5_libdir}/*.prl

## unpackaged files
# .la files, die, die, die.
rm -fv %{buildroot}%{_qt5_libdir}/lib*.la

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc LGPL_EXCEPTION.txt LICENSE.GPL LICENSE.LGPL
%{_qt5_libdir}/libQt5Multimedia.so.5*
%{_qt5_libdir}/libQt5MultimediaQuick_p.so.5*
%{_qt5_libdir}/libQt5MultimediaWidgets.so.5*
%{_qt5_libdir}/libqgsttools_p.so.1*
%{_qt5_archdatadir}/qml/QtAudioEngine/
%{_qt5_archdatadir}/qml/QtMultimedia/
%{_qt5_plugindir}/audio/
%{_qt5_plugindir}/mediaservice/
%{_qt5_plugindir}/playlistformats/

%files devel
%{_qt5_headerdir}/QtMultimedia/
%{_qt5_headerdir}/QtMultimediaQuick_p/
%{_qt5_headerdir}/QtMultimediaWidgets/
%{_qt5_libdir}/libQt5Multimedia.so
%{_qt5_libdir}/libQt5Multimedia.prl
%{_qt5_libdir}/libQt5MultimediaQuick_p.so
%{_qt5_libdir}/libQt5MultimediaQuick_p.prl
%{_qt5_libdir}/libQt5MultimediaWidgets.so
%{_qt5_libdir}/libQt5MultimediaWidgets.prl
%{_qt5_libdir}/libqgsttools_p.so
%{_qt5_libdir}/libqgsttools_p.prl
%{_qt5_libdir}/cmake/Qt5*/
%{_qt5_libdir}/pkgconfig/Qt5Multimedia.pc
%{_qt5_libdir}/pkgconfig/Qt5MultimediaQuick_p.pc
%{_qt5_libdir}/pkgconfig/Qt5MultimediaWidgets.pc
%{_qt5_archdatadir}/mkspecs/modules/*.pri

%if 0%{?docs}
%files doc
%{_qt5_docdir}/qtmultimedia.qch
%{_qt5_docdir}/qtmultimedia/
%{_qt5_docdir}/qtmultimediawidgets.qch
%{_qt5_docdir}/qtmultimediawidgets/
%endif

%if 0%{?_qt5_examplesdir:1}
%files examples
%{_qt5_examplesdir}/
%endif


%changelog
* Wed Feb 05 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.1-1
- 5.2.1

* Mon Jan 27 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-3
- build -examples only if supported

* Sun Jan 26 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-2
- -examples subpkg

* Thu Dec 12 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-1
- 5.2.0

* Mon Dec 02 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.10.rc1
- 5.2.0-rc1

* Sun Nov 10 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.4.beta1
- rebuild (arm/qreal)

* Thu Oct 24 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.3.beta1
- 5.2.0-beta1

* Wed Oct 16 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.2.alpha
- bootstrap ppc

* Wed Oct 02 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.1.alpha
- 5.2.0-alpha
- -doc subpkg

* Sat Sep 07 2013 Rex Dieter <rdieter@fedoraproject.org> 5.1.1-2
- ExclusiveArch: %%{ix86} x86_64 %%{arm} (to match qt5-qtdeclarative)

* Thu Aug 29 2013 Rex Dieter <rdieter@fedoraproject.org> 5.1.1-1
- 5.1.1

* Wed Aug 28 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.2-3
- update Source URL (and refetch tarball)
- improved summary/description

* Thu May 09 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.2-2
- BR: qt5-qtdeclarative-devel

* Thu Apr 11 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.2-1
- 5.0.2

* Sat Feb 23 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.1-1
- first try

