%global framework ktnef

Name:           kf5-%{framework}
Version:        15.12.0
Release:        1%{?dist}
Summary:        The KTNef Library

License:        LGPLv2+
URL:            https://projects.kde.org/projects/kde/pim/%{framework}

%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/applications/%{version}/src/%{framework}-%{version}.tar.xz

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel

BuildRequires:  kf5-kdelibs4support-devel >= 5.15

BuildRequires:  kf5-kcalendarcore-devel >= 15.11.90
BuildRequires:  kf5-kcalendarutils-devel >= 15.11.90
BuildRequires:  kf5-kcontacts-devel >= 15.11.90

Obsoletes:      kdepimlibs%{?_isa} < 15.08.0
Conflicts:      kdepimlibs%{?_isa} < 15.08.0

%description
%{summary}.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       kf5-kcalendarcore-devel
Obsoletes:      kdepimlibs-devel%{?_isa} < 15.08.0
Conflicts:      kdepimlibs-devel%{?_isa} < 15.08.0

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n %{framework}-%{version}

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license COPYING.LIB
%{_kf5_libdir}/libKF5Tnef.so.*

%files devel
%{_kf5_includedir}/ktnef_version.h
%{_kf5_includedir}/KTNEF
%{_kf5_libdir}/libKF5Tnef.so
%{_kf5_libdir}/cmake/KF5Tnef
%{_kf5_archdatadir}/mkspecs/modules/qt_KTNef.pri


%changelog
* Sat Dec 19 2015 Liu Di <liudidi@gmail.com> - 15.12.0-1
- 为 Magic 3.0 重建

* Mon Dec 07 2015 Jan Grulich <jgrulich@redhat.com> - 15.11.90-1
- Update to 15.11.90

* Thu Dec 03 2015 Jan Grulich <jgrulich@redhat.com> - 15.11.80-1
- Update to 15.11.80

* Mon Aug 24 2015 Daniel Vrátil <dvratil@redhat.com> - 15.08.0-1
- Initial version
