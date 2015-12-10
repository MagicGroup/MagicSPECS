Name:    kde4-kactivities
%define real_name kactivities
Summary: API for using and interacting with Activities 
Summary(zh_CN.UTF-8): 使用和与 Activities 交互的 API
Version: 4.14.3
Release: 3%{?dist}

License: GPLv2+ and LGPLv2+
URL:     https://projects.kde.org/projects/kde/kdelibs/kactivities
%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0: ftp://ftp.kde.org/pub/kde/%{stable}/4.13.3/src/%{real_name}-4.13.3.tar.xz

BuildRequires: kdelibs4-devel >= %{version}

Requires: kdelibs4%{?_isa}%{?_kde4_version: >= %{_kde4_version}}

# libkactivities moved from kdelibs, but turns out there's no actual conflicts
# kactivitymanagerd moved here from kde-runtime 
Conflicts: kdebase-runtime < 4.7.3-10

Obsoletes: libkactivities < 6.1-100
Provides:  libkactivities = 6.1-100

%description
API for using and interacting with Activities as a consumer, 
application adding information to them or as an activity manager.

%description -l zh_CN.UTF-8
使用和与 Activities 交互的 API。

%package devel
Summary: Developer files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发文件 
Obsoletes: libkactivities-devel < 6.1-100
Provides:  libkactivities-devel = 6.1-100
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: kdelibs4-devel
%description devel
%{summary}.

%description devel -l zh_CN.UTF-8
%{name} 的开发文件。


%prep
%setup -q -n %{real_name}-4.13.3


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}
magic_rpm_clean.sh

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{_kde4_bindir}/kactivitymanagerd
%{_kde4_libdir}/libkactivities.so.6*
%{_kde4_libdir}/kde4/activitymanager_plugin_globalshortcuts.so
%{_kde4_libdir}/kde4/activitymanager_plugin_slc.so
%{_kde4_libdir}/kde4/activitymanager_plugin_sqlite.so
#%{_kde4_libdir}/kde4/activitymanager_uihandler_declarative.so
#%{_kde4_libdir}/kde4/activitymanager_uihandler_kdialog.so
%{_kde4_libdir}/kde4/kactivitymanagerd_fileitem_linking_plugin.so
%{_kde4_libdir}/kde4/kio_activities.so
%{_kde4_libdir}/kde4/activitymanager_plugin_activityranking.so
%{_kde4_libdir}/kde4/activitymanager_plugin_virtualdesktopswitch.so
%{_kde4_libdir}/kde4/imports/org/kde/activities/models/libkactivities-models-component-plugin.so
%{_kde4_libdir}/kde4/imports/org/kde/activities/models/qmldir
%{_kde4_libdir}/kde4/kcm_activities.so
%{_kde4_libdir}/libkactivities-models.so.*
%{_kde4_datadir}/apps/activitymanager/workspace/settings/BlacklistApplicationView.qml
%{kde4_servicesdir}/activitymanager-plugin-activityranking.desktop
%{kde4_servicesdir}/activitymanager-plugin-virtualdesktopswitch.desktop
%{kde4_servicesdir}/kcm_activities.desktop
%{_kde4_datadir}/kde4/services/activities.protocol
%{_kde4_datadir}/kde4/services/activitymanager-plugin-globalshortcuts.desktop
%{_kde4_datadir}/kde4/services/activitymanager-plugin-slc.desktop
%{_kde4_datadir}/kde4/services/activitymanager-plugin-sqlite.desktop
%{_kde4_datadir}/kde4/services/kactivitymanagerd_fileitem_linking_plugin.desktop
%{_kde4_datadir}/kde4/services/kactivitymanagerd.desktop
%{_kde4_datadir}/kde4/servicetypes/activitymanager-plugin.desktop
%{_kde4_datadir}/ontology/kde/
%{_kde4_libdir}/kde4/activitymanager_plugin_nepomuk.so
%{_kde4_datadir}/kde4/services/activitymanager-plugin-nepomuk.desktop
#%dir %{_kde4_appsdir}/plasma/packages/
#%{_kde4_appsdir}/plasma/packages/org.kde.ActivityManager.UiHandler/

%files devel
%{_kde4_libdir}/libkactivities.so
%{_kde4_libdir}/cmake/KActivities/
%{_kde4_libdir}/pkgconfig/libkactivities.pc
%{_kde4_includedir}/KDE/KActivities/
%{_kde4_includedir}/kactivities/
%{_kde4_includedir}/kactivities-models/
%{_kde4_libdir}/cmake/KActivities-Models/
%{_kde4_libdir}/libkactivities-models.so
%{_kde4_libdir}/pkgconfig/libkactivities-models.pc

%changelog
* Sun Nov 08 2015 Liu Di <liudidi@gmail.com> - 4.14.3-3
- 为 Magic 3.0 重建

* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 4.14.3-2
- 为 Magic 3.0 重建

* Tue Dec 30 2014 Liu Di <liudidi@gmail.com> - 4.14.3-1
- 更新到 4.14.3

* Tue Oct 21 2014 Liu Di <liudidi@gmail.com> - 4.14.2-1
- 更新到 4.14.2

* Fri Jul 18 2014 Liu Di <liudidi@gmail.com> - 4.13.3-1
- 更新到 4.13.3

* Wed Jun 18 2014 Liu Di <liudidi@gmail.com> - 4.13.2-1
- 更新到 4.13.2

* Sat May 24 2014 Liu Di <liudidi@gmail.com> - 4.13.1-1
- 更新到 4.13.1

* Wed Apr 23 2014 Liu Di <liudidi@gmail.com> - 4.13.0-2
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 4.9.3-2
- 为 Magic 3.0 重建


