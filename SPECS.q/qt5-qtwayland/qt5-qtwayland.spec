
%global qt_module qtwayland

Summary:        Qt5 - Wayland platform support and QtCompositor module
Name:           qt5-%{qt_module}
Version:        5.2.1
Release:        0.6.20140202git6d038fb%{?dist}
License:        LGPLv2 with exceptions or GPLv3 with exceptions
Url:            http://qt-project.org/wiki/QtWayland
# git clone --no-checkout git://gitorious.org/qt/qtwayland.git
# cd qtwayland/
# git archive 6d038fb --prefix=qtwayland/ |gzip >qtwayland.tar.gz
Source0:        qtwayland.tar.gz
Patch0:         0001-Disable-stuff-that-does-not-build-with-desktop-gl.patch

BuildRequires:  qt5-qtbase-devel >= 5.2
BuildRequires:  qt5-qtbase-static >= 5.2
BuildRequires:  qt5-qtdeclarative-devel
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(xcomposite)
BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  git

%{?_qt5_version:Requires: qt5-qtbase%{?_isa} >= %{_qt5_version}}

%description
%{summary}


%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       qt5-qtbase-devel%{?_isa}

%description devel
%{summary}.


%package examples
Summary:        Examples for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description examples
%{summary}.


%prep
%setup -q -n %{qt_module}
%patch0 -p1


%build
# Presence of repository tricks qmake into invoking syncqt for us with
# correct arguments at make time.
git init

%{_qt5_qmake} -o gl/Makefile CONFIG+=wayland-compositor
%{_qt5_qmake} -o nogl/Makefile QT_WAYLAND_GL_CONFIG=nogl
make -C nogl %{?_smp_mflags}
make -C gl %{?_smp_mflags}


%install
make -C nogl install INSTALL_ROOT=%{buildroot}
make -C gl install INSTALL_ROOT=%{buildroot}
install -pm644 gl/include/QtCompositor/%{version}/QtCompositor/private/{wayland-wayland-server-protocol.h,qwayland-server-wayland.h} \
        %{buildroot}%{_qt5_headerdir}/QtCompositor/%{version}/QtCompositor/private


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%{_qt5_plugindir}/platforms
%{_qt5_plugindir}/wayland-graphics-integration
%{_qt5_libdir}/libQt5*.so.5*
%doc README
%doc LICENSE.FDL LICENSE.LGPL LICENSE.GPL
%doc LGPL_EXCEPTION.txt


%files devel
%{_qt5_bindir}/qtwaylandscanner
%{_qt5_headerdir}/Qt*/
%{_qt5_libdir}/libQt5*.so
%{_qt5_libdir}/libQt5*.prl
%{_qt5_libdir}/cmake/Qt5*/
%{_qt5_libdir}/pkgconfig/Qt5*.pc
%{_qt5_archdatadir}/mkspecs/modules/*.pri
%exclude %{_qt5_libdir}/libQt5*.la


%files examples
%{_qt5_examplesdir}


%changelog
* Fri Feb 14 2014 Lubomir Rintel <lkundrak@v3.sk> - 5.1.0-0.6.20140202git6d038fb
- A more recent snapshot
- Disable xcomposite compositor until it builds

* Sat Jan 04 2014 Lubomir Rintel <lkundrak@v3.sk> - 5.1.0-0.6.20131203git6b20dfe
- Enable QtQuick compositor

* Sat Jan 04 2014 Lubomir Rintel <lkundrak@v3.sk> - 5.1.0-0.5.20131203git6b20dfe
- A newer snapshot

* Mon Nov 25 2013 Lubomir Rintel <lkundrak@v3.sk> - 5.1.0-0.5.20131125git4f5985c
- Rebase to a later snapshot, drop our patches
- Add license texts

* Sat Nov 23 2013 Lubomir Rintel <lkundrak@v3.sk> - 5.1.0-0.5.20131120git8cd1a77
- Rebuild with EGL backend

* Fri Nov 22 2013 Lubomir Rintel <lkundrak@v3.sk> - 5.1.0-0.4.20131120git8cd1a77
- Rebase to a later snapshot, drop 5.2 ABI patch
- Enable nogl backend

* Sun Nov 10 2013 Rex Dieter <rdieter@fedoraproject.org> 5.1.0-0.4.20130826git3b0b90b
- rebuild (arm/qreal)

* Thu Oct 24 2013 Lubomir Rintel <lkundrak@v3.sk> - 5.1.0-0.3.20130826git3b0b90b
- Bulk sad and useless attempt at consistent SPEC file formatting

* Sun Oct 06 2013 Lubomir Rintel <lkundrak@v3.sk> - 5.1.0-0.2.20130826git3b0b90b
- Bump platform plugin ABI to 5.2 for Qt 5.2 aplha

* Wed Sep 11 2013 Lubomir Rintel <lkundrak@v3.sk> - 5.1.0-0.1.20130826git3b0b90b
- Initial packaging
- Adjustments from review (Rex Dieter, #1008529)
