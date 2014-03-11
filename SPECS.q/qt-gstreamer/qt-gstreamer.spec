Name:           qt-gstreamer
Version:        0.10.2
Release:        3%{?dist}
Summary:        C++ bindings for GStreamer with a Qt-style API

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://gstreamer.freedesktop.org/wiki/QtGStreamer
Source0:        http://gstreamer.freedesktop.org/src/%{name}/%{name}-%{version}.tar.bz2

BuildRequires:  automoc
BuildRequires:  boost-devel
BuildRequires:  gstreamer-plugins-base-devel >= 0.10.33
BuildRequires:  qt4-devel

%{?_qt4_version:Requires: qt4%{?_isa} >= %{_qt4_version}}

%description
QtGStreamer provides C++ bindings for GStreamer with a Qt-style
API, plus some helper classes for integrating GStreamer better
in Qt applications.


%package devel
Summary:        Header files and development documentation for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       boost-devel%{?_isa}
Requires:       gstreamer-plugins-base-devel%{?_isa}
Requires:       qt4-devel%{?_isa}
%description devel
This package contains the header files and development documentation
for %{name}.


%prep
%setup -q

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
rm -rf %{buildroot}
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}
magic_rpm_clean.sh

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING README
%{_libdir}/gstreamer-0.10/libgstqtvideosink.so
%{_libdir}/libQtGLib-2.0.so.0*
%{_libdir}/libQtGStreamer-0.10.so.0*
%{_libdir}/libQtGStreamerUi-0.10.so.0*
%{_libdir}/libQtGStreamerUtils-0.10.so.0*
%{_libdir}/qt4/imports/QtGStreamer/

%files devel
%defattr(-,root,root,-)
%doc HACKING
%{_includedir}/QtGStreamer
%{_libdir}/QtGStreamer
%{_libdir}/libQtGLib-2.0.so
%{_libdir}/libQtGStreamer-0.10.so
%{_libdir}/libQtGStreamerUi-0.10.so
%{_libdir}/libQtGStreamerUtils-0.10.so
%{_libdir}/pkgconfig/QtGLib-2.0.pc
%{_libdir}/pkgconfig/QtGStreamer-0.10.pc
%{_libdir}/pkgconfig/QtGStreamerUi-0.10.pc
%{_libdir}/pkgconfig/QtGStreamerUtils-0.10.pc


%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 0.10.2-3
- 为 Magic 3.0 重建

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
