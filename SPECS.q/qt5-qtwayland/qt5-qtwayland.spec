
%global qt_module qtwayland

# build support for non-egl platforms
%define nogl 1

Summary:        Qt5 - Wayland platform support and QtCompositor module
Summary(zh_CN.UTF-8): Qt5 - Wayland 平台支持和 QtCompositor 模块
Name:           qt5-%{qt_module}
Version: 5.5.1
Release: 3%{?dist}
License:        LGPLv2 with exceptions or GPLv3 with exceptions
Url:            http://qt-project.org/wiki/QtWayland
%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
%if 0%{?pre:1}
Source0: http://download.qt-project.org/development_releases/qt/%{majorver}/%{version}-%{pre}/submodules/%{qt_module}-opensource-src-%{version}-%{pre}.tar.xz
%else
Source0: http://download.qt-project.org/official_releases/qt/%{majorver}/%{version}/submodules/%{qt_module}-opensource-src-%{version}.tar.xz
%endif

BuildRequires:  qt5-qtbase-devel >= %{version} 
BuildRequires:  qt5-qtbase-static
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

%{?_qt5_version:Requires: qt5-qtbase%{?_isa} >= %{_qt5_version}}

%description
%{summary}.
%description -l zh_CN.UTF-8
Qt5 - Wayland 平台支持和 QtCompositor 模块。

%package devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       qt5-qtbase-devel%{?_isa}
%description devel
%{summary}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package examples
Summary:        Examples for %{name}
Summary(zh_CN.UTF-8): %{name} 的样例
Requires:       %{name}%{?_isa} = %{version}-%{release}
%description examples
%{summary}.

%description examples -l zh_CN.UTF-8
%{name} 的样例。

%prep
%setup -q -n %{qt_module}-opensource-src-%{version}%{?pre:-%{pre}}

# Presence of .git/ qmake into invoking syncqt for us with
# correct arguments at make time.
# else, out-of-src-tree builds fail with stuff like:
# qwaylanddisplay_p.h:52:54: fatal error: QtWaylandClient/private/qwayland-wayland.h: No such file or directory
# #include <QtWaylandClient/private/qwayland-wayland.h>
mkdir .git


%build

%if 0%{?nogl}
# build support for non-egl platforms
mkdir nogl
pushd nogl
%{qmake_qt5} QT_WAYLAND_GL_CONFIG=nogl ..
popd
make %{?_smp_mflags} -C nogl
%endif

%{_qt5_qmake} CONFIG+=wayland-compositor
make %{?_smp_mflags}


%install
%if 0%{?nogl}
make install INSTALL_ROOT=%{buildroot} -C nogl/
%endif
make install INSTALL_ROOT=%{buildroot}

## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_qt5_libdir}
for prl_file in libQt5*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
popd


# install private headers... needed by hawaii shell 
install -pm644 \
  include/QtCompositor/%{version}/QtCompositor/private/{wayland-wayland-server-protocol.h,qwayland-server-wayland.h} \
  %{buildroot}%{_qt5_headerdir}/QtCompositor/%{version}/QtCompositor/private/
magic_rpm_clean.sh

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc README
%{_qt5_libdir}/libQt5Compositor.so.5*
%{_qt5_libdir}/libQt5WaylandClient.so.5*
%dir %{_qt5_plugindir}/wayland-decoration-client/
%{_qt5_plugindir}/wayland-decoration-client/libbradient.so
%{_qt5_plugindir}/wayland-graphics-integration-server
%{_qt5_plugindir}/wayland-graphics-integration-client
%{_qt5_plugindir}/platforms/libqwayland-egl.so
%{_qt5_plugindir}/platforms/libqwayland-generic.so
%{_qt5_plugindir}/platforms/libqwayland-xcomposite-egl.so
%{_qt5_plugindir}/platforms/libqwayland-xcomposite-glx.so
%dir %{_qt5_libdir}/cmake/Qt5Compositor/
%{_qt5_libdir}/cmake/Qt5Compositor/Qt5Compositor_*.cmake
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_*.cmake
%dir %{_qt5_libdir}/cmake/Qt5WaylandClient/
%{_qt5_libdir}/cmake/Qt5WaylandClient/Qt5WaylandClient_*.cmake

%files devel
%{_qt5_bindir}/qtwaylandscanner
%{_qt5_headerdir}/QtCompositor/
%{_qt5_headerdir}/QtWaylandClient/
%{_qt5_libdir}/libQt5Compositor.so
%{_qt5_libdir}/libQt5WaylandClient.so
%{_qt5_libdir}/libQt5Compositor.prl
%{_qt5_libdir}/libQt5WaylandClient.prl
%{_qt5_libdir}/cmake/Qt5Compositor/Qt5CompositorConfig*.cmake
%{_qt5_libdir}/pkgconfig/Qt5Compositor.pc
%{_qt5_libdir}/pkgconfig/Qt5WaylandClient.pc
%{_qt5_archdatadir}/mkspecs/modules/qt_lib_compositor*.pri
%{_qt5_archdatadir}/mkspecs/modules/qt_lib_waylandclient*.pri

%files examples
%{_qt5_examplesdir}/wayland/


%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 5.5.1-3
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 5.5.1-2
- 更新到 5.5.1

* Fri Sep 11 2015 Liu Di <liudidi@gmail.com> - 5.5.0-1
- 更新到 5.5.0

* Fri Mar 20 2015 Liu Di <liudidi@gmail.com> - 5.4.1-2
- 为 Magic 3.0 重建

* Fri Feb 27 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.1-1
- 5.4.1

* Wed Dec 10 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-1
- 5.4.0 (final)

* Fri Nov 28 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-0.3.rc
- 5.4.0-rc

* Mon Nov 03 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-0.2.beta
- use %%qmake_qt5 macro

* Mon Oct 20 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-0.1.beta 
- 5.4.0-beta

* Wed Sep 24 2014 Lubomir Rintel <lkundrak@v3.sk> - 5.4.0-0.alpha1
- Switch from a Git snapshot to a pre-release tarball

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.0-0.3.20140723git02c499c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 24 2014 Lubomir Rintel <lkundrak@v3.sk> - 5.3.0-0.2.20140723git02c499c
- Update

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.0-0.2.20140529git98dca3b
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 27 2014 Lubomir Rintel <lkundrak@v3.sk> - 5.3.0-0.1.20140529git98dca3b
- Update and rebuild for Qt 5.3

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
