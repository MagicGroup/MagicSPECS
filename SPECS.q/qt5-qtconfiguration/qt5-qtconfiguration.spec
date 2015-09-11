
%global qt_module qtconfiguration

Summary:        Qt5 - QtConfiguration module
Summary(zh_CN.UTF-8): Qt5 - QtConfiguration 模块
Name:           qt5-%{qt_module}
Version:        0.3.0
Release:        4%{?dist}

# See LGPL_EXCEPTIONS.txt, LICENSE.GPL3, respectively, for exception details
License:        LGPLv2 with exceptions or GPLv3 with exceptions
URL:            https://github.com/mauios/qtconfiguration
Source0:        http://downloads.sourceforge.net/project/mauios/hawaii/%{qt_module}/%{qt_module}-%{version}.tar.gz
Patch1:		qtconfiguration-0.3.0-qt55.patch
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Qml)
BuildRequires:  pkgconfig(dconf)
BuildRequires:  cmake

%{?_qt5_version:Requires: qt5-qtbase%{?_isa} >= %{_qt5_version}}

%description
Settings API with change notifications.

%description -l zh_CN.UTF-8
Qt5 - QtConfiguration 模块。

%package devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       qt5-qtbase-devel%{?_isa}

%description devel
%{summary}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n %{qt_module}-%{version}
%patch1 -p1

%build
%cmake .
make %{?_smp_mflags} LINK='g++ -Wl,--as-needed'


%install
make install DESTDIR=$RPM_BUILD_ROOT
magic_rpm_clean.sh

%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%{_libdir}/libqtconfiguration.so.0*
%{_libdir}/hawaii
%doc LICENSE.FDL
%doc LICENSE.GPL
%doc LICENSE.LGPL
%doc README.md


%files devel
%{_includedir}/QtConfiguration/
%{_libdir}/libqtconfiguration.so
%{_libdir}/cmake/QtConfiguration/


%changelog
* Fri Sep 11 2015 Liu Di <liudidi@gmail.com> - 0.3.0-4
- 为 Magic 3.0 重建

* Thu Mar 19 2015 Liu Di <liudidi@gmail.com> - 0.3.0-3
- 为 Magic 3.0 重建

* Tue Aug 05 2014 Liu Di <liudidi@gmail.com> - 0.3.0-2
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Lubomir Rintel <lkundrak@v3.sk> - 0.3.0-1
- Update to latest version

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Nov 17 2013 Pier Luigi Fiorini <pierluigi.fiorini@gmail.com> - 0.2.1-1
- Upstream switched from qmake to cmake
- Update to latest version

* Tue Sep 24 2013 Lubomir Rintel <lkundrak@v3.sk> - 0.1.0-3
- Get rid of extra library links (Christopher Meng, #1011501)
- Drop irrelevant license file (Christopher Meng, #1011501)

* Tue Sep 24 2013 Lubomir Rintel <lkundrak@v3.sk> - 0.1.0-2
- Incorporate some review fixes (Christopher Meng, #1011501)

* Thu Sep 12 2013 Lubomir Rintel <lkundrak@v3.sk> - 0.1.0-1
- Initial packaging
