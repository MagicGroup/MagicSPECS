%global qt_module qtaccountsservice

Name:           qt5-%{qt_module}
Summary:        Qt5 - AccountService addon
Summary(zh_CN.UTF-8): Qt5 - 账号服务附加组件
Version:        0.1.2
Release:        6%{?dist}
Group:          Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
License:        LGPLv2+
URL:            https://github.com/hawaii-desktop/qt-accountsservice-addon
Source0:        http://downloads.sourceforge.net/project/mauios/hawaii/%{qt_module}/%{qt_module}-%{version}.tar.gz

BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5DBus)
BuildRequires:  pkgconfig(Qt5Network)
BuildRequires:  pkgconfig(Qt5Qml)
BuildRequires:  pkgconfig(Qt5Quick)
BuildRequires:  qt5-qtbase-devel
BuildRequires:  cmake

%description
Qt-style API for freedesktop.org's AccountsService DBus service (see 
http://www.freedesktop.org/wiki/Software/AccountsService).

%description -l zh_CN.UTF-8
freedesktop.org 的账号服务 DBus 服务的 QT API。

%package devel
Summary:    Development files for Qt Account Service Addon
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:      Development/System
Group(zh_CN.UTF-8): 开发/库
Requires:   %{name}%{?isa} = %{version}-%{release}
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description devel
Files for development using Qt Account Service Addon.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n %{qt_module}-%{version}


%build
%cmake -DCMAKE_INSTALL_PREFIX=$RPM_BUILD_ROOT%{_prefix} .
make %{?_smp_mflags} LINK='g++ -Wl,--as-needed'


%install
make install INSTALL_ROOT=$RPM_BUILD_ROOT
magic_rpm_clean.sh

%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%{_libdir}/libqtaccountsservice-qt5.so.*
%{_libdir}/hawaii
%doc README.md
%doc LICENSE


%files devel
%{_includedir}/QtAccountsService
%{_libdir}/cmake/QtAccountsService
%{_libdir}/libqtaccountsservice-qt5.so


%changelog
* Wed Mar 18 2015 Liu Di <liudidi@gmail.com> - 0.1.2-6
- 为 Magic 3.0 重建

* Tue Aug 05 2014 Liu Di <liudidi@gmail.com> - 0.1.2-5
- 为 Magic 3.0 重建

* Thu Jul 24 2014 Lubomir Rintel <lkundrak@v3.sk> - 0.1.2-1
- Update to 0.1.2

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Nov 24 2013 Lubomir Rintel <lkundrak@v3.sk> - 0.1.1-1
- Rebase

* Tue Oct 15 2013 Lubomir Rintel <lkundrak@v3.sk> - 0.1.0-3
- Own our directories (Christopher Meng, #1011501)
- Don't link to unused libraries (Christopher Meng, #1011501)

* Tue Sep 24 2013 Lubomir Rintel <lkundrak@v3.sk> - 0.1.0-2
- Incorporate some review fixes (Christopher Meng, #1011501)

* Mon Sep 16 2013 Lubomir Rintel <lkundrak@v3.sk> - 0.1.0-1
- Initial packaging
