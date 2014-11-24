Name:           qt-gstreamer
Version:        1.2.0
Release:        3%{?dist}
Summary:        C++ bindings for GStreamer with a Qt-style API
License:        LGPLv2+
URL:            http://gstreamer.freedesktop.org/modules/qt-gstreamer.html
Source0:        http://gstreamer.freedesktop.org/src/%{name}/%{name}-%{version}.tar.xz

BuildRequires:  automoc
BuildRequires:  boost-devel
BuildRequires:  gstreamer1-plugins-base-devel
BuildRequires:  qt4-devel
BuildRequires:  qt5-qtdeclarative-devel
BuildRequires:  qt5-qtquick1-devel

%{?_qt4_version:Requires: qt4%{?_isa} >= %{_qt4_version}}

%description
QtGStreamer provides C++ bindings for GStreamer with a Qt-style
API, plus some helper classes for integrating GStreamer better
in Qt4 applications.


%package devel
Summary:        Header files and development documentation for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       boost-devel%{?_isa}
%description devel
This package contains the header files and development documentation
for %{name}.

%package -n qt5-gstreamer
Summary:        C++ bindings for GStreamer with a Qt5-style API
%{?_qt5_version:Requires: qt5-qtbase%{?_isa} >= %{_qt5_version}}
%description -n qt5-gstreamer
QtGStreamer provides C++ bindings for GStreamer with a Qt-style
API, plus some helper classes for integrating GStreamer better
in Qt5 applications.

%package -n qt5-gstreamer-devel
Summary:        Header files and development documentation for qt5-gstreamer
Requires:       qt5-gstreamer%{?_isa} = %{version}-%{release}
Requires:       boost-devel%{?_isa}
%description -n qt5-gstreamer-devel
This package contains the header files and development documentation
for qt5-gstreamer.

%prep
%setup -q

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} -DQT_VERSION=4 ..
popd

make %{?_smp_mflags} -C %{_target_platform}

mkdir -p %{_target_platform}-qt5
pushd %{_target_platform}-qt5
%{cmake} -DQT_VERSION=5 ..
popd

make %{?_smp_mflags} -C %{_target_platform}-qt5


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}-qt5


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc COPYING README
%{_libdir}/gstreamer-1.0/libgstqtvideosink.so
%{_libdir}/libQtGLib-2.0.so.0
%{_libdir}/libQtGLib-2.0.so.1*
%{_libdir}/libQtGStreamer-1.0.so.0
%{_libdir}/libQtGStreamer-1.0.so.1*
%{_libdir}/libQtGStreamerUi-1.0.so.0
%{_libdir}/libQtGStreamerUi-1.0.so.1*
%{_libdir}/libQtGStreamerUtils-1.0.so.0
%{_libdir}/libQtGStreamerUtils-1.0.so.1*
%{_libdir}/qt4/imports/QtGStreamer/

%files devel
%doc HACKING
%{_includedir}/QtGStreamer
%{_libdir}/cmake/QtGStreamer
%{_libdir}/libQtGLib-2.0.so
%{_libdir}/libQtGStreamer-1.0.so
%{_libdir}/libQtGStreamerUi-1.0.so
%{_libdir}/libQtGStreamerUtils-1.0.so
%{_libdir}/pkgconfig/QtGLib-2.0.pc
%{_libdir}/pkgconfig/QtGStreamer-1.0.pc
%{_libdir}/pkgconfig/QtGStreamerUi-1.0.pc
%{_libdir}/pkgconfig/QtGStreamerUtils-1.0.pc

%post -n qt5-gstreamer -p /sbin/ldconfig
%postun -n qt5-gstreamer -p /sbin/ldconfig

%files -n qt5-gstreamer
%doc COPYING README
%{_libdir}/gstreamer-1.0/libgstqt5videosink.so
%{_libdir}/libQt5GLib-2.0.so.0
%{_libdir}/libQt5GLib-2.0.so.1*
%{_libdir}/libQt5GStreamer-1.0.so.0
%{_libdir}/libQt5GStreamer-1.0.so.1*
%{_libdir}/libQt5GStreamerUi-1.0.so.0
%{_libdir}/libQt5GStreamerUi-1.0.so.1*
%{_libdir}/libQt5GStreamerUtils-1.0.so.0
%{_libdir}/libQt5GStreamerUtils-1.0.so.1*
%{_libdir}/libQt5GStreamerQuick-1.0.so.0
%{_libdir}/libQt5GStreamerQuick-1.0.so.1*
%{_libdir}/qt5/imports/QtGStreamer/
%{_libdir}/qt5/qml/QtGStreamer/

%files -n qt5-gstreamer-devel
%doc HACKING
%{_includedir}/Qt5GStreamer
%{_libdir}/cmake/Qt5GStreamer
%{_libdir}/libQt5GLib-2.0.so
%{_libdir}/libQt5GStreamer-1.0.so
%{_libdir}/libQt5GStreamerUi-1.0.so
%{_libdir}/libQt5GStreamerUtils-1.0.so
%{_libdir}/libQt5GStreamerQuick-1.0.so
%{_libdir}/pkgconfig/Qt5GLib-2.0.pc
%{_libdir}/pkgconfig/Qt5GStreamer-1.0.pc
%{_libdir}/pkgconfig/Qt5GStreamerUi-1.0.pc
%{_libdir}/pkgconfig/Qt5GStreamerUtils-1.0.pc
%{_libdir}/pkgconfig/Qt5GStreamerQuick-1.0.pc
%{_libdir}/pkgconfig/Qt5GStreamerQuick-1.0.pc


%changelog
* Fri Oct 31 2014 Liu Di <liudidi@gmail.com> - 1.2.0-3
- 为 Magic 3.0 重建

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jul  9 2014 Alexey Kurov <nucleo@fedoraproject.org> - 1.2.0-1
- qt-gstreamer-1.2.0
- switch to gstreamer1

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 23 2014 Petr Machata <pmachata@redhat.com> - 0.10.3-3
- Rebuild for boost 1.55.0

* Fri Nov 15 2013 Alexey Kurov <nucleo@fedoraproject.org> - 0.10.3-2
- rebuilt for arm switch qreal double

* Wed Oct 16 2013 Alexey Kurov <nucleo@fedoraproject.org> - 0.10.3-1
- qt-gstreamer-0.10.3
- BR: qt5-qtbase-devel qt5-qtquick1-devel
- added qt5-gstreamer and qt5-gstreamer-devel subpackages
- remove Requires pulled in via automatic pkgconfig deps

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 30 2013 Petr Machata <pmachata@redhat.com> - 0.10.2-5
- Rebuild for boost 1.54.0

* Sun Feb 10 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 0.10.2-4
- Rebuild for Boost-1.53.0

* Sat Feb 09 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 0.10.2-3
- Rebuild for Boost-1.53.0

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Apr 15 2012 Alexey Kurov <nucleo@fedoraproject.org> - 0.10.2-1
- qt-gstreamer-0.10.2

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Aug 31 2011 Alexey Kurov <nucleo@fedoraproject.org> - 0.10.1-2
- Fix compilation with glib 2.29 (FTBFS #716209)

* Thu Feb  3 2011 Alexey Kurov <nucleo@fedoraproject.org> - 0.10.1-1
- Initial RPM release
