%define shared_desktop_ontologies_ver 0.10.0
%define soprano_ver 2.8.0
%define rversion %{kde4_kdelibs_version}

%global shared_desktop_ontologies_version %(pkg-config --modversion shared-desktop-ontologies 2>/dev/null || echo %{shared_desktop_ontologies_ver})
%global soprano_version %(pkg-config --modversion soprano 2>/dev/null || echo %{soprano_ver})

# undef or set to 0 to disable items for a faster build
#global tests 1

Name:    nepomuk-widgets
Version: %{rversion}
Release: 2%{?dist}
Summary: Nepomuk  Widgets
Summary(zh_CN.UTF-8): Nepomuk 小工具

License: LGPLv2 or LGPLv3
URL:     http://www.kde.org/

%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0: ftp://ftp.kde.org/pub/kde/%{stable}/%{version}/src/%{name}-%{version}.tar.xz

%define sysctl 1

BuildRequires:  doxygen
BuildRequires:  kdelibs4-devel >= %{version}
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(soprano) >= %{soprano_ver}
BuildRequires:  pkgconfig(libstreamanalyzer) pkgconfig(libstreams)
BuildRequires:  pkgconfig(shared-desktop-ontologies)
%if  0%{?tests}
BuildRequires:  dbus-x11
BuildRequires:  virtuoso-opensource
%endif

Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: kdelibs4%{?_isa} >= %{version}
Requires: shared-desktop-ontologies >= %{shared_desktop_ontologies_version}
Provides: soprano-backend-virtuoso >= %{soprano_version}
Requires: virtuoso-opensource

# moved from kde-runtime in 4.8.80 (nepomuk common has nepomuk-core preference)
Conflicts: kde-runtime < 4.8.80-2

%description
%{summary}.

%description -l zh_CN.UTF-8
Nepomuk 小工具。

%package devel
Summary:  Developer files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发文件 
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: kdelibs4-devel
%description devel
%{summary}.

%description devel -l zh_CN.UTF-8
%{name} 的开发文件。

%package libs
Summary:  Runtime libraries for %{name}
Summary(zh_CN.UTF-8): %{name} 的运行库
Requires: kdelibs4%{?_isa} >= %{version}
%description libs
%{summary}.

%description libs -l zh_CN.UTF-8
%{name} 的运行库。

%prep
%setup -q

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install

make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

magic_rpm_clean.sh

%check
%if 0%{?tests}
make -C %{_target_platform}/autotests/test test  ||:
%endif


%files devel
%{kde4_includedir}/nepomuk2/*.h
%{kde4_libdir}/cmake/NepomukWidgets/*.cmake
%{kde4_libdir}/libnepomukwidgets.so

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files libs
%{kde4_libdir}/libnepomukwidgets.so.*

%changelog
* Wed Apr 23 2014 Liu Di <liudidi@gmail.com> - 4.13.0-2
- 为 Magic 3.0 重建

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 4.9.3-6
- 为 Magic 3.0 重建

