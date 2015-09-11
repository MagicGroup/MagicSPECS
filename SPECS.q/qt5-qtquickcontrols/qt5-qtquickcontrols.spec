
%global qt_module qtquickcontrols

# define to build docs, need to undef this for bootstrapping
# where qt5-qttools builds are not yet available
%define docs 1

Name:           qt5-%{qt_module}
Summary:        Qt5 - module with set of QtQuick controls
Summary(zh_CN.UTF-8): Qt5 - QtQuick 控件集的模块
Version: 5.5.0
Release: 1%{?dist}

License:        BSD and (LGPLv2 with exceptions or GPLv3 with exceptions) and GFDL
Url:            http://qt-project.org/
%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
%if 0%{?pre:1}
Source0: http://download.qt-project.org/development_releases/qt/%{majorver}/%{version}-%{pre}/submodules/%{qt_module}-opensource-src-%{version}-%{pre}.tar.xz
%else
Source0: http://download.qt-project.org/official_releases/qt/%{majorver}/%{version}/submodules/%{qt_module}-opensource-src-%{version}.tar.xz
%endif

BuildRequires:  qt5-qtbase-devel >= %{version}
BuildRequires:  qt5-qtbase-static >= %{version}
BuildRequires:  pkgconfig(Qt5Quick)
BuildRequires:  pkgconfig(Qt5Qml)
BuildRequires:  pkgconfig(Qt5Network)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5Core)

%{?_qt5_version:Requires: qt5-qtbase%{?_isa} >= %{_qt5_version}}

%description
The Qt Quick Controls module provides a set of controls that can be used to
build complete interfaces in Qt Quick.

%description -l zh_CN.UTF-8
Qt5 - QtQuick 控件集的模块。

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
Summary(zh_CN.UTF-8): %{name} 的样例程序
Requires: %{name}%{?_isa} = %{version}-%{release}
%description examples
%{summary}.

%description examples -l zh_CN.UTF-8
%{name} 的样例程序。

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
magic_rpm_clean.sh

%files
%{_qt5_archdatadir}/qml/QtQuick/
%doc LICENSE.*

%if 0%{?docs}
%files doc
%doc LICENSE.FDL
%{_qt5_docdir}/qtquickcontrols.qch
%{_qt5_docdir}/qtquickcontrols/
%{_qt5_docdir}/qtquicklayouts.qch
%{_qt5_docdir}/qtquicklayouts/
%{_qt5_docdir}/qtquickdialogs.qch
%{_qt5_docdir}/qtquickdialogs/
%{_qt5_docdir}/qtquickextras.qch
%{_qt5_docdir}/qtquickextras/
%endif

%if 0%{?_qt5_examplesdir:1}
%files examples
%{_qt5_examplesdir}/
%endif

%changelog
* Fri Sep 11 2015 Liu Di <liudidi@gmail.com> - 5.5.0-1
- 更新到 5.5.0

* Fri Mar 20 2015 Liu Di <liudidi@gmail.com> - 5.4.1-1
- 更新到 5.4.1

* Wed Aug 06 2014 Liu Di <liudidi@gmail.com> - 5.3.1-2
- 为 Magic 3.0 重建

* Tue Jun 17 2014 Jan Grulich <jgrulich@redhat.com> - 5.3.1-1
- 5.3.1

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 21 2014 Jan Grulich <jgrulich@redhat.com> 5.3.0-1
- 5.3.0

* Thu Feb 06 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.1-1
- 5.2.1

* Mon Jan 27 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-2
- ready -examples subpkg

* Thu Dec 12 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-1
- 5.2.0

* Mon Dec 02 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.10.rc1
- 5.2.0-rc1

* Mon Nov 11 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.5.beta1
- rebuild (arm/qreal)

* Thu Oct 24 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.4.beta1
- 5.2.0-beta1

* Thu Oct 24 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.3.alpha
- bootstrap ppc

* Thu Oct 24 2013 Lubomir Rintel <lkundrak@v3.sk> - 5.2.0-0.2.alpha
- Bulk sad and useless attempt at consistent SPEC file formatting

* Wed Oct 02 2013 Rex Dieter <rdieter@fedoraproject.org> - 5.2.0-0.1.alpha
- 5.2.0-alpha
- tidy dir ownership
- -doc subpkg

* Mon Sep 23 2013 Lubomir Rintel <lkundrak@v3.sk> - 5.1.1-2
- Drop unused devel package (Rex Dieter, #1008527)

* Wed Sep 11 2013 Lubomir Rintel <lkundrak@v3.sk> - 5.1.1-1
- Initial packaging
