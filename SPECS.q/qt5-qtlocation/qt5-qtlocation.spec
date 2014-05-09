
%global qt_module qtlocation
# define to build docs, need to undef this for bootstrapping
%define docs 1

Summary: Qt5 - Location component
Name:    qt5-%{qt_module}
Version: 5.2.1
Release: 3%{?dist}

# See LGPL_EXCEPTIONS.txt, LICENSE.GPL3, respectively, for exception details
License: LGPLv2 with exceptions or GPLv3 with exceptions
Url: http://qt-project.org/
%if 0%{?pre:1}
Source0: http://download.qt-project.org/development_releases/qt/5.2/%{version}-%{pre}/submodules/%{qt_module}-opensource-src-%{version}-%{pre}.tar.xz
%else
Source0: http://download.qt-project.org/official_releases/qt/5.2/%{version}/submodules/%{qt_module}-opensource-src-%{version}.tar.xz
%endif

BuildRequires: qt5-qtbase-devel >= %{version}
BuildRequires: pkgconfig(Qt5Qml)
BuildRequires: pkgconfig(geoclue)
BuildRequires: pkgconfig(gypsy)
%{?_qt5_version:Requires: qt5-qtbase%{?_isa} >= %{_qt5_version}}

%description
The Qt Positioning API gives developers the ability to determine a position
by using a variety of possible sources, including satellite, or wifi, or
 text file, and so on. That information can then be used to for example
determine a position on a map. In addition satellite information can be
retrieved and area based monitoring can be performed.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: qt5-qtbase-devel%{?_isa}
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

## unpackaged files
# .la files, die, die, die.
rm -fv %{buildroot}%{_qt5_libdir}/lib*.la


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc LGPL_EXCEPTION.txt LICENSE.GPL LICENSE.LGPL
%{_qt5_libdir}/libQt5Positioning.so.5*
%{_qt5_plugindir}/position/
%{_qt5_archdatadir}/qml/QtPositioning/

%files devel
%{_qt5_headerdir}/QtPositioning/
%{_qt5_libdir}/libQt5Positioning.so
%{_qt5_libdir}/libQt5Positioning.prl
%{_qt5_libdir}/cmake/Qt5Positioning/
%{_qt5_libdir}/pkgconfig/Qt5Positioning.pc
%{_qt5_archdatadir}/mkspecs/modules/qt_lib_positioning*.pri

%if 0%{?docs}
%files doc
%doc LICENSE.FDL
%{_qt5_docdir}/qtpositioning.qch
%{_qt5_docdir}/qtpositioning/
%endif

%if 0%{?_qt5_examplesdir:1}
%files examples
%{_qt5_examplesdir}/
%endif


%changelog
* Mon May 05 2014 Liu Di <liudidi@gmail.com> - 5.2.1-3
- 为 Magic 3.0 重建

* Mon May 05 2014 Liu Di <liudidi@gmail.com> - 5.2.1-2
- 为 Magic 3.0 重建

* Wed Feb 05 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.1-1
- 5.2.1

* Mon Jan 27 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-3
- build -examples only when supported

* Sun Jan 26 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-2
- -examples subpkg

* Thu Jan 02 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-1
- first try
