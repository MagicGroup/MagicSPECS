%define qt5 0
Name:           qt-gstreamer
Version:        0.10.3
Release:        4%{?dist}
Summary:        C++ bindings for GStreamer with a Qt-style API
License:        LGPLv2+
URL:            http://gstreamer.freedesktop.org/wiki/QtGStreamer
Source0:        http://gstreamer.freedesktop.org/src/%{name}/%{name}-%{version}.tar.bz2

BuildRequires:  automoc
BuildRequires:  boost-devel
BuildRequires:  gstreamer-plugins-base-devel >= 0.10.33
BuildRequires:  qt4-devel
%if 0%{qt5}
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtquick1-devel
%endif

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

%if 0%{qt5}
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
%endif

%prep
%setup -q

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} -DQT_VERSION=4 ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%if 0%{qt5}
mkdir -p %{_target_platform}-qt5
pushd %{_target_platform}-qt5
%{cmake} -DQT_VERSION=5 ..
popd

make %{?_smp_mflags} -C %{_target_platform}-qt5
%endif

%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}
%if 0%{qt5}
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}-qt5
%endif

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc COPYING README
%{_libdir}/gstreamer-0.10/libgstqtvideosink.so
%{_libdir}/libQtGLib-2.0.so.0*
%{_libdir}/libQtGStreamer-0.10.so.0*
%{_libdir}/libQtGStreamerUi-0.10.so.0*
%{_libdir}/libQtGStreamerUtils-0.10.so.0*
%{_libdir}/qt4/imports/QtGStreamer/

%files devel
%doc HACKING
%{_includedir}/QtGStreamer
%{_libdir}/cmake/QtGStreamer
%{_libdir}/libQtGLib-2.0.so
%{_libdir}/libQtGStreamer-0.10.so
%{_libdir}/libQtGStreamerUi-0.10.so
%{_libdir}/libQtGStreamerUtils-0.10.so
%{_libdir}/pkgconfig/QtGLib-2.0.pc
%{_libdir}/pkgconfig/QtGStreamer-0.10.pc
%{_libdir}/pkgconfig/QtGStreamerUi-0.10.pc
%{_libdir}/pkgconfig/QtGStreamerUtils-0.10.pc

%if 0%{qt5}
%post -n qt5-gstreamer -p /sbin/ldconfig
%postun -n qt5-gstreamer -p /sbin/ldconfig

%files -n qt5-gstreamer
%doc COPYING README
%{_libdir}/gstreamer-0.10/libgstqt5videosink.so
%{_libdir}/libQt5GLib-2.0.so.0*
%{_libdir}/libQt5GStreamer-0.10.so.0*
%{_libdir}/libQt5GStreamerUi-0.10.so.0*
%{_libdir}/libQt5GStreamerUtils-0.10.so.0*
%{_libdir}/qt5/imports/QtGStreamer/

%files -n qt5-gstreamer-devel
%doc HACKING
%{_includedir}/Qt5GStreamer
%{_libdir}/cmake/Qt5GStreamer
%{_libdir}/libQt5GLib-2.0.so
%{_libdir}/libQt5GStreamer-0.10.so
%{_libdir}/libQt5GStreamerUi-0.10.so
%{_libdir}/libQt5GStreamerUtils-0.10.so
%{_libdir}/pkgconfig/Qt5GLib-2.0.pc
%{_libdir}/pkgconfig/Qt5GStreamer-0.10.pc
%{_libdir}/pkgconfig/Qt5GStreamerUi-0.10.pc
%{_libdir}/pkgconfig/Qt5GStreamerUtils-0.10.pc
%endif

%changelog
* Tue Apr 29 2014 Liu Di <liudidi@gmail.com> - 0.10.3-4
- 为 Magic 3.0 重建

* Tue Apr 29 2014 Liu Di <liudidi@gmail.com> - 0.10.3-3
- 为 Magic 3.0 重建

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
