%global qt_module qtaccountsservice

Name:           qt5-%{qt_module}
Summary:        Qt5 - AccountService addon
Version:        0.1.1
Release:        3%{?dist}
Group:          Applications/System
License:        LGPLv2+
URL:            https://github.com/hawaii-desktop/qt-accountsservice-addon
# git clone --no-checkout https://github.com/hawaii-desktop/qt-accountsservice-addon.git
# cd qt-accountsservice-addon/
# git archive v0.1.1 --prefix=qt-accountsservice-addon-0.1.1/ |gzip >qt-accountsservice-addon-0.1.1.tar.gz
Source0:        qt-accountsservice-addon-%{version}.tar.gz

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


%package devel
Summary:    Development files for Qt Account Service Addon
Group:      Development/System
Requires:   %{name}%{?isa} = %{version}-%{release}
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description devel
Files for development using Qt Account Service Addon.


%prep
%setup -q -n qt-accountsservice-addon-%{version}


%build
%cmake -DCMAKE_INSTALL_PREFIX=$RPM_BUILD_ROOT%{_prefix} .
make %{?_smp_mflags} LINK='g++ -Wl,--as-needed'


%install
make install INSTALL_ROOT=$RPM_BUILD_ROOT
#DESTDIR=$RPM_BUILD_ROOT
#INSTALL_ROOT=$RPM_BUILD_ROOT
#make install DESTDIR=$RPM_BUILD_ROOT INSTALL_ROOT=$RPM_BUILD_ROOT


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
* Sun Nov 24 2013 Lubomir Rintel <lkundrak@v3.sk> - 0.1.1-1
- Rebase

* Tue Oct 15 2013 Lubomir Rintel <lkundrak@v3.sk> - 0.1.0-3
- Own our directories (Christopher Meng, #1011501)
- Don't link to unused libraries (Christopher Meng, #1011501)

* Tue Sep 24 2013 Lubomir Rintel <lkundrak@v3.sk> - 0.1.0-2
- Incorporate some review fixes (Christopher Meng, #1011501)

* Mon Sep 16 2013 Lubomir Rintel <lkundrak@v3.sk> - 0.1.0-1
- Initial packaging
