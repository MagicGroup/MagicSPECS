
%global qt_module qtx11extras

Summary: Qt5 - X11 support library
Name:    qt5-%{qt_module}
Version: 5.2.1
Release: 2%{?dist}

# See LGPL_EXCEPTIONS.txt, LICENSE.GPL3, respectively, for exception details
License: LGPLv2 with exceptions or GPLv3 with exceptions
Url: http://qt-project.org/
%if 0%{?pre:1}
Source0: http://download.qt-project.org/development_releases/qt/5.2/%{version}-%{pre}/submodules/%{qt_module}-opensource-src-%{version}-%{pre}.tar.xz
%else
Source0: http://download.qt-project.org/official_releases/qt/5.2/%{version}/submodules/%{qt_module}-opensource-src-%{version}.tar.xz
%endif

BuildRequires: qt5-qtbase-devel >= %{version}
%{?_qt5_version:Requires: qt5-qtbase%{?_isa} >= %{_qt5_version}}

%description
The X11 Extras module provides features specific to platforms using X11, e.g.
Linux and UNIX-like systems including embedded Linux systems that use the X
Window System.


%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: qt5-qtbase-devel%{?_isa}

%description devel
%{summary}.


%prep
%setup -q -n %{qt_module}-opensource-src-%{version}%{?pre:-%{pre}}


%build
%{_qt5_qmake}

make %{?_smp_mflags}


%install
make install INSTALL_ROOT=%{buildroot}


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%doc LGPL_EXCEPTION.txt LICENSE.GPL LICENSE.LGPL
%{_qt5_libdir}/libQt5X11Extras.so.5*


%files devel
%{_qt5_headerdir}/QtX11Extras/
%{_qt5_libdir}/libQt5X11Extras.so
%{_qt5_libdir}/libQt5X11Extras.prl
%{_qt5_libdir}/cmake/Qt5X11Extras/
%{_qt5_libdir}/pkgconfig/Qt5X11Extras.pc
%{_qt5_archdatadir}/mkspecs/modules/qt_lib_x11extras*.pri
%exclude %{_qt5_libdir}/libQt5X11Extras.la



%changelog
* Mon May 05 2014 Liu Di <liudidi@gmail.com> - 5.2.1-2
- 为 Magic 3.0 重建

* Thu Feb 06 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.1-1
- 5.2.1

* Thu Dec 12 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-1
- 5.2.0

* Sun Nov 10 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.4.beta1
- rebuild (arm/qreal)

* Thu Oct 24 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.3.beta1
- 5.2.0-beta1

* Thu Oct 24 2013 Lubomir Rintel <lkundrak@v3.sk> - 5.2.0-0.2.alpha
- Bulk sad and useless attempt at consistent SPEC file formatting

* Wed Oct 23 2013 Lubomir Rintel <lkundrak@v3.sk> - 5.2.0-0.2.alpha
- Remove ppc64 exclude

* Wed Oct 23 2013 Lubomir Rintel <lkundrak@v3.sk> - 5.2.0-0.1.alpha
- 5.2 alpha

* Fri Sep 27 2013 Lubomir Rintel <lkundrak@v3.sk> - 5.1.1-1
- Initial packaging
