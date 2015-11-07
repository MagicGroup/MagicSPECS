
%global qt_module qtlocation
# define to build docs, need to undef this for bootstrapping
%define docs 1

Summary: Qt5 - Location component
Summary(zh_CN.UTF-8): Qt5 - 位置组件
Name:    qt5-%{qt_module}
Version: 5.5.1
Release: 2%{?dist}

# See LGPL_EXCEPTIONS.txt, LICENSE.GPL3, respectively, for exception details
License: LGPLv2 with exceptions or GPLv3 with exceptions
Url: http://qt-project.org/
%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
%if 0%{?pre:1}
Source0: http://download.qt-project.org/development_releases/qt/%{majorver}/%{version}-%{pre}/submodules/%{qt_module}-opensource-src-%{version}-%{pre}.tar.xz
%else
Source0: http://download.qt-project.org/official_releases/qt/%{majorver}/%{version}/submodules/%{qt_module}-opensource-src-%{version}.tar.xz
%endif

BuildRequires: qt5-qtbase-devel >= %{version}
BuildRequires: pkgconfig(Qt5Qml)
BuildRequires: pkgconfig(geoclue)
# gyspy currently not available on epel7, https://bugzilla.redhat.com/1069225
%if 0%{?rhel} != 7
BuildRequires: pkgconfig(gypsy)
%endif
%{?_qt5_version:Requires: qt5-qtbase%{?_isa} >= %{_qt5_version}}

%description
The Qt Positioning API gives developers the ability to determine a position
by using a variety of possible sources, including satellite, or wifi, or
 text file, and so on. That information can then be used to for example
determine a position on a map. In addition satellite information can be
retrieved and area based monitoring can be performed.

%description -l zh_CN.UTF-8
Qt5 的位置组件。

%package devel
Summary: Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: qt5-qtbase-devel%{?_isa}
%description devel
%{summary}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%if 0%{?docs}
%package doc
Summary: API documentation for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发文档
Requires: %{name} = %{version}-%{release}
# for qhelpgenerator
BuildRequires: qt5-qttools-devel
BuildArch: noarch
%description doc
%{summary}.
%description doc -l zh_CN.UTF-8
%{name} 的开发文档。
%endif

%package examples
Summary: Programming examples for %{name}
Summary(zh_CN.UTF-8): %{name} 的程序样例
Requires: %{name}%{?_isa} = %{version}-%{release}
%description examples
%{summary}.
%description examples -l zh_CN.UTF-8
%{name} 的程序样例。


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
magic_rpm_clean.sh

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc LGPL_EXCEPTION.txt LICENSE.GPL* LICENSE.LGPL*
%{_qt5_libdir}/libQt5Location.so.5*
%{_qt5_archdatadir}/qml/QtLocation/
%{_qt5_plugindir}/geoservices/
%{_qt5_libdir}/libQt5Positioning.so.5*
%{_qt5_plugindir}/position/
%{_qt5_archdatadir}/qml/QtPositioning/
%dir %{_qt5_libdir}/cmake/Qt5Location
%{_qt5_libdir}/cmake/Qt5Location/Qt5Location_QGeoServiceProviderFactory*.cmake

%files devel
%{_qt5_headerdir}/QtLocation/
%{_qt5_libdir}/libQt5Location.so
%{_qt5_libdir}/libQt5Location.prl
%{_qt5_libdir}/pkgconfig/Qt5Location.pc
%{_qt5_archdatadir}/mkspecs/modules/qt_lib_location*.pri
%{_qt5_libdir}/cmake/Qt5Location/Qt5LocationConfig*.cmake
%{_qt5_headerdir}/QtPositioning/
%{_qt5_libdir}/libQt5Positioning.so
%{_qt5_libdir}/libQt5Positioning.prl
%{_qt5_libdir}/cmake/Qt5Positioning/
%{_qt5_libdir}/pkgconfig/Qt5Positioning.pc
%{_qt5_archdatadir}/mkspecs/modules/qt_lib_positioning*.pri

%if 0%{?docs}
%files doc
%{_qt5_docdir}/qtpositioning.qch
%{_qt5_docdir}/qtpositioning/
%{_qt5_docdir}/qtlocation.qch
%{_qt5_docdir}/qtlocation/
%endif

%if 0%{?_qt5_examplesdir:1}
%files examples
%{_qt5_examplesdir}/
%endif


%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 5.5.1-2
- 更新到 5.5.1

* Thu Sep 10 2015 Liu Di <liudidi@gmail.com> - 5.5.0-1
- 更新到 5.5.0

* Wed Mar 18 2015 Liu Di <liudidi@gmail.com> - 5.4.1-1
- 更新到 5.4.1

* Wed Aug 06 2014 Liu Di <liudidi@gmail.com> - 5.3.1-2
- 为 Magic 3.0 重建

* Tue Jun 17 2014 Jan Grulich <jgrulich@redhat.com> - 5.3.1-1
- 5.3.1

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 21 2014 Jan Grulich <jgrulich@redhat.com> 5.3.0-1
- 5.3.0

* Mon May 05 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.1-2
- sanitize .prl file(s)

* Wed Feb 05 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.1-1
- 5.2.1

* Mon Jan 27 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-3
- build -examples only when supported

* Sun Jan 26 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-2
- -examples subpkg

* Thu Jan 02 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-1
- first try
