%define shared_desktop_ontologies_ver 0.10.0
%define soprano_ver 2.8.0

%global shared_desktop_ontologies_version %(pkg-config --modversion shared-desktop-ontologies 2>/dev/null || echo %{shared_desktop_ontologies_ver})
%global soprano_version %(pkg-config --modversion soprano 2>/dev/null || echo %{soprano_ver})

# undef or set to 0 to disable items for a faster build
#global tests 1

Name:    nepomuk-core
Version: 4.14.2
Release: 1%{?dist}
Summary: Nepomuk Core utilities and libraries
Summary(zh_CN.UTF-8): Nepomuk 核心工具和库
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
Source1: nepomuk-inotify.conf

BuildRequires:  doxygen
BuildRequires:  kdelibs4-devel >= %{version}
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(soprano) >= %{soprano_ver}
BuildRequires:  pkgconfig(libstreamanalyzer) pkgconfig(libstreams)
BuildRequires:  pkgconfig(shared-desktop-ontologies)
BuildRequires:	poppler-qt4-devel
BuildRequires:  exiv2-devel
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
Nepomuk 核心工具和库。

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
Requires: %{name} = %{version}-%{release}
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

%if 0%{?sysctl}
install -p -m644 -D %{SOURCE1} %{buildroot}%{_sysconfdir}/sysctl.d/nepomuk-inotify.conf
%else
install -p -m644    %{SOURCE1} ./nepomuk-inotify.conf
%endif
magic_rpm_clean.sh

%check
desktop-file-validate %{buildroot}%{_kde4_datadir}/applications/kde4/nepomukbackup.desktop
%if 0%{?tests}
make -C %{_target_platform}/autotests/test test  ||:
%endif


%files
%doc ontologies/README COPYING.LGPL*
%if 0%{?sysctl}
%config(noreplace) %{_sysconfdir}/sysctl.d/nepomuk-inotify.conf
%else
%doc nepomuk-inotify.conf 
%endif
%{_kde4_bindir}/nepomuk2-rcgen
%{_kde4_bindir}/nepomukcleaner
%{_kde4_bindir}/nepomukbaloomigrator
%{_kde4_datadir}/autostart/nepomukbaloomigrator.desktop
%{kde4_xdgappsdir}/nepomukcleaner.desktop
%{kde4_servicetypesdir}/nepomukextractor.desktop
%{_kde4_appsdir}/fileindexerservice/
%{_kde4_appsdir}/nepomukfilewatch/
%{_kde4_appsdir}/nepomukstorage/
# this one maybe in -devel?  --rex
%{_kde4_bindir}/nepomuk-simpleresource-rcgen
%{_kde4_bindir}/nepomukbackup
%{_kde4_bindir}/nepomukindexer
%{_kde4_bindir}/nepomukserver
%{_kde4_bindir}/nepomukservicestub
%{_kde4_libdir}/libkdeinit4_nepomukserver.so
%{_kde4_libdir}/libnepomukcore.so
%{_kde4_libdir}/libnepomukextractor.so
%{_kde4_datadir}/applications/kde4/nepomukbackup.desktop
%{_kde4_datadir}/autostart/nepomukserver.desktop
%{_kde4_datadir}/kde4/services/*.desktop
%{_kde4_datadir}/kde4/servicetypes/nepomukservice.desktop
%{_kde4_datadir}/ontology/kde/
%{_datadir}/dbus-1/interfaces/*.xml
%{_sysconfdir}/dbus-1/system.d/org.kde.nepomuk.filewatch.conf
%{_kde4_bindir}/nepomukcmd
%{_kde4_bindir}/nepomukctl
%{_kde4_bindir}/nepomukfileindexer
%{_kde4_bindir}/nepomukfilewatch
%{_kde4_bindir}/nepomukmigrator
%{_kde4_bindir}/nepomuksearch
%{_kde4_bindir}/nepomukshow
%{_kde4_bindir}/nepomukstorage
%{_kde4_libexecdir}/kde_nepomuk_filewatch_raiselimit
%{kde4_libdir}/libnepomukcleaner.so.*
%{kde4_datadir}/dbus-1/system-services/org.kde.nepomuk.filewatch.service
%{kde4_servicetypesdir}/nepomukcleaningjob.desktop
%{kde4_servicetypesdir}/nepomukservice2.desktop
%{kde4_datadir}/polkit-1/actions/org.kde.nepomuk.filewatch.policy

%files devel
#%{_kde4_libdir}/libnepomuksync.so
%{_kde4_libdir}/cmake/NepomukCore/
%{_kde4_includedir}/nepomuk2/
%{_kde4_includedir}/Nepomuk2/
%{kde4_libdir}/*.so

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files libs
%{_kde4_libdir}/kde4/*.so
%{_kde4_libdir}/libnepomukcommon.so
%{_kde4_libdir}/libnepomukcore.so.4*
#%{_kde4_libdir}/libnepomuksync.so.4*


%changelog
* Tue Oct 21 2014 Liu Di <liudidi@gmail.com> - 4.14.2-1
- 更新到 4.14.2

* Fri Jul 18 2014 Liu Di <liudidi@gmail.com> - 4.13.3-1
- 更新到 4.13.3

* Wed Jun 18 2014 Liu Di <liudidi@gmail.com> - 4.13.2-1
- 更新到 4.13.2

* Wed Apr 23 2014 Liu Di <liudidi@gmail.com> - 4.13.0-8
- 为 Magic 3.0 重建

* Fri Jul 05 2013 Liu Di <liudidi@gmail.com> - 4.10.4-7
- 为 Magic 3.0 重建

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 4.9.3-6
- 为 Magic 3.0 重建


